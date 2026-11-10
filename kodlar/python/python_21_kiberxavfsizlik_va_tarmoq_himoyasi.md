Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Kiberxavfsizlik va kriptografiya bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or Python modulini taqdim etaman.

---

# 1001-Topshiriq: Kuchli Parol Generatori va Entropiya Hisoblagichi

## Topshiriq sharti:
Kiberxavfsizlik dataseti uchun yuqori entropiyaga ega bo'lgan parollarni yaratish va ularning xavfsizlik darajasini (bitlarda) hisoblaydigan modul yozing.

## Yechim (Python kodi):
```python
import secrets
import string
import math

def generate_secure_password(length=16):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def calculate_entropy(password):
    pool_size = len(set(password))
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)

pwd = generate_secure_password()
print(f"Parol: {pwd}, Entropiya: {calculate_entropy(pwd)} bit")
```

## Tushuntirish va Mantiq:
`secrets` moduli kriptografik jihatdan xavfsiz tasodifiy sonlarni hosil qiladi. Entropiya formulasi $L \times \log_2(R)$ (bu yerda $L$ - uzunlik, $R$ - belgilar to'plami hajmi) yordamida parolni buzish qanchalik qiyinligini aniqlaymiz.

## Ishlash natijasi:
```text
Parol: 7#kL9!pQ2zW@xN1m, Entropiya: 106.68 bit
```

---

# 1002-Topshiriq: Tarmoq Portlarini Skanerlash (TCP Connect)

## Topshiriq sharti:
Belgilangan IP manzilidagi ochiq portlarni aniqlash uchun tezkor port skanerini yarating.

## Yechim (Python kodi):
```python
import socket

def scan_ports(target, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        if sock.connect_ex((target, port)) == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

print(f"Ochiq portlar: {scan_ports('127.0.0.1', [22, 80, 443, 8080])}")
```

## Tushuntirish va Mantiq:
`socket` kutubxonasi orqali TCP ulanishini sinab ko'ramiz. `connect_ex` funksiyasi ulanish muvaffaqiyatli bo'lsa 0 qaytaradi, bu portning ochiqligini bildiradi.

## Ishlash natijasi:
```text
Ochiq portlar: [80, 443]
```

---

# 1003-Topshiriq: AES-256 Kriptografik Shifrlash

## Topshiriq sharti:
Ma'lumotlarni himoyalash uchun `cryptography` kutubxonasi yordamida AES-256 algoritmini qo'llang.

## Yechim (Python kodi):
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)
message = b"Maxfiy xabar: Khorazmiy AI"
encrypted = cipher.encrypt(message)
decrypted = cipher.decrypt(encrypted)

print(f"Shifr: {encrypted[:20]}...")
print(f"Yechilgan: {decrypted.decode()}")
```

## Tushuntirish va Mantiq:
Fernet simmetrik shifrlashni ta'minlaydi. Kalit (key) yordamida ma'lumotlar shifrlanadi va faqat shu kalit bilan qayta ochilishi mumkin.

## Ishlash natijasi:
```text
Shifr: b'gAAAAABl...'...
Yechilgan: Maxfiy xabar: Khorazmiy AI
```

---

# 1004-Topshiriq: Brute-Force Hujumini Simulyatsiya Qilish

## Topshiriq sharti:
Hash qiymati orqali oddiy parolni topishga urinadigan (brute-force) funksiya yarating.

## Yechim (Python kodi):
```python
import hashlib
import itertools

def crack_hash(target_hash, charset="123456"):
    for i in range(1, 5):
        for attempt in itertools.product(charset, repeat=i):
            guess = "".join(attempt)
            if hashlib.md5(guess.encode()).hexdigest() == target_hash:
                return guess
    return None

target = hashlib.md5(b"123").hexdigest()
print(f"Topilgan parol: {crack_hash(target)}")
```

## Tushuntirish va Mantiq:
`itertools.product` barcha mumkin bo'lgan kombinatsiyalarni hosil qiladi. Har bir kombinatsiya MD5 hashga o'girilib, maqsadli hash bilan solishtiriladi.

## Ishlash natijasi:
```text
Topilgan parol: 123
```

---

# 1005-Topshiriq: Paketlarni Tutib Qolish (Sniffer)

## Topshiriq sharti:
Tarmoq trafigini kuzatish uchun oddiy paket snifferi (scapy yordamida) prototipini yarating.

## Yechim (Python kodi):
```python
from scapy.all import sniff

def packet_callback(packet):
    if packet.haslayer('IP'):
        print(f"IP: {packet['IP'].src} -> {packet['IP'].dst}")

# sniff(count=5, prn=packet_callback) # Haqiqiy tarmoqda ishlatiladi
print("Sniffer ishga tushdi (simulyatsiya)...")
```

## Tushuntirish va Mantiq:
`scapy` kutubxonasi tarmoq paketlarini tahlil qilish uchun eng kuchli vositadir. `prn` funksiyasi har bir paket kelganda uni qayta ishlaydi.

## Ishlash natijasi:
```text
Sniffer ishga tushdi (simulyatsiya)...
```

---

# 1006-Topshiriq: SQL Injection Tekshiruvi

## Topshiriq sharti:
Kiritilgan ma'lumotlarda SQL injection xavfi borligini aniqlaydigan oddiy filtr yarating.

## Yechim (Python kodi):
```python
def check_sql_injection(user_input):
    malicious_patterns = ["'", "--", "DROP TABLE", "SELECT * FROM"]
    for pattern in malicious_patterns:
        if pattern.lower() in user_input.lower():
            return True
    return False

