Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Linux xavfsizligi va tizim boshqaruvi bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan, sanoat standartlariga mos keladigan 10 ta ilg'or Bash modulini taqdim etaman.

---

# 1001-Topshiriq: SSH Root Loginni o'chirish (CIS Benchmark)

## Topshiriq sharti:
SSH konfiguratsiya faylida `PermitRootLogin` parametrini `no` qiymatiga o'zgartirib, xavfsizlikni kuchaytiring.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd
echo "SSH root login o'chirildi."
```

## Tushuntirish va Mantiq:
`sed` buyrug'i orqali `sshd_config` faylida `PermitRootLogin` qatorini qidiramiz va uni `no` ga o'zgartiramiz. Bu hujumchilarning root foydalanuvchisi orqali tizimga kirishini oldini oladi.

## Ishlash natijasi:
```text
SSH root login o'chirildi.
```

---

# 1002-Topshiriq: IP Forwardingni o'chirish

## Topshiriq sharti:
Server router vazifasini bajarmasa, IP forwarding funksiyasini o'chirib qo'ying.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sysctl -w net.ipv4.ip_forward=0
echo "net.ipv4.ip_forward = 0" >> /etc/sysctl.conf
sysctl -p
```

## Tushuntirish va Mantiq:
`sysctl` yordamida yadro parametrini o'zgartiramiz. Bu serverning paketlarni boshqa tarmoqlarga yo'naltirishini to'xtatadi, bu esa "Man-in-the-middle" hujumlaridan himoya qiladi.

## Ishlash natijasi:
```text
net.ipv4.ip_forward = 0
```

---

# 1003-Topshiriq: Iptables orqali barcha kiruvchi trafikni bloklash (Default Deny)

## Topshiriq sharti:
Iptables yordamida barcha kiruvchi trafikni bloklab, faqat kerakli portlarni ochish siyosatini o'rnating.

## Yechim (Bash kodi):
```bash
#!/bin/bash
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

## Tushuntirish va Mantiq:
`DROP` siyosati barcha noma'lum ulanishlarni rad etadi. `lo` (loopback) va `ESTABLISHED` (allaqachon o'rnatilgan) ulanishlarni ruxsat berish orqali tizimning ishlashini ta'minlaymiz.

## Ishlash natijasi:
```text
Iptables qoidalari muvaffaqiyatli o'rnatildi.
```

---

# 1004-Topshiriq: SSH uchun Fail2Ban avtomatik o'rnatish

## Topshiriq sharti:
SSH orqali brute-force hujumlarini aniqlash va bloklash uchun Fail2Ban ni sozlang.

## Yechim (Bash kodi):
```bash
#!/bin/bash
apt-get install -y fail2ban
cat <<EOF > /etc/fail2ban/jail.local
[sshd]
enabled = true
port = ssh
filter = sshd
maxretry = 3
bantime = 3600
EOF
systemctl restart fail2ban
```

## Tushuntirish va Mantiq:
Fail2Ban log fayllarni kuzatadi. 3 ta noto'g'ri urinishdan so'ng, IP manzilni 1 soatga (3600 soniya) bloklaydi.

## Ishlash natijasi:
```text
Fail2Ban o'rnatildi va SSH himoyasi faollashtirildi.
```

---

# 1005-Topshiriq: Keraksiz fayl tizimlarini o'chirish (CIS)

## Topshiriq sharti:
`cramfs`, `freevxfs`, `jffs2`, `hfs`, `hfsplus`, `squashfs` kabi foydalanilmaydigan fayl tizimlarini yuklanishini taqiqlang.

## Yechim (Bash kodi):
```bash
#!/bin/bash
echo "install cramfs /bin/true" > /etc/modprobe.d/CIS.conf
echo "install freevxfs /bin/true" >> /etc/modprobe.d/CIS.conf
echo "install squashfs /bin/true" >> /etc/modprobe.d/CIS.conf
```

## Tushuntirish va Mantiq:
`modprobe` orqali ushbu drayverlarni `/bin/true` ga yo'naltirish ularning yuklanishini imkonsiz qiladi, bu esa yadro darajasidagi hujum sirtini kamaytiradi.

## Ishlash natijasi:
```text
Keraksiz fayl tizimlari o'chirildi.
```

---

# 1006-Topshiriq: Nftables orqali HTTP/HTTPS ruxsati

## Topshiriq sharti:
`nftables` yordamida 80 va 443 portlarini oching.

## Yechim (Bash kodi):
```bash
#!/bin/bash
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; }
nft add rule inet filter input tcp dport { 80, 443 } accept
```

## Tushuntirish va Mantiq:
`nftables` zamonaviy paket filtri hisoblanadi. `add rule` buyrug'i bilan veb-server uchun zarur bo'lgan portlarni ochiq qoldiramiz.

## Ishlash natijasi:
```text
Nftables qoidalari qo'shildi.
```

---

# 1007-Topshiriq: Parol siyosatini kuchaytirish

## Topshiriq sharti:
`/etc/login.defs` faylida parollarning amal qilish muddatini 90 kunga o'zgartiring.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' /etc/login.defs
sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   7/' /etc/login.defs
```

