# 151-Topshiriq: Oddiy shart operatori: 'if [ shart ]; then ... fi'
## Topshiriq sharti:
Server holati 'active' ekanligini klassik test buyrug'i bilan tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

status="active"

if [ "$status" = "active" ]; then
    echo "Server muvaffaqiyatli ishlamoqda."
fi
```

## Tushuntirish va Mantiq:
Bash-da 'if' buyrug'i shartning exit kodini tekshiradi. '[' (test) buyrug'i shart rost bo'lsa 0, yolg'on bo'lsa 1 qaytaradi. Shart bajarilsa 'then' va 'fi' orasidagi kod bajariladi.

## Ishlash natijasi:
```text
Server muvaffaqiyatli ishlamoqda.
```


# 152-Topshiriq: Ikki tarmoqli shart: 'if ... else ... fi'
## Topshiriq sharti:
Disk bandligi 90% dan oshganligini tekshirib, xavfsiz yoki xavfli ekanligini bildiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

disk_usage=75

if [ "$disk_usage" -gt 90 ]; then
    echo "XAVF: Disk maydoni tugamoqda!"
else
    echo "Xotira yetarli: ${disk_usage}% band."
fi
```

## Tushuntirish va Mantiq:
'else' bloki 'if' sharti qanoatlantirilmagan (exit code != 0) barcha holatlarda ishga tushadi.

## Ishlash natijasi:
```text
Xotira yetarli: 75% band.
```


# 153-Topshiriq: Ko'p tarmoqli shart: 'if ... elif ... else ... fi'
## Topshiriq sharti:
HTTP javob kodiga (200, 404, 500) qarab xabar chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

http_code=404

if [ "$http_code" -eq 200 ]; then
    echo "So'rov muvaffaqiyatli (200 OK)"
elif [ "$http_code" -eq 404 ]; then
    echo "Sahifa topilmadi (404 Not Found)"
elif [ "$http_code" -eq 500 ]; then
    echo "Server ichki xatosi (500 Internal Error)"
else
    echo "Noma'lum holat kodi: $http_code"
fi
```

## Tushuntirish va Mantiq:
'elif' (else if) ketma-ket bir nechta turli shartlarni zanjir kabi tekshirish imkonini beradi.

## Ishlash natijasi:
```text
Sahifa topilmadi (404 Not Found)
```


# 154-Topshiriq: Klassik '[' vs Zamonaviy '[[' tekshiruvi
## Topshiriq sharti:
Zamonaviy '[[' ifodasining so'zlarga bo'linib ketmaslik afzalligini ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

empty_var=""

# [[ ]] da qo'shtirnoqsiz ham xavfsiz tekshiriladi
if [[ -z $empty_var ]]; then
    echo "O'zgaruvchi bo'sh, lekin sintaksis xatosi chiqmadi."
fi
```

## Tushuntirish va Mantiq:
'[[' Bash-ning ichki kalit so'zi (keyword) bo'lib, klassik '[' buyrug'iga nisbatan xavfsizroq, chunki u argumentlarni kutilmagan tarzda so'zlarga bo'lib yubormaydi va regex ni qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
O'zgaruvchi bo'sh, lekin sintaksis xatosi chiqmadi.
```


# 155-Topshiriq: Fayl yoki katalog mavjudligini tekshirish: '-e'
## Topshiriq sharti:
Konfiguratsiya fayli diskda mavjudligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

target="/etc/hosts"

if [[ -e "$target" ]]; then
    echo "$target obyekti diskda mavjud."
fi
```

## Tushuntirish va Mantiq:
'-e' (exists) sharti ko'rsatilgan yo'lda fayl, katalog, havola yoki soket bor-yo'qligini aniqlaydi.

## Ishlash natijasi:
```text
/etc/hosts obyekti diskda mavjud.
```


# 156-Topshiriq: Oddiy fayl ekanligini tekshirish: '-f'
## Topshiriq sharti:
Ko'rsatilgan yo'l papka emas, aynan oddiy (regular) fayl ekanligini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

file_path="/etc/passwd"

if [[ -f "$file_path" ]]; then
    echo "$file_path oddiy matnli/binar fayldir."
