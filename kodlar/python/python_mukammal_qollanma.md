# Python Dasturlash Tili: Mukammal Qo'llanma va Ensiklopediya
## (Noldan Tizimli Arxitektura, Algoritmlar va Sun'iy Intellekt Dvigatellarigacha)

> **Muallif:** O'zbekiston Mustaqil Sun'iy Intellekt Laboratoriyasi  
> **Standart:** Python 3.10 - 3.13+ (Zamonaviy Standartlar)  
> **Maqsad:** O'zbek tilida mukammal, to'liq va jahon andozalariga mos dasturlash qo'llanmasi.

---

## MUNDARIJA

1. [1-Bob: Python Falsafasi, Xotira Modeli va CPython Arxitekturasi](#1-bob)
2. [2-Bob: O'zgaruvchilar, Arifmetika va Xotiradagi Mutability](#2-bob)
3. [3-Bob: Shartlar, Mantiq va Strukturaviy Pattern Matching (`match-case`)](#3-bob)
4. [4-Bob: Tsikllar, Generatorlar va Iteratsiya Protokollari](#4-bob)
5. [5-Bob: Kolleksiyalar: List, Tuple, Dict, Set va collections Moduli](#5-bob)
6. [6-Bob: Funksiyalar, Qamrov Doirasi (LEGB), Closures va Dekoratorlar](#6-bob)
7. [7-Bob: Ob'ektga Yo'naltirilgan Dasturlash (OOP), MRO va Metaprogramming](#7-bob)
8. [8-Bob: Istisnolar, Crash-Proof Arxitektura va Logging](#8-bob)
9. [9-Bob: Fayllar Tizimi, I/O Oqimlari va Baza Amallari (SQLite/ORM)](#9-bob)
10. [10-Bob: Parallelizm: Threading, Multiprocessing va Asinxron Dasturlash (asyncio)](#10-bob)
11. [11-Bob: Regulyar Ifodalar (re) va Matn Muhandisligi (NLP Preprocessing)](#11-bob)
12. [12-Bob: Tarmoq Protokollari, Socket Dasturlash va REST API Arxitekturasi](#12-bob)
13. [13-Bob: Algoritmlar va Ma'lumotlar Tuzilmalari (Big-O dan Dinamik Dasturlashgacha)](#13-bob)
14. [14-Bob: Ilmiy Hisoblash, Chiziqli Algebra va Mashinali O'rganish Poydevori](#14-bob)
15. [15-Bob: Dastur Sifat Nazorati: Testlash (pytest/unittest), Profiling va CI/CD](#15-bob)
16. [16-Bob: Maxsus Bob: 1-Bit LLM va Kvantlangan On-Device Sun'iy Intellekt Dvigatellari](#16-bob)

---

<a name="1-bob"></a>
# 1-Bob: Python Falsafasi, Xotira Modeli va CPython Arxitekturasi

Python — bu yuqori darajadagi, dinamik tiplangan, umumiy maqsadli va interpretatsiya qilinadigan dasturlash tili. U 1991-yilda Gvido van Rossum tomonidan yaratilgan.

### 1.1. Python Falsafasi (Zen of Python)
Python ning asosiy tamoyillari Tim Peters tomonidan quyidagicha ta'riflangan:
* **Chiroyli kod xunuk koddan afzalroqdir.** (Beautiful is better than ugly.)
* **Ochiq-oydin yozilgan kod yashirin koddan afzaldir.** (Explicit is better than implicit.)
* **Oddiy yechim murakkab yechimdan ustundir.** (Simple is better than complex.)
* **O'qilishi oson bo'lishi juda muhim.** (Readability counts.)
* **Xatolar hech qachon jimgina o'tkazib yuborilmasligi kerak.** (Errors should never pass silently.)

### 1.2. CPython Qanday Ishlaydi?
1. **Source Code (`.py`)**: Matnli kod yoziladi.
2. **Kompilyatsiya**: CPython interpreter matnni o'qib, uni sintaktik daraxtga (AST) va undan so'ng bayt-kodga (`.pyc`) aylantiradi.
3. **PVM (Python Virtual Machine)**: Stack-based virtual mashina bo'lib, bayt-kod buyruqlarini (LOAD_CONST, BINARY_OP, STORE_NAME) protsessor buyruqlariga aylantirib ijro etadi.

### 1.3. Global Interpreter Lock (GIL)
CPython ning asosiy xususiyatlaridan biri — GIL dir. Bu o'zaro blokirovka mexanizmi bo'lib, bir vaqtning o'zida faqat bitta mahalliy CPU oqimi (Thread) Python bayt-kodini bajarishini kafolatlaydi. Bu xotiradagi ziddiyatlarning oldini oladi, biroq CPU-intensive vazifalar uchun multiprocessing yoki C-kengaytmalarini talab qiladi.

---

<a name="2-bob"></a>
# 2-Bob: O'zgaruvchilar, Arifmetika va Xotiradagi Mutability

Python da hamma narsa ob'ektdir (Everything is an object).

### 2.1. O'zgaruvchilar va Havolalar (Pointers)
O'zgaruvchi — bu quti emas, balki xotiradagi ob'ektga qaratilgan **yorliq (label)** dir.
```python
a = [1, 2, 3]
b = a  # b yangi ro'yxat yaratmaydi, a bilan bitta manzilga qaraydi
b.append(4)
print(a)  # [1, 2, 3, 4]
```

### 2.2. O'zgaruvchan (Mutable) va O'zgarmas (Immutable) Turlar
* **O'zgarmas (Immutable)**: `int`, `float`, `str`, `tuple`, `frozenset`, `bytes`. Ularning qiymati xotirada o'zgarmaydi; yangi qiymat berilsa, yangi manzil ajratiladi.
* **O'zgaruvchan (Mutable)**: `list`, `dict`, `set`, `bytearray`. Ularning ichki qiymati o'zgarganda xotira manzili (`id()`) bir xil saqlanadi.

---

<a name="3-bob"></a>
# 3-Bob: Shartlar, Mantiq va Strukturaviy Pattern Matching (`match-case`)

Python 3.10 versiyasida kiritilgan `match-case` klassik `switch` dan ancha qudratli bo'lib, ma'lumotlar tuzilmasini tahlil qilish imkonini beradi.

```python
def komandani_bajar(action):
    match action:
        case {"type": "yurish", "masofa": m} if m > 0:
            print(f"{m} metr oldinga yurildi")
        case {"type": "sakrash"}:
            print("Sakrash amalga oshirildi")
        case _:
            print("Noma'lum harakat!")
```

---

<a name="4-bob"></a>
# 4-Bob: Tsikllar, Generatorlar va Iteratsiya Protokollari

### 4.1. `for` va `while` Sikllari
Python dagi `for` sikli boshqa tillardagi sanagich emas, balki to'liq **Iterator Pattern** ustiga qurilgan:
```python
for element in [10, 20, 30]:
    print(element)
```

### 4.2. Generatorlar va `yield`
Generator — bu xotirani tejashning eng yuqori cho'qqisi. U barcha elementlarni birdaniga xotiraga yuklamaydi, balki har chaqirilganda bitta qiymat ishlab chiqaradi:
```python
def katta_oqim(n):
    for i in range(n):
        yield i ** 2

gen = katta_oqim(1000000) # RAM deyarli 0 bayt sarflaydi
print(next(gen)) # 0
print(next(gen)) # 1
```

---

<a name="5-bob"></a>
# 5-Bob: Kolleksiyalar: List, Tuple, Dict, Set va collections Moduli

Zamonaviy dasturlashda to'g'ri kolleksiyani tanlash algoritm tezligini belgilaydi:
* `list`: Dinamik massiv. Oxiriga qo'shish O(1), boshiga qo'shish O(n).
* `deque`: Ikki tomonlama navbat. Boshiga va oxiriga qo'shish O(1).
* `dict`: Xesh-jadval (Hash Table). Qidirish, qo'shish, o'chirish O(1).
* `set`: Noyob elementlar to'plami. Qidirish O(1).

```python
from collections import Counter, defaultdict, deque

sozlar = ["olma", "anor", "olma", "uzum"]
hisob = Counter(sozlar)
print("Eng ko'p uchragan:", hisob.most_common(1))
```

---

<a name="6-bob"></a>
# 6-Bob: Funksiyalar, Qamrov Doirasi (LEGB), Closures va Dekoratorlar

### 6.1. LEGB Qoidasi
O'zgaruvchilarni qidirish tartibi:
1. **L (Local)**: Funksiya ichida.
2. **E (Enclosing)**: Tashqi o'rab turuvchi funksiyada.
3. **G (Global)**: Modul fayl darajasida.
4. **B (Built-in)**: Python ichki nomlari (`len`, `range`).

### 6.2. Dekoratorlar (Decorators)
Dekorator — bu boshqa funksiyani argument sifatida qabul qilib, uning xatti-harakatini kengaytiruvchi funksiyadir:
```python
import time
from functools import wraps

def vaqtni_olcha(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        boshlanish = time.perf_counter()
        natija = func(*args, **kwargs)
        tugash = time.perf_counter()
        print(f"[{func.__name__}] {tugash - boshlanish:.6f} soniyada bajarildi")
        return natija
    return wrapper

@vaqtni_olcha
def tezkor_hisob():
    return sum(range(1000000))

tezkor_hisob()
```

---

<a name="7-bob"></a>
# 7-Bob: Ob'ektga Yo'naltirilgan Dasturlash (OOP), MRO va Metaprogramming

### 7.1. OOP ning 4 ta Asosiy Ustuni
1. **Inkapsulyatsiya (Encapsulation)**: Ma'lumotlar va metodlarni bitta sinfga birlashtirish hamda tashqi xavflardan yashirish (`_private`, `__mangled`).
2. **Merosxo'rlik (Inheritance)**: Umumiy xususiyatlarni ota sinfdan vorislik orqali olish (`super()`).
3. **Polimorfizm (Polymorphism)**: Bir xil interfeys bilan turli xil ob'ektlarning harakatlanishi (`Duck Typing`).
4. **Abstraksiya (Abstraction)**: Muhim bo'lmagan detallarni yashirish (`abc.ABC`, `@abstractmethod`).

### 7.2. Metaklasslar (Metaclasses)
Klasslarning o'zini yaratuvchi klasslar metaklass deyiladi. Ular yordamida orxestratorlar, plaginlar va validatsiya tizimlari quriladi:
```python
class StandartMetaklass(type):
    def __new__(cls, nom, asoslar, sifatlar):
        print(f"Yangi klass tizimda ro'yxatga olindi: {nom}")
        return super().__new__(cls, nom, asoslar, sifatlar)

class MeningModelim(metaclass=StandartMetaklass):
    pass
```

---

<a name="8-bob"></a>
# 8-Bob: Istisnolar, Crash-Proof Arxitektura va Logging

Professional dasturlar hech qachon kutilmaganda "qulab tushmasligi" (Crash) shart:
```python
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

try:
    qiymat = 10 / 2
    logging.info(f"Hisoblandi: {qiymat}")
except ZeroDivisionError as e:
    logging.error("Nolga bo'lish xatosi yuz berdi", exc_info=True)
finally:
    logging.info("Resurslar toza yopildi")
```

---

<a name="9-bob"></a>
# 9-Bob: Fayllar Tizimi, I/O Oqimlari va Baza Amallari (SQLite/ORM)

Fayllar bilan xavfsiz ishlash har doim `with` kontekst menejeri orqali amalga oshiriladi:
```python
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("O'zbek tili sun'iy intellekti")
```
SQLite bilan parametrlangan so'rovlar SQL Injection xavfini yo'qotadi:
```python
import sqlite3
with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE talabalar (ism TEXT, ball INT)")
    conn.execute("INSERT INTO talabalar VALUES (?, ?)", ("Alisher", 100))
```

---

<a name="10-bob"></a>
# 10-Bob: Parallelizm: Threading, Multiprocessing va Asinxron Dasturlash (asyncio)

* **I/O-Bound (Tarmoq, Fayl o'qish)**: `asyncio` yoki `threading` optimal.
* **CPU-Bound (Hisoblash, Kriptografiya, AI)**: `multiprocessing` yoki `ProcessPoolExecutor` optimal.

```python
import asyncio

async def yuklash(nom):
    await asyncio.sleep(0.01)
    return f"{nom} yuklandi"

async def main():
    natijalar = await asyncio.gather(yuklash("Fayl 1"), yuklash("Fayl 2"))
    print(natijalar)

asyncio.run(main())
```

---

<a name="11-bob"></a>
# 11-Bob: Regulyar Ifodalar (re) va Matn Muhandisligi (NLP Preprocessing)

Sun'iy intellekt modellarini o'qitishdan oldin xom matn tozalanishi shart:
1. HTML va keraksiz teglarni o'chirish: `re.sub(r'<[^>]+>', '', matn)`.
2. URL manzillarni tozalash: `re.sub(r'https?://\S+', '', matn)`.
3. Ortiqcha bo'shliqlar va bo'g'in chiziqchalarini birlashtirish (`kitob-\nlar` -> `kitoblar`).

---

<a name="12-bob"></a>
# 12-Bob: Tarmoq Protokollari, Socket Dasturlash va REST API Arxitekturasi

Past darajadagi TCP/UDP soketlaridan tortib, HTTP GET/POST, WebSocket va zamonaviy SSE (Server-Sent Events) oqimlarigacha to'liq modellashtiriladi.

---

<a name="13-bob"></a>
# 13-Bob: Algoritmlar va Ma'lumotlar Tuzilmasi (Big-O dan Dinamik Dasturlashgacha)

* **Murakkablik**: O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n).
* **Saralash**: Merge Sort (har doim O(n log n)), Quick Sort (o'rtacha O(n log n)).
* **Qidiruv**: Binary Search O(log n).
* **Dinamik Dasturlash (DP)**: Katta masalani bir-birini takrorlovchi kichik qismlarga bo'lib xotirada saqlash (Memoization & Tabulation).

---

<a name="14-bob"></a>
# 14-Bob: Ilmiy Hisoblash, Chiziqli Algebra va Mashinali O'rganish Poydevori

AI modelining poydevori quyidagi matematik tushunchalardir:
1. **Skalyar ko'paytma (Dot Product)**: Vektorlarning o'zaro ta'siri.
2. **Kosinus o'xshashligi (Cosine Similarity)**: Matnlar ma'nodoshligi (Embeddings).
3. **Faollashtiruvchilar**: Sigmoid, ReLU, Softmax, GeLU.
4. **Attention Mexanizmi**: `Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V`.

---

<a name="15-bob"></a>
# 15-Bob: Dastur Sifat Nazorati: Testlash (pytest/unittest), Profiling va CI/CD

Professional tizim sifat nazorati darajalari:
* **Unit Testing**: Har bir funksiyaning alohida to'g'ri ishlashi.
* **Integration Testing**: Modullarning o'zaro to'g'ri ulanishi.
* **Mocking**: Tashqi servislarni (baza, internet) ajratib sinash.
* **Benchmarking (cProfile)**: Unumdorlikdagi tor joylarni aniqlash.

---

<a name="16-bob"></a>
# 16-Bob: Maxsus Bob: 1-Bit LLM va Kvantlangan On-Device Sun'iy Intellekt Dvigatellari

### 16.1. 1-Bit Inqilobi (BitNet b1.58)
An'anaviy sun'iy intellekt modellari (FP16 yoki FP32) har bir parametr uchun 16 yoki 32 bit xotira sarflaydi. Masalan, 10 milliard (10B) parametrli modelni ishlatish uchun kamida 20-40 GB qimmatbaho video xotirasi (VRAM) kerak bo'ladi.

1-Bit arxitekturasida har bir vazn (weight) faqat uchta qiymatdan birini oladi: **{-1, 0, +1}**.
Bu inqilob quyidagi mislsiz afzalliklarni beradi:
1. **Xotira tejami**: 10B parametrli model 20 GB emas, balki atigi **1.5 - 2.5 GB** xotiraga sig'adi!
2. **Tezlik**: Qimmat float ko'paytirish (`float multiplication`) amali yo'qoladi. Uning o'rniga faqat **butun sonli qo'shish va ayirish** (`addition & subtraction`) bajariladi.
3. **On-Device Imkoniyat**: Katta serverlarsiz, to'g'ridan-to'g'ri foydalanuvchining shaxsiy noutbuki yoki smartfonida to'liq mustaqil ishlay oladi.

### 16.2. 1-Bit Matritsa Ko'paytmasi Kvantlash Koding:
```python
class BitNetLayer:
    def __init__(self, in_features, out_features):
        self.weights = [[1, -1], [-1, 1]] # Kvantlangan {-1, +1} vaznlar

    def forward(self, x):
        # Suzuvchi ko'paytirishlarsiz sof qo'shish/ayirish
        out = []
        for j in range(len(self.weights[0])):
            val = sum(x[i] if self.weights[i][j] == 1 else -x[i] for i in range(len(x)))
            out.append(val)
        return out
```

---

## XULOSA VA KELAJAK QADAMLARI

Ushbu mukammal qo'llanma va unga biriktirilgan 20 ta bobdan iborat **1,000 ta amaliy dasturlash topshiriqlari** mustaqil O'zbek tili sun'iy intellektini o'qitish uchun poydevor dataset bo'lib xizmat qiladi.

Endi sizning qo'lingizda dunyo darajasidagi to'liq, mukammal va professional O'zbek dasturlash bilimlari bazasi mavjud!
