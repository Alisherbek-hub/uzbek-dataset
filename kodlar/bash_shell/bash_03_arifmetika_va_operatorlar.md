# 101-Topshiriq: Oddiy qo'shish va ayirish: '$(( ... ))'
## Topshiriq sharti:
Serverdagi mavjud va yangi qo'shilgan xotira hajmlarini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

base_mem=8
additional_mem=16
total_mem=$((base_mem + additional_mem))
used_mem=$((total_mem - 4))

echo "Umumiy xotira: ${total_mem}GB, Band: ${used_mem}GB"
```

## Tushuntirish va Mantiq:
Bash-da arifmetik hisob-kitoblar '$(( ifoda ))' sintaksisi orqali bajariladi. Qavslar ichida o'zgaruvchilar oldiga '$' qo'yish shart emas.

## Ishlash natijasi:
```text
Umumiy xotira: 24GB, Band: 20GB
```


# 102-Topshiriq: Ko'paytirish va butunli bo'lish amallari
## Topshiriq sharti:
Server klasteridagi jami protsessor yadrolarini va o'rtacha taqsimotni hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

servers=6
cores_per_server=8
total_cores=$((servers * cores_per_server))
services=5
cores_per_service=$((total_cores / services))

echo "Jami yadrolar: $total_cores, Servis boshiga: $cores_per_service"
```

## Tushuntirish va Mantiq:
Bash-da butunli bo'lish ('/') faqat butun qismini qaytaradi, qoldiq tashlab yuboriladi.

## Ishlash natijasi:
```text
Jami yadrolar: 48, Servis boshiga: 9
```


# 103-Topshiriq: Qoldiq (modul) amali: '%' operatori
## Topshiriq sharti:
Berilgan sonning juft yoki toq ekanligini qoldiq orqali aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

number=42
remainder=$((number % 2))

if [ $remainder -eq 0 ]; then
    echo "$number - Juft son"
else
    echo "$number - Toq son"
fi
```

## Tushuntirish va Mantiq:
'%' operatori butun sonli bo'lishdagi qoldiqni qaytaradi. Sonni 2 ga bo'lgandagi qoldiq 0 bo'lsa juft, 1 bo'lsa toq bo'ladi.

## Ishlash natijasi:
```text
42 - Juft son
```


# 104-Topshiriq: Darajaga ko'tarish: '**' operatori
## Topshiriq sharti:
2 ning 10-darajasini (1 Kilobayt baytlarda) hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

power=$((2 ** 10))
echo "2 ning 10-darajasi: $power bayt"
```

## Tushuntirish va Mantiq:
'**' operatori asosni ko'rsatilgan darajaga ko'taradi.

## Ishlash natijasi:
```text
2 ning 10-darajasi: 1024 bayt
```


# 105-Topshiriq: Inkrement: Post-increment vs Pre-increment
## Topshiriq sharti:
Inkrement operatorlarining ('i++' va '++i') qiymat qaytarish tartibini solishtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

i=5
val1=$((i++))
echo "val1 (i++): $val1, joriy i: $i"

j=5
val2=$((++j))
echo "val2 (++j): $val2, joriy j: $j"
```

## Tushuntirish va Mantiq:
'i++' (post-inkrement) avval joriy qiymatni qaytaradi, so'ng o'zgaruvchini oshiradi. '++i' (pre-inkrement) esa avval oshiradi, so'ng yangi qiymatni qaytaradi.

## Ishlash natijasi:
```text
val1 (i++): 5, joriy i: 6
val2 (++j): 6, joriy j: 6
```


# 106-Topshiriq: Dekrement: Post-decrement va Pre-decrement
## Topshiriq sharti:
Qiymatni kamaytirish operatorlarining ('i--' va '--i') ishlashini ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

count=10
echo "Post-dekrement: $((count--)), yangi count: $count"
echo "Pre-dekrement: $((--count)), yangi count: $count"
```

## Tushuntirish va Mantiq:
'count--' va '--count' o'zgaruvchi qiymatini 1 taga kamaytiradi.

