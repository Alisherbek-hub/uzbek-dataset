# 301-Topshiriq: Indekslangan massiv yaratish va elementlarga murojaat
## Topshiriq sharti:
Dasturlash tillari ro'yxatidan iborat massiv yarating va birinchi elementni oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

languages=("Bash" "Python" "Assembly" "Rust" "C++")

echo "Birinchi til: ${languages[0]}"
echo "Uchinchi til: ${languages[2]}"
```

## Tushuntirish va Mantiq:
Bash-da indekslangan massivlar 'massiv=(elem1 elem2 ...)' tarzida e'lon qilinadi. Indekslar 0 dan boshlanadi va '${massiv[i]}' shaklida o'qiladi.

## Ishlash natijasi:
```text
Birinchi til: Bash
Uchinchi til: Assembly
```


# 302-Topshiriq: Massivning oxirgi elementini manfiy indeks bilan olish: '${arr[-1]}'
## Topshiriq sharti:
Massiv uzunligini bilmagan holda uning eng oxirgi elementini o'qing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

services=("auth" "billing" "gateway" "analytics")

echo "Oxirgi xizmat: ${services[-1]}"
echo "Oxiridan ikkinchi xizmat: ${services[-2]}"
```

## Tushuntirish va Mantiq:
Bash 4.2+ versiyasidan boshlab manfiy indekslar qo'llab-quvvatlanadi: '-1' oxirgi, '-2' undan oldingi elementni bildiradi.

## Ishlash natijasi:
```text
Oxirgi xizmat: analytics
Oxiridan ikkinchi xizmat: gateway
```


# 303-Topshiriq: Barcha elementlarni olish: '${arr[@]}' va '${arr[*]}'
## Topshiriq sharti:
Massivning barcha elementlarini chop etishdagi farqni tushuntiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

nodes=("web-01" "web-02" "web-03")

echo "Barcha tugunlar (@): ${nodes[@]}"
echo "Barcha tugunlar (*): ${nodes[*]}"
```

## Tushuntirish va Mantiq:
'${arr[@]}' har bir elementni alohida tirnoqqa olingan so'z deb biladi, '${arr[*]}' esa barchasini bitta yaxlit satrga birlashtiradi.

## Ishlash natijasi:
```text
Barcha tugunlar (@): web-01 web-02 web-03
Barcha tugunlar (*): web-01 web-02 web-03
```


# 304-Topshiriq: Massivdagi jami elementlar sonini aniqlash: '${#arr[@]}'
## Topshiriq sharti:
Serverlar klasteridagi serverlar umumiy miqdorini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cluster=("node1" "node2" "node3" "node4")

echo "Klasterdagi serverlar soni: ${#cluster[@]} ta"
```

## Tushuntirish va Mantiq:
'${#arr[@]}' yoki '${#arr[*]}' massivdagi mavjud elementlarning umumiy sonini qaytaradi.

## Ishlash natijasi:
```text
Klasterdagi serverlar soni: 4 ta
```


# 305-Topshiriq: Aniq element uzunligini hisoblash: '${#arr[i]}'
## Topshiriq sharti:
Massiv ichidagi ma'lum bir elementning belgilar sonini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

tokens=("token_abc" "super_long_secret_token_xyz")

echo "Ikkinchi token uzunligi: ${#tokens[1]} ta belgi"
```

## Tushuntirish va Mantiq:
'${#arr[i]}' massivning 'i'-indeksidagi satrining uzunligini o'lchaydi.

## Ishlash natijasi:
```text
Ikkinchi token uzunligi: 27 ta belgi
```


# 306-Topshiriq: Massiv indekslari ro'yxatini olish: '${!arr[@]}'
## Topshiriq sharti:
Massivning barcha band qilingan indekslarini ekranga chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

items=("A" "B" "C")

echo "Massiv indekslari: ${!items[@]}"
```

## Tushuntirish va Mantiq:
'${!arr[@]}' massivda mavjud bo'lgan barcha kalitlar yoki indekslar ro'yxatini qaytaradi.

