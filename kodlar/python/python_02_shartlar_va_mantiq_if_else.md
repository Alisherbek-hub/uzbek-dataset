# Python Dasturlash Tili — 2-Qism: Shartlar, Mantiqiy Operatorlar va Qaror Qabul Qilish
## (51-100 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam dasturlashning eng muhim qismi — shartli mantiqni o'z ichiga oladi:
* `if`, `elif`, `else` tarmoqlanishlari;
* Mantiqiy operatorlar (`and`, `or`, `not`);
* Solishtirish amallari (`==`, `!=`, `<`, `>`, `<=`, `>=`);
* Ichma-ich joylashgan shartlar (Nested If) va Ternar operatori;
* Amaliy masalalar: shaxmat harakatlari, kalendar sanalari, soliqlar, oraliqlar va validatsiya.

---

# 51-Topshiriq: Sonning musbat, manfiy yoki nol ekanligini aniqlash

## Topshiriq sharti:
Foydalanuvchi kiritgan sonning ishorasini (musbat, manfiy yoki nol) aniqlovchi dastur yozing.

## Yechim (Python kodi):
```python
son = float(input("Sonni kiriting: "))

if son > 0:
    print(f"{son} — Musbat son")
elif son < 0:
    print(f"{son} — Manfiy son")
else:
    print("Kiritilgan son nolga teng")
```

## Tushuntirish va Mantiq:
1. `if` birinchi shartni tekshiradi (`son > 0`).
2. `elif` (else if) birinchi shart bajarilmasa ikkinchi shartni tekshiradi (`son < 0`).
3. `else` yuqoridagi barcha shartlar qanoatlanmaganda (ya'ni son nol bo'lganda) ishlaydi.

## Ishlash natijasi:
```text
Kiritish: -14.5
Chiqish: -14.5 — Manfiy son
```


# 52-Topshiriq: Ikki sondan kattasini topish

## Topshiriq sharti:
Foydalanuvchi kiritgan ikkita sondan kattasini `max()` funksiyasisiz aniqlang.

## Yechim (Python kodi):
```python
a = float(input("1-son: "))
b = float(input("2-son: "))

if a > b:
    katta = a
    print(f"Katta son: {katta}")
elif b > a:
    katta = b
    print(f"Katta son: {katta}")
else:
    print("Ikkala son o'zaro teng")
```

## Tushuntirish va Mantiq:
1. `a > b` sharti orqali birinchi son kattaligi tekshiriladi.
2. Agar teng bo'lsa, `else` bloki ishga tushadi.

## Ishlash natijasi:
```text
Kiritish: a = 25, b = 40
Chiqish: Katta son: 40.0
```


# 53-Topshiriq: Uchta sondan eng kattasini topish

## Topshiriq sharti:
Kiritilgan uchta sondan eng kattasini shart operatorlari orqali toping.

## Yechim (Python kodi):
```python
a = float(input("a: "))
b = float(input("b: "))
c = float(input("c: "))

if a >= b and a >= c:
    eng_katta = a
elif b >= a and b >= c:
    eng_katta = b
else:
    eng_katta = c

print(f"Eng katta son: {eng_katta}")
```

## Tushuntirish va Mantiq:
1. `and` mantiqiy operatori har ikkala shart bir vaqtda to'g'ri bo'lishini talab qiladi.
2. `a >= b and a >= c` bo'lsa, eng katta son shubhasiz `a` hisoblanadi.

## Ishlash natijasi:
```text
Kiritish: a = 12, b = 45, c = 33
Chiqish: Eng katta son: 45.0
```


# 54-Topshiriq: Kabisa yilini aniqlash

## Topshiriq sharti:
Kiritilgan yilning kabisa yili (366 kun) yoki oddiy yil (365 kun) ekanligini tekshiring.

## Yechim (Python kodi):
```python
yil = int(input("Yilni kiriting (masalan, 2024): "))

# Kabisa yili qoidasi:
# 400 ga bo'linsa — kabisa;
# 4 ga bo'linib, 100 ga bo'linmasa — kabisa; aks holda oddiy.
if (yil % 400 == 0) or (yil % 4 == 0 and yil % 100 != 0):
    print(f"{yil}-yil — Kabisa yili (366 kun, fevral 29 kun)")
else:
    print(f"{yil}-yil — Oddiy yil (365 kun, fevral 28 kun)")
```

## Tushuntirish va Mantiq:
1. Grigorian taqvimi bo'yicha yuz yilliklar (1900, 2100) faqat 400 ga bo'linsagina kabisa hisoblanadi (1600, 2000, 2400).
2. Qolgan yillar uchun 4 ga qoldiqsiz bo'linish yetarli.

## Ishlash natijasi:
```text
Kiritish: 2024 -> Chiqish: 2024-yil — Kabisa yili
Kiritish: 1900 -> Chiqish: 1900-yil — Oddiy yil
```


# 55-Topshiriq: Imtihon bahosini ballga qarab chiqarish

## Topshiriq sharti:
Foydalanuvchining imtihon bali (0-100) kiritilganda uning harfli bahosini chiqaring.