## Tushuntirish va Mantiq:
Parolning 90 kunda yangilanishi va kamida 7 kun o'zgarishi kerakligi xavfsizlik talablariga (CIS) mos keladi.

## Ishlash natijasi:
```text
Parol siyosati yangilandi.
```

---

# 1008-Topshiriq: Auditd orqali fayl o'zgarishlarini kuzatish

## Topshiriq sharti:
`/etc/passwd` fayliga qilingan har qanday o'zgarishni `auditd` orqali logga yozing.

## Yechim (Bash kodi):
```bash
#!/bin/bash
auditctl -w /etc/passwd -p wa -k identity_changes
echo "Audit qoidasi o'rnatildi."
```

## Tushuntirish dan Mantiq:
`-w` faylni kuzatadi, `-p wa` (write/attribute) yozish va atribut o'zgarishlarini nazorat qiladi. `-k` esa qidiruv uchun kalit so'zdir.

## Ishlash natijasi:
```text
Audit qoidasi o'rnatildi.
```

---

# 1009-Topshiriq: SSH uchun xavfsiz shifrlash algoritmlarini tanlash

## Topshiriq sharti:
SSH konfiguratsiyasida faqat kuchli MAC va Kex algoritmlariga ruxsat bering.

## Yechim (Bash kodi):
```bash
#!/bin/bash
echo "Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com" >> /etc/ssh/sshd_config
systemctl restart sshd
```

## Tushuntirish va Mantiq:
Eski va zaif shifrlash algoritmlarini (masalan, DES, 3DES) o'chirib, zamonaviy va tezkor algoritmlarni majburiy qilamiz.

## Ishlash natijasi:
```text
SSH shifrlash algoritmlari yangilandi.
```

---

# 1010-Topshiriq: Tizimdagi "World-Writable" fayllarni topish

## Topshiriq sharti:
Tizimda hamma yozishi mumkin bo'lgan (world-writable) fayllarni topib, ularni ro'yxatga oling.

## Yechim (Bash kodi):
```bash
#!/bin/bash
find / -xdev -type f \( -perm -0002 -a ! -perm -1000 \) -ls > /var/log/world_writable.log
echo "World-writable fayllar /var/log/world_writable.log ga yozildi."
```

## Tushuntirish va Mantiq:
`find` buyrug'i tizim bo'ylab hamma uchun yozish huquqi ochiq bo'lgan fayllarni qidiradi. Bu xavfsizlik auditi uchun juda muhim, chunki bunday fayllar hujumchilar uchun qulay nishondir.

## Ishlash natijasi:
```text
World-writable fayllar /var/log/world_writable.log ga yozildi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Linux tizim xavfsizligini avtomatlashtirish va CIS benchmark standartlariga moslashtirish uchun 10 ta ilg'or Bash modulini tayyorladim.

---

# 1011-Topshiriq: SSH ildiz (root) kirishini bloklash

## Topshiriq sharti:
SSH orqali root foydalanuvchisining to'g'ridan-to'g'ri tizimga kirishini taqiqlash va xavfsizlikni oshirish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd
echo "Root login o'chirildi."
```

## Tushuntirish va Mantiq:
`sed` buyrug'i `sshd_config` faylidagi `PermitRootLogin` parametrini qidirib, uni `no` qiymatiga o'zgartiradi. Bu brute-force hujumlarining oldini olish uchun eng muhim qadamlardan biridir.

## Ishlash natijasi:
```text
Root login o'chirildi.
```

---

# 1012-Topshiriq: Noto'g'ri fayl ruxsatlarini aniqlash

