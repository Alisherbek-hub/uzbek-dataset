# Python Dasturlash Tili — 5-Qism: Ro'yxatlar (Lists) va Kortejlar (Tuples) bilan Mukammal Ishlash
## (201-250 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam ro'yxatlar va kortejlar bo'yicha eng muhim ma'lumotlar tuzilmalarini qamrab oladi:
* Ro'yxat metodlari: `append`, `insert`, `extend`, `pop`, `remove`, `clear`;
* Saralash algoritmlari: Bubble sort, `sorted()`, lambda kalitlari bilan saralash;
* To'plam amallari: kesishma, birlashma, ayirma, Kadane algoritmi, zik-zak;
* Kortejlar (tuples): o'zgarmaslik (immutability), unpacking, ko'p qiymat qaytarish;
* Amaliyot: 2D matritsalar, transponatsiya, normalizatsiya, medianani hisoblash;

---

# 201-Topshiriq: Ro'yxat metodlari (append, insert, extend, pop, remove)

## Topshiriq sharti:
Ro'yxatga yangi element qo'shish, indeks bo'yicha kiritish, ro'yxatni kengaytirish va elementlarni o'chirish amallarini ko'rsating.

## Yechim (Python kodi):
```python
mevalar = ["olma", "anor", "uzum"]

# 1. append — oxiriga qo'shish
mevalar.append("banan")

# 2. insert — ko'rsatilgan indeksga kiritish
mevalar.insert(1, "shaftoli")

# 3. extend — boshqa ro'yxat bilan kengaytirish
mevalar.extend(["nok", "o'rik"])

# 4. remove — qiymat bo'yicha birinchi uchraganini o'chirish
mevalar.remove("anor")

# 5. pop — indeks bo'yicha sug'urib olish (standart bo'yicha oxirgisini)
sugurilgan = mevalar.pop(0)

print(f"Sug'urib olingan meva: {sugurilgan}")
print(f"Yakuniy ro'yxat: {mevalar}")
```

## Tushuntirish va Mantiq:
1. `append(x)` elementni ro'yxat oxiriga O(1) vaqtda qo'shadi.
2. `insert(i, x)` elementni i-o'ringa joylab, keyingilarini o'ngga suradi.
3. `pop(i)` elementni ro'yxatdan o'chirib, o'zgaruvchiga qaytaradi.

## Ishlash natijasi:
```text
Chiqish: Sug'urilgan: olma, Yakuniy: ['shaftoli', 'uzum', 'banan', 'nok', "o'rik"]
```


# 202-Topshiriq: Maksimum va minimum elementlarni algoritmik topish

## Topshiriq sharti:
Ro'yxatdagi eng katta va eng kichik sonlarni tayyor `max()` va `min()` funksiyalarisiz, bitta for tsiklida toping.

## Yechim (Python kodi):
```python
sonlar = [23, 45, 12, 89, 4, 67, 91, 34, 2]

if not sonlar:
    print("Ro'yxat bo'sh!")
else:
    eng_katta = sonlar[0]
    eng_kichik = sonlar[0]

    for son in sonlar[1:]:
        if son > eng_katta:
            eng_katta = son
        if son < eng_kichik:
            eng_kichik = son

    print(f"Sonlar: {sonlar}")
    print(f"Eng katta element: {eng_katta}")
    print(f"Eng kichik element: {eng_kichik}")
```

## Tushuntirish va Mantiq:
1. Ro'yxatning 1-elementini boshlang'ich maksimum va minimum deb olamiz.
2. Tsikl davomida har bir element solishtirilib, qiymatlar yangilanib boradi.

## Ishlash natijasi:
```text
Chiqish: Eng katta: 91, Eng kichik: 2
```


# 203-Topshiriq: Ro'yxat yig'indisi va o'rta arifmetigini hisoblash

## Topshiriq sharti:
Sonlar ro'yxatining yig'indisini va o'rta arifmetik qiymatini `sum()` va `len()` siz hisoblang.

## Yechim (Python kodi):
```python
baholar = [85, 90, 78, 92, 88, 76, 95]

jami = 0
soni = 0

for b in baholar:
    jami += b
    soni += 1

ortacha = jami / soni if soni > 0 else 0

print(f"Baholar ro'yxati: {baholar}")
print(f"Jami ball: {jami}")
print(f"Talabalar soni: {soni} ta")
print(f"O'rtacha ball: {ortacha:.2f}")
```

## Tushuntirish va Mantiq:
1. Tsikl har bir sonni jamlab va hisoblagichni oshirib boradi.
2. Yakunda jami yig'indi sonlar miqdoriga bo'linadi.

## Ishlash natijasi:
```text
Chiqish: Jami: 604, Soni: 7, O'rtacha: 86.29
```


# 204-Topshiriq: Pufakchali saralash algoritmi (Bubble Sort)

## Topshiriq sharti:
Sonlar ro'yxatini klassik pufakchali saralash (Bubble sort) algoritmi yordamida o'sish tartibida saralang.

## Yechim (Python kodi):
```python
massiv = [64, 34, 25, 12, 22, 11, 90]
n = len(massiv)

for i in range(n):
    almashtirildimi = False
    for j in range(0, n - i - 1):
        if massiv[j] > massiv[j + 1]:
            # Qo'shni elementlar o'rnini almashtiramiz
            massiv[j], massiv[j + 1] = massiv[j + 1], massiv[j]
            almashtirildimi = True
    # Agar hech qanday almashish bo'lmasa, demak ro'yxat saralanib bo'lgan
    if not almashtirildimi:
        break

print(f"Saralangan massiv: {massiv}")
```

## Tushuntirish va Mantiq:
1. Bubble sort har qadamda eng katta elementni ro'yxat oxiriga 'pufakcha' kabi chiqarib qo'yadi.
2. `almashtirildimi` bayrog'i ro'yxat allaqachon saralangan bo'lsa ortiqcha iteratsiyalarni to'xtatadi.

## Ishlash natijasi:
```text
Chiqish: [11, 12, 22, 25, 34, 64, 90]
```


# 205-Topshiriq: Ro'yxatni juft va toq sonlarga ajratish

## Topshiriq sharti:
Bitta aralash sonlar ro'yxatidan faqat juft sonlar va faqat toq sonlardan iborat ikkita yangi ro'yxat hosil qiling.

