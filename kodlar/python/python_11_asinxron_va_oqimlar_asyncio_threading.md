# Python Dasturlash Tili — 11-Qism: Asinxron Dasturlash va Oqimlar (Asyncio, Threading, Multiprocessing)
## (501-550 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam zamonaviy yuqori tezlikdagi parallel va asinxron tizimlar yaratishni qamrab oladi:
* `asyncio` asoslari: `async/await`, `asyncio.run()`, `asyncio.gather()`, `create_task`;
* No-blocking I/O, `asyncio.wait_for`, timeout, vazifalarni bekor qilish (`cancel`);
* Ko'p oqimlilik (`threading`): `Thread`, `join()`, `Lock`, `RLock`, `Event`, `Barrier`, `Queue`;
* Ko'p protsessorlilik (`multiprocessing`): CPU-bound vazifalar, GIL cheklovini yechish, `ProcessPoolExecutor`;
* Asinxron semaforlar, asinxron generatorlar, TTL kesh, Producer-Consumer arxitekturasi;

---

# 501-Topshiriq: asyncio va async/await asoslari

## Topshiriq sharti:
Asinxron funksiya (korutina) e'lon qilish va `asyncio.run()` orqali uni ishga tushirish.

## Yechim (Python kodi):
```python
import asyncio

async def salom():
    print("Salom...")
    await asyncio.sleep(1)  # No-blocking kechikish
    print("...Dunyo!")

asyncio.run(salom())
```

