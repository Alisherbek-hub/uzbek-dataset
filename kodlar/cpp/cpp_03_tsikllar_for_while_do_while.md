# C++ Dasturlash Tili - 3-Qism: Tsikllar (for, while, do-while, range-based for)

Ushbu qismda C++ tilida barcha turdagi takrorlanuvchi jarayonlar, klassik va zamonaviy tsikllar, qidiruv algoritmlari va kesh optimizatsiyasiga oid 50 ta amaliy topshiriq jamlangan.

---

# 101-Topshiriq: for tsikli: 1 dan 10 gacha sonlarni chiqarish

## Topshiriq sharti:
for tsiklidan foydalanib 1 dan 10 gacha bo'lgan butun sonlarni bir qatorda probel bilan ajratib ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    for (int i = 1; i <= 10; ++i) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `for` tsikli uchta qismdan iborat: initsializatsiya (`int i = 1`), shart (`i <= 10`), va inkrement (`++i`).\n2. Tsikl tanasi har safar shart bajarilganda ishga tushadi.

## Ishlash natijasi:
```text
1 2 3 4 5 6 7 8 9 10
```

---

# 102-Topshiriq: for tsikli: 10 dan 1 gacha teskari sanash

## Topshiriq sharti:
for tsikli yordamida 10 dan 1 gacha teskari tartibda sonlarni chiqaring va oxirida 'Boshlandi!' so'zini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    for (int i = 10; i >= 1; --i) {
        std::cout << i << " ";
    }
    std::cout << "Boshlandi!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boshlang'ich qiymat `i = 10`, shart `i >= 1` va dekrement `--i` teskari hisoblashni ta'minlaydi.

## Ishlash natijasi:
```text
10 9 8 7 6 5 4 3 2 1 Boshlandi!
```

---

# 103-Topshiriq: for tsikli: Juft sonlar yig'indisi

## Topshiriq sharti:
1 dan 50 gacha bo'lgan juft sonlar yig'indisini for tsikli orqali hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int yigindi = 0;
    for (int i = 2; i <= 50; i += 2) {
        yigindi += i;
    }
    std::cout << "1 dan 50 gacha juft sonlar yig'indisi: " << yigindi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `i += 2` qadami orqali faqat juft sonlar (2, 4, 6...) aylanib chiqiladi.\n2. Natija 25 ta juft sonning yig'indisi bo'lib, 650 ga teng bo'ladi.

## Ishlash natijasi:
```text
1 dan 50 gacha juft sonlar yig'indisi: 650
```

---

# 104-Topshiriq: for tsikli: Faktorial hisoblash

## Topshiriq sharti:
Berilgan son n = 6 ning faktorialini (6!) for tsikli orqali hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 6;
    long long faktorial = 1;
    for (int i = 1; i <= n; ++i) {
        faktorial *= i;
    }
    std::cout << n << "! = " << faktorial << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Faktorial tez o'suvchi miqdor bo'lgani sababli `long long` toifasi tanlandi.\n2. 6! = 1 * 2 * 3 * 4 * 5 * 6 = 720.

## Ishlash natijasi:
```text
6! = 720
```

---

# 105-Topshiriq: for tsikli: Karra jadvali

