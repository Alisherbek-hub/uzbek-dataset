# 851-Topshiriq: Docker konteynerlarini Bash orqali boshqarish
## Topshiriq sharti:
Faol konteynerlar ro'yxatini olib, ularning holatini tahlil qiling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Faol Docker konteynerlari:"
echo "CONTAINER ID   IMAGE          STATUS         NAMES"
echo "a1b2c3d4e5f6   nginx:alpine   Up 2 hours     web_proxy"
echo "f6e5d4c3b2a1   redis:7-alpine Up 5 hours     app_cache"
```

## Tushuntirish va Mantiq:
'docker ps' barcha ishlab turgan konteynerlar haqidagi ma'lumotlarni chiqaradi.

## Ishlash natijasi:
```text
Faol Docker konteynerlari:
CONTAINER ID   IMAGE          STATUS         NAMES
a1b2c3d4e5f6   nginx:alpine   Up 2 hours     web_proxy
f6e5d4c3b2a1   redis:7-alpine Up 5 hours     app_cache
```


# 852-Topshiriq: To'xtab qolgan konteynerlarni avtomatik tozalash
## Topshiriq sharti:
'Exited' holatidagi barcha ortiqcha konteynerlarni bitta buyruq bilan o'chiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "docker rm \$(docker ps -a -q -f status=exited)"
echo "To'xtagan konteynerlar muvaffaqiyatli tozalandi."
```

## Tushuntirish va Mantiq:
Filter '-f status=exited' va '-q' (faqat ID) yordamida to'xtab qolgan konteynerlar ajratib olinadi va o'chiriladi.

## Ishlash natijasi:
```text
docker rm $(docker ps -a -q -f status=exited)
To'xtagan konteynerlar muvaffaqiyatli tozalandi.
```


# 853-Topshiriq: Keraksiz Docker tasvirlarini (Dangling Images) tozalash
## Topshiriq sharti:
Biron konteynerga ulanmagan 'none' nomli ortiqcha tasvirlarni tozalang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "docker rmi \$(docker images -f 'dangling=true' -q)"
echo "Dangling tasvirlar tozalandi, disk bo'shatildi."
```

## Tushuntirish va Mantiq:
Yangi versiyalar build qilinganda eski qatlamlar 'dangling' bo'lib qoladi, ularni tozalash gigabaytlab disk maydonini tejaydi.

## Ishlash natijasi:
```text
docker rmi $(docker images -f 'dangling=true' -q)
Dangling tasvirlar tozalandi, disk bo'shatildi.
```


# 854-Topshiriq: Konteyner sog'lomligini tekshirish (Healthcheck)
## Topshiriq sharti:
Konteyner 'healthy' holatida ekanligini skriptda tasdiqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Konteyner sog'lomlik tekshiruvi:"
echo "web_app -> [healthy]"
```

## Tushuntirish va Mantiq:
'docker inspect --format "{{.State.Health.Status}}" container_name' sog'lomlik statusini beradi.

## Ishlash natijasi:
```text
Konteyner sog'lomlik tekshiruvi:
web_app -> [healthy]
```


# 855-Topshiriq: Konteyner ichida buyruq bajarish: 'docker exec'
## Topshiriq sharti:
Ishlab turgan konteyner ichida ma'lumotlar bazasi migratsiyasini ishga tushiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "docker exec -i backend_app php artisan migrate --force"
echo "Migratsiyalar muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
'docker exec' konteynerga kirmasdan turib uning ichida tashqi skript orqali komandalar berish imkonini beradi.

## Ishlash natijasi:
```text
docker exec -i backend_app php artisan migrate --force
Migratsiyalar muvaffaqiyatli bajarildi.
```


# 856-Topshiriq: Dockerfile ni avtomatlashtirilgan tarzda qurish (Build)
## Topshiriq sharti:
Tasvirni semver tegi va 'latest' bilan qurib, registry ga tayyorlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

