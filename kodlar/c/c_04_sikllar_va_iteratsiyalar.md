# C Dasturlash Tili — 4-Qism: Sikllar va Iteratsiyalar
## (151-200 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* for, while va do-while sikllarining to'liq tahlili
* break, continue, goto va cleanup arxitekturasi
* Piramidalar, Floyd va Paskal uchburchaklari, yulduzchalar grafikasi
* Tub sonlar, Eratosfen g'alviri, Evklid EKUB/EKUK algoritmlari
* Tezkor daraja (Binary Exponentiation), Nyuton ildiz va Teylor qatorlari
* Loop Invariant Motion, Loop Unrolling va Kollats zanjiri

---

# 151-Topshiriq: Oddiy for sikli: 1 dan 10 gacha sonlarni chop etish

## Topshiriq sharti:
for sikli yordamida 1 dan 10 gacha bo'lgan sonlarni bitta qatorda chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 10; i++) {
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `for (init; condition; step)` uchta qismdan iborat:
   - `int i = 1` — boshlang'ich qiymat (faqat 1 marta bajariladi).
   - `i <= 10` — davom etish sharti (har bir iteratsiya oldidan tekshiriladi).
   - `i++` — har bir iteratsiya yakunida hisoblagichni oshirish.
2. Shart yolg'on bo'lganda sikl to'xtaydi.

## Ishlash natijasi:
```text
1 2 3 4 5 6 7 8 9 10
```

---

# 152-Topshiriq: Kamayish tartibidagi for sikli: 10 dan 1 gacha teskari sanash

