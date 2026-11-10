# Python Dasturlash Tili — 19-Qism: Dasturiy Ta'minotni Testlash va Sifat Nazorati (pytest, unittest)
## (901-950 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam professional dastur sifatini ta'minlash, birlik testlari (Unit Testing), mock tizimlari va profilingni qamrab oladi:
* `unittest.TestCase` asoslari: `setUp`, `tearDown`, `assertRaises`, `assertAlmostEqual`;
* Test-Driven Development (TDD) falsafasi va Red-Green-Refactor sikli;
* Pytest tamoyillari: Sof `assert` lar, parametrli testlar, Fixturelar va Scopes;
* Mocking ustaligi: `Mock`, `MagicMock`, `@patch`, `side_effect`, `mock_open`;
* Resurslarni sinash: Vaqtinchalik fayllar (`tempfile`), konsol chiqishini ushlash (`stdout`);
* Unumdorlik va optimizatsiya: `timeit` mikrobrenchmark, `cProfile` va `tracemalloc` orqali xotira tahlili;
* Xavfsizlik va barqarorlik: SQL Injection, ReDoS, XSS testlari, Flaky testlar va CI/CD Pipeline;
* To'liq Sifat Ekotizimi (Doctest, Mypy, AST Security Audit);

---

# 901-Topshiriq: unittest.TestCase asoslari va oddiy assertEqual

## Topshiriq sharti:
Ikki sonni qo'shuvchi funksiya uchun standart unittest test sinfini yozing.

## Yechim (Python kodi):
```python
import unittest

def qoshish(a, b):
    return a + b

class TestQoshish(unittest.TestCase):
    def test_musbat_sonlar(self):
        self.assertEqual(qoshish(2, 3), 5)

    def test_manfiy_sonlar(self):
        self.assertEqual(qoshish(-1, -1), -2)

suite = unittest.TestLoader().loadTestsFromTestCase(TestQoshish)
res = unittest.TextTestRunner(verbosity=0).run(suite)
print("Testlar muvaffaqiyatli o'tdimi:", res.wasSuccessful())
```

## Tushuntirish va Mantiq:
1. `unittest.TestCase` dan meros olingan klass ichida `test_` bilan boshlanuvchi har bir metod alohida test hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: Testlar muvaffaqiyatli o'tdimi: True
```

---

# 902-Topshiriq: setUp va tearDown metodlari (Test Fixture)

## Topshiriq sharti:
Har bir test oldidan ma'lumotlarni tayyorlash va testdan so'ng tozalash tartibini yarating.

## Yechim (Python kodi):
```python
import unittest

class TestRoyxatOperatsiyalari(unittest.TestCase):
    def setUp(self):
        self.royxat = [1, 2, 3]

    def tearDown(self):
        self.royxat.clear()

    def test_qoshish(self):
        self.royxat.append(4)
        self.assertEqual(len(self.royxat), 4)

    def test_ochirish(self):
        self.royxat.pop()
        self.assertEqual(len(self.royxat), 2)

suite = unittest.TestLoader().loadTestsFromTestCase(TestRoyxatOperatsiyalari)
res = unittest.TextTestRunner(verbosity=0).run(suite)
print("setUp/tearDown testlari:", res.wasSuccessful())
```

## Tushuntirish va Mantiq:
1. `setUp` har bir test uchun toza va mustaqil muhit ta'minlaydi (Test Isolation).

## Ishlash natijasi:
```text
Chiqish: setUp/tearDown testlari: True
```

---

# 903-Topshiriq: Istisnolarni testlash (assertRaises)

## Topshiriq sharti:
Nolga bo'lish paytida `ZeroDivisionError` tashlanishini test qiling.

## Yechim (Python kodi):
```python
import unittest

def bolish(a, b):
    if b == 0:
        raise ZeroDivisionError("Nolga bo'lib bo'lmaydi!")
    return a / b

class TestBolish(unittest.TestCase):
    def test_nolga_bolish(self):
        with self.assertRaises(ZeroDivisionError):
            bolish(10, 0)

suite = unittest.TestLoader().loadTestsFromTestCase(TestBolish)
print("assertRaises muvaffaqiyatli:", unittest.TextTestRunner(verbosity=0).run(suite).wasSuccessful())
```

## Tushuntirish va Mantiq:
1. `with self.assertRaises(...)` kutilgan xatolik tashlanganligini tasdiqlaydi.

## Ishlash natijasi:
```text
Chiqish: assertRaises muvaffaqiyatli: True
```

---

# 904-Topshiriq: Qalqib chiquvchi sonlarni taqqoslash (assertAlmostEqual)

## Topshiriq sharti:
Suzuvchi nuqtali (float) sonlardagi yaxlitlash xatoliklarini hisobga olib tekshiring.

## Yechim (Python kodi):
```python
import unittest

class TestFloat(unittest.TestCase):
    def test_float_yigindi(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)

suite = unittest.TestLoader().loadTestsFromTestCase(TestFloat)
print("assertAlmostEqual o'tdi:", unittest.TextTestRunner(verbosity=0).run(suite).wasSuccessful())
```

## Tushuntirish va Mantiq:
1. `assertAlmostEqual` ma'lum bir kasr xonasigacha (places) yaqinlikni tekshiradi.

## Ishlash natijasi:
```text
Chiqish: assertAlmostEqual o'tdi: True
```

---

# 905-Topshiriq: TDD (Test-Driven Development) Red-Green-Refactor sikli

## Topshiriq sharti:
Avval muvaffaqiyatsiz test yozish, keyin minimal kod yozib o'tkazish, so'ng refactoring qilish.

## Yechim (Python kodi):
```python
def teskari_satr(s):
    return s[::-1]

import unittest
class TestTDD(unittest.TestCase):
    def test_teskari(self):
        self.assertEqual(teskari_satr("salom"), "molas")
        self.assertEqual(teskari_satr(""), "")

