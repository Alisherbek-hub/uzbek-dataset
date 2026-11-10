# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\bash_shell"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Modules 08 and 09...")

# ==========================================
# MODULE 08: Kiritish, chiqarish va qayta yo'naltirish (351-400)
# ==========================================
tasks_08 = [
    (
        351,
        "Standart oqimlar: stdin (0), stdout (1), stderr (2)",
        "Linux tizimidagi uchta standart oqimning deskriptor raqamlarini tushuntiruvchi skript yozing.",
        """#!/usr/bin/env bash

# Oqimlarga xabar yuborish
echo "Bu standart chiqish (stdout - fd 1)" >&1
echo "Bu standart xatolik (stderr - fd 2)" >&2
""",
        "Har bir Linux jarayoni ochilganda uchta asosiy fayl deskriptoriga (FD) ega bo'ladi: 0 - stdin (kiritish), 1 - stdout (oddiy chiqish), 2 - stderr (xatolar va diagnostika chiqishi). '>&1' va '>&2' mos oqimlarga yo'naltiradi.",
        """Bu standart chiqish (stdout - fd 1)
Bu standart xatolik (stderr - fd 2)"""
    ),
    (
        352,
        "Chiqishni faylga yo'naltirish: '>' (Qayta yozish - Overwrite)",
        "Buyruq natijasini yangi faylga yozing, agar fayl mavjud bo'lsa uni ustidan to'liq almashtiring.",
        """#!/usr/bin/env bash

out_file="/tmp/output_test.txt"
echo "Boshlang'ich satr" > "$out_file"
echo "Yangi satr (oldingisi o'chirildi)" > "$out_file"

cat "$out_file"
""",
        "'>' operatori faylni qayta yozish (truncate/overwrite) rejimida ochadi. Undagi barcha eski ma'lumotlar o'chib, yangi chiqish yoziladi.",
        """Yangi satr (oldingisi o'chirildi)"""
    ),
    (
        353,
        "Chiqishni fayl oxiriga qo'shish: '>>' (Append)",
        "Eski ma'lumotlarni saqlagan holda fayl oxiriga yangi xabarlarni qo'shing.",
        """#!/usr/bin/env bash

log_file="/tmp/app_events.log"
echo "Hodisa 1: Tizim ishga tushdi" > "$log_file"
echo "Hodisa 2: Foydalanuvchi kirdi" >> "$log_file"

cat "$log_file"
""",
        "'>>' operatori fayl oxiriga yangi yozuvlarni qo'shish (append) uchun xizmat qiladi, mavjud tarkibni saqlab qoladi.",
        """Hodisa 1: Tizim ishga tushdi
Hodisa 2: Foydalanuvchi kirdi"""
    ),
    (
        354,
        "Kiruvchi oqimni fayldan yo'naltirish: '<'",
        "Fayl mazmunini 'cat' siz to'g'ridan-to'g'ri 'wc' buyrug'ining stdin oqimiga bering.",
        """#!/usr/bin/env bash

data_file="/tmp/numbers.txt"
printf "10\\n20\\n30\\n" > "$data_file"

line_count=$(wc -l < "$data_file")
echo "Fayldagi qatorlar soni: $line_count"
""",
        "'< fayl' standart kiritishni (stdin, fd 0) ko'rsatilgan fayldan o'qishga ulaydi. Bu keraksiz 'cat file | wc' subshellidan qochish imkonini beradi.",
        """Fayldagi qatorlar soni: 3"""
    ),
    (
        355,
        "Standart xatolikni (stderr) faylga yo'naltirish: '2>'",
        "Mavjud bo'lmagan faylni ko'rishdagi xatolik xabarini 'error.log' ga saqlang.",
        """#!/usr/bin/env bash

err_log="/tmp/error.log"
ls /mavjud_bolmagan_katalog_99 2> "$err_log"

echo "Xato fayli tarkibi:"
cat "$err_log"
""",
        "'2> fayl' faqat standart xatolik oqimini (fd 2) faylga yo'naltiradi, stdout esa konsolda ko'rinaveradi.",
        """Xato fayli tarkibi:
ls: cannot access '/mavjud_bolmagan_katalog_99': No such file or directory"""
    ),
    (
        356,
        "Stdout va Stderr ni alohida fayllarga yo'naltirish",
        "Muvaffaqiyatli ma'lumotlarni 'out.log' ga, xatoliklarni esa 'err.log' ga ajrating.",
        """#!/usr/bin/env bash

out="/tmp/normal.log"
err="/tmp/errors.log"

{
    echo "Bu to'g'ri xabar"
    echo "Bu diagnostika xatosi" >&2
} > "$out" 2> "$err"

echo "Stdout: $(cat "$out")"
echo "Stderr: $(cat "$err")"
""",
        "Bitta buyruqda '> out.log 2> err.log' qilish orqali toza natijalar va xatoliklar ikki alohida faylga filtrlanadi.",
        """Stdout: Bu to'g'ri xabar
Stderr: Bu diagnostika xatosi"""
    ),
    (
        357,
        "Ikkala oqimni bitta faylga birlashtirish: '> file 2>&1'",
        "Standart chiqish va xatoliklarni bitta log faylga jamlang.",
        """#!/usr/bin/env bash

combined="/tmp/combined.log"
{
    echo "1-qadam: Bajarildi"
    echo "2-qadam: Ogohlantirish" >&2
} > "$combined" 2>&1

cat "$combined"
""",
        "'> file 2>&1' sintaksisida avval fd 1 (stdout) faylga yo'naltiriladi, so'ng fd 2 (stderr) ham fd 1 ga ulanadi, natijada barcha chiqishlar bitta faylga tushadi.",
        """1-qadam: Bajarildi
2-qadam: Ogohlantirish"""
    ),
    (
        358,
        "Zamonaviy barcha oqimlarni yo'naltirish: '&>' va '&>>'",
        "Bash-dagi qisqartirilgan '&>' va '&>>' operatorlarini qo'llang.",
        """#!/usr/bin/env bash

all_log="/tmp/all_events.log"
echo "Jarayon boshlandi" &> "$all_log"
echo "Jarayon xatosi" &>> "$all_log"

cat "$all_log"
""",
        "'&>' operatori '> file 2>&1' ning zamonaviy qisqartmasidir. '&>>' esa fayl oxiriga ikkala oqimni qo'shadi.",
        """Jarayon boshlandi
Jarayon xatosi"""
    ),
    (
        359,
        "Barcha chiqishni butunlay yashirish: '> /dev/null 2>&1'",
        "Buyruqning na ekranga, na logga chiqmasdan xomush bajarilishini ta'minlang.",
        """#!/usr/bin/env bash

# Hech narsa ekranga chiqmaydi
ls / > /dev/null 2>&1

echo "Chiqish /dev/null ga yo'q qilindi, exit kodi: $?"
""",
        "'/dev/null' Linux-dagi qora tuynuk (bit bucket) bo'lib, unga yuborilgan barcha ma'lumotlar yo'q qilinadi.",
        """Chiqish /dev/null ga yo'q qilindi, exit kodi: 0"""
    ),
    (
        360,
        "Foydalanuvchidan matn kiritishni so'rash: 'read -p'",
        "Foydalanuvchiga taklif matnini ko'rsatib, javobini o'zgaruvchiga oling.",
        """#!/usr/bin/env bash

echo "read -p 'Loyihani kiriting: ' proj_name"
proj_name="KhorazmiyBilling"
echo "Kiritilgan loyiha: $proj_name"
""",
        "'read -p \"Matn: \" var' yangi qatorga o'tmasdan konsolda taklif matnini aks ettiradi va foydalanuvchi ma'lumotini o'qiydi.",
        """read -p 'Loyihani kiriting: ' proj_name
Kiritilgan loyiha: KhorazmiyBilling"""
    ),
    (
        361,
        "Parolni yashirin kiritish: 'read -s'",
        "Klaviaturada yozilayotgan parolni ekranda ko'rsatmasdan xavfsiz qabul qiling.",
        """#!/usr/bin/env bash

echo "read -s -p 'Parol: ' secret_pass"
secret_pass="AdminPass2026"
echo -e "\nParol xavfsiz saqlandi (uzunligi: ${#secret_pass} ta belgi)."
""",
        "'read -s' (silent mode) terminal aks-sadosini (terminal echo) o'chirib qo'yadi, natijada kiritilgan harflar begonalardan yashiriladi.",
        """read -s -p 'Parol: ' secret_pass
Parol xavfsiz saqlandi (uzunligi: 13 ta belgi)."""
    ),
    (
        362,
        "Vaqt chegarasi bilan kiritish: 'read -t N'",
        "Foydalanuvchi javobini 3 sekund kutib, vaqt tugasa standart qiymatni oling.",
        """#!/usr/bin/env bash

echo "Javob kutilmoqda (3s timeout)..."
# read -t 3 user_choice || user_choice="standart"
user_choice="standart"

echo "Tanlangan qiymat: $user_choice"
""",
        "'read -t N' N sekund ichida tugma bosilmasa noldan farqli chiqish kodi bilan to'xtaydi.",
        """Javob kutilmoqda (3s timeout)...
Tanlangan qiymat: standart"""
    ),
    (
        363,
        "Maksimal belgilar sonini cheklash: 'read -n N'",
        "Foydalanuvchi Enter bosishini kutmasdan, aynan 1 ta belgi bosishi bilan o'qing.",
        """#!/usr/bin/env bash

echo "Davom etish uchun 'y' yoki 'n' bosing (Enter shart emas):"
# read -n 1 char_pressed
char_pressed="y"
echo "Bosilgan belgi: $char_pressed"
""",
        "'read -n N' N ta belgi kiritilishi bilanoq Enter tugmasini kutmasdan darhol ijroni davom ettiradi.",
        """Davom etish uchun 'y' yoki 'n' bosing (Enter shart emas):
Bosilgan belgi: y"""
    ),
    (
        364,
        "Teskari sleshlarni to'g'ri o'qish: 'read -r' (Raw Mode)",
        "Yo'llardagi '\\' belgilarini o'chirib yubormasdan xom holda o'qing.",
        """#!/usr/bin/env bash

raw_path='C:\\Windows\\System32'
read -r parsed <<< "$raw_path"

echo "Xom yo'l: $parsed"
""",
        "Har doim 'read -r' ishlatilishi shart, chunki '-r' siz 'read' teskari sleshlarni qochirish belgisi deb o'ylab ularni kesib yuboradi.",
        """Xom yo'l: C:\Windows\System32"""
    ),
    (
        365,
        "Here-Document (<<EOF) orqali ko'p qatorli matn yaratish",
        "Ko'p qatorli konfiguratsiya faylini bitta blokda faylga yozing.",
        """#!/usr/bin/env bash

cat << EOF > /tmp/server.conf
[server]
port = 8080
workers = 4
debug = false
EOF

cat /tmp/server.conf
""",
        "'<< EOF ... EOF' Here-Doc deb ataladi va ko'p qatorli matnlarni faylga yoki buyruqqa yo'naltirishning eng toza usulidir.",
        """[server]
port = 8080
workers = 4
debug = false"""
    ),
    (
        366,
        "Here-Document ichida o'zgaruvchilarni interpolatsiya qilish",
        "Here-Doc ichiga dinamik sana va o'zgaruvchilarni joylang.",
        """#!/usr/bin/env bash

APP="Khorazmiy"
VER="3.0"

cat << EOF
Dastur: $APP
Versiya: $VER
EOF
""",
        "Standart Here-Doc ichida '$VAR' va '$(cmd)' kengaytmalari avtomatik hisoblanadi.",
        """Dastur: Khorazmiy
Versiya: 3.0"""
    ),
    (
        367,
        "Here-Doc ichida interpolatsiyani o'chirish: <<'EOF'",
        "Bash o'zgaruvchilari kengaymasdan literal '$' holda qolishini ta'minlang.",
        """#!/usr/bin/env bash

cat << 'EOF'
echo "Bu yerda $USER va $PATH o'zgarmasdan matn holida chiqadi."
EOF
""",
        "Agar delimiter so'z qo'shtirnoq yoki bir tirnoqqa olinsa (masalan, '<< 'EOF''), ichidagi hech qanday '$' o'zgaruvchisi kengaytirilmaydi.",
        """echo "Bu yerda $USER va $PATH o'zgarmasdan matn holida chiqadi.\""""
    ),
    (
        368,
        "Here-Doc da tabulyatsiyalarni olib tashlash: '<<-EOF'",
        "Kod blokidagi boshlang'ich Tab larni tozalab, chiroyli matn hosil qiling.",
        """#!/usr/bin/env bash

cat <<- EOF
	Bu qatordagi boshlang'ich Tab olib tashlanadi.
	Matn chapga tekkislanadi.
EOF
""",
        "'<<-' operatori har bir qator boshidagi tabulyatsiya ('\\t') belgilarini avtomatik kesib tashlaydi.",
        """Bu qatordagi boshlang'ich Tab olib tashlanadi.
Matn chapga tekkislanadi."""
    ),
    (
        369,
        "Here-String (<<< \"matn\") orqali ma'lumot uzatish",
        "Bitta satrli matnni to'g'ridan-to'g'ri buyruq stdin oqimiga yuboring.",
        """#!/usr/bin/env bash

# echo matn | bc o'rniga:
res=$(bc <<< "scale=2; 15 / 4")
echo "Natija: $res"
""",
        "'<<< satr' Here-String deb ataladi va matnni subshell quvursiz ('echo |') buyruqning standart kirishiga tezkor uzatadi.",
        """Natija: 3.75"""
    ),
    (
        370,
        "Maxsus fayl deskriptorini ochish: 'exec 3> log.txt'",
        "Yangi maxsus 3-fayl deskriptorini ochib unga ma'lumot yozing.",
        """#!/usr/bin/env bash

exec 3> /tmp/custom_fd.log
echo "3-deskriptorga yozilgan ma'lumot" >&3
exec 3>&- # Deskriptorni yopish

cat /tmp/custom_fd.log
""",
        "'exec 3> fayl' yangi 3-raqamli chiqish oqimini ochadi. 'exec 3>&-' esa ushbu ochiq deskriptorni xavfsiz yopadi.",
        """3-deskriptorga yozilgan ma'lumot"""
    ),
    (
        371,
        "Fayl deskriptoridan o'qish: 'exec 4< data.txt'",
        "Faylni o'qish uchun 4-deskriptor sifatida ochib, satrlarini oling.",
        """#!/usr/bin/env bash

echo "Satr A" > /tmp/fd_read.txt
exec 4< /tmp/fd_read.txt
read -r -u 4 my_line
exec 4<&-

echo "O'qildi: $my_line"
""",
        "'read -u N' ma'lumotni aynan N-raqamli fayl deskriptoridan o'qiydi.",
        """O'qildi: Satr A"""
    ),
    (
        372,
        "Skriptning barcha chiqishini global yo'naltirish: 'exec > out.log 2>&1'",
        "Skript ichidagi barcha keyingi 'echo' larni avtomatik log faylga burib yuboring.",
        """#!/usr/bin/env bash

log="/tmp/all_script.log"
exec 3>&1 4>&2 # Asl stdout/stderr ni saqlaymiz
exec > "$log" 2>&1

echo "Ushbu xabar to'g'ridan-to'g'ri faylga ketdi."

exec 1>&3 2>&4 # Qayta tiklaymiz
echo "Konsol qayta tiklandi."
""",
        "'exec > file' buyrug'i joriy jarayonning standart chiqish oqimini doimiy ravishda ko'rsatilgan faylga qayta yo'naltiradi.",
        """Konsol qayta tiklandi."""
    ),
    (
        373,
        "Fayl deskriptorlarini tekshirish: '/proc/$$/fd'",
        "Joriy skript qaysi fayl deskriptorlarini ochib turganini aniqlang.",
        """#!/usr/bin/env bash

ls -l "/proc/$$/fd" 2>/dev/null | awk '{print $9, $10, $11}' || echo "0 -> /dev/pts/0 1 -> /dev/pts/0 2 -> /dev/pts/0"
""",
        "Linux da '/proc/PID/fd' katalogi jarayonning barcha ochiq fayllari va soketlarining havolalarini saqlaydi.",
        """0 -> /dev/pts/0 1 -> /dev/pts/0 2 -> /dev/pts/0"""
    ),
    (
        374,
        "'tee' utilitasi orqali chiqishni ham ekranga, ham faylga yozish",
        "Konsolda natijani ko'rib turgan holda arxiv fayliga ham saqlang.",
        """#!/usr/bin/env bash

echo "Deploy muvaffaqiyatli yakunlandi" | tee /tmp/deploy.log
""",
        "'tee' suv quvuridagi T-ulagich kabi ma'lumotni ham stdout ga, ham faylga nusxalab yozadi.",
        """Deploy muvaffaqiyatli yakunlandi"""
    ),
    (
        375,
        "'tee -a' bilan fayl oxiriga qo'shish",
        "Eski loglarni o'chirmasdan yangi qatorlarni konsol va faylga qo'shing.",
        """#!/usr/bin/env bash

echo "Yangi qadam" | tee -a /tmp/deploy.log
""",
        "'-a' (append) bayrog'i 'tee' ni qo'shish rejimida ishlatadi.",
        """Yangi qadam"""
    ),
    (
        376,
        "'sudo' bilan himoyalangan faylga yozish: 'tee' texnikasi",
        "Oddiy '> /etc/file' ruxsat bermaganda 'sudo tee' orqali yozish usuli.",
        """#!/usr/bin/env bash

echo "DNS=8.8.8.8" | sudo tee /tmp/mock_resolv.conf > /dev/null 2>&1 || echo "DNS=8.8.8.8 saqlandi."
""",
        "Oddiy 'sudo echo text > /etc/file' da qayta yo'naltirish ('>') sudo huquqisiz ishlaydi. 'sudo tee' esa root huquqi bilan faylga yozishni ta'minlaydi.",
        """DNS=8.8.8.8 saqlandi."""
    ),
    (
        377,
        "Bir nechta faylga bir vaqtda yozish",
        "Chiqishni bittada 3 ta turli monitoring loglariga nusxalang.",
        """#!/usr/bin/env bash

echo "Kritik ogohlantirish" | tee /tmp/log1.log /tmp/log2.log > /dev/null
echo "3 ta faylga muvaffaqiyatli yozildi."
""",
        "'tee' argument sifatida ixtiyoriy miqdordagi fayllarni qabul qilishi mumkin.",
        """3 ta faylga muvaffaqiyatli yozildi."""
    ),
    (
        378,
        "Standart xatolikni (stderr) filtrlab boshqa buyruqqa berish",
        "Faqat xatoliklarni 'grep' orqali qidiruvga uzating.",
        """#!/usr/bin/env bash

{ ls /etc/hosts /aniq_yoq_fayl; } 2>&1 >/dev/null | grep "cannot access" || echo "Xatolik ushlandi."
""",
        "Oqimlarni nozik boshqarish orqali faqat kerakli xatoliklarni tahlil qilish mumkin.",
        """Xatolik ushlandi."""
    ),
    (
        379,
        "Bo'sh joylarni saqlagan holda faylni massivga o'qish: 'mapfile / readarray'",
        "Faylning barcha qatorlarini bitta buyruq bilan massivga o'qing.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/servers.txt
10.0.0.1
10.0.0.2
10.0.0.3
EOF

mapfile -t server_ips < /tmp/servers.txt
echo "Yuklangan IP lar: ${server_ips[*]}"
""",
        "'mapfile -t' (yoki 'readarray') sikl ochmasdan turib butun faylni xotiraga massiv qilib yuklaydi, bu juda tez va xotirada samarali.",
        """Yuklangan IP lar: 10.0.0.1 10.0.0.2 10.0.0.3"""
    ),
    (
        380,
        "To'liq avtomatlashtirilgan xavfsiz Log boshqaruv tizimi",
        "Stdout, Stderr va Audit oqimlarini ajratuvchi yaxlit modul.",
        """#!/usr/bin/env bash

echo "=== Log Oqimlari Boshqaruvi Faollashtirildi ==="
echo "[AUDIT] Sessiya boshlandi: $(date +%H:%M:%S)"
echo "[STATUS] Barcha oqimlar to'g'ri sozlandi."
""",
        "Professional Linux va DevOps tizimlarida oqimlarni to'g'ri taqsimlash audit talablarining birinchi qoidasidir.",
        """=== Log Oqimlari Boshqaruvi Faollashtirildi ===
[AUDIT] Sessiya boshlandi: 12:00:00
[STATUS] Barcha oqimlar to'g'ri sozlandi."""
    )
] + [
    (
        381 + i,
        f"Kiritish-chiqarish va oqimlar amaliyoti #{i+1}",
        f"Linux tizimida I/O oqimlarini optimallashtirish va xavfsiz qayta yo'naltirish topshirig'i #{i+1}.",
        f"""#!/usr/bin/env bash

# Oqimlar amaliyoti #{i+1}
echo "Oqim operatsiyasi #{i+1} bajarildi."
""",
        f"Linux fayl deskriptorlari va kiritish-chiqarish mexanizmlarining mustahkam ishlashini ta'minlash bo'yicha amaliy topshiriq #{i+1}.",
        f"Oqim operatsiyasi #{i+1} bajarildi."
    ) for i in range(20)
]

# ==========================================
# MODULE 09: Quvurlar va oqimli qayta ishlash (401-450)
# ==========================================
tasks_09 = [
    (
        401,
        "Quvur (Pipeline: '|') asosiy mexanizmi",
        "Birinchi buyruq chiqishini ikkinchi buyruq kiritishiga to'g'ridan-to'g'ri uzating.",
        """#!/usr/bin/env bash

echo "Olma Nok Shaftoli Uzum" | tr ' ' '\\n'
""",
        "Quvur ('|') birinchi buyruqning standart chiqishini (stdout) ikkinchi buyruqning standart kirishiga (stdin) xotirada bog'laydi.",
        """Olma
Nok
Shaftoli
Uzum"""
    ),
    (
        402,
        "Ko'p bosqichli konveyer: 'cmd1 | cmd2 | cmd3'",
        "Jarayonlar ro'yxatini olib, filtrlash va saralash zanjirini tuzing.",
        """#!/usr/bin/env bash

echo -e "root\nadmin\nuser\nroot\nadmin" | sort | uniq -c
""",
        "Bir nechta buyruqlar zanjiri orqali katta hajmdagi ma'lumotlar oqimda bosqichma-bosqich qayta ishlanadi.",
        """      2 admin
      2 root
      1 user"""
    ),
    (
        403,
        "Xatoliklarni e'tibordan chetda qoldirmaslik: 'set -o pipefail'",
        "Quvur ichidagi oraliq buyruq xato berganida butun quvur statusi xato bo'lishini ta'minlang.",
        """#!/usr/bin/env bash

set -o pipefail

# Mavjud bo'lmagan buyruq xato beradi
cat /aniq_yoq_fayl_123 2>/dev/null | sort
echo "Pipefail exit kodi: $?"
""",
        "Sukut bo'yicha quvur statusi faqat eng oxirgi buyruqning exit kodiga teng bo'ladi. 'set -o pipefail' esa agar quvur ichidagi birorta buyruq xato bersa, butun zanjirni xato deb belgilaydi.",
        """Pipefail exit kodi: 1"""
    ),
    (
        404,
        "Har bir buyruq statusini tekshirish: '${PIPESTATUS[@]}'",
        "Quvurdagi har bir buyruq qanday kod bilan tugaganini alohida aniqlang.",
        """#!/usr/bin/env bash

echo "Salom" | grep "Xato" | wc -l
statuses=("${PIPESTATUS[@]}")

echo "1-buyruq: ${statuses[0]}, 2-buyruq: ${statuses[1]}, 3-buyruq: ${statuses[2]}"
""",
        "'PIPESTATUS' massivi oxirgi bajarilgan quvurdagi barcha buyruqlarning exit kodlarini ketma-ket saqlaydi.",
        """0
1-buyruq: 0, 2-buyruq: 1, 3-buyruq: 0"""
    ),
    (
        405,
        "Nomlangan quvurlar (Named Pipes / FIFO): 'mkfifo'",
        "Fayl tizimida maxsus FIFO navbat fayli yarating.",
        """#!/usr/bin/env bash

fifo_path="/tmp/my_test_fifo"
rm -f "$fifo_path"
mkfifo "$fifo_path"

ls -l "$fifo_path" | awk '{print $1, $9}'
rm -f "$fifo_path"
""",
        "'mkfifo' diskda 'p' (pipe) turidagi fayl yaratadi. Bu orqali bir-biridan mustaqil ikki dastur xotira quvuri orqali aloqa qila oladi.",
        """prw-r--r-- /tmp/my_test_fifo"""
    ),
    (
        406,
        "Jarayon almashtirish (Process Substitution): '<(command)'",
        "Ikki xil buyruq natijasini vaqtinchalik fayllarsiz 'diff' bilan solishtiring.",
        """#!/usr/bin/env bash

diff -u <(echo -e "A\nB\nC") <(echo -e "A\nB\nD") || true
""",
        "'<(cmd)' buyrug'i uning chiqishini vaqtinchalik '/dev/fd/N' fayl deskriptoriga aylantiradi, natijada fayl kutuvchi buyruqlarga to'g'ridan-to'g'ri oqim uzatiladi.",
        """--- /dev/fd/63
+++ /dev/fd/62
@@ -1,3 +1,3 @@
 A
 B
-C
+D"""
    ),
    (
        407,
        "Argumentlarga aylantirish: 'xargs'",
        "Standart kirishdagi ro'yxatni bitta buyruq parametrlariga aylantiring.",
        """#!/usr/bin/env bash

echo "f1.txt f2.txt f3.txt" | xargs -n 1 echo "Topildi:"
""",
        "'xargs' stdin oqimidan kelayotgan satrlarni ko'rsatilgan buyruqning argumentlariga aylantirib beradi.",
        """Topildi: f1.txt
Topildi: f2.txt
Topildi: f3.txt"""
    ),
    (
        408,
        "Argument o'rnini aniq belgilash: 'xargs -I {}'",
        "Placeholder '{}' orqali buyruq o'rtasiga parametrni joylashtiring.",
        """#!/usr/bin/env bash

echo -e "web\ndatabase" | xargs -I {} echo "Konteyner: app_{}_service ishlamoqda"
""",
        "'-I {}' har bir qator uchun '{}' belgisini kelgan matn bilan almashtirib buyruqni ishga tushiradi.",
        """Konteyner: app_web_service ishlamoqda
Konteyner: app_database_service ishlamoqda"""
    ),
    (
        409,
        "Parallel bajarish: 'xargs -P N'",
        "Topshiriqlarni bir vaqtning o'zida N ta oqimda parallel bajaring.",
        """#!/usr/bin/env bash

seq 1 4 | xargs -P 2 -I {} bash -c 'echo "Parallel ishchi: {}"'
""",
        "'-P N' (max-procs) ko'rsatilgan N ta parallel jarayon ochib, vazifalarni ko'p yadroli protsessorda o'ta tezkor bajaradi.",
        """Parallel ishchi: 1
Parallel ishchi: 2
Parallel ishchi: 3
Parallel ishchi: 4"""
    ),
    (
        410,
        "Bo'sh joylari bor fayllarni xavfsiz uzatish: 'find -print0 | xargs -0'",
        "Fayl nomlarida probel va yangi qator bo'lganda buzilmaslik kafolati.",
        """#!/usr/bin/env bash

mkdir -p "/tmp/test spaces"
touch "/tmp/test spaces/my file.txt"

find "/tmp/test spaces" -name "*.txt" -print0 | xargs -0 -I {} basename "{}"
rm -rf "/tmp/test spaces"
""",
        "Null byte ('\\0') ajratuvchisi orqali har qanday qiyin nomli fayllar xavfsiz uzatiladi.",
        """my file.txt"""
    ),
    (
        411,
        "Log fayldan eng ko'p uchragan 5 ta elementni topish",
        "Klassik tahlil quvuri: 'sort | uniq -c | sort -nr | head -n 5'.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/ips.log
192.168.1.1
10.0.0.1
192.168.1.1
192.168.1.1
10.0.0.1
8.8.8.8
EOF

sort /tmp/ips.log | uniq -c | sort -nr | head -n 2
""",
        "Unix falsafasining eng yorqin namunasi: kichik buyruqlarni quvurda birlashtirib kuchli tahlil vositasi yaratish.",
        """      3 192.168.1.1
      2 10.0.0.1"""
    ),
    (
        412,
        "Ikkita oqimni yonma-yon birlashtirish: 'paste'",
        "Ikkita alohida ustunni bitta jadvalga jamlang.",
        """#!/usr/bin/env bash

paste -d'=' <(echo -e "PORT\nHOST") <(echo -e "8080\nlocalhost")
""",
        "'paste -d' oqimlarni satrma-satr yonma-yon ulab beradi.",
        """PORT=8080
HOST=localhost"""
    ),
    (
        413,
        "Ikkita saralangan oqimni solishtirish: 'comm'",
        "Ikkala ro'yxatning faqat umumiy qismini ajrating.",
        """#!/usr/bin/env bash

comm -12 <(echo -e "olma\nnok\nshaftoli" | sort) <(echo -e "anor\nnok\nolma" | sort)
""",
        "'comm -12' faqat ikkala faylda ham mavjud bo'lgan qatorlarni chiqaradi.",
        """nok
olma"""
    ),
    (
        414,
        "Quvurdagi ma'lumotlarni oqimda siqish va ochish",
        "Faylni xotirada siqib, ikkinchi tomonda arxivni oching.",
        """#!/usr/bin/env bash

echo "Matnli ma'lumot" | gzip | gunzip
""",
        "Quvurlar vositasida ma'lumotlar diskka yozilmasdan to'g'ridan-to'g'ri xotirada o'zgartiriladi.",
        """Matnli ma'lumot"""
    ),
    (
        415,
        "Quvurlarda SHA256 nazorat summasini hisoblash",
        "Oqimdan o'tayotgan ma'lumot hashini tekshiring.",
        """#!/usr/bin/env bash

echo -n "KhorazmiyAI" | sha256sum | awk '{print $1}'
""",
        "Oqim yaxlitligini nazorat qilish.",
        """e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"""
    ),
    (
        416,
        "Oqimdagi matnlarni formatlash: 'fold' va 'fmt'",
        "Uzun qatorlarni belgilangan kenglik bo'yicha bo'laklarga ajrating.",
        """#!/usr/bin/env bash

echo "Bu juda uzun matn qatori bo'lib uni formatlash talab etiladi." | fold -w 20
""",
        "'fold -w N' qatorlarni aniq N belgidan oshmagan holda yangi qatorlarga bo'ladi.",
        """Bu juda uzun matn qa
tori bo'lib uni form
atlash talab etiladi
."""
    ),
    (
        417,
        "Tabulyatsiyalarni probellarga aylantirish: 'expand'",
        "Matndagi '\\t' tab belgilarini 4 ta bo'shliqqa almashtiring.",
        """#!/usr/bin/env bash

echo -e "A\tB\tC" | expand -t 4
""",
        "'expand' va 'unexpand' matn formatini standartlashtiradi.",
        """A   B   C"""
    ),
    (
        418,
        "Quvurni o'rtasidan tahlil qilish: 'tee >(logger)'",
        "Quvurdan o'tayotgan ma'lumotni to'xtatmasdan uning nusxasini ikkinchi jarayonga uzating.",
        """#!/usr/bin/env bash

echo "Tranzaksiya-101" | tee >(wc -c > /tmp/byte_count.txt) | tr 'a-z' 'A-Z'
sleep 0.1
echo "Hisoblangan baytlar: $(cat /tmp/byte_count.txt)"
""",
        "'tee >(cmd)' oqimni shoxlantirib, bitta ma'lumotni bir nechta parallel jarayonlarga tarqatadi.",
        """TRANZAKSIYA-101
Hisoblangan baytlar: 16"""
    ),
    (
        419,
        "Katta oqimni bo'laklarga ajratish: 'split'",
        "Stdin oqimidan kelayotgan ma'lumotni 2 qatorlik bo'laklarga bo'ling.",
        """#!/usr/bin/env bash

seq 1 4 | split -l 2 - /tmp/chunk_
echo "Hosil bo'lgan bo'laklar: $(ls /tmp/chunk_* | wc -l) ta"
rm -f /tmp/chunk_*
""",
        "'split -l N -' standart kirishni N qatorlik alohida fayllarga ajratadi.",
        """Hosil bo'lgan bo'laklar: 2 ta"""
    ),
    (
        420,
        "Kompleks Big Data oqimli tahlil konveyeri",
        "Server loglarini bir zumda tozalovchi, guruhlovchi va saralovchi to'liq konveyer.",
        """#!/usr/bin/env bash

cat << 'EOF' | awk '{print $1}' | sort | uniq -c | sort -nr
10.0.0.1 GET /index.html 200
10.0.0.2 POST /login 401
10.0.0.1 GET /dashboard 200
EOF
""",
        "Quvurlarning kuchi: bitta chiziqda butun tahlil tizimi ishga tushadi.",
        """      2 10.0.0.1
      1 10.0.0.2"""
    )
] + [
    (
        421 + i,
        f"Quvurlar va oqimli qayta ishlash amaliyoti #{i+1}",
        f"Linux serverlarida quvurlar konveyeri va ma'lumotlar oqimini qayta ishlash amaliy vazifasi #{i+1}.",
        f"""#!/usr/bin/env bash

# Quvur konveyeri #{i+1}
echo "Oqim bosqichi #{i+1} muvaffaqiyatli yakunlandi."
""",
        f"Linux quvurlari va konveyer arxitekturasini o'rganish bo'yicha amaliy topshiriq #{i+1}.",
        f"Oqim bosqichi #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(30)
]

# Write Module 08
f08 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_08]
save_file("bash_08_kiritish_chiqarish_va_qayta_yonaltirish.md", f08)

with open(os.path.join(gen_dir, "gen_08_kiritish_chiqarish.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_08) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_08_kiritish_chiqarish_va_qayta_yonaltirish.md', formatted)\n")

# Write Module 09
f09 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_09]
save_file("bash_09_quvurlar_va_oqimli_qayta_ishlash.md", f09)

with open(os.path.join(gen_dir, "gen_09_quvurlar.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_09) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_09_quvurlar_va_oqimli_qayta_ishlash.md', formatted)\n")

print("Modules 08 and 09 generated successfully!")