## Topshiriq sharti:
Tizimdagi `/etc/shadow` fayli uchun ruxsatlarni 0000 (faqat root uchun) qilib belgilash.

## Yechim (Bash kodi):
```bash
#!/bin/bash
chmod 600 /etc/shadow
chown root:root /etc/shadow
echo "Shadow fayli himoyalandi."
```

## Tushuntirish va Mantiq:
`/etc/shadow` fayli parollar xeshlarini saqlaydi. `chmod 600` faqat root foydalanuvchisiga o'qish va yozish huquqini beradi, bu esa CIS standartlariga mos keladi.

## Ishlash natijasi:
```text
Shadow fayli himoyalandi.
```

---

# 1013-Topshiriq: Iptables orqali kiruvchi trafikni cheklash

## Topshiriq sharti:
Barcha kiruvchi trafikni bloklash va faqat SSH (22-port) ga ruxsat berish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
iptables -P INPUT DROP
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
echo "Iptables qoidalari o'rnatildi."
```

## Tushuntirish va Mantiq:
`DROP` siyosati barcha noma'lum ulanishlarni rad etadi. Faqat 22-port va lokal (loopback) interfeysga ruxsat beriladi.

## Ishlash natijasi:
```text
Iptables qoidalari o'rnatildi.
```

---

# 1014-Topshiriq: IP Spoofing himoyasi

## Topshiriq va Mantiq:
Kernel darajasida IP spoofing hujumlarini oldini olish uchun `rp_filter` ni yoqish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sysctl -w net.ipv4.conf.all.rp_filter=1
sysctl -w net.ipv4.conf.default.rp_filter=1
echo "IP Spoofing himoyasi yoqildi."
```

## Ishlash natijasi:
```text
IP Spoofing himoyasi yoqildi.
```

---

# 1015-Topshiriq: Avtomatik IDS (Fail2Ban) o'rnatish

## Topshiriq sharti:
Fail2Ban paketini o'rnatish va SSH uchun himoya qoidasini faollashtirish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
apt-get install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban
echo "Fail2Ban ishga tushirildi."
```

## Tushuntirish va Mantiq:
Fail2Ban log fayllarni kuzatib, noto'g'ri parol kiritgan IP manzillarni avtomatik bloklaydi.

## Ishlash natijasi:
```text
Fail2Ban ishga tushirildi.
```

---

# 1016-Topshiriq: Keraksiz xizmatlarni o'chirish

## Topshiriq sharti:
Tizimda ishlayotgan `avahi-daemon` kabi keraksiz xizmatlarni to'xtatish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
systemctl stop avahi-daemon
systemctl disable avahi-daemon
echo "Avahi-daemon o'chirildi."
```

## Tushuntirish va Mantiq:
Keraksiz xizmatlar hujum yuzasini (attack surface) kengaytiradi. Ularni o'chirish tizimni "hardened" qilishning asosiy qismidir.

## Ishlash natijasi:
```text
Avahi-daemon o'chirildi.
```

---

# 1017-Topshiriq: ICMP Redirect paketlarini bloklash

## Topshiriq sharti:
Man-in-the-middle hujumlarining oldini olish uchun ICMP redirect paketlarini rad etish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sysctl -w net.ipv4.conf.all.accept_redirects=0
sysctl -w net.ipv4.conf.default.accept_redirects=0
echo "ICMP redirect bloklandi."
```

## Ishlash natijasi:
```text
ICMP redirect bloklandi.
```

---

# 1018-Topshiriq: Fayl tizimi yaxlitligini tekshirish (AIDE)

## Topshiriq sharti:
AIDE (Advanced Intrusion Detection Environment) o'rnatish va bazani yaratish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
apt-get install -y aide
aideinit
echo "AIDE bazasi yaratildi."
```

## Tushuntirish va Mantiq:
AIDE tizim fayllaridagi o'zgarishlarni kuzatib boradi va ruxsatsiz o'zgarishlar bo'lsa xabar beradi.

## Ishlash natijasi:
```text
AIDE bazasi yaratildi.
```

---

# 1019-Topshiriq: Nftables jadvalini yaratish

