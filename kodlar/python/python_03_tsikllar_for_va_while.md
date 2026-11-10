# Python Dasturlash Tili — 3-Qism: Tsikllar (For va While), Ichma-ich Tsikllar va Boshqaruv Operatorlari
## (101-150 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam tsikllar (takrorlanish jarayonlari) bo'yicha eng muhim amaliy bilimlarni qamrab oladi:
* `for` va `while` tsikllari, ularning farqlari va qo'llanish o'rinlari;
* `range()`, `enumerate()`, `zip()`, `reversed()` yordamchi funksiyalari;
* `break`, `continue`, `pass` boshqaruv operatorlari;
* Ichma-ich (nested) tsikllar: matritsalar, karra jadvali va geometrik naqshlar;
* Matematik algoritmlar: tub sonlar, Fibonachchi, Evklid EKUB/EKUK, Collatz, faktorial;

---

# 101-Topshiriq: 1 dan N gacha bo'lgan natural sonlar yig'indisi

## Topshiriq sharti:
Foydalanuvchi kiritgan musbat N sonigacha bo'lgan barcha natural sonlar yig'indisini for tsikli orqali hisoblang.

## Yechim (Python kodi):
```python
# Foydalanuvchidan N sonini olamiz
n = int(input("N natural sonini kiriting: "))

yigindi = 0
for i in range(1, n + 1):
    yigindi += i

print(f"1 dan {n} gacha sonlar yig'indisi: {yigindi}")
```

## Tushuntirish va Mantiq:
1. `range(1, n + 1)` 1 dan boshlab `n` gacha (n o'zi ham kiradi) bo'lgan sonlar ketma-ketligini beradi.
2. `yigindi += i` har bir iteratsiyada joriy sonni jamlovchi o'zgaruvchiga qo'shib boradi.
3. Dastur natijasi arifmetik progressiya formulasiga (`n*(n+1)//2`) teng bo'ladi.

## Ishlash natijasi:
```text
Kiritish: 10
Chiqish: 1 dan 10 gacha sonlar yig'indisi: 55
```


# 102-Topshiriq: N gacha bo'lgan barcha juft sonlarni chiqarish

## Topshiriq sharti:
1 dan N gacha bo'lgan oraliqdagi faqat juft sonlarni qadam parametri (step=2) yordamida ekranga chiqaring.

## Yechim (Python kodi):
```python
n = int(input("N sonini kiriting: "))

print(f"{n} gacha bo'lgan juft sonlar:")
for i in range(2, n + 1, 2):
    print(i, end=" ")
print()  # Yangi qatorga o'tish
```

## Tushuntirish va Mantiq:
1. `range(start, stop, step)` funksiyasida `step=2` qilib belgilanganda, qadam 2 tadan o'sib boradi.
2. Boshlang'ich qiymat 2 bo'lgani sababli faqat juft sonlar (2, 4, 6, ...) hosil bo'ladi.
3. `end=" "` parametri har bir son orasiga bo'sh joy tashlab, bir qatorda chiqarishni ta'minlaydi.

## Ishlash natijasi:
```text
Kiritish: 12
Chiqish: 2 4 6 8 10 12
```


# 103-Topshiriq: Sonning faktorialini hisoblash

## Topshiriq sharti:
Kiritilgan nomanfiy n sonining faktorialini (n!) for tsikli yordamida toping.

## Yechim (Python kodi):
```python
n = int(input("Faktoriali hisoblanadigan sonni kiriting: "))

if n < 0:
    print("Manfiy sonlarning faktoriali mavjud emas!")
else:
    faktorial = 1
    for i in range(1, n + 1):
        faktorial *= i
    print(f"{n}! = {faktorial}")
```

## Tushuntirish va Mantiq:
1. Matematikada 0! = 1 va n! = 1 * 2 * 3 * ... * n bo'ladi.
2. `faktorial = 1` qilib boshlanadi, chunki ko'paytirish uchun 1 neytral element hisoblanadi.
3. Tsikl har bir qadamda qiymatni `i` ga ko'paytirib boradi.

## Ishlash natijasi:
```text
Kiritish: 5
Chiqish: 5! = 120
```


# 104-Topshiriq: Manfiy son kiritilguncha kiritilgan sonlarni yig'ish

## Topshiriq sharti:
Foydalanuvchi klaviaturadan sonlar kiritadi. Manfiy son kiritilganda dastur to'xtab, ungacha bo'lgan musbat sonlar yig'indisini chiqarishi kerak.

## Yechim (Python kodi):
```python
jami = 0

print("Sonlarni kiriting (to'xtatish uchun manfiy son kiriting):")
while True:
    son = float(input("Son: "))
    if son < 0:
        break
    jami += son

print(f"Kiritilgan musbat sonlar yig'indisi: {jami}")
```

## Tushuntirish va Mantiq:
1. `while True` cheksiz tsikl bo'lib, to'xtash sharti uning ichida beriladi.
2. `if son < 0:` sharti bajarilganda `break` operatori tsiklni darhol yakunlaydi.
3. `jami += son` faqat manfiy bo'lmagan sonlar uchun ishlaydi.

## Ishlash natijasi:
```text
Kiritish: 10, 25, 5, -1
Chiqish: Kiritilgan musbat sonlar yig'indisi: 40.0
```


# 105-Topshiriq: Natural sonning barcha bo'luvchilarini topish

## Topshiriq sharti:
Kiritilgan natural sonning barcha butun bo'luvchilarini va ularning umumiy sonini aniqlang.

## Yechim (Python kodi):
```python
son = int(input("Natural son kiriting: "))

boluvchilar = []
for i in range(1, son + 1):
    if son % i == 0:
        boluvchilar.append(i)

print(f"{son} sonining bo'luvchilari: {boluvchilar}")
print(f"Bo'luvchilar soni: {len(boluvchilar)} ta")
```

## Tushuntirish va Mantiq:
1. `son % i == 0` ifodasi son `i` ga qoldiqsiz bo'linishini tekshiradi.
2. Bo'luvchilar ro'yxatga yig'iladi va `len()` orqali ularning soni topiladi.

## Ishlash natijasi:
```text
Kiritish: 24
Chiqish: [1, 2, 3, 4, 6, 8, 12, 24], Bo'luvchilar soni: 8 ta
```


# 106-Topshiriq: Tub sonni aniqlash (Prime Check)

## Topshiriq sharti:
Berilgan sonning tub (faqat 1 ga va o'ziga bo'linadigan) yoki murakkab ekanligini aniqlang.

## Yechim (Python kodi):
```python
import math

son = int(input("Musbat butun son kiriting: "))

if son <= 1:
    tubmi = False
elif son == 2:
    tubmi = True
elif son % 2 == 0:
    tubmi = False
else:
    tubmi = True
    # Ildizigacha bo'lgan toq sonlarni tekshirish kifoya (O(sqrt(n)))
    chegara = int(math.isqrt(son))
    for i in range(3, chegara + 1, 2):
        if son % i == 0:
            tubmi = False
            break

if tubmi:
    print(f"{son} — TUB son.")
else:
    print(f"{son} — MURAKKAB son (yoki tub emas).")
```

## Tushuntirish va Mantiq:
1. 1 dan kichik yoki teng sonlar tub emas, 2 yagona juft tub son.
2. Samaradorlik uchun bo'luvchilarni `sqrt(son)` gacha tekshirish yetarli, bu katta sonlarni juda tez tekshirishga imkon beradi.

## Ishlash natijasi:
```text
Kiritish: 29 -> Chiqish: 29 — TUB son.
Kiritish: 35 -> Chiqish: 35 — MURAKKAB son.
```


# 107-Topshiriq: Oraliqdagi barcha tub sonlarni topish

## Topshiriq sharti:
1 dan N gacha bo'lgan barcha tub sonlar ro'yxatini chiqaring.

## Yechim (Python kodi):
```python
n = int(input("Yuqori chegarani kiriting (N): "))

tublar = []
for son in range(2, n + 1):
    tub = True
    for b in range(2, int(son**0.5) + 1):
        if son % b == 0:
            tub = False
            break
    if tub:
        tublar.append(son)

print(f"1 dan {n} gacha tub sonlar ({len(tublar)} ta):")
print(tublar)
```

## Tushuntirish va Mantiq:
1. Ichma-ich tsikl har bir sonni 2 dan boshlab uning ildizigacha bo'lgan bo'luvchilarga tekshiradi.
2. Agar bitta ham bo'luvchi topilmasa, son tub deb hisoblanadi va ro'yxatga kiritiladi.

## Ishlash natijasi:
```text
Kiritish: 30
Chiqish: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] (10 ta)
```


# 108-Topshiriq: Fibonachchi ketma-ketligining N ta hadini hisoblash

## Topshiriq sharti:
Dastlabki N ta Fibonachchi sonini (0, 1, 1, 2, 3, 5, 8, 13, ...) ekranga chiqaring.

## Yechim (Python kodi):
```python
n = int(input("Nechta Fibonachchi soni kerak? "))

if n <= 0:
    print("Musbat butun son kiriting!")
elif n == 1:
    print([0])
else:
    fibo = [0, 1]
    for _ in range(2, n):
        yangi_had = fibo[-1] + fibo[-2]
        fibo.append(yangi_had)
    print(f"Dastlabki {n} ta Fibonachchi soni: {fibo}")
```

## Tushuntirish va Mantiq:
1. Fibonachchi ketma-ketligida har bir yangi had oldingi ikki hadning yig'indisiga teng: F(n) = F(n-1) + F(n-2).
2. Python'da `fibo[-1]` oxirgi elementni, `fibo[-2]` esa undan oldingi elementni ifodalaydi.

## Ishlash natijasi:
```text
Kiritish: 8
Chiqish: [0, 1, 1, 2, 3, 5, 8, 13]
```


# 109-Topshiriq: Sonning raqamlari yig'indisini topish (while)

## Topshiriq sharti:
Kiritilgan butun sonning barcha raqamlari yig'indisini arifmetik amallar (% va //) bilan while tsikli orqali toping.

## Yechim (Python kodi):
```python
son = abs(int(input("Butun son kiriting: ")))

yigindi = 0
vaqtinchalik = son

while vaqtinchalik > 0:
    raqam = vaqtinchalik % 10   # Oxirgi raqamni ajratib olamiz
    yigindi += raqam
    vaqtinchalik //= 10         # Oxirgi raqamni o'chirib tashlaymiz

print(f"{son} sonining raqamlari yig'indisi: {yigindi}")
```

## Tushuntirish va Mantiq:
1. `% 10` amali sonning oxirgi birlik raqamini ajratib beradi.
2. `//= 10` amali sonni 10 ga butunli bo'lib, oxirgi raqamni olib tashlaydi.
3. Tsikl son 0 bo'lgunga qadar davom etadi.

## Ishlash natijasi:
```text
Kiritish: 7543
Chiqish: 7543 sonining raqamlari yig'indisi: 19 (7+5+4+3)
```


# 110-Topshiriq: Sonni arifmetik usulda teskari qilish

## Topshiriq sharti:
Kiritilgan sonning raqamlarini arifmetik yo'l bilan (satrga o'girmasdan) teskari tartibda yozing.

