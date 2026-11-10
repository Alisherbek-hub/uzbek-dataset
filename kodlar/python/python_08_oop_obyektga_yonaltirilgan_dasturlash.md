# Python Dasturlash Tili — 8-Qism: Obyektga Yo'naltirilgan Dasturlash (OOP)
## (351-400 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam Obyektga Yo'naltirilgan Dasturlashning barcha asosiy va ilg'or tamoyillarini qamrab oladi:
* Klasslar va Ob'ektlar: `class`, `self`, `__init__`, instansiya va klass atributlari;
* Inkapsulyatsiya: public, protected (`_`), private (`__`), `@property` getter va setter;
* Vorislik (Inheritance) va Polimorfizm: `super()`, Method Overriding, MRO;
* Abstrakt klasslar: `abc.ABC`, `@abstractmethod`, interfeyslar;
* Dunder (sehrli) metodlar: `__str__`, `__repr__`, `__add__`, `__eq__`, `__len__`, `__getitem__`, `__call__`;
* Dizayn patternlari: Singleton, Observer, Command Pattern (Undo/Redo), Kompozitsiya, Dataclasses;

---

# 351-Topshiriq: Klass yaratish va __init__ konstruktori

## Topshiriq sharti:
Talaba haqidagi ma'lumotlarni saqlovchi va o'zini tanishtiruvchi `Talaba` klassini tuzing.

## Yechim (Python kodi):
```python
class Talaba:
    def __init__(self, ism, yosh, kurs):
        self.ism = ism
        self.yosh = yosh
        self.kurs = kurs

    def tanishtir(self):
        return f"Assalomu alaykum, mening ismim {self.ism}, yoshim {self.yosh} da, {self.kurs}-kurs talabasiman."

t1 = Talaba("Alisherbek", 17, 1)
t2 = Talaba("Madina", 19, 2)

print(t1.tanishtir())
print(t2.tanishtir())
```

## Tushuntirish va Mantiq:
1. `class` kalit so'zi yangi ma'lumot turini (klass) yaratadi.
2. `__init__` konstruktor metodi ob'ekt yaratilganda avtomatik ishga tushadi.
3. `self` joriy yaratilayotgan ob'ekt nusxasiga ishora qiladi.

## Ishlash natijasi:
```text
Chiqish: Assalomu alaykum, mening ismim Alisherbek, yoshim 17 da, 1-kurs talabasiman.
```


# 352-Topshiriq: Instansiya va Klass atributlari farqi

## Topshiriq sharti:
Barcha ob'ektlar uchun umumiy bo'lgan klass atributi va har bir ob'ektning o'ziga xos instansiya atributlarini ko'rsating.

## Yechim (Python kodi):
```python
class Xodim:
    kompaniya = "UzbekAI Texnologiyalari"  # Klass atributi (barcha xodimlar uchun bir xil)

    def __init__(self, ism, lavozim):
        self.ism = ism            # Instansiya atributi
        self.lavozim = lavozim    # Instansiya atributi

x1 = Xodim("Sardor", "Backend Dasturchi")
x2 = Xodim("Nilufar", "UI/UX Dizayner")

print(f"{x1.ism} ({x1.lavozim}) -> {x1.kompaniya}")
print(f"{x2.ism} ({x2.lavozim}) -> {x2.kompaniya}")
```

## Tushuntirish va Mantiq:
1. Klass atributi butun klass bo'yicha yagona xotira maydonida saqlanadi.
2. Instansiya atributlari esa har bir yangi ob'ekt uchun alohida shakllanadi.

## Ishlash natijasi:
```text
Chiqish: Sardor (Backend Dasturchi) -> UzbekAI Texnologiyalari...
```


# 353-Topshiriq: __str__ va __repr__ sehrli metodlari

## Topshiriq sharti:
Ob'ektni print() qilganda chiroyli o'qilishi (`__str__`) va ishlab chiquvchilar uchun aniq ko'rinishi (`__repr__`) ni ta'minlang.

## Yechim (Python kodi):
```python
class Kitob:
    def __init__(self, nom, muallif, narx):
        self.nom = nom
        self.muallif = muallif
        self.narx = narx

    def __str__(self):
        # Oddiy foydalanuvchi uchun chiroyli matn
        return f"'{self.nom}' — {self.muallif} ({self.narx:,} so'm)"

    def __repr__(self):
        # Ishlab chiquvchi va qayta tiklash uchun rasmiy ko'rinish
        return f"Kitob(nom='{self.nom}', muallif='{self.muallif}', narx={self.narx})"

k = Kitob("O'tkan kunlar", "Abdulla Qodiriy", 65000)

print("str() natijasi :", str(k))
print("repr() natijasi:", repr(k))
```

## Tushuntirish va Mantiq:
1. `__str__` `print(ob'ekt)` chaqirilganda ishlaydi.
2. `__repr__` ro'yxatlar ichida yoki dasturni tuzatishda (debugging) ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: str: 'O'tkan kunlar' — Abdulla Qodiriy (65,000 so'm), repr: Kitob(nom='...', muallif='...', narx=65000)
```


# 354-Topshiriq: Inkapsulyatsiya: Public, Protected va Private atributlar

## Topshiriq sharti:
Bank hisobi klassida himoyalangan (`_`) va yopiq xususiy (`__`) atributlar orqali ma'lumotlarni himoyalang.

## Yechim (Python kodi):
```python
class BankHisobi:
    def __init__(self, egasi, boshlangich_balans):
        self.egasi = egasi              # Public (ochiq)
        self._hisob_turi = "Jamg'arma"   # Protected (himoyalangan)
        self.__balans = boshlangich_balans  # Private (shaxsiy, yopiq)

    def depozit(self, summa):
        if summa > 0:
            self.__balans += summa
            print(f"{summa:,} so'm qabul qilindi.")

    def get_balans(self):
        return self.__balans

hisob = BankHisobi("Jasur", 500000)
print(f"Hisob egasi: {hisob.egasi}")
print(f"Joriy balans: {hisob.get_balans():,} so'm")

# Private atributga to'g'ridan-to'g'ri murojaat xatolik beradi
try:
    print(hisob.__balans)
except AttributeError as e:
    print("Private atributga to'g'ridan-to'g'ri kirish taqiqlangan!")
```

## Tushuntirish va Mantiq:
1. `__balans` nomi Python'da Name Mangling orqali `_BankHisobi__balans` ga aylanadi va to'g'ridan-to'g'ri o'zgartirishdan himoyalanadi.

## Ishlash natijasi:
```text
Chiqish: Hisob egasi: Jasur, Balans: 500,000 so'm, Private atributga kirish taqiqlangan!
```


# 355-Topshiriq: Getter va Setter: @property dekoratori

## Topshiriq sharti:
Harorat klassida Selsiy bo'yicha qiymat o'rnatilganda manfiy absolyut noldan (-273.15) past bo'lmasligini tekshiruvchi setter yozing.

## Yechim (Python kodi):
```python
class Harorat:
    def __init__(self, selsiy=0.0):
        self.selsiy = selsiy  # Setter orqali o'rnatiladi

    @property
    def selsiy(self):
        return self._selsiy

    @selsiy.setter
    def selsiy(self, qiymat):
        if qiymat < -273.15:
            raise ValueError("Harorat absolyut noldan (-273.15°C) past bo'lishi mumkin emas!")
        self._selsiy = qiymat

h = Harorat(25)
print(f"Harorat: {h.selsiy}°C")

h.selsiy = 36.6
print(f"Tana harorati: {h.selsiy}°C")

try:
    h.selsiy = -300
except ValueError as e:
    print(f"Xatolik ushlandi: {e}")
```

## Tushuntirish va Mantiq:
1. `@property` metodni atribut kabi o'qish imkonini beradi.
2. `@selsiy.setter` qiymat o'zgartirilganda validatsiya qoidalarini tekshiradi.

## Ishlash natijasi:
```text
Chiqish: Harorat: 25°C, Tana: 36.6°C, Xatolik: Harorat absolyut noldan...
```


# 356-Topshiriq: Vorislik (Inheritance) va super() metodi

## Topshiriq sharti:
Umumiy `Shaxs` klassidan meros oluvchi `Oqituvchi` klassini tuzing va `super()` orqali ota klass konstruktorini chaqiring.

## Yechim (Python kodi):
```python
class Shaxs:
    def __init__(self, ism, familiya):
        self.ism = ism
        self.familiya = familiya

    def toliq_ism(self):
        return f"{self.ism} {self.familiya}"

class Oqituvchi(Shaxs):
    def __init__(self, ism, familiya, fan, oylik):
        super().__init__(ism, familiya)  # Ota klass konstruktori
        self.fan = fan
        self.oylik = oylik

    def info(self):
        return f"{self.toliq_ism()} — {self.fan} fani o'qituvchisi (Oylik: {self.oylik:,} so'm)"

oqituvchi = Oqituvchi("Rustam", "Karimov", "Informatika", 8000000)
print(oqituvchi.info())
```

## Tushuntirish va Mantiq:
1. `class Bola(Ota):` vorislik hosil qiladi.
2. `super().__init__()` ota klassdagi barcha maydonlarni o'zlashtiradi.

## Ishlash natijasi:
```text
Chiqish: Rustam Karimov — Informatika fani o'qituvchisi (Oylik: 8,000,000 so'm)
```


# 357-Topshiriq: Polimorfizm va Metodlarni qayta aniqlash (Overriding)

## Topshiriq sharti:
Turli xil hayvonlar klassida umumiy `ovoz_chiqar()` metodini har bir hayvon uchun o'ziga xos tarzda qayta aniqlang.

## Yechim (Python kodi):
```python
class Hayvon:
    def ovoz_chiqar(self):
        raise NotImplementedError("Har bir hayvon o'z ovoziga ega bo'lishi kerak!")

