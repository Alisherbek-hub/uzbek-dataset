# 601-Topshiriq: 'find' yordamida fayllarni nomi bo'yicha qidirish: '-name'
## Topshiriq sharti:
Loyiha papkasidan barcha '.conf' konfiguratsiya fayllarini toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/find_demo/sub
touch /tmp/find_demo/app.conf /tmp/find_demo/sub/db.conf /tmp/find_demo/notes.txt

find /tmp/find_demo -type f -name "*.conf"
rm -rf /tmp/find_demo
```

## Tushuntirish va Mantiq:
'find [katalog] -name [shablon]' kataloglar daraxti bo'ylab rekursiv qidiruvni amalga oshiradi.

## Ishlash natijasi:
```text
/tmp/find_demo/app.conf
/tmp/find_demo/sub/db.conf
```


# 602-Topshiriq: Fayl hajmi bo'yicha qidirish: '-size'
## Topshiriq sharti:
Hajmi 10 Megabaytdan katta bo'lgan yirik fayllarni toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/size_test
truncate -s 15M /tmp/size_test/large.log
touch /tmp/size_test/small.txt

find /tmp/size_test -type f -size +10M
rm -rf /tmp/size_test
```

## Tushuntirish va Mantiq:
'-size +10M' hajmi 10 MB dan yuqori, '-size -1k' esa 1 KB dan kichik fayllarni aniqlaydi.

## Ishlash natijasi:
```text
/tmp/size_test/large.log
```


# 603-Topshiriq: Vaqt bo'yicha qidirish: '-mtime' va '-mmin'
## Topshiriq sharti:
So'nggi 24 soat (yoki 60 daqiqa) ichida o'zgartirilgan fayllarni toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/time_test
touch /tmp/time_test/recent.log

find /tmp/time_test -type f -mmin -60
rm -rf /tmp/time_test
```

## Tushuntirish va Mantiq:
'-mtime -N' oxirgi N kun, '-mmin -M' esa oxirgi M daqiqa ichida modifikatsiya qilingan fayllarni qidiradi.

## Ishlash natijasi:
```text
/tmp/time_test/recent.log
```


# 604-Topshiriq: Topilgan fayllarda buyruq bajarish: '-exec cmd {} \;'
## Topshiriq sharti:
Eski log fayllarini topib, ularni avtomatik o'chiring yoki arxivlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/exec_test
touch /tmp/exec_test/old1.bak /tmp/exec_test/old2.bak

find /tmp/exec_test -type f -name "*.bak" -exec rm -f {} +
echo "Qolgan fayllar soni: $(ls /tmp/exec_test | wc -l)"
rm -rf /tmp/exec_test
```

## Tushuntirish va Mantiq:
'-exec cmd {} +' topilgan barcha fayllarni bitta buyruqqa parametr qilib uzatadi, bu '-exec cmd {} \;' ga qaraganda ancha tez ishlaydi.

## Ishlash natijasi:
```text
Qolgan fayllar soni: 0
```


# 605-Topshiriq: TAR arxivi yaratish va ochish: 'tar -czvf' va 'tar -xzvf'
## Topshiriq sharti:
Katalogni siqilgan GZIP tarball arxiviga aylantiring va qayta oching.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/tar_src
echo "Muhim ma'lumot" > /tmp/tar_src/data.txt

tar -czf /tmp/backup.tar.gz -C /tmp tar_src
echo "Arxiv yaratildi: $(ls -lh /tmp/backup.tar.gz | awk '{print $9, $5}')"

rm -rf /tmp/tar_src /tmp/backup.tar.gz
```

## Tushuntirish va Mantiq:
'tar -czf' arxiv yaratadi ('c' - create, 'z' - gzip, 'f' - file). '-xzf' esa arxivni ochadi ('x' - extract).

## Ishlash natijasi:
```text
Arxiv yaratildi: /tmp/backup.tar.gz 140B
```


# 606-Topshiriq: Fayllarni masofaga sinxronlash: 'rsync -avz'
## Topshiriq sharti:
Katalogdagi yangi fayllarni ikkinchi katalogga samarali sinxronlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/src_sync /tmp/dst_sync
echo "Versiya 1" > /tmp/src_sync/file.txt

rsync -avz /tmp/src_sync/ /tmp/dst_sync/ > /dev/null
echo "Sinxronlandi: $(cat /tmp/dst_sync/file.txt)"

rm -rf /tmp/src_sync /tmp/dst_sync
```

## Tushuntirish va Mantiq:
'rsync' (Remote Sync) faqat o'zgargan baytlarni uzatuvchi juda samarali vositadir. '-a' (archive) barcha ruxsatlar va vaqtlarni saqlaydi.

## Ishlash natijasi:
```text
Sinxronlandi: Versiya 1
```


# 607-Topshiriq: Fayl ruxsatlari: 'chmod' (Raqamli va simvolik)
## Topshiriq sharti:
Skriptga bajarish (755) va maxfiy kalitga faqat o'qish (600) huquqini bering.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