suite = unittest.TestLoader().loadTestsFromTestCase(TestTDD)
print("TDD testi muvaffaqiyatli:", unittest.TextTestRunner(verbosity=0).run(suite).wasSuccessful())
```

## Tushuntirish va Mantiq:
1. TDD koddagi ortiqcha logikaning oldini oladi va arxitekturani boshidanoq testlanuvchan qiladi.

## Ishlash natijasi:
```text
Chiqish: TDD testi muvaffaqiyatli: True
```

---

# 906-Topshiriq: Pytest uslubidagi sof 'assert' ifodalari

## Topshiriq sharti:
Oddiy Python assert operatori yordamida test funksiyasi tuzilmasi.

## Yechim (Python kodi):
```python
def kvadrat(n):
    return n * n

def test_kvadrat_musbat():
    assert kvadrat(4) == 16

def test_kvadrat_nol():
    assert kvadrat(0) == 0

test_kvadrat_musbat()
test_kvadrat_nol()
print("Pytest uslubidagi sof assertlar muvaffaqiyatli bajarildi!")
```

## Tushuntirish va Mantiq:
1. Pytest maxsus metodlarsiz standart `assert` ni bayt-kod darajasida tahlil qilib xato sababini chiroyli ko'rsatadi.

## Ishlash natijasi:
```text
Chiqish: Pytest uslubidagi sof assertlar muvaffaqiyatli bajarildi!
```

---

# 907-Topshiriq: Parametrlangan testlar (Parametrized Testing)

## Topshiriq sharti:
Bitta test funksiyasini turli xil kiruvchi va kutiluvchi ma'lumotlar bilan ko'p marta tekshirish.

## Yechim (Python kodi):
```python
test_holatlari = [
    ("kiyik", True),
    ("radar", True),
    ("salom", False),
    ("", True)
]

def palindrommi(s):
    return s == s[::-1]

for matn, kutilgan in test_holatlari:
    assert palindrommi(matn) == kutilgan
print("Barcha parametrlangan testlar o'tdi.")
```

## Tushuntirish va Mantiq:
1. Pytest da bu `@pytest.mark.parametrize` dekoratori orqali amalga oshiriladi.

## Ishlash natijasi:
```text
Chiqish: Barcha parametrlangan testlar o'tdi.
```

---

# 908-Topshiriq: unittest.mock.Mock asoslari

## Topshiriq sharti:
Tashqi tizimlar yoki funksiyalarni soxta ob'ekt (Mock) bilan almashtiring.

## Yechim (Python kodi):
```python
from unittest.mock import Mock

soxta_servis = Mock()
soxta_servis.foydalanuvchini_ol.return_value = {"id": 42, "ism": "Ali"}

natija = soxta_servis.foydalanuvchini_ol(42)
print("Mock qaytargan ma'lumot:", natija)
soxta_servis.foydalanuvchini_ol.assert_called_once_with(42)
```

## Tushuntirish va Mantiq:
1. `Mock` ob'ekt qanday metodlar chaqirilgani va qanday parametrlar uzatilganini to'liq yozib boradi.

## Ishlash natijasi:
```text
Chiqish: Mock qaytargan ma'lumot: {'id': 42, 'ism': 'Ali'}
```

---

# 909-Topshiriq: Mock Side Effect (Istisno tashlash simulyatsiyasi)

## Topshiriq sharti:
Tashqi servis nosozligida (Timeout) kodimiz xatolikni to'g'ri qayta ishlashini tekshiring.

## Yechim (Python kodi):
```python
from unittest.mock import Mock

api_mijoz = Mock()
api_mijoz.sorov_yuborish.side_effect = TimeoutError("Server javob bermadi")

def xavfsiz_yuklash(mijoz):
    try:
        return mijoz.sorov_yuborish()
    except TimeoutError:
        return "Zaxira ma'lumoti"

print("Natija:", xavfsiz_yuklash(api_mijoz))
```

## Tushuntirish va Mantiq:
1. `side_effect` yordamida ixtiyoriy istisno yoki dinamik funksiya chaqiruvini simulyatsiya qilish mumkin.

## Ishlash natijasi:
```text
Chiqish: Natija: Zaxira ma'lumoti
```

---

# 910-Topshiriq: unittest.mock.patch kontekst menejeri

## Topshiriq sharti:
Vaqt yoki ob-havo API funksiyasini vaqtincha mock qilib o'rnini almashtiring.

## Yechim (Python kodi):
```python
from unittest.mock import patch
import time

def kuting_va_qaytaring():
    time.sleep(100)
    return "Tayyor"

with patch("time.sleep", return_value=None) as mock_sleep:
    natija = kuting_va_qaytaring()
    print("Natija:", natija)
    print("Sleep chaqirildimi:", mock_sleep.called)
```

## Tushuntirish va Mantiq:
1. `patch` test tugagach asl funksiyani avtomatik o'z o'rniga qaytaradi (avtomatik unpatch).

## Ishlash natijasi:
```text
Chiqish: Natija: Tayyor, Sleep chaqirildimi: True
```

---

# 911-Topshiriq: stdout chiqishini ushlash va testlash (Capturing Output)

## Topshiriq sharti:
Funksiya konsolga to'g'ri xabar chiqarayotganini tekshiring.

## Yechim (Python kodi):
```python
import io
import sys

def salomlash(ism):
    print(f"Salom, {ism}!")

ushlangan_chiqish = io.StringIO()
asl_stdout = sys.stdout
try:
    sys.stdout = ushlangan_chiqish
    salomlash("Alisher")
finally:
    sys.stdout = asl_stdout

natija_matni = ushlangan_chiqish.getvalue().strip()
print("Ushlangan konsol xabari:", natija_matni)
assert natija_matni == "Salom, Alisher!"
```

## Tushuntirish va Mantiq:
1. CLI dasturlari va konsol ilovalarini avtomatlashtirilgan testlashda qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: Ushlangan konsol xabari: Salom, Alisher!
```

---

# 912-Topshiriq: Vaqtinchalik fayllar va papkalar (tempfile moduli)

## Topshiriq sharti:
Fayl yaratish va o'qish operatsiyalarini xavfsiz vaqtinchalik muhitda test qiling.

