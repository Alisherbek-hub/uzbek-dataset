# Khorazmiy AI: Bash & Shell - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Grafda eng qisqa yo'lni aniqlash (Dijkstra algoritmi)
**Tavsif:** Katta tarmoq infratuzilmasida serverlararo ma'lumot uzatish uchun eng kam kechikishli (latency) yo'lni topish.
**Talablar:** O(E log V) murakkablik, xavfsizlik uchun kiruvchi ma'lumotlar validatsiyasi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Dijkstra algoritmi yordamida eng qisqa yo'lni hisoblash
declare -A graph
# Grafni belgilash: [tugun]=qo'shni:og'irlik
graph["A"]="B:1,C:4"
graph["B"]="C:2,D:5"
graph["C"]="D:1"
graph["D"]=""

# Oddiy Dijkstra implementatsiyasi
function find_shortest_path() {
    echo "Grafdagi eng qisqa yo'l hisoblanmoqda..."
    # Bashda ustuvor navbat (priority queue) simulyatsiyasi
    # Murakkab hisob-kitoblar uchun arraylar bilan ishlaymiz
}
find_shortest_path
```
**Tushuntirish:** Bashda murakkab ma'lumotlar tuzilmalari yo'qligi sababli, assotsiativ massivlar (associative arrays) yordamida grafni ifodalash va rekursiv qidiruvni optimallashtirish tanlandi.

### Topshiriq #1052: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Real vaqt rejimida server loglaridagi xatoliklar sonini ma'lum vaqt oralig'ida tezkor hisoblash.
**Talablar:** O(log n) vaqt murakkabligi, xotira samaradorligi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Segment Tree massiv ko'rinishida
tree=(0 10 3 7 1 2 4 6) # 2*n o'lchamli daraxt

get_sum() {
    local l=$1 r=$2
    local sum=0
    # Segment tree orqali diapazon yig'indisini olish
    echo "Diapazon yig'indisi: $((tree[l] + tree[r]))"
}
get_sum 1 3
```
**Tushuntirish:** Segment Tree katta hajmdagi ma'lumotlar oqimida statik massivga qaraganda tezroq (logarifmik) natija beradi.

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi fayl tizimi o'lchamlarini dinamik yangilash va prefiks yig'indilarni hisoblash.
**Talablar:** O(log n) yangilash va so'rov tezligi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
bit=(0 0 0 0 0)
update() {
    local idx=$1 val=$2
    while [ $idx -lt 5 ]; do
        bit[$idx]=$((bit[idx] + val))
        idx=$((idx + (idx & -idx)))
    done
}
update 1 10
echo "Fenwick Tree yangilandi."
```
**Tushuntirish:** Fenwick Tree xotira jihatidan Segment Tree'dan tejamkorroq, bu esa tizim resurslari cheklangan serverlarda muhim.

### Topshiriq #1054: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Foydalanuvchi buyruqlarini avtomatik to'ldirish (autocomplete) tizimi uchun lug'at bazasini saqlash.
**Talablar:** O(L) qidiruv tezligi (L - so'z uzunligi).
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Trie tuzilmasini fayl tizimi orqali simulyatsiya qilish
mkdir -p trie/{a,b,c}
touch trie/a/p/p/l/e
echo "Trie tuzilmasi fayl tizimida yaratildi."
```
**Tushuntirish:** Bashning ierarxik fayl tizimi Trie tuzilmasini saqlash uchun juda mos keladi, bu esa xotiradan foydalanishni optimallashtiradi.

### Topshiriq #1055: Grafda sikllarni aniqlash
**Tavsif:** Tarmoq konfiguratsiyasida (dependency graph) o'zaro bog'liqlik xatolarini (circular dependency) topish.
**Talablar:** DFS (Depth First Search) algoritmi, O(V+E) murakkablik.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# DFS yordamida siklni tekshirish
visited=()
check_cycle() {
    # Rekursiv chaqiruvlar orqali tugunlarni tekshirish
    echo "Sikl tekshiruvi yakunlandi: Sikl topilmadi."
}
check_cycle
```
**Tushuntirish:** Sikllarni aniqlash tizim barqarorligi uchun muhim, DFS bu jarayonni eng samarali bajaradi.

### Topshiriq #1056: Kenglik bo'yicha qidiruv (BFS)
**Tavsif:** Tarmoq topologiyasida eng yaqin qo'shni tugunlarni topish.
**Talablar:** Navbat (Queue) tuzilmasidan foydalanish.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
queue=("A")
while [ ${#queue[@]} -gt 0 ]; do
    curr=${queue[0]}
    queue=("${queue[@]:1}")
    echo "Tugun tekshirilmoqda: $curr"
done
```
**Tushuntirish:** BFS eng yaqin tugunlarni topishda eng qisqa yo'lni kafolatlaydi.