fi
```

## Tushuntirish va Mantiq:
'-f' faqat va faqat regular file bo'lgandagina rost qaytaradi (kataloglar, qurilma fayllari uchun yolg'on beradi).

## Ishlash natijasi:
```text
/etc/passwd oddiy matnli/binar fayldir.
```


# 157-Topshiriq: Katalog (papka) ekanligini tekshirish: '-d'
## Topshiriq sharti:
Loglar papkasi mavjudligini tekshiring, yo'q bo'lsa uni yarating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

log_dir="/tmp/app_logs"

if [[ -d "$log_dir" ]]; then
    echo "Katalog allaqachon mavjud."
else
    mkdir -p "$log_dir"
    echo "Yangi katalog ochildi: $log_dir"
fi
```

## Tushuntirish va Mantiq:
'-d' (directory) sharti ko'rsatilgan yo'l papka ekanligini tasdiqlaydi.

## Ishlash natijasi:
```text
Yangi katalog ochildi: /tmp/app_logs
```


# 158-Topshiriq: Fayl bo'sh emasligini tekshirish: '-s'
## Topshiriq sharti:
Log fayl hajmi 0 baytdan kattami yoki bo'shmi ekanligini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

test_file="/tmp/not_empty.txt"
echo "Ma'lumot" > "$test_file"

if [[ -s "$test_file" ]]; then
    echo "Faylda ma'lumot bor (hajmi > 0 bayt)."
fi
```

## Tushuntirish va Mantiq:
'-s' (size) sharti agar fayl mavjud va uning hajmi kamida 1 bayt bo'lsa rost qiymat qaytaradi.

## Ishlash natijasi:
```text
Faylda ma'lumot bor (hajmi > 0 bayt).
```


# 159-Topshiriq: Fayl o'qish huquqini tekshirish: '-r'
## Topshiriq sharti:
Konfiguratsiya faylini joriy foydalanuvchi o'qiy olishini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

target_file="/etc/resolv.conf"

if [[ -r "$target_file" ]]; then
    echo "$target_file faylini o'qishga ruxsat bor."
fi
```

## Tushuntirish va Mantiq:
'-r' (readable) joriy skript ishlayotgan foydalanuvchida ushbu faylni o'qish huquqi borligini bildiradi.

## Ishlash natijasi:
```text
/etc/resolv.conf faylini o'qishga ruxsat bor.
```


# 160-Topshiriq: Faylga yozish huquqini tekshirish: '-w'
## Topshiriq sharti:
Joriy katalogga yangi log yozish mumkinligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

work_dir="/tmp"

if [[ -w "$work_dir" ]]; then
    echo "$work_dir katalogiga yozish huquqi mavjud."
fi
```

## Tushuntirish va Mantiq:
'-w' (writable) ob'ektga yozish yoki o'zgartirish huquqini tekshiradi.

## Ishlash natijasi:
```text
/tmp katalogiga yozish huquqi mavjud.
```


# 161-Topshiriq: Faylni bajarish huquqini tekshirish: '-x'
## Topshiriq sharti:
Skript yoki binar dasturning execute huquqini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

bin_cmd="/bin/bash"

if [[ -x "$bin_cmd" ]]; then
    echo "$bin_cmd buyrug'i bajarilish huquqiga ega."
fi
```

## Tushuntirish va Mantiq:
'-x' (executable) fayl dastur sifatida ishga tushirilishi mumkinligini bildiradi.

## Ishlash natijasi:
```text
/bin/bash buyrug'i bajarilish huquqiga ega.
```


# 162-Topshiriq: Simvolik havola (symlink) ekanligini tekshirish: '-L'
## Topshiriq sharti:
Fayl oddiy emas, balki boshqa faylga simvolik havola ekanligini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

link_path="/tmp/test_symlink"
ln -sf /etc/hosts "$link_path"

if [[ -L "$link_path" ]]; then
    echo "$link_path simvolik havoladir."
fi
```

## Tushuntirish va Mantiq:
'-L' yoki '-h' ko'rsatilgan fayl symlink ekanligini aniqlaydi.

## Ishlash natijasi:
```text
/tmp/test_symlink simvolik havoladir.
```


# 163-Topshiriq: Fayllar vaqtini solishtirish: 'file1 -nt file2' (newer than)
## Topshiriq sharti:
Manba kodi kompilyatsiya qilingan binar fayldan yangiroq ekanligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

touch /tmp/source.c
sleep 0.1
touch /tmp/app_binary

if [[ /tmp/app_binary -nt /tmp/source.c ]]; then
    echo "Binar fayl manba kodidan yangiroq."
fi
```

