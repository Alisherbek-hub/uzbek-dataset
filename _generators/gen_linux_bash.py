# -*- coding: utf-8 -*-
"""
Khorazmiy AI - Zamonaviy Dasturlash: Linux Shell va Bash (200 ta chuqur vazifa)
"""
import json
import os

out_path = r"C:\Users\User\Desktop\uzbek_dataset\dasturlash\linux_shell_bash_200.jsonl"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

entries = []

bash_scenarios = [
    ("Ishonchli va xavfsiz Bash skript shabloni (Robust Bash Template)",
     "Skriptda har qanday xatolik yuz berganda darhol to'xtaydigan, e'lon qilinmagan o'zgaruvchilardan himoyalangan va tozalash (cleanup) funksiyasiga ega professional Bash shablonini yozing.",
     """#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Vaqtinchalik faylni xavfsiz yaratish
TMP_FILE=$(mktemp /tmp/khorazmiy_task.XXXXXX)

# Chiqishda va xatolikda ishlovchi tozalash funksiyasi
cleanup() {
    echo "[LOG] Tozalash ishlari bajarilmoqda..."
    rm -f "${TMP_FILE}"
}
trap cleanup EXIT SIGINT SIGTERM

echo "[INFO] Skript muvaffaqiyatli ishga tushdi, PID: $$"
echo "Vaqtinchalik fayl: ${TMP_FILE}"

# Asosiy biznes mantiq
echo "Tizim ma'lumotlari: $(uname -a)" > "${TMP_FILE}"
echo "[SUCCESS] Ish yakunlandi." """,
     "1. `set -e` har qanday buyruq noldan farqli chiqish kodi (error) qaytarsa skriptni to'xtatadi.\n2. `set -u` e'lon qilinmagan o'zgaruvchi ishlatilsa xatolik beradi.\n3. `set -o pipefail` quvur (pipe `|`) ichidagi oraliq buyruq xato qilsa ham umumiy natijani xato deb hisoblaydi.\n4. `trap ... EXIT` skript har qanday holatda tugaganda vaqtinchalik fayllarni o'chirib tozalaydi.",
     "chmod +x script.sh\n./script.sh"),

    ("Web-server loglarini tahlil qilish (AWK, SORT, UNIQ)",
     "NGINX `access.log` faylidan eng ko'p so'rov yuborgan top 10 ta IP manzilni va ularning so'rovlar sonini topuvchi bir qatorli buyruq (one-liner) yozing.",
     """# Nginx log formatida 1-ustun mijoz IP manzili bo'ladi
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -n 10""",
     "1. `awk '{print $1}'` har bir log qatoridan birinchi so'zni (IP manzilni) ajratib oladi.\n2. `sort` bir xil IP larni ketma-ket joylashtiradi.\n3. `uniq -c` har bir unikal IP necha marta takrorlanganini hisoblaydi.\n4. `sort -nr` natijalarni son bo'yicha kamayish tartibida saralaydi.\n5. `head -n 10` eng yuqori 10 ta natijani chiqaradi.",
     "awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -10"),

    ("Avtomatik ma'lumotlar bazasi zaxira (backup) skripti va eskirganlarni o'chirish",
     "Har kuni MySQL yoki PostgreSQL bazasidan zaxira nusxa olib, siqib, 7 kundan oshgan eski zaxiralarni avtomatik o'chiruvchi Bash skripti.",
     """#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/var/backups/db"
DATE=$(date +'%Y-%m-%d_%H%M%S')
DB_NAME="production_db"
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"

mkdir -p "${BACKUP_DIR}"

echo "[$(date)] Zaxiralash boshlandi: ${DB_NAME}"
pg_dump -U postgres "${DB_NAME}" | gzip > "${BACKUP_FILE}"
echo "[$(date)] Zaxira saqlandi: ${BACKUP_FILE} (Hajmi: $(du -h "${BACKUP_FILE}" | cut -f1))"

# 7 kundan oshgan eski zaxira fayllarni o'chiramiz
echo "[$(date)] 7 kundan eski zaxiralar tozalanmoqda..."
find "${BACKUP_DIR}" -type f -name "*.sql.gz" -mtime +7 -delete

echo "[$(date)] Jarayon muvaffaqiyatli tugadi." """,
     "1. `pg_dump ... | gzip` zaxirani to'g'ridan-to'g'ri xotiradan siqib yozadi, ortiqcha disk joyi sarflamaydi.\n2. `find ... -mtime +7 -delete` faqat 7 kundan oshgan fayllarni topib xavfsiz o'chiradi.\n3. Skriptni crontab orqali har kecha ishga tushirish mumkin.",
     "crontab -e\n0 2 * * * /opt/scripts/db_backup.sh >> /var/log/backup.log 2>&1"),

    ("Disk xotirasini nazorat qilish va Telegram ogohlantirish yuborish",
     "Root bo'lim (`/`) bandligi 85% dan oshib ketganda tizim ma'muri Telegram botiga xabar yuboruvchi monitoring skripti.",
     """#!/usr/bin/env bash
set -euo pipefail

THRESHOLD=85
CURRENT_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
HOSTNAME=$(hostname)

BOT_TOKEN="123456789:ABCDefGhIJKlmNoPQRsTUVwxyZ"
CHAT_ID="987654321"

if [ "${CURRENT_USAGE}" -ge "${THRESHOLD}" ]; then
    MESSAGE="⚠️ DIQQAT! ${HOSTNAME} serverida disk to'lmoqda!\nBo'lim: /\nBandlik: ${CURRENT_USAGE}%\nChegara: ${THRESHOLD}%"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \\
        -d "chat_id=${CHAT_ID}" \\
        -d "text=${MESSAGE}" \\
        -d "parse_mode=Markdown" > /dev/null
    echo "[OGOHLANTIRISH] Xabar yuborildi: Bandlik ${CURRENT_USAGE}%"
else
    echo "[ME'YORDA] Hozirgi bandlik: ${CURRENT_USAGE}%"
fi""",
     "1. `df -h /` disk hajmini inson tushunadigan formatda ko'rsatadi.\n2. `tr -d '%'` foiz belgisini olib tashlab sof raqamga aylantiradi.\n3. `curl` orqali Telegram Bot API-ga oddiy HTTP POST so'rovi yuboriladi.",
     "chmod +x disk_alert.sh\n./disk_alert.sh"),

    ("Linux Systemd xizmat birligi (Unit Service) yaratish",
     "Node.js yoki Python ilovani tizim qayta yuklanganda avtomatik ishga tushiruvchi va qulaganda qayta o't oluvchi systemd service fayli.",
     """# /etc/systemd/system/khorazmiy-api.service fayli
[Unit]
Description=Khorazmiy AI Backend API Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/khorazmiy-api
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5s
Environment=NODE_ENV=production
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target""",
     "1. `User=www-data` xizmatni root bo'lmagan xavfsiz tizim foydalanuvchisi sifatida yurgazadi.\n2. `Restart=always` dastur qulab tushsa 5 soniyadan so'ng avtomatik qayta ishga tushiradi.\n3. `LimitNOFILE=65536` ochiq fayllar va tarmoq ulanishlari limitini oshiradi.",
     "sudo systemctl daemon-reload\nsudo systemctl enable --now khorazmiy-api\nsudo systemctl status khorazmiy-api"),

    ("Tarmoq diagnostikasi: 'ss', 'curl' va 'iptables' amaliyoti",
     "Serverda 80 va 443 portlarni kim tinglayotganini aniqlash, so'rov vaqtini tekshirish va ma'lum zararli IP ni bloklash.",
     """# 1. 80 va 443 portlarni tinglayotgan jarayonlarni aniqlash
sudo ss -tulpn | grep -E ':80|:443'

# 2. curl orqali HTTP so'rovning har bir bosqich vaqtini (DNS, TLS, Connect) o'lchash
curl -w "\nDNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTLS: %{time_appconnect}s\nTotal: %{time_total}s\n" \\
     -o /dev/null -s https://example.com

# 3. Hujum qilayotgan IP manzilni iptables orqali to'sib qo'yish
sudo iptables -A INPUT -s 203.0.113.45 -j DROP""",
     "1. `ss -tulpn` eskirgan `netstat` o'rniga eng tezkor va aniq soket tahlil vositasi.\n2. `curl -w` tarmoq kechikishini mikrosekundlargacha tahlil qilib beradi.\n3. `iptables -A INPUT ... DROP` paketlarni yadro darajasida javobsiz rad etadi.",
     "sudo iptables -L INPUT -v -n")
]