## Topshiriq sharti:
Teskari sanash for siklini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    for (int i = 10; i >= 1; i--) {
        printf("%d ", i);
    }
    printf("\nStart!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boshlang'ich qiymat 10, shart `i >= 1` va har qadamda `i--` dekrement qilinadi.

## Ishlash natijasi:
```text
10 9 8 7 6 5 4 3 2 1 
Start!
```

---

# 153-Topshiriq: Qadami 2 ga teng bo'lgan for sikli: Juft sonlarni chop etish

## Topshiriq sharti:
2 dan 20 gacha bo'lgan juft sonlarni qadami 2 bo'lgan sikl bilan chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    for (int i = 2; i <= 20; i += 2) {
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sikl qadami faqat `i++` bo'lishi shart emas; `i += 2`, `i *= 2` kabi ixtiyoriy amal bo'lishi mumkin.
2. Bu ortiqcha `if (i % 2 == 0)` tekshiruvlarisiz to'g'ridan-to'g'ri faqat juft sonlarni aylanish imkonini beradi.

## Ishlash natijasi:
```text
2 4 6 8 10 12 14 16 18 20
```

---

# 154-Topshiriq: 1 dan N gacha bo'lgan sonlar yig'indisi va arifmetik progressiya

## Topshiriq sharti:
1 dan 100 gacha sonlar yig'indisini sikl orqali hisoblang va Gauss formulasi bilan solishtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int n = 100;
    long long yigindi = 0;

    for (int i = 1; i <= n; i++) {
        yigindi += i;
    }

    long long formula_bilan = (long long)n * (n + 1) / 2;

    printf("Sikl orqali yig'indi: %lld\n", yigindi);
    printf("Gauss formulasi bilan: %lld\n", formula_bilan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir iteratsiyada `yigindi` ga `i` qo'shib boriladi.
2. Gauss formulasi `n*(n+1)/2` natijani O(1) vaqtda beradi va sikl natijasining to'g'riligini tasdiqlaydi.

## Ishlash natijasi:
```text
Sikl orqali yig'indi: 5050
Gauss formulasi bilan: 5050
```

---

# 155-Topshiriq: Sonning faktorialini for sikli orqali hisoblash

## Topshiriq sharti:
N! faktorialni sikl orqali toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int n = 6;
    long long faktorial = 1;

    for (int i = 1; i <= n; i++) {
        faktorial *= i;
    }

    printf("%d! = %lld\n", n, faktorial);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Faktorial ko'paytma bo'lgani uchun boshlang'ich qiymat `1` bo'lishi shart (0 emas).
2. 1 * 2 * 3 * 4 * 5 * 6 = 720.

## Ishlash natijasi:
```text
6! = 720
```

---

# 156-Topshiriq: for siklida bir nechta o'zgaruvchilarni birgalikda boshqarish

## Topshiriq sharti:
Bitta siklda i ni oshirib, j ni kamaytirib boring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    for (int i = 0, j = 10; i <= j; i++, j--) {
        printf("i = %d, j = %d\n", i, j);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Vergul operatori orqali `for` boshida bir nechta o'zgaruvchini e'lon qilish va qadam qismida ikkalasini o'zgartirish mumkin.
2. Bu ikki ko'rsatkichli algoritmlarda (Two Pointers) keng qo'llaniladi.

## Ishlash natijasi:
```text
i = 0, j = 10
i = 1, j = 9
i = 2, j = 8
i = 3, j = 7
i = 4, j = 6
i = 5, j = 5
```

---

# 157-Topshiriq: Cheksiz for (;;) sikli va ichidan break bilan chiqish

## Topshiriq sharti:
Cheksiz sikldan shart bajarilganda break orqali chiqishni ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int qadam = 1;

    for (;;) {
        printf("Qadam: %d\n", qadam);
        if (qadam >= 4) {
            printf("To'xtash sharti bajarildi, break qilindi.\n");
            break;
        }
        qadam++;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `for (;;)` sintaksisi C tilida cheksiz siklni ifodalashning standart usulidir.
2. Sikl tanasida `break` operatori bajarilganda sikl darhol yakunlanadi.

## Ishlash natijasi:
```text
Qadam: 1
Qadam: 2
Qadam: 3
Qadam: 4
To'xtash sharti bajarildi, break qilindi.
```

---

# 158-Topshiriq: while sikli asoslari: Shart bajarilgunicha takrorlash

## Topshiriq sharti:
Sonni 1 ga teng bo'lgunicha 2 ga bo'lib borish sikli.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 64;
    int bolish_soni = 0;

    while (son > 1) {
        son /= 2;
        bolish_soni++;
    }

    printf("64 soni 1 ga yetishi uchun %d marta 2 ga bo'lindi.\n", bolish_soni);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `while` sikli iteratsiyalar soni oldindan aniq bo'lmagan, lekin to'xtash sharti ma'lum bo'lgan hollarda qulaydir.
2. Kirishdan oldin shart tekshiriladi; agar dastlabdayoq shart yolg'on bo'lsa, sikl tanasi biror marta ham bajarilmaydi.

## Ishlash natijasi:
```text
64 soni 1 ga yetishi uchun 6 marta 2 ga bo'lindi.
```

---

# 159-Topshiriq: while orqali sonning raqamlari sonini aniqlash

## Topshiriq sharti:
Sonni har qadamda 10 ga bo'lib, uning necha xonali ekanligini toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    long long son = 9876543210LL;
    long long vaqtinchalik = son;
    int xonalar = 0;

    if (vaqtinchalik == 0) {
        xonalar = 1;
    } else {
        while (vaqtinchalik > 0) {
            vaqtinchalik /= 10;
            xonalar++;
        }
    }

    printf("%lld soni %d xonali.\n", son, xonalar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Butun son 10 ga bo'linganda uning oxirgi raqami tushib qoladi.
2. Har bir bo'linish bitta raqam mavjudligini bildiradi.

## Ishlash natijasi:
```text
9876543210 soni 10 xonali.
```

---

# 160-Topshiriq: while orqali sonning raqamlari yig'indisini hisoblash

## Topshiriq sharti:
Sonning barcha raqamlari yig'indisini toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 4567;
    int n = son;
    int yigindi = 0;

    while (n > 0) {
        int oxirgi_raqam = n % 10;
        yigindi += oxirgi_raqam;
        n /= 10;
    }

    printf("%d sonining raqamlari yig'indisi: %d\n", son, yigindi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `n % 10` oxirgi raqamni ajratib beradi.
2. `n /= 10` raqamni o'chiradi.
3. 4 + 5 + 6 + 7 = 22.

## Ishlash natijasi:
```text
4567 sonining raqamlari yig'indisi: 22
```

---

# 161-Topshiriq: Sonni teskarisiga o'girish (Reversing a number)

## Topshiriq sharti:
Butun sonning raqamlarini teskari tartibda joylashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 12345;
    int n = son;
    int teskari = 0;

    while (n > 0) {
        int r = n % 10;
        teskari = teskari * 10 + r;
        n /= 10;
    }

    printf("Asl son: %d, Teskari son: %d\n", son, teskari);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yangi son hosil qilish formulasi: `teskari = teskari * 10 + r`.
2. Har bir qadamda oldingi qiymat chapga bitta xona siljitiladi va yangi raqam qo'shiladi.

## Ishlash natijasi:
```text
Asl son: 12345, Teskari son: 54321
```

---

# 162-Topshiriq: Sonning palindrom ekanligini aniqlash

## Topshiriq sharti:
Son o'ngdan ham, chapdan ham bir xil o'qilishini (palindrom) tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool palindrommi(int son) {
    if (son < 0) return false;
    int asl = son;
    int teskari = 0;
    while (son > 0) {
        teskari = teskari * 10 + (son % 10);
        son /= 10;
    }
    return asl == teskari;
}

int main(void) {
    int a = 12321;
    int b = 12345;

    printf("%d palindrommi: %s\n", a, palindrommi(a) ? "Ha" : "Yo'q");
    printf("%d palindrommi: %s\n", b, palindrommi(b) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sonning teskarisi hisoblanadi va asl son bilan tengligi solishtiriladi.
2. 12321 soni har ikki tomondan bir xil bo'lgani uchun palindromdir.

## Ishlash natijasi:
```text
12321 palindrommi: Ha
12345 palindrommi: Yo'q
```

---

# 163-Topshiriq: do-while sikli: Kamida bir marta bajariluvchi sikl

## Topshiriq sharti:
Shart hatto dastlabdayoq noto'g'ri bo'lsa ham tana 1 marta ishlashini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 100;

    do {
        printf("Bu qator kamida bir marta bajarildi! x = %d\n", x);
    } while (x < 10); // Shart yolg'on!
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `do-while` siklida shart pastda (post-condition) tekshiriladi.
2. Shuning uchun shart qanday bo'lishidan qat'i nazar, tana kamida 1 marta bajarilishi kafolatlanadi.

## Ishlash natijasi:
```text
Bu qator kamida bir marta bajarildi! x = 100
```

---

# 164-Topshiriq: do-while orqali to'g'ri oraliqdagi ma'lumot kiritilishini tekshirish

## Topshiriq sharti:
Foydalanuvchi to'g'ri baho (1 dan 5 gacha) kiritmaguncha so'rash simulyatsiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int baho = 0;
    int urinish = 1;

    do {
        // Simulyatsiya: 2-urinishda to'g'ri qiymat 4 berildi
        if (urinish == 1) baho = 7; // Noto'g'ri
        else baho = 4;              // To'g'ri

        printf("%d-urinish: Kiritilgan baho = %d\n", urinish, baho);
        urinish++;
    } while (baho < 1 || baho > 5);

    printf("To'g'ri baho qabul qilindi: %d\n", baho);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kiritilgan qiymat me'yorda bo'lmasa, sikl yana qayta so'raydi.
2. Bu interaktiv kiritish validatsiyasida do-while ning asosiy ishlatilishidir.

## Ishlash natijasi:
```text
1-urinish: Kiritilgan baho = 7
2-urinish: Kiritilgan baho = 4
To'g'ri baho qabul qilindi: 4
```

---

# 165-Topshiriq: break operatori: Qidirilayotgan son topilganda siklni to'xtatish

## Topshiriq sharti:
Massiv ichidan qiymat qidirib, topilishi bilan siklni to'xtating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int sonlar[] = {14, 25, 33, 42, 58, 69};
    int qidirilayotgan = 42;
    int topilgan_indeks = -1;

    for (int i = 0; i < 6; i++) {
        if (sonlar[i] == qidirilayotgan) {
            topilgan_indeks = i;
            printf("Son %d indeksda topildi! Sikl to'xtatildi.\n", i);
            break; // Qolgan elementlarni ko'rib chiqish shart emas
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `break` siklni muddatidan oldin yakunlaydi.
2. Keraksiz iteratsiyalarning oldi olinib, dastur tezligi tejaladi.

## Ishlash natijasi:
```text
Son 3 indeksda topildi! Sikl to'xtatildi.
```

---

# 166-Topshiriq: continue operatori: Keraksiz iteratsiyani o'tkazib yuborish

## Topshiriq sharti:
1 dan 10 gacha bo'lgan toq sonlarni continue bilan o'tkazib yuborib faqat juftlarini chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 10; i++) {
        if (i % 2 != 0) {
            continue; // Toq son bo'lsa quyidagi qatorlarni bajarmasdan keyingi iteratsiyaga o'tish
        }
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `continue` operatori joriy iteratsiyaning qolgan qismini tashlab o'tadi va siklning keyingi qadamiga sakraydi.
2. `break` dan farqli ravishda siklni butunlay to'xtatmaydi.

## Ishlash natijasi:
```text
2 4 6 8 10
```

---

# 167-Topshiriq: Ichma-ich sikllar: Karra jadvalini chiqarish

## Topshiriq sharti:
Ichma-ich for sikllari orqali 1 dan 5 gacha karra jadvalini chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 5; i++) {
        for (int j = 1; j <= 5; j++) {
            printf("%4d", i * j);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tashqi sikl qatorlarni (`i`), ichki sikl esa har bir qatordagi ustunlarni (`j`) aylantiradi.
2. `%4d` ustunlarni tekislab jadval hosil qiladi.

## Ishlash natijasi:
```text
1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
   4   8  12  16  20
   5  10  15  20  25
```

---

# 168-Topshiriq: Ichma-ich sikllar: Yulduzchalar to'g'ri to'rtburchagi

## Topshiriq sharti:
N qator va M ustundan iborat yulduzchalar to'rini chizing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int qator = 3, ustun = 6;

    for (int i = 0; i < qator; i++) {
        for (int j = 0; j < ustun; j++) {
            printf("* ");
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tashqi sikl har bir yangi qatorni boshlaydi.
2. Ichki sikl o'sha qatordagi barcha yulduzchalarni bitta qatorda chop etadi.

## Ishlash natijasi:
```text
* * * * * * 
* * * * * * 
* * * * * *
```

---

# 169-Topshiriq: Yulduzchalar bilan to'g'ri burchakli uchburchak chizish

## Topshiriq sharti:
Balandligi 5 bo'lgan o'suvchi yulduzchalar uchburchagini chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int n = 5;

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            printf("* ");
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ichki sikl sharti `j <= i` bo'lib, har bir qatordagi yulduzchalar soni qator raqamiga teng bo'ladi.

## Ishlash natijasi:
```text
* 
* * 
* * * 
* * * * 
* * * * *
```

---

# 170-Topshiriq: Yulduzchalar bilan teskari to'g'ri burchakli uchburchak chizish

## Topshiriq sharti:
Balandligi 5 bo'lgan kamayuvchi yulduzchalar uchburchagini chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int n = 5;

    for (int i = n; i >= 1; i--) {
        for (int j = 1; j <= i; j++) {
            printf("* ");
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tashqi sikl 5 dan 1 gacha kamayib boradi, har safar yulduzchalar soni 1 taga qisqaradi.

## Ishlash natijasi:
```text
* * * * * 
* * * * 
* * * 
* * 
*
```

---

# 171-Topshiriq: Yulduzchalar bilan teng yonli piramida chizish

## Topshiriq sharti:
Bo'shliqlar va yulduzchalar mutanosibligi bilan markazlashgan piramida chizing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int n = 4;

    for (int i = 1; i <= n; i++) {
        // Bo'sh joylar: n - i ta
        for (int b = 1; b <= n - i; b++) {
            printf(" ");
        }
        // Yulduzchalar: 2*i - 1 ta
        for (int y = 1; y <= 2 * i - 1; y++) {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir qatorda `n - i` ta probel va `2*i - 1` ta yulduzcha chiqadi.
2. Bu shakllarni simmetrik markazlashtirish formulasidir.

## Ishlash natijasi:
```text
*
  ***
 *****
*******
```

---

# 172-Topshiriq: Yulduzchalar bilan romb (Diamond) shaklini chizish

## Topshiriq sharti:
Yuqori va pastki piramidalar yordamida to'liq romb hosil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int n = 3;

    // Yuqori qism
    for (int i = 1; i <= n; i++) {
        for (int b = 1; b <= n - i; b++) printf(" ");
        for (int y = 1; y <= 2 * i - 1; y++) printf("*");
        printf("\n");
    }
    // Quyi qism
    for (int i = n - 1; i >= 1; i--) {
        for (int b = 1; b <= n - i; b++) printf(" ");
        for (int y = 1; y <= 2 * i - 1; y++) printf("*");
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Romb ikkita teskari simmetrik sikldan tashkil topadi.

## Ishlash natijasi:
```text
*
 ***
*****
 ***
  *
```

---

# 173-Topshiriq: Sonli piramida: Floyd uchburchagi

## Topshiriq sharti:
Ketma-ket sonlar bilan to'ldirilgan Floyd uchburchagini chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int qator = 4;
    int son = 1;

    for (int i = 1; i <= qator; i++) {
        for (int j = 1; j <= i; j++) {
            printf("%-3d ", son++);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `son` o'zgaruvchisi har bir chop etilishda 1 ga oshadi va keyingi qatorga o'tishda ham davom etadi.

## Ishlash natijasi:
```text
1   
2   3   
4   5   6   
7   8   9   10
```

---

# 174-Topshiriq: Paskal uchburchagini sikllar orqali chiqarish

## Topshiriq sharti:
Binomial koeffitsientlar asosida Paskal uchburchagini hosil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int qator = 5;

    for (int i = 0; i < qator; i++) {
        int qiymat = 1;
        for (int b = 0; b < qator - i - 1; b++) printf("  ");
        for (int j = 0; j <= i; j++) {
            printf("%4d", qiymat);
            qiymat = qiymat * (i - j) / (j + 1);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Paskal uchburchagidagi har bir had oldingisidan `qiymat * (i - j) / (j + 1)` formulasi orqali topiladi.

## Ishlash natijasi:
```text
1
        1   1
      1   2   1
    1   3   3   1
  1   4   6   4   1
```

---

# 175-Topshiriq: Fibonachchi ketma-ketligining dastlabki N ta hadini sikl bilan hisoblash

## Topshiriq sharti:
0, 1, 1, 2, 3, 5, 8... ketma-ketligining 8 ta hadini chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int n = 8;
    long long f0 = 0, f1 = 1;

    printf("Fibonachchi (%d ta): ", n);
    for (int i = 0; i < n; i++) {
        printf("%lld ", f0);
        long long f_keyingi = f0 + f1;
        f0 = f1;
        f1 = f_keyingi;
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir yangi had oldingi ikki had yig'indisiga teng.
2. O'zgaruvchilarni navbati bilan siljitib borish xotirani tejaydi (O(1) xotira).

## Ishlash natijasi:
```text
Fibonachchi (8 ta): 0 1 1 2 3 5 8 13
```

---

# 176-Topshiriq: Sonning tub (Prime) ekanligini sqrt(N) gacha tekshirish

## Topshiriq sharti:
Optimal algoritm orqali sonning tubligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool tubmi(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;

    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return false;
        }
    }
    return true;
}

int main(void) {
    int son = 29;
    printf("%d tub sonmi: %s\n", son, tubmi(son) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sonning bo'luvchisi juftlikda keladi; agar son `sqrt(n)` gacha bo'linmasa, undan keyin ham bo'linmaydi.
2. `i * i <= n` orqali tekshirish `sqrt` funksiyasini chaqirmasdan butun sonli hisob beradi.

## Ishlash natijasi:
```text
29 tub sonmi: Ha
```

---

# 177-Topshiriq: [A, B] oralig'idagi barcha tub sonlarni topish

## Topshiriq sharti:
10 dan 30 gacha bo'lgan barcha tub sonlarni chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool tubmi(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}

int main(void) {
    int a = 10, b = 30;
    printf("[%d, %d] oralig'idagi tub sonlar: ", a, b);

    for (int i = a; i <= b; i++) {
        if (tubmi(i)) {
            printf("%d ", i);
        }
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oraliqdagi har bir son alohida tublikka tekshiriladi.

## Ishlash natijasi:
```text
[10, 30] oralig'idagi tub sonlar: 11 13 17 19 23 29
```

---

# 178-Topshiriq: Eratosfen g'alviri (Sieve of Eratosthenes) algoritmi asoslari

## Topshiriq sharti:
Massiv yordamida 30 gacha bo'lgan barcha tub sonlarni toping.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    int n = 30;
    bool tub[31];
    for (int i = 0; i <= n; i++) tub[i] = true;
    tub[0] = tub[1] = false;

    for (int p = 2; p * p <= n; p++) {
        if (tub[p]) {
            for (int i = p * p; i <= n; i += p) {
                tub[i] = false;
            }
        }
    }

    printf("30 gacha bo'lgan tub sonlar: ");
    for (int i = 2; i <= n; i++) {
        if (tub[i]) printf("%d ", i);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Eratosfen g'alviri har bir topilgan tub sonning barcha karralilarini o'chirib chiqadi.
2. Murakkabligi O(N log log N) bo'lib, oraliqdagi tub sonlarni topishning eng tezkor usulidir.

## Ishlash natijasi:
```text
30 gacha bo'lgan tub sonlar: 2 3 5 7 11 13 17 19 23 29
```

---

# 179-Topshiriq: Evklid algoritmi: Eng Katta Umumiy Bo'luvchi (EKUB / GCD)

## Topshiriq sharti:
Ikki sonning EKUBini qoldiqli bo'lish sikli orqali toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int ekub(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int main(void) {
    int x = 48, y = 18;
    printf("EKUB(%d, %d) = %d\n", x, y, ekub(x, y));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Evklid algoritmi: `EKUB(a, b) = EKUB(b, a % b)`.
2. `b` nolga teng bo'lguncha qoldiq almashtiriladi; oxirgi qolgan `a` EKUB bo'ladi.

## Ishlash natijasi:
```text
EKUB(48, 18) = 6
```

---

# 180-Topshiriq: Eng Kichik Umumiy Karrali (EKUK / LCM) hisoblash

## Topshiriq sharti:
EKUB orqali EKUKni hisoblash formulasini amalga oshiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int ekub(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

long long ekuk(int a, int b) {
    return ((long long)a * b) / ekub(a, b);
}

int main(void) {
    int a = 12, b = 15;
    printf("EKUK(%d, %d) = %lld\n", a, b, ekuk(a, b));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matematik formula: `EKUK(a, b) = (a * b) / EKUB(a, b)`.
2. 12 va 15 uchun EKUB 3, ko'paytmasi 180, EKUK esa 60.

## Ishlash natijasi:
```text
EKUK(12, 15) = 60
```

---

# 181-Topshiriq: Sonning barcha natural bo'luvchilarini topish va chop etish

## Topshiriq sharti:
Sonning barcha bo'luvchilarini sikl bilan aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 36;
    printf("%d sonining bo'luvchilari: ", son);

    for (int i = 1; i <= son; i++) {
        if (son % i == 0) {
            printf("%d ", i);
        }
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1 dan n gacha bo'lgan har bir son qoldiqsiz bo'linishga tekshiriladi.

## Ishlash natijasi:
```text
36 sonining bo'luvchilari: 1 2 3 4 6 9 12 18 36
```

---

# 182-Topshiriq: Mukammal sonni (Perfect Number) aniqlash

## Topshiriq sharti:
O'zidan tashqari barcha bo'luvchilari yig'indisi o'ziga teng bo'lgan sonni toping.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool mukammal_sonmi(int n) {
    if (n <= 1) return false;
    int yigindi = 1;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            yigindi += i;
            if (i * i != n) {
                yigindi += n / i;
            }
        }
    }
    return yigindi == n;
}

int main(void) {
    int a = 28;
    int b = 12;

    printf("%d mukammal sonmi: %s\n", a, mukammal_sonmi(a) ? "Ha" : "Yo'q");
    printf("%d mukammal sonmi: %s\n", b, mukammal_sonmi(b) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 28 ning bo'luvchilari: 1, 2, 4, 7, 14.
2. 1 + 2 + 4 + 7 + 14 = 28 bo'lgani sababli u mukammal sondir.

## Ishlash natijasi:
```text
28 mukammal sonmi: Ha
12 mukammal sonmi: Yo'q
```

---

# 183-Topshiriq: Armstrong sonini aniqlash (Har bir raqamining kublari yig'indisi)

## Topshiriq sharti:
Uch xonali son Armstrong soni ekanligini tekshiring (153 = 1^3 + 5^3 + 3^3).

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool armstrongmi(int n) {
    int asl = n;
    int yigindi = 0;
    while (n > 0) {
        int r = n % 10;
        yigindi += r * r * r;
        n /= 10;
    }
    return yigindi == asl;
}

int main(void) {
    int son = 153;
    printf("%d Armstrong sonimi: %s\n", son, armstrongmi(son) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153.

## Ishlash natijasi:
```text
153 Armstrong sonimi: Ha
```

---

# 184-Topshiriq: Sonni tub ko'paytuvchilarga ajratish (Prime Factorization)

## Topshiriq sharti:
Sonni tub ko'paytuvchilar ko'rinishida chop etuvchi siklni tuzing.

## Yechim (C kodi):
```c
#include <stdio.h>

void tub_kopaytuvchilar(int n) {
    printf("%d = ", n);
    for (int p = 2; p * p <= n; p++) {
        while (n % p == 0) {
            printf("%d ", p);
            n /= p;
            if (n > 1) printf("* ");
        }
    }
    if (n > 1) {
        printf("%d", n);
    }
    printf("\n");
}

int main(void) {
    tub_kopaytuvchilar(84);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir bo'luvchi `p` sonni qoldiqsiz bo'lgunicha sikl orqali bo'lib boriladi.
2. 84 = 2 * 2 * 3 * 7.

## Ishlash natijasi:
```text
84 = 2 * 2 * 3 * 7
```

---

# 185-Topshiriq: O'nlik sonni ikkilik (binary) sanoq sistemasiga sikl orqali o'tkazish

## Topshiriq sharti:
Sonni 2 ga bo'lib qoldiqlarni yig'ish orqali binar formatda chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

void chop_et_binar(unsigned int n) {
    int binar[32];
    int i = 0;

    if (n == 0) {
        printf("0\n");
        return;
    }

    while (n > 0) {
        binar[i++] = n % 2;
        n /= 2;
    }

    for (int j = i - 1; j >= 0; j--) {
        printf("%d", binar[j]);
    }
    printf("\n");
}

int main(void) {
    printf("43 soni ikkilikda: ");
    chop_et_binar(43);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 2 ga bo'lish qoldiqlari massivga teskari yoziladi va oxiridan boshlab chiqariladi.

## Ishlash natijasi:
```text
43 soni ikkilikda: 101011
```

---

# 186-Topshiriq: Ikkilik son satrini o'nlik butun songa o'tkazish

## Topshiriq sharti:
Binar satrni ('10110') o'nlik songa aylantiruvchi siklni yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int binar_to_onlik(const char *s) {
    int natija = 0;
    for (int i = 0; s[i] != '\0'; i++) {
        natija = (natija << 1) + (s[i] - '0');
    }
    return natija;
}

int main(void) {
    char binar_satr[] = "10110";
    printf("'%s' ikkilik satri o'nlikda: %d\n", binar_satr, binar_to_onlik(binar_satr));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir belgi uchun `natija = (natija * 2) + raqam` amali bajariladi.
2. `natija << 1` 2 ga ko'paytirish bilan tengdir.

## Ishlash natijasi:
```text
'10110' ikkilik satri o'nlikda: 22
```

---

# 187-Topshiriq: O'nlik sonni o'n oltilik (Hex) sanoq sistemasiga sikl orqali o'tkazish

## Topshiriq sharti:
Sonni 16 ga bo'lib qoldiqlarni '0'-'9' va 'A'-'F' ga aylantiring.

## Yechim (C kodi):
```c
#include <stdio.h>

void chop_et_hex(unsigned int n) {
    char hex_belgilar[] = "0123456789ABCDEF";
    char bufer[16];
    int idx = 0;

    if (n == 0) {
        printf("0x0\n");
        return;
    }

    while (n > 0) {
        bufer[idx++] = hex_belgilar[n % 16];
        n /= 16;
    }

    printf("0x");
    for (int j = idx - 1; j >= 0; j--) {
        printf("%c", bufer[j]);
    }
    printf("\n");
}

int main(void) {
    printf("255 soni o'n oltilikda: ");
    chop_et_hex(255);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 16 ga bo'lish qoldiqlari `hex_belgilar` jadvalidagi mos belgiga o'giriladi.

## Ishlash natijasi:
```text
255 soni o'n oltilikda: 0xFF
```

---

# 188-Topshiriq: Darajaga ko'tarish algoritmi (Oddiy for sikli orqali)

## Topshiriq sharti:
Asos va darajani ko'paytirib chiqish siklini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

long long daraja(int asos, int daraja_k) {
    long long res = 1;
    for (int i = 0; i < daraja_k; i++) {
        res *= asos;
    }
    return res;
}

int main(void) {
    printf("3^4 = %lld\n", daraja(3, 4));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O(N) murakkablikdagi klassik ko'paytirish sikli.

## Ishlash natijasi:
```text
3^4 = 81
```

---

# 189-Topshiriq: Tezkor darajaga ko'tarish (Binary Exponentiation / Fast Power: O(log N))

## Topshiriq sharti:
Logarifmik vaqtda darajaga ko'taruvchi siklni dasturlang.

## Yechim (C kodi):
```c
#include <stdio.h>

long long tezkor_daraja(long long asos, int daraja) {
    long long natija = 1;
    while (daraja > 0) {
        if (daraja & 1) { // Agar toq bo'lsa
            natija *= asos;
        }
        asos *= asos;
        daraja >>= 1; // 2 ga bo'lish
    }
    return natija;
}

int main(void) {
    printf("2^10 = %lld\n", tezkor_daraja(2, 10));
    printf("3^7 = %lld\n", tezkor_daraja(3, 7));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar daraja juft bo'lsa `a^n = (a^2)^(n/2)`.
2. Bu algoritm 1000 darajani 1000 qadam emas, atigi 10 ta qadamda hisoblaydi.

## Ishlash natijasi:
```text
2^10 = 1024
3^7 = 2187
```

---

# 190-Topshiriq: Nyuton usuli (Babylonian method) bilan kvadrat ildiz hisoblash

## Topshiriq sharti:
while sikli orqali kvadrat ildizni yaqinlashuvchi iteratsiya bilan toping.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

double nyuton_sqrt(double s) {
    double x = s;
    double aniqlik = 1e-7;
    while (1) {
        double keyingi_x = 0.5 * (x + s / x);
        if (fabs(x - keyingi_x) < aniqlik) {
            break;
        }
        x = keyingi_x;
    }
    return x;
}

int main(void) {
    double son = 25.0;
    printf("sqrt(%.1lf) = %.5lf\n", son, nyuton_sqrt(son));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Nyuton-Rafson formulasi: `x_k+1 = 0.5 * (x_k + s / x_k)`.
2. Sikl farq belgilangan aniqlikdan kichik bo'lgunicha aylanadi va kvadrat ildizga juda tez yaqinlashadi.

## Ishlash natijasi:
```text
sqrt(25.0) = 5.00000
```

---

# 191-Topshiriq: Leybnits qatori yordamida Pi sonini yaqinlashtirib hisoblash

## Topshiriq sharti:
Pi / 4 = 1 - 1/3 + 1/5 - 1/7 + ... qatorini sikl bilan jamlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int iteratsiyalar = 100000;
    double pi_taqribiy = 0.0;
    double ishora = 1.0;

    for (int i = 0; i < iteratsiyalar; i++) {
        pi_taqribiy += ishora / (2 * i + 1);
        ishora = -ishora;
    }
    pi_taqribiy *= 4.0;

    printf("%d iteratsiyadan so'ng Pi: %.5lf\n", iteratsiyalar, pi_taqribiy);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Belgisi almashinib boruvchi Leybnits qatori Pi ga yaqinlashadi.

## Ishlash natijasi:
```text
100000 iteratsiyadan so'ng Pi: 3.14158
```

---

# 192-Topshiriq: Teylor qatori orqali e^x sonini hisoblash

## Topshiriq sharti:
e^x = 1 + x/1! + x^2/2! + ... qatorini hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

double hisobla_exp(double x) {
    double yigindi = 1.0;
    double had = 1.0;
    for (int n = 1; n <= 15; n++) {
        had = had * x / n;
        yigindi += had;
    }
    return yigindi;
}

int main(void) {
    printf("e^1 = %.6lf\n", hisobla_exp(1.0));
    printf("e^2 = %.6lf\n", hisobla_exp(2.0));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir yangi had oldingi hadga `x / n` ni ko'paytirish orqali hosil qilinadi.

## Ishlash natijasi:
```text
e^1 = 2.718282
e^2 = 7.389056
```

---

# 193-Topshiriq: Sinus funksiyasini Teylor qatori orqali hisoblash

## Topshiriq sharti:
sin(x) ni Makloren qatori orqali sikl yordamida hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

double hisobla_sin(double x) {
    double yigindi = x;
    double had = x;
    for (int i = 1; i <= 7; i++) {
        had = -had * x * x / ((2 * i) * (2 * i + 1));
        yigindi += had;
    }
    return yigindi;
}

int main(void) {
    double pi = 3.14159265;
    double burchak = pi / 6; // 30 gradus (sin(30) = 0.5)
    printf("sin(pi/6) = %.4lf\n", hisobla_sin(burchak));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sin(x) = x - x^3/3! + x^5/5! - x^7/7! + ...`

## Ishlash natijasi:
```text
sin(pi/6) = 0.5000
```

---

# 194-Topshiriq: goto operatori va label: 3 qavat ichma-ich sikldan birdaniga chiqish

## Topshiriq sharti:
Ichma-ich 3 ta for siklidan maqsadli son topilganda bitta sakrash bilan chiqing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int maqsad = 42;

    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            for (int k = 0; k < 10; k++) {
                if (i * 100 + j * 10 + k == maqsad) {
                    printf("Topildi: i=%d, j=%d, k=%d\n", i, j, k);
                    goto sikldan_chiqish;
                }
            }
        }
    }

sikldan_chiqish:
    printf("Barcha ichma-ich sikllardan muvaffaqiyatli chiqildi!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `break` faqat o'zi turgan 1 ta sikldan chiqaradi.
2. 3 ta sikldan chiqish uchun 3 ta bayroq va 3 ta break yozish o'rniga `goto nishon;` ishlatish C tilidagi eng asosiy va to'g'ri oqlangan foydalanish holatidir.

## Ishlash natijasi:
```text
Topildi: i=0, j=4, k=2
Barcha ichma-ich sikllardan muvaffaqiyatli chiqildi!
```

---

# 195-Topshiriq: goto bilan resurslarni tozalash (Cleanup Pattern — Linux Kernel uslubi)

## Topshiriq sharti:
Xatolik yuz berganda xotira va fayllarni toza yopish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    bool resurs1_ochildimi = true;
    bool resurs2_xatolik = true;

    printf("Resurs 1 tayyorlandi.\n");

    if (resurs2_xatolik) {
        printf("XATOLIK: Resurs 2 yuklanmadi!\n");
        goto tozalash;
    }

    printf("Asosiy ish bajarildi.\n");

tozalash:
    if (resurs1_ochildimi) {
        printf("Resurs 1 xavfsiz tozalandi va yopildi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Linux yadrosi (Kernel) C kodida xatolik yuz berganda resurslarni ozod qilish uchun bitta `cleanup` nishoniga `goto` qilish oltin standartdir.

## Ishlash natijasi:
```text
Resurs 1 tayyorlandi.
XATOLIK: Resurs 2 yuklanmadi!
Resurs 1 xavfsiz tozalandi va yopildi.
```

---

# 196-Topshiriq: Siklni optimallashtirish: Loop Invariant Code Motion

## Topshiriq sharti:
Sikl ichidagi o'zgarmas hisob-kitoblarni sikl tashqarisiga chiqarish afzalligi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int kenglik = 1920;
    int balandlik = 1080;

    // YOMON USUL: for (int i = 0; i < n; i++) { int piksel = kenglik * balandlik; ... }
    // TO'G'RI USUL (Loop Invariant tashqarida):
    int jami_piksel = kenglik * balandlik;
    long long hisob = 0;

    for (int i = 0; i < 5; i++) {
        hisob += jami_piksel;
    }

    printf("Jami piksel hisobi: %lld\n", hisob);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sikl ichida qiymati o'zgarmaydigan har qanday amalni sikl tashqarisida hisoblash CPU ga millionlab keraksiz ko'paytirishlarni bajarmaslik imkonini beradi.

## Ishlash natijasi:
```text
Jami piksel hisobi: 10368000
```

---

# 197-Topshiriq: Siklni ochish (Loop Unrolling) orqali tezlikni oshirish

## Topshiriq sharti:
Sikl shartini kamroq tekshirish uchun iteratsiyalarni guruhlab bajarish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int massiv[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    int yigindi = 0;

    // Loop Unrolling (qadami 4):
    for (int i = 0; i < 8; i += 4) {
        yigindi += massiv[i];
        yigindi += massiv[i + 1];
        yigindi += massiv[i + 2];
        yigindi += massiv[i + 3];
    }

    printf("Unrolled sikl yig'indisi: %d\n", yigindi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Loop unrolling — sikl hisoblagichini va sakrash buyruqlarini (branch overhead) kamaytiradi.
2. Zamonaviy kompilyatorlar `-O3` bayrog'ida buni avtomatik bajaradi.

## Ishlash natijasi:
```text
Unrolled sikl yig'indisi: 36
```

---

# 198-Topshiriq: Sikl hisoblagichida suzuvchi sonlar (float) ishlatish xatosi

## Topshiriq sharti:
float i = 0.0; i != 1.0; i += 0.1 cheksiz siklga aylanib ketishi sababi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // XATOLI USUL: for (float f = 0.0f; f != 1.0f; f += 0.1f) -> Cheksiz sikl bo'ladi!
    // Chunki 0.1 ikkilikda aniq emas va f hech qachon 1.0f ga teng bo'lmaydi.

    // TO'G'RI USUL: Butun sonli sikl bilan kasr hosil qilish
    for (int i = 0; i <= 10; i++) {
        float f = i * 0.1f;
        printf("%.1f ", f);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Suzuvchi nuqtali sonlarda `==` yoki `!=` bilan sikl to'xtatish mutlaqo taqiqlanadi.
2. Har doim butun sonli hisoblagich ishlatib, uni kasrga ko'paytirish lozim.

## Ishlash natijasi:
```text
0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
```

---

# 199-Topshiriq: Kollats gipotezasi (Collatz Conjecture / 3n + 1 muammosi)

## Topshiriq sharti:
Juft bo'lsa n/2, toq bo'lsa 3n+1 qilib 1 ga yetib borish zanjirini chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    long long n = 6;
    int qadam = 0;

    printf("Kollats zanjiri (%lld): ", n);
    while (n != 1) {
        printf("%lld -> ", n);
        if (n % 2 == 0) {
            n /= 2;
        } else {
            n = 3 * n + 1;
        }
        qadam++;
    }
    printf("1 (Jami qadamlar: %d)\n", qadam);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matematikadagi eng mashhur ochiq muammolardan biri.
2. 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1 (8 qadamda 1 ga yetadi).

## Ishlash natijasi:
```text
Kollats zanjiri (6): 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1 (Jami qadamlar: 8)
```

---

# 200-Topshiriq: ASCII grafikasi: Sinus to'lqinini konsolda sikllar yordamida chizish

## Topshiriq sharti:
for sikli va probellar yordamida vertikal sinus to'lqini grafigini chizing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    int nuqtalar_soni = 10;
    int kenglik = 20;

    for (int i = 0; i < nuqtalar_soni; i++) {
        double burchak = i * (3.14159265 / 4.0); // Qadami 45 gradus
        int probellar = (int)(kenglik / 2 + (sin(burchak) * (kenglik / 2 - 1)));
        
        for (int p = 0; p < probellar; p++) {
            printf(" ");
        }
        printf("*\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sin(burchak)` -1 dan +1 gacha tebranadi.
2. Uni masshtablab `probellar` soniga aylantirish orqali konsolda gorizontal siljish va to'lqin hosil qilinadi.
3. Bu 4-qismning barcha sikl va matematik imkoniyatlarini mustahkamlaydi.

## Ishlash natijasi:
```text
*
                *
                   *
                *
          *
    *
 *
    *
          *
                *
```

---
