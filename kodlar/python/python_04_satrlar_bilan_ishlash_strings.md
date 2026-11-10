# Python Dasturlash Tili — 4-Qism: Satrlar (Strings) bilan Mukammal Ishlash va Matn Tahlili
## (151-200 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam satrlar (strings) va matnlarni qayta ishlash bo'yicha eng muhim amaliy vazifalarni o'z ichiga oladi:
* Satrlarni kesish (slicing), indeksatsiya va teskarisiga o'girish;
* Palindromlar, anagrammalar, izogrammalar va pangrammalar;
* Regulyar ifodalar (regex): email, URL, telefon, teglarni tozalash;
* Formatlash, registrlarni o'zgartirish, kebab-case, camelCase, snake_case konvertatsiyasi;
* Qavslar balansi (stack mantiqi), Morze va ROT13 shifrlari;

---

# 151-Topshiriq: Satr uzunligini len() funksiyasisiz hisoblash

## Topshiriq sharti:
Kiritilgan satrning uzunligini (belgilar sonini) tayyor `len()` funksiyasidan foydalanmasdan, for tsikli yordamida hisoblang.

## Yechim (Python kodi):
```python
matn = input("Satr kiriting: ")

uzunlik = 0
for _ in matn:
    uzunlik += 1

print(f"Satr: '{matn}'")
print(f"Belgilar soni: {uzunlik} ta")
```

## Tushuntirish va Mantiq:
1. Tsikl satrning har bir belgisi bo'yicha bittadan aylanib chiqadi.
2. `uzunlik += 1` har bir iteratsiyada hisoblagichni 1 taga oshirib, yakuniy uzunlikni beradi.

## Ishlash natijasi:
```text
Kiritish: Python dasturlash -> Chiqish: 18 ta
```


# 152-Topshiriq: Satrni teskari o'girish (Slicing va Tsikl)

## Topshiriq sharti:
Satrni ikkita usulda: indeks qadami (`[::-1]`) va for tsikli orqali teskarisiga o'giring.

## Yechim (Python kodi):
```python
matn = input("Matn kiriting: ")

# 1-usul: Slicing (eng tezkor va qisqa)
teskari_slice = matn[::-1]

# 2-usul: Tsikl yordamida
teskari_tsikl = ""
for ch in matn:
    teskari_tsikl = ch + teskari_tsikl

print(f"1-usul natijasi: {teskari_slice}")
print(f"2-usul natijasi: {teskari_tsikl}")
```

## Tushuntirish va Mantiq:
1. `matn[::-1]` satrni oxiridan boshlab boshiga qarab -1 qadam bilan kesib oladi.
2. `ch + teskari_tsikl` yangi belgini natija boshiga qo'shish orqali teskari tartib hosil qiladi.

## Ishlash natijasi:
```text
Kiritish: Toshkent -> Chiqish: tnekshoT
```


# 153-Topshiriq: Palindrom satrni tekshirish

## Topshiriq sharti:
Kiritilgan satrning katta-kichik harflar va bo'shliqlarni hisobga olmaganda palindrom ekanligini aniqlang.

## Yechim (Python kodi):
```python
matn = input("Matn yoki ibora kiriting: ")

# Bo'shliqlarni olib tashlaymiz va kichik harfga o'tkazamiz
toza = "".join(ch.lower() for ch in matn if ch.isalnum())

if toza == toza[::-1]:
    print(f"'{matn}' — PALINDROM ibora!")
else:
    print(f"'{matn}' — Palindrom emas.")
```

## Tushuntirish va Mantiq:
1. `.isalnum()` faqat harf va raqamlarni qoldirib, tinish belgilari va bo'shliqlarni chiqarib tashlaydi.
2. Tozalangan satr o'zining teskarisi bilan taqqoslanadi.

## Ishlash natijasi:
```text
Kiritish: 'A nod, a dog, a pant: a gnat at a gap, god, a don' -> Chiqish: PALINDROM ibora!
```


# 154-Topshiriq: So'zlarning bosh harfini kattalashtirish (Capitalize)

## Topshiriq sharti:
Matndagi barcha so'zlarning birinchi harfini bosh harfga, qolganlarini kichik harfga o'tkazing.

## Yechim (Python kodi):
```python
gap = input("Jumla kiriting: ")

# 1-usul: Tayyor metod
natija_title = gap.title()

# 2-usul: Algoritmik usul
sozlar = gap.split()
kattalashgan = [s.capitalize() for s in sozlar]
natija_algoritm = " ".join(kattalashgan)

print("Natija:", natija_algoritm)
```

## Tushuntirish va Mantiq:
1. `.capitalize()` so'zning 1-harfini katta, qolganlarini kichik qiladi.
2. `split()` va `join()` kombinatsiyasi barcha so'zlarga bir xil qoidani qo'llaydi.

## Ishlash natijasi:
```text
Kiritish: 'alisher navoiy xamsa asari' -> Chiqish: 'Alisher Navoiy Xamsa Asari'
```


# 155-Topshiriq: Satrdan barcha tinish belgilarini tozalash

## Topshiriq sharti:
Matndan vergul, nuqta, undov, qavs kabi barcha tinish belgilarini tozalovchi dastur yozing.

## Yechim (Python kodi):
```python
import string

matn = input("Tinish belgili matn kiriting: ")

# string.punctuation ichida barcha standart tinish belgilari mavjud
toza_matn = "".join(ch for ch in matn if ch not in string.punctuation)

print(f"Tozalangan matn: {toza_matn}")
```

## Tushuntirish va Mantiq:
1. `string.punctuation` barcha `!"#$%&'()*+,-./:;<=>?@[\]^_{|}~` belgilarini o'z ichiga oladi.
2. Generator ifodasi orqali faqat tinish belgisi bo'lmagan belgilar yig'iladi.

## Ishlash natijasi:
```text
Kiritish: 'Salom, do'stlar! Ishlar qalay?' -> Chiqish: 'Salom do'stlar Ishlar qalay'
```


# 156-Topshiriq: Anagramma so'zlarni aniqlash

## Topshiriq sharti:
Ikki so'zning anagramma ekanligini (bir xil harflarning boshqa tartibda joylashuvi, masalan: 'tok' va 'kot') aniqlang.

## Yechim (Python kodi):
```python
soz1 = input("1-so'zni kiriting: ").strip().lower()
soz2 = input("2-so'zni kiriting: ").strip().lower()

# Harflar saralanganda bir xil bo'lsa anagramma hisoblanadi
if sorted(soz1) == sorted(soz2):
    print(f"'{soz1}' va '{soz2}' — ANAGRAMMA!")
else:
    print(f"'{soz1}' va '{soz2}' — Anagramma emas.")
```

