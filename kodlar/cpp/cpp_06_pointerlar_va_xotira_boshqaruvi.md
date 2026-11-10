# C++ Dasturlash Tili - 6-Qism: Ko'rsatkichlar (Pointers) va Xotira Boshqaruvi

Ushbu qismda xotira manzillari, ko'rsatkichlar arifmetikasi, const pointerlar, void*, function pointerlar, dispatch table va past darajadagi xotira boshqaruviga oid 50 ta amaliy topshiriq jamlangan.

---

# 251-Topshiriq: Xotira manzili va manzil olish operatori (&)

## Topshiriq sharti:
O'zgaruvchining xotiradagi o'n oltilik (hexadecimal) manzilini ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int son = 42;
    std::cout << "O'zgaruvchi qiymati: " << son << std::endl;
    std::cout << "O'zgaruvchi manzili: " << &son << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `&` (address-of) operatori o'zgaruvchining operativ xotiradagi (RAM) boshlang'ich bayt manzilini qaytaradi.

## Ishlash natijasi:
```text
O'zgaruvchi qiymati: 42\nO'zgaruvchi manzili: 0x...
```

---

# 252-Topshiriq: Ko'rsatkich (Pointer) e'lon qilish va dereferensiya (*)

## Topshiriq sharti:
Ko'rsatkich o'zgaruvchisi orqali xotira katakchasidagi qiymatni o'qing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 100;
    int* ptr = &a; // ptr ga a ning manzili yuklandi
    std::cout << "ptr saqlayotgan manzil: " << ptr << std::endl;
    std::cout << "ptr ko'rsatayotgan qiymat (*ptr): " << *ptr << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `*ptr` (dereference) operatori ko'rsatkich saqlayotgan manzilga borib, u yerdagi qiymatni o'qiydi.

## Ishlash natijasi:
```text
ptr saqlayotgan manzil: 0x...\nptr ko'rsatayotgan qiymat (*ptr): 100
```

---

# 253-Topshiriq: Ko'rsatkich orqali qiymatni o'zgartirish

## Topshiriq sharti:
Ko'rsatkichga dereferensiya qilib o'zgaruvchining asl qiymatini o'zgartiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int x = 50;
    int* p = &x;
    *p = 500; // xotiradagi x qiymati to'g'ridan-to'g'ri o'zgardi
    std::cout << "x ning yangi qiymati: " << x << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `*p = 500` orqali `p` ko'rsatib turgan `x` o'zgaruvchisi 500 ga aylanadi.

## Ishlash natijasi:
```text
x ning yangi qiymati: 500
```

---

# 254-Topshiriq: Ko'rsatkich hajmi (sizeof pointer)

## Topshiriq sharti:
Har xil toifadagi (char, int, double) ko'rsatkichlarning xotiradagi hajmini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    char* cp;
    int* ip;
    double* dp;
    std::cout << "sizeof(char*): " << sizeof(cp) << " bayt" << std::endl;
    std::cout << "sizeof(int*): " << sizeof(ip) << " bayt" << std::endl;
    std::cout << "sizeof(double*): " << sizeof(dp) << " bayt" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 64-bitli arxitekturada barcha ko'rsatkichlar turi qanday bo'lishidan qat'i nazar aynan 8 bayt hajmga ega (32-bitda 4 bayt).

## Ishlash natijasi:
```text
sizeof(char*): 8 bayt\nsizeof(int*): 8 bayt\nsizeof(double*): 8 bayt
```

---

# 255-Topshiriq: nullptr bilan xavfsiz initsializatsiya

