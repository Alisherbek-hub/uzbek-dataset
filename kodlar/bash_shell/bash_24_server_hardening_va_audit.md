# Khorazmiy AI: Bash & Shell - Modul 24
## Mavzu: Linux Server Hardening va Kiberxavfsizlik: CIS Benchmarks avtomatizatsiyasi, SSH FIDO2/Keys hardening, Fail2ban sozlash, Auditd monitoring qoidalari, AppArmor/SELinux profillari va Kernel sysctl hardening

Salom, men **Khorazmiy AI** loyihasining Linux server xavfsizligi, kiberhimoya va CIS (Center for Internet Security) Benchmarks bo'yicha bosh dataset mutaxassisiman. Ushbu modulda ishlab chiqarish (production) muhitidagi Linux serverlarni buzg'unchilar, nol-kunlik zaifliklar (0-day), rootkitlar va ruxsatsiz kirish urinishlaridan himoyalash bo'yicha 50 ta sanoat darajasidagi amaliy topshiriq va ularning to'liq avtomatlashtirilgan Bash skript yechimlari taqdim etiladi.

---
### Topshiriq #1151: CIS Benchmark: Bo'limlarni Xavfsiz Montaj Qilish (/tmp, /var/tmp da noexec, nosuid, nodev)
**Tavsif:** Xakerlar yuklagan zararli binar dasturlar va skriptlarning `/tmp` yoki `/var/tmp` orqali to'g'ridan-to'g'ri ishga tushib ketishini to'xtatish uchun bo'limlarni xavfsiz opsiyalar bilan qayta montaj qiling.
**Talablar:** /etc/fstab tahlili, mount -o remount,noexec,nosuid,nodev, tmpfs konfiguratsiyasi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS Benchmark 1.1: Vaqtinchalik Bo'limlarni Hardening Qilish
set -euo pipefail

echo "=========================================================="
echo "[*] CIS Hardening: /tmp va /dev/shm bo'limlari himoyalanmoqda..."
echo "=========================================================="

# 1. /tmp uchun tmpfs konfiguratsiyasini systemd da yoqish
if systemctl is-enabled tmp.mount >/dev/null 2>&1; then
    echo "[+] tmp.mount allaqachon faol."
else
    echo "[*] tmp.mount xizmati faollashtirilmoqda..."
    systemctl unmask tmp.mount 2>/dev/null || true
    systemctl enable --now tmp.mount 2>/dev/null || true
fi

# 2. /etc/fstab faylida /tmp va /dev/shm opsiyalarini qat'iylashtirish
# noexec:  Ushbu bo'limda hech qanday binar faylni ishga tushirib bo'lmaydi
# nosuid:  SUID/SGID huquqlari ishlamaydi (Privilege Escalation oldini oladi)
# nodev:   Maxsus apparat qurilma fayllari (device nodes) yaratish taqiqlanadi

FSTAB="/etc/fstab"
cp "$FSTAB" "${FSTAB}.bak_$(date +%s)"

# /dev/shm bo'limi tekshiruvi
if grep -q "[[:space:]]/dev/shm[[:space:]]" "$FSTAB"; then
    sed -i 's|.*[[:space:]]/dev/shm[[:space:]].*|tmpfs /dev/shm tmpfs defaults,noexec,nosuid,nodev 0 0|' "$FSTAB"
else
    echo "tmpfs /dev/shm tmpfs defaults,noexec,nosuid,nodev 0 0" >> "$FSTAB"
fi

# Qayta montaj qilish
mount -o remount,noexec,nosuid,nodev /dev/shm 2>/dev/null || true
if mountpoint -q /tmp; then
    mount -o remount,noexec,nosuid,nodev /tmp 2>/dev/null || true
fi

echo "[+] Muvaffaqiyatli! /tmp va /dev/shm bo'limlarida kod bajarish (noexec) taqiqlandi."
mount | grep -E "(/tmp|/dev/shm)"

```
**Tushuntirish:** Buzg'unchilar veb-zaifliklar orqali serverga kirganda dastlabki ekspluatatsiyani har doim barcha yoza oladigan `/tmp` katalogiga yuklaydi va ishga tushiradi. `noexec` opsiyasi Linux yadrosiga ushbu katalogdagi har qanday faylga `execve` chaqiruvini rad etishni buyuradi (Permission Denied).

---

### Topshiriq #1152: CIS Benchmark: Keraksiz Qadimgi Fayl Tizimlari Drayverlarini Qora Ro'yxatga Olish
**Tavsif:** Linux yadrosidagi eskirgan va tekshirilmagan fayl tizimlari drayverlaridagi (cramfs, freevxfs, jffs2, hfs, hfsplus, squashfs, udf) zaifliklarni bartaraf qilish uchun ularni bloklang.
**Talablar:** /etc/modprobe.d/cis.conf yaratish, install <fs> /bin/false, rmmod orqali xotiradan tozalash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS Benchmark 1.1.1: Xavfli Fayl Tizimlari Drayverlarini O'chirish
set -euo pipefail

CIS_MODPROBE_FILE="/etc/modprobe.d/cis_filesystem_blacklist.conf"

echo "[*] Keraksiz fayl tizimlari yadrodan bloklanmoqda..."

UNUSED_FS=(
    "cramfs"
    "freevxfs"
    "jffs2"
    "hfs"
    "hfsplus"
    "squashfs"
    "udf"
)

cat <<'EOF' > "$CIS_MODPROBE_FILE"
# CIS Security Standard: Keraksiz fayl tizimlari bloklandi
EOF

for fs in "${UNUSED_FS[@]}"; do
    # 'install <modul> /bin/false' buyrug'i drayver chaqirilganda nol natija beradi
    echo "install $fs /bin/false" >> "$CIS_MODPROBE_FILE"
    echo "blacklist $fs" >> "$CIS_MODPROBE_FILE"
    
    # Agar xotirada yuklangan bo'lsa darhol chiqaramiz
    rmmod "$fs" 2>/dev/null || true
done

echo "[+] Barcha keraksiz drayverlar /etc/modprobe.d da bloklandi!"
cat "$CIS_MODPROBE_FILE"

```
**Tushuntirish:** Linux yadrosida minglab drayverlar mavjud bo'lib, buzg'unchi USB yoki maxsus soxtalashtirilgan disk tasvirini (disk image) montaj qilish orqali eski fayl tizimlari kodidagi bufer to'lib ketishi (Buffer Overflow) orqali Root huquqini qo'lga kiritishi mumkin. Uni `install /bin/false` qilish yadro darajasida yuklanishni to'xtatadi.

---

### Topshiriq #1153: Yadro Xavfsizligi: To'liq ASLR va Ptrace Cheklovlarini Majburlash
**Tavsif:** Xotiradagi bufer to'lib toshishi (Buffer Overflow va ROP) hujumlariga qarshi ASLR (Address Space Layout Randomization) ni maksimal 2-darajaga ko'taring va jarayonlar xotirasini ptrace orqali o'g'irlashni cheklang.
**Talablar:** kernel.randomize_va_space=2, kernel.yama.ptrace_scope=2, sysctl -p.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - ASLR va Yama Ptrace Xotira Himoyasi
set -euo pipefail

SYSCTL_CONF="/etc/sysctl.d/99-security-memory.conf"

echo "[*] Xotira darajasidagi kiberhimoya (ASLR + Yama) faollashtirilmoqda..."

cat <<'EOF' > "$SYSCTL_CONF"
# CIS 1.5.3: ASLR (Address Space Layout Randomization) maksimal darajaga sozlash
# 2 = Stack, VDSO, Shared Memory va Data Segmentlarni tasodifiy joylashtirish
kernel.randomize_va_space = 2

# Yama LSM: ptrace orqali boshqa dasturlarning xotirasini o'qishni taqiqlash
# 1 = Faqat bevosita ajdod (parent) jarayongina ruxsat oladi
# 2 = Faqat root (CAP_SYS_PTRACE) ruxsati bilan
kernel.yama.ptrace_scope = 2

# BPF JIT kuchaytirish (Spectre/Meltdown himoyasi)
net.core.bpf_jit_harden = 2

# dmesg jurnalini oddiy foydalanuvchilardan yashirish (Kernel manzil sizishini oldini oladi)
kernel.dmesg_restrict = 1

# Kptr cheklovi: /proc/kallsyms da yadro ko'rsatkichlarini yashirish
kernel.kptr_restrict = 2
EOF

# Qoidalarni yadroga yuklaymiz
sysctl -p "$SYSCTL_CONF" > /dev/null

echo "[+] ASLR va Ptrace himoyasi yadroda faollashtirildi!"
echo "kernel.randomize_va_space = $(sysctl -n kernel.randomize_va_space)"
echo "kernel.yama.ptrace_scope  = $(sysctl -n kernel.yama.ptrace_scope)"

```
**Tushuntirish:** ASLR xotiradagi stek (stack), kutubxonalar (libc) va ma'lumotlar manzilini har safar dastur ishga tushganda o'zgartiradi. Natijada xakerlar Return-Oriented Programming (ROP) hujumlarida aniq xotira manzilini topa olmaydi va dastur qulab tushadi (Segfault).

---

### Topshiriq #1154: Yadro Tarmoq Parametrlari Hardening: SYN Cookies, Redirects va Martian Logging
**Tavsif:** Linux serverini TCP darajasidagi DDoS va yo'naltirish (Man-in-the-Middle) hujumlaridan himoya qilish uchun barcha yadro tarmoq flaglarini CIS standartlariga muvofiq sozlang.
**Talablar:** tcp_syncookies=1, accept_redirects=0, send_redirects=0, log_martians=1, rp_filter=1.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS Benchmark 3.1 & 3.2: Tarmoq Yadrosi Parametrlari
set -euo pipefail

SYSCTL_NET="/etc/sysctl.d/99-security-network.conf"

echo "[*] Tarmoq xavfsizligi sysctl konfiguratsiyasi kiritilmoqda..."

cat <<'EOF' > "$SYSCTL_NET"
# 1. SYN Flood hujumlariga qarshi TCP SYN Cookies ni yoqish
net.ipv4.tcp_syncookies = 1

# 2. ICMP Redirect paketlarini qabul qilmaslik (MITM hujumlarini to'xtatadi)
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# 3. Router bo'lmagan server uchun ICMP Redirect jo'natishni o'chirish
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# 4. IP Source Routing (Paketning o'z yo'lini belgilashi) ni rad etish
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0

# 5. Soxta va noto'g'ri (Martian / Spoofed) paketlarni logga yozish
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1

# 6. ICMP Broadcast Ping (Smurf DDoS) so'rovlariga javob bermaslik
net.ipv4.icmp_echo_ignore_broadcasts = 1

# 7. Noto'g'ri ICMP xatolik javoblarini e'tiborsiz qoldirish
net.ipv4.icmp_ignore_bogus_error_responses = 1
EOF

sysctl -p "$SYSCTL_NET" > /dev/null
echo "[+] Tarmoq yadro hardening qoidalari muvaffaqiyatli qo'llandi!"

```
**Tushuntirish:** ICMP Redirect paketlari xakerga tarmoq trafigini o'ziga burib olishga (Route Poisoning) imkon beradi. `accept_redirects=0` qilish orqali server faqat o'zining mahalliy shlyuziga ishonadi va begona router so'rovlarini rad etadi.

---

### Topshiriq #1155: IP Spoofing dan Himoyalanish: Reverse Path Filtering (rp_filter) ni Majburlash
**Tavsif:** Serverga soxta boshlang'ich manzil bilan (IP Spoofing) kelayotgan paketlarni kirish interfeysiga qarab darhol tashlab yuboruvchi qat'iy Reverse Path Filtering sozlamasini bajaring.
**Talablar:** net.ipv4.conf.all.rp_filter = 1, default.rp_filter = 1, mavjud interfeyslarni tekshirish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Qat'iy Reverse Path Filtering (Strict Anti-Spoofing)
set -euo pipefail

SYSCTL_RP="/etc/sysctl.d/99-anti-spoofing.conf"

echo "[*] Reverse Path Filtering (rp_filter=1) sozlanmoqda..."

cat <<'EOF' > "$SYSCTL_RP"
# 1 = Qat'iy rejim (Strict Mode): Paket kelgan interfeys bilan marshrutlash jadvaliga qat'iy mos bo'lishi shart
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
EOF

