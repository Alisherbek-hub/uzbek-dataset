# Python Dasturlash Tili — 10-Qism: Istisnolar, Xatoliklar, Logging va Crash-Proof Tizimlar
## (451-500 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam dastur xavfsizligi, barqarorligi va xatoliklarni professional boshqarishni qamrab oladi:
* `try...except...else...finally` to'liq blok strukturalari;
* Standart istisnolar: `ZeroDivisionError`, `ValueError`, `KeyError`, `IndexError`, `FileNotFoundError`;
* Maxsus istisno sinflari (Custom Exceptions), `raise` va `raise ... from` zanjirlari;
* `assert` operatori, `traceback` steki, `contextlib.suppress`;
* `logging` moduli: DEBUG dan CRITICAL gacha, faylga log yozish, vaqt tamg'asi;
* Crash-Proof arxitektura: Exponential Backoff Retry, Rollback tranzaksiyalari, ErrorTracker;

---

# 451-Topshiriq: try...except asoslari (ZeroDivisionError)

## Topshiriq sharti:
Ikki sonni bo'lishda nolga bo'lish xatoligini ushlab, dasturni qulashdan saqlang.

## Yechim (Python kodi):
```python
def xavfsiz_bolish(a, b):
    try:
        natija = a / b
        return natija
    except ZeroDivisionError:
        print("[XATOLIK] Nolga bo'lish mumkin emas!")
        return None

print("10 / 2 =", xavfsiz_bolish(10, 2))
print("10 / 0 =", xavfsiz_bolish(10, 0))
```

## Tushuntirish va Mantiq:
1. `try` bloki ichidagi kodda xatolik yuz bersa, dastur to'xtab qolmaydi, balki `except` blokiga sakraydi.

## Ishlash natijasi:
```text
Chiqish: 10 / 2 = 5.0, [XATOLIK] Nolga bo'lish mumkin emas!, 10 / 0 = None
```


# 452-Topshiriq: Bir nechta xatoliklarni alohida ushlash

## Topshiriq sharti:
Foydalanuvchi kiritgan satrni songa o'girib bo'lishda `ValueError` va `ZeroDivisionError` ni alohida-alohida qayta ishlang.

## Yechim (Python kodi):
```python
def son_kirit_va_bol(satr_a, satr_b):
    try:
        a = float(satr_a)
        b = float(satr_b)
        return a / b
    except ValueError:
        return "XATO: Faqat son kiritish kerak!"
    except ZeroDivisionError:
        return "XATO: 2-son nol bo'lishi mumkin emas!"

print(son_kirit_va_bol("10", "2"))
print(son_kirit_va_bol("salom", "2"))
print(son_kirit_va_bol("10", "0"))
```

## Tushuntirish va Mantiq:
1. Har xil turdagi xatoliklar uchun alohida `except` bloklari aniq tushuntirish berish imkonini beradi.

## Ishlash natijasi:
```text
Chiqish: 5.0, XATO: Faqat son kiritish kerak!, XATO: 2-son nol bo'lishi mumkin emas!
```


# 453-Topshiriq: try...except...else...finally to'liq bloki

## Topshiriq sharti:
Xatolik bo'lmasa `else` da, har qanday holatda esa `finally` da ishlovchi to'liq strukturani ko'rsating.

## Yechim (Python kodi):
```python
def faylni_sinab_kor(fayl_nomi):
    try:
        f = open(fayl_nomi, "r", encoding="utf-8")
        matn = f.read()
    except FileNotFoundError:
        print(f"[EXCEPT] '{fayl_nomi}' fayli topilmadi!")
    else:
        print(f"[ELSE] Fayl muvaffaqiyatli o'qildi ({len(matn)} belgi).")
        f.close()
    finally:
        print("[FINALLY] Operatsiya yakunlandi (har doim ishlaydi).")

faylni_sinab_kor("mavjud_emas.txt")
```

## Tushuntirish va Mantiq:
1. `else` faqat xatolik bo'lmaganda ishlaydi.
2. `finally` xatolik bo'lsa ham, bo'lmasa ham har doim kafolatlangan holda ishga tushadi.

## Ishlash natijasi:
```text
Chiqish: [EXCEPT] topilmadi... [FINALLY] Operatsiya yakunlandi.
```


# 454-Topshiriq: Sun'iy xatolik chaqirish (raise operatori)

## Topshiriq sharti:
Foydalanuvchi yoshi manfiy yoki 150 dan katta kiritilganda `ValueError` xatoligini ataylab chaqiring.

## Yechim (Python kodi):
```python
def yoshni_tekshir(yosh):
    if not isinstance(yosh, int):
        raise TypeError("Yosh butun son (int) bo'lishi shart!")
    if yosh < 0 or yosh > 150:
        raise ValueError(f"Yaroqsiz yosh: {yosh}. Yosh 0 va 150 oralig'ida bo'lishi kerak!")
    return f"Yosh qabul qilindi: {yosh}"

print(yoshni_tekshir(25))

try:
    yoshni_tekshir(-5)
except ValueError as e:
    print(f"Ushlangan xatolik: {e}")
```

## Tushuntirish va Mantiq:
1. `raise XatolikTuri('xabar')` shart buzilganda darhol istisno holatini vujudga keltiradi.

## Ishlash natijasi:
```text
Chiqish: Yosh qabul qilindi: 25, Ushlangan: Yaroqsiz yosh: -5...
```


# 455-Topshiriq: Shaxsiy istisno klasslari (Custom Exceptions)

## Topshiriq sharti:
Bank xizmatlari uchun `KreditLimitidanOshishXatosi` nomli shaxsiy istisno sinfini yarating.

## Yechim (Python kodi):
```python
class BankXatosi(Exception):
    """Bank tizimining umumiy asosiy xatoligi."""
    pass

class KreditLimitidanOshishXatosi(BankXatosi):
    def __init__(self, soralgan, limit):
        self.soralgan = soralgan
        self.limit = limit
        super().__init__(f"So'ralgan summa ({soralgan:,} so'm) kredit limitidan ({limit:,} so'm) oshib ketdi!")

def kredit_ber(summa, limit=50_000_000):
    if summa > limit:
        raise KreditLimitidanOshishXatosi(summa, limit)
    return "Kredit tasdiqlandi!"

try:
    kredit_ber(75_000_000)
except KreditLimitidanOshishXatosi as e:
    print(f"Bank xatoligi: {e}")
```

## Tushuntirish va Mantiq:
1. `Exception` dan meros olib dastur domeniga mos professional xatoliklar iyerarxiyasi tuziladi.

## Ishlash natijasi:
```text
Chiqish: Bank xatoligi: So'ralgan summa (75,000,000 so'm) kredit limitidan... oshib ketdi!
```


# 456-Topshiriq: Xatoliklar zanjiri (Exception Chaining: raise ... from)

## Topshiriq sharti:
Quyi darajadagi xatolikni yuqori darajadagi dastur xatoligiga bog'lab uzating.

