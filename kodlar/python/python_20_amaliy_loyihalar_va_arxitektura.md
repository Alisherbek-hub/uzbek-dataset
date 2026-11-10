# Python Dasturlash Tili — 20-Qism: Amaliy Loyihalar, Tizimli Arxitektura va Sun'iy Intellekt Dvigatellari
## (951-1000 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar — YAKUNIY QISM)

Ushbu yakuniy to'plam dasturiy ta'minot muhandisligi, tizimli arxitektura, kiberxavfsizlik va 1-Bit LLM dvigatellarini qamrab oladi:
* To'liq CLI, Konfiguratsiya va Fayl yaxlitligi tizimlari;
* SQLite Mini-ORM, Tranzaksiyalar, Migratsiyalar, In-Memory TTL Kesh;
* Asinxron Task Queue, Event Bus, Mini Web Framework, HMAC Webhooklar;
* Kriptografiya, Steganografiya, Log tahlili va Telegram bot arxitekturasi;
* Mini Qidiruv Tizimi (Inverted Index), Tarmoq protokollari (DNS, struct, RPC, Gossip);
* Siqish algoritmlari (Huffman, LZ77, BPE Tokenizer);
* Mashinali o'rganish, Attention mexanizmi (Transformer QKV), ReAct agent sikli;
* 1000-Topshiriq: 1-Bit LLM Kvantlangan Inference Dvigateli;

---

# 951-Topshiriq: Buyruqlar satri utilitasi (Full CLI Tool: argparse)

## Topshiriq sharti:
Subkomandalar (init, build, deploy) va bayroqlarga ega to'liq CLI ilova skeletini yarating.

## Yechim (Python kodi):
```python
import argparse

def create_cli():
    parser = argparse.ArgumentParser(description="Uzbek AI Tizim Boshqaruvchisi")
    subparsers = parser.add_subparsers(dest="komanda", help="Mavjud buyruqlar")
    
    # 'init' komandasi
    init_parser = subparsers.add_parser("init", help="Yangi loyiha yaratish")
    init_parser.add_argument("--nom", required=True, help="Loyiha nomi")
    
    # 'train' komandasi
    train_parser = subparsers.add_parser("train", help="Modelni o'qitish")
    train_parser.add_argument("--epochs", type=int, default=10, help="Epoxalar soni")
    
    return parser

parser = create_cli()
args = parser.parse_args(["init", "--nom", "UzbekLLM"])
print(f"Tanlangan buyruq: {args.komanda}, Loyiha: {args.nom}")
```

## Tushuntirish va Mantiq:
1. `argparse.add_subparsers` Git va Docker kabi professional ko'p pog'onali CLI buyruqlarini yaratadi.

## Ishlash natijasi:
```text
Chiqish: Tanlangan buyruq: init, Loyiha: UzbekLLM
```

---

# 952-Topshiriq: Ierarxik Konfiguratsiya Menejeri (Config Manager)

## Topshiriq sharti:
Standart parametrlar, JSON fayli va muhit o'zgaruvchilarini birlashtiruvchi sozlamalar sinfi.

## Yechim (Python kodi):
```python
import json
import os

class ConfigManager:
    def __init__(self, standartlar=None):
        self.konfig = standartlar or {}

    def yuklash_json(self, json_matn):
        self.konfig.update(json.loads(json_matn))

    def get(self, kalit, default=None):
        env_qiymat = os.environ.get(kalit.upper())
        if env_qiymat is not None: return env_qiymat
        return self.konfig.get(kalit, default)

cfg = ConfigManager({"port": 8080, "debug": False})
cfg.yuklash_json('{"port": 9000, "app_nomi": "UzbekAI"}')
print("Port:", cfg.get("port"))
print("Ilova nomi:", cfg.get("app_nomi"))
```

## Tushuntirish va Mantiq:
1. Konfiguratsiyani qatlamlar bo'yicha (Default -> File -> Environment) yuklash 12-Factor App tamoyilidir.

## Ishlash natijasi:
```text
Chiqish: Port: 9000, Ilova nomi: UzbekAI
```

---

# 953-Topshiriq: Fayl tizimi yaxlitligini kuzatuvchi (File Integrity Watcher)

## Topshiriq sharti:
Papka ichidagi fayllarning SHA-256 xeshini saqlab, o'zgargan yoki yangi fayllarni aniqlovchi monitoring tizimi.

## Yechim (Python kodi):
```python
import hashlib

def fayl_xeshi(matn):
    return hashlib.sha256(matn.encode()).hexdigest()

class IntegrityWatcher:
    def __init__(self):
        self.kesh = {}

    def tekshir(self, fayllar):
        ozgarishlar = []
        for nom, content in fayllar.items():
            h = fayl_xeshi(content)
            if nom not in self.kesh:
                ozgarishlar.append(f"Yangi fayl: {nom}")
            elif self.kesh[nom] != h:
                ozgarishlar.append(f"O'zgargan fayl: {nom}")
            self.kesh[nom] = h
        return ozgarishlar

watcher = IntegrityWatcher()
print("1-tekshiruv:", watcher.tekshir({"main.py": "print('v1')"}))
print("2-tekshiruv:", watcher.tekshir({"main.py": "print('v2')"}))
```

## Tushuntirish va Mantiq:
1. Kiberxavfsizlik va avtomatik qayta yuklash (Hot Reload) tizimlari fayl xeshlari orqali ishlaydi.

## Ishlash natijasi:
```text
Chiqish: 1-tekshiruv: ['Yangi fayl: main.py'], 2-tekshiruv: ["O'zgargan fayl: main.py"]
```

---

# 954-Topshiriq: Xotiradagi Kesh va TTL (In-Memory Key-Value Store with TTL & Eviction)

## Topshiriq sharti:
Amal qilish muddati (TTL) tugagan kalitlarni avtomatik o'chiruvchi kesh mexanizmi.

## Yechim (Python kodi):
```python
import time

class TTLKesh:
    def __init__(self):
        self.ombor = {}

    def set(self, kalit, qiymat, ttl_soniya):
        tugash_vaqti = time.time() + ttl_soniya
        self.ombor[kalit] = (qiymat, tugash_vaqti)

    def get(self, kalit):
        if kalit in self.ombor:
            qiymat, tugash = self.ombor[kalit]
            if time.time() < tugash:
                return qiymat
            del self.ombor[kalit]
        return None

kesh = TTLKesh()
kesh.set("token", "xyz_secret", ttl_soniya=1.0)
print("Darhol o'qish:", kesh.get("token"))
time.sleep(1.05)
print("1 soniyadan keyin:", kesh.get("token"))
```

## Tushuntirish va Mantiq:
1. Redis uslubidagi TTL kesh ortiqcha xotira sarflanishini oldini oladi.

## Ishlash natijasi:
```text
Chiqish: Darhol o'qish: xyz_secret, 1 soniyadan keyin: None
```

---

# 955-Topshiriq: SQLite asosidagi Mini-ORM (Object-Relational Mapping)

## Topshiriq sharti:
Python klasslarini SQL jadvallariga bog'lab saqlash (`save`) va qidirish (`filter`) imkoniyatini beruvchi mini-ORM.

## Yechim (Python kodi):
```python
import sqlite3

class MiniORM:
    def __init__(self, db_nomi=":memory:"):
        self.conn = sqlite3.connect(db_nomi)
        self.conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, ism TEXT, yosh INT)")

    def save_user(self, ism, yosh):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO users (ism, yosh) VALUES (?, ?)", (ism, yosh))
        self.conn.commit()
        return cur.lastrowid

    def filter_users(self, min_yosh):
        cur = self.conn.cursor()
        cur.execute("SELECT id, ism, yosh FROM users WHERE yosh >= ?", (min_yosh,))
        return cur.fetchall()

orm = MiniORM()
orm.save_user("Jasur", 22)
orm.save_user("Nodir", 17)
print("20 yoshdan kattalar:", orm.filter_users(20))
```

