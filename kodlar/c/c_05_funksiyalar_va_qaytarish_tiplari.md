# C Dasturlash Tili — 5-Qism: Funksiyalar va Qaytarish Tiplari
## (201-250 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* Funksiya prototipi va ta'rifi, pass-by-value tabiati
* Rekursiya: Base case, quyruq rekursiyasi (Tail recursion), Xanoy minoralari
* Saqlash toifalari: auto, static (lokal va global), extern, register
* inline funksiyalar va Stack Frame arxitekturasi
* stdarg.h: Variadic funksiyalar va o'z printf() analogi
* Funksiyadan ko'rsatkich qaytarish xavfsizligi va Recursive Descent Parser

---

# 201-Topshiriq: Funksiya prototipi (Declaration) va ta'rifi (Definition)

## Topshiriq sharti:
Funksiya prototipini main dan oldin e'lon qilib, uning tanasini main dan keyin yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

// Funksiya prototipi (Forward declaration)
int kvadrat(int x);

int main(void) {
    int son = 7;
    printf("%d ning kvadrati: %d\n", son, kvadrat(son));
    return 0;
}

// Funksiya ta'rifi
int kvadrat(int x) {
    return x * x;
}
```

## Tushuntirish va Mantiq:
1. Prototip kompilyatorga funksiyaning nomi, parametrlar turlari va qaytarish tipini oldindan bildiradi.
2. Bu C dasturining kirish nuqtasi bo'lgan `main` funksiyasini fayl boshida o'qilishi oson qilib joylashtirish imkonini beradi.

## Ishlash natijasi:
```text
7 ning kvadrati: 49
```

---

# 202-Topshiriq: Qiymat qaytarmaydigan void funksiyalar

## Topshiriq sharti:
Ekranga ajratuvchi chiziq va salom matnini chiqaruvchi void funksiya yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

void chiziq_tort(int uzunlik) {
    for (int i = 0; i < uzunlik; i++) {
        printf("=");
    }
    printf("\n");
}

int main(void) {
    chiziq_tort(20);
    printf("   XUSH KELIBSIZ!\n");
    chiziq_tort(20);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `void` qaytarish tipi funksiya hech qanday qiymat qaytarmasligini bildiradi.
2. Bunday funksiyalarda `return;` yozish ixtiyoriy bo'lib, odatda funksiyani muddatidan oldin to'xtatish uchun ishlatiladi.

## Ishlash natijasi:
```text
====================
   XUSH KELIBSIZ!
====================
```

---

# 203-Topshiriq: Qiymat qaytaruvchi int funksiya: Ikkita sonning kattasini topish

## Topshiriq sharti:
Ikki sondan kattasini aniqlab qaytaruvchi funksiyani yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int kattasi(int a, int b) {
    return (a > b) ? a : b;
}

int main(void) {
    int x = 25, y = 42;
    printf("%d va %d ning kattasi: %d\n", x, y, kattasi(x, y));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiya bajarilishi tugagach, `return` orqali natija chaqiruvchi kodga uzatiladi.

## Ishlash natijasi:
```text
25 va 42 ning kattasi: 42
```

---

# 204-Topshiriq: Haqiqiy son qaytaruvchi double funksiya: Doira yuzini hisoblash

## Topshiriq sharti:
Radius bo'yicha doira yuzini hisoblovchi funksiya tuzing.

## Yechim (C kodi):
```c
#include <stdio.h>

#define PI 3.1415926535

double doira_yuzi(double radius) {
    if (radius < 0.0) return 0.0;
    return PI * radius * radius;
}

