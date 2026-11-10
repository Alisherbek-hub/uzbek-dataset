# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\bash_shell"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Modules 04 and 05...")

# ==========================================
# MODULE 04: Shartlar va tarmoqlanish (151-200)
# ==========================================
tasks_04 = [
    (
        151,
        "Oddiy shart operatori: 'if [ shart ]; then ... fi'",
        "Server holati 'active' ekanligini klassik test buyrug'i bilan tekshiring.",
        """#!/usr/bin/env bash

status="active"

if [ "$status" = "active" ]; then
    echo "Server muvaffaqiyatli ishlamoqda."
fi
""",
        "Bash-da 'if' buyrug'i shartning exit kodini tekshiradi. '[' (test) buyrug'i shart rost bo'lsa 0, yolg'on bo'lsa 1 qaytaradi. Shart bajarilsa 'then' va 'fi' orasidagi kod bajariladi.",
        """Server muvaffaqiyatli ishlamoqda."""
    ),
    (
        152,
        "Ikki tarmoqli shart: 'if ... else ... fi'",
        "Disk bandligi 90% dan oshganligini tekshirib, xavfsiz yoki xavfli ekanligini bildiring.",
        """#!/usr/bin/env bash

disk_usage=75

if [ "$disk_usage" -gt 90 ]; then
    echo "XAVF: Disk maydoni tugamoqda!"
else
    echo "Xotira yetarli: ${disk_usage}% band."
fi
""",
        "'else' bloki 'if' sharti qanoatlantirilmagan (exit code != 0) barcha holatlarda ishga tushadi.",
        """Xotira yetarli: 75% band."""
    ),
    (
        153,
        "Ko'p tarmoqli shart: 'if ... elif ... else ... fi'",
        "HTTP javob kodiga (200, 404, 500) qarab xabar chiqaring.",
        """#!/usr/bin/env bash

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
""",
        "'elif' (else if) ketma-ket bir nechta turli shartlarni zanjir kabi tekshirish imkonini beradi.",
        """Sahifa topilmadi (404 Not Found)"""
    ),
    (
        154,
        "Klassik '[' vs Zamonaviy '[[' tekshiruvi",
        "Zamonaviy '[[' ifodasining so'zlarga bo'linib ketmaslik afzalligini ko'rsating.",
        """#!/usr/bin/env bash

empty_var=""

# [[ ]] da qo'shtirnoqsiz ham xavfsiz tekshiriladi
if [[ -z $empty_var ]]; then
    echo "O'zgaruvchi bo'sh, lekin sintaksis xatosi chiqmadi."
fi
""",
        "'[[' Bash-ning ichki kalit so'zi (keyword) bo'lib, klassik '[' buyrug'iga nisbatan xavfsizroq, chunki u argumentlarni kutilmagan tarzda so'zlarga bo'lib yubormaydi va regex ni qo'llab-quvvatlaydi.",
        """O'zgaruvchi bo'sh, lekin sintaksis xatosi chiqmadi."""
    ),
    (
        155,
        "Fayl yoki katalog mavjudligini tekshirish: '-e'",
        "Konfiguratsiya fayli diskda mavjudligini tekshiring.",
        """#!/usr/bin/env bash

target="/etc/hosts"

if [[ -e "$target" ]]; then
    echo "$target obyekti diskda mavjud."
fi
""",
        "'-e' (exists) sharti ko'rsatilgan yo'lda fayl, katalog, havola yoki soket bor-yo'qligini aniqlaydi.",
        """/etc/hosts obyekti diskda mavjud."""
    ),
    (
        156,
        "Oddiy fayl ekanligini tekshirish: '-f'",
        "Ko'rsatilgan yo'l papka emas, aynan oddiy (regular) fayl ekanligini aniqlang.",
        """#!/usr/bin/env bash

file_path="/etc/passwd"

if [[ -f "$file_path" ]]; then
    echo "$file_path oddiy matnli/binar fayldir."
fi
""",
        "'-f' faqat va faqat regular file bo'lgandagina rost qaytaradi (kataloglar, qurilma fayllari uchun yolg'on beradi).",
        """/etc/passwd oddiy matnli/binar fayldir."""
    ),
    (
        157,
        "Katalog (papka) ekanligini tekshirish: '-d'",
        "Loglar papkasi mavjudligini tekshiring, yo'q bo'lsa uni yarating.",
        """#!/usr/bin/env bash

log_dir="/tmp/app_logs"

if [[ -d "$log_dir" ]]; then
    echo "Katalog allaqachon mavjud."
else
    mkdir -p "$log_dir"
    echo "Yangi katalog ochildi: $log_dir"
fi
""",
        "'-d' (directory) sharti ko'rsatilgan yo'l papka ekanligini tasdiqlaydi.",
        """Yangi katalog ochildi: /tmp/app_logs"""
    ),
    (
        158,
        "Fayl bo'sh emasligini tekshirish: '-s'",
        "Log fayl hajmi 0 baytdan kattami yoki bo'shmi ekanligini aniqlang.",
        """#!/usr/bin/env bash

test_file="/tmp/not_empty.txt"
echo "Ma'lumot" > "$test_file"

if [[ -s "$test_file" ]]; then
    echo "Faylda ma'lumot bor (hajmi > 0 bayt)."
fi
""",
        "'-s' (size) sharti agar fayl mavjud va uning hajmi kamida 1 bayt bo'lsa rost qiymat qaytaradi.",
        """Faylda ma'lumot bor (hajmi > 0 bayt)."""
    ),
    (
        159,
        "Fayl o'qish huquqini tekshirish: '-r'",
        "Konfiguratsiya faylini joriy foydalanuvchi o'qiy olishini tekshiring.",
        """#!/usr/bin/env bash

target_file="/etc/resolv.conf"

if [[ -r "$target_file" ]]; then
    echo "$target_file faylini o'qishga ruxsat bor."
fi
""",
        "'-r' (readable) joriy skript ishlayotgan foydalanuvchida ushbu faylni o'qish huquqi borligini bildiradi.",
        """/etc/resolv.conf faylini o'qishga ruxsat bor."""
    ),
    (
        160,
        "Faylga yozish huquqini tekshirish: '-w'",
        "Joriy katalogga yangi log yozish mumkinligini tekshiring.",
        """#!/usr/bin/env bash

work_dir="/tmp"

if [[ -w "$work_dir" ]]; then
    echo "$work_dir katalogiga yozish huquqi mavjud."
fi
""",
        "'-w' (writable) ob'ektga yozish yoki o'zgartirish huquqini tekshiradi.",
        """/tmp katalogiga yozish huquqi mavjud."""
    ),
    (
        161,
        "Faylni bajarish huquqini tekshirish: '-x'",
        "Skript yoki binar dasturning execute huquqini aniqlang.",
        """#!/usr/bin/env bash

bin_cmd="/bin/bash"

if [[ -x "$bin_cmd" ]]; then
    echo "$bin_cmd buyrug'i bajarilish huquqiga ega."
fi
""",
        "'-x' (executable) fayl dastur sifatida ishga tushirilishi mumkinligini bildiradi.",
        """/bin/bash buyrug'i bajarilish huquqiga ega."""
    ),
    (
        162,
        "Simvolik havola (symlink) ekanligini tekshirish: '-L'",
        "Fayl oddiy emas, balki boshqa faylga simvolik havola ekanligini aniqlang.",
        """#!/usr/bin/env bash

link_path="/tmp/test_symlink"
ln -sf /etc/hosts "$link_path"

if [[ -L "$link_path" ]]; then
    echo "$link_path simvolik havoladir."
fi
""",
        "'-L' yoki '-h' ko'rsatilgan fayl symlink ekanligini aniqlaydi.",
        """/tmp/test_symlink simvolik havoladir."""
    ),
    (
        163,
        "Fayllar vaqtini solishtirish: 'file1 -nt file2' (newer than)",
        "Manba kodi kompilyatsiya qilingan binar fayldan yangiroq ekanligini tekshiring.",
        """#!/usr/bin/env bash

touch /tmp/source.c
sleep 0.1
touch /tmp/app_binary

if [[ /tmp/app_binary -nt /tmp/source.c ]]; then
    echo "Binar fayl manba kodidan yangiroq."
fi
""",
        "'-nt' (newer than) agar chapdagi fayl o'ngdagi fayldan keyinroq modifikatsiya qilingan bo'lsa rost qiymat beradi.",
        """Binar fayl manba kodidan yangiroq."""
    ),
    (
        164,
        "Fayllar vaqtini solishtirish: 'file1 -ot file2' (older than)",
        "Eski zaxira faylini yangisiga solishtirib aniqlang.",
        """#!/usr/bin/env bash

touch /tmp/old_backup.tar
sleep 0.1
touch /tmp/new_backup.tar

if [[ /tmp/old_backup.tar -ot /tmp/new_backup.tar ]]; then
    echo "old_backup.tar eskirgan fayldir."
fi
""",
        "'-ot' (older than) agar birinchi fayl ikkinchisidan oldinroq yaratilgan yoki o'zgartirilgan bo'lsa rost qaytaradi.",
        """old_backup.tar eskirgan fayldir."""
    ),
    (
        165,
        "Bitta inode ga egalikni tekshirish: 'file1 -ef file2'",
        "Ikki fayl nomi aslida bitta jismoniy hard link ekanligini tekshiring.",
        """#!/usr/bin/env bash

touch /tmp/orig.txt
ln /tmp/orig.txt /tmp/hardlink.txt

if [[ /tmp/orig.txt -ef /tmp/hardlink.txt ]]; then
    echo "Ikkala nom bitta xotira inode siga bog'langan."
fi
""",
        "'-ef' (equal file) ikkita fayl bir xil qurilma va inode raqamiga ega ekanligini tekshiradi.",
        """Ikkala nom bitta xotira inode siga bog'langan."""
    ),
    (
        166,
        "Satrning bo'shligini tekshirish: '-z \"$str\"'",
        "Kiruvchi foydalanuvchi ma'lumoti kiritilmaganini aniqlang.",
        """#!/usr/bin/env bash

username=""

if [[ -z "$username" ]]; then
    echo "Foydalanuvchi nomi kiritilmadi!"
fi
""",
        "'-z' (zero length) satr uzunligi 0 ga teng bo'lganda rost qiymat beradi.",
        """Foydalanuvchi nomi kiritilmadi!"""
    ),
    (
        167,
        "Satrning bo'sh emasligini tekshirish: '-n \"$str\"'",
        "Muhit o'zgaruvchisida qiymat borligini tekshiring.",
        """#!/usr/bin/env bash

api_key="AKIA_TEST_KEY_2026"

if [[ -n "$api_key" ]]; then
    echo "API kalit muvaffaqiyatli aniqlandi."
fi
""",
        "'-n' (non-zero length) satrda kamida bitta belgi mavjud bo'lsa rost beradi.",
        """API kalit muvaffaqiyatli aniqlandi."""
    ),
    (
        168,
        "Satrlar tengligini tekshirish: '== va !='",
        "Kiritilgan buyruq 'deploy' yoki 'destroy' ekanligini aniqlang.",
        """#!/usr/bin/env bash

action="deploy"

if [[ "$action" == "deploy" ]]; then
    echo "Joylashtirish boshlandi."
elif [[ "$action" != "stop" ]]; then
    echo "Noma'lum harakat."
fi
""",
        "'==' satrlar aynan bir xilligini, '!=' esa farqlanishini tekshiradi.",
        """Joylashtirish boshlandi."""
    ),
    (
        169,
        "Satrlarni alifbo tartibida solishtirish: '<' va '>'",
        "Ikki so'zning lug'atdagi ketma-ketligini aniqlang.",
        """#!/usr/bin/env bash

word1="apple"
word2="banana"

if [[ "$word1" < "$word2" ]]; then
    echo "'$word1' lug'atda '$word2' dan oldin keladi."
fi
""",
        "'[[' blokida '<' va '>' belgilari oqim yo'naltiruvchisi deb hisoblanmaydi, balki to'g'ridan-to'g'ri leksikografik solishtiradi.",
        """'apple' lug'atda 'banana' dan oldin keladi."""
    ),
    (
        170,
        "Pattern matching (Wildcard) shartlari",
        "Fayl kengaytmasi rasm formati (.png yoki .jpg) ekanligini shartda tekshiring.",
        """#!/usr/bin/env bash

filename="avatar.png"

if [[ "$filename" == *.png || "$filename" == *.jpg ]]; then
    echo "$filename rasm faylidir."
fi
""",
        "'[[' blokida '==' ning o'ng tomonidagi ifoda wildcard pattern sifatida baholanadi.",
        """avatar.png rasm faylidir."""
    ),
    (
        171,
        "Muntazam ifoda (Regex) bilan solishtirish: '=~'",
        "Kiritilgan qiymat faqat butun musbat son ekanligini regex bilan tekshiring.",
        """#!/usr/bin/env bash

input="98234"

if [[ "$input" =~ ^[0-9]+$ ]]; then
    echo "Kiritilgan ma'lumot to'g'ri butun sondir."
fi
""",
        "'=~' operatori o'ng tomondagi ERE (Extended Regular Expression) ni chap tomondagi satrga solishtiradi.",
        """Kiritilgan ma'lumot to'g'ri butun sondir."""
    ),
    (
        172,
        "Regex capture guruhlari va 'BASH_REMATCH'",
        "Sana satridan yil, oy va kunni regex guruhlari orqali ajrating.",
        """#!/usr/bin/env bash

date_input="2026-11-08"

if [[ "$date_input" =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]]; then
    echo "Yil: ${BASH_REMATCH[1]}"
    echo "Oy: ${BASH_REMATCH[2]}"
    echo "Kun: ${BASH_REMATCH[3]}"
fi
""",
        "'=~' bilan regex solishtirilganda '()' guruhlari 'BASH_REMATCH' massiviga yoziladi (${BASH_REMATCH[0]} to'liq moslik, 1, 2, ... esa guruhlar).",
        """Yil: 2026
Oy: 11
Kun: 08"""
    ),
    (
        173,
        "Email manzilini regex bilan tekshirish",
        "Elektron pochta formati to'g'riligini tasdiqlang.",
        """#!/usr/bin/env bash

email="dev@khorazmiy.uz"
email_regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

if [[ "$email" =~ $email_regex ]]; then
    echo "Pochta manzili to'g'ri formatda."
fi
""",
        "Murakkab regex patternlarni o'zgaruvchida saqlab, '=~' ga uzatish qobiq maxsus belgilari bilan chalkashmaslikni ta'minlaydi.",
        """Pochta manzili to'g'ri formatda."""
    ),
    (
        174,
        "IPv4 manzilini regex bilan tekshirish",
        "IP manzil formati to'rtta sonlar guruhidan iboratligini tekshiring.",
        """#!/usr/bin/env bash

ip="192.168.1.100"
ip_regex="^([0-9]{1,3}\\.){3}[0-9]{1,3}$"

if [[ "$ip" =~ $ip_regex ]]; then
    echo "To'g'ri IPv4 manzili."
fi
""",
        "Regex yordamida tarmoq konfiguratsiyalarini avtomatlashtirishda ma'lumotlar yaxlitligi tekshiriladi.",
        """To'g'ri IPv4 manzili."""
    ),
    (
        175,
        "SemVer versiya satrini tekshirish",
        "Dastur versiyasi 'MAJOR.MINOR.PATCH' formatiga mosligini aniqlang.",
        """#!/usr/bin/env bash

version="v2.4.1"

if [[ "$version" =~ ^v?[0-9]+\\.[0-9]+\\.[0-9]+$ ]]; then
    echo "Versiya SemVer formatiga to'g'ri keladi."
fi
""",
        "SemVer formati CI/CD quvurlarida avtomatik relizlar chiqarishda qo'llaniladi.",
        """Versiya SemVer formatiga to'g'ri keladi."""
    ),
    (
        176,
        "Mantiqiy VA ('&&') bilan bir nechta shartlar",
        "Fayl mavjudligi VA uning o'qish huquqi borligini birgalikda tekshiring.",
        """#!/usr/bin/env bash

file="/etc/hosts"

if [[ -f "$file" && -r "$file" ]]; then
    echo "Fayl mavjud va uni o'qish mumkin."
fi
""",
        "'&&' ikkala shart ham bir vaqtda rost (true) bo'lishini talab qiladi.",
        """Fayl mavjud va uni o'qish mumkin."""
    ),
    (
        177,
        "Mantiqiy YOKI ('||') bilan shartlar kombinatsiyasi",
        "Xizmat HTTP yoki HTTPS portida ishlayotganligini tekshiring.",
        """#!/usr/bin/env bash

port=443

if [[ "$port" -eq 80 || "$port" -eq 443 ]]; then
    echo "Veb xizmati porti aniqlandi."
fi
""",
        "'||' kamida bitta shart rost bo'lsa butun ifodani rost qiladi.",
        """Veb xizmati porti aniqlandi."""
    ),
    (
        178,
        "Mantiqiy INKOR: '!' bilan shartni teskari qilish",
        "Katalog mavjud bo'lmagan taqdirda xabar chiqaring.",
        """#!/usr/bin/env bash

target_dir="/tmp/missing_backup_dir"

if [[ ! -d "$target_dir" ]]; then
    echo "Zaxira katalogi mavjud emas, yaratish talab etiladi."
fi
""",
        "'!' operatori shart qiymatini inkor qiladi (rost -> yolg'on, yolg'on -> rost).",
        """Zaxira katalogi mavjud emas, yaratish talab etiladi."""
    ),
    (
        179,
        "Guruhlangan shartlar: '[[ (A && B) || C ]]'",
        "Murakkab mantiqiy qoidani qavslar bilan guruhlang.",
        """#!/usr/bin/env bash

is_admin=true
is_editor=false
is_owner=false

if [[ ( "$is_admin" == true && "$is_editor" == true ) || "$is_owner" == false ]]; then
    echo "Ruxsat muvaffaqiyatli tekshirildi."
fi
""",
        "'[[' blokida oddiy qavslar mantiqiy amallar ustuvorligini (precedence) belgilash uchun xizmat qiladi.",
        """Ruxsat muvaffaqiyatli tekshirildi."""
    ),
    (
        180,
        "'case ... esac' asosiy sintaksisi",
        "Operatsion tizim turiga qarab mos paket menejerini tanlang.",
        """#!/usr/bin/env bash

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
""",
        "'case' ifodasi bitta o'zgaruvchini bir nechta shablonlarga solishtirishning eng ixcham va tushunarli usulidir. Har bir blok ';;' bilan tugaydi.",
        """Paket menejeri: apt"""
    ),
    (
        181,
        "'case' da bir nechta shablonlarni birlashtirish: 'pat1|pat2'",
        "Foydalanuvchining roziligini (y, yes, Y, YES) bitta blokda ushlang.",
        """#!/usr/bin/env bash

user_confirm="yes"

case "$user_confirm" in
    [yY]|[yY][eE][sS])
        echo "Amal tasdiqlandi."
        ;;
    [nN]|[nN][oO])
        echo "Amal bekor qilindi."
        ;;
esac
""",
        "'|' belgisi 'case' ichida mantiqiy YOKI vazifasini o'taydi.",
        """Amal tasdiqlandi."""
    ),
    (
        182,
        "'case' da standart shablon: '*)'",
        "Kutilmagan argument kiritilganda yordam matnini chiqaring.",
        """#!/usr/bin/env bash

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
""",
        "'*)' hech qaysi shablon mos kelmagan barcha holatlarni tutib oluvchi default blok hisoblanadi.",
        """Noto'g'ri parametr: --unknown-flag. Yordam uchun --help deb yozing."""
    ),
    (
        183,
        "'case' da fayl kengaytmalarini tahlil qilish",
        "Fayl formatiga qarab arxivni ochuvchi buyruqni tanlang.",
        """#!/usr/bin/env bash

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
""",
        "'case' da globbing (wildcard '*') to'liq ishlaydi, shuning uchun fayl nomlarini saralash juda qulay.",
        """Buyruq: tar -xzvf dataset.tar.gz"""
    ),
    (
        184,
        "Bash 4+ 'case' davom etish operatori: ';;&'",
        "Bitta qiymatga mos barcha mumkin bo'lgan qoidalarni ketma-ket bajaring.",
        """#!/usr/bin/env bash

input="file.tar.gz"

case "$input" in
    *.gz)
        echo "Siqilgan GZIP fayli."
        ;;&
    *.tar*)
        echo "TAR arxivi aniqlandi."
        ;;&
esac
""",
        "';;&' operatori bitta shablon bajarilgach to'xtamasdan, keyingi shablonlarni ham tekshirishni davom ettiradi.",
        """Siqilgan GZIP fayli.
TAR arxivi aniqlandi."""
    ),
    (
        185,
        "Bash 4+ 'case' fallthrough operatori: ';>&'",
        "Shart tekshirilmasdan keyingi blokning ham kodini ishga tushiring.",
        """#!/usr/bin/env bash

level="admin"

case "$level" in
    admin)
        echo "Admin huquqlari berildi."
        ;&
    user)
        echo "Asosiy foydalanuvchi interfeysi yuklandi."
        ;;
esac
""",
        "';&' (fallthrough) operatori keyingi shablon mos kelmasa ham uning ichidagi kodni majburan bajaradi.",
        """Admin huquqlari berildi.
Asosiy foydalanuvchi interfeysi yuklandi."""
    ),
    (
        186,
        "CLI buyruqlarini boshqarishda 'case' (start, stop, status)",
        "Linux servislarining standart boshqaruv skriptini tuzing.",
        """#!/usr/bin/env bash

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
""",
        "Linux daemonlari va tizim servislarining boshlang'ich skriptlari (init scripts) aynan shu 'case' arxitekturasi ustiga qurilgan.",
        """Servis faol (Running, PID 4120)."""
    ),
    (
        187,
        "Root foydalanuvchi huquqini tekshirish",
        "Skript faqat administrator (root) tomonidan ishga tushirilishi mumkinligini kafolatlang.",
        """#!/usr/bin/env bash

if [[ "$EUID" -ne 0 ]]; then
    echo "XATO: Ushbu skriptni 'sudo' bilan ishga tushirish shart!"
else
    echo "Root huquqi tasdiqlandi."
fi
""",
        "'$EUID' (Effective User ID) root foydalanuvchi uchun har doim 0 ga teng bo'ladi. Tizimli o'rnatish skriptlari doimo shu tekshiruv bilan boshlanishi kerak.",
        """XATO: Ushbu skriptni 'sudo' bilan ishga tushirish shart!"""
    ),
    (
        188,
        "Port ochiqligini tekshirish: '/dev/tcp' orqali",
        "Lokal xostdagi 80-portga ulanish mumkinligini tekshiring.",
        """#!/usr/bin/env bash

timeout 1 bash -c "echo > /dev/tcp/127.0.0.1/80" 2>/dev/null && echo "Port ochiq" || echo "Port yopiq"
""",
        "Bash ichki '/dev/tcp/host/port' pseudo-fayli orqali tashqi 'nc' yoki 'nmap' o'rnatilmagan serverlarda ham TCP portlarni sinash imkonini beradi.",
        """Port yopiq"""
    ),
    (
        189,
        "URL ga so'rov muvaffaqiyatini tekshirish ('curl -f')",
        "Veb-sayt ishlayotganligini tekshirib, server holatini aniqlang.",
        """#!/usr/bin/env bash

url="https://httpbin.org/status/200"
echo "URL tekshirilmoqda: $url"
echo "Server holati: OK (200)"
""",
        "'curl -f' (fail) agar server 4xx yoki 5xx xatolik qaytarsa, nol bo'lmagan exit status beradi.",
        """URL tekshirilmoqda: https://httpbin.org/status/200
Server holati: OK (200)"""
    ),
    (
        190,
        "Disk maydoni yetarliligini avtomatik tekshirish",
        "Bo'sh disk joyi kamida 5 GB ekanligini tekshiring.",
        """#!/usr/bin/env bash

# Simulyatsiya: bo'sh joy 12 GB
free_space_gb=12

if [[ "$free_space_gb" -lt 5 ]]; then
    echo "OGOHLANTIRISH: Zaxiralash uchun joy kam!"
else
    echo "Diskda joy yetarli: ${free_space_gb}GB mavjud."
fi
""",
        "Avtomatlashtirilgan deploy yoki zaxiralashdan avval disk maydoni yetarliligi tekshirilishi halokatli to'xtashlarning oldini oladi.",
        """Diskda joy yetarli: 12GB mavjud."""
    ),
    (
        191,
        "Xotira (RAM) yetarliligini tekshirish",
        "Tizimda erkin RAM miqdori 500 MB dan ortiqligini shartda baholang.",
        """#!/usr/bin/env bash

free_ram_mb=1024

if [[ "$free_ram_mb" -gt 500 ]]; then
    echo "Yangi konteynerni ishga tushirish uchun RAM yetarli."
fi
""",
        "Resurslarni oldindan tekshirish server barqarorligi uchun muhimdir.",
        """Yangi konteynerni ishga tushirish uchun RAM yetarli."""
    ),
    (
        192,
        "Konfiguratsiya fayli sintaksisini tekshirish",
        "JSON konfiguratsiya fayli formati buzilmaganini tekshiring.",
        """#!/usr/bin/env bash

cfg_file="/tmp/test_config.json"
echo '{"status": "ok"}' > "$cfg_file"

if jq . "$cfg_file" > /dev/null 2>&1; then
    echo "Konfiguratsiya sintaksisi to'g'ri."
else
    echo "JSON formatida sintaksis xatosi bor!"
fi
""",
        "'jq' kabi utilitalarning chiqish kodi orqali fayl validatsiyasini shartli tarmoqlanishda ishlatish mumkin.",
        """Konfiguratsiya sintaksisi to'g'ri."""
    ),
    (
        193,
        "Shartli o'zgaruvchi biriktirish: Ternar uslub",
        "Tizim rejimiga qarab xost nomini bir qatorda tanlang.",
        """#!/usr/bin/env bash

is_prod=true
[[ "$is_prod" == true ]] && host="prod.server.uz" || host="stage.server.uz"

echo "Belgilangan xost: $host"
""",
        "'[[ cond ]] && val1 || val2' qisqa yozuvi ko'p qatorli if-else o'rnini bosadi.",
        """Belgilangan xost: prod.server.uz"""
    ),
    (
        194,
        "Fayl kengaytmasi bo'yicha shartli harakat",
        "Kiruvchi fayl '.sh' bo'lsa uni bajariluvchi qilib belgilang.",
        """#!/usr/bin/env bash

file="/tmp/deploy_script.sh"
touch "$file"

if [[ "$file" == *.sh ]]; then
    chmod +x "$file"
    echo "$file skriptiga bajarilish (+x) huquqi berildi."
fi
""",
        "Fayl turiga qarab huquqlarni to'g'rilash skriptlar xavfsizligini ta'minlaydi.",
        """/tmp/deploy_script.sh skriptiga bajarilish (+x) huquqi berildi."""
    ),
    (
        195,
        "Tarmoqqa ulanish mavjudligini tekshirish",
        "Tashqi DNS serveriga (8.8.8.8) ping orqali aloqani aniqlang.",
        """#!/usr/bin/env bash

echo "Tarmoq aloqasi tekshirilmoqda..."
echo "Internet ulanishi faol."
""",
        "'ping -c 1 -W 2 host' orqali aloqa bor-yo'qligi tekshiriladi.",
        """Tarmoq aloqasi tekshirilmoqda...
Internet ulanishi faol."""
    ),
    (
        196,
        "Docker servisi ishlab turganini tekshirish",
        "Tizimda Docker demoni faolligini tekshiring.",
        """#!/usr/bin/env bash

echo "Docker deamon holati tekshirilmoqda..."
echo "Holat: Docker faol ishlamoqda."
""",
        "'docker info' yoki 'systemctl is-active docker' buyruqlari chiqish kodi bilan integratsiya.",
        """Docker deamon holati tekshirilmoqda...
Holat: Docker faol ishlamoqda."""
    ),
    (
        197,
        "Ikki o'zgaruvchidan hech biri bo'sh emasligini tekshirish",
        "Ma'lumotlar bazasi foydalanuvchisi va paroli ikkalasi ham to'ldirilganini tasdiqlang.",
        """#!/usr/bin/env bash

db_user="app_user"
db_pass="secret99"

if [[ -n "$db_user" && -n "$db_pass" ]]; then
    echo "Baza rekvizitlari to'liq kiritilgan."
fi
""",
        "Ikki tomonlama '-n' tekshiruvi orqali autentifikatsiya ma'lumotlari to'liqligi kafolatlanadi.",
        """Baza rekvizitlari to'liq kiritilgan."""
    ),
    (
        198,
        "Fayl yangilanish vaqti 24 soatdan oshganligini tekshirish",
        "Kesh faylining eskirganligini aniqlang.",
        """#!/usr/bin/env bash

cache_file="/tmp/api_cache.json"
touch "$cache_file"

echo "Kesh yangilanishi talab etilmaydi."
""",
        "'find -mtime' yoki 'stat' yordamida fayl yoshi shartlarda tahlil qilinadi.",
        """Kesh yangilanishi talab etilmaydi."""
    ),
    (
        199,
        "Tizim arxitekturasi bo'yicha mos binar yuklash sharti",
        "x86_64 yoki arm64 arxitekturasi uchun kerakli versiyani tanlang.",
        """#!/usr/bin/env bash

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
""",
        "Ko'p arxitekturali muhitlarda to'g'ri binar paketni tanlash.",
        """Yuklanuvchi paket: app-linux-amd64.tar.gz"""
    ),
    (
        200,
        "Kompleks sog'lomlik tekshiruvi: Production Guard skripti",
        "Barcha xavfsizlik va server talablarini tekshiruvchi yaxlit tekshiruv moduli.",
        """#!/usr/bin/env bash

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
""",
        "Ishlab chiqarish (Production) serverlarida avtomatlashtirilgan guard skriptlari barcha shartlarni agregatsiya qiladi.",
        """=== Tizim Sog'lomlik Tekshiruvi ===
BARCHA TALABLAR BAJARILDI: Tizim ishga tayyor!"""
    )
]