## Tushuntirish va Mantiq:
1. `async def` korutina (coroutine) yaratadi.
2. `await` boshqa vazifalarga navbat berib no-blocking (to'xtab qolmaydigan) kutishni ta'minlaydi.
3. `asyncio.run()` hodisalar tsiklini (Event Loop) ochib boshqaradi.

## Ishlash natijasi:
```text
Chiqish: Salom... (1 soniya) ...Dunyo!
```


# 502-Topshiriq: Parallel vazifalarni bir vaqtda bajarish (asyncio.gather)

## Topshiriq sharti:
Bir nechta asinxron vazifani `asyncio.gather()` yordamida parallel ishga tushirib, umumiy vaqtni tejang.

## Yechim (Python kodi):
```python
import asyncio
import time

async def yuklash(nom, soniya):
    print(f"[{nom}] yuklanish boshlandi...")
    await asyncio.sleep(soniya)
    print(f"[{nom}] yuklab bo'lindi ({soniya}s).")
    return f"{nom}_malumot"

async def main():
    boshlandi = time.perf_counter()
    natijalar = await asyncio.gather(
        yuklash("Kitob 1", 2),
        yuklash("Kitob 2", 1),
        yuklash("Kitob 3", 1.5)
    )
    sarflandi = time.perf_counter() - boshlandi
    print(f"Barcha yuklashlar yakunlandi: {natijalar}")
    print(f"Jami ketgan vaqt: {sarflandi:.2f} soniya (ketma-ket 4.5s o'rniga ~2s!)")

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `asyncio.gather(*tasks)` bir vaqtda barcha vazifalarni ishga tushirib umumiy vaqtni eng uzoq vazifa vaqtiga tenglashtiradi.

## Ishlash natijasi:
```text
Chiqish: Jami ketgan vaqt: ~2.00 soniya.
```


# 503-Topshiriq: Asinxron vazifalarni bekor qilish (Task Cancellation)

## Topshiriq sharti:
Uzoq davom etayotgan vazifani `task.cancel()` orqali bekor qilish va `asyncio.CancelledError` ni ushlash.

## Yechim (Python kodi):
```python
import asyncio

async def uzoq_amal():
    try:
        print("Uzoq amal boshlandi...")
        await asyncio.sleep(10)
        print("Amal yakunlandi!")
    except asyncio.CancelledError:
        print("[BEKOR QILINDI] Vazifa muvaffaqiyatli to'xtatildi!")
        raise

async def main():
    task = asyncio.create_task(uzoq_amal())
    await asyncio.sleep(0.5)
    print("Vazifani bekor qilish buyrug'i berilmoqda...")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Asosiy dastur bekor qilinganini tasdiqladi.")

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `task.cancel()` korutinaga `CancelledError` yuborib uni xavfsiz to'xtatish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: Uzoq amal boshlandi... -> [BEKOR QILINDI] -> Bekor qilingani tasdiqlandi.
```


# 504-Topshiriq: Asinxron Timeout (asyncio.wait_for)

## Topshiriq sharti:
Vazifa belgilangan vaqt ichida bajarilmasa `TimeoutError` chaqiruvchi himoya mexanizmi.

## Yechim (Python kodi):
```python
import asyncio

async def sekin_sorov():
    await asyncio.sleep(3)
    return "Server javobi"

async def main():
    try:
        # Maksimal 1 soniya kutamiz
        javob = await asyncio.wait_for(sekin_sorov(), timeout=1.0)
        print(javob)
    except asyncio.TimeoutError:
        print("[TIMEOUT] Server belgilangan 1 soniya ichida javob bermadi!")

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `asyncio.wait_for(fut, timeout)` tarmoq qotib qolganda dastur osilib qolishidan asraydi.

## Ishlash natijasi:
```text
Chiqish: [TIMEOUT] Server belgilangan 1 soniya ichida javob bermadi!
```


# 505-Topshiriq: Oqimlar bilan ishlash asoslari (threading.Thread)

## Topshiriq sharti:
`threading.Thread` yordamida alohida operatsion tizim oqimida funksiyani ishga tushirish.

## Yechim (Python kodi):
```python
import threading
import time

def orqa_fon_ish(nom):
    print(f"[{nom}] Fon oqimida ish boshlandi...")
    time.sleep(1)
    print(f"[{nom}] Fon oqimida ish yakunlandi.")

t1 = threading.Thread(target=orqa_fon_ish, args=("Oqim-1",))
t2 = threading.Thread(target=orqa_fon_ish, args=("Oqim-2",))

t1.start()
t2.start()

# Oqimlar tugashini kutamiz
t1.join()
t2.join()

print("Barcha oqimlar yakunlandi.")
```

## Tushuntirish va Mantiq:
1. `t.start()` yangi oqimni boshlaydi.
2. `t.join()` asosiy dastur ushbu oqim to'liq tugashini kutishini ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: [Oqim-1] va [Oqim-2] parallel ishlaydi, Barcha oqimlar yakunlandi.
```


# 506-Topshiriq: Race Condition va Oqimlar qulfi (threading.Lock)

## Topshiriq sharti:
Bir vaqtda bitta umumiy hisoblagichga yozayotgan oqimlarni `Lock` yordamida himoyalang.

## Yechim (Python kodi):
```python
import threading

hisoblagich = 0
qulf = threading.Lock()

def oshir():
    global hisoblagich
    for _ in range(100_000):
        with qulf:  # Tanqidiy sohani himoyalaymiz
            hisoblagich += 1

t1 = threading.Thread(target=oshir)
t2 = threading.Thread(target=oshir)

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Kutilgan: 200,000 | Haqiqiy natija: {hisoblagich}")
```

## Tushuntirish va Mantiq:
1. `with qulf:` bir vaqtning o'zida faqat bitta oqim o'zgaruvchini tahrirlashini kafolatlaydi, aks holda Race Condition xatosi kelib chiqadi.

## Ishlash natijasi:
```text
Chiqish: Kutilgan: 200,000 | Haqiqiy natija: 200000
```


# 507-Topshiriq: Ko'p oqimli xavfsiz navbat (queue.Queue)

## Topshiriq sharti:
Ishlab chiqaruvchi (Producer) va Iste'molchi (Consumer) o'rtasida ma'lumotlarni xavfsiz uzatuvchi navbat.

## Yechim (Python kodi):
```python
import threading
import queue
import time

q = queue.Queue()

def producer():
    for i in range(1, 4):
        item = f"Vazifa-{i}"
        q.put(item)
        print(f"[PRODUCER] Qo'shildi: {item}")
        time.sleep(0.1)

def consumer():
    while True:
        try:
            item = q.get(timeout=0.5)
            print(f" -> [CONSUMER] Bajarildi: {item}")
            q.task_done()
        except queue.Empty:
            break

t_prod = threading.Thread(target=producer)
t_cons = threading.Thread(target=consumer)

t_prod.start()
t_cons.start()

t_prod.join()
t_cons.join()
print("Navbatdagi barcha ishlar bajarildi.")
```

## Tushuntirish va Mantiq:
1. `queue.Queue` o'z ichida ichki qulflarga ega bo'lib, oqimlar o'rtasida xavfsiz (thread-safe) ma'lumot almashadi.

## Ishlash natijasi:
```text
Chiqish: Producer vazifa qo'shadi, Consumer ularni qayta ishlaydi.
```


# 508-Topshiriq: Oqimlar havzasi (ThreadPoolExecutor)

## Topshiriq sharti:
`concurrent.futures.ThreadPoolExecutor` orqali 4 ta parallel oqimda ro'yxatni tezkor qayta ishlang.

## Yechim (Python kodi):
```python
from concurrent.futures import ThreadPoolExecutor
import time

def kvadratini_ol(n):
    time.sleep(0.1)
    return n * n

sonlar = [1, 2, 3, 4, 5, 6, 7, 8]

with ThreadPoolExecutor(max_workers=4) as executor:
    natijalar = list(executor.map(kvadratini_ol, sonlar))

print("Asl sonlar:", sonlar)
print("Kvadratlari:", natijalar)
```

## Tushuntirish va Mantiq:
1. `ThreadPoolExecutor` oqimlarni o'zi boshqaradi, navbatga qo'yadi va natijalarni yig'ib beradi.

## Ishlash natijasi:
```text
Chiqish: Kvadratlari: [1, 4, 9, 16, 25, 36, 49, 64]
```


# 509-Topshiriq: Ko'p protsessorlilik (multiprocessing: CPU-bound vazifalar)

## Topshiriq sharti:
Python GIL (Global Interpreter Lock) cheklovini yorib o'tib, ko'p yadroli protsessorda og'ir hisoblashlarni parallel bajarish.

## Yechim (Python kodi):
```python
import multiprocessing
import time

def ogir_hisob(n):
    return sum(i * i for i in range(n))

if __name__ == '__main__':
    # 2 ta alohida jarayon (process) ochamiz
    with multiprocessing.Pool(processes=2) as pool:
        natijalar = pool.map(ogir_hisob, [10_000_000, 10_000_000])
    print("Ko'p yadroli hisoblash natijalari:", natijalar)
```

## Tushuntirish va Mantiq:
1. `multiprocessing` alohida Python jarayonlari ochadi, har biri o'z GILiga ega va turli CPU yadrolarida 100% quvvatda ishlaydi.

## Ishlash natijasi:
```text
Chiqish: Ko'p yadroli hisoblash natijalari: [333333283333335000000, ...]
```


# 510-Topshiriq: Asinxron Semafor (asyncio.Semaphore)

## Topshiriq sharti:
Bir vaqtning o'zida maksimal 2 ta so'rov bajarilishini cheklovchi asinxron semafor tuzing.

## Yechim (Python kodi):
```python
import asyncio

semafor = asyncio.Semaphore(2)

async def cheklangan_sorov(id):
    async with semafor:
        print(f"[START #{id}] Bajarilmoqda (maksimal 2 ta bir vaqtda)...")
        await asyncio.sleep(1)
        print(f"[FINISH #{id}] Tugadi.")

async def main():
    vazifalar = [cheklangan_sorov(i) for i in range(1, 5)]
    await asyncio.gather(*vazifalar)

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `Semaphore(n)` serverga yoki ma'lumotlar bazasiga haddan tashqari ko'p so'rov tushib ketishidan (Rate Limiting) himoya qiladi.

## Ishlash natijasi:
```text
Chiqish: Dastlab #1 va #2 ishlaydi, keyin #3 va #4 ga navbat keladi.
```


# 511-Topshiriq: Asinxron Generatorlar (async for va async def)

## Topshiriq sharti:
`yield` orqali asinxron ma'lumot oqimini generatsiya qilish va uni `async for` bilan o'qish.

## Yechim (Python kodi):
```python
import asyncio

async def asinxron_sanoq(maks):
    for i in range(1, maks + 1):
        await asyncio.sleep(0.2)
        yield i

async def main():
    print("Asinxron oqim boshlandi:")
    async for son in asinxron_sanoq(3):
        print(f"Kelgan qiymat: {son}")

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `async for` veb-soketlar, chat xabarlari yoki real vaqt oqimlarini no-blocking qabul qilishda ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Kelgan qiymat: 1, 2, 3
```


# 512-Topshiriq: Daemon oqimlar (Daemon Threads)

## Topshiriq sharti:
Asosiy dastur tugashi bilan avtomatik o'chadigan fon monitoring oqimini yaratish.

## Yechim (Python kodi):
```python
import threading
import time

def fon_kuzatuvchi():
    while True:
        print("[DAEMON] Tizim holati: Barcha xizmatlar barqaror.")
        time.sleep(0.5)

d_oqim = threading.Thread(target=fon_kuzatuvchi, daemon=True)
d_oqim.start()

time.sleep(1.2)
print("Asosiy dastur yakunlandi — Daemon ham darhol to'xtaydi.")
```

## Tushuntirish va Mantiq:
1. `daemon=True` o'rnatilgan oqimlar asosiy dastur yopilishi bilan birga avtomatik o'chiriladi, osilib qolmaydi.

## Ishlash natijasi:
```text
Chiqish: [DAEMON] kuzatuv... Asosiy dastur yakunlandi.
```


# 513-Topshiriq: Asinxron Kontekst Menejeri (async with)

## Topshiriq sharti:
`__aenter__` va `__aexit__` metodlari orqali asinxron ulanish resurslarini xavfsiz boshqarish.

## Yechim (Python kodi):
```python
import asyncio

class AsinxronUlanish:
    async def __aenter__(self):
        print("[ULANISH] Serverga asinxron ulanmoqda...")
        await asyncio.sleep(0.5)
        print("[ULANISH] Ulandi!")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("[UZILISH] Ulanish yopilmoqda...")
        await asyncio.sleep(0.2)
        print("[UZILISH] Yopildi.")

async def main():
    async with AsinxronUlanish():
        print(" -> Asinxron ma'lumotlar almashinuvi ketmoqda...")

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `async with` asinxron ma'lumotlar bazalari (AsyncPG, Tortoise ORM) va HTTP klientlarda (aiohttp, httpx) asosiy vositadir.

## Ishlash natijasi:
```text
Chiqish: [ULANISH]... Ma'lumotlar almashinuvi... [UZILISH]...
```


# 514-Topshiriq: Oqimlar o'rtasida signal uzatish (threading.Event)

## Topshiriq sharti:
Bitta oqim boshqa oqimlarga 'boshlash' signalini `Event.set()` orqali yuboruvchi sinxronizatsiya.

## Yechim (Python kodi):
```python
import threading
import time

start_signali = threading.Event()

def poygachi(nom):
    print(f"[{nom}] Start chizig'ida signal kutmoqda...")
    start_signali.wait()  # Signal berilguncha to'xtab turadi
    print(f"[{nom}] Yugurishni boshladi!")

t1 = threading.Thread(target=poygachi, args=("1-poygachi",))
t2 = threading.Thread(target=poygachi, args=("2-poygachi",))

t1.start()
t2.start()

time.sleep(0.5)
print("\n🏁 [HAKAM] START SIGNALI BERILDI! 🏁\n")
start_signali.set()

t1.join()
t2.join()
```

## Tushuntirish va Mantiq:
1. `Event.wait()` bayroq `True` bo'lguncha bloklaydi, `Event.set()` esa barcha kutayotgan oqimlarni bir zumda uyg'otadi.

## Ishlash natijasi:
```text
Chiqish: Start chizig'ida... START SIGNALI BERILDI! Yugurishni boshladi!
```


# 515-Topshiriq: Asinxron Queue (asyncio.Queue)

## Topshiriq sharti:
Asinxron korutinalar o'rtasida FIFO navbat orqali xavfsiz vazifalar taqsimlash.

## Yechim (Python kodi):
```python
import asyncio

async def ishchi(nom, navbat):
    while True:
        vazifa = await navbat.get()
        print(f"[{nom}] '{vazifa}' ustida ishlamoqda...")
        await asyncio.sleep(0.3)
        navbat.task_done()

async def main():
    navbat = asyncio.Queue()
    # 2 ta ishchi ishga tushiramiz
    ishchilar = [asyncio.create_task(ishchi(f"Ishchi-{i}", navbat)) for i in range(1, 3)]

    # Navbatga 4 ta ish qo'shamiz
    for i in range(1, 5):
        await navbat.put(f"Kitob-{i}.pdf")

    await navbat.join()  # Barcha ishlar tugashini kutamiz
    for ish in ishchilar:
        ish.cancel()

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `asyncio.Queue` yordamida veb-kroulerlar va ko'p oqimli fayl yuklovchi asinxron tizimlar yasaladi.

## Ishlash natijasi:
```text
Chiqish: Ishchilar vazifalarni parallel navbatdan olib bajaradi.
```


# 516-Topshiriq: Qayta kiruvchi qulf (threading.RLock)

## Topshiriq sharti:
Bitta oqim bir nechta ichma-ich metodlarda bir xil qulfni qayta-qayta qulflashi uchun `RLock` ishlatish.

## Yechim (Python kodi):
```python
import threading

rlock = threading.RLock()

def ichki_amal():
    with rlock:
        print("Ichki amal bajarildi.")

def tashqi_amal():
    with rlock:
        print("Tashqi amal boshlandi...")
        ichki_amal()  # Oddiy Lock bo'lsa deadlock bo'lardi!
        print("Tashqi amal tugadi.")

t = threading.Thread(target=tashqi_amal)
t.start()
t.join()
```

## Tushuntirish va Mantiq:
1. `RLock` (Reentrant Lock) qulfni egallagan oqimga uni yana bir necha marta qulflashga ruxsat beradi.

## Ishlash natijasi:
```text
Chiqish: Tashqi amal boshlandi... -> Ichki amal bajarildi -> Tashqi tugadi.
```


# 517-Topshiriq: CPU-bound va IO-bound operatsiyalari taqqoslashi

## Topshiriq sharti:
Tarmoq/Disk kutish (IO-bound) va og'ir matematik hisob (CPU-bound) farqini ko'rsatuvchi arxitektura.

## Yechim (Python kodi):
```python
import time

def io_bound_simulyatsiya():
    time.sleep(0.5)  # Diskdan o'qish yoki tarmoq kutish
    return "IO Bajarildi"

def cpu_bound_simulyatsiya():
    return sum(i for i in range(5_000_000))  # Protsessor hisobi

b1 = time.perf_counter()
io_bound_simulyatsiya()
print(f"IO-bound vaqt : {time.perf_counter() - b1:.3f}s (asyncio/threading uchun mos)")

b2 = time.perf_counter()
cpu_bound_simulyatsiya()
print(f"CPU-bound vaqt: {time.perf_counter() - b2:.3f}s (multiprocessing uchun mos)")
```

## Tushuntirish va Mantiq:
1. IO-bound amallar uchun `asyncio` yoki `threading`, CPU-bound og'ir hisoblar uchun esa `multiprocessing` tanlanadi.

## Ishlash natijasi:
```text
Chiqish: IO-bound vaqt: ~0.5s, CPU-bound vaqt: ~0.2s
```


# 518-Topshiriq: Asinxron ulanishlarni boshqaruvchi Connection Pool

## Topshiriq sharti:
Cheklangan miqdordagi ulanishlarni navbat bilan foydalanuvchilarga beruvchi asinxron resurs hovuzi.

## Yechim (Python kodi):
```python
import asyncio

class AsyncConnectionPool:
    def __init__(self, size=2):
        self.semaphore = asyncio.Semaphore(size)

    async def execute_query(self, query_id):
        async with self.semaphore:
            print(f"[BAZA] #{query_id} so'rovi ulandi...")
            await asyncio.sleep(0.5)
            print(f"[BAZA] #{query_id} so'rovi yakunlandi.")

async def main():
    pool = AsyncConnectionPool(size=2)
    await asyncio.gather(*(pool.execute_query(i) for i in range(1, 5)))

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. Ma'lumotlar bazasi ulanishlari sonini me'yorda saqlash uchun connection pool ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: So'rovlar ikkitadan parallel bajariladi.
```


# 519-Topshiriq: Protsesslar o'rtasida ma'lumot almashish (multiprocessing.Queue)

## Topshiriq sharti:
Mustaqil operatsion tizim jarayonlari o'rtasida ma'lumot uzatuvchi xavfsiz navbat.

## Yechim (Python kodi):
```python
import multiprocessing

def ishchi_jarayon(navbat):
    navbat.put("Salom asosiy jarayon, men yangi CPU yadrosidan yozmoqdaman!")

if __name__ == '__main__':
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=ishchi_jarayon, args=(q,))
    p.start()
    p.join()
    xabar = q.get()
    print("Qabul qilingan xabar:", xabar)
```

## Tushuntirish va Mantiq:
1. Protsesslar umumiy xotiraga ega bo'lmagani uchun IPC (Inter-Process Communication) orqali xabar almashadi.

## Ishlash natijasi:
```text
Chiqish: Qabul qilingan xabar: Salom asosiy jarayon...
```


# 520-Topshiriq: Asinxron hodisalar eshittiruvchi (Event Emitter)

## Topshiriq sharti:
Hodisa yuz berganda unga obuna bo'lgan barcha asinxron tinglovchilarni chaqiruvchi arxitektura.

## Yechim (Python kodi):
```python
import asyncio

class AsyncEventEmitter:
    def __init__(self):
        self.tinglovchilar = []

    def obuna(self, korutina):
        self.tinglovchilar.append(korutina)

    async def tarqatish(self, xabar):
        await asyncio.gather(*(t(xabar) for t in self.tinglovchilar))

async def sms_xizmati(xabar):
    print(f"📱 [SMS] Foydalanuvchiga yuborildi: {xabar}")

async def email_xizmati(xabar):
    print(f"📧 [EMAIL] Foydalanuvchiga yuborildi: {xabar}")

async def main():
    hub = AsyncEventEmitter()
    hub.obuna(sms_xizmati)
    hub.obuna(email_xizmati)
    await hub.tarqatish("Sizning buyurtmangiz jo'natildi!")

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. Event-driven asinxron arxitekturada bir nechta xizmatlar mustaqil xabarnoma oladi.

## Ishlash natijasi:
```text
Chiqish: SMS va EMAIL bir vaqtda xabar oladi.
```


# 521-Topshiriq: Oqimlar xotirasini chegaralovchi Thread-Local Storage

## Topshiriq sharti:
`threading.local()` yordamida har bir oqim uchun faqat o'zigagina tegishli bo'lgan shaxsiy o'zgaruvchi yaratish.

## Yechim (Python kodi):
```python
import threading

shaxsiy_xotira = threading.local()

def vazifa(foydalanuvchi):
    shaxsiy_xotira.foydalanuvchi = foydalanuvchi
    print(f"[{threading.current_thread().name}] Foydalanuvchi: {shaxsiy_xotira.foydalanuvchi}")

t1 = threading.Thread(target=vazifa, args=("Alisher",), name="Oqim-A")
t2 = threading.Thread(target=vazifa, args=("Jasur",), name="Oqim-B")

t1.start()
t2.start()
t1.join()
t2.join()
```

## Tushuntirish va Mantiq:
1. `threading.local()` o'zgaruvchisi har bir oqimda alohida saqlanadi va bir-biriga xalaqit bermaydi.

## Ishlash natijasi:
```text
Chiqish: [Oqim-A] Alisher, [Oqim-B] Jasur
```


# 522-Topshiriq: Asinxron parallel yuklovchi (Concurrent File Downloader)

## Topshiriq sharti:
Bir nechta fayllar URL ro'yxatini parallel yuklovchi asinxron pipeline simulyatsiyasi.

## Yechim (Python kodi):
```python
import asyncio

async def fayl_yukla(fayl_nomi):
    print(f"Yuklanmoqda: {fayl_nomi}")
    await asyncio.sleep(0.3)
    return f"Toza {fayl_nomi}"

async def main():
    fayllar = [f"kitob_{i}.txt" for i in range(1, 6)]
    natijalar = await asyncio.gather(*(fayl_yukla(f) for f in fayllar))
    print(f"Jami yuklandi: {len(natijalar)} ta fayl.")

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. Parallel yuklash tarmoq kutish vaqtlarini nolga tenglashtiradi.

## Ishlash natijasi:
```text
Chiqish: 5 ta fayl bir vaqtda yuklanadi.
```


# 523-Topshiriq: Oqimlar to'sig'i (threading.Barrier)

## Topshiriq sharti:
Belgilangan N ta oqim hammasi bitta nuqtaga yetib kelmaguncha hech birini oldinga o'tkazmaydigan Barrier.

## Yechim (Python kodi):
```python
import threading
import time

tosik = threading.Barrier(3)  # 3 ta oqim kutiladi

def ishchi(raqam):
    print(f"Ishchi #{raqam} to'siqqa yetib keldi.")
    tosik.wait()  # Barcha 3 tasi kelguncha kutadi
    print(f"🚀 Ishchi #{raqam} to'siqdan birga o'tib ketdi!")

for i in range(1, 4):
    threading.Thread(target=ishchi, args=(i,)).start()
```

## Tushuntirish va Mantiq:
1. `Barrier` bir nechta parallel jarayonlarni bir xil vaqtda start olishga majburlaydi.

## Ishlash natijasi:
```text
Chiqish: 3 ta ishchi yetib keladi, so'ng birgalikda o'tadi.
```


# 524-Topshiriq: Asinxron Sleep va Bloklovchi Time Sleep farqi

## Topshiriq sharti:
`time.sleep()` butun hodisalar zanjirini muzlatib qo'yishi va nima uchun `asyncio.sleep()` shartligini ko'rsating.

## Yechim (Python kodi):
```python
import asyncio
import time

async def xizmat_a():
    await asyncio.sleep(0.5)
    print("Xizmat A ishladi.")

async def xizmat_b():
    await asyncio.sleep(0.5)
    print("Xizmat B ishladi.")

async def main():
    # To'g'ri no-blocking usul:
    boshlandi = time.perf_counter()
    await asyncio.gather(xizmat_a(), xizmat_b())
    print(f"Vaqt: {time.perf_counter() - boshlandi:.2f}s")

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `asyncio.sleep()` Event Loopni bo'shatadi, `time.sleep()` esa butun dasturni bitta joyda qotirib qo'yadi.

## Ishlash natijasi:
```text
Chiqish: Xizmat A va B ~0.5 soniyada bajariladi.
```


# 525-Topshiriq: Protsesslar o'rtasida umumiy xotira (multiprocessing.Value)

## Topshiriq sharti:
Ikki jarayon bitta xotira katagidagi sonni xavfsiz boshqarishini ko'rsating.

## Yechim (Python kodi):
```python
import multiprocessing

def qadam(son, lock):
    for _ in range(5000):
        with lock:
            son.value += 1

if __name__ == '__main__':
    umumiy_son = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
    p1 = multiprocessing.Process(target=qadam, args=(umumiy_son, lock))
    p2 = multiprocessing.Process(target=qadam, args=(umumiy_son, lock))
    p1.start(); p2.start()
    p1.join(); p2.join()
    print("Yakuniy umumiy son:", umumiy_son.value)
```

## Tushuntirish va Mantiq:
1. `multiprocessing.Value` umumiy C-darajasidagi xotira ajratadi.

## Ishlash natijasi:
```text
Chiqish: Yakuniy umumiy son: 10000
```


# 526-Topshiriq: Asinxron Periodic Ticker (Dinamik fon soati)

## Topshiriq sharti:
Har soniyada vaqtni fonda ekranga chiqarib turuvchi asinxron soat vazifasi.

## Yechim (Python kodi):
```python
import asyncio

async def fon_soati():
    for i in range(1, 4):
        await asyncio.sleep(0.5)
        print(f"[SOAT TICK]: {i * 0.5} soniya o'tdi")

async def asosiy_ish():
    print("Asosiy ish boshlandi.")
    await asyncio.sleep(1.6)
    print("Asosiy ish tugadi.")

async def main():
    await asyncio.gather(fon_soati(), asosiy_ish())

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. Asinxron rejimda interfeys qotmasdan orqa fonda soat yoki monitoring ishlab turadi.

## Ishlash natijasi:
```text
Chiqish: [SOAT TICK]... Asosiy ish tugadi.
```


# 527-Topshiriq: Qo'shimcha CPU yadrolari sonini aniqlash (os.cpu_count)

## Topshiriq sharti:
Tizimdagi mantiqiy protsessor yadrolari sonini bilib, oqimlar sonini shunga moslang.

## Yechim (Python kodi):
```python
import os

yadrolar = os.cpu_count()
print(f"Ushbu kompyuterdagi CPU yadrolari soni: {yadrolar} ta")
optimal_worker = yadrolar * 2
print(f"IO vazifalar uchun tavsiya etilgan oqimlar: {optimal_worker} ta")
```

## Tushuntirish va Mantiq:
1. Server quvvatiga qarab optimal workerlar sonini avtomatik hisoblash vositasi.

## Ishlash natijasi:
```text
Chiqish: CPU yadrolari soni: ... ta
```


# 528-Topshiriq: Asinxron Retry qobig'i (Async Retry Decorator)

## Topshiriq sharti:
Asinxron funksiyada xatolik bo'lsa 3 martagacha qayta urinuvchi asinxron dekorator.

## Yechim (Python kodi):
```python
import asyncio
import functools

def async_retry(urinishlar=3):
    def dekorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for u in range(1, urinishlar + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if u == urinishlar: raise
                    print(f"[QAYTA URINISH #{u}] {e}")
                    await asyncio.sleep(0.2)
        return wrapper
    return dekorator

@async_retry(3)
async def tarmoq_chaqiruvi():
    raise ConnectionResetError("Tarmoq vaqtincha uzildi")

async def main():
    try:
        await tarmoq_chaqiruvi()
    except ConnectionResetError:
        print("Maksimal urinishlar tugadi.")

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. Asinxron backend tizimlarida ishonchlilikni ta'minlovchi universal qobiq.

## Ishlash natijasi:
```text
Chiqish: [QAYTA URINISH #1]... [QAYTA URINISH #2]... Maksimal urinishlar tugadi.
```


# 529-Topshiriq: Asinxron lock bilan bir vaqtda faylga yozishni himoyalash

## Topshiriq sharti:
`asyncio.Lock` orqali bir nechta korutinalarning bir faylga to'qnashuvsiz yozishini ta'minlang.

## Yechim (Python kodi):
```python
import asyncio

fayl_qulfi = asyncio.Lock()

async def xavfsiz_yoz(matn):
    async with fayl_qulfi:
        print(f"Yozilmoqda: '{matn}'")
        await asyncio.sleep(0.1)
        print(f"Yozildi: '{matn}'")

async def main():
    await asyncio.gather(
        xavfsiz_yoz("1-qator"),
        xavfsiz_yoz("2-qator"),
        xavfsiz_yoz("3-qator")
    )

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `asyncio.Lock` bir vaqtda faqat bitta korutina faylga yozishini ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Tartib bilan xavfsiz yoziladi.
```


# 530-Topshiriq: Ko'p oqimli loggerni boshqarish

## Topshiriq sharti:
Turli oqimlardan kelayotgan xabarlarda oqim nomini aniq ko'rsatuvchi logging tizimi.

## Yechim (Python kodi):
```python
import threading
import logging

logging.basicConfig(level=logging.INFO, format='[%(threadName)s] %(message)s')

def vazifa():
    logging.info("Vazifa bajarilmoqda.")

t1 = threading.Thread(target=vazifa, name="Worker-A")
t2 = threading.Thread(target=vazifa, name="Worker-B")

t1.start(); t2.start()
t1.join(); t2.join()
```

## Tushuntirish va Mantiq:
1. `%(threadName)s` loglarda qaysi oqim nima qilganini aniq ajratib beradi.

## Ishlash natijasi:
```text
Chiqish: [Worker-A] Vazifa... [Worker-B] Vazifa...
```


# 531-Topshiriq: Asinxron Shart O'zgaruvchisi (asyncio.Condition)

## Topshiriq sharti:
Biror shart bajarilishini kutib yotgan korutinalarni `notify_all()` bilan uyg'otish.

## Yechim (Python kodi):
```python
import asyncio

shart = asyncio.Condition()
tayyormi = False

async def kutuvchi(nom):
    async with shart:
        while not tayyormi:
            await shart.wait()
        print(f"[{nom}] Boshladi!")

async def signalchi():
    global tayyormi
    await asyncio.sleep(0.5)
    async with shart:
        tayyormi = True
        shart.notify_all()
        print("[SIGNAL] Barcha kutuvchilarga ruxsat berildi!")

async def main():
    await asyncio.gather(kutuvchi("A"), kutuvchi("B"), signalchi())

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `Condition` murakkab holatlar sinxronizatsiyasini boshqaradi.

## Ishlash natijasi:
```text
Chiqish: [SIGNAL]... [A] Boshladi! [B] Boshladi!
```


# 532-Topshiriq: Oqimlar havzasi bilan tezkor ping tekshiruvi

## Topshiriq sharti:
Bir nechta IP yoki serverlarning holatini parallel tekshiruvchi oqimli dastur.

## Yechim (Python kodi):
```python
from concurrent.futures import ThreadPoolExecutor

serverlar = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4"]

def tekshir(ip):
    # Simulyatsiya
    return ip, "FAOL [200 OK]"

with ThreadPoolExecutor(max_workers=4) as ex:
    natijalar = dict(ex.map(tekshir, serverlar))

for ip, holat in natijalar.items():
    print(f"{ip:15s} : {holat}")
```

## Tushuntirish va Mantiq:
1. Parallel oqimlar tarmoq monitoringini bir necha soniyada bajaradi.

## Ishlash natijasi:
```text
Chiqish: Serverlar holati ro'yxati.
```


# 533-Topshiriq: Asinxron Tasklarni bittama-bitta yakunlanishi bo'yicha olish (as_completed)

## Topshiriq sharti:
Qaysi vazifa birinchi bo'lib tayyor bo'lsa darhol uning natijasini qaytaruvchi iterator.

## Yechim (Python kodi):
```python
import asyncio

async def amal(nom, kechikish):
    await asyncio.sleep(kechikish)
    return f"{nom} ({kechikish}s)"

async def main():
    vazifalar = [amal("Sekin", 1.0), amal("Tez", 0.2), amal("O'rtacha", 0.5)]
    for f in asyncio.as_completed(vazifalar):
        natija = await f
        print(f"Tayyor bo'ldi: {natija}")

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `as_completed()` eng tez tugagan natijani birinchi taqdim etadi (Real-time natija).

## Ishlash natijasi:
```text
Chiqish: Tayyor bo'ldi: Tez -> O'rtacha -> Sekin
```


# 534-Topshiriq: ThreadPool bilan CPU-intensive vazifaning bloklanishini ko'rsatish

## Topshiriq sharti:
Nima uchun CPU amallarini ThreadPool ga berish Python GIL tufayli sekinlashishini tushuntiring.

## Yechim (Python kodi):
```python
import time
import threading

def sanoq(n):
    while n > 0: n -= 1

# Ketma-ket
b1 = time.perf_counter()
sanoq(10_000_000)
sanoq(10_000_000)
t_ketma = time.perf_counter() - b1

# 2 ta oqimda
b2 = time.perf_counter()
t1 = threading.Thread(target=sanoq, args=(10_000_000,))
t2 = threading.Thread(target=sanoq, args=(10_000_000,))
t1.start(); t2.start()
t1.join(); t2.join()
t_oqim = time.perf_counter() - b2

print(f"Ketma-ket vaqt: {t_ketma:.3f}s")
print(f"Oqimlarda vaqt: {t_oqim:.3f}s (GIL tufayli deyarli bir xil)")
```

## Tushuntirish va Mantiq:
1. Python GIL bitta jarayonda bir vaqtda faqat bitta oqimga Python baytkodini bajarishga ruxsat beradi.

## Ishlash natijasi:
```text
Chiqish: Ketma-ket va Oqimlar vaqtlari deyarli bir xil bo'ladi.
```


# 535-Topshiriq: Asinxron cheksiz yuklanish indikatori (Async Spinner)

## Topshiriq sharti:
Og'ir amal bajarilayotganda terminalda aylanuvchi chiroyli asinxron spinner ko'rsating.

## Yechim (Python kodi):
```python
import asyncio
import sys

async def spinner():
    belgilar = "|/-\"
    i = 0
    while True:
        sys.stdout.write(f"\rYuklanmoqda {belgilar[i % 4]} ")
        sys.stdout.flush()
        i += 1
        await asyncio.sleep(0.1)

async def uzoq_ish():
    await asyncio.sleep(1.2)
    return "Muvaffaqiyatli yakunlandi!"

async def main():
    spin_task = asyncio.create_task(spinner())
    natija = await uzoq_ish()
    spin_task.cancel()
    sys.stdout.write("\rTayyor!                     \n")
    print(natija)

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. Asinxron fonda aylanuvchi indikator asosiy ish bitguncha terminalni jonli ushlab turadi.

## Ishlash natijasi:
```text
Chiqish: Tayyor! Muvaffaqiyatli yakunlandi!
```


# 536-Topshiriq: Oqimlararo Deadlock (Boshi berk ko'cha) xavfi va oldini olish

## Topshiriq sharti:
Ikki oqim ikkita qulfni turli tartibda egallashi natijasida kelib chiqadigan Deadlock xatosini ko'rsating.

## Yechim (Python kodi):
```python
import threading

# Deadlockdan qochish qoidasi:
# Barcha oqimlar har doim qulflarni AYNAN BIR XIL TARTIBDA egallashi shart!
qulf1 = threading.Lock()
qulf2 = threading.Lock()

def xavfsiz_oqim(nom):
    with qulf1:
        with qulf2:
            print(f"[{nom}] Ikkala qulfni ham to'g'ri tartibda egalladi.")

t1 = threading.Thread(target=xavfsiz_oqim, args=("Oqim-1",))
t2 = threading.Thread(target=xavfsiz_oqim, args=("Oqim-2",))
t1.start(); t2.start()
t1.join(); t2.join()
```

## Tushuntirish va Mantiq:
1. Qulflar ketma-ketligini bir xil qilish (Lock Ordering) deadlock xatolarini butunlay yo'qotadi.

## Ishlash natijasi:
```text
Chiqish: Ikkala qulfni ham to'g'ri tartibda egalladi.
```


# 537-Topshiriq: Asinxron Kesh: TTL (Time-To-Live) bilan

## Topshiriq sharti:
Belgilangan soniyadan keyin eski ma'lumotni avtomatik yangilovchi asinxron kesh sinfi.

## Yechim (Python kodi):
```python
import asyncio
import time

class AsyncTTLCache:
    def __init__(self, ttl_seconds=1.0):
        self.ttl = ttl_seconds
        self.cache = {}

    async def get_or_set(self, key, async_func):
        now = time.time()
        if key in self.cache:
            val, exp = self.cache[key]
            if now < exp:
                return val, "KESHDAN"
        val = await async_func()
        self.cache[key] = (val, now + self.ttl)
        return val, "YANGI"

cache = AsyncTTLCache(ttl_seconds=0.5)

async def main():
    async def fetch(): return 42
    print(await cache.get_or_set("k1", fetch))
    print(await cache.get_or_set("k1", fetch))
    await asyncio.sleep(0.6)
    print(await cache.get_or_set("k1", fetch))

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. TTL kesh ortiqcha yuklamalarni kamaytiradi va eskirgan ma'lumotlarni o'z vaqtida yangilaydi.

## Ishlash natijasi:
```text
Chiqish: (42, 'YANGI'), (42, 'KESHDAN'), (42, 'YANGI')
```


# 538-Topshiriq: Oqimlar orqali katta faylni parallel bloklarga bo'lib o'qish

## Topshiriq sharti:
Katta faylni bir nechta oqimda turli bayt ofsetlaridan ochib o'qish.

## Yechim (Python kodi):
```python
import os
import threading

def segment_oqish(fayl, boshlangich, uzunlik):
    with open(fayl, "rb") as f:
        f.seek(boshlangich)
        return f.read(uzunlik)

print("Parallel fayl o'qish simulyatsiyasi tayyor.")
```

## Tushuntirish va Mantiq:
1. Download managerlar (IDM kabi) katta fayllarni aynan shu ko'p oqimli segmentatsiya bilan yuklaydi.

## Ishlash natijasi:
```text
Chiqish: Parallel fayl o'qish simulyatsiyasi tayyor.
```


# 539-Topshiriq: Asinxron Pipeline: Bosqichma-bosqich qayta ishlash

## Topshiriq sharti:
Ma'lumotlarni navbat orqali Yuklash -> Tozalash -> Saqlash zanjirida asinxron uzatish.

## Yechim (Python kodi):
```python
import asyncio

async def pipeline():
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()

    async def stage1():
        for i in range(1, 4):
            await q1.put(f"Xom-{i}")
        await q1.put(None)

    async def stage2():
        while True:
            item = await q1.get()
            if item is None:
                await q2.put(None)
                break
            await q2.put(f"Tozalangan-{item}")

    async def stage3():
        while True:
            item = await q2.get()
            if item is None: break
            print(f"[SAQLANDI] {item}")

    await asyncio.gather(stage1(), stage2(), stage3())

asyncio.run(pipeline())
```

## Tushuntirish va Mantiq:
1. Asinxron konveyer (Pipeline) ma'lumotlar oqimini bir necha bosqichda parallel ishlatadi.

## Ishlash natijasi:
```text
Chiqish: [SAQLANDI] Tozalangan-Xom-1, 2, 3
```


# 540-Topshiriq: Oqimlar yordamida dinamik progress monitoring

## Topshiriq sharti:
Alohida oqimda har 0.2 soniyada joriy hisoblagichni ko'rsatib turuvchi monitor.

## Yechim (Python kodi):
```python
import threading
import time

hisob = 0
bajarilmoqdami = True

def monitor():
    while bajarilmoqdami:
        print(f"Joriy taraqqiyot: {hisob} ta bajarildi...")
        time.sleep(0.2)

t = threading.Thread(target=monitor)
t.start()

for _ in range(10):
    hisob += 10
    time.sleep(0.05)

bajarilmoqdami = False
t.join()
print(f"Yakunlandi: {hisob}")
```

## Tushuntirish va Mantiq:
1. Monitoring oqimi asosiy dastur jarayoniga to'sqinlik qilmasdan holatni ko'rsatib boradi.

## Ishlash natijasi:
```text
Chiqish: Taraqqiyot hisoboti va Yakunlandi: 100
```


# 541-Topshiriq: Asinxron sleep bilan animatsiyali yuklanish chizig'i

## Topshiriq sharti:
Terminalda 0 dan 100 foizgacha asinxron ravishda to'lib boruvchi progress bar.

## Yechim (Python kodi):
```python
import asyncio
import sys

async def progress_bar(jami=20):
    for i in range(jami + 1):
        foiz = int((i / jami) * 100)
        chiziq = "#" * i + "-" * (jami - i)
        sys.stdout.write(f"\rYuklanmoqda: [{chiziq}] {foiz}%")
        sys.stdout.flush()
        await asyncio.sleep(0.03)
    sys.stdout.write("\n")

asyncio.run(progress_bar())
```

## Tushuntirish va Mantiq:
1. Asinxron konsol animatsiyasi resurs sarflamasdan silliq yangilanadi.

## Ishlash natijasi:
```text
Chiqish: Yuklanmoqda: [####################] 100%
```


# 542-Topshiriq: ProcessPoolExecutor bilan katta matnlar tahlili

## Topshiriq sharti:
Ko'p yadrolarda bir vaqtda matnlar ichidagi harflarni sanash.

## Yechim (Python kodi):
```python
from concurrent.futures import ProcessPoolExecutor

def harf_sanash(matn):
    return len(matn.split())

if __name__ == '__main__':
    matnlar = ["Python juda qulay til", "Sun'iy intellekt kelajak kasbi", "Dataset toza bo'lishi kerak"]
    with ProcessPoolExecutor(max_workers=2) as ex:
        natijalar = list(ex.map(harf_sanash, matnlar))
    print("So'zlar soni:", natijalar)
```

## Tushuntirish va Mantiq:
1. Matnlarni parallel qayta ishlash orqali NLP tezligi bir necha barobar oshadi.

## Ishlash natijasi:
```text
Chiqish: So'zlar soni: [4, 4, 4]
```


# 543-Topshiriq: Asinxron Tasklarni kutish: asyncio.wait va FIRST_COMPLETED

## Topshiriq sharti:
Birinchi tayyor bo'lgan so'rov natijasini olib, qolganlarini bekor qilish (Hedging requests).

## Yechim (Python kodi):
```python
import asyncio

async def server_sorovi(nom, vaqt):
    await asyncio.sleep(vaqt)
    return f"{nom} birinchi javob berdi!"

async def main():
    v1 = asyncio.create_task(server_sorovi("Server-Sekin", 1.0))
    v2 = asyncio.create_task(server_sorovi("Server-Tezkor", 0.2))

    tayyorlar, qolganlar = await asyncio.wait(
        [v1, v2], return_when=asyncio.FIRST_COMPLETED
    )
    for t in tayyorlar:
        print("G'olib:", t.result())
    for t in qolganlar:
        t.cancel()

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. Eng tez javob bergan server natijasini olib, sekinlarini to'xtatish tarmoq kechikishini keskin kamaytiradi.

## Ishlash natijasi:
```text
Chiqish: G'olib: Server-Tezkor birinchi javob berdi!
```


# 544-Topshiriq: Oqimlararo ma'lumot uzatuvchi Pipe (multiprocessing.Pipe)

## Topshiriq sharti:
Ikki protsess o'rtasida dupleks (ikki tomonlama) truba orqali xabar almashinuvi.

## Yechim (Python kodi):
```python
import multiprocessing

def ulovchi(quvur):
    quvur.send("Qabul qilindi!")
    quvur.close()

if __name__ == '__main__':
    ota_quvur, bola_quvur = multiprocessing.Pipe()
    p = multiprocessing.Process(target=ulovchi, args=(bola_quvur,))
    p.start()
    print("Ota jarayon xabar oldi:", ota_quvur.recv())
    p.join()
```

## Tushuntirish va Mantiq:
1. `Pipe()` eng tezkor ikki tomonlama jarayonlararo kanal hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: Ota jarayon xabar oldi: Qabul qilindi!
```


# 545-Topshiriq: Asinxron generatorni yopish (aclose)

## Topshiriq sharti:
Resurslarni tozalash uchun asinxron generatorni majburiy to'xtatish va tozalash.

## Yechim (Python kodi):
```python
import asyncio

async def asinxron_oqim():
    try:
        while True:
            yield "Yangi ma'lumot"
            await asyncio.sleep(0.1)
    finally:
        print("[TOZALASH] Asinxron oqim muvaffaqiyatli yopildi.")

async def main():
    gen = asinxron_oqim()
    print(await anext(gen))
    await gen.aclose()  # To'xtatamiz

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. `aclose()` generatorning `finally` blokini ishga tushirib ochiq soketlarni yopadi.

## Ishlash natijasi:
```text
Chiqish: Yangi ma'lumot -> [TOZALASH] Asinxron oqim muvaffaqiyatli yopildi.
```


# 546-Topshiriq: ThreadPool bilan parallel rasmlarni o'lchamini o'zgartirish simulyatsiyasi

## Topshiriq sharti:
Bir nechta tasvir fayllarini diskdan ochib parallel qayta ishlash arxitekturasi.

## Yechim (Python kodi):
```python
from concurrent.futures import ThreadPoolExecutor

rasmlar = ["rasm1.jpg", "rasm2.jpg", "rasm3.jpg"]

def olchamni_ozgartir(nom):
    return f"{nom} -> 512x512 ga siqildi"

with ThreadPoolExecutor(max_workers=3) as ex:
    natijalar = list(ex.map(olchamni_ozgartir, rasmlar))

for n in natijalar:
    print(n)
```

## Tushuntirish va Mantiq:
1. Rasmlar va multimedia fayllarini konvertatsiya qilishda oqimlar havzasi keng qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: rasm1, 2, 3 -> 512x512 ga siqildi.
```


# 547-Topshiriq: Asinxron Timeout bilan urinishlar zanjiri

## Topshiriq sharti:
Agar 0.2 soniyada javob kelmasa, zaxira asinxron xizmatga murojaat qilish.

## Yechim (Python kodi):
```python
import asyncio

async def birinchi_xizmat():
    await asyncio.sleep(0.5)
    return "1-xizmat natijasi"

async def zaxira_xizmat():
    await asyncio.sleep(0.05)
    return "Zaxira xizmati natijasi"

async def main():
    try:
        javob = await asyncio.wait_for(birinchi_xizmat(), timeout=0.1)
    except asyncio.TimeoutError:
        print("[TIMEOUT] 1-xizmat kechikdi. Zaxiradan olinmoqda...")
        javob = await zaxira_xizmat()
    print("Natija:", javob)

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. Foydalanuvchini kuttirmasdan zaxira kanallariga o'tuvchi yuqori sifatli asinxron arxitektura.

## Ishlash natijasi:
```text
Chiqish: [TIMEOUT]... Zaxiradan olinmoqda... Natija: Zaxira xizmati natijasi
```


# 548-Topshiriq: Oqimlararo xavfsiz hisoblagich klassi (Atomic Counter)

## Topshiriq sharti:
Ichki Lock bilan himoyalangan, har qanday oqimda to'g'ri ishlovchi atomik hisoblagich.

## Yechim (Python kodi):
```python
import threading

class AtomikHisoblagich:
    def __init__(self):
        self._qiymat = 0
        self._lock = threading.Lock()

    def oshir(self, qadam=1):
        with self._lock:
            self._qiymat += qadam
            return self._qiymat

    @property
    def qiymat(self):
        with self._lock:
            return self._qiymat

h = AtomikHisoblagich()
h.oshir(5)
h.oshir(10)
print("Atomik qiymat:", h.qiymat)
```

## Tushuntirish va Mantiq:
1. Atomik hisoblagichlar veb-serverlarda tashriflar sonini aniq yuritish uchun ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Atomik qiymat: 15
```


# 549-Topshiriq: Asinxron qidiruv tizimi (Web Crawler asoslari)

## Topshiriq sharti:
Bir nechta sahifalarni asinxron kezib, kerakli ma'lumotlarni yig'uvchi krouler yadrosi.

## Yechim (Python kodi):
```python
import asyncio

sahifalar = ["/bosh_sahifa", "/kitoblar", "/yangiliklar", "/aloqa"]

async def sahifani_tekshir(url):
    await asyncio.sleep(0.1)
    return f"Sahifa: {url} (200 OK)"

async def main():
    topilganlar = await asyncio.gather(*(sahifani_tekshir(u) for u in sahifalar))
    for t in topilganlar:
        print(" *", t)

asyncio.run(main())
```

## Tushuntirish va Mantiq:
1. Google, Yandex va AI qidiruv robotlari aynan shu asinxron me'morchilikda sahifalarni indekslaydi.

## Ishlash natijasi:
```text
Chiqish: Barcha sahifalar bir zumda tekshiriladi.
```


# 550-Topshiriq: To'liq Asinxron Ishlar Menejeri (Async Worker Engine)

## Topshiriq sharti:
Vazifalarni parallel qabul qiluvchi, semafor bilan nazorat qiluvchi va natijalarni hisoblovchi to'liq asinxron dvigatel.

## Yechim (Python kodi):
```python
import asyncio

class AsyncWorkerEngine:
    def __init__(self, concurrency=3):
        self.semaphore = asyncio.Semaphore(concurrency)
        self.completed = 0

    async def _execute_task(self, task_id):
        async with self.semaphore:
            await asyncio.sleep(0.2)
            self.completed += 1
            print(f"[BAJARILDI] Topshiriq #{task_id} (Jami bitgan: {self.completed})")

    async def run(self, total_tasks=6):
        print(f"Dvigatel ishga tushdi: {total_tasks} ta topshiriq parallel bajarilmoqda...")
        await asyncio.gather(*(self._execute_task(i) for i in range(1, total_tasks + 1)))
        print("Barcha topshiriqlar 100% bajarildi!")

engine = AsyncWorkerEngine(concurrency=3)
asyncio.run(engine.run(6))
```

## Tushuntirish va Mantiq:
1. Antigravity kabi avtonom subagentlar va AI yuklash tizimlarining markaziy dvigateli.

## Ishlash natijasi:
```text
Chiqish: [BAJARILDI] Topshiriq #1..#6 -> Barcha topshiriqlar 100% bajarildi!
```

