# C++ Dasturlash Tili - 9-Qism: Merosxo'rlik va Polimorfizm (Inheritance and Polymorphism)

Ushbu qismda merosxo'rlik turlari, virtual funksiyalar, abstrakt sinflar, VTable, dynamic_cast, RTTI, dizayn andozalari va CRTP ga oid 50 ta amaliy topshiriq jamlangan.

---

# 401-Topshiriq: Merosxo'rlik (Inheritance) asoslari

## Topshiriq sharti:
Asosiy `Hayvon` sinfidan hosila `It` sinfini meros oling va umumiy metodni chaqiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Hayvon {
public:
    void nafasOlish() {
        std::cout << "Nafas olmoqda..." << std::endl;
    }
};

class It : public Hayvon {
public:
    void vovullash() {
        std::cout << "Vov-vov!" << std::endl;
    }
};

int main() {
    It it;
    it.nafasOlish(); // Asosiy sinfdan meros
    it.vovullash();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Hosila sinf asosiy sinfning barcha public imkoniyatlariga ega bo'ladi.

## Ishlash natijasi:
```text
Nafas olmoqda...\nVov-vov!
```

---

# 402-Topshiriq: Merosxo'rlik ko'rinish darajalari (public, protected, private)

## Topshiriq sharti:
`protected` a'zo hosila sinfda ko'rinishi, lekin tashqaridan yopiq bo'lishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asos {
protected:
    int xavfsizSon = 77;
};

class Bola : public Asos {
public:
    void korsat() {
        std::cout << "Bola sinfda ko'rindi: " << xavfsizSon << std::endl;
    }
};