## Yechim (Python kodi):
```python
sonlar = [14, 7, 22, 31, 40, 55, 68, 73, 80, 99]

juftlar = [x for x in sonlar if x % 2 == 0]
toqlar = [x for x in sonlar if x % 2 != 0]

print(f"Asl ro'yxat: {sonlar}")
print(f"Juft sonlar: {juftlar}")
print(f"Toq sonlar : {toqlar}")
```

## Tushuntirish va Mantiq:
1. List comprehension yordamida shart orqali filtrlash eng toza va Pythonik usul hisoblanadi.
2. `x % 2 == 0` juftlik shartidir.

## Ishlash natijasi:
```text
Chiqish: Juftlar: [14, 22, 40, 68, 80], Toqlar: [7, 31, 55, 73, 99]
```


# 206-Topshiriq: Ikki ro'yxatning kesishuvi (Intersection)

## Topshiriq sharti:
Ikkala ro'yxatda ham mavjud bo'lgan umumiy elementlarni takrorlanmas shaklda ajrating.

## Yechim (Python kodi):
```python
a = [1, 2, 3, 4, 5, 6, 7]
b = [4, 5, 6, 7, 8, 9, 10]

# 1-usul: To'plam (set) orqali
umumiy_set = list(set(a) & set(b))

# 2-usul: List comprehension orqali (tartib saqlanadi)
umumiy_list = [x for x in a if x in b]

print(f"A ro'yxat: {a}")
print(f"B ro'yxat: {b}")
print(f"Umumiy elementlar: {sorted(umumiy_set)}")
```

## Tushuntirish va Mantiq:
1. `set(a) & set(b)` to'plamlar kesishmasini O(min(len(a), len(b))) tezlikda topadi.

## Ishlash natijasi:
```text
Chiqish: Umumiy: [4, 5, 6, 7]
```


# 207-Topshiriq: Ikki ro'yxatning birlashmasi (Union)

## Topshiriq sharti:
Ikki ro'yxatdagi barcha elementlarni birlashtiring va dublikatlarni olib tashlang.

## Yechim (Python kodi):
```python
guruh1 = ["Ali", "Vali", "Hasan", "Zuhra"]
guruh2 = ["Vali", "Olim", "Zuhra", "Botir"]

birlashma = list(set(guruh1) | set(guruh2))
birlashma.sort()

print(f"Barcha talabalar ({len(birlashma)} ta): {birlashma}")
```

## Tushuntirish va Mantiq:
1. `set(a) | set(b)` to'plamlar birlashmasi amali hisoblanadi.
2. `sort()` ro'yxatni alifbo tartibida tartiblaydi.

## Ishlash natijasi:
```text
Chiqish: ['Ali', 'Botir', 'Hasan', 'Olim', 'Vali', 'Zuhra']
```


# 208-Topshiriq: Ikki ro'yxat ayirmasi (Difference)

## Topshiriq sharti:
1-ro'yxatda bor, lekin 2-ro'yxatda yo'q bo'lgan elementlarni toping.

## Yechim (Python kodi):
```python
barcha_kitoblar = ["O'tkan kunlar", "Mehrobdan chayon", "Sarob", "Shum bola", "Yulduzli tunlar"]
oqilgan_kitoblar = ["O'tkan kunlar", "Shum bola"]

oqilmaganlar = [k for k in barcha_kitoblar if k not in oqilgan_kitoblar]

print(f"O'qilishi kerak bo'lgan kitoblar: {oqilmaganlar}")
```

## Tushuntirish va Mantiq:
1. `if k not in oqilgan_kitoblar` 2-ro'yxatda bo'lmagan elementlarni qoldiradi.

## Ishlash natijasi:
```text
Chiqish: ["Mehrobdan chayon", "Sarob", "Yulduzli tunlar"]
```


# 209-Topshiriq: Ro'yxatni k qadam siklik siljitish (Rotate List)