## Yechim (Python kodi):
```python
son = int(input("Musbat butun son kiriting: "))

teskari = 0
n = son

while n > 0:
    raqam = n % 10
    teskari = teskari * 10 + raqam
    n //= 10

print(f"Asl son: {son}")
print(f"Teskari son: {teskari}")
```

## Tushuntirish va Mantiq:
1. `teskari * 10 + raqam` formulasi mavjud sonni bir xona chapga surib, yangi raqamni oxiriga qo'shadi.
2. Bu algoritmlashda klassik arifmetik ko'chirish usulidir.

## Ishlash natijasi:
```text
Kiritish: 12345
Chiqish: Asl: 12345, Teskari: 54321
```


# 111-Topshiriq: Sonning palindrom ekanligini matematik tekshirish

## Topshiriq sharti:
Kiritilgan natural son o'ngdan ham, chapdan ham bir xil o'qiladimi (palindrommi) yo'qligini aniqlang.

## Yechim (Python kodi):
```python
son = int(input("Sonni kiriting: "))

teskari = 0
n = son

while n > 0:
    teskari = teskari * 10 + (n % 10)
    n //= 10

if son == teskari:
    print(f"{son} — PALINDROM son.")
else:
    print(f"{son} — Palindrom emas (teskarisi: {teskari}).")
```

## Tushuntirish va Mantiq:
1. Son arifmetik teskarisiga teng bo'lsa, u palindrom hisoblanadi.
2. Masalan, 1221, 1331, 4554 kabi sonlar palindromdir.

## Ishlash natijasi:
```text
Kiritish: 12321 -> Chiqish: 12321 — PALINDROM son.
```


# 112-Topshiriq: To'liq karra jadvalini chiqarish

## Topshiriq sharti:
1 dan 9 gacha bo'lgan to'liq karra jadvalini ichma-ich (nested) for tsikllari yordamida chiroyli ustun shaklida chiqaring.

## Yechim (Python kodi):
```python
print("========== KARRA JADVALI ==========\n")

for i in range(1, 10):
    for j in range(1, 10):
        # 4 ta belgi kenglikda o'ngga tekislab chiqaramiz
        print(f"{i * j:4d}", end="")
    print()  # Har bir qator tugagach yangi qator
```

## Tushuntirish va Mantiq:
1. Tashqi tsikl qatorlarni (`i`), ichki tsikl ustunlarni (`j`) boshqaradi.
2. `{i * j:4d}` formati har bir son uchun 4 ta katak ajratadi, bu jadvalning tekis chiqishini ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: 1 dan 9 gacha bo'lgan karra matritsasi ekranda paydo bo'ladi.
```


# 113-Topshiriq: Yulduzchali to'g'ri burchakli uchburchak

## Topshiriq sharti:
Balandligi N bo'lgan to'g'ri burchakli uchburchak naqshini yulduzchalar (*) bilan chizing.

## Yechim (Python kodi):
```python
n = int(input("Balandlikni kiriting: "))