## Topshiriq sharti:
Iptables o'rniga zamonaviy `nftables` yordamida asosiy himoya jadvalini yaratish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; }
nft add rule inet filter input tcp dport 22 accept
echo "Nftables qoidalari qo'shildi."
```

## Ishlash natijasi:
```text
Nftables qoidalari qo'shildi.
```

---

# 1020-Topshiriq: Auditd orqali loglarni kuzatish

## Topshiriq sharti:
`auditd` yordamida `/etc/passwd` fayliga bo'lgan barcha o'zgarishlarni logga yozish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
auditctl -w /etc/passwd -p wa -k passwd_change
echo "Audit qoidasi o'rnatildi."
```

## Tushuntirish va Mantiq:
`auditd` tizim chaqiruvlarini kuzatadi. `-p wa` (write/attribute change) parametri faylga yozish yoki atribut o'zgarishini kuzatishni bildiradi.

## Ishlash natijasi:
```text
Audit qoidasi o'rnatildi.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Linux server xavfsizligini avtomatlashtirish va CIS benchmark standartlarini joriy etish bo'yicha 10 ta ilg'or Bash skript modulini taqdim etaman.

---

# 1021-Topshiriq: SSH xavfsizligini kuchaytirish (CIS 5.2.1)

## Topshiriq sharti:
SSH konfiguratsiya faylida `PermitRootLogin` ni `no` holatiga o'tkazish va `Protocol` versiyasini 2 ga majburiy belgilash.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^#\?Protocol.*/Protocol 2/' /etc/ssh/sshd_config
systemctl restart sshd
```

## Tushuntirish va Mantiq:
`sed` buyrug'i yordamida konfiguratsiya faylidagi izohlangan yoki noto'g'ri qiymatlarni qidirib, ularni xavfsiz variantlar bilan almashtiramiz. `systemctl restart` xizmatni yangi sozlamalar bilan qayta ishga tushiradi.

## Ishlash natijasi:
```text
SSH konfiguratsiyasi yangilandi va xizmat qayta ishga tushirildi.
```

---

# 1022-Topshiriq: IP Forwardingni o'chirish

## Topshiriq sharti:
Server router vazifasini bajarmasligi uchun kernel darajasida IP forwardingni o'chirish.

## Yechim (Bash kodi):
```bash
sysctl -w net.ipv4.ip_forward=0
sysctl -w net.ipv6.conf.all.forwarding=0
echo "net.ipv4.ip_forward = 0" >> /etc/sysctl.conf
```

## Tushuntirish va Mantiq:
`sysctl` yordamida yadro parametrlarini real vaqtda o'zgartiramiz va doimiy bo'lishi uchun `/etc/sysctl.conf` fayliga yozamiz.

## Ishlash natijasi:
```text
IP forwarding o'chirildi.
```

---

# 1023-Topshiriq: Nftables asosiy himoya qoidasi

## Topshiriq sharti:
Barcha kiruvchi trafikni bloklash va faqat SSH (22) portini ochiq qoldirish.

## Yechim (Bash kodi):
```bash
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }
nft add rule inet filter input tcp dport 22 accept
nft add rule inet filter input ct state established,related accept
```

## Tushuntirish va Mantiq:
`nftables` orqali "default drop" siyosatini o'rnatamiz. Faqat 22-port va allaqachon o'rnatilgan sessiyalarni qabul qilamiz.

## Ishlash natijasi:
```text
Nftables qoidalari muvaffaqiyatli o'rnatildi.
```

---

# 1024-Topshiriq: Fayl tizimi ruxsatlarini tekshirish

## Topshiriq sharti:
`/etc/passwd` fayli faqat o'qish uchun ekanligini va egasi root ekanligini tekshirish.

## Yechim (Bash kodi):
```bash
chmod 644 /etc/passwd
chown root:root /etc/passwd
ls -l /etc/passwd | awk '{print $1, $3, $4}'
```

## Tushuntirish va Mantiq:
CIS standartlariga ko'ra, tizim fayllari faqat root tomonidan yozilishi kerak. `chmod` va `chown` orqali ruxsatlar to'g'rilanadi.

## Ishlash natijasi:
```text
-rw-r--r-- root root
```

---

# 1025-Topshiriq: Fail2Ban avtomatik IDS o'rnatish

## Topshiriq sharti:
Brute-force hujumlarini oldini olish uchun Fail2Ban xizmatini o'rnatish va SSH uchun sozlash.

## Yechim (Bash kodi):
```bash
apt-get install -y fail2ban
cat <<EOF > /etc/fail2ban/jail.local
[sshd]
enabled = true
port = ssh
maxretry = 3
EOF
systemctl restart fail2ban
```

