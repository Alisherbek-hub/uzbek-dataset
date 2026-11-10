# Python Dasturlash Tili — 1-Qism: O'zgaruvchilar, Ma'lumot Turlari va Arifmetik Amallar
## (1-50 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam Python dasturlash tilining poydevor tushunchalarini o'z ichiga oladi:
* O'zgaruvchilar yaratish va qiymat berish;
* Satrlar (str), butun sonlar (int) va haqiqiy sonlar (float);
* Arifmetik operatorlar (`+`, `-`, `*`, `/`, `//`, `%`, `**`);
* `math` kutubxonasining asosiy funksiyalari (`sqrt`, `pi`, `radians`, `hypot`);
* Har bir vazifaning to'liq o'zbekcha sharhi va test namunalari.

---

# 1-Topshiriq: Foydalanuvchini ismi bilan qutlash

## Topshiriq sharti:
Foydalanuvchidan uning ismini so'rab olib, unga samimiy salom beruvchi dastur tuzing.

## Yechim (Python kodi):
```python
# Foydalanuvchidan ismini kiritishini so'raymiz
ism = input("Ismingizni kiriting: ")

# Qutlov matnini f-string yordamida shakllantiramiz
salom_matni = f"Assalomu alaykum, {ism}! Python olamiga xush kelibsiz!"

# Ekranga chiqaramiz
print(salom_matni)
```

## Tushuntirish va Mantiq:
1. `input()` funksiyasi klaviaturadan kiritilgan ma'lumotni satr (string) shaklida qabul qiladi.
2. `f-string` (formatlangan satr) satr ichiga o'zgaruvchi qiymatini qulay joylashtirish imkonini beradi.
3. `print()` natijani terminalga chiqaradi.

## Ishlash natijasi:
```text
Kiritish: Alisher
Chiqish: Assalomu alaykum, Alisher! Python olamiga xush kelibsiz!
```


# 2-Topshiriq: Ikki son ustida 4 ta asosiy arifmetik amal

## Topshiriq sharti:
Foydalanuvchi kiritgan ikkita haqiqiy sonning yig'indisi, ayirmasi, ko'paytmasi va bo'linmasini hisoblang.

## Yechim (Python kodi):
```python
# Ikki sonni float (haqiqiy son) shaklida kiritamiz
a = float(input("1-sonni kiriting: "))
b = float(input("2-sonni kiriting: "))

# Arifmetik amallar
yigindi = a + b
ayirma = a - b
kopaytma = a * b
bolinma = a / b if b != 0 else "Nolga bo'lish mumkin emas"

print(f"{a} + {b} = {yigindi}")
print(f"{a} - {b} = {ayirma}")
print(f"{a} * {b} = {kopaytma}")
print(f"{a} / {b} = {bolinma}")
```

## Tushuntirish va Mantiq:
1. `float()` funksiyasi kiritilgan satrni o'nlik kasr songa o'tkazadi.
2. `+`, `-`, `*`, `/` asosiy arifmetik operatorlardir.
3. Nolga bo'lish xatoligining (ZeroDivisionError) oldi shart orqali olinadi.

## Ishlash natijasi:
```text
Kiritish: 15 va 4
Chiqish:
15.0 + 4.0 = 19.0
15.0 - 4.0 = 11.0
15.0 * 4.0 = 60.0
15.0 / 4.0 = 3.75
```


# 3-Topshiriq: Butun bo'lish (//) va qoldiq olish (%) operatorlari

## Topshiriq sharti:
Ikkita butun son berilgan. Birinchi sonni ikkinchi songa bo'lgandagi butun qism va qoldiqni toping.

## Yechim (Python kodi):
```python
a = int(input("Bo'linuvchi (a): "))
b = int(input("Bo'luvchi (b): "))

butun_qism = a // b
qoldiq = a % b

print(f"Butun qism (a // b): {butun_qism}")
print(f"Qoldiq (a % b): {qoldiq}")
```

## Tushuntirish va Mantiq:
1. `//` operatori bo'linmaning faqat butun qismini oladi (floor division).
2. `%` operatori bo'lishdan qolgan qoldiqni hisoblaydi (modulo).
3. Ushbu operatorlar vaqt, raqamlarni ajratish va juft-toqlikni tekshirishda juda keng qo'llaniladi.

## Ishlash natijasi:
```text
Kiritish: a = 17, b = 5
Chiqish:
Butun qism (a // b): 3
Qoldiq (a % b): 2
```


# 4-Topshiriq: To'g'ri to'rtburchakning perimetri va yuzi

## Topshiriq sharti:
To'g'ri to'rtburchakning bo'yi va eni berilgan. Uning yuzi va perimetrini hisoblang.

## Yechim (Python kodi):
```python
a = float(input("Bo'yi (a): "))
b = float(input("Eni (b): "))

yuzi = a * b
perimetr = 2 * (a + b)

print(f"Yuzi (S): {yuzi}")
print(f"Perimetri (P): {perimetr}")
```

## Tushuntirish va Mantiq:
1. To'g'ri to'rtburchak yuzi tomonlar ko'paytmasiga teng: S = a * b.
2. Perimetri tomonlar yig'indisining ikkilanganiga teng: P = 2 * (a + b).

## Ishlash natijasi:
```text
Kiritish: a = 8, b = 5
Chiqish:
Yuzi (S): 40.0
Perimetri (P): 26.0
```