# Tizimdagi barcha mavjud tarmoq kartalari uchun yoqamiz
for iface in /proc/sys/net/ipv4/conf/*/rp_filter; do
    echo 1 > "$iface" 2>/dev/null || true
done

sysctl -p "$SYSCTL_RP" > /dev/null
echo "[+] IP Spoofing ga qarshi Strict Reverse Path Filtering yoqildi!"

```
**Tushuntirish:** Reverse Path Filtering (RFC 3704) Linux yadrosiga har bir paketni teskari tekshirishni buyuradi: 'Agar men ushbu manba IP ga javob qaytarsam, u aynan shu kelgan interfeysdan chiqib ketadimi?' Agar yo'q bo'lsa (demak paket soxtalashtirilgan), paket darhol yadroda yo'q qilinadi.

---

### Topshiriq #1156: Core Dumps va SUID Core Dumps ni Butunlay O'chirish
**Tavsif:** Dasturlar qulaganda (crash) ularning operativ xotirasi (parollar, shifrlash kalitlari, tokenlar) diskka `.dump` bo'lib yozilib qolishini va xakerlar uni o'qib olishini to'xtating.
**Talablar:** fs.suid_dumpable = 0, /etc/security/limits.conf da '* hard core 0', systemd-coredump ni o'chirish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 1.5.1: Xavfli Core Dump Fayllarini Butunlay O'chirish
set -euo pipefail

echo "[*] Core dump fayllari tizim darajasida taqiqlanmoqda..."

# 1. Yadro darajasida SUID dasturlar dumpini o'chirish
SYSCTL_DUMP="/etc/sysctl.d/99-disable-coredump.conf"
cat <<'EOF' > "$SYSCTL_DUMP"
fs.suid_dumpable = 0
EOF
sysctl -p "$SYSCTL_DUMP" > /dev/null

# 2. /etc/security/limits.conf da barcha foydalanuvchilar uchun core limitini 0 qilish
LIMITS_FILE="/etc/security/limits.d/99-disable-core.conf"
cat <<'EOF' > "$LIMITS_FILE"
* hard core 0
* soft core 0
EOF

# 3. systemd-coredump demoni mavjud bo'lsa uni o'chirish
if systemctl is-active systemd-coredump.socket >/dev/null 2>&1; then
    systemctl stop systemd-coredump.socket 2>/dev/null || true
    systemctl disable systemd-coredump.socket 2>/dev/null || true
fi

echo "[+] Core dump to'liq o'chirildi! Xotira sizib chiqishi xavfi bartaraf etildi."

```
**Tushuntirish:** Agar serverda ishlayotgan Nginx yoki OpenSSH dasturiga tajovuzkor sun'iy xato (Segmentation fault) bersa, tizim operativ xotira holatini diskka yozib qo'yadi. Agar tajovuzkor ushbu faylni o'qiy olsa, xotiradagi barcha foydalanuvchilar parollari va TLS maxfiy kalitlarini o'g'irlashi mumkin.

---

### Topshiriq #1157: Tizimdagi Xavfli SUID/SGID Fayllarni Skanerlash va Huquqlarini Pasaytirish
**Tavsif:** Oddiy foydalanuvchiga Root huquqlarini beruvchi xavfli yoki keraksiz SUID bitlari qo'yilgan (masalan, `pkexec`, `chfn`, `chsh`, `traceroute`) dasturlarni topib, ortiqcha bitlarni olib tashlang.
**Talablar:** find / -perm -4000 -o -perm -2000, ruxsat berilgan dasturlar oq ro'yxati, chmod u-s,g-s.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - SUID/SGID Privilegiyalar Auditi va Tozalash
set -euo pipefail

SCAN_LOG="/var/log/suid_audit_$(date +%Y%m%d).log"

echo "=========================================================="
echo "[*] Tizimdagi barcha SUID/SGID fayllar skanerlanmoqda..."
echo "=========================================================="

# Ruxsat berilgan standart SUID utilitalari (Whitelist)
ALLOWED_SUID=(
    "/usr/bin/sudo"
    "/usr/bin/passwd"
    "/usr/bin/su"
    "/usr/bin/newgrp"
    "/usr/bin/gpasswd"
)

# 1. Barcha SUID (4000) va SGID (2000) fayllarni qidiramiz
FOUND_FILES=$(find / -xdev \( -perm -4000 -o -perm -2000 \) -type f 2>/dev/null)

echo "$FOUND_FILES" > "$SCAN_LOG"
echo "[+] Jami topildi: $(wc -l < "$SCAN_LOG") ta SUID/SGID fayl."

# 2. Xavfli deb hisoblangan keraksiz dasturlardan SUID bitini olib tashlaymiz
POTENTIALLY_DANGEROUS=(
    "/usr/bin/chfn"
    "/usr/bin/chsh"
    "/usr/bin/traceroute6.iputils"
    "/usr/bin/wall"
    "/usr/bin/write"
)

for bin in "${POTENTIALLY_DANGEROUS[@]}"; do
    if [[ -f "$bin" && ( -u "$bin" || -g "$bin" ) ]]; then
        echo "[*] Xavfli SUID olib tashlanmoqda: $bin"
        chmod u-s,g-s "$bin"
    fi
done

echo "[+] SUID auditi tugadi. To'liq ro'yxat: $SCAN_LOG"

```
**Tushuntirish:** SUID (Set User ID) biti yoqilgan faylni har qanday oddiy foydalanuvchi ishga tushirsa, dastur Root huquqi bilan ishlaydi. 2021-yildagi mashhur Baron Samedit (sudo) va PwnKit (pkexec) kabi xavfli 0-day zaifliklari aynan keraksiz SUID fayllari orqali amalga oshirilgan.

---

### Topshiriq #1158: Dunyoga Ochiq (World-Writable) Fayllar va Kataloglarga Sticky-Bit Qo'yish
**Tavsif:** Tizimdagi istalgan foydalanuvchi yozishi mumkin bo'lgan kataloglarda begonalar bir-birining faylini o'chirib yoki o'zgartirib qo'ymasligi uchun Sticky-Bit (`+t`) o'rnatuvchi avtomatizatsiya tuzing.
**Talablar:** find / -type d -perm -0002, sticky-bit tekshiruvi (! -perm -1000), chmod +t qo'llash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 1.1.10: World-Writable Kataloglarda Sticky-Bit Nazorati
set -euo pipefail

echo "[*] Dunyoga ochiq (World-Writable) kataloglar qidirilmoqda..."

# -perm -0002: Barcha yoza oladigan (others write)
# ! -perm -1000: Lekin Sticky-Bit yoqilmagan bo'limlar
VULNERABLE_DIRS=$(find / -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null || true)

if [[ -z "$VULNERABLE_DIRS" ]]; then
    echo "[+] A'lo! Barcha ochiq kataloglarda Sticky-Bit allaqachon to'g'ri sozlangan."
else
    echo "[!] Quyidagi kataloglarda Sticky-Bit yo'q ekanligi aniqlandi:"
    echo "$VULNERABLE_DIRS"
    
    echo "$VULNERABLE_DIRS" | while read -r dir; do
        if [[ -n "$dir" && -d "$dir" ]]; then
            echo "[*] Sticky-Bit qo'shilmoqda: $dir"
            chmod +t "$dir"
        fi
    done
    echo "[+] Barcha xavfli kataloglar tuzatildi!"
fi

```
**Tushuntirish:** Agar katalog hammaga ochiq (777) bo'lsa va unda Sticky-Bit (`1777` yoki `+t`) bo'lmasa, oddiy foydalanuvchi boshqa foydalanuvchilarning yoki xizmatlarning fayllarini bemalol o'chirib tashlashi yoki simvolik havola (Symlink Attack) bilan almashtirib qo'yishi mumkin.

---

### Topshiriq #1159: Egasi Yo'q (Orphaned / No-User / No-Group) Fayllarni Audit Qilish va Tozalash
**Tavsif:** Foydalanuvchi tizimdan o'chirilgandan so'ng xotirada qolib ketgan, hech kimga tegishli bo'lmagan fayllarni yangi yaratilgan foydalanuvchi o'zlashtirib olishini oldini oling.
**Talablar:** find / -nouser -o -nogroup, xavfsiz karantin katalogiga ko'chirish yoki rootga biriktirish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 6.1.11 & 6.1.12: Egasi Yo'q (Orphaned) Fayllar Auditi
set -euo pipefail

ORPHAN_LOG="/var/log/orphaned_files_$(date +%Y%m%d).log"

echo "[*] Tizimdagi egasiz fayllar (nouser / nogroup) tekshirilmoqda..."

# /proc, /sys kabi dinamik virtual bo'limlarni qoldirib, haqiqiy disklarni tekshiramiz
ORPHANS=$(find / -xdev \( -nouser -o -nogroup \) 2>/dev/null || true)

if [[ -n "$ORPHANS" ]]; then
    echo "$ORPHANS" > "$ORPHAN_LOG"
    COUNT=$(wc -l < "$ORPHAN_LOG")
    echo "[!] Diqqat: Tizimda ${COUNT} ta egasiz fayl topildi!"
    echo "[*] Xavfsizlik choralari: Egasiz fayllar root:root ga biriktirilmoqda..."

    echo "$ORPHANS" | while read -r item; do
        if [[ -e "$item" ]]; then
            chown root:root "$item"
        fi
    done
    echo "[+] Barcha egasiz fayllar xavfsiz holda root ga o'tkazildi. Jurnal: $ORPHAN_LOG"
else
    echo "[+] Tizimda hech qanday egasiz fayl topilmadi. Tizim toza!"
fi

```
**Tushuntirish:** Agar serverdan `developer1` foydalanuvchisi o'chirilsa, uning UID raqamiga (masalan 1005) tegishli fayllar diskda egasiz qoladi. Keyinchalik yangi foydalanuvchi ro'yxatdan o'tib unga o'sha 1005 UID berilsa, u avtomatik ravishda eski fayllarga ega bo'lib qoladi. Shu sababli ular `root:root` ga o'tkazilishi shart.

---

### Topshiriq #1160: GRUB Bootloader ni Parol Bilan Himoyalash va Single-User Rejimini Qulflash
**Tavsif:** Serverga jismoniy yoki virtual konsol orqali kirgan buzg'unchi GRUB menyusida `init=/bin/sh` orqali parolsiz to'g'ridan-to'g'ri Root bo'lib kirib olishining oldini olish uchun GRUB ga PBKDF2 shifrlangan parol o'rnating.
**Talablar:** grub-mkpasswd-pbkdf2, /etc/grub.d/40_custom da superusers sozlash, update-grub.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 1.4.1: GRUB Bootloader Xavfsizlik Paroli
set -euo pipefail

GRUB_CUSTOM="/etc/grub.d/40_custom"

echo "=========================================================="
echo "[*] GRUB Bootloader Parol Himoyasi Konfiguratsiyasi"
echo "=========================================================="

ADMIN_USER="khorazmiy_admin"
# Oldindan hisoblangan xavfsiz PBKDF2 paroli (grub-mkpasswd-pbkdf2 orqali hosil qilinadi)
# Namuna paroli: 'GrubSecurePass2026!'
GRUB_HASH="grub.pbkdf2.sha512.10000.C39B7C074C655B81001E854D265DA4F518DDAEE00B7AA4C3C914EEAE82B2CE83E7D566B38644A14E304856614138676E4B4C18EC3B9DDFBC87326D16F0BD24A8.C3DDF7607CA88BE803E55EE3432B665E4AC6FF9A564A27B08B9F51B27B504C06FDE934B8BA74EE7C6BE9044A8C4B598F53FF98C14A2925232DE67E96CCDF1C42"

cat <<EOF >> "$GRUB_CUSTOM"

# CIS Benchmark: GRUB Superuser Himoyasi
set superusers="${ADMIN_USER}"
password_pbkdf2 ${ADMIN_USER} ${GRUB_HASH}
EOF

# GRUB konfiguratsiya faylining o'qish huquqini faqat rootga beramiz (600)
chmod 600 "$GRUB_CUSTOM"
if [[ -f "/boot/grub/grub.cfg" ]]; then
    chmod 600 /boot/grub/grub.cfg
fi

echo "[+] GRUB konfiguratsiyasi yangilanmoqda (update-grub)..."
if command -v update-grub >/dev/null 2>&1; then
    update-grub > /dev/null 2>&1 || true
fi

echo "[+] GRUB xavfsiz parol bilan muvaffaqiyatli qulflandi!"

```
**Tushuntirish:** Agar server qayta ishga tushirilganda GRUB menyusida 'e' harfi bosilsa, yadro parametrlariga `rw init=/bin/bash` yozib, hech qanday parol so'ramasdan darhol Root konsolga kirish mumkin. GRUB PBKDF2 paroli ushbu menyuni tahrirlashni butunlay to'xtatadi.

---

### Topshiriq #1161: CIS SSH Hardening: Zaif Algoritmlarni Butunlay O'chirish
**Tavsif:** SSH konfiguratsiyasida eskirgan zaif shifrlash usullarini (3DES, CBC, RC4, MD5, SHA1) olib tashlab, faqat eng zamonaviy ChaCha20-Poly1305 va Curve25519 algoritmlarini majburiy qiling.
**Talablar:** Ciphers, MACs, KexAlgorithms parametrlarini sozlash, sshd -t sintaktik tekshiruv, sshd restart.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 5.2.14: SSH Kriptografik Kuchaytirish (Crypto Hardening)
set -euo pipefail

SSHD_HARDENING="/etc/ssh/sshd_config.d/99-cis-crypto.conf"
mkdir -p /etc/ssh/sshd_config.d

echo "[*] SSHD zamonaviy kuchli kriptografiya parametrlariga o'tkazilmoqda..."

cat <<'EOF' > "$SSHD_HARDENING"
# Faqat kuchli va xavfsiz Kalit Almashinuvi (Key Exchange) algoritmlari
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512

# Faqat Authenticated Ciphers (CBC rejimlari butunlay taqiqlanadi)
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com

# Xavfsiz Xabarlar Haqiqiyligi Kodlari (MAC)
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com
EOF

# Sintaksisni tekshirish
if sshd -t; then
    echo "[+] SSHD konfiguratsiyasi to'g'ri. Xizmat qayta yuklanmoqda..."
    systemctl reload sshd || systemctl reload ssh || true
    echo "[+] SSH faqat ChaCha20 va Curve25519 orqali ishlaydi!"
else
    echo "[!] Xatolik: sshd sintaksisi xato!"
    rm -f "$SSHD_HARDENING"
    exit 1
fi

```
**Tushuntirish:** CBC (Cipher Block Chaining) rejimlarida 'Plaintext Recovery' va Terrapin hujumi kabi tarmoq orqali sessiyani buzish zaifliklari mavjud. `chacha20-poly1305` va `aes-gcm` esa har bir paketni mustaqil autentifikatsiya qiluvchi (AEAD) zamonaviy standartdir.

---

### Topshiriq #1162: SSH Root Login va Parol Orqali Kirishni To'liq Taqiqlash
**Tavsif:** Brute-force hujumlarining 99% ini to'xtatish uchun SSH da parol orqali kirishni o'chirib, faqatgina Ed25519 yoki RSA ommaviy kalitlari bilan kirishni majburiy qiling.
**Talablar:** PermitRootLogin no, PasswordAuthentication no, KbdInteractiveAuthentication no, PubkeyAuthentication yes.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 5.2.8 & 5.2.10: SSH Parolsiz Qat'iy Kalitli Kirish
set -euo pipefail

CONF_FILE="/etc/ssh/sshd_config.d/99-disable-passwords.conf"

echo "[*] SSH da parollar va Root kirishi taqiqlanmoqda..."

cat <<'EOF' > "$CONF_FILE"
# Root foydalanuvchisi to'g'ridan-to'g'ri SSH orqali kira olmaydi
PermitRootLogin no

# Parol bilan kirishni butunlay o'chirish
PasswordAuthentication no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no

# Faqat kriptografik ommaviy kalitlar orqali kirish
PubkeyAuthentication yes

# Bo'sh parollarni taqiqlash
PermitEmptyPasswords no
EOF

if sshd -t; then
    systemctl reload sshd || systemctl reload ssh || true
    echo "[+] Muvaffaqiyatli! Endi SSH orqali faqat shaxsiy kalit (SSH Key) bilan kirish mumkin."
else
    echo "[XATO] SSH konfiguratsiyasida xatolik yuz berdi!"
    rm -f "$CONF_FILE"
    exit 1
fi

```
**Tushuntirish:** Internetdagi botnetlar doimiy ravishda 22-portga `root` foydalanuvchisi va oddiy parollarni (admin, 123456, root2024) yuborib turadi. Parol autentifikatsiyasini o'chirish ushbu hujum vektorini 100% samarasiz qiladi.

---

### Topshiriq #1163: SSH FIDO2 Hardware Token (YubiKey ed25519-sk) orqali Kirish
**Tavsif:** Fizik xavfsizlik kalitlari (YubiKey FIDO2) yordamida, faqat jismoniy kalit tugmachasini qo'l bilan bosgandagina (User Presence) serverga SSH kirishga ruxsat beruvchi apparat darajasidagi autentifikatsiyani sozlang.
**Talablar:** ssh-keygen -t ed25519-sk, Security Key OpenSSH 8.2+ talabi, authorized_keys sozlamalari.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - SSH FIDO2 Hardware Key (ed25519-sk) Konfiguratsiyasi
set -euo pipefail

echo "=========================================================="
echo "[*] FIDO2 / U2F Hardware SSH Kalitlari Integratsiyasi"
echo "=========================================================="

# Foydalanuvchi kompyuterida FIDO2 kalit yasash namunasi:
# ssh-keygen -t ed25519-sk -O resident -O verify-required -C "yubikey_admin@khorazmiy.uz"

TARGET_USER="sysadmin"
TARGET_HOME=$(getent passwd "$TARGET_USER" | cut -d: -f6 || echo "/home/$TARGET_USER")
SSH_DIR="${TARGET_HOME}/.ssh"
AUTH_KEYS="${SSH_DIR}/authorized_keys"

mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

# ed25519-sk tipidagi ommaviy kalit namunasi:
# sk-ssh-ed25519@openssh.com AAAAGnNrLXNzaC1lZDI1NTE5QG9wZW5zc2guY29tAAAAI...
echo "[*] FIDO2 ommaviy kaliti authorized_keys fayliga biriktirilmoqda..."

# 'verify-required' bayrog'i: Server har doim apparat kalitda PIN kod terilganligini talab qiladi
SAMPLE_FIDO2_KEY="sk-ssh-ed25519@openssh.com AAAAGnNrLXNzaC1lZDI1NTE5QG9wZW5zc2guY29tAAAAIBB123456789012345678901234567890123456789012 yubikey_hardware_key"

echo "$SAMPLE_FIDO2_KEY" >> "$AUTH_KEYS"
chmod 600 "$AUTH_KEYS"
chown -R "$TARGET_USER:$TARGET_USER" "$SSH_DIR" 2>/dev/null || true

echo "[+] FIDO2 Hardware Security Key muvaffaqiyatli ro'yxatga olindi!"

```
**Tushuntirish:** Oddiy SSH xususiy kalitlari (id_rsa) xaker tomonidan o'g'irlanishi mumkin. `ed25519-sk` kalitida esa maxfiy kalit YubiKey mikrosxemasidan HECH QACHON tashqariga chiqmaydi va serverga kirish uchun odam jismonan kalitga barmog'i bilan teginishi shart.

---

### Topshiriq #1164: SSH Certificate Authority (SSH CA) Tizimini O'rnatish
**Tavsif:** Yuzlab serverlarga doimiy `authorized_keys` tarqatish o'rniga, markaziy SSH CA orqali xodimlarga 8 soatlik vaqtinchalik kriptografik sertifikatlar beruvchi CA infratuzilmasini yarating.
**Talablar:** ssh-keygen -f ca_key, TrustedUserCAKeys sozlamasi, ssh-keygen -s ca_key -V +8h bilan imzolash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Markaziy SSH Certificate Authority (CA) Tizimi
set -euo pipefail

CA_DIR="/etc/ssh/ca"
mkdir -p "$CA_DIR"

echo "[*] SSH CA Master kaliti yaratilmoqda..."
if [[ ! -f "$CA_DIR/ca_user_key" ]]; then
    ssh-keygen -t ed25519 -f "$CA_DIR/ca_user_key" -N "" -C "Khorazmiy_SSH_CA"
    chmod 600 "$CA_DIR/ca_user_key"
    chmod 644 "$CA_DIR/ca_user_key.pub"
fi

# 1. Barcha serverlarga ushbu CA ommaviy kalitiga ishonishni buyuramiz
TRUSTED_CA_FILE="/etc/ssh/trusted_user_ca_keys.pub"
cp "$CA_DIR/ca_user_key.pub" "$TRUSTED_CA_FILE"
chmod 644 "$TRUSTED_CA_FILE"

cat <<EOF > /etc/ssh/sshd_config.d/99-ssh-ca.conf
TrustedUserCAKeys ${TRUSTED_CA_FILE}
EOF

# 2. Xodim uchun 8 soatlik muddatli sertifikat imzolash namunasi:
echo "[*] Muhandis uchun 8 soatlik sertifikat chiqarish namoyishi:"
USER_PUB_KEY="/tmp/dummy_user.pub"
ssh-keygen -t ed25519 -f "/tmp/dummy_user" -N "" -C "dev@khorazmiy.uz" >/dev/null 2>&1

ssh-keygen -s "$CA_DIR/ca_user_key" \
    -I "developer_alisher" \
    -n "ubuntu,sysadmin" \
    -V "+8h" \
    "$USER_PUB_KEY"

echo "[+] 8 soatlik sertifikat imzolandi: /tmp/dummy_user-cert.pub"
ssh-keygen -L -f "/tmp/dummy_user-cert.pub"

```
**Tushuntirish:** SSH sertifikatlari xuddi TLS veb sertifikatlari kabi ishlaydi. Xodim ishdan bo'shasa, 1000 ta serverdan kalitni o'chirish shart emas; berilgan sertifikat 8 soatdan keyin avtomatik ravishda o'z kuchini yo'qotadi.

---

### Topshiriq #1165: SSH 2FA/MFA: Google Authenticator (PAM TOTP) Bilan Kirishni Kuchaytirish
**Tavsif:** SSH kalitiga qo'shimcha ravishda xodimdan telefondagi Google Authenticator 6 xonali kodini kiritishni talab qiluvchi ikki faktorli autentifikatsiya (2FA) tizimini o'rnating.
**Talablar:** libpam-google-authenticator, /etc/pam.d/sshd da auth required, AuthenticationMethods publickey,keyboard-interactive.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - SSH + Google Authenticator PAM 2FA/MFA
set -euo pipefail

echo "[*] SSH uchun Google Authenticator (TOTP) sozlanmoqda..."

# 1. /etc/pam.d/sshd konfiguratsiyasiga TOTP modulini qo'shamiz
PAM_SSHD="/etc/pam.d/sshd"
if ! grep -q "pam_google_authenticator.so" "$PAM_SSHD"; then
    echo "auth required pam_google_authenticator.so nullok" >> "$PAM_SSHD"
fi

# 2. sshd_config da kalit VA kod ikkalasini majburlash:
cat <<'EOF' > /etc/ssh/sshd_config.d/99-mfa.conf
# Ikki faktorli autentifikatsiya usullari:
# Foydalanuvchi DASTLAB SSH kalitini beradi, SO'NGRA 2FA kodini kiritadi
AuthenticationMethods publickey,keyboard-interactive:pam
KbdInteractiveAuthentication yes
EOF

if sshd -t; then
    systemctl reload sshd || systemctl reload ssh || true
    echo "[+] SSH MFA muvaffaqiyatli sozlandi!"
    echo "[*] Foydalanuvchi o'z profilida 'google-authenticator' buyrug'ini ishga tushirishi kerak."
else
    echo "[!] Xatolik yuz berdi!"
fi

```
**Tushuntirish:** `AuthenticationMethods publickey,keyboard-interactive` buyrug'i bir vaqtning o'zida ikkita faktorni talab qiladi: 'Sizda nima bor?' (SSH shaxsiy kaliti) va 'Siz nimani bilasiz/egasisiz?' (Telefondagi bir martalik TOTP kod). Bu kompyuter buzilsa ham serverga kirishni to'xtatadi.

---

### Topshiriq #1166: SSH MaxAuthTries va ClientAlive Bo'sh Sessiyalarni Uzish
**Tavsif:** Bitta ulanishda 3 martadan ortiq xato urinishlarni rad etish va 10 daqiqa foydalanilmagan bo'sh SSH sessiyalarni avtomatik uzuvchi Keep-Alive va Urinishlar chegarasini sozlang.
**Talablar:** MaxAuthTries 3, ClientAliveInterval 300, ClientAliveCountMax 2, LoginGraceTime 60.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 5.2.5 & 5.2.13: SSH Sessiya Vaqti va Urinishlar Nazorati
set -euo pipefail

CONF="/etc/ssh/sshd_config.d/99-session-limits.conf"

echo "[*] SSH bo'sh sessiyalar va urinishlar chegarasi o'rnatilmoqda..."

cat <<'EOF' > "$CONF"
# Bitta ulanishda ko'pi bilan 3 ta urinishga ruxsat (Brute-force ga qarshi)
MaxAuthTries 3

# Parol/kalit kiritish uchun maksimal kutish vaqti: 60 soniya
LoginGraceTime 60

# Har 300 soniyada (5 daqiqa) mijozga signal yuboriladi
ClientAliveInterval 300

# Agar 2 marta javob bermasa (jami 10 daqiqa), sessiya uziladi
ClientAliveCountMax 2

# Bir vaqtda ochilishi mumkin bo'lgan maksimal ulanishlar
MaxStartups 10:30:100
EOF

if sshd -t; then
    systemctl reload sshd || systemctl reload ssh || true
    echo "[+] SSH sessiya muddatlari muvaffaqiyatli qat'iylashtirildi!"
fi

```
**Tushuntirish:** Xakerlar ko'pincha bitta ochiq TCP ulanish orqali yuzlab parollarni tekshirishga urinadi. `MaxAuthTries 3` har 3 ta xatodan keyin soketni uzadi. `ClientAliveInterval` esa admin kompyuterini qulflamay ketgan holatlarda tarmoq xavfsizligini ta'minlaydi.

---

### Topshiriq #1167: SSH Kirish Banneri va Huquqiy Ogohlantirish (Legal Disclaimer)
**Tavsif:** Serverga ruxsatsiz kiruvchilarni qonuniy javobgarlikka tortish va tajovuzkorlarga operatsion tizim versiyasini bildirmaslik uchun xavfsiz `/etc/issue.net` bannerini o'rnating.
**Talablar:** Banner /etc/issue.net, OS versiyalari ko'rsatilmasligi, CIS talablariga mos ogohlantirish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 1.7.2: SSH Huquqiy Ogohlantirish Banneri
set -euo pipefail

BANNER_FILE="/etc/issue.net"

echo "[*] Maxfiy server xavfsizlik banneri o'rnatilmoqda..."

cat <<'EOF' > "$BANNER_FILE"
*******************************************************************************
                          DIQQAT: XUSUSIY TIZIM!
 Bu server "Khorazmiy AI" korporativ tarmog'ining himoyalangan resursidir.
 Faqat rasmiy ruxsat berilgan xodimlarga kirish huquqi mavjud.
 Barcha harakatlar (IP, buyruqlar, sessiyalar) 24/7 qat'iy nazorat ostida.
 Ruxsatsiz kirish urinishlari O'zbekiston Respublikasi Jinoyat Kodeksining
 tegishli moddalariga muvofiq jinoiy javobgarlikka sabab bo'ladi.
*******************************************************************************
EOF

# sshd_config da bannerni yoqamiz
cat <<EOF > /etc/ssh/sshd_config.d/99-banner.conf
Banner ${BANNER_FILE}
EOF

if sshd -t; then
    systemctl reload sshd || systemctl reload ssh || true
    echo "[+] Xavfsizlik banneri faollashtirildi!"
fi

```
**Tushuntirish:** Ko'pgina default Linux distrolari SSH ga kirishda 'Ubuntu 22.04 LTS' deb OS versiyasini ko'rsatadi, bu esa xakerga qaysi kernel zaifligini ishlatishni aytib beradi. Maxsus huquqiy banner esa sud jarayonlarida dalil sifatida muhim ahamiyatga ega.

---

### Topshiriq #1168: SSH AllowUsers va AllowGroups Bilan Faqat Belgilangan Guruhga Ruxsat Berish
**Tavsif:** Tizimda mavjud bo'lgan 50 ta texnik foydalanuvchilar (www-data, daemon, postfix) nomidan SSH orqali kirishni to'xtatib, faqat `ssh-admins` guruhi a'zolarigagina ruxsat bering.
**Talablar:** groupadd ssh-admins, AllowGroups ssh-admins, sshd_config tekshiruvi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 5.2.15: SSH Kirish Guruhini Qat'iy Cheklash
set -euo pipefail

ADMIN_GROUP="ssh-admins"

echo "[*] Maxsus SSH ruxsat guruhi sozlanmoqda: ${ADMIN_GROUP}..."

# Guruhni yaratamiz (mavjud bo'lmasa)
if ! getent group "$ADMIN_GROUP" >/dev/null; then
    groupadd "$ADMIN_GROUP"
    echo "[+] ${ADMIN_GROUP} guruhi yaratildi."
fi

# Joriy sudo foydalanuvchisini shu guruhga qo'shamiz (bloklanib qolmaslik uchun!)
CURRENT_USER="${SUDO_USER:-$(whoami)}"
usermod -aG "$ADMIN_GROUP" "$CURRENT_USER"
echo "[+] Foydalanuvchi '${CURRENT_USER}' guruhga qo'shildi."

# sshd konfiguratsiyasi
cat <<EOF > /etc/ssh/sshd_config.d/99-allow-groups.conf
# Faqat ushbu guruh a'zolarigina SSH qila oladi!
AllowGroups ${ADMIN_GROUP}
EOF

if sshd -t; then
    systemctl reload sshd || systemctl reload ssh || true
    echo "[+] SSH ga faqat '${ADMIN_GROUP}' guruhidagilar kira oladi."
else
    echo "[!] Xatolik yuz berdi!"
    rm -f /etc/ssh/sshd_config.d/99-allow-groups.conf
fi

```
**Tushuntirish:** Standart sozlamalarda Linux dagi paroli bor har qanday hisob (masalan postgres yoki test foydalanuvchisi) SSH ga kirishi mumkin. `AllowGroups` oq ro'yxati boshqa barcha xizmat hisoblarini (service accounts) avtomatik tarzda tarmoqdan uzadi.

---

### Topshiriq #1169: SSH Agent Forwarding va X11 Forwarding Xavflarini Neytrallash
**Tavsif:** Xodimlarning kompyuterlaridagi SSH agent kalitlari oraliq bastion serverda buzg'unchilar tomonidan tutilib qolmasligi uchun Agent va X11 Forwarding ni serverda o'chirib qo'ying.
**Talablar:** AllowAgentForwarding no, X11Forwarding no, AllowTcpForwarding no.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 5.2.4 & 5.2.6: SSH Forwarding Xavflarini O'chirish
set -euo pipefail

CONF="/etc/ssh/sshd_config.d/99-disable-forwarding.conf"

echo "[*] SSH Agent va X11 Forwarding xavflari bartaraf etilmoqda..."

cat <<'EOF' > "$CONF"
# SSH Agent orqali kalit sizib chiqishini to'xtatish
AllowAgentForwarding no

# X11 grafik interfeys tunnellashni o'chirish (X11 kiberhujumlarini oldini oladi)
X11Forwarding no

# Keraksiz TCP port tunnellashni cheklash
AllowTcpForwarding no

# Keraksiz StreamLocal (Unix soket) uzatishni to'xtatish
AllowStreamLocalForwarding no
EOF

if sshd -t; then
    systemctl reload sshd || systemctl reload ssh || true
    echo "[+] Barcha xavfli SSH tunnellari va Agent Forwarding to'xtatildi!"
fi

```
**Tushuntirish:** Agar admin xaker buzgan oraliq serverga `ssh -A` (Agent Forwarding) bilan kirsa, xaker serverdagi Unix soket (`/tmp/ssh-XXXX/agent`) orqali adminning barcha boshqa serverlariga uning shaxsiy kalitini o'g'irlamasdan turib kirib keta oladi. `AllowAgentForwarding no` bu xavfni yo'qotadi.

---

### Topshiriq #1170: SSH Portini Standart 22 dan Yashirin Portga Ko'chirish va SELinux Moslashuvi
**Tavsif:** Internetdagi avtomatlashgan skanerlarning 95% e'tiborini chalg'itish uchun SSH portini nostandart 2222-portga ko'chiring va SELinux/Firewall da yangi portga ruxsat bering.
**Talablar:** Port 2222, semanage port -a -t ssh_port_t, ufw/nftables ruxsati.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - SSH Portini Nostandart Xavfsiz Portga Ko'chirish
set -euo pipefail

NEW_SSH_PORT=2222

echo "[*] SSH porti ${NEW_SSH_PORT}-portga ko'chirilmoqda..."

# 1. SELinux yoqilgan bo'lsa yangi portni xavfsizlik siyosatiga qo'shamiz
if command -v semanage >/dev/null 2>&1; then
    semanage port -a -t ssh_port_t -p tcp "$NEW_SSH_PORT" 2>/dev/null || \
    semanage port -m -t ssh_port_t -p tcp "$NEW_SSH_PORT" 2>/dev/null || true
    echo "[+] SELinux ssh_port_t ruxsati yangilandi."
fi

# 2. Xavfsizlik devorida yangi portni ochamiz
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active"; then
    ufw allow "${NEW_SSH_PORT}/tcp" comment "SSH Hardened Port"
elif command -v iptables >/dev/null 2>&1; then
    iptables -I INPUT 1 -p tcp --dport "$NEW_SSH_PORT" -j ACCEPT
fi

# 3. sshd konfiguratsiyasiga kiritamiz
cat <<EOF > /etc/ssh/sshd_config.d/99-custom-port.conf
Port ${NEW_SSH_PORT}
EOF

if sshd -t; then
    systemctl reload sshd || systemctl reload ssh || true
    echo "[+] SSH endi ${NEW_SSH_PORT}-portda eshitmoqda! Yangi kirish buyrug'i: ssh -p ${NEW_SSH_PORT} user@host"
else
    echo "[!] Xatolik: sshd sintaksisi noto'g'ri!"
    rm -f /etc/ssh/sshd_config.d/99-custom-port.conf
fi

```
**Tushuntirish:** Standart 22-port butun dunyo botlari tomonidan tinimsiz skanerlanadi. Portni 2222 yoki 50222 kabi nostandart portga o'tkazish server loglaridagi millionlab keraksiz 'Failed password' shovqinlarini kesadi va haqiqiy tahdidlarni ko'rishni osonlashtiradi.

---

### Topshiriq #1171: Fail2ban O'rnatish va SSH jail.local Qat'iy Himoyasini Sozlash
**Tavsif:** SSH ga 3 marta noto'g'ri kalit yoki parol bilan ulanishga uringan har qanday IP manzilni zudlik bilan 24 soatga xavfsizlik devorida (iptables/nftables) bloklovchi Fail2ban xizmatini yoqing.
**Talablar:** jail.local yaratish, maxretry=3, findtime=600, bantime=86400, fail2ban-client tekshiruvi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Fail2ban SSH Himoyasi va Avtomatik Bloklash
set -euo pipefail

echo "[*] Fail2ban o'rnatilmoqda va sozlanmoqda..."

# Paketni o'rnatish (Debian/Ubuntu/RHEL)
if command -v apt-get >/dev/null 2>&1; then
    apt-get update -qq && apt-get install -y -qq fail2ban
elif command -v dnf >/dev/null 2>&1; then
    dnf install -y fail2ban
fi

JAIL_CONF="/etc/fail2ban/jail.d/99-ssh-hardening.local"

cat <<'EOF' > "$JAIL_CONF"
[sshd]
enabled  = true
port     = ssh,22,2222
mode     = aggressive
filter   = sshd
backend  = systemd
maxretry = 3
findtime = 600
bantime  = 86400

# Mahalliy IP va ishonchli ofis subnetlarini oq ro'yxatga olamiz
ignoreip = 127.0.0.1/8 ::1 192.168.1.0/24
EOF

systemctl enable --now fail2ban
systemctl restart fail2ban

echo "[+] Fail2ban faol! 3 marta xato qilgan har qanday begona IP 24 soatga bloklanadi."
fail2ban-client status sshd

```
**Tushuntirish:** Fail2ban tizim jurnallarini (journald yoki /var/log/auth.log) doimiy kuzatib boradi. Regex orqali ulanish xatolarini tahlil qiladi va qoida buzilishi bilan Linux yadrosidagi `nftables` yoki `iptables` ga o'sha IP ni bloklash buyrug'ini kiritadi.

---

### Topshiriq #1172: Nginx/Apache Veb Skanerlar va Zaiflik Qidiruvchilarni Fail2ban Bilan Bloklash
**Tavsif:** Veb serverda `phpmyadmin`, `.env`, `wp-login.php`, `aws/credentials` kabi maxfiy fayllarni qidirib skaner qilayotgan botlarni 404/403 loglariga qarab darhol jazolovchi maxsus filtr tuzing.
**Talablar:** fail2ban filter.d/nginx-scanner.conf, failregex qoidalari, jail sozlamalari.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Veb Zaiflik Skanerlarini Fosh Qiluvchi Fail2ban Qoidasi
set -euo pipefail

FILTER_FILE="/etc/fail2ban/filter.d/nginx-scanner.conf"
JAIL_FILE="/etc/fail2ban/jail.d/nginx-scanner.local"

echo "[*] Veb skanerlar uchun maxsus Fail2ban filtri yaratilmoqda..."

# 1. Regex filtri
cat <<'EOF' > "$FILTER_FILE"
[Definition]
failregex = ^<HOST> - .* "(GET|POST|HEAD) .*(/\.env|/\.git|/phpmyadmin|/wp-login|/eval-stdin|/xmlrpc\.php).* HTTP/.*" (403|404|400)
ignoreregex =
EOF

# 2. Qamoqxona (Jail) konfiguratsiyasi
cat <<'EOF' > "$JAIL_FILE"
[nginx-scanner]
enabled  = true
port     = http,https
filter   = nginx-scanner
logpath  = /var/log/nginx/access.log
maxretry = 2
findtime = 300
bantime  = 604800
EOF

systemctl restart fail2ban 2>/dev/null || true
echo "[+] Veb skanerlar filtri faollashtirildi (Zararli so'rov jo'natgan IP 7 kunga bloklanadi)!"

```
**Tushuntirish:** Avtomatlashtirilgan kiber-qurollar har kuni millionlab saytlardan `.env` fayllari va ma'lumotlar bazasi parollarini qidiradi. Maxsus regex filtri oddiy foydalanuvchilar kirmaydigan noqonuniy yo'llarga tushgan IP larni 1-2 urinishdanoq tarmoq darajasida kesib tashlaydi.

---

### Topshiriq #1173: WordPress va Laravel Login Endpointlarini Brute-Force dan Himoyalash
**Tavsif:** Veb-ilovaning `/login` yoki `wp-login.php` sahifasiga HTTP POST orqali soniyasiga o'nlab parol kiritayotgan buzg'unchilarni aniqlovchi va bloklovchi Fail2ban zanjirini yarating.
**Talablar:** POST /login 200/401/422 statuslarini ushlovchi failregex, Nginx access.log monitoringi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Veb Ilova Login Brute-Force Himoyachisi
set -euo pipefail

FILTER_APP="/etc/fail2ban/filter.d/web-login-bruteforce.conf"
JAIL_APP="/etc/fail2ban/jail.d/web-login.local"

echo "[*] Veb login brute-force filtri o'rnatilmoqda..."

cat <<'EOF' > "$FILTER_APP"
[Definition]
# Foydalanuvchi POST /login ga so'rov yubordi va xatolik (401 yoki 422) qaytdi
failregex = ^<HOST> - .* "POST /(login|api/v1/auth/login|wp-login\.php) HTTP/.*" (401|422|200)
ignoreregex =
EOF

cat <<'EOF' > "$JAIL_APP"
[web-login-bruteforce]
enabled  = true
port     = http,https
filter   = web-login-bruteforce
logpath  = /var/log/nginx/access.log
maxretry = 5
findtime = 120
bantime  = 3600
EOF

systemctl restart fail2ban 2>/dev/null || true
echo "[+] Veb login brute-force himoyasi faollashtirildi!"

```
**Tushuntirish:** Foydalanuvchi hisoblarini o'g'irlashda eng ommabop usul - login sahifasiga millionlab parollarni yuborishdir. Ushbu qoida POST so'rovlarini hisoblab boradi va 2 daqiqa ichida 5 marta xato qilgan botlarni 1 soatga bloklaydi.

---

### Topshiriq #1174: Fail2ban Recidive Jail: Takroriy Qoidabuzarlarni Bir Umrga / Oylab Bloklash
**Tavsif:** Oddiy 1 soatlik yoki 1 kunlik blokdan so'ng yana qaytib kelib serverga hujum qilayotgan asabiy tajovuzkorlarni 'Recidive' rejimi orqali 30 kunga yoki bir umrga bloklang.
**Talablar:** jail.conf dagi [recidive] bo'limi, bantime=2592000 (30 kun), findtime=86400, maxretry=3.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Fail2ban Recidive (Takroriy Qoidabuzarlar) Qat'iy Himoyasi
set -euo pipefail

RECIDIVE_CONF="/etc/fail2ban/jail.d/99-recidive.local"

echo "[*] Recidive (Takroriy hujumchilar) qamoqxonasi sozlanmoqda..."

cat <<'EOF' > "$RECIDIVE_CONF"
[recidive]
enabled  = true
logpath  = /var/log/fail2ban.log
banaction = %(banaction_allports)s
bantime  = 2592000
findtime = 86400
maxretry = 2
EOF

systemctl restart fail2ban 2>/dev/null || true
echo "[+] Recidive faol! 24 soat ichida 2 marta bloklangan IP endi 30 kunga barcha portlardan kesiladi!"
fail2ban-client status recidive

```
**Tushuntirish:** Ko'pgina tajovuzkorlar blok muddati (masalan 1 soat) tugashini kutadi va muddati o'tishi bilan yana buzishni davom ettiradi. `recidive` jail bevosita `fail2ban.log` ning o'zini tahlil qiladi va oldin jazolangan IP larni 30 kunlik qat'iy qora ro'yxatga tiqadi.

---

### Topshiriq #1175: Fail2ban ni Zamonaviy nftables Bilan Integratsiya Qilish
**Tavsif:** Eskirgan iptables o'rniga, Fail2ban qoidabuzarlar IP larini to'g'ridan-to'g'ri `nftables` to'plamlariga (sets) qo'shishi uchun `banaction = nftables-multiport` konfiguratsiyasini bajaring.
**Talablar:** banaction = nftables-multiport, nftables to'plamlari bilan tezkor atomik boshqaruv.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Fail2ban + nftables Zamonaviy Integratsiyasi
set -euo pipefail

FAIL2BAN_LOCAL="/etc/fail2ban/jail.local"

echo "[*] Fail2ban backend-i zamonaviy nftables tizimiga o'tkazilmoqda..."

cat <<'EOF' >> "$FAIL2BAN_LOCAL"

[DEFAULT]
# Standart iptables o'rniga nftables dan foydalanish
banaction = nftables-multiport
banaction_allports = nftables-allports
EOF

systemctl restart fail2ban 2>/dev/null || true

echo "[+] Fail2ban nftables rejimida ishlamoqda!"
# nftables dagi f2b to'plamini ko'rish
nft list table inet f2b-table 2>/dev/null || echo "[*] Yangi qoidabuzar paydo bo'lganda f2b-table avtomatik ochiladi."

```
**Tushuntirish:** iptables da har bir yangi bloklangan IP uchun alohida qoida kiritilardi, bu esa 10,000 ta blokdan so'ng tarmoqni sekinlashtirardi. `nftables` da esa barcha bloklangan IP lar yagona xesh to'plamiga (Set) kiritiladi va O(1) vaqtda zudlik bilan filtrlanadi.

---

### Topshiriq #1176: AbuseIPDB va Threat Intelligence Orqali Zararli IP larni Avtomatik Bloklash
**Tavsif:** Xalqaro kiberxavfsizlik ma'lumotlar bazasidan (AbuseIPDB) eng xavfli botnet va tajovuzkor IP manzillar ro'yxatini yuklab, har kuni `ipset` orqali server kirishini to'sib boruvchi avtomatizatsiya quring.
**Talablar:** AbuseIPDB API dan JSON/CSV olish, ipset hash:ip to'plami, iptables/nftables integratsiyasi, cron bilan avtomatlashtirish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Threat Intelligence: Zararli IP larni Dinamik Bloklash
set -euo pipefail

BLOCKLIST_SET="global_threat_blacklist"
API_KEY="${ABUSEIPDB_API_KEY:-dummy_api_key_2026}"
CONFIDENCE_MIN=90 # Kamida 90% aniqlangan buzg'unchi IP lar

echo "[*] Threat Intelligence IP qora ro'yxati yangilanmoqda..."

# ipset to'plamini tekshiramiz
ipset create "$BLOCKLIST_SET" hash:ip maxelem 200000 -exist

TEMP_IPS="/tmp/bad_ips.txt"

# AbuseIPDB API orqali eng so'nggi zararli IP larni yuklab olamiz
curl -s -G https://api.abuseipdb.com/api/v2/blacklist \
    -d confidenceMinimum="$CONFIDENCE_MIN" \
    -H "Key: $API_KEY" \
    -H "Accept: text/plain" 2>/dev/null > "$TEMP_IPS" || true

# Agar API kalit bo'lmasa, sinov uchun lokal zararli IP lar bilan ishlaymiz
if [[ ! -s "$TEMP_IPS" ]]; then
    cat <<'EOF' > "$TEMP_IPS"
198.51.100.44
203.0.113.88
192.0.2.199
EOF
fi

COUNT=0
while read -r ip; do
    # IP formatini tasdiqlash
    if [[ "$ip" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        ipset add "$BLOCKLIST_SET" "$ip" -exist
        COUNT=$((COUNT + 1))
    fi
done < "$TEMP_IPS"

# iptables ga birinchi qoida qilib ulaymiz
if ! iptables -C INPUT -m set --match-set "$BLOCKLIST_SET" src -j DROP 2>/dev/null; then
    iptables -I INPUT 1 -m set --match-set "$BLOCKLIST_SET" src -j DROP
fi

rm -f "$TEMP_IPS"
echo "[+] ${COUNT} ta global kiber-tahdid IP manzillari darhol bloklandi!"

```
**Tushuntirish:** Ushbu profilaktika usuli serveringizga hujum boshlanmasdanoq, dunyo bo'ylab boshqa serverlarga hujum qilgani aniqlangan botnet IP larini tarmoq chegarasidayoq (Perimeter) to'xtatadi.

---

### Topshiriq #1177: Portscan Hujumlarini Fosh Qilish va IP larni Darhol Karantinga Olish
**Tavsif:** Yopiq portlarga (masalan 23 Telnet, 445 SMB) tegingan har qanday tashqi IP manzilni port skaneri deb baholab, uni barcha boshqa ruxsat etilgan xizmatlardan ham 24 soatga uzib qo'yuvchi tuzoq (Port-Trap) quring.
**Talablar:** iptables da qora portlar to'plami, recent moduli yoki ipset timeout qo'llash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Port-Trap: Skanerlarni Avtomatik Tutuvchi Tuzoq
set -euo pipefail

TRAP_SET="port_scan_quarantine"

echo "[*] Port-Scan Karantin tuzog'i o'rnatilmoqda..."

# 24 soatlik (86400 soniya) vaqt chegarali xesh to'plam
ipset create "$TRAP_SET" hash:ip timeout 86400 -exist

# 1. Karantindagi barcha IP lardan kiruvchi har qanday paketni darhol tashlash
iptables -I INPUT 1 -m set --match-set "$TRAP_SET" src -j DROP

# 2. Tuzoq portlar (Serverda hech qachon ochilmaydigan, faqat skanerlar uriladigan portlar):
# 23 (Telnet), 135/139/445 (SMB), 1433 (MSSQL), 3389 (RDP)
TRAP_PORTS="23,135,139,445,1433,3389"

iptables -A INPUT -p tcp -m multiport --dports "$TRAP_PORTS" -m set ! --match-set "$TRAP_SET" src \
    -j SET --add-set "$TRAP_SET" src

iptables -A INPUT -p tcp -m multiport --dports "$TRAP_PORTS" -j DROP

echo "[+] Skanerlar tuzog'i faol! ${TRAP_PORTS} portlariga tegingan IP 24 soatga to'liq bloklanadi."

```
**Tushuntirish:** Hujumchilar serverni buzishdan oldin har doim port skanerlashni (Reconnaissance) amalga oshiradi. Ular tuzoq portlardan birontasiga teginishi bilan, tizim ularni to'liq karantinga oladi va asosiy veb-sayt yoki SSH portini tekshirish imkoniyatini boy beradi.

---

### Topshiriq #1178: SSH Kirishlarni Telegram/Slack Botga Real Vaqtda Xabar Qilish
**Tavsif:** Serverga SSH orqali kimdir kirganida (muvaffaqiyatli yoki muvaffaqiyatsiz) uning foydalanuvchi nomi, IP manzili va GeoIP davlatini Telegram kanaliga zudlik bilan jo'natuvchi xavfsizlik ogohlantirishini tuzing.
**Talablar:** /etc/pam.d/sshd da pam_exec.so, Telegram Bot API, curl orqali xabar yuborish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - SSH Login Real-Time Telegram Alert
set -euo pipefail

ALERT_SCRIPT="/usr/local/bin/ssh_telegram_alert.sh"

cat <<'EOF' > "$ALERT_SCRIPT"
#!/usr/bin/env bash
# PAM faqat sessiya ochilganda (open_session) ishga tushadi
if [ "$PAM_TYPE" != "open_session" ]; then
    exit 0
fi

BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-dummy_bot_token}"
CHAT_ID="${TELEGRAM_CHAT_ID:-123456789}"

USER_NAME="$PAM_USER"
CLIENT_IP="$PAM_RHOST"
SERVER_NAME="$(hostname)"
LOGIN_TIME="$(date '+%Y-%m-%d %H:%M:%S')"

# IP bo'yicha davlatni aniqlash
GEO_INFO=$(curl -s "https://ipapi.co/${CLIENT_IP}/country_name/" 2>/dev/null || echo "Noma'lum")

MESSAGE="🚨 <b>[SSH KIRISH OGOHLANTIRISHI]</b>
🏢 Server: <code>${SERVER_NAME}</code>
👤 Foydalanuvchi: <code>${USER_NAME}</code>
🌐 IP Manzil: <code>${CLIENT_IP}</code> (${GEO_INFO})
⏰ Vaqt: <code>${LOGIN_TIME}</code>"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"     -d chat_id="${CHAT_ID}"     -d parse_mode="HTML"     -d text="${MESSAGE}" >/dev/null 2>&1 || true

exit 0
EOF

chmod +x "$ALERT_SCRIPT"

# PAM konfiguratsiyasiga qo'shamiz
PAM_SSHD="/etc/pam.d/sshd"
if ! grep -q "ssh_telegram_alert.sh" "$PAM_SSHD"; then
    echo "session optional pam_exec.so seteuid /usr/local/bin/ssh_telegram_alert.sh" >> "$PAM_SSHD"
fi

echo "[+] SSH Telegram ogohlantirish xizmati PAM ga muvaffaqiyatli ulandi!"

```
**Tushuntirish:** PAM (Pluggable Authentication Modules) mexanizmi operatsion tizimda har qanday sessiya boshlanganda maxsus skriptlarni chaqirish imkonini beradi. Adminlar har bir login bo'yicha bir necha soniyada telefoniga xabar oladi va begona kirishlarni darhol payqaydi.

---

### Topshiriq #1179: SSH Sessiyasida Har Bir Buyruqni O'zgarmas Logga Yozish (pam_tty_audit)
**Tavsif:** Tizim ma'murlari yoki xakerlar SSH orqali kirib bajargan har bir tugmachalar bosilishini (Keystroke logging) o'zgartirib bo'lmaydigan audit jurnaliga yozib boruvchi PAM auditini yoqing.
**Talablar:** pam_tty_audit.so enable=*, ausearch -m TTY tahlili, bash history o'chirilishiga chidamlilik.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 5.3.3: TTY Keystroke Auditi (O'zgarmas Terminal Nazorati)
set -euo pipefail

PAM_SSHD="/etc/pam.d/sshd"
PAM_PASSWORD_AUTH="/etc/pam.d/common-session"

echo "[*] TTY Keystroke Logging (pam_tty_audit) sozlanmoqda..."

# Foydalanuvchi `history -c` yoki `unset HISTFILE` qilsa ham,
# pam_tty_audit bevosita Linux yadrosining TTY drayveri orqali har bir belgini yozib oladi!
AUDIT_LINE="session required pam_tty_audit.so enable=* log_passwd"

if ! grep -q "pam_tty_audit.so" "$PAM_SSHD"; then
    echo "$AUDIT_LINE" >> "$PAM_SSHD"
fi

echo "[+] TTY audit faollashtirildi!"
echo "[*] Audit jurnallarini ko'rish uchun buyruq: aureport --tty"

```
**Tushuntirish:** Tajovuzkorlar kirgach, birinchi bo'lib `history -c` orqali o'z izlarini tozalaydi. `pam_tty_audit` esa bash tarixiga bog'liq emas; u Linux yadrosi (Kernel TTY Driver) darajasida barcha kiritilgan belgilarni `auditd` xotirasiga to'g'ridan-to'g'ri yozadi.

---

### Topshiriq #1180: Foydalanuvchilar Sessiyasi 15 Daqiqa Harakatsiz Qolsa Avtomatik Chiqarish (TMOUT)
**Tavsif:** Xodimlar o'z kompyuterlarini qoldirib ketganda sessiya ochiq qolib xavf tug'dirmasligi uchun, 900 soniya davomida harakatsiz qolgan terminalni avtomatik yopuvchi o'zgarmas (readonly) TMOUT sozlang.
**Talablar:** /etc/profile.d/timeout.sh, typeset -r TMOUT=900, readonly TMOUT, export TMOUT.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 5.4.5: Global Terminal Timeout (TMOUT) Himoyasi
set -euo pipefail

TIMEOUT_FILE="/etc/profile.d/99-session-timeout.sh"

echo "[*] Global TMOUT (15 daqiqalik harakatsizlik cheklovi) o'rnatilmoqda..."

cat <<'EOF' > "$TIMEOUT_FILE"
# 900 soniya = 15 daqiqa
TMOUT=900

# 'readonly' va 'typeset -r' foydalanuvchiga ushbu o'zgaruvchini terminalda o'zgartirishni taqiqlaydi
readonly TMOUT
export TMOUT
EOF

chmod 644 "$TIMEOUT_FILE"
echo "[+] 15 daqiqalik avtomatik sessiya yopilishi barcha foydalanuvchilar uchun majburiy qilindi!"

```
**Tushuntirish:** Agar `readonly` qo'yilmasa, dasturchilar o'z terminalida `unset TMOUT` yoki `TMOUT=0` qilib cheklovni chetlab o'tishi mumkin. Readonly xususiyati terminal sessiyasi yopilguniga qadar o'zgaruvchini muzlatadi.

---

### Topshiriq #1181: Auditd (Linux Audit Daemon) O'rnatish va Yo'qotishsiz Bufer Parametrlari
**Tavsif:** Tizimdagi barcha kiberxavfsizlik voqealarini yadro darajasida ushlash uchun `auditd` demonini o'rnating va yuqori yuklamada paketlar yo'qolmasligi uchun buferni 8192 ga sozlang.
**Talablar:** auditd o'rnatish, /etc/audit/auditd.conf da max_log_file, space_left_action, auditctl -b 8192.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 4.1.1: Auditd Monitoring Dvigateli Hardening
set -euo pipefail

echo "[*] auditd xavfsizlik auditi xizmati sozlanmoqda..."

# Paketlarni o'rnatamiz
if command -v apt-get >/dev/null 2>&1; then
    apt-get update -qq && apt-get install -y -qq auditd audispd-plugins
elif command -v dnf >/dev/null 2>&1; then
    dnf install -y audit
fi

AUDITD_CONF="/etc/audit/auditd.conf"

# Disk to'lib qolganda yoki xavf yuzaga kelganda to'g'ri harakat qilish
sed -i 's/^max_log_file =.*/max_log_file = 100/' "$AUDITD_CONF"
sed -i 's/^num_logs =.*/num_logs = 10/' "$AUDITD_CONF"
sed -i 's/^max_log_file_action =.*/max_log_file_action = ROTATE/' "$AUDITD_CONF"
sed -i 's/^space_left_action =.*/space_left_action = SYSLOG/' "$AUDITD_CONF"
sed -i 's/^admin_space_left_action =.*/admin_space_left_action = SUSPEND/' "$AUDITD_CONF"