## Yechim (Python kodi):
```python
ball = float(input("Imtihon balingizni kiriting (0-100): "))

if ball < 0 or ball > 100:
    print("Xatolik: Ball 0 dan 100 gacha bo'lishi kerak!")
elif ball >= 90:
    print("Baho: A (A'lo)")
elif ball >= 80:
    print("Baho: B (Yaxshi)")
elif ball >= 70:
    print("Baho: C (Qoniqarli)")
elif ball >= 60:
    print("Baho: D (Yetarli)")
else:
    print("Baho: F (Qoniqarsiz - Yiqildi)")
```

## Tushuntirish va Mantiq:
1. Avval noto'g'ri oraliqdagi qiymatlar tekshiriladi (`ball < 0 or ball > 100`).
2. Shartlar yuqoridan pastga (90, 80, 70...) ketma-ket tekshiriladi.

## Ishlash natijasi:
```text
Kiritish: 86.5 -> Chiqish: Baho: B (Yaxshi)
```


# 56-Topshiriq: Chipta narxini yoshga qarab hisoblash

## Topshiriq sharti:
Yoshga qarab: 7 yoshgacha bepul, 7-17 yoshgacha 10,000 so'm, 18-60 yoshgacha 25,000 so'm, 60 dan yuqori 15,000 so'm.

## Yechim (Python kodi):
```python
yosh = int(input("Yoshingiz: "))
if yosh < 7:
    narx = 0
elif yosh <= 17:
    narx = 10000
elif yosh <= 60:
    narx = 25000
else:
    narx = 15000
print(f"Chipta narxi: {narx:,} so'm")
```

## Tushuntirish va Mantiq:
Yosh toifalarini ajratish va narxlash.

## Ishlash natijasi:
```text
Kiritish: 15 -> Chiqish: 10,000 so'm
```


# 57-Topshiriq: Uchburchak mavjudlik shartini tekshirish

## Topshiriq sharti:
Uchburchak tomonlari a, b, c berilgan. Bunday uchburchak mavjud bo'la oladimi?

## Yechim (Python kodi):
```python
a = float(input("a: "))
b = float(input("b: "))
c = float(input("c: "))
if (a + b > c) and (a + c > b) and (b + c > a):
    print("Bunday uchburchak mavjud")
else:
    print("Bunday uchburchak mavjud emas!")
```

## Tushuntirish va Mantiq:
Uchburchak tengsizligi: ixtiyoriy ikki tomon yig'indisi uchinchisidan katta bo'lishi shart.

## Ishlash natijasi:
```text
Kiritish: 3, 4, 10 -> Chiqish: Mavjud emas!
```


# 58-Topshiriq: Uchburchak turini aniqlash

## Topshiriq sharti:
Mavjud uchburchakning tomonlariga qarab turini toping: teng tomonli, teng yonli yoki turli tomonli.

## Yechim (Python kodi):
```python
a, b, c = float(input("a: ")), float(input("b: ")), float(input("c: "))
if a == b == c:
    print("Teng tomonli uchburchak")
elif a == b or a == c or b == c:
    print("Teng yonli uchburchak")
else:
    print("Turli tomonli uchburchak")
```

## Tushuntirish va Mantiq:
Tomonlar tengligi solishtiriladi.

## Ishlash natijasi:
```text
Kiritish: 5, 5, 8 -> Chiqish: Teng yonli uchburchak
```


# 59-Topshiriq: To'g'ri burchakli uchburchakni Pifagor bo'yicha tekshirish

## Topshiriq sharti:
Berilgan uch tomon to'g'ri burchakli uchburchak hosil qila oladimi?

## Yechim (Python kodi):
```python
tom = sorted([float(input(f"{i+1}-tomon: ")) for i in range(3)])
if round(tom[0]**2 + tom[1]**2, 5) == round(tom[2]**2, 5):
    print("To'g'ri burchakli uchburchak!")
else:
    print("To'g'ri burchakli emas.")
```

## Tushuntirish va Mantiq:
Kichik ikki tomon kvadratlari yig'indisi eng katta tomon kvadratiga teng bo'lishi kerak.

## Ishlash natijasi:
```text
Kiritish: 3, 4, 5 -> Chiqish: To'g'ri burchakli uchburchak!
```


# 60-Topshiriq: Oy raqamiga qarab faslni aniqlash

## Topshiriq sharti:
Oy raqami (1-12) berilganda faslni (Qish, Bahor, Yoz, Kuz) chiqaring.

## Yechim (Python kodi):
```python
oy = int(input("Oy raqami (1-12): "))
if oy in [12, 1, 2]:
    print("Fasl: Qish")
elif oy in [3, 4, 5]:
    print("Fasl: Bahor")
elif oy in [6, 7, 8]:
    print("Fasl: Yoz")
elif oy in [9, 10, 11]:
    print("Fasl: Kuz")
else:
    print("Noto'g'ri oy raqami!")
```

## Tushuntirish va Mantiq:
`in` operatori ro'yxat ichida element borligini tekshiradi.

## Ishlash natijasi:
```text
Kiritish: 4 -> Chiqish: Bahor
```


# 61-Topshiriq: Oy raqamiga qarab kunlar soni

## Topshiriq sharti:
Oy raqamiga qarab unda necha kun borligini toping (fevral uchun 28 yoki 29).

