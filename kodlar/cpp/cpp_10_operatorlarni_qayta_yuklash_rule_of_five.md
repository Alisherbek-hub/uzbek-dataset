# C++ Dasturlash Tili - 10-Qism: Operatorlarni Qayta Yuklash va Beshlik Qoidasi (Rule of Five)

Ushbu qismda operator overloading, spaceship operator <=>, stream I/O, Rule of Three/Five/Zero, Move semantikasi, std::move, rvalue havolalar va custom literallarga oid 50 ta amaliy topshiriq jamlangan.

---

# 451-Topshiriq: Operatorlarni qayta yuklash (Operator Overloading) asoslari

## Topshiriq sharti:
Ikki nuqta koordinatalarini qo'shuvchi `operator+` metodini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Nuqta {
public:
    int x, y;
    Nuqta(int a = 0, int b = 0) : x(a), y(b) {}
    Nuqta operator+(const Nuqta& boshqa) const {
        return Nuqta(x + boshqa.x, y + boshqa.y);
    }
};

int main() {
    Nuqta p1(2, 3), p2(4, 5);
    Nuqta p3 = p1 + p2;
    std::cout << "p3: (" << p3.x << ", " << p3.y << ")" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `operator+` obyektdan yangi yig'indi nusxasini qaytaradi va tabiiy arifmetik sintaksis beradi.

## Ishlash natijasi:
```text
p3: (6, 8)
```

---

# 452-Topshiriq: Binar ayirish va ko'paytirish (operator-, operator*)

## Topshiriq sharti:
Vektor koordinatalari uchun ayirish va skalyarga ko'paytirish operatorlarini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Vektor2D {
public:
    double x, y;
    Vektor2D(double a, double b) : x(a), y(b) {}
    Vektor2D operator-(const Vektor2D& v) const { return Vektor2D(x - v.x, y - v.y); }
    Vektor2D operator*(double skalyar) const { return Vektor2D(x * skalyar, y * skalyar); }
};

int main() {
    Vektor2D v1(10, 8), v2(3, 2);
    Vektor2D ayirma = v1 - v2;
    Vektor2D kopaytma = ayirma * 2.0;
    std::cout << "Kopaytma: (" << kopaytma.x << ", " << kopaytma.y << ")" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Operatorlar orqali vektorlar ustida matematik amallar qulay bajariladi.

## Ishlash natijasi:
```text
Kopaytma: (14, 12)
```

---

# 453-Topshiriq: Unar minus operatori (-obj)

## Topshiriq sharti:
Obyekt qiymatlarini qarama-qarshisiga o'zgartiruvchi unar `-` operatorini yuklang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Son {
public:
    int val;
    Son(int v) : val(v) {}
    Son operator-() const {
        return Son(-val);
    }
};