# Bufer hajmini oshirish (Katta yuklamada xabarlar yo'qolmasligi uchun)
auditctl -b 8192

systemctl enable --now auditd
systemctl restart auditd 2>/dev/null || service auditd restart

echo "[+] auditd xizmati faol va bufer 8192 ga sozlandi!"
auditctl -s

```
**Tushuntirish:** `auditd` Linux yadrosining ichki audit quyi tizimi (kauditd) bilan Netlink soket orqali bog'lanadi. U syslog dan farqli ravishda tizim chaqiruvlari (syscalls) darajasida ishlaydi va o'chirilgan yoki o'zgartirilgan fayllarni kim, qachon, qaysi PID bilan qilganini aniq ko'rsatadi.

---

### Topshiriq #1182: Parollar va Sudoers Fayllari O'zgarishlarini Kuzatuvchi Auditd Qoidalari
**Tavsif:** Tizimdagi `/etc/passwd`, `/etc/shadow`, `/etc/sudoers` va `/etc/group` fayllari ochilganda yoki o'zgartirilganda zudlik bilan audit logiga xavfsizlik tegini qo'yuvchi qoidalar yozing.
**Talablar:** /etc/audit/rules.d/99-identity.rules, -w /etc/shadow -p wa -k identity_changes, augenrules --load.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 4.1.4: Foydalanuvchi Hisoblari va Parollar Auditi
set -euo pipefail

RULES_FILE="/etc/audit/rules.d/99-cis-identity.rules"

echo "[*] Parollar va sudoers fayllari uchun audit qoidalari yozilmoqda..."

cat <<'EOF' > "$RULES_FILE"
# -w: Kuzatilayotgan fayl yo'li
# -p wa: Faqat yozish (write) va atribut o'zgarishi (attribute change) paytida
# -k: Qidiruv va hisobotlar uchun unikal kalit (Key)

-w /etc/group -p wa -k identity_changes
-w /etc/passwd -p wa -k identity_changes
-w /etc/gshadow -p wa -k identity_changes
-w /etc/shadow -p wa -k identity_changes
-w /etc/security/opasswd -p wa -k identity_changes

# Sudo ruxsatlari o'zgarishlarini kuzatish
-w /etc/sudoers -p wa -k sudo_changes
-w /etc/sudoers.d/ -p wa -k sudo_changes
EOF

# Qoidalarni auditd ga yuklaymiz
augenrules --load
echo "[+] Parollar va Sudoers monitoring qoidalari faollashtirildi!"
auditctl -l | grep -E "(identity_changes|sudo_changes)"

```
**Tushuntirish:** Buzg'unchi tizimga kirgach yangi 'backdoor' hisob yaratishga yoki `/etc/sudoers` ga o'zini qo'shishga harakat qiladi. Ushbu qoidalar yordamida `ausearch -k sudo_changes` buyrug'i berilsa, ushbu faylni kim qaysi buyruq orqali o'zgartirganini bir zumda aniqlash mumkin.

