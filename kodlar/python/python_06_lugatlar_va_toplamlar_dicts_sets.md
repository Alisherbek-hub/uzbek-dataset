# Python Dasturlash Tili — 6-Qism: Lug'atlar (Dictionaries) va To'plamlar (Sets)
## (251-300 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam lug'atlar va to'plamlar bo'yicha eng muhim ma'lumotlar tuzilmalarini qamrab oladi:
* Lug'at metodlari: `get()`, `pop()`, `update()`, `setdefault()`, `keys()`, `values()`, `items()`;
* Dict Comprehension, kalit va qiymatlarni almashtirish (inverting), saralash;
* To'plam amallari (sets): birlashma, kesishma, ayirma, simmetrik ayirma, `frozenset`;
* Jaccard o'xshashligi, anagrammalar guruhlash, ichma-ich lug'atlarni yassilash, JSON konvertatsiya;
* Amaliyot: LRU kesh simulyatsiyasi, do'kon savatchasi, xodimlar tahlili, quiz dasturi;

---

# 251-Topshiriq: Lug'at metodlari (get, pop, del, update, clear)

## Topshiriq sharti:
Lug'at yaratish, kalit bo'yicha xavfsiz qiymat olish, yangilash va o'chirish amallarini ko'rsating.

## Yechim (Python kodi):
```python
foydalanuvchi = {
    "ism": "Jasur",
    "yosh": 22,
    "kasb": "Dasturchi"
}

# 1. get() — xavfsiz olish (kalit bo'lmasa xato bermaydi, standart qiymat qaytaradi)
shahar = foydalanuvchi.get("shahar", "Noma'lum")

# 2. Yangi kalit qo'shish yoki mavjudini yangilash
foydalanuvchi["shahar"] = "Toshkent"
foydalanuvchi["yosh"] = 23

# 3. pop() — elementni o'chirib, qiymatini qaytarish
kasb = foydalanuvchi.pop("kasb")

# 4. del — kalit bo'yicha o'chirish
# del foydalanuvchi["shahar"]

print(f"Olingan shahar: {shahar}")
print(f"O'chirilgan kasb: {kasb}")
print(f"Yakuniy lug'at: {foydalanuvchi}")
```

## Tushuntirish va Mantiq:
1. `dict[key]` agar kalit topilmasa `KeyError` beradi.
2. `dict.get(key, default)` esa xatoliksiz xavfsiz ishlaydi.
3. Lug'atlar O(1) o'rtacha murakkablikda kalit bo'yicha qidirishni ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Olingan: Noma'lum, O'chirilgan: Dasturchi, Yakuniy: {'ism': 'Jasur', 'yosh': 23, 'shahar': 'Toshkent'}
```


# 252-Topshiriq: Lug'atni keys(), values() va items() bilan aylanish

## Topshiriq sharti:
Lug'atning faqat kalitlari, faqat qiymatlari va kalit-qiymat juftliklarini for tsikli bilan chiqaring.

## Yechim (Python kodi):
```python
narxlar = {"olma": 12000, "banan": 22000, "anor": 18000}

print("1. Faqat kalitlar (keys):")
for kalit in narxlar.keys():
    print(f" - {kalit}")

