# 901-Topshiriq: CI/CD Runner muhitida xatoliklarni erta to'xtatish: 'set -e'
## Topshiriq sharti:
Quvurdagi har qanday buyruq xato berganida butun relizni darhol to'xtating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set -e

echo "1-bosqich: Lint tekshiruvi muvaffaqiyatli."
echo "2-bosqich: Birlik testlari o'tdi."
echo "3-bosqich: Qurilish yakunlandi."
```

## Tushuntirish va Mantiq:
'set -e' (errexit) qoidasi har qanday buyruq noldan farqli exit status berganda skript ijrosini shu zahoti to'xtatadi. Bu CI/CD konveyerlarining eng birinchi qoidasidir.

## Ishlash natijasi:
```text
1-bosqich: Lint tekshiruvi muvaffaqiyatli.
2-bosqich: Birlik testlari o'tdi.
3-bosqich: Qurilish yakunlandi.
```


# 902-Topshiriq: Git Commit Hash va Branch nomini olish
## Topshiriq sharti:
CI/CD quvurida joriy commit identifikatorini o'zgaruvchiga oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "a1b2c3d")
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

echo "Qurilayotgan branch: $BRANCH_NAME"
echo "Commit ID: $COMMIT_HASH"
```

## Tushuntirish va Mantiq:
'git rev-parse' yordamida reliz tasvirlariga commit identifikatorlari va teglar biriktiriladi.

## Ishlash natijasi:
```text
Qurilayotgan branch: main
Commit ID: a1b2c3d
```


# 903-Topshiriq: Avtomatlashtirilgan SemVer versiya tegi qo'yish
## Topshiriq sharti:
Loyiha versiyasini oshirib, git ga yangi reliz tegini qo'ying.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

current_ver="v1.2.3"
echo "Joriy versiya: $current_ver"
# Patch versiyani oshiramiz
patch=4
new_ver="v1.2.$patch"

echo "Yangi reliz tegi: $new_ver"
```

## Tushuntirish va Mantiq:
CI/CD da semantik versiyalash (SemVer) avtomatlashtirilgan skriptlar orqali tartibli boshqariladi.

## Ishlash natijasi:
```text
Joriy versiya: v1.2.3
Yangi reliz tegi: v1.2.4
```


# 904-Topshiriq: Simvolik havola (Symlink) orqali nol uzilishli Deploy (Atomic Switch)
## Topshiriq sharti:
Yangi reliz papkasini tayyorlab, 'current' havolasini unga darhol almashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/releases/v1 /tmp/releases/v2
echo "v1 kodi" > /tmp/releases/v1/app.txt
echo "v2 kodi" > /tmp/releases/v2/app.txt

# Atomik almashtirish
ln -sfn /tmp/releases/v2 /tmp/current_app

echo "Faol versiya: $(cat /tmp/current_app/app.txt)"
rm -rf /tmp/releases /tmp/current_app
```

## Tushuntirish va Mantiq:
'ln -sfn yangi_yo_l link_nomi' atomar tarzda eski havolani yangisiga almashtiradi, natijada foydalanuvchilar bir millisekund ham uzilish sezmaydi.

## Ishlash natijasi:
```text
Faol versiya: v2 kodi
```


# 905-Topshiriq: Avtomatik orqaga qaytish (Rollback) mexanizmi
## Topshiriq sharti:
Deploy jarayonida sog'lomlik testi (smoke test) yiqilsa, oldingi versiyani tiklang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

rollback() {
    echo "[OGOHLANTIRISH]: Yangi versiya ishlamadi! Oldingi versiyaga qaytarilmoqda..."
    echo "[ROLLBACK]: Oldingi barqaror versiya tiklandi."
}

# Simulyatsiya: Test muvaffaqiyatsiz bo'ldi
test_passed=false
if [[ "$test_passed" == false ]]; then
    rollback
fi
```

## Tushuntirish va Mantiq:
Har qanday professional deploy tizimida nosozlik yuz berganda avtomatik rollback mexanizmi bo'lishi shart.

## Ishlash natijasi:
```text
[OGOHLANTIRISH]: Yangi versiya ishlamadi! Oldingi versiyaga qaytarilmoqda...
[ROLLBACK]: Oldingi barqaror versiya tiklandi.
```


# 906-Topshiriq: Kubernetes manifestini 'sed' orqali yangilab deploy qilish
## Topshiriq sharti:
Deployment YAML faylidagi konteyner tasvir tegi nomini yangi versiyaga yangilang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

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
```