int main() {
    Son s(25);
    Son manfiy = -s;
    std::cout << "Asl: " << s.val << ", Manfiy: " << manfiy.val << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Unar minus argument qabul qilmaydi va obyekt koordinatalarini teskari ishoraga aylantiradi.

## Ishlash natijasi:
```text
Asl: 25, Manfiy: -25
```

---

# 454-Topshiriq: Prefiks va Postfiks inkrement (++obj va obj++)

## Topshiriq sharti:
Prefiks va postfiks `++` operatorlari orasidagi farqni (dummy `int` parametri) ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Sanagich {
public:
    int son;
    Sanagich(int s = 0) : son(s) {}
    // Prefiks: ++obj
    Sanagich& operator++() {
        ++son;
        return *this;
    }
    // Postfiks: obj++
    Sanagich operator++(int) {
        Sanagich eski = *this;
        ++son;
        return eski;
    }
};

int main() {
    Sanagich c(5);
    ++c;
    std::cout << "Prefiks keyin: " << c.son << std::endl;
    Sanagich oldingi = c++;
    std::cout << "Postfiks qaytargan: " << oldingi.son << ", Hozirgi: " << c.son << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Postfiks `operator++(int)` eski nusxani qaytaradi, shu bois prefiks `++c` nisbatan tezroq ishlaydi.

## Ishlash natijasi:
```text
Prefiks keyin: 6\nPostfiks qaytargan: 6, Hozirgi: 7
```

---

# 455-Topshiriq: Taqqoslash operatorlari (operator== va operator!=)

## Topshiriq sharti:
Ikki obyektning tengligi va tengsizligini tekshiruvchi operatorlarni yuklang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

class Mahsulot {
public:
    int id;
    std::string nom;
    Mahsulot(int i, std::string n) : id(i), nom(n) {}
    bool operator==(const Mahsulot& b) const { return id == b.id; }
    bool operator!=(const Mahsulot& b) const { return !(*this == b); }
};

int main() {
    Mahsulot m1(1, "Noutbuk"), m2(1, "Laptop"), m3(2, "Sichqoncha");
    std::cout << "m1 == m2: " << (m1 == m2 ? "Teng" : "Farqli") << std::endl;
    std::cout << "m1 != m3: " << (m1 != m3 ? "Farqli" : "Teng") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `!=` operatori `==` operatorini inkor qilish orqali ixcham yoziladi.

## Ishlash natijasi:
```text
m1 == m2: Teng\nm1 != m3: Farqli
```

---

# 456-Topshiriq: Katta va kichik taqqoslash (operator<)

## Topshiriq sharti:
STL konteynerlari va saralash (`std::sort`) ishlashi uchun `operator<` ni aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

class Talaba {
public:
    int ball;
    Talaba(int b) : ball(b) {}
    bool operator<(const Talaba& b) const { return ball < b.ball; }
};

int main() {
    std::vector<Talaba> guruh = {Talaba(90), Talaba(75), Talaba(85)};
    std::sort(guruh.begin(), guruh.end());
    for (const auto& t : guruh) std::cout << t.ball << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `operator<` obyektlar uchun tabiiy tartibni (Strict Weak Ordering) o'rnatadi.

## Ishlash natijasi:
```text
75 85 90 
```

---

# 457-Topshiriq: C++20 Uch tomonlama taqqoslash (Spaceship Operator <=>)

## Topshiriq sharti:
C++20 ning `<=>` operatori orqali barcha 6 ta taqqoslashni bitta qatorda ta'minlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <compare>

class Nuqta1D {
public:
    int x;
    Nuqta1D(int val) : x(val) {}
    auto operator<=>(const Nuqta1D&) const = default;
};

int main() {
    Nuqta1D a(10), b(20);
    std::cout << "a < b: " << (a < b) << std::endl;
    std::cout << "a == b: " << (a == b) << std::endl;
    std::cout << "a >= b: " << (a >= b) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `auto operator<=>(...) = default;` barcha a'zolar bo'yicha avtomatik `<, <=, ==, !=, >, >=` ni hosil qiladi.

## Ishlash natijasi:
```text
a < b: 1\na == b: 0\na >= b: 0
```

---

# 458-Topshiriq: Oqimga chiqarish operatori (operator<< friend)

## Topshiriq sharti:
`std::cout << obj` sintaksisini ta'minlovchi `operator<<` ni friend orqali yuklang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Kompleks {
    double re, im;
public:
    Kompleks(double r, double i) : re(r), im(i) {}
    friend std::ostream& operator<<(std::ostream& os, const Kompleks& k) {
        os << k.re << " + " << k.im << "i";
        return os;
    }
};

int main() {
    Kompleks c(4.5, 2.5);
    std::cout << "Kompleks son: " << c << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::ostream&` qaytarilishi bir nechta chiqarishni zanjir (`cout << a << b`) qilish imkonini beradi.

## Ishlash natijasi:
```text
Kompleks son: 4.5 + 2.5i
```

---

# 459-Topshiriq: Oqimdan o'qish operatori (operator>> friend)

## Topshiriq sharti:
`std::cin >> obj` orqali obyekt maydonlarini kiritish operatorini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <sstream>

class Koordinata {
public:
    int x, y;
    friend std::istream& operator>>(std::istream& is, Koordinata& k) {
        is >> k.x >> k.y;
        return is;
    }
};

int main() {
    std::stringstream kirish("15 25");
    Koordinata k;
    kirish >> k;
    std::cout << "O'qilgan: x=" << k.x << ", y=" << k.y << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `operator>>` kiruvchi oqimdan ma'lumotlarni o'qib obyekt maydonlariga joylaydi.

## Ishlash natijasi:
```text
O'qilgan: x=15, y=25
```

---

# 460-Topshiriq: Indekslash operatori (operator[])

## Topshiriq sharti:
Konteyner sinfiga massiv kabi murojaat qilish imkonini beruvchi oddiy va const `operator[]` ni yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class ButunMassiv {
    int data[5] = {10, 20, 30, 40, 50};
public:
    int& operator[](size_t i) { return data[i]; }
    const int& operator[](size_t i) const { return data[i]; }
};

int main() {
    ButunMassiv m;
    m[2] = 99; // O'zgartirish
    std::cout << "m[2] = " << m[2] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int&` qaytarsa elementni o'zgartirish mumkin, `const int&` esa const obyektlar uchun xizmat qiladi.

## Ishlash natijasi:
```text
m[2] = 99
```

---

# 461-Topshiriq: Funksiya chaqiruvi operatori (operator()) va Funktor

## Topshiriq sharti:
Sinf obyektini funksiya kabi chaqirishni amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class ChiziqliFunksiya {
    double k, b;
public:
    ChiziqliFunksiya(double k_, double b_) : k(k_), b(b_) {}
    double operator()(double x) const {
        return k * x + b;
    }
};

int main() {
    ChiziqliFunksiya f(2.0, 3.0); // y = 2x + 3
    std::cout << "f(5) = " << f(5.0) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `operator()` obyektlarni algoritmlarga (masalan `std::transform`) uzatishda juda qulay.

## Ishlash natijasi:
```text
f(5) = 13
```

---

# 462-Topshiriq: O'q operatori (operator-> va operator*)

## Topshiriq sharti:
Smart pointer kabi ishlovchi wrapper sinfida `->` va `*` ni yuklang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Model {
    void xulosa() { std::cout << "1-Bit AI Model xulosasi tayyor." << std::endl; }
};

class ModelOrami {
    Model* ptr;
public:
    ModelOrami(Model* p) : ptr(p) {}
    ~ModelOrami() { delete ptr; }
    Model& operator*() { return *ptr; }
    Model* operator->() { return ptr; }
};

int main() {
    ModelOrami m(new Model());
    m->xulosa();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `operator->` smart ko'rsatkichlarga xuddi asl obyektdek murojaat qilish imkonini beradi.

## Ishlash natijasi:
```text
1-Bit AI Model xulosasi tayyor.
```

---

# 463-Topshiriq: O'zlashtirish operatori (Copy Assignment Operator)

## Topshiriq sharti:
O'ziga-o'zi tenglashtirish (self-assignment `this != &other`) dan himoyalangan `operator=` yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Resurs {
    int* val;
public:
    Resurs(int v = 0) : val(new int(v)) {}
    ~Resurs() { delete val; }
    Resurs& operator=(const Resurs& other) {
        if (this != &other) { // Self-assignment tekshiruvi
            delete val;
            val = new int(*other.val);
        }
        return *this;
    }
    int get() const { return *val; }
};

int main() {
    Resurs r1(50), r2(80);
    r1 = r2;
    std::cout << "r1: " << r1.get() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `if (this != &other)` obyekti o'ziga tenglashtirilganda uning xotirasi bevaqt o'chib ketishining oldini oladi.

## Ishlash natijasi:
```text
r1: 80
```

---

# 464-Topshiriq: Birikmali o'zlashtirish operatorlari (operator+=)

## Topshiriq sharti:
`operator+=` orqali obyektning o'zini o'zgartirib, havola qaytarishni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Balans {
public:
    double summa;
    Balans(double s = 0) : summa(s) {}
    Balans& operator+=(const Balans& b) {
        summa += b.summa;
        return *this;
    }
};

int main() {
    Balans b1(100), b2(50);
    b1 += b2;
    std::cout << "Balans: " << b1.summa << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `+=` yangi nusxa yaratmasdan to'g'ridan-to'g'ri joriy obyektni o'zgartiradi.

## Ishlash natijasi:
```text
Balans: 150
```

---

# 465-Topshiriq: Toifa o'girish operatori (Type Conversion Operator: operator int())

## Topshiriq sharti:
Obyektni avtomatik yoki oshkora butun songa aylantiruvchi operator yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class MasofaMetr {
    int metr;
public:
    MasofaMetr(int m) : metr(m) {}
    operator int() const {
        return metr;
    }
};

int main() {
    MasofaMetr masofa(150);
    int m = masofa; // Avtomatik int ga aylandi
    std::cout << "Metr: " << m << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `operator T()` qaytarish toifasiga ega bo'lmaydi, chunki uning nomi maqsadli turdan iborat.

## Ishlash natijasi:
```text
Metr: 150
```

---

# 466-Topshiriq: explicit operator bool()

## Topshiriq sharti:
Obyektni `if (obj)` shartlarida xavfsiz tekshirish uchun `explicit operator bool()` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class FaylHolati {
    bool ochiq;
public:
    FaylHolati(bool o) : ochiq(o) {}
    explicit operator bool() const {
        return ochiq;
    }
};

int main() {
    FaylHolati f(true);
    if (f) {
        std::cout << "Fayl ochiq va tayyor." << std::endl;
    }
    // int x = f; // explicit tufayli xato! Tasodifiy songa aylanmaydi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `explicit operator bool()` obyektning mantiqiy ifodalarda xavfsiz qatnashishini ta'minlaydi.

## Ishlash natijasi:
```text
Fayl ochiq va tayyor.
```

---

# 467-Topshiriq: Rule of Three (3 qoidasi) asoslari

## Topshiriq sharti:
Agar sinf Destruktor talab qilsa, unga Copy Constructor va Copy Assignment ham shart ekanligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class TrioSinf {
    int* ptr;
public:
    TrioSinf(int v) : ptr(new int(v)) {}
    // 1. Destruktor
    ~TrioSinf() { delete ptr; }
    // 2. Nusxa konstruktori
    TrioSinf(const TrioSinf& other) : ptr(new int(*other.ptr)) {}
    // 3. Nusxa o'zlashtirish
    TrioSinf& operator=(const TrioSinf& other) {
        if (this != &other) {
            delete ptr;
            ptr = new int(*other.ptr);
        }
        return *this;
    }
    int get() const { return *ptr; }
};

int main() {
    TrioSinf a(10);
    TrioSinf b = a;
    TrioSinf c(20);
    c = b;
    std::cout << "Hammasi chuqur nusxalandi: " << c.get() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Rule of Three xotira sizishi va ikki marta o'chirish falokatlaridan to'liq himoyalaydi.

## Ishlash natijasi:
```text
Hammasi chuqur nusxalandi: 10
```

---

# 468-Topshiriq: Rvalue havola (T&&) va Lvalue havola (T&)

## Topshiriq sharti:
Nomi bor o'zgaruvchilar (lvalue) va vaqtinchalik ifodalar (rvalue) farqini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void tekshir(int& lval) {
    std::cout << "Lvalue havola: " << lval << std::endl;
}

void tekshir(int&& rval) {
    std::cout << "Rvalue havola: " << rval << std::endl;
}

int main() {
    int x = 100;
    tekshir(x);   // Lvalue
    tekshir(200); // Rvalue (vaqtinchalik qiymat)
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `T&&` vaqtinchalik obyektlarni tutib olish va ularning resurslarini ko'chirish (Move) imkonini beradi.

## Ishlash natijasi:
```text
Lvalue havola: 100\nRvalue havola: 200
```

---

# 469-Topshiriq: std::move ning mohiyati

## Topshiriq sharti:
`std::move` obyektni lvalue dan rvalue ga aylantirishini (unconditional cast) tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <utility>

void test(int&& x) {
    std::cout << "rvalue sifatida qabul qilindi: " << x << std::endl;
}

int main() {
    int son = 77;
    // test(son); // Xato: lvalue rvalue havolaga o'tmaydi
    test(std::move(son)); // std::move rvalue ga aylantiradi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::move` hech qanday kod bajarmaydi, faqat kompilyator uchun ko'chirish ruxsatini bildiradi.

## Ishlash natijasi:
```text
rvalue sifatida qabul qilindi: 77
```

---

# 470-Topshiriq: Ko'chirish konstruktori (Move Constructor)

## Topshiriq sharti:
Vaqtinchalik obyektdan ko'rsatkichni olib, uni `nullptr` qilish orqali xotira nusxalamasdan o'tkazing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class KattaBuffer {
public:
    int* data;
    int size;
    KattaBuffer(int s) : size(s), data(new int[s]) {}
    ~KattaBuffer() { delete[] data; }
    // Move konstruktor:
    KattaBuffer(KattaBuffer&& other) noexcept : data(other.data), size(other.size) {
        other.data = nullptr; // Resurs o'g'irlandi, eskisi bo'shatildi
        other.size = 0;
        std::cout << "Move konstruktor ishladi!" << std::endl;
    }
};

int main() {
    KattaBuffer b1(1000);
    KattaBuffer b2 = std::move(b1); // Xotira qayta ajratilmadi, faqat ko'rsatkich surildi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Move konstruktor katta hajmdagi xotirani 0 vaqtda (O(1)) ko'chirib beradi.

## Ishlash natijasi:
```text
Move konstruktor ishladi!
```

---

# 471-Topshiriq: Ko'chirish o'zlashtirish operatori (Move Assignment Operator)

## Topshiriq sharti:
Mavjud resursni tozalab, rvalue obyekt resursini ko'chirib oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class DinamikMatn {
public:
    char* str;
    DinamikMatn() : str(nullptr) {}
    DinamikMatn(DinamikMatn&& other) noexcept : str(other.str) { other.str = nullptr; }
    DinamikMatn& operator=(DinamikMatn&& other) noexcept {
        if (this != &other) {
            delete[] str;
            str = other.str;
            other.str = nullptr;
        }
        return *this;
    }
    ~DinamikMatn() { delete[] str; }
};

int main() {
    DinamikMatn d1;
    d1 = DinamikMatn(); // Move assignment
    std::cout << "Move assignment muvaffaqiyatli bajarildi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Move assignment vaqtinchalik obyektlar bilan ishlashda unumdorlikni keskin oshiradi.

## Ishlash natijasi:
```text
Move assignment muvaffaqiyatli bajarildi.
```

---

# 472-Topshiriq: Rule of Five (5 qoidasi) to'liq namunasi

## Topshiriq sharti:
Destruktor, Copy Ctor, Copy Assign, Move Ctor, Move Assign barchasini to'liq yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class BeshlikSinf {
    int* ptr;
public:
    BeshlikSinf(int val) : ptr(new int(val)) {}
    // 1. Destruktor
    ~BeshlikSinf() { delete ptr; }
    // 2. Copy Constructor
    BeshlikSinf(const BeshlikSinf& o) : ptr(new int(*o.ptr)) {}
    // 3. Copy Assignment
    BeshlikSinf& operator=(const BeshlikSinf& o) {
        if (this != &o) { delete ptr; ptr = new int(*o.ptr); }
        return *this;
    }
    // 4. Move Constructor
    BeshlikSinf(BeshlikSinf&& o) noexcept : ptr(o.ptr) { o.ptr = nullptr; }
    // 5. Move Assignment
    BeshlikSinf& operator=(BeshlikSinf&& o) noexcept {
        if (this != &o) { delete ptr; ptr = o.ptr; o.ptr = nullptr; }
        return *this;
    }
};

int main() {
    BeshlikSinf a(100);
    BeshlikSinf b = std::move(a);
    std::cout << "Rule of Five to'liq amalga oshirildi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dinamik resurs boshqaruvchi zamonaviy sinflar uchun Rule of Five oltin standartdir.

## Ishlash natijasi:
```text
Rule of Five to'liq amalga oshirildi.
```

---

# 473-Topshiriq: Rule of Zero (0 qoidasi)

## Topshiriq sharti:
Standart kutubxona sinflari (`std::string`, `std::vector`) ishlatilganda birorta ham maxsus metod yozish shart emasligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <vector>

class NolQoidasi {
public:
    std::string nom;
    std::vector<int> baholar;
    // Hech qanday destruktor yoki copy/move yozilmaydi!
};

int main() {
    NolQoidasi n1{"Olim", {5, 5, 4}};
    NolQoidasi n2 = std::move(n1); // Standart kutubxona avtomatik xavfsiz boshqaradi
    std::cout << "Rule of Zero: Kod toza va 100% xavfsiz!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Rule of Zero eng yaxshi amaliyot hisoblanadi: qo'lda ko'rsatkich boshqarmang, STL ga ishoning.

## Ishlash natijasi:
```text
Rule of Zero: Kod toza va 100% xavfsiz!
```

---

# 474-Topshiriq: Copy-and-Swap idiomasi

## Topshiriq sharti:
`std::swap` yordamida nusxalash va ko'chirishni bitta qisqa `operator=` da birlashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <utility>

class SwapSinf {
    int* ptr;
public:
    SwapSinf(int v) : ptr(new int(v)) {}
    ~SwapSinf() { delete ptr; }
    SwapSinf(const SwapSinf& other) : ptr(new int(*other.ptr)) {}
    // Copy-and-Swap: qiymat bo'yicha qabul qilib almashtiriladi
    SwapSinf& operator=(SwapSinf other) noexcept {
        std::swap(ptr, other.ptr);
        return *this;
    }
    int get() const { return *ptr; }
};

int main() {
    SwapSinf s1(10), s2(20);
    s1 = s2;
    std::cout << "s1 qiymati: " << s1.get() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Copy-and-Swap kodi ixcham, o'z-o'ziga tenglashtirishga tabiiy chidamli va kuchli istisno kafolatini beradi.

## Ishlash natijasi:
```text
s1 qiymati: 20
```

---

# 475-Topshiriq: std::exchange (C++14)

## Topshiriq sharti:
`std::exchange` yordamida eski qiymatni qaytarib yangi qiymat yuklashni Move amallarida qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <utility>

class ResursX {
    int* p;
public:
    ResursX(int v) : p(new int(v)) {}
    ~ResursX() { delete p; }
    // std::exchange orqali bitta qatorda ko'chirish:
    ResursX(ResursX&& o) noexcept : p(std::exchange(o.p, nullptr)) {}
    int get() const { return p ? *p : 0; }
};

int main() {
    ResursX r1(42);
    ResursX r2 = std::move(r1);
    std::cout << "r2: " << r2.get() << ", r1: " << r1.get() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::exchange(o.p, nullptr)` manzilni oladi va `o.p` ni darhol `nullptr` qiladi.

## Ishlash natijasi:
```text
r2: 42, r1: 0
```

---

# 476-Topshiriq: Noexcept Move Constructor zarurati

## Topshiriq sharti:
Move konstruktor `noexcept` bo'lmasa `std::vector` qayta o'lchamda ko'chirish o'rniga sekin nusxalashga o'tib ketishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class Sinov {
public:
    Sinov() = default;
    Sinov(const Sinov&) { std::cout << "Copy\n"; }
    Sinov(Sinov&&) noexcept { std::cout << "Move (noexcept)\n"; }
};

int main() {
    std::vector<Sinov> v;
    v.reserve(1);
    v.emplace_back();
    std::cout << "Qayta allokatsiya:\n";
    v.reserve(2); // noexcept bo'lgani uchun Move chaqiriladi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `noexcept` bo'lmasa vektor istisno yuz berganda ma'lumot yo'qolmasligi uchun xavfsiz nusxalashni ishlatadi.

## Ishlash natijasi:
```text
Qayta allokatsiya:\nMove (noexcept)
```

---

# 477-Topshiriq: Ref-qualifiers (& va && metod oxirida)

## Topshiriq sharti:
Obyekt lvalue yoki rvalue bo'lishiga qarab turli metodlarni ishga tushirish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class MatnQutisi {
public:
    void chop() & { std::cout << "Lvalue obyektda chaqirildi\n"; }
    void chop() && { std::cout << "Rvalue (vaqtinchalik) obyektda chaqirildi\n"; }
};

int main() {
    MatnQutisi quti;
    quti.chop();          // &
    MatnQutisi().chop();  // &&
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ref-qualifiers vaqtinchalik obyektlardan ma'lumotlarni o'g'irlash (move) imkoniyatini metod darajasiga beradi.

## Ishlash natijasi:
```text
Lvalue obyektda chaqirildi\nRvalue (vaqtinchalik) obyektda chaqirildi
```

---

# 478-Topshiriq: Move-only sinflar (Nusxalanmaydigan, faqat ko'chuvchi)

## Topshiriq sharti:
Nusxalash taqiqlangan (`= delete`), faqat ko'chirish mumkin bo'lgan fayl boshqaruvchisini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class FaqatKochuvchi {
public:
    int id;
    FaqatKochuvchi(int i) : id(i) {}
    FaqatKochuvchi(const FaqatKochuvchi&) = delete;
    FaqatKochuvchi& operator=(const FaqatKochuvchi&) = delete;
    FaqatKochuvchi(FaqatKochuvchi&&) noexcept = default;
    FaqatKochuvchi& operator=(FaqatKochuvchi&&) noexcept = default;
};

int main() {
    FaqatKochuvchi a(10);
    // FaqatKochuvchi b = a; // Xato! Nusxalash yo'q
    FaqatKochuvchi c = std::move(a); // Ruxsat etilgan
    std::cout << "Move-only obyekt ID: " << c.id << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::unique_ptr` va `std::thread` aynan shu Move-only tamoyilida qurilgan.

## Ishlash natijasi:
```text
Move-only obyekt ID: 10
```

---

# 479-Topshiriq: User-Defined Literals (operator""_km)

## Topshiriq sharti:
Maxsus literal orqali masofani metrlarda ifodalash.

## Yechim (C++ kodi):
```cpp
#include <iostream>

long double operator"" _km(long double km) {
    return km * 1000.0;
}

int main() {
    auto masofaMetrda = 3.5_km;
    std::cout << "3.5 km = " << masofaMetrda << " metr" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. User-Defined Literals C++ kodini o'qishli va tabiiy qilishga yordam beradi.

## Ishlash natijasi:
```text
3.5 km = 3500 metr
```

---

# 480-Topshiriq: Satrlar uchun User-Defined Literal (operator""_uz)

## Topshiriq sharti:
O'zbekcha maxsus satr literalini e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

std::string operator"" _salom(const char* str, size_t len) {
    return "Assalomu alaykum, " + std::string(str, len) + "!";
}

int main() {
    auto xabar = "Toshkent"_salom;
    std::cout << xabar << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Satr literali kompilyatsiya vaqtida maxsus obyekt yoki matnga aylanadi.

## Ishlash natijasi:
```text
Assalomu alaykum, Toshkent!
```

---

# 481-Topshiriq: operator new va operator delete ni sinf ichida yuklash

## Topshiriq sharti:
Sinf obyektlari uchun xotirani o'zimizning statik buferimizdan ajratuvchi operatorlarni yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstddef>

class MaxsusObyekt {
public:
    int x;
    void* operator new(size_t size) {
        std::cout << "Maxsus operator new: " << size << " bayt ajratilmoqda\n";
        return ::operator new(size);
    }
    void operator delete(void* ptr) noexcept {
        std::cout << "Maxsus operator delete xotirani ozod qildi\n";
        ::operator delete(ptr);
    }
};

int main() {
    MaxsusObyekt* obj = new MaxsusObyekt();
    delete obj;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sinf ichidagi `operator new` faqat shu sinf obyektlari xotirasini boshqarish uchun ishlatiladi.

## Ishlash natijasi:
```text
Maxsus operator new: 4 bayt ajratilmoqda\nMaxsus operator delete xotirani ozod qildi
```

---

# 482-Topshiriq: Matritsada operator() orqali ikki o'lchamli indekslash

## Topshiriq sharti:
C++ da `mat[i, j]` C++23 gacha bo'lmagani sababli `mat(i, j)` orqali indekslashni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Matritsa2x2 {
    int m[2][2] = {{1, 2}, {3, 4}};
public:
    int& operator()(int r, int c) { return m[r][c]; }
    int operator()(int r, int c) const { return m[r][c]; }
};

int main() {
    Matritsa2x2 mat;
    mat(0, 1) = 99;
    std::cout << "mat(0, 1) = " << mat(0, 1) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `operator()` bir nechta argument qabul qila oladi va ko'p o'lchamli massivlar uchun idealdir.

## Ishlash natijasi:
```text
mat(0, 1) = 99
```

---

# 483-Topshiriq: Kompozit 2D Vektor sinfi to'liq operatorlari bilan

## Topshiriq sharti:
Vektorlar uchun `+`, `-`, `*` (skalyar ko'paytma) va `<<` oqim operatorlarini birlashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Vektor {
public:
    double x, y;
    Vektor(double a = 0, double b = 0) : x(a), y(b) {}
    Vektor operator+(const Vektor& o) const { return Vektor(x + o.x, y + o.y); }
    double operator*(const Vektor& o) const { return x * o.x + y * o.y; } // Skalyar ko'paytma
    friend std::ostream& operator<<(std::ostream& os, const Vektor& v) {
        return os << "(" << v.x << ", " << v.y << ")";
    }
};

int main() {
    Vektor v1(3, 4), v2(1, 2);
    std::cout << "Yig'indi: " << (v1 + v2) << std::endl;
    std::cout << "Dot product: " << (v1 * v2) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matematik sinflar operatorlar yuklanganda o'qilishi eng qulay shaklga keladi.

## Ishlash natijasi:
```text
Yig'indi: (4, 6)\nDot product: 11
```

---

# 484-Topshiriq: Valyuta (Pul) sinfi va operator+

## Topshiriq sharti:
Bir xil valyutadagi mablag'larni qo'shuvchi xavfsiz sinf tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Pul {
public:
    long long som;
    Pul(long long s = 0) : som(s) {}
    Pul operator+(const Pul& b) const {
        return Pul(som + b.som);
    }
    friend std::ostream& operator<<(std::ostream& os, const Pul& p) {
        return os << p.som << " so'm";
    }
};

int main() {
    Pul p1(50000), p2(75000);
    Pul jami = p1 + p2;
    std::cout << "Jami summa: " << jami << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Moliyaviy hisob-kitoblarda toifa xavfsizligi arifmetik xatolardan asraydi.

## Ishlash natijasi:
```text
Jami summa: 125000 so'm
```

---

# 485-Topshiriq: Bitset va binar operatorlar (&, |, ^, ~)

## Topshiriq sharti:
Klass ichida baytlarni bit darajasida manipulyatsiya qiluvchi operatorlarni yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class BitNiob {
public:
    unsigned char mask;
    BitNiob(unsigned char m = 0) : mask(m) {}
    BitNiob operator&(const BitNiob& b) const { return BitNiob(mask & b.mask); }
    BitNiob operator|(const BitNiob& b) const { return BitNiob(mask | b.mask); }
    BitNiob operator~() const { return BitNiob(~mask); }
};

int main() {
    BitNiob b1(0b1100), b2(0b1010);
    BitNiob va = b1 & b2;
    std::cout << "AND natijasi: " << (int)va.mask << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bit darajasidagi operatorlar apparat bilan to'g'ridan-to'g'ri ishlashda va 1-bit modellarida asosiy vositadir.

## Ishlash natijasi:
```text
AND natijasi: 8
```

---

# 486-Topshiriq: Oddiy BigInt (Katta Son) sinfida operator+

## Topshiriq sharti:
Cheksiz uzunlikdagi sonlarni satr ko'rinishida qo'shuvchi `operator+` ni amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <algorithm>

class BigInt {
public:
    std::string raqamlar;
    BigInt(std::string r) : raqamlar(r) {}
    BigInt operator+(const BigInt& b) const {
        std::string res = "";
        int i = raqamlar.length() - 1, j = b.raqamlar.length() - 1, dilda = 0;
        while (i >= 0 || j >= 0 || dilda) {
            int sum = dilda;
            if (i >= 0) sum += raqamlar[i--] - '0';
            if (j >= 0) sum += b.raqamlar[j--] - '0';
            dilda = sum / 10;
            res += (sum % 10) + '0';
        }
        std::reverse(res.begin(), res.end());
        return BigInt(res);
    }
};

int main() {
    BigInt a("99999999999999999999"), b("1");
    BigInt c = a + b;
    std::cout << "Natija: " << c.raqamlar << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta sonlar arifmetikasi xuddi shu kabi operatorlar ustiga quriladi.

## Ishlash natijasi:
```text
Natija: 100000000000000000000
```

---

# 487-Topshiriq: Polinomial (Ko'phad) sinfida operator+ va hisoblash

## Topshiriq sharti:
Ko'phad koeffitsiyentlarini qo'shuvchi va berilgan x uchun qiymat hisoblovchi sinf.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class Polinom {
public:
    std::vector<double> c; // c[0] + c[1]*x + c[2]*x^2
    Polinom(std::initializer_list<double> list) : c(list) {}
    double operator()(double x) const {
        double res = 0, daraja = 1;
        for (double koeff : c) {
            res += koeff * daraja;
            daraja *= x;
        }
        return res;
    }
};

int main() {
    Polinom p = {1.0, 2.0, 3.0}; // 1 + 2x + 3x^2
    std::cout << "p(2) = " << p(2.0) << std::endl; // 1 + 4 + 12 = 17
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Gorner yoki daraja sxemasi bilan ko'phad qiymati hisoblanadi.

## Ishlash natijasi:
```text
p(2) = 17
```

---

# 488-Topshiriq: Oqimga chiroyli chiqaruvchi Matrix sinfi (operator<<)

## Topshiriq sharti:
2D massivni tekislab konsolga chiqaruvchi `operator<<` yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Matritsa {
    int data[2][2] = {{5, 8}, {3, 9}};
public:
    friend std::ostream& operator<<(std::ostream& os, const Matritsa& m) {
        for (int i = 0; i < 2; ++i) {
            os << "| ";
            for (int j = 0; j < 2; ++j) os << m.data[i][j] << " ";
            os << "|\n";
        }
        return os;
    }
};

int main() {
    Matritsa m;
    std::cout << m;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Foydalanuvchi interfeysida matematik jadvallarni chiroyli ko'rsatish.

## Ishlash natijasi:
```text
| 5 8 |\n| 3 9 |
```

---

# 489-Topshiriq: 3D Tensor indekslash operatori: tensor(x, y, z)

## Topshiriq sharti:
Ko'p o'lchamli tenzorni 1D buferda saqlab, `operator()` orqali 3D indekslashni amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class Tensor3D {
    int D1, D2, D3;
    std::vector<float> data;
public:
    Tensor3D(int d1, int d2, int d3) : D1(d1), D2(d2), D3(d3), data(d1 * d2 * d3, 0.0f) {}
    float& operator()(int i, int j, int k) {
        return data[i * (D2 * D3) + j * D3 + k];
    }
};

int main() {
    Tensor3D t(2, 2, 2);
    t(1, 1, 1) = 0.85f;
    std::cout << "Tensor qiymati: " << t(1, 1, 1) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu aynan PyTorch va TensorFlow kabi freymvorklarning C++ yadrosidagi asosiy usuldir.

## Ishlash natijasi:
```text
Tensor qiymati: 0.85
```

---

# 490-Topshiriq: Smart Pointerda Rule of Five ning to'liq tekshiruvi

## Topshiriq sharti:
O'zimiz yozgan smart ko'rsatkich sinfining barcha 5 ta operatsiyasini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class MeningSmartPtr {
    int* ptr;
public:
    MeningSmartPtr(int* p = nullptr) : ptr(p) {}
    ~MeningSmartPtr() { delete ptr; }
    MeningSmartPtr(const MeningSmartPtr&) = delete;
    MeningSmartPtr& operator=(const MeningSmartPtr&) = delete;
    MeningSmartPtr(MeningSmartPtr&& o) noexcept : ptr(o.ptr) { o.ptr = nullptr; }
    MeningSmartPtr& operator=(MeningSmartPtr&& o) noexcept {
        if (this != &o) { delete ptr; ptr = o.ptr; o.ptr = nullptr; }
        return *this;
    }
    int& operator*() { return *ptr; }
};

int main() {
    MeningSmartPtr p1(new int(55));
    MeningSmartPtr p2 = std::move(p1);
    std::cout << "*p2 = " << *p2 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mukammal Move-only aqlli ko'rsatkich arxitekturasi.

## Ishlash natijasi:
```text
*p2 = 55
```

---

# 491-Topshiriq: String Move Semantikasi unumdorlik testi

## Topshiriq sharti:
Katta satrni nusxalash va ko'chirish o'rtasidagi farqni tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string katta(1000000, 'A'); // 1 million belgi
    std::string ko'chirilgan = std::move(katta); // 0 vaqtda faqat pointer ko'chadi
    std::cout << "Ko'chirilgan satr uzunligi: " << ko'chirilgan.length() << std::endl;
    std::cout << "Asl satr uzunligi: " << katta.length() << " (bo'sh qoldi)" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::move` yordamida millionlab belgilar xotirada nusxalanmasdan darhol ko'chiriladi.

## Ishlash natijasi:
```text
Ko'chirilgan satr uzunligi: 1000000\nAsl satr uzunligi: 0 (bo'sh qoldi)
```

---

# 492-Topshiriq: Mantiqiy operatorlarni yuklashdagi tuzoq (Short-circuit buzilishi)

## Topshiriq sharti:
Nima uchun `&&` va `||` ni yuklash qat'iyan man etilishi (chunki ular qisqa tutashuv xossasini yo'qotadi) ni tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "operator&& va operator|| qayta yuklansa, oddiy funksiya kabi "
              << "ikkala argument ham hisoblanadi va short-circuit bekor bo'ladi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shu sababli C++ da mantiqiy `&&` va `||` operatorlarini qayta yuklash yomon amaliyot (anti-pattern) hisoblanadi.

## Ishlash natijasi:
```text
operator&& va operator|| qayta yuklansa, oddiy funksiya kabi ikkala argument ham hisoblanadi va short-circuit bekor bo'ladi.
```

---

# 493-Topshiriq: Qayta yuklab bo'lmaydigan C++ operatorlari

## Topshiriq sharti:
Qaysi operatorlarni C++ tilida qayta yuklash mumkin emasligini aniq sanab bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Yuklab bo'lmaydigan operatorlar: . (nuqta), .* , :: (scope), ?: (ternar), sizeof, typeid" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu operatorlar tilning sintaktik va semantik poydevori bo'lgani sababli qayta yuklanishi taqiqlangan.

## Ishlash natijasi:
```text
Yuklab bo'lmaydigan operatorlar: . (nuqta), .* , :: (scope), ?: (ternar), sizeof, typeid
```

---

# 494-Topshiriq: Tenglik operatorini generatsiya qilish qoidalari (C++20)

## Topshiriq sharti:
`operator==` aniqlansa, C++20 kompilyatori avtomatik `!=` ni ham yaratib berishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Mahsulot {
    int narx;
    bool operator==(const Mahsulot& other) const = default;
};

int main() {
    Mahsulot a{100}, b{200};
    std::cout << "Teng emasmi: " << (a != b ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++20 dan boshlab faqat `==` ni e'lon qilish `!=` ni ham avtomatik ta'minlaydi.

## Ishlash natijasi:
```text
Teng emasmi: Ha
```

---

# 495-Topshiriq: Global va do'st operatorlar (Friend vs Member operators)

## Topshiriq sharti:
Chap tomonda asosiy tur turganda (masalan `2.0 * v`) global operator yuklash zarurati.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Vektor {
public:
    double x;
    Vektor(double a) : x(a) {}
    // Global do'st operator:
    friend Vektor operator*(double skalyar, const Vektor& v) {
        return Vektor(skalyar * v.x);
    }
};

int main() {
    Vektor v(10);
    Vektor natija = 2.5 * v; // Chapda double turibdi
    std::cout << "Natija: " << natija.x << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar operatorning chap argumenti sinf bo'lmasa, uni a'zo funksiya emas, global/friend funksiya sifatida yuklash shart.

## Ishlash natijasi:
```text
Natija: 25
```

---

# 496-Topshiriq: ADL (Argument-Dependent Lookup) va std::swap

## Topshiriq sharti:
O'zimizning `swap` funksiyamizni to'g'ri nomlar maydoni bilan yuklash.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <utility>

class Quti {
public:
    int hajm;
    Quti(int h) : hajm(h) {}
    friend void swap(Quti& a, Quti& b) noexcept {
        std::swap(a.hajm, b.hajm);
        std::cout << "Maxsus swap chaqirildi!\n";
    }
};

int main() {
    Quti q1(10), q2(20);
    using std::swap;
    swap(q1, q2); // ADL orqali Quti uchun yozilgan swap chaqiriladi
    std::cout << "q1: " << q1.hajm << ", q2: " << q2.hajm << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ADL argumentlar toifasiga qarab tegishli nomlar maydonidagi maxsus `swap` ni avtomatik topadi.

## Ishlash natijasi:
```text
Maxsus swap chaqirildi!\nq1: 20, q2: 10
```

---

# 497-Topshiriq: Operatorlarni ketma-ket ulash (Chaining operators: a + b + c)

## Topshiriq sharti:
Nima uchun `operator+` havolani emas, yangi obyekt qiymatini qaytarishi kerakligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Son {
public:
    int v;
    Son(int val) : v(val) {}
    Son operator+(const Son& other) const {
        return Son(v + other.v);
    }
};

int main() {
    Son a(1), b(2), c(3);
    Son res = a + b + c; // Ketma-ket zanjir
    std::cout << "Yig'indi: " << res.v << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Vaqtinchalik natijalar havola emas, qiymat sifatida uzatiladi va Move orqali optimallashadi.

## Ishlash natijasi:
```text
Yig'indi: 6
```

---

# 498-Topshiriq: Kompilyatsiya vaqtida Move qobiliyatini tekshirish

## Topshiriq sharti:
`std::is_move_constructible` orqali sinf ko'chish qobiliyatiga egaligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <type_traits>
#include <memory>

int main() {
    std::cout << "int ko'chuvchimi: " << std::is_move_constructible<int>::value << std::endl;
    std::cout << "unique_ptr ko'chuvchimi: " << std::is_move_constructible<std::unique_ptr<int>>::value << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Meta-dasturlashda sinflarning move xossasi tekshirilib mos algoritmlar tanlanadi.

## Ishlash natijasi:
```text
int ko'chuvchimi: 1\nunique_ptr ko'chuvchimi: 1
```

---

# 499-Topshiriq: Operatorlarni ortiqcha suiiste'mol qilish (Anti-pattern)

## Topshiriq sharti:
Operator ma'nosi tabiiy bo'lmagan hollarda operator emas, nomli metod yozish lozimligini xulosa qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Qoida: Operator faqat uning matematik yoki tabiiy ma'nosi aniq bo'lgandagina yuklanadi. "
              << "Noaniq hollarda nomli metodlar (masalan .qoshish()) yozish afzaldir." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Aniq va tushunarli kod noaniq operatorlardan doimo ustun turadi.

## Ishlash natijasi:
```text
Qoida: Operator faqat uning matematik yoki tabiiy ma'nosi aniq bo'lgandagina yuklanadi. Noaniq hollarda nomli metodlar (masalan .qoshish()) yozish afzaldir.
```

---

# 500-Topshiriq: 10-qism xulosasi: Move Semantikasi va Zamonaviy C++ Inqilobi

## Topshiriq sharti:
Move semantikasi (C++11) va Rule of Five C++ tilini xotira xavfsizligi va maksimal tezlik bo'yicha dunyodagi eng yetakchi tizimiy tilga aylantirganini umumlashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "C++ da Move Semantikasi - bu xotirani qayta ajratmasdan resurslarni "
              << "lahzada o'tkazish qudratidir!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Move semantikasi zamonaviy yuqori unumdor tizimlarning asosi hisoblanadi.

## Ishlash natijasi:
```text
C++ da Move Semantikasi - bu xotirani qayta ajratmasdan resurslarni lahzada o'tkazish qudratidir!
```

---

