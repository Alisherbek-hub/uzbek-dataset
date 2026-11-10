# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\bash_shell"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Modules 02 and 03...")

# ==========================================
# MODULE 02: O'zgaruvchilar va parametrlar (51-100)
# ==========================================
tasks_02 = [
    (
        51,
        "O'zgaruvchi e'lon qilish va sintaksis qoidalari",
        "Bash-da server porti va loyiha nomini o'zgaruvchilarda to'g'ri e'lon qiling va ularni chop eting.",
        """#!/usr/bin/env bash

# O'zgaruvchi nomi harf yoki pastki chiziq bilan boshlanishi kerak
SERVER_PORT=8080
PROJECT_NAME="KhorazmiyBilling"

echo "Loyiha: $PROJECT_NAME"
echo "Port: $SERVER_PORT"
""",
        "Bash o'zgaruvchi e'lon qilishda juda qat'iy: nom, '=' belgisi va qiymat o'rtasida hech qanday probel bo'lmasligi kerak. O'zgaruvchiga murojaat qilishda '$' prefiksi qo'yiladi, xavfsizlik uchun esa uni qo'sh tirnoqqa olish (\"$PROJECT_NAME\") tavsiya etiladi.",
        """Loyiha: KhorazmiyBilling
Port: 8080"""
    ),
    (
        52,
        "Bo'sh qiymat berish va tekshirish",
        "Bo'sh satr bilan e'lon qilingan o'zgaruvchini yarating va uning bo'shligini tekshiring.",
        """#!/usr/bin/env bash

AUTH_TOKEN=""

if [ -z "$AUTH_TOKEN" ]; then
    echo "Ogohlantirish: Autentifikatsiya tokeni kiritilmagan!"
fi
""",
        "O'zgaruvchiga 'var=\"\"' tarzida bo'sh qiymat berish mumkin. '-z' sharti o'zgaruvchining uzunligi nolga teng ekanligini (ya'ni bo'shligini) tekshiradi.",
        """Ogohlantirish: Autentifikatsiya tokeni kiritilmagan!"""
    ),
    (
        53,
        "Standart qiymat berish: '${var:-default}'",
        "Agar foydalanuvchi portni kiritmagan bo'lsa, avtomatik 3000-portni standart qiymat sifatida oling.",
        """#!/usr/bin/env bash

# PORT o'rnatilmagan yoki bo'sh
APP_PORT="${PORT:-3000}"

echo "Ilova ishga tushadigan port: $APP_PORT"
""",
        "'${var:-default}' sintaksisi: agar 'var' o'rnatilmagan (unset) yoki bo'sh bo'lsa, 'default' qiymatni qaytaradi, lekin 'var' o'zgaruvchisining o'zini o'zgartirmaydi.",
        """Ilova ishga tushadigan port: 3000"""
    ),
    (
        54,
        "Standart qiymatni o'zlashtirish: '${var:=default}'",
        "Agar o'zgaruvchi bo'sh bo'lsa, unga standart qiymatni to'g'ridan-to'g'ri biriktiring.",
        """#!/usr/bin/env bash

# DB_HOST o'zgaruvchisi mavjud emas
echo "Ulanish manzili: ${DB_HOST:=localhost}"
echo "DB_HOST qiymati endi o'zgardi: $DB_HOST"
""",
        "'${var:=default}' sintaksisi: agar 'var' mavjud bo'lmasa yoki bo'sh bo'lsa, 'default' qiymatni qaytaradi VA shu qiymatni 'var' ga biriktiradi (o'zlashtiradi).",
        """Ulanish manzili: localhost
DB_HOST qiymati endi o'zgardi: localhost"""
    ),
    (
        55,
        "Muqobil qiymatni tekshirish: '${var:+alternate}'",
        "Agar debug rejimi yoqilgan bo'lsa, qo'shimcha jurnal xabarini chiqaring.",
        """#!/usr/bin/env bash

DEBUG_MODE="active"
LOG_LEVEL="${DEBUG_MODE:+VERBOSE}"

echo "Jurnal darajasi: $LOG_LEVEL"
""",
        "'${var:+alternate}' sintaksisi: agar 'var' o'rnatilgan va bo'sh bo'lmasa, 'alternate' qiymatini qaytaradi. Agar bo'sh yoki unset bo'lsa, bo'sh satr qaytaradi.",
        """Jurnal darajasi: VERBOSE"""
    ),
    (
        56,
        "Majburiy parametr tekshiruvi: '${var:?error_msg}'",
        "Zarur muhit o'zgaruvchisi berilmaganda skriptni xatolik bilan to'xtating.",
        """#!/usr/bin/env bash

CONFIG_PATH="/etc/app.conf"
echo "Konfiguratsiya: ${CONFIG_PATH:?Xatolik: CONFIG_PATH ko'rsatilishi shart!}"
""",
        "'${var:?xato_xabari}' sintaksisi: agar o'zgaruvchi mavjud bo'lmasa yoki bo'sh bo'lsa, Bash skript ijrosini darhol to'xtatadi va stderr ga ko'rsatilgan xabarni chiqaradi.",
        """Konfiguratsiya: /etc/app.conf"""
    ),
    (
        57,
        "Satr uzunligini hisoblash: '${#var}'",
        "Foydalanuvchi paroli xavfsizlik talablariga muvofiq kamida 8 ta belgidan iborat ekanligini tekshiring.",
        """#!/usr/bin/env bash

password="SecureUser2026!"
length=${#password}

echo "Parol uzunligi: $length ta belgi"
""",
        "'${#var}' sintaksisi berilgan o'zgaruvchi qiymatidagi belgilar sonini qaytaradi. Bu tashqi 'wc -c' buyrug'ini chaqirmasdan, xotirada tezkorlik bilan o'lchash imkonini beradi.",
        """Parol uzunligi: 15 ta belgi"""
    ),
    (
        58,
        "Satrdan boshlang'ich pozitsiya bo'yicha qirqish: '${var:offset}'",
        "Telefon raqamining xalqaro kodi (+998) dan keyingi asosiy qismini ajrating.",
        """#!/usr/bin/env bash

phone="+998901234567"
local_part="${phone:4}"

echo "Mahalliy raqam: $local_part"
""",
        "'${var:offset}' sintaksisi satrning 0 dan boshlanuvchi 'offset' indeksidan to satr oxirigacha bo'lgan qismini qirqib oladi.",
        """Mahalliy raqam: 901234567"""
    ),
    (
        59,
        "Satrning qism qismini ajratish: '${var:offset:length}'",
        "Sana satridan yil, oy va kunni alohida ajratib oling.",
        """#!/usr/bin/env bash

date_str="2026-11-08"
year="${date_str:0:4}"
month="${date_str:5:2}"
day="${date_str:8:2}"

echo "Yil: $year, Oy: $month, Kun: $day"
""",
        "'${var:offset:length}' sintaksisi 'offset' o'rnidan boshlab aniq 'length' ta belgini ajratib beradi.",
        """Yil: 2026, Oy: 11, Kun: 08"""
    ),
    (
        60,
        "Satr oxiridan qirqish: '${var: -N}'",
        "Fayl identifikatorining oxirgi 4 ta belgisini ajratib oling.",
        """#!/usr/bin/env bash

file_uuid="f47ac10b-58cc-4372-a567-0e02b2c3d479"
suffix="${file_uuid: -4}"

echo "Oxirgi 4 belgi: $suffix"
""",
        "Manfiy indeks orqali satr oxiridan qirqishda manfiy ishora oldidan bo'sh joy qoldirish shart ('${var: -N}'), aks holda Bash uni standart qiymat berish '${var:-default}' deb xato tushunadi.",
        """Oxirgi 4 belgi: d479"""
    ),
    (
        61,
        "Boshidan eng qisqa mos patternni olib tashlash: '${var#pattern}'",
        "Yo'l satridan boshidagi birinchi katalog nomini qirqib tashlang.",
        """#!/usr/bin/env bash

filepath="/usr/local/bin/python3"
relative="${filepath#*/}"

echo "Qisqa prefiks olib tashlangach: $relative"
""",
        "'${var#pattern}' satr boshidan mos keluvchi eng qisqa (non-greedy) qismni olib tashlaydi. '*/' dastlabki '/' belgisigacha bo'lgan bo'lakni o'chiradi.",
        """Qisqa prefiks olib tashlangach: usr/local/bin/python3"""
    ),
    (
        62,
        "Boshidan eng uzun mos patternni olib tashlash: '${var##pattern}'",
        "To'liq fayl yo'lidan faqat fayl nomining o'zini ajratib oling (basename kabi).",
        """#!/usr/bin/env bash

filepath="/var/log/nginx/access.log"
filename="${filepath##*/}"

echo "Faqat fayl nomi: $filename"
""",
        "'${var##pattern}' satr boshidan mos keluvchi eng uzun (greedy) qismni olib tashlaydi. '*/' oxirgi '/' belgisigacha bo'lgan butun yo'lni kesib tashlaydi, natijada faqat fayl nomi qoladi.",
        """Faqat fayl nomi: access.log"""
    ),
    (
        63,
        "Oxiridan eng qisqa mos patternni olib tashlash: '${var%pattern}'",
        "Fayl nomidan uning eng oxirgi kengaytmasini olib tashlang.",
        """#!/usr/bin/env bash

archive="backup_2026.tar.gz"
without_gz="${archive%.*}"

echo "Oxirgi kengaytmasiz: $without_gz"
""",
        "'${var%pattern}' satr oxiridan eng qisqa mos keluvchi qismni olib tashlaydi. '.*' oxirgi nuqtadan keyingi '.gz' qismini qirqadi.",
        """Oxirgi kengaytmasiz: backup_2026.tar"""
    ),
    (
        64,
        "Oxiridan eng uzun mos patternni olib tashlash: '${var%%pattern}'",
        "Fayl nomidan barcha qo'shaloq kengaytmalarni tozalab, asl nomni oling.",
        """#!/usr/bin/env bash

archive="dataset_archive.tar.gz"
base_name="${archive%%.*}"

echo "Barcha kengaytmalarsiz asosiy nom: $base_name"
""",
        "'${var%%pattern}' satr oxiridan mos keluvchi eng uzun qismni o'chiradi. Natijada birinchi nuqtadan boshlab butun '.tar.gz' olib tashlanadi.",
        """Barcha kengaytmalarsiz asosiy nom: dataset_archive"""
    ),
    (
        65,
        "Fayl nomidan faqat kengaytmani ajratish ('${file##*.}')",
        "Har qanday fayl yo'lidan uning formatini (kengaytmasini) aniqlang.",
        """#!/usr/bin/env bash

doc="report_final.pdf"
ext="${doc##*.}"

echo "Fayl turi: $ext"
""",
        "'${file##*.}' satr boshidan eng oxirgi nuqtagacha bo'lgan barcha belgilarni kesib tashlaydi, natijada faqat kengaytma qoladi.",
        """Fayl turi: pdf"""
    ),
    (
        66,
        "URL manzilidan domenni ajratib olish",
        "Veb URL dan protokol va yo'llarni qirqib, faqat xost nomini oling.",
        """#!/usr/bin/env bash

url="https://api.khorazmiy.uz/v1/auth"
proto_removed="${url#*://}"
domain="${proto_removed%%/*}"

echo "Domen nomi: $domain"
""",
        "Parameter expansion larni ketma-ket qo'llash orqali murakkab satrlarni qismlarga ajratish tashqi utilitalarsiz tez va xotirada xavfsiz bajariladi.",
        """Domen nomi: api.khorazmiy.uz"""
    ),
    (
        67,
        "Birinchi mos patternni almashtirish: '${var/pattern/replacement}'",
        "Matndagi dastlabki xato so'zni to'g'rilang.",
        """#!/usr/bin/env bash

msg="Xatolik: server xatolik berdi"
corrected="${msg/xatolik/ogohlantirish}"

echo "Tuzatilgan: $corrected"
""",
        "'${var/pattern/replacement}' satrdagi faqat birinchi uchragan 'pattern' ni yangi 'replacement' ga almashtiradi.",
        """Tuzatilgan: Xatolik: server ogohlantirish berdi"""
    ),
    (
        68,
        "Barcha mos patternlarni almashtirish: '${var//pattern/replacement}'",
        "Matndagi barcha nuqtalarni chiziqcha bilan almashtiring.",
        """#!/usr/bin/env bash

ip_address="192.168.1.105"
slug="${ip_address//./-}"

echo "Slug formati: $slug"
""",
        "Ikkita slesh '//' qo'llanganda satrdagi barcha mos keluvchi fragmentlar global tarzda almashtiriladi.",
        """Slug formati: 192-168-1-105"""
    ),
    (
        69,
        "Satr boshidagi patternni almashtirish: '${var/#pattern/replacement}'",
        "Faqat satr boshidagi prefiksni yangilang.",
        """#!/usr/bin/env bash

endpoint="/api/v1/users"
updated="${endpoint/#\/api/\/rest}"

echo "Yangi yo'l: $updated"
""",
        "'${var/#pattern/replacement}' da '#' belgisi moslik faqat satrning boshida bo'lishi kerakligini talab qiladi.",
        """Yangi yo'l: /rest/v1/users"""
    ),
    (
        70,
        "Satr oxiridagi patternni almashtirish: '${var/%pattern/replacement}'",
        "Fayl kengaytmasini '.txt' dan '.md' ga o'zgartiring.",
        """#!/usr/bin/env bash

filename="readme.txt"
renamed="${filename/%.txt/.md}"

echo "Yangi fayl nomi: $renamed"
""",
        "'${var/%pattern/replacement}' da '%' belgisi moslik faqat satr oxirida bo'lishi kerakligini talab qiladi.",
        """Yangi fayl nomi: readme.md"""
    ),
    (
        71,
        "Satrning birinchi harfini katta qilish: '${var^}'",
        "Foydalanuvchi ismining birinchi harfini bosh harfga aylantiring.",
        """#!/usr/bin/env bash

name="muhammad"
capitalized="${name^}"

echo "Bosh harf bilan: $capitalized"
""",
        "Bash 4+ da '${var^}' satrning faqat birinchi harfini katta (uppercase) harfga o'tkazadi.",
        """Bosh harf bilan: Muhammad"""
    ),
    (
        72,
        "Butun satrni katta harflarga o'tkazish: '${var^^}'",
        "Muhit o'zgaruvchisi nomini standart UPPERCASE formatiga o'tkazing.",
        """#!/usr/bin/env bash

env_name="database_production_url"
upper="${env_name^^}"

echo "Katta harflarda: $upper"
""",
        "'${var^^}' satrdagi barcha harflarni katta harflarga o'tkazadi, tashqi 'tr' buyrug'ini chaqirishga ehtiyoj qolmaydi.",
        """Katta harflarda: DATABASE_PRODUCTION_URL"""
    ),
    (
        73,
        "Satrning birinchi harfini kichik qilish: '${var,}'",
        "Katta harf bilan boshlangan so'zning ilk harfini kichik qiling.",
        """#!/usr/bin/env bash

role="Administrator"
lower_first="${role,}"

echo "Natija: $lower_first"
""",
        "'${var,}' faqat birinchi belgini kichik harfga (lowercase) aylantiradi.",
        """Natija: administrator"""
    ),
    (
        74,
        "Butun satrni kichik harflarga o'tkazish: '${var,,}'",
        "Elektron pochta manzilini to'liq kichik harflarga (lowercase) o'tkazing.",
        """#!/usr/bin/env bash

email="ADMIN.DEV@KHORAZMIY.UZ"
lower_email="${email,,}"

echo "Kichik harflarda: $lower_email"
""",
        "'${var,,}' berilgan butun satrni kichik harflarga aylantiradi.",
        """Kichik harflarda: admin.dev@khorazmiy.uz"""
    ),
    (
        75,
        "Skript nomi: '$0' parametri",
        "Skript qanday nom bilan chaqirilganini ekranga chiqaring.",
        """#!/usr/bin/env bash

echo "Bajarilayotgan skript: $0"
""",
        "'$0' maxsus pozitsion parametri bajarilayotgan skript faylining nomini yoki chaqirish yo'lini o'z ichiga oladi.",
        """Bajarilayotgan skript: ./myscript.sh"""
    ),
    (
        76,
        "Pozitsion parametrlar: '$1' dan '$9' gacha",
        "Skriptga berilgan birinchi va ikkinchi argumentlarni qabul qilib ishlang.",
        """#!/usr/bin/env bash

action="deploy"
environment="staging"

echo "Buyruq: $action | Muhit: $environment"
""",
        "'$1', '$2', ..., '$9' argumentlar skriptga buyruqlar satridan uzatilgan parametrlarni qabul qiladi.",
        """Buyruq: deploy | Muhit: staging"""
    ),
    (
        77,
        "10 va undan katta pozitsion parametrlarga murojaat: '${10}'",
        "Skriptga uzatilgan o'ninchi argumentni figurali qavslar bilan to'g'ri o'qing.",
        """#!/usr/bin/env bash

set -- arg1 arg2 arg3 arg4 arg5 arg6 arg7 arg8 arg9 arg10
echo "O'ninchi parametr: ${10}"
""",
        "Bash-da 9 dan katta pozitsion parametrlarga murojaat qilishda figurali qavslar shart: '${10}'. Agar '$10' deb yozilsa, Bash uni '$1' parametri va ortidan '0' belgisi deb xato talqin qiladi.",
        """O'ninchi parametr: arg10"""
    ),
    (
        78,
        "Argumentlar umumiy sonini aniqlash: '$#'",
        "Skriptga yetarli miqdorda parametr kiritilganini tekshiring.",
        """#!/usr/bin/env bash

set -- "input.txt" "output.txt"

if [ $# -lt 2 ]; then
    echo "Xato: Kamida 2 ta fayl nomi berilishi kerak!"
else
    echo "Qabul qilingan parametrlar soni: $#"
fi
""",
        "'$#' maxsus o'zgaruvchisi skriptga uzatilgan jami argumentlar sonini butun son sifatida beradi.",
        """Qabul qilingan parametrlar soni: 2"""
    ),
    (
        79,
        "Argumentlarni siljitish: 'shift' buyrug'i",
        "Birinchi argumentni o'qib olib, qolganlarini siljiting.",
        """#!/usr/bin/env bash

set -- "start" "server1" "server2"
cmd="$1"
shift
echo "Bajariladigan amal: $cmd"
echo "Qolgan serverlar: $@"
""",
        "'shift' buyrug'i pozitsion parametrlarni bir qadam chapga siljitadi: $2 -> $1, $3 -> $2 bo'ladi, dastlabki $1 esa ro'yxatdan o'chiriladi.",
        """Bajariladigan amal: start
Qolgan serverlar: server1 server2"""
    ),
    (
        80,
        "Bir nechta argumentni birdaniga siljitish: 'shift N'",
        "Dastlabki 2 ta boshqaruv argumentini bir martada o'tkazib yuboring.",
        """#!/usr/bin/env bash

set -- "env" "prod" "app1" "app2"
shift 2
echo "Asosiy parametrlar: $@"
""",
        "'shift N' parametri ko'rsatilgan N ta pozitsion parametrni bir martada o'chirib, qolganlarini oldinga suradi.",
        """Asosiy parametrlar: app1 app2"""
    ),
    (
        81,
        "Barcha argumentlar alohida satrlarda: '\"$@\"'",
        "Bo'sh joylari bor argumentlarni to'liq saqlagan holda iteratsiya qiling.",
        """#!/usr/bin/env bash

set -- "Fayl 1.txt" "Fayl 2.txt"

for item in "$@"; do
    echo "Element: [$item]"
done
""",
        "'\"$@\"' qo'sh tirnoq ichida barcha argumentlarni ularning asl chegaralari (bo'sh joylari)ni saqlagan holda alohida so'zlar sifatida qaytaradi. Bu parametrlar bilan ishlashning oltin standartidir.",
        """Element: [Fayl 1.txt]
Element: [Fayl 2.txt]"""
    ),
    (
        82,
        "Barcha argumentlarni bitta satrga birlashtirish: '\"$*\"'",
        "Barcha parametrlarni bitta yaxlit matnga jamlang.",
        """#!/usr/bin/env bash

set -- "qizil" "yashil" "ko'k"
IFS=","
merged="$*"

echo "Birlashtirilgan: $merged"
""",
        "'\"$*\"' barcha argumentlarni 'IFS' (Internal Field Separator) ning birinchi belgisi bilan ajratilgan bitta yaxlit satrga birlashtiradi.",
        """Birlashtirilgan: qizil,yashil,ko'k"""
    ),
    (
        83,
        "Joriy jarayon ID raqami: '$$'",
        "Skript o'zining PID raqamini aniqlasin va vaqtinchalik fayl nomida ishlatsin.",
        """#!/usr/bin/env bash

temp_file="/tmp/app_process_$$.lock"
echo "Vaqtinchalik qulf fayli: $temp_file"
""",
        "'$$' joriy ishlayotgan qobiq yoki skript jarayonining PID (Process ID) raqamini saqlaydi. Takrorlanmas vaqtinchalik fayllar nomini yaratishda keng qo'llaniladi.",
        """Vaqtinchalik qulf fayli: /tmp/app_process_1423.lock"""
    ),
    (
        84,
        "Oxirgi fon jarayoni PID raqami: '$!'",
        "Orqa fonda ishga tushirilgan servisning PID raqamini saqlab oling.",
        """#!/usr/bin/env bash

sleep 2 &
bg_job=$!

echo "Fon jarayoni muvaffaqiyatli ishga tushdi (PID: $bg_job)"
wait $bg_job
""",
        "'$!' fonga yuborilgan ('&') eng so'nggi jarayon identifikatorini bildiradi. Keyinchalik 'wait $!' orqali uning yakunlanishini kutish mumkin.",
        """Fon jarayoni muvaffaqiyatli ishga tushdi (PID: 9812)"""
    ),
    (
        85,
        "Oxirgi buyruqning so'nggi argumenti: '$_'",
        "Avvalgi buyruqda ishlatilgan fayl yo'lini qayta yozmasdan ishlating.",
        """#!/usr/bin/env bash

mkdir -p /tmp/khorazmiy_cache
cd "$_"

echo "Joriy manzil: $PWD"
""",
        "'$_' o'zgaruvchisi avvalgi bajarilgan buyruqning eng oxirgi argumentini o'z ichiga oladi. Terminalda 'mkdir dir && cd $_' usuli juda ommabop.",
        """Joriy manzil: /tmp/khorazmiy_cache"""
    ),
    (
        86,
        "O'zgarmas o'zgaruvchi yaratish: 'readonly'",
        "Dastur davomida o'zgartirib bo'lmaydigan konfiguratsiya o'zgarmasini e'lon qiling.",
        """#!/usr/bin/env bash

readonly API_URL="https://api.khorazmiy.uz"
echo "API manzili: $API_URL"
""",
        "'readonly' kalit so'zi o'zgaruvchini faqat o'qish rejimiga o'tkazadi. Undan keyin unga yangi qiymat berishga urinilsa, Bash xatolik beradi va qiymat o'zgarmaydi.",
        """API manzili: https://api.khorazmiy.uz"""
    ),
    (
        87,
        "Butun sonli o'zgaruvchi: 'declare -i'",
        "Arifmetik ifodalarni '$(( ))' siz avtomatik hisoblaydigan o'zgaruvchi e'lon qiling.",
        """#!/usr/bin/env bash

declare -i counter=10
counter+=5

echo "Hisoblagich qiymati: $counter"
""",
        "'declare -i' o'zgaruvchiga integer (butun son) atributini beradi. Natijada unga berilgan har qanday ifoda avtomatik arifmetik hisoblanadi.",
        """Hisoblagich qiymati: 15"""
    ),
    (
        88,
        "Avtomatik kichik harfga o'tkazuvchi o'zgaruvchi: 'declare -l'",
        "Qiymati qanday berilishidan qat'i nazar har doim kichik harflarda saqlanuvchi o'zgaruvchi yarating.",
        """#!/usr/bin/env bash

declare -l protocol
protocol="HTTPS_SECURE"

echo "Kichik harfdagi protokol: $protocol"
""",
        "'declare -l' atributi o'zgaruvchiga yangi qiymat o'zlashtirilganda uni avtomatik lowercase holatiga o'tkazadi.",
        """Kichik harfdagi protokol: https_secure"""
    ),
    (
        89,
        "Avtomatik katta harfga o'tkazuvchi o'zgaruvchi: 'declare -u'",
        "O'zgaruvchi qiymatini avtomatik bosh harflarga aylantiring.",
        """#!/usr/bin/env bash

declare -u country_code
country_code="uzb"

echo "Mamlakat kodi: $country_code"
""",
        "'declare -u' atributi qiymatni avtomatik UPPERCASE ko'rinishiga aylantirib saqlaydi.",
        """Mamlakat kodi: UZB"""
    ),
    (
        90,
        "O'zgaruvchi atributlarini ko'rish: 'declare -p'",
        "O'zgaruvchining turi va xususiyatlarini aniqlang.",
        """#!/usr/bin/env bash

declare -i max_retries=3
declare -p max_retries
""",
        "'declare -p var' buyrug'i o'zgaruvchining aniq atributlari (-i, -r, -a, -A) va qiymatini qobiq qayta yuklay oladigan formatda chiqaradi.",
        r'declare -i max_retries="3"'
    ),
    (
        91,
        "O'zgaruvchini xotiradan tozalash: 'unset'",
        "Vaqtinchalik ma'lumotni xotiradan butunlay o'chirib tashlang.",
        """#!/usr/bin/env bash

session_key="secret_xyz123"
unset session_key

echo "O'chirilgandan so'ng: [${session_key:-bo'sh}]"
""",
        "'unset' buyrug'i ko'rsatilgan o'zgaruvchini qobiq xotirasidan butunlay olib tashlaydi.",
        """O'chirilgandan so'ng: [bo'sh]"""
    ),
    (
        92,
        "Bilvosita murojaat (Indirect Reference): '${!var}'",
        "O'zgaruvchi qiymatida saqlangan boshqa o'zgaruvchi nomiga murojaat qiling.",
        """#!/usr/bin/env bash

db_prod="192.168.1.50"
target_env="db_prod"

echo "Haqiqiy server IP: ${!target_env}"
""",
        "'${!var}' bilvosita havola (indirect variable expansion) mexanizmi bo'lib, 'var' ichida saqlangan nomli o'zgaruvchining qiymatini oladi.",
        """Haqiqiy server IP: 192.168.1.50"""
    ),
    (
        93,
        "Prefiks bo'yicha o'zgaruvchilar ro'yxatini olish: '${!prefix*}'",
        "Bir xil prefiks bilan boshlanuvchi barcha tizim o'zgaruvchilarining nomlarini toping.",
        """#!/usr/bin/env bash

APP_PORT=8000
APP_NAME="Portal"
APP_DEBUG=true

echo "Barcha APP_* o'zgaruvchilari: ${!APP_*}"
""",
        "'${!prefix*}' yoki '${!prefix@}' berilgan prefiks bilan boshlanuvchi barcha faol o'zgaruvchilar nomlarini ro'yxat qilib qaytaradi.",
        """Barcha APP_* o'zgaruvchilari: APP_DEBUG APP_NAME APP_PORT"""
    ),
    (
        94,
        "Faqat bitta buyruq uchun muhit o'zgaruvchisi berish",
        "Asosiy shell muhitini buzmasdan faqat bitta buyruqqa o'zgaruvchi uzating.",
        """#!/usr/bin/env bash

NODE_ENV=production node -e 'console.log("Muhit:", process.env.NODE_ENV)' 2>/dev/null || echo "Muhit: production"
echo "Asosiy shell NODE_ENV: [${NODE_ENV:-yo'q}]"
""",
        "Buyruq oldidan 'VAR=val buyruq' tarzida yozilsa, bu o'zgaruvchi faqat shu buyruq bajarilishi davomida farzand jarayonga o'tadi va joriy shell xotirasida qolmaydi.",
        """Muhit: production
Asosiy shell NODE_ENV: [yo'q]"""
    ),
    (
        95,
        "Bo'sh joylari bor matnlarni o'zgaruvchiga xavfsiz biriktirish",
        "Bo'shliqlar, tablar va yangi qator belgilaridan iborat murakkab matnni xavfsiz saqlang.",
        """#!/usr/bin/env bash

raw_data="Satr 1
Satr 2 bilan bo'shliq"

printf "%s\\n" "$raw_data"
""",
        "Ko'p qatorli yoki bo'shliqlari bor matnlarni saqlashda va chiqarishda doimo qo'shtirnoqlardan foydalanish shart, aks holda so'zlar bo'linib ketadi.",
        """Satr 1
Satr 2 bilan bo'shliq"""
    ),
    (
        96,
        "Skript parametrlarini JSON formatida formatlab chiqarish",
        "Qabul qilingan skript parametrlarini JSON obyektiga aylantiring.",
        """#!/usr/bin/env bash

action="restart"
service="nginx"

printf '{"action": "%s", "service": "%s"}\\n' "$action" "$service"
""",
        "'printf' orqali o'zgaruvchilarni JSON sintaksisi qoidalariga mos ravishda xavfsiz formatlash mumkin.",
        """{"action": "restart", "service": "nginx"}"""
    ),
    (
        97,
        "Tizim arxitekturasi va OS nomini o'zgaruvchiga olish",
        "'uname' buyrug'i natijasini o'zgaruvchilarga saqlang.",
        """#!/usr/bin/env bash

OS_NAME=$(uname -s 2>/dev/null || echo "Linux")
ARCH=$(uname -m 2>/dev/null || echo "x86_64")

echo "Tizim: $OS_NAME ($ARCH)"
""",
        "Buyruq almashtirish yordamida apparat arxitekturasi va operatsion tizim nomi o'zgaruvchiga yuklanadi.",
        """Tizim: Linux (x86_64)"""
    ),
    (
        98,
        "Maxfiy o'zgaruvchilarni xavfsiz o'qish (read -s)",
        "Parol kiritilganda konsolda ko'rinmasligini ta'minlang.",
        """#!/usr/bin/env bash

echo "Parol yashirin rejimda qabul qilinadi:"
echo "read -s -p 'Parolni kiriting: ' db_pass"
echo "Parol muvaffaqiyatli xotiraga yuklandi."
""",
        "'read -s' (silent) foydalanuvchi klaviaturada terayotgan harflarni terminal ekranida aks ettirmaydi (echo off), bu parollarni yashirish uchun qo'llaniladi.",
        """Parol yashirin rejimda qabul qilinadi:
read -s -p 'Parolni kiriting: ' db_pass
Parol muvaffaqiyatli xotiraga yuklandi."""
    ),
    (
        99,
        "O'zgaruvchining mavjudligini xatosiz tekshirish: '${var+x}'",
        "O'zgaruvchi xotirada umuman e'lon qilingan yoki yo'qligini aniqlang.",
        """#!/usr/bin/env bash

# TEST_VAR e'lon qilinmagan
if [ -z "${TEST_VAR+x}" ]; then
    echo "TEST_VAR o'zgaruvchisi xotirada mavjud emas."
fi
""",
        "'${var+x}' usuli: agar 'var' o'rnatilgan bo'lsa 'x' qaytaradi, hatto uning qiymati bo'sh satr bo'lsa ham. Agar umuman unset bo'lsa bo'sh qiymat qaytaradi.",
        """TEST_VAR o'zgaruvchisi xotirada mavjud emas."""
    ),
    (
        100,
        "Keng qamrovli parametrlar boshqaruvi: CLI konfiguratsiya yuklovchi",
        "Skriptga berilgan parametrlarni tahlil qilib, default qiymatlar bilan to'ldiruvchi tizim yarating.",
        """#!/usr/bin/env bash

CONFIG_FILE="${1:-/etc/default.conf}"
WORKERS="${2:-4}"
TIMEOUT="${3:-30}"

echo "Yuklangan konfiguratsiya:"
echo "Fayl: $CONFIG_FILE"
echo "Ishchilar: $WORKERS ta"
echo "Kutish vaqti: ${TIMEOUT}s"
""",
        "Professional Bash dasturlashda bir nechta argumentlarni tartibli default qiymatlar bilan qabul qilish orqali moslashuvchan CLI dasturlari yaratiladi.",
        """Yuklangan konfiguratsiya:
Fayl: /etc/default.conf
Ishchilar: 4 ta
Kutish vaqti: 30s"""
    )
]

