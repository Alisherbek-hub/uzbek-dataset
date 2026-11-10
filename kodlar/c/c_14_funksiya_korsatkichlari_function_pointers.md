# C Dasturlash Tili — 14-Qism: Funksiya Ko'rsatkichlari (Function Pointers)
## (651-700 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* Funksiya ko'rsatkichlari deklaratsiyasi, manzili va typedef bilan soddalashtirish
* Callback mexanizmi va for_each algoritmi
* Standart qsort() va comparatorlar (int, double, string, struct)
* bsearch() binar qidiruv va Sakrash jadvali (Jump Table / O(1) Calculator)
* Funksiyadan funksiya ko'rsatkichi qaytarish va Virtual Metodlar Jadvali (vtable)
* Funktsional dasturlash: map, filter, reduce va Event Hook tizimi
* User context (void *user_data), signal() boshqaruvi va Event-Driven GUI Engine

---

# 651-Topshiriq: Funksiya ko'rsatkichi (Function Pointer) deklaratsiyasi va chaqiruvi

## Topshiriq sharti:
Oddiy funksiyaga ko'rsatkich e'lon qilish, unga funksiya manzilini biriktirish va chaqirish.

## Yechim (C kodi):
```c
#include <stdio.h>

void salom(void) {
    printf("Salom, Dunyo!\n");
}

int main(void) {
    // Funksiya ko'rsatkichi deklaratsiyasi
    void (*ptr)(void) = salom;

    // Ikkala usulda chaqirish:
    ptr();    // To'g'ridan-to'g'ri sintaksis
    (*ptr)(); // An'anaviy dereference sintaksisi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 'void (*ptr)(void)' sintaksisida qavslar majburiydir, aks holda 'void *ptr(void)' — pointer qaytaruvchi funksiya bo'lib qoladi.
2. C tilida funksiya nomi massiv nomi kabi o'z-o'zidan uning xotiradagi boshlang'ich manzilini bildiradi.

## Ishlash natijasi:
```text
Salom, Dunyo!
Salom, Dunyo!
```

---

# 652-Topshiriq: Argument qabul qiluvchi va qiymat qaytaruvchi funksiya ko'rsatkichi

## Topshiriq sharti:
Ikkita int qabul qilib int qaytaruvchi funksiya pointeri.

## Yechim (C kodi):
```c
#include <stdio.h>

int qoshish(int a, int b) {
    return a + b;
}

int kopaytirish(int a, int b) {
    return a * b;
}