## Topshiriq sharti:
Ro'yxat elementlarini k ta pozitsiya o'ngga suruvchi dastur yozing (oxirgi elementlar boshiga o'tadi).

## Yechim (Python kodi):
```python
massiv = [1, 2, 3, 4, 5, 6, 7]
k = 3

k = k % len(massiv)  # Ortiqcha to'liq aylanishlarni hisobga olamiz
siljigan = massiv[-k:] + massiv[:-k]

print(f"Asl ro'yxat: {massiv}")
print(f"{k} qadam o'ngga siljigan: {siljigan}")
```

## Tushuntirish va Mantiq:
1. `massiv[-k:]` oxirgi k ta elementni oladi.
2. `massiv[:-k]` boshidan boshlab oxirgi k ta elementgacha bo'lgan qismini oladi.
3. Ikkalasini `+` bilan ulash elementlarni to'liq siljitadi.

## Ishlash natijasi:
```text
Kiritish: [1, 2, 3, 4, 5, 6, 7], k=3 -> Chiqish: [5, 6, 7, 1, 2, 3, 4]
```


# 210-Topshiriq: Manfiy sonlarni nolga almashtirish

## Topshiriq sharti:
Ro'yxatdagi barcha manfiy sonlarni 0 ga, musbatlarini esa o'z holicha qoldiring.

## Yechim (Python kodi):
```python
qiymatlar = [12, -5, 8, -19, 0, 44, -3, 17]

tozalangan = [x if x >= 0 else 0 for x in qiymatlar]

print(f"Asl qiymatlar: {qiymatlar}")
print(f"Manfiysiz:     {tozalangan}")
```

## Tushuntirish va Mantiq:
1. Ternary operator `x if x >= 0 else 0` shart bo'yicha qiymat tanlaydi.
2. Bu neyron tarmoqlaridagi ReLU (Rectified Linear Unit) faollashtirish funksiyasi mantiqidir.

## Ishlash natijasi:
```text
Chiqish: [12, 0, 8, 0, 0, 44, 0, 17]
```


# 211-Topshiriq: Kvadratlar ro'yxatini hosil qilish (List Comprehension)

## Topshiriq sharti:
1 dan 20 gacha bo'lgan sonlarning kvadratlaridan iborat ro'yxatni bitta qatorda yarating.

## Yechim (Python kodi):
```python
kvadratlar = [x ** 2 for x in range(1, 21)]

print(f"1 dan 20 gacha kvadratlar: {kvadratlar}")
```

## Tushuntirish va Mantiq:
1. `[x**2 for x in range(1, 21)]` sintaksisi an'anaviy 4 qatorli for tsikli o'rnini bosadi va ancha tez ishlaydi.

## Ishlash natijasi:
```text
Chiqish: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400]
```


# 212-Topshiriq: Filtrlangan List Comprehension

## Topshiriq sharti:
1 dan 50 gacha bo'lgan sonlar orasidan ham 3 ga, ham 5 ga bo'linadigan sonlarning kublar ro'yxatini tuzing.

## Yechim (Python kodi):
```python
mos_sonlar = [x ** 3 for x in range(1, 51) if x % 15 == 0]

print(f"15 ga karrali sonlarning kublari: {mos_sonlar}")
```

## Tushuntirish va Mantiq:
1. List comprehension oxiriga `if x % 15 == 0` filtri qo'shiladi.

## Ishlash natijasi:
```text
Chiqish: [3375, 27000, 91125] (15^3, 30^3, 45^3)
```


# 213-Topshiriq: Ichma-ich ro'yxatni yassilash (Flatten 2D List)

## Topshiriq sharti:
Ikki o'lchamli matritsani bitta o'lchamli tekis ro'yxatga (flat list) aylantiring.

## Yechim (Python kodi):
```python
matritsa = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Ichma-ich list comprehension
yassi = [element for qator in matritsa for element in qator]

print(f"2D matritsa: {matritsa}")
print(f"1D yassi ro'yxat: {yassi}")
```

## Tushuntirish va Mantiq:
1. `for qator in matritsa` har bir satrni oladi.
2. `for element in qator` ushbu satr ichidagi har bir elementni alohida chiqarib, yakuniy ro'yxatga joylaydi.

## Ishlash natijasi:
```text
Chiqish: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```


# 214-Topshiriq: Eng ko'p takrorlangan elementni (Moda) topish

## Topshiriq sharti:
Ro'yxatdagi eng ko'p uchragan sonni va uning takrorlanishlar sonini aniqlang.

## Yechim (Python kodi):
```python
sonlar = [1, 3, 2, 5, 3, 2, 3, 4, 3, 1, 5, 3]

chastota = {}
for s in sonlar:
    chastota[s] = chastota.get(s, 0) + 1

eng_kop = max(chastota, key=chastota.get)

print(f"Ro'yxat: {sonlar}")
print(f"Moda (eng ko'p uchragan son): {eng_kop} ({chastota[eng_kop]} marta)")
```

## Tushuntirish va Mantiq:
1. Lug'at har bir elementning necha marta uchraganini saqlaydi.
2. `max(..., key=chastota.get)` eng katta takrorlanish soniga ega kalitni qaytaradi.

## Ishlash natijasi:
```text
Chiqish: Moda: 3 (5 marta)
```


# 215-Topshiriq: Ikkinchi eng katta elementni topish (Second Largest)

## Topshiriq sharti:
Ro'yxatdagi eng katta elementdan keyin turuvchi ikkinchi eng katta elementni toping.

## Yechim (Python kodi):
```python
sonlar = [10, 45, 23, 89, 89, 56, 78]

# Dublikatlarni olib tashlaymiz
noyob = list(set(sonlar))
noyob.sort()

if len(noyob) < 2:
    print("Kamida 2 ta har xil son bo'lishi kerak!")
else:
    ikkinchi_katta = noyob[-2]
    print(f"Sonlar: {sonlar}")
    print(f"Eng katta: {noyob[-1]}")
    print(f"Ikkinchi eng katta: {ikkinchi_katta}")
```

## Tushuntirish va Mantiq:
1. `set()` orqali 89 kabi takrorlangan eng katta son bitta qilinadi.
2. Saralangach `[-2]` indeksi ikkinchi eng kattani aniq beradi.

## Ishlash natijasi:
```text
Chiqish: Eng katta: 89, Ikkinchi eng katta: 78
```


# 216-Topshiriq: Ro'yxat elementlari ko'paytmasini hisoblash

## Topshiriq sharti:
Ro'yxatdagi barcha sonlarning umumiy ko'paytmasini topuvchi funksiya tuzing.

## Yechim (Python kodi):
```python
sonlar = [2, 3, 4, 5, 6]

kopaytma = 1
for s in sonlar:
    kopaytma *= s

print(f"Sonlar: {sonlar}")
print(f"Ko'paytmasi: {kopaytma}")
```

## Tushuntirish va Mantiq:
1. Boshlang'ich qiymat 1 qilib olinadi.
2. Har bir element ketma-ket ko'paytirib boriladi.

## Ishlash natijasi:
```text
Chiqish: Ko'paytmasi: 720 (2*3*4*5*6)
```


# 217-Topshiriq: Elementning barcha indekslarini topish

## Topshiriq sharti:
Ro'yxatda qidirilayotgan element qaysi barcha indekslarda joylashganini toping.

## Yechim (Python kodi):
```python
ro'yxat = ["a", "b", "c", "a", "d", "a", "e"]
qidirilayotgan = "a"

indekslar = [i for i, x in enumerate(ro'yxat) if x == qidirilayotgan]

print(f"Element '{qidirilayotgan}' quyidagi indekslarda joylashgan: {indekslar}")
```

## Tushuntirish va Mantiq:
1. `enumerate()` indeks va qiymatni birgalikda taqdim etadi.
2. Shartga mos barcha indekslar ro'yxatga yig'iladi.

## Ishlash natijasi:
```text
Chiqish: [0, 3, 5]
```


# 218-Topshiriq: Barcha nollarni ro'yxat oxiriga ko'chirish (Move Zeroes)

## Topshiriq sharti:
Nol bo'lmagan elementlarning tartibini saqlagan holda barcha 0 larni ro'yxat oxiriga o'tkazing.

## Yechim (Python kodi):
```python
massiv = [0, 1, 0, 3, 12, 0, 5, 8]

nol_emas = [x for x in massiv if x != 0]
nollar_soni = len(massiv) - len(nol_emas)
natija = nol_emas + [0] * nollar_soni

print(f"Asl massiv: {massiv}")
print(f"Nollari oxiriga surilgan: {natija}")
```

## Tushuntirish va Mantiq:
1. Noldan farqlilar ajratib olinadi.
2. Yetishmayotgan miqdordagi nollar `[0] * soni` orqali oxiriga ulanadi.

## Ishlash natijasi:
```text
Chiqish: [1, 3, 12, 5, 8, 0, 0, 0]
```


# 219-Topshiriq: Maksimal qism-massiv yig'indisi (Kadane Algoritmi)

## Topshiriq sharti:
Manfiy va musbat sonlar aralash ro'yxatidan yig'indisi eng katta bo'lgan uzluksiz qism-massivni toping.

## Yechim (Python kodi):
```python
sonlar = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

maks_yigindi = sonlar[0]
joriy_yigindi = sonlar[0]

for x in sonlar[1:]:
    joriy_yigindi = max(x, joriy_yigindi + x)
    maks_yigindi = max(maks_yigindi, joriy_yigindi)

print(f"Massiv: {sonlar}")
print(f"Maksimal qism-massiv yig'indisi: {maks_yigindi}")
```

## Tushuntirish va Mantiq:
1. Kadane algoritmi O(n) chiziqli vaqtda optimal yechimni beradi.
2. Har bir qadamda yangi elementdan yangi ketma-ketlik boshlash yoki oldingisiga qo'shish tanlanadi.

## Ishlash natijasi:
```text
Chiqish: 6 (qism: [4, -1, 2, 1])
```


# 220-Topshiriq: Palindrom ro'yxatni tekshirish

## Topshiriq sharti:
Ro'yxat chapdan ham, o'ngdan ham bir xil o'qiladimi (palindrommi) yo'qligini aniqlang.

## Yechim (Python kodi):
```python
r1 = [1, 2, 3, 2, 1]
r2 = [1, 2, 3, 4, 5]

def palindrommi(r):
    return r == r[::-1]

print(f"{r1} — Palindrommi? {palindrommi(r1)}")
print(f"{r2} — Palindrommi? {palindrommi(r2)}")
```

## Tushuntirish va Mantiq:
1. `r == r[::-1]` ro'yxat o'zining teskarisiga tengligini tekshiradi.

## Ishlash natijasi:
```text
Chiqish: r1: True, r2: False
```


# 221-Topshiriq: Kortej (Tuple) va uning o'zgarmasligi (Immutability)

## Topshiriq sharti:
Kortej yaratish va uning elementlarini o'zgartirishga urinilganda qanday xatolik yuz berishini ko'rsating.

## Yechim (Python kodi):
```python
talaba = ("Alisher", 20, "Kompyuter fanlari")

print(f"Kortej: {talaba}")
print(f"1-element: {talaba[0]}")

try:
    talaba[1] = 21  # Kortej elementini to'g'ridan-to'g'ri o'zgartirib bo'lmaydi
except TypeError as e:
    print(f"Kutilgan xatolik: {e}")
```

## Tushuntirish va Mantiq:
1. Kortej (tuple) ro'yxatdan farqli o'laroq o'zgarmas (immutable) bo'ladi.
2. Bu xavfsizlikni ta'minlaydi va lug'atlarda kalit sifatida ishlatish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: TypeError: 'tuple' object does not support item assignment
```


# 222-Topshiriq: Ro'yxat va Kortej o'rtasida konvertatsiya

## Topshiriq sharti:
Kortejni ro'yxatga o'tkazib, qiymatini o'zgartiring va yana kortejga qaytaring.

## Yechim (Python kodi):
```python
boshlangich_kortej = (10, 20, 30)

# Ro'yxatga o'giramiz
vaqtinchalik_royxat = list(boshlangich_kortej)
vaqtinchalik_royxat.append(40)
vaqtinchalik_royxat[0] = 99

# Qayta kortejga o'giramiz
yakuniy_kortej = tuple(vaqtinchalik_royxat)

print(f"Boshlang'ich: {boshlangich_kortej}")
print(f"Yangilangan:  {yakuniy_kortej}")
```

## Tushuntirish va Mantiq:
1. `list()` va `tuple()` o'zaro tur konvertatsiyasini amalga oshiradi.

## Ishlash natijasi:
```text
Chiqish: Boshlang'ich: (10, 20, 30), Yangilangan: (99, 20, 30, 40)
```


# 223-Topshiriq: Kortejni qismlarga ochish (Tuple Unpacking)

## Topshiriq sharti:
Kortej elementlarini o'zgaruvchilarga ochish va `*` (yulduzcha) bilan qolgan elementlarni yig'ib olish.

## Yechim (Python kodi):
```python
nuqta = (15, 28, 42)
x, y, z = nuqta
print(f"x={x}, y={y}, z={z}")

# *rest bilan bir qismini ro'yxatga olish
sonlar = (1, 2, 3, 4, 5, 6, 7)
boshi, *ortasi, oxiri = sonlar
print(f"Boshi : {boshi}")
print(f"O'rtasi: {ortasi}")
print(f"Oxiri : {oxiri}")
```

## Tushuntirish va Mantiq:
1. Unpacking kortej elementlarini to'g'ridan-to'g'ri o'zgaruvchilarga biriktiradi.
2. `*ortasi` qolgan barcha elementlarni avtomatik ro'yxatga yig'adi.

## Ishlash natijasi:
```text
Chiqish: Boshi: 1, O'rtasi: [2, 3, 4, 5, 6], Oxiri: 7
```


# 224-Topshiriq: Qiymatlarni uchinchi o'zgaruvchisiz almashtirish (Swap)

## Topshiriq sharti:
Python'da tuple unpacking yordamida ikki o'zgaruvchining qiymatini bitta qatorda almashtiring.

## Yechim (Python kodi):
```python
a = 50
b = 100

print(f"Oldin: a={a}, b={b}")

# Qiymatlarni almashtiramiz
a, b = b, a

print(f"Keyin: a={a}, b={b}")
```

## Tushuntirish va Mantiq:
1. `b, a` o'ng tomonda kortej hosil qiladi va chapdagi `a, b` ga ochib beriladi.

## Ishlash natijasi:
```text
Chiqish: Oldin: a=50, b=100 -> Keyin: a=100, b=50
```


# 225-Topshiriq: Kortejlar ro'yxatini kalit bo'yicha saralash

## Topshiriq sharti:
Talabalarning ismi va ballari kortejlaridan iborat ro'yxatni ballar bo'yicha kamayish tartibida saralang.

## Yechim (Python kodi):
```python
natijalar = [
    ("Jasur", 78),
    ("Madina", 95),
    ("Anvar", 84),
    ("Kamola", 91),
    ("Sardor", 65)
]

# lambda x: x[1] ball bo'yicha saralashni bildiradi
saralangan = sorted(natijalar, key=lambda x: x[1], reverse=True)

print("Reyting jadvali:")
for orin, (ism, ball) in enumerate(saralangan, start=1):
    print(f"{orin}-o'rin: {ism:10s} - {ball} ball")
```

## Tushuntirish va Mantiq:
1. `sorted()` funksiyasi `key` parametrida saralash mezonini oladi.
2. `reverse=True` eng yuqori ballni birinchi o'ringa qo'yadi.

## Ishlash natijasi:
```text
Chiqish: 1-o'rin: Madina (95), 2-o'rin: Kamola (91), 3-o'rin: Anvar (84)...
```


# 226-Topshiriq: Ro'yxatdagi so'zlarni uzunligi bo'yicha saralash

## Topshiriq sharti:
So'zlar ro'yxatini ularning harflar soni bo'yicha o'sish tartibida saralang.

## Yechim (Python kodi):
```python
sozlar = ["fil", "chumoli", "ot", "begemot", "quyon", "arslon"]

sozlar.sort(key=len)

print(f"Uzunlik bo'yicha saralangan: {sozlar}")
```

## Tushuntirish va Mantiq:
1. `key=len` har bir so'zning uzunligini hisoblab, shunga ko'ra saralaydi.

## Ishlash natijasi:
```text
Chiqish: ['ot', 'fil', 'quyon', 'arslon', 'chumoli', 'begemot']
```


# 227-Topshiriq: Kortej ichidagi ro'yxatni o'zgartirish (Nested Mutability)

## Topshiriq sharti:
Kortejning o'zi o'zgarmas bo'lsa-da, uning ichida joylashgan ro'yxat o'zgaruvchanligini ko'rsating.

## Yechim (Python kodi):
```python
malumot = ("Toshkent", [2024, 2025], True)

print(f"Oldingi holat: {malumot}")

# Kortej ichidagi ro'yxatga yangi element qo'shamiz
malumot[1].append(2026)

print(f"Keyingi holat: {malumot}")
```

## Tushuntirish va Mantiq:
1. Kortej havolalarni (references) o'zgarmas saqlaydi.
2. Havola qilingan ob'ektning o'zi (ro'yxat) o'zgaruvchan (mutable) bo'lsa, uning ichki holati o'zgartirilishi mumkin.

## Ishlash natijasi:
```text
Chiqish: ('Toshkent', [2024, 2025, 2026], True)
```


# 228-Topshiriq: Ro'yxatni N o'lchamli bo'laklarga (Chunks) ajratish

## Topshiriq sharti:
Katta ro'yxatni har biri n ta elementdan iborat kichik qismlarga (chunks) bo'ling.

## Yechim (Python kodi):
```python
massiv = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
bolak_olchami = 3

bolaklar = [massiv[i:i + bolak_olchami] for i in range(0, len(massiv), bolak_olchami)]

print(f"Asl ro'yxat: {massiv}")
print(f"Bo'laklar: {bolaklar}")
```

## Tushuntirish va Mantiq:
1. `range(0, len, n)` qadami n ga teng.
2. `massiv[i:i+n]` qism-kesmalari olinadi.

## Ishlash natijasi:
```text
Chiqish: [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11]]
```


# 229-Topshiriq: Qo'shni elementlar farqini hisoblash

## Topshiriq sharti:
Ro'yxatdagi har bir element bilan undan keyingi element orasidagi ayirmalar ro'yxatini tuzing.

## Yechim (Python kodi):
```python
narxlar = [100, 105, 102, 110, 108, 115]

