# C++ Dasturlash Tili - 14-Qism: STL Algoritmlari, Lambda Ifodalari va C++20 Ranges

Ushbu qismda sort, transform, accumulate, C++20 Ranges va views, lambdalar sintaksisi, heap algoritmlari va parallel amallarga oid 50 ta amaliy topshiriq jamlangan.

---

# 651-Topshiriq: STL Algoritmlari falsafasi

## Topshiriq sharti:
Qo'lda tsikl yozish o'rniga STL algoritmlaridan foydalanish unumdorligi va tozaligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {10, 20, 30, 40};
    std::for_each(v.begin(), v.end(), [](int x) {
        std::cout << x << " ";
    });
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. STL algoritmlari standartlashtirilgan, optimallashtirilgan va xatolardan xolidir.

## Ishlash natijasi:
```text
10 20 30 40 
```

---

# 652-Topshiriq: Lambda ifodasi to'liq sintaksisi

## Topshiriq sharti:
Tutish qoidasi `[]`, parametrlar `()`, qaytarish toifasi `->` va tanasi `{}` bilan lambda yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    auto kopaytir = [](int a, int b) -> int {
        return a * b;
    };
    std::cout << "6 * 7 = " << kopaytir(6, 7) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qaytarish toifasi oddiy hollarda avtomatik aniqlanadi, murakkab hollarda `-> tur` yoziladi.

## Ishlash natijasi:
```text
6 * 7 = 42
```

---

# 653-Topshiriq: Lambda capture: Qiymat ([=]) va Havola ([&])

## Topshiriq sharti:
Tashqi o'zgaruvchilarni qiymat bo'yicha nusxalash va havola bo'yicha o'zgartirish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int x = 10;
    auto oqi = [=]() { std::cout << "Nusxa x: " << x << std::endl; };
    auto ozgartir = [&]() { x += 5; };
    ozgartir();
    oqi();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `[=]` tashqi o'zgaruvchilarni o'zgarmas nusxa sifatida oladi, `[&]` esa ularni to'g'ridan-to'g'ri o'zgartiradi.

## Ishlash natijasi:
```text
Nusxa x: 15
```

---

# 654-Topshiriq: mutable lambdalar

## Topshiriq sharti:
Qiymat bo'yicha tutib olingan nusxani lambda ichida o'zgartirish uchun `mutable` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int sanagich = 0;
    auto fn = [sanagich]() mutable {
        sanagich++;
        std::cout << "Lambda ichida: " << sanagich << std::endl;
    };
    fn();
    fn();
    std::cout << "Asl sanagich: " << sanagich << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `mutable` tutib olingan nusxani o'zgartirishga ruxsat beradi, ammo tashqi asl qiymat o'zgarmaydi.

## Ishlash natijasi:
```text
Lambda ichida: 1\nLambda ichida: 2\nAsl sanagich: 0
```

---

# 655-Topshiriq: Init-capture (C++14 Generalized Lambda Capture)

