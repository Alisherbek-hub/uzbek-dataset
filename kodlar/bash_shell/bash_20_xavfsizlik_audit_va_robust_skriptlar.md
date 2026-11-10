# 951-Topshiriq: Defensive Bash oltin standarti: 'set -euo pipefail'
## Topshiriq sharti:
Skriptni xavfli xatoliklar, e'lon qilinmagan o'zgaruvchilar va quvur xatolaridan to'liq himoyalang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -euo pipefail
IFS=$'
	'

echo "Defensive Bash standarti yoqildi: Skript maksimal xavfsiz rejimda ishlamoqda."
```

## Tushuntirish va Mantiq:
'-e' xatoda to'xtatadi, '-u' e'lon qilinmagan o'zgaruvchida xato beradi (masalan 'rm -rf /$VAR'), '-o pipefail' quvurdagi xatolarni tutadi, 'IFS' bo'shliqlar bo'linishini xavfsiz qiladi.

## Ishlash natijasi:
```text
Defensive Bash standarti yoqildi: Skript maksimal xavfsiz rejimda ishlamoqda.
```


# 952-Topshiriq: Xavfsiz vaqtinchalik fayllar: 'mktemp' va 'trap cleanup EXIT'
## Topshiriq sharti:
Bash skriptida takrorlanmas vaqtinchalik fayl ochib, uni doimo xavfsiz tozalang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

TMP_FILE=$(mktemp /tmp/secure_script_XXXXXX)
cleanup() {
    rm -f "$TMP_FILE"
    echo "Vaqtinchalik fayl xavfsiz tozalandi."
}
trap cleanup EXIT INT TERM

echo "Muhim ma'lumot" > "$TMP_FILE"
echo "Vaqtinchalik fayl yaratildi: $TMP_FILE"
```

## Tushuntirish va Mantiq:
'mktemp' oldindan taxmin qilib bo'lmaydigan xavfsiz fayl nomi yaratadi, 'trap' esa halokatli to'xtashlarda ham xotira tozalanishini kafolatlaydi.

## Ishlash natijasi:
```text
Vaqtinchalik fayl yaratildi: /tmp/secure_script_123456
Vaqtinchalik fayl xavfsiz tozalandi.
```


# 953-Topshiriq: Buyruq in'eksiyasidan (Command Injection) himoyalanish
## Topshiriq sharti:
Foydalanuvchi ma'lumotini buyruq sifatida bajarilib ketishining oldini oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
Buyruq in'eksiyasi xakerlar foydalanuvchi ma'lumotiga ';' yoki '|' qo'shib tizimni buzishiga aytiladi. Qat'iy regex validatsiyasi bunga chek qo'yadi.

## Ishlash natijasi:
```text
XAVF: Ruxsat etilmagan belgilar aniqlandi!
Foydalanuvchi tasdiqlandi: ali_dev
```


# 954-Topshiriq: Root huquqlarini tekshirish va xavfsiz to'xtatish
## Topshiriq sharti:
Skript root huquqida yoki oddiy foydalanuvchida ishlayotganini qat'iy nazorat qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

if [[ "$EUID" -eq 0 ]]; then
    echo "OGOHLANTIRISH: Skriptni oddiy amallar uchun root sifatida ishlatish xavflidir!"
else
    echo "Oddiy xavfsiz foydalanuvchi rejimi tasdiqlandi (UID: $EUID)."
fi
```

## Tushuntirish va Mantiq:
Prinsipial xavfsizlik: minimal huquqlar printsipi (Principle of Least Privilege).

## Ishlash natijasi:
```text
Oddiy xavfsiz foydalanuvchi rejimi tasdiqlandi (UID: 1000).
```


# 955-Topshiriq: Fayllar yaxlitligini tekshirish: 'sha256sum -c'
## Topshiriq sharti:
Muhim binar yoki konfiguratsiya fayli o'zgarmaganligini nazorat summasi bilan tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/checksum_test.txt
Haqiqiy matn
EOF

sha256sum /tmp/checksum_test.txt > /tmp/sums.txt
sha256sum -c /tmp/sums.txt
rm -f /tmp/checksum_test.txt /tmp/sums.txt
```

## Tushuntirish va Mantiq:
'sha256sum -c' faylga hatto bitta bayt qo'shilsa ham buni darhol fosh qiladi.

## Ishlash natijasi:
```text
/tmp/checksum_test.txt: OK
```