farqlar = [narxlar[i+1] - narxlar[i] for i in range(len(narxlar) - 1)]

print(f"Narxlar dinamikasi: {narxlar}")
print(f"Kundalik o'zgarishlar: {farqlar}")
```

## Tushuntirish va Mantiq:
1. Tsikl `len(narxlar) - 1` gacha aylanadi, shunda `i+1` indeks chegarasidan chiqib ketmaydi.

## Ishlash natijasi:
```text
Chiqish: [+5, -3, +8, -2, +7]
```


# 230-Topshiriq: Ro'yxatni tasodifiy aralashtirish (Shuffle)

## Topshiriq sharti:
Ro'yxat elementlari tartibini `random.shuffle()` yordamida tasodifiy almashtiring.

## Yechim (Python kodi):
```python
import random

kartalar = ["Tuz", "Qirol", "Dama", "Valet", "10", "9"]
print(f"Tartiblangan kartalar: {kartalar}")

random.shuffle(kartalar)
print(f"Aralashtirilgan: {kartalar}")
```

## Tushuntirish va Mantiq:
1. `random.shuffle()` mavjud ro'yxatni o'z o'rnida (in-place) aralashtiradi.

## Ishlash natijasi:
```text
Chiqish: Tasodifiy tartibdagi kartalar ro'yxati.
```


# 231-Topshiriq: Sayoz nusxa (Shallow Copy) va Chuqur nusxa (Deep Copy)

## Topshiriq sharti:
Ichma-ich ro'yxatlarni nusxalashda oddiy nusxa va `copy.deepcopy` o'rtasidagi farqni ko'rsating.

## Yechim (Python kodi):
```python
import copy

