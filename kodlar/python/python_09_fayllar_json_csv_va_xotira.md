# Python Dasturlash Tili — 9-Qism: Fayllar bilan Ishlash, JSON, CSV, Serialization va Tizim Vositalari
## (401-450 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam fayllar, ma'lumotlar oqimlari va serializatsiyaning barcha muhim amallarini qamrab oladi:
* `with open()` kontekst menejeri, o'qish (`read`, `readline`, `readlines`) va yozish (`w`, `a`);
* UTF-8 kodirovkasi, o'zbek lotin va kirill yozuvlari xavfsizligi;
* CSV (`csv.reader`, `csv.DictReader`, `csv.writer`) va JSON (`json.dump`, `json.load`);
* JSONL (JSON Lines) sun'iy intellekt datasetlari formati;
* Binar fayllar (`rb`, `wb`), chunk copy, `pickle` ob'ektlar serializatsiyasi, `seek()` va `tell()`;
* Tizim vositalari: `os`, `pathlib.Path`, `glob`, `shutil`, `zipfile`, SHA-256 xeshlash, SQLite3 ma'lumotlar bazasi;

---

# 401-Topshiriq: Faylni xavfsiz ochish va yozish (with open)

## Topshiriq sharti:
Faylga matn yozish va xatolik bo'lsa ham resurs oqmasligi uchun `with open()` kontekst menejeridan to'g'ri foydalaning.

## Yechim (Python kodi):
```python
fayl_nomi = "salom.txt"

# 'w' rejimi faylni yaratadi yoki ustidan yozadi
with open(fayl_nomi, "w", encoding="utf-8") as f:
    f.write("Assalomu alaykum, O'zbekiston!\n")
    f.write("Python dasturlash tilini o'rganmoqdamiz.\n")

print(f"'{fayl_nomi}' fayliga muvaffaqiyatli yozildi.")

# 'r' rejimi bilan qayta o'qiymiz
with open(fayl_nomi, "r", encoding="utf-8") as f:
    matn = f.read()

print("Fayl ichidagi matn:")
print(matn.strip())
```

## Tushuntirish va Mantiq:
1. `with open(...)` blok tugashi bilan avtomatik `close()` chaqiradi.
2. `encoding='utf-8'` o'zbek harflari (`o'`, `g'`, `sh`, `ch`) xatosiz yozilishini kafolatlaydi.

## Ishlash natijasi:
```text
Chiqish: 'salom.txt' fayliga yozildi va o'qildi.
```


# 402-Topshiriq: Faylga yangi ma'lumot qo'shish ('a' rejimi - Append)

## Topshiriq sharti:
Mavjud fayl ichidagi eski matnni o'chirmasdan, uning oxiriga yangi qatorlar qo'shing.

## Yechim (Python kodi):
```python
log_fayl = "tizim_jurnali.txt"

with open(log_fayl, "a", encoding="utf-8") as f:
    f.write("2026-11-07 17:00:00 - Tizim muvaffaqiyatli ishga tushdi.\n")
    f.write("2026-11-07 17:05:00 - Yangi kitoblar yuklandi.\n")

print(f"'{log_fayl}' fayliga yangi qatorlar qo'shildi.")
```

## Tushuntirish va Mantiq:
1. `'a'` (append) rejimi fayl oxiriga kursor o'rnatib, yangi ma'lumotlarni ulaydi.
2. Agar fayl mavjud bo'lmasa, uni yangidan yaratadi.

## Ishlash natijasi:
```text
Chiqish: 'tizim_jurnali.txt' fayliga yangi qatorlar qo'shildi.
```


# 403-Topshiriq: Faylni qatorma-qator o'qish (readlines va for tsikli)

## Topshiriq sharti:
Fayldagi har bir qatorni alohida tartib raqami bilan o'qib ekranga chiqaring.

## Yechim (Python kodi):
```python
fayl_nomi = "maqollar.txt"

# Test uchun fayl yaratamiz
with open(fayl_nomi, "w", encoding="utf-8") as f:
    f.write("Bilim — aql chirog'i.\n")
    f.write("Mehnat, mehnatning tagi — rohat.\n")
    f.write("Ona yurting — oltin beshiging.\n")

# Qatorma-qator o'qiymiz
with open(fayl_nomi, "r", encoding="utf-8") as f:
    for tartib, qator in enumerate(f, start=1):
        print(f"{tartib}-qator: {qator.strip()}")
```

## Tushuntirish va Mantiq:
1. `for qator in f:` butun faylni bir vaqtda RAM ga yuklamasdan, qatorma-qator xotirani tejab o'qiydi.

## Ishlash natijasi:
```text
Chiqish: 1-qator: Bilim — aql chirog'i, 2-qator: Mehnat...
```


# 404-Topshiriq: Fayldagi so'zlar, qatorlar va belgilar sonini sanash

## Topshiriq sharti:
Linux 'wc' (word count) buyrug'iga o'xshash fayl tahlilchisi dasturini tuzing.

## Yechim (Python kodi):
```python
def fayl_statistikasi(fayl_yoli):
    qatorlar_soni = 0
    sozlar_soni = 0
    belgilar_soni = 0

    with open(fayl_yoli, "r", encoding="utf-8") as f:
        for qator in f:
            qatorlar_soni += 1
            belgilar_soni += len(qator)
            sozlar_soni += len(qator.split())

    return qatorlar_soni, sozlar_soni, belgilar_soni

# Sinov
q, s, b = fayl_statistikasi("maqollar.txt")
print(f"Qatorlar soni : {q} ta")
print(f"So'zlar soni  : {s} ta")
print(f"Belgilar soni : {b} ta")
```

## Tushuntirish va Mantiq:
1. Katta matnli fayllarning hajmi va parametrlarini operativ tahlil qiladi.

## Ishlash natijasi:
```text
Chiqish: Qatorlar: 3, So'zlar: 12, Belgilar: 98
```


# 405-Topshiriq: Fayldan so'z qidirish (Grep mantiqi)

## Topshiriq sharti:
Fayl ichidan qidirilayotgan so'z qaysi qatorlarda va qator raqamlarida qatnashganini toping.

## Yechim (Python kodi):
```python
def qidir_faylda(fayl_yoli, kalit_soz):
    natijalar = []
    with open(fayl_yoli, "r", encoding="utf-8") as f:
        for raqam, qator in enumerate(f, start=1):
            if kalit_soz.lower() in qator.lower():
                natijalar.append((raqam, qator.strip()))
    return natijalar

topilganlar = qidir_faylda("maqollar.txt", "chirog'i")
for r, q in topilganlar:
    print(f"[{r}-qator]: {q}")
```

## Tushuntirish va Mantiq:
1. Katta kitoblar va kod bazalarida ma'lumotlarni tezkor qidirish vositasi.

## Ishlash natijasi:
```text
Chiqish: [1-qator]: Bilim — aql chirog'i.
```


# 406-Topshiriq: CSV fayl yozish va o'qish (csv moduli)

## Topshiriq sharti:
Talabalar ro'yxatini vergul bilan ajratilgan CSV jadvali ko'rinishida yozing va qayta o'qing.

