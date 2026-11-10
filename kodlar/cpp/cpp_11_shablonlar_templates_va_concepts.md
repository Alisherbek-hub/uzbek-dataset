# C++ Dasturlash Tili - 11-Qism: Shablonlar (Templates), SFINAE va C++20 Konseptlar (Concepts)

Ushbu qismda funksiya va sinf shablonlari, ixtisoslashuv, variadic templates, folding expressions, perfect forwarding, constexpr if, SFINAE va C++20 Concepts ga oid 50 ta amaliy topshiriq jamlangan.

---

# 501-Topshiriq: Funksiya shabloni (Function Template) asoslari

## Topshiriq sharti:
Har qanday turdagi ikkita qiymatni taqqoslab kattasini qaytaruvchi shablon funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T>
T maksimal(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    std::cout << "Butun: " << maksimal(10, 20) << std::endl;
    std::cout << "Haqiqiy: " << maksimal(5.5, 3.2) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `template <typename T>` kompilyatorga har bir aniq tur uchun funksiyani avtomatik generatsiya qilishni buyuradi.

## Ishlash natijasi:
```text
Butun: 20\nHaqiqiy: 5.5
```

---

# 502-Topshiriq: Bir nechta parametrli shablon funksiya

## Topshiriq sharti:
Har xil turdagi ikkita argumentni qabul qilib chop etuvchi shablon tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T, typename U>
void juftlikChop(T a, U b) {
    std::cout << "A: " << a << " | B: " << b << std::endl;
}

int main() {
    juftlikChop("Yil", 2026);
    juftlikChop(3.14, 'P');
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `T` va `U` mustaqil turlar bo'lib, ixtiyoriy kombinatsiyalarni qabul qiladi.

## Ishlash natijasi:
```text
A: Yil | B: 2026\nA: 3.14 | B: P
```

---

# 503-Topshiriq: Shablonda avtomatik toifa aniqlash (Deduction)

## Topshiriq sharti:
Kompilyator argumentlar orqali shablon parametrlarini avtomatik taniy olishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T>
void kvadratiniChiqar(T x) {
    std::cout << x << " kvadrati: " << (x * x) << std::endl;
}

int main() {
    kvadratiniChiqar(7);    // T = int avtomatik aniqlandi
    kvadratiniChiqar(2.5);  // T = double avtomatik aniqlandi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dasturchi `<int>` deb ko'rsatishi shart emas, argument turi yetarli bo'ladi.

## Ishlash natijasi:
```text
7 kvadrati: 49\n2.5 kvadrati: 6.25
```

---

# 504-Topshiriq: Oshkora toifa ko'rsatish (Explicit Template Argument)

## Topshiriq sharti:
Turlari bir xil bo'lishi talab qilingan joyda turli xil argumentlar berilganda oshkora toifani ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T>
T qosh(T a, T b) {
    return a + b;
}

int main() {
    // qosh(5, 2.5); // Xato: T int bo'lsinmi yoki double?
    double res = qosh<double>(5, 2.5); // Oshkora ko'rsatildi
    std::cout << "Natija: " << res << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `<double>` ko'rsatilishi barcha parametrlarni double ga keltiradi.

## Ishlash natijasi:
```text
Natija: 7.5
```

---

# 505-Topshiriq: Toifa bo'lmagan shablon parametri (Non-Type Template Parameter - NTTP)

## Topshiriq sharti:
Massiv o'lchamini shablon parametri sifatida berishni amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T, size_t N>
void massivChop(const T (&arr)[N]) {
    std::cout << "Massiv hajmi: " << N << " | Elementlar: ";
    for (size_t i = 0; i < N; ++i) std::cout << arr[i] << " ";
    std::cout << std::endl;
}

int main() {
    int sonlar[] = {1, 2, 3, 4};
    massivChop(sonlar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `size_t N` kompilyatsiya vaqtida massiv o'lchamini aniq ushlaydi va array decay sodir bo'lmaydi.

## Ishlash natijasi:
```text
Massiv hajmi: 4 | Elementlar: 1 2 3 4 
```

---

# 506-Topshiriq: Sinf shabloni (Class Template) asoslari

## Topshiriq sharti:
Har qanday turdagi bitta qiymatni saqlovchi umumiy `Quti<T>` sinfini tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

template <typename T>
class Quti {
    T qiymat;
public:
    Quti(T q) : qiymat(q) {}
    T get() const { return qiymat; }
};

int main() {
    Quti<int> q1(123);
    Quti<std::string> q2("Antigravity");
    std::cout << "q1: " << q1.get() << ", q2: " << q2.get() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sinf shabloni bir nechta tur uchun bitta yagona sinf kodi yozish imkonini beradi.

## Ishlash natijasi:
```text
q1: 123, q2: Antigravity
```

---

# 507-Topshiriq: Sinf shablonida metodni sinfdan tashqarida aniqlash

## Topshiriq sharti:
`template <typename T>` prefiksi bilan sinfdan tashqarida metod yozish sintaksisini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T>
class Saqlagich {
    T element;
public:
    Saqlagich(T e);
    void korsat() const;
};

template <typename T>
Saqlagich<T>::Saqlagich(T e) : element(e) {}

template <typename T>
void Saqlagich<T>::korsat() const {
    std::cout << "Element: " << element << std::endl;
}

int main() {
    Saqlagich<double> s(99.99);
    s.korsat();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir tashqi metod `template <typename T>` sarlavhasiga ega bo'lishi kerak.

## Ishlash natijasi:
```text
Element: 99.99
```

---

# 508-Topshiriq: Sinf shablonida standart parametrlar (Default template arguments)

## Topshiriq sharti:
Shablon parametriga standart toifa berishni (`template <typename T = int>`) ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T = int>
class Raqam {
public:
    T qiymat;
    Raqam(T q = 0) : qiymat(q) {}
};

int main() {
    Raqam<> r1(10); // Sukut bo'yicha int
    Raqam<double> r2(3.14);
    std::cout << "r1: " << r1.qiymat << ", r2: " << r2.qiymat << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Standart parametr berilganda bo'sh burchakli qavslar `<>` kifoya qiladi.

## Ishlash natijasi:
```text
r1: 10, r2: 3.14
```

---

# 509-Topshiriq: Funksiya shablonini to'liq ixtisoslashtirish (Full Specialization)

## Topshiriq sharti:
`bool` toifasi uchun alohida mantiqqa ega ixtisoslashgan funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T>
void tavsif(T x) {
    std::cout << "Umumiy qiymat: " << x << std::endl;
}

// To'liq ixtisoslashuv:
template <>
void tavsif<bool>(bool b) {
    std::cout << "Mantiqiy qiymat: " << (b ? "HA" : "YO'Q") << std::endl;
}

int main() {
    tavsif(42);
    tavsif(true);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `template <>` orqali ma'lum bir tur uchun maxsus implementatsiya beriladi.

## Ishlash natijasi:
```text
Umumiy qiymat: 42\nMantiqiy qiymat: HA
```

---

# 510-Topshiriq: Sinf shablonini qisman ixtisoslashtirish (Partial Specialization)

## Topshiriq sharti:
Ko'rsatkich turlari (`T*`) uchun sinf shablonini qisman ixtisoslashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T>
class Tahlilchi {
public:
    void tur() { std::cout << "Oddiy toifa" << std::endl; }
};

// Qisman ixtisoslashuv (Faqat ko'rsatkichlar uchun):
template <typename T>
class Tahlilchi<T*> {
public:
    void tur() { std::cout << "Ko'rsatkich (Pointer) toifasi" << std::endl; }
};

int main() {
    Tahlilchi<int> t1;
    t1.tur();
    Tahlilchi<int*> t2;
    t2.tur();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qisman ixtisoslashuv sinf shablonlarini ma'lum bir tur guruhiga (masalan barcha pointerlarga) moslashtiradi.

## Ishlash natijasi:
```text
Oddiy toifa\nKo'rsatkich (Pointer) toifasi
```

---

# 511-Topshiriq: CTAD (Class Template Argument Deduction - C++17)

## Topshiriq sharti:
C++17 dan boshlab sinf shablonlarida burchakli qavslarsiz obyekt yaratishni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <utility>

template <typename T, typename U>
struct Juftlik {
    T birinchi;
    U ikkinchi;
    Juftlik(T a, U b) : birinchi(a), ikkinchi(b) {}
};

int main() {
    Juftlik j(10, "Satr"); // CTAD orqali Juftlik<int, const char*> avtomatik aniqlandi
    std::cout << j.birinchi << " va " << j.ikkinchi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++17 konstruktor parametrlariga qarab sinf shablon turlarini mustaqil aniqlaydi.

## Ishlash natijasi:
```text
10 va Satr
```

---

# 512-Topshiriq: Maxsus CTAD Yo'riqnomasi (Deduction Guide)

## Topshiriq sharti:
Kompilyatorga qanday toifani tanlash kerakligini o'rgatuvchi yo'riqnoma yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

template <typename T>
struct Konteyner {
    T element;
    Konteyner(T val) : element(val) {}
};

// Deduction Guide: const char* kelsa std::string deb tushun
Konteyner(const char*) -> Konteyner<std::string>;

int main() {
    Konteyner k("Salom");
    std::cout << "Turi: std::string (" << k.element.length() << " belgi)" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Deduction Guide konstruktor argumentlarini kutilgan maqsadli shablon turiga o'giradi.

## Ishlash natijasi:
```text
Turi: std::string (5 belgi)
```

---

# 513-Topshiriq: O'zgaruvchilar shabloni (Variable Templates - C++14)

## Topshiriq sharti:
Har xil toifadagi Pi sonini beruvchi o'zgaruvchi shablonini e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T>
constexpr T pi = T(3.1415926535897932385);

int main() {
    std::cout << "float pi: " << pi<float> << std::endl;
    std::cout << "double pi: " << pi<double> << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++14 da qo'shilgan o'zgaruvchilar shabloni matematik konstantalar uchun juda qulay.

## Ishlash natijasi:
```text
float pi: 3.14159\ndouble pi: 3.14159
```

---

# 514-Topshiriq: Tur taxalluslari shabloni (Alias Templates)

## Topshiriq sharti:
`using` orqali shablonli turga qisqa nom bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

template <typename T>
using Matritsa = std::vector<std::vector<T>>;

int main() {
    Matritsa<int> m = {{1, 2}, {3, 4}};
    std::cout << "m[1][1] = " << m[1][1] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Alias templates murakkab shablon tuzilmalarini soddalashtiradi.

## Ishlash natijasi:
```text
m[1][1] = 4
```

---

# 515-Topshiriq: Bog'liq turlar va typename kalit so'zi

## Topshiriq sharti:
Shablon ichida ichki turga murojaat qilishda `typename` ning majburiyligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

template <typename T>
void birinchiElement(const T& idish) {
    typename T::const_iterator it = idish.begin();
    if (it != idish.end()) {
        std::cout << "Birinchi: " << *it << std::endl;
    }
}

int main() {
    std::vector<int> v = {77, 88};
    birinchiElement(v);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `typename T::const_iterator` kompilyatorga bu a'zo o'zgaruvchi emas, balki tur ekanligini bildiradi.

## Ishlash natijasi:
```text
Birinchi: 77
```

---

# 516-Topshiriq: Shablon rekursiyasi (Kompilyatsiya vaqtida faktorial)

## Topshiriq sharti:
Struktura shabloni orqali 6! faktorial qiymatini dastur ishga tushmasdan oldin hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <int N>
struct Faktorial {
    static constexpr long long qiymat = N * Faktorial<N - 1>::qiymat;
};

// Bazaviy holat:
template <>
struct Faktorial<0> {
    static constexpr long long qiymat = 1;
};

int main() {
    std::cout << "6! (shablon rekursiyasi) = " << Faktorial<6>::qiymat << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Template Metaprogramming C++ ning kompilyatsiya vaqtidagi to'liq Turing hisoblash qobiliyatini namoyish etadi.

## Ishlash natijasi:
```text
6! (shablon rekursiyasi) = 720
```

---

# 517-Topshiriq: constexpr if (C++17) orqali tarmoqlanish

## Topshiriq sharti:
Kompilyatsiya vaqtida toifaga qarab faqat mos kelgan kod qismini kompilyatsiya qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <type_traits>

template <typename T>
void xususiyat(T x) {
    if constexpr (std::is_pointer_v<T>) {
        std::cout << "Ko'rsatkich: " << *x << std::endl;
    } else {
        std::cout << "Oddiy qiymat: " << x << std::endl;
    }
}

int main() {
    int son = 100;
    xususiyat(son);
    xususiyat(&son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `if constexpr` shart bajarilmagan qismni kompilyatsiyadan butunlay chiqarib tashlaydi.

## Ishlash natijasi:
```text
Oddiy qiymat: 100\nKo'rsatkich: 100
```

---

# 518-Topshiriq: std::is_integral va type_traits

## Topshiriq sharti:
`<type_traits>` orqali turning butun son ekanligini kompilyatsiya vaqtida tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <type_traits>

template <typename T>
void sonTekshir() {
    if constexpr (std::is_integral_v<T>) {
        std::cout << "Butun son turi" << std::endl;
    } else {
        std::cout << "Butun son emas" << std::endl;
    }
}

int main() {
    sonTekshir<int>();
    sonTekshir<double>();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `type_traits` turlar haqidagi xususiyatlarni kompilyatsiya bosqichida tahlil qiladi.

## Ishlash natijasi:
```text
Butun son turi\nButun son emas
```

---

# 519-Topshiriq: SFINAE va std::enable_if (C++11)

## Topshiriq sharti:
Funksiyani faqat butun sonlar uchun yoquvchi SFINAE mexanizmini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <type_traits>

template <typename T, typename std::enable_if<std::is_integral<T>::value, int>::type = 0>
void faqatButun(T x) {
    std::cout << "Qabul qilindi: " << x << std::endl;
}

int main() {
    faqatButun(55);
    // faqatButun(3.14); // Kompilyatsiya xatosi: mos funksiya topilmadi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. SFINAE (Substitution Failure Is Not An Error) mos kelmagan shablon variantini xato bermasdan o'tkazib yuboradi.

## Ishlash natijasi:
```text
Qabul qilindi: 55
```

---

# 520-Topshiriq: decltype va return type deduction

## Topshiriq sharti:
`decltype` yordamida ifodaning toifasini aniqlab qaytarish turini belgilang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T, typename U>
auto kopaytir(T a, U b) -> decltype(a * b) {
    return a * b;
}

int main() {
    auto res = kopaytir(3, 2.5); // res double bo'ladi
    std::cout << "Natija: " << res << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `decltype(a * b)` natijaning toifasini kompilyatordan oladi.

## Ishlash natijasi:
```text
Natija: 7.5
```

---

# 521-Topshiriq: decltype(auto) (C++14)

## Topshiriq sharti:
Havolalarni yo'qotmasdan aniq tur va havolalikni saqlab qoluvchi `decltype(auto)` ni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int globalSon = 500;

int& getRef() { return globalSon; }

decltype(auto) chaqir() {
    return getRef(); // int& toifasi to'liq saqlanadi
}

int main() {
    chaqir() = 700;
    std::cout << "globalSon: " << globalSon << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oddiy `auto` havolani tashlab yuboradi (`int`), ammo `decltype(auto)` aniq `int&` ni saqlaydi.

## Ishlash natijasi:
```text
globalSon: 700
```

---

# 522-Topshiriq: Cheksiz parametrli shablonlar (Variadic Templates)

## Topshiriq sharti:
Ixtiyoriy sondagi har xil turdagi argumentlarni qabul qiluvchi shablon e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename... Args>
void argumentlarSoni(Args... args) {
    std::cout << "Uzatilgan argumentlar soni: " << sizeof...(args) << std::endl;
}

int main() {
    argumentlarSoni(1, 2.5, "Salom", 'A');
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sizeof...(args)` parametrlar to'plamidagi argumentlar miqdorini hisoblaydi.

## Ishlash natijasi:
```text
Uzatilgan argumentlar soni: 4
```

---

# 523-Topshiriq: Variadic shablonni rekursiv ochish

## Topshiriq sharti:
Klassik rekursiya orqali barcha argumentlarni ketma-ket ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void chopHammasi() {
    std::cout << std::endl; // Bazaviy holat
}

template <typename T, typename... Qolganlar>
void chopHammasi(T birinchi, Qolganlar... qolgan) {
    std::cout << birinchi << " ";
    chopHammasi(qolgan...); // Qolgan qismi rekursiv uzatiladi
}

int main() {
    chopHammasi(10, "kitob", 3.14, 'C');
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir chaqiruvda bitta argument ajratiladi va qolgan pack rekursiv uzatiladi.

## Ishlash natijasi:
```text
10 kitob 3.14 C 
```

---

# 524-Topshiriq: Folding Expressions (C++17 Buklash ifodalari)

## Topshiriq sharti:
C++17 ning qulay buklash ifodasi orqali barcha argumentlar yig'indisini bitta qatorda hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename... Args>
auto jamiYigindi(Args... args) {
    return (... + args); // Unary left fold
}

int main() {
    std::cout << "Yig'indi: " << jamiYigindi(1, 2, 3, 4, 5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `(... + args)` ifodasi `((1 + 2) + 3) + 4) + 5` ga aylanadi.

## Ishlash natijasi:
```text
Yig'indi: 15
```

---

# 525-Topshiriq: Folding Expression bilan chiqarish

## Topshiriq sharti:
Folding expression orqali rekursiyasiz barcha argumentlarni chop eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename... Args>
void birQatorda(Args... args) {
    ((std::cout << args << " "), ...);
    std::cout << std::endl;
}

int main() {
    birQatorda("AI", 2026, "Toshkent", true);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Vergul operatori bilan buklash ifodasi kodni aqlbovar qilmas darajada ixcham qiladi.

## Ishlash natijasi:
```text
AI 2026 Toshkent 1 
```

---

# 526-Topshiriq: Universal havola (Forwarding Reference) va std::forward

## Topshiriq sharti:
Lvalue va Rvalue xossasini o'zgartirmasdan keyingi funksiyaga mukammal uzating (Perfect Forwarding).

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <utility>

void qaytaIshla(int& x) { std::cout << "Lvalue qabul qilindi\n"; }
void qaytaIshla(int&& x) { std::cout << "Rvalue qabul qilindi\n"; }

template <typename T>
void oramcha(T&& arg) {
    qaytaIshla(std::forward<T>(arg)); // Mukammal uzatish
}

int main() {
    int a = 10;
    oramcha(a);
    oramcha(20);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::forward<T>` argumentning asl toifasini (lvalue yoki rvalue) aniq saqlab qoladi.

## Ishlash natijasi:
```text
Lvalue qabul qilindi\nRvalue qabul qilindi
```

---

# 527-Topshiriq: Universal Factory funksiyasi (make_unique analogi)

## Topshiriq sharti:
Perfect forwarding orqali ixtiyoriy sinf obyektini dinamik yaratuvchi zavod funksiyasi yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>
#include <string>

struct Xodim {
    std::string ism;
    int yosh;
    Xodim(std::string i, int y) : ism(i), yosh(y) {}
};

template <typename T, typename... Args>
std::unique_ptr<T> meningMakeUnique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

int main() {
    auto x = meningMakeUnique<Xodim>("Temur", 28);
    std::cout << x->ism << ", " << x->yosh << " yosh" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::make_unique` aynan shu tamoyil asosida mukammal uzatish bilan qurilgan.

## Ishlash natijasi:
```text
Temur, 28 yosh
```

---

# 528-Topshiriq: C++20 Konseptlar (Concepts) asoslari

## Topshiriq sharti:
`concept` kalit so'zi yordamida turga nisbatan shart belgilang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <concepts>

template <typename T>
concept SonTuri = std::is_arithmetic_v<T>;

template <SonTuri T>
T ikkiBarobar(T x) {
    return x * 2;
}

int main() {
    std::cout << ikkiBarobar(15) << std::endl;
    std::cout << ikkiBarobar(4.5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++20 Konseptlari shablonlarni tekshirishni nihoyatda oson va tushunarli qiladi.

## Ishlash natijasi:
```text
30\n9
```

---

# 529-Topshiriq: requires bandi (Requires clause)

## Topshiriq sharti:
Funksiya sarlavhasida `requires` bandi orqali shartni ifodalang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <concepts>

template <typename T>
requires std::integral<T>
T qoldiq(T a, T b) {
    return a % b;
}

int main() {
    std::cout << "17 % 5 = " << qoldiq(17, 5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `requires std::integral<T>` funksiyani faqat butun sonlar uchun cheklaydi.

## Ishlash natijasi:
```text
17 % 5 = 2
```

---

# 530-Topshiriq: Standart C++20 konseptlari: std::floating_point

## Topshiriq sharti:
Faqat suzuvchi nuqtali sonlar bilan ishlovchi funksiyani standart konsept bilan himoyalang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <concepts>

template <std::floating_point T>
T yarmi(T x) {
    return x / 2.0;
}

int main() {
    std::cout << "5.0 ning yarmi: " << yarmi(5.0) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `<concepts>` sarlavhasida o'nlab tayyor standart konseptlar mavjud.

## Ishlash natijasi:
```text
5.0 ning yarmi: 2.5
```

---

# 531-Topshiriq: O'zimizning maxsus konseptimizni yaratish

## Topshiriq sharti:
Qo'shish va ko'paytirish mumkin bo'lgan turlarni talab qiluvchi konsept yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <concepts>

template <typename T>
concept MatematikObekt = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
    { a * b } -> std::same_as<T>;
};

template <MatematikObekt T>
T formula(T x) {
    return x * x + x;
}

int main() {
    std::cout << "formula(3) = " << formula(3) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `requires` blokida ifodalar sintaksisi va ularning qaytarish toifasi tekshiriladi.

## Ishlash natijasi:
```text
formula(3) = 12
```

---

# 532-Topshiriq: Sinf metodlari mavjudligini tekshiruvchi Konsept

## Topshiriq sharti:
Sinfda `.chopEt()` metodi bo'lishini majburiy talab qiluvchi konsept tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <concepts>

template <typename T>
concept ChopQilinuvchi = requires(T t) {
    t.chopEt();
};

struct Hujjat {
    void chopEt() { std::cout << "Hujjat chop etildi" << std::endl; }
};

template <ChopQilinuvchi T>
void bajargich(T obj) {
    obj.chopEt();
}

int main() {
    Hujjat h;
    bajargich(h);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Metod yo'q bo'lsa kompilyator juda aniq va qisqa xato xabarini beradi.

## Ishlash natijasi:
```text
Hujjat chop etildi
```

---

# 533-Topshiriq: Qisqartirilgan funksiya shabloni (Abbreviated Function Template - auto parametr)

## Topshiriq sharti:
C++20 da `void funksiya(auto x)` deb yozish avtomatik funksiya shabloniga aylanishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void chopAuto(auto x) {
    std::cout << "Qiymat: " << x << std::endl;
}

int main() {
    chopAuto(100);
    chopAuto("Avtomatik shablon");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `auto` parametri C++20 da funksiya shablonini eng qisqa va qulay yozish yo'lidir.

## Ishlash natijasi:
```text
Qiymat: 100\nQiymat: Avtomatik shablon
```

---

# 534-Topshiriq: Konseptlar orqali funksiyani qayta yuklash (Overloading with Concepts)

## Topshiriq sharti:
Butun sonlar va haqiqiy sonlar uchun konseptlar asosida bitta nomli alohida funksiyalarni ishga tushiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <concepts>

void tahlil(std::integral auto x) {
    std::cout << "Butun son tahlili: " << x << std::endl;
}

void tahlil(std::floating_point auto x) {
    std::cout << "Haqiqiy son tahlili: " << x << std::endl;
}

int main() {
    tahlil(42);
    tahlil(3.14);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyator qaysi konsept mos kelsa, o'sha funksiyani aniq tanlaydi.

## Ishlash natijasi:
```text
Butun son tahlili: 42\nHaqiqiy son tahlili: 3.14
```

---

# 535-Topshiriq: Kompilyatsiya xatolari sifati: SFINAE vs Concepts

## Topshiriq sharti:
Nima uchun Konseptlar C++ shablonlarining 30 yillik tushunarsiz xatolar muammosini hal qilganini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "C++20 Konseptlari yuzlab qatorli shablon xatolarini "
              << "bitta tushunarli: 'T konsept shartini qanoatlantirmadi' xabariga aylantiradi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu dasturchilar samaradorligini va kod xavfsizligini keskin oshiradi.

## Ishlash natijasi:
```text
C++20 Konseptlari yuzlab qatorli shablon xatolarini bitta tushunarli: 'T konsept shartini qanoatlantirmadi' xabariga aylantiradi.
```

---

# 536-Topshiriq: Shablonli Stek (Stack) ma'lumotlar tuzilmasi

## Topshiriq sharti:
Har qanday turdagi ma'lumotlar uchun LIFO asosida ishlovchi Stack sinf shablonini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

template <typename T>
class MeningStekim {
    std::vector<T> data;
public:
    void push(T val) { data.push_back(val); }
    void pop() { data.pop_back(); }
    T top() const { return data.back(); }
    bool boshmi() const { return data.empty(); }
};

int main() {
    MeningStekim<std::string> st;
    st.push("bir");
    st.push("ikki");
    std::cout << "Top: " << st.top() << std::endl;
    st.pop();
    std::cout << "Keyingi: " << st.top() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shablonlar yordamida yozilgan ma'lumotlar tuzilmasi universal bo'ladi.

## Ishlash natijasi:
```text
Top: ikki\nKeyingi: bir
```

---

# 537-Topshiriq: O'lchami va turi shablonda berilgan Matritsa sinfi

## Topshiriq sharti:
`template <typename T, size_t R, size_t C>` orqali stekda joylashuvchi tezkor matritsa tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T, size_t Rows, size_t Cols>
class MatritsaShablon {
    T mat[Rows][Cols]{};
public:
    T& operator()(size_t r, size_t c) { return mat[r][c]; }
    size_t qatorlar() const { return Rows; }
    size_t ustunlar() const { return Cols; }
};

int main() {
    MatritsaShablon<int, 2, 3> m;
    m(0, 0) = 10;
    std::cout << "Matritsa: " << m.qatorlar() << "x" << m.ustunlar() 
              << ", m(0,0) = " << m(0, 0) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dynamic allokatsiya yo'q, xotira to'liq stekda va kesh uchun super tez.

## Ishlash natijasi:
```text
Matritsa: 2x3, m(0,0) = 10
```

---

# 538-Topshiriq: Turlar tengligini tekshirish (std::is_same)

## Topshiriq sharti:
Ikki toifaning mutlaqo bir xil ekanligini kompilyatsiya vaqtida aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <type_traits>

template <typename T, typename U>
void turlarniSolishtir() {
    if constexpr (std::is_same_v<T, U>) {
        std::cout << "Turlar mutlaqo bir xil!" << std::endl;
    } else {
        std::cout << "Har xil turlar" << std::endl;
    }
}

int main() {
    turlarniSolishtir<int, int>();
    turlarniSolishtir<int, double>();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::is_same_v` meta-dasturlashda turlarni qat'iy tekshirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Turlar mutlaqo bir xil!\nHar xil turlar
```

---

# 539-Topshiriq: std::decay orqali toifani tozalash

## Topshiriq sharti:
`std::decay` havolalar va `const` larni olib tashlab, turning asl holatini qaytarishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <type_traits>

int main() {
    using AslTur = std::decay_t<const int&>;
    std::cout << "const int& tozalandi int ga: " 
              << std::is_same_v<AslTur, int> << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::decay` funksiya parametrlarini oddiy qiymat toifasiga keltiradi.

## Ishlash natijasi:
```text
const int& tozalandi int ga: 1
```

---

# 540-Topshiriq: std::void_t orqali a'zo bor-yo'qligini aniqlash

## Topshiriq sharti:
Sinf ichida `value_type` aniqlangan yoki yo'qligini aniqlovchi meta-funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <type_traits>

template <typename, typename = void>
struct HasValueType : std::false_type {};

template <typename T>
struct HasValueType<T, std::void_t<typename T::value_type>> : std::true_type {};

int main() {
    std::cout << "vector da value_type bormi: " << HasValueType<std::vector<int>>::value << std::endl;
    std::cout << "int da value_type bormi: " << HasValueType<int>::value << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::void_t` yordamida har qanday sinf xususiyatlarini kompilyatsiya paytida aniqlash mumkin.

## Ishlash natijasi:
```text
vector da value_type bormi: 1\nint da value_type bormi: 0
```

---

# 541-Topshiriq: Oddiy static_assert bilan tur xavfsizligi

## Topshiriq sharti:
Kompilyatsiya vaqtida shart bajarilmasa kompilyatsiyani to'xtatuvchi `static_assert` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <type_traits>

template <typename T>
void faqatPointerlar(T ptr) {
    static_assert(std::is_pointer_v<T>, "Xatolik: Funksiya faqat ko'rsatkich qabul qiladi!");
    std::cout << "Ko'rsatkich qabul qilindi: " << (void*)ptr << std::endl;
}

int main() {
    int son = 10;
    faqatPointerlar(&son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `static_assert` dasturchiga xato haqida tushunarli xabar beradi.

## Ishlash natijasi:
```text
Ko'rsatkich qabul qilindi: 0x...
```

---

# 542-Topshiriq: Expression SFINAE asoslari

## Topshiriq sharti:
Ifodaning haqiqiyligiga qarab funksiyani tanlash.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T>
auto chop(T x) -> decltype(std::cout << x, void()) {
    std::cout << "Oqimga chiqdi: " << x << std::endl;
}

int main() {
    chop(1234);
    chop("Salom");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Faqat `std::cout << x` amali mavjud bo'lgan tiplargina bu funksiyaga tushadi.

## Ishlash natijasi:
```text
Oqimga chiqdi: 1234\nOqimga chiqdi: Salom
```

---

# 543-Topshiriq: Funksiya shablonlari va nomlar maydoni

## Topshiriq sharti:
Nomlar maydoni ichida shablon funksiyalarni modulli saqlash.

## Yechim (C++ kodi):
```cpp
#include <iostream>

namespace Matematika {
    template <typename T>
    T kvadrat(T x) { return x * x; }
}

int main() {
    std::cout << Matematika::kvadrat(8) << std::endl;
    std::cout << Matematika::kvadrat(1.2) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Modulli kutubxonalar nomlar to'qnashuvidan xoli bo'ladi.

## Ishlash natijasi:
```text
64\n1.44
```

---

# 544-Topshiriq: Shablonli Yagona Nusxa (Template Singleton)

## Topshiriq sharti:
Ixtiyoriy sinf uchun yagona Singleton nusxasini ta'minlovchi umumiy shablon.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T>
class Singleton {
public:
    static T& getInstance() {
        static T instance;
        return instance;
    }
};

class AuditLog : public Singleton<AuditLog> {
public:
    void yoz(const char* m) { std::cout << "Audit: " << m << std::endl; }
};

int main() {
    AuditLog::getInstance().yoz("Tizim sozlandi");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shablon orqali istalgan sinfni Meyer Singleton qilish mumkin.

## Ishlash natijasi:
```text
Audit: Tizim sozlandi
```

---

# 545-Topshiriq: Shablonli Lambda ifodalari (Generic Lambdas - C++14)

## Topshiriq sharti:
`auto` parametrli umumiy lambda funksiyalaridan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    auto qoshuvchi = [](auto a, auto b) {
        return a + b;
    };
    std::cout << qoshuvchi(5, 7) << std::endl;
    std::cout << qoshuvchi(std::string("A"), std::string("B")) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Generic lambdalar funksiya shablonlarining anonim ko'rinishidir.

## Ishlash natijasi:
```text
12\nAB
```

---

# 546-Topshiriq: Shablonli Lambda bilan aniq tur belgilash (C++20)

## Topshiriq sharti:
C++20 da lambdaga `<typename T>` sintaksisini qo'llash.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    auto birinchiOlish = []<typename T>(const std::vector<T>& v) {
        return v.empty() ? T{} : v.front();
    };
    std::vector<int> sonlar = {42, 99};
    std::cout << "Birinchi: " << birinchiOlish(sonlar) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++20 da lambdalar ham to'laqonli shablon sintaksisiga ega bo'ldi.

## Ishlash natijasi:
```text
Birinchi: 42
```

---

# 547-Topshiriq: Konseptlar bilan Container konsepti yaratish

## Topshiriq sharti:
`begin()`, `end()` va `size()` metodlariga ega bo'lgan konteynerlarni aniqlovchi konsept.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <concepts>

template <typename C>
concept Konteyner = requires(C c) {
    c.begin();
    c.end();
    c.size();
};

template <Konteyner C>
void hajm(const C& c) {
    std::cout << "Konteyner hajmi: " << c.size() << std::endl;
}

int main() {
    std::vector<int> v = {1, 2, 3};
    hajm(v);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. STL konteynerlarini filtrlovchi o'z konseptimiz.

## Ishlash natijasi:
```text
Konteyner hajmi: 3
```

---

# 548-Topshiriq: Shablonli Kvadrat Ildiz (Compile-time Sqrt)

## Topshiriq sharti:
`constexpr` funksiya yordamida kvadrat ildizni kompilyatsiyada Nyuton usuli bilan hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

constexpr double sqrtNyuton(double x, double joriy, double oldingi) {
    return (joriy == oldingi) ? joriy : sqrtNyuton(x, 0.5 * (joriy + x / joriy), joriy);
}

constexpr double kompilIldiz(double x) {
    return (x >= 0) ? sqrtNyuton(x, x, 0) : 0;
}

int main() {
    constexpr double ildiz25 = kompilIldiz(25.0);
    std::cout << "sqrt(25.0) = " << ildiz25 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Nyuton-Rafson iteratsiyasi `constexpr` rekursiya orqali kompilyatsiyada aniq natija beradi.

## Ishlash natijasi:
```text
sqrt(25.0) = 5
```

---

# 549-Topshiriq: Shablon kodining shishishi (Code Bloat) va uni kamaytirish

## Topshiriq sharti:
Har bir tur uchun yangi kod generatsiya bo'lishi va umumiy qismlarni `void*` orqali birlashtirish amaliyotini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Code Bloat - har bir T turi uchun alohida mashina kodi generatsiya bo'lib, "
              << "bajariluvchi fayl hajmining oshib ketishi. Yechim: umumiy qismlarni merosxo'rlik orqali ajratish." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta shablon sinflarida umumiy mantiq alohida polimorfik bo'lmagan asosiy sinfga chiqariladi.

## Ishlash natijasi:
```text
Code Bloat - har bir T turi uchun alohida mashina kodi generatsiya bo'lib, bajariluvchi fayl hajmining oshib ketishi. Yechim: umumiy qismlarni merosxo'rlik orqali ajratish.
```

---

# 550-Topshiriq: 11-qism xulosasi: C++ da Shablonlar va Konseptlar Quvvati

## Topshiriq sharti:
Shablonlar va C++20 Konseptlari kompilyatsiya bosqichida maksimal tip xavfsizligi va mutlaq nol unumdorlik yo'qotilishini (Zero Overhead) ta'minlaydi.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "C++ Shablonlari va C++20 Konseptlari - dasturlash olamidagi eng qudratli "
              << "kompilyatsiya vaqtidagi meta-dasturlash tizimidir!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shablonlar C++ ning o'ziga xos eng ustun qurolidir.

## Ishlash natijasi:
```text
C++ Shablonlari va C++20 Konseptlari - dasturlash olamidagi eng qudratli kompilyatsiya vaqtidagi meta-dasturlash tizimidir!
```

---