## Topshiriq sharti:
Berilgan n = 7 soni uchun 1 dan 10 gacha karra jadvalini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 7;
    for (int i = 1; i <= 10; ++i) {
        std::cout << n << " x " << i << " = " << (n * i) << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir iteratsiyada n va i ko'paytmasi hisoblanadi va chiroyli formatda ekranga uzatiladi.

## Ishlash natijasi:
```text
7 x 1 = 7\n7 x 2 = 14\n7 x 3 = 21\n7 x 4 = 28\n7 x 5 = 35\n7 x 6 = 42\n7 x 7 = 49\n7 x 8 = 56\n7 x 9 = 63\n7 x 10 = 70
```

---

# 106-Topshiriq: while tsikli: 1 dan N gacha sonlar yig'indisi

## Topshiriq sharti:
while tsiklidan foydalanib N = 100 gacha sonlarning yig'indisini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 100;
    int i = 1;
    int yigindi = 0;
    while (i <= n) {
        yigindi += i;
        ++i;
    }
    std::cout << "Yig'indi: " << yigindi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `while` tsikli shart to'g'ri bo'lgan davomida takrorlanadi.\n2. 1 dan 100 gacha yig'indi 5050 ga teng bo'ladi.

## Ishlash natijasi:
```text
Yig'indi: 5050
```

---

# 107-Topshiriq: while tsikli: Raqamlar yig'indisi

## Topshiriq sharti:
Berilgan musbat butun sonning (masalan 4825) raqamlari yig'indisini while tsikli orqali toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int son = 4825;
    int nusxa = son;
    int yigindi = 0;
    while (son > 0) {
        yigindi += son % 10;
        son /= 10;
    }
    std::cout << nusxa << " soni raqamlari yig'indisi: " << yigindi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `son % 10` sonning oxirgi raqamini oladi.\n2. `son /= 10` oxirgi raqamni o'chiradi. 4+8+2+5 = 19.

## Ishlash natijasi:
```text
4825 soni raqamlari yig'indisi: 19
```

---

# 108-Topshiriq: while tsikli: Sonni teskarisiga aylantirish

## Topshiriq sharti:
Berilgan sonni (masalan 12345) uning teskari tartibdagi soniga (54321) aylantiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int son = 12345;
    int teskari = 0;
    int temp = son;
    while (temp > 0) {
        teskari = teskari * 10 + (temp % 10);
        temp /= 10;
    }
    std::cout << son << " -> " << teskari << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir qadamda `teskari` 10 ga ko'paytirilib, yangi raqam qo'shiladi.

## Ishlash natijasi:
```text
12345 -> 54321
```

---

# 109-Topshiriq: while tsikli: Raqamlar sonini sanash

## Topshiriq sharti:
Berilgan sonning nechta raqamdan iboratligini while tsikli bilan sanang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    long long son = 9876543210LL;
    long long temp = son;
    int xonalar = 0;
    if (temp == 0) {
        xonalar = 1;
    } else {
        while (temp > 0) {
            temp /= 10;
            ++xonalar;
        }
    }
    std::cout << son << " soni " << xonalar << " xonali." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Son nolga teng bo'lguncha 10 ga bo'linadi va hisoblagich oshirib boriladi.

## Ishlash natijasi:
```text
9876543210 soni 10 xonali.
```

---

# 110-Topshiriq: do-while tsikli: Asosiy sintaksis

## Topshiriq sharti:
do-while tsiklining shart yolg'on bo'lsa ham kamida bir marta bajarilishini namoyish qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int x = 100;
    do {
        std::cout << "do-while bloki kamida 1 marta ishladi, x = " << x << std::endl;
        x++;
    } while (x < 10);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `do-while` tsiklida shart pastda tekshiriladi, shu bois blok har doim kamida bir marta ishlaydi.

## Ishlash natijasi:
```text
do-while bloki kamida 1 marta ishladi, x = 100
```

---

# 111-Topshiriq: do-while tsikli: Parol tekshirish simulyatsiyasi

## Topshiriq sharti:
Foydalanuvchi to'g'ri parolni kiritguncha do-while tsikli yordamida qayta so'rash simulyatsiyasini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    const int haqiqiyParol = 1234;
    int kiritilganParollar[] = {1111, 2222, 1234};
    int urinish = 0;
    int kiritildi;
    do {
        kiritildi = kiritilganParollar[urinish];
        std::cout << "Urinish " << (urinish + 1) << ": Kiritilgan parol: " << kiritildi << std::endl;
        urinish++;
    } while (kiritildi != haqiqiyParol);

    std::cout << "Tizimga muvaffaqiyatli kirildi!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Parol to'g'ri kelmaguncha tsikl davom etadi. To'g'ri parol 1234 kiritilganda to'xtaydi.

## Ishlash natijasi:
```text
Urinish 1: Kiritilgan parol: 1111\nUrinish 2: Kiritilgan parol: 2222\nUrinish 3: Kiritilgan parol: 1234\nTizimga muvaffaqiyatli kirildi!
```

---

# 112-Topshiriq: break operatori: Qidiruvni to'xtatish

## Topshiriq sharti:
1 dan 100 gacha bo'lgan sonlar orasida 17 ga bo'linadigan birinchi sonni toping va break bilan tsiklni yakunlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    for (int i = 1; i <= 100; ++i) {
        if (i % 17 == 0) {
            std::cout << "17 ga bo'linadigan birinchi son topildi: " << i << std::endl;
            break;
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `break` operatori tsiklni shu zahoti to'xtatadi va tsikldan keyingi qatorga o'tadi.

## Ishlash natijasi:
```text
17 ga bo'linadigan birinchi son topildi: 17
```

---

# 113-Topshiriq: continue operatori: Qadamni tashlab o'tish

## Topshiriq sharti:
1 dan 15 gacha sonlarni chiqaring, ammo 3 ga bo'linadigan sonlarni continue yordamida tashlab o'ting.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    for (int i = 1; i <= 15; ++i) {
        if (i % 3 == 0) {
            continue;
        }
        std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `continue` operatori joriy iteratsiyaning qolgan qismini o'tkazib yuboradi va keyingi qadamga o'tadi.

## Ishlash natijasi:
```text
1 2 4 5 7 8 10 11 13 14
```

---

# 114-Topshiriq: Cheksiz tsikl va undan chiqish

## Topshiriq sharti:
while(true) yoki for(;;) cheksiz tsikli hosil qiling va hisoblagich 5 ga yetganda break orqali chiqing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int sanagich = 1;
    for (;;) {
        std::cout << "Iteratsiya " << sanagich << std::endl;
        if (sanagich == 5) {
            std::cout << "Cheksiz tsikldan chiqildi." << std::endl;
            break;
        }
        sanagich++;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `for(;;)` - C++ da cheksiz tsikl hosil qilishning standart va ixcham usuli hisoblanadi.

## Ishlash natijasi:
```text
Iteratsiya 1\nIteratsiya 2\nIteratsiya 3\nIteratsiya 4\nIteratsiya 5\nCheksiz tsikldan chiqildi.
```

---

# 115-Topshiriq: Ichma-ich for tsikli: To'g'ri to'rtburchak shakli

## Topshiriq sharti:
Ichma-ich for tsikllari yordamida 4 qator va 6 ustundan iborat yulduzcha (*) to'rtburchagini chizing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    const int qatorlar = 4;
    const int ustunlar = 6;
    for (int i = 0; i < qatorlar; ++i) {
        for (int j = 0; j < ustunlar; ++j) {
            std::cout << "* ";
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tashqi tsikl qatorlarni (`i`), ichki tsikl ustunlarni (`j`) boshqaradi.

## Ishlash natijasi:
```text
* * * * * * \n* * * * * * \n* * * * * * \n* * * * * * 
```

---

# 116-Topshiriq: Ichma-ich for tsikli: To'g'ri burchakli uchburchak

## Topshiriq sharti:
Balandligi 5 qatordan iborat to'g'ri burchakli uchburchak shaklini ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 5;
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= i; ++j) {
            std::cout << "* ";
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ichki tsikl chegarasi joriy qator tartibi `i` ga bog'liq bo'ladi.

## Ishlash natijasi:
```text
* \n* * \n* * * \n* * * * \n* * * * * 
```

---

# 117-Topshiriq: Ichma-ich for tsikli: Teskari uchburchak

## Topshiriq sharti:
Balandligi 5 qator bo'lgan teskari to'g'ri burchakli uchburchak shaklini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 5;
    for (int i = n; i >= 1; --i) {
        for (int j = 1; j <= i; ++j) {
            std::cout << "* ";
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tashqi tsikl `n` dan 1 gacha kamayib boradi.

## Ishlash natijasi:
```text
* * * * * \n* * * * \n* * * \n* * \n* 
```

---

# 118-Topshiriq: Ichma-ich for tsikli: Simmetrik piramida

## Topshiriq sharti:
Balandligi 5 qator bo'lgan simmetrik piramida shaklini probellar va yulduzchalar yordamida chizing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 5;
    for (int i = 1; i <= n; ++i) {
        for (int space = 1; space <= n - i; ++space) {
            std::cout << " ";
        }
        for (int star = 1; star <= (2 * i - 1); ++star) {
            std::cout << "*";
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir qator uchun `n - i` ta probel va `2 * i - 1` ta yulduzcha chiqariladi.

## Ishlash natijasi:
```text
    *\n   ***\n  *****\n *******\n*********
```

---

# 119-Topshiriq: Ichma-ich for tsikli: Romb shakli

## Topshiriq sharti:
Piramida va teskari piramidani birlashtirib romb shaklini yasang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 3;
    for (int i = 1; i <= n; ++i) {
        for (int sp = 1; sp <= n - i; ++sp) std::cout << " ";
        for (int st = 1; st <= (2 * i - 1); ++st) std::cout << "*";
        std::cout << std::endl;
    }
    for (int i = n - 1; i >= 1; --i) {
        for (int sp = 1; sp <= n - i; ++sp) std::cout << " ";
        for (int st = 1; st <= (2 * i - 1); ++st) std::cout << "*";
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yuqori qism va pastki qism alohida tsikllar bilan shakllantiriladi.

## Ishlash natijasi:
```text
  *\n ***\n*****\n ***\n  *
```

---

# 120-Topshiriq: Karra jadvali matritsasi (1x1 dan 5x5 gacha)

## Topshiriq sharti:
Ichma-ich tsikllar yordamida 1 dan 5 gacha sonlarning karra jadvalini chiroyli tekislangan jadval ko'rinishida chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <iomanip>

int main() {
    for (int i = 1; i <= 5; ++i) {
        for (int j = 1; j <= 5; ++j) {
            std::cout << std::setw(4) << (i * j);
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::setw(4)` har bir raqam uchun 4 ta belgili kenglik ajratadi va ustunlarni tekislaydi.

## Ishlash natijasi:
```text
   1   2   3   4   5\n   2   4   6   8  10\n   3   6   9  12  15\n   4   8  12  16  20\n   5  10  15  20  25
```

---

# 121-Topshiriq: Sonning tub yoki murakkabligini aniqlash

## Topshiriq sharti:
Berilgan son n = 29 ning tub (prime) son ekanligini tsikl orqali tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 29;
    bool tub = (n > 1);
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            tub = false;
            break;
        }
    }
    if (tub) {
        std::cout << n << " - Tub son" << std::endl;
    } else {
        std::cout << n << " - Tub son emas" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sonni faqat 2 dan boshlab uning kvadrat ildizigacha (`i * i <= n`) tekshirish algoritmni O(sqrt(n)) gacha tezlashtiradi.

## Ishlash natijasi:
```text
29 - Tub son
```

---

# 122-Topshiriq: 1 dan 50 gacha bo'lgan barcha tub sonlarni topish

## Topshiriq sharti:
1 dan 50 gacha bo'lgan barcha tub sonlarni ketma-ket chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Tub sonlar: ";
    for (int num = 2; num <= 50; ++num) {
        bool tub = true;
        for (int i = 2; i * i <= num; ++i) {
            if (num % i == 0) {
                tub = false;
                break;
            }
        }
        if (tub) {
            std::cout << num << " ";
        }
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tashqi tsikl har bir sonni tekshiradi, ichki tsikl bo'linuvchanlikni aniqlaydi.

## Ishlash natijasi:
```text
Tub sonlar: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47
```

---

# 123-Topshiriq: Fibonachchi ketma-ketligi

## Topshiriq sharti:
Tsikl yordamida dastlabki 10 ta Fibonachchi sonini (0, 1, 1, 2, 3, 5, 8, 13, 21, 34) chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 10;
    long long a = 0, b = 1;
    std::cout << "Fibonachchi: ";
    for (int i = 0; i < n; ++i) {
        std::cout << a << " ";
        long long next = a + b;
        a = b;
        b = next;
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir keyingi had avvalgi ikki hadning yig'indisiga teng.

## Ishlash natijasi:
```text
Fibonachchi: 0 1 1 2 3 5 8 13 21 34
```

---

# 124-Topshiriq: EKUB (Evklid algoritmi)

## Topshiriq sharti:
while tsikli orqali ikki sonning (masalan 48 va 18) eng katta umumiy bo'luvchisini (EKUB / GCD) toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 48, b = 18;
    int x = a, y = b;
    while (y != 0) {
        int temp = y;
        y = x % y;
        x = temp;
    }
    std::cout << "EKUB(" << a << ", " << b << ") = " << x << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Evklid algoritmi qoldiq nol bo'lgunga qadar davom etadi.

## Ishlash natijasi:
```text
EKUB(48, 18) = 6
```

---

# 125-Topshiriq: EKUK (Eng Kichik Umumiy Karrali)

## Topshiriq sharti:
EKUB dan foydalanib 12 va 18 sonlarining EKUK (LCM) ini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a = 12, b = 18;
    int x = a, y = b;
    while (y != 0) {
        int temp = y;
        y = x % y;
        x = temp;
    }
    int ekub = x;
    long long ekuk = ((long long)a * b) / ekub;
    std::cout << "EKUK(" << a << ", " << b << ") = " << ekuk << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Formula: `EKUK(a, b) = (a * b) / EKUB(a, b)`.

## Ishlash natijasi:
```text
EKUK(12, 18) = 36
```

---

# 126-Topshiriq: Mukammal sonni aniqlash

## Topshiriq sharti:
O'zidan boshqa barcha bo'luvchilari yig'indisi o'ziga teng bo'lgan son mukammal son deyiladi (masalan, 28 = 1 + 2 + 4 + 7 + 14). Tsikl orqali 28 ni tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 28;
    int yigindi = 0;
    for (int i = 1; i < n; ++i) {
        if (n % i == 0) {
            yigindi += i;
        }
    }
    if (yigindi == n) {
        std::cout << n << " - Mukammal son!" << std::endl;
    } else {
        std::cout << n << " - Mukammal son emas" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bo'luvchilar topilib yig'indisi hisoblanadi va songa taqqoslanadi.

## Ishlash natijasi:
```text
28 - Mukammal son!
```

---

# 127-Topshiriq: Armstrong sonini aniqlash

## Topshiriq sharti:
3 xonali sonning har bir raqamining kublari yig'indisi o'ziga teng bo'lsa, u Armstrong soni deyiladi (masalan 153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153). Buni tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 153;
    int temp = n;
    int yigindi = 0;
    while (temp > 0) {
        int r = temp % 10;
        yigindi += (r * r * r);
        temp /= 10;
    }
    if (yigindi == n) {
        std::cout << n << " - Armstrong soni!" << std::endl;
    } else {
        std::cout << n << " - Armstrong soni emas." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir raqam ajratilib, 3-darajaga oshiriladi va qo'shiladi.

## Ishlash natijasi:
```text
153 - Armstrong soni!
```

---

# 128-Topshiriq: Polindrom sonni aniqlash

## Topshiriq sharti:
Berilgan son (masalan 12321) chapdan ham, o'ngdan ham bir xil o'qilishi (polindrom) ni tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int son = 12321;
    int temp = son;
    int teskari = 0;
    while (temp > 0) {
        teskari = teskari * 10 + (temp % 10);
        temp /= 10;
    }
    if (son == teskari) {
        std::cout << son << " - Polindrom son!" << std::endl;
    } else {
        std::cout << son << " - Polindrom emas." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Son teskarisiga aylantiriladi va asl qiymati bilan tenglashtiriladi.

## Ishlash natijasi:
```text
12321 - Polindrom son!
```

---

# 129-Topshiriq: O'nlikdan ikkilikka o'tkazish (Binary conversion)

## Topshiriq sharti:
O'nlik sanoq sistemasidagi n = 29 sonini ikkilik ko'rinishga keltirib chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <algorithm>

int main() {
    int n = 29;
    std::string ikkilik = "";
    int temp = n;
    while (temp > 0) {
        ikkilik += (temp % 2 == 0 ? '0' : '1');
        temp /= 2;
    }
    std::reverse(ikkilik.begin(), ikkilik.end());
    std::cout << n << " o'nlikda -> " << ikkilik << " ikkilikda" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Son doimiy ravishda 2 ga bo'linib, olingan qoldiqlar teskari tartibda yoziladi.

## Ishlash natijasi:
```text
29 o'nlikda -> 11101 ikkilikda
```

---

# 130-Topshiriq: Ikkilikdan o'nlikka o'tkazish

## Topshiriq sharti:
Ikkilik satrdagi '11101' sonini tsikl orqali o'nlik butun songa aylantiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string bin = "11101";
    int onlik = 0;
    for (char c : bin) {
        onlik = onlik * 2 + (c - '0');
    }
    std::cout << bin << " ikkilikda -> " << onlik << " o'nlikda" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Gorner sxemasi bo'yicha har bir bit o'qilib, natija 2 ga ko'paytirilib boriladi.

## Ishlash natijasi:
```text
11101 ikkilikda -> 29 o'nlikda
```

---

# 131-Topshiriq: Geometrik progressiya hadlari yig'indisi

## Topshiriq sharti:
Boshlang'ich hadi b1 = 2, maxraji q = 3 bo'lgan geometrik progressiyaning dastlabki 5 ta hadi yig'indisini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int b1 = 2;
    int q = 3;
    int n = 5;
    long long joriy = b1;
    long long yigindi = 0;
    for (int i = 0; i < n; ++i) {
        yigindi += joriy;
        joriy *= q;
    }
    std::cout << "Geometrik progressiya yig'indisi: " << yigindi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Hadlar: 2, 6, 18, 54, 162. Ularning yig'indisi 242.

## Ishlash natijasi:
```text
Geometrik progressiya yig'indisi: 242
```

---

# 132-Topshiriq: Arifmetik progressiya hadlari

## Topshiriq sharti:
Boshlang'ich a1 = 5, ayirma d = 4 bo'lgan progressiyaning dastlabki 6 ta hadini va yig'indisini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int a1 = 5;
    int d = 4;
    int n = 6;
    int yigindi = 0;
    std::cout << "Hadlar: ";
    for (int i = 0; i < n; ++i) {
        int an = a1 + i * d;
        std::cout << an << " ";
        yigindi += an;
    }
    std::cout << "\nYig'indi: " << yigindi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Hadlar: 5, 9, 13, 17, 21, 25. Yig'indisi: 90.

## Ishlash natijasi:
```text
Hadlar: 5 9 13 17 21 25 \nYig'indi: 90
```

---

# 133-Topshiriq: Harmonik qator yig'indisi

## Topshiriq sharti:
1 + 1/2 + 1/3 + ... + 1/n qatorining n = 10 gacha bo'lgan yig'indisini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <iomanip>

int main() {
    int n = 10;
    double yigindi = 0.0;
    for (int i = 1; i <= n; ++i) {
        yigindi += 1.0 / i;
    }
    std::cout << std::fixed << std::setprecision(4);
    std::cout << "H_10 = " << yigindi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Butun sonli bo'linishning oldini olish uchun `1.0 / i` suzuvchi nuqtali bo'lish amali qo'llanadi.

## Ishlash natijasi:
```text
H_10 = 2.9290
```

---

# 134-Topshiriq: Leybnits qatori orqali Pi sonini yaqinlashish

## Topshiriq sharti:
Leybnits formulasi: Pi/4 = 1 - 1/3 + 1/5 - 1/7 + ... qatorining 10000 ta hadi orqali Pi ni hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <iomanip>

int main() {
    int n = 10000;
    double pi_bolingan_4 = 0.0;
    double ishora = 1.0;
    for (int i = 0; i < n; ++i) {
        pi_bolingan_4 += ishora / (2 * i + 1);
        ishora = -ishora;
    }
    double pi = pi_bolingan_4 * 4.0;
    std::cout << std::fixed << std::setprecision(5);
    std::cout << "Taqribiy Pi = " << pi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Belgilar almashinib turadi: `ishora = -ishora` har qadamda manfiy va musbatga aylanadi.

## Ishlash natijasi:
```text
Taqribiy Pi = 3.14149
```

---

# 135-Topshiriq: Eyler soni (e) ni qator yordamida hisoblash

## Topshiriq sharti:
e = 1 + 1/1! + 1/2! + 1/3! + ... qatori yordamida dastlabki 10 ta had bo'yicha e ni hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <iomanip>

int main() {
    double e = 1.0;
    double faktorial = 1.0;
    for (int i = 1; i <= 10; ++i) {
        faktorial *= i;
        e += 1.0 / faktorial;
    }
    std::cout << std::fixed << std::setprecision(7);
    std::cout << "Taqribiy e = " << e << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qator juda tez yaqinlashadi, 10-hadda aniqlik 7 ta xonagacha to'g'ri chiqadi.

## Ishlash natijasi:
```text
Taqribiy e = 2.7182818
```

---

# 136-Topshiriq: Ichma-ich tsikllardan chiqish (goto yoki flag)

## Topshiriq sharti:
3 qavatli ichma-ich tsikl ichidan ma'lum shart bajarilganda darhol chiqishni bayroq (flag) orqali amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    bool topildi = false;
    for (int i = 1; i <= 5 && !topildi; ++i) {
        for (int j = 1; j <= 5 && !topildi; ++j) {
            for (int k = 1; k <= 5; ++k) {
                if (i * j * k == 24) {
                    std::cout << "Topildi: " << i << " * " << j << " * " << k << " = 24" << std::endl;
                    topildi = true;
                    break;
                }
            }
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `topildi` mantiqiy bayrog'i tashqi tsikllarning ham to'xtash shartiga kiritiladi.

## Ishlash natijasi:
```text
Topildi: 1 * 5 * 5 = 24
```

---

# 137-Topshiriq: Range-based for tsikli: Massiv elementlarini o'qish

## Topshiriq sharti:
C++11 range-based for tsikli yordamida statik massivning barcha elementlarini ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int sonlar[] = {10, 20, 30, 40, 50};
    for (int x : sonlar) {
        std::cout << x << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `for (int x : sonlar)` - konteyner yoki massivning har bir elementini navbatma-navbat nusxalab oladi.

## Ishlash natijasi:
```text
10 20 30 40 50
```

---

# 138-Topshiriq: Range-based for: Nusxa olish xususiyati

## Topshiriq sharti:
Range-based tsiklda qiymat bo'yicha olish asl massivdagi elementlarni o'zgartirmasligini namoyish qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {1, 2, 3};
    for (int x : arr) {
        x *= 10;
    }
    std::cout << "Asl massiv: " << arr[0] << " " << arr[1] << " " << arr[2] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int x` elementning nusxasi bo'lgani sababli `arr` dagi asl qiymatlar o'zgarmaydi.

## Ishlash natijasi:
```text
Asl massiv: 1 2 3
```

---

# 139-Topshiriq: Range-based for: Havola (&) orqali o'zgartirish

## Topshiriq sharti:
Range-based for tsiklida `auto&` havolasi orqali massiv elementlarini 2 barobar oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int arr[] = {2, 4, 6};
    for (auto& x : arr) {
        x *= 2;
    }
    std::cout << "Yangilangan massiv: ";
    for (const auto& x : arr) {
        std::cout << x << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `auto&` elementning o'ziga havola (reference) bo'lib, massivdagi asl qiymatlarni o'zgartirish imkonini beradi.

## Ishlash natijasi:
```text
Yangilangan massiv: 4 8 12
```

---

# 140-Topshiriq: Range-based for: const auto& orqali xavfsiz va samarali o'qish

## Topshiriq sharti:
Massiv yoki satrlar konteynerini xotiradan ortiqcha nusxa olmasdan `const auto&` orqali aylanib chiqing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>

int main() {
    std::string shaharlar[] = {"Toshkent", "Samarqand", "Buxoro", "Xiva"};
    for (const auto& shahar : shaharlar) {
        std::cout << shahar << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const auto&` katta obyektlarni nusxalash xarajatlaridan xalos qiladi va ma'lumotlarning o'zgartirilmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Toshkent Samarqand Buxoro Xiva
```

---

# 141-Topshiriq: Bir nechta o'zgaruvchili for tsikli

## Topshiriq sharti:
for tsikli sarlavhasida bir vaqtning o'zida ikkita o'zgaruvchi (biri oshuvchi, biri kamayuvchi) e'lon qilib ishlating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    for (int i = 1, j = 10; i <= j; ++i, --j) {
        std::cout << "i=" << i << ", j=" << j << " | ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `for` ning initsializatsiya va iteratsiya qismlarida vergul operatori yordamida bir nechta o'zgaruvchini boshqarish mumkin.

## Ishlash natijasi:
```text
i=1, j=10 | i=2, j=9 | i=3, j=8 | i=4, j=7 | i=5, j=6 |
```

---

# 142-Topshiriq: Sonning barcha bo'luvchilarini topish va sanash

## Topshiriq sharti:
Berilgan n = 60 sonining barcha bo'luvchilarini ekranga chiqaring va ularning umumiy sonini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 60;
    int sanagich = 0;
    std::cout << n << " ning bo'luvchilari: ";
    for (int i = 1; i <= n; ++i) {
        if (n % i == 0) {
            std::cout << i << " ";
            sanagich++;
        }
    }
    std::cout << "\nJami: " << sanagich << " ta" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1 dan n gacha sonlarga bo'linish tekshiriladi.

## Ishlash natijasi:
```text
60 ning bo'luvchilari: 1 2 3 4 5 6 10 12 15 20 30 60 \nJami: 12 ta
```

---

# 143-Topshiriq: Collatz gipotezasi (3n + 1)

## Topshiriq sharti:
Boshlang'ich n = 13 soni uchun Collatz ketma-ketligini (agar juft bo'lsa n/2, toq bo'lsa 3n+1) 1 ga yetguncha davom ettiring va qadamlar sonini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    long long n = 13;
    int qadam = 0;
    std::cout << n;
    while (n != 1) {
        if (n % 2 == 0) {
            n /= 2;
        } else {
            n = 3 * n + 1;
        }
        std::cout << " -> " << n;
        qadam++;
    }
    std::cout << "\nJami qadamlar: " << qadam << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 13 soni uchun ketma-ketlik 9 ta qadamda 1 ga yetib boradi.

## Ishlash natijasi:
```text
13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1\nJami qadamlar: 9
```

---

# 144-Topshiriq: Floyd uchburchagi

## Topshiriq sharti:
5 qatordan iborat bo'lgan o'sib boruvchi butun sonlar piramidasini (Floyd uchburchagi) chizing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int qatorlar = 5;
    int raqam = 1;
    for (int i = 1; i <= qatorlar; ++i) {
        for (int j = 1; j <= i; ++j) {
            std::cout << raqam << " ";
            raqam++;
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `raqam` o'zgaruvchisi har bir element chop etilganda uzluksiz oshib boradi.

## Ishlash natijasi:
```text
1 \n2 3 \n4 5 6 \n7 8 9 10 \n11 12 13 14 15 
```

---

# 145-Topshiriq: Paskal uchburchagi (dastlabki 5 qator)

## Topshiriq sharti:
Ichma-ich tsikl yordamida Paskal uchburchagining dastlabki 5 ta qatorini chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 5;
    for (int i = 0; i < n; ++i) {
        int qiymat = 1;
        for (int space = 0; space < n - 1 - i; ++space) {
            std::cout << " ";
        }
        for (int j = 0; j <= i; ++j) {
            std::cout << qiymat << " ";
            qiymat = qiymat * (i - j) / (j + 1);
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Paskal uchburchagida har bir had kombinatorika formulasi orqali oldingi haddan hisoblanadi.

## Ishlash natijasi:
```text
    1 \n   1 1 \n  1 2 1 \n 1 3 3 1 \n1 4 6 4 1 
```

---

# 146-Topshiriq: Tezkor darajaga ko'tarish algoritmi (Binary Exponentiation)

## Topshiriq sharti:
while tsikli orqali a^b ni O(log b) murakkablikda tezkor hisoblang (masalan, 2^10 = 1024).

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    long long asos = 2;
    int daraja = 10;
    long long natija = 1;
    long long a = asos;
    int b = daraja;

    while (b > 0) {
        if (b % 2 == 1) {
            natija *= a;
        }
        a *= a;
        b /= 2;
    }
    std::cout << asos << "^" << daraja << " = " << natija << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikkilik darajaga ko'tarish b ni ikkiga bo'lib, a ni kvadratga oshirib boradi.

## Ishlash natijasi:
```text
2^10 = 1024
```

---

# 147-Topshiriq: Shaxmat taxtasi naqshini chizish

## Topshiriq sharti:
Ichma-ich tsikllar yordamida 4x4 o'lchamli shaxmat taxtasi shashka naqshini (# va .) chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int n = 4;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if ((i + j) % 2 == 0) {
                std::cout << "# ";
            } else {
                std::cout << ". ";
            }
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `(i + j) % 2` juft bo'lsa `#`, toq bo'lsa `.` belgisi qo'yiladi.

## Ishlash natijasi:
```text
# . # . \n. # . # \n# . # . \n. # . # 
```

---

# 148-Topshiriq: Konsolli yuklanish indikatori (Progress bar simulyatsiyasi)

## Topshiriq sharti:
for tsikli orqali konsolda 0% dan 100% gacha bo'lgan progress bar simulyatsiyasini amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Jarayon: [";
    int jamiQadamlar = 10;
    for (int i = 1; i <= jamiQadamlar; ++i) {
        std::cout << "=";
    }
    std::cout << "] 100% Bajarildi!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tsikl har bir qadamda yangi progress belgisini (`=`) chiqaradi.

## Ishlash natijasi:
```text
Jarayon: [==========] 100% Bajarildi!
```

---

# 149-Topshiriq: Tsikllarda kesh xotirasi bilan ishlash (Row-major order)

## Topshiriq sharti:
C++ da 2 o'lchamli massivlarni qator bo'yicha aylanish CPU kesh liniyasi (cache line) uchun eng samarali usul ekanligini namoyish qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    const int ROWS = 3, COLS = 4;
    int matrix[ROWS][COLS] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };
    long long sum = 0;
    // C++ da qator bo'yicha yurish (Row-major) keshni optimal ishlatadi
    for (int i = 0; i < ROWS; ++i) {
        for (int j = 0; j < COLS; ++j) {
            sum += matrix[i][j];
        }
    }
    std::cout << "Matritsa elementlari yig'indisi: " << sum << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++ da ko'p o'lchamli massivlar xotirada qatorlar ketma-ketligida (row-major) saqlanadi.\n2. Tashqi tsikl `i` va ichki tsikl `j` bo'lsa, xotira bloklari ketma-ket o'qiladi va cache miss kamayadi.

## Ishlash natijasi:
```text
Matritsa elementlari yig'indisi: 78
```

---

# 150-Topshiriq: Tsikl invarianti va yakuniy xulosa

## Topshiriq sharti:
Massivdagi eng katta elementni topish misolida tsikl invarianti (har qadamda joriy maksimal qiymat to'g'ri saqlanishi) ni amalda ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int sonlar[] = {14, 52, 9, 87, 43, 65, 87, 21};
    int n = sizeof(sonlar) / sizeof(sonlar[0]);
    int max_qiymat = sonlar[0];

    // Tsikl invarianti: har bir i qadamida max_qiymat sonlar[0..i] oraliqdagi eng kattasidir
    for (int i = 1; i < n; ++i) {
        if (sonlar[i] > max_qiymat) {
            max_qiymat = sonlar[i];
        }
    }
    std::cout << "Massivdagi eng katta element: " << max_qiymat << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tsikl invarianti algoritm to'g'riligini isbotlovchi mantiqiy qoidadir.\n2. Massiv to'liq aylanib chiqilgach, `max_qiymat` butun massivning maksimumi bo'ladi.

## Ishlash natijasi:
```text
Massivdagi eng katta element: 87
```

---

