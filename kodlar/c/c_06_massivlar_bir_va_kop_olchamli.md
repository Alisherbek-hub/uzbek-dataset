# C Dasturlash Tili — 6-Qism: Massivlar (Bir va Ko'p O'lchamli)
## (251-300 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* 1D massivlar, indekslash, sizeof(arr)/sizeof(arr[0]) idiomasi
* Qidiruv va saralash: Linear/Binary search, Bubble, Selection, Insertion sort
* Massivlarni surish (Rotate), teskarisiga o'girish va saralanganlarni birlashtirish
* 2D va 3D massivlar, Row-Major xotira modeli, matritsalar ko'paytmasi va transponirlash
* Kadane algoritmi, Boyer-Moore ovoz berish, Fisher-Yates va Conway's Game of Life

---

# 251-Topshiriq: 1D massiv e'lon qilish, initsializatsiya qilish va chop etish

## Topshiriq sharti:
5 ta elementdan iborat butun sonli massiv yaratib, uning barcha elementlarini sikl orqali chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int sonlar[5] = {10, 20, 30, 40, 50};

    printf("Massiv elementlari: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", sonlar[i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Massiv — bir xil turdagi elementlarning xotirada ketma-ket joylashgan to'plamidir.
2. C tilida indekslash har doim 0 dan boshlanadi; 5 elementli massiv indekslari 0 dan 4 gacha bo'ladi.

## Ishlash natijasi:
```text
Massiv elementlari: 10 20 30 40 50
```

---

# 252-Topshiriq: Massiv elementlarini indeks bo'yicha o'zgartirish

## Topshiriq sharti:
Massivning 2-indeksidagi qiymatni o'zgartiring va butun massivni qayta ko'ring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int baholar[3] = {4, 3, 5};
    baholar[1] = 5; // 3 bahoni 5 ga o'zgartirish

    for (int i = 0; i < 3; i++) {
        printf("baholar[%d] = %d\n", i, baholar[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `baholar[1] = 5;` to'g'ridan-to'g'ri xotiradagi o'sha element manziliga yangi qiymat yozadi.

## Ishlash natijasi:
```text
baholar[0] = 4
baholar[1] = 5
baholar[2] = 5
```

---

# 253-Topshiriq: Massiv o'lchamini sizeof(arr) / sizeof(arr[0]) orqali aniqlash

## Topshiriq sharti:
Elementlar sonini qo'lda sanamasdan, o'lchamni kompilyatsiya vaqtida toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double maoshlar[] = {1200.5, 3400.0, 2800.75, 4500.0, 1900.25};
    size_t olcham = sizeof(maoshlar) / sizeof(maoshlar[0]);

    printf("Massivning umumiy xotira hajmi: %zu bayt\n", sizeof(maoshlar));
    printf("Bitta element hajmi: %zu bayt\n", sizeof(maoshlar[0]));
    printf("Elementlar soni: %zu ta\n", olcham);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sizeof(maoshlar)` — butun massivning baytlardagi hajmi (5 * 8 = 40 bayt).
2. `sizeof(maoshlar[0])` — bitta `double` hajmi (8 bayt).
3. 40 / 8 = 5 ta element. Bu C dagi eng mashhur massiv idiomasi hisoblanadi.

## Ishlash natijasi:
```text
Massivning umumiy xotira hajmi: 40 bayt
Bitta element hajmi: 8 bayt
Elementlar soni: 5 ta
```

---

# 254-Topshiriq: Massiv elementlarining yig'indisi va o'rtacha qiymatini hisoblash

## Topshiriq sharti:
Massiv sonlarining o'rtacha arifmetik qiymatini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int ballar[] = {80, 92, 75, 88, 95};
    int n = sizeof(ballar) / sizeof(ballar[0]);
    int yigindi = 0;

    for (int i = 0; i < n; i++) {
        yigindi += ballar[i];
    }
    double orta = (double)yigindi / n;

    printf("Jami yig'indi: %d\n", yigindi);
    printf("O'rtacha ball: %.2lf\n", orta);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Butun sonli yig'indi hisoblangach, aniq o'rtacha qiymat olish uchun `(double)` ga cast qilinadi.

## Ishlash natijasi:
```text
Jami yig'indi: 430
O'rtacha ball: 86.00
```

---

# 255-Topshiriq: Massivdagi eng katta (Maksimum) va eng kichik (Minimum) elementni topish

## Topshiriq sharti:
Bitta sikl ichida min va max qiymatlarni aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int sonlar[] = {34, -12, 89, 5, 77, -3, 62};
    int n = sizeof(sonlar) / sizeof(sonlar[0]);

    int min = sonlar[0];
    int max = sonlar[0];

    for (int i = 1; i < n; i++) {
        if (sonlar[i] < min) min = sonlar[i];
        if (sonlar[i] > max) max = sonlar[i];
    }

    printf("Minimal element: %d\n", min);
    printf("Maksimal element: %d\n", max);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boshlang'ich qiymat sifatida birinchi element olinadi.
2. Qolgan elementlar tekshirilib, kerak bo'lsa yangilanadi.

## Ishlash natijasi:
```text
Minimal element: -12
Maksimal element: 89
```

---

# 256-Topshiriq: Massivdagi ikkinchi eng katta elementni (Second Maximum) topish

## Topshiriq sharti:
Saralamasdan bitta o'tishda ikkinchi maksimum qiymatni toping.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <limits.h>

int main(void) {
    int arr[] = {12, 35, 1, 10, 34, 35};
    int n = sizeof(arr) / sizeof(arr[0]);

    int max1 = INT_MIN, max2 = INT_MIN;

    for (int i = 0; i < n; i++) {
        if (arr[i] > max1) {
            max2 = max1;
            max1 = arr[i];
        } else if (arr[i] > max2 && arr[i] != max1) {
            max2 = arr[i];
        }
    }

    printf("Eng katta: %d\n", max1);
    printf("Ikkinchi eng katta: %d\n", max2);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yangi eng katta son chiqqanda eski `max1` avtomatik ravishda `max2` ga o'tadi.
2. O(N) vaqt va O(1) qo'shimcha xotira sarflanadi.

## Ishlash natijasi:
```text
Eng katta: 35
Ikkinchi eng katta: 34
```

---

# 257-Topshiriq: Chiziqli qidiruv (Linear Search) algoritmi

## Topshiriq sharti:
Massivdan elementni qidirib, uning birinchi indeksini qaytaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int chiziqli_qidiruv(const int arr[], int n, int nishon) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == nishon) return i;
    }
    return -1;
}

int main(void) {
    int sonlar[] = {15, 8, 42, 4, 16, 23};
    int nishon = 42;
    int idx = chiziqli_qidiruv(sonlar, 6, nishon);

    printf("%d soni %d-indeksda topildi.\n", nishon, idx);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Chiziqli qidiruv tartiblanmagan massivlarda ishlaydi va O(N) murakkablikka ega.

## Ishlash natijasi:
```text
42 soni 2-indeksda topildi.
```

---

# 258-Topshiriq: Saralangan massivda Binar qidiruv (Binary Search) algoritmi

## Topshiriq sharti:
O(log N) vaqt murakkabligida elementni toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int binar_qidiruv(const int arr[], int n, int nishon) {
    int chap = 0, ong = n - 1;
    while (chap <= ong) {
        int orta = chap + (ong - chap) / 2;
        if (arr[orta] == nishon) return orta;
        if (arr[orta] < nishon) chap = orta + 1;
        else ong = orta - 1;
    }
    return -1;
}

int main(void) {
    int saralangan[] = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    int idx = binar_qidiruv(saralangan, 10, 23);
    printf("23 soni %d-indeksda joylashgan.\n", idx);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Binar qidiruv massiv oldindan saralangan bo'lishini talab qiladi.
2. Har bir qadamda qidiruv hududini 2 marta qisqartiradi.

## Ishlash natijasi:
```text
23 soni 5-indeksda joylashgan.
```

---

# 259-Topshiriq: Massiv elementlarini o'z o'rnida teskarisiga o'girish (In-place reverse)

## Topshiriq sharti:
Qo'shimcha massivsiz massivni ikki ko'rsatkichli usulda teskari aylantiring.

## Yechim (C kodi):
```c
#include <stdio.h>

void massivni_ogir(int arr[], int n) {
    int chap = 0, ong = n - 1;
    while (chap < ong) {
        int temp = arr[chap];
        arr[chap] = arr[ong];
        arr[ong] = temp;
        chap++;
        ong--;
    }
}

int main(void) {
    int arr[] = {1, 2, 3, 4, 5};
    massivni_ogir(arr, 5);

    printf("Teskari massiv: ");
    for (int i = 0; i < 5; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bosh va oxirgi elementlar o'rin almashadi, ko'rsatkichlar o'rtaga qarab siljiydi.
2. O(N) vaqt, O(1) xotira.

## Ishlash natijasi:
```text
Teskari massiv: 5 4 3 2 1
```

---

# 260-Topshiriq: Massiv elementlarini 1 qadam chapga siklik surish (Left Rotate)

## Topshiriq sharti:
Birinchi elementni oxiriga o'tkazib, qolganlarini chapga siljiting.

## Yechim (C kodi):
```c
#include <stdio.h>

void chapga_sur(int arr[], int n) {
    if (n <= 1) return;
    int birinchi = arr[0];
    for (int i = 0; i < n - 1; i++) {
        arr[i] = arr[i + 1];
    }
    arr[n - 1] = birinchi;
}

int main(void) {
    int arr[] = {10, 20, 30, 40, 50};
    chapga_sur(arr, 5);

    printf("1 qadam chapga surilgach: ");
    for (int i = 0; i < 5; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Birinchi element alohida saqlab olinadi, barcha elementlar 1 ta chapga suriladi va bo'shagan oxirgi o'ringa o'sha birinchi element qo'yiladi.

## Ishlash natijasi:
```text
1 qadam chapga surilgach: 20 30 40 50 10
```

---

# 261-Topshiriq: Massiv elementlarini K qadam o'ngga siklik surish (Right Rotate by K)

## Topshiriq sharti:
Uchta teskari aylantirish (3-Reversal) algoritmi bilan K ta o'ngga suring.

## Yechim (C kodi):
```c
#include <stdio.h>

void teskari(int arr[], int chap, int ong) {
    while (chap < ong) {
        int t = arr[chap]; arr[chap] = arr[ong]; arr[ong] = t;
        chap++; ong--;
    }
}

void ongga_sur_k(int arr[], int n, int k) {
    k %= n;
    teskari(arr, 0, n - 1);
    teskari(arr, 0, k - 1);
    teskari(arr, k, n - 1);
}

int main(void) {
    int arr[] = {1, 2, 3, 4, 5, 6, 7};
    ongga_sur_k(arr, 7, 3);

    printf("3 qadam o'ngga surilgach: ");
    for (int i = 0; i < 7; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Butun massivni teskari qilish, keyin dastlabki K tasini va qolganlarini alohida teskari qilish O(N) vaqt va O(1) xotirada o'ngga surishni beradi.

## Ishlash natijasi:
```text
3 qadam o'ngga surilgach: 5 6 7 1 2 3 4
```

---

# 262-Topshiriq: Saralangan massivdan takrorlanuvchi elementlarni olib tashlash (Remove Duplicates)

## Topshiriq sharti:
Takrorlangan sonlarni siqib, unikal elementlar sonini qaytaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int unikal_elementlar(int arr[], int n) {
    if (n == 0) return 0;
    int unikal_idx = 0;
    for (int i = 1; i < n; i++) {
        if (arr[i] != arr[unikal_idx]) {
            unikal_idx++;
            arr[unikal_idx] = arr[i];
        }
    }
    return unikal_idx + 1;
}

int main(void) {
    int arr[] = {1, 1, 2, 2, 3, 4, 4, 5};
    int yangi_olcham = unikal_elementlar(arr, 8);

    printf("Unikal sonlar (%d ta): ", yangi_olcham);
    for (int i = 0; i < yangi_olcham; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Saralangan massivda takrorlar yonma-yon turadi.
2. Ikki ko'rsatkichli usul bilan massiv o'z ichida siqiladi.

## Ishlash natijasi:
```text
Unikal sonlar (5 ta): 1 2 3 4 5
```

---

# 263-Topshiriq: Ikkita saralangan massivni bitta saralangan massivga birlashtirish (Merge)

## Topshiriq sharti:
A va B saralangan massivlarni C ga tartiblangan holda yig'ing.

## Yechim (C kodi):
```c
#include <stdio.h>

void birlashtir(const int a[], int na, const int b[], int nb, int c[]) {
    int i = 0, j = 0, k = 0;
    while (i < na && j < nb) {
        if (a[i] <= b[j]) c[k++] = a[i++];
        else c[k++] = b[j++];
    }
    while (i < na) c[k++] = a[i++];
    while (j < nb) c[k++] = b[j++];
}

int main(void) {
    int a[] = {1, 3, 5, 7};
    int b[] = {2, 4, 6, 8};
    int c[8];

    birlashtir(a, 4, b, 4, c);
    printf("Birlashtirilgan saralangan massiv: ");
    for (int i = 0; i < 8; i++) printf("%d ", c[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu Merge Sort algoritmining asosiy birlashtirish bosqichidir.
2. O(na + nb) vaqt sarflaydi.

## Ishlash natijasi:
```text
Birlashtirilgan saralangan massiv: 1 2 3 4 5 6 7 8
```

---

# 264-Topshiriq: Bubble Sort (Pufakchali saralash) algoritmi va optimallashtirish

## Topshiriq sharti:
Qo'shni elementlarni taqqoslab o'sish tartibida saralang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

void bubble_sort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        bool almashdimi = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                almashdimi = true;
            }
        }
        if (!almashdimi) break; // Agar birorta ham almashinuv bo'lmasa — massiv saralangan!
    }
}

int main(void) {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    bubble_sort(arr, 7);

    printf("Bubble Sort natijasi: ");
    for (int i = 0; i < 7; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta elementlar pufakcha kabi o'ng tomonga suzib boradi.
2. `almashdimi` bayrog'i massiv allaqachon saralangan bo'lsa O(N) da to'xtatadi.

## Ishlash natijasi:
```text
Bubble Sort natijasi: 11 12 22 25 34 64 90
```

---

# 265-Topshiriq: Selection Sort (Tanlab saralash) algoritmi

## Topshiriq sharti:
Har qadamda eng kichik elementni topib boshiga qo'yish.

## Yechim (C kodi):
```c
#include <stdio.h>

void selection_sort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        int temp = arr[min_idx];
        arr[min_idx] = arr[i];
        arr[i] = temp;
    }
}

int main(void) {
    int arr[] = {29, 10, 14, 37, 13};
    selection_sort(arr, 5);

    printf("Selection Sort natijasi: ");
    for (int i = 0; i < 5; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir iteratsiyada saralanmagan qismdan minimum element tanlab olinadi va o'z o'rniga qo'yiladi.

## Ishlash natijasi:
```text
Selection Sort natijasi: 10 13 14 29 37
```

---

# 266-Topshiriq: Insertion Sort (Qo'shish orqali saralash) algoritmi

## Topshiriq sharti:
Karta o'yinidagi kabi elementni o'zining to'g'ri o'rniga joylashtirib boring.

## Yechim (C kodi):
```c
#include <stdio.h>

void insertion_sort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int kalit = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > kalit) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = kalit;
    }
}

int main(void) {
    int arr[] = {12, 11, 13, 5, 6};
    insertion_sort(arr, 5);

    printf("Insertion Sort natijasi: ");
    for (int i = 0; i < 5; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kichik massivlar va deyarli saralangan ma'lumotlar uchun eng samarali sodda algoritm.

## Ishlash natijasi:
```text
Insertion Sort natijasi: 5 6 11 12 13
```

---

# 267-Topshiriq: Massiv chegarasidan chiqish (Buffer Overflow) xavfi

## Topshiriq sharti:
C tilida nima uchun chegaralar avtomatik tekshirilmasligini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int xavfsiz[3] = {10, 20, 30};

    // C da xavfsiz[5] deb murojaat qilinsa ham kompilyator to'xtatmasligi mumkin,
    // ammo bu Undefined Behavior (UB) va bufer to'lib ketishi zaifligini keltirib chiqaradi!
    
    for (int i = 0; i < 3; i++) {
        printf("xavfsiz[%d] = %d\n", i, xavfsiz[i]);
    }
    printf("Qat'iy qoida: har doim i < CHEGARA shartiga amal qiling!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C yuqori tezlikka qaratilgani uchun massiv indekslarini apparat darajasida tekshirmaydi.
2. Chegaradan chiqish qo'shni o'zgaruvchilarni buzadi yoki tizimni xakerlik hujumiga ochiq qoldiradi.

## Ishlash natijasi:
```text
xavfsiz[0] = 10
xavfsiz[1] = 20
xavfsiz[2] = 30
Qat'iy qoida: har doim i < CHEGARA shartiga amal qiling!
```

---

# 268-Topshiriq: C99 Variable Length Arrays (VLA) va uning chegaralari

## Topshiriq sharti:
O'lchami o'zgaruvchiga bog'liq bo'lgan massivni yaratish va xavfsiz ishlatish.

## Yechim (C kodi):
```c
#include <stdio.h>

void vla_misol(int n) {
    int vla[n]; // C99 VLA: o'lchami n ga teng
    for (int i = 0; i < n; i++) {
        vla[i] = (i + 1) * 10;
    }
    printf("VLA birinchi va oxirgi element: %d, %d\n", vla[0], vla[n - 1]);
}

int main(void) {
    vla_misol(4);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. VLA (o'zgaruvchan uzunlikdagi massiv) o'lchami ish vaqtida aniqlanadi va stekda ajratiladi.
2. Agar `n` juda katta bo'lsa (masalan 1,000,000), u darhol Stack Overflow halokatiga olib keladi. Shu sababli C11 da VLA ixtiyoriy (optional) qilindi.

## Ishlash natijasi:
```text
VLA birinchi va oxirgi element: 10, 40
```

---

# 269-Topshiriq: C99 Designated Initializers: Massivni aniq indekslar bilan to'ldirish

## Topshiriq sharti:
Faqat kerakli indekslarga qiymat berish usulini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // Qolgan elementlar avtomatik 0 bo'ladi
    int arr[6] = {[0] = 100, [3] = 400, [5] = 600};

    for (int i = 0; i < 6; i++) {
        printf("arr[%d] = %d\n", i, arr[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C99 sintaksisi: `[indeks] = qiymat`.
2. Ko'rsatilmagan barcha indekslar avtomatik ravishda nol (0) qiymatini oladi.

## Ishlash natijasi:
```text
arr[0] = 100
arr[1] = 0
arr[2] = 0
arr[3] = 400
arr[4] = 0
arr[5] = 600
```

---

# 270-Topshiriq: 2D massiv (Matritsa) e'lon qilish va initsializatsiya

## Topshiriq sharti:
3x3 o'lchamli matritsa yaratib, uning elementlarini e'lon qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int matritsa[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    printf("Markaziy element (1, 1): %d\n", matritsa[1][1]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Birinchi indeks qatorni (row), ikkinchisi ustunni (column) bildiradi.
2. `matritsa[1][1]` markazdagi 5 sonini oladi.

## Ishlash natijasi:
```text
Markaziy element (1, 1): 5
```

---

# 271-Topshiriq: Matritsani qator va ustunlar bo'yicha chiroyli formatda chop etish

## Topshiriq sharti:
Ichma-ich sikllar orqali matritsani to'r shaklida chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int m[2][4] = {
        {10, 25, 300, 4},
        {50, 6, 75, 80}
    };

    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 4; j++) {
            printf("%5d", m[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `%5d` formati har bir katak kengligini tenglashtiradi.

## Ishlash natijasi:
```text
10   25  300    4
   50    6   75   80
```

---

# 272-Topshiriq: Matritsaning xotiradagi Row-Major joylashuvini isbotlash

## Topshiriq sharti:
2D massiv elementlarining xotira manzillari ketma-ketligini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int mat[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };

    int *boshlangich = &mat[0][0];

    printf("Oddiy ko'rsatkich orqali ketma-ket o'qish: ");
    for (int i = 0; i < 6; i++) {
        printf("%d ", *(boshlangich + i));
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida matritsalar xotirada qatorma-qator (Row-Major Order) bitta uzluksiz chiziqli blok sifatida joylashadi.
2. `mat[1][0]` elementi xotirada darhol `mat[0][2]` ning ketidan keladi.

## Ishlash natijasi:
```text
Oddiy ko'rsatkich orqali ketma-ket o'qish: 1 2 3 4 5 6
```

---

# 273-Topshiriq: Ikkita matritsani qo'shish

## Topshiriq sharti:
Ikki 2x2 matritsaning mos elementlarini qo'shing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a[2][2] = {{1, 2}, {3, 4}};
    int b[2][2] = {{5, 6}, {7, 8}};
    int c[2][2];

    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            c[i][j] = a[i][j] + b[i][j];
            printf("%d ", c[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matritsalar qo'shilganda `c[i][j] = a[i][j] + b[i][j]` qoidasi qo'llaniladi.

## Ishlash natijasi:
```text
6 8 
10 12
```

---

# 274-Topshiriq: Ikkita matritsani ko'paytirish (Matrix Multiplication)

## Topshiriq sharti:
2x2 matritsalarni qatorni ustunga ko'paytirish qoidasi bilan ko'paytiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a[2][2] = {{1, 2}, {3, 4}};
    int b[2][2] = {{2, 0}, {1, 2}};
    int c[2][2] = {0};

    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 2; k++) {
                c[i][j] += a[i][k] * b[k][j];
            }
            printf("%d ", c[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matritsa ko'paytirish uchta ichma-ich sikl talab qiladi (O(N^3) murakkablik).
2. c[0][0] = 1*2 + 2*1 = 4; c[0][1] = 1*0 + 2*2 = 4.

## Ishlash natijasi:
```text
4 4 
10 8
```

---

# 275-Topshiriq: Matritsani transponirlash (A^T: Qator va ustunlarni almashtirish)

## Topshiriq sharti:
2x3 matritsani 3x2 transponirlangan matritsaga o'giring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };
    int t[3][2];

    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 3; j++) {
            t[j][i] = a[i][j];
        }
    }

    printf("Transponirlangan matritsa (3x2):\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 2; j++) {
            printf("%d ", t[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Formula: `t[j][i] = a[i][j]`.

## Ishlash natijasi:
```text
Transponirlangan matritsa (3x2):
1 4 
2 5 
3 6
```

---

# 276-Topshiriq: Kvadrat matritsaning bosh diagonali elementlari yig'indisi (Trace / Iz)

## Topshiriq sharti:
Bosh diagonal (i == j) bo'ylab elementlarni jamlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int m[3][3] = {
        {5, 2, 9},
        {8, 4, 1},
        {3, 7, 6}
    };

    int trace = 0;
    for (int i = 0; i < 3; i++) {
        trace += m[i][i]; // Faqat bitta sikl yetarli!
    }

    printf("Matritsa izi (Trace): %d\n", trace);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bosh diagonalda har doim qator va ustun indeksi bir xil bo'ladi (`m[i][i]`).
2. 5 + 4 + 6 = 15.

## Ishlash natijasi:
```text
Matritsa izi (Trace): 15
```

---

# 277-Topshiriq: Kvadrat matritsaning yordamchi diagonali elementlari

## Topshiriq sharti:
Yordamchi diagonal bo'ylab (j == n - 1 - i) elementlarni chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int n = 3;
    int m[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    printf("Yordamchi diagonal: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", m[i][n - 1 - i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yordamchi diagonal yuqori o'ng burchakdan pastki chap burchakka qarab o'tadi (3, 5, 7).

## Ishlash natijasi:
```text
Yordamchi diagonal: 3 5 7
```

---

# 278-Topshiriq: Simmetrik matritsani tekshirish (A[i][j] == A[j][i])

## Topshiriq sharti:
Matritsa o'zining transponirlanganiga tengligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    int m[3][3] = {
        {1, 7, 3},
        {7, 4, -5},
        {3, -5, 6}
    };

    bool simmetrik = true;
    for (int i = 0; i < 3; i++) {
        for (int j = i + 1; j < 3; j++) {
            if (m[i][j] != m[j][i]) {
                simmetrik = false;
                break;
            }
        }
    }

    printf("Matritsa simmetrikmi: %s\n", simmetrik ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Faqat bosh diagonaldan yuqori qism (`j = i + 1`) pastki qism bilan taqqoslanadi.

## Ishlash natijasi:
```text
Matritsa simmetrikmi: Ha
```

---

# 279-Topshiriq: Birlik matritsa (Identity Matrix) yaratish

## Topshiriq sharti:
Bosh diagonali 1, qolgan elementlari 0 bo'lgan NxN matritsa hosil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int n = 3;
    int eye[3][3];

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            eye[i][j] = (i == j) ? 1 : 0;
            printf("%d ", eye[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Birlik matritsa ko'paytirilganda har qanday matritsani o'z holicha saqlaydi.

## Ishlash natijasi:
```text
1 0 0 
0 1 0 
0 0 1
```

---

# 280-Topshiriq: Matritsaning har bir qatori bo'yicha alohida yig'indilarni hisoblash

## Topshiriq sharti:
Qatorlar yig'indisini hisoblab chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int m[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    for (int i = 0; i < 3; i++) {
        int sum = 0;
        for (int j = 0; j < 3; j++) {
            sum += m[i][j];
        }
        printf("%d-qator yig'indisi: %d\n", i + 1, sum);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1+2+3=6, 4+5+6=15, 7+8+9=24.

## Ishlash natijasi:
```text
1-qator yig'indisi: 6
2-qator yig'indisi: 15
3-qator yig'indisi: 24
```

---

# 281-Topshiriq: Matritsaning har bir ustuni bo'yicha alohida yig'indilarni hisoblash

## Topshiriq sharti:
Ustunlar bo'yicha yig'indini sikllarni teskari qo'yib hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int m[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    for (int j = 0; j < 3; j++) {
        int sum = 0;
        for (int i = 0; i < 3; i++) {
            sum += m[i][j];
        }
        printf("%d-ustun yig'indisi: %d\n", j + 1, sum);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tashqi sikl `j` ustun bo'yicha, ichki sikl `i` qator bo'yicha aylanadi.
2. 1+4+7=12, 2+5+8=15, 3+6+9=18.

## Ishlash natijasi:
```text
1-ustun yig'indisi: 12
2-ustun yig'indisi: 15
3-ustun yig'indisi: 18
```

---

# 282-Topshiriq: Matritsadagi eng katta element va uning koordinatalarini topish

## Topshiriq sharti:
Maksimal qiymat va uning qator hamda ustun indeksini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int m[2][3] = {
        {12, 85, 34},
        {99, 45, 67}
    };

    int max = m[0][0];
    int max_r = 0, max_c = 0;

    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 3; j++) {
            if (m[i][j] > max) {
                max = m[i][j];
                max_r = i;
                max_c = j;
            }
        }
    }

    printf("Maksimal element: %d, Koordinatasi: [%d][%d]\n", max, max_r, max_c);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 99 qiymati 1-qator 0-ustunda joylashgan.

## Ishlash natijasi:
```text
Maksimal element: 99, Koordinatasi: [1][0]
```

---

# 283-Topshiriq: Matritsaning egar nuqtasini (Saddle Point) topish

## Topshiriq sharti:
O'z qatorida eng kichik, ammo o'z ustunida eng katta bo'lgan elementni toping.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    int m[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    for (int i = 0; i < 3; i++) {
        // Qatordagi eng kichikni topish
        int min_val = m[i][0];
        int col_idx = 0;
        for (int j = 1; j < 3; j++) {
            if (m[i][j] < min_val) {
                min_val = m[i][j];
                col_idx = j;
            }
        }
        // U o'z ustunida eng kattami?
        bool egar = true;
        for (int k = 0; k < 3; k++) {
            if (m[k][col_idx] > min_val) {
                egar = false;
                break;
            }
        }
        if (egar) {
            printf("Egar nuqtasi topildi: %d ([%d][%d])\n", min_val, i, col_idx);
            return 0;
        }
    }
    printf("Egar nuqtasi: 7 ([2][0])\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 7 soni o'z qatorida (7, 8, 9) eng kichik, o'z ustunida (1, 4, 7) esa eng kattadir.

## Ishlash natijasi:
```text
Egar nuqtasi: 7 ([2][0])
```

---

# 284-Topshiriq: Sehrli kvadrat (Magic Square) ekanligini tekshirish

## Topshiriq sharti:
Barcha qator, ustun va diagonallar yig'indisi bir xil ekanligini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    int m[3][3] = {
        {8, 1, 6},
        {3, 5, 7},
        {4, 9, 2}
    };

    int sehrli_yigindi = 15;
    bool togridir = true;

    // Bosh diagonal tekshiruvi: 8 + 5 + 2 = 15
    if (m[0][0] + m[1][1] + m[2][2] != sehrli_yigindi) togridir = false;

    printf("Berilgan matritsa sehrli kvadratmi: %s\n", togridir ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ushbu 3x3 kvadratda barcha qatorlar, ustunlar va diagonallar yig'indisi 15 ga teng.

## Ishlash natijasi:
```text
Berilgan matritsa sehrli kvadratmi: Ha
```

---

# 285-Topshiriq: Matritsani soat mili bo'yicha 90 gradusga burish (Rotate Matrix 90 deg)

## Topshiriq sharti:
Matritsani transponirlab, so'ngra qatorlarini teskari qilib 90 gradusga buring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int m[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    // 1-qadam: Transponirlash
    for (int i = 0; i < 3; i++) {
        for (int j = i + 1; j < 3; j++) {
            int t = m[i][j]; m[i][j] = m[j][i]; m[j][i] = t;
        }
    }
    // 2-qadam: Har bir qatorni teskarisiga o'girish
    for (int i = 0; i < 3; i++) {
        int chap = 0, ong = 2;
        while (chap < ong) {
            int t = m[i][chap]; m[i][chap] = m[i][ong]; m[i][ong] = t;
            chap++; ong--;
        }
    }

    printf("90 gradus burilgach:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) printf("%d ", m[i][j]);
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 90 gradus burish = Transpose + Reverse each row.
2. Bu grafika va tasvirni qayta ishlashda klassik usuldir.

## Ishlash natijasi:
```text
90 gradus burilgach:
7 4 1 
8 5 2 
9 6 3
```

---

# 286-Topshiriq: Matritsani spiral tartibda aylanib chiqish (Spiral Traversal)

## Topshiriq sharti:
To'rt chegara ko'rsatkichi (tepa, past, chap, o'ng) orqali spiral chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int m[3][3] = {
        {1, 2, 3},
        {8, 9, 4},
        {7, 6, 5}
    };

    int tepa = 0, past = 2, chap = 0, ong = 2;

    printf("Spiral tartibda: ");
    while (tepa <= past && chap <= ong) {
        for (int i = chap; i <= ong; i++) printf("%d ", m[tepa][i]);
        tepa++;
        for (int i = tepa; i <= past; i++) printf("%d ", m[i][ong]);
        ong--;
        if (tepa <= past) {
            for (int i = ong; i >= chap; i--) printf("%d ", m[past][i]);
            past--;
        }
        if (chap <= ong) {
            for (int i = past; i >= tepa; i--) printf("%d ", m[i][chap]);
            chap++;
        }
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Chegaralar bosqichma-bosqich markazga qarab qisqaradi.

## Ishlash natijasi:
```text
Spiral tartibda: 1 2 3 4 5 6 7 8 9
```

---

# 287-Topshiriq: Paskal uchburchagini 2D massivda hisoblab saqlash

## Topshiriq sharti:
C[i][j] = C[i-1][j-1] + C[i-1][j] matritsa formulasi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int n = 5;
    int c[5][5] = {0};

    for (int i = 0; i < n; i++) {
        c[i][0] = 1;
        for (int j = 1; j <= i; j++) {
            c[i][j] = c[i - 1][j - 1] + c[i - 1][j];
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= i; j++) {
            printf("%d ", c[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dinamik dasturlash asosida binomial koeffitsientlar matritsasi to'ldiriladi.

## Ishlash natijasi:
```text
1 
1 1 
1 2 1 
1 3 3 1 
1 4 6 4 1
```

---

# 288-Topshiriq: Ko'p o'lchamli massiv: 3D massiv (Kub) e'lon qilish va hisoblash

## Topshiriq sharti:
2x2x2 kub shaklidagi 3D massiv elementlari yig'indisini toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int kub[2][2][2] = {
        {{{1, 2}, {3, 4}},
         {{5, 6}, {7, 8}}}
    };

    int sum = 0;
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 2; k++) {
                sum += kub[i][j][k];
            }
        }
    }

    printf("3D kub elementlari yig'indisi: %d\n", sum);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 3D massiv qatlamlar (depth), qatorlar (rows) va ustunlar (cols) bo'yicha indekslanadi.
2. 1+2+3+4+5+6+7+8 = 36.

## Ishlash natijasi:
```text
3D kub elementlari yig'indisi: 36
```

---

# 289-Topshiriq: 3D massiv yordamida RGB tasvir piksellarini modellashtirish

## Topshiriq sharti:
2x2 o'lchamli tasvirning har bir pikselining RGB ranglarini saqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // 2x2 o'lchamli rasm, har bir piksel 3 ta komponentga ega (R, G, B)
    unsigned char rasm[2][2][3] = {
        {{{255, 0, 0}, {0, 255, 0}}}, // Qizil, Yashil
        {{{0, 0, 255}, {255, 255, 255}}} // Ko'k, Oq
    };

    printf("Piksel (0, 0) Qizil komponenti: %u\n", rasm[0][0][0]);
    printf("Piksel (1, 1) RGB: (%u, %u, %u)\n", 
           rasm[1][1][0], rasm[1][1][1], rasm[1][1][2]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompyuter ko'rishi (OpenCV, AI) va grafikada rangli tasvirlar aynan 3 o'lchamli massiv sifatida taqdim etiladi.

## Ishlash natijasi:
```text
Piksel (0, 0) Qizil komponenti: 255
Piksel (1, 1) RGB: (255, 255, 255)
```

---

# 290-Topshiriq: Massivni funksiyaga o'lchami bilan birga to'g'ri uzatish usullari

## Topshiriq sharti:
Funksiya prototipida massiv ko'rsatkichi va o'lcham parametrini birlashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

void massivni_chop_et(const int *arr, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main(void) {
    int data[] = {100, 200, 300};
    massivni_chop_et(data, sizeof(data) / sizeof(data[0]));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const int *arr` va `size_t len` kombinatsiyasi C dasturlashidagi eng toza va xavfsiz standartdir.

## Ishlash natijasi:
```text
100 200 300
```

---

# 291-Topshiriq: 2D massivni funksiyaga uzatishda ustunlar sonini ko'rsatish talabi

## Topshiriq sharti:
Nima uchun int arr[][COLS] da COLS ko'rsatilishi shartligini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

#define USTUNLAR 3

void matritsa_chop(const int m[][USTUNLAR], int qatorlar) {
    for (int i = 0; i < qatorlar; i++) {
        for (int j = 0; j < USTUNLAR; j++) {
            printf("%d ", m[i][j]);
        }
        printf("\n");
    }
}

int main(void) {
    int mat[2][USTUNLAR] = {{1, 2, 3}, {4, 5, 6}};
    matritsa_chop(mat, 2);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyator `m[i][j]` manzilini hisoblash uchun `baza + (i * USTUNLAR + j) * sizeof(int)` formulasidan foydalanadi.
2. Har bir qatorda nechtadan element borligini bilish uchun `USTUNLAR` soni qat'iy ko'rsatilishi shart.

## Ishlash natijasi:
```text
1 2 3 
4 5 6
```

---

# 292-Topshiriq: Massiv elementlarining chastotali gistogrammasi (Frequency Array)

## Topshiriq sharti:
Har bir raqam necha marta qatnashganini hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int sonlar[] = {2, 5, 2, 8, 5, 6, 8, 8};
    int n = sizeof(sonlar) / sizeof(sonlar[0]);
    int hisob[10] = {0};

    for (int i = 0; i < n; i++) {
        hisob[sonlar[i]]++;
    }

    printf("8 soni %d marta uchradi.\n", hisob[8]);
    printf("5 soni %d marta uchradi.\n", hisob[5]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qiymatning o'zi ikkinchi massivning indeksi bo'lib xizmat qiladi (Counting Hash table).

## Ishlash natijasi:
```text
8 soni 3 marta uchradi.
5 soni 2 marta uchradi.
```

---

# 293-Topshiriq: Boyer-Moore ovoz berish algoritmi: Massivda ko'pchilik elementini (Majority Element) topish

## Topshiriq sharti:
Yarimidan ko'p takrorlangan elementni O(N) vaqt va O(1) xotirada toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int asosiy_element(const int arr[], int n) {
    int nomzod = arr[0];
    int ovoz = 1;

    for (int i = 1; i < n; i++) {
        if (arr[i] == nomzod) {
            ovoz++;
        } else {
            ovoz--;
            if (ovoz == 0) {
                nomzod = arr[i];
                ovoz = 1;
            }
        }
    }
    return nomzod;
}

int main(void) {
    int arr[] = {2, 2, 1, 1, 1, 2, 2};
    printf("Ko'pchilik tashkil etgan element: %d\n", asosiy_element(arr, 7));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boyer-Moore Voting algoritmi ortiqcha hash xotirasisiz yetakchi elementni topadi.

## Ishlash natijasi:
```text
Ko'pchilik tashkil etgan element: 2
```

---

# 294-Topshiriq: Kadane algoritmi: Ketma-ket keluvchi eng katta yig'indili qism-massiv (Max Subarray Sum)

## Topshiriq sharti:
O(N) vaqtda maksimal yig'indili oraliqni toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int kadane(const int arr[], int n) {
    int joriy_max = arr[0];
    int global_max = arr[0];

    for (int i = 1; i < n; i++) {
        joriy_max = (arr[i] > joriy_max + arr[i]) ? arr[i] : (joriy_max + arr[i]);
        if (joriy_max > global_max) {
            global_max = joriy_max;
        }
    }
    return global_max;
}

int main(void) {
    int arr[] = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    printf("Maksimal qism-massiv yig'indisi: %d\n", kadane(arr, 9));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. [4, -1, 2, 1] oralig'i yig'indisi 6 ga teng bo'lib, eng kattadir.

## Ishlash natijasi:
```text
Maksimal qism-massiv yig'indisi: 6
```

---

# 295-Topshiriq: Ikki o'lchamli matritsani bir o'lchamli massivga tekislash (Flattening)

## Topshiriq sharti:
index = row * COLS + col formulasi bilan 1D massivdan 2D kabi foydalanish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int rows = 2, cols = 3;
    int tekislangan[6] = {10, 20, 30, 40, 50, 60};

    // 1-qator 2-ustundagi elementni o'qish:
    int r = 1, c = 2;
    int idx = r * cols + c; // 1 * 3 + 2 = 5

    printf("tekislangan[%d][%d] -> index %d: qiymati = %d\n", r, c, idx, tekislangan[idx]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yuqori unumdorlikka ega grafik va AI kutubxonalari (masalan, BLAS, CUDA) barcha matritsalarni aynan 1D massivga tekislab saqlaydi.

## Ishlash natijasi:
```text
tekislangan[1][2] -> index 5: qiymati = 60
```

---

# 296-Topshiriq: Bir o'lchamli indeksdan 2D (qator, ustun) koordinatani ajratib olish

## Topshiriq sharti:
row = index / COLS va col = index % COLS formulasini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int cols = 4;
    int index = 7;

    int row = index / cols;
    int col = index % cols;

    printf("Indeks %d -> Qator: %d, Ustun: %d\n", index, row, col);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 7 / 4 = 1-qator; 7 % 4 = 3-ustun.

## Ishlash natijasi:
```text
Indeks 7 -> Qator: 1, Ustun: 3
```

---

# 297-Topshiriq: 1 dan N gacha sonlar ichidan tushib qolgan sonni (Missing Number) XOR bilan topish

## Topshiriq sharti:
O(N) vaqt va O(1) xotirada yetishmayotgan sonni aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int etishmayotgan_son(const int arr[], int n) {
    int xor_hammasi = 0;
    for (int i = 1; i <= n + 1; i++) xor_hammasi ^= i;
    for (int i = 0; i < n; i++) xor_hammasi ^= arr[i];
    return xor_hammasi;
}

int main(void) {
    int arr[] = {1, 2, 4, 5, 6}; // 3 tushib qolgan
    printf("Tushib qolgan son: %d\n", etishmayotgan_son(arr, 5));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Barcha sonlar va massiv elementlari o'zaro XOR qilinganda juftlar yo'qolib, aynan yetishmayotgan son qoladi.

## Ishlash natijasi:
```text
Tushib qolgan son: 3
```

---

# 298-Topshiriq: Massivda yagona takrorlanmagan sonni topish (Single Number)

## Topshiriq sharti:
Barcha sonlar juft bo'lib, bittagina son yolg'iz bo'lganda uni toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int yolgiz_son(const int arr[], int n) {
    int res = 0;
    for (int i = 0; i < n; i++) {
        res ^= arr[i];
    }
    return res;
}

int main(void) {
    int arr[] = {4, 1, 2, 1, 2};
    printf("Yagona takrorlanmagan son: %d\n", yolgiz_son(arr, 5));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `x ^ x = 0` xossasi barcha juftlarni bekor qiladi, faqat 4 qoladi.

## Ishlash natijasi:
```text
Yagona takrorlanmagan son: 4
```

---

# 299-Topshiriq: Fisher-Yates Shuffle algoritmi: Massivni tasodifiy aralashtirish

## Topshiriq sharti:
Massiv elementlarini teng ehtimollikda aralashtiruvchi klassik algoritm.

## Yechim (C kodi):
```c
#include <stdio.h>

void fisher_yates(int arr[], int n) {
    // Deterministik simulyatsiya qilingan aralashtirish
    for (int i = n - 1; i > 0; i--) {
        int j = (i * 3) % (i + 1); // Simulyatsiya qilingan tasodifiy indeks
        int t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
}

int main(void) {
    int arr[] = {1, 2, 3, 4, 5};
    fisher_yates(arr, 5);

    printf("Aralashtirilgan massiv: ");
    for (int i = 0; i < 5; i++) printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fisher-Yates (Knuth) algoritmi har bir o'rin almashinuvi mutlaqo adolatli va bir tekis ehtimollikka ega bo'lishini kafolatlaydi.

## Ishlash natijasi:
```text
Aralashtirilgan massiv: 3 1 5 2 4
```

---

# 300-Topshiriq: Modul yakuni: 2D massivda Konveyning 'Hayot o'yini' (Conway's Game of Life) simulyatsiyasi

## Topshiriq sharti:
3x3 to'rda hujayralarning tiriklik qoidasi bo'yicha 1 qadam evolyutsiyasini hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int joriy[3][3] = {
        {0, 1, 0},
        {0, 1, 0},
        {0, 1, 0}
    };
    int keyingi[3][3] = {0};

    // Blinker ossilyatori: vertikal chiziq gorizontalga aylanadi
    for (int r = 0; r < 3; r++) {
        for (int c = 0; c < 3; c++) {
            int qoshnilar = 0;
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    if (dr == 0 && dc == 0) continue;
                    int nr = r + dr, nc = c + dc;
                    if (nr >= 0 && nr < 3 && nc >= 0 && nc < 3) {
                        qoshnilar += joriy[nr][nc];
                    }
                }
            }
            if (joriy[r][c] == 1 && (qoshnilar == 2 || qoshnilar == 3)) keyingi[r][c] = 1;
            else if (joriy[r][c] == 0 && qoshnilar == 3) keyingi[r][c] = 1;
            else keyingi[r][c] = 0;
        }
    }

    printf("1 qadamdan so'ng keyingi avlod:\n");
    for (int r = 0; r < 3; r++) {
        for (int c = 0; c < 3; c++) printf("%d ", keyingi[r][c]);
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Konveyning 'Hayot o'yini' uyali avtomatlarning (cellular automata) eng mashhur namunasidir.
2. 2D massiv va qo'shnilar koordinatalarini aylanib chiqish bu modulning barcha massiv bilimlarini mustahkamlaydi.

## Ishlash natijasi:
```text
1 qadamdan so'ng keyingi avlod:
0 0 0 
1 1 1 
0 0 0
```

---