class It(Hayvon):
    def ovoz_chiqar(self):
        return "Vov-vov!"

class Mushuk(Hayvon):
    def ovoz_chiqar(self):
        return "Miyov-miyov!"

class Sigir(Hayvon):
    def ovoz_chiqar(self):
        return "Moo-moo!"

hayvonlar = [It(), Mushuk(), Sigir()]

for h in hayvonlar:
    print(f"{h.__class__.__name__:8s} aytadi: {h.ovoz_chiqar()}")
```

## Tushuntirish va Mantiq:
1. Polimorfizm: bitta interfeys (`ovoz_chiqar()`) turli ob'ektlar tomonidan har xil amalga oshiriladi.

## Ishlash natijasi:
```text
Chiqish: It: Vov-vov!, Mushuk: Miyov-miyov!, Sigir: Moo-moo!
```


# 358-Topshiriq: Ko'p tomonlama vorislik (Multiple Inheritance) va MRO

## Topshiriq sharti:
Ikkita ota klassdan meros oluvchi bolaning metodlarni qidirish tartibini (`MRO`) ko'rsating.

## Yechim (Python kodi):
```python
class Uchuvchi:
    def uchish(self):
        return "Osmon bo'ylab uchmoqda..."

class Suzuvchi:
    def suzish(self):
        return "Suv tubida suzmoqda..."

class Ordaq(Uchuvchi, Suzuvchi):
    def qichqirish(self):
        return "G'a-g'a!"

ordak = Ordaq()
print(ordak.uchish())
print(ordak.suzish())
print(ordak.qichqirish())
print("MRO (Method Resolution Order):", [c.__name__ for c in Ordaq.__mro__])
```

## Tushuntirish va Mantiq:
1. Python bir nechta ota klasslardan bir vaqtda meros olish imkonini beradi.
2. `__mro__` atributi metodlar qaysi tartibda qidirilishini ko'rsatadi.

## Ishlash natijasi:
```text
Chiqish: Uchmoqda..., Suzmoqda..., MRO: ['Ordaq', 'Uchuvchi', 'Suzuvchi', 'object']
```


# 359-Topshiriq: Abstrakt Klasslar va Metodlar (abc moduli)

## Topshiriq sharti:
`abc.ABC` yordamida geometrik shakllar uchun majburiy `maydon()` va `perimetr()` metodlariga ega shablon klass tuzing.

## Yechim (Python kodi):
```python
from abc import ABC, abstractmethod
import math

class Shakl(ABC):
    @abstractmethod
    def maydon(self):
        pass

    @abstractmethod
    def perimetr(self):
        pass

class TogriTortburchak(Shakl):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def maydon(self):
        return self.a * self.b

    def perimetr(self):
        return 2 * (self.a + self.b)

class Doira(Shakl):
    def __init__(self, radius):
        self.radius = radius

    def maydon(self):
        return round(math.pi * (self.radius ** 2), 2)

    def perimetr(self):
        return round(2 * math.pi * self.radius, 2)

shakllar = [TogriTortburchak(4, 5), Doira(3)]
for s in shakllar:
    print(f"{s.__class__.__name__}: Maydon={s.maydon()}, Perimetr={s.perimetr()}")
```

## Tushuntirish va Mantiq:
1. Abstrakt klassdan to'g'ridan-to'g'ri ob'ekt olib bo'lmaydi.
2. Undan meros olgan har qanday klass barcha `@abstractmethod` metodlarini to'liq yozishi shart.

## Ishlash natijasi:
```text
Chiqish: TogriTortburchak: Maydon=20, Perimetr=18; Doira: Maydon=28.27, Perimetr=18.85
```


# 360-Topshiriq: Klass metodlari (@classmethod) va alternativ konstruktorlar

## Topshiriq sharti:
Matndan (masalan, 'Ali, 25') ob'ekt yaratuvchi alternativ konstruktorni `@classmethod` bilan dasturlang.

## Yechim (Python kodi):
```python
class Foydalanuvchi:
    def __init__(self, ism, yosh):
        self.ism = ism
        self.yosh = yosh

    @classmethod
    def satrdan_yarat(cls, satr):
        ism, yosh = satr.split(",")
        return cls(ism.strip(), int(yosh.strip()))

# Standart konstruktor
f1 = Foydalanuvchi("Vali", 30)

# Alternativ konstruktor (@classmethod)
f2 = Foydalanuvchi.satrdan_yarat("Hasan, 22")

print(f"1-foydalanuvchi: {f1.ism}, {f1.yosh} yoshda")
print(f"2-foydalanuvchi: {f2.ism}, {f2.yosh} yoshda")
```

## Tushuntirish va Mantiq:
1. `@classmethod` birinchi argument sifatida klassning o'zini (`cls`) qabul qiladi.
2. Bu turli formatdagi ma'lumotlardan (JSON, satr, fayl) ob'ekt yasashda ideal usuldir.

## Ishlash natijasi:
```text
Chiqish: Vali, 30 yoshda; Hasan, 22 yoshda
```


# 361-Topshiriq: Statik metodlar (@staticmethod)

## Topshiriq sharti:
Klass yoki instansiya holatiga bog'liq bo'lmagan, faqat yordamchi vazifani bajaruvchi `@staticmethod` funksiyasini tuzing.

## Yechim (Python kodi):
```python
class Matematika:
    @staticmethod
    def tubmi(n):
        if n <= 1: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: return False
        return True

    @staticmethod
    def kvadrat(x):
        return x * x

print("17 tub sonmi?", Matematika.tubmi(17))
print("20 tub sonmi?", Matematika.tubmi(20))
print("8 ning kvadrati:", Matematika.kvadrat(8))
```

## Tushuntirish va Mantiq:
1. `@staticmethod` na `self` va na `cls` argumentini qabul qiladi.
2. U klass ichida mantiqan guruhlangan oddiy funksiyadir.

## Ishlash natijasi:
```text
Chiqish: 17 tub sonmi? True, 20: False, Kvadrat: 64
```


# 362-Topshiriq: Operator Overloading: __add__ va __sub__

## Topshiriq sharti:
Ikki o'lchamli 2D koordinata vektorlarini `+` va `-` belgilari bilan to'g'ridan-to'g'ri qo'shish va ayirishni ta'minlang.

## Yechim (Python kodi):
```python
class Vektor2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, boshqa):
        return Vektor2D(self.x + boshqa.x, self.y + boshqa.y)

    def __sub__(self, boshqa):
        return Vektor2D(self.x - boshqa.x, self.y - boshqa.y)

    def __repr__(self):
        return f"Vektor2D({self.x}, {self.y})"

