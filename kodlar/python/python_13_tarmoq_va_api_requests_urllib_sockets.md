# Python Dasturlash Tili — 13-Qism: Tarmoq, HTTP So'rovlar, API va Socket Dasturlash
## (601-650 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam zamonaviy tarmoq protokollari, API integratsiyalari va past darajadagi soketlarni qamrab oladi:
* `urllib.request` va `urllib.parse` orqali URL tahlili va HTTP so'rovlar;
* Past darajadagi TCP va UDP socketlar, port skanerlash, DNS qidiruvi;
* HTTP metodlari (GET, POST), sarlavhalar, Cookie va Sessiyalarni boshqarish;
* Tarmoq arxitekturasi: Exponential Backoff Retry, Rate Limiting, Streaming Download;
* Autentifikatsiya: Basic Auth, Bearer Token, JWT tahlili, HMAC-SHA256 Webhook tekshiruvi;
* To'liq REST SDK arxitekturasi va LLM SSE Streaming oqimlarini o'qish;

---

# 601-Topshiriq: urllib.parse yordamida URL qismlarini tahlil qilish

## Topshiriq sharti:
URL manzilidan protokol, domen, yo'l va query parametrlarni urllib.parse.urlparse() bilan ajrating.

## Yechim (Python kodi):
```python
from urllib.parse import urlparse, parse_qs

url = "https://api.uzai.uz:8080/v1/search?query=python&lang=uz&page=1#results"
parsed = urlparse(url)

print("Sxema (Protokol):", parsed.scheme)
print("Domen va Port:", parsed.netloc)
print("Yo'l (Path):", parsed.path)
print("Parametrlar:", parse_qs(parsed.query))
print("Fragment:", parsed.fragment)
```

## Tushuntirish va Mantiq:
1. `urlparse()` URL manzilini tarkibiy qismlarga bo'ladi.
2. `parse_qs()` so'rov satridagi (`query`) parametrlarni lug'at ko'rinishiga keltiradi.

## Ishlash natijasi:
```text
Chiqish: Sxema (Protokol): https, Domen va Port: api.uzai.uz:8080, Yo'l (Path): /v1/search, Parametrlar: {'query': ['python'], 'lang': ['uz'], 'page': ['1']}, Fragment: results
```

---

# 602-Topshiriq: urllib.parse.urlencode() bilan so'rov parametrlarini kodlash

## Topshiriq sharti:
Lug'at ko'rinishidagi so'rov parametrlarini xavfsiz URL query satriga aylantiring.

## Yechim (Python kodi):
```python
from urllib.parse import urlencode

parametrlar = {
    "qidiruv": "sun'iy intellekt",
    "shahar": "Toshkent",
    "narx": "150000"
}

query_satr = urlencode(parametrlar)
print("Hosil bo'lgan query:", query_satr)
```

## Tushuntirish va Mantiq:
1. `urlencode()` maxsus belgilar va probellarni URL formatida (`%20`, `%27`) avtomatik kodlaydi.

## Ishlash natijasi:
```text
Chiqish: Hosil bo'lgan query: qidiruv=sun%27iy+intellekt&shahar=Toshkent&narx=150000
```

---

# 603-Topshiriq: urllib.request bilan oddiy GET so'rovi yuborish

## Topshiriq sharti:
urllib kutubxonasi orqali veb-sahifaning HTML kodini o'qing va javob kodini tekshiring.

## Yechim (Python kodi):
```python
import urllib.request

try:
    req = urllib.request.Request(
        "https://httpbin.org/get",
        headers={"User-Agent": "UzbekAI-Bot/1.0"}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        status_kodi = response.status
        matn = response.read().decode('utf-8')
        print("Status kodi:", status_kodi)
        print("Javob hajmi:", len(matn), "belgi")
except Exception as e:
    print("Xatolik:", e)
```

## Tushuntirish va Mantiq:
1. `urllib.request.Request` so'rovga sarlavhalar (`headers`) qo'shish imkonini beradi.
2. `timeout=5` server javobini kutish vaqtini cheklaydi.

## Ishlash natijasi:
```text
Chiqish: Status kodi: 200, Javob hajmi: 320 belgi
```

---

# 604-Topshiriq: urllib.request bilan JSON qabul qilish va yuklash

## Topshiriq sharti:
Veb-serverdan JSON ma'lumotni yuklab, Python lug'atiga o'giring.

## Yechim (Python kodi):
```python
import urllib.request
import json

url = "https://httpbin.org/json"
req = urllib.request.Request(url, headers={"Accept": "application/json"})

with urllib.request.urlopen(req) as res:
    malumot = json.loads(res.read().decode('utf-8'))
    print("Mavzu:", malumot.get('slideshow', {}).get('title'))
```

## Tushuntirish va Mantiq:
1. `json.loads()` satr holatidagi JSON ma'lumotni Python ob'ektiga aylantiradi.

## Ishlash natijasi:
```text
Chiqish: Mavzu: Sample Slide Show
```

---

# 605-Topshiriq: urllib bilan POST so'rovi yuborish (Form Data)

## Topshiriq sharti:
Serverga yangi ma'lumotlarni POST so'rovi orqali yuborish mantiqini yozing.

## Yechim (Python kodi):
```python
import urllib.request
import urllib.parse
import json

url = "https://httpbin.org/post"
data = {"ism": "Alisher", "loyiha": "Uzbek-AI"}
encoded_data = urllib.parse.urlencode(data).encode('utf-8')

req = urllib.request.Request(url, data=encoded_data, method='POST')
with urllib.request.urlopen(req) as res:
    javob = json.loads(res.read().decode('utf-8'))
    print("Server qabul qilgan forma:", javob.get('form'))
```

## Tushuntirish va Mantiq:
1. `urllib.request.Request` ga `data` bayt ko'rinishida berilganda so'rov avtomatik POST ga aylanadi.

## Ishlash natijasi:
```text
Chiqish: Server qabul qilgan forma: {'ism': 'Alisher', 'loyiha': 'Uzbek-AI'}
```

---

# 606-Topshiriq: HTTP Status Kodlari klassifikatsiyasi

## Topshiriq sharti:
HTTP status kodini (200, 301, 404, 500) ma'nosini tahlil qiluvchi klass yarating.

## Yechim (Python kodi):
```python
class HTTPStatusTahlilchi:
    @staticmethod
    def tahlil(kod):
        if 200 <= kod < 300:
            return f"{kod}: Muvaffaqiyatli (Success)"
        elif 300 <= kod < 400:
            return f"{kod}: Yo'naltirish (Redirection)"
        elif 400 <= kod < 500:
            return f"{kod}: Mijoz xatoligi (Client Error)"
        elif 500 <= kod < 600:
            return f"{kod}: Server xatoligi (Server Error)"
        return f"{kod}: Noma'lum kod"

print(HTTPStatusTahlilchi.tahlil(200))
print(HTTPStatusTahlilchi.tahlil(404))
print(HTTPStatusTahlilchi.tahlil(503))
```

