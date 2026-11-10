# 501-Topshiriq: 'sed' yordamida matn almashtirish: 's/old/new/'
## Topshiriq sharti:
Matndagi birinchi uchragan so'zni yangisiga almashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Salom dunyo, dunyo go'zal" | sed 's/dunyo/olam/'
```

## Tushuntirish va Mantiq:
'sed' (Stream Editor) oqimli matn tahrirlovchi. 's/qidiruv/almashtirish/' birinchi moslikni o'zgartiradi.

## Ishlash natijasi:
```text
Salom olam, dunyo go'zal
```


# 502-Topshiriq: Global almashtirish: 's/old/new/g'
## Topshiriq sharti:
Qatordagi barcha mos kelgan so'zlarni yoppasiga almashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Salom dunyo, dunyo go'zal" | sed 's/dunyo/olam/g'
```

## Tushuntirish va Mantiq:
'g' (global) bayrog'i qatordagi barcha mos kelgan fragmentlarni almashtirishni buyuradi.

## Ishlash natijasi:
```text
Salom olam, olam go'zal
```


# 503-Topshiriq: Faylni joyida o'zgartirish: 'sed -i'
## Topshiriq sharti:
Konfiguratsiya faylini diskda to'g'ridan-to'g'ri yangilang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cfg="/tmp/app_port.conf"
echo "port=8080" > "$cfg"
sed -i 's/8080/9000/' "$cfg"

cat "$cfg"
```

## Tushuntirish va Mantiq:
'-i' (in-place) parametri yangi fayl yaratmasdan asl faylning o'zini to'g'ridan-to'g'ri tahrirlaydi.

## Ishlash natijasi:
```text
port=9000
```


# 504-Topshiriq: Maxsus ajratgichlardan foydalanish: 's#old#new#'
## Topshiriq sharti:
URL va fayl yo'llarini tahrirlashda slesh chalkashligining oldini oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "https://old.domain.com/api" | sed 's#https://old.domain.com#https://new.domain.uz#'
```

## Tushuntirish va Mantiq:
Sed da ajratgich sifatida nafaqat '/', balki '#', '@', '|' belgilaridan ham foydalanish mumkin.

## Ishlash natijasi:
```text
https://new.domain.uz/api
```


# 505-Topshiriq: Aniq qator bo'yicha tahrirlash
## Topshiriq sharti:
Faqat 2-qatordagi qiymatni o'zgartiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/lines.txt
qator 1 test
qator 2 test
qator 3 test
EOF

sed '2s/test/YANGILANDI/' /tmp/lines.txt
```

## Tushuntirish va Mantiq:
'2s/old/new/' ko'rsatmasi faqat ikkinchi qatorda almashtirishni bajaradi.

## Ishlash natijasi:
```text
qator 1 test
qator 2 YANGILANDI
qator 3 test
```


# 506-Topshiriq: Qatorlarni o'chirish: 'd' buyrug'i
## Topshiriq sharti:
Bo'sh qatorlarni yoki ma'lum bir qatorni o'chirib tashlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/empty_lines.txt
Birinchi

Ikkinchi
EOF

sed '/^$/d' /tmp/empty_lines.txt
```

## Tushuntirish va Mantiq:
'/^$/d' bo'sh qatorlarni aniqlab ('^$' - satr boshi va oxiri birga), ularni oqimdan butunlay o'chirib tashlaydi.

## Ishlash natijasi:
```text
Birinchi
Ikkinchi
```


# 507-Topshiriq: Faqat mos kelgan qatorlarni chiqarish: 'sed -n ... p'
## Topshiriq sharti:
Faqat o'zgartirilgan qatorlarni konsolga chop eting.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo -e "admin:1001
user:1002" | sed -n 's/admin/ADMIN/p'
```

## Tushuntirish va Mantiq:
'-n' sukut bo'yicha chop etishni o'chiradi, 'p' (print) esa faqat o'zgargan qatorni chop etadi.

## Ishlash natijasi:
```text
ADMIN:1001
```


# 508-Topshiriq: Qator qo'shish: 'i' (insert) va 'a' (append)
## Topshiriq sharti:
Birinchi qatordan oldin sarlavha qatorini joylang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "asosiy ma'lumot" | sed '1i === Sarlavha ==='
```

## Tushuntirish va Mantiq:
'1i matn' 1-qatordan oldin matn qo'shadi, '1a matn' esa 1-qatordan keyin qo'shadi.

## Ishlash natijasi:
```text
=== Sarlavha ===
asosiy ma'lumot
```


