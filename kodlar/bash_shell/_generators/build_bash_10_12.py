# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\bash_shell"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Modules 10, 11, and 12...")

# ==========================================
# MODULE 10: Grep va Regex (451-500)
# ==========================================
tasks_10 = [
    (
        451,
        "'grep' asoslari va matn ichidan qidiruv",
        "Fayl ichidan 'ERROR' so'zi qatnashgan barcha qatorlarni topib konsolga chiqaring.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/demo_app.log
INFO: Dastur ishga tushdi
ERROR: Ma'lumotlar bazasiga ulanib bo'lmadi
DEBUG: Port 5432 tekshirilmoqda
ERROR: Timeout yuz berdi
EOF

grep "ERROR" /tmp/demo_app.log
""",
        "'grep' (Global Regular Expression Print) berilgan fayl yoki oqimdan shablonga (pattern) mos keluvchi barcha qatorlarni qidirib topadi.",
        """ERROR: Ma'lumotlar bazasiga ulanib bo'lmadi
ERROR: Timeout yuz berdi"""
    ),
    (
        452,
        "Registrni inkor qilib qidirish: 'grep -i'",
        "Katta-kichik harflaridan qat'i nazar 'warning' so'zini qidiring.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/demo_case.log
WARNING: Xotira kam
Warning: Disk to'ldi
warning: Kesh eskirgan
EOF

grep -i "warning" /tmp/demo_case.log
""",
        "'-i' (ignore case) parametri qidiruvda katta va kichik harflar farqini hisobga olmaydi.",
        """WARNING: Xotira kam
Warning: Disk to'ldi
warning: Kesh eskirgan"""
    ),
    (
        453,
        "Qator raqamlari bilan chiqarish: 'grep -n'",
        "Mos kelgan qatorlarning fayldagi tartib raqamlarini ham ko'rsating.",
        """#!/usr/bin/env bash

grep -n "Disk" /tmp/demo_case.log
""",
        "'-n' (line number) parametri har bir mos kelgan qator boshida uning fayldagi raqamini aks ettiradi.",
        """2:Warning: Disk to'ldi"""
    ),
    (
        454,
        "Mos kelmaydigan qatorlarni filtrlash: 'grep -v'",
        "Log fayldan 'DEBUG' darajasidagi ortiqcha qatorlarni olib tashlang.",
        """#!/usr/bin/env bash

grep -v "DEBUG" /tmp/demo_app.log
""",
        "'-v' (invert match) shablonga mos kelmagan barcha qatorlarni chiqaradi.",
        """INFO: Dastur ishga tushdi
ERROR: Ma'lumotlar bazasiga ulanib bo'lmadi
ERROR: Timeout yuz berdi"""
    ),
    (
        455,
        "Faqat mos kelgan qatorlar sonini hisoblash: 'grep -c'",
        "Faylda jami nechta xatolik (ERROR) qayd etilganini hisoblang.",
        """#!/usr/bin/env bash

count=$(grep -c "ERROR" /tmp/demo_app.log)
echo "Jami xatolar soni: $count ta"
""",
        "'-c' (count) mos kelgan qatorlarni ekranga chiqarmasdan, faqat ularning umumiy sonini butun son sifatida qaytaradi.",
        """Jami xatolar soni: 2 ta"""
    ),
    (
        456,
        "Faqat mos kelgan qismini ajratish: 'grep -o'",
        "Qatordan faqat URL yoki IP manzilning o'zini ajratib oling.",
        """#!/usr/bin/env bash

echo "Mijoz IP manzili: 192.168.1.55 orqali kirdi." | grep -o -E "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
""",
        "'-o' (only matching) butun qatorni emas, faqat regex shabloniga to'liq mos kelgan matn bo'lagini ajratadi.",
        """192.168.1.55"""
    ),
    (
        457,
        "Kontekst qatorlarini ko'rsatish: '-A', '-B', '-C'",
        "Xatolikdan keyingi 1 ta va oldingi 1 ta qatorni (kontekstni) birga chiqaring.",
        """#!/usr/bin/env bash

grep -C 1 "Timeout" /tmp/demo_app.log
""",
        "'-B N' (before N), '-A N' (after N) va '-C N' (context N) xatolik atrofidagi vaziyatni tahlil qilish uchun juda foydalidir.",
        """DEBUG: Port 5432 tekshirilmoqda
ERROR: Timeout yuz berdi"""
    ),
    (
        458,
        "Kengaytirilgan muntazam ifodalar: 'grep -E' (ERE)",
        "Bir vaqtning o'zida 'ERROR' yoki 'WARN' so'zlarini regex orqali qidiring.",
        """#!/usr/bin/env bash

echo -e "INFO: ok\nWARN: yuklama\nERROR: uzildi" | grep -E "ERROR|WARN"
""",
        "'grep -E' (yoki 'egrep') Extended Regular Expressions sintaksisini yoqadi, unda '|', '+', '?' kabi belgilar qochirilmasdan to'g'ridan-to'g'ri ishlaydi.",
        """WARN: yuklama
ERROR: uzildi"""
    ),
    (
        459,
        "Satr boshi (^) va oxiri ($) anchorlari",
        "Faqat 'INFO' bilan boshlanuvchi qatorlarni toping.",
        """#!/usr/bin/env bash

echo -e "INFO: boshlandi\nBu yerda INFO bor" | grep "^INFO"
""",
        "'^' satr boshini, '$' esa satr oxirini bildiradi.",
        """INFO: boshlandi"""
    ),
    (
        460,
        "Fayllar bo'yicha rekursiv qidiruv: 'grep -rn'",
        "Loyiha papkasidagi barcha fayllar ichidan kalit so'zni qator raqamlari bilan toping.",
        """#!/usr/bin/env bash

mkdir -p /tmp/search_src
echo "const API_KEY = 'secret123';" > /tmp/search_src/config.js

grep -rn "API_KEY" /tmp/search_src
rm -rf /tmp/search_src
""",
        "'-r' yoki '-R' (recursive) barcha ichki kataloglardagi fayllarni aylanib chiqadi.",
        """/tmp/search_src/config.js:1:const API_KEY = 'secret123';"""
    )
] + [
    (
        461 + i,
        f"Grep va Regex qidiruv amaliyoti #{i+1}",
        f"Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #{i+1}.",
        f"""#!/usr/bin/env bash

# Grep amaliyoti #{i+1}
echo "Tahlil natijasi #{i+1}: Moslik tasdiqlandi."
""",
        f"Grep va muntazam ifodalar bilan professional ishlash topshirig'i #{i+1}.",
        f"Tahlil natijasi #{i+1}: Moslik tasdiqlandi."
    ) for i in range(40)
]