## Yechim (Python kodi):
```python
class KonfiguratsiyaXatosi(Exception):
    pass

def sozlamani_oqish(fayl):
    try:
        with open(fayl, "r") as f:
            return f.read()
    except FileNotFoundError as original_xato:
        raise KonfiguratsiyaXatosi("Tizim sozlamalari fayli topilmadi!") from original_xato

try:
    sozlamani_oqish("server.cfg")
except KonfiguratsiyaXatosi as e:
    print(f"Xatolik: {e}")
    print(f"Dastlabki sabab: {e.__cause__}")
```

## Tushuntirish va Mantiq:
1. `raise ... from original_xato` disk xatosi kabi ichki xatolikni yo'qotmasdan, foydalanuvchiga tushunarli yangi xatolikka ulaydi.

## Ishlash natijasi:
```text
Chiqish: Xatolik: Tizim sozlamalari topilmadi!, Dastlabki sabab: [Errno 2] No such file...
```


# 457-Topshiriq: assert operatori bilan invariantlarni tekshirish

## Topshiriq sharti:
Funksiya ichida muhim shartlarni `assert` orqali tezkor tekshiring.

## Yechim (Python kodi):
```python
def chegirma_qolla(narx, foiz):
    assert narx >= 0, "Narx manfiy bo'lishi mumkin emas!"
    assert 0 <= foiz <= 100, "Chegirma foizi 0 va 100 oralig'ida bo'lishi kerak!"
    return narx * (1 - foiz / 100)

print("Yangi narx:", chegirma_qolla(100000, 20))

try:
    chegirma_qolla(100000, 150)
except AssertionError as e:
    print(f"Assert tekshiruvi: {e}")
```

## Tushuntirish va Mantiq:
1. `assert shart, xabar` agar shart `False` bo'lsa darhol `AssertionError` chaqiradi (debugging va testlar uchun).

## Ishlash natijasi:
```text
Chiqish: Yangi narx: 80000.0, Assert tekshiruvi: Chegirma foizi 0 va 100 oralig'ida...
```


# 458-Topshiriq: traceback moduli bilan xatolik stekini formatlash

## Topshiriq sharti:
Xatolik qaysi fayl, qaysi funksiya va nechanchi qatorda sodir bo'lganini `traceback.format_exc()` orqali matn sifatida oling.

## Yechim (Python kodi):
```python
import traceback

def funksiya_a():
    funksiya_b()

def funksiya_b():
    return 10 / 0

try:
    funksiya_a()
except Exception:
    xato_matni = traceback.format_exc()
    print("--- USHLANGAN STACK TRACE ---")
    print(xato_matni.strip())
```

## Tushuntirish va Mantiq:
1. `traceback` murakkab ko'p qatlamli dasturlarda xatoning asl manbasini aniq topishga imkon beradi.

## Ishlash natijasi:
```text
Chiqish: To'liq qatorlar zanjiri va ZeroDivisionError ko'rsatiladi.
```


# 459-Topshiriq: logging moduli: Barcha darajalar (DEBUG dan CRITICAL gacha)

## Topshiriq sharti:
Standart `logging` modulining 5 ta muhimlik darajasidagi xabarlarini konsolga chiqaring.

## Yechim (Python kodi):
```python
import logging

# Log formatini sozlaymiz
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

logging.debug("Bu nosozliklarni tuzatish (Debug) xabari.")
logging.info("Tizim normal holatda ishlamoqda (Info).")
logging.warning("Diqqat: Xotira hajmi kam qolmoqda (Warning)!")
logging.error("Faylni yuklab bo'lmadi (Error)!")
logging.critical("Favqulodda holat: Ma'lumotlar bazasi quladi (Critical)!")
```

## Tushuntirish va Mantiq:
1. `print()` o'rniga `logging` ishlatish ishlab chiqarish (Production) tizimlarining standart talabidir.

## Ishlash natijasi:
```text
Chiqish: DEBUG, INFO, WARNING, ERROR, CRITICAL darajali rang-barang xabarlar.
```


# 460-Topshiriq: Faylga log yozish va vaqt tamg'asi (Timestamp)

## Topshiriq sharti:
Barcha log xabarlarini vaqt, modul nomi va daraja bilan `dastur.log` fayliga saqlang.

## Yechim (Python kodi):
```python
import logging

log_format = '%(asctime)s [%(levelname)s] (%(name)s) %(message)s'
logging.basicConfig(
    filename='dastur.log',
    filemode='a',
    level=logging.INFO,
    format=log_format,
    encoding='utf-8'
)

logger = logging.getLogger("DatasetPipeline")

logger.info("Pipeline muvaffaqiyatli boshlandi.")
logger.info("50 ta kitob yuklandi va tozalashdan o'tdi.")
logger.warning("1 ta kitob skanerlangan rasm bo'lgani sababli o'tkazib yuborildi.")

print("'dastur.log' fayliga loglar muvaffaqiyatli yozildi.")
```

## Tushuntirish va Mantiq:
1. `asctime` har bir hodisaning aniq soniyasigacha qayd etadi.

## Ishlash natijasi:
```text
Chiqish: 'dastur.log' fayliga loglar muvaffaqiyatli yozildi.
```


# 461-Topshiriq: Loglarda xatolik stack trace'ini yozish (exc_info=True)

## Topshiriq sharti:
Xatolik sodir bo'lganda `logger.error` ga `exc_info=True` berib butun tracebackni log faylga tushiring.

## Yechim (Python kodi):
```python
import logging

logger = logging.getLogger("Hisobchi")

try:
    son = int("bu_son_emas")
except ValueError:
    # exc_info=True butun xatolik tarixini logga yozadi
    logger.error("Sonni o'girishda kutilmagan xatolik yuz berdi!", exc_info=True)
```

## Tushuntirish va Mantiq:
1. Ishlab chiquvchi log faylni ochganda aynan qaysi kodda xato bo'lganini darhol ko'radi.

## Ishlash natijasi:
```text
Chiqish: ERROR xabari va uning orqasidan ValueError steki yoziladi.
```


# 462-Topshiriq: contextlib.suppress bilan xatoliklarni xavfsiz e'tiborsiz qoldirish

## Topshiriq sharti:
Fayl bo'lmasa o'chirishga uringanda `FileNotFoundError` xatosini bitta qatorda e'tiborsiz qoldiring.

## Yechim (Python kodi):
```python
import os
from contextlib import suppress

# Oddiy try-except pass o'rniga toza yechim:
with suppress(FileNotFoundError):
    os.remove("mavjud_bolmagan_fayl.txt")

print("Fayl yo'q bo'lsa ham dastur to'xtamasdan muvaffaqiyatli o'tib ketdi!")
```

## Tushuntirish va Mantiq:
1. `suppress(XatolikTuri)` ko'rsatilgan xatoliklarni xavfsiz chetlab o'tuvchi rasmiy Python kontekst menejeridir.

## Ishlash natijasi:
```text
Chiqish: Dastur to'xtamasdan muvaffaqiyatli o'tib ketdi!
```


# 463-Topshiriq: Eskirgan funksiyalar uchun ogohlantirish (warnings moduli)

## Topshiriq sharti:
`warnings.warn` orqali foydalanuvchiga funksiya tez orada eskirishini xabar qiling.

## Yechim (Python kodi):
```python
import warnings

def eski_hisoblash(a, b):
    warnings.warn(
        "'eski_hisoblash' funksiyasi eskirgan, o'rniga 'yangi_hisob' dan foydalaning!",
        DeprecationWarning,
        stacklevel=2
    )
    return a + b

natija = eski_hisoblash(5, 7)
print("Natija:", natija)
```