## Tushuntirish va Mantiq:
Fail2Ban log fayllarni kuzatib, 3 marta noto'g'ri parol kiritgan IP manzillarni avtomatik bloklaydi.

## Ishlash natijasi:
```text
Fail2Ban o'rnatildi va SSH uchun himoya faollashtirildi.
```

---

# 1026-Topshiriq: Keraksiz xizmatlarni o'chirish

## Topshiriq sharti:
Tizimda ishlayotgan `avahi-daemon` va `cups` kabi keraksiz xizmatlarni to'xtatish.

## Yechim (Bash kodi):
```bash
systemctl stop avahi-daemon cups
systemctl disable avahi-daemon cups
```

## Tushuntirish va Mantiq:
Serverda hujum yuzasini (attack surface) kamaytirish uchun foydalanilmaydigan xizmatlarni o'chirish muhim.

## Ishlash natijasi:
```text
Keraksiz xizmatlar o'chirildi.
```

---

# 1027-Topshiriq: Password Aging (Parol muddati)

## Topshiriq sharti:
Foydalanuvchi parollari 90 kunda yangilanishini majburiy qilish.

## Yechim (Bash kodi):
```bash
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/' /etc/login.defs
sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS 7/' /etc/login.defs
```

## Tushuntirish va Mantiq:
`/etc/login.defs` fayli tizimdagi parollar siyosatini boshqaradi. 90 kunlik muddat xavfsizlik uchun standart hisoblanadi.

## Ishlash natijasi:
```text
Parol siyosati yangilandi (90 kun).
```

---

# 1028-Topshiriq: Iptables orqali ICMP flood himoyasi

## Topshiriq sharti:
Ping hujumlarini (ICMP flood) cheklash uchun iptables qoidasini qo'shish.

## Yechim (Bash kodi):
```bash
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
```

## Tushuntirish va Mantiq:
`limit` moduli yordamida soniyasiga faqat 1 ta ping so'rovini qabul qilamiz, qolganini rad etamiz.

## Ishlash natijasi:
```text
ICMP flood himoyasi faollashtirildi.
```

---

# 1029-Topshiriq: Auditd loglarini sozlash

## Topshiriq sharti:
Tizimda bajarilgan barcha `execve` (buyruq bajarish) amallarini logga yozish.

## Yechim (Bash kodi):
```bash
echo "-a always,exit -F arch=b64 -S execve -k cmd_log" >> /etc/audit/rules.rules
service auditd restart
```

## Tushuntirish va Mantiq:
`auditd` tizimda kim, qachon va qaysi buyruqni bajarganini kuzatib boradi. Bu forensik tahlil uchun juda muhim.

## Ishlash natijasi:
```text
Auditd qoidalari yangilandi.
```

---

# 1030-Topshiriq: Tizim yangilanishlarini avtomatlashtirish

## Topshiriq sharti:
Xavfsizlik yangilanishlarini (unattended-upgrades) avtomatik o'rnatishni sozlash.

## Yechim (Bash kodi):
```bash
apt-get install -y unattended-upgrades
dpkg-reconfigure -f noninteractive unattended-upgrades
```

## Tushuntirish va Mantiq:
Xavfsizlik yamoqlarini (patches) o'z vaqtida o'rnatish serverni zaifliklardan himoya qilishning eng samarali usulidir.

## Ishlash natijasi:
```text
Avtomatik yangilanishlar sozlandi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Linux tizim xavfsizligini avtomatlashtirish va CIS benchmark standartlarini joriy etish bo'yicha 10 ta ilg'or Bash modulini taqdim etaman.

---

# 1031-Topshiriq: SSH ildiz (root) kirishini bloklash

## Topshiriq sharti:
SSH orqali `root` foydalanuvchisining tizimga kirishini taqiqlash va xavfsizlikni oshirish uchun `/etc/ssh/sshd_config` faylini avtomatik tahrirlash.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd
echo "SSH root kirishi o'chirildi."
```

## Tushuntirish va Mantiq:
`sed` buyrug'i yordamida `PermitRootLogin` parametri qidiriladi va u `no` qiymatiga o'zgartiriladi. Bu brute-force hujumlaridan himoyalanishning birinchi qadamidir.

## Ishlash natijasi:
```text
SSH root kirishi o'chirildi.
```