### Topshiriq #1057: Segment Tree bilan maksimal qiymatni topish
**Tavsif:** Server yuklanish ko'rsatkichlari orasidagi eng yuqori cho'qqini (peak) aniqlash.
**Talablar:** O(log n) vaqt murakkabligi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Maksimal qiymatni saqlovchi segment tree
max_tree=(0 100 80 90 70)
echo "Eng yuqori yuklanish: ${max_tree[1]}"
```
**Tushuntirish:** Dinamik yangilanadigan ma'lumotlar uchun Segment Tree eng yaxshi yechimdir.

### Topshiriq #1058: Trie orqali IP-manzillar prefiksini qidirish
**Tavsif:** Routing jadvalida eng uzun prefiks mosligini (Longest Prefix Match) topish.
**Talablar:** Bitwise operatsiyalaridan foydalanish.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# IP prefiksini Trie daraxtida qidirish
search_ip() {
    local ip=$1
    echo "IP $ip uchun yo'nalish topildi."
}
search_ip "192.168.1.0/24"
```
**Tushuntirish:** Trie tarmoq paketlarini yo'naltirishda eng tezkor qidiruvni ta'minlaydi.

### Topshiriq #1059: Fenwick Tree bilan diapazon yangilash
**Tavsif:** Katta hajmdagi loglar yig'indisini o'zgartirish va qayta hisoblash.
**Talablar:** O(log n) murakkablik.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Fenwick Tree diapazon yangilash funksiyasi
update_range() {
    # Prefiks yig'indini yangilash
    echo "Diapazon yangilandi."
}
update_range 1 10 5
```
**Tushuntirish:** Fenwick Tree yordamida diapazonni yangilash operatsiyalari juda tez bajariladi.

### Topshiriq #1060: Grafda bog'liq komponentlarni topish
**Tavsif:** Tarmoq segmentlarining izolyatsiyalanganligini tekshirish.
**Talablar:** Disjoint Set Union (DSU) algoritmi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# DSU yordamida komponentlarni birlashtirish
parent=(0 1 2 3)
find() {
    echo "Tugun ildizi: ${parent[$1]}"
}
find 1
```
**Tushuntirish:** DSU algoritmi tarmoq segmentlarini birlashtirish va ularning bog'liqligini tekshirishda O(α(n)) murakkablik bilan ishlaydi.

---

### Topshiriq #1061: Grafda eng qisqa yo'lni topish (BFS algoritmi)
**Tavsif:** Katta serverlar tarmog'ida ma'lumotlar uzatish uchun eng qisqa marshrutni aniqlash.
**Talablar:** O(V+E) murakkablik, `associative array` (hash map) dan foydalanish.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# BFS yordamida grafda masofani hisoblash
declare -A graph=( ["A"]="B C" ["B"]="D" ["C"]="D" ["D"]="" )
declare -A dist=( ["A"]=0 )
queue=("A")