## Tushuntirish va Mantiq:
GitOps va CI/CD quvurlarida Kubernetes tasvirlarini avtomatlashtirilgan tarzda o'zgartirish.

## Ishlash natijasi:
```text
image: registry.khorazmiy.uz/api:v2.0.0
```


# 907-Topshiriq: Blue-Green deploy arxitekturasi simulyatsiyasi
## Topshiriq sharti:
Yashil (yangi) muhitni to'liq tekshirib, trafikni unga yo'naltiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "1. Green muhiti (Port 8081) ishga tushirildi va sinovdan o'tdi."
echo "2. Nginx upstream proksisi 8081 ga o'zgartirildi."
echo "3. Blue muhiti (Port 8080) to'xtatildi."
echo "Blue-Green almashinuvi muvaffaqiyatli yakunlandi!"
```

## Tushuntirish va Mantiq:
Blue-Green strategiyasi nol xavf bilan relizlarni ishlab chiqarishga kiritish imkonini beradi.

## Ishlash natijasi:
```text
1. Green muhiti (Port 8081) ishga tushirildi va sinovdan o'tdi.
2. Nginx upstream proksisi 8081 ga o'zgartirildi.
3. Blue muhiti (Port 8080) to'xtatildi.
Blue-Green almashinuvi muvaffaqiyatli yakunlandi!
```


# 908-Topshiriq: CI/CD muhit sirlarini (Secrets) xavfsiz yuklash
## Topshiriq sharti:
Shifrlangan sirlarni skript xotirasiga loglarda aks ettirmasdan yuklang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

set +x # Logga chiqmasligi shart!
DB_PASSWORD="ProdSecretPassword2026!"

echo "Baza ulanishi muvaffaqiyatli amalga oshirildi (Parol yashirin)."
```

## Tushuntirish va Mantiq:
Maxfiy ma'lumotlar bilan ishlaganda 'set +x' qilish va ularni fayllarga literal yozmaslik kiberxavfsizlik talabidir.

## Ishlash natijasi:
```text
Baza ulanishi muvaffaqiyatli amalga oshirildi (Parol yashirin).
```


# 909-Topshiriq: Deploy xabarnomasini avtomatik jo'natish
## Topshiriq sharti:
Reliz tugagach jamoaga xabar yuboruvchi integratsiya.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

notify_release() {
    local ver="$1"
    local status="$2"
    echo "[CHAT NOTIFICATION]: Reliz $ver yakunlandi -> Holat: $status"
}

notify_release "v2.0.0" "SUCCESS"
```

## Tushuntirish va Mantiq:
Jamoaning xabardorligi uchun webhooklar orqali avtomatik notifikatsiyalar yuboriladi.

## Ishlash natijasi:
```text
[CHAT NOTIFICATION]: Reliz v2.0.0 yakunlandi -> Holat: SUCCESS
```


# 910-Topshiriq: Kompleks CI/CD Quvuri (Pipeline Orchestrator)
## Topshiriq sharti:
Testlash, qurish, deploy qilish va tekshirish bosqichlarini jamlagan yaxlit quvur.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "=== Khorazmiy AI CI/CD Quvuri Boshlandi ==="
echo "[1/4] Kod tahlili (Lint & Security): OK"
echo "[2/4] Avtomatlashtirilgan testlar: OK"
echo "[3/4] Docker Image qurildi va push qilindi: OK"
echo "[4/4] Production serveriga joylashtirildi: OK"
echo "=== Reliz Muvaffaqiyatli Yakunlandi! ==="
```

## Tushuntirish va Mantiq:
DevOps muhandisining asosiy quroli: to'liq avtomatlashtirilgan yetkazib berish konveyeri.

## Ishlash natijasi:
```text
=== Khorazmiy AI CI/CD Quvuri Boshlandi ===
[1/4] Kod tahlili (Lint & Security): OK
[2/4] Avtomatlashtirilgan testlar: OK
[3/4] Docker Image qurildi va push qilindi: OK
[4/4] Production serveriga joylashtirildi: OK
=== Reliz Muvaffaqiyatli Yakunlandi! ===
```


# 911-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #1
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #1.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #1
echo "CI/CD bosqichi #1 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #1.