## Tushuntirish va Mantiq:
1. Warning xatolik emas, u dasturni to'xtatmaydi, lekin kutubxona yangilanganda nimalar o'zgarishini bildiradi.

## Ishlash natijasi:
```text
Chiqish: DeprecationWarning ogohlantirishi va Natija: 12
```


# 464-Topshiriq: Eksponentsial kechikish bilan qayta urinish (Retry with Exponential Backoff)

## Topshiriq sharti:
Tarmoq yoki API so'rovi uzilib qolsa 1s, 2s, 4s kutib 3 marta qayta urinuvchi xavfsiz tizim.

## Yechim (Python kodi):
```python
import time

def soxta_api_sorov(urinish_raqami):
    if urinish_raqami < 3:
        raise ConnectionError("Server vaqtincha javob bermayapti...")
    return "Muvaffaqiyatli ma'lumot olindi! [200 OK]"

def qayta_urinuvchi_ijro(maks_urinish=3):
    kutish = 1.0  # soniya
    for u in range(1, maks_urinish + 1):
        try:
            print(f"[{u}-urinish] So'rov yuborilmoqda...")
            return soxta_api_sorov(u)
        except ConnectionError as e:
            print(f"  -> Xatolik: {e}")
            if u == maks_urinish:
                raise
            print(f"  -> {kutish:.1f} soniya kutilmoqda...")
            time.sleep(kutish)
            kutish *= 2  # Eksponentsial 2 barobar oshirish

print("Natija:", qayta_urinuvchi_ijro(3))
```

## Tushuntirish va Mantiq:
1. Serverga birdaniga yuklama bermaslik uchun kutish vaqti har qadamda karrali oshirib boriladi.

## Ishlash natijasi:
```text
Chiqish: [1-urinish]... [2-urinish]... [3-urinish] Muvaffaqiyatli ma'lumot olindi!
```


# 465-Topshiriq: JSON parse xatoliklarini aniq ko'rsatish (JSONDecodeError)

## Topshiriq sharti:
Buzilgan JSON matni kiritilganda uning aynan qaysi qatori va ustunida sintaktik xato borligini aniqlang.

## Yechim (Python kodi):
```python
import json

buzilgan_json = '''{
    "ism": "Alisher",
    "yosh": 17,
}'''  # Oxirgi vergul JSON da xatolik!

try:
    json.loads(buzilgan_json)
except json.JSONDecodeError as e:
    print(f"[JSON XATOLIK]: {e.msg}")
    print(f"Qator: {e.lineno}, Ustun: {e.colno}, Belgilar o'rni: {e.pos}")
```

## Tushuntirish va Mantiq:
1. `JSONDecodeError` xatoning aynan qayerdaligini ko'rsatib diskdagi faylni tezda tuzatishga yordam beradi.

## Ishlash natijasi:
```text
Chiqish: [JSON XATOLIK]: Expecting property name..., Qator: 4, Ustun: 1
```


# 466-Topshiriq: Parol kuchliligini tekshiruvchi maxsus xatoliklar

## Topshiriq sharti:
Parolda xato bo'lsa `KichikUzunlikXatosi`, `KattaHarfYoqXatosi` kabi maxsus istisnolarni chaqiring.

## Yechim (Python kodi):
```python
class ParolXatosi(Exception): pass
class JudaQisqaParolXatosi(ParolXatosi): pass
class RaqamYoqParolXatosi(ParolXatosi): pass

def tekshir_parol(parol):
    if len(parol) < 8:
        raise JudaQisqaParolXatosi("Parol kamida 8 ta belgidan iborat bo'lishi kerak!")
    if not any(ch.isdigit() for ch in parol):
        raise RaqamYoqParolXatosi("Parolda kamida 1 ta raqam qatnashishi shart!")
    return "Parol qabul qilindi!"

try:
    tekshir_parol("salom")
except JudaQisqaParolXatosi as e:
    print(f"Xatolik: {e}")
```

## Tushuntirish va Mantiq:
1. Foydalanuvchiga paroli nima sababdan rad etilganini aniq yetkazish mexanizmi.

## Ishlash natijasi:
```text
Chiqish: Xatolik: Parol kamida 8 ta belgidan iborat bo'lishi kerak!
```


# 467-Topshiriq: Xatoliklarni yutib yubormaslik qoidasi (Anti-pattern tahlili)

## Topshiriq sharti:
`except: pass` nima uchun xavfli ekanligini va qanday qilib to'g'ri qayd etish lozimligini ko'rsating.

## Yechim (Python kodi):
```python
# XAVFLI USUL (Bunday qilmang!):
# try:
#     muhim_amal()
# except:
#     pass  # Dasturchi dastur nega ishlamayotganini hech qachon bilolmaydi!

# TO'G'RI VA XAVFSIZ USUL:
import logging

def xavfsiz_ijro(amal):
    try:
        return amal()
    except Exception as e:
        # Kamida xatolik turi va sababini logga yozib qo'yamiz
        logging.warning(f"Kutilmagan holat yuz berdi: {type(e).__name__} - {e}")
        return None

xavfsiz_ijro(lambda: 1 / 0)
```

## Tushuntirish va Mantiq:
1. Har qanday xatolik qayd etilishi (loglanishi) shart, aks holda xatoliklar yashirinib tizimni ishdan chiqaradi.

## Ishlash natijasi:
```text
Chiqish: WARNING: Kutilmagan holat: ZeroDivisionError - division by zero
```


# 468-Topshiriq: Xatoliklarni ushlab chiroyli JSON qaytaruvchi API dekoratori

## Topshiriq sharti:
Funksiya qulaganda uni tutib `{success: False, error: '...'}` JSON formatida qaytaruvchi dekorator.

## Yechim (Python kodi):
```python
import functools

def api_xavfsizlik_qobigi(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            natija = func(*args, **kwargs)
            return {"success": True, "data": natija, "error": None}
        except Exception as e:
            return {"success": False, "data": None, "error": f"{type(e).__name__}: {str(e)}"}
    return wrapper

@api_xavfsizlik_qobigi
def foydalanuvchi_ol(id):
    if id <= 0:
        raise ValueError("ID musbat natural son bo'lishi kerak!")
    return {"id": id, "ism": "Alisher"}

print(foydalanuvchi_ol(101))
print(foydalanuvchi_ol(-5))
```

## Tushuntirish va Mantiq:
1. Backend API (FastAPI, Flask) larda xatolik yuz berganda server 500 bermasdan chiroyli formatda javob qaytaradi.

## Ishlash natijasi:
```text
Chiqish: {success: True, data: ...}, {success: False, error: 'ValueError: ID musbat...'}
```


# 469-Topshiriq: pdb (Python Debugger) va breakpoint()

## Topshiriq sharti:
Kod bajarilishini to'xtatib o'zgaruvchilarni real vaqtda tekshiruvchi `breakpoint()` mexanizmi.

## Yechim (Python kodi):
```python
def murakkab_hisob(a, b):
    x = a * 2
    y = b + 10
    # breakpoint()  # Ushbu qatorda dastur to'xtab terminalda pdb konsoli ochiladi
    natija = x + y
    return natija

print("Natija:", murakkab_hisob(5, 3))
```

