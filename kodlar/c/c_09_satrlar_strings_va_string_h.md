# C Dasturlash Tili — 9-Qism: Satrlar (Strings) va string.h
## (401-450 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* Null-terminated strings ('\0') mohiyati va xavfsiz satr operatsiyalari
* string.h kutubxonasi: strlen, strcpy, strncpy, strcat, strncat, strcmp, strncmp
* Qidiruv va ajratish: strchr, strrchr, strstr, strspn, strcspn, strtok, strtok_r
* Xotira manipulyatsiyasi: memset, memcpy, memmove va sprintf/snprintf xavfsizligi
* Matnlarni tahlil qilish, Sezar shifri, RLE siqish va Mini JSON Parser

---

# 401-Topshiriq: Null-terminated satrlar tushunchasi va oxiridagi '\0' belgisi

## Topshiriq sharti:
Satr oxiridagi nol bayti nima uchun kerakligini va uning massivdagi o'rnini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // 5 ta harf + 1 ta '\0' (jami 6 bayt)
    char satr[6] = {'S', 'a', 'l', 'o', 'm', '\0'};

    printf("Satr: %s\n", satr);
    printf("Oxirgi nol baytining ASCII kodi: %d\n", satr[5]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida satr alohida tur emas, balki oxiri `\0` (nol qiymatli bayt) bilan tugaydigan `char` massividir.
2. Barcha standart satr funksiyalari satr tugaganini bilish uchun aynan `\0` belgisini qidiradi.

## Ishlash natijasi:
```text
Satr: Salom
Oxirgi nol baytining ASCII kodi: 0
```

---

# 402-Topshiriq: Satr uzunligini qo'lda hisoblash va strlen() kutubxona funksiyasi

## Topshiriq sharti:
Satr uzunligini tsikl bilan va strlen orqali hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char matn[] = "Algoritm";
    size_t hisob = 0;

    while (matn[hisob] != '\0') {
        hisob++;
    }

    printf("Qo'lda hisoblangan uzunlik: %zu\n", hisob);
    printf("strlen() qaytargan uzunlik:  %zu\n", strlen(matn));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strlen()` satrdagi harflar sonini hisoblaydi, lekin oxiridagi `\0` belgisini hisobga qo'shmaydi.
2. Shuning uchun "Algoritm" uzunligi 8 ga teng.

## Ishlash natijasi:
```text
Qo'lda hisoblangan uzunlik: 8
strlen() qaytargan uzunlik:  8
```

---

# 403-Topshiriq: strcpy() orqali satrni nusxalash va uning xavfi

## Topshiriq sharti:
Bir satrni ikkinchisiga ko'chiring va bufer sig'imi yetarli bo'lishi shartligini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char manba[] = "Toshkent";
    char nishon[20]; // 20 bayt xotira — "Toshkent" (9 bayt) sig'adi

    strcpy(nishon, manba);
    printf("Nusxalangan satr: %s\n", nishon);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strcpy(dest, src)` manbadan belgilar va `\0` ni nishonga to'liq nusxalaydi.
2. Xavfi: agar `dest` o'lchami kichik bo'lsa, `strcpy` baribir yozishda davom etadi va buferni to'ldirib yuboradi (Buffer Overflow).

## Ishlash natijasi:
```text
Nusxalangan satr: Toshkent
```

---

# 404-Topshiriq: strncpy() orqali xavfsiz nusxalash va '\0' bilan yakunlash

## Topshiriq sharti:
Hajmi cheklangan holda satrni xavfsiz nusxalash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char manba[] = "Bu juda uzun matn";
    char nishon[10];

    strncpy(nishon, manba, sizeof(nishon) - 1);
    nishon[sizeof(nishon) - 1] = '\0'; // Har doim oxiriga nol qo'yish shart!

    printf("Xavfsiz qirqilgan satr: %s\n", nishon);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strncpy` eng ko'pi bilan berilgan `n` ta belgini ko'chiradi.
2. Agar manba `n` dan uzun bo'lsa, `strncpy` oxiriga `\0` qo'ymaydi, shuning uchun oxirgi katakni o'zimiz majburiy `\0` qilishimiz kerak.

## Ishlash natijasi:
```text
Xavfsiz qirqilgan satr: Bu juda u
```

---

# 405-Topshiriq: strcat() orqali satrlarni ulash (Konkatenatsiya)

## Topshiriq sharti:
Ikki satrni bitta satrga birlashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char salom[30] = "Assalomu ";
    char ism[] = "Alaykum!";

    strcat(salom, ism);
    printf("Birlashgan satr: %s\n", salom);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strcat(dest, src)` birinchi satrning oxiridagi `\0` o'rnidan boshlab ikkinchi satrni yozadi.

## Ishlash natijasi:
```text
Birlashgan satr: Assalomu Alaykum!
```

---

# 406-Topshiriq: strncat() orqali chegaralangan xavfsiz ulanish

## Topshiriq sharti:
Nishon buferining bo'sh joyidan oshmagan holda satrlarni ulang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char bufer[15] = "Salom ";
    char davomi[] = "Dunyo va O'zbekiston!";

    size_t qolgan_joy = sizeof(bufer) - strlen(bufer) - 1;
    strncat(bufer, davomi, qolgan_joy);

    printf("Xavfsiz ulangan satr: %s\n", bufer);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strncat` belgilangan sondan ortiq belgi qo'shmaydi va avtomatik ravishda oxiriga `\0` belgisini qo'yadi.

## Ishlash natijasi:
```text
Xavfsiz ulangan satr: Salom Dunyo va
```

---

# 407-Topshiriq: strcmp() orqali leksikografik taqqoslash

## Topshiriq sharti:
Ikki satrning tengligi, kichik yoki kattaligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char s1[] = "olma";
    char s2[] = "anor";
    char s3[] = "olma";

    printf("strcmp('olma', 'olma'): %d\n", strcmp(s1, s3));
    printf("strcmp('olma', 'anor'): %d\n", strcmp(s1, s2));
    printf("strcmp('anor', 'olma'): %d\n", strcmp(s2, s1));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Teng bo'lsa 0, birinchi satr alifboda keyin tursa musbat (>0), oldin tursa manfiy (<0) qaytaradi.

## Ishlash natijasi:
```text
strcmp('olma', 'olma'): 0
strcmp('olma', 'anor'): 1
strcmp('anor', 'olma'): -1
```

---

# 408-Topshiriq: strncmp() orqali prefikslarni solishtirish

## Topshiriq sharti:
Buyruqning 'GET ' bilan boshlanishini dastlabki 4 ta belgi bo'yicha tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char so_rov[] = "GET /index.html HTTP/1.1";

    if (strncmp(so_rov, "GET ", 4) == 0) {
        printf("Bu HTTP GET so'rovi!\n");
    } else {
        printf("Boshqa turdagi so'rov.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strncmp(s1, s2, n)` faqat birinchi `n` ta belgini taqqoslaydi.
2. Bu protokollarni tahlil qilishda prefiks tekshirish uchun qulaydir.

## Ishlash natijasi:
```text
Bu HTTP GET so'rovi!
```

---

# 409-Topshiriq: strchr() orqali belgining birinchi uchrashini qidirish

## Topshiriq sharti:
Elektron pochta manzilida '@' belgisi mavjudligini va domen qismini ajrating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char email[] = "foydalanuvchi@milliy.uz";
    char *kuchukcha = strchr(email, '@');

    if (kuchukcha != NULL) {
        printf("Email yaroqli!\n");
        printf("Domen: %s\n", kuchukcha + 1);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strchr` belgini qidirib, uning satrdagi birinchi manzilini ko'rsatkich sifatida qaytaradi.
2. `kuchukcha + 1` esa domenni ko'rsatadi.

## Ishlash natijasi:
```text
Email yaroqli!
Domen: milliy.uz
```

---

# 410-Topshiriq: strrchr() orqali belgining oxirgi uchrashini topish (Fayl kengaytmasi)

## Topshiriq sharti:
Fayl nomining oxirgi nuqtasidan keyingi kengaytmasini (.c, .txt) oling.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char fayl_nomi[] = "mening.dastur.kodi.c";
    char *nuqta = strrchr(fayl_nomi, '.');

    if (nuqta != NULL) {
        printf("Fayl kengaytmasi: %s\n", nuqta);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strrchr` (reverse character) satr oxiridan qarab belgini qidiradi.
2. Bu fayl nomlaridagi ko'p nuqtalar orasidan eng oxirgisini topishda standartdir.

## Ishlash natijasi:
```text
Fayl kengaytmasi: .c
```

---

# 411-Topshiriq: strstr() orqali qism-satrni (Substring) qidirish

## Topshiriq sharti:
Matn ichidan so'z qidirish algoritmi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char matn[] = "Bugun C dasturlash tili bo'yicha dars.";
    char *joyi = strstr(matn, "dasturlash");

    if (joyi != NULL) {
        printf("Qidirilgan so'z topildi! Indeks: %td\n", joyi - matn);
        printf("Topilgan joydan boshlab: '%s'\n", joyi);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strstr` butun so'z yoki iborani qidirib, uning boshlanish manzilini qaytaradi.

## Ishlash natijasi:
```text
Qidirilgan so'z topildi! Indeks: 8
Topilgan joydan boshlab: 'dasturlash tili bo'yicha dars.'
```

---

# 412-Topshiriq: strspn() orqali faqat ruxsat etilgan belgilardan iborat qism uzunligini topish

## Topshiriq sharti:
Satr boshidagi faqat raqamlardan iborat bo'lgan prefiks uzunligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char satr[] = "12345ABCDE";
    size_t raqamlar_uzunligi = strspn(satr, "0123456789");

    printf("Boshidagi raqamlar soni: %zu ta\n", raqamlar_uzunligi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strspn(s, accept)` ikkinchi argumentdagi to'plamdan boshqa belgi uchraguncha nechta belgi o'tganini qaytaradi.

## Ishlash natijasi:
```text
Boshidagi raqamlar soni: 5 ta
```

---

# 413-Topshiriq: strcspn() orqali taqiqlangan belgigacha bo'lgan masofani topish

## Topshiriq sharti:
Satr oxiridagi '\n' belgisini topib uni '\0' ga almashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char kiritish[30] = "Salom Dunyo!\n";
    // '\n' yoki '\r' uchraguncha bo'lgan uzunlikni topish:
    kiritish[strcspn(kiritish, "\r\n")] = '\0';

    printf("Tozalangan satr: '%s'\n", kiritish);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `fgets` orqali olingan satr oxiridagi `\n` ni olib tashlashning C dagi eng toza va xavfsiz usulidir.

## Ishlash natijasi:
```text
Tozalangan satr: 'Salom Dunyo!'
```

---

# 414-Topshiriq: strpbrk() orqali belgilar to'plamidan birinchisini topish

## Topshiriq sharti:
Satrdagi birinchi uchragan unli harfni toping.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char matn[] = "shrift";
    char *birinchi_unli = strpbrk(matn, "aeiouAEIOU");

    if (birinchi_unli != NULL) {
        printf("Birinchi unli harf: '%c' (Indeksi: %td)\n", 
               *birinchi_unli, birinchi_unli - matn);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strpbrk` to'plamdagi ixtiyoriy belgi birinchi bo'lib uchragan joy manzilini qaytaradi.

## Ishlash natijasi:
```text
Birinchi unli harf: 'i' (Indeksi: 3)
```

---

# 415-Topshiriq: strtok() orqali CSV satrini maydonlarga ajratish

## Topshiriq sharti:
Vergul bilan ajratilgan ma'lumotlarni tokenlarga bo'lib chiqing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char csv_qator[] = "Ali,20,Toshkent,Dasturchi";
    char *token = strtok(csv_qator, ",");

    while (token != NULL) {
        printf("Maydon: %s\n", token);
        token = strtok(NULL, ",");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strtok` asl satr ichidagi ajratuvchilarni `\0` ga almashtiradi.
2. Keyingi chaqiruvlarda birinchi parametrga `NULL` beriladi, u o'z ichidagi statik ko'rsatkichdan davom etadi.

## Ishlash natijasi:
```text
Maydon: Ali
Maydon: 20
Maydon: Toshkent
Maydon: Dasturchi
```

---

# 416-Topshiriq: strtok_r() / strtok_s() reentrant xavfsiz tokenizer tushunchasi

## Topshiriq sharti:
Statik xotirasiz, holat ko'rsatkichini tashqaridan uzatib xavfsiz tokenizatsiya qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char matn[] = "A-B-C";
    char *saveptr;
    // strtok_s (Windows MSVC) yoki strtok_r (POSIX Linux)
    #ifdef _WIN32
    char *tok = strtok_s(matn, "-", &saveptr);
    while (tok) {
        printf("Token: %s\n", tok);
        tok = strtok_s(NULL, "-", &saveptr);
    }
    #else
    char *tok = strtok_r(matn, "-", &saveptr);
    while (tok) {
        printf("Token: %s\n", tok);
        tok = strtok_r(NULL, "-", &saveptr);
    }
    #endif
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Standart `strtok` ichki statik o'zgaruvchi ishlatgani uchun ko'p oqimli dasturlarda (Thread-Safe emas) bir-birining ishini buzadi.
2. `strtok_r` esa holatni `saveptr` ko'rsatkichida saqlab, 100% thread-safe ishlaydi.

## Ishlash natijasi:
```text
Token: A
Token: B
Token: C
```

---

# 417-Topshiriq: memset() orqali string buferini tozalash

## Topshiriq sharti:
Buferni to'liq nollar bilan tozalab xavfsizlantiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char bufer[10] = "Parol123";
    printf("Oldin: %s\n", bufer);

    memset(bufer, 0, sizeof(bufer));
    printf("Tozalangach buferning birinchi belgisi ASCII: %d\n", bufer[0]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Maxfiy parollar va kalitlar ishlatib bo'lingach, ularni RAM da qolib ketmasligi uchun darhol `memset` bilan 0 qilinadi.

## Ishlash natijasi:
```text
Oldin: Parol123
Tozalangach buferning birinchi belgisi ASCII: 0
```

---

# 418-Topshiriq: memmove() orqali bir-birini qoplovchi (Overlapping) xotira bloklarini xavfsiz ko'chirish

## Topshiriq sharti:
Satr boshidagi 3 ta harfni 1 ta o'ngga surishda memmove va memcpy farqi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char matn[10] = "12345";

    // Xotira bloklari bir-birining ustiga tushadi (Overlapping)
    // memcpy bunday holatda Undefined Behavior keltirib chiqaradi!
    // memmove esa vaqtinchalik bufer orqali xavfsiz ko'chiradi:
    memmove(matn + 1, matn, 4);

    printf("memmove natijasi: %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xotira bloklari bir-birini qoplaganda har doim `memmove` ishlatilishi shart.

## Ishlash natijasi:
```text
memmove natijasi: 11234
```

---

# 419-Topshiriq: sprintf() orqali o'zgaruvchilarni satrga formatlab yozish

## Topshiriq sharti:
Son va matnlarni birlashtirib bitta satr hosil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char xabar[50];
    const char *foydalanuvchi = "Jasur";
    int ball = 98;

    sprintf(xabar, "Foydalanuvchi %s natijasi: %d ball", foydalanuvchi, ball);
    printf("%s\n", xabar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sprintf` konsolga emas, xotiradagi `char` massiviga formatlangan matn yozadi.

## Ishlash natijasi:
```text
Foydalanuvchi Jasur natijasi: 98 ball
```

---

# 420-Topshiriq: snprintf() orqali xavfsiz formatlash (Bufer to'lishidan qat'iy himoya)

## Topshiriq sharti:
Hajmi cheklangan buferga snprintf bilan yozish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char kichik_bufer[15];
    int kod = 123456789;

    // snprintf hech qachon bufer o'lchamidan oshib ketmaydi
    int kerak_bolgan = snprintf(kichik_bufer, sizeof(kichik_bufer), "Kod: %d", kod);

    printf("Hosil bo'lgan satr: %s\n", kichik_bufer);
    printf("To'liq yozish uchun kerak bo'lgan hajm: %d bayt\n", kerak_bolgan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `snprintf` C99 da kiritilgan bo'lib, `sprintf` o'rniga har doim ishlatilishi tavsiya etiladi.
2. U buferdan oshib ketmaydi va qancha hajm kerak bo'lganini qaytaradi.

## Ishlash natijasi:
```text
Hosil bo'lgan satr: Kod: 123456789
To'liq yozish uchun kerak bo'lgan hajm: 14 bayt
```

---

# 421-Topshiriq: sscanf() orqali satr ichidan formatlangan ma'lumotlarni o'qish (Parsing)

## Topshiriq sharti:
Sanani '2026-11-08' formatidagi satrdan int o'zgaruvchilarga ajratib oling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    const char *sana_matni = "2026-11-08";
    int yil, oy, kun;

    int muvaffaqiyat = sscanf(sana_matni, "%d-%d-%d", &yil, &oy, &kun);

    if (muvaffaqiyat == 3) {
        printf("Yil: %d, Oy: %d, Kun: %d\n", yil, oy, kun);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sscanf` klaviaturadan emas, satr ichidan qiymatlarni o'qiydi.

## Ishlash natijasi:
```text
Yil: 2026, Oy: 11, Kun: 8
```

---

# 422-Topshiriq: Satrdagi barcha harflarni katta registrga o'tkazish (toupper, ctype.h)

## Topshiriq sharti:
Satrni joyida bosh harflarga aylantiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

void satr_katta(char *s) {
    while (*s) {
        *s = (char)toupper((unsigned char)*s);
        s++;
    }
}

int main(void) {
    char matn[] = "salom, dunyo!";
    satr_katta(matn);
    printf("Katta harflarda: %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `toupper` harf bo'lmagan belgilarga (tinish belgilari, probel) tegmaydi.

## Ishlash natijasi:
```text
Katta harflarda: SALOM, DUNYO!
```

---

# 423-Topshiriq: Satrdagi barcha harflarni kichik registrga o'tkazish (tolower)

## Topshiriq sharti:
Satrni joyida kichik harflarga o'giring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

void satr_kichik(char *s) {
    while (*s) {
        *s = (char)tolower((unsigned char)*s);
        s++;
    }
}

int main(void) {
    char matn[] = "C99 STANDARTI";
    satr_kichik(matn);
    printf("Kichik harflarda: %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `tolower` barcha bosh harflarni kichik qiladi.

## Ishlash natijasi:
```text
Kichik harflarda: c99 standarti
```

---

# 424-Topshiriq: Satr boshidagi va oxiridagi bo'shliqlarni tozalash (Trim)

## Topshiriq sharti:
Matn chetidagi keraksiz bo'shliqlarni olib tashlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

char* trim(char *s) {
    // Boshidagi probellarni o'tkazish
    while (isspace((unsigned char)*s)) s++;
    if (*s == 0) return s;

    // Oxiridagi probellarni qirqish
    char *oxir = s + strlen(s) - 1;
    while (oxir > s && isspace((unsigned char)*oxir)) oxir--;
    *(oxir + 1) = '\0';

    return s;
}

int main(void) {
    char matn[] = "   Salom Dunyo   ";
    char *tozalangan = trim(matn);
    printf("Tozalangan: '%s'\n", tozalangan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boshidagi probellardan o'tib, oxirgi probel o'rniga `\0` qo'yish orqali tozalash amalga oshiriladi.

## Ishlash natijasi:
```text
Tozalangan: 'Salom Dunyo'
```

---

# 425-Topshiriq: Satr ichidagi so'zlar sonini sanash

## Topshiriq sharti:
Bo'shliqlar bilan ajratilgan so'zlar miqdorini hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

int sozlar_soni(const char *s) {
    int hisob = 0;
    bool sozdami = false;

    while (*s) {
        if (!isspace((unsigned char)*s)) {
            if (!sozdami) {
                hisob++;
                sozdami = true;
            }
        } else {
            sozdami = false;
        }
        s++;
    }
    return hisob;
}

int main(void) {
    const char *matn = "  C dasturlash   tili juda tezkor  ";
    printf("So'zlar soni: %d ta\n", sozlar_soni(matn));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Holat bayrog'i (`sozdami`) ketma-ket bir nechta probellar bo'lganda ham so'zlarni to'g'ri sanashni ta'minlaydi.

## Ishlash natijasi:
```text
So'zlar soni: 4 ta
```

---

# 426-Topshiriq: Satr ichidagi unli va undosh harflar sonini hisoblash

## Topshiriq sharti:
Matndagi harflar statistikasini chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    const char *matn = "Antigravity";
    int unlilar = 0, undoshlar = 0;

    for (int i = 0; matn[i] != '\0'; i++) {
        char ch = tolower((unsigned char)matn[i]);
        if (ch >= 'a' && ch <= 'z') {
            if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
                unlilar++;
            } else {
                undoshlar++;
            }
        }
    }

    printf("'%s': Unlilar: %d, Undoshlar: %d\n", matn, unlilar, undoshlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Antigravity so'zida: a, i, a, i (4 ta unli); n, t, g, r, v, t, y (7 ta undosh).

## Ishlash natijasi:
```text
'Antigravity': Unlilar: 4, Undoshlar: 7
```

---

# 427-Topshiriq: Satrdagi har bir so'zni alohida teskarisiga o'girish

## Topshiriq sharti:
'Salom Dunyo' satrini 'molaS oynuD' ga aylantiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void teskari_qism(char *bosh, char *oxir) {
    while (bosh < oxir) {
        char t = *bosh; *bosh = *oxir; *oxir = t;
        bosh++; oxir--;
    }
}

void har_bir_sozni_ogir(char *s) {
    char *soz_boshi = s;
    while (*s) {
        if (*s == ' ') {
            teskari_qism(soz_boshi, s - 1);
            soz_boshi = s + 1;
        }
        s++;
    }
    teskari_qism(soz_boshi, s - 1); // Oxirgi so'z
}

int main(void) {
    char matn[] = "Salom Dunyo";
    har_bir_sozni_ogir(matn);
    printf("Natija: %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir so'z probel bo'yicha aniqlanib, o'z joyida teskarisiga aylantiriladi.

## Ishlash natijasi:
```text
Natija: molaS oynuD
```

---

# 428-Topshiriq: So'zlarning o'zaro joylashuv tartibini teskari qilish

## Topshiriq sharti:
'Salom Dunyo' matnini 'Dunyo Salom' ko'rinishiga o'tkazing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void teskari_oraliq(char *bosh, char *oxir) {
    while (bosh < oxir) {
        char t = *bosh; *bosh = *oxir; *oxir = t;
        bosh++; oxir--;
    }
}

void sozlarni_teskari_qil(char *s) {
    int len = strlen(s);
    // 1-qadam: Butun satrni teskari qilish ("oynuD molaS")
    teskari_oraliq(s, s + len - 1);

    // 2-qadam: Har bir so'zni alohida qayta teskari qilish ("Dunyo Salom")
    char *bosh = s;
    for (char *p = s; p <= s + len; p++) {
        if (*p == ' ' || *p == '\0') {
            teskari_oraliq(bosh, p - 1);
            bosh = p + 1;
        }
    }
}

int main(void) {
    char matn[] = "Salom Dunyo";
    sozlarni_teskari_qil(matn);
    printf("Natija: %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Butun satrni teskari qilib, keyin har bir so'zni qayta teskari qilish O(N) vaqt va O(1) qo'shimcha xotira bilan so'zlarni almashtiradi.

## Ishlash natijasi:
```text
Natija: Dunyo Salom
```

---

# 429-Topshiriq: Palindrom jumlani tekshirish (Katta-kichik harf va belgilarni inobatga olmasdan)

## Topshiriq sharti:
'A man, a plan, a canal: Panama' jumlasi palindromligini isbotlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

bool jumla_palindrom(const char *s) {
    int chap = 0;
    int ong = strlen(s) - 1;

    while (chap < ong) {
        while (chap < ong && !isalnum((unsigned char)s[chap])) chap++;
        while (chap < ong && !isalnum((unsigned char)s[ong])) ong--;

        if (tolower((unsigned char)s[chap]) != tolower((unsigned char)s[ong])) {
            return false;
        }
        chap++;
        ong--;
    }
    return true;
}

int main(void) {
    const char *jumla = "A man, a plan, a canal: Panama";
    printf("Jumla palindrommi: %s\n", jumla_palindrom(jumla) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Probellar va tinish belgilari o'tkazib yuboriladi, harflar esa kichik registrda taqqoslanadi.

## Ishlash natijasi:
```text
Jumla palindrommi: Ha
```

---

# 430-Topshiriq: Anagramma tekshiruvi (Ikki so'z bir xil harflardan tuzilganmi)

## Topshiriq sharti:
'silent' va 'listen' so'zlari anagramma ekanligini chastota massivi bilan aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool anagrammami(const char *s1, const char *s2) {
    if (strlen(s1) != strlen(s2)) return false;

    int hisob[256] = {0};
    for (int i = 0; s1[i] != '\0'; i++) {
        hisob[(unsigned char)s1[i]]++;
        hisob[(unsigned char)s2[i]]--;
    }

    for (int i = 0; i < 256; i++) {
        if (hisob[i] != 0) return false;
    }
    return true;
}

int main(void) {
    printf("'silent' va 'listen' anagrammami: %s\n", 
           anagrammami("silent", "listen") ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Harflar chastotasi bir xil bo'lsa barcha hisoblar 0 bo'ladi.

## Ishlash natijasi:
```text
'silent' va 'listen' anagrammami: Ha
```

---

# 431-Topshiriq: Xavfsiz son konvertatsiyasi: strtol() (String to Long)

## Topshiriq sharti:
atoi() o'rniga xatolikni ushlay oladigan strtol dan foydalaning.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

int main(void) {
    const char *matn = "12345XYZ";
    char *oxirgi_belgi;

    long son = strtol(matn, &oxirgi_belgi, 10);

    printf("O'qilgan son: %ld\n", son);
    printf("O'qilmay qolgan qoldiq: '%s'\n", oxirgi_belgi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strtol` son tugagan joy ko'rsatkichini (`oxirgi_belgi`) qaytaradi.
2. Bu kiritishdagi xatoliklarni aniq ushlash imkonini beradi.

## Ishlash natijasi:
```text
O'qilgan son: 12345
O'qilmay qolgan qoldiq: 'XYZ'
```

---

# 432-Topshiriq: Xavfsiz haqiqiy son konvertatsiyasi: strtod() (String to Double)

## Topshiriq sharti:
Matn ichidagi haqiqiy sonni double ga o'giring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const char *matn = "3.14159 rad";
    char *oxiri;

    double d = strtod(matn, &oxiri);
    printf("Haqiqiy son: %.5lf\n", d);
    printf("Birlik: '%s'\n", oxiri);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strtod` suzuvchi nuqtali sonlarni xatolarsiz o'qiydi.

## Ishlash natijasi:
```text
Haqiqiy son: 3.14159
Birlik: ' rad'
```

---

# 433-Topshiriq: Butun sonni satrga o'girish (snprintf orqali)

## Topshiriq sharti:
Butun sonni formatlangan satrga aylantiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = -9876;
    char bufer[20];

    snprintf(bufer, sizeof(bufer), "%d", son);
    printf("Satr ko'rinishi: '%s'\n", bufer);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C standartida `itoa` portativ emas; `snprintf` butun sonni satrga o'girishning eng toza standart usulidir.

## Ishlash natijasi:
```text
Satr ko'rinishi: '-9876'
```

---

# 434-Topshiriq: Satr ichidagi so'zni almashtirish (String Replace: 'olma' -> 'anor')

## Topshiriq sharti:
Berilgan so'zni yangi so'z bilan almashtiruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void so_z_almashtir(const char *matn, const char *eski, const char *yangi, char *natija) {
    const char *p = strstr(matn, eski);
    if (!p) {
        strcpy(natija, matn);
        return;
    }
    int bosh_uzunlik = p - matn;
    strncpy(natija, matn, bosh_uzunlik);
    natija[bosh_uzunlik] = '\0';
    strcat(natija, yangi);
    strcat(natija, p + strlen(eski));
}

int main(void) {
    char natija[50];
    so_z_almashtir("Qizil olma shirin", "olma", "anor", natija);
    printf("%s\n", natija);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strstr` bilan eski so'z topiladi va uning o'rniga yangi so'z ulanadi.

## Ishlash natijasi:
```text
Qizil anor shirin
```

---

# 435-Topshiriq: Satrni belgilar bilan chapdan to'ldirish (Pad Left)

## Topshiriq sharti:
Sonli satrni 8 xonagacha oldidan '0' bilan to'ldiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void pad_left(char *dest, const char *src, size_t jami_uzunlik, char belgi) {
    size_t len = strlen(src);
    if (len >= jami_uzunlik) {
        strcpy(dest, src);
        return;
    }
    size_t pad_soni = jami_uzunlik - len;
    memset(dest, belgi, pad_soni);
    strcpy(dest + pad_soni, src);
}

int main(void) {
    char natija[20];
    pad_left(natija, "42", 6, '0');
    printf("Pad natijasi: %s\n", natija);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. "42" -> "000042".

## Ishlash natijasi:
```text
Pad natijasi: 000042
```

---

# 436-Topshiriq: Satrning berilgan prefiks bilan boshlanishini tekshirish (starts_with)

## Topshiriq sharti:
starts_with mantiqiy funksiyasini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool starts_with(const char *satr, const char *prefiks) {
    return strncmp(satr, prefiks, strlen(prefiks)) == 0;
}

int main(void) {
    printf("https:// boshlanadimi: %s\n", 
           starts_with("https://google.com", "https://") ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strncmp` yordamida prefiks uzunligicha solishtiriladi.

## Ishlash natijasi:
```text
https:// boshlanadimi: Ha
```

---

# 437-Topshiriq: Satrning berilgan suffiks bilan tugashini tekshirish (ends_with)

## Topshiriq sharti:
Fayl nomi .png bilan tugashini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool ends_with(const char *satr, const char *suffiks) {
    size_t s_len = strlen(satr);
    size_t suf_len = strlen(suffiks);
    if (suf_len > s_len) return false;
    return strcmp(satr + (s_len - suf_len), suffiks) == 0;
}

int main(void) {
    printf("rasm.png .png bilan tugaydimi: %s\n", 
           ends_with("rasm.png", ".png") ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Satr oxiridagi qism suffiks bilan solishtiriladi.

## Ishlash natijasi:
```text
rasm.png .png bilan tugaydimi: Ha
```

---

# 438-Topshiriq: Run-Length Encoding (RLE): Matnni sodda siqish

## Topshiriq sharti:
'AAABBC' ketma-ketligini 'A3B2C1' ko'rinishida siqing.

## Yechim (C kodi):
```c
#include <stdio.h>

void rle_siqish(const char *src, char *dest) {
    while (*src) {
        char ch = *src;
        int hisob = 0;
        while (*src == ch) {
            hisob++;
            src++;
        }
        dest += sprintf(dest, "%c%d", ch, hisob);
    }
}

int main(void) {
    char siqilgan[50];
    rle_siqish("AAABBC", siqilgan);
    printf("RLE natijasi: %s\n", siqilgan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ketma-ket bir xil harflar ularning soni bilan almashtiriladi.

## Ishlash natijasi:
```text
RLE natijasi: A3B2C1
```

---

# 439-Topshiriq: RLE siqilgan matnni qayta ochish (Decompression)

## Topshiriq sharti:
'A3B2C1' matnini qayta 'AAABBC' ga aylantiring.

## Yechim (C kodi):
```c
#include <stdio.h>

void rle_ochish(const char *src, char *dest) {
    while (*src) {
        char ch = *src++;
        int son = *src++ - '0';
        for (int i = 0; i < son; i++) {
            *dest++ = ch;
        }
    }
    *dest = '\0';
}

int main(void) {
    char ochilgan[50];
    rle_ochish("A3B2C1", ochilgan);
    printf("Ochilgan matn: %s\n", ochilgan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Siqilgan harf va uning soni bo'yicha belgilar qayta yoziladi.

## Ishlash natijasi:
```text
Ochilgan matn: AAABBC
```

---

# 440-Topshiriq: Satrdagi takrorlanuvchi belgilarni olib tashlash

## Topshiriq sharti:
Barcha belgilardan faqat bittadan nusxa qoldiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

void unikal_belgilar(char *s) {
    bool korindi[256] = {false};
    char *yozish = s;
    for (char *p = s; *p != '\0'; p++) {
        if (!korindi[(unsigned char)*p]) {
            korindi[(unsigned char)*p] = true;
            *yozish++ = *p;
        }
    }
    *yozish = '\0';
}

int main(void) {
    char matn[] = "dasturlash";
    unikal_belgilar(matn);
    printf("Unikal harflar: %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Hash jadvali (bool massiv) orqali takroriy harflar tashlab ketiladi.

## Ishlash natijasi:
```text
Unikal harflar: dasturlh
```

---

# 441-Topshiriq: Qavslar balansini satrda tekshirish (Parentheses Matching)

## Topshiriq sharti:
Faqat oddiy qavslar '(' va ')' to'g'ri yopilganini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool qavslar_togrimi(const char *s) {
    int balans = 0;
    while (*s) {
        if (*s == '(') balans++;
        else if (*s == ')') {
            balans--;
            if (balans < 0) return false;
        }
        s++;
    }
    return balans == 0;
}

int main(void) {
    printf("(()) to'g'rimi: %s\n", qavslar_togrimi("(())") ? "Ha" : "Yo'q");
    printf("(() to'g'rimi:  %s\n", qavslar_togrimi("(()") ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Balans hech qachon 0 dan pastga tushmasligi va oxirida aynan 0 bo'lishi kerak.

## Ishlash natijasi:
```text
(()) to'g'rimi: Ha
(() to'g'rimi:  Yo'q
```

---

# 442-Topshiriq: Sezar shifri (Caesar Cipher): Harflarni K pozitsiyaga siljitish

## Topshiriq sharti:
Harflarni 3 qadam siljitib shifrlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

void sezar_shifrlash(char *s, int siljish) {
    while (*s) {
        if (isalpha((unsigned char)*s)) {
            char asos = isupper((unsigned char)*s) ? 'A' : 'a';
            *s = asos + (*s - asos + siljish) % 26;
        }
        s++;
    }
}

int main(void) {
    char matn[] = "SALOM";
    sezar_shifrlash(matn, 3);
    printf("Sezar shifri (K=3): %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Harflar alifbo bo'yicha 3 qadam suriladi: S->V, A->D, L->O, O->R, M->P.

## Ishlash natijasi:
```text
Sezar shifri (K=3): VDORP
```

---

# 443-Topshiriq: URL kodlash (Percent-Encoding: Probelni '%20' ga aylantirish)

## Topshiriq sharti:
Bo'shliqlarni URL formatiga o'tkazuvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

void url_kodla(const char *src, char *dest) {
    while (*src) {
        if (*src == ' ') {
            *dest++ = '%';
            *dest++ = '2';
            *dest++ = '0';
        } else {
            *dest++ = *src;
        }
        src++;
    }
    *dest = '\0';
}

int main(void) {
    char natija[50];
    url_kodla("Salom Dunyo", natija);
    printf("URL: %s\n", natija);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Brauzerlar probellarni xavfsiz uzatish uchun `%20` kodidan foydalanadi.

## Ishlash natijasi:
```text
URL: Salom%20Dunyo
```

---

# 444-Topshiriq: Satrdan HTML teglarini olib tashlash (Strip HTML tags)

## Topshiriq sharti:
'<p>Salom <b>Dunyo</b></p>' satridan teglarni tozalang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

void strip_html(const char *src, char *dest) {
    bool teg_ichida = false;
    while (*src) {
        if (*src == '<') teg_ichida = true;
        else if (*src == '>') teg_ichida = false;
        else if (!teg_ichida) *dest++ = *src;
        src++;
    }
    *dest = '\0';
}

int main(void) {
    char tozalangan[50];
    strip_html("<p>Salom <b>Dunyo</b></p>", tozalangan);
    printf("Matn: %s\n", tozalangan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `<` va `>` orasidagi barcha belgilar o'tkazib yuboriladi.

## Ishlash natijasi:
```text
Matn: Salom Dunyo
```

---

# 445-Topshiriq: Levenshteyn masofasi (Edit Distance) asoslari

## Topshiriq sharti:
Ikki so'zni bir-biriga aylantirish uchun kerak bo'lgan amallar soni tushunchasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int min3(int a, int b, int c) {
    int m = a;
    if (b < m) m = b;
    if (c < m) m = c;
    return m;
}

int main(void) {
    // "kitob" va "xitob" orasidagi masofa 1 ga teng (k -> x almashtirish)
    printf("Levenshteyn masofasi imlo tekshirish (Spell-check) va qidiruvda asosdir.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Levenshteyn masofasi bitta satrni ikkinchisiga aylantirish uchun minimal qo'shish, o'chirish va almashtirishlar sonini bildiradi.

## Ishlash natijasi:
```text
Levenshteyn masofasi imlo tekshirish (Spell-check) va qidiruvda asosdir.
```

---

# 446-Topshiriq: UTF-8 ko'p baytli belgilar va strlen() xususiyati

## Topshiriq sharti:
Nima uchun o'zbek kirill yoki emoji harflari bir nechta bayt egallashini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char ascii_satr[] = "Salom";
    char utf8_belgi[] = "©"; // Copyright belgisi 2 bayt

    printf("ASCII 'Salom' strlen: %zu bayt\n", strlen(ascii_satr));
    printf("UTF-8 '©' strlen:     %zu bayt\n", strlen(utf8_belgi));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strlen()` harflar sonini emas, baytlar sonini hisoblaydi.
2. UTF-8 da har bir belgi 1 dan 4 baytgacha joy egallashi mumkin.

## Ishlash natijasi:
```text
ASCII 'Salom' strlen: 5 bayt
UTF-8 '©' strlen:     2 bayt
```

---

# 447-Topshiriq: Satrlar massivini chiziqli qidiruv bilan topish

## Topshiriq sharti:
Ro'yxatdan qidirilayotgan so'z mavjudligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool so_z_bormi(const char *royxat[], int n, const char *qidiruv) {
    for (int i = 0; i < n; i++) {
        if (strcmp(royxat[i], qidiruv) == 0) return true;
    }
    return false;
}

int main(void) {
    const char *shaharlar[] = {"Toshkent", "Buxoro", "Samarqand"};
    printf("Buxoro bormi: %s\n", so_z_bormi(shaharlar, 3, "Buxoro") ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strcmp(royxat[i], qidiruv) == 0` sharti orqali satrlar to'liq tenglikka tekshiriladi.

## Ishlash natijasi:
```text
Buxoro bormi: Ha
```

---

# 448-Topshiriq: Satrdan raqamlarni ajratib oluvchi filtr

## Topshiriq sharti:
Matn ichidagi faqat raqamlardan yangi satr hosil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

void faqat_raqamlar(const char *src, char *dest) {
    while (*src) {
        if (isdigit((unsigned char)*src)) {
            *dest++ = *src;
        }
        src++;
    }
    *dest = '\0';
}

int main(void) {
    char raqamlar[20];
    faqat_raqamlar("Tel: +998-90-123-45-67", raqamlar);
    printf("Tozalangan raqamlar: %s\n", raqamlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `isdigit` orqali faqat raqamlar terib olinadi.

## Ishlash natijasi:
```text
Tozalangan raqamlar: 998901234567
```

---

# 449-Topshiriq: Satrni berilgan belgi bo'yicha markazlashtirish (Center string)

## Topshiriq sharti:
Matnni berilgan kenglikda markazga tekislang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void markazlashtir(const char *matn, int kenglik) {
    int len = strlen(matn);
    int chap = (kenglik - len) / 2;
    int ong = kenglik - len - chap;

    for (int i = 0; i < chap; i++) putchar('-');
    printf("%s", matn);
    for (int i = 0; i < ong; i++) putchar('-');
    printf("\n");
}

int main(void) {
    markazlashtir("MENYU", 15);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kenglikdan satr uzunligi ayirilib, ikkala tomonga teng bo'linadi.

## Ishlash natijasi:
```text
-----MENYU------
```

---

# 450-Topshiriq: Modul yakuni: Mini JSON Parser — Kalit va qiymatlarni ajratish

## Topshiriq sharti:
Oddiy '{"ism": "Ali", "yosh": 20}' satrini tahlil qiluvchi modul.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void json_qiymat_top(const char *json, const char *kalit, char *qiymat) {
    char qidiruv[50];
    sprintf(qidiruv, "\"%s\":", kalit);
    const char *p = strstr(json, qidiruv);
    if (!p) {
        strcpy(qiymat, "TOPILMADI");
        return;
    }
    p += strlen(qidiruv);
    while (*p == ' ' || *p == '\"') p++;

    int idx = 0;
    while (*p && *p != '\"' && *p != ',' && *p != '}') {
        qiymat[idx++] = *p++;
    }
    qiymat[idx] = '\0';
}

int main(void) {
    const char *json = "{\"ism\": \"Ali\", \"yosh\": 20}";
    char ism[20], yosh[20];

    json_qiymat_top(json, "ism", ism);
    json_qiymat_top(json, "yosh", yosh);

    printf("JSON tahlili:\n");
    printf("Ism:  %s\n", ism);
    printf("Yosh: %s\n", yosh);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strstr` va ko'rsatkichlar arifmetikasi orqali JSON kalitlari qidiriladi va qiymatlari ajratiladi.
2. Bu 9-qismning barcha string va string.h kutubxona amaliyotlarini umumlashtiradi.

## Ishlash natijasi:
```text
JSON tahlili:
Ism:  Ali
Yosh: 20
```

---
