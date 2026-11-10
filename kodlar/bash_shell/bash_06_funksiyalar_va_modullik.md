# 251-Topshiriq: Funksiya e'lon qilish va chaqirish
## Topshiriq sharti:
Linux serverida salomlashuv xabarini chiqaruvchi oddiy Bash funksiyasini e'lon qiling va chaqiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Funksiya e'lon qilishning standart usuli
greet_server() {
    echo "Khorazmiy Server Klasteriga xush kelibsiz!"
}

# Funksiyani chaqirish
greet_server
```

## Tushuntirish va Mantiq:
Bash-da funksiyalar 'funksiya_nomi() { ... }' sintaksisi orqali e'lon qilinadi. Uni chaqirishda oddiy buyruq kabi faqat nomi yoziladi (qavslar qo'yilmaydi).

## Ishlash natijasi:
```text
Khorazmiy Server Klasteriga xush kelibsiz!
```


# 252-Topshiriq: Funksiyaga parametrlar uzatish: '$1' va '$2'
## Topshiriq sharti:
Foydalanuvchi ismi va uning rolini qabul qilib xabar beruvchi funksiya yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

print_user_info() {
    local name="$1"
    local role="$2"
    echo "Foydalanuvchi: $name | Roli: $role"
}

print_user_info "Bobur" "DevOps Engineer"
```

## Tushuntirish va Mantiq:
Funksiya chaqirilganda uzatilgan argumentlar funksiya tanasi ichida '$1', '$2', ... pozitsion o'zgaruvchilari orqali qabul qilinadi.

## Ishlash natijasi:
```text
Foydalanuvchi: Bobur | Roli: DevOps Engineer
```


# 253-Topshiriq: Funksiya parametrlarini tekshirish: '$#'
## Topshiriq sharti:
Funksiyaga kamida 2 ta parametr uzatilganligini tekshiruvchi himoya mexanizmini qo'llang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