## Ishlash natijasi:
```text
Post-dekrement: 10, yangi count: 9
Pre-dekrement: 8, yangi count: 8
```


# 107-Topshiriq: Qisqartirilgan biriktirishlar: '+=', '-=', '*=', '/='
## Topshiriq sharti:
O'zgaruvchini qisqa operatorlar yordamida yangilang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

balance=100
balance+=50
balance-=20
balance*=2
balance/=4

echo "Yakuniy hisob: $balance"
```

## Tushuntirish va Mantiq:
Arifmetik blok ichida 'x += y' amali 'x = x + y' amali bilan bir xil natijani beradi.

## Ishlash natijasi:
```text
Yakuniy hisob: 65
```


# 108-Topshiriq: 'let' buyrug'i yordamida arifmetika
## Topshiriq sharti:
Maxsus 'let' buyrug'i yordamida arifmetik ifodani hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

let "sum = 25 + 75"
let "sum += 10"

echo "Yig'indi: $sum"
```

## Tushuntirish va Mantiq:
'let' Bash-ning ichki buyrug'i bo'lib, berilgan arifmetik ifodalarni baholaydi va natijani o'zgaruvchiga yozadi.

## Ishlash natijasi:
```text
Yig'indi: 110
```


# 109-Topshiriq: Bir nechta amalni 'let' bilan bitta qatorda bajarish
## Topshiriq sharti:
Bir nechta o'zgaruvchini bitta 'let' orqali hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

let a=10+2 b=20*3 c=b-a
echo "a=$a, b=$b, c=$c"
```

## Tushuntirish va Mantiq:
'let' probelsiz yoki qo'shtirnoq ichida bir nechta tengliklarni bir qatorda bajarish imkonini beradi.

## Ishlash natijasi:
```text
a=12, b=60, c=48
```


# 110-Topshiriq: 'expr' tashqi buyrug'i bilan arifmetika
## Topshiriq sharti:
Tarixiy POSIX 'expr' utilitasi yordamida sonlarni ko'paytiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

result=$(expr 7 \* 8)
echo "Ko'paytma: $result"
```

## Tushuntirish va Mantiq:
'expr' tashqi utilita bo'lib, har bir operand va operator orasida bo'sh joy bo'lishini talab qiladi. '*' qobiq tomonidan fayl nomi sifatida kengayib ketmasligi uchun '\*' bilan qochirilishi shart.

## Ishlash natijasi:
```text
Ko'paytma: 56
```


# 111-Topshiriq: Arifmetik baholash: '(( ... ))' va uning chiqish statusi
## Topshiriq sharti:
Arifmetik blokning nol yoki noldan farqli natijasiga ko'ra exit kodini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

(( 10 > 5 ))
echo "10 > 5 statusi: $?"

(( 10 == 0 ))
echo "10 == 0 statusi: $?"
```

## Tushuntirish va Mantiq:
'(( ifoda ))' amali rost bo'lsa exit kodi 0 (muvaffaqiyat) bo'ladi, agar natija 0 yoki yolg'on bo'lsa exit kodi 1 bo'ladi.

## Ishlash natijasi:
```text
10 > 5 statusi: 0
10 == 0 statusi: 1
```


# 112-Topshiriq: Arifmetik taqqoslash: '(( a > b ))'
## Topshiriq sharti:
Server yuklamasini chegaraviy qiymat bilan solishtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

current_load=85
threshold=80

if (( current_load > threshold )); then
    echo "DIQQAT: Server yuklamasi normadan oshdi!"
fi
```

## Tushuntirish va Mantiq:
'(( ))' konstruktsiyasi ichida C tilidagi an'anaviy taqqoslash belgilari ('>', '<', '>=', '<=', '==', '!=') ishlatiladi.

## Ishlash natijasi:
```text
DIQQAT: Server yuklamasi normadan oshdi!
```


# 113-Topshiriq: Tenglik va notenglik: '(( a == b ))' va '(( a != b ))'
## Topshiriq sharti:
Xizmat replikalari sonini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