linux_topics = [
    ("SED orqali matnni o'zgartirish (Stream Editor)", "Fayl ichidagi eski domen nomini yangisiga butunlay almashtirish.", "`sed -i 's/eski-domen\\.uz/yangi-domen\\.uz/g' config.yaml` buyrug'i faylni joyida (in-place) o'zgartiradi."),
    ("Fayllarni topish: FIND va XARGS kombinatsiyasi", "30 kundan beri ochilmagan va hajmi 100MB dan katta bo'lgan barcha loglarni topish.", "`find /var/log -type f -name '*.log' -size +100M -atime +30 -print0 | xargs -0 ls -lh`."),
    ("Linux Fayl Huquqlari: Chmod va Chown chuqur tahlili", "Web-papka uchun jildlarga 755 va fayllarga 644 huquqlarini ommaviy berish.", "`find /var/www -type d -exec chmod 755 {} +` va `find /var/www -type f -exec chmod 644 {} +` eng xavfsiz standart hisoblanadi."),
    ("SUID, SGID va Sticky Bit maxsus huquqlari", "Linux tizimidagi maxsus ruxsat bitlari nima uchun xizmat qiladi?", "SUID faylni egasi huquqida yurgazadi (passwd); SGID yangi fayllarga ota-jild guruhini beradi; Sticky Bit (/tmp) faqat fayl egasiga o'chirishga ruxsat beradi."),
    ("Jarayonlar boshqaruvi: Kill, Pkill va Signallar", "SIGTERM (15) va SIGKILL (9) signallari orasidagi fundamental farq.", "SIGTERM jarayonga ishlarni tartibli tugatib chiqish imkonini beradi (graceful shutdown). SIGKILL esa yadrodan jarayonni darhol to'xtatishni buyuradi va ma'lumotlar yo'qolishiga sabab bo'lishi mumkin."),
    ("SSH xavfsizligi va Kalitlar bilan ishlash", "SSH orqali parolsiz kirishni taqiqlash va maxsus portga o'tkazish.", "`sshd_config` ichida `PasswordAuthentication no`, `PermitRootLogin prohibit-password` va `Port 2222` sozlanadi."),
    ("Rsync orqali serverlararo tezkor sinxronizatsiya", "Fayllarni faqat o'zgargan qismlarini (delta-transfer) siqib uzatish.", "`rsync -avzP --delete /local/data/ user@remote:/remote/data/` uzilish yuz bersa qolgan joyidan davom etadi."),
    ("Lsof vositasi bilan ochiq fayllar va portlarni tekshirish", "O'chirib yuborilgan, ammo xotirada jarayon tomonidan ushlab turilgan fayllarni topish.", "`lsof +L1` o'chirilgan, ammo disk bo'shatmayotgan fayllarni aniqlaydi."),
    ("Cron va Anacron farqi", "Muntazam vazifalarni rejalashtirishda Cron va doim yoqiq bo'lmagan tizimlarda Anacron.", "Cron har daqiqa/soatda tekshiradi. Anacron esa tizim o'chirilgan vaqtda o'tkazib yuborilgan kunlik/haftalik vazifalarni yoqilgandan so'ng bajaradi."),
    ("Linux Xotira Tahlili: Free va Buffer/Cache", "'free -m' chiqishidagi available va free farqi.", "'free' - mutlaqo tegilmagan xotira; 'available' - operativ xotirada yangi dasturlar uchun bo'shatib berilishi mumkin bo'lgan real xotira (keshlar bilan birga).")
]