# 5-Topshiriq: Doiraning yuzi va aylananing uzunligi

## Topshiriq sharti:
Radiusi r bo'lgan doiraning yuzi va aylana uzunligini hisoblang (math kutubxonasidagi pi dan foydalaning).

## Yechim (Python kodi):
```python
import math

r = float(input("Radiusni kiriting: "))

aylana_uzunligi = 2 * math.pi * r
doira_yuzi = math.pi * (r ** 2)

print(f"Aylana uzunligi (L): {aylana_uzunligi:.2f}")
print(f"Doira yuzi (S): {doira_yuzi:.2f}")
```

## Tushuntirish va Mantiq:
1. `math.pi` konstanti pi sonining (3.14159...) aniq qiymatini beradi.
2. `r ** 2` radiusning kvadratini bildiradi.
3. `:.2f` formati natijani verguldan keyin 2 ta xonagacha yaxlitlab ko'rsatadi.

## Ishlash natijasi:
```text
Kiritish: r = 7
Chiqish:
Aylana uzunligi (L): 43.98
Doira yuzi (S): 153.94
```


# 6-Topshiriq: Pifagor teoremasi bo'yicha gipotenuzani topish

## Topshiriq sharti:
To'g'ri burchakli uchburchakning ikkita kateti berilgan. Uning gipotenuzasi uzunligini toping.

## Yechim (Python kodi):
```python
import math

a = float(input("1-katet (a): "))
b = float(input("2-katet (b): "))

# Gipotenuza: c = sqrt(a^2 + b^2)
c = math.sqrt(a**2 + b**2)
# Yoki math.hypot(a, b) dan foydalanish mumkin

print(f"Gipotenuza (c): {c}")
```

## Tushuntirish va Mantiq:
1. Pifagor teoremasi: c^2 = a^2 + b^2.
2. `math.sqrt()` sonning kvadrat ildizini hisoblaydi.
3. Python `math.hypot(a, b)` funksiyasi ham ayni shu vazifani bajaradi.

## Ishlash natijasi:
```text
Kiritish: a = 3, b = 4
Chiqish:
Gipotenuza (c): 5.0
```


# 7-Topshiriq: Gradus Selsiydan Farengeytga o'tkazish

## Topshiriq sharti:
Harorat Selsiy gradusida berilgan. Uni Farengeyt shkalasiga o'tkazuvchi dastur yozing.

## Yechim (Python kodi):
```python
celsius = float(input("Haroratni Selsiyda kiriting: "))

# Farengeyt formulasi: F = C * 9/5 + 32
fahrenheit = (celsius * 9 / 5) + 32

print(f"{celsius}°C = {fahrenheit:.1f}°F")
```

## Tushuntirish va Mantiq:
1. Fizikadagi haroratni o'zgartirish formulasi: F = C * 1.8 + 32.
2. Qavslar arifmetik amallar ketma-ketligini kafolatlaydi.

## Ishlash natijasi:
```text
Kiritish: 25
Chiqish: 25.0°C = 77.0°F
```


# 8-Topshiriq: Ikki o'zgaruvchi qiymatini uchinchi o'zgaruvchisiz almashtirish

## Topshiriq sharti:
a va b o'zgaruvchilar berilgan. Ularning qiymatlarini o'zaro almashtiring (Swap).

## Yechim (Python kodi):
```python
a = int(input("a soni: "))
b = int(input("b soni: "))

print(f"Dastlabki holat: a = {a}, b = {b}")

# Pythonik usul (tuple unpacking):
a, b = b, a

print(f"Almashtirilgandan so'ng: a = {a}, b = {b}")
```

## Tushuntirish va Mantiq:
1. Python tilida `a, b = b, a` sintaksisi o'ng tomonda kortej (tuple) hosil qilib, chap tomondagi o'zgaruvchilarga ochib beradi.
2. Bu boshqa tillardagi kabi qo'shimcha `temp` o'zgaruvchisini talab qilmaydi.

## Ishlash natijasi:
```text
Kiritish: a = 10, b = 25
Chiqish:
Dastlabki holat: a = 10, b = 25
Almashtirilgandan so'ng: a = 25, b = 10
```


# 9-Topshiriq: Uch xonali sonning raqamlari yig'indisini topish

## Topshiriq sharti:
Foydalanuvchi kiritgan uch xonali natural sonning raqamlari yig'indisini hisoblang.

## Yechim (Python kodi):
```python
n = int(input("Uch xonali son kiriting (masalan, 385): "))

yuzlar = n // 100
onlar = (n // 10) % 10
birliklar = n % 10

yigindi = yuzlar + onlar + birliklar

print(f"{n} soni raqamlari: {yuzlar} + {onlar} + {birliklar} = {yigindi}")
```

## Tushuntirish va Mantiq:
1. `n // 100` yuzlar xonasini ajratadi.
2. `(n // 10) % 10` o'nlar xonasini ajratadi.
3. `n % 10` birliklar xonasini ajratadi.

## Ishlash natijasi:
```text
Kiritish: 456
Chiqish: 456 soni raqamlari: 4 + 5 + 6 = 15
```


# 10-Topshiriq: Sekundlarni soat, daqiqa va sekundlarga ajratish