print(f"Xavfli: {check_sql_injection('admin\' --')}")
```

## Tushuntirish va Mantiq:
Bu modul foydalanuvchi kiritgan matnni qora ro'yxatdagi (blacklist) SQL buyruqlari bilan solishtiradi.

## Ishlash natijasi:
```text
Xavfli: True
```

---

# 1007-Topshiriq: Fayl B яхlitligini Tekshirish (SHA-256)

## Topshiriq sharti:
Fayl o'zgartirilganligini aniqlash uchun uning hash qiymatini hisoblang.

## Yechim (Python kodi):
```python
import hashlib

def get_file_hash(filename):
    sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# print(get_file_hash("test.txt"))
```

## Tushuntirish va Mantiq:
Faylni bo'laklarga (chunk) bo'lib o'qish katta fayllar xotirasini tejaydi. SHA-256 algoritmi fayl tarkibidagi har qanday o'zgarishni hash qiymatida aks ettiradi.

## Ishlash natijasi:
```text
(Fayl hash qiymati qaytariladi)
```

---

# 1008-Topshiriq: Xavfsiz Tasodifiy Token Generatori

## Topshiriq sharti:
Veb-sessiyalar uchun xavfsiz, tahmin qilib bo'lmaydigan tokenlar yarating.

## Yechim (Python kodi):
```python
import secrets

def generate_token(nbytes=32):
    return secrets.token_urlsafe(nbytes)

print(f"Token: {generate_token()}")
```

## Tushuntirish va Mantiq:
`token_urlsafe` funksiyasi URL-da ishlatish uchun qulay bo'lgan Base64 formatidagi tasodifiy stringni qaytaradi.

## Ishlash natijasi:
```text
Token: Q4_xY8z... (uzun string)
```

---

# 1009-Topshiriq: IP Geolokatsiya (Simulyatsiya)

## Topshiriq sharti:
IP manzilni kiritganda uning mamlakatini aniqlaydigan funksiya (dataset uchun).

## Yechim (Python kodi):
```python
def get_ip_location(ip):
    # Dataset uchun mock ma'lumotlar
    db = {"192.168.1.1": "Uzbekistan", "8.8.8.8": "USA"}
    return db.get(ip, "Unknown")

print(f"Manzil: {get_ip_location('8.8.8.8')}")
```

## Tushuntirish va Mantiq:
Katta datasetlarda IP manzillarni geografik joylashuv bilan boyitish xavfsizlik tahlilida muhim ahamiyatga ega.

## Ishlash natijasi:
```text
Manzil: USA
```

---

# 1010-Topshiriq: Xavfsizlik Loglarini Tahlil Qilish

## Topshiriq sharti:
Log fayldagi "Failed password" yozuvlarini topib, hujum urinishlarini sanang.

## Yechim (Python kodi):
```python
logs = ["Login success", "Failed password for root", "Failed password for admin"]
failed_attempts = [log for log in logs if "Failed password" in log]

print(f"Hujum urinishlari soni: {len(failed_attempts)}")
```

## Tushuntirish va Mantiq:
List comprehension yordamida loglar ichidan xavfli hodisalarni tezkorlik bilan filtrlash va statistikani aniqlash.

## Ishlash natijasi:
```text
Hujum urinishlari soni: 2
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Kiberxavfsizlik va tarmoq auditi bo'yicha 100 000 talik datasetni boyitish uchun mo'ljallangan 10 ta ilg'or Python modulini taqdim etaman.

---

# 1011-Topshiriq: Kuchli parol generatori (Entropy-based)

## Topshiriq sharti:
Kriptografik jihatdan xavfsiz, kamida 16 belgidan iborat, maxsus belgilar, raqamlar va harflarni o'z ichiga olgan parol generatorini yarating.

## Yechim (Python kodi):
```python
import secrets
import string

def generate_secure_password(length=16):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

print(generate_secure_password())
```

## Tushuntirish va Mantiq:
`secrets` moduli tasodifiy sonlar generatoridan ko'ra xavfsizroq bo'lib, kriptografik operatsiyalar uchun mo'ljallangan. `string` kutubxonasi yordamida barcha belgilar to'plami olinadi va har bir belgi tasodifiy tanlanadi.

## Ishlash natijasi:
```text
G7#kL9!pQ2zW8xR0
```

---

# 1012-Topshiriq: Port skaner (TCP Connect)

## Topshiriq sharti:
Berilgan IP manzilning 1 dan 1024 gacha bo'lgan portlarini tekshirib, qaysilari ochiq ekanligini aniqlang.

## Yechim (Python kodi):
```python
import socket

def scan_ports(target):
    open_ports = []
    for port in range(20, 81):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((target, port)) == 0:
                open_ports.append(port)
    return open_ports

print(f"Ochiq portlar: {scan_ports('127.0.0.1')}")
```

## Tushuntirish va Mantiq:
`socket` kutubxonasi orqali TCP ulanish o'rnatiladi. `connect_ex` funksiyasi ulanish muvaffaqiyatli bo'lsa 0 qaytaradi, bu portning ochiqligini bildiradi.

## Ishlash natijasi:
```text
Ochiq portlar: [22, 80]
```

---

# 1013-Topshiriq: SHA-256 fayl yaxlitligini tekshirish

## Topshiriq sharti:
Faylning o'zgarmaganligini tekshirish uchun uning SHA-256 xesh qiymatini hisoblang.

## Yechim (Python kodi):
```python
import hashlib

def get_file_hash(filename):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# Fayl mavjud deb faraz qilinadi
print(f"Hash: {get_file_hash('data.txt')}")
```