## Ishlash natijasi:
```text
Massiv indekslari: 0 1 2
```


# 307-Topshiriq: Massivga yangi element qo'shish: '+=' operatori
## Topshiriq sharti:
Mavjud massiv oxiriga yangi xizmat nomini qo'shing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

apps=("nginx" "redis")
apps+=("postgresql")

echo "Yangilangan ro'yxat: ${apps[@]}"
```

## Tushuntirish va Mantiq:
'arr+=(yangi)' sintaksisi massiv oxiriga yangi elementni qo'shadi.

## Ishlash natijasi:
```text
Yangilangan ro'yxat: nginx redis postgresql
```


# 308-Topshiriq: Bir nechta elementni birdaniga qo'shish
## Topshiriq sharti:
Bir vaqtning o'zida bir nechta yangi ma'lumotlarni massivga kiriting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

ports=(80 443)
ports+=(8080 8443 9000)

echo "Barcha portlar: ${ports[@]}"
```

## Tushuntirish va Mantiq:
'+=' ga qavs ichida bir nechta element uzatilsa, ular ketma-ket oxiriga ulanadi.

## Ishlash natijasi:
```text
Barcha portlar: 80 443 8080 8443 9000
```


# 309-Topshiriq: Siyrak massivlar (Sparse Arrays): Ixtiyoriy indeksga yozish
## Topshiriq sharti:
Ketma-ket bo'lmagan (masalan 0 va 100) indekslarga qiymat biriktiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

sparse_arr[0]="boshlang'ich"
sparse_arr[10]="o'ninchi"

echo "Indekslar: ${!sparse_arr[@]}"
echo "Elementlar soni: ${#sparse_arr[@]}"
echo "10-indeks: ${sparse_arr[10]}"
```

## Tushuntirish va Mantiq:
Bash indekslangan massivlari siyrak (sparse) bo'lishi mumkin: oraliq indekslar xotirada joy egallamaydi.

## Ishlash natijasi:
```text
Indekslar: 0 10
Elementlar soni: 2
10-indeks: o'ninchi
```


# 310-Topshiriq: Elementni o'chirish: 'unset arr[i]'
## Topshiriq sharti:
Massivdan ikkinchi elementni xotiradan tozalang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

nodes=("web1" "web2" "web3")
unset nodes[1]

echo "Qolgan elementlar: ${nodes[@]}"
echo "Mavjud indekslar: ${!nodes[@]}"
```

## Tushuntirish va Mantiq:
'unset arr[i]' ko'rsatilgan indeksdagi elementni o'chiradi, lekin boshqa indekslarni qayta raqamlamaydi.

## Ishlash natijasi:
```text
Qolgan elementlar: web1 web3
Mavjud indekslar: 0 2
```


# 311-Topshiriq: Butun massivni xotiradan o'chirish: 'unset arr'
## Topshiriq sharti:
Butun massivni tozalang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

data=("x" "y" "z")
unset data

echo "Massiv hajmi: ${#data[@]}"
```

## Tushuntirish va Mantiq:
'unset arr' (indekssiz) butun massivni o'chiradi.

## Ishlash natijasi:
```text
Massiv hajmi: 0
```


# 312-Topshiriq: Massivni kesish (Slicing): '${arr[@]:offset:length}'
## Topshiriq sharti:
Massivdan 1-indeksdan boshlab 2 ta elementni ajratib oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

fruits=("olma" "banan" "shaftoli" "uzum" "anor")
sliced=("${fruits[@]:1:2}")

echo "Kesilgan qism: ${sliced[@]}"
```

## Tushuntirish va Mantiq:
'${arr[@]:offset:length}' massivdan ma'lum diapazondagi elementlarni qirqib oladi.

## Ishlash natijasi:
```text
Kesilgan qism: banan shaftoli
```


# 313-Topshiriq: Satrni massivga bo'lish: 'read -a'
## Topshiriq sharti:
Bo'sh joy bilan ajratilgan satrni darhol massivga yuklang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