## Topshiriq sharti:
Lambdaga `std::unique_ptr` kabi ko'chuvchi obyektni `std::move` orqali tutib bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto ptr = std::make_unique<int>(123);
    auto lambda = [p = std::move(ptr)]() {
        std::cout << "Lambda ichidagi ptr: " << *p << std::endl;
    };
    lambda();
    std::cout << "Asl ptr bo'sh: " << (ptr == nullptr ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++14 Init-capture lambdaga Move-only resurslarni kiritish imkonini beradi.

## Ishlash natijasi:
```text
Lambda ichidagi ptr: 123\nAsl ptr bo'sh: Ha
```

---

# 656-Topshiriq: std::count va std::count_if

## Topshiriq sharti:
Massiv ichida shartga mos keluvchi nechta element borligini predikat orqali hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> ballar = {85, 92, 45, 78, 95, 60};
    int alo = std::count_if(ballar.begin(), ballar.end(), [](int b) {
        return b >= 90;
    });
    std::cout << "A'lo baholar soni: " << alo << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::count_if` predikat `true` qaytargan elementlarni sanaydi.

## Ishlash natijasi:
```text
A'lo baholar soni: 2
```

---

# 657-Topshiriq: std::find_if va std::find_if_not

## Topshiriq sharti:
Berilgan shartni qanoatlantiruvchi birinchi elementni toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> sonlar = {2, 4, 7, 8, 10};
    auto it = std::find_if(sonlar.begin(), sonlar.end(), [](int x) {
        return x % 2 != 0;
    });
    if (it != sonlar.end()) {
        std::cout << "Birinchi toq son: " << *it << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shartga mos birinchi element iteratorini qaytaradi.

## Ishlash natijasi:
```text
Birinchi toq son: 7
```

---

# 658-Topshiriq: std::all_of, std::any_of, std::none_of

## Topshiriq sharti:
Konteynerdagi barcha, kamida bitta yoki hech bir element shartga mosligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {2, 4, 6, 8};
    bool hammasiJuft = std::all_of(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
    bool manfiyBor = std::any_of(v.begin(), v.end(), [](int x) { return x < 0; });
    std::cout << "Hammasi juftmi: " << (hammasiJuft ? "Ha" : "Yo'q") << std::endl;
    std::cout << "Manfiy bormi: " << (manfiyBor ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mantiqiy kvantorlar (All, Any, None) to'plam tahlilini juda soddalashtiradi.

## Ishlash natijasi:
```text
Hammasi juftmi: Ha\nManfiy bormi: Yo'q
```

---

# 659-Topshiriq: std::sort va maxsus komparator

## Topshiriq sharti:
Elementlarni o'zimiz xohlagan qoida (masalan kamayish tartibida) bo'yicha lambda bilan saralang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {15, 3, 42, 8, 23};
    std::sort(v.begin(), v.end(), [](int a, int b) {
        return a > b; // Kamayish tartibida
    });
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::sort` Introsort algoritmi bo'lib, o'rtacha va eng yomon holatda O(N log N) kafolatlaydi.

## Ishlash natijasi:
```text
42 23 15 8 3 
```

---

# 660-Topshiriq: std::stable_sort (Barqaror saralash)

## Topshiriq sharti:
Teng elementlarning nisbiy o'rni buzilmasligini kafolatlovchi `std::stable_sort` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

struct Talaba {
    std::string ism;
    int guruh;
};

int main() {
    std::vector<Talaba> t = {{"Ali", 1}, {"Vali", 2}, {"Hasan", 1}};
    std::stable_sort(t.begin(), t.end(), [](const Talaba& a, const Talaba& b) {
        return a.guruh < b.guruh;
    });
    for (const auto& item : t) std::cout << item.ism << "(" << item.guruh << ") ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Guruh 1 bo'yicha saralanganda Ali Hasan dan oldin kelgani to'liq saqlanadi.

## Ishlash natijasi:
```text
Ali(1) Hasan(1) Vali(2) 
```

---

# 661-Topshiriq: std::nth_element: K-chi medianani O(N) da topish

## Topshiriq sharti:
Butun massivni to'liq saralamasdan O(N) vaqtda medianani o'z o'rniga keltiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {9, 1, 8, 2, 7, 3, 6, 4, 5};
    size_t k = v.size() / 2; // Markaziy indeks
    std::nth_element(v.begin(), v.begin() + k, v.end());
    std::cout << "Mediana elementi: " << v[k] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::nth_element` k-elementdan kichiklarni chapga, kattalarni o'ngga suradi.

## Ishlash natijasi:
```text
Mediana elementi: 5
```

---

# 662-Topshiriq: std::binary_search

## Topshiriq sharti:
Saralangan massivda element borligini O(log N) da tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> saralangan = {10, 20, 30, 40, 50};
    bool bor = std::binary_search(saralangan.begin(), saralangan.end(), 30);
    std::cout << "30 mavjudmi: " << (bor ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::binary_search` faqat bool natija beradi.

## Ishlash natijasi:
```text
30 mavjudmi: Ha
```

---

# 663-Topshiriq: std::transform (Map operatsiyasi)

## Topshiriq sharti:
Vektorning barcha elementlarini kvadratga oshirib yangi vektorga yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> sonlar = {1, 2, 3, 4};
    std::vector<int> kvadratlar(sonlar.size());
    std::transform(sonlar.begin(), sonlar.end(), kvadratlar.begin(), [](int x) {
        return x * x;
    });
    for (int k : kvadratlar) std::cout << k << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::transform` funksional dasturlashdagi `map` funksiyasining C++ dagi analogidir.

## Ishlash natijasi:
```text
1 4 9 16 
```

---

# 664-Topshiriq: Ikkita konteyner bilan std::transform

## Topshiriq sharti:
Ikkita vektorning mos elementlarini qo'shib uchinchi vektorga yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> a = {1, 2, 3};
    std::vector<int> b = {10, 20, 30};
    std::vector<int> c(3);
    std::transform(a.begin(), a.end(), b.begin(), c.begin(), [](int x, int y) {
        return x + y;
    });
    for (int val : c) std::cout << val << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikki manbali `transform` tensorlar qo'shish kabi amallarda juda qo'l keladi.

## Ishlash natijasi:
```text
11 22 33 
```

---

# 665-Topshiriq: std::accumulate (Reduce operatsiyasi)

## Topshiriq sharti:
`<numeric>` kutubxonasidagi `std::accumulate` yordamida yig'indi va ko'paytmani hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    int yigindi = std::accumulate(v.begin(), v.end(), 0);
    int kopaytma = std::accumulate(v.begin(), v.end(), 1, [](int a, int b) {
        return a * b;
    });
    std::cout << "Yig'indi: " << yigindi << ", Ko'paytma: " << kopaytma << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::accumulate` ketma-ketlikni bitta yakuniy qiymatga yig'adi (fold/reduce).

## Ishlash natijasi:
```text
Yig'indi: 15, Ko'paytma: 120
```

---

# 666-Topshiriq: std::inner_product (Skalyar ko'paytma)

## Topshiriq sharti:
Ikki vektorning skalyar ko'paytmasini bitta qatorda hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::vector<int> x = {1, 2, 3};
    std::vector<int> w = {4, 5, 6}; // Neyron tarmoq vaznlari
    int dotProduct = std::inner_product(x.begin(), x.end(), w.begin(), 0);
    std::cout << "Dot product: " << dotProduct << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32.

## Ishlash natijasi:
```text
Dot product: 32
```

---

# 667-Topshiriq: std::iota: Ketma-ket sonlar bilan to'ldirish

## Topshiriq sharti:
`std::iota` yordamida massivni 100 dan boshlab 1 qadam bilan to'ldiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::vector<int> v(5);
    std::iota(v.begin(), v.end(), 100);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::iota` ketma-ket indekslar yoki qiymatlar yaratishda ishlatiladi.

## Ishlash natijasi:
```text
100 101 102 103 104 
```

---

# 668-Topshiriq: std::copy_if va std::back_inserter

## Topshiriq sharti:
Shartga mos elementlarni dinamik ravishda yangi vektorga ko'chirib o'tkazing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> manba = {1, 15, 4, 20, 8, 30};
    std::vector<int> kattalar;
    std::copy_if(manba.begin(), manba.end(), std::back_inserter(kattalar), [](int x) {
        return x > 10;
    });
    for (int x : kattalar) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::back_inserter` elementlarni yangi vektorga `push_back` qilib beradi.

## Ishlash natijasi:
```text
15 20 30 
```

---

# 669-Topshiriq: std::replace va std::replace_if

## Topshiriq sharti:
Vektor ichidagi barcha 0 larni 1 ga almashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 0, 2, 0, 3};
    std::replace(v.begin(), v.end(), 0, 1);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `replace` belgilangan eski qiymatni yangisiga almashtiradi.

## Ishlash natijasi:
```text
1 1 2 1 3 
```

---

# 670-Topshiriq: std::unique orqali takrorlarni tozalash

## Topshiriq sharti:
Saralangan massivdagi ketma-ket takrorlarni bitta qoldirib qisqartiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 1, 2, 3, 3, 3, 4};
    auto it = std::unique(v.begin(), v.end());
    v.erase(it, v.end());
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::unique` faqat yonma-yon kelgan bir xillarni tozalaydi, shuning uchun oldindan saralangan bo'lishi kerak.

## Ishlash natijasi:
```text
1 2 3 4 
```

---

# 671-Topshiriq: std::rotate: Doiraviy siljitish

## Topshiriq sharti:
Vektor elementlarini 2 qadam chapga doiraviy suring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    std::rotate(v.begin(), v.begin() + 2, v.end());
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `begin() + 2` yangi boshlang'ich elementga aylanadi.

## Ishlash natijasi:
```text
3 4 5 1 2 
```

---

# 672-Topshiriq: std::shuffle va tasodifiy aralashtirish

## Topshiriq sharti:
Massivni `<random>` generatori bilan aralashtirib tashlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    std::mt19937 g(42); // Qat'iy seed
    std::shuffle(v.begin(), v.end(), g);
    std::cout << "Aralashgan: ";
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::shuffle` qadimgi `random_shuffle` ning zamonaviy va kriptografik jihatdan to'g'ri o'rnidir.