## Yechim (Python kodi):
```python
oy = int(input("Oy (1-12): "))
if oy in [1, 3, 5, 7, 8, 10, 12]:
    print("Bu oyda 31 kun bor")
elif oy in [4, 6, 9, 11]:
    print("Bu oyda 30 kun bor")
elif oy == 2:
    print("Bu oyda 28 yoki 29 kun bor (kabisa yiliga qarab)")
else:
    print("Xato oy raqami!")
```

## Tushuntirish va Mantiq:
Kalendardagi oylarning davomiyligi bo'yicha guruhlash.

## Ishlash natijasi:
```text
Kiritish: 2 -> Chiqish: 28 yoki 29 kun
```


# 62-Topshiriq: Hafta kunini raqamiga qarab nomlash

## Topshiriq sharti:
1 dan 7 gacha raqam kiritilganda hafta kunini nomini chiqaring.

## Yechim (Python kodi):
```python
kun = int(input("Hafta kuni raqami (1-7): "))
kunlar = {1: "Dushanba", 2: "Seshanba", 3: "Chorshanba", 4: "Payshanba", 5: "Juma", 6: "Shanba", 7: "Yakshanba"}
if 1 <= kun <= 7:
    print(f"Bugun: {kunlar[kun]}")
else:
    print("Bunday hafta kuni yo'q!")
```

## Tushuntirish va Mantiq:
Lug'at yoki if sharti orqali tekshirish.

## Ishlash natijasi:
```text
Kiritish: 5 -> Chiqish: Juma
```


# 63-Topshiriq: Kvadrat tenglama ildizlarini hisoblash

## Topshiriq sharti:
ax^2 + bx + c = 0 kvadrat tenglamaning diskriminantiga qarab haqiqiy ildizlarini toping.

## Yechim (Python kodi):
```python
import math
a, b, c = float(input("a: ")), float(input("b: ")), float(input("c: "))
D = b**2 - 4*a*c
if D > 0:
    x1 = (-b + math.sqrt(D)) / (2*a)
    x2 = (-b - math.sqrt(D)) / (2*a)
    print(f"Ikkita haqiqiy ildiz: x1 = {x1:.2f}, x2 = {x2:.2f}")
elif D == 0:
    x = -b / (2*a)
    print(f"Bitta ildiz: x = {x:.2f}")
else:
    print("Haqiqiy ildizlar yo'q (D < 0)")
```

## Tushuntirish va Mantiq:
Diskriminant qiymatiga qarab shartli tarmoqlanish.

## Ishlash natijasi:
```text
Kiritish: 1, -5, 6 -> Chiqish: x1 = 3.00, x2 = 2.00
```


# 64-Topshiriq: Parol mustahkamligini tekshirish

## Topshiriq sharti:
Parol uzunligi kamida 8 ta, raqam va harflar qatnashgan bo'lishi shart.

## Yechim (Python kodi):
```python
p = input("Parol kiriting: ")
has_digit = any(c.isdigit() for c in p)
has_alpha = any(c.isalpha() for c in p)
if len(p) >= 8 and has_digit and has_alpha:
    print("Parol qabul qilindi (Mustahkam)")
else:
    print("Parol zaif! Kamida 8 belgi, harf va raqam bo'lishi shart.")
```

## Tushuntirish va Mantiq:
Xavfsizlik talablarini tekshirish.

## Ishlash natijasi:
```text
Kiritish: python2026 -> Chiqish: Qabul qilindi
```


# 65-Topshiriq: Nuqtaning choragini aniqlash

## Topshiriq sharti:
(x, y) koordinatalari bo'yicha nuqtaning qaysi koordinata choragida joylashganini toping.

## Yechim (Python kodi):
```python
x, y = float(input("x: ")), float(input("y: "))
if x > 0 and y > 0: print("I chorak")
elif x < 0 and y > 0: print("II chorak")
elif x < 0 and y < 0: print("III chorak")
elif x > 0 and y < 0: print("IV chorak")
else: print("Nuqta koordinata o'qida yotadi")
```

## Tushuntirish va Mantiq:
Dekart tekisligidagi choraklar qoidasi.

## Ishlash natijasi:
```text
Kiritish: -3, 5 -> Chiqish: II chorak
```


# 66-Topshiriq: FizzBuzz masalasi

## Topshiriq sharti:
Son 3 ga bo'linsa 'Fizz', 5 ga bo'linsa 'Buzz', ikkalasiga ham bo'linsa 'FizzBuzz' chiqaring.

## Yechim (Python kodi):
```python
n = int(input("Son: "))
if n % 15 == 0: print("FizzBuzz")
elif n % 3 == 0: print("Fizz")
elif n % 5 == 0: print("Buzz")
else: print(n)
```

## Tushuntirish va Mantiq:
Eng qat'iy shart (`n % 15 == 0`) har doim birinchi tekshiriladi.

## Ishlash natijasi:
```text
Kiritish: 15 -> Chiqish: FizzBuzz
```


# 67-Topshiriq: Unli yoki undosh harfni aniqlash

## Topshiriq sharti:
Kiritilgan bitta o'zbek lotin harfining unli yoki undoshligini toping.

## Yechim (Python kodi):
```python
h = input("Bitta harf: ").lower()
unlilar = "aeiouo'e"
if len(h) == 1 and h.isalpha():
    print("Unli harf" if h in unlilar else "Undosh harf")
else: print("Noto'g'ri belgi")
```