## Topshiriq sharti:
Kun boshidan boshlab o'tgan jami sekundlar berilgan. Uni soat, daqiqa va sekundlarga ajrating.

## Yechim (Python kodi):
```python
jami_sekund = int(input("Sekundlar sonini kiriting: "))

soat = jami_sekund // 3600
qolgan_sekund = jami_sekund % 3600
daqiqa = qolgan_sekund // 60
sekund = qolgan_sekund % 60

print(f"Vaqt: {soat:02d}:{daqiqa:02d}:{sekund:02d}")
```

## Tushuntirish va Mantiq:
1. 1 soatda 3600 sekund bor (`// 3600`).
2. 1 daqiqada 60 sekund bor (`// 60`).
3. `:02d` formati son 10 dan kichik bo'lsa, oldiga nol qo'shib chiqaradi (masalan, 05).

## Ishlash natijasi:
```text
Kiritish: 3665
Chiqish: Vaqt: 01:01:05
```


# 11-Topshiriq: Sonning darajasini hisoblash

## Topshiriq sharti:
Berilgan asos (a) va daraja ko'rsatkichi (n) bo'yicha a^n qiymatini hisoblang.

## Yechim (Python kodi):
```python
a = float(input("Asos (a): "))
n = int(input("Daraja (n): "))
natija = a ** n
print(f"{a} ning {n}-darajasi: {natija}")
```

## Tushuntirish va Mantiq:
Python'da darajaga ko'tarish `**` operatori yoki `pow(a, n)` funksiyasi orqali bajariladi.

## Ishlash natijasi:
```text
Kiritish: a = 2, n = 10 -> Chiqish: 1024.0
```


# 12-Topshiriq: Oddiy foizlarni hisoblash

## Topshiriq sharti:
Boshlang'ich kapital P, yillik foiz stavkasi r va muddat t (yil) berilgan. Oddiy foizlar formulasiga ko'ra yakuniy summani toping: S = P * (1 + r * t).

## Yechim (Python kodi):
```python
P = float(input("Boshlang'ich summa: "))
r = float(input("Yillik foiz (%): ")) / 100
t = float(input("Muddat (yil): "))
S = P * (1 + r * t)
print(f"Yakuniy summa: {S:.2f}")
```

## Tushuntirish va Mantiq:
Oddiy foizlar investitsiya va kredit hisob-kitoblarida bazaviy formuladir.

## Ishlash natijasi:
```text
Kiritish: P = 1000000, r = 15%, t = 2 -> Chiqish: 1300000.00
```


# 13-Topshiriq: Murakkab foizlarni hisoblash

## Topshiriq sharti:
Murakkab foizlar formulasiga ko'ra jamg'armani hisoblang: S = P * (1 + r)^t.

## Yechim (Python kodi):
```python
P = float(input("Boshlang'ich summa: "))
r = float(input("Yillik foiz (%): ")) / 100
t = int(input("Yillar soni: "))
S = P * ((1 + r) ** t)
print(f"Murakkab foiz bilan yakuniy summa: {S:.2f}")
```

## Tushuntirish va Mantiq:
Murakkab foizda har yilgi foiz daromadi asosiy kapitalga qo'shilib boradi.

## Ishlash natijasi:
```text
Kiritish: P = 1000000, r = 10%, t = 3 -> Chiqish: 1331000.00
```


# 14-Topshiriq: Kinetik energiyani hisoblash

## Topshiriq sharti:
Jismning massasi m (kg) va tezligi v (m/s) berilgan. Kinetik energiyani hisoblang: E_k = (m * v^2) / 2.

## Yechim (Python kodi):
```python
m = float(input("Massa (kg): "))
v = float(input("Tezlik (m/s): "))
Ek = (m * (v ** 2)) / 2
print(f"Kinetik energiya: {Ek:.2f} Joul")
```

## Tushuntirish va Mantiq:
Fizikadagi harakat energiyasi formulasining to'g'ridan-to'g'ri dasturiy ifodasi.

## Ishlash natijasi:
```text
Kiritish: m = 2, v = 10 -> Chiqish: 100.00 Joul
```


# 15-Topshiriq: Potensial energiyani hisoblash

## Topshiriq sharti:
Jismning massasi m (kg) va ko'tarilgan balandligi h (m) berilgan. Potensial energiyani hisoblang: E_p = m * g * h (g = 9.8).

## Yechim (Python kodi):
```python
m = float(input("Massa (kg): "))
h = float(input("Balandlik (m): "))
g = 9.8
Ep = m * g * h
print(f"Potensial energiya: {Ep:.2f} Joul")
```

## Tushuntirish va Mantiq:
Yerning tortishish maydonidagi potensial energiya hisobi.

## Ishlash natijasi:
```text
Kiritish: m = 5, h = 10 -> Chiqish: 490.00 Joul
```


# 16-Topshiriq: Sonning oxirgi raqamini aniqlash

## Topshiriq sharti:
Har qanday butun musbat sonning oxirgi raqamini aniqlovchi dastur yozing.

## Yechim (Python kodi):
```python
n = int(input("Son kiriting: "))
oxirgi = n % 10
print(f"{n} sonining oxirgi raqami: {oxirgi}")
```

## Tushuntirish va Mantiq:
O'nlik sanoq sistemasida sonni 10 ga bo'lgandagi qoldiq uning oxirgi raqamiga teng.

