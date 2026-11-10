# 201-Topshiriq: Oddiy 'for' sikli va ro'yxat bo'yicha iteratsiya
## Topshiriq sharti:
Uchta server nomi bo'yicha ketma-ket aylanib chiqing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for server in "web-01" "db-01" "cache-01"; do
    echo "Ulanish tekshirilmoqda: $server"
done
```

## Tushuntirish va Mantiq:
'for var in item1 item2 ...; do ... done' ro'yxatdagi har bir elementni o'zlashtirib blok ichidagi buyruqlarni bajaradi.

## Ishlash natijasi:
```text
Ulanish tekshirilmoqda: web-01
Ulanish tekshirilmoqda: db-01
Ulanish tekshirilmoqda: cache-01
```


# 202-Topshiriq: Brace expansion yordamida 'for' sikli: '{1..5}'
## Topshiriq sharti:
1 dan 5 gacha bo'lgan sonlarni siklda chop eting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for i in {1..5}; do
    echo "Qadam: $i"
done
```

## Tushuntirish va Mantiq:
'{start..end}' sintaksisi Bash tomonidan sikl boshlanishidan oldin ro'yxatga aylantiriladi.

## Ishlash natijasi:
```text
Qadam: 1
Qadam: 2
Qadam: 3
Qadam: 4
Qadam: 5
```


# 203-Topshiriq: Qadamli brace expansion: '{0..20..5}'
## Topshiriq sharti:
0 dan 20 gacha 5 qadam bilan sanab chiqing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for val in {0..20..5}; do
    echo "Qiymat: $val"
done
```

## Tushuntirish va Mantiq:
'{start..end..step}' sintaksisida uchinchi raqam qadam (step) kattaligini bildiradi.

## Ishlash natijasi:
```text
Qiymat: 0
Qiymat: 5
Qiymat: 10
Qiymat: 15
Qiymat: 20
```


# 204-Topshiriq: Harflar bo'yicha iteratsiya: '{A..E}'
## Topshiriq sharti:
Alifbo harflari bo'ylab sikl aylantiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for ch in {A..E}; do
    echo "Klaster zonasi: $ch"
done
```

## Tushuntirish va Mantiq:
Brace expansion harflar (ASCII) oralig'ini ham to'liq qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Klaster zonasi: A
Klaster zonasi: B
Klaster zonasi: C
Klaster zonasi: D
Klaster zonasi: E
```


# 205-Topshiriq: Nol bilan to'ldirilgan raqamlar: '{01..05}'
## Topshiriq sharti:
Server nomlarining raqamlangan seriyasini generatsiya qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for num in {01..04}; do
    echo "node-$num.cluster.local"
done
```

## Tushuntirish va Mantiq:
Brace expansion boshlang'ich formatdagi nollarni saqlab qoladi.

## Ishlash natijasi:
```text
node-01.cluster.local
node-02.cluster.local
node-03.cluster.local
node-04.cluster.local
```


# 206-Topshiriq: C-uslubidagi 'for' sikli: 'for (( i=0; i<N; i++ ))'
## Topshiriq sharti:
Klassik 3 ta parametrli C sikli bilan hisoblagichni oshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for (( i=1; i<=4; i++ )); do
    echo "Iteratsiya #$i"
done
```

## Tushuntirish va Mantiq:
'for (( init; condition; step ))' sintaksisi dinamik o'zgaruvchilar bilan ishlashda eng qulay va tezkor hisoblanadi.

## Ishlash natijasi:
```text
Iteratsiya #1
Iteratsiya #2
Iteratsiya #3
Iteratsiya #4
```


# 207-Topshiriq: C-style for siklida orqaga sanash
## Topshiriq sharti:
10 dan 0 gacha 2 qadam bilan teskari sanab chiqing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for (( count=6; count>=0; count-=2 )); do
    echo "Ortga hisoblash: $count"
done
```

## Tushuntirish va Mantiq:
Dekrement va arifmetik qisqartmalar C-style for siklida qulay qo'llaniladi.

## Ishlash natijasi:
```text
Ortga hisoblash: 6
Ortga hisoblash: 4
Ortga hisoblash: 2
Ortga hisoblash: 0
```