## Tushuntirish va Mantiq:
Unlilar to'plami bilan a'zolik tekshiruvi.

## Ishlash natijasi:
```text
Kiritish: a -> Chiqish: Unli harf
```


# 68-Topshiriq: Ikki xonali sonning qaysi raqami katta

## Topshiriq sharti:
Ikki xonali sonning o'nligi kattami yoki birligimi ekanini aniqlang.

## Yechim (Python kodi):
```python
n = int(input("Ikki xonali son: "))
on, bir = n // 10, n % 10
if on > bir: print(f"O'nliklar xonasi katta ({on} > {bir})")
elif bir > on: print(f"Birliklar xonasi katta ({bir} > {on})")
else: print(f"Raqamlari teng ({on} == {bir})")
```

## Tushuntirish va Mantiq:
Xonalar ajratilib solishtiriladi.

## Ishlash natijasi:
```text
Kiritish: 82 -> Chiqish: O'nliklar katta (8 > 2)
```


# 69-Topshiriq: Uchta sonning o'rtanchasini (median) topish

## Topshiriq sharti:
Uchta turli sondan qiymat jihatidan o'rtacha bo'lganini toping.

## Yechim (Python kodi):
```python
a, b, c = float(input("a: ")), float(input("b: ")), float(input("c: "))
orta = sorted([a, b, c])[1]
print(f"O'rtancha son: {orta}")
```

## Tushuntirish va Mantiq:
Tartiblangan ro'yxatning 1-indeksidagi element medianadir.

## Ishlash natijasi:
```text
Kiritish: 10, 5, 20 -> Chiqish: 10.0
```


# 70-Topshiriq: Sonning xonalar sonini aniqlash

## Topshiriq sharti:
Butun musbat sonning 1 xonali, 2 xonali, 3 xonali yoki undan katta ekanligini toping.

## Yechim (Python kodi):
```python
n = int(input("Son: "))
if n < 10: print("1 xonali son")
elif n < 100: print("2 xonali son")
elif n < 1000: print("3 xonali son")
else: print("Ko'p xonali son")
```

## Tushuntirish va Mantiq:
Oraliq shartlari orqali aniqlash.

## Ishlash natijasi:
```text
Kiritish: 450 -> Chiqish: 3 xonali son
```


# 71-Topshiriq: Vaqtni validatsiya qilish

## Topshiriq sharti:
Kiritilgan soat (0-23) va minut (0-59) haqiqiy vaqtga to'g'ri kelishini tekshiring.

## Yechim (Python kodi):
```python
s, m = int(input("Soat: ")), int(input("Minut: "))
if 0 <= s <= 23 and 0 <= m <= 59:
    print(f"To'g'ri vaqt: {s:02d}:{m:02d}")
else: print("Noto'g'ri vaqt formati!")
```

## Tushuntirish va Mantiq:
Vaqt oraliqlarini chegaraviy tekshirish.

## Ishlash natijasi:
```text
Kiritish: 25:10 -> Chiqish: Noto'g'ri vaqt!
```


# 72-Topshiriq: Sana haqiqiyligini tekshirish

## Topshiriq sharti:
Kun, oy va yil kiritilganda uning kalendarda mavjudligini tekshiring.

## Yechim (Python kodi):
```python
from datetime import datetime
k, o, y = int(input("Kun: ")), int(input("Oy: ")), int(input("Yil: "))
try:
    sana = datetime(y, o, k)
    print(f"Sana haqiqiy: {sana.strftime('%d.%m.%Y')}")
except ValueError:
    print("Bunday sana mavjud emas!")
```

## Tushuntirish va Mantiq:
`datetime` orqali to'liq kalendar qoidalari avtomatik tekshiriladi.

## Ishlash natijasi:
```text
Kiritish: 29.02.2023 -> Chiqish: Mavjud emas!
```


# 73-Topshiriq: Shaxmat taxtasida ikki katak rangi bir xilligi

## Topshiriq sharti:
Shaxmat taxtasidagi (x1, y1) va (x2, y2) kataklarining rangi bir xil ekanligini aniqlang (1 dan 8 gacha).

## Yechim (Python kodi):
```python
x1, y1 = int(input("x1: ")), int(input("y1: "))
x2, y2 = int(input("x2: ")), int(input("y2: "))
if (x1 + y1) % 2 == (x2 + y2) % 2:
    print("Kataklar rangi bir xil")
else:
    print("Kataklar rangi har xil")
```

## Tushuntirish va Mantiq:
Shaxmatda koordinatalar yig'indisining juft-toqligi katak rangini belgilaydi.

## Ishlash natijasi:
```text
Kiritish: (1,1) va (2,2) -> Chiqish: Bir xil
```


# 74-Topshiriq: Shaxmatda Shoh yurishi

## Topshiriq sharti:
Shoh (x1, y1) dan (x2, y2) ga bir yurishda o'ta oladimi?

## Yechim (Python kodi):
```python
x1, y1 = int(input("x1: ")), int(input("y1: "))
x2, y2 = int(input("x2: ")), int(input("y2: "))
if max(abs(x2 - x1), abs(y2 - y1)) == 1:
    print("Shoh yura oladi")
else: print("Shoh yura olmaydi")
```