## Topshiriq sharti:
Hech qayerga ko'rsatmaydigan ko'rsatkichni C++11 ning `nullptr` bilan xavfsiz boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int* ptr = nullptr;
    if (ptr == nullptr) {
        std::cout << "Ko'rsatkich hozircha bo'sh (nullptr)." << std::endl;
    }
    int son = 77;
    ptr = &son;
    if (ptr != nullptr) {
        std::cout << "Ko'rsatkich qiymati: " << *ptr << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `nullptr` qat'iy tip xavfsizligiga ega bo'lib, eski `NULL` yoki `0` dan ko'ra ancha ishonchli.

## Ishlash natijasi:
```text
Ko'rsatkich hozircha bo'sh (nullptr).\nKo'rsatkich qiymati: 77
```

---

# 256-Topshiriq: Initsializatsiya qilinmagan (Wild) pointer xavfi

## Topshiriq sharti:
Boshlang'ich qiymat berilmagan ko'rsatkich tasodifiy manzilni ko'rsatishi va halokatga olib kelishi sababini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    // int* wildPtr; // Xavfli! Tasodifiy xotira manziliga ega bo'ladi
    int* safePtr = nullptr; // To'g'ri amaliyot
    std::cout << "Xavfsiz boshlang'ich holat: nullptr" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Doimo ko'rsatkichlarni darhol manzil bilan yoki `nullptr` bilan initsializatsiya qilish zarur.

## Ishlash natijasi:
```text
Xavfsiz boshlang'ich holat: nullptr
```

---

# 257-Topshiriq: Ko'rsatkichlar arifmetikasi: Qo'shish (ptr + 1)

## Topshiriq sharti:
`ptr + 1` qilinganda manzil 1 baytga emas, balki toifaning o'lchamiga (`sizeof(T)`) siljishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[3] = {10, 20, 30};
    int* p = arr;
    std::cout << "p manzili:      " << p << std::endl;
    std::cout << "p + 1 manzili:  " << (p + 1) << std::endl;
    std::cout << "Manzillar farqi: " << (char*)(p + 1) - (char*)p << " bayt" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int*` ga 1 qo'shilsa, manzil aniq `sizeof(int) = 4` baytga suriladi.

## Ishlash natijasi:
```text
p manzili:      0x...\np + 1 manzili:  0x...\nManzillar farqi: 4 bayt
```

---

# 258-Topshiriq: Ko'rsatkichlar arifmetikasi: Ayirish va ptrdiff_t

## Topshiriq sharti:
Bir massivdagi ikki ko'rsatkich ayirmasi ularning orasidagi elementlar sonini berishini namoyish qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstddef>

int main() {
    int arr[] = {1, 2, 3, 4, 5, 6};
    int* p1 = &arr[1];
    int* p4 = &arr[4];
    std::ptrdiff_t masofa = p4 - p1;
    std::cout << "p4 va p1 orasidagi elementlar soni: " << masofa << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikki ko'rsatkich ayirmasi `std::ptrdiff_t` toifasida bo'lib, elementlar sonini ifodalaydi.

## Ishlash natijasi:
```text
p4 va p1 orasidagi elementlar soni: 3
```

---

# 259-Topshiriq: Ko'rsatkich orqali massiv elementlarini o'qish

## Topshiriq sharti:
Tsiklda ko'rsatkichni oshirib borish orqali massiv elementlarini ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {11, 22, 33, 44, 55};
    int* ptr = arr;
    for (int i = 0; i < 5; ++i) {
        std::cout << *ptr << " ";
        ptr++;
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `*ptr` o'qiladi, so'ng `ptr++` keyingi element manziliga o'tadi.

## Ishlash natijasi:
```text
11 22 33 44 55
```

---

# 260-Topshiriq: Ko'rsatkich orqali massiv elementlarini o'zgartirish

## Topshiriq sharti:
Ko'rsatkich yordamida massivning har bir elementini 10 ga ko'paytiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {1, 2, 3, 4};
    int* p = arr;
    for (int i = 0; i < 4; ++i) {
        *p *= 10;
        p++;
    }
    for (int x : arr) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir qadamda dereferensiya qilib ko'paytirish bajariladi.

## Ishlash natijasi:
```text
10 20 30 40 
```

---

# 261-Topshiriq: *(arr + i) va arr[i] ekvivalentligi

## Topshiriq sharti:
C++ da indekslash amali aslida ko'rsatkichlar arifmetikasi ekanligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int sonlar[] = {7, 14, 21, 28};
    for (int i = 0; i < 4; ++i) {
        std::cout << "arr[" << i << "] = " << sonlar[i] 
                  << " | *(arr + " << i << ") = " << *(sonlar + i) << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sonlar[i]` ifodasi kompilyator tomonidan aynan `*(sonlar + i)` ga aylantiriladi.

## Ishlash natijasi:
```text
arr[0] = 7 | *(arr + 0) = 7\narr[1] = 14 | *(arr + 1) = 14\narr[2] = 21 | *(arr + 2) = 21\narr[3] = 28 | *(arr + 3) = 28
```

---

# 262-Topshiriq: Ko'rsatkichga ko'rsatkich (Pointer to Pointer: int**)

## Topshiriq sharti:
Ikki qavatli ko'rsatkich yaratib, o'zgaruvchi qiymatiga ikki marta dereferensiya qilib yetib boring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 777;
    int* p = &a;
    int** pp = &p;

    std::cout << "a = " << a << std::endl;
    std::cout << "*p = " << *p << std::endl;
    std::cout << "**pp = " << **pp << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `pp` ko'rsatkichning manzilini saqlaydi, `**pp` esa asl o'zgaruvchining qiymatini beradi.

## Ishlash natijasi:
```text
a = 777\n*p = 777\n**pp = 777
```

---

# 263-Topshiriq: Pointer to Pointer orqali dinamik 2D matritsa

## Topshiriq sharti:
Ko'rsatkichlar massivi orqali 2x2 jadvalni ifodalang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int row0[2] = {1, 2};
    int row1[2] = {3, 4};
    int* rows[2] = {row0, row1};
    int** mat = rows;

    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            std::cout << mat[i][j] << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `mat[i][j]` aslida `*(*(mat + i) + j)` amali hisoblanadi.

## Ishlash natijasi:
```text
1 2 \n3 4 
```

---

# 264-Topshiriq: const int* (Pointer to const)

## Topshiriq sharti:
Ko'rsatilayotgan ma'lumotni o'zgartirishni taqiqlovchi, ammo boshqa manzilga ko'rsata oluvchi ko'rsatkichni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int x = 10, y = 20;
    const int* ptr = &x;
    // *ptr = 15; // Kompilyatsiya xatosi: qiymatni o'zgartirib bo'lmaydi
    ptr = &y;     // To'g'ri: yangi manzilga o'tkazish mumkin
    std::cout << "Yangi manzil qiymati: " << *ptr << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const` toifadan oldin tursa, manzil ichidagi qiymat o'zgarmas (read-only) bo'ladi.

## Ishlash natijasi:
```text
Yangi manzil qiymati: 20
```

---

# 265-Topshiriq: int* const (Const pointer)

## Topshiriq sharti:
O'zgaruvchi qiymatini o'zgartirishga ruxsat beruvchi, ammo boshqa manzilga o'tishni taqiqlovchi ko'rsatkich tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 30, b = 40;
    int* const ptr = &a;
    *ptr = 35; // To'g'ri: qiymatni o'zgartirish mumkin
    // ptr = &b; // Kompilyatsiya xatosi: manzilni o'zgartirib bo'lmaydi
    std::cout << "a = " << a << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const` yulduzchadan keyin tursa, ko'rsatkichning o'zi o'zgarmas (doimiy manzil) bo'ladi.

## Ishlash natijasi:
```text
a = 35
```

---

# 266-Topshiriq: const int* const (Doimiy manzil va doimiy qiymat)

## Topshiriq sharti:
Ham manzili, ham qiymati qat'iy o'zgarmas bo'lgan ko'rsatkichni e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    const int x = 99;
    const int* const ptr = &x;
    std::cout << "Qiymat: " << *ptr << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Hech qanday tomondan o'zgartirib bo'lmaydigan to'liq xavfsiz ko'rsatkich.

## Ishlash natijasi:
```text
Qiymat: 99
```

---

# 267-Topshiriq: void* (Umumiy ko'rsatkich / Generic Pointer)

## Topshiriq sharti:
`void*` orqali turli toifadagi manzillarni saqlab, `static_cast` orqali kerakli turga o'giring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void chopEtSon(void* ptr, char tur) {
    if (tur == 'i') {
        std::cout << "Butun: " << *static_cast<int*>(ptr) << std::endl;
    } else if (tur == 'd') {
        std::cout << "Haqiqiy: " << *static_cast<double*>(ptr) << std::endl;
    }
}

