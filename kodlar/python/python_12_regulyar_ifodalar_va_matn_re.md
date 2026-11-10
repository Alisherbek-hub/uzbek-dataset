# Python Dasturlash Tili — 12-Qism: Regulyar Ifodalar (Regex re) va Matn Tahlili (NLP)
## (551-600 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam matnlar bilan professional ishlash, shablonli qidiruv va NLP tahlilini qamrab oladi:
* `re` modulining asosiy funksiyalari: `search`, `match`, `findall`, `finditer`, `sub`, `split`;
* Shablon elementlari, guruhlash (`(...)`), nomlangan guruhlar (`?P<nom>`);
* Ochko'z (Greedy) va dangasa (Lazy) qidiruvlar, Lookahead va Lookbehind tekshiruvlari;
* Bayroqlar: `re.IGNORECASE`, `re.MULTILINE`, `re.DOTALL`, `re.VERBOSE`;
* Amaliy matn muhandisligi: Levenshteyn masofasi, TF-IDF, N-grammalar, Jaccard o'xshashligi, Tokenizatsiya va tozalash quvurlari;

---

# 551-Topshiriq: re moduli va re.search() asoslari

## Topshiriq sharti:
Berilgan matnda 'Python' so'zi bor-yo'qligini re.search() yordamida aniqlang va topilgan indekslarni chiqaring.

## Yechim (Python kodi):
```python
import re

matn = "Bugungi kunda Python sun'iy intellektda yetakchi dasturlash tilidir."
moslik = re.search(r"Python", matn)

if moslik:
    print("Topildi:", moslik.group())
    print("Boshlanish indeksi:", moslik.start())
    print("Tugash indeksi:", moslik.end())
    print("Oraliq:", moslik.span())
else:
    print("Topilmadi.")
```

## Tushuntirish va Mantiq:
1. `re.search()` butun matn bo'ylab qidiradi va birinchi mos kelgan ob'ektni (`Match`) qaytaradi.
2. `moslik.group()` mos kelgan qism-satrni, `start()` va `end()` uning pozitsiyalarini ko'rsatadi.

## Ishlash natijasi:
```text
Chiqish: Topildi: Python, Boshlanish indeksi: 14, Tugash indeksi: 20, Oraliq: (14, 20)
```

---

# 552-Topshiriq: re.match() bilan satr boshini tekshirish

## Topshiriq sharti:
Satr aynan berilgan kalit so'z bilan boshlanganligini re.match() orqali tekshiring.

## Yechim (Python kodi):
```python
import re

def boshlanishini_tekshir(satr, namuna):
    moslik = re.match(namuna, satr)
    return bool(moslik)

print(boshlanishini_tekshir("AI texnologiyalari juda tez rivojlanmoqda", r"^AI"))
print(boshlanishini_tekshir("Bugun AI darsi bo'ladi", r"^AI"))
print(boshlanishini_tekshir("Python va AI", r"^AI"))
```