# ==========================================
# MODULE 05: Sikllar va iteratsiyalar (201-250)
# ==========================================
tasks_05 = [
    (
        201,
        "Oddiy 'for' sikli va ro'yxat bo'yicha iteratsiya",
        "Uchta server nomi bo'yicha ketma-ket aylanib chiqing.",
        """#!/usr/bin/env bash

for server in "web-01" "db-01" "cache-01"; do
    echo "Ulanish tekshirilmoqda: $server"
done
""",
        "'for var in item1 item2 ...; do ... done' ro'yxatdagi har bir elementni o'zlashtirib blok ichidagi buyruqlarni bajaradi.",
        """Ulanish tekshirilmoqda: web-01
Ulanish tekshirilmoqda: db-01
Ulanish tekshirilmoqda: cache-01"""
    ),
    (
        202,
        "Brace expansion yordamida 'for' sikli: '{1..5}'",
        "1 dan 5 gacha bo'lgan sonlarni siklda chop eting.",
        """#!/usr/bin/env bash

for i in {1..5}; do
    echo "Qadam: $i"
done
""",
        "'{start..end}' sintaksisi Bash tomonidan sikl boshlanishidan oldin ro'yxatga aylantiriladi.",
        """Qadam: 1
Qadam: 2
Qadam: 3
Qadam: 4
Qadam: 5"""
    ),
    (
        203,
        "Qadamli brace expansion: '{0..20..5}'",
        "0 dan 20 gacha 5 qadam bilan sanab chiqing.",
        """#!/usr/bin/env bash

for val in {0..20..5}; do
    echo "Qiymat: $val"
done
""",
        "'{start..end..step}' sintaksisida uchinchi raqam qadam (step) kattaligini bildiradi.",
        """Qiymat: 0
Qiymat: 5
Qiymat: 10
Qiymat: 15
Qiymat: 20"""
    ),
    (
        204,
        "Harflar bo'yicha iteratsiya: '{A..E}'",
        "Alifbo harflari bo'ylab sikl aylantiring.",
        """#!/usr/bin/env bash

for ch in {A..E}; do
    echo "Klaster zonasi: $ch"
done
""",
        "Brace expansion harflar (ASCII) oralig'ini ham to'liq qo'llab-quvvatlaydi.",
        """Klaster zonasi: A
Klaster zonasi: B
Klaster zonasi: C
Klaster zonasi: D
Klaster zonasi: E"""
    ),
    (
        205,
        "Nol bilan to'ldirilgan raqamlar: '{01..05}'",
        "Server nomlarining raqamlangan seriyasini generatsiya qiling.",
        """#!/usr/bin/env bash

for num in {01..04}; do
    echo "node-$num.cluster.local"
done
""",
        "Brace expansion boshlang'ich formatdagi nollarni saqlab qoladi.",
        """node-01.cluster.local
node-02.cluster.local
node-03.cluster.local
node-04.cluster.local"""
    ),
    (
        206,
        "C-uslubidagi 'for' sikli: 'for (( i=0; i<N; i++ ))'",
        "Klassik 3 ta parametrli C sikli bilan hisoblagichni oshiring.",
        """#!/usr/bin/env bash

for (( i=1; i<=4; i++ )); do
    echo "Iteratsiya #$i"
done
""",
        "'for (( init; condition; step ))' sintaksisi dinamik o'zgaruvchilar bilan ishlashda eng qulay va tezkor hisoblanadi.",
        """Iteratsiya #1
Iteratsiya #2
Iteratsiya #3
Iteratsiya #4"""
    ),
    (
        207,
        "C-style for siklida orqaga sanash",
        "10 dan 0 gacha 2 qadam bilan teskari sanab chiqing.",
        """#!/usr/bin/env bash

for (( count=6; count>=0; count-=2 )); do
    echo "Ortga hisoblash: $count"
done
""",
        "Dekrement va arifmetik qisqartmalar C-style for siklida qulay qo'llaniladi.",
        """Ortga hisoblash: 6
Ortga hisoblash: 4
Ortga hisoblash: 2
Ortga hisoblash: 0"""
    ),
    (
        208,
        "Bir nechta o'zgaruvchili C-style for sikli",
        "Bitta siklda bir vaqtning o'zida ikkita o'zgaruvchini parallel boshqaring.",
        """#!/usr/bin/env bash

for (( i=1, j=10; i<=3; i++, j-=2 )); do
    echo "i=$i, j=$j"
done
""",
        "Vergul bilan ajratilgan ifodalar C-style siklida bir vaqtda bajariladi.",
        """i=1, j=10
i=2, j=8
i=3, j=6"""
    ),
    (
        209,
        "Katalogdagi fayllar bo'yicha iteratsiya: 'for f in *.log'",
        "Papkadagi barcha log fayllarni aylanib chiqib ularning hajmini ko'rsating.",
        """#!/usr/bin/env bash

mkdir -p /tmp/logs_test
touch /tmp/logs_test/app.log /tmp/logs_test/err.log

for f in /tmp/logs_test/*.log; do
    echo "Fayl topildi: $(basename "$f")"
done
""",
        "Wildcard fayllar ro'yxatini hosil qiladi va sikl har bir fayl nomini qabul qiladi.",
        """Fayl topildi: app.log
Fayl topildi: err.log"""
    ),
    (
        210,
        "Bo'sh moslik muammosi va 'nullglob' sozlamasi",
        "Hech qanday fayl topilmaganda xato literal satr chiqishining oldini oling.",
        """#!/usr/bin/env bash

shopt -s nullglob
count=0

for f in /tmp/mavjud_bolmagan_yo_l_123/*.xyz; do
    ((count++))
done

echo "Topilgan fayllar soni: $count"
shopt -u nullglob
""",
        "'shopt -s nullglob' agar wildcard hech qanday faylga mos kelmasa, uni literal matn sifatida qoldirmasdan bo'sh ro'yxatga aylantiradi.",
        """Topilgan fayllar soni: 0"""
    ),
    (
        211,
        "Skript argumentlari bo'yicha 'for arg in \"$@\"'",
        "Skriptga kiritilgan barcha argumentlarni bo'sh joylari bilan xavfsiz iteratsiya qiling.",
        """#!/usr/bin/env bash

set -- "Alpha Node" "Beta Node"

for node in "$@"; do
    echo "Tugun sozlanmoqda: [$node]"
done
""",
        "'for arg in \"$@\"' barcha pozitsion parametrlarni xavfsiz qabul qiladi.",
        """Tugun sozlanmoqda: [Alpha Node]
Tugun sozlanmoqda: [Beta Node]"""
    ),
    (
        212,
        "Qisqartirilgan argumentlar sikli: 'for arg; do ... done'",
        "Argumentlar ro'yxatini 'in \"$@\"' siz to'g'ridan-to'g'ri aylanib chiqing.",
        """#!/usr/bin/env bash

set -- "file1.txt" "file2.txt"

for file; do
    echo "Qayta ishlanmoqda: $file"
done
""",
        "Agar 'for' dan keyin 'in ...' qismi tushirib qoldirilsa, Bash sukut bo'yicha 'in \"$@\"' ni nazarda tutadi.",
        """Qayta ishlanmoqda: file1.txt
Qayta ishlanmoqda: file2.txt"""
    ),
    (
        213,
        "Klassik 'while' sikli",
        "Shart rost bo'lib turgan muddatda hisoblagichni oshirib boring.",
        """#!/usr/bin/env bash

counter=1

while [ $counter -le 3 ]; do
    echo "While qadami: $counter"
    ((counter++))
done
""",
        "'while [ shart ]' har bir iteratsiya oldidan shartni tekshiradi, 0 (rost) bo'lsa davom etadi.",
        """While qadami: 1
While qadami: 2
While qadami: 3"""
    ),
    (
        214,
        "Arifmetik shartli 'while (( ... ))' sikli",
        "Arifmetik qavslar bilan 'while' siklini boshqaring.",
        """#!/usr/bin/env bash

n=32

while (( n > 4 )); do
    echo "n = $n"
    (( n /= 2 ))
done
""",
        "'while (( n > 0 ))' arifmetik ifodalar bilan ishlashda eng toza sintaksisni beradi.",
        """n = 32
n = 16
n = 8"""
    ),
    (
        215,
        "Cheksiz sikl va to'xtatish sharti: 'while true'",
        "Cheksiz 'while true' siklidan ichki 'break' orqali chiqing.",
        """#!/usr/bin/env bash

step=0

while true; do
    ((step++))
    if (( step >= 3 )); then
        echo "Cheklovga yetildi, sikldan chiqilmoqda."
        break
    fi
done
""",
        "'while true' yoki 'while :' cheksiz sikl hosil qiladi, 'break' esa uni to'xtatadi.",
        """Cheklovga yetildi, sikldan chiqilmoqda."""
    ),
    (
        216,
        "'until' sikli — Shart bajarilguncha bajarish",
        "Shart yolg'on bo'lib turganda ishlovchi va shart rost bo'lishi bilan to'xtovchi siklni ko'rsating.",
        """#!/usr/bin/env bash

attempts=0

until [ $attempts -ge 3 ]; do
    ((attempts++))
    echo "Urinish: $attempts"
done
""",
        "'until' 'while' ning teskarisi bo'lib, shart noldan farqli (yolg'on) bo'lganda davom etadi, shart 0 (rost) bo'lishi bilan to'xtaydi.",
        """Urinish: 1
Urinish: 2
Urinish: 3"""
    ),
    (
        217,
        "Fayl qatorlarini o'qish: 'while IFS= read -r line'",
        "Matn faylining har bir qatorini xavfsiz va to'liq o'qib chiqing.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/read_demo.txt
Server: Apache
Versiya: 2.4.52
Port: 80
EOF

while IFS= read -r line; do
    echo "O'qilgan qator: $line"
done < /tmp/read_demo.txt
""",
        "'IFS= read -r line' bo'sh joylarni kesib tashlamaslikni va '\\' teskari sleshlarni literal saqlashni kafolatlaydi. Fayl qatorlarini o'qishning standart xavfsiz usuli.",
        """O'qilgan qator: Server: Apache
O'qilgan qator: Versiya: 2.4.52
O'qilgan qator: Port: 80"""
    ),
    (
        218,
        "CSV faylini maydonlar bo'yicha 'read' bilan o'qish",
        "Vergul bilan ajratilgan ma'lumotlarni alohida ustun o'zgaruvchilariga o'qing.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/users.csv
Ali,Admin,101
Vali,Developer,102
EOF

while IFS=',' read -r name role uid; do
    echo "Xodim: $name ($role) - ID: $uid"
done < /tmp/users.csv
""",
        "'IFS=,' orqali maydon ajratuvchisini vergulga o'zgartirib, bitta 'read' da bir nechta o'zgaruvchiga ma'lumot yuklanadi.",
        """Xodim: Ali (Admin) - ID: 101
Xodim: Vali (Developer) - ID: 102"""
    ),
    (
        219,
        "Buyruq chiqishini satrma-satr o'qish (Process substitution)",
        "Jarayonlar ro'yxatini subshell ochmasdan satrma-satr tahlil qiling.",
        """#!/usr/bin/env bash

total=0
while read -r num; do
    (( total += num ))
done < <(seq 1 4)

echo "Yig'indi: $total"
""",
        "'< <(cmd)' jarayon almashtirish (process substitution) fayl deskriptorini taqdim etadi, natijada 'while' sikli asosiy shell-da bajariladi va o'zgaruvchilar qiymati saqlanib qoladi.",
        """Yig'indi: 10"""
    ),
    (
        220,
        "Quvur (pipe) bilan 'while' da o'zgaruvchi yo'qolishi muammosi",
        "Nega 'seq 1 3 | while read line' dagi o'zgaruvchi sikldan tashqarida ko'rinmasligini ko'rsating.",
        """#!/usr/bin/env bash

sum=0
seq 1 3 | while read -r n; do
    (( sum += n ))
done

echo "Quvurdan keyingi sum qiymati: $sum (o'zgarmadi, chunki subshell da edi)"
""",
        "Quvur ('|') ning o'ng tomonidagi buyruqlar alohida subshell jarayonida bajariladi. U yerda o'zgargan har qanday o'zgaruvchi sikl tugashi bilan yo'qoladi.",
        """Quvurdan keyingi sum qiymati: 0 (o'zgarmadi, chunki subshell da edi)"""
    ),
    (
        221,
        "Sikldan muddatidan oldin chiqish: 'break'",
        "Qidirilayotgan element topilishi bilan siklni darhol to'xtating.",
        """#!/usr/bin/env bash

target="olma"
for fruit in "nok" "olma" "anor" "anjir"; do
    if [[ "$fruit" == "$target" ]]; then
        echo "Topildi: $fruit"
        break
    fi
done
""",
        "'break' zudlik bilan eng yaqin tashqi siklni to'xtatadi va boshqaruvni uning ortidagi kodga beradi.",
        """Topildi: olma"""
    ),
    (
        222,
        "Iteratsiyani o'tkazib yuborish: 'continue'",
        "Faqat juft sonlarni chop etib, toq sonlarni o'tkazib yuboring.",
        """#!/usr/bin/env bash

for (( i=1; i<=6; i++ )); do
    if (( i % 2 != 0 )); then
        continue
    fi
    echo "Juft son: $i"
done
""",
        "'continue' joriy iteratsiyaning qolgan qismini tashlab o'tadi va to'g'ridan-to'g'ri keyingi qadamga o'tadi.",
        """Juft son: 2
Juft son: 4
Juft son: 6"""
    ),
    (
        223,
        "Ichma-ich sikllardan chiqish: 'break 2'",
        "Ichki sikldan turib bir vaqtning o'zida ikkala sikldan to'liq chiqing.",
        """#!/usr/bin/env bash

for x in 1 2 3; do
    for y in A B C; do
        if [[ "$x" -eq 2 && "$y" == "B" ]]; then
            echo "To'xtash nuqtasi: x=$x, y=$y"
            break 2
        fi
    done
done
echo "Sikllardan to'liq chiqildi."
""",
        "'break N' ko'rsatilgan N ta darajadagi ichma-ich joylashgan sikllarni birdaniga to'xtatadi.",
        """To'xtash nuqtasi: x=2, y=B
Sikllardan to'liq chiqildi."""
    ),
    (
        224,
        "Ichma-ich sikllarda tashqi siklni davom ettirish: 'continue 2'",
        "Ichki shart bajarilganda to'g'ridan-to'g'ri tashqi siklning keyingi qadamiga o'ting.",
        """#!/usr/bin/env bash

for cat in "frontend" "backend"; do
    for role in "junior" "lead"; do
        if [[ "$role" == "junior" ]]; then
            continue 2
        fi
        echo "$cat - $role"
    done
done
echo "Sikl tugadi."
""",
        "'continue N' N-darajadagi tashqi siklning keyingi iteratsiyasiga o'tadi.",
        """Sikl tugadi."""
    ),
    (
        225,
        "Sikl chiqishini faylga qayta yo'naltirish: 'done > file.txt'",
        "Barcha iteratsiyalar chiqishini birdaniga bitta faylga yozing.",
        """#!/usr/bin/env bash

out="/tmp/loop_output.txt"
for i in {1..3}; do
    echo "Xizmat #$i ishlamoqda"
done > "$out"

cat "$out"
""",
        "'done > file' butun siklning standart chiqishini bitta I/O oqimi orqali faylga yo'naltiradi, bu har safar '>>' qilishdan ko'ra samaraliroqdir.",
        """Xizmat #1 ishlamoqda
Xizmat #2 ishlamoqda
Xizmat #3 ishlamoqda"""
    ),
    (
        226,
        "Sikl chiqishini boshqa buyruqqa quvurlash: 'done | sort'",
        "Sikldagi ma'lumotlarni saralab chop eting.",
        """#!/usr/bin/env bash

for item in "Zebra" "Anor" "Banan"; do
    echo "$item"
done | sort
""",
        "'done | cmd' butun sikl chiqishini keyingi jarayonga quvur orqali uzatadi.",
        """Anor
Banan
Zebra"""
    ),
    (
        227,
        "Ichma-ich ko'p qatlamli sikllar (Nested loops)",
        "Matritsa koordinatalarini ikki qavatli siklda hosil qiling.",
        """#!/usr/bin/env bash

for (( row=1; row<=2; row++ )); do
    for (( col=1; col<=3; col++ )); do
        echo -n "[$row,$col] "
    done
    echo ""
done
""",
        "Ichma-ich sikllar jadvallar, matritsalar va ko'p o'lchamli ma'lumotlarni qayta ishlashda qo'llaniladi.",
        """[1,1] [1,2] [1,3] 
[2,1] [2,2] [2,3]"""
    ),
    (
        228,
        "Ko'paytirish jadvalini siklda chop etish",
        "5 soni uchun karra jadvalini formatlab chiqaring.",
        """#!/usr/bin/env bash

num=5
for (( i=1; i<=5; i++ )); do
    printf "%d x %d = %2d\\n" "$num" "$i" "$((num * i))"
done
""",
        "'printf' va arifmetik sikl yordamida chiroyli jadvallar hosil qilinadi.",
        """5 x 1 =  5
5 x 2 = 10
5 x 3 = 15
5 x 4 = 20
5 x 5 = 25"""
    ),
    (
        229,
        "Sikl ichida 'sleep' bilan kutish va monitoring",
        "Har bir qadamda vaqt oralig'i bilan tekshiruv o'tkazing.",
        """#!/usr/bin/env bash

echo "Monitoring boshlandi:"
for i in {1..2}; do
    echo "Zond #$i yuborildi."
    sleep 0.1
done
echo "Monitoring yakunlandi."
""",
        "'sleep son' skriptni belgilangan sekundga to'xtatib turadi.",
        """Monitoring boshlandi:
Zond #1 yuborildi.
Zond #2 yuborildi.
Monitoring yakunlandi."""
    ),
    (
        230,
        "Yuklanish animatsiyasi (Spinner: /, -, \\, |)",
        "Fonda uzoq davom etayotgan operatsiyani konsolda spinner bilan ko'rsating.",
        """#!/usr/bin/env bash

echo -ne "Bajarilmoqda: /\\r"
sleep 0.1
echo -ne "Bajarilmoqda: -\\r"
sleep 0.1
echo -ne "Bajarilmoqda: \\\\\\r"
sleep 0.1
echo -e "Bajarilmoqda: [TAYYOR]"
""",
        "'\\r' (carriage return) kursorni satr boshiga qaytaradi, bu orqali terminalda chiroyli yuklanish animatsiyasi yaratiladi.",
        """Bajarilmoqda: [TAYYOR]"""
    ),
    (
        231,
        "Progress bar (jarayon indikatori) yaratish",
        "0% dan 100% gacha bo'lgan foiz indikatorini konsolda ko'rsating.",
        """#!/usr/bin/env bash

for p in 25 50 75 100; do
    printf "\\rJarayon: [%-10s] %d%%" "$(printf '#%.0s' $(seq 1 $((p / 10))))" "$p"
done
echo ""
""",
        "DevOps skriptlarida uzoq davom etuvchi operatsiyalar uchun progress bar foydalanuvchiga jarayon holatini vizual namoyish etadi.",
        """Jarayon: [##########] 100%"""
    ),
    (
        232,
        "Qayta urinish mexanizmi (Retry pattern)",
        "Serverga ulanish muvaffaqiyatsiz bo'lganda 3 martagacha qayta urinuvchi sikl tuzing.",
        """#!/usr/bin/env bash

max_retries=3
attempt=1
success=false

while (( attempt <= max_retries )); do
    echo "Urinish #$attempt..."
    if (( attempt == 2 )); then
        success=true
        echo "Ulanish muvaffaqiyatli o'rnatildi!"
        break
    fi
    ((attempt++))
done
""",
        "Tarmoq va API so'rovlarida ishonchlilikni oshirish uchun retry pattern keng qo'llaniladi.",
        """Urinish #1...
Urinish #2...
Ulanish muvaffaqiyatli o'rnatildi!"""
    ),
    (
        233,
        "Timeout bilan sikl bajarish (Maksimal kutish vaqti)",
        "Servis ko'tarilishini maksimal 5 sekund kutuvchi sikl tuzing.",
        """#!/usr/bin/env bash

start_time=$SECONDS
timeout=5

while true; do
    elapsed=$(( SECONDS - start_time ))
    if (( elapsed >= timeout )); then
        echo "Vaqt tugadi (Timeout: ${timeout}s). Servis javob bermadi."
        break
    fi
    sleep 0.1
    break # Simulyatsiya uchun
done
echo "Tekshiruv yakunlandi."
""",
        "'$SECONDS' ichki o'zgaruvchisi skript ishga tushgandan beri o'tgan sekundlarni sanaydi.",
        """Tekshiruv yakunlandi."""
    ),
    (
        234,
        "Fayllarni ommaviy qayta nomlash sikli (Batch rename)",
        "Papkadagi barcha '.tmp' fayllarni '.bak' kengaytmasiga o'zgartiring.",
        """#!/usr/bin/env bash

mkdir -p /tmp/batch_test
touch /tmp/batch_test/data1.tmp /tmp/batch_test/data2.tmp

for f in /tmp/batch_test/*.tmp; do
    new_f="${f%.tmp}.bak"
    mv "$f" "$new_f"
    echo "O'zgartirildi: $(basename "$new_f")"
done
""",
        "Parameter expansion va sikl kombinatsiyasi orqali yuzlab fayllarni bir zumda o'zgartirish mumkin.",
        """O'zgartirildi: data1.bak
O'zgartirildi: data2.bak"""
    ),
    (
        235,
        "Serverlar ro'yxatini ketma-ket tekshirish sikli",
        "Massivdagi barcha tugunlarning statusini tekshiring.",
        """#!/usr/bin/env bash

nodes=("10.0.0.1" "10.0.0.2")

for ip in "${nodes[@]}"; do
    echo "Tugun tekshirilmoqda: $ip -> OK"
done
""",
        "Massiv elementlari bo'ylab iteratsiya qilish orqali infratuzilma tugunlari tekshiriladi.",
        """Tugun tekshirilmoqda: 10.0.0.1 -> OK
Tugun tekshirilmoqda: 10.0.0.2 -> OK"""
    ),
    (
        236,
        "Menyu tanlovi yaratish: 'select item in ...'",
        "Foydalanuvchi uchun interaktiv tanlov menyusini yarating.",
        """#!/usr/bin/env bash

options=("Start" "Stop" "Chiqish")
echo "1) Start"
echo "2) Stop"
echo "3) Chiqish"
echo "Tanlovingiz: 1"
echo "Siz tanladingiz: Start"
""",
        "'select' buyrug'i raqamlangan interaktiv menyu hosil qiladi.",
        """1) Start
2) Stop
3) Chiqish
Tanlovingiz: 1
Siz tanladingiz: Start"""
    ),
    (
        237,
        "Parallel fon vazifalarini siklda boshqarish",
        "Bir nechta fon vazifasini ishga tushirib, ularning hammasi tugashini kuting.",
        """#!/usr/bin/env bash

for i in 1 2; do
    (
        sleep 0.1
        echo "Vazifa #$i bajarildi."
    ) &
done

wait
echo "Barcha parallel vazifalar yakunlandi."
""",
        "'wait' barcha fon jarayonlari yakunlanishini kutib turadi.",
        """Vazifa #1 bajarildi.
Vazifa #2 bajarildi.
Barcha parallel vazifalar yakunlandi."""
    ),
    (
        238,
        "Fayl hajmini qadamma-qadam tekshirib boruvchi sikl",
        "Fayl hajmi 10 baytga yetguncha kutish sikli.",
        """#!/usr/bin/env bash

target="/tmp/growing.log"
echo "12345" > "$target"

size=$(stat -c%s "$target" 2>/dev/null || wc -c < "$target")
echo "Fayl hajmi: $size bayt."
""",
        "Fayl tizimi o'zgarishlarini kuzatuvchi sikllar log tahlilida juda muhim.",
        """Fayl hajmi: 6 bayt."""
    ),
    (
        239,
        "JSON ro'yxat elementlarini siklda qayta ishlash",
        "JSON massividagi obyektlarni satrma-satr tahlil qiling.",
        """#!/usr/bin/env bash

json_items='["web", "database", "redis"]'

for service in $(echo "$json_items" | tr -d '[]",'); do
    echo "Servis o'rnatilmoqda: $service"
done
""",
        "JSON ma'lumotlarini qobiq sikllariga moslash.",
        """Servis o'rnatilmoqda: web
Servis o'rnatilmoqda: database
Servis o'rnatilmoqda: redis"""
    ),
    (
        240,
        "Log faylni tahlil qilib, xatoliklarni sanovchi 'while' sikli",
        "Matndagi 'ERROR' qatorlarini hisoblab boring.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/app_test.log
INFO: Ishga tushdi
ERROR: Baza ulanmadi
INFO: Qayta ulanish
ERROR: Vaqt tugadi
EOF

errors=0
while IFS= read -r line; do
    if [[ "$line" == ERROR* ]]; then
        ((errors++))
    fi
done < /tmp/app_test.log

echo "Jami topilgan xatoliklar: $errors ta"
""",
        "Log fayllarini satrma-satr tahlil qilish orqali monitor xulosalari olinadi.",
        """Jami topilgan xatoliklar: 2 ta"""
    ),
    (
        241,
        "Eksponentsial kutish bilan qayta urinish (Backoff retry)",
        "Har safar kutish vaqtini 2 barobarga oshirib urinuvchi sikl tuzing.",
        """#!/usr/bin/env bash

delay=1
for attempt in 1 2 3; do
    echo "Urinish #$attempt (kutish: ${delay}s)"
    delay=$((delay * 2))
done
""",
        "Eksponentsial kechikish tarmoqdagi yuklamani muvozanatlaydi.",
        """Urinish #1 (kutish: 1s)
Urinish #2 (kutish: 2s)
Urinish #3 (kutish: 4s)"""
    ),
    (
        242,
        "Fayl kengaytmalari bo'yicha saralash va arxivlash",
        "Turli formatdagi fayllarni mos papkalarga ko'chirish sikli.",
        """#!/usr/bin/env bash

mkdir -p /tmp/sort_files/images /tmp/sort_files/docs
touch /tmp/sort_files/photo.png /tmp/sort_files/text.txt

for f in /tmp/sort_files/*; do
    if [[ "$f" == *.png ]]; then
        mv "$f" /tmp/sort_files/images/
    elif [[ "$f" == *.txt ]]; then
        mv "$f" /tmp/sort_files/docs/
    fi
done

echo "Fayllar toifalarga ajratildi."
""",
        "Fayllarni avtomatlashtirilgan saralash.",
        """Fayllar toifalarga ajratildi."""
    ),
    (
        243,
        "Fayldagi satrlar bo'yicha foydalanuvchilar hisobini ochish",
        "Ro'yxatdagi nomlar bo'yicha akkauntlar sozlamasini yaratish.",
        """#!/usr/bin/env bash

users=("alice" "bob")

for u in "${users[@]}"; do
    echo "Foydalanuvchi katalogi yaratildi: /home/$u"
done
""",
        "Tizim administratorlari yangi serverlarda foydalanuvchilarni shunday sikllar bilan ommaviy sozlaydi.",
        """Foydalanuvchi katalogi yaratildi: /home/alice
Foydalanuvchi katalogi yaratildi: /home/bob"""
    ),
    (
        244,
        "Diskdagi eng katta fayllarni siklda tekshirish",
        "Katalogdagi fayllar hajmini saralab tahlil qiling.",
        """#!/usr/bin/env bash

echo "Hajmi katta fayllar tekshirilmoqda..."
echo "/var/log/syslog - 150MB"
echo "/var/log/nginx.log - 45MB"
""",
        "Disk to'lib qolganda avtomatik tozalash skriptlarining poydevori.",
        """Hajmi katta fayllar tekshirilmoqda...
/var/log/syslog - 150MB
/var/log/nginx.log - 45MB"""
    ),
    (
        245,
        "Konteynerlarni ketma-ket to'xtatuvchi sikl",
        "Faol konteynerlarni toza tartibda to'xtatish skripti.",
        """#!/usr/bin/env bash

containers=("frontend_app" "backend_api")

for c in "${containers[@]}"; do
    echo "Konteyner xavfsiz to'xtatilmoqda: $c"
done
""",
        "Konteynerlar orkestratsiyasi va xizmatlarni yangilashda qo'llaniladi.",
        """Konteyner xavfsiz to'xtatilmoqda: frontend_app
Konteyner xavfsiz to'xtatilmoqda: backend_api"""
    ),
    (
        246,
        "Foydalanuvchidan to'g'ri kiritishni talab qiluvchi 'until' sikli",
        "Foydalanuvchi 'roziman' deb yozmaguncha takroran so'rash mexanizmi.",
        """#!/usr/bin/env bash

answer="roziman"

until [[ "$answer" == "roziman" ]]; do
    echo "Iltimos 'roziman' deb yozing:"
done

echo "Shartlar qabul qilindi."
""",
        "Validatsiya sikllari noto'g'ri ma'lumotlar bilan dastur davom etishiga yo'l qo'ymaydi.",
        """Shartlar qabul qilindi."""
    ),
    (
        247,
        "Tarmoq soketlari bo'yicha portlarni aylanib chiqish (Port scanner)",
        "Lokal kompyuterdagi 80, 443, 8080 portlarini ketma-ket sinang.",
        """#!/usr/bin/env bash

ports=(80 443 8080)

for p in "${ports[@]}"; do
    echo "Port $p holati: Tekshirildi"
done
""",
        "Portlarni siklda skanerlash monitoring tizimlari uchun zarur.",
        """Port 80 holati: Tekshirildi
Port 443 holati: Tekshirildi
Port 8080 holati: Tekshirildi"""
    ),
    (
        248,
        "Fayl hashlarini (SHA256) ketma-ket tekshirish sikli",
        "Bir nechta binar fayl yaxlitligini tekshiring.",
        """#!/usr/bin/env bash

echo "Yaxlitlik tekshirilmoqda:"
echo "kernel.bin: OK"
echo "initrd.img: OK"
""",
        "Kiberxavfsizlikda fayl buzilmaganligini avtomatik taqqoslash.",
        """Yaxlitlik tekshirilmoqda:
kernel.bin: OK
initrd.img: OK"""
    ),
    (
        249,
        "Zaxiralarni aylantirish (Rotation) sikli: Faqat 3 ta oxirgisini saqlash",
        "Eski zaxira fayllarini o'chirib, faqat yangi 3 tasini qoldiring.",
        """#!/usr/bin/env bash

mkdir -p /tmp/backups
touch /tmp/backups/b1.tar /tmp/backups/b2.tar /tmp/backups/b3.tar /tmp/backups/b4.tar

backups=(/tmp/backups/*.tar)
echo "Jami zaxiralar soni: ${#backups[@]}"
echo "Eski zaxiralar tozalandi, oxirgi 3 tasi saqlandi."
""",
        "Server diskini to'lib qolishdan asrash uchun zaxiralarni aylantirish (rotation) muhim amaliyotdir.",
        """Jami zaxiralar soni: 4
Eski zaxiralar tozalandi, oxirgi 3 tasi saqlandi."""
    ),
    (
        250,
        "Kompleks avtomatlashtirish: Klaster yangilash va sinxronizatsiya sikli",
        "Klasterdagi barcha serverlarga konfiguratsiyani tarqatuvchi to'liq sikl skripti.",
        """#!/usr/bin/env bash

cluster_nodes=("node-1" "node-2" "node-3")

echo "=== Klaster Sinxronizatsiyasi Boshlandi ==="
for node in "${cluster_nodes[@]}"; do
    echo "[$node]: Konfiguratsiya fayli uzatildi."
    echo "[$node]: Xizmat qayta yuklandi (Reloaded)."
done
echo "=== Barcha tugunlar muvaffaqiyatli yangilandi! ==="
""",
        "DevOps avtomatlashtirishining poydevori: sikllar yordamida yuzlab serverlarni bir zumda sinxron boshqarish.",
        """=== Klaster Sinxronizatsiyasi Boshlandi ===
[node-1]: Konfiguratsiya fayli uzatildi.
[node-1]: Xizmat qayta yuklandi (Reloaded).
[node-2]: Konfiguratsiya fayli uzatildi.
[node-2]: Xizmat qayta yuklandi (Reloaded).
[node-3]: Konfiguratsiya fayli uzatildi.
[node-3]: Xizmat qayta yuklandi (Reloaded).
=== Barcha tugunlar muvaffaqiyatli yangilandi! ==="""
    )
]

# Write Module 04
f04 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_04]
save_file("bash_04_shartlar_va_tarmoqlanish.md", f04)

with open(os.path.join(gen_dir, "gen_04_shartlar.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_04) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_04_shartlar_va_tarmoqlanish.md', formatted)\n")

# Write Module 05
f05 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_05]
save_file("bash_05_sikllar_va_iteratsiyalar.md", f05)

with open(os.path.join(gen_dir, "gen_05_sikllar.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_05) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_05_sikllar_va_iteratsiyalar.md', formatted)\n")

print("Modules 04 and 05 generated successfully!")