## Ishlash natijasi:
```text
Kiritish: 1984 -> Chiqish: 4
```


# 17-Topshiriq: O'nliklar xonasidagi raqamni topish

## Topshiriq sharti:
Butun sonning o'nliklar xonasidagi raqamini toping (masalan, 258 da 5).

## Yechim (Python kodi):
```python
n = int(input("Son kiriting: "))
onlik = (n // 10) % 10
print(f"O'nliklar xonasidagi raqam: {onlik}")
```

## Tushuntirish va Mantiq:
Avval son 10 ga bo'linib birliklar o'chiriladi, keyin 10 ga qoldiq olinadi.

## Ishlash natijasi:
```text
Kiritish: 789 -> Chiqish: 8
```


# 18-Topshiriq: To'g'ri to'rtburchak diagonali

## Topshiriq sharti:
To'g'ri to'rtburchak tomonlari a va b bo'lsa, uning diagonali d = sqrt(a^2 + b^2) ni hisoblang.

## Yechim (Python kodi):
```python
import math
a = float(input("a tomon: "))
b = float(input("b tomon: "))
d = math.sqrt(a**2 + b**2)
print(f"Diagonal uzunligi: {d:.2f}")
```

## Tushuntirish va Mantiq:
Pifagor teoremasi to'g'ri to'rtburchak diagonali uchun qo'llaniladi.

## Ishlash natijasi:
```text
Kiritish: a = 6, b = 8 -> Chiqish: 10.00
```


# 19-Topshiriq: Arifmetik progressiyaning n-hadi

## Topshiriq sharti:
Birinchi hadi a1, ayirmasi d va had raqami n berilgan. a_n = a1 + (n-1)*d ni hisoblang.

## Yechim (Python kodi):
```python
a1 = float(input("Birinchi had (a1): "))
d = float(input("Ayirma (d): "))
n = int(input("Had raqami (n): "))
an = a1 + (n - 1) * d
print(f"{n}-had (a_{n}): {an}")
```

## Tushuntirish va Mantiq:
Arifmetik progressiyaning umumiy hadi formulasi.

## Ishlash natijasi:
```text
Kiritish: a1 = 3, d = 4, n = 5 -> Chiqish: 19.0
```


# 20-Topshiriq: Arifmetik progressiya yig'indisi

## Topshiriq sharti:
Dastlabki n ta had yig'indisi: S_n = ((a1 + an) * n) / 2 ni hisoblang.

## Yechim (Python kodi):
```python
a1 = float(input("Birinchi had (a1): "))
an = float(input("Oxirgi had (an): "))
n = int(input("Hadlar soni (n): "))
Sn = ((a1 + an) * n) / 2
print(f"Dastlabki {n} ta had yig'indisi: {Sn}")
```

## Tushuntirish va Mantiq:
Gaus formulasi arifmetik progressiya yig'indisi uchun.

## Ishlash natijasi:
```text
Kiritish: a1 = 1, an = 100, n = 100 -> Chiqish: 5050.0
```


# 21-Topshiriq: Geometrik progressiyaning n-hadi

## Topshiriq sharti:
Birinchi hadi b1, maxraji q va had raqami n berilgan. b_n = b1 * q^(n-1) ni hisoblang.

## Yechim (Python kodi):
```python
b1 = float(input("Birinchi had (b1): "))
q = float(input("Maxraj (q): "))
n = int(input("Had raqami (n): "))
bn = b1 * (q ** (n - 1))
print(f"{n}-had: {bn}")
```

## Tushuntirish va Mantiq:
Geometrik progressiya hadining eksponentsial o'sishi.

## Ishlash natijasi:
```text
Kiritish: b1 = 2, q = 3, n = 4 -> Chiqish: 54.0
```


# 22-Topshiriq: Ikki nuqta orasidagi masofa

## Topshiriq sharti:
Tekislikdagi (x1, y1) va (x2, y2) nuqtalar orasidagi masofani hisoblang: d = sqrt((x2-x1)^2 + (y2-y1)^2).

## Yechim (Python kodi):
```python
import math
x1, y1 = float(input("x1: ")), float(input("y1: "))
x2, y2 = float(input("x2: ")), float(input("y2: "))
masofa = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
print(f"Orasidagi masofa: {masofa:.2f}")
```

## Tushuntirish va Mantiq:
Evklid masofasi formulasi koordinatalar uchun.

## Ishlash natijasi:
```text
Kiritish: (0,0) va (3,4) -> Chiqish: 5.00
```


# 23-Topshiriq: Valyuta konvertori

## Topshiriq sharti:
So'mdagi mablag'ni Markaziy bank kursi bo'yicha AQSH dollariga va aksincha konvertatsiya qiling.

## Yechim (Python kodi):
```python
som = float(input("So'm miqdori: "))
kurs = float(input("1 AQSH dollari kursi (so'mda): "))
dollar = som / kurs
print(f"{som:,.2f} so'm = {dollar:,.2f} USD")
```

## Tushuntirish va Mantiq:
Moliya dasturlaridagi asosiy valyuta konvertatsiyasi.

## Ishlash natijasi:
```text
Kiritish: 1280000 so'm, kurs 12800 -> Chiqish: 100.00 USD
```


# 24-Topshiriq: Kvadrat tenglama diskriminanti

## Topshiriq sharti:
ax^2 + bx + c = 0 tenglamaning diskriminantini hisoblang: D = b^2 - 4ac.