## Tushuntirish va Mantiq:
Shoh istalgan tomonga faqat 1 katak siljishi mumkin.

## Ishlash natijasi:
```text
Kiritish: (4,4) dan (5,5) ga -> Chiqish: Yura oladi
```


# 75-Topshiriq: Shaxmatda Ruh (to'ra) yurishi

## Topshiriq sharti:
Ruh (x1, y1) dan (x2, y2) ga bir yurishda o'ta oladimi?

## Yechim (Python kodi):
```python
x1, y1 = int(input("x1: ")), int(input("y1: "))
x2, y2 = int(input("x2: ")), int(input("y2: "))
if x1 == x2 or y1 == y2:
    print("Ruh yura oladi")
else: print("Ruh yura olmaydi")
```

## Tushuntirish va Mantiq:
Ruh faqat gorizontal yoki vertikal bo'yicha harakatlanadi.

## Ishlash natijasi:
```text
Kiritish: (1,1) dan (1,7) ga -> Chiqish: Yura oladi
```


# 76-Topshiriq: Shaxmatda Fil yurishi

## Topshiriq sharti:
Fil (x1, y1) dan (x2, y2) ga bir yurishda o'ta oladimi?

## Yechim (Python kodi):
```python
x1, y1 = int(input("x1: ")), int(input("y1: "))
x2, y2 = int(input("x2: ")), int(input("y2: "))
if abs(x2 - x1) == abs(y2 - y1) and (x1, y1) != (x2, y2):
    print("Fil yura oladi")
else: print("Fil yura olmaydi")
```

## Tushuntirish va Mantiq:
Fil faqat diagonallar bo'ylab yuradi (koordinatalar farqi teng bo'ladi).

## Ishlash natijasi:
```text
Kiritish: (2,2) dan (5,5) ga -> Chiqish: Yura oladi
```


# 77-Topshiriq: Shaxmatda Farzin yurishi

## Topshiriq sharti:
Farzin bir yurishda (x1, y1) dan (x2, y2) ga o'ta oladimi?

## Yechim (Python kodi):
```python
x1, y1 = int(input("x1: ")), int(input("y1: "))
x2, y2 = int(input("x2: ")), int(input("y2: "))
ruh = (x1 == x2 or y1 == y2)
fil = abs(x2 - x1) == abs(y2 - y1)
if (ruh or fil) and (x1, y1) != (x2, y2):
    print("Farzin yura oladi")
else: print("Farzin yura olmaydi")
```

## Tushuntirish va Mantiq:
Farzin Ruh va Filning imkoniyatlarini birlashtiradi.

## Ishlash natijasi:
```text
Kiritish: (4,4) dan (4,8) ga -> Chiqish: Yura oladi
```


# 78-Topshiriq: Shaxmatda Ot yurishi

## Topshiriq sharti:
Ot (Knight) (x1, y1) dan (x2, y2) ga 'G' shaklida yura oladimi?

## Yechim (Python kodi):
```python
x1, y1 = int(input("x1: ")), int(input("y1: "))
x2, y2 = int(input("x2: ")), int(input("y2: "))
dx, dy = abs(x2 - x1), abs(y2 - y1)
if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
    print("Ot yura oladi")
else: print("Ot yura olmaydi")
```

## Tushuntirish va Mantiq:
Otning harakati har doim 1 va 2 katakli siljishdan iborat.

## Ishlash natijasi:
```text
Kiritish: (1,1) dan (2,3) ga -> Chiqish: Yura oladi
```


# 79-Topshiriq: BMI toifasini aniqlash

## Topshiriq sharti:
BMI ko'rsatkichiga qarab inson vaznining tibbiy holatini chiqaring.

## Yechim (Python kodi):
```python
bmi = float(input("BMI qiymati: "))
if bmi < 18.5: print("Vazn yetishmasligi")
elif bmi < 25: print("Normal vazn")
elif bmi < 30: print("Ortiqcha vazn")
else: print("Semizlik")
```

## Tushuntirish va Mantiq:
Jahon sog'liqni saqlash tashkiloti standartlari.

## Ishlash natijasi:
```text
Kiritish: 23.4 -> Chiqish: Normal vazn
```


# 80-Topshiriq: Progressiv daromad solig'i hisobi

## Topshiriq sharti:
Daromad 3 mln gacha 0%, 3-10 mln orasi 12%, 10 mln dan ortig'i 20% soliqqa tortilsin.

## Yechim (Python kodi):
```python
d = float(input("Daromad: "))
if d <= 3000000:
    s = 0
elif d <= 10000000:
    s = (d - 3000000) * 0.12
else:
    s = 7000000 * 0.12 + (d - 10000000) * 0.20
print(f"To'lanadigan soliq: {s:,.2f} so'm")
```

## Tushuntirish va Mantiq:
Pog'onali soliq solish tizimi.

## Ishlash natijasi:
```text
Kiritish: 5,000,000 -> Chiqish: 240,000.00 so'm
```


# 81-Topshiriq: Bank krediti olish huquqi

## Topshiriq sharti:
Mijoz 21 yoshdan katta, oyligi kamida 4 mln va muddati o'tgan qarzi bo'lmasa kredit berilsin.