## Tushuntirish va Mantiq:
1. `re.match()` har doim satrning eng boshidan moslikni tekshiradi (boshida bo'lmasa, `None` qaytaradi).

## Ishlash natijasi:
```text
Chiqish: True, False, False
```

---

# 553-Topshiriq: re.findall() bilan barcha raqamlarni ajratib olish

## Topshiriq sharti:
Matn ichidagi barcha ketma-ket kelgan raqamlarni ro'yxat ko'rinishida ajratib oling.

## Yechim (Python kodi):
```python
import re

matn = "Buyurtma raqami: #48291, narxi: 150000 so'm, chegirma: 25000 so'm, sana: 2026-yil."
raqamlar = re.findall(r"\d+", matn)
print("Topilgan barcha raqamlar:", raqamlar)
```

## Tushuntirish va Mantiq:
1. `\d+` belgisi 1 yoki undan ortiq ketma-ket kelgan raqamli belgilarni anglatadi.
2. `re.findall()` barcha mosliklarni satrlar ro'yxati shaklida qaytaradi.

## Ishlash natijasi:
```text
Chiqish: Topilgan barcha raqamlar: ['48291', '150000', '25000', '2026']
```

---

# 554-Topshiriq: re.finditer() bilan iterator orqali mosliklarni ko'rish

## Topshiriq sharti:
Matndan barcha 4 xonali yillarni re.finditer() orqali topib, har birining boshlanish va tugash o'rnini chiqaring.

## Yechim (Python kodi):
```python
import re

matn = "O'zbekiston 1991-yilda mustaqillikka erishgan. 2026-yil esa yangi davr boshidir. 1997-yilda..."
for moslik in re.finditer(r"\b\d{4}\b", matn):
    print(f"Yil: {moslik.group()} (Indekslar: {moslik.start()}-{moslik.end()})")
```

## Tushuntirish va Mantiq:
1. `\b` so'z chegarasi (word boundary) hisoblanadi.
2. `re.finditer()` xotirani tejash uchun generator/iterator qaytaradi va har bir `Match` ob'ektini alohida taqdim etadi.

## Ishlash natijasi:
```text
Chiqish: Yil: 1991 (Indekslar: 12-16), Yil: 2026 (Indekslar: 46-50), Yil: 1997 (Indekslar: 73-77)
```

---

# 555-Topshiriq: re.sub() bilan so'zlarni almashtirish va senzura

## Topshiriq sharti:
Matndagi taqiqlangan so'zlarni yulduzchalar ('***') bilan almashtiring.

## Yechim (Python kodi):
```python
import re

matn = "Bu tizimda spam va virus so'zlarini ishlatish qat'iyan man etiladi. Spam xabarlar..."
taqiqlangan_pattern = r"(?i)\b(spam|virus)\b"
tozalangan = re.sub(taqiqlangan_pattern, "***", matn)
print("Senzuralangan matn:", tozalangan)
```

## Tushuntirish va Mantiq:
1. `re.sub(pattern, replacement, string)` mos kelgan hamma qismlarni yangi qiymat bilan almashtiradi.
2. `(?i)` bayrog'i katta-kichik harflarni farqlamaydi (case-insensitive).

## Ishlash natijasi:
```text
Chiqish: Senzuralangan matn: Bu tizimda *** va *** so'zlarini ishlatish qat'iyan man etiladi. *** xabarlar...
```

---

# 556-Topshiriq: re.split() yordamida bir nechta ajratuvchilar bilan bo'lish

## Topshiriq sharti:
Matnni vergul, nuqta, nuqta-vergul va bo'shliqlar bo'yicha so'zlarga ajrating.

## Yechim (Python kodi):
```python
import re

matn = "olma,nok;anor. shaftoli, uzum;   o'rik"
bolaklar = re.split(r"[,;.\s]+", matn.strip())
print("So'zlar ro'yxati:", bolaklar)
```

## Tushuntirish va Mantiq:
1. `[,;.\s]+` belgilar sinfi (character class) vergul, nuqta-vergul, nuqta yoki bo'shliqlarning bir yoki undan ortig'ini birlashtirib bitta bo'luvchi sifatida qabul qiladi.

## Ishlash natijasi:
```text
Chiqish: So'zlar ro'yxati: ['olma', 'nok', 'anor', 'shaftoli', 'uzum', "o'rik"]
```

---

# 557-Topshiriq: re.compile() bilan shablonni qayta ishlatish (Kesh va samaradorlik)

## Topshiriq sharti:
Tez-tez ishlatiladigan regex shablonini re.compile() orqali kompyutatsiya qilib saqlang.

## Yechim (Python kodi):
```python
import re

email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

namunalar = ["ali@gmail.com", "not_an_email", "toshmat@edu.uz", "invalid@.com"]
for email in namunalar:
    holat = "To'g'ri" if email_regex.match(email) else "Noto'g'ri"
    print(f"{email}: {holat}")
```

## Tushuntirish va Mantiq:
1. Agar bitta shablon ko'p marta ishlatilsa, `re.compile()` uni bayt-kodga o'girib xotirada saqlaydi, bu esa qidirish tezligini sezilarli darajada oshiradi.

## Ishlash natijasi:
```text
Chiqish: ali@gmail.com: To'g'ri, not_an_email: Noto'g'ri, toshmat@edu.uz: To'g'ri, invalid@.com: Noto'g'ri
```

---

# 558-Topshiriq: O'zbekiston telefon raqamlari formatini tekshirish (+998)

## Topshiriq sharti:
O'zbekiston mobil telefon raqamlari (+998 XX XXX XX XX) formatini tasdiqlovchi qat'iy regex yozing.

## Yechim (Python kodi):
```python
import re

tel_pattern = re.compile(r"^\+998[ -]?(9[01345789]|33|88|77)[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$")

testlar = ["+998901234567", "+998 90 123 45 67", "+998-99-987-65-43", "+998121234567", "+123456789"]
for t in testlar:
    print(f"{t} -> {'Mos' if tel_pattern.match(t) else 'Nomas'}")
```

## Tushuntirish va Mantiq:
1. Guruh `(9[01345789]|33|88|77)` O'zbekiston aloqa operatorlari (Beeline, Ucell, Mobiuz, Uzmobile, Humans) prefikslarini tekshiradi.

## Ishlash natijasi:
```text
Chiqish: +998901234567 -> Mos, +998 90 123 45 67 -> Mos, +998-99-987-65-43 -> Mos, +998121234567 -> Nomas, +123456789 -> Nomas
```

---

# 559-Topshiriq: Guruhlash (Groups) va guruh qiymatlarini olish

## Topshiriq sharti:
Sana formatidagi satrdan (YYYY-MM-DD) yil, oy va kunni alohida guruhlarga ajrating.

## Yechim (Python kodi):
```python
import re

sana = "2026-11-07"
moslik = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", sana)
if moslik:
    yil, oy, kun = moslik.groups()
    print(f"Yil: {yil}, Oy: {oy}, Kun: {kun}")
    print(f"1-guruh: {moslik.group(1)}, 2-guruh: {moslik.group(2)}")
```

## Tushuntirish va Mantiq:
1. Qavslar `(...)` qidiruv shablonida guruhlarni hosil qiladi.
2. `moslik.groups()` barcha guruh qiymatlarini tuple sifatida qaytaradi.

## Ishlash natijasi:
```text
Chiqish: Yil: 2026, Oy: 11, Kun: 07, 1-guruh: 2026, 2-guruh: 11
```

---

# 560-Topshiriq: Nomlangan guruhlar (?P<nom>pattern)

## Topshiriq sharti:
URL manzilidan protokol, domen va yo'lni nomlangan guruhlar (Named Groups) orqali ajrating.

## Yechim (Python kodi):
```python
import re

url = "https://kun.uz/news/2026/texnologiyalar"
pattern = r"^(?P<protokol>https?)://(?P<domen>[^/]+)(?P<path>/.*)?$"

m = re.match(pattern, url)
if m:
    malumot = m.groupdict()
    print("Domen:", malumot['domen'])
    print("Protokol:", malumot['protokol'])
    print("Yo'l:", malumot['path'])
```

## Tushuntirish va Mantiq:
1. `(?P<nom>...)` sintaksisi har bir guruhga kalit so'z nomi biriktiradi.
2. `m.groupdict()` guruhlarni lug'at (dict) ko'rinishida beradi.

## Ishlash natijasi:
```text
Chiqish: Domen: kun.uz, Protokol: https, Yo'l: /news/2026/texnologiyalar
```

---

# 561-Topshiriq: Ochko'z (Greedy) va Qanoatli (Non-greedy / Lazy) qidiruv

## Topshiriq sharti:
HTML teglari orasidagi matnni greedy va lazy usullarda ajratib solishtiring.

## Yechim (Python kodi):
```python
import re

html = "<div>Birinchi</div><div>Ikkinchi</div>"

# Greedy (ochko'z)
greedy_m = re.findall(r"<div>.*</div>", html)
# Lazy (dangasa/qanoatli)
lazy_m = re.findall(r"<div>.*?</div>", html)

print("Greedy natijasi:", greedy_m)
print("Lazy natijasi:", lazy_m)
```

## Tushuntirish va Mantiq:
1. Standart `.*` imkon qadar ko'p belgilarni qamrab oladi (oxirgi `</div>` gacha).
2. `.*?` so'roq belgisi bilan birinchi uchragan `</div>` da to'xtaydi.

## Ishlash natijasi:
```text
Chiqish: Greedy natijasi: ['<div>Birinchi</div><div>Ikkinchi</div>'], Lazy natijasi: ['<div>Birinchi</div>', '<div>Ikkinchi</div>']
```

---

# 562-Topshiriq: Matndagi barcha URL manzillarni ajratib olish

## Topshiriq sharti:
Katta matndan barcha http va https havolalarni regex orqali ajrating.

## Yechim (Python kodi):
```python
import re

matn = "Batafsil ma'lumot https://ziyouz.com saytida yoki http://edu.gov.uz portalida berilgan."
havolalar = re.findall(r"https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9_.-]*)*", matn)
print("Havolalar:", havolalar)
```

## Tushuntirish va Mantiq:
1. `(?:...)` belgilanmagan guruh (non-capturing group) bo'lib, xotirada alohida saqlanmaydi va faqat mantiqiy guruhlash uchun xizmat qiladi.

## Ishlash natijasi:
```text
Chiqish: Havolalar: ['https://ziyouz.com', 'http://edu.gov.uz']
```

---

# 563-Topshiriq: re.sub() ichida funksiya chaqirish (replacing with a callback)

## Topshiriq sharti:
Matndagi barcha narxlarni dollar kursiga ($1 = 12,800 so'm) ko'paytirib so'mga aylantiring.

## Yechim (Python kodi):
```python
import re

matn = "Monitor narxi $250, klaviatura esa $35 turadi."

def dollarni_somga(match):
    dollar = int(match.group(1))
    som = dollar * 12800
    return f"{som:,} so'm"

yangi_matn = re.sub(r"\$(\d+)", dollarni_somga, matn)
print("Yangi matn:", yangi_matn)
```

## Tushuntirish va Mantiq:
1. `re.sub()` ning 2-argumentiga funksiya uzatilsa, har bir moslik uchun shu funksiya chaqiriladi va qaytargan satr joylashtiriladi.

## Ishlash natijasi:
```text
Chiqish: Yangi matn: Monitor narxi 3,200,000 so'm, klaviatura esa 448,000 so'm turadi.
```

---

# 564-Topshiriq: Ortiqcha bo'shliqlar va yangi qatorlarni tozalash (Text Normalization)

## Topshiriq sharti:
Matndagi ketma-ket kelgan bir nechta bo'shliqlar, tabulyatsiyalar va bo'sh qatorlarni tozalang.

## Yechim (Python kodi):
```python
import re

matn = """Bu     matn    juda       tartibsiz.
   
   Unda   ko'p     bo'shliqlar    bor.


Oxirgi qator."""

# Bir nechta bo'shliqlarni bitta bo'shliqqa aylantirish
matn_1 = re.sub(r"[ \t]+", " ", matn)
# 3 va undan ortiq yangi qatorlarni 2 tasiga qisqartirish
matn_toza = re.sub(r"\n\s*\n", "\n\n", matn_1).strip()
print(matn_toza)
```

## Tushuntirish va Mantiq:
1. Matnlarni tozalash (NLP Preprocessing) jarayonida regex eng asosiy vositadir.

## Ishlash natijasi:
```text
Chiqish: Bu matn juda tartibsiz.\n\nUnda ko'p bo'shliqlar bor.\n\nOxirgi qator.
```

---

# 565-Topshiriq: Lookahead Assertions (?=...) — Oldinga qarab tekshirish

## Topshiriq sharti:
Matndan faqat orqasidan 'so'm' so'zi kelgan sonlarni ajrating, lekin 'so'm' so'zining o'zini natijaga qo'shmang.

## Yechim (Python kodi):
```python
import re

matn = "Non 4000 so'm, go'sht 95000 so'm, vazni 2 kg, xodimlar 15 kishi."
narxlar = re.findall(r"\d+(?=\s*so'm)", matn)
print("Topilgan narxlar:", narxlar)
```

## Tushuntirish va Mantiq:
1. `(?=...)` musbat oldindan ko'rish (Positive Lookahead). U shart bajarilishini talab qiladi, ammo natijaviy satrga belgini kiritmaydi.

## Ishlash natijasi:
```text
Chiqish: Topilgan narxlar: ['4000', '95000']
```

---

# 566-Topshiriq: Lookbehind Assertions (?<=...) — Orqaga qarab tekshirish

## Topshiriq sharti:
Faqat oldida '$' belgisi bo'lgan sonlarni ajratib oling.

## Yechim (Python kodi):
```python
import re

matn = "Telefon $300, noutbuk $1200, yetkazib berish 50000 so'm."
dollar_qiymatlari = re.findall(r"(?<=\$)\d+", matn)
print("Dollar qiymatlari:", dollar_qiymatlari)
```

## Tushuntirish va Mantiq:
1. `(?<=...)` musbat orqaga ko'rish (Positive Lookbehind). U belgi oldida moslik borligini tekshiradi va belgi o'zini o'tkazib yuboradi.

## Ishlash natijasi:
```text
Chiqish: Dollar qiymatlari: ['300', '1200']
```

---

# 567-Topshiriq: Salbiy tekshiruvlar: Negative Lookahead (?!...) va Negative Lookbehind (?<!...)

## Topshiriq sharti:
Oldida '$' bo'lmagan va orqasidan 'so'm' kelmagan sof raqamlarni ajrating.

## Yechim (Python kodi):
```python
import re

matn = "10 ta olma, $20 to'lov, 5000 so'm ijara, 42 soni."
natija = re.findall(r"(?<!\$)\b\d+\b(?!\s*so'm)", matn)
print("Mustaqil raqamlar:", natija)
```

## Tushuntirish va Mantiq:
1. `(?!...)` va `(?<!...)` shartlar qanoatlanmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Chiqish: Mustaqil raqamlar: ['10', '42']
```

---

# 568-Topshiriq: O'zbekcha 'tututq belgisi' va o'ziga xos harflarni ushlash

## Topshiriq sharti:
O'zbek tilidagi tutuq belgili (masalan, san'at, ma'rifat, a'lo) so'zlarni ajrating.

## Yechim (Python kodi):
```python
import re

matn = "O'zbek san'ati va ma'naviyati yuksak, a'lo darajadagi ta'lim tizimi."
tutuqli_sozlar = re.findall(r"\b[a-zA-Z]+['`’][a-zA-Z]+\b", matn)
print("Tutuq belgili so'zlar:", tutuqli_sozlar)
```

## Tushuntirish va Mantiq:
1. O'zbek tili lotin imlosida apostrof belgisi bir necha xil (`'`, `` ` ``, `’`) bo'lishi mumkin. Ularni belgilar sinfida qamrab olish lozim.

## Ishlash natijasi:
```text
Chiqish: Tutuq belgili so'zlar: ["san'ati", "ma'naviyati", "a'lo", "ta'lim"]
```

---

# 569-Topshiriq: Takrorlangan so'zlarni (Double Words) aniqlash va o'chirish

## Topshiriq sharti:
Matndagi xatolik bilan ketma-ket yozilib qolgan bir xil so'zlarni (masalan: 'bu bu') aniqlang.

## Yechim (Python kodi):
```python
import re

matn = "Bugun bugun biz biz yangi yangi texnologiyalar haqida gaplashamiz."
tozalangan = re.sub(r"\b(\w+)\s+\1\b", r"\1", matn, flags=re.IGNORECASE)
print("Tozalangan matn:", tozalangan)
```

## Tushuntirish va Mantiq:
1. `\1` orqaga havola (Backreference) bo'lib, 1-guruhda ushlangan so'zni aynan takrorlashni tekshiradi.

## Ishlash natijasi:
```text
Chiqish: Tozalangan matn: Bugun biz yangi texnologiyalar haqida gaplashamiz.
```

---

# 570-Topshiriq: IP-manzillarni (IPv4) validatsiya qilish

## Topshiriq sharti:
Satr to'g'ri IPv4 manzil (0.0.0.0 dan 255.255.255.255 gacha) ekanligini tasdiqlang.

## Yechim (Python kodi):
```python
import re

def ip_tekshir(ip):
    qism = r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"
    pattern = rf"^{qism}\.{qism}\.{qism}\.{qism}$"
    return bool(re.match(pattern, ip))

print("192.168.1.1 ->", ip_tekshir("192.168.1.1"))
print("255.255.255.255 ->", ip_tekshir("255.255.255.255"))
print("256.100.0.1 ->", ip_tekshir("256.100.0.1"))
print("192.168.1 ->", ip_tekshir("192.168.1"))
```

## Tushuntirish va Mantiq:
1. `25[0-5]` 250-255 oralig'ini, `2[0-4][0-9]` 200-249 oralig'ini qamrab oladi.

## Ishlash natijasi:
```text
Chiqish: 192.168.1.1 -> True, 255.255.255.255 -> True, 256.100.0.1 -> False, 192.168.1 -> False
```

---

# 571-Topshiriq: Kredit karta raqamlarini niqoblash (Masking)

## Topshiriq sharti:
16 xonali karta raqamining dastlabki 6 va oxirgi 4 xonasini qoldirib, o'rtasini '******' bilan almashtiring.

## Yechim (Python kodi):
```python
import re

def kartani_niqobla(karta_raqami):
    pattern = r"^(\d{4})[ -]?(\d{2})\d{2}[ -]?\d{4}[ -]?(\d{4})$"
    return re.sub(pattern, r"\1 \2** **** \3", karta_raqami)

print(kartani_niqobla("8600 1234 5678 9012"))
print(kartani_niqobla("9860-0123-4567-8901"))
```

## Tushuntirish va Mantiq:
1. Kartalardagi shaxsiy ma'lumotlarni (PCI DSS talablari bo'yicha) yashirish uchun regex guruhlari almashtiriladi.

## Ishlash natijasi:
```text
Chiqish: 8600 12** **** 9012, 9860 01** **** 8901
```

---

# 572-Topshiriq: re.VERBOSE (re.X) bilan o'qilishi oson regex yozish

## Topshiriq sharti:
Katta va murakkab shablonni izohlar bilan birga re.VERBOSE bayrog'idan foydalanib yozing.

## Yechim (Python kodi):
```python
import re

vaqt_regex = re.compile(r"""
    ^
    (?P<soat>[01]?[0-9]|2[0-3])   # 00 dan 23 gacha bo'lgan soat
    :
    (?P<daqiqa>[0-5][0-9])        # 00 dan 59 gacha bo'lgan daqiqa
    (?::(?P<soniya>[0-5][0-9]))?  # Ixtiyoriy soniya qismi
    $
""", re.VERBOSE)

print(bool(vaqt_regex.match("14:30")))
print(bool(vaqt_regex.match("23:59:59")))
print(bool(vaqt_regex.match("25:00")))
```

## Tushuntirish va Mantiq:
1. `re.VERBOSE` bo'sh joylar va `#` izohlarni e'tiborsiz qoldirish imkonini beradi, bu esa regex kodini juda tushunarli qiladi.

## Ishlash natijasi:
```text
Chiqish: True, True, False
```

---

# 573-Topshiriq: HTML teglarni butunlay tozalab sof matn qoldirish

## Topshiriq sharti:
HTML sahifa kodidan barcha teglarni olib tashlab, sof matnni ajrating.

## Yechim (Python kodi):
```python
import re

html_matn = "<p>O'zbekiston <b>Milliy Ensiklopediyasi</b> — buyuk meros. <a href='#'>Batafsil</a></p>"
sof_matn = re.sub(r"<[^>]+>", "", html_matn)
print("Sof matn:", sof_matn)
```

## Tushuntirish va Mantiq:
1. `<[^>]+>` ochiluvchi `<` dan yopiluvchi `>` gacha bo'lgan barcha belgilarni qamrab olib o'chiradi.

## Ishlash natijasi:
```text
Chiqish: Sof matn: O'zbekiston Milliy Ensiklopediyasi — buyuk meros. Batafsil
```

---

# 574-Topshiriq: Fayl kengaytmalarini (Extensions) ajratish va tekshirish

## Topshiriq sharti:
Fayl nomi faqat tasvir formatlari (.png, .jpg, .jpeg, .webp) ekanligini tekshiring.

## Yechim (Python kodi):
```python
import re

def rasmmi(fayl_nomi):
    return bool(re.search(r"\.(png|jpe?g|webp)$", fayl_nomi, re.IGNORECASE))

fayllar = ["foto.JPG", "hujjat.pdf", "rasm.png", "arxiv.zip", "banner.webp"]
for f in fayllar:
    print(f"{f}: {'Tasvir' if rasmmi(f) else 'Boshqa fayl'}")
```

## Tushuntirish va Mantiq:
1. `jpe?g` 'e' harfi ixtiyoriy ekanligini bildiradi (jpg yoki jpeg).

## Ishlash natijasi:
```text
Chiqish: foto.JPG: Tasvir, hujjat.pdf: Boshqa fayl, rasm.png: Tasvir, arxiv.zip: Boshqa fayl, banner.webp: Tasvir
```

---

# 575-Topshiriq: Parol murakkabligini tekshirish (Regex bilan Password Strength Validator)

## Topshiriq sharti:
Parolda kamida 8 ta belgi, 1 ta katta harf, 1 ta kichik harf, 1 ta raqam va 1 ta maxsus belgi borligini tekshiring.

## Yechim (Python kodi):
```python
import re

def kuchli_parol(parol):
    if len(parol) < 8:
        return False
    if not re.search(r"[A-Z]", parol):
        return False
    if not re.search(r"[a-z]", parol):
        return False
    if not re.search(r"[0-9]", parol):
        return False
    if not re.search(r"[!@#$%^&*(),.?":{}|<>]", parol):
        return False
    return True

print("Test1234! ->", kuchli_parol("Test1234!"))
print("parol123 ->", kuchli_parol("parol123"))
print("ODDIYPAROL ->", kuchli_parol("ODDIYPAROL"))
```

## Tushuntirish va Mantiq:
1. Har bir xavfsizlik sharti uchun alohida `re.search()` tekshiruvi amalga oshiriladi.

## Ishlash natijasi:
```text
Chiqish: Test1234! -> True, parol123 -> False, ODDIYPAROL -> False
```

---

# 576-Topshiriq: Satrdan barcha heshteglar (#hashtag) va eslatmalarni (@mention) ajratish

## Topshiriq sharti:
Ijtimoiy tarmoq postidan barcha teglar va foydalanuvchi nomlarini alohida ro'yxatlarga oling.

## Yechim (Python kodi):
```python
import re

post = "Salom dunyo! #ai va #python haqida @alisher bilan yangi loyiha boshladik! #uzbekistan"
heshteglar = re.findall(r"#(\w+)", post)
eslatmalar = re.findall(r"@(\w+)", post)

print("Heshteglar:", heshteglar)
print("Eslatmalar:", eslatmalar)
```

## Tushuntirish va Mantiq:
1. Qavs ichiga olingan `(\w+)` tufayli `re.findall()` faqat belgisiz so'zning o'zini qaytaradi.

## Ishlash natijasi:
```text
Chiqish: Heshteglar: ['ai', 'python', 'uzbekistan'], Eslatmalar: ['alisher']
```

---

# 577-Topshiriq: JSON ichidagi kalit-qiymat juftliklarini regex orqali qidirish

## Topshiriq sharti:
Buzilgan yoki qisman olingan JSON satridan 'name' va 'age' qiymatlarini regex bilan ajrating.

## Yechim (Python kodi):
```python
import re

raw_data = '{"name": "Jasur", "status": "active", "age": 21, "city": "Toshkent"}'
ism = re.search(r'"name"\s*:\s*"([^"]+)"', raw_data)
yosh = re.search(r'"age"\s*:\s*(\d+)', raw_data)

if ism and yosh:
    print(f"Ism: {ism.group(1)}, Yosh: {yosh.group(1)}")
```

## Tushuntirish va Mantiq:
1. `[^\"]+` qo'shtirnoqdan tashqari har qanday belgilar ketma-ketligini ushlaydi.

## Ishlash natijasi:
```text
Chiqish: Ism: Jasur, Yosh: 21
```

---

# 578-Topshiriq: Satrdagi qavslar ichidagi matnlarni ajratib olish

## Topshiriq sharti:
Dumaloq qavs `(...)` ichida keltirilgan barcha izohlarni ajrating.

## Yechim (Python kodi):
```python
import re

matn = "O'zbekiston (Markaziy Osiyo) mustaqil davlat. Poytaxti Toshkent (aholisi 3 mln)."
qavslar = re.findall(r"\((.*?)\)", matn)
print("Qavs ichidagi ma'lumotlar:", qavslar)
```

## Tushuntirish va Mantiq:
1. Maxsus belgilar `\(` va `\)` orqali ekranlashtiriladi (escape). `.*?` esa eng yaqin yopuvchi qavsgacha oladi.

## Ishlash natijasi:
```text
Chiqish: Qavs ichidagi ma'lumotlar: ['Markaziy Osiyo', 'aholisi 3 mln']
```

---

# 579-Topshiriq: Jumlalarga ajratish (Sentence Tokenizer)

## Topshiriq sharti:
Matnni nuqta, so'roq va undov belgilari bo'yicha to'g'ri jumlalarga ajrating (qisqartmalar va sonlarni inobatga olgan holda).

## Yechim (Python kodi):
```python
import re

matn = "Salom! Ishlar qalay? Bugun 2026-yil 7-noyabr. Biz yangi model quryapmiz! Bu ajoyib."
jumlalar = re.split(r"(?<=[.!?])\s+", matn.strip())
for i, j in enumerate(jumlalar, 1):
    print(f"{i}-jumla: {j}")
```

## Tushuntirish va Mantiq:
1. `(?<=[.!?])\s+` orqaga qarab tinish belgisidan keyingi bo'shliq bo'yicha ajratadi va tinish belgisini jumlada saqlab qoladi.

## Ishlash natijasi:
```text
Chiqish: 1-jumla: Salom!, 2-jumla: Ishlar qalay?, 3-jumla: Bugun 2026-yil 7-noyabr., 4-jumla: Biz yangi model quryapmiz!, 5-jumla: Bu ajoyib.
```

---

# 580-Topshiriq: So'z chastotasi (Word Frequency) tahlili

## Topshiriq sharti:
Matndan barcha tinish belgilarini chiqarib tashlab, har bir so'z necha marta qatnashganini hisoblang.

## Yechim (Python kodi):
```python
import re
from collections import Counter

matn = "Ilm, fan va texnologiya. Ilm — insoniyat kelajagi. Fan va taraqqiyot doim birga."
sozlar = re.findall(r"\b[a-zA-Z'’-]+\b", matn.lower())
chastota = Counter(sozlar)

for soz, son in chastota.most_common(4):
    print(f"'{soz}': {son} marta")
```

## Tushuntirish va Mantiq:
1. `\b[a-zA-Z'’-]+\b` o'zbekcha so'zlarni tire va tutuq belgilari bilan birga to'liq ajratadi.

## Ishlash natijasi:
```text
Chiqish: 'ilm': 2 marta, 'va': 2 marta, 'fan': 2 marta, 'texnologiya': 1 marta
```

---

# 581-Topshiriq: N-gramma generatori (Bigram va Trigram)

## Topshiriq sharti:
Matn so'zlaridan ketma-ket keluvchi 2 ta (bigram) va 3 ta (trigram) so'z birikmalarini hosil qiling.

## Yechim (Python kodi):
```python
import re

def n_gramma(matn, n):
    sozlar = re.findall(r"\b\w+\b", matn.lower())
    return [tuple(sozlar[i:i+n]) for i in range(len(sozlar) - n + 1)]

matn = "Sun'iy intellekt kelajak kasblarini butunlay o'zgartirib yuboradi"
print("Bigrammalar:", n_gramma(matn, 2)[:3])
print("Trigrammalar:", n_gramma(matn, 3)[:2])
```

## Tushuntirish va Mantiq:
1. NLP modellarida N-grammalar so'zlarning kontekstual birikuvchanligini o'rganishda xizmat qiladi.

## Ishlash natijasi:
```text
Chiqish: Bigrammalar: [('sun', 'iy'), ('iy', 'intellekt'), ('intellekt', 'kelajak')], Trigrammalar: [('sun', 'iy', 'intellekt'), ('iy', 'intellekt', 'kelajak')]
```

---

# 582-Topshiriq: Stop-so'zlarni (Stopwords) tozalash

## Topshiriq sharti:
Matndan ma'no yuklamaydigan yordamchi so'zlarni (va, ham, bilan, uchun, da) olib tashlang.

## Yechim (Python kodi):
```python
import re

stop_words = {"va", "ham", "bilan", "uchun", "da", "esa", "bu"}
matn = "Bu model O'zbekiston uchun va yoshlar bilan birgalikda yaratildi ham rivojlanadi."

sozlar = re.findall(r"\b\w+\b", matn)
foydali = [s for s in sozlar if s.lower() not in stop_words]
print("Tozalangan so'zlar:", " ".join(foydali))
```

## Tushuntirish va Mantiq:
1. NLP modellarining lug'at hajmini qisqartirish uchun stop-so'zlar filtrlanadi.

## Ishlash natijasi:
```text
Chiqish: Tozalangan so'zlar: model O zbekiston yoshlar birgalikda yaratildi rivojlanadi
```

---

# 583-Topshiriq: Levenshteyn masofasi (Edit Distance) — So'zlar o'xshashligi

## Topshiriq sharti:
Ikki so'z orasidagi minimal tahrirlash amallarini (qo'shish, o'chirish, almashtirish) dinamik dasturlash bilan hisoblang.

## Yechim (Python kodi):
```python
def levenshtein(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

print("kitob vs kitoblar:", levenshtein("kitob", "kitoblar"))
print("olma vs olma:", levenshtein("olma", "olma"))
print("salom vs valom:", levenshtein("salom", "valom"))
```

## Tushuntirish va Mantiq:
1. Levenshteyn masofasi imlo tekshirgichlar (Spell Checker) va fuzzy search mexanizmlarining poydevoridir.

## Ishlash natijasi:
```text
Chiqish: kitob vs kitoblar: 3, olma vs olma: 0, salom vs valom: 1
```

---

# 584-Topshiriq: Imlo xatolarini tuzatuvchi oddiy Spell Checker

## Topshiriq sharti:
Lug'at yordamida berilgan xato so'zga eng yaqin to'g'ri so'zni Levenshteyn masofasi orqali toping.

## Yechim (Python kodi):
```python
lugat = ["dasturchi", "mashina", "kitob", "kompyuter", "maktab", "universitet"]

def togri_sozni_top(xato_soz, lugat):
    def dist(s1, s2):
        if s1 == s2: return 0
        dp = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            yangi_dp = [i + 1] * (len(s2) + 1)
            for j, c2 in enumerate(s2):
                narx = 0 if c1 == c2 else 1
                yangi_dp[j + 1] = min(dp[j + 1] + 1, yangi_dp[j] + 1, dp[j] + narx)
            dp = yangi_dp
        return dp[-1]

    eng_yaxshi = min(lugat, key=lambda s: dist(xato_soz, s))
    return eng_yaxshi

print("dasturch ->", togri_sozni_top("dasturch", lugat))
print("kamputer ->", togri_sozni_top("kamputer", lugat))
```

## Tushuntirish va Mantiq:
1. Har bir lug'at so'zi bilan masofa tekshirilib, minimal masofali nomzod tanlanadi.

## Ishlash natijasi:
```text
Chiqish: dasturch -> dasturchi, kamputer -> kompyuter
```

---

# 585-Topshiriq: Jaccard o'xshashlik koeffitsiyenti (Jaccard Similarity)

## Topshiriq sharti:
Ikki matnning so'zlar to'plami kesishmasi va birlashmasi asosida o'xshashlik foizini hisoblang.

## Yechim (Python kodi):
```python
def jaccard_oxshashlik(m1, m2):
    s1 = set(m1.lower().split())
    s2 = set(m2.lower().split())
    kesishma = s1.intersection(s2)
    birlashma = s1.union(s2)
    return len(kesishma) / len(birlashma) if birlashma else 0.0

m1 = "Sun'iy intellekt dasturlash va ma'lumotlar bilan ishlaydi"
m2 = "Sun'iy intellekt algoritmlar va dasturlash asosida ishlaydi"
print(f"O'xshashlik: {jaccard_oxshashlik(m1, m2):.2%}")
```

## Tushuntirish va Mantiq:
1. Jaccard koeffitsiyenti: J(A, B) = |A ∩ B| / |A ∪ B|. U to'plamlar o'xshashligini 0 dan 1 gacha o'lchaydi.

## Ishlash natijasi:
```text
Chiqish: O'xshashlik: 50.00%
```

---

# 586-Topshiriq: Bag of Words (BoW) vektorini qurish

## Topshiriq sharti:
Bir nechta matnlar uchun barcha noyob so'zlardan iborat lug'at tuzib, har bir matnni vektorga aylantiring.

## Yechim (Python kodi):
```python
matnlar = [
    "sun'iy intellekt kelajak",
    "kelajak dasturlash bilan bog'liq",
    "sun'iy intellekt dasturlash"
]

# Lug'at tuzish
lugat = sorted(list(set(soz for m in matnlar for soz in m.split())))
print("Lug'at:", lugat)

vektorlar = []
for m in matnlar:
    sozlar = m.split()
    vektor = [sozlar.count(w) for w in lugat]
    vektorlar.append(vektor)

print("Vektorlar:", vektorlar)
```

## Tushuntirish va Mantiq:
1. Bag of Words matnni raqamli ko'rinishga keltirishning eng oddiy usuli bo'lib, so'zlar chastotasini ifodalaydi.

## Ishlash natijasi:
```text
Chiqish: Lug'at: ["bog'liq", 'bilan', 'dasturlash', 'intellekt', 'kelajak', "sun'iy"], Vektorlar: [[0, 0, 0, 1, 1, 1], [1, 1, 1, 0, 1, 0], [0, 0, 1, 1, 0, 1]]
```

---

# 587-Topshiriq: TF-IDF (Term Frequency - Inverse Document Frequency) hisoblash

## Topshiriq sharti:
Matnlar to'plami ichida so'zlarning TF-IDF vaznini sof Python kutubxonalarsiz hisoblang.

## Yechim (Python kodi):
```python
import math

hujjatlar = [
    "python ma'lumotlar tahlili",
    "python va sun'iy intellekt",
    "sun'iy intellekt va robototexnika"
]

def tf(soz, matn):
    sozlar = matn.split()
    return sozlar.count(soz) / len(sozlar)

def idf(soz, docs):
    hujjat_soni = sum(1 for d in docs if soz in d.split())
    return math.log(len(docs) / (1 + hujjat_soni))

def tf_idf(soz, matn, docs):
    return tf(soz, matn) * idf(soz, docs)

print("TF-IDF ('python' 1-hujjatda):", round(tf_idf("python", hujjatlar[0], hujjatlar), 4))
print("TF-IDF ('tahlili' 1-hujjatda):", round(tf_idf("tahlili", hujjatlar[0], hujjatlar), 4))
```

## Tushuntirish va Mantiq:
1. Keng tarqalgan umumiy so'zlar kichikroq vazn oladi, noyob va muhim so'zlar esa yuqoriroq TF-IDF qiymatiga ega bo'ladi.

## Ishlash natijasi:
```text
Chiqish: TF-IDF ('python' 1-hujjatda): 0.0, TF-IDF ('tahlili' 1-hujjatda): 0.1352
```

---

# 588-Topshiriq: Matndan elektron pochtalarni (Email) regex bilan ajratib olish

## Topshiriq sharti:
Aralash matndan barcha to'g'ri elektron pochta manzillarini ajrating.

## Yechim (Python kodi):
```python
import re

matn = "Murojaat uchun: support@uzai.uz yoki info@data-center.org, admin.test@sub.domain.com"
email_lar = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", matn)
print("Topilgan email-lar:", email_lar)
```

## Tushuntirish va Mantiq:
1. `[A-Za-z0-9._%+-]+` email nomini, `@` dan keyingisi esa domenni ushlaydi.

## Ishlash natijasi:
```text
Chiqish: Topilgan email-lar: ['support@uzai.uz', 'info@data-center.org', 'admin.test@sub.domain.com']
```

---

# 589-Topshiriq: Subtitr fayllaridagi (SRT) vaqt belgilarini regex bilan o'qish

## Topshiriq sharti:
SRT subtitr satrlaridan boshlanish va tugash vaqtlarini ajratib oling.

## Yechim (Python kodi):
```python
import re

srt_qator = "00:01:20,500 --> 00:01:23,800"
pattern = r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})"

m = re.match(pattern, srt_qator)
if m:
    boshlanish, tugash = m.groups()
    print(f"Boshlandi: {boshlanish}, Tugadi: {tugash}")
```

## Tushuntirish va Mantiq:
1. SRT fayllari soat:daqiqa:soniya,millisoniya formatida vaqt belgilarini saqlaydi.

## Ishlash natijasi:
```text
Chiqish: Boshlandi: 00:01:20,500, Tugadi: 00:01:23,800
```

---

# 590-Topshiriq: Matndagi xeshlarni (MD5, SHA-256) aniqlash

## Topshiriq sharti:
Satrdan 32 belgili MD5 va 64 belgili SHA-256 xesh kodlarini ajrating.

## Yechim (Python kodi):
```python
import re

log = "File checksum: md5=5d41402abc4b2a76b9719d911017c592 sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

md5_xesh = re.findall(r"\b[a-fA-F0-9]{32}\b", log)
sha256_xesh = re.findall(r"\b[a-fA-F0-9]{64}\b", log)

print("MD5:", md5_xesh)
print("SHA256:", sha256_xesh)
```

## Tushuntirish va Mantiq:
1. Xesh qiymatlari o'n oltilik (hex) sanoq tizimidagi belgilardan tashkil topadi.

## Ishlash natijasi:
```text
Chiqish: MD5: ['5d41402abc4b2a76b9719d911017c592'], SHA256: ['e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']
```

---

# 591-Topshiriq: Log fayllaridagi xatolik darajalari (INFO, WARN, ERROR) bo'yicha guruhlash

## Topshiriq sharti:
Server log qatoridan vaqt, daraja va xabarni ajratib lug'at hosil qiling.

## Yechim (Python kodi):
```python
import re

log_qator = "2026-11-07 14:22:10 [ERROR] Bazaga ulanishda timeout yuz berdi"
pattern = r"^(?P<vaqt>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(?P<daraja>[A-Z]+)\] (?P<xabar>.*)$"

m = re.match(pattern, log_qator)
if m:
    print(m.groupdict())
```

## Tushuntirish va Mantiq:
1. Nomlangan guruhlar log analizatorlarida (Logstash, Fluentd kabi) parsing jarayonini soddalashtiradi.

## Ishlash natijasi:
```text
Chiqish: {'vaqt': '2026-11-07 14:22:10', 'daraja': 'ERROR', 'xabar': 'Bazaga ulanishda timeout yuz berdi'}
```

---

# 592-Topshiriq: re.MULTILINE (re.M) bayrog'i bilan har bir qator boshini tekshirish

## Topshiriq sharti:
Ko'p qatorli matndan har bir qator boshidagi '#' belgisini (Markdown sarlavhalari) toping.

## Yechim (Python kodi):
```python
import re

md_matn = """# Asosiy sarlavha
Oddiy matn qatori
## Kichik sarlavha
Yana bir matn
# Yakuniy bob"""

sarlavhalar = re.findall(r"^#+\s+(.*)$", md_matn, flags=re.MULTILINE)
print("Sarlavhalar:", sarlavhalar)
```

## Tushuntirish va Mantiq:
1. `re.MULTILINE` yoqilganda `^` va `$` butun matn boshi va oxirini emas, balki har bir yangi qator (`\n`) boshi va oxirini bildiradi.

## Ishlash natijasi:
```text
Chiqish: Sarlavhalar: ['Asosiy sarlavha', 'Kichik sarlavha', 'Yakuniy bob']
```

---

# 593-Topshiriq: re.DOTALL (re.S) bayrog'i bilan yangi qatorlarni ham qamrab olish

## Topshiriq sharti:
Bir nechta qatorda davom etgan blokni `/* ... */` regex bilan to'liq ajratib oling.

## Yechim (Python kodi):
```python
import re

kod = """
int a = 10;
/*
 Bu ko'p qatorli
 izoh bloki
*/
int b = 20;
"""

izohlar = re.findall(r"/\*.*?\*/", kod, flags=re.DOTALL)
print("Izoh:", izohlar[0].strip())
```

## Tushuntirish va Mantiq:
1. Standart holatda `.` belgisi `\n` dan boshqa hamma belgiga mos keladi. `re.DOTALL` esa `.` ga yangi qatorni ham qo'shadi.

## Ishlash natijasi:
```text
Chiqish: Izoh: /*\n Bu ko'p qatorli\n izoh bloki\n*/
```

---

# 594-Topshiriq: CamelCase satrni snake_case ga o'girish

## Topshiriq sharti:
Regex yordamida 'ObyektKlassNomi' ko'rinishidagi satrni 'obyekt_klass_nomi' ga aylantiring.

## Yechim (Python kodi):
```python
import re

def camel_to_snake(satr):
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', satr)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

print(camel_to_snake("ObyektKlassNomi"))
print(camel_to_snake("getUserProfileData"))
print(camel_to_snake("HTTPRequestParser"))
```

## Tushuntirish va Mantiq:
1. Katta harflar oldiga chiziqcha qo'shish va keyin kichik harfga o'tkazish orqali standart konvensiya yaratiladi.

## Ishlash natijasi:
```text
Chiqish: obyekt_klass_nomi, get_user_profile_data, http_request_parser
```

---

# 595-Topshiriq: snake_case satrni camelCase va PascalCase ga o'girish

## Topshiriq sharti:
Regex yordamida 'foydalanuvchi_ismi' satrini 'foydalanuvchiIsmi' va 'FoydalanuvchiIsmi' ga o'giring.

## Yechim (Python kodi):
```python
import re

def snake_to_camel(satr):
    sozlar = satr.split('_')
    return sozlar[0] + ''.join(s.capitalize() for s in sozlar[1:])

def snake_to_pascal(satr):
    return ''.join(s.capitalize() for s in satr.split('_'))

print("Camel:", snake_to_camel("foydalanuvchi_ismi"))
print("Pascal:", snake_to_pascal("foydalanuvchi_ismi"))
```

## Tushuntirish va Mantiq:
1. `split('_')` qilib har bir so'zning bosh harfini kattalashtirish konvertatsiyani osonlashtiradi.

## Ishlash natijasi:
```text
Chiqish: Camel: foydalanuvchiIsmi, Pascal: FoydalanuvchiIsmi
```

---

# 596-Topshiriq: Matndan barcha emoji belgilarini tozalash

## Topshiriq sharti:
Matndagi turli xil smaylik va emojilarni regex diapazoni orqali tozalang.

## Yechim (Python kodi):
```python
import re

matn = "Salom do'stlar! 🚀 Bugun havo juda zo'r ☀️🎉 Dasturlaymiz 💻🔥"
tozalangan = re.sub(r"[\U00010000-\U0010ffff]", "", matn)
print("Emojisiz matn:", tozalangan.strip())
```

## Tushuntirish va Mantiq:
1. Unicode diapazonidagi 4 baytli emojilar `[\U00010000-\U0010ffff]` filtri orqali yo'qotiladi.

## Ishlash natijasi:
```text
Chiqish: Emojisiz matn: Salom do'stlar!  Bugun havo juda zo'r  Dasturlaymiz
```

---

# 597-Topshiriq: Satrdan dublikat bo'shliqlarni olib tashlab slug yaratish (URL Slugify)

## Topshiriq sharti:
Sarlavhadan veb-sayt havolasi uchun xavfsiz URL slug (masalan: 'sun-iy-intellekt-kelajagi') yasang.

## Yechim (Python kodi):
```python
import re

def slugify(matn):
    matn = matn.lower().strip()
    matn = re.sub(r"['`’]", "", matn)  # Tutuqlarni olib tashlash
    matn = re.sub(r"[^a-z0-9]+", "-", matn)  # Begona belgilarni chiziqchaga aylantirish
    return matn.strip("-")