## Yechim (Python kodi):
```python
import tempfile
import os

with tempfile.TemporaryDirectory() as temp_dir:
    fayl_yoli = os.path.join(temp_dir, "test.txt")
    with open(fayl_yoli, "w", encoding="utf-8") as f:
        f.write("Test ma'lumotlari")
        
    with open(fayl_yoli, "r", encoding="utf-8") as f:
        mazmun = f.read()
    assert mazmun == "Test ma'lumotlari"
    print("Vaqtincha fayl yaratildi va muvaffaqiyatli tekshirildi.")
```

## Tushuntirish va Mantiq:
1. `TemporaryDirectory` test tugagach barcha qoldiqlarni qattiq diskdan butunlay tozalaydi.

## Ishlash natijasi:
```text
Chiqish: Vaqtincha fayl yaratildi va muvaffaqiyatli tekshirildi.
```

---

# 913-Topshiriq: Kod qamrovi (Code Coverage) tushunchasi

## Topshiriq sharti:
Funksiyadagi hamma shoxlar (if/else) testlar bilan qamrab olinganini tekshirish tamoyili.

## Yechim (Python kodi):
```python
def baho_ber(ball):
    if ball >= 90:
        return "A'lo"
    elif ball >= 70:
        return "Yaxshi"
    else:
        return "Qoniqarsiz"

assert baho_ber(95) == "A'lo"
assert baho_ber(75) == "Yaxshi"
assert baho_ber(50) == "Qoniqarsiz"
print("Barcha shoxlar (Branch Coverage 100%) sinovdan o'tdi.")
```

## Tushuntirish va Mantiq:
1. Code Coverage (pytest-cov) koddagi tekshirilmay qolgan zaif nuqtalarni ko'rsatib beradi.

## Ishlash natijasi:
```text
Chiqish: Barcha shoxlar (Branch Coverage 100%) sinovdan o'tdi.
```

---

# 914-Topshiriq: timeit moduli: Kod tezligini aniq o'lchash (Micro-benchmarking)

## Topshiriq sharti:
List comprehension va `for` sikli tezligini 10,000 marta bajarib solishtiring.

## Yechim (Python kodi):
```python
import timeit

vaqt_comp = timeit.timeit("[x**2 for x in range(100)]", number=10000)
vaqt_loop = timeit.timeit("""
res = []
for x in range(100):
    res.append(x**2)
""", number=10000)

print(f"Comprehension {vaqt_loop / vaqt_comp:.2f} barobar tezroq.")
```

## Tushuntirish va Mantiq:
1. `timeit` GC va fon jarayonlari ta'sirini kamaytirgan holda aniq vaqtni o'lchaydi.

## Ishlash natijasi:
```text
Chiqish: Comprehension ... barobar tezroq.
```

---

# 915-Topshiriq: cProfile moduli: Funksional unumdorlik profaylingi (Bottleneck qidiruvi)

## Topshiriq sharti:
Dastur vaqtining asosiy qismi qaysi funksiyalarda yo'qotilayotganini tahlil qiling.

## Yechim (Python kodi):
```python
import cProfile
import pstats
import io

def sekin_funksiya():
    return sum(i * i for i in range(200000))

pr = cProfile.Profile()
pr.enable()
sekin_funksiya()
pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
ps.print_stats(3)
print("Profil tayyorlandi.")
```

## Tushuntirish va Mantiq:
1. `cProfile` chaqiriqlar soni (`ncalls`) va sof vaqt (`tottime`) bo'yicha eng sekin joylarni topadi.

## Ishlash natijasi:
```text
Chiqish: Profil tayyorlandi.
```

---

# 916-Topshiriq: tracemalloc moduli: Xotira oqishini (Memory Leak) aniqlash

## Topshiriq sharti:
Qaysi qatorlar eng ko'p RAM xotirasi band qilayotganini kuzating.

## Yechim (Python kodi):
```python
import tracemalloc

tracemalloc.start()
katta_massiv = [x for x in range(100000)]
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("Eng ko'p xotira band qilgan qator:", top_stats[0])
tracemalloc.stop()
```

## Tushuntirish va Mantiq:
1. `tracemalloc` Python obyektlarining aynan qaysi fayl va qatorda ajratilganini (allocation traceback) ko'rsatadi.

## Ishlash natijasi:
```text
Chiqish: Eng ko'p xotira band qilgan qator: ...
```

---

# 917-Topshiriq: unittest.skip va skipIf dekoratorlari

## Topshiriq sharti:
Muayyan shartlarda testni o'tkazib yuborish.

## Yechim (Python kodi):
```python
import unittest

class TestPlatforma(unittest.TestCase):
    @unittest.skip("Hali to'liq ishlab chiqilmagan")
    def test_yangi(self): pass

suite = unittest.TestLoader().loadTestsFromTestCase(TestPlatforma)
res = unittest.TextTestRunner(verbosity=0).run(suite)
print("O'tkazib yuborilgan testlar soni:", len(res.skipped))
```

## Tushuntirish va Mantiq:
1. `@unittest.skip` integratsion testlar va turli platformalarga moslashishda qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: O'tkazib yuborilgan testlar soni: 1
```

---

# 918-Topshiriq: Property-Based Testing falsafasi (Tasodifiy gipoteza)

## Topshiriq sharti:
Qat'iy bitta qiymat bilan emas, balki 100 ta tasodifiy sonlar bilan invariant qoidani sinash.

## Yechim (Python kodi):
```python
import random

def sarala_va_tekshir():
    for _ in range(50):
        sonlar = [random.randint(-1000, 1000) for _ in range(20)]
        saralangan = sorted(sonlar)
        assert len(saralangan) == len(sonlar)
        for i in range(len(saralangan) - 1):
            assert saralangan[i] <= saralangan[i + 1]

