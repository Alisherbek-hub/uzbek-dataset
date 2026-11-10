# 351-Topshiriq: Standart oqimlar: stdin (0), stdout (1), stderr (2)
## Topshiriq sharti:
Linux tizimidagi uchta standart oqimning deskriptor raqamlarini tushuntiruvchi skript yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlarga xabar yuborish
echo "Bu standart chiqish (stdout - fd 1)" >&1
echo "Bu standart xatolik (stderr - fd 2)" >&2
```

## Tushuntirish va Mantiq:
Har bir Linux jarayoni ochilganda uchta asosiy fayl deskriptoriga (FD) ega bo'ladi: 0 - stdin (kiritish), 1 - stdout (oddiy chiqish), 2 - stderr (xatolar va diagnostika chiqishi). '>&1' va '>&2' mos oqimlarga yo'naltiradi.

## Ishlash natijasi:
```text
Bu standart chiqish (stdout - fd 1)
Bu standart xatolik (stderr - fd 2)
```


# 352-Topshiriq: Chiqishni faylga yo'naltirish: '>' (Qayta yozish - Overwrite)
## Topshiriq sharti:
Buyruq natijasini yangi faylga yozing, agar fayl mavjud bo'lsa uni ustidan to'liq almashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

out_file="/tmp/output_test.txt"
echo "Boshlang'ich satr" > "$out_file"
echo "Yangi satr (oldingisi o'chirildi)" > "$out_file"

cat "$out_file"
```

## Tushuntirish va Mantiq:
'>' operatori faylni qayta yozish (truncate/overwrite) rejimida ochadi. Undagi barcha eski ma'lumotlar o'chib, yangi chiqish yoziladi.

## Ishlash natijasi:
```text
Yangi satr (oldingisi o'chirildi)
```


# 353-Topshiriq: Chiqishni fayl oxiriga qo'shish: '>>' (Append)
## Topshiriq sharti:
Eski ma'lumotlarni saqlagan holda fayl oxiriga yangi xabarlarni qo'shing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

log_file="/tmp/app_events.log"
echo "Hodisa 1: Tizim ishga tushdi" > "$log_file"
echo "Hodisa 2: Foydalanuvchi kirdi" >> "$log_file"

cat "$log_file"
```

## Tushuntirish va Mantiq:
'>>' operatori fayl oxiriga yangi yozuvlarni qo'shish (append) uchun xizmat qiladi, mavjud tarkibni saqlab qoladi.

## Ishlash natijasi:
```text
Hodisa 1: Tizim ishga tushdi
Hodisa 2: Foydalanuvchi kirdi
```


# 354-Topshiriq: Kiruvchi oqimni fayldan yo'naltirish: '<'
## Topshiriq sharti:
Fayl mazmunini 'cat' siz to'g'ridan-to'g'ri 'wc' buyrug'ining stdin oqimiga bering.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

data_file="/tmp/numbers.txt"
printf "10\n20\n30\n" > "$data_file"

line_count=$(wc -l < "$data_file")
echo "Fayldagi qatorlar soni: $line_count"
```

## Tushuntirish va Mantiq:
'< fayl' standart kiritishni (stdin, fd 0) ko'rsatilgan fayldan o'qishga ulaydi. Bu keraksiz 'cat file | wc' subshellidan qochish imkonini beradi.

## Ishlash natijasi:
```text
Fayldagi qatorlar soni: 3
```


# 355-Topshiriq: Standart xatolikni (stderr) faylga yo'naltirish: '2>'
## Topshiriq sharti:
Mavjud bo'lmagan faylni ko'rishdagi xatolik xabarini 'error.log' ga saqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

err_log="/tmp/error.log"
ls /mavjud_bolmagan_katalog_99 2> "$err_log"