print(slugify("Sun'iy intellekt va Kvant Kompyuterlari: 2026!"))
```

## Tushuntirish va Mantiq:
1. Veb sahifalarda SEO uchun qulay bo'lgan slug yaratishda harflar va sonlardan boshqa belgilar chiziqchaga almashtiriladi.

## Ishlash natijasi:
```text
Chiqish: suniy-intellekt-va-kvant-kompyuterlari-2026
```

---

# 598-Topshiriq: Binar (Ikkilik) satrlarni tekshiruvchi regex

## Topshiriq sharti:
Faqat 0 va 1 lardan tashkil topgan hamda uzunligi 8 ga karrali bo'lgan bayt satrlarini tekshiring.

## Yechim (Python kodi):
```python
import re

def baytmi(satr):
    return bool(re.match(r"^([01]{8})+$", satr))

print("01000001 ->", baytmi("01000001"))
print("0100000101000010 ->", baytmi("0100000101000010"))
print("0101 ->", baytmi("0101"))
print("01002001 ->", baytmi("01002001"))
```

## Tushuntirish va Mantiq:
1. `([01]{8})+` har biri 8 ta 0 yoki 1 dan iborat bo'lgan bloklarni bitta yoki bir nechtasini tekshiradi.

## Ishlash natijasi:
```text
Chiqish: 01000001 -> True, 0100000101000010 -> True, 0101 -> False, 01002001 -> False
```

---

# 599-Topshiriq: Matndan Markdown havolalarini [nom](url) ajratish

## Topshiriq sharti:
Markdown formatidagi havolalardan matn va manzilni ajratib oling.

## Yechim (Python kodi):
```python
import re