int main() {
    int i = 123;
    double d = 4.56;
    chopEtSon(&i, 'i');
    chopEtSon(&d, 'd');
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `void*` har qanday ma'lumot manzilini saqlay oladi, ammo dereferensiya qilishdan oldin aniq turga aylantirilishi shart.

## Ishlash natijasi:
```text
Butun: 123\nHaqiqiy: 4.56
```

---

# 268-Topshiriq: const char* va satr literallari

## Topshiriq sharti:
Satr literali xotiraning read-only segmentida joylashishini va `const char*` orqali boshqarilishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    const char* shior = "Bilim - eng katta boylik";
    std::cout << shior << std::endl;
    std::cout << "Birinchi harf: " << *shior << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Satr literali o'zgarmas xotirada bo'lgani uchun zamonaviy C++ da faqat `const char*` ga bog'lanishi kerak.

## Ishlash natijasi:
```text
Bilim - eng katta boylik\nBirinchi harf: B
```

---

# 269-Topshiriq: Satr uzunligini ko'rsatkich bilan hisoblash (strlen)

## Topshiriq sharti:
Null-terminator `\0` gacha ko'rsatkichni surib, satr uzunligini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int satrUzunligi(const char* s) {
    const char* boshlanish = s;
    while (*s != '\0') {
        s++;
    }
    return s - boshlanish;
}