## Yechim (Python kodi):
```python
a = float(input("a koeffitsient: "))
b = float(input("b koeffitsient: "))
c = float(input("c koeffitsient: "))
D = b**2 - 4*a*c
print(f"Diskriminant D = {D}")
```

## Tushuntirish va Mantiq:
Diskriminant ildizlar soni va mavjudligini aniqlash uchun kalit hisoblanadi.

## Ishlash natijasi:
```text
Kiritish: a = 1, b = -5, c = 6 -> Chiqish: 1.0
```


# 25-Topshiriq: Masshtab bo'yicha masofa

## Topshiriq sharti:
Xaritadagi masofa (sm) va masshtab (1:M) berilgan. Haqiqiy masofani kilometrda toping.

## Yechim (Python kodi):
```python
xarita_sm = float(input("Xaritadagi masofa (sm): "))
masshtab = float(input("Masshtab (1:X dagi X): "))
haqiqiy_sm = xarita_sm * masshtab
haqiqiy_km = haqiqiy_sm / 100000
print(f"Haqiqiy masofa: {haqiqiy_km:.2f} km")
```

## Tushuntirish va Mantiq:
1 metr = 100 sm, 1 km = 1000 m = 100,000 sm.

## Ishlash natijasi:
```text
Kiritish: 5 sm, masshtab 1:1,000,000 -> Chiqish: 50.00 km
```


# 26-Topshiriq: Avtomobilning o'rtacha tezligi

## Topshiriq sharti:
Bosib o'tilgan yo'l s (km) va sarflangan vaqt t (soat) berilgan. O'rtacha tezlik v = s / t ni hisoblang.

## Yechim (Python kodi):
```python
s = float(input("Yo'l (km): "))
t = float(input("Vaqt (soat): "))
v = s / t
print(f"O'rtacha tezlik: {v:.1f} km/soat")
```

## Tushuntirish va Mantiq:
Klassik mexanikadagi o'rtacha tezlik hisobi.

## Ishlash natijasi:
```text
Kiritish: s = 300 km, t = 4 soat -> Chiqish: 75.0 km/soat
```


# 27-Topshiriq: Uch xonali sonni teskari o'girish

## Topshiriq sharti:
Uch xonali son berilgan (masalan, 123). Uni arifmetik amallar bilan 321 ga aylantiring.

## Yechim (Python kodi):
```python
n = int(input("3 xonali son: "))
yuz = n // 100
on = (n // 10) % 10
bir = n % 10
teskari = bir * 100 + on * 10 + yuz
print(f"{n} ning teskarisi: {teskari}")
```

## Tushuntirish va Mantiq:
Matematik usulda xonalar ko'paytirilib teskari son yig'iladi.

## Ishlash natijasi:
```text
Kiritish: 582 -> Chiqish: 285
```


# 28-Topshiriq: Baytlarni KB, MB va GB ga o'girish

## Topshiriq sharti:
Fayl hajmi baytlarda berilgan. Uni Kilobayt, Megabayt va Gigabaytda ifodalang.

## Yechim (Python kodi):
```python
bayt = int(input("Baytlar soni: "))
kb = bayt / 1024
mb = kb / 1024
gb = mb / 1024
print(f"{kb:.2f} KB | {mb:.2f} MB | {gb:.4f} GB")
```

## Tushuntirish va Mantiq:
Informatikada 1 KB = 1024 Bayt, 1 MB = 1024 KB, 1 GB = 1024 MB.

## Ishlash natijasi:
```text
Kiritish: 10485760 bayt -> Chiqish: 10240.00 KB | 10.00 MB | 0.0098 GB
```


# 29-Topshiriq: O'rtacha arifmetik va geometrik qiymat

## Topshiriq sharti:
Ikkita musbat sonning o'rtacha arifmetik ((a+b)/2) va o'rtacha geometrik (sqrt(a*b)) qiymatlarini toping.

## Yechim (Python kodi):
```python
import math
a = float(input("a: "))
b = float(input("b: "))
or_arif = (a + b) / 2
or_geom = math.sqrt(a * b)
print(f"O'rtacha arifmetik: {or_arif}, O'rtacha geometrik: {or_geom:.2f}")
```

## Tushuntirish va Mantiq:
Matematik tengsizlik bo'yicha har doim o'rtacha arifmetik >= o'rtacha geometrik bo'ladi.

## Ishlash natijasi:
```text
Kiritish: a = 4, b = 9 -> Chiqish: O'rtacha arifmetik: 6.5, O'rtacha geometrik: 6.00
```


# 30-Topshiriq: Geron formulasi bilan uchburchak yuzi

## Topshiriq sharti:
Uchburchakning uchta tomoni a, b, c berilgan. Geron formulasi bilan yuzini hisoblang: p = (a+b+c)/2, S = sqrt(p(p-a)(p-b)(p-c)).

## Yechim (Python kodi):
```python
import math
a = float(input("a: "))
b = float(input("b: "))
c = float(input("c: "))
p = (a + b + c) / 2
S = math.sqrt(p * (p - a) * (p - b) * (p - c))
print(f"Uchburchak yuzi S = {S:.2f}")
```

## Tushuntirish va Mantiq:
Ixtiyoriy uchburchakning faqat tomonlari ma'lum bo'lganda yuzini topish formulasi.