md = "Bizning loyiha: [GitHub](https://github.com/ai) va [HuggingFace](https://huggingface.co/datas)."
havolalar = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", md)

for nom, url in havolalar:
    print(f"Havola nomi: {nom} -> URL: {url}")
```

## Tushuntirish va Mantiq:
1. `\[([^\]]+)\]` kvadrat qavs ichidagi matnni, `\(([^\)]+)\)` esa dumaloq qavs ichidagi URL ni guruhlaydi.

## Ishlash natijasi:
```text
Chiqish: Havola nomi: GitHub -> URL: https://github.com/ai, Havola nomi: HuggingFace -> URL: https://huggingface.co/datas
```

---

# 600-Topshiriq: Mukammal Matn Tozalash Quvuri (NLP Text Cleaning Pipeline)

## Topshiriq sharti:
Barcha o'rganilgan regex usullarini birlashtirib, katta xom matnni tozalovchi yaxlit pipeline yarating.

## Yechim (Python kodi):
```python
import re

class MatnTozalovchi:
    def __init__(self):
        self.html_re = re.compile(r"<[^>]+>")
        self.url_re = re.compile(r"https?://\S+|www\.\S+")
        self.kop_boshliq_re = re.compile(r"\s+")

    def tozalash(self, matn):
        # 1. HTML teglarni tozalash
        qadam1 = self.html_re.sub(" ", matn)
        # 2. Havolalarni tozalash
        qadam2 = self.url_re.sub(" ", qadam1)
        # 3. Maxsus keraksiz belgilarni yo'qotish
        qadam3 = re.sub(r"[^a-zA-Z0-9'’\s.,!?-]", " ", qadam2)
        # 4. Ortiqcha bo'shliqlarni bitta bo'shliqqa keltirish
        yakuniy = self.kop_boshliq_re.sub(" ", qadam3).strip()
        return yakuniy

tozalovchi = MatnTozalovchi()
xom_matn = """<div><p>Diqqat! Saytimiz: https://ziyouz.com 🚀 Narxi: @$500!!</p></div>"""
print("Natija:", tozalovchi.tozalash(xom_matn))
```

## Tushuntirish va Mantiq:
1. Matnni bosqichma-bosqich tozalash (Text Preprocessing Pipeline) sun'iy intellekt modellarini o'qitishda sifatni ta'minlovchi eng muhim bosqichdir.

## Ishlash natijasi:
```text
Chiqish: Natija: Diqqat! Saytimiz Narxi 500!!
```

---