for i in range(1, n + 1):
    print("*" * i)
```

## Tushuntirish va Mantiq:
1. Python'da satrni songa ko'paytirish (`"*" * i`) uni takrorlash imkonini beradi.
2. 1-qatorda 1 ta, 2-qatorda 2 ta, i-qatorda i ta yulduzcha chiqadi.

## Ishlash natijasi:
```text
Kiritish: 4
Chiqish:
*
**
***
****
```


# 114-Topshiriq: Teskari burchakli uchburchak naqshi

## Topshiriq sharti:
Balandligi N bo'lgan kamayib boruvchi yulduzchali uchburchak chizing.

## Yechim (Python kodi):
```python
n = int(input("Balandlikni kiriting: "))

for i in range(n, 0, -1):
    print("*" * i)
```

## Tushuntirish va Mantiq:
1. `range(n, 0, -1)` kamayish tartibida ishlaydi: n dan boshlab 1 gacha har qadamda 1 ayirib boradi.

## Ishlash natijasi:
```text
Kiritish: 4
Chiqish:
****
***
**
*
```


# 115-Topshiriq: Teng yonli piramida naqshi

## Topshiriq sharti:
Balandligi N bo'lgan simmetrik piramida naqshini yulduzchalar va bo'shliqlar yordamida ekranga chiqaring.

## Yechim (Python kodi):
```python
n = int(input("Piramida balandligi: "))

for i in range(1, n + 1):
    boshliq = " " * (n - i)
    yulduz = "*" * (2 * i - 1)
    print(boshliq + yulduz)
```

## Tushuntirish va Mantiq:
1. Har bir qatorda chap tomonda `n - i` ta bo'shliq bo'ladi.
2. Yulduzchalar soni toq sonlar qoidasi bo'yicha `2 * i - 1` ta bo'ladi (1, 3, 5, 7, ...).

## Ishlash natijasi:
```text
Kiritish: 4
Chiqish:
   *
  ***
 *****
*******
```


# 116-Topshiriq: Romb shaklidagi yulduzcha naqshi

## Topshiriq sharti:
Yulduzchalardan iborat to'liq simmetrik romb (diamond) shaklini chizing.

## Yechim (Python kodi):
```python
n = int(input("Romb yarim balandligi: "))

# Yuqori piramida
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * (2 * i - 1))

# Pastki teskari piramida
for i in range(n - 1, 0, -1):
    print(" " * (n - i) + "*" * (2 * i - 1))
```

## Tushuntirish va Mantiq:
1. Romb yuqori va pastki ikkita simmetrik piramidaning birlashmasidan iborat.
2. Pastki tsikl `n-1` dan boshlanib 1 gacha kamayib boradi.

## Ishlash natijasi:
```text
Kiritish: 3
Chiqish:
  *
 ***
*****
 ***
  *
```


# 117-Topshiriq: Paskal uchburchagining N ta qatori

## Topshiriq sharti:
Paskal uchburchagining dastlabki N ta qatorini hisoblab chiqaring.

## Yechim (Python kodi):
```python
n = int(input("Paskal uchburchagi qatorlari soni: "))

uchburchak = []

for i in range(n):
    qator = [1] * (i + 1)
    for j in range(1, i):
        qator[j] = uchburchak[i - 1][j - 1] + uchburchak[i - 1][j]
    uchburchak.append(qator)

for q in uchburchak:
    print(" ".join(map(str, q)))
```

## Tushuntirish va Mantiq:
1. Paskal uchburchagida chetki elementlar har doim 1 ga teng.
2. O'rtadagi har bir element tepasidagi ikki qo'shni elementning yig'indisiga teng.

## Ishlash natijasi:
```text
Kiritish: 4
Chiqish:
1
1 1
1 2 1
1 3 3 1
```


# 118-Topshiriq: Collatz (3n + 1) gipotezasi

## Topshiriq sharti:
Har qanday musbat sondan boshlab: juft bo'lsa 2 ga bo'linadi, toq bo'lsa 3 ga ko'paytirilib 1 qo'shiladi. 1 ga yetguncha bo'lgan qadamlarni chiqaring.

## Yechim (Python kodi):
```python
n = int(input("Boshlang'ich sonni kiriting: "))

qadamlar = 0
ketma_ketlik = [n]

while n != 1:
    if n % 2 == 0:
        n //= 2
    else:
        n = 3 * n + 1
    ketma_ketlik.append(n)
    qadamlar += 1

print(f"Collatz yo'li: {ketma_ketlik}")
print(f"Jami qadamlar soni: {qadamlar}")
```

## Tushuntirish va Mantiq:
1. Collatz gipotezasiga ko'ra har qanday son oxir-oqibat 1 ga borib taqaladi.
2. While tsikli `n != 1` sharti bajarilgunicha navbatdagi qiymatlarni hisoblaydi.

## Ishlash natijasi:
```text
Kiritish: 6
Chiqish: [6, 3, 10, 5, 16, 8, 4, 2, 1], Qadamlar: 8
```


# 119-Topshiriq: Foydalanuvchi 'stop' deb yozguncha so'z yig'ish

## Topshiriq sharti:
Foydalanuvchi so'zlar kiritadi, 'stop' so'zi kiritilganda dastur to'xtaydi va kiritilgan barcha so'zlarni bitta matnga birlashtiradi.

## Yechim (Python kodi):
```python
sozlar = []

print("So'zlarni kiriting (yakunlash uchun 'stop' deb yozing):")
while True:
    s = input("So'z: ").strip()
    if s.lower() == "stop":
        break
    if s:
        sozlar.append(s)

natija = " ".join(sozlar)
print(f"Jami kiritilgan matn: {natija}")
print(f"So'zlar soni: {len(sozlar)} ta")
```

## Tushuntirish va Mantiq:
1. `.lower() == 'stop'` kiritilgan so'zning katta-kichik harflaridan qat'i nazar to'xtatish imkonini beradi.
2. `join()` ro'yxatdagi barcha so'zlarni bitta satrga bog'laydi.

## Ishlash natijasi:
```text
Kiritish: Python, juda, qiziqarli, stop
Chiqish: Python juda qiziqarli (3 ta)
```


# 120-Topshiriq: Continue operatori: 3 ga bo'linmaydigan sonlar

## Topshiriq sharti:
1 dan 30 gacha bo'lgan sonlar ichida 3 ga karrali bo'lganlarini continue bilan tashlab ketib, qolganlarini chiqaring.

## Yechim (Python kodi):
```python
print("1 dan 30 gacha bo'lgan 3 ga karrali bo'lmagan sonlar:")
for i in range(1, 31):
    if i % 3 == 0:
        continue  # 3 ga bo'linadiganlarini o'tkazib yuboramiz
    print(i, end=" ")