v1 = Vektor2D(3, 5)
v2 = Vektor2D(2, 4)

v3 = v1 + v2  # __add__ chaqiriladi
v4 = v1 - v2  # __sub__ chaqiriladi

print(f"{v1} + {v2} = {v3}")
print(f"{v1} - {v2} = {v4}")
```

## Tushuntirish va Mantiq:
1. `__add__` va `__sub__` dunder metodlari standart `+` va `-` operatorlarini o'z klassimiz uchun qayta aniqlashga (overload) imkon beradi.

## Ishlash natijasi:
```text
Chiqish: Vektor2D(3, 5) + Vektor2D(2, 4) = Vektor2D(5, 9)
```


# 363-Topshiriq: Taqqoslash metodlari: __eq__, __lt__, __gt__

## Topshiriq sharti:
Mahsulotlar narxi bo'yicha ularni `==`, `<`, `>` operatorlari bilan taqqoslanadigan qiling.

## Yechim (Python kodi):
```python
class Mahsulot:
    def __init__(self, nom, narx):
        self.nom = nom
        self.narx = narx

    def __eq__(self, boshqa):
        return self.narx == boshqa.narx

    def __lt__(self, boshqa):
        return self.narx < boshqa.narx

    def __repr__(self):
        return f"{self.nom}: {self.narx:,} so'm"

m1 = Mahsulot("Noutbuk", 8000000)
m2 = Mahsulot("Smartfon", 4000000)
m3 = Mahsulot("Planshet", 4000000)

print("m1 > m2 :", m1 > m2)
print("m2 == m3:", m2 == m3)

# Saralash avtomatik ishlaydi:
mahsulotlar = [m1, m2, m3]
print("Saralangan:", sorted(mahsulotlar))
```

## Tushuntirish va Mantiq:
1. `__lt__` (less than) ta'riflangan bo'lsa, Python'ning `sorted()` funksiyasi ushbu ob'ektlarni avtomatik saralay oladi.

## Ishlash natijasi:
```text
Chiqish: m1 > m2: True, m2 == m3: True, Saralangan: [Smartfon, Planshet, Noutbuk]
```


# 364-Topshiriq: Sehrli metod: __len__ va __getitem__

## Topshiriq sharti:
O'z klassimizga ro'yxat kabi indeks orqali murojaat qilish (`obj[0]`) va `len(obj)` imkoniyatini qo'shing.

## Yechim (Python kodi):
```python
class Guruh:
    def __init__(self, nom, talabalar):
        self.nom = nom
        self.talabalar = talabalar

    def __len__(self):
        return len(self.talabalar)

    def __getitem__(self, indeks):
        return self.talabalar[indeks]

g = Guruh("AI-2026", ["Alisher", "Madina", "Jasur", "Sardor"])

print(f"Guruhdagi talabalar soni: {len(g)} ta")
print(f"1-talaba: {g[0]}")
print(f"Oxirgi talaba: {g[-1]}")

# for tsiklida to'g'ridan-to'g'ri aylanadi:
for t in g:
    print(" -", t)
```

## Tushuntirish va Mantiq:
1. `__len__` `len()` funksiyasi bilan ulanadi.
2. `__getitem__` indekslash va for tsiklida avtomatik aylanishni ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Soni: 4 ta, 1-talaba: Alisher, Oxirgi: Sardor
```


# 365-Topshiriq: Sehrli metod: __call__ (Callable Objects)

## Topshiriq sharti:
Klass ob'ektini xuddi oddiy funksiya kabi qavslar bilan chaqiriladigan (`obj(x)`) qiling.

## Yechim (Python kodi):
```python
class DarajaHisoblagich:
    def __init__(self, daraja):
        self.daraja = daraja

    def __call__(self, son):
        return son ** self.daraja

kub = DarajaHisoblagich(3)
kvadrat = DarajaHisoblagich(2)

print("4 ning kubi    :", kub(4))        # ob'ekt funksiya kabi chaqirilmoqda!
print("9 ning kvadrati:", kvadrat(9))
```

## Tushuntirish va Mantiq:
1. `__call__` metodi ob'ektni funksional obyektga (Callable) aylantiradi.

## Ishlash natijasi:
```text
Chiqish: 4 ning kubi: 64, 9 ning kvadrati: 81
```


# 366-Topshiriq: Kontekst Menejeri: __enter__ va __exit__

## Topshiriq sharti:
`with` operatori bilan ishlovchi shaxsiy resurs boshqaruvchi (Timer context manager) klassini tuzing.

## Yechim (Python kodi):
```python
import time

class VaqtOlchagich:
    def __enter__(self):
        self.boshlanish = time.perf_counter()
        print("[START] Blok bajarilishi boshlandi...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sarflandi = time.perf_counter() - self.boshlanish
        print(f"[STOP] Blok {sarflandi:.5f} soniyada yakunlandi.")
        return False  # Xatoliklarni yutmasdan yuqoriga uzatish

with VaqtOlchagich():
    # Vaqt o'lchanadigan kod bloki
    yigindi = sum(i ** 2 for i in range(500_000))
    print("Yig'indi hisoblandi!")
```

## Tushuntirish va Mantiq:
1. `__enter__` with blokiga kirishda ishlaydi.
2. `__exit__` blok tugaganda (hatto xatolik yuz berganda ham) resurslarni tozalashni kafolatlaydi.

## Ishlash natijasi:
```text
Chiqish: [START]... Yig'indi hisoblandi!... [STOP] Blok 0.04... soniyada yakunlandi.
```


# 367-Topshiriq: __slots__ orqali xotirani tejash

## Topshiriq sharti:
Millionlab ob'ektlar yaratilganda RAM xotirani 40-50% tejovchi `__slots__` mexanizmini ko'rsating.

## Yechim (Python kodi):
```python
class NuqtaSlots:
    __slots__ = ('x', 'y')  # Faqat shu 2 ta atributga ruxsat beriladi, __dict__ yaratilmaydi

    def __init__(self, x, y):
        self.x = x
        self.y = y

n = NuqtaSlots(10, 20)
print(f"Nuqta: x={n.x}, y={n.y}")

try:
    n.z = 30  # Yangi dinamik atribut qo'shib bo'lmaydi
except AttributeError as e:
    print(f"Xatolik: {e}")
```

## Tushuntirish va Mantiq:
1. Standart klasslar har bir ob'ekt uchun ichki `__dict__` lug'atini ochadi, bu katta xotira oladi.
2. `__slots__` lug'at o'rniga qat'iy C-massiv strukturasi ishlatadi.

## Ishlash natijasi:
```text
Chiqish: Nuqta: x=10, y=20, Xatolik: 'NuqtaSlots' object has no attribute 'z'
```


# 368-Topshiriq: Kompozitsiya (Composition): Avtomobil va Dvigatel

## Topshiriq sharti:
Vorislik o'rniga kompozitsiya ('Has-A' munosabati) orqali Dvigatelni Avtomobil ichiga biriktiring.

## Yechim (Python kodi):
```python
class Dvigatel:
    def __init__(self, ot_kuchi, tur):
        self.ot_kuchi = ot_kuchi
        self.tur = tur

    def ishga_tushir(self):
        return f"{self.ot_kuchi} ot kuchiga ega {self.tur} dvigatel o't oldirildi!"

class Avtomobil:
    def __init__(self, model, dvigatel):
        self.model = model
        self.dvigatel = dvigatel  # Kompozitsiya: Avtomobil dvigatelga ega

    def haydash(self):
        print(f"{self.model} harakatga tayyorlanmoqda:")
        print(" ->", self.dvigatel.ishga_tushir())

motor = Dvigatel(150, "Turbo Benzin")
mashina = Avtomobil("Chevrolet Onix", motor)

mashina.haydash()
```

## Tushuntirish va Mantiq:
1. 'Composition over Inheritance' dasturiy ta'minot arxitekturasining asosiy qoidalaridan biridir.

## Ishlash natijasi:
```text
Chiqish: Chevrolet Onix harakatga tayyorlanmoqda: -> 150 ot kuchiga ega Turbo Benzin dvigatel o't oldirildi!
```


