# C++ Dasturlash Tili: Mukammal Qo'llanma va Ensiklopediya
## (Noldan Tizimli Dasturlash, Yuqori Tezlikdagi Xotira Boshqaruvi va AI Dvigatellarigacha)

> **Standartlar:** C++11, C++17, C++20, C++23  
> **Maqsad:** Yuqori unumdorlikka ega tizimlar, o'yin dvigatellari, drayverlar va AI inference dvigatellari (llama.cpp) uchun C++ ni o'zbek tilida mukammal o'rganish.

---

## MUNDARIJA

1. [1-Bob: C++ Falsafasi, Tarixi va Kompilyatsiya Modeli](#1-bob)
2. [2-Bob: Xotira Modeli: Stack, Heap, Pointerlar va Havolalar](#2-bob)
3. [3-Bob: RAII Tamoyili va Aqlli Ko'rsatkichlar (Smart Pointers)](#3-bob)
4. [4-Bob: OOP: Konstruktorlar, Destruktorlar va Rule of Five](#4-bob)
5. [5-Bob: Polimorfizm va Virtual Metodlar Jadvali (VTable)](#5-bob)
6. [6-Bob: Ko'chirish Semantikasi (Move Semantics) va Rvalue (`&&`)](#6-bob)
7. [7-Bob: Shablonlar (Templates), Metaprogramming va C++20 Concepts](#7-bob)
8. [8-Bob: Standart Shablonlar Kutubxonasi (STL: Containers & Algorithms)](#8-bob)
9. [9-Bob: Ko'p Oqimlilik (Multithreading), Atomics va Xotira Buyruqlari](#9-bob)
10. [10-Bob: Apparat Darajasidagi Optimizatsiya: SIMD, Kesh va Alignment](#10-bob)
11. [11-Bob: Maxsus Bob: C++ da 1-Bit LLM Tensor Dvigateli (GGML/llama.cpp uslubi)](#11-bob)

---

<a name="1-bob"></a>
# 1-Bob: C++ Falsafasi, Tarixi va Kompilyatsiya Modeli

C++ tili 1979-yilda Byorn Straustrup (Bjarne Stroustrup) tomonidan Bell laboratoriyasida yaratilgan bo'lib, uning asosiy shiori: **"Siz ishlatmagan narsangiz uchun haq to'lamaysiz" (Zero-Overhead Principle)** hisoblanadi.

### 1.1. Kompilyatsiya Bosqichlari
C++ kodi to'g'ridan-to'g'ri protsessorning mashina kodiga kompilyatsiya qilinadi:
1. **Preprotsessor (`#include`, `#define`)**: Sarlavha fayllarni birlashtiradi va makroslarni kengaytiradi.
2. **Kompilyator (Compiler)**: C++ kodini tahlil qilib, assembler tiliga o'giradi.
3. **Assembler**: Assembler kodini mashina binar obyekt fayliga (`.o` yoki `.obj`) aylantiradi.
4. **Bog'lovchi (Linker)**: Bir nechta obyekt fayllarni va tashqi kutubxonalarni bitta `.exe` yoki ELF binar faylga jamlaydi.

```cpp
#include <iostream>

int main() {
    std::cout << "Assalomu alaykum, C++ dunyosi!" << std::endl;
    return 0;
}
```

---

<a name="2-bob"></a>
# 2-Bob: Xotira Modeli: Stack, Heap, Pointerlar va Havolalar

C++ dasturchiga kompyuterning operativ xotirasi (RAM) ustidan to'liq va mutlaq nazorat beradi.

### 2.1. Stack vs Heap
* **Stack**: Funksiya chaqirilganda lokal o'zgaruvchilar uchun ajratiladi. O'ta tezkor (CPU registriga yaqin), hajmi cheklangan (odatda 1-8 MB), xotira funksiya tugashi bilan avtomatik ozod bo'ladi.
* **Heap (Dynamic Memory)**: Dasturchi tomonidan qo'lda ajratiladi (`new` / `malloc`). Hajmi butun RAM bilan cheklanadi, ammo qo'lda o'chirib tashlanmasa (`delete` / `free`), **Memory Leak** (xotira oqishi) yuz beradi.

### 2.2. Pointerlar va Havolalar (Pointers vs References)
```cpp
int son = 42;
int* ptr = &son;     // ptr sonning xotira manzilini saqlaydi
int& ref = son;      // ref sonning o'ziga to'g'ridan-to'g'ri taxallus (alias)

*ptr = 100;          // Xotira manzilidagi qiymatni o'zgartirish
std::cout << son;    // 100 chiqadi
```

---

<a name="3-bob"></a>
# 3-Bob: RAII Tamoyili va Aqlli Ko'rsatkichlar (Smart Pointers)

Zamonaviy C++ da (C++11 dan boshlab) xom `new` va `delete` deyarli ishlatilmaydi. Buning o'rniga **RAII (Resource Acquisition Is Initialization)** tamoyili qo'llaniladi.

### 3.1. `std::unique_ptr`
Fayl yoki xotira ob'ektiga faqat bitta egadorlik (Exclusive Ownership) huquqini beradi. U nusxalanmaydi, faqat ko'chiriladi (`std::move`).
```cpp
#include <memory>

void xavfsiz_xotira() {
    std::unique_ptr<int> p = std::make_unique<int>(500);
    // Funksiya tugaganda xotira avtomatik 'delete' qilinadi!
}
```

### 3.2. `std::shared_ptr` va `std::weak_ptr`
Reference-counting orqali bir nechta egalar o'rtasida umumiy resursni boshqaradi. Oxirgi ega yo'qolganda xotira ozod bo'ladi. Siklik bog'lanishlarning oldini olish uchun `std::weak_ptr` ishlatiladi.

---

<a name="4-bob"></a>
# 4-Bob: OOP: Konstruktorlar, Destruktorlar va Rule of Five

Klass resurslarni (xotira, soket, fayl) boshqarsa, C++ ning "Beshlik Qoidasi" (Rule of Five) ga amal qilishi shart:
1. Destruktor (`~MyClass()`)
2. Nusxalash konstruktori (`MyClass(const MyClass& other)`)
3. Nusxalash biriktirish operatori (`operator=(const MyClass& other)`)
4. Ko'chirish konstruktori (`MyClass(MyClass&& other) noexcept`)
5. Ko'chirish biriktirish operatori (`operator=(MyClass&& other) noexcept`)

---

<a name="5-bob"></a>
# 5-Bob: Polimorfizm va Virtual Metodlar Jadvali (VTable)

C++ da dinamik polimorfizm `virtual` kalit so'zi orqali amalga oshiriladi:
```cpp
class Shakl {
public:
    virtual void chizish() const = 0; // Sof virtual funksiya (Interface)
    virtual ~Shakl() = default;
};

class Doira : public Shakl {
public:
    void chizish() const override {
        std::cout << "Doira chizildi" << std::endl;
    }
};
```
Har bir virtual funksiyaga ega klass uchun kompilyator **VTable** nomli ko'rsatkichlar massivini tuzadi. Har bir obyekt esa ushbu jadvalga havola qiluvchi yashirin `_vptr` ko'rsatkichini saqlaydi.

---

<a name="6-bob"></a>
# 6-Bob: Ko'chirish Semantikasi (Move Semantics) va Rvalue (`&&`)

C++11 ning eng katta yutug'i — bu ortiqcha xotira nusxalashni bartaraf etishdir:
* **Lvalue**: Xotirada aniq manzili bor ob'ektlar.
* **Rvalue (`&&`)**: Vaqtinchalik, tez orada yo'qoladigan ob'ektlar.

`std::move()` orqali vaqtinchalik obyektning xotira ko'rsatkichi yangi ob'ektga o'tkaziladi va nusxalash xarajati O(n) dan O(1) ga tushadi.

---

<a name="7-bob"></a>
# 7-Bob: Shablonlar (Templates), Metaprogramming va C++20 Concepts

Shablonlar kompilyatsiya vaqtida kod generatsiya qilish (Compile-Time Metaprogramming) imkonini beradi:
```cpp
template <typename T>
T maksimal(T a, T b) {
    return (a > b) ? a : b;
}
```

C++20 dagi **Concepts** shablonlarga qat'iy tipli shartlar qo'yadi:
```cpp
#include <concepts>

template <std::integral T>
T qoldiq(T a, T b) {
    return a % b; // Faqat butun sonlar uchun ishlaydi!
}
```

---

<a name="8-bob"></a>
# 8-Bob: Standart Shablonlar Kutubxonasi (STL: Containers & Algorithms)

* `std::vector<T>`: Ketma-ket dinamik massiv. Kesh xotirasi bilan ishlashda eng tezkor konteyner.
* `std::unordered_map<K, V>`: Xesh-jadval, O(1) qidiruv.
* `std::sort()`: Introsort algoritmi (QuickSort + HeapSort + InsertionSort gibridi), kafolatlangan O(n log n).

```cpp
#include <vector>
#include <algorithm>
#include <iostream>

int main() {
    std::vector<int> v = {5, 2, 8, 1, 9};
    std::sort(v.begin(), v.end());
    for (int x : v) std::cout << x << " ";
    return 0;
}
```

---

<a name="9-bob"></a>
# 9-Bob: Ko'p Oqimlilik (Multithreading), Atomics va Xotira Buyruqlari

C++11 dan boshlab platformadan mustaqil `std::thread` standarti kiritildi:
```cpp
#include <thread>
#include <mutex>
#include <atomic>

std::atomic<int> hisoblagich = 0;
std::mutex mtx;

void vazifa() {
    hisoblagich.fetch_add(1, std::memory_order_relaxed);
}

int main() {
    std::thread t1(vazifa);
    std::thread t2(vazifa);
    t1.join();
    t2.join();
    std::cout << "Yakuniy hisob: " << hisoblagich << std::endl;
}
```

---

<a name="10-bob"></a>
# 10-Bob: Apparat Darajasidagi Optimizatsiya: SIMD, Kesh va Alignment

C++ dasturlarini zamonaviy protsessorlarda maksimal tezlatish usullari:
1. **Cache Locality**: Ma'lumotlarni massivlarda ketma-ket joylashtirish (Data-Oriented Design).
2. **SIMD Intrinsics (AVX-512 / NEON)**: Bitta CPU taktida 8 ta yoki 16 ta suzuvchi sonlarni bir vaqtda ko'paytirish.
3. **Memory Alignment (`alignas(64)`)**: Kesh liniyasi (Cache Line) bo'yicha ma'lumotlarni tekislash.

---

<a name="11-bob"></a>
# 11-Bob: Maxsus Bob: C++ da 1-Bit LLM Tensor Dvigateli (GGML/llama.cpp uslubi)

Sun'iy intellekt modellarini (masalan, 10B parametrli model) oddiy kompyuterlarda ishlatish uchun `llama.cpp` C++ tilida yozilgan.

Quyidagi kod 1-bitli kvantlangan vaznlar bilan tezkor inferensiya (Forward Pass) amalga oshirish mexanizmini ko'rsatadi:

```cpp
#include <iostream>
#include <vector>
#include <cstdint>

// 1-Bit Kvantlangan qatlam (BitNet b1.58 C++ implementatsiyasi)
class OneBitLayer {
private:
    int in_dim;
    int out_dim;
    std::vector<int8_t> weights; // -1 yoki +1 vaznlar

public:
    OneBitLayer(int in_d, int out_d) : in_dim(in_d), out_dim(out_d), weights(in_d * out_d) {
        for (int i = 0; i < in_dim * out_dim; ++i) {
            weights[i] = (i % 2 == 0) ? 1 : -1;
        }
    }

    // Hech qanday float ko'paytirishlarsiz sof qo'shish va ayirish
    void forward(const float* input, float* output) const {
        for (int j = 0; j < out_dim; ++j) {
            float sum = 0.0f;
            for (int i = 0; i < in_dim; ++i) {
                int8_t w = weights[i * out_dim + j];
                if (w == 1) sum += input[i];
                else sum -= input[i];
            }
            output[j] = sum;
        }
    }
};

int main() {
    const int in_size = 4;
    const int out_size = 4;
    
    OneBitLayer layer(in_size, out_size);
    float input[in_size] = {0.5f, -0.2f, 0.8f, 0.1f};
    float output[out_size] = {0.0f};

    layer.forward(input, output);

    std::cout << "1-Bit C++ Inferensiya Chiqishi: ";
    for (int i = 0; i < out_size; ++i) {
        std::cout << output[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

---

## XULOSA

C++ — kompyuter arxitekturasi va apparat ta'minotining barcha qudratini to'liq ochib beruvchi tildir. Ushbu qo'llanma O'zbekiston dasturchilariga eng yuqori darajadagi tizimli dasturiy ta'minot va AI dvigatellarini yaratishda mustahkam poydevor bo'lib xizmat qiladi!