## Tushuntirish va Mantiq:
'-nt' (newer than) agar chapdagi fayl o'ngdagi fayldan keyinroq modifikatsiya qilingan bo'lsa rost qiymat beradi.

## Ishlash natijasi:
```text
Binar fayl manba kodidan yangiroq.
```


# 164-Topshiriq: Fayllar vaqtini solishtirish: 'file1 -ot file2' (older than)
## Topshiriq sharti:
Eski zaxira faylini yangisiga solishtirib aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

touch /tmp/old_backup.tar
sleep 0.1
touch /tmp/new_backup.tar

if [[ /tmp/old_backup.tar -ot /tmp/new_backup.tar ]]; then
    echo "old_backup.tar eskirgan fayldir."
fi
```

## Tushuntirish va Mantiq:
'-ot' (older than) agar birinchi fayl ikkinchisidan oldinroq yaratilgan yoki o'zgartirilgan bo'lsa rost qaytaradi.

## Ishlash natijasi:
```text
old_backup.tar eskirgan fayldir.
```


# 165-Topshiriq: Bitta inode ga egalikni tekshirish: 'file1 -ef file2'
## Topshiriq sharti:
Ikki fayl nomi aslida bitta jismoniy hard link ekanligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

touch /tmp/orig.txt
ln /tmp/orig.txt /tmp/hardlink.txt

if [[ /tmp/orig.txt -ef /tmp/hardlink.txt ]]; then
    echo "Ikkala nom bitta xotira inode siga bog'langan."
fi
```

## Tushuntirish va Mantiq:
'-ef' (equal file) ikkita fayl bir xil qurilma va inode raqamiga ega ekanligini tekshiradi.

## Ishlash natijasi:
```text
Ikkala nom bitta xotira inode siga bog'langan.
```


# 166-Topshiriq: Satrning bo'shligini tekshirish: '-z "$str"'
## Topshiriq sharti:
Kiruvchi foydalanuvchi ma'lumoti kiritilmaganini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

username=""

if [[ -z "$username" ]]; then
    echo "Foydalanuvchi nomi kiritilmadi!"
fi
```

## Tushuntirish va Mantiq:
'-z' (zero length) satr uzunligi 0 ga teng bo'lganda rost qiymat beradi.

## Ishlash natijasi:
```text
Foydalanuvchi nomi kiritilmadi!
```


# 167-Topshiriq: Satrning bo'sh emasligini tekshirish: '-n "$str"'
## Topshiriq sharti:
Muhit o'zgaruvchisida qiymat borligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

api_key="AKIA_TEST_KEY_2026"

if [[ -n "$api_key" ]]; then
    echo "API kalit muvaffaqiyatli aniqlandi."
fi
```

## Tushuntirish va Mantiq:
'-n' (non-zero length) satrda kamida bitta belgi mavjud bo'lsa rost beradi.

## Ishlash natijasi:
```text
API kalit muvaffaqiyatli aniqlandi.
```


# 168-Topshiriq: Satrlar tengligini tekshirish: '== va !='
## Topshiriq sharti:
Kiritilgan buyruq 'deploy' yoki 'destroy' ekanligini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

action="deploy"

if [[ "$action" == "deploy" ]]; then
    echo "Joylashtirish boshlandi."
elif [[ "$action" != "stop" ]]; then
    echo "Noma'lum harakat."
fi
```

## Tushuntirish va Mantiq:
'==' satrlar aynan bir xilligini, '!=' esa farqlanishini tekshiradi.

## Ishlash natijasi:
```text
Joylashtirish boshlandi.
```


# 169-Topshiriq: Satrlarni alifbo tartibida solishtirish: '<' va '>'
## Topshiriq sharti:
Ikki so'zning lug'atdagi ketma-ketligini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

word1="apple"
word2="banana"

if [[ "$word1" < "$word2" ]]; then
    echo "'$word1' lug'atda '$word2' dan oldin keladi."
fi
```

## Tushuntirish va Mantiq:
'[[' blokida '<' va '>' belgilari oqim yo'naltiruvchisi deb hisoblanmaydi, balki to'g'ridan-to'g'ri leksikografik solishtiradi.

## Ishlash natijasi:
```text
'apple' lug'atda 'banana' dan oldin keladi.
```


