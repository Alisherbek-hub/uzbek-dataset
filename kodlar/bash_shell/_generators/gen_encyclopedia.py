# -*- coding: utf-8 -*-
"""
Generator for bash_mukammal_qollanma.md
Comprehensive Fundamental Encyclopedia for Bash / Shell Scripting & DevOps Automation
"""

import os

ENCYCLOPEDIA_CONTENT = """# Bash / Shell: Mukammal Ensiklopediya va Fundamental Qo'llanma
**Loyiha:** Khorazmiy AI — O'zbek Tilidagi Katta Dasturlash Dataseti  
**Muallif:** Khorazmiy AI Bash / Shell Dataset Specialist  
**Versiya:** GNU Bash 5.2+ / POSIX Standard (2026-yil holatiga)  
**Qamrovi:** Shell tili falsafasi, Interpretator arxitekturasi, Parameter Expansion, Fayl deskriptorlari va I/O yo'naltirish, Matn tahlili triosi (grep, sed, awk), Jarayonlar va signallar boshqaruvi, Cron va Systemd timers, DevOps va Docker avtomatlashtirish, CI/CD quvurlari, Defensive Bash va Kiberxavfsizlik.

---

## Mundarija
1. [Kirish va Shell Falsafasi](#1-kirish-va-shell-falsafasi)
2. [Shell Interpretatorining Ichki Arxitekturasi](#2-shell-interpretatorining-ichki-arxitekturasi)
3. [O'zgaruvchilar va Parameter Expansion Chuqurligi](#3-ozgaruvchilar-va-parameter-expansion-chuqurligi)
4. [Kiritish-Chiqarish (I/O), Fayl Deskriptorlari va Quvurlar](#4-kiritish-chiqarish-io-fayl-deskriptorlari-va-quvurlar)
5. [Matn Tahlili Triosi: Grep, Sed va Awk Falsafasi](#5-matn-tahlili-triosi-grep-sed-va-awk-falsafasi)
6. [Jarayonlar, Signallar va Xotira Resurslari Boshqaruvi](#6-jarayonlar-signallar-va-xotira-resurslari-boshqaruvi)
7. [Vazifalarni Rejalashtirish: Cron va Systemd Timers](#7-vazifalarni-rejalashtirish-cron-va-systemd-timers)
8. [DevOps, Konteynerlar (Docker) va CI/CD Avtomatlashtirish](#8-devops-konteynerlar-docker-va-cicd-avtomatlashtirish)
9. [Defensive Bash va Kiberxavfsizlik Standartlari](#9-defensive-bash-va-kiberxavfsizlik-standartlari)
10. [Professional Xulosa va Best Practices](#10-professional-xulosa-va-best-practices)

---

## 1. Kirish va Shell Falsafasi

Unix va Linux operatsion tizimlarida qobiq (Shell) shunchaki foydalanuvchi buyruqlarini qabul qiluvchi oddiy terminal emas, balki to'laqonli, qudratli va dinamik dasturlash muhitidir. 1970-yillarda Ken Tompson va Dennis Ritchi tomonidan asos solingan Unix falsafasining markaziy ustunlaridan biri shunday yangraydi:
> *"Har bir dastur faqat bitta ishni bajarsin va uni mukammal qilsin. Dasturlar bir-biri bilan oson bog'lanishi uchun ma'lumotlar oqimlaridan foydalansin."*

Bash (Bourne Again Shell) 1989-yilda Brayan Foks (Brian Fox) tomonidan GNU loyihasi doirasida Stiven Bornning original Sh (Bourne Shell) interpretatorining o'rnini bosuvchi erkin va kengaytirilgan qobiq sifatida taqdim etildi. Bugungi kunda Bash barcha Linux distributivlarida, server infratuzilmalarida, bulutli platformalarda (AWS, GCP, Azure) va zamonaviy konteyner orkestratsiyasida (Kubernetes, Docker) avtomatlashtirishning asosiy tili hisoblanadi.

### Shell Turlarining Qiyosiy Tahlili:
1. **sh (Bourne Shell):** Tarixiy poydevor, POSIX standartining o'zagi. Juda sodda, lekin massivlar va qulayliklar cheklangan.
2. **bash (Bourne Again Shell):** Dunyodagi eng ommabop qobiq. Massivlar, regex, assotsiativ lug'atlar, qulay debugging va moslashuvchanlikka ega.
3. **dash (Debian Almquist Shell):** Juda yengil, tezkor va minimalistik POSIX qobiq. Ubuntu va Debian tizimlarida `/bin/sh` sifatida yuklanadi (tezkor boot uchun).
4. **zsh (Z Shell):** macOS ning standart interaktiv qobig'i. Plaginlar va vizual mavzular uchun qulay, lekin server ishlab chiqarishida Bash asosiy standart bo'lib qolmoqda.

---

## 2. Shell Interpretatorining Ichki Arxitekturasi

Bash buyruqlar satrida kiritilgan matnni operatsion tizim chaqiruviga aylantirishda qat'iy va ko'p bosqichli kengaytirish (expansion) konveyeridan o'tadi:

```
[Foydalanuvchi Matni]
        │
        ▼
[1. Tokenization & Parsing] ──> Matn ajratgichlar (bo'shliqlar, quotes) bo'yicha so'zlarga bo'linadi
        │
        ▼
[2. Brace Expansion]        ──> {1..10}, {A,B,C} ro'yxatlarga aylanadi
        │
        ▼
[3. Tilde Expansion]        ──> ~ foydalanuvchi uy katalogiga ($HOME) aylanadi
        │
        ▼
[4. Parameter & Variable]   ──> $VAR va ${VAR:-default} qiymatlari joylanadi
        │
        ▼
[5. Command Substitution]   ──> $(cmd) subshell orqali bajarilib, natijasi olinadi
        │
        ▼
[6. Arithmetic Expansion]   ──> $(( 2 + 2 )) arifmetik ifodalari hisoblanadi
        │
        ▼
[7. Word Splitting]         ──> IFS belgisi bo'yicha so'zlar bo'linadi (agar tirnoqqa olinmagan bo'lsa)
        │
        ▼
[8. Pathname (Globbing)]    ──> *.txt, [a-z]* fayl tizimi nomlariga kengayadi
        │
        ▼
[9. Quote Removal]          ──> Qo'shtirnoq va bir tirnoqlar olib tashlanadi
        │
        ▼
[10. Buyruqni Ijro Qilish]  ──> Builtin yoki execve() tizim chaqiruvi orqali ishga tushadi
```

Ushbu ketma-ketlikni tushunish skriptlardagi kutilmagan xatoliklarning (masalan, bo'sh joylari bor fayl nomlari buzilishi yoki wildcard kengayib ketishi) oldini olishda hal qiluvchi ahamiyatga ega.

---

## 3. O'zgaruvchilar va Parameter Expansion Chuqurligi

Bash tilida o'zgaruvchilar bilan ishlash shunchaki qiymat saqlash emas, balki kuchli ichki matn protsessoridir. Parameter Expansion yordamida tashqi dasturlarni (`cut`, `sed`, `awk`) chaqirmasdan, xotirada mikrosekundlarda ma'lumotlarni o'zgartirish mumkin.

### Eng Muhim Parameter Expansion Formulalari:
- **Standart qiymatlar:**
  - `${var:-default}` — Agar `var` bo'sh yoki unset bo'lsa, `default` ni qaytaradi.
  - `${var:=default}` — Agar `var` bo'sh bo'lsa, unga `default` qiymatini biriktiradi.
  - `${var:?xato_xabari}` — O'zgaruvchi yo'q bo'lsa, xato xabari bilan ijroni to'xtatadi.
- **Satr qirqish va o'lchash:**
  - `${#var}` — Satrdagi belgilar soni.
  - `${var:offset:length}` — Substring ajratish.
- **Prefiks va Suffikslarni tozalash:**
  - `${var#pattern}` — Boshidan eng qisqa mos qismni olib tashlash.
  - `${var##pattern}` — Boshidan eng uzun mos qismni olib tashlash (basename kabi).
  - `${var%pattern}` — Oxiridan eng qisqa mos qismni olib tashlash (kengaytmasiz nom).
  - `${var%%pattern}` — Oxiridan eng uzun mos qismni olib tashlash.
- **Almashtirish va registr:**
  - `${var/old/new}` — Birinchi moslikni almashtirish.
  - `${var//old/new}` — Barcha mosliklarni global almashtirish.
  - `${var^^}` — To'liq UPPERCASE ga o'tkazish.
  - `${var,,}` — To'liq lowercase ga o'tkazish.

---

## 4. Kiritish-Chiqarish (I/O), Fayl Deskriptorlari va Quvurlar

Linux-da "hamma narsa fayldir". Har bir ishga tushirilgan jarayon operatsion tizim yadrosi tomonidan boshqariluvchi Fayl Deskriptorlari (File Descriptors - FD) orqali muloqot qiladi:
- **FD 0 (stdin):** Standart kiritish oqimi.
- **FD 1 (stdout):** Standart chiqish oqimi.
- **FD 2 (stderr):** Standart xatolik oqimi.

### Qayta Yo'naltirish Operatorlari:
- `>` — Faylni qayta yozish (truncate).
- `>>` — Fayl oxiriga qo'shish (append).
- `<` — Fayldan stdin ga o'qish.
- `2>&1` — Stderr ni stdout oqimiga birlashtirish.
- `&>` yoki `&>>` — Ikkala oqimni birdaniga faylga yo'naltirish.
- `exec 3> fayl` — Maxsus fayl deskriptorini ochish va `exec 3>&-` bilan yopish.
- `|` (Pipe) — Birinchi jarayonning stdout ini ikkinchi jarayonning stdin iga xotiradagi halqasimon bufer (circular buffer) orqali to'g'ridan-to'g'ri bog'lash.

---

## 5. Matn Tahlili Triosi: Grep, Sed va Awk Falsafasi

Unix muhitida ma'lumotlarni qayta ishlashning uchta buyuk ustuni mavjud:

### 1. `grep` — Filtrlovchi (Filter)
Faqat berilgan qoidaga (muntazam ifodaga) mos keluvchi qatorlarni qidirib topish va saralash uchun ixtisoslashgan.
- Foydali bayroqlar: `-i` (registrni inkor qilish), `-v` (teskari filtr), `-E` (kengaytirilgan regex), `-o` (faqat mos kelgan qism), `-n` (qator raqamlari).

### 2. `sed` — Oqimli Tahrirlovchi (Stream Editor)
Matnni satrma-satr qabul qilib, oqimning o'zida almashtirish, o'chirish va qo'shish amallarini bajaradi.
- Asosiy buyruqlar: `s/eski/yangi/g`, `d` (o'chirish), `i` va `a` (qo'shish), `sed -i` (faylni joyida tahrirlash).

### 3. `awk` — Matn Dasturlash Tili (Data Processor)
To'liq va mustaqil dasturlash tili. Jadvallar, ustunlar, hisob-kitoblar va statistik hisobotlar yaratish uchun eng qudratli vosita.
- Asosiy o'zgaruvchilar: `$0` (butun satr), `$1..$NF` (ustunlar), `NR` (qator raqami), `FS` (maydon ajratuvchi), `BEGIN` va `END` bloklari, assotsiativ massivlar.

---

## 6. Jarayonlar, Signallar va Xotira Resurslari Boshqaruvi

Linux ko'p vazifali (multitasking) operatsion tizimdir. Bash orqali fonda va parallel rejimda vazifalarni boshqarish DevOps avtomatlashtirishining poydevoridir:
- `cmd &` — Buyruqni fon rejimida ishga tushirish.
- `$!` — Oxirgi fon jarayonining PID raqami.
- `$$` — Skriptning o'z PID raqami.
- `jobs` va `fg %N` — Fon vazifalarini nazorat qilish va ekranga qaytarish.
- `wait $PID` — Jarayonlar yakunlanishini kutish.
- `kill -SIGNAL PID` — Signallar yuborish:
  - `SIGTERM (15)`: Muloyim to'xtash so'rovi (resurslarni xavfsiz tozalashga imkon beradi).
  - `SIGKILL (9)`: Yadro tomonidan darhol majburiy to'xtatish.
  - `SIGHUP (1)`: Terminal uzilishi yoki konfiguratsiyani qayta yuklash signali.
- `trap 'cleanup' EXIT INT TERM` — Signallarni ushlab xavfsiz tozalashni kafolatlash.

---

## 7. Vazifalarni Rejalashtirish: Cron va Systemd Timers

Avtomatlashtirilgan zaxiralash, monitoring va tozalash ishlari vaqt bo'yicha rejalashtiriladi:
- **Crontab:** An'anaviy va ommabop rejalashtiruvchi. 5 ta maydondan iborat (`daqiqa soat kun oy haftakuni`). Ehtiyot bo'lish zarur: Cron cheklangan muhitda (`PATH` kam) ishlaydi, shuning uchun mutlaq yo'llar ko'rsatilishi shart.
- **Systemd Timers:** Zamonaviy Linux standarti. `.timer` va `.service` birliklari orqali boshqariladi. O'tkazib yuborilgan topshiriqlarni tiklash (`Persistent=true`), mustahkam loglash (`journalctl`) va resurs cheklovlarini qo'llash imkonini beradi.

---

## 8. DevOps, Konteynerlar (Docker) va CI/CD Avtomatlashtirish

Zamonaviy bulutli dunyoda Bash barcha CI/CD (GitHub Actions, GitLab CI, Jenkins) platformalarining asosiy boshqaruvchisidir:
- **Docker Boshqaruvi:** Konteynerlar sog'lomligini tekshirish (`docker inspect`), eskirgan tasvirlar va hajmlarni tozalash (`docker system prune`), ko'p konteynerli loyihalarni Docker Compose bilan nol uzilishda yangilash.
- **Atomik Deploy:** Simvolik havolalar (`ln -sfn`) orqali yangi relizga bir zumda o'tish (Zero-Downtime Deployment).
- **Avtomatik Rollback:** Yangi relizda xatolik aniqlanganda darhol oldingi barqaror versiyaga qaytarish mexanizmi.

---

## 9. Defensive Bash va Kiberxavfsizlik Standartlari

Ishlab chiqarish (Production) tizimlarida ishlatiladigan har bir Bash skripti quyidagi qat'iy Defensive standartlarga javob berishi shart:

```bash
#!/usr/bin/env bash
# Defensive Bash Oltin Qoidasi
set -euo pipefail
IFS=$'\n\t'
```

1. **`set -e`:** Har qanday buyruq xato bergan zahoti skriptni to'xtatadi.
2. **`set -u`:** E'lon qilinmagan o'zgaruvchilardan foydalanilganda xato beradi (masalan, `rm -rf "$MDIR/"` da `MDIR` bo'sh bo'lsa tizim o'chib ketishidan asraydi).
3. **`set -o pipefail`:** Quvur ichidagi oraliq xatoliklarni e'tibordan chetda qoldirmaydi.
4. **Har doim o'zgaruvchilarni qo'shtirnoqqa olish:** `"$var"` ko'rinishida yozish so'zlarning probellar bo'yicha bo'linib ketishi va globbing hujumlarining oldini oladi.
5. **Xavfsiz vaqtinchalik fayllar:** `mktemp` va `trap cleanup EXIT` orqali xotirani toza saqlash.
6. **Input Sanitization:** Foydalanuvchi ma'lumotlaridagi in'eksiya (`rm`, `;`, `|`) belgilarini qat'iy filtrlash.

---

## 10. Professional Xulosa va Best Practices

Bash — tizim muhandisi, DevOps mutaxassisi va kiberxavfsizlik tahlilchisining eng ishonchli qurolidir. U operatsion tizimning yuragi bilan bevosita gaplashish, murakkab serverlar klasterini birgina skript orqali uyg'unlashtirish imkonini beradi.

### Asosiy Qoidalar (Cheatsheet):
- Skriptni doimo to'g'ri shebang bilan boshlang: `#!/usr/bin/env bash`.
- O'zgaruvchilarga qiymat berishda tenglik atrofida bo'sh joy qoldirmang (`VAR=val`).
- Har bir yozilgan skriptni **ShellCheck** statik analizatori orqali tekshiring.
- Takrorlanuvchi kodlarni mustaqil funksiyalarga va kutubxona modullariga ajrating.
- Xatolik xabarlarini doimo standart xatolik oqimiga yo'naltiring: `echo "Xato" >&2`.
- Ishonchli, qisqa va tushunarli kod yozish — barqaror server infratuzilmasining kafolatidir.
"""

def generate_encyclopedia():
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\bash_shell"
    out_path = os.path.join(base_dir, "bash_mukammal_qollanma.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(ENCYCLOPEDIA_CONTENT.strip() + "\n")
    size = os.path.getsize(out_path)
    print(f"bash_mukammal_qollanma.md muvaffaqiyatli yaratildi! Hajmi: {size} bayt")

if __name__ == "__main__":
    generate_encyclopedia()
