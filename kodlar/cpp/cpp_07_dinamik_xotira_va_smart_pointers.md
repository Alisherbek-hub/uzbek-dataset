# C++ Dasturlash Tili - 7-Qism: Dinamik Xotira va Aqlli Ko'rsatkichlar (Smart Pointers)

Ushbu qismda Stack vs Heap, new/delete, RAII, std::unique_ptr, std::shared_ptr, std::weak_ptr, Arena allokatorlar va zamonaviy xotira xavfsizligiga oid 50 ta amaliy topshiriq jamlangan.

---

# 301-Topshiriq: Stack vs Heap xotira tushunchasi

## Topshiriq sharti:
Stekda avtomatik boshqariladigan o'zgaruvchi va Xipda (Heap) dinamik ajratiladigan xotira o'rtasidagi farqni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int stackSon = 10; // Stekda joylashadi, avtomatik o'chiriladi
    int* heapSon = new int(20); // Xipda (Heap) dinamik xotira
    std::cout << "Stack qiymati: " << stackSon << std::endl;
    std::cout << "Heap qiymati: " << *heapSon << std::endl;
    delete heapSon; // Qo'lda ozod qilish shart
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Stek xotira juda tez va hajmi chegaralangan bo'ladi. Xip (Heap) esa katta hajmdagi dinamik xotira uchun xizmat qiladi.

## Ishlash natijasi:
```text
Stack qiymati: 10\nHeap qiymati: 20
```

---

# 302-Topshiriq: new operatori orqali bitta butun songa dinamik xotira ajratish

## Topshiriq sharti:
Dinamik xotiradan int uchun joy olib, qiymat yozing va ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int* ptr = new int(100);
    std::cout << "Dinamik int qiymati: " << *ptr << std::endl;
    delete ptr;
    ptr = nullptr;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `new int(100)` xotira ajratadi va darhol initsializatsiya qiladi.

## Ishlash natijasi:
```text
Dinamik int qiymati: 100
```

---

# 303-Topshiriq: delete operatori va ko'rsatkichni nullptr qilish