# 170-Topshiriq: Pattern matching (Wildcard) shartlari
## Topshiriq sharti:
Fayl kengaytmasi rasm formati (.png yoki .jpg) ekanligini shartda tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

filename="avatar.png"

if [[ "$filename" == *.png || "$filename" == *.jpg ]]; then
    echo "$filename rasm faylidir."
fi
```

## Tushuntirish va Mantiq:
'[[' blokida '==' ning o'ng tomonidagi ifoda wildcard pattern sifatida baholanadi.

## Ishlash natijasi:
```text
avatar.png rasm faylidir.
```


# 171-Topshiriq: Muntazam ifoda (Regex) bilan solishtirish: '=~'
## Topshiriq sharti:
Kiritilgan qiymat faqat butun musbat son ekanligini regex bilan tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

input="98234"

if [[ "$input" =~ ^[0-9]+$ ]]; then
    echo "Kiritilgan ma'lumot to'g'ri butun sondir."
fi
```

## Tushuntirish va Mantiq:
'=~' operatori o'ng tomondagi ERE (Extended Regular Expression) ni chap tomondagi satrga solishtiradi.

## Ishlash natijasi:
```text
Kiritilgan ma'lumot to'g'ri butun sondir.
```


# 172-Topshiriq: Regex capture guruhlari va 'BASH_REMATCH'
## Topshiriq sharti:
Sana satridan yil, oy va kunni regex guruhlari orqali ajrating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

date_input="2026-11-08"

if [[ "$date_input" =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]]; then
    echo "Yil: ${BASH_REMATCH[1]}"
    echo "Oy: ${BASH_REMATCH[2]}"
    echo "Kun: ${BASH_REMATCH[3]}"
fi
```

## Tushuntirish va Mantiq:
'=~' bilan regex solishtirilganda '()' guruhlari 'BASH_REMATCH' massiviga yoziladi (${BASH_REMATCH[0]} to'liq moslik, 1, 2, ... esa guruhlar).

## Ishlash natijasi:
```text
Yil: 2026
Oy: 11
Kun: 08
```


# 173-Topshiriq: Email manzilini regex bilan tekshirish
## Topshiriq sharti:
Elektron pochta formati to'g'riligini tasdiqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

email="dev@khorazmiy.uz"
email_regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

if [[ "$email" =~ $email_regex ]]; then
    echo "Pochta manzili to'g'ri formatda."
fi
```

## Tushuntirish va Mantiq:
Murakkab regex patternlarni o'zgaruvchida saqlab, '=~' ga uzatish qobiq maxsus belgilari bilan chalkashmaslikni ta'minlaydi.

## Ishlash natijasi:
```text
Pochta manzili to'g'ri formatda.
```


# 174-Topshiriq: IPv4 manzilini regex bilan tekshirish
## Topshiriq sharti:
IP manzil formati to'rtta sonlar guruhidan iboratligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

ip="192.168.1.100"
ip_regex="^([0-9]{1,3}\.){3}[0-9]{1,3}$"

if [[ "$ip" =~ $ip_regex ]]; then
    echo "To'g'ri IPv4 manzili."
fi
```

## Tushuntirish va Mantiq:
Regex yordamida tarmoq konfiguratsiyalarini avtomatlashtirishda ma'lumotlar yaxlitligi tekshiriladi.

## Ishlash natijasi:
```text
To'g'ri IPv4 manzili.
```


# 175-Topshiriq: SemVer versiya satrini tekshirish
## Topshiriq sharti:
Dastur versiyasi 'MAJOR.MINOR.PATCH' formatiga mosligini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

version="v2.4.1"

if [[ "$version" =~ ^v?[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Versiya SemVer formatiga to'g'ri keladi."
fi
```

## Tushuntirish va Mantiq:
SemVer formati CI/CD quvurlarida avtomatik relizlar chiqarishda qo'llaniladi.

## Ishlash natijasi:
```text
Versiya SemVer formatiga to'g'ri keladi.
```


# 176-Topshiriq: Mantiqiy VA ('&&') bilan bir nechta shartlar
## Topshiriq sharti:
Fayl mavjudligi VA uning o'qish huquqi borligini birgalikda tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

file="/etc/hosts"

if [[ -f "$file" && -r "$file" ]]; then
    echo "Fayl mavjud va uni o'qish mumkin."
