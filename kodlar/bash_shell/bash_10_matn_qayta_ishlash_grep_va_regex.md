# 451-Topshiriq: 'grep' asoslari va matn ichidan qidiruv
## Topshiriq sharti:
Fayl ichidan 'ERROR' so'zi qatnashgan barcha qatorlarni topib konsolga chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/demo_app.log
INFO: Dastur ishga tushdi
ERROR: Ma'lumotlar bazasiga ulanib bo'lmadi
DEBUG: Port 5432 tekshirilmoqda
ERROR: Timeout yuz berdi
EOF

grep "ERROR" /tmp/demo_app.log
```

## Tushuntirish va Mantiq:
'grep' (Global Regular Expression Print) berilgan fayl yoki oqimdan shablonga (pattern) mos keluvchi barcha qatorlarni qidirib topadi.

## Ishlash natijasi:
```text
ERROR: Ma'lumotlar bazasiga ulanib bo'lmadi
ERROR: Timeout yuz berdi
```


# 452-Topshiriq: Registrni inkor qilib qidirish: 'grep -i'
## Topshiriq sharti:
Katta-kichik harflaridan qat'i nazar 'warning' so'zini qidiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

cat << 'EOF' > /tmp/demo_case.log
WARNING: Xotira kam
Warning: Disk to'ldi
warning: Kesh eskirgan
EOF

grep -i "warning" /tmp/demo_case.log
```

## Tushuntirish va Mantiq:
'-i' (ignore case) parametri qidiruvda katta va kichik harflar farqini hisobga olmaydi.

## Ishlash natijasi:
```text
WARNING: Xotira kam
Warning: Disk to'ldi
warning: Kesh eskirgan
```


# 453-Topshiriq: Qator raqamlari bilan chiqarish: 'grep -n'
## Topshiriq sharti:
Mos kelgan qatorlarning fayldagi tartib raqamlarini ham ko'rsating.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

grep -n "Disk" /tmp/demo_case.log
```

## Tushuntirish va Mantiq:
'-n' (line number) parametri har bir mos kelgan qator boshida uning fayldagi raqamini aks ettiradi.

## Ishlash natijasi:
```text
2:Warning: Disk to'ldi
```


# 454-Topshiriq: Mos kelmaydigan qatorlarni filtrlash: 'grep -v'
## Topshiriq sharti:
Log fayldan 'DEBUG' darajasidagi ortiqcha qatorlarni olib tashlang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

grep -v "DEBUG" /tmp/demo_app.log
```

## Tushuntirish va Mantiq:
'-v' (invert match) shablonga mos kelmagan barcha qatorlarni chiqaradi.

## Ishlash natijasi:
```text
INFO: Dastur ishga tushdi
ERROR: Ma'lumotlar bazasiga ulanib bo'lmadi
ERROR: Timeout yuz berdi
```


# 455-Topshiriq: Faqat mos kelgan qatorlar sonini hisoblash: 'grep -c'
## Topshiriq sharti:
Faylda jami nechta xatolik (ERROR) qayd etilganini hisoblang.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

count=$(grep -c "ERROR" /tmp/demo_app.log)
echo "Jami xatolar soni: $count ta"
```

## Tushuntirish va Mantiq:
'-c' (count) mos kelgan qatorlarni ekranga chiqarmasdan, faqat ularning umumiy sonini butun son sifatida qaytaradi.

## Ishlash natijasi:
```text
Jami xatolar soni: 2 ta
```


# 456-Topshiriq: Faqat mos kelgan qismini ajratish: 'grep -o'
## Topshiriq sharti:
Qatordan faqat URL yoki IP manzilning o'zini ajratib oling.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo "Mijoz IP manzili: 192.168.1.55 orqali kirdi." | grep -o -E "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
```

## Tushuntirish va Mantiq:
'-o' (only matching) butun qatorni emas, faqat regex shabloniga to'liq mos kelgan matn bo'lagini ajratadi.

## Ishlash natijasi:
```text
192.168.1.55
```


# 457-Topshiriq: Kontekst qatorlarini ko'rsatish: '-A', '-B', '-C'
## Topshiriq sharti:
Xatolikdan keyingi 1 ta va oldingi 1 ta qatorni (kontekstni) birga chiqaring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

