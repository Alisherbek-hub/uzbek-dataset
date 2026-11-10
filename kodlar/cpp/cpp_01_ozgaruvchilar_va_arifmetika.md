# C++ Dasturlash Tili — 1-Qism: O'zgaruvchilar, Ma'lumot Turlari va Arifmetika
## (1-50 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam zamonaviy C++ (C++17/20) asoslarini, xotira turlari, arifmetik va bitli amallarni qamrab oladi:
* Standart turlar: `int`, `double`, `float`, `char`, `bool`, `auto`;
* Xavfsiz tur o'zgartirish: `static_cast`;
* Doimiylar va kompilyatsiya hisoblari: `const`, `constexpr`;
* Arifmetik, mantiqiy va bitli amallar (`&`, `|`, `^`, `<<`, `>>`);
* I/O oqimlari va formatlash: `std::cout`, `std::cin`, `std::setprecision`, `std::setw`;

---

# 1-Topshiriq: C++ da 'Salom Dunyo!' dasturi

## Topshiriq sharti:
Ekranga 'Salom Dunyo!' matnini std::cout orqali chiqaruvchi dastur yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Salom Dunyo!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `#include <iostream>` kiritish-chiqarish oqimlari kutubxonasini ulaydi.
2. `std::cout` konsolga matn chiqaradi, `std::endl` yangi qatorga o'tadi va oqimni tozalaydi (flush).

## Ishlash natijasi:
```text
Salom Dunyo!
```

---

# 2-Topshiriq: Butun sonli o'zgaruvchilar (int, long long)

## Topshiriq sharti:
Ikki butun son o'zgaruvchisi e'lon qilib, ularning yig'indisini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 15;
    int b = 27;
    int yigindi = a + b;
    std::cout << "Yig'indi: " << yigindi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int` turi 32-bitli butun sonlarni saqlaydi (-2,147,483,648 dan 2,147,483,647 gacha).

## Ishlash natijasi:
```text
Yig'indi: 42
```

---

# 3-Topshiriq: Haqiqiy sonlar (float va double)

## Topshiriq sharti:
Doira radiusidan uning yuzini hisoblang (S = pi * r^2).

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double radius = 5.0;
    const double PI = 3.1415926535;
    double yuza = PI * radius * radius;
    std::cout << "Doira yuzi: " << yuza << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `double` 64-bitli suzuvchi nuqtali son bo'lib, 15-17 xona aniqlik beradi.
2. `const` o'zgaruvchi qiymatini o'zgarmas qilib belgilaydi.

## Ishlash natijasi:
```text
Doira yuzi: 78.5398
```

---

# 4-Topshiriq: Belgilar (char va ASCII kodlar)

## Topshiriq sharti:
Belgi o'zgaruvchisi e'lon qilib, uning ASCII raqamli kodini chop eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    char belgi = 'A';
    int ascii_kod = static_cast<int>(belgi);
    std::cout << "Belgi: " << belgi << ", ASCII kodi: " << ascii_kod << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `char` 8-bit (1 bayt) xotira oladi va belgining ASCII jadvalidagi sonli indeksini saqlaydi.
2. `static_cast<int>` xavfsiz C++ tur almashtirish (casting) usulidir.

## Ishlash natijasi:
```text
Belgi: A, ASCII kodi: 65
```

---

# 5-Topshiriq: Mantiqiy tur (bool) va std::boolalpha

## Topshiriq sharti:
Mantiqiy ifodalar qiymatini true/false so'zlari ko'rinishida chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    bool rost = true;
    bool yolgon = (10 < 5);
    std::cout << std::boolalpha;
    std::cout << "Rost: " << rost << ", Yolgon: " << yolgon << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `bool` faqat `true` (1) yoki `false` (0) qiymat oladi.
2. `std::boolalpha` sonli 1/0 o'rniga so'z ko'rinishida chiqarishni ta'minlaydi.

## Ishlash natijasi:
```text
Rost: true, Yolgon: false
```

---

# 6-Topshiriq: Konsoldan kiritish (std::cin)

## Topshiriq sharti:
Foydalanuvchidan ikkita son kiritishni so'rab, ularning ko'paytmasini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int x = 6, y = 7;
    // std::cin >> x >> y; simulyatsiyasi
    int kopaytma = x * y;
    std::cout << "Ko'paytma: " << kopaytma << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::cin >> x` kiritish oqimidan qiymatni o'qib oladi.

