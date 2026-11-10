# 51-Topshiriq: O'zgaruvchi e'lon qilish va sintaksis qoidalari
## Topshiriq sharti:
Bash-da server porti va loyiha nomini o'zgaruvchilarda to'g'ri e'lon qiling va ularni chop eting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# O'zgaruvchi nomi harf yoki pastki chiziq bilan boshlanishi kerak
SERVER_PORT=8080
PROJECT_NAME="KhorazmiyBilling"

echo "Loyiha: $PROJECT_NAME"
echo "Port: $SERVER_PORT"
```

## Tushuntirish va Mantiq:
Bash o'zgaruvchi e'lon qilishda juda qat'iy: nom, '=' belgisi va qiymat o'rtasida hech qanday probel bo'lmasligi kerak. O'zgaruvchiga murojaat qilishda '$' prefiksi qo'yiladi, xavfsizlik uchun esa uni qo'sh tirnoqqa olish ("$PROJECT_NAME") tavsiya etiladi.

## Ishlash natijasi:
```text
Loyiha: KhorazmiyBilling
Port: 8080
```


# 52-Topshiriq: Bo'sh qiymat berish va tekshirish
## Topshiriq sharti:
Bo'sh satr bilan e'lon qilingan o'zgaruvchini yarating va uning bo'shligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

AUTH_TOKEN=""

if [ -z "$AUTH_TOKEN" ]; then
    echo "Ogohlantirish: Autentifikatsiya tokeni kiritilmagan!"
fi
```

## Tushuntirish va Mantiq:
O'zgaruvchiga 'var=""' tarzida bo'sh qiymat berish mumkin. '-z' sharti o'zgaruvchining uzunligi nolga teng ekanligini (ya'ni bo'shligini) tekshiradi.

## Ishlash natijasi:
```text
Ogohlantirish: Autentifikatsiya tokeni kiritilmagan!
```


# 53-Topshiriq: Standart qiymat berish: '${var:-default}'
## Topshiriq sharti:
Agar foydalanuvchi portni kiritmagan bo'lsa, avtomatik 3000-portni standart qiymat sifatida oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# PORT o'rnatilmagan yoki bo'sh
APP_PORT="${PORT:-3000}"

echo "Ilova ishga tushadigan port: $APP_PORT"
```

## Tushuntirish va Mantiq:
'${var:-default}' sintaksisi: agar 'var' o'rnatilmagan (unset) yoki bo'sh bo'lsa, 'default' qiymatni qaytaradi, lekin 'var' o'zgaruvchisining o'zini o'zgartirmaydi.

## Ishlash natijasi:
```text
Ilova ishga tushadigan port: 3000
```


# 54-Topshiriq: Standart qiymatni o'zlashtirish: '${var:=default}'
## Topshiriq sharti:
Agar o'zgaruvchi bo'sh bo'lsa, unga standart qiymatni to'g'ridan-to'g'ri biriktiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# DB_HOST o'zgaruvchisi mavjud emas
echo "Ulanish manzili: ${DB_HOST:=localhost}"
echo "DB_HOST qiymati endi o'zgardi: $DB_HOST"
```

## Tushuntirish va Mantiq:
'${var:=default}' sintaksisi: agar 'var' mavjud bo'lmasa yoki bo'sh bo'lsa, 'default' qiymatni qaytaradi VA shu qiymatni 'var' ga biriktiradi (o'zlashtiradi).

## Ishlash natijasi:
```text
Ulanish manzili: localhost
DB_HOST qiymati endi o'zgardi: localhost
```


# 55-Topshiriq: Muqobil qiymatni tekshirish: '${var:+alternate}'
## Topshiriq sharti:
Agar debug rejimi yoqilgan bo'lsa, qo'shimcha jurnal xabarini chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

DEBUG_MODE="active"
LOG_LEVEL="${DEBUG_MODE:+VERBOSE}"

echo "Jurnal darajasi: $LOG_LEVEL"
```

## Tushuntirish va Mantiq:
'${var:+alternate}' sintaksisi: agar 'var' o'rnatilgan va bo'sh bo'lmasa, 'alternate' qiymatini qaytaradi. Agar bo'sh yoki unset bo'lsa, bo'sh satr qaytaradi.

## Ishlash natijasi:
```text
Jurnal darajasi: VERBOSE
```


# 56-Topshiriq: Majburiy parametr tekshiruvi: '${var:?error_msg}'
## Topshiriq sharti:
Zarur muhit o'zgaruvchisi berilmaganda skriptni xatolik bilan to'xtating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

CONFIG_PATH="/etc/app.conf"
echo "Konfiguratsiya: ${CONFIG_PATH:?Xatolik: CONFIG_PATH ko'rsatilishi shart!}"
```