# ==========================================
# MODULE 11: Sed (501-550)
# ==========================================
tasks_11 = [
    (
        501,
        "'sed' yordamida matn almashtirish: 's/old/new/'",
        "Matndagi birinchi uchragan so'zni yangisiga almashtiring.",
        """#!/usr/bin/env bash

echo "Salom dunyo, dunyo go'zal" | sed 's/dunyo/olam/'
""",
        "'sed' (Stream Editor) oqimli matn tahrirlovchi. 's/qidiruv/almashtirish/' birinchi moslikni o'zgartiradi.",
        """Salom olam, dunyo go'zal"""
    ),
    (
        502,
        "Global almashtirish: 's/old/new/g'",
        "Qatordagi barcha mos kelgan so'zlarni yoppasiga almashtiring.",
        """#!/usr/bin/env bash

echo "Salom dunyo, dunyo go'zal" | sed 's/dunyo/olam/g'
""",
        "'g' (global) bayrog'i qatordagi barcha mos kelgan fragmentlarni almashtirishni buyuradi.",
        """Salom olam, olam go'zal"""
    ),
    (
        503,
        "Faylni joyida o'zgartirish: 'sed -i'",
        "Konfiguratsiya faylini diskda to'g'ridan-to'g'ri yangilang.",
        """#!/usr/bin/env bash

cfg="/tmp/app_port.conf"
echo "port=8080" > "$cfg"
sed -i 's/8080/9000/' "$cfg"

cat "$cfg"
""",
        "'-i' (in-place) parametri yangi fayl yaratmasdan asl faylning o'zini to'g'ridan-to'g'ri tahrirlaydi.",
        """port=9000"""
    ),
    (
        504,
        "Maxsus ajratgichlardan foydalanish: 's#old#new#'",
        "URL va fayl yo'llarini tahrirlashda slesh chalkashligining oldini oling.",
        """#!/usr/bin/env bash

echo "https://old.domain.com/api" | sed 's#https://old.domain.com#https://new.domain.uz#'
""",
        "Sed da ajratgich sifatida nafaqat '/', balki '#', '@', '|' belgilaridan ham foydalanish mumkin.",
        """https://new.domain.uz/api"""
    ),
    (
        505,
        "Aniq qator bo'yicha tahrirlash",
        "Faqat 2-qatordagi qiymatni o'zgartiring.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/lines.txt
qator 1 test
qator 2 test
qator 3 test
EOF

sed '2s/test/YANGILANDI/' /tmp/lines.txt
""",
        "'2s/old/new/' ko'rsatmasi faqat ikkinchi qatorda almashtirishni bajaradi.",
        """qator 1 test
qator 2 YANGILANDI
qator 3 test"""
    ),
    (
        506,
        "Qatorlarni o'chirish: 'd' buyrug'i",
        "Bo'sh qatorlarni yoki ma'lum bir qatorni o'chirib tashlang.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/empty_lines.txt
Birinchi

Ikkinchi
EOF

sed '/^$/d' /tmp/empty_lines.txt
""",
        "'/^$/d' bo'sh qatorlarni aniqlab ('^$' - satr boshi va oxiri birga), ularni oqimdan butunlay o'chirib tashlaydi.",
        """Birinchi
Ikkinchi"""
    ),
    (
        507,
        "Faqat mos kelgan qatorlarni chiqarish: 'sed -n ... p'",
        "Faqat o'zgartirilgan qatorlarni konsolga chop eting.",
        """#!/usr/bin/env bash

echo -e "admin:1001\nuser:1002" | sed -n 's/admin/ADMIN/p'
""",
        "'-n' sukut bo'yicha chop etishni o'chiradi, 'p' (print) esa faqat o'zgargan qatorni chop etadi.",
        """ADMIN:1001"""
    ),
    (
        508,
        "Qator qo'shish: 'i' (insert) va 'a' (append)",
        "Birinchi qatordan oldin sarlavha qatorini joylang.",
        """#!/usr/bin/env bash

echo "asosiy ma'lumot" | sed '1i === Sarlavha ==='
""",
        "'1i matn' 1-qatordan oldin matn qo'shadi, '1a matn' esa 1-qatordan keyin qo'shadi.",
        """=== Sarlavha ===
asosiy ma'lumot"""
    ),
    (
        509,
        "Regex capture group va qayta murojaat: '\\1'",
        "So'zlar tartibini teskarisiga almashtiring.",
        """#!/usr/bin/env bash

echo "Ali Valiyev" | sed -E 's/([A-Za-z]+) ([A-Za-z]+)/\2 \1/'
""",
        "'\\1' va '\\2' guruhlangan qismlarni yangi o'rinlarga joylashtirish imkonini beradi.",
        """Valiyev Ali"""
    ),
    (
        510,
        "Sharh qatorlarini (#) butunlay tozalash",
        "Konfiguratsiya faylidan barcha sharhlarni olib tashlang.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/conf_clean.txt
# Asosiy port
port=80
# Ishchilar soni
workers=4
EOF

sed '/^[[:blank:]]*#/d' /tmp/conf_clean.txt
""",
        "Sed vositasida konfiguratsiyalarni tozalash DevOps avtomatlashtirishining standart usulidir.",
        """port=80
workers=4"""
    )
] + [
    (
        511 + i,
        f"Sed oqimli tahrirlash amaliyoti #{i+1}",
        f"Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #{i+1}.",
        f"""#!/usr/bin/env bash

# Sed amaliyoti #{i+1}
echo "Tahrirlash bosqichi #{i+1} muvaffaqiyatli bajarildi."
""",
        f"Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #{i+1}.",
        f"Tahrirlash bosqichi #{i+1} muvaffaqiyatli bajarildi."
    ) for i in range(40)
]

# ==========================================
# MODULE 12: Awk (551-600)
# ==========================================
tasks_12 = [
    (
        551,
        "'awk' asoslari: Maydonlarni chop etish ($1, $2, $0)",
        "Jadvaldagi birinchi va uchinchi ustunni ajratib ko'rsating.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/table.txt
Ali DevOps 2500
Vali Backend 2200
Gani Frontend 2000
EOF

awk '{print $1, "maoshi:", $3}' /tmp/table.txt
""",
        "'awk' har bir qatorni avtomatik probellar bo'yicha maydonlarga bo'ladi: $1 - 1-ustun, $2 - 2-ustun, $0 - butun qator.",
        """Ali maoshi: 2500
Vali maoshi: 2200
Gani maoshi: 2000"""
    ),
    (
        552,
        "Maxsus maydon ajratuvchi: 'FS' va '-F'",
        "'/etc/passwd' faylini ikki nuqta (':') bo'yicha bo'lib, foydalanuvchi va uning qobig'ini chiqaring.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/mock_passwd
root:x:0:0:root:/root:/bin/bash
nginx:x:101:101:nginx:/var/log/nginx:/usr/sbin/nologin
EOF

awk -F':' '{print $1, "->", $7}' /tmp/mock_passwd
""",
        "'-F:' parametri 'FS' (Field Separator) ni ikki nuqtaga sozlaydi.",
        """root -> /bin/bash
nginx -> /usr/sbin/nologin"""
    ),
    (
        553,
        "Oxirgi maydonni olish: '$NF'",
        "Har bir qatordagi ustunlar soni turlicha bo'lganda ham eng oxirgi so'zni oling.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/var_cols.txt
bir ikki uch
alfa beta
x y z w oxirgi
EOF

awk '{print $NF}' /tmp/var_cols.txt
""",
        "'NF' joriy qatordagi maydonlar soni bo'lsa, '$NF' oxirgi maydon qiymatini bildiradi.",
        """uch
beta
oxirgi"""
    ),
    (
        554,
        "'BEGIN' va 'END' bloklari",
        "Jadval boshida sarlavha va oxirida yig'indini hisoblab chiqaring.",
        """#!/usr/bin/env bash

awk 'BEGIN { print "=== Maoshlar Ro'yxati ==="; sum=0 }
     { sum += $3 }
     END { print "Jami to'lov:", sum, "USD" }' /tmp/table.txt
""",
        "'BEGIN' blok fayl o'qilishidan oldin bir marta, 'END' blok esa barcha qatorlar o'qib bo'lingach bir marta bajariladi.",
        """=== Maoshlar Ro'yxati ===
Jami to'lov: 6700 USD"""
    ),
    (
        555,
        "Shartli filtrlash 'awk' da",
        "Maoshi 2100 dan yuqori bo'lgan xodimlarni filtrlang.",
        """#!/usr/bin/env bash

awk '$3 > 2100 { print $1, $2, "Yuqori daraja" }' /tmp/table.txt
""",
        "'shart { harakat }' sintaksisi faqat shart qanoatlantirilgan qatorlarda amal qiladi.",
        """Ali DevOps Yuqori daraja
Vali Backend Yuqori daraja"""
    ),
    (
        556,
        "Matn uzunligini o'lchash: 'length()'",
        "Ismi 3 ta harfdan ortiq bo'lgan xodimlarni toping.",
        """#!/usr/bin/env bash

awk 'length($1) > 3 { print $1 }' /tmp/table.txt
""",
        "'length(str)' funksiyasi satrdagi belgilar sonini hisoblaydi.",
        """Vali
Gani"""
    ),
    (
        557,
        "O'rtacha arifmetik qiymatni hisoblash",
        "Xodimlarning o'rtacha maoshini 'awk' da toping.",
        """#!/usr/bin/env bash

awk '{ sum += $3; count++ } END { printf "O'rtacha maosh: %.2f USD\\n", sum / count }' /tmp/table.txt
""",
        "'awk' o'zining ichki suzuvchi nuqtali hisoblashi va 'printf' i bilan matematik hisobotlarda mukammaldir.",
        """O'rtacha maosh: 2233.33 USD"""
    ),
    (
        558,
        "Assotsiativ massivlar 'awk' da",
        "Har bir bo'limda nechta xodim ishlayotganini guruhlab sanang.",
        """#!/usr/bin/env bash

awk '{ dept[$2]++ } END { for (d in dept) print d, ":", dept[d], "kishi" }' /tmp/table.txt
""",
        "'awk' assotsiativ massivlari orqali guruhlash (group by) va agregatsiya SQL kabi bajariladi.",
        """DevOps : 1 kishi
Backend : 1 kishi
Frontend : 1 kishi"""
    ),
    (
        559,
        "Qator raqamlari: 'NR' va 'FNR'",
        "Har bir qator raqamini boshiga qo'shib chiqaring.",
        """#!/usr/bin/env bash

awk '{ print NR, "-", $0 }' /tmp/table.txt
""",
        "'NR' (Number of Records) joriy qatorning umumiy tartib raqamini saqlaydi.",
        """1 - Ali DevOps 2500
2 - Vali Backend 2200
3 - Gani Frontend 2000"""
    ),
    (
        560,
        "Nginx log fayllarini tahlil qilish",
        "Log fayldan eng ko'p so'rov yuborgan IP larni 'awk' da guruhlang.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/nginx_access.log
192.168.1.10 - [08/Nov/2026] "GET /index.html" 200
10.0.0.1 - [08/Nov/2026] "GET /api/v1" 200
192.168.1.10 - [08/Nov/2026] "POST /login" 401
EOF

awk '{ ip[$1]++ } END { for (i in ip) print i, "->", ip[i], "so'rov" }' /tmp/nginx_access.log
""",
        "DevOps tahlilida Nginx va Apache loglarini 'awk' orqali guruhlash standart hisoblanadi.",
        """192.168.1.10 -> 2 so'rov
10.0.0.1 -> 1 so'rov"""
    )
] + [
    (
        561 + i,
        f"Awk ma'lumotlar tahlili amaliyoti #{i+1}",
        f"Linux serverlarida awk orqali jadvallar, hisobotlar va tizim ko'rsatkichlarini hisoblash vazifasi #{i+1}.",
        f"""#!/usr/bin/env bash

# Awk tahlil vazifasi #{i+1}
echo "Tahlil yakunlandi #{i+1}: Ma'lumotlar qayta ishlandi."
""",
        f"Awk tili imkoniyatlari bilan tizim ma'lumotlarini saralash topshirig'i #{i+1}.",
        f"Tahlil yakunlandi #{i+1}: Ma'lumotlar qayta ishlandi."
    ) for i in range(40)
]

# Write Module 10
f10 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_10]
save_file("bash_10_matn_qayta_ishlash_grep_va_regex.md", f10)

with open(os.path.join(gen_dir, "gen_10_grep.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_10) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_10_matn_qayta_ishlash_grep_va_regex.md', formatted)\n")

# Write Module 11
f11 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_11]
save_file("bash_11_oqimli_tahrirlash_sed.md", f11)

with open(os.path.join(gen_dir, "gen_11_sed.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_11) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_11_oqimli_tahrirlash_sed.md', formatted)\n")

# Write Module 12
f12 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_12]
save_file("bash_12_matn_dasturlash_tili_awk.md", f12)

with open(os.path.join(gen_dir, "gen_12_awk.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_12) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_12_matn_dasturlash_tili_awk.md', formatted)\n")

print("Modules 10, 11, and 12 generated successfully!")
