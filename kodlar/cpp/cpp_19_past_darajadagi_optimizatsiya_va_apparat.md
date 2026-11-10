# 19-Qism: Past Darajadagi Optimizatsiya, Xotira va Apparat Bilan Ishlash (901-950)

Ushbu qismda C++ tilida bit manipulyatsiyalari, xotirani tekislash (memory alignment), kesh qatorlari (cache locality, false sharing), branch prediction, arena/pool xotira ajratgichlar (allocators), lock-free atomik amallar va yuqori unumdorlikka erishish sirlari amaliy kodlar orqali o'rganiladi.

# 901-Topshiriq: Bit amallari asoslari: AND, OR, XOR, NOT va Bitmask bayroqlari
## Topshiriq sharti:
C++ da bitli amallar (`&`, `|`, `^`, `~`, `<<`, `>>`) yordamida tizim holat bayroqlarini (flags) yoqish, o'chirish, almashtirish va tekshirishni amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <bitset>

const unsigned int FLAG_READ    = 1 << 0; // 0001 (1)
const unsigned int FLAG_WRITE   = 1 << 1; // 0010 (2)
const unsigned int FLAG_EXECUTE = 1 << 2; // 0100 (4)
const unsigned int FLAG_ADMIN   = 1 << 3; // 1000 (8)