int main() {
    const char* matn = "O'zbekiston";
    std::cout << "Uzunligi: " << satrUzunligi(matn) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oxirgi manzil va boshlang'ich manzil ayirmasi belgilar sonini beradi.

## Ishlash natijasi:
```text
Uzunligi: 11
```

---

# 270-Topshiriq: Satrni ko'rsatkichlar bilan nusxalash (strcpy analogi)

## Topshiriq sharti:
Bir satrni boshqa buferga ko'rsatkichlar orqali ko'chirib o'tkazing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void satrNusxala(char* maqsad, const char* manba) {
    while (*manba != '\0') {
        *maqsad = *manba;
        maqsad++;
        manba++;
    }
    *maqsad = '\0'; // Yakuniy null-terminator
}

int main() {
    char bufer[50];
    satrNusxala(bufer, "Antigravity AI");
    std::cout << "Nusxa: " << bufer << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Manba belgisi manzilga ko'chiriladi va oxiriga `\0` qo'yiladi.

## Ishlash natijasi:
```text
Nusxa: Antigravity AI
```

---

# 271-Topshiriq: Satrni ko'rsatkichlar bilan teskarisiga o'girish

## Topshiriq sharti:
Ko'rsatkichlar juftligi (bosh va oxir) orqali char massivini joyida teskari qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstring>

void teskariQil(char* str) {
    char* chap = str;
    char* ong = str + strlen(str) - 1;
    while (chap < ong) {
        char temp = *chap;
        *chap = *ong;
        *ong = temp;
        chap++;
        ong--;
    }
}

int main() {
    char soz[] = "Dasturchi";
    teskariQil(soz);
    std::cout << "Teskari: " << soz << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkichlarni bir-biriga qarab yaqinlashtirib almashtiriladi.

## Ishlash natijasi:
```text
Teskari: ihcrutsaD
```

---

# 272-Topshiriq: Massivdagi eng katta element manzilini qaytarish

## Topshiriq sharti:
Massivning maksimal elementi ko'rsatkichini topuvchi funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int* maxElementManzili(int* arr, int n) {
    if (n <= 0) return nullptr;
    int* maxPtr = arr;
    for (int i = 1; i < n; ++i) {
        if (*(arr + i) > *maxPtr) {
            maxPtr = arr + i;
        }
    }
    return maxPtr;
}

int main() {
    int arr[] = {34, 12, 98, 45, 67};
    int* pMax = maxElementManzili(arr, 5);
    std::cout << "Maksimal qiymat: " << *pMax << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiya maksimal elementning o'ziga ko'rsatkich qaytaradi.

## Ishlash natijasi:
```text
Maksimal qiymat: 98
```

---

# 273-Topshiriq: Stack xotirasi manzilini qaytarish xatosi (Dangling Pointer)

## Topshiriq sharti:
Lokal (stek) o'zgaruvchi manzilini funksiyadan qaytarish xavfli ekanligini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

// int* xavfliFunksiya() {
//     int lokal = 42;
//     return &lokal; // XATOLIK! Funksiya tugashi bilan lokal o'zgaruvchi yo'q bo'ladi
// }

void xavfsizYondashuv(int& chiqish) {
    chiqish = 42;
}

int main() {
    int natija;
    xavfsizYondashuv(natija);
    std::cout << "Xavfsiz qiymat: " << natija << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Stek freymi yopilgach, lokal manzil bekor qilinadi. Bunday manzilga murojaat qilish halokatga olib keladi.

## Ishlash natijasi:
```text
Xavfsiz qiymat: 42
```

---

# 274-Topshiriq: Ko'rsatkichlar massivi (Array of Pointers)

## Topshiriq sharti:
Bir nechta satrlarning manzillarini ko'rsatkichlar massiviga to'plab chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    const char* tillar[4] = {"C++", "Python", "Rust", "Go"};
    for (int i = 0; i < 4; ++i) {
        std::cout << i + 1 << "-til: " << tillar[i] << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir element alohida satr xotirasiga ko'rsatkich hisoblanadi.

## Ishlash natijasi:
```text
1-til: C++\n2-til: Python\n3-til: Rust\n4-til: Go
```

---

# 275-Topshiriq: Massivga ko'rsatkich (Pointer to Array)

## Topshiriq sharti:
`int (*ptr)[3]` sintaksisi yordamida butun 3 elementli massivga ko'rsatkichni boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[3] = {10, 20, 30};
    int (*pArr)[3] = &arr;
    std::cout << "Birinchi element: " << (*pArr)[0] << std::endl;
    std::cout << "Ikkinchi element: " << (*pArr)[1] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int (*pArr)[3]` bitta elementga emas, balki 3 ta sondan iborat yaxlit massivga ko'rsatadi.

## Ishlash natijasi:
```text
Birinchi element: 10\nIkkinchi element: 20
```

---

# 276-Topshiriq: Ko'rsatkichlarni taqqoslash (ptr1 < ptr2)

## Topshiriq sharti:
Bitta massiv doirasida ko'rsatkichlar pozitsiyasini taqqoslashni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int massiv[5] = {1, 2, 3, 4, 5};
    int* pBosh = &massiv[0];
    int* pOxir = &massiv[4];
    if (pBosh < pOxir) {
        std::cout << "pBosh xotirada pOxir dan oldin joylashgan." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitta massiv doirasida manzil taqqoslash standart bo'yicha to'liq ruxsat etilgan.

## Ishlash natijasi:
```text
pBosh xotirada pOxir dan oldin joylashgan.
```

---

# 277-Topshiriq: Dispatch Table (Funksiya ko'rsatkichlari jadvali)

## Topshiriq sharti:
Funksiya ko'rsatkichlari massivi orqali buyruqlarni qabul qiluvchi dispatcher tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void buyruq0() { std::cout << "Boshlash" << std::endl; }
void buyruq1() { std::cout << "To'xtatish" << std::endl; }
void buyruq2() { std::cout << "Qayta yuklash" << std::endl; }

int main() {
    void (*jadval[3])() = {buyruq0, buyruq1, buyruq2};
    int buyruqId = 1;
    jadval[buyruqId](); // To'xtatish chaqiriladi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dispatch table `switch-case` siz O(1) vaqtda kerakli funksiyani tezkor chaqirish imkonini beradi.

## Ishlash natijasi:
```text
To'xtatish
```

---

# 278-Topshiriq: Kalkulyator amallarini funksiya ko'rsatkichi bilan boshqarish

## Topshiriq sharti:
Amal belgisiga qarab mos funksiyani ko'rsatkichga yuklab hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int qosh(int a, int b) { return a + b; }
int kopaytir(int a, int b) { return a * b; }

int main() {
    int (*amal)(int, int) = qosh;
    std::cout << "5 + 3 = " << amal(5, 3) << std::endl;
    amal = kopaytir;
    std::cout << "5 * 3 = " << amal(5, 3) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkich dinamik ravishda har xil amallarni ko'rsatishi mumkin.

## Ishlash natijasi:
```text
5 + 3 = 8\n5 * 3 = 15
```

---

# 279-Topshiriq: reinterpret_cast: Butun sonni baytlarga ajratish

## Topshiriq sharti:
32-bitli butun sonni xotirada joylashgan 4 ta alohida bayt ko'rinishida ko'rsatkich bilan o'qing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <iomanip>

int main() {
    unsigned int x = 0x12345678;
    unsigned char* baytlar = reinterpret_cast<unsigned char*>(&x);
    for (int i = 0; i < 4; ++i) {
        std::cout << "Bayt " << i << ": 0x" 
                  << std::hex << (int)baytlar[i] << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `reinterpret_cast` xotirani past darajadagi xom baytlar sifatida talqin qilish imkonini beradi.

## Ishlash natijasi:
```text
Bayt 0: 0x78\nBayt 1: 0x56\nBayt 2: 0x34\nBayt 3: 0x12
```

---

# 280-Topshiriq: Endianness (Little-Endian vs Big-Endian) aniqlash

## Topshiriq sharti:
Tizim xotirasida sonlar Little-Endian tartibida saqlanishini ko'rsatkich bilan tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    unsigned int test = 1;
    char* c = (char*)&test;
    if (*c == 1) {
        std::cout << "Tizim arxitekturasi: Little-Endian (Intel/AMD/ARM standart)" << std::endl;
    } else {
        std::cout << "Tizim arxitekturasi: Big-Endian" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Eng kichik manzilga eng kichik bayt yozilsa, tizim Little-Endian hisoblanadi.

## Ishlash natijasi:
```text
Tizim arxitekturasi: Little-Endian (Intel/AMD/ARM standart)
```

---

# 281-Topshiriq: Xotirani to'ldirish (memset analogi)

## Topshiriq sharti:
Ko'rsatkich orqali massivning har bir baytini nolga tenglashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void xotiraniNolla(void* ptr, size_t baytlar) {
    char* p = static_cast<char*>(ptr);
    for (size_t i = 0; i < baytlar; ++i) {
        p[i] = 0;
    }
}

int main() {
    int arr[3] = {111, 222, 333};
    xotiraniNolla(arr, sizeof(arr));
    std::cout << arr[0] << " " << arr[1] << " " << arr[2] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Baytma-bayt xotira xavfsiz tarzda tozalanadi.

## Ishlash natijasi:
```text
0 0 0
```

---

# 282-Topshiriq: Xotiradan nusxa olish (memcpy analogi)

## Topshiriq sharti:
Ko'rsatkichlar orqali bir xotira blokini boshqasiga baytma-bayt nusxalang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void xotiraNusxa(void* maqsad, const void* manba, size_t baytlar) {
    char* d = static_cast<char*>(maqsad);
    const char* s = static_cast<const char*>(manba);
    for (size_t i = 0; i < baytlar; ++i) {
        d[i] = s[i];
    }
}

int main() {
    int asil[3] = {10, 20, 30};
    int nusxa[3];
    xotiraNusxa(nusxa, asil, sizeof(asil));
    std::cout << nusxa[0] << " " << nusxa[1] << " " << nusxa[2] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har qanday obyektning xotira baytlari ko'chiriladi.

## Ishlash natijasi:
```text
10 20 30
```

---

# 283-Topshiriq: Xotira ustma-ust tushishi (Overlapping memory va memmove)

## Topshiriq sharti:
Bir massiv ichida siljitishda ma'lumotlar buzilmasligi uchun teskari yo'nalishda ko'chirish zaruratini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void xavfsizSurish(char* str, int surish, int n) {
    for (int i = n - 1; i >= 0; --i) {
        str[i + surish] = str[i];
    }
}

int main() {
    char buf[10] = "ABC";
    xavfsizSurish(buf, 2, 4); // "ABC " ni 2 qadam o'ngga surish
    std::cout << "Surilgan: " << (buf + 2) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xotira bloklari bir-biriga kelsa, oxiridan ko'chirish ma'lumotlarni yo'qolishdan asraydi.

## Ishlash natijasi:
```text
Surilgan: ABC
```

---

# 284-Topshiriq: Ko'rsatkichlar oralig'ida qidiruv

## Topshiriq sharti:
Boshlang'ich va oxirgi ko'rsatkichlar oralig'ida qiymat qidiruvchi funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

const int* qidir(const int* bosh, const int* oxir, int qiymat) {
    while (bosh != oxir) {
        if (*bosh == qiymat) return bosh;
        bosh++;
    }
    return oxir; // Topilmasa oxirgi ko'rsatkich
}

int main() {
    int arr[] = {4, 7, 12, 19, 25};
    const int* res = qidir(arr, arr + 5, 12);
    if (res != arr + 5) {
        std::cout << "Topildi: " << *res << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu aynan STL iteratorlari konsepsiyasining ko'rsatkichlardagi asosi hisoblanadi.

## Ishlash natijasi:
```text
Topildi: 12
```

---

# 285-Topshiriq: Reference va Pointer farqlari

## Topshiriq sharti:
Reference doimiy bog'langanligi va nullptr bo'la olmasligi, pointer esa moslashuvchanligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 10, b = 20;
    int& ref = a; // Doim a ga bog'liq
    ref = b;      // a ning qiymati 20 ga aylandi, ref b ga o'tmadi!
    std::cout << "a = " << a << ", b = " << b << std::endl;

    int* ptr = &a;
    ptr = &b;     // ptr endi b ning manziliga ko'rsatadi
    std::cout << "*ptr = " << *ptr << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Reference boshqa o'zgaruvchiga qayta bog'lana olmaydi, pointer esa boshqa manzilga yo'naltirilishi mumkin.

## Ishlash natijasi:
```text
a = 20, b = 20\n*ptr = 20
```

---

# 286-Topshiriq: Ko'rsatkichga havola (Reference to Pointer: int*&)

## Topshiriq sharti:
Funksiya orqali ko'rsatkich saqlayotgan manzilning o'zini o'zgartirish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int globalX = 999;

void manzilniAlmashtir(int*& p) {
    p = &globalX;
}

int main() {
    int lokal = 10;
    int* ptr = &lokal;
    manzilniAlmashtir(ptr);
    std::cout << "*ptr = " << *ptr << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int*&` ko'rsatkichning o'ziga havola bo'lib, uning manzilini funksiya ichida o'zgartirish imkonini beradi.

## Ishlash natijasi:
```text
*ptr = 999
```

---

# 287-Topshiriq: Dangling Pointer va uni nullptr ga tenglashtirish

## Topshiriq sharti:
Manzil yaroqsiz bo'lgach ko'rsatkichni nullptr qilish zarurati.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int* ptr = nullptr;
    {
        int temp = 55;
        ptr = &temp;
    } // temp o'zgaruvchisi bu yerda yo'q qilindi
    ptr = nullptr; // Endi xavfsiz, osilib qolgan (dangling) bo'lmaydi
    std::cout << "Ko'rsatkich xavfsizlantirildi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yaroqsiz bo'lgan ko'rsatkichni `nullptr` ga aylantirish xatoliklardan himoya qiladi.

## Ishlash natijasi:
```text
Ko'rsatkich xavfsizlantirildi.
```

---

# 288-Topshiriq: Xotira tekislanishi (Memory Alignment)

## Topshiriq sharti:
`alignof` orqali toifalarning xotirada necha bayt karrali joylashishini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "int alignment: " << alignof(int) << " bayt" << std::endl;
    std::cout << "double alignment: " << alignof(double) << " bayt" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zamonaviy protsessorlar xotirani o'z karraligi bo'yicha tezroq o'qiydi (Data Alignment).

## Ishlash natijasi:
```text
int alignment: 4 bayt\ndouble alignment: 8 bayt
```

---

# 289-Topshiriq: Strukturaga ko'rsatkich va -> operatori

## Topshiriq sharti:
Struktura manzilini ko'rsatkichda saqlab `->` (arrow operator) orqali a'zolariga murojaat qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Nuqta {
    int x;
    int y;
};

int main() {
    Nuqta n1 = {15, 25};
    Nuqta* pN = &n1;
    std::cout << "x = " << pN->x << ", y = " << pN->y << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `pN->x` ifodasi `(*pN).x` ning qulay va o'qishli qisqartmasidir.

## Ishlash natijasi:
```text
x = 15, y = 25
```

---

# 290-Topshiriq: Strukturalar massivini ko'rsatkich orqali aylanib chiqish

## Topshiriq sharti:
Ko'rsatkich yordamida strukturalar ketma-ketligini o'qing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Talaba {
    int id;
    int ball;
};

int main() {
    Talaba guruh[3] = {{1, 85}, {2, 92}, {3, 78}};
    Talaba* p = guruh;
    for (int i = 0; i < 3; ++i) {
        std::cout << "ID: " << p->id << " | Ball: " << p->ball << std::endl;
        p++;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkich har qadamda `sizeof(Talaba)` baytga siljiydi.

## Ishlash natijasi:
```text
ID: 1 | Ball: 85\nID: 2 | Ball: 92\nID: 3 | Ball: 78
```

---

# 291-Topshiriq: O'z-o'ziga havola qiluvchi struktura (Tugun / Node)

## Topshiriq sharti:
Keyingi tugun manzilini saqlovchi sodda `Node` tuzilmasini e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Tugun {
    int qiymat;
    Tugun* keyingi;
};

int main() {
    Tugun t1 = {10, nullptr};
    std::cout << "Tugun qiymati: " << t1.qiymat << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'z turiga ko'rsatkich saqlash bog'langan ro'yxatlar (Linked List) va daraxtlarning poydevoridir.

## Ishlash natijasi:
```text
Tugun qiymati: 10
```

---

# 292-Topshiriq: Ikki tugunni bog'lash (Linked List boshlanishi)

## Topshiriq sharti:
Ikki tugunni ko'rsatkich orqali ketma-ket bog'lang va birinchisi orqali ikkinchisini o'qing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Node {
    int data;
    Node* next;
};

int main() {
    Node n2 = {200, nullptr};
    Node n1 = {100, &n2};

    std::cout << "Birinchi: " << n1.data << std::endl;
    std::cout << "Ikkinchi: " << n1.next->data << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `n1.next->data` orqali zanjir bo'ylab keyingi obyektga o'tiladi.

## Ishlash natijasi:
```text
Birinchi: 100\nIkkinchi: 200
```

---

# 293-Topshiriq: Ko'rsatkichlar bilan bitlar to'plamini (bitmask) o'qish

## Topshiriq sharti:
Ko'rsatkich orqali xotiraning alohida bitlarini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    unsigned char bayt = 0b00101000;
    unsigned char* p = &bayt;
    bool uchinchiBit = (*p & (1 << 3)) != 0;
    std::cout << "3-bit yoniqmi: " << (uchinchiBit ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkich orqali apparat registrlari va bit niqoblarini boshqarish mumkin.

## Ishlash natijasi:
```text
3-bit yoniqmi: Ha
```

---

# 294-Topshiriq: Float sonining IEEE 754 bitlarini ko'rsatkich bilan ko'rish

## Topshiriq sharti:
float sonining 32 ta bitini `uint32_t*` ko'rsatkich orqali o'qing (Type punning).

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>

int main() {
    float f = 1.0f;
    uint32_t* p = reinterpret_cast<uint32_t*>(&f);
    std::cout << "1.0f ning IEEE 754 hex kodi: 0x" << std::hex << *p << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1.0f sonining IEEE 754 shakli `0x3f800000` ga teng.

## Ishlash natijasi:
```text
1.0f ning IEEE 754 hex kodi: 0x3f800000
```

---

# 295-Topshiriq: Satrdan belgi qidiruvchi ko'rsatkich (strchr analogi)

## Topshiriq sharti:
Satr ichidan berilgan belgining birinchi uchragan joyiga ko'rsatkich qaytaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

const char* belgiTop(const char* str, char c) {
    while (*str != '\0') {
        if (*str == c) return str;
        str++;
    }
    return nullptr;
}

int main() {
    const char* matn = "Antigravity";
    const char* ptr = belgiTop(matn, 'g');
    if (ptr != nullptr) {
        std::cout << "'g' dan keyingi qism: " << ptr << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Belgining manzilini topib, undan keyingi matn ko'rsatkich orqali chiqariladi.

## Ishlash natijasi:
```text
'g' dan keyingi qism: gravity
```

---

# 296-Topshiriq: Satrlarni ko'rsatkich bilan taqqoslash (strcmp analogi)

## Topshiriq sharti:
Ikki satrni ko'rsatkichlar yordamida belgi-ba-belgi solishtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int satrSolishtir(const char* s1, const char* s2) {
    while (*s1 && (*s1 == *s2)) {
        s1++;
        s2++;
    }
    return *(const unsigned char*)s1 - *(const unsigned char*)s2;
}

int main() {
    std::cout << satrSolishtir("olma", "olma") << " (teng)\n";
    std::cout << (satrSolishtir("anor", "olma") < 0 ? "anor kichik" : "") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Birinchi farqli belgilar kodi ayirmasi qaytariladi.

## Ishlash natijasi:
```text
0 (teng)\nanor kichik
```

---

# 297-Topshiriq: Ko'rsatkichlar oralig'i (Pointer Range)

## Topshiriq sharti:
Boshlanish va tugash ko'rsatkichlari yordamida massiv qismini chop etuvchi funksiya.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void chopEtOraliq(const int* begin, const int* end) {
    for (const int* it = begin; it != end; ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;
}

int main() {
    int arr[] = {10, 20, 30, 40, 50, 60};
    chopEtOraliq(arr + 1, arr + 4); // 20, 30, 40
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `[begin, end)` yarim ochiq oralig'i zamonaviy C++ da asosiy standartdir.

## Ishlash natijasi:
```text
20 30 40 
```

---

# 298-Topshiriq: Massiv o'rtasidagi elementga ko'rsatkich

## Topshiriq sharti:
Ko'rsatkichlar arifmetikasi orqali massiv markaziy elementini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {100, 200, 300, 400, 500};
    int* pBosh = arr;
    int* pOxir = arr + 5;
    int* pOrta = pBosh + (pOxir - pBosh) / 2;
    std::cout << "Markaziy element: " << *pOrta << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikkilik qidiruvda ko'rsatkichlar bilan o'rta nuqta aynan shunday hisoblanadi.

## Ishlash natijasi:
```text
Markaziy element: 300
```

---

# 299-Topshiriq: Ko'rsatkich xavfsizligi va Memory Sanitizers

## Topshiriq sharti:
AddressSanitizer (ASan) ko'rsatkichlar xatosini (Use-after-free, Buffer Overflow) qanday aniqlashini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "AddressSanitizer (ASan) - C++ da xotira xatolarini "
              << "ish vaqtida tutuvchi kuchli vosita." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ASan kompilyatsiya vaqtida xotira chegaralari va holatini tekshiruvchi qo'riqchi (shadow memory) qo'shadi.

## Ishlash natijasi:
```text
AddressSanitizer (ASan) - C++ da xotira xatolarini ish vaqtida tutuvchi kuchli vosita.
```

---

# 300-Topshiriq: Pointerlar va zamonaviy C++ falsafasi xulosasi

## Topshiriq sharti:
Xom ko'rsatkichlar (raw pointers) mulkdorlikka (ownership) ega bo'lmasligi, faqat kuzatuvchi sifatida ishlatilishi kerakligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void kuzat(const int* ptr) {
    if (ptr) {
        std::cout << "Kuzatilayotgan qiymat: " << *ptr << std::endl;
    }
}

int main() {
    int son = 1234;
    kuzat(&son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zamonaviy C++ da xom ko'rsatkichlar xotirani o'chirish uchun emas, faqat o'qish va kuzatish uchun tavsiya etiladi.

## Ishlash natijasi:
```text
Kuzatilayotgan qiymat: 1234
```

---