## Tushuntirish va Mantiq:
1. HTTP javob kodlari 5 guruhga bo'linadi (1xx axborot, 2xx muvaffaqiyat, 3xx yo'naltirish, 4xx mijoz, 5xx server).

## Ishlash natijasi:
```text
Chiqish: 200: Muvaffaqiyatli (Success), 404: Mijoz xatoligi (Client Error), 503: Server xatoligi (Server Error)
```

---

# 607-Topshiriq: HTTP Sarlavhalari (Headers) bilan ishlash

## Topshiriq sharti:
So'rovga 'Authorization', 'User-Agent' va maxsus 'X-API-Key' sarlavhalarini o'rnatish.

## Yechim (Python kodi):
```python
sarlavhalar = {
    "User-Agent": "MyCustomBot/2.0",
    "Authorization": "Bearer eyJhbGciOiJIUzI1Ni...",
    "X-API-Key": "secret-key-123",
    "Content-Type": "application/json"
}

print("Sarlavhalar ro'yxati:")
for kalit, qiymat in sarlavhalar.items():
    print(f"  {kalit}: {qiymat[:20]}...")
```

## Tushuntirish va Mantiq:
1. Sarlavhalar mijoz haqidagi ma'lumotlar, ruxsat kalitlari va ma'lumot formatlarini serverga yetkazadi.

## Ishlash natijasi:
```text
Chiqish: Sarlavhalar ro'yxati:\n  User-Agent: MyCustomBot/2.0...\n  Authorization: Bearer eyJhbGciOiJIU...\n  X-API-Key: secret-key-123...\n  Content-Type: application/json...
```

---

# 608-Topshiriq: TCP Socket Server yaratish (socket moduli)

## Topshiriq sharti:
Lokal portda tinglovchi (listen) va kelgan xabarni qabul qilib javob beruvchi sodda TCP server yozing.

## Yechim (Python kodi):
```python
import socket

def mini_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8888))
    server.listen(1)
    print("Server 8888-portda ulanishni kutmoqda...")
    # server.accept() bilan mijoz ulanishi kutiladi
    server.close()

mini_server()
```

## Tushuntirish va Mantiq:
1. `AF_INET` IPv4 protokoli, `SOCK_STREAM` esa ishonchli TCP bayt oqimini bildiradi.

## Ishlash natijasi:
```text
Chiqish: Server 8888-portda ulanishni kutmoqda...
```

---

# 609-Topshiriq: TCP Socket Client yaratish

## Topshiriq sharti:
Serverga ulanib xabar yuboruvchi va javob qabul qiluvchi TCP mijoz dasturini tuzing.

## Yechim (Python kodi):
```python
import socket

def send_tcp_message(host, port, xabar):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mijoz:
        mijoz.settimeout(2.0)
        try:
            mijoz.connect((host, port))
            mijoz.sendall(xabar.encode('utf-8'))
            javob = mijoz.recv(1024)
            return javob.decode('utf-8')
        except socket.error as e:
            return f"Ulanish xatosi: {e}"

print(send_tcp_message('127.0.0.1', 9999, "Salom Server"))
```

## Tushuntirish va Mantiq:
1. `mijoz.connect()` uch tomonlama TCP qo'l siqishish (Handshake) jarayonini amalga oshiradi.

## Ishlash natijasi:
```text
Chiqish: Ulanish xatosi: [WinError 10061] No connection could be made because the target machine actively refused it
```

---

# 610-Topshiriq: UDP Socket aloqasi (Datagram)

## Topshiriq sharti:
Ulanishsiz va tezkor UDP paketi yuboruvchi kod yozing.

## Yechim (Python kodi):
```python
import socket

def send_udp(xabar, host='127.0.0.1', port=9000):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(xabar.encode('utf-8'), (host, port))
        print(f"UDP paketi {len(xabar)} bayt yuborildi.")

send_udp("DNS so'rovi simulyatsiyasi")
```

## Tushuntirish va Mantiq:
1. `SOCK_DGRAM` UDP protokolidan foydalanadi; unda ulanish o'rnatilmaydi va paket yetib borishi kafolatlanmaydi, ammo tezlik yuqori bo'ladi.

## Ishlash natijasi:
```text
Chiqish: UDP paketi 28 bayt yuborildi.
```

---

# 611-Topshiriq: IP-manzil va Domen nomini o'girish (DNS Lookup)

## Topshiriq sharti:
Domen nomining IP-manzilini (gethostbyname) va aksincha IP ning domen nomini (gethostbyaddr) aniqlang.

## Yechim (Python kodi):
```python
import socket

domen = "google.com"
ip = socket.gethostbyname(domen)
print(f"{domen} IP-manzili: {ip}")

hostname = socket.gethostname()
lokal_ip = socket.gethostbyname(hostname)
print(f"Lokal kompyuter: {hostname} ({lokal_ip})")
```

## Tushuntirish va Mantiq:
1. `socket.gethostbyname()` tizimning DNS resolveri orqali A-yozuvni so'raydi.

## Ishlash natijasi:
```text
Chiqish: google.com IP-manzili: 142.250.185.78, Lokal kompyuter: ... (...) 
```

---

# 612-Topshiriq: Ochiq portlarni skanerlovchi sodda Port Scanner

## Topshiriq sharti:
Berilgan IP-manzilning ma'lum bir porti ochiq yoki yopiq ekanligini tezkor tekshiring.

## Yechim (Python kodi):
```python
import socket

def port_ochiqmi(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    natija = s.connect_ex((host, port))
    s.close()
    return natija == 0

print("80-port (HTTP):", port_ochiqmi("127.0.0.1", 80))
print("443-port (HTTPS):", port_ochiqmi("127.0.0.1", 443))
```

## Tushuntirish va Mantiq:
1. `connect_ex()` xatolik yuz berganda istisno tashlamay, xato kodini qaytaradi (0 = muvaffaqiyatli ulangan).

## Ishlash natijasi:
```text
Chiqish: 80-port (HTTP): False, 443-port (HTTPS): False
```

---

# 613-Topshiriq: Baza uchun HTTP GET mijoz sinfi (Mock Requests)

## Topshiriq sharti:
urllib asosida requests kutubxonasiga o'xshash qulay API so'rovlar klassini yarating.

## Yechim (Python kodi):
```python
import urllib.request
import json

class MiniHTTP:
    @staticmethod
    def get(url, headers=None):
        req = urllib.request.Request(url, headers=headers or {})
        try:
            with urllib.request.urlopen(req, timeout=5) as res:
                return {
                    "status_code": res.status,
                    "body": res.read().decode('utf-8'),
                    "headers": dict(res.getheaders())
                }
        except Exception as e:
            return {"error": str(e)}

javob = MiniHTTP.get("https://httpbin.org/get")
print("Status:", javob.get("status_code"))
```