## Ishlash natijasi:
```text
Kiritish: a = 3, b = 4, c = 5 -> Chiqish: 6.00
```


# 31-Topshiriq: Tug'ilgan yil bo'yicha yoshni hisoblash

## Topshiriq sharti:
Foydalanuvchining tug'ilgan yili kiritilganda joriy yildagi yoshini hisoblang.

## Yechim (Python kodi):
```python
from datetime import datetime
tugilgan_yil = int(input("Tug'ilgan yilingiz: "))
joriy_yil = datetime.now().year
yosh = joriy_yil - tugilgan_yil
print(f"Sizning yoshingiz: {yosh} da")
```

## Tushuntirish va Mantiq:
`datetime.now().year` joriy yilni avtomatik aniqlaydi.

## Ishlash natijasi:
```text
Kiritish: 2008 -> Chiqish: Sizning yoshingiz: 18 da
```


# 32-Topshiriq: BMI (Tana vazni indeksi)

## Topshiriq sharti:
Vazn (kg) va bo'y (metrda) berilgan. Tana vazni indeksini hisoblang: BMI = vazn / (boy^2).

## Yechim (Python kodi):
```python
vazn = float(input("Vazningiz (kg): "))
boy = float(input("Bo'yingiz (metrda, masalan 1.75): "))
bmi = vazn / (boy ** 2)
print(f"Sizning BMI ko'rsatkichingiz: {bmi:.1f}")
```

## Tushuntirish va Mantiq:
Tibbiyotda inson tana vaznining me'yorga mosligini baholash formulasi.

## Ishlash natijasi:
```text
Kiritish: vazn = 70, boy = 1.75 -> Chiqish: 22.9
```


# 33-Topshiriq: Tovar narxiga QQS (12%) hisoblash

## Topshiriq sharti:
Tovarning sof narxi kiritilganda 12% lik QQS (Qo'shilgan qiymat solig'i) va yakuniy narxni hisoblang.

## Yechim (Python kodi):
```python
narx = float(input("Tovar narxi: "))
qqs = narx * 0.12
yakuniy = narx + qqs
print(f"QQS (12%): {qqs:,.2f} so'm | Jami to'lov: {yakuniy:,.2f} so'm")
```

## Tushuntirish va Mantiq:
Buxgalteriya va savdo dasturlaridagi soliq hisoblash.

## Ishlash natijasi:
```text
Kiritish: 100,000 -> Chiqish: QQS: 12,000.00 so'm, Jami: 112,000.00 so'm
```


# 34-Topshiriq: Chegirma miqdori va tejalgan summa

## Topshiriq sharti:
Mahsulot narxi va chegirma foizi kiritilganda tejalgan summa va to'lanadigan narxni toping.

## Yechim (Python kodi):
```python
narx = float(input("Mahsulot narxi: "))
foiz = float(input("Chegirma foizi (%): "))
tejash = narx * (foiz / 100)
yangi_narx = narx - tejash
print(f"Tejaldi: {tejash:,.2f} | Yangi narx: {yangi_narx:,.2f}")
```

## Tushuntirish va Mantiq:
Savdo va do'kon tizimlaridagi chegirma hisoblash.

## Ishlash natijasi:
```text
Kiritish: 500,000 so'm, 20% -> Chiqish: Tejaldi: 100,000.00, Yangi: 400,000.00
```


# 35-Topshiriq: Kun boshidan o'tgan minutlar

## Topshiriq sharti:
Soat va minut kiritilganda kun boshidan beri jami necha minut o'tganini hisoblang.

## Yechim (Python kodi):
```python
soat = int(input("Soat (0-23): "))
minut = int(input("Minut (0-59): "))
jami_minut = soat * 60 + minut
print(f"Kun boshidan beri o'tgan vaqt: {jami_minut} minut")
```

## Tushuntirish va Mantiq:
Vaqt hisob-kitoblarida birliklarni daqiqaga keltirish.

## Ishlash natijasi:
```text
Kiritish: 14:30 -> Chiqish: 870 minut
```


# 36-Topshiriq: Tezlanuvchan harakatda bosib o'tilgan yo'l

## Topshiriq sharti:
Boshlang'ich tezlik v0, tezlanish a va vaqt t berilgan. Yo'lni hisoblang: s = v0*t + (a*t^2)/2.

## Yechim (Python kodi):
```python
v0 = float(input("Boshlang'ich tezlik (m/s): "))
a = float(input("Tezlanish (m/s^2): "))
t = float(input("Vaqt (s): "))
s = v0 * t + (a * (t ** 2)) / 2
print(f"Bosib o'tilgan masofa: {s:.2f} metr")
```

## Tushuntirish va Mantiq:
Kinematikaning asosiy harakat tenglamasi.

## Ishlash natijasi:
```text
Kiritish: v0 = 5, a = 2, t = 3 -> Chiqish: 24.00 metr
```


# 37-Topshiriq: Trapetsiya yuzini hisoblash

## Topshiriq sharti:
Trapetsiyaning asoslari a, b va balandligi h berilgan. Yuzi S = ((a + b) / 2) * h ni hisoblang.

## Yechim (Python kodi):
```python
a = float(input("Kichik asos (a): "))
b = float(input("Katta asos (b): "))
h = float(input("Balandlik (h): "))
S = ((a + b) / 2) * h
print(f"Trapetsiya yuzi S = {S:.2f}")
```