## Tushuntirish va Mantiq:
1. `sorted('tok')` -> `['k', 'o', 't']` ro'yxatini beradi.
2. Agar ikkala so'zning saralangan harflar ro'yxati teng bo'lsa, demak ular aynan bir xil harflardan tashkil topgan.

## Ishlash natijasi:
```text
Kiritish: 'olma', 'mola' -> Chiqish: ANAGRAMMA!
```


# 157-Topshiriq: Harflar chastotasi xaritasi (Frequency Map)

## Topshiriq sharti:
Matndagi har bir harf necha martadan qatnashganini hisoblab, lug'at (dictionary) shaklida chiqaring.

## Yechim (Python kodi):
```python
matn = input("Matn kiriting: ").lower()

chastota = {}
for ch in matn:
    if ch.isalpha():  # Faqat harflarni hisoblaymiz
        chastota[ch] = chastota.get(ch, 0) + 1

# Eng ko'p qatnashgan tartibida saralaymiz
saralangan = sorted(chastota.items(), key=lambda x: x[1], reverse=True)

print("
Harflar chastotasi:")
for harf, soni in saralangan:
    print(f"'{harf}': {soni} marta")
```

## Tushuntirish va Mantiq:
1. `.get(ch, 0)` kalit lug'atda bo'lsa uning qiymatini, bo'lmasa 0 qaytaradi.
2. `sorted(..., reverse=True)` eng ko'p uchragan harflarni birinchi qilib chiqaradi.

## Ishlash natijasi:
```text
Kiritish: 'dasturlash' -> Chiqish: 'a': 2, 's': 2, 'd': 1, 't': 1, 'u': 1, 'r': 1, 'l': 1, 'h': 1
```


# 158-Topshiriq: Matndagi eng uzun so'zni topish

## Topshiriq sharti:
Foydalanuvchi kiritgan jumlada eng uzun so'zni va uning harflar sonini aniqlang.

## Yechim (Python kodi):
```python
gap = input("Gap kiriting: ")

sozlar = gap.split()
if not sozlar:
    print("Bo'sh matn kiritildi.")
else:
    # max() funksiyasi key=len bilan eng uzun so'zni topadi
    eng_uzun = max(sozlar, key=lambda s: len(s.strip(".,!?:;"'()")))
    toza_uzun = eng_uzun.strip(".,!?:;"'()")
    print(f"Eng uzun so'z: '{toza_uzun}'")
    print(f"Uzunligi: {len(toza_uzun)} ta harf")
```

## Tushuntirish va Mantiq:
1. `max(sozlar, key=...)` har bir elementning berilgan xossasi bo'yicha maksimumini tanlaydi.
2. `.strip()` tinish belgilarini hisobga olmaslikni ta'minlaydi.

## Ishlash natijasi:
```text
Kiritish: 'Sun'iy intellekt kelajak texnologiyasidir' -> Chiqish: 'texnologiyasidir' (16 ta)
```


# 159-Topshiriq: Parol kuchliligini tekshiruvchi validator

## Topshiriq sharti:
Parol kamida 8 ta belgidan iborat, katta harf, kichik harf, raqam va maxsus belgi qatnashganligini tekshiring.

## Yechim (Python kodi):
```python
parol = input("Parolni kiriting: ")

kamchiliklar = []

if len(parol) < 8:
    kamchiliklar.append("Kamida 8 ta belgidan iborat bo'lishi kerak")
if not any(ch.isupper() for ch in parol):
    kamchiliklar.append("Kamida 1 ta katta harf (A-Z) bo'lishi kerak")
if not any(ch.islower() for ch in parol):
    kamchiliklar.append("Kamida 1 ta kichik harf (a-z) bo'lishi kerak")
if not any(ch.isdigit() for ch in parol):
    kamchiliklar.append("Kamida 1 ta raqam (0-9) bo'lishi kerak")
if not any(ch in "!@#$%^&*()-_=+[]{}|;:,.<>?" for ch in parol):
    kamchiliklar.append("Kamida 1 ta maxsus belgi (!@#$%...) bo'lishi kerak")

if not kamchiliklar:
    print("Parol juda kuchli va xavfsiz!")
else:
    print("Parol talabga javob bermaydi:")
    for k in kamchiliklar:
        print(f" - {k}")
```

## Tushuntirish va Mantiq:
1. `any()` funksiyasi shart kamida bir marta bajarilsa `True` qaytaradi.
2. `.isupper()`, `.islower()`, `.isdigit()` xarakter guruhlarini aniq tekshiradi.

## Ishlash natijasi:
```text
Kiritish: 'Parol123' -> Chiqish: Kamida 1 ta maxsus belgi bo'lishi kerak
```


# 160-Topshiriq: Email manzilining to'g'riligini (validatsiya) tekshirish

## Topshiriq sharti:
Kiritilgan email manzilida `@` belgisi borligi, domenda nuqta mavjudligi va formati to'g'riligini aniqlang.

## Yechim (Python kodi):
```python
import re

email = input("Email manzilini kiriting: ").strip()

# Standart email regulyar ifodasi (RFC 5322 soddalashtirilgan)
andoza = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

if re.match(andoza, email):
    print(f"'{email}' — TO'G'RI email manzili.")
else:
    print(f"'{email}' — NOTO'G'RI email formati!")
```

## Tushuntirish va Mantiq:
1. `re.match()` satr boshidan oxirigacha andozaga mosligini tekshiradi.
2. `^[a-zA-Z0-9._%+-]+` nom qismi, `@[a-zA-Z0-9.-]+` provayder qismi, `\.[a-zA-Z]{2,}$` domen zonasi.

## Ishlash natijasi:
```text
Kiritish: alisher@gmail.com -> Chiqish: TO'G'RI email manzili.
```


# 161-Topshiriq: Matndan raqamlarni ajratib, yig'indisini hisoblash

## Topshiriq sharti:
Satr ichidagi barcha raqamlarni ajratib olib, ularning arifmetik yig'indisini hisoblang.

## Yechim (Python kodi):
```python
matn = input("Raqamlar aralashgan matn kiriting: ")

raqamlar = [int(ch) for ch in matn if ch.isdigit()]
yigindi = sum(raqamlar)

print(f"Ajratilgan raqamlar: {raqamlar}")
print(f"Raqamlar yig'indisi: {yigindi}")
```