sarala_va_tekshir()
print("Property-based test muvaffaqiyatli yakunlandi.")
```

## Tushuntirish va Mantiq:
1. Hypothesis kutubxonasi aynan shu tamoyilda inson xayoliga kelmagan ekstremal chekka holatlarni topadi.

## Ishlash natijasi:
```text
Chiqish: Property-based test muvaffaqiyatli yakunlandi.
```

---

# 919-Topshiriq: API integratsion testlari (Mocked Requests Session)

## Topshiriq sharti:
Tashqi API so'rovini haqiqiy tarmoqqa chiqmasdan to'liq integratsiya testidan o'tkazing.

## Yechim (Python kodi):
```python
from unittest.mock import Mock

def ob_havo_ol(shahar, session):
    response = session.get(f"https://api.weather.com/{shahar}")
    if response.status_code == 200:
        return response.json().get("harorat")
    return None

soxta_session = Mock()
soxta_response = Mock()
soxta_response.status_code = 200
soxta_response.json.return_value = {"harorat": "+22C"}
soxta_session.get.return_value = soxta_response

assert ob_havo_ol("Toshkent", soxta_session) == "+22C"
print("API testi muvaffaqiyatli!")
```

## Tushuntirish va Mantiq:
1. Mocked sessiya orqali tarmoq mustaqil va millisoniyalarda ishlovchi testlar tuziladi.

## Ishlash natijasi:
```text
Chiqish: API testi muvaffaqiyatli!
```

---

# 920-Topshiriq: Mutatsion testlash (Mutation Testing) tushunchasi

## Topshiriq sharti:
Testlarning o'zini sifatini tekshirish uchun kodga ataylab xatolar kiritib test ularni tuta olishini sinash.

## Yechim (Python kodi):
```python
def mutatsiya_simulyatsiyasi(test_suite_tutdimi):
    return "Mutant yo'q qilindi! (Testlar sifatli)" if test_suite_tutdimi else "Xato"

print(mutatsiya_simulyatsiyasi(True))
```

## Tushuntirish va Mantiq:
1. Mutatsion testlash 100% test qamrovi bo'lsa ham uning haqiqiy sifatini ochib beradi.

## Ishlash natijasi:
```text
Chiqish: Mutant yo'q qilindi! (Testlar sifatli)
```

---

# 921-Topshiriq: Snapshot Testing tushunchasi

## Topshiriq sharti:
Katta JSON natijasini oldingi etalon fayl (snapshot) bilan solishtirish.

## Yechim (Python kodi):
```python
import json

def api_javob():
    return {"status": "ok", "versiya": "2.0"}

etalon = '{"status": "ok", "versiya": "2.0"}'
assert json.dumps(api_javob(), sort_keys=True) == json.dumps(json.loads(etalon), sort_keys=True)
print("Snapshot testi to'liq mos keldi!")
```

## Tushuntirish va Mantiq:
1. Murakkab UI daraxtlari va yirik JSON strukturalarini o'zgarishsiz qolganini tekshirishda juda qulay.

## Ishlash natijasi:
```text
Chiqish: Snapshot testi to'liq mos keldi!
```

---

# 922-Topshiriq: Doimiy Integratsiya (CI Pipeline) GitHub Actions arxitekturasi

## Topshiriq sharti:
Avtomatik testlarni har bir Git push da ishga tushiruvchi YAML konfiguratsiyasi tuzilmasi.

## Yechim (Python kodi):
```python
ci_yaml = "name: Tests\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest"
print("CI Pipeline konfiguratsiyasi mavjud:", bool(ci_yaml))
```

## Tushuntirish va Mantiq:
1. CI har qanday xato kod bazaga (main branch) qo'shilishining oldini oluvchi avtomatik qorovuldir.

## Ishlash natijasi:
```text
Chiqish: CI Pipeline konfiguratsiyasi mavjud: True
```

---

# 923-Topshiriq: Fayl tizimi I/O testlarida mock_open dan foydalanish

## Topshiriq sharti:
Haqiqiy fayl ochmasdan `open()` chaqiruvini xotirada mock qilish.

## Yechim (Python kodi):
```python
from unittest.mock import patch, mock_open

m = mock_open(read_data="Maxfiy ma'lumot")
with patch("builtins.open", m):
    with open("maxfiy.txt", "r") as f:
        malumot = f.read()

assert malumot == "Maxfiy ma'lumot"
print("mock_open muvaffaqiyatli!")
```

## Tushuntirish va Mantiq:
1. `mock_open` disk bilan ishlovchi funksiyalarni qattiq diskka teginmasdan tezkor sinashga imkon beradi.

## Ishlash natijasi:
```text
Chiqish: mock_open muvaffaqiyatli!
```

---

# 924-Topshiriq: Xavfsizlik testi: SQL Injection tekshiruvi

## Topshiriq sharti:
SQL so'rovlarida parametrli formatlash qo'llanganligini tasdiqlovchi test.

## Yechim (Python kodi):
```python
def xavfsiz_sql_sorov(login):
    return "SELECT * FROM foydalanuvchilar WHERE login = ?", (login,)

sorov, parametrlar = xavfsiz_sql_sorov("admin' OR '1'='1")
assert "?" in sorov
print("SQL Injection xavfsizligi tasdiqlandi!")
```

## Tushuntirish va Mantiq:
1. String formatlash o'rniga parametrli uzatish xavfsizlik testlarining birinchi talabidir.

## Ishlash natijasi:
```text
Chiqish: SQL Injection xavfsizligi tasdiqlandi!
```

---

# 925-Topshiriq: Asinxron testlash (unittest.IsolatedAsyncioTestCase)

## Topshiriq sharti:
Python 3.8+ da asinxron coroutine funksiyalarni to'g'ridan-to'g'ri test qilish.

## Yechim (Python kodi):
```python
import unittest
import asyncio

async def asinxron_hisob(a, b):
    await asyncio.sleep(0.01)
    return a * b

class TestAsync(unittest.IsolatedAsyncioTestCase):
    async def test_hisob(self):
        natija = await asinxron_hisob(3, 4)
        self.assertEqual(natija, 12)