## Tushuntirish va Mantiq:
1. `breakpoint()` Python 3.7+ da kiritilgan bo'lib, xatoliklarni tahlil qilish uchun interaktiv debug rejimini yoqadi.

## Ishlash natijasi:
```text
Chiqish: Natija: 23
```


# 470-Topshiriq: Global tutib olinmagan xatoliklar qopqoni (sys.excepthook)

## Topshiriq sharti:
Dasturning istalgan joyida kutilmagan xatolik yuz bersa tizimni to'liq logga tushiruvchi global hodisa.

## Yechim (Python kodi):
```python
import sys

def global_xatolik_qopqoni(exc_type, exc_value, exc_traceback):
    print(f"\n🚨 [GLOBAL XATOLIK QOPQONI] Tizim qulashining oldi olindi!")
    print(f"Turi  : {exc_type.__name__}")
    print(f"Xabar : {exc_value}")

# Standart ushlagichni o'zgartiramiz
eski_hook = sys.excepthook
sys.excepthook = global_xatolik_qopqoni

# Qayta tiklaymiz
sys.excepthook = eski_hook
print("Global excepthook muvaffaqiyatli ro'yxatga olindi.")
```

## Tushuntirish va Mantiq:
1. `sys.excepthook` orqali dastur kutilmaganda yopilib ketishining oldi olinadi va yakuniy xabar yuboriladi.

## Ishlash natijasi:
```text
Chiqish: Global excepthook muvaffaqiyatli ro'yxatga olindi.
```


# 471-Topshiriq: Tranzaksiyani bekor qilish (Rollback simulation)

## Topshiriq sharti:
Ma'lumotlar bazasida amallardan biri xato bo'lsa barcha o'zgarishlarni bekor qiluvchi Rollback mexanizmi.

## Yechim (Python kodi):
```python
class TranzaksiyaMenejeri:
    def __init__(self):
        self.baza = ["Ali", "Vali"]
        self.zaxira = []

    def bajar(self, amallar):
        self.zaxira = list(self.baza)
        try:
            for ism in amallar:
                if ism == "XATO":
                    raise ValueError("Xatolik yuz berdi! Amal to'xtatildi.")
                self.baza.append(ism)
            print("[TRANZAKSIYA] Muvaffaqiyatli tasdiqlandi (Commit)!")
        except Exception as e:
            print(f"[ROLLBACK] Xato: {e}. Baza asl holatiga qaytarildi!")
            self.baza = list(self.zaxira)

tm = TranzaksiyaMenejeri()
tm.bajar(["G'ani", "XATO", "Sardor"])
print("Hozirgi baza:", tm.baza)
```

## Tushuntirish va Mantiq:
1. ACID tamoyillaridagi Atomicity (yo hammasi bajariladi, yo hech biri bajarilmaydi) qoidasi.

## Ishlash natijasi:
```text
Chiqish: [ROLLBACK] Xato... Baza asl holatiga qaytarildi! Baza: ['Ali', 'Vali']
```


# 472-Topshiriq: Loglarda maxfiy ma'lumotlarni niqoblash (Masking Filter)

## Topshiriq sharti:
Loglarga kredit karta yoki parol yozilayotganda ularni yulduzcha `****` bilan niqoblovchi Filter tuzing.

## Yechim (Python kodi):
```python
import logging
import re

class MaxfiylikFilteri(logging.Filter):
    def filter(self, record):
        # 16 xonali karta raqamlarini topib niqoblaymiz
        xabar = record.getMessage()
        toza = re.sub(r'\b\d{4}\s?\d{4}\s?\d{4}\s?(\d{4})\b', '**** **** **** \\1', xabar)
        record.msg = toza
        return True

logger = logging.getLogger("TolovLog")
logger.addFilter(MaxfiylikFilteri())

# Xabarni chiqaramiz
print("Niqoblangan log namunasi:")
print(re.sub(r'\b\d{12}(\d{4})\b', '**** **** **** \\1', "Mijoz 8600123456789988 kartasidan to'ladi."))
```

## Tushuntirish va Mantiq:
1. Xavfsizlik talablariga ko'ra log fayllariga mijozlarning maxfiy parollari va to'liq karta raqamlari yozilishi taqiqlanadi.

## Ishlash natijasi:
```text
Chiqish: Mijoz **** **** **** 9988 kartasidan to'ladi.
```


# 473-Topshiriq: Fayl ochishdagi xatoliklarni xavfsiz boshqarish

## Topshiriq sharti:
`FileNotFoundError`, `PermissionError` va `IsADirectoryError` xatoliklarini alohida ushlang.

## Yechim (Python kodi):
```python
def xavfsiz_fayl_oqish(yol):
    try:
        with open(yol, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "[XATO] Fayl mavjud emas!"
    except PermissionError:
        return "[XATO] Faylni o'qishga huquq yetarli emas!"
    except IsADirectoryError:
        return "[XATO] Ko'rsatilgan yo'l fayl emas, papkadir!"

print(xavfsiz_fayl_oqish("yoq_fayl.txt"))
print(xavfsiz_fayl_oqish("."))  # Papka
```

## Tushuntirish va Mantiq:
1. Har bir operatsion tizim fayl xatoliklarini aniq ushlab xavfsiz xabar beradi.

## Ishlash natijasi:
```text
Chiqish: [XATO] Fayl mavjud emas!, [XATO] Ko'rsatilgan yo'l papkadir!
```


# 474-Topshiriq: Cheksiz tsikllarni vaqt bo'yicha to'xtatuvchi Timeout Guard

## Topshiriq sharti:
Tsikl belgilangan soniyadan ortiq davom etsa `TimeoutError` chaqiruvchi xavfsizlik nazorati.

## Yechim (Python kodi):
```python
import time

def uzoq_tsikl_himoyasi(maks_soniya=0.5):
    boshlandi = time.perf_counter()
    i = 0
    while True:
        i += 1
        # Vaqtni tekshiramiz
        if time.perf_counter() - boshlandi > maks_soniya:
            raise TimeoutError(f"Cheksiz tsikl aniqlandi! ({maks_soniya} soniya limitidan oshdi). Iteratsiyalar: {i:,}")

try:
    uzoq_tsikl_himoyasi(0.05)
except TimeoutError as e:
    print(f"Xavfsizlik tizimi ishladi: {e}")
```

## Tushuntirish va Mantiq:
1. Dastur server protsessorini (CPU 100%) osilib qolishidan himoya qiladi.

## Ishlash natijasi:
```text
Chiqish: Xavfsizlik tizimi ishladi: Cheksiz tsikl aniqlandi!...
```


# 475-Topshiriq: Formadagi barcha xatoliklarni bitta qopga yig'ish (Errors Bag)

## Topshiriq sharti:
Foydalanuvchi ma'lumotlaridagi barcha kamchiliklarni bitta ro'yxatga jamlovchi validator klassi.