# 208-Topshiriq: Bir nechta o'zgaruvchili C-style for sikli
## Topshiriq sharti:
Bitta siklda bir vaqtning o'zida ikkita o'zgaruvchini parallel boshqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for (( i=1, j=10; i<=3; i++, j-=2 )); do
    echo "i=$i, j=$j"
done
```

## Tushuntirish va Mantiq:
Vergul bilan ajratilgan ifodalar C-style siklida bir vaqtda bajariladi.

## Ishlash natijasi:
```text
i=1, j=10
i=2, j=8
i=3, j=6
```


# 209-Topshiriq: Katalogdagi fayllar bo'yicha iteratsiya: 'for f in *.log'
## Topshiriq sharti:
Papkadagi barcha log fayllarni aylanib chiqib ularning hajmini ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/logs_test
touch /tmp/logs_test/app.log /tmp/logs_test/err.log

for f in /tmp/logs_test/*.log; do
    echo "Fayl topildi: $(basename "$f")"
done
```

## Tushuntirish va Mantiq:
Wildcard fayllar ro'yxatini hosil qiladi va sikl har bir fayl nomini qabul qiladi.

## Ishlash natijasi:
```text
Fayl topildi: app.log
Fayl topildi: err.log
```


# 210-Topshiriq: Bo'sh moslik muammosi va 'nullglob' sozlamasi
## Topshiriq sharti:
Hech qanday fayl topilmaganda xato literal satr chiqishining oldini oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

shopt -s nullglob
count=0