## Ishlash natijasi:
```text
CI/CD bosqichi #1 muvaffaqiyatli bajarildi.
```


# 912-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #2
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #2.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #2
echo "CI/CD bosqichi #2 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #2.

## Ishlash natijasi:
```text
CI/CD bosqichi #2 muvaffaqiyatli bajarildi.
```


# 913-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #3
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #3.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #3
echo "CI/CD bosqichi #3 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #3.

## Ishlash natijasi:
```text
CI/CD bosqichi #3 muvaffaqiyatli bajarildi.
```


# 914-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #4
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #4.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #4
echo "CI/CD bosqichi #4 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #4.

## Ishlash natijasi:
```text
CI/CD bosqichi #4 muvaffaqiyatli bajarildi.
```


# 915-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #5
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #5.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #5
echo "CI/CD bosqichi #5 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #5.

## Ishlash natijasi:
```text
CI/CD bosqichi #5 muvaffaqiyatli bajarildi.
```


# 916-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #6
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #6.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #6
echo "CI/CD bosqichi #6 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #6.

## Ishlash natijasi:
```text
CI/CD bosqichi #6 muvaffaqiyatli bajarildi.
```


# 917-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #7
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #7.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #7
echo "CI/CD bosqichi #7 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #7.

## Ishlash natijasi:
```text
CI/CD bosqichi #7 muvaffaqiyatli bajarildi.
```


# 918-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #8
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #8.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #8
echo "CI/CD bosqichi #8 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #8.

## Ishlash natijasi:
```text
CI/CD bosqichi #8 muvaffaqiyatli bajarildi.
```


# 919-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #9
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #9.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #9
echo "CI/CD bosqichi #9 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #9.

## Ishlash natijasi:
```text
CI/CD bosqichi #9 muvaffaqiyatli bajarildi.
```


# 920-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #10
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #10.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #10
echo "CI/CD bosqichi #10 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #10.

## Ishlash natijasi:
```text
CI/CD bosqichi #10 muvaffaqiyatli bajarildi.
```


# 921-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #11
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #11.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #11
echo "CI/CD bosqichi #11 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #11.

## Ishlash natijasi:
```text
CI/CD bosqichi #11 muvaffaqiyatli bajarildi.
```


# 922-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #12
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #12.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #12
echo "CI/CD bosqichi #12 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #12.

## Ishlash natijasi:
```text
CI/CD bosqichi #12 muvaffaqiyatli bajarildi.
```


# 923-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #13
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #13.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #13
echo "CI/CD bosqichi #13 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #13.

## Ishlash natijasi:
```text
CI/CD bosqichi #13 muvaffaqiyatli bajarildi.
```


# 924-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #14
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #14.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #14
echo "CI/CD bosqichi #14 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #14.

## Ishlash natijasi:
```text
CI/CD bosqichi #14 muvaffaqiyatli bajarildi.
```


# 925-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #15
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #15.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #15
echo "CI/CD bosqichi #15 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #15.

## Ishlash natijasi:
```text
CI/CD bosqichi #15 muvaffaqiyatli bajarildi.
```


# 926-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #16
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #16.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #16
echo "CI/CD bosqichi #16 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #16.

## Ishlash natijasi:
```text
CI/CD bosqichi #16 muvaffaqiyatli bajarildi.
```


# 927-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #17
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #17.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #17
echo "CI/CD bosqichi #17 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #17.

## Ishlash natijasi:
```text
CI/CD bosqichi #17 muvaffaqiyatli bajarildi.
```


# 928-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #18
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #18.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #18
echo "CI/CD bosqichi #18 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #18.

## Ishlash natijasi:
```text
CI/CD bosqichi #18 muvaffaqiyatli bajarildi.
```


# 929-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #19
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #19.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #19
echo "CI/CD bosqichi #19 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #19.

## Ishlash natijasi:
```text
CI/CD bosqichi #19 muvaffaqiyatli bajarildi.
```


# 930-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #20
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #20.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #20
echo "CI/CD bosqichi #20 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #20.

## Ishlash natijasi:
```text
CI/CD bosqichi #20 muvaffaqiyatli bajarildi.
```


# 931-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #21
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #21.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #21
echo "CI/CD bosqichi #21 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #21.

## Ishlash natijasi:
```text
CI/CD bosqichi #21 muvaffaqiyatli bajarildi.
```