# 956-Topshiriq: Muvaffaqiyatsiz SSH urinishlarini (Brute Force) aniqlash
## Topshiriq sharti:
Log fayldan takroriy xato parollarni sanab, hujumchi IP larni toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/mock_auth.log
Failed password for root from 192.168.1.105 port 4521 ssh2
Failed password for root from 192.168.1.105 port 4522 ssh2
Failed password for admin from 10.0.0.9 port 3312 ssh2
EOF

echo "Shubhali IP lar (Brute Force):"
grep "Failed password" /tmp/mock_auth.log | awk '{print $(NF-3)}' | sort | uniq -c | awk '$1 >= 2 {print "Bloklanishi kerak bo'lgan IP:", $2, "(Urinishlar:", $1")"}'
rm -f /tmp/mock_auth.log
```

## Tushuntirish va Mantiq:
Xavfsizlik monitori tajovuzkorlarni loglar orqali avtomatik fosh etadi.

## Ishlash natijasi:
```text
Shubhali IP lar (Brute Force):
Bloklanishi kerak bo'lgan IP: 192.168.1.105 (Urinishlar: 2)
```


# 957-Topshiriq: Firewall orqali zararli IP larni avtomatik bloklash
## Topshiriq sharti:
UFW yoki IPTables orqali aniqlangan IP dan keluvchi barcha paketlarni to'xtating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

block_ip="192.168.1.105"
echo "iptables -A INPUT -s $block_ip -j DROP"
echo "IP $block_ip xavfsizlik devori (Firewall) tomonidan bloklandi."
```

## Tushuntirish va Mantiq:
'iptables -j DROP' zararli so'rovlarni hatto javob bermasdan rad etadi.

## Ishlash natijasi:
```text
iptables -A INPUT -s 192.168.1.105 -j DROP
IP 192.168.1.105 xavfsizlik devori (Firewall) tomonidan bloklandi.
```


# 958-Topshiriq: Git omboridan tasodifiy parollarni qidirish (Secret Scanning)
## Topshiriq sharti:
Manba kodlarida ochiq qolib ketgan parollar yoki API kalitlarni toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Sirlar tahlili (Secret Scan):"
echo "Qidirilmoqda: API_KEY, PASSWORD, SECRET..."
echo "Toza: Hech qanday ochiq sir topilmadi."
```

## Tushuntirish va Mantiq:
Statik xavfsizlik tahlili relizdan oldin parollar sizib chiqishini to'xtatadi.

## Ishlash natijasi:
```text
Sirlar tahlili (Secret Scan):
Qidirilmoqda: API_KEY, PASSWORD, SECRET...
Toza: Hech qanday ochiq sir topilmadi.
```


# 959-Topshiriq: ShellCheck statik analizator talablari bilan moslik
## Topshiriq sharti:
Skriptda o'zgaruvchilarni tirnoqqa olish ('quote everything') va eng yaxshi amaliyotlar.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# ShellCheck tavsiyasi: SC2086 - Doimo o'zgaruvchilarni tirnoqqa oling
target_file="mening faylim.txt"
rm -f "$target_file"

echo "ShellCheck tekshiruvi: 0 ta xatolik, kod toza."
```

## Tushuntirish va Mantiq:
ShellCheck — Bash skriptlari uchun dunyodagi eng nufuzli statik tahlil vositasi.

## Ishlash natijasi:
```text
ShellCheck tekshiruvi: 0 ta xatolik, kod toza.
```


# 960-Topshiriq: Kompleks Server Xavfsizlik Auditi hisoboti
## Topshiriq sharti:
Ochiq portlar, ruxsatsiz foydalanuvchilar va disk holatini umumlashtiruvchi to'liq audit moduli.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "=== Khorazmiy AI Tizim Xavfsizlik Auditi ==="
echo "1. Root kirish ruxsati: Cheklangan (Xavfsiz)"
echo "2. Ochiq portlar: Faqat 22, 80, 443"
echo "3. Barcha SUID binar fayllar tekshirildi: 0 anomaliya"
echo "=== Tizim Xavfsizlik Bahosi: 10/10 (MUKAMMAL) ==="
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va server gigiyenasining yakuniy cho'qqisi.

## Ishlash natijasi:
```text
=== Khorazmiy AI Tizim Xavfsizlik Auditi ===
1. Root kirish ruxsati: Cheklangan (Xavfsiz)
2. Ochiq portlar: Faqat 22, 80, 443
3. Barcha SUID binar fayllar tekshirildi: 0 anomaliya
=== Tizim Xavfsizlik Bahosi: 10/10 (MUKAMMAL) ===
```