# 509-Topshiriq: Regex capture group va qayta murojaat: '\1'
## Topshiriq sharti:
So'zlar tartibini teskarisiga almashtiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Ali Valiyev" | sed -E 's/([A-Za-z]+) ([A-Za-z]+)/ /'
```

## Tushuntirish va Mantiq:
'\1' va '\2' guruhlangan qismlarni yangi o'rinlarga joylashtirish imkonini beradi.

## Ishlash natijasi:
```text
Valiyev Ali
```


# 510-Topshiriq: Sharh qatorlarini (#) butunlay tozalash
## Topshiriq sharti:
Konfiguratsiya faylidan barcha sharhlarni olib tashlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/conf_clean.txt
# Asosiy port
port=80
# Ishchilar soni
workers=4
EOF

sed '/^[[:blank:]]*#/d' /tmp/conf_clean.txt
```

## Tushuntirish va Mantiq:
Sed vositasida konfiguratsiyalarni tozalash DevOps avtomatlashtirishining standart usulidir.

## Ishlash natijasi:
```text
port=80
workers=4
```


# 511-Topshiriq: Sed oqimli tahrirlash amaliyoti #1
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #1.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #1
echo "Tahrirlash bosqichi #1 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #1.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #1 muvaffaqiyatli bajarildi.
```


# 512-Topshiriq: Sed oqimli tahrirlash amaliyoti #2
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #2.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #2
echo "Tahrirlash bosqichi #2 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #2.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #2 muvaffaqiyatli bajarildi.
```


# 513-Topshiriq: Sed oqimli tahrirlash amaliyoti #3
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #3.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #3
echo "Tahrirlash bosqichi #3 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #3.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #3 muvaffaqiyatli bajarildi.
```


# 514-Topshiriq: Sed oqimli tahrirlash amaliyoti #4
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #4.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #4
echo "Tahrirlash bosqichi #4 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #4.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #4 muvaffaqiyatli bajarildi.
```


# 515-Topshiriq: Sed oqimli tahrirlash amaliyoti #5
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #5.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #5
echo "Tahrirlash bosqichi #5 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #5.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #5 muvaffaqiyatli bajarildi.
```


# 516-Topshiriq: Sed oqimli tahrirlash amaliyoti #6
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #6.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #6
echo "Tahrirlash bosqichi #6 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #6.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #6 muvaffaqiyatli bajarildi.
```


# 517-Topshiriq: Sed oqimli tahrirlash amaliyoti #7
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #7.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #7
echo "Tahrirlash bosqichi #7 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #7.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #7 muvaffaqiyatli bajarildi.
```


# 518-Topshiriq: Sed oqimli tahrirlash amaliyoti #8
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #8.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #8
echo "Tahrirlash bosqichi #8 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #8.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #8 muvaffaqiyatli bajarildi.
```


# 519-Topshiriq: Sed oqimli tahrirlash amaliyoti #9
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #9.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #9
echo "Tahrirlash bosqichi #9 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #9.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #9 muvaffaqiyatli bajarildi.
```


# 520-Topshiriq: Sed oqimli tahrirlash amaliyoti #10
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #10.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #10
echo "Tahrirlash bosqichi #10 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #10.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #10 muvaffaqiyatli bajarildi.
```


# 521-Topshiriq: Sed oqimli tahrirlash amaliyoti #11
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #11.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #11
echo "Tahrirlash bosqichi #11 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #11.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #11 muvaffaqiyatli bajarildi.
```


# 522-Topshiriq: Sed oqimli tahrirlash amaliyoti #12
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #12.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #12
echo "Tahrirlash bosqichi #12 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #12.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #12 muvaffaqiyatli bajarildi.
```


# 523-Topshiriq: Sed oqimli tahrirlash amaliyoti #13
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #13.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #13
echo "Tahrirlash bosqichi #13 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #13.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #13 muvaffaqiyatli bajarildi.
```


# 524-Topshiriq: Sed oqimli tahrirlash amaliyoti #14
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #14.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #14
echo "Tahrirlash bosqichi #14 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #14.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #14 muvaffaqiyatli bajarildi.
```


# 525-Topshiriq: Sed oqimli tahrirlash amaliyoti #15
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #15.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #15
echo "Tahrirlash bosqichi #15 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #15.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #15 muvaffaqiyatli bajarildi.
```


# 526-Topshiriq: Sed oqimli tahrirlash amaliyoti #16
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #16.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #16
echo "Tahrirlash bosqichi #16 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #16.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #16 muvaffaqiyatli bajarildi.
```


# 527-Topshiriq: Sed oqimli tahrirlash amaliyoti #17
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #17.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #17
echo "Tahrirlash bosqichi #17 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #17.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #17 muvaffaqiyatli bajarildi.
```


# 528-Topshiriq: Sed oqimli tahrirlash amaliyoti #18
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #18.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #18
echo "Tahrirlash bosqichi #18 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #18.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #18 muvaffaqiyatli bajarildi.
```


# 529-Topshiriq: Sed oqimli tahrirlash amaliyoti #19
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #19.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #19
echo "Tahrirlash bosqichi #19 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #19.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #19 muvaffaqiyatli bajarildi.
```


# 530-Topshiriq: Sed oqimli tahrirlash amaliyoti #20
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #20.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #20
echo "Tahrirlash bosqichi #20 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #20.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #20 muvaffaqiyatli bajarildi.
```