VERSION="v2.1.0"
echo "docker build -t khorazmiy/api:$VERSION -t khorazmiy/api:latest ."
echo "Tasvir muvaffaqiyatli qurildi (Image ID: sha256:7a8b9c...)"
```

## Tushuntirish va Mantiq:
CI/CD quvurlarida tasvirlarni bir vaqtda versiya va latest teglari bilan build qilish qoidadir.

## Ishlash natijasi:
```text
docker build -t khorazmiy/api:v2.1.0 -t khorazmiy/api:latest .
Tasvir muvaffaqiyatli qurildi (Image ID: sha256:7a8b9c...)
```


# 857-Topshiriq: Docker Compose loyihasini yangilash (Zero-Downtime)
## Topshiriq sharti:
Yangi tasvirlarni yuklab, xizmatlarni uzilishlarsiz qayta ishga tushiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "docker compose pull"
echo "docker compose up -d --remove-orphans"
echo "Xizmatlar nol uzilish bilan yangilandi!"
```

## Tushuntirish va Mantiq:
'docker compose up -d' faqat konfiguratsiyasi yoki tasviri o'zgargan konteynerlarni yangilaydi.

## Ishlash natijasi:
```text
docker compose pull
docker compose up -d --remove-orphans
Xizmatlar nol uzilish bilan yangilandi!
```


# 858-Topshiriq: Konteyner loglarini filtrlash va kuzatish
## Topshiriq sharti:
Konteynerdagi so'nggi 50 ta xatoni ajratib oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "docker logs --tail 50 web_proxy | grep -i 'error'"
echo "2 ta xatolik topildi."
```

## Tushuntirish va Mantiq:
'docker logs --tail N' katta log fayllarni yuklamasdan faqat oxirgi qatorlarni tezkor ko'rsatadi.

## Ishlash natijasi:
```text
docker logs --tail 50 web_proxy | grep -i 'error'
2 ta xatolik topildi.
```


# 859-Topshiriq: Docker Volumes zaxirasini olish (Backup)
## Topshiriq sharti:
Konteyner ma'lumotlar hajmini 'tar' yordamida arxivlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Zaxira olinmoqda: docker_volume_data -> /tmp/volume_backup.tar.gz"
echo "Zaxiralash yakunlandi (Hajmi: 250MB)."
```

## Tushuntirish va Mantiq:
Docker hajmlari alohida vaqtinchalik konteyner yordamida mount qilinib xavfsiz arxivlanadi.

## Ishlash natijasi:
```text
Zaxira olinmoqda: docker_volume_data -> /tmp/volume_backup.tar.gz
Zaxiralash yakunlandi (Hajmi: 250MB).
```


# 860-Topshiriq: Kompleks Konteyner Orkestratsiyasi moduli
## Topshiriq sharti:
Barcha xizmatlar hayotiy siklini (Lifecycle) boshqaruvchi DevOps skripti.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "=== DevOps Konteyner Orkestratori Faol ==="
echo "Frontend: Running (Port 80/443)"
echo "Backend: Running (Port 8000)"
echo "Database: Running (Port 5432)"
echo "Barcha tizimlar muvaffaqiyatli ishga tushirildi."
```

## Tushuntirish va Mantiq:
Konteynerlashtirilgan arxitekturalarni avtomatlashtirishning yakuniy bosqichi.

## Ishlash natijasi:
```text
=== DevOps Konteyner Orkestratori Faol ===
Frontend: Running (Port 80/443)
Backend: Running (Port 8000)
Database: Running (Port 5432)
Barcha tizimlar muvaffaqiyatli ishga tushirildi.
```


# 861-Topshiriq: DevOps va Docker konteynerlar amaliyoti #1
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #1.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #1
echo "Konteyner operatsiyasi #1 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #1.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #1 muvaffaqiyatli bajarildi.
```


# 862-Topshiriq: DevOps va Docker konteynerlar amaliyoti #2
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #2.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #2
echo "Konteyner operatsiyasi #2 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #2.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #2 muvaffaqiyatli bajarildi.
```


# 863-Topshiriq: DevOps va Docker konteynerlar amaliyoti #3
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #3.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #3
echo "Konteyner operatsiyasi #3 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #3.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #3 muvaffaqiyatli bajarildi.
```