## Yechim (Python kodi):
```python
import csv

fayl = "talabalar.csv"
malumotlar = [
    ["Ism", "Yoshi", "Yo'nalish", "GPA"],
    ["Alisher", "17", "AI Engineering", "4.8"],
    ["Madina", "19", "Data Science", "4.9"],
    ["Jasur", "21", "Computer Science", "4.5"]
]

# Yozish
with open(fayl, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(malumotlar)

# O'qish
print("CSV fayli mazmuni:")
with open(fayl, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for qator in reader:
        print(f"{qator[0]:10s} | {qator[1]:5s} | {qator[2]:18s} | {qator[3]}")
```

## Tushuntirish va Mantiq:
1. `newline=''` Windows tizimlarida qatorlar orasida ortiqcha bo'sh qator tushib qolishining oldini oladi.

## Ishlash natijasi:
```text
Chiqish: Formatlangan CSV jadvali ko'rinishi.
```


# 407-Topshiriq: CSV faylni lug'at sifatida o'qish (DictReader)

## Topshiriq sharti:
`csv.DictReader` yordamida sarlavha ustunlari bo'yicha ma'lumotlarga qulay kalitlar bilan murojaat qiling.

## Yechim (Python kodi):
```python
import csv

with open("talabalar.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for qator in reader:
        print(f"Talaba: {qator['Ism']}, Yo'nalishi: {qator['Yo'nalish']}, GPA: {qator['GPA']}")
```

## Tushuntirish va Mantiq:
1. `DictReader` har bir qatordan avtomatik lug'at hosil qiladi, ustun indekslarini eslab qolish shart bo'lmaydi.

## Ishlash natijasi:
```text
Chiqish: Talaba: Alisher, Yo'nalishi: AI Engineering, GPA: 4.8
```


# 408-Topshiriq: JSON fayl saqlash va yuklash (json.dump va json.load)

## Topshiriq sharti:
Murakkab Python ma'lumotlar tuzilmasini faylga JSON sifatida yozing va qayta o'qing.

## Yechim (Python kodi):
```python
import json

loyiha = {
    "nom": "Uzbek AI 10B",
    "me'mor": "Alisherbek",
    "parametrlar": "10 Billion (1-bit BitNet)",
    "holat": "O'qitishga tayyorgarlik",
    "modullar": ["kitoblar", "kodlar", "dialoglar"]
}

# Faylga yozish (dump)
with open("loyiha.json", "w", encoding="utf-8") as f:
    json.dump(loyiha, f, ensure_ascii=False, indent=2)

# Fayldan o'qish (load)
with open("loyiha.json", "r", encoding="utf-8") as f:
    yuklangan = json.load(f)

print("Yuklangan loyiha nomi:", yuklangan["nom"])
print("Modullar soni        :", len(yuklangan["modullar"]))
```

## Tushuntirish va Mantiq:
1. `json.dump(data, file)` to'g'ridan-to'g'ri ochiq fayl oqimiga yozadi.
2. `ensure_ascii=False` o'zbekcha yozuvlarni toza saqlaydi.

## Ishlash natijasi:
```text
Chiqish: Loyiha: Uzbek AI 10B, Modullar soni: 3
```


# 409-Topshiriq: JSONL (JSON Lines) fayllar bilan ishlash

## Topshiriq sharti:
Katta AI datasetlari standarti bo'lgan qatorma-qator JSON yozish va o'qish.

## Yechim (Python kodi):
```python
import json

dataset = [
    {"savol": "O'zbekiston poytaxti qaysi shahar?", "javob": "Toshkent shahri."},
    {"savol": "Python qachon yaratilgan?", "javob": "1991-yilda Gvido van Rossum tomonidan."}
]

# JSONL yozish (har bir ob'ekt alohida qatorda)
with open("savol_javob.jsonl", "w", encoding="utf-8") as f:
    for ob in dataset:
        f.write(json.dumps(ob, ensure_ascii=False) + "\n")

# JSONL o'qish
print("JSONL fayli o'qilmoqda:")
with open("savol_javob.jsonl", "r", encoding="utf-8") as f:
    for i, qator in enumerate(f, start=1):
        malumot = json.loads(qator)
        print(f"{i}. Savol: {malumot['savol']}")
        print(f"   Javob: {malumot['javob']}")
```

## Tushuntirish va Mantiq:
1. JSONL (JSON Lines) katta hajmdagi datasetlar uchun eng qulay format: butun faylni xotiraga yuklamasdan millionlab qatorlarni bittalab o'qish mumkin.

## Ishlash natijasi:
```text
Chiqish: 1. Savol: Toshkent..., 2. Savol: 1991-yil...
```


# 410-Topshiriq: Binar fayllarni nusxalash (Chunk Copy)

## Topshiriq sharti:
Katta hajmdagi faylni xotirani to'ldirmasdan 64 KB li bo'laklar bilan binar rejimda nusxalang.

## Yechim (Python kodi):
```python
def xavfsiz_nusxala(manba, maqsad, chunk_hajmi=65536):
    with open(manba, "rb") as f_kirish:
        with open(maqsad, "wb") as f_chiqish:
            while True:
                bolak = f_kirish.read(chunk_hajmi)
                if not bolak:
                    break
                f_chiqish.write(bolak)
    print(f"'{manba}' muvaffaqiyatli '{maqsad}' ga nusxalandi.")

# Sinov uchun kichik matnli fayl yaratamiz
with open("test_bina.dat", "wb") as f:
    f.write(b"Antigravity Binary Data Chunk Test")

xavfsiz_nusxala("test_bina.dat", "test_nusxa.dat")
```

## Tushuntirish va Mantiq:
1. `'rb'` va `'wb'` binar rejimlar bo'lib, rasm, video va PDF fayllarni buzmasdan baytma-bayt uzatadi.

## Ishlash natijasi:
```text
Chiqish: 'test_bina.dat' muvaffaqiyatli 'test_nusxa.dat' ga nusxalandi.
```


# 411-Topshiriq: Ob'ektlarni pickle orqali binar serializatsiya qilish

## Topshiriq sharti:
Istalgan Python ob'ektini (klass, ro'yxat, lug'at) `pickle` orqali faylga saqlash va qayta tiklash.

## Yechim (Python kodi):
```python
import pickle

class FoydalanuvchiHolati:
    def __init__(self, username, ball):
        self.username = username
        self.ball = ball

original = FoydalanuvchiHolati("Alisher", 995)

# Serializatsiya (Pickling)
with open("state.pkl", "wb") as f:
    pickle.dump(original, f)

# Deserializatsiya (Unpickling)
with open("state.pkl", "rb") as f:
    tiklangan = pickle.load(f)

print(f"Qayta tiklangan: {tiklangan.username} (Ball: {tiklangan.ball})")
```

