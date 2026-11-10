# C Dasturlash Tili — 10-Qism: Dinamik Xotira (malloc, calloc, realloc, free)
## (451-500 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* Stack va Heap xotira modellari farqi va malloc() / free() asoslari
* calloc() bilan nol initsializatsiyasi va realloc() bilan xavfsiz kengaytirish
* Memory Leak, Dangling pointer va Double Free profilaktikasi
* Dinamik 1D va 2D massivlar, Flexible Array Member (C99)
* Arena Allocator, Free List, aligned_alloc (C11) va to'liq Dinamik Vektor kutubxonasi

---

# 451-Topshiriq: Dinamik xotira (Heap) tushunchasi va Stack bilan solishtirish

## Topshiriq sharti:
Heap xotirasining dasturchi nazoratida ekanligini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int stack_son = 10; // Stekda (avtomatik boshqariladi)
    int *heap_son = (int*)malloc(sizeof(int)); // Heapda (qo'lda boshqariladi)

    if (heap_son != NULL) {
        *heap_son = 20;
        printf("Stack o'zgaruvchisi: %d (Manzili: %p)\n", stack_son, (void*)&stack_son);
        printf("Heap o'zgaruvchisi:  %d (Manzili: %p)\n", *heap_son, (void*)heap_son);
        free(heap_son); // Qo'lda ozod qilish shart!
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Stek xotira o'lchami cheklangan (1-8 MB) va funksiya tugashi bilan o'chiriladi.
2. Heap xotira butun RAM bilan cheklanadi va dasturchi `free()` chaqirmaguncha saqlanib turadi.
3. Heap manzillari va Stack manzillari operativ xotiraning mutlaqo turli hududlarida joylashadi.

## Ishlash natijasi:
```text
Stack o'zgaruvchisi: 10 (Manzili: 000000000012FFE4)
Heap o'zgaruvchisi:  20 (Manzili: 0000000000551010)
```

---

# 452-Topshiriq: malloc() asoslari va free() bilan xotirani tozalash

## Topshiriq sharti:
malloc yordamida bitta butun son uchun joy ajrating va tozalang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *p = (int*)malloc(sizeof(int));

    if (p == NULL) {
        printf("Xotira ajratishda xatolik!\n");
        return 1;
    }

    *p = 777;
    printf("Ajratilgan qiymat: %d\n", *p);

    free(p); // Xotirani operatsion tizimga qaytarish
    p = NULL;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `malloc(hajm)` so'ralgan baytlar soniga teng xotira blokini Heapdan ajratadi va `void*` qaytaradi.
2. Har bir `malloc` uchun bitta `free` bo'lishi shart.

## Ishlash natijasi:
```text
Ajratilgan qiymat: 777
```

---

# 453-Topshiriq: malloc() qaytargan ko'rsatkichni NULL ga qat'iy tekshirish

## Topshiriq sharti:
Xotira tugab qolganda dastur qulamasligi uchun NULL tekshiruvini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    size_t ulkan_hajm = 1000 * sizeof(int);
    int *massiv = (int*)malloc(ulkan_hajm);

    if (massiv == NULL) {
        fprintf(stderr, "XATOLIK: Operativ xotira yetarli emas!\n");
        return EXIT_FAILURE;
    }

    printf("1000 ta int uchun xotira muvaffaqiyatli ajratildi.\n");
    free(massiv);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar tizimda bo'sh RAM qolmagan bo'lsa, `malloc` `NULL` qaytaradi.
2. `NULL` ni tekshirmasdan unga yozish dasturning Segmentation fault bilan qulashiga sabab bo'ladi.

## Ishlash natijasi:
```text
1000 ta int uchun xotira muvaffaqiyatli ajratildi.
```

---

# 454-Topshiriq: calloc() asoslari: Xotirani ajratish va uni avtomatik 0 bilan tozalash

## Topshiriq sharti:
calloc orqali 5 ta element ajratib, ularning 0 ga tengligini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *arr = (int*)calloc(5, sizeof(int));
    if (arr == NULL) return 1;

    printf("calloc bilan ajratilgan elementlar: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    free(arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `calloc(soni, olcham)` ikkita parametr oladi: elementlar soni va har birining hajmi.
2. U xotirani ajratib, uning barcha baytlarini avtomatik 0 (nol) bilan tozalaydi.

## Ishlash natijasi:
```text
calloc bilan ajratilgan elementlar: 0 0 0 0 0
```

---

# 455-Topshiriq: malloc() vs calloc() xatti-harakat va unumdorlik farqi

## Topshiriq sharti:
malloc nollar bermasligini (axlat qiymatlar saqlanishi) va calloc tozalashini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    printf("1. malloc() tezroq ishlaydi, ammo xotirani tozalamaydi (Garbage data qoladi).\n");
    printf("2. calloc() sekinroq, chunki u butun blokni 0 bilan to'ldirib chiqadi.\n");
    printf("Qoida: agar massiv darhol yangi qiymatlar bilan to'ldirilsa malloc, aks holda calloc ishlatiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `malloc` faqat manzilni beradi, `calloc` esa qo'shimcha ravishda xotirani nolga tenglashtirish (zero-initialization) amalini bajaradi.

## Ishlash natijasi:
```text
1. malloc() tezroq ishlaydi, ammo xotirani tozalamaydi (Garbage data qoladi).
2. calloc() sekinroq, chunki u butun blokni 0 bilan to'ldirib chiqadi.
Qoida: agar massiv darhol yangi qiymatlar bilan to'ldirilsa malloc, aks holda calloc ishlatiladi.
```

---

# 456-Topshiriq: realloc() asoslari: Massiv hajmini kattalashtirish

## Topshiriq sharti:
3 ta elementli massivni 5 taga kattalashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *arr = (int*)malloc(3 * sizeof(int));
    if (!arr) return 1;

    arr[0] = 10; arr[1] = 20; arr[2] = 30;

    // Hajmni 5 tagacha oshirish
    int *temp = (int*)realloc(arr, 5 * sizeof(int));
    if (temp != NULL) {
        arr = temp;
        arr[3] = 40;
        arr[4] = 50;
    }

    printf("Kengaytirilgan massiv: ");
    for (int i = 0; i < 5; i++) printf("%d ", arr[i]);
    printf("\n");

    free(arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `realloc(ptr, yangi_hajm)` mavjud xotirani joyida kengaytiradi yoki yangi kattaroq joyga ko'chirib, eskisini avtomatik ozod qiladi.

## Ishlash natijasi:
```text
Kengaytirilgan massiv: 10 20 30 40 50
```

---

# 457-Topshiriq: realloc() da xavfsizlik: Nima uchun arr = realloc(arr, ...) xavfli?

## Topshiriq sharti:
realloc muvaffaqiyatsiz bo'lganda asl xotira yo'qolib ketishining oldini olish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *arr = (int*)malloc(10 * sizeof(int));
    if (!arr) return 1;

    // XAVFLI: arr = realloc(arr, yangi_hajm);
    // Agar realloc NULL qaytarsa, arr NULL bo'lib qoladi va eski xotira unutilib (Leak) ketadi!

    // TO'G'RI VA XAVFSIZ:
    int *vaqtinchalik = (int*)realloc(arr, 20 * sizeof(int));
    if (vaqtinchalik != NULL) {
        arr = vaqtinchalik;
        printf("Xotira muvaffaqiyatli kengaytirildi.\n");
    } else {
        printf("Kengaytirib bo'lmadi, ammo eski xotira saqlanib qoldi.\n");
    }

    free(arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Doimo oraliq ko'rsatkichdan foydalanish talab etiladi, aks holda xotira oqishi (Memory leak) kafolatlanadi.

## Ishlash natijasi:
```text
Xotira muvaffaqiyatli kengaytirildi.
```

---

# 458-Topshiriq: realloc() orqali xotira hajmini kichraytirish (Shrinking)

## Topshiriq sharti:
Ortiqcha bo'sh joyni operatsion tizimga qaytarish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *arr = (int*)malloc(10 * sizeof(int));
    for (int i = 0; i < 10; i++) arr[i] = i * 2;

    // Faqat 3 ta element kerak, qolgan 7 tasini qirqib tashlaymiz
    int *kichraytirilgan = (int*)realloc(arr, 3 * sizeof(int));
    if (kichraytirilgan != NULL) {
        arr = kichraytirilgan;
    }

    printf("Qisqargan massiv: %d %d %d\n", arr[0], arr[1], arr[2]);
    free(arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `realloc` xotirani qisqartirish uchun ham ishlatiladi; keraksiz qoldiq RAM tizimga qaytariladi.

## Ishlash natijasi:
```text
Qisqargan massiv: 0 2 4
```

---

# 459-Topshiriq: Xotira oqishi (Memory Leak) nima va uning oqibatlari

## Topshiriq sharti:
free() chaqirilmagan xotira dastur tugaguncha band qolib ketishini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

void xotira_oqishi_namunasi(void) {
    int *oqish = (int*)malloc(100 * sizeof(int));
    // free(oqish) qilinmadi! Funksiya tugashi bilan oqish ko'rsatkichi yo'qoladi,
    // ammo 400 bayt Heapda abadiy band bo'lib qoladi!
    (void)oqish;
}

int main(void) {
    printf("Memory Leak — ajratilgan xotirani ozod qilish unutilganda sodir bo'ladi.\n");
    printf("Uzoq ishlaydigan serverlarda bu butun RAM ning to'lib ketishiga olib keladi!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xotira oqishi dasturning vaqt o'tishi bilan tobora ko'p RAM yeb qo'yishiga va oxir-oqibat tizimning qotib qolishiga olib keladi.

## Ishlash natijasi:
```text
Memory Leak — ajratilgan xotirani ozod qilish unutilganda sodir bo'ladi.
Uzoq ishlaydigan serverlarda bu butun RAM ning to'lib ketishiga olib keladi!
```

---

# 460-Topshiriq: Use-After-Free (Ozod qilingan xotirani o'qish/yozish) zaifligi

## Topshiriq sharti:
Nima uchun free qilingan pointerni qayta ishlatish jiddiy xato ekanligini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *p = (int*)malloc(sizeof(int));
    *p = 50;
    free(p);

    // XAVFLI USE-AFTER-FREE:
    // printf("%d\n", *p); // UB! Bu manzil boshqa kodga berilgan bo'lishi mumkin!
    
    p = NULL; // Darhol NULL qilish Use-After-Free dan asraydi
    printf("p xavfsiz NULL qilindi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Use-After-Free — dunyodagi eng mashhur kritik xavfsizlik zaifliklaridan biridir (xakerlar bu orqali masofadan kod ishga tushirishadi).
2. Xotira ozod etilishi bilan uning ko'rsatkichi `NULL` qilinishi shart!

## Ishlash natijasi:
```text
p xavfsiz NULL qilindi.
```

---

# 461-Topshiriq: Double Free (Bitta manzilni ikki marta free qilish) halokati

## Topshiriq sharti:
Ikki marta free chaqirish qanday xatolik keltirib chiqarishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *p = (int*)malloc(sizeof(int));
    free(p);
    
    // free(p); // HALOKAT: double free or corruption!
    // Lekin NULL ko'rsatkichni free qilish xavfsiz (standart bo'yicha hech narsa qilmaydi):
    p = NULL;
    free(p); // Qonuniy va hech qanday xato bermaydi!

    printf("NULL pointerni free qilish mutlaqo xavfsiz!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C standarti bo'yicha `free(NULL)` mutlaqo xavfsiz va hech qanday yomon oqibat keltirmaydi.
2. Shuning uchun pointerni `free()` dan keyin `NULL` qilish Double Free xatosini ham bartaraf etadi.

## Ishlash natijasi:
```text
NULL pointerni free qilish mutlaqo xavfsiz!
```

---

# 462-Topshiriq: Dinamik 1D massiv yaratish va to'ldirish

## Topshiriq sharti:
O'lchami ish vaqtida kiritiladigan dinamik massiv yarating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n = 5; // Simulyatsiya qilingan hajm
    int *arr = (int*)malloc(n * sizeof(int));
    if (!arr) return 1;

    for (int i = 0; i < n; i++) {
        arr[i] = (i + 1) * 10;
    }

    printf("Dinamik massiv: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    free(arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Massiv o'lchami faqat ish vaqtida ma'lum bo'lganda dinamik massiv yagona to'g'ri yechimdir.

## Ishlash natijasi:
```text
Dinamik massiv: 10 20 30 40 50
```

---

# 463-Topshiriq: Dinamik massiv elementlari yig'indisi va o'rtachasini hisoblash

## Topshiriq sharti:
Dinamik massiv ma'lumotlarini tahlil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n = 4;
    double *qiymatlar = (double*)malloc(n * sizeof(double));
    if (!qiymatlar) return 1;

    qiymatlar[0] = 12.5; qiymatlar[1] = 20.0;
    qiymatlar[2] = 17.5; qiymatlar[3] = 30.0;

    double jami = 0;
    for (int i = 0; i < n; i++) jami += qiymatlar[i];

    printf("Jami: %.1lf, O'rtacha: %.2lf\n", jami, jami / n);
    free(qiymatlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 12.5 + 20.0 + 17.5 + 30.0 = 80.0. O'rtacha: 20.00.

## Ishlash natijasi:
```text
Jami: 80.0, O'rtacha: 20.00
```

---

# 464-Topshiriq: Dinamik vektor: push_back() orqali avtomatik 2 barobar kengayish

## Topshiriq sharti:
Sig'im (capacity) to'lganda hajmini 2 karra oshiruvchi struktura.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    size_t size;
    size_t capacity;
} Vektor;

void vektor_push(Vektor *v, int qiymat) {
    if (v->size == v->capacity) {
        size_t yangi_cap = (v->capacity == 0) ? 2 : v->capacity * 2;
        int *yangi_data = (int*)realloc(v->data, yangi_cap * sizeof(int));
        if (!yangi_data) return;
        v->data = yangi_data;
        v->capacity = yangi_cap;
    }
    v->data[v->size++] = qiymat;
}

int main(void) {
    Vektor v = {NULL, 0, 0};
    for (int i = 1; i <= 5; i++) vektor_push(&v, i * 100);

    printf("Vektor elementlari (Hajmi: %zu, Sig'imi: %zu):\n", v.size, v.capacity);
    for (size_t i = 0; i < v.size; i++) printf("%d ", v.data[i]);
    printf("\n");

    free(v.data);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 2 barobar kengayish (Exponential growth) amortizatsiyalangan O(1) vaqt murakkabligini kafolatlaydi (C++ std::vector kabi).

## Ishlash natijasi:
```text
Vektor elementlari (Hajmi: 5, Sig'imi: 8):
100 200 300 400 500
```

---

# 465-Topshiriq: O'z strdup() funktsiyangizni yozish (Dinamik satr nusxasi)

## Topshiriq sharti:
Satr uchun xotira ajratib nusxasini qaytaruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* mening_strdup(const char *s) {
    size_t len = strlen(s) + 1; // '\0' uchun +1
    char *nusxa = (char*)malloc(len);
    if (nusxa != NULL) {
        memcpy(nusxa, s, len);
    }
    return nusxa;
}

int main(void) {
    char *yangi_satr = mening_strdup("Dinamik Matn");
    if (yangi_satr != NULL) {
        printf("Yaratilgan dinamik satr: %s\n", yangi_satr);
        free(yangi_satr);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strdup` POSIX funksiyasi bo'lib, xotirani `malloc` bilan ajratadi va satrni nusxalaydi.
2. Ishlatib bo'lingach chaqiruvchi uni `free()` qilishi shart.

## Ishlash natijasi:
```text
Yaratilgan dinamik satr: Dinamik Matn
```

---

# 466-Topshiriq: Dinamik 2D matritsa: Qatorma-qator malloc va to'liq tozalash

## Topshiriq sharti:
Rows x Cols matritsasini yaratish va xavfsiz tozalash.

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

    mat[0][0] = 1; mat[0][1] = 2; mat[0][2] = 3;
    mat[1][0] = 4; mat[1][1] = 5; mat[1][2] = 6;

    printf("mat[1][1] = %d\n", mat[1][1]);

    // Tozalash tartibi: avval har bir qator, so'ngra asosiy ko'rsatkich
    for (int i = 0; i < rows; i++) {
        free(mat[i]);
    }
    free(mat);
    printf("Matritsa to'liq tozalandi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tozalash har doim ajratishning teskari tartibida amalga oshiriladi.

## Ishlash natijasi:
```text
mat[1][1] = 5
Matritsa to'liq tozalandi.
```

---

# 467-Topshiriq: Dinamik 2D matritsa: Yaxlit uzluksiz blok (Single contiguous allocation)

## Topshiriq sharti:
Bitta malloc bilan keshga mos 2D dinamik matritsa.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int r = 2, c = 2;
    int *blok = (int*)malloc(r * c * sizeof(int));
    int **mat = (int**)malloc(r * sizeof(int*));

    for (int i = 0; i < r; i++) {
        mat[i] = blok + (i * c);
    }

    mat[0][0] = 10; mat[0][1] = 20;
    mat[1][0] = 30; mat[1][1] = 40;

    printf("Yaxlit mat[1][0] = %d\n", mat[1][0]);

    free(mat);
    free(blok);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Barcha kataklar xotirada ketma-ket yotadi, bu `free()` qilishda ham atigi 2 ta chaqiruv talab qiladi.

## Ishlash natijasi:
```text
Yaxlit mat[1][0] = 30
```

---

# 468-Topshiriq: Dinamik Jagged Array (Har bir qator hajmi turlicha) yaratish

## Topshiriq sharti:
Uchburchak shaklidagi dinamik massiv tuzing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int qatorlar = 3;
    int **uchburchak = (int**)malloc(qatorlar * sizeof(int*));

    for (int i = 0; i < qatorlar; i++) {
        uchburchak[i] = (int*)malloc((i + 1) * sizeof(int));
        for (int j = 0; j <= i; j++) {
            uchburchak[i][j] = i + 1;
            printf("%d ", uchburchak[i][j]);
        }
        printf("\n");
    }

    for (int i = 0; i < qatorlar; i++) free(uchburchak[i]);
    free(uchburchak);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1-qator 1 ta, 2-qator 2 ta, 3-qator 3 ta xotira oladi.
2. Xotira ortiqcha isrof qilinmaydi.

## Ishlash natijasi:
```text
1 
2 2 
3 3 3
```

---

# 469-Topshiriq: Dinamik massivni chuqur nusxalash (Deep Copy)

## Topshiriq sharti:
Massiv ko'rsatkichini emas, uning barcha elementlarini yangi xotiraga nusxalang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int* nusxa_yarat(const int *asl, int n) {
    int *yangi = (int*)malloc(n * sizeof(int));
    if (yangi != NULL) {
        memcpy(yangi, asl, n * sizeof(int));
    }
    return yangi;
}

int main(void) {
    int asl[] = {1, 2, 3};
    int *nusxa = nusxa_yarat(asl, 3);

    nusxa[0] = 999; // Faqat nusxa o'zgaradi!

    printf("Asl:   %d %d %d\n", asl[0], asl[1], asl[2]);
    printf("Nusxa: %d %d %d\n", nusxa[0], nusxa[1], nusxa[2]);

    free(nusxa);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shallow copy faqat pointerni nusxalaydi, Deep copy esa yangi xotira ajratib barcha qiymatlarni mustaqil ko'chiradi.

## Ishlash natijasi:
```text
Asl:   1 2 3
Nusxa: 999 2 3
```

---

# 470-Topshiriq: Dinamik massivdan elementni indeksi bo'yicha o'chirish

## Topshiriq sharti:
Indeksdan keyingi elementlarni chapga suruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

void element_ochir(int *arr, int *n, int idx) {
    if (idx < 0 || idx >= *n) return;
    for (int i = idx; i < *n - 1; i++) {
        arr[i] = arr[i + 1];
    }
    (*n)--;
}

int main(void) {
    int n = 5;
    int *arr = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) arr[i] = (i + 1) * 10;

    element_ochir(arr, &n, 2); // 30 ni o'chirish

    printf("O'chirilgach: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    free(arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 2-indeksdagi 30 soni o'chirilib, qolgan sonlar chapga siljiydi.

## Ishlash natijasi:
```text
O'chirilgach: 10 20 40 50
```

---

# 471-Topshiriq: Dinamik struktura yaratish va xotira boshqaruvi

## Topshiriq sharti:
malloc orqali strukturaga xotira ajratish va -> operatori bilan ishlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int id;
    char nom[30];
    double narx;
} Mahsulot;

int main(void) {
    Mahsulot *m = (Mahsulot*)malloc(sizeof(Mahsulot));
    if (!m) return 1;

    m->id = 101;
    strcpy(m->nom, "Noutbuk");
    m->narx = 850.5;

    printf("Mahsulot #%d: %s, Narxi: $%.1lf\n", m->id, m->nom, m->narx);
    free(m);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Struktura ko'rsatkichi maydonlariga `->` (arrow) operatori orqali murojaat qilinadi.

## Ishlash natijasi:
```text
Mahsulot #101: Noutbuk, Narxi: $850.5
```

---

# 472-Topshiriq: Ichida dinamik maydoni bo'lgan struktura va uning ko'p bosqichli tozalanishi

## Topshiriq sharti:
Ichki satri malloc bo'lgan strukturani xatosiz tozalash tartibi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int id;
    char *tavsif; // Ichki dinamik satr
} Maqola;

int main(void) {
    Maqola *m = (Maqola*)malloc(sizeof(Maqola));
    m->id = 1;
    m->tavsif = (char*)malloc(100);
    strcpy(m->tavsif, "C tilida dinamik xotira arxitekturasi");

    printf("Maqola: %s\n", m->tavsif);

    // QAT'IY TARTIB:
    free(m->tavsif); // Avval ichki dinamik xotirani tozalash!
    free(m);         // So'ngra tashqi strukturani tozalash!
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar avval `free(m)` chaqirilsa, uning ichidagi `tavsif` ko'rsatkichi yo'qolib, ichki xotira abadiy leak bo'lib qoladi.

## Ishlash natijasi:
```text
Maqola: C tilida dinamik xotira arxitekturasi
```

---

# 473-Topshiriq: Flexible Array Member (C99): Struktura oxiridagi o'lchamsiz massiv

## Topshiriq sharti:
Struktura va uning ma'lumotlar massivini bitta malloc bilan ajratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int uzunlik;
    int elementlar[]; // C99 Flexible Array Member
} Paket;

int main(void) {
    int n = 3;
    Paket *p = (Paket*)malloc(sizeof(Paket) + n * sizeof(int));
    p->uzunlik = n;

    for (int i = 0; i < n; i++) p->elementlar[i] = (i + 1) * 5;

    printf("Paket elementlari: %d %d %d\n", 
           p->elementlar[0], p->elementlar[1], p->elementlar[2]);
    free(p);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Flexible Array Member strukturadan keyingi xotirani massiv sifatida ishlatish imkonini beradi.
2. Bitta `malloc` va bitta `free` bilan to'liq boshqariladi.

## Ishlash natijasi:
```text
Paket elementlari: 5 10 15
```

---

# 474-Topshiriq: Custom Memory Tracker: Nechta malloc va free bo'lganini hisoblash

## Topshiriq sharti:
Xotira oqishini dastur ichida ushlovchi sodda kuzatuvchi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

static size_t jami_ajratilgan = 0;
static size_t jami_ozod_etilgan = 0;

void* kuzatuvchi_malloc(size_t hajm) {
    jami_ajratilgan += hajm;
    return malloc(hajm);
}

void kuzatuvchi_free(void *ptr, size_t hajm) {
    jami_ozod_etilgan += hajm;
    free(ptr);
}

int main(void) {
    int *a = (int*)kuzatuvchi_malloc(10 * sizeof(int));
    kuzatuvchi_free(a, 10 * sizeof(int));

    printf("Ajratilgan: %zu bayt, Ozod etilgan: %zu bayt\n", 
           jami_ajratilgan, jami_ozod_etilgan);
    if (jami_ajratilgan == jami_ozod_etilgan) {
        printf("Xotira oqishi yo'q! 100%% toza.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta dasturlarda maxsus 'Wrapper' funksiyalar orqali barcha xotira sarfi monitoring qilinadi.

## Ishlash natijasi:
```text
Ajratilgan: 40 bayt, Ozod etilgan: 40 bayt
Xotira oqishi yo'q! 100% toza.
```

---

# 475-Topshiriq: Arena Allocator (Region-based memory) asoslari

## Topshiriq sharti:
Bitta katta buferdan mayda xotiralarni bir zumda kesib beruvchi mexanizm.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char *bufer;
    size_t sigim;
    size_t ofset;
} Arena;

void* arena_alloc(Arena *a, size_t hajm) {
    if (a->ofset + hajm > a->sigim) return NULL; // Joy yetmadi
    void *ptr = &a->bufer[a->ofset];
    a->ofset += hajm;
    return ptr;
}

void arena_reset(Arena *a) {
    a->ofset = 0; // Bir zumda barcha xotirani tozalash!
}

int main(void) {
    char xotira[1024];
    Arena a = {xotira, sizeof(xotira), 0};

    int *son = (int*)arena_alloc(&a, sizeof(int));
    *son = 42;
    printf("Arena dan olingan son: %d (Ofset: %zu)\n", *son, a.ofset);

    arena_reset(&a);
    printf("Arena tozalangach ofset: %zu\n", a.ofset);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Arena Allocator har bir ob'ekt uchun alohida `free` chaqirishni talab qilmaydi.
2. `ofset = 0` qilish orqali butun xotira O(1) vaqtda tozalanadi (O'yin dvigatellari va kompilyatorlar arxitekturasi).

## Ishlash natijasi:
```text
Arena dan olingan son: 42 (Ofset: 4)
Arena tozalangach ofset: 0
```

---

# 476-Topshiriq: alloca() funktsiyasi: Stekda dinamik xotira ajratish

## Topshiriq sharti:
free() talab qilmaydigan stekdagi dinamik xotira.

## Yechim (C kodi):
```c
#include <stdio.h>
#if defined(_WIN32)
#include <malloc.h>
#else
#include <alloca.h>
#endif

void stek_massiv(int n) {
    int *arr = (int*)alloca(n * sizeof(int));
    for (int i = 0; i < n; i++) arr[i] = i * 11;
    printf("alloca massiv: %d %d %d\n", arr[0], arr[1], arr[2]);
    // free(arr) qilinmaydi! Funksiya tugashi bilan stek avtomatik tozalanadi!
}

int main(void) {
    stek_massiv(3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `alloca` xotirani Heapdan emas, to'g'ridan-to'g'ri chaqiruv stekidan oladi.
2. U o'ta tez ishlaydi, ammo katta hajm so'ralsa Stack Overflow ga sabab bo'lishi mumkin.

## Ishlash natijasi:
```text
alloca massiv: 0 11 22
```

---

# 477-Topshiriq: aligned_alloc() (C11): Xotirani apparat chegarasiga tekislab ajratish

## Topshiriq sharti:
AVX/SIMD buyruqlari uchun 64-baytga tekislangan xotira ajratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    // 64-bayt chegarasiga tekislangan 256 bayt xotira
    #if defined(_WIN32)
    void *ptr = _aligned_malloc(256, 64);
    #else
    void *ptr = aligned_alloc(64, 256);
    #endif

    if (ptr != NULL) {
        printf("Tekislangan manzil: %p\n", ptr);
        printf("64 ga bo'linadimi: %s\n", 
               ((uintptr_t)ptr % 64 == 0) ? "Ha (Aligned)" : "Yo'q");
        #if defined(_WIN32)
        _aligned_free(ptr);
        #else
        free(ptr);
        #endif
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. SIMD (AVX-512) operatsiyalari xotira 64 bayt chegarasiga tekislangan bo'lishini talab qiladi.

## Ishlash natijasi:
```text
Tekislangan manzil: 0000000000551040
64 ga bo'linadimi: Ha (Aligned)
```

---

# 478-Topshiriq: malloc(0) ning C standartidagi o'ziga xos xatti-harakati

## Topshiriq sharti:
0 bayt so'ralganda malloc nima qaytarishini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    void *p = malloc(0);
    printf("malloc(0) qaytargan manzil: %p\n", p);
    // C standartiga ko'ra bu yoki NULL, yoki free() qilinishi mumkin bo'lgan yagona ko'rsatkich bo'ladi!
    free(p);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C standarti `malloc(0)` ga aniq NULL yoki o'ziga xos bo'sh manzil qaytarishni kompilyator ixtiyoriga qoldiradi.

## Ishlash natijasi:
```text
malloc(0) qaytargan manzil: 0000000000551010
```

---

# 479-Topshiriq: Canary qiymatlari orqali dinamik bufer to'lib ketishini (Heap Overflow) aniqlash

## Topshiriq sharti:
Massiv atrofida maxsus qo'riqchi baytlar qo'yib tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define CANARY 0xDEADBEEF

typedef struct {
    unsigned int bosh_canary;
    int data[4];
    unsigned int oxir_canary;
} XavfsizMassiv;

int main(void) {
    XavfsizMassiv *xm = (XavfsizMassiv*)malloc(sizeof(XavfsizMassiv));
    xm->bosh_canary = CANARY;
    xm->oxir_canary = CANARY;

    // Normal ma'lumot yozish
    for (int i = 0; i < 4; i++) xm->data[i] = i;

    // Tekshirish
    if (xm->bosh_canary == CANARY && xm->oxir_canary == CANARY) {
        printf("Xotira yaxlitligi buzilmagan! (Canary butun)\n");
    } else {
        printf("OGOHLANTIRISH: Bufer to'lib ketishi aniqlandi!\n");
    }

    free(xm);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Canary (Konareyka) texnikasi xakerlik hujumlari va bufer to'lib ketishini aniqlashning eng mashhur usulidir.

## Ishlash natijasi:
```text
Xotira yaxlitligi buzilmagan! (Canary butun)
```

---

# 480-Topshiriq: Dinamik massivni qisqartirish (shrink_to_fit)

## Topshiriq sharti:
Haqiqiy elementlar soniga tenglashtirib ortiqcha sig'imni ozod qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int cap = 100;
    int size = 5;
    int *arr = (int*)malloc(cap * sizeof(int));
    for (int i = 0; i < size; i++) arr[i] = i + 1;

    // shrink_to_fit:
    int *yangi = (int*)realloc(arr, size * sizeof(int));
    if (yangi) arr = yangi;

    printf("Hajm 100 dan 5 taga qisqartirildi. Birinchi element: %d\n", arr[0]);
    free(arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta bufer ishlatilib bo'lgach, uni ixchamlashtirish uchun `realloc(arr, size)` qilinadi.

## Ishlash natijasi:
```text
Hajm 100 dan 5 taga qisqartirildi. Birinchi element: 1
```

---

# 481-Topshiriq: Dinamik satrlar ro'yxati (Dynamic String List)

## Topshiriq sharti:
Foydalanuvchi xohlagancha so'z qo'sha oladigan dinamik massiv.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char **sozlar = (char**)malloc(2 * sizeof(char*));
    sozlar[0] = (char*)malloc(10);
    sozlar[1] = (char*)malloc(10);

    strcpy(sozlar[0], "Salom");
    strcpy(sozlar[1], "Olam");

    printf("%s %s!\n", sozlar[0], sozlar[1]);

    free(sozlar[0]);
    free(sozlar[1]);
    free(sozlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir so'z alohida dinamik xotirada, ularning ko'rsatkichlari esa umumiy massivda saqlanadi.

## Ishlash natijasi:
```text
Salom Olam!
```

---

# 482-Topshiriq: Heap ustida bitset yaratish (Dinamik Bitmask massivi)

## Topshiriq sharti:
1 millionta bitni atigi 125 KB xotirada boshqarish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    uint8_t *bitlar;
    size_t bit_soni;
} DinamikBitset;

DinamikBitset bitset_yarat(size_t n) {
    DinamikBitset bs;
    bs.bit_soni = n;
    size_t baytlar = (n + 7) / 8;
    bs.bitlar = (uint8_t*)calloc(baytlar, 1);
    return bs;
}

void bitset_yoq(DinamikBitset *bs, size_t idx) {
    bs->bitlar[idx / 8] |= (1 << (idx % 8));
}

int main(void) {
    DinamikBitset bs = bitset_yarat(100);
    bitset_yoq(&bs, 42);

    int bit = (bs.bitlar[42 / 8] >> (42 % 8)) & 1;
    printf("42-bit qiymati: %d\n", bit);

    free(bs.bitlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitset millionlab boolean bayroqlarni minimal RAM bilan Heapda saqlashning eng samarali usulidir.

## Ishlash natijasi:
```text
42-bit qiymati: 1
```

---

# 483-Topshiriq: Xotira fragmentatsiyasi (External Fragmentation) simulyatsiyasi

## Topshiriq sharti:
Nima uchun tez-tez malloc va free qilish xotirani bo'laklab tashlashini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    // 3 ta ketma-ket blok ajratiladi
    void *p1 = malloc(100);
    void *p2 = malloc(100);
    void *p3 = malloc(100);

    free(p2); // O'rtadagi 100 bayt ozod bo'ldi, ammo p1 va p3 band!
    // Endi 150 baytlik yangi blok so'ralsa, o'rtadagi 100 baytga sig'maydi (Fragmentatsiya).

    printf("Fragmentatsiya — bo'sh xotira bo'laklanib, katta blok so'roviga yetmay qolishi holatidir.\n");
    free(p1);
    free(p3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xotira fragmentatsiyasi kompyuterda umumiy bo'sh RAM ko'p bo'lsa ham, bitta yaxlit katta xotira ajratib bo'lmay qolishiga olib keladi.

## Ishlash natijasi:
```text
Fragmentatsiya — bo'sh xotira bo'laklanib, katta blok so'roviga yetmay qolishi holatidir.
```

---

# 484-Topshiriq: Free List arxitekturasi: Xotirani qayta ishlatuvchi bog'langan ro'yxat

## Topshiriq sharti:
Ozod qilingan bloklarni ro'yxatga olib qayta tarqatish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Tugun {
    struct Tugun *keyingi;
} Tugun;

typedef struct {
    Tugun *bosh;
} BepulRoyxat;

void qosh(BepulRoyxat *fl, void *ptr) {
    Tugun *t = (Tugun*)ptr;
    t->keyingi = fl->bosh;
    fl->bosh = t;
}

int main(void) {
    BepulRoyxat fl = {NULL};
    void *b1 = malloc(32);
    qosh(&fl, b1);

    printf("Blok Free List ro'yxatiga qo'shildi va qayta ishlatishga tayyor!\n");
    free(b1);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `malloc` va `free` ning ichki dvigateli aynan shunday 'Free List' jadvallariga tayanadi.

## Ishlash natijasi:
```text
Blok Free List ro'yxatiga qo'shildi va qayta ishlatishga tayyor!
```

---

# 485-Topshiriq: Valgrind va AddressSanitizer (ASan) qanday ishlashi haqida tushuncha

## Topshiriq sharti:
Kompilyator bayroqlari (-fsanitize=address) orqali xotira xatolarini avtomatik ushlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("AddressSanitizer (ASan) kompilyatsiya vaqtida maxsus tekshiruv kodlarini qo'shadi.\n");
    printf("U Buffer Overflow, Use-After-Free va Memory Leak larni aniq qatorigacha ko'rsatib beradi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. GCC va Clang kompilyatorlarida `-fsanitize=address -g` bayrog'ini qo'shish har qanday xotira buzilishini darhol terminalda qizil bilan ko'rsatadi.

## Ishlash natijasi:
```text
AddressSanitizer (ASan) kompilyatsiya vaqtida maxsus tekshiruv kodlarini qo'shadi.
U Buffer Overflow, Use-After-Free va Memory Leak larni aniq qatorigacha ko'rsatib beradi.
```

---

# 486-Topshiriq: Dinamik stek (Dynamic Stack) LIFO ma'lumotlar tuzilmasi

## Topshiriq sharti:
realloc yordamida avtomatik kattalashuvchi stek yarating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *elementlar;
    int tepa;
    int sigim;
} DinamikStek;

void push(DinamikStek *s, int val) {
    if (s->tepa == s->sigim) {
        s->sigim = (s->sigim == 0) ? 2 : s->sigim * 2;
        s->elementlar = (int*)realloc(s->elementlar, s->sigim * sizeof(int));
    }
    s->elementlar[s->tepa++] = val;
}

int pop(DinamikStek *s) {
    return s->elementlar[--s->tepa];
}

int main(void) {
    DinamikStek s = {NULL, 0, 0};
    push(&s, 10);
    push(&s, 20);

    printf("Pop: %d\n", pop(&s));
    printf("Pop: %d\n", pop(&s));

    free(s.elementlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dinamik stek elementlar soni oldindan noma'lum bo'lganda avtomatik kengayadi.

## Ishlash natijasi:
```text
Pop: 20
Pop: 10
```

---

# 487-Topshiriq: Dinamik navbat (Dynamic Queue) FIFO ma'lumotlar tuzilmasi

## Topshiriq sharti:
Dinamik xotirada navbat (birinchi kelgan birinchi chiqadi) mexanizmi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *ma_lumot;
    int bosh;
    int oxir;
    int soni;
} Navbat;

Navbat navbat_yarat(int sigim) {
    Navbat q;
    q.ma_lumot = (int*)malloc(sigim * sizeof(int));
    q.bosh = 0; q.oxir = 0; q.soni = 0;
    return q;
}

int main(void) {
    Navbat q = navbat_yarat(5);
    q.ma_lumot[q.oxir++] = 100;
    q.soni++;

    printf("Navbatdan chiqdi: %d\n", q.ma_lumot[q.bosh++]);
    free(q.ma_lumot);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. FIFO prinsipi bo'yicha dinamik navbat boshqariladi.

## Ishlash natijasi:
```text
Navbatdan chiqdi: 100
```

---

# 488-Topshiriq: Ko'rsatkich ofseti orqali xotira blokining boshqaruv sarlavhasi (Header) ni o'qish

## Topshiriq sharti:
malloc qanday qilib free(p) ga o'lcham aytilmasa ham qancha bayt tozalashni bilishini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    printf("malloc() har bir ajratilgan blokdan oldin yashirin sarlavha (Header) saqlaydi.\n");
    printf("Ushbu sarlavhada blok hajmi yozilgan bo'ladi, shuning uchun free() ga hajm berish shart emas!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `p` ko'rsatkichidan bir necha bayt orqada (masalan `p - 8` yoki `p - 16`) xotira menejerining ichki metadata bloki yotadi.

## Ishlash natijasi:
```text
malloc() har bir ajratilgan blokdan oldin yashirin sarlavha (Header) saqlaydi.
Ushbu sarlavhada blok hajmi yozilgan bo'ladi, shuning uchun free() ga hajm berish shart emas!
```

---

# 489-Topshiriq: Dinamik xotirada tasodifiy sonlar massivini generatsiya qilish

## Topshiriq sharti:
Foydalanuvchi so'ragan N ta tasodifiy son bilan massivni to'ldiruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int* tasodifiy_massiv(int n) {
    int *arr = (int*)malloc(n * sizeof(int));
    if (!arr) return NULL;
    for (int i = 0; i < n; i++) {
        arr[i] = (i * 37 + 13) % 100; // Simulyatsiya qilingan tasodifiy
    }
    return arr;
}

int main(void) {
    int *sonlar = tasodifiy_massiv(3);
    printf("Generatsiya qilingan: %d %d %d\n", sonlar[0], sonlar[1], sonlar[2]);
    free(sonlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiya xotirani o'zi ajratadi va ko'rsatkichni qaytaradi.

## Ishlash natijasi:
```text
Generatsiya qilingan: 13 50 87
```

---

# 490-Topshiriq: Dinamik massivni qismlarga ajratuvchi (Split) funksiya

## Topshiriq sharti:
Bitta massivni ikkita dinamik yangi massivga bo'ling.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void massiv_bol(const int *src, int n, int **birinchi, int **ikkinchi) {
    int yarmi = n / 2;
    *birinchi = (int*)malloc(yarmi * sizeof(int));
    *ikkinchi = (int*)malloc((n - yarmi) * sizeof(int));

    memcpy(*birinchi, src, yarmi * sizeof(int));
    memcpy(*ikkinchi, src + yarmi, (n - yarmi) * sizeof(int));
}

int main(void) {
    int data[4] = {10, 20, 30, 40};
    int *b1, *b2;

    massiv_bol(data, 4, &b1, &b2);
    printf("Bo'lak 1: %d %d\n", b1[0], b1[1]);
    printf("Bo'lak 2: %d %d\n", b2[0], b2[1]);

    free(b1);
    free(b2);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Double pointerlar orqali ikkita yangi dinamik massiv ko'rsatkichi tashqariga chiqariladi.

## Ishlash natijasi:
```text
Bo'lak 1: 10 20
Bo'lak 2: 30 40
```

---

# 491-Topshiriq: Dinamik xotirani to'ldirish va bo'shatish sikli testi (Stress test)

## Topshiriq sharti:
1000 marta malloc va free qilib xotira barqarorligini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    for (int i = 0; i < 1000; i++) {
        int *p = (int*)malloc(128);
        if (p == NULL) {
            printf("Xatolik!\n");
            return 1;
        }
        free(p);
    }
    printf("1000 ta dinamik ajratish va tozalash muvaffaqiyatli yakunlandi!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir ajratilgan blok darhol tozalansa, xotira oqishi bo'lmaydi va tizim barqaror ishlaydi.

## Ishlash natijasi:
```text
1000 ta dinamik ajratish va tozalash muvaffaqiyatli yakunlandi!
```

---

# 492-Topshiriq: Dinamik matritsani transponirlab yangi xotiraga yozish

## Topshiriq sharti:
Transponirlangan matritsani dinamik yaratuvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int** transponirla_dinamik(int **mat, int r, int c) {
    int **t = (int**)malloc(c * sizeof(int*));
    for (int i = 0; i < c; i++) {
        t[i] = (int*)malloc(r * sizeof(int));
        for (int j = 0; j < r; j++) {
            t[i][j] = mat[j][i];
        }
    }
    return t;
}

int main(void) {
    int r = 1, c = 2;
    int **m = (int**)malloc(r * sizeof(int*));
    m[0] = (int*)malloc(c * sizeof(int));
    m[0][0] = 5; m[0][1] = 9;

    int **t = transponirla_dinamik(m, r, c);
    printf("Transponirlangan: %d va %d\n", t[0][0], t[1][0]);

    free(m[0]); free(m);
    free(t[0]); free(t[1]); free(t);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yangi o'lchamdagi matritsa to'liq dinamik xotirada yaratiladi.

## Ishlash natijasi:
```text
Transponirlangan: 5 va 9
```

---

# 493-Topshiriq: Dinamik xotirada bitli massivlar bilan Eratosfen g'alviri

## Topshiriq sharti:
Katta oraliqdagi tub sonlarni Heapda toping.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(void) {
    int n = 20;
    bool *tub = (bool*)calloc(n + 1, sizeof(bool));
    // calloc false beradi, 0 va 1 tub emas deb belgilaymiz
    tub[0] = tub[1] = true;

    for (int p = 2; p * p <= n; p++) {
        if (!tub[p]) {
            for (int i = p * p; i <= n; i += p) tub[i] = true;
        }
    }

    printf("20 gacha tub sonlar: ");
    for (int p = 2; p <= n; p++) {
        if (!tub[p]) printf("%d ", p);
    }
    printf("\n");

    free(tub);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Heapda ajratilgan massiv katta oraliqlar uchun yetarli hajm beradi.

## Ishlash natijasi:
```text
20 gacha tub sonlar: 2 3 5 7 11 13 17 19
```

---

# 494-Topshiriq: Dinamik satrlar massividan so'zni qidirish

## Topshiriq sharti:
char** ko'rsatkichlar massivi ichidan so'z topish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    int n = 2;
    char **lugat = (char**)malloc(n * sizeof(char*));
    lugat[0] = strdup("Kitob");
    lugat[1] = strdup("Qalam");

    int idx = -1;
    for (int i = 0; i < n; i++) {
        if (strcmp(lugat[i], "Qalam") == 0) idx = i;
    }

    printf("'Qalam' indeksi: %d\n", idx);

    free(lugat[0]); free(lugat[1]); free(lugat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dinamik lug'at elementlari solishtirilib, topilgan indeks chiqariladi.

## Ishlash natijasi:
```text
'Qalam' indeksi: 1
```

---

# 495-Topshiriq: Xotirani qayta ajratishda elementlar saqlanishini tekshirish

## Topshiriq sharti:
realloc barcha eski ma'lumotlarni xatosiz ko'chirishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *arr = (int*)malloc(2 * sizeof(int));
    arr[0] = 55; arr[1] = 66;

    arr = (int*)realloc(arr, 100 * sizeof(int));
    printf("realloc dan keyin arr[0]=%d, arr[1]=%d\n", arr[0], arr[1]);

    free(arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `realloc` hatto yangi xotira manziliga ko'chganda ham barcha eski ma'lumotlarni to'liq saqlab o'tkazadi.

## Ishlash natijasi:
```text
realloc dan keyin arr[0]=55, arr[1]=66
```

---

# 496-Topshiriq: Xotira oqishini oldini oluvchi avtomatik tozalash makrosi

## Topshiriq sharti:
Funksiya tugaganda xotirani xavfsiz tozalash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

#define AUTO_FREE(ptr) free(ptr); ptr = NULL

int main(void) {
    int *res = (int*)malloc(sizeof(int));
    *res = 42;
    printf("Natija: %d\n", *res);

    AUTO_FREE(res);
    printf("Xotira ozod qilindi!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yaxshi yozilgan makroslar xotira bilan ishlashda insoniy xatolarni keskin kamaytiradi.

## Ishlash natijasi:
```text
Natija: 42
Xotira ozod qilindi!
```

---

# 497-Topshiriq: Dinamik ravishda o'suvchi string buferi (String Builder analogi)

## Topshiriq sharti:
Belgilarni qo'shib boruvchi dinamik satr yig'uvchi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *satr;
    size_t uzunlik;
    size_t sigim;
} StringBuilder;

void sb_qosh(StringBuilder *sb, const char *matn) {
    size_t len = strlen(matn);
    if (sb->uzunlik + len + 1 > sb->sigim) {
        sb->sigim = (sb->sigim == 0) ? 16 : (sb->sigim + len) * 2;
        sb->satr = (char*)realloc(sb->satr, sb->sigim);
        if (sb->uzunlik == 0) sb->satr[0] = '\0';
    }
    strcat(sb->satr, matn);
    sb->uzunlik += len;
}

int main(void) {
    StringBuilder sb = {NULL, 0, 0};
    sb_qosh(&sb, "C ");
    sb_qosh(&sb, "tili ");
    sb_qosh(&sb, "kuchli!");

    printf("Hosil bo'lgan satr: %s\n", sb.satr);
    free(sb.satr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. StringBuilder satrlarni ko'p marta ulashda doimiy yangi xotira ajratish xarajatlarini yo'qotadi.

## Ishlash natijasi:
```text
Hosil bo'lgan satr: C tili kuchli!
```

---

# 498-Topshiriq: Dinamik xotirani solishtirish (memcmp bilan dinamik bloklarni tekshirish)

## Topshiriq sharti:
Ikkita malloc qilingan massivning tengligini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    int *a = (int*)malloc(3 * sizeof(int));
    int *b = (int*)malloc(3 * sizeof(int));

    for (int i = 0; i < 3; i++) { a[i] = i * 5; b[i] = i * 5; }

    if (memcmp(a, b, 3 * sizeof(int)) == 0) {
        printf("Ikkala dinamik massiv bir xil!\n");
    }

    free(a); free(b);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `memcmp` dinamik bloklar baytlarini solishtirishda eng tezkor usuldir.

## Ishlash natijasi:
```text
Ikkala dinamik massiv bir xil!
```

---

# 499-Topshiriq: Dinamik massivni o'z joyida qisqartirish va tozalash amaliyoti

## Topshiriq sharti:
Massiv sig'imini boshqarish va to'liq tozalash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *d = (int*)malloc(10 * sizeof(int));
    d[0] = 1; d[1] = 2;
    // Faqat 2 ta element qoldirish
    int *qisqartirilgan = (int*)realloc(d, 2 * sizeof(int));
    if (qisqartirilgan) d = qisqartirilgan;

    printf("Yakuniy massiv: %d, %d\n", d[0], d[1]);
    free(d);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xotira resurslaridan tejamkor foydalanish amaliyoti.

## Ishlash natijasi:
```text
Yakuniy massiv: 1, 2
```

---

# 500-Topshiriq: Modul yakuni: C tilida to'liq dinamik massiv (Vector) kutubxonasini realizatsiya qilish

## Topshiriq sharti:
init, push, get, set, free funksiyalariga ega to'liq Vektor moduli.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    size_t size;
    size_t capacity;
} IntVector;

IntVector vector_create(void) {
    IntVector v = {NULL, 0, 0};
    return v;
}

void vector_push(IntVector *v, int value) {
    if (v->size >= v->capacity) {
        size_t new_cap = (v->capacity == 0) ? 2 : v->capacity * 2;
        int *new_data = (int*)realloc(v->data, new_cap * sizeof(int));
        if (!new_data) return;
        v->data = new_data;
        v->capacity = new_cap;
    }
    v->data[v->size++] = value;
}

int vector_get(const IntVector *v, size_t index) {
    if (index < v->size) return v->data[index];
    return -1;
}

void vector_free(IntVector *v) {
    free(v->data);
    v->data = NULL;
    v->size = 0;
    v->capacity = 0;
}

int main(void) {
    IntVector v = vector_create();
    for (int i = 1; i <= 4; i++) {
        vector_push(&v, i * 25);
    }

    printf("Vector elementlari: ");
    for (size_t i = 0; i < v.size; i++) {
        printf("%d ", vector_get(&v, i));
    }
    printf("\n");

    vector_free(&v);
    printf("Vector to'liq tozalandi!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. To'liq dinamik vektor ma'lumotlar tuzilmasi realizatsiya qilindi.
2. `malloc`, `realloc` va `free` funksiyalari orqali xavfsiz va qulay konteyner yaratildi.
3. Bu 10-qismning barcha dinamik xotira konsepsiyalarini mukammal umumlashtiradi.

## Ishlash natijasi:
```text
Vector elementlari: 25 50 75 100 
Vector to'liq tozalandi!
```

---