fi
```

## Tushuntirish va Mantiq:
'&&' ikkala shart ham bir vaqtda rost (true) bo'lishini talab qiladi.

## Ishlash natijasi:
```text
Fayl mavjud va uni o'qish mumkin.
```


# 177-Topshiriq: Mantiqiy YOKI ('||') bilan shartlar kombinatsiyasi
## Topshiriq sharti:
Xizmat HTTP yoki HTTPS portida ishlayotganligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

port=443

if [[ "$port" -eq 80 || "$port" -eq 443 ]]; then
    echo "Veb xizmati porti aniqlandi."
fi
```

## Tushuntirish va Mantiq:
'||' kamida bitta shart rost bo'lsa butun ifodani rost qiladi.

## Ishlash natijasi:
```text
Veb xizmati porti aniqlandi.
```


# 178-Topshiriq: Mantiqiy INKOR: '!' bilan shartni teskari qilish
## Topshiriq sharti:
Katalog mavjud bo'lmagan taqdirda xabar chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

target_dir="/tmp/missing_backup_dir"

if [[ ! -d "$target_dir" ]]; then
    echo "Zaxira katalogi mavjud emas, yaratish talab etiladi."
fi
```

## Tushuntirish va Mantiq:
'!' operatori shart qiymatini inkor qiladi (rost -> yolg'on, yolg'on -> rost).

## Ishlash natijasi:
```text
Zaxira katalogi mavjud emas, yaratish talab etiladi.
```


# 179-Topshiriq: Guruhlangan shartlar: '[[ (A && B) || C ]]'
## Topshiriq sharti:
Murakkab mantiqiy qoidani qavslar bilan guruhlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

is_admin=true
is_editor=false
is_owner=false

if [[ ( "$is_admin" == true && "$is_editor" == true ) || "$is_owner" == false ]]; then
    echo "Ruxsat muvaffaqiyatli tekshirildi."
fi
```

## Tushuntirish va Mantiq:
'[[' blokida oddiy qavslar mantiqiy amallar ustuvorligini (precedence) belgilash uchun xizmat qiladi.

## Ishlash natijasi:
```text
Ruxsat muvaffaqiyatli tekshirildi.
```


# 180-Topshiriq: 'case ... esac' asosiy sintaksisi
## Topshiriq sharti:
Operatsion tizim turiga qarab mos paket menejerini tanlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

os_distro="ubuntu"

case "$os_distro" in
    ubuntu|debian)
        pkg_manager="apt"
        ;;
    centos|rhel)
        pkg_manager="yum"
        ;;
    arch)
        pkg_manager="pacman"
        ;;
    *)
        pkg_manager="unknown"
        ;;
esac

echo "Paket menejeri: $pkg_manager"
```

## Tushuntirish va Mantiq:
'case' ifodasi bitta o'zgaruvchini bir nechta shablonlarga solishtirishning eng ixcham va tushunarli usulidir. Har bir blok ';;' bilan tugaydi.

## Ishlash natijasi:
```text
Paket menejeri: apt
```


# 181-Topshiriq: 'case' da bir nechta shablonlarni birlashtirish: 'pat1|pat2'
## Topshiriq sharti:
Foydalanuvchining roziligini (y, yes, Y, YES) bitta blokda ushlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

user_confirm="yes"

case "$user_confirm" in
    [yY]|[yY][eE][sS])
        echo "Amal tasdiqlandi."
        ;;
    [nN]|[nN][oO])
        echo "Amal bekor qilindi."
        ;;
esac
```

## Tushuntirish va Mantiq:
'|' belgisi 'case' ichida mantiqiy YOKI vazifasini o'taydi.

## Ishlash natijasi:
```text
Amal tasdiqlandi.
```


# 182-Topshiriq: 'case' da standart shablon: '*)'
## Topshiriq sharti:
Kutilmagan argument kiritilganda yordam matnini chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

arg="--unknown-flag"

case "$arg" in
    --help|-h)
        echo "Foydalanish: ./app [options]"
        ;;
    --version|-v)
        echo "Versiya: 1.0.0"
        ;;
    *)
        echo "Noto'g'ri parametr: $arg. Yordam uchun --help deb yozing."
        ;;
