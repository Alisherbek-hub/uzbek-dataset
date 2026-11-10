# C++ Dasturlash Tili - 5-Qism: Funksiyalar, Rekursiya va Overloading

Ushbu qismda C++ tilida funksiyalar arxitekturasi, havolalar, rekursiya, overloading, lambda, constexpr, RVO va zamonaviy C++ atributlariga oid 50 ta amaliy topshiriq jamlangan.

---

# 201-Topshiriq: Oddiy void funksiya e'lon qilish va chaqirish

## Topshiriq sharti:
Ekranga xush kelibsiz xabarini chiqaruvchi parametrsiz va qiymat qaytarmaydigan void funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void salomBer() {
    std::cout << "Assalomu alaykum! C++ olamiga xush kelibsiz!" << std::endl;
}

int main() {
    salomBer();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `void` funksiya hech qanday qiymat qaytarmaydi, faqat o'z tanasidagi amallarni bajaradi.

## Ishlash natijasi:
```text
Assalomu alaykum! C++ olamiga xush kelibsiz!
```

---

# 202-Topshiriq: Qiymat qaytaruvchi funksiya: Kvadrat hisoblash

## Topshiriq sharti:
Berilgan butun sonning kvadratini hisoblab qaytaruvchi funksiya tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int kvadrat(int x) {
    return x * x;
}

int main() {
    int son = 8;
    std::cout << son << " ning kvadrati: " << kvadrat(son) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `return` operatori hisoblangan natijani chaqiruvchi kodga qaytaradi.

## Ishlash natijasi:
```text
8 ning kvadrati: 64
```

---

# 203-Topshiriq: Parametrlarni qiymat bo'yicha uzatish (Pass-by-value)

## Topshiriq sharti:
Parametr qiymat bo'yicha uzatilganda funksiya ichidagi o'zgarish asl argumentga ta'sir qilmasligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void oshir(int a) {
    a += 10;
    std::cout << "Funksiya ichida a = " << a << std::endl;
}

int main() {
    int son = 5;
    oshir(son);
    std::cout << "main ichida son = " << son << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Pass-by-value da argumentning nusxasi yaratiladi, shu sababli asl o'zgaruvchi o'zgarmaydi.

## Ishlash natijasi:
```text
Funksiya ichida a = 15\nmain ichida son = 5
```

---

# 204-Topshiriq: Parametrlarni havola bo'yicha uzatish (Pass-by-reference)

## Topshiriq sharti:
Funksiya argumentini havola (`int&`) orqali qabul qilib, asl o'zgaruvchi qiymatini oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void oshirReference(int& a) {
    a += 10;
}

int main() {
    int son = 5;
    oshirReference(son);
    std::cout << "Yangi qiymat: " << son << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Havola (`&`) o'sha o'zgaruvchining ikkinchi nomi (taxallusi) bo'lib, unga qilingan o'zgarish to'g'ridan-to'g'ri asl qiymatga ta'sir qiladi.

## Ishlash natijasi:
```text
Yangi qiymat: 15
```

---

# 205-Topshiriq: Ikki son qiymatini almashtirish (Swap funksiyasi)

## Topshiriq sharti:
Havolalar yordamida ikkita butun son qiymatini o'zaro almashtiruvchi funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void almashtir(int& x, int& y) {
    int temp = x;
    x = y;
    y = temp;
}

int main() {
    int a = 10, b = 20;
    almashtir(a, b);
    std::cout << "a = " << a << ", b = " << b << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Nusxa yaratmasdan to'g'ridan-to'g'ri asl o'zgaruvchilar xotira katakchalari almashtiriladi.

## Ishlash natijasi:
```text
a = 20, b = 10
```

---

# 206-Topshiriq: Parametrlarni ko'rsatkich bo'yicha uzatish (Pass-by-pointer)

## Topshiriq sharti:
Funksiyaga ko'rsatkich (`int*`) uzatish orqali manzil bo'yicha qiymatni o'zgartiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void nolgaAylantir(int* ptr) {
    if (ptr != nullptr) {
        *ptr = 0;
    }
}

int main() {
    int val = 99;
    nolgaAylantir(&val);
    std::cout << "Natija: " << val << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkich dereferensiyasi (`*ptr`) orqali asl manzilga murojaat qilinadi.

## Ishlash natijasi:
```text
Natija: 0
```

---

# 207-Topshiriq: const parametrlar va xavfsizlik

## Topshiriq sharti:
Funksiya parametrini `const` qilish orqali uni o'zgarishdan himoya qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

void chopEt(const std::string& matn) {
    // matn += " xato"; // Kompilyatsiya xatosi beradi
    std::cout << "Chiqarish: " << matn << std::endl;
}

int main() {
    std::string s = "Himoyalangan ma'lumot";
    chopEt(s);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const &` ham xotiradan ortiqcha nusxa olishning oldini oladi, ham obyektni o'zgartirishdan asraydi.

## Ishlash natijasi:
```text
Chiqarish: Himoyalangan ma'lumot
```

---

# 208-Topshiriq: Standart parametrlar (Default arguments)

## Topshiriq sharti:
Parametrlari standart qiymatga ega bo'lgan funksiya e'lon qiling va turli usulda chaqiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void xabar(std::string matn = "Bo'sh xabar", int takror = 1) {
    for (int i = 0; i < takror; ++i) {
        std::cout << matn << " ";
    }
    std::cout << std::endl;
}

int main() {
    xabar();
    xabar("Salom", 3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Standart parametrlar funksiya chaqirilganda argument ko'rsatilmagan hollarda ishlatiladi.

## Ishlash natijasi:
```text
Bo'sh xabar \nSalom Salom Salom 
```

---

# 209-Topshiriq: Default parametrlar qoidasi: O'ngdan chapga

## Topshiriq sharti:
Default parametrlar faqat ro'yxatning o'ng tomonidan boshlab berilishi lozimligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int hisobla(int a, int b = 5, int c = 10) {
    return a + b + c;
}

int main() {
    std::cout << hisobla(1) << std::endl;
    std::cout << hisobla(1, 2) << std::endl;
    std::cout << hisobla(1, 2, 3) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `hisobla(1)` chaqirilganda b=5, c=10 olinadi. 1 + 5 + 10 = 16.

## Ishlash natijasi:
```text
16\n13\n6
```

---

# 210-Topshiriq: Funksiyani qayta yuklash (Overloading: turli toifalar)

## Topshiriq sharti:
Bir xil nomli, ammo har xil turdagi parametrlarni qabul qiluvchi `qoshish` funksiyalarini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int qoshish(int a, int b) {
    return a + b;
}

double qoshish(double a, double b) {
    return a + b;
}

int main() {
    std::cout << "Butun: " << qoshish(4, 5) << std::endl;
    std::cout << "Haqiqiy: " << qoshish(4.5, 2.3) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyator parametrlar toifasiga qarab mos funksiyani avtomatik tanlaydi.

## Ishlash natijasi:
```text
Butun: 9\nHaqiqiy: 6.8
```

---

# 211-Topshiriq: Funksiyani qayta yuklash: Turli sondagi parametrlar

## Topshiriq sharti:
Bir, ikki va uchta sonning yig'indisini hisoblovchi qayta yuklangan funksiyalar tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int sum(int a, int b) { return a + b; }
int sum(int a, int b, int c) { return a + b + c; }

int main() {
    std::cout << "Ikki son: " << sum(10, 20) << std::endl;
    std::cout << "Uch son: " << sum(10, 20, 30) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Argumentlar soni bo'yicha funksiyalar farqlanadi va kompilyatsiya qilinadi.

## Ishlash natijasi:
```text
Ikki son: 30\nUch son: 60
```

---

# 212-Topshiriq: Funksiya prototipi (Declaration vs Definition)

## Topshiriq sharti:
Funksiya deklaratsiyasini main dan oldin, tanasini esa main dan keyin joylashtirishni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

// Funksiya prototipi
int kopaytir(int, int);

int main() {
    std::cout << "Ko'paytma: " << kopaytir(6, 7) << std::endl;
    return 0;
}

// Funksiya tanasi
int kopaytir(int a, int b) {
    return a * b;
}
```

## Tushuntirish va Mantiq:
1. Prototip kompilyatorga funksiya imzosi haqida oldindan axborot beradi.

## Ishlash natijasi:
```text
Ko'paytma: 42
```

---

# 213-Topshiriq: Rekursiya asoslari: N dan 1 gacha sonlar

## Topshiriq sharti:
Rekursiv funksiya yordamida N dan 1 gacha sonlarni teskari tartibda chop eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void teskariChiqar(int n) {
    if (n <= 0) return; // Rekursiya to'xtash sharti (base case)
    std::cout << n << " ";
    teskariChiqar(n - 1); // Rekursiv chaqiruv
}

int main() {
    teskariChiqar(5);
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir rekursiv funksiyada cheksiz chaqiruv bo'lmasligi uchun to'xtash sharti bo'lishi shart.

## Ishlash natijasi:
```text
5 4 3 2 1
```

---

# 214-Topshiriq: Rekursiv faktorial hisoblash

## Topshiriq sharti:
n! faktorial qiymatini rekursiya yordamida hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

long long faktorial(int n) {
    if (n <= 1) return 1;
    return n * faktorial(n - 1);
}

int main() {
    int son = 6;
    std::cout << son << "! = " << faktorial(son) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Formulalar: 0! = 1, 1! = 1, n! = n * (n - 1)!.

## Ishlash natijasi:
```text
6! = 720
```

---

# 215-Topshiriq: Rekursiv Fibonachchi soni

## Topshiriq sharti:
N-chi Fibonachchi sonini rekursiv usulda toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int fib(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    return fib(n - 1) + fib(n - 2);
}

int main() {
    int n = 7;
    std::cout << n << "-Fibonachchi soni: " << fib(n) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. F(0)=0, F(1)=1, F(7) = 13 bo'ladi.

## Ishlash natijasi:
```text
7-Fibonachchi soni: 13
```

---

# 216-Topshiriq: Rekursiv raqamlar yig'indisi

## Topshiriq sharti:
Berilgan sonning barcha raqamlari yig'indisini rekursiv hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int raqamlarYigindisi(int n) {
    if (n == 0) return 0;
    return (n % 10) + raqamlarYigindisi(n / 10);
}

int main() {
    int n = 3456;
    std::cout << n << " raqamlari yig'indisi: " << raqamlarYigindisi(n) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 3 + 4 + 5 + 6 = 18.

## Ishlash natijasi:
```text
3456 raqamlari yig'indisi: 18
```

---

# 217-Topshiriq: Rekursiv darajaga oshirish

## Topshiriq sharti:
x^n darajani rekursiv ko'paytirish orqali hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

long long daraja(int x, int n) {
    if (n == 0) return 1;
    return x * daraja(x, n - 1);
}

int main() {
    std::cout << "3^4 = " << daraja(3, 4) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 3^4 = 3 * 3^3 = 3 * 27 = 81.

## Ishlash natijasi:
```text
3^4 = 81
```

---

# 218-Topshiriq: Rekursiv Evklid EKUB algoritmi

## Topshiriq sharti:
Ikki sonning EKUB ini rekursiv Evklid usulida bitta qatorda toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int ekub(int a, int b) {
    return (b == 0) ? a : ekub(b, a % b);
}

int main() {
    std::cout << "EKUB(56, 98) = " << ekub(56, 98) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `ekub(a, b) = ekub(b, a % b)` - qoldiq nol bo'lganda `a` EKUB hisoblanadi.

## Ishlash natijasi:
```text
EKUB(56, 98) = 14
```

---

# 219-Topshiriq: Xano minorasi masalasi (Tower of Hanoi)

## Topshiriq sharti:
3 ta ustun va N ta disk uchun Xano minorasi rekursiv ko'chirish ketma-ketligini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void hanoi(int n, char bosh, char yordam, char maqsad) {
    if (n == 1) {
        std::cout << "Disk 1: " << bosh << " -> " << maqsad << std::endl;
        return;
    }
    hanoi(n - 1, bosh, maqsad, yordam);
    std::cout << "Disk " << n << ": " << bosh << " -> " << maqsad << std::endl;
    hanoi(n - 1, yordam, bosh, maqsad);
}

int main() {
    int disklar = 3;
    hanoi(disklar, 'A', 'B', 'C');
    return 0;
}
```

## Tushuntirish va Mantiq:
1. N ta diskni ko'chirish uchun 2^N - 1 ta qadam (3 ta disk uchun 7 ta qadam) talab qilinadi.

## Ishlash natijasi:
```text
Disk 1: A -> C\nDisk 2: A -> B\nDisk 1: C -> B\nDisk 3: A -> C\nDisk 1: B -> A\nDisk 2: B -> C\nDisk 1: A -> C
```

---

# 220-Topshiriq: Qator rekursiyasi (Tail Recursion) va akkumulyator

## Topshiriq sharti:
Kompilyator stekni optimallashtira olishi uchun faktorialni Tail-call ko'rinishida yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

long long faktorialTail(int n, long long acc = 1) {
    if (n <= 1) return acc;
    return faktorialTail(n - 1, n * acc); // Oxirgi amal rekursiv chaqiruv
}

int main() {
    std::cout << "5! = " << faktorialTail(5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tail-call da rekursiv chaqiruvdan so'ng boshqa arifmetik amal bajarilmaydi, bu esa kompilyatorga tsiklga aylantirish imkonini beradi.

## Ishlash natijasi:
```text
5! = 120
```

---

# 221-Topshiriq: O'zaro rekursiya (Mutual Recursion)

## Topshiriq sharti:
Biri ikkinchisini chaqiruvchi `juftmi` va `toqmi` funksiyalarini tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

bool toqmi(int n);

bool juftmi(int n) {
    if (n == 0) return true;
    return toqmi(n - 1);
}

bool toqmi(int n) {
    if (n == 0) return false;
    return juftmi(n - 1);
}

int main() {
    std::cout << "4 juftmi? " << (juftmi(4) ? "Ha" : "Yo'q") << std::endl;
    std::cout << "5 juftmi? " << (juftmi(5) ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'zaro rekursiyada ikki funksiya navbatma-navbat bir-birini chaqirib boradi.

## Ishlash natijasi:
```text
4 juftmi? Ha\n5 juftmi? Yo'q
```

---

# 222-Topshiriq: inline funksiyalar va unumdorlik

## Topshiriq sharti:
`inline` kalit so'zi yordamida funksiya chaqiruvini kodga to'g'ridan-to'g'ri joylashtirishni (inlining) ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

inline int maksimal(int a, int b) {
    return (a > b) ? a : b;
}

int main() {
    int x = 45, y = 82;
    std::cout << "Kattasi: " << maksimal(x, y) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `inline` funksiya chaqirish xarajatlarini (call overhead) bartaraf etib, kod o'rniga joylashtiriladi.

## Ishlash natijasi:
```text
Kattasi: 82
```

---

# 223-Topshiriq: Statik mahalliy o'zgaruvchilar (static local variable)

## Topshiriq sharti:
Funksiya chaqiruvlari oralig'ida o'z qiymatini saqlab qoluvchi `static` o'zgaruvchini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void sanagich() {
    static int soni = 0;
    soni++;
    std::cout << "Funksiya " << soni << "-marta chaqirildi." << std::endl;
}

int main() {
    sanagich();
    sanagich();
    sanagich();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `static` o'zgaruvchi faqat bir marta initsializatsiya qilinadi va dastur yakunlangunga qadar xotirada saqlanadi.

## Ishlash natijasi:
```text
Funksiya 1-marta chaqirildi.\nFunksiya 2-marta chaqirildi.\nFunksiya 3-marta chaqirildi.
```

---

# 224-Topshiriq: Funksiyadan havola qaytarish (Return by reference)

## Topshiriq sharti:
Funksiya orqali massiv elementiga havola qaytarib, unga yangi qiymat yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int arr[3] = {10, 20, 30};

int& elementOlish(int indeks) {
    return arr[indeks];
}

int main() {
    elementOlish(1) = 999; // Funksiya qaytargan manzilga qiymat yozish
    std::cout << "arr[1] = " << arr[1] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Havola qaytaruvchi funksiya tenglikning chap tomonida (lvalue) qatnashishi mumkin.

## Ishlash natijasi:
```text
arr[1] = 999
```

---

# 225-Topshiriq: std::pair orqali bir vaqtda ikkita qiymat qaytarish

## Topshiriq sharti:
Massivning ham minimumi, ham maksimumini bitta funksiyadan `std::pair` orqali qaytaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <utility>

std::pair<int, int> minMaxTop(const int arr[], int n) {
    int mn = arr[0], mx = arr[0];
    for (int i = 1; i < n; ++i) {
        if (arr[i] < mn) mn = arr[i];
        if (arr[i] > mx) mx = arr[i];
    }
    return {mn, mx};
}

int main() {
    int data[] = {7, 2, 9, 4, 1};
    auto natija = minMaxTop(data, 5);
    std::cout << "Min: " << natija.first << ", Max: " << natija.second << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::pair` `.first` va `.second` a'zolari orqali ikki qiymatni guruhlaydi.

## Ishlash natijasi:
```text
Min: 1, Max: 9
```

---

# 226-Topshiriq: std::tuple orqali ko'p qiymat qaytarish (C++11)

## Topshiriq sharti:
`std::tuple` yordamida ism, yosh va bahoni bitta funksiyadan qaytaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <tuple>
#include <string>

std::tuple<std::string, int, double> talabaMalumoti() {
    return {"Alisher", 20, 4.95};
}

int main() {
    auto t = talabaMalumoti();
    std::cout << "Ism: " << std::get<0>(t) 
              << ", Yosh: " << std::get<1>(t) 
              << ", GPA: " << std::get<2>(t) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::tuple` ixtiyoriy turdagi bir nechta qiymatni saqlaydi va `std::get<N>()` orqali olinadi.

## Ishlash natijasi:
```text
Ism: Alisher, Yosh: 20, GPA: 4.95
```

---

# 227-Topshiriq: Structured Binding (C++17 tuzilmali bog'lash)

## Topshiriq sharti:
C++17 ning qulay sintaksisi orqali tuple yoki pair qiymatlarini alohida o'zgaruvchilarga ochib oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <tuple>
#include <string>

std::tuple<std::string, int, double> getInfo() {
    return {"Rustam", 22, 98.5};
}

int main() {
    auto [ism, yosh, ball] = getInfo();
    std::cout << ism << " | " << yosh << " yosh | " << ball << " ball" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `auto [a, b, c] = ...` sintaksisi kodni juda ixcham va o'qishli qiladi.

## Ishlash natijasi:
```text
Rustam | 22 yosh | 98.5 ball
```

---

# 228-Topshiriq: constexpr funksiyalar (Kompilyatsiya vaqtida hisoblash)

## Topshiriq sharti:
Kompilyatsiya vaqtida qiymati hisoblanadigan `constexpr` faktorial funksiyasini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

constexpr int faktorialConstexpr(int n) {
    int res = 1;
    for (int i = 2; i <= n; ++i) res *= i;
    return res;
}

int main() {
    constexpr int f5 = faktorialConstexpr(5); // Kompilyatsiya vaqtida 120 bo'ladi
    std::cout << "5! (constexpr) = " << f5 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `constexpr` funksiya doimiy ifodalar bilan chaqirilsa, dastur ishga tushishidan oldinroq kompilyatsiyada hisoblanadi.

## Ishlash natijasi:
```text
5! (constexpr) = 120
```

---

# 229-Topshiriq: consteval funksiyalar (C++20)

## Topshiriq sharti:
C++20 `consteval` (immediate function) doimiy ravishda kompilyatsiya vaqtida hisoblanishini talab qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

consteval int kubik(int n) {
    return n * n * n;
}

int main() {
    constexpr int k = kubik(4);
    std::cout << "4^3 = " << k << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `consteval` funksiyasi dinamik (runtime) qiymat bilan chaqirilsa, kompilyator xatolik beradi.

## Ishlash natijasi:
```text
4^3 = 64
```

---

# 230-Topshiriq: Massivning ko'rsatkichga aylanib ketishi (Array Decay)

## Topshiriq sharti:
Funksiyaga massiv uzatilganda uning ko'rsatkichga aylanib `sizeof` massiv hajmini ko'rsatmasligini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void tahlil(int arr[]) {
    // arr bu yerda int* ga aylangan
    std::cout << "Funksiya ichida sizeof(arr): " << sizeof(arr) << " bayt (pointer hajmi)" << std::endl;
}

int main() {
    int sonlar[10];
    std::cout << "main ichida sizeof(sonlar): " << sizeof(sonlar) << " bayt (massiv hajmi)" << std::endl;
    tahlil(sonlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shu sababli C++ da massivlar bilan birga ularning o'lchamini ham funksiyaga uzatish kerak bo'ladi.

## Ishlash natijasi:
```text
main ichida sizeof(sonlar): 40 bayt (massiv hajmi)\nFunksiya ichida sizeof(arr): 8 bayt (pointer hajmi)
```

---

# 231-Topshiriq: Massivni o'lchami bilan birga uzatish

## Topshiriq sharti:
Massiv va uning o'lchamini funksiyaga to'g'ri uzatib, o'rtacha qiymatini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

double ortacha(const int arr[], int size) {
    int sum = 0;
    for (int i = 0; i < size; ++i) sum += arr[i];
    return (double)sum / size;
}

int main() {
    int ballar[] = {80, 90, 85, 95, 100};
    std::cout << "O'rtacha: " << ortacha(ballar, 5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const int arr[]` ma'lumotlar o'zgartirilmasligini bildiradi.

## Ishlash natijasi:
```text
O'rtacha: 90
```

---

# 232-Topshiriq: 2D Massivni funksiyaga uzatish

## Topshiriq sharti:
2 o'lchamli massivni funksiyaga uzatishda ustunlar soni aniq ko'rsatilishi kerakligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void chopEtMatritsa(int mat[][3], int rows) {
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < 3; ++j) {
            std::cout << mat[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

int main() {
    int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
    chopEtMatritsa(m, 2);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++ xotira ofsetini to'g'ri hisoblashi uchun 2-o'lcham (ustunlar soni) ko'rsatilishi shart.

## Ishlash natijasi:
```text
1 2 3 \n4 5 6 
```

---

# 233-Topshiriq: std::array ni funksiyaga havola orqali uzatish

## Topshiriq sharti:
`std::array` o'lchamini yo'qotmaydigan zamonaviy massiv sifatida funksiyaga qabul qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <array>

void chopEtArray(const std::array<int, 4>& a) {
    for (int x : a) std::cout << x << " ";
    std::cout << std::endl;
}

int main() {
    std::array<int, 4> sonlar = {11, 22, 33, 44};
    chopEtArray(sonlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::array` o'z o'lchamini bilar ekan, array decay yuz bermaydi.

## Ishlash natijasi:
```text
11 22 33 44 
```

---

# 234-Topshiriq: std::vector ni const reference orqali uzatish

## Topshiriq sharti:
Katta dinamik ro'yxatlarni `const std::vector<int>&` orqali xotira nusxalamasdan uzatish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int yigindi(const std::vector<int>& v) {
    int s = 0;
    for (int x : v) s += x;
    return s;
}

int main() {
    std::vector<int> sonlar = {5, 15, 25, 35};
    std::cout << "Yig'indi: " << yigindi(sonlar) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const &` katta dinamik massivlarni sekundiga millionlab chaqiruvlarda juda yuqori tezlikda uzatadi.

## Ishlash natijasi:
```text
Yig'indi: 80
```

---

# 235-Topshiriq: const std::string& va std::string_view taqqoslashi

## Topshiriq sharti:
Satrlarni qabul qilishda `std::string_view` ning afzalligini namoyish qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string_view>

void chopEtView(std::string_view sv) {
    std::cout << "Ko'rinish: " << sv << std::endl;
}

int main() {
    chopEtView("C-string literal"); // Hech qanday string obyekti yaratilmaydi
    std::string s = "std::string obyekti";
    chopEtView(s);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::string_view` ham `const char*`, ham `std::string` ni vaqtinchalik xotira ajratmasdan qabul qiladi.

## Ishlash natijasi:
```text
Ko'rinish: C-string literal\nKo'rinish: std::string obyekti
```

---

# 236-Topshiriq: Nomlar maydoni (Namespace)

## Topshiriq sharti:
Nomlar to'qnashuvining oldini olish uchun nomlar maydonini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

namespace Matematika {
    int hisobla(int a, int b) { return a * b; }
}

namespace Fizika {
    int hisobla(int a, int b) { return a + b; }
}

int main() {
    std::cout << "Matematika: " << Matematika::hisobla(5, 4) << std::endl;
    std::cout << "Fizika: " << Fizika::hisobla(5, 4) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `namespace` bir xil nomli funksiyalarni alohida mantiqiy guruhlarga ajratadi.

## Ishlash natijasi:
```text
Matematika: 20\nFizika: 9
```

---

# 237-Topshiriq: Ichma-ich nomlar maydoni (Nested namespaces)

## Topshiriq sharti:
C++17 ning `namespace A::B` ixcham yozilishidan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>

namespace Ai::Engine {
    void init() {
        std::cout << "AI Dvigateli ishga tushirildi." << std::endl;
    }
}

int main() {
    Ai::Engine::init();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++17 dan boshlab `namespace A::B` shaklida ixcham yozish mumkin.

## Ishlash natijasi:
```text
AI Dvigateli ishga tushirildi.
```

---

# 238-Topshiriq: Anonim (Nomsiz) namespace

## Topshiriq sharti:
Fayl ichidagi funksiyalarni boshqa fayllardan yashirish (Internal Linkage) uchun anonim nomlar maydonini ishlating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

namespace {
    int yashirinSon = 42;
    void maxfiyAmal() {
        std::cout << "Maxfiy qiymat: " << yashirinSon << std::endl;
    }
}

int main() {
    maxfiyAmal();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Nomsiz namespace faqat joriy tarjima birligi (.cpp fayl) doirasida ko'rinadi (C tilidagi `static` o'rniga zamonaviy alternativ).

## Ishlash natijasi:
```text
Maxfiy qiymat: 42
```

---

# 239-Topshiriq: Funksiyaga ko'rsatkich (Function Pointer)

## Topshiriq sharti:
Funksiya manzilini ko'rsatkichda saqlang va ko'rsatkich orqali chaqiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int kvadrat(int x) { return x * x; }

int main() {
    int (*funPtr)(int) = &kvadrat;
    int natija = funPtr(7);
    std::cout << "7 ning kvadrati: " << natija << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int (*funPtr)(int)` - bitta int qabul qilib, int qaytaruvchi funksiya ko'rsatkichi.

## Ishlash natijasi:
```text
7 ning kvadrati: 49
```

---

# 240-Topshiriq: Callback funksiyalar

## Topshiriq sharti:
Funksiya ko'rsatkichini argument sifatida qabul qilib qayta ishlovchi (callback) funksiya tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void massivniOzgartir(int arr[], int n, int (*amal)(int)) {
    for (int i = 0; i < n; ++i) {
        arr[i] = amal(arr[i]);
    }
}

int ikkiBarobar(int x) { return x * 2; }

int main() {
    int data[] = {1, 2, 3, 4};
    massivniOzgartir(data, 4, ikkiBarobar);
    for (int x : data) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Callback lar algoritmlarni moslashuvchan qilishning klassik usulidir.

## Ishlash natijasi:
```text
2 4 6 8 
```

---

# 241-Topshiriq: using orqali funksiya ko'rsatkichi turini aniqlash

## Topshiriq sharti:
`using` sintaksisi yordamida funksiya ko'rsatkichi turiga o'qilishi qulay nom bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>

using Amaliyotchi = int(*)(int, int);

int qosh(int a, int b) { return a + b; }
int ayir(int a, int b) { return a - b; }

void bajar(int a, int b, Amaliyotchi op) {
    std::cout << "Natija: " << op(a, b) << std::endl;
}

int main() {
    bajar(10, 4, qosh);
    bajar(10, 4, ayir);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `using Amaliyotchi = int(*)(int, int);` murakkab ko'rsatkich sintaksisini soddalashtiradi.

## Ishlash natijasi:
```text
Natija: 14\nNatija: 6
```

---

# 242-Topshiriq: std::function (Universal funksiya o'rami)

## Topshiriq sharti:
`<functional>` dagi `std::function` orqali oddiy funksiya va lambdalarni bir xil turda saqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <functional>

void hisob(std::function<int(int)> fn, int x) {
    std::cout << "Hisob: " << fn(x) << std::endl;
}

int main() {
    hisob([](int n) { return n * n * n; }, 3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::function` polimorfik funksiya obyekti bo'lib, har qanday chaqiriluvchi (callable) narsani o'z ichiga oladi.

## Ishlash natijasi:
```text
Hisob: 27
```

---

# 243-Topshiriq: Rekursiv ikkilik qidiruv (Recursive Binary Search)

## Topshiriq sharti:
Saralangan massivda qidiruvni rekursiv funksiya yordamida bajaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int rekursivBS(const int arr[], int chap, int ong, int kalit) {
    if (chap > ong) return -1;
    int orta = chap + (ong - chap) / 2;
    if (arr[orta] == kalit) return orta;
    if (arr[orta] > kalit) return rekursivBS(arr, chap, orta - 1, kalit);
    return rekursivBS(arr, orta + 1, ong, kalit);
}

int main() {
    int arr[] = {2, 5, 8, 12, 16, 23, 38, 56};
    int idx = rekursivBS(arr, 0, 7, 23);
    std::cout << "23 soni indeksi: " << idx << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir chaqiruvda diapazon 2 barobar qisqaradi.

## Ishlash natijasi:
```text
23 soni indeksi: 5
```

---

# 244-Topshiriq: Rekursiv polindrom tekshiruvi

## Topshiriq sharti:
Satrning bosh va oxirgi harflarini tekshirib, ichkari tomon harakatlanuvchi rekursiv funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

bool rekursivPolindrom(const std::string& s, int chap, int ong) {
    if (chap >= ong) return true;
    if (s[chap] != s[ong]) return false;
    return rekursivPolindrom(s, chap + 1, ong - 1);
}

int main() {
    std::string s = "radar";
    std::cout << s << (rekursivPolindrom(s, 0, s.length() - 1) ? " - Polindrom" : " - Emas") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Chekka harflar teng bo'lsa, oraliq qism rekursiv tekshiriladi.

## Ishlash natijasi:
```text
radar - Polindrom
```

---

# 245-Topshiriq: Rekursiv massiv elementlari yig'indisi

## Topshiriq sharti:
Massivning barcha sonlari yig'indisini rekursiv hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int massivSum(const int arr[], int n) {
    if (n <= 0) return 0;
    return arr[n - 1] + massivSum(arr, n - 1);
}

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    std::cout << "Yig'indi: " << massivSum(arr, 5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oxirgi element olingach, qolgan `n - 1` ta element rekursiv hisoblanadi.

## Ishlash natijasi:
```text
Yig'indi: 15
```

---

# 246-Topshiriq: [[nodiscard]] atributi (C++17)

## Topshiriq sharti:
Qaytarilgan natijani e'tiborsiz qoldirish xatolikka olib kelishi mumkin bo'lganda kompilyatorni ogohlantiruvchi qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

[[nodiscard]] bool xotiraniAjrat() {
    // Muvaffaqiyatli bo'lsa true
    return true;
}

int main() {
    bool ok = xotiraniAjrat();
    std::cout << "Status: " << (ok ? "Bajarildi" : "Xato") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `[[nodiscard]]` funksiyaning qaytargan qiymatini o'zgaruvchiga olmasdan tashlab yuborishda kompilyator ogohlantirish (warning) berishini ta'minlaydi.

## Ishlash natijasi:
```text
Status: Bajarildi
```

---

# 247-Topshiriq: [[maybe_unused]] atributi (C++17)

## Topshiriq sharti:
Ishlatilmagan parametr yoki o'zgaruvchilar bo'yicha ogohlantirishlarni bartaraf qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void logXabari([[maybe_unused]] int kod, const char* matn) {
    std::cout << "Xabar: " << matn << std::endl;
}

int main() {
    logXabari(200, "Tizim tayyor");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `[[maybe_unused]]` kompilyatorning 'unused parameter' ogohlantirishini bostiradi.

## Ishlash natijasi:
```text
Xabar: Tizim tayyor
```

---

# 248-Topshiriq: Copy Elision va RVO (Return Value Optimization)

## Topshiriq sharti:
Funksiyadan obyekt qaytarilganda zamonaviy C++ da ortiqcha nusxalash yuz bermasligini (RVO) ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

std::string yarat() {
    std::string s = "Katta ma'lumotlar bloki";
    return s; // C++17 dan majburiy RVO / NRVO
}

int main() {
    std::string res = yarat();
    std::cout << "Res: " << res << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Return Value Optimization (RVO) obyekti to'g'ridan-to'g'ri chaqiruvchining xotirasida quradi, nusxalash xarajatlarini nolga tushiradi.

## Ishlash natijasi:
```text
Res: Katta ma'lumotlar bloki
```

---

# 249-Topshiriq: Oddiy Lambda funksiyasi asoslari

## Topshiriq sharti:
Funksiya ichida anonim (lambda) funksiya e'lon qilib foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    auto kub = [](int n) {
        return n * n * n;
    };
    std::cout << "5 ning kubi: " << kub(5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `[](int n) { ... }` - nomsiz ixcham funksiya bo'lib, C++11 da qo'shilgan.

## Ishlash natijasi:
```text
5 ning kubi: 125
```

---

# 250-Topshiriq: Funksiyalar va Stek freymi (Call Stack tahlili)

## Topshiriq sharti:
Funksiya chaqiruvlari kompyuter xotirasining stekida (Stack) qanday saqlanishi va qaytishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void funC() {
    std::cout << "funC bajarildi (Stack eng yuqori nuqtasi)" << std::endl;
}

void funB() {
    std::cout << "funB boshlandi" << std::endl;
    funC();
    std::cout << "funB tugadi" << std::endl;
}

void funA() {
    std::cout << "funA boshlandi" << std::endl;
    funB();
    std::cout << "funA tugadi" << std::endl;
}

int main() {
    funA();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir funksiya chaqirilganda stekda yangi freym ochiladi va tugagach LIFO (Last-In, First-Out) tartibida yopiladi.

## Ishlash natijasi:
```text
funA boshlandi\nfunB boshlandi\nfunC bajarildi (Stack eng yuqori nuqtasi)\nfunB tugadi\nfunA tugadi
```

---