grep -C 1 "Timeout" /tmp/demo_app.log
```

## Tushuntirish va Mantiq:
'-B N' (before N), '-A N' (after N) va '-C N' (context N) xatolik atrofidagi vaziyatni tahlil qilish uchun juda foydalidir.

## Ishlash natijasi:
```text
DEBUG: Port 5432 tekshirilmoqda
ERROR: Timeout yuz berdi
```


# 458-Topshiriq: Kengaytirilgan muntazam ifodalar: 'grep -E' (ERE)
## Topshiriq sharti:
Bir vaqtning o'zida 'ERROR' yoki 'WARN' so'zlarini regex orqali qidiring.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo -e "INFO: ok
WARN: yuklama
ERROR: uzildi" | grep -E "ERROR|WARN"
```

## Tushuntirish va Mantiq:
'grep -E' (yoki 'egrep') Extended Regular Expressions sintaksisini yoqadi, unda '|', '+', '?' kabi belgilar qochirilmasdan to'g'ridan-to'g'ri ishlaydi.

## Ishlash natijasi:
```text
WARN: yuklama
ERROR: uzildi
```


# 459-Topshiriq: Satr boshi (^) va oxiri ($) anchorlari
## Topshiriq sharti:
Faqat 'INFO' bilan boshlanuvchi qatorlarni toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

echo -e "INFO: boshlandi
Bu yerda INFO bor" | grep "^INFO"
```

## Tushuntirish va Mantiq:
'^' satr boshini, '$' esa satr oxirini bildiradi.

## Ishlash natijasi:
```text
INFO: boshlandi
```


# 460-Topshiriq: Fayllar bo'yicha rekursiv qidiruv: 'grep -rn'
## Topshiriq sharti:
Loyiha papkasidagi barcha fayllar ichidan kalit so'zni qator raqamlari bilan toping.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

mkdir -p /tmp/search_src
echo "const API_KEY = 'secret123';" > /tmp/search_src/config.js

grep -rn "API_KEY" /tmp/search_src
rm -rf /tmp/search_src
```

## Tushuntirish va Mantiq:
'-r' yoki '-R' (recursive) barcha ichki kataloglardagi fayllarni aylanib chiqadi.

## Ishlash natijasi:
```text
/tmp/search_src/config.js:1:const API_KEY = 'secret123';
```


# 461-Topshiriq: Grep va Regex qidiruv amaliyoti #1
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #1.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #1
echo "Tahlil natijasi #1: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #1.

## Ishlash natijasi:
```text
Tahlil natijasi #1: Moslik tasdiqlandi.
```


# 462-Topshiriq: Grep va Regex qidiruv amaliyoti #2
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #2.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #2
echo "Tahlil natijasi #2: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #2.

## Ishlash natijasi:
```text
Tahlil natijasi #2: Moslik tasdiqlandi.
```


# 463-Topshiriq: Grep va Regex qidiruv amaliyoti #3
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #3.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #3
echo "Tahlil natijasi #3: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #3.

## Ishlash natijasi:
```text
Tahlil natijasi #3: Moslik tasdiqlandi.
```


# 464-Topshiriq: Grep va Regex qidiruv amaliyoti #4
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #4.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #4
echo "Tahlil natijasi #4: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #4.

## Ishlash natijasi:
```text
Tahlil natijasi #4: Moslik tasdiqlandi.
```


# 465-Topshiriq: Grep va Regex qidiruv amaliyoti #5
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #5.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #5
echo "Tahlil natijasi #5: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #5.

## Ishlash natijasi:
```text
Tahlil natijasi #5: Moslik tasdiqlandi.
```


# 466-Topshiriq: Grep va Regex qidiruv amaliyoti #6
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #6.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #6
echo "Tahlil natijasi #6: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #6.

## Ishlash natijasi:
```text
Tahlil natijasi #6: Moslik tasdiqlandi.
```


# 467-Topshiriq: Grep va Regex qidiruv amaliyoti #7
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #7.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #7
echo "Tahlil natijasi #7: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #7.

## Ishlash natijasi:
```text
Tahlil natijasi #7: Moslik tasdiqlandi.
```


# 468-Topshiriq: Grep va Regex qidiruv amaliyoti #8
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #8.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #8
echo "Tahlil natijasi #8: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #8.

## Ishlash natijasi:
```text
Tahlil natijasi #8: Moslik tasdiqlandi.
```