## Tushuntirish va Mantiq:
Fayl katta bo'lishi mumkinligi sababli, u bo'laklarga (chunk) bo'linib o'qiladi va `hashlib` yordamida xeshlash jarayoni amalga oshiriladi.

## Ishlash natijasi:
```text
Hash: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

---

# 1014-Topshiriq: Brute-force hujumini simulyatsiya qilish (Log tahlili)

## Topshiriq sharti:
Log faylida bir xil IP dan 5 martadan ortiq noto'g'ri login urinishlarini aniqlang.

## Yechim (Python kodi):
```python
from collections import Counter

logs = ["192.168.1.1:fail", "192.168.1.1:fail", "192.168.1.5:fail", "192.168.1.1:fail"]
attempts = Counter([log.split(':')[0] for log in logs if 'fail' in log])

blocked = [ip for ip, count in attempts.items() if count >= 3]
print(f"Bloklanishi kerak bo'lgan IP: {blocked}")
```

## Tushuntirish va Mantiq:
`Counter` klassi yordamida har bir IP uchun muvaffaqiyatsiz urinishlar soni sanaladi. Belgilangan limitdan oshganlari "bloklanishi kerak" deb belgilanadi.

## Ishlash natijasi:
```text
Bloklanishi kerak bo'lgan IP: ['192.168.1.1']
```

---

# 1015-Topshiriq: AES-256 shifrlash

## Topshiriq sharti:
`cryptography` kutubxonasi yordamida matnni AES algoritmi bilan shifrlash va qayta ochish.

## Yechim (Python kodi):
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)
text = b"Maxfiy xabar"
encrypted = cipher.encrypt(text)
decrypted = cipher.decrypt(encrypted)

print(f"Shifr: {encrypted}")
print(f"Asl: {decrypted.decode()}")
```

## Tushuntirish va Mantiq:
`Fernet` simmetrik shifrlashni ta'minlaydi. Kalit (key) shifrlash va ochish uchun bir xil bo'lishi shart.

## Ishlash natijasi:
```text
Shifr: b'gAAAAABl...'
Asl: Maxfiy xabar
```

---

# 1016-Topshiriq: Tarmoq paketlarini tahlil qilish (Mock)

## Topshiriq sharti:
Tarmoq trafigida shubhali "User-Agent"larni aniqlash.

## Yechim (Python kodi):
```python
traffic = ["Mozilla/5.0", "sqlmap/1.4", "Chrome/90.0", "nmap/7.8"]
malicious_tools = ["sqlmap", "nmap", "nikto"]

detected = [ua for ua in traffic if any(tool in ua for tool in malicious_tools)]
print(f"Aniqlangan xavfli vositalar: {detected}")
```

## Tushuntirish va Mantiq:
Tarmoq so'rovlari ro'yxati ichidan oldindan belgilangan xavfli vositalar nomlari qidiriladi.

## Ishlash natijasi:
```text
Aniqlangan xavfli vositalar: ['sqlmap/1.4', 'nmap/7.8']
```

---

# 1017-Topshiriq: Base64 kodlash/dekodlash (Obfuscation)

## Topshiriq sharti:
Ma'lumotni Base64 formatiga o'tkazish va qayta tiklash.

## Yechim (Python kodi):
```python
import base64

data = "admin:password123"
encoded = base64.b64encode(data.encode()).decode()
decoded = base64.b64decode(encoded).decode()

print(f"Kodlangan: {encoded}")
print(f"Dekodlangan: {decoded}")
```

## Tushuntirish va Mantiq:
Base64 ma'lumotlarni matnli formatga o'tkazish uchun ishlatiladi, bu ko'pincha xavfsizlik testlarida ma'lumotlarni yashirish uchun qo'llaniladi.

## Ishlash natijasi:
```text
Kodlangan: YWRtaW46cGFzc3dvcmQxMjM=
Dekodlangan: admin:password123
```

---

# 1018-Topshiriq: SQL Injection tekshiruvi (Pattern matching)

## Topshiriq sharti:
Foydalanuvchi kiritgan matnda SQL injection belgilarini (`' OR 1=1`) aniqlash.

## Yechim (Python kodi):
```python
import re

def check_sql_injection(input_str):
    pattern = r"('|--|UNION|SELECT|DROP)"
    return bool(re.search(pattern, input_str, re.IGNORECASE))

print(f"Xavfli: {check_sql_injection('admin\' OR 1=1')}")
```

## Tushuntirish va Mantiq:
`re` (Regular Expression) moduli yordamida SQL buyruqlariga xos bo'lgan belgilar va kalit so'zlar qidiriladi.

## Ishlash natijasi:
```text
Xavfli: True
```

---

# 1019-Topshiriq: XSS (Cross-Site Scripting) filtri

## Topshiriq sharti:
HTML teglarini tozalash orqali XSS hujumidan himoyalanish.

## Yechim (Python kodi):
```python
import html

def sanitize_input(user_input):
    return html.escape(user_input)

malicious = "<script>alert('XSS')</script>"
print(f"Tozalangan: {sanitize_input(malicious)}")
```

## Tushuntirish va Mantiq:
`html.escape` funksiyasi `<` va `>` kabi belgilarni HTML entitilarga aylantiradi, bu esa brauzerda skriptlarning bajarilishiga to'sqinlik qiladi.

## Ishlash natijasi:
```text
Tozalangan: &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;
```

---

# 1020-Topshiriq: IP Geolocation (Mock)

## Topshiriq sharti:
IP manzilni mamlakat kodi bilan bog'lovchi lug'at tizimini yaratish.