---

### Topshiriq #1183: Tizim Chaqiruvlari (Syscalls) Auditi: execve Orqali Bajarilgan Barcha Dasturlar
**Tavsif:** Serverda qaysi foydalanuvchi qaysi binar dasturni (masalan, `whoami`, `nmap`, `nc`) ishga tushirganini qayd etish uchun 64-bitli `execve` va `execveat` tizim chaqiruvlarini audit qiling.
**Talablar:** -a always,exit -F arch=b64 -S execve,execveat -F auid>=1000 -k process_execution.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 4.1.13: Dasturlar Ishga Tushirilishi (execve) Auditi
set -euo pipefail

RULES_FILE="/etc/audit/rules.d/99-exec-audit.rules"

echo "[*] Jarayonlar ishga tushirilishi (execve) audit qoidalari o'rnatilmoqda..."

cat <<'EOF' > "$RULES_FILE"
# Oddiy foydalanuvchilar (auid >= 1000) tomonidan ishga tushirilgan barcha buyruqlar
# auid != 4294967295 (daemon yoki tizim fon jarayonlarini chiqarib tashlash)
-a always,exit -F arch=b64 -S execve -F auid>=1000 -F auid!=4294967295 -k proc_execution
-a always,exit -F arch=b32 -S execve -F auid>=1000 -F auid!=4294967295 -k proc_execution