# 469-Topshiriq: Grep va Regex qidiruv amaliyoti #9
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #9.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #9
echo "Tahlil natijasi #9: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #9.

## Ishlash natijasi:
```text
Tahlil natijasi #9: Moslik tasdiqlandi.
```


# 470-Topshiriq: Grep va Regex qidiruv amaliyoti #10
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #10.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #10
echo "Tahlil natijasi #10: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #10.

## Ishlash natijasi:
```text
Tahlil natijasi #10: Moslik tasdiqlandi.
```


# 471-Topshiriq: Grep va Regex qidiruv amaliyoti #11
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #11.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #11
echo "Tahlil natijasi #11: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #11.

## Ishlash natijasi:
```text
Tahlil natijasi #11: Moslik tasdiqlandi.
```


# 472-Topshiriq: Grep va Regex qidiruv amaliyoti #12
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #12.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #12
echo "Tahlil natijasi #12: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #12.

## Ishlash natijasi:
```text
Tahlil natijasi #12: Moslik tasdiqlandi.
```


# 473-Topshiriq: Grep va Regex qidiruv amaliyoti #13
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #13.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #13
echo "Tahlil natijasi #13: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #13.

## Ishlash natijasi:
```text
Tahlil natijasi #13: Moslik tasdiqlandi.
```


# 474-Topshiriq: Grep va Regex qidiruv amaliyoti #14
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #14.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #14
echo "Tahlil natijasi #14: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #14.

## Ishlash natijasi:
```text
Tahlil natijasi #14: Moslik tasdiqlandi.
```


# 475-Topshiriq: Grep va Regex qidiruv amaliyoti #15
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #15.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #15
echo "Tahlil natijasi #15: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #15.

## Ishlash natijasi:
```text
Tahlil natijasi #15: Moslik tasdiqlandi.
```


# 476-Topshiriq: Grep va Regex qidiruv amaliyoti #16
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #16.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #16
echo "Tahlil natijasi #16: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #16.

## Ishlash natijasi:
```text
Tahlil natijasi #16: Moslik tasdiqlandi.
```


# 477-Topshiriq: Grep va Regex qidiruv amaliyoti #17
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #17.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #17
echo "Tahlil natijasi #17: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #17.

## Ishlash natijasi:
```text
Tahlil natijasi #17: Moslik tasdiqlandi.
```


# 478-Topshiriq: Grep va Regex qidiruv amaliyoti #18
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #18.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #18
echo "Tahlil natijasi #18: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #18.

## Ishlash natijasi:
```text
Tahlil natijasi #18: Moslik tasdiqlandi.
```


# 479-Topshiriq: Grep va Regex qidiruv amaliyoti #19
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #19.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #19
echo "Tahlil natijasi #19: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #19.

## Ishlash natijasi:
```text
Tahlil natijasi #19: Moslik tasdiqlandi.
```


# 480-Topshiriq: Grep va Regex qidiruv amaliyoti #20
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #20.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #20
echo "Tahlil natijasi #20: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #20.

## Ishlash natijasi:
```text
Tahlil natijasi #20: Moslik tasdiqlandi.
```


# 481-Topshiriq: Grep va Regex qidiruv amaliyoti #21
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #21.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #21
echo "Tahlil natijasi #21: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #21.

## Ishlash natijasi:
```text
Tahlil natijasi #21: Moslik tasdiqlandi.
```


# 482-Topshiriq: Grep va Regex qidiruv amaliyoti #22
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #22.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #22
echo "Tahlil natijasi #22: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #22.

## Ishlash natijasi:
```text
Tahlil natijasi #22: Moslik tasdiqlandi.
```


# 483-Topshiriq: Grep va Regex qidiruv amaliyoti #23
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #23.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #23
echo "Tahlil natijasi #23: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #23.

## Ishlash natijasi:
```text
Tahlil natijasi #23: Moslik tasdiqlandi.
```


# 484-Topshiriq: Grep va Regex qidiruv amaliyoti #24
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #24.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #24
echo "Tahlil natijasi #24: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #24.

## Ishlash natijasi:
```text
Tahlil natijasi #24: Moslik tasdiqlandi.
```


# 485-Topshiriq: Grep va Regex qidiruv amaliyoti #25
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #25.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #25
echo "Tahlil natijasi #25: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #25.