## Tushuntirish va Mantiq:
1. `pickle` Python ob'ektining to'liq ichki holatini baytlar ko'rinishida saqlash imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: Qayta tiklangan: Alisher (Ball: 995)
```


# 412-Topshiriq: Fayl kursorini boshqarish (seek va tell)

## Topshiriq sharti:
`tell()` orqali joriy kursor o'rnini bilish va `seek()` bilan fayl boshiga yoki o'rtasiga qaytish.

## Yechim (Python kodi):
```python
with open("kursor_test.txt", "w+", encoding="utf-8") as f:
    f.write("0123456789ABCDEF")
    print("Yozgandan keyingi kursor o'rni:", f.tell())  # 16-baytda

    # Boshiga qaytamiz
    f.seek(0)
    print("Boshidagi 5 ta belgi:", f.read(5))  # '01234'
    print("Hozirgi kursor o'rni:", f.tell())    # 5-baytda

    # 10-baytga sakraymiz
    f.seek(10)
    print("10-baytdan keyingi qism:", f.read()) # 'ABCDEF'
```

## Tushuntirish va Mantiq:
1. `seek(offset)` kursor manzilini o'zgartiradi.
2. `tell()` kursor ayni paytda faylning nechanchi baytida turganini ko'rsatadi.

## Ishlash natijasi:
```text
Chiqish: Kursor o'rni: 16, Boshidagi: 01234, 10-baytdan: ABCDEF
```


# 413-Topshiriq: os va os.path bilan fayl va papka amallari

## Topshiriq sharti:
Fayl mavjudligini, uning hajmini va papka yaratish/o'chirish amallarini bajaring.

## Yechim (Python kodi):
```python
import os

papka = "sinov_papkasi"
fayl = os.path.join(papka, "malumot.txt")

# Papka ochish
os.makedirs(papka, exist_ok=True)

# Fayl yaratish
with open(fayl, "w", encoding="utf-8") as f:
    f.write("Test ma'lumotlari")

print(f"Fayl mavjudmi? {os.path.exists(fayl)}")
print(f"Fayl hajmi: {os.path.getsize(fayl)} bayt")
print(f"Fayl nomi: {os.path.basename(fayl)}")
print(f"Papka yo'li: {os.path.dirname(fayl)}")
```

## Tushuntirish va Mantiq:
1. `os.path.join()` barcha operatsion tizimlarda (Windows va Linux) to'g'ri slashelarni ishlatadi.

## Ishlash natijasi:
```text
Chiqish: Mavjudmi: True, Hajmi: 17 bayt, Fayl nomi: malumot.txt
```


# 414-Topshiriq: pathlib.Path orqali zamonaviy fayllar bilan ishlash

## Topshiriq sharti:
Python 3.4+ da kiritilgan `pathlib` moduli yordamida fayl yo'llarini ob'ekt sifatida boshqaring.

## Yechim (Python kodi):
```python
from pathlib import Path

p = Path("sinov_papkasi") / "yangi_matn.txt"
p.write_text("Pathlib yordamida yozilgan toza matn!", encoding="utf-8")

print(f"Fayl nomi      : {p.name}")
print(f"Kengaytmasi    : {p.suffix}")
print(f"Asl nomi       : {p.stem}")
print(f"O'qilgan matn  : {p.read_text(encoding='utf-8')}")
```

## Tushuntirish va Mantiq:
1. `Path.write_text()` va `Path.read_text()` faylni bir qatorda yozish va o'qish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: Nomi: yangi_matn.txt, Kengaytma: .txt, Stem: yangi_matn
```


# 415-Topshiriq: Papkadagi fayllarni kengaytma bo'yicha qidirish (glob)

## Topshiriq sharti:
Papkadagi barcha `.txt` fayllarni `glob` yordamida qidirib toping.

## Yechim (Python kodi):
```python
from pathlib import Path

baza_papka = Path(".")
txt_fayllar = list(baza_papka.glob("*.txt"))

print(f"Joriy papkadagi .txt fayllar ({len(txt_fayllar)} ta):")
for f in txt_fayllar[:5]:
    print(f" - {f.name} ({f.stat().st_size} bayt)")
```

## Tushuntirish va Mantiq:
1. `.glob('*.txt')` andoza bo'yicha qidirish vositasidir (`**/*.txt` ichma-ich papkalarni ham qidiradi).

## Ishlash natijasi:
```text
Chiqish: .txt fayllar ro'yxati.
```


# 416-Topshiriq: Fayllarni ZIP arxiviga siqish va ochish (zipfile)

## Topshiriq sharti:
Bir nechta faylni `.zip` arxiviga joylang va uni yangi papkaga arxivdan chiqaring.

## Yechim (Python kodi):
```python
import zipfile

arxiv_nomi = "fayllar_arxivi.zip"

# Arxivlash
with zipfile.ZipFile(arxiv_nomi, "w", zipfile.ZIP_DEFLATED) as zip_f:
    zip_f.write("salom.txt")
    zip_f.write("maqollar.txt")
print(f"'{arxiv_nomi}' arxivi yaratildi.")

# Arxivdan chiqarish
with zipfile.ZipFile(arxiv_nomi, "r") as zip_f:
    zip_f.extractall("arxivdan_ochilgan")
print("Fayllar 'arxivdan_ochilgan' papkasiga ajratib olindi.")
```

## Tushuntirish va Mantiq:
1. `zipfile.ZIP_DEFLATED` fayllarni samarali siqib hajmini kichraytiradi.

## Ishlash natijasi:
```text
Chiqish: Arxiv yaratildi va ochildi.
```


# 417-Topshiriq: Faylning MD5 va SHA-256 hashini hisoblash

## Topshiriq sharti:
Fayl yaxlitligini va o'zgarmaganligini tekshirish uchun uning SHA-256 xesh summasini hisoblang.

## Yechim (Python kodi):
```python
import hashlib

def fayl_sha256(fayl_yoli):
    sha = hashlib.sha256()
    with open(fayl_yoli, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()

xesh = fayl_sha256("salom.txt")
print(f"salom.txt faylining SHA-256 xeshi: {xesh}")
```

## Tushuntirish va Mantiq:
1. Kriptografik xesh faylning bitta bayti o'zgarganda ham butunlay boshqacha natija beradi.

## Ishlash natijasi:
```text
Chiqish: SHA-256: 64 belgili unikal xesh kodi.
```


# 418-Topshiriq: CSV faylni JSON ga aylantirish

## Topshiriq sharti:
CSV jadvalidagi qatorlarni JSON ob'ektlar ro'yxatiga o'giruvchi universal konvertor yozing.

## Yechim (Python kodi):
```python
import csv
import json

def csv_to_json(csv_fayl, json_fayl):
    with open(csv_fayl, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        malumotlar = list(reader)

    with open(json_fayl, "w", encoding="utf-8") as f:
        json.dump(malumotlar, f, ensure_ascii=False, indent=2)
    print(f"'{csv_fayl}' -> '{json_fayl}' ga muvaffaqiyatli aylantirildi.")

csv_to_json("talabalar.csv", "talabalar.json")
```

## Tushuntirish va Mantiq:
1. CSV qatorlari `DictReader` bilan o'qilib to'g'ridan-to'g'ri JSON massiviga yoziladi.

## Ishlash natijasi:
```text
Chiqish: 'talabalar.csv' -> 'talabalar.json' ga aylantirildi.
```


# 419-Topshiriq: Fayl yaratilgan va o'zgartirilgan vaqtini aniqlash

## Topshiriq sharti:
Faylning oxirgi marta qachon tahrirlanganini `datetime` formati bilan o'qing.