# 369-Topshiriq: Bank Hisobi klassi (Depozit, Yechish va Tranzaksiyalar)

## Topshiriq sharti:
Balansni boshqaruvchi, pul yetarli bo'lmaganda ogohlantiruvchi va barcha operatsiyalar tarixini yozib boruvchi to'liq bank hisobi klassi.

## Yechim (Python kodi):
```python
class BankAccount:
    def __init__(self, hisob_raqam, egasi, balans=0):
        self.hisob_raqam = hisob_raqam
        self.egasi = egasi
        self.balans = balans
        self.tarix = []

    def depozit(self, summa):
        if summa <= 0:
            print("Summa musbat bo'lishi kerak!")
            return
        self.balans += summa
        self.tarix.append(f"+{summa:,} so'm (Depozit)")
        print(f"{summa:,} so'm qo'shildi. Joriy balans: {self.balans:,} so'm")

    def yechish(self, summa):
        if summa > self.balans:
            print(f"XATOLIK: Balansda yetarli mablag' yo'q! (Mavjud: {self.balans:,} so'm)")
            return False
        self.balans -= summa
        self.tarix.append(f"-{summa:,} so'm (Yechib olindi)")
        print(f"{summa:,} so'm yechildi. Qolgan balans: {self.balans:,} so'm")
        return True

    def hisobot(self):
        print(f"\n--- {self.egasi} ({self.hisob_raqam}) HISOB VARAQASI ---")
        for qadam in self.tarix:
            print(" *", qadam)
        print(f"YAKUNIY BALANS: {self.balans:,} so'm")

hisob = BankAccount("UZ86001122", "Alisherbek", 1000000)
hisob.depozit(500000)
hisob.yechish(300000)
hisob.yechish(2000000)  # Yetarli emas
hisob.hisobot()
```

## Tushuntirish va Mantiq:
1. Real bank tizimlari kabi operatsiyalar tekshiriladi va xavfsiz balans yuritiladi.

## Ishlash natijasi:
```text
Chiqish: Depozit, Yechish, Xatolik va Yakuniy hisobot ko'rinishi.
```


# 370-Topshiriq: Kutubxona boshqaruv tizimi (Library va Book)

## Topshiriq sharti:
Kitoblarni qidirish, kitobxonga berish va qaytarish funksiyalariga ega to'liq kutubxona tizimi.

## Yechim (Python kodi):
```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True

    def __repr__(self):
        holat = "Mavjud" if self.is_available else "Ijarada"
        return f"'{self.title}' ({self.author}) - [{holat}]"

class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def borrow_book(self, title):
        for b in self.books:
            if b.title.lower() == title.lower():
                if b.is_available:
                    b.is_available = False
                    print(f"Kitob berildi: '{b.title}'")
                    return True
                else:
                    print(f"Kechirasiz, '{b.title}' hozir ijarada!")
                    return False
        print(f"Kutubxonada '{title}' kitobi topilmadi!")
        return False

lib = Library("Alisher Navoiy Milliy Kutubxonasi")
lib.add_book(Book("O'tkan kunlar", "Abdulla Qodiriy"))
lib.add_book(Book("Yulduzli tunlar", "Pirimqul Qodirov"))

lib.borrow_book("O'tkan kunlar")
lib.borrow_book("O'tkan kunlar")  # 2-marta so'ralganda band
```

## Tushuntirish va Mantiq:
1. Kutubxona klassi Book ob'ektlarining ro'yxatini boshqaradi.

## Ishlash natijasi:
```text
Chiqish: Kitob berildi: 'O'tkan kunlar', Kechirasiz, kitob hozir ijarada!
```


# 371-Topshiriq: dataclass dan foydalanish (Python 3.7+)

## Topshiriq sharti:
`@dataclass` orqali `__init__`, `__repr__`, `__eq__` metodlarini qo'lda yozmasdan avtomatik hosil qiling.

## Yechim (Python kodi):
```python
from dataclasses import dataclass

@dataclass
class MahsulotData:
    nom: str
    narx: float
    miqdor: int = 1

    def jami_qiymat(self) -> float:
        return self.narx * self.miqdor

p1 = MahsulotData("Monitor", 2500000.0, 2)
p2 = MahsulotData("Monitor", 2500000.0, 2)

print("Ob'ekt ko'rinishi:", p1)
print("Ikkita ob'ekt tengmi?", p1 == p2)  # __eq__ avtomatik ishlaydi!
print("Jami qiymati:", p1.jami_qiymat())
```

## Tushuntirish va Mantiq:
1. `@dataclass` boilerplate (ortiqcha bir xil) kodlarni 80% ga qisqartiradi.

## Ishlash natijasi:
```text
Chiqish: MahsulotData(nom='Monitor', narx=2500000.0, miqdor=2), Tengmi: True
```


# 372-Topshiriq: Muzlatilgan Data Class (frozen=True)

## Topshiriq sharti:
O'zgarmas (immutable) va lug'at kaliti bo'la oladigan xavfsiz dataclass yarating.

## Yechim (Python kodi):
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Koordinata:
    kenglik: float
    uzunlik: float

toshkent = Koordinata(41.2995, 69.2401)
print(f"Toshkent: {toshkent}")

try:
    toshkent.kenglik = 42.0  # O'zgartirib bo'lmaydi
except Exception as e:
    print(f"Xatolik ushlandi: {e}")
```

## Tushuntirish va Mantiq:
1. `frozen=True` ob'ekt xossalarini read-only qiladi va unga `__hash__` metodini beradi.

## Ishlash natijasi:
```text
Chiqish: Toshkent: Koordinata(...), Xatolik: cannot assign to field 'kenglik'
```


# 373-Topshiriq: Sanab o'tiluvchi turlar (enum.Enum)

## Topshiriq sharti:
Buyurtma holatlarini xatoliklarsiz boshqarish uchun `Enum` klassidan foydalaning.

## Yechim (Python kodi):
```python
from enum import Enum

class BuyurtmaHolati(Enum):
    KUTILMOQDA = "pending"
    TOLANDI = "paid"
    YUBORILDI = "shipped"
    YETKAZILDI = "delivered"
    BEKOR_QILINDI = "cancelled"

class Buyurtma:
    def __init__(self, id, summa):
        self.id = id
        self.summa = summa
        self.holat = BuyurtmaHolati.KUTILMOQDA

    def tolov_qilish(self):
        self.holat = BuyurtmaHolati.TOLANDI
        print(f"Buyurtma #{self.id} to'landi!")

b = Buyurtma(501, 450000)
print(f"Boshlang'ich holat: {b.holat.value}")
b.tolov_qilish()
print(f"Yangi holat: {b.holat.name} ({b.holat.value})")
```

## Tushuntirish va Mantiq:
1. `Enum` imlo xatolarining ('paidd', 'payed') oldini oladi va kod xavfsizligini kafolatlaydi.

## Ishlash natijasi:
```text
Chiqish: Boshlang'ich: pending, Buyurtma to'landi!, Yangi holat: TOLANDI (paid)
```


# 374-Topshiriq: Singleton Dizayn Patterni

## Topshiriq sharti:
Dastur davomida faqat va faqat bitta nusxasi mavjud bo'ladigan Ma'lumotlar Bazasi ulanishi klassini tuzing.

## Yechim (Python kodi):
```python
class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("[INFO] Yangi ma'lumotlar bazasi ulanishi yaratildi.")
            cls._instance = super().__new__(cls)
        return cls._instance

db1 = DatabaseConnection()
db2 = DatabaseConnection()

print("db1 va db2 bitta ob'ektmi?", db1 is db2)
```

## Tushuntirish va Mantiq:
1. `__new__` metodi ob'ekt xotirada yaratilishini boshqaradi.
2. Agar nusxa allaqachon mavjud bo'lsa, mavjud nusxani qaytaradi.

## Ishlash natijasi:
```text
Chiqish: Yangi ulanish yaratildi (faqat 1 marta!), db1 is db2: True
```


# 375-Topshiriq: Shaxsiy Istisno (Custom Exception) klassi

## Topshiriq sharti:
Mablag' yetarli bo'lmaganda chaqiriluvchi `MablagYetarliEmasXatosi` nomli shaxsiy xatolik klassini tuzing.

## Yechim (Python kodi):
```python
class MablagYetarliEmasXatosi(Exception):
    def __init__(self, yetishmayotgan):
        self.yetishmayotgan = yetishmayotgan
        super().__init__(f"Yetarli mablag' mavjud emas! Yetishmayapti: {yetishmayotgan:,} so'm")

