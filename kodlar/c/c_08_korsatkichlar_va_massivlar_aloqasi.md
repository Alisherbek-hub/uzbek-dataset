# C Dasturlash Tili — 8-Qism: Ko'rsatkichlar va Massivlar Aloqasi
## (351-400 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* Massiv nomining ko'rsatkichga aylanishi (Array decay) va arr[i] == *(arr + i)
* i[arr] sintaksisi, &arr vs arr farqi (int (*)[N] vs int*)
* Ko'rsatkichlar massivi (char *argv[]) va massivga ko'rsatkich
* 2D massivlarning pointer arifmetikasi: *(*(mat + i) + j)
* Dinamik 2D massivlar (Contiguous vs Non-contiguous)
* Manfiy indekslash (mid[-1]), Two Sum algoritmi va o'z strtok realizatsiyasi

---

# 351-Topshiriq: Massiv nomi va uning birinchi element ko'rsatkichiga aylanishi (Array Decay)

## Topshiriq sharti:
Massiv nomi uning 0-indeksdagi elementi manziliga teng ekanligini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[3] = {10, 20, 30};

    printf("Massiv nomi qiymati (arr):     %p\n", (void*)arr);
    printf("Birinchi element manzili (&arr[0]): %p\n", (void*)&arr[0]);

    if ((void*)arr == (void*)&arr[0]) {
        printf("Ikkala manzil mutlaqo bir xil!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida ko'p hollarda massiv nomi avtomatik tarzda uning birinchi elementining ko'rsatkichiga aylanadi (Decay to pointer).
2. Shuning uchun `arr` va `&arr[0]` bir xil xotira manzilini ifodalaydi.

## Ishlash natijasi:
```text
Massiv nomi qiymati (arr):     000000000012FFE0
Birinchi element manzili (&arr[0]): 000000000012FFE0
Ikkala manzil mutlaqo bir xil!
```

---

# 352-Topshiriq: arr[i] aslida *(arr + i) ekanligining isboti

## Topshiriq sharti:
Kvadrat qavs [] operatorining pointer arifmetikasi ekanligini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int sonlar[] = {100, 200, 300};

    for (int i = 0; i < 3; i++) {
        printf("sonlar[%d] = %d | *(sonlar + %d) = %d\n", 
               i, sonlar[i], i, *(sonlar + i));
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida `arr[i]` bu mustaqil buyruq emas, balki `*(arr + i)` sintaktik qulayligidir (Syntactic sugar).
2. Kompilyator `arr[i]` ni ko'rishi bilan uni `*(arr + i)` ko'rinishida talqin qiladi.

## Ishlash natijasi:
```text
sonlar[0] = 100 | *(sonlar + 0) = 100
sonlar[1] = 200 | *(sonlar + 1) = 200
sonlar[2] = 300 | *(sonlar + 2) = 300
```

---

# 353-Topshiriq: Qiziqarli C sintaksisi: i[arr] ning qonuniyligi va sababi

## Topshiriq sharti:
Nima uchun 2[arr] ifodasi arr[2] bilan bir xil ishlashini namoyish eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[] = {11, 22, 33, 44};

    printf("arr[2] orqali: %d\n", arr[2]);
    printf("2[arr] orqali: %d\n", 2[arr]);

    // Sababi: arr[2] == *(arr + 2) == *(2 + arr) == 2[arr]
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qo'shish amali kommutativdir: `arr + 2 == 2 + arr`.
2. Shuning uchun `*(2 + arr)` ifodasi `2[arr]` ko'rinishida ham yozilishi mumkin.
3. Bu C tilida indekslash aslida pointer siljitish ekanligining yaqqol isbotidir.

## Ishlash natijasi:
```text
arr[2] orqali: 33
2[arr] orqali: 33
```

---

# 354-Topshiriq: Ko'rsatkich yordamida massiv elementlarini indekslarsiz aylanib chiqish

## Topshiriq sharti:
Faqat pointerni oshirib borish orqali massivni chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int sonlar[] = {5, 10, 15, 20};
    int *p = sonlar;

    for (int i = 0; i < 4; i++) {
        printf("%d ", *p);
        p++;
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `*p` joriy qiymatni o'qiydi, `p++` esa manzilni keyingi elementga suradi.

## Ishlash natijasi:
```text
5 10 15 20
```

---

# 355-Topshiriq: Massiv manzili (&arr) va birinchi element manzili (&arr[0]) ning nozik farqi

## Topshiriq sharti:
Ikkala ifodaning qiymati bir xil, lekin tiplari boshqa ekanligini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[5] = {1, 2, 3, 4, 5};

    printf("arr manzili:     %p\n", (void*)arr);
    printf("&arr[0] manzili: %p\n", (void*)&arr[0]);
    printf("&arr manzili:    %p\n", (void*)&arr);

    printf("arr + 1:         %p (siljish: %td bayt)\n", 
           (void*)(arr + 1), (char*)(arr + 1) - (char*)arr);
    printf("&arr + 1:        %p (siljish: %td bayt)\n", 
           (void*)(&arr + 1), (char*)(&arr + 1) - (char*)&arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `arr` turi: `int*` (1 elementga ko'rsatkich). Shuning uchun `arr + 1` 4 baytga suriladi.
2. `&arr` turi: `int (*)[5]` (butun 5 elementli massivga ko'rsatkich!).
3. Shuning uchun `&arr + 1` butun massiv hajmi bo'yicha (5 * 4 = 20 baytga) suriladi!

## Ishlash natijasi:
```text
arr manzili:     000000000012FFE0
&arr[0] manzili: 000000000012FFE0
&arr manzili:    000000000012FFE0
arr + 1:         000000000012FFE4 (siljish: 4 bayt)
&arr + 1:        000000000012FFF4 (siljish: 20 bayt)
```

---

# 356-Topshiriq: Massivga ko'rsatkich (Pointer to an Array: int (*ptr)[N])

## Topshiriq sharti:
Aniq o'lchamli butun massivni ko'rsatib turuvchi ko'rsatkichni e'lon qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int massiv[3] = {10, 20, 30};
    int (*ptr)[3] = &massiv; // 3 ta int dan iborat butun massivga pointer

    printf("Birinchi element (*ptr)[0]: %d\n", (*ptr)[0]);
    printf("Ikkinchi element (*ptr)[1]: %d\n", (*ptr)[1]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qavslar o'ta muhim: `int (*ptr)[3]` bu 3 ta int li massivga yagona ko'rsatkichdir.
2. Agar qavs qo'yilmasa (`int *ptr[3]`), bu ko'rsatkichlar massiviga aylanadi.

## Ishlash natijasi:
```text
Birinchi element (*ptr)[0]: 10
Ikkinchi element (*ptr)[1]: 20
```

---

# 357-Topshiriq: Ko'rsatkichlar massivi (Array of Pointers: int *arr[N])

## Topshiriq sharti:
Turli alohida o'zgaruvchilarning manzillarini bitta massivda saqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 100, b = 200, c = 300;
    int *ko_rsatkichlar[3] = {&a, &b, &c};

    for (int i = 0; i < 3; i++) {
        printf("Element %d: %d\n", i, *ko_rsatkichlar[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `ko_rsatkichlar[3]` massivining har bir elementi mustaqil xotira manzilini saqlaydi.

## Ishlash natijasi:
```text
Element 0: 100
Element 1: 200
Element 2: 300
```

---

# 358-Topshiriq: 2D massiv elementlariga pointer arifmetikasi orqali murojaat: *(*(matrix + i) + j)

## Topshiriq sharti:
2D matritsaning i-qator j-ustunidagi elementini ko'rsatkich orqali o'qing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int mat[2][3] = {
        {10, 20, 30},
        {40, 50, 60}
    };

    int i = 1, j = 2;
    // mat[i][j] ning pointer ekvivalenti:
    int qiymat = *(*(mat + i) + j);

    printf("mat[%d][%d] = %d\n", i, j, mat[i][j]);
    printf("*(*(mat + %d) + %d) = %d\n", i, j, qiymat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `mat + i` — i-chi qator boshiga ko'rsatkich.
2. `*(mat + i)` — i-chi qatorning birinchi elementi ko'rsatkichi (`&mat[i][0]`).
3. `*(mat + i) + j` — o'sha qatordagi j-chi element manzili.
4. `*(*(mat + i) + j)` — nihoyat qiymatning o'zini ochadi (60).

## Ishlash natijasi:
```text
mat[1][2] = 60
*(*(mat + 1) + 2) = 60
```

---

# 359-Topshiriq: 2D massivning i-qator manzilini olish: *(matrix + i) yoki matrix[i]

## Topshiriq sharti:
Har bir qatorning alohida 1D massiv sifatida ko'rilishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int mat[2][3] = {{1, 2, 3}, {4, 5, 6}};

    int *qator0 = mat[0];
    int *qator1 = mat[1];

    printf("0-qator birinchi: %d\n", *qator0);
    printf("1-qator birinchi: %d\n", *qator1);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da 2D massiv aslida massivlarning massividir.
2. `mat[0]` 0-qator boshiga ko'rsatkich (`int*`), `mat[1]` esa 1-qator boshiga ko'rsatkichdir.

## Ishlash natijasi:
```text
0-qator birinchi: 1
1-qator birinchi: 4
```

---

# 360-Topshiriq: Massivni funksiyaga ko'rsatkich sifatida uzatish va o'lcham

## Topshiriq sharti:
Funksiya parametrida massiv o'lchami yo'qolishini (decay) namoyish eting.

## Yechim (C kodi):
```c
#include <stdio.h>

void massiv_tekshir(int arr[]) {
    // Bu yerda arr oddiy int* ko'rsatkichga aylanadi!
    printf("Funksiya ichida sizeof(arr): %zu bayt (pointer hajmi!)\n", sizeof(arr));
}

int main(void) {
    int a[10];
    printf("main ichida sizeof(a):       %zu bayt (butun massiv!)\n", sizeof(a));
    massiv_tekshir(a);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `main` ichida `sizeof(a)` 10 * 4 = 40 bayt beradi.
2. Lekin funksiya ichida `sizeof(arr)` 8 bayt (64-bit ko'rsatkich o'lchami) beradi.
3. Shuning uchun massiv o'lchamini funksiyaga har doim alohida parametr sifatida berish shart!

## Ishlash natijasi:
```text
main ichida sizeof(a):       40 bayt (butun massiv!)
Funksiya ichida sizeof(arr): 8 bayt (pointer hajmi!)
```

---

# 361-Topshiriq: char arr[] (Stackda o'zgaruvchan) va char *s (Read-only segment) farqi

## Topshiriq sharti:
Satr massivi va satr ko'rsatkichining xotiradagi mutlaq farqi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char stack_satr[] = "Salom"; // Stackda alohida 6 bayt xotira ajratiladi
    const char *rodata_satr = "Salom"; // Read-Only Data segmentdagi manzilga ko'rsatadi

    stack_satr[0] = 'B'; // Qonuniy!
    printf("Stackdagi satr o'zgardi: %s\n", stack_satr);

    // rodata_satr[0] = 'B'; // TAQIQLANADI! Dastur qulaydi
    printf("Rodata satri o'zgarmas: %s\n", rodata_satr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `char arr[]` massiv bo'lib, uning elementlarini xohlagancha o'zgartirish mumkin.
2. `char *s = "..."` esa o'zgarmas doimiy xotiraga qaratilgan bo'ladi.

## Ishlash natijasi:
```text
Stackdagi satr o'zgardi: Balom
Rodata satri o'zgarmas: Salom
```

---

# 362-Topshiriq: Satrlar massivini (char *lugat[]) pointerlar orqali boshqarish

## Topshiriq sharti:
So'zlar ro'yxatini ko'rsatkichlar massivi orqali aylanib chiqing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    const char *mevalar[] = {"Olma", "Nok", "Uzum", "Shaftoli"};
    size_t soni = sizeof(mevalar) / sizeof(mevalar[0]);

    for (size_t i = 0; i < soni; i++) {
        printf("Meva %zu: %s\n", i + 1, mevalar[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir so'z xotiraning ixtiyoriy joyida saqlanishi mumkin, massiv esa faqat ularning ko'rsatkichlarini saqlaydi.

## Ishlash natijasi:
```text
Meva 1: Olma
Meva 2: Nok
Meva 3: Uzum
Meva 4: Shaftoli
```

---

# 363-Topshiriq: Ko'rsatkichlar massivini saralash: Matnlarni ko'chirmasdan saralash

## Topshiriq sharti:
Satrlarning o'zini joyidan jildirmasdan, faqat ularning pointerlarini almashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void pointer_sort(const char *arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (strcmp(arr[j], arr[j + 1]) > 0) {
                const char *temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int main(void) {
    const char *shaharlar[] = {"Toshkent", "Buxoro", "Andijon", "Samarqand"};
    pointer_sort(shaharlar, 4);

    printf("Saralangan shaharlar: ");
    for (int i = 0; i < 4; i++) printf("%s ", shaharlar[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta matnlar yoki obyektlarni nusxalash juda qimmatga tushadi.
2. Faqat 8 baytli ko'rsatkichlarni almashtirish saralashni juda tezkor qiladi.

## Ishlash natijasi:
```text
Saralangan shaharlar: Andijon Buxoro Samarqand Toshkent
```

---

# 364-Topshiriq: 2D massivni bir o'lchamli ko'rsatkich orqali to'liq aylanib chiqish

## Topshiriq sharti:
Row-major xossasidan foydalanib bitta sikl bilan barcha elementlarni chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int mat[2][3] = {
        {10, 20, 30},
        {40, 50, 60}
    };

    int *ptr = &mat[0][0];
    int jami = 2 * 3;

    printf("Chiziqli ko'rsatkich orqali: ");
    for (int i = 0; i < jami; i++) {
        printf("%d ", *(ptr + i));
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matritsa xotirada bo'linmas yagona blok bo'lgani uchun bitta `int*` orqali uning barcha kataklarini o'qish mumkin.

## Ishlash natijasi:
```text
Chiziqli ko'rsatkich orqali: 10 20 30 40 50 60
```

---

# 365-Topshiriq: Jagged array (Har xil o'lchamdagi qatorlar) ko'rsatkichlar massivida

## Topshiriq sharti:
Har bir qatori turli uzunlikda bo'lgan massiv tuzilmasini yarating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int qator1[] = {1, 2};
    int qator2[] = {10, 20, 30, 40};
    int qator3[] = {100};

    int *jagged[] = {qator1, qator2, qator3};
    int olchamlar[] = {2, 4, 1};

    for (int i = 0; i < 3; i++) {
        printf("%d-qator: ", i);
        for (int j = 0; j < olchamlar[i]; j++) {
            printf("%d ", jagged[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Jagged array kvadrat yoki to'g'ri to'rtburchak bo'lmagan, 'tishli' massivlarni hosil qilish imkonini beradi.

## Ishlash natijasi:
```text
0-qator: 1 2 
1-qator: 10 20 30 40 
2-qator: 100
```

---

# 366-Topshiriq: Pointer arifmetikasi bilan massivdagi qism-massiv ko'rsatkichini qaytarish

## Topshiriq sharti:
Massiv ichidan nishon qiymat topilganda uning manzilini qaytaruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

int* qism_massiv_top(int *arr, int len, int nishon) {
    for (int i = 0; i < len; i++) {
        if (arr[i] == nishon) return &arr[i]; // Qolgan qism boshlanishi
    }
    return NULL;
}

int main(void) {
    int sonlar[] = {1, 2, 3, 4, 5, 6};
    int *qism = qism_massiv_top(sonlar, 6, 4);

    if (qism != NULL) {
        printf("Topilgan joydan oxirigacha: ");
        while (qism < sonlar + 6) {
            printf("%d ", *qism++);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qaytgan ko'rsatkich o'sha elementdan boshlanuvchi qism-massiv (slice) sifatida ishlatiladi.

## Ishlash natijasi:
```text
Topilgan joydan oxirigacha: 4 5 6
```

---

# 367-Topshiriq: One-past-the-end pointer xususiyati va C standarti kafolatlari

## Topshiriq sharti:
Massiv oxiridan bitta keyingi manzilni ko'rsatkich bilan ishlatish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a[4] = {10, 20, 30, 40};
    int *oxir = a + 4; // Oxirgi elementdan keyingi manzil

    printf("Massiv boshlanishi: %p\n", (void*)a);
    printf("One-past-the-end:  %p\n", (void*)oxir);

    // C standarti bunday manzilni yaratish va taqqoslashni kafolatlaydi,
    // lekin uni dereference (*oxir) qilish TAQIQLANADI!
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C standarti har qanday massivning oxirgi elementidan keyingi bitta manzilni hisoblash va taqqoslashni rasman ruxsat beradi.
2. Bu STL iteratorlari (`end()`) ning poydevoridir.

## Ishlash natijasi:
```text
Massiv boshlanishi: 000000000012FFE0
One-past-the-end:  000000000012FFF0
```

---

# 368-Topshiriq: Massivni ko'rsatkichlar orqali ikkita teng bo'lakka bo'lish

## Topshiriq sharti:
Massivning chap va o'ng yarmini alohida ko'rsatkichlar bilan boshqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

void chop(const int *p, int len) {
    for (int i = 0; i < len; i++) printf("%d ", p[i]);
    printf("\n");
}

int main(void) {
    int arr[6] = {1, 2, 3, 4, 5, 6};
    int *chap = arr;
    int *ong = arr + 3;

    printf("Chap yarmi: "); chop(chap, 3);
    printf("O'ng yarmi: "); chop(ong, 3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `arr + 3` yangi massiv yaratmasdan, mavjud xotiraning ikkinchi qismiga bevosita ko'rsatkich beradi.

## Ishlash natijasi:
```text
Chap yarmi: 1 2 3 
O'ng yarmi: 4 5 6
```

---

# 369-Topshiriq: Massiv elementlarini ko'rsatkichlar orqali almashtirish (Pointer Swap)

## Topshiriq sharti:
Ikki massiv elementlarini ko'rsatkichlar yordamida o'zaro almashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

void massiv_almash(int *a, int *b, int n) {
    for (int i = 0; i < n; i++) {
        int temp = *(a + i);
        *(a + i) = *(b + i);
        *(b + i) = temp;
    }
}

int main(void) {
    int m1[3] = {1, 1, 1};
    int m2[3] = {9, 9, 9};

    massiv_almash(m1, m2, 3);
    printf("m1: %d %d %d, m2: %d %d %d\n", m1[0], m1[1], m1[2], m2[0], m2[1], m2[2]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkichlar orqali ikki massivning barcha elementlari o'zaro almashtiriladi.

## Ishlash natijasi:
```text
m1: 9 9 9, m2: 1 1 1
```

---

# 370-Topshiriq: Ko'rsatkichlar yordamida massivni filtrlab yangi buferga yozish

## Topshiriq sharti:
Faqat musbat sonlarni nishon buferiga ko'rsatkichlar bilan nusxalang.

## Yechim (C kodi):
```c
#include <stdio.h>

int filtrla_musbat(const int *src, int n, int *dest) {
    int *boshlangich = dest;
    for (int i = 0; i < n; i++) {
        if (*(src + i) > 0) {
            *dest++ = *(src + i);
        }
    }
    return dest - boshlangich; // Filtrlangan elementlar soni
}

int main(void) {
    int data[] = {-5, 12, 0, -3, 44, 7};
    int natija[6];
    int soni = filtrla_musbat(data, 6, natija);

    printf("Musbat sonlar (%d ta): ", soni);
    for (int i = 0; i < soni; i++) printf("%d ", natija[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `*dest++` qiymatni yozib, darhol keyingi bo'sh katakka o'tadi.

## Ishlash natijasi:
```text
Musbat sonlar (3 ta): 12 44 7
```

---

# 371-Topshiriq: 2D massiv ustunini pointer orqali o'qish (Stride / Step arifmetikasi)

## Topshiriq sharti:
Matritsaning faqat 1-ustunidagi elementlarni qadam tashlash orqali chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

#define COLS 3

int main(void) {
    int mat[3][COLS] = {
        {10, 20, 30},
        {40, 50, 60},
        {70, 80, 90}
    };

    // 1-ustun (20, 50, 80)
    int *p = &mat[0][1];
    printf("1-ustun elementlari: ");
    for (int r = 0; r < 3; r++) {
        printf("%d ", *p);
        p += COLS; // Stride = COLS ta element oldinga sakrash
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ustun bo'ylab pastga yurish uchun ko'rsatkichga har safar qatordagi ustunlar soni (`COLS`) qo'shiladi.

## Ishlash natijasi:
```text
1-ustun elementlari: 20 50 80
```

---

# 372-Topshiriq: Funksiyaga 2D massivni int** sifatida uzatish xatosi va sababi

## Topshiriq sharti:
Nima uchun int mat[3][3] ni int** qabul qiluvchi funksiyaga uzatib bo'lmasligini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

// XATOLIK: void xato(int **ptr);
// int mat[3][3]; xato(mat); // Warning: incompatible pointer type!

// Sababi: mat bu bitta yaxlit 9 ta int li blok.
// int** esa ko'rsatkichlar massiviga ko'rsatkich bo'lib, xotira tuzilishi mutlaqo boshqacha!

int main(void) {
    printf("int mat[3][3] bu int** EMAS! Uning haqiqiy turi: int (*)[3]\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'plab yangi boshlovchilar 2D massivni `int**` deb o'ylashadi, ammo bu jiddiy xatodir.
2. 2D massiv uchun to'g'ri ko'rsatkich turi `int (*)[COLS]` bo'ladi.

## Ishlash natijasi:
```text
int mat[3][3] bu int** EMAS! Uning haqiqiy turi: int (*)[3]
```

---

# 373-Topshiriq: To'g'ri usul: 2D massivni funksiyaga int (*arr)[COLS] bilan uzatish

## Topshiriq sharti:
Matritsani qator ko'rsatkichi bilan qabul qiluvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

#define USTUNLAR 3

void chop_2d(int (*arr)[USTUNLAR], int rows) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < USTUNLAR; j++) {
            printf("%d ", arr[i][j]);
        }
        printf("\n");
    }
}

int main(void) {
    int mat[2][USTUNLAR] = {{1, 2, 3}, {4, 5, 6}};
    chop_2d(mat, 2);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int (*arr)[USTUNLAR]` funksiyaga har bir qatori 3 ta elementli massivga ko'rsatkich uzatadi.

## Ishlash natijasi:
```text
1 2 3 
4 5 6
```

---

# 374-Topshiriq: Dinamik 2D massiv: Ko'rsatkichlar massivi orqali malloc

## Topshiriq sharti:
Qatorma-qator malloc chaqirib 2D massiv hosil qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int rows = 2, cols = 3;
    int **mat = (int**)malloc(rows * sizeof(int*));
    for (int i = 0; i < rows; i++) {
        mat[i] = (int*)malloc(cols * sizeof(int));
    }

    mat[0][0] = 5; mat[0][1] = 6; mat[0][2] = 7;
    mat[1][0] = 8; mat[1][1] = 9; mat[1][2] = 10;

    printf("Dinamik mat[1][2]: %d\n", mat[1][2]);

    for (int i = 0; i < rows; i++) free(mat[i]);
    free(mat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ushbu usulda yaratilgan massiv haqiqatan ham `int**` turida bo'ladi.

## Ishlash natijasi:
```text
Dinamik mat[1][2]: 10
```

---

# 375-Topshiriq: Dinamik 2D massiv: Bitta yaxlit uzluksiz blok (Single contiguous block)

## Topshiriq sharti:
Keshga qulay bitta malloc bilan 2D matritsa yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int r = 2, c = 3;
    // Bitta uzluksiz blok
    int *ma_lumot = (int*)malloc(r * c * sizeof(int));
    // Qatorlar ko'rsatkichlari massivi
    int **mat = (int**)malloc(r * sizeof(int*));
    for (int i = 0; i < r; i++) {
        mat[i] = ma_lumot + (i * c);
    }

    mat[0][1] = 99;
    printf("Contiguous mat[0][1]: %d\n", mat[0][1]);

    free(mat);
    free(ma_lumot);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Barcha ma'lumotlar xotirada ketma-ket yotadi, bu CPU keshida juda yuqori unumdorlik beradi.

## Ishlash natijasi:
```text
Contiguous mat[0][1]: 99
```

---

# 376-Topshiriq: Contiguous va Non-contiguous 2D massivlar solishtiruvi

## Topshiriq sharti:
Xotira yaxlitligi kesh tezligiga qanday ta'sir qilishini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("1. Contiguous (Yaxlit) massiv: barcha elementlar bitta RAM blokida yotadi (Kesh L1/L2 uchun a'lo).\n");
    printf("2. Non-contiguous massiv: har bir qator xotiraning turli burchagida joylashadi (Pointer chasing xarajati).\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yuqori unumdor tizimlarda har doim bitta yaxlit blokdan foydalanish talab etiladi.

## Ishlash natijasi:
```text
1. Contiguous (Yaxlit) massiv: barcha elementlar bitta RAM blokida yotadi (Kesh L1/L2 uchun a'lo).
2. Non-contiguous massiv: har bir qator xotiraning turli burchagida joylashadi (Pointer chasing xarajati).
```

---

# 377-Topshiriq: Ko'rsatkichlar bilan polindrom massivni tekshirish

## Topshiriq sharti:
Massiv boshidan va oxiridan ikkita ko'rsatkich bilan markazga qarab tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool massiv_palindrom(const int *bosh, const int *oxir) {
    while (bosh < oxir) {
        if (*bosh != *oxir) return false;
        bosh++;
        oxir--;
    }
    return true;
}

int main(void) {
    int arr[] = {10, 20, 30, 20, 10};
    bool res = massiv_palindrom(arr, arr + 4);
    printf("Massiv palindrommi: %s\n", res ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikki ko'rsatkichli algoritm eng kam amallar bilan palindromlikni aniqlaydi.

## Ishlash natijasi:
```text
Massiv palindrommi: Ha
```

---

# 378-Topshiriq: Satr ichidan qidirilgan belgining indeksini pointer ayirmasi bilan topish

## Topshiriq sharti:
strchr analogini yozib, qidirilgan harf indeksini chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    const char *satr = "Dasturlash";
    const char *p = satr;
    char nishon = 'u';

    while (*p != '\0' && *p != nishon) {
        p++;
    }

    if (*p == nishon) {
        printf("'%c' harfi %td-indeksda topildi.\n", nishon, p - satr);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `p - satr` ko'rsatkichlar ayirmasi belgining 0 dan boshlangan indeksini beradi.

## Ishlash natijasi:
```text
'u' harfi 4-indeksda topildi.
```

---

# 379-Topshiriq: Massiv o'rtasidagi elementga to'g'ridan-to'g'ri ko'rsatkich o'rnatish

## Topshiriq sharti:
int *mid = arr + n/2 ko'rsatkichini o'rnatib, uning atrofidagi qiymatlarni o'qing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[] = {10, 20, 30, 40, 50};
    int *mid = arr + 2; // 30 elementiga ko'rsatadi

    printf("Markaz: %d\n", *mid);
    printf("Markazdan 1 ta oldin: %d\n", *(mid - 1));
    printf("Markazdan 1 ta keyin: %d\n", *(mid + 1));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Markaziy ko'rsatkichdan ikkala tomonga ham erkin harakatlanish mumkin.

## Ishlash natijasi:
```text
Markaz: 30
Markazdan 1 ta oldin: 20
Markazdan 1 ta keyin: 40
```

---

# 380-Topshiriq: Manfiy indekslash: mid[-1] va mid[1] sintaksisi va pointerlar mantiqi

## Topshiriq sharti:
C tilida manfiy indeksning qanday qilib to'liq ishlashini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int sonlar[] = {100, 200, 300, 400, 500};
    int *p = &sonlar[2]; // 300 ga ko'rsatadi

    // p[-1] == *(p - 1) == 200
    // p[0]  == *(p + 0) == 300
    // p[1]  == *(p + 1) == 400
    printf("p[-1] = %d\n", p[-1]);
    printf("p[0]  = %d\n", p[0]);
    printf("p[1]  = %d\n", p[1]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `p[-1]` qoidaga ko'ra `*(p + (-1))` bo'ladi.
2. Agar ko'rsatkich massiv o'rtasiga qaratilgan bo'lsa, manfiy indeks orqaga qarab elementlarni xatosiz o'qiydi!

## Ishlash natijasi:
```text
p[-1] = 200
p[0]  = 300
p[1]  = 400
```

---

# 381-Topshiriq: char* ko'rsatkichi bilan satrdagi bo'shliqlarni olib tashlash (In-place trim)

## Topshiriq sharti:
O'qish va yozish ko'rsatkichlari bilan probellarni yo'qoting.

## Yechim (C kodi):
```c
#include <stdio.h>

void boshliqlarni_ochir(char *s) {
    char *oqish = s;
    char *yozish = s;
    while (*oqish != '\0') {
        if (*oqish != ' ') {
            *yozish++ = *oqish;
        }
        oqish++;
    }
    *yozish = '\0'; // Yangi satr oxiri
}

int main(void) {
    char matn[] = "C   dasturlash   tili";
    boshliqlarni_ochir(matn);
    printf("Natija: '%s'\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikki ko'rsatkichli usul (oqish va yozish) bitta satr ichida xotira ajratmasdan bo'shliqlarni siqib chiqaradi.

## Ishlash natijasi:
```text
Natija: 'Cdasturlashtili'
```

---

# 382-Topshiriq: Ko'rsatkichlar yordamida saralangan ikki massiv kesishmasini (Intersection) topish

## Topshiriq sharti:
Ikkala massivda ham qatnashgan umumiy elementlarni toping.

## Yechim (C kodi):
```c
#include <stdio.h>

void kesishma(const int *a, int na, const int *b, int nb) {
    const int *pa = a;
    const int *pb = b;
    printf("Umumiy elementlar: ");
    while (pa < a + na && pb < b + nb) {
        if (*pa == *pb) {
            printf("%d ", *pa);
            pa++; pb++;
        } else if (*pa < *pb) {
            pa++;
        } else {
            pb++;
        }
    }
    printf("\n");
}

int main(void) {
    int a[] = {1, 2, 4, 5, 6};
    int b[] = {2, 3, 5, 7};
    kesishma(a, 5, b, 4);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikkita ko'rsatkich kichik qiymat tomon siljib boradi va umumiy sonlarni chop etadi.

## Ishlash natijasi:
```text
Umumiy elementlar: 2 5
```

---

# 383-Topshiriq: Pointerlar orqali 1D konvolyutsiya (1D Convolution / Silliqlash)

## Topshiriq sharti:
3 ta elementli o'rtacha filtri bilan massivni tekislang.

## Yechim (C kodi):
```c
#include <stdio.h>

void silliqla(const int *src, int n, double *dest) {
    for (int i = 1; i < n - 1; i++) {
        dest[i] = (*(src + i - 1) + *(src + i) + *(src + i + 1)) / 3.0;
    }
}

int main(void) {
    int signal[] = {10, 50, 10, 50, 10};
    double tozalangan[5] = {0};

    silliqla(signal, 5, tozalangan);
    printf("Silliqlangan signal: %.1lf %.1lf %.1lf\n", 
           tozalangan[1], tozalangan[2], tozalangan[3]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Raqamli signallarni qayta ishlash (DSP) va neyron tarmoqlar (CNN) aynan mana shu konvolyutsiya amali asosida ishlaydi.

## Ishlash natijasi:
```text
Silliqlangan signal: 23.3 23.3 23.3
```

---

# 384-Topshiriq: Ko'rsatkichlar bilan prefiks yig'indilari (Prefix Sums) massivini shakllantirish

## Topshiriq sharti:
Har bir katak o'zigacha bo'lgan barcha sonlar yig'indisini saqlasin.

## Yechim (C kodi):
```c
#include <stdio.h>

void prefiks_yigindi(const int *src, int *dest, int n) {
    *dest = *src;
    for (int i = 1; i < n; i++) {
        *(dest + i) = *(dest + i - 1) + *(src + i);
    }
}

int main(void) {
    int a[] = {2, 4, 6, 8};
    int p[4];

    prefiks_yigindi(a, p, 4);
    printf("Prefiks massiv: %d %d %d %d\n", p[0], p[1], p[2], p[3]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Prefiks massiv orqali ixtiyoriy [L, R] oraliq yig'indisi O(1) vaqtda topiladi.

## Ishlash natijasi:
```text
Prefiks massiv: 2 6 12 20
```

---

# 385-Topshiriq: Ko'rsatkichlar orqali massivdagi juft va toq elementlarni ajratish (Partition)

## Topshiriq sharti:
Juft sonlarni chapga, toq sonlarni o'ngga suruvchi ko'rsatkichli algoritm.

## Yechim (C kodi):
```c
#include <stdio.h>

void ajrat_juft_toq(int *chap, int *ong) {
    while (chap < ong) {
        while (chap < ong && (*chap % 2 == 0)) chap++;
        while (chap < ong && (*ong % 2 != 0)) ong--;
        if (chap < ong) {
            int t = *chap; *chap = *ong; *ong = t;
            chap++; ong--;
        }
    }
}

int main(void) {
    int arr[] = {1, 2, 3, 4, 5, 6};
    ajrat_juft_toq(arr, arr + 5);

    printf("Ajratilgach: ");
    for (int i = 0; i < 6; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Quicksort algoritmining asosiy bo'lish (Lomuto/Hoare partition) mexanizmi.

## Ishlash natijasi:
```text
Ajratilgach: 6 2 4 3 5 1
```

---

# 386-Topshiriq: Massivni aylanib chiqishda kesh samaradorligi: Qatorlar bo'yicha vs Ustunlar bo'yicha

## Topshiriq sharti:
Row-major tartibning xotira keshiga qanchalik mos kelishini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

#define N 3

int main(void) {
    int mat[N][N] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int sum = 0;

    // TEZKOR USUL (Keshga mos - Cache Friendly):
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            sum += mat[i][j];
        }
    }

    printf("Row-major yig'indi: %d\n", sum);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. CPU bir vaqtning o'zida butun kesh liniyasini (64 bayt) keshga yuklaydi.
2. Qatorma-qator yurilganda qo'shni elementlar allaqachon keshda tayyor turadi (Cache Hit).
3. Ustun bo'yicha sakrab yurilsa har safar kesh yangilanadi (Cache Miss) va tezlik 10 barobargacha tushib ketishi mumkin.

## Ishlash natijasi:
```text
Row-major yig'indi: 45
```

---

# 387-Topshiriq: Pointer Decay hodisasi nima va u qachon sodir bo'lmaydi?

## Topshiriq sharti:
Massiv nomi ko'rsatkichga aylanmaydigan ikkita holatni ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[10];

    // 1-holat: sizeof(arr) da massiv pointerga aylanmaydi, butun massiv hajmini beradi:
    printf("1. sizeof(arr): %zu bayt\n", sizeof(arr));

    // 2-holat: &arr da butun massivning manzili olinadi (int (*)[10]):
    printf("2. sizeof(&arr): %zu bayt\n", sizeof(&arr));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sizeof` va `&` operatorlari qo'llanilganda massiv nomi pointerga aylanmaydi (Decay bo'lmaydi).
2. Qolgan deyarli barcha holatlarda (funksiyaga uzatilganda, arifmetik amallarda) massiv ko'rsatkichga aylanadi.

## Ishlash natijasi:
```text
1. sizeof(arr): 40 bayt
2. sizeof(&arr): 8 bayt
```

---

# 388-Topshiriq: Ko'rsatkichlar yordamida massivni qadam tashlab (Step / Stride) o'qish

## Topshiriq sharti:
Massiv elementlarini har 2 qadamda bitta o'qib chiquvchi ko'rsatkich sikli.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a[] = {10, 20, 30, 40, 50, 60};
    int *p = a;
    int *oxir = a + 6;

    printf("Har 2 qadamdagi elementlar: ");
    while (p < oxir) {
        printf("%d ", *p);
        p += 2; // Stride = 2
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Stride arifmetikasi ilmiy hisob-kitoblar va neyron tarmoqlar tenzorlarida qadam tashlash (strided memory) uchun asosdir.

## Ishlash natijasi:
```text
Har 2 qadamdagi elementlar: 10 30 50
```

---

# 389-Topshiriq: Ko'rsatkichlar bilan massivni polindrom qilish (In-place)

## Topshiriq sharti:
Massivning ikkinchi yarmini birinchi yarmiga qarab nosimmetriklikdan tozalang.

## Yechim (C kodi):
```c
#include <stdio.h>

void nosimmetrikni_tuzat(int *bosh, int *oxir) {
    while (bosh < oxir) {
        *oxir = *bosh; // Chap tomondagi qiymatni o'ng tomonga ko'chirish
        bosh++;
        oxir--;
    }
}

int main(void) {
    int a[4] = {10, 20, 99, 99};
    nosimmetrikni_tuzat(a, a + 3);

    printf("Simmetrik qilindi: %d %d %d %d\n", a[0], a[1], a[2], a[3]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkichlar o'zaro yaqinlashib, massivni to'liq simmetrik (palindrom) holatga keltiradi.

## Ishlash natijasi:
```text
Simmetrik qilindi: 10 20 20 10
```

---

# 390-Topshiriq: String literalidagi belgilarni pointer yordamida sanash

## Topshiriq sharti:
Matn ichidagi harflar sonini ko'rsatkich bilan sanang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    const char *matn = "Assalomu Alaykum";
    const char *p = matn;
    int hisob = 0;

    while (*p != '\0') {
        hisob++;
        p++;
    }

    printf("'%s' matnida %d ta belgi bor.\n", matn, hisob);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `*p != '\0'` sharti satrning oxirgi nol baytiga yetguncha ko'rsatkichni siljitadi.

## Ishlash natijasi:
```text
'Assalomu Alaykum' matnida 16 ta belgi bor.
```

---

# 391-Topshiriq: Massiv elementlarini pointer orqali 0 ga tozalash

## Topshiriq sharti:
while sikli va ko'rsatkich bilan massivni tezkor tozalash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[4] = {5, 6, 7, 8};
    int *p = arr;
    int *oxir = arr + 4;

    while (p < oxir) {
        *p++ = 0;
    }

    printf("Tozalangach: %d %d %d %d\n", arr[0], arr[1], arr[2], arr[3]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `*p++ = 0;` bitta qisqa buyruq bilan qiymatni 0 qiladi va keyingisiga o'tadi.

## Ishlash natijasi:
```text
Tozalangach: 0 0 0 0
```

---

# 392-Topshiriq: Ko'rsatkich yordamida massivning eng uzun o'suvchi qism ketma-ketligini topish

## Topshiriq sharti:
Yonma-yon o'suvchi sonlar blokini pointerlar bilan aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[] = {1, 2, 3, 1, 2, 3, 4, 5, 2};
    int n = 9;
    int max_len = 1, cur_len = 1;

    for (int *p = arr + 1; p < arr + n; p++) {
        if (*p > *(p - 1)) {
            cur_len++;
            if (cur_len > max_len) max_len = cur_len;
        } else {
            cur_len = 1;
        }
    }

    printf("Eng uzun o'suvchi oraliq uzunligi: %d\n", max_len);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. [1, 2, 3, 4, 5] oralig'i ketma-ket o'suvchi bo'lib, uzunligi 5 ga teng.

## Ishlash natijasi:
```text
Eng uzun o'suvchi oraliq uzunligi: 5
```

---

# 393-Topshiriq: Ko'rsatkichlar massivi orqali matnlarni alifbo tartibida saralash

## Topshiriq sharti:
Satrlar massivini qsort() ga o'xshash almashtirish bilan saralang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *dasturlar[] = {"Python", "C", "Rust", "Go"};
    int n = 4;

    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (strcmp(dasturlar[j], dasturlar[j + 1]) > 0) {
                const char *tmp = dasturlar[j];
                dasturlar[j] = dasturlar[j + 1];
                dasturlar[j + 1] = tmp;
            }
        }
    }

    printf("Saralangan: %s, %s, %s, %s\n", 
           dasturlar[0], dasturlar[1], dasturlar[2], dasturlar[3]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkichlar massivi matnlarning o'rnini almashtirishni juda yengil qiladi.

## Ishlash natijasi:
```text
Saralangan: C, Go, Python, Rust
```

---

# 394-Topshiriq: Pointerlar bilan massivdagi ikki element yig'indisini topish (Two Sum)

## Topshiriq sharti:
Saralangan massivda yig'indisi target bo'lgan juftlikni O(N) da toping.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool two_sum(const int *chap, const int *ong, int target, int *r1, int *r2) {
    while (chap < ong) {
        int sum = *chap + *ong;
        if (sum == target) {
            *r1 = *chap;
            *r2 = *ong;
            return true;
        }
        if (sum < target) chap++;
        else ong--;
    }
    return false;
}

int main(void) {
    int arr[] = {2, 7, 11, 15};
    int r1, r2;
    if (two_sum(arr, arr + 3, 9, &r1, &r2)) {
        printf("Topildi: %d + %d = 9\n", r1, r2);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Saralangan massivda ikki ko'rsatkich orqali O(N) da qidirish amalga oshiriladi.

## Ishlash natijasi:
```text
Topildi: 2 + 7 = 9
```

---

# 395-Topshiriq: Ko'rsatkichlar yordamida massivni nollardan tozalash (Move Zeroes)

## Topshiriq sharti:
Barcha nollarni massiv oxiriga surib, qolgan tartibni saqlab qoling.

## Yechim (C kodi):
```c
#include <stdio.h>

void nollarni_oxiriga_sur(int *arr, int n) {
    int *nol_emas = arr;
    for (int *p = arr; p < arr + n; p++) {
        if (*p != 0) {
            int t = *nol_emas;
            *nol_emas = *p;
            *p = t;
            nol_emas++;
        }
    }
}

int main(void) {
    int arr[] = {0, 1, 0, 3, 12};
    nollarni_oxiriga_sur(arr, 5);

    printf("Natija: ");
    for (int i = 0; i < 5; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `nol_emas` ko'rsatkichi noldan farqli elementlar qo'yilishi kerak bo'lgan navbatdagi katakni belgilaydi.

## Ishlash natijasi:
```text
Natija: 1 3 12 0 0
```

---

# 396-Topshiriq: Pointerlar bilan massivdagi eng ko'p takrorlangan elementni topish

## Topshiriq sharti:
Saralangan massivda pointerlar bilan eng uzun takrorlanishni toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int eng_kop_takrorlangan(const int *arr, int n) {
    int max_count = 1, cur_count = 1;
    int dominant = *arr;

    for (const int *p = arr + 1; p < arr + n; p++) {
        if (*p == *(p - 1)) {
            cur_count++;
            if (cur_count > max_count) {
                max_count = cur_count;
                dominant = *p;
            }
        } else {
            cur_count = 1;
        }
    }
    return dominant;
}

int main(void) {
    int arr[] = {1, 2, 2, 2, 3, 4, 4};
    printf("Eng ko'p takrorlangan: %d\n", eng_kop_takrorlangan(arr, 7));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 2 soni ketma-ket 3 marta takrorlangan.

## Ishlash natijasi:
```text
Eng ko'p takrorlangan: 2
```

---

# 397-Topshiriq: Pointerlar yordamida massivning medianasini topish

## Topshiriq sharti:
Saralangan massivda o'rtadagi elementni aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

double mediana_top(const int *arr, int n) {
    const int *mid = arr + n / 2;
    if (n % 2 != 0) {
        return *mid;
    }
    return (*(mid - 1) + *mid) / 2.0;
}

int main(void) {
    int toq_massiv[] = {1, 3, 5, 7, 9};
    int juft_massiv[] = {1, 2, 3, 4};

    printf("Toq massiv medianasi: %.1lf\n", mediana_top(toq_massiv, 5));
    printf("Juft massiv medianasi: %.1lf\n", mediana_top(juft_massiv, 4));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'rtadagi manzilga ko'rsatkich qo'yilib, mediana darhol O(1) da hisoblanadi.

## Ishlash natijasi:
```text
Toq massiv medianasi: 5.0
Juft massiv medianasi: 2.5
```

---

# 398-Topshiriq: Massiv nomi va pointerning sizeof bilan o'zaro taqqoslanishi

## Topshiriq sharti:
sizeof(arr) vs sizeof(ptr) ning barcha jihatlarini umumlashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int arr[8] = {0};
    int *ptr = arr;

    printf("arr hajmi (massiv):     %zu bayt\n", sizeof(arr));
    printf("ptr hajmi (ko'rsatkich): %zu bayt\n", sizeof(ptr));
    printf("Elementlar soni:        %zu ta\n", sizeof(arr) / sizeof(arr[0]));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `arr` butun massivni (8 * 4 = 32 bayt) ifodalaydi.
2. `ptr` esa shunchaki xotira manzilini (8 bayt) saqlaydi.

## Ishlash natijasi:
```text
arr hajmi (massiv):     32 bayt
ptr hajmi (ko'rsatkich): 8 bayt
Elementlar soni:        8 ta
```

---

# 399-Topshiriq: Ko'rsatkichlar yordamida satrni joyida teskari qilish (In-place String Reversal)

## Topshiriq sharti:
Bosh va oxirgi ko'rsatkichlar bilan so'zni teskarisiga o'giring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void satr_teskari(char *s) {
    char *bosh = s;
    char *oxir = s + strlen(s) - 1;
    while (bosh < oxir) {
        char t = *bosh; *bosh = *oxir; *oxir = t;
        bosh++; oxir--;
    }
}

int main(void) {
    char matn[] = "TOSHKENT";
    satr_teskari(matn);
    printf("Teskari: %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qo'shimcha massivsiz satrning o'zida harflar o'rni almashtiriladi.

## Ishlash natijasi:
```text
Teskari: TNEKHSOT
```

---

# 400-Topshiriq: Modul yakuni: Ko'rsatkichlar va massivlar asosida yuqori tezlikdagi String Tokenizer

## Topshiriq sharti:
Satrni ajratuvchi bo'yicha tokenlarga bo'luvchi xavfsiz strtok analogi.

## Yechim (C kodi):
```c
#include <stdio.h>

char* mening_strtok(char *str, char ajratuvchi) {
    static char *keyingi = NULL;
    if (str != NULL) {
        keyingi = str;
    }
    if (keyingi == NULL || *keyingi == '\0') {
        return NULL;
    }

    char *boshlanish = keyingi;
    while (*keyingi != '\0') {
        if (*keyingi == ajratuvchi) {
            *keyingi = '\0'; // Satrni tugatish
            keyingi++;       // Keyingi token boshiga o'tish
            return boshlanish;
        }
        keyingi++;
    }
    return boshlanish;
}

int main(void) {
    char matn[] = "Olma,Anor,Uzum,Anjir";
    printf("Tokenlar:\n");
    char *token = mening_strtok(matn, ',');
    while (token != NULL) {
        printf("-> %s\n", token);
        token = mening_strtok(NULL, ',');
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `static char *keyingi` ko'rsatkichi satr ichidagi joriy holatni saqlab qoladi.
2. Ajratuvchi belgi o'rniga ` ` qo'yilib, bitta satr bir nechta qism-satrlarga bo'linadi.
3. Bu 8-qismning barcha ko'rsatkich, massiv va satr o'zaro bog'lanishlarini to'liq mujassamlashtiradi.

## Ishlash natijasi:
```text
Tokenlar:
-> Olma
-> Anor
-> Uzum
-> Anjir
```

---