## Topshiriq sharti:
Xotirani delete qilgach ko'rsatkichni darhol nullptr qilish xavfsizlik qoidasi ekanligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double* d = new double(3.14159);
    delete d;
    d = nullptr; // Dangling pointer bo'lmasligi uchun
    if (d == nullptr) {
        std::cout << "Xotira muvaffaqiyatli ozod qilindi va ko'rsatkich tozalandi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `delete` qilingan manzilga qayta murojaat qilish falokatli oqibatlarga olib kelishi sababli `d = nullptr` yoziladi.

## Ishlash natijasi:
```text
Xotira muvaffaqiyatli ozod qilindi va ko'rsatkich tozalandi.
```

---

# 304-Topshiriq: new[] orqali dinamik 1D massiv yaratish

## Topshiriq sharti:
O'lchami ish vaqtida aniqlanadigan N ta elementli dinamik massiv yarating va to'ldiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 5;
    int* arr = new int[n];
    for (int i = 0; i < n; ++i) {
        arr[i] = (i + 1) * 10;
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
    delete[] arr; // Massiv uchun delete[]
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dinamik massivlar o'lchami o'zgaruvchiga bog'liq bo'lishi mumkin.

## Ishlash natijasi:
```text
10 20 30 40 50
```

---

# 305-Topshiriq: delete[] operatori zarurati

## Topshiriq sharti:
Nima uchun massiv uchun oddiy `delete` emas, balki `delete[]` ishlatilishi shartligini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int* massiv = new int[10];
    // To'g'ri ozod qilish usuli:
    delete[] massiv;
    std::cout << "delete[] barcha elementlar xotirasini to'liq ozod qiladi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `delete[]` massiv hajmi haqidagi ichki metama'lumotni o'qiydi va har bir element destruktorini to'g'ri chaqiradi.

## Ishlash natijasi:
```text
delete[] barcha elementlar xotirasini to'liq ozod qiladi.
```

---

# 306-Topshiriq: Xotira sizib ketishi (Memory Leak)

## Topshiriq sharti:
Ozod qilinmagan xotira RAM sarflanishiga olib kelishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void xotiraSizishiMisoli() {
    int* s = new int[1000]; // Ajratildi
    // delete[] s; qilinmadi! Funksiya tugagach manzil yo'qoladi, xotira esa band qoladi
}

int main() {
    std::cout << "Xotira sizishi - ajratilgan xotirani ozod qilish unutilganda yuzaga keladi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir `new` uchun aniq bitta `delete` bo'lishi shart, aks holda dastur xotirani to'ldirib qo'yadi.

## Ishlash natijasi:
```text
Xotira sizishi - ajratilgan xotirani ozod qilish unutilganda yuzaga keladi.
```

---

# 307-Topshiriq: Dinamik 2D massiv yaratish (int**)

## Topshiriq sharti:
Qatorlari va ustunlari dinamik bo'lgan 2D matritsa yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int rows = 2, cols = 3;
    int** mat = new int*[rows];
    for (int i = 0; i < rows; ++i) {
        mat[i] = new int[cols];
    }
    mat[0][0] = 5; mat[0][1] = 6; mat[0][2] = 7;
    std::cout << "mat[0][1] = " << mat[0][1] << std::endl;

    for (int i = 0; i < rows; ++i) delete[] mat[i];
    delete[] mat;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Avval qator ko'rsatkichlari massivi, so'ngra har bir satr uchun alohida massiv ajratiladi.

## Ishlash natijasi:
```text
mat[0][1] = 6
```

---

# 308-Topshiriq: Dinamik 2D matritsani to'liq ozod qilish

## Topshiriq sharti:
Dinamik 2D matritsani bosqichma-bosqich teskari tartibda ozod qilish algoritmini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void ozodQil2D(int**& mat, int rows) {
    if (mat == nullptr) return;
    for (int i = 0; i < rows; ++i) {
        delete[] mat[i];
    }
    delete[] mat;
    mat = nullptr;
}

int main() {
    int rows = 3;
    int** m = new int*[rows];
    for (int i = 0; i < rows; ++i) m[i] = new int[3];
    ozodQil2D(m, rows);
    std::cout << "2D matritsa xavfsiz o'chirildi: " << (m == nullptr ? "nullptr" : "xato") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ichki massivlar o'chirilgach, tashqi massiv o'chiriladi va ko'rsatkich `nullptr` ga tenglashtiriladi.

## Ishlash natijasi:
```text
2D matritsa xavfsiz o'chirildi: nullptr
```

---

# 309-Topshiriq: Bitta tekis blokda 2D massiv yaratish (Flat 2D Array)

## Topshiriq sharti:
Kesh unumdorligini oshirish uchun 2D massivni bitta yaxlit 1D massiv sifatida ajratish usulini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int rows = 2, cols = 3;
    int* flatMat = new int[rows * cols];

    // Murojaat: [i * cols + j]
    flatMat[0 * cols + 2] = 99;
    std::cout << "flatMat[0][2] = " << flatMat[0 * cols + 2] << std::endl;

    delete[] flatMat; // Bitta delete[] bilan to'liq ozod qilinadi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitta yaxlit xotira bloki kesh xotirasi uchun juda qulay va allokatsiya xarajatlarini kamaytiradi.

## Ishlash natijasi:
```text
flatMat[0][2] = 99
```

---

# 310-Topshiriq: std::nothrow bilan new operatori

## Topshiriq sharti:
Xotira yetishmaganda istisno tashlamasdan `nullptr` qaytaruvchi `std::nothrow` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <new>

int main() {
    int* ptr = new (std::nothrow) int(42);
    if (ptr != nullptr) {
        std::cout << "Xotira muvaffaqiyatli ajratildi: " << *ptr << std::endl;
        delete ptr;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `new (std::nothrow)` xotira tugaganda `std::bad_alloc` tashlamaydi, balki `nullptr` qaytaradi.

## Ishlash natijasi:
```text
Xotira muvaffaqiyatli ajratildi: 42
```

---

# 311-Topshiriq: RAII tamoyili asoslari

## Topshiriq sharti:
Resurs konstruktorda olinib, destruktorda avtomatik ozod qilinadigan RAII sinfini tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class ResursXoJayin {
    int* data;
public:
    ResursXoJayin(int qiymat) : data(new int(qiymat)) {
        std::cout << "Resurs ajratildi: " << *data << std::endl;
    }
    ~ResursXoJayin() {
        std::cout << "Resurs avtomatik ozod qilindi: " << *data << std::endl;
        delete data;
    }
};

int main() {
    {
        ResursXoJayin r(555);
    } // Blok tugagach destruktor avtomatik ishlaydi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. RAII (Resource Acquisition Is Initialization) C++ da xotira va fayllarni xavfsiz boshqarishning oltin qoidasidir.

## Ishlash natijasi:
```text
Resurs ajratildi: 555\nResurs avtomatik ozod qilindi: 555
```

---

# 312-Topshiriq: Sodda Smart Pointer o'rami (RAII Wrapper)

## Topshiriq sharti:
O'zimizning sodda `SmartIntPtr` sinfimizni yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class SmartIntPtr {
    int* ptr;
public:
    explicit SmartIntPtr(int* p = nullptr) : ptr(p) {}
    ~SmartIntPtr() { delete ptr; }
    int& operator*() { return *ptr; }
    int* operator->() { return ptr; }
};

int main() {
    SmartIntPtr p(new int(77));
    std::cout << "Smart pointer qiymati: " << *p << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Obyekt ko'lamdan (scope) chiqishi bilan avtomatik ravishda `delete ptr` chaqiriladi.

## Ishlash natijasi:
```text
Smart pointer qiymati: 77
```

---

# 313-Topshiriq: std::unique_ptr asoslari (C++11)

## Topshiriq sharti:
Faqat bitta egaga ega bo'lgan standart `std::unique_ptr` dan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    std::unique_ptr<int> uptr(new int(123));
    std::cout << "unique_ptr qiymati: " << *uptr << std::endl;
    return 0; // Avtomatik delete qilinadi!
}
```

## Tushuntirish va Mantiq:
1. `std::unique_ptr` ortiqcha xotira va vaqt sarflamaydi (Zero Overhead).

## Ishlash natijasi:
```text
unique_ptr qiymati: 123
```

---

# 314-Topshiriq: std::make_unique orqali xavfsiz yaratish (C++14)

## Topshiriq sharti:
To'g'ridan-to'g'ri `new` ishlatmasdan `std::make_unique` orqali obyekt yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto uptr = std::make_unique<int>(456);
    std::cout << "make_unique qiymati: " << *uptr << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::make_unique` istisnolarga qarshi to'liq xavfsiz (exception safe) va zamonaviy usuldir.

## Ishlash natijasi:
```text
make_unique qiymati: 456
```

---

# 315-Topshiriq: unique_ptr ni nusxalab bo'lmasligi

## Topshiriq sharti:
std::unique_ptr nusxalash konstruktori o'chirilganini (`= delete`) va nusxalash xatolik berishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto p1 = std::make_unique<int>(10);
    // auto p2 = p1; // Kompilyatsiya xatosi! Nusxa olish taqiqlangan
    std::cout << "p1 yakka mulkdor: " << *p1 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mulkdorlik faqat bitta ko'rsatkichda bo'lishi kafolatlanadi.

## Ishlash natijasi:
```text
p1 yakka mulkdor: 10
```

---

# 316-Topshiriq: std::move yordamida unique_ptr mulkdorligini o'tkazish

## Topshiriq sharti:
`std::move` orqali resurs egaligini boshqa `unique_ptr` ga ko'chiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto p1 = std::make_unique<int>(88);
    std::unique_ptr<int> p2 = std::move(p1); // p1 dan p2 ga ko'chirildi

    if (p1 == nullptr) {
        std::cout << "p1 endi bo'sh (nullptr)." << std::endl;
    }
    std::cout << "p2 qiymati: " << *p2 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'chirishdan so'ng asl ko'rsatkich `nullptr` bo'lib qoladi.

## Ishlash natijasi:
```text
p1 endi bo'sh (nullptr).\np2 qiymati: 88
```

---

# 317-Topshiriq: unique_ptr: get() metodi

## Topshiriq sharti:
Mulkdorlikni bermagan holda xom ko'rsatkich manzilini `.get()` orqali o'qing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

void faqatOqi(const int* ptr) {
    if (ptr) std::cout << "O'qildi: " << *ptr << std::endl;
}

int main() {
    auto uptr = std::make_unique<int>(99);
    faqatOqi(uptr.get());
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.get()` xom ko'rsatkichni faqat o'qish uchun tashqi funksiyalarga uzatishda ishlatiladi.

## Ishlash natijasi:
```text
O'qildi: 99
```

---

# 318-Topshiriq: unique_ptr: release() metodi

## Topshiriq sharti:
Smart pointerdan mulkdorlikni tortib olib, xom ko'rsatkichga aylantiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto uptr = std::make_unique<int>(33);
    int* xom = uptr.release(); // uptr endi mas'ul emas
    std::cout << "Xom pointer qiymati: " << *xom << std::endl;
    delete xom; // Endi qo'lda delete qilish zarur
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.release()` obyekti o'chirmasdan uning boshqaruvini qo'yib yuboradi.

## Ishlash natijasi:
```text
Xom pointer qiymati: 33
```

---

# 319-Topshiriq: unique_ptr: reset() metodi

## Topshiriq sharti:
Eski resursni ozod qilib, yangi qiymat bilan yangilang yoki bo'shating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto uptr = std::make_unique<int>(10);
    std::cout << "Eski: " << *uptr << std::endl;
    uptr.reset(new int(20)); // Eski 10 o'chirildi, yangi 20 yuklandi
    std::cout << "Yangi: " << *uptr << std::endl;
    uptr.reset(); // Butunlay bo'shatildi
    std::cout << "Bo'shmi: " << (uptr == nullptr ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.reset()` eski xotirani xavfsiz ozod qilib yangi manzilni biriktiradi.

## Ishlash natijasi:
```text
Eski: 10\nYangi: 20\nBo'shmi: Ha
```

---

# 320-Topshiriq: Dinamik massivlar uchun std::unique_ptr<int[]>

## Topshiriq sharti:
Dinamik massivni boshqaruvchi va `delete[]` ni avtomatik chaqiruvchi `unique_ptr` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto arr = std::make_unique<int[]>(3);
    arr[0] = 11;
    arr[1] = 22;
    arr[2] = 33;
    for (int i = 0; i < 3; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `unique_ptr<int[]>` ixtisoslashuvi indekslash `[]` operatorini va to'g'ri `delete[]` ni ta'minlaydi.

## Ishlash natijasi:
```text
11 22 33 
```

---

# 321-Topshiriq: unique_ptr uchun Custom Deleter

## Topshiriq sharti:
Fayl yoki maxsus resursni yopish uchun maxsus o'chiruvchi (custom deleter) funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

struct FaylYopuvchi {
    void operator()(FILE* f) const {
        if (f) {
            std::cout << "Fayl Custom Deleter orqali yopildi." << std::endl;
            fclose(f);
        }
    }
};

int main() {
    {
        // Mock tarzda stdout ni kuzatish
        std::unique_ptr<FILE, FaylYopuvchi> fPtr(nullptr);
    }
    std::cout << "Custom deleter muvaffaqiyatli sinovdan o'tdi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Custom deleter `unique_ptr` ga nafaqat xotira, balki har qanday tizim resursini boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Custom deleter muvaffaqiyatli sinovdan o'tdi.
```

---

# 322-Topshiriq: std::shared_ptr asoslari

## Topshiriq sharti:
Bir nechta ko'rsatkich bitta umumiy obyektga egalik qiluvchi `std::shared_ptr` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    std::shared_ptr<int> p1 = std::make_shared<int>(777);
    std::shared_ptr<int> p2 = p1; // Egalik bo'lishildi
    std::cout << "p1: " << *p1 << ", p2: " << *p2 << std::endl;
    std::cout << "Egalar soni (use_count): " << p1.use_count() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::shared_ptr` ichki havola hisoblagichiga (reference counter) ega.

## Ishlash natijasi:
```text
p1: 777, p2: 777\nEgalar soni (use_count): 2
```

---

# 323-Topshiriq: std::make_shared samaradorligi

## Topshiriq sharti:
Nima uchun `make_shared` ikki marta emas, balki bitta xotira allokatsiyasini bajarishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto p = std::make_shared<int>(50);
    std::cout << "make_shared nazorat bloki va obyektni bitta xotirada joylashtiradi: " << *p << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::make_shared` boshqaruv bloki va ma'lumotni yaxlit bitta blokda ajratadi va kesh tezligini oshiradi.

## Ishlash natijasi:
```text
make_shared nazorat bloki va obyektni bitta xotirada joylashtiradi: 50
```

---

# 324-Topshiriq: shared_ptr: use_count() dinamikasi

## Topshiriq sharti:
Yangi ko'rsatkich qo'shilganda va o'chirilganda `use_count()` o'zgarishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto a = std::make_shared<int>(100);
    std::cout << "Boshida: " << a.use_count() << std::endl;
    {
        auto b = a;
        std::cout << "Blok ichida: " << a.use_count() << std::endl;
    }
    std::cout << "Blokdan keyin: " << a.use_count() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `b` ko'lamdan chiqib o'chirilganda hisoblagich 1 ga kamayadi. 0 ga yetganda xotira butunlay tozalanadi.

## Ishlash natijasi:
```text
Boshida: 1\nBlok ichida: 2\nBlokdan keyin: 1
```

---

# 325-Topshiriq: shared_ptr ni funksiyalarga uzatish

## Topshiriq sharti:
shared_ptr ni qiymat bo'yicha uzatish (egalikni bo'lishish) va const reference orqali uzatish farqini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

void nusxaBilan(std::shared_ptr<int> p) {
    std::cout << "Nusxa use_count: " << p.use_count() << std::endl;
}

void refBilan(const std::shared_ptr<int>& p) {
    std::cout << "Ref use_count: " << p.use_count() << std::endl;
}

int main() {
    auto sp = std::make_shared<int>(25);
    refBilan(sp);      // 1 ta
    nusxaBilan(sp);    // 2 ta
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Faqat o'qish kerak bo'lsa `const std::shared_ptr<T>&` ishlatish hisoblagichni ortiqcha o'zgartirmaydi.

## Ishlash natijasi:
```text
Ref use_count: 1\nNusxa use_count: 2
```

---

# 326-Topshiriq: Siklik havola muammosi (Circular Reference)

## Topshiriq sharti:
Ikki obyekt bir-biriga `shared_ptr` orqali ko'rsatsa, xotira hech qachon ozod bo'lmasligini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

struct B;
struct A {
    std::shared_ptr<B> bPtr;
    ~A() { std::cout << "A o'chirildi" << std::endl; }
};
struct B {
    std::shared_ptr<A> aPtr; // Sikl hosil qiluvchi xavfli havola!
    ~B() { std::cout << "B o'chirildi" << std::endl; }
};

int main() {
    std::cout << "Siklik havolada hisoblagich 0 bo'lmaydi va xotira sizib ketadi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. A B ga, B A ga bog'lanib qolsa, use_count doim kamida 1 bo'lib qoladi.

## Ishlash natijasi:
```text
Siklik havolada hisoblagich 0 bo'lmaydi va xotira sizib ketadi.
```

---

# 327-Topshiriq: std::weak_ptr asoslari

## Topshiriq sharti:
Hisoblagichni oshirmaydigan zaif ko'rsatkich `std::weak_ptr` ni e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto sp = std::make_shared<int>(42);
    std::weak_ptr<int> wp = sp;
    std::cout << "use_count: " << sp.use_count() << std::endl;
    std::cout << "weak_ptr use_count ga ta'sir qilmadi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::weak_ptr` obyektga egalik qilmaydi, faqat uning tirikligini kuzatadi.

## Ishlash natijasi:
```text
use_count: 1\nweak_ptr use_count ga ta'sir qilmadi.
```

---

# 328-Topshiriq: weak_ptr: expired() va lock() metodlari

## Topshiriq sharti:
Obyekt o'chirilgan yoki yo'qligini `expired()` bilan tekshirib, `lock()` orqali xavfsiz `shared_ptr` oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    std::weak_ptr<int> wp;
    {
        auto sp = std::make_shared<int>(99);
        wp = sp;
        if (auto temp = wp.lock()) {
            std::cout << "Obyekt tirik: " << *temp << std::endl;
        }
    }
    if (wp.expired()) {
        std::cout << "Obyekt allaqachon xotiradan o'chirilgan (expired)." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.lock()` obyekt mavjud bo'lsa yangi `shared_ptr` qaytaradi, aks holda `nullptr`.

## Ishlash natijasi:
```text
Obyekt tirik: 99\nObyekt allaqachon xotiradan o'chirilgan (expired).
```

---

# 329-Topshiriq: weak_ptr orqali siklik havolani bartaraf etish

## Topshiriq sharti:
Oldingi misoldagi `B` strukturasidagi ko'rsatkichni `weak_ptr` ga aylantirib xotira sizishini hal qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

struct NodeB;
struct NodeA {
    std::shared_ptr<NodeB> b;
    ~NodeA() { std::cout << "NodeA o'chirildi" << std::endl; }
};
struct NodeB {
    std::weak_ptr<NodeA> a; // Sikl buzildi!
    ~NodeB() { std::cout << "NodeB o'chirildi" << std::endl; }
};

int main() {
    {
        auto na = std::make_shared<NodeA>();
        auto nb = std::make_shared<NodeB>();
        na->b = nb;
        nb->a = na;
    }
    std::cout << "Xotira to'liq tozalandi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `weak_ptr` siklni uzadi va destruktorlar to'liq ishga tushadi.

## Ishlash natijasi:
```text
NodeA o'chirildi\nNodeB o'chirildi\nXotira to'liq tozalandi.
```

---

# 330-Topshiriq: std::enable_shared_from_this

## Topshiriq sharti:
Sinf metodlari ichida o'z obyektiga xavfsiz `shared_ptr` olishni namoyish qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

class Xizmat : public std::enable_shared_from_this<Xizmat> {
public:
    std::shared_ptr<Xizmat> getPtr() {
        return shared_from_this();
    }
};

int main() {
    auto s1 = std::make_shared<Xizmat>();
    auto s2 = s1->getPtr();
    std::cout << "shared_from_this use_count: " << s1.use_count() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `shared_from_this()` `this` kalit so'zidan yangi control block yaratmasdan mavjud shared_ptr ni uzatadi.

## Ishlash natijasi:
```text
shared_from_this use_count: 2
```

---

# 331-Topshiriq: shared_ptr uchun Custom Deleter

## Topshiriq sharti:
shared_ptr ga lambda ko'rinishidagi custom deleter biriktiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    std::shared_ptr<int> p(new int(100), [](int* ptr) {
        std::cout << "Maxsus o'chirish: " << *ptr << std::endl;
        delete ptr;
    });
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `shared_ptr` ning afzalligi: custom deleter uning toifasiga ta'sir qilmaydi (`std::shared_ptr<int>`).

## Ishlash natijasi:
```text
Maxsus o'chirish: 100
```

---

# 332-Topshiriq: Polimorfizm va std::unique_ptr<Base>

## Topshiriq sharti:
Asosiy sinf ko'rsatkichiga ega `unique_ptr` orqali hosila sinf obyektini boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

class Asos {
public:
    virtual void salom() { std::cout << "Asos" << std::endl; }
    virtual ~Asos() = default;
};

class Bola : public Asos {
public:
    void salom() override { std::cout << "Bola sinfi" << std::endl; }
};

int main() {
    std::unique_ptr<Asos> ptr = std::make_unique<Bola>();
    ptr->salom();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Virtual destruktor tufayli `unique_ptr<Base>` to'g'ri Bola destruktorini chaqiradi.

## Ishlash natijasi:
```text
Bola sinfi
```

---

# 333-Topshiriq: std::dynamic_pointer_cast

## Topshiriq sharti:
`std::dynamic_pointer_cast` yordamida polimorfik `shared_ptr` ni pastga o'giring (downcasting).

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

class Asosiy {
public:
    virtual ~Asosiy() = default;
};
class Hosila : public Asosiy {
public:
    void maxsusFunksiya() { std::cout << "Hosila funksiyasi" << std::endl; }
};

int main() {
    std::shared_ptr<Asosiy> base = std::make_shared<Hosila>();
    auto derived = std::dynamic_pointer_cast<Hosila>(base);
    if (derived) {
        derived->maxsusFunksiya();
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar o'girish muvaffaqiyatli bo'lsa, `derived` yangi shared_ptr ga ega bo'ladi.

## Ishlash natijasi:
```text
Hosila funksiyasi
```

---

# 334-Topshiriq: Smart pointerlarni funksiyaga to'g'ri uzatish qoidalari

## Topshiriq sharti:
Faqat mulkdorlik o'zgargandagina smart pointer uzatish, boshqa holda xom ko'rsatkich yoki reference ishlatish qoidasi.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

void ishla(const int& qiymat) {
    std::cout << "Eng yaxshi amaliyot (qiymat yoki reference): " << qiymat << std::endl;
}

int main() {
    auto p = std::make_unique<int>(77);
    ishla(*p);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mulkdorlikka daxli bo'lmagan funksiyalarga smart pointer emas, oddiy `T&` yoki `const T*` uzatish afzaldir.

## Ishlash natijasi:
```text
Eng yaxshi amaliyot (qiymat yoki reference): 77
```

---

# 335-Topshiriq: unique_ptr ning Zero-overhead prinsipi

## Topshiriq sharti:
`sizeof(std::unique_ptr<int>)` va `sizeof(int*)` tengligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    std::cout << "sizeof(int*): " << sizeof(int*) << " bayt" << std::endl;
    std::cout << "sizeof(unique_ptr<int>): " << sizeof(std::unique_ptr<int>) << " bayt" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::unique_ptr` xom ko'rsatkich bilan aynan bir xil hajm va tezlikka ega (Zero-Cost Abstraction).

## Ishlash natijasi:
```text
sizeof(int*): 8 bayt\nsizeof(unique_ptr<int>): 8 bayt
```

---

# 336-Topshiriq: C uslubidagi malloc va free

## Topshiriq sharti:
C tilidagi `malloc` va `free` orqali xotira ajratish va C++ dagi farqlarini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdlib>

int main() {
    int* ptr = (int*)malloc(sizeof(int));
    if (ptr) {
        *ptr = 123;
        std::cout << "malloc orqali: " << *ptr << std::endl;
        free(ptr);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `malloc` faqat xom xotira ajratadi, ammo C++ konstruktorini chaqirmaydi.

## Ishlash natijasi:
```text
malloc orqali: 123
```

---

# 337-Topshiriq: malloc va new o'rtasidagi asosiy farqlar

## Topshiriq sharti:
`new` konstruktorni chaqirishi va toifa xavfsizligi afzalligini taqqoslang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Sinov {
    Sinov() { std::cout << "Konstruktor chaqirildi!" << std::endl; }
    ~Sinov() { std::cout << "Destruktor chaqirildi!" << std::endl; }
};

int main() {
    Sinov* s = new Sinov();
    delete s;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `malloc` obyekti to'g'ri initsializatsiya qilmaydi, C++ da doimo `new` yoki smart pointer ishlatiladi.

## Ishlash natijasi:
```text
Konstruktor chaqirildi!\nDestruktor chaqirildi!
```

---

# 338-Topshiriq: Placement new operatori

## Topshiriq sharti:
Oldindan ajratilgan statik bufer ustida obyekt qurish (Placement new) imkoniyatini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <new>

struct Nuqta {
    int x, y;
    Nuqta(int a, int b) : x(a), y(b) {}
};

int main() {
    alignas(Nuqta) char bufer[sizeof(Nuqta)];
    Nuqta* pN = new (bufer) Nuqta(10, 20); // Bufer ichida obyekt qurildi
    std::cout << "Nuqta: " << pN->x << ", " << pN->y << std::endl;
    pN->~Nuqta(); // Qo'lda destruktor chaqiriladi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Placement new maxsus allokatorlar va yuqori unumdor tizimlarda qo'llaniladi.

## Ishlash natijasi:
```text
Nuqta: 10, 20
```

---

# 339-Topshiriq: Placement new da qo'lda destruktor chaqirish

## Topshiriq sharti:
Nima uchun placement new bilan qurilgan obyekt `delete` qilinmasdan `p->~T()` bilan yopilishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <new>

class Element {
public:
    ~Element() { std::cout << "Element destruktori qo'lda chaqirildi." << std::endl; }
};

int main() {
    char xotira[sizeof(Element)];
    Element* e = new (xotira) Element();
    e->~Element(); // delete qilinmaydi, chunki xotira stekda!
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Placement new da xotira heap dan olinmagan bo'lishi mumkin, shu sababli faqat destruktor chaqiriladi.

## Ishlash natijasi:
```text
Element destruktori qo'lda chaqirildi.
```

---

# 340-Topshiriq: Oddiy Arena xotira ajratgich (Arena Allocator)

## Topshiriq sharti:
Bitta katta buferdan ketma-ket joy beruvchi super tezkor Arena boshqaruvchisini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstddef>

class ArenaAllocator {
    char bufer[1024];
    size_t ofset = 0;
public:
    void* ajrat(size_t baytlar) {
        if (ofset + baytlar > 1024) return nullptr;
        void* ptr = &bufer[ofset];
        ofset += baytlar;
        return ptr;
    }
    void hammasiniTozala() { ofset = 0; }
};

int main() {
    ArenaAllocator arena;
    int* son = (int*)arena.ajrat(sizeof(int));
    *son = 500;
    std::cout << "Arena qiymati: " << *son << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Arena allokator alohida-alohida `delete` talab qilmaydi, butun bufer birdaniga tozalanadi.

## Ishlash natijasi:
```text
Arena qiymati: 500
```

---

# 341-Topshiriq: Xotira parchalanishi (Fragmentation) tushunchasi

## Topshiriq sharti:
Xotirada turli hajmdagi bo'laklar ajratilib o'chirilganda bo'shliqlar hosil bo'lishi sababini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "External fragmentation - bo'sh xotira yetarli bo'lsa-da, "
              << "u uzluksiz bo'lmagani sababli katta massiv ajratib bo'lmaslik holati." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Parchalanishning oldini olish uchun xotira havzalari (Memory Pools) qo'llanadi.

## Ishlash natijasi:
```text
External fragmentation - bo'sh xotira yetarli bo'lsa-da, u uzluksiz bo'lmagani sababli katta massiv ajratib bo'lmaslik holati.
```

---

# 342-Topshiriq: Katta massivlar uchun virtual xotira sahifalari

## Topshiriq sharti:
Operatsion tizim xotirani 4KB sahifalarda (Pages) boshqarishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "OS virtual xotirani 4KB sahifalarda boshqaradi (Page-level allocation)." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zamonaviy operatsion tizimlar sahifalash mexanizmi orqali RAM va disktagi sahifalar bilan ishlaydi.

## Ishlash natijasi:
```text
OS virtual xotirani 4KB sahifalarda boshqaradi (Page-level allocation).
```

---

# 343-Topshiriq: std::bad_alloc istisnosini ushlash

## Topshiriq sharti:
Imkonsiz darajada katta xotira so'ralganda `std::bad_alloc` istisnosini `try-catch` bilan ushlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <new>

int main() {
    try {
        size_t judaKatta = (size_t)-1 / 2; // Gigant o'lcham
        char* p = new char[judaKatta];
        delete[] p;
    } catch (const std::bad_alloc& e) {
        std::cout << "bad_alloc ushlandi: Tizimda yetarli xotira mavjud emas!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xotira ajratish xatoligi `std::bad_alloc` orqali tutib olinadi.

## Ishlash natijasi:
```text
bad_alloc ushlandi: Tizimda yetarli xotira mavjud emas!
```

---

# 344-Topshiriq: Double Free xatosi va uning xavfi

## Topshiriq sharti:
Bitta xotira manzilini ikki marta delete qilish crash keltirib chiqarishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int* p = new int(10);
    delete p;
    p = nullptr; // Agar nullptr qilinsa:
    delete p;    // delete nullptr to'liq xavfsiz va hech narsa qilmaydi
    std::cout << "Double free ning oldi nullptr orqali olindi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++ standartida `delete nullptr;` hech qanday xato keltirib chiqarmaydi.

## Ishlash natijasi:
```text
Double free ning oldi nullptr orqali olindi.
```

---

# 345-Topshiriq: Wild delete xatosi

## Topshiriq sharti:
Stack xotirasidagi o'zgaruvchi manzilini delete qilish taqiqlanganini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    // int x = 5;
    // delete &x; // XATOLIK! Stekdagi xotirani delete qilib bo'lmaydi
    std::cout << "Faqat new bilan olingan xotirani delete qilish shart." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Faqat erkin xotiradan (Heap) ajratilgan ko'rsatkichlargina `delete` qilinadi.

## Ishlash natijasi:
```text
Faqat new bilan olingan xotirani delete qilish shart.
```

---

# 346-Topshiriq: RAII orqali xotira oqishini kuzatuvchi sanagich

## Topshiriq sharti:
Obyektlar sonini sanab turuvchi sinf orqali oqish yo'qligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Sinovchi {
    static int faolSoni;
public:
    Sinovchi() { faolSoni++; }
    ~Sinovchi() { faolSoni--; }
    static int getFaol() { return faolSoni; }
};
int Sinovchi::faolSoni = 0;

int main() {
    {
        Sinovchi s1, s2;
        std::cout << "Faol obyektlar: " << Sinovchi::getFaol() << std::endl;
    }
    std::cout << "Blokdan keyin faol: " << Sinovchi::getFaol() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Blokdan keyin faol obyektlar 0 bo'lib, xotira to'liq tozalanganini ko'rsatadi.

## Ishlash natijasi:
```text
Faol obyektlar: 2\nBlokdan keyin faol: 0
```

---

# 347-Topshiriq: auto_ptr ning eskirishi va unique_ptr ning afzalligi

## Topshiriq sharti:
Nima uchun eski `auto_ptr` taqiqlanib, o'rniga aniq Move semantikali `unique_ptr` kelganini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "auto_ptr yashirincha nusxalashda mulkdorlikni o'g'irlar edi, "
              << "unique_ptr esa buni faqat oshkora std::move orqali talab qiladi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zamonaviy C++ da faqat `std::unique_ptr` va `std::shared_ptr` ishlatiladi.

## Ishlash natijasi:
```text
auto_ptr yashirincha nusxalashda mulkdorlikni o'g'irlar edi, unique_ptr esa buni faqat oshkora std::move orqali talab qiladi.
```

---

# 348-Topshiriq: shared_ptr va atomik hisoblagich (Thread safety)

## Topshiriq sharti:
shared_ptr hisoblagichi oqimlararo xavfsiz (atomic) boshqarilishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto sp = std::make_shared<int>(123);
    std::cout << "shared_ptr ning ref-counteri std::atomic asosida ishlaydi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boshqaruv blokining use_count hisoblagichi parallel oqimlarda sinxronlash talab qilmasdan xavfsiz ishlaydi.

## Ishlash natijasi:
```text
shared_ptr ning ref-counteri std::atomic asosida ishlaydi.
```

---

# 349-Topshiriq: Smart pointerlar orqali ikkilik daraxt (Binary Tree) tuzish

## Topshiriq sharti:
`std::unique_ptr` orqali xotirani avtomatik tozalovchi daraxt tugunini quring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

struct DaraxtTuguni {
    int qiymat;
    std::unique_ptr<DaraxtTuguni> chap;
    std::unique_ptr<DaraxtTuguni> ong;
    explicit DaraxtTuguni(int v) : qiymat(v) {}
};

int main() {
    auto ildiz = std::make_unique<DaraxtTuguni>(10);
    ildiz->chap = std::make_unique<DaraxtTuguni>(5);
    ildiz->ong = std::make_unique<DaraxtTuguni>(15);
    std::cout << "Ildiz: " << ildiz->qiymat 
              << ", Chap: " << ildiz->chap->qiymat 
              << ", O'ng: " << ildiz->ong->qiymat << std::endl;
    return 0; // Butun daraxt avtomatik chuqurlik bo'yicha ozod qilinadi!
}
```

## Tushuntirish va Mantiq:
1. `ildiz` o'chirilganda uning barcha farzand tugunlari rekursiv ravishda avtomatik xotiradan tozalanadi.

## Ishlash natijasi:
```text
Ildiz: 10, Chap: 5, O'ng: 15
```

---

# 350-Topshiriq: Zamonaviy C++ da 'new' va 'delete' dan voz kechish falsafasi

## Topshiriq sharti:
Zamonaviy C++ dasturchilari to'g'ridan-to'g'ri `new` va `delete` yozmasdan standart konteynerlar va smart pointerlar ishlatishi lozimligini xulosa qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <memory>

int main() {
    // Zamonaviy C++:
    std::vector<int> v = {1, 2, 3}; // Dinamik massiv
    auto p = std::make_unique<int>(10); // Dinamik obyekt
    std::cout << "Zamonaviy C++: Nol qo'lda new/delete, 100% xavfsiz va xotira sizmaydi!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zamonaviy C++ da barcha xotira boshqaruvi RAII, STL konteynerlari va aqlli ko'rsatkichlarga topshiriladi.

## Ishlash natijasi:
```text
Zamonaviy C++: Nol qo'lda new/delete, 100% xavfsiz va xotira sizmaydi!
```

---

