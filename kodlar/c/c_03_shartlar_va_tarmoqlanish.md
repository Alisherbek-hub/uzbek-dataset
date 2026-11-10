# C Dasturlash Tili — 3-Qism: Shartlar va Tarmoqlanish
## (101-150 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* if, else if, else tarmoqlanishlari va nested shartlar
* Dangling else xavfi va figurali qavslarning zarurati
* switch-case operatori, break roli va Fall-through mexanizmi
* Ternary operatori va uning ifodali qo'llanilishi
* Geometrik, mantiqiy va shaxmat algoritmlari (Pifagor, Kabisa yili, AABB to'qnashuvi)
* Finite State Machine (FSM) holatlar mashinasi arxitekturasi

---

# 101-Topshiriq: Oddiy if sharti: Musbat sonni tekshirish

## Topshiriq sharti:
Berilgan son 0 dan katta bo'lsa, uning musbat ekanligini bildiruvchi if konstruktsiyasini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 42;

    if (son > 0) {
        printf("Son musbat: %d\n", son);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `if` operatori qavs ichidagi shartni baholaydi.
2. Agar shart rost (1 yoki har qanday 0 dan farqli son) bo'lsa, blokdagi kod bajariladi.
3. Aks holda blok tashlab o'tiladi.

## Ishlash natijasi:
```text
Son musbat: 42
```

---

# 102-Topshiriq: if-else sharti: Sonning juft yoki toqligini aniqlash

## Topshiriq sharti:
Sonning juft yoki toq ekanligini if-else konstruktsiyasi orqali aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 15;

    if (son % 2 == 0) {
        printf("%d — Juft son\n", son);
    } else {
        printf("%d — Toq son\n", son);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `if-else` sharti ikkita muqobil yo'ldan birini tanlash imkonini beradi.
2. Shart rost bo'lsa `if` qismi, yolg'on bo'lsa `else` qismi ishlaydi.

## Ishlash natijasi:
```text
15 — Toq son
```

---

# 103-Topshiriq: if-else if-else zanjiri: Sonning ishorasini aniqlash

## Topshiriq sharti:
Sonning musbat, manfiy yoki nol ekanligini uch tarmoqli shart orqali toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = -8;

    if (son > 0) {
        printf("Musbat son\n");
    } else if (son < 0) {
        printf("Manfiy son\n");
    } else {
        printf("Son nolga teng\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `else if` zanjiri bir nechta shartlarni navbat bilan tekshirish imkonini beradi.
2. Birinchi rost chiqqan shart bloki bajariladi va qolgan barcha tarmoqlar o'tkazib yuboriladi.

## Ishlash natijasi:
```text
Manfiy son
```

---

# 104-Topshiriq: Ichma-ich if (Nested if): Yoshi va guvohnomasi borligini tekshirish

## Topshiriq sharti:
Ichma-ich if orqali avtomobil haydash huquqini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    int yosh = 19;
    bool guvohnoma_bor = true;

    if (yosh >= 18) {
        if (guvohnoma_bor) {
            printf("Avtomobil boshqarishingiz mumkin.\n");
        } else {
            printf("Yoshingiz yetadi, ammo haydovchilik guvohnomangiz yo'q!\n");
        }
    } else {
        printf("Yoshingiz 18 ga yetmagan, ruxsat berilmaydi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitta `if` bloki ichida yana boshqa bir `if` joylashtirilishi ichma-ich (nested) shart deyiladi.
2. Tashqi shart rost bo'lgandagina ichki shart tekshiriladi.

## Ishlash natijasi:
```text
Avtomobil boshqarishingiz mumkin.
```

---

# 105-Topshiriq: Shartlarda mantiqiy VA (&&): Harorat qulayligini tekshirish

## Topshiriq sharti:
Harorat 18 dan 25 darajagacha bo'lganda qulay deb hisoblovchi dastur tuzing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int harorat = 22;

    if (harorat >= 18 && harorat <= 25) {
        printf("Harorat xonada qulay: %d daraja.\n", harorat);
    } else {
        printf("Konditsionerni yoqish tavsiya etiladi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `&&` ikkala chegara ham qanoatlantirilishini talab qiladi.
2. Bir vaqtda `harorat >= 18` va `harorat <= 25` rost bo'lishi kerak.

## Ishlash natijasi:
```text
Harorat xonada qulay: 22 daraja.
```

---

# 106-Topshiriq: Shartlarda mantiqiy YOKI (||): Chegirma huquqini tekshirish

## Topshiriq sharti:
Talabalar yoki nafaqaxo'rlar uchun jamoat transportida chegirma borligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    bool talaba = false;
    bool nafaqaxor = true;

    if (talaba || nafaqaxor) {
        printf("Siz uchun 50%% chegirma mavjud!\n");
    } else {
        printf("To'liq tarif bo'yicha to'lov.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `||` operatori shartlardan kamida bittasi rost bo'lsa yetarli deb hisoblaydi.
2. Bu yerda `nafaqaxor` true bo'lgani sababli chegirma taqdim etiladi.

## Ishlash natijasi:
```text
Siz uchun 50% chegirma mavjud!
```

---

# 107-Topshiriq: Dangling else muammosi va figurali qavslar ({}) ning hayotiy zarurati

## Topshiriq sharti:
Figurali qavssiz if-else qanday xato tushunilishi mumkinligini va uni to'g'rilashni ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 10;
    int b = -5;

    // Figurali qavslar bilan yozilgan xavfsiz va aniq kod:
    if (a > 0) {
        if (b > 0) {
            printf("Ikkalasi ham musbat\n");
        } else {
            printf("a musbat, lekin b manfiy yoki nol\n");
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da `else` o'zidan oldingi eng yaqin `if` ga tegishli bo'ladi (Dangling Else qoidasi).
2. Figurali qavs qo'yilmasa, dasturchi tashqi `if` ga tegishli deb o'ylagan `else` aslida ichki `if` ga birikib ketadi va yashirin mantiqiy xatoga olib keladi.
3. Shuning uchun har bir `if` va `else` blokini doimo `{}` ichiga olish qat'iy talab qilinadi.

## Ishlash natijasi:
```text
a musbat, lekin b manfiy yoki nol
```

---

# 108-Topshiriq: Uchta son orasidan eng kattasini topish

## Topshiriq sharti:
Uchta turli butun son orasidan maksimumini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 25, y = 47, z = 33;
    int max;

    if (x >= y && x >= z) {
        max = x;
    } else if (y >= x && y >= z) {
        max = y;
    } else {
        max = z;
    }

    printf("Eng katta son: %d\n", max);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir son boshqa ikki songa nisbatan `&&` orqali taqqoslanadi.
2. Eng katta qiymat `max` o'zgaruvchisiga olinadi.

## Ishlash natijasi:
```text
Eng katta son: 47
```

---

# 109-Topshiriq: To'rtta son orasidan eng kattasini o'zgaruvchi bilan solishtirib topish

## Topshiriq sharti:
To'rtta son orasidan eng kattasini bosqichma-bosqich yangilash usuli bilan toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 12, b = 89, c = 45, d = 67;
    int max = a;

    if (b > max) max = b;
    if (c > max) max = c;
    if (d > max) max = d;

    printf("To'rtta sondan eng kattasi: %d\n", max);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boshlang'ich maksimum sifatida birinchi son olinadi.
2. Keyingi har bir son `max` bilan solishtirilib, kattaroq bo'lsa yangilanadi.
3. Bu usul zanjirli murakkab if-larga qaraganda ancha oson va ixtiyoriy miqdordagi sonlarga kengaytiriladi.

## Ishlash natijasi:
```text
To'rtta sondan eng kattasi: 89
```

---

# 110-Topshiriq: Kabisa yilini (Leap Year) hisoblash logikasi

## Topshiriq sharti:
Yil kabisa yili ekanligini Grigoriy taqvimi qoidasi bo'yicha aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool kabisa_yilimi(int yil) {
    // 400 ga bo'linsa yoki 4 ga bo'linib 100 ga bo'linmasa
    return (yil % 400 == 0) || ((yil % 4 == 0) && (yil % 100 != 0));
}

int main(void) {
    int y1 = 2024;
    int y2 = 1900;
    int y3 = 2000;

    printf("%d kabisami: %s\n", y1, kabisa_yilimi(y1) ? "Ha" : "Yo'q");
    printf("%d kabisami: %s\n", y2, kabisa_yilimi(y2) ? "Ha" : "Yo'q");
    printf("%d kabisami: %s\n", y3, kabisa_yilimi(y3) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qoida: har 4 yilda bir kabisa bo'ladi, lekin 100 ga bo'linadigan yillar kabisa emas, istisno tariqasida 400 ga bo'linadigan yillar yana kabisa hisoblanadi.
2. 2024 — kabisa, 1900 — kabisa emas (chunki 100 ga bo'linadi, 400 ga emas), 2000 — kabisa (400 ga bo'linadi).

## Ishlash natijasi:
```text
2024 kabisami: Ha
1900 kabisami: Yo'q
2000 kabisami: Ha
```

---

# 111-Topshiriq: Uchburchak mavjudlik sharti (Uchburchak tengsizligi)

## Topshiriq sharti:
Berilgan uchta kesmadan uchburchak yasash mumkinligini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 5, b = 7, c = 10;

    if (a + b > c && a + c > b && b + c > a) {
        printf("Tomonlari %d, %d, %d bo'lgan uchburchak mavjud!\n", a, b, c);
    } else {
        printf("Bunday tomonlar bilan uchburchak yasab bo'lmaydi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Uchburchak tengsizligi qoidasi: ixtiyoriy ikki tomon yig'indisi uchinchi tomondan qat'iy katta bo'lishi shart.
2. Barcha 3 ta juftlik `&&` orqali tekshirilishi kerak.

## Ishlash natijasi:
```text
Tomonlari 5, 7, 10 bo'lgan uchburchak mavjud!
```

---

# 112-Topshiriq: Uchburchak turini aniqlash (Teng tomonli, teng yonli, turli tomonli)

## Topshiriq sharti:
Tomonlari berilgan uchburchakning geometrik turini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 6, b = 6, c = 8;

    if (a == b && b == c) {
        printf("Teng tomonli uchburchak (Equilateral)\n");
    } else if (a == b || b == c || a == c) {
        printf("Teng yonli uchburchak (Isosceles)\n");
    } else {
        printf("Turli tomonli uchburchak (Scalene)\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar 3 ta tomoni ham teng bo'lsa — teng tomonli.
2. Agar kamida 2 ta tomoni teng bo'lsa — teng yonli.
3. Barcha tomonlari har xil bo'lsa — turli tomonli.

## Ishlash natijasi:
```text
Teng yonli uchburchak (Isosceles)
```

---

# 113-Topshiriq: To'g'ri burchakli uchburchakni aniqlash (Pifagor teoremasi)

## Topshiriq sharti:
Berilgan tomonlar to'g'ri burchakli uchburchak hosil qilishini tekshiring (a^2 + b^2 == c^2).

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 3, b = 4, c = 5;

    int a2 = a * a, b2 = b * b, c2 = c * c;

    if (a2 + b2 == c2 || a2 + c2 == b2 || b2 + c2 == a2) {
        printf("Uchburchak to'g'ri burchakli (Pifagor uchligi: %d, %d, %d)\n", a, b, c);
    } else {
        printf("To'g'ri burchakli emas.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Pifagor teoremasiga ko'ra katetlar kvadratlari yig'indisi gipotenuza kvadratiga teng.
2. Qaysi tomon gipotenuza ekanligi oldindan ma'lum bo'lmasligi mumkin, shuning uchun barcha kombinatsiyalar `||` orqali tekshiriladi.

## Ishlash natijasi:
```text
Uchburchak to'g'ri burchakli (Pifagor uchligi: 3, 4, 5)
```

---

# 114-Topshiriq: Kvadrat tenglama ildizlarini diskriminant (D = b^2 - 4ac) orqali topish

## Topshiriq sharti:
ax^2 + bx + c = 0 kvadrat tenglamasining ildizlarini aniqlovchi dastur tuzing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    double a = 1.0, b = -5.0, c = 6.0;
    double d = b * b - 4 * a * c;

    printf("Tenglama: %.0lfx^2 + (%.0lf)x + (%.0lf) = 0\n", a, b, c);
    printf("Diskriminant: %.2lf\n", d);

    if (d > 0) {
        double x1 = (-b + sqrt(d)) / (2 * a);
        double x2 = (-b - sqrt(d)) / (2 * a);
        printf("Ikkita haqiqiy ildiz: x1 = %.2lf, x2 = %.2lf\n", x1, x2);
    } else if (d == 0) {
        double x = -b / (2 * a);
        printf("Bitta karrali ildiz: x = %.2lf\n", x);
    } else {
        printf("Haqiqiy ildizlarga ega emas (kompleks ildizlar)\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `d > 0` bo'lsa ikkita turli haqiqiy ildiz.
2. `d == 0` bo'lsa bitta umumiy ildiz.
3. `d < 0` bo'lsa haqiqiy sonlar to'plamida ildiz yo'q.

## Ishlash natijasi:
```text
Tenglama: 1x^2 + (-5)x + (6) = 0
Diskriminant: 1.00
Ikkita haqiqiy ildiz: x1 = 3.00, x2 = 2.00
```

---

# 115-Topshiriq: Belgining turini aniqlash (Katta, kichik harf, raqam yoki maxsus belgi)

## Topshiriq sharti:
Kiritilgan belgining qaysi toifaga kirishini if shartlari orqali aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char ch = 'K';

    if (ch >= 'A' && ch <= 'Z') {
        printf("'%c' — Katta lotin harfi\n", ch);
    } else if (ch >= 'a' && ch <= 'z') {
        printf("'%c' — Kichik lotin harfi\n", ch);
    } else if (ch >= '0' && ch <= '9') {
        printf("'%c' — Raqam\n", ch);
    } else {
        printf("'%c' — Maxsus yoki tinish belgisi\n", ch);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Belgilar ASCII kodi bo'yicha ketma-ket joylashgan.
2. `ch >= 'A' && ch <= 'Z'` orqali katta harflar oraliqda ekanligi oson aniqlanadi.

## Ishlash natijasi:
```text
'K' — Katta lotin harfi
```

---

# 116-Topshiriq: Unli va undosh harflarni tekshirish

## Topshiriq sharti:
Lotin harfining unli yoki undosh ekanligini if bilan aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    char harf = 'E';
    char kichik = tolower(harf);

    if (kichik == 'a' || kichik == 'e' || kichik == 'i' || 
        kichik == 'o' || kichik == 'u') {
        printf("'%c' — Unli harf (Vowel)\n", harf);
    } else {
        printf("'%c' — Undosh harf (Consonant)\n", harf);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Avval harf `tolower` bilan kichik registrga o'tkaziladi.
2. So'ngra 5 ta asosiy lotin unlisi bilan taqqoslanadi.

## Ishlash natijasi:
```text
'E' — Unli harf (Vowel)
```

---

# 117-Topshiriq: Koordinata choragini aniqlash (Dekart koordinatalar tekisligi)

## Topshiriq sharti:
Nuqtaning (X, Y) koordinatalari bo'yicha qaysi chorakda yotishini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = -4, y = 7;

    if (x > 0 && y > 0) {
        printf("(%d, %d) — I chorakda\n", x, y);
    } else if (x < 0 && y > 0) {
        printf("(%d, %d) — II chorakda\n", x, y);
    } else if (x < 0 && y < 0) {
        printf("(%d, %d) — III chorakda\n", x, y);
    } else if (x > 0 && y < 0) {
        printf("(%d, %d) — IV chorakda\n", x, y);
    } else {
        printf("(%d, %d) — Koordinata o'qida yoki markazda\n", x, y);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. X > 0, Y > 0: 1-chorak.
2. X < 0, Y > 0: 2-chorak.
3. X < 0, Y < 0: 3-chorak.
4. X > 0, Y < 0: 4-chorak.

## Ishlash natijasi:
```text
(-4, 7) — II chorakda
```

---

# 118-Topshiriq: Koordinatalar bo'yicha markazga eng yaqin nuqtani topish

## Topshiriq sharti:
Ikki nuqtadan qaysi biri koordinata boshiga (0, 0) yaqinroq ekanligini toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x1 = 3, y1 = 4;   // r1^2 = 9 + 16 = 25
    int x2 = 5, y2 = 1;   // r2^2 = 25 + 1 = 26

    int d1 = x1 * x1 + y1 * y1;
    int d2 = x2 * x2 + y2 * y2;

    if (d1 < d2) {
        printf("1-nuqta (3, 4) yaqinroq (masofa kvadrati: %d)\n", d1);
    } else if (d2 < d1) {
        printf("2-nuqta (5, 1) yaqinroq (masofa kvadrati: %d)\n", d2);
    } else {
        printf("Ikkala nuqta ham teng masofada joylashgan.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Taqqoslash uchun kvadrat ildiz `sqrt` ni hisoblash shart emas; kvadratlarning o'zini solishtirish yetarli va ancha tezroqdir.

## Ishlash natijasi:
```text
1-nuqta (3, 4) yaqinroq (masofa kvadrati: 25)
```

---

# 119-Topshiriq: Talaba baholash tizimi (Akademik reyting shkalasi)

## Topshiriq sharti:
Ballga qarab akademik bahoni chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int ball = 83;

    if (ball >= 90 && ball <= 100) {
        printf("Baho: A (A'lo)\n");
    } else if (ball >= 80 && ball < 90) {
        printf("Baho: B (Yaxshi)\n");
    } else if (ball >= 70 && ball < 80) {
        printf("Baho: C (Qoniqarli)\n");
    } else if (ball >= 60 && ball < 70) {
        printf("Baho: D (Yetarli)\n");
    } else {
        printf("Baho: F (Qoniqarsiz / Yiqildi)\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir oraliq qat'iy chegaralangan.
2. 83 ball B toifasiga to'g'ri keladi.

## Ishlash natijasi:
```text
Baho: B (Yaxshi)
```

---

# 120-Topshiriq: Tabaqalashgan savdo chegirmasini hisoblash

## Topshiriq sharti:
Xarid summasiga qarab 0%, 5%, 10% yoki 15% chegirma hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double xarid = 350000.0; // so'm
    double chegirma_foizi = 0.0;

    if (xarid >= 500000.0) {
        chegirma_foizi = 15.0;
    } else if (xarid >= 300000.0) {
        chegirma_foizi = 10.0;
    } else if (xarid >= 100000.0) {
        chegirma_foizi = 5.0;
    }

    double chegirma_summasi = xarid * (chegirma_foizi / 100.0);
    double yakuniy_narx = xarid - chegirma_summasi;

    printf("Xarid summasi: %.0f so'm\n", xarid);
    printf("Chegirma: %.0f%% (%.0f so'm)\n", chegirma_foizi, chegirma_summasi);
    printf("To'lov: %.0f so'm\n", yakuniy_narx);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kattaroq summadan boshlab tekshirish shartlar ketma-ketligini to'g'ri tashkil etish imkonini beradi.
2. 350,000 so'm uchun 10% chegirma beriladi.

## Ishlash natijasi:
```text
Xarid summasi: 350000 so'm
Chegirma: 10% (35000 so'm)
To'lov: 315000 so'm
```

---

# 121-Topshiriq: Progressiv elektr energiyasi to'lovini hisoblash

## Topshiriq sharti:
Iste'mol kVt*soatiga qarab bosqichma-bosqich oshuvchi tarif hisoblagichini tuzing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int kvt = 280;
    double jami = 0.0;

    // 200 kVt*soatgacha - 450 so'mdan
    // 200 dan oshgani - 900 so'mdan
    if (kvt <= 200) {
        jami = kvt * 450.0;
    } else {
        jami = (200 * 450.0) + ((kvt - 200) * 900.0);
    }

    printf("Iste'mol: %d kVt*soat\n", kvt);
    printf("To'lov summasi: %.0f so'm\n", jami);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Barcha hajmga birdaniga yuqori stavka qo'llanilmaydi, faqat belgilangan limitdan oshgan qismiga oshirilgan narx hisoblanadi (Progressive billing).
2. 200 * 450 = 90,000 so'm + 80 * 900 = 72,000 so'm. Jami: 162,000 so'm.

## Ishlash natijasi:
```text
Iste'mol: 280 kVt*soat
To'lov summasi: 162000 so'm
```

---

# 122-Topshiriq: Daromad solig'i hisobi (Soliq tabaqalari)

## Topshiriq sharti:
Yillik daromadga qarab bosqichli soliq hisoblash logikasini dasturlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double daromad = 60000.0; // $
    double soliq = 0.0;

    if (daromad <= 20000.0) {
        soliq = daromad * 0.10;
    } else if (daromad <= 50000.0) {
        soliq = (20000.0 * 0.10) + ((daromad - 20000.0) * 0.15);
    } else {
        soliq = (20000.0 * 0.10) + (30000.0 * 0.15) + ((daromad - 50000.0) * 0.25);
    }

    printf("Yillik daromad: $%.2lf\n", daromad);
    printf("Hisoblangan soliq: $%.2lf\n", soliq);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1-toifa (20k gacha 10%): $2,000.
2. 2-toifa (20k-50k oralig'idagi 30k ga 15%): $4,500.
3. 3-toifa (50k dan oshgan 10k ga 25%): $2,500. Jami: $9,000.

## Ishlash natijasi:
```text
Yillik daromad: $60000.00
Hisoblangan soliq: $9000.00
```

---

# 123-Topshiriq: BMI (Tana vazni indeksi) kalkulyatori va sog'liq toifasi

## Topshiriq sharti:
Bo'y va vazn asosida BMI hisoblab (BMI = vazn / bo'y^2), toifani aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double vazn = 70.0; // kg
    double boy = 1.75;   // metr
    double bmi = vazn / (boy * boy);

    printf("BMI: %.2lf\n", bmi);

    if (bmi < 18.5) {
        printf("Holat: Vazn yetishmasligi\n");
    } else if (bmi < 25.0) {
        printf("Holat: Me'yoriy (Sog'lom vazn)\n");
    } else if (bmi < 30.0) {
        printf("Holat: Ortiqcha vazn\n");
    } else {
        printf("Holat: Semizlik\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 70 / (1.75 * 1.75) = 22.86.
2. 18.5 va 25.0 oralig'ida bo'lgani uchun me'yoriy sog'lom vazn deb topiladi.

## Ishlash natijasi:
```text
BMI: 22.86
Holat: Me'yoriy (Sog'lom vazn)
```

---

# 124-Topshiriq: 24 soatlik vaqt formatidan 12 soatlik (AM/PM) formatga o'tkazish

## Topshiriq sharti:
Soat ko'rsatkichini 12 soatlik tizimga moslashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int soat24 = 17;
    int minut = 45;

    int soat12;
    char *davr;

    if (soat24 == 0) {
        soat12 = 12;
        davr = "AM";
    } else if (soat24 < 12) {
        soat12 = soat24;
        davr = "AM";
    } else if (soat24 == 12) {
        soat12 = 12;
        davr = "PM";
    } else {
        soat12 = soat24 - 12;
        davr = "PM";
    }

    printf("24-soatlik: %02d:%02d\n", soat24, minut);
    printf("12-soatlik: %02d:%02d %s\n", soat12, minut, davr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 17 soat 12 dan ayirilsa 5 bo'ladi va davr 'PM' deb belgilanadi.

## Ishlash natijasi:
```text
24-soatlik: 17:45
12-soatlik: 05:45 PM
```

---

# 125-Topshiriq: Sana to'g'riligini tekshirish (Kun, oy, yil va oydagi kunlar soni)

## Topshiriq sharti:
Kiritilgan sananing taqvimda rostdan ham mavjudligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool sana_togrimi(int kun, int oy, int yil) {
    if (yil < 1 || oy < 1 || oy > 12 || kun < 1) return false;

    int max_kun = 31;
    if (oy == 4 || oy == 6 || oy == 9 || oy == 11) {
        max_kun = 30;
    } else if (oy == 2) {
        bool kabisa = (yil % 400 == 0) || (yil % 4 == 0 && yil % 100 != 0);
        max_kun = kabisa ? 29 : 28;
    }

    return (kun <= max_kun);
}

int main(void) {
    int k = 29, o = 2, y = 2024;
    printf("%02d.%02d.%d sanasi to'g'rimi: %s\n", 
           k, o, y, sana_togrimi(k, o, y) ? "Ha" : "Yo'q");

    k = 29; o = 2; y = 2023;
    printf("%02d.%02d.%d sanasi to'g'rimi: %s\n", 
           k, o, y, sana_togrimi(k, o, y) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir oyning maksimal kunlari alohida shart bilan tekshiriladi.
2. Fevral oyi uchun kabisa yili hisobga olinadi (2024-yilda 29 kun bor, 2023-yilda esa yo'q).

## Ishlash natijasi:
```text
29.02.2024 sanasi to'g'rimi: Ha
29.02.2023 sanasi to'g'rimi: Yo'q
```

---

# 126-Topshiriq: Shaxmat mantiqi: Ruh (Rook) yurishi to'g'riligini tekshirish

## Topshiriq sharti:
Ruhning (x1, y1) dan (x2, y2) ga o'tishi qoidaga mosligini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool ruh_yura_oladimi(int x1, int y1, int x2, int y2) {
    // Ruh faqat gorizontal yoki vertikal to'g'ri chiziq bo'ylab yuradi
    return (x1 == x2 && y1 != y2) || (y1 == y2 && x1 != x2);
}

int main(void) {
    printf("(2, 3) dan (2, 7) ga: %s\n", ruh_yura_oladimi(2, 3, 2, 7) ? "Mumkin" : "Mumkin emas");
    printf("(2, 3) dan (5, 6) ga: %s\n", ruh_yura_oladimi(2, 3, 5, 6) ? "Mumkin" : "Mumkin emas");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ruh bir xil qatorda yoki bir xil ustunda yura oladi.
2. Koordinatalardan faqat bittasi o'zgarishi, ikkinchisi esa o'zgarmasdan qolishi kerak.

## Ishlash natijasi:
```text
(2, 3) dan (2, 7) ga: Mumkin
(2, 3) dan (5, 6) ga: Mumkin emas
```

---

# 127-Topshiriq: Shaxmat mantiqi: Fil (Bishop) yurishi to'g'riligini tekshirish

## Topshiriq sharti:
Filning diagonal bo'ylab yurishi to'g'riligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

bool fil_yura_oladimi(int x1, int y1, int x2, int y2) {
    // Diagonalda dx == dy bo'lishi shart
    return (abs(x1 - x2) == abs(y1 - y2)) && (x1 != x2);
}

int main(void) {
    printf("(3, 3) dan (6, 6) ga: %s\n", fil_yura_oladimi(3, 3, 6, 6) ? "Mumkin" : "Mumkin emas");
    printf("(3, 3) dan (3, 5) ga: %s\n", fil_yura_oladimi(3, 3, 3, 5) ? "Mumkin" : "Mumkin emas");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Diagonallar bo'yicha yurishda gorizontal siljish absolut qiymati vertikal siljish absolut qiymatiga teng bo'ladi (`abs(x1 - x2) == abs(y1 - y2)`).

## Ishlash natijasi:
```text
(3, 3) dan (6, 6) ga: Mumkin
(3, 3) dan (3, 5) ga: Mumkin emas
```

---

# 128-Topshiriq: Shaxmat mantiqi: Farzin (Queen) yurishi to'g'riligini tekshirish

## Topshiriq sharti:
Farzinning ruh yoki fil kabi yura olish qoidasini birlashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

bool farzin_yura_oladimi(int x1, int y1, int x2, int y2) {
    bool ruh = (x1 == x2 && y1 != y2) || (y1 == y2 && x1 != x2);
    bool fil = (abs(x1 - x2) == abs(y1 - y2)) && (x1 != x2);
    return ruh || fil;
}

int main(void) {
    printf("(4, 4) dan (4, 8) ga: %s\n", farzin_yura_oladimi(4, 4, 4, 8) ? "Mumkin" : "Mumkin emas");
    printf("(4, 4) dan (7, 7) ga: %s\n", farzin_yura_oladimi(4, 4, 7, 7) ? "Mumkin" : "Mumkin emas");
    printf("(4, 4) dan (5, 6) ga: %s\n", farzin_yura_oladimi(4, 4, 5, 6) ? "Mumkin" : "Mumkin emas");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Farzin yurishi bu Ruh va Fil yurishlarining mantiqiy `||` birikmasidir.

## Ishlash natijasi:
```text
(4, 4) dan (4, 8) ga: Mumkin
(4, 4) dan (7, 7) ga: Mumkin
(4, 4) dan (5, 6) ga: Mumkin emas
```

---

# 129-Topshiriq: Shaxmat mantiqi: Ot (Knight) yurishi 'L' shaklidaligini tekshirish

## Topshiriq sharti:
Otning (dx=1, dy=2) yoki (dx=2, dy=1) shaklida yurishini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

bool ot_yura_oladimi(int x1, int y1, int x2, int y2) {
    int dx = abs(x1 - x2);
    int dy = abs(y1 - y2);
    return (dx == 1 && dy == 2) || (dx == 2 && dy == 1);
}

int main(void) {
    printf("(3, 3) dan (4, 5) ga: %s\n", ot_yura_oladimi(3, 3, 4, 5) ? "Mumkin" : "Mumkin emas");
    printf("(3, 3) dan (5, 4) ga: %s\n", ot_yura_oladimi(3, 3, 5, 4) ? "Mumkin" : "Mumkin emas");
    printf("(3, 3) dan (4, 4) ga: %s\n", ot_yura_oladimi(3, 3, 4, 4) ? "Mumkin" : "Mumkin emas");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ot har doim bitta o'q bo'yicha 1 katak, ikkinchi o'q bo'yicha 2 katak siljiydi (`dx * dy == 2`).

## Ishlash natijasi:
```text
(3, 3) dan (4, 5) ga: Mumkin
(3, 3) dan (5, 4) ga: Mumkin
(3, 3) dan (4, 4) ga: Mumkin emas
```

---

# 130-Topshiriq: Shaxmat mantiqi: Shoh (King) yurishi to'g'riligini tekshirish

## Topshiriq sharti:
Shohning ixtiyoriy tomonga faqat 1 katak yura olishini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

bool shoh_yura_oladimi(int x1, int y1, int x2, int y2) {
    int dx = abs(x1 - x2);
    int dy = abs(y1 - y2);
    return (dx <= 1 && dy <= 1) && (dx + dy > 0);
}

int main(void) {
    printf("(4, 4) dan (5, 5) ga: %s\n", shoh_yura_oladimi(4, 4, 5, 5) ? "Mumkin" : "Mumkin emas");
    printf("(4, 4) dan (4, 6) ga: %s\n", shoh_yura_oladimi(4, 4, 4, 6) ? "Mumkin" : "Mumkin emas");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shoh qo'shni 8 ta katakdan biriga o'ta oladi (`dx <= 1 && dy <= 1`), lekin o'z o'rnida qolishi mumkin emas (`dx + dy > 0`).

## Ishlash natijasi:
```text
(4, 4) dan (5, 5) ga: Mumkin
(4, 4) dan (4, 6) ga: Mumkin emas
```

---

# 131-Topshiriq: Shaxmat doskasidagi katak rangini (qora yoki oq) aniqlash

## Topshiriq sharti:
Katak koordinatalari (x, y) bo'yicha uning rangi oq yoki qoraligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 1; // A ustuni
    int y = 1; // 1 qatori

    // (x + y) juft bo'lsa qora, toq bo'lsa oq (yoki aksincha)
    if ((x + y) % 2 == 0) {
        printf("Katak (%d, %d) — Qora rangda\n", x, y);
    } else {
        printf("Katak (%d, %d) — Oq rangda\n", x, y);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shaxmat doskasida har ikkala yo'nalishda ranglar almashinib boradi.
2. `(x + y)` yig'indisining juft yoki toqligi katak rangini bir zumda aniqlaydi.

## Ishlash natijasi:
```text
Katak (1, 1) — Qora rangda
```

---

# 132-Topshiriq: switch-case operatori asoslari: Hafta kuni nomi

## Topshiriq sharti:
Hafta kuni raqamiga qarab uning nomini switch-case orqali chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int kun = 3;

    switch (kun) {
        case 1: printf("Dushanba\n"); break;
        case 2: printf("Seshanba\n"); break;
        case 3: printf("Chorshanba\n"); break;
        case 4: printf("Payshanba\n"); break;
        case 5: printf("Juma\n"); break;
        case 6: printf("Shanba\n"); break;
        case 7: printf("Yakshanba\n"); break;
        default: printf("Noto'g'ri hafta kuni raqami!\n"); break;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `switch` operatori butun sonli ifodani baholaydi va mos `case` belgisiga sakraydi.
2. `break` blokdan darhol chiqishni ta'minlaydi.

## Ishlash natijasi:
```text
Chorshanba
```

---

# 133-Topshiriq: switch-case da break operatorining o'rni va uning yo'qligi oqibati

## Topshiriq sharti:
break qo'yilmaganda keyingi barcha case'lar ketma-ket bajarilib ketishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int bosqich = 2;

    printf("break siz switch:\n");
    switch (bosqich) {
        case 1: printf("1-bosqich bajarildi\n");
        case 2: printf("2-bosqich bajarildi\n");
        case 3: printf("3-bosqich bajarildi\n");
        default: printf("Yakunlandi\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida `switch` avtomatik to'xtamaydi: agar `break` bo'lmasa, mos case dan boshlab barcha keyingi case'lar ijro qilinadi.
2. Bu xususiyat 'Fall-through' deb ataladi.

## Ishlash natijasi:
```text
break siz switch:
2-bosqich bajarildi
3-bosqich bajarildi
Yakunlandi
```

---

# 134-Topshiriq: switch-case Fall-through hodisasidan maqsadli foydalanish: Oydagi kunlar soni

## Topshiriq sharti:
Bir nechta oylarni bitta guruhga birlashtirib, kunlar sonini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int oy = 4; // Aprel

    switch (oy) {
        case 1: case 3: case 5: case 7: case 8: case 10: case 12:
            printf("Bu oyda 31 kun bor.\n");
            break;
        case 4: case 6: case 9: case 11:
            printf("Bu oyda 30 kun bor.\n");
            break;
        case 2:
            printf("Bu oyda 28 yoki 29 kun bor.\n");
            break;
        default:
            printf("Bunday oy yo'q!\n");
            break;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `case 4: case 6: case 9: case 11:` ketma-ket yozilganda, ularning barchasi bir xil kod blokini bajaradi.
2. Bu Fall-through ning eng mashhur va foydali qo'llanilishidir.

## Ishlash natijasi:
```text
Bu oyda 30 kun bor.
```

---

# 135-Topshiriq: switch-case da char (belgilar) bilan ishlash

## Topshiriq sharti:
Tugmachalar boshqaruvi (W, A, S, D) bo'yicha harakat yo'nalishini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char buyruq = 'W';

    switch (buyruq) {
        case 'W': case 'w':
            printf("Oldinga harakatlanish\n");
            break;
        case 'S': case 's':
            printf("Orqaga harakatlanish\n");
            break;
        case 'A': case 'a':
            printf("Chapga burilish\n");
            break;
        case 'D': case 'd':
            printf("O'ngga burilish\n");
            break;
        default:
            printf("Noma'lum buyruq!\n");
            break;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `char` turi aslida 1 baytli butun son bo'lgani uchun uni `switch` da to'liq ishlatish mumkin.
2. Katta va kichik harflar Fall-through orqali birlashtiriladi.

## Ishlash natijasi:
```text
Oldinga harakatlanish
```

---

# 136-Topshiriq: switch-case da default bo'limi va kutilmagan kirishlarni filtrlash

## Topshiriq sharti:
Tarmoq protokoli status kodini switch orqali tahlil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int http_kod = 404;

    switch (http_kod) {
        case 200: printf("200 OK — So'rov muvaffaqiyatli\n"); break;
        case 301: printf("301 Moved Permanently\n"); break;
        case 400: printf("400 Bad Request\n"); break;
        case 404: printf("404 Not Found — Sahifa topilmadi\n"); break;
        case 500: printf("500 Internal Server Error\n"); break;
        default:  printf("Noma'lum HTTP status kodi: %d\n", http_kod); break;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `default` bo'limi hech qaysi `case` ga mos kelmagan barcha holatlarni qamrab oladi.
2. U xavfsizlik va xatoliklarni ro'yxatga olish uchun muhimdir.

## Ishlash natijasi:
```text
404 Not Found — Sahifa topilmadi
```

---

# 137-Topshiriq: switch-case orqali oddiy kalkulyator (+, -, *, /) yasash

## Topshiriq sharti:
Amal belgisi bo'yicha arifmetik hisob bajaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char amal = '*';
    double a = 12.0, b = 4.0;
    double natija;

    switch (amal) {
        case '+': natija = a + b; printf("%.1lf + %.1lf = %.1lf\n", a, b, natija); break;
        case '-': natija = a - b; printf("%.1lf - %.1lf = %.1lf\n", a, b, natija); break;
        case '*': natija = a * b; printf("%.1lf * %.1lf = %.1lf\n", a, b, natija); break;
        case '/': 
            if (b != 0) printf("%.1lf / %.1lf = %.1lf\n", a, b, a / b);
            else printf("Xatolik: Nolga bo'lish mumkin emas!\n");
            break;
        default: printf("Noto'g'ri amal belgisi!\n"); break;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Belgili operator switch orqali tahlil qilinadi.
2. Bo'lish amali ichida nolga bo'lish xavfi qo'shimcha `if` bilan himoyalanadi.

## Ishlash natijasi:
```text
12.0 * 4.0 = 48.0
```

---

# 138-Topshiriq: Nima uchun switch-case da float yoki satr ishlatib bo'lmaydi?

## Topshiriq sharti:
switch faqat integral tiplar bilan ishlashi sababini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // switch (3.14) { ... } -> KOMPILYATSIYA XATOSI!
    // float va stringlar C da switch case ga qo'yilmaydi!
    // Buning o'rniga if-else if zanjiri ishlatiladi:
    
    double harorat = 36.6;

    if (harorat == 36.6) {
        printf("Normal tana harorati: %.1lf C\n", harorat);
    } else {
        printf("Boshqa harorat\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyator `switch-case` ni samarali sakrash jadvali (Jump Table) ga aylantiradi.
2. Jump Table faqat diskret butun sonli indekslar bilan ishlay oladi.
3. Haqiqiy sonlar (float) va satrlar diskret butun son bo'lmagani uchun C standarti ularni switch ga kiritishni man etadi.

## Ishlash natijasi:
```text
Normal tana harorati: 36.6 C
```

---

# 139-Topshiriq: switch-case bilan konsol menyusi (Menu-driven interface)

## Topshiriq sharti:
Foydalanuvchi tanlagan menyu bandini qayta ishlovchi dastur karkasi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int tanlov = 2; // Simulyatsiya qilingan foydalanuvchi tanlovi

    printf("--- BOSH MENYU ---\n");
    printf("1. Yangi fayl yaratish\n");
    printf("2. Faylni ochish\n");
    printf("3. Chiqish\n");

    switch (tanlov) {
        case 1: printf("-> Yangi fayl yaratish rejimi tanlandi.\n"); break;
        case 2: printf("-> Faylni ochish rejimi tanlandi.\n"); break;
        case 3: printf("-> Dasturdan chiqildi.\n"); break;
        default: printf("-> Noto'g'ri tanlov!\n"); break;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Konsol ilovalarida menyu tuzish uchun switch eng toza va o'qilishi oson tuzilmadir.

## Ishlash natijasi:
```text
--- BOSH MENYU ---
1. Yangi fayl yaratish
2. Faylni ochish
3. Chiqish
-> Faylni ochish rejimi tanlandi.
```

---

# 140-Topshiriq: switch-case ichida yangi lokal o'zgaruvchi e'lon qilish va blok {} zarurati

## Topshiriq sharti:
Case ichida o'zgaruvchi e'lon qilishda figurali qavslar nima uchun talab qilinishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int rejim = 1;

    switch (rejim) {
        case 1: {
            // Blok ichida lokal o'zgaruvchi e'lon qilish mumkin!
            int x = 100;
            printf("Rejim 1: x = %d\n", x);
            break;
        }
        case 2: {
            int y = 200;
            printf("Rejim 2: y = %d\n", y);
            break;
        }
        default:
            printf("Standart rejim\n");
            break;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar `case 1:` dan so'ng darhol `int x = 100;` deb qavssiz yozilsa, C kompilyatori 'crosses initialization' xatosini beradi.
2. Sababi: `case` lar oddiy nishon (label) bo'lib, o'zgaruvchining ko'rinish sohasi (scope) butun switch bo'ylab tarqalishi mumkin.
3. Figurali qavslar `{}` orqali o'zgaruvchi faqat o'sha `case` bloki ichida chegaralanadi.

## Ishlash natijasi:
```text
Rejim 1: x = 100
```

---

# 141-Topshiriq: Ternary operator: Sonning absolut qiymatini topish

## Topshiriq sharti:
Ternary operatori yordamida bitta qatorda modul hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = -25;
    int abs_qiymat = (son < 0) ? -son : son;

    printf("Son: %d, Absolut qiymati: %d\n", son, abs_qiymat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `(son < 0) ? -son : son` sharti `if-else` ga qaraganda ancha qisqa va toza yoziladi.

## Ishlash natijasi:
```text
Son: -25, Absolut qiymati: 25
```

---

# 142-Topshiriq: Ternary operator: Uchta sonning minimumini bitta qatorda topish

## Topshiriq sharti:
Ichma-ich ternary orqali a, b va c sonlarining minimumini toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 18, b = 7, c = 12;
    int min = (a < b) ? ((a < c) ? a : c) : ((b < c) ? b : c);

    printf("Minimum: %d\n", min);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ichma-ich ternary operatori orqali uchta son minimumi bitta ifodada aniqlanadi.

## Ishlash natijasi:
```text
Minimum: 7
```

---

# 143-Topshiriq: Ternary operator orqali satr tanlash va printf ga to'g'ridan-to'g'ri uzatish

## Topshiriq sharti:
printf chaqiruvi ichida ternary bilan so'z tanlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int ball = 75;
    printf("Natija: Siz imtihondan %s!\n", (ball >= 60) ? "o'tdingiz" : "yiqildingiz");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ternary operator qiymat qaytargani sababli uni to'g'ridan-to'g'ri funksiya argumenti sifatida `%s` ga uzatish mumkin.

## Ishlash natijasi:
```text
Natija: Siz imtihondan o'tdingiz!
```

---

# 144-Topshiriq: Bankomat (ATM) simulyatsiyasi: Balans, yechish va limit tekshiruvi

## Topshiriq sharti:
Mablag' yetarliligi va kunlik limitni if-else orqali tekshiruvchi kassa moduli.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double balans = 1500000.0; // so'm
    double yechish_summasi = 500000.0;
    double kunlik_limit = 1000000.0;

    if (yechish_summasi > kunlik_limit) {
        printf("XATO: Yechish summasi kunlik limitdan (%.0f so'm) oshib ketdi!\n", kunlik_limit);
    } else if (yechish_summasi > balans) {
        printf("XATO: Hisobingizda yetarli mablag' mavjud emas!\n");
    } else {
        balans -= yechish_summasi;
        printf("Muvaffaqiyatli yechildi: %.0f so'm\n", yechish_summasi);
        printf("Qolgan balans: %.0f so'm\n", balans);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shartlar tartibi: avval eng qat'iy cheklov (kunlik limit), so'ngra hisob balansi tekshiriladi.

## Ishlash natijasi:
```text
Muvaffaqiyatli yechildi: 500000 so'm
Qolgan balans: 1000000 so'm
```

---

# 145-Topshiriq: Parol mustahkamligini tekshirish (Uzunlik, katta harf, raqam)

## Topshiriq sharti:
Parolning xavfsizlik talablariga javob berishini shartlar bilan baholang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

int main(void) {
    char parol[] = "Kripto2026";
    size_t uzunlik = strlen(parol);
    bool katta_harf_bor = false;
    bool raqam_bor = false;

    for (size_t i = 0; i < uzunlik; i++) {
        if (isupper((unsigned char)parol[i])) katta_harf_bor = true;
        if (isdigit((unsigned char)parol[i])) raqam_bor = true;
    }

    if (uzunlik >= 8 && katta_harf_bor && raqam_bor) {
        printf("Parol mustahkam va qabul qilindi!\n");
    } else {
        printf("Parol talablarga javob bermaydi (kamida 8 belgi, 1 ta katta harf va 1 ta raqam kerak).\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mantiqiy bayroqlar orqali har bir mezon tekshirilib, yakuniy `if` da `&&` bilan xulosa qilinadi.

## Ishlash natijasi:
```text
Parol mustahkam va qabul qilindi!
```

---

# 146-Topshiriq: Pointer xavfsizligi: Qisqa tutashuv bilan NULL tekshiruvi

## Topshiriq sharti:
ptr != NULL va *ptr qiymatini bitta if da xavfsiz tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int qiymat = 50;
    int *ptr1 = &qiymat;
    int *ptr2 = NULL;

    // ptr1 tekshiruvi:
    if (ptr1 != NULL && *ptr1 > 0) {
        printf("ptr1 ko'rsatgan qiymat musbat: %d\n", *ptr1);
    }

    // ptr2 tekshiruvi (Segment fault bermaydi!):
    if (ptr2 != NULL && *ptr2 > 0) {
        printf("Bu qator ishlamaydi\n");
    } else {
        printf("ptr2 xavfsiz tekshirildi: NULL ko'rsatkich aniqlandi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar birinchi shart `ptr2 != NULL` yolg'on bo'lsa, ikkinchi `*ptr2 > 0` qismi hisoblanmaydi.
2. Bu NULL pointerni dereference qilib tizim halokatiga (Segmentation Fault) uchrashdan asraydi.

## Ishlash natijasi:
```text
ptr1 ko'rsatgan qiymat musbat: 50
ptr2 xavfsiz tekshirildi: NULL ko'rsatkich aniqlandi.
```

---

# 147-Topshiriq: Doira ichida nuqtaning yotishini tekshirish (R^2 masofa sharti)

## Topshiriq sharti:
Nuqta (x, y) markazi (cx, cy) va radiusi R bo'lgan doira ichidami?

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int cx = 0, cy = 0, r = 5;
    int x = 3, y = 4;

    int dx = x - cx;
    int dy = y - cy;
    int masofa_kvadrati = dx * dx + dy * dy;

    if (masofa_kvadrati <= r * r) {
        printf("Nuqta (%d, %d) radiusi %d bo'lgan doira ichida yoki chegarasida!\n", x, y, r);
    } else {
        printf("Nuqta doira tashqarisida.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matematik shart: `(x - cx)^2 + (y - cy)^2 <= r^2`.
2. Masofa kvadrati 3^2 + 4^2 = 25, radius kvadrati 5^2 = 25. Teng bo'lgani uchun doira chegarasida yotadi.

## Ishlash natijasi:
```text
Nuqta (3, 4) radiusi 5 bo'lgan doira ichida yoki chegarasida!
```

---

# 148-Topshiriq: O'yin dasturlash: To'rtburchaklar to'qnashuvi (AABB Collision Detection)

## Topshiriq sharti:
Ikki to'rtburchak o'zaro kesishganini shartlar orqali aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int x, y, w, h;
} Tortburchak;

bool toqnashuv_bormi(Tortburchak a, Tortburchak b) {
    // Agar biri ikkinchisining butunlay chapida, o'ngida, tepasida yoki pastida bo'lmasa, to'qnashuv bor
    if (a.x + a.w < b.x || b.x + b.w < a.x ||
        a.y + a.h < b.y || b.y + b.h < a.y) {
        return false;
    }
    return true;
}

int main(void) {
    Tortburchak r1 = {10, 10, 50, 50};
    Tortburchak r2 = {30, 30, 40, 40};
    Tortburchak r3 = {100, 100, 20, 20};

    printf("r1 va r2 to'qnashdimi: %s\n", toqnashuv_bormi(r1, r2) ? "Ha" : "Yo'q");
    printf("r1 va r3 to'qnashdimi: %s\n", toqnashuv_bormi(r1, r3) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Axis-Aligned Bounding Box (AABB) 2D o'yin dvigatellarida eng ko'p ishlatiladigan to'qnashuv algoritmidir.
2. Shart orqali to'rtburchaklar bir-birini qoplaganligi tekshiriladi.

## Ishlash natijasi:
```text
r1 va r2 to'qnashdimi: Ha
r1 va r3 to'qnashdimi: Yo'q
```

---

# 149-Topshiriq: Harorat bo'yicha moddiy holatni (Qattiq, Suyuq, Gaz) aniqlash

## Topshiriq sharti:
Suvning haroratiga qarab uning agregat holatini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double t = 105.5;

    if (t <= 0.0) {
        printf("Harorat: %.1lf C — Muz (Qattiq holat)\n", t);
    } else if (t < 100.0) {
        printf("Harorat: %.1lf C — Suv (Suyuq holat)\n", t);
    } else {
        printf("Harorat: %.1lf C — Bug' (Gaz holat)\n", t);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Suvning erish (0 C) va qaynash (100 C) nuqtalari bo'yicha agregat holati aniqlanadi.

## Ishlash natijasi:
```text
Harorat: 105.5 C — Bug' (Gaz holat)
```

---

# 150-Topshiriq: Holatlar mashinasi (Finite State Machine) switch yordamida: Svetofor tizimi

## Topshiriq sharti:
Svetoforning holat almashinuvi (Qizil -> Sariq -> Yashil) mantig'ini modellashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef enum {
    QIZIL,
    SARIQ,
    YASHIL
} SvetoforHolati;

int main(void) {
    SvetoforHolati joriy = QIZIL;

    for (int qadam = 1; qadam <= 3; qadam++) {
        switch (joriy) {
            case QIZIL:
                printf("%d-qadam: QIZIL chiroq — To'xtang! Keyingisi SARIQ.\n", qadam);
                joriy = SARIQ;
                break;
            case SARIQ:
                printf("%d-qadam: SARIQ chiroq — Tayyorlaning! Keyingisi YASHIL.\n", qadam);
                joriy = YASHIL;
                break;
            case YASHIL:
                printf("%d-qadam: YASHIL chiroq — Harakatlaning! Keyingisi QIZIL.\n", qadam);
                joriy = QIZIL;
                break;
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Finite State Machine (FSM) — dastur qat'iy belgilangan holatlarda bo'lishi va kirish signallari bo'yicha bir holatdan ikkinchisiga o'tishini boshqaradi.
2. `switch-case` konstruksiyasi FSM larni yaratishda sanoat standartidir.
3. Bu topshiriq 3-qismning barcha shart va tarmoqlanish mavzularini birlashtiradi.

## Ishlash natijasi:
```text
1-qadam: QIZIL chiroq — To'xtang! Keyingisi SARIQ.
2-qadam: SARIQ chiroq — Tayyorlaning! Keyingisi YASHIL.
3-qadam: YASHIL chiroq — Harakatlaning! Keyingisi QIZIL.
```

---