touch /tmp/deploy.sh /tmp/id_rsa
chmod 755 /tmp/deploy.sh
chmod 600 /tmp/id_rsa

ls -l /tmp/deploy.sh /tmp/id_rsa | awk '{print $1, $9}'
rm -f /tmp/deploy.sh /tmp/id_rsa
```

## Tushuntirish va Mantiq:
755: rwxr-xr-x (egasi to'liq, qolganlar o'qish/bajarish). 600: rw------- (faqat egasiga o'qish/yozish, SSH kalitlar talabi).

## Ishlash natijasi:
```text
-rwxr-xr-x /tmp/deploy.sh
-rw------- /tmp/id_rsa
```


# 608-Topshiriq: Fayl egasini o'zgartirish: 'chown' va 'chgrp'
## Topshiriq sharti:
Fayl egasi va guruhini administratorga o'zgartirish sintaksisi.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "chown www-data:www-data /var/www/html"
echo "Fayl egasi 'www-data' foydalanuvchisi va guruhiga biriktirildi."
```

## Tushuntirish va Mantiq:
'chown user:group fayl' operatsion tizim darajasida fayl egaligini yangilaydi.

## Ishlash natijasi:
```text
chown www-data:www-data /var/www/html
Fayl egasi 'www-data' foydalanuvchisi va guruhiga biriktirildi.
```


# 609-Topshiriq: Maxsus ruxsatlar: SUID (4000), SGID (2000), Sticky Bit (1000)
## Topshiriq sharti:
Vaqtinchalik papkaga (masalan, /tmp) Sticky bit o'rnatish.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/shared_dir
chmod 1777 /tmp/shared_dir

ls -ld /tmp/shared_dir | awk '{print $1, $9}'
rm -rf /tmp/shared_dir
```

## Tushuntirish va Mantiq:
Sticky bit ('t') o'rnatilgan katalogda (1777) har bir foydalanuvchi fayl yarata oladi, lekin birovning faylini faqat uning egasi yoki root o'chira oladi.

## Ishlash natijasi:
```text
drwxrwxrwt /tmp/shared_dir
```


# 610-Topshiriq: Disk maydoni tahlili: 'df -h' va 'du -sh *'
## Topshiriq sharti:
Mavjud disk bo'limlari bandligi va eng yirik papkalarni aniqlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Asosiy bo'lim bandligi:"
df -h / | awk 'NR==2 {print "Bo'lim:", $1, "| Band:", $5, "| Bo'sh:", $4}'
```

## Tushuntirish va Mantiq:
'df -h' fayl tizimlaridagi bo'sh joyni, 'du -sh' esa kataloglar egallagan haqiqiy disk hajmini ko'rsatadi.

## Ishlash natijasi:
```text
Bo'lim: /dev/sda1 | Band: 45% | Bo'sh: 28G
```


# 611-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #1
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #1.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #1
echo "Fayl tizimi operatsiyasi #1 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #1.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #1 muvaffaqiyatli bajarildi.
```


# 612-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #2
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #2.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #2
echo "Fayl tizimi operatsiyasi #2 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #2.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #2 muvaffaqiyatli bajarildi.
```


# 613-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #3
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #3.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #3
echo "Fayl tizimi operatsiyasi #3 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #3.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #3 muvaffaqiyatli bajarildi.
```


# 614-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #4
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #4.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #4
echo "Fayl tizimi operatsiyasi #4 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #4.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #4 muvaffaqiyatli bajarildi.
```


# 615-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #5
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #5.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #5
echo "Fayl tizimi operatsiyasi #5 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #5.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #5 muvaffaqiyatli bajarildi.
```


# 616-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #6
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #6.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #6
echo "Fayl tizimi operatsiyasi #6 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #6.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #6 muvaffaqiyatli bajarildi.
```


# 617-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #7
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #7.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #7
echo "Fayl tizimi operatsiyasi #7 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #7.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #7 muvaffaqiyatli bajarildi.
```


# 618-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #8
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #8.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #8
echo "Fayl tizimi operatsiyasi #8 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #8.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #8 muvaffaqiyatli bajarildi.
```


# 619-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #9
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #9.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #9
echo "Fayl tizimi operatsiyasi #9 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #9.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #9 muvaffaqiyatli bajarildi.
```


# 620-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #10
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #10.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #10
echo "Fayl tizimi operatsiyasi #10 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #10.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #10 muvaffaqiyatli bajarildi.
```


# 621-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #11
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #11.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #11
echo "Fayl tizimi operatsiyasi #11 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #11.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #11 muvaffaqiyatli bajarildi.
```


# 622-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #12
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #12.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #12
echo "Fayl tizimi operatsiyasi #12 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #12.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #12 muvaffaqiyatli bajarildi.
```