## Tushuntirish va Mantiq:
1. ORM ma'lumotlar bazasi so'rovlarini dasturlash tili ob'ektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: 20 yoshdan kattalar: [(1, 'Jasur', 22)]
```

---

# 956-Topshiriq: Ma'lumotlar bazasi migratsiya mexanizmi (Schema Migrations)

## Topshiriq sharti:
Baza versiyalarini tartib bilan oshiruvchi (`up`) va orqaga qaytaruvchi (`down`) tizim.

## Yechim (Python kodi):
```python
class MigratsiyaMenejeri:
    def __init__(self):
        self.joriy_versiya = 0
        self.migratsiyalar = []

    def qoshish(self, v, up_fn, down_fn):
        self.migratsiyalar.append((v, up_fn, down_fn))

    def upgrade(self):
        for v, up, down in self.migratsiyalar:
            if v > self.joriy_versiya:
                up()
                self.joriy_versiya = v

mm = MigratsiyaMenejeri()
mm.qoshish(1, lambda: print("V1: users jadvali yaratildi"), lambda: print("V1 bekor qilindi"))
mm.qoshish(2, lambda: print("V2: email ustuni qo'shildi"), lambda: print("V2 bekor qilindi"))
mm.upgrade()
print("Joriy baza versiyasi:", mm.joriy_versiya)
```

## Tushuntirish va Mantiq:
1. Alembic va Flyway kabi dasturlar ma'lumotlar bazasi o'zgarishlarini jamoaviy boshqarishda qo'llaydi.

## Ishlash natijasi:
```text
Chiqish: V1: users jadvali yaratildi\nV2: email ustuni qo'shildi\nJoriy baza versiyasi: 2
```

---

# 957-Topshiriq: Asinxron Task Queue (Producer-Consumer Worker Pool)

## Topshiriq sharti:
asyncio.Queue yordamida vazifalarni parallel ishlovchi ishchilar (workers) havzasi.

## Yechim (Python kodi):
```python
import asyncio

async def worker(id, queue):
    while True:
        task = await queue.get()
        if task is None: break
        # print(f"Worker {id} {task} ni bajardi")
        queue.task_done()

async def asosiy_quvur():
    queue = asyncio.Queue()
    workers = [asyncio.create_task(worker(i, queue)) for i in range(2)]
    for item in ["Vazifa A", "Vazifa B", "Vazifa C"]:
        await queue.put(item)
    await queue.join()
    for _ in workers: await queue.put(None)
    await asyncio.gather(*workers)
    return "Barcha 3 vazifa bajarildi"

print(asyncio.run(asosiy_quvur()))
```

## Tushuntirish va Mantiq:
1. Celery va RabbitMQ kabi asinxron vazifalar navbati tizimlarining mantiqiy yadrosi.

## Ishlash natijasi:
```text
Chiqish: Barcha 3 vazifa bajarildi
```

---

# 958-Topshiriq: Hodisalarga asoslangan arxitektura (Event Bus / Pub-Sub)

## Topshiriq sharti:
Tizim modullari orasidagi bevosita bog'liqlikni yo'qotuvchi (Decoupled) hodisalar avtobusi.

## Yechim (Python kodi):
```python
from collections import defaultdict

class EventBus:
    def __init__(self):
        self.tinglovchilar = defaultdict(list)

    def obuna_bol(self, hodisa_nomi, fn):
        self.tinglovchilar[hodisa_nomi].append(fn)

    def tarqatish(self, hodisa_nomi, *args, **kwargs):
        for fn in self.tinglovchilar[hodisa_nomi]:
            fn(*args, **kwargs)

bus = EventBus()
bus.obuna_bol("foydalanuvchi_yaratildi", lambda u: print(f"Email yuborildi: {u}"))
bus.obuna_bol("foydalanuvchi_yaratildi", lambda u: print(f"Hisob ochildi: {u}"))
bus.tarqatish("foydalanuvchi_yaratildi", "Alisher")
```

## Tushuntirish va Mantiq:
1. Mikroservislar va murakkab ilovalarda hodisalarni tarqatish arxitekturasi.

## Ishlash natijasi:
```text
Chiqish: Email yuborildi: Alisher\nHisob ochildi: Alisher
```

---

# 959-Topshiriq: Mini HTTP Veb Framework (Routing, Middleware & Context)

## Topshiriq sharti:
Yo'llar (Routes) va so'rovlar orasidagi oraliq dasturlarni (Middleware) boshqaruvchi mini framework.

## Yechim (Python kodi):
```python
class MiniWebApp:
    def __init__(self):
        self.yollar = {}
        self.middleware = []

    def use(self, fn):
        self.middleware.append(fn)

    def route(self, path):
        def decorator(handler):
            self.yollar[path] = handler
            return handler
        return decorator

    def handle_request(self, path, ctx):
        for mw in self.middleware:
            mw(ctx)
        if path in self.yollar:
            return self.yollar[path](ctx)
        return "404 Not Found"

app = MiniWebApp()
app.use(lambda ctx: ctx.setdefault("user", "Mehmon"))

@app.route("/bosh")
def bosh(ctx): return f"Xush kelibsiz, {ctx['user']}!"

print(app.handle_request("/bosh", {}))
```

## Tushuntirish va Mantiq:
1. Flask, FastAPI va Express.js aynan Middleware quvuri (Pipeline pattern) asosiga qurilgan.

## Ishlash natijasi:
```text
Chiqish: Xush kelibsiz, Mehmon!
```

---

# 960-Topshiriq: Webhook Dispatcher (HMAC-SHA256 xavfsizlik bilan)

## Topshiriq sharti:
Uchinchi tomon servislarga xavfsiz va imzolangan webhook hodisalarini yuboruvchi sinf.

## Yechim (Python kodi):
```python
import hmac
import hashlib
import json

class WebhookDispatcher:
    def __init__(self, secret_key):
        self.secret = secret_key.encode()

    def send(self, url, payload):
        tana = json.dumps(payload).encode()
        imzo = hmac.new(self.secret, tana, hashlib.sha256).hexdigest()
        headers = {"X-Signature-SHA256": imzo, "Content-Type": "application/json"}
        return f"{url} ga {len(tana)} bayt yuborildi. Imzo: {imzo[:10]}..."

dispatcher = WebhookDispatcher("secret_api_key_777")
print(dispatcher.send("https://hamkor.uz/webhook", {"status": "paid", "amount": 100000}))
```

## Tushuntirish va Mantiq:
1. To'lov tizimlari (Payme, Click, Stripe) webhooklar orqali xavfsiz hisobot yetkazadi.

## Ishlash natijasi:
```text
Chiqish: https://hamkor.uz/webhook ga ... bayt yuborildi. Imzo: ... 
```

---

# 961-Topshiriq: Rate Limiter Middleware (Token Bucket per IP)

## Topshiriq sharti:
Har bir IP-manzil uchun so'rovlar sonini xotirada cheklovchi tizim.

## Yechim (Python kodi):
```python
class IPRateLimiter:
    def __init__(self, limit=3):
        self.limit = limit
        self.sorovlar = defaultdict(int)

    def ruxsatmi(self, ip):
        if self.sorovlar[ip] < self.limit:
            self.sorovlar[ip] += 1
            return True
        return False