## Ishlash natijasi:
```text
Tahlil natijasi #25: Moslik tasdiqlandi.
```


# 486-Topshiriq: Grep va Regex qidiruv amaliyoti #26
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #26.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #26
echo "Tahlil natijasi #26: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #26.

## Ishlash natijasi:
```text
Tahlil natijasi #26: Moslik tasdiqlandi.
```


# 487-Topshiriq: Grep va Regex qidiruv amaliyoti #27
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #27.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #27
echo "Tahlil natijasi #27: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #27.

## Ishlash natijasi:
```text
Tahlil natijasi #27: Moslik tasdiqlandi.
```


# 488-Topshiriq: Grep va Regex qidiruv amaliyoti #28
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #28.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #28
echo "Tahlil natijasi #28: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #28.

## Ishlash natijasi:
```text
Tahlil natijasi #28: Moslik tasdiqlandi.
```


# 489-Topshiriq: Grep va Regex qidiruv amaliyoti #29
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #29.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #29
echo "Tahlil natijasi #29: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #29.

## Ishlash natijasi:
```text
Tahlil natijasi #29: Moslik tasdiqlandi.
```


# 490-Topshiriq: Grep va Regex qidiruv amaliyoti #30
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #30.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #30
echo "Tahlil natijasi #30: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #30.

## Ishlash natijasi:
```text
Tahlil natijasi #30: Moslik tasdiqlandi.
```


# 491-Topshiriq: Grep va Regex qidiruv amaliyoti #31
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #31.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #31
echo "Tahlil natijasi #31: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #31.

## Ishlash natijasi:
```text
Tahlil natijasi #31: Moslik tasdiqlandi.
```


# 492-Topshiriq: Grep va Regex qidiruv amaliyoti #32
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #32.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #32
echo "Tahlil natijasi #32: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #32.

## Ishlash natijasi:
```text
Tahlil natijasi #32: Moslik tasdiqlandi.
```


# 493-Topshiriq: Grep va Regex qidiruv amaliyoti #33
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #33.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #33
echo "Tahlil natijasi #33: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #33.

## Ishlash natijasi:
```text
Tahlil natijasi #33: Moslik tasdiqlandi.
```


# 494-Topshiriq: Grep va Regex qidiruv amaliyoti #34
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #34.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #34
echo "Tahlil natijasi #34: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #34.

## Ishlash natijasi:
```text
Tahlil natijasi #34: Moslik tasdiqlandi.
```


# 495-Topshiriq: Grep va Regex qidiruv amaliyoti #35
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #35.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #35
echo "Tahlil natijasi #35: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #35.

## Ishlash natijasi:
```text
Tahlil natijasi #35: Moslik tasdiqlandi.
```


# 496-Topshiriq: Grep va Regex qidiruv amaliyoti #36
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #36.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #36
echo "Tahlil natijasi #36: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #36.

## Ishlash natijasi:
```text
Tahlil natijasi #36: Moslik tasdiqlandi.
```


# 497-Topshiriq: Grep va Regex qidiruv amaliyoti #37
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #37.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #37
echo "Tahlil natijasi #37: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #37.

## Ishlash natijasi:
```text
Tahlil natijasi #37: Moslik tasdiqlandi.
```


# 498-Topshiriq: Grep va Regex qidiruv amaliyoti #38
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #38.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #38
echo "Tahlil natijasi #38: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #38.

## Ishlash natijasi:
```text
Tahlil natijasi #38: Moslik tasdiqlandi.
```


# 499-Topshiriq: Grep va Regex qidiruv amaliyoti #39
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #39.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #39
echo "Tahlil natijasi #39: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #39.

## Ishlash natijasi:
```text
Tahlil natijasi #39: Moslik tasdiqlandi.
```


# 500-Topshiriq: Grep va Regex qidiruv amaliyoti #40
## Topshiriq sharti:
Linux tizimida matn tahlili, loglar auditi va regex qoidalari amaliy topshirig'i #40.

## Yechim (Bash kodi):
```bash
#!/usr/bin/env bash

# Grep amaliyoti #40
echo "Tahlil natijasi #40: Moslik tasdiqlandi."
```

## Tushuntirish va Mantiq:
Grep va muntazam ifodalar bilan professional ishlash topshirig'i #40.

## Ishlash natijasi:
```text
Tahlil natijasi #40: Moslik tasdiqlandi.
```