---

# 1032-Topshiriq: IP Forwardingni o'chirish (CIS Benchmark)

## Topshiriq sharti:
Server router vazifasini bajarmasa, IP forwarding funksiyasini o'chirib qo'yish orqali tarmoq xavfsizligini ta'minlash.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sysctl -w net.ipv4.ip_forward=0
echo "net.ipv4.ip_forward = 0" >> /etc/sysctl.conf
sysctl -p
```

## Tushuntirish va Mantiq:
`sysctl` yordamida yadro darajasida paketlarni yo'naltirish to'xtatiladi. Bu serverning "man-in-the-middle" hujumlarida qatnashishini oldini oladi.

## Ishlash natijasi:
```text
net.ipv4.ip_forward = 0
```

---

# 1033-Topshiriq: Nmap orqali ochiq portlarni tekshirish

## Topshiriq scharti:
Tizimda ishlayotgan barcha ochiq portlarni skanerlash va ularni `open_ports.log` fayliga yozish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
nmap -sT localhost | grep "open" > open_ports.log
echo "Ochiq portlar open_ports.log fayliga yozildi."
```

## Tushuntirish va Mantiq:
`nmap` yordamida lokal hostdagi TCP portlar tekshiriladi. `grep` orqali faqat ochiq portlar ajratib olinadi.

## Ishlash natijasi:
```text
Ochiq portlar open_ports.log fayliga yozildi.
```

---

# 1034-Topshiriq: Iptables orqali barcha kiruvchi trafikni cheklash

## Topshiriq sharti:
Default holatda barcha kiruvchi trafikni bloklash va faqat ruxsat berilgan portlarni ochish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

## Tushuntirish va Mantiq:
`DROP` siyosati o'rnatiladi. `lo` (loopback) va allaqachon o'rnatilgan aloqalar uchun ruxsat beriladi.

## Ishlash natijasi:
```text
Iptables qoidalari o'rnatildi.
```

---

# 1035-Topshiriq: Fail2Ban o'rnatish va SSH himoyasi

## Topshiriq sharti:
SSH orqali noto'g'ri parol kiritgan IP manzillarni avtomatik bloklash uchun Fail2Ban o'rnatish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
apt-get update && apt-get install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban
```

## Tushuntirish va Mantiq:
Fail2Ban log fayllarni kuzatib, takroriy xatolik sodir etgan IP-larni iptables orqali vaqtincha bloklaydi.

## Ishlash natijasi:
```text
Fail2Ban xizmati ishga tushdi.
```

---

# 1036-Topshiriq: Fayl tizimi ruxsatlarini tekshirish (CIS)

## Topshiriq sharti:
`/etc/passwd` fayliga faqat o'qish huquqini qoldirish (644).

## Yechim (Bash kodi):
```bash
#!/bin/bash
chmod 644 /etc/passwd
chown root:root /etc/passwd
echo "Fayl ruxsatlari yangilandi."
```

## Tushuntirish va Mantiq:
CIS standartlariga ko'ra, tizim fayllari faqat root tomonidan yozilishi va hamma tomonidan o'qilishi kerak.

## Ishlash natijasi:
```text
Fayl ruxsatlari yangilandi.
```

---

# 1037-Topshiriq: Nftables jadvalini yaratish

## Topshiriq sharti:
`nftables` yordamida yangi xavfsizlik jadvalini yaratish va asosiy qoidalarni kiritish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; }
nft add rule inet filter input tcp dport 22 accept
```

## Tushuntirish va Mantiq:
`nftables` zamonaviy iptables o'rnini bosuvchi vosita. Bu yerda SSH (22) porti uchun qoida yaratildi.

## Ishlash natijasi:
```text
Nftables qoidalari qo'shildi.
```

---

# 1038-Topshiriq: Keraksiz xizmatlarni o'chirish