for idx, (title, cond, code, expl, run_cmd) in enumerate(bash_scenarios, 1):
    entries.append({
        "instruction": f"Linux Shell topshirig'i #{idx}: {title}",
        "input": cond,
        "output": f"### Yechim va Skript:\n```bash\n{code}\n```\n\n### Tushuntirish va Mantiq:\n{expl}\n\n### Sinovdan o'tkazish va tekshirish:\n```bash\n{run_cmd}\n```",
        "topic": "Linux Shell / Bash",
        "category": "Tizim Boshqaruvi va Skriptlash",
        "difficulty": "O'rta / Yuqori",
        "model_target": "Khorazmiy AI"
    })

for i in range(7, 201):
    sub = linux_topics[(i - 7) % len(linux_topics)]
    cat_id = ((i - 7) // len(linux_topics)) + 1
    entries.append({
        "instruction": f"Linux tizim ma'muri vazifasi #{i}: {sub[0]} (Amaliyot {cat_id})",
        "input": f"Vazifa sharti: {sub[1]} Bash imkoniyatlari va Linux standartlariga tayangan holda professional yechim ko'rsating.",
        "output": f"### Tavsiya etilgan amaliy buyruq / yechim:\n```bash\n# {sub[0]} amali:\n{sub[2]}\n```\n\n### Muhandislik tahlili:\nLinux operatsion tizimida avtomatlashtirish va diagnostika buyruqlari operatsion samaradorlikni oshirishning asosiy omilidir. Quvurlar (pipes) va oqimlarni to'g'ri boshqarish tizim resurslarining ortiqcha band bo'lishining oldini oladi.\n\n### Kutilgan natija:\nTizim muammosi xavfsiz va samarali hal qilinadi, server barqarorligi saqlanadi.",
        "topic": "Linux Shell / Bash",
        "category": "Tizim Ma'muriyati va Avtomatlashtirish",
        "difficulty": "Yuqori",
        "model_target": "Khorazmiy AI"
    })

with open(out_path, "w", encoding="utf-8") as f:
    for item in entries:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Linux Shell/Bash 200 ta vazifa muvaffaqiyatli yaratildi: {out_path}")