## Yechim (Python kodi):
```python
class FormValidator:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def validate(self):
        if not self.data.get("username"):
            self.errors.append("Foydalanuvchi nomi kiritilmagan!")
        if "@" not in self.data.get("email", ""):
            self.errors.append("Email noto'g'ri formatda!")
        if len(self.data.get("password", "")) < 6:
            self.errors.append("Parol kamida 6 belgidan iborat bo'lishi kerak!")
        return len(self.errors) == 0

forma = {"username": "", "email": "xato_pochta", "password": "123"}
v = FormValidator(forma)

if not v.validate():
    print(f"Formada {len(v.errors)} ta xatolik topildi:")
    for x in v.errors:
        print(f" - {x}")
```

## Tushuntirish va Mantiq:
1. Birinchi xatoda to'xtamasdan barcha xatoliklarni birdaniga ko'rsatish foydalanuvchi tajribasini (UX) oshiradi.

## Ishlash natijasi:
```text
Chiqish: 3 ta xatolik ro'yxati.
```


# 476-Topshiriq: Xatoliklar audit jurnalini CSV ga yozish (ErrorTracker)

## Topshiriq sharti:
Yuz bergan barcha istisnolarni vaqt, tur va xabar bo'yicha CSV jurnaliga saqlang.

## Yechim (Python kodi):
```python
import csv
from datetime import datetime

class ErrorTracker:
    def __init__(self, csv_file="xatoliklar_auditi.csv"):
        self.csv_file = csv_file

    def log_error(self, exception_obj):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([now, type(exception_obj).__name__, str(exception_obj)])

tracker = ErrorTracker()
try:
    int("nol")
except Exception as e:
    tracker.log_error(e)

print("Xatolik CSV audit fayliga muvaffaqiyatli kiritildi.")
```

## Tushuntirish va Mantiq:
1. Tizim xatoliklarini tahlil qilish uchun avtomatlashtirilgan audit jurnali.

## Ishlash natijasi:
```text
Chiqish: Xatolik CSV audit fayliga kiritildi.
```


# 477-Topshiriq: Xotira yetishmasligi (MemoryError) simulyatsiyasi

## Topshiriq sharti:
Katta massivlar yaratishda xotira chegarasini xavfsiz tekshirish.

## Yechim (Python kodi):
```python
def xavfsiz_massiv_yarat(olcham):
    try:
        # Juda ulkan massiv yaratishga urinish
        if olcham > 100_000_000:
            raise MemoryError("Xotira sarfi xavfsizlik chegarasidan (100M) oshib ketdi!")
        return [0] * olcham
    except MemoryError as e:
        print(f"[XOTIRA XATOLIGI]: {e}")
        return []

massiv = xavfsiz_massiv_yarat(500_000_000)
print(f"Yaratilgan massiv uzunligi: {len(massiv)}")
```

## Tushuntirish va Mantiq:
1. Dastur operativ xotirani to'ldirib OS qulashining (OOM Killer) oldini oladi.

## Ishlash natijasi:
```text
Chiqish: [XOTIRA XATOLIGI]: Xotira sarfi chegaradan oshdi! Uzunlik: 0
```


# 478-Topshiriq: Avtomatik zaxira xizmati (Failover Fallback)

## Topshiriq sharti:
Asosiy server ishlamay qolsa avtomatik tarzda zaxira (backup) serveriga o'tuvchi tizim.

## Yechim (Python kodi):
```python
def asosiy_server():
    raise ConnectionRefusedError("Asosiy server [192.168.1.10] ishlamayapti!")

def zaxira_server():
    return "Zaxira server [192.168.1.20] ma'lumotni muvaffaqiyatli taqdim etdi! [OK]"

def xavfsiz_sorov():
    try:
        return asosiy_server()
    except ConnectionRefusedError:
        print("[OGOHLANTIRISH] Asosiy server javob bermadi. Zaxira serverga o'tilmoqda...")
        return zaxira_server()

print(xavfsiz_sorov())
```

## Tushuntirish va Mantiq:
1. Yuqori ishonchlilikka (High Availability) ega tizimlar doimo zaxira yo'liga ega bo'ladi.

## Ishlash natijasi:
```text
Chiqish: Asosiy server javob bermadi... Zaxira server ma'lumotni taqdim etdi!
```


# 479-Topshiriq: Matnni sonlarga o'giruvchi aqlli parser

## Topshiriq sharti:
Probel, vergul va boshqa belgilarni tozalab xavfsiz `int` yoki `float` ga o'tkazuvchi funksiya.

## Yechim (Python kodi):
```python
def aqlli_son_parser(satr):
    try:
        # Bo'shliqlar va valyuta belgilarini tozalaymiz
        toza = satr.replace(" ", "").replace("so'm", "").replace("$", "").replace(",", ".")
        if "." in toza:
            return float(toza)
        return int(toza)
    except (ValueError, AttributeError) as e:
        print(f"[OGOHLANTIRISH] '{satr}' ni songa o'girib bo'lmadi ({e}). 0 qaytarildi.")
        return 0

print("12 500 so'm ->", aqlli_son_parser("12 500 so'm"))
print("$ 99.95     ->", aqlli_son_parser("$ 99.95"))
print("noma'lum    ->", aqlli_son_parser("noma'lum"))
```

## Tushuntirish va Mantiq:
1. Real ma'lumotlar bilan ishlaganda xom satrlarni xavfsiz konvertatsiya qilish.

## Ishlash natijasi:
```text
Chiqish: 12500, 99.95, [OGOHLANTIRISH]... 0
```


# 480-Topshiriq: HTTP Status xatoliklari iyerarxiyasi

## Topshiriq sharti:
REST API status kodlari (400 Bad Request, 404 Not Found, 500 Server Error) uchun klasslar.

## Yechim (Python kodi):
```python
class HTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")

class NotFoundException(HTTPException):
    def __init__(self, resource):
        super().__init__(404, f"'{resource}' topilmadi!")

class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(401, "Tizimga kirish huquqi mavjud emas (Avtorizatsiyadan o'ting)!")

def mahsulotni_qidir(id):
    if id != 1:
        raise NotFoundException(f"Mahsulot #{id}")
    return "Mahsulot: Noutbuk"

try:
    mahsulotni_qidir(99)
except HTTPException as e:
    print(f"API javobi: Status={e.status_code}, Xabar={e.detail}")
```

## Tushuntirish va Mantiq:
1. Zamonaviy web-freymvorklar (FastAPI, Django) aynan shu xatoliklar iyerarxiyasida ishlaydi.

## Ishlash natijasi:
```text
Chiqish: API javobi: Status=404, Xabar='Mahsulot #99' topilmadi!
```


# 481-Topshiriq: Avtomatik resurs qulfi (Lock Guard)

## Topshiriq sharti:
Kritik amal bajarilayotganda resursni qulflab, yakunda kafolatlangan ochuvchi kontekst menejeri.

## Yechim (Python kodi):
```python
class ResursQulfi:
    def __init__(self, resurs_nomi):
        self.resurs_nomi = resurs_nomi
        self.qulflangan = False

    def __enter__(self):
        self.qulflangan = True
        print(f"[QULF] '{self.resurs_nomi}' qulflandi (faqat bitta oqim ishlaydi).")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.qulflangan = False
        print(f"[OCHILDI] '{self.resurs_nomi}' qulfi ochildi.")

with ResursQulfi("Kitoblar bazasi"):
    print(" -> Muhim yozish amali bajarilmoqda...")
```

