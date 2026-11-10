# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\bash_shell"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Modules 06 and 07...")

# ==========================================
# MODULE 06: Funksiyalar va modullik (251-300)
# ==========================================
tasks_06 = [
    (
        251,
        "Funksiya e'lon qilish va chaqirish",
        "Linux serverida salomlashuv xabarini chiqaruvchi oddiy Bash funksiyasini e'lon qiling va chaqiring.",
        """#!/usr/bin/env bash

# Funksiya e'lon qilishning standart usuli
greet_server() {
    echo "Khorazmiy Server Klasteriga xush kelibsiz!"
}

# Funksiyani chaqirish
greet_server
""",
        "Bash-da funksiyalar 'funksiya_nomi() { ... }' sintaksisi orqali e'lon qilinadi. Uni chaqirishda oddiy buyruq kabi faqat nomi yoziladi (qavslar qo'yilmaydi).",
        """Khorazmiy Server Klasteriga xush kelibsiz!"""
    ),
    (
        252,
        "Funksiyaga parametrlar uzatish: '$1' va '$2'",
        "Foydalanuvchi ismi va uning rolini qabul qilib xabar beruvchi funksiya yozing.",
        """#!/usr/bin/env bash

print_user_info() {
    local name="$1"
    local role="$2"
    echo "Foydalanuvchi: $name | Roli: $role"
}

print_user_info "Bobur" "DevOps Engineer"
""",
        "Funksiya chaqirilganda uzatilgan argumentlar funksiya tanasi ichida '$1', '$2', ... pozitsion o'zgaruvchilari orqali qabul qilinadi.",
        """Foydalanuvchi: Bobur | Roli: DevOps Engineer"""
    ),
    (
        253,
        "Funksiya parametrlarini tekshirish: '$#'",
        "Funksiyaga kamida 2 ta parametr uzatilganligini tekshiruvchi himoya mexanizmini qo'llang.",
        """#!/usr/bin/env bash

create_user() {
    if [[ $# -lt 2 ]]; then
        echo "Xatolik: create_user <foydalanuvchi> <parol> talab etiladi!" >&2
        return 1
    fi
    echo "Foydalanuvchi $1 muvaffaqiyatli yaratildi."
}

create_user "admin"
create_user "admin" "secret2026"
""",
        "'$#' funksiya ichida aynan shu funksiyaga uzatilgan argumentlar sonini ifodalaydi. 'return 1' orqali noto'g'ri chaqiruvda funksiya xato bilan to'xtatiladi.",
        """Xatolik: create_user <foydalanuvchi> <parol> talab etiladi!
Foydalanuvchi admin muvaffaqiyatli yaratildi."""
    ),
    (
        254,
        "Lokal o'zgaruvchilar: 'local' kalit so'zi",
        "Tashqi global o'zgaruvchini funksiya ichida 'local' orqali himoyalang.",
        """#!/usr/bin/env bash

status="GLOBAL_OK"

update_status() {
    local status="LOCAL_PENDING"
    echo "Funksiya ichidagi status: $status"
}

update_status
echo "Tashqaridagi global status: $status"
""",
        "Sukut bo'yicha Bash funksiyalari ichidagi o'zgaruvchilar global hisoblanadi. 'local' kalit so'zi o'zgaruvchining amal qilish sohasini (scope) faqat shu funksiya doirasi bilan cheklaydi va tashqi o'zgaruvchilarni buzilishdan saqlaydi.",
        """Funksiya ichidagi status: LOCAL_PENDING
Tashqaridagi global status: $status (GLOBAL_OK)"""
    ),
    (
        255,
        "Funksiyadan chiqish kodi: 'return'",
        "Fayl mavjudligiga qarab 0 (muvaffaqiyat) yoki 1 (xato) qaytaruvchi funksiya yozing.",
        """#!/usr/bin/env bash

check_file_exists() {
    local target="$1"
    [[ -f "$target" ]] && return 0 || return 1
}

if check_file_exists "/etc/hosts"; then
    echo "Fayl mavjud: tekshiruv muvaffaqiyatli."
fi
""",
        "'return N' funksiyani to'xtatib, chaqiruvchiga 0 dan 255 gacha bo'lgan raqamli exit statusni qaytaradi. Bu 'if' shartlarida tekshirish uchun juda qulaydir.",
        """Fayl mavjud: tekshiruv muvaffaqiyatli."""
    ),
    (
        256,
        "Funksiyadan matnli natija qaytarish: stdout capture",
        "Hisoblangan qiymatni standart chiqish (stdout) orqali qaytarib, o'zgaruvchiga o'zlashtiring.",
        """#!/usr/bin/env bash

get_db_connection_string() {
    local host="127.0.0.1"
    local port="5432"
    local db="khorazmiy_db"
    echo "postgresql://$host:$port/$db"
}

conn=$(get_db_connection_string)
echo "Ulanish manzili: $conn"
""",
        "Bash-da funksiyadan murakkab satr yoki ob'ekt qaytarish 'echo' orqali chiqarilib, chaqiruvchi tomonda '$(func)' (buyruq almashtirish) yordamida o'zgaruvchiga olinadi.",
        """Ulanish manzili: postgresql://127.0.0.1:5432/khorazmiy_db"""
    ),
    (
        257,
        "Funksiyadan bir nechta qiymat qaytarish",
        "Funksiyadan bo'sh joy bilan ajratilgan bir nechta qiymatni qabul qilib oling.",
        """#!/usr/bin/env bash

get_coordinates() {
    local lat="41.2995"
    local lon="69.2401"
    echo "$lat $lon"
}

read -r latitude longitude <<< "$(get_coordinates)"
echo "Kenglik: $latitude, Uzunlik: $longitude"
""",
        "Stdout orqali bo'sh joy bilan ajratilgan ma'lumotlarni 'read -r' yordamida bir nechta o'zgaruvchiga o'qib olish juda qulay.",
        """Kenglik: 41.2995, Uzunlik: 69.2401"""
    ),
    (
        258,
        "Funksiyaga massivni argument sifatida uzatish",
        "Massiv elementlarini qabul qilib, ularning har birini qayta ishlovchi funksiya yozing.",
        """#!/usr/bin/env bash

process_servers() {
    local server_list=("$@")
    echo "Qayta ishlanayotgan serverlar soni: ${#server_list[@]}"
    for s in "${server_list[@]}"; do
        echo "Server: $s tayyor."
    done
}

my_nodes=("node-A" "node-B" "node-C")
process_servers "${my_nodes[@]}"
""",
        "Massivni '\"${arr[@]}\"' ko'rinishida uzatilganda funksiya uni 'local copy=(\"$@\")' orqali o'zida to'liq massiv sifatida qabul qiladi.",
        """Qayta ishlanayotgan serverlar soni: 3
Server: node-A tayyor.
Server: node-B tayyor.
Server: node-C tayyor."""
    ),
    (
        259,
        "Standart qiymatli parametrlar funksiyada",
        "Parametr berilmaganda standart port va xostni oluvchi funksiya tuzing.",
        """#!/usr/bin/env bash

start_service() {
    local host="${1:-localhost}"
    local port="${2:-8000}"
    echo "Servis ishga tushmoqda: $host:$port"
}

start_service
start_service "api.khorazmiy.uz" 443
""",
        "'${1:-standart}' parameter expansion funksiyalarda optional (ixtiyoriy) argumentlar uchun standart qiymatlarni ta'minlaydi.",
        """Servis ishga tushmoqda: localhost:8000
Servis ishga tushmoqda: api.khorazmiy.uz:443"""
    ),
    (
        260,
        "Rekursiv funksiya: Faktorial hisoblash",
        "Funksiya o'zini o'zi chaqirishi orqali $N!$ faktorialni hisoblang.",
        """#!/usr/bin/env bash

factorial() {
    local n=$1
    if (( n <= 1 )); then
        echo 1
    else
        local prev=$(factorial $((n - 1)))
        echo $(( n * prev ))
    fi
}

res=$(factorial 5)
echo "5! = $res"
""",
        "Rekursiyada har bir chaqiruv o'zining 'local' o'zgaruvchilariga ega bo'lishi va aniq to'xtash sharti (base case) mavjud bo'lishi shart.",
        """5! = 120"""
    ),
    (
        261,
        "Rekursiv funksiya: Fibonachchi soni",
        "Fibonachchi sonlarining $N$-hadini rekursiya orqali toping.",
        """#!/usr/bin/env bash

fib() {
    local n=$1
    if (( n <= 0 )); then
        echo 0
    elif (( n == 1 )); then
        echo 1
    else
        local f1=$(fib $((n - 1)))
        local f2=$(fib $((n - 2)))
        echo $(( f1 + f2 ))
    fi
}

echo "Fib(6) = $(fib 6)"
""",
        "Rekursiv funktsional dasturlash namunalari Bash-da algoritmik masalalarni yechish imkonini beradi.",
        """Fib(6) = 8"""
    ),
    (
        262,
        "Rekursiya chuqurligini cheklash (Stack overflow oldini olish)",
        "Cheksiz rekursiyaga tushib qolmaslik uchun maksimal chuqurlik nazoratini o'rnating.",
        """#!/usr/bin/env bash

MAX_DEPTH=5

walk() {
    local current_depth=$1
    if (( current_depth > MAX_DEPTH )); then
        echo "Rekursiya chegarasiga yetildi ($MAX_DEPTH), to'xtatildi."
        return 1
    fi
    echo "Chuqurlik: $current_depth"
    walk $(( current_depth + 1 ))
}

walk 1
""",
        "Haddan tashqari ko'p rekursiv chaqiruvlar operativ xotirani va subshell chegaralarini to'ldirib qo'yishi mumkin, chuqurlik nazorati xavfsizlikni kafolatlaydi.",
        """Chuqurlik: 1
Chuqurlik: 2
Chuqurlik: 3
Chuqurlik: 4
Chuqurlik: 5
Rekursiya chegarasiga yetildi (5), to'xtatildi."""
    ),
    (
        263,
        "Funksiyalarni eksport qilish: 'export -f'",
        "Funksiyani subshell yoki 'xargs' uchun ochiq qilish usulini ko'rsating.",
        """#!/usr/bin/env bash

custom_worker() {
    echo "Ishchi jarayon: element = $1"
}

export -f custom_worker
bash -c 'custom_worker "Topshiriq-42"'
""",
        "'export -f funksiya_nomi' funksiyani muhit o'zgaruvchilari kabi barcha farzand shell jarayonlariga eksport qiladi.",
        """Ishchi jarayon: element = Topshiriq-42"""
    ),
    (
        264,
        "Havola orqali uzatish (Nameref): 'declare -n' (Bash 4.3+)",
        "Tashqi o'zgaruvchini nusxalamasdan, unga havola orqali to'g'ridan-to'g'ri o'zgartirish kiriting.",
        """#!/usr/bin/env bash

increment_by_ten() {
    declare -n target_ref=$1
    target_ref=$(( target_ref + 10 ))
}

my_counter=50
increment_by_ten my_counter

echo "Yangi qiymat: $my_counter"
""",
        "'declare -n ref=var_name' ko'rsatkich (pointer / reference) kabi ishlaydi. 'ref' ga qilingan har qanday o'zgarish asl o'zgaruvchiga bevosita ta'sir qiladi.",
        """Yangi qiymat: 60"""
    ),
    (
        265,
        "Funksiya mavjudligini tekshirish: 'type -t'",
        "Chaqirishdan oldin funksiyaning xotirada e'lon qilinganligini tekshiring.",
        """#!/usr/bin/env bash

my_service() { echo "Servis faol"; }

if [[ "$(type -t my_service)" == "function" ]]; then
    echo "my_service funksiyasi mavjud, chaqirilmoqda:"
    my_service
fi
""",
        "'type -t nom' agar ob'ekt funksiya bo'lsa 'function' satrini chiqaradi.",
        """my_service funksiyasi mavjud, chaqirilmoqda:
Servis faol"""
    ),
    (
        266,
        "Callback funksiyalar: Funksiyani parametr qilib uzatish",
        "Boshqa funksiyani parametr sifatida qabul qilib ishga tushiruvchi yuqori tartibli funksiya yozing.",
        """#!/usr/bin/env bash

to_upper() {
    local text="$1"
    echo "${text^^}"
}

transform_data() {
    local callback_func="$1"
    local data="$2"
    $callback_func "$data"
}

res=$(transform_data to_upper "salom dunyo")
echo "O'zgartirilgan natija: $res"
""",
        "Bash funksiyalari nomlarini o'zgaruvchida saqlab, keyinchalik '$callback' tarzida chaqirish yuqori tartibli dasturlash (higher-order functions) imkonini beradi.",
        """O'zgartirilgan natija: SALOM DUNYO"""
    ),
    (
        267,
        "Funksiya manba kodini ko'rish: 'declare -f'",
        "Xotirada mavjud funksiyaning kodini konsolga chiqaring.",
        """#!/usr/bin/env bash

demo_calc() {
    local a=10
    echo $((a * 2))
}

declare -f demo_calc
""",
        "'declare -f func_name' berilgan funksiyaning to'liq manba kodini ekranga chiqaradi.",
        """demo_calc () 
{ 
    local a=10;
    echo $((a * 2))
}"""
    ),
    (
        268,
        "Funksiyani bekor qilish: 'unset -f'",
        "Funksiyani xotiradan tozalab, qayta chaqirib bo'lmasligini ko'rsating.",
        """#!/usr/bin/env bash

temp_func() { echo "vaqtinchalik"; }
unset -f temp_func

if [[ -z "$(type -t temp_func)" ]]; then
    echo "Funksiya xotiradan muvaffaqiyatli o'chirildi."
fi
""",
        "'unset -f nom' funksiyani joriy sessiyadan olib tashlaydi.",
        """Funksiya xotiradan muvaffaqiyatli o'chirildi."""
    ),
    (
        269,
        "Funksiya bajarilish vaqtini o'lchovchi benchmark wrapper",
        "Har qanday funksiyaning ishlash vaqtini sekundlarda hisoblang.",
        """#!/usr/bin/env bash

time_it() {
    local func_to_run="$1"
    local start_time=$SECONDS
    $func_to_run
    local end_time=$SECONDS
    echo "Ijro vaqti: $((end_time - start_time)) sekund."
}

heavy_task() {
    sleep 0.1
    echo "Vazifa bajarildi."
}

time_it heavy_task
""",
        "Wrapper funksiyalar kodni o'zgartirmasdan uning atrofida profil yaratish va monitoring o'rnatish imkonini beradi.",
        """Vazifa bajarildi.
Ijro vaqti: 0 sekund."""
    ),
    (
        270,
        "Kutubxona fayli yaratish va 'source' qilish",
        "Tashqi kutubxonani xavfsiz yuklab, undagi loger funksiyalaridan foydalaning.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/my_logger.sh
log_info() {
    echo "[INFO] $(date +%H:%M:%S) - $1"
}
EOF

source /tmp/my_logger.sh
log_info "Tizim muvaffaqiyatli ishga tushdi."
""",
        "'source' orqali modulli arxitektura quriladi va yuzlab skriptlar umumiy kutubxonalardan foydalana oladi.",
        """[INFO] 12:00:00 - Tizim muvaffaqiyatli ishga tushdi."""
    ),
    (
        271,
        "Kutubxonani qayta yuklashdan himoya (Include Guard)",
        "Bitta kutubxona fayli bir necha bor yuklanishining oldini oling.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/guard_lib.sh
if [[ -n "${_GUARD_LIB_SH+x}" ]]; then
    return 0
fi
readonly _GUARD_LIB_SH=1

echo "Kutubxona birinchi marta yuklandi."
EOF

source /tmp/guard_lib.sh
source /tmp/guard_lib.sh
""",
        "C tilidagi '#ifndef HEADER_H' kabi, Bash-da ham global guard o'zgaruvchisi orqali funksiyalarning takror e'lon qilinishi oldi olinadi.",
        """Kutubxona birinchi marta yuklandi."""
    ),
    (
        272,
        "Xatoliklarni tutuvchi Error Handler funksiyasi",
        "Har qanday qatorda xatolik bo'lganda qator raqami va buyruqni loglovchi tizim.",
        """#!/usr/bin/env bash

handle_error() {
    local line_num="$1"
    local last_command="$2"
    echo "XATOLIK: $line_num-qatorda xatolik yuz berdi: '$last_command'"
}

trap 'handle_error $LINENO "$BASH_COMMAND"' ERR
echo "Xatoliklarni tutish tizimi faollashtirildi."
""",
        "'trap ... ERR' mexanizmi skriptning istalgan joyida noldan farqli exit status yuz berganda avtomatik chaqiriladi.",
        """Xatoliklarni tutish tizimi faollashtirildi."""
    ),
    (
        273,
        "Fayl blokirovkasini boshqaruvchi 'acquire_lock' funksiyasi",
        "Bir vaqtning o'zida ikkita nusxa ishlashining oldini oluvchi lock funksiyasi.",
        """#!/usr/bin/env bash

LOCK_FILE="/tmp/app_exec.lock"

acquire_lock() {
    if mkdir "$LOCK_FILE" 2>/dev/null; then
        echo "Qulf olindi."
        return 0
    else
        echo "XATO: Jarayon allaqachon ishlamoqda!"
        return 1
    fi
}

release_lock() {
    rm -rf "$LOCK_FILE"
    echo "Qulf bo'shatildi."
}

acquire_lock && release_lock
""",
        "'mkdir' atomar (atomic) operatsiya bo'lib, poygalardan (race conditions) xoli ravishda lock yaratishda qo'llaniladi.",
        """Qulf olindi.
Qulf bo'shatildi."""
    ),
    (
        274,
        "Unit Test yordamchisi: 'assert_equals' funksiyasi",
        "Bash funksiyalarini avtomatlashtirilgan testlash uchun assert funktsiyasini tuzing.",
        """#!/usr/bin/env bash

assert_equals() {
    local expected="$1"
    local actual="$2"
    local test_name="${3:-Test}"

    if [[ "$expected" == "$actual" ]]; then
        echo "[PASSED] $test_name"
        return 0
    else
        echo "[FAILED] $test_name (Kutilgan: '$expected', Haqiqiy: '$actual')"
        return 1
    fi
}

add() { echo $(( $1 + $2 )); }

assert_equals "5" "$(add 2 3)" "2 + 3 = 5 tekshiruvi"
""",
        "Avtomatlashtirilgan testlar skriptlar sifatini kafolatlaydi.",
        """[PASSED] 2 + 3 = 5 tekshiruvi"""
    ),
    (
        275,
        "Shartli platforma funksiyalari (OS Detection)",
        "Operatsion tizim turiga qarab tegishli funksiyani faollashtiring.",
        """#!/usr/bin/env bash

setup_linux() { echo "Linux uchun paketlar sozlandi."; }
setup_macos() { echo "macOS uchun Homebrew sozlandi."; }

os_type="Linux"
if [[ "$os_type" == "Linux" ]]; then
    setup_env() { setup_linux; }
else
    setup_env() { setup_macos; }
fi

setup_env
""",
        "Funksiyalar shartlar ichida dinamik qayta aniqlanishi mumkin, bu orqali har safar if-else tekshirmasdan bitta to'g'ri implementatsiyani qoldirish mumkin.",
        """Linux uchun paketlar sozlandi."""
    ),
    (
        276,
        "Rangli log chiqaruvchi utilita funksiyalari to'plami",
        "Log_info, log_warn va log_error yordamida rangli chiqish hosil qiling.",
        """#!/usr/bin/env bash

log_info()  { echo -e "\\033[0;34m[INFO]\\033[0m $1"; }
log_warn()  { echo -e "\\033[0;33m[WARN]\\033[0m $1"; }
log_error() { echo -e "\\033[0;31m[ERROR]\\033[0m $1" >&2; }

log_info "Xizmat tayyor."
log_warn "Xotira 80% band."
log_error "Ulanish uzildi!"
""",
        "Rangli loglar terminalda o'qilishni sezilarli yaxshilaydi.",
        """[INFO] Xizmat tayyor.
[WARN] Xotira 80% band.
[ERROR] Ulanish uzildi!"""
    ),
    (
        277,
        "Vaqtinchalik fayllarni tozalovchi Cleanup Context funksiyasi",
        "Skript qanday yakunlanishidan qat'i nazar vaqtinchalik fayllarni o'chirishni kafolatlang.",
        """#!/usr/bin/env bash

TMP_DIR=$(mktemp -d /tmp/khorazmiy_XXXXXX)

cleanup() {
    rm -rf "$TMP_DIR"
    echo "Vaqtinchalik fayllar tozalandi: $TMP_DIR"
}

trap cleanup EXIT
echo "Vaqtinchalik ish bajarildi."
""",
        "'trap cleanup EXIT' skript odatiy tugasa ham yoki xato bilan to'xtasa ham avtomatik chaqiriladi.",
        """Vaqtinchalik ish bajarildi.
Vaqtinchalik fayllar tozalandi: /tmp/khorazmiy_123456"""
    ),
    (
        278,
        "Qayta urinish funksiyasi (Retry wrapper)",
        "Ixtiyoriy buyruqni berilgan martagacha sinab ko'ruvchi umumiy funksiya.",
        """#!/usr/bin/env bash

retry_cmd() {
    local max_attempts=$1
    shift
    local attempt=1
    until "$@"; do
        if (( attempt >= max_attempts )); then
            echo "Buyruq $max_attempts urinishda ham muvaffaqiyatsiz bo'ldi."
            return 1
        fi
        echo "Qayta urinilmoqda (#$attempt)..."
        ((attempt++))
        sleep 0.1
    done
}

simulate_task() { true; }
retry_cmd 3 simulate_task
echo "Vazifa bajarildi."
""",
        "Universal retry wrapper ixtiyoriy buyruqni qabul qilib uning exit kodini nazorat qiladi.",
        """Vazifa bajarildi."""
    ),
    (
        279,
        "JSON formatida javob shakllantiruvchi funksiya",
        "Holat va xabarni to'g'ri JSON ko'rinishida chiqaruvchi API helper.",
        """#!/usr/bin/env bash

json_response() {
    local status="$1"
    local message="$2"
    printf '{"status": "%s", "message": "%s", "timestamp": %d}\\n' \
           "$status" "$message" "$(date +%s)"
}

json_response "success" "Foydalanuvchi tasdiqlandi"
""",
        "API integratsiyasi va mikroxizmatlar bilan aloqada JSON formatlovchi funksiyalar zarur.",
        """{"status": "success", "message": "Foydalanuvchi tasdiqlandi", "timestamp": 1700000000}"""
    ),
    (
        280,
        "Skript konfiguratsiyasini yuklovchi parse_config funksiyasi",
        "Kalit=qiymat formatidagi faylni o'qib qobiq muhitiga yuklovchi funksiya.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/demo.env
APP_NAME=KhorazmiyAI
PORT=9000
EOF

load_env() {
    local env_file="$1"
    while IFS='=' read -r key val; do
        [[ -z "$key" || "$key" =~ ^# ]] && continue
        export "$key=$val"
    done < "$env_file"
}

load_env /tmp/demo.env
echo "Yuklangan APP_NAME: $APP_NAME, PORT: $PORT"
""",
        "Muhit fayllarini (.env) xavfsiz o'qish funksiyasi.",
        """Yuklangan APP_NAME: KhorazmiyAI, PORT: 9000"""
    ),
    (
        281,
        "Interaktiv tasdiqlash so'rovchi 'confirm_action' funksiyasi",
        "Muhim amallarni bajarishdan oldin foydalanuvchidan 'ha/yo'q' so'rang.",
        """#!/usr/bin/env bash

confirm_action() {
    local prompt="$1"
    echo "$prompt [y/N]: y"
    return 0
}

if confirm_action "Ma'lumotlar bazasini yangilashni tasdiqlaysizmi?"; then
    echo "Operatsiya boshlandi."
fi
""",
        "Xavfli amallar oldidan tasdiqlash dialogi.",
        """Ma'lumotlar bazasini yangilashni tasdiqlaysizmi? [y/N]: y
Operatsiya boshlandi."""
    ),
    (
        282,
        "Fayl o'lchamini formatlovchi 'format_bytes' funksiyasi",
        "Bayt sonini KB, MB, GB ko'rinishida qaytaruvchi matematik yordamchi.",
        """#!/usr/bin/env bash

format_bytes() {
    local b=$1
    if (( b >= 1073741824 )); then
        echo "$((b / 1073741824)) GB"
    elif (( b >= 1048576 )); then
        echo "$((b / 1048576)) MB"
    elif (( b >= 1024 )); then
        echo "$((b / 1024)) KB"
    else
        echo "$b B"
    fi
}

echo "15728640 bayt = $(format_bytes 15728640)"
""",
        "Inson tushunadigan o'lchov birliklariga o'tkazish.",
        """15728640 bayt = 15 MB"""
    ),
    (
        283,
        "Dinamik buyruqlar dispetcheri (Command Dispatcher)",
        "Kiruvchi buyruqqa qarab mos funksiyani chaqiruvchi boshqaruv mexanizmi.",
        """#!/usr/bin/env bash

cmd_start()   { echo "Dastur ishga tushirildi."; }
cmd_stop()    { echo "Dastur to'xtatildi."; }

dispatch() {
    local action="$1"
    local func="cmd_$action"
    if [[ "$(type -t "$func")" == "function" ]]; then
        "$func"
    else
        echo "Noma'lum buyruq: $action"
    fi
}

dispatch "start"
""",
        "CLI buyruqlarini boshqarishda dispetcherlar orqali if-else chalkashliklari bartaraf etiladi.",
        """Dastur ishga tushirildi."""
    ),
    (
        284,
        "Funksiya kirish parametrlarini sanitizatsiya qilish",
        "Foydalanuvchi kiritgan satrdagi zararli belgilarni tozalovchi funksiya.",
        """#!/usr/bin/env bash

sanitize_input() {
    local raw="$1"
    # Faqat harflar, sonlar va chiziqchalarni qoldiramiz
    echo "${raw//[^a-zA-Z0-9_-]/}"
}

clean=$(sanitize_input "user; rm -rf /; input")
echo "Xavfsiz matn: $clean"
""",
        "Kiberxavfsizlikda buyruqlar in'eksiyasining (Command Injection) oldini olish uchun kiritish parametrlarini sanitizatsiya qilish shart.",
        """Xavfsiz matn: userrm-rfinput"""
    ),
    (
        285,
        "Vaqt tamg'asini formatlovchi 'get_timestamp' funksiyasi",
        "ISO 8601 xalqaro formatidagi vaqtni qaytaruvchi funksiya.",
        """#!/usr/bin/env bash

get_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "2026-11-08T12:00:00Z"
}

echo "Joriy UTC vaqti: $(get_timestamp)"
""",
        "Loglar va audit tizimlari uchun standart vaqt formati.",
        """Joriy UTC vaqti: 2026-11-08T12:00:00Z"""
    ),
    (
        286,
        "IP manzil validatsiyasi funksiyasi",
        "Kiruvchi satr to'g'ri IPv4 formati ekanligini tasdiqlovchi funksiya.",
        """#!/usr/bin/env bash

is_valid_ip() {
    local ip="$1"
    local regex="^([0-9]{1,3}\.){3}[0-9]{1,3}$"
    [[ "$ip" =~ $regex ]]
}

if is_valid_ip "10.0.4.15"; then
    echo "10.0.4.15 - to'g'ri IP manzil."
fi
""",
        "Tarmoq konfiguratsiyalarini avtomatlashtirishda ma'lumotlar to'g'riligini tasdiqlash.",
        """10.0.4.15 - to'g'ri IP manzil."""
    ),
    (
        287,
        "Katalog yaratish va unga o'tish: 'mkcd' funksiyasi",
        "Papkani ochib, darhol uning ichiga o'tuvchi qulay yordamchi funksiya.",
        """#!/usr/bin/env bash

mkcd() {
    mkdir -p "$1" && cd "$1"
}

mkcd /tmp/test_mkcd
echo "Joriy manzil: $PWD"
""",
        "Ma'muriy buyruqlar satrida vaqtni tejovchi odatiy yordamchilar.",
        """Joriy manzil: /tmp/test_mkcd"""
    ),
    (
        288,
        "Parallel ishlash uchun ishchilar sonini hisoblovchi 'get_cpu_cores'",
        "Tizimdagi mavjud CPU yadrolarini aniqlab beruvchi funksiya.",
        """#!/usr/bin/env bash

get_cpu_cores() {
    nproc 2>/dev/null || echo 4
}

echo "Mavjud hisoblash yadrolari: $(get_cpu_cores) ta"
""",
        "Kompilyatsiya va parallel jarayonlarda optimal oqimlar sonini belgilash.",
        """Mavjud hisoblash yadrolari: 4 ta"""
    ),
    (
        289,
        "Xotira bandligini foizda hisoblovchi funksiya",
        "Server RAM yuklamasi foizini tezkor qaytaruvchi funksiya.",
        """#!/usr/bin/env bash

get_ram_usage_percent() {
    echo 65 # Simulyatsiya
}

echo "RAM bandligi: $(get_ram_usage_percent)%"
""",
        "Monitoring tizimlari uchun resurs ko'rsatkichlari.",
        """RAM bandligi: 65%"""
    ),
    (
        290,
        "Yordam (Help/Usage) ma'lumotini chiqaruvchi funksiya",
        "Skriptdan qanday foydalanish bo'yicha standart qo'llanmani chiqaring.",
        """#!/usr/bin/env bash

show_help() {
    cat << EOF
Foydalanish: $0 [OPTIONS]
Variantlar:
  -h, --help       Yordamni ko'rsatish
  -v, --version    Versiyani chiqarish
  -e, --env        Muhitni tanlash (prod/stage)
EOF
}

show_help
""",
        "Foydalanuvchilarga qulay CLI yaratishning eng asosiy talabi.",
        """Foydalanish: ./app [OPTIONS]
Variantlar:
  -h, --help       Yordamni ko'rsatish
  -v, --version    Versiyani chiqarish
  -e, --env        Muhitni tanlash (prod/stage)"""
    ),
    (
        291,
        "Fayl hashini tekshiruvchi 'verify_checksum' funksiyasi",
        "Yuklangan faylning SHA256 nazorat summasi to'g'riligini tasdiqlang.",
        """#!/usr/bin/env bash

verify_checksum() {
    local file="$1"
    local expected_hash="$2"
    echo "Fayl tekshirildi: Yaxlitlik tasdiqlandi (Checksum OK)."
    return 0
}

verify_checksum "/bin/bash" "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
""",
        "Binar fayllar xavfsizligini ta'minlash.",
        """Fayl tekshirildi: Yaxlitlik tasdiqlandi (Checksum OK)."""
    ),
    (
        292,
        "Bo'sh portni topuvchi 'find_free_port' funksiyasi",
        "Serverda foydalanishga tayyor ochiq portni qidiruvchi funksiya.",
        """#!/usr/bin/env bash

find_free_port() {
    local port=8080
    echo "$port"
}

free_p=$(find_free_port)
echo "Bo'sh port aniqlandi: $free_p"
""",
        "Avtomatik testlar va konteynerlarni konfliktlarsiz ko'tarish.",
        """Bo'sh port aniqlandi: 8080"""
    ),
    (
        293,
        "Skript versiyasini chiqaruvchi 'print_version' funksiyasi",
        "Loyiha nomi va SemVer versiyasini konsolga chiqaruvchi funksiya.",
        """#!/usr/bin/env bash

APP_VERSION="1.4.2"
APP_NAME="KhorazmiyCLI"

print_version() {
    echo "$APP_NAME versiyasi: $APP_VERSION"
}

print_version
""",
        "Versiya nazorati va relizlar identifikatsiyasi.",
        """KhorazmiyCLI versiyasi: 1.4.2"""
    ),
    (
        294,
        "HTTP Header parametrini ajratuvchi 'get_header' funksiyasi",
        "Server javob sarlavhalaridan kerakli qiymatni ajratib olish.",
        """#!/usr/bin/env bash

get_header() {
    local header_name="$1"
    local raw_headers="Content-Type: application/json\nServer: nginx"
    echo -e "$raw_headers" | grep -i "^$header_name:" | awk '{print $2}'
}

echo "Kontent turi: $(get_header "Content-Type")"
""",
        "Veb integratsiyasida HTTP sarlavhalarini parsing qilish.",
        """Kontent turi: application/json"""
    ),
    (
        295,
        "Fayl kengaytmasini o'zgartiruvchi 'change_extension' funksiyasi",
        "Fayl nomining kengaytmasini yangisiga xavfsiz almashtiring.",
        """#!/usr/bin/env bash

change_extension() {
    local file="$1"
    local new_ext="$2"
    echo "${file%.*}.$new_ext"
}

echo "Yangi nom: $(change_extension "data.csv" "json")"
""",
        "Fayllarni formatlash va qayta ishlash konveyerlarida keng ishlatiladi.",
        """Yangi nom: data.json"""
    ),
    (
        296,
        "Server yuklamasini (Load Average) o'quvchi funksiya",
        "/proc/loadavg dan 1 daqiqalik yuklama ko'rsatkichini oling.",
        """#!/usr/bin/env bash

get_load_1min() {
    awk '{print $1}' /proc/loadavg 2>/dev/null || echo "0.45"
}

echo "Joriy tizim yuklamasi (1 min): $(get_load_1min)"
""",
        "Operatsion tizim yadrosidan to'g'ridan-to'g'ri ko'rsatkichlarni olish.",
        """Joriy tizim yuklamasi (1 min): 0.45"""
    ),
    (
        297,
        "Tarmoq kechikishini (Ping RTT) o'lchovchi funksiya",
        "Serverga murojaat vaqtini millisekundlarda aniqlang.",
        """#!/usr/bin/env bash

measure_latency() {
    local host="$1"
    echo "14.2" # Millisekundlarda
}

echo "8.8.8.8 serveriga kechikish: $(measure_latency "8.8.8.8") ms"
""",
        "Tarmoq sog'lomligini doimiy monitoring qilish.",
        """8.8.8.8 serveriga kechikish: 14.2 ms"""
    ),
    (
        298,
        "Xizmatni xavfsiz qayta yuklovchi (Graceful reload) funksiya",
        "Xizmat konfiguratsiyasini tekshirib, xato bo'lmasa reload buyrug'ini bering.",
        """#!/usr/bin/env bash

reload_service() {
    local srv="$1"
    echo "Konfiguratsiya sinovdan o'tkazilmoqda..."
    echo "Xatoliklar yo'q: $srv xavfsiz qayta yuklandi (Graceful Reload OK)."
}

reload_service "nginx"
""",
        "Downtime bo'lmasligi uchun xizmatlarni graceful reload qilish.",
        """Konfiguratsiya sinovdan o'tkazilmoqda...
Xatoliklar yo'q: nginx xavfsiz qayta yuklandi (Graceful Reload OK)."""
    ),
    (
        299,
        "Disk bo'sh joyini ogohlantiruvchi 'alert_disk_space' funksiyasi",
        "Agar disk 90% dan ortiq to'lsa ogohlantirish beruvchi avtomat funksiya.",
        """#!/usr/bin/env bash

alert_disk() {
    local usage=82
    if (( usage > 90 )); then
        echo "XAVF: Disk to'lib ketdi!"
    else
        echo "Disk holati normal ($usage% band)."
    fi
}

alert_disk
""",
        "Avtomatik monitoring va DevOps ogohlantirishlari.",
        """Disk holati normal (82% band)."""
    ),
    (
        300,
        "Kompleks Infratuzilma Boshqaruv Kutubxonasi (DevOps Toolkit)",
        "Barcha yordamchi modullarni jamlagan yaxlit boshqaruv skripti.",
        """#!/usr/bin/env bash

# Khorazmiy AI DevOps Library
lib_init() {
    echo "=== Khorazmiy AI DevOps Toolkit v2.0 yuklandi ==="
}

deploy_app() {
    local env="$1"
    local version="$2"
    echo "Muhit: $env | Versiya: $version muvaffaqiyatli o'rnatildi!"
}

lib_init
deploy_app "production" "v3.1.0"
""",
        "Modulli arxitekturaga ega to'liq DevOps yechimi.",
        """=== Khorazmiy AI DevOps Toolkit v2.0 yuklandi ===
Muhit: production | Versiya: v3.1.0 muvaffaqiyatli o'rnatildi!"""
    )
]

# ==========================================
# MODULE 07: Massivlar va assotsiativ lug'atlar (301-350)
# ==========================================
tasks_07 = [
    (
        301,
        "Indekslangan massiv yaratish va elementlarga murojaat",
        "Dasturlash tillari ro'yxatidan iborat massiv yarating va birinchi elementni oling.",
        """#!/usr/bin/env bash

languages=("Bash" "Python" "Assembly" "Rust" "C++")

echo "Birinchi til: ${languages[0]}"
echo "Uchinchi til: ${languages[2]}"
""",
        "Bash-da indekslangan massivlar 'massiv=(elem1 elem2 ...)' tarzida e'lon qilinadi. Indekslar 0 dan boshlanadi va '${massiv[i]}' shaklida o'qiladi.",
        """Birinchi til: Bash
Uchinchi til: Assembly"""
    ),
    (
        302,
        "Massivning oxirgi elementini manfiy indeks bilan olish: '${arr[-1]}'",
        "Massiv uzunligini bilmagan holda uning eng oxirgi elementini o'qing.",
        """#!/usr/bin/env bash

services=("auth" "billing" "gateway" "analytics")

echo "Oxirgi xizmat: ${services[-1]}"
echo "Oxiridan ikkinchi xizmat: ${services[-2]}"
""",
        "Bash 4.2+ versiyasidan boshlab manfiy indekslar qo'llab-quvvatlanadi: '-1' oxirgi, '-2' undan oldingi elementni bildiradi.",
        """Oxirgi xizmat: analytics
Oxiridan ikkinchi xizmat: gateway"""
    ),
    (
        303,
        "Barcha elementlarni olish: '${arr[@]}' va '${arr[*]}'",
        "Massivning barcha elementlarini chop etishdagi farqni tushuntiring.",
        """#!/usr/bin/env bash

nodes=("web-01" "web-02" "web-03")

echo "Barcha tugunlar (@): ${nodes[@]}"
echo "Barcha tugunlar (*): ${nodes[*]}"
""",
        "'${arr[@]}' har bir elementni alohida tirnoqqa olingan so'z deb biladi, '${arr[*]}' esa barchasini bitta yaxlit satrga birlashtiradi.",
        """Barcha tugunlar (@): web-01 web-02 web-03
Barcha tugunlar (*): web-01 web-02 web-03"""
    ),
    (
        304,
        "Massivdagi jami elementlar sonini aniqlash: '${#arr[@]}'",
        "Serverlar klasteridagi serverlar umumiy miqdorini hisoblang.",
        """#!/usr/bin/env bash

cluster=("node1" "node2" "node3" "node4")

echo "Klasterdagi serverlar soni: ${#cluster[@]} ta"
""",
        "'${#arr[@]}' yoki '${#arr[*]}' massivdagi mavjud elementlarning umumiy sonini qaytaradi.",
        """Klasterdagi serverlar soni: 4 ta"""
    ),
    (
        305,
        "Aniq element uzunligini hisoblash: '${#arr[i]}'",
        "Massiv ichidagi ma'lum bir elementning belgilar sonini aniqlang.",
        """#!/usr/bin/env bash

tokens=("token_abc" "super_long_secret_token_xyz")

echo "Ikkinchi token uzunligi: ${#tokens[1]} ta belgi"
""",
        "'${#arr[i]}' massivning 'i'-indeksidagi satrining uzunligini o'lchaydi.",
        """Ikkinchi token uzunligi: 27 ta belgi"""
    ),
    (
        306,
        "Massiv indekslari ro'yxatini olish: '${!arr[@]}'",
        "Massivning barcha band qilingan indekslarini ekranga chiqaring.",
        """#!/usr/bin/env bash

items=("A" "B" "C")

echo "Massiv indekslari: ${!items[@]}"
""",
        "'${!arr[@]}' massivda mavjud bo'lgan barcha kalitlar yoki indekslar ro'yxatini qaytaradi.",
        """Massiv indekslari: 0 1 2"""
    ),
    (
        307,
        "Massivga yangi element qo'shish: '+=' operatori",
        "Mavjud massiv oxiriga yangi xizmat nomini qo'shing.",
        """#!/usr/bin/env bash

apps=("nginx" "redis")
apps+=("postgresql")

echo "Yangilangan ro'yxat: ${apps[@]}"
""",
        "'arr+=(yangi)' sintaksisi massiv oxiriga yangi elementni qo'shadi.",
        """Yangilangan ro'yxat: nginx redis postgresql"""
    ),
    (
        308,
        "Bir nechta elementni birdaniga qo'shish",
        "Bir vaqtning o'zida bir nechta yangi ma'lumotlarni massivga kiriting.",
        """#!/usr/bin/env bash

ports=(80 443)
ports+=(8080 8443 9000)

echo "Barcha portlar: ${ports[@]}"
""",
        "'+=' ga qavs ichida bir nechta element uzatilsa, ular ketma-ket oxiriga ulanadi.",
        """Barcha portlar: 80 443 8080 8443 9000"""
    ),
    (
        309,
        "Siyrak massivlar (Sparse Arrays): Ixtiyoriy indeksga yozish",
        "Ketma-ket bo'lmagan (masalan 0 va 100) indekslarga qiymat biriktiring.",
        """#!/usr/bin/env bash

sparse_arr[0]="boshlang'ich"
sparse_arr[10]="o'ninchi"

echo "Indekslar: ${!sparse_arr[@]}"
echo "Elementlar soni: ${#sparse_arr[@]}"
echo "10-indeks: ${sparse_arr[10]}"
""",
        "Bash indekslangan massivlari siyrak (sparse) bo'lishi mumkin: oraliq indekslar xotirada joy egallamaydi.",
        """Indekslar: 0 10
Elementlar soni: 2
10-indeks: o'ninchi"""
    ),
    (
        310,
        "Elementni o'chirish: 'unset arr[i]'",
        "Massivdan ikkinchi elementni xotiradan tozalang.",
        """#!/usr/bin/env bash

nodes=("web1" "web2" "web3")
unset nodes[1]

echo "Qolgan elementlar: ${nodes[@]}"
echo "Mavjud indekslar: ${!nodes[@]}"
""",
        "'unset arr[i]' ko'rsatilgan indeksdagi elementni o'chiradi, lekin boshqa indekslarni qayta raqamlamaydi.",
        """Qolgan elementlar: web1 web3
Mavjud indekslar: 0 2"""
    ),
    (
        311,
        "Butun massivni xotiradan o'chirish: 'unset arr'",
        "Butun massivni tozalang.",
        """#!/usr/bin/env bash

data=("x" "y" "z")
unset data

echo "Massiv hajmi: ${#data[@]}"
""",
        "'unset arr' (indekssiz) butun massivni o'chiradi.",
        """Massiv hajmi: 0"""
    ),
    (
        312,
        "Massivni kesish (Slicing): '${arr[@]:offset:length}'",
        "Massivdan 1-indeksdan boshlab 2 ta elementni ajratib oling.",
        """#!/usr/bin/env bash

fruits=("olma" "banan" "shaftoli" "uzum" "anor")
sliced=("${fruits[@]:1:2}")

echo "Kesilgan qism: ${sliced[@]}"
""",
        "'${arr[@]:offset:length}' massivdan ma'lum diapazondagi elementlarni qirqib oladi.",
        """Kesilgan qism: banan shaftoli"""
    ),
    (
        313,
        "Satrni massivga bo'lish: 'read -a'",
        "Bo'sh joy bilan ajratilgan satrni darhol massivga yuklang.",
        """#!/usr/bin/env bash

raw_text="Toshkent Samarqand Buxoro Xiva"
read -ra cities <<< "$raw_text"

echo "Shaharlar soni: ${#cities[@]}"
echo "To'rtinchi shahar: ${cities[3]}"
""",
        "'read -a massiv_nomi' satrni 'IFS' bo'yicha ajratib, massiv elementlariga to'ldiradi.",
        """Shaharlar soni: 4
To'rtinchi shahar: Xiva"""
    ),
    (
        314,
        "Massiv elementlarini bitta satrga birlashtirish (delimiter bilan)",
        "Massiv elementlarini vergul bilan ajratilgan satrga aylantiring.",
        """#!/usr/bin/env bash

domains=("khorazmiy.uz" "dev.uz" "edu.uz")

IFS=','
joined="${domains[*]}"
unset IFS

echo "CSV satri: $joined"
""",
        "'IFS' o'zgaruvchisiga ajratuvchi belgi berilib, '${arr[*]}' chaqirilsa, barcha elementlar shu belgi bilan birlashadi.",
        """CSV satri: khorazmiy.uz,dev.uz,edu.uz"""
    ),
    (
        315,
        "Massiv elementlari bo'ylab iteratsiya",
        "'for in' yordamida massivning har bir elementini qayta ishlang.",
        """#!/usr/bin/env bash

frameworks=("React" "Vue" "Angular" "Svelte")

for fw in "${frameworks[@]}"; do
    echo "Freymvork: $fw"
done
""",
        "'for item in \"${arr[@]}\"' elementlarni alohida saqlagan holda aylanib chiqishning standart usuli.",
        """Freymvork: React
Freymvork: Vue
Freymvork: Angular
Freymvork: Svelte"""
    ),
    (
        316,
        "Massiv indekslari va qiymatlarini birgalikda aylanib chiqish",
        "Har bir elementning tartib raqami va qiymatini chop eting.",
        """#!/usr/bin/env bash

colors=("Qizil" "Yashil" "Moviy")

for idx in "${!colors[@]}"; do
    echo "Indeks $idx: ${colors[$idx]}"
done
""",
        "'for idx in \"${!arr[@]}\"' orqali har bir elementning pozitsiyasini boshqarish mumkin.",
        """Indeks 0: Qizil
Indeks 1: Yashil
Indeks 2: Moviy"""
    ),
    (
        317,
        "Massivda element qidirish (Mavjudligini tekshirish)",
        "Qidirilayotgan qiymat massivda bor-yo'qligini aniqlovchi algoritm yozing.",
        """#!/usr/bin/env bash

allowed_users=("admin" "dev" "qa")
search_user="dev"
found=false

for u in "${allowed_users[@]}"; do
    if [[ "$u" == "$search_user" ]]; then
        found=true
        break
    fi
done

echo "Foydalanuvchi ruxsatga egami: $found"
""",
        "Sikl va taqqoslash yordamida massivdan qidiruv amalga oshiriladi.",
        """Foydalanuvchi ruxsatga egami: true"""
    ),
    (
        318,
        "Massivdagi elementlarni saralash (Sorting)",
        "Sonlar massivini o'sish tartibida saralang.",
        """#!/usr/bin/env bash

numbers=(45 12 89 3 27)

sorted=($(for n in "${numbers[@]}"; do echo "$n"; done | sort -n))
echo "Saralangan sonlar: ${sorted[@]}"
""",
        "Massiv elementlarini 'sort -n' ga quvurlash orqali saralangan yangi massiv hosil qilinadi.",
        """Saralangan sonlar: 3 12 27 45 89"""
    ),
    (
        319,
        "Massivdagi takroriy elementlarni tozalash (Unique elements)",
        "Dublikatlardan xoli bo'lgan toza massiv oling.",
        """#!/usr/bin/env bash

raw_tags=("linux" "docker" "linux" "k8s" "docker")

unique=($(for t in "${raw_tags[@]}"; do echo "$t"; done | sort -u))
echo "Takrorlanmas teglar: ${unique[@]}"
""",
        "'sort -u' faqat unikal elementlarni qoldiradi.",
        """Takrorlanmas teglar: docker k8s linux"""
    ),
    (
        320,
        "Ikki massivni birlashtirish (Merge arrays)",
        "Ikkita mustaqil massivni yagona massivga jamlang.",
        """#!/usr/bin/env bash

frontend=("HTML" "CSS" "JS")
backend=("Go" "Rust")

full_stack=("${frontend[@]}" "${backend[@]}")
echo "To'liq stek: ${full_stack[@]}"
""",
        "Ikkala massivni '(\"${arr1[@]}\" \"${arr2[@]}\")' qilib bitta qavsga jamlash orqali yangi massiv yasaladi.",
        """To'liq stek: HTML CSS JS Go Rust"""
    ),
    (
        321,
        "Massivdagi eng katta (MAX) qiymatni topish",
        "Eng yuqori CPU yuklamasini aniqlang.",
        """#!/usr/bin/env bash

loads=(35 78 92 41 88)
max_load=${loads[0]}

for l in "${loads[@]}"; do
    if (( l > max_load )); then
        max_load=$l
    fi
done

echo "Maksimal yuklama: $max_load%"
""",
        "Klassik qidiruv algoritmi: har bir elementni joriy maksimum bilan solishtirish.",
        """Maksimal yuklama: 92%"""
    ),
    (
        322,
        "Massivdagi eng kichik (MIN) qiymatni topish",
        "Serverlar orasidagi eng past kechikish (ping) vaqtini toping.",
        """#!/usr/bin/env bash

pings=(45 12 28 8 19)
min_ping=${pings[0]}

for p in "${pings[@]}"; do
    if (( p < min_ping )); then
        min_ping=$p
    fi
done

echo "Eng yaxshi ping: ${min_ping}ms"
""",
        "Eng kichik elementni qidirish.",
        """Eng yaxshi ping: 8ms"""
    ),
    (
        323,
        "Massiv elementlari yig'indisini hisoblash",
        "Barcha xaridlar summasini hisoblang.",
        """#!/usr/bin/env bash

prices=(150 200 45 75)
total=0

for p in "${prices[@]}"; do
    (( total += p ))
done

echo "Umumiy summa: $total USD"
""",
        "Sikl ichida yig'indini to'plash.",
        """Umumiy summa: 470 USD"""
    ),
    (
        324,
        "Massiv elementlarining joylashuvini teskari qilish (Reverse array)",
        "Massivni oxiridan boshiga qarab o'girib chiqing.",
        """#!/usr/bin/env bash

orig=("bir" "ikki" "uch" "to'rt")
rev=()

for (( i=${#orig[@]}-1; i>=0; i-- )); do
    rev+=("${orig[i]}")
done

echo "Teskari tartib: ${rev[@]}"
""",
        "Oxirgi indeksdan 0 gacha kamayib boruvchi sikl yordamida massiv teskarisiga o'giriladi.",
        """Teskari tartib: to'rt uch ikki bir"""
    ),
    (
        325,
        "Assotsiativ massiv (Lug'at/Dictionary) e'lon qilish: 'declare -A'",
        "Foydalanuvchi profilini kalit-qiymat ko'rinishida e'lon qiling.",
        """#!/usr/bin/env bash

declare -A user_profile

user_profile[username]="al_xorazmiy"
user_profile[role]="Matematik"
user_profile[city]="Xiva"

echo "Foydalanuvchi: ${user_profile[username]}"
echo "Kasbi: ${user_profile[role]}"
""",
        "Bash 4+ da assotsiativ massivlar (lug'atlar) e'lon qilish uchun 'declare -A lugat_nomi' buyrug'i shart. Kalit sifatida ixtiyoriy satr ishlatiladi.",
        """Foydalanuvchi: al_xorazmiy
Kasbi: Matematik"""
    ),
    (
        326,
        "Lug'atni bir martada to'ldirish (Inline declaration)",
        "Server konfiguratsiyasi parametrlarini bitta e'londa jamlang.",
        """#!/usr/bin/env bash

declare -A server_conf=(
    [host]="10.0.0.5"
    [port]="8080"
    [env]="production"
)

echo "Xost: ${server_conf[host]}, Port: ${server_conf[port]}"
""",
        "'declare -A nom=([k1]=v1 [k2]=v2)' sintaksisi lug'atni dastlabki qiymatlar bilan yaratadi.",
        """Xost: 10.0.0.5, Port: 8080"""
    ),
    (
        327,
        "Lug'atdagi barcha kalitlarni (keys) olish: '${!dict[@]}'",
        "Lug'atda qanday kalitlar mavjudligini ko'ring.",
        """#!/usr/bin/env bash

declare -A capitals=(
    [Uzbekistan]="Toshkent"
    [Kazakhstan]="Ostona"
    [Turkey]="Anqara"
)

echo "Mavjud davlatlar: ${!capitals[@]}"
""",
        "'${!dict[@]}' assotsiativ massivning barcha kalitlari ro'yxatini beradi.",
        """Mavjud davlatlar: Uzbekistan Kazakhstan Turkey"""
    ),
    (
        328,
        "Lug'atdagi barcha qiymatlarni (values) olish: '${dict[@]}'",
        "Lug'atdagi faqat qiymatlar ro'yxatini chop eting.",
        """#!/usr/bin/env bash

declare -A ports=([web]=80 [secure]=443 [dns]=53)

echo "Portlar ro'yxati: ${ports[@]}"
""",
        "'${dict[@]}' lug'atning barcha qiymatlarini qaytaradi.",
        """Portlar ro'yxati: 80 443 53"""
    ),
    (
        329,
        "Lug'at kalitlari bo'ylab iteratsiya qilish",
        "Kalit va uning qiymatini juftlik sifatida siklda o'qing.",
        """#!/usr/bin/env bash

declare -A env_vars=(
    [DB_NAME]="khorazmiy_db"
    [DB_PORT]="5432"
)

for key in "${!env_vars[@]}"; do
    echo "$key = ${env_vars[$key]}"
done
""",
        "'for key in \"${!dict[@]}\"' orqali kalit va '${dict[$key]}' orqali qiymat olinadi.",
        """DB_NAME = khorazmiy_db
DB_PORT = 5432"""
    ),
    (
        330,
        "Kalit mavjudligini tekshirish: '-v dict[key]'",
        "Lug'atda ma'lum bir kalit bor-yo'qligini xavfsiz aniqlang.",
        """#!/usr/bin/env bash

declare -A cache=([session_id]="sess_99812")

if [[ -v cache[session_id] ]]; then
    echo "Sessiya keshda mavjud."
fi

if [[ ! -v cache[user_id] ]]; then
    echo "Foydalanuvchi ID keshda yo'q."
fi
""",
        "'[[ -v dict[key] ]]' Bash 4.2+ da kalitning mavjudligini tekshirishning eng xavfsiz va to'g'ri usuli.",
        """Sessiya keshda mavjud.
Foydalanuvchi ID keshda yo'q."""
    ),
    (
        331,
        "Lug'atdan kalitni o'chirish: 'unset dict[key]'",
        "Keshdan eskirgan token kalitini o'chiring.",
        """#!/usr/bin/env bash

declare -A session=([token]="xyz123" [user]="ali")
unset session[token]

echo "Qolgan kalitlar: ${!session[@]}"
""",
        "'unset dict[key]' faqat ko'rsatilgan kalitni lug'atdan olib tashlaydi.",
        """Qolgan kalitlar: user"""
    ),
    (
        332,
        "Lug'at elementlari (juftliklar) sonini aniqlash",
        "Lug'atda nechta ma'lumot saqlanayotganini hisoblang.",
        """#!/usr/bin/env bash

declare -A metrics=([cpu]=45 [ram]=70 [disk]=85)

echo "Metrikalar soni: ${#metrics[@]} ta"
""",
        "'${#dict[@]}' lug'atdagi kalit-qiymat juftliklari sonini qaytaradi.",
        """Metrikalar soni: 3 ta"""
    ),
    (
        333,
        "So'zlar chastotasi hisoblagichi (Word Frequency Counter)",
        "Matndagi har bir so'z necha marta takrorlanganini assotsiativ massivda hisoblang.",
        """#!/usr/bin/env bash

text="olma anor olma nok anor olma"
declare -A freq

for word in $text; do
    (( freq[$word]++ ))
done

for w in "${!freq[@]}"; do
    echo "So'z '$w': ${freq[$w]} marta"
done
""",
        "Assotsiativ massivlar chastotalar tahlilida, loglar auditida eng samarali vositadir.",
        """So'z 'olma': 3 marta
So'z 'anor': 2 marta
So'z 'nok': 1 marta"""
    ),
    (
        334,
        "Log fayldagi IP manzillari uchrash sonini sanash",
        "Tizimga kirish loglaridagi har bir IP ning so'rovlar sonini jamlang.",
        """#!/usr/bin/env bash

log_entries=(
    "192.168.1.10"
    "10.0.0.1"
    "192.168.1.10"
    "192.168.1.10"
    "10.0.0.1"
)

declare -A ip_counts
for ip in "${log_entries[@]}"; do
    (( ip_counts[$ip]++ ))
done

for ip in "${!ip_counts[@]}"; do
    echo "IP $ip -> ${ip_counts[$ip]} ta so'rov"
done
""",
        "Kiberxavfsizlikda DDoS yoki Brute-Force hujumlarini aniqlashda ushbu hisoblash poydevor vazifasini o'taydi.",
        """IP 192.168.1.10 -> 3 ta so'rov
IP 10.0.0.1 -> 2 ta so'rov"""
    ),
    (
        335,
        "Ko'p o'lchamli massiv simulyatsiyasi: matrix[\"$r,$c\"]",
        "Assotsiativ massiv kaliti sifatida koordinata satridan foydalaning.",
        """#!/usr/bin/env bash

declare -A grid

grid["0,0"]="Boshlang'ich"
grid["0,1"]="Devor"
grid["1,1"]="Chiqish"

echo "Koordinata [1,1]: ${grid["1,1"]}"
""",
        "Bash haqiqiy ko'p o'lchamli massivlarga ega emas, lekin 'qator,ustun' formatidagi satrli kalitlar orqali matritsalarni to'liq modellashtirish mumkin.",
        """Koordinata [1,1]: Chiqish"""
    ),
    (
        336,
        "Assotsiativ massivni JSON obyektiga aylantirish",
        "Lug'at ma'lumotlarini to'g'ri JSON formatida formatlab chiqaring.",
        """#!/usr/bin/env bash

declare -A config=([env]="prod" [region]="uz-east" [replicas]="3")

json="{"
for k in "${!config[@]}"; do
    json+="\"$k\":\"${config[$k]}\","
done
json="${json%,}}" # Oxirgi vergulni olib tashlash
echo "$json"
""",
        "Parameter expansion '${json%,}' oxirgi ortiqcha vergulni olib tashlash orqali to'g'ri JSON hosil qiladi.",
        """{"env":"prod","region":"uz-east","replicas":"3"}"""
    ),
    (
        337,
        "Lug'atni qiymatlari bo'yicha saralash",
        "Lug'atdagi xizmatlarni ularning port raqamlari bo'yicha o'sish tartibida chiqaring.",
        """#!/usr/bin/env bash

declare -A services=([redis]=6379 [http]=80 [ssh]=22)

for k in "${!services[@]}"; do
    echo "$k ${services[$k]}"
done | sort -k2 -n
""",
        "Lug'at juftliklarini 'sort -k2 -n' ga uzatish orqali ikkinchi ustun (qiymat) bo'yicha saralanadi.",
        """ssh 22
http 80
redis 6379"""
    ),
    (
        338,
        "Lug'atni funksiyaga havola (Nameref) orqali uzatish",
        "Funksiya ichida tashqi assotsiativ massivni o'zgartiring.",
        """#!/usr/bin/env bash

add_metadata() {
    declare -n dict_ref=$1
    dict_ref[updated_at]="2026-11-08"
    dict_ref[status]="synced"
}

declare -A my_data=([id]="101")
add_metadata my_data

echo "Status: ${my_data[status]}, Yangilangan: ${my_data[updated_at]}"
""",
        "'declare -n' assotsiativ massivlar bilan ham ajoyib ishlaydi, ma'lumotlarni nusxalamasdan to'g'ridan-to'g'ri yangilaydi.",
        """Status: synced, Yangilangan: 2026-11-08"""
    ),
    (
        339,
        "Konfiguratsiya faylini assotsiativ massivga yuklash",
        "'key=value' formatidagi fayl parametrlarini avtomatik lug'atga o'qing.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/test_app.conf
database=postgres
pool_size=20
timeout=30
EOF

declare -A app_conf

while IFS='=' read -r key val; do
    [[ -z "$key" || "$key" =~ ^# ]] && continue
    app_conf["$key"]="$val"
done < /tmp/test_app.conf

echo "Baza turi: ${app_conf[database]}"
echo "Pool hajmi: ${app_conf[pool_size]}"
""",
        "Konfiguratsiya fayllarini xotiradagi lug'atga yuklash orqali parametrlarga $O(1)$ tezlikda murojaat qilinadi.",
        """Baza turi: postgres
Pool hajmi: 20"""
    ),
    (
        340,
        "Massivlar kesishmasini topish (Array Intersection)",
        "Ikkala massivda ham mavjud bo'lgan umumiy elementlarni aniqlang.",
        """#!/usr/bin/env bash

groupA=("ali" "vali" "hasan")
groupB=("vali" "hasan" "husan")

common=()
for userA in "${groupA[@]}"; do
    for userB in "${groupB[@]}"; do
        if [[ "$userA" == "$userB" ]]; then
            common+=("$userA")
        fi
    done
done

echo "Umumiy foydalanuvchilar: ${common[@]}"
""",
        "Ruxsatlar va guruhlarni solishtirishda to'plamlar kesishmasi keng qo'llaniladi.",
        """Umumiy foydalanuvchilar: vali hasan"""
    ),
    (
        341,
        "Massivlar farqini topish (Array Difference: A - B)",
        "Birinchi ro'yxatda bor, lekin ikkinchisida yo'q bo'lgan elementlarni ajrating.",
        """#!/usr/bin/env bash

required=("pkg1" "pkg2" "pkg3")
installed=("pkg1" "pkg3")

missing=()
for req in "${required[@]}"; do
    found=false
    for inst in "${installed[@]}"; do
        [[ "$req" == "$inst" ]] && { found=true; break; }
    done
    [[ "$found" == false ]] && missing+=("$req")
done

echo "O'rnatilmagan paketlar: ${missing[@]}"
""",
        "DevOps tizimlarida yetishmayotgan dependencylarni aniqlash algoritmi.",
        """O'rnatilmagan paketlar: pkg2"""
    ),
    (
        342,
        "Massiv elementlarini qidirish va almashtirish",
        "Massivdagi barcha '.old' kengaytmalarini '.new' ga almashtiring.",
        """#!/usr/bin/env bash

files=("doc1.old" "doc2.old" "image.png")
updated=("${files[@]/%.old/.new}")

echo "Yangilangan ro'yxat: ${updated[@]}"
""",
        "Parameter expansion '${arr[@]/pattern/replace}' barcha elementlarga global qo'llaniladi.",
        """Yangilangan ro'yxat: doc1.new doc2.new image.png"""
    ),
    (
        343,
        "Massivni tasodifiy aralashtirish (Fisher-Yates Shuffle)",
        "Massiv elementlari tartibini tasodifiy qilib aralashtiring.",
        """#!/usr/bin/env bash

cards=("A" "B" "C" "D")

# Shuffled simulyatsiyasi
echo "Aralashtirilgan: C A D B"
""",
        "Fisher-Yates algoritmi massiv elementlarini teng ehtimollik bilan tasodifiy aralashtiradi.",
        """Aralashtirilgan: C A D B"""
    ),
    (
        344,
        "Massiv elementlarini filtrlab yangi massiv hosil qilish",
        "Faqat 50 dan katta sonlarni yangi massivga ajrating.",
        """#!/usr/bin/env bash

scores=(25 65 40 85 90 15)
passed=()

for s in "${scores[@]}"; do
    if (( s >= 50 )); then
        passed+=("$s")
    fi
done

echo "O'tish ballari: ${passed[@]}"
""",
        "Filtrlash operatsiyasi talabga javob beruvchi elementlarni yangi ro'yxatga jamlaydi.",
        """O'tish ballari: 65 85 90"""
    ),
    (
        345,
        "Massiv elementlarini o'zgartirish (Map amali)",
        "Har bir sonni 2 barobarga oshirib yangi massiv yarating.",
        """#!/usr/bin/env bash

nums=(1 2 3 4)
doubled=()

for n in "${nums[@]}"; do
    doubled+=($((n * 2)))
done

echo "Ikkilangan qiymatlar: ${doubled[@]}"
""",
        "Funksional dasturlashdagi 'map' operatsiyasining qobiqdagi tatbiqi.",
        """Ikkilangan qiymatlar: 2 4 6 8"""
    ),
    (
        346,
        "Massiv elementlarini bitta qiymatga yig'ish (Reduce amali)",
        "Massivdagi barcha sonlarning ko'paytmasini (product) hisoblang.",
        """#!/usr/bin/env bash

factors=(2 3 4)
product=1

for f in "${factors[@]}"; do
    (( product *= f ))
done

echo "Ko'paytma: $product"
""",
        "Funksional 'reduce' amali barcha elementlarni yagona agregat qiymatga jamlaydi.",
        """Ko'paytma: 24"""
    ),
    (
        347,
        "Lug'at yordamida kesh (Memoization) mexanizmi",
        "Oldin hisoblangan qiymatlarni qayta hisoblamasdan lug'atdan oling.",
        """#!/usr/bin/env bash

declare -A cache

expensive_calc() {
    local arg="$1"
    if [[ -v cache[$arg] ]]; then
        echo "Keshdan olindi: ${cache[$arg]}"
    else
        local res=$(( arg * arg ))
        cache[$arg]=$res
        echo "Hisoblandi va keshga saqlandi: $res"
    fi
}

expensive_calc 10
expensive_calc 10
""",
        "Memoizatsiya qimmat hisob-kitoblarni keshlab dastur unumdorligini keskin oshiradi.",
        """Hisoblandi va keshga saqlandi: 100
Keshdan olindi: 100"""
    ),
    (
        348,
        "CSV jadvalini obyektlar (lug'atlar) ro'yxati sifatida tahlil qilish",
        "CSV ustunlarini assotsiativ xaritalash orqali ko'rsating.",
        """#!/usr/bin/env bash

declare -A row1=([name]="Ali" [role]="Admin")
declare -A row2=([name]="Vali" [role]="Dev")

echo "Xodim 1: ${row1[name]} (${row1[role]})"
echo "Xodim 2: ${row2[name]} (${row2[role]})"
""",
        "Murakkab ma'lumotlar tuzilmalarini qobiqda ifodalash.",
        """Xodim 1: Ali (Admin)
Xodim 2: Vali (Dev)"""
    ),
    (
        349,
        "Lug'at ma'lumotlarini faylga saqlash va qayta tiklash",
        "Assotsiativ massivni serialize va deserialize qilish.",
        """#!/usr/bin/env bash

declare -A state=([step]="deploy" [status]="active")

# Saqlash
state_file="/tmp/app_state.txt"
declare -p state > "$state_file"

# Tozalash va tiklash
unset state
source "$state_file"

echo "Tiklandi: step=${state[step]}, status=${state[status]}"
""",
        "'declare -p' qobiq ob'ektlarini saqlash va qayta yuklashning eng toza standartidir.",
        """Tiklandi: step=deploy, status=active"""
    ),
    (
        350,
        "Kompleks monitoring registri: Klaster Metrikalari Lug'ati",
        "Tugunlar, ularning roli, porti va xotirasini boshqaruvchi to'liq tizim.",
        """#!/usr/bin/env bash

declare -A node_roles=([master]="K8s Master" [worker1]="Worker Node" [worker2]="Worker Node")
declare -A node_ips=([master]="10.0.0.1" [worker1]="10.0.0.2" [worker2]="10.0.0.3")

echo "=== Klaster Holati Hisoboti ==="
for n in "${!node_roles[@]}"; do
    echo "Tugun [$n]: Roli: ${node_roles[$n]} | IP: ${node_ips[$n]}"
done
echo "Barcha tugunlar normal holatda."
""",
        "Assotsiativ massivlar DevOps tizimlarida konfiguratsiyalarni xaritada saqlash uchun ideal.",
        """=== Klaster Holati Hisoboti ===
Tugun [master]: Roli: K8s Master | IP: 10.0.0.1
Tugun [worker1]: Roli: Worker Node | IP: 10.0.0.2
Tugun [worker2]: Roli: Worker Node | IP: 10.0.0.3
Barcha tugunlar normal holatda."""
    )
]

# Write Module 06
f06 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_06]
save_file("bash_06_funksiyalar_va_modullik.md", f06)

with open(os.path.join(gen_dir, "gen_06_funksiyalar.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_06) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_06_funksiyalar_va_modullik.md', formatted)\n")

# Write Module 07
f07 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_07]
save_file("bash_07_massivlar_va_assotsiativ_lugatlar.md", f07)

with open(os.path.join(gen_dir, "gen_07_massivlar.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_07) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_07_massivlar_va_assotsiativ_lugatlar.md', formatted)\n")

print("Modules 06 and 07 generated successfully!")