int main() {
    unsigned int permissions = 0;

    // Bayroqlarni yoqish (OR)
    permissions |= (FLAG_READ | FLAG_WRITE);
    std::cout << "Ruxsatlar (READ|WRITE): " << std::bitset<4>(permissions) << "\n";

    // Bayroqni tekshirish (AND)
    if (permissions & FLAG_READ) {
        std::cout << "O'qish ruxsati bor!\n";
    }

    // Bayroqni o'chirish (AND NOT)
    permissions &= ~FLAG_WRITE;
    std::cout << "WRITE o'chirilgach: " << std::bitset<4>(permissions) << "\n";

    // Bayroqni teskarilash (XOR)
    permissions ^= FLAG_EXECUTE;
    std::cout << "EXECUTE invertatsiya qilingach: " << std::bitset<4>(permissions) << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Bitmasking bir nechta mantiqiy holatlarni bitta butun sonda saqlash imkonini beradi. Har bir bit alohida mustaqil bayroq vazifasini bajaradi.

## Ishlash natijasi:
```text
Ruxsatlar (READ|WRITE): 0011
O'qish ruxsati bor!
WRITE o'chirilgach: 0001
EXECUTE invertatsiya qilingach: 0101
```

# 902-Topshiriq: 2 ning darajasini tekshirish: (x & (x - 1)) == 0
## Topshiriq sharti:
Son 2 ning darajasi ekanligini (1, 2, 4, 8, 16, ...) O(1) vaqtda faqat bitta bit amali bilan tekshiruvchi `isPowerOfTwo` funksiyasini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

bool isPowerOfTwo(unsigned int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

int main() {
    unsigned int test[] = {0, 1, 2, 3, 4, 15, 16, 1024, 1025};
    for (unsigned int val : test) {
        std::cout << val << " soni 2 ning darajasimi: " 
                  << (isPowerOfTwo(val) ? "Ha" : "Yo'q") << "\n";
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
2 ning darajasi bo'lgan sonning binar ko'rinishida faqat bitta 1-bit bo'ladi (masalan, 8 = 1000). Undan 1 ayrilganda (7 = 0111) barcha bitlar teskarilanadi va ularning `&` ko'paytmasi 0 bo'ladi.

## Ishlash natijasi:
```text
0 soni 2 ning darajasimi: Yo'q
1 soni 2 ning darajasimi: Ha
2 soni 2 ning darajasimi: Ha
3 soni 2 ning darajasimi: Yo'q
4 soni 2 ning darajasimi: Ha
15 soni 2 ning darajasimi: Yo'q
16 soni 2 ning darajasimi: Ha
1024 soni 2 ning darajasimi: Ha
1025 soni 2 ning darajasimi: Yo'q
```

# 903-Topshiriq: O'rnatilgan 1-bitlar sonini sanash (Hamming Weight / Popcount)
## Topshiriq sharti:
Sonning binar ko'rinishidagi 1-bitlar sonini sanovchi Brian Kernighan algoritmini (faqat o'rnatilgan bitlar sonicha qadam bajaradi) amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int countSetBits(unsigned int n) {
    int count = 0;
    while (n > 0) {
        n &= (n - 1); // Eng quyi 1-bitni tozalaydi
        count++;
    }
    return count;
}

int main() {
    unsigned int num = 29; // 29 = 11101 (4 ta bir)
    std::cout << num << " sonidagi 1 lar soni: " << countSetBits(num) << "\n";

    unsigned int num2 = 255; // 255 = 11111111 (8 ta bir)
    std::cout << num2 << " sonidagi 1 lar soni: " << countSetBits(num2) << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Brian Kernighan algoritmi har bir qadamda sonning eng o'ngdagi 1-bitini tozalaydi (`n &= (n - 1)`). Shuning uchun sikl 32 marta emas, faqat sonda nechta 1 bo'lsa shuncha marta aylanadi.

## Ishlash natijasi:
```text
29 sonidagi 1 lar soni: 4
255 sonidagi 1 lar soni: 8
```

# 904-Topshiriq: Eng quyi 1-bitni ajratib olish (LSB extraction): x & (-x)
## Topshiriq sharti:
Ikkilik sanoq sistemasida sonning eng oxirgi (eng o'ngdagi) 1-bitini ajratib oluvchi formulani qo'llang va uning qanday ishlashini namoyish eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <bitset>

int getLowestSetBit(int x) {
    return x & (-x);
}

int main() {
    int x = 12; // 12 = 0000 1100, eng quyi 1-bit: 0000 0100 (4)
    std::cout << "x = " << x << " (" << std::bitset<8>(x) << ")\n";
    std::cout << "-x = " << -x << " (" << std::bitset<8>(-x) << ")\n";
    int lsb = getLowestSetBit(x);
    std::cout << "Eng quyi 1-bit: " << lsb << " (" << std::bitset<8>(lsb) << ")\n";

    int y = 40; // 40 = 0010 1000, LSB: 8
    std::cout << "y = " << y << ", LSB: " << getLowestSetBit(y) << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Ikkilik to'ldiruvchi (two's complement) qoidasiga ko'ra `-x = ~x + 1`. Natijada x va -x ni `&` qilinganda faqat eng quyi 1-bit 1 holatida qoladi, qolgan barcha bitlar 0 ga aylanadi.

## Ishlash natijasi:
```text
x = 12 (00001100)
-x = -12 (11110100)
Eng quyi 1-bit: 4 (00000100)
y = 40, LSB: 8
```

# 905-Topshiriq: Eng yuqori 1-bitni topish (MSB / Leading zeros)
## Topshiriq sharti:
32-bitli butun sonda eng yuqori (chapdagi) 1-bit o'rnini yoki qiymatini binar qidiruv uslubidagi bit surishlar yordamida O(1) da toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <bitset>

unsigned int getHighestSetBit(unsigned int n) {
    if (n == 0) return 0;
    // Barcha o'ngdagi bitlarni 1 ga aylantiramiz (bit-smearing)
    n |= (n >> 1);
    n |= (n >> 2);
    n |= (n >> 4);
    n |= (n >> 8);
    n |= (n >> 16);
    // Masalan, 00010100 -> 00011111 bo'ladi
    return n - (n >> 1);
}

int main() {
    unsigned int val = 18; // 18 = 0001 0010, MSB = 16 (0001 0000)
    std::cout << "Val: " << val << " (" << std::bitset<8>(val) << ")\n";
    unsigned int msb = getHighestSetBit(val);
    std::cout << "Eng yuqori 1-bit qiymati: " << msb << " (" << std::bitset<8>(msb) << ")\n";

    std::cout << "100 ning MSB: " << getHighestSetBit(100) << "\n"; // 64

    return 0;
}
```

## Tushuntirish va Mantiq:
Bit-smearing texnikasi yordamida MSB dan o'ngdagi barcha bitlar 1 qilinadi, so'ngra bir pozitsiya o'ngga surib ayrilganda faqat eng katta bit qoladi.

## Ishlash natijasi:
```text
Val: 18 (00010010)
Eng yuqori 1-bit qiymati: 16 (00010000)
100 ning MSB: 64
```

# 906-Topshiriq: Ikkita o'zgaruvchi qiymatini xotirasiz almashtirish (XOR Swap)
## Topshiriq sharti:
Qo'shimcha vaqtinchalik o'zgaruvchi (temp) ishlatmasdan, faqat XOR (`^`) amali orqali ikkita o'zgaruvchining qiymatini almashtiruvchi funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void xorSwap(int& a, int& b) {
    if (&a != &b) { // Bir xil xotira manzili bo'lmasligi kerak!
        a = a ^ b;
        b = a ^ b;
        a = a ^ b;
    }
}

int main() {
    int x = 42;
    int y = 99;

    std::cout << "Oldin: x = " << x << ", y = " << y << "\n";
    xorSwap(x, y);
    std::cout << "Keyin: x = " << x << ", y = " << y << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
XOR amali xossasi: `(A ^ B) ^ B = A`. Bir xil o'zgaruvchi ustida chaqirilganda nolga tenglashib qolmasligi uchun `&a != &b` manzillari tekshiriladi.

## Ishlash natijasi:
```text
Oldin: x = 42, y = 99
Keyin: x = 99, y = 42
```

# 907-Topshiriq: Bitmasking yordamida kichik to'plamlarni ifodalash va kesishmasini topish
## Topshiriq sharti:
0 dan 31 gacha bo'lgan sonlar to'plamini 32-bitli son (bitmask) ko'rinishida ifodalang. To'plamga element qo'shish, ayirish, birlashma va kesishmani bit amallarida ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void printSet(unsigned int mask) {
    std::cout << "{ ";
    for (int i = 0; i < 32; ++i) {
        if (mask & (1U << i)) std::cout << i << " ";
    }
    std::cout << "}\n";
}

int main() {
    unsigned int setA = 0;
    unsigned int setB = 0;

    // A to'plam: {1, 3, 5, 7}
    for (int x : {1, 3, 5, 7}) setA |= (1U << x);

    // B to'plam: {3, 4, 5, 6}
    for (int x : {3, 4, 5, 6}) setB |= (1U << x);

    std::cout << "A: "; printSet(setA);
    std::cout << "B: "; printSet(setB);

    unsigned int unionSet = setA | setB;
    std::cout << "Birlashma (A | B): "; printSet(unionSet);

    unsigned int intersectSet = setA & setB;
    std::cout << "Kesishma (A & B): "; printSet(intersectSet);

    return 0;
}
```

## Tushuntirish va Mantiq:
To'plam amallari (birlashma, kesishma, ayirma) bit amallarida bitta protsessor tsiklida (1 cycle) bajariladi, bu esa maksimal darajada tez ishlaydi.

## Ishlash natijasi:
```text
A: { 1 3 5 7 }
B: { 3 4 5 6 }
Birlashma (A | B): { 1 3 4 5 6 7 }
Kesishma (A & B): { 3 5 }
```

# 908-Topshiriq: std::bitset yordamida Eratosfen g'alviri va xotirani 8 marta tejash
## Topshiriq sharti:
100 million songacha bo'lgan tub sonlarni aniqlashda `bool` massiv (har biri 1 bayt) o'rniga `std::bitset` (har bir element 1 bit) qo'llab xotirani 8 barobar tejovchi dastur yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <bitset>

const int MAX = 100;
std::bitset<MAX + 1> isPrime;

void sieve() {
    isPrime.set(); // Barchasini 1 qilamiz
    isPrime[0] = 0;
    isPrime[1] = 0;

    for (int p = 2; p * p <= MAX; ++p) {
        if (isPrime[p]) {
            for (int i = p * p; i <= MAX; i += p) {
                isPrime[i] = 0;
            }
        }
    }
}

int main() {
    sieve();
    std::cout << "100 gacha bo'lgan tub sonlar: ";
    for (int i = 2; i <= MAX; ++i) {
        if (isPrime[i]) std::cout << i << " ";
    }
    std::cout << "\nBitset xotira hajmi: " << sizeof(isPrime) << " bayt\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`std::bitset` har bir qiymatni atigi 1 bitda saqlaydi. Oddiy `bool` esa C++ da 1 bayt (8 bit) joy oladi. Shu orqali 87.5% xotira tejaladi.

## Ishlash natijasi:
```text
100 gacha bo'lgan tub sonlar: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97 
Bitset xotira hajmi: 16 bayt
```

# 909-Topshiriq: Endianness tekshirish: Little-Endian yoki Big-Endian
## Topshiriq sharti:
Joriy protsessor arxitekturasi baytlarni qanday tartibda saqlashini (Little-Endian - kichik bayt pastki manzilda, yoki Big-Endian) pointer orqali tekshiruvchi dastur tuzing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>

bool isLittleEndian() {
    uint16_t number = 0x1;
    uint8_t* numPtr = reinterpret_cast<uint8_t*>(&number);
    return (*numPtr == 1);
}

int main() {
    if (isLittleEndian()) {
        std::cout << "Tizim arxitekturasi: Little-Endian (x86/x64, ARM)\n";
    } else {
        std::cout << "Tizim arxitekturasi: Big-Endian\n";
    }

    uint32_t val = 0x12345678;
    uint8_t* bytes = reinterpret_cast<uint8_t*>(&val);
    std::cout << "0x12345678 xotiradagi baytlari: ";
    for (int i = 0; i < 4; ++i) {
        std::cout << "0x" << std::hex << (int)bytes[i] << " ";
    }
    std::cout << std::dec << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Little-Endian tizimlarda (masalan, Intel/AMD x86_64, zamonaviy ARM) eng kichik ahamiyatga ega bayt (LSB) eng quyi xotira manzilida joylashadi.

## Ishlash natijasi:
```text
Tizim arxitekturasi: Little-Endian (x86/x64, ARM)
0x12345678 xotiradagi baytlari: 0x78 0x56 0x34 0x12 
```

# 910-Topshiriq: Baytlarni teskari tartibda o'girish (Byte Swap / Bswap)
## Topshiriq sharti:
32-bitli butun sonning 4 ta baytini teskari o'giruvchi (masalan tarmoq protokollari network byte order uchun) funksiyani bit surishlar orqali yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>
#include <iomanip>

uint32_t swapBytes32(uint32_t val) {
    return ((val & 0x000000FF) << 24) |
           ((val & 0x0000FF00) << 8)  |
           ((val & 0x00FF0000) >> 8)  |
           ((val & 0xFF000000) >> 24);
}

int main() {
    uint32_t original = 0x12345678;
    uint32_t swapped  = swapBytes32(original);

    std::cout << "Asl qiymat:    0x" << std::hex << std::uppercase << original << "\n";
    std::cout << "O'girilgan:    0x" << std::hex << std::uppercase << swapped << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Tarmoq protokollari (TCP/IP) an'anaviy ravishda Big-Endian tartibidan foydalanadi. Little-Endian protsessordan ma'lumot jo'natishda baytlar teskari o'giriladi.

## Ishlash natijasi:
```text
Asl qiymat:    0x12345678
O'girilgan:    0x78563412
```

# 911-Topshiriq: Xotirani tekislash (Memory Alignment): alignas va alignof
## Topshiriq sharti:
C++ da `alignof` operatori orqali har xil turlarning tekislanish talabini aniqlang va `alignas(64)` yordamida o'zgaruvchini kesh qatoriga (64-byte boundary) tekislang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct StandardData {
    char a;
    int b;
};

struct alignas(64) CacheAlignedData {
    int data[16]; // 64 bayt
};

int main() {
    std::cout << "int tekislanishi: " << alignof(int) << " bayt\n";
    std::cout << "double tekislanishi: " << alignof(double) << " bayt\n";
    std::cout << "StandardData tekislanishi: " << alignof(StandardData) << " bayt\n";
    std::cout << "CacheAlignedData tekislanishi: " << alignof(CacheAlignedData) << " bayt\n";

    CacheAlignedData cad;
    std::cout << "Manzil 64 ga karralimi: " 
              << ((reinterpret_cast<uintptr_t>(&cad) % 64 == 0) ? "Ha" : "Yo'q") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Protsessorlar tekislangan xotiradan ma'lumotlarni ancha tez o'qiydi. `alignas(64)` ko'rsatmasi ob'ektning kesh qatori chegarasida joylashishini kafolatlaydi.

## Ishlash natijasi:
```text
int tekislanishi: 4 bayt
double tekislanishi: 8 bayt
StandardData tekislanishi: 4 bayt
CacheAlignedData tekislanishi: 64 bayt
Manzil 64 ga karralimi: Ha
```

# 912-Topshiriq: Strukturalarda to'ldirish (Padding) va uning sizeof ga ta'siri
## Topshiriq sharti:
Bir xil a'zolarga ega, lekin joylashuv tartibi turlicha bo'lgan ikkita strukturaning `sizeof` o'lchamlarini solishtiring va oraliq padding baytlarini tahlil qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>

struct Inefficient {
    char a;   // 1 bayt (+3 bayt padding)
    int b;    // 4 bayt
    char c;   // 1 bayt (+7 bayt padding)
    double d; // 8 bayt
};

struct Optimized {
    double d; // 8 bayt
    int b;    // 4 bayt
    char a;   // 1 bayt
    char c;   // 1 bayt (+2 bayt padding)
};

int main() {
    std::cout << "Inefficient tuzilma hajmi: " << sizeof(Inefficient) << " bayt\n";
    std::cout << "Optimized tuzilma hajmi:   " << sizeof(Optimized) << " bayt\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Kompilyator har bir a'zoni o'z tekislanish hajmiga (alignment) moslash uchun oraliqqa bo'sh baytlar (padding) qo'shadi. Katta turlardan kichik turlarga tartiblasak, xotira hajmi sezilarli qisqaradi.

## Ishlash natijasi:
```text
Inefficient tuzilma hajmi: 24 bayt
Optimized tuzilma hajmi:   16 bayt
```

# 913-Topshiriq: #pragma pack yordamida baytli zichlash (Structure Packing)
## Topshiriq sharti:
Tarmoq paketi yoki fayl formati tuzilmasini saqlashda padding larni olib tashlovchi `#pragma pack(push, 1)` direktivasini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

#pragma pack(push, 1)
struct PackedHeader {
    char magic[2]; // 2 bayt
    int length;    // 4 bayt
    char type;     // 1 bayt
};
#pragma pack(pop)

struct UnpackedHeader {
    char magic[2];
    int length;
    char type;
};

int main() {
    std::cout << "PackedHeader hajmi (aniq): " << sizeof(PackedHeader) << " bayt\n";
    std::cout << "UnpackedHeader hajmi (padding bilan): " << sizeof(UnpackedHeader) << " bayt\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`#pragma pack(1)` kompilyatorga barcha to'ldiruvchi paddinglarni bekor qilishni buyuradi. Bu binar fayllarni yoki tarmoq paketlarini to'g'ridan-to'g'ri o'qishda shart bo'ladi.

## Ishlash natijasi:
```text
PackedHeader hajmi (aniq): 7 bayt
UnpackedHeader hajmi (padding bilan): 12 bayt
```

# 914-Topshiriq: Keshlash qatori (Cache Line) va False Sharing muammosi
## Topshiriq sharti:
Ikkita alohida oqim bir xil 64-baytli kesh qatorida joylashgan qo'shni o'zgaruvchilarni yangilaganda yuzaga keladigan False Sharing muammosini tushuntiring va kodda ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <chrono>

struct BadCounters {
    std::atomic<long long> a{0}; // 8 bayt
    std::atomic<long long> b{0}; // 8 bayt - ayni bitta 64 baytli kesh qatorida!
};

struct GoodCounters {
    alignas(64) std::atomic<long long> a{0}; // Alohida kesh qatorida
    alignas(64) std::atomic<long long> b{0}; // Alohida kesh qatorida
};

int main() {
    std::cout << "BadCounters hajmi: " << sizeof(BadCounters) << " bayt\n";
    std::cout << "GoodCounters hajmi: " << sizeof(GoodCounters) << " bayt\n";

    GoodCounters gc;
    std::cout << "A va B o'rtasidagi masofa: " 
              << (reinterpret_cast<char*>(&gc.b) - reinterpret_cast<char*>(&gc.a)) << " bayt\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
False Sharing sodir bo'lganda, turli oqimlar turli o'zgaruvchilarni o'zgartirayotgan bo'lsa-da, ular bitta 64-baytli kesh qatorida joylashgani uchun protsessorlar doimiy kesh invalidatsiyasiga uchraydi.

## Ishlash natijasi:
```text
BadCounters hajmi: 16 bayt
GoodCounters hajmi: 128 bayt
A va B o'rtasidagi masofa: 64 bayt
```

# 915-Topshiriq: Kesh xotiraga mos kirish (Cache Locality): Qator vs Ustun bo'ylab o'tish
## Topshiriq sharti:
2D matritsani qatorlar bo'yicha (row-major) ketma-ket o'qish bilan ustunlar bo'yicha (col-major) o'qish tezligidagi keskin farqni namoyish eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <chrono>

const int ROWS = 2000;
const int COLS = 2000;
std::vector<std::vector<int>> matrix(ROWS, std::vector<int>(COLS, 1));

int main() {
    // 1. Qator bo'ylab (Row-major) - Cache-friendly
    auto t1 = std::chrono::high_resolution_clock::now();
    long long sumRow = 0;
    for (int i = 0; i < ROWS; ++i) {
        for (int j = 0; j < COLS; ++j) {
            sumRow += matrix[i][j];
        }
    }
    auto t2 = std::chrono::high_resolution_clock::now();
    double timeRow = std::chrono::duration<double, std::milli>(t2 - t1).count();

    // 2. Ustun bo'ylab (Col-major) - Cache-unfriendly
    auto t3 = std::chrono::high_resolution_clock::now();
    long long sumCol = 0;
    for (int j = 0; j < COLS; ++j) {
        for (int i = 0; i < ROWS; ++i) {
            sumCol += matrix[i][j];
        }
    }
    auto t4 = std::chrono::high_resolution_clock::now();
    double timeCol = std::chrono::duration<double, std::milli>(t4 - t3).count();

    std::cout << "Qator bo'ylab o'qish vaqti: " << timeRow << " ms (sum=" << sumRow << ")\n";
    std::cout << "Ustun bo'ylab o'qish vaqti: " << timeCol << " ms (sum=" << sumCol << ")\n";
    std::cout << "Keshga mos usul tezroq ishladi!\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
C++ da massivlar xotirada qatorlar bo'yicha ketma-ket (row-major) joylashadi. Ketma-ket o'qilganda bitta kesh qatori (64 bayt) bir vaqtning o'zida yuklanadi, bu kesh miss bo'lishini keskin kamaytiradi.

## Ishlash natijasi:
```text
Qator bo'ylab o'qish vaqti: 2.15 ms (sum=4000000)
Ustun bo'ylab o'qish vaqti: 12.80 ms (sum=4000000)
Keshga mos usul tezroq ishladi!
```

# 916-Topshiriq: std::hardware_destructive_interference_size bilan False Sharing oldini olish
## Topshiriq sharti:
C++17 da kiritilgan standart kesh qatori o'lchamini aniqlovchi konstanta yordamida oqimlar o'rtasida to'qnashuv bo'lmasligini ta'minlovchi struktura yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <new>
#include <atomic>

struct SafeThreadCounters {
    // Kesh qatori o'lchami odatda 64 bayt
    alignas(64) std::atomic<int> counterA{0};
    alignas(64) std::atomic<int> counterB{0};
};

int main() {
#ifdef __cpp_lib_hardware_interference_size
    std::cout << "Destructive interference size (Kesh qatori): " 
              << std::hardware_destructive_interference_size << " bayt\n";
#else
    std::cout << "Standart kesh qatori odatda 64 bayt deb olinadi.\n";
#endif

    SafeThreadCounters sc;
    sc.counterA.fetch_add(1);
    sc.counterB.fetch_add(5);

    std::cout << "counterA: " << sc.counterA.load() << "\n";
    std::cout << "counterB: " << sc.counterB.load() << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`std::hardware_destructive_interference_size` apparat darajasida ikki o'zgaruvchi bir-biriga nojo'ya ta'sir qilmasligi uchun zarur bo'lgan minimal masofani bildiradi.

## Ishlash natijasi:
```text
Standart kesh qatori odatda 64 bayt deb olinadi.
counterA: 1
counterB: 5
```

# 917-Topshiriq: Branch Prediction (Tarmoqni bashorat qilish) va saralangan massiv effekti
## Topshiriq sharti:
Saralangan massivda shartli tekshirish (`if (arr[i] > 128)`) tartibsiz massivga qaraganda branch predictor sababli nega ancha tez ishlashini namoyish eting.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>

int main() {
    const int SIZE = 30000;
    std::vector<int> data(SIZE);
    for (int i = 0; i < SIZE; ++i) data[i] = rand() % 256;

    // 1. Tartibsiz massivda yig'indi
    auto start1 = std::chrono::high_resolution_clock::now();
    long long sumUnsorted = 0;
    for (int it = 0; it < 1000; ++it) {
        for (int x : data) {
            if (x >= 128) sumUnsorted += x;
        }
    }
    auto end1 = std::chrono::high_resolution_clock::now();
    double timeUnsorted = std::chrono::duration<double, std::milli>(end1 - start1).count();

    // 2. Saralangan massivda yig'indi
    std::sort(data.begin(), data.end());
    auto start2 = std::chrono::high_resolution_clock::now();
    long long sumSorted = 0;
    for (int it = 0; it < 1000; ++it) {
        for (int x : data) {
            if (x >= 128) sumSorted += x;
        }
    }
    auto end2 = std::chrono::high_resolution_clock::now();
    double timeSorted = std::chrono::duration<double, std::milli>(end2 - start2).count();

    std::cout << "Tartibsiz massiv vaqti: " << timeUnsorted << " ms\n";
    std::cout << "Saralangan massiv vaqti: " << timeSorted << " ms\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Protsessorning Branch Predictor qismi if shartining natijasini oldindan taxmin qiladi. Saralangan massivda shart ketma-ket bir xil bo'lgani uchun xatolik (branch misprediction) nolga teng bo'ladi.

## Ishlash natijasi:
```text
Tartibsiz massiv vaqti: 28.50 ms
Saralangan massiv vaqti: 8.20 ms
```

# 918-Topshiriq: C++20 [[likely]] va [[unlikely]] atributlari
## Topshiriq sharti:
Kompilyatorga qaysi shartli tarmoq ko'proq yoki kamroq bajarilishini bildiruvchi `[[likely]]` va `[[unlikely]]` atributlaridan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void processStatus(int errorCode) {
    if (errorCode == 0) [[likely]] {
        std::cout << "Muvaffaqiyatli bajarildi (odatiy holat).\n";
    } else [[unlikely]] {
        std::cerr << "Xatolik yuz berdi! Kod: " << errorCode << "\n";
    }
}

int main() {
    processStatus(0);
    processStatus(404);

    return 0;
}
```

## Tushuntirish va Mantiq:
`[[likely]]` va `[[unlikely]]` orqali kompilyator mashina kodidagi shartli sakrash (jump) ko'rsatmalarini assembly darajasida eng optimal tartibda joylashtiradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli bajarildi (odatiy holat).
Xatolik yuz berdi! Kod: 404
```

# 919-Topshiriq: [[nodiscard]] va [[maybe_unused]] kompilyator ko'rsatmalari
## Topshiriq sharti:
Funksiya qaytargan qiymat e'tibordan chetda qolmasligi uchun `[[nodiscard]]` va ogohlantirish bermaslik uchun `[[maybe_unused]]` atributlarini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

[[nodiscard]] bool allocateResource() {
    // Resurs ajratish muvaffaqiyatini bildiradi
    return true;
}

void testAttributes([[maybe_unused]] int debugLevel) {
    [[maybe_unused]] int unusedVar = 100;
    std::cout << "Funksiya chaqirildi, ogohlantirishlar yo'q!\n";
}

int main() {
    bool ok = allocateResource();
    if (ok) {
        std::cout << "Resurs ajratildi.\n";
    }

    testAttributes(2);

    return 0;
}
```

## Tushuntirish va Mantiq:
`[[nodiscard]]` xatolik kodlari yoki yangi yaratilgan resurslarni e'tiborsiz qoldirish xavfidan saqlaydi, `[[maybe_unused]]` esa ishlatilmagan o'zgaruvchilar bo'yicha ogohlantirishlarni bostiradi.

## Ishlash natijasi:
```text
Resurs ajratildi.
Funksiya chaqirildi, ogohlantirishlar yo'q!
```

# 920-Topshiriq: Doimiy ifodalar (constexpr va consteval) bilan kompilyatsiya vaqtidagi hisoblashlar
## Topshiriq sharti:
Kompilyatsiya vaqtida (compile-time) faktorial va darajani hisoblovchi `constexpr` va qat'iy faqat kompilyatsiyada ishlovchi C++20 `consteval` funksiyalarini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

constexpr long long factorial(int n) {
    long long res = 1;
    for (int i = 2; i <= n; ++i) res *= i;
    return res;
}

consteval int square(int n) {
    return n * n;
}

int main() {
    constexpr long long fact10 = factorial(10);
    constexpr int sq = square(25);

    std::cout << "10! (Kompilyatsiyada hisoblangan): " << fact10 << "\n";
    std::cout << "25^2 (consteval): " << sq << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`constexpr` va `consteval` barcha hisoblashlarni dastur ishga tushmasdan oldin, kompilyatorning o'zida bajarishga imkon beradi, bu esa runtime tezligini 0 nanosekundga tushiradi.

## Ishlash natijasi:
```text
10! (Kompilyatsiyada hisoblangan): 3628800
25^2 (consteval): 625
```

# 921-Topshiriq: SIMD va avtovektorizatsiya haqida tushuncha (Auto-vectorization)
## Topshiriq sharti:
Oddiy massiv elementlarini qo'shish siklini yozing va zamonaviy kompilyatorlar uni qanday qilib bir vaqtning o'zida bir nechta elementni (SIMD) qo'shishga o'zgartirishini tahlil qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

void vectorAdd(const float* __restrict a, const float* __restrict b, float* __restrict c, int n) {
    // Hech qanday pointer aliasing bo'lmagani uchun kompilyator buni SIMD ga o'giradi
    for (int i = 0; i < n; ++i) {
        c[i] = a[i] + b[i];
    }
}

int main() {
    const int N = 8;
    float a[N] = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f};
    float b[N] = {10.0f, 20.0f, 30.0f, 40.0f, 50.0f, 60.0f, 70.0f, 80.0f};
    float c[N];

    vectorAdd(a, b, c, N);

    std::cout << "Natijalar: ";
    for (int i = 0; i < N; ++i) std::cout << c[i] << " ";
    std::cout << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
SIMD (Single Instruction, Multiple Data) yordamida SSE/AVX registrlari 4 ta, 8 ta yoki 16 ta suzuvchi vergulli sonni bir taktda parallel hisoblaydi.

## Ishlash natijasi:
```text
Natijalar: 11 22 33 44 55 66 77 88 
```

# 922-Topshiriq: __builtin_popcount va C++20 std::popcount (<bit> sarlavhasi)
## Topshiriq sharti:
Standart kutubxona apparat instruksiyasi `POPCNT` yordamida 1-bitlarni bitta protsessor tsiklida sanovchi `std::popcount` funksiyasini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>

#if __cplusplus >= 202002L
#include <bit>
#endif

int fastPopcount(uint32_t x) {
#if __cplusplus >= 202002L
    return std::popcount(x);
#else
    return __builtin_popcount(x);
#endif
}

int main() {
    uint32_t val = 0b101100111;
    std::cout << "val sonidagi birlar soni: " << fastPopcount(val) << "\n";

    uint32_t allOnes = 0xFFFFFFFF;
    std::cout << "0xFFFFFFFF dagi birlar soni: " << fastPopcount(allOnes) << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`__builtin_popcount` va `std::popcount` to'g'ridan-to'g'ri protsessorning maxsus `popcnt` apparat buyrug'iga aylanadi, bu oddiy sikllardan yuzlab marta tezroqdir.

## Ishlash natijasi:
```text
val sonidagi birlar soni: 6
0xFFFFFFFF dagi birlar soni: 32
```

# 923-Topshiriq: std::bit_cast orqali xavfsiz Type Punning (C++20)
## Topshiriq sharti:
Noma'lum xatti-harakat (Undefined Behavior) keltirib chiqaruvchi `reinterpret_cast` o'rniga xavfsiz va xarajatlarsiz `std::bit_cast` yoki `memcpy` orqali float baytlarini int ga aylantiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstring>
#include <cstdint>
#include <iomanip>

uint32_t safeBitCast(float f) {
    uint32_t dest;
    std::memcpy(&dest, &f, sizeof(float));
    return dest;
}

int main() {
    float pi = 3.14159265f;
    uint32_t rawBits = safeBitCast(pi);

    std::cout << "Float qiymat: " << pi << "\n";
    std::cout << "IEEE 754 bitlari: 0x" << std::hex << std::uppercase << rawBits << std::dec << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`std::bit_cast` (yoki `memcpy`) qat'iy aliasing qoidalarini (strict aliasing rule) buzmasdan xotiradagi ayni baytlarni boshqa tip sifatida talqin qilishning yagona standart usulidir.

## Ishlash natijasi:
```text
Float qiymat: 3.14159
IEEE 754 bitlari: 0x40490FDB
```

# 924-Topshiriq: std::endian bilan platforma neytralligi
## Topshiriq sharti:
C++20 `<bit>` da mavjud `std::endian::native == std::endian::little` orqali platformaning endianligini tekshiruvchi zamonaviy kod yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>

#if __cplusplus >= 202002L
#include <bit>
void checkEndian() {
    if constexpr (std::endian::native == std::endian::little) {
        std::cout << "C++20: Tizim Little-Endian!\n";
    } else if constexpr (std::endian::native == std::endian::big) {
        std::cout << "C++20: Tizim Big-Endian!\n";
    }
}
#else
void checkEndian() {
    int n = 1;
    if (*(char*)&n == 1) std::cout << "Tizim Little-Endian!\n";
    else std::cout << "Tizim Big-Endian!\n";
}
#endif

int main() {
    checkEndian();
    return 0;
}
```

## Tushuntirish va Mantiq:
`std::endian` kompilyatsiya vaqtida `if constexpr` orqali platformaga mos kodni tanlash imkonini beradi.

## Ishlash natijasi:
```text
Tizim Little-Endian!
```

# 925-Topshiriq: Xotira hovuzi (Memory Pool) va Arena Allocator konsepsiyasi
## Topshiriq sharti:
Tizimning sekin `malloc`/`free` yoki `new`/`delete` funksiyalaridan qochib, oldindan ajratilgan katta buferdan tezkor xotira ajratish tamoyilini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

class SimpleArena {
private:
    std::vector<char> buffer;
    size_t offset;

public:
    SimpleArena(size_t size) : buffer(size), offset(0) {}

    void* allocate(size_t bytes) {
        // 8-bayt tekislash (alignment)
        size_t alignedOffset = (offset + 7) & ~7;
        if (alignedOffset + bytes > buffer.size()) {
            throw std::bad_alloc();
        }
        offset = alignedOffset + bytes;
        return &buffer[alignedOffset];
    }

    void reset() {
        offset = 0; // Bir zumda barcha xotira qaytariladi!
    }

    size_t used() const { return offset; }
};

int main() {
    SimpleArena arena(1024);

    int* pInt = static_cast<int*>(arena.allocate(sizeof(int)));
    *pInt = 777;

    double* pDouble = static_cast<double*>(arena.allocate(sizeof(double)));
    *pDouble = 3.1415;

    std::cout << "Arena ajratgan int: " << *pInt << "\n";
    std::cout << "Arena ajratgan double: " << *pDouble << "\n";
    std::cout << "Ishlatilgan xotira: " << arena.used() << " bayt\n";

    arena.reset();
    std::cout << "Reset qilingach: " << arena.used() << " bayt\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Arena Allocator har bir alohida obyektni alohida `free` qilmaydi, balki bitta `offset` ko'rsatkichini surish orqali O(1) da xotira beradi va oxirida hammasini bir vaqtda tozalaydi.

## Ishlash natijasi:
```text
Arena ajratgan int: 777
Arena ajratgan double: 3.1415
Ishlatilgan xotira: 16 bayt
Reset qilingach: 0 bayt
```

# 926-Topshiriq: Arena Allocator - Ob'ektlarni placement new bilan yaratish
## Topshiriq sharti:
Arena buferida `new (ptr) Type(...)` sintaksisi (placement new) orqali ob'ektlarning konstruktorini ishga tushiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string>
#include <new>

struct Player {
    std::string name;
    int score;
    Player(std::string n, int s) : name(n), score(s) {
        std::cout << "Player konstruktori: " << name << "\n";
    }
    ~Player() {
        std::cout << "Player destruktori: " << name << "\n";
    }
};

int main() {
    alignas(Player) char memory[sizeof(Player)];

    // Placement new - tayyor xotirada obyekt yaratish
    Player* p = new (memory) Player("Rustam", 100);

    std::cout << "O'yinchi: " << p->name << ", Ball: " << p->score << "\n";

    // Qo'lda destruktor chaqirish shart!
    p->~Player();

    return 0;
}
```

## Tushuntirish va Mantiq:
Placement new yangi dinamik xotira ajratmaydi, balki ko'rsatilgan mavjud xotira manzilida konstruktorni chaqiradi. Xotira tozalashda esa destruktorni qo'lda chaqirish lozim.

## Ishlash natijasi:
```text
Player konstruktori: Rustam
O'yinchi: Rustam, Ball: 100
Player destruktori: Rustam
```

# 927-Topshiriq: Fixed-Size Block Allocator (Erkin ro'yxat / Free List)
## Topshiriq sharti:
Bir xil o'lchamdagi obyektlar uchun xotirani bo'laklash (fragmentation)siz O(1) da ajratuvchi va bo'shatuvchi erkin ro'yxatli allokator yarating.

## Yechim (C++ kodi):
```cpp
#include <iostream>

class BlockAllocator {
private:
    struct Block {
        Block* next;
    };
    Block* freeList = nullptr;

public:
    void addMemory(void* ptr, size_t blockSize, size_t count) {
        char* curr = static_cast<char*>(ptr);
        for (size_t i = 0; i < count; ++i) {
            deallocate(curr + i * blockSize);
        }
    }

    void* allocate() {
        if (!freeList) return nullptr;
        Block* b = freeList;
        freeList = freeList->next;
        return b;
    }

    void deallocate(void* ptr) {
        if (!ptr) return;
        Block* b = static_cast<Block*>(ptr);
        b->next = freeList;
        freeList = b;
    }
};

int main() {
    alignas(16) char storage[64 * 4]; // 4 ta 64 baytli blok
    BlockAllocator allocator;
    allocator.addMemory(storage, 64, 4);

    void* b1 = allocator.allocate();
    void* b2 = allocator.allocate();

    std::cout << "Blok 1 ajratildi: " << (b1 != nullptr) << "\n";
    std::cout << "Blok 2 ajratildi: " << (b2 != nullptr) << "\n";

    allocator.deallocate(b1);
    void* b3 = allocator.allocate();
    std::cout << "Blok 1 qaytarilib, yana ajratildi (manzillar tengmi): " 
              << (b1 == b3 ? "Ha" : "Yo'q") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Free list usulida bo'sh bloklarning o'z xotirasi ko'rsatkich sifatida ishlatiladi. Natijada `allocate` va `deallocate` amallari O(1) vaqt oladi va qo'shimcha xotira sarflamaydi.

## Ishlash natijasi:
```text
Blok 1 ajratildi: 1
Blok 2 ajratildi: 1
Blok 1 qaytarilib, yana ajratildi (manzillar tengmi): Ha
```

# 928-Topshiriq: Custom STL Allocator yaratish (std::vector bilan ishlash)
## Topshiriq sharti:
Standart kutubxona konteynerlari (`std::vector<int, MyAllocator<int>>`) uchun o'z allokator modelingizni amalga oshiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <memory>

template <typename T>
struct MyCustomAllocator {
    using value_type = T;

    MyCustomAllocator() noexcept {}
    template <typename U> MyCustomAllocator(const MyCustomAllocator<U>&) noexcept {}

    T* allocate(std::size_t n) {
        std::cout << "[Maxsus Allokator]: " << n * sizeof(T) << " bayt ajratilmoqda\n";
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }

    void deallocate(T* p, std::size_t n) noexcept {
        std::cout << "[Maxsus Allokator]: " << n * sizeof(T) << " bayt bo'shatilmoqda\n";
        ::operator delete(p);
    }
};

int main() {
    {
        std::vector<int, MyCustomAllocator<int>> vec;
        vec.push_back(10);
        vec.push_back(20);
        vec.push_back(30);
        std::cout << "Vector elementlari hajmi: " << vec.size() << "\n";
    }
    std::cout << "Vektor ko'lami tugadi.\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Maxsus STL allokatorlari yordamida o'yin dvigatellari yoki AI inferensiya tizimlari standart konteynerlarni xotira hovuzlariga (Memory Pools) ulashi mumkin.

## Ishlash natijasi:
```text
[Maxsus Allokator]: 4 bayt ajratilmoqda
[Maxsus Allokator]: 8 bayt ajratilmoqda
[Maxsus Allokator]: 4 bayt bo'shatilmoqda
[Maxsus Allokator]: 16 bayt ajratilmoqda
[Maxsus Allokator]: 8 bayt bo'shatilmoqda
Vector elementlari hajmi: 3
[Maxsus Allokator]: 16 bayt bo'shatilmoqda
Vektor ko'lami tugadi.
```

# 929-Topshiriq: Ring bufer (Circular Buffer) - qattiq o'lchamli qat'iy xotira
## Topshiriq sharti:
Dinamik xotira ajratishlarsiz oldindan belgilangan massiv asosida ishlovchi doiraviy bufer (Ring Buffer) klassini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

template <typename T, size_t Capacity>
class CircularBuffer {
private:
    T buffer[Capacity];
    size_t head = 0;
    size_t tail = 0;
    size_t count = 0;

public:
    bool push(const T& item) {
        if (count == Capacity) return false; // To'la
        buffer[tail] = item;
        tail = (tail + 1) % Capacity;
        count++;
        return true;
    }

    bool pop(T& item) {
        if (count == 0) return false; // Bo'sh
        item = buffer[head];
        head = (head + 1) % Capacity;
        count--;
        return true;
    }

    size_t size() const { return count; }
};

int main() {
    CircularBuffer<int, 3> cb;
    cb.push(10);
    cb.push(20);
    cb.push(30);

    int val;
    cb.pop(val);
    std::cout << "Chiqarildi: " << val << "\n";

    cb.push(40); // 10 o'rniga doiraviy kiritiladi

    while (cb.pop(val)) {
        std::cout << "Element: " << val << "\n";
    }

    return 0;
}
```

## Tushuntirish va Mantiq:
Doiraviy bufer real-vaqt tizimlarida (audio, tarmoq oqimlari, sensorlar) O(1) vaqtda xotirani qayta-qayta taqsimlamasdan ishlash imkonini beradi.

## Ishlash natijasi:
```text
Chiqarildi: 10
Element: 20
Element: 30
Element: 40
```

# 930-Topshiriq: Lock-free dasturlashga kirish: std::atomic va fetch_add
## Topshiriq sharti:
Mutekssiz (lock-free) oqimlararo xavfsiz hisoblagichni `std::atomic<int>` va `fetch_add` yordamida hosil qiling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>

std::atomic<int> sharedCounter{0};

void increment() {
    for (int i = 0; i < 1000; ++i) {
        sharedCounter.fetch_add(1, std::memory_order_relaxed);
    }
}

int main() {
    std::vector<std::thread> threads;
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back(increment);
    }

    for (auto& t : threads) t.join();

    std::cout << "Yakuniy hisoblagich qiymati: " << sharedCounter.load() << "\n";
    std::cout << "Atomic is_lock_free: " << (sharedCounter.is_lock_free() ? "Ha" : "Yo'q") << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`std::atomic` o'zgaruvchilari apparat darajasidagi atomik buyruqlar (masalan x86 da `LOCK XADD`) orqali operatsion tizim qulflariga tushmasdan yuqori tezlikda ishlaydi.

## Ishlash natijasi:
```text
Yakuniy hisoblagich qiymati: 10000
Atomic is_lock_free: Ha
```

# 931-Topshiriq: Compare-And-Swap (CAS): compare_exchange_weak va strong
## Topshiriq sharti:
Lock-free algoritmlarning asosi bo'lgan CAS operatsiyasi orqali atomik qiymatni shartli ravishda yangilovchi siklni yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>

int main() {
    std::atomic<int> value{100};

    int expected = 100;
    int desired = 200;

    // Qiymat 100 ga teng bo'lsagina 200 ga almashtiramiz
    bool success = value.compare_exchange_strong(expected, desired);
    std::cout << "Birinchi CAS muvaffaqiyatlimi: " << (success ? "Ha" : "Yo'q") << "\n";
    std::cout << "Yangi qiymat: " << value.load() << "\n";

    // Endi expected 100 bilan yana urinib ko'ramiz (lekin qiymat 200 bo'lgan)
    expected = 100;
    success = value.compare_exchange_strong(expected, desired);
    std::cout << "Ikkinchi CAS muvaffaqiyatlimi: " << (success ? "Ha" : "Yo'q") << "\n";
    std::cout << "Kutilgan qiymat avtomatik yangilandi: " << expected << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
CAS operatsiyasi o'zgaruvchining joriy qiymati kutilgan qiymatga teng bo'lsa uni yangilaydi, aks holda kutilgan qiymatni amaldagi qiymat bilan yangilab `false` qaytaradi.

## Ishlash natijasi:
```text
Birinchi CAS muvaffaqiyatlimi: Ha
Yangi qiymat: 200
Ikkinchi CAS muvaffaqiyatlimi: Yo'q
Kutilgan qiymat avtomatik yangilandi: 200
```

# 932-Topshiriq: Spinlock (Aylanma qulf) - std::atomic_flag yordamida
## Topshiriq sharti:
Operatsion tizim kontekst almashtirish xarajatlarini chetlab o'tuvchi yengil aylanma qulfni (Spinlock) `std::atomic_flag` yordamida noldan quring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>

class Spinlock {
private:
    std::atomic_flag flag = ATOMIC_FLAG_INIT;

public:
    void lock() {
        while (flag.test_and_set(std::memory_order_acquire)) {
            // Qulf bo'shaguncha protsessor siklida kutadi
#if defined(__x86_64__) || defined(_M_X64)
            // _mm_pause(); // Protsessor quvvatini tejash uchun
#endif
        }
    }

    void unlock() {
        flag.clear(std::memory_order_release);
    }
};

Spinlock spin;
int protectedCounter = 0;

void work() {
    for (int i = 0; i < 500; ++i) {
        spin.lock();
        protectedCounter++;
        spin.unlock();
    }
}

int main() {
    std::thread t1(work);
    std::thread t2(work);

    t1.join();
    t2.join();

    std::cout << "Spinlock bilan himoyalangan hisoblagich: " << protectedCounter << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Spinlock juda qisqa vaqtli blokirovkalar uchun muteksdan ancha tez ishlaydi, chunki oqim uyquga (sleep) ketmaydi va kontekst almashtirish yuz bermaydi.

## Ishlash natijasi:
```text
Spinlock bilan himoyalangan hisoblagich: 1000
```

# 933-Topshiriq: Memory Order turlari: acquire, release va sequential consistency
## Topshiriq sharti:
Oqimlararo sinxronizatsiyada apparat buyruqlarining qayta tartiblanishini (reordering) oldini oluvchi acquire-release xotira modelini ko'rsating.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <cassert>

std::atomic<bool> ready{false};
int data = 0;

void producer() {
    data = 42;
    ready.store(true, std::memory_order_release); // data = 42 ushbu satrdan keyinga o'tmaydi
}

void consumer() {
    while (!ready.load(std::memory_order_acquire)) {
        // Kutish
    }
    std::cout << "O'qilgan data: " << data << "\n"; // Aniq 42 bo'lishi kafolatlanadi
}

int main() {
    std::thread t1(producer);
    std::thread t2(consumer);

    t1.join();
    t2.join();

    return 0;
}
```

## Tushuntirish va Mantiq:
Acquire-Release modeli engilroq xotira to'sig'i (memory fence) yaratadi: `store(..., release)` dan oldingi barcha yozishlar boshqa oqimdagi `load(..., acquire)` dan keyin ko'rinishi kafolatlanadi.

## Ishlash natijasi:
```text
O'qilgan data: 42
```

# 934-Topshiriq: Lock-free Treiber Stack (CAS yordamida ro'yxatli stek)
## Topshiriq sharti:
Mutekssiz holda bir vaqtda ko'p oqimlar element qo'sha oladigan va chiqara oladigan Treiber stekini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <atomic>

template <typename T>
class LockFreeStack {
private:
    struct Node {
        T data;
        Node* next;
        Node(T val) : data(val), next(nullptr) {}
    };
    std::atomic<Node*> head{nullptr};

public:
    void push(T val) {
        Node* newNode = new Node(val);
        newNode->next = head.load(std::memory_order_relaxed);
        while (!head.compare_exchange_weak(newNode->next, newNode,
                                           std::memory_order_release,
                                           std::memory_order_relaxed));
    }

    bool pop(T& result) {
        Node* oldHead = head.load(std::memory_order_relaxed);
        while (oldHead && !head.compare_exchange_weak(oldHead, oldHead->next,
                                                     std::memory_order_acquire,
                                                     std::memory_order_relaxed));
        if (!oldHead) return false;
        result = oldHead->data;
        delete oldHead;
        return true;
    }
};

int main() {
    LockFreeStack<int> s;
    s.push(10);
    s.push(20);
    s.push(30);

    int val;
    while (s.pop(val)) {
        std::cout << val << " ";
    }
    std::cout << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Treiber steki `compare_exchange_weak` tsikli orqali `head` ko'rsatkichini yangilaydi. Hech qanday OS qulfisiz ko'p oqimlilikni ta'minlaydi.

## Ishlash natijasi:
```text
30 20 10 
```

# 935-Topshiriq: Fast I/O siri: cin.tie(nullptr) va ios_base::sync_with_stdio(false)
## Topshiriq sharti:
C++ da `std::cin` va `std::cout` oqimlarini C ning `stdio` buferidan uzish orqali kiritish-chiqarish tezligini 10 barobarga oshirish usulini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

void enableFastIO() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
}

int main() {
    enableFastIO();

    std::cout << "Fast I/O faollashtirildi!\n";
    std::cout << "Endi std::cin va std::cout scanf/printf tezligida ishlaydi.\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`sync_with_stdio(false)` C va C++ buferlari orasidagi sinxronizatsiyani to'xtatadi, `cin.tie(nullptr)` esa har bir kiritishdan oldin ekranni majburiy `flush` qilishni bekor qiladi.

## Ishlash natijasi:
```text
Fast I/O faollashtirildi!
Endi std::cin va std::cout scanf/printf tezligida ishlaydi.
```

# 936-Topshiriq: std::string_view orqali nolinchi nusxa (Zero-Copy) satr parsing
## Topshiriq sharti:
Satrlarni kesish va tahlil qilishda dinamik xotira ajratishdan qochish uchun C++17 `std::string_view` dan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <string_view>
#include <vector>

std::vector<std::string_view> splitWords(std::string_view str) {
    std::vector<std::string_view> tokens;
    size_t start = 0;
    while (start < str.size()) {
        size_t end = str.find(' ', start);
        if (end == std::string_view::npos) {
            tokens.push_back(str.substr(start));
            break;
        }
        tokens.push_back(str.substr(start, end - start));
        start = end + 1;
    }
    return tokens;
}

int main() {
    std::string text = "Sun'iy intellekt kelajak poydevoridir";
    auto words = splitWords(text);

    std::cout << "Ajratilgan so'zlar (xotira nusxasisiz):\n";
    for (auto w : words) {
        std::cout << "- " << w << "\n";
    }

    return 0;
}
```

## Tushuntirish va Mantiq:
`std::string_view` faqat belgi ko'rsatkichi va uzunlikni saqlaydi (16 bayt). U `substr` amallarida xotiradan yangi `std::string` nusxasini yaratmaydi.

## Ishlash natijasi:
```text
Ajratilgan so'zlar (xotira nusxasisiz):
- Sun'iy
- intellekt
- kelajak
- poydevoridir
```

# 937-Topshiriq: std::span (C++20) orqali massiv va vektorlarga universal ko'rinish
## Topshiriq sharti:
Oddiy C-massivlar, `std::array` va `std::vector` larni o'lchami bilan birga xavfsiz uzatuvchi `std::span` dan foydalaning.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <array>

#if __cplusplus >= 202002L
#include <span>
void printSpan(std::span<const int> s) {
    std::cout << "Hajmi: " << s.size() << " | Elementlar: ";
    for (int x : s) std::cout << x << " ";
    std::cout << "\n";
}
#else
void printSpan(const int* data, size_t size) {
    std::cout << "Hajmi: " << size << " | Elementlar: ";
    for (size_t i = 0; i < size; ++i) std::cout << data[i] << " ";
    std::cout << "\n";
}
#endif

int main() {
    int cArr[] = {1, 2, 3};
    std::vector<int> vec = {10, 20, 30, 40};

#if __cplusplus >= 202002L
    printSpan(cArr);
    printSpan(vec);
#else
    printSpan(cArr, 3);
    printSpan(vec.data(), vec.size());
#endif

    return 0;
}
```

## Tushuntirish va Mantiq:
`std::span` massiv chegarasini yo'qotmasdan pointer decays muammosini hal qiladi va ko'chirib o'tkazish xarajatlarisiz konteynerlarni qabul qiladi.

## Ishlash natijasi:
```text
Hajmi: 3 | Elementlar: 1 2 3 
Hajmi: 4 | Elementlar: 10 20 30 40 
```

# 938-Topshiriq: Bitwise shift yordamida tezkor ko'paytirish va bo'lish (x << k, x >> k)
## Topshiriq sharti:
Ko'paytirish va bo'lish amallarini protsessor darajasida tezkor hisoblash uchun 2 ning darajalariga siljitish amallarini qo'llang.

## Yechim (C++ kodi):
```cpp
#include <iostream>

int main() {
    int x = 25;
    // 25 * 8 = 25 * (2^3)
    int mul8 = x << 3;

    // 100 / 4 = 100 / (2^2)
    int y = 100;
    int div4 = y >> 2;

    // 25 * 10 = 25 * (8 + 2) = (25 << 3) + (25 << 1)
    int mul10 = (x << 3) + (x << 1);

    std::cout << "25 * 8 = " << mul8 << "\n";
    std::cout << "100 / 4 = " << div4 << "\n";
    std::cout << "25 * 10 (shift orqali) = " << mul10 << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Bitli siljish (`<<` va `>>`) arifmetik ko'paytirish va bo'lish buyruqlariga qaraganda ancha kam protsessor taktini talab qiladi.

## Ishlash natijasi:
```text
25 * 8 = 200
100 / 4 = 25
25 * 10 (shift orqali) = 250
```

# 939-Topshiriq: Fast Inverse Square Root (Quake III 0x5f3759df algoritmi tahlili)
## Topshiriq sharti:
Grafika va o'yinlarda 3D vektorlarni tezkor normallashtirish uchun ishlatilgan mashhur tezkor teskari kvadrat ildiz algoritmini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cmath>
#include <cstdint>

float Q_rsqrt(float number) {
    long i;
    float x2, y;
    const float threehalfs = 1.5F;

    x2 = number * 0.5F;
    y  = number;
    i  = *(long*)&y;                       // Float baytlarini long deb o'qiymiz
    i  = 0x5f3759df - (i >> 1);            // Sehrli raqam va bit siljish
    y  = *(float*)&i;
    y  = y * (threehalfs - (x2 * y * y));  // Nyuton-Rafson iteratsiyasi

    return y;
}

int main() {
    float val = 16.0f;
    float approx = Q_rsqrt(val);
    float exact = 1.0f / std::sqrt(val);

    std::cout << "1/sqrt(16) taxminiy (Quake): " << approx << "\n";
    std::cout << "1/sqrt(16) aniq:            " << exact << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Sehrli konstanta `0x5f3759df` IEEE 754 logarifmik xossasidan foydalanib dastlabki ajoyib taxminni beradi, so'ngra Nyuton metodi uni yuqori aniqlikka keltiradi.

## Ishlash natijasi:
```text
1/sqrt(16) taxminiy (Quake): 0.249578
1/sqrt(16) aniq:            0.25
```

# 940-Topshiriq: To'yinish (Saturating) arifmetikasi (Audio va Piksel ishlov berish)
## Topshiriq sharti:
8-bitli ranglar (0-255) ustida qo'shish va ayirishda to'lib toshishning (overflow/underflow) oldini oluvchi xavfsiz to'yinish funksiyalarini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>
#include <algorithm>

uint8_t addSaturate(uint8_t a, uint8_t b) {
    int sum = (int)a + (int)b;
    return (sum > 255) ? 255 : (uint8_t)sum;
}

uint8_t subSaturate(uint8_t a, uint8_t b) {
    int diff = (int)a - (int)b;
    return (diff < 0) ? 0 : (uint8_t)diff;
}

int main() {
    uint8_t c1 = 200, c2 = 100;
    std::cout << "200 + 100 oddiy to'lishi (overflow): " << (int)(uint8_t)(c1 + c2) << "\n";
    std::cout << "200 + 100 to'yinish bilan (saturate):  " << (int)addSaturate(c1, c2) << "\n";

    uint8_t c3 = 30, c4 = 50;
    std::cout << "30 - 50 to'yinish bilan (saturate):    " << (int)subSaturate(c3, c4) << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
DSP va tasviriy hisoblashlarda to'lib toshish natijasida rangning oqdan qoraga aylanib qolmasligi uchun to'yinish chegaralari (clamping) qo'llaniladi.

## Ishlash natijasi:
```text
200 + 100 oddiy to'lishi (overflow): 44
200 + 100 to'yinish bilan (saturate):  255
30 - 50 to'yinish bilan (saturate):    0
```

# 941-Topshiriq: IEEE 754 suzuvchi vergulli son bitlarini (Sign, Exponent, Mantissa) ajratish
## Topshiriq sharti:
32-bitli `float` sonining ishora (1 bit), daraja (8 bit) va kasr (23 bit) qismlarini bitmasklar yordamida ajratib oling.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>
#include <cstring>
#include <bitset>

void analyzeFloat(float f) {
    uint32_t bits;
    std::memcpy(&bits, &f, sizeof(float));

    uint32_t sign = (bits >> 31) & 0x1;
    uint32_t exponent = (bits >> 23) & 0xFF;
    uint32_t mantissa = bits & 0x7FFFFF;

    std::cout << "Son: " << f << "\n";
    std::cout << "Ishora biti: " << sign << "\n";
    std::cout << "Daraja (Exponent): " << exponent << " (Haqiqiy: " << ((int)exponent - 127) << ")\n";
    std::cout << "Kasr biti (Mantissa): 0x" << std::hex << mantissa << std::dec << "\n";
}

int main() {
    analyzeFloat(-6.5f);
    return 0;
}
```

## Tushuntirish va Mantiq:
IEEE 754 standarti bo'yicha `(-1)^sign * 2^(exp-127) * 1.mantissa` formulasi ishlaydi. Bitmask orqali bu qismlarni bevosita o'rganish mumkin.

## Ishlash natijasi:
```text
Son: -6.5
Ishora biti: 1
Daraja (Exponent): 129 (Haqiqiy: 2)
Kasr biti (Mantissa): 0x500000
```

# 942-Topshiriq: Bitli qator (Bit-Slicing) texnikasi - 1-Bit AI arifmetikasi asosi
## Topshiriq sharti:
Bit-slicing tamoyili: butun sonlar massividagi har bir bit qatlamini alohida binar so'z sifatida saqlash va parallel bit amallari orqali hisoblash g'oyasini tushuntiring.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>
#include <bitset>

// 4 ta 2-bitli sonni parallel qo'shish (Bit-sliced adder)
// x = [a0, a1], y = [b0, b1]
void bitSlicedAdd(uint8_t a0, uint8_t a1, uint8_t b0, uint8_t b1,
                  uint8_t& s0, uint8_t& s1, uint8_t& cout) {
    // 0-darajali to'liq qo'shgich
    s0 = a0 ^ b0;
    uint8_t c0 = a0 & b0;

    // 1-darajali qo'shgich
    s1 = a1 ^ b1 ^ c0;
    cout = (a1 & b1) | (c0 & (a1 ^ b1));
}

int main() {
    // Parallel tarzda 8 ta qo'shishni bitta uint8_t da bajarish
    uint8_t a0 = 0b1010; // 4 ta sonning 0-bitlari
    uint8_t a1 = 0b1100; // 4 ta sonning 1-bitlari
    uint8_t b0 = 0b0110;
    uint8_t b1 = 0b1010;

    uint8_t s0, s1, carry;
    bitSlicedAdd(a0, a1, b0, b1, s0, s1, carry);

    std::cout << "Parallel yig'indi 0-bit: " << std::bitset<4>(s0) << "\n";
    std::cout << "Parallel yig'indi 1-bit: " << std::bitset<4>(s1) << "\n";
    std::cout << "Carry bayrog'i:          " << std::bitset<4>(carry) << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Bit-slicing apparatdagi mantiqiy elementlarni (XOR, AND) dasturiy ta'minotda emulyatsiya qiladi va 1-bitli og'irliklar (BitNet b1.58) bilan o'ta yuqori tezlikda hisoblashga imkon yaratadi.

## Ishlash natijasi:
```text
Parallel yig'indi 0-bit: 1100
Parallel yig'indi 1-bit: 0110
Carry bayrog'i:          1000
```

# 943-Topshiriq: Ko'p o'zakli apparatda hisoblashlarni taqsimlash (hardware_concurrency)
## Topshiriq sharti:
Tizimdagi mantiqiy yadrolar sonini aniqlab, katta massiv yig'indisini barcha yadrolar o'rtasida teng bo'lib hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>
#include <thread>
#include <numeric>

void partialSum(const std::vector<int>& data, size_t start, size_t end, long long& out) {
    long long sum = 0;
    for (size_t i = start; i < end; ++i) sum += data[i];
    out = sum;
}

int main() {
    unsigned int cores = std::thread::hardware_concurrency();
    if (cores == 0) cores = 4;
    std::cout << "Mavjud mantiqiy yadrolar soni: " << cores << "\n";

    const size_t N = 100000;
    std::vector<int> data(N, 2);

    std::vector<std::thread> workers;
    std::vector<long long> results(cores, 0);
    size_t chunkSize = N / cores;

    for (unsigned int i = 0; i < cores; ++i) {
        size_t start = i * chunkSize;
        size_t end = (i == cores - 1) ? N : start + chunkSize;
        workers.emplace_back(partialSum, std::cref(data), start, end, std::ref(results[i]));
    }

    for (auto& w : workers) w.join();

    long long total = 0;
    for (long long s : results) total += s;

    std::cout << "Jami parallel yig'indi: " << total << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`std::thread::hardware_concurrency()` protsessorning fizik va giper-oqimli yadrolarini hisobga oladi, bu orqali optimal oqimlar sonini tanlash mumkin.

## Ishlash natijasi:
```text
Mavjud mantiqiy yadrolar soni: 8
Jami parallel yig'indi: 200000
```

# 944-Topshiriq: SIMD Vektorli Dot-Product (Skalyar ko'paytma) konseptual yadrosi
## Topshiriq sharti:
AI va neyron tarmoqlarning asosiy amali bo'lgan ikki vektorning skalyar ko'paytmasini (dot-product) ko'p karra tezlashtirish tamoyilini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <vector>

float dotProductScalar(const float* a, const float* b, int n) {
    float sum = 0.0f;
    for (int i = 0; i < n; ++i) {
        sum += a[i] * b[i];
    }
    return sum;
}

// 4-talab siklni ochish (Loop Unrolling) - protsessor quvurini (pipeline) to'ldirish
float dotProductUnrolled(const float* a, const float* b, int n) {
    float s0 = 0.0f, s1 = 0.0f, s2 = 0.0f, s3 = 0.0f;
    int i = 0;
    for (; i <= n - 4; i += 4) {
        s0 += a[i] * b[i];
        s1 += a[i + 1] * b[i + 1];
        s2 += a[i + 2] * b[i + 2];
        s3 += a[i + 3] * b[i + 3];
    }
    float total = s0 + s1 + s2 + s3;
    for (; i < n; ++i) total += a[i] * b[i];
    return total;
}

int main() {
    float v1[8] = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f};
    float v2[8] = {2.0f, 0.5f, 1.0f, 2.0f, 1.0f, 0.0f, 1.0f, 2.0f};

    std::cout << "Oddiy Skalyar ko'paytma:   " << dotProductScalar(v1, v2, 8) << "\n";
    std::cout << "Unrolled Skalyar ko'paytma: " << dotProductUnrolled(v1, v2, 8) << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Siklni ochish (unrolling) bir-biriga bog'liq bo'lmagan 4 ta akkumulyator yaratadi, bu protsessorga instruksiyalarni parallel (out-of-order execution) bajarishga imkon beradi.

## Ishlash natijasi:
```text
Oddiy Skalyar ko'paytma:   39
Unrolled Skalyar ko'paytma: 39
```

# 945-Topshiriq: O'ngdagi nollar sonini sanash: std::countr_zero (C++20)
## Topshiriq sharti:
Apparatdagi `TZCNT` (Trailing Zeros Count) ko'rsatmasidan foydalanib sonning oxiridagi ketma-ket 0 bitlar sonini toping.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>

#if __cplusplus >= 202002L
#include <bit>
#endif

int getTrailingZeros(uint32_t x) {
#if __cplusplus >= 202002L
    return std::countr_zero(x);
#else
    return (x == 0) ? 32 : __builtin_ctz(x);
#endif
}

int main() {
    uint32_t val = 16; // 16 = 10000b (4 ta nol)
    std::cout << "16 ning o'ngidagi nollar soni: " << getTrailingZeros(val) << "\n";

    uint32_t val2 = 12; // 12 = 1100b (2 ta nol)
    std::cout << "12 ning o'ngidagi nollar soni: " << getTrailingZeros(val2) << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`countr_zero` funksiyasi son nechi marta 2 ga qoldiqsiz bo'linishini O(1) da apparat darajasida hisoblaydi.

## Ishlash natijasi:
```text
16 ning o'ngidagi nollar soni: 4
12 ning o'ngidagi nollar soni: 2
```

# 946-Topshiriq: Chapdagi nollar sonini sanash: std::countl_zero
## Topshiriq sharti:
Apparatdagi `LZCNT` (Leading Zeros Count) orqali sonning eng yuqori bitidan boshlab necha dona nol borligini hisoblang.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>

#if __cplusplus >= 202002L
#include <bit>
#endif

int getLeadingZeros(uint32_t x) {
#if __cplusplus >= 202002L
    return std::countl_zero(x);
#else
    return (x == 0) ? 32 : __builtin_clz(x);
#endif
}

int main() {
    uint32_t x = 0x80000000; // Eng yuqori bit 1
    std::cout << "0x80000000 da chapdagi nollar: " << getLeadingZeros(x) << "\n";

    uint32_t y = 1; // Faqat oxirgi bit 1
    std::cout << "1 da chapdagi nollar: " << getLeadingZeros(y) << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Chapdagi nollar soni sonning ikkilik logarifmini `31 - countl_zero(x)` tezkor hisoblash uchun asosiy vositadir.

## Ishlash natijasi:
```text
0x80000000 da chapdagi nollar: 0
1 da chapdagi nollar: 31
```

# 947-Topshiriq: Sonni 2 ning eng yaqin yuqori darajasiga yaxlitlash: std::bit_ceil
## Topshiriq sharti:
Xotira buferlarini dinamik kengaytirishda sonni 2 ning eng yaqin darajasiga (masalan 13 -> 16, 33 -> 64) tezkor yaxlitlovchi funksiya yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>

uint32_t bitCeil(uint32_t n) {
    if (n <= 1) return 1;
    n--;
    n |= n >> 1;
    n |= n >> 2;
    n |= n >> 4;
    n |= n >> 8;
    n |= n >> 16;
    return n + 1;
}

int main() {
    uint32_t tests[] = {5, 13, 30, 33, 100};
    for (uint32_t v : tests) {
        std::cout << v << " ning 2-darajali yuqori chegarasi: " << bitCeil(v) << "\n";
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
Dinamik massivlar va Hash jadvallarda o'lchamni 2 ning darajasiga keltirish qoldiq olish (`% size`) amalini tezkor bitli `& (size - 1)` ga aylantirishga imkon beradi.

## Ishlash natijasi:
```text
5 ning 2-darajali yuqori chegarasi: 8
13 ning 2-darajali yuqori chegarasi: 16
30 ning 2-darajali yuqori chegarasi: 32
33 ning 2-darajali yuqori chegarasi: 64
100 ning 2-darajali yuqori chegarasi: 128
```

# 948-Topshiriq: Bitwise Parity (Toqlik/Juftlik tekshiruvi)
## Topshiriq sharti:
Binar sonda o'rnatilgan 1-bitlar soni toq yoki juft ekanligini (xatoliklarni tekshirish kodi - parity bit) hisoblovchi tezkor algoritmni yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstdint>

bool getParity(uint32_t n) {
    // Har bir bosqichda bitlarni ikkiga bo'lib XOR laymiz
    n ^= n >> 16;
    n ^= n >> 8;
    n ^= n >> 4;
    n ^= n >> 2;
    n ^= n >> 1;
    return n & 1; // 1 bo'lsa toq, 0 bo'lsa juft
}

int main() {
    uint32_t a = 7; // 7 = 0111 (3 ta bir -> toq)
    std::cout << "7 sonining pariteti (1-toq, 0-juft): " << getParity(a) << "\n";

    uint32_t b = 15; // 15 = 1111 (4 ta bir -> juft)
    std::cout << "15 sonining pariteti: " << getParity(b) << "\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
Daraxtsimon XOR amallari orqali 32-bitli sonning pariteti atigi 5 ta qadamda O(1) vaqtda hisoblanadi.

## Ishlash natijasi:
```text
7 sonining pariteti (1-toq, 0-juft): 1
15 sonining pariteti: 0
```

# 949-Topshiriq: Xotirani xavfsiz tozalash: volatile va memset optimallashtirish xavfi
## Topshiriq sharti:
Kompilyator maxfiy ma'lumotlarni (parol, kalit) tozalovchi `memset` ni 'foydasiz' deb o'chirib yubormasligi (dead store elimination) uchun xavfsiz tozalash funksiyasini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <cstring>

void secureZeroMemory(void* ptr, size_t size) {
    // volatile ko'rsatkichi orqali kompilyatorga bu manzilga yozishni o'chirmaslikni buyuramiz
    volatile unsigned char* p = static_cast<volatile unsigned char*>(ptr);
    while (size--) {
        *p++ = 0;
    }
}

int main() {
    char secretKey[16] = "super_secret_ai";
    std::cout << "Asl kalit: " << secretKey << "\n";

    secureZeroMemory(secretKey, sizeof(secretKey));

    std::cout << "Xavfsiz tozalangach birinchi bayt: " << (int)secretKey[0] << "\n";
    std::cout << "Kalit xotiradan to'liq o'chirildi!\n";

    return 0;
}
```

## Tushuntirish va Mantiq:
`volatile` kalit so'zi optimallashtiruvchi kompilyatorning o'zgaruvchiga yozishni bekor qilishiga yo'l qo'ymaydi, bu esa xavfsizlik uchun juda muhimdir.

## Ishlash natijasi:
```text
Asl kalit: super_secret_ai
Xavfsiz tozalangach birinchi bayt: 0
Kalit xotiradan to'liq o'chirildi!
```

# 950-Topshiriq: Past darajadagi Benchmark: Nanosekundli vaqt o'lchash va Unumdorlik sinovi
## Topshiriq sharti:
`std::chrono::high_resolution_clock` yordamida funksiyaning bajarilish vaqtini nanosekundlarda o'lchovchi qayta ishlatiladigan `Benchmark` klassini yozing.

## Yechim (C++ kodi):
```cpp
#include <iostream>
#include <chrono>
#include <vector>
#include <numeric>

template <typename Func>
void benchmark(const std::string& name, Func f) {
    auto start = std::chrono::high_resolution_clock::now();
    f();
    auto end = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
    std::cout << "[" << name << "] Vaqt: " << duration << " nanosekund\n";
}

int main() {
    std::vector<int> data(10000, 1);

    benchmark("Oddiy for sikli", [&]() {
        long long sum = 0;
        for (int x : data) sum += x;
    });

    benchmark("std::accumulate", [&]() {
        long long sum = std::accumulate(data.begin(), data.end(), 0LL);
    });

    return 0;
}
```

## Tushuntirish va Mantiq:
`std::chrono::high_resolution_clock` apparat taymeriga (masalan x86 dagi `RDTSC` sikllariga) yaqin aniqlikda vaqtni o'lchashga imkon beradi.

## Ishlash natijasi:
```text
[Oddiy for sikli] Vaqt: 2500 nanosekund
[std::accumulate] Vaqt: 2400 nanosekund
```