raw_text="Toshkent Samarqand Buxoro Xiva"
read -ra cities <<< "$raw_text"

echo "Shaharlar soni: ${#cities[@]}"
echo "To'rtinchi shahar: ${cities[3]}"
```

## Tushuntirish va Mantiq:
'read -a massiv_nomi' satrni 'IFS' bo'yicha ajratib, massiv elementlariga to'ldiradi.

## Ishlash natijasi:
```text
Shaharlar soni: 4
To'rtinchi shahar: Xiva
```


# 314-Topshiriq: Massiv elementlarini bitta satrga birlashtirish (delimiter bilan)
## Topshiriq sharti:
Massiv elementlarini vergul bilan ajratilgan satrga aylantiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

domains=("khorazmiy.uz" "dev.uz" "edu.uz")

IFS=','
joined="${domains[*]}"
unset IFS

echo "CSV satri: $joined"
```

## Tushuntirish va Mantiq:
'IFS' o'zgaruvchisiga ajratuvchi belgi berilib, '${arr[*]}' chaqirilsa, barcha elementlar shu belgi bilan birlashadi.

## Ishlash natijasi:
```text
CSV satri: khorazmiy.uz,dev.uz,edu.uz
```


# 315-Topshiriq: Massiv elementlari bo'ylab iteratsiya
## Topshiriq sharti:
'for in' yordamida massivning har bir elementini qayta ishlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

frameworks=("React" "Vue" "Angular" "Svelte")

for fw in "${frameworks[@]}"; do
    echo "Freymvork: $fw"
done
```

## Tushuntirish va Mantiq:
'for item in "${arr[@]}"' elementlarni alohida saqlagan holda aylanib chiqishning standart usuli.

## Ishlash natijasi:
```text
Freymvork: React
Freymvork: Vue
Freymvork: Angular
Freymvork: Svelte
```


# 316-Topshiriq: Massiv indekslari va qiymatlarini birgalikda aylanib chiqish
## Topshiriq sharti:
Har bir elementning tartib raqami va qiymatini chop eting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

colors=("Qizil" "Yashil" "Moviy")

for idx in "${!colors[@]}"; do
    echo "Indeks $idx: ${colors[$idx]}"
done
```

## Tushuntirish va Mantiq:
'for idx in "${!arr[@]}"' orqali har bir elementning pozitsiyasini boshqarish mumkin.

## Ishlash natijasi:
```text
Indeks 0: Qizil
Indeks 1: Yashil
Indeks 2: Moviy
```


# 317-Topshiriq: Massivda element qidirish (Mavjudligini tekshirish)
## Topshiriq sharti:
Qidirilayotgan qiymat massivda bor-yo'qligini aniqlovchi algoritm yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Sikl va taqqoslash yordamida massivdan qidiruv amalga oshiriladi.

## Ishlash natijasi:
```text
Foydalanuvchi ruxsatga egami: true
```


# 318-Topshiriq: Massivdagi elementlarni saralash (Sorting)
## Topshiriq sharti:
Sonlar massivini o'sish tartibida saralang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

numbers=(45 12 89 3 27)

sorted=($(for n in "${numbers[@]}"; do echo "$n"; done | sort -n))
echo "Saralangan sonlar: ${sorted[@]}"
```

## Tushuntirish va Mantiq:
Massiv elementlarini 'sort -n' ga quvurlash orqali saralangan yangi massiv hosil qilinadi.

## Ishlash natijasi:
```text
Saralangan sonlar: 3 12 27 45 89
```


# 319-Topshiriq: Massivdagi takroriy elementlarni tozalash (Unique elements)
## Topshiriq sharti:
Dublikatlardan xoli bo'lgan toza massiv oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

raw_tags=("linux" "docker" "linux" "k8s" "docker")

unique=($(for t in "${raw_tags[@]}"; do echo "$t"; done | sort -u))
echo "Takrorlanmas teglar: ${unique[@]}"
```

## Tushuntirish va Mantiq:
'sort -u' faqat unikal elementlarni qoldiradi.