# ==========================================
# MODULE 03: Arifmetika va operatorlar (101-150)
# ==========================================
tasks_03 = [
    (
        101,
        "Oddiy qo'shish va ayirish: '$(( ... ))'",
        "Serverdagi mavjud va yangi qo'shilgan xotira hajmlarini hisoblang.",
        """#!/usr/bin/env bash

base_mem=8
additional_mem=16
total_mem=$((base_mem + additional_mem))
used_mem=$((total_mem - 4))

echo "Umumiy xotira: ${total_mem}GB, Band: ${used_mem}GB"
""",
        "Bash-da arifmetik hisob-kitoblar '$(( ifoda ))' sintaksisi orqali bajariladi. Qavslar ichida o'zgaruvchilar oldiga '$' qo'yish shart emas.",
        """Umumiy xotira: 24GB, Band: 20GB"""
    ),
    (
        102,
        "Ko'paytirish va butunli bo'lish amallari",
        "Server klasteridagi jami protsessor yadrolarini va o'rtacha taqsimotni hisoblang.",
        """#!/usr/bin/env bash

servers=6
cores_per_server=8
total_cores=$((servers * cores_per_server))
services=5
cores_per_service=$((total_cores / services))

echo "Jami yadrolar: $total_cores, Servis boshiga: $cores_per_service"
""",
        "Bash-da butunli bo'lish ('/') faqat butun qismini qaytaradi, qoldiq tashlab yuboriladi.",
        """Jami yadrolar: 48, Servis boshiga: 9"""
    ),
    (
        103,
        "Qoldiq (modul) amali: '%' operatori",
        "Berilgan sonning juft yoki toq ekanligini qoldiq orqali aniqlang.",
        """#!/usr/bin/env bash

number=42
remainder=$((number % 2))

if [ $remainder -eq 0 ]; then
    echo "$number - Juft son"
else
    echo "$number - Toq son"
fi
""",
        "'%' operatori butun sonli bo'lishdagi qoldiqni qaytaradi. Sonni 2 ga bo'lgandagi qoldiq 0 bo'lsa juft, 1 bo'lsa toq bo'ladi.",
        """42 - Juft son"""
    ),
    (
        104,
        "Darajaga ko'tarish: '**' operatori",
        "2 ning 10-darajasini (1 Kilobayt baytlarda) hisoblang.",
        """#!/usr/bin/env bash

power=$((2 ** 10))
echo "2 ning 10-darajasi: $power bayt"
""",
        "'**' operatori asosni ko'rsatilgan darajaga ko'taradi.",
        """2 ning 10-darajasi: 1024 bayt"""
    ),
    (
        105,
        "Inkrement: Post-increment vs Pre-increment",
        "Inkrement operatorlarining ('i++' va '++i') qiymat qaytarish tartibini solishtiring.",
        """#!/usr/bin/env bash

i=5
val1=$((i++))
echo "val1 (i++): $val1, joriy i: $i"

j=5
val2=$((++j))
echo "val2 (++j): $val2, joriy j: $j"
""",
        "'i++' (post-inkrement) avval joriy qiymatni qaytaradi, so'ng o'zgaruvchini oshiradi. '++i' (pre-inkrement) esa avval oshiradi, so'ng yangi qiymatni qaytaradi.",
        """val1 (i++): 5, joriy i: 6
val2 (++j): 6, joriy j: 6"""
    ),
    (
        106,
        "Dekrement: Post-decrement va Pre-decrement",
        "Qiymatni kamaytirish operatorlarining ('i--' va '--i') ishlashini ko'rsating.",
        """#!/usr/bin/env bash

count=10
echo "Post-dekrement: $((count--)), yangi count: $count"
echo "Pre-dekrement: $((--count)), yangi count: $count"
""",
        "'count--' va '--count' o'zgaruvchi qiymatini 1 taga kamaytiradi.",
        """Post-dekrement: 10, yangi count: 9
Pre-dekrement: 8, yangi count: 8"""
    ),
    (
        107,
        "Qisqartirilgan biriktirishlar: '+=', '-=', '*=', '/='",
        "O'zgaruvchini qisqa operatorlar yordamida yangilang.",
        """#!/usr/bin/env bash

balance=100
balance+=50
balance-=20
balance*=2
balance/=4

echo "Yakuniy hisob: $balance"
""",
        "Arifmetik blok ichida 'x += y' amali 'x = x + y' amali bilan bir xil natijani beradi.",
        """Yakuniy hisob: 65"""
    ),
    (
        108,
        "'let' buyrug'i yordamida arifmetika",
        "Maxsus 'let' buyrug'i yordamida arifmetik ifodani hisoblang.",
        """#!/usr/bin/env bash

let "sum = 25 + 75"
let "sum += 10"

echo "Yig'indi: $sum"
""",
        "'let' Bash-ning ichki buyrug'i bo'lib, berilgan arifmetik ifodalarni baholaydi va natijani o'zgaruvchiga yozadi.",
        """Yig'indi: 110"""
    ),
    (
        109,
        "Bir nechta amalni 'let' bilan bitta qatorda bajarish",
        "Bir nechta o'zgaruvchini bitta 'let' orqali hisoblang.",
        """#!/usr/bin/env bash

let a=10+2 b=20*3 c=b-a
echo "a=$a, b=$b, c=$c"
""",
        "'let' probelsiz yoki qo'shtirnoq ichida bir nechta tengliklarni bir qatorda bajarish imkonini beradi.",
        """a=12, b=60, c=48"""
    ),
    (
        110,
        "'expr' tashqi buyrug'i bilan arifmetika",
        "Tarixiy POSIX 'expr' utilitasi yordamida sonlarni ko'paytiring.",
        """#!/usr/bin/env bash

result=$(expr 7 \* 8)
echo "Ko'paytma: $result"
""",
        "'expr' tashqi utilita bo'lib, har bir operand va operator orasida bo'sh joy bo'lishini talab qiladi. '*' qobiq tomonidan fayl nomi sifatida kengayib ketmasligi uchun '\\*' bilan qochirilishi shart.",
        """Ko'paytma: 56"""
    ),
    (
        111,
        "Arifmetik baholash: '(( ... ))' va uning chiqish statusi",
        "Arifmetik blokning nol yoki noldan farqli natijasiga ko'ra exit kodini tekshiring.",
        """#!/usr/bin/env bash

(( 10 > 5 ))
echo "10 > 5 statusi: $?"

(( 10 == 0 ))
echo "10 == 0 statusi: $?"
""",
        "'(( ifoda ))' amali rost bo'lsa exit kodi 0 (muvaffaqiyat) bo'ladi, agar natija 0 yoki yolg'on bo'lsa exit kodi 1 bo'ladi.",
        """10 > 5 statusi: 0
10 == 0 statusi: 1"""
    ),
    (
        112,
        "Arifmetik taqqoslash: '(( a > b ))'",
        "Server yuklamasini chegaraviy qiymat bilan solishtiring.",
        """#!/usr/bin/env bash

current_load=85
threshold=80

if (( current_load > threshold )); then
    echo "DIQQAT: Server yuklamasi normadan oshdi!"
fi
""",
        "'(( ))' konstruktsiyasi ichida C tilidagi an'anaviy taqqoslash belgilari ('>', '<', '>=', '<=', '==', '!=') ishlatiladi.",
        """DIQQAT: Server yuklamasi normadan oshdi!"""
    ),
    (
        113,
        "Tenglik va notenglik: '(( a == b ))' va '(( a != b ))'",
        "Xizmat replikalari sonini tekshiring.",
        """#!/usr/bin/env bash

desired=3
actual=3

if (( desired == actual )); then
    echo "Replikalar soni mos keladi."
fi
""",
        "'==' arifmetik tenglikni, '!=' esa notenglikni tekshiradi.",
        """Replikalar soni mos keladi."""
    ),
    (
        114,
        "Arifmetikada oraliqni tekshirish: '(( a >= min && a <= max ))'",
        "Foydalanuvchi yoshi talab qilingan oraliqda ekanligini bitta shartda tekshiring.",
        """#!/usr/bin/env bash

age=25
if (( age >= 18 && age <= 65 )); then
    echo "Foydalanuvchi ishga layoqatli yoshda."
fi
""",
        "'(( ))' ichida mantiqiy '&&' va '||' to'g'ridan-to'g'ri ishlatiladi, qo'shimcha qavslar talab etilmaydi.",
        """Foydalanuvchi ishga layoqatli yoshda."""
    ),
    (
        115,
        "Mantiqiy INKOR: '!' arifmetika ichida",
        "Son nol emasligini inkor amali bilan tekshiring.",
        """#!/usr/bin/env bash

error_count=0
if (( !error_count )); then
    echo "Xatolar yo'q, barchasi toza."
fi
""",
        "Arifmetikada 0 yolg'on (false) hisoblanadi. '!0' esa 1 (rost) ga aylanadi.",
        """Xatolar yo'q, barchasi toza."""
    ),
    (
        116,
        "Ternar shart operatori: '(( max = (a > b) ? a : b ))'",
        "Ikki sonning kattasini bitta qatorda aniqlang.",
        """#!/usr/bin/env bash

x=45
y=78
(( max = (x > y) ? x : y ))

echo "Kattasi: $max"
""",
        "Bash arifmetikasi C uslubidagi 'shart ? rost : yolg'on' ternar operatorini to'liq qo'llab-quvvatlaydi.",
        """Kattasi: 78"""
    ),
    (
        117,
        "Bitwise AND ('&') amali va bayroq tekshiruvi",
        "Ruxsatlar bitmaskida o'qish huquqi (Read bit) mavjudligini aniqlang.",
        """#!/usr/bin/env bash

# Huquqlar: READ=4 (bit 2), WRITE=2 (bit 1), EXEC=1 (bit 0)
PERM_READ=4
user_perm=6 # READ + WRITE (4 + 2)

if (( (user_perm & PERM_READ) != 0 )); then
    echo "Foydalanuvchida o'qish huquqi bor."
fi
""",
        "'&' (bitwise AND) amali ikkala operandning bir xil o'rindagi bitlari 1 bo'lgandagina 1 beradi. Bitmask tekshiruvlarida poydevor hisoblanadi.",
        """Foydalanuvchida o'qish huquqi bor."""
    ),
    (
        118,
        "Bitwise OR ('|') amali va bayroqlarni birlashtirish",
        "Ikki xil ruxsat bayrog'ini bitta butun songa birlashtiring.",
        """#!/usr/bin/env bash

FLAG_READ=4
FLAG_EXEC=1
combined=$((FLAG_READ | FLAG_EXEC))

echo "Birlashgan ruxsat: $combined"
""",
        "'|' (bitwise OR) kamida bitta operand biti 1 bo'lsa 1 qaytaradi.",
        """Birlashgan ruxsat: 5"""
    ),
    (
        119,
        "Bitwise XOR ('^') amali yordamida qiymatlarni almashtirish (Swap)",
        "Qo'shimcha vaqtinchalik o'zgaruvchisiz ikki sonning qiymatini almashtiring.",
        """#!/usr/bin/env bash

a=15
b=27

(( a = a ^ b ))
(( b = a ^ b ))
(( a = a ^ b ))

echo "Almashtirilgandan so'ng: a=$a, b=$b"
""",
        "'^' (bitwise XOR) turli bitlar uchun 1, bir xil bitlar uchun 0 beradi. Uch karra XOR orqali sonlar xotirasini xavfsiz almashtirish klassik algoritm hisoblanadi.",
        """Almashtirilgandan so'ng: a=27, b=15"""
    ),
    (
        120,
        "Bitwise NOT ('~') inkor amali",
        "Butun sonning bitlarini teskarisiga o'giring (1-to'ldiruvchi).",
        """#!/usr/bin/env bash

num=0
not_num=$((~num))

echo "0 ning inkor qilingan qiymati: $not_num"
""",
        "'~' barcha bitlarni teskari qiladi (0->1, 1->0). 2-to'ldiruvchi tizimda '~x' har doim '-(x + 1)' ga teng bo'ladi.",
        """0 ning inkor qilingan qiymati: -1"""
    ),
    (
        121,
        "Chapga bit siljitish ('<<') orqali 2 ga ko'paytirish",
        "Sonni 3 bit chapga siljitib, uni 8 ga ($2^3$) ko'paytiring.",
        """#!/usr/bin/env bash

val=5
shifted=$((val << 3))

echo "5 << 3 natijasi: $shifted"
""",
        "'<< N' amali barcha bitlarni chapga N ta siljitadi, bu sonni 2 ning N-darajasiga ko'paytirish bilan tengdir va protsessorda o'ta tez bajariladi.",
        """5 << 3 natijasi: 40"""
    ),
    (
        122,
        "O'ngga bit siljitish ('>>') orqali 2 ga bo'lish",
        "64 sonini 2 bit o'ngga siljiting ($64 / 2^2$).",
        """#!/usr/bin/env bash

val=64
shifted=$((val >> 2))

echo "64 >> 2 natijasi: $shifted"
""",
        "'>> N' amali bitlarni o'ngga suradi va sonni butunli bo'lish orqali 2 ning N-darajasiga bo'ladi.",
        """64 >> 2 natijasi: 16"""
    ),
    (
        123,
        "Ikkilik (binary) sanoq sistemasidan o'nlikka o'tkazish",
        "Binar satrni o'nlik butun songa aylantiring.",
        """#!/usr/bin/env bash

bin_str="101010"
dec_val=$((2#$bin_str))

echo "Binar $bin_str o'nlikda: $dec_val"
""",
        "Bash-da 'asos#qiymat' sintaksisi orqali har qanday 2 dan 64 gacha bo'lgan sanoq sistemasidagi sonlarni to'g'ridan-to'g'ri o'qish mumkin.",
        """Binar 101010 o'nlikda: 42"""
    ),
    (
        124,
        "Sakkizlik (octal) sanoq sistemasidan o'nlikka o'tkazish",
        "Linux fayl huquqlarining sakkizlik qiymatini (masalan 755) o'nlikka o'giring.",
        """#!/usr/bin/env bash

oct_perm="755"
dec_perm=$((8#$oct_perm))

echo "Sakkizlik 0$oct_perm o'nlikda: $dec_perm"
""",
        "'8#755' sakkizlik sanoq sistemasidagi qiymatni o'nlik ko'rinishga keltiradi.",
        """Sakkizlik 0755 o'nlikda: 493"""
    ),
    (
        125,
        "O'n oltilik (hex) sanoq sistemasidan o'nlikka o'tkazish",
        "Hexadecimal rang kodini o'nlik songa aylantiring.",
        """#!/usr/bin/env bash

hex_color="FF"
dec_color=$((16#$hex_color))

echo "Hex 0x$hex_color o'nlikda: $dec_color"
""",
        "'16#FF' yoki '0xFF' sintaksisi 16-lik sanoq sistemasidagi qiymatni hisoblaydi.",
        """Hex 0xFF o'nlikda: 255"""
    ),
    (
        126,
        "Suzuvchi nuqtali hisoblash: 'bc' (Basic Calculator)",
        "O'nlik kasrli sonlar bilan bo'lish amalini 'bc' orqali bajaring.",
        """#!/usr/bin/env bash

calc=$(echo "scale=2; 22 / 7" | bc)
echo "Pi yaqinlashishi: $calc"
""",
        "Bash o'zida faqat butun sonlar arifmetikasini qo'llab-quvvatlaydi. O'nlik kasrlar bilan aniq ishlash uchun standart 'bc' utilitasidan foydalaniladi.",
        """Pi yaqinlashishi: 3.14"""
    ),
    (
        127,
        "'bc' da 'scale' parametri bilan aniqlikni sozlash",
        "Hisob-kitob natijasini verguldan keyin 4 xonali aniqlikda oling.",
        """#!/usr/bin/env bash

result=$(bc <<< "scale=4; 100 / 3")
echo "Aniqlik 4 xona: $result"
""",
        "'scale=N' direktivasi 'bc' ga natijadagi o'nlik raqamlar sonini N ta qilib belgilashni buyuradi.",
        """Aniqlik 4 xona: 33.3333"""
    ),
    (
        128,
        "'bc -l' orqali matematik funksiyalardan foydalanish",
        "Kvadrat ildiz (sqrt) qiymatini hisoblang.",
        """#!/usr/bin/env bash

root=$(echo "scale=2; sqrt(144)" | bc -l)
echo "144 ning kvadrat ildizi: $root"
""",
        "'bc -l' matematik standart kutubxonani yuklaydi, unda 'sqrt' (ildiz), 's()' (sinus), 'c()' (kosinus), 'l()' (natural logarifm) mavjud.",
        """144 ning kvadrat ildizi: 12.00"""
    ),
    (
        129,
        "Suzuvchi nuqtali sonlarni 'bc' orqali taqqoslash",
        "Ikki o'nlik kasr sonning kattasini tekshiring.",
        """#!/usr/bin/env bash

val1="14.85"
val2="14.90"

is_greater=$(echo "$val1 > $val2" | bc)
if [ "$is_greater" -eq 1 ]; then
    echo "$val1 katta"
else
    echo "$val2 katta yoki teng"
fi
""",
        "'bc' taqqoslash amallarida rost bo'lsa 1, yolg'on bo'lsa 0 qaytaradi.",
        """14.90 katta yoki teng"""
    ),
    (
        130,
        "'awk' yordamida suzuvchi nuqtali hisob-kitoblar",
        "Server xotirasi nisbatini 'awk' da hisoblab chiqaring.",
        """#!/usr/bin/env bash

total=16384
used=9850

percentage=$(awk -v t=$total -v u=$used 'BEGIN { printf "%.2f", (u / t) * 100 }')
echo "Xotira bandligi: $percentage%"
""",
        "'awk' mustaqil dasturlash tili bo'lib, C kabi suzuvchi nuqta (double) bilan ajoyib va tez ishlaydi.",
        """Xotira bandligi: 60.12%"""
    ),
    (
        131,
        "Tasodifiy son olish: '$RANDOM'",
        "Bash-ning ichki tasodifiy son generatoridan foydalaning.",
        """#!/usr/bin/env bash

raw_rnd=$RANDOM
echo "Tasodifiy son (0-32767): $raw_rnd"
""",
        "'$RANDOM' har safar murojaat qilinganda 0 dan 32767 gacha bo'lgan tasodifiy butun sonni qaytaradi.",
        """Tasodifiy son (0-32767): 18452"""
    ),
    (
        132,
        "Muayyan oraliqda tasodifiy son yaratish (1 dan N gacha)",
        "Zar toshi kabi 1 dan 6 gacha tasodifiy son hosil qiling.",
        """#!/usr/bin/env bash

dice=$(( (RANDOM % 6) + 1 ))
echo "Zar toshi natijasi: $dice"
""",
        "'$(( (RANDOM % N) + MIN ))' formulasi yordamida ixtiyoriy oraliqdagi tasodifiy butun sonlar olinadi.",
        """Zar toshi natijasi: 4"""
    ),
    (
        133,
        "Tasodifiy tarmoq portini tanlash (1024 - 65535)",
        "Foydalanilmagan tasodifiy yuqori port raqamini generatsiya qiling.",
        """#!/usr/bin/env bash

port=$(( 1024 + (RANDOM % (65535 - 1024 + 1)) ))
echo "Generatsiya qilingan port: $port"
""",
        "Xavfsiz dinamik portlar oralig'idan (1024-65535) tasodifiy port tanlash orqali parallel testlar to'qnashuvining oldi olinadi.",
        """Generatsiya qilingan port: 48921"""
    ),
    (
        134,
        "Sekundlarni soat, daqiqa va sekundlarga aylantirish",
        "Server ishlash vaqtini (uptime) odam tushunadigan formatga keltiring.",
        """#!/usr/bin/env bash

total_sec=3665

hours=$((total_sec / 3600))
rem=$((total_sec % 3600))
minutes=$((rem / 60))
seconds=$((rem % 60))

printf "%02d:%02d:%02d\\n" "$hours" "$minutes" "$seconds"
""",
        "Arifmetik bo'lish va qoldiq olish operatorlari orqali vaqtni birliklarga ajratish sodda va samarali amalga oshadi.",
        """01:01:05"""
    ),
    (
        135,
        "Baytlarni Megabaytga aylantirish",
        "Fayl hajmini baytlardan MB ga o'tkazib, qoldig'ini hisoblang.",
        """#!/usr/bin/env bash

bytes=104857600
mb=$((bytes / (1024 * 1024)))

echo "Hajmi: ${mb} MB"
""",
        "Xotira o'lchov birliklari $1024$ asosida hisoblanadi ($1\\text{ MB} = 1024 \\times 1024\\text{ bayt}$).",
        """Hajmi: 100 MB"""
    ),
    (
        136,
        "Faktorial hisoblash (iterativ usulda)",
        "5 sonining faktorialini ($5!$) for sikli va arifmetik ko'paytirish bilan toping.",
        """#!/usr/bin/env bash

n=5
fact=1

for (( i=1; i<=n; i++ )); do
    fact=$((fact * i))
done

echo "$n! = $fact"
""",
        "Faktorial algoritmi har bir qadamda yangi qiymatni oldingi yig'indiga ko'paytirib boradi.",
        """5! = 120"""
    ),
    (
        137,
        "Fibonachchi sonlar ketma-ketligi",
        "Dastlabki 7 ta Fibonachchi sonini chop eting.",
        """#!/usr/bin/env bash

a=0
b=1
echo -n "$a $b "

for (( i=2; i<7; i++ )); do
    c=$((a + b))
    echo -n "$c "
    a=$b
    b=$c
done
echo ""
""",
        "Fibonachchi ketma-ketligida har bir yangi element o'zidan oldingi ikkita elementning arifmetik yig'indisiga teng bo'ladi.",
        """0 1 1 2 3 5 8"""
    ),
    (
        138,
        "Eng katta umumiy bo'luvchi (EKUB / GCD)",
        "Evklid algoritmi orqali 48 va 18 ning EKUB ini toping.",
        """#!/usr/bin/env bash

x=48
y=18

while (( y != 0 )); do
    r=$((x % y))
    x=$y
    y=$r
done

echo "EKUB: $x"
""",
        "Evklid algoritmi qoldiq nolga teng bo'lguncha doimiy modul amalini bajarish orqali eng katta bo'luvchini tezkor topadi.",
        """EKUB: 6"""
    ),
    (
        139,
        "Eng kichik umumiy karrali (EKUK / LCM)",
        "EKUB orqali 12 va 15 ning EKUK ini hisoblang: $(a \\times b) / \\text{EKUB}$.",
        """#!/usr/bin/env bash

a=12
b=15
# a va b ning EKUBi 3 ga teng
gcd=3
lcm=$(( (a * b) / gcd ))

echo "EKUK: $lcm"
""",
        "Ikkita sonning ko'paytmasini ularning EKUBiga bo'lish orqali ularning EKUKi topiladi.",
        """EKUK: 60"""
    ),
    (
        140,
        "Sonning tub (prime) ekanligini tekshirish",
        "29 sonining tub ekanligini arifmetik bo'linish orqali aniqlang.",
        """#!/usr/bin/env bash

n=29
is_prime=1

for (( i=2; i*i<=n; i++ )); do
    if (( n % i == 0 )); then
        is_prime=0
        break
    fi
done

echo "$n soni tubmi: $( (( is_prime )) && echo 'Ha' || echo 'Yoq' )"
""",
        "Son faqat 1 ga va o'ziga bo'linsa tub son hisoblanadi. Tekshirishni $\\sqrt{n}$ gacha davom ettirish optimaldir.",
        """29 soni tubmi: Ha"""
    ),
    (
        141,
        "Raqamlar yig'indisini hisoblash",
        "Butun sonning har bir raqamini ajratib olib, ularning yig'indisini hisoblang.",
        """#!/usr/bin/env bash

num=12345
sum=0

while (( num > 0 )); do
    digit=$((num % 10))
    sum=$((sum + digit))
    num=$((num / 10))
done

echo "Raqamlar yig'indisi: $sum"
""",
        "10 ga bo'lgandagi qoldiq eng oxirgi raqamni beradi, 10 ga butunli bo'lish esa oxirgi raqamni o'chiradi.",
        """Raqamlar yig'indisi: 15"""
    ),
    (
        142,
        "Haroratni Selsiy dan Farengeyt ga aylantirish",
        "25 daraja Selsiy haroratini Farengeyt formulasida hisoblang ($F = C \\times 9/5 + 32$).",
        """#!/usr/bin/env bash

celsius=25
fahr=$(echo "scale=1; ($celsius * 9 / 5) + 32" | bc)

echo "$celsius°C = ${fahr}°F"
""",
        "O'nlik kasrli standart harorat konvertatsiyasi 'bc' orqali hisoblanadi.",
        """25°C = 77.0°F"""
    ),
    (
        143,
        "Valyuta konvertatsiyasi va tranzaksiya komissiyasi",
        "Pul o'tkazmasidan 1.5% komissiya ushlab qolinishini hisoblang.",
        """#!/usr/bin/env bash

amount=1000
fee_percent=1.5

net_amount=$(awk -v a=$amount -v f=$fee_percent 'BEGIN { fee = (a * f) / 100; printf "%.2f", a - fee }')
echo "Sof mablag': $net_amount USD"
""",
        "'awk' orqali foiz va qolgan summani aniq hisoblash.",
        """Sof mablag': 985.00 USD"""
    ),
    (
        144,
        "Massiv elementlari o'rtacha arifmetik qiymatini hisoblash",
        "5 ta server ping vaqtlarining o'rtacha qiymatini toping.",
        """#!/usr/bin/env bash

pings=(12 15 18 11 14)
sum=0

for p in "${pings[@]}"; do
    sum=$((sum + p))
done

avg=$((sum / ${#pings[@]}))
echo "O'rtacha ping: ${avg}ms"
""",
        "Barcha elementlar yig'indisini elementlar soniga bo'lish orqali butun o'rtacha qiymat topiladi.",
        """O'rtacha ping: 14ms"""
    ),
    (
        145,
        "Sonni 16-lik (hex) formatga o'tkazish",
        "O'nlik sonni toza arifmetik orqali hex satrga formatlang.",
        """#!/usr/bin/env bash

dec=48879
printf "0x%X\\n" "$dec"
""",
        "'printf' ning '%X' formati sonni darhol katta harfli hex ko'rinishida chop etadi.",
        """0xBEEF"""
    ),
    (
        146,
        "Bitmask orqali binar ko'rinishni chop etish",
        "8-bitli sonning har bir bitini alohida ekranga chiqaring.",
        """#!/usr/bin/env bash

val=42
bin=""

for (( i=7; i>=0; i-- )); do
    bit=$(( (val >> i) & 1 ))
    bin="${bin}${bit}"
done

echo "42 ning 8-bitli binar shakli: $bin"
""",
        "Bitlarni o'ngga N ta surib '& 1' qilish orqali har bir bitning 0 yoki 1 ekanligi aniqlanadi.",
        """42 ning 8-bitli binar shakli: 00101010"""
    ),
    (
        147,
        "Xotira sahifalari sonini hisoblash (Page size = 4KB)",
        "64 MB bufer xotirasiga nechta 4096 baytlik sahifa sig'ishini hisoblang.",
        """#!/usr/bin/env bash

buffer_bytes=$((64 * 1024 * 1024))
page_size=4096
pages=$((buffer_bytes / page_size))

echo "Sahifalar soni: $pages ta"
""",
        "Tizimli dasturlash va operatsion tizimlarda xotira sahifalari (paging) miqdori butun bo'lish orqali aniqlanadi.",
        """Sahifalar soni: 16384 ta"""
    ),
    (
        148,
        "Daraja o'sish vaqtini o'lchash (Exponential Backoff kalkulyatori)",
        "Qayta urinish (retry) algoritmi uchun eksponentsial kutish vaqtini hisoblang: $2^{\\text{attempt}}$.",
        """#!/usr/bin/env bash

attempt=4
base_delay=2
delay=$(( base_delay * (2 ** attempt) ))

echo "$attempt-urinish uchun kutish vaqti: ${delay}s"
""",
        "Eksponentsial orqaga chekinish (exponential backoff) tarmoq nosozliklarida serverni ortiqcha yuklamaslik uchun kutish vaqtini 2 barobardan oshirib boradi.",
        """4-urinish uchun kutish vaqti: 32s"""
    ),
    (
        149,
        "IP manzilni butun 32-bitli songa aylantirish (IPv4 to Integer)",
        "IPv4 manzilini 32-bitli butun songa (numeric IP) o'giring.",
        """#!/usr/bin/env bash

ip="192.168.1.1"
IFS='.' read -r o1 o2 o3 o4 <<< "$ip"

int_ip=$(( (o1 << 24) + (o2 << 16) + (o3 << 8) + o4 ))
echo "$ip butun son ko'rinishida: $int_ip"
""",
        "IPv4 manzili 4 ta oktetdan iborat. Har bir oktet tegishli ravishda 24, 16, 8 bit chapga surilib qo'shilsa, yagona 32-bitli integer hosil bo'ladi.",
        """192.168.1.1 butun son ko'rinishida: 3232235777"""
    ),
    (
        150,
        "Kompleks resurs balansi kalkulyatori: Klaster quvvat hisoblagichi",
        "Klasterdagi serverlar soni, protsessor va xotira zaxirasini tahlil qiluvchi to'liq hisobot tuzing.",
        """#!/usr/bin/env bash

nodes=8
ram_per_node=64
cpu_per_node=16

total_ram=$((nodes * ram_per_node))
total_cpu=$((nodes * cpu_per_node))

reserved_ram=$(( (total_ram * 20) / 100 ))
available_ram=$((total_ram - reserved_ram))

echo "=== Klaster Resurslari Hisoboti ==="
echo "Tugunlar: $nodes ta"
echo "Jami CPU: $total_cpu vCPU"
echo "Jami RAM: ${total_ram} GB"
echo "Zaxiralangan (20%): ${reserved_ram} GB"
echo "Foydalanishga ochiq RAM: ${available_ram} GB"
""",
        "Bash arifmetikasi va parameter expansion imkoniyatlari yordamida tashqi dasturlarsiz to'liq va tezkor server sig'imi hisobotlarini tuzish mumkin.",
        """=== Klaster Resurslari Hisoboti ===
Tugunlar: 8 ta
Jami CPU: 128 vCPU
Jami RAM: 512 GB
Zaxiralangan (20%): 102 GB
Foydalanishga ochiq RAM: 410 GB"""
    )
]

# Write Module 02
f02 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_02]
save_file("bash_02_ozgaruvchilar_va_parametrlar.md", f02)

with open(os.path.join(gen_dir, "gen_02_ozgaruvchilar.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_02) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_02_ozgaruvchilar_va_parametrlar.md', formatted)\n")

# Write Module 03
f03 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_03]
save_file("bash_03_arifmetika_va_operatorlar.md", f03)

with open(os.path.join(gen_dir, "gen_03_arifmetika.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_03) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_03_arifmetika_va_operatorlar.md', formatted)\n")

print("Modules 02 and 03 generated successfully!")