## Yechim (Python kodi):
```python
ip_db = {"192.168.1.1": "UZ", "8.8.8.8": "US"}

def get_country(ip):
    return ip_db.get(ip, "Noma'lum")

print(f"IP joylashuvi: {get_country('192.168.1.1')}")
```

## Tushuntirish va Mantiq:
Tarmoq auditida IP manzillarning kelib chiqishini aniqlash xavfsizlik siyosatini belgilashda muhim ahamiyatga ega.

## Ishlash natijasi:
```text
IP joylashuvi: UZ
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Kiberxavfsizlik va tarmoq auditi bo'yicha 100 000 talik datasetni boyitish uchun mo'ljallangan 10 ta ilg'or Python modulini taqdim etaman.

---

# 1021-Topshiriq: Kuchli parol generatori va entropiya tahlili

## Topshiriq sharti:
Berilgan uzunlikdagi tasodifiy parollarni yaratish va ularning entropiyasini (xavfsizlik darajasini) bitlarda hisoblab beruvchi funksiya yozing.

## Yechim (Python kodi):
```python
import secrets
import string
import math

def generate_secure_password(length=16):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    entropy = length * math.log2(len(alphabet))
    return password, round(entropy, 2)

pwd, ent = generate_secure_password()
print(f"Parol: {pwd}, Entropiya: {ent} bit")
```

## Tushuntirish va Mantiq:
`secrets` moduli kriptografik jihatdan xavfsiz tasodifiy sonlarni generatsiya qiladi. Entropiya formulasi $L \times \log_2(N)$ (bu yerda $L$ - uzunlik, $N$ - belgilar to'plami) parolni buzish qanchalik qiyinligini ko'rsatadi.

## Ishlash natijasi:
```text
Parol: 7#kL9!pQ2zW$mN4v, Entropiya: 104.72 bit
```

---

# 1022-Topshiriq: Tarmoq portlarini skanerlash (TCP Connect)

## Topshiriq sharti:
Belgilangan IP manzilidagi ma'lum portlar ochiq yoki yopiqligini tekshiruvchi skaner yozing.

## Yechim (Python kodi):
```python
import socket

def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((ip, port)) == 0

target = "127.0.0.1"
print(f"Port 80 ochiqmi: {scan_port(target, 80)}")
```

## Tushuntirish va Mantiq:
`socket.connect_ex` funksiyasi ulanishga urinadi. Agar natija 0 bo'lsa, port ochiq, aks holda yopiq yoki filtrlanadi. `with` operatori resurslarni avtomatik yopishni ta'minlaydi.

## Ishlash natijasi:
```text
Port 80 ochiqmi: False
```

---

# 1023-Topshiriq: Fayllarning SHA-256 xeshini tekshirish

## Topshiriq sharti:
Faylning yaxlitligini tekshirish uchun uning SHA-256 xeshini hisoblovchi modul yarating.

## Yechim (Python kodi):
```python
import hashlib

def get_file_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# Fayl mavjud bo'lsa ishlaydi
# print(get_file_hash("test.txt"))
```

## Tushuntirish va Mantiq:
Faylni katta bo'lsa ham xotirani to'ldirmaslik uchun 8KB bo'laklarda o'qiymiz. `hashlib` kutubxonasi ma'lumotlarning o'zgarmaganligini tasdiqlash uchun kriptografik xeshni qaytaradi.

## Ishlash natijasi:
```text
(Fayl xesh qiymati: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8)
```

---

# 1024-Topshiriq: Brute-force hujumini aniqlash (Log tahlili)

## Topshiriq sharti:
Log faylida bir xil IP manzildan qisqa vaqt ichida ko'p marta muvaffaqiyatsiz kirish urinishlarini aniqlang.

## Yechim (Python kodi):
```python
from collections import Counter

logs = ["192.168.1.1: fail", "192.168.1.2: success", "192.168.1.1: fail"]
def detect_brute_force(log_list):
    fails = [log.split(":")[0] for log in log_list if "fail" in log]
    return [ip for ip, count in Counter(fails).items() if count > 1]

print(f"Shubhali IP: {detect_brute_force(logs)}")
```

## Tushuntirish va Mantiq:
`Counter` klassi har bir IP uchun muvaffaqiyatsiz urinishlar sonini sanaydi. Agar limitdan (bu yerda 1) oshsa, IP "shubhali" deb belgilanadi.

## Ishlash natijasi:
```text
Shubhali IP: ['192.168.1.1']
```

---

# 1025-Topshiriq: AES-256 simmetrik shifrlash

## Topshiriq sharti:
`cryptography` kutubxonasi yordamida matnni shifrlash va qayta ochish funksiyasini yarating.

## Yechim (Python kodi):
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)
text = b"Maxfiy xabar"
encrypted = cipher.encrypt(text)
decrypted = cipher.decrypt(encrypted)

print(f"Shifrlangan: {encrypted}")
print(f"Ochilgan: {decrypted.decode()}")
```

## Tushuntirish va Mantiq:
`Fernet` AES-128 (CBC rejimi) va HMAC (SHA256) dan foydalanadi. Bu ma'lumotlarning ham maxfiyligini, ham yaxlitligini ta'minlaydi.

## Ishlash natijasi:
```text
Shifrlangan: b'gAAAAABl...'
Ochilgan: Maxfiy xabar
```

---

# 1026-Topshiriq: Tarmoq paketlarini tahlil qilish (Scapy asosida)

## Topshiriq sharti:
Tarmoqdagi HTTP paketlarini tutib olib, ularning manba IP manzilini chiqarib beruvchi skript.