int main() {
    Bola b;
    b.korsat();
    // b.xavfsizSon; // Kompilyatsiya xatosi: tashqaridan yopiq
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `protected` a'zolar tashqi dunyodan yashirin, ammo voris sinflarga ochiq bo'ladi.

## Ishlash natijasi:
```text
Bola sinfda ko'rindi: 77
```

---

# 403-Topshiriq: Hosila sinfda asosiy sinf konstruktorini chaqirish

## Topshiriq sharti:
Hosila sinf konstruktori initsializatsiya ro'yxatida asosiy sinf konstruktoriga parametr uzating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

class Shaxs {
public:
    std::string ism;
    Shaxs(std::string i) : ism(i) {}
};

class Xodim : public Shaxs {
public:
    int oylik;
    Xodim(std::string i, int o) : Shaxs(i), oylik(o) {}
};

int main() {
    Xodim x("Javohir", 4500);
    std::cout << x.ism << " - $" << x.oylik << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `Shaxs(i)` orqali avval asosiy sinf maydonlari quriladi, so'ngra hosila sinf.

## Ishlash natijasi:
```text
Javohir - $4500
```

---

# 404-Topshiriq: Konstruktor va Destruktorlar chaqirilish tartibi

## Topshiriq sharti:
Merosxo'rlikda konstruktorlar yuqoridan pastga, destruktorlar esa pastdan yuqoriga chaqirilishini isbotlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asosiy {
public:
    Asosiy() { std::cout << "Asosiy konstruktor\n"; }
    ~Asosiy() { std::cout << "Asosiy destruktor\n"; }
};

class Hosila : public Asosiy {
public:
    Hosila() { std::cout << "Hosila konstruktor\n"; }
    ~Hosila() { std::cout << "Hosila destruktor\n"; }
};

int main() {
    {
        Hosila h;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Asosiy quriladi -> Hosila quriladi -> Hosila yo'qotiladi -> Asosiy yo'qotiladi.

## Ishlash natijasi:
```text
Asosiy konstruktor\nHosila konstruktor\nHosila destruktor\nAsosiy destruktor
```

---

# 405-Topshiriq: Metodni qayta aniqlash (Method Overriding)

## Topshiriq sharti:
Hosila sinfda asosiy sinf metodini o'ziga xos mantiq bilan almashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Ota {
public:
    void salom() { std::cout << "Salom, men ota sinfman." << std::endl; }
};

class Bola : public Ota {
public:
    void salom() { std::cout << "Salom, men bola sinfman." << std::endl; }
};

int main() {
    Bola b;
    b.salom();
    b.Ota::salom(); // Otasining asl metodiga murojaat
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bola sinf o'z versiyasini chaqiradi, `Ota::salom()` esa asl metodga kirish beradi.

## Ishlash natijasi:
```text
Salom, men bola sinfman.\nSalom, men ota sinfman.
```

---

# 406-Topshiriq: Name Hiding va using Base::metod

## Topshiriq sharti:
Hosila sinfdagi metod asosiy sinfdagi bir xil nomli barcha variantlarni yashirib qo'yishi va uni ochishni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asos {
public:
    void chopEt(int x) { std::cout << "Int: " << x << std::endl; }
    void chopEt(double d) { std::cout << "Double: " << d << std::endl; }
};

class Hosila : public Asos {
public:
    using Asos::chopEt; // Yashirilgan metodlarni ochish
    void chopEt(const char* s) { std::cout << "Satr: " << s << std::endl; }
};

int main() {
    Hosila h;
    h.chopEt(42);
    h.chopEt("Antigravity");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `using Asos::chopEt;` asosiy sinfdagi qayta yuklangan metodlarni hosila sinfga qaytaradi.

## Ishlash natijasi:
```text
Int: 42\nSatr: Antigravity
```

---

# 407-Topshiriq: Statik va Dinamik bog'lanish farqi

## Topshiriq sharti:
Oddiy metod ko'rsatkich toifasiga qarab (statik) chaqirilishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asos {
public:
    void xabar() { std::cout << "Asosiy xabar" << std::endl; }
};

class Hosila : public Asos {
public:
    void xabar() { std::cout << "Hosila xabar" << std::endl; }
};

int main() {
    Hosila h;
    Asos* p = &h;
    p->xabar(); // Asosiy xabar chiqadi (Statik bog'lanish)
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `virtual` bo'lmagan metodlar ko'rsatkichning kompilyatsiya vaqtidagi turiga qarab chaqiriladi.

## Ishlash natijasi:
```text
Asosiy xabar
```

---

# 408-Topshiriq: Virtual funksiyalar (virtual methods)

## Topshiriq sharti:
`virtual` kalit so'zi yordamida dinamik (ish vaqtidagi) polimorfizmni ishga tushiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asos {
public:
    virtual void xabar() { std::cout << "Asosiy virtual" << std::endl; }
};

class Hosila : public Asos {
public:
    void xabar() override { std::cout << "Hosila virtual" << std::endl; }
};

int main() {
    Hosila h;
    Asos* p = &h;
    p->xabar(); // Endi Hosila virtual chiqadi!
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `virtual` metod haqiqiy obyekt turiga qarab runtime da chaqiriladi.

## Ishlash natijasi:
```text
Hosila virtual
```

---

# 409-Topshiriq: override kalit so'zi (C++11)

## Topshiriq sharti:
`override` yordamida imzo xatolarini kompilyator aniqlashini ta'minlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asosiy {
public:
    virtual void hisobla(int a) { std::cout << "Asosiy: " << a << std::endl; }
};

class Hosila : public Asosiy {
public:
    void hisobla(int a) override { // To'g'ri override
        std::cout << "Hosila: " << (a * 2) << std::endl;
    }
};

int main() {
    Hosila h;
    Asosiy* p = &h;
    p->hisobla(5);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `override` agar asosiy sinfda mos virtual funksiya topilmasa, darhol kompilyatsiya xatosi beradi.

## Ishlash natijasi:
```text
Hosila: 10
```

---

# 410-Topshiriq: final kalit so'zi

## Topshiriq sharti:
Metodni boshqa override qilishni yoki sinfdan meros olishni taqiqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class OxirgiSinf final {
public:
    void salom() { std::cout << "Mendan boshqa sinf meros ololmaydi!" << std::endl; }
};

// class Bola : public OxirgiSinf {}; // Kompilyatsiya xatosi!

int main() {
    OxirgiSinf o;
    o.salom();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `final` sinf ierarxiyasini yopish va optimallashtirish (devirtualization) uchun ishlatiladi.

## Ishlash natijasi:
```text
Mendan boshqa sinf meros ololmaydi!
```

---

# 411-Topshiriq: Virtual Destruktor zarurati

## Topshiriq sharti:
Base pointer orqali delete qilinganda xotira sizmasligi uchun virtual destruktor yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asos {
public:
    virtual ~Asos() { std::cout << "Asos destruktori\n"; }
};

class Hosila : public Asos {
    int* ptr;
public:
    Hosila() : ptr(new int[10]) {}
    ~Hosila() override {
        delete[] ptr;
        std::cout << "Hosila destruktori (Xotira tozalandi)\n";
    }
};

int main() {
    Asos* p = new Hosila();
    delete p; // Virtual destruktor tufayli ikkala destruktor ham to'g'ri ishlaydi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Polimorfik asosiy sinflarda doimo destruktor `virtual` bo'lishi shart.

## Ishlash natijasi:
```text
Hosila destruktori (Xotira tozalandi)\nAsos destruktori
```

---

# 412-Topshiriq: Sof virtual funksiya (Pure Virtual Function)

## Topshiriq sharti:
`= 0` orqali hosila sinflar majburiy ravishda realizatsiya qilishi kerak bo'lgan sof virtual metod yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Shakl {
public:
    virtual double yuzasi() const = 0; // Sof virtual funksiya
    virtual ~Shakl() = default;
};

int main() {
    // Shakl s; // Xato! Abstrakt sinfdan obyekt yaratib bo'lmaydi
    std::cout << "Sof virtual metod obyekt yaratishni taqiqlaydi va qat'iy interfeys beradi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kamida bitta sof virtual funksiyasi bor sinf Abstrakt sinf deyiladi.

## Ishlash natijasi:
```text
Sof virtual metod obyekt yaratishni taqiqlaydi va qat'iy interfeys beradi.
```

---

# 413-Topshiriq: Abstrakt sinfdan meros olish va amalga oshirish

## Topshiriq sharti:
`Shakl` abstrakt sinfidan meros olib `Kvadrat` sinfini to'liq ishlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Shakl {
public:
    virtual double yuzasi() const = 0;
    virtual ~Shakl() = default;
};

class Kvadrat : public Shakl {
    double tomon;
public:
    Kvadrat(double t) : tomon(t) {}
    double yuzasi() const override {
        return tomon * tomon;
    }
};

int main() {
    Kvadrat k(6.0);
    std::cout << "Kvadrat yuzasi: " << k.yuzasi() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Barcha sof virtual funksiyalari aniqlangach, sinfdan bemalol obyekt olinishi mumkin.

## Ishlash natijasi:
```text
Kvadrat yuzasi: 36
```

---

# 414-Topshiriq: Polimorfik interfeys orqali turli obyektlarni boshqarish

## Topshiriq sharti:
Asosiy sinf ko'rsatkichi orqali aylana va to'g'ri to'rtburchak yuzalarini bir xil kod bilan hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <memory>

class Shakl {
public:
    virtual void chizish() const = 0;
    virtual ~Shakl() = default;
};

class Aylana : public Shakl {
public:
    void chizish() const override { std::cout << "O Aylana chizildi" << std::endl; }
};

class Kvadrat : public Shakl {
public:
    void chizish() const override { std::cout << "[] Kvadrat chizildi" << std::endl; }
};

int main() {
    std::vector<std::unique_ptr<Shakl>> shakllar;
    shakllar.push_back(std::make_unique<Aylana>());
    shakllar.push_back(std::make_unique<Kvadrat>());
    for (const auto& sh : shakllar) {
        sh->chizish();
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Polimorfizm yordamida kod umumlashtiriladi va yangi shakllar osongina qo'shiladi.

## Ishlash natijasi:
```text
O Aylana chizildi\n[] Kvadrat chizildi
```

---

# 415-Topshiriq: VTable va vptr mexanizmi

## Topshiriq sharti:
Virtual funksiyalari bor obyekt ichida yashirin `vptr` ko'rsatkichi joylashishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Oddiy {
    int x;
};

class Polimorfik {
    int x;
    virtual void f() {}
};

int main() {
    std::cout << "sizeof(Oddiy): " << sizeof(Oddiy) << " bayt\n";
    std::cout << "sizeof(Polimorfik): " << sizeof(Polimorfik) << " bayt (4 bayt int + 8 bayt vptr + padding)\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir polimorfik obyekt VTable jadvaliga ko'rsatuvchi 8 baytli yashirin `vptr` ga ega bo'ladi.

## Ishlash natijasi:
```text
sizeof(Oddiy): 4 bayt\nsizeof(Polimorfik): 16 bayt (4 bayt int + 8 bayt vptr + padding)
```

---

# 416-Topshiriq: Ko'p qirrali merosxo'rlik (Multiple Inheritance)

## Topshiriq sharti:
Bitta hosila sinf bir vaqtning o'zida ikkita asosiy sinfdan meros olishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Printer {
public:
    void chopEtish() { std::cout << "Chop etilmoqda..." << std::endl; }
};

class Skaner {
public:
    void skanerlash() { std::cout << "Skanerlanmoqda..." << std::endl; }
};

class MFP : public Printer, public Skaner {};

int main() {
    MFP mfp;
    mfp.chopEtish();
    mfp.skanerlash();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. MFP ikkala ota sinfning metodlarini birlashtiradi.

## Ishlash natijasi:
```text
Chop etilmoqda...\nSkanerlanmoqda...
```

---

# 417-Topshiriq: Olmos merosxo'rligi muammosi (Diamond Problem)

## Topshiriq sharti:
Bir asosiy sinf ikki tarmoq orqali bitta vorisga kelib tushganda noaniqlik chiqishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Qurilma { int quvvat = 100; };
struct Ekran : public Qurilma {};
struct Klaviatura : public Qurilma {};
// struct Noutbuk : public Ekran, public Klaviatura {}; // Qurilma ikki marta nusxalanadi!

int main() {
    std::cout << "Diamond problem - bitta asos sinfning ikki nusxasi hosil bo'lishi xatosi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ushbu noaniqlikni hal qilish uchun virtual merosxo'rlik ishlatiladi.

## Ishlash natijasi:
```text
Diamond problem - bitta asos sinfning ikki nusxasi hosil bo'lishi xatosi.
```

---

# 418-Topshiriq: Virtual merosxo'rlik (virtual inheritance)

## Topshiriq sharti:
`virtual public` orqali Olmos muammosini hal qilib, bitta umumiy nusxani kafolatlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Qurilma { int quvvat = 100; };
struct Ekran : virtual public Qurilma {};
struct Klaviatura : virtual public Qurilma {};
struct Noutbuk : public Ekran, public Klaviatura {};

int main() {
    Noutbuk n;
    std::cout << "Noutbuk quvvati: " << n.quvvat << "%" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `virtual public` umumiy ota sinfning faqat bitta bo'lishini ta'minlaydi.

## Ishlash natijasi:
```text
Noutbuk quvvati: 100%
```

---

# 419-Topshiriq: dynamic_cast asoslari (Downcasting)

## Topshiriq sharti:
`dynamic_cast` yordamida asosiy sinf ko'rsatkichini hosila sinf ko'rsatkichiga xavfsiz o'giring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asos { public: virtual ~Asos() = default; };
class Hosila : public Asos {
public:
    void maxsus() { std::cout << "Hosila sinfi maxsus amali!" << std::endl; }
};

int main() {
    Asos* a = new Hosila();
    Hosila* h = dynamic_cast<Hosila*>(a);
    if (h != nullptr) {
        h->maxsus();
    }
    delete a;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar haqiqiy obyekt turiga to'g'ri kelsa, ko'rsatkich qaytariladi, aks holda `nullptr`.

## Ishlash natijasi:
```text
Hosila sinfi maxsus amali!
```

---

# 420-Topshiriq: dynamic_cast va havolalar (&)

## Topshiriq sharti:
Havolalar bilan `dynamic_cast` xato bo'lganda `std::bad_cast` istisnosi tashlanishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <typeinfo>

class Ota { public: virtual ~Ota() = default; };
class Bola : public Ota {};
class Boshqa : public Ota {};

int main() {
    Bola b;
    Ota& ref = b;
    try {
        Boshqa& xato = dynamic_cast<Boshqa&>(ref);
        (void)xato;
    } catch (const std::bad_cast& e) {
        std::cout << "bad_cast ushlandi: Noto'g'ri havola o'girilishi!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Reference hech qachon nullptr bo'lolmagani sababli, `dynamic_cast` istisno (exception) tashlaydi.

## Ishlash natijasi:
```text
bad_cast ushlandi: Noto'g'ri havola o'girilishi!
```

---

# 421-Topshiriq: typeid va RTTI (Run-Time Type Information)

## Topshiriq sharti:
`typeid` operatori orqali ish vaqtida obyektning haqiqiy tur nomini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <typeinfo>

class Hayvon { public: virtual ~Hayvon() = default; };
class Mushuk : public Hayvon {};

int main() {
    Hayvon* h = new Mushuk();
    std::cout << "Obyekt turi: " << typeid(*h).name() << std::endl;
    delete h;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. RTTI dastur ishlayotgan paytda virtual jadvallar orqali tip ma'lumotlarini o'qiydi.

## Ishlash natijasi:
```text
Obyekt turi: ...
```

---

# 422-Topshiriq: static_cast orqali tezkor Downcasting

## Topshiriq sharti:
Turi 100% aniq bo'lganda `dynamic_cast` xarajatlarisiz `static_cast` bilan o'girish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Base { public: virtual ~Base() = default; };
class Derived : public Base {
public:
    void salom() { std::cout << "Tezkor static_cast" << std::endl; }
};

int main() {
    Base* b = new Derived();
    Derived* d = static_cast<Derived*>(b); // Ish vaqtida tekshiruvsiz tezkor o'girish
    d->salom();
    delete b;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `static_cast` VTable ni tekshirmaydi, shuning uchun juda tez ishlaydi, ammo xavfsizlik dasturchi zimmasida.

## Ishlash natijasi:
```text
Tezkor static_cast
```

---

# 423-Topshiriq: Obyektni kesib tashlash muammosi (Object Slicing)

## Topshiriq sharti:
Obyekt qiymat bo'yicha tayinlanganda hosila sinf maydonlari yo'qolib qolishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asos {
public:
    int a = 1;
};

class Hosila : public Asos {
public:
    int b = 2;
};

int main() {
    Hosila h;
    Asos asos = h; // Object slicing! Faqat 'a' ko'chiriladi, 'b' kesib tashlanadi
    std::cout << "asos.a = " << asos.a << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Polimorfizmda obyektlarni nusxalash emas, ko'rsatkich yoki havola orqali boshqarish lozim.

## Ishlash natijasi:
```text
asos.a = 1
```

---

# 424-Topshiriq: Kovariant qaytarish turlari (Covariant Return Types)

## Topshiriq sharti:
Virtual metod hosila sinfda o'z sinfi ko'rsatkichini qaytarishi mumkinligini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asos {
public:
    virtual Asos* klonlash() { return new Asos(*this); }
    virtual ~Asos() = default;
};

class Hosila : public Asos {
public:
    Hosila* klonlash() override { return new Hosila(*this); } // Kovariant tur
};

int main() {
    Hosila h;
    Hosila* nusxa = h.klonlash();
    std::cout << "Kovariant klonlash muvaffaqiyatli bajarildi." << std::endl;
    delete nusxa;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kovariantlik hosila sinf metodiga aniqroq qaytarish toifasini berishga ruxsat etadi.

## Ishlash natijasi:
```text
Kovariant klonlash muvaffaqiyatli bajarildi.
```

---

# 425-Topshiriq: Prototype andozasi (clone() metodi)

## Topshiriq sharti:
Polimorfik obyektlardan to'g'ri nusxa olish uchun virtual `clone()` metodini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

class Qahramon {
public:
    virtual std::unique_ptr<Qahramon> clone() const = 0;
    virtual void jang() const = 0;
    virtual ~Qahramon() = default;
};

class Jangchi : public Qahramon {
public:
    std::unique_ptr<Qahramon> clone() const override {
        return std::make_unique<Jangchi>(*this);
    }
    void jang() const override { std::cout << "Qilich bilan zarba!" << std::endl; }
};

int main() {
    std::unique_ptr<Qahramon> j1 = std::make_unique<Jangchi>();
    auto j2 = j1->clone();
    j2->jang();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Virtual konstruktor bo'lmagani sababli `clone()` Prototype andozasini yaratadi.

## Ishlash natijasi:
```text
Qilich bilan zarba!
```

---

# 426-Topshiriq: Interfeys sinfi (Interface in C++)

## Topshiriq sharti:
Faqat sof virtual funksiyalardan iborat toza interfeys sinfini e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class ILoglovchi {
public:
    virtual void log(const char* xabar) = 0;
    virtual ~ILoglovchi() = default;
};

class KonsolLog : public ILoglovchi {
public:
    void log(const char* xabar) override {
        std::cout << "[LOG]: " << xabar << std::endl;
    }
};

int main() {
    KonsolLog logger;
    logger.log("Tizim barqaror ishlayapti.");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Interfeys sinflari tizim modullari o'rtasidagi erkin bog'lanishni (loose coupling) ta'minlaydi.

## Ishlash natijasi:
```text
[LOG]: Tizim barqaror ishlayapti.
```

---

# 427-Topshiriq: Bir nechta interfeyslarni amalga oshirish

## Topshiriq sharti:
Bitta sinf bir vaqtning o'zida bir nechta interfeysni to'liq qanoatlantirishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class IChopQiluvchi { public: virtual void chop() = 0; virtual ~IChopQiluvchi() = default; };
class ISaqlagich { public: virtual void saqla() = 0; virtual ~ISaqlagich() = default; };

class Hujjat : public IChopQiluvchi, public ISaqlagich {
public:
    void chop() override { std::cout << "Hujjat chop etildi." << std::endl; }
    void saqla() override { std::cout << "Hujjat saqlandi." << std::endl; }
};

int main() {
    Hujjat h;
    h.chop();
    h.saqla();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bir nechta sof interfeyslarni meros olish C++ da xavfsiz va tavsiya etilgan amaliyotdir.

## Ishlash natijasi:
```text
Hujjat chop etildi.\nHujjat saqlandi.
```

---

# 428-Topshiriq: Kompozitsiya merosxo'rlikdan afzal (Composition over Inheritance)

## Topshiriq sharti:
Meros olish o'rniga obyektni o'z ichiga a'zo sifatida joylashtirishni (Has-A munosabati) ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Dvigatel {
public:
    void start() { std::cout << "Dvigatel o't oldi." << std::endl; }
};

class Mashina {
    Dvigatel dvigatel; // Kompozitsiya: Mashinada dvigatel bor (Has-A)
public:
    void haydash() {
        dvigatel.start();
        std::cout << "Mashina harakatlanmoqda." << std::endl;
    }
};

int main() {
    Mashina m;
    m.haydash();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompozitsiya tizimni yanada moslashuvchan qiladi va qattiq bog'liqlikni yo'qotadi.

## Ishlash natijasi:
```text
Dvigatel o't oldi.\nMashina harakatlanmoqda.
```

---

# 429-Topshiriq: Bog'liqlikni kiritish (Dependency Injection)

## Topshiriq sharti:
Sinfga kerakli xizmatni konstruktor orqali interfeys ko'rinishida uzating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class IXabar {
public:
    virtual void yubor(const char* matn) = 0;
    virtual ~IXabar() = default;
};

class SmsXabar : public IXabar {
public:
    void yubor(const char* matn) override {
        std::cout << "SMS yuborildi: " << matn << std::endl;
    }
};

class Bildirishnoma {
    IXabar& xizmat;
public:
    Bildirishnoma(IXabar& x) : xizmat(x) {}
    void xabarBer() { xizmat.yubor("Parolingiz tiklandi"); }
};

int main() {
    SmsXabar sms;
    Bildirishnoma b(sms);
    b.xabarBer();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dependency Injection testlashni (mocking) va tizim qismlarini almashtirishni osonlashtiradi.

## Ishlash natijasi:
```text
SMS yuborildi: Parolingiz tiklandi
```

---

# 430-Topshiriq: Shablon Metod (Template Method) dizayn andozasi

## Topshiriq sharti:
Algoritm skeletini asosiy sinfda belgilab, aniq qadamlarni hosila sinflarga topshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class AlgoritmKarkasi {
public:
    void bajar() {
        qadam1();
        qadam2();
    }
    virtual ~AlgoritmKarkasi() = default;
protected:
    virtual void qadam1() = 0;
    virtual void qadam2() { std::cout << "Standart 2-qadam\n"; }
};

class MeningAlgoritmim : public AlgoritmKarkasi {
protected:
    void qadam1() override { std::cout << "Maxsus 1-qadam\n"; }
};

int main() {
    MeningAlgoritmim a;
    a.bajar();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Umumiy oqim boshqariladi, detallar esa ixtisoslashtiriladi.

## Ishlash natijasi:
```text
Maxsus 1-qadam\nStandart 2-qadam
```

---

# 431-Topshiriq: Strategiya (Strategy) dizayn andozasi

## Topshiriq sharti:
Saralash strategiyasini ish vaqtida almashtirishni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

class ISaralash {
public:
    virtual void sarala() = 0;
    virtual ~ISaralash() = default;
};

class TezkorSaralash : public ISaralash {
public:
    void sarala() override { std::cout << "QuickSort ishlatildi" << std::endl; }
};

class Kontekst {
    std::unique_ptr<ISaralash> strategiya;
public:
    void setStrategiya(std::unique_ptr<ISaralash> s) { strategiya = std::move(s); }
    void bajar() { if (strategiya) strategiya->sarala(); }
};

int main() {
    Kontekst k;
    k.setStrategiya(std::make_unique<TezkorSaralash>());
    k.bajar();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Strategiya andozasi algoritmlar oilasini mustaqil ravishda almashtirish imkonini beradi.

## Ishlash natijasi:
```text
QuickSort ishlatildi
```

---

# 432-Topshiriq: Virtual metodning standart argumenti tuzog'i

## Topshiriq sharti:
Default parametrlar dinamik emas, balki statik bog'lanish asosida olinishi xavfini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Asos {
public:
    virtual void korsat(int x = 10) {
        std::cout << "Asos: " << x << std::endl;
    }
    virtual ~Asos() = default;
};

class Hosila : public Asos {
public:
    void korsat(int x = 20) override {
        std::cout << "Hosila: " << x << std::endl;
    }
};

int main() {
    Hosila h;
    Asos* p = &h;
    p->korsat(); // Hosila kodi ishlaydi, ammo Asosning default qiymati 10 olinadi!
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Hech qachon virtual funksiyalarda turlicha standart argumentlar bermang, chunki default argumentlar kompilyatsiya vaqtida qotiriladi.

## Ishlash natijasi:
```text
Hosila: 10
```

---

# 433-Topshiriq: protected destruktor orqali xavfsizlik

## Topshiriq sharti:
Faqat hosila sinflar orqali boshqarilishini ta'minlash uchun asosiy sinf destruktorini protected qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Interfeys {
protected:
    ~Interfeys() = default; // To'g'ridan-to'g'ri delete taqiqlandi
public:
    virtual void ishla() = 0;
};

class Amal : public Interfeys {
public:
    void ishla() override { std::cout << "Amal bajarildi" << std::endl; }
};

int main() {
    Amal a;
    a.ishla();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu polimorfik bo'lmagan asosiy sinf ko'rsatkichini tasodifiy `delete` qilishdan saqlaydi.

## Ishlash natijasi:
```text
Amal bajarildi
```

---

# 434-Topshiriq: Yopiq merosxo'rlik (private inheritance)

## Topshiriq sharti:
`private` merosxo'rlik faqat amalga oshirishni (implementation) yashirin ko'chirish uchun xizmat qilishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Dvigatel {
public:
    void yoqish() { std::cout << "Dvigatel yondi" << std::endl; }
};

class MaxfiyMashina : private Dvigatel {
public:
    void start() {
        yoqish(); // Ichkarida ishlaydi, ammo tashqariga yopiq
    }
};

int main() {
    MaxfiyMashina m;
    m.start();
    // m.yoqish(); // Xato: private meros bo'lgani uchun yopiq
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yopiq merosxo'rlik Is-A emas, balki Has-A munosabatining maxsus shaklidir.

## Ishlash natijasi:
```text
Dvigatel yondi
```

---

# 435-Topshiriq: CRTP (Curiously Recurring Template Pattern) asoslari

## Topshiriq sharti:
Statik polimorfizm: VTable va vptr siz virtual chaqiruv tezligiga erishing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename Hosila>
class AsosCRTP {
public:
    void salom() {
        static_cast<Hosila*>(this)->amalgaOshir();
    }
};

class MeningSinfim : public AsosCRTP<MeningSinfim> {
public:
    void amalgaOshir() {
        std::cout << "CRTP: Virtual xarajatlarsiz statik polimorfizm!" << std::endl;
    }
};

int main() {
    MeningSinfim obj;
    obj.salom();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. CRTP kompilyatsiya vaqtida to'g'ridan-to'g'ri chaqiruvni bog'laydi va VTable xarajatlarini nolga tushiradi.

## Ishlash natijasi:
```text
CRTP: Virtual xarajatlarsiz statik polimorfizm!
```

---

# 436-Topshiriq: CRTP orqali umumiy qobiliyatlarni kiritish (Mixins)

## Topshiriq sharti:
Sinfga avtomatik tenglik va tengsizlik operatorlarini qo'shuvchi CRTP yordamchisini tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

template <typename T>
struct Taqqoslanuvchi {
    friend bool operator!=(const T& a, const T& b) {
        return !(a == b);
    }
};

class Son : public Taqqoslanuvchi<Son> {
public:
    int val;
    Son(int v) : val(v) {}
    bool operator==(const Son& other) const { return val == other.val; }
};

int main() {
    Son s1(10), s2(20);
    std::cout << "Teng emasmi: " << (s1 != s2 ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Faqat `==` operatorini yozish orqali `!=` operatori CRTP orqali avtomatik ta'minlanadi.

## Ishlash natijasi:
```text
Teng emasmi: Ha
```

---

# 437-Topshiriq: Zavod (Factory Method) dizayn andozasi

## Topshiriq sharti:
Satr parametriga qarab mos polimorfik obyekt yaratib qaytaruvchi Factory funksiyasi.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>
#include <string>

class Transport {
public:
    virtual void harakat() = 0;
    virtual ~Transport() = default;
};
class Qayiq : public Transport { public: void harakat() override { std::cout << "Suvda suzmoqda" << std::endl; } };
class Samolyot : public Transport { public: void harakat() override { std::cout << "Osmonda uchmoqda" << std::endl; } };

std::unique_ptr<Transport> transportZavodi(const std::string& tur) {
    if (tur == "suv") return std::make_unique<Qayiq>();
    return std::make_unique<Samolyot>();
}

int main() {
    auto t = transportZavodi("suv");
    t->harakat();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Factory andozasi yangi sinflar yaratishni chaqiruvchi koddan ajratadi.

## Ishlash natijasi:
```text
Suvda suzmoqda
```

---

# 438-Topshiriq: Kuzatuvchi (Observer) dizayn andozasi

## Topshiriq sharti:
O'zgarishlar haqida obunachilarni polimorfizm orqali xabardor qiluvchi tizim tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class IObunachi {
public:
    virtual void yangilanish(int yangiXabar) = 0;
    virtual ~IObunachi() = default;
};

class Foydalanuvchi : public IObunachi {
public:
    void yangilanish(int x) override {
        std::cout << "Foydalanuvchi yangi qiymat oldi: " << x << std::endl;
    }
};

class Kanal {
    std::vector<IObunachi*> a'zolar;
public:
    void obunaBolish(IObunachi* o) { a'zolar.push_back(o); }
    void xabarTarqat(int x) {
        for (auto* a : a'zolar) a->yangilanish(x);
    }
};

int main() {
    Kanal kanal;
    Foydalanuvchi f;
    kanal.obunaBolish(&f);
    kanal.xabarTarqat(101);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Observer andozasi voqealarga asoslangan (event-driven) tizimlarning poydevoridir.

## Ishlash natijasi:
```text
Foydalanuvchi yangi qiymat oldi: 101
```

---

# 439-Topshiriq: Decorator dizayn andozasi asoslari

## Topshiriq sharti:
Mavjud obyekt funksionalligini polimorfik qobiq bilan kengaytiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

class Qahva {
public:
    virtual double narx() const = 0;
    virtual ~Qahva() = default;
};

class OddiyQahva : public Qahva {
public:
    double narx() const override { return 10.0; }
};

class SutliQahva : public Qahva {
    std::unique_ptr<Qahva> asos;
public:
    SutliQahva(std::unique_ptr<Qahva> q) : asos(std::move(q)) {}
    double narx() const override { return asos->narx() + 3.0; }
};

int main() {
    auto qahva = std::make_unique<SutliQahva>(std::make_unique<OddiyQahva>());
    std::cout << "Sutli qahva narxi: $" << qahva->narx() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Decorator yangi xususiyatlarni sinfni o'zgartirmasdan qatlam-qatlam qo'shish imkonini beradi.

## Ishlash natijasi:
```text
Sutli qahva narxi: $13
```

---

# 440-Topshiriq: Adapter dizayn andozasi

## Topshiriq sharti:
Eski sinf interfeysini yangi kutilayotgan interfeysga moslashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class EskiTermometr {
public:
    double getFarengeyt() { return 86.0; }
};

class ISelsiyTermometr {
public:
    virtual double getSelsiy() = 0;
    virtual ~ISelsiyTermometr() = default;
};

class TermometrAdapter : public ISelsiyTermometr {
    EskiTermometr eski;
public:
    double getSelsiy() override {
        return (eski.getFarengeyt() - 32) * 5.0 / 9.0;
    }
};

int main() {
    TermometrAdapter adapter;
    std::cout << "Harorat: " << adapter.getSelsiy() << " C" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Adapter mos kelmaydigan interfeyslarni birlashtiradi.

## Ishlash natijasi:
```text
Harorat: 30 C
```

---

# 441-Topshiriq: O'yin qahramonlari sinflar ierarxiyasi

## Topshiriq sharti:
Qahramon -> Jangchi, Sehrgar va Kamonchi polimorfik sinflarini tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Qahramon {
public:
    virtual void hujum() const = 0;
    virtual ~Qahramon() = default;
};

class Sehrgar : public Qahramon {
public:
    void hujum() const override { std::cout << "Olovli sharcha sehri!" << std::endl; }
};

int main() {
    Sehrgar s;
    s.hujum();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'yin mexanikalarini modellashtirishning standart usuli.

## Ishlash natijasi:
```text
Olovli sharcha sehri!
```

---

# 442-Topshiriq: Xotirani xavfsiz boshqaruvchi polimorfik ierarxiya

## Topshiriq sharti:
`std::vector<std::unique_ptr<Base>>` orqali hech qanday xotira sizishisiz to'liq tozalanishni isbotlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <memory>

class Resurs {
public:
    virtual ~Resurs() { std::cout << "Resurs tozalandi\n"; }
};
class FaylResurs : public Resurs {
    ~FaylResurs() override { std::cout << "FaylResurs tozalandi\n"; }
};

int main() {
    {
        std::vector<std::unique_ptr<Resurs>> royxat;
        royxat.push_back(std::make_unique<FaylResurs>());
    }
    std::cout << "Massiv xavfsiz tugatildi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Smart pointer va virtual destruktor birgalikda 100% xotira xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
FaylResurs tozalandi\nResurs tozalandi\nMassiv xavfsiz tugatildi.
```

---

# 443-Topshiriq: Dasturiy qatlamlar va Interfeys ajratish tamoyili (ISP)

## Topshiriq sharti:
SOLID tamoyillaridan biri: Katta interfeyslarni kichik va aniq interfeyslarga bo'ling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class IOqish { public: virtual void oqish() = 0; virtual ~IOqish() = default; };
class IYozish { public: virtual void yozish() = 0; virtual ~IYozish() = default; };

class FaqatOquvchiFayl : public IOqish {
public:
    void oqish() override { std::cout << "Faqat o'qish mumkin." << std::endl; }
};

int main() {
    FaqatOquvchiFayl f;
    f.oqish();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Keraksiz metodlarni majburlamaslik uchun interfeyslar mayda bo'lishi kerak.

## Ishlash natijasi:
```text
Faqat o'qish mumkin.
```

---

# 444-Topshiriq: Liskov O'rnini Bosish Tamoyili (LSP)

## Topshiriq sharti:
Hosila sinf asosiy sinf kutilgan joyda uning mantiqiy shartlarini buzmasdan ishlay olishi shartligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class ParvozQiluvchiQush {
public:
    virtual void uchish() { std::cout << "Qush uchmoqda" << std::endl; }
    virtual ~ParvozQiluvchiQush() = default;
};

class Qaldirgoch : public ParvozQiluvchiQush {};

int main() {
    Qaldirgoch q;
    q.uchish();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. LSP buzilmasligi uchun uchmaydigan qushlar (masalan Pingvin) uchish interfeysidan meros olmasligi kerak.

## Ishlash natijasi:
```text
Qush uchmoqda
```

---

# 445-Topshiriq: Virtual funksiyalar va kompilyator devirtualizatsiyasi

## Topshiriq sharti:
Kompilyator obyektning aniq turini bilsa, virtual chaqiruvni to'g'ridan-to'g'ri chaqiruvga aylantirishini (Devirtualization) tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class A { public: virtual void test() { std::cout << "A::test" << std::endl; } };

int main() {
    A a;
    a.test(); // Ko'rsatkich orqali emas, to'g'ridan-to'g'ri chaqiruv: Devirtualization ishlaydi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyator aniq obyektda VTable ga kirmasdan to'g'ridan-to'g'ri bog'laydi.

## Ishlash natijasi:
```text
A::test
```

---

# 446-Topshiriq: Interfeys invariantlarini tekshiruvchi NVI (Non-Virtual Interface) Idiomasi

## Topshiriq sharti:
Public no-virtual metod orqali shartlarni tekshirib, private virtual metodni chaqiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class NviAsos {
public:
    void bajar() {
        std::cout << "[Oldingi tekshiruv]\n";
        amalgaOshir();
        std::cout << "[Keyingi tozalash]\n";
    }
    virtual ~NviAsos() = default;
private:
    virtual void amalgaOshir() = 0;
};

class NviHosila : public NviAsos {
private:
    void amalgaOshir() override {
        std::cout << "Asosiy mantiq bajarildi\n";
    }
};

int main() {
    NviHosila obj;
    obj.bajar();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. NVI idiomasi asosiy sinfga invariantlar va tekshiruvlar ustidan to'liq nazoratni beradi.

## Ishlash natijasi:
```text
[Oldingi tekshiruv]\nAsosiy mantiq bajarildi\n[Keyingi tozalash]
```

---

# 447-Topshiriq: Virtual metodlar bilan xotira keshining buzilishi (Cache Misses)

## Topshiriq sharti:
Nima uchun virtual metod chaqiruvlari CPU ko'rsatkich sakrashlari tufayli sekinroq bo'lishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "VTable orqali murojaat bilvosita (indirect) bo'lgani sababli "
              << "CPU branch predictor va instruction keshiga qo'shimcha yuklama beradi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yuqori unumdor tizimlarda va AI dvigatellarida ko'pincha statik polimorfizm (CRTP yoki shablonlar) tanlanadi.

## Ishlash natijasi:
```text
VTable orqali murojaat bilvosita (indirect) bo'lgani sababli CPU branch predictor va instruction keshiga qo'shimcha yuklama beradi.
```

---

# 448-Topshiriq: Polimorfik Serialization (Ma'lumotlarni oqimga yozish)

## Topshiriq sharti:
Har bir sinf o'zini JSON yoki matn shaklida ifodalashini ta'minlovchi virtual metod.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

class ISerializable {
public:
    virtual std::string toJson() const = 0;
    virtual ~ISerializable() = default;
};

class Foydalanuvchi : public ISerializable {
    std::string ism = "Ali";
public:
    std::string toJson() const override {
        return "{\"ism\": \"" + ism + "\"}";
    }
};

int main() {
    Foydalanuvchi f;
    std::cout << f.toJson() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Barcha modellar o'z ma'lumotlarini standart formatda eksport qiladi.

## Ishlash natijasi:
```text
{"ism": "Ali"}
```

---

# 449-Topshiriq: Abstrakt sinflar orqali AI Modeli dvigateli interfeysi

## Topshiriq sharti:
Neyron tarmoqlar qatlamlari uchun umumiy `ILayer` interfeysini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class ILayer {
public:
    virtual void forward(const std::vector<float>& kirish) = 0;
    virtual ~ILayer() = default;
};

class DenseLayer : public ILayer {
public:
    void forward(const std::vector<float>& kirish) override {
        std::cout << "Dense Layer: " << kirish.size() << " ta kiruvchi tensor hisoblandi." << std::endl;
    }
};

int main() {
    DenseLayer layer;
    std::vector<float> input = {0.5f, -0.2f, 0.9f};
    layer.forward(input);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Neyron tarmoqlarning qatlamlari shu tarzda abstraktlashtirilib ketma-ket ulanadi.

## Ishlash natijasi:
```text
Dense Layer: 3 ta kiruvchi tensor hisoblandi.
```

---

# 450-Topshiriq: 9-qism xulosasi: Merosxo'rlik va Polimorfizm Me'morchiligi

## Topshiriq sharti:
Dinamik polimorfizm (VTable) moslashuvchanlik uchun, Statik polimorfizm (CRTP/Templates) esa maksimal unumdorlik uchun xizmat qilishini xulosa qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "C++ da polimorfizm: Runtime moslashuvchanlik va Compile-time maksimal tezlikning mukammal balansi!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Merosxo'rlik va polimorfizm dastur me'morchiligining poydevori hisoblanadi.

## Ishlash natijasi:
```text
C++ da polimorfizm: Runtime moslashuvchanlik va Compile-time maksimal tezlikning mukammal balansi!
```

---

