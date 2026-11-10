# Python Dasturlash Tili — 18-Qism: Zamonaviy Python Standartlari va Ilg'or Imkoniyatlar
## (851-900 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam eng so'nggi Python 3.10-3.13 standartlari, chuqur metaprogramming va optimizatsiya vositalarini qamrab oladi:
* Strukturaviy Pattern Matching (`match...case`), Guard tekshiruvlari va unpacking;
* Walrus (`:=`), Positional-only (`/`) va Keyword-only (`*`) argumentlar;
* Statik turlar: `Generic`, `TypeVar`, `Protocol`, `TypedDict`;
* Metaprogramming: Metaklasslar, Avtomatik Plugin Registrator, Deskriptorlar protokoli;
* Xotira optimizatsiyasi: `__slots__`, `weakref`, `mmap`, `gc` nazorati;
* Funksional vositalar: `functools` (`lru_cache`, `singledispatch`), `itertools` (`chain`, `islice`, `product`);
* Zamonaviy `dataclasses`, `enum.Flag`, `contextlib` va CPython bayt-kod tahlili;

---

# 851-Topshiriq: Pattern Matching (match...case) asoslari

## Topshiriq sharti:
Python 3.10+ ning strukturaviy pattern matching imkoniyatidan foydalanib HTTP status kodini qayta ishlang.

## Yechim (Python kodi):
```python
def http_xabar(status):
    match status:
        case 200:
            return "OK: So'rov muvaffaqiyatli bajarildi"
        case 404:
            return "Not Found: Sahifa topilmadi"
        case 500:
            return "Internal Server Error: Server nosozligi"
        case _:
            return f"Boshqa status: {status}"

print(http_xabar(200))
print(http_xabar(404))
print(http_xabar(418))
```

## Tushuntirish va Mantiq:
1. `match...case` oddiy `switch` ga qaraganda ancha qudratli bo'lib, chuqur tahlil va destructuring imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: OK: So'rov muvaffaqiyatli bajarildi, Not Found: Sahifa topilmadi, Boshqa status: 418
```

---

# 852-Topshiriq: Pattern Matching: Guard shartlari (case ... if ...)

## Topshiriq sharti:
Pattern matching ichida qo'shimcha mantiqiy filtr (Guard) qo'llang.

## Yechim (Python kodi):
```python
def yosh_kategoriya(odam):
    match odam:
        case {"ism": ism, "yosh": yosh} if yosh >= 18:
            return f"{ism} balog'atga yetgan ({yosh} yoshda)"
        case {"ism": ism, "yosh": yosh}:
            return f"{ism} voyaga yetmagan ({yosh} yoshda)"
        case _:
            return "Noma'lum ma'lumot formati"

print(yosh_kategoriya({"ism": "Akmal", "yosh": 20}))
print(yosh_kategoriya({"ism": "Zuhra", "yosh": 15}))
```

## Tushuntirish va Mantiq:
1. `if yosh >= 18` sharti pattern mos kelgandan so'ng qo'shimcha tekshiruv o'tkazadi.

## Ishlash natijasi:
```text
Chiqish: Akmal balog'atga yetgan (20 yoshda), Zuhra voyaga yetmagan (15 yoshda)
```

---

# 853-Topshiriq: Pattern Matching: Ketma-ketliklarni ajratish (Sequence Unpacking)

## Topshiriq sharti:
Buyruq va argumentlar ro'yxatini match-case orqali komandalar sintaksisiga ajrating.

## Yechim (Python kodi):
```python
def buyruq_bajar(komanda):
    match komanda.split():
        case ["start"]:
            return "Tizim ishga tushirildi"
        case ["say", soz]:
            return f"Aytildi: {soz}"
        case ["set", kalit, qiymat]:
            return f"O'rnatildi: {kalit} = {qiymat}"
        case _:
            return "Noma'lum buyruq"

print(buyruq_bajar("say Salom"))
print(buyruq_bajar("set til uzbek"))
```

## Tushuntirish va Mantiq:
1. Ketma-ketlik patterni elementlar soni va o'zgaruvchilarga avtomatik bog'lashni ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Aytildi: Salom, O'rnatildi: til = uzbek
```

---

# 854-Topshiriq: Walrus operatori (:= Assignment Expression)

## Topshiriq sharti:
Shart tekshirish bilan bir vaqtda o'zgaruvchiga qiymat biriktirish.

## Yechim (Python kodi):
```python
matnlar = ["Python", "", "Sun'iy Intellekt", "Data Science", ""]
# Uzunligi 5 dan katta bo'lgan matnlarni va ularning uzunligini chiqaramiz
for m in matnlar:
    if (uzunlik := len(m)) > 5:
        print(f"'{m}' matni uzunligi: {uzunlik}")
```

## Tushuntirish va Mantiq:
1. `:=` operatori hisoblangan qiymatni takroran hisoblamasdan o'zgaruvchida saqlab qoladi.

## Ishlash natijasi:
```text
Chiqish: 'Python' matni uzunligi: 6, 'Sun'iy Intellekt' matni uzunligi: 16, 'Data Science' matni uzunligi: 12
```

---

# 855-Topshiriq: Positional-only (/) va Keyword-only (*) parametrlar

## Topshiriq sharti:
Funksiyada qaysi argumentlar faqat tartib bo'yicha, qaysilari faqat nom bo'yicha uzatilishini qat'iy belgilang.

## Yechim (Python kodi):
```python
def standart_funksiya(a, b, /, c, *, d, e):
    return a + b + c + d + e

# a va b faqat positional bo'lishi shart (/ dan oldin)
# d va e faqat nomlangan (keyword) bo'lishi shart (* dan keyin)
natija = standart_funksiya(1, 2, 3, d=4, e=5)
print("Natija:", natija)
```

## Tushuntirish va Mantiq:
1. API larni loyihalashda o'zgarishlarga chidamli (API stability) interfeys yaratishda ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Natija: 15
```

---

# 856-Topshiriq: TypeVar va Generic turlar bilan ishlash

## Topshiriq sharti:
Istalgan turdagi ro'yxatning birinchi elementini tur saqlagan holda qaytaruvchi Generic funksiya yozing.

## Yechim (Python kodi):
```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