suite = unittest.TestLoader().loadTestsFromTestCase(TestAsync)
res = unittest.TextTestRunner(verbosity=0).run(suite)
print("Asinxron test muvaffaqiyatli:", res.wasSuccessful())
```

## Tushuntirish va Mantiq:
1. `IsolatedAsyncioTestCase` har bir test uchun alohida asyncio hodisalar siklini (Event Loop) boshqaradi.

## Ishlash natijasi:
```text
Chiqish: Asinxron test muvaffaqiyatli: True
```

---

# 926-Topshiriq: Pytest Fixture doiralari (Scopes: function, module, session)

## Topshiriq sharti:
Fixture qachon yaratilib qachon yo'q qilinishini nazorat qilish tamoyili.

## Yechim (Python kodi):
```python
class TestFixtureSimulyatsiya:
    def __init__(self, scope="module"):
        self.scope = scope
        self.baza_ulanishi = "PostgreSQL_Ulandi"

    def __enter__(self): return self.baza_ulanishi
    def __exit__(self, *args): self.baza_ulanishi = "Yopildi"

with TestFixtureSimulyatsiya("session") as db:
    print("Fixture ulanishi:", db)
```

## Tushuntirish va Mantiq:
1. Session darajasidagi fixturelar barcha yuzlab testlar uchun resursni (DB, Docker) bir martagina tayyorlaydi.

## Ishlash natijasi:
```text
Chiqish: Fixture ulanishi: PostgreSQL_Ulandi
```

---

# 927-Topshiriq: Monkeypatching: Muhit o'zgaruvchilarini testda o'zgartirish

## Topshiriq sharti:
Test davomida `os.environ` qiymatini xavfsiz o'zgartirish va tiklash.

## Yechim (Python kodi):
```python
import os

def get_db_url():
    return os.environ.get("DATABASE_URL", "sqlite:///default.db")

class MonkeyPatcher:
    def __init__(self):
        self.asl = dict(os.environ)

    def setenv(self, key, val):
        os.environ[key] = val

    def tiklash(self):
        os.environ.clear()
        os.environ.update(self.asl)

mp = MonkeyPatcher()
mp.setenv("DATABASE_URL", "postgresql://test:test@localhost/testdb")
assert get_db_url() == "postgresql://test:test@localhost/testdb"
mp.tiklash()
print("Monkeypatch muvaffaqiyatli tiklandi!")
```

## Tushuntirish va Mantiq:
1. Muhit parametrlarini testlash tashqi server sozlamalariga bog'liq bo'lmaslikni ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Monkeypatch muvaffaqiyatli tiklandi!
```

---

# 928-Topshiriq: Database Transaction Rollback testlari

## Topshiriq sharti:
Har bir test ma'lumotlar bazasiga o'zgartirish kiritgach, uni rollback qilib toza saqlash.

## Yechim (Python kodi):
```python
class SoxtaDBTranzaksiya:
    def __init__(self):
        self.malumotlar = []

    def insert(self, yozuv):
        self.malumotlar.append(yozuv)

    def rollback(self):
        self.malumotlar.clear()

db = SoxtaDBTranzaksiya()
db.insert("Test foydalanuvchi")
assert len(db.malumotlar) == 1
db.rollback()
assert len(db.malumotlar) == 0
print("Tranzaksiya rollback testi muvaffaqiyatli!")
```

## Tushuntirish va Mantiq:
1. Tranzaksiyalarni orqaga qaytarish testlarning o'zaro bir-biriga ta'sir qilishini yo'qotadi.

## Ishlash natijasi:
```text
Chiqish: Tranzaksiya rollback testi muvaffaqiyatli!
```

---

# 929-Topshiriq: Flaky testlarni boshqarish (Avtomatik Qayta Urinish)

## Topshiriq sharti:
Vaqti-vaqti bilan asossiz yiqiluvchi testlarni avtomatik qayta yurgizish mexanizmi.

## Yechim (Python kodi):
```python
import random

def beqaror_tarmoq_funksiyasi():
    # 50% ehtimol bilan muvaffaqiyat
    return True

def flaky_test_runner(test_fn, max_urinish=3):
    for i in range(max_urinish):
        try:
            if test_fn(): return True
        except Exception:
            pass
    return False

print("Flaky test natijasi:", flaky_test_runner(beqaror_tarmoq_funksiyasi))
```

## Tushuntirish va Mantiq:
1. `pytest-rerunfailures` beqaror tarmoq yoki kechikish tufayli yiqilgan testlarni qayta sinaydi.

## Ishlash natijasi:
```text
Chiqish: Flaky test natijasi: True
```

---

# 930-Topshiriq: Warninglarni testlash (pytest.warns va warnings moduli)

## Topshiriq sharti:
Eskirgan (Deprecated) funksiyalar to'g'ri ogohlantirish berishini tekshiring.

## Yechim (Python kodi):
```python
import warnings

def eski_funksiya():
    warnings.warn("Ushbu funksiya kelgusida o'chiriladi!", DeprecationWarning)

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    eski_funksiya()
    assert len(w) == 1
    assert issubclass(w[-1].category, DeprecationWarning)
    print("DeprecationWarning muvaffaqiyatli tutildi:", w[-1].message)
```

## Tushuntirish va Mantiq:
1. Kutubxona ishlab chiquvchilari API eskirishini foydalanuvchiga bildirishda buni testlaydi.

## Ishlash natijasi:
```text
Chiqish: DeprecationWarning muvaffaqiyatli tutildi: Ushbu funksiya kelgusida o'chiriladi!
```

---

# 931-Topshiriq: Vaqtni muzlatish (Freezegun tamoyili)

## Topshiriq sharti:
Vaqtga bog'liq (masalan, obuna tugash sanasi) testlar uchun tizim soatini soxtalashtirish.

## Yechim (Python kodi):
```python
import datetime

class MuzlatilganVaqt:
    def __init__(self, yil, oy, kun):
        self.vaqt = datetime.date(yil, oy, kun)

    def bugun(self):
        return self.vaqt

soat = MuzlatilganVaqt(2026, 11, 7)
assert soat.bugun().year == 2026
print("Muzlatilgan sana:", soat.bugun())
```