def pul_yech(balans, miqdor):
    if miqdor > balans:
        raise MablagYetarliEmasXatosi(miqdor - balans)
    return balans - miqdor

try:
    pul_yech(50000, 120000)
except MablagYetarliEmasXatosi as e:
    print(f"Xatolik ushlandi: {e}")
```

## Tushuntirish va Mantiq:
1. `Exception` klassidan meros olib shaxsiy xatoliklar (Domain Exceptions) yaratiladi.

## Ishlash natijasi:
```text
Chiqish: Xatolik ushlandi: Yetarli mablag' mavjud emas! Yetishmayapti: 70,000 so'm
```


# 376-Topshiriq: Observer (Kuzatuvchi) dizayn patterni

## Topshiriq sharti:
Kanalga yangi video yuklanganda barcha obunachilarga avtomatik xabar yuboruvchi kuzatuvchi tizimi.

## Yechim (Python kodi):
```python
class YouTubeKanal:
    def __init__(self, nom):
        self.nom = nom
        self.obunachilar = []

    def obuna_bol(self, foydalanuvchi):
        self.obunachilar.append(foydalanuvchi)

    def yangi_video_chiqar(self, video_nomi):
        print(f"\n[{self.nom}] Yangi video yuklandi: '{video_nomi}'")
        for obunachi in self.obunachilar:
            obunachi.bildirishnoma_ol(self.nom, video_nomi)

class Obunachi:
    def __init__(self, ism):
        self.ism = ism

    def bildirishnoma_ol(self, kanal_nomi, video):
        print(f" -> Xabar {self.ism}ga yetib bordi: {kanal_nomi} kanalida '{video}' chiqdi!")

kanal = YouTubeKanal("Python Uz")
u1 = Obunachi("Alisher")
u2 = Obunachi("Jasur")

kanal.obuna_bol(u1)
kanal.obuna_bol(u2)

kanal.yangi_video_chiqar("Sun'iy intellekt 2.0 darsi")
```

## Tushuntirish va Mantiq:
1. Observer pattern hodisalarga asoslangan arxitekturaning (Event-Driven) asosidir.

## Ishlash natijasi:
```text
Chiqish: Yangi video chiqdi, ikkala obunachiga ham xabar yetkazildi.
```


# 377-Topshiriq: Stek (Stack - LIFO) ma'lumotlar tuzilmasi klassi

## Topshiriq sharti:
Klass yordamida `push`, `pop`, `peek`, `is_empty` metodlariga ega LIFO stekini dasturlang.

## Yechim (Python kodi):
```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, element):
        self._items.append(element)

    def pop(self):
        if self.is_empty():
            raise IndexError("Bo'sh stekdan element sug'urib bo'lmaydi!")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if not self.is_empty() else None

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

s = Stack()
s.push("Kitob 1")
s.push("Kitob 2")
s.push("Kitob 3")

print("Eng yuqoridagi:", s.peek())
print("Sug'urilgan   :", s.pop())
print("Yangi yuqori  :", s.peek())
```

## Tushuntirish va Mantiq:
1. LIFO (Last In, First Out) oxirgi kirgan element birinchi bo'lib chiqadi.

## Ishlash natijasi:
```text
Chiqish: Yuqoridagi: Kitob 3, Sug'urilgan: Kitob 3, Yangi yuqori: Kitob 2
```


# 378-Topshiriq: Navbat (Queue - FIFO) ma'lumotlar tuzilmasi klassi

## Topshiriq sharti:
Kassadagi navbat kabi birinchi kelgan birinchi ketadigan (`FIFO`) navbat klassi.

## Yechim (Python kodi):
```python
from collections import deque

class Queue:
    def __init__(self):
        self._elementlar = deque()

    def enqueue(self, element):
        self._elementlar.append(element)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Bo'sh navbatdan element olib bo'lmaydi!")
        return self._elementlar.popleft()

    def is_empty(self):
        return len(self._elementlar) == 0

q = Queue()
q.enqueue("1-mijoz: Ali")
q.enqueue("2-mijoz: Vali")
q.enqueue("3-mijoz: G'ani")

print("Xizmat ko'rsatildi:", q.dequeue())
print("Xizmat ko'rsatildi:", q.dequeue())
```

## Tushuntirish va Mantiq:
1. `collections.deque` boshidan element olishni O(1) vaqtda tezkor bajaradi.

## Ishlash natijasi:
```text
Chiqish: 1-mijoz: Ali, 2-mijoz: Vali
```


# 379-Topshiriq: Bog'langan Ro'yxat (Singly Linked List) klassi

## Topshiriq sharti:
Tugunlar (Node) zanjiridan iborat bitta yo'nalishli bog'langan ro'yxatni dasturlang.

## Yechim (Python kodi):
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        yangi = Node(data)
        if not self.head:
            self.head = yangi
            return
        oxiri = self.head
        while oxiri.next:
            oxiri = oxiri.next
        oxiri.next = yangi

    def chop_et(self):
        joriy = self.head
        elementlar = []
        while joriy:
            elementlar.append(str(joriy.data))
            joriy = joriy.next
        print(" -> ".join(elementlar) + " -> None")

ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
ll.chop_et()
```

## Tushuntirish va Mantiq:
1. Har bir tugun o'z qiymatini va keyingi tugunning xotira manzilini (`next`) saqlaydi.

## Ishlash natijasi:
```text
Chiqish: 10 -> 20 -> 30 -> None
```


# 380-Topshiriq: Mini RPG O'yin: Qahramonlar jangi

## Topshiriq sharti:
Polimorfizm va vorislikka asoslangan Warrior va Mage qahramonlarining jang simulyatsiyasi.

## Yechim (Python kodi):
```python
class Qahramon:
    def __init__(self, nom, jon, kuch):
        self.nom = nom
        self.jon = jon
        self.kuch = kuch

    def hujum(self, raqib):
        zarar = self.kuch
        raqib.jon -= zarar
        print(f"{self.nom} {raqib.nom}ga hujum qildi ({zarar} zarar). {raqib.nom} joni: {max(0, raqib.jon)}")

class Jangchi(Qahramon):
    def hujum(self, raqib):
        # Qilich bilan kuchaytirilgan zarba
        zarar = self.kuch + 5
        raqib.jon -= zarar
        print(f"🗡️ Jangchi {self.nom} qattiq zarba berdi! ({zarar} zarar). {raqib.nom} joni: {max(0, raqib.jon)}")

class Sehrgar(Qahramon):
    def hujum(self, raqib):
        # Olovli to'p sehri
        zarar = self.kuch * 2
        raqib.jon -= zarar
        print(f"🔥 Sehrgar {self.nom} olovli to'p otdi! ({zarar} zarar). {raqib.nom} joni: {max(0, raqib.jon)}")

j = Jangchi("Temur", jon=100, kuch=15)
s = Sehrgar("Merlin", jon=80, kuch=12)

j.hujum(s)
s.hujum(j)
```

## Tushuntirish va Mantiq:
1. Vorislik orqali umumiy xususiyatlar olinadi va polimorfik `hujum` metodi bilan o'ziga xos zarba beriladi.

## Ishlash natijasi:
```text
Chiqish: 🗡️ Jangchi Temur zarba berdi... 🔥 Sehrgar Merlin olovli to'p otdi...
```


# 381-Topshiriq: Iterator klassi yaratish: __iter__ va __next__

## Topshiriq sharti:
Berilgan sonlar oralig'ida kvadratlarni ketma-ket qaytaruvchi shaxsiy iterator klassi tuzing.

