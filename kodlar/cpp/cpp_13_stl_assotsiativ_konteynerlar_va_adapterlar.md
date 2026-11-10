# C++ Dasturlash Tili - 13-Qism: STL Assotsiativ Konteynerlar va Adapterlar

Ushbu qismda std::set, std::map, std::multiset, std::unordered_map, std::stack, std::queue, std::priority_queue, std::bitset, C++17/C++20 metodlari va memoizatsiyaga oid 50 ta amaliy topshiriq jamlangan.

---

# 601-Topshiriq: Assotsiativ konteynerlar tushunchasi (Daraxt vs Xesh-jadval)

## Topshiriq sharti:
Tartiblangan (std::set/map - Red-Black Tree) va tartiblanmagan (unordered - Hash Table) konteynerlar farqini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "std::set/map: Qizil-qora daraxt, doimo saralangan, O(log N) qidiruv.\n"
              << "std::unordered_set/map: Xesh-jadval, tartibsiz, o'rtacha O(1) qidiruv." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qidiruv tezligi muhim bo'lsa unordered, elementlar tartibi yoki oraliq so'rovlari kerak bo'lsa ordered konteynerlar tanlanadi.

## Ishlash natijasi:
```text
std::set/map: Qizil-qora daraxt, doimo saralangan, O(log N) qidiruv.\nstd::unordered_set/map: Xesh-jadval, tartibsiz, o'rtacha O(1) qidiruv.
```

---

# 602-Topshiriq: std::set asoslari: Noyob va avtomatik saralangan to'plam

## Topshiriq sharti:
`std::set` yaratib, takroriy qiymatlar tushib qolishini va tartiblanishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>

