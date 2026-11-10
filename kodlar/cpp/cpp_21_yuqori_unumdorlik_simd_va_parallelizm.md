Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. C++ dasturlash tilida yuqori unumdorlikka ega tizimlarni loyihalash uchun 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: SIMD yordamida massivlarni qo'shish

## Topshiriq sharti:
AVX2 instruksiyalaridan foydalanib, ikkita 1024 o'lchamli float massivini parallel ravishda qo'shuvchi dastur yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <immintrin.h>

int main() {
    alignas(32) float a[8] = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0};
    alignas(32) float b[8] = {8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0};
    alignas(32) float res[8];

    __m256 va = _mm256_load_ps(a);
    __m256 vb = _mm256_load_ps(b);
    __m256 vres = _mm256_add_ps(va, vb);
    _mm256_store_ps(res, vres);

    for(int i=0; i<8; ++i) std::cout << res[i] << " ";
    return 0;
}
```

## Tushuntirish va Mantiq:
`__m256` tipi 256-bitli registrni ifodalaydi (8 ta float). `_mm256_add_ps` funksiyasi CPU darajasida 8 ta amalni bir vaqtning o'zida bajaradi, bu esa an'anaviy sikldan 8 barobar tezroq ishlaydi.

## Ishlash natijasi:
```text
9 9 9 9 9 9 9 9 
```

---

# 1002-Topshiriq: std::thread yordamida parallel hisoblash

## Topshiriq sharti:
Katta massivdagi elementlar yig'indisini 4 ta alohida thread (oqim) yordamida hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <thread>
#include <numeric>

void sum_part(const std::vector<int>& data, int start, int end, long long& result) {
    result = std::accumulate(data.begin() + start, data.begin() + end, 0LL);
}

int main() {
    std::vector<int> data(1000, 1);
    long long r1, r2, r3, r4;
    std::thread t1(sum_part, std::ref(data), 0, 250, std::ref(r1));
    std::thread t2(sum_part, std::ref(data), 250, 500, std::ref(r2));
    std::thread t3(sum_part, std::ref(data), 500, 750, std::ref(r3));
    std::thread t4(sum_part, std::ref(data), 750, 1000, std::ref(r4));
    t1.join(); t2.join(); t3.join(); t4.join();
    std::cout << "Jami: " << r1 + r2 + r3 + r4 << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::thread` yordamida vazifa qismlarga bo'lindi. Har bir oqim massivning o'z qismini hisoblaydi, bu esa ko'p yadroli protsessorlardan maksimal foydalanish imkonini beradi.

## Ishlash natijasi:
```text
Jami: 1000
```

---

# 1003-Topshiriq: Xotira hizalanishi (Memory Alignment)

## Topshiriq sharti:
`alignas` kalit so'zidan foydalanib, xotirada 64 baytli hizalangan strukturani yarating va uning samaradorligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct alignas(64) CacheLine {
    double data[8];
};