## Yechim (Python kodi):
```python
class KvadratlarIteratori:
    def __init__(self, maksimal):
        self.maksimal = maksimal
        self.joriy = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.joriy > self.maksimal:
            raise StopIteration
        natija = self.joriy ** 2
        self.joriy += 1
        return natija

kv = KvadratlarIteratori(5)
for k in kv:
    print(k, end=" ")
print()
```

## Tushuntirish va Mantiq:
1. `StopIteration` iteratsiya tugaganini for tsikliga bildiradi.

## Ishlash natijasi:
```text
Chiqish: 1 4 9 16 25
```


# 382-Topshiriq: getattr() va setattr() bilan dinamik atributlar

## Topshiriq sharti:
Atribut nomlari satr shaklida berilganda ularni dinamik o'qish va yozishni amalga oshiring.

## Yechim (Python kodi):
```python
class Avto:
    def __init__(self, model):
        self.model = model

m = Avto("Malibu")

# Dinamik o'qish
print("Model:", getattr(m, "model"))

# Dinamik yozish
setattr(m, "rang", "Qora")
print("Yangi qo'shilgan rang:", getattr(m, "rang"))
print("Mavjud bo'lmagan atribut:", getattr(m, "narx", "Ko'rsatilmagan"))
```

## Tushuntirish va Mantiq:
1. ORM (masalan, Django ORM, SQLAlchemy) dinamik ma'lumotlar bazasi ustunlarini boshqarishda `getattr/setattr` dan foydalanadi.

## Ishlash natijasi:
```text
Chiqish: Model: Malibu, Rang: Qora, Narx: Ko'rsatilmagan
```


# 383-Topshiriq: Termostat klassi: Selsiy va Farengeyt o'rtasida konvertatsiya

## Topshiriq sharti:
Qaysi birlikda kiritilsa ham ichida Selsiyda saqlovchi va xohlagan birlikda qaytaruvchi aqlli termostat.

## Yechim (Python kodi):
```python
class Termostat:
    def __init__(self, selsiy=20.0):
        self._selsiy = float(selsiy)

    @property
    def selsiy(self):
        return round(self._selsiy, 2)

    @selsiy.setter
    def selsiy(self, q):
        self._selsiy = float(q)

    @property
    def farengeyt(self):
        return round(self._selsiy * 9 / 5 + 32, 2)

    @farengeyt.setter
    def farengeyt(self, q):
        self._selsiy = (float(q) - 32) * 5 / 9

t = Termostat(25)
print(f"Selsiy: {t.selsiy}°C  |  Farengeyt: {t.farengeyt}°F")

t.farengeyt = 86  # Farengeytda o'rnatamiz
print(f"Yangilangan Selsiy: {t.selsiy}°C  |  Farengeyt: {t.farengeyt}°F")
```

## Tushuntirish va Mantiq:
1. Ikkita bog'liq xususiyat o'rtasidagi avtomatik hisob-kitobni `@property` yordamida nafis yechish.

## Ishlash natijasi:
```text
Chiqish: Selsiy: 25.0°C | Farengeyt: 77.0°F -> Yangilangan Selsiy: 30.0°C
```


# 384-Topshiriq: Valyuta summasi klassi (Money Class)

## Topshiriq sharti:
Valyuta miqdori va kodini saqlovchi, faqat bir xil valyutadagi pullarni qo'shishga ruxsat beruvchi klass.

## Yechim (Python kodi):
```python
class Pul:
    def __init__(self, miqdor, valyuta="UZS"):
        self.miqdor = miqdor
        self.valyuta = valyuta

    def __add__(self, boshqa):
        if self.valyuta != boshqa.valyuta:
            raise ValueError(f"Har xil valyutalarni ({self.valyuta} va {boshqa.valyuta}) to'g'ridan-to'g'ri qo'shib bo'lmaydi!")
        return Pul(self.miqdor + boshqa.miqdor, self.valyuta)

    def __repr__(self):
        return f"{self.miqdor:,} {self.valyuta}"

p1 = Pul(50000, "UZS")
p2 = Pul(75000, "UZS")
p3 = p1 + p2

print("Natija:", p3)
```

## Tushuntirish va Mantiq:
1. Domen modeli orqali moliya xatoliklarining (Dollar va So'mni adashib qo'shib yuborish) oldi olinadi.

## Ishlash natijasi:
```text
Chiqish: 125,000 UZS
```


# 385-Topshiriq: Mehmonxona xonalari band qilish tizimi

## Topshiriq sharti:
Xonalarning raqami, narxi va bandlik holatini kuzatib boruvchi Mehmonxona klassi.

## Yechim (Python kodi):
```python
class Xona:
    def __init__(self, raqam, narx):
        self.raqam = raqam
        self.narx = narx
        self.bandmi = False

class Mehmonxona:
    def __init__(self, nom):
        self.nom = nom
        self.xonalar = []

    def xona_qosh(self, xona):
        self.xonalar.append(xona)

    def band_qilish(self, raqam):
        for x in self.xonalar:
            if x.raqam == raqam:
                if not x.bandmi:
                    x.bandmi = True
                    print(f"{x.raqam}-xona muvaffaqiyatli band qilindi!")
                    return True
                else:
                    print(f"{x.raqam}-xona allaqachon band!")
                    return False
        print("Bunday xona yo'q!")
        return False

m = Mehmonxona("Hilton Tashkent")
m.xona_qosh(Xona(101, 1200000))
m.xona_qosh(Xona(102, 1500000))

m.band_qilish(101)
m.band_qilish(101)  # Qayta urinish
```

## Tushuntirish va Mantiq:
1. Mehmonxona ob'ektlari o'rtasidagi bog'liqlik va holat o'zgarishi boshqariladi.

## Ishlash natijasi:
```text
Chiqish: 101-xona band qilindi!, 101-xona allaqachon band!
```


# 386-Topshiriq: Faqat bir marta ishga tushuvchi Init-Guard

## Topshiriq sharti:
Klass metodining qayta chaqirilishini cheklovchi bayroq mexanizmi.

## Yechim (Python kodi):
```python
class TizimUlanishi:
    def __init__(self):
        self._ulangan = False

    def ulanish(self):
        if self._ulangan:
            print("[OGOHLANTIRISH] Tizimga allaqachon ulangan!")
            return
        self._ulangan = True
        print("[MUVAFFAQIYAT] Server bilan aloqa o'rnatildi.")

t = TizimUlanishi()
t.ulanish()
t.ulanish()
```

## Tushuntirish va Mantiq:
1. Qimmat resurslar (tarmoq soketlari, fayl deskriptorlari) qayta ochilishidan himoyalanadi.

## Ishlash natijasi:
```text
Chiqish: [MUVAFFAQIYAT] Aloqa o'rnatildi, [OGOHLANTIRISH] Allaqachon ulangan!
```


# 387-Topshiriq: Avtosalon Ombori (Filtrlash va Saralash)

## Topshiriq sharti:
Mashinalarni markasi, narxi va ishlab chiqarilgan yili bo'yicha qidiruvchi ombor klassi.

## Yechim (Python kodi):
```python
class Mashina:
    def __init__(self, marka, yil, narx):
        self.marka = marka
        self.yil = yil
        self.narx = narx

    def __repr__(self):
        return f"{self.marka} ({self.yil}) - ${self.narx:,}"

class Avtosalon:
    def __init__(self):
        self.avtolar = []

    def qoshish(self, a):
        self.avtolar.append(a)

    def narx_boyicha_filtr(self, maks_narx):
        return [a for a in self.avtolar if a.narx <= maks_narx]

salon = Avtosalon()
salon.qoshish(Mashina("Cobalt", 2024, 12000))
salon.qoshish(Mashina("Malibu", 2023, 28000))
salon.qoshish(Mashina("Gentra", 2022, 11000))

arzonlar = salon.narx_boyicha_filtr(15000)
print("15,000$ dan arzon avtomobillar:", arzonlar)
```

## Tushuntirish va Mantiq:
1. Ma'lumotlarni saralash va filtrlash klass ichki metodlariga yuklanadi.

## Ishlash natijasi:
```text
Chiqish: [Cobalt (2024) - $12,000, Gentra (2022) - $11,000]
```


# 388-Topshiriq: Vaqt formati klassi (Time24: Qo'shish va Formatlash)