## Tushuntirish va Mantiq:
1. `ch.isdigit()` faqat raqamlarni ajratadi.
2. `sum()` barcha int ga o'girilgan raqamlar yig'indisini hisoblaydi.

## Ishlash natijasi:
```text
Kiritish: 'Toshkent-2026, 3 ta bekat, 5-yo'l' -> Chiqish: [2, 0, 2, 6, 3, 5], Yig'indi: 18
```


# 162-Topshiriq: kebab-case satrni camelCase ga o'tkazish

## Topshiriq sharti:
Chiziqcha bilan ajratilgan satrni (masalan: 'user-profile-id') camelCase formatiga o'giring.

## Yechim (Python kodi):
```python
kebab = input("kebab-case matn (masalan: order-item-count): ").strip()

bolaklar = kebab.split('-')
if not bolaklar:
    camel = ""
else:
    # 1-so'z kichik harfda, qolganlari bosh harf bilan
    camel = bolaklar[0].lower() + "".join(b.capitalize() for b in bolaklar[1:])

print(f"kebab-case: {kebab}")
print(f"camelCase : {camel}")
```

## Tushuntirish va Mantiq:
1. `.split('-')` chiziqchalar bo'yicha so'zlarga bo'ladi.
2. 1-qism o'zgarishsiz qoladi, keyingi barcha qismlar `capitalize()` orqali birlashtiriladi.

## Ishlash natijasi:
```text
Kiritish: 'user-first-name' -> Chiqish: 'userFirstName'
```


# 163-Topshiriq: camelCase satrni snake_case ga o'tkazish

## Topshiriq sharti:
camelCase formatidagi identifikatorni (masalan: 'getUserProfile') snake_case formatiga ('get_user_profile') o'giring.

## Yechim (Python kodi):
```python
camel = input("camelCase matn kiriting (masalan: totalStudentScore): ").strip()

natija = []
for ch in camel:
    if ch.isupper():
        natija.append('_')
        natija.append(ch.lower())
    else:
        natija.append(ch)

snake = "".join(natija).lstrip('_')
print(f"camelCase : {camel}")
print(f"snake_case: {snake}")
```

## Tushuntirish va Mantiq:
1. Har bir katta harf uchraganda oldiga `_` belgisi qo'yiladi va harf kichiklashtiriladi.
2. `lstrip('_')` agar 1-harf katta bo'lsa hosil bo'ladigan boshdagi ortiqcha chiziqchani olib tashlaydi.

## Ishlash natijasi:
```text
Kiritish: 'calculateMonthlySalary' -> Chiqish: 'calculate_monthly_salary'
```


# 164-Topshiriq: So'zlar sonini to'g'ri sanash

## Topshiriq sharti:
Oralarida bir nechta ketma-ket bo'shliqlar bo'lgan matndagi haqiqiy so'zlar sonini aniqlang.

## Yechim (Python kodi):
```python
matn = input("Matn kiriting: ")

# split() argumentlarsiz chaqirilganda har qanday bo'shliqlar ketma-ketligini bitta deb oladi
sozlar = matn.split()

print(f"So'zlar ro'yxati: {sozlar}")
print(f"Haqiqiy so'zlar soni: {len(sozlar)} ta")
```

## Tushuntirish va Mantiq:
1. `matn.split(' ')` bitta bo'shliqni qidirib bo'sh satrlar hosil qiladi, lekin `matn.split()` argumentisiz barcha bo'shliqlarni avtomatik tozalaydi.

## Ishlash natijasi:
```text
Kiritish: 'Bugun   ob-havo    juda   issiq' -> Chiqish: 4 ta so'z
```


# 165-Topshiriq: Registrlarni teskarisiga almashtirish (Swapcase)

## Topshiriq sharti:
Matndagi katta harflarni kichikka, kichik harflarni kattaga aylantiruvchi algoritmni tuzing.

## Yechim (Python kodi):
```python
matn = input("Matn kiriting: ")

# Algoritmik usul:
almashtirilgan = []
for ch in matn:
    if ch.isupper():
        almashtirilgan.append(ch.lower())
    elif ch.islower():
        almashtirilgan.append(ch.upper())
    else:
        almashtirilgan.append(ch)

natija = "".join(almashtirilgan)
print(f"Natija: {natija}")
```

## Tushuntirish va Mantiq:
1. `.isupper()` va `.islower()` yordamida registr aniqlanadi.
2. Python'da tayyor `matn.swapcase()` metodi ham aynan shu vazifani bajaradi.

## Ishlash natijasi:
```text
Kiritish: 'PyThOn 3.12' -> Chiqish: 'pYtHoN 3.12'
```


# 166-Topshiriq: Ortiqcha bo'shliqlarni bittaga keltirish

## Topshiriq sharti:
Matn ichidagi ikki yoki undan ortiq ketma-ket kelgan bo'shliqlarni bitta bo'shliqqa keltiring.

## Yechim (Python kodi):
```python
import re

matn = input("Matn kiriting: ")

# 1-usul: split va join bilan
toza_1 = " ".join(matn.split())

# 2-usul: Regulyar ifoda bilan
toza_2 = re.sub(r'\s+', ' ', matn).strip()

print(f"Toza matn: '{toza_1}'")
```

## Tushuntirish va Mantiq:
1. `\s+` regulyar ifodasi bir yoki bir nechta probel, tab yoki yangi qator belgilarini bildiradi.
2. `matn.split()` esa so'zlarni ajratib, `" ".join()` orqali bitta bo'shliq bilan ulaydi.

## Ishlash natijasi:
```text
Kiritish: 'Men     kelajakda    dasturchi     bo'laman' -> Chiqish: 'Men kelajakda dasturchi bo'laman'
```


# 167-Topshiriq: So'zlar tartibini teskari qilish