## Yechim (Python kodi):
```python
yosh = int(input("Yosh: "))
maosh = float(input("Oylik daromad: "))
qarz = input("Qarzingiz bormi (ha/yo'q): ").lower() == 'ha'
if yosh >= 21 and maosh >= 4000000 and not qarz:
    print("Kredit tasdiqlandi!")
else:
    print("Kredit rad etildi.")
```

## Tushuntirish va Mantiq:
Skoring shartlarini tekshirish.

## Ishlash natijasi:
```text
Kiritish: 25 yosh, 5 mln, qarzi yo'q -> Chiqish: Tasdiqlandi!
```


# 82-Topshiriq: Bankomatdan pul yechish va komissiya

## Topshiriq sharti:
Balansdan so'ralgan summani 1% komissiya bilan yechish mumkinligini tekshiring.

## Yechim (Python kodi):
```python
balans = float(input("Balans: "))
sur = float(input("Yechiladigan summa: "))
jami = sur * 1.01
if balans >= jami:
    print(f"Muvaffaqiyatli! Qoldiq: {balans - jami:,.2f} so'm")
else: print("Mablag' yetarli emas!")
```

## Tushuntirish va Mantiq:
Tranzaksiya xarajatlari bilan hisob tekshiruvi.

## Ishlash natijasi:
```text
Kiritish: Balans 100 ming, so'ralgan 100 ming -> Chiqish: Mablag' yetarli emas (chunki 101 ming kerak)
```


# 83-Topshiriq: 24 soatlik formatni 12 soatlik (AM/PM) ga o'girish

## Topshiriq sharti:
0 dan 23 gacha soat kiritilganda AM/PM shaklida ifodalang.

## Yechim (Python kodi):
```python
s = int(input("Soat (0-23): "))
if s == 0: print("12 AM (Yarim tun)")
elif s < 12: print(f"{s} AM")
elif s == 12: print("12 PM (Peshin)")
else: print(f"{s - 12} PM")
```

## Tushuntirish va Mantiq:
Xalqaro vaqt formatiga o'tkazish.

## Ishlash natijasi:
```text
Kiritish: 15 -> Chiqish: 3 PM
```


# 84-Topshiriq: Haroratga qarab kiyinish tavsiyasi

## Topshiriq sharti:
Haroratga qarab foydalanuvchiga nima kiyish kerakligini tavsiya qiling.

## Yechim (Python kodi):
```python
t = float(input("Harorat (°C): "))
if t < 0: print("Qalin palto va shlyapa kiying!")
elif t < 15: print("Kurtka yoki jemper kiying.")
elif t < 25: print("Ko'ylak yoki yengil kiyim qulay.")
else: print("Juda issiq! Yengil futbolka kiying.")
```

## Tushuntirish va Mantiq:
Qaror qabul qilish mantig'i.

## Ishlash natijasi:
```text
Kiritish: 8 -> Chiqish: Kurtka kiying
```


# 85-Topshiriq: Palindrom sonni tekshirish

## Topshiriq sharti:
Butun sonning o'ngdan va chapdan bir xil o'qilishini tekshiring (masalan, 1221).

## Yechim (Python kodi):
```python
s = input("Son: ")
if s == s[::-1]:
    print("Palindrom son!")
else: print("Palindrom emas.")
```

## Tushuntirish va Mantiq:
Satrni teskari o'girish (`[::-1]`) orqali taqqoslash.

## Ishlash natijasi:
```text
Kiritish: 1331 -> Chiqish: Palindrom son!
```


# 86-Topshiriq: Baxtli chipta masalasi

## Topshiriq sharti:
4 xonali chipta raqamining dastlabki 2 ta raqami yig'indisi oxirgi 2 tasiga tengmi?

## Yechim (Python kodi):
```python
c = input("4 xonali chipta: ")
if len(c) == 4 and c.isdigit():
    if int(c[0]) + int(c[1]) == int(c[2]) + int(c[3]):
        print("Baxtli chipta!")
    else: print("Oddiy chipta.")
```

## Tushuntirish va Mantiq:
Raqamlar yig'indisi taqqoslanadi.

## Ishlash natijasi:
```text
Kiritish: 3517 -> Chiqish: Baxtli chipta (3+5 == 1+7)
```


# 87-Topshiriq: Yetkazib berish narxini hisoblash

## Topshiriq sharti:
Buyurtma summasi 100,000 so'mdan oshsa yetkazib berish bepul, aks holda 15,000 so'm.

## Yechim (Python kodi):
```python
b = float(input("Buyurtma summasi: "))
yetk = 0 if b >= 100000 else 15000
print(f"Yetkazib berish: {yetk:,} so'm | Jami: {b + yetk:,} so'm")
```

## Tushuntirish va Mantiq:
Ternar shart operatori yordamida tezkor hisob.

## Ishlash natijasi:
```text
Kiritish: 80,000 -> Chiqish: Yetkazib berish: 15,000 so'm
```


# 88-Topshiriq: Login va parolni tekshirish

## Topshiriq sharti:
To'g'ri login 'admin' va parol 'secret123' bo'lsa tizimga kiritilsin.