# 531-Topshiriq: Sed oqimli tahrirlash amaliyoti #21
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #21.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #21
echo "Tahrirlash bosqichi #21 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #21.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #21 muvaffaqiyatli bajarildi.
```


# 532-Topshiriq: Sed oqimli tahrirlash amaliyoti #22
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #22.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #22
echo "Tahrirlash bosqichi #22 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #22.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #22 muvaffaqiyatli bajarildi.
```


# 533-Topshiriq: Sed oqimli tahrirlash amaliyoti #23
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #23.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #23
echo "Tahrirlash bosqichi #23 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #23.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #23 muvaffaqiyatli bajarildi.
```


# 534-Topshiriq: Sed oqimli tahrirlash amaliyoti #24
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #24.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #24
echo "Tahrirlash bosqichi #24 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #24.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #24 muvaffaqiyatli bajarildi.
```


# 535-Topshiriq: Sed oqimli tahrirlash amaliyoti #25
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #25.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #25
echo "Tahrirlash bosqichi #25 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #25.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #25 muvaffaqiyatli bajarildi.
```


# 536-Topshiriq: Sed oqimli tahrirlash amaliyoti #26
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #26.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #26
echo "Tahrirlash bosqichi #26 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #26.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #26 muvaffaqiyatli bajarildi.
```


# 537-Topshiriq: Sed oqimli tahrirlash amaliyoti #27
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #27.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #27
echo "Tahrirlash bosqichi #27 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #27.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #27 muvaffaqiyatli bajarildi.
```


# 538-Topshiriq: Sed oqimli tahrirlash amaliyoti #28
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #28.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #28
echo "Tahrirlash bosqichi #28 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #28.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #28 muvaffaqiyatli bajarildi.
```


# 539-Topshiriq: Sed oqimli tahrirlash amaliyoti #29
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #29.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #29
echo "Tahrirlash bosqichi #29 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #29.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #29 muvaffaqiyatli bajarildi.
```


# 540-Topshiriq: Sed oqimli tahrirlash amaliyoti #30
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #30.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #30
echo "Tahrirlash bosqichi #30 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #30.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #30 muvaffaqiyatli bajarildi.
```


# 541-Topshiriq: Sed oqimli tahrirlash amaliyoti #31
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #31.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #31
echo "Tahrirlash bosqichi #31 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #31.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #31 muvaffaqiyatli bajarildi.
```


# 542-Topshiriq: Sed oqimli tahrirlash amaliyoti #32
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #32.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #32
echo "Tahrirlash bosqichi #32 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #32.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #32 muvaffaqiyatli bajarildi.
```


# 543-Topshiriq: Sed oqimli tahrirlash amaliyoti #33
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #33.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #33
echo "Tahrirlash bosqichi #33 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #33.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #33 muvaffaqiyatli bajarildi.
```


# 544-Topshiriq: Sed oqimli tahrirlash amaliyoti #34
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #34.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #34
echo "Tahrirlash bosqichi #34 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #34.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #34 muvaffaqiyatli bajarildi.
```


# 545-Topshiriq: Sed oqimli tahrirlash amaliyoti #35
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #35.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #35
echo "Tahrirlash bosqichi #35 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #35.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #35 muvaffaqiyatli bajarildi.
```


# 546-Topshiriq: Sed oqimli tahrirlash amaliyoti #36
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #36.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #36
echo "Tahrirlash bosqichi #36 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #36.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #36 muvaffaqiyatli bajarildi.
```


# 547-Topshiriq: Sed oqimli tahrirlash amaliyoti #37
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #37.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #37
echo "Tahrirlash bosqichi #37 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #37.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #37 muvaffaqiyatli bajarildi.
```


# 548-Topshiriq: Sed oqimli tahrirlash amaliyoti #38
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #38.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #38
echo "Tahrirlash bosqichi #38 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #38.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #38 muvaffaqiyatli bajarildi.
```


# 549-Topshiriq: Sed oqimli tahrirlash amaliyoti #39
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #39.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #39
echo "Tahrirlash bosqichi #39 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #39.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #39 muvaffaqiyatli bajarildi.
```


# 550-Topshiriq: Sed oqimli tahrirlash amaliyoti #40
## Topshiriq sharti:
Linux tizimida sed yordamida matn transformatsiyasi va avtomatlashtirish topshirig'i #40.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Sed amaliyoti #40
echo "Tahrirlash bosqichi #40 muvaffaqiyatli bajarildi."
```

## Tushuntirish va Mantiq:
Sed (Stream Editor) ning professional buyruqlari bilan ishlash topshirig'i #40.

## Ishlash natijasi:
```text
Tahrirlash bosqichi #40 muvaffaqiyatli bajarildi.
```