## Ishlash natijasi:
```text
Ko'paytma: 42
```

---

# 7-Topshiriq: Butun sonli bo'lish va qoldiq olish (%)

## Topshiriq sharti:
Sonni bo'lganda butun qismini va qoldig'ini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int son = 17;
    int boluvchi = 5;
    std::cout << "Butun qism: " << son / boluvchi << std::endl;
    std::cout << "Qoldiq: " << son % boluvchi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Butun sonlar bo'linganda kasr qismi tashlab yuboriladi. `%` amali qoldiqni beradi.

## Ishlash natijasi:
```text
Butun qism: 3\nQoldiq: 2
```

---

# 8-Topshiriq: auto kalit so'zi (Type Inference)

## Topshiriq sharti:
Kompilyator turini avtomatik aniqlovchi auto bilan o'zgaruvchilar e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    auto butun = 100;       // int
    auto suzuvchi = 3.14;   // double
    auto matn = "O'zbek";   // const char*
    std::cout << butun << " " << suzuvchi << " " << matn << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `auto` C++11 dan boshlab boshlang'ich qiymat asosida o'zgaruvchi turini aniq belgilaydi.

## Ishlash natijasi:
```text
100 3.14 O'zbek
```

---

# 9-Topshiriq: sizeof operatori: Xotira hajmini baytlarda o'lchash

## Topshiriq sharti:
Asosiy ma'lumot turlari RAM dan qancha bayt joy olishini ko'ring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "char: " << sizeof(char) << " bayt\n";
    std::cout << "int: " << sizeof(int) << " bayt\n";
    std::cout << "double: " << sizeof(double) << " bayt\n";
    std::cout << "long long: " << sizeof(long long) << " bayt\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sizeof` kompilyatsiya vaqtida hisoblanadi va xotira arxitekturasini tushunishda muhimdir.

## Ishlash natijasi:
```text
char: 1 bayt\nint: 4 bayt\ndouble: 8 bayt\nlong long: 8 bayt
```

---

# 10-Topshiriq: static_cast bilan aniq konvertatsiya

## Topshiriq sharti:
Butun sonlar bo'linmasini haqiqiy son sifatida aniq hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int jami = 15;
    int soni = 4;
    double ortacha = static_cast<double>(jami) / soni;
    std::cout << "O'rtacha qiymat: " << ortacha << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `static_cast<double>(jami)` amali ifodani butun sonli bo'linishdan haqiqiy bo'linishga o'tkazadi.

## Ishlash natijasi:
```text
O'rtacha qiymat: 3.75
```

---

# 11-Topshiriq: Prefix va Postfix Increment (++i va i++)

## Topshiriq sharti:
Prefix va postfix amallarining farqini amalda ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 5;
    int b = ++a; // a oldin oshadi, keyin b ga o'tadi
    int c = a++; // c a ning eski qiymatini oladi, keyin a oshadi
    std::cout << "a: " << a << ", b: " << b << ", c: " << c << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `++i` yangi qiymatni qaytaradi, `i++` esa eski nusxani qaytarib keyin oshiradi.

## Ishlash natijasi:
```text
a: 7, b: 6, c: 6
```

---

# 12-Topshiriq: constexpr bilan kompilyatsiya vaqtidagi konstantalar

## Topshiriq sharti:
Kompilyatsiya vaqtida hisoblanadigan doimiylarni constexpr orqali aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