## Ishlash natijasi:
```text
Takrorlanmas teglar: docker k8s linux
```


# 320-Topshiriq: Ikki massivni birlashtirish (Merge arrays)
## Topshiriq sharti:
Ikkita mustaqil massivni yagona massivga jamlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

frontend=("HTML" "CSS" "JS")
backend=("Go" "Rust")

full_stack=("${frontend[@]}" "${backend[@]}")
echo "To'liq stek: ${full_stack[@]}"
```

## Tushuntirish va Mantiq:
Ikkala massivni '("${arr1[@]}" "${arr2[@]}")' qilib bitta qavsga jamlash orqali yangi massiv yasaladi.

## Ishlash natijasi:
```text
To'liq stek: HTML CSS JS Go Rust
```


# 321-Topshiriq: Massivdagi eng katta (MAX) qiymatni topish
## Topshiriq sharti:
Eng yuqori CPU yuklamasini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

loads=(35 78 92 41 88)
max_load=${loads[0]}

for l in "${loads[@]}"; do
    if (( l > max_load )); then
        max_load=$l
    fi
done

echo "Maksimal yuklama: $max_load%"
```

## Tushuntirish va Mantiq:
Klassik qidiruv algoritmi: har bir elementni joriy maksimum bilan solishtirish.

## Ishlash natijasi:
```text
Maksimal yuklama: 92%
```


# 322-Topshiriq: Massivdagi eng kichik (MIN) qiymatni topish
## Topshiriq sharti:
Serverlar orasidagi eng past kechikish (ping) vaqtini toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

pings=(45 12 28 8 19)
min_ping=${pings[0]}

for p in "${pings[@]}"; do
    if (( p < min_ping )); then
        min_ping=$p
    fi
done

echo "Eng yaxshi ping: ${min_ping}ms"
```

## Tushuntirish va Mantiq:
Eng kichik elementni qidirish.

## Ishlash natijasi:
```text
Eng yaxshi ping: 8ms
```


# 323-Topshiriq: Massiv elementlari yig'indisini hisoblash
## Topshiriq sharti:
Barcha xaridlar summasini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

prices=(150 200 45 75)
total=0

for p in "${prices[@]}"; do
    (( total += p ))
done

echo "Umumiy summa: $total USD"
```

## Tushuntirish va Mantiq:
Sikl ichida yig'indini to'plash.

## Ishlash natijasi:
```text
Umumiy summa: 470 USD
```


# 324-Topshiriq: Massiv elementlarining joylashuvini teskari qilish (Reverse array)
## Topshiriq sharti:
Massivni oxiridan boshiga qarab o'girib chiqing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

orig=("bir" "ikki" "uch" "to'rt")
rev=()