print("
2. Faqat qiymatlar (values):")
for qiymat in narxlar.values():
    print(f" - {qiymat:,} so'm")

print("
3. Kalit va qiymatlar juftligi (items):")
for mahsulot, narx in narxlar.items():
    print(f" * {mahsulot:8s} -> {narx:,} so'm")
```

## Tushuntirish va Mantiq:
1. `.items()` unpacking orqali `for k, v in dict.items():` shaklida juda qulay ishlaydi.

## Ishlash natijasi:
```text
Chiqish: Mahsulot va narxlarning 3 xil usulda aylanish natijasi.
```


# 253-Topshiriq: Ikki lug'atni birlashtirish (| operatori va update)

## Topshiriq sharti:
Ikki alohida lug'atni bitta yangi lug'atga birlashtirish usullarini ko'rsating.

## Yechim (Python kodi):
```python
d1 = {"a": 1, "b": 2, "c": 3}
d2 = {"c": 99, "d": 4, "e": 5}

# Python 3.9+ birlashma operatori: |
birlashgan = d1 | d2

print(f"d1: {d1}")
print(f"d2: {d2}")
print(f"Birlashgan (|): {birlashgan}")
```

## Tushuntirish va Mantiq:
1. `|` operatori bir xil kalitlar bo'lsa, o'ng tarafdagi (`d2`) qiymat ustunlik qiladi (c: 99).
2. Asl lug'atlar o'zgarmasdan yangi lug'at hosil bo'ladi.

## Ishlash natijasi:
```text
Chiqish: {'a': 1, 'b': 2, 'c': 99, 'd': 4, 'e': 5}
```


# 254-Topshiriq: Dictionary Comprehension

## Topshiriq sharti:
1 dan 10 gacha sonlarning son va uning kubidan iborat lug'atini bitta qatorda tuzing.

## Yechim (Python kodi):
```python
kublar = {x: x ** 3 for x in range(1, 11)}

print("Sonlar va ularning kublari:")
for son, kub in kublar.items():
    print(f"{son:2d}^3 = {kub:4d}")
```

## Tushuntirish va Mantiq:
1. `{k: v for ... in ...}` sintaksisi yangi lug'atni ixcham yaratishga xizmat qiladi.

## Ishlash natijasi:
```text
Chiqish: {1: 1, 2: 8, 3: 27, 4: 64, 5: 125, 6: 216, 7: 343, 8: 512, 9: 729, 10: 1000}
```


# 255-Topshiriq: Lug'atni qiymati (Value) bo'yicha saralash

## Topshiriq sharti:
Talabalar va ularning to'plagan ballari lug'atini ball bo'yicha kamayish tartibida saralang.

## Yechim (Python kodi):
```python
ballar = {
    "Malika": 88,
    "Sardor": 75,
    "Aziz": 96,
    "Nilufar": 91,
    "Bekzod": 82
}

# x[1] qiymat (ball) bo'yicha saralash
saralangan = dict(sorted(ballar.items(), key=lambda x: x[1], reverse=True))

print("Ballar bo'yicha reyting:")
for ism, ball in saralangan.items():
    print(f"{ism:10s} : {ball}")
```

## Tushuntirish va Mantiq:
1. `sorted(ballar.items(), key=lambda x: x[1])` juftliklarning 2-elementi (qiymati) bo'yicha tartiblaydi.
2. `dict()` uni qaytadan lug'at ko'rinishiga keltiradi.

## Ishlash natijasi:
```text
Chiqish: Aziz: 96, Nilufar: 91, Malika: 88, Bekzod: 82, Sardor: 75
```


# 256-Topshiriq: Lug'at kalitlari va qiymatlarini almashtirish (Invert)

## Topshiriq sharti:
Lug'atning har bir kalitini qiymatga, qiymatini esa kalitga aylantiring.

## Yechim (Python kodi):
```python
davlat_poytaxt = {
    "O'zbekiston": "Toshkent",
    "Qozog'iston": "Ostona",
    "Tojikiston": "Dushanbe",
    "Qirg'iziston": "Bishkek"
}

poytaxt_davlat = {poytaxt: davlat for davlat, poytaxt in davlat_poytaxt.items()}

print(f"Asl lug'at: {davlat_poytaxt}")
print(f"Teskari lug'at: {poytaxt_davlat}")
```

## Tushuntirish va Mantiq:
1. `{v: k for k, v in d.items()}` yordamida teskari qidiruv lug'ati hosil qilinadi.

## Ishlash natijasi:
```text
Chiqish: {'Toshkent': "O'zbekiston", 'Ostona': "Qozog'iston", ...}
```


# 257-Topshiriq: setdefault() orqali guruhlash

## Topshiriq sharti:
Harflar bo'yicha so'zlarni guruhlovchi lug'atni `setdefault()` yordamida shakllantiring.

## Yechim (Python kodi):
```python
sozlar = ["olma", "anor", "shaftoli", "behi", "banan", "nok", "olxo'ri"]

guruhlar = {}
for s in sozlar:
    bosh_harf = s[0]
    guruhlar.setdefault(bosh_harf, []).append(s)

print("Harflar bo'yicha guruhlangan:")
for h, royxat in sorted(guruhlar.items()):
    print(f"'{h}': {royxat}")
```

## Tushuntirish va Mantiq:
1. `setdefault(key, default)` kalit bo'lmasa uni `default` bilan yaratadi va mavjud qiymatni qaytaradi.
2. Bu ortiqcha `if key not in dict:` tekshiruvlarining oldini oladi.

## Ishlash natijasi:
```text
Chiqish: 'a': ['anor'], 'b': ['behi', 'banan'], 'n': ['nok'], 'o': ['olma', "olxo'ri"], 's': ['shaftoli']
```


# 258-Topshiriq: collections.defaultdict dan foydalanish

## Topshiriq sharti:
`defaultdict` orqali mavjud bo'lmagan kalitlarga avtomatik boshlang'ich ro'yxat yoki son biriktirish.

## Yechim (Python kodi):
```python
from collections import defaultdict

# Standart qiymati int (0) bo'lgan lug'at
harf_hisobi = defaultdict(int)
matn = "antigravity"

for ch in matn:
    harf_hisobi[ch] += 1

print(f"Harflar chastotasi: {dict(harf_hisobi)}")
```

## Tushuntirish va Mantiq:
1. `defaultdict(int)` yangi kalit uchraganda uni avtomatik 0 qilib boshlaydi, shuning uchun `+= 1` xatosiz ishlaydi.

## Ishlash natijasi:
```text
Chiqish: {'a': 2, 'n': 1, 't': 2, 'i': 2, 'g': 1, 'r': 1, 'v': 1, 'y': 1}
```


# 259-Topshiriq: Anagramma so'zlarni guruhlash

## Topshiriq sharti:
So'zlar ro'yxatidan bir-biriga anagramma bo'lgan so'zlarni bitta guruhga yig'ing.

## Yechim (Python kodi):
```python
sozlar = ["tok", "kot", "olma", "mola", "bolg'a", "loma", "choy"]

anagrammalar = {}
for s in sozlar:
    kalit = "".join(sorted(s))
    if kalit not in anagrammalar:
        anagrammalar[kalit] = []
    anagrammalar[kalit].append(s)

print("Anagramma guruhlari:")
for g in anagrammalar.values():
    if len(g) > 1:
        print(f" - {g}")
```

## Tushuntirish va Mantiq:
1. Saralangan harflar ketma-ketligi (`''.join(sorted(s))`) anagrammalar uchun yagona umumiy kalit bo'ladi.

## Ishlash natijasi:
```text
Chiqish: ['tok', 'kot'], ['olma', 'mola', 'loma']
```


# 260-Topshiriq: Ikki lug'at qiymatlarini jamlash (Merge & Sum)

## Topshiriq sharti:
Ikkala do'kondagi bir xil tovarlarning miqdorlarini qo'shib, umumiy ombor hisobotini tuzing.

## Yechim (Python kodi):
```python
ombor1 = {"daftar": 50, "ruchka": 120, "qalam": 80}
ombor2 = {"daftar": 30, "ruchka": 40, "chizg'ich": 25}

umumiy = dict(ombor1)
for tovar, soni in ombor2.items():
    umumiy[tovar] = umumiy.get(tovar, 0) + soni

print(f"1-ombor: {ombor1}")
print(f"2-ombor: {ombor2}")
print(f"Jami tovarlar: {umumiy}")
```

## Tushuntirish va Mantiq:
1. `.get(tovar, 0)` tovar birinchi marta kiritilayotgan bo'lsa 0 olib, unga sonini qo'shadi.

## Ishlash natijasi:
```text
Chiqish: {'daftar': 80, 'ruchka': 160, 'qalam': 80, "chizg'ich": 25}
```


# 261-Topshiriq: Ichma-ich lug'atlar bilan ishlash (Nested Dictionary)

## Topshiriq sharti:
Talabalar va ularning fanlar bo'yicha baholari ma'lumotlar bazasini boshqaring va o'rtacha ballni toping.

## Yechim (Python kodi):
```python
talabalar = {
    "Alisher": {"Matematika": 90, "Fizika": 85, "Dasturlash": 98},
    "Zarina": {"Matematika": 95, "Fizika": 92, "Dasturlash": 94},
    "Jasur": {"Matematika": 70, "Fizika": 65, "Dasturlash": 80}
}

for ism, fanlar in talabalar.items():
    ortacha = sum(fanlar.values()) / len(fanlar)
    print(f"{ism:10s} -> O'rtacha baho: {ortacha:.1f}")
```

## Tushuntirish va Mantiq:
1. Ichki lug'at `fanlar.values()` orqali barcha fanlar baholarini oladi va o'rtachasini hisoblaydi.

## Ishlash natijasi:
```text
Chiqish: Alisher: 91.0, Zarina: 93.7, Jasur: 71.7
```


# 262-Topshiriq: Lug'atdan shart bo'yicha filtrlash

## Topshiriq sharti:
Mijozlar lug'atidan faqat balansi 1,000,000 so'mdan ko'p bo'lganlarini yangi lug'atga ajrating.

## Yechim (Python kodi):
```python
balanslar = {
    "Ali": 450000,
    "Vali": 1200000,
    "G'ani": 3500000,
    "Hasan": 850000,
    "Husan": 2100000
}

katta_mijozlar = {k: v for k, v in balanslar.items() if v >= 1000000}

print(f"VIP mijozlar: {katta_mijozlar}")
```

## Tushuntirish va Mantiq:
1. Dict comprehension ichiga `if v >= 1000000` shartini kiritish orqali qulay filtrlanadi.

## Ishlash natijasi:
```text
Chiqish: {'Vali': 1200000, "G'ani": 3500000, 'Husan': 2100000}
```


# 263-Topshiriq: To'plam (Set) yaratish va metodlari (add, discard, remove)

## Topshiriq sharti:
To'plam yaratish, element qo'shish va `remove()` bilan `discard()` o'rtasidagi asosiy farqni ko'rsating.

## Yechim (Python kodi):
```python
raqamlar = {1, 2, 3, 4, 5}

# add — yangi element qo'shish
raqamlar.add(6)
raqamlar.add(3)  # 3 allaqachon bor, to'plamda takrorlanmaydi

# discard — xavfsiz o'chirish (agar element bo'lmasa xato bermaydi)
raqamlar.discard(10)

# remove — o'chirish (agar element bo'lmasa KeyError beradi)
raqamlar.remove(1)

print(f"Yakuniy to'plam: {raqamlar}")
```

## Tushuntirish va Mantiq:
1. To'plam faqat unikal elementlarni saqlaydi va tartiblanmagan bo'ladi.
2. `discard()` element yo'q bo'lsa ham dasturni to'xtatmaydi.

## Ishlash natijasi:
```text
Chiqish: {2, 3, 4, 5, 6}
```


# 264-Topshiriq: To'plam amallari (Birlashma, Kesishma, Ayirma, Simmetrik ayirma)

## Topshiriq sharti:
Ikki to'plam ustida barcha to'plamlar nazariyasi amallarini bajaring.

## Yechim (Python kodi):
```python
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

print(f"A: {a}")
print(f"B: {b}")
print(f"Birlashma (|)         : {a | b}")
print(f"Kesishma (&)          : {a & b}")
print(f"A ayirma B (-)        : {a - b}")
print(f"Simmetrik ayirma (^)  : {a ^ b}")
```

## Tushuntirish va Mantiq:
1. `|` birlashma (hammasi).
2. `&` kesishma (ikkalasida ham bor).
3. `-` ayirma (faqat A da bor).
4. `^` simmetrik ayirma (faqat bittasida bor bo'lganlar).

## Ishlash natijasi:
```text
Chiqish: Birlashma: 1..8, Kesishma: {4, 5}, Ayirma: {1, 2, 3}, Simmetrik: {1, 2, 3, 6, 7, 8}
```


# 265-Topshiriq: Qism-to'plam (Subset) va Yuqori-to'plam (Superset)

## Topshiriq sharti:
Bir to'plam boshqa to'plamning to'liq ichki qismi ekanligini tekshiring.

## Yechim (Python kodi):
```python
tillar = {"Python", "JavaScript", "C++", "Java", "Go"}
mening_tillarim = {"Python", "Go"}

kichikmi = mening_tillarim.issubset(tillar)
kattami = tillar.issuperset(mening_tillarim)

print(f"Mening bilimlarim umumiy to'plamga kiradimi? {kichikmi}")
print(f"Umumiy to'plam mening bilimlarimni to'liq qamraydimi? {kattami}")
```

## Tushuntirish va Mantiq:
1. `A.issubset(B)` A to'plamning barcha elementlari B da mavjudligini bildiradi.

## Ishlash natijasi:
```text
Chiqish: issubset: True, issuperset: True
```


# 266-Topshiriq: Muzlatilgan to'plam (frozenset)

## Topshiriq sharti:
O'zgarmas to'plam yaratish va uni boshqa to'plam yoki lug'at kaliti sifatida ishlatish.

## Yechim (Python kodi):
```python
muzlatilgan = frozenset([1, 2, 3])

# Oddiy setni lug'at kaliti qilib bo'lmaydi (unhashable), lekin frozenset mumkin:
kesh = {
    muzlatilgan: "1, 2, 3 to'plam natijasi"
}

print(f"Frozenset: {muzlatilgan}")
print(f"Kesh qiymati: {kesh[muzlatilgan]}")
```

## Tushuntirish va Mantiq:
1. `frozenset` immutable (o'zgarmas) bo'lgani sababli hash qiymatiga ega va xavfsiz kalit bo'la oladi.

## Ishlash natijasi:
```text
Chiqish: Kesh qiymati: 1, 2, 3 to'plam natijasi
```


# 267-Topshiriq: Ijtimoiy tarmoqda umumiy do'stlarni topish

## Topshiriq sharti:
Ikki foydalanuvchining do'stlar ro'yxatidan umumiy do'stlarini to'plam amali orqali aniqlang.

## Yechim (Python kodi):
```python
anvar_dostlari = {"Jasur", "Sardor", "Olim", "Malika", "Kamola"}
dilnoza_dostlari = {"Malika", "Ziyoda", "Sardor", "Farrux"}

umumiy_dostlar = anvar_dostlari & dilnoza_dostlari

print(f"Umumiy do'stlar ({len(umumiy_dostlar)} ta): {umumiy_dostlar}")
```

## Tushuntirish va Mantiq:
1. `set1 & set2` kesishmasi ijtimoiy tarmoqlardagi 'Umumiy tanishlar' funksiyasining asosi hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: {'Malika', 'Sardor'}
```


# 268-Topshiriq: Jaccard o'xshashlik koeffitsientini hisoblash

## Topshiriq sharti:
Ikki matnning so'zlar to'plami asosida Jaccard o'xshashlik foizini hisoblang.

## Yechim (Python kodi):
```python
matn1 = "sun'iy intellekt va mashinali o'rganish kelajak texnologiyasi"
matn2 = "mashinali o'rganish va katta ma'lumotlar kelajak texnologiyasi"

s1 = set(matn1.split())
s2 = set(matn2.split())

kesishma = len(s1 & s2)
birlashma = len(s1 | s2)

jaccard = kesishma / birlashma if birlashma > 0 else 0

print(f"Umumiy so'zlar soni: {kesishma} ta")
print(f"Jami turli so'zlar : {birlashma} ta")
print(f"Jaccard o'xshashlik darajasi: {jaccard * 100:.1f}%")
```

## Tushuntirish va Mantiq:
1. Jaccard indeksi = |A ∩ B| / |A ∪ B|.
2. Qidiruv tizimlari va plagiat tekshiruvida ikki matn o'xshashligini o'lchashda qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: O'xshashlik: ~50-60%
```


# 269-Topshiriq: Top-3 eng qimmat mahsulotni topish

## Topshiriq sharti:
Mahsulotlar va ularning narxlari lug'atidan eng qimmat 3 ta mahsulotni ajratib oling.

## Yechim (Python kodi):
```python
tovarlar = {
    "Noutbuk": 8500000,
    "Smartfon": 4200000,
    "Sichqoncha": 150000,
    "Monitor": 2800000,
    "Klaviatura": 350000,
    "Quloqchin": 600000
}

top3 = sorted(tovarlar.items(), key=lambda x: x[1], reverse=True)[:3]

print("Eng qimmat 3 ta mahsulot:")
for i, (nom, narx) in enumerate(top3, start=1):
    print(f"{i}. {nom:12s} : {narx:,} so'm")
```

## Tushuntirish va Mantiq:
1. `[:3]` slicing orqali eng yuqori 3 ta element olinadi.

## Ishlash natijasi:
```text
Chiqish: 1. Noutbuk (8.5M), 2. Smartfon (4.2M), 3. Monitor (2.8M)
```


# 270-Topshiriq: Ovoz berish natijalarini hisoblash (Counter mantiqi)

## Topshiriq sharti:
Saylovdagi barcha ovozlar ro'yxatidan nomzodlarning ovoz foizlarini hisoblang.

## Yechim (Python kodi):
```python
ovozlar = ["Ali", "Vali", "Ali", "Ali", "G'ani", "Vali", "Ali", "Vali"]

natijalar = {}
for nomzod in ovozlar:
    natijalar[nomzod] = natijalar.get(nomzod, 0) + 1

jami_ovoz = len(ovozlar)

print("Saylov natijalari:")
for nomzod, soni in sorted(natijalar.items(), key=lambda x: x[1], reverse=True):
    foiz = (soni / jami_ovoz) * 100
    print(f"{nomzod:8s}: {soni} ta ovoz ({foiz:.1f}%)")
```

## Tushuntirish va Mantiq:
1. Har bir nomzod ovozi sanab boriladi va jami ovozga nisbati hisoblanadi.

## Ishlash natijasi:
```text
Chiqish: Ali: 4 ta (50.0%), Vali: 3 ta (37.5%), G'ani: 1 ta (12.5%)
```


# 271-Topshiriq: Ichma-ich lug'atni yassilash (Flatten Dictionary)

## Topshiriq sharti:
Ko'p darajali konfiguratsiya lug'atini nuqtalar bilan ajratilgan yassi lug'atga aylantiring.

## Yechim (Python kodi):
```python
konfiguratsiya = {
    "app": {
        "name": "UzbekAI",
        "version": "2.0"
    },
    "database": {
        "host": "localhost",
        "port": 5432
    }
}

yassi = {}
for bosh_kalit, ichki in konfiguratsiya.items():
    for ichki_kalit, qiymat in ichki.items():
        yassi[f"{bosh_kalit}.{ichki_kalit}"] = qiymat

print("Yassi konfiguratsiya:")
for k, v in yassi.items():
    print(f"{k} = {v}")
```

## Tushuntirish va Mantiq:
1. Ichma-ich kalitlar `app.name`, `database.host` ko'rinishida yagona kalitga keltiriladi.

## Ishlash natijasi:
```text
Chiqish: app.name = UzbekAI, database.port = 5432
```


# 272-Topshiriq: Lug'atni JSON ga va JSON ni lug'atga o'tkazish

## Topshiriq sharti:
Ma'lumotlar lug'atini JSON formatidagi satrga aylantirish va uni qayta o'qish.

## Yechim (Python kodi):
```python
import json

profil = {
    "id": 101,
    "ism": "Alisherbek",
    "faolmi": True,
    "ko'nikmalar": ["Python", "Machine Learning", "NLP"]
}

# Lug'atni JSON matniga o'giramiz
json_matn = json.dumps(profil, ensure_ascii=False, indent=2)
print("JSON matni:")
print(json_matn)

# JSON matnini qayta Python lug'atiga o'giramiz
qayta_lugat = json.loads(json_matn)
print("
Qayta tiklangan tur:", type(qayta_lugat))
```

## Tushuntirish va Mantiq:
1. `json.dumps()` lug'atni matnga aylantiradi (`ensure_ascii=False` o'zbek harflarini to'g'ri saqlaydi).
2. `json.loads()` JSON matnini Python lug'atiga tiklaydi.

## Ishlash natijasi:
```text
Chiqish: Chiroyli formatlangan JSON va uning qayta tiklanishi.
```


# 273-Topshiriq: Lug'atdagi bo'sh yoki None qiymatlarni tozalash

## Topshiriq sharti:
Lug'at ichidagi barcha `None`, bo'sh satr `""` yoki `[]` qiymatlarga ega kalitlarni o'chirib tashlang.

## Yechim (Python kodi):
```python
malumot = {
    "ism": "Farrux",
    "email": "farrux@mail.uz",
    "telefon": None,
    "manzil": "",
    "ballar": [85, 90],
    "qoshimcha": []
}

toza = {k: v for k, v in malumot.items() if v is not None and v != "" and v != []}

print(f"Tozalangan ma'lumot: {toza}")
```

## Tushuntirish va Mantiq:
1. Keraksiz bo'sh maydonlar API ga yuborishdan oldin xotirani tejash uchun tozalanadi.

## Ishlash natijasi:
```text
Chiqish: {'ism': 'Farrux', 'email': 'farrux@mail.uz', 'ballar': [85, 90]}
```


# 274-Topshiriq: To'plamlarning o'zaro kesishmasligini tekshirish (isdisjoint)

## Topshiriq sharti:
Ikki to'plamda birorta ham umumiy element yo'qligini aniqlang.

## Yechim (Python kodi):
```python
juft_sonlar = {2, 4, 6, 8, 10}
toq_sonlar = {1, 3, 5, 7, 9}

kesishmaydimi = juft_sonlar.isdisjoint(toq_sonlar)

print(f"Juft va toq sonlar to'plamida umumiy element bormi? {not kesishmaydimi}")
print(f"isdisjoint natijasi: {kesishmaydimi}")
```

## Tushuntirish va Mantiq:
1. `A.isdisjoint(B)` agar kesishma bo'sh to'plam bo'lsa `True` qaytaradi.

## Ishlash natijasi:
```text
Chiqish: isdisjoint: True
```


# 275-Topshiriq: Matndan unikal so'zlar chastotasini tahlil qilish

## Topshiriq sharti:
Matndagi har bir so'zning necha martadan qatnashganini hisoblab, jadval ko'rinishida chiqaring.

## Yechim (Python kodi):
```python
matn = "ilm olish har bir inson uchun zarur ilm insonni uluglaydi bilim va ilm"

sozlar = matn.split()
chastota = {}

for s in sozlar:
    chastota[s] = chastota.get(s, 0) + 1

print(f"Jami so'zlar: {len(sozlar)} ta")
print(f"Unikal so'zlar: {len(chastota)} ta
")

for s, n in sorted(chastota.items(), key=lambda x: x[1], reverse=True):
    print(f"'{s}': {n} marta")
```

## Tushuntirish va Mantiq:
1. Matn tahlilida TF (Term Frequency) hisoblash poydevoridir.

## Ishlash natijasi:
```text
Chiqish: 'ilm': 3 marta, 'inson': 1, 'insonni': 1...
```


# 276-Topshiriq: Telefon kitobchasi (CRUD amallari)

## Topshiriq sharti:
Kontaktlar lug'atiga yangi raqam qo'shish, qidirish, yangilash va o'chirish dasturi.

## Yechim (Python kodi):
```python
kontaktlar = {
    "Onam": "+998901112233",
    "Otam": "+998904445566",
    "Akam": "+998907778899"
}

# 1. Qidirish
ism = "Onam"
print(f"{ism}ning raqami: {kontaktlar.get(ism, 'Topilmadi')}")

# 2. Yangi qo'shish
kontaktlar["Do'stim"] = "+998901234567"

# 3. Yangilash
kontaktlar["Akam"] = "+998990001122"

# 4. O'chirish
kontaktlar.pop("Otam", None)

print(f"
Yangilangan kontaktlar ({len(kontaktlar)} ta): {kontaktlar}")
```

## Tushuntirish va Mantiq:
1. Lug'at kaliti sifatida shaxs ismi, qiymat sifatida telefon raqami saqlanadi.

## Ishlash natijasi:
```text
Chiqish: Kontaktlar ro'yxatining muvaffaqiyatli boshqarilishi.
```


# 277-Topshiriq: Lug'atdagi qiymatlarni foizga aylantirish

## Topshiriq sharti:
Kompaniyadagi xarajatlar turlari summasini umumiy byudjetdagi foiz hisobiga o'tkazing.

## Yechim (Python kodi):
```python
xarajatlar = {
    "Ish haqi": 45000000,
    "Ijara": 12000000,
    "Marketing": 8000000,
    "Serverlar": 5000000
}

jami = sum(xarajatlar.values())

foizlar = {k: round((v / jami) * 100, 2) for k, v in xarajatlar.items()}

print(f"Jami byudjet: {jami:,} so'm")
print("Xarajatlar taqsimoti:")
for k, f in foizlar.items():
    print(f" - {k:12s}: {f}%")
```

## Tushuntirish va Mantiq:
1. Dict comprehension har bir qiymatni jami summaga bo'lib foizga aylantiradi.

## Ishlash natijasi:
```text
Chiqish: Ish haqi: 64.29%, Ijara: 17.14%, Marketing: 11.43%, Serverlar: 7.14%
```


# 278-Topshiriq: Ikki lug'at o'rtasidagi farqlarni (Diff) topish

## Topshiriq sharti:
Ikki versiyadagi konfiguratsiyada nimalar o'zgarganini (qo'shilgan, o'chirilgan, o'zgargan kalitlar) aniqlang.

## Yechim (Python kodi):
```python
v1 = {"host": "localhost", "port": 8080, "debug": True}
v2 = {"host": "localhost", "port": 9000, "workers": 4}

qoshilgan = set(v2) - set(v1)
ochirilgan = set(v1) - set(v2)
umumiy_kalitlar = set(v1) & set(v2)
ozgargan = {k: (v1[k], v2[k]) for k in umumiy_kalitlar if v1[k] != v2[k]}

print(f"Qo'shilgan parametrlar : {qoshilgan}")
print(f"O'chirilgan parametrlar: {ochirilgan}")
print(f"Qiymati o'zgarganlar   : {ozgargan}")
```

## Tushuntirish va Mantiq:
1. To'plamlar ayirmasi orqali konfiguratsiya versiyalaridagi o'zgarishlar audit qilinadi.

## Ishlash natijasi:
```text
Chiqish: Qo'shilgan: {'workers'}, O'chirilgan: {'debug'}, O'zgargan: {'port': (8080, 9000)}
```


# 279-Topshiriq: LRU Kesh (Least Recently Used) simulyatsiyasi

## Topshiriq sharti:
Belgilangan maksimal hajmga ega (masalan 3 ta) va eng kam ishlatilgan elementni chiqarib yuboruvchi kesh mexanizmi.

## Yechim (Python kodi):
```python
from collections import OrderedDict

class OddiyKesh:
    def __init__(self, hajm=3):
        self.hajm = hajm
        self.kesh = OrderedDict()

    def olish(self, kalit):
        if kalit not in self.kesh:
            return None
        self.kesh.move_to_end(kalit)  # Ishlatilgani uchun oxiriga suramiz
        return self.kesh[kalit]

    def qoyish(self, kalit, qiymat):
        if kalit in self.kesh:
            self.kesh.move_to_end(kalit)
        self.kesh[kalit] = qiymat
        if len(self.kesh) > self.hajm:
            self.kesh.popitem(last=False)  # Eng eski ishlatilmaganini o'chiramiz

k = OddiyKesh(3)
k.qoyish("A", 1)
k.qoyish("B", 2)
k.qoyish("C", 3)
k.olish("A")      # A ishlatildi, shuning uchun eng eski endi B bo'lib qoldi
k.qoyish("D", 4)  # B avtomatik o'chib ketadi!

print(f"Keshdagi elementlar: {list(k.kesh.keys())}")
```

## Tushuntirish va Mantiq:
1. `OrderedDict` elementlar kiritilish va murojaat qilinish tartibini qat'iy saqlaydi.
2. Bu veb-serverlar va ma'lumotlar bazalarida eng ko'p ishlatiladigan kesh algoritmidir.

## Ishlash natijasi:
```text
Chiqish: ['C', 'A', 'D'] (B o'chirilgan)
```


# 280-Topshiriq: Elektron do'kon savatchasi tizimi (Shopping Cart)

## Topshiriq sharti:
Mahsulotlar katalogi asosida xaridor savatchasidagi tovarlar umumiy narxini hisoblovchi to'liq tizim.

## Yechim (Python kodi):
```python
katalog = {
    "p1": {"nom": "Futbolka", "narx": 120000},
    "p2": {"nom": "Shim", "narx": 250000},
    "p3": {"nom": "Krossovka", "narx": 450000}
}

savatcha = {
    "p1": 2,  # 2 ta futbolka
    "p3": 1   # 1 ta krossovka
}

jami_summa = 0
print("--- CHEK ---")
for pid, miqdor in savatcha.items():
    mahsulot = katalog[pid]
    narx = mahsulot["narx"]
    summa = narx * miqdor
    jami_summa += summa
    print(f"{mahsulot['nom']:12s} x {miqdor} = {summa:,} so'm")

print("-" * 25)
print(f"JAMI TO'LOV : {jami_summa:,} so'm")
```

## Tushuntirish va Mantiq:
1. Real elektron tijorat (E-commerce) tizimlarining mahsulot ID si orqali hisob-kitob qilish arxitekturasi.

## Ishlash natijasi:
```text
Chiqish: Futbolka x 2 = 240,000, Krossovka x 1 = 450,000 -> Jami: 690,000 so'm
```


# 281-Topshiriq: Lug'atdagi kalitlarni prefiks bo'yicha qidirish

## Topshiriq sharti:
Foydalanuvchi bir necha harf kiritganda shu harflar bilan boshlanuvchi barcha kalitlarni topuvchi dastur.

## Yechim (Python kodi):
```python
lugat = {
    "algoritm": "Muammoni yechish ketma-ketligi",
    "alifbo": "Harflar majmui",
    "algebra": "Matematikaning bir bo'limi",
    "dastur": "Buyruqlar to'plami",
    "data": "Ma'lumotlar"
}

qidiruv = "al"
moslar = {k: v for k, v in lugat.items() if k.startswith(qidiruv)}

print(f"'{qidiruv}' bilan boshlanuvchi so'zlar:")
for k, v in moslar.items():
    print(f" - {k}: {v}")
```

## Tushuntirish va Mantiq:
1. `.startswith()` orqali avtomatik to'ldirish (Autocomplete) takliflari generatsiya qilinadi.

## Ishlash natijasi:
```text
Chiqish: algoritm, alifbo, algebra
```


# 282-Topshiriq: Venn diagrammasi sohalari bo'yicha hisoblash

## Topshiriq sharti:
Ikki to'plam uchun Venn diagrammasining 3 ta asosiy sohasidagi (faqat A, faqat B, ikkalasi ham) elementlar sonini toping.

## Yechim (Python kodi):
```python
a = {"futbol", "shaxmat", "tennis", "suzish"}
b = {"tennis", "suzish", "basketbol", "voleybol"}

faqat_a = a - b
faqat_b = b - a
ikkalasi = a & b

print(f"Faqat A da: {faqat_a} ({len(faqat_a)} ta)")
print(f"Faqat B da: {faqat_b} ({len(faqat_b)} ta)")
print(f"Ikkalasida: {ikkalasi} ({len(ikkalasi)} ta)")
```

## Tushuntirish va Mantiq:
1. Venn diagrammasining barcha bo'limlari to'plamlar amali bilan aniq ajratiladi.

## Ishlash natijasi:
```text
Chiqish: Faqat A: futbol, shaxmat; Faqat B: basketbol, voleybol; Ikkalasida: tennis, suzish
```


# 283-Topshiriq: Matndan eng kam uchragan so'zlarni (Noyob so'zlar) topish

## Topshiriq sharti:
Matnda faqat 1 martagina uchragan barcha kamyob so'zlarni to'plam shaklida chiqaring.

## Yechim (Python kodi):
```python
matn = "kitob oqish foydali kitob inson qalbi uchun oziq ilm olish kitob"

sozlar = matn.split()
hisob = {}
for s in sozlar:
    hisob[s] = hisob.get(s, 0) + 1

faqat_bir_marta = {s for s, soni in hisob.items() if soni == 1}

print(f"Faqat 1 marta uchragan so'zlar: {faqat_bir_marta}")
```

## Tushuntirish va Mantiq:
1. Set comprehension orqali chastotasi 1 bo'lgan so'zlar to'plami olinadi.

## Ishlash natijasi:
```text
Chiqish: {'oqish', 'foydali', 'inson', 'qalbi', 'uchun', 'oziq', 'ilm', 'olish'}
```


# 284-Topshiriq: To'plamlar orqali bir nechta guruhlarning umumiy a'zolarini topish

## Topshiriq sharti:
3 yoki undan ortiq to'plamlarning barchasida qatnashgan umumiy elementlarni toping.

## Yechim (Python kodi):
```python
g1 = {1, 2, 3, 4, 5}
g2 = {2, 3, 5, 7}
g3 = {3, 5, 8, 9}

# set.intersection bir nechta to'plamlarni bir vaqtda kesadi
umumiy = g1.intersection(g2, g3)

print(f"3 ta to'plamning barchasida mavjud elementlar: {umumiy}")
```

## Tushuntirish va Mantiq:
1. `set.intersection(*sets)` bir nechta to'plamlarning umumiy kesishmasini bitta qadamda hisoblaydi.

## Ishlash natijasi:
```text
Chiqish: {3, 5}
```


# 285-Topshiriq: Departamentlar bo'yicha oylik maosh hisoboti

## Topshiriq sharti:
Xodimlar, ularning bo'limlari va maoshlari lug'atidan har bir bo'limning o'rtacha va jami maoshini hisoblang.

## Yechim (Python kodi):
```python
xodimlar = [
    {"ism": "Anvar", "bolim": "IT", "maosh": 15000000},
    {"ism": "Dilnoza", "bolim": "Buxgalteriya", "maosh": 9000000},
    {"ism": "Sardor", "bolim": "IT", "maosh": 18000000},
    {"ism": "Kamola", "bolim": "Marketing", "maosh": 11000000},
    {"ism": "Bekzod", "bolim": "IT", "maosh": 12000000}
]

bolimlar = {}
for x in xodimlar:
    b = x["bolim"]
    if b not in bolimlar:
        bolimlar[b] = []
    bolimlar[b].append(x["maosh"])

print("Bo'limlar bo'yicha tahlil:")
for b, maoshlar in bolimlar.items():
    jami = sum(maoshlar)
    ortacha = jami / len(maoshlar)
    print(f"{b:14s}: Xodimlar: {len(maoshlar)} ta | Jami: {jami:,} so'm | O'rtacha: {ortacha:,.0f} so'm")
```

## Tushuntirish va Mantiq:
1. Guruhlash va yig'ish (Aggregation) amallari orqali biznes hisobot shakllanadi.

## Ishlash natijasi:
```text
Chiqish: IT: 3 ta xodim, O'rtacha: 15,000,000 so'm...
```


# 286-Topshiriq: Lug'atdagi kalitlarni katta harfga o'tkazish

## Topshiriq sharti:
Lug'atdagi barcha satr kalitlarni bosh harflarga aylantiring.

## Yechim (Python kodi):
```python
sozlamalar = {"theme": "dark", "lang": "uz", "font_size": 14}

kattalashtirilgan = {k.upper(): v for k, v in sozlamalar.items()}

print(f"Asl: {sozlamalar}")
print(f"Katta harfli kalitlar: {kattalashtirilgan}")
```

## Tushuntirish va Mantiq:
1. Dict comprehension yordamida kalitlar ustida operatsiya bajariladi.

## Ishlash natijasi:
```text
Chiqish: {'THEME': 'dark', 'LANG': 'uz', 'FONT_SIZE': 14}
```


# 287-Topshiriq: Lug'at qiymatlari bo'yicha ro'yxatlarni birlashtirish

## Topshiriq sharti:
Turli fanlar to'garaklariga yozilgan o'quvchilar ro'yxatidan barcha to'garak a'zolarining takrorlanmas ro'yxatini tuzing.

## Yechim (Python kodi):
```python
togaraklar = {
    "Robototexnika": ["Ali", "Vali", "Sardor"],
    "Shaxmat": ["Vali", "Husan", "Malika"],
    "Dasturlash": ["Ali", "Malika", "Jasur"]
}

barcha_a'zolar = set()
for a'zolar in togaraklar.values():
    barcha_a'zolar.update(a'zolar)

print(f"To'garak qatnashchilari ({len(barcha_a'zolar)} nafar unikal o'quvchi):")
print(sorted(barcha_a'zolar))
```

## Tushuntirish va Mantiq:
1. `set.update(list)` yangi ro'yxat elementlarini to'plamga dublikatsiz qo'shadi.

## Ishlash natijasi:
```text
Chiqish: ['Ali', 'Husan', 'Jasur', 'Malika', 'Sardor', 'Vali']
```


# 288-Topshiriq: IP manzillar oqimidan unikal tashrif buyuruvchilarni sanash

## Topshiriq sharti:
Veb-server jurnalidagi takrorlangan IP manzillardan haqiqiy unikal mehmonlar sonini aniqlang.

## Yechim (Python kodi):
```python
log_ip_oqimi = [
    "192.168.1.1", "10.0.0.5", "192.168.1.1", "172.16.0.2",
    "10.0.0.5", "192.168.1.1", "10.0.0.8", "172.16.0.2"
]

unikal_mehmonlar = set(log_ip_oqimi)

print(f"Jami so'rovlar soni  : {len(log_ip_oqimi)} ta")
print(f"Haqiqiy unikal IP lar: {len(unikal_mehmonlar)} ta")
print(f"IP manzillar ro'yxati: {sorted(unikal_mehmonlar)}")
```

## Tushuntirish va Mantiq:
1. `set()` to'plami yuz minglab log ma'lumotlarini O(n) da unikal qilib beradi.

## Ishlash natijasi:
```text
Chiqish: Jami: 8 ta, Unikal: 4 ta
```


# 289-Topshiriq: Lug'at yordamida valyuta ayirboshlash kalkulyatori

## Topshiriq sharti:
So'mga nisbatan kurslar lug'atidan foydalanib, istalgan ikki xorijiy valyuta o'rtasida konvertatsiya qiling.

## Yechim (Python kodi):
```python
kurslar = {
    "USD": 12800.0,
    "EUR": 13900.0,
    "RUB": 138.0,
    "UZS": 1.0
}

def konvertatsiya(summa, qaysidan, qaysiga):
    somdagi_qiymat = summa * kurslar[qaysidan]
    natija = somdagi_qiymat / kurslar[qaysiga]
    return natija

summa = 100
dan = "USD"
ga = "EUR"
natija = konvertatsiya(summa, dan, ga)

print(f"{summa} {dan} = {natija:.2f} {ga}")
```

## Tushuntirish va Mantiq:
1. Barcha valyutalar avval asosiy bazaga (UZS ga) keltiriladi, keyin maqsad valyutaga bo'linadi.

## Ishlash natijasi:
```text
Chiqish: 100 USD = 92.09 EUR
```


# 290-Topshiriq: So'zlarning uzunligi bo'yicha to'plamlar lug'atini tuzish

## Topshiriq sharti:
Har bir so'z uzunligini kalit qilib, shu uzunlikdagi unikal so'zlar to'plamini hosil qiling.

## Yechim (Python kodi):
```python
matn = "olma anor nok behi shaftoli uzum gilos behi olma"

uzunliklar = {}
for s in matn.split():
    l = len(s)
    if l not in uzunliklar:
        uzunliklar[l] = set()
    uzunliklar[l].add(s)

print("Uzunliklar bo'yicha so'z to'plamlari:")
for u, toplam in sorted(uzunliklar.items()):
    print(f"{u} harfli: {toplam}")
```

## Tushuntirish va Mantiq:
1. To'plam qiymat bo'lgani sababli bir xil so'zlar takrorlanmaydi.

## Ishlash natijasi:
```text
Chiqish: 3 harfli: {'nok'}, 4 harfli: {'behi', 'olma', 'anor', 'uzum'}...
```


# 291-Topshiriq: Lug'at elementlarini qiymati bo'yicha guruhlash

## Topshiriq sharti:
Bir xil yoshdagi odamlarni bitta guruhga birlashtiruvchi teskari indeks yarating.

## Yechim (Python kodi):
```python
odamlar = {
    "Ali": 20,
    "Vali": 22,
    "Hasan": 20,
    "Husan": 21,
    "Zuhra": 22
}

yosh_boyicha = {}
for ism, yosh in odamlar.items():
    if yosh not in yosh_boyicha:
        yosh_boyicha[yosh] = []
    yosh_boyicha[yosh].append(ism)

print("Yosh bo'yicha guruhlangan:")
for yosh, ismlar in sorted(yosh_boyicha.items()):
    print(f"{yosh} yosh: {ismlar}")
```

## Tushuntirish va Mantiq:
1. Bir xil xususiyatga ega ob'ektlarni guruhlash uchun teskari indeks qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: 20 yosh: ['Ali', 'Hasan'], 21 yosh: ['Husan'], 22 yosh: ['Vali', 'Zuhra']
```


# 292-Topshiriq: To'plam orqali dublikatlarni aniqlash va sanash

## Topshiriq sharti:
Ro'yxatdagi qaysi elementlar aynan necha marta takrorlanganini to'plam va lug'at yordamida ko'rsating.

## Yechim (Python kodi):
```python
sonlar = [1, 2, 3, 2, 4, 5, 1, 6, 2, 7, 1]

korilgan = set()
dublikatlar = set()

for x in sonlar:
    if x in korilgan:
        dublikatlar.add(x)
    else:
        korilgan.add(x)

print(f"Asl ro'yxat: {sonlar}")
print(f"Takrorlangan sonlar to'plami: {dublikatlar}")
```

## Tushuntirish va Mantiq:
1. `korilgan` to'plamiga qarab 2-marta uchragan element `dublikatlar` to'plamiga o'tkaziladi.

## Ishlash natijasi:
```text
Chiqish: Takrorlanganlar: {1, 2}
```


# 293-Topshiriq: Sinonimlar qidiruv tizimi (Tezaurus)

## Topshiriq sharti:
So'z kiritilganda uning barcha ma'nodoshlarini (sinonimlarini) qaytaruvchi lug'at tizimi.

## Yechim (Python kodi):
```python
tezaurus = {
    "chiroyli": ["go'zal", "suluv", "zebo", "latofatli"],
    "katta": ["ulkan", "bahaybat", "azim", "yirik"],
    "tez": ["chaqqon", "jadal", "ildam", "shiddatli"]
}

soz = "chiroyli"
sinonimlar = tezaurus.get(soz, [])

print(f"'{soz}' so'zining sinonimlari: {sinonimlar}")
```

## Tushuntirish va Mantiq:
1. NLP (tabiiy tilni qayta ishlash) tizimlarida matn boyligini oshirish uchun qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: ['go'zal', 'suluv', 'zebo', 'latofatli']
```


# 294-Topshiriq: Talabalar baholari matritsasini tahlil qilish

## Topshiriq sharti:
Har bir fan bo'yicha eng yuqori ball to'plagan talabalarni aniqlang.

## Yechim (Python kodi):
```python
fan_baholari = {
    "Matematika": {"Ali": 85, "Vali": 95, "Olim": 90},
    "Fizika": {"Ali": 92, "Vali": 88, "Olim": 80},
    "Dasturlash": {"Ali": 98, "Vali": 94, "Olim": 100}
}

print("Har bir fan bo'yicha g'oliblar:")
for fan, talabalar in fan_baholari.items():
    eng_yaxshi = max(talabalar, key=talabalar.get)
    print(f" - {fan:12s}: {eng_yaxshi} ({talabalar[eng_yaxshi]} ball)")
```

## Tushuntirish va Mantiq:
1. `max(talabalar, key=talabalar.get)` ichki lug'at maksimumini topadi.

## Ishlash natijasi:
```text
Chiqish: Matematika: Vali (95), Fizika: Ali (92), Dasturlash: Olim (100)
```


# 295-Topshiriq: Lug'atdagi kalit va qiymatlarni almashtirish (bir nechta qiymatli holat)

## Topshiriq sharti:
Bir nechta kalitlar bir xil qiymatga ega bo'lganda ham ma'lumot yo'qolmaydigan teskari lug'at tuzing.

## Yechim (Python kodi):
```python
baholar = {
    "Anvar": 5,
    "Malika": 5,
    "Sardor": 4,
    "Jasur": 3,
    "Madina": 4
}

teskari = {}
for ism, ball in baholar.items():
    if ball not in teskari:
        teskari[ball] = []
    teskari[ball].append(ism)

print("Baholar bo'yicha talabalar:")
for ball, ismlar in sorted(teskari.items(), reverse=True):
    print(f"{ball} baho: {ismlar}")
```

## Tushuntirish va Mantiq:
1. Oddiy teskari qilishda 5 baholi talabalardan bittasi qolib ketishi mumkin edi. Ro'yxat ishlatish ma'lumotni to'liq saqlaydi.

## Ishlash natijasi:
```text
Chiqish: 5 baho: ['Anvar', 'Malika'], 4 baho: ['Sardor', 'Madina'], 3 baho: ['Jasur']
```


# 296-Topshiriq: O'yin inventari va buyumlar yig'ish tizimi

## Topshiriq sharti:
O'yin qahramoni buyumlar yig'ganda inventar miqdorlarini yangilovchi tizim.

## Yechim (Python kodi):
```python
inventar = {"oltin": 120, "xanjer": 1, "dori": 3}

topilgan_narsalar = ["oltin", "dori", "oltin", "qalqon", "dori"]

for narsa in topilgan_narsalar:
    if narsa == "oltin":
        inventar["oltin"] += 50
    else:
        inventar[narsa] = inventar.get(narsa, 0) + 1

print(f"Yangilangan qahramon inventari: {inventar}")
```

## Tushuntirish va Mantiq:
1. O'yin mexanikasida inventar lug'ati asosiy saqlash vositasidir.

## Ishlash natijasi:
```text
Chiqish: {'oltin': 220, 'xanjer': 1, 'dori': 5, 'qalqon': 1}
```


# 297-Topshiriq: Lug'atni ro'yxat ichidagi kalit bo'yicha indekslash

## Topshiriq sharti:
Foydalanuvchilar ro'yxatidan ularning `id`si bo'yicha bir zumda O(1) da topish imkonini beruvchi lug'at yarating.

## Yechim (Python kodi):
```python
foydalanuvchilar = [
    {"id": 101, "ism": "Ali", "rol": "Admin"},
    {"id": 102, "ism": "Vali", "rol": "User"},
    {"id": 103, "ism": "G'ani", "rol": "Moderator"}
]

id_boyicha_indeks = {u["id"]: u for u in foydalanuvchilar}

# 102 ID li foydalanuvchini tezkor olish:
qidirilgan_id = 102
print(f"Topilgan foydalanuvchi: {id_boyicha_indeks.get(qidirilgan_id)}")
```

## Tushuntirish va Mantiq:
1. Ro'yxatda qidirish O(n) vaqt olsa, bunday indeks lug'at orqali O(1) ga tushadi.

## Ishlash natijasi:
```text
Chiqish: {'id': 102, 'ism': 'Vali', 'rol': 'User'}
```


# 298-Topshiriq: To'plam yordamida ikkita satr o'xshashligini tekshirish

## Topshiriq sharti:
Ikki matn aynan bir xil harflar to'plamidan tashkil topganligini aniqlang.

## Yechim (Python kodi):
```python
satr1 = "dasturchi"
satr2 = "ruchkidast"

t1 = set(satr1)
t2 = set(satr2)

print(f"1-matn harflari: {t1}")
print(f"2-matn harflari: {t2}")
print(f"Harflar tarkibi bir xilmi? {t1 == t2}")
```

## Tushuntirish va Mantiq:
1. `set(s1) == set(s2)` harflarning uchrash tartibi va takrorlanishlariga qaramasdan alifbo tarkibini tekshiradi.

## Ishlash natijasi:
```text
Chiqish: True
```


# 299-Topshiriq: Lug'at elementlarini chiroyli jadval shaklida chiqarish

## Topshiriq sharti:
Lug'atdagi ko'p sonli ma'lumotlarni terminalda tekis ustunlar bilan chop etuvchi funksiya.

## Yechim (Python kodi):
```python
shaharlar = {
    "Toshkent": 3000000,
    "Samarqand": 550000,
    "Buxoro": 280000,
    "Andijon": 450000,
    "Namangan": 650000
}

print(f"{'Shahar':15s} | {'Aholi soni':12s}")
print("-" * 30)
for sh, a in shaharlar.items():
    print(f"{sh:15s} | {a:12,d}")
```

## Tushuntirish va Mantiq:
1. Format spetsifikatorlari tekis chiroyli jadval chiqarishni ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: Tekislangan jadval ko'rinishi.
```


# 300-Topshiriq: Lug'at va To'plamlar bilan Quiz (Test Sinovi) Dasturi

## Topshiriq sharti:
Savollar, variantlar to'plami va to'g'ri javoblar lug'ati asosida interaktiv test tizimini tuzing.

## Yechim (Python kodi):
```python
savollar = [
    {
        "savol": "Python qachon yaratilgan?",
        "variantlar": {"A": "1991", "B": "1995", "C": "2000"},
        "togri": "A"
    },
    {
        "savol": "Qaysi ma'lumot turi o'zgarmas (immutable)?",
        "variantlar": {"A": "List", "B": "Dictionary", "C": "Tuple"},
        "togri": "C"
    }
]

ball = 0
for i, s in enumerate(savollar, start=1):
    print(f"
{i}-Savol: {s['savol']}")
    for kalit, matn in s["variantlar"].items():
        print(f"  {kalit}) {matn}")
    
    # Simulyatsiya: to'g'ri javob berildi deb olamiz
    javob = s["togri"]
    if javob == s["togri"]:
        ball += 1

print(f"
Test yakunlandi! Sizning natijangiz: {ball}/{len(savollar)}")
```

## Tushuntirish va Mantiq:
1. Lug'atlar va ro'yxatlar kombinatsiyasi orqali har qanday murakkab test tizimlari dasturlanadi.

## Ishlash natijasi:
```text
Chiqish: Natija: 2/2
```