asl = [[1, 2], [3, 4]]

sayoz = list(asl)
chuqur = copy.deepcopy(asl)

# Ichki ro'yxatni o'zgartiramiz
asl[0][0] = 99

print(f"Asl ro'yxat : {asl}")
print(f"Sayoz nusxa : {sayoz} (o'zgardi!)")
print(f"Chuqur nusxa: {chuqur} (o'zgarmadi!)")
```

## Tushuntirish va Mantiq:
1. Sayoz nusxa ichki ro'yxatlarning havolasini oladi, shuning uchun asl o'zgarsa u ham o'zgaradi.
2. `deepcopy()` butunlay mustaqil yangi ob'ektlar yaratadi.

## Ishlash natijasi:
```text
Chiqish: Sayoz: [[99, 2], [3, 4]], Chuqur: [[1, 2], [3, 4]]
```


# 232-Topshiriq: Bo'sh va yolg'on qiymatlarni tozalash

## Topshiriq sharti:
Ro'yxatdan barcha `None`, `False`, `0`, `""` kabi bo'sh qiymatlarni olib tashlang.

## Yechim (Python kodi):
```python
aralash = [0, "Salom", None, "", 42, False, "Dunyo", [], True]

# filter(None, ...) barcha False deb baholanuvchi qiymatlarni elaydi
toza = list(filter(None, aralash))