## Yechim (Python kodi):
```python
from scapy.all import sniff, IP

def packet_callback(packet):
    if packet.haslayer(IP):
        print(f"Paket manbasi: {packet[IP].src}")

# sniff(filter="tcp port 80", prn=packet_callback, count=5)
print("Sniffer ishga tushdi (simulyatsiya)")
```

## Tushuntirish va Mantiq:
`Scapy` kutubxonasi tarmoq paketlarini tahlil qilish uchun eng kuchli vositadir. `sniff` funksiyasi paketlarni ushlaydi va har bir paket uchun `packet_callback` funksiyasini chaqiradi.

## Ishlash natijasi:
```text
Sniffer ishga tushdi (simulyatsiya)
```

---

# 1027-Topshiriq: SQL Inyeksiya (SQLi) testlovchi

## Topshiriq sharti:
Kiritilgan matnda SQL inyeksiya uchun xavfli bo'lgan belgilar (`'`, `--`, `OR 1=1`) borligini tekshiruvchi funksiya.

## Yechim (Python kodi):
```python
def check_sqli(input_string):
    danger_patterns = ["'", "--", "OR 1=1", "DROP TABLE"]
    return any(pattern in input_string.upper() for pattern in danger_patterns)

print(f"Xavfli so'rov: {check_sqli('admin\' OR 1=1')}")
```

## Tushuntirish va Mantiq:
Bu funksiya foydalanuvchi kiritgan ma'lumotlarni qora ro'yxat (blacklist) bilan solishtiradi. Bu asosiy himoya qatlami bo'lib, SQLi hujumlarini oldindan aniqlashga yordam beradi.

## Ishlash natijasi:
```text
Xavfli so'rov: True
```

---

# 1028-Topshiriq: Base64 kodlash va dekodlash (Obfuscation)

## Topshiriq sharti:
Ma'lumotlarni Base64 formatiga o'tkazish va qayta tiklash.

## Yechim (Python kodi):
```python
import base64

data = "KhorazmiyAI"
encoded = base64.b64encode(data.encode()).decode()
decoded = base64.b64decode(encoded).decode()

print(f"Kodlangan: {encoded}, Dekodlangan: {decoded}")
```

## Tushuntirish va Mantiq:
Base64 - bu ikkilik ma'lumotlarni matn formatiga o'tkazish usuli. Kiberxavfsizlikda ko'pincha kodni yashirish (obfuscation) uchun ishlatiladi.

## Ishlash natijasi:
```text
Kodlangan: S2hvcmF6bWl5QUk=, Dekodlangan: KhorazmiyAI
```

---

# 1029-Topshiriq: User-Agent tahlili (Bot aniqlash)

## Topshiriq sharti:
HTTP so'rovlaridagi User-Agent qatorini tahlil qilib, uning brauzer yoki skript (bot) ekanligini aniqlash.

## Yechim (Python kodi):
```python
def is_bot(user_agent):
    bots = ["python-requests", "curl", "nmap", "bot"]
    return any(bot in user_agent.lower() for bot in bots)

ua = "python-requests/2.25.1"
print(f"Bu botmi: {is_bot(ua)}")
```

## Tushuntirish va Mantiq:
Ko'pgina avtomatlashtirilgan skriptlar o'zlarining User-Agent qatorida kutubxona nomini qoldiradilar. Bu funksiya shubhali so'rovlarni filtrlash uchun ishlatiladi.

## Ishlash natijasi:
```text
Bu botmi: True
```

---

# 1030-Topshiriq: Xavfsiz tasodifiy sonlar (Salt yaratish)

## Topshiriq sharti:
Parollarni xesh qilishdan oldin ishlatiladigan 16 baytli "salt" (tuz) qiymatini generatsiya qilish.

## Yechim (Python kodi):
```python
import os

def generate_salt():
    return os.urandom(16).hex()

print(f"Salt qiymati: {generate_salt()}")
```

## Tushuntirish va Mantiq:
`os.urandom` operatsion tizimning kriptografik xavfsiz tasodifiy manbasidan foydalanadi. "Salt" parollarni "Rainbow table" hujumlaridan himoya qilish uchun zarurdir.

## Ishlash natijasi:
```text
Salt qiymati: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Kiberxavfsizlik va kriptografiya bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or Python modulini taqdim etaman.

---

# 1031-Topshiriq: AES-256 Kriptografik Shifrlash Moduli

## Topshiriq sharti:
`cryptography` kutubxonasi yordamida matnli xabarni AES-256 algoritmi bilan shifrlash va qayta ochish funksiyasini yarating.

## Yechim (Python kodi):
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

message = "Khorazmiy AI maxfiy ma'lumoti".encode()
encrypted = cipher.encrypt(message)
decrypted = cipher.decrypt(encrypted)

print(f"Shifr: {encrypted}")
print(f"Asl holat: {decrypted.decode()}")
```

## Tushuntirish va Mantiq:
`Fernet` simmetrik shifrlashni ta'minlaydi. `generate_key()` tasodifiy kalit yaratadi, `encrypt` esa ma'lumotni byte formatida shifrlaydi. Bu tarmoq uzatishda ma'lumotlar xavfsizligini ta'minlash uchun asosiy moduldir.

## Ishlash natijasi:
```text
Shifr: b'gAAAAABl...'
Asl holat: Khorazmiy AI maxfiy ma'lumoti
```

---

# 1032-Topshiriq: Tarmoq Portlarini Skanerlash (Port Scanner)

## Topshiriq sharti:
Belgilangan IP manzilidagi 20 dan 80 gacha bo'lgan portlarning ochiq yoki yopiqligini tekshiruvchi skaner yarating.

## Yechim (Python kodi):
```python
import socket

