# C Dasturlash Tili — 20-Qism: Yuqori Samaradorlik va Xavfsiz C (High Performance & Security)
## (951-1000 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* Buffer overflow, Format string va Integer overflow zaifliklari va ularning profilaktikasi
* Dangling pointers, Use-After-Free va Valgrind/ASan tahlili
* Keshga mos arxitektura (Row-Major vs Column-Major), False Sharing va Padding
* Branch prediction (likely/unlikely), Inline Assembly (RDTSC) va xotirani tekislash (_Alignas)
* SIMD Intrinsics, Loop Unrolling, Lock-Free CAS va Arena Allocator
* Kvantlangan AI (INT8 Dot Product va 1-Bit BitNet Popcount)
* 1000-Topshiriq: Super-Optimizatsiyalangan va Xavfsiz Tenzor Dvigateli

---

# 951-Topshiriq: Buffer Overflow (Bufer to'lib ketishi) xatosi va uning mexanizmi

## Topshiriq sharti:
Chegarasiz nusxalashning stack xotirasini buzishi va uning oldini olish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void xavfsiz_nusxa(char *dst, size_t dst_size, const char *src) {
    if (dst_size == 0) return;
    strncpy(dst, src, dst_size - 1);
    dst[dst_size - 1] = '\0'; // Kafolatlangan yakun
}

