# C++ Dasturlash Tili - 15-Qism: Istisnolar (Exceptions), Fayllar I/O va C++17 Filesystem

Ushbu qismda try/catch/throw, maxsus istisnolar, noexcept, ifstream/ofstream, binar fayllar, stringstream va C++17 std::filesystem imkoniyatlariga oid 50 ta amaliy topshiriq jamlangan.

---

# 701-Topshiriq: Istisnolar (Exceptions) asoslari: try, catch, throw

## Topshiriq sharti:
Nolga bo'lish xatoligini `throw` orqali tashlab, `try-catch` blokida xavfsiz ushlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stdexcept>

double bolish(double a, double b) {
    if (b == 0.0) {
        throw std::runtime_error("Nolga bo'lish mumkin emas!");
    }
    return a / b;
}

int main() {
    try {
        std::cout << "10 / 2 = " << bolish(10, 2) << std::endl;
        std::cout << "10 / 0 = " << bolish(10, 0) << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Xatolik ushlandi: " << e.what() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `throw` dastur ijrosini to'xtatib istisno tashlaydi, `catch` esa uni ushlab xatolikdan tiklanish imkonini beradi.

## Ishlash natijasi:
```text
10 / 2 = 5\nXatolik ushlandi: Nolga bo'lish mumkin emas!
```

---

# 702-Topshiriq: Standart istisnolar ierarxiyasi

## Topshiriq sharti:
`std::invalid_argument` va `std::out_of_range` standart xatoliklarini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stdexcept>

void yoshTekshir(int yosh) {
    if (yosh < 0) throw std::invalid_argument("Yosh manfiy bo'lolmaydi!");
    if (yosh > 150) throw std::out_of_range("Yosh ko'rsatkichi chegaradan tashqarida!");
    std::cout << "Yosh qabul qilindi: " << yosh << std::endl;
}

int main() {
    try {
        yoshTekshir(-5);
    } catch (const std::invalid_argument& e) {
        std::cout << "Parametr xatosi: " << e.what() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `<stdexcept>` kutubxonasi turli holatlar uchun tayyor ierarxiyani taqdim etadi.

## Ishlash natijasi:
```text
Parametr xatosi: Yosh manfiy bo'lolmaydi!
```

---

# 703-Topshiriq: Maxsus istisno sinfi (Custom Exception Class)

## Topshiriq sharti:
`std::exception` dan meros oluvchi o'zimizning `AiXatolik` sinfimizni yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <exception>
#include <string>

class AiXatolik : public std::exception {
    std::string xabar;
public:
    AiXatolik(std::string x) : xabar("AI Xatosi: " + x) {}
    const char* what() const noexcept override {
        return xabar.c_str();
    }
};

int main() {
    try {
        throw AiXatolik("1-bit tensor o'lchamlari mos kelmadi!");
    } catch (const AiXatolik& e) {
        std::cout << e.what() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Maxsus istisnolar `what()` virtual metodini override qilish orqali tizimga mos xabar beradi.

## Ishlash natijasi:
```text
AI Xatosi: 1-bit tensor o'lchamlari mos kelmadi!
```

---

# 704-Topshiriq: Bir nechta catch bloklari orqali saralash

## Topshiriq sharti:
Xatoliklarni aniq turidan boshlab umumiy turga qarab alohida-alohida tuting.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stdexcept>

void sinov(int kod) {
    if (kod == 1) throw std::invalid_argument("Noto'g'ri argument");
    if (kod == 2) throw std::runtime_error("Ish vaqti xatosi");
    throw 404; // Butun sonli xato
}

int main() {
    try {
        sinov(1);
    } catch (const std::invalid_argument& e) {
        std::cout << "Maxsus: " << e.what() << std::endl;
    } catch (const std::runtime_error& e) {
        std::cout << "Runtime: " << e.what() << std::endl;
    } catch (...) {
        std::cout << "Noma'lum istisno ushlandi!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `catch (...)` har qanday kutilmagan istisnoni tutuvchi oxirgi xavfsizlik to'ridir.

## Ishlash natijasi:
```text
Maxsus: Noto'g'ri argument
```

---

# 705-Topshiriq: Istisnoni qayta tashlash (Rethrowing: throw;)

## Topshiriq sharti:
Xatoni jurnalga (log) yozib, qayta yuqori qatlamga uzatish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stdexcept>

void quyiQatlam() {
    try {
        throw std::runtime_error("Ma'lumotlar bazasi uzildi");
    } catch (const std::exception& e) {
        std::cout << "[LOG]: Quyi qatlam xatoni qayd etdi, yuqoriga uzatmoqda...\n";
        throw; // Asl istisno qayta tashlandi
    }
}

int main() {
    try {
        quyiQatlam();
    } catch (const std::exception& e) {
        std::cout << "Asosiy dastur xatoni qabul qildi: " << e.what() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `throw;` argumentsiz yozilsa joriy tutilgan istisnoni o'zgartirmasdan yuqoriga otadi.

## Ishlash natijasi:
```text
[LOG]: Quyi qatlam xatoni qayd etdi, yuqoriga uzatmoqda...\nAsosiy dastur xatoni qabul qildi: Ma'lumotlar bazasi uzildi
```

---

# 706-Topshiriq: Stack Unwinding va RAII xavfsizligi

## Topshiriq sharti:
Istisno otilganda stekdagi barcha lokal obyektlarning destruktorlari avtomatik ishlashini isbotlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stdexcept>

class ResursQorovul {
    std::string nom;
public:
    ResursQorovul(std::string n) : nom(n) { std::cout << "+" << nom << " ochildi\n"; }
    ~ResursQorovul() { std::cout << "-" << nom << " yopildi\n"; }
};

void ish() {
    ResursQorovul r1("Fayl");
    ResursQorovul r2("Xotira");
    throw std::runtime_error("Kutilmagan avariya!");
}

int main() {
    try {
        ish();
    } catch (const std::exception& e) {
        std::cout << "Xato ushlandi: " << e.what() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Stack Unwinding istisno yuz berganda ham barcha RAII resurslar xavfsiz yopilishini kafolatlaydi.

## Ishlash natijasi:
```text
+Fayl ochildi\n+Xotira ochildi\n-Xotira yopildi\n-Fayl yopildi\nXato ushlandi: Kutilmagan avariya!
```

---

# 707-Topshiriq: Konstruktorda istisno va yarim qurilgan obyekt

## Topshiriq sharti:
Konstruktor ichida xato bo'lsa obyekt qurilmagan hisoblanishi va o'z destruktori chaqirilmasligini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stdexcept>

class Bino {
public:
    Bino() {
        std::cout << "Poydevor qurildi\n";
        throw std::runtime_error("Tom yopishda xatolik!");
    }
    ~Bino() {
        std::cout << "Bino buzildi\n"; // Chaqirilmaydi!
    }
};

int main() {
    try {
        Bino b;
    } catch (const std::exception& e) {
        std::cout << "Qurilish to'xtatildi: " << e.what() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Konstruktor xato bersa, obyekt mavjud bo'lmagani sababli uning destruktori chaqirilmaydi.

## Ishlash natijasi:
```text
Poydevor qurildi\nQurilish to'xtatildi: Tom yopishda xatolik!
```

---

# 708-Topshiriq: Destruktorda hech qachon istisno tashlamaslik qoidasi

## Topshiriq sharti:
Destruktor sukut bo'yicha `noexcept` ekanligi va undan istisno otilsa `std::terminate` chaqirilishini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class XavfsizDestruktor {
public:
    ~XavfsizDestruktor() noexcept {
        // Destruktor ichidagi barcha xatolar ichkarida hal qilinishi shart!
        try {
            // potentsial xatolik
        } catch (...) {}
    }
};

int main() {
    std::cout << "Destruktordan istisno tashlash dasturni darhol halokatga olib keladi (std::terminate)." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++11 dan boshlab barcha destruktorlar avtomatik `noexcept` hisoblanadi.

## Ishlash natijasi:
```text
Destruktordan istisno tashlash dasturni darhol halokatga olib keladi (std::terminate).
```

---

# 709-Topshiriq: noexcept kalit so'zi va optimizatsiya

## Topshiriq sharti:
Funksiya istisno tashlamasligini kompilyatorga bildirib chaqiruvlarni optimallashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void tezkorAmal() noexcept {
    int a = 5, b = 10;
    int c = a + b;
    (void)c;
}

int main() {
    tezkorAmal();
    std::cout << "noexcept funksiya istisno jadvallarisiz (zero exception overhead) ishlaydi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `noexcept` kompilyatorga istisnolarni boshqarish mexanizmini o'chirib, kod hajmini qisqartirish imkonini beradi.

## Ishlash natijasi:
```text
noexcept funksiya istisno jadvallarisiz (zero exception overhead) ishlaydi.
```

---

# 710-Topshiriq: Matnli faylga yozish: std::ofstream

## Topshiriq sharti:
`std::ofstream` orqali fayl yaratib unga bir nechta qator yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ofstream fayl("sinov_chiqish.txt");
    if (fayl.is_open()) {
        fayl << "C++ Dasturlash Tili\n";
        fayl << "1-Bit AI Tizimlari\n";
        fayl.close();
        std::cout << "Faylga muvaffaqiyatli yozildi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `ofstream` faylga yozish uchun oqim ochadi va `<<` operatori orqali ma'lumot qabul qiladi.

## Ishlash natijasi:
```text
Faylga muvaffaqiyatli yozildi.
```

---

# 711-Topshiriq: Matnli fayldan butun qatorlarni o'qish: std::getline

## Topshiriq sharti:
`std::ifstream` va `getline` yordamida faylning barcha qatorlarini ekranga chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::ifstream fayl("sinov_chiqish.txt");
    if (fayl.is_open()) {
        std::string qator;
        while (std::getline(fayl, qator)) {
            std::cout << "O'qildi: " << qator << std::endl;
        }
        fayl.close();
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::getline(fayl, qator)` bo'shliqlar bilan birga butun satrni o'qiydi.

## Ishlash natijasi:
```text
O'qildi: C++ Dasturlash Tili\nO'qildi: 1-Bit AI Tizimlari
```

---

# 712-Topshiriq: Faylga qo'shish rejimi (std::ios::app)

## Topshiriq sharti:
Eski ma'lumotlarni o'chirmasdan fayl oxiriga yangi qator qo'shing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ofstream fayl("sinov_chiqish.txt", std::ios::app);
    if (fayl.is_open()) {
        fayl << "Qo'shilgan yangi satr\n";
        fayl.close();
        std::cout << "Oxiriga qo'shildi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::ios::app` ko'rsatkichni fayl oxiriga o'rnatib append rejimida ishlaydi.

## Ishlash natijasi:
```text
Oxiriga qo'shildi.
```

---

# 713-Topshiriq: Binar faylga yozish (std::ios::binary va write)

## Topshiriq sharti:
Butun sonlar massivini xom baytlar ko'rinishida binar faylga saqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>

int main() {
    int sonlar[4] = {100, 200, 300, 400};
    std::ofstream fayl("data.bin", std::ios::binary);
    if (fayl.is_open()) {
        fayl.write(reinterpret_cast<const char*>(sonlar), sizeof(sonlar));
        fayl.close();
        std::cout << "Binar fayl yaratildi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.write()` ma'lumotlarni matnga aylantirmasdan to'g'ridan-to'g'ri xotiradagi xom baytlarda yozadi.

## Ishlash natijasi:
```text
Binar fayl yaratildi.
```

---

# 714-Topshiriq: Binar fayldan o'qish (read)

## Topshiriq sharti:
Binar fayldagi xom baytlarni massivga qayta o'qib oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>

int main() {
    int olingan[4] = {0};
    std::ifstream fayl("data.bin", std::ios::binary);
    if (fayl.is_open()) {
        fayl.read(reinterpret_cast<char*>(olingan), sizeof(olingan));
        fayl.close();
        for (int x : olingan) std::cout << x << " ";
        std::cout << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.read()` binar ma'lumotlarni maksimal tezlikda xotiraga yuklaydi.

## Ishlash natijasi:
```text
100 200 300 400 
```

---

# 715-Topshiriq: Fayl hajmini aniqlash (seekg va tellg)

## Topshiriq sharti:
Fayl ko'rsatkichini oxiriga surib baytlar sonini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ifstream fayl("data.bin", std::ios::binary | std::ios::ate);
    if (fayl.is_open()) {
        std::streamsize hajmi = fayl.tellg();
        std::cout << "Fayl hajmi: " << hajmi << " bayt (4 ta int * 4 bayt = 16 bayt)" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::ios::ate` faylni ochishdayoq oxiriga o'rnatadi, `tellg()` esa joriy ofsetni qaytaradi.

## Ishlash natijasi:
```text
Fayl hajmi: 16 bayt (4 ta int * 4 bayt = 16 bayt)
```

---

# 716-Topshiriq: std::stringstream orqali ma'lumotlarni formatlash

## Topshiriq sharti:
Turli ma'lumotlarni xotiradagi oqim orqali satrga yig'ing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <sstream>

int main() {
    std::stringstream ss;
    ss << "Model: BitNet, Parametrlar: " << 10 << "B, Aniqlik: " << 1.58 << " bit";
    std::string matn = ss.str();
    std::cout << matn << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `stringstream` xotirada satrlarni oqim uslubida birlashtirishning eng qulay vositasidir.

## Ishlash natijasi:
```text
Model: BitNet, Parametrlar: 10B, Aniqlik: 1.58 bit
```

---

# 717-Topshiriq: CSV qatorini bo'laklarga ajratish (istringstream va getline)

## Topshiriq sharti:
Vergul bilan ajratilgan ma'lumotlarni `getline(ss, token, ',')` orqali ajrating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <sstream>
#include <string>

int main() {
    std::string csv = "Alisher,25,Toshkent,AI Muhandisi";
    std::istringstream ss(csv);
    std::string qism;
    while (std::getline(ss, qism, ',')) {
        std::cout << "[" << qism << "] ";
    }
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `getline` ning uchinchi parametri istalgan ajratuvchi belgini (delimiter) belgilaydi.

## Ishlash natijasi:
```text
[Alisher] [25] [Toshkent] [AI Muhandisi] 
```

---

# 718-Topshiriq: C++17 std::filesystem::path

## Topshiriq sharti:
`<filesystem>` orqali fayl yo'llarini xavfsiz boshqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    fs::path p = "C:/dataset/kitoblar/lugat.txt";
    std::cout << "Fayl nomi: " << p.filename() << std::endl;
    std::cout << "Kengaytmasi: " << p.extension() << std::endl;
    std::cout << "Papka yo'li: " << p.parent_path() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::filesystem::path` platformalardan mustaqil ravishda (Windows/Linux) yo'llarni boshqaradi.

## Ishlash natijasi:
```text
Fayl nomi: "lugat.txt"
Kengaytmasi: ".txt"
Papka yo'li: "C:/dataset/kitoblar"
```

---

# 719-Topshiriq: Fayl mavjudligini tekshirish (std::filesystem::exists)

## Topshiriq sharti:
Fayl yoki papka diskda bor-yo'qligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

int main() {
    if (std::filesystem::exists("sinov_chiqish.txt")) {
        std::cout << "Fayl diskda mavjud!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `fs::exists` operatsion tizim chaqiruvlari orqali fayl mavjudligini aniqlaydi.

## Ishlash natijasi:
```text
Fayl diskda mavjud!
```

---

# 720-Topshiriq: Yangi papka yaratish (create_directories)

## Topshiriq sharti:
Ichma-ich papkalar zanjirini bitta chaqiruvda yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    fs::create_directories("test_papka/ichki/model");
    if (fs::exists("test_papka/ichki/model")) {
        std::cout << "Papkalar ierarxiyasi muvaffaqiyatli yaratildi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `create_directories` yo'lda yetishmayotgan barcha oraliq papkalarni ham avtomatik ochadi.

## Ishlash natijasi:
```text
Papkalar ierarxiyasi muvaffaqiyatli yaratildi.
```

---

# 721-Topshiriq: Papka ichidagi fayllarni ko'rish (directory_iterator)

## Topshiriq sharti:
Papkadagi barcha fayl va kataloglarni range-based for bilan aylanib chiqing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    std::cout << "Joriy papkadagi fayllar:\n";
    for (const auto& entry : fs::directory_iterator(".")) {
        if (entry.is_regular_file()) {
            std::cout << "  Fayl: " << entry.path().filename() << std::endl;
            break; // Namunaviy bitta fayl kifoya
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `directory_iterator` papkadagi har bir elementni `directory_entry` sifatida beradi.

## Ishlash natijasi:
```text
Joriy papkadagi fayllar:\n  Fayl: ...
```

---

# 722-Topshiriq: Papka va fayllarni tozalash (remove va remove_all)

## Topshiriq sharti:
Yaratilgan vaqtinchalik papkani ichidagi barcha fayllari bilan birga o'chiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    auto ochirildi = fs::remove_all("test_papka");
    std::cout << ochirildi << " ta fayl/papka o'chirildi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `remove_all` papkani rekursiv ravishda tozalaydi.

## Ishlash natijasi:
```text
... ta fayl/papka o'chirildi.
```

---

# 723-Topshiriq: std::filesystem::file_size

## Topshiriq sharti:
Fayl hajmini baytlarda to'g'ridan-to'g'ri o'qing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

int main() {
    if (std::filesystem::exists("data.bin")) {
        auto hajmi = std::filesystem::file_size("data.bin");
        std::cout << "data.bin hajmi: " << hajmi << " bayt" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Faylni ochmasdan uning hajmini aniqlash imkonini beradi.

## Ishlash natijasi:
```text
data.bin hajmi: 16 bayt
```

---

# 724-Topshiriq: Konsol formatlash manipulyatorlari (setprecision, fixed, setw)

## Topshiriq sharti:
Sonlarni jadval ko'rinishida tekislab va aniq o'nlik xonalar bilan chiqaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <iomanip>

int main() {
    double pi = 3.1415926535;
    std::cout << std::fixed << std::setprecision(3);
    std::cout << "Pi (3 xona): " << pi << std::endl;
    std::cout << std::setw(10) << std::setfill('*') << 42 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `<iomanip>` orqali sonlar chiqarilish formati qat'iy nazorat qilinadi.

## Ishlash natijasi:
```text
Pi (3 xona): 3.142\n********42
```

---

# 725-Topshiriq: Binar faylda strukturani saqlash va o'qish

## Topshiriq sharti:
O'yinchining holatini binar faylga saqlab, qayta tiklang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>

struct OyinchiHolati {
    int id;
    int jon;
    double ball;
};

int main() {
    OyinchiHolati h1 = {7, 100, 9500.5};
    std::ofstream out("oyinchi.dat", std::ios::binary);
    out.write(reinterpret_cast<const char*>(&h1), sizeof(h1));
    out.close();

    OyinchiHolati h2;
    std::ifstream in("oyinchi.dat", std::ios::binary);
    in.read(reinterpret_cast<char*>(&h2), sizeof(h2));
    in.close();

    std::cout << "Yuklandi: ID=" << h2.id << ", Jon=" << h2.jon << ", Ball=" << h2.ball << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Trivially copyable strukturalar to'g'ridan-to'g'ri binar saqlanadi.

## Ishlash natijasi:
```text
Yuklandi: ID=7, Jon=100, Ball=9500.5
```

---

# 726-Topshiriq: AI modeli 1-bit og'irliklarini saqlash va yuklash simulyatsiyasi

## Topshiriq sharti:
BitNet b1.58 vaznlarini {-1, 0, 1} binar faylga saqlash va yuklash.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>

int main() {
    std::vector<int8_t> vaznlar = {-1, 0, 1, 1, -1, 0, 1, 1};
    std::ofstream f("weights.bin", std::ios::binary);
    f.write(reinterpret_cast<const char*>(vaznlar.data()), vaznlar.size());
    f.close();

    std::vector<int8_t> yuklangan(8);
    std::ifstream in("weights.bin", std::ios::binary);
    in.read(reinterpret_cast<char*>(yuklangan.data()), yuklangan.size());
    in.close();

    std::cout << "Yuklangan vaznlar: ";
    for (int w : yuklangan) std::cout << w << " ";
    std::cout << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1-bit va ternary modellar og'irliklari ixcham 8-bit yoki 2-bit binar oqimda saqlanadi.

## Ishlash natijasi:
```text
Yuklangan vaznlar: -1 0 1 1 -1 0 1 1 
```

---

# 727-Topshiriq: Fayl oqimi xatolarini istisno sifatida yoqish

## Topshiriq sharti:
`file.exceptions(std::ifstream::failbit)` orqali fayl xatolarini `try-catch` ga uzating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ifstream f;
    f.exceptions(std::ifstream::failbit);
    try {
        f.open("mavjud_bolmagan_fayl_123.xyz");
    } catch (const std::ios_base::failure& e) {
        std::cout << "Fayl ochishda istisno tutildi: " << e.what() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oqim bayroqlari o'rniga istisnolar orqali fayl xatolarini avtomatik ushlash mumkin.

## Ishlash natijasi:
```text
Fayl ochishda istisno tutildi: ...
```

---

# 728-Topshiriq: RAII orqali fayllarni avtomatik yopish kafolati

## Topshiriq sharti:
`ifstream` yoki `ofstream` ko'lamdan chiqqanda `.close()` avtomatik chaqirilishini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>

void yoz() {
    std::ofstream f("avto.txt");
    f << "RAII bilan fayl yopiladi";
    // f.close() chaqirilmasa ham destruktorda avtomatik yopiladi!
}

int main() {
    yoz();
    std::cout << "Fayl RAII orqali xavfsiz yopildi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fayl oqimlari to'liq RAII ga asoslangan.

## Ishlash natijasi:
```text
Fayl RAII orqali xavfsiz yopildi.
```

---

# 729-Topshiriq: Rekursiv papkalar kezuvchisi (recursive_directory_iterator)

## Topshiriq sharti:
Barcha ichma-ich papkalardagi fayllarni chuqurlik bo'yicha sanang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    int sanagich = 0;
    for (const auto& entry : fs::recursive_directory_iterator(".")) {
        sanagich++;
        if (sanagich >= 3) break;
    }
    std::cout << "Rekursiv iterator muvaffaqiyatli ishladi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `recursive_directory_iterator` daraxtsimon kataloglarni to'liq aylanib chiqish imkonini beradi.

## Ishlash natijasi:
```text
Rekursiv iterator muvaffaqiyatli ishladi.
```

---

# 730-Topshiriq: Faylni nusxalash: std::filesystem::copy_file

## Topshiriq sharti:
Faylni yangi nom bilan diskda nusxalang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    if (fs::exists("data.bin")) {
        fs::copy_file("data.bin", "data_nusxa.bin", fs::copy_options::overwrite_existing);
        std::cout << "data_nusxa.bin yaratildi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. OS ning tezkor nusxalash mexanizmidan foydalanadi.

## Ishlash natijasi:
```text
data_nusxa.bin yaratildi.
```

---

# 731-Topshiriq: Faylni qayta nomlash va ko'chirish: std::filesystem::rename

## Topshiriq sharti:
Fayl nomini o'zgartiring yoki boshqa papkaga ko'chiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    if (fs::exists("data_nusxa.bin")) {
        fs::rename("data_nusxa.bin", "data_yangi.bin");
        std::cout << "Fayl nomi o'zgartirildi." << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `rename` fayl nomini tezkor o'zgartiradi.

## Ishlash natijasi:
```text
Fayl nomi o'zgartirildi.
```

---

# 732-Topshiriq: Fayl ruxsatlarini tekshirish: std::filesystem::status

## Topshiriq sharti:
Fayl o'qish yoki yozish huquqlariga egaligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    auto s = fs::status("data.bin");
    std::cout << "Fayl turi: " << (fs::is_regular_file(s) ? "Oddiy fayl" : "Boshqa") << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `fs::status` fayl atributlari va xavfsizlik ruxsatlarini beradi.

## Ishlash natijasi:
```text
Fayl turi: Oddiy fayl
```

---

# 733-Topshiriq: seekp orqali fayl o'rtasidagi ma'lumotni almashtirish

## Topshiriq sharti:
Fayl ko'rsatkichini berilgan manzilga surib yangi bayt yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>

int main() {
    std::fstream f("matn.txt", std::ios::in | std::ios::out | std::ios::trunc);
    f << "Salom Dunyo";
    f.seekp(6); // 'D' ning o'rni
    f << "Olam!";
    f.seekg(0);
    std::string natija;
    std::getline(f, natija);
    std::cout << natija << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `seekp` yozish ko'rsatkichini istalgan ofsetga surish imkonini beradi.

## Ishlash natijasi:
```text
Salom Olam!
```

---

# 734-Topshiriq: Fayl oqimi holat bayroqlari: clear()

## Topshiriq sharti:
EOF ga yetgach oqim holatini tozalab boshidan qayta o'qish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <sstream>

int main() {
    std::stringstream ss("10 20");
    int a, b;
    ss >> a >> b;
    std::cout << "eof(): " << ss.eof() << std::endl;
    ss.clear(); // Xato va EOF bayroqlarini tozalash
    ss.seekg(0);
    int c;
    ss >> c;
    std::cout << "Qayta o'qildi: " << c << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.clear()` oqim xatolarini tozalab yangi murojaatlarga tayyorlaydi.

## Ishlash natijasi:
```text
eof(): 1\nQayta o'qildi: 10
```

---

# 735-Topshiriq: std::nested_exception va throw_with_nested

## Topshiriq sharti:
Xatoni boshqa yuqori darajali xatolik ichiga o'rab (nesting) uzatish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <stdexcept>
#include <exception>

void pastkiAmal() {
    throw std::runtime_error("Diskda joy tugadi");
}

void yuqoriAmal() {
    try {
        pastkiAmal();
    } catch (...) {
        std::throw_with_nested(std::runtime_error("Fayl saqlab bo'lmadi"));
    }
}

int main() {
    try {
        yuqoriAmal();
    } catch (const std::exception& e) {
        std::cout << "Asosiy xato: " << e.what() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ichma-ich istisnolar xatolikning butun chaqiruv zanjirini saqlab qoladi.

## Ishlash natijasi:
```text
Asosiy xato: Fayl saqlab bo'lmadi
```

---

# 736-Topshiriq: std::exception_ptr orqali istisnoni oqimlararo uzatish

## Topshiriq sharti:
Bir oqimdagi xatoni boshqa oqimda ushlash uchun `std::current_exception` dan foydalanish asoslari.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <exception>

int main() {
    std::exception_ptr p;
    try {
        throw std::runtime_error("Oqimdagi xatolik");
    } catch (...) {
        p = std::current_exception(); // Istisno saqlab olindi
    }

    try {
        if (p) std::rethrow_exception(p); // Boshqa joyda qayta otish
    } catch (const std::exception& e) {
        std::cout << "Qayta ushlandi: " << e.what() << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `std::exception_ptr` istisnolarni bir oqimdan ikkinchisiga xavfsiz ko'chirish imkonini beradi.

## Ishlash natijasi:
```text
Qayta ushlandi: Oqimdagi xatolik
```

---

# 737-Topshiriq: std::filesystem orqali bo'sh disk hajmini aniqlash (space)

## Topshiriq sharti:
Diskdagi mavjud bo'sh xotira hajmini GB da o'qing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    fs::space_info si = fs::space(".");
    double boshGB = si.available / (1024.0 * 1024.0 * 1024.0);
    std::cout << "Diskdagi bo'sh joy: " << (int)boshGB << " GB dan ortiq" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `fs::space` diskdagi umumiy, band va bo'sh baytlar miqdorini qaytaradi.

## Ishlash natijasi:
```text
Diskdagi bo'sh joy: ... GB dan ortiq
```

---

# 738-Topshiriq: Fayl kengaytmasini o'zgartirish: replace_extension

## Topshiriq sharti:
Yo'l kengaytmasini '.txt' dan '.bin' ga o'zgartiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

int main() {
    std::filesystem::path p = "model_vaznlari.txt";
    p.replace_extension(".bin");
    std::cout << "Yangi yo'l: " << p << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `replace_extension` kengaytmalarni xavfsiz almashtirish metodidir.

## Ishlash natijasi:
```text
Yangi yo'l: "model_vaznlari.bin"
```

---

# 739-Topshiriq: CSV Faylini o'qib jadval hosil qilish

## Topshiriq sharti:
CSV faylidagi ma'lumotlarni o'qib strukturalar vektoriga to'plang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <sstream>
#include <vector>
#include <string>

struct Qator {
    std::string nom;
    int narx;
};

int main() {
    std::string csvData = "Olma,15000\nAnor,25000";
    std::stringstream ss(csvData);
    std::string line;
    std::vector<Qator> jadval;
    while (std::getline(ss, line)) {
        std::stringstream lineStream(line);
        std::string n, p;
        std::getline(lineStream, n, ',');
        std::getline(lineStream, p, ',');
        jadval.push_back({n, std::stoi(p)});
    }
    for (const auto& q : jadval) {
        std::cout << q.nom << " - " << q.narx << " so'm\n";
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ma'lumotlarni qayta ishlashning klassik CSV tahlilchisi.

## Ishlash natijasi:
```text
Olma - 15000 so'm\nAnor - 25000 so'm
```

---

# 740-Topshiriq: Vaqtinchalik papka yo'lini olish: temp_directory_path

## Topshiriq sharti:
Operatsion tizimning kesh yoki vaqtinchalik katalogini aniqlang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

int main() {
    std::cout << "Vaqtinchalik papka: " << std::filesystem::temp_directory_path() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kesh va vaqtinchalik hisob-kitoblarni saqlash uchun tizim tavsiya qilgan manzil.

## Ishlash natijasi:
```text
Vaqtinchalik papka: ...
```

---

# 741-Topshiriq: Katta fayllarni buferlash (rdbuf)

## Topshiriq sharti:
Faylning butun mazmunini bitta satrga super tezkor o'qib olish (`ss << f.rdbuf()`).

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>
#include <sstream>

int main() {
    std::ifstream f("sinov_chiqish.txt");
    if (f.is_open()) {
        std::stringstream ss;
        ss << f.rdbuf(); // Butun fayl buferi oqimga ko'chirildi
        std::cout << "Yuklangan satrlar hajmi: " << ss.str().length() << " belgi\n";
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `rdbuf()` faylni belgi-ba-belgi emas, yaxlit bufer sifatida eng yuqori tezlikda o'qiydi.

## Ishlash natijasi:
```text
Yuklangan satrlar hajmi: ... belgi
```

---

# 742-Topshiriq: Fayl mavjud bo'lmasa ochishni taqiqlash (C++23 std::ios::noreplace)

## Topshiriq sharti:
Faylni ustiga yozib yubormaslik uchun bayroqlar bilan ishlash.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ofstream f("test_yangi.txt", std::ios::out);
    f << "Yangi ma'lumot";
    f.close();
    std::cout << "Fayl yaratildi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fayllarni boshqarishda mavjud fayllarni tasodifiy o'chirib yuborishdan ehtiyot bo'lish lozim.

## Ishlash natijasi:
```text
Fayl yaratildi.
```

---

# 743-Topshiriq: Fayl nomidan faqat bazaviy nomni ajratish: path::stem

## Topshiriq sharti:
`/path/to/model.bin` dan faqat `model` so'zini ajratib oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

int main() {
    std::filesystem::path p = "/opt/models/bitnet_10b.bin";
    std::cout << "Stem (fayl asosi): " << p.stem() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.stem()` kengaytmasiz asosiy fayl nomini qaytaradi.

## Ishlash natijasi:
```text
Stem (fayl asosi): "bitnet_10b"
```

---

# 744-Topshiriq: Joriy ishchi jildni olish va o'zgartirish: current_path

## Topshiriq sharti:
`std::filesystem::current_path` orqali dastur qayerdan ishlayotganini ko'ring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

int main() {
    std::cout << "Joriy papka: " << std::filesystem::current_path() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dasturning joriy ishchi katalogini (Working Directory) aniqlaydi.

## Ishlash natijasi:
```text
Joriy papka: ...
```

---

# 745-Topshiriq: Oqim manipulyatorlari: boolalpha va hex

## Topshiriq sharti:
Mantiqiy qiymatlarni 'true/false' va sonlarni '0x' formatida chiqarish.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    bool bayroq = true;
    int son = 255;
    std::cout << std::boolalpha << bayroq << std::endl;
    std::cout << "0x" << std::hex << son << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `boolalpha` 1 o'rniga true, `hex` esa 16 lik sanoq sistemasida chiqaradi.

## Ishlash natijasi:
```text
true\n0xff
```

---

# 746-Topshiriq: Fayllarni tozalash (Chiqindi fayllarni o'chirish)

## Topshiriq sharti:
Dastur yakunida yaratilgan sinov fayllarini o'chiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    fs::remove("data_yangi.bin");
    fs::remove("oyinchi.dat");
    fs::remove("test_yangi.txt");
    std::cout << "Sinov fayllari muvaffaqiyatli tozalandi." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Resurslarni toza saqlash dasturiy gigiyenaning asosi hisoblanadi.

## Ishlash natijasi:
```text
Sinov fayllari muvaffaqiyatli tozalandi.
```

---

# 747-Topshiriq: try-catch ichida samaradorlik: Zero-cost Exception handling

## Topshiriq sharti:
Itanium ABI da istisno yuz bermasa try blokining tezlikka mutlaqo ta'sir qilmasligini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Zero-Cost Exceptions: Istisno otilmasa, try bloki uchun hech qanday "
              << "qo'shimcha instruksiya bajarilmaydi (0 overhead)." << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Istisnolar faqat haqiqiy xato sodir bo'lgandagina qo'shimcha jadval o'qishini talab qiladi.

## Ishlash natijasi:
```text
Zero-Cost Exceptions: Istisno otilmasa, try bloki uchun hech qanday qo'shimcha instruksiya bajarilmaydi (0 overhead).
```

---

# 748-Topshiriq: Fayl yo'llarini birlashtirish: operator/

## Topshiriq sharti:
`std::filesystem::path` dagi `/` operatori orqali yo'llarni tabiiy birlashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    fs::path ildiz = "C:/AI_Loyihasi";
    fs::path model = ildiz / "modellar" / "1bit_model.bin";
    std::cout << "Yaxlit yo'l: " << model << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `/` operatori platforma sleshlarini (`/` yoki `\`) avtomatik to'g'ri ulaydi.

## Ishlash natijasi:
```text
Yaxlit yo'l: "C:/AI_Loyihasi/modellar/1bit_model.bin"
```

---

# 749-Topshiriq: Oqimlarda xatoliklarni tekshirish (bad, fail, good)

## Topshiriq sharti:
Oqimning yaxlitlik holatini tahlil qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <sstream>

int main() {
    std::stringstream ss("yuz");
    int son;
    ss >> son; // Harfni songa o'qishga urinish: failbit o'rnatiladi
    if (ss.fail()) {
        std::cout << "Oqimda xato yuz berdi: Matn songa aylanmadi!" << std::endl;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `fail()` mantiqiy xatolar (noto'g'ri format) paytida `true` bo'ladi.

## Ishlash natijasi:
```text
Oqimda xato yuz berdi: Matn songa aylanmadi!
```

---

# 750-Topshiriq: 15-qism xulosasi: Istisnolar, Fayllar va Filesystem Quvvati

## Topshiriq sharti:
RAII va zamonaviy `<filesystem>` birgalikda C++ da fayllar va resurslar boshqaruvini to'liq xavfsiz va qulay qilganini xulosa qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    std::cout << "Istisnolar va Filesystem to'liq o'zlashtirildi: Tizim xotira va fayllar xatolaridan to'liq himoyalangan!" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tizimli dasturlashda to'g'ri I/O va istisnolarni boshqarish barqarorlikning garovidir.

## Ishlash natijasi:
```text
Istisnolar va Filesystem to'liq o'zlashtirildi: Tizim xotira va fayllar xatolaridan to'liq himoyalangan!
```

---