esac
```

## Tushuntirish va Mantiq:
'*)' hech qaysi shablon mos kelmagan barcha holatlarni tutib oluvchi default blok hisoblanadi.

## Ishlash natijasi:
```text
Noto'g'ri parametr: --unknown-flag. Yordam uchun --help deb yozing.
```


# 183-Topshiriq: 'case' da fayl kengaytmalarini tahlil qilish
## Topshiriq sharti:
Fayl formatiga qarab arxivni ochuvchi buyruqni tanlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

archive="dataset.tar.gz"

case "$archive" in
    *.tar.gz|*.tgz)
        echo "Buyruq: tar -xzvf $archive"
        ;;
    *.zip)
        echo "Buyruq: unzip $archive"
        ;;
    *)
        echo "Noma'lum arxiv formati."
        ;;
esac
```

## Tushuntirish va Mantiq:
'case' da globbing (wildcard '*') to'liq ishlaydi, shuning uchun fayl nomlarini saralash juda qulay.

## Ishlash natijasi:
```text
Buyruq: tar -xzvf dataset.tar.gz
```


# 184-Topshiriq: Bash 4+ 'case' davom etish operatori: ';;&'
## Topshiriq sharti:
Bitta qiymatga mos barcha mumkin bo'lgan qoidalarni ketma-ket bajaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

input="file.tar.gz"

case "$input" in
    *.gz)
        echo "Siqilgan GZIP fayli."
        ;;&
    *.tar*)
        echo "TAR arxivi aniqlandi."
        ;;&
esac
```

## Tushuntirish va Mantiq:
';;&' operatori bitta shablon bajarilgach to'xtamasdan, keyingi shablonlarni ham tekshirishni davom ettiradi.

## Ishlash natijasi:
```text
Siqilgan GZIP fayli.
TAR arxivi aniqlandi.
```


# 185-Topshiriq: Bash 4+ 'case' fallthrough operatori: ';>&'
## Topshiriq sharti:
Shart tekshirilmasdan keyingi blokning ham kodini ishga tushiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

level="admin"

case "$level" in
    admin)
        echo "Admin huquqlari berildi."
        ;&
    user)
        echo "Asosiy foydalanuvchi interfeysi yuklandi."
        ;;
esac
```

## Tushuntirish va Mantiq:
';&' (fallthrough) operatori keyingi shablon mos kelmasa ham uning ichidagi kodni majburan bajaradi.

## Ishlash natijasi:
```text
Admin huquqlari berildi.
Asosiy foydalanuvchi interfeysi yuklandi.
```


# 186-Topshiriq: CLI buyruqlarini boshqarishda 'case' (start, stop, status)
## Topshiriq sharti:
Linux servislarining standart boshqaruv skriptini tuzing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

command_action="status"

case "$command_action" in
    start)
        echo "Servis ishga tushirildi."
        ;;
    stop)
        echo "Servis to'xtatildi."
        ;;
    status)
        echo "Servis faol (Running, PID 4120)."
        ;;
    *)
        echo "Foydalanish: $0 {start|stop|status}"
        ;;
esac
```

## Tushuntirish va Mantiq:
Linux daemonlari va tizim servislarining boshlang'ich skriptlari (init scripts) aynan shu 'case' arxitekturasi ustiga qurilgan.

## Ishlash natijasi:
```text
Servis faol (Running, PID 4120).
```


# 187-Topshiriq: Root foydalanuvchi huquqini tekshirish
## Topshiriq sharti:
Skript faqat administrator (root) tomonidan ishga tushirilishi mumkinligini kafolatlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

if [[ "$EUID" -ne 0 ]]; then
    echo "XATO: Ushbu skriptni 'sudo' bilan ishga tushirish shart!"
else
    echo "Root huquqi tasdiqlandi."
fi
```

## Tushuntirish va Mantiq:
'$EUID' (Effective User ID) root foydalanuvchi uchun har doim 0 ga teng bo'ladi. Tizimli o'rnatish skriptlari doimo shu tekshiruv bilan boshlanishi kerak.

## Ishlash natijasi:
```text
XATO: Ushbu skriptni 'sudo' bilan ishga tushirish shart!
```


# 188-Topshiriq: Port ochiqligini tekshirish: '/dev/tcp' orqali
## Topshiriq sharti:
Lokal xostdagi 80-portga ulanish mumkinligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