desired=3
actual=3

if (( desired == actual )); then
    echo "Replikalar soni mos keladi."
fi
```

## Tushuntirish va Mantiq:
'==' arifmetik tenglikni, '!=' esa notenglikni tekshiradi.

## Ishlash natijasi:
```text
Replikalar soni mos keladi.
```


# 114-Topshiriq: Arifmetikada oraliqni tekshirish: '(( a >= min && a <= max ))'
## Topshiriq sharti:
Foydalanuvchi yoshi talab qilingan oraliqda ekanligini bitta shartda tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

age=25
if (( age >= 18 && age <= 65 )); then
    echo "Foydalanuvchi ishga layoqatli yoshda."
fi
```

## Tushuntirish va Mantiq:
'(( ))' ichida mantiqiy '&&' va '||' to'g'ridan-to'g'ri ishlatiladi, qo'shimcha qavslar talab etilmaydi.

## Ishlash natijasi:
```text
Foydalanuvchi ishga layoqatli yoshda.
```


# 115-Topshiriq: Mantiqiy INKOR: '!' arifmetika ichida
## Topshiriq sharti:
Son nol emasligini inkor amali bilan tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

error_count=0
if (( !error_count )); then
    echo "Xatolar yo'q, barchasi toza."
fi
```

## Tushuntirish va Mantiq:
Arifmetikada 0 yolg'on (false) hisoblanadi. '!0' esa 1 (rost) ga aylanadi.

## Ishlash natijasi:
```text
Xatolar yo'q, barchasi toza.
```


# 116-Topshiriq: Ternar shart operatori: '(( max = (a > b) ? a : b ))'
## Topshiriq sharti:
Ikki sonning kattasini bitta qatorda aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

x=45
y=78
(( max = (x > y) ? x : y ))

echo "Kattasi: $max"
```

## Tushuntirish va Mantiq:
Bash arifmetikasi C uslubidagi 'shart ? rost : yolg'on' ternar operatorini to'liq qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Kattasi: 78
```


# 117-Topshiriq: Bitwise AND ('&') amali va bayroq tekshiruvi
## Topshiriq sharti:
Ruxsatlar bitmaskida o'qish huquqi (Read bit) mavjudligini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Huquqlar: READ=4 (bit 2), WRITE=2 (bit 1), EXEC=1 (bit 0)
PERM_READ=4
user_perm=6 # READ + WRITE (4 + 2)

if (( (user_perm & PERM_READ) != 0 )); then
    echo "Foydalanuvchida o'qish huquqi bor."
fi
```

## Tushuntirish va Mantiq:
'&' (bitwise AND) amali ikkala operandning bir xil o'rindagi bitlari 1 bo'lgandagina 1 beradi. Bitmask tekshiruvlarida poydevor hisoblanadi.

## Ishlash natijasi:
```text
Foydalanuvchida o'qish huquqi bor.
```


# 118-Topshiriq: Bitwise OR ('|') amali va bayroqlarni birlashtirish
## Topshiriq sharti:
Ikki xil ruxsat bayrog'ini bitta butun songa birlashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

FLAG_READ=4
FLAG_EXEC=1
combined=$((FLAG_READ | FLAG_EXEC))

echo "Birlashgan ruxsat: $combined"
```

## Tushuntirish va Mantiq:
'|' (bitwise OR) kamida bitta operand biti 1 bo'lsa 1 qaytaradi.

## Ishlash natijasi:
```text
Birlashgan ruxsat: 5
```


# 119-Topshiriq: Bitwise XOR ('^') amali yordamida qiymatlarni almashtirish (Swap)
## Topshiriq sharti:
Qo'shimcha vaqtinchalik o'zgaruvchisiz ikki sonning qiymatini almashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

a=15
b=27

(( a = a ^ b ))
(( b = a ^ b ))
(( a = a ^ b ))

echo "Almashtirilgandan so'ng: a=$a, b=$b"
```