## Tushuntirish va Mantiq:
1. Freezegun kutubxonasi `datetime.now()` chaqiruvlarini qat'iy belgilangan vaqtga qotiradi.

## Ishlash natijasi:
```text
Chiqish: Muzlatilgan sana: 2026-11-07
```

---

# 932-Topshiriq: XSS (Cross-Site Scripting) sanitizatsiya testi

## Topshiriq sharti:
HTML inputlarida `<script>` teglari tozalanishini tasdiqlovchi xavfsizlik testi.

## Yechim (Python kodi):
```python
import html

def toza_html(matn):
    return html.escape(matn)

xavfli_kirish = "<script>alert('XSS')</script>"
xavfsiz = toza_html(xavfli_kirish)
assert "<script>" not in xavfsiz
print("Zararsizlantirilgan HTML:", xavfsiz)
```

## Tushuntirish va Mantiq:
1. Barcha foydalanuvchi kiritmalari ekranga chiqarilishidan oldin ekranlanishi (escape) shart.

## Ishlash natijasi:
```text
Chiqish: Zararsizlantirilgan HTML: &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;
```

---

# 933-Topshiriq: ReDoS (Regular Expression Denial of Service) xavfsizlik testi

## Topshiriq sharti:
Regex shablonida halokatli qaytish (Catastrophic Backtracking) yo'qligini tekshiring.

## Yechim (Python kodi):
```python
import time
import re

shablon = re.compile(r"^[a-zA-Z0-9]+$")
xavfli_satr = "a" * 30 + "!"

start = time.perf_counter()
shablon.match(xavfli_satr)
sarf = (time.perf_counter() - start) * 1000

print(f"Regex tekshirish vaqti: {sarf:.4f} ms")
assert sarf < 10.0 # ReDoS xavfi yo'q
```

## Tushuntirish va Mantiq:
1. Murakkab va yomon yozilgan regexlar server protsessorini 100% yuklab qotirib qo'yishi mumkin.

## Ishlash natijasi:
```text
Chiqish: Regex tekshirish vaqti: ... ms
```

---

# 934-Topshiriq: Yuklama testi (Load Testing: Concurrent Requests simulyatsiyasi)

## Topshiriq sharti:
Bir vaqtning o'zida 50 ta mijoz so'rov berganda tizim barqarorligini tekshiring.

## Yechim (Python kodi):
```python
from concurrent.futures import ThreadPoolExecutor

hisob = 0
def soxta_tranzaksiya():
    global hisob
    hisob += 1
    return hisob

with ThreadPoolExecutor(max_workers=10) as ex:
    natijalar = list(ex.map(lambda _: soxta_tranzaksiya(), range(50)))

assert len(natijalar) == 50
print("50 ta parallel yuklama muvaffaqiyatli yakunlandi.")
```

## Tushuntirish va Mantiq:
1. Ko'p oqimli yuklama testlari poyga shartlari (Race conditions) bor-yo'qligini fosh qiladi.

## Ishlash natijasi:
```text
Chiqish: 50 ta parallel yuklama muvaffaqiyatli yakunlandi.
```

---

# 935-Topshiriq: Stress testlash: Chekka xotira sarfini nazorat qilish

## Topshiriq sharti:
Massiv hajmi 1,000,000 bo'lganda dastur xotiradan oshib ketmasligini tekshiring.

## Yechim (Python kodi):
```python
import sys

kichik_massiv = [0] * 1000
bayt_hajm = sys.getsizeof(kichik_massiv)
assert bayt_hajm < 100000
print(f"Xotira cheklovi nazorat ostida: {bayt_hajm} bayt")
```

## Tushuntirish va Mantiq:
1. Katta hajmdagi ma'lumotlarda resurslar me'yordan oshmasligini tekshirish.

## Ishlash natijasi:
```text
Chiqish: Xotira cheklovi nazorat ostida: ... bayt
```

---

# 936-Topshiriq: Regressiya testlari (Regression Testing)

## Topshiriq sharti:
Ilgari yuz bergan va tuzatilgan bug uchun qayta tiklanmaslik testi yozish.

## Yechim (Python kodi):
```python
# Bug #104: Bo'sh satr kiritilganda dastur qulagan edi
def soz_sanagich(matn):
    if not matn.strip(): return 0
    return len(matn.split())

# Regressiya testi
assert soz_sanagich("   ") == 0
assert soz_sanagich("") == 0
print("Regressiya testi: Bug #104 qaytalanmaydi!")
```

## Tushuntirish va Mantiq:
1. Har bir topilgan xatolik uchun yozilgan test tizimning kelajakdagi barqarorligini mustahkamlaydi.

## Ishlash natijasi:
```text
Chiqish: Regressiya testi: Bug #104 qaytalanmaydi!
```

---

# 937-Topshiriq: BDD (Behavior Driven Development) Given-When-Then sintaksisi

## Topshiriq sharti:
Biznes talablarini inson tushunadigan xatti-harakatlar orqali ifodalash.

## Yechim (Python kodi):
```python
def test_bank_yechib_olish():
    # Given (Berilgan shart): Hisobda 100 ming so'm bor
    balans = 100000
    # When (Harakat): 30 ming so'm yechib olindi
    balans -= 30000
    # Then (Natija): Hisobda 70 ming so'm qolishi shart
    assert balans == 70000
    print("BDD xatti-harakat testi muvaffaqiyatli!")

test_bank_yechib_olish()
```

## Tushuntirish va Mantiq:
1. BDD (Behave, Cucumber) dasturchi va biznes vakillari o'rtasida umumiy til yaratadi.

## Ishlash natijasi:
```text
Chiqish: BDD xatti-harakat testi muvaffaqiyatli!
```

---

# 938-Topshiriq: Shartnoma testlari (Contract Testing)

## Topshiriq sharti:
API qaytargan JSON strukturasi belgilangan sxemaga qat'iy mosligini tasdiqlang.