constexpr int kvadrat(int x) {
    return x * x;
}

int main() {
    constexpr int maydon = kvadrat(12);
    std::cout << "Kvadrat maydoni: " << maydon << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `constexpr` ifodalar runtime vaqtida CPU taktini sarflamaydi, balki to'g'ridan-to'g'ri binar faylga hisoblangan qiymat qo'yiladi.

## Ishlash natijasi:
```text
Kvadrat maydoni: 144
```

---

# 13-Topshiriq: std::string bilan satrli o'zgaruvchilar

## Topshiriq sharti:
Ikki satrni birlashtirish (konkatenatsiya) va uzunligini aniqlash.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string ism = "Alisher";
    std::string familiya = "Navoiy";
    std::string toliq = ism + " " + familiya;
    std::cout << "To'liq ism: " << toliq << " (Uzunligi: " << toliq.length() << ")" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::string` dinamik o'suvchi xavfsiz C++ satr turidir.

## Ishlash natijasi:
```text
To'liq ism: Alisher Navoiy (Uzunligi: 14)
```

---

# 14-Topshiriq: Murakkab biriktirish operatorlari (+=, -=, *=, /=)

## Topshiriq sharti:
O'zgaruvchi qiymatini qisqartirilgan amallar bilan yangilang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int ball = 50;
    ball += 20; // 70
    ball *= 2;  // 140
    ball -= 40; // 100
    std::cout << "Yakuniy ball: " << ball << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `x += y` ifodasi `x = x + y` ning qisqartmasidir.

## Ishlash natijasi:
```text
Yakuniy ball: 100
```

---

# 15-Topshiriq: Bitwise operatorlar: VA (&), YOKI (|) va XOR (^)

## Topshiriq sharti:
Sonlar bitlari ustida mantiqiy amallarni bajaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 5; // 0101b
    int b = 3; // 0011b
    std::cout << "AND: " << (a & b) << std::endl; // 0001b = 1
    std::cout << "OR:  " << (a | b) << std::endl; // 0111b = 7
    std::cout << "XOR: " << (a ^ b) << std::endl; // 0110b = 6
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitli amallar apparat darajasida eng tezkor hisoblanadi.

## Ishlash natijasi:
```text
AND: 1\nOR:  7\nXOR: 6
```

---

# 16-Topshiriq: Bitli siljitish (Bit Shifting: << va >>)

## Topshiriq sharti:
Sonni 2 ga ko'paytirish va bo'lishni bitli siljitish bilan bajaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int x = 8;
    std::cout << "Chapga 1 (x * 2): " << (x << 1) << std::endl;
    std::cout << "O'ngga 2 (x / 4): " << (x >> 2) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `x << k` sonni 2^k ga ko'paytiradi, `x >> k` esa 2^k ga bo'ladi.

## Ishlash natijasi:
```text
Chapga 1 (x * 2): 16\nO'ngga 2 (x / 4): 2
```

---

# 17-Topshiriq: Unsigned turlar (Manfiysiz butun sonlar)

## Topshiriq sharti:
Faqat musbat sonlarni saqlovchi unsigned int dan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    unsigned int x = 3000000000U;
    std::cout << "Katta musbat son: " << x << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `unsigned` turlarda manfiy ishora bo'lmagani uchun musbat sonlar chegarasi 2 barobar katta bo'ladi (0 dan 4,294,967,295 gacha).

## Ishlash natijasi:
```text
Katta musbat son: 3000000000
```

---

# 18-Topshiriq: Sonlarning chegaralari (std::numeric_limits)

## Topshiriq sharti:
int va double turlarining minimal va maksimal qiymatlarini chop eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <limits>

int main() {
    std::cout << "int min: " << std::numeric_limits<int>::min() << std::endl;
    std::cout << "int max: " << std::numeric_limits<int>::max() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::numeric_limits` turlarning apparat chegaralarini aniqlashda standartdir.

## Ishlash natijasi:
```text
int min: -2147483648\nint max: 2147483647
```

---

# 19-Topshiriq: O'zgaruvchilarni qiymatini almashtirish (std::swap)

## Topshiriq sharti:
Qo'shimcha o'zgaruvchisiz ikki sonning o'rnini almashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <utility>

int main() {
    int x = 10, y = 20;
    std::swap(x, y);
    std::cout << "x: " << x << ", y: " << y << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::swap` xotirada eng samarali tarzda o'rin almashtirishni ta'minlaydi.

## Ishlash natijasi:
```text
x: 20, y: 10
```

---

# 20-Topshiriq: Arifmetik ifodalarning ustuvorlik tartibi (Operator Precedence)

## Topshiriq sharti:
Qavslar va amallar ketma-ketligini to'g'ri hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int natija = 10 + 5 * 2 - (8 / 4);
    std::cout << "Natija: " << natija << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'paytirish va bo'lish qo'shish va ayirishdan oldin bajariladi, qavslar eng yuqori ustuvorlikka ega.

## Ishlash natijasi:
```text
Natija: 18
```

---

# 21-Topshiriq: Havola (Reference) o'zgaruvchilari

## Topshiriq sharti:
O'zgaruvchiga havola yaratib, u orqali qiymatni o'zgartiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int asosiy = 50;
    int& havola = asosiy;
    havola += 25;
    std::cout << "Asosiy qiymat: " << asosiy << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Havola (`&`) yangi xotira ajratmaydi, u mavjud o'zgaruvchining boshqa nomidir.

## Ishlash natijasi:
```text
Asosiy qiymat: 75
```

---

# 22-Topshiriq: Konstanta havolalar (const Reference)

## Topshiriq sharti:
O'zgartirib bo'lmaydigan faqat o'qish uchun havola e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int ball = 100;
    const int& xavfsiz = ball;
    // xavfsiz = 90; // Kompilyatsiya xatosi!
    std::cout << "Xavfsiz o'qish: " << xavfsiz << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const &` katta hajmdagi ma'lumotlarni nusxalamasdan va o'zgartirishdan himoyalagan holda uzatishda ishlatiladi.

## Ishlash natijasi:
```text
Xavfsiz o'qish: 100
```

---

# 23-Topshiriq: Tenglik va taqqoslash operatorlari (==, !=, <, >)

## Topshiriq sharti:
Ikki sonni taqqoslab mantiqiy natijani oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 10, b = 20;
    std::cout << std::boolalpha;
    std::cout << "Tengmi: " << (a == b) << "\n";
    std::cout << "Kichikmi: " << (a < b) << "\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Taqqoslash amallari mantiqiy `bool` qiymat qaytaradi.

## Ishlash natijasi:
```text
Tengmi: false\nKichikmi: true
```

---

# 24-Topshiriq: std::getline bilan bo'shliqli satr kiritish

## Topshiriq sharti:
Foydalanuvchining to'liq ismi-sharifini probellari bilan birga o'qing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <sstream>

int main() {
    std::istringstream stream("Alisherbek Qodirov");
    std::string toliq_ism;
    std::getline(stream, toliq_ism);
    std::cout << "Kiritildi: " << toliq_ism << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::cin >> satr` birinchi bo'shliqda to'xtaydi, `std::getline` esa butun qatorni oladi.

## Ishlash natijasi:
```text
Kiritildi: Alisherbek Qodirov
```

---

# 25-Topshiriq: Matematik kutubxona (<cmath>): Ildiz va daraja

## Topshiriq sharti:
Kvadrat ildiz (std::sqrt) va darajaga ko'tarish (std::pow) amallarini bajaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cmath>

int main() {
    double x = 16.0;
    std::cout << "Ildiz: " << std::sqrt(x) << std::endl;
    std::cout << "2^8: " << std::pow(2.0, 8.0) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `<cmath>` da suzuvchi nuqtali matematik hisob-kitoblar funksiyalari joylashgan.

## Ishlash natijasi:
```text
Ildiz: 4\n2^8: 256
```

---

# 26-Topshiriq: Yaxlitlash amallari: floor, ceil, round

## Topshiriq sharti:
Haqiqiy sonni pastga, yuqoriga va eng yaqin butun songa yaxlitlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cmath>

int main() {
    double son = 4.6;
    std::cout << "floor(4.6): " << std::floor(son) << "\n";
    std::cout << "ceil(4.6):  " << std::ceil(son) << "\n";
    std::cout << "round(4.6): " << std::round(son) << "\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `floor` pastga, `ceil` yuqoriga, `round` esa 0.5 chegarasi bo'yicha yaxlitlaydi.

## Ishlash natijasi:
```text
floor(4.6): 4\nceil(4.6):  5\nround(4.6): 5
```

---

# 27-Topshiriq: Turi aniqlangan butun sonlar (<cstdint>)

## Topshiriq sharti:
Har qanday platformada aniq 32 yoki 64 bit kafolatlangan turlardan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>

int main() {
    int32_t a = 100000;
    int64_t b = 5000000000LL;
    uint8_t bayt = 255;
    std::cout << "32-bit: " << a << ", 64-bit: " << b << ", 8-bit: " << static_cast<int>(bayt) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tizimli va tarmoq dasturlarida o'lchami o'zgarmas bo'lgan `<cstdint>` turlari ishlatiladi.

## Ishlash natijasi:
```text
32-bit: 100000, 64-bit: 5000000000, 8-bit: 255
```

---

# 28-Topshiriq: Satrni songa o'girish (std::stoi, std::stod)

## Topshiriq sharti:
Satrli ma'lumotlarni butun va haqiqiy songa aylantiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string s1 = "1234";
    std::string s2 = "45.67";
    int son = std::stoi(s1);
    double narx = std::stod(s2);
    std::cout << "Son + 1: " << son + 1 << ", Narx + 0.5: " << narx + 0.5 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::stoi` (String to Integer) va `std::stod` (String to Double) xavfsiz parsing amallaridir.

## Ishlash natijasi:
```text
Son + 1: 1235, Narx + 0.5: 46.17
```

---

# 29-Topshiriq: Sonni satrga o'girish (std::to_string)

## Topshiriq sharti:
Raqamli qiymatni string ob'ektiga aylantirib matnga qo'shing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    int id = 42;
    std::string xabar = "Buyurtma #" + std::to_string(id);
    std::cout << xabar << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::to_string` har qanday asosiy sonli turni satrga o'giradi.

## Ishlash natijasi:
```text
Buyurtma #42
```

---

# 30-Topshiriq: Murakkab sanoq tizimlari: O'nlik, Sakkizlik va O'n oltilik (Hex)

## Topshiriq sharti:
Sonlarni turli sanoq tizimlarida konsolga chiqarish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int son = 255;
    std::cout << "O'nlik: " << std::dec << son << "\n";
    std::cout << "O'n oltilik (Hex): " << std::hex << son << "\n";
    std::cout << "Sakkizlik (Oct): " << std::oct << son << "\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::hex` va `std::oct` oqim manipulyatorlari sanoq tizimini o'zgartiradi.

## Ishlash natijasi:
```text
O'nlik: 255\nO'n oltilik (Hex): ff\nSakkizlik (Oct): 377
```

---

# 31-Topshiriq: Ikki lik sanoq sistemasida son kiritish (0b prefiksi)

## Topshiriq sharti:
C++14 standarti bo'yicha ikkilik binar sonlarni to'g'ridan-to'g'ri e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int binar_son = 0b101010; // O'nlikda 42
    std::cout << "0b101010 o'nlikda: " << binar_son << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `0b` prefiksi ikkilik sonlar bilan qulay ishlashga imkon beradi.

## Ishlash natijasi:
```text
0b101010 o'nlikda: 42
```

---

# 32-Topshiriq: Raqam ajratuvchi (Digit Separator: apostrof ')

## Topshiriq sharti:
Katta sonlarni o'qilishini osonlashtirish uchun C++14 apostrofidan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    long long bir_milliard = 1'000'000'000LL;
    std::cout << "Bir milliard: " << bir_milliard << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyator son ichidagi apostrof belgilarini e'tiborsiz qoldiradi.

## Ishlash natijasi:
```text
Bir milliard: 1000000000
```

---

# 33-Topshiriq: Modul va Manfiy sonlar arifmetikasi

## Topshiriq sharti:
Manfiy sonlarning qoldig'i C++11 standartida qanday hisoblanishini ko'ring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "-7 % 3 = " << (-7 % 3) << std::endl;
    std::cout << "7 % -3 = " << (7 % -3) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++ da qoldiq ishorasi chap tomondagi bo'linuvchining ishorasi bilan bir xil bo'ladi.

## Ishlash natijasi:
```text
-7 % 3 = -1\n7 % -3 = 1
```

---

# 34-Topshiriq: Ternary shartli operatori (?:)

## Topshiriq sharti:
Qisqa shart orqali ikki sonning kattasini bitta qatorda tanlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 25, b = 40;
    int max_son = (a > b) ? a : b;
    std::cout << "Kattasi: " << max_son << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `shart ? rost : yolgon` ternary ifodasi qiymat qaytaradi.

## Ishlash natijasi:
```text
Kattasi: 40
```

---

# 35-Topshiriq: Enum (Sanash turi) asoslari

## Topshiriq sharti:
Hafta kunlarini ifodalovchi sodda enum yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

enum HaftaKunlari {
    Dushanba = 1,
    Seshanba,
    Chorshanba,
    Payshanba,
    Juma,
    Shanba,
    Yakshanba
};

int main() {
    HaftaKunlari bugun = Juma;
    std::cout << "Juma kunining raqami: " << bugun << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `enum` sonli konstantalarga o'qilishi oson nomlar biriktiradi.

## Ishlash natijasi:
```text
Juma kunining raqami: 5
```

---

# 36-Topshiriq: Scoped Enum (enum class) — Xavfsiz sanash turi

## Topshiriq sharti:
C++11 ning nomlar to'qnashuvidan himoyalangan enum class dan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>

enum class Rang { Qizil, Yashil, Kok };

int main() {
    Rang r = Rang::Yashil;
    if (r == Rang::Yashil) {
        std::cout << "Yashil rang tanlandi!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `enum class` avtomatik butun songa aylanmaydi va to'liq tur xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
Yashil rang tanlandi!
```

---

# 37-Topshiriq: Typedef va using bilan yangi tur taxalluslari

## Topshiriq sharti:
`using` kalit so'zi bilan murakkab turlarga sodda nom bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>

using ButunSon = long long;

int main() {
    ButunSon hisob = 9876543210LL;
    std::cout << "Hisob: " << hisob << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `using YangiNom = AslTur;` zamonaviy C++ da `typedef` ning o'rnini to'liq egallagan.

## Ishlash natijasi:
```text
Hisob: 9876543210
```

---

# 38-Topshiriq: decltype bilan ifoda turini aniqlash

## Topshiriq sharti:
Ifoda qanday turga ega bo'lsa, xuddi shu turdagi yangi o'zgaruvchi e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 10;
    double b = 5.5;
    decltype(a * b) natija = a * b; // double bo'ladi
    std::cout << "Natija: " << natija << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `decltype(expr)` ifodaning turini kompilyatsiya vaqtida hisoblaydi.

## Ishlash natijasi:
```text
Natija: 55
```

---

# 39-Topshiriq: Struktura (struct) asoslari

## Topshiriq sharti:
Talabaning ismi, kursi va o'rtacha ballini saqlovchi sodda struktura yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

struct Talaba {
    std::string ism;
    int kurs;
    double gpa;
};

int main() {
    Talaba t1 = {"Botir", 3, 4.8};
    std::cout << t1.ism << ", " << t1.kurs << "-kurs, GPA: " << t1.gpa << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++ da `struct` ning barcha a'zolari standart holatda `public` bo'ladi.

## Ishlash natijasi:
```text
Botir, 3-kurs, GPA: 4.8
```

---

# 40-Topshiriq: Strukturalarni initsializatsiya qilish (Designated Initializers C++20)

## Topshiriq sharti:
C++20 uslubida maydon nomlarini ko'rsatib strukturani to'ldiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Nuqta {
    int x;
    int y;
};

int main() {
    Nuqta p = {.x = 10, .y = 20};
    std::cout << "P(" << p.x << ", " << p.y << ")" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++20 designated initializers kodning tushunarliligini sezilarli darajada oshiradi.

## Ishlash natijasi:
```text
P(10, 20)
```

---

# 41-Topshiriq: Chiqarish formatlash: std::fixed va std::setprecision

## Topshiriq sharti:
Haqiqiy sonni aniq verguldan keyin 2 xona bilan formatlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <iomanip>

int main() {
    double summa = 1234.56789;
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Formatlangan: " << summa << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `<iomanip>` kutubxonasidagi `std::setprecision` moliya va ilmiy hisoblashlarda zarurdir.

## Ishlash natijasi:
```text
Formatlangan: 1234.57
```

---

# 42-Topshiriq: Chiqarish kengligi va to'ldirish (std::setw, std::setfill)

## Topshiriq sharti:
Sonlarni ustun shaklida chiroyli qilib tekislang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <iomanip>

int main() {
    std::cout << std::setfill('0') << std::setw(5) << 42 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::setw(5)` maydon kengligini, `std::setfill('0')` esa bo'sh joylarni to'ldiruvchi belgini belgilaydi.

## Ishlash natijasi:
```text
00042
```

---

# 43-Topshiriq: Escape belgilar (\n, \t, \\, \")

## Topshiriq sharti:
Matn ichida tabulyatsiya, tirnoq va teskari slesh belgilarini to'g'ri chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Ism:\t\"Alisher\"\nYo'l:\tC:\\fayllar\\kod.cpp" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Maxsus belgilar teskari slesh (`\`) bilan ekranlashtiriladi.

## Ishlash natijasi:
```text
Ism:\t"Alisher"\nYo'l:\tC:\fayllar\kod.cpp
```

---

# 44-Topshiriq: Xom satrli literallar (Raw String Literals: R"(...)")

## Topshiriq sharti:
Ekranlashtirishlarsiz ko'p qatorli yoki regex satrlarini e'lon qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string yo_l = R"(C:\Program Files\UzbekAI\data.txt)";
    std::cout << yo_l << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++11 raw string literali `R"(...)\` regex va yo'llar bilan ishlashni juda osonlashtiradi.

## Ishlash natijasi:
```text
C:\\Program Files\\UzbekAI\\data.txt
```

---

# 45-Topshiriq: Matematik doimiylar (<numbers> C++20)

## Topshiriq sharti:
C++20 ning rasmiy matematik doimiylaridan (pi, e, sqrt2) foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <numbers>

int main() {
    std::cout << "Pi: " << std::numbers::pi << std::endl;
    std::cout << "e:  " << std::numbers::e << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++20 da `<numbers>` sarlavhasi ostida eng yuqori aniqlikdagi doimiylar kiritilgan.

## Ishlash natijasi:
```text
Pi: 3.14159\ne:  2.71828
```

---

# 46-Topshiriq: Qo'shimcha arifmetika: std::abs va std::fmod

## Topshiriq sharti:
Sonning moduli va haqiqiy sonlar qoldig'ini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cmath>

int main() {
    std::cout << "abs(-15): " << std::abs(-15) << std::endl;
    std::cout << "fmod(5.3, 2.0): " << std::fmod(5.3, 2.0) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::fmod` suzuvchi nuqtali sonlarning qoldig'ini topish uchun xizmat qiladi.

## Ishlash natijasi:
```text
abs(-15): 15\nfmod(5.3, 2.0): 1.3
```

---

# 47-Topshiriq: Random sonlar generatsiyasi (C++11 <random>)

## Topshiriq sharti:
Mersenne Twister (std::mt19937) yordamida sifatli tasodifiy son oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <random>

int main() {
    std::mt19937 generator(42); // Seed
    std::uniform_int_distribution<int> diapazon(1, 100);
    int tasodifiy = diapazon(generator);
    std::cout << "Tasodifiy son: " << tasodifiy << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Eski `rand()` o'rniga zamonaviy C++11 `<random>` to'g'ri taqsimot va yuqori entropiya beradi.

## Ishlash natijasi:
```text
Tasodifiy son: 38
```

---

# 48-Topshiriq: Butun son toshishi (Integer Overflow) oqibatlari

## Topshiriq sharti:
Maksimal son chegarasidan oshganda nima sodir bo'lishini ko'ring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <limits>

int main() {
    unsigned int u_max = std::numeric_limits<unsigned int>::max();
    std::cout << "Max unsigned: " << u_max << std::endl;
    u_max += 1; // 0 ga aylanadi
    std::cout << "Toshgandan so'ng: " << u_max << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Unsigned sonlar toshganda modulo 2^32 bo'yicha aylanadi.

## Ishlash natijasi:
```text
Max unsigned: 4294967295\nToshgandan so'ng: 0
```

---

# 49-Topshiriq: Kompilyator optimizatsiyasiga taqiq (volatile kalit so'zi)

## Topshiriq sharti:
Apparat registri yoki tashqi o'zgaruvchilar uchun volatile ishlatish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    volatile int bayroq = 1;
    std::cout << "Volatile o'zgaruvchi: " << bayroq << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `volatile` kompilyatorga ushbu o'zgaruvchini keshlamasdan har doim xotiradan to'g'ridan-to'g'ri o'qishni buyuradi.

## Ishlash natijasi:
```text
Volatile o'zgaruvchi: 1
```

---

# 50-Topshiriq: Amaliy Sintez: Valyuta konvertori va kassa cheki dasturi

## Topshiriq sharti:
O'rganilgan barcha turlar, arifmetika va formatlashni birlashtirgan to'liq dastur.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <iomanip>

int main() {
    std::string mahsulot = "Noutbuk";
    double dollar_narx = 850.50;
    const double KURS = 12800.0; // 1 USD = 12800 UZS
    
    double som_narx = dollar_narx * KURS;
    double soliq = som_narx * 0.12; // 12% QQS
    double jami = som_narx + soliq;
    
    std::cout << "====================================\n";
    std::cout << "          XARID CHEKI               \n";
    std::cout << "====================================\n";
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Mahsulot: " << mahsulot << "\n";
    std::cout << "Narxi ($):  $" << dollar_narx << "\n";
    std::cout << "Narxi (so'm): " << som_narx << " so'm\n";
    std::cout << "QQS (12%):    " << soliq << " so'm\n";
    std::cout << "------------------------------------\n";
    std::cout << "JAMI TO'LOV:  " << jami << " so'm\n";
    std::cout << "====================================\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Valyuta hisobi, QQS va konsol formatlash amallarining amaliy integratsiyasi.

## Ishlash natijasi:
```text
====================================\n          XARID CHEKI               \n====================================\nMahsulot: Noutbuk\nNarxi ($):  $850.50\nNarxi (so'm): 10886400.00 so'm\nQQS (12%):    1306368.00 so'm\n------------------------------------\nJAMI TO'LOV:  12192768.00 so'm\n====================================
```

---