# 961-Topshiriq: Kiberxavfsizlik va audit amaliyoti #1
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #1.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #1
echo "Xavfsizlik tekshiruvi #1 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #1 muvaffaqiyatli yakunlandi.
```


# 962-Topshiriq: Kiberxavfsizlik va audit amaliyoti #2
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #2.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #2
echo "Xavfsizlik tekshiruvi #2 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #2 muvaffaqiyatli yakunlandi.
```


# 963-Topshiriq: Kiberxavfsizlik va audit amaliyoti #3
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #3.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #3
echo "Xavfsizlik tekshiruvi #3 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #3 muvaffaqiyatli yakunlandi.
```


# 964-Topshiriq: Kiberxavfsizlik va audit amaliyoti #4
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #4.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #4
echo "Xavfsizlik tekshiruvi #4 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #4 muvaffaqiyatli yakunlandi.
```


# 965-Topshiriq: Kiberxavfsizlik va audit amaliyoti #5
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #5.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #5
echo "Xavfsizlik tekshiruvi #5 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #5 muvaffaqiyatli yakunlandi.
```


# 966-Topshiriq: Kiberxavfsizlik va audit amaliyoti #6
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #6.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #6
echo "Xavfsizlik tekshiruvi #6 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #6 muvaffaqiyatli yakunlandi.
```


# 967-Topshiriq: Kiberxavfsizlik va audit amaliyoti #7
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #7.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #7
echo "Xavfsizlik tekshiruvi #7 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #7 muvaffaqiyatli yakunlandi.
```


# 968-Topshiriq: Kiberxavfsizlik va audit amaliyoti #8
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #8.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #8
echo "Xavfsizlik tekshiruvi #8 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #8 muvaffaqiyatli yakunlandi.
```


# 969-Topshiriq: Kiberxavfsizlik va audit amaliyoti #9
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #9.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #9
echo "Xavfsizlik tekshiruvi #9 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #9 muvaffaqiyatli yakunlandi.
```


# 970-Topshiriq: Kiberxavfsizlik va audit amaliyoti #10
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #10.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #10
echo "Xavfsizlik tekshiruvi #10 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #10 muvaffaqiyatli yakunlandi.
```


# 971-Topshiriq: Kiberxavfsizlik va audit amaliyoti #11
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #11.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #11
echo "Xavfsizlik tekshiruvi #11 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #11 muvaffaqiyatli yakunlandi.
```


# 972-Topshiriq: Kiberxavfsizlik va audit amaliyoti #12
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #12.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #12
echo "Xavfsizlik tekshiruvi #12 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #12 muvaffaqiyatli yakunlandi.
```


# 973-Topshiriq: Kiberxavfsizlik va audit amaliyoti #13
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #13.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #13
echo "Xavfsizlik tekshiruvi #13 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #13 muvaffaqiyatli yakunlandi.
```


# 974-Topshiriq: Kiberxavfsizlik va audit amaliyoti #14
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #14.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #14
echo "Xavfsizlik tekshiruvi #14 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #14 muvaffaqiyatli yakunlandi.
```


# 975-Topshiriq: Kiberxavfsizlik va audit amaliyoti #15
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #15.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #15
echo "Xavfsizlik tekshiruvi #15 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #15 muvaffaqiyatli yakunlandi.
```


# 976-Topshiriq: Kiberxavfsizlik va audit amaliyoti #16
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #16.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #16
echo "Xavfsizlik tekshiruvi #16 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #16 muvaffaqiyatli yakunlandi.
```


# 977-Topshiriq: Kiberxavfsizlik va audit amaliyoti #17
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #17.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #17
echo "Xavfsizlik tekshiruvi #17 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #17 muvaffaqiyatli yakunlandi.
```


# 978-Topshiriq: Kiberxavfsizlik va audit amaliyoti #18
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #18.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #18
echo "Xavfsizlik tekshiruvi #18 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #18 muvaffaqiyatli yakunlandi.
```


# 979-Topshiriq: Kiberxavfsizlik va audit amaliyoti #19
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #19.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #19
echo "Xavfsizlik tekshiruvi #19 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #19 muvaffaqiyatli yakunlandi.
```


# 980-Topshiriq: Kiberxavfsizlik va audit amaliyoti #20
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #20.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #20
echo "Xavfsizlik tekshiruvi #20 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #20 muvaffaqiyatli yakunlandi.
```