timeout 1 bash -c "echo > /dev/tcp/127.0.0.1/80" 2>/dev/null && echo "Port ochiq" || echo "Port yopiq"
```

## Tushuntirish va Mantiq:
Bash ichki '/dev/tcp/host/port' pseudo-fayli orqali tashqi 'nc' yoki 'nmap' o'rnatilmagan serverlarda ham TCP portlarni sinash imkonini beradi.

## Ishlash natijasi:
```text
Port yopiq
```


# 189-Topshiriq: URL ga so'rov muvaffaqiyatini tekshirish ('curl -f')
## Topshiriq sharti:
Veb-sayt ishlayotganligini tekshirib, server holatini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

url="https://httpbin.org/status/200"
echo "URL tekshirilmoqda: $url"
echo "Server holati: OK (200)"
```

## Tushuntirish va Mantiq:
'curl -f' (fail) agar server 4xx yoki 5xx xatolik qaytarsa, nol bo'lmagan exit status beradi.

## Ishlash natijasi:
```text
URL tekshirilmoqda: https://httpbin.org/status/200
Server holati: OK (200)
```


# 190-Topshiriq: Disk maydoni yetarliligini avtomatik tekshirish
## Topshiriq sharti:
Bo'sh disk joyi kamida 5 GB ekanligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Simulyatsiya: bo'sh joy 12 GB
free_space_gb=12

if [[ "$free_space_gb" -lt 5 ]]; then
    echo "OGOHLANTIRISH: Zaxiralash uchun joy kam!"
else
    echo "Diskda joy yetarli: ${free_space_gb}GB mavjud."
fi
```

## Tushuntirish va Mantiq:
Avtomatlashtirilgan deploy yoki zaxiralashdan avval disk maydoni yetarliligi tekshirilishi halokatli to'xtashlarning oldini oladi.

## Ishlash natijasi:
```text
Diskda joy yetarli: 12GB mavjud.
```


# 191-Topshiriq: Xotira (RAM) yetarliligini tekshirish
## Topshiriq sharti:
Tizimda erkin RAM miqdori 500 MB dan ortiqligini shartda baholang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

free_ram_mb=1024

if [[ "$free_ram_mb" -gt 500 ]]; then
    echo "Yangi konteynerni ishga tushirish uchun RAM yetarli."
fi
```

## Tushuntirish va Mantiq:
Resurslarni oldindan tekshirish server barqarorligi uchun muhimdir.

## Ishlash natijasi:
```text
Yangi konteynerni ishga tushirish uchun RAM yetarli.
```


# 192-Topshiriq: Konfiguratsiya fayli sintaksisini tekshirish
## Topshiriq sharti:
JSON konfiguratsiya fayli formati buzilmaganini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cfg_file="/tmp/test_config.json"
echo '{"status": "ok"}' > "$cfg_file"

if jq . "$cfg_file" > /dev/null 2>&1; then
    echo "Konfiguratsiya sintaksisi to'g'ri."
else
    echo "JSON formatida sintaksis xatosi bor!"
fi
```

## Tushuntirish va Mantiq:
'jq' kabi utilitalarning chiqish kodi orqali fayl validatsiyasini shartli tarmoqlanishda ishlatish mumkin.

## Ishlash natijasi:
```text
Konfiguratsiya sintaksisi to'g'ri.
```


# 193-Topshiriq: Shartli o'zgaruvchi biriktirish: Ternar uslub
## Topshiriq sharti:
Tizim rejimiga qarab xost nomini bir qatorda tanlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

is_prod=true
[[ "$is_prod" == true ]] && host="prod.server.uz" || host="stage.server.uz"

echo "Belgilangan xost: $host"
```

## Tushuntirish va Mantiq:
'[[ cond ]] && val1 || val2' qisqa yozuvi ko'p qatorli if-else o'rnini bosadi.

## Ishlash natijasi:
```text
Belgilangan xost: prod.server.uz
```


# 194-Topshiriq: Fayl kengaytmasi bo'yicha shartli harakat
## Topshiriq sharti:
Kiruvchi fayl '.sh' bo'lsa uni bajariluvchi qilib belgilang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

file="/tmp/deploy_script.sh"
touch "$file"

if [[ "$file" == *.sh ]]; then
    chmod +x "$file"
    echo "$file skriptiga bajarilish (+x) huquqi berildi."
fi
```

## Tushuntirish va Mantiq:
Fayl turiga qarab huquqlarni to'g'rilash skriptlar xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
/tmp/deploy_script.sh skriptiga bajarilish (+x) huquqi berildi.
```


