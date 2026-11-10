# C++ Dasturlash Tili — 2-Qism: Shartlar, Mantiqiy Operatorlar va switch-case
## (51-100 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam dastur oqimini shartlar bo'yicha boshqarishni to'liq qamrab oladi:
* `if`, `else if`, `else` tarmoqlanish konstruksiyalari;
* Mantiqiy operatorlar: `&&` (VA), `||` (YOKI), `!` (INKOR), qisqa tutashuv;
* `switch-case`, `break`, `[[fallthrough]]`, scoped enum bilan ishlash;
* Zamonaviy C++17 `if (init; condition)` va `switch (init; condition)`;
* Geometriya, bank tizimlari, shaxmat va xavfsizlik shartlari mantiqi;

---

# 51-Topshiriq: if sharti asoslari: Musbat, manfiy yoki nol

## Topshiriq sharti:
Kiritilgan son musbat, manfiy yoki nol ekanligini if shartlari orqali aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int son = -7;
    if (son > 0) {
        std::cout << "Musbat son" << std::endl;
    } else if (son < 0) {
        std::cout << "Manfiy son" << std::endl;
    } else {
        std::cout << "Nol" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `if` sharti rost (`true`) bo'lganda tegishli blokdagi kod bajariladi, aks holda `else if` yoki `else` ga o'tadi.

## Ishlash natijasi:
```text
Manfiy son
```

---

# 52-Topshiriq: if-else: Juft yoki toq sonni aniqlash

## Topshiriq sharti:
Son 2 ga qoldiqsiz bo'linishini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int son = 14;
    if (son % 2 == 0) {
        std::cout << son << " — Juft son" << std::endl;
    } else {
        std::cout << son << " — Toq son" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `% 2 == 0` qoldiqsiz bo'linishni tekshiradi.

## Ishlash natijasi:
```text
14 — Juft son
```

---

# 53-Topshiriq: Baholash shkalasi (if-else if zanjiri)

## Topshiriq sharti:
Talabaning 100 ballik tizimdagi natijasiga qarab an'anaviy bahosini (2, 3, 4, 5) chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int ball = 85;
    if (ball >= 86) {
        std::cout << "Baho: 5 (A'lo)" << std::endl;
    } else if (ball >= 71) {
        std::cout << "Baho: 4 (Yaxshi)" << std::endl;
    } else if (ball >= 56) {
        std::cout << "Baho: 3 (Qoniqarli)" << std::endl;
    } else {
        std::cout << "Baho: 2 (Qoniqarsiz)" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yuqoridan pastga tekshirish orqali oraliqlar avtomatik to'g'ri taqsimlanadi.

## Ishlash natijasi:
```text
Baho: 4 (Yaxshi)
```

---

# 54-Topshiriq: Mantiqiy VA (&&) operatori: Oraliqni tekshirish

## Topshiriq sharti:
Son 10 va 50 oralig'ida (ikkala chegara ham kiradi) joylashganligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int x = 25;
    if (x >= 10 && x <= 50) {
        std::cout << x << " oraliqda joylashgan." << std::endl;
    } else {
        std::cout << x << " oraliqdan tashqarida." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `&&` (Mantiqiy VA) har ikkala shart ham rost bo'lgandagina rost qiymat qaytaradi.

## Ishlash natijasi:
```text
25 oraliqda joylashgan.
```

---

# 55-Topshiriq: Mantiqiy YOKI (||) operatori: Dam olish kunlari

## Topshiriq sharti:
Hafta kuni raqami bo'yicha ish yoki dam olish kuni ekanligini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int kun = 6; // 6 - Shanba, 7 - Yakshanba
    if (kun == 6 || kun == 7) {
        std::cout << "Dam olish kuni!" << std::endl;
    } else {
        std::cout << "Ish kuni." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `||` (Mantiqiy YOKI) shartlardan kamida bittasi rost bo'lsa kifoya.

## Ishlash natijasi:
```text
Dam olish kuni!
```

---

# 56-Topshiriq: Mantiqiy INKOR (!) operatori

## Topshiriq sharti:
Foydalanuvchi tizimga kirmaganligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    bool tizimga_kirgan = false;
    if (!tizimga_kirgan) {
        std::cout << "Iltimos, avval tizimga kiring!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `!` operatori rostni yolg'onga, yolg'onni rostga aylantiradi.

## Ishlash natijasi:
```text
Iltimos, avval tizimga kiring!
```

---

# 57-Topshiriq: Qisqa tutashuvli baholash (Short-Circuit Evaluation)

## Topshiriq sharti:
Nolga bo'lish xatoligining oldini qisqa tutashuv bilan oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int boluvchi = 0;
    int son = 100;
    if (boluvchi != 0 && (son / boluvchi > 5)) {
        std::cout << "Shart bajarildi." << std::endl;
    } else {
        std::cout << "Xavfsiz chetlab o'tildi (nolga bo'linmadi)." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar `&&` ning chap tomoni yolg'on bo'lsa, o'ng tomoni umuman hisoblanmaydi.

## Ishlash natijasi:
```text
Xavfsiz chetlab o'tildi (nolga bo'linmadi).
```

---

# 58-Topshiriq: Ichma-ich if (Nested if) konstruksiyasi

## Topshiriq sharti:
Haydovchilik guvohnomasini olish talablarini tekshiring (yosh va tibbiy ko'rik).

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int yosh = 19;
    bool tibbiy_korigi_otgan = true;
    
    if (yosh >= 18) {
        if (tibbiy_korigi_otgan) {
            std::cout << "Guvohnoma olish mumkin." << std::endl;
        } else {
            std::cout << "Tibbiy ko'rikdan o'tish zarur!" << std::endl;
        }
    } else {
        std::cout << "Yosh yetarli emas (kamida 18 yosh)." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ichma-ich if ketma-ket shartlarni tekshirish imkonini beradi.

## Ishlash natijasi:
```text
Guvohnoma olish mumkin.
```

---

# 59-Topshiriq: Ternary operator zanjiri: Uchta sonning kattasi

## Topshiriq sharti:
Uchta sondan eng kattasini ternary operator bilan toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 12, b = 45, c = 30;
    int eng_katta = (a > b) ? ((a > c) ? a : c) : ((b > c) ? b : c);
    std::cout << "Eng katta son: " << eng_katta << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ternary operatorlar bir-birining ichiga joylanishi mumkin.

## Ishlash natijasi:
```text
Eng katta son: 45
```

---

# 60-Topshiriq: switch-case asoslari: Hafta kuni nomi

## Topshiriq sharti:
Son bo'yicha hafta kunining nomini switch orqali ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int kun = 3;
    switch (kun) {
        case 1: std::cout << "Dushanba"; break;
        case 2: std::cout << "Seshanba"; break;
        case 3: std::cout << "Chorshanba"; break;
        case 4: std::cout << "Payshanba"; break;
        case 5: std::cout << "Juma"; break;
        case 6: std::cout << "Shanba"; break;
        case 7: std::cout << "Yakshanba"; break;
        default: std::cout << "Noto'g'ri kun raqami!"; break;
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `switch` ifodasi mos `case` belgisiga sakraydi. `break` blokdan chiqish uchun shart.

## Ishlash natijasi:
```text
Chorshanba
```

---

# 61-Topshiriq: switch-case: Fallthrough xatti-harakati

## Topshiriq sharti:
Bir nechta case larni birlashtirib umumiy guruhlash.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int baho = 4;
    switch (baho) {
        case 5:
        case 4:
            std::cout << "Grant saqlab qolindi!" << std::endl;
            break;
        case 3:
        case 2:
            std::cout << "Stipendiya to'xtatildi." << std::endl;
            break;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `break` qo'yilmasa, ijro keyingi case ga tushib ketaveradi (fallthrough).

## Ishlash natijasi:
```text
Grant saqlab qolindi!
```

---

# 62-Topshiriq: [[fallthrough]] atributi (C++17)

## Topshiriq sharti:
Ataylab keyingi case ga tushishni kompilyator ogohlantirishisiz tasdiqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int bosqich = 1;
    switch (bosqich) {
        case 1:
            std::cout << "1-qadam bajarildi\n";
            [[fallthrough]];
        case 2:
            std::cout << "2-qadam bajarildi\n";
            break;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++17 `[[fallthrough]]` koddagi niyatni aniq ko'rsatib xatoliklarni oldini oladi.

## Ishlash natijasi:
```text
1-qadam bajarildi\n2-qadam bajarildi
```

---

# 63-Topshiriq: Oddiy kalkulyator (switch char bo'yicha)

## Topshiriq sharti:
Amal belgisiga qarab (+, -, *, /) hisoblashni bajaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double a = 20, b = 4;
    char amal = '/';
    switch (amal) {
        case '+': std::cout << a + b; break;
        case '-': std::cout << a - b; break;
        case '*': std::cout << a * b; break;
        case '/': std::cout << a / b; break;
        default: std::cout << "Xato amal"; break;
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `switch` char belgilari bilan ham ishlaydi.

## Ishlash natijasi:
```text
5
```

---

# 64-Topshiriq: Scoped enum bilan switch-case

## Topshiriq sharti:
enum class holatlarini xavfsiz qayta ishlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

enum class Holat { Boshlandi, Jarayonda, Yakunlandi };

int main() {
    Holat h = Holat::Jarayonda;
    switch (h) {
        case Holat::Boshlandi: std::cout << "Yangi"; break;
        case Holat::Jarayonda: std::cout << "Yuklanmoqda..."; break;
        case Holat::Yakunlandi: std::cout << "Tayyor"; break;
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `enum class` switch da barcha variantlar ko'rib chiqilganini tekshirishni osonlashtiradi.

## Ishlash natijasi:
```text
Yuklanmoqda...
```

---

# 65-Topshiriq: If with initializer (C++17)

## Topshiriq sharti:
Shart qatorining o'zida o'zgaruvchi e'lon qilib tekshirish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int hisobla() { return 42; }

int main() {
    if (int res = hisobla(); res > 0) {
        std::cout << "Natija musbat: " << res << std::endl;
    }
    // res bu yerda mavjud emas (scope toza qoladi)
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++17 `if (init; condition)` o'zgaruvchining qamrov sohasini faqat kerakli blokda cheklaydi.

## Ishlash natijasi:
```text
Natija musbat: 42
```

---

# 66-Topshiriq: Switch with initializer (C++17)

## Topshiriq sharti:
Switch shartining o'zida o'zgaruvchi yaratib ishlatish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int get_status() { return 200; }

int main() {
    switch (int kod = get_status(); kod) {
        case 200: std::cout << "OK"; break;
        case 404: std::cout << "Not Found"; break;
        default:  std::cout << "Boshqa"; break;
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qamrov doirasini ifloslantirmasdan switch boshqarish imkoniyati.

## Ishlash natijasi:
```text
OK
```

---

# 67-Topshiriq: Kabisa yilini aniqlash (Leap Year)

## Topshiriq sharti:
Yil kabisa ekanligini tekshiring (4 ga bo'linadi, 100 ga bo'linmaydi yoki 400 ga bo'linadi).

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int yil = 2024;
    bool kabisami = (yil % 4 == 0 && yil % 100 != 0) || (yil % 400 == 0);
    std::cout << yil << (kabisami ? " — Kabisa yili" : " — Oddiy yil") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kabisa yili murakkab mantiqiy ifoda bilan aniqlanadi.

## Ishlash natijasi:
```text
2024 — Kabisa yili
```

---

# 68-Topshiriq: Uchburchak mavjudlik sharti va turi

## Topshiriq sharti:
Uchta tomon bo'yicha uchburchak yasalishini va uning turini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 5, b = 5, c = 5;
    if (a + b > c && a + c > b && b + c > a) {
        if (a == b && b == c) {
            std::cout << "Teng tomonli uchburchak" << std::endl;
        } else if (a == b || a == c || b == c) {
            std::cout << "Teng yonli uchburchak" << std::endl;
        } else {
            std::cout << "Turli tomonli uchburchak" << std::endl;
        }
    } else {
        std::cout << "Bunday uchburchak mavjud emas!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har qanday ikki tomon yig'indisi uchinchi tomondan katta bo'lishi shart.

## Ishlash natijasi:
```text
Teng tomonli uchburchak
```

---

# 69-Topshiriq: Kvadrat tenglama ildizlari soni (Diskriminant)

## Topshiriq sharti:
ax^2 + bx + c = 0 kvadrat tenglama diskriminanti orqali ildizlar sonini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double a = 1, b = -5, c = 6;
    double D = b * b - 4 * a * c;
    if (D > 0) {
        std::cout << "Ikkita haqiqiy ildiz mavjud (D > 0)" << std::endl;
    } else if (D == 0) {
        std::cout << "Bitta ildiz mavjud (D = 0)" << std::endl;
    } else {
        std::cout << "Haqiqiy ildizlar yo'q (D < 0)" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Diskriminant ishorasi ildizlar xarakterini belgilaydi.

## Ishlash natijasi:
```text
Ikkita haqiqiy ildiz mavjud (D > 0)
```

---

# 70-Topshiriq: Raqamlar oralig'ini tekshirish (3 xonali sonmi?)

## Topshiriq sharti:
Musbat son aynan 3 xonali ekanligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int son = 458;
    if (son >= 100 && son <= 999) {
        std::cout << son << " — Uch xonali son" << std::endl;
    } else {
        std::cout << son << " — Uch xonali emas" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 100 dan 999 gacha bo'lgan oraliq uch xonali sonlarni ifodalaydi.

## Ishlash natijasi:
```text
458 — Uch xonali son
```

---

# 71-Topshiriq: Parol uzunligi tekshiruvi

## Topshiriq sharti:
Parol kamida 8 ta belgidan iboratligini tasdiqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string parol = "Maxfiy123";
    if (parol.length() >= 8) {
        std::cout << "Parol uzunligi yetarli." << std::endl;
    } else {
        std::cout << "Parol juda qisqa (kamida 8 ta belgi)!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `str.length()` orqali satr uzunligi tekshiriladi.

## Ishlash natijasi:
```text
Parol uzunligi yetarli.
```

---

# 72-Topshiriq: Belgi turini aniqlash (<cctype>)

## Topshiriq sharti:
Belgi katta harf, kichik harf yoki raqam ekanligini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cctype>

int main() {
    char c = 'Z';
    if (std::isupper(c)) {
        std::cout << c << " — Katta harf" << std::endl;
    } else if (std::islower(c)) {
        std::cout << c << " — Kichik harf" << std::endl;
    } else if (std::isdigit(c)) {
        std::cout << c << " — Raqam" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `<cctype>` kutubxonasi belgilar klassifikatsiyasi funksiyalarini beradi.

## Ishlash natijasi:
```text
Z — Katta harf
```

---

# 73-Topshiriq: Ikki son orasidagi farq chegarasi

## Topshiriq sharti:
Ikki son orasidagi absolyut farq 10 dan kichikligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cmath>

int main() {
    int a = 45, b = 52;
    if (std::abs(a - b) <= 10) {
        std::cout << "Sonlar bir-biriga yaqin." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::abs(a - b)` masofani hisoblaydi.

## Ishlash natijasi:
```text
Sonlar bir-biriga yaqin.
```

---

# 74-Topshiriq: Shaxmatda ot (Knight) yurishi qoidasi

## Topshiriq sharti:
Ot (x1, y1) katakdan (x2, y2) katakka qoida bo'yicha o'ta oladimi?

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cmath>

int main() {
    int x1 = 1, y1 = 1;
    int x2 = 2, y2 = 3;
    int dx = std::abs(x1 - x2);
    int dy = std::abs(y1 - y2);
    if ((dx == 1 && dy == 2) || (dx == 2 && dy == 1)) {
        std::cout << "Otning to'g'ri yurishi!" << std::endl;
    } else {
        std::cout << "Noto'g'ri yurish!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shaxmatda ot 'G' shaklida yuradi: bir yo'nalishda 1, ikkinchisida 2 katak.

## Ishlash natijasi:
```text
Otning to'g'ri yurishi!
```

---

# 75-Topshiriq: Shaxmatda shox (King) yurishi qoidasi

## Topshiriq sharti:
Shox har qanday yo'nalishda faqat 1 katak siljiy oladi.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cmath>

int main() {
    int x1 = 4, y1 = 4;
    int x2 = 5, y2 = 5;
    if (std::abs(x1 - x2) <= 1 && std::abs(y1 - y2) <= 1) {
        std::cout << "Shox yurishi to'g'ri" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Chebbi-Shev masofasi `max(dx, dy) <= 1` bo'lishi shart.

## Ishlash natijasi:
```text
Shox yurishi to'g'ri
```

---

# 76-Topshiriq: Koordinatalar choragini aniqlash

## Topshiriq sharti:
Nuqta (x, y) qaysi koordinata choragida joylashganini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int x = -3, y = 5;
    if (x > 0 && y > 0) std::cout << "I chorak";
    else if (x < 0 && y > 0) std::cout << "II chorak";
    else if (x < 0 && y < 0) std::cout << "III chorak";
    else if (x > 0 && y < 0) std::cout << "IV chorak";
    else std::cout << "O'qda joylashgan";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. X va Y ishoralari chorakni belgilaydi.

## Ishlash natijasi:
```text
II chorak
```

---

# 77-Topshiriq: To'g'ri to'rtburchak ichida nuqta tekshiruvi (Bounding Box)

## Topshiriq sharti:
Nuqta (x, y) to'g'ri to'rtburchak [x_min, x_max] x [y_min, y_max] ichidami?

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int x = 15, y = 25;
    int x1 = 10, y1 = 10, x2 = 30, y2 = 40;
    if (x >= x1 && x <= x2 && y >= y1 && y <= y2) {
        std::cout << "Nuqta soha ichida joylashgan." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'yinlar va kompyuter grafikasida to'qnashuvlarni (Collision detection) aniqlash asosi.

## Ishlash natijasi:
```text
Nuqta soha ichida joylashgan.
```

---

# 78-Topshiriq: Vaqt validatsiyasi (Soat, Daqiqa, Soniya)

## Topshiriq sharti:
Kiritilgan vaqt qiymatlari to'g'ri ekanligini tasdiqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int soat = 14, daqiqa = 30, soniya = 45;
    if (soat >= 0 && soat < 24 && daqiqa >= 0 && daqiqa < 60 && soniya >= 0 && soniya < 60) {
        std::cout << "To'g'ri vaqt formati." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Chegaralarni to'liq tekshirish.

## Ishlash natijasi:
```text
To'g'ri vaqt formati.
```

---

# 79-Topshiriq: Oy bo'yicha faslni aniqlash

## Topshiriq sharti:
Oy raqamiga (1-12) qarab yil faslini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int oy = 4; // Aprel
    if (oy == 12 || oy == 1 || oy == 2) std::cout << "Qish";
    else if (oy >= 3 && oy <= 5) std::cout << "Bahor";
    else if (oy >= 6 && oy <= 8) std::cout << "Yoz";
    else if (oy >= 9 && oy <= 11) std::cout << "Kuz";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mavsumiy guruhlash.

## Ishlash natijasi:
```text
Bahor
```

---

# 80-Topshiriq: Oydagi kunlar sonini aniqlash

## Topshiriq sharti:
Oy va yilga qarab necha kun borligini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int oy = 2, yil = 2024;
    int kunlar = 0;
    switch (oy) {
        case 1: case 3: case 5: case 7: case 8: case 10: case 12: kunlar = 31; break;
        case 4: case 6: case 9: case 11: kunlar = 30; break;
        case 2:
            kunlar = ((yil % 4 == 0 && yil % 100 != 0) || (yil % 400 == 0)) ? 29 : 28;
            break;
    }
    std::cout << "Kunlar soni: " << kunlar << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fevral oyi uchun kabisa sharti qo'llaniladi.

## Ishlash natijasi:
```text
Kunlar soni: 29
```

---

# 81-Topshiriq: Tana vazni indeksi (BMI) toifasi

## Topshiriq sharti:
BMI = vazn / (boy * boy) qiymatiga qarab salomatlik holatini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double vazn = 70.0; // kg
    double boy = 1.75;   // metr
    double bmi = vazn / (boy * boy);
    if (bmi < 18.5) std::cout << "Vazn yetishmasligi";
    else if (bmi < 25.0) std::cout << "Normal vazn";
    else if (bmi < 30.0) std::cout << "Ortiqcha vazn";
    else std::cout << "Semizlik";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tibbiy standart shkala.

## Ishlash natijasi:
```text
Normal vazn
```

---

# 82-Topshiriq: Progressiv soliq stavkasi

## Topshiriq sharti:
Daromad miqdoriga qarab soliq summasini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double daromad = 15000000;
    double soliq = 0;
    if (daromad <= 5000000) {
        soliq = daromad * 0.05;
    } else {
        soliq = 5000000 * 0.05 + (daromad - 5000000) * 0.12;
    }
    std::cout << "Hisoblangan soliq: " << soliq << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Pog'onali hisoblash modeli.

## Ishlash natijasi:
```text
Hisoblangan soliq: 1.45e+06
```

---

# 83-Topshiriq: Ruxsat darajasini tekshirish (Role-Based Access)

## Topshiriq sharti:
Foydalanuvchi roli bo'yicha tizim huquqlarini taqsimlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string rol = "admin";
    if (rol == "admin") {
        std::cout << "To'liq ruxsat (Superuser)" << std::endl;
    } else if (rol == "moderator") {
        std::cout << "Faqat tahrirlash ruxsati" << std::endl;
    } else {
        std::cout << "Faqat o'qish ruxsati" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kiberxavfsizlikda avtorizatsiya nazorati.

## Ishlash natijasi:
```text
To'liq ruxsat (Superuser)
```

---

# 84-Topshiriq: Valyuta ayirboshlash komissiyasi

## Topshiriq sharti:
Summa hajmiga qarab komissiya foizini (1% yoki 0.5%) qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double summa = 5000;
    double stavka = (summa > 1000) ? 0.005 : 0.01;
    double komissiya = summa * stavka;
    std::cout << "Komissiya: $" << komissiya << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta tranzaksiyalarga chegirma berish.

## Ishlash natijasi:
```text
Komissiya: $25
```

---

# 85-Topshiriq: Internet paketi tanlovi

## Topshiriq sharti:
Trafik hajmiga qarab eng tejamkor tarif nomini bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int gb = 25;
    if (gb <= 10) std::cout << "Tarif: Mini";
    else if (gb <= 30) std::cout << "Tarif: Standard";
    else std::cout << "Tarif: Unlimited";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Biznes mantiqini oraliqlar orqali boshqarish.

## Ishlash natijasi:
```text
Tarif: Standard
```

---

# 86-Topshiriq: Doiralar kesishishi (Circles Intersection)

## Topshiriq sharti:
Ikki doiraning markazlari va radiuslari bo'yicha kesishishini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cmath>

int main() {
    double x1 = 0, y1 = 0, r1 = 3;
    double x2 = 4, y2 = 0, r2 = 2;
    double masofa = std::sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2));
    if (masofa <= r1 + r2 && masofa >= std::abs(r1 - r2)) {
        std::cout << "Doiralar kesishadi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Geometrik tahlil va masofa formulasi.

## Ishlash natijasi:
```text
Doiralar kesishadi.
```

---

# 87-Topshiriq: Suvning agregat holati

## Topshiriq sharti:
Haroratga qarab suvning holatini (muz, suyuqlik, bug') aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double t = 105.0;
    if (t <= 0) std::cout << "Muz (Qattiq)";
    else if (t < 100) std::cout << "Suv (Suyuq)";
    else std::cout << "Bug' (Gaz)";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fizik holatlarni modellashtirish.

## Ishlash natijasi:
```text
Bug' (Gaz)
```

---

# 88-Topshiriq: 4 xonali sonning palindromligini tekshirish

## Topshiriq sharti:
Son chapdan ham, o'ngdan ham bir xil o'qilishini if bilan tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 1221;
    int b1 = n / 1000;
    int b2 = (n / 100) % 10;
    int b3 = (n / 10) % 10;
    int b4 = n % 10;
    if (b1 == b4 && b2 == b3) {
        std::cout << n << " — Palindrom son" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Raqamlarni ajratib o'zaro taqqoslash.

## Ishlash natijasi:
```text
1221 — Palindrom son
```

---

# 89-Topshiriq: 3 xonali Armstrong sonini tekshirish

## Topshiriq sharti:
Son o'z raqamlari kublarining yig'indisiga tengmi (masalan, 153)?

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 153;
    int a = n / 100;
    int b = (n / 10) % 10;
    int c = n % 10;
    if (a*a*a + b*b*b + c*c*c == n) {
        std::cout << n << " — Armstrong soni!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Raqamli matematik xususiyat.

## Ishlash natijasi:
```text
153 — Armstrong soni!
```

---

# 90-Topshiriq: Ikki oraliq kesishishi (Interval Overlap)

## Topshiriq sharti:
[a1, b1] va [a2, b2] oraliqlari umumiy nuqtaga egami?

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <algorithm>

int main() {
    int a1 = 1, b1 = 5;
    int a2 = 3, b2 = 8;
    if (std::max(a1, a2) <= std::min(b1, b2)) {
        std::cout << "Oraliqlar kesishadi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `max(start) <= min(end)` qoidasi.

## Ishlash natijasi:
```text
Oraliqlar kesishadi.
```

---

# 91-Topshiriq: Karta turini aniqlash

## Topshiriq sharti:
Karta boshidagi raqamlar bo'yicha to'lov tizimini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string karta = "8600123456789012";
    if (karta.rfind("8600", 0) == 0) std::cout << "Uzcard";
    else if (karta.rfind("9860", 0) == 0) std::cout << "Humo";
    else if (karta.rfind("4", 0) == 0) std::cout << "Visa";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Prefiks tekshiruvi orqali marshrutlash.

## Ishlash natijasi:
```text
Uzcard
```

---

# 92-Topshiriq: Chegirma foizini hisoblash

## Topshiriq sharti:
Xarid summasi $100 dan oshsa 10%, $500 dan oshsa 20% chegirma bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double summa = 600;
    double chegirma = 0;
    if (summa >= 500) chegirma = 0.20;
    else if (summa >= 100) chegirma = 0.10;
    double tolov = summa * (1 - chegirma);
    std::cout << "To'lov summasi: $" << tolov << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shartli moliya hisobi.

## Ishlash natijasi:
```text
To'lov summasi: $480
```

---

# 93-Topshiriq: Autentifikatsiya tekshiruvi

## Topshiriq sharti:
Foydalanuvchi login va parolini solishtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string login = "admin";
    std::string parol = "secret123";
    if (login == "admin" && parol == "secret123") {
        std::cout << "Muvaffaqiyatli kirdingiz!" << std::endl;
    } else {
        std::cout << "Login yoki parol xato!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xavfsiz taqqoslash.

## Ishlash natijasi:
```text
Muvaffaqiyatli kirdingiz!
```

---

# 94-Topshiriq: Tosh-Qaychi-Qog'oz o'yini natijasi

## Topshiriq sharti:
Ikki o'yinchining tanloviga qarab g'olibni aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string p1 = "tosh", p2 = "qaychi";
    if (p1 == p2) {
        std::cout << "Durang!";
    } else if ((p1 == "tosh" && p2 == "qaychi") ||
               (p1 == "qaychi" && p2 == "qog'oz") ||
               (p1 == "qog'oz" && p2 == "tosh")) {
        std::cout << "1-o'yinchi g'olib!";
    } else {
        std::cout << "2-o'yinchi g'olib!";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'yin qoidalari mantiqi.

## Ishlash natijasi:
```text
1-o'yinchi g'olib!
```

---

# 95-Topshiriq: O'qituvchi oylik maoshi ustamasi

## Topshiriq sharti:
Toifasiga qarab ustama foizini belgilang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int toifa = 1; // 1-oliy, 2-birinchi, 3-ikkinchi
    double ustama = 0;
    switch (toifa) {
        case 1: ustama = 0.50; break;
        case 2: ustama = 0.35; break;
        case 3: ustama = 0.20; break;
        default: ustama = 0.0; break;
    }
    std::cout << "Ustama foizi: " << ustama * 100 << "%" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Rag'batlantirish tizimi.

## Ishlash natijasi:
```text
Ustama foizi: 50%
```

---

# 96-Topshiriq: Avtomobil tezligi va jarima miqdori

## Topshiriq sharti:
Ruxsat etilgan tezlikdan oshish darajasiga qarab jarimani hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int tezlik = 85;
    int limit = 60;
    int farq = tezlik - limit;
    if (farq <= 0) std::cout << "Qoida buzilmadi.";
    else if (farq <= 20) std::cout << "Jarima: 1 BHM";
    else if (farq <= 40) std::cout << "Jarima: 5 BHM";
    else std::cout << "Jarima: 9 BHM";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yo'l harakati xavfsizligi shkalasi.

## Ishlash natijasi:
```text
Jarima: 5 BHM
```

---

# 97-Topshiriq: Mehmonxona mavsumiy narxi

## Topshiriq sharti:
Yoz mavsumida narxni 30% ga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double asosiy_narx = 500000;
    bool yozgi_mavsum = true;
    double yakuniy = yozgi_mavsum ? asosiy_narx * 1.30 : asosiy_narx;
    std::cout << "Xona narxi: " << yakuniy << " so'm" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dinamik narxlash (Dynamic Pricing).

## Ishlash natijasi:
```text
Xona narxi: 650000 so'm
```

---

# 98-Topshiriq: Elektr energiyasi tabaqalashtirilgan tarifi

## Topshiriq sharti:
200 kVt gacha bazaviy narx, oshgan qismiga 2 barobar narx hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    double sarf = 250; // kVt
    double baza_tarif = 450;
    double jami = 0;
    if (sarf <= 200) {
        jami = sarf * baza_tarif;
    } else {
        jami = 200 * baza_tarif + (sarf - 200) * (baza_tarif * 2);
    }
    std::cout << "Elektr to'lovi: " << jami << " so'm" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ijtimoiy norma hisoblash mantiqi.

## Ishlash natijasi:
```text
Elektr to'lovi: 135000 so'm
```

---

# 99-Topshiriq: Satr prefiksini tekshirish (C++20 starts_with)

## Topshiriq sharti:
URL manzil xavfsiz https bilan boshlanganligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string url = "https://uzai.uz";
    if (url.rfind("https://", 0) == 0) {
        std::cout << "Xavfsiz HTTPS aloqa." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tarmoq protokoli xavfsizligini tekshirish.

## Ishlash natijasi:
```text
Xavfsiz HTTPS aloqa.
```

---

# 100-Topshiriq: Amaliy Sintez: Bankomat (ATM) Dasturi

## Topshiriq sharti:
PIN-kod tekshiruvi, balansni ko'rish, pul yechish va limitlarni boshqaruvchi yaxlit mantiq.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    const int TOGRI_PIN = 7788;
    int kiritilgan_pin = 7788;
    double balans = 1500000.0;
    double yechiladigan_pul = 400000.0;
    
    if (kiritilgan_pin != TOGRI_PIN) {
        std::cout << "PIN-kod noto'g'ri! Karta bloklandi.\n";
    } else {
        std::cout << "Xush kelibsiz! Joriy balans: " << balans << " so'm\n";
        if (yechiladigan_pul <= 0) {
            std::cout << "Xato summa kiritildi.\n";
        } else if (yechiladigan_pul > balans) {
            std::cout << "Mablag' yetarli emas!\n";
        } else if (static_cast<int>(yechiladigan_pul) % 10000 != 0) {
            std::cout << "Faqat 10,000 so'mga karrali summalarni yechish mumkin!\n";
        } else {
            balans -= yechiladigan_pul;
            std::cout << "Pul berildi: " << yechiladigan_pul << " so'm\n";
            std::cout << "Qolgan balans: " << balans << " so'm\n";
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bankomat xavfsizlik va tranzaksiya qoidalarining to'liq if/else integratsiyasi.

## Ishlash natijasi:
```text
Xush kelibsiz! Joriy balans: 1.5e+06 so'm\nPul berildi: 400000 so'm\nQolgan balans: 1.1e+06 so'm
```

---