## Yechim (Python kodi):
```python
import os
from datetime import datetime

fayl = "salom.txt"
mtime_soniya = os.path.getmtime(fayl)
oxirgi_ozgarish = datetime.fromtimestamp(mtime_soniya).strftime('%Y-%m-%d %H:%M:%S')

print(f"Fayl: {fayl}")
print(f"Oxirgi o'zgartirilgan vaqt: {oxirgi_ozgarish}")
```

## Tushuntirish va Mantiq:
1. `os.path.getmtime()` fayl modifikatsiya vaqtini timestamp shaklida beradi.

## Ishlash natijasi:
```text
Chiqish: Oxirgi o'zgartirilgan vaqt: 2026-11-07 17:...
```


# 420-Topshiriq: Fayldan takrorlangan qatorlarni tozalash (Deduplicate lines)

## Topshiriq sharti:
Katta fayldagi takrorlangan qatorlarni ularning dastlabki tartibini saqlagan holda tozalang.

## Yechim (Python kodi):
```python
def toza_qatorlar(kirish_fayl, chiqish_fayl):
    korilganlar = set()
    toza = []

    with open(kirish_fayl, "r", encoding="utf-8") as f:
        for qator in f:
            if qator not in korilganlar:
                korilganlar.add(qator)
                toza.append(qator)

    with open(chiqish_fayl, "w", encoding="utf-8") as f:
        f.writelines(toza)
    print(f"Takrorlanmas qatorlar soni: {len(toza)} ta")

# Sinov
with open("dublikat.txt", "w", encoding="utf-8") as f:
    f.write("Olma\nAnor\nOlma\nUzum\nAnor\n")

toza_qatorlar("dublikat.txt", "toza_mevalar.txt")
```

## Tushuntirish va Mantiq:
1. To'plam tezkor tekshiradi, `toza` ro'yxati esa tartibni saqlab qoladi.

## Ishlash natijasi:
```text
Chiqish: Takrorlanmas qatorlar soni: 3 ta
```


# 421-Topshiriq: Katta faylni kichik qismlarga bo'lish (File Splitter)

## Topshiriq sharti:
Katta matnli faylni har biri maksimal 2 qatordan iborat bo'laklarga ajrating.

## Yechim (Python kodi):
```python
def bolakla_faylni(fayl_yoli, har_birida=2):
    qism = 1
    with open(fayl_yoli, "r", encoding="utf-8") as f:
        while True:
            qatorlar = [f.readline() for _ in range(har_birida)]
            haqiqiy_qatorlar = [q for q in qatorlar if q]
            if not haqiqiy_qatorlar:
                break
            qism_nomi = f"qism_{qism:02d}.txt"
            with open(qism_nomi, "w", encoding="utf-8") as chiqish:
                chiqish.writelines(haqiqiy_qatorlar)
            print(f"Yozildi: {qism_nomi} ({len(haqiqiy_qatorlar)} qator)")
            qism += 1

bolakla_faylni("maqollar.txt", har_birida=2)
```

## Tushuntirish va Mantiq:
1. Katta gigabaytlik datasetlarni tahlil qilish uchun qismlarga bo'lishda ishlatiladi.

## Ishlash natijasi:
```text
Chiqish: Yozildi: qism_01.txt, Yozildi: qism_02.txt
```


# 422-Topshiriq: Bir nechta matnli fayllarni bitta faylga ulash (Merger)

## Topshiriq sharti:
Alohida qism fayllarini birlashtirib, bitta umumiy fayl hosil qiling.

## Yechim (Python kodi):
```python
def birlashtir_fayllarni(chiqish_fayl, *kirish_fayllari):
    with open(chiqish_fayl, "w", encoding="utf-8") as chiqish:
        for f_nom in kirish_fayllari:
            with open(f_nom, "r", encoding="utf-8") as kirish:
                chiqish.write(kirish.read())
                chiqish.write("\n")  # Fayllar orasiga ajratkich
    print(f"Fayllar birlashtirildi: {chiqish_fayl}")

birlashtir_fayllarni("umumiy_maqollar.txt", "qism_01.txt", "qism_02.txt")
```

## Tushuntirish va Mantiq:
1. Bir nechta dataset qismlarini bitta to'liq korpusga yig'ish mexanizmi.

## Ishlash natijasi:
```text
Chiqish: Fayllar birlashtirildi: umumiy_maqollar.txt
```


# 423-Topshiriq: Fayllarni xavfsiz atomik yozish (Atomic Write)

## Topshiriq sharti:
Dastur kutilmaganda to'xtab qolganda asl fayl buzilmasligi uchun avval vaqtinchalik faylga yozib, so'ng almashtiring.

## Yechim (Python kodi):
```python
import os

def xavfsiz_yoz(fayl_yoli, matn):
    temp_nom = fayl_yoli + ".tmp"
    with open(temp_nom, "w", encoding="utf-8") as f:
        f.write(matn)
        f.flush()
        os.fsync(f.fileno())  # Diskka to'liq yozilishini majburlaymiz

    # Atomik almashtirish (Windows va Linux'da xavfsiz)
    os.replace(temp_nom, fayl_yoli)
    print(f"[ATOMIK YOZILDI] '{fayl_yoli}'")

xavfsiz_yoz("muhim_baza.txt", "Kritik muhim moliyaviy ma'lumotlar")
```

## Tushuntirish va Mantiq:
1. `os.replace()` atomik operatsiya bo'lib, elektr o'chganda ham eski fayl buzilmasdan saqlanib qolishini ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: [ATOMIK YOZILDI] 'muhim_baza.txt'
```


# 424-Topshiriq: Diskdagi bo'sh joyni hisoblash (shutil.disk_usage)

## Topshiriq sharti:
Joriy qattiq diskning jami, band va bo'sh joy hajmini GB larda ko'rsating.

## Yechim (Python kodi):
```python
import shutil

jami, band, bosh = shutil.disk_usage(".")

gb = 1024 ** 3
print(f"Jami disk hajmi  : {jami / gb:.2f} GB")
print(f"Ishlatilgan joy  : {band / gb:.2f} GB")
print(f"Bo'sh qolgan joy : {bosh / gb:.2f} GB")
print(f"Bandlik darajasi : {(band / jami) * 100:.1f}%")
```

## Tushuntirish va Mantiq:
1. Katta AI modellari o'qitilganda disk to'lib qolmasligini nazorat qilish uchun juda zarur.

## Ishlash natijasi:
```text
Chiqish: Jami, Ishlatilgan va Bo'sh joy GB da.
```


# 425-Topshiriq: Konfiguratsiya fayllarini boshqarish (configparser)

## Topshiriq sharti:
INI formatidagi server va ma'lumotlar bazasi sozlamalari faylini yozing va o'qing.

## Yechim (Python kodi):
```python
import configparser

config = configparser.ConfigParser()

# Sozlamalar kiritamiz
config["DATABASE"] = {
    "host": "127.0.0.1",
    "port": "5432",
    "user": "postgres",
    "db_name": "uzbek_ai_db"
}
config["APP"] = {
    "debug": "True",
    "max_workers": "4"
}