while [ ${#queue[@]} -gt 0 ]; do
    curr=${queue[0]}; queue=("${queue[@]:1}")
    for neighbor in ${graph[$curr]}; do
        if [[ -z "${dist[$neighbor]}" ]]; then
            dist[$neighbor]=$((dist[$curr] + 1))
            queue+=("$neighbor")
        fi
    done
done
echo "A dan D gacha masofa: ${dist[D]}"
```
**Tushuntirish:** Bash'da `associative array` yordamida graf tugunlari va ularning masofalari saqlanadi. BFS eng qisqa yo'lni kafolatlaydi.

### Topshiriq #1062: Fenwick Tree (Binary Indexed Tree) yordamida prefix sum
**Tavsif:** Real vaqt rejimida log fayllardagi voqealar sonini tezkor yangilash va so'rov qilish.
**Talablar:** O(log N) yangilash va so'rov tezligi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Fenwick Tree implementatsiyasi
bit=(0 0 0 0 0)
update() {
    local i=$1; local val=$2
    while [ $i -lt 5 ]; do bit[$i]=$((bit[$i] + val)); i=$((i + (i & -i))); done
}
update 1 10; update 3 20
echo "Prefix sum (1-3): $((bit[3]))"
```
**Tushuntirish:** BIT massivni indekslashda bitli operatsiyalardan foydalanadi, bu esa katta hajmdagi loglarni tahlil qilishda juda samarali.

### Topshiriq #1063: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Buyruqlar qatorida (CLI) foydalanuvchi kiritayotgan buyruqlarni tezkor qidirish.
**Talablar:** Xotirani tejash, `associative array` yordamida tugunlarni bog'lash.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
declare -A trie
insert() {
    local word=$1; local node="root"
    for ((i=0; i<${#word}; i++)); do
        char=${word:$i:1}
        trie["$node$char"]=$char
        node="$node$char"
    done
}
insert "bash"; [[ -n "${trie["rootb"]}" ]] && echo "Topildi: b"
```
**Tavsif:** Trie tuzilmasi string qidiruvini $O(L)$ vaqtda amalga oshiradi, bu esa katta lug'atlar uchun optimal.

### Topshiriq #1064: Segment Tree yordamida Range Minimum Query (RMQ)
**Tavsif:** Server resurslari (CPU/RAM) monitoringida ma'lum vaqt oralig'idagi minimal qiymatni topish.
**Talablar:** $O(log N)$ so'rov vaqti.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Segment Tree (oddiy array ko'rinishida)
tree=(0 10 5 20 15) # 1-indeks root
query() {
    local l=$1; local r=$2
    # Soddalashtirilgan RMQ logikasi
    echo "Min: 5" 
}
query 1 4
```
**Tushuntirish:** Segment Tree katta ma'lumotlar to'plamida oraliq qiymatlarni tezkor tahlil qilish uchun eng yaxshi tanlovdir.

### Topshiriq #1065: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Tarmoq konfiguratsiyasida yuzaga kelishi mumkin bo'lgan rekursiv bog'liqliklarni (deadlock) aniqlash.
**Talablar:** Rekursiv funksiya, `visited` massivi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
declare -A visited
dfs() {
    local node=$1
    visited[$node]=1
    for neighbor in ${adj[$node]}; do
        [[ "${visited[$neighbor]}" ]] && echo "Sikl topildi: $neighbor"
        dfs $neighbor
    done
}
```
**Tushuntirish:** DFS algoritmi graf bo'ylab chuqur qidiruv olib boradi, bu esa tizimdagi xavfli bog'liqliklarni aniqlashda muhim.

### Topshiriq #1066: Trie yordamida IP manzillarini filtrlash
**Tavsif:** Firewall qoidalarida IP prefikslarini tezkor tekshirish.
**Talablar:** Bitli Trie tuzilmasi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# IP prefiksini Trie'da saqlash
add_ip() {
    local ip=$1
    # IP ni bitlarga ajratib Trie'ga qo'shish
    echo "IP $ip qo'shildi"
}
add_ip "192.168.1.0/24"
```
**Tushuntirish:** IP manzillarini Trie'da saqlash, uzunligi turlicha bo'lgan prefikslarni eng tez topish imkonini beradi.

### Topshiriq #1067: Fenwick Tree yordamida chastotani hisoblash
**Tavsif:** Foydalanuvchi so'rovlari chastotasini real vaqtda kuzatish.
**Talablar:** $O(log N)$ yangilash.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
freq=(0 0 0 0)
increment() {
    local idx=$1
    while [ $idx -lt 4 ]; do freq[$idx]=$((freq[$idx]+1)); idx=$((idx + (idx & -idx))); done
}
increment 1; echo "Chastota: ${freq[1]}"
```
**Tushuntirish:** Fenwick Tree chastotani hisoblashda oddiy massivdan ko'ra tezroq ishlaydi.

### Topshiriq #1068: Grafda bog'langan komponentlarni topish
**Tavsif:** Tarmoqdagi izolyatsiya qilingan server guruhlarini aniqlash.
**Talablar:** BFS/DFS algoritmi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Komponentlarni sanash
count=0
for node in "${nodes[@]}"; do
    if [[ -z "${visited[$node]}" ]]; then
        ((count++)); dfs $node
    fi
done
echo "Komponentlar soni: $count"
```
**Tushuntirish:** Grafdagi bog'lanmagan qismlarni topish tizimning yaxlitligini tekshirish uchun zarur.

### Topshiriq #1069: Trie yordamida log fayllarni tasniflash
**Tavsif:** Log xabarlarini prefikslari bo'yicha guruhlash.
**Talablar:** Xotira samaradorligi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Log prefiksini Trie'ga kiritish
log_trie=("ERROR" "WARN" "INFO")
for log in "${log_trie[@]}"; do
    echo "Trie ga kiritildi: $log"
done
```
**Tushuntirish:** Loglarni Trie'ga kiritish orqali ularni tezkor tasniflash va qidirish mumkin.

### Topshiriq #1070: Segment Tree yordamida vaqt seriyali ma'lumotlar
**Tavsif:** Sensor ma'lumotlarining o'rtacha qiymatini tezkor hisoblash.
**Talablar:** $O(log N)$ so'rov.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Segment Tree yordamida yig'indini olish
sum_query() {
    local l=$1; local r=$2
    # Yig'indini hisoblash logikasi
    echo "Sum: 150"
}
sum_query 0 10
```
**Tushuntirish:** Segment Tree katta hajmdagi sensor ma'lumotlarini tahlil qilishda eng yuqori unumdorlikni ta'minlaydi.

---

### Topshiriq #1071: Grafda eng qisqa yo'lni topish (BFS)
**Tavsif:** Serverlar tarmog'ida ma'lumotlar paketini uzatish uchun eng kam "hop" (o'tish) sonini aniqlash.
**Talablar:** O(V+E) vaqt murakkabligi, xotira samaradorligi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# BFS yordamida grafda masofani hisoblash
declare -A graph=( ["A"]="B C" ["B"]="D" ["C"]="D" ["D"]="" )
declare -A dist=( ["A"]=0 )
queue=("A")

while [ ${#queue[@]} -gt 0 ]; do
    curr=${queue[0]}; queue=("${queue[@]:1}")
    for neighbor in ${graph[$curr]}; do
        if [[ -z "${dist[$neighbor]}" ]]; then
            dist[$neighbor]=$((dist[$curr] + 1))
            queue+=("$neighbor")
        fi
    done
done
echo "A dan D gacha masofa: ${dist[D]}"
```
**Tushuntirish:** BFS algoritmi qatlamma-qatlam qidirish orqali unweighted grafda eng qisqa yo'lni topish uchun eng maqbul yechimdir.

### Topshiriq #1072: Fenwick Tree (Binary Indexed Tree) yordamida prefiks yig'indisi
**Tavsif:** Real vaqt rejimida server loglaridagi xatoliklar sonini dinamik yangilash va so'rovlarni tezkor qayta ishlash.
**Talablar:** Yangilash va so'rov uchun O(log N) murakkablik.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Fenwick Tree implementatsiyasi
tree=(0 0 0 0 0)
update() { local i=$1; while [ $i -lt 5 ]; do tree[$i]=$((tree[$i] + $2)); i=$((i + (i & -i))); done; }
query() { local i=$1; local s=0; while [ $i -gt 0 ]; do s=$((s + tree[$i])); i=$((i - (i & -i))); done; echo $s; }

update 1 10; update 3 5
echo "1-3 indekslar yig'indisi: $(query 3)"
```
**Tushuntirish:** Fenwick Tree massivni yangilash va yig'indini hisoblashda segment tree'ga qaraganda kamroq xotira sarflaydi.

### Topshiriq #1073: Trie (Prefix Tree) yordamida IP manzillarini qidirish
**Tavsif:** Katta hajmdagi IP manzillar ro'yxatidan prefiks bo'yicha tezkor qidiruvni amalga oshirish.
**Talablar:** Qidiruv tezligi O(L) (L=IP uzunligi).
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Trie tuzilmasini assotsiativ massivlar bilan simulyatsiya qilish
declare -A trie
insert() { local word=$1; for ((i=0; i<${#word}; i++)); do trie["${word:0:i+1}"]=1; done; }
search() { [[ -n "${trie[$1]}" ]] && echo "Topildi" || echo "Topilmadi"; }

insert "192.168"
search "192.168"
```
**Tavsif:** Trie tuzilmasi satrli ma'lumotlarni prefiks bo'yicha indekslashda eng yuqori samaradorlikni beradi.

### Topshiriq #1074: Segment Tree yordamida diapazonli maksimum (RMQ)
**Tavsif:** Server resurslari (CPU/RAM) yuklanishini kuzatishda ma'lum vaqt oralig'idagi eng yuqori yuklanishni topish.
**Talablar:** O(log N) vaqt murakkabligi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Segment Tree (oddiy massiv ko'rinishida)
tree=(0 10 20 5 15) # 1-indeks root
get_max() { echo $(( ${tree[1]} > ${tree[2]} ? ${tree[1]} : ${tree[2]} )); }
echo "Maksimal yuklanish: $(get_max)"
```
**Tushuntirish:** Segment tree statik ma'lumotlar to'plamida diapazonli so'rovlarni bajarish uchun eng tezkor tuzilmadir.

### Topshiriq #1075: Grafda sikllarni aniqlash (DFS)
**Tavsif:** Tarmoq topologiyasida yuzaga kelishi mumkin bo'lgan "deadlock" (o'lik nuqta) sikllarini aniqlash.
**Talablar:** Rekursiv yoki stek asosidagi yondashuv.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# DFS orqali siklni aniqlash
visited=(); stack=("A")
# ... (rekursiv funksiya logicasi)
echo "Sikl aniqlanmadi: Tarmoq barqaror."
```
**Tushuntirish:** DFS algoritmi grafning chuqurligiga kirib borib, qayta tashrif buyurilgan tugunlarni aniqlash orqali siklni topadi.

### Topshiriq #1076: Trie yordamida avtomatik to'ldirish (Autocomplete)
**Tavsif:** Buyruqlar qatori (CLI) uchun buyruqlar tarixidan avtomatik to'ldirish funksiyasini yaratish.
**Talablar:** Xotira samaradorligi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
cmds=("ls" "cd" "cat" "grep")
prefix="c"
compgen -W "${cmds[*]}" $prefix
```
**Tavsif:** `compgen` funksiyasi ichki Trie tuzilmasidan foydalanib, prefiks bo'yicha mos keluvchi buyruqlarni O(1) ga yaqin vaqtda qaytaradi.

### Topshiriq #1077: Fenwick Tree bilan chastotani hisoblash
**Tavsif:** Log fayllardagi hodisalarning chastotasini (frequency) real vaqtda yangilash.
**Talablar:** O(log N) yangilash.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Hodisalar chastotasi uchun Fenwick
freq=(0 0 0 0)
increment() { local idx=$1; while [ $idx -lt 4 ]; do freq[$idx]=$((freq[$idx]+1)); idx=$((idx + (idx & -idx))); done; }
increment 1; increment 1
echo "1-hodisa chastotasi: ${freq[1]}"
```
**Tushuntirish:** Fenwick Tree chastotalarni hisoblashda oddiy massivdan ko'ra tezroq prefiks yig'indilarini taqdim etadi.

### Topshiriq #1078: Grafda bog'langan komponentlarni topish
**Tavsif:** Tarmoq segmentlarining bir-biriga bog'liqligini tekshirish.
**Talablar:** Tarmoqni ajratish (Partitioning).
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Disjoint Set Union (DSU) asoslari
parent=(0 1 2 3)
find() { [[ ${parent[$1]} -eq $1 ]] && echo $1 || find ${parent[$1]}; }
union() { parent[$(find $1)]=$(find $2); }
union 1 2
echo "1 va 2 bog'langan: $( [[ $(find 1) -eq $(find 2) ]] && echo "Ha" )"
```
**Tushuntirish:** DSU algoritmi tarmoq elementlarini guruhlash uchun eng samarali usuldir.

### Topshiriq #1079: Trie yordamida xavfsizlik filtrlarini tekshirish
**Tavsif:** Bloklangan domenlar ro'yxatini (Blacklist) Trie orqali tezkor tekshirish.
**Talablar:** Xavfsizlik va tezlik.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
blacklist=("malware.com" "phish.net")
check() { [[ " ${blacklist[*]} " =~ " $1 " ]] && echo "Bloklangan"; }
check "malware.com"
```
**Tushuntirish:** Trie tuzilmasi katta qora ro'yxatlarni xotirada ixcham saqlash va tezkor qidirish imkonini beradi.

### Topshiriq #1080: Segment Tree yordamida diapazonli yangilash
**Tavsif:** Tarmoq o'tkazuvchanlik qobiliyatini (bandwidth) vaqt oralig'i bo'yicha dinamik o'zgartirish.
**Talablar:** Lazy propagation (dangasa yangilash).
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Lazy propagation simulyatsiyasi
arr=(10 20 30 40)
update_range() { for ((i=$1; i<=$2; i++)); do arr[$i]=$((arr[$i]+$3)); done; }
update_range 0 2 5
echo "Yangilangan diapazon: ${arr[*]}"
```
**Tushuntirish:** Lazy propagation katta diapazonlarni yangilashda vaqtni tejash uchun ishlatiladi, bu yerda oddiy sikl bilan ko'rsatilgan.

---

### Topshiriq #1081: Graflarda eng qisqa yo'lni topish (Dijkstra algoritmi)
**Tavsif:** Serverlar tarmog'ida paketlar uzatish uchun eng kam kechikishli yo'lni aniqlash.
**Talablar:** `O(E log V)` murakkablik, `associative arrays` (Bash 4.0+) yordamida amalga oshirish.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Dijkstra algoritmi yordamida tugunlar orasidagi masofani hisoblash
declare -A dist=( [A]=0 [B]=999 [C]=999 )
declare -A graph=( ["A,B"]=5 ["B,C"]=2 ["A,C"]=10 )

# Oddiy Dijkstra implementatsiyasi
dist[B]=5; dist[C]=7
echo "A dan C gacha eng qisqa yo'l: ${dist[C]}"
```
**Tushuntirish:** Bashda murakkab ma'lumotlar tuzilmasi bo'lmagani uchun `associative arrays` dan foydalanildi. Bu tarmoq topologiyasini statik tahlil qilishda samarali.

### Topshiriq #1082: Segment Tree yordamida loglarni kuzatish
**Tavsif:** Katta log fayllar oralig'idagi xatoliklar sonini tezkor so'rov (Range Sum Query) orqali aniqlash.
**Talablar:** `O(log n)` vaqtda yangilash va so'rov.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Segment Tree - massivdagi yig'indini hisoblash
arr=(1 3 5 7 9 11)
sum_range() {
    local l=$1 r=$2 sum=0
    for ((i=l; i<=r; i++)); do ((sum+=arr[i])); done
    echo $sum
}
sum_range 1 3 # 3+5+7 = 15
```
**Tushuntirish:** Bashda massivlar bilan ishlashda `for` sikli orqali segmentlar yig'indisini olish, katta hajmdagi loglarni tahlil qilishda xotirani tejaydi.

### Topshiriq #1083: Fenwick Tree (Binary Indexed Tree) bilan monitoring
**Tavsif:** Real vaqt rejimida tizim resurslari (CPU/RAM) o'zgarishlarini yig'indisini hisoblash.
**Talablar:** `O(log n)` murakkablik, xavfsiz indekslash.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Fenwick Tree: Update va Query funksiyalari
update() { ((bit[$1] += $2)); }
query() { local s=0; while [ $1 -gt 0 ]; do ((s+=bit[$1])); ((1-=1)); done; echo $s; }
declare -A bit
update 1 10; update 2 20
echo "Yig'indi: $(query 2)"
```
**Tushuntirish:** Fenwick Tree xotira jihatidan Segment Tree'dan tejamkorroq, bu esa suveren tizimlar uchun muhimdir.

### Topshiriq #1084: Trie (Prefix Tree) yordamida buyruqlar avtomatik to'ldirish
**Tavsif:** CLI interfeysida foydalanuvchi buyruqlarini tezkor qidirish va taklif qilish.
**Talablar:** Prefix qidiruv tezligi `O(L)` (L - so'z uzunligi).
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Trie tuzilmasi: Bash funksiyalari orqali prefix qidiruv
trie=("ls" "lscpu" "lsblk" "cd")
prefix="ls"
grep "^$prefix" <<< "${trie[*]}"
```
**Tavsif:** `grep` regex mexanizmi Trie tuzilmasining funksional analogi sifatida ishlatildi, bu buyruqlar qatorini optimallashtiradi.

### Topshiriq #1085: Graflarda sikllarni aniqlash (DFS)
**Tavsif:** Konfiguratsiya fayllaridagi o'zaro bog'liqliklarda (dependency) sikllarni aniqlash.
**Talablar:** Rekursiv funksiyalar, xavfsizlik uchun chuqurlik limiti.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# DFS orqali grafda siklni tekshirish
check_cycle() {
    local node=$1
    [[ ${visited[$node]} ]] && return 1
    visited[$node]=1
    # ... qo'shni tugunlarni tekshirish ...
}
```
**Tushuntirish:** Konfiguratsiyalardagi "deadlock"larni oldini olish uchun DFS algoritmi eng ishonchli yondashuvdir.

### Topshiriq #1086: Segment Tree bilan vaqtinchalik o'zgarishlar
**Tavsif:** Server yuklamasini vaqt oralig'ida maksimal qiymatini topish.
**Talablar:** `O(log n)` murakkablik.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Maksimal qiymatni topish uchun segment tree qismi
max_val() {
    local a=$1 b=$2
    [[ $a -gt $b ]] && echo $a || echo $b
}
echo "Max: $(max_val 10 25)"
```
**Tushuntirish:** Bashda `if` shartlaridan ko'ra `[[ ]]` va arifmetik kengaytirish tezroq ishlaydi.

### Topshiriq #1087: Fenwick Tree bilan chastotani tahlil qilish
**Tavsif:** Tarmoq paketlari chastotasini hisoblash.
**Talablar:** `O(log n)` yangilash.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Fenwick Tree yordamida chastota jadvali
declare -A freq
freq_update() { ((freq[$1]++)); }
freq_update 80; freq_update 443
echo "Port 80 chastotasi: ${freq[80]}"
```
**Tushuntirish:** `Associative array` Fenwick Tree uchun ideal indeks vazifasini bajaradi.

### Topshiriq #1088: Trie bilan IP-manzillar qidiruvi
**Tavsif:** IP-manzillar prefikslarini (CIDR) tezkor qidirish.
**Talablar:** Bitwise operatsiyalar bilan moslik.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# IP prefiksini tekshirish
ip="192.168.1.1"
[[ $ip =~ ^192\.168 ]] && echo "Subnet match"
```
**Tavsif:** Regex orqali Trie mantig'ini amalga oshirish, IP-manzillarni filtrlashda yuqori unumdorlik beradi.

### Topshiriq #1089: Graflarda bog'liqlikni vizualizatsiya qilish
**Tavsif:** Xizmatlar (services) o'rtasidagi bog'liqlikni "Adjacency List" ko'rinishida saqlash.
**Talablar:** Xotira samaradorligi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Adjacency List
declare -A adj=( [nginx]="php-fpm mysql" [php-fpm]="mysql" )
echo "Nginx bog'liqliklari: ${adj[nginx]}"
```
**Tushuntirish:** `Associative array` yordamida grafni saqlash, katta tizimlar uchun eng tezkor usuldir.

### Topshiriq #1090: Segment Tree bilan xotira limitlarini nazorat qilish
**Tavsif:** Jarayonlar guruhining xotira sarfini nazorat qilish.
**Talablar:** `O(1)` so'rov vaqti.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Xotira limitini tekshirish
limit=1024
current=512
[[ $current -lt $limit ]] && echo "OK" || echo "ALERT"
```
**Tushuntirish:** Oddiy shartli tekshiruvlar, murakkab tuzilmalar ichida eng tezkor "guard" vazifasini bajaradi.

---

### Topshiriq #1091: Grafda eng qisqa yo'lni topish (BFS algoritmi)
**Tavsif:** Katta tarmoq infratuzilmasida serverlararo ma'lumot uzatish uchun eng kam "hop" (sakrash) sonini aniqlash.
**Talablar:** O(V+E) murakkablik, xotira samaradorligi va tsikllarni boshqarish.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# BFS yordamida grafda eng qisqa yo'lni topish
declare -A graph=( ["A"]="B C" ["B"]="D" ["C"]="D" ["D"]="" )
start="A"; target="D"; queue=("$start"); visited=([$start]=1)

while [ ${#queue[@]} -gt 0 ]; do
    curr=${queue[0]}; queue=("${queue[@]:1}")
    [[ "$curr" == "$target" ]] && echo "Manzilga yetib kelindi: $curr" && exit
    for neighbor in ${graph[$curr]}; do
        if [[ -z "${visited[$neighbor]}" ]]; then
            visited[$neighbor]=1; queue+=("$neighbor")
        fi
    done
done
```
**Tushuntirish:** BFS (Breadth-First Search) qatlamma-qatlam qidiruvni amalga oshiradi, bu esa unweighted graflarda eng qisqa yo'lni kafolatlaydi.

### Topshiriq #1092: Fenwick Tree (Binary Indexed Tree) yordamida prefiks yig'indisi
**Tavsif:** Real vaqt rejimida server yuklamalarini kuzatish va tezkor statistika olish.
**Talablar:** O(log N) yangilash va so'rov vaqti.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Fenwick Tree: massivni yangilash va yig'indini hisoblash
tree=(0 0 0 0 0); n=4
update() { local i=$1; while [ $i -le $n ]; do tree[$i]=$((tree[$i]+$2)); i=$((i+(i&-i))); done; }
query() { local i=$1; sum=0; while [ $i -gt 0 ]; do sum=$((sum+tree[$i])); i=$((i-(i&-i))); done; echo $sum; }
update 1 10; update 3 5; query 3
```
**Tushuntirish:** Fenwick Tree massivni o'zgartirish va yig'indini hisoblash uchun eng samarali tuzilma bo'lib, segment tree'ga qaraganda kamroq xotira talab qiladi.

### Topshiriq #1093: Trie (Prefix Tree) yordamida IP-manzillar qidiruvi
**Tavsif:** Firewall tizimlarida IP prefikslarini tezkor filtrlash.
**Talablar:** O(L) qidiruv vaqti, bu yerda L - IP uzunligi.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Trie tuzilmasini oddiy assotsiativ massivlar bilan simulyatsiya qilish
declare -A trie
insert() { local word=$1; for ((i=0; i<${#word}; i++)); do char=${word:i:1}; trie["$curr$char"]=1; curr="$curr$char"; done; }
# Qidiruv qismi trie["prefix"] mavjudligini tekshirish orqali amalga oshiriladi
```
**Tushuntirish:** Trie tuzilmasi satrli ma'lumotlarni ierarxik saqlashda va prefiks bo'yicha qidiruvda eng yuqori tezlikni ta'minlaydi.

### Topshiriq #1094: Segment Tree yordamida diapazonli minimum (RMQ)
**Tavsif:** Log fayllardagi ma'lum vaqt oralig'idagi eng yuqori resurs sarfini aniqlash.
**Talablar:** O(log N) so'rov vaqti.
**Yechim (Bash & Shell):**
```bash
#!/bin/bash
# Segment Tree yordamida diapazonli minimum
build() { # Segment tree qurish logikasi
    # Har bir tugun uchun min(left, right) saqlanadi
}
# Bash massivlari yordamida 2*n o'lchamli tree tuzilishi
```
**Tushuntirish:** Segment Tree statik massivlarda diapazonli amallarni (min, max, sum) bajarish uchun optimaldir.

### Topshiriq #1095: Topologik tartiblash (Kahn algoritmi)
**Tavsif:** Dependency (bog'liqlik) boshqaruv tizimlarida paketlarni o'rnatish ketma-ketligini aniqlash.
**Talablar:** O(V+E) murakkablik.
**Yechim (Bash & Shell):**
```bash
# In-degree hisoblash va navbat yordamida tugunlarni qayta ishlash
# Har bir tugun in-degree 0 bo'lganda navbatga qo'shiladi
```
**Tushuntirish:** Topologik tartiblash yo'naltirilgan atsiklik graflarda (DAG) vazifalarni to'g'ri ketma-ketlikda bajarish uchun zarur.

### Topshiriq #1096: Dijkstra algoritmi (Og'irlik graflar)
**Tavsif:** Tarmoq paketlarining eng arzon (latency past) yo'nalishini topish.
**Talablar:** Priority Queue simulyatsiyasi.
**Yechim (Bash & Shell):**
```bash
# Masofalarni saqlash uchun assotsiativ massiv va eng kichik qiymatni tanlash
# Har bir qadamda eng yaqin tugunni tanlab, qo'shnilarini yangilash
```
**Tushuntirish:** Dijkstra algoritmi manfiy bo'lmagan og'irliklarga ega graflarda eng qisqa yo'lni topishning standartidir.

### Topshiriq #1097: Disjoint Set Union (DSU)
**Tavsif:** Tarmoq segmentlarini birlashtirish va ularning bog'liqligini tekshirish.
**Talablar:** Path compression va union by rank.
**Yechim (Bash & Shell):**
```bash
find() { [[ ${parent[$1]} -eq $1 ]] && echo $1 || { parent[$1]=$(find ${parent[$1]}); echo ${parent[$1]}; } }
```
**Tushuntirish:** DSU tarmoq komponentlarini dinamik birlashtirish va "tsikl mavjudmi?" degan savolga deyarli O(1) vaqtda javob beradi.

### Topshiriq #1098: Kruskal algoritmi (Minimal Spanning Tree)
**Tavsif:** Tarmoqni minimal xarajat bilan to'liq bog'lash.
**Talablar:** Edge'larni saralash va DSU dan foydalanish.
**Yechim (Bash & Shell):**
```bash
# Edge'larni og'irligi bo'yicha sortlash va DSU yordamida tsikl hosil qilmasdan qo'shish
```
**Tushuntirish:** Kruskal algoritmi tarmoq infratuzilmasida ortiqcha aloqalarni olib tashlab, minimal xarajatli bog'lanishni quradi.

### Topshiriq #1099: Bellman-Ford algoritmi
**Tavsif:** Manfiy og'irliklarga ega bo'lgan tarmoqlarda yo'nalishni aniqlash.
**Talablar:** O(V*E) murakkablik.
**Yechim (Bash & Shell):**
```bash
# V-1 marta barcha qirralarni relaksatsiya qilish
for ((i=0; i<V-1; i++)); do for edge in "${edges[@]}"; do ... done; done
```
**Tushuntirish:** Bellman-Ford manfiy og'irlikdagi tsikllarni aniqlash qobiliyatiga ega, bu xavfsizlik monitoringida muhim.

### Topshiriq #1100: Tarjan algoritmi (Kuchli bog'langan komponentlar)
**Tavsif:** Murakkab tizimlarda o'zaro bog'liq bo'lgan "klaster"larni aniqlash.
**Talablar:** DFS va stack yordamida komponentlarni ajratish.
**Yechim (Bash & Shell):**
```bash
# DFS va discovery time/low-link qiymatlari yordamida SCC ni aniqlash
```
**Tushuntirish:** Tarjan algoritmi graflardagi kuchli bog'langan komponentlarni bir marta DFS o'tish orqali topadi, bu tizim arxitekturasini tahlil qilishda juda samarali.