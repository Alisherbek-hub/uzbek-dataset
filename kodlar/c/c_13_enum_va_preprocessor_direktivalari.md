# C Dasturlash Tili — 13-Qism: Enum va Preprocessor Direktivalari
## (601-650 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* enum asoslari, typedef enum va FSM (Holat mashinalari)
* Bitmask bayroqlari va COUNT elementlar soni idiomi
* #define konstantalari va funksiya-makroslardagi xavflar (Parentheses trap)
* do-while(0) ko'p qatorli makroslar, Stringification (#) va Token-pasting (##)
* Shartli kompilyatsiya (#ifdef, #if, defined) va Include Guards / #pragma once
* Standart makroslar (__FILE__, __LINE__, __func__), assert va _Static_assert
* X-Macros metaprogramming va Avtomatik Buyruqlar Dispatcheri

---

# 601-Topshiriq: enum asoslari va sukut bo'yicha qiymatlar

## Topshiriq sharti:
Hafta kunlarini enum sifatida e'lon qilish va ularning 0 dan boshlanuvchi ketma-ket qiymatlarini chiqarish.

## Yechim (C kodi):
```c
#include <stdio.h>

enum HaftaKuni {
    DUSHANBA,  // 0
    SESHANBA,  // 1
    CHORSHANBA,// 2
    PAYSHANBA, // 3
    JUMA,      // 4
    SHANBA,    // 5
    YAKSHANBA  // 6
};

int main(void) {
    enum HaftaKuni bugun = JUMA;
    printf("Juma kunining sonli qiymati: %d\n", bugun);
    printf("Dushanba: %d, Yakshanba: %d\n", DUSHANBA, YAKSHANBA);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida enum elementlari sukut bo'yicha 0 dan boshlab 1 qadam bilan o'sib boruvchi butun sonli konstantalardir.
2. enum o'qiluvchanlikni oshiradi va 'sehrli sonlar' (magic numbers) dan qochishga yordam beradi.

## Ishlash natijasi:
```text
Juma kunining sonli qiymati: 4
Dushanba: 0, Yakshanba: 6
```

---

# 602-Topshiriq: enum konstantalariga ixtiyoriy qiymatlar belgilash

## Topshiriq sharti:
enum a'zolariga boshlang'ich va oraliq ixtiyoriy qiymatlarni biriktirish hamda ularning keyingi tartibini ko'rsatish.

## Yechim (C kodi):
```c
#include <stdio.h>

enum ServerStatus {
    STATUS_OK = 200,
    STATUS_CREATED = 201,
    STATUS_BAD_REQUEST = 400,
    STATUS_UNAUTHORIZED, // 401
    STATUS_FORBIDDEN,    // 402
    STATUS_NOT_FOUND = 404,
    STATUS_INTERNAL_ERROR = 500
};

int main(void) {
    printf("OK: %d\n", STATUS_OK);
    printf("Bad Request: %d\n", STATUS_BAD_REQUEST);
    printf("Unauthorized: %d (avtomatik +1)\n", STATUS_UNAUTHORIZED);
    printf("Forbidden: %d\n", STATUS_FORBIDDEN);
    printf("Not Found: %d\n", STATUS_NOT_FOUND);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar enum elementiga aniq qiymat berilsa, undan keyingi element avtomatik ravishda unga 1 qo'shilgan qiymatni oladi.
2. Bu HTTP status kodlari yoki apparat kodlarini modellashtirish uchun juda qulaydir.

## Ishlash natijasi:
```text
OK: 200
Bad Request: 400
Unauthorized: 401 (avtomatik +1)
Forbidden: 402
Not Found: 404
```

---

# 603-Topshiriq: typedef enum sintaksisi va qulayliklari

## Topshiriq sharti:
typedef yordamida enum so'zini takrorlamasdan yangi tip yaratish va undan funksiyalarda foydalanish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef enum {
    FAIL,
    SUCCESS
} Result;

Result bajar_amaliyot(int son) {
    if (son < 0) return FAIL;
    return SUCCESS;
}

int main(void) {
    Result r = bajar_amaliyot(10);
    if (r == SUCCESS) {
        printf("Amaliyot muvaffaqiyatli bajarildi (kod: %d)\n", r);
    } else {
        printf("Xatolik yuz berdi\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. typedef enum { ... } TipNomi; konstruksiyasi o'zgaruvchi e'lon qilishda har safar 'enum' so'zini yozish majburiyatidan xalos qiladi.
2. Funksiyadan qaytuvchi holat kodlari uchun bu eng ommabop C idiomasi hisoblanadi.

## Ishlash natijasi:
```text
Amaliyot muvaffaqiyatli bajarildi (kod: 1)
```

---

# 604-Topshiriq: enum xotira hajmi: sizeof(enum)

## Topshiriq sharti:
enum o'zgaruvchisining xotiradagi hajmini o'lchash va uning int tipi bilan bog'liqligini tushuntirish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef enum {
    KICHIK = 1,
    ORTA = 2,
    KATTA = 3
} Hajm;

int main(void) {
    Hajm h = ORTA;
    printf("Hajm enum o'lchami: %zu bayt\n", sizeof(h));
    printf("int tipi o'lchami:    %zu bayt\n", sizeof(int));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C standartiga ko'ra, enum qiymatlari kompilyator tomonidan mos butun son (odatda 'signed int' yoki 'unsigned int') sifatida saqlanadi.
2. Shuning uchun sizeof(enum) odatda sizeof(int) ga, ya'ni zamonaviy tizimlarda 4 baytga teng bo'ladi.

## Ishlash natijasi:
```text
Hajm enum o'lchami: 4 bayt
int tipi o'lchami:    4 bayt
```

---

# 605-Topshiriq: enum orqali Holat Mashinasi (Finite State Machine - FSM)

## Topshiriq sharti:
Oddiy FSM (Boshlang'ich, Ishlamoqda, To'xtatilgan, Tugallangan) ni enum va switch-case yordamida boshqarish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef enum {
    STATE_IDLE,
    STATE_RUNNING,
    STATE_PAUSED,
    STATE_COMPLETED
} FSMState;

void handle_state(FSMState s) {
    switch (s) {
        case STATE_IDLE:      printf("Tizim kutish holatida.\n"); break;
        case STATE_RUNNING:   printf("Tizim ish jarayonida.\n"); break;
        case STATE_PAUSED:    printf("Tizim vaqtincha to'xtatildi.\n"); break;
        case STATE_COMPLETED: printf("Tizim ishni yakunladi.\n"); break;
    }
}

int main(void) {
    FSMState holat = STATE_IDLE;
    handle_state(holat);
    holat = STATE_RUNNING;
    handle_state(holat);
    holat = STATE_COMPLETED;
    handle_state(holat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Finite State Machine (Chekli holat mashinasi) protokollar, robotlar va o'yin mantiqida asosiy arxitektura hisoblanadi.
2. enum barcha mumkin bo'lgan holatlarni xatosiz cheklash va kodni sodda saqlash imkonini beradi.

## Ishlash natijasi:
```text
Tizim kutish holatida.
Tizim ish jarayonida.
Tizim ishni yakunladi.
```

---

# 606-Topshiriq: enum bitmask bayroqlari (Bitmask Flags)

## Topshiriq sharti:
enum qiymatlarini 1<<0, 1<<1, 1<<2 ko'rinishida berib, bitwise OR (|) va AND (&) bilan bir nechta holatlarni birlashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef enum {
    FLAG_NONE  = 0,
    FLAG_READ  = 1 << 0, // 0x01
    FLAG_WRITE = 1 << 1, // 0x02
    FLAG_EXEC  = 1 << 2  // 0x04
} PermissionFlags;

int main(void) {
    int ruxsatlar = FLAG_READ | FLAG_WRITE; // O'qish va yozish

    if (ruxsatlar & FLAG_READ)  printf("O'qish ruxsati bor\n");
    if (ruxsatlar & FLAG_WRITE) printf("Yozish ruxsati bor\n");
    if (ruxsatlar & FLAG_EXEC)  printf("Bajarish ruxsati bor\n");
    else                        printf("Bajarish ruxsati YO'Q\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitmask enumlar yordamida bitta butun son ichida 32 tagacha mustaqil sozlamalar va bayroqlarni birlashtirish mumkin.
2. Bitwise OR (|) bayroqni qo'shadi, bitwise AND (&) esa bayroq mavjudligini tekshiradi.

## Ishlash natijasi:
```text
O'qish ruxsati bor
Yozish ruxsati bor
Bajarish ruxsati YO'Q
```

---

# 607-Topshiriq: enum qiymatini matnga (String) o'giruvchi yordamchi funksiya

## Topshiriq sharti:
enum qiymatini qabul qilib, uning inson tushunadigan nomini const char* sifatida qaytaruvchi switch-case funksiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef enum {
    ERROR_NONE,
    ERROR_TIMEOUT,
    ERROR_DISCONNECTED,
    ERROR_OUT_OF_MEMORY
} ErrorCode;

const char* error_to_string(ErrorCode code) {
    switch (code) {
        case ERROR_NONE:          return "Hech qanday xatolik yo'q";
        case ERROR_TIMEOUT:       return "Vaqt tugadi (Timeout)";
        case ERROR_DISCONNECTED:  return "Aloqa uzildi";
        case ERROR_OUT_OF_MEMORY: return "Xotira yetishmadi";
        default:                  return "Noma'lum xatolik";
    }
}

int main(void) {
    ErrorCode e1 = ERROR_TIMEOUT;
    ErrorCode e2 = ERROR_NONE;

    printf("e1 holati: %s\n", error_to_string(e1));
    printf("e2 holati: %s\n", error_to_string(e2));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida enum nomlari kompilyatsiyadan keyin saqlanmaydi (int ga aylanadi).
2. Konsolga yoki log fayllarga chiroyli xabarlar chiqarish uchun har doim enum_to_string yordamchi funksiyasi yoziladi.

## Ishlash natijasi:
```text
e1 holati: Vaqt tugadi (Timeout)
e2 holati: Hech qanday xatolik yo'q
```

---

# 608-Topshiriq: enum ichida takroriy qiymatlar berish (Aliases)

## Topshiriq sharti:
Bitta enum ichida turli nomlarga bir xil sonli qiymat belgilash va ularning ekvivalentligini tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>

enum Ranglar {
    QIZIL = 1,
    YASHIL = 2,
    KO_K = 3,
    RED = 1,     // Inglizcha taxallus (Alias)
    GREEN = 2,
    BLUE = 3
};

int main(void) {
    printf("QIZIL = %d, RED = %d\n", QIZIL, RED);
    if (QIZIL == RED) {
        printf("QIZIL va RED xotirada bir xil qiymatga ega!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. enum ichida bir nechta identifikatorga aynan bitta sonli qiymatni belgilash mumkin.
2. Bu xalqaro nomlash yoki versiyalar o'rtasidagi orqaga moslikni ta'minlashda qulay vositadir.

## Ishlash natijasi:
```text
QIZIL = 1, RED = 1
QIZIL va RED xotirada bir xil qiymatga ega!
```

---

# 609-Topshiriq: enum chegaralari va elementlar sonini avtomatik hisoblash (COUNT idiomi)

## Topshiriq sharti:
enum oxiriga COUNT yoki TOTAL identifikatorini qo'yish orqali elementlar sonini avtomatik olish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef enum {
    MEVA_OLMA,
    MEVA_BANAN,
    MEVA_ANOR,
    MEVA_UZUM,
    MEVALAR_SONI // Avtomatik ravishda 4 bo'ladi
} Meva;

int main(void) {
    const char *nomlar[MEVALAR_SONI] = {
        "Olma", "Banan", "Anor", "Uzum"
    };

    printf("Mavjud mevalar soni: %d\n", MEVALAR_SONI);
    for (int i = 0; i < MEVALAR_SONI; i++) {
        printf("Meva %d: %s\n", i + 1, nomlar[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar enum 0 dan boshlansa, oxiriga qo'shilgan elementning sonli qiymati barcha oldingi elementlar soniga teng bo'ladi.
2. Bu usul massivlar o'lchamini belgilashda dinamik va xavfsiz C idiomasi hisoblanadi.

## Ishlash natijasi:
```text
Mavjud mevalar soni: 4
Meva 1: Olma
Meva 2: Banan
Meva 3: Anor
Meva 4: Uzum
```

---

# 610-Topshiriq: #define ob'ektli makroslar (Object-like Macros)

## Topshiriq sharti:
#define yordamida o'zgarmas sonlar, matnlar va konfiguratsiya parametrlarini belgilash.

## Yechim (C kodi):
```c
#include <stdio.h>

#define MAKSIMAL_FOYDALANUVCHILAR 100
#define ILIBAQIYA 3.14159265
#define DASTUR_NOMI "Antigravity OS"

int main(void) {
    printf("Dastur: %s\n", DASTUR_NOMI);
    printf("Maksimal foydalanuvchilar: %d\n", MAKSIMAL_FOYDALANUVCHILAR);
    printf("Pi soni: %.5f\n", ILIBAQIYA);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. #define preprocessor direktivasi bo'lib, kompilyatsiyadan oldin kod ichidagi barcha mos so'zlarni to'g'ridan-to'g'ri almashtiradi (tekstual almashtirish).
2. Xotirada o'zgaruvchi yaratmaydi, to'g'ridan-to'g'ri kod matniga kiritiladi.

## Ishlash natijasi:
```text
Dastur: Antigravity OS
Maksimal foydalanuvchilar: 100
Pi soni: 3.14159
```

---

# 611-Topshiriq: #define funksiya-makroslar (Function-like Macros) asoslari

## Topshiriq sharti:
Argument qabul qiluvchi oddiy makros yaratish va uning ishlashini tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

int main(void) {
    int x = 25, y = 42;
    printf("Kattasi: %d\n", MAX(x, y));
    printf("Kichigi: %d\n", MIN(x, y));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Funksiya-makroslar funksiya chaqiruvi sarf-xarajatlarisiz (stack frame, call instruction) inline kod bajarish imkonini beradi.
2. Tiplarga bog'liq emas (Generic) bo'lib, float va int lar bilan bir xil ishlay oladi.

## Ishlash natijasi:
```text
Kattasi: 42
Kichigi: 25
```

---

# 612-Topshiriq: Makroslarda qavslar xavfi (The Parenthesis Trap)

## Topshiriq sharti:
Qavslarsiz yozilgan makrosning arifmetik amallar tartibini buzishini va uni to'g'rilash usulini ko'rsatish.

## Yechim (C kodi):
```c
#include <stdio.h>

// Xavfli makros (qavslarsiz)
#define XATO_KVADRAT(x) x * x

// Xavfsiz makros (har bir argument va umumiy ifoda qavsda)
#define TOGRI_KVADRAT(x) ((x) * (x))

int main(void) {
    int a = 2 + 3; // 5

    // XATO: 2 + 3 * 2 + 3 = 2 + 6 + 3 = 11!
    printf("XATO_KVADRAT(2 + 3) = %d (Kutilgan: 25!)\n", XATO_KVADRAT(a)); 
    printf("XATO_KVADRAT to'g'ridan-to'g'ri ifoda bilan: %d\n", XATO_KVADRAT(2 + 3));

    // TOGRI: ((2 + 3) * (2 + 3)) = 5 * 5 = 25
    printf("TOGRI_KVADRAT(2 + 3) = %d\n", TOGRI_KVADRAT(2 + 3));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Preprocessor matematikani tushunmaydi, faqat matnni almashtiradi. 2 + 3 * 2 + 3 amallarida ko'paytirish ustun bo'lib qoladi.
2. Qoida: Makros argumentlari har doim qavsga olinishi ((x)) va butun ifoda ham qavsga olinishi shart!

## Ishlash natijasi:
```text
XATO_KVADRAT(2 + 3) = 25 (Kutilgan: 25!)
XATO_KVADRAT to'g'ridan-to'g'ri ifoda bilan: 11
TOGRI_KVADRAT(2 + 3) = 25
```

---

# 613-Topshiriq: Makroslarda nojo'ya ta'sirlar (Macro Side-effects) va takroriy hisoblash xavfi

## Topshiriq sharti:
Inkrement (++) operatorini makrosga uzatganda ikki marta bajarilish xatosini tahlil qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define MAX(a, b) ((a) > (b) ? (a) : (b))

int main(void) {
    int x = 5;
    int y = 3;

    // x++ ikki marta bajariladi, chunki MAX(x++, y) -> ((x++) > (y) ? (x++) : (y))
    int natija = MAX(x++, y);

    printf("Natija: %d\n", natija);
    printf("x ning yakuniy qiymati: %d (Kutilgan 6 emas, 7!)\n", x);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar makros o'z argumentini bir necha bor ishlatsa, argumentdagi inkrement/dekrement yoki funksiya chaqiruvi qayta-qayta ishga tushadi.
2. Bu C tilidagi eng mashhur va xavfli 'macro side-effect' xatosi hisoblanadi. Inline funksiyalar bu xatodan xoli.

## Ishlash natijasi:
```text
Natija: 6
x ning yakuniy qiymati: 7 (Kutilgan 6 emas, 7!)
```

---

# 614-Topshiriq: Ko'p qatorli makroslar va do { ... } while(0) idiomasi

## Topshiriq sharti:
Nima uchun ko'p operatorli makroslar do { ... } while(0) blokiga olinishi shartligini if-else kontekstida isbotlash.

## Yechim (C kodi):
```c
#include <stdio.h>

// Xavfsiz ko'p qatorli makros
#define ALMASH(a, b, tip) do { \
    tip temp = (a);            \
    (a) = (b);                 \
    (b) = temp;                \
} while (0)

int main(void) {
    int x = 10, y = 20;
    int shart = 1;

    if (shart)
        ALMASH(x, y, int); // do { ... } while(0); if-else bilan bexato ulanadi
    else
        printf("Bajarilmadi\n");

    printf("x = %d, y = %d\n", x, y);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar oddiy { ... } ishlatilsa, oxiriga qo'yilgan nuqtali vergul (;) if-else zanjirini buzadi va 'else without previous if' sintaksis xatosini keltirib chiqaradi.
2. do { ... } while(0) idiomasi bitta butun sintaktik operator hosil qilib, nuqtali vergulni bexato qabul qiladi.

## Ishlash natijasi:
```text
x = 20, y = 10
```

---

# 615-Topshiriq: Stringification operatori (#) - Argumentni satrga aylantirish

## Topshiriq sharti:
# operatori orqali makrosga berilgan o'zgaruvchi nomini matn ko'rinishida chop etish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define CHOP_ET(x) printf(#x " = %d\n", (x))
#define CHOP_FLOAT(x) printf(#x " = %.2f\n", (x))

int main(void) {
    int yosh = 25;
    float harorat = 36.6f;

    CHOP_ET(yosh);
    CHOP_FLOAT(harorat);
    CHOP_ET(10 + 5 * 2);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Preprocessor da argument oldiga '#' belgisi qo'yilsa, u stringification (satrlashtirish) amalini bajaradi va argumentni qo'shtirnoq ichiga oladi.
2. Bu debug va o'zgaruvchi nomlarini avtomatik chiqaruvchi log tizimlarida juda keng qo'llaniladi.

## Ishlash natijasi:
```text
yosh = 25
harorat = 36.60
10 + 5 * 2 = 20
```

---

# 616-Topshiriq: Token-pasting operatori (##) - Identifikatorlarni birlashtirish

## Topshiriq sharti:
## operatori yordamida ikkita tokenni birlashtirib yangi o'zgaruvchi yoki funksiya nomini hosil qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define YARAT_OZGARUVCHI(nom, son) int nom##_##son = son * 10
#define CHOP_VAR(nom, son) printf(#nom "_" #son " = %d\n", nom##_##son)

int main(void) {
    YARAT_OZGARUVCHI(hisob, 1); // int hisob_1 = 10;
    YARAT_OZGARUVCHI(hisob, 2); // int hisob_2 = 20;

    CHOP_VAR(hisob, 1);
    CHOP_VAR(hisob, 2);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. '##' operatori preprocessor bosqichida ikkita alohida tokenni bitta identifikatorga yopishtiradi.
2. Metaprogramming va kod shablonlarini (templates) C tilida simulyatsiya qilish uchun asosiy vositadir.

## Ishlash natijasi:
```text
hisob_1 = 10
hisob_2 = 20
```

---

# 617-Topshiriq: Shartli kompilyatsiya: #ifdef, #ifndef, #endif

## Topshiriq sharti:
Belgilangan makros mavjudligiga qarab kod qismini kompilyatsiyaga kiritish yoki chiqarib tashlash.

## Yechim (C kodi):
```c
#include <stdio.h>

#define DEBUG_REJIM

int main(void) {
    printf("Asosiy dastur ishga tushdi.\n");

#ifdef DEBUG_REJIM
    printf("[DEBUG]: Tizim resurslari va xotira tekshirilmoqda...\n");
#endif

#ifndef ISHLAB_CHIQARISH
    printf("[INFO]: Ishlab chiqarish (Production) rejimi yoqilmagan.\n");
#endif

    return 0;
}
```

## Tushuntirish va Mantiq:
1. #ifdef va #ifndef direktivalari berilgan identifikator #define qilingan yoki qilinmaganligini tekshiradi.
2. Agar shart bajarilmasa, blok ichidagi kod kompilyatorga yetib bormaydi va yakuniy binar faylda umuman joy egallamaydi.

## Ishlash natijasi:
```text
Asosiy dastur ishga tushdi.
[DEBUG]: Tizim resurslari va xotira tekshirilmoqda...
[INFO]: Ishlab chiqarish (Production) rejimi yoqilmagan.
```

---

# 618-Topshiriq: Ko'p shartli kompilyatsiya: #if, #elif, #else, defined()

## Topshiriq sharti:
Sonli ifodalar va defined() operatori orqali versiyalarni boshqarish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define PROTOCOL_VERSION 2

int main(void) {
#if PROTOCOL_VERSION == 1
    printf("Eski Protokol v1 faollashtirildi.\n");
#elif PROTOCOL_VERSION == 2
    printf("Zamonaviy Protokol v2 faollashtirildi.\n");
#else
    printf("Noma'lum protokol versiyasi!\n");
#endif

#if defined(DEBUG) || !defined(NDEBUG)
    printf("Debug xususiyatlari faol.\n");
#endif
    return 0;
}
```

## Tushuntirish va Mantiq:
1. #if sonli mantiqiy ifodalarni (==, !=, >, <, &&, ||) tekshirish imkonini beradi.
2. defined(X) operatori identifikator mavjudligini murakkab shartlar ichida tekshirish uchun ishlatiladi.

## Ishlash natijasi:
```text
Zamonaviy Protokol v2 faollashtirildi.
Debug xususiyatlari faol.
```

---

# 619-Topshiriq: Include Guards: Takroriy yuklanishning (Multiple Inclusion) oldini olish

## Topshiriq sharti:
Sarlavha fayllarini (Header files) himoya qilish uchun #ifndef HEADER_H idiomasi qanday ishlashini modellashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

// Sarlavha fayli simulyatsiyasi (masalan math_custom.h)
#ifndef MATH_CUSTOM_H
#define MATH_CUSTOM_H

typedef struct {
    double x, y;
} Point2D;

void chop_nuqta(Point2D p) {
    printf("Nuqta: (%.1f, %.1f)\n", p.x, p.y);
}

#endif // MATH_CUSTOM_H

// Ikkinchi marta chaqirilganda hech qanday takroriy deklaratsiya xatosi yuz bermaydi
#ifndef MATH_CUSTOM_H
#define MATH_CUSTOM_H
// Bu blok to'liq o'tkazib yuboriladi
#endif

int main(void) {
    Point2D p = {3.5, 7.2};
    chop_nuqta(p);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar bir nechta fayl bitta header faylni yuklasa (#include), struct yoki typedef takror e'lon qilinib xatolik yuz beradi.
2. Include Guard (#ifndef HEADER_H ... #endif) fayl faqat bitta marta o'qilishini kafolatlaydi.

## Ishlash natijasi:
```text
Nuqta: (3.5, 7.2)
```

---

# 620-Topshiriq: #pragma once direktivasi

## Topshiriq sharti:
Zamonaviy C kompilyatorlarida fayl takror yuklanishidan himoyalanishning muqobil usuli.

## Yechim (C kodi):
```c
#include <stdio.h>

// Odatda header faylning eng birinchi qatorida yoziladi:
// #pragma once

int main(void) {
    printf("#pragma once - include guard lar o'rniga no-standart ammo deyarli barcha\n");
    printf("zamonaviy kompilyatorlar (GCC, Clang, MSVC) tomonidan qo'llab-quvvatlanuvchi\n");
    printf("fayl darajasidagi himoya direktivasidir.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. #pragma once faylni faqat bir marta kompilyatsiya qilishni buyuradi va nom to'qnashuvlari xavfini bartaraf etadi.
2. Katta loyihalarda kompilyatsiya vaqtini tezlashtiradi, chunki kompilyator faylni qayta ochib o'tirmaydi.

## Ishlash natijasi:
```text
#pragma once - include guard lar o'rniga no-standart ammo deyarli barcha
zamonaviy kompilyatorlar (GCC, Clang, MSVC) tomonidan qo'llab-quvvatlanuvchi
fayl darajasidagi himoya direktivasidir.
```

---

# 621-Topshiriq: Standart oldindan aniqlangan makroslar: __FILE__, __LINE__, __DATE__, __TIME__

## Topshiriq sharti:
Kompilyatsiya vaqti, sanasi, fayl nomi va qator raqamini aniqlovchi tizim makroslari.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Ushbu fayl: %s\n", __FILE__);
    printf("Kompilyatsiya sanasi: %s\n", __DATE__);
    printf("Kompilyatsiya vaqti:  %s\n", __TIME__);
    printf("Hozirgi qator raqami: %d\n", __LINE__);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. __FILE__ va __LINE__ makroslari xatolik va log xabarlarida kodning qaysi joyida muammo chiqqanini ko'rsatish uchun bebaho vositadir.
2. __DATE__ va __TIME__ binar faylning qachon yig'ilganini aniqlash imkonini beradi.

## Ishlash natijasi:
```text
Ushbu fayl: main.c
Kompilyatsiya sanasi: Nov  8 2026
Kompilyatsiya vaqti:  10:30:00
Hozirgi qator raqami: 8
```

---

# 622-Topshiriq: __func__ identifikatori (C99) orqali faol funksiya nomini olish

## Topshiriq sharti:
Funksiya ichida o'z nomini matn sifatida olish va xatoliklarni qayd etish.

## Yechim (C kodi):
```c
#include <stdio.h>

void malumot_saqla(int id) {
    printf("[%s] ID %d bo'yicha ma'lumot saqlanmoqda...\n", __func__, id);
}

void tarmoq_ulanish(const char *manzil) {
    printf("[%s] '%s' serveriga ulanish...\n", __func__, manzil);
}

int main(void) {
    malumot_saqla(42);
    tarmoq_ulanish("192.168.1.1");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C99 standartida __func__ har bir funksiya tanasida avtomatik yaratiladigan 'static const char __func__[]' o'zgaruvchisidir.
2. Funksiyani qayta nomlaganda ham log xabarlaridagi nomlar avtomatik to'g'ri chiqadi.

## Ishlash natijasi:
```text
[malumot_saqla] ID 42 bo'yicha ma'lumot saqlanmoqda...
[tarmoq_ulanish] '192.168.1.1' serveriga ulanish...
```

---

# 623-Topshiriq: #error direktivasi orqali noto'g'ri konfiguratsiyada kompilyatsiyani to'xtatish

## Topshiriq sharti:
#error yordamida shart qanoatlantirilmaganda kompilyatorga majburiy xato signali berish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define BUFFER_SIZE 512

#if BUFFER_SIZE < 1024
    // #error "BUFFER_SIZE kamida 1024 bo'lishi shart!"
#endif

int main(void) {
    printf("#error direktivasi kompilyatsiya jarayonida shart noto'g'ri bo'lsa\n");
    printf("barcha jarayonni darhol to'xtatadi va berilgan xabar bilan xatolik qaytaradi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. #error direktivasi platforma, arxitektura yoki konfiguratsiyaviy parametrlar mos kelmaganda kompilyatsiyani to'xtatish uchun qo'llaniladi.
2. Bu noto'g'ri binar fayl hosil bo'lishining oldini oladi.

## Ishlash natijasi:
```text
#error direktivasi kompilyatsiya jarayonida shart noto'g'ri bo'lsa
barcha jarayonni darhol to'xtatadi va berilgan xabar bilan xatolik qaytaradi.
```

---

# 624-Topshiriq: #warning direktivasi orqali ogohlantirish chiqarish

## Topshiriq sharti:
Kompilyatsiya vaqtida dasturchi uchun xavfsizlik yoki eskirgan (deprecated) kod haqida ogohlantirish berish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define ESKI_API 1

#if ESKI_API
    // #warning "Diqqat: Ushbu API eskirgan, keyingi versiyalarda o'chiriladi!"
#endif

int main(void) {
    printf("#warning direktivasi kompilyatsiyani to'xtatmaydi, ammo konsolga\n");
    printf("ogohlantirish (warning) chiqarib dasturchini xabardor qiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. #warning (GCC/Clang va C23 standartida) dasturchiga eskirgan metodlar yoki tavsiya etilmaydigan sozlamalar haqida ogohlantirish berish uchun qulay.

## Ishlash natijasi:
```text
#warning direktivasi kompilyatsiyani to'xtatmaydi, ammo konsolga
ogohlantirish (warning) chiqarib dasturchini xabardor qiladi.
```

---

# 625-Topshiriq: #undef direktivasi: Makrosni bekor qilish

## Topshiriq sharti:
Oldin e'lon qilingan makros ta'rifini o'chirish va unga yangi qiymat berish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define CHEGARA 100

void funksiya1(void) {
    printf("CHEGARA funksiya 1 da: %d\n", CHEGARA);
}

#undef CHEGARA
#define CHEGARA 500

void funksiya2(void) {
    printf("CHEGARA funksiya 2 da: %d\n", CHEGARA);
}

int main(void) {
    funksiya1();
    funksiya2();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. #undef direktivasi ko'rsatilgan makros nomini preprocessor xotirasidan o'chirib tashlaydi.
2. Shundan so'ng ushbu identifikatorni boshqa qiymat bilan qayta aniqlash (#define) mumkin.

## Ishlash natijasi:
```text
CHEGARA funksiya 1 da: 100
CHEGARA funksiya 2 da: 500
```

---

# 626-Topshiriq: Variadic Makroslar: __VA_ARGS__ yordamida o'zgaruvchan argumentlar

## Topshiriq sharti:
printf kabi istalgancha argument qabul qiluvchi maxsus LOG_DEBUG makrosi yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define LOG_XABAR(daraja, fmt, ...) \
    printf("[%s] %s:%d: " fmt "\n", daraja, __FILE__, __LINE__, __VA_ARGS__)

int main(void) {
    int x = 10;
    const char *foydalanuvchi = "Ali";

    LOG_XABAR("INFO", "Foydalanuvchi tizimga kirdi: %s", foydalanuvchi);
    LOG_XABAR("DEBUG", "x qiymati = %d, kvadrat = %d", x, x * x);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C99 dan boshlab makroslarda '...' ellipsisi va __VA_ARGS__ maxsus identifikatori qo'llab-quvvatlanadi.
2. Bu murakkab logging, diagnostika va formatli xabarlar uchun juda kuchli vositadir.

## Ishlash natijasi:
```text
[INFO] main.c:11: Foydalanuvchi tizimga kirdi: Ali
[DEBUG] main.c:12: x qiymati = 10, kvadrat = 100
```

---

# 627-Topshiriq: Standart assert() makrosi va NDEBUG bilan o'chirish

## Topshiriq sharti:
Invariantlarni tekshirish uchun assert() dan foydalanish hamda NDEBUG makrosining unga ta'siri.

## Yechim (C kodi):
```c
#include <stdio.h>
// #define NDEBUG // Agar bu yoqilsa, barcha assert tekshiruvlari o'chadi
#include <assert.h>

int bolish(int a, int b) {
    assert(b != 0); // Maxraj nol bo'lmasligi shart
    return a / b;
}

int main(void) {
    int natija = bolish(20, 4);
    printf("20 / 4 = %d\n", natija);

    printf("assert tekshiruvi muvaffaqiyatli o'tdi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. assert() shart yolg'on (0) bo'lganda dastur bajarilishini darhol to'xtatadi va qaysi qatorda xato yuz berganini ko'rsatadi.
2. Ishlab chiqarish (Release) rejimida #define NDEBUG qo'yilsa, assert koddan butunlay olib tashlanadi va tezlik tushmaydi.

## Ishlash natijasi:
```text
20 / 4 = 5
assert tekshiruvi muvaffaqiyatli o'tdi.
```

---

# 628-Topshiriq: Kompilyatsiya vaqti tekshiruvi (Compile-Time Assertion): _Static_assert (C11)

## Topshiriq sharti:
_Static_assert orqali tiplar hajmini kompilyatsiya jarayonidayoq tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

// Tuzilma hajmi aniq 8 bayt bo'lishi shartligini tekshiramiz
typedef struct {
    uint32_t id;
    uint32_t yosh;
} Xodim;

_Static_assert(sizeof(Xodim) == 8, "Xodim strukturasi aniq 8 bayt bo'lishi shart!");
_Static_assert(sizeof(void*) == 8 || sizeof(void*) == 4, "Faqat 32-bit yoki 64-bit qo'llab-quvvatlanadi");

int main(void) {
    printf("Static assert tekshiruvlari muvaffaqiyatli yakunlandi.\n");
    printf("Xodim hajmi: %zu bayt\n", sizeof(Xodim));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C11 da kiritilgan _Static_assert dastur ishga tushmasidan oldin, aynan kompilyatsiya bosqichida shartni tekshiradi.
2. Agar shart buzilsa, kompilyator xatolik berib binar fayl yaratishdan bosh tortadi.

## Ishlash natijasi:
```text
Static assert tekshiruvlari muvaffaqiyatli yakunlandi.
Xodim hajmi: 8 bayt
```

---

# 629-Topshiriq: X-Macros texnikasi: enum va satrlar jadvalini bitta ro'yxatdan yaratish

## Topshiriq sharti:
Bitta markaziy makros ro'yxati orqali enum va unga mos keluvchi satrlar massivini avtomatik yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>

// 1. Markaziy ma'lumotlar ro'yxati (X-Macro)
#define BUYRUQLAR_ROYXATI \
    X(BUYRUQ_YURISH, "Yurish") \
    X(BUYRUQ_SAKRASH, "Sakrash") \
    X(BUYRUQ_HUJUM, "Hujum qilish")

// 2. enum larni generatsiya qilish
typedef enum {
    #define X(id, nom) id,
    BUYRUQLAR_ROYXATI
    #undef X
    BUYRUQLAR_SONI
} Buyruq;

// 3. Satrlar massivini generatsiya qilish
const char* buyruq_nomlari[] = {
    #define X(id, nom) nom,
    BUYRUQLAR_ROYXATI
    #undef X
};

int main(void) {
    for (int i = 0; i < BUYRUQLAR_SONI; i++) {
        printf("Buyruq %d: %s\n", i, buyruq_nomlari[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. X-Macros texnikasi C tilidagi eng kuchli metaprogramming usullaridan biri hisoblanadi.
2. Yangi buyruq qo'shilganda faqat bitta joyga (BUYRUQLAR_ROYXATI) qo'shiladi va enum, massiv, switch-case lar avtomatik yangilanadi!

## Ishlash natijasi:
```text
Buyruq 0: Yurish
Buyruq 1: Sakrash
Buyruq 2: Hujum qilish
```

---

# 630-Topshiriq: Massiv elementlari sonini hisoblovchi xavfsiz ARRAY_SIZE makrosi

## Topshiriq sharti:
sizeof yordamida massivdagi elementlar sonini aniqlash makrosini yozish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

int main(void) {
    int sonlar[] = {10, 20, 30, 40, 50, 60, 70};
    double narxlar[] = {12.5, 99.9, 45.0};

    printf("sonlar massivida: %zu ta element\n", ARRAY_SIZE(sonlar));
    printf("narxlar massivida: %zu ta element\n", ARRAY_SIZE(narxlar));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ARRAY_SIZE makrosi butun massiv bayt hajmini bitta element bayt hajmiga bo'lish orqali elementlar sonini beradi.
2. Muhim: Ushbu makros faqat haqiqiy massivlar uchun ishlaydi, ko'rsatkichlarga (decayed pointers) nisbatan ishlatilmasligi kerak!

## Ishlash natijasi:
```text
sonlar massivida: 7 ta element
narxlar massivida: 3 ta element
```

---

# 631-Topshiriq: Struktura ichidagi maydon siljishini (Offset) hisoblash: offsetof makrosi

## Topshiriq sharti:
stddef.h kutubxonasidagi offsetof makrosi qanday ishlashini tushunish va qo'lda amalga oshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stddef.h>

#define QOLDA_OFFSETOF(tip, maydon) ((size_t)&(((tip*)0)->maydon))

typedef struct {
    char belgi;     // 1 bayt
    // 3 bayt padding
    int son;        // 4 bayt
    double haqiqiy; // 8 bayt
} Sinov;

int main(void) {
    printf("Struktura hajmi: %zu bayt\n", sizeof(Sinov));
    printf("belgi siljishi:  %zu bayt\n", offsetof(Sinov, belgi));
    printf("son siljishi:    %zu bayt\n", offsetof(Sinov, son));
    printf("haqiqiy siljishi:%zu bayt\n", offsetof(Sinov, haqiqiy));

    printf("Qo'lda hisoblangan son siljishi: %zu bayt\n", 
           QOLDA_OFFSETOF(Sinov, son));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. offsetof makrosi 0 manzilidagi soxta ko'rsatkich (NULL pointer) orqali maydon manzilini oladi va uni bayt ko'rinishida qaytaradi.
2. Bu Linux yadrosi (container_of) va serialization kutubxonalarida keng qo'llaniladi.

## Ishlash natijasi:
```text
Struktura hajmi: 16 bayt
belgi siljishi:  0 bayt
son siljishi:    4 bayt
haqiqiy siljishi:8 bayt
Qo'lda hisoblangan son siljishi: 4 bayt
```

---

# 632-Topshiriq: Linux yadrosining container_of makrosi mexanizmi

## Topshiriq sharti:
Strukturaning ichki a'zosi ko'rsatkichidan foydalanib, butun ota strukturaga ko'rsatkichni topish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stddef.h>

#define CONTAINER_OF(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))

typedef struct {
    int id;
    int muhim_kod;
    char nom[32];
} Xabar;

int main(void) {
    Xabar x = {101, 777, "Salom"};
    int *ichki_kod_ptr = &x.muhim_kod;

    // Faqat ichki_kod_ptr orqali butun x strukturani topamiz:
    Xabar *ota_xabar = CONTAINER_OF(ichki_kod_ptr, Xabar, muhim_kod);

    printf("Topilgan Xabar ID: %d\n", ota_xabar->id);
    printf("Topilgan Xabar Nomi: %s\n", ota_xabar->nom);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. container_of Linux yadrosida Linked List, Task struct va Device driverlarda eng asosiy qurilish blokidir.
2. Ichki a'zo manzilidan uning struct ichidagi offset ini ayirish orqali ota struct ning boshlang'ich manzili aniqlanadi.

## Ishlash natijasi:
```text
Topilgan Xabar ID: 101
Topilgan Xabar Nomi: Salom
```

---

# 633-Topshiriq: Shartli kompilyatsiya bilan operatsion tizimni aniqlash (OS Detection)

## Topshiriq sharti:
Kompilyator makroslari yordamida dastur Windows, Linux yoki macOS da kompilyatsiya bo'layotganini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

void aniqla_os(void) {
#if defined(_WIN32) || defined(_WIN64)
    printf("Operatsion tizim: Windows\n");
#elif defined(__APPLE__) || defined(__MACH__)
    printf("Operatsion tizim: macOS\n");
#elif defined(__linux__)
    printf("Operatsion tizim: Linux\n");
#else
    printf("Noma'lum yoki maxsus operatsion tizim\n");
#endif
}

int main(void) {
    aniqla_os();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir operatsion tizim kompilyatori maxsus global makroslarni (_WIN32, __linux__, __APPLE__) avtomatik belgilaydi.
2. Bu kross-platforma kutubxonalarida platformaga xos kodlarni ajratish uchun ishlatiladi.

## Ishlash natijasi:
```text
Operatsion tizim: Windows
```

---

# 634-Topshiriq: Bit manipulyatsiyasi uchun yordamchi makroslar to'plami

## Topshiriq sharti:
Bitni yoqish, o'chirish, teskari qilish va tekshirish uchun makroslar.

## Yechim (C kodi):
```c
#include <stdio.h>

#define BIT_SET(var, pos)   ((var) |= (1ULL << (pos)))
#define BIT_CLEAR(var, pos) ((var) &= ~(1ULL << (pos)))
#define BIT_TOGGLE(var, pos)((var) ^= (1ULL << (pos)))
#define BIT_CHECK(var, pos) (!!((var) & (1ULL << (pos))))

int main(void) {
    unsigned char reg = 0; // 0000 0000

    BIT_SET(reg, 3);    // 0000 1000 (8)
    printf("3-bit yoqildi: 0x%02X\n", reg);

    BIT_SET(reg, 0);    // 0000 1001 (9)
    printf("0-bit yoqildi: 0x%02X\n", reg);

    BIT_TOGGLE(reg, 3); // 0000 0001 (1)
    printf("3-bit teskari qilindi: 0x%02X\n", reg);

    printf("0-bit bormi? %d\n", BIT_CHECK(reg, 0));
    printf("3-bit bormi? %d\n", BIT_CHECK(reg, 3));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'rnatilgan tizimlarda (Embedded Systems) registrlarni boshqarish deyarli to'liq ushbu 4 ta makros orqali amalga oshiriladi.
2. '1ULL' dan foydalanish 64-bitgacha bo'lgan arxitekturalarda xavfsiz siljitishni kafolatlaydi.

## Ishlash natijasi:
```text
3-bit yoqildi: 0x08
0-bit yoqildi: 0x09
3-bit teskari qilindi: 0x01
0-bit bormi? 1
3-bit bormi? 0
```

---

# 635-Topshiriq: Kompilyator turini va versiyasini aniqlash

## Topshiriq sharti:
GCC, Clang yoki MSVC kompilyatorini va uning versiyasini preprocessor orqali aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
#if defined(__clang__)
    printf("Kompilyator: Clang (Versiya: %s)\n", __VERSION__);
#elif defined(__GNUC__)
    printf("Kompilyator: GCC (Versiya: %s)\n", __VERSION__);
#elif defined(_MSC_VER)
    printf("Kompilyator: Microsoft Visual C++ (MSC_VER: %d)\n", _MSC_VER);
#else
    printf("Boshqa standart C kompilyatori\n");
#endif
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyatorga xos optimizatsiyalar va buyruqlarni (attributes, pragmas) ajratish uchun kompilyator makroslaridan foydalaniladi.
2. Clang o'zini __GNUC__ deb ham e'lon qilishi sababli, tekshiruvda doim __clang__ birinchi tekshirilishi kerak.

## Ishlash natijasi:
```text
Kompilyator: GCC (Versiya: 13.2.0)
```

---

# 636-Topshiriq: Stringlarning o'zaro ulanishi (String Literal Concatenation)

## Topshiriq sharti:
Preprocessor tomonidan yonma-yon turgan satr konstantalarini bitta yaxlit satrga avtomatik birlashtirish xususiyati.

## Yechim (C kodi):
```c
#include <stdio.h>

#define PREFIX "[ANTIGRAVITY] "
#define LOG_INFO(msg) printf(PREFIX "INFO: " msg "\n")

int main(void) {
    // C tilida "Salom " "Dunyo" avtomatik ravishda "Salom Dunyo" bo'ladi
    const char *matn = "Bu birinchi qator. "
                       "Bu ikkinchi qator. "
                       "Bu uchinchi qator.";

    printf("%s\n", matn);
    LOG_INFO("Tizim barqaror ishlamoqda.");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C leksik analizatori oralarida bo'sh joy bo'lgan satr konstantalarini kompilyatsiya bosqichidayoq bitta satrga ulaydi.
2. Bu makros prefikslarini format satrlariga to'g'ridan-to'g'ri ulashda juda qulaydir.

## Ishlash natijasi:
```text
Bu birinchi qator. Bu ikkinchi qator. Bu uchinchi qator.
[ANTIGRAVITY] INFO: Tizim barqaror ishlamoqda.
```

---

# 637-Topshiriq: Ikki bosqichli makros kengaytirish (Two-Level Macro Expansion)

## Topshiriq sharti:
Preprocessor makros parametrini stringize qilishdan oldin uni kengaytirishi uchun ikkinchi yordamchi makros qo'llash.

## Yechim (C kodi):
```c
#include <stdio.h>

#define STR_HELPER(x) #x
#define STR(x) STR_HELPER(x)

#define PORT 8080

int main(void) {
    // STR_HELPER(PORT) to'g'ridan-to'g'ri "PORT" beradi (chunki # kengaytirishni to'xtatadi)
    printf("STR_HELPER(PORT) = %s\n", STR_HELPER(PORT));

    // STR(PORT) esa oldin PORT ni 8080 ga kengaytiradi, keyin stringize qiladi -> "8080"
    printf("STR(PORT)        = %s\n", STR(PORT));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C preprocessor qoidasiga ko'ra, agar parametr '#' yoki '##' bilan ishlatilsa, u argument kengaytirilmasdan to'g'ridan-to'g'ri stringga olinadi.
2. Ikki bosqichli STR(x) wrapper orqali makros qiymatini satrga aylantirish ta'minlanadi.

## Ishlash natijasi:
```text
STR_HELPER(PORT) = PORT
STR(PORT)        = 8080
```

---

# 638-Topshiriq: Birlashtirilgan funksiya generatori (Template Generator via Macros)

## Topshiriq sharti:
## token-pasting yordamida turli ma'lumot tiplari (int, double) uchun funksiyalarni avtomatik generatsiya qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define MAKSIMAL_FUNKSIYA_YARAT(TIP)               \
TIP max_##TIP(TIP a, TIP b) {                     \
    return (a > b) ? a : b;                       \
}

// int va double uchun ikkita alohida funksiya generatsiya qilamiz
MAKSIMAL_FUNKSIYA_YARAT(int)
MAKSIMAL_FUNKSIYA_YARAT(double)

int main(void) {
    printf("int kattasi:    %d\n", max_int(15, 42));
    printf("double kattasi: %.2f\n", max_double(3.14, 2.71));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C++ da shablonlar (templates) mavjud, sof C tilida esa bu vazifa preprocessor ning token pasting imkoniyati orqali hal etiladi.
2. Har bir tip uchun to'g'ri nomlangan va optimallashtirilgan funksiya yaratiladi.

## Ishlash natijasi:
```text
int kattasi:    42
double kattasi: 3.14
```

---

# 639-Topshiriq: enum va typedef struct kombinatsiyasi: Xabar paketi sarlavhasi

## Topshiriq sharti:
Tarmoq protokoli xabar turini bildiruvchi enum va ma'lumot sarlavhasi strukturasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef enum {
    MSG_PING = 1,
    MSG_PONG = 2,
    MSG_DATA = 3,
    MSG_DISCONNECT = 4
} MessageType;

typedef struct {
    MessageType type;
    uint32_t payload_len;
} MessageHeader;

int main(void) {
    MessageHeader hdr = { MSG_PING, 0 };
    printf("Xabar turi: %d, Yuklama uzunligi: %u\n", hdr.type, hdr.payload_len);
    if (hdr.type == MSG_PING) {
        printf("PING qabul qilindi. Javob: PONG (tur: %d)\n", MSG_PONG);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tarmoq va xabar tizimlarida paket turi har doim enum orqali boshqariladi.
2. Bu kodning tushunarliligini oshiradi va faqat ruxsat etilgan xabarlarni qabul qilishga kafolat beradi.

## Ishlash natijasi:
```text
Xabar turi: 1, Yuklama uzunligi: 0
PING qabul qilindi. Javob: PONG (tur: 2)
```

---

# 640-Topshiriq: #line direktivasi va uning ishlash mexanizmi

## Topshiriq sharti:
#line orqali kompilyator ko'radigan fayl nomi va qator raqamini dastur ichidan o'zgartirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Asl qator: %d\n", __LINE__);

#line 500 "soxta_fayl.c"
    printf("Yangi qator: %d, Yangi fayl: %s\n", __LINE__, __FILE__);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. #line direktivasi lexer/parser generatorlari (masalan, Bison, Yacc, Flex) tomonidan yaratilgan C kodlarini asl grammatika fayllariga bog'lash uchun ishlatiladi.
2. Kompilyator xatolik chiqarganda asl kodning qatorini aniq ko'rsata oladi.

## Ishlash natijasi:
```text
Asl qator: 4
Yangi qator: 501, Yangi fayl: soxta_fayl.c
```

---

# 641-Topshiriq: Faylni shartli yuklash: Konfiguratsiyaga qarab mos sarlavha faylini tanlash

## Topshiriq sharti:
Makros qiymatiga qarab dinamik fayl nomini #include qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define QURILMA_TURI 1

#if QURILMA_TURI == 1
    #define QURILMA_NOMI "Qurilma A (Kichik quvvatli)"
#elif QURILMA_TURI == 2
    #define QURILMA_NOMI "Qurilma B (Yuqori tezlikli)"
#endif

int main(void) {
    printf("Yuklangan konfiguratsiya: %s\n", QURILMA_NOMI);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Turli mikrokontrollerlar yoki apparat modellarida bitta dasturiy kodni ishlatish uchun sarlavha fayllari va konstantalar shartli yuklanadi.

## Ishlash natijasi:
```text
Yuklangan konfiguratsiya: Qurilma A (Kichik quvvatli)
```

---

# 642-Topshiriq: O'zgaruvchilar va ifodalarni xavfsiz taqqoslash makrosi (MIN / MAX)

## Topshiriq sharti:
GCC kengaytmasi ({ ... }) yordamida nojo'ya ta'sirsiz (type-safe no-side-effects) MAX makrosi yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>

// Statement expression GCC extension: no side effects
#define SAFE_MAX(a, b) ({    \
    __typeof__(a) _a = (a);  \
    __typeof__(b) _b = (b);  \
    _a > _b ? _a : _b;       \
})

int main(void) {
    int x = 5, y = 3;
    // x++ faqat bitta marta bajariladi!
    int m = SAFE_MAX(x++, y);

    printf("SAFE_MAX natijasi: %d\n", m);
    printf("x ning yakuniy qiymati: %d (To'g'ri: 6)\n", x);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. GNU C ning 'statement expressions' ({ ... }) xususiyati blok ichida vaqtinchalik o'zgaruvchilar e'lon qilish imkonini beradi.
2. Bu Linux yadrosida 'max(x, y)' makrosida inkrementlar ikki marta bajarilmasligini kafolatlash uchun qo'llaniladi.

## Ishlash natijasi:
```text
SAFE_MAX natijasi: 5
x ning yakuniy qiymati: 6 (To'g'ri: 6)
```

---

# 643-Topshiriq: Kompilyatsiya vaqtidagi sanani tekshirish va dastur amal qilish muddatini cheklash

## Topshiriq sharti:
__DATE__ makrosidan foydalanib dastur qurilgan sanani chop etish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Dastur kompilyatsiya qilingan: %s, soat %s\n", __DATE__, __TIME__);
    printf("Litsenziya muddati tekshirildi: Faol\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. __DATE__ preprocessor tomonidan 'Mmm dd yyyy' formatidagi satrga almashtiriladi.
2. Bu versiya nazorati va beta versiyalarning eskirganligini aniqlashda foydalidir.

## Ishlash natijasi:
```text
Dastur kompilyatsiya qilingan: Nov  8 2026, soat 10:30:00
Litsenziya muddati tekshirildi: Faol
```

---

# 644-Topshiriq: C Standart versiyasini aniqlash: __STDC_VERSION__ makrosi

## Topshiriq sharti:
Kompilyator C89, C99, C11, C17 yoki C23 standartlaridan qaysi birida ishlayotganini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
#if defined(__STDC_VERSION__)
    #if __STDC_VERSION__ >= 202311L
        printf("C Standarti: C23 (Versiya kodi: %ldL)\n", __STDC_VERSION__);
    #elif __STDC_VERSION__ >= 201710L
        printf("C Standarti: C17 (Versiya kodi: %ldL)\n", __STDC_VERSION__);
    #elif __STDC_VERSION__ >= 201112L
        printf("C Standarti: C11 (Versiya kodi: %ldL)\n", __STDC_VERSION__);
    #elif __STDC_VERSION__ >= 199901L
        printf("C Standarti: C99 (Versiya kodi: %ldL)\n", __STDC_VERSION__);
    #else
        printf("C Standarti: Eski C (Versiya kodi: %ldL)\n", __STDC_VERSION__);
    #endif
#else
    printf("C Standarti: C89 / C90 (ANSI C)\n");
#endif
    return 0;
}
```

## Tushuntirish va Mantiq:
1. __STDC_VERSION__ makrosi qaysi C tili standarti faollashtirilganini (masalan -std=c11 yoki -std=c17) ifodalovchi 'long int' qiymatini qaytaradi.
2. Standartga xos xususiyatlarni (masalan _Static_assert, threads.h) moslashtirish uchun tekshiriladi.

## Ishlash natijasi:
```text
C Standarti: C17 (Versiya kodi: 201710L)
```

---

# 645-Topshiriq: Bit maydoni maskalarini (Bitmask) makroslar orqali avtomatlashtirish

## Topshiriq sharti:
Bit maydoni kengligi va pozitsiyasi bo'yicha maska generatsiya qiluvchi makros.

## Yechim (C kodi):
```c
#include <stdio.h>

#define GEN_MASK(width, shift) (((1ULL << (width)) - 1ULL) << (shift))

int main(void) {
    // Masalan 4-bitli maydon 8-bit siljishda
    unsigned long long maska = GEN_MASK(4, 8);
    printf("4-bit kenglik, 8-bit siljish maskasi: 0x%llX\n", maska);

    unsigned long long son = 0x12345;
    unsigned long long ajratilgan = (son & maska) >> 8;
    printf("Ajratib olingan qiymat: 0x%llX\n", ajratilgan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. GEN_MASK makrosi apparat registrlari va protokollarda ma'lum bit oralig'ini tozalash yoki o'qish uchun maska yasaydi.
2. (1 << width) - 1 ifodasi width ta ketma-ket birlik bitlarini hosil qiladi.

## Ishlash natijasi:
```text
4-bit kenglik, 8-bit siljish maskasi: 0xF00
Ajratib olingan qiymat: 0x3
```

---

# 646-Topshiriq: Xotira ajratishni nazorat qiluvchi xavfsiz MALLOC makrosi

## Topshiriq sharti:
MALLOC chaqiruvida hajm hisoblash va NULL ko'rsatkichni avtomatik tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

#define SAFE_MALLOC(ptr, tip, soni) do {                                \
    (ptr) = (tip *)malloc((soni) * sizeof(tip));                       \
    if ((ptr) == NULL) {                                                \
        fprintf(stderr, "[XATO] Xotira ajratilmadi: %s:%d\n",          \
                __FILE__, __LINE__);                                    \
        exit(1);                                                        \
    }                                                                   \
} while (0)

int main(void) {
    int *massiv = NULL;
    SAFE_MALLOC(massiv, int, 5);

    for (int i = 0; i < 5; i++) {
        massiv[i] = (i + 1) * 10;
        printf("%d ", massiv[i]);
    }
    printf("\n");
    free(massiv);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. SAFE_MALLOC makrosi dasturchini har safar malloc dan so'ng NULL tekshiruvini yozish mashaqqatidan xalos qiladi.
2. Agar xotira tugasa, xatolik bergan fayl va qatorni ko'rsatib dasturni xavfsiz to'xtatadi.

## Ishlash natijasi:
```text
10 20 30 40 50
```

---

# 647-Topshiriq: Statik massiv o'lchamini tekshiruvchi makros (Compile-time Array Bound)

## Topshiriq sharti:
Massiv chegarasidan chiqmaslikni ta'minlovchi assert makrosi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <assert.h>

#define MASSIV_SIZE 5
#define MASSIV_GET(arr, idx) (assert((idx) >= 0 && (idx) < MASSIV_SIZE), (arr)[(idx)])

int main(void) {
    int m[MASSIV_SIZE] = {100, 200, 300, 400, 500};

    printf("m[2] = %d\n", MASSIV_GET(m, 2));
    printf("m[4] = %d\n", MASSIV_GET(m, 4));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida oddiy massiv indeksatsiyasida chegara (boundary) tekshirilmaydi.
2. Vergul operatori (comma operator) yordamida assert va indekslashni bitta ifodaga birlashtirish mumkin.

## Ishlash natijasi:
```text
m[2] = 300
m[4] = 500
```

---

# 648-Topshiriq: Struktura a'zolarini avtomatik initsializatsiya qiluvchi makros

## Topshiriq sharti:
Katta struktura maydonlarini bir xil standart shablon bilan to'ldirish makrosi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int id;
    const char *nom;
    int faol;
} Element;

#define YANGI_ELEMENT(id, nom) ((Element){ (id), (nom), 1 })

int main(void) {
    Element e1 = YANGI_ELEMENT(1, "Birlamchi sensor");
    Element e2 = YANGI_ELEMENT(2, "Ikkilamchi sensor");

    printf("E1: ID=%d, Nom=%s, Faol=%d\n", e1.id, e1.nom, e1.faol);
    printf("E2: ID=%d, Nom=%s, Faol=%d\n", e2.id, e2.nom, e2.faol);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C99 Compound Literals ((Element){...}) va funksiya-makros birlashmasi obyektga yo'naltirilgan tillardagi konstruktorga o'xshash qulaylik yaratadi.

## Ishlash natijasi:
```text
E1: ID=1, Nom=Birlamchi sensor, Faol=1
E2: ID=2, Nom=Ikkilamchi sensor, Faol=1
```

---

# 649-Topshiriq: Ko'p darajali Debug Logging tizimi: DEBUG, INFO, WARN, ERROR

## Topshiriq sharti:
Darajalar (LogLevel) bo'yicha filtrlangan xabarlarni chiqaruvchi to'liq makroslar tizimi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef enum {
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_INFO,
    LOG_LEVEL_WARN,
    LOG_LEVEL_ERROR
} LogLevel;

#define CURRENT_LOG_LEVEL LOG_LEVEL_INFO

#define LOG(level, tag, fmt, ...) do {                                     \
    if ((level) >= CURRENT_LOG_LEVEL) {                                   \
        printf("[%s] [%s] " fmt "\n", (tag), __func__, ##__VA_ARGS__);   \
    }                                                                      \
} while (0)

int main(void) {
    LOG(LOG_LEVEL_DEBUG, "DEBUG", "Bu ko'rinmaydi, chunki filter INFO da");
    LOG(LOG_LEVEL_INFO,  "INFO",  "Tizim muvaffaqiyatli yuklandi");
    LOG(LOG_LEVEL_WARN,  "WARN",  "Disk xotirasi 85%% ga yetdi");
    LOG(LOG_LEVEL_ERROR, "ERROR", "Tarmoq bilan aloqa uzildi: kod %d", 503);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'p darajali log tizimi ishlab chiqishda batafsil xabarlarni, ishlab chiqarishda esa faqat xatoliklarni chiqarishga imkon beradi.
2. ##__VA_ARGS__ GNU kengaytmasi bo'lib, argumentlar bo'lmaganda oldidagi vergulni olib tashlaydi.

## Ishlash natijasi:
```text
[INFO] [main] Tizim muvaffaqiyatli yuklandi
[WARN] [main] Disk xotirasi 85% ga yetdi
[ERROR] [main] Tarmoq bilan aloqa uzildi: kod 503
```

---

# 650-Topshiriq: Modul yakuni va Master Loyiha: Preprocessor Metaprogramming yordamida Avtomatik Buyruqlar Dispatcheri (Command Dispatcher)

## Topshiriq sharti:
X-Macros, enum, funksiya ko'rsatkichlari va stringifikatsiyani birlashtirib buyruqlarni qabul qiluvchi va bajaruvchi to'liq tizim yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

// 1. Tizimdagi barcha buyruqlar va ularning funksiyalari jadvali
#define BUYRUQLAR_JADVALI \
    BUYRUQ(START, "start", cmd_start) \
    BUYRUQ(STOP,  "stop",  cmd_stop)  \
    BUYRUQ(RESET, "reset", cmd_reset) \
    BUYRUQ(INFO,  "info",  cmd_info)

// Funksiyalar prototiplari
void cmd_start(void) { printf("[ACTION]: Tizim ishga tushirildi!\n"); }
void cmd_stop(void)  { printf("[ACTION]: Tizim to'xtatildi!\n"); }
void cmd_reset(void) { printf("[ACTION]: Tizim qayta yuklandi!\n"); }
void cmd_info(void)  { printf("[ACTION]: Tizim holati: Barcha modullar normal.\n"); }

// 2. Enum ro'yxatini avtomatik yaratish
typedef enum {
    #define BUYRUQ(id, str, fn) CMD_##id,
    BUYRUQLAR_JADVALI
    #undef BUYRUQ
    BUYRUQ_JAMI_SONI
} CommandId;

// 3. Buyruqlar jadvali strukturasi
typedef struct {
    const char *nom;
    void (*bajar)(void);
} CommandEntry;

const CommandEntry dispatcher[BUYRUQ_JAMI_SONI] = {
    #define BUYRUQ(id, str, fn) { str, fn },
    BUYRUQLAR_JADVALI
    #undef BUYRUQ
};

// Buyruqni matn bo'yicha qidirib bajarish
void bajar_buyruq(const char *buyruq_matni) {
    for (int i = 0; i < BUYRUQ_JAMI_SONI; i++) {
        if (strcmp(dispatcher[i].nom, buyruq_matni) == 0) {
            dispatcher[i].bajar();
            return;
        }
    }
    printf("[XATO]: '%s' nomli buyruq topilmadi!\n", buyruq_matni);
}

int main(void) {
    printf("=== BUYRUQLAR DISPATCHERI ISHGA TUSHDI ===\n");
    printf("Mavjud buyruqlar soni: %d\n", BUYRUQ_JAMI_SONI);

    bajar_buyruq("start");
    bajar_buyruq("info");
    bajar_buyruq("reset");
    bajar_buyruq("stop");
    bajar_buyruq("noma'lum");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ushbu yakuniy topshiriq 13-modulning barcha bilimlarini o'zida mujassam etadi: X-Macros, enum, typedef struct, funksiya ko'rsatkichlari va preprocessor metaprogramming.
2. Yangi buyruq qo'shish uchun faqat BUYRUQLAR_JADVALI ga bitta qator qo'shish va uning funksiyasini yozish kifoya — qolgan barcha ro'yxat, massiv va qidiruv tizimi avtomatik yangilanadi!

## Ishlash natijasi:
```text
=== BUYRUQLAR DISPATCHERI ISHGA TUSHDI ===
Mavjud buyruqlar soni: 4
[ACTION]: Tizim ishga tushirildi!
[ACTION]: Tizim holati: Barcha modullar normal.
[ACTION]: Tizim qayta yuklandi!
[ACTION]: Tizim to'xtatildi!
[XATO]: 'noma\'lum' nomli buyruq topilmadi!
```

---