print()
```

## Tushuntirish va Mantiq:
1. `continue` operatori tsiklning joriy qadamini darhol yakunlab, keyingi qadamga o'tkazadi.
2. `i % 3 == 0` sharti to'g'ri bo'lgan har qanday qadamda `print` ishga tushmaydi.

## Ishlash natijasi:
```text
Chiqish: 1 2 4 5 7 8 10 11 13 14 16 17 19 20 22 23 25 26 28 29
```


# 121-Topshiriq: Sonning eng katta va eng kichik raqamini topish

## Topshiriq sharti:
Kiritilgan butun sonning raqamlari ichida eng kattasini va eng kichigini tsikl orqali aniqlang.

## Yechim (Python kodi):
```python
son = abs(int(input("Sonni kiriting: ")))

temp = son
eng_katta = -1
eng_kichik = 10

if temp == 0:
    eng_katta = eng_kichik = 0

while temp > 0:
    raqam = temp % 10
    if raqam > eng_katta:
        eng_katta = raqam
    if raqam < eng_kichik:
        eng_kichik = raqam
    temp //= 10

print(f"{son} sonining eng katta raqami: {eng_katta}")
print(f"{son} sonining eng kichik raqami: {eng_kichik}")
```

## Tushuntirish va Mantiq:
1. Boshlang'ich maksimum eng kichik (-1), minimum eng katta (10) deb olinadi.
2. Har bir raqam ajratib olinib, shart orqali taqqoslanadi.

## Ishlash natijasi:
```text
Kiritish: 8352 -> Chiqish: Eng katta: 8, Eng kichik: 2
```


# 122-Topshiriq: Arifmetik progressiyaning dastlabki N ta hadi

## Topshiriq sharti:
Birinchi hadi a1, ayirmasi d bo'lgan arifmetik progressiyaning dastlabki N ta hadini va ularning yig'indisini hisoblang.

## Yechim (Python kodi):
```python
a1 = float(input("1-had (a1): "))
d = float(input("Ayirma (d): "))
n = int(input("Hadlar soni (n): "))

hadlar = []
yigindi = 0

for i in range(n):
    an = a1 + i * d
    hadlar.append(an)
    yigindi += an

print(f"Progressiya hadlari: {hadlar}")
print(f"Jami yig'indi (S_{n}): {yigindi}")
```

## Tushuntirish va Mantiq:
1. Arifmetik progressiyaning i-hadi: an = a1 + (i-1)*d.
2. Tsikl orqali har bir had hisoblanadi va jamlanadi.

## Ishlash natijasi:
```text
Kiritish: a1=2, d=3, n=5 -> Chiqish: [2.0, 5.0, 8.0, 11.0, 14.0], Yig'indi: 40.0
```


# 123-Topshiriq: Geometrik progressiyaning dastlabki N ta hadi

## Topshiriq sharti:
Birinchi hadi b1, maxraji q bo'lgan geometrik progressiyaning dastlabki N ta hadini chiqaring.

## Yechim (Python kodi):
```python
b1 = float(input("1-had (b1): "))
q = float(input("Maxraj (q): "))
n = int(input("Hadlar soni (n): "))

hadlar = []
joriy = b1

for _ in range(n):
    hadlar.append(joriy)
    joriy *= q

print(f"Geometrik progressiya hadlari: {hadlar}")
```

## Tushuntirish va Mantiq:
1. Geometrik progressiyada keyingi had oldingi hadni `q` ga ko'paytirish orqali olinadi.
2. Har bir qadamda qiymat `*=` operatori bilan yangilanadi.

## Ishlash natijasi:
```text
Kiritish: b1=3, q=2, n=5 -> Chiqish: [3.0, 6.0, 12.0, 24.0, 48.0]
```


# 124-Topshiriq: Evklid algoritmi orqali EKUB (GCD) topish

## Topshiriq sharti:
Ikki butun sonning eng katta umumiy bo'luvchisini (EKUB) klassik Evklid algoritmi (while) bilan toping.

## Yechim (Python kodi):
```python
a = abs(int(input("1-sonni kiriting: ")))
b = abs(int(input("2-sonni kiriting: ")))

x, y = a, b
while y != 0:
    x, y = y, x % y

print(f"EKUB({a}, {b}) = {x}")
```

## Tushuntirish va Mantiq:
1. Evklid algoritmi: EKUB(a, b) = EKUB(b, a % b).
2. Qoldiq nol bo'lgunga qadar tsikl aylanadi va oxirgi noldan farqli qoldiq EKUB bo'ladi.

## Ishlash natijasi:
```text
Kiritish: 48, 18 -> Chiqish: EKUB(48, 18) = 6
```


# 125-Topshiriq: EKUK (LCM) ni topish

## Topshiriq sharti:
Ikki sonning eng kichik umumiy karralisini (EKUK) ularning ko'paytmasi va EKUBi orqali hisoblang.

## Yechim (Python kodi):
```python
a = int(input("1-son: "))
b = int(input("2-son: "))

def hisobla_ekub(x, y):
    while y != 0:
        x, y = y, x % y
    return x

ekub = hisobla_ekub(a, b)
# EKUK(a, b) = |a * b| // EKUB(a, b)
ekuk = abs(a * b) // ekub if ekub != 0 else 0

print(f"EKUB({a}, {b}) = {ekub}")
print(f"EKUK({a}, {b}) = {ekuk}")
```

## Tushuntirish va Mantiq:
1. Arifmetikaning asosiy teoremasiga ko'ra a * b = EKUB(a, b) * EKUK(a, b).
2. Shuning uchun EKUK = (a * b) // EKUB formulasi juda tez ishlaydi.

## Ishlash natijasi:
```text
Kiritish: 12, 15 -> Chiqish: EKUB: 3, EKUK: 60
```


# 126-Topshiriq: O'nlik sonni ikkilik (Binary) ga o'tkazish

## Topshiriq sharti:
Natural sonni 2 ga bo'lish algoritmi va while tsikli yordamida ikkilik sanoq sistemasiga o'tkazing.

## Yechim (Python kodi):
```python
son = int(input("Musbat o'nlik son kiriting: "))

if son == 0:
    ikkilik = "0"
else:
    qoldiqlar = []
    n = son
    while n > 0:
        qoldiqlar.append(str(n % 2))
        n //= 2
    # Qoldiqlarni teskari tartibda birlashtiramiz
    ikkilik = "".join(reversed(qoldiqlar))

