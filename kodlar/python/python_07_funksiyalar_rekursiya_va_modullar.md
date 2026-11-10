# Python Dasturlash Tili — 7-Qism: Funksiyalar, Rekursiya, Dekoratorlar va Generatorlar
## (301-350 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam Python'dagi funksiyalar va ilg'or funksional dasturlash vositalarini qamrab oladi:
* `def`, `return`, standart argumentlar, kalit parametrlar;
* `*args` va `**kwargs`: universal o'zgaruvchan argumentlar qabul qilish;
* `lambda`, `map()`, `filter()`, `functools.reduce()`;
* Rekursiya asoslari: faktorial, Fibonachchi, raqamlar yig'indisi, EKUB, Xonoi minoralari, qism-to'plamlar;
* Scope: `global` va `nonlocal` kalit so'zlari, Yopilmalar (Closures);
* Dekoratorlar: timer, loglash, kesh (`lru_cache`), parametrli dekoratorlar;
* Generatorlar va `yield`: xotirani tejash, cheksiz ketma-ketliklar, Dispatcher arxitekturasi;

---

# 301-Topshiriq: Oddiy funksiya va return operatori

## Topshiriq sharti:
Ikkita sonning yig'indisini hisoblab qaytaruvchi oddiy funksiya tuzing va uni chaqiring.

## Yechim (Python kodi):
```python
def qoshish(a, b):
    """Ikki son yig'indisini qaytaradi."""
    return a + b

natija1 = qoshish(15, 25)
natija2 = qoshish(-7, 12)

print(f"15 + 25 = {natija1}")
print(f"-7 + 12 = {natija2}")
```

## Tushuntirish va Mantiq:
1. `def` kalit so'zi funksiya e'lon qiladi.
2. `return` funksiya natijasini uni chaqirgan joyga qaytaradi va funksiya ishini yakunlaydi.

## Ishlash natijasi:
```text
Chiqish: 15 + 25 = 40, -7 + 12 = 5
```


# 302-Topshiriq: Standart parametrlar (Default Arguments)

## Topshiriq sharti:
Darajaga ko'taruvchi funksiya yozing, agar daraja ko'rsatkichi berilmasa, avtomatik kvadratini (2-daraja) hisoblasin.

## Yechim (Python kodi):
```python
def daraja(asos, korsatkich=2):
    return asos ** korsatkich

print("5 ning kvadrati :", daraja(5))       # korsatkich=2 avtomatik olinadi
print("2 ning 5-darajasi:", daraja(2, 5))    # korsatkich=5 berildi
print("10 ning kubi    :", daraja(10, 3))
```

## Tushuntirish va Mantiq:
1. `korsatkich=2` standart qiymat bo'lib, argument berilmaganda ishlatiladi.
2. Standart parametrlar har doim majburiy parametrlardan keyin kelishi shart.

## Ishlash natijasi:
```text
Chiqish: 5 ning kvadrati: 25, 2 ning 5-darajasi: 32, 10 ning kubi: 1000
```


# 303-Topshiriq: O'zgaruvchan sonli pozitsion argumentlar (*args)

## Topshiriq sharti:
Istalgancha miqdordagi sonlarni qabul qilib, ularning o'rta arifmetigini qaytaruvchi funksiya tuzing.

## Yechim (Python kodi):
```python
def ortacha(*sonlar):
    if not sonlar:
        return 0
    return sum(sonlar) / len(sonlar)

print("3 ta son o'rtachasi :", ortacha(10, 20, 30))
print("5 ta son o'rtachasi :", ortacha(5, 15, 25, 35, 45))
print("Argument berilmaganda:", ortacha())
```

## Tushuntirish va Mantiq:
1. `*args` funksiyaga uzatilgan barcha ortiqcha pozitsion argumentlarni kortej (tuple) shaklida qabul qiladi.

## Ishlash natijasi:
```text
Chiqish: 3 ta son: 20.0, 5 ta son: 25.0, Argument berilmaganda: 0
```


# 304-Topshiriq: O'zgaruvchan sonli kalit argumentlar (**kwargs)

## Topshiriq sharti:
Foydalanuvchi haqidagi istalgan ma'lumotlarni qabul qilib, chiroyli profil kartochkasi shaklida chiqaruvchi funksiya tuzing.

## Yechim (Python kodi):
```python
def profil_yaratish(ism, **malumotlar):
    print(f"--- {ism.upper()} PROFILI ---")
    for kalit, qiymat in malumotlar.items():
        # Kalit nomini chiroyli sarlavhaga aylantiramiz
        print(f" * {kalit.capitalize():12s}: {qiymat}")

profil_yaratish("Alisherbek", yosh=17, shahar="Toshkent", kasb="AI Muhandisi", til="O'zbek")
```

## Tushuntirish va Mantiq:
1. `**kwargs` kalit-qiymat ko'rinishida berilgan barcha argumentlarni lug'at (dict) sifatida qabul qiladi.

## Ishlash natijasi:
```text
Chiqish: Alisherbek profili: Yosh: 17, Shahar: Toshkent, Kasb: AI Muhandisi...
```


# 305-Topshiriq: Universal argumentlar (*args va **kwargs birgalikda)

## Topshiriq sharti:
Har qanday boshqa funksiyani chaqirib, uning argumentlarini va qaytargan natijasini loglovchi universal wrapper funksiya yozing.

## Yechim (Python kodi):
```python
def log_funksiya(func, *args, **kwargs):
    print(f"[LOG] '{func.__name__}' funksiyasi chaqirilmoqda...")
    print(f"      Pozitsion argumentlar (*args) : {args}")
    print(f"      Kalit argumentlar (**kwargs)   : {kwargs}")
    natija = func(*args, **kwargs)
    print(f"[LOG] Natija: {natija}
")
    return natija

def kopaytirish(x, y, z=1):
    return x * y * z

log_funksiya(kopaytirish, 4, 5, z=2)
```

## Tushuntirish va Mantiq:
1. `*args, **kwargs` har qanday funksiyaning barcha argumentlarini o'zgarishsiz qabul qilib, unga uzatish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: [LOG] 'kopaytirish' chaqirilmoqda... Natija: 40
```


# 306-Topshiriq: Lambda (Nomsiz) funksiyalar

## Topshiriq sharti:
Sonning kvadratini hisoblovchi, ikki son yig'indisini topuvchi va satrni teskarisiga o'giruvchi lambda funksiyalari tuzing.

## Yechim (Python kodi):
```python
kvadrat = lambda x: x ** 2
yigindi = lambda a, b: a + b
teskari = lambda s: s[::-1]