## Yechim (Python kodi):
```python
login = input("Login: ")
parol = input("Parol: ")
if login == "admin" and parol == "secret123":
    print("Xush kelibsiz, Admin!")
else:
    print("Login yoki parol xato!")
```

## Tushuntirish va Mantiq:
Autentifikatsiya mantig'i.

## Ishlash natijasi:
```text
Kiritish: admin, secret123 -> Chiqish: Xush kelibsiz!
```


# 89-Topshiriq: Stop so'zlarni aniqlash

## Topshiriq sharti:
Foydalanuvchi xabarida taqiqlangan so'zlar borligini tekshiring.

## Yechim (Python kodi):
```python
xabar = input("Xabarni kiriting: ").lower()
taqiqlangan = ["spam", "reklama", "yutuq"]
if any(soz in xabar for soz in taqiqlangan):
    print("Xabar bloklandi (Taqiqlangan so'z bor)!")
else: print("Xabar yuborildi.")
```

## Tushuntirish va Mantiq:
Filtr va moderatsiya tizimi.

## Ishlash natijasi:
```text
Kiritish: Sizda yutuq bor -> Chiqish: Xabar bloklandi!
```


# 90-Topshiriq: GPA bo'yicha stipendiya belgilash

## Topshiriq sharti:
GPA 4.5 dan yuqori bo'lsa 'A'lochi', 3.5 dan yuqori bo'lsa 'Oddiy', aks holda stipendiya yo'q.

## Yechim (Python kodi):
```python
gpa = float(input("GPA (0-5): "))
if gpa >= 4.5: print("100% stipendiya (A'lochi)")
elif gpa >= 3.5: print("Standart stipendiya")
else: print("Stipendiya berilmaydi")
```

## Tushuntirish va Mantiq:
Akademik ko'rsatkichlarni toifalash.

## Ishlash natijasi:
```text
Kiritish: 4.8 -> Chiqish: 100% stipendiya
```


# 91-Topshiriq: Tezlik oshirilgan jarima miqdori

## Topshiriq sharti:
Ruxsat etilgan tezlik 60 km/soat. Oshirilgan tezlikka qarab jarimani aniqlang.

## Yechim (Python kodi):
```python
tezlik = float(input("Haqiqiy tezlik (km/soat): "))
osgan = tezlik - 60
if osgan <= 0: print("Qoida buzilmadi.")
elif osgan <= 20: print("Jarima: BHM ning 1 baravari (340,000 so'm)")
elif osgan <= 40: print("Jarima: BHM ning 5 baravari (1,700,000 so'm)")
else: print("Jarima: BHM ning 9 baravari (3,060,000 so'm)")
```

## Tushuntirish va Mantiq:
Yo'l harakati qoidalari jarimalari.

## Ishlash natijasi:
```text
Kiritish: 85 km/soat -> Chiqish: 5 baravar
```


# 92-Topshiriq: Poyezd chiptasiga talabalar chegirmasi

## Topshiriq sharti:
Talabalar uchun 50% chegirma, pensionerlar uchun 30% chegirma berilsin.

## Yechim (Python kodi):
```python
asos = float(input("Chipta narxi: "))
status = input("Maqomingiz (talaba/pensioner/oddiy): ").lower()
if status == "talaba": narx = asos * 0.5
elif status == "pensioner": narx = asos * 0.7
else: narx = asos
print(f"To'lanadigan summa: {narx:,.2f} so'm")
```

## Tushuntirish va Mantiq:
Ijtimoiy chegirmalar hisoblash.

## Ishlash natijasi:
```text
Kiritish: 200 ming, talaba -> Chiqish: 100,000.00 so'm
```


# 93-Topshiriq: Belgi turini aniqlash

## Topshiriq sharti:
Kiritilgan belgi lotin harfi, raqam yoki maxsus belgi ekanini aniqlang.

## Yechim (Python kodi):
```python
b = input("Bitta belgi: ")
if b.isalpha(): print("Lotin harfi")
elif b.isdigit(): print("Raqam")
else: print("Maxsus belgi yoki punktuatsiya")
```

## Tushuntirish va Mantiq:
Belgilar klassifikatsiyasi.

## Ishlash natijasi:
```text
Kiritish: # -> Chiqish: Maxsus belgi
```


# 94-Topshiriq: To'g'ri to'rtburchaklar kesishishi

## Topshiriq sharti:
Ikkita to'g'ri to'rtburchak koordinatalari bo'yicha ularning umumiy qismi borligini tekshiring.

## Yechim (Python kodi):
```python
# [x1, y1, x2, y2] formatida
r1 = [0, 0, 4, 4]
r2 = [2, 2, 6, 6]
kesishadi = not (r1[2] < r2[0] or r1[0] > r2[2] or r1[3] < r2[1] or r1[1] > r2[3])
print("To'rtburchaklar kesishadi!" if kesishadi else "Kesishmaydi.")
```

## Tushuntirish va Mantiq:
Geometrik to'qnashuvlar (AABB Collision Detection) algoritmi.

## Ishlash natijasi:
```text
Chiqish: Kesishadi!
```


# 95-Topshiriq: Nuqtaning doira ichida yotishi

## Topshiriq sharti:
(x, y) nuqta R radiusli markazi (0,0) da bo'lgan doira ichidami?