## Topshiriq sharti:
24 soatlik formatdagi soat va daqiqalarni saqlovchi va daqiqa qo'shilganda soatni to'g'ri o'tkazuvchi klass.

## Yechim (Python kodi):
```python
class Vaqt24:
    def __init__(self, soat, daqiqa):
        self.soat = soat % 24
        self.daqiqa = daqiqa % 60

    def daqiqa_qosh(self, m):
        jami_daqiqa = self.soat * 60 + self.daqiqa + m
        self.soat = (jami_daqiqa // 60) % 24
        self.daqiqa = jami_daqiqa % 60

    def __repr__(self):
        return f"{self.soat:02d}:{self.daqiqa:02d}"

v = Vaqt24(23, 45)
print("Hozirgi vaqt:", v)

v.daqiqa_qosh(30)  # 23:45 + 30 min = 00:15
print("30 daqiqadan keyin:", v)
```

## Tushuntirish va Mantiq:
1. 24 soatlik davriy o'tishlar arifmetik modul (`%`) yordamida to'g'ri boshqariladi.

## Ishlash natijasi:
```text
Chiqish: Hozirgi: 23:45, 30 daqiqadan keyin: 00:15
```


# 389-Topshiriq: Matn Tahlili Protsessori klassi (TextAnalyzer)

## Topshiriq sharti:
Matn kiritilganda so'zlar, qatorlar, eng ko'p uchragan so'z va o'qish vaqtini beruvchi OOP protsessori.

## Yechim (Python kodi):
```python
class TextAnalyzer:
    def __init__(self, text):
        self.text = text
        self.words = text.split()

    def word_count(self):
        return len(self.words)

    def reading_time_seconds(self):
        # 200 so'z / daqiqa = ~3.3 so'z / soniya
        return round(len(self.words) / 3.33, 1)

    def summary(self):
        return f"So'zlar soni: {self.word_count()} ta | O'qish vaqti: ~{self.reading_time_seconds()} soniya"

t = TextAnalyzer("Sun'iy intellekt va katta ma'lumotlar zamonaviy dunyoni butunlay o'zgartirib yubormoqda.")
print(t.summary())
```

## Tushuntirish va Mantiq:
1. Ma'lumotlarni tahlil qilish uchun ob'ektga yo'naltirilgan qulay wrapper yaratiladi.

## Ishlash natijasi:
```text
Chiqish: So'zlar soni: 9 ta | O'qish vaqti: ~2.7 soniya
```


# 390-Topshiriq: Xodimlar va Maoshlar Iyerarxiyasi (Employee Polymorphism)

## Topshiriq sharti:
Manager (bonusli) va Developer (soatlik) xodimlarning maoshini polimorfik hisoblash tizimi.

## Yechim (Python kodi):
```python
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calculate_pay(self):
        return self.base_salary

class Manager(Employee):
    def __init__(self, name, base_salary, bonus):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def calculate_pay(self):
        return self.base_salary + self.bonus

class Developer(Employee):
    def __init__(self, name, hourly_rate, hours_worked):
        super().__init__(name, 0)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_pay(self):
        return self.hourly_rate * self.hours_worked

xodimlar = [
    Manager("Aziz (Menejer)", 10000000, 3000000),
    Developer("Farrux (Dasturchi)", 100000, 160)
]

for x in xodimlar:
    print(f"{x.name:25s} -> Oylik to'lov: {x.calculate_pay():,} so'm")
```

## Tushuntirish va Mantiq:
1. Bitta `calculate_pay()` metodi har bir lavozim turi uchun mutlaqo o'ziga xos formula bo'yicha hisoblaydi.

## Ishlash natijasi:
```text
Chiqish: Aziz: 13,000,000 so'm, Farrux: 16,000,000 so'm
```


# 391-Topshiriq: Xarid Savatchasi va Chek generatori (Cart & Item)

## Topshiriq sharti:
Mahsulotlar soni va narxini hisoblab, chegirma va soliqlarni kirituvchi kassa tizimi.

## Yechim (Python kodi):
```python
class CartItem:
    def __init__(self, title, price, quantity=1):
        self.title = title
        self.price = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def subtotal(self):
        return sum(i.total() for i in self.items)

    def print_receipt(self, discount_percent=0):
        sub = self.subtotal()
        chegirma = sub * (discount_percent / 100)
        yakuniy = sub - chegirma
        print("--- KASSA CHEKI ---")
        for i in self.items:
            print(f"{i.title:15s} x {i.quantity} = {i.total():,} so'm")
        print("-" * 30)
        print(f"Oraliq summa: {sub:,} so'm")
        print(f"Chegirma ({discount_percent}%): -{chegirma:,} so'm")
        print(f"JAMI TO'LOV : {yakuniy:,} so'm")

savat = ShoppingCart()
savat.add(CartItem("Non", 3500, 3))
savat.add(CartItem("Sut", 11000, 2))
savat.add(CartItem("Go'sht", 90000, 1))

savat.print_receipt(discount_percent=5)
```

## Tushuntirish va Mantiq:
1. Savat va Mahsulot o'rtasidagi ob'ektlar munosabati hisob-kitobni qulay qiladi.

## Ishlash natijasi:
```text
Chiqish: Non x 3 = 10500, Sut x 2 = 22000, Go'sht x 1 = 90000 -> Chek hisoboti.
```


# 392-Topshiriq: Litsenziya kalitini tekshiruvchi validator klassi

## Topshiriq sharti:
Dastur litsenziyasi to'g'ri formatda (XXXX-XXXX-XXXX-XXXX) ekanligini va cheksumini tekshiruvchi klass.

## Yechim (Python kodi):
```python
import re

class LicenseValidator:
    def __init__(self, key):
        self.key = key.strip().upper()

    def is_valid_format(self):
        # 4 ta blok, har birida 4 ta harf/raqam
        pattern = r'^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$'
        return bool(re.match(pattern, self.key))

    def validate(self):
        if not self.is_valid_format():
            return False, "Format noto'g'ri! (Namuna: ABCD-1234-EF56-7890)"
        return True, "Litsenziya kaliti haqiqiy va faollashtirildi!"

k1 = LicenseValidator("AGY1-2026-UZAI-100B")
k2 = LicenseValidator("not-a-valid-key")

print("k1:", k1.validate()[1])
print("k2:", k2.validate()[1])
```

## Tushuntirish va Mantiq:
1. Dasturiy ta'minotni litsenziyalash va himoyalash modullari shu asosda ishlaydi.

## Ishlash natijasi:
```text
Chiqish: k1: Litsenziya kaliti haqiqiy..., k2: Format noto'g'ri...
```


# 393-Topshiriq: Maxsus Logger klassi

## Topshiriq sharti:
Konsolga vaqt tamg'asi (timestamp) va xabar darajasi (INFO, WARNING, ERROR) bilan yozuvchi klass.

## Yechim (Python kodi):
```python
from datetime import datetime

class Logger:
    def __init__(self, service_name):
        self.service_name = service_name

    def _log(self, level, message):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] [{self.service_name}] [{level}] {message}")

    def info(self, msg): self._log("INFO", msg)
    def warning(self, msg): self._log("WARNING", msg)
    def error(self, msg): self._log("ERROR", msg)

log = Logger("ModelTrainingService")
log.info("Dataset xotiraga yuklandi (100 MB).")
log.warning("RAM bandligi 85% ga yetdi.")
log.error("Ulanish vaqti tugadi (Timeout).")
```

## Tushuntirish va Mantiq:
1. Tizimli loglash vositalari (logging kutubxonasi kabi) hodisalarni kuzatish uchun muhimdir.

## Ishlash natijasi:
```text
Chiqish: [2026-..-..] [ModelTrainingService] [INFO] Dataset yuklandi...
```


# 394-Topshiriq: Avtomatik ID beruvchi klass (Auto-Incrementing ID)

## Topshiriq sharti:
Klass atributi hisoblagichidan foydalanib har bir yangi ob'ektga unikal avto-id beruvchi tizim.