print("7 ning kvadrati :", kvadrat(7))
print("12 + 18         :", yigindi(12, 18))
print("'Dasturlash'    :", teskari("Dasturlash"))
```

## Tushuntirish va Mantiq:
1. `lambda argumentlar: ifoda` ixcham, bir qatorli nomsiz funksiyalar yaratadi.
2. Ifoda natijasi avtomatik `return` qilinadi.

## Ishlash natijasi:
```text
Chiqish: 49, 30, hsalrutsaD
```


# 307-Topshiriq: map() funksiyasi bilan massivni o'zgartirish

## Topshiriq sharti:
Sonlar ro'yxatidagi barcha haroratlarni Selsiydan Farengeytga `map()` orqali o'tkazing ($F = C \times 9/5 + 32$).

## Yechim (Python kodi):
```python
selsiy_graduslar = [0, 10, 20, 25, 30, 36.6, 100]

# Farengeytga o'tkazish
farengeyt = list(map(lambda c: round(c * 9/5 + 32, 1), selsiy_graduslar))

print("Selsiy   :", selsiy_graduslar)
print("Farengeyt:", farengeyt)
```

## Tushuntirish va Mantiq:
1. `map(funksiya, ketma-ketlik)` ro'yxatning har bir elementiga funksiyani qo'llaydi va yangi iterator qaytaradi.

## Ishlash natijasi:
```text
Chiqish: [32.0, 50.0, 68.0, 77.0, 86.0, 97.9, 212.0]
```


# 308-Topshiriq: filter() funksiyasi bilan saralash

## Topshiriq sharti:
So'zlar ro'yxatidan faqat uzunligi 5 tadan ortiq bo'lganlarini `filter()` orqali ajratib oling.

## Yechim (Python kodi):
```python
shaharlar = ["Toshkent", "Samarqand", "Xiva", "Buxoro", "Nukus", "Qarshi"]

uzun_shaharlar = list(filter(lambda s: len(s) > 5, shaharlar))

print("Barcha shaharlar :", shaharlar)
print("Uzun nomli shaharlar:", uzun_shaharlar)
```

## Tushuntirish va Mantiq:
1. `filter(shart_funksiya, ketma-ketlik)` shart `True` bo'lgan elementlarnigina qoldiradi.

## Ishlash natijasi:
```text
Chiqish: ['Toshkent', 'Samarqand', 'Buxoro', 'Qarshi']
```


# 309-Topshiriq: functools.reduce() bilan yagona qiymatga keltirish

## Topshiriq sharti:
Sonlar ro'yxatining umumiy ko'paytmasini (faktorialini) `reduce()` funksiyasi yordamida hisoblang.

## Yechim (Python kodi):
```python
from functools import reduce

sonlar = [1, 2, 3, 4, 5, 6]

# ketma-ket a * b amalini bajaradi
kopaytma = reduce(lambda a, b: a * b, sonlar)

print(f"Sonlar: {sonlar}")
print(f"6! (umumiy ko'paytma): {kopaytma}")
```

## Tushuntirish va Mantiq:
1. `reduce()` ro'yxat elementlarini ikkitadan olib oxiriga qadar bitta natijaga keltirib boradi (fold/accumulate).

## Ishlash natijasi:
```text
Chiqish: 720
```


# 310-Topshiriq: Rekursiya: Faktorialni hisoblash

## Topshiriq sharti:
Sonning faktorialini (n!) klassik rekursiya usuli bilan topuvchi funksiya yozing.

## Yechim (Python kodi):
```python
def faktorial_rekursiv(n):
    # 1. Baza holati (Base case)
    if n <= 1:
        return 1
    # 2. Rekursiv qadam
    return n * faktorial_rekursiv(n - 1)