## Tushuntirish va Mantiq:
1. Ko'p oqimli (multithreading) tizimlarda Race Condition xatolarining oldini oladi.

## Ishlash natijasi:
```text
Chiqish: [QULF]... Yozish amali... [OCHILDI]...
```


# 482-Topshiriq: Fayl mavjud bo'lmasa avtomatik yaratuvchi Decorator

## Topshiriq sharti:
Fayl bilan ishlovchi funksiya oldidan fayl yo'q bo'lsa uni avtomatik ochib beruvchi dekorator.

## Yechim (Python kodi):
```python
import os
import functools

def faylni_kafolatla(fayl_yoli):
    def dekorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not os.path.exists(fayl_yoli):
                with open(fayl_yoli, "w", encoding="utf-8") as f:
                    f.write("")
                print(f"[KAFOLATLANDI] '{fayl_yoli}' yangidan yaratildi.")
            return func(*args, **kwargs)
        return wrapper
    return dekorator

@faylni_kafolatla("yangi_baza.txt")
def qoshimcha_yoz(matn):
    with open("yangi_baza.txt", "a", encoding="utf-8") as f:
        f.write(matn + "\n")
    print(f"Yozildi: {matn}")

qoshimcha_yoz("1-qator")
```

## Tushuntirish va Mantiq:
1. Dastur birinchi marta ishga tushganda `FileNotFoundError` berishining oldini oladi.

## Ishlash natijasi:
```text
Chiqish: [KAFOLATLANDI]... Yozildi: 1-qator
```


# 483-Topshiriq: Xatoliklar statistikasini yig'uvchi hisoblagich

## Topshiriq sharti:
Dastur ishlashi davomida qaysi xatolik necha marta uchraganini hisoblab boruvchi klass.

## Yechim (Python kodi):
```python
class XatolikStatistikasi:
    def __init__(self):
        self.statistika = {}

    def qayd_et(self, xato):
        nom = type(xato).__name__
        self.statistika[nom] = self.statistika.get(nom, 0) + 1

    def hisobot(self):
        print("\n--- XATOLIKLAR STATISTIKASI ---")
        for nom, soni in self.statistika.items():
            print(f" * {nom:22s}: {soni} marta")

stat = XatolikStatistikasi()

for amal in [lambda: 1/0, lambda: int("x"), lambda: 1/0, lambda: [][0]]:
    try:
        amal()
    except Exception as e:
        stat.qayd_et(e)

stat.hisobot()
```

## Tushuntirish va Mantiq:
1. Katta tizimlarning barqarorligini monitoring qilish (Observability) vositasi.

## Ishlash natijasi:
```text
Chiqish: ZeroDivisionError: 2, ValueError: 1, IndexError: 1
```


# 484-Topshiriq: Konsolda xatoliklarni rangli chiqarish (ANSI Colors)

## Topshiriq sharti:
Qizil, sariq va yashil rangli konsol xabarlarini chiqaruvchi utility funksiya.

## Yechim (Python kodi):
```python
def rangli_chop(matn, rang="oq"):
    ranglar = {
        "qizil": "\033[91m",
        "yashil": "\033[92m",
        "sariq": "\033[93m",
        "kok": "\033[94m",
        "reset": "\033[0m"
    }
    kod = ranglar.get(rang.lower(), ranglar["reset"])
    print(f"{kod}{matn}{ranglar['reset']}")

rangli_chop("[XATOLIK] Fayl topilmadi!", "qizil")
rangli_chop("[OGOHLANTIRISH] Xotira to'lmoqda!", "sariq")
rangli_chop("[MUVAFFAQIYAT] Barcha 500 ta kitob saqlandi!", "yashil")
```

## Tushuntirish va Mantiq:
1. Terminal xabarlarini o'qish qulayligini keskin oshiradi.

## Ishlash natijasi:
```text
Chiqish: Qizil xatolik, Sariq ogohlantirish, Yashil muvaffaqiyat xabarlari.
```


# 485-Topshiriq: Xatoliklar yuz berganda avtomatik qayta ishga tushuvchi Daemon

## Topshiriq sharti:
Xizmat qulaganda uni avtomatik tarzda 3 soniyadan keyin qayta tiklovchi mustahkam loop.

## Yechim (Python kodi):
```python
def nozik_xizmat(qadam):
    if qadam == 2:
        raise RuntimeError("Kutilmagan xotira uzilishi!")
    print(f"Xizmat {qadam}-qadamni muvaffaqiyatli bajardi.")

for qadam in range(1, 4):
    try:
        nozik_xizmat(qadam)
    except Exception as e:
        print(f"[RESTART] Xatolik yuz berdi: {e}. Xizmat zudlik bilan qayta ishga tushirilmoqda...")
```

## Tushuntirish va Mantiq:
1. Uzluksiz ishlovchi fon xizmatlarining (Daemon) barqarorligi ta'minlanadi.

## Ishlash natijasi:
```text
Chiqish: 1-qadam muvaffaqiyatli... [RESTART] Xatolik yuz berdi... 3-qadam muvaffaqiyatli.
```


# 486-Topshiriq: Konfiguratsiyadagi yetishmayotgan kalitlarni to'ldiruvchi Safe Dict

## Topshiriq sharti:
Agar kalit mavjud bo'lmasa `KeyError` o'rniga ogohlantirish berib standart qiymat qaytaruvchi klass.

## Yechim (Python kodi):
```python
class XavfsizSozlamalar(dict):
    def __init__(self, *args, standart="Ko'rsatilmagan", **kwargs):
        super().__init__(*args, **kwargs)
        self.standart = standart

    def __getitem__(self, kalit):
        if kalit not in self:
            print(f"[OGOHLANTIRISH] '{kalit}' parametri yo'q, standart qiymat ishlatilmoqda.")
            return self.standart
        return super().__getitem__(kalit)

cfg = XavfsizSozlamalar({"theme": "dark"}, standart="BirlamchiQiymat")
print("Theme:", cfg["theme"])
print("Port :", cfg["port"])  # KeyError bermaydi!
```

## Tushuntirish va Mantiq:
1. `__getitem__` ni qayta aniqlash orqali to'satdan qulashlarning oldi olinadi.

## Ishlash natijasi:
```text
Chiqish: Theme: dark, [OGOHLANTIRISH] 'port' yo'q... Port: BirlamchiQiymat
```


# 487-Topshiriq: API chaqiruvlari uchun Vaqt Chegarasi (Timeout Context)

## Topshiriq sharti:
Funksiya chaqiruvi belgilangan vaqt ichida yakunlanishini nazorat qiluvchi sodda struktura.

## Yechim (Python kodi):
```python
import time

def uzoq_amalli_sorov(kutiladigan_vaqt):
    boshlandi = time.time()
    time.sleep(kutiladigan_vaqt)
    if time.time() - boshlandi > 0.1:
        raise TimeoutError("Operatsiya belgilangan 0.1 soniyadan ko'p vaqt oldi!")
    return "Muvaffaqiyatli bajarildi!"

try:
    print(uzoq_amalli_sorov(0.02))
    print(uzoq_amalli_sorov(0.15))
except TimeoutError as e:
    print(f"Timeout: {e}")
```

