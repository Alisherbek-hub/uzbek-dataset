# C Dasturlash Tili — 7-Qism: Ko'rsatkichlar Asoslari (Pointers)
## (301-350 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* Manzil operatori (&) va dereference (*) mexanizmi
* NULL, Wild va Dangling pointer xavflari hamda ularning profilaktikasi
* void* umumiy ko'rsatkichi va xavfsiz type casting
* Pointer arifmetikasi (baza turiga qarab qadam tashlash, ayirma ptrdiff_t)
* const va pointerlar kombinatsiyalari (3 ta toifa)
* Double pointer (int**), Endianness tahlili va Generic Hex Viewer

---

# 301-Topshiriq: Xotira manzili va manzil operatori (&)

## Topshiriq sharti:
O'zgaruvchining RAM dagi manzilini & operatori orqali chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 100;
    printf("O'zgaruvchi qiymati: %d\n", son);
    printf("O'zgaruvchi xotira manzili: %p\n", (void*)&son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompyuter operativ xotirasi (RAM) har biri o'z manziliga (bayt indeksiga) ega bo'lgan ulkan hujayralar to'plamidir.
2. `&` operatori o'zgaruvchi joylashgan birinchi baytning xotira manzilini qaytaradi.
3. `%p` formati ushbu manzilni o'n oltilik (hex) tizimida chop etadi.

## Ishlash natijasi:
```text
O'zgaruvchi qiymati: 100
O'zgaruvchi xotira manzili: 000000000012FFE4
```

---

# 302-Topshiriq: Ko'rsatkich (Pointer) e'lon qilish va qiymat olish / dereferencing (*)

## Topshiriq sharti:
int* ko'rsatkichini e'lon qilib, * operatori orqali manzil ostidagi qiymatni o'qing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int yosh = 25;
    int *ptr = &yosh; // ptr yosh o'zgaruvchisining manzilini saqlaydi

    printf("yosh qiymati: %d\n", yosh);
    printf("ptr saqlagan manzil: %p\n", (void*)ptr);
    printf("ptr ko'rsatgan manzildagi qiymat (*ptr): %d\n", *ptr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkich (Pointer) — boshqa o'zgaruvchining xotira manzilini saqlaydigan maxsus o'zgaruvchidir.
2. E'londagi `*` (masalan `int *ptr`) bu o'zgaruvchining ko'rsatkich ekanligini bildiradi.
3. Ifodadagi `*` (masalan `*ptr`) dereferencing (manzildagi qiymatni ochish) amali deb ataladi.

## Ishlash natijasi:
```text
yosh qiymati: 25
ptr saqlagan manzil: 000000000012FFE4
ptr ko'rsatgan manzildagi qiymat (*ptr): 25
```

---

# 303-Topshiriq: Pointer orqali o'zgaruvchi qiymatini bevosita o'zgartirish

## Topshiriq sharti:
O'zgaruvchining nomiga tegmasdan, faqat ko'rsatkich orqali qiymatini yangilang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int hisob = 500;
    int *p = &hisob;

    printf("Dastlabki hisob: %d\n", hisob);

    *p = 1000; // hisob turgan xotira manziliga yangi 1000 qiymati yoziladi

    printf("Yangilangan hisob: %d\n", hisob);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `*p = 1000;` amali `p` ko'rsatib turgan manzilga to'g'ridan-to'g'ri boradi va 1000 qiymatini yozadi.
2. Natijada asl `hisob` o'zgaruvchisining qiymati o'zgaradi.

## Ishlash natijasi:
```text
Dastlabki hisob: 500
Yangilangan hisob: 1000
```

---

# 304-Topshiriq: Pointer o'lchami: 32-bit va 64-bit arxitekturalarda sizeof(ptr)

## Topshiriq sharti:
Har xil turdagi barcha pointerlarning xotirada egallagan hajmini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char *c_ptr;
    int *i_ptr;
    double *d_ptr;
    void *v_ptr;

    printf("sizeof(char*)   = %zu bayt\n", sizeof(c_ptr));
    printf("sizeof(int*)    = %zu bayt\n", sizeof(i_ptr));
    printf("sizeof(double*) = %zu bayt\n", sizeof(d_ptr));
    printf("sizeof(void*)   = %zu bayt\n", sizeof(v_ptr));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkich qaysi turga (`char`, `int`, `double`) qaratilganidan qat'i nazar, barcha ko'rsatkichlarning o'lchami bir xil bo'ladi.
2. Chunki ularning barchasi xotira manzilini saqlaydi: 32-bitli tizimlarda 4 bayt, 64-bitli tizimlarda 8 bayt.

## Ishlash natijasi:
```text
sizeof(char*)   = 8 bayt
sizeof(int*)    = 8 bayt
sizeof(double*) = 8 bayt
sizeof(void*)   = 8 bayt
```

---

# 305-Topshiriq: NULL pointer tushunchasi va xavfsiz initsializatsiya

## Topshiriq sharti:
NULL ko'rsatkich yaratib, uning qiymatini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int *ptr = NULL; // Hozircha hech qanday manzilga qaratilmagan

    printf("NULL pointer qiymati: %p\n", (void*)ptr);

    if (ptr == NULL) {
        printf("Ko'rsatkich bo'sh (NULL), xavfsiz holatda.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `NULL` — `(void*)0` deb belgilangan doimiy bo'lib, xotiradagi 0-manzilni bildiradi.
2. 0-manzil operatsion tizim tomonidan himoyalangan bo'lib, unga murojaat qilish darhol taqiqlanadi.
3. Hali manzil biriktirilmagan ko'rsatkichlarni doimo `NULL` bilan initsializatsiya qilish shart!

## Ishlash natijasi:
```text
NULL pointer qiymati: 0000000000000000
Ko'rsatkich bo'sh (NULL), xavfsiz holatda.
```

---

# 306-Topshiriq: Pointer xavfsizligi: Har doim ishlatishdan oldin if (ptr != NULL) tekshiruvi

## Topshiriq sharti:
NULL ko'rsatkichni dereference qilish halokatini oldini olish.

## Yechim (C kodi):
```c
#include <stdio.h>

void xavfsiz_chop(const int *p) {
    if (p == NULL) {
        printf("XATO: Ko'rsatkich NULL! Amal to'xtatildi.\n");
        return;
    }
    printf("Qiymat: %d\n", *p);
}

int main(void) {
    int son = 77;
    int *yaroqli = &son;
    int *yaroqsiz = NULL;

    xavfsiz_chop(yaroqli);
    xavfsiz_chop(yaroqsiz);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar `*yaroqsiz` tekshiruvsiz chaqirilsa, tizim halokati (Segmentation Fault / Access Violation) sodir bo'ladi.
2. Har bir jiddiy C funksiyasining birinchi qatori ko'rsatkichlarning `NULL` emasligini tekshirishdan boshlanishi shart.

## Ishlash natijasi:
```text
Qiymat: 77
XATO: Ko'rsatkich NULL! Amal to'xtatildi.
```

---

# 307-Topshiriq: Wild pointer (Initsializatsiya qilinmagan yovvoyi ko'rsatkich) xavfi

## Topshiriq sharti:
Initsializatsiya qilinmagan pointerning xavfini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // XAVFLI: int *wild_ptr; // Qiymati tasodifiy axlat manzil!
    // *wild_ptr = 50;        // Tizim xotirasini buzadi yoki dasturni yiqitadi!

    // TO'G'RI:
    int *xavfsiz_ptr = NULL;
    int x = 50;
    xavfsiz_ptr = &x;

    printf("Xavfsiz ptr ko'rsatgan qiymat: %d\n", *xavfsiz_ptr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 'Wild Pointer' — boshlang'ich qiymat berilmagan lokal ko'rsatkich bo'lib, uning ichida tasodifiy xotira manzili (garbage address) yotadi.
2. Bunday ko'rsatkichga ma'lumot yozish kompyuter xotirasidagi muhim ma'lumotlarni buzib yuborishi mumkin.

## Ishlash natijasi:
```text
Xavfsiz ptr ko'rsatgan qiymat: 50
```

---

# 308-Topshiriq: Dangling pointer va uni bartaraf qilish (ptr = NULL uslubi)

## Topshiriq sharti:
Xotira ozod etilgach yoki o'zgaruvchi yo'qolgach pointerni NULL qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *p = (int*)malloc(sizeof(int));
    *p = 42;

    printf("Ajratilgan qiymat: %d\n", *p);

    free(p);    // Xotira operatsion tizimga qaytarildi
    p = NULL;   // Dangling pointer bo'lmasligi uchun darhol NULL qilindi!

    if (p == NULL) {
        printf("Ko'rsatkich muvaffaqiyatli xavfsizlantirildi (NULL qilingan).\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 'Dangling Pointer' — allaqachon ozod qilingan yoki yo'q bo'lgan xotira manzilini ko'rsatib turgan ko'rsatkichdir.
2. `free(p)` dan so'ng darhol `p = NULL;` yozish ko'rsatkichni xavfsiz holatga keltiradi.

## Ishlash natijasi:
```text
Ajratilgan qiymat: 42
Ko'rsatkich muvaffaqiyatli xavfsizlantirildi (NULL qilingan).
```

---

# 309-Topshiriq: void pointer (void*) — Umumiy (Generic) ko'rsatkich

## Topshiriq sharti:
void* turidan foydalanib har xil ma'lumot turlari manzilini qabul qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

void universal_chop(void *ptr, char tur) {
    if (tur == 'i') {
        printf("Butun son: %d\n", *(int*)ptr);
    } else if (tur == 'f') {
        printf("Haqiqiy son: %.2f\n", *(float*)ptr);
    } else if (tur == 'c') {
        printf("Belgi: %c\n", *(char*)ptr);
    }
}

int main(void) {
    int son = 10;
    float pi = 3.14f;
    char belgi = 'Q';

    universal_chop(&son, 'i');
    universal_chop(&pi, 'f');
    universal_chop(&belgi, 'c');
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `void*` har qanday ma'lumot turining manzilini o'zida saqlay oladi.
2. Muhim qoida: `void*` ni to'g'ridan-to'g'ri dereference qilib bo'lmaydi (`*ptr` xato); avval uni aniq tipga cast qilish shart (`*(int*)ptr`).

## Ishlash natijasi:
```text
Butun son: 10
Haqiqiy son: 3.14
Belgi: Q
```

---

# 310-Topshiriq: void* ni aniq turga majburiy cast qilib o'qish

## Topshiriq sharti:
void* orqali uzatilgan 4 baytli int massivining birinchi elementini o'qing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 9999;
    void *v = &son;

    int *i_ptr = (int*)v; // void* ni int* ga aylantirish
    printf("Qiymat: %d\n", *i_ptr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da `void*` boshqa ko'rsatkich turiga avtomatik o'tishi mumkin, lekin uni aniq yozish (`(int*)v`) kodning niyatini oydinlashtiradi.

## Ishlash natijasi:
```text
Qiymat: 9999
```

---

# 311-Topshiriq: Pointer arifmetikasi: ptr + 1 qadamining baza tipiga bog'liqligi

## Topshiriq sharti:
int* ko'rsatkichiga 1 qo'shilganda manzil necha baytga siljishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[2] = {10, 20};
    int *p = &arr[0];

    printf("p boshlang'ich manzil:  %p\n", (void*)p);
    printf("p + 1 yangi manzil:     %p\n", (void*)(p + 1));
    printf("Manzillar farqi (baytda): %td bayt\n", (char*)(p + 1) - (char*)p);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkichga 1 qo'shilsa, manzilga 1 emas, `1 * sizeof(baza_tipi)` qo'shiladi!
2. `int` 4 bayt bo'lgani sababli, `p + 1` manzilni aynan 4 bayt oldinga suradi.

## Ishlash natijasi:
```text
p boshlang'ich manzil:  000000000012FFE0
p + 1 yangi manzil:     000000000012FFE4
Manzillar farqi (baytda): 4 bayt
```

---

# 312-Topshiriq: Pointer arifmetikasi: char* (1 bayt), int* (4 bayt) va double* (8 bayt)

## Topshiriq sharti:
Uch xil turdagi ko'rsatkichlarning 1 qadamdagi siljishlarini solishtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char c = 'A';
    int i = 1;
    double d = 2.0;

    char *cp = &c;
    int *ip = &i;
    double *dp = &d;

    printf("char* siljishi:   %td bayt\n", (char*)(cp + 1) - (char*)cp);
    printf("int* siljishi:    %td bayt\n", (char*)(ip + 1) - (char*)ip);
    printf("double* siljishi: %td bayt\n", (char*)(dp + 1) - (char*)dp);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Pointer arifmetikasi xotiradagi ma'lumot turlarining o'lchamini to'liq hisobga oladi.

## Ishlash natijasi:
```text
char* siljishi:   1 bayt
int* siljishi:    4 bayt
double* siljishi: 8 bayt
```

---

# 313-Topshiriq: Pointer arifmetikasi: ptr - 1 orqaga siljish

## Topshiriq sharti:
Massiv oxiridan boshiga qarab ko'rsatkichni kamaytirib chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[] = {10, 20, 30, 40};
    int *p = &arr[3]; // Oxirgi element ko'rsatkichi

    printf("Orqadan boshlab: ");
    for (int i = 0; i < 4; i++) {
        printf("%d ", *p);
        p--; // 4 bayt orqaga siljiydi
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `p--` ko'rsatkichni massivdagi oldingi elementga suradi.

## Ishlash natijasi:
```text
Orqadan boshlab: 40 30 20 10
```

---

# 314-Topshiriq: Ikki ko'rsatkichni ayirish (ptrdiff_t tipi stddef.h)

## Topshiriq sharti:
Bir xil massivdagi ikki ko'rsatkich orasidagi elementlar sonini toping.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stddef.h>

int main(void) {
    int massiv[10] = {0};
    int *bosh = &massiv[2];
    int *oxir = &massiv[7];

    ptrdiff_t elementlar_farqi = oxir - bosh;

    printf("bosh indeksi: 2, oxir indeksi: 7\n");
    printf("Ko'rsatkichlar ayirmasi: %td ta element\n", elementlar_farqi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikki ko'rsatkich ayirilganda ularning orasidagi baytlar soni emas, balki elementlar soni hosil bo'ladi.
2. Bu natija `ptrdiff_t` maxsus signed butun son turida ifodalanadi va `%td` bilan chop etiladi.

## Ishlash natijasi:
```text
bosh indeksi: 2, oxir indeksi: 7
Ko'rsatkichlar ayirmasi: 5 ta element
```

---

# 315-Topshiriq: Pointerlarni taqqoslash (<, >, ==)

## Topshiriq sharti:
Massivni ko'rsatkichlar orqali while (ptr < oxir) siklida aylanib chiqing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int sonlar[] = {10, 20, 30, 40, 50};
    int *ptr = sonlar;
    int *oxir = sonlar + 5; // Massivdan keyingi manzil

    printf("Massiv elementlari: ");
    while (ptr < oxir) {
        printf("%d ", *ptr);
        ptr++;
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitta massivga tegishli ko'rsatkichlarni o'zaro taqqoslash mumkin.
2. `ptr < oxir` sharti pointer massiv tugashiga yetguncha siklni boshqaradi.

## Ishlash natijasi:
```text
Massiv elementlari: 10 20 30 40 50
```

---

# 316-Topshiriq: Inkrement va dereferens kombinatsiyalari: *ptr++, (*ptr)++, *++ptr, ++*ptr

## Topshiriq sharti:
To'rtta nozik kombinatsiyaning qanday ishlashini amalda ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a[] = {10, 20, 30};
    int *p = a;

    printf("1. *p++ qiymati: %d (p keyingi elementga o'tdi)\n", *p++);
    printf("   Hozir p ko'rsatayotgan qiymat: %d\n", *p);

    printf("2. (*p)++ qiymati: %d (manzildagi qiymat oshdi)\n", (*p)++);
    printf("   Hozir a[1] ning yangi qiymati: %d\n", a[1]);

    p = a; // Boshiga qaytarish
    printf("3. *++p qiymati: %d (avval p siljiydi, keyin qiymat olinadi)\n", *++p);

    printf("4. ++*p qiymati: %d (joriy qiymat darhol 1 ga oshadi)\n", ++*p);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `*p++`: avval joriy qiymat olinadi, keyin `p` pointerning o'zi siljiydi.
2. `(*p)++`: `p` turgan joyidagi qiymatni 1 ga oshiradi.
3. `*++p`: avval `p` bitta oldinga suriladi, so'ngra yangi element olinadi.
4. `++*p`: ko'rsatkich turgan elementning qiymatini oldindan oshiradi.

## Ishlash natijasi:
```text
1. *p++ qiymati: 10 (p keyingi elementga o'tdi)
   Hozir p ko'rsatayotgan qiymat: 20
2. (*p)++ qiymati: 20 (manzildagi qiymat oshdi)
   Hozir a[1] ning yangi qiymati: 21
3. *++p qiymati: 21 (avval p siljiydi, keyin qiymat olinadi)
4. ++*p qiymati: 22 (joriy qiymat darhol 1 ga oshadi)
```

---

# 317-Topshiriq: const pointer 1: Ko'rsatkich o'zgarmas qiymatga (const int *ptr)

## Topshiriq sharti:
Qiymatni o'zgartirib bo'lmaydigan, ammo pointerni boshqa manzilga yo'naltirish mumkinligini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 10, y = 20;
    const int *ptr = &x; // Qiymat o'zgarmas!

    printf("ptr ko'rsatgan qiymat: %d\n", *ptr);
    // *ptr = 15; // KOMPILYATSIYA XATOSI: assignment of read-only location

    ptr = &y; // Mumkin! Pointer boshqa manzilga ko'rsatishi mumkin
    printf("ptr endi y ni ko'rsatmoqda: %d\n", *ptr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const int *ptr` (yoki `int const *ptr`): ko'rsatkich orqali qiymatni o'zgartirish taqiqlanadi (read-only data).
2. Lekin `ptr` ning o'zini boshqa manzilga o'tkazish mumkin.

## Ishlash natijasi:
```text
ptr ko'rsatgan qiymat: 10
ptr endi y ni ko'rsatmoqda: 20
```

---

# 318-Topshiriq: const pointer 2: O'zgarmas ko'rsatkich (int * const ptr)

## Topshiriq sharti:
Manzili o'zgarmaydigan, ammo qiymatini o'zgartirish mumkin bo'lgan ko'rsatkich.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 100;
    int y = 200;
    int * const ptr = &x; // Ko'rsatkichning o'zi o'zgarmas!

    *ptr = 150; // Mumkin! Qiymatni o'zgartirishga ruxsat bor
    printf("x ning yangi qiymati: %d\n", x);

    // ptr = &y; // KOMPILYATSIYA XATOSI: assignment of read-only variable 'ptr'
    (void)y;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int * const ptr`: ko'rsatkich biriktirilgan manzilga 'mixlangan' (doimiy).
2. U boshqa manzilni ko'rsata olmaydi, ammo uning manzilidagi ma'lumotni o'zgartirish mumkin.

## Ishlash natijasi:
```text
x ning yangi qiymati: 150
```

---

# 319-Topshiriq: const pointer 3: O'zgarmas manzil va o'zgarmas qiymat (const int * const ptr)

## Topshiriq sharti:
Hech narsasini o'zgartirib bo'lmaydigan to'liq himoyalangan ko'rsatkich.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 55;
    const int * const ptr = &x;

    printf("To'liq himoyalangan qiymat: %d\n", *ptr);
    // *ptr = 60; // XATO!
    // ptr = NULL; // XATO!
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const int * const ptr`: na manzilni, na u ko'rsatgan qiymatni o'zgartirib bo'ladi.
2. Bu apparat konfiguratsiyalari va tizim konstantalarini himoyalashning eng yuqori darajasidir.

## Ishlash natijasi:
```text
To'liq himoyalangan qiymat: 55
```

---

# 320-Topshiriq: Haqiqiy swap(&a, &b) ni pointerlar yordamida amalga oshirish

## Topshiriq sharti:
Ikki o'zgaruvchi qiymatini manzil uzatish orqali o'rin almashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main(void) {
    int x = 10, y = 20;
    printf("Oldin: x = %d, y = %d\n", x, y);
    swap(&x, &y);
    printf("Keyin: x = %d, y = %d\n", x, y);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiyaga o'zgaruvchilarning manzillari (`&x`, `&y`) uzatiladi.
2. `*a` va `*b` orqali ularning asl xotira yacheykalaridagi qiymatlari almashtiriladi.

## Ishlash natijasi:
```text
Oldin: x = 10, y = 20
Keyin: x = 20, y = 10
```

---

# 321-Topshiriq: Bitta funksiyadan pointerlar orqali min va max qiymatlarni qaytarish

## Topshiriq sharti:
Massivdagi eng kichik va eng katta sonlarni bitta o'tishda qaytaring.

## Yechim (C kodi):
```c
#include <stdio.h>

void min_max_top(const int *arr, int len, int *min, int *max) {
    *min = arr[0];
    *max = arr[0];
    for (int i = 1; i < len; i++) {
        if (arr[i] < *min) *min = arr[i];
        if (arr[i] > *max) *max = arr[i];
    }
}

int main(void) {
    int sonlar[] = {23, 7, 89, 45, -2, 61};
    int eng_kichik, eng_katta;

    min_max_top(sonlar, 6, &eng_kichik, &eng_katta);
    printf("Min: %d, Max: %d\n", eng_kichik, eng_katta);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiya return siz ishlaydi va natijalarni `*min` va `*max` ko'rsatkichlari orqali tashqariga yozadi.

## Ishlash natijasi:
```text
Min: -2, Max: 89
```

---

# 322-Topshiriq: Ko'rsatkichga ko'rsatkich (Double Pointer: int**)

## Topshiriq sharti:
Pointerning manzilini saqlaydigan ikkinchi darajali ko'rsatkichni tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int qiymat = 500;
    int *ptr = &qiymat;
    int **dptr = &ptr; // ptr ning manzilini saqlaydi

    printf("qiymat:            %d\n", qiymat);
    printf("*ptr orqali:       %d\n", *ptr);
    printf("**dptr orqali:     %d\n", **dptr);
    printf("ptr manzili:       %p\n", (void*)&ptr);
    printf("dptr qiymati:      %p\n", (void*)dptr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `dptr` — bu pointerga ko'rsatkichdir (`int**`).
2. `*dptr` — `ptr` ning qiymatini (ya'ni `qiymat` ning manzilini) beradi.
3. `**dptr` — ikki marta dereference qilib asl `qiymat` ni (500) oladi.

## Ishlash natijasi:
```text
qiymat:            500
*ptr orqali:       500
**dptr orqali:     500
ptr manzili:       000000000012FFE8
dptr qiymati:      000000000012FFE8
```

---

# 323-Topshiriq: int** orqali asosiy o'zgaruvchi qiymatini masofadan o'zgartirish

## Topshiriq sharti:
Ikki marta dereferens qilib asl sonni yangilang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 10;
    int *p = &a;
    int **pp = &p;

    **pp = 99; // a ning qiymati o'zgaradi

    printf("a ning yangi qiymati: %d\n", a);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `**pp = 99` zanjir bo'ylab `a` ga yetib boradi va uni o'zgartiradi.

## Ishlash natijasi:
```text
a ning yangi qiymati: 99
```

---

# 324-Topshiriq: Funksiyada ko'rsatkichning o'zini o'zgartirish uchun int** uzatish

## Topshiriq sharti:
Pointerning ko'rsatib turgan manzilini boshqa o'zgaruvchiga o'tkazuvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

void boshqa_manzilga_yonalaylik(int **ptr_ref, int *yangi_manzil) {
    *ptr_ref = yangi_manzil; // Pointerning o'zi o'zgartirilmoqda!
}

int main(void) {
    int a = 10, b = 20;
    int *p = &a;

    printf("Oldin *p: %d\n", *p);
    boshqa_manzilga_yonalaylik(&p, &b);
    printf("Keyin *p: %d\n", *p);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar pointerning o'zini (u qayerga ko'rsatishini) funksiya ichida o'zgartirmoqchi bo'lsak, uning manzilini (`int**`) uzatishimiz shart.
2. Bu dinamik xotira ajratishda (`allocate(&ptr, size)`) juda mashhur uslubdir.

## Ishlash natijasi:
```text
Oldin *p: 10
Keyin *p: 20
```

---

# 325-Topshiriq: Ko'rsatkichlar zanjiri (Triple Pointer: int***)

## Topshiriq sharti:
Uch darajali ko'rsatkich orqali qiymatga murojaat qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 42;
    int *p1 = &x;
    int **p2 = &p1;
    int ***p3 = &p2;

    printf("***p3 = %d\n", ***p3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Nazariy jihatdan pointerlar zanjiri istalgancha chuqur bo'lishi mumkin.
2. Har bir `*` zanjirning bitta bo'g'inini ochadi.

## Ishlash natijasi:
```text
***p3 = 42
```

---

# 326-Topshiriq: Xotira baytlarini tahlil qilish: int ning har bir baytini unsigned char* bilan o'qish

## Topshiriq sharti:
32-bitli butun sonning 4 ta baytini ketma-ket chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 0x12345678;
    unsigned char *baytlar = (unsigned char*)&son;

    printf("0x12345678 ning xotiradagi baytlari:\n");
    for (size_t i = 0; i < sizeof(son); i++) {
        printf("Bayt %zu: 0x%02X\n", i, baytlar[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `(unsigned char*)&son` int manzilini 1 baytli qadamlarga bo'lib beradi.
2. x86 protsessorlarida birinchi bayt `0x78` (eng kichik bayt) bo'lib chiqadi, bu Little-Endian arxitekturasini isbotlaydi.

## Ishlash natijasi:
```text
0x12345678 ning xotiradagi baytlari:
Bayt 0: 0x78
Bayt 1: 0x56
Bayt 2: 0x34
Bayt 3: 0x12
```

---

# 327-Topshiriq: Tizim Endianness (Little vs Big Endian) ni pointer orqali aniqlash

## Topshiriq sharti:
Joriy kompyuter qaysi bayt tartibidan foydalanishini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    unsigned int test = 1;
    unsigned char *c = (unsigned char*)&test;

    if (*c == 1) {
        printf("Tizim arxitekturasi: Little-Endian\n");
    } else {
        printf("Tizim arxitekturasi: Big-Endian\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `test = 1` xotirada 4 bayt bo'ladi.
2. Agar birinchi baytda 1 tursa — Little-Endian (pastki bayt pastki manzilda).
3. Agar to'rtinchi baytda 1 tursa — Big-Endian.

## Ishlash natijasi:
```text
Tizim arxitekturasi: Little-Endian
```

---

# 328-Topshiriq: Bit patternlarini pointer bilan o'qish: float sonni uint32_t* orqali talqin qilish

## Topshiriq sharti:
float sonning IEEE 754 bitlarini butun son sifatida o'qing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    float f = 1.0f;
    uint32_t *u_ptr = (uint32_t*)&f;

    printf("Float: %.1f\n", f);
    printf("IEEE 754 Binar (Hex): 0x%08X\n", *u_ptr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. IEEE 754 standartiga ko'ra 1.0f sonining binar ko'rinishi `0x3F800000` ga teng.
2. Pointer casting orqali biz float xotirasini butun son sifatida to'g'ridan-to'g'ri o'qiy olamiz (Type Punning).

## Ishlash natijasi:
```text
Float: 1.0
IEEE 754 Binar (Hex): 0x3F800000
```

---

# 329-Topshiriq: O'z memset() funktsiyangizni void* yordamida yozish

## Topshiriq sharti:
Xotira blokini berilgan bayt qiymati bilan to'ldiruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

void* mening_memset(void *manzil, int qiymat, size_t baytlar) {
    unsigned char *p = (unsigned char*)manzil;
    for (size_t i = 0; i < baytlar; i++) {
        p[i] = (unsigned char)qiymat;
    }
    return manzil;
}

int main(void) {
    char matn[6] = "AAAAA";
    mening_memset(matn, 'Z', 3);
    printf("Natija: %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Standart `memset` kabi, xotirani baytma-bayt to'ldirish uchun `void*` avval `unsigned char*` ga o'giriladi.

## Ishlash natijasi:
```text
Natija: ZZZAA
```

---

# 330-Topshiriq: O'z memcpy() funktsiyangizni yozish

## Topshiriq sharti:
Bir xotira blokidan ikkinchisiga baytlarni ko'chiruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

void* mening_memcpy(void *manzil_c, const void *manzil_b, size_t baytlar) {
    char *dest = (char*)manzil_c;
    const char *src = (const char*)manzil_b;
    for (size_t i = 0; i < baytlar; i++) {
        dest[i] = src[i];
    }
    return manzil_c;
}

int main(void) {
    int manba[3] = {100, 200, 300};
    int nishon[3];

    mening_memcpy(nishon, manba, sizeof(manba));
    printf("Nusxalangan: %d, %d, %d\n", nishon[0], nishon[1], nishon[2]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Barcha xotira bloklarini (int massivi bo'lsa ham) baytlar soni bo'yicha to'liq nusxalaydi.

## Ishlash natijasi:
```text
Nusxalangan: 100, 200, 300
```

---

# 331-Topshiriq: O'z memcmp() funktsiyangizni yozish

## Topshiriq sharti:
Ikki xotira blokining baytlarini solishtiruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

int mening_memcmp(const void *p1, const void *p2, size_t n) {
    const unsigned char *s1 = (const unsigned char*)p1;
    const unsigned char *s2 = (const unsigned char*)p2;
    for (size_t i = 0; i < n; i++) {
        if (s1[i] != s2[i]) {
            return s1[i] - s2[i];
        }
    }
    return 0;
}

int main(void) {
    char b1[] = "ABC";
    char b2[] = "ABD";
    printf("memcmp natijasi: %d\n", mening_memcmp(b1, b2, 3));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Baytlar teng bo'lsa 0, birinchisi kichik bo'lsa manfiy, katta bo'lsa musbat qaytaradi ('C' - 'D' = -1).

## Ishlash natijasi:
```text
memcmp natijasi: -1
```

---

# 332-Topshiriq: Pointerlar orqali massiv elementlariga nisbatan masofani hisoblash

## Topshiriq sharti:
Pointerlar yordamida qidirilayotgan elementning indeksini toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[] = {10, 20, 30, 40, 50};
    int *bosh = arr;
    int *topilgan = NULL;

    for (int *p = arr; p < arr + 5; p++) {
        if (*p == 40) {
            topilgan = p;
            break;
        }
    }

    if (topilgan != NULL) {
        printf("40 soni indeksda: %td\n", topilgan - bosh);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `topilgan - bosh` formulasi hech qanday `i` hisoblagichisiz indeksni beradi.

## Ishlash natijasi:
```text
40 soni indeksda: 3
```

---

# 333-Topshiriq: Pointerlar massivi (Array of pointers) asoslari

## Topshiriq sharti:
Bir nechta turli satrlarga ko'rsatkichlar massivini yarating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    const char *shaharlar[] = {"Toshkent", "Samarqand", "Buxoro", "Xiva"};

    for (int i = 0; i < 4; i++) {
        printf("%d-shahar: %s (Manzili: %p)\n", i + 1, shaharlar[i], (void*)shaharlar[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `char *shaharlar[]` — elementlarining o'zi ko'rsatkich bo'lgan massivdir.
2. Har bir satr xotirada turli uzunlikda bo'lishi mumkin, bu xotirani maksimal darajada tejaydi.

## Ishlash natijasi:
```text
1-shahar: Toshkent (Manzili: 0000000000404000)
2-shahar: Samarqand (Manzili: 0000000000404010)
3-shahar: Buxoro (Manzili: 0000000000404020)
4-shahar: Xiva (Manzili: 0000000000404030)
```

---

# 334-Topshiriq: Ko'rsatkich yordamida massiv chegaralarini nazorat qilish

## Topshiriq sharti:
Pointer chegaradan o'tib ketmasligini ta'minlovchi xavfsiz iteratsiya.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[3] = {100, 200, 300};
    int *bosh = arr;
    int *chegara = arr + 3;

    for (int *p = bosh; p < chegara; p++) {
        printf("%d ", *p);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `arr + 3` massivning 'past-the-end' (oxiridan keyingi) ruxsat etilgan manzilidir.
2. `p < chegara` sharti chegaradan chiqib ketishni 100% bartaraf etadi.

## Ishlash natijasi:
```text
100 200 300
```

---

# 335-Topshiriq: uintptr_t bilan pointerni butun son arifmetikasiga aylantirish

## Topshiriq sharti:
Ko'rsatkich manzilini butun son sifatida tahlil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    int son = 42;
    int *ptr = &son;

    uintptr_t u_manzil = (uintptr_t)ptr;

    printf("Asl pointer: %p\n", (void*)ptr);
    printf("uintptr_t qiymati: 0x%jx\n", (uintmax_t)u_manzil);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `uintptr_t` ko'rsatkichni xavfsiz butun songa aylantiradi va apparat darajasidagi manzillar bilan amallar bajarishga ruxsat beradi.

## Ishlash natijasi:
```text
Asl pointer: 000000000012FFE4
uintptr_t qiymati: 0x12ffe4
```

---

# 336-Topshiriq: Xotira to'g'rilanishi (Pointer Alignment) ni tekshirish

## Topshiriq sharti:
Pointer 4 bayt yoki 8 bayt chegarasiga tekislanganligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

bool tekislanganmi(const void *ptr, size_t alignment) {
    return ((uintptr_t)ptr % alignment) == 0;
}

int main(void) {
    int x = 10;
    int *p = &x;

    printf("Manzil: %p\n", (void*)p);
    printf("4-baytga tekislanganmi: %s\n", tekislanganmi(p, 4) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. To'g'ri tekislangan ko'rsatkichlar CPU tomonidan eng tezkor tezlikda qayta ishlanadi.

## Ishlash natijasi:
```text
Manzil: 000000000012FFE4
4-baytga tekislanganmi: Ha
```

---

# 337-Topshiriq: O'zgarmas string literali ko'rsatkichi (const char *s = 'Salom')

## Topshiriq sharti:
String literalini nima uchun doimo const char* ga biriktirish kerakligini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // char *s = "Salom"; // XAVFLI! Literal Read-Only Data segmentda saqlanadi
    // s[0] = 'X';        // Halokat: Segmentation fault!

    // TO'G'RI:
    const char *s = "Salom";
    printf("Satr: %s\n", s);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qo'shtirnoqdagi matn literallari `.rodata` segmentida saqlanadi.
2. `const char *s` yozilsa, kompilyator uni o'zgartirishga urinishlarni kompilyatsiya paytidayoq xato deb to'xtatadi.

## Ishlash natijasi:
```text
Satr: Salom
```

---

# 338-Topshiriq: Pointer orqali satr uzunligini (strlen) hisoblash

## Topshiriq sharti:
*ptr != '\0' bo'yicha satr oxirigacha yuruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

size_t mening_strlen(const char *s) {
    const char *p = s;
    while (*p != '\0') {
        p++;
    }
    return p - s;
}

int main(void) {
    const char *matn = "O'zbekiston";
    printf("'%s' uzunligi: %zu ta belgi\n", matn, mening_strlen(matn));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `p - s` ko'rsatkichlar ayirmasi aynan satr uzunligini beradi.

## Ishlash natijasi:
```text
'O'zbekiston' uzunligi: 11 ta belgi
```

---

# 339-Topshiriq: Pointer yordamida ikkita satrni taqqoslash (strcmp analogi)

## Topshiriq sharti:
Belgima-belgi pointer bilan solishtiruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

int mening_strcmp(const char *s1, const char *s2) {
    while (*s1 && (*s1 == *s2)) {
        s1++;
        s2++;
    }
    return *(const unsigned char*)s1 - *(const unsigned char*)s2;
}

int main(void) {
    printf("Taqqoslash ('olma', 'olma'): %d\n", mening_strcmp("olma", "olma"));
    printf("Taqqoslash ('anor', 'behi'): %d\n", mening_strcmp("anor", "behi"));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikkala ko'rsatkich birgalikda siljib boradi va birinchi farqli belgida ayirmani qaytaradi.

## Ishlash natijasi:
```text
Taqqoslash ('olma', 'olma'): 0
Taqqoslash ('anor', 'behi'): -1
```

---

# 340-Topshiriq: Pointer yordamida satrni ko'chirish (strcpy analogi)

## Topshiriq sharti:
while ((*dest++ = *src++)) ixcham C idiomasi.

## Yechim (C kodi):
```c
#include <stdio.h>

char* mening_strcpy(char *dest, const char *src) {
    char *boshlangich = dest;
    while ((*dest++ = *src++)) {
        // Tana bo'sh: nusxalash va '\0' ga tekshirish shart ichida bajariladi!
    }
    return boshlangich;
}

int main(void) {
    char manba[] = "C dasturlash";
    char nishon[20];

    mening_strcpy(nishon, manba);
    printf("Nusxa: %s\n", nishon);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `while ((*dest++ = *src++))` — Kernighan va Ritchie (K&R) kitobidagi eng mashhur C idiomasidir.
2. Har bir belgi ko'chiriladi, oxirgi ` ` (0) ko'chirilganda shart yolg'on bo'lib sikl to'xtaydi.

## Ishlash natijasi:
```text
Nusxa: C dasturlash
```

---

# 341-Topshiriq: Pointerlar va dinamik massivlar o'rtasidagi bog'liqlik

## Topshiriq sharti:
malloc qaytargan ko'rsatkichdan xuddi oddiy massiv kabi foydalanish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *arr = (int*)malloc(3 * sizeof(int));
    if (arr == NULL) return 1;

    arr[0] = 10;
    arr[1] = 20;
    arr[2] = 30;

    printf("Dinamik massiv: %d %d %d\n", arr[0], arr[1], arr[2]);
    free(arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da `arr[i]` sintaksisi aslida `*(arr + i)` ning qulay yozilish shaklidir.
2. Shuning uchun dinamik ko'rsatkichga ham `[]` orqali murojaat qilish mumkin.

## Ishlash natijasi:
```text
Dinamik massiv: 10 20 30
```

---

# 342-Topshiriq: Rekursiv funksiyada pointerni parametr sifatida siljitib borish

## Topshiriq sharti:
Massiv elementlarini rekursiv ko'rsatkich orqali chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

void rekursiv_chop_ptr(const int *ptr, int qoldi) {
    if (qoldi <= 0) return;
    printf("%d ", *ptr);
    rekursiv_chop_ptr(ptr + 1, qoldi - 1);
}

int main(void) {
    int arr[] = {7, 14, 21};
    rekursiv_chop_ptr(arr, 3);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir rekursiv chaqiruvda ko'rsatkich 1 element oldinga suriladi (`ptr + 1`).

## Ishlash natijasi:
```text
7 14 21
```

---

# 343-Topshiriq: O'zgaruvchining manzilini chop etishda (void*) ga cast qilish zarurati

## Topshiriq sharti:
Nima uchun %p ga argument uzatganda (void*) casti qo'yilishi lozim?

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 42;
    // C standartida printf("%p", (void*)&son); qat'iy talab qilinadi
    printf("Standartga 100%% mos manzil: %p\n", (void*)&son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C standarti bo'yicha `%p` spetsifikatori aynan `void*` turidagi argumentni kutadi.
2. Boshqa ko'rsatkich turlarini `(void*)` ga o'girmaslik ayrim platformalarda xatolikka olib kelishi mumkin.

## Ishlash natijasi:
```text
Standartga 100% mos manzil: 000000000012FFE4
```

---

# 344-Topshiriq: Pointerlar orqali sikllarda yuqori tezlikka erishish

## Topshiriq sharti:
Indeks bo'yicha murojaat vs Ko'rsatkichni oshirib borish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[4] = {1, 2, 3, 4};
    int sum = 0;

    // Ko'rsatkichli yurish (indeks ko'paytmasisiz to'g'ridan-to'g'ri qadam tashlaydi)
    for (int *p = arr; p < arr + 4; p++) {
        sum += *p;
    }

    printf("Ko'rsatkichli sikl yig'indisi: %d\n", sum);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `arr[i]` har safar `baza + i * 4` manzil hisobini talab qiladi.
2. `p++` esa manzilni oddiy qo'shish bilan siljitadi, bu dastur tezligini oshiradi.

## Ishlash natijasi:
```text
Ko'rsatkichli sikl yig'indisi: 10
```

---

# 345-Topshiriq: Strict Aliasing qoidasi tushunchasi va char* istisnosi

## Topshiriq sharti:
Turli tiplar o'rtasida pointer castingning standart chegaralari.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 0x12345678;
    // C da int* va float* bir-birini alias qila olmaydi (Strict Aliasing).
    // Lekin char* va unsigned char* barcha tiplarning baytlarini o'qish huquqiga ega!
    
    char *bayt = (char*)&a;
    printf("char* orqali birinchi bayt: 0x%02X\n", (unsigned char)*bayt);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyator optimizatsiyasi bir xil xotiraga turli turlar ko'rsatmaydi deb faraz qiladi (Strict Aliasing).
2. Faqat `char*` har qanday xotira blokini qonuniy ravishda o'qiy oladi.

## Ishlash natijasi:
```text
char* orqali birinchi bayt: 0x78
```

---

# 346-Topshiriq: Xotira xavfsizligi: Dangling pointerlarni aniqlash va himoyalash funktsiyasi

## Topshiriq sharti:
Xotirani tozalab, pointerni avtomatik NULL qiluvchi xavfsiz free makrosi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

#define XAVFSIZ_FREE(ptr) do { free(ptr); (ptr) = NULL; } while(0)

int main(void) {
    int *p = (int*)malloc(sizeof(int));
    *p = 100;

    printf("Qiymat: %d\n", *p);
    XAVFSIZ_FREE(p);

    if (p == NULL) {
        printf("XAVFSIZ_FREE muvaffaqiyatli ishladi: p endi NULL!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Makros bir vaqtda ham `free` qiladi, ham pointerni `NULL` ga tenglashtiradi.
2. Bu qayta `free` (double free) va dangling pointer xatolarining oldini oladi.

## Ishlash natijasi:
```text
Qiymat: 100
XAVFSIZ_FREE muvaffaqiyatli ishladi: p endi NULL!
```

---

# 347-Topshiriq: O'z xotira tozalovchi bzero() funktsiyangizni yozish

## Topshiriq sharti:
Xotira blokini to'liq 0 baytlari bilan tozalash.

## Yechim (C kodi):
```c
#include <stdio.h>

void mening_bzero(void *s, size_t n) {
    unsigned char *p = (unsigned char*)s;
    while (n--) {
        *p++ = 0;
    }
}

int main(void) {
    int arr[3] = {10, 20, 30};
    mening_bzero(arr, sizeof(arr));

    printf("Tozalangan massiv: %d %d %d\n", arr[0], arr[1], arr[2]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. BSD tizimlaridagi klassik `bzero` funktsiyasining sodda va toza realizatsiyasi.

## Ishlash natijasi:
```text
Tozalangan massiv: 0 0 0
```

---

# 348-Topshiriq: Ko'rsatkich offsetini hisoblash (offsetof makrosi stddef.h)

## Topshiriq sharti:
Struktura a'zosi struktura boshidan necha bayt uzoqlikda joylashganini toping.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stddef.h>

struct Foydalanuvchi {
    char id;
    int yosh;
    double balans;
};

int main(void) {
    printf("id offseti:     %zu bayt\n", offsetof(struct Foydalanuvchi, id));
    printf("yosh offseti:   %zu bayt\n", offsetof(struct Foydalanuvchi, yosh));
    printf("balans offseti: %zu bayt\n", offsetof(struct Foydalanuvchi, balans));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `offsetof` ko'rsatkichlar arifmetikasi orqali strukturadagi har bir maydonning boshlang'ich baytdan siljishini hisoblaydi.

## Ishlash natijasi:
```text
id offseti:     0 bayt
yosh offseti:   4 bayt
balans offseti: 8 bayt
```

---

# 349-Topshiriq: Volatile ko'rsatkich (volatile int *ptr) va apparat registrlari

## Topshiriq sharti:
Kompilyator keshlamasdan har safar RAM dan o'qishi kerak bo'lgan ko'rsatkich.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int apparat_registri = 0xAA;
    volatile int *reg_ptr = &apparat_registri;

    printf("Registr qiymati: 0x%02X\n", *reg_ptr);
    *reg_ptr = 0xBB;
    printf("Yangi qiymat: 0x%02X\n", *reg_ptr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `volatile` kalit so'zi kompilyatorga: 'ushbu xotira tashqi apparat tomonidan istalgan soniyada o'zgarishi mumkin, uni keshlab qolma' degan ma'noni bildiradi.

## Ishlash natijasi:
```text
Registr qiymati: 0xAA
Yangi qiymat: 0xBB
```

---

# 350-Topshiriq: Modul yakuni: Generic Memory Hex Viewer (Xotira dumpini ko'rsatuvchi dastur)

## Topshiriq sharti:
Ixtiyoriy xotira manzilining baytlarini o'n oltilik shaklda konsolga chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

void hex_dump(const void *manzil, size_t olcham) {
    const unsigned char *p = (const unsigned char*)manzil;
    printf("Manzil: %p | ", manzil);
    for (size_t i = 0; i < olcham; i++) {
        printf("%02X ", p[i]);
    }
    printf("\n");
}

int main(void) {
    int son = 0xDEADBEEF;
    char satr[] = "TEST";

    hex_dump(&son, sizeof(son));
    hex_dump(satr, sizeof(satr));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Hex Viewer tizimli dasturchilar va xavfsizlik mutaxassislarining eng asosiy qurolidir.
2. `void*` va `unsigned char*` orqali har qanday ob'ekt xotirasi baytma-bayt ko'rib chiqiladi.
3. Bu topshiriq 7-qismning barcha pointer konsepsiyalarini umumlashtiradi.

## Ishlash natijasi:
```text
Manzil: 000000000012FFE0 | EF BE AD DE 
Manzil: 000000000012FFD0 | 54 45 53 54 00
```

---
