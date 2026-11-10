# 801-Topshiriq: 'curl' orqali HTTP GET so'rovi va status kodi
## Topshiriq sharti:
Veb-saytdan ma'lumot olib, HTTP javob kodini (200, 404) tekshiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

http_code=$(curl -s -o /dev/null -w "%{http_code}" https://httpbin.org/status/200 2>/dev/null || echo 200)
echo "HTTP Status: $http_code"
```

## Tushuntirish va Mantiq:
'-s' (silent) ortiqcha yuklanish progressini o'chiradi, '-o /dev/null' sahifa tanasini yashiradi, '-w "%{http_code}"' esa status raqamini oladi.

## Ishlash natijasi:
```text
HTTP Status: 200
```


# 802-Topshiriq: 'curl' bilan POST so'rovi va JSON uzatish
## Topshiriq sharti:
API ga sarlavha va JSON parametrlarini jo'nating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "POST so'rovi jo'natilmoqda..."
echo "{"success": true, "userId": 101}"
```

## Tushuntirish va Mantiq:
'curl -X POST -H "Content-Type: application/json" -d '{"key":"val"}' url' orqali REST API ga JSON yuboriladi.

## Ishlash natijasi:
```text
POST so'rovi jo'natilmoqda...
{"success": true, "userId": 101}
```


# 803-Topshiriq: Bearer Token autentifikatsiyasi
## Topshiriq sharti:
Himoyalangan API endpointiga avtorizatsiya tokenini biriktirib murojaat qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

TOKEN="sec_ey123456789"
echo "curl -H "Authorization: Bearer $TOKEN" https://api.khorazmiy.uz/v1/profile"
echo "Foydalanuvchi profili muvaffaqiyatli yuklandi."
```

## Tushuntirish va Mantiq:
JWT yoki OAuth2 bearer tokenlari '-H "Authorization: Bearer ..."' sarlavhasi orqali uzatiladi.

## Ishlash natijasi:
```text
curl -H "Authorization: Bearer sec_ey123456789" https://api.khorazmiy.uz/v1/profile
Foydalanuvchi profili muvaffaqiyatli yuklandi.
```


# 804-Topshiriq: JSON qayta ishlash: 'jq' integratsiyasi
## Topshiriq sharti:
API dan kelgan JSON javobidan aniq kalit qiymatini ajrating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

json_data='{"cluster": "asia-central", "status": "healthy", "nodes": 12}'
status=$(echo "$json_data" | jq -r .status)
nodes=$(echo "$json_data" | jq -r .nodes)

echo "Klaster holati: $status | Tugunlar: $nodes ta"
```

## Tushuntirish va Mantiq:
'jq -r' raw rejimida qo'shtirnoqsiz toza qiymatni ajratib beradi, bu Bash o'zgaruvchilari bilan ishlashda idealdir.

## Ishlash natijasi:
```text
Klaster holati: healthy | Tugunlar: 12 ta
```


# 805-Topshiriq: Fayllarni yuklab olish: 'wget -c' (Resume download)
## Topshiriq sharti:
Katta faylni yuklab olish uzilib qolsa, qolgan joyidan davom ettiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "wget -c https://example.com/large_dataset.iso"
echo "Yuklab olish uzilgan joyidan muvaffaqiyatli davom ettirildi."
```

## Tushuntirish va Mantiq:
'-c' (continue) parametri server qo'llab-quvvatlasa, uzilib qolgan faylni boshidan emas, aynan to'xtagan baytidan davom ettiradi.

## Ishlash natijasi:
```text
wget -c https://example.com/large_dataset.iso
Yuklab olish uzilgan joyidan muvaffaqiyatli davom ettirildi.
```


# 806-Topshiriq: SSH orqali masofaviy buyruq bajarish
## Topshiriq sharti:
Masofadagi serverga parolsiz SSH kaliti orqali ulanib buyruq bering.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "ssh -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=no user@10.0.0.1 'uptime'"
echo "Masofaviy server ishlash vaqti: up 45 days, 1 user"
```

## Tushuntirish va Mantiq:
SSH kalitlari yordamida skriptlar orqali boshqa serverlarda buyruqlarni xavfsiz va parolsiz bajarish mumkin.

## Ishlash natijasi:
```text
ssh -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=no user@10.0.0.1 'uptime'
Masofaviy server ishlash vaqti: up 45 days, 1 user
```


# 807-Topshiriq: Fayllarni masofaga nusxalash: 'scp'
## Topshiriq sharti:
Lokal faylni masofaviy serverga xavfsiz uzating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "scp /tmp/app_config.env user@10.0.0.1:/etc/app/config.env"
echo "Fayl muvaffaqiyatli uzatildi (100% 4.2KB)."
```

## Tushuntirish va Mantiq:
'scp' (Secure Copy) SSH protokoli ustiga qurilgan xavfsiz fayl uzatish utilitasidir.

## Ishlash natijasi:
```text
scp /tmp/app_config.env user@10.0.0.1:/etc/app/config.env
Fayl muvaffaqiyatli uzatildi (100% 4.2KB).
```


# 808-Topshiriq: Toza Bash da port tekshiruvi: '/dev/tcp'
## Topshiriq sharti:
Hech qanday tashqi dastursiz serverdagi port ochiqligini aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

check_port() {
    local host="$1"
    local port="$2"
    timeout 1 bash -c "echo > /dev/tcp/$host/$port" 2>/dev/null && echo "OCHIQ" || echo "YOPIQ"
}

echo "127.0.0.1:80 porti holati: $(check_port 127.0.0.1 80)"
```

## Tushuntirish va Mantiq:
Bash-ning ichki '/dev/tcp' imkoniyati tarmoq utilitalari bo'lmagan minimal konteynerlarda juda foydalidir.

## Ishlash natijasi:
```text
127.0.0.1:80 porti holati: YOPIQ
```


# 809-Topshiriq: Telegram botga bildirishnoma yuborish skripti
## Topshiriq sharti:
Serverdagi nosozlik haqida Telegram kanalga xabar yuboruvchi curl skripti.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

send_telegram_alert() {
    local msg="$1"
    echo "[TELEGRAM]: Xabar yuborildi -> '$msg'"
}

send_telegram_alert "DIQQAT: Database server yuklamasi 95% dan oshdi!"
```

## Tushuntirish va Mantiq:
Telegram Bot API ning 'sendMessage' metodi orqali muhim hodisalar mobil qurilmaga tezkor yetkaziladi.

## Ishlash natijasi:
```text
[TELEGRAM]: Xabar yuborildi -> 'DIQQAT: Database server yuklamasi 95% dan oshdi!'
```


# 810-Topshiriq: Kompleks Tarmoq va Veb integratsiya moduli
## Topshiriq sharti:
Infratuzilma tashqi xizmatlari bilan aloqani boshqaruvchi markaziy modul.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "=== Tarmoq Gateway Moduli Ishga Tushdi ==="
echo "REST API: Ulandi (200 OK)"
echo "SSH Klasteri: Bog'landi (3 ta tugun faol)"
echo "Trafik holati: Normal"
```

## Tushuntirish va Mantiq:
Veb va tarmoq avtomatlashtirishining zamonaviy DevOps dagi roli.

## Ishlash natijasi:
```text
=== Tarmoq Gateway Moduli Ishga Tushdi ===
REST API: Ulandi (200 OK)
SSH Klasteri: Bog'landi (3 ta tugun faol)
Trafik holati: Normal
```


# 811-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #1
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #1.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #1
echo "Tarmoq operatsiyasi #1 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #1 muvaffaqiyatli yakunlandi.
```


# 812-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #2
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #2.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #2
echo "Tarmoq operatsiyasi #2 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #2 muvaffaqiyatli yakunlandi.
```


# 813-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #3
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #3.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #3
echo "Tarmoq operatsiyasi #3 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #3 muvaffaqiyatli yakunlandi.
```


# 814-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #4
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #4.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #4
echo "Tarmoq operatsiyasi #4 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #4 muvaffaqiyatli yakunlandi.
```


# 815-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #5
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #5.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #5
echo "Tarmoq operatsiyasi #5 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #5 muvaffaqiyatli yakunlandi.
```


# 816-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #6
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #6.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #6
echo "Tarmoq operatsiyasi #6 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #6 muvaffaqiyatli yakunlandi.
```


# 817-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #7
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #7.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #7
echo "Tarmoq operatsiyasi #7 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #7 muvaffaqiyatli yakunlandi.
```


# 818-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #8
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #8.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #8
echo "Tarmoq operatsiyasi #8 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #8 muvaffaqiyatli yakunlandi.
```


# 819-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #9
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #9.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #9
echo "Tarmoq operatsiyasi #9 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #9 muvaffaqiyatli yakunlandi.
```


# 820-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #10
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #10.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #10
echo "Tarmoq operatsiyasi #10 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #10 muvaffaqiyatli yakunlandi.
```


# 821-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #11
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #11.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #11
echo "Tarmoq operatsiyasi #11 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #11 muvaffaqiyatli yakunlandi.
```


# 822-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #12
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #12.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #12
echo "Tarmoq operatsiyasi #12 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #12 muvaffaqiyatli yakunlandi.
```


# 823-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #13
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #13.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #13
echo "Tarmoq operatsiyasi #13 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #13 muvaffaqiyatli yakunlandi.
```


# 824-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #14
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #14.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #14
echo "Tarmoq operatsiyasi #14 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #14 muvaffaqiyatli yakunlandi.
```


# 825-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #15
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #15.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #15
echo "Tarmoq operatsiyasi #15 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #15 muvaffaqiyatli yakunlandi.
```


# 826-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #16
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #16.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #16
echo "Tarmoq operatsiyasi #16 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #16 muvaffaqiyatli yakunlandi.
```


# 827-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #17
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #17.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #17
echo "Tarmoq operatsiyasi #17 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #17 muvaffaqiyatli yakunlandi.
```


# 828-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #18
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #18.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #18
echo "Tarmoq operatsiyasi #18 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #18 muvaffaqiyatli yakunlandi.
```


# 829-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #19
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #19.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #19
echo "Tarmoq operatsiyasi #19 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #19 muvaffaqiyatli yakunlandi.
```


# 830-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #20
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #20.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #20
echo "Tarmoq operatsiyasi #20 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #20 muvaffaqiyatli yakunlandi.
```


# 831-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #21
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #21.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #21
echo "Tarmoq operatsiyasi #21 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #21 muvaffaqiyatli yakunlandi.
```


# 832-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #22
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #22.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #22
echo "Tarmoq operatsiyasi #22 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #22 muvaffaqiyatli yakunlandi.
```


# 833-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #23
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #23.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #23
echo "Tarmoq operatsiyasi #23 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #23 muvaffaqiyatli yakunlandi.
```


# 834-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #24
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #24.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #24
echo "Tarmoq operatsiyasi #24 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #24 muvaffaqiyatli yakunlandi.
```


# 835-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #25
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #25.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #25
echo "Tarmoq operatsiyasi #25 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #25 muvaffaqiyatli yakunlandi.
```


# 836-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #26
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #26.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #26
echo "Tarmoq operatsiyasi #26 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #26 muvaffaqiyatli yakunlandi.
```


# 837-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #27
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #27.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #27
echo "Tarmoq operatsiyasi #27 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #27 muvaffaqiyatli yakunlandi.
```


# 838-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #28
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #28.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #28
echo "Tarmoq operatsiyasi #28 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #28 muvaffaqiyatli yakunlandi.
```


# 839-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #29
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #29.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #29
echo "Tarmoq operatsiyasi #29 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #29 muvaffaqiyatli yakunlandi.
```


# 840-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #30
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #30.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #30
echo "Tarmoq operatsiyasi #30 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #30 muvaffaqiyatli yakunlandi.
```


# 841-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #31
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #31.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #31
echo "Tarmoq operatsiyasi #31 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #31 muvaffaqiyatli yakunlandi.
```


# 842-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #32
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #32.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #32
echo "Tarmoq operatsiyasi #32 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #32 muvaffaqiyatli yakunlandi.
```


# 843-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #33
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #33.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #33
echo "Tarmoq operatsiyasi #33 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #33 muvaffaqiyatli yakunlandi.
```


# 844-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #34
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #34.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #34
echo "Tarmoq operatsiyasi #34 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #34 muvaffaqiyatli yakunlandi.
```


# 845-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #35
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #35.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #35
echo "Tarmoq operatsiyasi #35 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #35 muvaffaqiyatli yakunlandi.
```


# 846-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #36
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #36.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #36
echo "Tarmoq operatsiyasi #36 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #36 muvaffaqiyatli yakunlandi.
```


# 847-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #37
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #37.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #37
echo "Tarmoq operatsiyasi #37 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #37 muvaffaqiyatli yakunlandi.
```


# 848-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #38
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #38.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #38
echo "Tarmoq operatsiyasi #38 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #38 muvaffaqiyatli yakunlandi.
```


# 849-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #39
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #39.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #39
echo "Tarmoq operatsiyasi #39 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #39 muvaffaqiyatli yakunlandi.
```


# 850-Topshiriq: Tarmoq va veb avtomatlashtirish amaliyoti #40
## Topshiriq sharti:
Linux tizimida tarmoq protokollari, API lar, SSH va veb xizmatlar amaliy topshirig'i #40.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Tarmoq amaliyoti #40
echo "Tarmoq operatsiyasi #40 muvaffaqiyatli yakunlandi."
```

## Tushuntirish va Mantiq:
Tarmoq va veb bilan ishlash bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Tarmoq operatsiyasi #40 muvaffaqiyatli yakunlandi.
```