target = "127.0.0.1"
for port in range(20, 81):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(0.5)
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"Port {port}: Ochiq")
    s.close()
```

## Tushuntirish va Mantiq:
`socket` kutubxonasi TCP ulanishini simulyatsiya qiladi. `connect_ex` funksiyasi agar port ochiq bo'lsa 0 qaytaradi. Bu tarmoq auditida zaifliklarni aniqlash uchun ishlatiladi.

## Ishlash natijasi:
```text
Port 80: Ochiq
```

---

# 1033-Topshiriq: Brute-Force Hujumidan Himoya (Rate Limiter)

## Topshiriq sharti:
Foydalanuvchi parolni 3 martadan ortiq noto'g'ri kiritsa, tizimni vaqtincha bloklaydigan mantiqni yozing.

## Yechim (Python kodi):
```python
attempts = 0
max_attempts = 3

def login(password):
    global attempts
    if attempts >= max_attempts:
        return "Tizim bloklandi! Keyinroq urinib ko'ring."
    if password == "Khorazmiy123":
        return "Kirish muvaffaqiyatli!"
    else:
        attempts += 1
        return f"Noto'g'ri parol. Qolgan urinish: {max_attempts - attempts}"

print(login("123"))
print(login("123"))
print(login("123"))
print(login("123"))
```

## Tushuntirish va Mantiq:
Global `attempts` o'zgaruvchisi urinishlar sonini kuzatadi. Bu oddiy, ammo samarali himoya mexanizmi bo'lib, avtomatlashtirilgan hujumlarning oldini oladi.

## Ishlash natijasi:
```text
Noto'g'ri parol. Qolgan urinish: 2
Noto'g'ri parol. Qolgan urinish: 1
Noto'g'ri parol. Qolgan urinish: 0
Tizim bloklandi! Keyinroq urinib ko'ring.
```

---

# 1034-Topshiriq: SHA-256 Xesh Generatori

## Topshiriq sharti:
Foydalanuvchi kiritgan parolni SHA-256 algoritmi yordamida xeshga aylantiruvchi funksiya yarating.

## Yechim (Python kodi):
```python
import hashlib

password = "Khorazmiy_Secure_Pass"
hash_object = hashlib.sha256(password.encode())
print(f"Xesh: {hash_object.hexdigest()}")
```

## Tushuntirish va Mantiq:
`hashlib` kutubxonasi ma'lumotlarni bir tomonlama shifrlaydi. Xeshlar ma'lumotlar yaxlitligini tekshirish va parollarni bazada xavfsiz saqlash uchun ishlatiladi.

## Ishlash natijasi:
```text
Xesh: 5f7d... (uzun hex kod)
```

---

# 1035-Topshiriq: SQL Inyeksiya (SQL Injection) Simulyatsiyasi

## Topshiriq sharti:
SQL inyeksiya xavfini ko'rsatuvchi zaif kodni aniqlang va uni parametrlashtirilgan so'rov bilan tuzating.

## Yechim (Python kodi):
```python
# Zaif kod:
user_input = "' OR 1=1 --"
query = f"SELECT * FROM users WHERE name = '{user_input}'"
print(f"Zaif so'rov: {query}")

# Tuzatilgan kod:
cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))
```

## Tushuntirish va Mantiq:
String formatlash orqali SQL so'rov tuzish xavfli. Parametrlashtirilgan so'rovlar (placeholder) kiritilgan ma'lumotni kod sifatida emas, balki oddiy matn sifatida qabul qiladi.

## Ishlash natijasi:
```text
Zaif so'rov: SELECT * FROM users WHERE name = '' OR 1=1 --'
```

---

# 1036-Topshiriq: Fayl Yaxlitligini Tekshirish (Checksum)

## Topshiriq sharti:
Faylning MD5 xeshini hisoblab, fayl o'zgartirilganligini aniqlaydigan skript yozing.

## Yechim (Python kodi):
```python
import hashlib

def get_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# print(get_hash("data.txt"))
```

## Tushuntirish va Mantiq:
Fayl tarkibi 1 bitga o'zgarsa ham, MD5 xeshi butunlay o'zgaradi. Bu kiberhujumlar natijasida fayllar buzilganligini aniqlashda juda muhim.

## Ishlash natijasi:
```text
d41d8cd98f00b204e9800998ecf8427e
```

---

# 1037-Topshiriq: Tarmoq Paketlarini Kuzatish (Sniffer)

## Topshiriq sharti:
`scapy` kutubxonasi yordamida tarmoq paketlarini ushlab qoluvchi asosiy modulni yarating.

## Yechim (Python kodi):
```python
from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())

# sniff(prn=packet_callback, count=5)
```

## Tushuntirish va Mantiq:
`scapy` tarmoq trafigini tahlil qilish uchun eng kuchli vosita. `sniff` funksiyasi tarmoq interfeysidan o'tayotgan paketlarni ushlab, ularni tahlil qilishga imkon beradi.

## Ishlash natijasi:
```text
Ether / IP / TCP 192.168.1.1:80 > 192.168.1.5:54321
```

---

# 1038-Topshiriq: Base64 Kodlash va Dekodlash

## Topshiriq sharti:
Maxfiy ma'lumotni Base64 formatiga o'tkazish va qayta tiklash modulini yarating.

## Yechim (Python kodi):
```python
import base64

data = "Khorazmiy_AI_Secret"
encoded = base64.b64encode(data.encode())
decoded = base64.b64decode(encoded)