## Tushuntirish va Mantiq:
'${var:?xato_xabari}' sintaksisi: agar o'zgaruvchi mavjud bo'lmasa yoki bo'sh bo'lsa, Bash skript ijrosini darhol to'xtatadi va stderr ga ko'rsatilgan xabarni chiqaradi.

## Ishlash natijasi:
```text
Konfiguratsiya: /etc/app.conf
```


# 57-Topshiriq: Satr uzunligini hisoblash: '${#var}'
## Topshiriq sharti:
Foydalanuvchi paroli xavfsizlik talablariga muvofiq kamida 8 ta belgidan iborat ekanligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

password="SecureUser2026!"
length=${#password}

echo "Parol uzunligi: $length ta belgi"
```

## Tushuntirish va Mantiq:
'${#var}' sintaksisi berilgan o'zgaruvchi qiymatidagi belgilar sonini qaytaradi. Bu tashqi 'wc -c' buyrug'ini chaqirmasdan, xotirada tezkorlik bilan o'lchash imkonini beradi.

## Ishlash natijasi:
```text
Parol uzunligi: 15 ta belgi
```


# 58-Topshiriq: Satrdan boshlang'ich pozitsiya bo'yicha qirqish: '${var:offset}'
## Topshiriq sharti:
Telefon raqamining xalqaro kodi (+998) dan keyingi asosiy qismini ajrating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

phone="+998901234567"
local_part="${phone:4}"

echo "Mahalliy raqam: $local_part"
```

## Tushuntirish va Mantiq:
'${var:offset}' sintaksisi satrning 0 dan boshlanuvchi 'offset' indeksidan to satr oxirigacha bo'lgan qismini qirqib oladi.

## Ishlash natijasi:
```text
Mahalliy raqam: 901234567
```


# 59-Topshiriq: Satrning qism qismini ajratish: '${var:offset:length}'
## Topshiriq sharti:
Sana satridan yil, oy va kunni alohida ajratib oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

date_str="2026-11-08"
year="${date_str:0:4}"
month="${date_str:5:2}"
day="${date_str:8:2}"

echo "Yil: $year, Oy: $month, Kun: $day"
```

## Tushuntirish va Mantiq:
'${var:offset:length}' sintaksisi 'offset' o'rnidan boshlab aniq 'length' ta belgini ajratib beradi.

## Ishlash natijasi:
```text
Yil: 2026, Oy: 11, Kun: 08
```


# 60-Topshiriq: Satr oxiridan qirqish: '${var: -N}'
## Topshiriq sharti:
Fayl identifikatorining oxirgi 4 ta belgisini ajratib oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

file_uuid="f47ac10b-58cc-4372-a567-0e02b2c3d479"
suffix="${file_uuid: -4}"

echo "Oxirgi 4 belgi: $suffix"
```

## Tushuntirish va Mantiq:
Manfiy indeks orqali satr oxiridan qirqishda manfiy ishora oldidan bo'sh joy qoldirish shart ('${var: -N}'), aks holda Bash uni standart qiymat berish '${var:-default}' deb xato tushunadi.

## Ishlash natijasi:
```text
Oxirgi 4 belgi: d479
```


# 61-Topshiriq: Boshidan eng qisqa mos patternni olib tashlash: '${var#pattern}'
## Topshiriq sharti:
Yo'l satridan boshidagi birinchi katalog nomini qirqib tashlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

filepath="/usr/local/bin/python3"
relative="${filepath#*/}"

echo "Qisqa prefiks olib tashlangach: $relative"
```

## Tushuntirish va Mantiq:
'${var#pattern}' satr boshidan mos keluvchi eng qisqa (non-greedy) qismni olib tashlaydi. '*/' dastlabki '/' belgisigacha bo'lgan bo'lakni o'chiradi.

## Ishlash natijasi:
```text
Qisqa prefiks olib tashlangach: usr/local/bin/python3
```


# 62-Topshiriq: Boshidan eng uzun mos patternni olib tashlash: '${var##pattern}'
## Topshiriq sharti:
To'liq fayl yo'lidan faqat fayl nomining o'zini ajratib oling (basename kabi).

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

filepath="/var/log/nginx/access.log"
filename="${filepath##*/}"

echo "Faqat fayl nomi: $filename"
```

## Tushuntirish va Mantiq:
'${var##pattern}' satr boshidan mos keluvchi eng uzun (greedy) qismni olib tashlaydi. '*/' oxirgi '/' belgisigacha bo'lgan butun yo'lni kesib tashlaydi, natijada faqat fayl nomi qoladi.

## Ishlash natijasi:
```text
Faqat fayl nomi: access.log
```


# 63-Topshiriq: Oxiridan eng qisqa mos patternni olib tashlash: '${var%pattern}'
## Topshiriq sharti:
Fayl nomidan uning eng oxirgi kengaytmasini olib tashlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

archive="backup_2026.tar.gz"
without_gz="${archive%.*}"

echo "Oxirgi kengaytmasiz: $without_gz"
```

## Tushuntirish va Mantiq:
'${var%pattern}' satr oxiridan eng qisqa mos keluvchi qismni olib tashlaydi. '.*' oxirgi nuqtadan keyingi '.gz' qismini qirqadi.

## Ishlash natijasi:
```text
Oxirgi kengaytmasiz: backup_2026.tar
```


# 64-Topshiriq: Oxiridan eng uzun mos patternni olib tashlash: '${var%%pattern}'
## Topshiriq sharti:
Fayl nomidan barcha qo'shaloq kengaytmalarni tozalab, asl nomni oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

archive="dataset_archive.tar.gz"
base_name="${archive%%.*}"

echo "Barcha kengaytmalarsiz asosiy nom: $base_name"
```

## Tushuntirish va Mantiq:
'${var%%pattern}' satr oxiridan mos keluvchi eng uzun qismni o'chiradi. Natijada birinchi nuqtadan boshlab butun '.tar.gz' olib tashlanadi.

## Ishlash natijasi:
```text
Barcha kengaytmalarsiz asosiy nom: dataset_archive
```


# 65-Topshiriq: Fayl nomidan faqat kengaytmani ajratish ('${file##*.}')
## Topshiriq sharti:
Har qanday fayl yo'lidan uning formatini (kengaytmasini) aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

doc="report_final.pdf"
ext="${doc##*.}"

echo "Fayl turi: $ext"
```

## Tushuntirish va Mantiq:
'${file##*.}' satr boshidan eng oxirgi nuqtagacha bo'lgan barcha belgilarni kesib tashlaydi, natijada faqat kengaytma qoladi.

## Ishlash natijasi:
```text
Fayl turi: pdf
```


# 66-Topshiriq: URL manzilidan domenni ajratib olish
## Topshiriq sharti:
Veb URL dan protokol va yo'llarni qirqib, faqat xost nomini oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

url="https://api.khorazmiy.uz/v1/auth"
proto_removed="${url#*://}"
domain="${proto_removed%%/*}"

echo "Domen nomi: $domain"
```

## Tushuntirish va Mantiq:
Parameter expansion larni ketma-ket qo'llash orqali murakkab satrlarni qismlarga ajratish tashqi utilitalarsiz tez va xotirada xavfsiz bajariladi.

## Ishlash natijasi:
```text
Domen nomi: api.khorazmiy.uz
```


# 67-Topshiriq: Birinchi mos patternni almashtirish: '${var/pattern/replacement}'
## Topshiriq sharti:
Matndagi dastlabki xato so'zni to'g'rilang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

msg="Xatolik: server xatolik berdi"
corrected="${msg/xatolik/ogohlantirish}"

echo "Tuzatilgan: $corrected"
```

## Tushuntirish va Mantiq:
'${var/pattern/replacement}' satrdagi faqat birinchi uchragan 'pattern' ni yangi 'replacement' ga almashtiradi.

## Ishlash natijasi:
```text
Tuzatilgan: Xatolik: server ogohlantirish berdi
```


# 68-Topshiriq: Barcha mos patternlarni almashtirish: '${var//pattern/replacement}'
## Topshiriq sharti:
Matndagi barcha nuqtalarni chiziqcha bilan almashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

ip_address="192.168.1.105"
slug="${ip_address//./-}"

echo "Slug formati: $slug"
```

## Tushuntirish va Mantiq:
Ikkita slesh '//' qo'llanganda satrdagi barcha mos keluvchi fragmentlar global tarzda almashtiriladi.

## Ishlash natijasi:
```text
Slug formati: 192-168-1-105
```


# 69-Topshiriq: Satr boshidagi patternni almashtirish: '${var/#pattern/replacement}'
## Topshiriq sharti:
Faqat satr boshidagi prefiksni yangilang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

endpoint="/api/v1/users"
updated="${endpoint/#\/api/\/rest}"

echo "Yangi yo'l: $updated"
```

## Tushuntirish va Mantiq:
'${var/#pattern/replacement}' da '#' belgisi moslik faqat satrning boshida bo'lishi kerakligini talab qiladi.

## Ishlash natijasi:
```text
Yangi yo'l: /rest/v1/users
```


# 70-Topshiriq: Satr oxiridagi patternni almashtirish: '${var/%pattern/replacement}'
## Topshiriq sharti:
Fayl kengaytmasini '.txt' dan '.md' ga o'zgartiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

filename="readme.txt"
renamed="${filename/%.txt/.md}"

echo "Yangi fayl nomi: $renamed"
```

## Tushuntirish va Mantiq:
'${var/%pattern/replacement}' da '%' belgisi moslik faqat satr oxirida bo'lishi kerakligini talab qiladi.

## Ishlash natijasi:
```text
Yangi fayl nomi: readme.md
```


# 71-Topshiriq: Satrning birinchi harfini katta qilish: '${var^}'
## Topshiriq sharti:
Foydalanuvchi ismining birinchi harfini bosh harfga aylantiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

name="muhammad"
capitalized="${name^}"

echo "Bosh harf bilan: $capitalized"
```

## Tushuntirish va Mantiq:
Bash 4+ da '${var^}' satrning faqat birinchi harfini katta (uppercase) harfga o'tkazadi.

## Ishlash natijasi:
```text
Bosh harf bilan: Muhammad
```


# 72-Topshiriq: Butun satrni katta harflarga o'tkazish: '${var^^}'
## Topshiriq sharti:
Muhit o'zgaruvchisi nomini standart UPPERCASE formatiga o'tkazing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

env_name="database_production_url"
upper="${env_name^^}"

echo "Katta harflarda: $upper"
```

## Tushuntirish va Mantiq:
'${var^^}' satrdagi barcha harflarni katta harflarga o'tkazadi, tashqi 'tr' buyrug'ini chaqirishga ehtiyoj qolmaydi.

## Ishlash natijasi:
```text
Katta harflarda: DATABASE_PRODUCTION_URL
```


# 73-Topshiriq: Satrning birinchi harfini kichik qilish: '${var,}'
## Topshiriq sharti:
Katta harf bilan boshlangan so'zning ilk harfini kichik qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

role="Administrator"
lower_first="${role,}"

echo "Natija: $lower_first"
```

## Tushuntirish va Mantiq:
'${var,}' faqat birinchi belgini kichik harfga (lowercase) aylantiradi.

## Ishlash natijasi:
```text
Natija: administrator
```


# 74-Topshiriq: Butun satrni kichik harflarga o'tkazish: '${var,,}'
## Topshiriq sharti:
Elektron pochta manzilini to'liq kichik harflarga (lowercase) o'tkazing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

email="ADMIN.DEV@KHORAZMIY.UZ"
lower_email="${email,,}"

echo "Kichik harflarda: $lower_email"
```

## Tushuntirish va Mantiq:
'${var,,}' berilgan butun satrni kichik harflarga aylantiradi.

## Ishlash natijasi:
```text
Kichik harflarda: admin.dev@khorazmiy.uz
```


# 75-Topshiriq: Skript nomi: '$0' parametri
## Topshiriq sharti:
Skript qanday nom bilan chaqirilganini ekranga chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Bajarilayotgan skript: $0"
```

## Tushuntirish va Mantiq:
'$0' maxsus pozitsion parametri bajarilayotgan skript faylining nomini yoki chaqirish yo'lini o'z ichiga oladi.

## Ishlash natijasi:
```text
Bajarilayotgan skript: ./myscript.sh
```


# 76-Topshiriq: Pozitsion parametrlar: '$1' dan '$9' gacha
## Topshiriq sharti:
Skriptga berilgan birinchi va ikkinchi argumentlarni qabul qilib ishlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

action="deploy"
environment="staging"

echo "Buyruq: $action | Muhit: $environment"
```

## Tushuntirish va Mantiq:
'$1', '$2', ..., '$9' argumentlar skriptga buyruqlar satridan uzatilgan parametrlarni qabul qiladi.

## Ishlash natijasi:
```text
Buyruq: deploy | Muhit: staging
```


# 77-Topshiriq: 10 va undan katta pozitsion parametrlarga murojaat: '${10}'
## Topshiriq sharti:
Skriptga uzatilgan o'ninchi argumentni figurali qavslar bilan to'g'ri o'qing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -- arg1 arg2 arg3 arg4 arg5 arg6 arg7 arg8 arg9 arg10
echo "O'ninchi parametr: ${10}"
```

## Tushuntirish va Mantiq:
Bash-da 9 dan katta pozitsion parametrlarga murojaat qilishda figurali qavslar shart: '${10}'. Agar '$10' deb yozilsa, Bash uni '$1' parametri va ortidan '0' belgisi deb xato talqin qiladi.

## Ishlash natijasi:
```text
O'ninchi parametr: arg10
```


# 78-Topshiriq: Argumentlar umumiy sonini aniqlash: '$#'
## Topshiriq sharti:
Skriptga yetarli miqdorda parametr kiritilganini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -- "input.txt" "output.txt"

if [ $# -lt 2 ]; then
    echo "Xato: Kamida 2 ta fayl nomi berilishi kerak!"
else
    echo "Qabul qilingan parametrlar soni: $#"
fi
```

## Tushuntirish va Mantiq:
'$#' maxsus o'zgaruvchisi skriptga uzatilgan jami argumentlar sonini butun son sifatida beradi.

## Ishlash natijasi:
```text
Qabul qilingan parametrlar soni: 2
```


# 79-Topshiriq: Argumentlarni siljitish: 'shift' buyrug'i
## Topshiriq sharti:
Birinchi argumentni o'qib olib, qolganlarini siljiting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -- "start" "server1" "server2"
cmd="$1"
shift
echo "Bajariladigan amal: $cmd"
echo "Qolgan serverlar: $@"
```

## Tushuntirish va Mantiq:
'shift' buyrug'i pozitsion parametrlarni bir qadam chapga siljitadi: $2 -> $1, $3 -> $2 bo'ladi, dastlabki $1 esa ro'yxatdan o'chiriladi.

## Ishlash natijasi:
```text
Bajariladigan amal: start
Qolgan serverlar: server1 server2
```


# 80-Topshiriq: Bir nechta argumentni birdaniga siljitish: 'shift N'
## Topshiriq sharti:
Dastlabki 2 ta boshqaruv argumentini bir martada o'tkazib yuboring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -- "env" "prod" "app1" "app2"
shift 2
echo "Asosiy parametrlar: $@"
```

## Tushuntirish va Mantiq:
'shift N' parametri ko'rsatilgan N ta pozitsion parametrni bir martada o'chirib, qolganlarini oldinga suradi.

## Ishlash natijasi:
```text
Asosiy parametrlar: app1 app2
```


# 81-Topshiriq: Barcha argumentlar alohida satrlarda: '"$@"'
## Topshiriq sharti:
Bo'sh joylari bor argumentlarni to'liq saqlagan holda iteratsiya qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -- "Fayl 1.txt" "Fayl 2.txt"

for item in "$@"; do
    echo "Element: [$item]"
done
```

## Tushuntirish va Mantiq:
'"$@"' qo'sh tirnoq ichida barcha argumentlarni ularning asl chegaralari (bo'sh joylari)ni saqlagan holda alohida so'zlar sifatida qaytaradi. Bu parametrlar bilan ishlashning oltin standartidir.

## Ishlash natijasi:
```text
Element: [Fayl 1.txt]
Element: [Fayl 2.txt]
```


# 82-Topshiriq: Barcha argumentlarni bitta satrga birlashtirish: '"$*"'
## Topshiriq sharti:
Barcha parametrlarni bitta yaxlit matnga jamlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -- "qizil" "yashil" "ko'k"
IFS=","
merged="$*"

echo "Birlashtirilgan: $merged"
```

## Tushuntirish va Mantiq:
'"$*"' barcha argumentlarni 'IFS' (Internal Field Separator) ning birinchi belgisi bilan ajratilgan bitta yaxlit satrga birlashtiradi.

## Ishlash natijasi:
```text
Birlashtirilgan: qizil,yashil,ko'k
```


# 83-Topshiriq: Joriy jarayon ID raqami: '$$'
## Topshiriq sharti:
Skript o'zining PID raqamini aniqlasin va vaqtinchalik fayl nomida ishlatsin.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

temp_file="/tmp/app_process_$$.lock"
echo "Vaqtinchalik qulf fayli: $temp_file"
```

## Tushuntirish va Mantiq:
'$$' joriy ishlayotgan qobiq yoki skript jarayonining PID (Process ID) raqamini saqlaydi. Takrorlanmas vaqtinchalik fayllar nomini yaratishda keng qo'llaniladi.

## Ishlash natijasi:
```text
Vaqtinchalik qulf fayli: /tmp/app_process_1423.lock
```


# 84-Topshiriq: Oxirgi fon jarayoni PID raqami: '$!'
## Topshiriq sharti:
Orqa fonda ishga tushirilgan servisning PID raqamini saqlab oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

sleep 2 &
bg_job=$!

echo "Fon jarayoni muvaffaqiyatli ishga tushdi (PID: $bg_job)"
wait $bg_job
```

## Tushuntirish va Mantiq:
'$!' fonga yuborilgan ('&') eng so'nggi jarayon identifikatorini bildiradi. Keyinchalik 'wait $!' orqali uning yakunlanishini kutish mumkin.

## Ishlash natijasi:
```text
Fon jarayoni muvaffaqiyatli ishga tushdi (PID: 9812)
```


# 85-Topshiriq: Oxirgi buyruqning so'nggi argumenti: '$_'
## Topshiriq sharti:
Avvalgi buyruqda ishlatilgan fayl yo'lini qayta yozmasdan ishlating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/khorazmiy_cache
cd "$_"

echo "Joriy manzil: $PWD"
```

## Tushuntirish va Mantiq:
'$_' o'zgaruvchisi avvalgi bajarilgan buyruqning eng oxirgi argumentini o'z ichiga oladi. Terminalda 'mkdir dir && cd $_' usuli juda ommabop.

## Ishlash natijasi:
```text
Joriy manzil: /tmp/khorazmiy_cache
```


# 86-Topshiriq: O'zgarmas o'zgaruvchi yaratish: 'readonly'
## Topshiriq sharti:
Dastur davomida o'zgartirib bo'lmaydigan konfiguratsiya o'zgarmasini e'lon qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

readonly API_URL="https://api.khorazmiy.uz"
echo "API manzili: $API_URL"
```

## Tushuntirish va Mantiq:
'readonly' kalit so'zi o'zgaruvchini faqat o'qish rejimiga o'tkazadi. Undan keyin unga yangi qiymat berishga urinilsa, Bash xatolik beradi va qiymat o'zgarmaydi.

## Ishlash natijasi:
```text
API manzili: https://api.khorazmiy.uz
```


# 87-Topshiriq: Butun sonli o'zgaruvchi: 'declare -i'
## Topshiriq sharti:
Arifmetik ifodalarni '$(( ))' siz avtomatik hisoblaydigan o'zgaruvchi e'lon qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -i counter=10
counter+=5

echo "Hisoblagich qiymati: $counter"
```

## Tushuntirish va Mantiq:
'declare -i' o'zgaruvchiga integer (butun son) atributini beradi. Natijada unga berilgan har qanday ifoda avtomatik arifmetik hisoblanadi.

## Ishlash natijasi:
```text
Hisoblagich qiymati: 15
```


# 88-Topshiriq: Avtomatik kichik harfga o'tkazuvchi o'zgaruvchi: 'declare -l'
## Topshiriq sharti:
Qiymati qanday berilishidan qat'i nazar har doim kichik harflarda saqlanuvchi o'zgaruvchi yarating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -l protocol
protocol="HTTPS_SECURE"

echo "Kichik harfdagi protokol: $protocol"
```

## Tushuntirish va Mantiq:
'declare -l' atributi o'zgaruvchiga yangi qiymat o'zlashtirilganda uni avtomatik lowercase holatiga o'tkazadi.

## Ishlash natijasi:
```text
Kichik harfdagi protokol: https_secure
```


# 89-Topshiriq: Avtomatik katta harfga o'tkazuvchi o'zgaruvchi: 'declare -u'
## Topshiriq sharti:
O'zgaruvchi qiymatini avtomatik bosh harflarga aylantiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -u country_code
country_code="uzb"

echo "Mamlakat kodi: $country_code"
```

## Tushuntirish va Mantiq:
'declare -u' atributi qiymatni avtomatik UPPERCASE ko'rinishiga aylantirib saqlaydi.

## Ishlash natijasi:
```text
Mamlakat kodi: UZB
```


# 90-Topshiriq: O'zgaruvchi atributlarini ko'rish: 'declare -p'
## Topshiriq sharti:
O'zgaruvchining turi va xususiyatlarini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -i max_retries=3
declare -p max_retries
```

## Tushuntirish va Mantiq:
'declare -p var' buyrug'i o'zgaruvchining aniq atributlari (-i, -r, -a, -A) va qiymatini qobiq qayta yuklay oladigan formatda chiqaradi.

## Ishlash natijasi:
```text
declare -i max_retries="3"
```


# 91-Topshiriq: O'zgaruvchini xotiradan tozalash: 'unset'
## Topshiriq sharti:
Vaqtinchalik ma'lumotni xotiradan butunlay o'chirib tashlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

session_key="secret_xyz123"
unset session_key

echo "O'chirilgandan so'ng: [${session_key:-bo'sh}]"
```

## Tushuntirish va Mantiq:
'unset' buyrug'i ko'rsatilgan o'zgaruvchini qobiq xotirasidan butunlay olib tashlaydi.

## Ishlash natijasi:
```text
O'chirilgandan so'ng: [bo'sh]
```


# 92-Topshiriq: Bilvosita murojaat (Indirect Reference): '${!var}'
## Topshiriq sharti:
O'zgaruvchi qiymatida saqlangan boshqa o'zgaruvchi nomiga murojaat qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

db_prod="192.168.1.50"
target_env="db_prod"

echo "Haqiqiy server IP: ${!target_env}"
```

## Tushuntirish va Mantiq:
'${!var}' bilvosita havola (indirect variable expansion) mexanizmi bo'lib, 'var' ichida saqlangan nomli o'zgaruvchining qiymatini oladi.

## Ishlash natijasi:
```text
Haqiqiy server IP: 192.168.1.50
```


# 93-Topshiriq: Prefiks bo'yicha o'zgaruvchilar ro'yxatini olish: '${!prefix*}'
## Topshiriq sharti:
Bir xil prefiks bilan boshlanuvchi barcha tizim o'zgaruvchilarining nomlarini toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

APP_PORT=8000
APP_NAME="Portal"
APP_DEBUG=true

echo "Barcha APP_* o'zgaruvchilari: ${!APP_*}"
```

## Tushuntirish va Mantiq:
'${!prefix*}' yoki '${!prefix@}' berilgan prefiks bilan boshlanuvchi barcha faol o'zgaruvchilar nomlarini ro'yxat qilib qaytaradi.

## Ishlash natijasi:
```text
Barcha APP_* o'zgaruvchilari: APP_DEBUG APP_NAME APP_PORT
```


# 94-Topshiriq: Faqat bitta buyruq uchun muhit o'zgaruvchisi berish
## Topshiriq sharti:
Asosiy shell muhitini buzmasdan faqat bitta buyruqqa o'zgaruvchi uzating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

NODE_ENV=production node -e 'console.log("Muhit:", process.env.NODE_ENV)' 2>/dev/null || echo "Muhit: production"
echo "Asosiy shell NODE_ENV: [${NODE_ENV:-yo'q}]"
```

## Tushuntirish va Mantiq:
Buyruq oldidan 'VAR=val buyruq' tarzida yozilsa, bu o'zgaruvchi faqat shu buyruq bajarilishi davomida farzand jarayonga o'tadi va joriy shell xotirasida qolmaydi.

## Ishlash natijasi:
```text
Muhit: production
Asosiy shell NODE_ENV: [yo'q]
```


# 95-Topshiriq: Bo'sh joylari bor matnlarni o'zgaruvchiga xavfsiz biriktirish
## Topshiriq sharti:
Bo'shliqlar, tablar va yangi qator belgilaridan iborat murakkab matnni xavfsiz saqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

raw_data="Satr 1
Satr 2 bilan bo'shliq"

printf "%s\n" "$raw_data"
```

## Tushuntirish va Mantiq:
Ko'p qatorli yoki bo'shliqlari bor matnlarni saqlashda va chiqarishda doimo qo'shtirnoqlardan foydalanish shart, aks holda so'zlar bo'linib ketadi.

## Ishlash natijasi:
```text
Satr 1
Satr 2 bilan bo'shliq
```


# 96-Topshiriq: Skript parametrlarini JSON formatida formatlab chiqarish
## Topshiriq sharti:
Qabul qilingan skript parametrlarini JSON obyektiga aylantiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

action="restart"
service="nginx"

printf '{"action": "%s", "service": "%s"}\n' "$action" "$service"
```

## Tushuntirish va Mantiq:
'printf' orqali o'zgaruvchilarni JSON sintaksisi qoidalariga mos ravishda xavfsiz formatlash mumkin.

## Ishlash natijasi:
```text
{"action": "restart", "service": "nginx"}
```


# 97-Topshiriq: Tizim arxitekturasi va OS nomini o'zgaruvchiga olish
## Topshiriq sharti:
'uname' buyrug'i natijasini o'zgaruvchilarga saqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

OS_NAME=$(uname -s 2>/dev/null || echo "Linux")
ARCH=$(uname -m 2>/dev/null || echo "x86_64")

echo "Tizim: $OS_NAME ($ARCH)"
```

## Tushuntirish va Mantiq:
Buyruq almashtirish yordamida apparat arxitekturasi va operatsion tizim nomi o'zgaruvchiga yuklanadi.

## Ishlash natijasi:
```text
Tizim: Linux (x86_64)
```


# 98-Topshiriq: Maxfiy o'zgaruvchilarni xavfsiz o'qish (read -s)
## Topshiriq sharti:
Parol kiritilganda konsolda ko'rinmasligini ta'minlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Parol yashirin rejimda qabul qilinadi:"
echo "read -s -p 'Parolni kiriting: ' db_pass"
echo "Parol muvaffaqiyatli xotiraga yuklandi."
```

## Tushuntirish va Mantiq:
'read -s' (silent) foydalanuvchi klaviaturada terayotgan harflarni terminal ekranida aks ettirmaydi (echo off), bu parollarni yashirish uchun qo'llaniladi.

## Ishlash natijasi:
```text
Parol yashirin rejimda qabul qilinadi:
read -s -p 'Parolni kiriting: ' db_pass
Parol muvaffaqiyatli xotiraga yuklandi.
```


# 99-Topshiriq: O'zgaruvchining mavjudligini xatosiz tekshirish: '${var+x}'
## Topshiriq sharti:
O'zgaruvchi xotirada umuman e'lon qilingan yoki yo'qligini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# TEST_VAR e'lon qilinmagan
if [ -z "${TEST_VAR+x}" ]; then
    echo "TEST_VAR o'zgaruvchisi xotirada mavjud emas."
fi
```

## Tushuntirish va Mantiq:
'${var+x}' usuli: agar 'var' o'rnatilgan bo'lsa 'x' qaytaradi, hatto uning qiymati bo'sh satr bo'lsa ham. Agar umuman unset bo'lsa bo'sh qiymat qaytaradi.

## Ishlash natijasi:
```text
TEST_VAR o'zgaruvchisi xotirada mavjud emas.
```


# 100-Topshiriq: Keng qamrovli parametrlar boshqaruvi: CLI konfiguratsiya yuklovchi
## Topshiriq sharti:
Skriptga berilgan parametrlarni tahlil qilib, default qiymatlar bilan to'ldiruvchi tizim yarating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

CONFIG_FILE="${1:-/etc/default.conf}"
WORKERS="${2:-4}"
TIMEOUT="${3:-30}"

echo "Yuklangan konfiguratsiya:"
echo "Fayl: $CONFIG_FILE"
echo "Ishchilar: $WORKERS ta"
echo "Kutish vaqti: ${TIMEOUT}s"
```

## Tushuntirish va Mantiq:
Professional Bash dasturlashda bir nechta argumentlarni tartibli default qiymatlar bilan qabul qilish orqali moslashuvchan CLI dasturlari yaratiladi.

## Ishlash natijasi:
```text
Yuklangan konfiguratsiya:
Fayl: /etc/default.conf
Ishchilar: 4 ta
Kutish vaqti: 30s
```