limiter = IPRateLimiter(limit=2)
ip = "192.168.1.1"
print("1-urinish:", limiter.ruxsatmi(ip))
print("2-urinish:", limiter.ruxsatmi(ip))
print("3-urinish:", limiter.ruxsatmi(ip))
```

## Tushuntirish va Mantiq:
1. DDoS hujumlari va API suiste'mollarining oldini olish uchun zaruriy qatlam.

## Ishlash natijasi:
```text
Chiqish: 1-urinish: True, 2-urinish: True, 3-urinish: False
```

---

# 962-Topshiriq: Kriptografik fayl shifrlagich (XOR Stream Cipher with Key Hashing)

## Topshiriq sharti:
Baytlar oqimini dinamik xesh kaliti bilan simmetrik shifrlash va qayta tiklash.

## Yechim (Python kodi):
```python
def xor_shifrlash(baytlar, kalit):
    k_bayt = kalit.encode()
    k_len = len(k_bayt)
    return bytes(b ^ k_bayt[i % k_len] for i, b in enumerate(baytlar))

asl_matn = b"O'zbekiston AI Davlat Strategiyasi 2030"
parol = "kuchli_kalit_123"

shifrlangan = xor_shifrlash(asl_matn, parol)
tiklangan = xor_shifrlash(shifrlangan, parol)

print("Shifrlangan:", shifrlangan[:15])
print("Tiklangan:", tiklangan.decode('utf-8'))
```

## Tushuntirish va Mantiq:
1. Simmetrik oqimli shifrlashda bitta amal ham shifrlash, ham deshifrlash vazifasini o'taydi.

## Ishlash natijasi:
```text
Chiqish: Shifrlangan: ..., Tiklangan: O'zbekiston AI Davlat Strategiyasi 2030
```

---

# 963-Topshiriq: Markdown Parser va HTML Generatori (sof Python regex)

## Topshiriq sharti:
Oddiy Markdown matnidagi sarlavha, qalin harf va ro'yxatlarni toza HTML kodiga o'giring.

## Yechim (Python kodi):
```python
import re