-a always,exit -F arch=b64 -S execveat -F auid>=1000 -F auid!=4294967295 -k proc_execution
-a always,exit -F arch=b32 -S execveat -F auid>=1000 -F auid!=4294967295 -k proc_execution
EOF

augenrules --load
echo "[+] execve monitoringi yoqildi! Barcha foydalanuvchilar buyruqlari yadro darajasida qayd etiladi."

```
**Tushuntirish:** `execve` barcha yangi dasturlar ishga tushishi uchun javobgar bo'lgan asosiy tizim chaqiruvidir. `auid` (Audit User ID) foydalanuvchi `sudo su` qilib rootga o'tsa ham uning haqiqiy dastlabki kirish shaxsini saqlab qoladi va uning nomidan qilingan barcha amallarni fosh qiladi.

---

### Topshiriq #1184: Tarmoq Muhiti va Xavfsizlik Devori O'zgarishlarini Auditd da Nazorat Qilish
**Tavsif:** Xavfsizlik devori qoidalari (iptables, nftables) o'chirilishi yoki tarmoq konfiguratsiyasi (`/etc/network`, `/etc/resolv.conf`) o'zgartirilishini fosh qiluvchi audit qoidalarini joriy qiling.
**Talablar:** sethostname, setdomainname syscalls, /etc/issue, /etc/hosts, /etc/network kuzatuvi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 4.1.5: Tarmoq Konfiguratsiyasi O'zgarishlari Auditi
set -euo pipefail

RULES_FILE="/etc/audit/rules.d/99-network-audit.rules"

echo "[*] Tarmoq konfiguratsiyasi audit qoidalari yozilmoqda..."

cat <<'EOF' > "$RULES_FILE"
# Tizim hostname o'zgarishlarini kuzatish
-a always,exit -F arch=b64 -S sethostname -S setdomainname -k system_locale
-a always,exit -F arch=b32 -S sethostname -S setdomainname -k system_locale

# Tarmoq konfiguratsiya fayllari monitoringi
-w /etc/issue -p wa -k system_locale
-w /etc/issue.net -p wa -k system_locale
-w /etc/hosts -p wa -k system_locale
-w /etc/resolv.conf -p wa -k network_dns_changes
-w /etc/network/ -p wa -k network_interface_changes
-w /etc/netplan/ -p wa -k network_interface_changes

# Firewall qoidalari skriptlari
-w /etc/iptables/ -p wa -k firewall_changes
-w /etc/nftables.conf -p wa -k firewall_changes
EOF

augenrules --load
echo "[+] Tarmoq va DNS o'zgarishlari auditi muvaffaqiyatli faollashtirildi!"

```
**Tushuntirish:** DNS o'zgartirish (DNS Hijacking) orqali tajovuzkor serverdagi `/etc/resolv.conf` ni o'zining soxta DNS serveriga o'g'irib qo'yishi mumkin. Ushbu audit qoidasi har qanday ruxsatsiz tarmoq tahririni darhol qayd etadi.