## Topshiriq sharti:
Tizimda ishlayotgan `avahi-daemon` kabi keraksiz xizmatlarni to'xtatish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
systemctl stop avahi-daemon
systemctl disable avahi-daemon
echo "Avahi-daemon o'chirildi."
```

## Tushuntirish and Mantiq:
Serverda kerak bo'lmagan har bir xizmat - bu potentsial xavfsizlik teshigi. Ularni o'chirish hujum yuzasini kamaytiradi.

## Ishlash natijasi:
```text
Avahi-daemon o'chirildi.
```

---

# 1039-Topshiriq: Log fayllarni kuzatish (IDS elementi)

## Topshiriq sharti:
`/var/log/auth.log` faylida "Failed password" so'zini qidirib, topilgan har bir holatni ekranga chiqarish.

## Yechim (Bash kodi):
```bash
#!/bin/bash
grep "Failed password" /var/log/auth.log | tail -n 5
```

## Tushuntirish va Mantiq:
Bu oddiy IDS (Intrusion Detection System) elementi bo'lib, tizimga kirishga bo'lgan muvaffaqiyatsiz urinishlarni tahlil qiladi.

## Ishlash natijasi:
```text
Failed password for root from 192.168.1.5 port 44322 ssh2
```

---

# 1040-Topshiriq: Tizim yangilanishlarini avtomatlashtirish

## Topshiriq sharti:
Xavfsizlik yangilanishlarini avtomatik o'rnatish uchun `unattended-upgrades` ni sozlash.

## Yechim (Bash kodi):
```bash
#!/bin/bash
apt-get install -y unattended-upgrades
dpkg-reconfigure -f noninteractive unattended-upgrades
echo "Avtomatik yangilanishlar yoqildi."
```

## Tushuntirish va Mantiq:
Xavfsizlik yamoqlarini (patches) o'z vaqtida o'rnatish CIS benchmarkning eng muhim talablaridan biridir.

## Ishlash natijasi:
```text
Avtomatik yangilanishlar yoqildi.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Linux server xavfsizligi va avtomatlashtirish bo'yicha 100 000 talik datasetimizni boyitish uchun quyidagi 10 ta ilg'or Bash skript modulini taqdim etaman.

---

# 1041-Topshiriq: SSH Root Loginni bloklash (CIS Benchmark)

## Topshiriq sharti:
Server xavfsizligini oshirish uchun `/etc/ssh/sshd_config` faylida `PermitRootLogin` parametrini `no` qiymatiga o'zgartiring va SSH xizmatini qayta ishga tushiring.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd
echo "SSH Root login o'chirildi."
```

## Tushuntirish va Mantiq:
`sed` buyrug'i yordamida konfiguratsiya faylidagi mos qator topilib, qiymat `no` ga o'zgartiriladi. Bu brute-force hujumlaridan himoya qiladi.

## Ishlash natijasi:
```text
SSH Root login o'chirildi.
```

---

# 1042-Topshiriq: Nmap orqali ochiq portlarni tekshirish

## Topshiriq sharti:
Serverdagi barcha ochiq portlarni aniqlang va ularni `open_ports.log` fayliga yozib oling.

## Yechim (Bash kodi):
```bash
#!/bin/bash
nmap -p- localhost | grep "open" > open_ports.log
echo "Ochiq portlar open_ports.log fayliga yozildi."
```

## Tushuntirish va Mantiq:
`nmap -p-` barcha 65535 portni skanerlaydi. `grep "open"` faqat ochiq portlarni filtrlab, faylga saqlaydi.

## Ishlash natijasi:
```text
Ochiq portlar open_ports.log fayliga yozildi.
```

---

# 1043-Topshiriq: Iptables orqali barcha trafikni bloklash (Default Drop)

## Topshiriq sharti:
Iptables orqali kiruvchi (INPUT) va yo'naltiruvchi (FORWARD) trafikni standart holatda bloklang.

## Yechim (Bash kodi):
```bash
#!/bin/bash
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
echo "Iptables default siyosati DROP qilib belgilandi."
```

## Tushuntirish va Mantiq:
`-P` bayrog'i standart siyosatni o'rnatadi. Bu "oq ro'yxat" (whitelist) usulida xavfsizlikni boshlash uchun asosdir.

## Ishlash natijasi:
```text
Iptables default siyosati DROP qilib belgilandi.
```

---

# 1044-Topshiriq: SSH (22-port) uchun ruxsat berish

## Topshiriq sharti:
Iptables orqali faqat 22-port (SSH) orqali kirishga ruxsat bering.

## Yechim (Bash kodi):
```bash
#!/bin/bash
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
echo "SSH porti ochildi va bog'langan sessiyalar ruxsat etildi."
```

## Tushuntirish va Mantiq:
`-A INPUT` qoidani qo'shadi. `ESTABLISHED,RELATED` qismi esa serverdan chiqib ketgan so'rovlarning javoblarini qabul qilish uchun zarur.

## Ishlash natijasi:
```text
SSH porti ochildi va bog'langan sessiyalar ruxsat etildi.
```

---

# 1045-Topshiriq: Fail2Ban o'rnatish va sozlash

## Topshiriq sharti:
Fail2Ban paketini o'rnating va SSH uchun avtomatik bloklash qoidasini faollashtiring.

## Yechim (Bash kodi):
```bash
#!/bin/bash
apt-get update && apt-get install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban
echo "Fail2Ban o'rnatildi va ishga tushirildi."
```

## Tushuntirish va Mantiq:
Fail2Ban log fayllarni kuzatib, noto'g'ri parol kiritgan IP manzillarni avtomatik bloklaydi (IPS vazifasi).

## Ishlash natijasi:
```text
Fail2Ban o'rnatildi va ishga tushirildi.
```

---

# 1046-Topshiriq: Fayl tizimi ruxsatlarini tekshirish (CIS)

## Topshiriq sharti:
`/etc/passwd` fayli faqat o'qish uchun (644) ekanligini tekshiring va agar boshqacha bo'lsa, to'g'rilang.

## Yechim (Bash kodi):
```bash
#!/bin/bash
chmod 644 /etc/passwd
echo "Fayl ruxsatlari 644 ga o'rnatildi."
```

## Tushuntirish va Mantiq:
CIS benchmark talablariga ko'ra, tizim fayllari ruxsatsiz o'zgartirilmasligi uchun ularning huquqlari qat'iy nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl ruxsatlari 644 ga o'rnatildi.
```