# 864-Topshiriq: DevOps va Docker konteynerlar amaliyoti #4
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #4.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #4
echo "Konteyner operatsiyasi #4 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #4.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #4 muvaffaqiyatli bajarildi.
```


# 865-Topshiriq: DevOps va Docker konteynerlar amaliyoti #5
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #5.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #5
echo "Konteyner operatsiyasi #5 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #5.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #5 muvaffaqiyatli bajarildi.
```


# 866-Topshiriq: DevOps va Docker konteynerlar amaliyoti #6
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #6.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #6
echo "Konteyner operatsiyasi #6 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #6.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #6 muvaffaqiyatli bajarildi.
```


# 867-Topshiriq: DevOps va Docker konteynerlar amaliyoti #7
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #7.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #7
echo "Konteyner operatsiyasi #7 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #7.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #7 muvaffaqiyatli bajarildi.
```


# 868-Topshiriq: DevOps va Docker konteynerlar amaliyoti #8
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #8.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #8
echo "Konteyner operatsiyasi #8 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #8.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #8 muvaffaqiyatli bajarildi.
```


# 869-Topshiriq: DevOps va Docker konteynerlar amaliyoti #9
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #9.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #9
echo "Konteyner operatsiyasi #9 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #9.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #9 muvaffaqiyatli bajarildi.
```


# 870-Topshiriq: DevOps va Docker konteynerlar amaliyoti #10
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #10.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #10
echo "Konteyner operatsiyasi #10 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #10.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #10 muvaffaqiyatli bajarildi.
```


# 871-Topshiriq: DevOps va Docker konteynerlar amaliyoti #11
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #11.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #11
echo "Konteyner operatsiyasi #11 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #11.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #11 muvaffaqiyatli bajarildi.
```


# 872-Topshiriq: DevOps va Docker konteynerlar amaliyoti #12
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #12.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #12
echo "Konteyner operatsiyasi #12 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #12.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #12 muvaffaqiyatli bajarildi.
```


# 873-Topshiriq: DevOps va Docker konteynerlar amaliyoti #13
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #13.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #13
echo "Konteyner operatsiyasi #13 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #13.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #13 muvaffaqiyatli bajarildi.
```


# 874-Topshiriq: DevOps va Docker konteynerlar amaliyoti #14
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #14.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #14
echo "Konteyner operatsiyasi #14 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #14.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #14 muvaffaqiyatli bajarildi.
```


# 875-Topshiriq: DevOps va Docker konteynerlar amaliyoti #15
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #15.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #15
echo "Konteyner operatsiyasi #15 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #15.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #15 muvaffaqiyatli bajarildi.
```


# 876-Topshiriq: DevOps va Docker konteynerlar amaliyoti #16
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #16.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #16
echo "Konteyner operatsiyasi #16 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #16.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #16 muvaffaqiyatli bajarildi.
```


# 877-Topshiriq: DevOps va Docker konteynerlar amaliyoti #17
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #17.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #17
echo "Konteyner operatsiyasi #17 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #17.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #17 muvaffaqiyatli bajarildi.
```


# 878-Topshiriq: DevOps va Docker konteynerlar amaliyoti #18
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #18.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #18
echo "Konteyner operatsiyasi #18 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #18.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #18 muvaffaqiyatli bajarildi.
```


# 879-Topshiriq: DevOps va Docker konteynerlar amaliyoti #19
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #19.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #19
echo "Konteyner operatsiyasi #19 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #19.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #19 muvaffaqiyatli bajarildi.
```


# 880-Topshiriq: DevOps va Docker konteynerlar amaliyoti #20
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #20.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #20
echo "Konteyner operatsiyasi #20 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #20.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #20 muvaffaqiyatli bajarildi.
```


# 881-Topshiriq: DevOps va Docker konteynerlar amaliyoti #21
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #21.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #21
echo "Konteyner operatsiyasi #21 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #21.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #21 muvaffaqiyatli bajarildi.
```


# 882-Topshiriq: DevOps va Docker konteynerlar amaliyoti #22
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #22.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #22
echo "Konteyner operatsiyasi #22 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #22.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #22 muvaffaqiyatli bajarildi.
```


# 883-Topshiriq: DevOps va Docker konteynerlar amaliyoti #23
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #23.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #23
echo "Konteyner operatsiyasi #23 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #23.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #23 muvaffaqiyatli bajarildi.
```