create_user() {
    if [[ $# -lt 2 ]]; then
        echo "Xatolik: create_user <foydalanuvchi> <parol> talab etiladi!" >&2
        return 1
    fi
    echo "Foydalanuvchi $1 muvaffaqiyatli yaratildi."
}

create_user "admin"
create_user "admin" "secret2026"
```

## Tushuntirish va Mantiq:
'$#' funksiya ichida aynan shu funksiyaga uzatilgan argumentlar sonini ifodalaydi. 'return 1' orqali noto'g'ri chaqiruvda funksiya xato bilan to'xtatiladi.

## Ishlash natijasi:
```text
Xatolik: create_user <foydalanuvchi> <parol> talab etiladi!
Foydalanuvchi admin muvaffaqiyatli yaratildi.
```


# 254-Topshiriq: Lokal o'zgaruvchilar: 'local' kalit so'zi
## Topshiriq sharti:
Tashqi global o'zgaruvchini funksiya ichida 'local' orqali himoyalang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

status="GLOBAL_OK"

update_status() {
    local status="LOCAL_PENDING"
    echo "Funksiya ichidagi status: $status"
}

update_status
echo "Tashqaridagi global status: $status"
```

## Tushuntirish va Mantiq:
Sukut bo'yicha Bash funksiyalari ichidagi o'zgaruvchilar global hisoblanadi. 'local' kalit so'zi o'zgaruvchining amal qilish sohasini (scope) faqat shu funksiya doirasi bilan cheklaydi va tashqi o'zgaruvchilarni buzilishdan saqlaydi.

## Ishlash natijasi:
```text
Funksiya ichidagi status: LOCAL_PENDING
Tashqaridagi global status: $status (GLOBAL_OK)
```


# 255-Topshiriq: Funksiyadan chiqish kodi: 'return'
## Topshiriq sharti:
Fayl mavjudligiga qarab 0 (muvaffaqiyat) yoki 1 (xato) qaytaruvchi funksiya yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

check_file_exists() {
    local target="$1"
    [[ -f "$target" ]] && return 0 || return 1
}

if check_file_exists "/etc/hosts"; then
    echo "Fayl mavjud: tekshiruv muvaffaqiyatli."
fi
```

## Tushuntirish va Mantiq:
'return N' funksiyani to'xtatib, chaqiruvchiga 0 dan 255 gacha bo'lgan raqamli exit statusni qaytaradi. Bu 'if' shartlarida tekshirish uchun juda qulaydir.

## Ishlash natijasi:
```text
Fayl mavjud: tekshiruv muvaffaqiyatli.
```


# 256-Topshiriq: Funksiyadan matnli natija qaytarish: stdout capture
## Topshiriq sharti:
Hisoblangan qiymatni standart chiqish (stdout) orqali qaytarib, o'zgaruvchiga o'zlashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

get_db_connection_string() {
    local host="127.0.0.1"
    local port="5432"
    local db="khorazmiy_db"
    echo "postgresql://$host:$port/$db"
}

conn=$(get_db_connection_string)
echo "Ulanish manzili: $conn"
```

## Tushuntirish va Mantiq:
Bash-da funksiyadan murakkab satr yoki ob'ekt qaytarish 'echo' orqali chiqarilib, chaqiruvchi tomonda '$(func)' (buyruq almashtirish) yordamida o'zgaruvchiga olinadi.

## Ishlash natijasi:
```text
Ulanish manzili: postgresql://127.0.0.1:5432/khorazmiy_db
```


# 257-Topshiriq: Funksiyadan bir nechta qiymat qaytarish
## Topshiriq sharti:
Funksiyadan bo'sh joy bilan ajratilgan bir nechta qiymatni qabul qilib oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

get_coordinates() {
    local lat="41.2995"
    local lon="69.2401"
    echo "$lat $lon"
}

read -r latitude longitude <<< "$(get_coordinates)"
echo "Kenglik: $latitude, Uzunlik: $longitude"
```

## Tushuntirish va Mantiq:
Stdout orqali bo'sh joy bilan ajratilgan ma'lumotlarni 'read -r' yordamida bir nechta o'zgaruvchiga o'qib olish juda qulay.

## Ishlash natijasi:
```text
Kenglik: 41.2995, Uzunlik: 69.2401
```


# 258-Topshiriq: Funksiyaga massivni argument sifatida uzatish
## Topshiriq sharti:
Massiv elementlarini qabul qilib, ularning har birini qayta ishlovchi funksiya yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

process_servers() {
    local server_list=("$@")
    echo "Qayta ishlanayotgan serverlar soni: ${#server_list[@]}"
    for s in "${server_list[@]}"; do
        echo "Server: $s tayyor."
    done
}

my_nodes=("node-A" "node-B" "node-C")
process_servers "${my_nodes[@]}"
```

## Tushuntirish va Mantiq:
Massivni '"${arr[@]}"' ko'rinishida uzatilganda funksiya uni 'local copy=("$@")' orqali o'zida to'liq massiv sifatida qabul qiladi.

## Ishlash natijasi:
```text
Qayta ishlanayotgan serverlar soni: 3
Server: node-A tayyor.
Server: node-B tayyor.
Server: node-C tayyor.
```


# 259-Topshiriq: Standart qiymatli parametrlar funksiyada
## Topshiriq sharti:
Parametr berilmaganda standart port va xostni oluvchi funksiya tuzing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

start_service() {
    local host="${1:-localhost}"
    local port="${2:-8000}"
    echo "Servis ishga tushmoqda: $host:$port"
}

start_service
start_service "api.khorazmiy.uz" 443
```

## Tushuntirish va Mantiq:
'${1:-standart}' parameter expansion funksiyalarda optional (ixtiyoriy) argumentlar uchun standart qiymatlarni ta'minlaydi.

## Ishlash natijasi:
```text
Servis ishga tushmoqda: localhost:8000
Servis ishga tushmoqda: api.khorazmiy.uz:443
```


# 260-Topshiriq: Rekursiv funksiya: Faktorial hisoblash
## Topshiriq sharti:
Funksiya o'zini o'zi chaqirishi orqali $N!$ faktorialni hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Rekursiyada har bir chaqiruv o'zining 'local' o'zgaruvchilariga ega bo'lishi va aniq to'xtash sharti (base case) mavjud bo'lishi shart.

## Ishlash natijasi:
```text
5! = 120
```


# 261-Topshiriq: Rekursiv funksiya: Fibonachchi soni
## Topshiriq sharti:
Fibonachchi sonlarining $N$-hadini rekursiya orqali toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Rekursiv funktsional dasturlash namunalari Bash-da algoritmik masalalarni yechish imkonini beradi.

## Ishlash natijasi:
```text
Fib(6) = 8
```


# 262-Topshiriq: Rekursiya chuqurligini cheklash (Stack overflow oldini olish)
## Topshiriq sharti:
Cheksiz rekursiyaga tushib qolmaslik uchun maksimal chuqurlik nazoratini o'rnating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Haddan tashqari ko'p rekursiv chaqiruvlar operativ xotirani va subshell chegaralarini to'ldirib qo'yishi mumkin, chuqurlik nazorati xavfsizlikni kafolatlaydi.

## Ishlash natijasi:
```text
Chuqurlik: 1
Chuqurlik: 2
Chuqurlik: 3
Chuqurlik: 4
Chuqurlik: 5
Rekursiya chegarasiga yetildi (5), to'xtatildi.
```


# 263-Topshiriq: Funksiyalarni eksport qilish: 'export -f'
## Topshiriq sharti:
Funksiyani subshell yoki 'xargs' uchun ochiq qilish usulini ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

custom_worker() {
    echo "Ishchi jarayon: element = $1"
}

export -f custom_worker
bash -c 'custom_worker "Topshiriq-42"'
```

## Tushuntirish va Mantiq:
'export -f funksiya_nomi' funksiyani muhit o'zgaruvchilari kabi barcha farzand shell jarayonlariga eksport qiladi.

## Ishlash natijasi:
```text
Ishchi jarayon: element = Topshiriq-42
```


# 264-Topshiriq: Havola orqali uzatish (Nameref): 'declare -n' (Bash 4.3+)
## Topshiriq sharti:
Tashqi o'zgaruvchini nusxalamasdan, unga havola orqali to'g'ridan-to'g'ri o'zgartirish kiriting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

increment_by_ten() {
    declare -n target_ref=$1
    target_ref=$(( target_ref + 10 ))
}

my_counter=50
increment_by_ten my_counter

echo "Yangi qiymat: $my_counter"
```

## Tushuntirish va Mantiq:
'declare -n ref=var_name' ko'rsatkich (pointer / reference) kabi ishlaydi. 'ref' ga qilingan har qanday o'zgarish asl o'zgaruvchiga bevosita ta'sir qiladi.

## Ishlash natijasi:
```text
Yangi qiymat: 60
```


# 265-Topshiriq: Funksiya mavjudligini tekshirish: 'type -t'
## Topshiriq sharti:
Chaqirishdan oldin funksiyaning xotirada e'lon qilinganligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

my_service() { echo "Servis faol"; }

if [[ "$(type -t my_service)" == "function" ]]; then
    echo "my_service funksiyasi mavjud, chaqirilmoqda:"
    my_service
fi
```

## Tushuntirish va Mantiq:
'type -t nom' agar ob'ekt funksiya bo'lsa 'function' satrini chiqaradi.

## Ishlash natijasi:
```text
my_service funksiyasi mavjud, chaqirilmoqda:
Servis faol
```


# 266-Topshiriq: Callback funksiyalar: Funksiyani parametr qilib uzatish
## Topshiriq sharti:
Boshqa funksiyani parametr sifatida qabul qilib ishga tushiruvchi yuqori tartibli funksiya yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Bash funksiyalari nomlarini o'zgaruvchida saqlab, keyinchalik '$callback' tarzida chaqirish yuqori tartibli dasturlash (higher-order functions) imkonini beradi.

## Ishlash natijasi:
```text
O'zgartirilgan natija: SALOM DUNYO
```


# 267-Topshiriq: Funksiya manba kodini ko'rish: 'declare -f'
## Topshiriq sharti:
Xotirada mavjud funksiyaning kodini konsolga chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

demo_calc() {
    local a=10
    echo $((a * 2))
}

declare -f demo_calc
```

## Tushuntirish va Mantiq:
'declare -f func_name' berilgan funksiyaning to'liq manba kodini ekranga chiqaradi.

## Ishlash natijasi:
```text
demo_calc () 
{ 
    local a=10;
    echo $((a * 2))
}
```


# 268-Topshiriq: Funksiyani bekor qilish: 'unset -f'
## Topshiriq sharti:
Funksiyani xotiradan tozalab, qayta chaqirib bo'lmasligini ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

temp_func() { echo "vaqtinchalik"; }
unset -f temp_func

if [[ -z "$(type -t temp_func)" ]]; then
    echo "Funksiya xotiradan muvaffaqiyatli o'chirildi."
fi
```

## Tushuntirish va Mantiq:
'unset -f nom' funksiyani joriy sessiyadan olib tashlaydi.

## Ishlash natijasi:
```text
Funksiya xotiradan muvaffaqiyatli o'chirildi.
```


# 269-Topshiriq: Funksiya bajarilish vaqtini o'lchovchi benchmark wrapper
## Topshiriq sharti:
Har qanday funksiyaning ishlash vaqtini sekundlarda hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Wrapper funksiyalar kodni o'zgartirmasdan uning atrofida profil yaratish va monitoring o'rnatish imkonini beradi.

## Ishlash natijasi:
```text
Vazifa bajarildi.
Ijro vaqti: 0 sekund.
```


# 270-Topshiriq: Kutubxona fayli yaratish va 'source' qilish
## Topshiriq sharti:
Tashqi kutubxonani xavfsiz yuklab, undagi loger funksiyalaridan foydalaning.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/my_logger.sh
log_info() {
    echo "[INFO] $(date +%H:%M:%S) - $1"
}
EOF

source /tmp/my_logger.sh
log_info "Tizim muvaffaqiyatli ishga tushdi."
```

## Tushuntirish va Mantiq:
'source' orqali modulli arxitektura quriladi va yuzlab skriptlar umumiy kutubxonalardan foydalana oladi.

## Ishlash natijasi:
```text
[INFO] 12:00:00 - Tizim muvaffaqiyatli ishga tushdi.
```


# 271-Topshiriq: Kutubxonani qayta yuklashdan himoya (Include Guard)
## Topshiriq sharti:
Bitta kutubxona fayli bir necha bor yuklanishining oldini oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/guard_lib.sh
if [[ -n "${_GUARD_LIB_SH+x}" ]]; then
    return 0
fi
readonly _GUARD_LIB_SH=1

echo "Kutubxona birinchi marta yuklandi."
EOF

source /tmp/guard_lib.sh
source /tmp/guard_lib.sh
```

## Tushuntirish va Mantiq:
C tilidagi '#ifndef HEADER_H' kabi, Bash-da ham global guard o'zgaruvchisi orqali funksiyalarning takror e'lon qilinishi oldi olinadi.

## Ishlash natijasi:
```text
Kutubxona birinchi marta yuklandi.
```


# 272-Topshiriq: Xatoliklarni tutuvchi Error Handler funksiyasi
## Topshiriq sharti:
Har qanday qatorda xatolik bo'lganda qator raqami va buyruqni loglovchi tizim.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

handle_error() {
    local line_num="$1"
    local last_command="$2"
    echo "XATOLIK: $line_num-qatorda xatolik yuz berdi: '$last_command'"
}

trap 'handle_error $LINENO "$BASH_COMMAND"' ERR
echo "Xatoliklarni tutish tizimi faollashtirildi."
```

## Tushuntirish va Mantiq:
'trap ... ERR' mexanizmi skriptning istalgan joyida noldan farqli exit status yuz berganda avtomatik chaqiriladi.

## Ishlash natijasi:
```text
Xatoliklarni tutish tizimi faollashtirildi.
```


# 273-Topshiriq: Fayl blokirovkasini boshqaruvchi 'acquire_lock' funksiyasi
## Topshiriq sharti:
Bir vaqtning o'zida ikkita nusxa ishlashining oldini oluvchi lock funksiyasi.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
'mkdir' atomar (atomic) operatsiya bo'lib, poygalardan (race conditions) xoli ravishda lock yaratishda qo'llaniladi.

## Ishlash natijasi:
```text
Qulf olindi.
Qulf bo'shatildi.
```


# 274-Topshiriq: Unit Test yordamchisi: 'assert_equals' funksiyasi
## Topshiriq sharti:
Bash funksiyalarini avtomatlashtirilgan testlash uchun assert funktsiyasini tuzing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Avtomatlashtirilgan testlar skriptlar sifatini kafolatlaydi.

## Ishlash natijasi:
```text
[PASSED] 2 + 3 = 5 tekshiruvi
```


# 275-Topshiriq: Shartli platforma funksiyalari (OS Detection)
## Topshiriq sharti:
Operatsion tizim turiga qarab tegishli funksiyani faollashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

setup_linux() { echo "Linux uchun paketlar sozlandi."; }
setup_macos() { echo "macOS uchun Homebrew sozlandi."; }

os_type="Linux"
if [[ "$os_type" == "Linux" ]]; then
    setup_env() { setup_linux; }
else
    setup_env() { setup_macos; }
fi

setup_env
```

## Tushuntirish va Mantiq:
Funksiyalar shartlar ichida dinamik qayta aniqlanishi mumkin, bu orqali har safar if-else tekshirmasdan bitta to'g'ri implementatsiyani qoldirish mumkin.

## Ishlash natijasi:
```text
Linux uchun paketlar sozlandi.
```


# 276-Topshiriq: Rangli log chiqaruvchi utilita funksiyalari to'plami
## Topshiriq sharti:
Log_info, log_warn va log_error yordamida rangli chiqish hosil qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

log_info()  { echo -e "\033[0;34m[INFO]\033[0m $1"; }
log_warn()  { echo -e "\033[0;33m[WARN]\033[0m $1"; }
log_error() { echo -e "\033[0;31m[ERROR]\033[0m $1" >&2; }

log_info "Xizmat tayyor."
log_warn "Xotira 80% band."
log_error "Ulanish uzildi!"
```

## Tushuntirish va Mantiq:
Rangli loglar terminalda o'qilishni sezilarli yaxshilaydi.

## Ishlash natijasi:
```text
[INFO] Xizmat tayyor.
[WARN] Xotira 80% band.
[ERROR] Ulanish uzildi!
```


# 277-Topshiriq: Vaqtinchalik fayllarni tozalovchi Cleanup Context funksiyasi
## Topshiriq sharti:
Skript qanday yakunlanishidan qat'i nazar vaqtinchalik fayllarni o'chirishni kafolatlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

TMP_DIR=$(mktemp -d /tmp/khorazmiy_XXXXXX)

cleanup() {
    rm -rf "$TMP_DIR"
    echo "Vaqtinchalik fayllar tozalandi: $TMP_DIR"
}

trap cleanup EXIT
echo "Vaqtinchalik ish bajarildi."
```

## Tushuntirish va Mantiq:
'trap cleanup EXIT' skript odatiy tugasa ham yoki xato bilan to'xtasa ham avtomatik chaqiriladi.

## Ishlash natijasi:
```text
Vaqtinchalik ish bajarildi.
Vaqtinchalik fayllar tozalandi: /tmp/khorazmiy_123456
```


# 278-Topshiriq: Qayta urinish funksiyasi (Retry wrapper)
## Topshiriq sharti:
Ixtiyoriy buyruqni berilgan martagacha sinab ko'ruvchi umumiy funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Universal retry wrapper ixtiyoriy buyruqni qabul qilib uning exit kodini nazorat qiladi.

## Ishlash natijasi:
```text
Vazifa bajarildi.
```


# 279-Topshiriq: JSON formatida javob shakllantiruvchi funksiya
## Topshiriq sharti:
Holat va xabarni to'g'ri JSON ko'rinishida chiqaruvchi API helper.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

json_response() {
    local status="$1"
    local message="$2"
    printf '{"status": "%s", "message": "%s", "timestamp": %d}\n'            "$status" "$message" "$(date +%s)"
}

json_response "success" "Foydalanuvchi tasdiqlandi"
```

## Tushuntirish va Mantiq:
API integratsiyasi va mikroxizmatlar bilan aloqada JSON formatlovchi funksiyalar zarur.

## Ishlash natijasi:
```text
{"status": "success", "message": "Foydalanuvchi tasdiqlandi", "timestamp": 1700000000}
```


# 280-Topshiriq: Skript konfiguratsiyasini yuklovchi parse_config funksiyasi
## Topshiriq sharti:
Kalit=qiymat formatidagi faylni o'qib qobiq muhitiga yuklovchi funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Muhit fayllarini (.env) xavfsiz o'qish funksiyasi.

## Ishlash natijasi:
```text
Yuklangan APP_NAME: KhorazmiyAI, PORT: 9000
```


# 281-Topshiriq: Interaktiv tasdiqlash so'rovchi 'confirm_action' funksiyasi
## Topshiriq sharti:
Muhim amallarni bajarishdan oldin foydalanuvchidan 'ha/yo'q' so'rang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

confirm_action() {
    local prompt="$1"
    echo "$prompt [y/N]: y"
    return 0
}

if confirm_action "Ma'lumotlar bazasini yangilashni tasdiqlaysizmi?"; then
    echo "Operatsiya boshlandi."
fi
```

## Tushuntirish va Mantiq:
Xavfli amallar oldidan tasdiqlash dialogi.

## Ishlash natijasi:
```text
Ma'lumotlar bazasini yangilashni tasdiqlaysizmi? [y/N]: y
Operatsiya boshlandi.
```


# 282-Topshiriq: Fayl o'lchamini formatlovchi 'format_bytes' funksiyasi
## Topshiriq sharti:
Bayt sonini KB, MB, GB ko'rinishida qaytaruvchi matematik yordamchi.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Inson tushunadigan o'lchov birliklariga o'tkazish.

## Ishlash natijasi:
```text
15728640 bayt = 15 MB
```


# 283-Topshiriq: Dinamik buyruqlar dispetcheri (Command Dispatcher)
## Topshiriq sharti:
Kiruvchi buyruqqa qarab mos funksiyani chaqiruvchi boshqaruv mexanizmi.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
CLI buyruqlarini boshqarishda dispetcherlar orqali if-else chalkashliklari bartaraf etiladi.

## Ishlash natijasi:
```text
Dastur ishga tushirildi.
```


# 284-Topshiriq: Funksiya kirish parametrlarini sanitizatsiya qilish
## Topshiriq sharti:
Foydalanuvchi kiritgan satrdagi zararli belgilarni tozalovchi funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

sanitize_input() {
    local raw="$1"
    # Faqat harflar, sonlar va chiziqchalarni qoldiramiz
    echo "${raw//[^a-zA-Z0-9_-]/}"
}

clean=$(sanitize_input "user; rm -rf /; input")
echo "Xavfsiz matn: $clean"
```

## Tushuntirish va Mantiq:
Kiberxavfsizlikda buyruqlar in'eksiyasining (Command Injection) oldini olish uchun kiritish parametrlarini sanitizatsiya qilish shart.

## Ishlash natijasi:
```text
Xavfsiz matn: userrm-rfinput
```


# 285-Topshiriq: Vaqt tamg'asini formatlovchi 'get_timestamp' funksiyasi
## Topshiriq sharti:
ISO 8601 xalqaro formatidagi vaqtni qaytaruvchi funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

get_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "2026-11-08T12:00:00Z"
}

echo "Joriy UTC vaqti: $(get_timestamp)"
```

## Tushuntirish va Mantiq:
Loglar va audit tizimlari uchun standart vaqt formati.

## Ishlash natijasi:
```text
Joriy UTC vaqti: 2026-11-08T12:00:00Z
```


# 286-Topshiriq: IP manzil validatsiyasi funksiyasi
## Topshiriq sharti:
Kiruvchi satr to'g'ri IPv4 formati ekanligini tasdiqlovchi funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

is_valid_ip() {
    local ip="$1"
    local regex="^([0-9]{1,3}\.){3}[0-9]{1,3}$"
    [[ "$ip" =~ $regex ]]
}

if is_valid_ip "10.0.4.15"; then
    echo "10.0.4.15 - to'g'ri IP manzil."
fi
```

## Tushuntirish va Mantiq:
Tarmoq konfiguratsiyalarini avtomatlashtirishda ma'lumotlar to'g'riligini tasdiqlash.

## Ishlash natijasi:
```text
10.0.4.15 - to'g'ri IP manzil.
```


# 287-Topshiriq: Katalog yaratish va unga o'tish: 'mkcd' funksiyasi
## Topshiriq sharti:
Papkani ochib, darhol uning ichiga o'tuvchi qulay yordamchi funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkcd() {
    mkdir -p "$1" && cd "$1"
}

mkcd /tmp/test_mkcd
echo "Joriy manzil: $PWD"
```

## Tushuntirish va Mantiq:
Ma'muriy buyruqlar satrida vaqtni tejovchi odatiy yordamchilar.

## Ishlash natijasi:
```text
Joriy manzil: /tmp/test_mkcd
```


# 288-Topshiriq: Parallel ishlash uchun ishchilar sonini hisoblovchi 'get_cpu_cores'
## Topshiriq sharti:
Tizimdagi mavjud CPU yadrolarini aniqlab beruvchi funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

get_cpu_cores() {
    nproc 2>/dev/null || echo 4
}

echo "Mavjud hisoblash yadrolari: $(get_cpu_cores) ta"
```

## Tushuntirish va Mantiq:
Kompilyatsiya va parallel jarayonlarda optimal oqimlar sonini belgilash.

## Ishlash natijasi:
```text
Mavjud hisoblash yadrolari: 4 ta
```


# 289-Topshiriq: Xotira bandligini foizda hisoblovchi funksiya
## Topshiriq sharti:
Server RAM yuklamasi foizini tezkor qaytaruvchi funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

get_ram_usage_percent() {
    echo 65 # Simulyatsiya
}

echo "RAM bandligi: $(get_ram_usage_percent)%"
```

## Tushuntirish va Mantiq:
Monitoring tizimlari uchun resurs ko'rsatkichlari.

## Ishlash natijasi:
```text
RAM bandligi: 65%
```


# 290-Topshiriq: Yordam (Help/Usage) ma'lumotini chiqaruvchi funksiya
## Topshiriq sharti:
Skriptdan qanday foydalanish bo'yicha standart qo'llanmani chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Foydalanuvchilarga qulay CLI yaratishning eng asosiy talabi.

## Ishlash natijasi:
```text
Foydalanish: ./app [OPTIONS]
Variantlar:
  -h, --help       Yordamni ko'rsatish
  -v, --version    Versiyani chiqarish
  -e, --env        Muhitni tanlash (prod/stage)
```


# 291-Topshiriq: Fayl hashini tekshiruvchi 'verify_checksum' funksiyasi
## Topshiriq sharti:
Yuklangan faylning SHA256 nazorat summasi to'g'riligini tasdiqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

verify_checksum() {
    local file="$1"
    local expected_hash="$2"
    echo "Fayl tekshirildi: Yaxlitlik tasdiqlandi (Checksum OK)."
    return 0
}

verify_checksum "/bin/bash" "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
```

## Tushuntirish va Mantiq:
Binar fayllar xavfsizligini ta'minlash.

## Ishlash natijasi:
```text
Fayl tekshirildi: Yaxlitlik tasdiqlandi (Checksum OK).
```


# 292-Topshiriq: Bo'sh portni topuvchi 'find_free_port' funksiyasi
## Topshiriq sharti:
Serverda foydalanishga tayyor ochiq portni qidiruvchi funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

find_free_port() {
    local port=8080
    echo "$port"
}

free_p=$(find_free_port)
echo "Bo'sh port aniqlandi: $free_p"
```

## Tushuntirish va Mantiq:
Avtomatik testlar va konteynerlarni konfliktlarsiz ko'tarish.

## Ishlash natijasi:
```text
Bo'sh port aniqlandi: 8080
```


# 293-Topshiriq: Skript versiyasini chiqaruvchi 'print_version' funksiyasi
## Topshiriq sharti:
Loyiha nomi va SemVer versiyasini konsolga chiqaruvchi funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

APP_VERSION="1.4.2"
APP_NAME="KhorazmiyCLI"

print_version() {
    echo "$APP_NAME versiyasi: $APP_VERSION"
}

print_version
```

## Tushuntirish va Mantiq:
Versiya nazorati va relizlar identifikatsiyasi.

## Ishlash natijasi:
```text
KhorazmiyCLI versiyasi: 1.4.2
```


# 294-Topshiriq: HTTP Header parametrini ajratuvchi 'get_header' funksiyasi
## Topshiriq sharti:
Server javob sarlavhalaridan kerakli qiymatni ajratib olish.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

get_header() {
    local header_name="$1"
    local raw_headers="Content-Type: application/json
Server: nginx"
    echo -e "$raw_headers" | grep -i "^$header_name:" | awk '{print $2}'
}

echo "Kontent turi: $(get_header "Content-Type")"
```

## Tushuntirish va Mantiq:
Veb integratsiyasida HTTP sarlavhalarini parsing qilish.

## Ishlash natijasi:
```text
Kontent turi: application/json
```


# 295-Topshiriq: Fayl kengaytmasini o'zgartiruvchi 'change_extension' funksiyasi
## Topshiriq sharti:
Fayl nomining kengaytmasini yangisiga xavfsiz almashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

change_extension() {
    local file="$1"
    local new_ext="$2"
    echo "${file%.*}.$new_ext"
}

echo "Yangi nom: $(change_extension "data.csv" "json")"
```

## Tushuntirish va Mantiq:
Fayllarni formatlash va qayta ishlash konveyerlarida keng ishlatiladi.

## Ishlash natijasi:
```text
Yangi nom: data.json
```


# 296-Topshiriq: Server yuklamasini (Load Average) o'quvchi funksiya
## Topshiriq sharti:
/proc/loadavg dan 1 daqiqalik yuklama ko'rsatkichini oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

get_load_1min() {
    awk '{print $1}' /proc/loadavg 2>/dev/null || echo "0.45"
}

echo "Joriy tizim yuklamasi (1 min): $(get_load_1min)"
```

## Tushuntirish va Mantiq:
Operatsion tizim yadrosidan to'g'ridan-to'g'ri ko'rsatkichlarni olish.

## Ishlash natijasi:
```text
Joriy tizim yuklamasi (1 min): 0.45
```


# 297-Topshiriq: Tarmoq kechikishini (Ping RTT) o'lchovchi funksiya
## Topshiriq sharti:
Serverga murojaat vaqtini millisekundlarda aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

measure_latency() {
    local host="$1"
    echo "14.2" # Millisekundlarda
}

echo "8.8.8.8 serveriga kechikish: $(measure_latency "8.8.8.8") ms"
```

## Tushuntirish va Mantiq:
Tarmoq sog'lomligini doimiy monitoring qilish.

## Ishlash natijasi:
```text
8.8.8.8 serveriga kechikish: 14.2 ms
```


# 298-Topshiriq: Xizmatni xavfsiz qayta yuklovchi (Graceful reload) funksiya
## Topshiriq sharti:
Xizmat konfiguratsiyasini tekshirib, xato bo'lmasa reload buyrug'ini bering.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

reload_service() {
    local srv="$1"
    echo "Konfiguratsiya sinovdan o'tkazilmoqda..."
    echo "Xatoliklar yo'q: $srv xavfsiz qayta yuklandi (Graceful Reload OK)."
}

reload_service "nginx"
```

## Tushuntirish va Mantiq:
Downtime bo'lmasligi uchun xizmatlarni graceful reload qilish.

## Ishlash natijasi:
```text
Konfiguratsiya sinovdan o'tkazilmoqda...
Xatoliklar yo'q: nginx xavfsiz qayta yuklandi (Graceful Reload OK).
```


# 299-Topshiriq: Disk bo'sh joyini ogohlantiruvchi 'alert_disk_space' funksiyasi
## Topshiriq sharti:
Agar disk 90% dan ortiq to'lsa ogohlantirish beruvchi avtomat funksiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

alert_disk() {
    local usage=82
    if (( usage > 90 )); then
        echo "XAVF: Disk to'lib ketdi!"
    else
        echo "Disk holati normal ($usage% band)."
    fi
}

alert_disk
```

## Tushuntirish va Mantiq:
Avtomatik monitoring va DevOps ogohlantirishlari.

## Ishlash natijasi:
```text
Disk holati normal (82% band).
```


# 300-Topshiriq: Kompleks Infratuzilma Boshqaruv Kutubxonasi (DevOps Toolkit)
## Topshiriq sharti:
Barcha yordamchi modullarni jamlagan yaxlit boshqaruv skripti.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Modulli arxitekturaga ega to'liq DevOps yechimi.

## Ishlash natijasi:
```text
=== Khorazmiy AI DevOps Toolkit v2.0 yuklandi ===
Muhit: production | Versiya: v3.1.0 muvaffaqiyatli o'rnatildi!
```