## Tushuntirish va Mantiq:
Geometriyada trapetsiya yuzi o'rta chiziq va balandlik ko'paytmasiga teng.

## Ishlash natijasi:
```text
Kiritish: a = 4, b = 6, h = 5 -> Chiqish: 25.00
```


# 38-Topshiriq: Konus hajmini hisoblash

## Topshiriq sharti:
Asosining radiusi r va balandligi h bo'lgan konusning hajmini toping: V = (1/3) * pi * r^2 * h.

## Yechim (Python kodi):
```python
import math
r = float(input("Asos radiusi: "))
h = float(input("Balandlik: "))
V = (1/3) * math.pi * (r ** 2) * h
print(f"Konus hajmi: {V:.2f}")
```

## Tushuntirish va Mantiq:
Stereometriyada konus hajmi aylanma jism formulasi bo'yicha topiladi.

## Ishlash natijasi:
```text
Kiritish: r = 3, h = 4 -> Chiqish: 37.70
```


# 39-Topshiriq: Sharning hajmi va sirtining yuzi

## Topshiriq sharti:
Radiusi R bo'lgan sharning hajmi V = (4/3)*pi*R^3 va sirti yuzi S = 4*pi*R^2 ni toping.

## Yechim (Python kodi):
```python
import math
R = float(input("Shar radiusi: "))
V = (4/3) * math.pi * (R ** 3)
S = 4 * math.pi * (R ** 2)
print(f"Hajmi V = {V:.2f} | Sirt yuzi S = {S:.2f}")
```

## Tushuntirish va Mantiq:
Fazoviy figuralar: sharning hajm va sirt xususiyatlari.

## Ishlash natijasi:
```text
Kiritish: R = 3 -> Chiqish: V = 113.10, S = 113.10
```


# 40-Topshiriq: Ikki xonali sonning raqamlari o'rnini almashtirish

## Topshiriq sharti:
Ikki xonali son kiritilganda uning o'nlik va birliklarini almashtiruvchi dastur tuzing.

## Yechim (Python kodi):
```python
n = int(input("Ikki xonali son: "))
onlik = n // 10
birlik = n % 10
yangi_son = birlik * 10 + onlik
print(f"{n} ning almashtirilgani: {yangi_son}")
```

## Tushuntirish va Mantiq:
Raqamlar pozitsion sistemada og'irlik koeffitsienti bilan hisoblanadi.

## Ishlash natijasi:
```text
Kiritish: 73 -> Chiqish: 37
```


# 41-Topshiriq: Sonning juft yoki toqligini aniqlash

## Topshiriq sharti:
Kiritilgan butun sonning 2 ga bo'linish qoldig'i orqali juft yoki toq ekanligini ifodalang.

## Yechim (Python kodi):
```python
n = int(input("Butun son: "))
qoldiq = n % 2
status = "Juft son" if qoldiq == 0 else "Toq son"
print(f"{n} — {status}")
```

## Tushuntirish va Mantiq:
Matematikada 2 ga qoldiqsiz bo'linadigan har qanday son juft son hisoblanadi.

## Ishlash natijasi:
```text
Kiritish: 42 -> Chiqish: 42 — Juft son
```


# 42-Topshiriq: 5 ta sonning o'rtacha qiymati

## Topshiriq sharti:
Foydalanuvchi kiritgan 5 ta sonning o'rtacha arifmetik qiymatini hisoblang.

## Yechim (Python kodi):
```python
sonlar = [float(input(f"{i+1}-son: ")) for i in range(5)]
ortacha = sum(sonlar) / len(sonlar)
print(f"5 ta sonning o'rtacha qiymati: {ortacha:.2f}")
```

## Tushuntirish va Mantiq:
`sum()` ro'yxat elementlari yig'indisini, `len()` esa sonini qaytaradi.

## Ishlash natijasi:
```text
Kiritish: 10, 20, 30, 40, 50 -> Chiqish: 30.00
```


# 43-Topshiriq: Oylik maoshdan sof daromadni hisoblash

## Topshiriq sharti:
Oylik hisoblangan maoshdan 12% jismoniy shaxslar daromad solig'i ushlab qolingach qo'lga tegadigan summani hisoblang.

## Yechim (Python kodi):
```python
maosh = float(input("Hisoblangan oylik maosh (so'm): "))
soliq = maosh * 0.12
sof_maosh = maosh - soliq
print(f"Ushlab qolingan soliq (12%): {soliq:,.2f} so'm")
print(f"Qo'lga tegadigan sof maosh: {sof_maosh:,.2f} so'm")
```

## Tushuntirish va Mantiq:
O'zbekiston soliq qonunchiligiga muvofiq daromad solig'i hisobi.

## Ishlash natijasi:
```text
Kiritish: 5,000,000 -> Chiqish: Soliq: 600,000.00, Sof: 4,400,000.00
```


# 44-Topshiriq: Doiraviy sektor yuzini hisoblash

## Topshiriq sharti:
Radiusi r va markaziy burchagi alfa (gradusda) bo'lgan doiraviy sektor yuzini hisoblang: S = (pi * r^2 * alfa) / 360.