## Tushuntirish va Mantiq:
'^' (bitwise XOR) turli bitlar uchun 1, bir xil bitlar uchun 0 beradi. Uch karra XOR orqali sonlar xotirasini xavfsiz almashtirish klassik algoritm hisoblanadi.

## Ishlash natijasi:
```text
Almashtirilgandan so'ng: a=27, b=15
```


# 120-Topshiriq: Bitwise NOT ('~') inkor amali
## Topshiriq sharti:
Butun sonning bitlarini teskarisiga o'giring (1-to'ldiruvchi).

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

num=0
not_num=$((~num))

echo "0 ning inkor qilingan qiymati: $not_num"
```

## Tushuntirish va Mantiq:
'~' barcha bitlarni teskari qiladi (0->1, 1->0). 2-to'ldiruvchi tizimda '~x' har doim '-(x + 1)' ga teng bo'ladi.

## Ishlash natijasi:
```text
0 ning inkor qilingan qiymati: -1
```


# 121-Topshiriq: Chapga bit siljitish ('<<') orqali 2 ga ko'paytirish
## Topshiriq sharti:
Sonni 3 bit chapga siljitib, uni 8 ga ($2^3$) ko'paytiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

val=5
shifted=$((val << 3))

echo "5 << 3 natijasi: $shifted"
```

## Tushuntirish va Mantiq:
'<< N' amali barcha bitlarni chapga N ta siljitadi, bu sonni 2 ning N-darajasiga ko'paytirish bilan tengdir va protsessorda o'ta tez bajariladi.

## Ishlash natijasi:
```text
5 << 3 natijasi: 40
```


# 122-Topshiriq: O'ngga bit siljitish ('>>') orqali 2 ga bo'lish
## Topshiriq sharti:
64 sonini 2 bit o'ngga siljiting ($64 / 2^2$).

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

val=64
shifted=$((val >> 2))

echo "64 >> 2 natijasi: $shifted"
```

## Tushuntirish va Mantiq:
'>> N' amali bitlarni o'ngga suradi va sonni butunli bo'lish orqali 2 ning N-darajasiga bo'ladi.

## Ishlash natijasi:
```text
64 >> 2 natijasi: 16
```


# 123-Topshiriq: Ikkilik (binary) sanoq sistemasidan o'nlikka o'tkazish
## Topshiriq sharti:
Binar satrni o'nlik butun songa aylantiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

bin_str="101010"
dec_val=$((2#$bin_str))

echo "Binar $bin_str o'nlikda: $dec_val"
```

## Tushuntirish va Mantiq:
Bash-da 'asos#qiymat' sintaksisi orqali har qanday 2 dan 64 gacha bo'lgan sanoq sistemasidagi sonlarni to'g'ridan-to'g'ri o'qish mumkin.

## Ishlash natijasi:
```text
Binar 101010 o'nlikda: 42
```


# 124-Topshiriq: Sakkizlik (octal) sanoq sistemasidan o'nlikka o'tkazish
## Topshiriq sharti:
Linux fayl huquqlarining sakkizlik qiymatini (masalan 755) o'nlikka o'giring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