## Yechim (Python kodi):
```python
x, y, R = float(input("x: ")), float(input("y: ")), float(input("Radius: "))
if x**2 + y**2 <= R**2:
    print("Nuqta doira ichida (yoki chegarasida) yotadi")
else: print("Nuqta doiradan tashqarida")
```

## Tushuntirish va Mantiq:
Analitik geometriyada doira tenglamasi.

## Ishlash natijasi:
```text
Kiritish: (1, 1), R = 2 -> Chiqish: Doira ichida
```


# 96-Topshiriq: Tabaqalashtirilgan elektr energiyasi tarifi

## Topshiriq sharti:
200 kVt gacha 450 so'm, undan ortig'i 900 so'mdan hisoblansin.

## Yechim (Python kodi):
```python
kvt = float(input("Sarflangan elektr (kVt*soat): "))
if kvt <= 200:
    t = kvt * 450
else:
    t = 200 * 450 + (kvt - 200) * 900
print(f"Jami elektr to'lovi: {t:,.2f} so'm")
```

## Tushuntirish va Mantiq:
Ijtimoiy me'yor bo'yicha tabaqalashgan to'lov.

## Ishlash natijasi:
```text
Kiritish: 250 kVt -> Chiqish: 135,000.00 so'm
```


# 97-Topshiriq: O'zbekiston mobil operatorini aniqlash

## Topshiriq sharti:
Telefon raqami kodi bo'yicha operatorni (Ucell, Beeline, UMS/Mobiuz, Uztelecom) aniqlang.

## Yechim (Python kodi):
```python
kod = input("Operator kodi (masalan, 90, 93, 99): ").strip()
if kod in ["90", "91"]: print("Operator: Beeline")
elif kod in ["93", "94"]: print("Operator: Ucell")
elif kod in ["97", "88"]: print("Operator: Mobiuz")
elif kod in ["99", "95", "77"]: print("Operator: Uztelecom")
else: print("Noma'lum operator kodi")
```

## Tushuntirish va Mantiq:
Kodlar bo'yicha telekommunikatsiya yo'naltirish.

## Ishlash natijasi:
```text
Kiritish: 93 -> Chiqish: Ucell
```


# 98-Topshiriq: Zodiak (Burj) belgisini aniqlash

## Topshiriq sharti:
Tug'ilgan kun va oyga qarab insonning burj belgisini toping.

## Yechim (Python kodi):
```python
kun = int(input("Kun: "))
oy = int(input("Oy (1-12): "))
if (oy == 3 and kun >= 21) or (oy == 4 and kun <= 19): burj = "Qo'y (Aries)"
elif (oy == 4 and kun >= 20) or (oy == 5 and kun <= 20): burj = "Buzoq (Taurus)"
elif (oy == 5 and kun >= 21) or (oy == 6 and kun <= 21): burj = "Egizaklar (Gemini)"
elif (oy == 6 and kun >= 22) or (oy == 7 and kun <= 22): burj = "Qisqichbaqa (Cancer)"
elif (oy == 7 and kun >= 23) or (oy == 8 and kun <= 22): burj = "Arslon (Leo)"
else: burj = "Boshqa burj belgisi"
print(f"Sizning burjingiz: {burj}")
```

## Tushuntirish va Mantiq:
Kalendar sanalari oraliqlari bo'yicha tasniflash.

## Ishlash natijasi:
```text
Kiritish: 15-aprel -> Chiqish: Qo'y (Aries)
```


# 99-Topshiriq: Mijozning sodiqlik maqomi (Loyalty Status)

## Topshiriq sharti:
Yillik xarid hajmiga qarab: 10 mln gacha Bronze, 30 mln gacha Silver, 100 mln gacha Gold, undan yuqori Platinum.

## Yechim (Python kodi):
```python
xarid = float(input("Yillik xarid miqdori: "))
if xarid < 10000000: s = "Bronze (5% keshbek)"
elif xarid < 30000000: s = "Silver (7% keshbek)"
elif xarid < 100000000: s = "Gold (10% keshbek)"
else: s = "Platinum (15% keshbek + Shaxsiy menejer)"
print(f"Sizning maqomingiz: {s}")
```

## Tushuntirish va Mantiq:
CRM va marketing sodiqlik tizimi.

## Ishlash natijasi:
```text
Kiritish: 45,000,000 -> Chiqish: Gold
```


# 100-Topshiriq: Oddiy konsol kalkulyatori

## Topshiriq sharti:
Ikki son va arifmetik belgi ('+', '-', '*', '/') kiritilganda natijani to'g'ri hisoblang.

## Yechim (Python kodi):
```python
a = float(input("1-son: "))
amal = input("Amal (+, -, *, /): ").strip()
b = float(input("2-son: "))
if amal == '+': res = a + b
elif amal == '-': res = a - b
elif amal == '*': res = a * b
elif amal == '/': res = a / b if b != 0 else "Nolga bo'lish xatosi!"
else: res = "Noma'lum amal!"
print(f"Natija: {res}")
```

## Tushuntirish va Mantiq:
Foydalanuvchi tanlagan operatorga qarab tegishli arifmetikani chaqirish.

## Ishlash natijasi:
```text
Kiritish: 12, '*', 5 -> Chiqish: 60.0
```