int main() {
    std::set<int> s = {5, 2, 8, 2, 5, 1};
    for (int x : s) {
        std::cout << x << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::set` faqat noyob (unique) qiymatlarni saqlaydi va ularni o'sish tartibida joylashtiradi.

## Ishlash natijasi:
```text
1 2 5 8 
```

---

# 603-Topshiriq: std::set: insert, find va count

## Topshiriq sharti:
To'plamda element bor-yo'qligini `find()` va `count()` orqali aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>

int main() {
    std::set<std::string> mevalar = {"olma", "anor", "uzum"};
    mevalar.insert("banan");
    if (mevalar.find("anor") != mevalar.end()) {
        std::cout << "Anor to'plamda mavjud!" << std::endl;
    }
    std::cout << "Uzum soni: " << mevalar.count("uzum") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `find()` topilsa iterator, topilmasa `end()` qaytaradi. `count()` 0 yoki 1 beradi.

## Ishlash natijasi:
```text
Anor to'plamda mavjud!\nUzum soni: 1
```

---

# 604-Topshiriq: C++20 set::contains metodi

## Topshiriq sharti:
C++20 ning ixcham `.contains()` metodi orqali mavjudlikni tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>

int main() {
    std::set<int> idlar = {101, 202, 303};
    if (idlar.contains(202)) {
        std::cout << "202 ID si mavjud!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.contains()` metodi `find() != end()` tekshiruvini qulay bool qiymatiga aylantirdi.

## Ishlash natijasi:
```text
202 ID si mavjud!
```

---

# 605-Topshiriq: std::set dan element o'chirish: erase()

## Topshiriq sharti:
To'plamdan qiymat yoki iterator bo'yicha elementni o'chiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>

int main() {
    std::set<int> s = {10, 20, 30, 40};
    s.erase(20); // 20 qiymatini o'chirish
    for (int x : s) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.erase(val)` o'chirilgan elementlar sonini qaytaradi.

## Ishlash natijasi:
```text
10 30 40 
```

---

# 606-Topshiriq: std::multiset asoslari

## Topshiriq sharti:
Takroriy elementlarni o'z ichiga oluvchi tartiblangan `std::multiset` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>

int main() {
    std::multiset<int> ms = {5, 2, 5, 8, 2, 5};
    for (int x : ms) std::cout << x << " ";
    std::cout << "\n5 raqami soni: " << ms.count(5) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::multiset` barcha takrorlangan elementlarni saralangan holda saqlaydi.

## Ishlash natijasi:
```text
2 2 5 5 5 8 \n5 raqami soni: 3
```

---

# 607-Topshiriq: multiset::equal_range

## Topshiriq sharti:
Bir xil qiymatga ega barcha elementlar oralig'ini `equal_range` orqali oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>

int main() {
    std::multiset<int> ms = {10, 20, 20, 20, 30};
    auto [bosh, oxir] = ms.equal_range(20);
    std::cout << "20 lar guruhi: ";
    for (auto it = bosh; it != oxir; ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `equal_range` birinchi va oxirgi mos elementlar iteratorlari juftligini (`std::pair`) qaytaradi.

## Ishlash natijasi:
```text
20 lar guruhi: 20 20 20 
```

---

# 608-Topshiriq: std::map (Lug'at / Kalit-qiymat) asoslari

## Topshiriq sharti:
Kalit bo'yicha qiymat saqlovchi va kalitlari saralangan `std::map` yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> narxlar;
    narxlar["non"] = 3000;
    narxlar["choy"] = 5000;
    narxlar["gosht"] = 90000;
    for (const auto& [mahsulot, narx] : narxlar) {
        std::cout << mahsulot << ": " << narx << " so'm\n";
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::map` kalitlarni alfavit tartibida saqlaydi va O(log N) qidiruv beradi.

## Ishlash natijasi:
```text
choy: 5000 so'm\ngosht: 90000 so'm\nnon: 3000 so'm
```

---

# 609-Topshiriq: std::map: insert va emplace

## Topshiriq sharti:
`insert` va `emplace` yordamida juftliklarni map ga kiritish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<int, std::string> xodimlar;
    xodimlar.insert({101, "Akmal"});
    xodimlar.emplace(102, "Nodira");
    std::cout << "101: " << xodimlar[101] << ", 102: " << xodimlar[102] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `emplace` to'g'ridan-to'g'ri map ichida `std::pair` quradi.

## Ishlash natijasi:
```text
101: Akmal, 102: Nodira
```

---

# 610-Topshiriq: std::map da operator[] tuzog'i

## Topshiriq sharti:
Nima uchun faqat qidirish uchun `[]` emas, balki `.find()` ishlatilishi kerakligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> hisob;
    // hisob["mavjudEmas"]; // Tuzoq! Kalit yo'q bo'lsa avtomatik 0 qiymati bilan kiritib qo'yadi!
    std::cout << "Boshida hajm: " << hisob.size() << std::endl;
    int x = hisob["test"];
    std::cout << "operator[] chaqirilgach hajm: " << hisob.size() << ", qiymat: " << x << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `operator[]` topilmagan kalitni standart qiymat bilan map ga qo'shib qo'yadi. Xavfsiz o'qish uchun `.find()` yoki `.at()` ishlatiladi.

## Ishlash natijasi:
```text
Boshida hajm: 0\noperator[] chaqirilgach hajm: 1, qiymat: 0
```

---

# 611-Topshiriq: std::map da xavfsiz qidirish: find va at

## Topshiriq sharti:
Mavjud bo'lmagan kalitda istisno tashlovchi `.at()` va xavfsiz `.find()` ni qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> ballar = {{"Ali", 90}};
    auto it = ballar.find("Vali");
    if (it == ballar.end()) {
        std::cout << "Vali topilmadi (map hajmi o'zgarmadi: " << ballar.size() << ")" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.find()` yangi element qo'shmaydi va to'liq xavfsizdir.

## Ishlash natijasi:
```text
Vali topilmadi (map hajmi o'zgarmadi: 1)
```

---

# 612-Topshiriq: std::multimap asoslari

## Topshiriq sharti:
Bitta kalit ostida bir nechta qiymat saqlovchi `std::multimap` ni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::multimap<std::string, std::string> shaharAholisi;
    shaharAholisi.insert({"Toshkent", "Farhod"});
    shaharAholisi.insert({"Toshkent", "Malika"});
    shaharAholisi.insert({"Samarqand", "Sherzod"});

    auto [bosh, oxir] = shaharAholisi.equal_range("Toshkent");
    std::cout << "Toshkentliklar: ";
    for (auto it = bosh; it != oxir; ++it) {
        std::cout << it->second << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `multimap` bir kalitga bir nechta obyektni bog'lash imkonini beradi.

## Ishlash natijasi:
```text
Toshkentliklar: Farhod Malika 
```

---

# 613-Topshiriq: std::unordered_set asoslari (Hash Table)

## Topshiriq sharti:
O'rtacha O(1) qidiruv tezligiga ega bo'lgan `std::unordered_set` dan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <unordered_set>

int main() {
    std::unordered_set<int> us = {45, 12, 89, 3, 24};
    us.insert(99);
    if (us.find(89) != us.end()) {
        std::cout << "89 soni O(1) tezlikda topildi!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::unordered_set` xesh-jadval asosida ishlaydi va tartibni kafolatlamaydi.

## Ishlash natijasi:
```text
89 soni O(1) tezlikda topildi!
```

---

# 614-Topshiriq: std::unordered_map asoslari

## Topshiriq sharti:
Super tezkor kalit-qiymat xaritasi `std::unordered_map` ni ishlating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <unordered_map>
#include <string>

int main() {
    std::unordered_map<std::string, double> gpa;
    gpa["Aziz"] = 4.8;
    gpa["Bekzod"] = 4.2;
    std::cout << "Aziz GPA: " << gpa["Aziz"] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta hajmdagi ma'lumotlar bazasida kalit bo'yicha qidirish uchun eng samarali konteyner.

## Ishlash natijasi:
```text
Aziz GPA: 4.8
```

---

# 615-Topshiriq: Xesh to'qnashuvlari va chelaklar (Buckets & Load Factor)

## Topshiriq sharti:
Xesh-jadvalning ichki chelaklar soni va to'lish koeffitsiyentini o'rganing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<int, int> um;
    for (int i = 0; i < 10; ++i) um[i] = i * i;
    std::cout << "Chelaklar soni (bucket_count): " << um.bucket_count() << std::endl;
    std::cout << "To'lish koeffitsiyenti (load_factor): " << um.load_factor() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `load_factor` ko'tarilganda xesh-jadval avtomatik rehash qilib chelaklar sonini oshiradi.

## Ishlash natijasi:
```text
Chelaklar soni (bucket_count): ...\nTo'lish koeffitsiyenti (load_factor): ...
```

---

# 616-Topshiriq: rehash() va reserve() orqali unumdorlikni oshirish

## Topshiriq sharti:
Ko'p element kiritishdan oldin chelaklarni oldindan tayyorlab to'qnashuvlarni kamaytiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <unordered_set>

int main() {
    std::unordered_set<int> us;
    us.reserve(1000); // 1000 ta element uchun joy tayyorlash
    std::cout << "Chelaklar soni: " << us.bucket_count() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oldindan `reserve()` qilish qayta xeshlash (rehashing) to'xtalishlarini bartaraf etadi.

## Ishlash natijasi:
```text
Chelaklar soni: ...
```

---

# 617-Topshiriq: Maxsus sinf uchun std::hash ixtisoslashuvi

## Topshiriq sharti:
O'zimizning `Nuqta` sinfimizni `std::unordered_set` da saqlash uchun xesh funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <unordered_set>

struct Nuqta {
    int x, y;
    bool operator==(const Nuqta& o) const { return x == o.x && y == o.y; }
};

namespace std {
    template <>
    struct hash<Nuqta> {
        size_t operator()(const Nuqta& n) const {
            return hash<int>()(n.x) ^ (hash<int>()(n.y) << 1);
        }
    };
}

int main() {
    std::unordered_set<Nuqta> nuqtalar;
    nuqtalar.insert({1, 2});
    std::cout << "Nuqtalar soni: " << nuqtalar.size() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xesh-jadvalda maxsus obyekt saqlash uchun `operator==` va `std::hash` talab qilinadi.

## Ishlash natijasi:
```text
Nuqtalar soni: 1
```

---

# 618-Topshiriq: Kamayish tartibida saralangan std::set

## Topshiriq sharti:
Standart `std::less` o'rniga `std::greater` berib, to'plamni teskari tartibda saqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>
#include <functional>

int main() {
    std::set<int, std::greater<int>> kamayuvchi = {10, 50, 20, 40};
    for (int x : kamayuvchi) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikkinchi shablon parametri komparator bo'lib, daraxtdagi tartibni boshqaradi.

## Ishlash natijasi:
```text
50 40 20 10 
```

---

# 619-Topshiriq: lower_bound va upper_bound metodlari

## Topshiriq sharti:
`map` da berilgan qiymatdan kichik bo'lmagan birinchi elementni O(log N) da toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>

int main() {
    std::map<int, std::string> m = {{10, "A"}, {20, "B"}, {30, "C"}};
    auto it = m.lower_bound(15); // 20 ga ko'rsatadi
    std::cout << "lower_bound(15): " << it->first << " -> " << it->second << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `lower_bound` kalitdan katta yoki teng bo'lgan birinchi elementni qaytaradi.

## Ishlash natijasi:
```text
lower_bound(15): 20 -> B
```

---

# 620-Topshiriq: std::stack (Stek adapteri - LIFO)

## Topshiriq sharti:
Oxirgi kirgan birinchi chiqadigan `std::stack` adapteridan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stack>

int main() {
    std::stack<int> st;
    st.push(1);
    st.push(2);
    st.push(3);
    while (!st.empty()) {
        std::cout << st.top() << " ";
        st.pop();
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::stack` sukut bo'yicha `std::deque` ustiga qurilgan va LIFO tartibini ta'minlaydi.

## Ishlash natijasi:
```text
3 2 1 
```

---

# 621-Topshiriq: Qavslar balansini tekshirish masalasi (Stack)

## Topshiriq sharti:
Satrdagi qavslar `()[]{}` to'g'ri ochilib yopilganini stek yordamida tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stack>
#include <string>

bool qavslarTogrimi(const std::string& s) {
    std::stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') st.push(c);
        else {
            if (st.empty()) return false;
            char top = st.top(); st.pop();
            if ((c == ')' && top != '(') || (c == ']' && top != '[') || (c == '}' && top != '{'))
                return false;
        }
    }
    return st.empty();
}

int main() {
    std::cout << "({[]}) to'g'rimi: " << (qavslarTogrimi("({[]})") ? "Ha" : "Yo'q") << std::endl;
    std::cout << "([)] to'g'rimi: " << (qavslarTogrimi("([)]") ? "Ha" : "Yo'q") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Stekning eng mashhur va klassik amaliy masalalaridan biri.

## Ishlash natijasi:
```text
({[]}) to'g'rimi: Ha\n([)] to'g'rimi: Yo'q
```

---

# 622-Topshiriq: std::queue (Navbat adapteri - FIFO)

## Topshiriq sharti:
Birinchi kelgan birinchi xizmat ko'rsatiladigan `std::queue` ni ishlating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <queue>

int main() {
    std::queue<std::string> navbat;
    navbat.push("Mijoz 1");
    navbat.push("Mijoz 2");
    while (!navbat.empty()) {
        std::cout << navbat.front() << " xizmat oldi\n";
        navbat.pop();
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `front()` birinchi elementni ko'rsatadi, `pop()` esa uni navbatdan chiqaradi.

## Ishlash natijasi:
```text
Mijoz 1 xizmat oldi\nMijoz 2 xizmat oldi
```

---

# 623-Topshiriq: std::priority_queue (Ustuvorlik navbati / Max-Heap)

## Topshiriq sharti:
Elementlar har doim eng kattasi tepada turadigan navbatni boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <queue>

int main() {
    std::priority_queue<int> pq;
    pq.push(30);
    pq.push(100);
    pq.push(50);
    while (!pq.empty()) {
        std::cout << pq.top() << " ";
        pq.pop();
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::priority_queue` binar uyum (Binary Heap) asosida O(log N) da saralab boradi.

## Ishlash natijasi:
```text
100 50 30 
```

---

# 624-Topshiriq: Min-Heap yaratish (std::greater bilan)

## Topshiriq sharti:
Eng kichik element har doim birinchi chiqadigan Min-Heap hosil qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <queue>
#include <vector>

int main() {
    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;
    minHeap.push(45);
    minHeap.push(10);
    minHeap.push(30);
    std::cout << "Eng kichigi: " << minHeap.top() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::greater<int>` komparatori uyumni Min-Heap ga aylantiradi.

## Ishlash natijasi:
```text
Eng kichigi: 10
```

---

# 625-Topshiriq: Top-K eng katta elementlarni topish (Min-Heap usuli)

## Topshiriq sharti:
Katta oqim ichidan eng katta 3 ta sonni O(N log K) vaqtda toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <queue>
#include <vector>

int main() {
    std::vector<int> sonlar = {12, 3, 5, 7, 19, 2, 45, 89, 21};
    int k = 3;
    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;
    for (int x : sonlar) {
        minHeap.push(x);
        if (minHeap.size() > (size_t)k) minHeap.pop();
    }
    std::cout << "Top 3: ";
    while (!minHeap.empty()) {
        std::cout << minHeap.top() << " ";
        minHeap.pop();
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. K o'lchamli Min-Heap faqat eng katta K ta elementni saqlab qoladi.

## Ishlash natijasi:
```text
Top 3: 21 45 89 
```

---

# 626-Topshiriq: Matndagi so'zlar chastotasini hisoblash (Word Frequency)

## Topshiriq sharti:
Matndagi har bir so'z necha marta qatnashganini `std::unordered_map` bilan sanang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <unordered_map>
#include <sstream>
#include <string>

int main() {
    std::string matn = "ai model kelajak model ai ai dastur";
    std::stringstream ss(matn);
    std::string soz;
    std::unordered_map<std::string, int> chastota;
    while (ss >> soz) {
        chastota[soz]++;
    }
    std::cout << "'ai' so'zi: " << chastota["ai"] << " marta\n";
    std::cout << "'model' so'zi: " << chastota["model"] << " marta\n";
    return 0;
}
```

## Tushuntirish va Mantiq:
1. NLP va matn tahlilining eng asosiy poydevori.

## Ishlash natijasi:
```text
'ai' so'zi: 3 marta\n'model' so'zi: 2 marta
```

---

# 627-Topshiriq: Ikki to'plam kesishmasi (Set Intersection)

## Topshiriq sharti:
Ikkita `std::set` dagi umumiy elementlarni `std::set_intersection` orqali toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>
#include <vector>
#include <algorithm>

int main() {
    std::set<int> s1 = {1, 2, 3, 4, 5};
    std::set<int> s2 = {3, 4, 5, 6, 7};
    std::vector<int> kesishma;
    std::set_intersection(s1.begin(), s1.end(), s2.begin(), s2.end(),
                          std::back_inserter(kesishma));
    for (int x : kesishma) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Saralangan to'plamlar ustida matematik amallar O(N + M) vaqtda bajariladi.

## Ishlash natijasi:
```text
3 4 5 
```

---

# 628-Topshiriq: Ikki to'plam birlashmasi (Set Union)

## Topshiriq sharti:
Ikki to'plamni birlashtirib barcha elementlarni bir marta oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>
#include <vector>
#include <algorithm>

int main() {
    std::set<int> s1 = {1, 2, 3};
    std::set<int> s2 = {3, 4, 5};
    std::vector<int> birlashma;
    std::set_union(s1.begin(), s1.end(), s2.begin(), s2.end(),
                   std::back_inserter(birlashma));
    for (int x : birlashma) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Takrorlanishlarsiz yaxlit birlashma to'plami olinadi.

## Ishlash natijasi:
```text
1 2 3 4 5 
```

---

# 629-Topshiriq: Ikki to'plam ayirmasi (Set Difference)

## Topshiriq sharti:
Birinchi to'plamda bor, ikkinchisida yo'q elementlarni ajrating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>
#include <vector>
#include <algorithm>

int main() {
    std::set<int> s1 = {1, 2, 3, 4};
    std::set<int> s2 = {3, 4, 5};
    std::vector<int> ayirma;
    std::set_difference(s1.begin(), s1.end(), s2.begin(), s2.end(),
                        std::back_inserter(ayirma));
    for (int x : ayirma) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Birinchi to'plamdan ikkinchi to'plam elementlari ayirib tashlanadi.

## Ishlash natijasi:
```text
1 2 
```

---

# 630-Topshiriq: std::bitset asoslari

## Topshiriq sharti:
Qat'iy o'lchamdagi 8-bitli `std::bitset` yarating va bit amallarini bajaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <bitset>

int main() {
    std::bitset<8> b(0b00001010);
    std::cout << "Boshlang'ich: " << b << std::endl;
    b.set(0);  // 0-bitni 1 qilish
    b.flip(1); // 1-bitni teskari qilish
    std::cout << "O'zgargan:     " << b << std::endl;
    std::cout << "1 lar soni:    " << b.count() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::bitset` xotirani nihoyatda tejaydi va apparat darajasidagi tezlik beradi.

## Ishlash natijasi:
```text
Boshlang'ich: 00001010\nO'zgargan:     00001001\n1 lar soni:    2
```

---

# 631-Topshiriq: Eratosfen g'alviri bitset orqali (Super tezkor tub sonlar)

## Topshiriq sharti:
`std::bitset` orqali 100 gacha bo'lgan barcha tub sonlarni xotira sarflamay toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <bitset>

int main() {
    const int N = 100;
    std::bitset<N + 1> tub;
    tub.set(); // Barchasi 1
    tub[0] = tub[1] = 0;
    for (int p = 2; p * p <= N; ++p) {
        if (tub[p]) {
            for (int i = p * p; i <= N; i += p) tub[i] = 0;
        }
    }
    std::cout << "50 gacha tub sonlar: ";
    for (int i = 2; i <= 50; ++i) {
        if (tub[i]) std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitset orqali hatto 1 milliardlik oraliqni ham megabaytlar xotirada tezkor g'alvirlash mumkin.

## Ishlash natijasi:
```text
50 gacha tub sonlar: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 
```

---

# 632-Topshiriq: C++17 try_emplace metodi

## Topshiriq sharti:
`map` da kalit allaqachon mavjud bo'lsa yangi obyekt qurilishining oldini oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, std::string> sozlamalar;
    sozlamalar["til"] = "Uzbek";
    sozlamalar.try_emplace("til", "English"); // O'zgarmaydi!
    std::cout << "Til: " << sozlamalar["til"] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `try_emplace` kalit bo'lsa hech qanday argumentni ko'chirmaydi va konstruktorni chaqirmaydi.

## Ishlash natijasi:
```text
Til: Uzbek
```

---

# 633-Topshiriq: C++17 insert_or_assign

## Topshiriq sharti:
Mavjud bo'lsa yangilang, yo'q bo'lsa kirituvchi C++17 metodini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> ballar;
    ballar.insert_or_assign("Akmal", 85);
    ballar.insert_or_assign("Akmal", 95); // Yangilandi
    std::cout << "Akmal balli: " << ballar["Akmal"] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `insert_or_assign` operator `[]` ning to'liq xavfsiz va aniq alternatividir.

## Ishlash natijasi:
```text
Akmal balli: 95
```

---

# 634-Topshiriq: C++17 node extraction (.extract())

## Topshiriq sharti:
Daraxt yoki xesh jadvaldan tugunni (node) xotirasini qayta allokatsiya qilmasdan sug'urib oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>

int main() {
    std::set<int> s = {10, 20, 30};
    auto node = s.extract(20); // 20 tuguni ajratildi
    node.value() = 25;         // Kaliti o'zgartirildi
    s.insert(std::move(node)); // Qayta kiritildi xotira sarflamasdan
    for (int x : s) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `extract` orqali `std::set` dagi o'zgarmas elementlarni qayta ajratmasdan tahrirlash mumkin.

## Ishlash natijasi:
```text
10 25 30 
```

---

# 635-Topshiriq: C++17 map::merge metodi

## Topshiriq sharti:
Bitta map dagi elementlarni ikkinchisiga xotira nusxalamasdan O(N log N) da ulab oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>

int main() {
    std::map<int, char> m1 = {{1, 'a'}, {2, 'b'}};
    std::map<int, char> m2 = {{3, 'c'}, {4, 'd'}};
    m1.merge(m2);
    for (const auto& [k, v] : m1) std::cout << k << ":" << v << " ";
    std::cout << "| m2 hajmi: " << m2.size() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.merge()` xotirani qayta allokatsiya qilmasdan tugunlar ko'rsatkichlarini ko'chiradi.

## Ishlash natijasi:
```text
1:a 2:b 3:c 4:d | m2 hajmi: 0
```

---

# 636-Topshiriq: Dijkstra qisqa yo'l algoritmi uchun Priority Queue

## Topshiriq sharti:
Grafdagi eng qisqa yo'llarni topish uchun Min-Heap ni qo'llash skeleti.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <queue>
#include <vector>

typedef std::pair<int, int> pii; // (masofa, cho'qqi)

int main() {
    std::priority_queue<pii, std::vector<pii>, std::greater<pii>> pq;
    pq.push({0, 1}); // 1-cho'qqi masofasi 0
    pq.push({10, 2});
    pq.push({3, 3});
    auto [masofa, choqqi] = pq.top();
    std::cout << "Eng yaqin cho'qqi: " << choqqi << " (masofa: " << masofa << ")" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Min-Heap orqali eng yaqin cho'qqi doimo O(log V) da olinadi.

## Ishlash natijasi:
```text
Eng yaqin cho'qqi: 1 (masofa: 0)
```

---

# 637-Topshiriq: Qo'shimcha konteyner adapteri: stack ostiga vector qo'yish

## Topshiriq sharti:
`std::stack` ning ichki konteynerini `std::vector` ga almashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stack>
#include <vector>

int main() {
    std::stack<int, std::vector<int>> st;
    st.push(77);
    st.push(88);
    std::cout << "Top: " << st.top() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikkinchi shablon parametri orqali adapter ostidagi konteyner o'zgartiriladi.

## Ishlash natijasi:
```text
Top: 88
```

---

# 638-Topshiriq: Teskari tartibli map: map<int, string, greater<int>>

## Topshiriq sharti:
Kalitlari kamayish tartibida joylashuvchi map dan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<int, std::string, std::greater<int>> reyting;
    reyting[100] = "Oltin";
    reyting[80] = "Kumush";
    reyting[60] = "Bronza";
    for (const auto& [ball, unvon] : reyting) {
        std::cout << ball << " -> " << unvon << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Eng yuqori ball birinchi o'rinda turadi.

## Ishlash natijasi:
```text
100 -> Oltin 80 -> Kumush 60 -> Bronza 
```

---

# 639-Topshiriq: Custom Comparator orqali map da obyektlarni saralash

## Topshiriq sharti:
O'zimiz yozgan solishtiruvchi struktura bilan map kalitlarini boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <string>

struct UzunlikBoyicha {
    bool operator()(const std::string& a, const std::string& b) const {
        return a.length() < b.length();
    }
};

int main() {
    std::map<std::string, int, UzunlikBoyicha> m;
    m["A"] = 1;
    m["AAA"] = 3;
    m["AA"] = 2;
    for (const auto& [k, v] : m) std::cout << k << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Satrlar harflari bo'yicha emas, uzunligi bo'yicha tartiblanadi.

## Ishlash natijasi:
```text
A AA AAA 
```

---

# 640-Topshiriq: Hash-DoS hujumlari va maxsus xesh funksiyasi

## Topshiriq sharti:
Nima uchun raqiblar bir xil xesh qiymatli so'rovlar yuborib O(N^2) ga tushirishi va undan himoyalanishni tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Hash-DoS - ko'plab to'qnashuvlar sun'iy hosil qilinib serverni qotirib qo'yish. "
              << "Himoya: tasodifiy tuz (random seed) qo'shilgan custom hash funksiyalari." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompetitiv dasturlash va serverlarda xavfsiz xesh algoritmlari (masalan splitmix64) qo'llanadi.

## Ishlash natijasi:
```text
Hash-DoS - ko'plab to'qnashuvlar sun'iy hosil qilinib serverni qotirib qo'yish. Himoya: tasodifiy tuz (random seed) qo'shilgan custom hash funksiyalari.
```

---

# 641-Topshiriq: O'zaro bog'liq ma'lumotlar bazasi (Relational table analogi)

## Topshiriq sharti:
`map<int, vector<string>>` orqali guruhlar va ularning talabalari ro'yxatini yuring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <vector>
#include <string>

int main() {
    std::map<int, std::vector<std::string>> guruhlar;
    guruhlar[101].push_back("Ali");
    guruhlar[101].push_back("Vali");
    guruhlar[102].push_back("Sami");

    for (const auto& [guruh, talabalar] : guruhlar) {
        std::cout << "Guruh " << guruh << ": ";
        for (const auto& t : talabalar) std::cout << t << " ";
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bir-ko'pga (One-to-Many) munosabatlarini modellashtirish.

## Ishlash natijasi:
```text
Guruh 101: Ali Vali \nGuruh 102: Sami 
```

---

# 642-Topshiriq: Navbat orqali Kenglik bo'yicha qidiruv (BFS) skeleti

## Topshiriq sharti:
`std::queue` yordamida daraxt yoki grafni qavatma-qavat aylanib chiqish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <queue>
#include <vector>

int main() {
    std::queue<int> q;
    q.push(1); // Ildiz
    std::cout << "BFS ketma-ketligi: ";
    while (!q.empty()) {
        int joriy = q.front(); q.pop();
        std::cout << joriy << " ";
        if (joriy == 1) { q.push(2); q.push(3); }
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. FIFO xossasi tufayli `std::queue` BFS algoritmining tayanchi hisoblanadi.

## Ishlash natijasi:
```text
BFS ketma-ketligi: 1 2 3 
```

---

# 643-Topshiriq: Priority Queue da maxsus struct elementlarini boshqarish

## Topshiriq sharti:
Vazifa muhimligiga qarab birinchi bajariluvchi Job Scheduler yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <queue>
#include <string>

struct Vazifa {
    int ustuvorlik;
    std::string nom;
    bool operator<(const Vazifa& b) const { return ustuvorlik < b.ustuvorlik; }
};

int main() {
    std::priority_queue<Vazifa> reja;
    reja.push({1, "Elektron xat yozish"});
    reja.push({10, "Server halokatini tuzatish"});
    reja.push({5, "Hisobot tayyorlash"});

    std::cout << "Birinchi bajariladi: " << reja.top().nom << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Eng yuqori ustuvorlikka ega vazifa birinchi bo'lib bajariladi.

## Ishlash natijasi:
```text
Birinchi bajariladi: Server halokatini tuzatish
```

---

# 644-Topshiriq: Bitset yordamida tezkor to'plamlar amallari

## Topshiriq sharti:
Bitsetlar orqali ikkita to'plamning birlashma va kesishmasini bitta protsessor ko'rsatmasida bajaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <bitset>

int main() {
    std::bitset<4> A(0b1100);
    std::bitset<4> B(0b1010);
    std::cout << "A AND B: " << (A & B) << std::endl;
    std::cout << "A OR B:  " << (A | B) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bit darajasidagi amallar zamonaviy protsessorlarda 1 takt davomida hisoblanadi.

## Ishlash natijasi:
```text
A AND B: 1000\nA OR B:  1110
```

---

# 645-Topshiriq: std::set orqali saralangan noyob massiv hosil qilish

## Topshiriq sharti:
Tartibsiz massivdan takrorlarni olib tashlab, saralab vektorga qaytaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <set>
#include <vector>

int main() {
    std::vector<int> xom = {7, 2, 9, 2, 7, 1, 5};
    std::set<int> saralangan(xom.begin(), xom.end());
    for (int x : saralangan) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bir qatorda nusxalash orqali to'liq saralangan va noyob to'plam olinadi.

## Ishlash natijasi:
```text
1 2 5 7 9 
```

---

# 646-Topshiriq: std::map orqali konfiguratsiya faylini xotirada saqlash

## Topshiriq sharti:
Kalit-qiymat ko'rinishidagi sozlamalar jadvalini boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, std::string> config = {
        {"model_path", "weights/bitnet_10b.bin"},
        {"quantization", "1-bit"},
        {"device", "cuda"}
    };
    std::cout << "Model: " << config["model_path"] 
              << ", Kvantlash: " << config["quantization"] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. AI modellari konfiguratsiyasini boshqarishning standart usuli.

## Ishlash natijasi:
```text
Model: weights/bitnet_10b.bin, Kvantlash: 1-bit
```

---

# 647-Topshiriq: Stack orqali teskari polyak yozuvi (RPN Kalkulyator)

## Topshiriq sharti:
`std::stack` orqali postfiks arifmetik ifodani ('5 3 + 2 *') hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stack>
#include <sstream>

int hisoblaRPN(const std::string& exp) {
    std::stack<int> st;
    std::stringstream ss(exp);
    std::string token;
    while (ss >> token) {
        if (token == "+" || token == "*") {
            int b = st.top(); st.pop();
            int a = st.top(); st.pop();
            st.push((token == "+") ? (a + b) : (a * b));
        } else {
            st.push(std::stoi(token));
        }
    }
    return st.top();
}

int main() {
    std::cout << "5 3 + 2 * natijasi: " << hisoblaRPN("5 3 + 2 *") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. (5 + 3) * 2 = 16. Stek orqali kompyuter arifmetikasi bajarilishi.

## Ishlash natijasi:
```text
5 3 + 2 * natijasi: 16
```

---

# 648-Topshiriq: Konteyner adapterlarida iteratorlar yo'qligi

## Topshiriq sharti:
Nima uchun `stack` va `queue` da `begin()` va `end()` metodlari yo'qligini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Adapterlar ma'lumotlar tuzilmasi qoidalarini (faqat tepadan olish yoki faqat navbat bo'yicha) "
              << "qat'iy himoyalash uchun iteratorlarni atayin yashiradi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar iteratorlar ochiq bo'lsa, stekning o'rtasidagi element o'zgartirilib, uning ma'nosi buzilar edi.

## Ishlash natijasi:
```text
Adapterlar ma'lumotlar tuzilmasi qoidalarini (faqat tepadan olish yoki faqat navbat bo'yicha) qat'iy himoyalash uchun iteratorlarni atayin yashiradi.
```

---

# 649-Topshiriq: std::unordered_map orqali Fibonachchi Memoizatsiyasi

## Topshiriq sharti:
Kesh (memoization) orqali O(2^N) rekursiyani O(N) chiziqli vaqtga tushiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <unordered_map>

std::unordered_map<int, long long> kesh;

long long fibMemo(int n) {
    if (n <= 1) return n;
    if (kesh.contains(n)) return kesh[n];
    return kesh[n] = fibMemo(n - 1) + fibMemo(n - 2);
}

int main() {
    std::cout << "Fib(50) = " << fibMemo(50) << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Memoizatsiya xesh-jadval orqali hisoblangan natijalarni saqlab, takroriy hisoblashlarni nolga tushiradi.

## Ishlash natijasi:
```text
Fib(50) = 12586269025
```

---

# 650-Topshiriq: 13-qism xulosasi: Assotsiativ Konteynerlar Strategiyasi

## Topshiriq sharti:
Unordered konteynerlar - O(1) o'rtacha qidiruv uchun, Ordered konteynerlar - doimiy saralangan ma'lumotlar uchun, Priority Queue esa oqimda eng kattasini nazorat qilish uchun eng oliy yechimdir.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Assotsiativ konteynerlar va adapterlar o'zlashtirildi: Algoritmlar endi O(1) va O(log N) da ishlaydi!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Murakkab tizimlar va ma'lumotlar bazalarining poydevori shu konteynerlar ustida quriladi.

## Ishlash natijasi:
```text
Assotsiativ konteynerlar va adapterlar o'zlashtirildi: Algoritmlar endi O(1) va O(log N) da ishlaydi!
```

---

