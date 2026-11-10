# 1-Topshiriq: Shebang (#!/usr/bin/env bash) va oddiy matn chiqarish
## Topshiriq sharti:
Linux tizimida to'g'ri interpreter ko'rsatilgan eng sodda Bash skriptini yozing va konsolga xush kelibsiz xabarini chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Khorazmiy AI - Bash Shell kursi
echo "Linux Shell dunyosiga xush kelibsiz!"
```

## Tushuntirish va Mantiq:
Har qanday professional Bash skripti birinchi qatorda '#!/usr/bin/env bash' shebang direktivasi bilan boshlanishi kerak. Bu operatsion tizimga ushbu faylni bajarishda aynan qaysi qobiq interpretatoridan foydalanish kerakligini ko'rsatadi. 'echo' buyrug'i esa berilgan satrni standart chiqish oqimiga (stdout) yo'naltiradi.

## Ishlash natijasi:
```text
Linux Shell dunyosiga xush kelibsiz!
```


# 2-Topshiriq: 'echo -e' bilan rangli va maxsus belgilarni chiqarish
## Topshiriq sharti:
Konsolga ANSI escape kodlari yordamida yashil rangli muvaffaqiyat xabari va yangi qator belgisini chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

GREEN='\033[0;32m'
NC='\033[0m' # Rangni asl holiga qaytarish (No Color)

echo -e "${GREEN}[Muvaffaqiyat]: Tizim yangilanishi yakunlandi!${NC}\nKeyingi bosqichga o'tilmoqda..."
```