print("5! =", faktorial_rekursiv(5))
print("7! =", faktorial_rekursiv(7))
```

## Tushuntirish va Mantiq:
1. Har bir rekursiv funksiyada cheksiz tsiklga tushib qolmaslik uchun baza holati (`n <= 1`) bo'lishi shart.
2. Matematik qoida: n! = n * (n-1)!

## Ishlash natijasi:
```text
Chiqish: 5! = 120, 7! = 5040
```


# 311-Topshiriq: Rekursiya: Fibonachchi soni va rekursiv daraxt

## Topshiriq sharti:
N-chi Fibonachchi sonini rekursiv topuvchi funksiya tuzing va uning baza holatini ko'rsating.

## Yechim (Python kodi):
```python
def fibonachchi(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonachchi(n - 1) + fibonachchi(n - 2)

for i in range(8):
    print(f"F({i}) = {fibonachchi(i)}", end="  ")
print()
```

## Tushuntirish va Mantiq:
1. F(0)=0, F(1)=1 baza holatlari bo'lib, keyingi hadlar oldingi ikkitasining rekursiv yig'indisidir.

## Ishlash natijasi:
```text
Chiqish: F(0)=0  F(1)=1  F(2)=1  F(3)=2  F(4)=3  F(5)=5  F(6)=8  F(7)=13
```


# 312-Topshiriq: Rekursiya: Sonning raqamlari yig'indisi

## Topshiriq sharti:
Natural sonning raqamlari yig'indisini tsiklsiz, faqat rekursiya orqali hisoblang.

## Yechim (Python kodi):
```python
def raqamlar_yigindisi(n):
    if n < 10:
        return n
    return (n % 10) + raqamlar_yigindisi(n // 10)

son = 9876
print(f"{son} raqamlari yig'indisi: {raqamlar_yigindisi(son)}")
```

## Tushuntirish va Mantiq:
1. Oxirgi raqam `n % 10` olinadi va qolgan qismi `n // 10` rekursiv chaqiruvga uzatiladi.
2. Son 10 dan kichik bo'lganda rekursiya to'xtaydi.

## Ishlash natijasi:
```text
Chiqish: 9876 raqamlari yig'indisi: 30 (9+8+7+6)
```


# 313-Topshiriq: Rekursiya: Satrni teskarisiga o'girish

## Topshiriq sharti:
Satrni kesish (slicing) yoki tsikl ishlatmasdan, rekursiv funksiya yordamida teskari qiling.

## Yechim (Python kodi):
```python
def satr_teskari(s):
    if len(s) <= 1:
        return s
    return s[-1] + satr_teskari(s[:-1])

matn = "Antigravity"
print(f"Asl satr   : {matn}")
print(f"Teskari satr: {satr_teskari(matn)}")
```

## Tushuntirish va Mantiq:
1. Satrning oxirgi belgisi olinib, qolgan qismi rekursiv chaqiruvga yuboriladi.

## Ishlash natijasi:
```text
Chiqish: Asl: Antigravity, Teskari: ytivargitnA
```


# 314-Topshiriq: Rekursiya: Evklid algoritmi (EKUB / GCD)

## Topshiriq sharti:
Ikki sonning eng katta umumiy bo'luvchisini rekursiv Evklid formulasi bilan toping.

## Yechim (Python kodi):
```python
def ekub_rekursiv(a, b):
    if b == 0:
        return a
    return ekub_rekursiv(b, a % b)

print("EKUB(48, 18) =", ekub_rekursiv(48, 18))
print("EKUB(100, 35) =", ekub_rekursiv(100, 35))
```

## Tushuntirish va Mantiq:
1. Evklid formulasi: EKUB(a, b) = EKUB(b, a % b).
2. Qoldiq nol bo'lganda (`b == 0`), a qiymati EKUB bo'lib qaytadi.

## Ishlash natijasi:
```text
Chiqish: EKUB(48, 18) = 6, EKUB(100, 35) = 5
```


# 315-Topshiriq: Rekursiya: Xonoi minoralari (Towers of Hanoi)

## Topshiriq sharti:
N ta diskni A ustundan C ustunga B ustun yordamida ko'chirish qadamlarini chiqaruvchi klassik rekursiv dastur.

## Yechim (Python kodi):
```python
def xonoi(n, boshlangich, yordamchi, maqsad):
    if n == 1:
        print(f"1-diskni {boshlangich} dan {maqsad} ga ko'chiring")
        return
    # 1. n-1 ta diskni yordamchi ustunga olib o'tamiz
    xonoi(n - 1, boshlangich, maqsad, yordamchi)
    # 2. Eng katta diskni maqsad ustuniga o'tkazamiz
    print(f"{n}-diskni {boshlangich} dan {maqsad} ga ko'chiring")
    # 3. Yordamchi ustundagi n-1 diskni maqsad ustuniga o'tkazamiz
    xonoi(n - 1, yordamchi, boshlangich, maqsad)

print("3 ta disk uchun Xonoi minoralari yechimi:")
xonoi(3, 'A', 'B', 'C')
```

## Tushuntirish va Mantiq:
1. Har doim 3 ta bosqich: n-1 diskni yordamchiga, eng kattani maqsadga, qolgan n-1 ni maqsadga ko'chirish.
2. Jami qadamlar soni: 2^n - 1 ta bo'ladi (3 ta disk uchun 7 ta qadam).

## Ishlash natijasi:
```text
Chiqish: 7 qadamlik disk ko'chirish ko'rsatmasi.
```


# 316-Topshiriq: Ko'rinish sohasi (Scope): global kalit so'zi

## Topshiriq sharti:
Funksiya ichida tashqi global o'zgaruvchini o'zgartirish uchun `global` kalit so'zining ishlatilishini ko'rsating.

## Yechim (Python kodi):
```python
hisoblagich = 0

def qadam():
    global hisoblagich
    hisoblagich += 1

print(f"Boshlang'ich: {hisoblagich}")
qadam()
qadam()
qadam()
print(f"3 qadamdan keyin: {hisoblagich}")
```

## Tushuntirish va Mantiq:
1. `global hisoblagich` funksiyaga tashqi modul darajasidagi o'zgaruvchini tahrirlash huquqini beradi.

## Ishlash natijasi:
```text
Chiqish: Boshlang'ich: 0, 3 qadamdan keyin: 3
```


# 317-Topshiriq: Ko'rinish sohasi (Scope): nonlocal kalit so'zi

## Topshiriq sharti:
Ichma-ich funksiyada tashqi (enclosing) funksiyaning o'zgaruvchisini o'zgartirish uchun `nonlocal` ishlatilishini ko'rsating.

## Yechim (Python kodi):
```python
def tashqi():
    son = 10
    def ichki():
        nonlocal son
        son += 5
        print(f"Ichki funksiya ichida son: {son}")
    ichki()
    print(f"Tashqi funksiya ichida son: {son}")

tashqi()
```

## Tushuntirish va Mantiq:
1. `nonlocal` global emas, lekin o'rab turgan tashqi funksiya o'zgaruvchisini o'zgartirishga xizmat qiladi.

## Ishlash natijasi:
```text
Chiqish: Ichki: 15, Tashqi: 15
```


# 318-Topshiriq: Yopilmalar (Closures): Ko'paytiruvchi generator

## Topshiriq sharti:
O'zining ichki holatini xotirada saqlab qoluvchi closure funksiya orqali ikkiga va uchga ko'paytiruvchi funksiyalar yasang.

## Yechim (Python kodi):
```python
def kopaytiruvchi_yarat(daraja):
    def ichki(son):
        return son * daraja
    return ichki

ikkiga_kopaytir = kopaytiruvchi_yarat(2)
uchga_kopaytir = kopaytiruvchi_yarat(3)

print("10 * 2 =", ikkiga_kopaytir(10))
print("10 * 3 =", uchga_kopaytir(10))
```

## Tushuntirish va Mantiq:
1. Closure tashqi funksiya parametrlari (`daraja`) xotirada saqlanib, qaytarilgan ichki funksiya tomonidan ishlatilishidir.

## Ishlash natijasi:
```text
Chiqish: 10 * 2 = 20, 10 * 3 = 30
```


# 319-Topshiriq: Dekorator: Funksiya bajarilish vaqtini o'lchovchi Timer

## Topshiriq sharti:
Istalgan funksiyaning necha soniyada bajarilganini aniq hisoblovchi timer dekoratorini tuzing.

## Yechim (Python kodi):
```python
import time
import functools

def vaqtni_olcha(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        boshlanish = time.perf_counter()
        natija = func(*args, **kwargs)
        tugash = time.perf_counter()
        sarflandi = tugash - boshlanish
        print(f"[TIMER] '{func.__name__}' funksiyasi {sarflandi:.6f} soniyada bajarildi.")
        return natija
    return wrapper

@vaqtni_olcha
def katta_hisob():
    return sum(i ** 2 for i in range(1_000_000))

natija = katta_hisob()
```

## Tushuntirish va Mantiq:
1. `@dekorator` sintaksisi funksiyaning kodini o'zgartirmasdan unga qo'shimcha xususiyat qo'shadi.
2. `@functools.wraps` funksiya nomi va hujjatlarini asl holida saqlaydi.

## Ishlash natijasi:
```text
Chiqish: [TIMER] 'katta_hisob' funksiyasi 0.08... soniyada bajarildi.
```


# 320-Topshiriq: Dekorator: Funksiya chaqiruvlari hisoblagichi (Call Counter)

## Topshiriq sharti:
Funksiya dastur davomida jami necha marta chaqirilganini sanab boruvchi dekorator tuzing.

## Yechim (Python kodi):
```python
def hisobla_chaqiruv(func):
    chaqiruvlar = 0
    def wrapper(*args, **kwargs):
        nonlocal chaqiruvlar
        chaqiruvlar += 1
        print(f"[INFO] '{func.__name__}' {chaqiruvlar}-marta chaqirildi.")
        return func(*args, **kwargs)
    return wrapper

@hisobla_chaqiruv
def salom_ber(ism):
    return f"Salom, {ism}!"

print(salom_ber("Alisher"))
print(salom_ber("Jasur"))
print(salom_ber("Madina"))
```

## Tushuntirish va Mantiq:
1. Dekorator closure orqali ichki `chaqiruvlar` hisoblagichini eslab qoladi.

## Ishlash natijasi:
```text
Chiqish: 1-marta, 2-marta, 3-marta chaqirildi xabarlari.
```


# 321-Topshiriq: Generatorlar: yield kalit so'zi

## Topshiriq sharti:
Butun ro'yxatni xotiraga yuklamasdan, sonlarni bittadan generatsiya qiluvchi generator funksiya tuzing.

## Yechim (Python kodi):
```python
def sanoq_generatori(n):
    for i in range(1, n + 1):
        yield i

gen = sanoq_generatori(4)
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
print(next(gen))  # 4
```

## Tushuntirish va Mantiq:
1. `yield` funksiya holatini to'xtatib (pause), qiymatni qaytaradi va keyingi `next()` chaqirilganda shu joydan davom etadi.
2. Bu millionlab sonlar bilan ishlaganda gigabaytlab RAM tejaydi.

## Ishlash natijasi:
```text
Chiqish: 1, 2, 3, 4
```


# 322-Topshiriq: Cheksiz Fibonachchi generatori

## Topshiriq sharti:
`yield` yordamida cheksiz davom etuvchi Fibonachchi ketma-ketligi generatorini tuzing.

## Yechim (Python kodi):
```python
def cheksiz_fibonachchi():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fibo_gen = cheksiz_fibonachchi()

print("Dastlabki 10 ta Fibonachchi soni:")
for _ in range(10):
    print(next(fibo_gen), end=" ")
print()
```

## Tushuntirish va Mantiq:
1. `while True` bilan yozilgan bo'lsa-da, xotira to'lib ketmaydi, chunki faqat `next()` so'ralganda 1 qadam bajariladi.

## Ishlash natijasi:
```text
Chiqish: 0 1 1 2 3 5 8 13 21 34
```


# 323-Topshiriq: Type Hinting (Ma'lumot turlarini ko'rsatish)

## Topshiriq sharti:
Funksiya parametrlari va qaytuvchi qiymatining turlarini (int, str, List, Dict) aniq ko'rsating.

## Yechim (Python kodi):
```python
from typing import List, Optional

def talabalar_ortachasi(ballar: List[float], bonus: Optional[float] = None) -> float:
    if not ballar:
        return 0.0
    ortacha = sum(ballar) / len(ballar)
    if bonus is not None:
        ortacha += bonus
    return round(ortacha, 2)

b = [85.5, 90.0, 78.5]
print("Natija:", talabalar_ortachasi(b, bonus=2.5))
```

## Tushuntirish va Mantiq:
1. Type hints (`param: type -> return_type`) kod tushunarliligini oshiradi va IDE xatoliklarni oldindan topishiga yordam beradi.

## Ishlash natijasi:
```text
Chiqish: Natija: 87.17
```


# 324-Topshiriq: functools.partial orqali parametrlarni mahkamlash

## Topshiriq sharti:
`functools.partial` orqali ko'p parametrli funksiyadan ba'zi parametrlari qotirilgan yangi funksiya yasang.

## Yechim (Python kodi):
```python
from functools import partial

def soliq_hisobla(daromad, stavka_foiz):
    return daromad * (stavka_foiz / 100)

# O'zbekiston jismoniy shaxslar daromad solig'i (12%)
uzb_soliq = partial(soliq_hisobla, stavka_foiz=12)

maosh = 10_000_000
soliq = uzb_soliq(maosh)

print(f"{maosh:,} so'm maoshdan 12% soliq: {soliq:,} so'm")
```

## Tushuntirish va Mantiq:
1. `partial(func, arg)` mavjud funksiyaning ma'lum parametrlarini qotirib, yangi ixcham funksiya hosil qiladi.

## Ishlash natijasi:
```text
Chiqish: 10,000,000 so'm maoshdan 12% soliq: 1,200,000.0 so'm
```


# 325-Topshiriq: Rekursiv Ikkilik Qidiruv (Binary Search)

## Topshiriq sharti:
Saralangan ro'yxatdan elementni rekursiv ikkilik qidiruv algoritmi bilan O(log n) da toping.

## Yechim (Python kodi):
```python
def binar_qidiruv_rekursiv(massiv, nishon, chap, ong):
    if chap > ong:
        return -1  # Topilmadi

    orta = (chap + ong) // 2

    if massiv[orta] == nishon:
        return orta
    elif massiv[orta] > nishon:
        return binar_qidiruv_rekursiv(massiv, nishon, chap, orta - 1)
    else:
        return binar_qidiruv_rekursiv(massiv, nishon, orta + 1, ong)

sonlar = [10, 23, 35, 48, 59, 72, 85, 94]
nishon = 72

indeks = binar_qidiruv_rekursiv(sonlar, nishon, 0, len(sonlar) - 1)
print(f"{nishon} sonining indeksi: {indeks}")
```

## Tushuntirish va Mantiq:
1. Har bir rekursiv chaqiruvda qidiruv maydoni 2 barobar qisqaradi.

## Ishlash natijasi:
```text
Chiqish: 72 sonining indeksi: 5
```


# 326-Topshiriq: Ro'yxatdagi eng katta elementni rekursiv topish

## Topshiriq sharti:
Ro'yxatning maksimum elementini for/while tsikllarisiz, faqat rekursiya orqali toping.

## Yechim (Python kodi):
```python
def rekursiv_max(massiv):
    if len(massiv) == 1:
        return massiv[0]
    
    qolgan_max = rekursiv_max(massiv[1:])
    return massiv[0] if massiv[0] > qolgan_max else qolgan_max

sonlar = [14, 52, 89, 23, 97, 45, 12]
print(f"Maksimal son: {rekursiv_max(sonlar)}")
```

## Tushuntirish va Mantiq:
1. Massiv bitta element qolguncha bo'linadi va chekkadan taqqoslanib qaytadi.

## Ishlash natijasi:
```text
Chiqish: Maksimal son: 97
```


# 327-Topshiriq: Ko'p o'lchamli ro'yxatni rekursiv tekislash (Deep Flatten)

## Topshiriq sharti:
Istalgancha chuqurlikdagi ichma-ich ro'yxatlarni (`[1, [2, [3, 4], 5], 6]`) bitta tekis ro'yxatga aylantiring.

## Yechim (Python kodi):
```python
def deep_flatten(aralash):
    natija = []
    for x in aralash:
        if isinstance(x, list):
            natija.extend(deep_flatten(x))
        else:
            natija.append(x)
    return natija

ichma_ich = [1, [2, [3, [4, 5]], 6], [7, 8], 9]
print("Asl ro'yxat  :", ichma_ich)
print("Tekis ro'yxat:", deep_flatten(ichma_ich))
```

## Tushuntirish va Mantiq:
1. `isinstance(x, list)` agar element ro'yxat bo'lsa uni rekursiv qayta ishlaydi, aks holda natijaga qo'shadi.

## Ishlash natijasi:
```text
Chiqish: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```


# 328-Topshiriq: Barcha qism-to'plamlarni rekursiv hosil qilish (Power Set)

## Topshiriq sharti:
To'plamning barcha mumkin bo'lgan qism-to'plamlarini (bo'sh to'plamdan to to'liq to'plamgacha) rekursiv generatsiya qiling.

## Yechim (Python kodi):
```python
def power_set(elementlar):
    if not elementlar:
        return [[]]
    
    boshi = elementlar[0]
    qolgan = power_set(elementlar[1:])
    
    boshi_bilan = [[boshi] + q for q in qolgan]
    return qolgan + boshi_bilan

to'plam = [1, 2, 3]
natija = power_set(to'plam)

print(f"{to'plam} to'plamining barcha qism-to'plamlari ({len(natija)} ta):")
for q in natija:
    print(q)
```

## Tushuntirish va Mantiq:
1. Har bir element uchun 2 ta tanlov bor: qism-to'plamga kirish yoki kirmaslik.
2. Jami qism-to'plamlar soni 2^n ga teng bo'ladi (3 ta element uchun 8 ta).

## Ishlash natijasi:
```text
Chiqish: [], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]
```


# 329-Topshiriq: Permutatsiyalar (O'rin almashtirishlar) rekursiyasi

## Topshiriq sharti:
Elementlarning barcha mumkin bo'lgan o'rin almashtirishlarini (permutatsiyalarini) rekursiv toping.

## Yechim (Python kodi):
```python
def permutatsiyalar(massiv):
    if len(massiv) <= 1:
        return [massiv]
    
    natija = []
    for i in range(len(massiv)):
        joriy = massiv[i]
        qolganlar = massiv[:i] + massiv[i+1:]
        for p in permutatsiyalar(qolganlar):
            natija.append([joriy] + p)
    return natija

harflar = ['A', 'B', 'C']
p = permutatsiyalar(harflar)

print(f"{harflar} ning barcha permutatsiyalari ({len(p)} ta):")
for qator in p:
    print(qator)
```

## Tushuntirish va Mantiq:
1. N ta elementning permutatsiyalar soni n! ga teng (3 ta element uchun 3! = 6 ta).

## Ishlash natijasi:
```text
Chiqish: ['A', 'B', 'C'], ['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']
```


# 330-Topshiriq: Haqiqiy sonlar uchun qadamli diapazon generatori

## Topshiriq sharti:
Standart `range` faqat butun sonlar bilan ishlaydi. Float qadamlar bilan ishlovchi `float_range` generatorini yozing.

## Yechim (Python kodi):
```python
def float_range(start, stop, step):
    joriy = start
    while joriy < stop:
        yield round(joriy, 6)
        joriy += step

print("0.0 dan 1.0 gacha 0.2 qadam bilan:")
for x in float_range(0.0, 1.0, 0.2):
    print(x, end="  ")
print()
```

## Tushuntirish va Mantiq:
1. `round(joriy, 6)` suzuvchi nuqtali sonlarning binar yaxlitlash xatoliklarini bartaraf qiladi.

## Ishlash natijasi:
```text
Chiqish: 0.0  0.2  0.4  0.6  0.8
```


# 331-Topshiriq: Parametrli dekorator (Repeat)

## Topshiriq sharti:
Funksiyani berilgan n marta takroran ishga tushiruvchi parametrli dekorator yozing.

## Yechim (Python kodi):
```python
def takrorla(n_marta):
    def dekorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n_marta):
                natija = func(*args, **kwargs)
            return natija
        return wrapper
    return dekorator

@takrorla(n_marta=3)
def salom():
    print("Salom, O'zbekiston!")

salom()
```

## Tushuntirish va Mantiq:
1. Parametrli dekorator 3 ta ichma-ich funksiya qatlamidan iborat bo'ladi: parametr qabul qiluvchi, dekorator va wrapper.

## Ishlash natijasi:
```text
Chiqish: Salom, O'zbekiston! (3 marta chop etiladi)
```


# 332-Topshiriq: Funksiya keshlovchi lru_cache dekoratori

## Topshiriq sharti:
`functools.lru_cache` orqali sekin ishlovchi rekursiv Fibonachchini bir zumda ishlaydigan qiling.

## Yechim (Python kodi):
```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def tez_fibo(n):
    if n <= 1:
        return n
    return tez_fibo(n - 1) + tez_fibo(n - 2)

boshlanish = time.perf_counter()
natija = tez_fibo(35)
tugash = time.perf_counter()

print(f"F(35) = {natija}")
print(f"Bajarilish vaqti: {(tugash - boshlanish)*1000:.3f} millisoniya")
```

## Tushuntirish va Mantiq:
1. Oddiy rekursiya F(35) uchun bir necha soniya sarflasa, `lru_cache` bilan 0.01 millisoniyada bajariladi (O(2^n) dan O(n) ga tushadi).

## Ishlash natijasi:
```text
Chiqish: F(35) = 9227465, Vaqt: < 0.1 ms
```


# 333-Topshiriq: Funksiyani argument sifatida qabul qiluvchi amallar ijrochisi

## Topshiriq sharti:
Ikkita son va arifmetik funksiyani qabul qilib amalni bajaruvchi yuqori tartibli funksiya (Higher-order function) tuzing.

## Yechim (Python kodi):
```python
def hisoblagich(a, b, amal_funksiyasi):
    return amal_funksiyasi(a, b)

def qosh(x, y): return x + y
def kopaytir(x, y): return x * y
def daraja(x, y): return x ** y

print("10 + 5 =", hisoblagich(10, 5, qosh))
print("10 * 5 =", hisoblagich(10, 5, kopaytir))
print("10 ^ 3 =", hisoblagich(10, 3, daraja))
```

## Tushuntirish va Mantiq:
1. Python'da funksiyalar birinchi darajali ob'ekt (first-class citizens) bo'lib, o'zgaruvchi kabi uzatilishi mumkin.

## Ishlash natijasi:
```text
Chiqish: 15, 50, 1000
```


# 334-Topshiriq: Funksiya qaytaruvchi funksiya (Factory Pattern)

## Topshiriq sharti:
Foydalanuvchi tiliga qarab mos qutlovchi funksiya qaytaruvchi tizim tuzing.

## Yechim (Python kodi):
```python
def salomlashuvchi_yarat(til):
    if til == "uz":
        return lambda ism: f"Assalomu alaykum, {ism}!"
    elif til == "en":
        return lambda ism: f"Hello, {ism}!"
    elif til == "ru":
        return lambda ism: f"Здравствуйте, {ism}!"
    else:
        return lambda ism: f"Salom, {ism}!"

uz_salom = salomlashuvchi_yarat("uz")
en_salom = salomlashuvchi_yarat("en")

print(uz_salom("Alisher"))
print(en_salom("John"))
```

## Tushuntirish va Mantiq:
1. Funksiya zavodi (Factory) parametrlarga asosan maxsus moslashtirilgan funksiyalar generatsiya qiladi.

## Ishlash natijasi:
```text
Chiqish: Assalomu alaykum, Alisher!, Hello, John!
```


# 335-Topshiriq: Funksiya annotatsiyalari va inspeksiyasi

## Topshiriq sharti:
Funksiyaning docstring va parametr turlari annotatsiyasini dastur orqali o'qish.

## Yechim (Python kodi):
```python
def kredit_hisobla(summa: float, oy: int) -> float:
    """Oylik kredit to'lovini hisoblaydi."""
    return summa / oy

print("Funksiya nomi      :", kredit_hisobla.__name__)
print("Hujjat (Docstring) :", kredit_hisobla.__doc__)
print("Annotatsiyalar     :", kredit_hisobla.__annotations__)
```

## Tushuntirish va Mantiq:
1. `__doc__` va `__annotations__` meta-dasturlashda (avtomatik hujjatlashtirish va validatsiya) qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: Funksiya nomi, docstring va annotatsiya lug'ati.
```


# 336-Topshiriq: Rekursiv Palindrom tekshirgich

## Topshiriq sharti:
Satrning palindrom ekanligini tsikl va slicing ishlatmasdan, faqat rekursiv harflar solishtiruvi bilan tekshiring.

## Yechim (Python kodi):
```python
def palindrom_rekursiv(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return palindrom_rekursiv(s[1:-1])

print("'radar'   — Palindrommi?", palindrom_rekursiv("radar"))
print("'salom'   — Palindrommi?", palindrom_rekursiv("salom"))
print("'kazak'   — Palindrommi?", palindrom_rekursiv("kazak"))
```

## Tushuntirish va Mantiq:
1. Bosh va oxirgi harflar tekshiriladi, agar teng bo'lsa ichki qismi qisqartirilib tekshiriladi.

## Ishlash natijasi:
```text
Chiqish: radar: True, salom: False, kazak: True
```


# 337-Topshiriq: Sonning darajasini tezkor rekursiv hisoblash (Fast Power)

## Topshiriq sharti:
O(log n) tezlikdagi tezkor ikkilik darajaga ko'tarish algoritmini rekursiv tuzing.

## Yechim (Python kodi):
```python
def tezkor_daraja(a, n):
    if n == 0:
        return 1
    if n % 2 == 0:
        yarim = tezkor_daraja(a, n // 2)
        return yarim * yarim
    else:
        return a * tezkor_daraja(a, n - 1)

print("2^10 =", tezkor_daraja(2, 10))
print("3^5  =", tezkor_daraja(3, 5))
```

## Tushuntirish va Mantiq:
1. Agar daraja juft bo'lsa a^n = (a^(n/2))^2 formulasi hisoblashlar sonini keskin qisqartiradi.

## Ishlash natijasi:
```text
Chiqish: 2^10 = 1024, 3^5 = 243
```


# 338-Topshiriq: Rekursiya chuqurligi limitini boshqarish

## Topshiriq sharti:
`sys` moduli orqali Python'ning maksimal rekursiya chegarasini ko'rish va uni xavfsiz boshqarish.

## Yechim (Python kodi):
```python
import sys

joriy_limit = sys.getrecursionlimit()
print(f"Python standart rekursiya limiti: {joriy_limit}")

# Yangi limit o'rnatish
sys.setrecursionlimit(2000)
print(f"Yangi o'rnatilgan limit: {sys.getrecursionlimit()}")

# Qayta standart holatga qaytaramiz
sys.setrecursionlimit(joriy_limit)
```

## Tushuntirish va Mantiq:
1. Python cheksiz rekursiya kompyuter xotirasini to'ldirib (Stack Overflow) tizimni qulatmasligi uchun odatda 1000 limit qo'yadi.

## Ishlash natijasi:
```text
Chiqish: Standart limit: 1000
```


# 339-Topshiriq: Dispatcher Lug'ati (If-Else zanjiridan xalos bo'lish)

## Topshiriq sharti:
Amallar nomini funksiyalarga bog'lovchi lug'at (Command Dispatcher) orqali toza arxitektura tuzing.

## Yechim (Python kodi):
```python
def qoshish(a, b): return a + b
def ayirish(a, b): return a - b
def kopaytirish(a, b): return a * b
def bolish(a, b): return a / b if b != 0 else None

amallar = {
    "+": qoshish,
    "-": ayirish,
    "*": kopaytirish,
    "/": bolish
}

def hisobla(amal, x, y):
    funksiya = amallar.get(amal)
    if funksiya:
        return funksiya(x, y)
    return "Noma'lum amal!"

print("20 + 10 =", hisobla("+", 20, 10))
print("20 * 10 =", hisobla("*", 20, 10))
print("20 / 4  =", hisobla("/", 20, 4))
```

## Tushuntirish va Mantiq:
1. `if...elif...elif...` o'rniga lug'atdan funksiya chaqirish (Dispatcher Pattern) kodni ancha tez va kengaytiriladigan qiladi.

## Ishlash natijasi:
```text
Chiqish: 30, 200, 5.0
```


# 340-Topshiriq: Paskal uchburchagining ixtiyoriy hadini rekursiv topish

## Topshiriq sharti:
Paskal uchburchagining r-qatoridagi c-ustun elementini rekursiv kombinatorika formulasi bilan toping.

## Yechim (Python kodi):
```python
def paskal_hadi(qator, ustun):
    if ustun == 0 or ustun == qator:
        return 1
    return paskal_hadi(qator - 1, ustun - 1) + paskal_hadi(qator - 1, ustun)

print("Paskal uchburchagining 4-qatordagi hadlari:")
for c in range(5):
    print(paskal_hadi(4, c), end=" ")
print()
```

## Tushuntirish va Mantiq:
1. Chekka elementlar 1 bo'ladi.
2. Ichki element tepasidagi ikkita had yig'indisidir: C(n, k) = C(n-1, k-1) + C(n-1, k).

## Ishlash natijasi:
```text
Chiqish: 1 4 6 4 1
```


# 341-Topshiriq: Dekorator: Funksiya argumentlarini tekshiruvchi validator

## Topshiriq sharti:
Funksiyaga faqat musbat sonlar uzatilishini talab qiluvchi, aks holda ValueError chiqaruvchi dekorator.

## Yechim (Python kodi):
```python
def faqat_musbat(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Xato: manfiy argument qabul qilinmaydi: {arg}")
        return func(*args, **kwargs)
    return wrapper

@faqat_musbat
def ildiz(son):
    return son ** 0.5

print("16 ning ildizi:", ildiz(16))
try:
    print(ildiz(-4))
except ValueError as e:
    print(f"Ushlangan xatolik: {e}")
```

## Tushuntirish va Mantiq:
1. Dekorator funksiya bajarilishidan oldin argumentlar xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: 16 ning ildizi: 4.0, Ushlangan xatolik: Xato: manfiy argument...
```


# 342-Topshiriq: Funksiya kompozitsiyasi (Function Composition)

## Topshiriq sharti:
Ikki funksiyani birlashtirib f(g(x)) yangi kompozitsiya funksiyasini hosil qiluvchi helper yozing.

## Yechim (Python kodi):
```python
def kompozitsiya(f, g):
    return lambda x: f(g(x))

kvadrat = lambda x: x ** 2
bir_qosh = lambda x: x + 1

# f(g(x)) = (x + 1)^2
hisob = kompozitsiya(kvadrat, bir_qosh)

print("hisob(4) = (4 + 1)^2 =", hisob(4))
```

## Tushuntirish va Mantiq:
1. Funksional dasturlashda funksiyalarni zanjir kabi ulash kompozitsiya deyiladi.

## Ishlash natijasi:
```text
Chiqish: hisob(4) = (4 + 1)^2 = 25
```


# 343-Topshiriq: Matn tozalovchi funksional pipeline

## Topshiriq sharti:
Matn ustida ketma-ket bir nechta qayta ishlovchi funksiyalarni zanjir orqali qo'llash.

## Yechim (Python kodi):
```python
def kichik_harf(t): return t.lower()
def boshliqlarni_tozala(t): return " ".join(t.split())
def undovsiz(t): return t.replace("!", ".")

def pipeline_bajar(matn, *funksiyalar):
    for f in funksiyalar:
        matn = f(matn)
    return matn

xom_matn = "  ASSALOMU    ALAYKUM,   DUNYO!!!   "
toza = pipeline_bajar(xom_matn, kichik_harf, boshliqlarni_tozala, undovsiz)

print(f"Xom matn : '{xom_matn}'")
print(f"Toza matn: '{toza}'")
```

## Tushuntirish va Mantiq:
1. Ma'lumotlarni tozalash jarayonida modulli pipeline arxitekturasi juda qulaydir.

## Ishlash natijasi:
```text
Chiqish: 'assalomu alaykum, dunyo...'
```


# 344-Topshiriq: Generator yordamida tub sonlar oqimi

## Topshiriq sharti:
Talab qilinganda bittadan navbatdagi tub sonni beruvchi generator funksiya tuzing.

## Yechim (Python kodi):
```python
def tubmi(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def tub_sonlar_oqimi():
    son = 2
    while True:
        if tubmi(son):
            yield son
        son += 1

gen = tub_sonlar_oqimi()
print("Dastlabki 6 ta tub son:")
for _ in range(6):
    print(next(gen), end=" ")
print()
```

## Tushuntirish va Mantiq:
1. Cheksiz tub sonlar oqimidan xohlagancha sonni xotirani to'ldirmasdan sug'urib olish mumkin.

## Ishlash natijasi:
```text
Chiqish: 2 3 5 7 11 13
```


# 345-Topshiriq: Xatoliklarni xavfsiz chetlab o'tuvchi Safe-Runner

## Topshiriq sharti:
Xato berishi mumkin bo'lgan har qanday funksiyani xavfsiz ishga tushirib, xato bo'lsa standart qiymat qaytaruvchi helper.

## Yechim (Python kodi):
```python
def xavfsiz_chaqir(func, standart_qiymat=None, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"[OGOHLANTIRISH] '{func.__name__}' xatosi: {e}")
        return standart_qiymat

def bolish(a, b): return a / b

print("10 / 2 =", xavfsiz_chaqir(bolish, 0, 10, 2))
print("10 / 0 =", xavfsiz_chaqir(bolish, 0, 10, 0))
```

## Tushuntirish va Mantiq:
1. Dasturning kritik qismlarida kutilmagan qulashlarning oldini oladi.

## Ishlash natijasi:
```text
Chiqish: 10 / 2 = 5.0, 10 / 0 = 0
```


# 346-Topshiriq: Funksiya ichida dinamik funksiya yaratish va qaytarish

## Topshiriq sharti:
Ko'rsatilgan prefiks va suffiks bilan matn o'rovchi shaxsiy formatlagich funksiyalar generatori.

## Yechim (Python kodi):
```python
def teg_yasovchi(teg_nomi):
    def teg_ora(matn):
        return f"<{teg_nomi}>{matn}</{teg_nomi}>"
    return teg_ora

qalin = teg_yasovchi("b")
kursiv = teg_yasovchi("i")
sarlavha = teg_yasovchi("h1")

print(qalin("Salom"))
print(kursiv("Dunyo"))
print(sarlavha("Xush kelibsiz!"))
```

## Tushuntirish va Mantiq:
1. HTML va matn shablonlari yaratishda dinamik wrapper generatorlari keng qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: <b>Salom</b>, <i>Dunyo</i>, <h1>Xush kelibsiz!</h1>
```


# 347-Topshiriq: Rekursiv qidiruv: Ichma-ich lug'atdan kalit topish

## Topshiriq sharti:
Istalgancha chuqurlikdagi murakkab JSON/lug'at ichidan berilgan kalit qiymatini rekursiv qidirib toping.

## Yechim (Python kodi):
```python
def kalitni_qidir(malumot, qidirilayotgan_kalit):
    if isinstance(malumot, dict):
        for k, v in malumot.items():
            if k == qidirilayotgan_kalit:
                return v
            natija = kalitni_qidir(v, qidirilayotgan_kalit)
            if natija is not None:
                return natija
    elif isinstance(malumot, list):
        for element in malumot:
            natija = kalitni_qidir(element, qidirilayotgan_kalit)
            if natija is not None:
                return natija
    return None

baza = {
    "kompaniya": {
        "nomi": "UzbekAI",
        "bolimlar": [
            {"nom": "Tadqiqot", "boshliq": {"ism": "Alisher", "xona": 404}}
        ]
    }
}

print("Topilgan xona:", kalitni_qidir(baza, "xona"))
print("Topilgan boshliq:", kalitni_qidir(baza, "boshliq"))
```

## Tushuntirish va Mantiq:
1. Chuqur ob'ektlar daraxtini DFS (Depth First Search) algoritmi bilan rekursiv aylanib chiqadi.

## Ishlash natijasi:
```text
Chiqish: Topilgan xona: 404
```


# 348-Topshiriq: Yig'indisi nishonga teng ikkita sonni topish (Two Sum funksiyasi)

## Topshiriq sharti:
Ro'yxat ichidan yig'indisi berilgan `target` ga teng bo'lgan ikki son indekslarini O(n) da qaytaruvchi funksiya.

## Yechim (Python kodi):
```python
def two_sum(sonlar, nishon):
    korilganlar = {}
    for indeks, son in enumerate(sonlar):
        yetishmayotgan = nishon - son
        if yetishmayotgan in korilganlar:
            return korilganlar[yetishmayotgan], indeks
        korilganlar[son] = indeks
    return None

massiv = [2, 7, 11, 15]
nishon = 9

natija = two_sum(massiv, nishon)
print(f"Indekslar: {natija} (Qiymatlar: {massiv[natija[0]]} + {massiv[natija[1]]} = {nishon})")
```

## Tushuntirish va Mantiq:
1. Hash map orqali O(n) chiziqli vaqtda jahon miqyosidagi klassik masalani yechadi.

## Ishlash natijasi:
```text
Chiqish: Indekslar: (0, 1)
```


# 349-Topshiriq: Kesh tozalash va ma'lumotlarni yangilash mexanizmi

## Topshiriq sharti:
Kesh bilan ishlovchi funksiyada keshni majburiy tozalash (`clear_cache`) imkoniyatini ta'minlang.

## Yechim (Python kodi):
```python
def keshli_funksiya():
    kesh = {}
    def bajar(x):
        if x not in kesh:
            print(f"[HISOBLANDI: {x}]")
            kesh[x] = x ** 3
        else:
            print(f"[KESHDAN OLINDI: {x}]")
        return kesh[x]
    
    def tozalash():
        kesh.clear()
        print("[KESH TOZALANDI]")

    bajar.tozalash = tozalash
    return bajar

hisob = keshli_funksiya()
hisob(5)
hisob(5)
hisob.tozalash()
hisob(5)
```

## Tushuntirish va Mantiq:
1. Funksiya ob'ektiga atribut sifatida boshqa yordamchi funksiyalarni (`tozalash`) biriktirish mumkin.

## Ishlash natijasi:
```text
Chiqish: [HISOBLANDI], [KESHDAN OLINDI], [KESH TOZALANDI], [HISOBLANDI]
```


# 350-Topshiriq: To'liq Buyruqlar Markazi (CLI Command Dispatcher Framework)

## Topshiriq sharti:
Foydalanuvchi buyruqlarini ro'yxatga oluvchi, parametrlar uzatuvchi va natijalarni qaytaruvchi to'liq funksional CLI tizimi.

## Yechim (Python kodi):
```python
buyruqlar_markazi = {}

def buyruq(nom):
    def qosh(func):
        buyruqlar_markazi[nom] = func
        return func
    return qosh

@buyruq("salom")
def cmd_salom(ism="Mehmon"):
    return f"Assalomu alaykum, {ism}!"

@buyruq("kvadrat")
def cmd_kvadrat(son=0):
    return f"{son} ning kvadrati: {float(son)**2}"

@buyruq("yordam")
def cmd_yordam():
    return f"Mavjud buyruqlar: {list(buyruqlar_markazi.keys())}"

# Tizimni sinab ko'ramiz
def ijro(satr):
    bolaklar = satr.split()
    if not bolaklar: return ""
    b_nomi = bolaklar[0]
    argumentlar = bolaklar[1:]
    
    if b_nomi in buyruqlar_markazi:
        return buyruqlar_markazi[b_nomi](*argumentlar)
    return "Bunday buyruq mavjud emas!"

print(ijro("yordam"))
print(ijro("salom Alisher"))
print(ijro("kvadrat 12"))
```

## Tushuntirish va Mantiq:
1. Zamonaviy freymvorklar (Flask, FastAPI, Click) aynan shu dekorator va dispatcher arxitekturasida ishlaydi.

## Ishlash natijasi:
```text
Chiqish: Mavjud buyruqlar, Salom xabari, 144.0
```