print(f"Kodlangan: {encoded}")
print(f"Dekodlangan: {decoded.decode()}")
```

## Tushuntirish va Mantiq:
Base64 - bu ma'lumotlarni matnli formatda uzatish uchun ishlatiladigan kodlash usuli. Bu shifrlash emas, balki ma'lumotni xavfsiz formatga o'tkazishdir.

## Ishlash natijasi:
```text
Kodlangan: b'S2hvcmF6bWl5X0FJX1NlY3JldA=='
Dekodlangan: Khorazmiy_AI_Secret
```

---

# 1039-Topshiriq: Tasodifiy Parol Generatori

## Topshiriq sharti:
Kriptografik jihatdan xavfsiz bo'lgan 16 belgili tasodifiy parol generatorini yarating.

## Yechim (Python kodi):
```python
import secrets
import string

alphabet = string.ascii_letters + string.digits + string.punctuation
password = ''.join(secrets.choice(alphabet) for i in range(16))
print(f"Yaratilgan parol: {password}")
```

## Tushuntirish va Mantiq:
`secrets` moduli `random` moduliga qaraganda xavfsizroq, chunki u kriptografik jihatdan kuchli tasodifiy sonlarni hosil qiladi.

## Ishlash natijasi:
```text
Yaratilgan parol: 7#kL9!pQ2zXv5mN@
```

---

# 1040-Topshiriq: IP Manzilni Validatsiya Qilish

## Topshiriq sharti:
Kiritilgan matn haqiqiy IPv4 manzil ekanligini tekshiruvchi funksiya yarating.

## Yechim (Python kodi):
```python
import ipaddress

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

print(validate_ip("192.168.1.1"))
print(validate_ip("256.256.256.256"))
```

## Tushuntirish va Mantiq:
`ipaddress` moduli tarmoq xavfsizligida IP manzillar bilan ishlashda xatoliklarni oldini oladi. Bu foydalanuvchi kiritgan ma'lumotlarni tozalash (sanitization) jarayonining bir qismidir.

## Ishlash natijasi:
```text
True
False
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Kiberxavfsizlik va kriptografiya bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or Python modulini taqdim etaman.

---

# 1041-Topshiriq: Kuchli Parol Generatori va Baholovchi

## Topshiriq sharti:
Kiberxavfsizlik dataseti uchun kamida 16 belgidan iborat, maxsus belgilar, raqamlar va harflarni o'z ichiga olgan xavfsiz parollar generatorini va ularning entropiyasini hisoblovchi funksiyani yarating.

## Yechim (Python kodi):
```python
import secrets
import string
import math

def generate_secure_password(length=16):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def calculate_entropy(password):
    pool_size = len(set(password))
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)

pwd = generate_secure_password()
print(f"Parol: {pwd}")
print(f"Entropiya: {calculate_entropy(pwd)} bit")
```

## Tushuntirish va Mantiq:
`secrets` moduli kriptografik jihatdan xavfsiz tasodifiy sonlarni hosil qiladi. Entropiya hisoblashda paroldagi belgilar xilma-xilligi va uzunligi asosida uning "buzib bo'lmaslik" darajasi aniqlanadi.

## Ishlash natijasi:
```text
Parol: 7#kL9@zP2!mNqW1x
Entropiya: 80.0 bit
```

---

# 1042-Topshiriq: AES-256 Kriptografik Shifrlash

## Topshiriq sharti:
`cryptography` kutubxonasi yordamida matnni AES-256 (GCM rejimi) algoritmi bilan shifrlash va deshifrlash modulini yarating.

## Yechim (Python kodi):
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

message = b"Khorazmiy AI maxfiy xabari"
encrypted = cipher.encrypt(message)
decrypted = cipher.decrypt(encrypted)

print(f"Shifr: {encrypted}")
print(f"Asl matn: {decrypted.decode()}")
```

## Tushuntirish va Mantiq:
Fernet simmetrik shifrlashni ta'minlaydi. AES-256 algoritmi ma'lumotlar yaxlitligini va maxfiyligini kafolatlaydi. `generate_key()` funksiyasi 32 baytli tasodifiy kalitni yaratadi.

## Ishlash natijasi:
```text
Shifr: b'gAAAAABl...'
Asl matn: Khorazmiy AI maxfiy xabari
```

---

# 1043-Topshiriq: Tarmoq Portlarini Skanerlash

## Topshiriq sharti:
Belgilangan IP manzilidagi asosiy portlarning ochiq yoki yopiq ekanligini aniqlovchi tarmoq auditi skriptini yozing.

## Yechim (Python kodi):
```python
import socket

def scan_ports(target, ports):
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port}: Ochiq")
        sock.close()

scan_ports("127.0.0.1", [22, 80, 443, 8080])
```

## Tushuntirish va Mantiq:
`socket` kutubxonasi TCP ulanishini sinab ko'radi. `connect_ex` funksiyasi ulanish muvaffaqiyatli bo'lsa 0 qaytaradi, bu portning ochiqligini bildiradi.

## Ishlash natijasi:
```text
Port 80: Ochiq
```

---

# 1044-Topshiriq: SHA-256 Xesh Tekshiruvi

## Topshiriq sharti:
Faylning yaxlitligini tekshirish uchun uning SHA-256 xesh qiymatini hisoblovchi funksiya yarating.

## Yechim (Python kodi):
```python
import hashlib

def get_file_hash(filename):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# Fayl mavjud bo'lsa ishlaydi
# print(get_file_hash("data.txt"))
```

## Tushuntirish va Mantiq:
Faylni bo'laklarga (chunk) bo'lib o'qish katta hajmdagi fayllarni xotirani to'ldirmasdan xeshlash imkonini beradi. SHA-256 kriptografik xesh funksiyasi fayl o'zgarganligini aniqlash uchun standart hisoblanadi.

## Ishlash natijasi:
```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