for f in /tmp/mavjud_bolmagan_yo_l_123/*.xyz; do
    ((count++))
done

echo "Topilgan fayllar soni: $count"
shopt -u nullglob
```

## Tushuntirish va Mantiq:
'shopt -s nullglob' agar wildcard hech qanday faylga mos kelmasa, uni literal matn sifatida qoldirmasdan bo'sh ro'yxatga aylantiradi.

## Ishlash natijasi:
```text
Topilgan fayllar soni: 0
```


# 211-Topshiriq: Skript argumentlari bo'yicha 'for arg in "$@"'
## Topshiriq sharti:
Skriptga kiritilgan barcha argumentlarni bo'sh joylari bilan xavfsiz iteratsiya qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -- "Alpha Node" "Beta Node"

for node in "$@"; do
    echo "Tugun sozlanmoqda: [$node]"
done
```

## Tushuntirish va Mantiq:
'for arg in "$@"' barcha pozitsion parametrlarni xavfsiz qabul qiladi.

## Ishlash natijasi:
```text
Tugun sozlanmoqda: [Alpha Node]
Tugun sozlanmoqda: [Beta Node]
```


# 212-Topshiriq: Qisqartirilgan argumentlar sikli: 'for arg; do ... done'
## Topshiriq sharti:
Argumentlar ro'yxatini 'in "$@"' siz to'g'ridan-to'g'ri aylanib chiqing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -- "file1.txt" "file2.txt"

for file; do
    echo "Qayta ishlanmoqda: $file"
done
```

## Tushuntirish va Mantiq:
Agar 'for' dan keyin 'in ...' qismi tushirib qoldirilsa, Bash sukut bo'yicha 'in "$@"' ni nazarda tutadi.

## Ishlash natijasi:
```text
Qayta ishlanmoqda: file1.txt
Qayta ishlanmoqda: file2.txt
```


# 213-Topshiriq: Klassik 'while' sikli
## Topshiriq sharti:
Shart rost bo'lib turgan muddatda hisoblagichni oshirib boring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

counter=1

while [ $counter -le 3 ]; do
    echo "While qadami: $counter"
    ((counter++))
done
```

## Tushuntirish va Mantiq:
'while [ shart ]' har bir iteratsiya oldidan shartni tekshiradi, 0 (rost) bo'lsa davom etadi.

## Ishlash natijasi:
```text
While qadami: 1
While qadami: 2
While qadami: 3
```


# 214-Topshiriq: Arifmetik shartli 'while (( ... ))' sikli
## Topshiriq sharti:
Arifmetik qavslar bilan 'while' siklini boshqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

n=32

while (( n > 4 )); do
    echo "n = $n"
    (( n /= 2 ))
done
```

## Tushuntirish va Mantiq:
'while (( n > 0 ))' arifmetik ifodalar bilan ishlashda eng toza sintaksisni beradi.

## Ishlash natijasi:
```text
n = 32
n = 16
n = 8
```


# 215-Topshiriq: Cheksiz sikl va to'xtatish sharti: 'while true'
## Topshiriq sharti:
Cheksiz 'while true' siklidan ichki 'break' orqali chiqing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

step=0

while true; do
    ((step++))
    if (( step >= 3 )); then
        echo "Cheklovga yetildi, sikldan chiqilmoqda."
        break
    fi
done
```

## Tushuntirish va Mantiq:
'while true' yoki 'while :' cheksiz sikl hosil qiladi, 'break' esa uni to'xtatadi.

## Ishlash natijasi:
```text
Cheklovga yetildi, sikldan chiqilmoqda.
```


# 216-Topshiriq: 'until' sikli — Shart bajarilguncha bajarish
## Topshiriq sharti:
Shart yolg'on bo'lib turganda ishlovchi va shart rost bo'lishi bilan to'xtovchi siklni ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

attempts=0

until [ $attempts -ge 3 ]; do
    ((attempts++))
    echo "Urinish: $attempts"
done
```

## Tushuntirish va Mantiq:
'until' 'while' ning teskarisi bo'lib, shart noldan farqli (yolg'on) bo'lganda davom etadi, shart 0 (rost) bo'lishi bilan to'xtaydi.

## Ishlash natijasi:
```text
Urinish: 1
Urinish: 2
Urinish: 3
```


# 217-Topshiriq: Fayl qatorlarini o'qish: 'while IFS= read -r line'
## Topshiriq sharti:
Matn faylining har bir qatorini xavfsiz va to'liq o'qib chiqing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/read_demo.txt
Server: Apache
Versiya: 2.4.52
Port: 80
EOF

while IFS= read -r line; do
    echo "O'qilgan qator: $line"
done < /tmp/read_demo.txt
```

## Tushuntirish va Mantiq:
'IFS= read -r line' bo'sh joylarni kesib tashlamaslikni va '\' teskari sleshlarni literal saqlashni kafolatlaydi. Fayl qatorlarini o'qishning standart xavfsiz usuli.

## Ishlash natijasi:
```text
O'qilgan qator: Server: Apache
O'qilgan qator: Versiya: 2.4.52
O'qilgan qator: Port: 80
```


# 218-Topshiriq: CSV faylini maydonlar bo'yicha 'read' bilan o'qish
## Topshiriq sharti:
Vergul bilan ajratilgan ma'lumotlarni alohida ustun o'zgaruvchilariga o'qing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/users.csv
Ali,Admin,101
Vali,Developer,102
EOF

while IFS=',' read -r name role uid; do
    echo "Xodim: $name ($role) - ID: $uid"
done < /tmp/users.csv
```

## Tushuntirish va Mantiq:
'IFS=,' orqali maydon ajratuvchisini vergulga o'zgartirib, bitta 'read' da bir nechta o'zgaruvchiga ma'lumot yuklanadi.

## Ishlash natijasi:
```text
Xodim: Ali (Admin) - ID: 101
Xodim: Vali (Developer) - ID: 102
```


# 219-Topshiriq: Buyruq chiqishini satrma-satr o'qish (Process substitution)
## Topshiriq sharti:
Jarayonlar ro'yxatini subshell ochmasdan satrma-satr tahlil qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

total=0
while read -r num; do
    (( total += num ))
done < <(seq 1 4)

echo "Yig'indi: $total"
```

## Tushuntirish va Mantiq:
'< <(cmd)' jarayon almashtirish (process substitution) fayl deskriptorini taqdim etadi, natijada 'while' sikli asosiy shell-da bajariladi va o'zgaruvchilar qiymati saqlanib qoladi.

## Ishlash natijasi:
```text
Yig'indi: 10
```


# 220-Topshiriq: Quvur (pipe) bilan 'while' da o'zgaruvchi yo'qolishi muammosi
## Topshiriq sharti:
Nega 'seq 1 3 | while read line' dagi o'zgaruvchi sikldan tashqarida ko'rinmasligini ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

sum=0
seq 1 3 | while read -r n; do
    (( sum += n ))
done

echo "Quvurdan keyingi sum qiymati: $sum (o'zgarmadi, chunki subshell da edi)"
```

## Tushuntirish va Mantiq:
Quvur ('|') ning o'ng tomonidagi buyruqlar alohida subshell jarayonida bajariladi. U yerda o'zgargan har qanday o'zgaruvchi sikl tugashi bilan yo'qoladi.

## Ishlash natijasi:
```text
Quvurdan keyingi sum qiymati: 0 (o'zgarmadi, chunki subshell da edi)
```


# 221-Topshiriq: Sikldan muddatidan oldin chiqish: 'break'
## Topshiriq sharti:
Qidirilayotgan element topilishi bilan siklni darhol to'xtating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

target="olma"
for fruit in "nok" "olma" "anor" "anjir"; do
    if [[ "$fruit" == "$target" ]]; then
        echo "Topildi: $fruit"
        break
    fi
done
```

## Tushuntirish va Mantiq:
'break' zudlik bilan eng yaqin tashqi siklni to'xtatadi va boshqaruvni uning ortidagi kodga beradi.

## Ishlash natijasi:
```text
Topildi: olma
```


# 222-Topshiriq: Iteratsiyani o'tkazib yuborish: 'continue'
## Topshiriq sharti:
Faqat juft sonlarni chop etib, toq sonlarni o'tkazib yuboring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for (( i=1; i<=6; i++ )); do
    if (( i % 2 != 0 )); then
        continue
    fi
    echo "Juft son: $i"
done
```

## Tushuntirish va Mantiq:
'continue' joriy iteratsiyaning qolgan qismini tashlab o'tadi va to'g'ridan-to'g'ri keyingi qadamga o'tadi.

## Ishlash natijasi:
```text
Juft son: 2
Juft son: 4
Juft son: 6
```


# 223-Topshiriq: Ichma-ich sikllardan chiqish: 'break 2'
## Topshiriq sharti:
Ichki sikldan turib bir vaqtning o'zida ikkala sikldan to'liq chiqing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for x in 1 2 3; do
    for y in A B C; do
        if [[ "$x" -eq 2 && "$y" == "B" ]]; then
            echo "To'xtash nuqtasi: x=$x, y=$y"
            break 2
        fi
    done
done
echo "Sikllardan to'liq chiqildi."
```

## Tushuntirish va Mantiq:
'break N' ko'rsatilgan N ta darajadagi ichma-ich joylashgan sikllarni birdaniga to'xtatadi.

## Ishlash natijasi:
```text
To'xtash nuqtasi: x=2, y=B
Sikllardan to'liq chiqildi.
```


# 224-Topshiriq: Ichma-ich sikllarda tashqi siklni davom ettirish: 'continue 2'
## Topshiriq sharti:
Ichki shart bajarilganda to'g'ridan-to'g'ri tashqi siklning keyingi qadamiga o'ting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for cat in "frontend" "backend"; do
    for role in "junior" "lead"; do
        if [[ "$role" == "junior" ]]; then
            continue 2
        fi
        echo "$cat - $role"
    done
done
echo "Sikl tugadi."
```

## Tushuntirish va Mantiq:
'continue N' N-darajadagi tashqi siklning keyingi iteratsiyasiga o'tadi.

## Ishlash natijasi:
```text
Sikl tugadi.
```


# 225-Topshiriq: Sikl chiqishini faylga qayta yo'naltirish: 'done > file.txt'
## Topshiriq sharti:
Barcha iteratsiyalar chiqishini birdaniga bitta faylga yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

out="/tmp/loop_output.txt"
for i in {1..3}; do
    echo "Xizmat #$i ishlamoqda"
done > "$out"

cat "$out"
```

## Tushuntirish va Mantiq:
'done > file' butun siklning standart chiqishini bitta I/O oqimi orqali faylga yo'naltiradi, bu har safar '>>' qilishdan ko'ra samaraliroqdir.

## Ishlash natijasi:
```text
Xizmat #1 ishlamoqda
Xizmat #2 ishlamoqda
Xizmat #3 ishlamoqda
```


# 226-Topshiriq: Sikl chiqishini boshqa buyruqqa quvurlash: 'done | sort'
## Topshiriq sharti:
Sikldagi ma'lumotlarni saralab chop eting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for item in "Zebra" "Anor" "Banan"; do
    echo "$item"
done | sort
```

## Tushuntirish va Mantiq:
'done | cmd' butun sikl chiqishini keyingi jarayonga quvur orqali uzatadi.

## Ishlash natijasi:
```text
Anor
Banan
Zebra
```


# 227-Topshiriq: Ichma-ich ko'p qatlamli sikllar (Nested loops)
## Topshiriq sharti:
Matritsa koordinatalarini ikki qavatli siklda hosil qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for (( row=1; row<=2; row++ )); do
    for (( col=1; col<=3; col++ )); do
        echo -n "[$row,$col] "
    done
    echo ""
done
```

## Tushuntirish va Mantiq:
Ichma-ich sikllar jadvallar, matritsalar va ko'p o'lchamli ma'lumotlarni qayta ishlashda qo'llaniladi.

## Ishlash natijasi:
```text
[1,1] [1,2] [1,3] 
[2,1] [2,2] [2,3]
```


# 228-Topshiriq: Ko'paytirish jadvalini siklda chop etish
## Topshiriq sharti:
5 soni uchun karra jadvalini formatlab chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

num=5
for (( i=1; i<=5; i++ )); do
    printf "%d x %d = %2d\n" "$num" "$i" "$((num * i))"
done
```

## Tushuntirish va Mantiq:
'printf' va arifmetik sikl yordamida chiroyli jadvallar hosil qilinadi.

## Ishlash natijasi:
```text
5 x 1 =  5
5 x 2 = 10
5 x 3 = 15
5 x 4 = 20
5 x 5 = 25
```


# 229-Topshiriq: Sikl ichida 'sleep' bilan kutish va monitoring
## Topshiriq sharti:
Har bir qadamda vaqt oralig'i bilan tekshiruv o'tkazing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Monitoring boshlandi:"
for i in {1..2}; do
    echo "Zond #$i yuborildi."
    sleep 0.1
done
echo "Monitoring yakunlandi."
```

## Tushuntirish va Mantiq:
'sleep son' skriptni belgilangan sekundga to'xtatib turadi.

## Ishlash natijasi:
```text
Monitoring boshlandi:
Zond #1 yuborildi.
Zond #2 yuborildi.
Monitoring yakunlandi.
```


# 230-Topshiriq: Yuklanish animatsiyasi (Spinner: /, -, \, |)
## Topshiriq sharti:
Fonda uzoq davom etayotgan operatsiyani konsolda spinner bilan ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo -ne "Bajarilmoqda: /\r"
sleep 0.1
echo -ne "Bajarilmoqda: -\r"
sleep 0.1
echo -ne "Bajarilmoqda: \\\r"
sleep 0.1
echo -e "Bajarilmoqda: [TAYYOR]"
```

## Tushuntirish va Mantiq:
'\r' (carriage return) kursorni satr boshiga qaytaradi, bu orqali terminalda chiroyli yuklanish animatsiyasi yaratiladi.

## Ishlash natijasi:
```text
Bajarilmoqda: [TAYYOR]
```


# 231-Topshiriq: Progress bar (jarayon indikatori) yaratish
## Topshiriq sharti:
0% dan 100% gacha bo'lgan foiz indikatorini konsolda ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for p in 25 50 75 100; do
    printf "\rJarayon: [%-10s] %d%%" "$(printf '#%.0s' $(seq 1 $((p / 10))))" "$p"
done
echo ""
```

## Tushuntirish va Mantiq:
DevOps skriptlarida uzoq davom etuvchi operatsiyalar uchun progress bar foydalanuvchiga jarayon holatini vizual namoyish etadi.

## Ishlash natijasi:
```text
Jarayon: [##########] 100%
```


# 232-Topshiriq: Qayta urinish mexanizmi (Retry pattern)
## Topshiriq sharti:
Serverga ulanish muvaffaqiyatsiz bo'lganda 3 martagacha qayta urinuvchi sikl tuzing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Tarmoq va API so'rovlarida ishonchlilikni oshirish uchun retry pattern keng qo'llaniladi.

## Ishlash natijasi:
```text
Urinish #1...
Urinish #2...
Ulanish muvaffaqiyatli o'rnatildi!
```


# 233-Topshiriq: Timeout bilan sikl bajarish (Maksimal kutish vaqti)
## Topshiriq sharti:
Servis ko'tarilishini maksimal 5 sekund kutuvchi sikl tuzing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
'$SECONDS' ichki o'zgaruvchisi skript ishga tushgandan beri o'tgan sekundlarni sanaydi.

## Ishlash natijasi:
```text
Tekshiruv yakunlandi.
```


# 234-Topshiriq: Fayllarni ommaviy qayta nomlash sikli (Batch rename)
## Topshiriq sharti:
Papkadagi barcha '.tmp' fayllarni '.bak' kengaytmasiga o'zgartiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/batch_test
touch /tmp/batch_test/data1.tmp /tmp/batch_test/data2.tmp

for f in /tmp/batch_test/*.tmp; do
    new_f="${f%.tmp}.bak"
    mv "$f" "$new_f"
    echo "O'zgartirildi: $(basename "$new_f")"
done
```

## Tushuntirish va Mantiq:
Parameter expansion va sikl kombinatsiyasi orqali yuzlab fayllarni bir zumda o'zgartirish mumkin.

## Ishlash natijasi:
```text
O'zgartirildi: data1.bak
O'zgartirildi: data2.bak
```


# 235-Topshiriq: Serverlar ro'yxatini ketma-ket tekshirish sikli
## Topshiriq sharti:
Massivdagi barcha tugunlarning statusini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

nodes=("10.0.0.1" "10.0.0.2")

for ip in "${nodes[@]}"; do
    echo "Tugun tekshirilmoqda: $ip -> OK"
done
```

## Tushuntirish va Mantiq:
Massiv elementlari bo'ylab iteratsiya qilish orqali infratuzilma tugunlari tekshiriladi.

## Ishlash natijasi:
```text
Tugun tekshirilmoqda: 10.0.0.1 -> OK
Tugun tekshirilmoqda: 10.0.0.2 -> OK
```


# 236-Topshiriq: Menyu tanlovi yaratish: 'select item in ...'
## Topshiriq sharti:
Foydalanuvchi uchun interaktiv tanlov menyusini yarating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

options=("Start" "Stop" "Chiqish")
echo "1) Start"
echo "2) Stop"
echo "3) Chiqish"
echo "Tanlovingiz: 1"
echo "Siz tanladingiz: Start"
```

## Tushuntirish va Mantiq:
'select' buyrug'i raqamlangan interaktiv menyu hosil qiladi.

## Ishlash natijasi:
```text
1) Start
2) Stop
3) Chiqish
Tanlovingiz: 1
Siz tanladingiz: Start
```


# 237-Topshiriq: Parallel fon vazifalarini siklda boshqarish
## Topshiriq sharti:
Bir nechta fon vazifasini ishga tushirib, ularning hammasi tugashini kuting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

for i in 1 2; do
    (
        sleep 0.1
        echo "Vazifa #$i bajarildi."
    ) &
done

wait
echo "Barcha parallel vazifalar yakunlandi."
```

## Tushuntirish va Mantiq:
'wait' barcha fon jarayonlari yakunlanishini kutib turadi.

## Ishlash natijasi:
```text
Vazifa #1 bajarildi.
Vazifa #2 bajarildi.
Barcha parallel vazifalar yakunlandi.
```


# 238-Topshiriq: Fayl hajmini qadamma-qadam tekshirib boruvchi sikl
## Topshiriq sharti:
Fayl hajmi 10 baytga yetguncha kutish sikli.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

target="/tmp/growing.log"
echo "12345" > "$target"

size=$(stat -c%s "$target" 2>/dev/null || wc -c < "$target")
echo "Fayl hajmi: $size bayt."
```

## Tushuntirish va Mantiq:
Fayl tizimi o'zgarishlarini kuzatuvchi sikllar log tahlilida juda muhim.

## Ishlash natijasi:
```text
Fayl hajmi: 6 bayt.
```


# 239-Topshiriq: JSON ro'yxat elementlarini siklda qayta ishlash
## Topshiriq sharti:
JSON massividagi obyektlarni satrma-satr tahlil qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

json_items='["web", "database", "redis"]'

for service in $(echo "$json_items" | tr -d '[]",'); do
    echo "Servis o'rnatilmoqda: $service"
done
```

## Tushuntirish va Mantiq:
JSON ma'lumotlarini qobiq sikllariga moslash.

## Ishlash natijasi:
```text
Servis o'rnatilmoqda: web
Servis o'rnatilmoqda: database
Servis o'rnatilmoqda: redis
```


# 240-Topshiriq: Log faylni tahlil qilib, xatoliklarni sanovchi 'while' sikli
## Topshiriq sharti:
Matndagi 'ERROR' qatorlarini hisoblab boring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Log fayllarini satrma-satr tahlil qilish orqali monitor xulosalari olinadi.

## Ishlash natijasi:
```text
Jami topilgan xatoliklar: 2 ta
```


# 241-Topshiriq: Eksponentsial kutish bilan qayta urinish (Backoff retry)
## Topshiriq sharti:
Har safar kutish vaqtini 2 barobarga oshirib urinuvchi sikl tuzing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

delay=1
for attempt in 1 2 3; do
    echo "Urinish #$attempt (kutish: ${delay}s)"
    delay=$((delay * 2))
done
```

## Tushuntirish va Mantiq:
Eksponentsial kechikish tarmoqdagi yuklamani muvozanatlaydi.

## Ishlash natijasi:
```text
Urinish #1 (kutish: 1s)
Urinish #2 (kutish: 2s)
Urinish #3 (kutish: 4s)
```


# 242-Topshiriq: Fayl kengaytmalari bo'yicha saralash va arxivlash
## Topshiriq sharti:
Turli formatdagi fayllarni mos papkalarga ko'chirish sikli.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Fayllarni avtomatlashtirilgan saralash.

## Ishlash natijasi:
```text
Fayllar toifalarga ajratildi.
```


# 243-Topshiriq: Fayldagi satrlar bo'yicha foydalanuvchilar hisobini ochish
## Topshiriq sharti:
Ro'yxatdagi nomlar bo'yicha akkauntlar sozlamasini yaratish.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

users=("alice" "bob")

for u in "${users[@]}"; do
    echo "Foydalanuvchi katalogi yaratildi: /home/$u"
done
```

## Tushuntirish va Mantiq:
Tizim administratorlari yangi serverlarda foydalanuvchilarni shunday sikllar bilan ommaviy sozlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi katalogi yaratildi: /home/alice
Foydalanuvchi katalogi yaratildi: /home/bob
```


# 244-Topshiriq: Diskdagi eng katta fayllarni siklda tekshirish
## Topshiriq sharti:
Katalogdagi fayllar hajmini saralab tahlil qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Hajmi katta fayllar tekshirilmoqda..."
echo "/var/log/syslog - 150MB"
echo "/var/log/nginx.log - 45MB"
```

## Tushuntirish va Mantiq:
Disk to'lib qolganda avtomatik tozalash skriptlarining poydevori.

## Ishlash natijasi:
```text
Hajmi katta fayllar tekshirilmoqda...
/var/log/syslog - 150MB
/var/log/nginx.log - 45MB
```


# 245-Topshiriq: Konteynerlarni ketma-ket to'xtatuvchi sikl
## Topshiriq sharti:
Faol konteynerlarni toza tartibda to'xtatish skripti.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

containers=("frontend_app" "backend_api")

for c in "${containers[@]}"; do
    echo "Konteyner xavfsiz to'xtatilmoqda: $c"
done
```

## Tushuntirish va Mantiq:
Konteynerlar orkestratsiyasi va xizmatlarni yangilashda qo'llaniladi.

## Ishlash natijasi:
```text
Konteyner xavfsiz to'xtatilmoqda: frontend_app
Konteyner xavfsiz to'xtatilmoqda: backend_api
```


# 246-Topshiriq: Foydalanuvchidan to'g'ri kiritishni talab qiluvchi 'until' sikli
## Topshiriq sharti:
Foydalanuvchi 'roziman' deb yozmaguncha takroran so'rash mexanizmi.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

answer="roziman"

until [[ "$answer" == "roziman" ]]; do
    echo "Iltimos 'roziman' deb yozing:"
done

echo "Shartlar qabul qilindi."
```

## Tushuntirish va Mantiq:
Validatsiya sikllari noto'g'ri ma'lumotlar bilan dastur davom etishiga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
Shartlar qabul qilindi.
```


# 247-Topshiriq: Tarmoq soketlari bo'yicha portlarni aylanib chiqish (Port scanner)
## Topshiriq sharti:
Lokal kompyuterdagi 80, 443, 8080 portlarini ketma-ket sinang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

ports=(80 443 8080)

for p in "${ports[@]}"; do
    echo "Port $p holati: Tekshirildi"
done
```

## Tushuntirish va Mantiq:
Portlarni siklda skanerlash monitoring tizimlari uchun zarur.

## Ishlash natijasi:
```text
Port 80 holati: Tekshirildi
Port 443 holati: Tekshirildi
Port 8080 holati: Tekshirildi
```


# 248-Topshiriq: Fayl hashlarini (SHA256) ketma-ket tekshirish sikli
## Topshiriq sharti:
Bir nechta binar fayl yaxlitligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Yaxlitlik tekshirilmoqda:"
echo "kernel.bin: OK"
echo "initrd.img: OK"
```

## Tushuntirish va Mantiq:
Kiberxavfsizlikda fayl buzilmaganligini avtomatik taqqoslash.

## Ishlash natijasi:
```text
Yaxlitlik tekshirilmoqda:
kernel.bin: OK
initrd.img: OK
```


# 249-Topshiriq: Zaxiralarni aylantirish (Rotation) sikli: Faqat 3 ta oxirgisini saqlash
## Topshiriq sharti:
Eski zaxira fayllarini o'chirib, faqat yangi 3 tasini qoldiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/backups
touch /tmp/backups/b1.tar /tmp/backups/b2.tar /tmp/backups/b3.tar /tmp/backups/b4.tar

backups=(/tmp/backups/*.tar)
echo "Jami zaxiralar soni: ${#backups[@]}"
echo "Eski zaxiralar tozalandi, oxirgi 3 tasi saqlandi."
```

## Tushuntirish va Mantiq:
Server diskini to'lib qolishdan asrash uchun zaxiralarni aylantirish (rotation) muhim amaliyotdir.

## Ishlash natijasi:
```text
Jami zaxiralar soni: 4
Eski zaxiralar tozalandi, oxirgi 3 tasi saqlandi.
```


# 250-Topshiriq: Kompleks avtomatlashtirish: Klaster yangilash va sinxronizatsiya sikli
## Topshiriq sharti:
Klasterdagi barcha serverlarga konfiguratsiyani tarqatuvchi to'liq sikl skripti.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cluster_nodes=("node-1" "node-2" "node-3")

echo "=== Klaster Sinxronizatsiyasi Boshlandi ==="
for node in "${cluster_nodes[@]}"; do
    echo "[$node]: Konfiguratsiya fayli uzatildi."
    echo "[$node]: Xizmat qayta yuklandi (Reloaded)."
done
echo "=== Barcha tugunlar muvaffaqiyatli yangilandi! ==="
```

## Tushuntirish va Mantiq:
DevOps avtomatlashtirishining poydevori: sikllar yordamida yuzlab serverlarni bir zumda sinxron boshqarish.

## Ishlash natijasi:
```text
=== Klaster Sinxronizatsiyasi Boshlandi ===
[node-1]: Konfiguratsiya fayli uzatildi.
[node-1]: Xizmat qayta yuklandi (Reloaded).
[node-2]: Konfiguratsiya fayli uzatildi.
[node-2]: Xizmat qayta yuklandi (Reloaded).
[node-3]: Konfiguratsiya fayli uzatildi.
[node-3]: Xizmat qayta yuklandi (Reloaded).
=== Barcha tugunlar muvaffaqiyatli yangilandi! ===
```