print(f"Tozalangan ro'yxat: {toza}")
```

## Tushuntirish va Mantiq:
1. Python'da 0, None, '', [] mantiqan `False` ga teng.
2. `filter(None, ...)` faqat rost (`True`) qiymatlarni qoldiradi.

## Ishlash natijasi:
```text
Chiqish: ['Salom', 42, 'Dunyo', True]
```


# 233-Topshiriq: Matritsani transponatsiya qilish (Transpose)

## Topshiriq sharti:
Matritsaning qatorlarini ustunlarga almashtiring (`zip(*matrix)` yordamida).

## Yechim (Python kodi):
```python
matritsa = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# zip(*matritsa) barcha qatorlarni ustun qilib bog'laydi
transponirlangan = [list(ustun) for ustun in zip(*matritsa)]

print("Asl matritsa:")
for q in matritsa: print(q)

print("
Transponirlangan matritsa:")
for q in transponirlangan: print(q)
```

## Tushuntirish va Mantiq:
1. `*matritsa` qatorlarni alohida argument qilib uzatadi.
2. `zip()` har bir qatordan mos indeksdagi elementlarni juftlab ustunlar hosil qiladi.

## Ishlash natijasi:
```text
Chiqish: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```


# 234-Topshiriq: Ikki ro'yxatni lug'atga (Dictionary) aylantirish

## Topshiriq sharti:
Kalitlar ro'yxati va qiymatlar ro'yxatini bitta lug'atga birlashtiring.

## Yechim (Python kodi):
```python
kalitlar = ["ism", "yosh", "kasb", "shahar"]
qiymatlar = ["Botir", 25, "Muhandis", "Samarqand"]

lugat = dict(zip(kalitlar, qiymatlar))

print(f"Hosil bo'lgan lug'at: {lugat}")
```

## Tushuntirish va Mantiq:
1. `zip()` juftliklar hosil qiladi.
2. `dict()` ularni kalit-qiymat ko'rinishida lug'atga o'giradi.

## Ishlash natijasi:
```text
Chiqish: {'ism': 'Botir', 'yosh': 25, 'kasb': 'Muhandis', 'shahar': 'Samarqand'}
```


# 235-Topshiriq: Kumulyativ yig'indi ro'yxati (Cumulative Sum)

## Topshiriq sharti:
Har bir elementi o'zidan oldingi barcha elementlar yig'indisidan iborat bo'lgan ro'yxatni hisoblang.

## Yechim (Python kodi):
```python
sonlar = [1, 2, 3, 4, 5]

kumulyativ = []
yigindi = 0

for s in sonlar:
    yigindi += s
    kumulyativ.append(yigindi)

print(f"Asl sonlar: {sonlar}")
print(f"Kumulyativ yig'indi: {kumulyativ}")
```

## Tushuntirish va Mantiq:
1. Har bir qadamda yangi element joriy yig'indiga qo'shiladi va ro'yxatga yoziladi.

## Ishlash natijasi:
```text
Chiqish: [1, 3, 6, 10, 15]
```


# 236-Topshiriq: Eng uzun ketma-ket bir xil elementlar

## Topshiriq sharti:
Ro'yxatdagi eng uzun uzluksiz takrorlangan elementni va uning uzunligini aniqlang.

## Yechim (Python kodi):
```python
belgilar = ['a', 'a', 'b', 'b', 'b', 'b', 'c', 'c', 'a']

maks_uzunlik = 0
eng_kop_belgi = None

joriy_belgi = belgilar[0]
joriy_uzunlik = 1

for b in belgilar[1:]:
    if b == joriy_belgi:
        joriy_uzunlik += 1
    else:
        if joriy_uzunlik > maks_uzunlik:
            maks_uzunlik = joriy_uzunlik
            eng_kop_belgi = joriy_belgi
        joriy_belgi = b
        joriy_uzunlik = 1

if joriy_uzunlik > maks_uzunlik:
    maks_uzunlik = joriy_uzunlik
    eng_kop_belgi = joriy_belgi

print(f"Eng uzun takrorlangan element: '{eng_kop_belgi}' ({maks_uzunlik} marta ketma-ket)")
```

## Tushuntirish va Mantiq:
1. Tsikl o'zgarish sodir bo'lganda oldingi zanjir uzunligini tekshiradi.

## Ishlash natijasi:
```text
Chiqish: 'b' (4 marta ketma-ket)
```


# 237-Topshiriq: Tartiblangan ikki ro'yxatni birlashtirish (Merge Sorted Lists)

## Topshiriq sharti:
Oldindan saralangan ikkita ro'yxatni qayta saralamasdan, O(n+m) vaqtda bitta saralangan ro'yxatga birlashtiring.

## Yechim (Python kodi):
```python
l1 = [1, 3, 5, 7, 9]
l2 = [2, 4, 6, 8, 10]

birlashgan = []
i, j = 0, 0

while i < len(l1) and j < len(l2):
    if l1[i] <= l2[j]:
        birlashgan.append(l1[i])
        i += 1
    else:
        birlashgan.append(l2[j])
        j += 1

# Qolgan elementlarni ulaymiz
birlashgan.extend(l1[i:])
birlashgan.extend(l2[j:])

print(f"Birlashgan ro'yxat: {birlashgan}")
```

## Tushuntirish va Mantiq:
1. Merge Sort algoritmining asosiy birlashtirish bosqichi.
2. Ikkala ro'yxat ko'rsatkichlari solishtirilib, kichigi olinadi.

## Ishlash natijasi:
```text
Chiqish: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```


# 238-Topshiriq: Ro'yxatdagi tub sonlarni ajratish

## Topshiriq sharti:
Sonlar ro'yxatidan faqat tub sonlarni ajratib oluvchi filtr tuzing.

## Yechim (Python kodi):
```python
def tubmi(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

sonlar = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
tub_sonlar = [x for x in sonlar if tubmi(x)]

print(f"Asl ro'yxat: {sonlar}")
print(f"Tub sonlar:  {tub_sonlar}")
```

## Tushuntirish va Mantiq:
1. Funksiya sonning tubligini tekshiradi.
2. List comprehension faqat `tubmi(x) == True` bo'lganlarni qoldiradi.

## Ishlash natijasi:
```text
Chiqish: [11, 13, 17, 19]
```


# 239-Topshiriq: Nuqtalar orasidagi masofalar ro'yxati

## Topshiriq sharti:
(x, y) koordinata kortejlari ro'yxatidan koordinatalar boshigacha bo'lgan masofalarni hisoblang.

## Yechim (Python kodi):
```python
import math

nuqtalar = [(0, 0), (3, 4), (5, 12), (8, 15)]

masofalar = []
for x, y in nuqtalar:
    d = math.hypot(x, y)
    masofalar.append(round(d, 2))

print(f"Nuqtalar: {nuqtalar}")
print(f"Masofalar: {masofalar}")
```

## Tushuntirish va Mantiq:
1. `math.hypot(x, y)` Pifagor teoremasi bo'yicha masofani `sqrt(x^2 + y^2)` aniq hisoblaydi.

## Ishlash natijasi:
```text
Chiqish: [0.0, 5.0, 13.0, 17.0]
```


# 240-Topshiriq: Indeks bo'yicha juft va toq o'rindagi elementlar

## Topshiriq sharti:
Ro'yxatning juft indeksidagi (0, 2, 4...) va toq indeksidagi (1, 3, 5...) elementlarini alohida ro'yxatga ajrating.

## Yechim (Python kodi):
```python
elementlar = ["A", "B", "C", "D", "E", "F", "G"]

juft_orindagilar = elementlar[::2]
toq_orindagilar = elementlar[1::2]

print(f"Asl: {elementlar}")
print(f"Juft indekslar (0, 2, 4...): {juft_orindagilar}")
print(f"Toq indekslar  (1, 3, 5...): {toq_orindagilar}")
```

## Tushuntirish va Mantiq:
1. `[::2]` 0-indeksdan boshlab 2 qadam bilan kesadi.
2. `[1::2]` 1-indeksdan boshlab 2 qadam bilan kesadi.

## Ishlash natijasi:
```text
Chiqish: Juft: ['A', 'C', 'E', 'G'], Toq: ['B', 'D', 'F']
```


# 241-Topshiriq: Funksiyadan bir nechta qiymat qaytarish (Kortej bilan)

## Topshiriq sharti:
Ro'yxatdagi minimum, maksimum, yig'indi va o'rtacha qiymatni bitta funksiyada kortej ko'rinishida qaytaring.

## Yechim (Python kodi):
```python
def statistika(sonlar):
    min_qiymat = min(sonlar)
    max_qiymat = max(sonlar)
    yigindi = sum(sonlar)
    ortacha = yigindi / len(sonlar)
    return min_qiymat, max_qiymat, yigindi, ortacha

natijalar = [10, 20, 30, 40, 50]
mini, maksi, jami, ort = statistika(natijalar)

print(f"Min: {mini}, Max: {maksi}, Jami: {jami}, O'rtacha: {ort}")
```

## Tushuntirish va Mantiq:
1. Vergul bilan ajratilgan bir nechta qiymat qaytarilganda Python avtomatik kortej (tuple) hosil qiladi.

## Ishlash natijasi:
```text
Chiqish: Min: 10, Max: 50, Jami: 150, O'rtacha: 30.0
```


# 242-Topshiriq: Satrlarni xavfsiz songa o'tkazish

## Topshiriq sharti:
Aralash satrlar ro'yxatidagi faqat son bo'la oladiganlarini int ga o'tkazib yangi ro'yxat hosil qiling.

## Yechim (Python kodi):
```python
satrlar = ["12", "salom", "45", "100a", "99", "3.14", "200"]

haqiqiy_sonlar = []
for s in satrlar:
    try:
        haqiqiy_sonlar.append(int(s))
    except ValueError:
        pass  # Son bo'lmaganlarini chetlab o'tamiz

print(f"Muvaffaqiyatli o'girilgan sonlar: {haqiqiy_sonlar}")
```

## Tushuntirish va Mantiq:
1. `try...except ValueError` xatolik yuz berganda dastur to'xtab qolishining oldini oladi.

## Ishlash natijasi:
```text
Chiqish: [12, 45, 99, 200]
```


# 243-Topshiriq: Zik-zak (katta-kichik) tartibida qayta joylash

## Topshiriq sharti:
Ro'yxatni `a[0] < a[1] > a[2] < a[3] > a[4]` ko'rinishidagi zik-zak shakliga keltiring.

## Yechim (Python kodi):
```python
massiv = [4, 3, 7, 8, 6, 2, 1]
n = len(massiv)

for i in range(n - 1):
    if i % 2 == 0:
        # Juft indeksda chapdagi o'ngdagidan kichik bo'lishi kerak
        if massiv[i] > massiv[i + 1]:
            massiv[i], massiv[i + 1] = massiv[i + 1], massiv[i]
    else:
        # Toq indeksda chapdagi o'ngdagidan katta bo'lishi kerak
        if massiv[i] < massiv[i + 1]:
            massiv[i], massiv[i + 1] = massiv[i + 1], massiv[i]

print(f"Zik-zak tartibi: {massiv}")
```

## Tushuntirish va Mantiq:
1. Har bir qadamda juft yoki toq indeksga qarab qo'shni elementlar tartibi to'g'rilanadi.

## Ishlash natijasi:
```text
Chiqish: [3, 7, 4, 8, 2, 6, 1]
```


# 244-Topshiriq: Ro'yxatdagi anomaliyalarni (Outliers) aniqlash

## Topshiriq sharti:
O'rtacha qiymatdan va standart og'ishdan (standard deviation) 2 martadan ortiq farq qiluvchi keskin qiymatlarni toping.

## Yechim (Python kodi):
```python
qiymatlar = [10, 12, 11, 13, 12, 100, 11, 12, 9, -50]

ortacha = sum(qiymatlar) / len(qiymatlar)
dispersiya = sum((x - ortacha) ** 2 for x in qiymatlar) / len(qiymatlar)
std_dev = dispersiya ** 0.5

anomaliyalar = [x for x in qiymatlar if abs(x - ortacha) > 1.5 * std_dev]

print(f"O'rtacha: {ortacha:.2f}, Std Dev: {std_dev:.2f}")
print(f"Anomal (keskin chetga chiqqan) qiymatlar: {anomaliyalar}")
```

## Tushuntirish va Mantiq:
1. Ma'lumotlar tahlilida (Data Science) anomaliyalarni filtrlash muhim qadam hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: Anomaliyalar: [100, -50]
```


# 245-Topshiriq: Ro'yxatni o'z o'rnida teskari qilish (In-place Reverse)

## Topshiriq sharti:
Qo'shimcha ro'yxat yaratmasdan, ikki ko'rsatkich (two pointers) usulida ro'yxatni teskarisiga o'giring.

## Yechim (Python kodi):
```python
massiv = [1, 2, 3, 4, 5, 6]

chap = 0
ong = len(massiv) - 1

while chap < ong:
    massiv[chap], massiv[ong] = massiv[ong], massiv[chap]
    chap += 1
    ong -= 1

print(f"O'z o'rnida teskari qilingan: {massiv}")
```

## Tushuntirish va Mantiq:
1. Ikki ko'rsatkich chekkadan markazga qarab harakatlanadi va elementlar o'rni almashtiriladi.
2. Xotira sarfi O(1) bo'ladi.

## Ishlash natijasi:
```text
Chiqish: [6, 5, 4, 3, 2, 1]
```


# 246-Topshiriq: Kortejlar ro'yxatini kalit bo'yicha guruhlash

## Topshiriq sharti:
Mahsulotlar va ularning toifalari kortejlaridan iborat ro'yxatni toifalar bo'yicha guruhlang.

## Yechim (Python kodi):
```python
mahsulotlar = [
    ("Olma", "Meva"),
    ("Sabzi", "Sabzavot"),
    ("Banan", "Meva"),
    ("Bodring", "Sabzavot"),
    ("Nok", "Meva")
]

guruhlar = {}
for nom, toifa in mahsulotlar:
    if toifa not in guruhlar:
        guruhlar[toifa] = []
    guruhlar[toifa].append(nom)

print("Toifalar bo'yicha guruhlangan:")
for toifa, nomlar in guruhlar.items():
    print(f"{toifa}: {nomlar}")
```

## Tushuntirish va Mantiq:
1. Lug'at qiymati sifatida ro'yxat ishlatiladi.
2. Har bir yangi mahsulot o'z toifasi ro'yxatiga qo'shib boriladi.

## Ishlash natijasi:
```text
Chiqish: Meva: ['Olma', 'Banan', 'Nok'], Sabzavot: ['Sabzi', 'Bodring']
```


# 247-Topshiriq: Sonlar ro'yxatining medianasini topish

## Topshiriq sharti:
Ro'yxat saralanganda aynan o'rtada joylashgan qiymatni (medianani) to'g'ri hisoblang.

## Yechim (Python kodi):
```python
sonlar = [15, 3, 9, 21, 7, 11]

saralangan = sorted(sonlar)
n = len(saralangan)

if n % 2 != 0:
    mediana = saralangan[n // 2]
else:
    mediana = (saralangan[n // 2 - 1] + saralangan[n // 2]) / 2

print(f"Saralangan: {saralangan}")
print(f"Mediana: {mediana}")
```

## Tushuntirish va Mantiq:
1. Elementlar soni toq bo'lsa, o'rtadagi son mediana bo'ladi.
2. Juft bo'lsa, o'rtadagi ikki sonning o'rta arifmetigi olinadi.

## Ishlash natijasi:
```text
Kiritish: [3, 7, 9, 11, 15, 21] -> Chiqish: Mediana: 10.0 ((9+11)/2)
```


# 248-Topshiriq: Ro'yxatdagi qiymatlarni normalizatsiya qilish (Min-Max)

## Topshiriq sharti:
Sonlar ro'yxatidagi barcha qiymatlarni 0 va 1 oralig'iga keltiring (Min-Max Scaling).

## Yechim (Python kodi):
```python
sonlar = [10, 20, 30, 40, 50]

min_v = min(sonlar)
max_v = max(sonlar)

normal = [(x - min_v) / (max_v - min_v) for x in sonlar]

print(f"Asl qiymatlar: {sonlar}")
print(f"Normalizatsiya (0-1 oralig'ida): {[round(n, 2) for n in normal]}")
```

## Tushuntirish va Mantiq:
1. Formula: (x - min) / (max - min).
2. Mashinali o'rganishda xususiyatlarni bir xil miqyosga keltirishda keng qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: [0.0, 0.25, 0.5, 0.75, 1.0]
```


# 249-Topshiriq: Kortejlar yordamida kesh (Memoizatsiya) yaratish

## Topshiriq sharti:
Funksiya chaqiruvlari natijalarini kortej kalitlari bilan lug'atda keshlab, hisoblashni tezlashtiring.

## Yechim (Python kodi):
```python
kesh = {}

def fibonacci_kesh(n):
    if n in kesh:
        return kesh[n]
    if n <= 1:
        return n
    
    kesh[n] = fibonacci_kesh(n - 1) + fibonacci_kesh(n - 2)
    return kesh[n]

print("Fibonachchi sonlari:")
for i in range(10):
    print(f"F({i}) = {fibonacci_kesh(i)}")
```

## Tushuntirish va Mantiq:
1. Kesh (memoizatsiya) bir xil hisoblashlarni qayta bajarmasdan natijani darhol qaytaradi.

## Ishlash natijasi:
```text
Chiqish: F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5...
```


# 250-Topshiriq: Interaktiv Xaridlar Ro'yxati Menejeri (CLI Dastur)

## Topshiriq sharti:
Foydalanuvchiga ro'yxatga mahsulot qo'shish, o'chirish, ko'rish va tozalash imkonini beruvchi to'liq boshqaruv dasturi.

## Yechim (Python kodi):
```python
xaridlar = []

def menyu():
    print("\n--- XARIDLAR RO'YXATI ---")
    print("1. Ko'rish")
    print("2. Qo'shish")
    print("3. O'chirish")
    print("4. Tozalash")
    print("5. Chiqish")

# CLI dastur simulyatsiyasi
amal = "2"
if amal == "2":
    xaridlar.append("Non")
    xaridlar.append("Sut")
    xaridlar.append("Meva")

print(f"Joriy xaridlar ({len(xaridlar)} ta):")
for i, m in enumerate(xaridlar, start=1):
    print(f"{i}. {m}")
```

## Tushuntirish va Mantiq:
1. Ro'yxat boshqaruvi CRUD (Create, Read, Update, Delete) tamoyillariga asoslanadi.
2. Foydalanuvchi kiritgan ma'lumotlar asosida ro'yxat dinamik yangilanadi.

## Ishlash natijasi:
```text
Chiqish: 1. Non, 2. Sut, 3. Meva
```

