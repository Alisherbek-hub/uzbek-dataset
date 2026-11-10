# C++ Dasturlash Tili - 8-Qism: Obyektga Yo'naltirilgan Dasturlash (Klasslar va Obyektlar)

Ushbu qismda klasslar, obyektlar, konstruktorlar turlari, enkapsulyatsiya, static a'zolar, this, funktorlar va chuqur nusxalashga oid 50 ta amaliy topshiriq jamlangan.

---

# 351-Topshiriq: Klass va Obyekt tushunchasi

## Topshiriq sharti:
Oddiy `Avtomobil` klassini e'lon qilib, uning obyektini yarating va ma'lumotlarini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

class Avtomobil {
public:
    std::string model;
    int yil;
};

int main() {
    Avtomobil avto1;
    avto1.model = "Chevrolet Tracker";
    avto1.yil = 2024;
    std::cout << "Model: " << avto1.model << ", Yil: " << avto1.yil << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Klass - bu ma'lumotlar va metodlar uchun qolip (chizma), obyekt esa shu qolipdan yaratilgan aniq namunadir.

## Ishlash natijasi:
```text
Model: Chevrolet Tracker, Yil: 2024
```

---

# 352-Topshiriq: Kirish huquqlari: public, private, protected

## Topshiriq sharti:
Klass a'zolarini ochiq (public) va yopiq (private) bo'limlarga ajrating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Foydalanuvchi {
private:
    int parolKodi = 1234; // Faqat sinf ichida ko'rinadi
public:
    int id = 101;
    bool parolTogrimi(int kiritilgan) {
        return kiritilgan == parolKodi;
    }
};

int main() {
    Foydalanuvchi user;
    std::cout << "User ID: " << user.id << std::endl;
    std::cout << "Parol tekshiruvi: " << (user.parolTogrimi(1234) ? "To'g'ri" : "Xato") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `private` a'zolar tashqi koddan yashirin bo'lib, to'g'ridan-to'g'ri o'zgartirilishdan himoyalanadi.

## Ishlash natijasi:
```text
User ID: 101\nParol tekshiruvi: To'g'ri
```

---

# 353-Topshiriq: Maydonlar va Metodlar

## Topshiriq sharti:
Klass ichida o'zgaruvchilar va ularni ishlatuvchi a'zo funksiyalarni e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Doira {
public:
    double radius;
    double yuzasi() {
        return 3.14159 * radius * radius;
    }
};

int main() {
    Doira d;
    d.radius = 5.0;
    std::cout << "Doira yuzasi: " << d.yuzasi() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Metodlar sinf maydonlari ustida amallar bajaradi.

## Ishlash natijasi:
```text
Doira yuzasi: 78.5397
```

---

# 354-Topshiriq: Enkapsulyatsiya: Getter va Setter metodlari

## Topshiriq sharti:
Yopiq maydonga kirish va uni tekshirib o'zgartirish uchun `get` va `set` metodlarini tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Inson {
private:
    int yosh;
public:
    void setYosh(int y) {
        if (y > 0 && y < 150) {
            yosh = y;
        }
    }
    int getYosh() const {
        return yosh;
    }
};

int main() {
    Inson i;
    i.setYosh(25);
    std::cout << "Yosh: " << i.getYosh() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Setter noto'g'ri qiymatlar (masalan manfiy yosh) kiritilishining oldini oladi.

## Ishlash natijasi:
```text
Yosh: 25
```

---

# 355-Topshiriq: Standart konstruktor (Default Constructor)

## Topshiriq sharti:
Obyekt yaratilganda avtomatik ishga tushadigan parametrsiz konstruktor yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Mahsulot {
public:
    Mahsulot() {
        std::cout << "Yangi mahsulot obyekti yaratildi!" << std::endl;
    }
};

int main() {
    Mahsulot m;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Konstruktor nomi sinf nomi bilan bir xil bo'ladi va qaytarish toifasiga ega bo'lmaydi.

## Ishlash natijasi:
```text
Yangi mahsulot obyekti yaratildi!
```

---

# 356-Topshiriq: Parametrli konstruktor

## Topshiriq sharti:
Boshlang'ich qiymatlarni qabul qilib maydonlarga yuklovchi konstruktor tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

class Talaba {
public:
    std::string ism;
    int kurs;
    Talaba(std::string i, int k) {
        ism = i;
        kurs = k;
    }
};

int main() {
    Talaba t("Temur", 3);
    std::cout << t.ism << ", " << t.kurs << "-kurs" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Parametrli konstruktor orqali obyekt bir qatorda qiymatlar bilan yaratiladi.

## Ishlash natijasi:
```text
Temur, 3-kurs
```

---

# 357-Topshiriq: Initsializatsiya ro'yxati (Member Initializer List)

## Topshiriq sharti:
Konstruktor tanasidan oldin ikki nuqta `:` orqali maydonlarni initsializatsiya qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Nuqta {
public:
    int x, y;
    Nuqta(int a, int b) : x(a), y(b) {}
};

int main() {
    Nuqta p(10, 20);
    std::cout << "x = " << p.x << ", y = " << p.y << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Initsializatsiya ro'yxati maydonlarni to'g'ridan-to'g'ri quradi, ortiqcha standart konstruktor chaqiruvidan xalos qiladi.

## Ishlash natijasi:
```text
x = 10, y = 20
```

---

# 358-Topshiriq: const va reference a'zolarni initsializatsiya qilish

## Topshiriq sharti:
Sinfning `const` va havola (`&`) a'zolari faqat initsializatsiya ro'yxatida berilishi mumkinligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Boglama {
public:
    const int id;
    int& havola;
    Boglama(int yangiId, int& h) : id(yangiId), havola(h) {}
};

int main() {
    int qiymat = 50;
    Boglama b(1001, qiymat);
    std::cout << "ID: " << b.id << ", Bog'langan qiymat: " << b.havola << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const` va `&` maydonlar e'lon qilingan zahoti qiymat olishi shart bo'lgani sababli faqat initializer list da beriladi.

## Ishlash natijasi:
```text
ID: 1001, Bog'langan qiymat: 50
```

---

# 359-Topshiriq: Delegatsiya qiluvchi konstruktor (Delegating Constructor - C++11)

## Topshiriq sharti:
Bitta konstruktordan boshqa bir konstruktorni chaqiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

class Xodim {
public:
    std::string ism;
    int oylik;
    Xodim(std::string i, int o) : ism(i), oylik(o) {}
    // Delegatsiya:
    Xodim(std::string i) : Xodim(i, 3000) {}
};

int main() {
    Xodim x("Sardor");
    std::cout << x.ism << " maoshi: " << x.oylik << "$" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kod takrorlanishining oldi olinadi va umumiy mantiq bitta asosiy konstruktorda saqlanadi.

## Ishlash natijasi:
```text
Sardor maoshi: 3000$
```

---

# 360-Topshiriq: Sinf ichida boshlang'ich qiymat berish (In-class member initializers)

## Topshiriq sharti:
Maydonlarni sinf e'lon qilingan joyning o'zida standart qiymat bilan ta'minlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Konfiguratsiya {
public:
    int port = 8080;
    int timeout = 30;
};

int main() {
    Konfiguratsiya cfg;
    std::cout << "Port: " << cfg.port << ", Timeout: " << cfg.timeout << "s" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har qanday konstruktor bu qiymatlarni sukut bo'yicha oladi.

## Ishlash natijasi:
```text
Port: 8080, Timeout: 30s
```

---

# 361-Topshiriq: Nusxalash konstruktori (Copy Constructor) va Shallow Copy muammosi

## Topshiriq sharti:
Standart nusxalash faqat ko'rsatkich manzilini nusxalab qo'yishi natijasida ikki marta o'chirish yuzaga kelishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class OddiyNusxa {
public:
    int* ptr;
    OddiyNusxa(int val) : ptr(new int(val)) {}
    ~OddiyNusxa() { delete ptr; }
};

int main() {
    std::cout << "Shallow copy ko'rsatkichlarni ko'chiradi, bu esa double free ga sabab bo'ladi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dinamik xotirasi bor sinflarda standart nusxalash xavfli bo'lib, chuqur nusxalash (Deep Copy) yozilishi shart.

## Ishlash natijasi:
```text
Shallow copy ko'rsatkichlarni ko'chiradi, bu esa double free ga sabab bo'ladi.
```

---

# 362-Topshiriq: Chuqur nusxalash konstruktori (Deep Copy Constructor)

## Topshiriq sharti:
Dinamik xotirani yangidan ajratib nusxalovchi to'g'ri nusxalash konstruktorini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class ChuqurNusxa {
public:
    int* data;
    ChuqurNusxa(int v) : data(new int(v)) {}
    // Chuqur nusxalash konstruktori:
    ChuqurNusxa(const ChuqurNusxa& other) : data(new int(*other.data)) {}
    ~ChuqurNusxa() { delete data; }
};

int main() {
    ChuqurNusxa c1(42);
    ChuqurNusxa c2 = c1; // Yangi alohida xotira ajratildi
    *c2.data = 99;
    std::cout << "c1: " << *c1.data << ", c2: " << *c2.data << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir obyekt o'zining mustaqil dinamik xotira nusxasiga ega bo'ladi.

## Ishlash natijasi:
```text
c1: 42, c2: 99
```

---

# 363-Topshiriq: explicit konstruktor

## Topshiriq sharti:
Yashirin toifa o'girilishi (implicit conversion) natijasida kutilmagan xatolar chiqmasligi uchun `explicit` dan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Bino {
public:
    int qavatlar;
    explicit Bino(int q) : qavatlar(q) {}
};

void tekshir(Bino b) {
    std::cout << "Qavatlar soni: " << b.qavatlar << std::endl;
}

int main() {
    // tekshir(5); // explicit tufayli xato: 5 avtomatik Bino ga aylanmaydi
    tekshir(Bino(5)); // Faqat oshkora yaratish mumkin
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `explicit` bitta argumentli konstruktorlarning yashirin chaqirilishini to'xtatadi.

## Ishlash natijasi:
```text
Qavatlar soni: 5
```

---

# 364-Topshiriq: Destruktor (~Sinf) va resurslarni tozalash

## Topshiriq sharti:
Obyekt yo'q bo'layotganda destruktor xotirani ozod qilishi va xabar chiqarishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class FaylBoshqaruvchi {
public:
    FaylBoshqaruvchi() { std::cout << "Fayl ochildi" << std::endl; }
    ~FaylBoshqaruvchi() { std::cout << "Fayl avtomatik yopildi" << std::endl; }
};

int main() {
    {
        FaylBoshqaruvchi f;
    }
    std::cout << "Ko'lamdan chiqildi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Destruktor hech qanday parametr qabul qilmaydi va obyekt o'chirilishida avtomatik ishlaydi.

## Ishlash natijasi:
```text
Fayl ochildi\nFayl avtomatik yopildi\nKo'lamdan chiqildi.
```

---

# 365-Topshiriq: this ko'rsatkichi

## Topshiriq sharti:
Konstruktor parametr nomlari va sinf maydonlari bir xil bo'lganda `this->` orqali farqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Talaba {
    int id;
public:
    Talaba(int id) {
        this->id = id; // this joriy obyektga ko'rsatkich
    }
    void chopEt() {
        std::cout << "Talaba ID: " << this->id << std::endl;
    }
};

int main() {
    Talaba t(505);
    t.chopEt();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `this` kalit so'zi metod ichida shu metodni chaqirgan aniq obyekt manzilini saqlaydi.

## Ishlash natijasi:
```text
Talaba ID: 505
```

---

# 366-Topshiriq: Metodlar zanjiri (Method Chaining / Fluent API)

## Topshiriq sharti:
Metodlardan `*this` havolasini qaytarish orqali ketma-ket chaqiruvlarni (`p.setX(1).setY(2)`) amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Piksellar {
    int x = 0, y = 0;
public:
    Piksellar& setX(int a) { x = a; return *this; }
    Piksellar& setY(int b) { y = b; return *this; }
    void korsat() const {
        std::cout << "Piksel: (" << x << ", " << y << ")" << std::endl;
    }
};

int main() {
    Piksellar p;
    p.setX(10).setY(20);
    p.korsat();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `return *this;` joriy obyekt havolasini qaytaradi va metodlarni zanjir kabi ulab ketishga imkon beradi.

## Ishlash natijasi:
```text
Piksel: (10, 20)
```

---

# 367-Topshiriq: const a'zo funksiyalar (const methods)

## Topshiriq sharti:
Obyekt holatini o'zgartirmaydigan funksiyalarni `const` deb belgilang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Hisoblagich {
    int qiymat = 0;
public:
    void oshir() { qiymat++; }
    int getQiymat() const {
        // qiymat++; // Kompilyatsiya xatosi! const metod maydonni o'zgartira olmaydi
        return qiymat;
    }
};

int main() {
    Hisoblagich h;
    h.oshir();
    std::cout << "Qiymat: " << h.getQiymat() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const` metodlar obyektning ichki holatini o'zgartirmaslik kafolatini beradi.

## Ishlash natijasi:
```text
Qiymat: 1
```

---

# 368-Topshiriq: const obyektlar

## Topshiriq sharti:
O'zgarmas `const` obyekt faqat `const` metodlarni chaqira olishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Matn {
    std::string str;
public:
    Matn(std::string s) : str(s) {}
    void oqi() const { std::cout << "Matn: " << str << std::endl; }
    void tozalash() { str = ""; }
};

int main() {
    const Matn m("Muhim hujjat");
    m.oqi(); // To'g'ri, const metod
    // m.tozalash(); // Kompilyatsiya xatosi: const obyektda no-const metod chaqirib bo'lmaydi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const` obyektlar faqat `const` deb belgilangan xavfsiz metodlar bilan ishlashi mumkin.

## Ishlash natijasi:
```text
Matn: Muhim hujjat
```

---

# 369-Topshiriq: mutable kalit so'zi

## Topshiriq sharti:
const metod ichida ham o'zgarishi mumkin bo'lgan statistik maydonni `mutable` deb belgilang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Server {
    mutable int sorovlarSoni = 0;
public:
    void malumotOlish() const {
        sorovlarSoni++; // mutable bo'lgani uchun const metodda ham oshadi
        std::cout << "So'rov qabul qilindi." << std::endl;
    }
    int getSorovlar() const { return sorovlarSoni; }
};

int main() {
    const Server s;
    s.malumotOlish();
    s.malumotOlish();
    std::cout << "Jami so'rovlar: " << s.getSorovlar() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `mutable` keshlar, hisoblagichlar yoki mutexlar kabi obyektning mantiqiy holatini o'zgartirmaydigan yordamchi maydonlar uchun mo'ljallangan.

## Ishlash natijasi:
```text
So'rov qabul qilindi.\nSo'rov qabul qilindi.\nJami so'rovlar: 2
```

---

# 370-Topshiriq: Statik maydonlar (static member variables)

## Topshiriq sharti:
Barcha obyektlar uchun umumiy bo'lgan bitta statik o'zgaruvchini e'lon qiling va tashqarida aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Foydalanuvchi {
public:
    static int umumiySoni;
    Foydalanuvchi() { umumiySoni++; }
};

// Sinfdan tashqarida initsializatsiya:
int Foydalanuvchi::umumiySoni = 0;

int main() {
    Foydalanuvchi f1, f2, f3;
    std::cout << "Jami foydalanuvchilar: " << Foydalanuvchi::umumiySoni << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `static` maydon har bir obyektda alohida emas, butun sinf uchun xotirada bitta nusxada mavjud bo'ladi.

## Ishlash natijasi:
```text
Jami foydalanuvchilar: 3
```

---

# 371-Topshiriq: inline static o'zgaruvchilar (C++17)

## Topshiriq sharti:
C++17 ning `inline static` imkoniyati orqali statik maydonni sinf ichida to'g'ridan-to'g'ri initsializatsiya qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Dvigatel {
public:
    inline static int versiya = 2;
};

int main() {
    std::cout << "Dvigatel versiyasi: " << Dvigatel::versiya << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++17 `inline static` sinfdan tashqarida qayta e'lon qilish majburiyatini bekor qiladi.

## Ishlash natijasi:
```text
Dvigatel versiyasi: 2
```

---

# 372-Topshiriq: Statik metodlar (static member functions)

## Topshiriq sharti:
Obyekt yaratmasdan sinf nomi orqali to'g'ridan-to'g'ri chaqiriluvchi statik metod yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Matematika {
public:
    static int kvadrat(int x) {
        return x * x;
    }
};

int main() {
    int k = Matematika::kvadrat(9);
    std::cout << "9 ning kvadrati: " << k << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Statik metodlar `this` ko'rsatkichiga ega emas va faqat statik maydonlar bilan ishlay oladi.

## Ishlash natijasi:
```text
9 ning kvadrati: 81
```

---

# 373-Topshiriq: Singlton (Singleton) dizayn andozasi (Meyers Singleton)

## Topshiriq sharti:
Dastur bo'yicha faqat bitta nusxada mavjud bo'ladigan xavfsiz Meyer Singleton sinfini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class TizimSozlamasi {
private:
    TizimSozlamasi() {} // Konstruktor yopiq
public:
    TizimSozlamasi(const TizimSozlamasi&) = delete;
    void operator=(const TizimSozlamasi&) = delete;

    static TizimSozlamasi& getInstance() {
        static TizimSozlamasi nusxa; // C++11 dan thread-safe
        return nusxa;
    }
    void salom() { std::cout << "Yagona sozlama nusxasi ishlamoqda." << std::endl; }
};

int main() {
    TizimSozlamasi::getInstance().salom();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mahalliy `static` obyekt orqali yaratilgan Meyers Singleton xotira va ko'p oqimlilik uchun eng xavfsiz hisoblanadi.

## Ishlash natijasi:
```text
Yagona sozlama nusxasi ishlamoqda.
```

---

# 374-Topshiriq: Do'st funksiya (friend function)

## Topshiriq sharti:
Sinfning `private` maydonlariga kirish huquqiga ega tashqi `friend` funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Quti {
private:
    int ogirlik = 50;
    friend void ogirlikniKorsat(const Quti& q);
};

void ogirlikniKorsat(const Quti& q) {
    std::cout << "Quti og'irligi: " << q.ogirlik << " kg" << std::endl;
}

int main() {
    Quti q;
    ogirlikniKorsat(q);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `friend` funksiya sinf a'zosi hisoblanmaydi, ammo yopiq maydonlarga bevosita kirish imtiyoziga ega.

## Ishlash natijasi:
```text
Quti og'irligi: 50 kg
```

---

# 375-Topshiriq: Do'st sinf (friend class)

## Topshiriq sharti:
Bir sinfning barcha a'zolariga boshqa sinfga to'liq ruxsat beruvchi `friend class` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class YashirinBaza {
private:
    int maxfiyKod = 9876;
    friend class Administrator;
};

class Administrator {
public:
    void tekshir(const YashirinBaza& b) {
        std::cout << "Maxfiy kod: " << b.maxfiyKod << std::endl;
    }
};

int main() {
    YashirinBaza baza;
    Administrator admin;
    admin.tekshir(baza);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `friend class` orqali sinflar o'rtasida mustahkam do'stlik aloqasi o'rnatiladi.

## Ishlash natijasi:
```text
Maxfiy kod: 9876
```

---

# 376-Topshiriq: Ichma-ich sinflar (Nested classes)

## Topshiriq sharti:
Boshqa bir sinfning ichida yordamchi sinf e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Kompyuter {
public:
    class Protsessor {
    public:
        void model() { std::cout << "Protsessor: 8 yadroli ARM/x86" << std::endl; }
    };
};

int main() {
    Kompyuter::Protsessor cpu;
    cpu.model();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ichma-ich sinflar tashqi sinf nomlar maydoni bilan mantiqiy guruhlanadi.

## Ishlash natijasi:
```text
Protsessor: 8 yadroli ARM/x86
```

---

# 377-Topshiriq: struct va class farqi

## Topshiriq sharti:
C++ da `struct` standart kirish huquqi public, `class` niki esa private ekanligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct MyStruct {
    int x; // Sukut bo'yicha public
};

class MyClass {
    int y; // Sukut bo'yicha private
public:
    void setY(int val) { y = val; }
    int getY() const { return y; }
};

int main() {
    MyStruct s;
    s.x = 10;
    MyClass c;
    c.setY(20);
    std::cout << "s.x = " << s.x << ", c.y = " << c.getY() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++ da struct va class o'rtasidagi yagona farq: a'zolar va merosxo'rlikning sukut bo'yicha ko'rinish darajasidir.

## Ishlash natijasi:
```text
s.x = 10, c.y = 20
```

---

# 378-Topshiriq: Obyektlar massivi (Array of objects)

## Topshiriq sharti:
Bir nechta obyektlardan iborat massiv yaratib, ularning metodlarini tsiklda chaqiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Kitob {
public:
    int id;
    Kitob(int i = 0) : id(i) {}
    void korsat() const { std::cout << "Kitob #" << id << " "; }
};

int main() {
    Kitob javon[3] = {Kitob(101), Kitob(102), Kitob(103)};
    for (int i = 0; i < 3; ++i) {
        javon[i].korsat();
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Massiv elementlari ketma-ket xotirada joylashadi va har biri uchun konstruktor chaqiriladi.

## Ishlash natijasi:
```text
Kitob #101 Kitob #102 Kitob #103 
```

---

# 379-Topshiriq: Obyektlarni havola bo'yicha funksiyaga uzatish

## Topshiriq sharti:
Obyektni `const Sinf&` orqali uzatish nusxa yaratishning oldini olishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class KattaKlass {
public:
    int data[100];
    KattaKlass() { data[0] = 77; }
};

void tezChopEt(const KattaKlass& k) {
    std::cout << "Birinchi qiymat: " << k.data[0] << std::endl;
}

int main() {
    KattaKlass obj;
    tezChopEt(obj);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Obyektlarni parametr sifatida uzatishda doimo `const &` qo'llash unumdorlik uchun standart hisoblanadi.

## Ishlash natijasi:
```text
Birinchi qiymat: 77
```

---

# 380-Topshiriq: Obyektni funksiyadan qaytarish

## Topshiriq sharti:
Funksiya ichida yaratilgan obyektni qaytarish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Nuqta {
public:
    int x, y;
    Nuqta(int a, int b) : x(a), y(b) {}
};

Nuqta nuqtaYarat(int a, int b) {
    return Nuqta(a, b);
}

int main() {
    Nuqta p = nuqtaYarat(3, 4);
    std::cout << "Nuqta: " << p.x << ", " << p.y << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zamonaviy kompilyatorlar RVO (Return Value Optimization) orqali hech qanday nusxalashsiz to'g'ridan-to'g'ri qaytaradi.

## Ishlash natijasi:
```text
Nuqta: 3, 4
```

---

# 381-Topshiriq: = default kalit so'zi

## Topshiriq sharti:
Kompilyatorning standart konstruktorini `= default` bilan tiklang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Sinov {
public:
    int x;
    Sinov() = default; // Standart konstruktorni kompilyatorga topshirish
    Sinov(int a) : x(a) {}
};

int main() {
    Sinov s1;
    Sinov s2(42);
    std::cout << "s2.x = " << s2.x << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boshqa konstruktor yozilganda standart konstruktor yo'qolib ketadi, `= default` uni qayta tiklaydi.

## Ishlash natijasi:
```text
s2.x = 42
```

---

# 382-Topshiriq: = delete kalit so'zi

## Topshiriq sharti:
Nusxalashni butunlay taqiqlash uchun `= delete` dan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class YagonaResurs {
public:
    YagonaResurs() = default;
    YagonaResurs(const YagonaResurs&) = delete; // Nusxalash taqiqlandi!
};

int main() {
    YagonaResurs r1;
    // YagonaResurs r2 = r1; // Kompilyatsiya xatosi!
    std::cout << "Nusxalash muvaffaqiyatli taqiqlangan." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `= delete` metod yoki konstruktorning chaqirilishini kompilyatsiya darajasida man etadi.

## Ishlash natijasi:
```text
Nusxalash muvaffaqiyatli taqiqlangan.
```

---

# 383-Topshiriq: Bo'sh sinf hajmi (Empty Class Size)

## Topshiriq sharti:
Nima uchun mutlaqo bo'sh sinfning hajmi 0 emas, balki 1 bayt ekanligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class BoshSinf {};

int main() {
    std::cout << "sizeof(BoshSinf): " << sizeof(BoshSinf) << " bayt" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir obyekt xotirada o'zining unikal manziliga ega bo'lishi kerakligi sababli bo'sh sinflar kamida 1 bayt egallaydi.

## Ishlash natijasi:
```text
sizeof(BoshSinf): 1 bayt
```

---

# 384-Topshiriq: enum class (Toifa xavfsiz sanovchi - C++11)

## Topshiriq sharti:
Nomlar to'qnashuvining oldini oluvchi `enum class` dan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>

enum class Holat {
    Kutish,
    Ishlamoqda,
    Tugadi
};

int main() {
    Holat h = Holat::Ishlamoqda;
    if (h == Holat::Ishlamoqda) {
        std::cout << "Jarayon faol holatda!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `enum class` o'zining alohida nomlar maydoniga ega bo'lib, oddiy `int` ga yashirincha o'girilmaydi.

## Ishlash natijasi:
```text
Jarayon faol holatda!
```

---

# 385-Topshiriq: Sinf ichida enum class va holat boshqaruvi

## Topshiriq sharti:
Sinf a'zosi sifatida `enum class` saqlang va holatga qarab xabar bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class ServerUlanish {
public:
    enum class Status { Ulanmagan, Ulangan };
private:
    Status joriy = Status::Ulanmagan;
public:
    void ulanish() { joriy = Status::Ulangan; }
    void tekshir() const {
        std::cout << (joriy == Status::Ulangan ? "Ulangan" : "Ulanmagan") << std::endl;
    }
};

int main() {
    ServerUlanish s;
    s.tekshir();
    s.ulanish();
    s.tekshir();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ichki enum class sinf kontekstida tushunarli va xavfsiz holat mashinasini (State machine) yaratadi.

## Ishlash natijasi:
```text
Ulanmagan\nUlangan
```

---

# 386-Topshiriq: Sinf ichidagi tur taxalluslari (using Type = ...)

## Topshiriq sharti:
Sinf ichida ma'lumotlar turini `using` orqali abstraktlashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class MassivBoshqaruv {
public:
    using QiymatTuri = long long;
    QiymatTuri yigindi(QiymatTuri a, QiymatTuri b) {
        return a + b;
    }
};

int main() {
    MassivBoshqaruv::QiymatTuri natija = 1000LL + 2000LL;
    std::cout << "Natija: " << natija << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. STL konteynerlari (masalan `std::vector::value_type`) aynan shu tamoyilda ishlaydi.

## Ishlash natijasi:
```text
Natija: 3000
```

---

# 387-Topshiriq: static constexpr a'zolar

## Topshiriq sharti:
Kompilyatsiya vaqtida ma'lum bo'lgan doimiy statik qiymatlarni `static constexpr` bilan belgilang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class MatematikaKonstanta {
public:
    static constexpr double PI = 3.1415926535;
};

int main() {
    std::cout << "Pi soni: " << MatematikaKonstanta::PI << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `static constexpr` xotirada joy olmaydi va to'g'ridan-to'g'ri kompilyatsiya vaqtida hisob-kitoblarga qo'shiladi.

## Ishlash natijasi:
```text
Pi soni: 3.14159
```

---

# 388-Topshiriq: Obyektlarning yashash davri (Storage Duration)

## Topshiriq sharti:
Avtomatik (stack), Statik (global) va Dinamik (heap) obyektlarning yashash muddatlarini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Sinov {
public:
    Sinov(const char* nom) { std::cout << nom << " yaratildi\n"; }
    ~Sinov() { std::cout << "o'chirildi\n"; }
};

Sinov globalObyekt("Global");

int main() {
    std::cout << "main boshlandi\n";
    {
        Sinov lokalObyekt("Lokal");
    }
    std::cout << "main tugadi\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Global obyektlar main dan oldin quriladi va main dan keyin yo'q qilinadi.

## Ishlash natijasi:
```text
Global yaratildi\nmain boshlandi\nLokal yaratildi\no'chirildi\nmain tugadi\no'chirildi
```

---

# 389-Topshiriq: Konstruktor va Destruktorlar chaqirilish tartibi (LIFO)

## Topshiriq sharti:
Bir nechta obyekt yaratilganda destruktorlar teskari (LIFO) tartibda chaqirilishini isbotlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Tartib {
    int id;
public:
    Tartib(int i) : id(i) { std::cout << "+" << id << " "; }
    ~Tartib() { std::cout << "-" << id << " "; }
};

int main() {
    {
        Tartib a(1);
        Tartib b(2);
        Tartib c(3);
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yaratilish: 1 -> 2 -> 3. O'chirilish esa aniq teskari tartibda: 3 -> 2 -> 1.

## Ishlash natijasi:
```text
+1 +2 +3 -3 -2 -1 
```

---

# 390-Topshiriq: Obyekt ichida dinamik massivni to'g'ri o'rash

## Topshiriq sharti:
O'zimizning sodda dinamik int massiv sinfimizni (konstruktor, destruktor, chuqur nusxalash bilan) yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class MeningVektorim {
    int* arr;
    int hajm;
public:
    MeningVektorim(int h) : hajm(h), arr(new int[h]{0}) {}
    ~MeningVektorim() { delete[] arr; }
    void set(int idx, int val) { if (idx >= 0 && idx < hajm) arr[idx] = val; }
    int get(int idx) const { return arr[idx]; }
};

int main() {
    MeningVektorim v(3);
    v.set(0, 10);
    v.set(1, 20);
    std::cout << "v[0] = " << v.get(0) << ", v[1] = " << v.get(1) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xotirani boshqaruvchi to'liq RAII sinfi.

## Ishlash natijasi:
```text
v[0] = 10, v[1] = 20
```

---

# 391-Topshiriq: Getter metodidan const& qaytarish

## Topshiriq sharti:
Katta satr yoki obyektni nusxalamasdan `const std::string&` orqali tezkor qaytaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

class Profil {
    std::string toliqIsm;
public:
    Profil(std::string ism) : toliqIsm(ism) {}
    const std::string& getIsm() const {
        return toliqIsm; // Nusxa ko'chirilmaydi
    }
};

int main() {
    Profil p("Alisher Navoiy");
    std::cout << "Profil: " << p.getIsm() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const &` qaytarish katta matnlarni nusxalash xarajatlaridan butunlay qutqaradi.

## Ishlash natijasi:
```text
Profil: Alisher Navoiy
```

---

# 392-Topshiriq: Funktor (Functor) yasash: operator() ni yuklash

## Topshiriq sharti:
Sinfga qavs `operator()` yuklab, obyektni xuddi funksiya kabi chaqirishni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Kopaytiruvchi {
    int koeffitsiyent;
public:
    Kopaytiruvchi(int k) : koeffitsiyent(k) {}
    int operator()(int x) const {
        return x * koeffitsiyent;
    }
};

int main() {
    Kopaytiruvchi uchtalik(3);
    std::cout << "uchtalik(5) = " << uchtalik(5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funktorlar o'z ichida holat (state) saqlay oluvchi qudratli funksiya obyektlaridir.

## Ishlash natijasi:
```text
uchtalik(5) = 15
```

---

# 393-Topshiriq: Holat saqlovchi Funktor (Stateful Functor)

## Topshiriq sharti:
Har chaqirilganda yig'indini to'plab boruvchi funktor tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Akkumulyator {
    int jami = 0;
public:
    int operator()(int qoshiluvchi) {
        jami += qoshiluvchi;
        return jami;
    }
};

int main() {
    Akkumulyator akk;
    std::cout << akk(10) << " ";
    std::cout << akk(20) << " ";
    std::cout << akk(5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funktor ichidagi `jami` o'zgaruvchisi doimiy saqlanib oshib boradi.

## Ishlash natijasi:
```text
10 30 35
```

---

# 394-Topshiriq: Hisoblangan xususiyatlar (Computed properties)

## Topshiriq sharti:
Maydon sifatida saqlanmasdan, talab qilinganda hisoblanuvchi xususiyatni yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Tortburchak {
public:
    double eni, boyi;
    Tortburchak(double e, double b) : eni(e), boyi(b) {}
    double perimetr() const { return 2 * (eni + boyi); }
    double yuzasi() const { return eni * boyi; }
};

int main() {
    Tortburchak t(4, 6);
    std::cout << "Yuzi: " << t.yuzasi() << ", Perimetr: " << t.perimetr() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Doimiy o'zgarishi mumkin bo'lgan natijalar xotirada saqlanmasdan real vaqtda hisoblanadi.

## Ishlash natijasi:
```text
Yuzi: 24, Perimetr: 20
```

---

# 395-Topshiriq: Bank Hisob Raqami (Bank Account) to'liq enkapsulyatsiyasi

## Topshiriq sharti:
Balans, depozit, pul yechish va tekshirish metodlariga ega xavfsiz BankAccount sinfi.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class BankAccount {
private:
    double balans;
public:
    BankAccount(double boshlangich = 0.0) : balans(boshlangich > 0 ? boshlangich : 0.0) {}
    void depozit(double miqdor) {
        if (miqdor > 0) balans += miqdor;
    }
    bool pulYechish(double miqdor) {
        if (miqdor > 0 && miqdor <= balans) {
            balans -= miqdor;
            return true;
        }
        return false;
    }
    double getBalans() const { return balans; }
};

int main() {
    BankAccount hisob(1000);
    hisob.depozit(500);
    hisob.pulYechish(300);
    std::cout << "Joriy balans: $" << hisob.getBalans() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Balansni faqat tekshirilgan tranzaksiyalar orqali o'zgartirish mumkin.

## Ishlash natijasi:
```text
Joriy balans: $1200
```

---

# 396-Topshiriq: Talabalar reytingi boshqaruvi sinfi

## Topshiriq sharti:
Talaba ismi va bir nechta baholari o'rtacha qiymatini hisoblovchi sinf yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <vector>

class TalabaReyting {
    std::string ism;
    std::vector<int> baholar;
public:
    TalabaReyting(std::string i) : ism(i) {}
    void bahoQosh(int b) { baholar.push_back(b); }
    double ortachaBaho() const {
        if (baholar.empty()) return 0.0;
        double sum = 0;
        for (int b : baholar) sum += b;
        return sum / baholar.size();
    }
    void natija() const {
        std::cout << ism << " o'rtacha bali: " << ortachaBaho() << std::endl;
    }
};

int main() {
    TalabaReyting t("Farrux");
    t.bahoQosh(85);
    t.bahoQosh(90);
    t.bahoQosh(95);
    t.natija();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dinamik ro'yxat va enkapsulyatsiya uyg'unligi.

## Ishlash natijasi:
```text
Farrux o'rtacha bali: 90
```

---

# 397-Topshiriq: Vaqt (Time) sinfi va validatsiya

## Topshiriq sharti:
Soat, daqiqa va soniyalarni saqlab, 1 soniya qo'shish (tick) metodiga ega sinf tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <iomanip>

class Vaqt {
    int soat, daqiqa, soniya;
public:
    Vaqt(int s, int d, int sn) : soat(s % 24), daqiqa(d % 60), soniya(sn % 60) {}
    void tick() {
        soniya++;
        if (soniya >= 60) { soniya = 0; daqiqa++; }
        if (daqiqa >= 60) { daqiqa = 0; soat = (soat + 1) % 24; }
    }
    void chopEt() const {
        std::cout << std::setfill('0') << std::setw(2) << soat << ":"
                  << std::setw(2) << daqiqa << ":" << std::setw(2) << soniya << std::endl;
    }
};

int main() {
    Vaqt v(23, 59, 59);
    v.tick();
    v.chopEt();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 23:59:59 ga 1 soniya qo'shilganda to'g'ri 00:00:00 ga o'tadi.

## Ishlash natijasi:
```text
00:00:00
```

---

# 398-Topshiriq: Kompleks sonlar (Complex Number) sinfi skeleti

## Topshiriq sharti:
Haqiqiy va mavhum qismdan iborat kompleks sonlar sinfini tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class Kompleks {
public:
    double re, im;
    Kompleks(double r = 0.0, double i = 0.0) : re(r), im(i) {}
    Kompleks qoshish(const Kompleks& b) const {
        return Kompleks(re + b.re, im + b.im);
    }
    void korsat() const {
        std::cout << re << " + " << im << "i" << std::endl;
    }
};

int main() {
    Kompleks k1(3, 4), k2(1, 2);
    Kompleks k3 = k1.qoshish(k2);
    k3.korsat();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matematik obyektlarni modellashtirishning asosiy namunasi.

## Ishlash natijasi:
```text
4 + 6i
```

---

# 399-Topshiriq: MeningStringim sodda o'rami

## Topshiriq sharti:
RAII asosida char ko'rsatkichini boshqaruvchi ixcham satr sinfini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstring>

class MeningStringim {
    char* data;
public:
    MeningStringim(const char* s = "") {
        data = new char[strlen(s) + 1];
        strcpy(data, s);
    }
    ~MeningStringim() { delete[] data; }
    const char* c_str() const { return data; }
};

int main() {
    MeningStringim ms("Antigravity OOP");
    std::cout << ms.c_str() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::string` sinfining eng sodda va pishiq arxitekturasi.

## Ishlash natijasi:
```text
Antigravity OOP
```

---

# 400-Topshiriq: 8-qism xulosasi: Obyektga Yo'naltirilgan Dasturlash Falsafasi

## Topshiriq sharti:
Enkapsulyatsiya ma'lumotlarni noqonuniy o'zgarishlardan asrash va arxitektura barqarorligini ta'minlashini xulosa qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "OOP - ma'lumotlar va ular ustidagi amallarni bitta xavfsiz qobiqqa "
              << "birlashtirib, murakkab tizimlarni tartibga soladi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Klasslar va obyektlar zamonaviy tizimlar qurilishining asosiy poydevoridir.

## Ishlash natijasi:
```text
OOP - ma'lumotlar va ular ustidagi amallarni bitta xavfsiz qobiqqa birlashtirib, murakkab tizimlarni tartibga soladi.
```

---