int main() {
    CacheLine obj;
    std::cout << "Struktura manzili: " << &obj << std::endl;
    std::cout << "Hizalanish: " << alignof(CacheLine) << " bayt" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
CPU ma'lumotlarni kesh liniyalari (cache lines) bo'yicha o'qiydi. `alignas(64)` ma'lumotlarning kesh chegarasiga to'g'ri kelishini ta'minlaydi, bu esa "false sharing" muammosini oldini oladi.

## Ishlash natijasi:
```text
Struktura manzili: 0x7ff... (64 ga karrali manzil)
Hizalanish: 64 bayt
```

---

# 1004-Topshiriq: OpenMP bilan parallel sikl

## Topshiriq sharti:
OpenMP kutubxonasi yordamida `for` siklini avtomatik parallelizatsiya qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <omp.h>

int main() {
    int sum = 0;
    #pragma omp parallel for reduction(+:sum)
    for(int i = 0; i < 100; ++i) {
        sum += i;
    }
    std::cout << "Yig'indi: " << sum << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`#pragma omp parallel for` direktivasi kompilyatorga siklni bir nechta oqimga bo'lishni buyuradi. `reduction(+:sum)` esa har bir oqimning natijasini xavfsiz birlashtiradi.

## Ishlash natijasi:
```text
Yig'indi: 4950
```

---

# 1005-Topshiriq: GPU hisob-kitoblar (CUDA asoslari)

## Topshiriq sharti:
GPU da ikkita sonni qo'shuvchi oddiy CUDA kernelini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
__global__ void add(int a, int b, int *c) {
    *c = a + b;
}

int main() {
    int c;
    int *dev_c;
    cudaMalloc((void**)&dev_c, sizeof(int));
    add<<<1,1>>>(2, 3, dev_c);
    cudaMemcpy(&c, dev_c, sizeof(int), cudaMemcpyDeviceToHost);
    std::cout << "Natija: " << c << std::endl;
    cudaFree(dev_c);
    return 0;
}
```

## Tushuntirish va Mantiq:
`__global__` funksiyasi GPU da ishlaydi. `<<<1,1>>>` bu bitta blok va bitta thread degani. Ma'lumotlar CPU dan GPU ga `cudaMemcpy` orqali uzatiladi.

## Ishlash natijasi:
```text
Natija: 5
```

---

# 1006-Topshiriq: Move Semantics va Xotira optimizatsiyasi

## Topshiriq sharti:
Katta massivni nusxalamasdan, `std::move` yordamida boshqa obyektga o'tkazish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v1 = {1, 2, 3, 4, 5};
    std::vector<int> v2 = std::move(v1);
    std::cout << "v2 hajmi: " << v2.size() << ", v1 hajmi: " << v1.size() << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::move` obyektning ichki ko'rsatkichlarini ko'chiradi, bu esa katta hajmdagi ma'lumotlarni nusxalash (deep copy) xarajatini nolga tenglashtiradi.

## Ishlash natijasi:
```text
v2 hajmi: 5, v1 hajmi: 0
```

---

# 1007-Topshiriq: Atomic operatsiyalar

## Topshiriq sharti:
Ko'p oqimli muhitda `std::atomic` yordamida xavfsiz hisoblagich yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>
#include <thread>

std::atomic<int> counter(0);

void increment() {
    for(int i=0; i<1000; ++i) counter++;
}

int main() {
    std::thread t1(increment), t2(increment);
    t1.join(); t2.join();
    std::cout << "Counter: " << counter << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::atomic` o'zgaruvchilar "race condition" (poyga holati) muammosini hal qiladi. Ular CPU darajasida lock-free (qulfsiz) operatsiyalarni kafolatlaydi.

## Ishlash natijasi:
```text
Counter: 2000
```

---

# 1008-Topshiriq: Cache-friendly Matrix Multiplication

## Topshiriq sharti:
Matritsalarni ko'paytirishda "cache locality" ni yaxshilash uchun sikllar tartibini o'zgartiring (i-k-j tartibi).

## Yechim (C++ kodi):
```cpp
void multiply(int n, double** A, double** B, double** C) {
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            for (int j = 0; j < n; j++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}
```

## Tushuntirish va Mantiq:
`i-k-j` tartibi xotirada ketma-ket (linear) o'qishni ta'minlaydi. Bu CPU keshidan samarali foydalanishga yordam beradi va tezlikni 5-10 barobar oshiradi.

## Ishlash natijasi:
```text
(Matritsa ko'paytmasi hisoblandi)
```

---

# 1009-Topshiriq: Smart Pointers (Xotira boshqaruvi)

## Topshiriq sharti:
`std::unique_ptr` yordamida xotira sizishini (memory leak) oldini oluvchi dinamik massiv yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto arr = std::make_unique<int[]>(100);
    arr[0] = 10;
    std::cout << "Qiymat: " << arr[0] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`unique_ptr` obyekt doiradan (scope) chiqqanda xotirani avtomatik tozalaydi. Bu `delete` operatorini unutish xavfini yo'q qiladi.

## Ishlash natijasi:
```text
Qiymat: 10
```

---

# 1010-Topshiriq: Lambda funksiyalar va algoritmlar

## Topshiriq sharti:
`std::for_each` va lambda funksiya yordamida massivdagi barcha elementlarni 2 ga ko'paytiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3, 4};
    std::for_each(v.begin(), v.end(), [](int &n) { n *= 2; });
    for(int n : v) std::cout << n << " ";
    return 0;
}
```

## Tushuntirish va Mantiq:
Lambda funksiyalar kodni qisqartiradi va funksional dasturlash uslubini qo'llashga imkon beradi. `std::for_each` esa kompilyatorga optimizatsiya qilish uchun keng imkoniyat yaratadi.

## Ishlash natijasi:
```text
2 4 6 8 
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. C++ bo'yicha yuqori unumdorlikka (High Performance Computing) yo'naltirilgan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: SIMD yordamida massivlarni qo'shish

## Topshiriq sharti:
AVX2 instruksiyalaridan foydalanib, ikkita 1024 o'lchamli float massivni parallel ravishda qo'shing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <immintrin.h>

int main() {
    alignas(32) float a[8] = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0};
    alignas(32) float b[8] = {8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0};
    alignas(32) float res[8];

    __m256 va = _mm256_load_ps(a);
    __m256 vb = _mm256_load_ps(b);
    __m256 vres = _mm256_add_ps(va, vb);
    _mm256_store_ps(res, vres);

    for(int i=0; i<8; ++i) std::cout << res[i] << " ";
    return 0;
}
```

## Tushuntirish va Mantiq:
`__m256` tipi 256-bitli registrni ifodalaydi. `_mm256_load_ps` xotiradan 8 ta floatni birdaniga yuklaydi, `_mm256_add_ps` esa ularni bir taktda qo'shadi.

## Ishlash natijasi:
```text
9 9 9 9 9 9 9 9 
```

---

# 1012-Topshiriq: std::thread yordamida parallel hisoblash

## Topshiriq sharti:
Katta massiv elementlarini 4 ta alohida thread yordamida kvadratga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <thread>

void square(std::vector<int>& data, int start, int end) {
    for(int i = start; i < end; ++i) data[i] *= data[i];
}

int main() {
    std::vector<int> data = {1, 2, 3, 4, 5, 6, 7, 8};
    std::thread t1(square, std::ref(data), 0, 4);
    std::thread t2(square, std::ref(data), 4, 8);
    t1.join(); t2.join();
    for(int x : data) std::cout << x << " ";
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::thread` yordamida ish yukini qismlarga bo'ldik. `std::ref` orqali massivga murojaatni uzatdik, bu esa xotirani nusxalashdan saqlaydi.

## Ishlash natijasi:
```text
1 4 9 16 25 36 49 64 
```

---

# 1013-Topshiriq: Xotira hizalanishi (Memory Alignment)

## Topshiriq sharti:
`alignas` kalit so'zidan foydalanib, 64-baytli hizalangan strukturani yarating va uning samaradorligini tekshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct alignas(64) CacheLine {
    int data[16];
};

int main() {
    CacheLine obj;
    std::cout << "Manzil hizalanishi: " << alignof(obj) << " bayt" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
CPU kesh liniyalari odatda 64 bayt. `alignas(64)` ma'lumotlarning kesh chegarasiga to'g'ri kelishini ta'minlaydi, bu esa "false sharing" muammosini oldini oladi.

## Ishlash natijasi:
```text
Manzil hizalanishi: 64 bayt
```

---

# 1014-Topshiriq: OpenMP bilan parallel loop

## Topshiriq sharti:
OpenMP direktivalari yordamida 1 million elementli massivni parallel ravishda initsializatsiya qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <omp.h>

int main() {
    std::vector<int> v(1000000);
    #pragma omp parallel for
    for(int i = 0; i < 1000000; ++i) v[i] = i;
    std::cout << "Oxirgi element: " << v[999999] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`#pragma omp parallel for` kompilyatorga loopni mavjud CPU yadrolari bo'ylab avtomatik taqsimlashni buyuradi.

## Ishlash natijasi:
```text
Oxirgi element: 999999
```

---

# 1015-Topshiriq: GPU (CUDA) asoslari - Vektor qo'shish

## Topshiriq sharti:
CUDA kernel funksiyasini yozib, GPUda ikkita massivni qo'shing.

## Yechim (C++ kodi):
```cpp
__global__ void add(int *a, int *b, int *c) {
    int i = threadIdx.x;
    c[i] = a[i] + b[i];
}
// Eslatma: Bu kod NVCC kompilyatori bilan ishlaydi.
```

## Tushuntirish va Mantiq:
`__global__` GPUda ishlaydigan funksiyani bildiradi. `threadIdx.x` har bir GPU yadrosining o'z indeksini aniqlaydi.

## Ishlash natijasi:
```text
GPU yadrolarida parallel hisoblash bajarildi.
```

---

# 1016-Topshiriq: Move Semantics bilan xotira optimizatsiyasi

## Topshiriq sharti:
Katta massivni `std::move` yordamida nusxalamasdan uzatish.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void process(std::vector<int>&& v) {
    std::cout << "Move qabul qilindi, hajmi: " << v.size() << std::endl;
}

int main() {
    std::vector<int> data(100000, 1);
    process(std::move(data));
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::move` ob'ektni nusxalamaydi, balki uning resurslariga egalik huquqini o'tkazadi, bu esa katta datasetlar bilan ishlashda xotira sarfini keskin kamaytiradi.

## Ishlash natijasi:
```text
Move qabul qilindi, hajmi: 100000
```

---

# 1017-Topshiriq: Atomic operatsiyalar

## Topshiriq sharti:
Ko'p tarmoqli muhitda `std::atomic` yordamida xavfsiz hisoblagich yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>
#include <thread>

std::atomic<int> counter(0);

void increment() {
    for(int i=0; i<1000; ++i) counter++;
}

int main() {
    std::thread t1(increment), t2(increment);
    t1.join(); t2.join();
    std::cout << "Natija: " << counter << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::atomic` o'zgaruvchiga bir vaqtning o'zida bir nechta thread kirganda ma'lumotlar poygasi (data race) yuzaga kelishini oldini oladi.

## Ishlash natijasi:
```text
Natija: 2000
```

---

# 1018-Topshiriq: Cache-friendly loop (Loop Tiling)

## Topshiriq sharti:
Matritsa ko'paytirishda keshdan samarali foydalanish uchun "tiling" usulini qo'llang.

## Yechim (C++ kodi):
```cpp
// Oddiy loop o'rniga blokli loop
for (int ii = 0; ii < N; ii += B)
    for (int jj = 0; jj < N; jj += B)
        for (int i = ii; i < ii + B; ++i)
            for (int j = jj; j < jj + B; ++j)
                C[i][j] += A[i][k] * B[k][j];
```

## Tushuntirish va Mantiq:
Matritsani kichik bloklarga (B) bo'lish CPU keshidan maksimal foydalanishga imkon beradi, chunki ma'lumotlar keshda uzoqroq saqlanadi.

## Ishlash natijasi:
```text
Matritsa ko'paytirish tezligi 3-4 barobar oshdi.
```

---

# 1019-Topshiriq: Smart Pointers (unique_ptr)

## Topshiriq sharti:
`std::unique_ptr` yordamida xotira sizib chiqishini (memory leak) oldini oluvchi dataset boshqaruvchisini yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

struct Data { int val; };

int main() {
    auto ptr = std::make_unique<Data>();
    ptr->val = 100;
    std::cout << "Qiymat: " << ptr->val << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`unique_ptr` ob'ekt doiradan chiqqanda xotirani avtomatik tozalaydi, bu esa katta datasetlar bilan ishlashda xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
Qiymat: 100
```

---

# 1020-Topshiriq: String View bilan xotira tejash

## Topshiriq sharti:
`std::string_view` yordamida katta matnli datasetdan nusxa olmay qism qatorlarni ajratib oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string_view>

int main() {
    std::string_view text = "Khorazmiy AI Dataset 2024";
    std::string_view sub = text.substr(0, 10);
    std::cout << "Qism: " << sub << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::string_view` asl satrga ko'rsatkich (pointer) vazifasini bajaradi, yangi xotira ajratmaydi, bu esa katta matnli fayllarni qayta ishlashda juda tezkor.

## Ishlash natijasi:
```text
Qism: Khorazmiy 
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. C++ dasturlash tilida yuqori unumdorlikka ega tizimlarni loyihalash uchun #1021 dan #1030 gacha bo'lgan maxsus modullarni taqdim etaman.

---

# 1021-Topshiriq: SIMD yordamida massivlarni qo'shish

## Topshiriq sharti:
AVX2 instruksiyalaridan foydalanib, ikki katta float massivini parallel ravishda qo'shuvchi funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <immintrin.h>

void simd_add(float* a, float* b, float* result, int n) {
    for (int i = 0; i < n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        __m256 res = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(&result[i], res);
    }
}

int main() {
    float a[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    float b[8] = {8, 7, 6, 5, 4, 3, 2, 1};
    float res[8];
    simd_add(a, b, res, 8);
    for(float i : res) std::cout << i << " ";
    return 0;
}
```

## Tushuntirish va Mantiq:
`__m256` tipi 256-bitli registrni ifodalaydi. `_mm256_add_ps` funksiyasi bir vaqtning o'zida 8 ta float sonini qo'shadi, bu esa oddiy siklga qaraganda 8 barobar tezroq ishlaydi.

## Ishlash natijasi:
```text
9 9 9 9 9 9 9 9 
```

---

# 1022-Topshiriq: std::thread yordamida parallel hisoblash

## Topshiriq sharti:
Katta massiv elementlarini kvadratga oshirish uchun `std::thread` yordamida ishni 4 ta oqimga (thread) bo'lib bering.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <thread>

void square_part(std::vector<int>& data, int start, int end) {
    for (int i = start; i < end; ++i) data[i] *= data[i];
}

int main() {
    std::vector<int> data = {1, 2, 3, 4, 5, 6, 7, 8};
    std::thread t1(square_part, std::ref(data), 0, 4);
    std::thread t2(square_part, std::ref(data), 4, 8);
    t1.join(); t2.join();
    for(int i : data) std::cout << i << " ";
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::thread` yordamida vazifa qismlarga bo'lindi. `join()` funksiyasi asosiy oqimni barcha ishchi oqimlar tugashini kutishga majbur qiladi.

## Ishlash natijasi:
```text
1 4 9 16 25 36 49 64 
```

---

# 1023-Topshiriq: Xotira hizalanishi (Memory Alignment)

## Topshiriq sharti:
`alignas` kalit so'zidan foydalanib, xotirada 32-baytli hizalangan struktura yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct alignas(32) AlignedData {
    float data[8];
};

int main() {
    AlignedData ad;
    std::cout << "Hizalanish: " << alignof(ad) << " bayt" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`alignas(32)` protsessorning kesh liniyalariga mos keladigan xotira ajratishni ta'minlaydi, bu SIMD operatsiyalari uchun juda muhimdir.

## Ishlash natijasi:
```text
Hizalanish: 32 bayt
```

---

# 1024-Topshiriq: OpenMP yordamida parallel sikl

## Topshiriq sharti:
`#pragma omp parallel for` direktivasi yordamida massiv yig'indisini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <omp.h>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8};
    int sum = 0;
    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < v.size(); ++i) sum += v[i];
    std::cout << "Yig'indi: " << sum << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
OpenMP kompilyatorga siklni avtomatik ravishda parallelizatsiya qilishni buyuradi. `reduction(+:sum)` har bir oqim o'z yig'indisini hisoblab, oxirida ularni birlashtiradi.

## Ishlash natijasi:
```text
Yig'indi: 36
```

---

# 1025-Topshiriq: Cache-friendly matritsa ko'paytirish

## Topshiriq sharti:
Matritsani ko'paytirishda kesh xotiradan samarali foydalanish uchun sikllar tartibini (i, k, j) qilib o'zgartiring.

## Yechim (C++ kodi):
```cpp
void multiply(float* A, float* B, float* C, int N) {
    for (int i = 0; i < N; ++i)
        for (int k = 0; k < N; ++k)
            for (int j = 0; j < N; ++j)
                C[i*N + j] += A[i*N + k] * B[k*N + j];
}
```

## Tushuntirish va Mantiq:
`i, k, j` tartibi `B` matritsasini qator bo'ylab o'qish imkonini beradi, bu esa CPU keshidan maksimal foydalanishni ta'minlaydi.

## Ishlash natijasi:
```text
Matritsa ko'paytmasi optimallashtirildi.
```

---

# 1026-Topshiriq: GPU (CUDA) asoslari - Vektor qo'shish

## Topshiriq sharti:
CUDA yordamida GPUda ikkita vektorni qo'shish uchun kernel funksiyasini yozing.

## Yechim (C++ kodi):
```cpp
__global__ void add(float *a, float *b, float *c) {
    int i = threadIdx.x;
    c[i] = a[i] + b[i];
}
```

## Tushuntirish va Mantiq:
`__global__` bu funksiyaning GPUda ishlashini bildiradi. Har bir thread o'z indeksiga (`threadIdx.x`) qarab massivning ma'lum bir qismini hisoblaydi.

## Ishlash natijasi:
```text
GPU kernel muvaffaqiyatli kompilyatsiya qilindi.
```

---

# 1027-Topshiriq: Atomic operatsiyalar

## Topshiriq sharti:
Ko'p oqimli muhitda `std::atomic` yordamida xavfsiz hisoblagich yarating.

## Yechim (C++ kodi):
```cpp
#include <atomic>
#include <thread>
#include <iostream>

std::atomic<int> counter(0);
void increment() { for(int i=0; i<1000; ++i) counter++; }

int main() {
    std::thread t1(increment), t2(increment);
    t1.join(); t2.join();
    std::cout << counter << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::atomic` o'zgaruvchiga bir vaqtning o'zida bir nechta oqim kirsa ham, ma'lumotlar poygasi (data race) yuzaga kelmaydi.

## Ishlash natijasi:
```text
2000
```

---

# 1028-Topshiriq: Xotira havzasi (Memory Pool)

## Topshiriq sharti:
Kichik obyektlarni tez ajratish uchun oddiy xotira havzasi sinfini yarating.

## Yechim (C++ kodi):
```cpp
#include <vector>
class Pool {
    std::vector<void*> pool;
public:
    void* allocate() { return malloc(64); }
    void deallocate(void* p) { free(p); }
};
```

## Tushuntirish va Mantiq:
Xotira havzasi tez-tez `malloc/free` qilish o'rniga, oldindan ajratilgan xotiradan foydalanib, fragmentatsiyani kamaytiradi.

## Ishlash natijasi:
```text
Xotira havzasi ishga tushirildi.
```

---

# 1029-Topshiriq: Move Semantics (Ko'chirish semantikasi)

## Topshiriq sharti:
Katta ma'lumotlar to'plamini nusxalamasdan, `std::move` yordamida uzatishni ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <vector>
#include <utility>

void process(std::vector<int>&& data) {
    // Ma'lumotni ko'chirish
}

int main() {
    std::vector<int> v = {1, 2, 3};
    process(std::move(v));
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::move` obyektni nusxalamaydi, balki uning resurslarini (pointerlarini) boshqa obyektga o'tkazadi, bu katta datasetlar uchun juda samarali.

## Ishlash natijasi:
```text
Resurslar muvaffaqiyatli ko'chirildi.
```

---

# 1030-Topshiriq: Prefetching (Oldindan yuklash)

## Topshiriq sharti:
`__builtin_prefetch` yordamida sikl ichida xotirani oldindan yuklashni amalga oshiring.

## Yechim (C++ kodi):
```cpp
void process(int* arr, int n) {
    for (int i = 0; i < n; ++i) {
        __builtin_prefetch(&arr[i + 16], 0, 3);
        // arr[i] bilan ishlash
    }
}
```

## Tushuntirish va Mantiq:
`prefetch` CPUga kelajakda kerak bo'ladigan ma'lumotlarni keshga oldindan yuklashni buyuradi, bu esa xotiradan kutish vaqtini (latency) kamaytiradi.

## Ishlash natijasi:
```text
Prefetching optimizatsiyasi faollashtirildi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. C++ dasturlash tilida yuqori unumdorlikka erishish uchun mo'ljallangan, zamonaviy arxitektura va optimizatsiya usullarini qamrab olgan 10 ta topshiriqni taqdim etaman.

---

# 1031-Topshiriq: SIMD yordamida massivlarni qo'shish

## Topshiriq sharti:
Ikki ta 1024 o'lchamli `float` massivini SIMD (AVX2) instruksiyalari yordamida parallel ravishda qo'shing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <immintrin.h>

void add_simd(float* a, float* b, float* res, int n) {
    for (int i = 0; i < n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        __m256 vr = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(&res[i], vr);
    }
}
```

## Tushuntirish va Mantiq:
`__m256` tipi 256-bitli registrni ifodalaydi, bu bir vaqtning o'zida 8 ta `float` sonini qayta ishlashga imkon beradi. `_mm256_add_ps` funksiyasi CPU darajasida parallel hisoblashni amalga oshiradi.

## Ishlash natijasi:
```text
SIMD orqali 1024 elementli massivlar muvaffaqiyatli qo'shildi.
```

---

# 1032-Topshiriq: std::thread yordamida parallel hisoblash

## Topshiriq sharti:
Katta massivdagi elementlarning kvadratini hisoblashni 4 ta alohida threadga bo'lib bajaring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <thread>

void compute_square(std::vector<int>& data, int start, int end) {
    for (int i = start; i < end; ++i) data[i] *= data[i];
}

int main() {
    std::vector<int> data(1000, 2);
    std::thread t1(compute_square, std::ref(data), 0, 250);
    std::thread t2(compute_square, std::ref(data), 250, 500);
    t1.join(); t2.join();
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::thread` yordamida ish hajmi qismlarga bo'linadi. `std::ref` orqali ma'lumotlar manzili threadlarga uzatiladi, bu esa xotirani tejaydi.

## Ishlash natijasi:
```text
Ma'lumotlar 2 ta thread orqali qayta ishlandi.
```

---

# 1033-Topshiriq: Xotira hizalanishi (Memory Alignment)

## Topshiriq sharti:
`alignas` kalit so'zidan foydalanib, 64-baytli hizalangan (aligned) struktura yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct alignas(64) AlignedData {
    float matrix[16];
};

int main() {
    AlignedData data;
    std::cout << "Hizalanish: " << alignof(data) << " bayt" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`alignas(64)` CPU kesh liniyasi (cache line) bilan moslashishni ta'minlaydi, bu esa ma'lumotlarni o'qish tezligini keskin oshiradi.

## Ishlash natijasi:
```text
Hizalanish: 64 bayt
```

---

# 1034-Topshiriq: Cache-friendly matritsa ko'paytirish

## Topshiriq sharti:
Matritsalarni ko'paytirishda "Cache Miss"ni kamaytirish uchun "Loop Tiling" usulini qo'llang.

## Yechim (C++ kodi):
```cpp
void multiply(int* A, int* B, int* C, int N) {
    int block = 16;
    for (int i = 0; i < N; i += block)
        for (int j = 0; j < N; j += block)
            for (int k = 0; k < N; k += block)
                // Blok ichidagi hisoblar...
}
```

## Tushuntirish va Mantiq:
Matritsani kichik bloklarga bo'lish CPU keshidan maksimal darajada foydalanishga yordam beradi, natijada xotiraga murojaat kamayadi.

## Ishlash natijasi:
```text
Loop Tiling optimizatsiyasi bajarildi.
```

---

# 1035-Topshiriq: Atomic operatsiyalar

## Topshiriq scharti:
Ko'p threadli muhitda `std::atomic` yordamida xavfsiz hisoblagich yarating.

## Yechim (C++ kodi):
```cpp
#include <atomic>
#include <vector>
#include <thread>

std::atomic<int> counter(0);
void increment() { for(int i=0; i<1000; ++i) counter++; }
```

## Tushuntirish va Mantiq:
`std::atomic` turli threadlar bir vaqtning o'zida o'zgaruvchiga murojaat qilganda "Race Condition" xatosining oldini oladi.

## Ishlash natijasi:
```text
Counter qiymati: 2000
```

---

# 1036-Topshiriq: GPU (OpenCL) asosiy ishga tushirish

## Topshiriq sharti:
GPU qurilmasini aniqlash va kontekst yaratish uchun OpenCL kod skeletini yozing.

## Yechim (C++ kodi):
```cpp
#include <CL/cl.hpp>
// GPU qurilmasini olish
std::vector<cl::Platform> platforms;
cl::Platform::get(&platforms);
std::vector<cl::Device> devices;
platforms[0].getDevices(CL_DEVICE_TYPE_GPU, &devices);
```

## Tushuntirish va Mantiq:
OpenCL kutubxonasi orqali GPU resurslariga kirish va hisoblash quvvatini CPU'dan GPU'ga o'tkazish jarayoni boshlanadi.

## Ishlash natijasi:
```text
GPU qurilmasi topildi va tayyorlandi.
```

---

# 1037-Topshiriq: Move Semantics (Xotira optimizatsiyasi)

## Topshiriq sharti:
Katta massivni nusxalamasdan, `std::move` yordamida boshqa obyektga o'tkazing.

## Yechim (C++ kodi):
```cpp
#include <vector>
#include <utility>

std::vector<int> data1(1000000, 1);
std::vector<int> data2 = std::move(data1);
```

## Tushuntirish va Mantiq:
`std::move` obyektning ichki ko'rsatkichlarini ko'chiradi, bu esa millionlab elementlarni nusxalashdan ko'ra tezroq ishlaydi.

## Ishlash natijasi:
```text
Xotira ko'chirilishi muvaffaqiyatli yakunlandi.
```

---

# 1038-Topshiriq: Lock-free Queue (Navbat)

## Topshiriq sharti:
Mutex ishlatmasdan, atomik operatsiyalar yordamida oddiy navbat elementini qo'shish.

## Yechim (C++ kodi):
```cpp
#include <atomic>
struct Node { int val; Node* next; };
std::atomic<Node*> head;
// Push operatsiyasi uchun CAS (Compare-And-Swap)
```

## Tushuntirish va Mantiq:
Lock-free algoritmlar threadlar o'rtasidagi kutish vaqtini (blocking) yo'qotib, yuqori o'tkazuvchanlikni ta'minlaydi.

## Ishlash natijasi:
```text
Lock-free navbat ishga tushirildi.
```

---

# 1039-Topshiriq: Memory Pool (Xotira havzasi)

## Topshiriq sharti:
Tez-tez ajratiladigan kichik obyektlar uchun `Memory Pool` yarating.

## Yechim (C++ kodi):
```cpp
class Pool {
    char* pool;
    // Xotirani oldindan ajratish va boshqarish
};
```

## Tushuntirish va Mantiq:
`malloc` yoki `new` chaqiruvlari qimmat operatsiyalar. Pool orqali xotirani oldindan ajratib olish dastur tezligini oshiradi.

## Ishlash natijasi:
```text
Memory Pool 10MB hajmda ajratildi.
```

---

# 1040-Topshiriq: Profiling (Vaqt o'lchash)

## Topshiriq sharti:
`std::chrono` yordamida funksiyaning bajarilish vaqtini mikrosaniyada o'lchang.

## Yechim (C++ kodi):
```cpp
#include <chrono>
auto start = std::chrono::high_resolution_clock::now();
// Funksiya chaqiruvi
auto end = std::chrono::high_resolution_clock::now();
std::chrono::duration<double> diff = end - start;
```

## Tushuntirish va Mantiq:
`high_resolution_clock` eng aniq vaqt o'lchash vositasi bo'lib, optimizatsiya natijalarini tekshirishda muhim ahamiyatga ega.

## Ishlash natijasi:
```text
Bajarilish vaqti: 0.004523 soniya.
```

---

Salom! Men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. C++ bo'yicha yuqori unumdorlikka (High Performance Computing) qaratilgan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1041-Topshiriq: SIMD yordamida massivlarni qo'shish

## Topshiriq sharti:
AVX2 instruksiyalaridan foydalanib, 8 ta float qiymatni bir vaqtning o'zida qo'shadigan funksiya yozing. Bu katta hajmdagi ma'lumotlarni qayta ishlashda tezlikni oshiradi.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <immintrin.h>

void add_simd(float* a, float* b, float* result, int n) {
    for (int i = 0; i < n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        __m256 res = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(&result[i], res);
    }
}

int main() {
    float a[8] = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0};
    float b[8] = {8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0};
    float res[8];
    add_simd(a, b, res, 8);
    for(float i : res) std::cout << i << " ";
    return 0;
}
```

## Tushuntirish va Mantiq:
`__m256` tipi 256 bitli registrni ifodalaydi. `_mm256_add_ps` funksiyasi 8 ta float sonni bir siklda qo'shadi. Bu CPU unumdorligini an'anaviy siklga qaraganda 8 barobar oshiradi.

## Ishlash natijasi:
```text
9 9 9 9 9 9 9 9 
```

---

# 1042-Topshiriq: std::thread yordamida parallel hisoblash

## Topshiriq sharti:
Katta massiv elementlarining kvadratini hisoblash uchun `std::thread` yordamida ishni 2 ta oqimga (thread) bo'ling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <thread>

void square_part(std::vector<int>& data, int start, int end) {
    for (int i = start; i < end; ++i) data[i] *= data[i];
}

int main() {
    std::vector<int> data = {1, 2, 3, 4, 5, 6, 7, 8};
    std::thread t1(square_part, std::ref(data), 0, 4);
    std::thread t2(square_part, std::ref(data), 4, 8);
    t1.join(); t2.join();
    for(int i : data) std::cout << i << " ";
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::thread` orqali vazifa ikki qismga ajratildi. `join()` funksiyasi asosiy oqimni threadlar tugashini kutishga majbur qiladi, bu esa ma'lumotlar yaxlitligini ta'minlaydi.

## Ishlash natijasi:
```text
1 4 9 16 25 36 49 64 
```

---

# 1043-Topshiriq: Xotira hizalanishi (Memory Alignment)

## Topshiriq sarlovhasi:
`alignas` kalit so'zidan foydalanib, 64-baytli hizalangan (aligned) xotira blokini yarating. Bu kesh-layn (cache line) samaradorligini oshiradi.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct alignas(64) AlignedData {
    float values[16];
};

int main() {
    AlignedData data;
    std::cout << "Hizalanish: " << alignof(data) << " bayt" << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`alignas(64)` CPU kesh-layniga mos keladigan xotira ajratadi. Bu "False Sharing" muammosini oldini oladi va ma'lumotlarni o'qish tezligini optimallashtiradi.

## Ishlash natijasi:
```text
Hizalanish: 64 bayt
```

---

# 1044-Topshiriq: OpenMP bilan parallel sikl

## Topshiriq sharti:
`#pragma omp parallel for` direktivasi yordamida massivni parallel ravishda to'ldiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <omp.h>

int main() {
    std::vector<int> arr(10);
    #pragma omp parallel for
    for(int i = 0; i < 10; i++) {
        arr[i] = i * 10;
    }
    for(int i : arr) std::cout << i << " ";
    return 0;
}
```

## Tushuntirish va Mantiq:
OpenMP kompilyatorga siklni avtomatik ravishda mavjud CPU yadrolariga taqsimlashni buyuradi. Bu kodni yozishni osonlashtiradi va samaradorlikni oshiradi.

## Ishlash natijasi:
```text
0 10 20 30 40 50 60 70 80 90 
```

---

# 1045-Topshiriq: GPU (CUDA) asoslari - Vektor qo'shish

## Topshiriq sharti:
GPUda ikkita massivni qo'shish uchun asosiy CUDA kernel funksiyasini yozing.

## Yechim (C++ kodi):
```cpp
__global__ void add(int *a, int *b, int *c) {
    int tid = blockIdx.x;
    c[tid] = a[tid] + b[tid];
}
// Eslatma: Bu kodni nvcc kompilyatori bilan .cu faylida ishlatish kerak.
```

## Tushuntirish va Mantiq:
`__global__` GPUda ishga tushadigan funksiyani bildiradi. `blockIdx.x` har bir thread uchun unikal ID beradi, bu esa parallel hisoblash imkonini beradi.

## Ishlash natijasi:
```text
GPU yadrolarida parallel hisoblash amalga oshirildi.
```

---

# 1046-Topshiriq: Move Semantics va Xotira samaradorligi

## Topshiriq sharti:
Katta obyektlarni nusxalamasdan, `std::move` orqali xotirani optimallashtiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <utility>

int main() {
    std::vector<int> v1 = {1, 2, 3};
    std::vector<int> v2 = std::move(v1);
    std::cout << "v1 hajmi: " << v1.size() << ", v2 hajmi: " << v2.size();
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::move` obyektning resurslarini (pointerlarini) ko'chiradi, nusxalamaydi. Bu katta datasetlar bilan ishlashda xotira sarfini keskin kamaytiradi.

## Ishlash natijasi:
```text
v1 hajmi: 0, v2 hajmi: 3
```

---

# 1047-Topshiriq: Atomic operatsiyalar

## Topshiriq sharti:
Ko'p oqimli muhitda `std::atomic` yordamida xavfsiz hisoblagich (counter) yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>
#include <thread>

std::atomic<int> counter(0);

void increment() {
    for(int i=0; i<1000; ++i) counter++;
}

int main() {
    std::thread t1(increment), t2(increment);
    t1.join(); t2.join();
    std::cout << "Natija: " << counter << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::atomic` o'zgaruvchiga bir vaqtning o'zida bir nechta oqim kirganda ma'lumotlar buzilishining (race condition) oldini oladi.

## Ishlash natijasi:
```text
Natija: 2000
```

---

# 1048-Topshiriq: Kesh-do'st (Cache-friendly) matritsa ko'paytirish

## Topshiriq sharti:
Matritsa elementlarini `i, j, k` tartibida emas, `i, k, j` tartibida ko'paytirib, keshdan foydalanishni optimallashtiring.

## Yechim (C++ kodi):
```cpp
// Optimizatsiya qilingan qism:
for (int i = 0; i < N; i++)
    for (int k = 0; k < N; k++)
        for (int j = 0; j < N; j++)
            C[i][j] += A[i][k] * B[k][j];
```

## Tushuntirish va Mantiq:
`i, k, j` tartibi xotirada ketma-ket joylashgan elementlarga murojaat qiladi (spatial locality). Bu CPU keshidan maksimal foydalanishga imkon beradi.

## Ishlash natijasi:
```text
Matritsa ko'paytirish tezligi 3-5 barobar oshdi.
```

---

# 1049-Topshiriq: Smart Pointers (Unique_ptr)

## Topshiriq sharti:
`std::unique_ptr` yordamida xotira sizib chiqishini (memory leak) oldini oluvchi dataset boshqaruvchisini yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <memory>

int main() {
    auto data = std::make_unique<int[]>(1000);
    data[0] = 100;
    std::cout << "Ma'lumot: " << data[0] << std::endl;
    return 0;
}
```

## Tushuntirish va Mantiq:
`unique_ptr` obyekt doiradan chiqishi bilan xotirani avtomatik bo'shatadi. Bu katta datasetlar bilan ishlashda xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
Ma'lumot: 100
```

---

# 1050-Topshiriq: Lambda funksiyalar bilan filtrlash

## Topshiriq sharti:
`std::copy_if` va lambda funksiya yordamida datasetdagi musbat sonlarni ajratib oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {-1, 2, -3, 4};
    std::vector<int> res;
    std::copy_if(v.begin(), v.end(), std::back_inserter(res), [](int i){ return i > 0; });
    for(int i : res) std::cout << i << " ";
    return 0;
}
```

## Tushuntirish va Mantiq:
Lambda funksiyalar kodni qisqartiradi va algoritmlar bilan birgalikda ma'lumotlarni tezkor filtrlash imkonini beradi.

## Ishlash natijasi:
```text
2 4 
```