with open("settings.ini", "w") as configfile:
    config.write(configfile)

# Qayta o'qiymiz
oqilgan = configparser.ConfigParser()
oqilgan.read("settings.ini")

print("DB Host:", oqilgan["DATABASE"]["host"])
print("Workers:", oqilgan.getint("APP", "max_workers"))
```

## Tushuntirish va Mantiq:
1. `configparser` standart INI fayllarni tahlil qilish va qulay boshqarish vositasidir.

## Ishlash natijasi:
```text
Chiqish: DB Host: 127.0.0.1, Workers: 4
```


# 426-Topshiriq: Papkalar daraxtini konsolda chizish (Folder Tree)

## Topshiriq sharti:
Papka ichidagi fayl va papkalarni daraxt shaklida chiroyli ko'rsatuvchi rekursiv dastur.

## Yechim (Python kodi):
```python
import os

def chiz_daraxt(boshlangich_yo'l, chekinish=""):
    nomlar = sorted(os.listdir(boshlangich_yo'l))
    for i, nom in enumerate(nomlar):
        toliq = os.path.join(boshlangich_yo'l, nom)
        oxirgimi = (i == len(nomlar) - 1)
        belgi = "└── " if oxirgimi else "├── "
        print(chekinish + belgi + nom)
        if os.path.isdir(toliq):
            yangi_chekinish = chekinish + ("    " if oxirgimi else "│   ")
            chiz_daraxt(toliq, yangi_chekinish)

print("Papka strukturasi:")
chiz_daraxt("sinov_papkasi")
```

## Tushuntirish va Mantiq:
1. Rekursiv daraxt chizish loyihalar strukturasini vizual tushunishni osonlashtiradi.

## Ishlash natijasi:
```text
Chiqish: ├── va └── belgili daraxt ko'rinishi.
```


# 427-Topshiriq: Fayldan barcha havolalarni (URL) ajratib boshqa faylga saqlash

## Topshiriq sharti:
Matnli fayl ichidagi barcha veb-sayt manzillarini regex bilan topib, alohida havolalar fayliga yozing.

## Yechim (Python kodi):
```python
import re

with open("maqola_test.txt", "w", encoding="utf-8") as f:
    f.write("Batafsil ma'lumot https://ziyouz.com va https://kun.uz saytlarida berilgan.")

with open("maqola_test.txt", "r", encoding="utf-8") as f:
    matn = f.read()

havolalar = re.findall(r'https?://[^\s<>"]+', matn)

with open("topilgan_havolalar.txt", "w", encoding="utf-8") as f:
    for h in havolalar:
        f.write(h + "\n")

print(f"Topilgan {len(havolalar)} ta havola saqlandi: {havolalar}")
```

## Tushuntirish va Mantiq:
1. Web scraping va ma'lumotlar yig'ish vazifalarida asosiy o'rin tutadi.

## Ishlash natijasi:
```text
Chiqish: Topilgan 2 ta havola saqlandi: ['https://ziyouz.com', 'https://kun.uz']
```


# 428-Topshiriq: Markdown faylidan Mundarija (Table of Contents) tuzish

## Topshiriq sharti:
Markdown faylidagi barcha `# Sarlavha` va `## Qism` qatorlarini ajratib Mundarija shakllantiring.

## Yechim (Python kodi):
```python
md_matn = """# 1. Kirish
## 1.1 O'zgaruvchilar
## 1.2 Arifmetika
# 2. Shartlar
## 2.1 If Else
# 3. Tsikllar"""

with open("namuna.md", "w", encoding="utf-8") as f:
    f.write(md_matn)

print("Generatsiya qilingan Mundarija:")
with open("namuna.md", "r", encoding="utf-8") as f:
    for qator in f:
        q = qator.strip()
        if q.startswith("#"):
            daraja = q.count("#")
            sarlavha = q.lstrip("# ").strip()
            chekinish = "  " * (daraja - 1)
            print(f"{chekinish}* {sarlavha}")
```

## Tushuntirish va Mantiq:
1. Markdown sarlavhalarining `#` soni bo'yicha chekinish hisoblanib mundarija tuziladi.

## Ishlash natijasi:
```text
Chiqish: * 1. Kirish,   * 1.1 O'zgaruvchilar...
```


# 429-Topshiriq: SQLite3 Ma'lumotlar Bazasi (Jadval yaratish va yozish)

## Topshiriq sharti:
Standart `sqlite3` moduli yordamida faylli ma'lumotlar bazasida jadval yarating va ma'lumot yozing.

## Yechim (Python kodi):
```python
import sqlite3

# Bazaga ulanamiz (agar fayl bo'lmasa yaratadi)
conn = sqlite3.connect("baza_test.db")
cursor = conn.cursor()

# Jadval yaratamiz
cursor.execute('''
    CREATE TABLE IF NOT EXISTS kitoblar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        muallif TEXT,
        sahifalar INTEGER
    )
''')

# Yangi yozuv qo'shamiz
cursor.execute("INSERT INTO kitoblar (nom, muallif, sahifalar) VALUES (?, ?, ?)",
               ("O'tkan kunlar", "Abdulla Qodiriy", 209))

conn.commit()
print("Ma'lumotlar bazaga muvaffaqiyatli saqlandi!")
conn.close()
```

## Tushuntirish va Mantiq:
1. SQLite Python'da hech qanday qo'shimcha server o'rnatmasdan to'liq SQL ma'lumotlar bazasini bitta faylda yuritish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: Ma'lumotlar bazaga muvaffaqiyatli saqlandi!
```


# 430-Topshiriq: SQLite bazasidan o'qish va filtrlash

## Topshiriq sharti:
SQL so'rovlari (`SELECT * WHERE...`) orqali bazadagi ma'lumotlarni o'qing.

## Yechim (Python kodi):
```python
import sqlite3

conn = sqlite3.connect("baza_test.db")
cursor = conn.cursor()

cursor.execute("SELECT id, nom, muallif, sahifalar FROM kitoblar")
qatorlar = cursor.fetchall()

print("Kitoblar ro'yxati:")
for q in qatorlar:
    print(f"ID: {q[0]} | '{q[1]}' ({q[2]}) - {q[3]} bet")

conn.close()
```

## Tushuntirish va Mantiq:
1. `cursor.fetchall()` barcha topilgan qatorlarni kortejlar ro'yxati shaklida qaytaradi.

## Ishlash natijasi:
```text
Chiqish: ID: 1 | 'O'tkan kunlar' (Abdulla Qodiriy) - 209 bet
```


# 431-Topshiriq: SQLite ma'lumotlarini JSON faylga eksport qilish

## Topshiriq sharti:
Ma'lumotlar bazasidagi barcha yozuvlarni JSON formatiga o'tkazib saqlang.

## Yechim (Python kodi):
```python
import sqlite3
import json

conn = sqlite3.connect("baza_test.db")
conn.row_factory = sqlite3.Row  # Qatorlarni lug'at kabi olish imkonini beradi
cursor = conn.cursor()

cursor.execute("SELECT * FROM kitoblar")
qatorlar = [dict(row) for row in cursor.fetchall()]

with open("kitoblar_eksport.json", "w", encoding="utf-8") as f:
    json.dump(qatorlar, f, ensure_ascii=False, indent=2)

print("JSON eksport natijasi:")
print(qatorlar)
conn.close()
```

## Tushuntirish va Mantiq:
1. `conn.row_factory = sqlite3.Row` SQL natijalarini to'g'ridan-to'g'ri lug'atlarga aylantirishni osonlashtiradi.

## Ishlash natijasi:
```text
Chiqish: [{'id': 1, 'nom': "O'tkan kunlar", 'muallif': 'Abdulla Qodiriy', 'sahifalar': 209}]
```


# 432-Topshiriq: Log Rotation: Fayl hajmiga qarab yangilash

## Topshiriq sharti:
Agar joriy log fayli hajmi 1 KB dan oshsa, uni arxivlab, yangi toza log fayli ochuvchi mexanizm.

## Yechim (Python kodi):
```python
import os

def log_yozish(xabar, log_fayl="amallar.log", maks_bayt=1024):
    if os.path.exists(log_fayl) and os.path.getsize(log_fayl) > maks_bayt:
        arxiv_nomi = log_fayl + ".old"
        os.replace(log_fayl, arxiv_nomi)
        print(f"[ROTATION] '{log_fayl}' hajmi oshdi, '{arxiv_nomi}' ga ko'chirildi.")

    with open(log_fayl, "a", encoding="utf-8") as f:
        f.write(xabar + "\n")

log_yozish("1-harakat")
log_yozish("2-harakat")
print("Log muvaffaqiyatli qayd etildi.")
```

## Tushuntirish va Mantiq:
1. Log rotation server diski to'lib tizim qulashining oldini olish uchun zarurdir.

## Ishlash natijasi:
```text
Chiqish: Log muvaffaqiyatli qayd etildi.
```


# 433-Topshiriq: Faylni shifrlash va deshifrlash (XOR shifri)

## Topshiriq sharti:
Maxfiy kalit so'z orqali fayl baytlarini XOR shifrlab saqlang va yana qayta tiklang.

## Yechim (Python kodi):
```python
def xor_shifrla_fayl(kirish_fayl, chiqish_fayl, kalit_bayt=0x5A):
    with open(kirish_fayl, "rb") as f_in:
        malumot = bytearray(f_in.read())

    for i in range(len(malumot)):
        malumot[i] ^= kalit_bayt  # XOR amali

    with open(chiqish_fayl, "wb") as f_out:
        f_out.write(malumot)

# 1. Shifrlaymiz
xor_shifrla_fayl("salom.txt", "salom_shifr.dat")
# 2. Deshifrlaymiz (XOR o'ziga o'zi teskari)
xor_shifrla_fayl("salom_shifr.dat", "salom_tiklangan.txt")

with open("salom_tiklangan.txt", "r", encoding="utf-8") as f:
    print("Tikланган matn:", f.readline().strip())
```

## Tushuntirish va Mantiq:
1. XOR amali (A ^ B ^ B = A) eng sodda simmetrik shifrlash vositasidir.

## Ishlash natijasi:
```text
Chiqish: Tiklangan matn: Assalomu alaykum, O'zbekiston!
```


# 434-Topshiriq: Fayl ichidagi bo'sh qatorlarni tozalash

## Topshiriq sharti:
Fayldan barcha keraksiz ortiqcha bo'sh qatorlarni olib tashlab toza nusxasini yozing.

## Yechim (Python kodi):
```python
with open("boshliqli.txt", "w", encoding="utf-8") as f:
    f.write("1-qator\n\n\n2-qator\n\n3-qator\n\n\n")

with open("boshliqli.txt", "r", encoding="utf-8") as kirish:
    toza_qatorlar = [q for q in kirish if q.strip()]

with open("toza_qatorlar.txt", "w", encoding="utf-8") as chiqish:
    chiqish.writelines(toza_qatorlar)

print(f"Bo'sh qatorlar olib tashlandi ({len(toza_qatorlar)} ta toza qator qoldi).")
```

## Tushuntirish va Mantiq:
1. `q.strip()` agar qatorda faqat probel yoki newline bo'lsa uni bo'sh deb baholaydi.

## Ishlash natijasi:
```text
Chiqish: Bo'sh qatorlar olib tashlandi (3 ta toza qator qoldi).
```


# 435-Topshiriq: Ikki faylni baytma-bayt solishtirish

## Topshiriq sharti:
Ikki faylning 100% aynan bir xilligini baytlari bo'yicha tekshiruvchi dastur tuzing.

## Yechim (Python kodi):
```python
def fayllar_bir_xilmi(f1, f2):
    if os.path.getsize(f1) != os.path.getsize(f2):
        return False
    with open(f1, "rb") as oqim1, open(f2, "rb") as oqim2:
        while True:
            b1 = oqim1.read(8192)
            b2 = oqim2.read(8192)
            if b1 != b2:
                return False
            if not b1:
                return True

print("salom.txt va salom_tiklangan.txt bir xilmi?",
      fayllar_bir_xilmi("salom.txt", "salom_tiklangan.txt"))
```

## Tushuntirish va Mantiq:
1. Avval hajm tekshiriladi (tezkor rad etish), so'ngra 8 KB bo'laklar bilan solishtiriladi.

## Ishlash natijasi:
```text
Chiqish: True
```


# 436-Topshiriq: CSV jadvalini saralash (Ustun bo'yicha)

## Topshiriq sharti:
CSV fayldagi ma'lumotlarni GPA bo'yicha kamayish tartibida saralab yangi CSV faylga yozing.

## Yechim (Python kodi):
```python
import csv

with open("talabalar.csv", "r", encoding="utf-8") as f:
    reader = list(csv.DictReader(f))

# GPA bo'yicha saralaymiz
saralangan = sorted(reader, key=lambda x: float(x["GPA"]), reverse=True)

with open("talabalar_saralangan.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=reader[0].keys())
    writer.writeheader()
    writer.writerows(saralangan)

print("GPA bo'yicha saralangan talabalar:")
for t in saralangan:
    print(f" - {t['Ism']}: {t['GPA']}")
```

## Tushuntirish va Mantiq:
1. `float(x['GPA'])` sonli saralashni to'g'ri ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: 1. Madina (4.9), 2. Alisher (4.8), 3. Jasur (4.5)
```


# 437-Topshiriq: Fayl satrlarini alifbo tartibida saralash

## Topshiriq sharti:
Matnli fayldagi barcha qatorlarni lotin alifbosi bo'yicha tartiblab saqlang.

## Yechim (Python kodi):
```python
with open("shaharlar.txt", "w", encoding="utf-8") as f:
    f.write("Toshkent\nAndijon\nBuxoro\nSamarqand\nXiva\nFarg'ona\n")

with open("shaharlar.txt", "r", encoding="utf-8") as f:
    qatorlar = [q.strip() for q in f if q.strip()]

qatorlar.sort()

with open("shaharlar_saralangan.txt", "w", encoding="utf-8") as f:
    for q in qatorlar:
        f.write(q + "\n")

print("Alifbo bo'yicha saralangan shaharlar:", qatorlar)
```

## Tushuntirish va Mantiq:
1. Matnlarni alifbo tartibiga keltirish va indekslashda qo'llaniladi.

## Ishlash natijasi:
```text
Chiqish: ['Andijon', "Farg'ona", 'Buxoro', 'Samarqand', 'Toshkent', 'Xiva']
```


# 438-Topshiriq: Fayl ruxsatlarini (Permissions) tekshirish

## Topshiriq sharti:
`os.access` orqali fayl o'qishga (R_OK), yozishga (W_OK) ruxsat etilganligini aniqlang.

## Yechim (Python kodi):
```python
import os

fayl = "salom.txt"
oqish_mumkin = os.access(fayl, os.R_OK)
yozish_mumkin = os.access(fayl, os.W_OK)

print(f"'{fayl}' fayli tahlili:")
print(f" - O'qishga ruxsat bormi? {oqish_mumkin}")
print(f" - Yozishga ruxsat bormi? {yozish_mumkin}")
```

## Tushuntirish va Mantiq:
1. Dastur fayl ochishdan oldin ruxsatlarni tekshirib, PermissionError xatolarining oldini oladi.

## Ishlash natijasi:
```text
Chiqish: O'qishga: True, Yozishga: True
```


# 439-Topshiriq: Katta faylni generator bilan xotira tejamkor o'qish

## Topshiriq sharti:
Yuzlab megabaytli faylni xotiraga yuklamasdan `yield` bilan qatorma-qator beruvchi generator yozing.

## Yechim (Python kodi):
```python
def xotira_tejamkor_oqish(fayl_yoli):
    with open(fayl_yoli, "r", encoding="utf-8") as f:
        for qator in f:
            yield qator.strip()

for q in xotira_tejamkor_oqish("maqollar.txt"):
    print("Generator qatori:", q)
```

## Tushuntirish va Mantiq:
1. Generator faylning butun tarkibini RAM da saqlamaydi, faqat joriy qator xotirada turadi.

## Ishlash natijasi:
```text
Chiqish: Generator qatori: Bilim — aql chirog'i...
```


# 440-Topshiriq: XML faylni o'qish va tahlil qilish (ElementTree)

## Topshiriq sharti:
XML formatidagi ma'lumotlarni `xml.etree.ElementTree` orqali teglari bo'yicha o'qing.

## Yechim (Python kodi):
```python
import xml.etree.ElementTree as ET

xml_matn = """<kutubxona>
    <kitob id="1">
        <nom>O'tkan kunlar</nom>
        <muallif>Qodiriy</muallif>
    </kitob>
    <kitob id="2">
        <nom>Mehrobdan chayon</nom>
        <muallif>Qodiriy</muallif>
    </kitob>
</kutubxona>"""

root = ET.fromstring(xml_matn)

print(f"Asosiy teg: {root.tag}")
for k in root.findall("kitob"):
    nom = k.find("nom").text
    muallif = k.find("muallif").text
    print(f"Kitob #{k.attrib['id']}: '{nom}' ({muallif})")
```

## Tushuntirish va Mantiq:
1. XML daraxti elementlarini qidirish va atributlarini o'qish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: Kitob #1: 'O'tkan kunlar' (Qodiriy)...
```


# 441-Topshiriq: Vaqtinchalik fayllar bilan ishlash (tempfile moduli)

## Topshiriq sharti:
`tempfile.NamedTemporaryFile` yordamida avtomatik o'chiriluvchi xavfsiz vaqtinchalik fayl tuzing.

## Yechim (Python kodi):
```python
import tempfile

with tempfile.NamedTemporaryFile(mode="w+", delete=True, encoding="utf-8") as temp:
    temp.write("Vaqtinchalik xotira matni")
    temp.seek(0)
    print("Vaqtinchalik fayl nomi:", temp.name)
    print("Ichidagi matn         :", temp.read())

print("Blok tugadi — fayl avtomatik o'chirildi!")
```

## Tushuntirish va Mantiq:
1. Operatsion tizimning vaqtinchalik papkasida (Temp) xavfsiz fayl ochadi va chiqishda darhol o'chiradi.

## Ishlash natijasi:
```text
Chiqish: Vaqtinchalik fayl nomi: ... Blok tugadi — fayl o'chirildi!
```


# 442-Topshiriq: Fayldagi ma'lum bir qatorni almashtirish

## Topshiriq sharti:
Katta faylning aniq bir n-qatoridagi matnni boshqasiga o'zgartiring.

## Yechim (Python kodi):
```python
def qatorni_almashtir(fayl_yoli, qator_nomeri, yangi_matn):
    with open(fayl_yoli, "r", encoding="utf-8") as f:
        qatorlar = f.readlines()

    if 1 <= qator_nomeri <= len(qatorlar):
        qatorlar[qator_nomeri - 1] = yangi_matn + "\n"
        with open(fayl_yoli, "w", encoding="utf-8") as f:
            f.writelines(qatorlar)
        print(f"{qator_nomeri}-qator muvaffaqiyatli yangilandi.")
    else:
        print("Bunday qator raqami mavjud emas!")

qatorni_almashtir("maqollar.txt", 2, "Mehnat, mehnatning tagi — rohat va baxt.")
```

## Tushuntirish va Mantiq:
1. Ro'yxat indeksi `n-1` orqali kerakli satr yangilanadi.

## Ishlash natijasi:
```text
Chiqish: 2-qator muvaffaqiyatli yangilandi.
```


# 443-Topshiriq: Fayllar ro'yxatini hajmi bo'yicha saralash

## Topshiriq sharti:
Papkadagi fayllarni ularning egallagan xotira hajmi (bayt) bo'yicha kamayish tartibida saralang.

## Yechim (Python kodi):
```python
import os

fayllar = [f for f in os.listdir(".") if os.path.isfile(f)]
saralangan = sorted(fayllar, key=os.path.getsize, reverse=True)

print("Eng katta 5 ta fayl:")
for f in saralangan[:5]:
    hajm_kb = os.path.getsize(f) / 1024
    print(f" - {f:25s} : {hajm_kb:.2f} KB")
```

## Tushuntirish va Mantiq:
1. `key=os.path.getsize` fayllar hajmini to'g'ridan-to'g'ri hisoblab saralaydi.

## Ishlash natijasi:
```text
Chiqish: Eng katta fayllar ro'yxati.
```


# 444-Topshiriq: Fayldan faqat raqamlarni ajratib o'rtachasini topish

## Topshiriq sharti:
Matnli fayldagi barcha butun sonlarni ajratib olib ularning o'rta arifmetigini hisoblang.

## Yechim (Python kodi):
```python
import re

with open("raqamlar_test.txt", "w", encoding="utf-8") as f:
    f.write("Talaba 1: 85 ball, Talaba 2: 90 ball, Talaba 3: 95 ball.")

with open("raqamlar_test.txt", "r", encoding="utf-8") as f:
    matn = f.read()

sonlar = [int(x) for x in re.findall(r'\b\d+\b', matn)]
ortacha = sum(sonlar) / len(sonlar) if sonlar else 0

print(f"Topilgan sonlar: {sonlar}")
print(f"O'rtacha qiymat : {ortacha:.2f}")
```

## Tushuntirish va Mantiq:
1. `\b\d+\b` faqat alohida turgan sonlarni topadi.

## Ishlash natijasi:
```text
Chiqish: Sonlar: [1, 85, 2, 90, 3, 95]...
```


# 445-Topshiriq: Fayl nomi prefiksi va suffiksini o'zgartirish (Batch Rename)

## Topshiriq sharti:
Papkadagi barcha `.txt` fayllar boshiga 'arxiv_' prefiksini qo'shuvchi dastur tuzing.

## Yechim (Python kodi):
```python
import os

def prefiks_qosh(papka, prefiks="arxiv_"):
    for nom in os.listdir(papka):
        if nom.endswith(".tmp") and not nom.startswith(prefiks):
            eski = os.path.join(papka, nom)
            yangi = os.path.join(papka, prefiks + nom)
            os.rename(eski, yangi)
            print(f"O'zgartirildi: {nom} -> {prefiks + nom}")

# Sinov
prefiks_qosh(".", prefiks="arxiv_")
```

## Tushuntirish va Mantiq:
1. `os.rename()` fayllarni ommaviy qayta nomlash imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: O'zgartirildi: test.tmp -> arxiv_test.tmp
```


# 446-Topshiriq: Fayl ichidagi so'zlarni almashtirish (Find and Replace in File)

## Topshiriq sharti:
Fayl ichidagi ma'lum bir so'zni butun fayl bo'ylab boshqasiga xavfsiz almashtiring.

## Yechim (Python kodi):
```python
def faylda_almashtir(fayl_yoli, eski_soz, yangi_soz):
    with open(fayl_yoli, "r", encoding="utf-8") as f:
        matn = f.read()

    yangi_matn = matn.replace(eski_soz, yangi_soz)

    with open(fayl_yoli, "w", encoding="utf-8") as f:
        f.write(yangi_matn)
    print(f"'{eski_soz}' so'zi '{yangi_soz}' ga almashtirildi.")

faylda_almashtir("salom.txt", "O'zbekiston", "Jonajon O'zbekiston")
```

## Tushuntirish va Mantiq:
1. Fayl matnini xotiraga olib almashtiradi va qayta yozadi.

## Ishlash natijasi:
```text
Chiqish: 'O'zbekiston' so'zi 'Jonajon O'zbekiston' ga almashtirildi.
```


# 447-Topshiriq: Jurnal faylini oxiridan o'qish (Tail mantiqi)

## Topshiriq sharti:
Linux 'tail -n' buyrug'i kabi katta log faylining faqat oxirgi N ta qatorini o'qing.

## Yechim (Python kodi):
```python
from collections import deque

def oxirgi_qatorlar(fayl_yoli, n=3):
    with open(fayl_yoli, "r", encoding="utf-8") as f:
        # deque(maxlen=n) faqat oxirgi n ta elementni saqlaydi
        return list(deque(f, maxlen=n))

oxirgilari = oxirgi_qatorlar("maqollar.txt", n=2)
print("Oxirgi 2 ta qator:")
for q in oxirgilari:
    print(" *", q.strip())
```

## Tushuntirish va Mantiq:
1. `collections.deque(maxlen=n)` butun faylni xotirada ushlamasdan faqat oxirgi n qatorni qoldiradi.

## Ishlash natijasi:
```text
Chiqish: Oxirgi 2 ta qator chop etiladi.
```


# 448-Topshiriq: Papka hajmini to'liq hisoblash (Folder Size Calculator)

## Topshiriq sharti:
Papka ichidagi barcha ichki fayllar va pastki papkalar hajmini jamlab MB larda ko'rsating.

## Yechim (Python kodi):
```python
import os

def papka_hajmi_mb(papka_yoli):
    jami_bayt = 0
    for root, dirs, files in os.walk(papka_yoli):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.exists(fp):
                jami_bayt += os.path.getsize(fp)
    return jami_bayt / (1024 * 1024)

hajm = papka_hajmi_mb(".")
print(f"Joriy papka umumiy hajmi: {hajm:.2f} MB")
```

## Tushuntirish va Mantiq:
1. `os.walk()` butun fayllar daraxtini rekursiv aylanib umumiy hajmni hisoblaydi.

## Ishlash natijasi:
```text
Chiqish: Joriy papka umumiy hajmi: ... MB
```


# 449-Topshiriq: Fayllar uchun kesh indeksi (File Catalog Indexer)

## Topshiriq sharti:
Papkadagi barcha fayllar nomi, hajmi va xeshini JSON faylga katalog qilib saqlang.

## Yechim (Python kodi):
```python
import os
import json
import hashlib

def katalog_yarat(papka):
    katalog = []
    for f in os.listdir(papka):
        fp = os.path.join(papka, f)
        if os.path.isfile(fp):
            hajm = os.path.getsize(fp)
            katalog.append({
                "fayl": f,
                "hajm_bayt": hajm,
                "hajm_kb": round(hajm / 1024, 2)
            })
    return katalog

k = katalog_yarat(".")
with open("katalog_indeksi.json", "w", encoding="utf-8") as out:
    json.dump(k[:5], out, indent=2, ensure_ascii=False)

print(f"Katalog yaratildi ({len(k)} ta fayl indekslandi).")
```

## Tushuntirish va Mantiq:
1. Ma'lumotlar arxivini indekslash va tezkor qidiruv tizimlari poydevoridir.

## Ishlash natijasi:
```text
Chiqish: Katalog yaratildi (... ta fayl indekslandi).
```


# 450-Topshiriq: To'liq Mini Fayl Menejeri (CLI File Manager)

## Topshiriq sharti:
Fayl yaratish, ko'rish, nusxalash, o'chirish va qidirish imkoniyatlariga ega interaktiv fayl boshqaruvchisi.

## Yechim (Python kodi):
```python
import os
import shutil

class MiniFaylMenejeri:
    @staticmethod
    def royxat(papka="."):
        return sorted(os.listdir(papka))

    @staticmethod
    def yaratish(fayl_nomi, matn=""):
        with open(fayl_nomi, "w", encoding="utf-8") as f:
            f.write(matn)
        print(f"[YARATILDI] {fayl_nomi}")

    @staticmethod
    def korish(fayl_nomi):
        if os.path.exists(fayl_nomi):
            with open(fayl_nomi, "r", encoding="utf-8") as f:
                print(f"--- {fayl_nomi} ---")
                print(f.read().strip())
        else:
            print("Fayl topilmadi!")

    @staticmethod
    def ochirish(fayl_nomi):
        if os.path.exists(fayl_nomi):
            os.remove(fayl_nomi)
            print(f"[O'CHIRILDI] {fayl_nomi}")

fm = MiniFaylMenejeri()
fm.yaratish("menejer_test.txt", "Fayl menejeri orqali yaratildi!")
fm.korish("menejer_test.txt")
fm.ochirish("menejer_test.txt")
```

## Tushuntirish va Mantiq:
1. Barcha fayl operatsiyalari yagona toza ob'ektga yo'naltirilgan interfeysga jamlangan.

## Ishlash natijasi:
```text
Chiqish: [YARATILDI] menejer_test.txt -> Ichidagi matn -> [O'CHIRILDI] menejer_test.txt
```