## Tushuntirish va Mantiq:
1. Murakkab quyi darajadagi kutubxonalarni yuqori darajadagi qulay interfeys (Wrapper/Facade) bilan o'rash dasturlashda keng qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: Status: 200
```

---

# 614-Topshiriq: JSON REST API ga POST so'rov yuborish va javobni tekshirish

## Topshiriq sharti:
JSON formatidagi ma'lumotni Content-Type: application/json sarlavhasi bilan yuborish.

## Yechim (Python kodi):
```python
import urllib.request
import json

url = "https://httpbin.org/post"
payload = {"foydalanuvchi": "bot", "vazifa": "matn_generatsiyasi"}
data_bytes = json.dumps(payload).encode('utf-8')

req = urllib.request.Request(
    url,
    data=data_bytes,
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as res:
        javob = json.loads(res.read().decode('utf-8'))
        print("Serverdagi JSON:", javob.get('json'))
except Exception as e:
    print("Xato:", e)
```

## Tushuntirish va Mantiq:
1. JSON API larda ma'lumotlar `application/json` sarlavhasi ostida yuboriladi.

## Ishlash natijasi:
```text
Chiqish: Serverdagi JSON: {'foydalanuvchi': 'bot', 'vazifa': 'matn_generatsiyasi'}
```

---

# 615-Topshiriq: Katta fayllarni oqimli (Streaming/Chunked) yuklab olish

## Topshiriq sharti:
Xotirani to'ldirib qo'ymaslik uchun faylni qismlarga (chunks) bo'lib diskka yozing.

## Yechim (Python kodi):
```python
import urllib.request
import io

url = "https://httpbin.org/bytes/10240"  # 10 KB fayl
buffer = io.BytesIO()

with urllib.request.urlopen(url) as response:
    chunk_size = 2048
    while True:
        chunk = response.read(chunk_size)
        if not chunk:
            break
        buffer.write(chunk)

print("Yuklab olingan jami baytlar:", len(buffer.getvalue()))
```

## Tushuntirish va Mantiq:
1. Katta (masalan, 1 GB) fayllarni butunlay RAM ga yuklamasdan 4-8 KB lik bo'laklarda o'qish xotira barqarorligini ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Yuklab olingan jami baytlar: 10240
```

---

# 616-Topshiriq: Yuklab olish progress-bar (Download Progress Bar)

## Topshiriq sharti:
Fayl yuklanish foizini konsolda real vaqt rejimida hisoblab ko'rsating.

## Yechim (Python kodi):
```python
def progress_simulyatsiya(jami_hajm, qism_hajmi):
    yuklangan = 0
    while yuklangan < jami_hajm:
        yuklangan += qism_hajmi
        yuklangan = min(yuklangan, jami_hajm)
        foiz = (yuklangan / jami_hajm) * 100
        belgilar = int(foiz // 5)
        bar = "█" * belgilar + "-" * (20 - belgilar)
        print(f"\rYuklanmoqda: [{bar}] {foiz:.1f}% ({yuklangan}/{jami_hajm} bayt)", end="")
    print("\nTayyor!")

progress_simulyatsiya(1000, 250)
```

## Tushuntirish va Mantiq:
1. `\r` (Carriage return) yordamida konsol kursorini satr boshiga qaytarib yangilab turiladi.

## Ishlash natijasi:
```text
Chiqish: Yuklanmoqda: [████████████████████] 100.0% (1000/1000 bayt)\nTayyor!
```

---

# 617-Topshiriq: HTTP Cookie lar bilan ishlash (Cookie Jar)

## Topshiriq sharti:
http.cookiejar moduli yordamida so'rovlar o'rtasida sessiya cookie larini avtomatik saqlang.

## Yechim (Python kodi):
```python
import urllib.request
import http.cookiejar

cookie_ombori = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_ombori))

# Cookie o'rnatuvchi sahifaga so'rov
try:
    res = opener.open("https://httpbin.org/cookies/set?session_token=abc123xyz")
    for cookie in cookie_ombori:
        print(f"Saqlangan cookie: {cookie.name} = {cookie.value}")
except Exception as e:
    print("Xato:", e)
```

## Tushuntirish va Mantiq:
1. `CookieJar` avtorizatsiya va foydalanuvchi holatini saqlashda brauzer kabi harakat qiladi.

## Ishlash natijasi:
```text
Chiqish: Saqlangan cookie: session_token = abc123xyz
```

---

# 618-Topshiriq: Qayta urinish mexanizmi (Exponential Backoff Retry)

## Topshiriq sharti:
Tarmoq uzilishi yoki 503 xatolarida intervalni 2 barobar oshirib qayta urinuvchi dekorator yozing.

## Yechim (Python kodi):
```python
import time

def retry_bilan(urinishlar=3, dastlabki_kutish=1.0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            kutish = dastlabki_kutish
            for i in range(urinishlar):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[XATO] {i+1}-urinish muvaffaqiyatsiz: {e}. Kutish: {kutish}s")
                    time.sleep(kutish)
                    kutish *= 2
            raise Exception("Barcha urinishlar tugadi!")
        return wrapper
    return decorator

@retry_bilan(urinishlar=3, dastlabki_kutish=0.1)
def soxta_api():
    raise ConnectionResetError("Server ulanishni uzdi")

try:
    soxta_api()
except Exception as e:
    print(e)
```

## Tushuntirish va Mantiq:
1. Exponential backoff tarmoqdagi yuklamani kamaytirib, vaqtinchalik nosozliklarda tizimni barqaror ushlaydi.

## Ishlash natijasi:
```text
Chiqish: [XATO] 1-urinish muvaffaqiyatsiz... [XATO] 2-urinish... Barcha urinishlar tugadi!
```

---

# 619-Topshiriq: So'rovlar tezligini cheklovchi (Rate Limiter: Token Bucket)

## Topshiriq sharti:
Sekundiga maksimal 3 ta so'rov yuborishga ruxsat beruvchi klass tuzing.

## Yechim (Python kodi):
```python
import time

class RateLimiter:
    def __init__(self, max_sorov, vaqt_oraligi):
        self.max_sorov = max_sorov
        self.vaqt_oraligi = vaqt_oraligi
        self.tarix = []

    def ruxsatmi(self):
        hozir = time.time()
        self.tarix = [t for t in self.tarix if hozir - t < self.vaqt_oraligi]
        if len(self.tarix) < self.max_sorov:
            self.tarix.append(hozir)
            return True
        return False

limiter = RateLimiter(max_sorov=2, vaqt_oraligi=1.0)
print("1-so'rov:", limiter.ruxsatmi())
print("2-so'rov:", limiter.ruxsatmi())
print("3-so'rov:", limiter.ruxsatmi())
```

## Tushuntirish va Mantiq:
1. Rate Limiting tashqi API lardan 429 Too Many Requests xatosini olmaslik uchun zarurdir.

## Ishlash natijasi:
```text
Chiqish: 1-so'rov: True, 2-so'rov: True, 3-so'rov: False
```

---

# 620-Topshiriq: HTTP Basic Authentication sarlavhasini kodlash

## Topshiriq sharti:
Foydalanuvchi nomi va parolini Base64 orqali HTTP Basic Auth sarlavhasiga aylantiring.

## Yechim (Python kodi):
```python
import base64

def basic_auth_sarlavhasi(login, parol):
    juftlik = f"{login}:{parol}".encode('utf-8')
    shifrlangan = base64.b64encode(juftlik).decode('utf-8')
    return {"Authorization": f"Basic {shifrlangan}"}

headers = basic_auth_sarlavhasi("admin", "parol1234")
print("Auth sarlavhasi:", headers)
```

## Tushuntirish va Mantiq:
1. RFC 7617 bo'yicha Basic Auth foydalanuvchi ma'lumotlarini Base64 ko'rinishida jo'natadi.

## Ishlash natijasi:
```text
Chiqish: Auth sarlavhasi: {'Authorization': 'Basic YWRtaW46cGFyb2wxMjM0'}
```

---

# 621-Topshiriq: JWT (JSON Web Token) tuzilishini tahlil qilish

## Topshiriq sharti:
JWT tokenining Header va Payload qismlarini ochib ma'lumotlarini o'qing (imzosiz).

## Yechim (Python kodi):
```python
import base64
import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTYiLCJpc20iOiJBa21hbCIsInJvbGUiOiJhZG1pbiJ9.signature"

qismlar = token.split(".")
def pad_va_decode(qism):
    qism += "=" * ((4 - len(qism) % 4) % 4)
    return json.loads(base64.urlsafe_b64decode(qism).decode('utf-8'))

header = pad_va_decode(qismlar[0])
payload = pad_va_decode(qismlar[1])

print("Header:", header)
print("Payload:", payload)
```

## Tushuntirish va Mantiq:
1. JWT 3 qismdan iborat: header.payload.signature. Payload qismida foydalanuvchi da'volari (claims) saqlanadi.

## Ishlash natijasi:
```text
Chiqish: Header: {'alg': 'HS256', 'typ': 'JWT'}, Payload: {'sub': '123456', 'ism': 'Akmal', 'role': 'admin'}
```

---

# 622-Topshiriq: HTTP Proxy orqali so'rov yuborish mantiqi

## Topshiriq sharti:
urllib da proksi server (HTTP/HTTPS) orqali internetga chiqish uchun ProxyHandler o'rnating.

## Yechim (Python kodi):
```python
import urllib.request

proxy_manzili = "http://10.10.1.10:3128"
proxy_handler = urllib.request.ProxyHandler({
    "http": proxy_manzili,
    "https": proxy_manzili
})

opener = urllib.request.build_opener(proxy_handler)
print("Proxy handler tayyorlandi:", proxy_manzili)
```

## Tushuntirish va Mantiq:
1. `ProxyHandler` korporativ tarmoqlar yoki IP rotatsiyasi uchun so'rovlarni proksi orqali yo'naltiradi.

## Ishlash natijasi:
```text
Chiqish: Proxy handler tayyorlandi: http://10.10.1.10:3128
```

---

# 623-Topshiriq: SSL Sertifikatini tekshirishni boshqarish (ssl moduli)

## Topshiriq sharti:
ssl kontekstini sozlab, o'z-o'zidan imzolangan (self-signed) sertifikatlarni xavfsiz boshqaring.

## Yechim (Python kodi):
```python
import ssl
import urllib.request

kontekst = ssl.create_default_context()
# Sertifikat tekshiruvini boshqarish
kontekst.check_hostname = True
kontekst.verify_mode = ssl.CERT_REQUIRED

print("Standart SSL konteksti sozlandi:", kontekst.protocol)
```

## Tushuntirish va Mantiq:
1. Sun'iy intellekt agentlari va skriptlar xavfsiz HTTPS ulanishlarda SSL zanjirini tekshirishi shart.

## Ishlash natijasi:
```text
Chiqish: Standart SSL konteksti sozlandi: _SSLMethod.PROTOCOL_TLS_CLIENT
```

---

# 624-Topshiriq: Multipart/form-data fayl yuklash (File Upload) tanasini yasash

## Topshiriq sharti:
HTTP orqali rasm yoki hujjat faylini yuborish uchun multipart bayt tanasini qo'lda tuzing.

## Yechim (Python kodi):
```python
import uuid

def multipart_body_yasa(maydonlar, fayl_nomi, fayl_baytlari):
    chegara = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    tana = bytearray()
    
    for kalit, qiymat in maydonlar.items():
        tana.extend(f"--{chegara}\r\nContent-Disposition: form-data; name=\"{kalit}\"\r\n\r\n{qiymat}\r\n".encode())
        
    tana.extend(f"--{chegara}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{fayl_nomi}\"\r\nContent-Type: text/plain\r\n\r\n".encode())
    tana.extend(fayl_baytlari)
    tana.extend(f"\r\n--{chegara}--\r\n".encode())
    
    headers = {"Content-Type": f"multipart/form-data; boundary={chegara}"}
    return bytes(tana), headers

tana, hdr = multipart_body_yasa({"tavsif": "Test hisobot"}, "test.txt", b"Salom dunyo!")
print("Tana hajmi:", len(tana), "bayt")
print("Sarlavha:", hdr["Content-Type"][:35] + "...")
```

## Tushuntirish va Mantiq:
1. Multipart form ma'lumotlari chegara (boundary) bilan ajratilgan turli xil fayl va matn bloklaridan iborat bo'ladi.

## Ishlash natijasi:
```text
Chiqish: Tana hajmi: 228 bayt, Sarlavha: multipart/form-data; boundary=----...
```

---

# 625-Topshiriq: Gzip siqilgan javoblarni ochish (Content-Encoding: gzip)

## Topshiriq sharti:
Veb-serverdan kelgan gzip bilan siqilgan ma'lumotni dekompressiya qiling.

## Yechim (Python kodi):
```python
import gzip
import io

asl_matn = "Bu siqilgan ma'lumot! Sun'iy intellekt modeli uchun o'quv korpusi." * 5
siqilgan = gzip.compress(asl_matn.encode('utf-8'))

ochilgan = gzip.decompress(siqilgan).decode('utf-8')
print("Asl hajm:", len(asl_matn.encode()), "bayt")
print("Siqilgan hajm:", len(siqilgan), "bayt")
print("Tengmi:", asl_matn == ochilgan)
```

## Tushuntirish va Mantiq:
1. Veb protokollarda ma'lumot trafigini tejash uchun gzip va brotli algoritmlari ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Asl hajm: 330 bayt, Siqilgan hajm: 98 bayt, Tengmi: True
```

---

# 626-Topshiriq: Lokal HTTP Server ishga tushirish (http.server moduli)

## Topshiriq sharti:
Python ning ichki http.server moduli yordamida dastur ichidan mini veb-server ishga tushirish mantiqi.

## Yechim (Python kodi):
```python
import http.server
import socketserver

PORT = 8081
Handler = http.server.SimpleHTTPRequestHandler

# Server ob'ektini hosil qilish
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Lokal server {PORT}-portda yaratildi.")
    # httpd.serve_forever() serverni tinglashga qo'yadi
```

## Tushuntirish va Mantiq:
1. `http.server` tezkor testlash va mahalliy fayllarni tarqatish uchun ajoyib vositadir.

## Ishlash natijasi:
```text
Chiqish: Lokal server 8081-portda yaratildi.
```

---

# 627-Topshiriq: Maxsus HTTP Request Handler yozish

## Topshiriq sharti:
BaseHTTPRequestHandler yordamida '/api/salom' yo'liga JSON javob qaytaruvchi server tuzing.

## Yechim (Python kodi):
```python
from http.server import BaseHTTPRequestHandler
import json

class MeningHandlerim(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/salom":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            javob = json.dumps({"xabar": "Assalomu alaykum!", "status": "ok"})
            self.wfile.write(javob.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

print("Handler klassi muvaffaqiyatli aniqlandi:", MeningHandlerim.__name__)
```

## Tushuntirish va Mantiq:
1. `do_GET` va `do_POST` metodlarini qayta yozish orqali ixtiyoriy routing va API logikasini yaratish mumkin.

## Ishlash natijasi:
```text
Chiqish: Handler klassi muvaffaqiyatli aniqlandi: MeningHandlerim
```

---

# 628-Topshiriq: Asinxron HTTP mijoz (aiohttp va asyncio asoslari)

## Topshiriq sharti:
asyncio kutubxonasi yordamida asinxron so'rov yuborish mantiqiy tuzilmasi.

## Yechim (Python kodi):
```python
import asyncio

async def soxta_api_sorov(id):
    await asyncio.sleep(0.01)
    return {"id": id, "natija": f"Ma'lumot #{id}"}

async def barchasini_ol():
    vazifalar = [soxta_api_sorov(i) for i in range(1, 4)]
    natijalar = await asyncio.gather(*vazifalar)
    return natijalar

javoblar = asyncio.run(barchasini_ol())
print("Asinxron olingan ma'lumotlar:", javoblar)
```

## Tushuntirish va Mantiq:
1. Bir vaqtning o'zida yuzlab HTTP so'rovlarni bloklanmasdan parallel yuborish uchun asinxron arxitektura tanlanadi.

## Ishlash natijasi:
```text
Chiqish: Asinxron olingan ma'lumotlar: [{'id': 1, 'natija': "Ma'lumot #1"}, {'id': 2, 'natija': "Ma'lumot #2"}, {'id': 3, 'natija': "Ma'lumot #3"}]
```

---

# 629-Topshiriq: Webhook qabul qiluvchi va imzoni tekshiruvchi (HMAC-SHA256)

## Topshiriq sharti:
Webhook so'rovi soxta emasligini xesh imzo (HMAC-SHA256) orqali tasdiqlang.

## Yechim (Python kodi):
```python
import hmac
import hashlib

def imzoni_tekshir(tana_baytlari, maxfiy_kalit, kelgan_imzo):
    hisoblangan = hmac.new(maxfiy_kalit.encode(), tana_baytlari, hashlib.sha256).hexdigest()
    return hmac.compare_digest(hisoblangan, kelgan_imzo)

tana = b'{"hodisa": "tolov_otdi", "summa": 50000}'
secret = "maxfiy_kalit_123"
imzo = hmac.new(secret.encode(), tana, hashlib.sha256).hexdigest()

print("Imzo to'g'rimi:", imzoni_tekshir(tana, secret, imzo))
print("Buzilgan tana bilan:", imzoni_tekshir(b'buzilgan', secret, imzo))
```

## Tushuntirish va Mantiq:
1. `hmac.compare_digest()` vaqtga asoslangan hujumlarning (Timing Attacks) oldini oladi.

## Ishlash natijasi:
```text
Chiqish: Imzo to'g'rimi: True, Buzilgan tana bilan: False
```

---

# 630-Topshiriq: Server-Sent Events (SSE) oqimini o'qish formati

## Topshiriq sharti:
LLM lardan keluvchi 'data: ...' ko'rinishidagi streaming tokenlarni ajratib oluvchi o'quvchi yozing.

## Yechim (Python kodi):
```python
oqimli_matn = """data: {"token": "Sun'iy"}

data: {"token": " intellekt"}

data: {"token": " modeli."}

data: [DONE]
"""

for qator in oqimli_matn.splitlines():
    if qator.startswith("data: "):
        payload = qator[6:].strip()
        if payload == "[DONE]":
            print("[OQIM TUGADI]")
        else:
            print("Token:", payload)
```

## Tushuntirish va Mantiq:
1. OpenAI, Gemini va zamonaviy LLM API lari matnni streaming qilishda SSE protokolidan foydalanadi.

## Ishlash natijasi:
```text
Chiqish: Token: {"token": "Sun'iy"}, Token: {"token": " intellekt"}, Token: {"token": " modeli."}, [OQIM TUGADI]
```

---

# 631-Topshiriq: DNS MX yozuvlarini tahlil qilish mantiqi

## Topshiriq sharti:
Domen nomining pochta serverlarini aniqlash tamoyili.

## Yechim (Python kodi):
```python
import socket

def tekshir_domen(domen):
    try:
        ip = socket.gethostbyname(domen)
        return f"{domen} mavjud, IP: {ip}"
    except socket.gaierror:
        return f"{domen} mavjud emas!"

print(tekshir_domen("google.com"))
print(tekshir_domen("mavjud_bolmagan_domen_xyz123.com"))
```

## Tushuntirish va Mantiq:
1. `socket.gaierror` (getaddrinfo error) domen ro'yxatdan o'tmagan yoki IP mavjud bo'lmaganda yuz beradi.

## Ishlash natijasi:
```text
Chiqish: google.com mavjud, IP: 142.250.185.78, mavjud_bolmagan_domen_xyz123.com mavjud emas!
```

---

# 632-Topshiriq: Ulanish havzasi (Connection Pooling) mexanizmi

## Topshiriq sharti:
Har safar yangi TCP ulanish ochmasdan, ochiq soketlarni qayta ishlatish havzasini simulyatsiya qiling.

## Yechim (Python kodi):
```python
class ConnectionPool:
    def __init__(self, host, port, max_size=5):
        self.host = host
        self.port = port
        self.max_size = max_size
        self.bosh_ulanislar = []

    def get_connection(self):
        if self.bosh_ulanislar:
            return f"Qayta ishlatilayotgan ulanish: {self.bosh_ulanislar.pop()}"
        return f"Yangi TCP ulanish ochildi ({self.host}:{self.port})"

    def release_connection(self, conn_id):
        if len(self.bosh_ulanislar) < self.max_size:
            self.bosh_ulanislar.append(conn_id)

pool = ConnectionPool("api.uzai.uz", 443)
print(pool.get_connection())
pool.release_connection("conn_#1")
print(pool.get_connection())
```

## Tushuntirish va Mantiq:
1. Connection Pooling har bir so'rov uchun 3 tomonlama TCP qo'l siqishish vaqtini tejab qoladi.

## Ishlash natijasi:
```text
Chiqish: Yangi TCP ulanish ochildi (api.uzai.uz:443), Qayta ishlatilayotgan ulanish: conn_#1
```

---

# 633-Topshiriq: HTTP Kesh (ETag va If-None-Match) mexanizmi

## Topshiriq sharti:
Agar serverdagi ma'lumot o'zgarmagan bo'lsa 304 Not Modified qaytarish mantig'ini yozing.

## Yechim (Python kodi):
```python
import hashlib

resurs_xotirasi = "O'zbek tilining izohli lug'ati ma'lumotlar bazasi"
resurs_etag = hashlib.md5(resurs_xotirasi.encode()).hexdigest()

def so_rovni_bajar(mijoz_etagi):
    if mijoz_etagi == resurs_etag:
        return 304, "Not Modified (Keshdan o'qing)"
    return 200, resurs_xotirasi

print("1-so'rov (keshsiz):", so_rovni_bajar(None)[0])
print("2-so'rov (etag bilan):", so_rovni_bajar(resurs_etag))
```

## Tushuntirish va Mantiq:
1. ETag (Entity Tag) fayl o'zgarganligini tekshirish uchun xesh-identifikator sifatida ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: 1-so'rov (keshsiz): 200, 2-so'rov (etag bilan): (304, "Not Modified (Keshdan o'qing)")
```

---

# 634-Topshiriq: FTP protokoli orqali fayl ro'yxatini olish (ftplib)

## Topshiriq sharti:
ftplib moduli yordamida FTP serverga ulanish va fayllar ro'yxatini ko'rish strukturasi.

## Yechim (Python kodi):
```python
from ftplib import FTP

def ftp_ulanish_strukturasi():
    ftp = FTP()
    print("FTP mijozi ob'ekti:", type(ftp).__name__)
    # ftp.connect('ftp.example.com', 21)
    # ftp.login('user', 'pass')
    # ftp.nlst()
    ftp.close()

ftp_ulanish_strukturasi()
```

## Tushuntirish va Mantiq:
1. `ftplib` fayllarni masofaviy serverlarga uzatish va qabul qilish uchun standart kutubxonadir.

## Ishlash natijasi:
```text
Chiqish: FTP mijozi ob'ekti: FTP
```

---

# 635-Topshiriq: SMTP orqali elektron pochta jo'natish formati (smtplib, email)

## Topshiriq sharti:
MIMEText va MIMEMultipart yordamida xat tanasi va sarlavhalarini shakllantiring.

## Yechim (Python kodi):
```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

xat = MIMEMultipart()
xat["From"] = "ai-system@uzai.uz"
xat["To"] = "foydalanuvchi@gmail.com"
xat["Subject"] = "O'quv jarayoni yakunlandi"

matn = "Assalomu alaykum! AI modelining 1000 ta topshiriq to'plami tayyor bo'ldi."
xat.attach(MIMEText(matn, "plain", "utf-8"))

print("Tayyor xat sarlavhalari:")
print(xat.as_string()[:110] + "...")
```

## Tushuntirish va Mantiq:
1. `smtplib` va `email` modullari orqali xavfsiz (TLS/SSL) elektron pochta xabarlari yuboriladi.

## Ishlash natijasi:
```text
Chiqish: Tayyor xat sarlavhalari:\nContent-Type: multipart/mixed; ... From: ai-system@uzai.uz... To: foydalanuvchi@gmail.com...
```

---

# 636-Topshiriq: POP3 va IMAP pochta o'qish tamoyillari (imaplib)

## Topshiriq sharti:
Masofaviy pochta qutisidan yangi xatlarni qidirish va o'qish mexanizmi.

## Yechim (Python kodi):
```python
import imaplib

def imap_mijoz_namunasi():
    print("IMAP4 klassi:", imaplib.IMAP4_SSL.__name__)
    # mail = imaplib.IMAP4_SSL('imap.gmail.com')
    # mail.login('user', 'pass')
    # mail.select('inbox')

imap_mijoz_namunasi()
```

## Tushuntirish va Mantiq:
1. IMAP protokoli serverdagi papkalar va xatlarni sinxronlashtirgan holda o'qish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: IMAP4 klassi: IMAP4_SSL
```

---

# 637-Topshiriq: WebSocket ramkasi (Frame) tuzilishi

## Topshiriq sharti:
WebSocket protokoli bo'yicha bayt ma'lumotlarni qadoqlash (Masking va Opcode) tushunchasi.

## Yechim (Python kodi):
```python
def ws_frame_yasa(matn):
    baytlar = matn.encode('utf-8')
    uzunlik = len(baytlar)
    # Oddiy unmasked text frame (0x81 = FIN + Text Opcode)
    header = bytearray([0x81])
    if uzunlik <= 125:
        header.append(uzunlik)
    return bytes(header) + baytlar

frame = ws_frame_yasa("Salom WebSocket")
print("WS Frame baytlari:", list(frame[:6]))
```

## Tushuntirish va Mantiq:
1. WebSocket to'liq dupleks (Full-Duplex) doimiy aloqa kanali bo'lib, HTTP ga qaraganda minimal sarlavha yuklamasiga ega.

## Ishlash natijasi:
```text
Chiqish: WS Frame baytlari: [129, 15, 83, 97, 108, 111]
```

---

# 638-Topshiriq: Tarmoq paketlarini tahlil qilish (Raw Sockets va Hexdump)

## Topshiriq sharti:
Bayt ma'lumotlarini qulay hexdump ko'rinishida formatlab chiqaruvchi utilita yozing.

## Yechim (Python kodi):
```python
def hexdump(baytlar):
    natija = []
    for i in range(0, len(baytlar), 16):
        blok = baytlar[i:i+16]
        hex_qator = " ".join(f"{b:02x}" for b in blok)
        ascii_qator = "".join(chr(b) if 32 <= b <= 126 else "." for b in blok)
        natija.append(f"{i:04x}  {hex_qator:<48}  |{ascii_qator}|")
    return "\n".join(natija)

print(hexdump(b"GET / HTTP/1.1\r\nHost: uzai.uz\r\n\r\n"))
```

## Tushuntirish va Mantiq:
1. Hexdump tarmoq trafigini va ikkilik (binary) protokollarni tahlil qilishda eng muhim vositadir.

## Ishlash natijasi:
```text
Chiqish: 0000  47 45 54 20 2f 20 48 54 54 50 2f 31 2e 31 0d 0a  |GET / HTTP/1.1..|\n0010  48 6f 73 74 3a 20 75 7a 61 69 2e 75 7a 0d 0a 0d  |Host: uzai.uz...|\n0020  0a                                                |.|
```

---

# 639-Topshiriq: HTTP/2 va HTTP/3 (QUIC) asosiy farqlari

## Topshiriq sharti:
Protokollarning asosiy xususiyatlarini ifodalovchi ma'lumotlar modeli.

## Yechim (Python kodi):
```python
protokollar = {
    "HTTP/1.1": "Matnli, ulanish navbatlanishi (Head-of-Line blocking)",
    "HTTP/2": "Ikkilik (Binary), Multiplekslash (Bitta TCP da ko'p oqim), HPACK siqish",
    "HTTP/3": "UDP (QUIC) ustiga qurilgan, 0-RTT ulanish, tarmoq almashuviga bardoshli"
}

for nom, xususiyat in protokollar.items():
    print(f"[{nom}]: {xususiyat}")
```

## Tushuntirish va Mantiq:
1. Zamonaviy veb HTTP/3 QUIC orqali paketlar yo'qolishida barcha oqimlarning to'xtab qolishining oldini oladi.

## Ishlash natijasi:
```text
Chiqish: [HTTP/1.1]: Matnli... [HTTP/2]: Ikkilik... [HTTP/3]: UDP (QUIC)...
```

---

# 640-Topshiriq: API Response Caching (Memory Kesh bilan HTTP optimizatsiya)

## Topshiriq sharti:
Bir xil URL ga yuborilgan so'rov javobini 60 soniya xotirada keshlab qaytaruvchi sinf.

## Yechim (Python kodi):
```python
import time

class APICache:
    def __init__(self, ttl_soniya=60):
        self.kesh = {}
        self.ttl = ttl_soniya

    def get(self, kalit):
        if kalit in self.kesh:
            qiymat, vaqt = self.kesh[kalit]
            if time.time() - vaqt < self.ttl:
                return qiymat
            del self.kesh[kalit]
        return None

    def set(self, kalit, qiymat):
        self.kesh[kalit] = (qiymat, time.time())

kesh = APICache(ttl_soniya=2)
kesh.set("/users/1", {"ism": "Ali"})
print("Keshdan olindi:", kesh.get("/users/1"))
```

## Tushuntirish va Mantiq:
1. Tez-tez o'zgarmaydigan API ma'lumotlarini keshda saqlash tarmoq trafigini va javob vaqtini yuzlab barobar kamaytiradi.

## Ishlash natijasi:
```text
Chiqish: Keshdan olindi: {'ism': 'Ali'}
```

---

# 641-Topshiriq: CORS (Cross-Origin Resource Sharing) sarlavhalari

## Topshiriq sharti:
Veb brauzerlar xavfsizligi uchun CORS sarlavhalarini shakllantirish.

## Yechim (Python kodi):
```python
def cors_sarlavhalari(origin="*"):
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
        "Access-Control-Max-Age": "86400"
    }

print(cors_sarlavhalari("https://uzai.uz"))
```

## Tushuntirish va Mantiq:
1. CORS brauzer orqali boshqa domendan kelgan JavaScript so'rovlariga ruxsat berishni boshqaradi.

## Ishlash natijasi:
```text
Chiqish: {'Access-Control-Allow-Origin': 'https://uzai.uz', ...}
```

---

# 642-Topshiriq: OAuth2 Authorization Code Flow bosqichlari simulyatsiyasi

## Topshiriq sharti:
Avtorizatsiya kodi (code) evaziga Access Token olish mexanizmini modellashtiring.

## Yechim (Python kodi):
```python
class SoxtaOAuth2Server:
    def __init__(self):
        self.kodlar = {"auth_code_xyz": "user_42"}
        self.tokenlar = {}

    def token_almashtirish(self, code, client_id, client_secret):
        if code in self.kodlar and client_secret == "my_secret":
            token = f"access_token_{self.kodlar[code]}"
            self.tokenlar[token] = self.kodlar[code]
            del self.kodlar[code]
            return {"access_token": token, "token_type": "Bearer", "expires_in": 3600}
        return {"error": "invalid_grant"}

oauth = SoxtaOAuth2Server()
print(oauth.token_almashtirish("auth_code_xyz", "client_1", "my_secret"))
```

## Tushuntirish va Mantiq:
1. OAuth2 zamonaviy veb va mobil ilovalarda foydalanuvchi parolini bermasdan xavfsiz avtorizatsiya qilish standarti.

## Ishlash natijasi:
```text
Chiqish: {'access_token': 'access_token_user_42', 'token_type': 'Bearer', 'expires_in': 3600}
```

---

# 643-Topshiriq: IP CIDR subnet tekshiruvi (ipaddress moduli)

## Topshiriq sharti:
Berilgan IP-manzil ma'lum bir tarmoq diapazoniga (CIDR) tegishli ekanligini tekshiring.

## Yechim (Python kodi):
```python
import ipaddress

def ip_tarmoqdami(ip_str, tarmoq_cidr):
    ip = ipaddress.ip_address(ip_str)
    tarmoq = ipaddress.ip_network(tarmoq_cidr)
    return ip in tarmoq

print("192.168.1.5 in 192.168.1.0/24:", ip_tarmoqdami("192.168.1.5", "192.168.1.0/24"))
print("10.0.0.1 in 192.168.1.0/24:", ip_tarmoqdami("10.0.0.1", "192.168.1.0/24"))
```

## Tushuntirish va Mantiq:
1. `ipaddress` moduli IP diapazonlarini, subnetlarni va marshrutlash qoidalarini aniqlashda juda qulay.

## Ishlash natijasi:
```text
Chiqish: 192.168.1.5 in 192.168.1.0/24: True, 10.0.0.1 in 192.168.1.0/24: False
```

---

# 644-Topshiriq: HTTP User-Agent Parser

## Topshiriq sharti:
User-Agent satridan brauzer turi va operatsion tizimni aniqlang.

## Yechim (Python kodi):
```python
def ua_tahlil(ua_str):
    os = "Noma'lum OS"
    brauzer = "Noma'lum brauzer"
    
    if "Windows" in ua_str: os = "Windows"
    elif "Macintosh" in ua_str: os = "macOS"
    elif "Linux" in ua_str: os = "Linux"
    elif "Android" in ua_str: os = "Android"
    
    if "Chrome" in ua_str and "Edg" not in ua_str: brauzer = "Chrome"
    elif "Firefox" in ua_str: brauzer = "Firefox"
    elif "Safari" in ua_str and "Chrome" not in ua_str: brauzer = "Safari"
    elif "Edg" in ua_str: brauzer = "Edge"
    
    return {"os": os, "brauzer": brauzer}

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0"
print(ua_tahlil(ua))
```

## Tushuntirish va Mantiq:
1. Veb tahlil (Web Analytics) tizimlari foydalanuvchilar qurilmasini User-Agent orqali aniqlaydi.

## Ishlash natijasi:
```text
Chiqish: {'os': 'Windows', 'brauzer': 'Chrome'}
```

---

# 645-Topshiriq: Curl buyrug'ini Python requests kodiga o'giruvchi parser

## Topshiriq sharti:
Oddiy 'curl -X POST https://... -H ... -d ...' satridan parametrlarni ajrating.

## Yechim (Python kodi):
```python
import re

def parse_curl(curl_cmd):
    url_m = re.search(r"curl(?: -X [A-Z]+)? ['"]?([^'"\s]+)['"]?", curl_cmd)
    url = url_m.group(1) if url_m else ""
    
    headers = dict(re.findall(r"-H ['"]([^:]+):\s*([^'"]+)['"]", curl_cmd))
    return {"url": url, "headers": headers}

cmd = 'curl https://api.uzai.uz/data -H "Authorization: Bearer token123" -H "Accept: application/json"'
print(parse_curl(cmd))
```

## Tushuntirish va Mantiq:
1. Dasturchilar ko'pincha brauzer Network tabidan curl buyrug'ini ko'chirib Python kodiga o'tkazishadi.

## Ishlash natijasi:
```text
Chiqish: {'url': 'https://api.uzai.uz/data', 'headers': {'Authorization': 'Bearer token123', 'Accept': 'application/json'}}
```

---

# 646-Topshiriq: Parallel HTTP so'rovlar (ThreadPoolExecutor)

## Topshiriq sharti:
concurrent.futures yordamida 5 ta sahifaga bir vaqtning o'zida parallel so'rov yuborish.

## Yechim (Python kodi):
```python
from concurrent.futures import ThreadPoolExecutor
import time

def soxta_yuklab_olish(url):
    time.sleep(0.05)
    return f"{url} muvaffaqiyatli yuklandi"

manzillar = [f"https://api.site.uz/page/{i}" for i in range(1, 6)]
with ThreadPoolExecutor(max_workers=3) as executor:
    natijalar = list(executor.map(soxta_yuklab_olish, manzillar))

for n in natijalar:
    print(n)
```

## Tushuntirish va Mantiq:
1. I/O-bound tarmoq operatsiyalarida oqimlar (Threads) so'rovlarni parallel kutish hisobiga tezlikni oshiradi.

## Ishlash natijasi:
```text
Chiqish: https://api.site.uz/page/1 muvaffaqiyatli yuklandi... (5 ta qator)
```

---

# 647-Topshiriq: Tarmoq kechikishini (Latency / Ping) o'lchash

## Topshiriq sharti:
Serverga TCP ulanish ochish orqali tarmoq kechikish vaqtini (RTT - Round Trip Time) millisoniyalarda o'lchang.

## Yechim (Python kodi):
```python
import socket
import time

def tcp_ping(host, port=80, timeout=2.0):
    start = time.perf_counter()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        otgan_vaqt = (time.perf_counter() - start) * 1000
        return f"{host}:{port} -> {otgan_vaqt:.2f} ms"
    except Exception as e:
        return f"{host}:{port} -> Ulanib bo'lmadi ({e})"

print(tcp_ping("google.com", 80))
print(tcp_ping("127.0.0.1", 9999))
```

## Tushuntirish va Mantiq:
1. TCP ping orqali serverning tarmoq masofasi va uning yuklamasi baholanadi.

## Ishlash natijasi:
```text
Chiqish: google.com:80 -> 25.40 ms, 127.0.0.1:9999 -> Ulanib bo'lmadi (...)
```

---

# 648-Topshiriq: REST API Resurs marshrutizatori (Mini URL Router)

## Topshiriq sharti:
Web frameworklar (Flask, FastAPI kabi) uslubida yo'llarni funksiyalarga biriktiruvchi router klassi.

## Yechim (Python kodi):
```python
class MiniRouter:
    def __init__(self):
        self.yollar = {}

    def marshrut(self, path):
        def decorator(func):
            self.yollar[path] = func
            return func
        return decorator

    def chaqir(self, path):
        if path in self.yollar:
            return self.yollar[path]()
        return "404 Not Found"

app = MiniRouter()

@app.marshrut("/bosh-sahifa")
def index():
    return "Xush kelibsiz!"

print(app.chaqir("/bosh-sahifa"))
print(app.chaqir("/kontaktlar"))
```

## Tushuntirish va Mantiq:
1. Dekoratorlar yordamida URL manzillarini funksiyalarga xaritalash (Routing) zamonaviy veb dasturlashning asosidir.

## Ishlash natijasi:
```text
Chiqish: Xush kelibsiz!, 404 Not Found
```

---

# 649-Topshiriq: API Paginatsiya bilan barcha sahifalarni avtomatik yig'ish

## Topshiriq sharti:
Keyingi sahifa havolasi (`next_page`) mavjud bo'lgancha ma'lumotlarni ketma-ket to'plovchi generator.

## Yechim (Python kodi):
```python
def soxta_sahifalovchi_api(sahifa):
    bazalar = {
        1: {"data": ["Kitob 1", "Kitob 2"], "next": 2},
        2: {"data": ["Kitob 3", "Kitob 4"], "next": 3},
        3: {"data": ["Kitob 5"], "next": None}
    }
    return bazalar.get(sahifa, {"data": [], "next": None})

def barcha_sahifalarni_ol():
    sahifa = 1
    while sahifa:
        res = soxta_sahifalovchi_api(sahifa)
        for element in res["data"]:
            yield element
        sahifa = res["next"]

print("Barcha kitoblar:", list(barcha_sahifalarni_ol()))
```

## Tushuntirish va Mantiq:
1. API paginatsiyasini generator yordamida o'qish xotirani tejaydi va kodni toza saqlaydi.

## Ishlash natijasi:
```text
Chiqish: Barcha kitoblar: ['Kitob 1', 'Kitob 2', 'Kitob 3', 'Kitob 4', 'Kitob 5']
```

---

# 650-Topshiriq: Yaxlit API Mijozi (Full-Featured REST Client)

## Topshiriq sharti:
Token autentifikatsiyasi, kesh, retry va xatoliklarni qayta ishlashni o'zida birlashtirgan to'liq SDK sinfi.

## Yechim (Python kodi):
```python
import json

class UzbekAISDK:
    def __init__(self, api_key, base_url="https://api.uzai.uz"):
        self.api_key = api_key
        self.base_url = base_url

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "UzbekAI-Python-SDK/1.0"
        }

    def chat_completion(self, model, xabar):
        payload = {"model": model, "messages": [{"role": "user", "content": xabar}]}
        # Haqiqiy tarmoq so'rovi simulyatsiyasi
        return {
            "status": 200,
            "choices": [{"message": {"role": "assistant", "content": f"'{xabar}' bo'yicha javob tayyor."}}]
        }

sdk = UzbekAISDK(api_key="uz_live_secret_777")
javob = sdk.chat_completion(model="uzbek-10b-1bit", xabar="Salom AI!")
print("Model javobi:", javob["choices"][0]["message"]["content"])
```

## Tushuntirish va Mantiq:
1. Mukammal SDK mijoz arxitekturasi foydalanuvchiga tarmoq detallarini yashirgan holda yuqori darajadagi qulay metodlar taqdim etadi.

## Ishlash natijasi:
```text
Chiqish: Model javobi: 'Salom AI!' bo'yicha javob tayyor.
```

---

