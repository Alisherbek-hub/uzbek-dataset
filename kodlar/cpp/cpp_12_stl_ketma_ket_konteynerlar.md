# C++ Dasturlash Tili - 12-Qism: STL Ketma-ket Konteynerlar (vector, deque, list, forward_list, span)

Ushbu qismda std::vector, reserve, capacity, emplace_back, deque, list, forward_list, C++20 std::span, iteratorlar va kesh lokalligiga oid 50 ta amaliy topshiriq jamlangan.

---

# 551-Topshiriq: STL Arxitekturasi asoslari

## Topshiriq sharti:
STL ning uchta asosiy ustuni: Konteyner, Iterator va Algoritmning birgalikda ishlashini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> sonlar = {5, 2, 8, 1, 9}; // Konteyner
    std::sort(sonlar.begin(), sonlar.end());   // Algoritm va Iteratorlar
    for (auto it = sonlar.begin(); it != sonlar.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. STL konteynerlari ma'lumotlarni saqlaydi, iteratorlar ko'rsatkich kabi bog'laydi, algoritmlar esa ularni qayta ishlaydi.

## Ishlash natijasi:
```text
1 2 5 8 9 
```

---

# 552-Topshiriq: std::vector asoslari: push_back va chiqarish

## Topshiriq sharti:
Dinamik `std::vector` yaratib, elementlar qo'shing va indeks orqali chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;
    v.push_back(10);
    v.push_back(20);
    v.push_back(30);
    for (size_t i = 0; i < v.size(); ++i) {
        std::cout << v[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::vector` avtomatik kengayuvchi dinamik massiv bo'lib, xotirani o'zi boshqaradi.

## Ishlash natijasi:
```text
10 20 30 
```

---

# 553-Topshiriq: size() va capacity() farqi

## Topshiriq sharti:
Vektor elementlari soni (`size()`) va uning hozirgi xotira sig'imi (`capacity()`) o'zgarishini kuzating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;
    for (int i = 1; i <= 5; ++i) {
        v.push_back(i);
        std::cout << "Element qo'shildi: " << i 
                  << " | size: " << v.size() 
                  << " | capacity: " << v.capacity() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `capacity()` tugaganda vektor odatda 1.5 yoki 2 barobar kattaroq yangi xotira ajratadi va elementlarni ko'chiradi.

## Ishlash natijasi:
```text
Element qo'shildi: 1 | size: 1 | capacity: 1\nElement qo'shildi: 2 | size: 2 | capacity: 2\nElement qo'shildi: 3 | size: 3 | capacity: 3\nElement qo'shildi: 4 | size: 4 | capacity: 4\nElement qo'shildi: 5 | size: 5 | capacity: 6
```

---

# 554-Topshiriq: reserve() orqali ortiqcha allokatsiyalarni yo'qotish

## Topshiriq sharti:
`reserve()` orqali xotirani oldindan band qilib, qayta allokatsiya xarajatlarini bartaraf eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;
    v.reserve(100); // 100 ta element uchun joy birdan ajratildi
    std::cout << "Boshlang'ich capacity: " << v.capacity() << std::endl;
    v.push_back(1);
    v.push_back(2);
    std::cout << "Hozirgi size: " << v.size() << ", capacity: " << v.capacity() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta hajmdagi ma'lumotlar qo'shilishidan oldin `reserve()` chaqirish dastur tezligini keskin oshiradi.

## Ishlash natijasi:
```text
Boshlang'ich capacity: 100\nHozirgi size: 2, capacity: 100
```

---

# 555-Topshiriq: resize() va standart qiymat

## Topshiriq sharti:
`resize()` yordamida vektor hajmini oshirib, yangi elementlarni sukut bo'yicha qiymatlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {1, 2, 3};
    v.resize(6, 99); // 6 tagacha kengaytirish, yetmaganini 99 bilan to'ldirish
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `resize()` haqiqiy elementlar sonini o'zgartiradi va yangi obyektlarni konstruksiya qiladi.

## Ishlash natijasi:
```text
1 2 3 99 99 99 
```

---

# 556-Topshiriq: shrink_to_fit() orqali xotirani ixchamlashtirish

## Topshiriq sharti:
Ishlatilmayotgan zaxira xotirani OS ga qaytarish uchun `shrink_to_fit()` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;
    v.reserve(1000);
    v.push_back(10);
    std::cout << "shrink oldidan capacity: " << v.capacity() << std::endl;
    v.shrink_to_fit();
    std::cout << "shrink keyin capacity: " << v.capacity() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `shrink_to_fit()` capacity ni size darajasiga tushirib beradi.

## Ishlash natijasi:
```text
shrink oldidan capacity: 1000\nshrink keyin capacity: 1
```

---

# 557-Topshiriq: emplace_back ning push_back dan afzalligi

## Topshiriq sharti:
`emplace_back` vaqtinchalik obyekt yaratmasdan to'g'ridan-to'g'ri xotirada qurishini (in-place) ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

struct Nuqta {
    int x, y;
    Nuqta(int a, int b) : x(a), y(b) {
        std::cout << "Nuqta qurildi\n";
    }
};

int main() {
    std::vector<Nuqta> v;
    v.reserve(2);
    v.emplace_back(10, 20); // Konstruktor argumentlari to'g'ridan-to'g'ri uzatildi
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `emplace_back` vaqtinchalik obyekt va ortiqcha nusxalash xarajatlarini yo'qotadi.

## Ishlash natijasi:
```text
Nuqta qurildi
```

---

# 558-Topshiriq: Vektorda xavfsiz at() metodi

## Topshiriq sharti:
Chegaradan chiqib ketish xavfini `.at()` va `try-catch` bilan boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <stdexcept>

int main() {
    std::vector<int> v = {10, 20};
    try {
        std::cout << v.at(5) << std::endl;
    } catch (const std::out_of_range& e) {
        std::cout << "Xatolik tutildi: Indeks mavjud emas!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.at()` chegara tekshiruvini olib boradi va noto'g'ri indeksda istisno tashlaydi.

## Ishlash natijasi:
```text
Xatolik tutildi: Indeks mavjud emas!
```

---

# 559-Topshiriq: front() va back() metodlari

## Topshiriq sharti:
Vektorning birinchi va oxirgi elementlarini o'qish va o'zgartirish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {100, 200, 300};
    v.front() = 111;
    v.back() = 333;
    std::cout << "Birinchi: " << v.front() << ", Oxirgi: " << v.back() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `front()` va `back()` birinchi va oxirgi elementlarga havola (`T&`) qaytaradi.

## Ishlash natijasi:
```text
Birinchi: 111, Oxirgi: 333
```

---

# 560-Topshiriq: Iteratorlar asoslari (begin va end)

## Topshiriq sharti:
Iterator orqali vektorni aylanib chiqish va qiymatlarini ko'rish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {11, 22, 33};
    for (std::vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `begin()` birinchi elementga, `end()` esa oxirgi elementdan keyingi xotiraga ko'rsatadi.

## Ishlash natijasi:
```text
11 22 33 
```

---

# 561-Topshiriq: Teskari iteratorlar (rbegin va rend)

## Topshiriq sharti:
`rbegin()` va `rend()` orqali vektorni teskari tartibda aylanib chiqing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    for (auto it = v.rbegin(); it != v.rend(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `rbegin()` oxirgi elementdan boshlab oldinga qarab harakatlanadi.

## Ishlash natijasi:
```text
5 4 3 2 1 
```

---

# 562-Topshiriq: Doimiy iteratorlar (cbegin va cend)

## Topshiriq sharti:
O'zgartirishni taqiqlovchi xavfsiz `cbegin()` va `cend()` iteratorlaridan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {10, 20, 30};
    for (auto it = v.cbegin(); it != v.cend(); ++it) {
        // *it = 99; // Kompilyatsiya xatosi: const iterator orqali o'zgartirib bo'lmaydi
        std::cout << *it << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `cbegin()` o'qish xavfsizligini kafolatlaydi.

## Ishlash natijasi:
```text
10 20 30 
```

---

# 563-Topshiriq: Vektordan element o'chirish: erase()

## Topshiriq sharti:
Ko'rsatilgan pozitsiyadagi elementni `.erase()` orqali o'chiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {10, 20, 30, 40};
    v.erase(v.begin() + 1); // 20 o'chirildi
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.erase()` ko'rsatilgan elementni o'chirib, qolgan elementlarni chapga suradi.

## Ishlash natijasi:
```text
10 30 40 
```

---

# 564-Topshiriq: Vektor o'rtasiga element kiritish: insert()

## Topshiriq sharti:
Belgilangan indeksga yangi qiymatni `.insert()` orqali joylashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {10, 30, 40};
    v.insert(v.begin() + 1, 20); // 1-indeksga 20 qo'yildi
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.insert()` elementlarni o'ngga surib berilgan joyga yangi qiymat kiritadi.

## Ishlash natijasi:
```text
10 20 30 40 
```

---

# 565-Topshiriq: Iteratorlarning yaroqsizlanishi (Iterator Invalidation)

## Topshiriq sharti:
`push_back` tufayli xotira qayta ajratilganda eski iteratorlar yaroqsiz bo'lib qolishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {1, 2};
    auto it = v.begin();
    v.push_back(3); // Qayta allokatsiya yuz berishi mumkin!
    // *it; // Xavfli! Eski manzil yaroqsizlangan bo'lishi mumkin
    std::cout << "Allokatsiyadan so'ng yangi iterator olish shart." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Vektor kengayganda uning barcha mavjud iteratorlari va ko'rsatkichlari bekor qilinadi.

## Ishlash natijasi:
```text
Allokatsiyadan so'ng yangi iterator olish shart.
```

---

# 566-Topshiriq: Erase-Remove Idiomasi

## Topshiriq sharti:
Vektordan barcha 0 qiymatlarini klassik `erase-remove` orqali tozalang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 0, 2, 0, 3, 0, 4};
    v.erase(std::remove(v.begin(), v.end(), 0), v.end());
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::remove` elementlarni chapga suradi, `v.erase` esa ortiqcha qismini kesib tashlaydi.

## Ishlash natijasi:
```text
1 2 3 4 
```

---

# 567-Topshiriq: std::erase va std::erase_if (C++20)

## Topshiriq sharti:
C++20 ning super qulay `std::erase_if` yordamida barcha juft sonlarni bir qatorda o'chiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5, 6};
    std::erase_if(v, [](int x) { return x % 2 == 0; });
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++20 `std::erase_if` qadimgi murakkab Erase-Remove idiomasini o'rniga kelgan.

## Ishlash natijasi:
```text
1 3 5 
```

---

# 568-Topshiriq: std::vector<bool> ning 1-bitli siqilgan tabiati

## Topshiriq sharti:
Nima uchun `std::vector<bool>` oddiy vektor emas, balki bitlar to'plami ekanligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<bool> v = {true, false, true, true};
    std::cout << "sizeof(vector<bool>): " << sizeof(v) << " bayt" << std::endl;
    std::cout << "Har bir bool faqat 1 bit egallaydi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::vector<bool>` 1 baytda 8 ta qiymat saqlaydi, shu bois uning elementlariga oddiy `bool&` havola olib bo'lmaydi.

## Ishlash natijasi:
```text
sizeof(vector<bool>): ... bayt\nHar bir bool faqat 1 bit egallaydi.
```

---

# 569-Topshiriq: std::deque (Double-ended queue) asoslari

## Topshiriq sharti:
Boshidan ham, oxiridan ham O(1) tezlikda qo'shish va olish imkonini beruvchi `std::deque` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <deque>

int main() {
    std::deque<int> dq;
    dq.push_back(10);
    dq.push_front(5);
    dq.push_back(20);
    for (int x : dq) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::deque` har ikki tomondan samarali ishlaydi va indekslashni (`dq[i]`) qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
5 10 20 
```

---

# 570-Topshiriq: std::deque: pop_front va pop_back

## Topshiriq sharti:
Dekning oldi va orqa elementlarini navbatma-navbat o'chiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <deque>

int main() {
    std::deque<std::string> navbat = {"A", "B", "C", "D"};
    navbat.pop_front(); // A ketdi
    navbat.pop_back();  // D ketdi
    for (const auto& s : navbat) std::cout << s << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `pop_front()` O(1) tezlikda ishlaydi, `std::vector` da esa boshidan o'chirish O(N) vaqt oladi.

## Ishlash natijasi:
```text
B C 
```

---

# 571-Topshiriq: std::deque ning xotiradagi bo'lingan (Chunked) tuzilishi

## Topshiriq sharti:
Nima uchun `deque` yagona uzluksiz xotira blokida bo'lmasdan bir nechta qismlardan iboratligini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "std::deque xotirani qat'iy o'lchamdagi sahifalar (chunks) "
              << "va ularga ko'rsatuvchi indeks jadvali orqali boshqaradi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shu sababli kengayganda butun xotirani ko'chirish talab qilinmaydi va mavjud elementlar ko'rsatkichlari buzilmaydi.

## Ishlash natijasi:
```text
std::deque xotirani qat'iy o'lchamdagi sahifalar (chunks) va ularga ko'rsatuvchi indeks jadvali orqali boshqaradi.
```

---

# 572-Topshiriq: std::list (Doubly Linked List) asoslari

## Topshiriq sharti:
Ikki tomonlama bog'langan ro'yxat `std::list` yarating va elementlarni chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <list>

int main() {
    std::list<int> l = {10, 20, 30};
    l.push_front(5);
    l.push_back(40);
    for (int x : l) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::list` da har bir element o'z qiymati va oldingi hamda keyingi tugunga ko'rsatkichni saqlaydi.

## Ishlash natijasi:
```text
5 10 20 30 40 
```

---

# 573-Topshiriq: std::list da ixtiyoriy joyga O(1) qo'shish va o'chirish

## Topshiriq sharti:
Iterator turgan joyga yangi element kiritish massiv siljitishni talab qilmasligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <list>

int main() {
    std::list<int> l = {1, 3};
    auto it = l.begin();
    ++it; // 3 ga ko'rsatmoqda
    l.insert(it, 2); // 3 dan oldin 2 kiritildi O(1)
    for (int x : l) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qo'shish va o'chirish faqat bir nechta ko'rsatkichlarni yangilash bilan amalga oshadi.

## Ishlash natijasi:
```text
1 2 3 
```

---

# 574-Topshiriq: std::list splice metodi (Ro'yxatlarni nusxalamasdan ulash)

## Topshiriq sharti:
Bitta ro'yxat qismini ikkinchisiga O(1) vaqtda ko'chirib o'tkazing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <list>

int main() {
    std::list<int> l1 = {1, 2};
    std::list<int> l2 = {3, 4};
    l1.splice(l1.end(), l2); // l2 elementlari l1 ga ulandi, l2 bo'sh qoldi
    for (int x : l1) std::cout << x << " ";
    std::cout << "| l2 hajmi: " << l2.size() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.splice()` xotira qayta ajratmasdan faqat tugunlar ko'rsatkichlarini qayta ulab qo'yadi.

## Ishlash natijasi:
```text
1 2 3 4 | l2 hajmi: 0
```

---

# 575-Topshiriq: std::list ning ichki sort() va reverse() metodlari

## Topshiriq sharti:
Nima uchun `std::sort` emas, balki `l.sort()` chaqirilishi kerakligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <list>

int main() {
    std::list<int> l = {40, 10, 30, 20};
    l.sort();    // list uchun maxsus saralash
    l.reverse(); // teskari qilish
    for (int x : l) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::list` Random Access iteratorga ega bo'lmagani sababli `std::sort` u bilan ishlay olmaydi, shuning uchun ichki `l.sort()` qo'llanadi.

## Ishlash natijasi:
```text
40 30 20 10 
```

---

# 576-Topshiriq: std::forward_list (Bir tomonlama bog'langan ro'yxat - C++11)

## Topshiriq sharti:
Xotirani eng minimal sarflovchi `std::forward_list` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <forward_list>

int main() {
    std::forward_list<int> fl = {10, 20, 30};
    fl.push_front(5);
    for (int x : fl) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `forward_list` faqat oldinga qarab harakatlanadi va har bir tugun faqat 1 ta ko'rsatkich saqlaydi.

## Ishlash natijasi:
```text
5 10 20 30 
```

---

# 577-Topshiriq: forward_list: insert_after va erase_after

## Topshiriq sharti:
Bir tomonlama ro'yxatda amallar faqat joriy elementdan keyingisiga ta'sir qilishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <forward_list>

int main() {
    std::forward_list<int> fl = {10, 30};
    fl.insert_after(fl.begin(), 20); // 10 dan keyin 20 qo'yildi
    for (int x : fl) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bir tomonlama bog'langanlik sababli `insert` emas, aynan `insert_after` ishlatiladi.

## Ishlash natijasi:
```text
10 20 30 
```

---

# 578-Topshiriq: std::span (C++20 Zero-copy View)

## Topshiriq sharti:
Dinamik vektor va statik massivni nusxalamasdan bitta funksiyada `std::span` orqali qabul qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <span>
#include <vector>

void chopSpan(std::span<const int> s) {
    for (int x : s) std::cout << x << " ";
    std::cout << std::endl;
}

int main() {
    int arr[] = {1, 2, 3};
    std::vector<int> v = {4, 5, 6};
    chopSpan(arr);
    chopSpan(v);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::span` har qanday uzluksiz xotira blokini ortiqcha nusxasiz qabul qiladi.

## Ishlash natijasi:
```text
1 2 3 \n4 5 6 
```

---

# 579-Topshiriq: std::span ning subspan metodi

## Topshiriq sharti:
Massivning faqat bir qismini xotira nusxalamasdan `subspan` orqali ko'ring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <span>

int main() {
    int sonlar[] = {10, 20, 30, 40, 50};
    std::span<int> sp(sonlar);
    auto bo'lak = sp.subspan(1, 3); // 20, 30, 40
    for (int x : bo'lak) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `subspan(offset, count)` xotirani qayta ajratmaydi, faqat ko'rsatkich va o'lchamni belgilaydi.

## Ishlash natijasi:
```text
20 30 40 
```

---

# 580-Topshiriq: std::distance va iteratorlar masofasi

## Topshiriq sharti:
`std::distance` orqali ikki iterator orasidagi masofani hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <iterator>

int main() {
    std::vector<int> v = {10, 20, 30, 40, 50};
    auto bosh = v.begin();
    auto oxir = v.end();
    std::cout << "Elementlar soni: " << std::distance(bosh, oxir) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Random Access iteratorlarda `std::distance` O(1), ro'yxatlarda esa O(N) vaqt oladi.

## Ishlash natijasi:
```text
Elementlar soni: 5
```

---

# 581-Topshiriq: std::advance, std::next va std::prev

## Topshiriq sharti:
Iteratorlarni xavfsiz va qulay surish vositalarini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <list>
#include <iterator>

int main() {
    std::list<int> l = {10, 20, 30, 40};
    auto it = l.begin();
    std::advance(it, 2); // 2 qadam oldinga surish
    std::cout << "advance keyin: " << *it << std::endl;
    auto oldingi = std::prev(it);
    std::cout << "prev qiymati: " << *oldingi << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::next` va `std::prev` iteratorni joyida o'zgartirmasdan yangi iterator qaytaradi.

## Ishlash natijasi:
```text
advance keyin: 30\nprev qiymati: 20
```

---

# 582-Topshiriq: 2D Dinamik massiv: std::vector<std::vector<int>>

## Topshiriq sharti:
Vektorlar vektori orqali 3x3 o'lchamli dinamik matritsani boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<std::vector<int>> mat(2, std::vector<int>(3, 7));
    mat[0][1] = 9;
    for (size_t i = 0; i < mat.size(); ++i) {
        for (size_t j = 0; j < mat[i].size(); ++j) {
            std::cout << mat[i][j] << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir satr alohida vektor bo'lib, har xil uzunlikda ham bo'lishi mumkin.

## Ishlash natijasi:
```text
7 9 7 \n7 7 7 
```

---

# 583-Topshiriq: Kesh-do'stona 1D vektor orqali 2D ma'lumotlarni saqlash

## Topshiriq sharti:
Nima uchun `vector<vector<T>>` dan ko'ra bitta `vector<T>` va `[r * cols + c]` formulasi ancha tez ekanligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    int rows = 2, cols = 3;
    std::vector<int> flat(rows * cols, 0);
    flat[1 * cols + 2] = 42; // (1, 2) elementi
    std::cout << "flat[1, 2] = " << flat[1 * cols + 2] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitta vektor barcha ma'lumotlarni RAM da ketma-ket saqlaydi, bu esa CPU keshini 100% samarali qiladi.

## Ishlash natijasi:
```text
flat[1, 2] = 42
```

---

# 584-Topshiriq: Vektorni tozalash: clear() va capacity saqlanishi

## Topshiriq sharti:
`.clear()` chaqirilganda elementlar yo'qolsa-da, xotira ajratilganicha qolishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    v.clear();
    std::cout << "size: " << v.size() << ", capacity: " << v.capacity() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `clear()` xotirani qaytarib bermaydi, bu esa keyingi qo'shishlarda qayta allokatsiyani oldini oladi.

## Ishlash natijasi:
```text
size: 0, capacity: 5
```

---

# 585-Topshiriq: Vektorlar almashinuvi: swap() O(1)

## Topshiriq sharti:
Ikki gigant vektor xotirasini `swap` orqali 0 vaqtda (faqat ko'rsatkichlarni) almashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v1(1000, 1);
    std::vector<int> v2(2000, 2);
    v1.swap(v2);
    std::cout << "v1 hajmi: " << v1.size() << ", v2 hajmi: " << v2.size() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.swap()` ichki uchta ko'rsatkichni (`start`, `finish`, `end_of_storage`) almashtiradi.

## Ishlash natijasi:
```text
v1 hajmi: 2000, v2 hajmi: 1000
```

---

# 586-Topshiriq: Xom ko'rsatkichni olish: vector::data()

## Topshiriq sharti:
Vektor xotirasini `v.data()` orqali xom C massivi kabi C-kutubxonalarga uzatish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void cFunksiya(const int* arr, int n) {
    for (int i = 0; i < n; ++i) std::cout << arr[i] << " ";
    std::cout << std::endl;
}

int main() {
    std::vector<int> v = {10, 20, 30};
    cFunksiya(v.data(), v.size());
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `v.data()` ichki xom ko'rsatkichni qaytaradi va C API lari bilan to'liq mos keladi.

## Ishlash natijasi:
```text
10 20 30 
```

---

# 587-Topshiriq: Range Constructor orqali vektorni to'ldirish

## Topshiriq sharti:
Oddiy statik massivdan iteratorlar oralig'i orqali yangi vektor yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    int arr[] = {7, 14, 21, 28};
    std::vector<int> v(arr + 1, arr + 3); // 14, 21
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Range konstruktor har qanday iteratorlar oralig'idagi elementlarni nusxalaydi.

## Ishlash natijasi:
```text
14 21 
```

---

# 588-Topshiriq: Vektor ichida maxsus sinf obyektlarini to'g'ri saqlash

## Topshiriq sharti:
`emplace_back` bilan yangi obyektlarni vektorga joylashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <string>

class Xodim {
public:
    std::string ism;
    Xodim(std::string i) : ism(i) {}
};

int main() {
    std::vector<Xodim> korxona;
    korxona.emplace_back("Dilshod");
    std::cout << "Xodim: " << korxona[0].ism << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Obyektlar to'g'ridan-to'g'ri vektor ichida quriladi.

## Ishlash natijasi:
```text
Xodim: Dilshod
```

---

# 589-Topshiriq: vector::assign metodi

## Topshiriq sharti:
Vektorning barcha eski ma'lumotlarini o'chirib yangi ketma-ketlik bilan to'ldiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {1, 2, 3};
    v.assign(4, 100); // 4 ta 100 bilan to'ldirish
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.assign()` butun konteynerni yangi qiymatlar bilan qayta to'ldiradi.

## Ishlash natijasi:
```text
100 100 100 100 
```

---

# 590-Topshiriq: Vektor elementlarini range-based for bilan o'zgartirish

## Topshiriq sharti:
Havola `auto&` orqali vektorning barcha elementlarini 5 ga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {10, 20, 30};
    for (auto& x : v) x += 5;
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `auto&` orqali to'g'ridan-to'g'ri vektor ichidagi qiymatlar tahrirlanadi.

## Ishlash natijasi:
```text
15 25 35 
```

---

# 591-Topshiriq: Vector vs Deque vs List unumdorlik tahlili

## Topshiriq sharti:
Qaysi konteyner kesh uchun eng maqbul ekanligini xulosa qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Tahlil: std::vector uzluksiz xotirasi (contiguity) tufayli "
              << "99% holatlarda deque va list dan bir necha barobar tez ishlaydi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Protsessorlar ketma-ket xotirani tezroq yuklaydi (Hardware Prefetching).

## Ishlash natijasi:
```text
Tahlil: std::vector uzluksiz xotirasi (contiguity) tufayli 99% holatlarda deque va list dan bir necha barobar tez ishlaydi.
```

---

# 592-Topshiriq: Vektorda massivlar almashinuvi (In-place reverse)

## Topshiriq sharti:
Iteratorlar yordamida vektorni teskarisiga aylantiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3, 4};
    std::reverse(v.begin(), v.end());
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::reverse` Random Access iteratorlar bilan O(N) vaqtda ishlaydi.

## Ishlash natijasi:
```text
4 3 2 1 
```

---

# 593-Topshiriq: std::deque orqali siljuvchi oyna (Sliding Window Maximum asoslari)

## Topshiriq sharti:
Deque yordamida o'lchami k bo'lgan oynadagi eng katta elementlarni kuzatish g'oyasi.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <deque>
#include <vector>

int main() {
    std::deque<int> d;
    d.push_back(10);
    d.push_back(20);
    std::cout << "Oynadagi oxirgi: " << d.back() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Monoton deq yordamida sliding window O(N) da yechiladi.

## Ishlash natijasi:
```text
Oynadagi oxirgi: 20
```

---

# 594-Topshiriq: Konteynerlar uchun Custom Allocator tushunchasi

## Topshiriq sharti:
STL konteynerlariga maxsus xotira ajratgich biriktirish imkoniyati (`std::vector<T, Alloc>`).

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::cout << "Custom Allocator orqali std::vector ni Memory Pool, Shared Memory "
              << "yoki GPU xotirasiga moslashtirish mumkin." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. STL konteynerlarining ikkinchi parametri doimo allokator hisoblanadi.

## Ishlash natijasi:
```text
Custom Allocator orqali std::vector ni Memory Pool, Shared Memory yoki GPU xotirasiga moslashtirish mumkin.
```

---

# 595-Topshiriq: std::list orqali LRU Kesh ro'yxatini yuritish

## Topshiriq sharti:
Ro'yxat boshiga elementni o'tkazish O(1) bo'lgani sababli LRU Kesh uchun `std::list` qo'llash.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <list>

int main() {
    std::list<int> lru = {1, 2, 3};
    // 3 ishlatildi, uni boshiga suramiz:
    auto it = lru.end(); --it;
    lru.splice(lru.begin(), lru, it);
    for (int x : lru) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.splice()` elementni nusxalamasdan O(1) da boshiga o'tkazadi.

## Ishlash natijasi:
```text
3 1 2 
```

---

# 596-Topshiriq: std::vector::pop_back unumdorligi

## Topshiriq sharti:
Oxirgi elementni o'chirish O(1) vaqt olishini va xotira allokatsiyasini talab qilmasligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {10, 20, 30};
    v.pop_back();
    std::cout << "Yangi oxirgi: " << v.back() << ", hajm: " << v.size() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `pop_back()` faqat destruktorni chaqiradi va `size` ni 1 ga kamaytiradi.

## Ishlash natijasi:
```text
Yangi oxirgi: 20, hajm: 2
```

---

# 597-Topshiriq: Vektorlar tengligini solishtirish (operator==)

## Topshiriq sharti:
Ikki vektorning barcha elementlari bir xilligini `==` bilan tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> a = {1, 2, 3};
    std::vector<int> b = {1, 2, 3};
    std::cout << "a va b tengmi: " << (a == b ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Vektorlar o'zaro leksikografik taqqoslash operatorlariga (`==`, `<`, `>`) ega.

## Ishlash natijasi:
```text
a va b tengmi: Ha
```

---

# 598-Topshiriq: Konteyner elementlarini std::fill bilan to'ldirish

## Topshiriq sharti:
`std::fill` algoritmi yordamida vektor elementlarini bir xil qiymat bilan to'ldiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v(4);
    std::fill(v.begin(), v.end(), 7);
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::fill` iteratorlar oralig'iga berilgan qiymatni tezkor yozadi.

## Ishlash natijasi:
```text
7 7 7 7 
```

---

# 599-Topshiriq: Bjarne Stroustrup nima uchun har doim std::vector ni tavsiya qiladi

## Topshiriq sharti:
Modern CPU arxitekturasida L1/L2 kesh lokalligi ko'rsatkichlar sakrashidan ancha muhimligini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Stroustrup qoidasi: Agar maxsus sabab bo'lmasa, har doim std::vector ni tanlang. "
              << "Kesh tezligi har qanday nazariy bog'langan ro'yxatdan ustundir!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zamonaviy apparatda ketma-ket xotirani o'qish tasodifiy sakrashlardan 10-50 baravar tezroqdir.

## Ishlash natijasi:
```text
Stroustrup qoidasi: Agar maxsus sabab bo'lmasa, har doim std::vector ni tanlang. Kesh tezligi har qanday nazariy bog'langan ro'yxatdan ustundir!
```

---

# 600-Topshiriq: 12-qism xulosasi: Ketma-ket Konteynerlar Strategiyasi

## Topshiriq sharti:
Vector - standart tanlov, Deque - ikki tomonlama navbatlar, List - faqat tez-tez splice qilish uchun, Span - xotirani ko'rish uchun eng zo'r vositadir.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Ketma-ket konteynerlar o'zlashtirildi: std::vector va std::span zamonaviy C++ ning eng qudratli kuchi!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xotira samaradorligi bo'yicha to'g'ri konteyner tanlash eng asosiy mahoratdir.

## Ishlash natijasi:
```text
Ketma-ket konteynerlar o'zlashtirildi: std::vector va std::span zamonaviy C++ ning eng qudratli kuchi!
```

---