## Yechim (Python kodi):
```python
import math
r = float(input("Radius: "))
alfa = float(input("Markaziy burchak (gradus): "))
S = (math.pi * (r ** 2) * alfa) / 360
print(f"Sektor yuzi: {S:.2f}")
```

## Tushuntirish va Mantiq:
To'liq doira 360 gradusdan iborat bo'lgani uchun sektor uning ulushi bo'ladi.

## Ishlash natijasi:
```text
Kiritish: r = 6, alfa = 60 -> Chiqish: 18.85
```


# 45-Topshiriq: Gradusdan radianga va radiandan gradusga

## Topshiriq sharti:
Burchakni gradusdan radianga va radianga o'tkazish formulalari bilan ishlang.

## Yechim (Python kodi):
```python
import math
gradus = float(input("Burchak (gradusda): "))
radian = math.radians(gradus)
print(f"{gradus}° = {radian:.4f} rad")

rad_input = float(input("Burchak (radianda): "))
grad_res = math.degrees(rad_input)
print(f"{rad_input} rad = {grad_res:.2f}°")
```

## Tushuntirish va Mantiq:
`math.radians()` va `math.degrees()` aniq matematik konvertatsiyani amalga oshiradi.

## Ishlash natijasi:
```text
Kiritish: 180° -> Chiqish: 3.1416 rad
```


# 46-Topshiriq: Silindrning hajmi va to'la sirti

## Topshiriq sharti:
Asos radiusi r va balandligi h bo'lgan silindrning hajmi (V = pi*r^2*h) va to'la sirti (S = 2*pi*r*(r + h)) ni hisoblang.

## Yechim (Python kodi):
```python
import math
r = float(input("Radius (r): "))
h = float(input("Balandlik (h): "))
V = math.pi * (r ** 2) * h
S = 2 * math.pi * r * (r + h)
print(f"Silindr hajmi: {V:.2f} | To'la sirti: {S:.2f}")
```

## Tushuntirish va Mantiq:
Silindr geometriyasining asosiy hajmiy formulasi.

## Ishlash natijasi:
```text
Kiritish: r = 3, h = 5 -> Chiqish: Hajm: 141.37, Sirt: 150.80
```


# 47-Topshiriq: Gravitatsion tortishish kuchi

## Topshiriq sharti:
Nyutonning butunjahon tortishish qonuni bo'yicha ikki jism orasidagi kuchni hisoblang: F = G * (m1*m2)/r^2 (G = 6.67430e-11).

## Yechim (Python kodi):
```python
G = 6.67430e-11
m1 = float(input("1-jism massasi (kg): "))
m2 = float(input("2-jism massasi (kg): "))
r = float(input("Orasidagi masofa (m): "))
F = G * (m1 * m2) / (r ** 2)
print(f"Tortishish kuchi: {F:.6e} Nyuton")
```

## Tushuntirish va Mantiq:
Astrofizika va klassik mexanikaning asosiy fundamental qonunlaridan biri.

## Ishlash natijasi:
```text
Kiritish: m1 = 5.97e24 (Yer), m2 = 70 (odam), r = 6.37e6 (Yer radiusi) -> Chiqish: 686.08 Nyuton
```


# 48-Topshiriq: Kubning qirrasi bo'yicha to'la sirti va hajmi

## Topshiriq sharti:
Qirrasi a bo'lgan kubning hajmi V = a^3 va to'la sirti S = 6*a^2 ni toping.

## Yechim (Python kodi):
```python
a = float(input("Kub qirrasi (a): "))
V = a ** 3
S = 6 * (a ** 2)
print(f"Kub hajmi: {V:.2f} | To'la sirti: {S:.2f}")
```

## Tushuntirish va Mantiq:
Muntazam olti yoqli figura (kub) xususiyatlari.

## Ishlash natijasi:
```text
Kiritish: a = 4 -> Chiqish: Hajm: 64.00, Sirt: 96.00
```


# 49-Topshiriq: Erkin tushish vaqtini hisoblash

## Topshiriq sharti:
Jism h balandlikdan boshlang'ich tezliksiz tushganda yerga yetib borish vaqtini toping: t = sqrt(2h / g) (g = 9.8).

## Yechim (Python kodi):
```python
import math
h = float(input("Balandlik (m): "))
g = 9.8
t = math.sqrt((2 * h) / g)
print(f"Yerga tushish vaqti: {t:.2f} sekund")
```

## Tushuntirish va Mantiq:
Erkin tushish tezlanishi vaqtining balandlikka bog'liqligi.

## Ishlash natijasi:
```text
Kiritish: h = 45 -> Chiqish: 3.03 sekund
```


# 50-Topshiriq: Sonning butun va kasr qismini ajratish

## Topshiriq sharti:
Kiritilgan haqiqiy (kasr) sonning butun qismi va kasr qismini alohida ajratib oling.

## Yechim (Python kodi):
```python
son = float(input("Haqiqiy son kiriting (masalan, 15.75): "))
butun_qism = int(son)
kasr_qism = son - butun_qism
print(f"Butun qismi: {butun_qism}")
print(f"Kasr qismi: {kasr_qism:.4f}")
```

## Tushuntirish va Mantiq:
`int()` funksiyasi sonning butun qismini oladi, asl sondan butun qism ayirilsa kasr qism qoladi.

## Ishlash natijasi:
```text
Kiritish: 12.345 -> Chiqish: Butun: 12, Kasr: 0.3450
```