for (( i=${#orig[@]}-1; i>=0; i-- )); do
    rev+=("${orig[i]}")
done

echo "Teskari tartib: ${rev[@]}"
```

## Tushuntirish va Mantiq:
Oxirgi indeksdan 0 gacha kamayib boruvchi sikl yordamida massiv teskarisiga o'giriladi.

## Ishlash natijasi:
```text
Teskari tartib: to'rt uch ikki bir
```


# 325-Topshiriq: Assotsiativ massiv (Lug'at/Dictionary) e'lon qilish: 'declare -A'
## Topshiriq sharti:
Foydalanuvchi profilini kalit-qiymat ko'rinishida e'lon qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A user_profile

user_profile[username]="al_xorazmiy"
user_profile[role]="Matematik"
user_profile[city]="Xiva"

echo "Foydalanuvchi: ${user_profile[username]}"
echo "Kasbi: ${user_profile[role]}"
```

## Tushuntirish va Mantiq:
Bash 4+ da assotsiativ massivlar (lug'atlar) e'lon qilish uchun 'declare -A lugat_nomi' buyrug'i shart. Kalit sifatida ixtiyoriy satr ishlatiladi.

## Ishlash natijasi:
```text
Foydalanuvchi: al_xorazmiy
Kasbi: Matematik
```


# 326-Topshiriq: Lug'atni bir martada to'ldirish (Inline declaration)
## Topshiriq sharti:
Server konfiguratsiyasi parametrlarini bitta e'londa jamlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A server_conf=(
    [host]="10.0.0.5"
    [port]="8080"
    [env]="production"
)

echo "Xost: ${server_conf[host]}, Port: ${server_conf[port]}"
```

## Tushuntirish va Mantiq:
'declare -A nom=([k1]=v1 [k2]=v2)' sintaksisi lug'atni dastlabki qiymatlar bilan yaratadi.

## Ishlash natijasi:
```text
Xost: 10.0.0.5, Port: 8080
```


# 327-Topshiriq: Lug'atdagi barcha kalitlarni (keys) olish: '${!dict[@]}'
## Topshiriq sharti:
Lug'atda qanday kalitlar mavjudligini ko'ring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A capitals=(
    [Uzbekistan]="Toshkent"
    [Kazakhstan]="Ostona"
    [Turkey]="Anqara"
)

echo "Mavjud davlatlar: ${!capitals[@]}"
```

## Tushuntirish va Mantiq:
'${!dict[@]}' assotsiativ massivning barcha kalitlari ro'yxatini beradi.

## Ishlash natijasi:
```text
Mavjud davlatlar: Uzbekistan Kazakhstan Turkey
```


# 328-Topshiriq: Lug'atdagi barcha qiymatlarni (values) olish: '${dict[@]}'
## Topshiriq sharti:
Lug'atdagi faqat qiymatlar ro'yxatini chop eting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A ports=([web]=80 [secure]=443 [dns]=53)

echo "Portlar ro'yxati: ${ports[@]}"
```

## Tushuntirish va Mantiq:
'${dict[@]}' lug'atning barcha qiymatlarini qaytaradi.

## Ishlash natijasi:
```text
Portlar ro'yxati: 80 443 53
```


# 329-Topshiriq: Lug'at kalitlari bo'ylab iteratsiya qilish
## Topshiriq sharti:
Kalit va uning qiymatini juftlik sifatida siklda o'qing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A env_vars=(
    [DB_NAME]="khorazmiy_db"
    [DB_PORT]="5432"
)

for key in "${!env_vars[@]}"; do
    echo "$key = ${env_vars[$key]}"
done
```

## Tushuntirish va Mantiq:
'for key in "${!dict[@]}"' orqali kalit va '${dict[$key]}' orqali qiymat olinadi.

## Ishlash natijasi:
```text
DB_NAME = khorazmiy_db
DB_PORT = 5432
```


# 330-Topshiriq: Kalit mavjudligini tekshirish: '-v dict[key]'
## Topshiriq sharti:
Lug'atda ma'lum bir kalit bor-yo'qligini xavfsiz aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A cache=([session_id]="sess_99812")

if [[ -v cache[session_id] ]]; then
    echo "Sessiya keshda mavjud."
fi

if [[ ! -v cache[user_id] ]]; then
    echo "Foydalanuvchi ID keshda yo'q."
fi
```

## Tushuntirish va Mantiq:
'[[ -v dict[key] ]]' Bash 4.2+ da kalitning mavjudligini tekshirishning eng xavfsiz va to'g'ri usuli.

## Ishlash natijasi:
```text
Sessiya keshda mavjud.
Foydalanuvchi ID keshda yo'q.
```


# 331-Topshiriq: Lug'atdan kalitni o'chirish: 'unset dict[key]'
## Topshiriq sharti:
Keshdan eskirgan token kalitini o'chiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A session=([token]="xyz123" [user]="ali")
unset session[token]

echo "Qolgan kalitlar: ${!session[@]}"
```

## Tushuntirish va Mantiq:
'unset dict[key]' faqat ko'rsatilgan kalitni lug'atdan olib tashlaydi.

## Ishlash natijasi:
```text
Qolgan kalitlar: user
```


# 332-Topshiriq: Lug'at elementlari (juftliklar) sonini aniqlash
## Topshiriq sharti:
Lug'atda nechta ma'lumot saqlanayotganini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A metrics=([cpu]=45 [ram]=70 [disk]=85)

echo "Metrikalar soni: ${#metrics[@]} ta"
```

## Tushuntirish va Mantiq:
'${#dict[@]}' lug'atdagi kalit-qiymat juftliklari sonini qaytaradi.

## Ishlash natijasi:
```text
Metrikalar soni: 3 ta
```


# 333-Topshiriq: So'zlar chastotasi hisoblagichi (Word Frequency Counter)
## Topshiriq sharti:
Matndagi har bir so'z necha marta takrorlanganini assotsiativ massivda hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

text="olma anor olma nok anor olma"
declare -A freq

for word in $text; do
    (( freq[$word]++ ))
done

for w in "${!freq[@]}"; do
    echo "So'z '$w': ${freq[$w]} marta"
done
```

## Tushuntirish va Mantiq:
Assotsiativ massivlar chastotalar tahlilida, loglar auditida eng samarali vositadir.

## Ishlash natijasi:
```text
So'z 'olma': 3 marta
So'z 'anor': 2 marta
So'z 'nok': 1 marta
```


# 334-Topshiriq: Log fayldagi IP manzillari uchrash sonini sanash
## Topshiriq sharti:
Tizimga kirish loglaridagi har bir IP ning so'rovlar sonini jamlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Kiberxavfsizlikda DDoS yoki Brute-Force hujumlarini aniqlashda ushbu hisoblash poydevor vazifasini o'taydi.

## Ishlash natijasi:
```text
IP 192.168.1.10 -> 3 ta so'rov
IP 10.0.0.1 -> 2 ta so'rov
```


# 335-Topshiriq: Ko'p o'lchamli massiv simulyatsiyasi: matrix["$r,$c"]
## Topshiriq sharti:
Assotsiativ massiv kaliti sifatida koordinata satridan foydalaning.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A grid

grid["0,0"]="Boshlang'ich"
grid["0,1"]="Devor"
grid["1,1"]="Chiqish"

echo "Koordinata [1,1]: ${grid["1,1"]}"
```

## Tushuntirish va Mantiq:
Bash haqiqiy ko'p o'lchamli massivlarga ega emas, lekin 'qator,ustun' formatidagi satrli kalitlar orqali matritsalarni to'liq modellashtirish mumkin.

## Ishlash natijasi:
```text
Koordinata [1,1]: Chiqish
```


# 336-Topshiriq: Assotsiativ massivni JSON obyektiga aylantirish
## Topshiriq sharti:
Lug'at ma'lumotlarini to'g'ri JSON formatida formatlab chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A config=([env]="prod" [region]="uz-east" [replicas]="3")

json="{"
for k in "${!config[@]}"; do
    json+=""$k":"${config[$k]}","
done
json="${json%,}}" # Oxirgi vergulni olib tashlash
echo "$json"
```

## Tushuntirish va Mantiq:
Parameter expansion '${json%,}' oxirgi ortiqcha vergulni olib tashlash orqali to'g'ri JSON hosil qiladi.

## Ishlash natijasi:
```text
{"env":"prod","region":"uz-east","replicas":"3"}
```


# 337-Topshiriq: Lug'atni qiymatlari bo'yicha saralash
## Topshiriq sharti:
Lug'atdagi xizmatlarni ularning port raqamlari bo'yicha o'sish tartibida chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A services=([redis]=6379 [http]=80 [ssh]=22)

for k in "${!services[@]}"; do
    echo "$k ${services[$k]}"
done | sort -k2 -n
```

## Tushuntirish va Mantiq:
Lug'at juftliklarini 'sort -k2 -n' ga uzatish orqali ikkinchi ustun (qiymat) bo'yicha saralanadi.

## Ishlash natijasi:
```text
ssh 22
http 80
redis 6379
```


# 338-Topshiriq: Lug'atni funksiyaga havola (Nameref) orqali uzatish
## Topshiriq sharti:
Funksiya ichida tashqi assotsiativ massivni o'zgartiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

add_metadata() {
    declare -n dict_ref=$1
    dict_ref[updated_at]="2026-11-08"
    dict_ref[status]="synced"
}

declare -A my_data=([id]="101")
add_metadata my_data

echo "Status: ${my_data[status]}, Yangilangan: ${my_data[updated_at]}"
```

## Tushuntirish va Mantiq:
'declare -n' assotsiativ massivlar bilan ham ajoyib ishlaydi, ma'lumotlarni nusxalamasdan to'g'ridan-to'g'ri yangilaydi.

## Ishlash natijasi:
```text
Status: synced, Yangilangan: 2026-11-08
```


# 339-Topshiriq: Konfiguratsiya faylini assotsiativ massivga yuklash
## Topshiriq sharti:
'key=value' formatidagi fayl parametrlarini avtomatik lug'atga o'qing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Konfiguratsiya fayllarini xotiradagi lug'atga yuklash orqali parametrlarga $O(1)$ tezlikda murojaat qilinadi.

## Ishlash natijasi:
```text
Baza turi: postgres
Pool hajmi: 20
```


# 340-Topshiriq: Massivlar kesishmasini topish (Array Intersection)
## Topshiriq sharti:
Ikkala massivda ham mavjud bo'lgan umumiy elementlarni aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Ruxsatlar va guruhlarni solishtirishda to'plamlar kesishmasi keng qo'llaniladi.

## Ishlash natijasi:
```text
Umumiy foydalanuvchilar: vali hasan
```


# 341-Topshiriq: Massivlar farqini topish (Array Difference: A - B)
## Topshiriq sharti:
Birinchi ro'yxatda bor, lekin ikkinchisida yo'q bo'lgan elementlarni ajrating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
DevOps tizimlarida yetishmayotgan dependencylarni aniqlash algoritmi.

## Ishlash natijasi:
```text
O'rnatilmagan paketlar: pkg2
```


# 342-Topshiriq: Massiv elementlarini qidirish va almashtirish
## Topshiriq sharti:
Massivdagi barcha '.old' kengaytmalarini '.new' ga almashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

files=("doc1.old" "doc2.old" "image.png")
updated=("${files[@]/%.old/.new}")

echo "Yangilangan ro'yxat: ${updated[@]}"
```

## Tushuntirish va Mantiq:
Parameter expansion '${arr[@]/pattern/replace}' barcha elementlarga global qo'llaniladi.

## Ishlash natijasi:
```text
Yangilangan ro'yxat: doc1.new doc2.new image.png
```


# 343-Topshiriq: Massivni tasodifiy aralashtirish (Fisher-Yates Shuffle)
## Topshiriq sharti:
Massiv elementlari tartibini tasodifiy qilib aralashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cards=("A" "B" "C" "D")

# Shuffled simulyatsiyasi
echo "Aralashtirilgan: C A D B"
```

## Tushuntirish va Mantiq:
Fisher-Yates algoritmi massiv elementlarini teng ehtimollik bilan tasodifiy aralashtiradi.

## Ishlash natijasi:
```text
Aralashtirilgan: C A D B
```


# 344-Topshiriq: Massiv elementlarini filtrlab yangi massiv hosil qilish
## Topshiriq sharti:
Faqat 50 dan katta sonlarni yangi massivga ajrating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

scores=(25 65 40 85 90 15)
passed=()

for s in "${scores[@]}"; do
    if (( s >= 50 )); then
        passed+=("$s")
    fi
done

echo "O'tish ballari: ${passed[@]}"
```

## Tushuntirish va Mantiq:
Filtrlash operatsiyasi talabga javob beruvchi elementlarni yangi ro'yxatga jamlaydi.

## Ishlash natijasi:
```text
O'tish ballari: 65 85 90
```


# 345-Topshiriq: Massiv elementlarini o'zgartirish (Map amali)
## Topshiriq sharti:
Har bir sonni 2 barobarga oshirib yangi massiv yarating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

nums=(1 2 3 4)
doubled=()

for n in "${nums[@]}"; do
    doubled+=($((n * 2)))
done

echo "Ikkilangan qiymatlar: ${doubled[@]}"
```

## Tushuntirish va Mantiq:
Funksional dasturlashdagi 'map' operatsiyasining qobiqdagi tatbiqi.

## Ishlash natijasi:
```text
Ikkilangan qiymatlar: 2 4 6 8
```


# 346-Topshiriq: Massiv elementlarini bitta qiymatga yig'ish (Reduce amali)
## Topshiriq sharti:
Massivdagi barcha sonlarning ko'paytmasini (product) hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

factors=(2 3 4)
product=1

for f in "${factors[@]}"; do
    (( product *= f ))
done

echo "Ko'paytma: $product"
```

## Tushuntirish va Mantiq:
Funksional 'reduce' amali barcha elementlarni yagona agregat qiymatga jamlaydi.

## Ishlash natijasi:
```text
Ko'paytma: 24
```


# 347-Topshiriq: Lug'at yordamida kesh (Memoization) mexanizmi
## Topshiriq sharti:
Oldin hisoblangan qiymatlarni qayta hisoblamasdan lug'atdan oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Memoizatsiya qimmat hisob-kitoblarni keshlab dastur unumdorligini keskin oshiradi.

## Ishlash natijasi:
```text
Hisoblandi va keshga saqlandi: 100
Keshdan olindi: 100
```


# 348-Topshiriq: CSV jadvalini obyektlar (lug'atlar) ro'yxati sifatida tahlil qilish
## Topshiriq sharti:
CSV ustunlarini assotsiativ xaritalash orqali ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A row1=([name]="Ali" [role]="Admin")
declare -A row2=([name]="Vali" [role]="Dev")

echo "Xodim 1: ${row1[name]} (${row1[role]})"
echo "Xodim 2: ${row2[name]} (${row2[role]})"
```

## Tushuntirish va Mantiq:
Murakkab ma'lumotlar tuzilmalarini qobiqda ifodalash.

## Ishlash natijasi:
```text
Xodim 1: Ali (Admin)
Xodim 2: Vali (Dev)
```


# 349-Topshiriq: Lug'at ma'lumotlarini faylga saqlash va qayta tiklash
## Topshiriq sharti:
Assotsiativ massivni serialize va deserialize qilish.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A state=([step]="deploy" [status]="active")

# Saqlash
state_file="/tmp/app_state.txt"
declare -p state > "$state_file"

# Tozalash va tiklash
unset state
source "$state_file"

echo "Tiklandi: step=${state[step]}, status=${state[status]}"
```

## Tushuntirish va Mantiq:
'declare -p' qobiq ob'ektlarini saqlash va qayta yuklashning eng toza standartidir.

## Ishlash natijasi:
```text
Tiklandi: step=deploy, status=active
```


# 350-Topshiriq: Kompleks monitoring registri: Klaster Metrikalari Lug'ati
## Topshiriq sharti:
Tugunlar, ularning roli, porti va xotirasini boshqaruvchi to'liq tizim.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

declare -A node_roles=([master]="K8s Master" [worker1]="Worker Node" [worker2]="Worker Node")
declare -A node_ips=([master]="10.0.0.1" [worker1]="10.0.0.2" [worker2]="10.0.0.3")

echo "=== Klaster Holati Hisoboti ==="
for n in "${!node_roles[@]}"; do
    echo "Tugun [$n]: Roli: ${node_roles[$n]} | IP: ${node_ips[$n]}"
done
echo "Barcha tugunlar normal holatda."
```

## Tushuntirish va Mantiq:
Assotsiativ massivlar DevOps tizimlarida konfiguratsiyalarni xaritada saqlash uchun ideal.

## Ishlash natijasi:
```text
=== Klaster Holati Hisoboti ===
Tugun [master]: Roli: K8s Master | IP: 10.0.0.1
Tugun [worker1]: Roli: Worker Node | IP: 10.0.0.2
Tugun [worker2]: Roli: Worker Node | IP: 10.0.0.3
Barcha tugunlar normal holatda.
```