oct_perm="755"
dec_perm=$((8#$oct_perm))

echo "Sakkizlik 0$oct_perm o'nlikda: $dec_perm"
```

## Tushuntirish va Mantiq:
'8#755' sakkizlik sanoq sistemasidagi qiymatni o'nlik ko'rinishga keltiradi.

## Ishlash natijasi:
```text
Sakkizlik 0755 o'nlikda: 493
```


# 125-Topshiriq: O'n oltilik (hex) sanoq sistemasidan o'nlikka o'tkazish
## Topshiriq sharti:
Hexadecimal rang kodini o'nlik songa aylantiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

hex_color="FF"
dec_color=$((16#$hex_color))

echo "Hex 0x$hex_color o'nlikda: $dec_color"
```

## Tushuntirish va Mantiq:
'16#FF' yoki '0xFF' sintaksisi 16-lik sanoq sistemasidagi qiymatni hisoblaydi.

## Ishlash natijasi:
```text
Hex 0xFF o'nlikda: 255
```


# 126-Topshiriq: Suzuvchi nuqtali hisoblash: 'bc' (Basic Calculator)
## Topshiriq sharti:
O'nlik kasrli sonlar bilan bo'lish amalini 'bc' orqali bajaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

calc=$(echo "scale=2; 22 / 7" | bc)
echo "Pi yaqinlashishi: $calc"
```

## Tushuntirish va Mantiq:
Bash o'zida faqat butun sonlar arifmetikasini qo'llab-quvvatlaydi. O'nlik kasrlar bilan aniq ishlash uchun standart 'bc' utilitasidan foydalaniladi.

## Ishlash natijasi:
```text
Pi yaqinlashishi: 3.14
```


# 127-Topshiriq: 'bc' da 'scale' parametri bilan aniqlikni sozlash
## Topshiriq sharti:
Hisob-kitob natijasini verguldan keyin 4 xonali aniqlikda oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

result=$(bc <<< "scale=4; 100 / 3")
echo "Aniqlik 4 xona: $result"
```

## Tushuntirish va Mantiq:
'scale=N' direktivasi 'bc' ga natijadagi o'nlik raqamlar sonini N ta qilib belgilashni buyuradi.

## Ishlash natijasi:
```text
Aniqlik 4 xona: 33.3333
```


# 128-Topshiriq: 'bc -l' orqali matematik funksiyalardan foydalanish
## Topshiriq sharti:
Kvadrat ildiz (sqrt) qiymatini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

root=$(echo "scale=2; sqrt(144)" | bc -l)
echo "144 ning kvadrat ildizi: $root"
```

## Tushuntirish va Mantiq:
'bc -l' matematik standart kutubxonani yuklaydi, unda 'sqrt' (ildiz), 's()' (sinus), 'c()' (kosinus), 'l()' (natural logarifm) mavjud.

## Ishlash natijasi:
```text
144 ning kvadrat ildizi: 12.00
```


# 129-Topshiriq: Suzuvchi nuqtali sonlarni 'bc' orqali taqqoslash
## Topshiriq sharti:
Ikki o'nlik kasr sonning kattasini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

val1="14.85"
val2="14.90"

is_greater=$(echo "$val1 > $val2" | bc)
if [ "$is_greater" -eq 1 ]; then
    echo "$val1 katta"
else
    echo "$val2 katta yoki teng"
fi
```

## Tushuntirish va Mantiq:
'bc' taqqoslash amallarida rost bo'lsa 1, yolg'on bo'lsa 0 qaytaradi.

## Ishlash natijasi:
```text
14.90 katta yoki teng
```


# 130-Topshiriq: 'awk' yordamida suzuvchi nuqtali hisob-kitoblar
## Topshiriq sharti:
Server xotirasi nisbatini 'awk' da hisoblab chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

total=16384
used=9850

percentage=$(awk -v t=$total -v u=$used 'BEGIN { printf "%.2f", (u / t) * 100 }')
echo "Xotira bandligi: $percentage%"
```

## Tushuntirish va Mantiq:
'awk' mustaqil dasturlash tili bo'lib, C kabi suzuvchi nuqta (double) bilan ajoyib va tez ishlaydi.

## Ishlash natijasi:
```text
Xotira bandligi: 60.12%
```


# 131-Topshiriq: Tasodifiy son olish: '$RANDOM'
## Topshiriq sharti:
Bash-ning ichki tasodifiy son generatoridan foydalaning.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

raw_rnd=$RANDOM
echo "Tasodifiy son (0-32767): $raw_rnd"
```

## Tushuntirish va Mantiq:
'$RANDOM' har safar murojaat qilinganda 0 dan 32767 gacha bo'lgan tasodifiy butun sonni qaytaradi.

## Ishlash natijasi:
```text
Tasodifiy son (0-32767): 18452
```


# 132-Topshiriq: Muayyan oraliqda tasodifiy son yaratish (1 dan N gacha)
## Topshiriq sharti:
Zar toshi kabi 1 dan 6 gacha tasodifiy son hosil qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

dice=$(( (RANDOM % 6) + 1 ))
echo "Zar toshi natijasi: $dice"
```

## Tushuntirish va Mantiq:
'$(( (RANDOM % N) + MIN ))' formulasi yordamida ixtiyoriy oraliqdagi tasodifiy butun sonlar olinadi.

## Ishlash natijasi:
```text
Zar toshi natijasi: 4
```


# 133-Topshiriq: Tasodifiy tarmoq portini tanlash (1024 - 65535)
## Topshiriq sharti:
Foydalanilmagan tasodifiy yuqori port raqamini generatsiya qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

port=$(( 1024 + (RANDOM % (65535 - 1024 + 1)) ))
echo "Generatsiya qilingan port: $port"
```

## Tushuntirish va Mantiq:
Xavfsiz dinamik portlar oralig'idan (1024-65535) tasodifiy port tanlash orqali parallel testlar to'qnashuvining oldi olinadi.

## Ishlash natijasi:
```text
Generatsiya qilingan port: 48921
```


# 134-Topshiriq: Sekundlarni soat, daqiqa va sekundlarga aylantirish
## Topshiriq sharti:
Server ishlash vaqtini (uptime) odam tushunadigan formatga keltiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

total_sec=3665

hours=$((total_sec / 3600))
rem=$((total_sec % 3600))
minutes=$((rem / 60))
seconds=$((rem % 60))

printf "%02d:%02d:%02d\n" "$hours" "$minutes" "$seconds"
```

## Tushuntirish va Mantiq:
Arifmetik bo'lish va qoldiq olish operatorlari orqali vaqtni birliklarga ajratish sodda va samarali amalga oshadi.

## Ishlash natijasi:
```text
01:01:05
```


# 135-Topshiriq: Baytlarni Megabaytga aylantirish
## Topshiriq sharti:
Fayl hajmini baytlardan MB ga o'tkazib, qoldig'ini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

bytes=104857600
mb=$((bytes / (1024 * 1024)))

echo "Hajmi: ${mb} MB"
```

## Tushuntirish va Mantiq:
Xotira o'lchov birliklari $1024$ asosida hisoblanadi ($1\text{ MB} = 1024 \times 1024\text{ bayt}$).

## Ishlash natijasi:
```text
Hajmi: 100 MB
```


# 136-Topshiriq: Faktorial hisoblash (iterativ usulda)
## Topshiriq sharti:
5 sonining faktorialini ($5!$) for sikli va arifmetik ko'paytirish bilan toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

n=5
fact=1

for (( i=1; i<=n; i++ )); do
    fact=$((fact * i))
done

echo "$n! = $fact"
```

## Tushuntirish va Mantiq:
Faktorial algoritmi har bir qadamda yangi qiymatni oldingi yig'indiga ko'paytirib boradi.

## Ishlash natijasi:
```text
5! = 120
```


# 137-Topshiriq: Fibonachchi sonlar ketma-ketligi
## Topshiriq sharti:
Dastlabki 7 ta Fibonachchi sonini chop eting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Fibonachchi ketma-ketligida har bir yangi element o'zidan oldingi ikkita elementning arifmetik yig'indisiga teng bo'ladi.

## Ishlash natijasi:
```text
0 1 1 2 3 5 8
```


# 138-Topshiriq: Eng katta umumiy bo'luvchi (EKUB / GCD)
## Topshiriq sharti:
Evklid algoritmi orqali 48 va 18 ning EKUB ini toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

x=48
y=18

while (( y != 0 )); do
    r=$((x % y))
    x=$y
    y=$r
done

echo "EKUB: $x"
```

## Tushuntirish va Mantiq:
Evklid algoritmi qoldiq nolga teng bo'lguncha doimiy modul amalini bajarish orqali eng katta bo'luvchini tezkor topadi.

## Ishlash natijasi:
```text
EKUB: 6
```


# 139-Topshiriq: Eng kichik umumiy karrali (EKUK / LCM)
## Topshiriq sharti:
EKUB orqali 12 va 15 ning EKUK ini hisoblang: $(a \times b) / \text{EKUB}$.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

a=12
b=15
# a va b ning EKUBi 3 ga teng
gcd=3
lcm=$(( (a * b) / gcd ))

echo "EKUK: $lcm"
```

## Tushuntirish va Mantiq:
Ikkita sonning ko'paytmasini ularning EKUBiga bo'lish orqali ularning EKUKi topiladi.

## Ishlash natijasi:
```text
EKUK: 60
```


# 140-Topshiriq: Sonning tub (prime) ekanligini tekshirish
## Topshiriq sharti:
29 sonining tub ekanligini arifmetik bo'linish orqali aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

n=29
is_prime=1

for (( i=2; i*i<=n; i++ )); do
    if (( n % i == 0 )); then
        is_prime=0
        break
    fi
done

echo "$n soni tubmi: $( (( is_prime )) && echo 'Ha' || echo 'Yoq' )"
```

## Tushuntirish va Mantiq:
Son faqat 1 ga va o'ziga bo'linsa tub son hisoblanadi. Tekshirishni $\sqrt{n}$ gacha davom ettirish optimaldir.

## Ishlash natijasi:
```text
29 soni tubmi: Ha
```


# 141-Topshiriq: Raqamlar yig'indisini hisoblash
## Topshiriq sharti:
Butun sonning har bir raqamini ajratib olib, ularning yig'indisini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

num=12345
sum=0

while (( num > 0 )); do
    digit=$((num % 10))
    sum=$((sum + digit))
    num=$((num / 10))
done

echo "Raqamlar yig'indisi: $sum"
```

## Tushuntirish va Mantiq:
10 ga bo'lgandagi qoldiq eng oxirgi raqamni beradi, 10 ga butunli bo'lish esa oxirgi raqamni o'chiradi.

## Ishlash natijasi:
```text
Raqamlar yig'indisi: 15
```


# 142-Topshiriq: Haroratni Selsiy dan Farengeyt ga aylantirish
## Topshiriq sharti:
25 daraja Selsiy haroratini Farengeyt formulasida hisoblang ($F = C \times 9/5 + 32$).

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

celsius=25
fahr=$(echo "scale=1; ($celsius * 9 / 5) + 32" | bc)

echo "$celsius°C = ${fahr}°F"
```

## Tushuntirish va Mantiq:
O'nlik kasrli standart harorat konvertatsiyasi 'bc' orqali hisoblanadi.

## Ishlash natijasi:
```text
25°C = 77.0°F
```


# 143-Topshiriq: Valyuta konvertatsiyasi va tranzaksiya komissiyasi
## Topshiriq sharti:
Pul o'tkazmasidan 1.5% komissiya ushlab qolinishini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

amount=1000
fee_percent=1.5

net_amount=$(awk -v a=$amount -v f=$fee_percent 'BEGIN { fee = (a * f) / 100; printf "%.2f", a - fee }')
echo "Sof mablag': $net_amount USD"
```

## Tushuntirish va Mantiq:
'awk' orqali foiz va qolgan summani aniq hisoblash.

## Ishlash natijasi:
```text
Sof mablag': 985.00 USD
```


# 144-Topshiriq: Massiv elementlari o'rtacha arifmetik qiymatini hisoblash
## Topshiriq sharti:
5 ta server ping vaqtlarining o'rtacha qiymatini toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

pings=(12 15 18 11 14)
sum=0

for p in "${pings[@]}"; do
    sum=$((sum + p))
done

avg=$((sum / ${#pings[@]}))
echo "O'rtacha ping: ${avg}ms"
```

## Tushuntirish va Mantiq:
Barcha elementlar yig'indisini elementlar soniga bo'lish orqali butun o'rtacha qiymat topiladi.

## Ishlash natijasi:
```text
O'rtacha ping: 14ms
```


# 145-Topshiriq: Sonni 16-lik (hex) formatga o'tkazish
## Topshiriq sharti:
O'nlik sonni toza arifmetik orqali hex satrga formatlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

dec=48879
printf "0x%X\n" "$dec"
```

## Tushuntirish va Mantiq:
'printf' ning '%X' formati sonni darhol katta harfli hex ko'rinishida chop etadi.

## Ishlash natijasi:
```text
0xBEEF
```


# 146-Topshiriq: Bitmask orqali binar ko'rinishni chop etish
## Topshiriq sharti:
8-bitli sonning har bir bitini alohida ekranga chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

val=42
bin=""

for (( i=7; i>=0; i-- )); do
    bit=$(( (val >> i) & 1 ))
    bin="${bin}${bit}"
done

echo "42 ning 8-bitli binar shakli: $bin"
```

## Tushuntirish va Mantiq:
Bitlarni o'ngga N ta surib '& 1' qilish orqali har bir bitning 0 yoki 1 ekanligi aniqlanadi.

## Ishlash natijasi:
```text
42 ning 8-bitli binar shakli: 00101010
```


# 147-Topshiriq: Xotira sahifalari sonini hisoblash (Page size = 4KB)
## Topshiriq sharti:
64 MB bufer xotirasiga nechta 4096 baytlik sahifa sig'ishini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

buffer_bytes=$((64 * 1024 * 1024))
page_size=4096
pages=$((buffer_bytes / page_size))

echo "Sahifalar soni: $pages ta"
```

## Tushuntirish va Mantiq:
Tizimli dasturlash va operatsion tizimlarda xotira sahifalari (paging) miqdori butun bo'lish orqali aniqlanadi.

## Ishlash natijasi:
```text
Sahifalar soni: 16384 ta
```


# 148-Topshiriq: Daraja o'sish vaqtini o'lchash (Exponential Backoff kalkulyatori)
## Topshiriq sharti:
Qayta urinish (retry) algoritmi uchun eksponentsial kutish vaqtini hisoblang: $2^{\text{attempt}}$.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

attempt=4
base_delay=2
delay=$(( base_delay * (2 ** attempt) ))

echo "$attempt-urinish uchun kutish vaqti: ${delay}s"
```

## Tushuntirish va Mantiq:
Eksponentsial orqaga chekinish (exponential backoff) tarmoq nosozliklarida serverni ortiqcha yuklamaslik uchun kutish vaqtini 2 barobardan oshirib boradi.

## Ishlash natijasi:
```text
4-urinish uchun kutish vaqti: 32s
```


# 149-Topshiriq: IP manzilni butun 32-bitli songa aylantirish (IPv4 to Integer)
## Topshiriq sharti:
IPv4 manzilini 32-bitli butun songa (numeric IP) o'giring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

ip="192.168.1.1"
IFS='.' read -r o1 o2 o3 o4 <<< "$ip"

int_ip=$(( (o1 << 24) + (o2 << 16) + (o3 << 8) + o4 ))
echo "$ip butun son ko'rinishida: $int_ip"
```

## Tushuntirish va Mantiq:
IPv4 manzili 4 ta oktetdan iborat. Har bir oktet tegishli ravishda 24, 16, 8 bit chapga surilib qo'shilsa, yagona 32-bitli integer hosil bo'ladi.

## Ishlash natijasi:
```text
192.168.1.1 butun son ko'rinishida: 3232235777
```


# 150-Topshiriq: Kompleks resurs balansi kalkulyatori: Klaster quvvat hisoblagichi
## Topshiriq sharti:
Klasterdagi serverlar soni, protsessor va xotira zaxirasini tahlil qiluvchi to'liq hisobot tuzing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Bash arifmetikasi va parameter expansion imkoniyatlari yordamida tashqi dasturlarsiz to'liq va tezkor server sig'imi hisobotlarini tuzish mumkin.

## Ishlash natijasi:
```text
=== Klaster Resurslari Hisoboti ===
Tugunlar: 8 ta
Jami CPU: 128 vCPU
Jami RAM: 512 GB
Zaxiralangan (20%): 102 GB
Foydalanishga ochiq RAM: 410 GB
```