## Topshiriq sharti:
Jumlani so'zma-so'z teskari tartibda chiqaring (harflar o'zgarmasdan qoladi).

## Yechim (Python kodi):
```python
gap = input("Jumla kiriting: ")

sozlar = gap.split()
teskari_gap = " ".join(reversed(sozlar))

print(f"Asl gap   : {gap}")
print(f"Teskari gap: {teskari_gap}")
```

## Tushuntirish va Mantiq:
1. `gap.split()` so'zlar ro'yxatini beradi.
2. `reversed(sozlar)` ro'yxatni oxiridan boshiga o'giradi.
3. `" ".join()` ularni yana bo'shliq bilan birlashtiradi.

## Ishlash natijasi:
```text
Kiritish: 'Oltin olma duo ol' -> Chiqish: 'ol duo olma Oltin'
```


# 168-Topshiriq: Izogramma so'zni tekshirish

## Topshiriq sharti:
Birorta ham harfi takrorlanmagan so'z izogramma deyiladi. So'zning izogramma ekanligini aniqlang.

## Yechim (Python kodi):
```python
soz = input("So'z kiriting: ").strip().lower()

# Faqat harflarni olamiz
harflar = [ch for ch in soz if ch.isalpha()]

if len(harflar) == len(set(harflar)):
    print(f"'{soz}' — IZOGRAMMA (barcha harflar takrorlanmas).")
else:
    print(f"'{soz}' — Izogramma emas (harflar takrorlangan).")
```

## Tushuntirish va Mantiq:
1. `set()` to'plami faqat unikal elementlarni saqlaydi.
2. Agar to'plam uzunligi asl ro'yxat uzunligiga teng bo'lsa, demak dublikat harflar yo'q.

## Ishlash natijasi:
```text
Kiritish: 'daryo' -> Chiqish: IZOGRAMMA! / Kiritish: 'kitoblar' -> Chiqish: Izogramma emas
```


# 169-Topshiriq: Gapdagi har bir so'zning o'zini teskari qilish

## Topshiriq sharti:
So'zlarning joylashuv tartibini saqlagan holda, har bir so'zning harflarini teskarisiga o'giring.

## Yechim (Python kodi):
```python
gap = input("Gap kiriting: ")

sozlar = gap.split()
teskari_sozlar = [s[::-1] for s in sozlar]
natija = " ".join(teskari_sozlar)

print(f"Natija: {natija}")
```

## Tushuntirish va Mantiq:
1. `s[::-1]` har bir so'zning ichidagi harflarni teskarisiga o'giradi.
2. List comprehension orqali har bir so'zga alohida qo'llanadi.

## Ishlash natijasi:
```text
Kiritish: 'Salom dunyo' -> Chiqish: 'molaS oynud'
```


# 170-Topshiriq: Pangramma gapni tekshirish

## Topshiriq sharti:
Ingliz alifbosidagi barcha 26 ta harf qatnashgan gap pangramma deyiladi. Berilgan gapni tekshiring.

## Yechim (Python kodi):
```python
import string

gap = input("Matn kiriting: ").lower()

alifbo = set(string.ascii_lowercase)
matn_harflari = set(ch for ch in gap if ch.isalpha())

if alifbo.issubset(matn_harflari):
    print("Bu gap — PANGRAMMA! (Barcha harflar mavjud)")
else:
    yetishmayotgan = alifbo - matn_harflari
    print("Pangramma emas.")
    print("Yetishmayotgan harflar:", sorted(yetishmayotgan))
```

## Tushuntirish va Mantiq:
1. `string.ascii_lowercase` barcha 'a' dan 'z' gacha harflar to'plamidir.
2. `.issubset()` butun alifbo matn ichida mavjudligini aniqlaydi.

## Ishlash natijasi:
```text
Kiritish: 'The quick brown fox jumps over the lazy dog' -> Chiqish: PANGRAMMA!
```


# 171-Topshiriq: HTML teglarini tozalash

## Topshiriq sharti:
Matn ichidagi barcha `<p>`, `<b>`, `<a href=...>` kabi HTML teglarini olib tashlang.

## Yechim (Python kodi):
```python
import re

html_matn = input("HTML matn kiriting: ")

# Regulyar ifoda orqali < va > orasidagi barcha teglarni o'chiramiz
toza_matn = re.sub(r'<[^>]+>', '', html_matn)

print(f"Tozalangan matn: {toza_matn}")
```

## Tushuntirish va Mantiq:
1. `<[^>]+>` andozasi `<` belgisi bilan boshlanib, `>` gacha bo'lgan har qanday teglarni topadi.
2. `re.sub(..., '', matn)` ularni bo'sh satrga almashtiradi.

## Ishlash natijasi:
```text
Kiritish: '<p>Salom <b>dunyo</b>! <a href="#">Bosing</a></p>' -> Chiqish: 'Salom dunyo! Bosing'
```


# 172-Topshiriq: Telefon raqamini xalqaro formatga keltirish

## Topshiriq sharti:
Kiritilgan har qanday 9 xonali o'zbek raqamini '+998 (XX) XXX-XX-XX' standart formatiga keltiring.

## Yechim (Python kodi):
```python
raqam = input("Telefon raqamini kiriting: ")

# Faqat raqamlarni ajratib olamiz
toza = "".join(ch for ch in raqam if ch.isdigit())

# Agar 998 bilan boshlangan bo'lsa uni olib tashlaymiz
if toza.startswith("998") and len(toza) == 12:
    toza = toza[3:]

if len(toza) == 9:
    kod = toza[:2]
    qism1 = toza[2:5]
    qism2 = toza[5:7]
    qism3 = toza[7:9]
    formatlangan = f"+998 ({kod}) {qism1}-{qism2}-{qism3}"
    print(f"Standart format: {formatlangan}")
else:
    print("Noto'g'ri raqam uzunligi (9 ta raqam bo'lishi kerak)!")
```

## Tushuntirish va Mantiq:
1. Avval foydalanuvchi kiritgan ortiqcha qavs, chiziqcha va bo'shliqlar tozalanadi.
2. 9 ta raqam bo'laklarga ajratilib f-string bilan rasmiy formatga keltiriladi.

## Ishlash natijasi:
```text
Kiritish: '901234567' -> Chiqish: '+998 (90) 123-45-67'
```


# 173-Topshiriq: So'zlarni xavfsiz almashtirish (Word Replacement)

## Topshiriq sharti:
Matndagi ma'lum bir so'zni boshqasiga faqat butun so'z bo'lgandagina almashtiring.

## Yechim (Python kodi):
```python
import re

matn = "Men olma yedim. Olmaxon esa daraxtda sakradi."
eski = "olma"
yangi = "anor"

# \b so'z chegarasini (word boundary) bildiradi
natija = re.sub(rf'{eski}', yangi, matn, flags=re.IGNORECASE)

print("Asl matn   :", matn)
print("Natija     :", natija)
```

## Tushuntirish va Mantiq:
1. Oddiy `str.replace('olma', 'anor')` 'Olmaxon' so'zini ham 'Anorxon' qilib yuboradi.
2. `\b` so'z chegarasi faqat mustaqil 'olma' so'zini almashtirishni kafolatlaydi.

## Ishlash natijasi:
```text
Chiqish: 'Men anor yedim. Olmaxon esa daraxtda sakradi.'
```


# 174-Topshiriq: URL manzilini qismlarga ajratish

## Topshiriq sharti:
Veb-manzilni protokoli, domeni, yo'li va parametri bo'yicha qismlarga ajrating.

## Yechim (Python kodi):
```python
from urllib.parse import urlparse

url = input("URL manzilini kiriting: ").strip()
ajratilgan = urlparse(url)

print(f"Protokol (Scheme) : {ajratilgan.scheme}")
print(f"Domen (Netloc)    : {ajratilgan.netloc}")
print(f"Yo'l (Path)       : {ajratilgan.path}")
print(f"Parametrlar (Query): {ajratilgan.query}")
```

## Tushuntirish va Mantiq:
1. Standart kutubxonadagi `urllib.parse.urlparse` URL manzilini xalqaro standartlar bo'yicha tahlil qiladi.

## Ishlash natijasi:
```text
Kiritish: 'https://kun.uz/news/2026/05/10?category=texno' -> Protokol: https, Domen: kun.uz, Yo'l: /news/2026/05/10, Query: category=texno
```


# 175-Topshiriq: Qavslar balansini tekshirish (Stack mantiqi)

## Topshiriq sharti:
Matndagi barcha `()`, `[]`, `{}` qavslarning to'g'ri ochilib va tartib bilan yopilganligini aniqlang.

## Yechim (Python kodi):
```python
ifoda = input("Qavsli ifoda kiriting: ")

moslik = {')': '(', ']': '[', '}': '{'}
stek = []
tugri = True

for ch in ifoda:
    if ch in moslik.values():
        stek.append(ch)
    elif ch in moslik.keys():
        if not stek or stek.pop() != moslik[ch]:
            tugri = False
            break

if tugri and len(stek) == 0:
    print("Qavslar balansi TO'G'RI!")
else:
    print("XATOLIK: Qavslar noto'g'ri joylashtirilgan!")
```

## Tushuntirish va Mantiq:
1. Stack (stek) ma'lumotlar tuzilmasi: oxirgi ochilgan qavs birinchi yopilishi shart (LIFO).
2. `pop()` oxirgi elementni olib, yopilayotgan qavsga mosligini tekshiradi.

## Ishlash natijasi:
```text
Kiritish: '{[a + b] * (c - d)}' -> Chiqish: TO'G'RI! / Kiritish: '([)]' -> Chiqish: XATOLIK
```


# 176-Topshiriq: Kredit karta raqamini niqoblash (Masking)

## Topshiriq sharti:
16 xonali karta raqamining faqat oxirgi 4 ta raqamini ko'rsatib, qolganlarini yulduzcha bilan niqoblang.

## Yechim (Python kodi):
```python
karta = input("16 xonali karta raqami: ").replace(" ", "")

if len(karta) == 16 and karta.isdigit():
    niqoblangan = "**** **** **** " + karta[-4:]
    print(f"Karta: {niqoblangan}")
else:
    print("Karta raqami 16 ta raqamdan iborat bo'lishi shart!")
```

## Tushuntirish va Mantiq:
1. `karta[-4:]` oxirgi 4 ta raqamni ajratib oladi.
2. Xavfsizlik talablariga ko'ra cheklar va ilovalarda mijoz kartasining faqat oxiri ko'rsatiladi.

## Ishlash natijasi:
```text
Kiritish: '8600123456789988' -> Chiqish: '**** **** **** 9988'
```


# 177-Topshiriq: Matndagi unli harflarni yulduzcha bilan almashtirish

## Topshiriq sharti:
Matndagi barcha unli harflarni (a, e, i, o, u) yulduzcha (*) belgisi bilan almashtiring.

## Yechim (Python kodi):
```python
matn = input("Matn kiriting: ")

unlilar = "aeiouAEIOU"
natija = "".join('*' if ch in unlilar else ch for ch in matn)

print(f"Natija: {natija}")
```

## Tushuntirish va Mantiq:
1. Har bir belgi unlilar to'plamida borligi tekshiriladi va mos ravishda almashtiriladi.

## Ishlash natijasi:
```text
Kiritish: 'Salom Dunyo' -> Chiqish: 'S*l*m D*ny*'
```


# 178-Topshiriq: Matnni so'zni kesmasdan qisqartirish (Truncate)

## Topshiriq sharti:
Matnni berilgan maksimal uzunlikda (masalan, 20 belgi) so'zlarni o'rtasidan kesmasdan '...' bilan qisqartiring.

## Yechim (Python kodi):
```python
matn = input("Matn kiriting: ")
maks_uzunlik = 25

if len(matn) <= maks_uzunlik:
    natija = matn
else:
    qisqa = matn[:maks_uzunlik]
    # Oxirgi bo'shliqdan keyingi qismini olib tashlaymiz
    if " " in qisqa:
        qisqa = qisqa.rsplit(" ", 1)[0]
    natija = qisqa + "..."

print(f"Qisqartirilgan matn: {natija}")
```

## Tushuntirish va Mantiq:
1. `rsplit(' ', 1)` o'ngdan birinchi bo'shliq bo'yicha bo'ladi.
2. Bu usul so'zlarning yarmi kesilib xunuk chiqishining oldini oladi.

## Ishlash natijasi:
```text
Kiritish: 'Sun'iy intellekt kelajak kasbidir', maks=20 -> Chiqish: 'Sun'iy intellekt...'
```


# 179-Topshiriq: Satrdan barcha dublikat belgilarni olib tashlash

## Topshiriq sharti:
Satrdagi harflar tartibini saqlagan holda ikkinchi marta takrorlangan belgilarni o'chiring.

## Yechim (Python kodi):
```python
matn = input("Satr kiriting: ")

korilganlar = set()
natija = []

for ch in matn:
    if ch not in korilganlar:
        korilganlar.add(ch)
        natija.append(ch)

print(f"Toza satr: {''.join(natija)}")
```

## Tushuntirish va Mantiq:
1. `set()` qidirish amalini O(1) da juda tez bajaradi.
2. `natija` ro'yxati esa asl tartibni saqlab qoladi.

## Ishlash natijasi:
```text
Kiritish: 'banana' -> Chiqish: 'ban'
```


# 180-Topshiriq: Matndagi eng ko'p takrorlangan so'zni topish

## Topshiriq sharti:
Matndagi eng ko'p ishlatilgan so'zni va uning sonini aniqlang.

## Yechim (Python kodi):
```python
gap = input("Matn kiriting: ").lower()

sozlar = [s.strip(".,!?:;"'()") for s in gap.split()]
hisob = {}

for s in sozlar:
    if s:
        hisob[s] = hisob.get(s, 0) + 1

if hisob:
    eng_kop_soz = max(hisob, key=hisob.get)
    print(f"Eng ko'p ishlatilgan so'z: '{eng_kop_soz}' ({hisob[eng_kop_soz]} marta)")
```

## Tushuntirish va Mantiq:
1. Lug'atda so'zlar chastotasi shakllantiriladi.
2. `max(hisob, key=hisob.get)` eng katta qiymatga ega kalitni qaytaradi.

## Ishlash natijasi:
```text
Kiritish: 'kitob bilim manbai, yaxshi kitob do'st' -> Chiqish: 'kitob' (2 marta)
```


# 181-Topshiriq: Matndan butun sonlarni ajratib olish

## Topshiriq sharti:
Matn ichidagi alohida ko'p xonali butun sonlarni ro'yxat shaklida ajratib oling.

## Yechim (Python kodi):
```python
import re

matn = input("Matn kiriting: ")

# \d+ bir yoki undan ortiq raqamlar ketma-ketligini topadi
sonlar = [int(x) for x in re.findall(r'\d+', matn)]

print(f"Matndagi sonlar: {sonlar}")
```

## Tushuntirish va Mantiq:
1. `re.findall(r'\d+', matn)` barcha butun sonlarni alohida qilib ro'yxatga oladi.

## Ishlash natijasi:
```text
Kiritish: 'Bugun 15 ta talaba 120 ta misol yechdi' -> Chiqish: [15, 120]
```


# 182-Topshiriq: IPv4 manzilining to'g'riligini tekshirish

## Topshiriq sharti:
Kiritilgan satr to'g'ri IPv4 manzili (nuqta bilan ajratilgan 4 ta 0-255 oraliqdagi son) ekanligini aniqlang.

## Yechim (Python kodi):
```python
ip = input("IP manzilini kiriting: ").strip()

bolaklar = ip.split('.')
tugri = True

if len(bolaklar) != 4:
    tugri = False
else:
    for b in bolaklar:
        if not b.isdigit():
            tugri = False
            break
        val = int(b)
        # 0 dan 255 gacha bo'lishi va ortiqcha boshdagi 0 bo'lmasligi kerak (masalan '01' xato)
        if val < 0 or val > 255 or (len(b) > 1 and b[0] == '0'):
            tugri = False
            break

if tugri:
    print(f"'{ip}' — TO'G'RI IPv4 manzili.")
else:
    print(f"'{ip}' — NOTO'G'RI IP manzili!")
```

## Tushuntirish va Mantiq:
1. IP 4 ta qismdan iborat bo'lishi shart.
2. Har bir qism 0-255 oraliqda bo'lishi va '01' kabi yetakchi nollarga ega bo'lmasligi lozim.

## Ishlash natijasi:
```text
Kiritish: '192.168.1.1' -> Chiqish: TO'G'RI! / Kiritish: '256.100.0.1' -> Chiqish: NOTO'G'RI!
```


# 183-Topshiriq: Satrni split() metodisiz bo'laklarga ajratish

## Topshiriq sharti:
Satrni berilgan ajratkich (masalan, vergul) bo'yicha tayyor `split()`siz, tsikl orqali bo'laklang.

## Yechim (Python kodi):
```python
matn = input("Satr kiriting: ")
ajratkich = input("Ajratuvchi belgi: ")

natija = []
joriy = ""

for ch in matn:
    if ch == ajratkich:
        natija.append(joriy)
        joriy = ""
    else:
        joriy += ch
natija.append(joriy)

print(f"Bo'lingan ro'yxat: {natija}")
```

## Tushuntirish va Mantiq:
1. Har bir belgi joriy bo'lakka qo'shiladi.
2. Ajratuvchi belgi uchraganda, joriy bo'lak ro'yxatga kiritilib, bo'shatiladi.

## Ishlash natijasi:
```text
Kiritish: 'olma,anor,uzum', ajratkich=',' -> Chiqish: ['olma', 'anor', 'uzum']
```


# 184-Topshiriq: Fayl yo'lidan nom va kengaytmani ajratish

## Topshiriq sharti:
To'liq fayl yo'lidan fayl nomi, uning kengaytmasi va papkasini ajrating.

## Yechim (Python kodi):
```python
import os

fayl_yoli = r"C:\Users\User\Documents\hisobot_2026.pdf"

papka = os.path.dirname(fayl_yoli)
fayl_nomi_toliq = os.path.basename(fayl_yoli)
nom, kengaytma = os.path.splitext(fayl_nomi_toliq)

print(f"Papka yo'li : {papka}")
print(f"Fayl nomi   : {nom}")
print(f"Kengaytmasi : {kengaytma}")
```

## Tushuntirish va Mantiq:
1. `os.path.basename()` faylning to'liq nomini oladi.
2. `os.path.splitext()` kengaytmani ajratadi.

## Ishlash natijasi:
```text
Chiqish: Nom: hisobot_2026, Kengaytma: .pdf
```


# 185-Topshiriq: Lotin matnini Morze kodiga o'tkazish

## Topshiriq sharti:
Matndagi harflarni xalqaro Morze alifbosi signallariga (nuqta va chiziqchalar) o'giring.

## Yechim (Python kodi):
```python
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ' ': '/'
}

matn = input("Matn kiriting: ").upper()
morze = [MORSE_CODE_DICT.get(ch, '') for ch in matn]

print("Morze kodi:", " ".join(morze))
```

## Tushuntirish va Mantiq:
1. Har bir harf lug'atdagi signallarga almashtiriladi.
2. So'zlar orasidagi bo'shliq `/` belgisi bilan ifodalanadi.

## Ishlash natijasi:
```text
Kiritish: 'SOS' -> Chiqish: '... --- ...'
```


# 186-Topshiriq: Morze kodini matnga o'girish

## Topshiriq sharti:
Nuqta va chiziqchalardan iborat Morze kodini qaytadan o'qiladigan matnga aylantiring.

## Yechim (Python kodi):
```python
MORSE_TO_CHAR = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '/': ' '
}

morze = input("Morze kodini kiriting (bo'shliq bilan): ")
belgilar = morze.split()
matn = "".join(MORSE_TO_CHAR.get(b, '') for b in belgilar)

print(f"Deshifrlangan matn: {matn}")
```

## Tushuntirish va Mantiq:
1. Teskari lug'at yordamida signallar harflarga tiklanadi.

## Ishlash natijasi:
```text
Kiritish: '... --- ...' -> Chiqish: 'SOS'
```


# 187-Topshiriq: O'zbek so'zining bo'g'inlar sonini hisoblash

## Topshiriq sharti:
O'zbek tilida so'zdagi bo'g'inlar soni unli harflar soniga teng degan qoidaga asosan bo'g'inlar sonini toping.

## Yechim (Python kodi):
```python
soz = input("So'z kiriting: ").lower()

unlilar = "aeiouo'oʻ"
bogin_soni = sum(1 for ch in soz if ch in unlilar)

print(f"'{soz}' so'zida {bogin_soni} ta bo'g'in bor.")
```

## Tushuntirish va Mantiq:
1. O'zbek tili fonetikasida har bir bo'g'in asosini unli tovush tashkil etadi.

## Ishlash natijasi:
```text
Kiritish: 'Dasturchilar' -> Chiqish: 4 ta bo'g'in
```


# 188-Topshiriq: Matndan barcha akronimlarni (qisqartmalarni) ajratish

## Topshiriq sharti:
Matn ichidagi kamida 2 ta bosh harfdan iborat qisqartmalarni (masalan: OAV, BMT, AQSH, IT) ajratib oling.

## Yechim (Python kodi):
```python
import re

matn = input("Matn kiriting: ")

# \b[A-Z]{2,}\b kamida 2 ta bosh harfli mustaqil so'zlarni topadi
akronimlar = re.findall(r'[A-Z]{2,}', matn)

print(f"Topilgan akronimlar: {akronimlar}")
```

## Tushuntirish va Mantiq:
1. `[A-Z]{2,}` faqat bosh harflardan tuzilgan so'zlarni qidiradi.

## Ishlash natijasi:
```text
Kiritish: 'BMT va OAV vakillari IT sohasini muhokama qildi' -> Chiqish: ['BMT', 'OAV', 'IT']
```


# 189-Topshiriq: Matndan barcha URL havolalarini topish

## Topshiriq sharti:
Matn ichidagi 'http://' yoki 'https://' bilan boshlanadigan veb-sayt havolalarini toping.

## Yechim (Python kodi):
```python
import re

matn = input("Matn kiriting: ")

andoza = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
havolalar = re.findall(andoza, matn)

print(f"Topilgan havolalar ({len(havolalar)} ta):")
for h in havolalar:
    print(f" - {h}")
```

## Tushuntirish va Mantiq:
1. `https?` ham http, ham https ni qamrab oladi.
2. `[^\s<>"]+` bo'shliq yoki qavsgacha bo'lgan to'liq URL manzilini oladi.

## Ishlash natijasi:
```text
Kiritish: 'Batafsil https://kun.uz yoki https://ziyouz.com saytida' -> Chiqish: 2 ta havola
```


# 190-Topshiriq: 'H' va 'X' harflari statistikasi

## Topshiriq sharti:
Matnda 'h' va 'x' harflarining necha marta uchrashini hisoblab, taqqoslang.

## Yechim (Python kodi):
```python
matn = input("Matn kiriting: ").lower()

h_soni = matn.count('h')
x_soni = matn.count('x')

print(f"'H' harfi: {h_soni} marta")
print(f"'X' harfi: {x_soni} marta")
```

## Tushuntirish va Mantiq:
1. `.count()` satrdagi belgi sonini tezkor hisoblaydi.

## Ishlash natijasi:
```text
Kiritish: 'xushxabar va halovat' -> H: 2, X: 2
```


# 191-Topshiriq: Matnni gaplarga ajratish

## Topshiriq sharti:
Matnni nuqta, so'roq va undov belgilari bo'yicha toza gaplarga ajrating.

## Yechim (Python kodi):
```python
import re

matn = input("Matn kiriting: ")

# [.!?]+ tinish belgilari bo'yicha bo'lamiz
gaplar = [g.strip() for g in re.split(r'[.!?]+', matn) if g.strip()]

print(f"Jami {len(gaplar)} ta gap topildi:")
for i, g in enumerate(gaplar, 1):
    print(f"{i}. {g}")
```

## Tushuntirish va Mantiq:
1. `re.split()` bir nechta har xil tinish belgilari bo'yicha bo'lish imkonini beradi.

## Ishlash natijasi:
```text
Kiritish: 'Salom! Qandaysiz? Men yaxshiman.' -> Chiqish: 3 ta alohida gap
```


# 192-Topshiriq: Matnni o'qish vaqtini baholash (WPM)

## Topshiriq sharti:
Inson o'rtacha daqiqasiga 200 ta so'z o'qiydi deb hisoblab, matnni o'qish uchun ketadigan vaqtni hisoblang.

## Yechim (Python kodi):
```python
matn = input("Matn kiriting: ")

sozlar_soni = len(matn.split())
wpm = 200  # Words Per Minute

daqiqalar = sozlar_soni / wpm
soniyalar = int(daqiqalar * 60)

print(f"So'zlar soni: {sozlar_soni} ta")
print(f"Taxminiy o'qish vaqti: {soniyalar // 60} daqiqa {soniyalar % 60} soniya")
```

## Tushuntirish va Mantiq:
1. WPM (Words Per Minute) jahon standartlarida tezlik o'lchovi hisoblanadi.

## Ishlash natijasi:
```text
Kiritish: 300 ta so'z -> Chiqish: 1 daqiqa 30 soniya
```


# 193-Topshiriq: Harflarning alifbodagi o'rni bo'yicha kodlash

## Topshiriq sharti:
Har bir lotin harfini uning alifbodagi o'rni bo'yicha songa aylantiring (A=1, B=2 ... Z=26).

## Yechim (Python kodi):
```python
matn = input("Lotin matn kiriting: ").upper()

kodlar = []
for ch in matn:
    if 'A' <= ch <= 'Z':
        kodlar.append(str(ord(ch) - ord('A') + 1))

print("Kodlangan sonlar:", " ".join(kodlar))
```

## Tushuntirish va Mantiq:
1. `ord(ch) - ord('A') + 1` formulasi A uchun 1, B uchun 2 va hk. beradi.

## Ishlash natijasi:
```text
Kiritish: 'CAB' -> Chiqish: '3 1 2'
```


# 194-Topshiriq: ROT13 shifrlash algoritmi

## Topshiriq sharti:
Matndagi har bir harfni alifboda 13 ta o'rin oldinga suruvchi klassik ROT13 shifrlashini amalga oshiring.

## Yechim (Python kodi):
```python
import codecs

matn = input("Matn kiriting: ")
rot13_shifr = codecs.encode(matn, 'rot_13')

print(f"Shifrlangan: {rot13_shifr}")
# ROT13 o'ziga o'zi teskari: qayta qo'llash asl matnni beradi
tiklangan = codecs.encode(rot13_shifr, 'rot_13')
print(f"Qayta tiklangan: {tiklangan}")
```

## Tushuntirish va Mantiq:
1. Alifbo 26 ta harfdan iborat bo'lgani sababli, 13 ta surish shifrlash va deshifrlashni aynan bir xil qiladi.

## Ishlash natijasi:
```text
Kiritish: 'Hello' -> Chiqish: 'Uryyb'
```


# 195-Topshiriq: Satrni markazlashtirish (Center Alignment)

## Topshiriq sharti:
Satrni berilgan kenglikda yonlariga belgi (masalan, '=') qo'yib markazga tekislang.

## Yechim (Python kodi):
```python
sarlavha = input("Sarlavha kiriting: ").strip()
kenglik = 40

markazlashgan = sarlavha.center(kenglik, "=")
print(markazlashgan)
```

## Tushuntirish va Mantiq:
1. `.center(kenglik, belgi)` metodi matnni o'rtaga joylashtirib, ikki yonini ko'rsatilgan belgi bilan to'ldiradi.

## Ishlash natijasi:
```text
Kiritish: 'PYTHON', 30 -> Chiqish: '============PYTHON============'
```


# 196-Topshiriq: Prefiks va suffiks tekshirish

## Topshiriq sharti:
Fayl nomi '.py' bilan tugashi va 'test_' bilan boshlanishini tekshiring.

## Yechim (Python kodi):
```python
fayl = input("Fayl nomini kiriting: ").strip()

boshlanadi = fayl.startswith("test_")
tugaydi = fayl.endswith(".py")

if boshlanadi and tugaydi:
    print(f"'{fayl}' — Python test fayli!")
else:
    print(f"Mos kelmaydi (Boshlanishi: {boshlanadi}, Tugashi: {tugaydi})")
```

## Tushuntirish va Mantiq:
1. `.startswith()` va `.endswith()` satr boshi va oxirini juda tez tekshiradi.

## Ishlash natijasi:
```text
Kiritish: 'test_main.py' -> Chiqish: Python test fayli!
```


# 197-Topshiriq: Pul summalarini xonalar bo'yicha chiroyli formatlash

## Topshiriq sharti:
Katta sonni (masalan: 1250000000) o'qish oson bo'lishi uchun bo'shliqlar bilan '1 250 000 000 so'm' qilib chiqaring.

## Yechim (Python kodi):
```python
summa = int(input("Summani kiriting: "))

formatlangan = f"{summa:,}".replace(",", " ")
print(f"Formatlangan: {formatlangan} so'm")
```

## Tushuntirish va Mantiq:
1. `{summa:,}` raqamlarni mingliklar bo'yicha vergul bilan ajratadi.
2. `.replace(',', ' ')` uni o'zbek milliy standartidagi bo'shliqqa almashtiradi.

## Ishlash natijasi:
```text
Kiritish: 15000000 -> Chiqish: '15 000 000 so'm'
```


# 198-Topshiriq: Matndan barcha @foydalanuvchi nomlarini ajratish

## Topshiriq sharti:
Ijtimoiy tarmoq matnidan barcha '@username' ko'rinishidagi eslatmalarni (mentions) ajratib oling.

## Yechim (Python kodi):
```python
import re

post = input("Post matnini kiriting: ")

foydalanuvchilar = re.findall(r'@([a-zA-Z0-9_]+)', post)

print(f"Eslatilgan foydalanuvchilar: {foydalanuvchilar}")
```

## Tushuntirish va Mantiq:
1. `@([a-zA-Z0-9_]+)` @ belgisidan keyingi harf, raqam va pastki chiziqdan iborat nomni ajratadi.

## Ishlash natijasi:
```text
Kiritish: 'Salom @anvar va @dilnoza_99!' -> Chiqish: ['anvar', 'dilnoza_99']
```


# 199-Topshiriq: Matndan barcha #heshteglarni ajratish

## Topshiriq sharti:
Matn ichidagi barcha '#teg' ko'rinishidagi heshteglarni ro'yxatga oling.

## Yechim (Python kodi):
```python
import re

matn = input("Post matnini kiriting: ")

heshteglar = re.findall(r'#([a-zA-Z0-9_]+)', matn)

print(f"Topilgan heshteglar: {heshteglar}")
```

## Tushuntirish va Mantiq:
1. `#` bilan boshlanuvchi barcha kalit so'zlar ajratiladi.

## Ishlash natijasi:
```text
Kiritish: 'Bugun #python va #dasturlash o'rgandik' -> Chiqish: ['python', 'dasturlash']
```


# 200-Topshiriq: Matnning to'liq statistikasi hisoblagichi

## Topshiriq sharti:
Kiritilgan matndagi belgilar, bo'shliqsiz belgilar, so'zlar, qatorlar, unli va undosh harflar sonini hisoblovchi to'liq tahlil dasturi.

## Yechim (Python kodi):
```python
matn = '''O'zbekiston — kelajagi buyuk davlat.
Bu yerda ilm-fan va sun'iy intellekt jadal rivojlanmoqda.
Dasturchilar soni kundan-kunga ortib bormoqda.'''

jami_belgi = len(matn)
boshliqsiz = len(matn.replace(" ", "").replace("\n", ""))
qatorlar = len(matn.splitlines())
sozlar = len(matn.split())

unlilar = "aeiouo'oʻ"
unli_soni = sum(1 for ch in matn.lower() if ch in unlilar)
harflar = sum(1 for ch in matn if ch.isalpha())
undosh_soni = harflar - unli_soni

print("========== MATN STATISTIKASI ==========")
print(f"Qatorlar soni       : {qatorlar}")
print(f"So'zlar soni        : {sozlar}")
print(f"Jami belgilar soni  : {jami_belgi}")
print(f"Bo'shliqsiz belgilar: {boshliqsiz}")
print(f"Unli harflar soni   : {unli_soni}")
print(f"Undosh harflar soni : {undosh_soni}")
print("=======================================")
```

## Tushuntirish va Mantiq:
1. `splitlines()` matndagi qatorlar sonini aniqlaydi.
2. `split()` so'zlar sonini beradi.
3. Barcha parametrlar hisoblanib, professional konsol hisoboti taqdim etiladi.

## Ishlash natijasi:
```text
Chiqish: Matnning barcha parametrlarini o'z ichiga olgan to'liq statistika jadvali.
```