print(f"{son} (o'nlik) = {ikkilik} (ikkilik)")
```

## Tushuntirish va Mantiq:
1. O'nlik sonni 2 ga bo'lib, qoldiqlarni yig'ib boramiz.
2. Yakunda qoldiqlar teskari tartibda o'qilsa, ikkilik ko'rinish hosil bo'ladi.

## Ishlash natijasi:
```text
Kiritish: 13 -> Chiqish: 13 (o'nlik) = 1101 (ikkilik)
```


# 127-Topshiriq: Ikkilik sonni o'nlikka o'tkazish (tsikl bilan)

## Topshiriq sharti:
Ikkilik satr (masalan '1101') berilganda, uni tsikl yordamida o'nlik songa aylantiring.

## Yechim (Python kodi):
```python
ikkilik = input("Ikkilik son kiriting (masalan 1011): ").strip()

onlik = 0
daraja = 0

for belgi in reversed(ikkilik):
    if belgi == '1':
        onlik += 2 ** daraja
    elif belgi != '0':
        print("Noto'g'ri ikkilik raqam!")
        break
    daraja += 1
else:
    print(f"{ikkilik} (ikkilik) = {onlik} (o'nlik)")
```

## Tushuntirish va Mantiq:
1. O'ngdan chapga qarab har bir raqam 2 ning tegishli darajasiga ko'paytiriladi.
2. `for...else` konstruktsiyasi tsikl `break`siz muvaffaqiyatli yakunlanganda ishlaydi.

## Ishlash natijasi:
```text
Kiritish: 1010 -> Chiqish: 1010 (ikkilik) = 10 (o'nlik)
```


# 128-Topshiriq: Mukammal sonni (Perfect Number) aniqlash

## Topshiriq sharti:
O'zidan boshqa barcha bo'luvchilari yig'indisi o'ziga teng bo'lgan son mukammal son deyiladi (masalan, 6 = 1 + 2 + 3). Sonning mukammalligini tekshiring.

## Yechim (Python kodi):
```python
son = int(input("Natural son kiriting: "))

if son <= 1:
    mukammalmi = False
else:
    boluvchilar_yigindisi = 0
    for i in range(1, son // 2 + 1):
        if son % i == 0:
            boluvchilar_yigindisi += i
    mukammalmi = (boluvchilar_yigindisi == son)

if mukammalmi:
    print(f"{son} — MUKAMMAL son!")
else:
    print(f"{son} — Mukammal son emas.")
```

## Tushuntirish va Mantiq:
1. Sonning o'zidan kichik eng katta bo'luvchisi `son // 2` dan oshmaydi.
2. Shuning uchun range chegarasini `son // 2 + 1` qilib olish hisoblash vaqtini 2 barobar qisqartiradi.

## Ishlash natijasi:
```text
Kiritish: 28 -> Chiqish: 28 — MUKAMMAL son! (1+2+4+7+14 = 28)
```


# 129-Topshiriq: Armstrong sonini aniqlash

## Topshiriq sharti:
Raqamlarining k-darajalari yig'indisi o'ziga teng bo'lgan son Armstrong soni deyiladi (k — raqamlar soni). Berilgan sonni tekshiring.

## Yechim (Python kodi):
```python
son = int(input("Musbat butun son kiriting: "))

satr = str(son)
k = len(satr)
yigindi = 0

for belgi in satr:
    yigindi += int(belgi) ** k

if yigindi == son:
    print(f"{son} — ARMSTRONG soni! ({' + '.join([f'{b}^{k}' for b in satr])} = {son})")
else:
    print(f"{son} — Armstrong soni emas (yig'indi: {yigindi}).")
```

## Tushuntirish va Mantiq:
1. Masalan: 153 soni 3 xonali: 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153.
2. Har bir raqam alohida ajratilib, `len` darajasiga ko'tariladi.

## Ishlash natijasi:
```text
Kiritish: 153 -> Chiqish: 153 — ARMSTRONG soni!
```


# 130-Topshiriq: Sonni tub ko'paytuvchilarga ajratish

## Topshiriq sharti:
Kiritilgan natural sonni tub ko'paytuvchilar (prime factors) ko'rinishida yozing.

## Yechim (Python kodi):
```python
son = int(input("Natural son kiriting: "))

n = son
kopaytuvchilar = []
boluvchi = 2

while boluvchi * boluvchi <= n:
    while n % boluvchi == 0:
        kopaytuvchilar.append(boluvchi)
        n //= boluvchi
    boluvchi += 1

if n > 1:
    kopaytuvchilar.append(n)

natija_matn = " * ".join(map(str, kopaytuvchilar))
print(f"{son} = {natija_matn}")
```

## Tushuntirish va Mantiq:
1. 2 dan boshlab bo'luvchini oshirib boramiz.
2. Har bir bo'luvchiga qoldiqsiz bo'linmay qolguncha ichki while orqali bo'lib boriladi.

## Ishlash natijasi:
```text
Kiritish: 360 -> Chiqish: 360 = 2 * 2 * 2 * 3 * 3 * 5
```


# 131-Topshiriq: Ro'yxatni enumerate() bilan tartiblash

## Topshiriq sharti:
Talabalar ro'yxatini tartib raqami (1-dan boshlab) bilan ekranga chiroyli jadval shaklida chiqaring.

## Yechim (Python kodi):
```python
talabalar = ["Anvar", "Dilnoza", "Jasur", "Malika", "Sardor"]

print("Talabalar ro'yxati:")
for tartib, ism in enumerate(talabalar, start=1):
    print(f"{tartib}. {ism}")
```

## Tushuntirish va Mantiq:
1. `enumerate(ketma_ketlik, start=1)` funksiyasi indeks va qiymatni bir vaqtda qaytaradi.
2. `start=1` hisobni 0 dan emas, odatiy 1 dan boshlashni ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish:
1. Anvar
2. Dilnoza
3. Jasur
4. Malika
5. Sardor
```


# 132-Topshiriq: Ikki ro'yxatni zip() orqali parallel aylanish

## Topshiriq sharti:
Mahsulotlar va ularning narxlari alohida ro'yxatda berilgan. Ularni juftlab chek shaklida chiqaring.

## Yechim (Python kodi):
```python
mahsulotlar = ["Olma", "Non", "Sut", "Go'sht", "Shakar"]
narxlar = [12000, 3500, 11000, 85000, 14000]

print("Do'kon kassa cheki:")
print("-" * 30)
jami = 0

for m, n in zip(mahsulotlar, narxlar):
    print(f"{m:10s} : {n:8,d} so'm")
    jami += n

print("-" * 30)
print(f"JAMI       : {jami:8,d} so'm")
```

## Tushuntirish va Mantiq:
1. `zip(list1, list2)` ikkala ro'yxat elementlarini bittadan moslab juftliklar (tuple) hosil qiladi.
2. `{n:8,d}` formati narxlarni minglik ajratkich (vergul) bilan tekislab chiqaradi.

## Ishlash natijasi:
```text
Chiqish: Mahsulot va narxlarning chiroyli kassa cheki ko'rinishi.
```


# 133-Topshiriq: Ro'yxatni teskari tartibda aylanib chiqish

## Topshiriq sharti:
Berilgan ro'yxat elementlarini teskari tartibda for tsikli orqali ko'rib chiqing va chiqaring.

## Yechim (Python kodi):
```python
shaharlar = ["Toshkent", "Samarqand", "Buxoro", "Xiva", "Andijon"]

print("Teskari tartibda:")
for shahar in reversed(shaharlar):
    print(shahar, end=" <- ")
print("Boshlanishi")
```

## Tushuntirish va Mantiq:
1. `reversed()` funksiyasi xotiradan yangi ro'yxat yaratmasdan, teskari iterator qaytaradi.
2. Bu katta ma'lumotlar bilan ishlashda xotirani tejaydi.

## Ishlash natijasi:
```text
Chiqish: Andijon <- Xiva <- Buxoro <- Samarqand <- Toshkent <- Boshlanishi
```


# 134-Topshiriq: Bank omonatining murakkab foizli o'sish jadvali

## Topshiriq sharti:
Boshlang'ich kapital, yillik foiz va yillar soni berilganda, har bir yildagi kapital o'sishini jadval ko'rinishida chiqaring.

## Yechim (Python kodi):
```python
kapital = float(input("Boshlang'ich summa (so'm): "))
foiz = float(input("Yillik foiz (%): "))
yillar = int(input("Necha yil: "))

print("
Yil | Omonat miqdori       | Yillik sof foyda")
print("-" * 45)

for yil in range(1, yillar + 1):
    foyda = kapital * (foiz / 100)
    kapital += foyda
    print(f"{yil:3d} | {kapital:18,.2f} | {foyda:16,.2f}")
```

## Tushuntirish va Mantiq:
1. Murakkab foizda (compound interest) yillik foyda asosiy summaga qo'shiladi va keyingi yilda shu yangi summadan foiz hisoblanadi.
2. Jadval har bir yildagi o'sishni yaqqol ko'rsatib beradi.

## Ishlash natijasi:
```text
Kiritish: 10,000,000 so'm, 20%, 3 yil -> Yillik o'sish jadvali hosil bo'ladi.
```


# 135-Topshiriq: Valyuta konvertatsiya jadvalini qadamli chiqarish

## Topshiriq sharti:
10 dollardan 100 dollargacha (10 dollar qadam bilan) so'mdagi qiymatlarini ko'rsatuvchi jadval tuzing.

## Yechim (Python kodi):
```python
kurs = float(input("1 AQSH dollari kursi (so'mda): "))

print("
AQSH Dollari ($) | O'zbek So'mi (UZS)")
print("-" * 35)

for dollar in range(10, 101, 10):
    som = dollar * kurs
    print(f"${dollar:14d} | {som:16,.2f} UZS")
```

## Tushuntirish va Mantiq:
1. `range(10, 101, 10)` qiymatlari 10, 20, 30 ... 100 gacha qadamlaydi.
2. Valyuta almashinuv shoxobchalari uchun qulay ma'lumotnoma jadvali hosil qilinadi.

## Ishlash natijasi:
```text
Kiritish: 12800 -> Chiqish: $10 = 128,000 UZS ... $100 = 1,280,000 UZS
```


# 136-Topshiriq: Maxfiy sonni topish o'yini (Binary Search mantiqi)

## Topshiriq sharti:
Kompyuter 1 dan 100 gacha son o'ylaydi. Foydalanuvchi sonni topguncha 'Kattaroq' yoki 'Kichikroq' deb yo'naltiruvchi dastur tuzing.

## Yechim (Python kodi):
```python
import random

maxfiy = random.randint(1, 100)
urinishlar = 0

print("Men 1 dan 100 gacha son o'yladim. Uni topa olasizmi?")

while True:
    taxmin = int(input("Taxminingizni kiriting: "))
    urinishlar += 1

    if taxmin == maxfiy:
        print(f"Tabriklaymiz! Siz {urinishlar} ta urinishda topdingiz!")
        break
    elif taxmin < maxfiy:
        print("Men o'ylagan son bundan KATTAROQ!")
    else:
        print("Men o'ylagan son bundan KICHIKROQ!")
```

## Tushuntirish va Mantiq:
1. `random.randint(1, 100)` tasodifiy son tanlaydi.
2. `while True` tsikli foydalanuvchi to'g'ri topmaguncha qayta-qayta savol beradi va `urinishlar` hisoblagichini oshirib boradi.

## Ishlash natijasi:
```text
Namuna: 50 -> KATTAROQ, 75 -> KICHIKROQ, 63 -> To'g'ri topdingiz!
```


# 137-Topshiriq: 8x8 shaxmat taxtasi naqshini generatsiya qilish

## Topshiriq sharti:
Ichma-ich tsikllar yordamida shaxmat taxtasi katakchalarini '#' (qora) va ' ' (oq) belgilar bilan chiqaring.

## Yechim (Python kodi):
```python
olcham = 8

for qator in range(olcham):
    qator_matni = ""
    for ustun in range(olcham):
        if (qator + ustun) % 2 == 0:
            qator_matni += "[#]"
        else:
            qator_matni += "[ ]"
    print(qator_matni)
```

## Tushuntirish va Mantiq:
1. `(qator + ustun) % 2 == 0` sharti shaxmat tartibini (shaxmat shataklarini) mukammal ta'minlaydi.
2. Har bir qator 8 ta katakchadan iborat qilib shakllantiriladi.

## Ishlash natijasi:
```text
Chiqish: 8x8 oq va qora katakchalardan iborat shaxmat taxtasi tasviri.
```


# 138-Topshiriq: O'sib boruvchi onlayn o'rtacha qiymat

## Topshiriq sharti:
Foydalanuvchi kiritgan har bir yangi sondan keyin shu paytgacha kiritilgan barcha sonlarning o'rta arifmetigini real vaqtda yangilab boring.

## Yechim (Python kodi):
```python
jami = 0.0
soni = 0

print("Sonlarni kiriting (chiqish uchun '0' kiriting):")
while True:
    qiymat = float(input(f"{soni + 1}-son: "))
    if qiymat == 0:
        break
    jami += qiymat
    soni += 1
    ortacha = jami / soni
    print(f"Joriy soni: {soni} ta | Yig'indi: {jami:.2f} | O'rtacha: {ortacha:.2f}")

print("Dastur yakunlandi.")
```

## Tushuntirish va Mantiq:
1. Ma'lumotlar oqimida (stream processing) har bir yangi kelgan qiymat jami yig'indiga qo'shiladi va yangi o'rtacha qiymat qayta hisoblanadi.

## Ishlash natijasi:
```text
Kiritish: 10 -> O'rtacha: 10.00, 20 -> O'rtacha: 15.00, 30 -> O'rtacha: 20.00
```


# 139-Topshiriq: Sonning darajasini ko'paytirish tsikli bilan topish

## Topshiriq sharti:
Asos a va daraja n berilganda, `**` darajaga ko'tarish operatorsiz, faqat ko'paytirish va tsikl yordamida a^n ni hisoblang.

## Yechim (Python kodi):
```python
a = float(input("Asos (a): "))
n = int(input("Daraja ko'rsatkichi (butun son, n): "))

if n == 0:
    natija = 1.0
else:
    natija = 1.0
    musbat_n = abs(n)
    for _ in range(musbat_n):
        natija *= a
    if n < 0:
        natija = 1.0 / natija

print(f"{a}^{n} = {natija}")
```

## Tushuntirish va Mantiq:
1. a^n n marta a ni o'ziga ko'paytirish demakdir.
2. Agar daraja manfiy bo'lsa (n < 0), hisoblangan natija 1 / natija ga aylantiriladi.

## Ishlash natijasi:
```text
Kiritish: a=2, n=5 -> Chiqish: 2^5 = 32.0
Kiritish: a=2, n=-3 -> Chiqish: 2^-3 = 0.125
```


# 140-Topshiriq: Ketma-ket kelgan bir xil belgilarni sanash

## Topshiriq sharti:
Satr ichidagi ketma-ket takrorlangan belgilarni sanab chiqaring (masalan, 'AAABBBCC' -> 3 ta A, 3 ta B, 2 ta C).

## Yechim (Python kodi):
```python
matn = input("Satr kiriting (masalan AAABBBCCDAA): ")

if not matn:
    print("Bo'sh satr kiritildi.")
else:
    natija = []
    joriy_belgi = matn[0]
    hisob = 1

    for ch in matn[1:]:
        if ch == joriy_belgi:
            hisob += 1
        else:
            natija.append(f"{hisob}{joriy_belgi}")
            joriy_belgi = ch
            hisob = 1
    natija.append(f"{hisob}{joriy_belgi}")

    print("Siqilgan ko'rinish (RLE):", "".join(natija))
```

## Tushuntirish va Mantiq:
1. Run-Length Encoding (RLE) ma'lumotlarni yo'qotishsiz siqishning eng sodda va samarali algoritmidir.
2. Tsikl belgi o'zgarganda oraliq natijani ro'yxatga saqlab, yangi belgini sanashni boshlaydi.

## Ishlash natijasi:
```text
Kiritish: AAABBBCC -> Chiqish: 3A3B2C
```


# 141-Topshiriq: 24 soatlik formatdagi barcha vaqtlarni chiqarish

## Topshiriq sharti:
00:00 dan 23:59 gacha bo'lgan vaqtlarni ichma-ich tsikllar orqali ikki xonali formatda chiqaring.

## Yechim (Python kodi):
```python
qadam = 15  # Har 15 daqiqadagi vaqtlar
print(f"Kunlik vaqtlar rejasi (har {qadam} daqiqada):")

for soat in range(24):
    for daqiqa in range(0, 60, qadam):
        print(f"{soat:02d}:{daqiqa:02d}", end="  ")
    print()  # Har soat tugagach yangi qator
```

## Tushuntirish va Mantiq:
1. `{soat:02d}` formati 1 xonali sonlarni oldiga 0 qo'yib (masalan: 05) 2 xonali qilib chiqaradi.
2. Ichki tsikl `range(0, 60, 15)` orqali har 15 daqiqalik intervallarni chiqaradi.

## Ishlash natijasi:
```text
Chiqish: 00:00 00:15 00:30 00:45 ... 23:45
```


# 142-Topshiriq: PIN-kod kiritish va xavfsiz bloklash

## Topshiriq sharti:
Foydalanuvchiga to'g'ri PIN-kodni kiritish uchun maksimal 3 ta imkoniyat bering. 3 marta xato kiritilsa kartani bloklang.

## Yechim (Python kodi):
```python
HAQIQIY_PIN = "7788"
urinishlar_chegarasi = 3

for urinish in range(1, urinishlar_chegarasi + 1):
    kiritilgan_pin = input(f"PIN-kodni kiriting ({urinish}-urinish): ").strip()
    if kiritilgan_pin == HAQIQIY_PIN:
        print("Muvaffaqiyatli! Tizimga xush kelibsiz!")
        break
    else:
        qolgan = urinishlar_chegarasi - urinish
        if qolgan > 0:
            print(f"Noto'g'ri PIN! Qolgan urinishlar soni: {qolgan}")
        else:
            print("XAVFSIZLIK: 3 marta noto'g'ri kiritildi! Kartangiz 24 soatga bloklandi!")
```

## Tushuntirish va Mantiq:
1. `range(1, 4)` 3 ta imkoniyat beradi.
2. To'g'ri kiritilganda `break` orqali tsikldan chiqiladi, aks holda ogohlantirish beriladi.

## Ishlash natijasi:
```text
Kiritish: 1234 (Noto'g'ri), 7788 -> Chiqish: Muvaffaqiyatli!
```


# 143-Topshiriq: Matndagi so'zlarning uzunligini hisoblash

## Topshiriq sharti:
Foydalanuvchi kiritgan gapdagi har bir so'zning necha harfdan iborat ekanligini for tsikli orqali ko'rsating.

## Yechim (Python kodi):
```python
gap = input("Biror jumla kiriting: ")

sozlar = gap.split()

print("
So'zlar tahlili:")
for tartib, soz in enumerate(sozlar, start=1):
    toza_soz = soz.strip(".,!?:;"'()")
    print(f"{tartib}. '{toza_soz}' -> {len(toza_soz)} ta harf")
```

## Tushuntirish va Mantiq:
1. `gap.split()` bo'shliqlar bo'yicha matnni so'zlarga ajratadi.
2. `.strip('.,!?:;')` tinish belgilarini chetlatib, faqat so'zning o'z uzunligini aniqlashga xizmat qiladi.

## Ishlash natijasi:
```text
Kiritish: O'zbekiston kelajagi buyuk davlat!
Chiqish: O'zbekiston (11), kelajagi (8), buyuk (5), davlat (6)
```


# 144-Topshiriq: Matndagi unli harflarni sanash

## Topshiriq sharti:
Kiritilgan matndagi barcha o'zbek tili unli harflari (a, o, i, u, e, o') sonini for tsikli orqali sanang.

## Yechim (Python kodi):
```python
matn = input("Matn kiriting: ").lower()

unlilar = "aeiouoʻo'o`"
unli_soni = 0
batafsil = {}

for ch in matn:
    if ch in unlilar:
        unli_soni += 1
        batafsil[ch] = batafsil.get(ch, 0) + 1

print(f"Jami unli harflar soni: {unli_soni} ta")
print(f"Harflar bo'yicha taqsimot: {batafsil}")
```

## Tushuntirish va Mantiq:
1. `if ch in unlilar:` a'zolik operatori belgi unlilar to'plamiga kirishini tekshiradi.
2. Lug'at (dictionary) yordamida qaysi unli necha marta qatnashgani ham sanab boriladi.

## Ishlash natijasi:
```text
Kiritish: Assalomu alaykum -> Chiqish: Jami unlilar: 7 ta
```


# 145-Topshiriq: Oddiy Sezar shifrlash algoritmi

## Topshiriq sharti:
Matndagi har bir lotin harfini alifboda N ta pozitsiya oldinga surish orqali shifrlang.

## Yechim (Python kodi):
```python
matn = input("Shifrlanadigan matnni kiriting: ")
siljish = int(input("Siljish kaliti (masalan 3): "))

shifrlangan = []

for ch in matn:
    if 'a' <= ch <= 'z':
        yangi = chr((ord(ch) - ord('a') + siljish) % 26 + ord('a'))
        shifrlangan.append(yangi)
    elif 'A' <= ch <= 'Z':
        yangi = chr((ord(ch) - ord('A') + siljish) % 26 + ord('A'))
        shifrlangan.append(yangi)
    else:
        shifrlangan.append(ch)  # Belgilar va tinish belgilari o'zgarmaydi

natija = "".join(shifrlangan)
print(f"Shifrlangan matn: {natija}")
```

## Tushuntirish va Mantiq:
1. `ord(ch)` belgining ASCII kodini, `chr()` esa kodning belgisini qaytaradi.
2. `% 26` moduli alifbo chegarasidan chiqib ketmasdan, aylanma ravishda qaytishini kafolatlaydi.

## Ishlash natijasi:
```text
Kiritish: 'Salom', Kalit: 3 -> Chiqish: 'Vdorpr'
```


# 146-Topshiriq: Monoton o'suvchi ketma-ketlik uzunligini topish

## Topshiriq sharti:
Sonlar ro'yxatidagi eng uzun uzluksiz o'suvchi qism-ketma-ketlik (subarray) uzunligini aniqlang.

## Yechim (Python kodi):
```python
sonlar = [1, 2, 2, 4, 7, 3, 5, 8, 9, 10, 2]

maks_uzunlik = 1
joriy_uzunlik = 1

for i in range(1, len(sonlar)):
    if sonlar[i] > sonlar[i - 1]:
        joriy_uzunlik += 1
        if joriy_uzunlik > maks_uzunlik:
            maks_uzunlik = joriy_uzunlik
    else:
        joriy_uzunlik = 1

print(f"Sonlar: {sonlar}")
print(f"Eng uzun o'suvchi qism uzunligi: {maks_uzunlik} ta element")
```

## Tushuntirish va Mantiq:
1. Tsikl har bir elementni o'zidan oldingi element bilan solishtiradi.
2. Agar tartib buzilsa, `joriy_uzunlik` yana 1 ga tenglashtiriladi.

## Ishlash natijasi:
```text
[1, 2, 2, 4, 7, 3, 5, 8, 9, 10, 2] -> 5 ta (3, 5, 8, 9, 10)
```


# 147-Topshiriq: Klassik FizzBuzz dasturi

## Topshiriq sharti:
1 dan 100 gacha sonlar: 3 ga bo'linsa 'Fizz', 5 ga bo'linsa 'Buzz', ikkalasiga ham bo'linsa 'FizzBuzz' deb chiqaring.

## Yechim (Python kodi):
```python
for son in range(1, 101):
    if son % 15 == 0:
        print("FizzBuzz", end=" ")
    elif son % 3 == 0:
        print("Fizz", end=" ")
    elif son % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(son, end=" ")
print()
```

## Tushuntirish va Mantiq:
1. Eng muhim qoida: 15 ga (ham 3 ga, ham 5 ga) bo'linish sharti eng birinchi tekshirilishi shart.
2. Aks holda 15 soni birinchi `son % 3 == 0` shartiga tushib, noto'g'ri 'Fizz' bo'lib qolardi.

## Ishlash natijasi:
```text
Chiqish: 1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz ...
```


# 148-Topshiriq: Ro'yxatdagi takrorlangan elementlarni saralash

## Topshiriq sharti:
Elementlar tartibini saqlagan holda ro'yxatdan barcha dublikatlarni tsikl orqali olib tashlang.

## Yechim (Python kodi):
```python
elementlar = [4, 7, 2, 4, 9, 7, 1, 2, 8, 5, 4]

takrorlanmas = []
for x in elementlar:
    if x not in takrorlanmas:
        takrorlanmas.append(x)

print(f"Asl ro'yxat: {elementlar}")
print(f"Dublikatlarsiz toza ro'yxat: {takrorlanmas}")
```

## Tushuntirish va Mantiq:
1. `if x not in takrorlanmas:` yangi ro'yxatda ushbu element yo'qligini tekshiradi.
2. Bu usul oddiy `set()` to'plamiga nisbatan elementlarning asl kelish tartibini (order) 100% saqlab qoladi.

## Ishlash natijasi:
```text
Kiritish: [4, 7, 2, 4, 9, 7] -> Chiqish: [4, 7, 2, 9]
```


# 149-Topshiriq: Kvadrat matritsa diagonallari yig'indisi

## Topshiriq sharti:
N x N o'lchamli matritsaning asosiy va yordamchi diagonallari elementlari yig'indisini hisoblang.

## Yechim (Python kodi):
```python
matritsa = [
    [1,  2,  3,  4],
    [5,  6,  7,  8],
    [9,  10, 11, 12],
    [13, 14, 15, 16]
]

n = len(matritsa)
asosiy_yigindi = 0
yordamchi_yigindi = 0

for i in range(n):
    asosiy_yigindi += matritsa[i][i]              # Asosiy diagonal: [i][i]
    yordamchi_yigindi += matritsa[i][n - 1 - i]    # Yordamchi diagonal: [i][n - 1 - i]

print(f"Matritsa o'lchami: {n}x{n}")
print(f"Asosiy diagonal yig'indisi (1+6+11+16): {asosiy_yigindi}")
print(f"Yordamchi diagonal yig'indisi (4+7+10+13): {yordamchi_yigindi}")
```

## Tushuntirish va Mantiq:
1. Asosiy diagonalda qator va ustun indekslari teng bo'ladi: `[i][i]`.
2. Yordamchi diagonalda qator va ustun yig'indisi `n - 1` ga teng: `[i][n - 1 - i]`.

## Ishlash natijasi:
```text
Chiqish: Asosiy: 34, Yordamchi: 34
```


# 150-Topshiriq: Terminalda Progress Bar (Yuklanish indikatori) simulyatsiyasi

## Topshiriq sharti:
Terminalda vazifaning bajarilish jarayonini vizual ko'rsatuvchi dinamik foizli progress bar dasturini tuzing.

## Yechim (Python kodi):
```python
import time
import sys

jami_qadamlar = 50
kenglik = 30  # Chiziqning belgilar soni

print("Fayllarni qayta ishlash boshlandi:")

for i in range(jami_qadamlar + 1):
    foiz = int((i / jami_qadamlar) * 100)
    toldirilgan = int(kenglik * i // jami_qadamlar)
    chiziq = '█' * toldirilgan + '-' * (kenglik - toldirilgan)
    
    # \r kursor boshiga qaytaradi, shu orqali yangi qator ochmasdan bitta joyda yangilanadi
    sys.stdout.write(f"\rJarayon: [{chiziq}] {foiz}% ({i}/{jami_qadamlar})")
    sys.stdout.flush()
    time.sleep(0.04)  # Qisqa tanaffus simulyatsiyasi

print("\nBarcha ma'lumotlar muvaffaqiyatli qayta ishlandi!")
```

## Tushuntirish va Mantiq:
1. `\r` (carriage return) kursorni terminal qatori boshiga qaytaradi, shunda yangi qatorga o'tmasdan oldingi matn ustidan yoziladi.
2. `sys.stdout.flush()` buferni zudlik bilan terminalga chiqarishga majburlaydi.

## Ishlash natijasi:
```text
Chiqish: Jarayon: [██████████████████████████████] 100% (50/50)
```