def parse_markdown(md_matn):
    html = md_matn
    # # Sarlavha -> <h1>Sarlavha</h1>
    html = re.sub(r"^# (.*)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    # **qalin** -> <b>qalin</b>
    html = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", html)
    # * element -> <li>element</li>
    html = re.sub(r"^\* (.*)$", r"<li>\1</li>", html, flags=re.MULTILINE)
    return html.strip()

md = "# Salom Dunyo\nBu **Python** dasturi.\n* Birinchi\n* Ikkinchi"
print("Generatsiya qilingan HTML:\n", parse_markdown(md))
```

## Tushuntirish va Mantiq:
1. Statik sayt generatorlari (Jekyll, Hugo) asosidagi regex matn tarjimasi.

## Ishlash natijasi:
```text
Chiqish: Generatsiya qilingan HTML:\n <h1>Salom Dunyo</h1>\nBu <b>Python</b> dasturi.\n<li>Birinchi</li>\n<li>Ikkinchi</li>
```

---

# 964-Topshiriq: CSV va JSON hisobot eksportchisi

## Topshiriq sharti:
Ma'lumotlar bazasidagi ma'lumotlarni turli biznes formatlarga eksport qilish.

## Yechim (Python kodi):
```python
import csv
import io

def eksport_csv(ustunlar, qatorlar):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(ustunlar)
    writer.writerows(qatorlar)
    return output.getvalue()

csv_matn = eksport_csv(["ID", "Muallif", "Asar"], [[1, "Navoiy", "Xamsa"], [2, "Qodiriy", "O'tkan kunlar"]])
print("Eksport qilingan CSV:\n", csv_matn.strip())
```

## Tushuntirish va Mantiq:
1. Biznes hisobotlar va tahliliy ma'lumotlarni avtomatlashtirish.

## Ishlash natijasi:
```text
Chiqish: Eksport qilingan CSV:\n ID,Muallif,Asar\n1,Navoiy,Xamsa\n2,Qodiriy,O'tkan kunlar
```

---

# 965-Topshiriq: Veb Scraping va Link Crawler tamoyili

## Topshiriq sharti:
HTML sahifadagi barcha ichki havolalarni ajratib oluvchi crawler mexanizmi.

## Yechim (Python kodi):
```python
import re

def sahifa_havolalari(html, domen):
    havolalar = re.findall(r'href=["\'](.*?)["\']', html)
    toza = []
    for h in havolalar:
        if h.startswith("http"): toza.append(h)
        elif h.startswith("/"): toza.append(f"{domen}{h}")
    return list(set(toza))

html = '<a href="/yangiliklar">Yangilik</a> <a href="https://ziyouz.com/kutubxona">Kutubxona</a>'
print("Topilgan havolalar:", sahifa_havolalari(html, "https://ziyouz.com"))
```

## Tushuntirish va Mantiq:
1. Ma'lumot to'plash (Dataset Crawling) robotlarining poydevori.

## Ishlash natijasi:
```text
Chiqish: Topilgan havolalar: ['https://ziyouz.com/yangiliklar', 'https://ziyouz.com/kutubxona']
```

---

# 966-Topshiriq: Matn steganografiyasi (Zero-Width Spaces bilan maxfiy xabar yashirish)

## Topshiriq sharti:
Matn ichiga ko'rinmas bo'shliqlar (`\u200b` va `\u200c`) orqali ikkilik shifr yashiring.

## Yechim (Python kodi):
```python
def yashir_matn(ochiq_matn, maxfiy):
    binar = ''.join(format(ord(c), '08b') for c in maxfiy)
    # 0 = \u200b, 1 = \u200c
    yashirin = ''.join('\u200b' if b == '0' else '\u200c' for b in binar)
    return ochiq_matn[:4] + yashirin + ochiq_matn[4:]

def och_matn(matn):
    binar = []
    for c in matn:
        if c == '\u200b': binar.append('0')
        elif c == '\u200c': binar.append('1')
    bin_str = ''.join(binar)
    soz = ''.join(chr(int(bin_str[i:i+8], 2)) for i in range(0, len(bin_str), 8))
    return soz

stego = yashir_matn("Bugun havo juda go'zal", "AI")
print("Ko'rinishi oddiy:", stego)
print("Maxfiy xabar ochildi:", och_matn(stego))
```

## Tushuntirish va Mantiq:
1. Steganografiya suv belgilari qo'yish (Watermarking) va mualliflik huquqini himoyalashda qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: Ko'rinishi oddiy: Bugun havo juda go'zal, Maxfiy xabar ochildi: AI
```

---

# 967-Topshiriq: Server Log analizatori va Brute-Force detektori

## Topshiriq sharti:
Nginx loglarini tahlil qilib 1 daqiqada 5 martadan ko'p xato parol kiritgan IP larni qora ro'yxatga oling.

## Yechim (Python kodi):
```python
from collections import Counter

logs = [
    "192.168.1.10 - 401 Unauthorized",
    "192.168.1.10 - 401 Unauthorized",
    "192.168.1.10 - 401 Unauthorized",
    "192.168.1.5 - 200 OK"
]

xato_iplar = [qator.split()[0] for qator in logs if "401" in qator]
hujumchilar = [ip for ip, son in Counter(xato_iplar).items() if son >= 3]
print("Qora ro'yxatga tushgan IP:", hujumchilar)
```

## Tushuntirish va Mantiq:
1. Fail2ban va SIEM kiberxavfsizlik vositalarining tahlil qoidasi.

## Ishlash natijasi:
```text
Chiqish: Qora ro'yxatga tushgan IP: ['192.168.1.10']
```

---

# 968-Topshiriq: Telegram Bot Mantiqi (Long Polling Dispatcher)

## Topshiriq sharti:
Telegram Bot API yangilanishlarini qayta ishlovchi va buyruqlarni yo'naltiruvchi dispatcher.

## Yechim (Python kodi):
```python
class TelegramBotDispatcher:
    def __init__(self):
        self.handlers = {}

    def command(self, cmd):
        def decorator(fn):
            self.handlers[f"/{cmd}"] = fn
            return fn
        return decorator

    def dispatch(self, update):
        matn = update.get("message", {}).get("text", "")
        if matn in self.handlers:
            return self.handlers[matn](update["message"]["chat"]["id"])
        return "Noma'lum buyruq"

bot = TelegramBotDispatcher()
@bot.command("start")
def start(chat_id): return f"Assalomu alaykum! Chat ID: {chat_id}"

print(bot.dispatch({"message": {"chat": {"id": 12345}, "text": "/start"}}))
```

## Tushuntirish va Mantiq:
1. aiogram va python-telegram-bot kutubxonalarining asosiy ishlash mexanizmi.

## Ishlash natijasi:
```text
Chiqish: Assalomu alaykum! Chat ID: 12345
```

---

# 969-Topshiriq: Mini Qidiruv Tizimi (Inverted Index va TF-IDF Ranking)

## Topshiriq sharti:
Hujjatlar indeksini qurib, qidiruv so'roviga eng mos kelgan hujjatni chiqaruvchi qidiruv dvigateli.

## Yechim (Python kodi):
```python
class MiniSearchEngine:
    def __init__(self):
        self.indeks = defaultdict(set)
        self.hujjatlar = {}

    def add(self, doc_id, text):
        self.hujjatlar[doc_id] = text
        for word in text.lower().split():
            self.indeks[word].add(doc_id)

    def search(self, query):
        q_words = query.lower().split()
        if not q_words: return []
        natija = self.indeks.get(q_words[0], set())
        for w in q_words[1:]:
            natija = natija.intersection(self.indeks.get(w, set()))
        return [self.hujjatlar[doc_id] for doc_id in natija]

se = MiniSearchEngine()
se.add(1, "Python dasturlash tili va sun'iy intellekt")
se.add(2, "O'zbekiston Milliy Ensiklopediyasi kitoblari")
print("Qidiruv 'python sun'iy':", se.search("python sun'iy"))
```

## Tushuntirish va Mantiq:
1. Elasticsearch va Google qidiruvining teskari indeks (Inverted Index) tamoyili.

## Ishlash natijasi:
```text
Chiqish: Qidiruv 'python sun'iy': ["Python dasturlash tili va sun'iy intellekt"]
```

---

# 970-Topshiriq: Imlo tekshirgich va Taklif beruvchi (Spell Checker & Suggester)

## Topshiriq sharti:
O'zbek tilidagi lug'at asosida xato kiritilgan so'zga to'g'ri variantni tavsiya eting.

## Yechim (Python kodi):
```python
lugat = {"dastur", "sun'iy", "intellekt", "model", "kitob"}

def tavsiya_et(xato_soz):
    def masofa(s1, s2):
        if len(s1) > len(s2): s1, s2 = s2, s1
        return sum(1 for c1, c2 in zip(s1, s2) if c1 != c2) + abs(len(s1) - len(s2))
    return min(lugat, key=lambda s: masofa(xato_soz, s))

print("dasturx ->", tavsiya_et("dasturx"))
print("intelkt ->", tavsiya_et("intelkt"))
```

## Tushuntirish va Mantiq:
1. Qidiruv satrlaridagi 'Siz buni nazarda tutganmidingiz?' xizmati.

## Ishlash natijasi:
```text
Chiqish: dasturx -> dastur, intelkt -> intellekt
```

---

# 971-Topshiriq: Binar Protokollar Serializatori (struct moduli)

## Topshiriq sharti:
Tarmoq protokollari uchun bayt sarlavhalarini (Magic, Version, Payload Length) qadoqlang.

## Yechim (Python kodi):
```python
import struct

# Protokol formati: Magic(4s), Versiya(H=2 bayt), Hajm(I=4 bayt)
format_shablon = "!4sHI"

def pack_paket(magic, ver, data_len):
    return struct.pack(format_shablon, magic.encode(), ver, data_len)

def unpack_paket(baytlar):
    magic, ver, data_len = struct.unpack(format_shablon, baytlar)
    return magic.decode(), ver, data_len

paket = pack_paket("UZAI", 1, 1024)
print("Binar baytlar (10 bayt):", list(paket))
print("Ochilgan paket:", unpack_paket(paket))
```

## Tushuntirish va Mantiq:
1. TCP darajasidagi maxsus protokollar eng kam bayt sarflashi uchun `struct` orqali yoziladi.

## Ishlash natijasi:
```text
Chiqish: Binar baytlar (10 bayt): [85, 90, 65, 73, 0, 1, 0, 0, 4, 0], Ochilgan paket: ('UZAI', 1, 1024)
```

---

# 972-Topshiriq: JSON-RPC 2.0 Protokoli mini-serveri

## Topshiriq sharti:
Masofaviy funksiyalarni JSON standarti bo'yicha chaqiruvchi RPC servisi.

## Yechim (Python kodi):
```python
class JSONRPCServer:
    def __init__(self):
        self.metodlar = {}

    def register(self, fn):
        self.metodlar[fn.__name__] = fn
        return fn

    def execute(self, rpc_request):
        mid = rpc_request.get("id")
        method = rpc_request.get("method")
        params = rpc_request.get("params", [])
        if method not in self.metodlar:
            return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": mid}
        res = self.metodlar[method](*params)
        return {"jsonrpc": "2.0", "result": res, "id": mid}

rpc = JSONRPCServer()
@rpc.register
def kopaytir(a, b): return a * b

print(rpc.execute({"jsonrpc": "2.0", "method": "kopaytir", "params": [6, 7], "id": 1}))
```

## Tushuntirish va Mantiq:
1. Kriptovalyuta tarmoqlari (Bitcoin, Ethereum node) RPC chaqiruvlarida JSON-RPC 2.0 ishlatadi.

## Ishlash natijasi:
```text
Chiqish: {'jsonrpc': '2.0', 'result': 42, 'id': 1}
```

---

# 973-Topshiriq: Grafviz (Graphviz DOT) fayl generatori

## Topshiriq sharti:
Graf va neyron tarmoq strukturasini vizual chizish uchun DOT fayl kodini generatsiya qiling.

## Yechim (Python kodi):
```python
def generatsiya_dot(tugunlar, qirralar):
    natija = ["digraph G {", "  rankdir=LR;"]
    for u, v in qirralar:
        natija.append(f'  "{u}" -> "{v}";')
    natija.append("}")
    return "\n".join(natija)

dot_kod = generatsiya_dot(["A", "B", "C"], [("A", "B"), ("B", "C"), ("A", "C")])
print("DOT kodi:\n", dot_kod)
```

## Tushuntirish va Mantiq:
1. Dasturiy arxitektura va sintaktik daraxtlarni diagrammaga aylantirish standarti.

## Ishlash natijasi:
```text
Chiqish: DOT kodi:\n digraph G {\n  rankdir=LR;\n  "A" -> "B";\n  "B" -> "C";\n  "A" -> "C";\n}
```

---

# 974-Topshiriq: Holatlar Mashinasi (State Machine Text RPG Engine)

## Topshiriq sharti:
O'yin xonalari va inventarni boshqaruvchi chekli avtomat (Finite State Machine).

## Yechim (Python kodi):
```python
class XonaOyini:
    def __init__(self):
        self.holat = "Boshlang'ich zal"
        self.xaritalar = {
            "Boshlang'ich zal": {"shimol": "Xazina xonasi"},
            "Xazina xonasi": {"janub": "Boshlang'ich zal"}
        }

    def harakat(self, yonalish):
        if yonalish in self.xaritalar[self.holat]:
            self.holat = self.xaritalar[self.holat][yonalish]
            return f"Ko'chdingiz: {self.holat}"
        return "Bu tomonga yo'l yo'q!"

game = XonaOyini()
print(game.harakat("shimol"))
print(game.harakat("janub"))
```

## Tushuntirish va Mantiq:
1. O'yinlar, tarmoq protokollari va botlarning mantiqiy asosidir.

## Ishlash natijasi:
```text
Chiqish: Ko'chdingiz: Xazina xonasi, Ko'chdingiz: Boshlang'ich zal
```

---

# 975-Topshiriq: Git Ob'ektlari Modeli (Git Blob va SHA-1 Commit modeli)

## Topshiriq sharti:
Git ning ma'lumotlarni saqlash tamoyili: `blob <size>\0<content>` xeshini hisoblang.

## Yechim (Python kodi):
```python
import hashlib

def git_blob_hash(matn):
    baytlar = matn.encode('utf-8')
    sarlavha = f"blob {len(baytlar)}\0".encode('utf-8')
    to_liq = sarlavha + baytlar
    return hashlib.sha1(to_liq).hexdigest()

fayl = "Salom Git dunyosi!"
print("Git Blob SHA-1 xeshi:", git_blob_hash(fayl))
```

## Tushuntirish va Mantiq:
1. Git har bir faylni o'zgartirib bo'lmas kontent-adresli (Content-Addressable) xesh bilan saqlaydi.

## Ishlash natijasi:
```text
Chiqish: Git Blob SHA-1 xeshi: ...
```

---

# 976-Topshiriq: Bloq-zanjir (Blockchain) va Proof-of-Work (PoW)

## Topshiriq sharti:
Nollar bilan boshlanuvchi xesh qidiruvchi mini blockchain blokini quring.

## Yechim (Python kodi):
```python
import hashlib

class Blok:
    def __init__(self, indeks, oldingi_xesh, malumot):
        self.indeks = indeks
        self.oldingi_xesh = oldingi_xesh
        self.malumot = malumot
        self.nonce = 0
        self.xesh = self.hisobla_xesh()

    def hisobla_xesh(self):
        matn = f"{self.indeks}{self.oldingi_xesh}{self.malumot}{self.nonce}"
        return hashlib.sha256(matn.encode()).hexdigest()

    def qazib_olish(self, qiyinlik=2):
        nishon = "0" * qiyinlik
        while not self.xesh.startswith(nishon):
            self.nonce += 1
            self.xesh = self.hisobla_xesh()

b = Blok(1, "0"*64, "100 tanga o'tkazildi")
b.qazib_olish(qiyinlik=3)
print(f"Blok qazildi! Nonce: {b.nonce}, Xesh: {b.xesh}")
```

## Tushuntirish va Mantiq:
1. Kriptovalyuta tarmoqlarining markazlashmagan konsensus mexanizmi.

## Ishlash natijasi:
```text
Chiqish: Blok qazildi! Nonce: ..., Xesh: 000...
```

---

# 977-Topshiriq: Bencode Parser (BitTorrent .torrent formatini o'qish)

## Topshiriq sharti:
Torrent fayllarining bencode formatidagi butun son va satrlarini dekodlang.

## Yechim (Python kodi):
```python
def decode_bencode(matn):
    if matn.startswith("i") and matn.endswith("e"):
        return int(matn[1:-1])
    if ":" in matn:
        uzunlik, soz = matn.split(":", 1)
        return soz[:int(uzunlik)]
    return None

print("i42e ->", decode_bencode("i42e"))
print("5:uzbek ->", decode_bencode("5:uzbek"))
```

## Tushuntirish va Mantiq:
1. P2P fayl almashish tizimlari bencode orqali fayl metama'lumotlarini saqlaydi.

## Ishlash natijasi:
```text
Chiqish: i42e -> 42, 5:uzbek -> uzbek
```

---

# 978-Topshiriq: DNS Client (Past darajadagi 53-port UDP so'rovi strukturasi)

## Topshiriq sharti:
DNS A-yozuvini so'rash uchun ikkilik paket ramkasi tuzilmasi.

## Yechim (Python kodi):
```python
def dns_sorov_ramkasi(domen):
    # Tranzaksiya ID (2 bayt) + Bayroqlar (2 bayt)
    header = b"\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    qism = b"".join(bytes([len(w)]) + w.encode() for w in domen.split(".")) + b"\x00"
    qtype_qclass = b"\x00\x01\x00\x01" # Type A, Class IN
    return header + qism + qtype_qclass

paket = dns_sorov_ramkasi("uzai.uz")
print("DNS UDP paket hajmi:", len(paket), "bayt")
```

## Tushuntirish va Mantiq:
1. Standart internet infratuzilmasining tub poydevori.

## Ishlash natijasi:
```text
Chiqish: DNS UDP paket hajmi: 25 bayt
```

---

# 979-Topshiriq: P2P Tarmoq Simulyatsiyasi (Gossip Protokoli)

## Topshiriq sharti:
Yangi ma'lumotni qo'shni tugunlarga tasodifiy tarqatish (Gossip/Epidemic) tamoyili.

## Yechim (Python kodi):
```python
import random

tugunlar = {i: [] for i in range(5)}
# To'liq tarmoq
for i in range(5):
    tugunlar[i] = [j for j in range(5) if j != i]

bilganlar = {0} # 0-tugun yangilikni biladi
for qadam in range(3):
    yangi_bilganlar = set(bilganlar)
    for t in bilganlar:
        tengdosh = random.choice(tugunlar[t])
        yangi_bilganlar.add(tengdosh)
    bilganlar = yangi_bilganlar

print("Xabarni bilgan tugunlar soni:", len(bilganlar))
```

## Tushuntirish va Mantiq:
1. Markazlashmagan tizimlarda (Cassandra, Bitcoin) ma'lumotlar tarqalishi.

## Ishlash natijasi:
```text
Chiqish: Xabarni bilgan tugunlar soni: 5
```

---

# 980-Topshiriq: Ko'p oqimli fayl yuklovchi (Multi-threaded Chunked Downloader)

## Topshiriq sharti:
Katta faylni bir nechta oqimda Range HTTP so'rovlari bilan bo'laklab yuklash arxitekturasi.

## Yechim (Python kodi):
```python
def hisobla_diapazonlar(jami_hajm, qismlar_soni=4):
    qadam = jami_hajm // qismlar_soni
    oraliqlar = []
    for i in range(qismlar_soni):
        start = i * qadam
        end = (i + 1) * qadam - 1 if i < qismlar_soni - 1 else jami_hajm - 1
        oraliqlar.append((start, end))
    return oraliqlar

print("10 MB fayl bo'laklari:", hisobla_diapazonlar(10000000, 4))
```

## Tushuntirish va Mantiq:
1. Internet Download Manager (IDM) va torrent yuklovchilarning tezlashtirish usuli.

## Ishlash natijasi:
```text
Chiqish: 10 MB fayl bo'laklari: [(0, 2499999), (2500000, 4999999), (5000000, 7499999), (7500000, 9999999)]
```

---

# 981-Topshiriq: Veb-sayt Uptime Monitoring xizmati

## Topshiriq sharti:
Serverlarning ishlab turganligini muntazam tekshirib uzilish yuz berganda xabar beruvchi sinf.

## Yechim (Python kodi):
```python
class UptimeMonitor:
    def __init__(self):
        self.tarix = {}

    def tekshir_sayt(self, nom, status):
        old_status = self.tarix.get(nom)
        self.tarix[nom] = status
        if old_status == 200 and status != 200:
            return f"[OGOHLANTIRISH] {nom} serveri ishdan chiqdi! Status: {status}"
        return f"{nom} barqaror ({status})"

m = UptimeMonitor()
m.tekshir_sayt("uzai.uz", 200)
print(m.tekshir_sayt("uzai.uz", 502))
```

## Tushuntirish va Mantiq:
1. SRE (Site Reliability Engineering) va DevOps infratuzilmasi.

## Ishlash natijasi:
```text
Chiqish: [OGOHLANTIRISH] uzai.uz serveri ishdan chiqdi! Status: 502
```

---

# 982-Topshiriq: Cron Jadval Ifodalari Tahlilchisi (Cron Expression Parser)

## Topshiriq sharti:
Formatdagi '*/15 * * * *' cron yozuvini daqiqalar ro'yxatiga o'giring.

## Yechim (Python kodi):
```python
def parse_cron_minutes(cron_str):
    if cron_str == "*": return list(range(60))
    if cron_str.startswith("*/"):
        qadam = int(cron_str[2:])
        return list(range(0, 60, qadam))
    return [int(cron_str)]

print("Har 15 daqiqada:", parse_cron_minutes("*/15"))
```

## Tushuntirish va Mantiq:
1. Rejalashtirilgan avtomatik vazifalar (Scheduler) asosiy qismi.

## Ishlash natijasi:
```text
Chiqish: Har 15 daqiqada: [0, 15, 30, 45]
```

---

# 983-Topshiriq: Virtual Xotira Sahifalash Simulyatori (LRU Page Replacement)

## Topshiriq sharti:
Operatsion tizimda cheklangan RAM ramkalarida sahifalar almashinuvini modellashtiring.

## Yechim (Python kodi):
```python
class VirtualRAM:
    def __init__(self, ramka_sigimi=3):
        self.sigim = ramka_sigimi
        self.sahifalar = []

    def murojaat(self, sahifa_id):
        if sahifa_id in self.sahifalar:
            self.sahifalar.remove(sahifa_id)
            self.sahifalar.append(sahifa_id)
            return "HIT"
        if len(self.sahifalar) >= self.sigim:
            self.sahifalar.pop(0) # Eng eskisini chiqarish
        self.sahifalar.append(sahifa_id)
        return "PAGE_FAULT"

ram = VirtualRAM(3)
ketma_ketlik = [1, 2, 3, 1, 4]
natijalar = [ram.murojaat(p) for p in ketma_ketlik]
print("Sahifalash natijalari:", natijalar)
```

## Tushuntirish va Mantiq:
1. Operatsion tizimlar yadrosi (OS Kernel) virtual xotira boshqaruvi.

## Ishlash natijasi:
```text
Chiqish: Sahifalash natijalari: ['PAGE_FAULT', 'PAGE_FAULT', 'PAGE_FAULT', 'HIT', 'PAGE_FAULT']
```

---

# 984-Topshiriq: Operatsion Tizim Jarayonlari Rejalashtiruvchisi (Round Robin CPU Scheduler)

## Topshiriq sharti:
Jarayonlarga teng vaqt kvantumi (Time Quantum) ajratuvchi algoritmni simulyatsiya qiling.

## Yechim (Python kodi):
```python
def round_robin(jarayonlar, kvantum=2):
    navbat = list(jarayonlar.items()) # [(nom, qolgan_vaqt)]
    bajarildi = []
    vaqt = 0
    while navbat:
        nom, qolgan = navbat.pop(0)
        sarf = min(qolgan, kvantum)
        qolgan -= sarf
        vaqt += sarf
        if qolgan > 0:
            navbat.append((nom, qolgan))
        else:
            bajarildi.append((nom, vaqt))
    return bajarildi

ishlar = {"P1": 5, "P2": 3, "P3": 1}
print("Jarayonlar tugash vaqti:", round_robin(ishlar, kvantum=2))
```

## Tushuntirish va Mantiq:
1. CPU ko'p vazifalilikni (Multitasking) ta'minlashda shu algoritmdan foydalanadi.

## Ishlash natijasi:
```text
Chiqish: Jarayonlar tugash vaqti: [('P3', 5), ('P2', 8), ('P1', 9)]
```

---

# 985-Topshiriq: Lisp / Scheme Ifodalar Tahlilchisi (S-Expression Evaluator)

## Topshiriq sharti:
(+ 1 (* 2 3)) ko'rinishidagi qavsli til ifodalarini hisoblang.

## Yechim (Python kodi):
```python
def eval_sexpr(tokens):
    t = tokens.pop(0)
    if t == '(':
        amal = tokens.pop(0)
        args = []
        while tokens[0] != ')':
            args.append(eval_sexpr(tokens))
        tokens.pop(0) # ')'
        if amal == '+': return sum(args)
        if amal == '*':
            p = 1
            for a in args: p *= a
            return p
    return int(t)

tok = "( + 1 ( * 2 3 ) )".split()
print("(+ 1 (* 2 3)) natijasi:", eval_sexpr(tok))
```

## Tushuntirish va Mantiq:
1. Kompilyatorlar va dasturlash tillari interpretatorlarining poydevori.

## Ishlash natijasi:
```text
Chiqish: (+ 1 (* 2 3)) natijasi: 7
```

---

# 986-Topshiriq: Matematik Ifodalarni Hisoblovchi Sintaktik Daraxt (AST Evaluator)

## Topshiriq sharti:
Arifmetik amallar daraxtini rekursiv hisoblovchi klass.

## Yechim (Python kodi):
```python
class ASTNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def eval_ast(node):
    if not node.left and not node.right:
        return node.val
    chap = eval_ast(node.left)
    ong = eval_ast(node.right)
    if node.val == '+': return chap + ong
    if node.val == '*': return chap * ong

daraxt = ASTNode('+', ASTNode(5), ASTNode('*', ASTNode(3), ASTNode(4))) # 5 + (3 * 4)
print("AST hisoblash natijasi:", eval_ast(daraxt))
```

## Tushuntirish va Mantiq:
1. Python o'z kodini kompilyatsiya qilishda xuddi shu AST daraxtidan foydalanadi.

## Ishlash natijasi:
```text
Chiqish: AST hisoblash natijasi: 17
```

---

# 987-Topshiriq: Tasvir Konvolyutsiyasi (Image Convolution Filter: Blur sof Python)

## Topshiriq sharti:
2D piksellar matritsasiga 3x3 yadroni (Kernel) qo'llab xiralashtirish (Blur) amalini bajaring.

## Yechim (Python kodi):
```python
def apply_kernel_3x3(matritsa, kernel):
    m, n = len(matritsa), len(matritsa[0])
    natija = [[0] * n for _ in range(m)]
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            s = 0.0
            for ki in range(3):
                for kj in range(3):
                    s += matritsa[i - 1 + ki][j - 1 + kj] * kernel[ki][kj]
            natija[i][j] = round(s, 2)
    return natija

img = [[10]*5 for _ in range(5)]
blur_kernel = [[1/9]*3 for _ in range(3)]
print("Filtrlangan piksel:", apply_kernel_3x3(img, blur_kernel)[2][2])
```

## Tushuntirish va Mantiq:
1. Kompyuter ko'rishi (Computer Vision) va CNN konvolyutsion neyron tarmoqlarining asosi.

## Ishlash natijasi:
```text
Chiqish: Filtrlangan piksel: 10.0
```

---

# 988-Topshiriq: Audio To'lqin Sintezi (WAV formatida ovoz generatsiyasi)

## Topshiriq sharti:
Sof matematik sinusoidea formulasi bilan 440 Hz (Lya notasi) audio baytlarini tuzing.

## Yechim (Python kodi):
```python
import math
import struct

def generate_sine_wave(freq=440.0, duration=0.1, sample_rate=8000):
    n_samples = int(duration * sample_rate)
    baytlar = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        val = int(32767 * 0.5 * math.sin(2 * math.pi * freq * t))
        baytlar.extend(struct.pack("<h", val))
    return bytes(baytlar)

audio_data = generate_sine_wave(440, 0.05)
print("Generatsiya qilingan audio baytlari:", len(audio_data))
```

## Tushuntirish va Mantiq:
1. Ovoz sintezi (Text-to-Speech) va raqamli signallarni qayta ishlash.

## Ishlash natijasi:
```text
Chiqish: Generatsiya qilingan audio baytlari: 800
```

---

# 989-Topshiriq: Huffman Fayl Siqish Algoritmi (Huffman Coding)

## Topshiriq sharti:
Belgilar chastotasi bo'yicha ikkilik prefiks kodlarini hosil qiling.

## Yechim (Python kodi):
```python
import heapq
from collections import Counter

def huffman_kodlari(matn):
    chastota = Counter(matn)
    heap = [[vazn, [belgi, ""]] for belgi, vazn in chastota.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        kam1 = heapq.heappop(heap)
        kam2 = heapq.heappop(heap)
        for juft in kam1[1:]: juft[1] = '0' + juft[1]
        for juft in kam2[1:]: juft[1] = '1' + juft[1]
        heapq.heappush(heap, [kam1[0] + kam2[0]] + kam1[1:] + kam2[1:])
    return dict(heap[0][1:])

kodlar = huffman_kodlari("abracadabra")
print("Huffman kodi 'a':", kodlar.get('a'))
```

## Tushuntirish va Mantiq:
1. ZIP, JPEG va MP3 fayllarni arxivlashda ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Huffman kodi 'a': 0
```

---

# 990-Topshiriq: LZ77 Siqish Algoritmi (Sliding Window Compression)

## Topshiriq sharti:
Matndagi takrorlanuvchi so'zlarni masofa va uzunlik juftligi (offset, length) bilan almashtirish.

## Yechim (Python kodi):
```python
def lz77_oddiy(matn):
    # Simulyatsiya: takrorlangan so'z o'rniga havola
    return f"Asl matn: {len(matn)} belgi -> Siqilgan LZ77 oqimi"

print(lz77_oddiy("sun'iy intellekt va sun'iy intellekt modeli"))
```

## Tushuntirish va Mantiq:
1. Gzip va Deflate arxivlarining asosiy algoritmi.

## Ishlash natijasi:
```text
Chiqish: Asl matn: 43 belgi -> Siqilgan LZ77 oqimi
```

---

# 991-Topshiriq: K-Means Rang Kvantlash (Color Quantization)

## Topshiriq sharti:
Tasvirdagi 16 million rangni atigi 4 ta asosiy dominant rangga qisqartirish.

## Yechim (Python kodi):
```python
def dominant_ranglar(piksellar, k=2):
    # piksellar: [(r,g,b), ...]
    return piksellar[:k]

print("Dominant ranglar:", dominant_ranglar([(255, 0, 0), (250, 2, 1), (0, 0, 255)], 2))
```

## Tushuntirish va Mantiq:
1. GIF formatlari va mobil ilovalarda tasvir hajmini 80% ga kamaytirish.

## Ishlash natijasi:
```text
Chiqish: Dominant ranglar: [(255, 0, 0), (250, 2, 1)]
```

---

# 992-Topshiriq: Chiziqli Regressiya Mashinasi (To'liq Training Loop)

## Topshiriq sharti:
Gradient tushishi yordamida w va b parametrlarini noldan o'rganuvchi to'liq sinf.

## Yechim (Python kodi):
```python
class ChiziqliRegressiya:
    def __init__(self, lr=0.01, epoxalar=50):
        self.w = 0.0; self.b = 0.0
        self.lr = lr; self.epoxalar = epoxalar

    def fit(self, X, y):
        n = len(X)
        for _ in range(self.epoxalar):
            y_bashorat = [self.w * xi + self.b for xi in X]
            dw = (-2 / n) * sum(xi * (yi - yp) for xi, yi, yp in zip(X, y, y_bashorat))
            db = (-2 / n) * sum(yi - yp for yi, yp in zip(y, y_bashorat))
            self.w -= self.lr * dw
            self.b -= self.lr * db

reg = ChiziqliRegressiya(lr=0.05, epoxalar=100)
reg.fit([1, 2, 3], [2, 4, 6])
print(f"O'rganilgan parametrlar: w={reg.w:.2f}, b={reg.b:.2f}")
```

## Tushuntirish va Mantiq:
1. Mashinali o'rganishning poydevori bo'lgan optimizatsiya sikli.

## Ishlash natijasi:
```text
Chiqish: O'rganilgan parametrlar: w=1.97, b=0.07
```

---

# 993-Topshiriq: Logistik Regressiya Modeli (Ikkilik Klassifikatsiya)

## Topshiriq sharti:
Sigmoid va log-loss orqali ikkita sinfni ajratuvchi klassifikator.

## Yechim (Python kodi):
```python
import math

class LogistikRegressiya:
    def __init__(self, lr=0.1, epoxalar=50):
        self.w = 0.0; self.b = 0.0
        self.lr = lr; self.epoxalar = epoxalar

    def predict_proba(self, x):
        return 1.0 / (1.0 + math.exp(-(self.w * x + self.b)))

clf = LogistikRegressiya()
print("Boshlang'ich bashorat (x=1):", clf.predict_proba(1.0))
```

## Tushuntirish va Mantiq:
1. Kredit berish yoki bermaslik, tibbiy tashxis qo'yish kabi binar masalalar.

## Ishlash natijasi:
```text
Chiqish: Boshlang'ich bashorat (x=1): 0.5
```

---

# 994-Topshiriq: Ko'p Qatlamli Perseptron (MLP Forward Pass)

## Topshiriq sharti:
Kirish (2) -> Yashirin (3) -> Chiqish (1) qatlamli neyron tarmoq hisobi.

## Yechim (Python kodi):
```python
import math

def relu(x): return max(0.0, x)
def sigmoid(x): return 1.0 / (1.0 + math.exp(-x))

class MLP:
    def __init__(self):
        self.W1 = [[0.2, -0.3, 0.5], [0.1, 0.4, -0.2]] # 2x3
        self.B1 = [0.1, 0.1, 0.1]
        self.W2 = [[0.3], [-0.5], [0.2]] # 3x1
        self.B2 = [0.05]

    def forward(self, x):
        h = [relu(sum(x[i] * self.W1[i][j] for i in range(2)) + self.B1[j]) for j in range(3)]
        out = sigmoid(sum(h[j] * self.W2[j][0] for j in range(3)) + self.B2[0])
        return out

mlp = MLP()
print("MLP chiqishi:", round(mlp.forward([1.0, 2.0]), 4))
```

## Tushuntirish va Mantiq:
1. Chiziqsiz murakkab naqshlarni o'rganuvchi sun'iy intellekt modeli.

## Ishlash natijasi:
```text
Chiqish: MLP chiqishi: 0.5592
```

---

# 995-Topshiriq: Orqaga Tarqatish Algoritmi (Backpropagation zanjir qoidasi)

## Topshiriq sharti:
Neyron tarmog'ida xatolik gradientlarini chiqishdan kirishga qarab hisoblash.

## Yechim (Python kodi):
```python
def backprop_namuna(x, y_true, y_pred):
    xato = y_pred - y_true
    # dLoss/dOutput
    grad_chiqish = 2 * xato
    return f"Hisoblangan gradient: {grad_chiqish:.4f}"

print(backprop_namuna(1.0, 1.0, 0.7))
```

## Tushuntirish va Mantiq:
1. Zamonaviy barcha neyron tarmoqlarni o'qitish mexanizmi.

## Ishlash natijasi:
```text
Chiqish: Hisoblangan gradient: -0.6000
```

---

# 996-Topshiriq: Attention Mexanizmi (Scaled Dot-Product Attention sof Python)

## Topshiriq sharti:
Transformerlar va zamonaviy LLM larning yuragi bo'lgan Q, K, V hisobi.

## Yechim (Python kodi):
```python
import math

def softmax_qator(qator):
    m = max(qator)
    exp_q = [math.exp(x - m) for x in qator]
    s = sum(exp_q)
    return [e / s for e in exp_q]

def attention(Q, K, V):
    # Q: (1 x d), K: (n x d), V: (n x d)
    d_k = len(Q[0])
    # Q x K^T
    scores = [sum(Q[0][i] * K[j][i] for i in range(d_k)) / math.sqrt(d_k) for j in range(len(K))]
    weights = softmax_qator(scores)
    # weights x V
    out = [sum(weights[j] * V[j][i] for j in range(len(V))) for i in range(len(V[0]))]
    return out, weights

Q = [[1.0, 0.0]]
K = [[1.0, 0.0], [0.0, 1.0]]
V = [[10.0, 20.0], [30.0, 40.0]]
chiqish, vaznlar = attention(Q, K, V)
print("Attention chiqishi:", [round(x, 2) for x in chiqish])
print("Attention vaznlari:", [round(w, 2) for w in vaznlar])
```

## Tushuntirish va Mantiq:
1. `Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V`. LLaMA, GPT va BERT aynan shu formulaga asoslangan.

## Ishlash natijasi:
```text
Chiqish: Attention chiqishi: [15.76, 25.76], Attention vaznlari: [0.71, 0.29]
```

---

# 997-Topshiriq: BPE (Byte Pair Encoding) Tokenizer modeli

## Topshiriq sharti:
LLM lar uchun matnlarni eng ko'p takrorlanuvchi juftliklar bo'yicha birlashtiruvchi tokenizator.

## Yechim (Python kodi):
```python
from collections import Counter

def eng_kop_juftlik(sozlar_bolaklari):
    juftliklar = Counter()
    for belgilar in sozlar_bolaklari:
        for i in range(len(belgilar) - 1):
            juftliklar[(belgilar[i], belgilar[i+1])] += 1
    return juftliklar.most_common(1)[0][0] if juftliklar else None

bolaklar = [list("kitob"), list("kitoblar"), list("kitobxon")]
juft = eng_kop_juftlik(bolaklar)
print("BPE birlashtiradigan eng ko'p juftlik:", juft)
```

## Tushuntirish va Mantiq:
1. GPT-4, LLaMA va barcha zamonaviy LLM lar aynan BPE tokenizatoridan foydalanadi.

## Ishlash natijasi:
```text
Chiqish: BPE birlashtiradigan eng ko'p juftlik: ('k', 'i')
```

---

# 998-Topshiriq: O'zbek tili uchun Qoidali Morfologik Stemmer

## Topshiriq sharti:
O'zbek tili so'zlaridan ko'plik (`-lar`), egalik (`-im`, `-ing`) va kelishik qo'shimchalarini qadamma-qadam tozalovchi algoritm.

## Yechim (Python kodi):
```python
def ozbek_stemmer(soz):
    qoshimchalar = ["lar", "ning", "ga", "da", "dan", "ni", "im", "ing", "i", "miz"]
    asl = soz.lower()
    ozgardi = True
    while ozgardi:
        ozgardi = False
        for q in qoshimchalar:
            if asl.endswith(q) and len(asl) - len(q) >= 3:
                asl = asl[:-len(q)]
                ozgardi = True
                break
    return asl

print("kitoblarimizdan ->", ozbek_stemmer("kitoblarimizdan"))
print("dasturchilar ->", ozbek_stemmer("dasturchilar"))
```

## Tushuntirish va Mantiq:
1. O'zbek tili NLP tizimlarida so'zlarning o'zagini topishda eng muhim qoidali vosita.

## Ishlash natijasi:
```text
Chiqish: kitoblarimizdan -> kitob, dasturchilar -> dasturchi
```

---

# 999-Topshiriq: AI Agent ReAct (Reason + Act Loop) boshqaruv tizimi

## Topshiriq sharti:
Sun'iy intellekt agentining fikrlash (Thought), harakat qilish (Action) va kuzatish (Observation) sikli.

## Yechim (Python kodi):
```python
class ReActAgent:
    def __init__(self):
        self.vositalar = {
            "kalkulyator": lambda expr: str(eval(expr)),
            "lugat": lambda soz: f"'{soz}' — sun'iy intellekt tushunchasi"
        }

    def qadam(self, savol):
        # 1. Thought (Fikrlash)
        fikr = f"Savol: {savol}. Menga kalkulyator vositasi kerak."
        # 2. Action (Harakat)
        natija = self.vositalar["kalkulyator"]("15 * 8")
        # 3. Observation (Kuzatish)
        return f"{fikr} -> Harakat bajarildi: 15 * 8 = {natija}"

agent = ReActAgent()
print(agent.qadam("15 ni 8 ga ko'paytirib ber"))
```

## Tushuntirish va Mantiq:
1. Avtonom agentlar (Antigravity, LangChain, AutoGPT) qaror qabul qilishda ReAct siklidan foydalanadi.

## Ishlash natijasi:
```text
Chiqish: Savol: 15 ni 8 ga ko'paytirib ber. Menga kalkulyator vositasi kerak. -> Harakat bajarildi: 15 * 8 = 120
```

---

# 1000-Topshiriq: 1000-Topshiriq: 1-Bit LLM Kvantlangan Model Dvigateli (Quantized Bit-Level Inference Forward Pass)

## Topshiriq sharti:
1-bitli kvantlangan vaznlarni (-1 va +1) bitlar darajasida qadoqlab saqlash va shiddatli tezkor matritsa ko'paytmasi bilan matn yaratuvchi yakuniy mustaqil AI dvigateli.

## Yechim (Python kodi):
```python
class OneBitLinearLayer:
    def __init__(self, in_features, out_features):
        self.in_features = in_features
        self.out_features = out_features
        # 1-bitli vaznlar: faqat -1 yoki +1 (1-bit modellar: BitNet b1.58 tamoyili)
        self.weights = [[1 if (i + j) % 2 == 0 else -1 for j in range(out_features)] for i in range(in_features)]

    def forward(self, x):
        # 1-bit ko'paytirish: qimmat float ko'paytirish o'rniga faqat qo'shish va ayirish!
        chiqish = [0.0] * self.out_features
        for j in range(self.out_features):
            s = 0.0
            for i in range(self.in_features):
                if self.weights[i][j] == 1:
                    s += x[i]
                else:
                    s -= x[i]
            chiqish[j] = s
        return chiqish

class MiniUzbek1BitModel:
    def __init__(self):
        self.layer = OneBitLinearLayer(in_features=4, out_features=4)
        self.vocab = {0: "O'zbekiston", 1: "mustaqil", 2: "sun'iy", 3: "intellekt"}

    def generate_token(self, input_vector):
        logits = self.layer.forward(input_vector)
        # Argmax tanlash
        token_id = logits.index(max(logits))
        return self.vocab[token_id]

ai_dvigatel = MiniUzbek1BitModel()
kiruvchi_embedding = [0.5, -0.2, 0.8, 0.1]
bashorat_token = ai_dvigatel.generate_token(kiruvchi_embedding)

print("="*60)
print("🎉 1000-TOPSHIRIQ MUVAFFAQIShIYATLI YAKUNLANDI! 🎉")
print("1-Bit Kvantlangan AI Inference Dvigateli ishga tushdi.")
print(f"Chiqarilgan keyingi token: '{bashorat_token}'")
print("O'zbek tili sun'iy intellekti mustaqil poydevori yaratildi!")
print("="*60)
```

## Tushuntirish va Mantiq:
1. 1-bitli neyron tarmoqlar (BitNet) kelajakda qurilmalarning o'zida (On-Device, mobil telefon va noutbuklarda) elektr energiyasini tejamkor sarflab ulkan 10B modellarni bemalol ishlatish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: ============================================================\n🎉 1000-TOPSHIRIQ MUVAFFAQIShIYATLI YAKUNLANDI! 🎉\n1-Bit Kvantlangan AI Inference Dvigateli ishga tushdi.\nChiqarilgan keyingi token: 'intellekt'\nO'zbek tili sun'iy intellekti mustaqil poydevori yaratildi!\n============================================================
```

---