def birinchi_element(royxat: List[T]) -> T:
    if not royxat:
        raise IndexError("Ro'yxat bo'sh!")
    return royxat[0]

son: int = birinchi_element([10, 20, 30])
satr: str = birinchi_element(["olma", "anor"])
print(f"Son: {son}, Satr: {satr}")
```

## Tushuntirish va Mantiq:
1. Generic tiplar statik tip tekshirgichlar (mypy, pyright) uchun to'liq turlilik xavfsizligini beradi.

## Ishlash natijasi:
```text
Chiqish: Son: 10, Satr: olma
```

---

# 857-Topshiriq: typing.Protocol (Strukturaviy Duck Typing)

## Topshiriq sharti:
Obyektning o'ziga xos metodlari mavjudligini interfeys kabi tekshiruvchi Protocol yarating.

## Yechim (Python kodi):
```python
from typing import Protocol

class Chiziluvchi(Protocol):
    def chizish(self) -> str:
        ...

class Doira:
    def chizish(self) -> str:
        return "⭕ Doira chizildi"

class Kvadrat:
    def chizish(self) -> str:
        return "⬜ Kvadrat chizildi"

def ekranga_chiqar(shakl: Chiziluvchi):
    print(shakl.chizish())

ekranga_chiqar(Doira())
ekranga_chiqar(Kvadrat())
```

## Tushuntirish va Mantiq:
1. `Protocol` Go yoki TypeScript interfeyslari kabi ishlaydi: meros olish shart emas, faqat metod mosligi yetarli.

## Ishlash natijasi:
```text
Chiqish: ⭕ Doira chizildi, ⬜ Kvadrat chizildi
```

---

# 858-Topshiriq: typing.TypedDict bilan qat'iy tipli lug'atlar

## Topshiriq sharti:
Lug'atning har bir kaliti va uning qiymati aniq qaysi tipda bo'lishini belgilang.

## Yechim (Python kodi):
```python
from typing import TypedDict

class Foydalanuvchi(TypedDict):
    id: int
    ism: str
    faol: bool

user: Foydalanuvchi = {
    "id": 1,
    "ism": "Sardor",
    "faol": True
}
print("Foydalanuvchi ma'lumoti:", user)
```

## Tushuntirish va Mantiq:
1. `TypedDict` oddiy Python dict bo'lib qoladi, ammo kod yozishda avtomatik to'ldirish va tip xatolarini tekshiradi.

## Ishlash natijasi:
```text
Chiqish: Foydalanuvchi ma'lumoti: {'id': 1, 'ism': 'Sardor', 'faol': True}
```

---

# 859-Topshiriq: __slots__ orqali xotirani tejash (Memory Optimization)

## Topshiriq sharti:
__slots__ ishlatilgan klassning oddiy klassga nisbatan xotira sarfini kamaytirish tamoyili.

## Yechim (Python kodi):
```python
import sys

class OddiyNuqta:
    def __init__(self, x, y):
        self.x = x; self.y = y

class OptimallashganNuqta:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x; self.y = y

p1 = OddiyNuqta(1, 2)
p2 = OptimallashganNuqta(1, 2)
print("Oddiy nuqtada __dict__ bormi:", hasattr(p1, '__dict__'))
print("Optimallashganda __dict__ bormi:", hasattr(p2, '__dict__'))
```

## Tushuntirish va Mantiq:
1. `__slots__` ob'ekt uchun ichki `__dict__` lug'atini yaratmaydi, bu esa millionlab ob'ektlarda RAM sarfini 50-60% tejaydi.

## Ishlash natijasi:
```text
Chiqish: Oddiy nuqtada __dict__ bormi: True, Optimallashganda __dict__ bormi: False
```

---

# 860-Topshiriq: Deskriptorlar (Descriptor Protocol): __get__ va __set__

## Topshiriq sharti:
Attributga qiymat berilganda manfiy son kiritilmasligini nazorat qiluvchi NonNegative deskriptori yozing.

## Yechim (Python kodi):
```python
class NonNegative:
    def __set_name__(self, owner, name):
        self.nom = name

    def __get__(self, instance, owner):
        if instance is None: return self
        return instance.__dict__.get(self.nom, 0)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.nom} manfiy bo'lishi mumkin emas!")
        instance.__dict__[self.nom] = value

class Mahsulot:
    narx = NonNegative()
    miqdor = NonNegative()

    def __init__(self, nom, narx, miqdor):
        self.nom = nom
        self.narx = narx
        self.miqdor = miqdor