## Tushuntirish va Mantiq:
1. Tezkor javob talab qiluvchi veb-xizmatlarda qotib qolishlarning oldi olinadi.

## Ishlash natijasi:
```text
Chiqish: Muvaffaqiyatli bajarildi!, Timeout: Operatsiya belgilangan... ko'p vaqt oldi!
```


# 488-Topshiriq: Bir nechta vazifalarni parallel xavfsiz bajarish (Batch Error Isolation)

## Topshiriq sharti:
Biror elementda xato bo'lsa, qolgan elementlarning ishi to'xtab qolmasligini ta'minlovchi izolyatsiya.

## Yechim (Python kodi):
```python
topshiriqlar = [10, "yaroqsiz", 20, 0, 40]

muvaffaqiyatli = []
xatoliklar = []

for t in topshiriqlar:
    try:
        natija = 100 / int(t)
        muvaffaqiyatli.append((t, natija))
    except Exception as e:
        xatoliklar.append((t, type(e).__name__))

print("Muvaffaqiyatli bajarilganlar:", muvaffaqiyatli)
print("Xatolik tufayli to'xtaganlar  :", xatoliklar)
```

## Tushuntirish va Mantiq:
1. 500 ta kitobni qayta ishlashda aynan shu mantiq ishlatiladi: bitta kitob xato bo'lsa, qolgan 499 tasi davom etadi.

## Ishlash natijasi:
```text
Chiqish: Muvaffaqiyatli: [(10, 10.0), (20, 5.0), (40, 2.5)], Xatoliklar: [('yaroqsiz', 'ValueError'), (0, 'ZeroDivisionError')]
```


# 489-Topshiriq: Xatoliklar yuz berganda xabar yuboruvchi Alert Dispatcher

## Topshiriq sharti:
Kritik xatolik bo'lganda ogohlantirish xizmatiga (Telegram/Email simulyatsiyasi) xabar yo'llovchi tizim.

## Yechim (Python kodi):
```python
def telegram_xabar_yubor(xabar):
    print(f"📲 [TELEGRAM BOT ALERTI]: {xabar}")

def kritik_amal(foydalanuvchi_id):
    if foydalanuvchi_id < 0:
        xato = ValueError(f"Noto'g'ri ID: {foydalanuvchi_id}")
        telegram_xabar_yubor(f"XATOLIK YUZ BERDI: {xato}")
        raise xato
    return "Foydalanuvchi ma'lumotlari olindi."

try:
    kritik_amal(-100)
except ValueError:
    pass
```

## Tushuntirish va Mantiq:
1. Serverdagi xatoliklar haqida dasturchilar jamoasiga real vaqtda avtomatik xabar yetkaziladi.

## Ishlash natijasi:
```text
Chiqish: 📲 [TELEGRAM BOT ALERTI]: XATOLIK YUZ BERDI: Noto'g'ri ID: -100
```


# 490-Topshiriq: Dasturning xotira oqishini (Memory Leak) monitoring qilish

## Topshiriq sharti:
`tracemalloc` orqali xotira qayerda sarflanayotganini tekshiruvchi tahlilchi.

## Yechim (Python kodi):
```python
import tracemalloc

tracemalloc.start()

# Xotira oluvchi amal
katta_massiv = [x ** 2 for x in range(100_000)]

joriy, eng_yuqori = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"Joriy ishlatilgan xotira: {joriy / (1024 * 1024):.2f} MB")
print(f"Eng yuqori cho'qqi (Peak): {eng_yuqori / (1024 * 1024):.2f} MB")
```

## Tushuntirish va Mantiq:
1. `tracemalloc` Python dasturining xotira profili va RAM tejamkorligini o'lchaydi.

## Ishlash natijasi:
```text
Chiqish: Joriy xotira: ~3.8 MB, Cho'qqi: ~3.9 MB
```


# 491-Topshiriq: Xatoliklarni audit qiluvchi File Error Handler

## Topshiriq sharti:
Xatolik ro'y berganda fayl nomini, funksiya nomini va vaqtini maxsus formatda faylga saqlovchi handler.

## Yechim (Python kodi):
```python
from datetime import datetime

def yoz_xato_jurnaliga(funksiya_nomi, xato):
    with open("xatolar_audit.log", "a", encoding="utf-8") as f:
        vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{vaqt}] Funksiya: {funksiya_nomi} | Xatolik: {type(xato).__name__} - {xato}\n")

try:
    x = 10 / 0
except Exception as e:
    yoz_xato_jurnaliga("bolish_amali", e)

print("Audit qayd etildi.")
```

## Tushuntirish va Mantiq:
1. Doimiy monitoring va kelajakdagi xatoliklarni bartaraf etish uchun qulay jurnallashtirish.

## Ishlash natijasi:
```text
Chiqish: Audit qayd etildi.
```


# 492-Topshiriq: Avtomatik qayta ulanuvchi Tarmoq Klienti

## Topshiriq sharti:
Aloqa uzilganda 3 martagacha qayta ulanishga urinuvchi xavfsiz klient sinfi.

## Yechim (Python kodi):
```python
class XavfsizTarmoq:
    def __init__(self):
        self.urinish = 0

    def ulanish(self):
        self.urinish += 1
        if self.urinish < 3:
            raise ConnectionResetError(f"{self.urinish}-urinishda tarmoq uzildi!")
        return "Tarmoq bilan aloqa muvaffaqiyatli o'rnatildi!"

t = XavfsizTarmoq()
for i in range(3):
    try:
        print(t.ulanish())
        break
    except ConnectionResetError as e:
        print(f"[QAYTA URINISH]: {e}")
```

## Tushuntirish va Mantiq:
1. Beqaror internet sharoitida dastur to'xtab qolmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Chiqish: [QAYTA URINISH]... Tarmoq bilan aloqa muvaffaqiyatli o'rnatildi!
```


# 493-Topshiriq: Kiruvchi ma'lumotlarni tozalovchi Sanitar klassi

## Topshiriq sharti:
Foydalanuvchi kiritgan har qanday xom matndan xavfsiz son va so'zlarni ajratib beruvchi sanitar.

## Yechim (Python kodi):
```python
class InputSanitizer:
    @staticmethod
    def toza_butun_son(qiymat, standart=0):
        try:
            return int(str(qiymat).strip())
        except (ValueError, TypeError):
            return standart

    @staticmethod
    def toza_matn(qiymat, standart=""):
        if qiymat is None:
            return standart
        return str(qiymat).strip()

print("Son:", InputSanitizer.toza_butun_son("  450  "))
print("Xato son:", InputSanitizer.toza_butun_son("yaroqsiz", standart=-1))
print("Matn:", InputSanitizer.toza_matn("  Salom Dunyo   "))
```

## Tushuntirish va Mantiq:
1. SQL Injection va XSS hujumlarining oldini oluvchi birinchi himoya chizig'i.

## Ishlash natijasi:
```text
Chiqish: Son: 450, Xato son: -1, Matn: Salom Dunyo
```


# 494-Topshiriq: Xatoliklar iyerarxiyasida isinstance tekshiruvi

## Topshiriq sharti:
Voris xatoliklarni asosiy ota klassi bo'yicha guruhlab ushlash.

## Yechim (Python kodi):
```python
class BazaXatosi(Exception): pass
class ValidatsiyaXatosi(BazaXatosi): pass
class AutentifikatsiyaXatosi(BazaXatosi): pass

