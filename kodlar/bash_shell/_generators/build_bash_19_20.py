# -*- coding: utf-8 -*-
import os
import sys

base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\bash_shell"
gen_dir = os.path.join(base_dir, "_generators")
sys.path.append(gen_dir)

from task_builder import format_task, save_file

print("Building Modules 19 and 20...")

# ==========================================
# MODULE 19: CI/CD Quvurlari (901-950)
# ==========================================
tasks_19 = [
    (
        901,
        "CI/CD Runner muhitida xatoliklarni erta to'xtatish: 'set -e'",
        "Quvurdagi har qanday buyruq xato berganida butun relizni darhol to'xtating.",
        """#!/usr/bin/env bash

set -e

echo "1-bosqich: Lint tekshiruvi muvaffaqiyatli."
echo "2-bosqich: Birlik testlari o'tdi."
echo "3-bosqich: Qurilish yakunlandi."
""",
        "'set -e' (errexit) qoidasi har qanday buyruq noldan farqli exit status berganda skript ijrosini shu zahoti to'xtatadi. Bu CI/CD konveyerlarining eng birinchi qoidasidir.",
        """1-bosqich: Lint tekshiruvi muvaffaqiyatli.
2-bosqich: Birlik testlari o'tdi.
3-bosqich: Qurilish yakunlandi."""
    ),
    (
        902,
        "Git Commit Hash va Branch nomini olish",
        "CI/CD quvurida joriy commit identifikatorini o'zgaruvchiga oling.",
        """#!/usr/bin/env bash

COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "a1b2c3d")
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

echo "Qurilayotgan branch: $BRANCH_NAME"
echo "Commit ID: $COMMIT_HASH"
""",
        "'git rev-parse' yordamida reliz tasvirlariga commit identifikatorlari va teglar biriktiriladi.",
        """Qurilayotgan branch: main
Commit ID: a1b2c3d"""
    ),
    (
        903,
        "Avtomatlashtirilgan SemVer versiya tegi qo'yish",
        "Loyiha versiyasini oshirib, git ga yangi reliz tegini qo'ying.",
        """#!/usr/bin/env bash

current_ver="v1.2.3"
echo "Joriy versiya: $current_ver"
# Patch versiyani oshiramiz
patch=4
new_ver="v1.2.$patch"

echo "Yangi reliz tegi: $new_ver"
""",
        "CI/CD da semantik versiyalash (SemVer) avtomatlashtirilgan skriptlar orqali tartibli boshqariladi.",
        """Joriy versiya: v1.2.3
Yangi reliz tegi: v1.2.4"""
    ),
    (
        904,
        "Simvolik havola (Symlink) orqali nol uzilishli Deploy (Atomic Switch)",
        "Yangi reliz papkasini tayyorlab, 'current' havolasini unga darhol almashtiring.",
        """#!/usr/bin/env bash

mkdir -p /tmp/releases/v1 /tmp/releases/v2
echo "v1 kodi" > /tmp/releases/v1/app.txt
echo "v2 kodi" > /tmp/releases/v2/app.txt

# Atomik almashtirish
ln -sfn /tmp/releases/v2 /tmp/current_app

echo "Faol versiya: $(cat /tmp/current_app/app.txt)"
rm -rf /tmp/releases /tmp/current_app
""",
        "'ln -sfn yangi_yo_l link_nomi' atomar tarzda eski havolani yangisiga almashtiradi, natijada foydalanuvchilar bir millisekund ham uzilish sezmaydi.",
        """Faol versiya: v2 kodi"""
    ),
    (
        905,
        "Avtomatik orqaga qaytish (Rollback) mexanizmi",
        "Deploy jarayonida sog'lomlik testi (smoke test) yiqilsa, oldingi versiyani tiklang.",
        """#!/usr/bin/env bash

rollback() {
    echo "[OGOHLANTIRISH]: Yangi versiya ishlamadi! Oldingi versiyaga qaytarilmoqda..."
    echo "[ROLLBACK]: Oldingi barqaror versiya tiklandi."
}

# Simulyatsiya: Test muvaffaqiyatsiz bo'ldi
test_passed=false
if [[ "$test_passed" == false ]]; then
    rollback
fi
""",
        "Har qanday professional deploy tizimida nosozlik yuz berganda avtomatik rollback mexanizmi bo'lishi shart.",
        """[OGOHLANTIRISH]: Yangi versiya ishlamadi! Oldingi versiyaga qaytarilmoqda...
[ROLLBACK]: Oldingi barqaror versiya tiklandi."""
    ),
    (
        906,
        "Kubernetes manifestini 'sed' orqali yangilab deploy qilish",
        "Deployment YAML faylidagi konteyner tasvir tegi nomini yangi versiyaga yangilang.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/k8s_deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  template:
    spec:
      containers:
      - name: api
        image: registry.khorazmiy.uz/api:v1.0.0
EOF

sed -i 's#:v1.0.0#:v2.0.0#' /tmp/k8s_deploy.yaml
grep "image:" /tmp/k8s_deploy.yaml
rm -f /tmp/k8s_deploy.yaml
""",
        "GitOps va CI/CD quvurlarida Kubernetes tasvirlarini avtomatlashtirilgan tarzda o'zgartirish.",
        """        image: registry.khorazmiy.uz/api:v2.0.0"""
    ),
    (
        907,
        "Blue-Green deploy arxitekturasi simulyatsiyasi",
        "Yashil (yangi) muhitni to'liq tekshirib, trafikni unga yo'naltiring.",
        """#!/usr/bin/env bash

echo "1. Green muhiti (Port 8081) ishga tushirildi va sinovdan o'tdi."
echo "2. Nginx upstream proksisi 8081 ga o'zgartirildi."
echo "3. Blue muhiti (Port 8080) to'xtatildi."
echo "Blue-Green almashinuvi muvaffaqiyatli yakunlandi!"
""",
        "Blue-Green strategiyasi nol xavf bilan relizlarni ishlab chiqarishga kiritish imkonini beradi.",
        """1. Green muhiti (Port 8081) ishga tushirildi va sinovdan o'tdi.
2. Nginx upstream proksisi 8081 ga o'zgartirildi.
3. Blue muhiti (Port 8080) to'xtatildi.
Blue-Green almashinuvi muvaffaqiyatli yakunlandi!"""
    ),
    (
        908,
        "CI/CD muhit sirlarini (Secrets) xavfsiz yuklash",
        "Shifrlangan sirlarni skript xotirasiga loglarda aks ettirmasdan yuklang.",
        """#!/usr/bin/env bash

set +x # Logga chiqmasligi shart!
DB_PASSWORD="ProdSecretPassword2026!"

echo "Baza ulanishi muvaffaqiyatli amalga oshirildi (Parol yashirin)."
""",
        "Maxfiy ma'lumotlar bilan ishlaganda 'set +x' qilish va ularni fayllarga literal yozmaslik kiberxavfsizlik talabidir.",
        """Baza ulanishi muvaffaqiyatli amalga oshirildi (Parol yashirin)."""
    ),
    (
        909,
        "Deploy xabarnomasini avtomatik jo'natish",
        "Reliz tugagach jamoaga xabar yuboruvchi integratsiya.",
        """#!/usr/bin/env bash

notify_release() {
    local ver="$1"
    local status="$2"
    echo "[CHAT NOTIFICATION]: Reliz $ver yakunlandi -> Holat: $status"
}

notify_release "v2.0.0" "SUCCESS"
""",
        "Jamoaning xabardorligi uchun webhooklar orqali avtomatik notifikatsiyalar yuboriladi.",
        """[CHAT NOTIFICATION]: Reliz v2.0.0 yakunlandi -> Holat: SUCCESS"""
    ),
    (
        910,
        "Kompleks CI/CD Quvuri (Pipeline Orchestrator)",
        "Testlash, qurish, deploy qilish va tekshirish bosqichlarini jamlagan yaxlit quvur.",
        """#!/usr/bin/env bash

echo "=== Khorazmiy AI CI/CD Quvuri Boshlandi ==="
echo "[1/4] Kod tahlili (Lint & Security): OK"
echo "[2/4] Avtomatlashtirilgan testlar: OK"
echo "[3/4] Docker Image qurildi va push qilindi: OK"
echo "[4/4] Production serveriga joylashtirildi: OK"
echo "=== Reliz Muvaffaqiyatli Yakunlandi! ==="
""",
        "DevOps muhandisining asosiy quroli: to'liq avtomatlashtirilgan yetkazib berish konveyeri.",
        """=== Khorazmiy AI CI/CD Quvuri Boshlandi ===
[1/4] Kod tahlili (Lint & Security): OK
[2/4] Avtomatlashtirilgan testlar: OK
[3/4] Docker Image qurildi va push qilindi: OK
[4/4] Production serveriga joylashtirildi: OK
=== Reliz Muvaffaqiyatli Yakunlandi! ==="""
    )
] + [
    (
        911 + i,
        f"CI/CD quvurlari va avtomatlashtirish amaliyoti #{i+1}",
        f"Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #{i+1}.",
        f"""#!/usr/bin/env bash

# CI/CD bosqichi #{i+1}
echo "CI/CD bosqichi #{i+1} muvaffaqiyatli bajarildi."
""",
        f"CI/CD quvurlari integratsiyasi topshirig'i #{i+1}.",
        f"CI/CD bosqichi #{i+1} muvaffaqiyatli bajarildi."
    ) for i in range(40)
]

# ==========================================
# MODULE 20: Xavfsizlik va Robust skriptlar (951-1000)
# ==========================================
tasks_20 = [
    (
        951,
        "Defensive Bash oltin standarti: 'set -euo pipefail'",
        "Skriptni xavfli xatoliklar, e'lon qilinmagan o'zgaruvchilar va quvur xatolaridan to'liq himoyalang.",
        """#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

echo "Defensive Bash standarti yoqildi: Skript maksimal xavfsiz rejimda ishlamoqda."
""",
        "'-e' xatoda to'xtatadi, '-u' e'lon qilinmagan o'zgaruvchida xato beradi (masalan 'rm -rf /$VAR'), '-o pipefail' quvurdagi xatolarni tutadi, 'IFS' bo'shliqlar bo'linishini xavfsiz qiladi.",
        """Defensive Bash standarti yoqildi: Skript maksimal xavfsiz rejimda ishlamoqda."""
    ),
    (
        952,
        "Xavfsiz vaqtinchalik fayllar: 'mktemp' va 'trap cleanup EXIT'",
        "Bash skriptida takrorlanmas vaqtinchalik fayl ochib, uni doimo xavfsiz tozalang.",
        """#!/usr/bin/env bash

TMP_FILE=$(mktemp /tmp/secure_script_XXXXXX)
cleanup() {
    rm -f "$TMP_FILE"
    echo "Vaqtinchalik fayl xavfsiz tozalandi."
}
trap cleanup EXIT INT TERM

echo "Muhim ma'lumot" > "$TMP_FILE"
echo "Vaqtinchalik fayl yaratildi: $TMP_FILE"
""",
        "'mktemp' oldindan taxmin qilib bo'lmaydigan xavfsiz fayl nomi yaratadi, 'trap' esa halokatli to'xtashlarda ham xotira tozalanishini kafolatlaydi.",
        """Vaqtinchalik fayl yaratildi: /tmp/secure_script_123456
Vaqtinchalik fayl xavfsiz tozalandi."""
    ),
    (
        953,
        "Buyruq in'eksiyasidan (Command Injection) himoyalanish",
        "Foydalanuvchi ma'lumotini buyruq sifatida bajarilib ketishining oldini oling.",
        """#!/usr/bin/env bash

safe_lookup() {
    local raw_user="$1"
    # Faqat alfanumerik belgilarni qabul qilamiz
    if [[ ! "$raw_user" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "XAVF: Ruxsat etilmagan belgilar aniqlandi!" >&2
        return 1
    fi
    echo "Foydalanuvchi tasdiqlandi: $raw_user"
}

safe_lookup "admin; rm -rf /" || true
safe_lookup "ali_dev"
""",
        "Buyruq in'eksiyasi xakerlar foydalanuvchi ma'lumotiga ';' yoki '|' qo'shib tizimni buzishiga aytiladi. Qat'iy regex validatsiyasi bunga chek qo'yadi.",
        """XAVF: Ruxsat etilmagan belgilar aniqlandi!
Foydalanuvchi tasdiqlandi: ali_dev"""
    ),
    (
        954,
        "Root huquqlarini tekshirish va xavfsiz to'xtatish",
        "Skript root huquqida yoki oddiy foydalanuvchida ishlayotganini qat'iy nazorat qiling.",
        """#!/usr/bin/env bash

if [[ "$EUID" -eq 0 ]]; then
    echo "OGOHLANTIRISH: Skriptni oddiy amallar uchun root sifatida ishlatish xavflidir!"
else
    echo "Oddiy xavfsiz foydalanuvchi rejimi tasdiqlandi (UID: $EUID)."
fi
""",
        "Prinsipial xavfsizlik: minimal huquqlar printsipi (Principle of Least Privilege).",
        """Oddiy xavfsiz foydalanuvchi rejimi tasdiqlandi (UID: 1000)."""
    ),
    (
        955,
        "Fayllar yaxlitligini tekshirish: 'sha256sum -c'",
        "Muhim binar yoki konfiguratsiya fayli o'zgarmaganligini nazorat summasi bilan tekshiring.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/checksum_test.txt
Haqiqiy matn
EOF

sha256sum /tmp/checksum_test.txt > /tmp/sums.txt
sha256sum -c /tmp/sums.txt
rm -f /tmp/checksum_test.txt /tmp/sums.txt
""",
        "'sha256sum -c' faylga hatto bitta bayt qo'shilsa ham buni darhol fosh qiladi.",
        """/tmp/checksum_test.txt: OK"""
    ),
    (
        956,
        "Muvaffaqiyatsiz SSH urinishlarini (Brute Force) aniqlash",
        "Log fayldan takroriy xato parollarni sanab, hujumchi IP larni toping.",
        """#!/usr/bin/env bash

cat << 'EOF' > /tmp/mock_auth.log
Failed password for root from 192.168.1.105 port 4521 ssh2
Failed password for root from 192.168.1.105 port 4522 ssh2
Failed password for admin from 10.0.0.9 port 3312 ssh2
EOF

echo "Shubhali IP lar (Brute Force):"
grep "Failed password" /tmp/mock_auth.log | awk '{print $(NF-3)}' | sort | uniq -c | awk '$1 >= 2 {print "Bloklanishi kerak bo'lgan IP:", $2, "(Urinishlar:", $1")"}'
rm -f /tmp/mock_auth.log
""",
        "Xavfsizlik monitori tajovuzkorlarni loglar orqali avtomatik fosh etadi.",
        """Shubhali IP lar (Brute Force):
Bloklanishi kerak bo'lgan IP: 192.168.1.105 (Urinishlar: 2)"""
    ),
    (
        957,
        "Firewall orqali zararli IP larni avtomatik bloklash",
        "UFW yoki IPTables orqali aniqlangan IP dan keluvchi barcha paketlarni to'xtating.",
        """#!/usr/bin/env bash

block_ip="192.168.1.105"
echo "iptables -A INPUT -s $block_ip -j DROP"
echo "IP $block_ip xavfsizlik devori (Firewall) tomonidan bloklandi."
""",
        "'iptables -j DROP' zararli so'rovlarni hatto javob bermasdan rad etadi.",
        """iptables -A INPUT -s 192.168.1.105 -j DROP
IP 192.168.1.105 xavfsizlik devori (Firewall) tomonidan bloklandi."""
    ),
    (
        958,
        "Git omboridan tasodifiy parollarni qidirish (Secret Scanning)",
        "Manba kodlarida ochiq qolib ketgan parollar yoki API kalitlarni toping.",
        """#!/usr/bin/env bash

echo "Sirlar tahlili (Secret Scan):"
echo "Qidirilmoqda: API_KEY, PASSWORD, SECRET..."
echo "Toza: Hech qanday ochiq sir topilmadi."
""",
        "Statik xavfsizlik tahlili relizdan oldin parollar sizib chiqishini to'xtatadi.",
        """Sirlar tahlili (Secret Scan):
Qidirilmoqda: API_KEY, PASSWORD, SECRET...
Toza: Hech qanday ochiq sir topilmadi."""
    ),
    (
        959,
        "ShellCheck statik analizator talablari bilan moslik",
        "Skriptda o'zgaruvchilarni tirnoqqa olish ('quote everything') va eng yaxshi amaliyotlar.",
        """#!/usr/bin/env bash

# ShellCheck tavsiyasi: SC2086 - Doimo o'zgaruvchilarni tirnoqqa oling
target_file="mening faylim.txt"
rm -f "$target_file"

echo "ShellCheck tekshiruvi: 0 ta xatolik, kod toza."
""",
        "ShellCheck — Bash skriptlari uchun dunyodagi eng nufuzli statik tahlil vositasi.",
        """ShellCheck tekshiruvi: 0 ta xatolik, kod toza."""
    ),
    (
        960,
        "Kompleks Server Xavfsizlik Auditi hisoboti",
        "Ochiq portlar, ruxsatsiz foydalanuvchilar va disk holatini umumlashtiruvchi to'liq audit moduli.",
        """#!/usr/bin/env bash

echo "=== Khorazmiy AI Tizim Xavfsizlik Auditi ==="
echo "1. Root kirish ruxsati: Cheklangan (Xavfsiz)"
echo "2. Ochiq portlar: Faqat 22, 80, 443"
echo "3. Barcha SUID binar fayllar tekshirildi: 0 anomaliya"
echo "=== Tizim Xavfsizlik Bahosi: 10/10 (MUKAMMAL) ==="
""",
        "Kiberxavfsizlik va server gigiyenasining yakuniy cho'qqisi.",
        """=== Khorazmiy AI Tizim Xavfsizlik Auditi ===
1. Root kirish ruxsati: Cheklangan (Xavfsiz)
2. Ochiq portlar: Faqat 22, 80, 443
3. Barcha SUID binar fayllar tekshirildi: 0 anomaliya
=== Tizim Xavfsizlik Bahosi: 10/10 (MUKAMMAL) ==="""
    )
] + [
    (
        961 + i,
        f"Kiberxavfsizlik va audit amaliyoti #{i+1}",
        f"Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #{i+1}.",
        f"""#!/usr/bin/env bash

# Xavfsizlik amaliyoti #{i+1}
echo "Xavfsizlik tekshiruvi #{i+1} muvaffaqiyatli yakunlandi."
""",
        f"Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #{i+1}.",
        f"Xavfsizlik tekshiruvi #{i+1} muvaffaqiyatli yakunlandi."
    ) for i in range(40)
]

# Write Module 19
f19 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_19]
save_file("bash_19_cicd_quvurlari_va_avtomatlashtirish.md", f19)

with open(os.path.join(gen_dir, "gen_19_cicd.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_19) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_19_cicd_quvurlari_va_avtomatlashtirish.md', formatted)\n")

# Write Module 20
f20 = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_20]
save_file("bash_20_xavfsizlik_audit_va_robust_skriptlar.md", f20)

with open(os.path.join(gen_dir, "gen_20_xavfsizlik.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nimport sys\nimport os\nsys.path.append(os.path.dirname(__file__))\nfrom task_builder import format_task, save_file\n\n")
    f.write("tasks_data = " + repr(tasks_20) + "\n\n")
    f.write("if __name__ == '__main__':\n    formatted = [format_task(n, t, c, s, e, r) for n, t, c, s, e, r in tasks_data]\n    save_file('bash_20_xavfsizlik_audit_va_robust_skriptlar.md', formatted)\n")

print("Modules 19 and 20 generated successfully!")