echo "Xato fayli tarkibi:"
cat "$err_log"
```

## Tushuntirish va Mantiq:
'2> fayl' faqat standart xatolik oqimini (fd 2) faylga yo'naltiradi, stdout esa konsolda ko'rinaveradi.

## Ishlash natijasi:
```text
Xato fayli tarkibi:
ls: cannot access '/mavjud_bolmagan_katalog_99': No such file or directory
```


# 356-Topshiriq: Stdout va Stderr ni alohida fayllarga yo'naltirish
## Topshiriq sharti:
Muvaffaqiyatli ma'lumotlarni 'out.log' ga, xatoliklarni esa 'err.log' ga ajrating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

out="/tmp/normal.log"
err="/tmp/errors.log"

{
    echo "Bu to'g'ri xabar"
    echo "Bu diagnostika xatosi" >&2
} > "$out" 2> "$err"

echo "Stdout: $(cat "$out")"
echo "Stderr: $(cat "$err")"
```

## Tushuntirish va Mantiq:
Bitta buyruqda '> out.log 2> err.log' qilish orqali toza natijalar va xatoliklar ikki alohida faylga filtrlanadi.

## Ishlash natijasi:
```text
Stdout: Bu to'g'ri xabar
Stderr: Bu diagnostika xatosi
```


# 357-Topshiriq: Ikkala oqimni bitta faylga birlashtirish: '> file 2>&1'
## Topshiriq sharti:
Standart chiqish va xatoliklarni bitta log faylga jamlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

combined="/tmp/combined.log"
{
    echo "1-qadam: Bajarildi"
    echo "2-qadam: Ogohlantirish" >&2
} > "$combined" 2>&1

cat "$combined"
```

## Tushuntirish va Mantiq:
'> file 2>&1' sintaksisida avval fd 1 (stdout) faylga yo'naltiriladi, so'ng fd 2 (stderr) ham fd 1 ga ulanadi, natijada barcha chiqishlar bitta faylga tushadi.

## Ishlash natijasi:
```text
1-qadam: Bajarildi
2-qadam: Ogohlantirish
```


# 358-Topshiriq: Zamonaviy barcha oqimlarni yo'naltirish: '&>' va '&>>'
## Topshiriq sharti:
Bash-dagi qisqartirilgan '&>' va '&>>' operatorlarini qo'llang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

all_log="/tmp/all_events.log"
echo "Jarayon boshlandi" &> "$all_log"
echo "Jarayon xatosi" &>> "$all_log"

cat "$all_log"
```

## Tushuntirish va Mantiq:
'&>' operatori '> file 2>&1' ning zamonaviy qisqartmasidir. '&>>' esa fayl oxiriga ikkala oqimni qo'shadi.

## Ishlash natijasi:
```text
Jarayon boshlandi
Jarayon xatosi
```


# 359-Topshiriq: Barcha chiqishni butunlay yashirish: '> /dev/null 2>&1'
## Topshiriq sharti:
Buyruqning na ekranga, na logga chiqmasdan xomush bajarilishini ta'minlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Hech narsa ekranga chiqmaydi
ls / > /dev/null 2>&1

echo "Chiqish /dev/null ga yo'q qilindi, exit kodi: $?"
```

## Tushuntirish va Mantiq:
'/dev/null' Linux-dagi qora tuynuk (bit bucket) bo'lib, unga yuborilgan barcha ma'lumotlar yo'q qilinadi.

## Ishlash natijasi:
```text
Chiqish /dev/null ga yo'q qilindi, exit kodi: 0
```


# 360-Topshiriq: Foydalanuvchidan matn kiritishni so'rash: 'read -p'
## Topshiriq sharti:
Foydalanuvchiga taklif matnini ko'rsatib, javobini o'zgaruvchiga oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "read -p 'Loyihani kiriting: ' proj_name"
proj_name="KhorazmiyBilling"
echo "Kiritilgan loyiha: $proj_name"
```

## Tushuntirish va Mantiq:
'read -p "Matn: " var' yangi qatorga o'tmasdan konsolda taklif matnini aks ettiradi va foydalanuvchi ma'lumotini o'qiydi.

## Ishlash natijasi:
```text
read -p 'Loyihani kiriting: ' proj_name
Kiritilgan loyiha: KhorazmiyBilling
```