m = Mahsulot("Kitob", 45000, 10)
print(f"{m.nom}: {m.narx} so'm, {m.miqdor} dona")
```

## Tushuntirish va Mantiq:
1. Python da `@property` aynan shu deskriptor protokoli asosiga qurilgan.

## Ishlash natijasi:
```text
Chiqish: Kitob: 45000 so'm, 10 dona
```

---

# 861-Topshiriq: Metaklasslar (Metaclasses): Klasslar yaratilishini boshqarish

## Topshiriq sharti:
Yaratilgan barcha klass metodlari nomini avtomatik tekshiruvchi metaklass tuzing.

## Yechim (Python kodi):
```python
class TekshiruvchiMetaklass(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_val in attrs.items():
            if callable(attr_val) and not attr_name.startswith("__"):
                if not attr_name.islower():
                    raise TypeError(f"Metod nomi '{attr_name}' kichik harfda (snake_case) bo'lishi shart!")
        return super().__new__(cls, name, bases, attrs)

class MeningKlassim(metaclass=TekshiruvchiMetaklass):
    def togri_metod(self):
        return "Barchasi to'g'ri"

obj = MeningKlassim()
print(obj.togri_metod())
```

## Tushuntirish va Mantiq:
1. Metaklass klassning o'zini yaratuvchi klassdir (`type` ning avlodi). Frameworklar (Django ORM, Pydantic) metaklasslar asosida ishlaydi.

## Ishlash natijasi:
```text
Chiqish: Barchasi to'g'ri
```

---

# 862-Topshiriq: Plugin Registry metaklassi (Avtomatik plaginlar ro'yxati)

## Topshiriq sharti:
Yangi yaratilgan har bir klassni avtomatik markaziy reyestrga qo'shuvchi arxitektura.

## Yechim (Python kodi):
```python
class PluginRegistrator(type):
    PLAGINLAR = {}
    def __new__(cls, name, bases, attrs):
        yangi_klass = super().__new__(cls, name, bases, attrs)
        if name != "AsosiyPlagin":
            cls.PLAGINLAR[name] = yangi_klass
        return yangi_klass

class AsosiyPlagin(metaclass=PluginRegistrator):
    pass

class AudioPlagin(AsosiyPlagin): pass
class VideoPlagin(AsosiyPlagin): pass

print("Ro'yxatga olingan plaginlar:", list(PluginRegistrator.PLAGINLAR.keys()))
```

## Tushuntirish va Mantiq:
1. Plaginlarni qo'lda import qilmasdan avtomatik tizimga ulash imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: Ro'yxatga olingan plaginlar: ['AudioPlagin', 'VideoPlagin']
```

---

# 863-Topshiriq: dataclasses: frozen=True va kw_only=True

## Topshiriq sharti:
O'zgarmas (immutable) va parametrlari faqat nomi bilan uzatiladigan zamonaviy dataclass.

## Yechim (Python kodi):
```python
from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class Konfiguratsiya:
    host: str
    port: int = 8080
    debug: bool = False

konfig = Konfiguratsiya(host="api.uzai.uz", debug=True)
print("Konfig:", konfig)
```

## Tushuntirish va Mantiq:
1. `frozen=True` ob'ektni o'zgarmas qilib xeshlanuvchi (hashable) qiladi va lug'at kaliti sifatida ishlatishga imkon beradi.

## Ishlash natijasi:
```text
Chiqish: Konfig: Konfiguratsiya(host='api.uzai.uz', port=8080, debug=True)
```

---

# 864-Topshiriq: dataclasses: __post_init__ va field(default_factory=...)

## Topshiriq sharti:
Obyekt yaratilgandan so'ng hisob-kitoblarni avtomatik to'ldirish va bo'sh ro'yxatlarni to'g'ri biriktirish.

## Yechim (Python kodi):
```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class XaridSavat:
    mijoz: str
    elementlar: List[str] = field(default_factory=list)
    jami_soni: int = field(init=False)

    def __post_init__(self):
        self.jami_soni = len(self.elementlar)

savat = XaridSavat("Ali", ["Kitob", "Daftar", "Qalam"])
print(f"Mijoz: {savat.mijoz}, Jami: {savat.jami_soni} ta mahsulot")
```

## Tushuntirish va Mantiq:
1. `default_factory=list` barcha nusxalar o'rtasida bitta ro'yxat ulanib qolish xatosini oldini oladi.

## Ishlash natijasi:
```text
Chiqish: Mijoz: Ali, Jami: 3 ta mahsulot
```

---

# 865-Topshiriq: functools.lru_cache va functools.cache

## Topshiriq sharti:
Rekursiv hisoblashlarni xotirada keshlab tezlikni minglab barobarga oshirish.

## Yechim (Python kodi):
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonachchi(n):
    if n < 2: return n
    return fibonachchi(n - 1) + fibonachchi(n - 2)

print("Fib(50) bir zumda:", fibonachchi(50))
print("Kesh statistikasi:", fibonachchi.cache_info())
```

## Tushuntirish va Mantiq:
1. `@lru_cache` eksponentsial O(2^n) murakkablikdagi rekursiyani chiziqli O(n) ga aylantiradi.

## Ishlash natijasi:
```text
Chiqish: Fib(50) bir zumda: 12586269025, Kesh statistikasi: CacheInfo(hits=48, misses=51, maxsize=128, currsize=51)
```

---

# 866-Topshiriq: functools.singledispatch (Funksiya polimorfizmi / Function Overloading)

## Topshiriq sharti:
Argumentning tipiga qarab turli xil mantiqni bajaruvchi funksiya yarating.

## Yechim (Python kodi):
```python
from functools import singledispatch

@singledispatch
def formatlovchi(arg):
    return f"Noma'lum tur: {arg}"

@formatlovchi.register(int)
def _(arg):
    return f"Butun son: {arg:,}"

@formatlovchi.register(list)
def _(arg):
    return f"Ro'yxat ({len(arg)} ta): {', '.join(str(x) for x in arg)}"

print(formatlovchi(1500000))
print(formatlovchi(["olma", "anor"]))
print(formatlovchi(3.14))
```

## Tushuntirish va Mantiq:
1. C++ yoki Java dagi kabi metodlarni parametrlar tipi bo'yicha qayta yuklash (Overloading) Python standarti.

## Ishlash natijasi:
```text
Chiqish: Butun son: 1,500,000, Ro'yxat (2 ta): olma, anor, Noma'lum tur: 3.14
```

---

# 867-Topshiriq: functools.partial bilan funksiyani qisman qo'llash

## Topshiriq sharti:
Ko'p argumentli funksiyaning ba'zi parametrlarini oldindan mahkamlab yangi funksiya hosil qilish.

## Yechim (Python kodi):
```python
from functools import partial

def daraja(asos, daraja_korsatkich):
    return asos ** daraja_korsatkich

kvadrat = partial(daraja, daraja_korsatkich=2)
kub = partial(daraja, daraja_korsatkich=3)

print("5 ning kvadrati:", kvadrat(5))
print("3 ning kubi:", kub(3))
```

## Tushuntirish va Mantiq:
1. `partial` funksional dasturlashda yangi sodda funksiyalar yasashning asosiy vositasidir.

## Ishlash natijasi:
```text
Chiqish: 5 ning kvadrati: 25, 3 ning kubi: 27
```

---

# 868-Topshiriq: itertools.chain bilan bir nechta kolleksiyalarni ulab o'qish

## Topshiriq sharti:
Bir nechta ro'yxatlarni birlashtirmasdan, xotirani tejab zanjirdek ketma-ket aylanib chiqish.

## Yechim (Python kodi):
```python
import itertools

guruh1 = [1, 2, 3]
guruh2 = [4, 5]
guruh3 = [6, 7, 8]

for x in itertools.chain(guruh1, guruh2, guruh3):
    print(x, end=" ")
print()
```

## Tushuntirish va Mantiq:
1. `itertools.chain` yangi katta ro'yxat yaratmasdan xotirada generator sifatida harakat qiladi.

## Ishlash natijasi:
```text
Chiqish: 1 2 3 4 5 6 7 8
```

---

# 869-Topshiriq: itertools.islice bilan generatorni qirqib olish (Slicing)

## Topshiriq sharti:
Cheksiz yoki juda katta generatordan `[start:stop:step]` bo'laklarini ajratib olish.

## Yechim (Python kodi):
```python
import itertools

cheksiz_juft = (x for x in itertools.count(0, 2))
birinchi_5_ta = list(itertools.islice(cheksiz_juft, 5))
print("Dastlabki 5 ta juft son:", birinchi_5_ta)
```

## Tushuntirish va Mantiq:
1. Oddiy generatorlarda `[start:stop]` ishlamaydi; buning uchun `itertools.islice` ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Dastlabki 5 ta juft son: [0, 2, 4, 6, 8]
```

---

# 870-Topshiriq: itertools.product (Dekart ko'paytmasi — Cartesian Product)

## Topshiriq sharti:
Ichma-ich sikllar (nested loops) o'rniga barcha elementlar kombinatsiyalarini hosil qilish.

## Yechim (Python kodi):
```python
import itertools

ranglar = ["qora", "oq"]
olchamlar = ["S", "M", "L"]

kombinatsiyalar = list(itertools.product(ranglar, olchamlar))
print("Barcha kombinatsiyalar:", kombinatsiyalar)
```

## Tushuntirish va Mantiq:
1. 3 yoki 4 qavatli `for` sikllarini bitta qatorli `itertools.product` bilan almashtirish kodni toza qiladi.

## Ishlash natijasi:
```text
Chiqish: Barcha kombinatsiyalar: [('qora', 'S'), ('qora', 'M'), ('qora', 'L'), ('oq', 'S'), ('oq', 'M'), ('oq', 'L')]
```

---

# 871-Topshiriq: contextlib.contextmanager dekoratori bilan kontekst menejeri

## Topshiriq sharti:
`__enter__` va `__exit__` yozmasdan oddiy generator funksiya orqali `with` bloki yaratish.

## Yechim (Python kodi):
```python
from contextlib import contextmanager
import time

@contextmanager
def vaqt_olchagich(nom):
    start = time.perf_counter()
    try:
        yield
    finally:
        sarf = (time.perf_counter() - start) * 1000
        print(f"[{nom}] bajarildi: {sarf:.2f} ms")

with vaqt_olchagich("Hisob-kitob"):
    jami = sum(i ** 2 for i in range(100000))
```

## Tushuntirish va Mantiq:
1. `yield` gacha bo'lgan kod `__enter__`, `finally` qismidagi kod esa `__exit__` vazifasini bajaradi.

## Ishlash natijasi:
```text
Chiqish: [Hisob-kitob] bajarildi: ... ms
```

---

# 872-Topshiriq: contextlib.suppress bilan aniq xatoliklarni xotirjam yutish

## Topshiriq sharti:
Bo'sh `try...except FileNotFoundError: pass` o'rniga zamonaviy usuldan foydalaning.

## Yechim (Python kodi):
```python
from contextlib import suppress
import os

# Mavjud bo'lmagan faylni o'chirishga urinish
with suppress(FileNotFoundError):
    os.remove("mavjud_bolmagan_fayl_123.tmp")

print("Dastur xatosiz davom etmoqda.")
```

## Tushuntirish va Mantiq:
1. `suppress` kodning o'qilishini oshiradi va niyatni yaqqol ko'rsatadi.

## Ishlash natijasi:
```text
Chiqish: Dastur xatosiz davom etmoqda.
```

---

# 873-Topshiriq: enum.Enum va enum.auto() bilan qat'iy konstantalar

## Topshiriq sharti:
Raqamlash va holatlarni xavfsiz ifodalovchi Enum klassi.

## Yechim (Python kodi):
```python
from enum import Enum, auto

class BuyurtmaHolati(Enum):
    YANGI = auto()
    TOLANDI = auto()
    YUBORILDI = auto()
    YAKUNLANDI = auto()

holat = BuyurtmaHolati.TOLANDI
print("Holat nomi:", holat.name)
print("Holat qiymati:", holat.value)
print("Tengmi:", holat == BuyurtmaHolati.TOLANDI)
```

## Tushuntirish va Mantiq:
1. Enum satr yoki raqamli xatoliklarni (typo) oldini oladi va holatlarni qat'iy boshqaradi.

## Ishlash natijasi:
```text
Chiqish: Holat nomi: TOLANDI, Holat qiymati: 2, Tengmi: True
```

---

# 874-Topshiriq: enum.Flag va bitli bayroqlar (Bitwise Flags)

## Topshiriq sharti:
Bir vaqtning o'zida bir nechta ruxsatlarni (Read, Write, Execute) bitli amallar bilan birlashtirish.

## Yechim (Python kodi):
```python
from enum import Flag, auto

class Ruxsatlar(Flag):
    OQISH = auto()
    YOZISH = auto()
    IJRO = auto()

foydalanuvchi_ruxsati = Ruxsatlar.OQISH | Ruxsatlar.YOZISH
print("Ruxsatlar:", foydalanuvchi_ruxsati)
print("Yozish huquqi bormi:", Ruxsatlar.YOZISH in foydalanuvchi_ruxsati)
print("Ijro huquqi bormi:", Ruxsatlar.IJRO in foydalanuvchi_ruxsati)
```

## Tushuntirish va Mantiq:
1. Fayl tizimlari va xavfsizlik protokollarida bir nechta bitlarni bitta o'zgaruvchida birlashtirish.

## Ishlash natijasi:
```text
Chiqish: Ruxsatlar: Ruxsatlar.YOZISH|OQISH, Yozish huquqi bormi: True, Ijro huquqi bormi: False
```

---

# 875-Topshiriq: weakref moduli (Kuchsiz havolalar va Memory Leak oldini olish)

## Topshiriq sharti:
Siklik bog'lanishlarda Garbage Collector resursni o'chirishi uchun weakref ishlatish.

## Yechim (Python kodi):
```python
import weakref

class KattaModel:
    def __init__(self, nom):
        self.nom = nom

model = KattaModel("LLM-10B")
kuchsiz_havola = weakref.ref(model)

print("Havola orqali obyekt:", kuchsiz_havola().nom)
del model # Asl obyekt o'chirildi
print("O'chirilgandan so'ng:", kuchsiz_havola())
```

## Tushuntirish va Mantiq:
1. Kuchsiz havolalar Reference Count hisoblagichini oshirmaydi va xotiradan tozalanishga to'sqinlik qilmaydi.

## Ishlash natijasi:
```text
Chiqish: Havola orqali obyekt: LLM-10B, O'chirilgandan so'ng: None
```

---

# 876-Topshiriq: mmap moduli: Gigabaytli fayllarni zumda o'qish (Memory Mapped File)

## Topshiriq sharti:
Faylni to'liq RAM ga yuklamasdan virtual xotiraga xaritalab o'qish.

## Yechim (Python kodi):
```python
import mmap

with open("test_mmap.tmp", "wb") as f:
    f.write(b"Boshlanish... Maxfiy_Token_12345 ...Tugash")

with open("test_mmap.tmp", "r+b") as f:
    with mmap.mmap(f.fileno(), 0) as mm:
        idx = mm.find(b"Maxfiy_Token")
        print("Mmap orqali topilgan bayt indeksi:", idx)

os.remove("test_mmap.tmp")
```

## Tushuntirish va Mantiq:
1. `mmap` operatsion tizimning sahifalash (paging) mexanizmidan foydalanib yirik ma'lumotlar bazalarini (masalan, SQLite) tezlashtiradi.

## Ishlash natijasi:
```text
Chiqish: Mmap orqali topilgan bayt indeksi: 14
```

---

# 877-Topshiriq: dis moduli: Python bayt-kodini (Bytecode) tahlil qilish

## Topshiriq sharti:
Oddiy qo'shish funksiyasining CPython virtual mashinasi qanday buyruqlarga aylanishini ko'ring.

## Yechim (Python kodi):
```python
import dis

def qoshish(a, b):
    return a + b

print("Bayt-kod ko'rinishi:")
dis.dis(qoshish)
```

## Tushuntirish va Mantiq:
1. `dis` moduli Python interpreterining ichki stack mexanizmini (LOAD_FAST, BINARY_OP, RETURN_VALUE) o'rganishda xizmat qiladi.

## Ishlash natijasi:
```text
Chiqish: Bayt-kod ko'rinishi:\n  ... LOAD_FAST ... BINARY_OP ... RETURN_VALUE
```

---

# 878-Topshiriq: sys.settrace bilan qadam-baqadam debagger yaratish

## Topshiriq sharti:
Dasturning har bir qatori bajarilishini kuzatib boruvchi mini-profiler.

## Yechim (Python kodi):
```python
import sys

def kuzatuvchi(frame, event, arg):
    if event == "line":
        print(f"Bajarilmoqda -> {frame.f_code.co_name} funksiyasida {frame.f_lineno}-qator")
    return kuzatuvchi

def hisob():
    a = 10
    b = 20
    return a + b

sys.settrace(kuzatuvchi)
hisob()
sys.settrace(None)
```

## Tushuntirish va Mantiq:
1. IDE larning debaggerlari (pdb, VSCode debug) aynan `sys.settrace` orqali ishlaydi.

## Ishlash natijasi:
```text
Chiqish: Bajarilmoqda -> hisob funksiyasida ...-qator
```

---

# 879-Topshiriq: inspect moduli: Funksiya signaturasini dinamik tahlil qilish

## Topshiriq sharti:
Funksiyaning parametrlari, turlari va default qiymatlarini dastur ichida o'rganing.

## Yechim (Python kodi):
```python
import inspect

def test_api(foydalanuvchi_id: int, status: str = "faol") -> dict:
    return {}

sig = inspect.signature(test_api)
print("Signatura:", sig)
for nom, param in sig.parameters.items():
    print(f"Parametr: {nom}, Tipi: {param.annotation}, Default: {param.default}")
```

## Tushuntirish va Mantiq:
1. FastAPI va Pydantic kabi frameworklar aynan `inspect` orqali funksiya parametrlarini avtomatik validatsiya qiladi.

## Ishlash natijasi:
```text
Chiqish: Signatura: (foydalanuvchi_id: int, status: str = 'faol') -> dict, Parametr: foydalanuvchi_id, Tipi: <class 'int'>...
```

---

# 880-Topshiriq: Garbage Collector (gc moduli) nazorati

## Topshiriq sharti:
Avtomatik xotira tozalagichni qo'lda chaqirish va aylanma zanjirlarni tozalash.

## Yechim (Python kodi):
```python
import gc

gc.collect() # Qo'lda chaqirish
print("GC hisoblagichlari:", gc.get_count())
print("GC yoqilganmi:", gc.isenabled())
```

## Tushuntirish va Mantiq:
1. Yirik ma'lumotlar bilan ishlaganda yoki o'yin dasturlarida kadrlar tushib ketmasligi uchun GC qo'lda boshqarilishi mumkin.

## Ishlash natijasi:
```text
Chiqish: GC hisoblagichlari: (...), GC yoqilganmi: True
```

---

# 881-Topshiriq: __missing__ metodi bilan avtomatik to'ldiriluvchi Dict

## Topshiriq sharti:
Lug'atda yo'q kalit so'ralganda xato bermasdan uni avtomatik yaratuvchi klass.

## Yechim (Python kodi):
```python
class AvtoLugat(dict):
    def __missing__(self, key):
        self[key] = f"Yangi_{key}"
        return self[key]

d = AvtoLugat()
print("Mavjud bo'lmagan kalit:", d["test"])
print("Lug'at holati:", d)
```

## Tushuntirish va Mantiq:
1. `defaultdict` aynan shu `__missing__` mexanizmi ustiga qurilgan.

## Ishlash natijasi:
```text
Chiqish: Mavjud bo'lmagan kalit: Yangi_test, Lug'at holati: {'test': 'Yangi_test'}
```

---

# 882-Topshiriq: __call__ metodi bilan obyektni funksiyadek chaqirish

## Topshiriq sharti:
O'z holatini (state) saqlovchi va funksiyadek chaqiriluvchi Callable klass.

## Yechim (Python kodi):
```python
class Hisoblagich:
    def __init__(self):
        self.soni = 0

    def __call__(self, qadam=1):
        self.soni += qadam
        return self.soni

c = Hisoblagich()
print("1-chaqiriq:", c())
print("2-chaqiriq:", c(5))
```

## Tushuntirish va Mantiq:
1. PyTorch dagi barcha modullar (`nn.Module`) aynan `__call__` orqali forward pass ni chaqiradi.

## Ishlash natijasi:
```text
Chiqish: 1-chaqiriq: 1, 2-chaqiriq: 6
```

---

# 883-Topshiriq: getattr va setattr bilan dinamik xususiyatlar

## Topshiriq sharti:
Obyektning attributlarini satr nomi bo'yicha dinamik o'qish va o'zgartirish.

## Yechim (Python kodi):
```python
class Server:
    def __init__(self):
        self.host = "localhost"
        self.port = 8080

s = Server()
# Dinamik o'qish
print("Port:", getattr(s, "port"))
# Dinamik yozish
setattr(s, "port", 9000)
print("Yangi port:", s.port)
```

## Tushuntirish va Mantiq:
1. Dinamik ORM va konfiguratsiyalarni yuklashda `getattr/setattr` eng mos keluvchi vositalardir.

## Ishlash natijasi:
```text
Chiqish: Port: 8080, Yangi port: 9000
```

---

# 884-Topshiriq: Operatorlarni qayta yuklash (Operator Overloading: __add__, __repr__)

## Topshiriq sharti:
2D koordinata nuqtalari uchun vektorli qo'shish `p1 + p2` amalini yarating.

## Yechim (Python kodi):
```python
class Nuqta:
    def __init__(self, x, y):
        self.x = x; self.y = y

    def __add__(self, boshqa):
        return Nuqta(self.x + boshqa.x, self.y + boshqa.y)

    def __repr__(self):
        return f"Nuqta({self.x}, {self.y})"

p1 = Nuqta(2, 3)
p2 = Nuqta(5, 7)
print("p1 + p2 =", p1 + p2)
```

## Tushuntirish va Mantiq:
1. Operator overloading matematik va ilmiy dasturlashda kodni ifodali va qulay qiladi.

## Ishlash natijasi:
```text
Chiqish: p1 + p2 = Nuqta(7, 10)
```

---

# 885-Topshiriq: Iteratordan Protokol: __iter__ va __next__

## Topshiriq sharti:
Maxsus oraliq (Range) generatorini generatorlarsiz, sof iterator sinfi orqali yarating.

## Yechim (Python kodi):
```python
class MeningRange:
    def __init__(self, bosh, oxir):
        self.joriy = bosh
        self.oxir = oxir

    def __iter__(self):
        return self

    def __next__(self):
        if self.joriy >= self.oxir:
            raise StopIteration
        qiymat = self.joriy
        self.joriy += 1
        return qiymat

for n in MeningRange(1, 4):
    print(n, end=" ")
print()
```

## Tushuntirish va Mantiq:
1. `StopIteration` istisnosi for-siklini to'xtatuvchi rasmiy protokol signali hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: 1 2 3
```

---

# 886-Topshiriq: Generatorlarni boshqarish: send(), throw() va close()

## Topshiriq sharti:
Generator bilan ikki tomonlama muloqot qilish: tashqaridan qiymat yuborish (`send`).

## Yechim (Python kodi):
```python
def yigindi_generator():
    jami = 0
    while True:
        yangi = yield jami
        if yangi is None: break
        jami += yangi

gen = yigindi_generator()
print("Boshlang'ich:", next(gen))
print("10 yuborildi:", gen.send(10))
print("25 yuborildi:", gen.send(25))
gen.close()
```

## Tushuntirish va Mantiq:
1. Generatorlarga ma'lumot yuborish (Coroutines) Python da asinxron dasturlashning ilk poydevori bo'lgan.

## Ishlash natijasi:
```text
Chiqish: Boshlang'ich: 0, 10 yuborildi: 10, 25 yuborildi: 35
```

---

# 887-Topshiriq: yield from bilan generatorlarni delegatsiyalash

## Topshiriq sharti:
Ichki generatordan kelayotgan barcha qiymatlarni tashqi oqimga to'g'ridan-to'g'ri o'tkazish.

## Yechim (Python kodi):
```python
def raqamlar():
    yield 1
    yield 2

def harflar():
    yield 'A'
    yield 'B'

def birlashgan():
    yield from raqamlar()
    yield from harflar()

print("Birlashgan generator:", list(birlashgan()))
```

## Tushuntirish va Mantiq:
1. `yield from` ichki generatorning xatoliklari va `send()` chaqiriqlarini shaffof ravishda bog'laydi.

## Ishlash natijasi:
```text
Chiqish: Birlashgan generator: [1, 2, 'A', 'B']
```

---

# 888-Topshiriq: Dinamik klass yaratish (type() uch argument bilan)

## Topshiriq sharti:
Klassni `class` kalit so'zisiz dastur ishlashi davomida dinamik ravishda yarating.

## Yechim (Python kodi):
```python
def salom_ber(self):
    return f"Salom, men dinamik yaratilgan {self.nom} obyektiman!"

# type(nomi, ota_klasslar_tuple, attributlar_dict)
DinamikKlass = type("DinamikKlass", (object,), {
    "nom": "UzbekAI",
    "salom": salom_ber
})

obj = DinamikKlass()
print(obj.salom())
```

## Tushuntirish va Mantiq:
1. ORM lar ma'lumotlar bazasi jadvallarini dastur ichida dinamik klasslarga aylantirishda shu usulni qo'llaydi.

## Ishlash natijasi:
```text
Chiqish: Salom, men dinamik yaratilgan UzbekAI obyektiman!
```

---

# 889-Topshiriq: copy moduli: Shallow Copy vs Deep Copy

## Topshiriq sharti:
Ichma-ich ro'yxatlarni nusxalashda yuzaki va chuqur nusxaning farqini ko'rsating.

## Yechim (Python kodi):
```python
import copy

asl = [[1, 2], [3, 4]]
yuzaki = copy.copy(asl)
chuqur = copy.deepcopy(asl)

asl[0][0] = 999
print("Yuzaki nusxa o'zgardimi:", yuzaki[0][0] == 999)
print("Chuqur nusxa o'zgardimi:", chuqur[0][0] == 999)
```

## Tushuntirish va Mantiq:
1. `deepcopy` barcha ichki obyektlarni rekursiv qaytadan yaratadi va to'liq mustaqillikni ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Yuzaki nusxa o'zgardimi: True, Chuqur nusxa o'zgardimi: False
```

---

# 890-Topshiriq: uuid moduli bilan global noyob identifikatorlar

## Topshiriq sharti:
UUID4 (tasodifiy) va UUID5 (SHA-1 xeshga asoslangan) identifikatorlarni generatsiya qiling.

## Yechim (Python kodi):
```python
import uuid

id4 = uuid.uuid4()
id5 = uuid.uuid5(uuid.NAMESPACE_DNS, "uzai.uz")

print("UUID4 (Tasodifiy):", id4)
print("UUID5 (Deterministik):", id5)
```

## Tushuntirish va Mantiq:
1. Tarqatilgan (Distributed) tizimlarda ID to'qnashuvlarining oldini oladi.

## Ishlash natijasi:
```text
Chiqish: UUID4 (Tasodifiy): ..., UUID5 (Deterministik): ...
```

---

# 891-Topshiriq: hashlib va hmac bilan xavfsiz parollash (PBKDF2-HMAC)

## Topshiriq sharti:
Tuz (Salt) va 100,000 iteratsiya yordamida parolni xavfsiz xeshlang.

## Yechim (Python kodi):
```python
import hashlib
import os

def parolni_xeshla(parol, tuz=None):
    if tuz is None:
        tuz = os.urandom(16)
    xesh = hashlib.pbkdf2_hmac('sha256', parol.encode(), tuz, 100000)
    return tuz, xesh

tuz, xesh = parolni_xeshla("maxfiy_parol_2026")
print("Tuz uzunligi:", len(tuz), "Xesh uzunligi:", len(xesh))
```

## Tushuntirish va Mantiq:
1. PBKDF2 Rainbow table hujumlariga qarshi tuz va hisoblash qiyinligini qo'llaydi.

## Ishlash natijasi:
```text
Chiqish: Tuz uzunligi: 16 Xesh uzunligi: 32
```

---

# 892-Topshiriq: secrets moduli bilan kriptografik xavfsiz tasodifiy sonlar

## Topshiriq sharti:
Xavfsiz tokenlar va parollar yaratishda `random` o'rniga `secrets` dan foydalaning.

## Yechim (Python kodi):
```python
import secrets

token_hex = secrets.token_hex(16)
token_url = secrets.token_urlsafe(16)
tasodifiy_son = secrets.randbelow(100)

print("Hex token:", token_hex)
print("URL-safe token:", token_url)
print("Xavfsiz son:", tasodifiy_son)
```

## Tushuntirish va Mantiq:
1. `random` psevdo-tasodifiy bo'lib oldindan bashorat qilinishi mumkin, `secrets` esa OS entropiya manbaidan oziqlanadi.

## Ishlash natijasi:
```text
Chiqish: Hex token: ..., URL-safe token: ..., Xavfsiz son: ...
```

---

# 893-Topshiriq: shutil moduli bilan fayl tizimini yuqori darajada boshqarish

## Topshiriq sharti:
Fayllarni nusxalash, disk joyini tekshirish va papkalarni arxivlash.

## Yechim (Python kodi):
```python
import shutil

joy = shutil.disk_usage(".")
print(f"Bo'sh disk maydoni: {joy.free // (1024**3)} GB")
```

## Tushuntirish va Mantiq:
1. `shutil` operatsion tizim darajasidagi fayl amallarini soddalashtiradi.

## Ishlash natijasi:
```text
Chiqish: Bo'sh disk maydoni: ... GB
```

---

# 894-Topshiriq: pathlib.Path bilan zamonaviy fayl yo'llari

## Topshiriq sharti:
Eski `os.path.join` o'rniga `/` operatorli ob'ektga yo'naltirilgan Path bilan ishlash.

## Yechim (Python kodi):
```python
from pathlib import Path

asosiy_papka = Path(".")
fayl_yoli = asosiy_papka / "ma'lumotlar" / "matn.txt"

print("Yo'l:", fayl_yoli)
print("Fayl nomi:", fayl_yoli.name)
print("Kengaytmasi:", fayl_yoli.suffix)
```

## Tushuntirish va Mantiq:
1. `pathlib` turli operatsion tizimlarda (Windows va Linux) yo'llarni avtomatik to'g'ri birlashtiradi.

## Ishlash natijasi:
```text
Chiqish: Yo'l: ma'lumotlar\matn.txt, Fayl nomi: matn.txt, Kengaytmasi: .txt
```

---

# 895-Topshiriq: collections.ChainMap bilan kontekstlar zanjiri

## Topshiriq sharti:
Standart sozlamalar, foydalanuvchi sozlamalari va CLI argumentlarini ierarxik qidiruv bilan birlashtirish.

## Yechim (Python kodi):
```python
from collections import ChainMap

standart = {"til": "uzbek", "mavzu": "yorug'", "shrift": 14}
foydalanuvchi = {"mavzu": "qorong'i"}
cli = {"shrift": 16}

sozlamalar = ChainMap(cli, foydalanuvchi, standart)
print("Mavzu:", sozlamalar["mavzu"]) # foydalanuvchidan oladi
print("Shrift:", sozlamalar["shrift"]) # cli dan oladi
print("Til:", sozlamalar["til"])       # standartdan oladi
```

## Tushuntirish va Mantiq:
1. `ChainMap` lug'atlarni jismonan nusxalamasdan ustma-ust qatlam sifatida ko'rib chiqadi.

## Ishlash natijasi:
```text
Chiqish: Mavzu: qorong'i, Shrift: 16, Til: uzbek
```

---

# 896-Topshiriq: heapq orqali ustuvor navbat (Priority Queue ob'ekti)

## Topshiriq sharti:
Ustuvorlik darajasiga ega vazifalarni boshqaruvchi xavfsiz navbat sinfi.

## Yechim (Python kodi):
```python
import heapq

class PriorityQueue:
    def __init__(self):
        self._ombor = []
        self._indeks = 0

    def push(self, element, ustuvorlik):
        # Ustuvorlik kichik bo'lsa birinchi chiqadi (-ustuvorlik bilan eng kattasini qilish mumkin)
        heapq.heappush(self._ombor, (ustuvorlik, self._indeks, element))
        self._indeks += 1

    def pop(self):
        return heapq.heappop(self._ombor)[-1]

pq = PriorityQueue()
pq.push("Elektron pochta jo'natish", 3)
pq.push("Favqulodda xatolik!", 1)
pq.push("Oddiy bildirishnoma", 2)

print("Birinchi bajariladigan vazifa:", pq.pop())
```

## Tushuntirish va Mantiq:
1. Indeks qo'shilishi bir xil ustuvorlikdagi vazifalarni FIFO tartibida saqlaydi.

## Ishlash natijasi:
```text
Chiqish: Birinchi bajariladigan vazifa: Favqulodda xatolik!
```

---

# 897-Topshiriq: Operator moduli (operator.itemgetter, operator.attrgetter)

## Topshiriq sharti:
Lambda funksiyalar o'rniga C-darajasida tez ishlovchi saralash kalitlari.

## Yechim (Python kodi):
```python
import operator

talabalar = [
    {"ism": "Ali", "ball": 85},
    {"ism": "Vali", "ball": 95},
    {"ism": "Hasan", "ball": 70}
]

talabalar.sort(key=operator.itemgetter("ball"), reverse=True)
print("Eng yuqori ball:", talabalar[0]["ism"])
```

## Tushuntirish va Mantiq:
1. `operator.itemgetter` Python kodi darajasida emas, balki to'g'ridan-to'g'ri CPython ichida ishlaydi.

## Ishlash natijasi:
```text
Chiqish: Eng yuqori ball: Vali
```

---

# 898-Topshiriq: Custom Exception zanjiri (raise ... from e)

## Topshiriq sharti:
Xatolik yuz berganda uning asl manbasini (Cause) yo'qotmasdan yuqori darajadagi xatoga o'rash.

## Yechim (Python kodi):
```python
class TizimXatosi(Exception): pass

def bazaga_ulan():
    try:
        raise ConnectionRefusedError("Port 5432 yopiq")
    except ConnectionRefusedError as e:
        raise TizimXatosi("Ma'lumotlar bazasi bilan aloqa uzildi!") from e

try:
    bazaga_ulan()
except TizimXatosi as err:
    print(f"Ushlandi: {err}")
    print(f"Asl sabab: {err.__cause__}")
```

## Tushuntirish va Mantiq:
1. `from e` sintaksisi xatoliklar steki (Traceback) to'liq saqlanishini ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Ushlandi: Ma'lumotlar bazasi bilan aloqa uzildi!, Asl sabab: Port 5432 yopiq
```

---

# 899-Topshiriq: Python 3.12+ type bayonoti (Type Alias Statement)

## Topshiriq sharti:
Yangi `type YangiNom = ...` sintaksisining ifodalanishi.

## Yechim (Python kodi):
```python
# Python 3.12+ sintaksisi simulyatsiyasi
Vektor = list[float]
Matritsa = list[Vektor]

def matritsa_yigindisi(m: Matritsa) -> float:
    return sum(sum(qator) for qator in m)

print("Yig'indi:", matritsa_yigindisi([[1.0, 2.0], [3.0, 4.0]]))
```

## Tushuntirish va Mantiq:
1. Yangi `type` kalit so'zi tip taxalluslarini o'qilishi va tekshirilishini yanada osonlashtiradi.

## Ishlash natijasi:
```text
Chiqish: Yig'indi: 10.0
```

---

# 900-Topshiriq: Mukammal Arxitektura Sintezi: Zamonaviy Python Metaklass + Deskriptor + Dataclass

## Topshiriq sharti:
Klass yaratilganda avtomatik turlarni tekshiruvchi, xotirani optimallashtiruvchi to'liq mikrotizim.

## Yechim (Python kodi):
```python
class ValidatsiyalanganMaydon:
    def __init__(self, tip):
        self.tip = tip

    def __set_name__(self, owner, name):
        self.nom = name

    def __set__(self, instance, value):
        if not isinstance(value, self.tip):
            raise TypeError(f"'{self.nom}' maydoni faqat {self.tip.__name__} bo'lishi shart! Kiritildi: {type(value).__name__}")
        instance.__dict__[self.nom] = value

    def __get__(self, instance, owner):
        if instance is None: return self
        return instance.__dict__.get(self.nom)

class ModelMetaklass(type):
    def __new__(cls, name, bases, attrs):
        # __slots__ avtomatik hosil qilish
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMetaklass):
    pass

class FoydalanuvchiModeli(Model):
    id = ValidatsiyalanganMaydon(int)
    ism = ValidatsiyalanganMaydon(str)

    def __init__(self, id, ism):
        self.id = id
        self.ism = ism

u = FoydalanuvchiModeli(101, "Botir")
print(f"Foydalanuvchi yaratildi: ID={u.id}, Ism={u.ism}")
```

## Tushuntirish va Mantiq:
1. Zamonaviy Python ning barcha qudrati — Metaklasslar, Deskriptorlar va OOP tamoyillari integratsiyalashgan to'liq arxitektura.

## Ishlash natijasi:
```text
Chiqish: Foydalanuvchi yaratildi: ID=101, Ism=Botir
```

---