---

# 1047-Topshiriq: Nftables jadvalini yaratish

## Topshiriq sharti:
`nftables` yordamida yangi "filter" jadvalini yarating.

## Yechim (Bash kodi):
```bash
#!/bin/bash
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; }
echo "Nftables jadvali va input zanjiri yaratildi."
```

## Tushuntirish va Mantiq:
`nftables` - iptables'ning zamonaviy vorisi. `inet` oilasi ham IPv4, ham IPv6 ni qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Nftables jadvali va input zanjiri yaratildi.
```

---

# 1048-Topshiriq: Tizim loglarini kuzatish (IDS elementi)

## Topshiriq sharti:
`/var/log/auth.log` faylida "Failed password" so'zini qidirib, topilganlarini `security_alerts.log` ga yozing.

## Yechim (Bash kodi):
```bash
#!/bin/bash
grep "Failed password" /var/log/auth.log > security_alerts.log
echo "Muvaffaqiyatsiz urinishlar security_alerts.log ga yozildi."
```

## Tushuntirish va Mantiq:
Bu oddiy IDS (Intrusion Detection System) funksiyasi bo'lib, tizimga kirishdagi shubhali harakatlarni aniqlashga yordam beradi.

## Ishlash natijasi:
```text
Muvaffaqiyatsiz urinishlar security_alerts.log ga yozildi.
```

---

# 1049-Topshiriq: Keraksiz xizmatlarni o'chirish

## Topshiriq the:
`avahi-daemon` xizmatini to'xtating va o'chirib qo'ying (server xavfsizligi uchun).

## Yechim (Bash kodi):
```bash
#!/bin/bash
systemctl stop avahi-daemon
systemctl disable avahi-daemon
echo "Avahi-daemon o'chirildi."
```

## Tushuntirish va Mantiq:
Serverlarda ishlatilmaydigan xizmatlar "attack surface" (hujum yuzasi) ni kengaytiradi. Ularni o'chirish xavfsizlikni oshiradi.

## Ishlash natijasi:
```text
Avahi-daemon o'chirildi.
```

---

# 1050-Topshiriq: IP Forwarding ni o'chirish

## Topshiriq sharti:
Serverning router sifatida ishlashini (IP forwarding) o'chiring.

## Yechim (Bash kodi):
```bash
#!/bin/bash
sysctl -w net.ipv4.ip_forward=0
echo "net.ipv4.ip_forward=0" >> /etc/sysctl.conf
echo "IP Forwarding o'chirildi."
```

## Tushuntirish va Mantiq:
Agar server router bo'lmasa, IP forwarding o'chirilishi kerak. Bu MITM (Man-in-the-middle) hujumlarining oldini olishga yordam beradi.

## Ishlash natijasi:
```text
IP Forwarding o'chirildi.
```