## Tushuntirish va Mantiq:
'echo' buyrug'i sukut bo'yicha maxsus qochirish belgilarini oddiy matn deb qabul qiladi. '-e' opsiyasi berilganda, u '\n' (yangi qator), '\t' (tabulyatsiya) va ANSI rang kodlarini to'g'ri talqin qiladi. Xabardan so'ng '\033[0m' yordamida rangni asl holiga qaytarish shart, aks holda keyingi barcha matnlar ham yashil rangda chiqadi.

## Ishlash natijasi:
```text
[Muvaffaqiyat]: Tizim yangilanishi yakunlandi!
Keyingi bosqichga o'tilmoqda...
```


# 3-Topshiriq: 'echo -n' bilan qator tashlamasdan chiqarish
## Topshiriq sharti:
Matnni yangi qatorga o'tmasdan chop eting va keyingi buyruq bilan bir qatorda davom ettiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo -n "Server yuklanmoqda... "
echo "[TAYYOR]"
```

## Tushuntirish va Mantiq:
Sukut bo'yicha 'echo' buyrug'i har bir matndan keyin yangi qator belgisini (newline, '\n') avtomatik qo'shadi. '-n' parametri bu xatti-harakatni bekor qiladi, natijada keyingi 'echo' buyrug'ining chiqishi avvalgi satrning davomidan yoziladi.

## Ishlash natijasi:
```text
Server yuklanmoqda... [TAYYOR]
```


# 4-Topshiriq: 'printf' yordamida satr va butun sonlarni formatlash
## Topshiriq sharti:
Foydalanuvchi ismi va uning tizimdagi UID raqamini 'printf' yordamida jadval ko'rinishida formatlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

username="admin"
user_id=1001

printf "Foydalanuvchi: %-10s | UID: %05d\n" "$username" "$user_id"
```

## Tushuntirish va Mantiq:
'printf' buyrug'i C tilidagi printf funktsiyasi kabi formatlangan chiqishni ta'minlaydi. '%-10s' matnni chap tomonga tekislab 10 ta belgi kenglik ajratadi, '%05d' esa butun sonni 5 xonali qilib, oldidagi bo'sh joylarni nollar bilan to'ldiradi.

## Ishlash natijasi:
```text
Foydalanuvchi: admin      | UID: 01001
```


# 5-Topshiriq: 'printf' yordamida o'nlik kasrlarni formatlash
## Topshiriq sharti:
Server CPU yuklamasini o'nlik kasr ko'rinishida 2 xona aniqlikda formatlab chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cpu_load="12.34567"

printf "CPU Yuklamasi: %.2f%%\n" "$cpu_load"
```

## Tushuntirish va Mantiq:
'printf' dagi '%.2f' format spetsifikatori berilgan o'nlik kasr sonning faqat nuqtadan keyingi 2 ta raqamini yaxlitlab chiqaradi. '%%' esa foiz belgisining o'zini ekranga chiqarish uchun xizmat qiladi.

## Ishlash natijasi:
```text
CPU Yuklamasi: 12.35%
```


# 6-Topshiriq: 'printf' yordamida o'n oltilik (hex) va sakkizlik (octal) chiqarish
## Topshiriq sharti:
O'nlik sanoq sistemasidagi sonni 16-lik (hex) va 8-lik (octal) ko'rinishda chop eting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

number=255

printf "O'nlik: %d | Hex: 0x%X | Sakkizlik: 0%o\n" "$number" "$number" "$number"
```

## Tushuntirish va Mantiq:
'printf' da '%X' butun sonni katta harflar bilan o'n oltilik (hexadecimal) shaklda chiqaradi, '%o' esa sakkizlik (octal) formatga o'tkazadi. Bu binar va tizimli dasturlashda baytlarni tekshirishda juda qo'l keladi.

## Ishlash natijasi:
```text
O'nlik: 255 | Hex: 0xFF | Sakkizlik: 0377
```


# 7-Topshiriq: Chiqish status kodi ($?) ni tekshirish
## Topshiriq sharti:
Oxirgi bajarilgan buyruq muvaffaqiyatli tugaganini exit status kodi orqali aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

ls /etc/hosts > /dev/null 2>&1
status=$?

echo "Oxirgi buyruq exit kodi: $status"
if [ $status -eq 0 ]; then
    echo "Fayl muvaffaqiyatli topildi."
fi
```

## Tushuntirish va Mantiq:
Linux va Bash-da har bir buyruq tugaganda 0 dan 255 gacha bo'lgan exit kod (chiqish kodi) qaytaradi. 0 kodi har doim 'muvaffaqiyatli yakunlandi' degan ma'noni anglatadi. Noldan farqli har qanday kod xatolik yuz berganini bildiradi. '$?' maxsus o'zgaruvchisi oxirgi buyruqning aynan shu kodini saqlaydi.

## Ishlash natijasi:
```text
Oxirgi buyruq exit kodi: 0
Fayl muvaffaqiyatli topildi.
```


# 8-Topshiriq: 'true' va 'false' buyruqlarining exit kodlari
## Topshiriq sharti:
Tizimdagi 'true' va 'false' yordamchi buyruqlarining chiqish kodlarini solishtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

true
echo "true exit kodi: $?"

false
echo "false exit kodi: $?"
```

## Tushuntirish va Mantiq:
'true' buyrug'i har doim 0 (muvaffaqiyat) kodi bilan chiqadi, 'false' buyrug'i esa har doim 1 (xato) kodi bilan chiqadi. Ular cheksiz sikllarda yoki shartli zanjirlarda default qiymat sifatida keng qo'llaniladi.

## Ishlash natijasi:
```text
true exit kodi: 0
false exit kodi: 1
```


# 9-Topshiriq: Bir tirnoq ('...') va qo'sh tirnoq ("...") farqi
## Topshiriq sharti:
O'zgaruvchini bir tirnoq va qo'sh tirnoq ichida chop etib, interpolatsiya farqini ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

server="production-web-01"

echo "Qo'sh tirnoqda: Server nomi - $server"
echo 'Bir tirnoqda: Server nomi - $server'
```

## Tushuntirish va Mantiq:
Qo'sh tirnoqlar (weak quoting) ichidagi o'zgaruvchilar va buyruq almashtirishlar interpolatsiya qilinadi (kengaytiriladi). Bir tirnoqlar (strong quoting) ichidagi har qanday belgi, jumladan '$' ham mutlaqo literal (xom matn) holida qoladi va hech qanday kengaytirish amalga oshirilmaydi.

## Ishlash natijasi:
```text
Qo'sh tirnoqda: Server nomi - production-web-01
Bir tirnoqda: Server nomi - $server
```


# 10-Topshiriq: Tirnoqlar ichida belgilarni qochirish (escaping with \)
## Topshiriq sharti:
Qo'sh tirnoq ichida '$' belgisi va qo'shtirnoqning o'zini ekranga chiqarish uchun qochirish belgisini qo'llang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

price=150
echo "Mahsulot narxi \$$price ni tashkil etadi va bu \"Chegirma\" zonasidadir."
```

## Tushuntirish va Mantiq:
Teskari slesh ('\') maxsus belgilarni qochirish (escaping) uchun xizmat qiladi. '\$' Bash ga ushbu '$' belgisi o'zgaruvchi emas, balki oddiy dollar belgisi ekanligini, '\"' esa qo'shtirnoq satr tugashi emas, balki matn belgisi ekanligini bildiradi.

## Ishlash natijasi:
```text
Mahsulot narxi $150 ni tashkil etadi va bu "Chegirma" zonasidadir.
```


# 11-Topshiriq: Buyruq almashtirish: '$(command)' sintaksisi
## Topshiriq sharti:
Tizimning joriy sana va vaqtini o'zgaruvchiga saqlang va xabarda chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

current_date=$(date "+%Y-%m-%d %H:%M:%S")
echo "Tizimning joriy vaqti: $current_date"
```

## Tushuntirish va Mantiq:
Buyruq almashtirish (command substitution) '$(buyruq)' sintaksisi orqali amalga oshiriladi. Subshell ichida ko'rsatilgan buyruq bajariladi va uning standart chiqishi (stdout) o'zgaruvchiga qiymat qilib beriladi. Eskirgan `buyruq` (backticks) ga nisbatan '$(...)' o'qilishi oson va ichma-ich joylashtirish imkonini beradi.

## Ishlash natijasi:
```text
Tizimning joriy vaqti: 2026-11-08 15:30:00
```


# 12-Topshiriq: Shell o'zgaruvchisi e'lon qilish va qiymatini o'qish
## Topshiriq sharti:
O'zgaruvchilarni tenglik belgisi atrofida bo'sh joy qoldirmasdan e'lon qiling va qiymatini o'qing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

app_name="KhorazmiyEngine"
version="1.0.4"

echo "Ilova: $app_name, Versiya: $version"
```

## Tushuntirish va Mantiq:
Bash-da o'zgaruvchi yaratishda 'nom=qiymat' formatida tenglik belgisi atrofida aslo bo'sh joy (space) qoldirish mumkin emas. Bo'sh joy qo'yilsa, Bash uni buyruq va uning argumentlari deb noto'g'ri talqin qiladi.

## Ishlash natijasi:
```text
Ilova: KhorazmiyEngine, Versiya: 1.0.4
```


# 13-Topshiriq: O'zgaruvchilarni eksport qilish ('export')
## Topshiriq sharti:
O'zgaruvchini farzand jarayonlar (subprocesses) uchun ochiq qilish uchun 'export' dan foydalaning.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

export CLUSTER_ENV="production"
bash -c 'echo "Farzand subshell ichida: $CLUSTER_ENV"'
```

## Tushuntirish va Mantiq:
Oddiy shell o'zgaruvchilari faqat joriy jarayon doirasida amal qiladi. Farzand jarayonlar (skriptlar, chaqirilgan utilitalar) unga kira olmaydi. 'export' kalit so'zi o'zgaruvchini muhit o'zgaruvchisiga aylantiradi, natijada barcha avlod jarayonlar uning nusxasiga ega bo'ladi.

## Ishlash natijasi:
```text
Farzand subshell ichida: production
```


# 14-Topshiriq: Tizim muhit o'zgaruvchilarini ko'rish ('printenv')
## Topshiriq sharti:
Tizimda mavjud barcha muhit o'zgaruvchilaridan 'USER' va 'SHELL' ni 'printenv' orqali oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

current_user=$(printenv USER)
current_shell=$(printenv SHELL)

echo "Foydalanuvchi: $current_user | Standart qobiq: $current_shell"
```

## Tushuntirish va Mantiq:
'printenv' yoki 'env' buyrug'i joriy sessiyaning barcha muhit o'zgaruvchilarini ko'rsatadi. Aniq bir o'zgaruvchi nomini argument sifatida berish orqali uning qiymatini to'g'ridan-to'g'ri o'qish mumkin.

## Ishlash natijasi:
```text
Foydalanuvchi: user | Standart qobiq: /bin/bash
```


# 15-Topshiriq: 'PATH' muhit o'zgaruvchisini kengaytirish
## Topshiriq sharti:
Yangi maxsus buyruqlar joylashgan papkani joriy 'PATH' ga xavfsiz qo'shing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

custom_bin="$HOME/.local/bin"
export PATH="$custom_bin:$PATH"

echo "Yangi PATH boshlanishi: $(echo $PATH | cut -d: -f1)"
```

## Tushuntirish va Mantiq:
'PATH' tizimda buyruq nomi kiritilganda binar fayllarni qaysi kataloglardan qidirish kerakligini ko'rsatuvchi ikki nuqta (':') bilan ajratilgan ro'yxatdir. Yangi manzilni uning boshiga 'export PATH="...:$PATH"' qilib qo'shish orqali foydalanuvchi skriptlariga ustuvorlik beriladi.

## Ishlash natijasi:
```text
Yangi PATH boshlanishi: /home/user/.local/bin
```


# 16-Topshiriq: 'HOME' va 'USER' maxsus tizim o'zgaruvchilari
## Topshiriq sharti:
Foydalanuvchining uy katalogi va nomini avtomatik aniqlab chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Xush kelibsiz, hurmatli $USER!"
echo "Sizning shaxsiy katalogingiz: $HOME"
```

## Tushuntirish va Mantiq:
Linux tizimida '$USER' joriy tizimga kirgan foydalanuvchi loginini, '$HOME' esa uning asosiy uy katalogi manzilini (masalan, '/home/user') saqlaydi.

## Ishlash natijasi:
```text
Xush kelibsiz, hurmatli user!
Sizning shaxsiy katalogingiz: /home/user
```


# 17-Topshiriq: 'PWD' va 'OLDPWD' orqali kataloglar o'rtasida navigatsiya
## Topshiriq sharti:
Katalog almashtirish va oldingi katalogga tezda qaytish mexanizmini ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Boshlang'ich katalog: $PWD"
cd /tmp
echo "Yangi katalog: $PWD"
cd - > /dev/null
echo "Qaytilgan katalog (OLDPWD orqali): $PWD"
```

## Tushuntirish va Mantiq:
'$PWD' joriy ishchi katalogni ko'rsatadi. 'cd -' buyrug'i esa '$OLDPWD' o'zgaruvchisida saqlangan avvalgi katalogga tezda qaytish imkonini beradi.

## Ishlash natijasi:
```text
Boshlang'ich katalog: /home/user
Yangi katalog: /tmp
Qaytilgan katalog (OLDPWD orqali): /home/user
```


# 18-Topshiriq: Skriptning o'z joylashgan manzilini aniqlash
## Topshiriq sharti:
Skript qayerdan chaqirilishidan qat'i nazar, uning haqiqiy papkasini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
echo "Skript joylashgan haqiqiy manzil: $SCRIPT_DIR"
```

## Tushuntirish va Mantiq:
DevOps va avtomatlashtirishda skriptlar ko'pincha turli kataloglardan ishga tushiriladi. 'dirname "${BASH_SOURCE[0]}"' skript faylining nisbiy yo'lini beradi, 'cd' va 'pwd' bilan birlashtirilganda uning mutlaq (absolute) manzili aniq olinadi.

## Ishlash natijasi:
```text
Skript joylashgan haqiqiy manzil: /home/user/scripts
```


# 19-Topshiriq: Chuqur kataloglar ierarxiyasini yaratish ('mkdir -p')
## Topshiriq sharti:
Bir nechta ichma-ich joylashgan kataloglarni bitta buyruq bilan xavfsiz yarating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

target_dir="/tmp/khorazmiy_dataset/logs/2026/11"
mkdir -p "$target_dir"

if [ -d "$target_dir" ]; then
    echo "Kataloglar zanjiri yaratildi: $target_dir"
fi
```

## Tushuntirish va Mantiq:
'mkdir' buyrug'iga '-p' (parents) bayrog'i berilsa, u barcha yetishmayotgan ota kataloglarni ketma-ket avtomatik yaratadi. Agar katalog allaqachon mavjud bo'lsa, xatolik chiqarmasdan xavfsiz davom etadi.

## Ishlash natijasi:
```text
Kataloglar zanjiri yaratildi: /tmp/khorazmiy_dataset/logs/2026/11
```


# 20-Topshiriq: Fayl yaratish va vaqt tamg'asini yangilash ('touch')
## Topshiriq sharti:
Yangi bo'sh konfiguratsiya faylini yarating va uning yaratilganligini tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

config_file="/tmp/app_config.env"
touch "$config_file"

ls -l "$config_file" | awk '{print $9, "fayli muvaffaqiyatli yaratildi."}'
```

## Tushuntirish va Mantiq:
'touch' buyrug'i agar ko'rsatilgan fayl mavjud bo'lmasa, uni bo'sh holda yaratadi. Agar fayl mavjud bo'lsa, uning o'zgartirilgan (mtime) va murojaat qilingan (atime) vaqt tamg'alarini joriy vaqtga yangilaydi.

## Ishlash natijasi:
```text
/tmp/app_config.env fayli muvaffaqiyatli yaratildi.
```


# 21-Topshiriq: Fayllarni rekursiv nusxalash ('cp -r')
## Topshiriq sharti:
Katalog va uning barcha ichki fayllarini yangi manzilga nusxalang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/src_dir && touch /tmp/src_dir/data.txt
cp -r /tmp/src_dir /tmp/dest_dir

echo "Nusxa yaratildi: $(ls /tmp/dest_dir)"
```

## Tushuntirish va Mantiq:
'cp' (copy) buyrug'i fayllarni nusxalaydi. Kataloglarni ichidagi barcha fayllar va kichik papkalar bilan birga nusxalash uchun '-r' yoki '-R' (recursive) parametri talab qilinadi.

## Ishlash natijasi:
```text
Nusxa yaratildi: data.txt
```


# 22-Topshiriq: Fayllarni ko'chirish va qayta nomlash ('mv')
## Topshiriq sharti:
Fayl nomini o'zgartiring va boshqa katalogga ko'chiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

touch /tmp/old_name.log
mv /tmp/old_name.log /tmp/new_name.log

if [ -f "/tmp/new_name.log" ]; then
    echo "Fayl nomi muvaffaqiyatli o'zgartirildi."
fi
```

## Tushuntirish va Mantiq:
Linux-da faylni qayta nomlash va boshqa katalogga ko'chirish bitta 'mv' (move) buyrug'i orqali bajariladi. Bu operatsion tizim darajasida faqat inode havolasini yangilaydi, ma'lumotlarni jismonan qayta yozmaydi.

## Ishlash natijasi:
```text
Fayl nomi muvaffaqiyatli o'zgartirildi.
```


# 23-Topshiriq: Fayl va papkalarni tozalash ('rm -rf')
## Topshiriq sharti:
Vaqtinchalik sinov katalogini barcha ichki elementlari bilan tozalang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/temp_trash
rm -rf /tmp/temp_trash

echo "Tozalash yakunlandi. Mavjudlik holati: $([ -d /tmp/temp_trash ] && echo 'Bor' || echo 'Yoq')"
```

## Tushuntirish va Mantiq:
'rm' buyrug'i fayllarni o'chiradi. '-r' rekursiv ravishda papkalarni, '-f' (force) esa ruxsat so'ramasdan va xatolar bo'lsa ularni e'tiborsiz qoldirib majburiy o'chirishni ta'minlaydi. Ishlab chiqarish tizimlarida juda ehtiyotkorlik bilan ishlatilishi zarur.

## Ishlash natijasi:
```text
Tozalash yakunlandi. Mavjudlik holati: Yoq
```


# 24-Topshiriq: Katalog tarkibini batafsil ko'rish ('ls -la')
## Topshiriq sharti:
Yashirin fayllar va fayl ruxsatlarini ko'rsatuvchi ro'yxatni filtrlab chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/test_ls && touch /tmp/test_ls/.hidden /tmp/test_ls/visible.txt
ls -la /tmp/test_ls | awk 'NR>1 {print $1, $9}'
```

## Tushuntirish va Mantiq:
'ls -l' batafsil (long listing: huquqlar, egasi, hajmi, vaqti) formatida chiqaradi, '-a' (all) esa nuqta ('.') bilan boshlanadigan yashirin konfiguratsiya fayllarini ham ko'rsatadi.

## Ishlash natijasi:
```text
.
..
.hidden
visible.txt
```


# 25-Topshiriq: Hajmlarni inson tushunadigan formatda ko'rish ('ls -lh')
## Topshiriq sharti:
Fayl hajmlarini baytlar o'rniga KB, MB, GB formatida ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/test_h && truncate -s 10M /tmp/test_h/large.bin
ls -lh /tmp/test_h/large.bin | awk '{print "Fayl:", $9, "| Hajmi:", $5}'
```

## Tushuntirish va Mantiq:
'-h' (human-readable) parametri baytlarni (masalan, 10485760) avtomatik ravishda 10M, 4.2K kabi oson tushuniladigan birliklarga aylantirib beradi.

## Ishlash natijasi:
```text
Fayl: /tmp/test_h/large.bin | Hajmi: 10M
```


# 26-Topshiriq: Vaqt bo'yicha teskari saralash ('ls -ltr')
## Topshiriq sharti:
Katalogdagi eng oxirgi o'zgartirilgan fayllarni ro'yxat oxirida ko'rsatish usulini yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/sort_test
touch /tmp/sort_test/old.txt
sleep 0.1
touch /tmp/sort_test/new.txt

ls -1tr /tmp/sort_test
```

## Tushuntirish va Mantiq:
'-t' fayllarni modifikatsiya vaqti bo'yicha saralaydi, '-r' (reverse) esa teskari tartibda joylashtiradi. Natijada eng so'nggi yaratilgan yoki yangilangan fayllar eng pastda ko'rinadi, bu esa server loglarini kuzatishda qulaydir.

## Ishlash natijasi:
```text
old.txt
new.txt
```


# 27-Topshiriq: Fayl qatorlarini raqamlab chiqarish ('cat -n')
## Topshiriq sharti:
Matn faylining har bir qatorini raqamlari bilan konsolga chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/demo_lines.txt
Birinchi qator
Ikkinchi qator
Uchinchi qator
EOF

cat -n /tmp/demo_lines.txt
```

## Tushuntirish va Mantiq:
'cat' (concatenate) fayllarni birlashtirish va chiqarish buyrug'i. '-n' (number) parametri uning har bir qatori boshiga 1 dan boshlab tartib raqamini qo'shadi.

## Ishlash natijasi:
```text
1	Birinchi qator
     2	Ikkinchi qator
     3	Uchinchi qator
```


# 28-Topshiriq: Matn qatorlarini 'nl' orqali formatlash
## Topshiriq sharti:
Faqat bo'sh bo'lmagan qatorlarni maxsus formatda raqamlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/nl_demo.txt
Server boshlandi

Xizmatlar tayyor
EOF

nl -ba /tmp/nl_demo.txt
```

## Tushuntirish va Mantiq:
'nl' (number lines) buyrug'i matn qatorlarini raqamlash uchun ixtisoslashgan bo'lib, bo'sh qatorlarni raqamlamaslik yoki maxsus ajratgichlar qo'yish imkoniyatlarini taqdim etadi.

## Ishlash natijasi:
```text
1	Server boshlandi
     2	
     3	Xizmatlar tayyor
```


# 29-Topshiriq: Fayl boshidagi qatorlarni ajratish ('head -n')
## Topshiriq sharti:
10 qatorlik fayldan dastlabki 3 qatorni ajratib oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

seq 1 5 > /tmp/seq.txt
head -n 3 /tmp/seq.txt
```

## Tushuntirish va Mantiq:
'head' buyrug'i faylning boshidan boshlab o'qiydi. '-n 3' parametri dastlabki 3 ta qatorni chiqarishni buyuradi. Sukut bo'yicha '-n' ko'rsatilmasa 10 ta qator chop etiladi.

## Ishlash natijasi:
```text
1
2
3
```


# 30-Topshiriq: Fayl oxiridagi qatorlarni ajratish ('tail -n')
## Topshiriq sharti:
Faylning eng so'nggi 2 ta qatorini oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

seq 10 15 > /tmp/seq_end.txt
tail -n 2 /tmp/seq_end.txt
```

## Tushuntirish va Mantiq:
'tail' buyrug'i fayl oxiridan boshlab o'qiydi. '-n 2' eng oxirgi 2 qatorni chiqaradi. Server konfiguratsiyalari va log xulosalarini olishda juda foydali.

## Ishlash natijasi:
```text
14
15
```


# 31-Topshiriq: Log fayllarni real vaqt rejimida kuzatish ('tail -f')
## Topshiriq sharti:
Yangi yozilayotgan loglarni jonli o'qish mexanizmini modellashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "tail -f buyrug'i yangi qatorlar qo'shilishini kutib turadi."
echo "Misol: tail -f /var/log/nginx/access.log"
```

## Tushuntirish va Mantiq:
'tail -f' (follow) fayl deskriptorini ochiq tutadi va faylga yangi ma'lumot yozilishi bilan uni darhol konsolga chiqaradi. Bu DevOps muhandislari uchun server xizmatlarini tekshirishning asosiy vositasidir.

## Ishlash natijasi:
```text
tail -f buyrug'i yangi qatorlar qo'shilishini kutib turadi.
Misol: tail -f /var/log/nginx/access.log
```


# 32-Topshiriq: Qatorlar sonini aniqlash ('wc -l')
## Topshiriq sharti:
Matn faylida jami nechta qator borligini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/wc_demo.txt
Qator 1
Qator 2
Qator 3
Qator 4
EOF

lines=$(wc -l < /tmp/wc_demo.txt)
echo "Jami qatorlar soni: $lines"
```

## Tushuntirish va Mantiq:
'wc' (word count) utilitasi matn statistikasini hisoblaydi. '-l' (lines) bayrog'i yangi qator belgilarini sanaydi. '<' orqali faylni yo'naltirish natijada fayl nomi chiqmasdan faqat toza son olinishini ta'minlaydi.

## Ishlash natijasi:
```text
Jami qatorlar soni: 4
```


# 33-Topshiriq: So'zlar va baytlar sonini sanash ('wc -w' va 'wc -c')
## Topshiriq sharti:
Fayldagi so'zlar va jami baytlar miqdorini tahlil qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

text="Salom Khorazmiy AI"
words=$(echo -n "$text" | wc -w)
bytes=$(echo -n "$text" | wc -c)

echo "So'zlar: $words, Baytlar: $bytes"
```

## Tushuntirish va Mantiq:
'-w' (words) bo'sh joylar bilan ajratilgan so'zlarni sanaydi, '-c' (bytes) esa matn egallagan aniq baytlar miqdorini hisoblab beradi.

## Ishlash natijasi:
```text
So'zlar: 3, Baytlar: 18
```


# 34-Topshiriq: Buyruq turini aniqlash ('type')
## Topshiriq sharti:
Berilgan buyruq ichki (builtin) yoki tashqi dastur ekanligini 'type' orqali aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

type cd
type ls
```

## Tushuntirish va Mantiq:
'type' buyrug'i qobiq qanday qilib ushbu buyruqni bajarishini tushuntiradi: u shell builtin (masalan, 'cd'), tashqi fayl, alias yoki kalit so'z ekanligini ajratib ko'rsatadi.

## Ishlash natijasi:
```text
cd is a shell builtin
ls is an alias for ls --color=auto
```


# 35-Topshiriq: Binar fayl manzilini topish ('which' va 'command -v')
## Topshiriq sharti:
Tizimda 'python3' yoki 'bash' ijro fayli qaysi yo'lda turganini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

bash_bin=$(command -v bash)
echo "Bash ijro fayli manzili: $bash_bin"
```

## Tushuntirish va Mantiq:
POSIX standartida 'command -v' tashqi binar yo'lini aniqlash uchun 'which' ga qaraganda ishonchliroq va tezroq hisoblanadi, chunki u ichki shell mexanizmidan foydalanadi.

## Ishlash natijasi:
```text
Bash ijro fayli manzili: /usr/bin/bash
```


# 36-Topshiriq: Buyruqqa alias (taxallus) biriktirish
## Topshiriq sharti:
Qisqartirilgan buyruq yaratish va uni ishlatishni ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

shopt -s expand_aliases
alias salom='echo "Assalomu alaykum!"'

salom
```

## Tushuntirish va Mantiq:
'alias' buyrug'i uzun buyruqlar uchun qisqa nomlar yaratish imkonini beradi. Skriptlar ichida aliaslar sukut bo'yicha o'chiq bo'ladi, uni 'shopt -s expand_aliases' orqali faollashtirish kerak.

## Ishlash natijasi:
```text
Assalomu alaykum!
```


# 37-Topshiriq: Aliasni bekor qilish ('unalias')
## Topshiriq sharti:
Yaratilgan aliasni xotiradan tozalang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

shopt -s expand_aliases
alias testcmd='echo 123'
unalias testcmd

echo "Alias bekor qilindi."
```

## Tushuntirish va Mantiq:
'unalias' ko'rsatilgan taxallusni bekor qiladi va qobiqni asl buyruqlarga qaytaradi.

## Ishlash natijasi:
```text
Alias bekor qilindi.
```


# 38-Topshiriq: Buyruqlar tarixidan foydalanish ('history')
## Topshiriq sharti:
Terminalda bajarilgan oxirgi buyruqlar tarixini tahlil qilish mexanizmini yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Buyruqlar tarixi 'HISTFILE' ($HOME/.bash_history) faylida saqlanadi."
echo "Joriy sessiyada 'history' orqali ko'riladi."
```

## Tushuntirish va Mantiq:
Bash har bir foydalanuvchi bajargan buyruqlarni xotirada saqlaydi va sessiya yakunlanganda ~/.bash_history fayliga yozadi. 'HISTSIZE' va 'HISTFILESIZE' o'zgaruvchilari tarix hajmini boshqaradi.

## Ishlash natijasi:
```text
Buyruqlar tarixi 'HISTFILE' (/home/user/.bash_history) faylida saqlanadi.
Joriy sessiyada 'history' orqali ko'riladi.
```


# 39-Topshiriq: Fon rejimi (&) da jarayonni yurgizish
## Topshiriq sharti:
Vaqt talab qiluvchi buyruqni fonga yuborib, skriptni to'xtovsiz davom ettiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

sleep 1 &
bg_pid=$!

echo "Fon jarayoni PID: $bg_pid ishga tushirildi."
wait $bg_pid
echo "Fon jarayoni tugadi."
```

## Tushuntirish va Mantiq:
Buyruq oxiriga '&' belgisi qo'yilsa, qobiq uning tugashini kutmasdan darhol keyingi qatorga o'tadi. '$!' o'zgaruvchisi esa oxirgi fonda ishga tushirilgan jarayonning PID raqamini saqlaydi.

## Ishlash natijasi:
```text
Fon jarayoni PID: 12345 ishga tushirildi.
Fon jarayoni tugadi.
```


# 40-Topshiriq: Subshell (...) va o'zgaruvchilar izolyatsiyasi
## Topshiriq sharti:
Qavslar ichida o'zgaruvchini o'zgartirib, asosiy shell ga ta'sir qilmasligini ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

count=10
(
    count=999
    echo "Subshell ichida: count = $count"
)
echo "Asosiy shell ichida: count = $count"
```

## Tushuntirish va Mantiq:
Oddiy yumaloq qavslar '( ... )' buyruqlarni alohida subshell (farzand jarayon) da bajaradi. U yerdagi o'zgaruvchilar va katalog o'zgarishlari asosiy ota shell ga aslo ta'sir qilmaydi.

## Ishlash natijasi:
```text
Subshell ichida: count = 999
Asosiy shell ichida: count = 10
```


# 41-Topshiriq: Guruhlash { ...; } va joriy kontekstda bajarish
## Topshiriq sharti:
Figurali qavslar orqali bir nechta buyruqni bitta blokda va bitta chiqish oqimiga birlashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

{
    echo "Hisobot sanasi: $(date +%Y)"
    echo "Holat: OK"
} > /tmp/group_report.txt

cat /tmp/group_report.txt
```

## Tushuntirish va Mantiq:
Figurali qavslar '{ buyruqlar; }' buyruqlarni subshell ochmasdan, joriy shell muhitida guruhlaydi. Bu orqali bir nechta buyruqlar chiqishini bitta faylga yoki quvurga yo'naltirish qulaydir. Oxirgi buyruqdan so'ng ';' bo'lishi shart.

## Ishlash natijasi:
```text
Hisobot sanasi: 2026
Holat: OK
```


# 42-Topshiriq: Ketma-ket bajarish operatori (;)
## Topshiriq sharti:
Bir nechta mustaqil buyruqni bir qatorda nuqta-vergul bilan ajratib bajaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Qadam 1"; echo "Qadam 2"; echo "Qadam 3"
```

## Tushuntirish va Mantiq:
Nuqta-vergul (';') buyruqlarni ketma-ket bajarishni ta'minlaydi. Oldingi buyruq xato bilan tugasa ham, keyingi buyruqlar baribir bajarilaveradi.

## Ishlash natijasi:
```text
Qadam 1
Qadam 2
Qadam 3
```


# 43-Topshiriq: Mantiqiy VA (&&) operatori bilan buyruqlar zanjiri
## Topshiriq sharti:
Faqat birinchi buyruq muvaffaqiyatli (exit code 0) bo'lgandagina ikkinchi buyruqni ishga tushiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/pipeline_test && echo "Papka yaratildi, davom etamiz!"
```

## Tushuntirish va Mantiq:
'cmd1 && cmd2' konstruksiyasida 'cmd2' faqat va faqat 'cmd1' muvaffaqiyatli (0 kodi bilan) yakunlangandagina bajariladi. Bu zanjirli operatsiyalarda xatoliklarni erta to'xtatishning eng samarali usuli.

## Ishlash natijasi:
```text
Papka yaratildi, davom etamiz!
```


# 44-Topshiriq: Mantiqiy YOKI (||) operatori bilan zaxira amal
## Topshiriq sharti:
Buyruq xato bilan tugagan taqdirda xabar beruvchi zaxira buyruqni ulang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

ls /mavjud_bolmagan_fayl_123 2> /dev/null || echo "OGOHLANTIRISH: Kerakli fayl topilmadi!"
```

## Tushuntirish va Mantiq:
'cmd1 || cmd2' konstruksiyasida 'cmd2' faqat 'cmd1' xatolik (noldan farqli kod) bilan tugaganda bajariladi. Bu orqali default holatlarni belgilash va xato xabarlarini chiqarish mumkin.

## Ishlash natijasi:
```text
OGOHLANTIRISH: Kerakli fayl topilmadi!
```


# 45-Topshiriq: Shartli qisqa operator: 'cmd1 && cmd2 || cmd3'
## Topshiriq sharti:
Ternar operator kabi bir qatorda tekshiruv va natija chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

num=10
[ $num -gt 5 ] && echo "Katta" || echo "Kichik"
```

## Tushuntirish va Mantiq:
Ushbu konstruksiya C tilidagi '(shart) ? to'g'ri : noto'g'ri' ternar operatoriga o'xshaydi. Shart bajarilsa birinchi qism, bajarilmasa ikkinchi qism ishga tushadi.

## Ishlash natijasi:
```text
Katta
```


# 46-Topshiriq: 'set -x' orqali skriptni disk raskadrovka qilish
## Topshiriq sharti:
Skriptning har bir bajarilayotgan qatorini terminalda ko'rsatishni yoqing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -x
a=5
b=10
c=$((a + b))
set +x

echo "Natija: $c"
```

## Tushuntirish va Mantiq:
'set -x' (xtrace) rejimi har bir buyruq bajarilishidan oldin uning kengaytirilgan ko'rinishini '+' belgisi bilan konsolga chiqaradi. Bu skriptlardagi xatolarni topish (debugging) uchun bebahodir.

## Ishlash natijasi:
```text
+ a=5
+ b=10
+ c=15
+ set +x
Natija: 15
```


# 47-Topshiriq: 'set +x' orqali debug rejimini o'chirish
## Topshiriq sharti:
Maxfiy ma'lumotlar bor sohada xtrace rejimini vaqtincha to'xtatib, so'ng qayta yoqing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Debug o'chirildi, xavfsiz blok bajarilmoqda."
```

## Tushuntirish va Mantiq:
'set +x' xtrace rejimini bekor qiladi. Maxfiy tokenlar, parollar bilan ishlaganda ularni loglarga tushib qolmasligi uchun xtrace o'chirilishi shart.

## Ishlash natijasi:
```text
Debug o'chirildi, xavfsiz blok bajarilmoqda.
```


# 48-Topshiriq: Qobiq turi va versiyasini aniqlash
## Topshiriq sharti:
Tizimdagi joriy Bash versiyasi va ishlayotgan qobiqni chop eting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Qobiq: $SHELL"
echo "Bash versiyasi: $BASH_VERSION"
```

## Tushuntirish va Mantiq:
'$BASH_VERSION' ichki o'zgaruvchisi o'rnatilgan Bash ning to'liq versiyasini (masalan, 5.2.15) saqlaydi. Ko'p platformali skriptlarda versiyaga mos funksiyalarni tanlashda qo'llaniladi.

## Ishlash natijasi:
```text
Qobiq: /bin/bash
Bash versiyasi: 5.2.15(1)-release
```


# 49-Topshiriq: Skriptda ko'p qatorli sharhlar yozish
## Topshiriq sharti:
Here-doc yordamida ko'p qatorli sharh (block comment) yaratish usulini qo'llang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

: << 'SHARH_TAMOMI'
Ushbu bo'lim loyiha hujjatlashuvi uchun mo'ljallangan.
Interpretator ushbu qatorlarni bajarmay tashlab o'tadi.
SHARH_TAMOMI

echo "Skript sharhlardan so'ng davom etmoqda."
```

## Tushuntirish va Mantiq:
Bash-da bir qatorli sharh '#' bilan boshlanadi. Ko'p qatorli sharhlar uchun esa ': << 'BELGI' ... BELGI' Here-doc konstruksiyasi qo'llaniladi, bu yerda ':' bo'sh buyruq (no-op) hisoblanadi.

## Ishlash natijasi:
```text
Skript sharhlardan so'ng davom etmoqda.
```


# 50-Topshiriq: Tashqi kutubxona skriptini yuklash ('source' va '.')
## Topshiriq sharti:
Yordamchi skriptdagi funksiya va o'zgaruvchilarni asosiy dasturga import qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/helper_lib.sh
say_greeting() {
    echo "Khorazmiy AI kutubxonasidan salom!"
}
EOF

source /tmp/helper_lib.sh
say_greeting
```

## Tushuntirish va Mantiq:
'source fayl' yoki '. fayl' buyrug'i ko'rsatilgan faylni alohida jarayon ochmasdan, to'g'ridan-to'g'ri joriy shell muhitida bajaradi. Natijada undagi barcha funksiyalar va o'zgaruvchilar joriy skriptga qo'shiladi.

## Ishlash natijasi:
```text
Khorazmiy AI kutubxonasidan salom!
```