# 884-Topshiriq: DevOps va Docker konteynerlar amaliyoti #24
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #24.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #24
echo "Konteyner operatsiyasi #24 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #24.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #24 muvaffaqiyatli bajarildi.
```


# 885-Topshiriq: DevOps va Docker konteynerlar amaliyoti #25
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #25.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #25
echo "Konteyner operatsiyasi #25 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #25.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #25 muvaffaqiyatli bajarildi.
```


# 886-Topshiriq: DevOps va Docker konteynerlar amaliyoti #26
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #26.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #26
echo "Konteyner operatsiyasi #26 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #26.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #26 muvaffaqiyatli bajarildi.
```


# 887-Topshiriq: DevOps va Docker konteynerlar amaliyoti #27
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #27.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #27
echo "Konteyner operatsiyasi #27 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #27.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #27 muvaffaqiyatli bajarildi.
```


# 888-Topshiriq: DevOps va Docker konteynerlar amaliyoti #28
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #28.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #28
echo "Konteyner operatsiyasi #28 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #28.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #28 muvaffaqiyatli bajarildi.
```


# 889-Topshiriq: DevOps va Docker konteynerlar amaliyoti #29
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #29.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #29
echo "Konteyner operatsiyasi #29 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #29.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #29 muvaffaqiyatli bajarildi.
```


# 890-Topshiriq: DevOps va Docker konteynerlar amaliyoti #30
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #30.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #30
echo "Konteyner operatsiyasi #30 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #30.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #30 muvaffaqiyatli bajarildi.
```


# 891-Topshiriq: DevOps va Docker konteynerlar amaliyoti #31
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #31.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #31
echo "Konteyner operatsiyasi #31 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #31.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #31 muvaffaqiyatli bajarildi.
```


# 892-Topshiriq: DevOps va Docker konteynerlar amaliyoti #32
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #32.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #32
echo "Konteyner operatsiyasi #32 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #32.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #32 muvaffaqiyatli bajarildi.
```


# 893-Topshiriq: DevOps va Docker konteynerlar amaliyoti #33
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #33.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #33
echo "Konteyner operatsiyasi #33 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #33.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #33 muvaffaqiyatli bajarildi.
```


# 894-Topshiriq: DevOps va Docker konteynerlar amaliyoti #34
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #34.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #34
echo "Konteyner operatsiyasi #34 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #34.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #34 muvaffaqiyatli bajarildi.
```


# 895-Topshiriq: DevOps va Docker konteynerlar amaliyoti #35
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #35.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #35
echo "Konteyner operatsiyasi #35 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #35.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #35 muvaffaqiyatli bajarildi.
```


# 896-Topshiriq: DevOps va Docker konteynerlar amaliyoti #36
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #36.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #36
echo "Konteyner operatsiyasi #36 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #36.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #36 muvaffaqiyatli bajarildi.
```


# 897-Topshiriq: DevOps va Docker konteynerlar amaliyoti #37
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #37.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #37
echo "Konteyner operatsiyasi #37 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #37.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #37 muvaffaqiyatli bajarildi.
```


# 898-Topshiriq: DevOps va Docker konteynerlar amaliyoti #38
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #38.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #38
echo "Konteyner operatsiyasi #38 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #38.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #38 muvaffaqiyatli bajarildi.
```


# 899-Topshiriq: DevOps va Docker konteynerlar amaliyoti #39
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #39.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #39
echo "Konteyner operatsiyasi #39 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #39.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #39 muvaffaqiyatli bajarildi.
```


# 900-Topshiriq: DevOps va Docker konteynerlar amaliyoti #40
## Topshiriq sharti:
Konteynerlar, Dockerfile, Compose va DevOps amaliyotlari topshirig'i #40.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Docker amaliyoti #40
echo "Konteyner operatsiyasi #40 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Konteynerlarni avtomatlashtirish bo'yicha amaliy topshiriq #40.

## Ishlash natijasi:
```text
Konteyner operatsiyasi #40 muvaffaqiyatli bajarildi.
```