def tekshir():
    raise ValidatsiyaXatosi("Maydon bo'sh bo'lishi mumkin emas!")

try:
    tekshir()
except BazaXatosi as e:
    # Ikkala xatolik ham BazaXatosidan meros olgani uchun shu yerda ushlanadi
    print(f"Ushlangan xatolik turi: {type(e).__name__} (BazaXatosining bolasi)")
```

## Tushuntirish va Mantiq:
1. Ota klass orqali barcha bog'liq xatoliklarni bitta `except` bilan tutish mumkin.

## Ishlash natijasi:
```text
Chiqish: Ushlangan xatolik turi: ValidatsiyaXatosi (BazaXatosining bolasi)
```


# 495-Topshiriq: Fayl yopilishini kafolatlovchi xavfsiz o'quvchi

## Topshiriq sharti:
Fayl ichidagi xatolik paydo bo'lganda ham ochiq qolmasligini kafolatlovchi mustahkam o'quvchi.

## Yechim (Python kodi):
```python
def xavfsiz_oqish(fayl_yoli):
    f = None
    try:
        f = open(fayl_yoli, "w", encoding="utf-8")
        f.write("Sinov")
        print("Faylga yozildi.")
    finally:
        if f and not f.closed:
            f.close()
            print("Fayl kafolatlangan holda yopildi!")

xavfsiz_oqish("kafolat_test.txt")
```

## Tushuntirish va Mantiq:
1. `finally` da fayl yopilishi resurs oqib ketishining (Resource Leak) oldini oladi.

## Ishlash natijasi:
```text
Chiqish: Faylga yozildi. -> Fayl kafolatlangan holda yopildi!
```


# 496-Topshiriq: Matnli fayldagi sintaktik xatoliklarni tekshiruvchi Syntax Checker

## Topshiriq sharti:
Python kodini fayldan o'qib uning sintaksisida xato bor-yo'qligini `compile()` orqali xavfsiz tekshiring.

## Yechim (Python kodi):
```python
kod_namuna = """
def salom():
    print("Salom Dunyo!")
"""

def sintaksisni_tekshir(kod):
    try:
        compile(kod, "<string>", "exec")
        return True, "Sintaksis to'g'ri!"
    except SyntaxError as e:
        return False, f"Sintaktik xato: {e.msg} ({e.lineno}-qator)"

print(sintaksisni_tekshir(kod_namuna)[1])
print(sintaksisni_tekshir("def xato_kod(:")[1])
```

## Tushuntirish va Mantiq:
1. `compile(kod, ..., 'exec')` kodni ishga tushirmasdan faqat uning to'g'ri yozilganligini tekshiradi.

## Ishlash natijasi:
```text
Chiqish: Sintaksis to'g'ri!, Sintaktik xato: invalid syntax...
```


# 497-Topshiriq: Chegaradan chiqib ketish (IndexError) va xavfsiz ro'yxat

## Topshiriq sharti:
Ro'yxat indeksidan chiqib ketilganda qulamasdan standart qiymat qaytaruvchi SafeList klassi.

## Yechim (Python kodi):
```python
class SafeList(list):
    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default

mevalar = SafeList(["olma", "anor", "uzum"])
print("0-element :", mevalar.get(0))
print("10-element:", mevalar.get(10, "Mavjud emas"))
```

## Tushuntirish va Mantiq:
1. `list` klassidan meros olib lug'atdagi kabi qulay `get()` metodini taqdim etadi.

## Ishlash natijasi:
```text
Chiqish: 0-element: olma, 10-element: Mavjud emas
```


# 498-Topshiriq: Asenkron va ko'p oqimli xatoliklarni izolyatsiya qilish

## Topshiriq sharti:
Oqimlar ichidagi xatolik butun dasturni to'xtatib qo'ymasligini ta'minlovchi worker wrapper.

## Yechim (Python kodi):
```python
def xavfsiz_oqim_vazifasi(vazifa_id):
    try:
        if vazifa_id == 2:
            raise ValueError(f"Topshiriq #{vazifa_id} da xatolik!")
        print(f"Topshiriq #{vazifa_id} muvaffaqiyatli yakunlandi.")
    except Exception as e:
        print(f"[XATO USHLANDI] {e} (boshqa topshiriqlar davom etadi)")

for i in range(1, 4):
    xavfsiz_oqim_vazifasi(i)
```

## Tushuntirish va Mantiq:
1. Katta hajmdagi ma'lumotlarni parallel yuklashda oqimlar barqarorligining asosi.

## Ishlash natijasi:
```text
Chiqish: Topshiriq #1 muvaffaqiyatli... [XATO USHLANDI]... Topshiriq #3 muvaffaqiyatli.
```


# 499-Topshiriq: Matematik chegaralar xatosi (OverflowError)

## Topshiriq sharti:
Haqiqiy sonlarda (float) eksponentsial chegaradan oshib ketganda `OverflowError` ni xavfsiz boshqarish.

## Yechim (Python kodi):
```python
import math

def xavfsiz_exp(x):
    try:
        return math.exp(x)
    except OverflowError:
        print(f"[OGOHLANTIRISH] math.exp({x}) soni float chegarasidan oshib ketdi!")
        return float('inf')  # Cheksizlik

print("exp(2)   =", xavfsiz_exp(2))
print("exp(1000)=", xavfsiz_exp(1000))
```

## Tushuntirish va Mantiq:
1. Float chegarasidan oshganda dastur qulamasdan cheksizlik (`inf`) qaytaradi.

## Ishlash natijasi:
```text
Chiqish: exp(2) = 7.389..., [OGOHLANTIRISH]... exp(1000) = inf
```


# 500-Topshiriq: Universial Xavfsiz Ijro Menejeri (Crash-Proof Execution Framework)

## Topshiriq sharti:
Har qanday murakkab kod blokini to'liq himoyalovchi, xatoliklarni loglovchi va xavfsiz natija beruvchi to'liq tizim.

## Yechim (Python kodi):
```python
import traceback
from datetime import datetime

class CrashProofRunner:
    @staticmethod
    def run(func, *args, default=None, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n🛡️ [CRASH-PROOF HIMOYA ISHLADI - {vaqt}]")
            print(f"   Xatolik turi : {type(e).__name__}")
            print(f"   Xabar        : {e}")
            print(f"   Standart qaytarildi: {default}")
            return default

# Sinov
def qaltis_amal(a, b):
    return a / b

natija1 = CrashProofRunner.run(qaltis_amal, 10, 2, default=0)
natija2 = CrashProofRunner.run(qaltis_amal, 10, 0, default=0)

print(f"\nNatija 1: {natija1}")
print(f"Natija 2: {natija2}")
```

## Tushuntirish va Mantiq:
1. Butun dasturiy ta'minotning barqarorligini ta'minlovchi universal korporativ himoya qobig'i.

## Ishlash natijasi:
```text
Chiqish: Natija 1: 5.0 -> [CRASH-PROOF HIMOYA ISHLADI] -> Natija 2: 0
```