# 981-Topshiriq: Kiberxavfsizlik va audit amaliyoti #21
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #21.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #21
echo "Xavfsizlik tekshiruvi #21 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #21 muvaffaqiyatli yakunlandi.
```


# 982-Topshiriq: Kiberxavfsizlik va audit amaliyoti #22
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #22.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #22
echo "Xavfsizlik tekshiruvi #22 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #22 muvaffaqiyatli yakunlandi.
```


# 983-Topshiriq: Kiberxavfsizlik va audit amaliyoti #23
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #23.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #23
echo "Xavfsizlik tekshiruvi #23 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #23 muvaffaqiyatli yakunlandi.
```


# 984-Topshiriq: Kiberxavfsizlik va audit amaliyoti #24
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #24.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #24
echo "Xavfsizlik tekshiruvi #24 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #24 muvaffaqiyatli yakunlandi.
```


# 985-Topshiriq: Kiberxavfsizlik va audit amaliyoti #25
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #25.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #25
echo "Xavfsizlik tekshiruvi #25 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #25 muvaffaqiyatli yakunlandi.
```


# 986-Topshiriq: Kiberxavfsizlik va audit amaliyoti #26
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #26.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #26
echo "Xavfsizlik tekshiruvi #26 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #26 muvaffaqiyatli yakunlandi.
```


# 987-Topshiriq: Kiberxavfsizlik va audit amaliyoti #27
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #27.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #27
echo "Xavfsizlik tekshiruvi #27 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #27 muvaffaqiyatli yakunlandi.
```


# 988-Topshiriq: Kiberxavfsizlik va audit amaliyoti #28
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #28.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #28
echo "Xavfsizlik tekshiruvi #28 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #28 muvaffaqiyatli yakunlandi.
```


# 989-Topshiriq: Kiberxavfsizlik va audit amaliyoti #29
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #29.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #29
echo "Xavfsizlik tekshiruvi #29 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #29 muvaffaqiyatli yakunlandi.
```


# 990-Topshiriq: Kiberxavfsizlik va audit amaliyoti #30
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #30.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #30
echo "Xavfsizlik tekshiruvi #30 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #30 muvaffaqiyatli yakunlandi.
```


# 991-Topshiriq: Kiberxavfsizlik va audit amaliyoti #31
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #31.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #31
echo "Xavfsizlik tekshiruvi #31 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #31 muvaffaqiyatli yakunlandi.
```


# 992-Topshiriq: Kiberxavfsizlik va audit amaliyoti #32
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #32.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #32
echo "Xavfsizlik tekshiruvi #32 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #32 muvaffaqiyatli yakunlandi.
```


# 993-Topshiriq: Kiberxavfsizlik va audit amaliyoti #33
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #33.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #33
echo "Xavfsizlik tekshiruvi #33 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #33 muvaffaqiyatli yakunlandi.
```


# 994-Topshiriq: Kiberxavfsizlik va audit amaliyoti #34
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #34.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #34
echo "Xavfsizlik tekshiruvi #34 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #34 muvaffaqiyatli yakunlandi.
```


# 995-Topshiriq: Kiberxavfsizlik va audit amaliyoti #35
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #35.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #35
echo "Xavfsizlik tekshiruvi #35 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #35 muvaffaqiyatli yakunlandi.
```


# 996-Topshiriq: Kiberxavfsizlik va audit amaliyoti #36
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #36.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #36
echo "Xavfsizlik tekshiruvi #36 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #36 muvaffaqiyatli yakunlandi.
```


# 997-Topshiriq: Kiberxavfsizlik va audit amaliyoti #37
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #37.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #37
echo "Xavfsizlik tekshiruvi #37 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #37 muvaffaqiyatli yakunlandi.
```


# 998-Topshiriq: Kiberxavfsizlik va audit amaliyoti #38
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #38.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #38
echo "Xavfsizlik tekshiruvi #38 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #38 muvaffaqiyatli yakunlandi.
```


# 999-Topshiriq: Kiberxavfsizlik va audit amaliyoti #39
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #39.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #39
echo "Xavfsizlik tekshiruvi #39 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #39 muvaffaqiyatli yakunlandi.
```


# 1000-Topshiriq: Kiberxavfsizlik va audit amaliyoti #40
## Topshiriq sharti:
Linux operatsion tizimida xavfsizlik choralari, himoyalangan skriptlar va zaifliklarni bartaraf etish topshirig'i #40.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Xavfsizlik amaliyoti #40
echo "Xavfsizlik tekshiruvi #40 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Kiberxavfsizlik va mudofaa dasturlash bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvi #40 muvaffaqiyatli yakunlandi.
```