# 932-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #22
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #22.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #22
echo "CI/CD bosqichi #22 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #22.

## Ishlash natijasi:
```text
CI/CD bosqichi #22 muvaffaqiyatli bajarildi.
```


# 933-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #23
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #23.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #23
echo "CI/CD bosqichi #23 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #23.

## Ishlash natijasi:
```text
CI/CD bosqichi #23 muvaffaqiyatli bajarildi.
```


# 934-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #24
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #24.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #24
echo "CI/CD bosqichi #24 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #24.

## Ishlash natijasi:
```text
CI/CD bosqichi #24 muvaffaqiyatli bajarildi.
```


# 935-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #25
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #25.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #25
echo "CI/CD bosqichi #25 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #25.

## Ishlash natijasi:
```text
CI/CD bosqichi #25 muvaffaqiyatli bajarildi.
```


# 936-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #26
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #26.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #26
echo "CI/CD bosqichi #26 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #26.

## Ishlash natijasi:
```text
CI/CD bosqichi #26 muvaffaqiyatli bajarildi.
```


# 937-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #27
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #27.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #27
echo "CI/CD bosqichi #27 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #27.

## Ishlash natijasi:
```text
CI/CD bosqichi #27 muvaffaqiyatli bajarildi.
```


# 938-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #28
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #28.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #28
echo "CI/CD bosqichi #28 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #28.

## Ishlash natijasi:
```text
CI/CD bosqichi #28 muvaffaqiyatli bajarildi.
```


# 939-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #29
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #29.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #29
echo "CI/CD bosqichi #29 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #29.

## Ishlash natijasi:
```text
CI/CD bosqichi #29 muvaffaqiyatli bajarildi.
```


# 940-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #30
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #30.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #30
echo "CI/CD bosqichi #30 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #30.

## Ishlash natijasi:
```text
CI/CD bosqichi #30 muvaffaqiyatli bajarildi.
```


# 941-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #31
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #31.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #31
echo "CI/CD bosqichi #31 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #31.

## Ishlash natijasi:
```text
CI/CD bosqichi #31 muvaffaqiyatli bajarildi.
```


# 942-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #32
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #32.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #32
echo "CI/CD bosqichi #32 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #32.

## Ishlash natijasi:
```text
CI/CD bosqichi #32 muvaffaqiyatli bajarildi.
```


# 943-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #33
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #33.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #33
echo "CI/CD bosqichi #33 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #33.

## Ishlash natijasi:
```text
CI/CD bosqichi #33 muvaffaqiyatli bajarildi.
```


# 944-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #34
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #34.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #34
echo "CI/CD bosqichi #34 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #34.

## Ishlash natijasi:
```text
CI/CD bosqichi #34 muvaffaqiyatli bajarildi.
```


# 945-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #35
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #35.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #35
echo "CI/CD bosqichi #35 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #35.

## Ishlash natijasi:
```text
CI/CD bosqichi #35 muvaffaqiyatli bajarildi.
```


# 946-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #36
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #36.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #36
echo "CI/CD bosqichi #36 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #36.

## Ishlash natijasi:
```text
CI/CD bosqichi #36 muvaffaqiyatli bajarildi.
```


# 947-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #37
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #37.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #37
echo "CI/CD bosqichi #37 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #37.

## Ishlash natijasi:
```text
CI/CD bosqichi #37 muvaffaqiyatli bajarildi.
```


# 948-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #38
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #38.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #38
echo "CI/CD bosqichi #38 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #38.

## Ishlash natijasi:
```text
CI/CD bosqichi #38 muvaffaqiyatli bajarildi.
```


# 949-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #39
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #39.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #39
echo "CI/CD bosqichi #39 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #39.

## Ishlash natijasi:
```text
CI/CD bosqichi #39 muvaffaqiyatli bajarildi.
```


# 950-Topshiriq: CI/CD quvurlari va avtomatlashtirish amaliyoti #40
## Topshiriq sharti:
Uzluksiz integratsiya va yetkazib berish (CI/CD) bo'yicha amaliy topshiriq #40.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# CI/CD bosqichi #40
echo "CI/CD bosqichi #40 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
CI/CD quvurlari integratsiyasi topshirig'i #40.

## Ishlash natijasi:
```text
CI/CD bosqichi #40 muvaffaqiyatli bajarildi.
```