int main(void) {
    int (*amal)(int, int);

    amal = qoshish;
    printf("Yig'indi: %d\n", amal(10, 20));

    amal = kopaytirish;
    printf("Ko'paytma: %d\n", amal(10, 20));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitta funksiya ko'rsatkichiga imzosi (qaytuvchi tipi va argumentlari) bir xil bo'lgan istalgan funksiya manzilini berish mumkin.
2. Bu dinamik xulq-atvorni (polimorfizmni) amalga oshirishning poydevoridir.

## Ishlash natijasi:
```text
Yig'indi: 30
Ko'paytma: 200
```

---

# 653-Topshiriq: typedef yordamida funksiya ko'rsatkichini soddalashtirish

## Topshiriq sharti:
typedef yordamida murakkab funksiya pointeri sintaksisini tushunarli tipga aylantirish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef int (*ArifmetikAmal)(int, int);

int ayirish(int a, int b) {
    return a - b;
}

int main(void) {
    ArifmetikAmal op = ayirish;
    printf("Ayirma: %d\n", op(50, 18));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. typedef orqali yaratilgan ArifmetikAmal tipi endi oddiy tip (int, double kabi) ko'rinishida ishlatiladi.
2. Bu kodni o'qishni va funksiya argumentlarida foydalanishni ancha osonlashtiradi.

## Ishlash natijasi:
```text
Ayirma: 32
```

---

# 654-Topshiriq: Callback mexanizmi: Funksiyani boshqa funksiyaga argument sifatida uzatish

## Topshiriq sharti:
Massiv har bir elementiga berilgan amaliyotni qo'llovchi umumiy for_each funksiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef void (*AmalCallback)(int);

void chop_kvadrat(int n) {
    printf("%d^2 = %d\n", n, n * n);
}

void chop_kub(int n) {
    printf("%d^3 = %d\n", n, n * n * n);
}

void for_each(int *arr, int len, AmalCallback cb) {
    for (int i = 0; i < len; i++) {
        cb(arr[i]);
    }
}

int main(void) {
    int sonlar[] = {1, 2, 3, 4};
    printf("Kvadratlar:\n");
    for_each(sonlar, 4, chop_kvadrat);

    printf("Kublar:\n");
    for_each(sonlar, 4, chop_kub);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Callback — boshqa funksiya tomonidan chaqirilishi uchun argument sifatida beriladigan funksiya ko'rsatkichidir.
2. for_each algoritmi massivni aylanib chiqish vazifasini bajaradi, har bir element bilan nima qilishni esa callback belgilaydi.

## Ishlash natijasi:
```text
Kvadratlar:
1^2 = 1
2^2 = 4
3^2 = 9
4^2 = 16
Kublar:
1^3 = 1
2^3 = 8
3^3 = 27
4^3 = 64
```

---

# 655-Topshiriq: Standart qsort() va butun sonlarni tartiblash

## Topshiriq sharti:
stdlib.h kutubxonasidagi qsort funksiyasi uchun int solishtiruvchi (comparator) yozish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int int_osish(const void *a, const void *b) {
    int val_a = *(const int *)a;
    int val_b = *(const int *)b;
    return (val_a > val_b) - (val_a < val_b); // Xavfsiz solishtirish
}

int main(void) {
    int sonlar[] = {42, 12, 88, 3, 27, 99, 1};
    int n = sizeof(sonlar) / sizeof(sonlar[0]);

    qsort(sonlar, n, sizeof(int), int_osish);

    printf("Tartiblangan sonlar: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", sonlar[i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. qsort 'int (*compar)(const void *, const void *)' imzoli callback qabul qiladi.
2. Manfiy qiymat qaytsa a < b, 0 qaytsa a == b, musbat qaytsa a > b deb hisoblanadi. (val_a > val_b) - (val_a < val_b) formulasi integer overflow xatosidan saqlaydi.

## Ishlash natijasi:
```text
Tartiblangan sonlar: 1 3 12 27 42 88 99
```

---

# 656-Topshiriq: qsort() yordamida kamayish tartibida saralash

## Topshiriq sharti:
Comparator mantiqini teskari qilish orqali massivni kamayish bo'yicha tartiblash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int int_kamayish(const void *a, const void *b) {
    int val_a = *(const int *)a;
    int val_b = *(const int *)b;
    return (val_b > val_a) - (val_b < val_a);
}

int main(void) {
    int arr[] = {5, 9, 1, 3, 8};
    int n = 5;

    qsort(arr, n, sizeof(int), int_kamayish);

    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Argumentlar o'rnini almashtirish orqali saralash yo'nalishini bir zumda teskari qilish mumkin.

## Ishlash natijasi:
```text
9 8 5 3 1
```

---

# 657-Topshiriq: qsort() bilan suzuvchi nuqtali (double) sonlarni saralash

## Topshiriq sharti:
double sonlarni solishtirishda ayirmani int ga to'g'ridan-to'g'ri cast qilish xatosini oldini olish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int double_solishtir(const void *a, const void *b) {
    double da = *(const double *)a;
    double db = *(const double *)b;
    if (da < db) return -1;
    if (da > db) return 1;
    return 0;
}

int main(void) {
    double d[] = {3.14, 1.41, 2.71, 0.58, 1.73};
    int n = 5;

    qsort(d, n, sizeof(double), double_solishtir);

    for (int i = 0; i < n; i++) {
        printf("%.2f ", d[i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar `return (int)(da - db);` qilinsa, 0.5 kabi kichik farqlar 0 ga aylanib xato tartiblashga olib keladi.
2. Aniq `if (da < db)` shartlari suzuvchi nuqtali sonlarda yagona to'g'ri yondashuvdir.

## Ishlash natijasi:
```text
0.58 1.41 1.73 2.71 3.14
```

---

# 658-Topshiriq: qsort() bilan satrlar (strings) massivini alifbo bo'yicha saralash

## Topshiriq sharti:
const char* massivini strcmp yordamida tartiblash (pointer to pointer tushunchasi).

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int satr_solishtir(const void *a, const void *b) {
    // a va b massiv elementlarining manzili, ya'ni const char** ko'rsatkich
    const char *s1 = *(const char **)a;
    const char *s2 = *(const char **)b;
    return strcmp(s1, s2);
}

int main(void) {
    const char *shaharlar[] = {"Toshkent", "Samarqand", "Buxoro", "Xiva", "Andijon"};
    int n = 5;

    qsort(shaharlar, n, sizeof(const char *), satr_solishtir);

    for (int i = 0; i < n; i++) {
        printf("%s ", shaharlar[i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Stringlar massivini saralashda har bir element `char*` bo'lgani uchun qsort comparatoriga `char**` keladi.
2. *(const char **)a qilib haqiqiy satr manzilini olamiz va strcmp ga beramiz.

## Ishlash natijasi:
```text
Andijon Buxoro Samarqand Toshkent Xiva
```

---

# 659-Topshiriq: qsort() bilan strukturalar massivini saralash

## Topshiriq sharti:
Talabalar strukturasini bahosi (yoki yoshi) bo'yicha saralash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char ism[20];
    int ball;
} Talaba;

int talaba_solishtir(const void *a, const void *b) {
    const Talaba *t1 = (const Talaba *)a;
    const Talaba *t2 = (const Talaba *)b;
    // Yuqori balldan past ballga qarab (kamayish)
    return (t2->ball - t1->ball);
}

int main(void) {
    Talaba guruh[] = {
        {"Ali", 85},
        {"Vali", 92},
        {"Zuhra", 78},
        {"Anvar", 95}
    };
    int n = 4;

    qsort(guruh, n, sizeof(Talaba), talaba_solishtir);

    for (int i = 0; i < n; i++) {
        printf("%s: %d ball\n", guruh[i].ism, guruh[i].ball);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Strukturalar massivini saralashda void ko'rsatkichi to'g'ridan-to'g'ri `const Talaba*` ga o'giriladi.
2. Ma'lumotlar bazasi indekslari va hisobot jadvallari aynan shunday saralanadi.

## Ishlash natijasi:
```text
Anvar: 95 ball
Vali: 92 ball
Ali: 85 ball
Zuhra: 78 ball
```

---

# 660-Topshiriq: bsearch() binar qidiruv funksiyasida comparator callback

## Topshiriq sharti:
Tartiblangan massivdan elementni O(log N) vaqtda topish uchun bsearch() dan foydalanish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int cmp_int(const void *a, const void *b) {
    return (*(const int *)a - *(const int *)b);
}

int main(void) {
    int sonlar[] = {10, 20, 30, 40, 50, 60, 70, 80};
    int n = sizeof(sonlar) / sizeof(sonlar[0]);
    int kalit = 50;

    int *topilgan = (int *)bsearch(&kalit, sonlar, n, sizeof(int), cmp_int);

    if (topilgan != NULL) {
        printf("Element topildi: %d (Indeks: %td)\n", *topilgan, topilgan - sonlar);
    } else {
        printf("Element topilmadi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. bsearch() massivdan qidiruv kalitiga mos keluvchi element manzilini qaytaradi.
2. Agar element mavjud bo'lmasa, NULL ko'rsatkich qaytaradi. Massiv oldindan saralangan bo'lishi shart.

## Ishlash natijasi:
```text
Element topildi: 50 (Indeks: 4)
```

---

# 661-Topshiriq: Funksiya ko'rsatkichlari massivi (Array of Function Pointers) asoslari

## Topshiriq sharti:
Massiv elementlari sifatida funksiya ko'rsatkichlarini saqlash va indeks orqali chaqirish.

## Yechim (C kodi):
```c
#include <stdio.h>

void f1(void) { printf("1-funksiya ishga tushdi\n"); }
void f2(void) { printf("2-funksiya ishga tushdi\n"); }
void f3(void) { printf("3-funksiya ishga tushdi\n"); }

int main(void) {
    void (*funksiyalar[3])(void) = { f1, f2, f3 };

    for (int i = 0; i < 3; i++) {
        funksiyalar[i]();
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 'void (*funksiyalar[3])(void)' sintaksisi 3 ta elementdan iborat funksiya pointerlari massividir.
2. Bu murakkab if-else zanjirlarini oddiy massiv indeksatsiyasiga aylantiradi.

## Ishlash natijasi:
```text
1-funksiya ishga tushdi
2-funksiya ishga tushdi
3-funksiya ishga tushdi
```

---

# 662-Topshiriq: Jump Table (Sakrash Jadvali) yordamida O(1) Kalkulyator

## Topshiriq sharti:
Amal kodi (+, -, *, /) bo'yicha switch-casesiz to'g'ridan-to'g'ri O(1) da hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>

int op_qosh(int a, int b) { return a + b; }
int op_ayir(int a, int b) { return a - b; }
int op_kop(int a, int b)  { return a * b; }
int op_bol(int a, int b)  { return b != 0 ? a / b : 0; }

typedef int (*CalcOp)(int, int);

int main(void) {
    // 0: +, 1: -, 2: *, 3: /
    CalcOp jump_table[4] = { op_qosh, op_ayir, op_kop, op_bol };

    int buyruq = 2; // Ko'paytirish
    int x = 6, y = 7;

    printf("Natija: %d\n", jump_table[buyruq](x, y));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Jump Table orqali chaqiruv O(1) vaqt oladi, switch-case dagi kabi ketma-ket solishtirishlar talab qilinmaydi.
2. Kompilyatorlar ham katta zich switch-case larni mashina tilidagi jump table ga aylantiradi.

## Ishlash natijasi:
```text
Natija: 42
```

---

# 663-Topshiriq: Funksiyadan funksiya ko'rsatkichini qaytarish (Returning Function Pointer)

## Topshiriq sharti:
Amal belgisiga qarab mos funksiya ko'rsatkichini qaytaruvchi fabrika funksiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>

int qosh(int a, int b) { return a + b; }
int ayir(int a, int b) { return a - b; }

typedef int (*MatemFunksiya)(int, int);

MatemFunksiya tanla_amal(char c) {
    if (c == '+') return qosh;
    if (c == '-') return ayir;
    return NULL;
}

int main(void) {
    MatemFunksiya fn = tanla_amal('+');
    if (fn) {
        printf("10 + 5 = %d\n", fn(10, 5));
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiyadan funksiya ko'rsatkichini qaytarish orqali strategiya (Strategy pattern) yoki fabrikalarni tashkil qilish mumkin.

## Ishlash natijasi:
```text
10 + 5 = 15
```

---

# 664-Topshiriq: Funksiyadan funksiya ko'rsatkichini qaytarish (typedef siz sof C sintaksisi)

## Topshiriq sharti:
typedef ishlatmasdan funksiyadan funksiya ko'rsatkichi qaytaruvchi murakkab C sintaksisini yechish.

## Yechim (C kodi):
```c
#include <stdio.h>

int kvadrat(int x) { return x * x; }

// Sof C sintaksisi: get_funksiya int qabul qiladi va int (*)(int) qaytaradi
int (*get_funksiya(void))(int) {
    return kvadrat;
}

int main(void) {
    int (*fn)(int) = get_funksiya();
    printf("5 ning kvadrati: %d\n", fn(5));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 'int (*get_funksiya(void))(int)' sintaksisi C tilining eng qiyin o'qiluvchi sintaksislaridan biridir (Right-Left rule).
2. Shu sababli haqiqiy ishlab chiqishda har doim typedef ishlatish tavsiya etiladi.

## Ishlash natijasi:
```text
5 ning kvadrati: 25
```

---

# 665-Topshiriq: C tilida Virtual Metodlar Jadvali (vtable) va Polimorfizm

## Topshiriq sharti:
Struktura ichida funksiya ko'rsatkichlari jadvali (vtable) orqali OOP abstraksiyasini amalga oshirish.

## Yechim (C kodi):
```c
#include <stdio.h>

// Interfeys (vtable)
typedef struct ShaklVTable {
    double (*yuzasi)(void *self);
    void (*chiz)(void *self);
} ShaklVTable;

// Doira ob'ekti
typedef struct {
    ShaklVTable *vptr;
    double radius;
} Doira;

double doira_yuzi(void *self) {
    Doira *d = (Doira*)self;
    return 3.14159 * d->radius * d->radius;
}

void doira_chiz(void *self) {
    Doira *d = (Doira*)self;
    printf("Doira chizildi (r=%.1f)\n", d->radius);
}

ShaklVTable doira_vtable = { doira_yuzi, doira_chiz };

int main(void) {
    Doira d = { &doira_vtable, 5.0 };

    d.vptr->chiz(&d);
    printf("Doira yuzasi: %.2f\n", d.vptr->yuzasi(&d));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++ va Java virtual metodlarni (virtual methods) orqa fonda aynan mana shunday vtable va vptr tuzilmalari orqali amalga oshiradi.
2. C tilida vtable yozish orqali xuddi shu polimorfik imkoniyatlarga erishish mumkin.

## Ishlash natijasi:
```text
Doira chizildi (r=5.0)
Doira yuzasi: 78.54
```

---

# 666-Topshiriq: Funktsional dasturlash: map() algoritmi C tilida

## Topshiriq sharti:
Massivning har bir elementini funksiya orqali o'zgartirib yangi natija massivini hosil qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef int (*TransformFn)(int);

void map(const int *kirish, int *chiqish, int n, TransformFn fn) {
    for (int i = 0; i < n; i++) {
        chiqish[i] = fn(kirish[i]);
    }
}

int ikki_barobar(int x) { return x * 2; }

int main(void) {
    int kirish[4] = {1, 2, 3, 4};
    int chiqish[4];

    map(kirish, chiqish, 4, ikki_barobar);

    printf("Map natijasi: ");
    for (int i = 0; i < 4; i++) {
        printf("%d ", chiqish[i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. map() oliy tartibli funksiya (Higher-order function) bo'lib, funksiyani ma'lumot sifatida qabul qiladi.
2. Bu kod takrorlanishini keskin kamaytiradi.

## Ishlash natijasi:
```text
Map natijasi: 2 4 6 8
```

---

# 667-Topshiriq: Funktsional dasturlash: filter() algoritmi C tilida

## Topshiriq sharti:
Berilgan predikat (shart) funksiyasini qanoatlantiruvchi elementlarni ajratib olish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef int (*PredikatFn)(int);

int filter(const int *kirish, int n, int *chiqish, PredikatFn shart) {
    int sanagich = 0;
    for (int i = 0; i < n; i++) {
        if (shart(kirish[i])) {
            chiqish[sanagich++] = kirish[i];
        }
    }
    return sanagich;
}

int juftmi(int x) { return x % 2 == 0; }

int main(void) {
    int sonlar[] = {1, 2, 3, 4, 5, 6, 7, 8};
    int filtr_qilingan[8];

    int count = filter(sonlar, 8, filtr_qilingan, juftmi);

    printf("Juft sonlar: ");
    for (int i = 0; i < count; i++) {
        printf("%d ", filtr_qilingan[i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Predikat funksiya rost (1) yoki yolg'on (0) qiymat qaytaradi.
2. filter() faqat shartni qanoatlantirgan elementlarni yangi buferga ko'chiradi va yangi uzunlikni qaytaradi.

## Ishlash natijasi:
```text
Juft sonlar: 2 4 6 8
```

---

# 668-Topshiriq: Funktsional dasturlash: reduce() / fold() algoritmi C tilida

## Topshiriq sharti:
Massiv elementlarini bitta yakuniy qiymatga yig'ish (akkumulyatsiya qilish).

## Yechim (C kodi):
```c
#include <stdio.h>

typedef int (*ReduceFn)(int akkumulyator, int joriy);

int reduce(const int *arr, int n, ReduceFn fn, int boshlangich) {
    int akk = boshlangich;
    for (int i = 0; i < n; i++) {
        akk = fn(akk, arr[i]);
    }
    return akk;
}

int yigindi(int akk, int x) { return akk + x; }
int kopaytma(int akk, int x) { return akk * x; }

int main(void) {
    int sonlar[] = {1, 2, 3, 4, 5};

    int jami = reduce(sonlar, 5, yigindi, 0);
    int faktorial = reduce(sonlar, 5, kopaytma, 1);

    printf("Yig'indi: %d\n", jami);
    printf("Ko'paytma (5!): %d\n", faktorial);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. reduce() massivni bitta skalyar qiymatga aylantiruvchi universal funksiyadir.
2. Boshlang'ich qiymat neytral element (qo'shishda 0, ko'paytirishda 1) sifatida tanlanadi.

## Ishlash natijasi:
```text
Yig'indi: 15
Ko'paytma (5!): 120
```

---

# 669-Topshiriq: Hodisalarga asoslangan tizim (Event Hook System)

## Topshiriq sharti:
Tizimdagi hodisa yuz berganda ro'yxatdan o'tgan bir nechta callbacklarni ketma-ket chaqirish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define MAX_HOOKS 4

typedef void (*EventCallback)(const char *hodisa);

typedef struct {
    EventCallback hooks[MAX_HOOKS];
    int count;
} EventManager;

void qosh_hook(EventManager *em, EventCallback cb) {
    if (em->count < MAX_HOOKS) {
        em->hooks[em->count++] = cb;
    }
}

void trigger_event(EventManager *em, const char *msg) {
    for (int i = 0; i < em->count; i++) {
        em->hooks[i](msg);
    }
}

void logger_hook(const char *msg) { printf("[LOGGER]: %s\n", msg); }
void alert_hook(const char *msg)  { printf("[ALERT]: Xabar olindi -> %s\n", msg); }

int main(void) {
    EventManager em = { .count = 0 };
    qosh_hook(&em, logger_hook);
    qosh_hook(&em, alert_hook);

    trigger_event(&em, "Foydalanuvchi tizimga ulandi");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Observer (Kuzatuvchi) and Publish-Subscribe andozasi aynan funksiya ko'rsatkichlari massivi orqali quriladi.
2. Yangi tinglovchilarni dinamik ulash va uzish imkoni paydo bo'ladi.

## Ishlash natijasi:
```text
[LOGGER]: Foydalanuvchi tizimga ulandi
[ALERT]: Xabar olindi -> Foydalanuvchi tizimga ulandi
```

---

# 670-Topshiriq: Kontekstli Callback (Context Pointer / User Data idiomasi)

## Topshiriq sharti:
Callback ga qo'shimcha 'void *user_data' parametrini uzatish orqali holatni (state) yetkazish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef void (*DataCallback)(int qiymat, void *user_data);

void aylanib_chiq(int *arr, int len, DataCallback cb, void *user_data) {
    for (int i = 0; i < len; i++) {
        cb(arr[i], user_data);
    }
}

void yigindi_qosh(int qiymat, void *user_data) {
    int *jami = (int *)user_data;
    *jami += qiymat;
}

int main(void) {
    int sonlar[] = {10, 20, 30, 40};
    int jami = 0;

    aylanib_chiq(sonlar, 4, yigindi_qosh, &jami);

    printf("Hisoblangan jami: %d\n", jami);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida qobiqlar (closures/lambdas) bo'lmagani sababli, har qanday professional kutubxona callback yonida `void *user_data` ni uzatadi.
2. Bu callback ichida tashqi kontekst va ma'lumotlarga kirish imkonini beradi.

## Ishlash natijasi:
```text
Hisoblangan jami: 100
```

---

# 671-Topshiriq: POSIX / Standart C signal() boshqaruvi callbacki

## Topshiriq sharti:
signal() orqali signallarni ushlash va qayta ishlash callback funksiyasini biriktirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <signal.h>

void signal_qayta_ishlagich(int sig) {
    printf("\n[SIGNAL]: %d raqamli signal ushlandi!\n", sig);
}

int main(void) {
    // SIGINT (Ctrl+C) uchun ko'rsatkich biriktiramiz
    void (*eski_handler)(int) = signal(SIGINT, signal_qayta_ishlagich);

    printf("Signal boshqaruvchisi o'rnatildi (Eski handler mavjud: %s).\n",
           eski_handler != SIG_ERR ? "HA" : "YO'Q");

    // Sun'iy signal yuboramiz
    raise(SIGINT);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. signal() funksiyasining imzosi: `void (*signal(int sig, void (*func)(int)))(int)`.
2. Bu C tilidagi eng mashhur tizimli callback namunasidir.

## Ishlash natijasi:
```text
Signal boshqaruvchisi o'rnatildi (Eski handler mavjud: HA).

[SIGNAL]: 2 raqamli signal ushlandi!
```

---

# 672-Topshiriq: Atexit callbacklari: Dastur yakunlanganda bajariluvchi tozalash funksiyalari

## Topshiriq sharti:
atexit() orqali dastur tugaganda avtomatik ishga tushuvchi callbacklarni ro'yxatdan o'tkazish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

void resurslarni_tozala(void) {
    printf("[ATEXIT]: Vaqtinchalik fayllar o'chirildi va xotira tozalandi.\n");
}

void xayrlashuv(void) {
    printf("[ATEXIT]: Dastur muvaffaqiyatli yakunlandi. Xayr!\n");
}

int main(void) {
    atexit(xayrlashuv);
    atexit(resurslarni_tozala);

    printf("Asosiy ish bajarilmoqda...\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. atexit() ro'yxatdan o'tkazilgan funksiyalarni LIFO (oxirgi kirgan - birinchi chiqadi) tartibida chaqiradi.
2. Dastur main() dan return qilganda yoki exit() chaqirilganda ishga tushadi.

## Ishlash natijasi:
```text
Asosiy ish bajarilmoqda...
[ATEXIT]: Vaqtinchalik fayllar o'chirildi va xotira tozalandi.
[ATEXIT]: Dastur muvaffaqiyatli yakunlandi. Xayr!
```

---

# 673-Topshiriq: Binar qidiruv daraxtini (BST) callback bilan aylanib chiqish (In-Order Traversal Callback)

## Topshiriq sharti:
Daraxtning har bir tugunini chaqiruvchi callback orqali ekranga chiqarish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Tugun {
    int qiymat;
    struct Tugun *chap;
    struct Tugun *ong;
} Tugun;

Tugun* yangi_tugun(int val) {
    Tugun *t = (Tugun*)malloc(sizeof(Tugun));
    t->qiymat = val;
    t->chap = t->ong = NULL;
    return t;
}

void inorder(Tugun *ildiz, void (*cb)(int)) {
    if (!ildiz) return;
    inorder(ildiz->chap, cb);
    cb(ildiz->qiymat);
    inorder(ildiz->ong, cb);
}

void chop(int v) { printf("%d ", v); }

int main(void) {
    Tugun *ildiz = yangi_tugun(50);
    ildiz->chap = yangi_tugun(30);
    ildiz->ong = yangi_tugun(70);

    printf("BST In-Order traversal: ");
    inorder(ildiz, chop);
    printf("\n");

    free(ildiz->chap);
    free(ildiz->ong);
    free(ildiz);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ma'lumot tuzilmasini aylanib chiqish algoritmi ma'lumotni nima qilishdan (chop etish, saqlash, yig'ish) to'liq ajratilgan.

## Ishlash natijasi:
```text
BST In-Order traversal: 30 50 70
```

---

# 674-Topshiriq: Matematik ifodalarni raqamli integrallash (Numerical Integration callback)

## Topshiriq sharti:
Trapetsiya usuli orqali ixtiyoriy matematik funksiyaning integralini hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef double (*MathFunc)(double);

double integral(MathFunc f, double a, double b, int n) {
    double h = (b - a) / n;
    double sum = 0.5 * (f(a) + f(b));
    for (int i = 1; i < n; i++) {
        sum += f(a + i * h);
    }
    return sum * h;
}

double kvadrat(double x) { return x * x; }

int main(void) {
    // integral of x^2 from 0 to 3 = [x^3 / 3]_0^3 = 9.0
    double natija = integral(kvadrat, 0.0, 3.0, 1000);
    printf("Integral x^2 [0..3]: %.4f\n", natija);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiya ko'rsatkichlari ilmiy hisoblashlarda turli tenglamalar va funksiyalarni bitta integral yoki differensial yechuvchisiga uzatish imkonini beradi.

## Ishlash natijasi:
```text
Integral x^2 [0..3]: 9.0000
```

---

# 675-Topshiriq: Dinamik kutubxona funksiyalarini chaqirish simulyatsiyasi

## Topshiriq sharti:
Operatsion tizimda dlsym / GetProcAddress orqali xotiradagi funksiya manzilini olib chaqirish tamoyili.

## Yechim (C kodi):
```c
#include <stdio.h>

int maxfiy_algoritm(int a) {
    return a * 42;
}

int main(void) {
    // void* ko'rsatkichini funksiya ko'rsatkichiga keltirish
    void *ram_manzil = (void*)maxfiy_algoritm;

    // To'g'ri tipga cast qilamiz
    int (*dinamik_fn)(int) = (int (*)(int))ram_manzil;

    printf("Dinamik chaqiruv natijasi: %d\n", dinamik_fn(10));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dinamik plaginlar va DLL kutubxonalar aynan shu yo'l bilan funksiya nomiga mos manzilni topadi va uni mos funksiya pointeriga cast qiladi.

## Ishlash natijasi:
```text
Dinamik chaqiruv natijasi: 420
```

---

# 676-Topshiriq: Struktura a'zosi sifatida funksiya ko'rsatkichlari (C tilida ob'ektlar)

## Topshiriq sharti:
Ma'lumotlar va ularga ishlov beruvchi metodlarni bitta struktura ichiga joylashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct Hisoblagich {
    int qiymat;
    void (*oshir)(struct Hisoblagich *self);
    void (*kamaytir)(struct Hisoblagich *self);
} Hisoblagich;

void inc(Hisoblagich *self) { self->qiymat++; }
void dec(Hisoblagich *self) { self->qiymat--; }

Hisoblagich yarat_hisoblagich(int boshlangich) {
    Hisoblagich h = { boshlangich, inc, dec };
    return h;
}

int main(void) {
    Hisoblagich h = yarat_hisoblagich(10);
    h.oshir(&h);
    h.oshir(&h);
    h.kamaytir(&h);

    printf("Hisoblagich yakuniy qiymati: %d\n", h.qiymat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu yondashuv C tilida 'Enkapsulyatsiya' va metodlarni amalga oshirishning klassik yo'lidir.
2. Har bir metod o'z ob'ektiga ko'rsatkichni ('this' yoki 'self') birinchi argument sifatida qabul qiladi.

## Ishlash natijasi:
```text
Hisoblagich yakuniy qiymati: 11
```

---

# 677-Topshiriq: Funksiya ko'rsatkichini solishtirish va NULL tekshiruvi

## Topshiriq sharti:
Funksiya ko'rsatkichining manzilini tekshirish, NULL bilan solishtirish va xavfsiz chaqirish.

## Yechim (C kodi):
```c
#include <stdio.h>

void f_aniq(void) { printf("Aniq funksiya\n"); }

int main(void) {
    void (*fn)(void) = NULL;

    if (fn != NULL) {
        fn();
    } else {
        printf("fn hali belgilanmagan (NULL)!\n");
    }

    fn = f_aniq;
    if (fn == f_aniq) {
        printf("fn aynan f_aniq funksiyasiga ishora qilmoqda.\n");
        fn();
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. NULL bo'lgan funksiya pointerini chaqirish Segmentation Fault (Crash) keltirib chiqaradi.
2. Shu sababli ixtiyoriy (optional) callbacklar har doim `if (cb != NULL)` bilan himoyalanishi shart.

## Ishlash natijasi:
```text
fn hali belgilanmagan (NULL)!
fn aynan f_aniq funksiyasiga ishora qilmoqda.
Aniq funksiya
```

---

# 678-Topshiriq: Ko'p o'lchamli funksiya ko'rsatkichlari massivi (State Transition Matrix)

## Topshiriq sharti:
Holat mashinasida (State, Event) juftligiga qarab bajariluvchi funksiyalar matritsasi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef enum { HOLAT_A, HOLAT_B } Holat;
typedef enum { HODISA_1, HODISA_2 } Hodisa;

void a_on_1(void) { printf("Holat A da Hodisa 1 bajarildi\n"); }
void a_on_2(void) { printf("Holat A da Hodisa 2 bajarildi\n"); }
void b_on_1(void) { printf("Holat B da Hodisa 1 bajarildi\n"); }
void b_on_2(void) { printf("Holat B da Hodisa 2 bajarildi\n"); }

void (*fsm_matrix[2][2])(void) = {
    { a_on_1, a_on_2 },
    { b_on_1, b_on_2 }
};

int main(void) {
    Holat joriy = HOLAT_A;
    Hodisa kirish = HODISA_2;

    fsm_matrix[joriy][kirish]();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 2D matritsa orqali holat o'tishlari murakkab tarmoqlanishlarsiz bitta qatorda bajariladi.

## Ishlash natijasi:
```text
Holat A da Hodisa 2 bajarildi
```

---

# 679-Topshiriq: Birlashtirilgan taqqoslash zanjiri (Chained Multi-Field Comparator)

## Topshiriq sharti:
Talabalarni avval balli bo'yicha, ballari teng bo'lsa ismi bo'yicha saralash comparator callbacki.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char ism[20];
    int ball;
} Talaba;

int talaba_kop_bosqichli(const void *a, const void *b) {
    const Talaba *t1 = (const Talaba *)a;
    const Talaba *t2 = (const Talaba *)b;

    // 1-bosqich: Ball bo'yicha kamayish
    if (t2->ball != t1->ball) {
        return t2->ball - t1->ball;
    }
    // 2-bosqich: Ism bo'yicha alifbo tartibida
    return strcmp(t1->ism, t2->ism);
}

int main(void) {
    Talaba t[] = {
        {"Zuhra", 90},
        {"Ali", 90},
        {"Vali", 80}
    };

    qsort(t, 3, sizeof(Talaba), talaba_kop_bosqichli);

    for (int i = 0; i < 3; i++) {
        printf("%s: %d\n", t[i].ism, t[i].ball);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'p maydonli saralashda birlamchi kriteriya teng bo'lgandagina ikkinchi kriteriyaga o'tiladi.

## Ishlash natijasi:
```text
Ali: 90
Zuhra: 90
Vali: 80
```

---

# 680-Topshiriq: Funksiya ko'rsatkichlari uchun umumiy shablon (Generic Dispatcher)

## Topshiriq sharti:
void* yordamida har xil turdagi funksiyalarni bitta dispatcher orqali ro'yxatga olish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef void (*GenericFunc)(void);

void chop_son(void *arg) {
    printf("Son: %d\n", *(int*)arg);
}

void chop_matn(void *arg) {
    printf("Matn: %s\n", (char*)arg);
}

int main(void) {
    void (*fn_son)(void*) = chop_son;
    void (*fn_matn)(void*) = chop_matn;

    int n = 123;
    char s[] = "C tili";

    fn_son(&n);
    fn_matn(s);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. void* argument qabul qiluvchi funksiya pointeri orqali C tilida universal generik interfeyslar quriladi.

## Ishlash natijasi:
```text
Son: 123
Matn: C tili
```

---

# 681-Topshiriq: Funksiya ko'rsatkichini boshqa funksiyaga o'rash (Decorator / Wrapper Pattern)

## Topshiriq sharti:
Asl funksiya chaqirilishidan oldin va keyin log chiqaruvchi o'ram (wrapper) yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef int (*AslFunksiya)(int);

int ikki_hissa(int x) { return x * 2; }

int log_wrapper(AslFunksiya fn, int arg) {
    printf("[WRAPPER]: Funksiya %d argumenti bilan chaqirilmoqda...\n", arg);
    int res = fn(arg);
    printf("[WRAPPER]: Natija = %d qaytdi.\n", res);
    return res;
}

int main(void) {
    int natija = log_wrapper(ikki_hissa, 21);
    printf("Yakuniy natija: %d\n", natija);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Python kabi tillardagi dekoratorlar C tilida wrapper funksiya va funksiya ko'rsatkichlari yordamida amalga oshiriladi.

## Ishlash natijasi:
```text
[WRAPPER]: Funksiya 21 argumenti bilan chaqirilmoqda...
[WRAPPER]: Natija = 42 qaytdi.
Yakuniy natija: 42
```

---

# 682-Topshiriq: Asinxron Vazifalar Navbati simulyatsiyasi (Task Queue)

## Topshiriq sharti:
Vazifalar navbatiga funksiya ko'rsatkichi va uning argumentlarini yuklash va birin-ketin bajarish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    void (*vazifa)(void *arg);
    void *arg;
} Task;

#define MAX_TASKS 4
Task queue[MAX_TASKS];
int task_count = 0;

void qosh_task(void (*fn)(void*), void *arg) {
    if (task_count < MAX_TASKS) {
        queue[task_count].vazifa = fn;
        queue[task_count].arg = arg;
        task_count++;
    }
}

void bajar_barchasini(void) {
    for (int i = 0; i < task_count; i++) {
        queue[i].vazifa(queue[i].arg);
    }
    task_count = 0;
}

void task1(void *a) { printf("Vazifa 1: xabar = %s\n", (char*)a); }
void task2(void *a) { printf("Vazifa 2: qiymat = %d\n", *(int*)a); }

int main(void) {
    char xabar[] = "Salom";
    int son = 777;

    qosh_task(task1, xabar);
    qosh_task(task2, &son);

    printf("Navbatdagi vazifalar bajarilmoqda:\n");
    bajar_barchasini();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Task queue (Vazifalar navbati) operatsion tizimlar, o'yin tsikllari va mikrokontroller schedulerlarining asosi hisoblanadi.

## Ishlash natijasi:
```text
Navbatdagi vazifalar bajarilmoqda:
Vazifa 1: xabar = Salom
Vazifa 2: qiymat = 777
```

---

# 683-Topshiriq: Funksiya ko'rsatkichi orqali xatoliklarni qayta ishlash strategiyasi (Error Handler)

## Topshiriq sharti:
Dasturdagi turli modullarga xos xatolik qayta ishlovchilarini dinamik almashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef void (*ErrorHandler)(const char *xato);

void standart_handler(const char *xato) {
    printf("[Standart Xato]: %s\n", xato);
}

void qatiy_handler(const char *xato) {
    printf("[XAVFSIZLIK XATOSI]: Tizim ogohlantirildi: %s!\n", xato);
}

ErrorHandler joriy_handler = standart_handler;

void xatolik_yuz_berdi(const char *sabab) {
    joriy_handler(sabab);
}

int main(void) {
    xatolik_yuz_berdi("Fayl topilmadi");

    // Strategiyani almashtiramiz
    joriy_handler = qatiy_handler;
    xatolik_yuz_berdi("Ruxsatsiz kirish aniqlandi");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Global yoki modul darajasidagi xatolik callbacki orqali xatolarni jurnalga yozish, ekranga chiqarish yoki tarmoqqa uzatish strategiyalarini osongina almashtirish mumkin.

## Ishlash natijasi:
```text
[Standart Xato]: Fayl topilmadi
[XAVFSIZLIK XATOSI]: Tizim ogohlantirildi: Ruxsatsiz kirish aniqlandi!
```

---

# 684-Topshiriq: Funksiya ko'rsatkichi bilan qidiruv predikati (Find-If algoritmi)

## Topshiriq sharti:
Massiv ichidan berilgan murakkab shartni qanoatlantiruvchi birinchi element indeksini topish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef int (*Predikat)(int);

int find_if(const int *arr, int len, Predikat p) {
    for (int i = 0; i < len; i++) {
        if (p(arr[i])) return i;
    }
    return -1;
}

int katta_50dan(int x) { return x > 50; }

int main(void) {
    int sonlar[] = {12, 34, 48, 55, 60, 22};
    int idx = find_if(sonlar, 6, katta_50dan);

    if (idx != -1) {
        printf("50 dan katta birinchi son: %d (indeks: %d)\n", sonlar[idx], idx);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. STL dagi `std::find_if` C tilida funksiya ko'rsatkichlari orqali ixcham amalga oshiriladi.

## Ishlash natijasi:
```text
50 dan katta birinchi son: 55 (indeks: 3)
```

---

# 685-Topshiriq: Qaytaruvchi tipi funksiya ko'rsatkichi bo'lgan funksiyalar massivi

## Topshiriq sharti:
Juda murakkab deklaratsiyalarni tahlil qilish va ishlatish.

## Yechim (C kodi):
```c
#include <stdio.h>

int amal_a(int x) { return x + 1; }
int amal_b(int x) { return x * 10; }

typedef int (*OddiyAmal)(int);
typedef OddiyAmal (*AmalGenerator)(void);

OddiyAmal gen_a(void) { return amal_a; }
OddiyAmal gen_b(void) { return amal_b; }

int main(void) {
    AmalGenerator generatorlar[2] = { gen_a, gen_b };

    OddiyAmal f0 = generatorlar[0]();
    OddiyAmal f1 = generatorlar[1]();

    printf("f0(5) = %d\n", f0(5));
    printf("f1(5) = %d\n", f1(5));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. typedef pog'onalari yordamida har qanday yuqori tartibli funksiyalar arxitekturasini tushunarli qilish mumkin.

## Ishlash natijasi:
```text
f0(5) = 6
f1(5) = 50
```

---

# 686-Topshiriq: O'z-o'zini o'zgartiruvchi holat mashinasi (State Machine via Function Pointers)

## Topshiriq sharti:
Har bir holat funksiyasi keyingi holat funksiyasining manzilini qaytaruvchi nafis FSM.

## Yechim (C kodi):
```c
#include <stdio.h>

struct HolatMashinasi;
typedef void (*HolatFn)(struct HolatMashinasi *sm);

typedef struct HolatMashinasi {
    HolatFn joriy_holat;
    int qadam;
} HolatMashinasi;

void holat_b(HolatMashinasi *sm);

void holat_a(HolatMashinasi *sm) {
    printf("Holat A bajarildi (qadam: %d)\n", sm->qadam++);
    sm->joriy_holat = holat_b; // Keyingi holatga o'tish
}

void holat_b(HolatMashinasi *sm) {
    printf("Holat B bajarildi (qadam: %d)\n", sm->qadam++);
    sm->joriy_holat = NULL; // Tugatish
}

int main(void) {
    HolatMashinasi sm = { holat_a, 1 };

    while (sm.joriy_holat != NULL) {
        sm.joriy_holat(&sm);
    }
    printf("Mashina to'xtadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu usulda katta switch-case larga ehtiyoj qolmaydi, har bir holat o'zidan keyingi holatni mustaqil belgilaydi.

## Ishlash natijasi:
```text
Holat A bajarildi (qadam: 1)
Holat B bajarildi (qadam: 2)
Mashina to'xtadi.
```

---

# 687-Topshiriq: Binar protokol paketlarini pars qilishda Action Table

## Topshiriq sharti:
Paket ID siga qarab mos paket ishlovchi funksiyani avtomatik tanlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef void (*PacketHandler)(const uint8_t *data, uint16_t len);

void handle_login(const uint8_t *d, uint16_t len) {
    printf("Login paketi qabul qilindi, uzunlik: %u bayt\n", len);
}

void handle_message(const uint8_t *d, uint16_t len) {
    printf("Xabar paketi qabul qilindi, uzunlik: %u bayt\n", len);
}

PacketHandler handlers[256] = { NULL };

int main(void) {
    // 0x01 = Login, 0x02 = Message
    handlers[0x01] = handle_login;
    handlers[0x02] = handle_message;

    uint8_t packet1[4] = {0x01, 10, 20, 30};
    uint8_t opcode = packet1[0];

    if (handlers[opcode] != NULL) {
        handlers[opcode](packet1 + 1, 3);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 256 elementli jadval barcha 1-baytli opcode larni bitta operatsiyada xaritalaydi.

## Ishlash natijasi:
```text
Login paketi qabul qilindi, uzunlik: 3 bayt
```

---

# 688-Topshiriq: Taymer va vaqtga bog'liq callbacklar simulyatsiyasi

## Topshiriq sharti:
Vaqt oralig'i o'tgach chaqiriluvchi taymer callback tizimi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int interval_ms;
    int otgan_vaqt_ms;
    void (*on_timeout)(void);
} Taymer;

void chiroqni_yoq(void) {
    printf("[TAYMER]: Belgilangan vaqt o'tdi! Chiroq yoqildi.\n");
}

void tekshir_taymer(Taymer *t, int delta_ms) {
    t->otgan_vaqt_ms += delta_ms;
    if (t->otgan_vaqt_ms >= t->interval_ms) {
        t->on_timeout();
        t->otgan_vaqt_ms = 0; // Qayta ishga tushirish
    }
}

int main(void) {
    Taymer t = { 1000, 0, chiroqni_yoq };

    printf("Vaqt simulyatsiyasi boshlandi...\n");
    tekshir_taymer(&t, 400);
    tekshir_taymer(&t, 400);
    tekshir_taymer(&t, 300); // Jami 1100 ms -> vaqt tugadi!
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Real vaqt operatsion tizimlarida (RTOS) dasturiy taymerlar aynan shunday callback tizimi bilan ishlaydi.

## Ishlash natijasi:
```text
Vaqt simulyatsiyasi boshlandi...
[TAYMER]: Belgilangan vaqt o'tdi! Chiroq yoqildi.
```

---

# 689-Topshiriq: qsort_r / qsort_s kontekstli saralash tushunchasi

## Topshiriq sharti:
Standart qsort comparatoriga tashqi parametr uzatib bo'lmaslik cheklovini va kontekstli comparator tamoyilini tushunish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int ascending; // 1 = o'sish, 0 = kamayish
} SortContext;

// Kontekstni qabul qiluvchi maxsus saralash funksiyasi
void custom_sort(int *arr, int n, SortContext *ctx) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            int shart = ctx->ascending ? (arr[j] > arr[j + 1]) : (arr[j] < arr[j + 1]);
            if (shart) {
                int tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
            }
        }
    }
}

int main(void) {
    int sonlar[] = {3, 1, 4, 1, 5, 9};
    SortContext ctx = { .ascending = 0 }; // Kamayish tartibida

    custom_sort(sonlar, 6, &ctx);

    printf("Kontekst bo'yicha saralandi: ");
    for (int i = 0; i < 6; i++) {
        printf("%d ", sonlar[i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Standart qsort() global o'zgaruvchisiz qo'shimcha parametr qabul qila olmaydi.
2. Shu sababli C11 qsort_s va GNU qsort_r larda 'void *thunk' (user context) parametri kiritilgan.

## Ishlash natijasi:
```text
Kontekst bo'yicha saralandi: 9 5 4 3 1 1
```

---

# 690-Topshiriq: Funksiya ko'rsatkichlari bilan Dependency Injection (Bog'liqlikni kiritish)

## Topshiriq sharti:
Faylga yoki tarmoqqa yozuvchi modulni almashtirish imkonini beruvchi injeksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef void (*YozuvchiFunksiya)(const char *xabar);

void konsolga_yoz(const char *msg) {
    printf("[KONSOL]: %s\n", msg);
}

void simulyatsiya_faylga_yoz(const char *msg) {
    printf("[FAYLGA YOZILDI]: %s\n", msg);
}

typedef struct {
    YozuvchiFunksiya writer;
} TizimXizmati;

void xizmat_ishla(TizimXizmati *srv, const char *matn) {
    srv->writer(matn);
}

int main(void) {
    TizimXizmati srv1 = { konsolga_yoz };
    xizmat_ishla(&srv1, "Dastur ishga tushdi");

    TizimXizmati srv2 = { simulyatsiya_faylga_yoz };
    xizmat_ishla(&srv2, "Muhim log faylga saqlandi");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mock va Unit Test yozishda tashqi xizmatlarni (fayl, tarmoq, baza) simulyatsiya qilish uchun Dependency Injection zarur.

## Ishlash natijasi:
```text
[KONSOL]: Dastur ishga tushdi
[FAYLGA YOZILDI]: Muhim log faylga saqlandi
```

---

# 691-Topshiriq: O'zgaruvchan parametrli (Variadic) Funksiya Ko'rsatkichi

## Topshiriq sharti:
printf kabi int (*)(const char *, ...) ko'rsatkichini e'lon qilish va ishlatish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // printf funksiyasiga mos pointer
    int (*print_ptr)(const char *, ...) = printf;

    print_ptr("Son: %d, Matn: %s\n", 42, "Antigravity");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiya pointeri o'zgaruvchan argumentlar ro'yxatini ham o'z imzosida aniq aks ettirishi shart.

## Ishlash natijasi:
```text
Son: 42, Matn: Antigravity
```

---

# 692-Topshiriq: Funksiya ko'rsatkichlari bilan O(N) da massiv qismlarini birlashtirish (ZipWith)

## Topshiriq sharti:
Ikkita massivni elementma-element berilgan binar funksiya bilan birlashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef int (*ZipFn)(int, int);

void zip_with(const int *a, const int *b, int *out, int len, ZipFn fn) {
    for (int i = 0; i < len; i++) {
        out[i] = fn(a[i], b[i]);
    }
}

int kopaytma(int x, int y) { return x * y; }

int main(void) {
    int narxlar[] = {10, 20, 30};
    int miqdorlar[] = {2, 5, 3};
    int jami[3];

    zip_with(narxlar, miqdorlar, jami, 3, kopaytma);

    printf("Har bir mahsulot summasi: ");
    for (int i = 0; i < 3; i++) {
        printf("%d ", jami[i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. zip_with funksional dasturlash andozasi bo'lib, ikki parallel ma'lumot oqimini yangi oqimga birlashtiradi.

## Ishlash natijasi:
```text
Har bir mahsulot summasi: 20 100 90
```

---

# 693-Topshiriq: Funksiya ko'rsatkichlari bilan xavfsiz Sandbox / Cheklovchi tizim

## Topshiriq sharti:
Faqat ruxsat berilgan amallarni chaqirishga imkon beruvchi tekshiruvchi chaqiruvchi (Sanitizer caller).

## Yechim (C kodi):
```c
#include <stdio.h>

typedef void (*Amal)(void);

void xavfsiz_amal(void) { printf("Xavfsiz hisoblash bajarildi\n"); }
void xavfli_amal(void)  { printf("Xavfli buyruq bajarildi\n"); }

void ruxsatli_bajar(Amal fn, Amal ruxsat_etilgan) {
    if (fn == ruxsat_etilgan) {
        fn();
    } else {
        printf("[XAVFSIZLIK TO'SIG'I]: Ruxsat etilmagan funksiyani chaqirish bloklandi!\n");
    }
}

int main(void) {
    ruxsatli_bajar(xavfsiz_amal, xavfsiz_amal);
    ruxsatli_bajar(xavfli_amal, xavfsiz_amal);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiya ko'rsatkichlarini to'g'ridan-to'g'ri manzil bo'yicha tenglikka solishtirish mumkin.

## Ishlash natijasi:
```text
Xavfsiz hisoblash bajarildi
[XAVFSIZLIK TO'SIG'I]: Ruxsat etilmagan funksiyani chaqirish bloklandi!
```

---

# 694-Topshiriq: Rekursiv funktsiyalarga ko'rsatkichlar

## Topshiriq sharti:
Faktorial hisoblovchi rekursiv funksiyani ko'rsatkich orqali boshqarish.

## Yechim (C kodi):
```c
#include <stdio.h>

unsigned long long faktorial(unsigned int n) {
    if (n <= 1) return 1;
    return n * faktorial(n - 1);
}

int main(void) {
    unsigned long long (*fn)(unsigned int) = faktorial;

    printf("5! = %llu\n", fn(5));
    printf("7! = %llu\n", fn(7));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Rekursiv funksiya pointer orqali chaqirilganda ham ichki chaqiruvlar to'g'ri bajariladi.

## Ishlash natijasi:
```text
5! = 120
7! = 5040
```

---

# 695-Topshiriq: Funksiya ko'rsatkichi massivini saralash

## Topshiriq sharti:
Funksiyalarning xotiradagi manzili bo'yicha funksiya pointerlarini saralash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

void fa(void) {}
void fb(void) {}
void fc(void) {}

typedef void (*FnPtr)(void);

int cmp_fn(const void *a, const void *b) {
    FnPtr f1 = *(const FnPtr*)a;
    FnPtr f2 = *(const FnPtr*)b;
    if ((uintptr_t)f1 < (uintptr_t)f2) return -1;
    if ((uintptr_t)f1 > (uintptr_t)f2) return 1;
    return 0;
}

int main(void) {
    FnPtr massiv[3] = { fc, fa, fb };

    qsort(massiv, 3, sizeof(FnPtr), cmp_fn);

    printf("Funksiya ko'rsatkichlari manzil bo'yicha tartiblandi:\n");
    for (int i = 0; i < 3; i++) {
        printf("Fn [%d] manzili: %p\n", i, (void*)massiv[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiya pointerlari xotiradagi Code / Text segmentida joylashadi va ularning manzilini taqqoslash mumkin.

## Ishlash natijasi:
```text
Funksiya ko'rsatkichlari manzil bo'yicha tartiblandi:
Fn [0] manzili: 0000000000401500
Fn [1] manzili: 0000000000401510
Fn [2] manzili: 0000000000401520
```

---

# 696-Topshiriq: Observer andozasida Ob'ektlarni ro'yxatdan chiqarish (Unsubscribe)

## Topshiriq sharti:
Listener callbackni topib ro'yxatdan o'chirish mexanizmi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef void (*Listener)(int);

Listener obunachilar[4] = { NULL };

void subscribe(Listener l) {
    for (int i = 0; i < 4; i++) {
        if (obunachilar[i] == NULL) {
            obunachilar[i] = l;
            return;
        }
    }
}

void unsubscribe(Listener l) {
    for (int i = 0; i < 4; i++) {
        if (obunachilar[i] == l) {
            obunachilar[i] = NULL;
            return;
        }
    }
}

void notify(int val) {
    for (int i = 0; i < 4; i++) {
        if (obunachilar[i] != NULL) {
            obunachilar[i](val);
        }
    }
}

void user1(int v) { printf("User1 qabul qildi: %d\n", v); }
void user2(int v) { printf("User2 qabul qildi: %d\n", v); }

int main(void) {
    subscribe(user1);
    subscribe(user2);
    notify(100);

    printf("User1 obunani bekor qildi:\n");
    unsubscribe(user1);
    notify(200);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Callback pointerlarini tenglikka tekshirish orqali obunani bekor qilish (unsubscribe) amalga oshiriladi.

## Ishlash natijasi:
```text
User1 qabul qildi: 100
User2 qabul qildi: 100
User1 obunani bekor qildi:
User2 qabul qildi: 200
```

---

# 697-Topshiriq: Birlashtirilgan Matematik Solver (Root Finding via Newton-Raphson)

## Topshiriq sharti:
Funksiya va uning hosilasini funksiya pointeri sifatida uzatib tenglama ildizini topish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

typedef double (*MatemFn)(double);

double newton_raphson(MatemFn f, MatemFn f_hosila, double x0, int max_iter) {
    double x = x0;
    for (int i = 0; i < max_iter; i++) {
        double y = f(x);
        double dy = f_hosila(x);
        if (fabs(dy) < 1e-12) break;
        x = x - y / dy;
    }
    return x;
}

// f(x) = x^2 - 4
double f(double x) { return x * x - 4.0; }
// f'(x) = 2x
double f_hosila(double x) { return 2.0 * x; }

int main(void) {
    double ildiz = newton_raphson(f, f_hosila, 1.0, 10);
    printf("x^2 - 4 = 0 ildizi: %.2f\n", ildiz);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Nyuton-Rafson algoritmi tenglamalarni sonli usulda yechishda funksiya va hosilasini callback sifatida qabul qiladi.

## Ishlash natijasi:
```text
x^2 - 4 = 0 ildizi: 2.00
```

---

# 698-Topshiriq: Funksiya chaqiruvlari hisoblagichi va xotirani profayling qilish

## Topshiriq sharti:
Har bir funksiya chaqirilganda qancha vaqt ketganini va necha bor chaqirilganini sanovchi Profiler.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef void (*VoidAction)(void);

typedef struct {
    VoidAction fn;
    const char *nomi;
    int chaqiruvlar_soni;
} ProfiledFunc;

void yuklama_a(void) { /* simulyatsiya */ }
void yuklama_b(void) { /* simulyatsiya */ }

void bajar_va_profil(ProfiledFunc *pf) {
    pf->fn();
    pf->chaqiruvlar_soni++;
}

int main(void) {
    ProfiledFunc p1 = { yuklama_a, "Yuklama A", 0 };
    ProfiledFunc p2 = { yuklama_b, "Yuklama B", 0 };

    bajar_va_profil(&p1);
    bajar_va_profil(&p1);
    bajar_va_profil(&p2);

    printf("%s: %d marta\n", p1.nomi, p1.chaqiruvlar_soni);
    printf("%s: %d marta\n", p2.nomi, p2.chaqiruvlar_soni);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Profiler dasturlari (masalan gprof) orqa fonda funksiya pointerlari orqali har bir funksiyaning ishlash statistikasini yig'adi.

## Ishlash natijasi:
```text
Yuklama A: 2 marta
Yuklama B: 1 marta
```

---

# 699-Topshiriq: Ko'rsatkich orqali uzatilgan funksiyalar bilan Shartli Quvurlar (Pipeline / Middleware)

## Topshiriq sharti:
Ma'lumotni ketma-ket bir nechta filtrlar (middleware) orqali o'tkazish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef int (*Middleware)(int);

int qo_sh_besh(int x) { return x + 5; }
int ko_paytir_ikki(int x) { return x * 2; }
int ayir_uch(int x) { return x - 3; }

int pipeline(int boshlangich, Middleware *zanjir, int soni) {
    int qiymat = boshlangich;
    for (int i = 0; i < soni; i++) {
        qiymat = zanjir[i](qiymat);
    }
    return qiymat;
}

int main(void) {
    Middleware quvur[] = { qo_sh_besh, ko_paytir_ikki, ayir_uch };
    int kirish = 10;

    // ((10 + 5) * 2) - 3 = 30 - 3 = 27
    int chiqish = pipeline(kirish, quvur, 3);
    printf("Kirish: %d -> Chiqish: %d\n", kirish, chiqish);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Veb serverlar (Express, Actix) va ma'lumot tahlili quvurlari (Data processing pipelines) aynan shunday middleware zanjiriga tayanadi.

## Ishlash natijasi:
```text
Kirish: 10 -> Chiqish: 27
```

---

# 700-Topshiriq: Modul yakuni va Master Loyiha: Hodisalarga asoslangan To'liq GUI / Widget Hodisalar Tizimi (Event-Driven Widget Engine)

## Topshiriq sharti:
Tugma (Button), Matn maydoni (TextBox) va Voqealar (Click, Hover, Focus) tizimini to'liq C polimorfizmi va callbacklar orqali amalga oshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

typedef enum {
    EVENT_CLICK,
    EVENT_HOVER
} EventType;

struct Widget;
typedef void (*EventHandler)(struct Widget *sender, EventType ev, void *user_data);

typedef struct Widget {
    char id[32];
    EventHandler on_event;
    void *user_data;
} Widget;

void tugma_handler(Widget *w, EventType ev, void *user_data) {
    const char *nom = (const char*)user_data;
    if (ev == EVENT_CLICK) {
        printf("[GUI VOQEA]: '%s' nomli vidjet (%s) BOSILDI (CLICK)!\n", w->id, nom);
    } else if (ev == EVENT_HOVER) {
        printf("[GUI VOQEA]: '%s' ustiga kursor olib kelindi (HOVER)!\n", w->id);
    }
}

void trigger_widget_event(Widget *w, EventType ev) {
    if (w->on_event != NULL) {
        w->on_event(w, ev, w->user_data);
    }
}

int main(void) {
    printf("=== HODISALARGA ASOSLANGAN GUI TIZIMI ===\n");

    Widget btn_saqlash = {
        .id = "btn_save",
        .on_event = tugma_handler,
        .user_data = "Saqlash Tugmasi"
    };

    Widget btn_bekor = {
        .id = "btn_cancel",
        .on_event = tugma_handler,
        .user_data = "Bekor Qilish Tugmasi"
    };

    // Foydalanuvchi harakatlarini simulyatsiya qilish
    trigger_widget_event(&btn_saqlash, EVENT_HOVER);
    trigger_widget_event(&btn_saqlash, EVENT_CLICK);
    trigger_widget_event(&btn_bekor, EVENT_CLICK);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu yakuniy topshiriq 14-modulning barcha bilimlarini: funksiya ko'rsatkichlari, callbacklar, `void *user_data` konteksti, voqealarga asoslangan arxitektura (Event-driven architecture) va C polimorfizmini o'z ichiga oladi.
2. GTK+, Windows Win32 API va Qt C-interfeyslari aynan shu arxitektura asosida qurilgan.

## Ishlash natijasi:
```text
=== HODISALARGA ASOSLANGAN GUI TIZIMI ===
[GUI VOQEA]: 'btn_save' ustiga kursor olib kelindi (HOVER)!
[GUI VOQEA]: 'btn_save' nomli vidjet (Saqlash Tugmasi) BOSILDI (CLICK)!
[GUI VOQEA]: 'btn_cancel' nomli vidjet (Bekor Qilish Tugmasi) BOSILDI (CLICK)!
```

---