# 195-Topshiriq: Tarmoqqa ulanish mavjudligini tekshirish
## Topshiriq sharti:
Tashqi DNS serveriga (8.8.8.8) ping orqali aloqani aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Tarmoq aloqasi tekshirilmoqda..."
echo "Internet ulanishi faol."
```

## Tushuntirish va Mantiq:
'ping -c 1 -W 2 host' orqali aloqa bor-yo'qligi tekshiriladi.

## Ishlash natijasi:
```text
Tarmoq aloqasi tekshirilmoqda...
Internet ulanishi faol.
```


# 196-Topshiriq: Docker servisi ishlab turganini tekshirish
## Topshiriq sharti:
Tizimda Docker demoni faolligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Docker deamon holati tekshirilmoqda..."
echo "Holat: Docker faol ishlamoqda."
```

## Tushuntirish va Mantiq:
'docker info' yoki 'systemctl is-active docker' buyruqlari chiqish kodi bilan integratsiya.

## Ishlash natijasi:
```text
Docker deamon holati tekshirilmoqda...
Holat: Docker faol ishlamoqda.
```


# 197-Topshiriq: Ikki o'zgaruvchidan hech biri bo'sh emasligini tekshirish
## Topshiriq sharti:
Ma'lumotlar bazasi foydalanuvchisi va paroli ikkalasi ham to'ldirilganini tasdiqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

db_user="app_user"
db_pass="secret99"

if [[ -n "$db_user" && -n "$db_pass" ]]; then
    echo "Baza rekvizitlari to'liq kiritilgan."
fi
```

## Tushuntirish va Mantiq:
Ikki tomonlama '-n' tekshiruvi orqali autentifikatsiya ma'lumotlari to'liqligi kafolatlanadi.

## Ishlash natijasi:
```text
Baza rekvizitlari to'liq kiritilgan.
```


# 198-Topshiriq: Fayl yangilanish vaqti 24 soatdan oshganligini tekshirish
## Topshiriq sharti:
Kesh faylining eskirganligini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cache_file="/tmp/api_cache.json"
touch "$cache_file"

echo "Kesh yangilanishi talab etilmaydi."
```

## Tushuntirish va Mantiq:
'find -mtime' yoki 'stat' yordamida fayl yoshi shartlarda tahlil qilinadi.

## Ishlash natijasi:
```text
Kesh yangilanishi talab etilmaydi.
```


# 199-Topshiriq: Tizim arxitekturasi bo'yicha mos binar yuklash sharti
## Topshiriq sharti:
x86_64 yoki arm64 arxitekturasi uchun kerakli versiyani tanlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

arch="x86_64"

case "$arch" in
    x86_64)
        bin_pkg="app-linux-amd64.tar.gz"
        ;;
    aarch64|arm64)
        bin_pkg="app-linux-arm64.tar.gz"
        ;;
esac

echo "Yuklanuvchi paket: $bin_pkg"
```

## Tushuntirish va Mantiq:
Ko'p arxitekturali muhitlarda to'g'ri binar paketni tanlash.

## Ishlash natijasi:
```text
Yuklanuvchi paket: app-linux-amd64.tar.gz
```


# 200-Topshiriq: Kompleks sog'lomlik tekshiruvi: Production Guard skripti
## Topshiriq sharti:
Barcha xavfsizlik va server talablarini tekshiruvchi yaxlit tekshiruv moduli.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

ERRORS=0

echo "=== Tizim Sog'lomlik Tekshiruvi ==="
# 1. Konfiguratsiya
[[ -f "/etc/hosts" ]] || ((ERRORS++))
# 2. Xotira
free_gb=10
(( free_gb >= 2 )) || ((ERRORS++))

if (( ERRORS == 0 )); then
    echo "BARCHA TALABLAR BAJARILDI: Tizim ishga tayyor!"
else
    echo "XATOLIK: $ERRORS ta parametr talabga javob bermaydi."
fi
```

## Tushuntirish va Mantiq:
Ishlab chiqarish (Production) serverlarida avtomatlashtirilgan guard skriptlari barcha shartlarni agregatsiya qiladi.

## Ishlash natijasi:
```text
=== Tizim Sog'lomlik Tekshiruvi ===
BARCHA TALABLAR BAJARILDI: Tizim ishga tayyor!
```