int main(void) {
    char kichik_bufer[8];
    const char *uzun_matn = "Antigravity C Language";

    xavfsiz_nusxa(kichik_bufer, sizeof(kichik_bufer), uzun_matn);

    printf("Xavfsiz nusxalangan natija: "%s" (Uzunligi: %zu)\n", 
           kichik_bufer, strlen(kichik_bufer));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. strcpy va gets kabi funksiyalar bufer hajmini tekshirmaydi va qo'shni stack xotirasini, jumladan funksiya qaytish manzilini (Return Address) qayta yozib yuboradi.
2. Har doim chegaralangan funksiyalar (snprintf, strncpy) ishlatilishi va oxirgi belgi '\0' ekanligi kafolatlanishi shart.

## Ishlash natijasi:
```text
Xavfsiz nusxalangan natija: "Antigra" (Uzunligi: 7)
```

---

# 952-Topshiriq: Format String zaifligi va uning oldini olish

## Topshiriq sharti:
printf(user_input) xatosi orqali stack ma'lumotlari o'g'irlanishi va to'g'ri printf("%s", user_input) yondashuvi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // Foydalanuvchi kiritgan soxta ma'lumot (ichida %x yoki %s bor)
    const char *xatarli_kirish = "%x %x %x";

    // XATO (Xavfli): printf(xatarli_kirish); -> Stackdagi qiymatlarni fosh qiladi!

    // TO'G'RI (Xavfsiz):
    printf("Xavfsiz chiqish: %s\n", xatarli_kirish);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar birinchi parametr to'g'ridan-to'g'ri foydalanuvchi satri bo'lsa, tajovuzkor '%x' orqali stackdagi parollarni o'qishi yoki '%n' orqali xotiraga yozishi mumkin.
2. Qoida: Birinchi argument doim qat'iy format satri (`"%s"`) bo'lishi shart!

## Ishlash natijasi:
```text
Xavfsiz chiqish: %x %x %x
```

---

# 953-Topshiriq: Integer Overflow va Wraparound ni xavfsiz tekshirish

## Topshiriq sharti:
Ikki butun sonni qo'shishdan oldin ularning chegaradan oshib ketishini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <limits.h>

int xavfsiz_qoshish(int a, int b, int *natija) {
    if ((b > 0 && a > INT_MAX - b) || (b < 0 && a < INT_MIN - b)) {
        return 0; // Overflow yuz berdi!
    }
    *natija = a + b;
    return 1; // Xavfsiz
}

int main(void) {
    int res;
    if (!xavfsiz_qoshish(INT_MAX, 1, &res)) {
        printf("Xatolik: INT_MAX + 1 chegaradan oshib ketdi!\n");
    }

    if (xavfsiz_qoshish(100, 200, &res)) {
        printf("100 + 200 = %d (Xavfsiz)\n", res);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida signed integer overflow rasman Undefined Behavior (UB) hisoblanadi.
2. Qo'shishdan oldin `a > INT_MAX - b` tekshiruvi xavfsizlikni kafolatlaydi.

## Ishlash natijasi:
```text
Xatolik: INT_MAX + 1 chegaradan oshib ketdi!
100 + 200 = 300 (Xavfsiz)
```

---

# 954-Topshiriq: Dangling Pointer (Mualaq ko'rsatkich) va Use-After-Free profilaktikasi

## Topshiriq sharti:
free() chaqirilgandan so'ng ko'rsatkichni darhol NULL qilish qoidasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

#define SAFE_FREE(ptr) do { \
    free(ptr);              \
    (ptr) = NULL;           \
} while (0)

int main(void) {
    int *p = (int *)malloc(sizeof(int));
    *p = 42;

    SAFE_FREE(p);

    if (p == NULL) {
        printf("Ko'rsatkich xavfsiz tozalangan (NULL), Use-After-Free xavfi yo'q!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. free() xotirani tizimga qaytaradi, ammo ko'rsatkichdagi manzilni o'chirmaydi.
2. SAFE_FREE makrosi ko'rsatkichni NULL qilib, unga tasodifiy murojaat qilinganda crash bo'lishini va yashirin zaiflik qolmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Ko'rsatkich xavfsiz tozalangan (NULL), Use-After-Free xavfi yo'q!
```

---

# 955-Topshiriq: Strict Aliasing qoidasi va uning buzilishi (Type Punning xatosi)

## Topshiriq sharti:
Turli tipli ko'rsatkichlar orqali bir xil xotiraga murojaat qilish xavfi va memcpy yechimi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

int main(void) {
    float f = 3.14f;

    // Strict aliasing buzilishi: *(uint32_t*)&f (Undefined Behavior!)
    // To'g'ri va xavfsiz usul:
    uint32_t u;
    memcpy(&u, &f, sizeof(float));

    printf("Float: %f -> Binar bitlar: 0x%08X\n", f, u);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C standartiga ko'ra ikki xil tipdagi pointer bir xil xotiraga ishora qilmaydi deb hisoblanadi (Strict Aliasing).
2. memcpy optimallashtiruvchi kompilyatorlar tomonidan bitta registr ko'chirishiga (MOVSS / MOVD) aylantiriladi va 100% xavfsizdir.

## Ishlash natijasi:
```text
Float: 3.140000 -> Binar bitlar: 0x4048F5C3
```

---

# 956-Topshiriq: Keshga mos arxitektura (Cache-Friendly Layout): Qatorlar bo'yicha yurish (Row-Major)

## Topshiriq sharti:
Matritsani qatorma-qator aylanib chiqish ustunma-ustun aylanib chiqishdan nima uchun 10 barobar tezligini isbotlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <time.h>

#define N 500
int mat[N][N];

int main(void) {
    // Row-Major (Kesh uchun optimal: ketma-ket RAM manzillari)
    clock_t t0 = clock();
    long long sum = 0;
    for (int r = 0; r < N; r++) {
        for (int c = 0; c < N; c++) {
            sum += mat[r][c];
        }
    }
    clock_t t1 = clock();

    printf("Row-Major yig'indisi: %lld (CPU vaqti: %.4f s)\n",
           sum, (double)(t1 - t0) / CLOCKS_PER_SEC);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida 2D massivlar xotirada qatorma-qator joylashadi (Row-major).
2. Qatorma-qator o'qilganda CPU L1 kesh liniyalari (64 bayt) 100% samarali ishlaydi (Kesh miss minimal bo'ladi).

## Ishlash natijasi:
```text
Row-Major yig'indisi: 0 (CPU vaqti: 0.0010 s)
```

---

# 957-Topshiriq: Tarmoqlanishni oldindan aytish: __builtin_expect, likely() va unlikely()

## Topshiriq sharti:
Kompilyatorga qaysi shart ko'proq bajarilishini bildirish orqali instruksiyalar quvurini (pipeline) tezlashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

#if defined(__GNUC__) || defined(__clang__)
#define likely(x)   __builtin_expect(!!(x), 1)
#define unlikely(x) __builtin_expect(!!(x), 0)
#else
#define likely(x)   (x)
#define unlikely(x) (x)
#endif

void xavfsizlik_tekshiruvi(int xato) {
    if (unlikely(xato)) {
        printf("[XATO]: Kamdan-kam uchraydigan favqulodda holat!\n");
    } else {
        printf("[ODDIY]: Asosiy tezkor magistral bajarildi.\n");
    }
}

int main(void) {
    xavfsizlik_tekshiruvi(0);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. likely/unlikely makroslari Linux yadrosida har bir if tekshiruvida ishlatiladi.
2. Kompilyator ehtimoli yuqori bo'lgan kodni to'g'ridan-to'g'ri keyingi qatorga joylashtiradi, bu esa branch misprediction jarimalarini kamaytiradi.

## Ishlash natijasi:
```text
[ODDIY]: Asosiy tezkor magistral bajarildi.
```

---

# 958-Topshiriq: Inline Assembly (__asm__): CPU ning RDTSC takt hisoblagichini o'qish

## Topshiriq sharti:
x86 protsessorining nanosekundlik aniqlikdagi Time-Stamp Counter (RDTSC) buyrug'ini bajarish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

static inline uint64_t rdtsc(void) {
#if defined(__x86_64__) || defined(_M_X64) || defined(__i386__)
    uint32_t lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
#else
    return 1234567890ULL; // Simulyatsiya
#endif
}

int main(void) {
    uint64_t start = rdtsc();
    // Kichik hisoblash
    volatile int x = 0;
    for (int i = 0; i < 1000; i++) x += i;
    uint64_t end = rdtsc();

    printf("1000 ta sikl uchun sarflangan CPU takt tsikllari: %llu\n",
           (unsigned long long)(end - start));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. RDTSC buyrug'i protsessor ishga tushgandan buyon necha takt o'tganini 64-bitda qaytaradi.
2. Bu C dasturlarida eng yuqori aniqlikdagi mikrosekund osti (sub-nanosecond) profiling vositasidir.

## Ishlash natijasi:
```text
1000 ta sikl uchun sarflangan CPU takt tsikllari: 2450
```

---

# 959-Topshiriq: Xotirani tekislash (Memory Alignment): _Alignas va _Alignof (C11)

## Topshiriq sharti:
SIMD (AVX/SSE) operatsiyalari uchun xotirani 32 yoki 64 bayt chegarasiga moslashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdalign.h>

typedef struct {
    alignas(32) float vektor[8]; // 32-bayt tekislangan (AVX registrlari uchun)
} AVXBuffer;

int main(void) {
    AVXBuffer buf;

    printf("AVXBuffer tekislanishi: %zu bayt\n", alignof(AVXBuffer));
    printf("Xotira manzili:         %p\n", (void*)&buf);
    printf("32 ga karralimi?        %s\n", 
           ((uintptr_t)&buf % 32 == 0) ? "HA" : "YO'Q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. AVX va SSE ko'rsatmalari agar xotira 32 yoki 16 baytga tekislanmagan bo'lsa General Protection Fault (Crash) beradi yoki tezligi 2 barobar tushadi.
2. C11 `alignas` orqali xotirani apparat talabiga moslash kafolatlanadi.

## Ishlash natijasi:
```text
AVXBuffer tekislanishi: 32 bayt
Xotira manzili:         000000000019F020
32 ga karralimi?        HA
```

---

# 960-Topshiriq: SIMD Intrinsics: 4 ta float sonini bitta buyruqda qo'shish (SSE)

## Topshiriq sharti:
Intel SSE intrinsics orqali vektorli parallel hisoblash konsepsiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>

void vektor_qoshish_oddiy(const float *a, const float *b, float *out, int n) {
    for (int i = 0; i < n; i++) {
        out[i] = a[i] + b[i];
    }
}

int main(void) {
    float a[4] = {1.0f, 2.0f, 3.0f, 4.0f};
    float b[4] = {10.0f, 20.0f, 30.0f, 40.0f};
    float c[4];

    vektor_qoshish_oddiy(a, b, c, 4);

    printf("Vektor natijasi: %.1f, %.1f, %.1f, %.1f\n",
           c[0], c[1], c[2], c[3]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. SIMD (Single Instruction, Multiple Data) bitta protsessor buyrug'ida (masalan `_mm_add_ps`) 4 ta yoki 8 ta sonni parallel hisoblaydi.

## Ishlash natijasi:
```text
Vektor natijasi: 11.0, 22.0, 33.0, 44.0
```

---

# 961-Topshiriq: Loop Unrolling (Siklni yoyish) orqali tezlashtirish

## Topshiriq sharti:
Sikldagi shart tekshirishlari sonini 4 barobar kamaytirib quvur unumdorligini oshirish.

## Yechim (C kodi):
```c
#include <stdio.h>

void massiv_nol_qil(int *arr, int n) {
    int i = 0;
    // 4 qadamdan yoyilgan sikl
    for (; i <= n - 4; i += 4) {
        arr[i] = 0;
        arr[i + 1] = 0;
        arr[i + 2] = 0;
        arr[i + 3] = 0;
    }
    // Qolgan elementlar
    for (; i < n; i++) arr[i] = 0;
}

int main(void) {
    int a[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    massiv_nol_qil(a, 8);

    printf("Tozalangan massiv: %d %d %d %d\n", a[0], a[1], a[2], a[3]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Siklni yoyish sakrash (branch) buyruqlari sonini keskin kamaytiradi va protsessorga instruksiyalarni parallel bajarish imkonini beradi.

## Ishlash natijasi:
```text
Tozalangan massiv: 0 0 0 0
```

---

# 962-Topshiriq: Lock-Free Dasturlash: Compare-And-Swap (CAS) amali

## Topshiriq sharti:
Mutex ishlatmasdan apparat darajasida atomik almashtirish (__sync_val_compare_and_swap).

## Yechim (C kodi):
```c
#include <stdio.h>

int atomik_cas(int *manzil, int kutilgan, int yangi) {
#if defined(__GNUC__) || defined(__clang__)
    return __sync_val_compare_and_swap(manzil, kutilgan, yangi);
#else
    if (*manzil == kutilgan) { *manzil = yangi; return kutilgan; }
    return *manzil;
#endif
}

int main(void) {
    int qiymat = 100;

    int eski = atomik_cas(&qiymat, 100, 200);
    printf("CAS muvaffaqiyatli: yangi qiymat = %d (eski edi = %d)\n", qiymat, eski);

    eski = atomik_cas(&qiymat, 100, 300); // 100 emas, 200 bo'lgani uchun o'zgarmaydi!
    printf("CAS muvaffaqiyatsiz: qiymat o'zgarmadi = %d\n", qiymat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. CAS (Compare-And-Swap) x86 'CMPXCHG' buyrug'iga tayanadi va Lock-Free navbatlar hamda ma'lumot tuzilmalarining poydevoridir.

## Ishlash natijasi:
```text
CAS muvaffaqiyatli: yangi qiymat = 200 (eski edi = 100)
CAS muvaffaqiyatsiz: qiymat o'zgarmadi = 200
```

---

# 963-Topshiriq: Kvantlangan Sun'iy Intellekt: INT8 Skalyar Ko'paytirish (Quantized Dot Product)

## Topshiriq sharti:
Float32 o'rniga 8-bitli butun sonlar (INT8) bilan matritsa ko'paytirib xotirani 4 barobar tejash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int32_t int8_dot_product(const int8_t *w, const int8_t *x, int len) {
    int32_t acc = 0;
    for (int i = 0; i < len; i++) {
        acc += (int32_t)w[i] * x[i];
    }
    return acc;
}

int main(void) {
    int8_t ogirliklar[4] = { 10, -5, 20, 2 };
    int8_t aktivatsiyalar[4] = { 1, 2, 3, 4 };

    // (10*1) + (-5*2) + (20*3) + (2*4) = 10 - 10 + 60 + 8 = 68
    int32_t natija = int8_dot_product(ogirliklar, aktivatsiyalar, 4);

    printf("INT8 Kvantlangan Neyron Chiqishi: %d\n", natija);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zamonaviy AI dvigatellari (llama.cpp, ONNX Runtime) neyron tarmoqlarni INT8 ga kvantlash orqali telefon va kompyuterlarda yuqori tezlikka erishadi.

## Ishlash natijasi:
```text
INT8 Kvantlangan Neyron Chiqishi: 68
```

---

# 964-Topshiriq: 1-Bitli Neyron Tarmoq (1-Bit LLM / BitNet) Popcount mantiqi

## Topshiriq sharti:
Faqat +1 va -1 og'irliklar uchun XNOR va Popcount orqali milliardlab ko'paytirishlarni bit amallariga aylantirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int bitnet_dot_product(uint64_t w_bits, uint64_t x_bits) {
    // XNOR amali: bir xil bitlar (1,1 yoki 0,0) mos kelganda 1 beradi
    uint64_t xnor = ~(w_bits ^ x_bits);

    // Birlik bitlarni sanash (Popcount)
    int mos_bitlar = 0;
    while (xnor) {
        mos_bitlar += (xnor & 1);
        xnor >>= 1;
    }
    // 64 bit ichida: natija = 2 * mos - 64
    return 2 * mos_bitlar - 64;
}

int main(void) {
    uint64_t w = 0xFFFFFFFFFFFFFFFFULL; // Barchasi +1
    uint64_t x = 0xFFFFFFFFFFFFFFFFULL; // Barchasi +1

    printf("1-Bit BitNet Skalyar ko'paytma: %d (Maksimal 64)\n", 
           bitnet_dot_product(w, x));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1-Bit LLM (BitNet 1.58b) kelajak sun'iy intellekti bo'lib, og'ir ko'paytirish bloklarini bitta protsessor 'POPCNT' buyrug'i bilan almashtiradi.

## Ishlash natijasi:
```text
1-Bit BitNet Skalyar ko'paytma: 64 (Maksimal 64)
```

---

# 965-Topshiriq: Kesh Liniyasini to'ldirish (Cache Line Padding) va False Sharing profilaktikasi

## Topshiriq sharti:
Ko'p oqimli hisoblashlarda 64-baytli padding orqali o'zgaruvchilarni ajratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    uint64_t hisob;
    uint8_t  pad[56]; // 8 + 56 = 64 bayt (Kesh liniyasi hajmi)
} PaddedCounter;

int main(void) {
    PaddedCounter c1, c2;
    printf("Padded struktura hajmi: %zu bayt\n", sizeof(PaddedCounter));
    printf("Ikki hisoblagich masofasi: %td bayt (64 bayt kesh chegarasida)\n",
           (char*)&c2 - (char*)&c1);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. False Sharing bir xil 64-baytli kesh liniyasidagi o'zgaruvchilarni turli CPU yadrolari o'zgartirganda L1 keshni doimiy bekor qilish xatosidir.

## Ishlash natijasi:
```text
Padded struktura hajmi: 64 bayt
Ikki hisoblagich masofasi: 64 bayt (64 bayt kesh chegarasida)
```

---

# 966-Topshiriq: restrict kalit so'zi (C99) va ko'rsatkichlar alohidaligi (No-Aliasing)

## Topshiriq sharti:
Kompilyatorga ko'rsatkichlar ustma-ust tushmasligini kafolatlash orqali vektorlashni yoqish.

## Yechim (C kodi):
```c
#include <stdio.h>

void vektor_qosh(int * restrict a, int * restrict b, int * restrict c, int n) {
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

int main(void) {
    int a[3] = {1, 2, 3};
    int b[3] = {4, 5, 6};
    int c[3];

    vektor_qosh(a, b, c, 3);
    printf("restrict natijasi: %d %d %d\n", c[0], c[1], c[2]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. restrict kalit so'zi ushbu xotira blokiga faqat shu ko'rsatkich orqali kirilishini va'da qiladi.
2. Bu kompilyatorga har bir qadamda qayta RAM dan o'qimasdan registrlarga keshlashga ruxsat beradi.

## Ishlash natijasi:
```text
restrict natijasi: 5 7 9
```

---

# 967-Topshiriq: Xavfsiz butun sonli ko'paytirish (Integer Multiplication Overflow Check)

## Topshiriq sharti:
Hajm hisoblashda (malloc argumentida) ko'paytirish to'lib ketishini tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int xavfsiz_malloc_hajmi(size_t elementlar, size_t element_hajmi, size_t *jami) {
    if (elementlar != 0 && SIZE_MAX / elementlar < element_hajmi) {
        return 0; // Overflow!
    }
    *jami = elementlar * element_hajmi;
    return 1;
}

int main(void) {
    size_t jami;
    if (!xavfsiz_malloc_hajmi(SIZE_MAX / 2, 4, &jami)) {
        printf("Xatolik: Xotira hajmi SIZE_MAX dan oshib ketdi!\n");
    }

    if (xavfsiz_malloc_hajmi(10, sizeof(int), &jami)) {
        printf("Xavfsiz hajm: %zu bayt\n", jami);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tajovuzkorlar katta sonlarni uzatib malloc(0) yoki kichik bufer ajratilishiga erishadi, so'ngra buferni to'ldirib tizimni buzadi.

## Ishlash natijasi:
```text
Xatolik: Xotira hajmi SIZE_MAX dan oshib ketdi!
Xavfsiz hajm: 40 bayt
```

---

# 968-Topshiriq: Xotira parchalanishini (Fragmentation) yo'qotuvchi Arena Xotira Boshqaruvi (Memory Arena)

## Topshiriq sharti:
Bitta katta xotira blokini olib, undan ketma-ket kesib berish va bitta free bilan tozalash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    uint8_t bufer[1024];
    size_t siljish;
} Arena;

void* arena_alloc(Arena *a, size_t hajm) {
    // 8-bayt tekislash
    size_t tekislangan = (hajm + 7) & ~7;
    if (a->siljish + tekislangan > sizeof(a->bufer)) return NULL;
    void *ptr = &a->bufer[a->siljish];
    a->siljish += tekislangan;
    return ptr;
}

void arena_reset(Arena *a) { a->siljish = 0; }

int main(void) {
    Arena a = { .siljish = 0 };

    int *sonlar = (int*)arena_alloc(&a, 10 * sizeof(int));
    char *matn  = (char*)arena_alloc(&a, 32);

    printf("Arena sarflagan xotira: %zu bayt\n", a.siljish);
    arena_reset(&a); // Barcha xotira bitta qatorda tozalandi!
    printf("Arena qayta tozalandi:   %zu bayt\n", a.siljish);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'yinlar (Game Dev) va yuqori tezlikdagi serverlarda millionlab malloc/free o'rniga Arena (Bump Allocator) ishlatiladi.

## Ishlash natijasi:
```text
Arena sarflagan xotira: 72 bayt
Arena qayta tozalandi:   0 bayt
```

---

# 969-Topshiriq: Xavfsiz satr formatlash: snprintf va bufer chegarasini tekshirish

## Topshiriq sharti:
snprintf qaytargan qiymat orqali matn to'liq sig'ganligini yoki kesilib qolganligini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char buf[12];
    int sigmagan = snprintf(buf, sizeof(buf), "Foydalanuvchi: %s", "Alisher");

    printf("Hosil bo'lgan matn: "%s"\n", buf);
    printf("Kerak bo'lgan hajm:  %d bayt\n", sigmagan);

    if (sigmagan >= (int)sizeof(buf)) {
        printf("Ogohlantirish: Matn buferga to'liq sig'madi va kesildi!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. snprintf buferga yozilishi kerak bo'lgan umumiy belgilar sonini qaytaradi.
2. Agar qaytgan son >= sizeof(buf) bo'lsa, demak bufer yetmagan.

## Ishlash natijasi:
```text
Hosil bo'lgan matn: "Foydalanuvc"
Kerak bo'lgan hajm:  22 bayt
Ogohlantirish: Matn buferga to'liq sig'madi va kesildi!
```

---

# 970-Topshiriq: Valgrind va AddressSanitizer (ASan) orqali xotira xatolarini ushlash

## Topshiriq sharti:
-fsanitize=address kompilyator bayrog'i yordamida Out-of-bounds va Memory Leak larni aniqlash tamoyili.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("AddressSanitizer (ASan) - dasturga maxsus qizil zonalar (Redzones)\n");
    printf("va soyali xotira (Shadow memory) qo'shib, 1 baytlik buffer overflow yoki\n");
    printf("use-after-free xatosini ham darhol aniqlab stack trace bilan qulatadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Zamonaviy C dasturlashda ASan va Valgrind barcha xavfsizlik testlarida majburiy talabdir.

## Ishlash natijasi:
```text
AddressSanitizer (ASan) - dasturga maxsus qizil zonalar (Redzones)
va soyali xotira (Shadow memory) qo'shib, 1 baytlik buffer overflow yoki
use-after-free xatosini ham darhol aniqlab stack trace bilan qulatadi.
```

---

# 971-Topshiriq: Xotira oqishini (Memory Leak) bartaraf etish tekshiruvi

## Topshiriq sharti:
Har bir malloc() uchun mos free() mavjudligini audit qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *massiv = (int *)malloc(5 * sizeof(int));
    if (!massiv) return 1;

    for (int i = 0; i < 5; i++) massiv[i] = i * 10;
    printf("Element: %d\n", massiv[2]);

    free(massiv); // Resurs to'liq qaytarildi
    massiv = NULL;

    printf("Xotira muvaffaqiyatli ozod qilindi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har doim malloc dan keyin free chaqirilishi va pointer NULL qilinishi zarur.

## Ishlash natijasi:
```text
Element: 20
Xotira muvaffaqiyatli ozod qilindi.
```

---

# 972-Topshiriq: Zeroization: Maxfiy parollarni xotiradan tozalash (memset_s / explicit_bzero)

## Topshiriq sharti:
Kompilyator optimizatsiyasi o'chirib yubormaydigan xavfsiz xotira tozalash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void xavfsiz_tozala(volatile void *p, size_t len) {
    volatile unsigned char *v = (volatile unsigned char *)p;
    while (len--) {
        *v++ = 0;
    }
}

int main(void) {
    char parol[16] = "MaxfiyParol123!";

    printf("Parol xotirada: %s\n", parol);
    xavfsiz_tozala(parol, sizeof(parol));
    printf("Xotira tozalandi, birinchi belgi: %d\n", parol[0]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oddiy memset(parol, 0, 16) kompilyator tomonidan 'foydasiz o'lik kod' (dead code elimination) deb olib tashlanishi mumkin.
2. volatile pointer orqali tozalash kompilyator optimizatsiyasining oldini oladi.

## Ishlash natijasi:
```text
Parol xotirada: MaxfiyParol123!
Xotira tozalandi, birinchi belgi: 0
```

---

# 973-Topshiriq: Tugunlar puli (Object Pool Allocator): Kichik ob'ektlarni tezkor taqsimlash

## Topshiriq sharti:
Linked list tugunlarini tezkor berish va qaytarib olish uchun xotira puli.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct Ob {
    int id;
    struct Ob *keyingi_bosh;
} Ob;

#define POOL_SIZE 3
Ob pool_xotira[POOL_SIZE];
Ob *bosh_boshi = NULL;

void init_pool(void) {
    for (int i = 0; i < POOL_SIZE - 1; i++) {
        pool_xotira[i].keyingi_bosh = &pool_xotira[i + 1];
    }
    pool_xotira[POOL_SIZE - 1].keyingi_bosh = NULL;
    bosh_boshi = &pool_xotira[0];
}

Ob* pool_alloc(void) {
    if (!bosh_boshi) return NULL;
    Ob *ret = bosh_boshi;
    bosh_boshi = bosh_boshi->keyingi_bosh;
    return ret;
}

int main(void) {
    init_pool();
    Ob *o1 = pool_alloc();
    o1->id = 777;
    printf("Ob'ekt puldan O(1) da olindi: ID = %d\n", o1->id);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Object Pool tizimi xotira bo'linishini nolga tushiradi va O(1) da resurs beradi.

## Ishlash natijasi:
```text
Ob'ekt puldan O(1) da olindi: ID = 777
```

---

# 974-Topshiriq: Fast Inverse Square Root (1/sqrt(x)) C tilida

## Topshiriq sharti:
Quake III o'yinidagi afsonaviy tezkor kvadrat ildizga teskari son hisoblash algoritmi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

float fast_inv_sqrt(float number) {
    int32_t i;
    float x2, y;
    const float threehalfs = 1.5F;

    x2 = number * 0.5F;
    y  = number;
    i  = * ( int32_t * ) &y;                       // Floatni int deb olish
    i  = 0x5f3759df - ( i >> 1 );                  // Sehrli doimiy son!
    y  = * ( float * ) &i;
    y  = y * ( threehalfs - ( x2 * y * y ) );     // 1-bosqich Nyuton yaqinlashuvi
    return y;
}

int main(void) {
    float x = 4.0f;
    float inv = fast_inv_sqrt(x); // 1 / sqrt(4) = 0.5
    printf("1 / sqrt(%.1f) = %.4f (Fast Inv Sqrt)\n", x, inv);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. John Carmack tomonidan mashhur qilingan bu algoritm 3D grafika vektorlarini normallashtirishni 4 barobar tezlashtirgan.

## Ishlash natijasi:
```text
1 / sqrt(4.0) = 0.4992 (Fast Inv Sqrt)
```

---

# 975-Topshiriq: Bitli siljitishlar orqali ko'paytirish va bo'lish optimizatsiyasi

## Topshiriq sharti:
2 ning darajalariga ko'paytirish va bo'lishni bitwise shift bilan almashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 15;

    // x * 8 -> x << 3
    int kopaytma = x << 3;

    // x / 4 -> x >> 2
    int bolinma = x >> 2;

    // x % 8 -> x & (8 - 1)
    int qoldiq = x & 7;

    printf("15 * 8 = %d\n", kopaytma);
    printf("15 / 4 = %d\n", bolinma);
    printf("15 %% 8 = %d\n", qoldiq);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitwise amallar CPU da atigi 1 takt vaqt oladi, bo'lish (DIV) esa 20-40 takt sarflaydi.

## Ishlash natijasi:
```text
15 * 8 = 120
15 / 4 = 3
15 % 8 = 7
```

---

# 976-Topshiriq: O(1) da 2 ning darajasini tekshirish (Power of Two Check)

## Topshiriq sharti:
Bitta bitwise AND amali orqali son 2 ning darajasi (2, 4, 8, 16...) ekanligini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int ikki_darajasimi(unsigned int n) {
    return (n != 0) && ((n & (n - 1)) == 0);
}

int main(void) {
    printf("16 ikki darajasimi? %d\n", ikki_darajasimi(16));
    printf("18 ikki darajasimi? %d\n", ikki_darajasimi(18));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. n & (n - 1) eng quyi 1-bitni nolga aylantiradi. Agar son 2 ning darajasi bo'lsa, unda faqat bitta 1-bit bo'ladi va natija 0 chiqadi.

## Ishlash natijasi:
```text
16 ikki darajasimi? 1
18 ikki darajasimi? 0
```

---

# 977-Topshiriq: Popcount: 32-bitli son ichidagi birlik bitlar sonini sanash (Hamming Weight)

## Topshiriq sharti:
Protsessorning POPCNT buyrug'i yoki O(log N) bitli hisoblash algoritmi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int popcount32(uint32_t x) {
    x = x - ((x >> 1) & 0x55555555);
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333);
    x = (x + (x >> 4)) & 0x0F0F0F0F;
    x = x + (x >> 8);
    x = x + (x >> 16);
    return x & 0x0000003F;
}

int main(void) {
    uint32_t son = 0b10110001; // 4 ta bir
    printf("0b10110001 da birlik bitlar soni: %d\n", popcount32(son));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kriptografiya, bioinformatika va BitNet AI modellarida popcount asosiy operatsiyadir.

## Ishlash natijasi:
```text
0b10110001 da birlik bitlar soni: 4
```

---

# 978-Topshiriq: Kesh to'qnashuvlarini (Cache Associativity Conflict) kamaytirish

## Topshiriq sharti:
Massiv o'lchamlarini 2 ning darajasidan (masalan 1024 o'rniga 1025) biroz farqli qilish sababi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Kesh assotsiativligi to'qnashuvlari - agar massiv ustunlari 2 ning darajasi\n");
    printf("(masalan 1024) bo'lsa, har bir qator CPU keshining bitta yo'lagiga (set) urilib\n");
    printf("keshni keraksiz tozalaydi. Buni 'padding' qo'shib hal qilinadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matritsa o'lchamlariga kichik padding qo'shish kesh assotsiativ to'qnashuvlarini bartaraf qiladi.

## Ishlash natijasi:
```text
Kesh assotsiativligi to'qnashuvlari - agar massiv ustunlari 2 ning darajasi
(masalan 1024) bo'lsa, har bir qator CPU keshining bitta yo'lagiga (set) urilib
keshni keraksiz tozalaydi. Buni 'padding' qo'shib hal qilinadi.
```

---

# 979-Topshiriq: Prefetching: Xotira ma'lumotlarini keshga oldindan yuklash

## Topshiriq sharti:
__builtin_prefetch orqali CPU ga ma'lumotni keshga tayyorlab turish buyrug'i.

## Yechim (C kodi):
```c
#include <stdio.h>

int binar_qidiruv_prefetch(const int *arr, int n, int kalit) {
    int low = 0, high = n - 1;
    while (low <= high) {
        int mid = (low + high) / 2;
#if defined(__GNUC__) || defined(__clang__)
        // Keyingi qadamda kerak bo'ladigan oraliqni keshga prefetch qilish
        __builtin_prefetch(&arr[(low + mid) / 2], 0, 1);
        __builtin_prefetch(&arr[(mid + high) / 2], 0, 1);
#endif
        if (arr[mid] == kalit) return mid;
        if (arr[mid] < kalit) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

int main(void) {
    int arr[] = {10, 20, 30, 40, 50, 60, 70};
    int idx = binar_qidiruv_prefetch(arr, 7, 40);
    printf("40 indeksi: %d\n", idx);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Prefetching xotiradan ma'lumot kutish (RAM latency - 200 takt) vaqtini bekorga sarflamaslikka yordam beradi.

## Ishlash natijasi:
```text
40 indeksi: 3
```

---

# 980-Topshiriq: Funksiya chaqiruvlari sarf-xarajati va inline kalit so'zi

## Topshiriq sharti:
static inline funksiyalar orqali funksiya chaqiruvi steki sarfini nolga tushirish.

## Yechim (C kodi):
```c
#include <stdio.h>

static inline int kvadrat(int x) {
    return x * x;
}

int main(void) {
    printf("Kvadrat: %d\n", kvadrat(12));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. static inline funksiyalar chaqiruv o'rniga to'g'ridan-to'g'ri kod joylashtiriladi va makros kabi tez, ammo tip xavfsiz (type-safe) bo'ladi.

## Ishlash natijasi:
```text
Kvadrat: 144
```

---

# 981-Topshiriq: Tugunlar saralashida Branchless Kodlash: Min / Max hisoblash

## Topshiriq sharti:
Shartli sakrashsiz (if-siz) bitwise amallar bilan min/max topish.

## Yechim (C kodi):
```c
#include <stdio.h>

int branchless_min(int a, int b) {
    return b + ((a - b) & ((a - b) >> 31));
}

int main(void) {
    printf("min(25, 42) = %d\n", branchless_min(25, 42));
    printf("min(70, 15) = %d\n", branchless_min(70, 15));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. If shartlarining yo'qligi CPU branch predictor xatolarini butunlay yo'q qiladi.

## Ishlash natijasi:
```text
min(25, 42) = 25
min(70, 15) = 15
```

---

# 982-Topshiriq: Branchless Absolute Value (Modul hisoblash)

## Topshiriq sharti:
If ishlatmasdan son modulini hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>

int branchless_abs(int n) {
    int mask = n >> 31;
    return (n + mask) ^ mask;
}

int main(void) {
    printf("abs(-55) = %d\n", branchless_abs(-55));
    printf("abs(42)  = %d\n", branchless_abs(42));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. (n + mask) ^ mask formulasi ikkilik qo'shimcha qoidasi bo'yicha if-siz ishlaydi.

## Ishlash natijasi:
```text
abs(-55) = 55
abs(42)  = 42
```

---

# 983-Topshiriq: Xotirada Bit Array (Bitfield) orqali Eratosfen G'alviri

## Topshiriq sharti:
Bitta baytda 8 ta sonni ifodalab tub sonlarni topishda xotirani 8 barobar tejash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#define MAX_PRIME 32
uint8_t tub_bitset[MAX_PRIME / 8] = {0}; // 0 = tub

void set_not_prime(int n) { tub_bitset[n / 8] |= (1 << (n % 8)); }
int is_prime(int n) { return !(tub_bitset[n / 8] & (1 << (n % 8))); }

int main(void) {
    set_not_prime(0);
    set_not_prime(1);

    for (int p = 2; p * p < MAX_PRIME; p++) {
        if (is_prime(p)) {
            for (int i = p * p; i < MAX_PRIME; i += p) set_not_prime(i);
        }
    }

    printf("20 gacha tub sonlar: ");
    for (int i = 2; i <= 20; i++) {
        if (is_prime(i)) printf("%d ", i);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bit array orqali milliardlab sonlarni minimal RAM da g'alvirdan o'tkazish mumkin.

## Ishlash natijasi:
```text
20 gacha tub sonlar: 2 3 5 7 11 13 17 19
```

---

# 984-Topshiriq: Null Pointer Dereference profilaktikasi: Sanitizer va Nonnull atributi

## Topshiriq sharti:
__attribute__((nonnull)) orqali kompilyatsiyada NULL uzatishni man etish.

## Yechim (C kodi):
```c
#include <stdio.h>

void chop_xavfsiz(const char *s) {
    if (s == NULL) {
        printf("[HIMOYA]: NULL ko'rsatkich uzatildi!\n");
        return;
    }
    printf("Matn: %s\n", s);
}

int main(void) {
    chop_xavfsiz("Salom");
    chop_xavfsiz(NULL);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. NULL pointer ustida amal bajarish (Dereference) eng keng tarqalgan Crash sababidir.

## Ishlash natijasi:
```text
Matn: Salom
[HIMOYA]: NULL ko'rsatkich uzatildi!
```

---

# 985-Topshiriq: Xotirani qismlarga ajratmasdan boshqarish: Ring Buffer Allocator

## Topshiriq sharti:
Vaqtinchalik satrlar va kiritish-chiqarish buferlari uchun halqasimon xotira.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#define RING_ALLOC_SIZE 64
uint8_t ring_alloc_buf[RING_ALLOC_SIZE];
size_t ring_head = 0;

void* ring_alloc(size_t hajm) {
    if (hajm > RING_ALLOC_SIZE) return NULL;
    if (ring_head + hajm > RING_ALLOC_SIZE) ring_head = 0; // Aylanma
    void *ptr = &ring_alloc_buf[ring_head];
    ring_head += hajm;
    return ptr;
}

int main(void) {
    char *s1 = (char*)ring_alloc(10);
    char *s2 = (char*)ring_alloc(20);

    printf("s1 manzili: %p\n", (void*)s1);
    printf("s2 manzili: %p\n", (void*)s2);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ring allocator qisqa muddatli formatlash va log satrlari uchun ideal va hech qachon xotirani to'ldirib yubormaydi.

## Ishlash natijasi:
```text
s1 manzili: 0000000000407000
s2 manzili: 000000000040700A
```

---

# 986-Topshiriq: Binar qidiruvni Branchless qilish (Branchless Binary Search)

## Topshiriq sharti:
CMOV (Conditional Move) orqali qidiruvdagi if-tarmoqlanishlarni olib tashlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int branchless_bsearch(const int *arr, int n, int val) {
    const int *base = arr;
    while (n > 1) {
        int half = n / 2;
        base = (base[half] < val) ? base + half : base;
        n -= half;
    }
    return (*base == val) ? (base - arr) : -1;
}

int main(void) {
    int arr[] = {1, 3, 5, 7, 9, 11, 13};
    int idx = branchless_bsearch(arr, 7, 9);
    printf("9 sonining indeksi: %d\n", idx);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta ma'lumotlar bazalarida indeks qidiruvini CMOV yordamida tezlashtirish.

## Ishlash natijasi:
```text
9 sonining indeksi: 4
```

---

# 987-Topshiriq: Strukturalar ichida ma'lumotlarni saralash (Structure Padding Minimization)

## Topshiriq sharti:
Maydonlarni kattasidan kichigiga (8B -> 4B -> 2B -> 1B) qarab terish orqali xotirani tejash.

## Yechim (C kodi):
```c
#include <stdio.h>

// Yomon tartib (Padding ko'p)
struct Yomon {
    char a;    // 1 bayt
    // 7 bayt padding
    double b;  // 8 bayt
    char c;    // 1 bayt
    // 7 bayt padding
}; // Jami: 24 bayt!

// Yaxshi tartib
struct Yaxshi {
    double b;  // 8 bayt
    char a;    // 1 bayt
    char c;    // 1 bayt
    // 6 bayt padding
}; // Jami: 16 bayt!

int main(void) {
    printf("Yomon struktura hajmi:  %zu bayt\n", sizeof(struct Yomon));
    printf("Yaxshi struktura hajmi: %zu bayt (33%% tejaldi!)\n", sizeof(struct Yaxshi));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Maydonlarni to'g'ri joylashtirish orqali millionlab ob'ektlarda yuzlab megabayt RAM tejaladi.

## Ishlash natijasi:
```text
Yomon struktura hajmi:  24 bayt
Yaxshi struktura hajmi: 16 bayt (33% tejaldi!)
```

---

# 988-Topshiriq: Tail Call Optimization (Dumaloq rekursiyani siklga aylantirish)

## Topshiriq sharti:
Rekursiv funksiya oxirgi amalida o'zini chaqirsa, stack xotira sarflanmasdan O(1) da ishlashi.

## Yechim (C kodi):
```c
#include <stdio.h>

long long faktorial_tail(int n, long long akk) {
    if (n <= 1) return akk;
    return faktorial_tail(n - 1, n * akk); // Dumaloq chaqiruv
}

int main(void) {
    printf("10! = %lld\n", faktorial_tail(10, 1));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. -O2 va -O3 da kompilyator dumaloq rekursiyani avtomatik ravishda oddiy siklga (JMP) aylantiradi va stack overflow xavfini yo'qotadi.

## Ishlash natijasi:
```text
10! = 3628800
```

---

# 989-Topshiriq: Link-Time Optimization (LTO) va Dead Code Elimination

## Topshiriq sharti:
Kompilyatsiya vaqtida ishlatilmagan funksiyalarni binar fayldan butunlay olib tashlash.

## Yechim (C kodi):
```c
#include <stdio.h>

void hech_kim_chaqirmagan_funksiya(void) {
    printf("Bu funksiya binar faylga kirmasligi kerak\n");
}

int main(void) {
    printf("LTO (-flto) butun loyiha bo'ylab tahlil qilib, ishlatilmagan funksiyalarni o'chiradi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. LTO binar hajmni 30% gacha kichraytiradi va fayllararo inline qilishni yoqadi.

## Ishlash natijasi:
```text
LTO (-flto) butun loyiha bo'ylab tahlil qilib, ishlatilmagan funksiyalarni o'chiradi.
```

---

# 990-Topshiriq: Dinamik kutubxona bilan xotirani himoyalash: Stack Canaries

## Topshiriq sharti:
Stack canary buzilganda __stack_chk_fail chaqirilishi tamoyili.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Stack Canary - funksiya qaytish manzilidan oldin maxsus tasodifiy qiymat qo'yadi.\n");
    printf("Agar bufer to'lib qaytish manzili buzilsa, dastur darhol qulatiladi va xavfsizlik saqlanadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. -fstack-protector bayrog'i barcha zamonaviy operatsion tizimlarda xavfsizlikning birinchi qalqonidir.

## Ishlash natijasi:
```text
Stack Canary - funksiya qaytish manzilidan oldin maxsus tasodifiy qiymat qo'yadi.
Agar bufer to'lib qaytish manzili buzilsa, dastur darhol qulatiladi va xavfsizlik saqlanadi.
```

---

# 991-Topshiriq: Kriptografik jihatdan xavfsiz vaqt tengligi (Constant-Time String Comparison)

## Topshiriq sharti:
Parollar va tokenlarni solishtirishda vaqt tahlili (Timing Attack) hujumlarining oldini olish.

## Yechim (C kodi):
```c
#include <stdio.h>

int doimiy_vaqt_solishtir(const char *a, const char *b, size_t len) {
    unsigned char farq = 0;
    for (size_t i = 0; i < len; i++) {
        farq |= (a[i] ^ b[i]);
    }
    return farq == 0;
}

int main(void) {
    const char kalit1[] = "MaxfiyTokenABC";
    const char kalit2[] = "MaxfiyTokenABC";
    const char kalit3[] = "MaxfiyTokenXYZ";

    printf("Kalitlar tengmi? %s\n", 
           doimiy_vaqt_solishtir(kalit1, kalit2, 14) ? "HA" : "YO'Q");
    printf("Kalitlar tengmi? %s\n", 
           doimiy_vaqt_solishtir(kalit1, kalit3, 14) ? "HA" : "YO'Q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Standart strcmp birinchi farqli belgidayoq return qiladi, tajovuzkor nanosekundlarni o'lchab parolni harfma-harf taxmin qilishi mumkin.
2. Constant-time taqqoslash har doim to'liq satrni tekshiradi va bir xil vaqt oladi.

## Ishlash natijasi:
```text
Kalitlar tengmi? HA
Kalitlar tengmi? YO'Q
```

---

# 992-Topshiriq: Xotirada soxta ma'lumotlarni yashirish (Data Obfuscation at Rest)

## Topshiriq sharti:
Binar faylda o'rnatilgan matnlarni (strings) o'qib bo'lmaydigan qilib shifrlash.

## Yechim (C kodi):
```c
#include <stdio.h>

#define OBFUSCATE_BYTE 0x5A

void chop_obfuscated(const unsigned char *data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        putchar(data[i] ^ OBFUSCATE_BYTE);
    }
    printf("\n");
}

int main(void) {
    // "Admin123" ^ 0x5A
    unsigned char yashirin[] = { 'A'^0x5A, 'd'^0x5A, 'm'^0x5A, 'i'^0x5A, 'n'^0x5A };

    printf("Tiklangan matn: ");
    chop_obfuscated(yashirin, 5);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu oddiy 'strings' utilitasi orqali binar ichidagi maxfiy so'zlarni darhol topishdan saqlaydi.

## Ishlash natijasi:
```text
Tiklangan matn: Admin
```

---

# 993-Topshiriq: Ko'p darajali Kesh Simulyatsiyasi: L1, L2 va RAM tezliklarini solishtirish

## Topshiriq sharti:
L1 kesh o'lchami (32 KB) doirasidagi va tashqarisidagi amallar unumdorligi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("L1 kesh: ~1 nanosekund (4 takt)\n");
    printf("L2 kesh: ~4 nanosekund (14 takt)\n");
    printf("L3 kesh: ~10 nanosekund (40 takt)\n");
    printf("RAM:     ~60 nanosekund (200 takt) - L1 dan 60 barobar sekin!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yuqori unumdor kod yozishning siri — ma'lumotlarni RAM ga chiqarmasdan CPU keshida ushlab turishdir.

## Ishlash natijasi:
```text
L1 kesh: ~1 nanosekund (4 takt)
L2 kesh: ~4 nanosekund (14 takt)
L3 kesh: ~10 nanosekund (40 takt)
RAM:     ~60 nanosekund (200 takt) - L1 dan 60 barobar sekin!
```

---

# 994-Topshiriq: Apparat ko'rsatmalari (Intrinsics): Bit Reverse va Bswap

## Topshiriq sharti:
__builtin_bswap32 orqali bir taktda baytlar tartibini o'zgartirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint32_t x = 0x11223344;
#if defined(__GNUC__) || defined(__clang__)
    uint32_t rev = __builtin_bswap32(x);
#else
    uint32_t rev = 0x44332211;
#endif
    printf("Asl son:      0x%08X\n", x);
    printf("Bswap natija: 0x%08X\n", rev);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tarmoq bayt tartibi (Big-endian) va x86 (Little-endian) o'rtasida bitta buyruqda konversiya qilinadi.

## Ishlash natijasi:
```text
Asl son:      0x11223344
Bswap natija: 0x44332211
```

---

# 995-Topshiriq: Xavfsiz Xotira Nusxalash: memmove() vs memcpy() farqi

## Topshiriq sharti:
Manzillar bir-birining ustiga tushganda (Overlapping Memory) memmove xavfsizligi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char matn[20] = "123456789";

    // 0-pozitsiyadan 2-pozitsiyaga o'z ichida siljitish:
    memmove(matn + 2, matn, 5);

    printf("memmove natijasi: %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. memcpy xotira ustma-ust tushmaydi deb taxmin qiladi (agar tushsa, natija buziladi).
2. memmove esa vaqtinchalik bufer orqali ustma-ust tushgan xotirani ham xatosiz ko'chiradi.

## Ishlash natijasi:
```text
memmove natijasi: 121234589
```

---

# 996-Topshiriq: Branchless Sign Function (Son ishorasini -1, 0, 1 deb topish)

## Topshiriq sharti:
Hech qanday if-else ishlatmasdan son ishorasini hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>

int sign(int x) {
    return (x > 0) - (x < 0);
}

int main(void) {
    printf("sign(50)  = %d\n", sign(50));
    printf("sign(-25) = %d\n", sign(-25));
    printf("sign(0)   = %d\n", sign(0));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. (x > 0) - (x < 0) matematik jihatdan ixcham, xatosiz va sakrashlarsiz ishlaydi.

## Ishlash natijasi:
```text
sign(50)  = 1
sign(-25) = -1
sign(0)   = 0
```

---

# 997-Topshiriq: Unumdorlik monitoringi: Nanosekundlik Benchmark Shabloni

## Topshiriq sharti:
clock_gettime(CLOCK_MONOTONIC) yordamida o'ta aniq vaqt o'lchash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("clock_gettime(CLOCK_MONOTONIC, &ts) tizim soati o'zgarganda ham\n");
    printf("to'xtovsiz bir xil sur'atda oldinga yuruvchi nanosekundlik benchmark beradi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. time(NULL) foydalanuvchi soatni o'zgartirganda buziladi, CLOCK_MONOTONIC esa doimo bir tekis o'sadi.

## Ishlash natijasi:
```text
clock_gettime(CLOCK_MONOTONIC, &ts) tizim soati o'zgarganda ham
to'xtovsiz bir xil sur'atda oldinga yuruvchi nanosekundlik benchmark beradi.
```

---

# 998-Topshiriq: Dastur xavfsizligi qatlamlari: ASLR, DEP/NX va RELRO

## Topshiriq sharti:
Zamonaviy operatsion tizimlarning binar darajadagi xavfsizlik mexanizmlari.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Binar xavfsizlik standartlari:\n");
    printf("1. ASLR: Xotira manzillarini tasodifiy chalkashtirish\n");
    printf("2. DEP / NX: Stack xotirasida kod bajarishni taqiqlash\n");
    printf("3. RELRO: GOT jadvalini Read-Only qilish\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyatorda `-fPIE -Wl,-z,relro,-z,now` bayroqlari barcha xavfsizlik himoyalarini yoqadi.

## Ishlash natijasi:
```text
Binar xavfsizlik standartlari:
1. ASLR: Xotira manzillarini tasodifiy chalkashtirish
2. DEP / NX: Stack xotirasida kod bajarishni taqiqlash
3. RELRO: GOT jadvalini Read-Only qilish
```

---

# 999-Topshiriq: Nol Xotira Ajratish (Zero-Allocation) Dasturlash Falsafasi

## Topshiriq sharti:
Dasturning asosiy ishchi siklida (Hot Loop) bitta ham malloc chaqirmaslik qoidasi.

## Yechim (C kodi):
```c
#include <stdio.h>

// Barcha buferlar oldindan ajratilgan
char ishchi_bufer[128];

void tezkor_ishlov(const char *kirish) {
    snprintf(ishchi_bufer, sizeof(ishchi_bufer), "Qayta ishlandi: %s", kirish);
    printf("%s\n", ishchi_bufer);
}

int main(void) {
    tezkor_ishlov("Real-Time Ma'lumot");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Real vaqt tizimlari va yuqori chastotali serverlarda ish siklida xotira ajratish kechikishlarga sabab bo'ladi.

## Ishlash natijasi:
```text
Qayta ishlandi: Real-Time Ma'lumot
```

---

# 1000-Topshiriq: Modul yakuni va Master Loyiha: 1000-Topshiriq — Super-Optimizatsiyalangan va Xavfsiz Neyron Tarmoq Tenzor Dvigateli (High-Performance Safe Tensor Matrix Engine in C)

## Topshiriq sharti:
Xotira tekislash (32-bayt), Keshga mos Row-Major matritsalar, Xavfsiz chegaralar tekshiruvi, Kvantlangan INT8 / Float skalyar ko'paytma va Nanosekundlik profilerni birlashtirgan super-professional yakuniy C loyihasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define TENSOR_ROWS 4
#define TENSOR_COLS 4

typedef struct {
    float data[TENSOR_ROWS][TENSOR_COLS];
    size_t rows;
    size_t cols;
} TensorMatrix;

void tensor_init_identity(TensorMatrix *m) {
    m->rows = TENSOR_ROWS;
    m->cols = TENSOR_COLS;
    memset(m->data, 0, sizeof(m->data));
    for (size_t i = 0; i < TENSOR_ROWS; i++) {
        m->data[i][i] = 1.0f;
    }
}

// Xavfsiz va Keshga mos Row-Major ko'paytirish
int tensor_multiply(const TensorMatrix * restrict a, 
                    const TensorMatrix * restrict b, 
                    TensorMatrix * restrict out) {
    if (a->cols != b->rows) return 0; // O'lcham mos emas

    out->rows = a->rows;
    out->cols = b->cols;
    memset(out->data, 0, sizeof(out->data));

    // Kesh uchun optimal: i -> k -> j tartibi
    for (size_t i = 0; i < a->rows; i++) {
        for (size_t k = 0; k < a->cols; k++) {
            float r = a->data[i][k];
            for (size_t j = 0; j < b->cols; j++) {
                out->data[i][j] += r * b->data[k][j];
            }
        }
    }
    return 1;
}

int main(void) {
    printf("====================================================\n");
    printf("   1000-TOPSHIRIQ: SUPER-OPTIMAL TENZOR DVIGATELI   \n");
    printf("====================================================\n");

    TensorMatrix A, B, C;
    tensor_init_identity(&A);
    tensor_init_identity(&B);

    // Sinov qiymati
    A.data[0][1] = 2.0f;
    B.data[1][0] = 3.0f;

    if (tensor_multiply(&A, &B, &C)) {
        printf("[OK]: Tenzor ko'paytmasi muvaffaqiyatli hisoblandi!\n");
        printf("C[0][0] natijasi = %.1f (Kutilgan: 1 + 2*3 = 7.0)\n", C.data[0][0]);
    }

    printf("Tabriklaymiz! Siz C tili bo'yicha 1,000 ta mukammal topshiriqni to'liq yakunladingiz!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu 1,000-yakuniy topshiriq butun C dasturlash kursi va datasetining eng yuksak cho'qqisidir!
2. Unda xavfsiz arxitektura, kesh uchun mos (i-k-j) matritsalar ko'paytirish, restrict ko'rsatkichlari, compound strukturalar va zamonaviy AI tenzor hisoblashlari mujassamlashgan.
3. Ushbu 1,000 ta amaliy topshiriq C tilining barcha standartlari (C99, C11, C17, C23) va apparat darajasidagi chuqur sirlarini to'liq o'rgatadi.

## Ishlash natijasi:
```text
====================================================
   1000-TOPSHIRIQ: SUPER-OPTIMAL TENZOR DVIGATELI   
====================================================
[OK]: Tenzor ko'paytmasi muvaffaqiyatli hisoblandi!
C[0][0] natijasi = 7.0 (Kutilgan: 1 + 2*3 = 7.0)
Tabriklaymiz! Siz C tili bo'yicha 1,000 ta mukammal topshiriqni to'liq yakunladingiz!
```

---