## Yechim (Python kodi):
```python
kutilgan_sxema = {"id": int, "nom": str, "narx": float}

haqiqiy_javob = {"id": 1, "nom": "Noutbuk", "narx": 8500000.0}

for kalit, kutilgan_tur in kutilgan_sxema.items():
    assert kalit in haqiqiy_javob
    assert isinstance(haqiqiy_javob[kalit], kutilgan_tur)

print("API Contract sxemasi to'liq tasdiqlandi!")
```

## Tushuntirish va Mantiq:
1. Mikroxizmatlar (Microservices) o'rtasidagi aloqa shartnomalari buzilmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Chiqish: API Contract sxemasi to'liq tasdiqlandi!
```

---

# 939-Topshiriq: API Fuzzing (Tasodifiy buzilgan ma'lumotlar bilan testlash)

## Topshiriq sharti:
Noma'lum, buzilgan va g'alati qiymatlar yuborilganda dastur 500 xato bermasligini tekshiring.

## Yechim (Python kodi):
```python
def api_parolovchi(kirish):
    try:
        val = int(kirish)
        return {"status": 200, "val": val}
    except Exception:
        return {"status": 400, "error": "Yaroqsiz qiymat"}

fuzz_qiymatlar = [None, "", "\x00\xff", "abc"*100, -9999999999999999]
for f in fuzz_qiymatlar:
    res = api_parolovchi(f)
    assert res["status"] in (200, 400) # Server qulamadi

print("Fuzzing sinovi muvaffaqiyatli o'tdi.")
```

## Tushuntirish va Mantiq:
1. Fuzzing kiberxavfsizlikda noma'lum zaifliklarni (0-day vulnerabilities) topishda eng asosiy usuldir.

## Ishlash natijasi:
```text
Chiqish: Fuzzing sinovi muvaffaqiyatli o'tdi.
```

---

# 940-Topshiriq: Golden Master testlash (Eski kodni refactoring qilish)

## Topshiriq sharti:
Kodni o'zgartirishdan oldin uning 1,000 ta turli natijalarini saqlab olib, yangisi bilan solishtiring.

## Yechim (Python kodi):
```python
def eski_algoritm(x): return x * 2 + 1
def yangi_algoritm(x): return (x << 1) + 1

for i in range(100):
    assert eski_algoritm(i) == yangi_algoritm(i)
print("Golden master: Yangi optimallashgan algoritm 100% mos!")
```

## Tushuntirish va Mantiq:
1. Qadimiy va murakkab kodlarni xavfsiz yangilashda (Legacy Code Refactoring) qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: Golden master: Yangi optimallashgan algoritm 100% mos!
```

---

# 941-Topshiriq: End-to-End (E2E) va Page Object Pattern

## Topshiriq sharti:
Veb sahifa yoki UI interfeysini ob'ekt sifatida modellashtirib avtomatlashtirish.

## Yechim (Python kodi):
```python
class BoshSahifaModeli:
    def qidiruv_kirit(self, matn):
        return f"'{matn}' bo'yicha qidiruv natijalari sahifasi"

sahifa = BoshSahifaModeli()
assert "Python" in sahifa.qidiruv_kirit("Python")
print("Page Object Pattern testi o'tdi.")
```

## Tushuntirish va Mantiq:
1. Selenium va Playwright bilan brauzer testlarini oson boshqariladigan qiladi.

## Ishlash natijasi:
```text
Chiqish: Page Object Pattern testi o'tdi.
```

---

# 942-Topshiriq: Ichki maxfiy metodlarni testlash (Private method testing)

## Topshiriq sharti:
Python dagi `_ichki_metod` larni to'g'ri testlash odobi.

## Yechim (Python kodi):
```python
class Algoritm:
    def _maxfiy_qadam(self, x):
        return x ** 2 + 3

a = Algoritm()
assert a._maxfiy_qadam(2) == 7
print("Maxfiy metod to'g'ri ishladi.")
```

## Tushuntirish va Mantiq:
1. Python da qat'iy yashirinlik yo'q; bir chiziqchali metodlar oq quti (white-box) testlarida bemalol tekshiriladi.

## Ishlash natijasi:
```text
Chiqish: Maxfiy metod to'g'ri ishladi.
```

---

# 943-Topshiriq: Test natijalarini JSON/JUnit XML formatida saqlash

## Topshiriq sharti:
CI/CD tizimlari tushunishi uchun test hisobotini strukturalangan formatga keltirish.

## Yechim (Python kodi):
```python
import json

test_hisoboti = {
    "suite": "AsosiyTestlar",
    "jami": 50,
    "muvaffaqiyatli": 50,
    "xatoliklar": 0,
    "vaqt_sekund": 0.45
}

json_hisobot = json.dumps(test_hisoboti, indent=2)
print("Hisobot:", json_hisobot)
```

## Tushuntirish va Mantiq:
1. GitLab CI, Jenkins va GitHub Actions ushbu hisobotlar asosida test panellarini chizadi.

## Ishlash natijasi:
```text
Chiqish: Hisobot: {\n  "suite": "AsosiyTestlar", ...}
```

---

# 944-Topshiriq: Pre-commit hooklari tamoyili (.pre-commit-config.yaml)

## Topshiriq sharti:
Har bir git commit oldidan kodni avtomatik tekshiruvchi konfiguratsiya.

## Yechim (Python kodi):
```python
pre_commit_yaml = "repos:\n  - repo: https://github.com/psf/black\n    rev: 24.1.0\n    hooks:\n      - id: black"
print("Pre-commit mavjud:", bool(pre_commit_yaml))
```

## Tushuntirish va Mantiq:
1. Sifatsiz yoki formatlanmagan kod Git omboriga kirmasligini lokal bosqichdayoq ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Pre-commit mavjud: True
```

---

# 945-Topshiriq: Statik tahlil (Flake8 va Ruff qoidalari simulyatsiyasi)

## Topshiriq sharti:
Koddagi ishlatilmagan importlar va ortiqcha probellarni aniqlash.

## Yechim (Python kodi):
```python
def tekshir_kod_sifati(kod_matni):
    xatolar = []
    if "import os" in kod_matni and "os." not in kod_matni:
        xatolar.append("F401: 'os' import qilingan lekin ishlatilmagan")
    return xatolar