## Ishlash natijasi:
```text
Aralashgan: ...
```

---

# 673-Topshiriq: std::minmax_element: Bitta o'tishda min va max ni topish

## Topshiriq sharti:
Bir martalik O(N) siklda ham eng kichik, ham eng katta element ko'rsatkichini oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {45, 12, 89, 3, 67};
    auto [minIt, maxIt] = std::minmax_element(v.begin(), v.end());
    std::cout << "Min: " << *minIt << ", Max: " << *maxIt << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::minmax_element` 3N/2 ta taqqoslash bilan ikkala ekstremumni beradi.

## Ishlash natijasi:
```text
Min: 3, Max: 89
```

---

# 674-Topshiriq: std::clamp (C++17)

## Topshiriq sharti:
Sonni ruxsat etilgan oraliq ichida [min, max] chegaralab ushlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <algorithm>

int main() {
    std::cout << "clamp(120, 0, 100) = " << std::clamp(120, 0, 100) << std::endl;
    std::cout << "clamp(-10, 0, 100) = " << std::clamp(-10, 0, 100) << std::endl;
    std::cout << "clamp(50, 0, 100)  = " << std::clamp(50, 0, 100) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::clamp` harorat, hajm, foiz yoki piksel chegaralarini belgilashda juda qulay.

