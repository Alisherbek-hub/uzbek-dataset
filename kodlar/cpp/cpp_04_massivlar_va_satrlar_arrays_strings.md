# C++ Dasturlash Tili - 4-Qism: Massivlar va Satrlar (Arrays and Strings)

Ushbu qismda C++ tilida 1D/2D/3D massivlar, matritsalar, std::array, C-string, std::string va C++17 std::string_view imkoniyatlariga oid 50 ta amaliy topshiriq jamlangan.

---

# 151-Topshiriq: 1D Statik massiv e'lon qilish va elementlarga murojaat

## Topshiriq sharti:
5 ta butun sondan iborat massiv e'lon qiling, elementlariga indeks orqali murojaat qilib ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int sonlar[5] = {12, 25, 33, 47, 59};
    for (int i = 0; i < 5; ++i) {
        std::cout << "Indeks [" << i << "] = " << sonlar[i] << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++ da massiv indekslari 0 dan boshlanadi. Massiv xotirada ketma-ket bitta xotira blokida joylashadi.

## Ishlash natijasi:
```text
Indeks [0] = 12\nIndeks [1] = 25\nIndeks [2] = 33\nIndeks [3] = 47\nIndeks [4] = 59
```

---

# 152-Topshiriq: Massiv yig'indisi va o'rtacha arifmetigi

## Topshiriq sharti:
Massiv elementlarining yig'indisi va o'rtacha arifmetik qiymatini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int n = sizeof(arr) / sizeof(arr[0]);
    int yigindi = 0;
    for (int i = 0; i < n; ++i) {
        yigindi += arr[i];
    }
    double ortacha = (double)yigindi / n;
    std::cout << "Yig'indi: " << yigindi << std::endl;
    std::cout << "O'rtacha qiymat: " << ortacha << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sizeof(arr) / sizeof(arr[0])` statik massivdagi elementlar sonini hisoblash usuli.

## Ishlash natijasi:
```text
Yig'indi: 150\nO'rtacha qiymat: 30
```

---

# 153-Topshiriq: Massivdagi eng katta va eng kichik elementlar

## Topshiriq sharti:
Massiv ichidagi eng maksimal va minimal qiymatlarni bitta tsiklda toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {45, 12, 89, 3, 67, 92, 24};
    int n = sizeof(arr) / sizeof(arr[0]);
    int min_val = arr[0], max_val = arr[0];
    for (int i = 1; i < n; ++i) {
        if (arr[i] < min_val) min_val = arr[i];
        if (arr[i] > max_val) max_val = arr[i];
    }
    std::cout << "Minimal element: " << min_val << std::endl;
    std::cout << "Maksimal element: " << max_val << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bir martalik O(n) o'tish bilan ikkala ekstremal qiymat aniqlanadi.

## Ishlash natijasi:
```text
Minimal element: 3\nMaksimal element: 92
```

---

# 154-Topshiriq: Massiv elementlarini teskari tartibda joylashtirish (In-place reverse)

## Topshiriq sharti:
Qo'shimcha massiv ochmasdan (in-place) massiv elementlari o'rnini teskarisiga almashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {1, 2, 3, 4, 5, 6};
    int n = sizeof(arr) / sizeof(arr[0]);
    int chap = 0, ong = n - 1;
    while (chap < ong) {
        int temp = arr[chap];
        arr[chap] = arr[ong];
        arr[ong] = temp;
        chap++;
        ong--;
    }
    for (int i = 0; i < n; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikki ko'rsatkich (Two-pointer) texnikasi orqali massiv xotira sarflamasdan teskari o'giriladi.

## Ishlash natijasi:
```text
6 5 4 3 2 1
```

---

# 155-Topshiriq: Massivni o'ngga 1 ta pozitsiyaga siklik siljitish

## Topshiriq sharti:
Massivning har bir elementini 1 qadam o'ngga suring, oxirgi element esa boshiga kelsin.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int n = sizeof(arr) / sizeof(arr[0]);
    int oxirgi = arr[n - 1];
    for (int i = n - 1; i > 0; --i) {
        arr[i] = arr[i - 1];
    }
    arr[0] = oxirgi;

    for (int i = 0; i < n; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oxirgi element saqlab olinadi, qolgan elementlar orqadan oldinga qarab o'ngga siljitiladi.

## Ishlash natijasi:
```text
50 10 20 30 40
```

---

# 156-Topshiriq: Chiziqli qidiruv (Linear Search)

## Topshiriq sharti:
Massiv ichidan berilgan qiymat qaysi indeksda joylashganini chiziqli qidiruv bilan toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {15, 23, 8, 42, 16, 4};
    int n = sizeof(arr) / sizeof(arr[0]);
    int kalit = 42;
    int indeks = -1;
    for (int i = 0; i < n; ++i) {
        if (arr[i] == kalit) {
            indeks = i;
            break;
        }
    }
    if (indeks != -1) {
        std::cout << kalit << " soni " << indeks << "-indeksda topildi." << std::endl;
    } else {
        std::cout << "Topilmadi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Chiziqli qidiruv O(n) vaqt oladi va saralanmagan massivlarda ishlaydi.

## Ishlash natijasi:
```text
42 soni 3-indeksda topildi.
```

---

# 157-Topshiriq: Ikkilik qidiruv (Binary Search)

## Topshiriq sharti:
Saralangan massivda elementni O(log n) vaqtda ikkilik qidiruv orqali toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {3, 9, 14, 21, 35, 48, 62, 77, 90};
    int n = sizeof(arr) / sizeof(arr[0]);
    int qidirilayotgan = 48;
    int chap = 0, ong = n - 1, natija = -1;

    while (chap <= ong) {
        int orta = chap + (ong - chap) / 2;
        if (arr[orta] == qidirilayotgan) {
            natija = orta;
            break;
        }
        if (arr[orta] < qidirilayotgan) {
            chap = orta + 1;
        } else {
            ong = orta - 1;
        }
    }
    std::cout << qidirilayotgan << " indeksi: " << natija << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir taqqoslashda qidiruv maydoni ikki barobar qisqaradi.

## Ishlash natijasi:
```text
48 indeksi: 5
```

---

# 158-Topshiriq: Massivdagi juft va toq elementlarni sanash

## Topshiriq sharti:
Massivdagi nechta element juft va nechta element toq ekanligini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {12, 17, 24, 39, 40, 55, 68, 71};
    int juft = 0, toq = 0;
    for (int x : arr) {
        if (x % 2 == 0) juft++;
        else toq++;
    }
    std::cout << "Juft sonlar: " << juft << " ta\nToq sonlar: " << toq << " ta" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `x % 2 == 0` sharti orqali elementlar guruhlanadi.

## Ishlash natijasi:
```text
Juft sonlar: 4 ta\nToq sonlar: 4 ta
```

---

# 159-Topshiriq: Massivdagi takroriy elementlarni aniqlash

## Topshiriq sharti:
Massivda kamida ikki marta qatnashgan elementlarni ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {2, 5, 8, 2, 9, 5, 3};
    int n = sizeof(arr) / sizeof(arr[0]);
    std::cout << "Takrorlanganlar: ";
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (arr[i] == arr[j]) {
                std::cout << arr[i] << " ";
                break;
            }
        }
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ichma-ich tsikl har bir elementni o'zidan keyingi elementlar bilan solishtiradi.

## Ishlash natijasi:
```text
Takrorlanganlar: 2 5 
```

---

# 160-Topshiriq: Massivdagi faqat bir marta uchragan (noyob) element

## Topshiriq sharti:
Barcha elementlar juft (2 marta) uchragan va faqat bitta element 1 marta qatnashgan massivdan o'sha yolg'iz elementni XOR yordamida O(n) vaqtda toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {7, 3, 5, 3, 7, 9, 5};
    int n = sizeof(arr) / sizeof(arr[0]);
    int yolgiz = 0;
    for (int i = 0; i < n; ++i) {
        yolgiz ^= arr[i];
    }
    std::cout << "Faqat bir marta qatnashgan element: " << yolgiz << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `x ^ x = 0` va `x ^ 0 = x` xossasi sababli barcha takrorlangan sonlar bir-birini bekor qiladi va faqat yolg'iz son qoladi.

## Ishlash natijasi:
```text
Faqat bir marta qatnashgan element: 9
```

---

# 161-Topshiriq: 2D Massiv (Matritsa) e'lon qilish va chiqarish

## Topshiriq sharti:
3x3 o'lchamli butun sonlar matritsasini e'lon qiling va jadval ko'rinishida chop eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int mat[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            std::cout << mat[i][j] << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `mat[i][j]` - i qator, j ustundagi elementga kirish.

## Ishlash natijasi:
```text
1 2 3 \n4 5 6 \n7 8 9 
```

---

# 162-Topshiriq: Matritsaning bosh diagonali yig'indisi

## Topshiriq sharti:
Kvadrat matritsaning bosh diagonali (i == j bo'lgan) elementlari yig'indisini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int mat[3][3] = {
        {10, 2, 3},
        {4, 20, 6},
        {7, 8, 30}
    };
    int sum = 0;
    for (int i = 0; i < 3; ++i) {
        sum += mat[i][i];
    }
    std::cout << "Bosh diagonal yig'indisi: " << sum << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bosh diagonaldagi elementlar `mat[i][i]` ko'rinishida bo'lgani uchun bitta tsikl kifoya.

## Ishlash natijasi:
```text
Bosh diagonal yig'indisi: 60
```

---

# 163-Topshiriq: Matritsaning yordamchi diagonali yig'indisi

## Topshiriq sharti:
Kvadrat matritsaning yordamchi diagonali (`j == n - 1 - i`) elementlari yig'indisini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int mat[3][3] = {
        {1, 2, 5},
        {4, 7, 6},
        {9, 8, 2}
    };
    int sum = 0;
    for (int i = 0; i < 3; ++i) {
        sum += mat[i][3 - 1 - i];
    }
    std::cout << "Yordamchi diagonal yig'indisi: " << sum << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yordamchi diagonal elementlari: mat[0][2], mat[1][1], mat[2][0]. 5 + 7 + 9 = 21.

## Ishlash natijasi:
```text
Yordamchi diagonal yig'indisi: 21
```

---

# 164-Topshiriq: Matritsani transponirlash (Transpose)

## Topshiriq sharti:
2x3 o'lchamli matritsani transponirlab 3x2 o'lchamli yangi matritsaga o'giring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int A[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };
    int T[3][2];
    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 3; ++j) {
            T[j][i] = A[i][j];
        }
    }
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 2; ++j) {
            std::cout << T[i][j] << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Transponirlashda satrlar ustunlarga aylanadi: `T[j][i] = A[i][j]`.

## Ishlash natijasi:
```text
1 4 \n2 5 \n3 6 
```

---

# 165-Topshiriq: Ikki matritsani qo'shish

## Topshiriq sharti:
Bir xil 2x2 o'lchamdagi ikkita matritsani mos elementlari bo'yicha qo'shing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int A[2][2] = {{1, 3}, {5, 7}};
    int B[2][2] = {{2, 4}, {6, 8}};
    int C[2][2];
    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            C[i][j] = A[i][j] + B[i][j];
            std::cout << C[i][j] << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir element `C[i][j] = A[i][j] + B[i][j]` ko'rinishida qo'shiladi.

## Ishlash natijasi:
```text
3 7 \n11 15 
```

---

# 166-Topshiriq: Matritsalarni ko'paytirish (Matrix Multiplication)

## Topshiriq sharti:
2x2 o'lchamli ikkita matritsani o'zaro ko'paytiring (C = A * B).

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int A[2][2] = {{1, 2}, {3, 4}};
    int B[2][2] = {{2, 0}, {1, 2}};
    int C[2][2] = {0};

    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            for (int k = 0; k < 2; ++k) {
                C[i][j] += A[i][k] * B[k][j];
            }
            std::cout << C[i][j] << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matritsalar ko'paytmasi uch qavatli tsikl orqali har bir satr va ustun skalyar ko'paytmasidan tashkil topadi.

## Ishlash natijasi:
```text
4 4 \n10 8 
```

---

# 167-Topshiriq: std::array konteyneri (C++11)

## Topshiriq sharti:
Standart kutubxonadagi xavfsiz va qulay `std::array` konteyneridan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <array>

int main() {
    std::array<int, 4> arr = {10, 20, 30, 40};
    for (int x : arr) {
        std::cout << x << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::array` oddiy massiv tezligiga ega bo'lib, STL konteynerlari interfeysi va xavfsizligini taqdim etadi.

## Ishlash natijasi:
```text
10 20 30 40
```

---

# 168-Topshiriq: std::array: front(), back(), size(), at()

## Topshiriq sharti:
std::array konteynerining xavfsiz `.at()` va chetki elementlarga murojaat metodlarini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <array>

int main() {
    std::array<int, 4> a = {5, 10, 15, 20};
    std::cout << "Hajmi: " << a.size() << std::endl;
    std::cout << "Birinchi: " << a.front() << std::endl;
    std::cout << "Oxirgi: " << a.back() << std::endl;
    std::cout << "2-indeks: " << a.at(2) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.at()` metodi chegaradan chiqib ketishni tekshiradi va xato bo'lsa `std::out_of_range` istisnosini tashlaydi.

## Ishlash natijasi:
```text
Hajmi: 4\nBirinchi: 5\nOxirgi: 20\n2-indeks: 15
```

---

# 169-Topshiriq: C-style satr va null-terminator (\0)

## Topshiriq sharti:
C tilidan meros bo'lgan belgilar massivi (`char[]`) va uning oxiridagi `\0` belgisini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    char satr[] = "Salom";
    std::cout << "Satr: " << satr << std::endl;
    std::cout << "Hajmi baytlarda: " << sizeof(satr) << std::endl;
    std::cout << "Oxirgi belgi kodi: " << (int)satr[5] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 'Salom' 5 ta harfdan iborat, ammo oxiridagi `\0` (null-terminator) bilan xotirada 6 bayt egallaydi.

## Ishlash natijasi:
```text
Satr: Salom\nHajmi baytlarda: 6\nOxirgi belgi kodi: 0
```

---

# 170-Topshiriq: C-string funksiyalari: strlen va strcmp

## Topshiriq sharti:
cstring kutubxonasidagi `strlen` va `strcmp` funksiyalaridan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstring>

int main() {
    const char* str1 = "Olma";
    const char* str2 = "Anor";
    std::cout << "Uzunligi: " << strlen(str1) << std::endl;
    int cmp = strcmp(str1, str2);
    if (cmp > 0) {
        std::cout << "str1 leksikografik jihatdan katta" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `strlen` satr uzunligini qaytaradi, `strcmp` ikki satrni harflar kodi bo'yicha solishtiradi.

## Ishlash natijasi:
```text
Uzunligi: 4\nstr1 leksikografik jihatdan katta
```

---

# 171-Topshiriq: std::string asosiy e'loni va chiqarilishi

## Topshiriq sharti:
C++ ning `std::string` sinfi yordamida dinamik satr yarating va chop eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string matn = "O'zbekiston - kelajagi buyuk davlat!";
    std::cout << matn << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::string` dinamik xotira boshqaruvini avtomatik amalga oshiradi va xotira sizib ketishining oldini oladi.

## Ishlash natijasi:
```text
O'zbekiston - kelajagi buyuk davlat!
```

---

# 172-Topshiriq: Satr uzunligi: length() va size()

## Topshiriq sharti:
std::string obyekti uzunligini `size()` va `length()` orqali aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string til = "C++ Dasturlash Tili";
    std::cout << "Uzunligi (length): " << til.length() << std::endl;
    std::cout << "Uzunligi (size): " << til.size() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `size()` va `length()` aynan bir xil vazifani bajaradi va belgilar sonini qaytaradi.

## Ishlash natijasi:
```text
Uzunligi (length): 19\nUzunligi (size): 19
```

---

# 173-Topshiriq: Satrlarni birlashtirish (Konkatenatsiya)

## Topshiriq sharti:
Satrlarni `+` operatori va `.append()` metodi yordamida birlashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string s1 = "Antigravity";
    std::string s2 = "AI";
    std::string natija1 = s1 + " " + s2;
    std::string natija2 = s1;
    natija2.append(" Tizimi");
    std::cout << natija1 << std::endl;
    std::cout << natija2 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `+` yangi satr nusxasini yaratadi, `.append()` esa mavjud satr oxiriga qo'shadi.

## Ishlash natijasi:
```text
Antigravity AI\nAntigravity Tizimi
```

---

# 174-Topshiriq: Satrdan belgini olish va o'zgartirish

## Topshiriq sharti:
Satr ichidagi ixtiyoriy belgini indeks orqali o'zgartiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string nom = "Toshkand";
    nom[7] = 't';
    std::cout << nom << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::string` da belgilar indeks orqali to'g'ridan-to'g'ri o'zgartirilishi mumkin (`mutable`).

## Ishlash natijasi:
```text
Toshkent
```

---

# 175-Topshiriq: Satr ichidan qidiruv: find() va npos

## Topshiriq sharti:
Satr ichida so'z borligini `find()` metodi orqali aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string matn = "Biz O'zbekistonda 10B AI model yaratmoqdamiz.";
    size_t pos = matn.find("10B");
    if (pos != std::string::npos) {
        std::cout << "'10B' " << pos << "-indeksdan boshlandi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar qidirilgan so'z topilmasa, `find()` maxsus `std::string::npos` qiymatini qaytaradi.

## Ishlash natijasi:
```text
'10B' 19-indeksdan boshlandi.
```

---

# 176-Topshiriq: Qism satr ajratish: substr()

## Topshiriq sharti:
Satrdan ma'lum indeksdan boshlab berilgan uzunlikdagi bo'lakni `substr()` orqali oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string sana = "2026-11-07";
    std::string yil = sana.substr(0, 4);
    std::string oy = sana.substr(5, 2);
    std::string kun = sana.substr(8, 2);
    std::cout << "Yil: " << yil << ", Oy: " << oy << ", Kun: " << kun << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `substr(start, count)` - boshlang'ich indeks va belgilar sonini qabul qiladi.

## Ishlash natijasi:
```text
Yil: 2026, Oy: 11, Kun: 07
```

---

# 177-Topshiriq: Satrdan o'chirish: erase()

## Topshiriq sharti:
Satrning o'rtasidagi keraksiz belgilar qismini `.erase()` orqali o'chirib tashlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string matn = "Salom dunyo azizlar!";
    matn.erase(6, 6); // 'dunyo ' ni o'chirish
    std::cout << matn << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `erase(pos, len)` ko'rsatilgan pozitsiyadan boshlab berilgan belgilar miqdorini o'chiradi.

## Ishlash natijasi:
```text
Salom azizlar!
```

---

# 178-Topshiriq: Satr ichiga kiritish: insert()

## Topshiriq sharti:
Satrning ko'rsatilgan pozitsiyasiga yangi qism satrni `.insert()` orqali joylashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string soz = "C Dasturlash";
    soz.insert(1, "++");
    std::cout << soz << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `insert(pos, text)` ko'rsatilgan indeksga yangi belgilarni kiritadi.

## Ishlash natijasi:
```text
C++ Dasturlash
```

---

# 179-Topshiriq: Satr qismini almashtirish: replace()

## Topshiriq sharti:
Satrdagi eski so'zni yangi so'z bilan `.replace()` metodi orqali almashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string xabar = "Bugun havo sovuq.";
    size_t pos = xabar.find("sovuq");
    if (pos != std::string::npos) {
        xabar.replace(pos, 5, "iliq");
    }
    std::cout << xabar << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `replace(pos, len, new_str)` eski bo'lakni yangi qiymatga almashtiradi.

## Ishlash natijasi:
```text
Bugun havo iliq.
```

---

# 180-Topshiriq: Satrni teskarisiga o'girish (std::reverse)

## Topshiriq sharti:
Satr harflarini boshidan oxirigacha teskari tartibda joylashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s = "Algoritm";
    std::reverse(s.begin(), s.end());
    std::cout << s << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `<algorithm>` dagi `std::reverse` iteratorlar oralig'idagi barcha elementlar o'rnini almashtiradi.

## Ishlash natijasi:
```text
mtprogla
```

---

# 181-Topshiriq: Satr polindromligini tekshirish

## Topshiriq sharti:
Berilgan satrning polindrom (chapdan va o'ngdan bir xil) ekanligini ikki ko'rsatkich yordamida tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string s = "kiyik";
    bool polindrom = true;
    int chap = 0, ong = s.length() - 1;
    while (chap < ong) {
        if (s[chap] != s[ong]) {
            polindrom = false;
            break;
        }
        chap++;
        ong--;
    }
    std::cout << s << (polindrom ? " - Polindrom" : " - Polindrom emas") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boshidan va oxiridan taqqoslash orqali tezkor tekshiriladi.

## Ishlash natijasi:
```text
kiyik - Polindrom
```

---

# 182-Topshiriq: Satrdagi unli va undosh harflarni sanash

## Topshiriq sharti:
Lotin alifbosidagi satrda nechta unli harf borligini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string matn = "O'zbekiston yoshlari";
    int unli = 0;
    std::string unlilar = "aeiouAEIOU";
    for (char c : matn) {
        if (unlilar.find(c) != std::string::npos) {
            unli++;
        }
    }
    std::cout << "Unli harflar soni: " << unli << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir harf `unlilar` to'plami ichidan qidiriladi.

## Ishlash natijasi:
```text
Unli harflar soni: 7
```

---

# 183-Topshiriq: Katta harflarga o'tkazish (toupper)

## Topshiriq sharti:
Satrdagi barcha kichik lotin harflarini katta harflarga o'zgartiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <cctype>

int main() {
    std::string s = "sun'iy intellekt";
    for (char& c : s) {
        c = std::toupper(c);
    }
    std::cout << s << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::toupper` belgini katta registrga o'tkazadi, havolasi (`char&`) esa satrni to'g'ridan-to'g'ri o'zgartiradi.

## Ishlash natijasi:
```text
SUN'IY INTELLEKT
```

---

# 184-Topshiriq: Kichik harflarga o'tkazish (tolower)

## Topshiriq sharti:
Satrdagi barcha katta harflarni kichik harflarga o'zgartiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <cctype>

int main() {
    std::string s = "KATTA MA'LUMOTLAR BAZASI";
    for (char& c : s) {
        c = std::tolower(c);
    }
    std::cout << s << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::tolower` funksiyasi belgilarni kichik harfga keltiradi.

## Ishlash natijasi:
```text
katta ma'lumotlar bazasi
```

---

# 185-Topshiriq: Satrdagi bo'shliqlarni (probel) sanash

## Topshiriq sharti:
Matndagi barcha probellar sonini sanab chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string matn = "C++ 20 standarti juda ko'p yangi imkoniyatlar qo'shdi.";
    int probellar = 0;
    for (char c : matn) {
        if (c == ' ') probellar++;
    }
    std::cout << "Probellar soni: " << probellar << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tsikl davomida probel belgisi hisoblab boriladi.

## Ishlash natijasi:
```text
Probellar soni: 7
```

---

# 186-Topshiriq: Sonni satrga aylantirish (std::to_string)

## Topshiriq sharti:
Butun va haqiqiy sonlarni `std::to_string` yordamida satrga aylantiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    int son = 2026;
    double vazn = 78.5;
    std::string s1 = std::to_string(son);
    std::string s2 = std::to_string(vazn);
    std::cout << "Yil: " << s1 << ", Vazn: " << s2.substr(0, 4) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::to_string` raqamli toifalarni `std::string` ga aylantirishning standart yo'lidir.

## Ishlash natijasi:
```text
Yil: 2026, Vazn: 78.5
```

---

# 187-Topshiriq: Satrni songa aylantirish (std::stoi, std::stod)

## Topshiriq sharti:
Satr ko'rinishidagi '1024' va '3.1415' qiymatlarini tegishli son turlariga aylantiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string int_str = "1024";
    std::string dbl_str = "3.1415";
    int a = std::stoi(int_str);
    double b = std::stod(dbl_str);
    std::cout << "a + 1 = " << (a + 1) << ", b * 2 = " << (b * 2) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::stoi` int ga, `std::stod` double ga o'giradi.

## Ishlash natijasi:
```text
a + 1 = 1025, b * 2 = 6.283
```

---

# 188-Topshiriq: std::string_view bilan tanishuv (C++17)

## Topshiriq sharti:
Nusxa ko'chirmasdan satrni ko'rish imkonini beruvchi yengil `std::string_view` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string_view>

void chopEt(std::string_view view) {
    std::cout << "Ko'rinish: " << view << ", Uzunligi: " << view.length() << std::endl;
}

int main() {
    const char* c_str = "Doimiy satr";
    chopEt(c_str);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::string_view` satr ma'lumotlarini nusxalamaydi, faqat uning ko'rsatkichi va hajmini ushlab turadi (Zero-copy).

## Ishlash natijasi:
```text
Ko'rinish: Doimiy satr, Uzunligi: 11
```

---

# 189-Topshiriq: std::string_view: remove_prefix va remove_suffix

## Topshiriq sharti:
std::string_view yordamida dinamik xotira ajratmasdan boshidan va oxiridan belgilarni kesib oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string_view>

int main() {
    std::string_view sv = "[XABAR: Muvaffaqiyatli]";
    sv.remove_prefix(1); // '[' ni olib tashlash
    sv.remove_suffix(1); // ']' ni olib tashlash
    std::cout << sv << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `remove_prefix` va `remove_suffix` faqat ichki ko'rsatkichni suradi va hech qanday dinamik allokatsiya talab qilmaydi.

## Ishlash natijasi:
```text
XABAR: Muvaffaqiyatli
```

---

# 190-Topshiriq: Satrni so'zlarga ajratish (std::stringstream)

## Topshiriq sharti:
Bo'shliqlar bilan ajratilgan gapni `std::stringstream` orqali alohida so'zlarga ajrating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <sstream>

int main() {
    std::string gap = "Katta tilli modellar matnni tez tahlil qiladi";
    std::stringstream ss(gap);
    std::string soz;
    int tartib = 1;
    while (ss >> soz) {
        std::cout << tartib++ << ": " << soz << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `stringstream` oqimi probellar orqali so'zlarni ketma-ket o'qib beradi.

## Ishlash natijasi:
```text
1: Katta\n2: tilli\n3: modellar\n4: matnni\n5: tez\n6: tahlil\n7: qiladi
```

---

# 191-Topshiriq: Gapdagi eng uzun so'zni topish

## Topshiriq sharti:
Berilgan gap ichidan eng uzun so'z va uning uzunligini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <sstream>

int main() {
    std::string matn = "O'zbekiston dasturchilari jahon darajasidagi sun'iy intellekt yaratmoqda";
    std::stringstream ss(matn);
    std::string soz, engUzun = "";
    while (ss >> soz) {
        if (soz.length() > engUzun.length()) {
            engUzun = soz;
        }
    }
    std::cout << "Eng uzun so'z: " << engUzun << " (" << engUzun.length() << " ta harf)" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir so'zning `length()` qiymati oldingi eng uzun so'z bilan taqqoslanadi.

## Ishlash natijasi:
```text
Eng uzun so'z: darajasidagi (12 ta harf)
```

---

# 192-Topshiriq: Anagramma tekshiruvi

## Topshiriq sharti:
Ikki satr bir xil harflardan tashkil topganligini (anagramma) ularni saralash orqali tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s1 = "tok";
    std::string s2 = "kot";
    std::string a = s1, b = s2;
    std::sort(a.begin(), a.end());
    std::sort(b.begin(), b.end());
    if (a == b) {
        std::cout << s1 << " va " << s2 << " - Anagramma" << std::endl;
    } else {
        std::cout << "Anagramma emas" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Harflari tartiblangan holatda teng bo'lsa, satrlar anagramma bo'ladi.

## Ishlash natijasi:
```text
tok va kot - Anagramma
```

---

# 193-Topshiriq: Satr ichidagi raqamlarni ajratish va yig'ish

## Topshiriq sharti:
Aralash matn ichidagi barcha raqamlarning yig'indisini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <cctype>

int main() {
    std::string matn = "Model 2026 yilda 10 milliard parametrga ega bo'ladi";
    int yigindi = 0;
    for (char c : matn) {
        if (std::isdigit(c)) {
            yigindi += (c - '0');
        }
    }
    std::cout << "Raqamlar yig'indisi: " << yigindi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::isdigit(c)` belgi raqam ekanligini bildiradi, `c - '0'` esa uning son qiymatini beradi.

## Ishlash natijasi:
```text
Raqamlar yig'indisi: 11
```

---

# 194-Topshiriq: Sezar shifri (Caesar Cipher shifrlash)

## Topshiriq sharti:
Matndagi harflarni alfavit bo'yicha k = 3 qadam oldinga siljitib shifrlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string matn = "SALOM";
    int k = 3;
    for (char& c : matn) {
        if (c >= 'A' && c <= 'Z') {
            c = 'A' + (c - 'A' + k) % 26;
        }
    }
    std::cout << "Shifrlangan: " << matn << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Modulli arifmetika `% 26` alifbo chegarasidan oshganda boshiga aylantiradi.

## Ishlash natijasi:
```text
Shifrlangan: VDORP
```

---

# 195-Topshiriq: Sezar shifridan deshifrlash

## Topshiriq sharti:
Shifrlangan 'VDORP' matnini k = 3 qadam orqaga surib asl holiga qaytaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string shifr = "VDORP";
    int k = 3;
    for (char& c : shifr) {
        if (c >= 'A' && c <= 'Z') {
            c = 'A' + (c - 'A' - k + 26) % 26;
        }
    }
    std::cout << "Asl matn: " << shifr << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Deshifrlashda manfiy qoldiq chiqmasligi uchun `+ 26` qo'shiladi.

## Ishlash natijasi:
```text
Asl matn: SALOM
```

---

# 196-Topshiriq: Oddiy siqish algoritmi (Run-Length Encoding asoslari)

## Topshiriq sharti:
Ketma-ket kelgan bir xil belgilarni sanab 'AAABBBCC' ni 'A3B3C2' ko'rinishida siqing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string kirish = "AAABBBCC";
    std::string natija = "";
    int n = kirish.length();
    for (int i = 0; i < n; ++i) {
        int soni = 1;
        while (i + 1 < n && kirish[i] == kirish[i + 1]) {
            soni++;
            i++;
        }
        natija += kirish[i] + std::to_string(soni);
    }
    std::cout << "Siqilgan: " << natija << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. RLE (Run-Length Encoding) ma'lumotlarni siqishning eng sodda va samarali usullaridan biridir.

## Ishlash natijasi:
```text
Siqilgan: A3B3C2
```

---

# 197-Topshiriq: Massiv chegarasidan chiqish xavfi va at() xavfsizligi

## Topshiriq sharti:
Operator `[]` chegara tekshirmasligi tufayli xavfli ekani va `.at()` xavfsizligi o'rtasidagi farqni tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <stdexcept>

int main() {
    std::vector<int> v = {10, 20, 30};
    try {
        std::cout << "Mavjud element: " << v.at(1) << std::endl;
        std::cout << "Xavfli murojaat: " << v.at(5) << std::endl;
    } catch (const std::out_of_range& e) {
        std::cout << "Xatolik ushlandi: Indeks chegaradan tashqarida!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `[]` noto'g'ri indeks kiritilganda Undefined Behavior yuzaga keltiradi, `.at()` esa xavfsiz istisno (`exception`) tashlaydi.

## Ishlash natijasi:
```text
Mavjud element: 20\nXatolik ushlandi: Indeks chegaradan tashqarida!
```

---

# 198-Topshiriq: 3 O'lchamli massiv (Tensor) asoslari

## Topshiriq sharti:
2x2x2 o'lchamli 3D massiv e'lon qiling va uning har bir qavatidagi elementlarni chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int tensor[2][2][2] = {
        {{{1, 2}, {3, 4}}},
        {{{5, 6}, {7, 8}}}
    };
    for (int i = 0; i < 2; ++i) {
        std::cout << "Qavat " << i << ":\n";
        for (int j = 0; j < 2; ++j) {
            for (int k = 0; k < 2; ++k) {
                std::cout << tensor[i][j][k] << " ";
            }
            std::cout << "\n";
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'p o'lchamli massivlar neyron tarmoqlar tensorlarini modellashtirishning asosi hisoblanadi.

## Ishlash natijasi:
```text
Qavat 0:\n1 2 \n3 4 \nQavat 1:\n5 6 \n7 8 
```

---

# 199-Topshiriq: Satrlar massivi va alfavit bo'yicha saralash

## Topshiriq sharti:
Satrlar massivini `std::sort` yordamida alfavit tartibida saralang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string tillar[] = {"Rust", "C++", "Python", "Go", "Dart"};
    int n = sizeof(tillar) / sizeof(tillar[0]);
    std::sort(tillar, tillar + n);
    for (int i = 0; i < n; ++i) {
        std::cout << tillar[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Satrlar leksikografik (ASCII tartibida) saralanadi.

## Ishlash natijasi:
```text
C++ Dart Go Python Rust
```

---

# 200-Topshiriq: Massivlar va satrlar xotirada joylashuvi tahlili

## Topshiriq sharti:
Massiv elementlarining xotira manzillari ketma-ket joylashishini isbotlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[3] = {100, 200, 300};
    for (int i = 0; i < 3; ++i) {
        std::cout << "arr[" << i << "] manzili: " << (void*)&arr[i] 
                  << ", oraliq bayt: sizeof(int)=" << sizeof(int) << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir element orasidagi manzil farqi aniq `sizeof(int) = 4` baytga teng bo'lib, xotira uzluksizligini ko'rsatadi.

## Ishlash natijasi:
```text
arr[0] manzili: 0x...\narr[1] manzili: 0x...\narr[2] manzili: 0x...
```

---