---

### Topshiriq #1185: Kernel Modullari Yuklanishi va O'chirilishini (LKM Rootkits) Ushlovchi Qoidalar
**Tavsif:** Serverga yashirin yadro darajasidagi rootkitlar (LKM Rootkits) o'rnatilishini yoki xavfsizlik drayverlari o'chirilishini `init_module` va `delete_module` tizim chaqiruvlari orqali kuzating.
**Talablar:** init_module, finit_module, delete_module syscalls, /bin/kmod kuzatuvi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 4.1.16: Yadro Modullari (LKM) Auditi
set -euo pipefail

RULES_FILE="/etc/audit/rules.d/99-kernel-modules.rules"

echo "[*] Yadro modullari (Kernel Modules) auditi o'rnatilmoqda..."

cat <<'EOF' > "$RULES_FILE"
# Kernel modullarini yuklash yoki o'chirish buyruqlari
-w /bin/kmod -p x -k kernel_module_tools
-w /sbin/insmod -p x -k kernel_module_tools
-w /sbin/rmmod -p x -k kernel_module_tools
-w /sbin/modprobe -p x -k kernel_module_tools

# Yadro tizim chaqiruvlari: init_module, finit_module, delete_module
-a always,exit -F arch=b64 -S init_module -S finit_module -S delete_module -k kernel_module_changes
-a always,exit -F arch=b32 -S init_module -S finit_module -S delete_module -k kernel_module_changes
EOF

augenrules --load
echo "[+] LKM Rootkit va yadro modullari monitoringi muvaffaqiyatli yoqildi!"

```
**Tushuntirish:** Loadable Kernel Module (LKM) rootkitlari eng xavfli kiber-qurollar hisoblanadi, chunki ular to'g'ridan-to'g'ri Linux yadrosiga integratsiyalashib, o'z jarayonlarini `ps` va `netstat` buyruqlaridan yashira oladi. `init_module` auditi bunday harakatni fosh qiladi.

---

### Topshiriq #1186: Tizim Vaqti O'zgarishi Auditi (Anti-Forensics Hujumlaridan Himoya)
**Tavsif:** Buzg'unchilar jinoyat vaqtini yashirish va loglarni chalg'itish uchun soatni orqaga surishining (Anti-Forensics) oldini olish uchun `settimeofday` va `adjtimex` chaqiruvlarini audit qiling.
**Talablar:** adjtimex, settimeofday, clock_settime syscalls, -k time_change.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 4.1.3: Tizim Vaqti Manipulyatsiyasi Auditi
set -euo pipefail

RULES_FILE="/etc/audit/rules.d/99-time-change.rules"

echo "[*] Vaqt o'zgarishi (Anti-Forensics) audit qoidalari qo'llanilmoqda..."

cat <<'EOF' > "$RULES_FILE"
# 64-bit va 32-bit vaqt o'zgartirish chaqiruvlari
-a always,exit -F arch=b64 -S adjtimex -S settimeofday -S clock_settime -k time_change
-a always,exit -F arch=b32 -S adjtimex -S settimeofday -S clock_settime -k time_change

# Mahalliy vaqt mintaqasi fayli
-w /etc/localtime -p wa -k time_change
EOF

augenrules --load
echo "[+] Vaqt o'zgartirish harakatlari to'liq nazoratga olindi!"

```
**Tushuntirish:** Sud-kiber-ekspertizasida (Digital Forensics) vaqt jadvali (Timeline) eng muhim dalildir. Xakerlar loglarni chalkashtirish uchun tizim soatini o'zgartirishga urinadi; ushbu qoida bu harakatni o'chmas qilib muhrlaydi.

---

### Topshiriq #1187: Ruxsatsiz Faylga Kirish Urinishlarini (EACCES va EPERM) Fosh Qilish
**Tavsif:** Tizimdagi oddiy foydalanuvchilar yoki veb-server xaker tomonidan egallangach, ruxsat berilmagan maxfiy fayllarni titkilash urinishlarini (Permission Denied) tahlil qiling.
**Talablar:** exit=-EACCES va exit=-EPERM filtrli audit qoidalari, ausearch hisoboti.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 4.1.10: Ruxsatsiz Faylga Kirish (EACCES/EPERM) Auditi
set -euo pipefail

RULES_FILE="/etc/audit/rules.d/99-access-denied.rules"

echo "[*] Ruxsatsiz faylga kirish urinishlari monitoringi sozlanmoqda..."

cat <<'EOF' > "$RULES_FILE"
# Fayl ochish, yaratish yoki o'chirish paytida EACCES (13) yoki EPERM (1) xatoligi qaytgan holatlar
-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access_denied
-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access_denied

-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access_denied
-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access_denied
EOF

augenrules --load
echo "[+] Muvaffaqiyatsiz (Permission Denied) fayl amallari auditi faol!"
echo "[*] Oxirgi urinishlarni ko'rish buyrug'i: ausearch -k access_denied --raw | aureport -f -i"

```
**Tushuntirish:** Oddiy qonuniy dasturlar kamdan-kam hollarda 'Permission Denied' xatosiga uchraydi. Agar qisqa vaqt ichida yuzlab EACCES xatoliklari qayd etilsa, demak serverda ichki razvedka (Privilege Escalation skripti) ishlayapti.

---

### Topshiriq #1188: Auditd Qoidalarini O'zgartirib Bo'lmaydigan (Immutable Mode -e 2) Qilish
**Tavsif:** Agar buzg'unchi Root huquqini qo'lga kiritsa ham, server qayta ishga tushirilmaguncha `auditctl` orqali audit qoidalarini o'chira olmasligi yoki o'zgartira olmasligi uchun Immutable rejimini yoqing.
**Talablar:** audit.rules oxiriga '-e 2' qo'yish, qayta yuklash cheklovi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 4.1.17: Auditd Immutable Qat'iy Rejimi (-e 2)
set -euo pipefail

IMMUTABLE_FILE="/etc/audit/rules.d/99-finalize-immutable.rules"

echo "=========================================================="
echo "[*] DIQQAT: auditd qoidalari IMMUTABLE (-e 2) rejimiga o'tkazilmoqda!"
echo "=========================================================="

# Barcha qoidalar fayllari ro'yxatining eng oxirida bo'lishi shart
cat <<'EOF' > "$IMMUTABLE_FILE"
# -e 2: Ushbu qoida yoqilgandan so'ng, hatto ROOT foydalanuvchisi ham
# server to'liq REBOOT bo'lmaguncha audit qoidalarini o'zgartira yoki o'chira olmaydi!
-e 2
EOF

augenrules --load
echo "[+] Audit tizimi muvaffaqiyatli muzlatildi (Immutable mode faol)!"
auditctl -s | grep "enabled"

```
**Tushuntirish:** Root foydalanuvchisi Linux da cheksiz huquqqa ega, biroq `auditctl -e 2` yadroga kiritilgach, kernel darajasida audit konfiguratsiyasini qabul qilish bloklanadi. Bu Rootkitlar va tajovuzkorlarning o'z izlarini o'chirishiga yo'l qo'ymaydi.

---

### Topshiriq #1189: aureport Yordamida Avtomatlashtirilgan Kiberxavfsizlik va Tizim Auditi Hisoboti
**Tavsif:** Har tong tizim ma'muri uchun serverdagi barcha xavfsizlik hodisalarini (muvaffaqiyatsiz loginlar, ishga tushirilgan buyruqlar, anomaliyalar) umumlashtirib chiroyli xulosa beruvchi skript tuzing.
**Talablar:** aureport -au, aureport -s, aureport --failed, formatlangan xulosa.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Haftalik/Kunlik Auditd Xavfsizlik Hisoboti
set -euo pipefail

REPORT_DATE=$(date '+%Y-%m-%d')
REPORT_FILE="/var/log/audit_security_report_${REPORT_DATE}.txt"

echo "=========================================================="
echo "          KHORAZMIY AI - TIZIM AUDIT XULOSASI             "
echo " Sana: ${REPORT_DATE} | Server: $(hostname)                "
echo "==========================================================" > "$REPORT_FILE"

echo -e "\n--- 1. MUVAFFAQIYATSIZ LOGIN URINISHLARI (Failed Logins) ---" >> "$REPORT_FILE"
aureport -l --failed --summary 2>/dev/null >> "$REPORT_FILE" || echo "Ma'lumot yo'q" >> "$REPORT_FILE"

echo -e "\n--- 2. FOYDALANUVCHILAR VA AUTENTIFIKATSIYA XULOSASI ---" >> "$REPORT_FILE"
aureport -au --summary 2>/dev/null >> "$REPORT_FILE" || echo "Ma'lumot yo'q" >> "$REPORT_FILE"

echo -e "\n--- 3. BAJARILGAN ENG KO'P TIZIM CHAQIRISHLARI (Syscalls) ---" >> "$REPORT_FILE"
aureport -s --summary 2>/dev/null | head -n 15 >> "$REPORT_FILE" || echo "Ma'lumot yo'q" >> "$REPORT_FILE"

echo -e "\n--- 4. FAYL HUQUQLARI XATOLIKLARI (Failed File Access) ---" >> "$REPORT_FILE"
aureport -f --failed --summary 2>/dev/null | head -n 10 >> "$REPORT_FILE" || echo "Ma'lumot yo'q" >> "$REPORT_FILE"

echo "[+] Hisobot tayyorlandi: ${REPORT_FILE}"
cat "$REPORT_FILE" | head -n 25

```
**Tushuntirish:** Xom `/var/log/audit/audit.log` millionlab qatorlardan iborat bo'lib, inson ko'zi bilan o'qish qiyin. `aureport` bu jurnallarni tezkor indekslab, aniq statistik jadvallarni (Failed logins, Syscalls, File access) bir necha soniyada chiqaradi.

---

### Topshiriq #1190: Audit Loglarini Markaziy Xavfsiz SIEM Serveriga Uzatish (audisp-remote)
**Tavsif:** Mahalliy server buzib kirilganda loglar o'chirib yuborilmasligi uchun, barcha audit hodisalarini real vaqtda markaziy xavfsiz Syslog/SIEM serveriga TLS orqali uzatuvchi `audisp-remote` ni sozlang.
**Talablar:** audisp-remote.conf, remote_server manzili, TLS shifrlash, audispd yoqish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - audisp-remote orqali SIEM Log Forwarding
set -euo pipefail

REMOTE_SIEM_IP="10.10.50.100"
REMOTE_PORT="514"

echo "[*] Audit loglarini markaziy SIEM ga yo'naltirish sozlanmoqda..."

PLUGIN_CONF="/etc/audit/plugins.d/au-remote.conf"
if [[ ! -f "$PLUGIN_CONF" ]]; then
    PLUGIN_CONF="/etc/audisp/plugins.d/au-remote.conf"
fi

if [[ -f "$PLUGIN_CONF" ]]; then
    # Pluginni yoqamiz
    sed -i 's/^active =.*/active = yes/' "$PLUGIN_CONF"
fi

REMOTE_CONF="/etc/audit/audisp-remote.conf"
if [[ ! -f "$REMOTE_CONF" ]]; then
    REMOTE_CONF="/etc/audisp/audisp-remote.conf"
fi

cat <<EOF > "$REMOTE_CONF"
remote_server = ${REMOTE_SIEM_IP}
port = ${REMOTE_PORT}
transport = tcp
mode = immediate
queue_file = /var/spool/audit/remote.log
EOF

systemctl restart auditd 2>/dev/null || true
echo "[+] Audit loglari real vaqtda ${REMOTE_SIEM_IP} manzilidagi SIEM tizimiga uzatilmoqda!"

```
**Tushuntirish:** Kiberxavfsizlikning oltin qoidasi: 'Mahalliy loglarga ishonma'. Buzg'unchi root huquqini olgach birinchi bo'lib diskdagi loglarni o'chiradi. `audisp-remote` hodisa sodir bo'lishi bilanoq uni tarmoq orqali tashqi xavfsiz serverga nusxalaydi.