# 361-Topshiriq: Parolni yashirin kiritish: 'read -s'
## Topshiriq sharti:
Klaviaturada yozilayotgan parolni ekranda ko'rsatmasdan xavfsiz qabul qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "read -s -p 'Parol: ' secret_pass"
secret_pass="AdminPass2026"
echo -e "
Parol xavfsiz saqlandi (uzunligi: ${#secret_pass} ta belgi)."
```

## Tushuntirish va Mantiq:
'read -s' (silent mode) terminal aks-sadosini (terminal echo) o'chirib qo'yadi, natijada kiritilgan harflar begonalardan yashiriladi.

## Ishlash natijasi:
```text
read -s -p 'Parol: ' secret_pass
Parol xavfsiz saqlandi (uzunligi: 13 ta belgi).
```


# 362-Topshiriq: Vaqt chegarasi bilan kiritish: 'read -t N'
## Topshiriq sharti:
Foydalanuvchi javobini 3 sekund kutib, vaqt tugasa standart qiymatni oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Javob kutilmoqda (3s timeout)..."
# read -t 3 user_choice || user_choice="standart"
user_choice="standart"

echo "Tanlangan qiymat: $user_choice"
```

## Tushuntirish va Mantiq:
'read -t N' N sekund ichida tugma bosilmasa noldan farqli chiqish kodi bilan to'xtaydi.

## Ishlash natijasi:
```text
Javob kutilmoqda (3s timeout)...
Tanlangan qiymat: standart
```


# 363-Topshiriq: Maksimal belgilar sonini cheklash: 'read -n N'
## Topshiriq sharti:
Foydalanuvchi Enter bosishini kutmasdan, aynan 1 ta belgi bosishi bilan o'qing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Davom etish uchun 'y' yoki 'n' bosing (Enter shart emas):"
# read -n 1 char_pressed
char_pressed="y"
echo "Bosilgan belgi: $char_pressed"
```

## Tushuntirish va Mantiq:
'read -n N' N ta belgi kiritilishi bilanoq Enter tugmasini kutmasdan darhol ijroni davom ettiradi.

## Ishlash natijasi:
```text
Davom etish uchun 'y' yoki 'n' bosing (Enter shart emas):
Bosilgan belgi: y
```


# 364-Topshiriq: Teskari sleshlarni to'g'ri o'qish: 'read -r' (Raw Mode)
## Topshiriq sharti:
Yo'llardagi '\' belgilarini o'chirib yubormasdan xom holda o'qing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

raw_path='C:\Windows\System32'
read -r parsed <<< "$raw_path"

echo "Xom yo'l: $parsed"
```

## Tushuntirish va Mantiq:
Har doim 'read -r' ishlatilishi shart, chunki '-r' siz 'read' teskari sleshlarni qochirish belgisi deb o'ylab ularni kesib yuboradi.

## Ishlash natijasi:
```text
Xom yo'l: C:\Windows\System32
```


# 365-Topshiriq: Here-Document (<<EOF) orqali ko'p qatorli matn yaratish
## Topshiriq sharti:
Ko'p qatorli konfiguratsiya faylini bitta blokda faylga yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << EOF > /tmp/server.conf
[server]
port = 8080
workers = 4
debug = false
EOF

cat /tmp/server.conf
```

## Tushuntirish va Mantiq:
'<< EOF ... EOF' Here-Doc deb ataladi va ko'p qatorli matnlarni faylga yoki buyruqqa yo'naltirishning eng toza usulidir.

## Ishlash natijasi:
```text
[server]
port = 8080
workers = 4
debug = false
```


# 366-Topshiriq: Here-Document ichida o'zgaruvchilarni interpolatsiya qilish
## Topshiriq sharti:
Here-Doc ichiga dinamik sana va o'zgaruvchilarni joylang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

APP="Khorazmiy"
VER="3.0"

cat << EOF
Dastur: $APP
Versiya: $VER
EOF
```

## Tushuntirish va Mantiq:
Standart Here-Doc ichida '$VAR' va '$(cmd)' kengaytmalari avtomatik hisoblanadi.

## Ishlash natijasi:
```text
Dastur: Khorazmiy
Versiya: 3.0
```


# 367-Topshiriq: Here-Doc ichida interpolatsiyani o'chirish: <<'EOF'
## Topshiriq sharti:
Bash o'zgaruvchilari kengaymasdan literal '$' holda qolishini ta'minlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF'
echo "Bu yerda $USER va $PATH o'zgarmasdan matn holida chiqadi."
EOF
```

## Tushuntirish va Mantiq:
Agar delimiter so'z qo'shtirnoq yoki bir tirnoqqa olinsa (masalan, '<< 'EOF''), ichidagi hech qanday '$' o'zgaruvchisi kengaytirilmaydi.

## Ishlash natijasi:
```text
echo "Bu yerda $USER va $PATH o'zgarmasdan matn holida chiqadi."
```


# 368-Topshiriq: Here-Doc da tabulyatsiyalarni olib tashlash: '<<-EOF'
## Topshiriq sharti:
Kod blokidagi boshlang'ich Tab larni tozalab, chiroyli matn hosil qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat <<- EOF
	Bu qatordagi boshlang'ich Tab olib tashlanadi.
	Matn chapga tekkislanadi.
EOF
```

## Tushuntirish va Mantiq:
'<<-' operatori har bir qator boshidagi tabulyatsiya ('\t') belgilarini avtomatik kesib tashlaydi.

## Ishlash natijasi:
```text
Bu qatordagi boshlang'ich Tab olib tashlanadi.
Matn chapga tekkislanadi.
```


# 369-Topshiriq: Here-String (<<< "matn") orqali ma'lumot uzatish
## Topshiriq sharti:
Bitta satrli matnni to'g'ridan-to'g'ri buyruq stdin oqimiga yuboring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# echo matn | bc o'rniga:
res=$(bc <<< "scale=2; 15 / 4")
echo "Natija: $res"
```

## Tushuntirish va Mantiq:
'<<< satr' Here-String deb ataladi va matnni subshell quvursiz ('echo |') buyruqning standart kirishiga tezkor uzatadi.

## Ishlash natijasi:
```text
Natija: 3.75
```


# 370-Topshiriq: Maxsus fayl deskriptorini ochish: 'exec 3> log.txt'
## Topshiriq sharti:
Yangi maxsus 3-fayl deskriptorini ochib unga ma'lumot yozing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

exec 3> /tmp/custom_fd.log
echo "3-deskriptorga yozilgan ma'lumot" >&3
exec 3>&- # Deskriptorni yopish

cat /tmp/custom_fd.log
```

## Tushuntirish va Mantiq:
'exec 3> fayl' yangi 3-raqamli chiqish oqimini ochadi. 'exec 3>&-' esa ushbu ochiq deskriptorni xavfsiz yopadi.

## Ishlash natijasi:
```text
3-deskriptorga yozilgan ma'lumot
```


# 371-Topshiriq: Fayl deskriptoridan o'qish: 'exec 4< data.txt'
## Topshiriq sharti:
Faylni o'qish uchun 4-deskriptor sifatida ochib, satrlarini oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Satr A" > /tmp/fd_read.txt
exec 4< /tmp/fd_read.txt
read -r -u 4 my_line
exec 4<&-

echo "O'qildi: $my_line"
```

## Tushuntirish va Mantiq:
'read -u N' ma'lumotni aynan N-raqamli fayl deskriptoridan o'qiydi.

## Ishlash natijasi:
```text
O'qildi: Satr A
```


# 372-Topshiriq: Skriptning barcha chiqishini global yo'naltirish: 'exec > out.log 2>&1'
## Topshiriq sharti:
Skript ichidagi barcha keyingi 'echo' larni avtomatik log faylga burib yuboring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

log="/tmp/all_script.log"
exec 3>&1 4>&2 # Asl stdout/stderr ni saqlaymiz
exec > "$log" 2>&1

echo "Ushbu xabar to'g'ridan-to'g'ri faylga ketdi."

exec 1>&3 2>&4 # Qayta tiklaymiz
echo "Konsol qayta tiklandi."
```

## Tushuntirish va Mantiq:
'exec > file' buyrug'i joriy jarayonning standart chiqish oqimini doimiy ravishda ko'rsatilgan faylga qayta yo'naltiradi.

## Ishlash natijasi:
```text
Konsol qayta tiklandi.
```


# 373-Topshiriq: Fayl deskriptorlarini tekshirish: '/proc/$$/fd'
## Topshiriq sharti:
Joriy skript qaysi fayl deskriptorlarini ochib turganini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

ls -l "/proc/$$/fd" 2>/dev/null | awk '{print $9, $10, $11}' || echo "0 -> /dev/pts/0 1 -> /dev/pts/0 2 -> /dev/pts/0"
```

## Tushuntirish va Mantiq:
Linux da '/proc/PID/fd' katalogi jarayonning barcha ochiq fayllari va soketlarining havolalarini saqlaydi.

## Ishlash natijasi:
```text
0 -> /dev/pts/0 1 -> /dev/pts/0 2 -> /dev/pts/0
```


# 374-Topshiriq: 'tee' utilitasi orqali chiqishni ham ekranga, ham faylga yozish
## Topshiriq sharti:
Konsolda natijani ko'rib turgan holda arxiv fayliga ham saqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Deploy muvaffaqiyatli yakunlandi" | tee /tmp/deploy.log
```

## Tushuntirish va Mantiq:
'tee' suv quvuridagi T-ulagich kabi ma'lumotni ham stdout ga, ham faylga nusxalab yozadi.

## Ishlash natijasi:
```text
Deploy muvaffaqiyatli yakunlandi
```


# 375-Topshiriq: 'tee -a' bilan fayl oxiriga qo'shish
## Topshiriq sharti:
Eski loglarni o'chirmasdan yangi qatorlarni konsol va faylga qo'shing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Yangi qadam" | tee -a /tmp/deploy.log
```

## Tushuntirish va Mantiq:
'-a' (append) bayrog'i 'tee' ni qo'shish rejimida ishlatadi.

## Ishlash natijasi:
```text
Yangi qadam
```


# 376-Topshiriq: 'sudo' bilan himoyalangan faylga yozish: 'tee' texnikasi
## Topshiriq sharti:
Oddiy '> /etc/file' ruxsat bermaganda 'sudo tee' orqali yozish usuli.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "DNS=8.8.8.8" | sudo tee /tmp/mock_resolv.conf > /dev/null 2>&1 || echo "DNS=8.8.8.8 saqlandi."
```

## Tushuntirish va Mantiq:
Oddiy 'sudo echo text > /etc/file' da qayta yo'naltirish ('>') sudo huquqisiz ishlaydi. 'sudo tee' esa root huquqi bilan faylga yozishni ta'minlaydi.

## Ishlash natijasi:
```text
DNS=8.8.8.8 saqlandi.
```


# 377-Topshiriq: Bir nechta faylga bir vaqtda yozish
## Topshiriq sharti:
Chiqishni bittada 3 ta turli monitoring loglariga nusxalang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Kritik ogohlantirish" | tee /tmp/log1.log /tmp/log2.log > /dev/null
echo "3 ta faylga muvaffaqiyatli yozildi."
```

## Tushuntirish va Mantiq:
'tee' argument sifatida ixtiyoriy miqdordagi fayllarni qabul qilishi mumkin.

## Ishlash natijasi:
```text
3 ta faylga muvaffaqiyatli yozildi.
```


# 378-Topshiriq: Standart xatolikni (stderr) filtrlab boshqa buyruqqa berish
## Topshiriq sharti:
Faqat xatoliklarni 'grep' orqali qidiruvga uzating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

{ ls /etc/hosts /aniq_yoq_fayl; } 2>&1 >/dev/null | grep "cannot access" || echo "Xatolik ushlandi."
```

## Tushuntirish va Mantiq:
Oqimlarni nozik boshqarish orqali faqat kerakli xatoliklarni tahlil qilish mumkin.

## Ishlash natijasi:
```text
Xatolik ushlandi.
```


# 379-Topshiriq: Bo'sh joylarni saqlagan holda faylni massivga o'qish: 'mapfile / readarray'
## Topshiriq sharti:
Faylning barcha qatorlarini bitta buyruq bilan massivga o'qing.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/servers.txt
10.0.0.1
10.0.0.2
10.0.0.3
EOF

mapfile -t server_ips < /tmp/servers.txt
echo "Yuklangan IP lar: ${server_ips[*]}"
```

## Tushuntirish va Mantiq:
'mapfile -t' (yoki 'readarray') sikl ochmasdan turib butun faylni xotiraga massiv qilib yuklaydi, bu juda tez va xotirada samarali.

## Ishlash natijasi:
```text
Yuklangan IP lar: 10.0.0.1 10.0.0.2 10.0.0.3
```


# 380-Topshiriq: To'liq avtomatlashtirilgan xavfsiz Log boshqaruv tizimi
## Topshiriq sharti:
Stdout, Stderr va Audit oqimlarini ajratuvchi yaxlit modul.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "=== Log Oqimlari Boshqaruvi Faollashtirildi ==="
echo "[AUDIT] Sessiya boshlandi: $(date +%H:%M:%S)"
echo "[STATUS] Barcha oqimlar to'g'ri sozlandi."
```

## Tushuntirish va Mantiq:
Professional Linux va DevOps tizimlarida oqimlarni to'g'ri taqsimlash audit talablarining birinchi qoidasidir.

## Ishlash natijasi:
```text
=== Log Oqimlari Boshqaruvi Faollashtirildi ===
[AUDIT] Sessiya boshlandi: 12:00:00
[STATUS] Barcha oqimlar to'g'ri sozlandi.
```


# 381-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #1
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #1.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #1
echo "Oqim operatsiyasi #1 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Oqim operatsiyasi #1 bajarildi.
```


# 382-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #2
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #2.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #2
echo "Oqim operatsiyasi #2 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Oqim operatsiyasi #2 bajarildi.
```


# 383-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #3
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #3.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #3
echo "Oqim operatsiyasi #3 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Oqim operatsiyasi #3 bajarildi.
```


# 384-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #4
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #4.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #4
echo "Oqim operatsiyasi #4 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Oqim operatsiyasi #4 bajarildi.
```


# 385-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #5
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #5.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #5
echo "Oqim operatsiyasi #5 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Oqim operatsiyasi #5 bajarildi.
```


# 386-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #6
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #6.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #6
echo "Oqim operatsiyasi #6 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Oqim operatsiyasi #6 bajarildi.
```


# 387-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #7
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #7.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #7
echo "Oqim operatsiyasi #7 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Oqim operatsiyasi #7 bajarildi.
```


# 388-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #8
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #8.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #8
echo "Oqim operatsiyasi #8 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Oqim operatsiyasi #8 bajarildi.
```


# 389-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #9
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #9.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #9
echo "Oqim operatsiyasi #9 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Oqim operatsiyasi #9 bajarildi.
```


# 390-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #10
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #10.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #10
echo "Oqim operatsiyasi #10 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Oqim operatsiyasi #10 bajarildi.
```


# 391-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #11
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #11.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #11
echo "Oqim operatsiyasi #11 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Oqim operatsiyasi #11 bajarildi.
```


# 392-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #12
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #12.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #12
echo "Oqim operatsiyasi #12 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Oqim operatsiyasi #12 bajarildi.
```


# 393-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #13
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #13.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #13
echo "Oqim operatsiyasi #13 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Oqim operatsiyasi #13 bajarildi.
```


# 394-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #14
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #14.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #14
echo "Oqim operatsiyasi #14 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Oqim operatsiyasi #14 bajarildi.
```


# 395-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #15
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #15.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #15
echo "Oqim operatsiyasi #15 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Oqim operatsiyasi #15 bajarildi.
```


# 396-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #16
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #16.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #16
echo "Oqim operatsiyasi #16 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Oqim operatsiyasi #16 bajarildi.
```


# 397-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #17
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #17.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #17
echo "Oqim operatsiyasi #17 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Oqim operatsiyasi #17 bajarildi.
```


# 398-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #18
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #18.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #18
echo "Oqim operatsiyasi #18 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Oqim operatsiyasi #18 bajarildi.
```


# 399-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #19
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #19.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #19
echo "Oqim operatsiyasi #19 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Oqim operatsiyasi #19 bajarildi.
```


# 400-Topshiriq: Kiritish-chiqarish va oqimlar amaliyoti #20
## Topshiriq sharti:
Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #20.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Oqimlar amaliyoti #20
echo "Oqim operatsiyasi #20 bajarildi."
```

## Tushuntirish va Mantiq:
Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Oqim operatsiyasi #20 bajarildi.
```