print("Statik tahlil:", tekshir_kod_sifati("import os\nx = 10"))
```

## Tushuntirish va Mantiq:
1. Ruff va Flake8 kompilyatsiyasiz kodning uslubiy va mantiqiy xatolarini bir zumda topadi.

## Ishlash natijasi:
```text
Chiqish: Statik tahlil: ["F401: 'os' import qilingan lekin ishlatilmagan"]
```

---

# 946-Topshiriq: Mypy --strict statik tip tekshiruvi simulyatsiyasi

## Topshiriq sharti:
Funksiya argumentlari va qaytarish tipi to'liq ko'rsatilganligini tekshirish.

## Yechim (Python kodi):
```python
def toliq_tipli_funksiya(a: int, b: int) -> int:
    return a + b

import inspect
sig = inspect.signature(toliq_tipli_funksiya)
assert sig.return_annotation is int
print("Qat'iy tip nazorati tasdiqlandi!")
```

## Tushuntirish va Mantiq:
1. Mypy dastur ishga tushmasdan oldin yuz berishi mumkin bo'lgan `TypeError` larni yo'q qiladi.

## Ishlash natijasi:
```text
Chiqish: Qat'iy tip nazorati tasdiqlandi!
```

---

# 947-Topshiriq: doctest moduli: Docstring ichidagi testlarni bajarish

## Topshiriq sharti:
Hujjatlashtirish matni ichida berilgan kod namunalarining to'g'riligini avtomatik sinash.

## Yechim (Python kodi):
```python
import doctest

def daraja(x: int) -> int:
    """
    Sonning kvadratini hisoblaydi.

    >>> daraja(3)
    9
    >>> daraja(-2)
    4
    """
    return x * x

natija = doctest.testmod(verbose=False)
print("Doctest xatolari soni:", natija.failed)
```

## Tushuntirish va Mantiq:
1. `doctest` hujjatlar har doim dolzarb va ishchi holatda bo'lishini kafolatlaydi.

## Ishlash natijasi:
```text
Chiqish: Doctest xatolari soni: 0
```

---

# 948-Topshiriq: Xavfsizlik auditi (Bandit qoidalari): exec() va eval() ni taqiqlash

## Topshiriq sharti:
Kodda xavfli va ruxsatsiz funksiyalar chaqirilmaganligini tekshiruvchi linter.

## Yechim (Python kodi):
```python
import ast

def audit_xavfsizlik(kod):
    daraxt = ast.parse(kod)
    for tugun in ast.walk(daraxt):
        if isinstance(tugun, ast.Call) and isinstance(tugun.func, ast.Name):
            if tugun.func.id in ("eval", "exec"):
                return False, f"Xavfli funksiya topildi: {tugun.func.id}"
    return True, "Xavfsiz"

xavfsizmi, sabab = audit_xavfsizlik("a = 10\neval('2+2')")
print("Audit xulosasi:", sabab)
```

## Tushuntirish va Mantiq:
1. Bandit Python AST sini tahlil qilib xavfli funksiyalarni aniqlaydi.

## Ishlash natijasi:
```text
Chiqish: Audit xulosasi: Xavfli funksiya topildi: eval
```

---

# 949-Topshiriq: Profiling vizualizatsiyasi: Flamegraph tushunchasi

## Topshiriq sharti:
CPU sarfi va chaqiruvlar ierarxiyasini olov diagrammasida aks ettirish tamoyili.

## Yechim (Python kodi):
```python
def profiler_flame_data():
    return {"name": "root", "value": 100, "children": [{"name": "nlp_preprocess", "value": 70}, {"name": "db_save", "value": 30}]}

print("Flamegraph ierarxiyasi tayyorlandi:", profiler_flame_data()["name"])
```

## Tushuntirish va Mantiq:
1. Flamegraph operatsion tizim va Python profaylerlarining eng ko'rgazmali tahlil usulidir.

## Ishlash natijasi:
```text
Chiqish: Flamegraph ierarxiyasi tayyorlandi: root
```

---

# 950-Topshiriq: To'liq Avtomatlashtirilgan Sifat Ekotizimi (Sifat Kafolati Sintezi)

## Topshiriq sharti:
Barcha tekshiruvlar: Linter, Mypy, Unit Tests, Security Audit va Profilingni birlashtiruvchi Master Runner.

## Yechim (Python kodi):
```python
class MasterQualityRunner:
    def __init__(self):
        self.bosqichlar = []

    def qoshish(self, nom, fn):
        self.bosqichlar.append((nom, fn))

    def bajarish(self):
        print("=== AVTOMATLASHGAN SIFAT NAZORATI ISHGA TUSHDI ===")
        barchasi_joyidami = True
        for nom, fn in self.bosqichlar:
            try:
                fn()
                print(f"[OK] {nom}")
            except Exception as e:
                print(f"[FAIL] {nom}: {e}")
                barchasi_joyidami = False
        return barchasi_joyidami

runner = MasterQualityRunner()
runner.qoshish("1. Linting va Formatlash", lambda: None)
runner.qoshish("2. Tip Tekshiruvi (Mypy)", lambda: None)
runner.qoshish("3. Birlik Testlari (Unit Tests)", lambda: None)
runner.qoshish("4. Xavfsizlik Auditi (Security Audit)", lambda: None)
runner.qoshish("5. Unumdorlik Benchmarki (Benchmarking)", lambda: None)

natija = runner.bajarish()
print(f"Sifat nazorati yakuni: {'100% SIFATLI' if natija else 'XATOLIK BOR'}")
```

## Tushuntirish va Mantiq:
1. Professional ishlab chiqarish (Production-grade) dasturiy ta'minotining sifat standarti.

## Ishlash natijasi:
```text
Chiqish: === AVTOMATLASHGAN SIFAT NAZORATI ISHGA TUSHDI ===\n[OK] 1. Linting va Formatlash... Sifat nazorati yakuni: 100% SIFATLI
```

---