---

### Topshiriq #1191: AppArmor Holatini Tekshirish va Nginx Uchun Cheklovchi Profil Yaratish
**Tavsif:** Nginx veb-serveri buzilgan taqdirda ham, uning tizimning boshqa qismlariga (masalan `/home`, `/root`) o'tib ketishini to'xtatuvchi AppArmor Enforcing profilini yarating.
**Talablar:** aa-status, /etc/apparmor.d/usr.sbin.nginx, aa-enforce, ruxsat etilgan yo'llar.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - AppArmor Nginx Qat'iy Izolyatsiya Profili
set -euo pipefail

PROFILE_PATH="/etc/apparmor.d/usr.sbin.nginx"

echo "[*] Nginx uchun AppArmor qat'iy profili yaratilmoqda..."

cat <<'EOF' > "$PROFILE_PATH"
#include <tunables/global>

/usr/sbin/nginx {
  #include <abstractions/base>
  #include <abstractions/nameservice>
  #include <abstractions/nis>

  # Tarmoq ulanishlariga ruxsat
  network inet stream,
  network inet6 stream,

  # Nginx binar fayli va kutubxonalari
  /usr/sbin/nginx mr,
  /usr/lib{,32,64}/** mr,

  # Konfiguratsiyalar: Faqat o'qish
  /etc/nginx/** r,
  /etc/ssl/** r,

  # Sayt fayllari: Faqat o'qish
  /var/www/** r,

  # Loglar va PID fayllar: Yozish huquqi
  /var/log/nginx/** rw,
  /var/log/nginx/*.log w,
  /run/nginx.pid rw,
  /var/run/nginx.pid rw,

  # Vaqtinchalik fayllar
  /var/lib/nginx/** rw,

  # XAVFLI HUDUDLARNI QAT'IY TAQIQLASH (Explicit Deny)
  deny /home/** rwklx,
  deny /root/** rwklx,
  deny /etc/shadow* rwklx,
  deny /etc/sudoers* rwklx,
}
EOF

# Profilni AppArmor ga yuklaymiz va Enforcing rejimiga o'tkazamiz
apparmor_parser -r "$PROFILE_PATH"
aa-enforce "$PROFILE_PATH" 2>/dev/null || true

echo "[+] Nginx AppArmor profili faollashtirildi!"
aa-status | grep nginx

```
**Tushuntirish:** AppArmor (Application Armor) - Linux Mandatory Access Control (MAC) tizimidir. Agar Nginx da 0-day zaiflik topilib, xaker veb-server nomidan buyruq bajarsa ham, AppArmor uni `/home` yoki `/etc/shadow` ga kirishini yadro darajasida to'xtatadi.

---

### Topshiriq #1192: AppArmor Profilida Xavfli Kataloglarni O'qishni Qat'iy Taqiqlash (deny qoidalari)
**Tavsif:** Har qanday foydalanuvchi maydonidagi dasturlarning maxfiy SSH kalitlari (`/home/*/.ssh`) va tizim konfiguratsiyalariga teginishini taqiqlovchi umumiy AppArmor bloklarini tuzing.
**Talablar:** deny /home/*/.ssh/** rwklx, abstractions/base kengaytmasi, audit jurnali tahlili.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - AppArmor Maxfiy Ma'lumotlarni Qat'iy Himoyalash
set -euo pipefail

DENY_SNIPPET="/etc/apparmor.d/abstractions/deny-sensitive-keys"

echo "[*] AppArmor umumiy taqiqlar andozasi yaratilmoqda..."

cat <<'EOF' > "$DENY_SNIPPET"
# Maxfiy SSH kalitlarini har qanday cheklangan dasturdan yashirish
deny @{HOME}/.ssh/** rwklx,
deny /root/.ssh/** rwklx,

# AWS va Bulut kalitlari
deny @{HOME}/.aws/** rwklx,
deny @{HOME}/.kube/** rwklx,

# Tizim parollari
deny /etc/shadow* rwklx,
deny /etc/gshadow* rwklx,
EOF

echo "[+] AppArmor deny-sensitive-keys andozasi tayyorlandi va profillarga ulanishi mumkin."

```
**Tushuntirish:** AppArmor qoidalarida `deny` har doim oddiy ruxsat beruvchi qoidalardan ustun turadi. Agar profil ichiga ushbu andoza kiritilsa, hatto dasturda keng ruxsatlar bo'lsa ham foydalanuvchilarning shaxsiy SSH va AWS kalitlari daxlsiz qoladi.

---

### Topshiriq #1193: SELinux Enforcing Rejimini Yoqish va Kontekstlarni Tiklash (restorecon)
**Tavsif:** RHEL, Rocky Linux yoki CentOS serverlarida SELinux ni 'Enforcing' rejimiga o'tkazib, veb-sayt kataloglariga to'g'ri `httpd_sys_content_t` xavfsizlik kontekstlarini avtomatik tiklang.
**Talablar:** /etc/selinux/config da SELINUX=enforcing, semanage fcontext, restorecon -Rv.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - SELinux Enforcing va Kontekstlar Boshqaruvi
set -euo pipefail

echo "[*] SELinux holati tekshirilmoqda..."

if ! command -v getenforce >/dev/null 2>&1; then
    echo "[!] SELinux ushbu tizimda mavjud emas (Ehtimol Debian/Ubuntu AppArmor ishlatmoqda)."
    exit 0
fi

CURRENT_MODE=$(getenforce)
echo "[+] Joriy rejim: ${CURRENT_MODE}"

# 1. Enforcing rejimiga o'tkazish
setenforce 1 2>/dev/null || true
sed -i 's/^SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config

# 2. Veb sayt katalogi uchun SELinux kontekstini to'g'irlash
WEB_DIR="/var/www/html"
mkdir -p "$WEB_DIR"

if command -v semanage >/dev/null 2>&1; then
    # Doimiy siyosatga qo'shamiz
    semanage fcontext -a -t httpd_sys_content_t "${WEB_DIR}(/.*)?" 2>/dev/null || true
fi

# Kontekstlarni diskda jismonan tiklash
restorecon -Rv "$WEB_DIR" > /dev/null

echo "[+] SELinux Enforcing rejimiga muvaffaqiyatli o'tkazildi!"
ls -dZ "$WEB_DIR"

```
**Tushuntirish:** SELinux (Security-Enhanced Linux) NSA tomonidan ishlab chiqilgan eng qudratli kiberhimoya tizimidir. Har bir jarayon va fayl maxsus yorliqqa (Type context, masalan `httpd_t` va `httpd_sys_content_t`) ega bo'lib, ular orasidagi harakatlar qat'iy yadro polislari bilan chegaralanadi.

---

### Topshiriq #1194: SELinux Taqiqlari Auditi va Tahlili (audit2why va audit2allow)
**Tavsif:** SELinux sababli ilova ishlamay qolganida (Avc Denied), butun xavfsizlik tizimini o'chirib yubormasdan (Permissive qilmasdan), muammoni professional tahlil qilib xavfsiz modul yozing.
**Talablar:** audit2why < /var/log/audit/audit.log, audit2allow -M custom_policy, semodule -i.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - SELinux AVC Taqiqlari Diagnostikasi
set -euo pipefail

AUDIT_LOG="/var/log/audit/audit.log"

if [[ ! -f "$AUDIT_LOG" ]]; then
    echo "[!] Audit log fayli topilmadi: $AUDIT_LOG"
    exit 0
fi

echo "=========================================================="
echo "[*] SELinux AVC Denied Xatoliklari Tahlili..."
echo "=========================================================="

# 1. Nima sababdan taqiqlanganini inson tushunadigan tilda ko'rsatish
if command -v audit2why >/dev/null 2>&1; then
    grep "type=AVC" "$AUDIT_LOG" | tail -n 20 | audit2why || true
else
    grep "type=AVC" "$AUDIT_LOG" | tail -n 10 || echo "AVC xatolari topilmadi."
fi

# 2. Xavfsiz siyosat moduli yaratish namunasi:
# grep "nginx" /var/log/audit/audit.log | audit2allow -M my_nginx_policy
# semodule -i my_nginx_policy.pp
echo "=========================================================="
echo "[+] SELinux diagnostikasi yakunlandi."

```
**Tushuntirish:** Ko'pgina yangi boshlovchilar muammoga duch kelganda SELinux-ni butunlay o'chirib qo'yadi (`SELINUX=disabled`). To'g'ri sanoat usuli - `audit2why` orqali taqiq sababini aniqlash va faqat kerakli port yoki fayl uchun minimal qonuniy ruxsat modulini yuklashdir.

---

### Topshiriq #1195: AIDE (Advanced Intrusion Detection Environment) Yaxlitlik Boshqaruvi
**Tavsif:** Tizim fayllari (`/bin`, `/sbin`, `/etc`) xakerlar yoki rootkitlar tomonidan o'zgartirilganligini bilish uchun barcha fayllarning SHA-512 xesh bazasini tuzuvchi va tekshiruvchi AIDE tizimini ishga tushiring.
**Talablar:** aide --init, bazani faollashtirish (mv aide.db.new aide.db), aide --check, o'zgarishlar auditi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - AIDE Fayl Tizimi Yaxlitligi Monitoringi (FIM)
set -euo pipefail

echo "[*] AIDE (File Integrity Monitoring) xizmati sozlanmoqda..."

# Paketni o'rnatish
if command -v apt-get >/dev/null 2>&1; then
    apt-get update -qq && apt-get install -y -qq aide
elif command -v dnf >/dev/null 2>&1; then
    dnf install -y aide
fi

AIDE_DB_DIR="/var/lib/aide"
mkdir -p "$AIDE_DB_DIR"

echo "[*] Boshlang'ich yaxlitlik xesh bazasi initsializatsiya qilinmoqda (aideinit)..."
if command -v aideinit >/dev/null 2>&1; then
    aideinit --force -y >/dev/null 2>&1 || true
else
    aide --init >/dev/null 2>&1 || true
    if [[ -f "${AIDE_DB_DIR}/aide.db.new.gz" ]]; then
        cp "${AIDE_DB_DIR}/aide.db.new.gz" "${AIDE_DB_DIR}/aide.db.gz"
    fi
fi

echo "[+] AIDE bazasi muvaffaqiyatli saqlandi!"
echo "[*] Tizimni har kecha tekshirish uchun cron vazifasi:"
cat <<EOF
# /etc/cron.daily/aide-check
0 3 * * * /usr/bin/aide --check | /usr/bin/mail -s "AIDE Yaxlitlik Xulosasi" admin@khorazmiy.uz
EOF

```
**Tushuntirish:** AIDE - bu ochiq manbali Tripwire analogidir. U har bir tizim binar faylining hajmi, ruxsatlari, egasi va kriptografik xeshini ma'lumotlar bazasida saqlaydi. Agar xaker `/bin/ls` yoki `/usr/bin/ssh` ni o'zgartirsa, `aide --check` buni darhol fosh qiladi.

---

### Topshiriq #1196: Rkhunter va Chkrootkit Orqali Rootkitlar va Backdoorlarni Skanerlash
**Tavsif:** Yashirin foydalanuvchi maydoni va yadro darajasidagi rootkitlar, troyanlar va shubhali fayllarni `rkhunter` va `chkrootkit` vositalari orqali avtomatlashtirilgan tarzda skanerlang.
**Talablar:** rkhunter --check --skip-keypress, rkhunter --propupd, chkrootkit, ogohlantirishlarni filtrlash.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Rootkit va Yashirin Backdoorlar Skaneri
set -euo pipefail

LOG_FILE="/var/log/rkhunter_scan_$(date +%Y%m%d).log"

echo "=========================================================="
echo "[*] Tizimda Rootkitlar va Yashirin Tahdidlar Tekshiruvi..."
echo "=========================================================="

# Agar rkhunter o'rnatilmagan bo'lsa o'rnatamiz
if ! command -v rkhunter >/dev/null 2>&1; then
    if command -v apt-get >/dev/null 2>&1; then
        apt-get update -qq && apt-get install -y -qq rkhunter chkrootkit
    fi
fi

if command -v rkhunter >/dev/null 2>&1; then
    echo "[*] rkhunter ma'lumotlar bazasi yangilanmoqda..."
    rkhunter --update --nolog >/dev/null 2>&1 || true
    rkhunter --propupd --nolog >/dev/null 2>&1 || true

    echo "[*] To'liq skanerlash boshlandi (bu 1-2 daqiqa olishi mumkin)..."
    # --rwo: Faqat ogohlantirishlarni chiqarish (Report Warnings Only)
    WARNINGS=$(rkhunter --check --skip-keypress --rwo 2>&1 || true)

    if [[ -n "$WARNINGS" ]]; then
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "[OGOHLANTIRISH] Tizimda shubhali modifikatsiyalar topildi:"
        echo "$WARNINGS"
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    else
        echo "[+] A'lo! rkhunter hech qanday ma'lum rootkit yoki backdoor topmadi."
    fi
fi

if command -v chkrootkit >/dev/null 2>&1; then
    echo -e "\n[*] chkrootkit tekshiruvi:"
    chkrootkit -q 2>&1 | grep -iE "(INFECTED|vulnerable)" || echo "[+] chkrootkit bo'yicha tizim toza."
fi

```
**Tushuntirish:** `rkhunter` (Rootkit Hunter) tizim buyruqlarining xeshlarini tekshiradi, `/dev` katalogidagi shubhali qurilma fayllarini qidiradi va yadro modullari orasidagi anomaliyalarni fosh qiladi. U APT hujumlari va o'rnatilgan troyanlarni aniqlashda juda samarali.

---

### Topshiriq #1197: Sudoers Konfiguratsiyasini CIS Standartida Qat'iylashtirish (requiretty, use_pty, logfile)
**Tavsif:** Privilegiya ko'tarilishida (Privilege Escalation) sudo suiiste'mol qilinmasligi uchun parolsiz buyruqlarni cheklang, har bir sudo harakatini alohida logga yozing va PTY majburlang.
**Talablar:** /etc/sudoers.d/99-hardening, Defaults requiretty, Defaults use_pty, Defaults logfile, visudo -c.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - CIS 5.3.4 & 5.3.7: Sudo Xavfsizligini Qat'iylashtirish
set -euo pipefail

SUDO_HARDENING="/etc/sudoers.d/99-cis-sudo-hardening"

echo "[*] Sudoers xavfsizlik konfiguratsiyasi yaratilmoqda..."

cat <<'EOF' > "$SUDO_HARDENING"
# Har bir sudo buyrug'i faqat haqiqiy terminal (TTY) orqali bajarilishi shart
# Bu veb-shellar yoki cron orqali orqa fonda sudo ishlatishni to'xtatadi
Defaults requiretty

# Har bir sudo sessiyasi uchun alohida psevdo-terminal ajratish (I/O spoofing himoyasi)
Defaults use_pty

# Barcha bajarilgan sudo buyruqlarini alohida xavfsiz logga yozish
Defaults logfile="/var/log/sudo.log"

# Xato parol kiritilganda kutish vaqti
Defaults passwd_tries=3
Defaults badpass_message="Noto'g'ri parol! Harakat auditga yozildi."

# Xavfsiz PATH ni majburlash (Zararli binar fayllarni chetlab o'tish)
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
EOF

chmod 440 "$SUDO_HARDENING"

# Sintaktik tekshiruv (visudo -c orqali xato bo'lsa server qulab qolmasligi uchun)
if visudo -c -f "$SUDO_HARDENING"; then
    echo "[+] Sudoers muvaffaqiyatli qat'iylashtirildi!"
else
    echo "[XATO] Sudoers sintaksisida xato! Fayl o'chirilmoqda..."
    rm -f "$SUDO_HARDENING"
    exit 1
fi

```
**Tushuntirish:** `Defaults requiretty` veb-server (masalan www-data) buzilganda, buzg'unchining veb-shell orqali fonda `sudo su` chaqirishini to'xtatadi, chunki uning sessiyasida haqiqiy TTY terminali bo'lmaydi. `use_pty` esa terminal orqali kiruvchi-chiquvchi oqimlarni manipulyatsiya qilishni yo'q qiladi.

---

### Topshiriq #1198: Xotirada Yashiringan Zombi Jarayonlar va Unlinked Binar Fayllarni Fosh Qilish
**Tavsif:** Diskdan o'chirib yuborilgan, lekin xotirada ishlab turgan (Fileless Malware / Memory-only) yoki nomini yashirgan shubhali jarayonlarni `/proc` orqali audit qiling.
**Talablar:** ls -l /proc/*/exe tekshiruvi, '(deleted)' bayrog'ini aniqlash, PID va tarmoq soketlarini tahlil qilish.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Xotirada Yashiringan (Fileless / Deleted) Jarayonlar Auditi
set -euo pipefail

echo "=========================================================="
echo "[*] Xotirada ishlab turgan shubhali jarayonlar tekshiruvi..."
echo "=========================================================="

SUSPICIOUS_COUNT=0

# Barcha ishlayotgan jarayonlarning bajariluvchi fayllarini (exe) tekshiramiz
for exe in /proc/[0-9]*/exe; do
    if [[ -l "$exe" ]]; then
        TARGET=$(readlink "$exe" 2>/dev/null || true)
        
        # Agar binar fayl diskdan o'chirilgan bo'lsa (Fileless malware texnikasi)
        if echo "$TARGET" | grep -q "(deleted)"; then
            PID=$(echo "$exe" | cut -d/ -f3)
            CMDLINE=$(tr ' ' ' ' < "/proc/${PID}/cmdline" 2>/dev/null || echo "Noma'lum")
            USER_NAME=$(stat -c '%U' "/proc/${PID}" 2>/dev/null || echo "Noma'lum")
            
            # Yangilanishdan so'ng qolib ketgan oddiy xizmatlarni chiqarib tashlaymiz
            if ! echo "$CMDLINE" | grep -qE "(systemd|dbus|multipathd)"; then
                echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                echo "[!] SHUBHALI JARAYON ANIQLANDI:"
                echo "    PID:     ${PID}"
                echo "    Egasi:   ${USER_NAME}"
                echo "    Fayl:    ${TARGET}"
                echo "    Buyruq:  ${CMDLINE}"
                echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                SUSPICIOUS_COUNT=$((SUSPICIOUS_COUNT + 1))
            fi
        fi
    fi
done

if [[ $SUSPICIOUS_COUNT -eq 0 ]]; then
    echo "[+] Xotirada hech qanday shubhali o'chirilgan binar jarayonlar topilmadi."
else
    echo "[!] Jami shubhali jarayonlar: ${SUSPICIOUS_COUNT} ta! Tekshirish tavsiya etiladi."
fi

```
**Tushuntirish:** Zamonaviy 'Fileless' troyanlar diskka o'z binarini yozadi, ishga tushiradi va darhol diskdagi faylni `rm` qilib o'chirib yuboradi. Natijada oddiy antiviruslar diskda faylni topa olmaydi. Ammo Linux yadrosi jarayon o'lmaguncha uni `/proc/$PID/exe (deleted)` ko'rinishida ushlab turadi.

---

### Topshiriq #1199: Cron va Systemd Timerlarini Audit Qilish (Persistence Aniqlash)
**Tavsif:** Buzg'unchilar server qayta ishga tushganda ham boshqaruvni saqlab qolish uchun (Persistence) o'rnatgan yashirin Cron vazifalari va Systemd timerlarini to'liq audit qiluvchi skript yozing.
**Talablar:** Barcha foydalanuvchilar crontab lari, /etc/cron.*, /etc/systemd/system/ timerlari tahlili.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Doimiy Qolib Ketish (Persistence Mechanism) Auditi
set -euo pipefail

echo "=========================================================="
echo "[*] Tizimdagi Barcha Rejalashtirilgan Vazifalar (Cron + Timers) Auditi"
echo "=========================================================="

echo "--- 1. Barcha foydalanuvchilar crontab lari ---"
while read -r user; do
    CRON_OUT=$(crontab -u "$user" -l 2>/dev/null | grep -v '^#' | grep -v '^$' || true)
    if [[ -n "$CRON_OUT" ]]; then
        echo "[+] Foydalanuvchi: ${user}"
        echo "$CRON_OUT"
    fi
done < <(cut -d: -f1 /etc/passwd)

echo -e "\n--- 2. Tizim Cron kataloglari (/etc/cron.* va /etc/crontab) ---"
grep -E -v "^(#|$)" /etc/crontab 2>/dev/null || true
for dir in /etc/cron.d /etc/cron.daily /etc/cron.hourly /etc/cron.monthly /etc/cron.weekly; do
    if [[ -d "$dir" ]]; then
        FILES=$(find "$dir" -type f 2>/dev/null)
        if [[ -n "$FILES" ]]; then
            echo "[*] Katalog: $dir"
            echo "$FILES" | xargs head -n 2 2>/dev/null || true
        fi
    fi
done

echo -e "\n--- 3. Systemd Aktiv Timerlari (systemctl list-timers) ---"
systemctl list-timers --no-pager 2>/dev/null | head -n 15 || echo "Systemd timerlar olinmadi"

echo "=========================================================="
echo "[+] Persistence auditi yakunlandi."

```
**Tushuntirish:** Tajovuzkor serverni egallagach, keyingi kirishi uchun `/etc/cron.d/` yoki `systemd timer` orqali har 10 daqiqada Reverse Shell ochuvchi skript qo'yib ketadi. Barcha cron yo'llarini markazlashgan holda audit qilish yashirin kirish nuqtalarini fosh qiladi.

---

### Topshiriq #1200: CIS Benchmark To'liq Avtomatlashtirilgan Audit va Yakuniy Hardening Tizimi
**Tavsif:** Tizimning xavfsizlik darajasini (Fayl huquqlari, Tarmoq, SSH, Yadro, Auditd, Xavfsizlik devori) noldan 100% gacha baholab, umumiy xulosa beruvchi yakuniy sanoat darajasidagi Hardening skriptini quring.
**Talablar:** Ko'p mezonli avtomatlashtirilgan tekshiruv, ballar tizimi (Scoring 0-100), ANSI ranglar, to'liq audit xulosasi.
**Yechim (Bash):**
```bash
#!/usr/bin/env bash
# Khorazmiy AI - Sanoat Darajasidagi CIS Benchmark Yakuniy Audit Skripti
set -euo pipefail

SCORE=0
TOTAL_CHECKS=10

# Ranglar
C_GREEN="[32m"
C_RED="[31m"
C_CYAN="[36m"
C_BOLD="[1m"
C_RESET="[0m"

echo -e "${C_BOLD}${C_CYAN}======================================================================${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}          KHORAZMIY AI - CIS BENCHMARK YAKUNIY XAVFSIZLIK AUDITI       ${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}======================================================================${C_RESET}"
echo -e " Server:    ${C_BOLD}$(hostname)${C_RESET} | Sana: $(date '+%Y-%m-%d %H:%M:%S')"
echo -e " OS:        $(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '"')"
echo -e "${C_CYAN}----------------------------------------------------------------------${C_RESET}"

# 1. ASLR Tekshiruvi
if [[ $(sysctl -n kernel.randomize_va_space 2>/dev/null) -eq 2 ]]; then
    echo -e " [1] ASLR (Address Space Layout Randomization): ${C_GREEN}[PASS] (Qiymat: 2)${C_RESET}"
    SCORE=$((SCORE + 1))
else
    echo -e " [1] ASLR:                                       ${C_RED}[FAIL] (Zaif)${C_RESET}"
fi

# 2. SYN Cookies
if [[ $(sysctl -n net.ipv4.tcp_syncookies 2>/dev/null) -eq 1 ]]; then
    echo -e " [2] TCP SYN Cookies (DDoS Himoyasi):          ${C_GREEN}[PASS] (Faol)${C_RESET}"
    SCORE=$((SCORE + 1))
else
    echo -e " [2] TCP SYN Cookies:                          ${C_RED}[FAIL]${C_RESET}"
fi

# 3. ICMP Redirects
if [[ $(sysctl -n net.ipv4.conf.all.accept_redirects 2>/dev/null) -eq 0 ]]; then
    echo -e " [3] ICMP Redirects Taqiqi (MITM Himoyasi):    ${C_GREEN}[PASS] (Taqiqlangan)${C_RESET}"
    SCORE=$((SCORE + 1))
else
    echo -e " [3] ICMP Redirects:                           ${C_RED}[FAIL]${C_RESET}"
fi

# 4. Core Dumps Cheklovi
if [[ $(sysctl -n fs.suid_dumpable 2>/dev/null) -eq 0 ]]; then
    echo -e " [4] SUID Core Dump Sizishini O'chirish:        ${C_GREEN}[PASS] (O'chirilgan)${C_RESET}"
    SCORE=$((SCORE + 1))
else
    echo -e " [4] SUID Core Dump:                           ${C_RED}[FAIL]${C_RESET}"
fi

# 5. SSH Root Login
if grep -riq "^PermitRootLogin[[:space:]]*no" /etc/ssh/ 2>/dev/null; then
    echo -e " [5] SSH Root Login Taqiqi:                     ${C_GREEN}[PASS] (No)${C_RESET}"
    SCORE=$((SCORE + 1))
else
    echo -e " [5] SSH Root Login:                            ${C_RED}[FAIL] (Root ochiq!)${C_RESET}"
fi

# 6. SSH Parol Autentifikatsiyasi
if grep -riq "^PasswordAuthentication[[:space:]]*no" /etc/ssh/ 2>/dev/null; then
    echo -e " [6] SSH Parolsiz (Faqat Kalit) Kirish:        ${C_GREEN}[PASS] (Faqat kalit)${C_RESET}"
    SCORE=$((SCORE + 1))
else
    echo -e " [6] SSH Parolsiz Kirish:                      ${C_RED}[FAIL] (Parol yoqilgan)${C_RESET}"
fi

# 7. Auditd Xizmati
if systemctl is-active auditd >/dev/null 2>&1; then
    echo -e " [7] Auditd Yadro Monitoring Demoni:            ${C_GREEN}[PASS] (Ishlamoqda)${C_RESET}"
    SCORE=$((SCORE + 1))
else
    echo -e " [7] Auditd Demoni:                             ${C_RED}[FAIL] (Nofaol)${C_RESET}"
fi

# 8. Fail2ban Xizmati
if systemctl is-active fail2ban >/dev/null 2>&1; then
    echo -e " [8] Fail2ban Brute-Force Himoyachisi:         ${C_GREEN}[PASS] (Faol)${C_RESET}"
    SCORE=$((SCORE + 1))
else
    echo -e " [8] Fail2ban:                                 ${C_RED}[FAIL] (Nofaol)${C_RESET}"
fi

# 9. AppArmor yoki SELinux
if (command -v aa-status >/dev/null 2>&1 && aa-status --enabled 2>/dev/null) ||    (command -v getenforce >/dev/null 2>&1 && [[ $(getenforce) == "Enforcing" ]]); then
    echo -e " [9] Mandatory Access Control (AppArmor/SELinux): ${C_GREEN}[PASS] (Faol)${C_RESET}"
    SCORE=$((SCORE + 1))
else
    echo -e " [9] Mandatory Access Control:                 ${C_RED}[FAIL] (Nofaol)${C_RESET}"
fi

# 10. /etc/shadow Huquqlari (Faqat root o'qishi kerak - 000 yoki 640/600)
SHADOW_PERM=$(stat -c '%a' /etc/shadow 2>/dev/null || echo "777")
if [[ "$SHADOW_PERM" =~ ^(0|600|640)$ ]]; then
    echo -e " [10] /etc/shadow Huquqlari Xavfsizligi:       ${C_GREEN}[PASS] (${SHADOW_PERM})${C_RESET}"
    SCORE=$((SCORE + 1))
else
    echo -e " [10] /etc/shadow Huquqlari:                  ${C_RED}[FAIL] (${SHADOW_PERM} - Juda ochiq!)${C_RESET}"
fi

# Yakuniy natija
PERCENT=$(( (SCORE * 100) / TOTAL_CHECKS ))
echo -e "${C_CYAN}----------------------------------------------------------------------${C_RESET}"
echo -e " ${C_BOLD}YAKUNIY XAVFSIZLIK BALLI: ${PERCENT}% (${SCORE}/${TOTAL_CHECKS})${C_RESET}"

if [[ $PERCENT -ge 80 ]]; then
    echo -e " ${C_GREEN}${C_BOLD}[A'LO] Server CIS Benchmark xavfsizlik talablariga to'liq javob beradi!${C_RESET}"
else
    echo -e " ${C_RED}${C_BOLD}[OGOHLANTIRISH] Tizimda jiddiy xavfsizlik kamchiliklari mavjud. Hardening tavsiya etiladi.${C_RESET}"
fi
echo -e "${C_BOLD}${C_CYAN}======================================================================${C_RESET}"

```
**Tushuntirish:** CIS (Center for Internet Security) Benchmarks kiberxavfsizlik sohasida global oltin standart hisoblanadi. Ushbu skript barcha asosiy himoya qatlamlarini (Yadro, Tarmoq, Autentifikatsiya, Audit, MAC) to'liq avtomatik tarzda baholaydi va zaif nuqtalarni ko'rsatib beradi.

---