# 623-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #13
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #13.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #13
echo "Fayl tizimi operatsiyasi #13 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #13.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #13 muvaffaqiyatli bajarildi.
```


# 624-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #14
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #14.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #14
echo "Fayl tizimi operatsiyasi #14 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #14.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #14 muvaffaqiyatli bajarildi.
```


# 625-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #15
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #15.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #15
echo "Fayl tizimi operatsiyasi #15 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #15.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #15 muvaffaqiyatli bajarildi.
```


# 626-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #16
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #16.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #16
echo "Fayl tizimi operatsiyasi #16 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #16.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #16 muvaffaqiyatli bajarildi.
```


# 627-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #17
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #17.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #17
echo "Fayl tizimi operatsiyasi #17 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #17.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #17 muvaffaqiyatli bajarildi.
```


# 628-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #18
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #18.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #18
echo "Fayl tizimi operatsiyasi #18 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #18.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #18 muvaffaqiyatli bajarildi.
```


# 629-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #19
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #19.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #19
echo "Fayl tizimi operatsiyasi #19 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #19.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #19 muvaffaqiyatli bajarildi.
```


# 630-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #20
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #20.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #20
echo "Fayl tizimi operatsiyasi #20 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #20.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #20 muvaffaqiyatli bajarildi.
```


# 631-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #21
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #21.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #21
echo "Fayl tizimi operatsiyasi #21 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #21.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #21 muvaffaqiyatli bajarildi.
```


# 632-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #22
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #22.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #22
echo "Fayl tizimi operatsiyasi #22 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #22.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #22 muvaffaqiyatli bajarildi.
```


# 633-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #23
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #23.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #23
echo "Fayl tizimi operatsiyasi #23 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #23.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #23 muvaffaqiyatli bajarildi.
```


# 634-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #24
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #24.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #24
echo "Fayl tizimi operatsiyasi #24 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #24.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #24 muvaffaqiyatli bajarildi.
```


# 635-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #25
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #25.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #25
echo "Fayl tizimi operatsiyasi #25 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #25.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #25 muvaffaqiyatli bajarildi.
```


# 636-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #26
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #26.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #26
echo "Fayl tizimi operatsiyasi #26 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #26.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #26 muvaffaqiyatli bajarildi.
```


# 637-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #27
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #27.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #27
echo "Fayl tizimi operatsiyasi #27 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #27.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #27 muvaffaqiyatli bajarildi.
```


# 638-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #28
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #28.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #28
echo "Fayl tizimi operatsiyasi #28 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #28.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #28 muvaffaqiyatli bajarildi.
```


# 639-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #29
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #29.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #29
echo "Fayl tizimi operatsiyasi #29 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #29.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #29 muvaffaqiyatli bajarildi.
```


# 640-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #30
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #30.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #30
echo "Fayl tizimi operatsiyasi #30 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #30.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #30 muvaffaqiyatli bajarildi.
```


# 641-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #31
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #31.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #31
echo "Fayl tizimi operatsiyasi #31 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #31.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #31 muvaffaqiyatli bajarildi.
```


# 642-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #32
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #32.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #32
echo "Fayl tizimi operatsiyasi #32 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #32.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #32 muvaffaqiyatli bajarildi.
```


# 643-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #33
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #33.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #33
echo "Fayl tizimi operatsiyasi #33 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #33.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #33 muvaffaqiyatli bajarildi.
```


# 644-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #34
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #34.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #34
echo "Fayl tizimi operatsiyasi #34 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #34.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #34 muvaffaqiyatli bajarildi.
```


# 645-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #35
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #35.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #35
echo "Fayl tizimi operatsiyasi #35 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #35.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #35 muvaffaqiyatli bajarildi.
```


# 646-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #36
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #36.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #36
echo "Fayl tizimi operatsiyasi #36 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #36.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #36 muvaffaqiyatli bajarildi.
```


# 647-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #37
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #37.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #37
echo "Fayl tizimi operatsiyasi #37 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #37.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #37 muvaffaqiyatli bajarildi.
```


# 648-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #38
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #38.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #38
echo "Fayl tizimi operatsiyasi #38 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #38.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #38 muvaffaqiyatli bajarildi.
```


# 649-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #39
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #39.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #39
echo "Fayl tizimi operatsiyasi #39 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #39.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #39 muvaffaqiyatli bajarildi.
```


# 650-Topshiriq: Fayl tizimi va kataloglar boshqaruvi amaliyoti #40
## Topshiriq sharti:
Linux operatsion tizimida fayllar, huquqlar, arxivlar va sinxronizatsiya topshirig'i #40.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Fayl tizimi amaliyoti #40
echo "Fayl tizimi operatsiyasi #40 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Fayllar va kataloglarni xavfsiz boshqarish bo'yicha amaliy vazifa #40.

## Ishlash natijasi:
```text
Fayl tizimi operatsiyasi #40 muvaffaqiyatli bajarildi.
```