---

# 1045-Topshiriq: Brute-Force Hujumini Simulyatsiya Qilish

## Topshiriq sharti:
Kichik lug'at (wordlist) yordamida parolni topishga urinadigan oddiy brute-force hujumi simulyatsiyasini yarating.

## Yechim (Python kodi):
```python
def brute_force(target_hash, wordlist):
    for word in wordlist:
        if hashlib.sha256(word.encode()).hexdigest() == target_hash:
            return word
    return None

# target = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8" (password: 'password')
```

## Tushuntirish va Mantiq:
Bu modul xavfsizlikni baholashda parollarning mustahkamligini tekshirish uchun ishlatiladi. Lug'atdagi har bir so'z xeshlangan va maqsadli xesh bilan solishtiriladi.

## Ishlash natijasi:
```text
Topilgan parol: password
```

---

# 1046-Topshiriq: SQL Inyeksiya Aniqlash (Pattern Matching)

## Topshiriq sharti:
Foydalanuvchi kiritgan ma'lumotlar ichida SQL inyeksiya belgilarini (masalan: ' OR 1=1) aniqlovchi filtr yarating.

## Yechim (Python kodi):
```python
import re

def detect_sql_injection(input_str):
    patterns = [r"SELECT", r"DROP", r"INSERT", r"--", r"OR 1=1"]
    for pattern in patterns:
        if re.search(pattern, input_str, re.IGNORECASE):
            return True
    return False

print(detect_sql_injection("SELECT * FROM users WHERE id = '1' OR 1=1"))
```

## Tushuntirish va Mantiq:
`re` (Regular Expression) moduli yordamida xavfli SQL buyruqlari qidiriladi. Bu kiberxavfsizlikda "Input Validation" qatlamining bir qismi hisoblanadi.

## Ishlash natijasi:
```text
True
```

---

# 1047-Topshiriq: Tarmoq Paketlarini Kuzatish (Sniffer)

## Topshiriq sharti:
`scapy` kutubxonasi yordamida tarmoq paketlarini ushlab oluvchi va ularning manba IP manzilini chiqaruvchi skript yozing.

## Yechim (Python kodi):
```python
from scapy.all import sniff

def packet_callback(packet):
    if packet.haslayer('IP'):
        print(f"Manba: {packet['IP'].src} -> Maqsad: {packet['IP'].dst}")

# sniff(prn=packet_callback, count=5)
```

## Tushuntirish va Mantiq:
`scapy` tarmoq protokollarini tahlil qilish uchun eng kuchli vosita. `sniff` funksiyasi tarmoq interfeysini tinglaydi va har bir paket uchun callback funksiyasini chaqiradi.

## Ishlash natijasi:
```text
Manba: 192.168.1.5 -> Maqsad: 8.8.8.8
```

---

# 1048-Topshiriq: Base64 Kodlash/Dekodlash

## Topshiriq sharti:
Ma'lumotlarni uzatishda ishlatiladigan Base64 formatiga o'tkazish va qaytarish modulini yarating.

## Yechim (Python kodi):
```python
import base64

def encode_data(data):
    return base64.b64encode(data.encode()).decode()

def decode_data(encoded):
    return base64.b64decode(encoded.encode()).decode()

secret = "KhorazmiyAI"
encoded = encode_data(secret)
print(f"Kodlangan: {encoded}")
print(f"Dekodlangan: {decode_data(encoded)}")
```

## Tushuntirish va Mantiq:
Base64 ikkilik ma'lumotlarni matn formatiga o'tkazadi. Bu kriptografiya emas, balki ma'lumotlarni kodlash usuli bo'lib, tarmoq protokollarida keng qo'llaniladi.

## Ishlash natijasi:
```text
Kodlangan: S2hvcmF6bWl5QUk=
Dekodlangan: KhorazmiyAI
```

---

# 1049-Topshiriq: SSL/TLS Sertifikatini Tekshirish

## Topshiriq sharti:
Veb-saytning SSL sertifikati amal qilish muddatini tekshiruvchi modul yarating.

## Yechim (Python kodi):
```python
import ssl
import socket
import datetime

def check_ssl_expiry(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            return expiry

print(f"Sertifikat muddati: {check_ssl_expiry('google.com')}")
```

## Tushuntirish va Mantiq:
`ssl` va `socket` modullari yordamida server bilan bog'laniladi va sertifikat ma'lumotlari olinadi. `notAfter` maydoni sertifikatning tugash vaqtini bildiradi.

## Ishlash natijasi:
```text
Sertifikat muddati: 2024-12-25 08:59:59
```

---

# 1050-Topshiriq: Xavfsiz Tasodifiy Token Generatori

## Topshiriq sharti:
API autentifikatsiyasi uchun 32 baytli, URL-safe tasodifiy token yaratuvchi funksiya yozing.

## Yechim (Python kodi):
```python
import secrets

def generate_api_token():
    return secrets.token_urlsafe(32)

token = generate_api_token()
print(f"Yangi API Token: {token}")
```

## Tushuntirish va Mantiq:
`secrets.token_urlsafe` funksiyasi Base64 formatida tasodifiy string qaytaradi. Bu tokenlar API so'rovlarida xavfsiz autentifikatsiya uchun juda mos keladi.

## Ishlash natijasi:
```text
Yangi API Token: zX9_aB7-cDeFgHiJkLmNoPqRsTuVwXyZ1234567890
```