int main(void) {
    double r = 5.0;
    printf("Radius %.1lf li doira yuzi: %.4lf\n", r, doira_yuzi(r));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `double` qaytarish tipi hisob-kitoblarning yuqori aniqligini ta'minlaydi.

## Ishlash natijasi:
```text
Radius 5.0 li doira yuzi: 78.5398
```

---

# 205-Topshiriq: Funksiyaga Pass-by-value (Qiymat bo'yicha uzatish) mexanizmi

## Topshiriq sharti:
Funksiya ichida o'zgartirilgan parametr tashqi o'zgaruvchiga ta'sir qilmasligini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

void ozgartir(int son) {
    son = son + 100;
    printf("Funksiya ichida: son = %d\n", son);
}

int main(void) {
    int x = 10;
    printf("Chaqirishdan oldin: x = %d\n", x);
    ozgartir(x);
    printf("Chaqirilgandan keyin: x = %d\n", x);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida barcha argumentlar standart bo'yicha qiymat nusxasi (copy by value) sifatida uzatiladi.
2. `ozgartir` funksiyasi `x` ning stekdagi alohida nusxasi ustida ishlaydi, shuning uchun `main` dagi asl `x` o'zgarmasdan qoladi.

## Ishlash natijasi:
```text
Chaqirishdan oldin: x = 10
Funksiya ichida: son = 110
Chaqirilgandan keyin: x = 10
```

---

# 206-Topshiriq: Nima uchun pass-by-value bilan oddiy swap(a, b) ishlamaydi?

## Topshiriq sharti:
Ikki o'zgaruvchi qiymatini nusxa orqali almashtirishga urinish xatosini tahlil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

void xato_swap(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
}

int main(void) {
    int x = 5, y = 9;
    printf("Oldin: x = %d, y = %d\n", x, y);
    xato_swap(x, y);
    printf("Keyin: x = %d, y = %d (Qiymatlar o'zgarmadi!)\n", x, y);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `xato_swap` ichidagi `a` va `b` lokal nusxalardir; ular o'zaro almashadi, lekin funksiya tugashi bilan yo'q bo'ladi.
2. Haqiqiy almashtirish uchun o'zgaruvchilarning ko'rsatkichlari (pointerlar) uzatilishi shart (`swap(&x, &y)`).

## Ishlash natijasi:
```text
Oldin: x = 5, y = 9
Keyin: x = 5, y = 9 (Qiymatlar o'zgarmadi!)
```

---

# 207-Topshiriq: Funksiyaga massivni argument sifatida uzatish

## Topshiriq sharti:
Massiv elementlari yig'indisini hisoblovchi funksiya yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int massiv_yigindisi(const int massiv[], int olcham) {
    int yigindi = 0;
    for (int i = 0; i < olcham; i++) {
        yigindi += massiv[i];
    }
    return yigindi;
}

int main(void) {
    int sonlar[] = {10, 20, 30, 40, 50};
    int jami = massiv_yigindisi(sonlar, 5);
    printf("Massiv yig'indisi: %d\n", jami);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da massiv funksiyaga uzatilganda u to'liq nusxalanmaydi, balki birinchi elementining ko'rsatkichiga aylanadi (array decaying).
2. Shuning uchun massiv bilan birga har doim uning o'lchami (`olcham`) ham alohida parametr qilib uzatiladi.
3. `const` modifikatori massiv elementlarini tasodifiy o'zgartirishdan asraydi.

## Ishlash natijasi:
```text
Massiv yig'indisi: 150
```

---

# 208-Topshiriq: Rekursiya asoslari: To'xtash sharti (Base case) va faktorial hisoblash

## Topshiriq sharti:
To'xtash sharti va rekursiv qadam bilan faktorial funksiyasini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

long long rekursiv_faktorial(int n) {
    // To'xtash sharti (Base case)
    if (n <= 1) return 1;
    // Rekursiv chaqiruv
    return n * rekursiv_faktorial(n - 1);
}

int main(void) {
    int son = 5;
    printf("%d! = %lld\n", son, rekursiv_faktorial(son));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Rekursiya — funksiyaning o'z-o'zini chaqirishidir.
2. Har bir rekursiv funksiyada to'xtash sharti bo'lishi shart, aks holda dastur cheksiz chuqurlashib Stack Overflow halokatiga uchraydi.
3. 5 * faktorial(4) -> 5 * 4 * faktorial(3) ... = 120.

## Ishlash natijasi:
```text
5! = 120
```

---

# 209-Topshiriq: Rekursiv Fibonachchi va uning daraxtsimon chaqiruv strukturasi

## Topshiriq sharti:
Fibonachchi ketma-ketligini rekursiv topuvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

int fibonachchi(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    return fibonachchi(n - 1) + fibonachchi(n - 2);
}

int main(void) {
    printf("Fibonachchi(7) = %d\n", fibonachchi(7));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir chaqiruv yana ikkita chaqiruvni tug'diradi (bifurkatsiya daraxti).
2. Algoritmik murakkabligi O(2^N) bo'lib, katta sonlar uchun sekin ishlaydi, ammo rekursiya mantiqini juda chiroyli ifodalaydi.

## Ishlash natijasi:
```text
Fibonachchi(7) = 13
```

---

# 210-Topshiriq: Quyruq rekursiyasi (Tail recursion) va stek xotirasini tejash

## Topshiriq sharti:
Faktorialni quyruq rekursiyasi (akkumulyator parametri) orqali yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

long long faktorial_tail(int n, long long akkumulyator) {
    if (n <= 1) return akkumulyator;
    return faktorial_tail(n - 1, n * akkumulyator);
}

int main(void) {
    printf("Tail faktorial(6) = %lld\n", faktorial_tail(6, 1));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Quyruq rekursiyasida rekursiv chaqiruv funksiyaning eng oxirgi amali hisoblanadi (qo'shimcha ko'paytirish qolmaydi).
2. Zamonaviy optimallashtiruvchi kompilyatorlar bunday rekursiyani oddiy siklga (jump) aylantiradi (Tail Call Optimization - TCO) va yangi stek kadrlari yaratilmaydi.

## Ishlash natijasi:
```text
Tail faktorial(6) = 720
```

---

# 211-Topshiriq: Rekursiya orqali sonning raqamlari yig'indisini hisoblash

## Topshiriq sharti:
Sonning raqamlarini rekursiv ajratib yig'indisini toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int raqamlar_yigindisi(int n) {
    if (n == 0) return 0;
    return (n % 10) + raqamlar_yigindisi(n / 10);
}

int main(void) {
    int son = 1234;
    printf("%d raqamlari yig'indisi: %d\n", son, raqamlar_yigindisi(son));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `n % 10` oxirgi raqamni qo'shadi, qolgan qism rekursiv yuboriladi: 4 + 3 + 2 + 1 = 10.

## Ishlash natijasi:
```text
1234 raqamlari yig'indisi: 10
```

---

# 212-Topshiriq: Rekursiya orqali natural sonlar yig'indisi

## Topshiriq sharti:
1 dan N gacha sonlar yig'indisini rekursiv hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

int natural_yigindi(int n) {
    if (n <= 1) return n;
    return n + natural_yigindi(n - 1);
}

int main(void) {
    printf("1 dan 10 gacha yig'indi: %d\n", natural_yigindi(10));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 10 + 9 + ... + 1 = 55.

## Ishlash natijasi:
```text
1 dan 10 gacha yig'indi: 55
```

---

# 213-Topshiriq: Rekursiya orqali darajaga ko'tarish (Power: a^b)

## Topshiriq sharti:
Rekursiv daraja funksiyasini dasturlang.

## Yechim (C kodi):
```c
#include <stdio.h>

double rekursiv_daraja(double asos, int daraja) {
    if (daraja == 0) return 1.0;
    if (daraja < 0) return 1.0 / rekursiv_daraja(asos, -daraja);
    return asos * rekursiv_daraja(asos, daraja - 1);
}

int main(void) {
    printf("2.0^4 = %.1lf\n", rekursiv_daraja(2.0, 4));
    printf("2.0^-2 = %.2lf\n", rekursiv_daraja(2.0, -2));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Manfiy daraja holati `1.0 / power(a, -b)` orqali chiroyli hal qilinadi.

## Ishlash natijasi:
```text
2.0^4 = 16.0
2.0^-2 = 0.25
```

---

# 214-Topshiriq: Rekursiya orqali satrni teskari chop etish

## Topshiriq sharti:
Satrni ko'rsatkich va rekursiya yordamida orqasidan boshlab chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

void teskari_chop(const char *s) {
    if (*s == '\0') return; // Satr oxiri
    teskari_chop(s + 1);   // Keyingi belgiga o'tish
    putchar(*s);           // Stekdan qaytishda chop etish
}

int main(void) {
    printf("Teskari: ");
    teskari_chop("ANTIGRAVITY");
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Rekursiya chaqiruvi `putchar(*s)` dan oldin yozilgani sababli, belgilar stekda to'planib boradi.
2. Satr oxiriga yetgach, funksiyalar stekdan qaytishda eng oxirgi harfdan boshlab birin-ketin konsolga chiqaradi.

## Ishlash natijasi:
```text
Teskari: YTIVARGINA
```

---

# 215-Topshiriq: Xanoy minoralari (Towers of Hanoi) rekursiv boshqotirmasi

## Topshiriq sharti:
3 ta diskni A sterjendan C sterjenga B yordamida ko'chirish qadamlarini chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

void xanoy(int n, char a, char c, char b) {
    if (n == 1) {
        printf("Disk 1 ni %c dan %c ga ko'chiring\n", a, c);
        return;
    }
    xanoy(n - 1, a, b, c);
    printf("Disk %d ni %c dan %c ga ko'chiring\n", n, a, c);
    xanoy(n - 1, b, c, a);
}

int main(void) {
    int disklar = 3;
    printf("Xanoy minoralari (%d ta disk):\n", disklar);
    xanoy(disklar, 'A', 'C', 'B');
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boshqotirma qoidasi: hech qachon katta disk kichik disk ustiga qo'yilmasligi kerak.
2. 3 ta disk uchun jami 2^3 - 1 = 7 ta qadam talab qilinadi.

## Ishlash natijasi:
```text
Xanoy minoralari (3 ta disk):
Disk 1 ni A dan C ga ko'chiring
Disk 2 ni A dan B ga ko'chiring
Disk 1 ni C dan B ga ko'chiring
Disk 3 ni A dan C ga ko'chiring
Disk 1 ni B dan A ga ko'chiring
Disk 2 ni B dan C ga ko'chiring
Disk 1 ni A dan C ga ko'chiring
```

---

# 216-Topshiriq: Rekursiv Evklid algoritmi (EKUB / GCD)

## Topshiriq sharti:
Bitta qatorda EKUBni rekursiv topuvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

int rekursiv_ekub(int a, int b) {
    return (b == 0) ? a : rekursiv_ekub(b, a % b);
}

int main(void) {
    printf("EKUB(54, 24) = %d\n", rekursiv_ekub(54, 24));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. EKUB ning eng nafis va qisqa ifodasi.

## Ishlash natijasi:
```text
EKUB(54, 24) = 6
```

---

# 217-Topshiriq: Saqlash toifalari: auto kalit so'zi va lokal o'zgaruvchilar umri

## Topshiriq sharti:
Lokal avtomatik o'zgaruvchilarning stekdagi umr davrini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

void sinov(void) {
    auto int son = 10; // auto odatda tushirib qoldiriladi
    son++;
    printf("Funksiya ichida son: %d\n", son);
}

int main(void) {
    sinov();
    sinov();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `auto` o'zgaruvchi blokga kirilganda stekda yaratiladi va blok tugashi bilan yo'q bo'ladi.
2. Har bir yangi chaqiruvda u qaytadan 10 ga tenglashtiriladi.

## Ishlash natijasi:
```text
Funksiya ichida son: 11
Funksiya ichida son: 11
```

---

# 218-Topshiriq: static lokal o'zgaruvchilar: Chaqiruvlar oralig'ida qiymatni saqlab qolish

## Topshiriq sharti:
static o'zgaruvchi orqali funksiya necha marta chaqirilganini sanang.

## Yechim (C kodi):
```c
#include <stdio.h>

void hisobla(void) {
    static int hisoblagich = 0; // Faqat birinchi chaqiruvda initsializatsiya qilinadi
    hisoblagich++;
    printf("Funksiya chaqirildi: %d-marta\n", hisoblagich);
}

int main(void) {
    hisobla();
    hisobla();
    hisobla();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Lokal o'zgaruvchi oldiga `static` qo'yilsa, u stekda emas, ma'lumotlar segmentida (Data segment) saqlanadi.
2. Funksiya tugasa ham uning qiymati o'chib ketmaydi va keyingi chaqiruvda davom ettiriladi.

## Ishlash natijasi:
```text
Funksiya chaqirildi: 1-marta
Funksiya chaqirildi: 2-marta
Funksiya chaqirildi: 3-marta
```

---

# 219-Topshiriq: static global o'zgaruvchi: Ichki bog'lanish (Internal linkage)

## Topshiriq sharti:
Global o'zgaruvchini faqat joriy .c fayl ichida cheklashni ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

static int ichki_maxfiy_id = 1001; // Boshqa .c fayllardan extern orqali ko'rib bo'lmaydi

void id_korsat(void) {
    printf("Maxfiy modul ID: %d\n", ichki_maxfiy_id);
}

int main(void) {
    id_korsat();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Global o'zgaruvchi oldiga `static` qo'yilsa, uning bog'lanishi (linkage) ichki bo'ladi.
2. Bog'lovchi (Linker) boshqa obyekt fayllarga bu nomni bermaydi, bu nomlar to'qnashuvini (naming collisions) oldini oladi.

## Ishlash natijasi:
```text
Maxfiy modul ID: 1001
```

---

# 220-Topshiriq: static funksiya: Funksiyani modul ichida xususiy (private) qilish

## Topshiriq sharti:
Modul ichki yordamchi funksiyasini static qilib cheklang.

## Yechim (C kodi):
```c
#include <stdio.h>

// Faqat shu fayl ichida ko'rinuvchi yordamchi funksiya
static int yordamchi_hisob(int a) {
    return a * 2 + 1;
}

void ochiq_api(int x) {
    int res = yordamchi_hisob(x);
    printf("API natijasi: %d\n", res);
}

int main(void) {
    ochiq_api(5);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida klassik OOP klasslari yo'q, lekin `static` funksiyalar orqali haqiqiy enkapsulyatsiya (private methods) amalga oshiriladi.

## Ishlash natijasi:
```text
API natijasi: 11
```

---

# 221-Topshiriq: extern kalit so'zi: Tashqi global o'zgaruvchini e'lon qilish

## Topshiriq sharti:
extern orqali boshqa joyda yaratilgan o'zgaruvchini qanday ishlatilishini simulyatsiya qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

// Global o'zgaruvchi ta'rifi (xotira ajratiladi)
int global_tizim_kodi = 99;

void funksiya_tekshiruv(void) {
    // extern faqat e'lon qiladi (xotira ajratmaydi)
    extern int global_tizim_kodi;
    printf("Tizim kodi: %d\n", global_tizim_kodi);
}

int main(void) {
    funksiya_tekshiruv();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `extern` kompilyatorga: 'bu o'zgaruvchi allaqachon mavjud, faqat unga murojaat qilishimga ruxsat ber' deydi.
2. Sarlavha (.h) fayllarda global o'zgaruvchilar faqat `extern` bilan e'lon qilinadi.

## Ishlash natijasi:
```text
Tizim kodi: 99
```

---

# 222-Topshiriq: register kalit so'zi va uning maqsadi

## Topshiriq sharti:
register orqali tez-tez aylanuvchi hisoblagichni belgilang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    register int hisoblagich = 0;
    for (int i = 0; i < 1000; i++) {
        hisoblagich += 1;
    }
    printf("Yakuniy hisoblagich: %d\n", hisoblagich);
    // &hisoblagich qilish C da man etiladi, chunki CPU registrining RAM manzili yo'q!
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `register` kompilyatorga o'zgaruvchini RAM ga emas, bevosita CPU registriga joylashtirishni tavsiya qiladi.
2. Eng muhim qoida: `register` o'zgaruvchining manzilini (`&`) olib bo'lmaydi!

## Ishlash natijasi:
```text
Yakuniy hisoblagich: 1000
```

---

# 223-Topshiriq: inline funksiyalar (C99): Chaqiruv xarajatini kamaytirish

## Topshiriq sharti:
inline funksiya orqali ikkita son kvadratlari yig'indisini hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

static inline int kvadratlar_yigindisi(int a, int b) {
    return (a * a) + (b * b);
}

int main(void) {
    int res = kvadratlar_yigindisi(3, 4);
    printf("3^2 + 4^2 = %d\n", res);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `inline` kalit so'zi kompilyatorga funksiya tanasini chaqiruv joyiga to'g'ridan-to'g'ri ko'chirib qo'yishni maslahat beradi.
2. Bu funksiya chaqirish, parametr uzatish va qaytish kabi stek xarajatlarini (call overhead) yo'qotadi.

## Ishlash natijasi:
```text
3^2 + 4^2 = 25
```

---

# 224-Topshiriq: Stack Frame (Chaqiruv steki kadri) tahlili

## Topshiriq sharti:
Ichma-ich chaqirilgan uchta funksiyaning stek kadrlarini vizual tasavvur qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

void funksiya_c(int c_val) {
    printf("   [Frame C] c_val manzili: %p\n", (void*)&c_val);
}

void funksiya_b(int b_val) {
    printf("  [Frame B] b_val manzili: %p\n", (void*)&b_val);
    funksiya_c(b_val + 1);
}

void funksiya_a(int a_val) {
    printf(" [Frame A] a_val manzili: %p\n", (void*)&a_val);
    funksiya_b(a_val + 1);
}

int main(void) {
    int main_val = 10;
    printf("[Main Frame] main_val manzili: %p\n", (void*)&main_val);
    funksiya_a(main_val);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir funksiya chaqirilganda stek ustiga yangi Stack Frame (lokal o'zgaruvchilar, parametrlar, return address) qo'shiladi.
2. Stek manzillari x86/ARM tizimlarida yuqoridan pastga (kamayib) boradi.

## Ishlash natijasi:
```text
[Main Frame] main_val manzili: 000000000012FFE4
 [Frame A] a_val manzili: 000000000012FFB0
  [Frame B] b_val manzili: 000000000012FF80
   [Frame C] c_val manzili: 000000000012FF50
```

---

# 225-Topshiriq: Stack Overflow halokati va uni oldini olish

## Topshiriq sharti:
Rekursiya chuqurligini cheklash orqali stek to'lib ketishidan saqlaning.

## Yechim (C kodi):
```c
#include <stdio.h>

#define MAX_CHUQURLIK 1000

void xavfsiz_rekursiya(int qadam) {
    if (qadam > MAX_CHUQURLIK) {
        printf("Ogohlantirish: Cheklovga yetildi (%d), to'xtatildi!\n", qadam);
        return;
    }
    if (qadam % 250 == 0) {
        printf("Qadam: %d\n", qadam);
    }
    xavfsiz_rekursiya(qadam + 1);
}

int main(void) {
    xavfsiz_rekursiya(1);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Stek xotira hajmi cheklangan (odatda 1 MB dan 8 MB gacha).
2. To'xtovsiz rekursiya tezda barcha stekni egallab, operatsion tizim tomonidan dasturning majburiy to'xtatilishiga (Segmentation Fault / Stack Overflow) olib keladi.

## Ishlash natijasi:
```text
Qadam: 250
Qadam: 500
Qadam: 750
Qadam: 1000
Ogohlantirish: Cheklovga yetildi (1001), to'xtatildi!
```

---

# 226-Topshiriq: stdarg.h: O'zgaruvchan sondagi argumentlar (Variadic functions)

## Topshiriq sharti:
Ixtiyoriy miqdordagi butun sonlar yig'indisini hisoblovchi funksiya yozing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdarg.h>

int variadic_yigindi(int soni, ...) {
    va_list args;
    va_start(args, soni);

    int jami = 0;
    for (int i = 0; i < soni; i++) {
        jami += va_arg(args, int);
    }

    va_end(args);
    return jami;
}

int main(void) {
    printf("3 ta son yig'indisi: %d\n", variadic_yigindi(3, 10, 20, 30));
    printf("5 ta son yig'indisi: %d\n", variadic_yigindi(5, 1, 2, 3, 4, 5));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `...` (ellips) o'zgaruvchan parametrlar borligini bildiradi.
2. `va_list` argumentlar ro'yxatini ushlaydi, `va_start` boshlaydi, `va_arg` navbatdagi elementni belgilangan turda o'qiydi, `va_end` tozalaydi.

## Ishlash natijasi:
```text
3 ta son yig'indisi: 60
5 ta son yig'indisi: 15
```

---

# 227-Topshiriq: O'z mini-printf funksiyangizni yozish (%d va %s formati bilan)

## Topshiriq sharti:
stdarg.h yordamida soddalashtirilgan mini_printf yarating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdarg.h>

void mini_printf(const char *format, ...) {
    va_list args;
    va_start(args, format);

    for (const char *p = format; *p != '\0'; p++) {
        if (*p != '%') {
            putchar(*p);
            continue;
        }
        p++; // '%' dan keyingi belgiga o'tish
        switch (*p) {
            case 'd': {
                int i = va_arg(args, int);
                printf("%d", i);
                break;
            }
            case 's': {
                char *s = va_arg(args, char *);
                fputs(s, stdout);
                break;
            }
            case '%':
                putchar('%');
                break;
        }
    }
    va_end(args);
}

int main(void) {
    mini_printf("Salom, %s! Sizning ballingiz: %d%%\n", "Sardor", 95);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Haqiqiy `printf` ning ichki ishlash mexanizmi aynan mana shu format satrini tahlil qilish va `va_arg` orqali parametrlarni o'qishga asoslangan.

## Ishlash natijasi:
```text
Salom, Sardor! Sizning ballingiz: 95%
```

---

# 228-Topshiriq: Variadic funksiya bilan sonlarning o'rtacha arifmetigini topish

## Topshiriq sharti:
Ixtiyoriy miqdordagi double sonlarning o'rtacha qiymatini hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdarg.h>

double orta_arifmetik(int soni, ...) {
    if (soni <= 0) return 0.0;
    va_list ap;
    va_start(ap, soni);

    double sum = 0.0;
    for (int i = 0; i < soni; i++) {
        sum += va_arg(ap, double);
    }
    va_end(ap);
    return sum / soni;
}

int main(void) {
    printf("O'rtacha: %.2lf\n", orta_arifmetik(4, 2.5, 3.5, 4.0, 6.0));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. (2.5 + 3.5 + 4.0 + 6.0) / 4 = 16.0 / 4 = 4.00.

## Ishlash natijasi:
```text
O'rtacha: 4.00
```

---

# 229-Topshiriq: Funksiyadan ko'rsatkich (Pointer) qaytarish qoidalari

## Topshiriq sharti:
Massivdagi maksimal elementning ko'rsatkichini qaytaruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

int* top_maksimum_ptr(int massiv[], int olcham) {
    if (olcham <= 0) return NULL;
    int *max_ptr = &massiv[0];
    for (int i = 1; i < olcham; i++) {
        if (massiv[i] > *max_ptr) {
            max_ptr = &massiv[i];
        }
    }
    return max_ptr;
}

int main(void) {
    int sonlar[] = {12, 45, 89, 23};
    int *ptr = top_maksimum_ptr(sonlar, 4);

    if (ptr != NULL) {
        printf("Maksimal qiymat: %d, xotira manzili: %p\n", *ptr, (void*)ptr);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tashqaridan berilgan massiv elementining manzilini qaytarish xavfsiz, chunki uning xotirasi `main` funktsiyasi davomida mavjud bo'ladi.

## Ishlash natijasi:
```text
Maksimal qiymat: 89, xotira manzili: 000000000012FFE8
```

---

# 230-Topshiriq: Lokal avtomatik o'zgaruvchi manzilini qaytarish xatosi (Dangling pointer)

## Topshiriq sharti:
Nima uchun lokal o'zgaruvchi ko'rsatkichini qaytarish qat'iyan taqiqlanishini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

// XAVFLI KOD:
// int* xavfli_funksiya() {
//     int lokal = 42;
//     return &lokal; // OGOHLANTIRISH: function returns address of local variable
// }

int main(void) {
    printf("Lokal avtomatik o'zgaruvchi funksiya tugashi bilan o'chiriladi!\n");
    printf("Uning manzilini qaytarish — Dangling pointer va jiddiy xavfsizlik zaifligidir.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Lokal o'zgaruvchi stekda yashaydi. Funksiya tugashi bilan uning stek kadri yo'q qilinadi va bu xotira boshqa funksiyalarga beriladi.
2. Dangling pointer ustida amal bajarish dasturning yashirin buzilishiga sabab bo'ladi.

## Ishlash natijasi:
```text
Lokal avtomatik o'zgaruvchi funksiya tugashi bilan o'chiriladi!
Uning manzilini qaytarish — Dangling pointer va jiddiy xavfsizlik zaifligidir.
```

---

# 231-Topshiriq: Statik o'zgaruvchi manzilini xavfsiz qaytarish

## Topshiriq sharti:
static o'zgaruvchi orqali funksiyadan xavfsiz pointer qaytarish.

## Yechim (C kodi):
```c
#include <stdio.h>

const char* status_matni(int kod) {
    static const char *muvaffaqiyat = "OK: Bajarildi";
    static const char *xatolik = "ERROR: Xato yuz berdi";

    if (kod == 0) return muvaffaqiyat;
    return xatolik;
}

int main(void) {
    printf("Status: %s\n", status_matni(0));
    printf("Status: %s\n", status_matni(1));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `static` o'zgaruvchilar dastur tugaguncha doimiy yashaydi, shuning uchun ularning ko'rsatkichini qaytarish mutlaqo xavfsizdir.

## Ishlash natijasi:
```text
Status: OK: Bajarildi
Status: ERROR: Xato yuz berdi
```

---

# 232-Topshiriq: Dinamik ajratilgan xotira manzilini funksiyadan qaytarish

## Topshiriq sharti:
malloc orqali xotira ajratib manzilini qaytaruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int* son_yarat(int qiymat) {
    int *p = (int*)malloc(sizeof(int));
    if (p != NULL) {
        *p = qiymat;
    }
    return p;
}

int main(void) {
    int *ptr = son_yarat(777);
    if (ptr != NULL) {
        printf("Dinamik yaratilgan qiymat: %d\n", *ptr);
        free(ptr); // Xotirani tozalash chaqiruvchining burchidir
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Heap xotirada ajratilgan ma'lumot funksiya tugasa ham saqlanadi.
2. Qoida: xotirani kim ajratgan bo'lsa, oxirida uni `free()` qilish mas'uliyati chaqiruvchi koddadir.

## Ishlash natijasi:
```text
Dinamik yaratilgan qiymat: 777
```

---

# 233-Topshiriq: _Noreturn funksiya spetsifikatori (C11): Qaytmaydigan funksiyalar

## Topshiriq sharti:
_Noreturn orqali dasturni to'xtatuvchi xatolik funksiyasini belgilang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdnoreturn.h>

noreturn void halokatli_xato(const char *xabar) {
    printf("FATAL ERROR: %s\n", xabar);
    exit(EXIT_FAILURE); // Hech qachon main ga qaytmaydi
}

int main(void) {
    printf("Dastur boshlandi...\n");
    // halokatli_xato("Tizimda xato!");
    printf("Kompilyator qaytmaydigan funksiyalarni optimallashtiradi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C11 da kiritilgan `_Noreturn` kompilyatorga ushbu funksiya hech qachon chaqiruv joyiga qaytmasligini bildiradi.
2. Bu keraksiz qaytish kodlarini olib tashlash orqali optimallashtirish imkonini beradi.

## Ishlash natijasi:
```text
Dastur boshlandi...
Kompilyator qaytmaydigan funksiyalarni optimallashtiradi.
```

---

# 234-Topshiriq: Funksiyalarni modulli tashkil etish (.h va .c fayllarga ajratish falsafasi)

## Topshiriq sharti:
Sarlavha fayllari va amalga oshirish fayllari arxitekturasini kodda ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

// matematika.h sarlavhasining simulyatsiyasi:
typedef struct {
    double x, y;
} Nuqta;

Nuqta nuqta_yarat(double x, double y) {
    Nuqta p = {x, y};
    return p;
}

void nuqta_chop_et(Nuqta p) {
    printf("Nuqta(x: %.1lf, y: %.1lf)\n", p.x, p.y);
}

int main(void) {
    Nuqta a = nuqta_yarat(3.5, 7.2);
    nuqta_chop_et(a);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sanoat C loyihalarida funksiya deklaratsiyasi `.h` faylga, uning kodi esa `.c` faylga ajratiladi.
2. Bu kodning qayta ishlatilishi va jamoaviy dasturlashni ta'minlaydi.

## Ishlash natijasi:
```text
Nuqta(x: 3.5, y: 7.2)
```

---

# 235-Topshiriq: Rekursiv ikkilik qidiruv (Binary Search) algoritmi

## Topshiriq sharti:
Saralangan massiv ichidan elementni rekursiv O(log N) da toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int rekursiv_binar_qidiruv(const int arr[], int chap, int ong, int nishon) {
    if (chap > ong) return -1; // Topilmadi

    int orta = chap + (ong - chap) / 2;

    if (arr[orta] == nishon) return orta;
    if (arr[orta] > nishon) {
        return rekursiv_binar_qidiruv(arr, chap, orta - 1, nishon);
    }
    return rekursiv_binar_qidiruv(arr, orta + 1, ong, nishon);
}

int main(void) {
    int saralangan[] = {11, 22, 33, 44, 55, 66, 77};
    int qidirilayotgan = 44;
    int indeks = rekursiv_binar_qidiruv(saralangan, 0, 6, qidirilayotgan);

    printf("%d soni %d-indeksda joylashgan.\n", qidirilayotgan, indeks);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir chaqiruvda qidiruv maydoni teng ikkiga bo'linadi.
2. 44 soni massivning 3-indeksida turibdi.

## Ishlash natijasi:
```text
44 soni 3-indeksda joylashgan.
```

---

# 236-Topshiriq: Rekursiya bilan massiv elementlari yig'indisini topish

## Topshiriq sharti:
Massivni bo'laklarga bo'lib rekursiv yig'indisini hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

int massiv_yigindi_rekursiv(const int arr[], int n) {
    if (n <= 0) return 0;
    return arr[n - 1] + massiv_yigindi_rekursiv(arr, n - 1);
}

int main(void) {
    int arr[] = {5, 10, 15, 20};
    printf("Rekursiv yig'indi: %d\n", massiv_yigindi_rekursiv(arr, 4));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 20 + yigindi(3) -> 20 + 15 + yigindi(2) ... = 50.

## Ishlash natijasi:
```text
Rekursiv yig'indi: 50
```

---

# 237-Topshiriq: Rekursiya bilan massivdagi maksimal elementni topish

## Topshiriq sharti:
Ikkiga bo'lib qidirish (Divide and Conquer) orqali maksimal elementni toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int rekursiv_max(const int arr[], int chap, int ong) {
    if (chap == ong) return arr[chap];

    int orta = (chap + ong) / 2;
    int max1 = rekursiv_max(arr, chap, orta);
    int max2 = rekursiv_max(arr, orta + 1, ong);

    return (max1 > max2) ? max1 : max2;
}

int main(void) {
    int arr[] = {18, 45, 9, 72, 33, 61};
    printf("Massivdagi eng katta qiymat: %d\n", rekursiv_max(arr, 0, 5));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Massiv ikkiga bo'linadi, har bir bo'lakning maksimallari taqqoslanadi.
2. Natijada 72 eng katta qiymat deb topiladi.

## Ishlash natijasi:
```text
Massivdagi eng katta qiymat: 72
```

---

# 238-Topshiriq: Palindrom satrni rekursiv tekshirish

## Topshiriq sharti:
Satrning bosh va oxirgi harflarini rekursiv qisqartirib tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool palindrom_rekursiv(const char *s, int chap, int ong) {
    if (chap >= ong) return true;
    if (s[chap] != s[ong]) return false;
    return palindrom_rekursiv(s, chap + 1, ong - 1);
}

int main(void) {
    char s1[] = "radari"; // radar
    char s2[] = "kiyik";
    printf("'%s' palindrommi: %s\n", s2, palindrom_rekursiv(s2, 0, strlen(s2) - 1) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar birinchi va oxirgi belgi teng bo'lsa, ichki qism tekshiriladi: 'kiyik' -> 'iyi' -> 'y'.

## Ishlash natijasi:
```text
'kiyik' palindrommi: Ha
```

---

# 239-Topshiriq: Rekursiv sonni ikkilik sanoq sistemasida chop etish

## Topshiriq sharti:
Qoldiqlarni teskari chiqarishni rekursiya steki orqali bajaring.

## Yechim (C kodi):
```c
#include <stdio.h>

void rekursiv_binar(unsigned int n) {
    if (n > 1) {
        rekursiv_binar(n / 2);
    }
    printf("%d", n % 2);
}

int main(void) {
    printf("13 ikkilikda: ");
    rekursiv_binar(13);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Avval rekursiv chaqiruv bo'ladi, so'ngra chop etiladi.
2. Bu massivsiz teskari tartibda binar chiqarishning eng nafis usulidir.

## Ishlash natijasi:
```text
13 ikkilikda: 1101
```

---

# 240-Topshiriq: Akerman (Ackermann) funksiyasi — Chuqur rekursiya klassikasi

## Topshiriq sharti:
O'ta tez o'suvchi Akerman funksiyasining A(2, 2) qiymatini hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

int ackermann(int m, int n) {
    if (m == 0) return n + 1;
    if (m > 0 && n == 0) return ackermann(m - 1, 1);
    return ackermann(m - 1, ackermann(m, n - 1));
}

int main(void) {
    printf("Ackermann(2, 2) = %d\n", ackermann(2, 2));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Akerman funksiyasi nazariy kompyuter fanida oddiy ibtidoiy rekursiv bo'lmagan, lekin to'liq hisoblanuvchi funksiya namunasi hisoblanadi.

## Ishlash natijasi:
```text
Ackermann(2, 2) = 7
```

---

# 241-Topshiriq: Funksiya parametrlarida const qo'llash (O'qish xavfsizligi)

## Topshiriq sharti:
Funksiyaga uzatilgan massivni o'zgarishdan himoya qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

void xavfsiz_chop(const int *arr, int len) {
    for (int i = 0; i < len; i++) {
        // arr[i] = 0; // Kompilyatsiya xatosi: assignment of read-only location
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main(void) {
    int data[] = {1, 2, 3};
    xavfsiz_chop(data, 3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const int *arr` parametrlari funksiya ichida ma'lumotlar faqat o'qilishini kafolatlaydi.

## Ishlash natijasi:
```text
1 2 3
```

---

# 242-Topshiriq: Funksiya orqali bir vaqtning o'zida bir nechta natija qaytarish (Output parameters)

## Topshiriq sharti:
Bitta funksiyada bo'linma va qoldiqni birgalikda qaytaring.

## Yechim (C kodi):
```c
#include <stdio.h>

void bolish_va_qoldiq(int bolinuvchi, int boluvchi, int *bolinma, int *qoldiq) {
    if (boluvchi != 0) {
        *bolinma = bolinuvchi / boluvchi;
        *qoldiq = bolinuvchi % boluvchi;
    }
}

int main(void) {
    int b, q;
    bolish_va_qoldiq(23, 5, &b, &q);
    printf("23 / 5 = %d, qoldiq = %d\n", b, q);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkich parametrlari orqali funksiya tashqaridagi bir nechta o'zgaruvchilarga natijalarni yozib berishi mumkin.

## Ishlash natijasi:
```text
23 / 5 = 4, qoldiq = 3
```

---

# 243-Topshiriq: Sof funksiyalar (Pure functions) va ularning afzalliklari

## Topshiriq sharti:
Tashqi global holatga bog'liq bo'lmagan deterministik funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

// Sof funksiya: har doim bir xil argumentga bir xil natija beradi, yon ta'siri yo'q
int sof_qoshish(int a, int b) {
    return a + b;
}

int main(void) {
    printf("5 + 7 = %d\n", sof_qoshish(5, 7));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sof funksiyalarni testlash, keshlash (memoization) va ko'p oqimli dasturlashda ishlatish o'ta oson va xavfsizdir.

## Ishlash natijasi:
```text
5 + 7 = 12
```

---

# 244-Topshiriq: Katta hajmdagi ma'lumotlarni qiymat bo'yicha emas, const pointer bilan uzatish

## Topshiriq sharti:
Nusxalash xarajatlarini yo'qotuvchi pass-by-const-pointer uslubi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    double mat[100];
} KattaObyekt;

void obyektni_ishla(const KattaObyekt *obj) {
    printf("Birinchi element: %.1lf\n", obj->mat[0]);
}

int main(void) {
    KattaObyekt o = {{42.5}};
    obyektni_ishla(&o); // Faqat 8 baytli ko'rsatkich uzatiladi (800 bayt nusxalanmaydi!)
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta ob'ektlarni qiymat bo'yicha uzatish butun xotirani stekka nusxalashni talab qiladi.
2. `const T*` orqali uzatish nusxalash xarajatini 0 ga tushiradi.

## Ishlash natijasi:
```text
Birinchi element: 42.5
```

---

# 245-Topshiriq: Rekursiyani iteratsiyaga aylantirish texnikasi (Qo'lda stek boshqaruvi)

## Topshiriq sharti:
Faktorialni rekursiyasiz, oddiy akkumulyator sikliga aylantirish.

## Yechim (C kodi):
```c
#include <stdio.h>

long long iterativ_faktorial(int n) {
    long long res = 1;
    while (n > 1) {
        res *= n;
        n--;
    }
    return res;
}

int main(void) {
    printf("Iterativ faktorial(5) = %lld\n", iterativ_faktorial(5));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har qanday rekursiv funksiyani sikl va yordamchi stek yordamida iterativ shaklga o'tkazish mumkin.

## Ishlash natijasi:
```text
Iterativ faktorial(5) = 120
```

---

# 246-Topshiriq: Standart xatolik kodini qaytarish an'anasi (Error codes)

## Topshiriq sharti:
0 muvaffaqiyat, manfiy sonlar xatolik ekanligini bildiruvchi funksiya arxitekturasi.

## Yechim (C kodi):
```c
#include <stdio.h>

#define ERR_OK           0
#define ERR_NULL_PTR    -1
#define ERR_MANFIY_YOSH -2

int foydalanuvchi_tekshir(const char *ism, int yosh) {
    if (ism == NULL) return ERR_NULL_PTR;
    if (yosh < 0) return ERR_MANFIY_YOSH;
    return ERR_OK;
}

int main(void) {
    int res = foydalanuvchi_tekshir("Botir", -5);
    if (res == ERR_OK) {
        printf("Ma'lumotlar to'g'ri!\n");
    } else {
        printf("Xatolik kodi: %d\n", res);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da istisnolar (Exceptions) yo'q; barcha funksiyalar xatolik holatini butun sonli kod sifatida qaytaradi (Unix standarti).

## Ishlash natijasi:
```text
Xatolik kodi: -2
```

---

# 247-Topshiriq: Chaqiruvlar zanjiri (Call chain) va hisoblash kaskadi

## Topshiriq sharti:
Uchta funksiyani zanjirband chaqirib natijani qayta ishlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int oshir(int x) { return x + 1; }
int ikki_karra(int x) { return x * 2; }
int kvadrat(int x) { return x * x; }

int main(void) {
    // ( (5 + 1) * 2 ) ^ 2 = (6 * 2)^2 = 12^2 = 144
    int natija = kvadrat(ikki_karra(oshir(5)));
    printf("Zanjir natijasi: %d\n", natija);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiya qaytargan qiymat bevosita keyingi funksiyaning argumenti bo'lib xizmat qiladi.

## Ishlash natijasi:
```text
Zanjir natijasi: 144
```

---

# 248-Topshiriq: Rekursiv kombinatorika: N elementdan K tasini tanlash (C(n, k))

## Topshiriq sharti:
Paskal qoidasi bo'yicha C(n, k) = C(n-1, k-1) + C(n-1, k) ni hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

long long kombinatsiya(int n, int k) {
    if (k == 0 || k == n) return 1;
    return kombinatsiya(n - 1, k - 1) + kombinatsiya(n - 1, k);
}

int main(void) {
    printf("C(5, 2) = %lld\n", kombinatsiya(5, 2));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 5 elementdan 2 tasini tanlash usullari soni: 5! / (2! * 3!) = 10.

## Ishlash natijasi:
```text
C(5, 2) = 10
```

---

# 249-Topshiriq: Bo'lib-tashla-va-hukmronlik-qil (Divide and Conquer) falsafasi

## Topshiriq sharti:
Masalani ikkita kichikroq qism-masalaga bo'lib yechish namoyishi.

## Yechim (C kodi):
```c
#include <stdio.h>

int yigindi_bolib_tashla(const int arr[], int chap, int ong) {
    if (chap == ong) return arr[chap];
    int orta = (chap + ong) / 2;
    return yigindi_bolib_tashla(arr, chap, orta) + 
           yigindi_bolib_tashla(arr, orta + 1, ong);
}

int main(void) {
    int sonlar[] = {1, 2, 3, 4, 5, 6};
    printf("Bo'lib-tashla yig'indisi: %d\n", yigindi_bolib_tashla(sonlar, 0, 5));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Divide and Conquer yondashuvi Merge Sort va Fast Fourier Transform (FFT) kabi ko'plab qudratli algoritmlarning asosidir.

## Ishlash natijasi:
```text
Bo'lib-tashla yig'indisi: 21
```

---

# 250-Topshiriq: Modul yakuni: Arifmetik ifodani hisoblovchi rekursiv tahlilchi (Recursive Parser)

## Topshiriq sharti:
Qo'shish va ko'paytirish qoidalarini bajaruvchi sodda ifoda kalkulyatori.

## Yechim (C kodi):
```c
#include <stdio.h>

// Oddiy ifoda: "2+3*4" ni hisoblaydi
int hisobla_kopaytirish(const char **s);

int hisobla_qoshish(const char **s) {
    int natija = hisobla_kopaytirish(s);
    while (**s == '+') {
        (*s)++; // '+' ni o'tkazish
        natija += hisobla_kopaytirish(s);
    }
    return natija;
}

int hisobla_kopaytirish(const char **s) {
    int natija = **s - '0';
    (*s)++;
    while (**s == '*') {
        (*s)++; // '*' ni o'tkazish
        natija *= (**s - '0');
        (*s)++;
    }
    return natija;
}

int main(void) {
    const char *ifoda = "2+3*4+5";
    const char *p = ifoda;
    int res = hisobla_qoshish(&p);
    printf("Ifoda '%s' natijasi: %d\n", ifoda, res);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Recursive Descent Parsing kompilyatorlarning sintaktik tahlil (AST) bosqichida qo'llaniladi.
2. 2 + (3 * 4) + 5 = 2 + 12 + 5 = 19 natijasini to'g'ri hisoblaydi.
3. Bu 5-qismning barcha funksiya, ko'rsatkich va rekursiya bilimlarini umumlashtiradi.

## Ishlash natijasi:
```text
Ifoda '2+3*4+5' natijasi: 19
```

---