## Yechim (Python kodi):
```python
class BuyurtmaAutoID:
    _keyingi_id = 1001

    def __init__(self, mijoz, summa):
        self.id = BuyurtmaAutoID._keyingi_id
        BuyurtmaAutoID._keyingi_id += 1
        self.mijoz = mijoz
        self.summa = summa

    def __repr__(self):
        return f"Order#{self.id} ({self.mijoz}: {self.summa:,} so'm)"

b1 = BuyurtmaAutoID("Ali", 150000)
b2 = BuyurtmaAutoID("Vali", 280000)
b3 = BuyurtmaAutoID("Olim", 90000)

print(b1)
print(b2)
print(b3)
```

## Tushuntirish va Mantiq:
1. `_keyingi_id` klass darajasida oshib boradi, natijada barcha yaratilgan nusxalar ketma-ket unikal ID oladi.

## Ishlash natijasi:
```text
Chiqish: Order#1001, Order#1002, Order#1003
```


# 395-Topshiriq: Faqat o'qiladigan ob'ektlar (Immutable Object pattern)

## Topshiriq sharti:
Yaratilgandan keyin birorta ham atributini o'zgartirib bo'lmaydigan qat'iy himoyalangan klass.

## Yechim (Python kodi):
```python
class ImmutablePoint:
    def __init__(self, x, y):
        super().__setattr__("x", x)
        super().__setattr__("y", y)

    def __setattr__(self, name, value):
        raise TypeError(f"'{self.__class__.__name__}' ob'ektini o'zgartirish taqiqlangan!")

p = ImmutablePoint(5, 10)
print(f"Nuqta: x={p.x}, y={p.y}")

try:
    p.x = 20
except TypeError as e:
    print(f"Xatolik: {e}")
```

## Tushuntirish va Mantiq:
1. `__setattr__` metodini qayta aniqlash orqali har qanday tahrir taqiqlanadi.

## Ishlash natijasi:
```text
Chiqish: Nuqta: x=5, y=10, Xatolik: ob'ektni o'zgartirish taqiqlangan!
```


# 396-Topshiriq: Dinamik xususiyatlar delegatsiyasi (Proxy Pattern)

## Topshiriq sharti:
Boshqa ob'ektni o'rab olib, uning barcha metodlariga murojaatni nazorat qiluvchi proksi klass.

## Yechim (Python kodi):
```python
class AslXizmat:
    def malumot_ol(self):
        return "Maxfiy server ma'lumotlari: [OK]"

class XavfsizProksi:
    def __init__(self, xizmat, parol):
        self._xizmat = xizmat
        self._parol = parol

    def malumot_ol(self, kiritilgan_parol):
        if kiritilgan_parol != self._parol:
            return "XATOLIK: Noto'g'ri parol! Ruxsat berilmadi."
        return self._xizmat.malumot_ol()

xizmat = AslXizmat()
proksi = XavfsizProksi(xizmat, "sirli_kalit_777")

print("Parolsiz urinish:", proksi.malumot_ol("notogri"))
print("To'g'ri parol  :", proksi.malumot_ol("sirli_kalit_777"))
```

## Tushuntirish va Mantiq:
1. Proksi asl ob'ektga kirishni xavfsizlik, kesh yoki loglash bilan o'rab turadi.

## Ishlash natijasi:
```text
Chiqish: Parolsiz: Noto'g'ri parol, To'g'ri parol: Maxfiy server ma'lumotlari: [OK]
```


# 397-Topshiriq: Vaqtinchalik Fayl Boshqaruvchisi (Context Manager)

## Topshiriq sharti:
Fayl ochib, ish yakunlangach avtomatik o'chirib yuboruvchi xavfsiz fayl kontekst menejeri klassi.

## Yechim (Python kodi):
```python
import os

class TempFileHandler:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, "w", encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"[TOZALASH] Vaqtinchalik fayl '{self.filename}' muvaffaqiyatli o'chirildi.")

with TempFileHandler("test_temp.txt") as f:
    f.write("Vaqtinchalik muhim ma'lumot")
    print("Faylga yozildi!")
```

## Tushuntirish va Mantiq:
1. Dastur to'xtasa yoki xato bersa ham resurslar tozalanadi va operatsion tizimda keraksiz qoldiqlar qolmaydi.

## Ishlash natijasi:
```text
Chiqish: Faylga yozildi! -> [TOZALASH] Vaqtinchalik fayl o'chirildi.
```


# 398-Topshiriq: Talabalar Reyting Daftarchasi klassi (GradeBook)

## Topshiriq sharti:
Talabaning har bir fandan olgan baholarini saqlovchi va umumiy GPA ni hisoblovchi klass.

## Yechim (Python kodi):
```python
class GradeBook:
    def __init__(self, student_name):
        self.student_name = student_name
        self.grades = {}

    def add_grade(self, subject, score):
        if not (0 <= score <= 100):
            print("Baho 0 dan 100 gacha bo'lishi kerak!")
            return
        if subject not in self.grades:
            self.grades[subject] = []
        self.grades[subject].append(score)

    def calculate_gpa(self):
        if not self.grades:
            return 0.0
        all_scores = [s for scores in self.grades.values() for s in scores]
        return round(sum(all_scores) / len(all_scores), 2)

gb = GradeBook("Alisherbek")
gb.add_grade("Python", 95)
gb.add_grade("Python", 98)
gb.add_grade("Math", 90)

print(f"{gb.student_name} umumiy o'rtacha bali (GPA): {gb.calculate_gpa()}")
```

## Tushuntirish va Mantiq:
1. Talaba ma'lumotlari xavfsiz saqlanadi va umumiy ko'rsatkichlar hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: Alisherbek umumiy o'rtacha bali (GPA): 94.33
```


# 399-Topshiriq: Avtomatik Serialization: to_dict va from_dict

## Topshiriq sharti:
Ob'ektni lug'atga o'giruvchi va lug'atdan ob'ekt yasovchi serializatsiya tizimi.

## Yechim (Python kodi):
```python
class FoydalanuvchiModel:
    def __init__(self, id, ism, email):
        self.id = id
        self.ism = ism
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "ism": self.ism,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["ism"], d["email"])

f = FoydalanuvchiModel(1, "Botir", "botir@uzai.uz")
d = f.to_dict()
print("Lug'at ko'rinishi:", d)

qayta_obekt = FoydalanuvchiModel.from_dict(d)
print("Qayta ob'ekt:", qayta_obekt.ism)
```

## Tushuntirish va Mantiq:
1. Web API va ma'lumotlar bazalariga saqlashda `to_dict` / `from_dict` standarti qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: Lug'at: {'id': 1, 'ism': 'Botir'...}, Qayta ob'ekt: Botir
```


# 400-Topshiriq: To'liq Buyruqlar Markazi klassi (Command Pattern)

## Topshiriq sharti:
Bajarilgan amallarni bekor qilish (Undo) imkoniyatiga ega bo'lgan to'liq OOP Command Pattern arxitekturasi.

## Yechim (Python kodi):
```python
class MatnTahrirlovchi:
    def __init__(self):
        self.matn = ""
        self.tarix = []

    def yozish(self, yangi_soz):
        self.tarix.append(self.matn)  # Oldingi holatni saqlab qo'yamiz
        if self.matn:
            self.matn += " " + yangi_soz
        else:
            self.matn = yangi_soz
        print(f"Yozildi: '{self.matn}'")

    def bekor_qilish(self):
        if self.tarix:
            self.matn = self.tarix.pop()
            print(f"[UNDO] Qaytarildi: '{self.matn}'")
        else:
            print("[UNDO] Bekor qilish uchun tarix bo'sh!")

editor = MatnTahrirlovchi()
editor.yozish("Salom")
editor.yozish("Dunyo")
editor.yozish("Python")

editor.bekor_qilish()  # Python bekor qilinadi
editor.bekor_qilish()  # Dunyo bekor qilinadi
```

## Tushuntirish va Mantiq:
1. Command Pattern (Undo/Redo) barcha zamonaviy matn muharrirlari (VS Code, Word) arxitekturasining poydevoridir.

## Ishlash natijasi:
```text
Chiqish: Yozildi: 'Salom Dunyo Python' -> [UNDO] Qaytarildi: 'Salom Dunyo' -> [UNDO] Qaytarildi: 'Salom'
```