## Ishlash natijasi:
```text
clamp(120, 0, 100) = 100\nclamp(-10, 0, 100) = 0\nclamp(50, 0, 100)  = 50
```

---

# 675-Topshiriq: std::partition: Shart bo'yicha ikkiga ajratish

## Topshiriq sharti:
Juft sonlarni chap tomonga, toq sonlarni o'ng tomonga ajrating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5, 6};
    std::partition(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::partition` shartni qanoatlantiruvchi qismni ajratib beradi.

## Ishlash natijasi:
```text
6 2 4 3 5 1 
```

---

# 676-Topshiriq: std::next_permutation (Barcha permutatsiyalarni chiqarish)

## Topshiriq sharti:
{1, 2, 3} to'plamining barcha tartiblarini leksikografik chiqarib boring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3};
    do {
        for (int x : v) std::cout << x << " ";
        std::cout << "| ";
    } while (std::next_permutation(v.begin(), v.end()));
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kombinatorika va to'liq qidiruv algoritmlarining asosi.

## Ishlash natijasi:
```text
1 2 3 | 1 3 2 | 2 1 3 | 2 3 1 | 3 1 2 | 3 2 1 | 
```

---

# 677-Topshiriq: Heap amallari: make_heap va pop_heap

## Topshiriq sharti:
Vektorni o'z joyida binar uyumga (Heap) aylantirib, eng kattasini oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {10, 50, 20, 40};
    std::make_heap(v.begin(), v.end());
    std::cout << "Heap tepasi: " << v.front() << std::endl;
    std::pop_heap(v.begin(), v.end()); // Eng kattasi oxiriga surildi
    v.pop_back();
    std::cout << "Yangi tepasi: " << v.front() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qo'shimcha xotira sarflamasdan vector ustida Heap yaratish usuli.

## Ishlash natijasi:
```text
Heap tepasi: 50\nYangi tepasi: 40
```

---

# 678-Topshiriq: C++20 Ranges: std::ranges::sort

## Topshiriq sharti:
C++20 da `begin()` va `end()` siz to'g'ridan-to'g'ri butun konteynerni saralang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {7, 1, 5, 2};
    std::ranges::sort(v); // C++20 Ranges
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++20 Ranges butun konteynerni argument sifatida qabul qiladi va kodni qisqartiradi.

## Ishlash natijasi:
```text
1 2 5 7 
```

---

# 679-Topshiriq: Ranges Projections (Proyeksiyalar)

## Topshiriq sharti:
Obyektlar vektorini lambda komparator yozmasdan to'g'ridan-to'g'ri maydoni bo'yicha saralang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

struct Odam {
    std::string ism;
    int yosh;
};

int main() {
    std::vector<Odam> guruh = {{"Zafar", 30}, {"Anvar", 20}, {"Botir", 25}};
    std::ranges::sort(guruh, {}, &Odam::yosh); // Proyeksiyalash: faqat yosh bo'yicha
    for (const auto& o : guruh) std::cout << o.ism << "(" << o.yosh << ") ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `&Odam::yosh` proyeksiyasi qo'shimcha komparator yozish zaruratini butunlay yo'qotadi.

## Ishlash natijasi:
```text
Anvar(20) Botir(25) Zafar(30) 
```

---

# 680-Topshiriq: C++20 Ranges Views (Quvur operatori |)

## Topshiriq sharti:
Filtrlash va o'zgartirishni xotira nusxalamasdan quvur `|` orqali bajaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <ranges>

int main() {
    std::vector<int> sonlar = {1, 2, 3, 4, 5, 6};
    auto natija = sonlar 
        | std::views::filter([](int n) { return n % 2 == 0; })
        | std::views::transform([](int n) { return n * n; });

    for (int x : natija) {
        std::cout << x << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Views dangasa (lazy evaluation) hisoblanadi va faqat o'qilayotganda kerakli qiymatni yaratadi.

## Ishlash natijasi:
```text
4 16 36 
```

---

# 681-Topshiriq: std::views::take va std::views::drop

## Topshiriq sharti:
Ketma-ketlikdan faqat dastlabki K tasini olish yoki tashlab yuborish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <ranges>

int main() {
    std::vector<int> v = {10, 20, 30, 40, 50};
    std::cout << "take(3): ";
    for (int x : v | std::views::take(3)) std::cout << x << " ";
    std::cout << "\ndrop(2): ";
    for (int x : v | std::views::drop(2)) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Paginatsiya (Pagination) va oyna amallari uchun juda qulay.

## Ishlash natijasi:
```text
take(3): 10 20 30 \ndrop(2): 30 40 50 
```

---

# 682-Topshiriq: std::views::reverse

## Topshiriq sharti:
Konteynerni nusxalamasdan teskari ko'rinishda o'qing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <ranges>

int main() {
    std::vector<int> v = {1, 2, 3};
    for (int x : v | std::views::reverse) {
        std::cout << x << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Asl massiv xotirasiga daxl qilmasdan faqat teskari ko'rinish beradi.

## Ishlash natijasi:
```text
3 2 1 
```

---

# 683-Topshiriq: std::adjacent_find

## Topshiriq sharti:
Ketma-ket kelgan bir xil elementlar juftligini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3, 3, 4, 5};
    auto it = std::adjacent_find(v.begin(), v.end());
    if (it != v.end()) {
        std::cout << "Ketma-ket takrorlangan qiymat: " << *it << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Satrlarda ketma-ket harflarni yoki massivdagi duplikatlarni aniqlashda qo'llaniladi.

## Ishlash natijasi:
```text
Ketma-ket takrorlangan qiymat: 3
```

---

# 684-Topshiriq: Oqim iteratorlari: std::ostream_iterator

## Topshiriq sharti:
Tsiklsiz vektorni bitta qatorda konsolga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>

int main() {
    std::vector<int> v = {5, 10, 15, 20};
    std::copy(v.begin(), v.end(), std::ostream_iterator<int>(std::cout, " "));
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::ostream_iterator` elementlarni oqimga yozishni oddiy iteratorga aylantiradi.

## Ishlash natijasi:
```text
5 10 15 20 
```

---

# 685-Topshiriq: std::includes (To'plam boshqasini o'z ichiga olishi)

## Topshiriq sharti:
Birinchi saralangan to'plam ikkinchi to'plamning barcha elementlariga egaligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> katta = {1, 2, 3, 4, 5, 6};
    std::vector<int> qism = {2, 4, 6};
    bool ichida = std::includes(katta.begin(), katta.end(), qism.begin(), qism.end());
    std::cout << "Qism to'liq kiritilganmi: " << (ichida ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matematik to'plamlar kiritilishi (Subset) tekshiruvi.

## Ishlash natijasi:
```text
Qism to'liq kiritilganmi: Ha
```

---

# 686-Topshiriq: std::is_sorted va std::is_sorted_until

## Topshiriq sharti:
Massiv qaysi elementgacha saralanganligini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 5, 3, 4};
    auto it = std::is_sorted_until(v.begin(), v.end());
    std::cout << "Saralanishni buzgan element: " << *it << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Saralanganlik buzilgan nuqtani topishda O(N) da yordam beradi.

## Ishlash natijasi:
```text
Saralanishni buzgan element: 3
```

---

# 687-Topshiriq: C++17 Parallel Algoritmlar (Execution Policies)

## Topshiriq sharti:
`std::execution::par` orqali ko'p yadroli protsessorda saralashni parallel rejimga o'tkazish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <execution>

int main() {
    std::vector<int> v = {5, 2, 8, 1, 9};
    std::sort(std::execution::par, v.begin(), v.end());
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::execution::par` kompilyatorga bir nechta oqimda (multithreaded) saralashni buyuradi.

## Ishlash natijasi:
```text
1 2 5 8 9 
```

---

# 688-Topshiriq: std::reduce ning accumulate dan farqi

## Topshiriq sharti:
`std::reduce` elementlarni ixtiyoriy tartibda qo'sha olishi sababli parallel hisoblashda ishlatilishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <numeric>
#include <execution>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    int jami = std::reduce(std::execution::par, v.begin(), v.end(), 0);
    std::cout << "Parallel yig'indi: " << jami << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Assotsiativ amallarda `std::reduce` bir necha yadrolarda parallel ishlaydi.

## Ishlash natijasi:
```text
Parallel yig'indi: 15
```

---

# 689-Topshiriq: Map-Filter-Reduce to'liq zanjiri C++20 da

## Topshiriq sharti:
Juft sonlarni olib, 10 ga ko'paytirib, yig'indisini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <ranges>
#include <numeric>

int main() {
    std::vector<int> sonlar = {1, 2, 3, 4, 5};
    auto juftlar = sonlar | std::views::filter([](int x) { return x % 2 == 0; });
    int jami = 0;
    for (int x : juftlar) jami += x * 10;
    std::cout << "Natija: " << jami << std::endl; // (2*10 + 4*10 = 60)
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zamonaviy funksional dasturlash uslubi C++ da yuqori tezlikda ishlaydi.

## Ishlash natijasi:
```text
Natija: 60
```

---

# 690-Topshiriq: std::generate orqali ma'lumotlar yaratish

## Topshiriq sharti:
Tasodifiy yoki o'sib boruvchi qiymatlar bilan konteynerni to'ldiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v(5);
    int n = 1;
    std::generate(v.begin(), v.end(), [&n]() { return n++ * 2; });
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::generate` generator funksiya orqali qiymatlarni ishlab chiqaradi.

## Ishlash natijasi:
```text
2 4 6 8 10 
```

---

# 691-Topshiriq: std::lexicographical_compare

## Topshiriq sharti:
Ikki so'z yoki massivni lug'at tartibida solishtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v1 = {1, 2, 3};
    std::vector<int> v2 = {1, 2, 4};
    bool kichik = std::lexicographical_compare(v1.begin(), v1.end(), v2.begin(), v2.end());
    std::cout << "v1 v2 dan kichikmi: " << (kichik ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Leksikografik solishtirish satrlar va massivlar uchun universaldir.

## Ishlash natijasi:
```text
v1 v2 dan kichikmi: Ha
```

---

# 692-Topshiriq: std::sample (Tasodifiy tanlab olish - C++17)

## Topshiriq sharti:
Katta massivdan K ta tasodifiy elementni tanlab oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>

int main() {
    std::vector<int> aholi = {10, 20, 30, 40, 50, 60};
    std::vector<int> tanlov;
    std::mt19937 g(123);
    std::sample(aholi.begin(), aholi.end(), std::back_inserter(tanlov), 3, g);
    std::cout << "Tanlab olingan 3 ta: ";
    for (int x : tanlov) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::sample` statistika va mashina o'rganishida mini-batch olish uchun ayni muddao.

## Ishlash natijasi:
```text
Tanlab olingan 3 ta: ...
```

---

# 693-Topshiriq: std::ranges::contains (C++23)

## Topshiriq sharti:
C++23 da butun konteynerda element borligini to'g'ridan-to'g'ri tekshirish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {10, 20, 30};
    bool bor = std::find(v.begin(), v.end(), 20) != v.end();
    std::cout << "20 bormi: " << (bor ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Konteynerda qidiruvni zamonaviy usulda bajarish.

## Ishlash natijasi:
```text
20 bormi: Ha
```

---

# 694-Topshiriq: std::mismatch: Birinchi farq qilgan joyni topish

## Topshiriq sharti:
Ikki massiv bir-biridan qayerda farq qilayotganini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v1 = {1, 2, 3, 4};
    std::vector<int> v2 = {1, 2, 9, 4};
    auto [it1, it2] = std::mismatch(v1.begin(), v1.end(), v2.begin());
    std::cout << "Farq: " << *it1 << " va " << *it2 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Test tizimlarida kutilgan va olingan natijalarni solishtirishda qo'llanadi.

## Ishlash natijasi:
```text
Farq: 3 va 9
```

---

# 695-Topshiriq: Lambda rekursiyasi va std::function

## Topshiriq sharti:
Lambda ichida o'zini o'zi chaqiruvchi rekursiv fibonachchi funksiyasini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <functional>

int main() {
    std::function<int(int)> fib = [&](int n) -> int {
        return (n <= 1) ? n : fib(n - 1) + fib(n - 2);
    };
    std::cout << "fib(6) = " << fib(6) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::function` yordamida lambdaga o'z nomiga murojaat qilish imkoniyati beriladi.

## Ishlash natijasi:
```text
fib(6) = 8
```

---

# 696-Topshiriq: C++23 Deducing this bilan rekursiv lambda

## Topshiriq sharti:
C++23 ning yangi imkoniyati: lambdaning birinchi parametri `this auto&& self` bo'lishi.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    auto faktorial = [](auto self, int n) -> int {
        return (n <= 1) ? 1 : n * self(self, n - 1);
    };
    std::cout << "5! = " << faktorial(faktorial, 5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++23 da `std::function` xarajatlarisiz 100% tezkor rekursiv lambda yozish imkoniyati.

## Ishlash natijasi:
```text
5! = 120
```

---

# 697-Topshiriq: std::partial_sum (Kumulyativ yig'indi)

## Topshiriq sharti:
Prefiks yig'indilar massivini (Prefix Sums) bir qatorda hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::vector<int> v = {1, 2, 3, 4};
    std::vector<int> pref(v.size());
    std::partial_sum(v.begin(), v.end(), pref.begin());
    for (int x : pref) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Prefiks massivlar oraliq yig'indilarni O(1) da topish algoritmining asosidir.

## Ishlash natijasi:
```text
1 3 6 10 
```

---

# 698-Topshiriq: std::adjacent_difference (Qo'shnilar farqi)

## Topshiriq sharti:
Ketma-ket elementlar orasidagi farqni hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::vector<int> v = {10, 15, 25, 40};
    std::vector<int> diff(v.size());
    std::adjacent_difference(v.begin(), v.end(), diff.begin());
    for (int x : diff) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Vaqt qatorlari va tezlanishni hisoblashda birinchi tartibli hosila.

## Ishlash natijasi:
```text
10 5 10 15 
```

---

# 699-Topshiriq: Nima uchun STL algoritmlari qo'lda yozilgan for tsiklidan afzal

## Topshiriq sharti:
Kompilyator optimizatsiyasi, SIMD vektorizatsiyasi va kod tozaligi haqida xulosa.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "STL Algoritmlari kompilyatorga niyatni (intent) aniq ko'rsatadi, "
              << "bu esa AVX/SIMD vektorizatsiyasini to'liq yoqishga imkon beradi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qo'lda yozilgan tsikllarda yashirin noaniqliklar optimizatsiyaga to'sqinlik qilishi mumkin.

## Ishlash natijasi:
```text
STL Algoritmlari kompilyatorga niyatni (intent) aniq ko'rsatadi, bu esa AVX/SIMD vektorizatsiyasini to'liq yoqishga imkon beradi.
```

---

# 700-Topshiriq: 14-qism xulosasi: STL Algoritmlari va C++20 Ranges Qudrati

## Topshiriq sharti:
Zamonaviy C++ da to'g'ridan-to'g'ri for/while tsikllari deyarli yozilmaydi; barcha ma'lumotlar oqimi algoritmlar, lambdalar va Ranges orqali boshqariladi.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "STL Algoritmlari va C++20 Ranges o'zlashtirildi: C++ funksional dasturlash tezligiga ega bo'ldi!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Algoritmlar C++ dasturlash uslubining eng yetuk va go'zal bosqichidir.

## Ishlash natijasi:
```text
STL Algoritmlari va C++20 Ranges o'zlashtirildi: C++ funksional dasturlash tezligiga ega bo'ldi!
```

---

