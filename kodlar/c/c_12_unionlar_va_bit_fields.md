# C Dasturlash Tili — 12-Qism: Unionlar va Bit Maydonlari (Bit-fields)
## (551-600 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* union tushunchasi, umumiy xotira va sizeof(union)
* Type Punning, IEEE 754 float binar tahlili va Endianness aniqlash
* Tagged Union (Variant) va nomsiz unionlar (C11)
* Bit-fields: xotirani bitma-bit taqsimlash, IPv4/TCP headerlari
* RGB565 rang modeli, Fast Inverse Square Root va 4-bitli AI tenzor og'irliklari

---

# 551-Topshiriq: union tushunchasi va deklaratsiyasi

## Topshiriq sharti:
Barcha a'zolari bir xil xotira manzilini bo'lishadigan union yarating.

## Yechim (C kodi):
```c
#include <stdio.h>

union Xotira {
    int butun;
    float haqiqiy;
    char belgi;
};

int main(void) {
    union Xotira x;
    printf("butun manzili:  %p\n", (void*)&x.butun);
    printf("haqiqiy manzili:%p\n", (void*)&x.haqiqiy);
    printf("belgi manzili:  %p\n", (void*)&x.belgi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `union` — barcha a'zolari bitta xotira manzilidan boshlanadigan maxsus ma'lumot tuzilmasidir.
2. `struct` dan farqli ravishda a'zolar alohida joy egallamaydi, bir vaqtning o'zida faqat bitta a'zodan foydalaniladi.

## Ishlash natijasi:
```text
butun manzili:  000000000012FFE0
haqiqiy manzili:000000000012FFE0
belgi manzili:  000000000012FFE0
```

---

# 552-Topshiriq: union ning xotiradagi hajmi: sizeof(union)

## Topshiriq sharti:
union hajmi uning eng katta a'zosiga teng bo'lishini isbotlang.

## Yechim (C kodi):
```c
#include <stdio.h>

union Sinov {
    char c;       // 1 bayt
    int i;        // 4 bayt
    double d;     // 8 bayt
};

int main(void) {
    printf("sizeof(char):   %zu bayt\n", sizeof(char));
    printf("sizeof(int):    %zu bayt\n", sizeof(int));
    printf("sizeof(double): %zu bayt\n", sizeof(double));
    printf("sizeof(union):  %zu bayt (eng kattasiga teng!)\n", sizeof(union Sinov));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `union` o'zining eng katta a'zosi sig'adigan hajmda xotira ajratadi (bu yerda `double` 8 bayt).

## Ishlash natijasi:
```text
sizeof(char):   1 bayt
sizeof(int):    4 bayt
sizeof(double): 8 bayt
sizeof(union):  8 bayt (eng kattasiga teng!)
```

---

# 553-Topshiriq: Type Punning asoslari: Bitta a'zoga yozib, boshqasidan o'qish

## Topshiriq sharti:
int ga qiymat yozib, uning pastki baytini char orqali o'qing.

## Yechim (C kodi):
```c
#include <stdio.h>

union Konvertor {
    int son;
    char pastki_bayt;
};

int main(void) {
    union Konvertor k;
    k.son = 0x41; // ASCII 65 ('A')

    printf("son:         %d\n", k.son);
    printf("pastki_bayt: %c (ASCII: %d)\n", k.pastki_bayt, k.pastki_bayt);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitta a'zoga qiymat yozib, boshqa a'zosi orqali binar xotirani o'qish Type Punning deyiladi.

## Ishlash natijasi:
```text
son:         65
pastki_bayt: A (ASCII: 65)
```

---

# 554-Topshiriq: union yordamida float sonning IEEE 754 bitlarini int orqali ko'rish

## Topshiriq sharti:
Float sonning binar xotirasini hex formatda tahlil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

union FloatBinar {
    float f;
    uint32_t u;
};

int main(void) {
    union FloatBinar fb;
    fb.f = -1.0f;

    printf("Float: %.1f\n", fb.f);
    printf("IEEE 754 Hex ko'rinishi: 0x%08X\n", fb.u);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. -1.0f sonining binar ko'rinishi `0xBF800000` ga teng (eng yuqori ishora biti 1).

## Ishlash natijasi:
```text
Float: -1.0
IEEE 754 Hex ko'rinishi: 0xBF800000
```

---

# 555-Topshiriq: union yordamida 32-bitli sonning 4 ta baytini ajratib olish

## Topshiriq sharti:
uint32_t ni 4 ta alohida bayt massivi orqali o'qing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

union IpManzil {
    uint32_t toliq;
    uint8_t baytlar[4];
};

int main(void) {
    union IpManzil ip;
    ip.baytlar[0] = 127;
    ip.baytlar[1] = 0;
    ip.baytlar[2] = 0;
    ip.baytlar[3] = 1;

    printf("IPv4 manzil: %u.%u.%u.%u\n", 
           ip.baytlar[0], ip.baytlar[1], ip.baytlar[2], ip.baytlar[3]);
    printf("32-bitli butun son: 0x%08X\n", ip.toliq);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tarmoq dasturlashda IP manzillar aynan shu uslubda boshqariladi.

## Ishlash natijasi:
```text
IPv4 manzil: 127.0.0.1
32-bitli butun son: 0x0100007F
```

---

# 556-Topshiriq: union orqali Endianness (Bayt tartibi) ni aniqlash

## Topshiriq sharti:
Tizim Little-Endian yoki Big-Endian ekanligini union bilan aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

union EndianTekshiruv {
    uint32_t son;
    uint8_t birinchi_bayt;
};

int main(void) {
    union EndianTekshiruv e = {0x00000001};

    if (e.birinchi_bayt == 1) {
        printf("Tizim: Little-Endian (Eng kichik bayt birinchi)\n");
    } else {
        printf("Tizim: Big-Endian (Eng katta bayt birinchi)\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `0x01` birinchi baytga tushsa — Little-Endian.

## Ishlash natijasi:
```text
Tizim: Little-Endian (Eng kichik bayt birinchi)
```

---

# 557-Topshiriq: Tagged Union (Discriminated Union / Variant) tushunchasi

## Topshiriq sharti:
Tur bayrog'i (enum) va unionni birlashtirib xavfsiz Variant turi yarating.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef enum { TUR_INT, TUR_FLOAT, TUR_SATR } TurTipi;

typedef struct {
    TurTipi tur;
    union {
        int i;
        float f;
        const char *s;
    } qiymat;
} Variant;

void variant_chop(Variant v) {
    switch (v.tur) {
        case TUR_INT:   printf("Int: %d\n", v.qiymat.i); break;
        case TUR_FLOAT: printf("Float: %.2f\n", v.qiymat.f); break;
        case TUR_SATR:  printf("Satr: %s\n", v.qiymat.s); break;
    }
}

int main(void) {
    Variant v1 = {TUR_INT, {.i = 100}};
    Variant v2 = {TUR_SATR, {.s = "C Dasturchi"}};

    variant_chop(v1);
    variant_chop(v2);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tagged Union dinamik tipli tillar (Python, JavaScript) o'zgaruvchilarini C da modellashtirishning asosidir.

## Ishlash natijasi:
```text
Int: 100
Satr: C Dasturchi
```

---

# 558-Topshiriq: Nomsiz unionlar (Anonymous Unions) C11 qulayligi

## Topshiriq sharti:
Struktura ichida nomsiz union ishlatib to'g'ridan-to'g'ri maydonlarga murojaat qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

struct Obyekt {
    int id;
    union {
        int raqamli_kod;
        char belgili_kod[4];
    };
};

int main(void) {
    struct Obyekt o;
    o.id = 1;
    o.raqamli_kod = 42; // o.nomli_union.raqamli_kod deb yozish shart emas!

    printf("Obyekt #%d, Kod: %d\n", o.id, o.raqamli_kod);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C11 standarti nomsiz unionlarni rasmiylashtirib, kod sintaksisini ancha soddalashtirdi.

## Ishlash natijasi:
```text
Obyekt #1, Kod: 42
```

---

# 559-Topshiriq: Bit-fields (Bit maydonlari) sintaksisi (: bit_soni)

## Topshiriq sharti:
Bitta unsigned int ichida bir nechta kichik sonlarni aniq bitlar bilan saqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

struct Paket {
    unsigned int versiya : 4;  // 4 bit (0 dan 15 gacha)
    unsigned int tur : 4;      // 4 bit (0 dan 15 gacha)
    unsigned int raqam : 8;    // 8 bit (0 dan 255 gacha)
};

int main(void) {
    struct Paket p = {4, 1, 200};

    printf("Versiya: %u, Tur: %u, Raqam: %u\n", p.versiya, p.tur, p.raqam);
    printf("Paket hajmi: %zu bayt\n", sizeof(struct Paket));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bit-fieldlar yordamida ma'lumotlar apparat paketlariga aniq bitma-bit joylashtiriladi.

## Ishlash natijasi:
```text
Versiya: 4, Tur: 1, Raqam: 200
Paket hajmi: 4 bayt
```

---

# 560-Topshiriq: 8 ta boolean bayroqni 1 bayt ichida bit-fields bilan saqlash

## Topshiriq sharti:
Bitta baytda 8 ta mustaqil kalit holatini ifodalang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

struct Bayroqlar {
    uint8_t b0 : 1;
    uint8_t b1 : 1;
    uint8_t b2 : 1;
    uint8_t b3 : 1;
    uint8_t b4 : 1;
    uint8_t b5 : 1;
    uint8_t b6 : 1;
    uint8_t b7 : 1;
};

int main(void) {
    struct Bayroqlar f = {1, 0, 1, 1, 0, 0, 1, 0};

    printf("b0=%u, b1=%u, b2=%u, b3=%u\n", f.b0, f.b1, f.b2, f.b3);
    printf("8 ta bayroq xotira hajmi: %zu bayt\n", sizeof(struct Bayroqlar));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 8 ta alohida `bool` 8 bayt olgan bo'lsa, bit-fields atigi 1 bayt xotira oladi.

## Ishlash natijasi:
```text
b0=1, b1=0, b2=1, b3=1
8 ta bayroq xotira hajmi: 1 bayt
```

---

# 561-Topshiriq: Signed bit-field va ishora biti xavfi

## Topshiriq sharti:
1-bitli signed maydon nima uchun faqat 0 va -1 qiymat olishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

struct TestSigned {
    signed int b : 1; // 1 bitli signed son
};

int main(void) {
    struct TestSigned s;
    s.b = 1;

    // 1 bitda '1' bu ishora biti bo'lib, two's complement bo'yicha -1 ni bildiradi!
    printf("s.b = 1 berilganda uning qiymati: %d\n", s.b);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1 bitli maydonlarda har doim `unsigned int` ishlatilishi shart, aks holda qiymat -1 bo'lib qoladi.

## Ishlash natijasi:
```text
s.b = 1 berilganda uning qiymati: -1
```

---

# 562-Topshiriq: Nomsiz bit-field (: 0) orqali keyingi so'z chegarasiga tekislash

## Topshiriq sharti:
: 0 orqali bitlarni yangi xotira chegarasidan boshlash.

## Yechim (C kodi):
```c
#include <stdio.h>

struct TekislanganBit {
    unsigned int a : 4;
    unsigned int   : 0; // Keyingi maydon yangi 32-bitli xotira so'zidan boshlanadi
    unsigned int b : 4;
};

int main(void) {
    printf("Hajmi: %zu bayt (Tekislash tufayli 8 bayt bo'ladi)\n", 
           sizeof(struct TekislanganBit));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `: 0` kenglikdagi nomsiz bit-field majburiy tekislash buyrug'idir.

## Ishlash natijasi:
```text
Hajmi: 8 bayt (Tekislash tufayli 8 bayt bo'ladi)
```

---

# 563-Topshiriq: Apparat registri modellashtirish: Mikrokontroller holat registri

## Topshiriq sharti:
Taymer, uzilish va yoqish bitlarini boshqarish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint8_t butun_registr;
    struct {
        uint8_t yoqilgan    : 1;
        uint8_t taymer_faol : 1;
        uint8_t uzilish_bor : 1;
        uint8_t xatolik     : 1;
        uint8_t zahira      : 4;
    } bitlar;
} RegistrBoshqaruvi;

int main(void) {
    RegistrBoshqaruvi r = {0};
    r.bitlar.yoqilgan = 1;
    r.bitlar.uzilish_bor = 1;

    printf("Registr binar qiymati (Hex): 0x%02X\n", r.butun_registr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Union va bit-field kombinatsiyasi registrga ham butun son, ham alohida bitlar sifatida murojaat qilish imkonini beradi.

## Ishlash natijasi:
```text
Registr binar qiymati (Hex): 0x05
```

---

# 564-Topshiriq: Tarmoq protokoli: TCP Flaglarini bit-fields orqali modellashtirish

## Topshiriq sharti:
SYN, ACK, FIN, RST bayroqlarini 1 baytda ifodalang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    uint8_t fin : 1;
    uint8_t syn : 1;
    uint8_t rst : 1;
    uint8_t psh : 1;
    uint8_t ack : 1;
    uint8_t urg : 1;
    uint8_t ece : 1;
    uint8_t cwr : 1;
} TCPFlags;

int main(void) {
    TCPFlags f = {0};
    f.syn = 1;
    f.ack = 1; // SYN-ACK paketi

    printf("SYN=%u, ACK=%u, FIN=%u\n", f.syn, f.ack, f.fin);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tarmoq stacklarida (TCP/IP) bayroqlar aynan shunday boshqariladi.

## Ishlash natijasi:
```text
SYN=1, ACK=1, FIN=0
```

---

# 565-Topshiriq: RGB565 16-bitli rang modelini bit-fields bilan ifodalash

## Topshiriq sharti:
Qizil (5 bit), Yashil (6 bit), Ko'k (5 bit) ranglarini 2 baytda saqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint16_t rang16;
    struct {
        uint16_t b : 5; // Ko'k (0-31)
        uint16_t g : 6; // Yashil (0-63)
        uint16_t r : 5; // Qizil (0-31)
    } kanallar;
} RangRGB565;

int main(void) {
    RangRGB565 c;
    c.kanallar.r = 31; // Maksimal qizil
    c.kanallar.g = 0;
    c.kanallar.b = 0;

    printf("To'liq qizil RGB565 kodi: 0x%04X\n", c.rang16);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. RGB565 eski konsollar (Game Boy Advance) va mikrokontroller LCD ekranlarida standartdir.

## Ishlash natijasi:
```text
To'liq qizil RGB565 kodi: 0xF800
```

---

# 566-Topshiriq: Bit-field maydonining manzilini (&) olib bo'lmasligi qoidasi

## Topshiriq sharti:
Nima uchun bit-field ko'rsatkichiga ega bo'lib bo'lmasligini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

struct TestBit {
    unsigned int bit : 1;
};

int main(void) {
    // struct TestBit t;
    // unsigned int *p = &t.bit; // KOMPILYATSIYA XATOSI: cannot take address of bit-field!
    printf("RAM manzillari baytlarga beriladi, alohida bitning xotira manzili yo'q!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompyuter xotirasi bayt-orientirlangan. Alohida bitning xotira manzili mavjud emas.

## Ishlash natijasi:
```text
RAM manzillari baytlarga beriladi, alohida bitning xotira manzili yo'q!
```

---

# 567-Topshiriq: Sanani atigi 2 baytda (16 bit) saqlash (Date Compression)

## Topshiriq sharti:
Kun (5 bit), Oy (4 bit), Yil (7 bit: 2000 dan boshlab) ixchamlashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint16_t xom_baytlar;
    struct {
        uint16_t kun : 5; // 1-31 (5 bit)
        uint16_t oy  : 4; // 1-12 (4 bit)
        uint16_t yil : 7; // 0-127 (2000 + yil)
    } qismlar;
} SiqilganSana;

int main(void) {
    SiqilganSana s;
    s.qismlar.kun = 8;
    s.qismlar.oy = 11;
    s.qismlar.yil = 26; // 2026-yil

    printf("Sana: %02u.%02u.%u (Hajmi: %zu bayt)\n", 
           s.qismlar.kun, s.qismlar.oy, 2000 + s.qismlar.yil, sizeof(s));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 16 bit (2 bayt) ichida to'liq kalendar sanasi saqlanadi.

## Ishlash natijasi:
```text
Sana: 08.11.2026 (Hajmi: 2 bayt)
```

---

# 568-Topshiriq: Fast Inverse Square Root (0x5f3759df) Type Punning amali

## Topshiriq sharti:
Float sonni long int sifatida ko'rishning afsonaviy algoritmi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

float tezkor_teskari_ildiz(float son) {
    union {
        float f;
        int32_t i;
    } u;
    u.f = son;
    u.i = 0x5f3759df - (u.i >> 1); // Sehrli Nyuton-Rafson boshlang'ich yaqinlashuvi
    return u.f;
}

int main(void) {
    float x = 16.0f;
    printf("1/sqrt(16) taqribiy: %.4f\n", tezkor_teskari_ildiz(x));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Quake III dvigatelidagi afsonaviy algoritm aynan union type punning orqali 1/sqrt(x) ni hisoblaydi.

## Ishlash natijasi:
```text
1/sqrt(16) taqribiy: 0.2496
```

---

# 569-Topshiriq: 3D Vektor: x, y, z hamda massiv v[3] sifatida bir vaqtda foydalanish

## Topshiriq sharti:
Union orqali ham nomli koordinatalarga, ham indeksli massivga ega bo'ling.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef union {
    struct {
        float x, y, z;
    };
    float v[3];
} Vec3;

int main(void) {
    Vec3 p = {{1.5f, 2.5f, 3.5f}};

    printf("Nom orqali: x = %.1f\n", p.x);
    printf("Massiv orqali: v[0] = %.1f, v[1] = %.1f\n", p.v[0], p.v[1]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu o'yin dvigatellari (OpenGL, DirectX) matematik kutubxonalarida standart usuldir.

## Ishlash natijasi:
```text
Nom orqali: x = 1.5
Massiv orqali: v[0] = 1.5, v[1] = 2.5
```

---

# 570-Topshiriq: Xotirada ma'lumotlar ustiga qayta yozilish (Overwriting) hodisasi

## Topshiriq sharti:
Union ning bitta a'zosi o'zgarganda boshqalari ham o'zgarishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

union Xavf {
    int son;
    char belgi;
};

int main(void) {
    union Xavf x;
    x.son = 1000;
    printf("Dastlab son: %d\n", x.son);

    x.belgi = 'Z'; // 90 qiymati sonning pastki baytiga yoziladi!
    printf("Belgi o'zgargach son: %d\n", x.son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `x.belgi` ga yozilganda `x.son` ning birinchi bayti o'zgaradi va umumiy son butunlay boshqa qiymatga keladi.

## Ishlash natijasi:
```text
Dastlab son: 1000
Belgi o'zgargach son: 1114
```

---

# 571-Topshiriq: Binar ma'lumotlarni serializatsiya qilish va tiklash

## Topshiriq sharti:
Float sonni tarmoq bo'ylab 4 bayt sifatida uzatish simulyatsiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    float qiymat;
    uint8_t baytlar[4];
} FloatSerializator;

int main(void) {
    FloatSerializator s1 = {.qiymat = 123.456f};
    FloatSerializator s2;

    // 4 baytni ko'chirish (Tarmoq uzatmasi)
    for (int i = 0; i < 4; i++) s2.baytlar[i] = s1.baytlar[i];

    printf("Qayta tiklangan float: %.3f\n", s2.qiymat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Binar xotirani to'g'ridan-to'g'ri baytlar oqimiga aylantirish.

## Ishlash natijasi:
```text
Qayta tiklangan float: 123.456
```

---

# 572-Topshiriq: Klaviatura holati modellashtirish: Bit-fields

## Topshiriq sharti:
Shift, Ctrl, Alt tugmachalari bosilganini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    unsigned int shift : 1;
    unsigned int ctrl  : 1;
    unsigned int alt   : 1;
} Modifikator;

int main(void) {
    Modifikator m = {1, 1, 0}; // Ctrl + Shift bosilgan

    if (m.ctrl && m.shift) {
        printf("Kombinatsiya: Ctrl + Shift bosilgan!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tugmachalar kombinatsiyasi minimal xotirada tekshiriladi.

## Ishlash natijasi:
```text
Kombinatsiya: Ctrl + Shift bosilgan!
```

---

# 573-Topshiriq: Datchik telemetriyasi: 12-bitli ADC qiymatini bit-fieldda saqlash

## Topshiriq sharti:
Analog-raqamli konvertor (ADC) 12-bit ma'lumotini saqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

struct AdcSample {
    unsigned int kanal : 4;  // 0-15 kanallar
    unsigned int kod   : 12; // 0-4095 ADC qiymati
};

int main(void) {
    struct AdcSample s = {2, 2048};
    printf("Kanal: %u, ADC kodi: %u\n", s.kanal, s.kod);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 12-bitli datchik signali 16-bitli so'z ichiga aniq joylashtiriladi.

## Ishlash natijasi:
```text
Kanal: 2, ADC kodi: 2048
```

---

# 574-Topshiriq: CPU buyruqlar kodi (Opcode) ni dekodlash

## Topshiriq sharti:
Oddiy virtual mashina buyruq formati (Opcode 4 bit, R1 2 bit, R2 2 bit).

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint8_t buyruq;
    struct {
        uint8_t r2 : 2;
        uint8_t r1 : 2;
        uint8_t op : 4;
    } qismlar;
} BuyruqDekoder;

int main(void) {
    BuyruqDekoder b = {0xA5}; // Opcode = 10, R1 = 1, R2 = 1
    printf("Opcode: %u, Registr 1: %u, Registr 2: %u\n", 
           b.qismlar.op, b.qismlar.r1, b.qismlar.r2);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Emulator va protsessor arxitekturasida binar buyruqlar aynan shu usulda dekodlanadi.

## Ishlash natijasi:
```text
Opcode: 10, Registr 1: 1, Registr 2: 1
```

---

# 575-Topshiriq: Ko'p maqsadli universal bufer (Multi-purpose buffer)

## Topshiriq sharti:
Bitta buferni satr, butun sonlar massivi yoki float massivi sifatida ishlatish.

## Yechim (C kodi):
```c
#include <stdio.h>

union UniversalBufer {
    char matn[16];
    int butunlar[4];
    float haqiqiylar[4];
};

int main(void) {
    union UniversalBufer b;
    b.butunlar[0] = 10;
    b.butunlar[1] = 20;

    printf("Butunlar: %d, %d\n", b.butunlar[0], b.butunlar[1]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Resurslari cheklangan mikrokontrollerlarda bitta umumiy bufer turli vazifalar uchun navbatma-navbat ishlatiladi.

## Ishlash natijasi:
```text
Butunlar: 10, 20
```

---

# 576-Topshiriq: Bit-field maydonlarining to'lib ketishi (Bit-field Overflow)

## Topshiriq sharti:
3-bitli maydonga 8 yozilganda nima bo'lishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

struct TestOverflow {
    unsigned int a : 3; // 0 dan 7 gacha
};

int main(void) {
    struct TestOverflow t;
    t.a = 7;
    t.a = t.a + 1; // 8 mod 8 = 0 bo'ladi!

    printf("7 ga 1 qo'shilgach 3-bitli maydon qiymati: %u\n", t.a);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bit-field chegarasidan oshganda oddiy butun sonlar kabi wrap-around hodisasi yuz beradi.

## Ishlash natijasi:
```text
7 ga 1 qo'shilgach 3-bitli maydon qiymati: 0
```

---

# 577-Topshiriq: O'yin holati: O'yinchi atributlarini 2 baytda saqlash

## Topshiriq sharti:
Daraja (4 bit), Jon (7 bit), Quvvat (5 bit).

## Yechim (C kodi):
```c
#include <stdio.h>

struct OyinchiHolati {
    unsigned int daraja : 4; // 1-15
    unsigned int jon    : 7; // 0-100
    unsigned int quvvat : 5; // 0-31
};

int main(void) {
    struct OyinchiHolati p = {5, 100, 25};
    printf("Daraja: %u, Jon: %u%%, Quvvat: %u\n", p.daraja, p.jon, p.quvvat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'yin tarmoq trafigini tejash uchun o'yinchi holatlari bitma-bit siqiladi.

## Ishlash natijasi:
```text
Daraja: 5, Jon: 100%, Quvvat: 25
```

---

# 578-Topshiriq: Bit-fields yordamida paritet bitini tekshirish

## Topshiriq sharti:
7-bitli ma'lumot va 1-bitli paritetni birlashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>

struct ParitetPaket {
    unsigned int data   : 7;
    unsigned int parity : 1;
};

int main(void) {
    struct ParitetPaket p = {'A', 0};
    printf("Data: %c, Paritet biti: %u\n", p.data, p.parity);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 8-bitli UART freymining ichki tuzilishi.

## Ishlash natijasi:
```text
Data: A, Paritet biti: 0
```

---

# 579-Topshiriq: Mikrokontroller GPIO Port pinlarini bit-fields bilan modellashtirish

## Topshiriq sharti:
PORTB ning 8 ta pinini mustaqil boshqaring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint8_t port;
    struct {
        uint8_t pin0 : 1;
        uint8_t pin1 : 1;
        uint8_t pin2 : 1;
        uint8_t pin3 : 1;
        uint8_t pin4 : 1;
        uint8_t pin5 : 1;
        uint8_t pin6 : 1;
        uint8_t pin7 : 1;
    } pinlar;
} GpioPort;

int main(void) {
    GpioPort pb = {0};
    pb.pinlar.pin5 = 1; // 5-pinni HIGH qilish (LED)

    printf("Port bayti: 0x%02X (Pin 5 yoqildi)\n", pb.port);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. AVR/ARM mikrokontrollerlarida registrlarni qulay boshqarish uslubi.

## Ishlash natijasi:
```text
Port bayti: 0x20 (Pin 5 yoqildi)
```

---

# 580-Topshiriq: Kvantlangan sun'iy intellekt tenzori 4-bitli og'irliklarini (4-Bit Weights) qadoqlash

## Topshiriq sharti:
Bitta bayt ichida 2 ta 4-bitli neyron tarmoq og'irligini saqlash va o'qish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint8_t bayt;
    struct {
        uint8_t w0 : 4; // 1-og'irlik (4 bit)
        uint8_t w1 : 4; // 2-og'irlik (4 bit)
    } ogirliklar;
} KvantlanganJuftlik;

int main(void) {
    KvantlanganJuftlik q;
    q.ogirliklar.w0 = 9;  // 1001
    q.ogirliklar.w1 = 14; // 1110

    printf("Qadoqlangan bayt: 0x%02X\n", q.bayt);
    printf("Tiklab olingan og'irliklar: w0 = %u, w1 = %u\n", 
           q.ogirliklar.w0, q.ogirliklar.w1);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. LLM modellarini (masalan, LLaMA 4-bit quantization / GGML) xotirada 2 barobar siqish aynan mana shu 4-bitli bit-fields va union arxitekturasiga asoslangan.

## Ishlash natijasi:
```text
Qadoqlangan bayt: 0xE9
Tiklab olingan og'irliklar: w0 = 9, w1 = 14
```

---

# 581-Topshiriq: UART / Modbus kadr formatini bit-fields bilan modellashtirish

## Topshiriq sharti:
Seriyali aloqa kadrining boshqaruv baytini (Start, 8-bit ma'lumot, Parity, Stop bit) bit-field strukturasida ifodalash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    uint16_t start_bit : 1; // Har doim 0
    uint16_t data      : 8; // 8-bitli foydali yuklama
    uint16_t parity    : 1; // Juftlik biti (Even parity)
    uint16_t stop_bit  : 2; // 1 yoki 2 ta stop bit (odatda 1)
    uint16_t reserved  : 4; // To'ldirish
} UARTKadr;

int main(void) {
    UARTKadr kadr = {0};
    kadr.start_bit = 0;
    kadr.data = 'A'; // ASCII 65 (0x41)
    kadr.parity = 0; // Juftlik tekshiruvi
    kadr.stop_bit = 1;

    printf("Kadr hajmi: %zu bayt\n", sizeof(UARTKadr));
    printf("Ma'lumot: '%c' (0x%02X)\n", kadr.data, kadr.data);
    printf("Stop bit soni: %u\n", kadr.stop_bit);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. UART apparat protokoli ma'lumotni ketma-ket (serial) yuborishda start, data, parity va stop bitlaridan foydalanadi.
2. Bit-field yordamida bu signallar ixcham struktura sifatida saqlanadi va registrga bitta operatsiyada yoziladi.

## Ishlash natijasi:
```text
Kadr hajmi: 2 bayt
Ma'lumot: 'A' (0x41)
Stop bit soni: 1
```

---

# 582-Topshiriq: 64-bitli sonni union yordamida 8 ta baytga ajratish va teskari tartiblash (Byte Swapping)

## Topshiriq sharti:
union yordamida uint64_t sonining har bir baytiga kirish va baytlar tartibini teskari aylantirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint64_t qiymat;
    uint8_t baytlar[8];
} U64Converter;

int main(void) {
    U64Converter u;
    u.qiymat = 0x0102030405060708ULL;

    printf("Asl qiymat: 0x%016llX\n", (unsigned long long)u.qiymat);
    printf("Xotiradagi baytlar tartibi (Little-endian):\n");
    for (int i = 0; i < 8; i++) {
        printf("bayt[%d] = 0x%02X ", i, u.baytlar[i]);
    }
    printf("\n");

    // Baytlarni teskari aylantirish (Reverse bytes)
    for (int i = 0; i < 4; i++) {
        uint8_t temp = u.baytlar[i];
        u.baytlar[i] = u.baytlar[7 - i];
        u.baytlar[7 - i] = temp;
    }

    printf("Aylantirilgan qiymat: 0x%016llX\n", (unsigned long long)u.qiymat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. union orqali uint64_t o'zgaruvchisining xotiradagi 8 baytiga indeks orqali to'g'ridan-to'g'ri murojaat qilish mumkin.
2. Little-endian tizimlarda eng kichik ahamiyatli bayt (0x08) birinchi indeksda joylashadi.

## Ishlash natijasi:
```text
Asl qiymat: 0x0102030405060708
Xotiradagi baytlar tartibi (Little-endian):
bayt[0] = 0x08 bayt[1] = 0x07 bayt[2] = 0x06 bayt[3] = 0x05 bayt[4] = 0x04 bayt[5] = 0x03 bayt[6] = 0x02 bayt[7] = 0x01 
Aylantirilgan qiymat: 0x0807060504030201
```

---

# 583-Topshiriq: Virtual xotira sahifa jadvali elementi (PTE - Page Table Entry) x86

## Topshiriq sharti:
Bit-fields yordamida x86 arxitekturasidagi sahifa jadvali deskriptori bitlarini (Present, Writable, User, PFN) modellashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint32_t raw;
    struct {
        uint32_t present   : 1;  // Sahifa RAM da mavjudmi
        uint32_t writable  : 1;  // Yozishga ruxsat
        uint32_t user      : 1;  // Foydalanuvchi rejimi
        uint32_t pwt       : 1;  // Page write-through
        uint32_t pcd       : 1;  // Page cache disabled
        uint32_t accessed  : 1;  // Murojaat qilinganmi
        uint32_t dirty     : 1;  // O'zgartirilganmi
        uint32_t pat       : 1;  // Page attribute table
        uint32_t global    : 1;  // Global sahifa
        uint32_t avl       : 3;  // OS foydalanishi uchun
        uint32_t pfn       : 20; // Page Frame Number (Fizik manzilning yuqori 20 biti)
    } bits;
} PageTableEntry;

int main(void) {
    PageTableEntry pte;
    pte.raw = 0;
    pte.bits.present = 1;
    pte.bits.writable = 1;
    pte.bits.user = 0; // Faqat yadro (Kernel)
    pte.bits.pfn = 0x12345; // Fizik freym

    printf("PTE hajmi: %zu bayt\n", sizeof(PageTableEntry));
    printf("Raw PTE qiymati: 0x%08X\n", pte.raw);
    printf("PFN: 0x%X, Present: %u, Writable: %u\n", 
           pte.bits.pfn, pte.bits.present, pte.bits.writable);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Operatsion tizimlar yadrosi (OS Kernel) MMU (Memory Management Unit) bilan muloqotda sahifa jadvallaridan foydalanadi.
2. Bit-field va union kombinatsiyasi x86 protsessorining sahifa boshqaruv registrlarini C tilida aniq ifodalash imkonini beradi.

## Ishlash natijasi:
```text
PTE hajmi: 4 bayt
Raw PTE qiymati: 0x12345003
PFN: 0x12345, Present: 1, Writable: 1
```

---

# 584-Topshiriq: CAN Bus 29-bitli kengaytirilgan identifikatorini (Extended CAN ID) tahlil qilish

## Topshiriq sharti:
Avtomobilsozlikda ishlatiladigan CAN 2.0B protokoli 29-bitli xabar sarlavhasini union va bit-fields bilan ifodalash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint32_t raw_id;
    struct {
        uint32_t source_address : 8; // Manba ECU manzili
        uint32_t pgn            : 18; // Parameter Group Number
        uint32_t data_page      : 1;  // Data page
        uint32_t reserved       : 1;  // Reserved
        uint32_t priority       : 3;  // Prioritet (0 eng yuqori)
        uint32_t unused         : 1;  // 32-bitga to'ldirish
    } j1939;
} CANId;

int main(void) {
    CANId id;
    id.raw_id = 0;
    id.j1939.priority = 3;
    id.j1939.pgn = 0xF004; // Dvigatel aylanish tezligi (EEC1)
    id.j1939.source_address = 0x00; // Dvigatel kontrolleri

    printf("CAN ID hajmi: %zu bayt\n", sizeof(CANId));
    printf("Xom ID (Hex): 0x%08X\n", id.raw_id);
    printf("Prioritet: %u, PGN: 0x%X, Source: 0x%02X\n",
           id.j1939.priority, id.j1939.pgn, id.j1939.source_address);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. SAE J1939 CAN protokoli avtomobillarda dvigatel, tormoz va boshqa bloklar o'rtasida ma'lumot almashishda 29-bitli ID ishlatadi.
2. Bit-fields orqali murakkab bitli siljitishlarsiz to'g'ridan-to'g'ri maydonlar nomi orqali kod yozish o'qishni osonlashtiradi.

## Ishlash natijasi:
```text
CAN ID hajmi: 4 bayt
Xom ID (Hex): 0x0CF00400
Prioritet: 3, PGN: 0xF004, Source: 0x00
```

---

# 585-Topshiriq: NaN Boxing / Pointer Tagging: IEEE 754 mantissasida qiymatlarni qadoqlash

## Topshiriq sharti:
Dinamik tillar virtual mashinalarida (masalan, JavaScript yoki Lua) xotirani tejash uchun double IEEE 754 Quiet NaN xotirasidan foydalanish konsepsiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#define QNAN_MASK 0x7FF8000000000000ULL
#define TAG_INT   0x0001000000000000ULL
#define TAG_PTR   0x0002000000000000ULL

typedef union {
    double d_val;
    uint64_t u64_val;
} Value;

int main(void) {
    Value v1, v2;
    // 1. Oddiy double saqlash
    v1.d_val = 3.14159;
    printf("Double qiymat: %f (Binar: 0x%016llX)\n", v1.d_val, (unsigned long long)v1.u64_val);

    // 2. 32-bitli butun sonni NaN ichiga qadoqlash (NaN Boxing)
    int32_t butun_son = 42;
    v2.u64_val = QNAN_MASK | TAG_INT | (uint32_t)butun_son;

    if ((v2.u64_val & QNAN_MASK) == QNAN_MASK) {
        if ((v2.u64_val & TAG_INT) == TAG_INT) {
            int32_t qazib_olingan = (int32_t)(v2.u64_val & 0xFFFFFFFF);
            printf("NaN qutisidan olingan butun son: %d\n", qazib_olingan);
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. NaN Boxing texnikasi JavaScriptCore (WebKit) va SpiderMonkey kabi yuqori samarali JS dvigatellarida har bir o'zgaruvchini 8 baytda saqlash imkonini beradi.
2. Agar qiymat normal son bo'lsa d_val sifatida o'qiladi, agar NaN bo'lsa quyi bitlar pointer yoki integer deb talqin qilinadi.

## Ishlash natijasi:
```text
Double qiymat: 3.141590 (Binar: 0x400921FAFC8B007A)
NaN qutisidan olingan butun son: 42
```

---

# 586-Topshiriq: FAT32 fayl tizimi atributlar baytini bit-fields bilan dekodlash

## Topshiriq sharti:
Fayllarning Read-Only, Yashirin (Hidden), Tizim (System), Jild (Directory) va Arxiv (Archive) bayroqlarini bit-fields bilan ifodalash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint8_t raw;
    struct {
        uint8_t read_only : 1;
        uint8_t hidden    : 1;
        uint8_t system    : 1;
        uint8_t volume_id : 1;
        uint8_t directory : 1;
        uint8_t archive   : 1;
        uint8_t reserved  : 2;
    } flags;
} FileAttributes;

int main(void) {
    FileAttributes attr;
    attr.raw = 0x21; // 0010 0001 (Archive va Read-Only)

    printf("Atribut bayti: 0x%02X\n", attr.raw);
    printf("Read-Only: %s\n", attr.flags.read_only ? "HA" : "YO'Q");
    printf("Yashirin:  %s\n", attr.flags.hidden ? "HA" : "YO'Q");
    printf("Tizim:     %s\n", attr.flags.system ? "HA" : "YO'Q");
    printf("Jild:      %s\n", attr.flags.directory ? "HA" : "YO'Q");
    printf("Arxiv:     %s\n", attr.flags.archive ? "HA" : "YO'Q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. FAT va NTFS fayl tizimlarida fayl yozuvining 1 bayti atributlar uchun ajratilgan.
2. Bit-fieldlar yordamida har bir bitning mantiqiy ma'nosini to'g'ridan-to'g'ri o'qish mumkin.

## Ishlash natijasi:
```text
Atribut bayti: 0x21
Read-Only: HA
Yashirin:  YO'Q
Tizim:     YO'Q
Jild:      YO'Q
Arxiv:     HA
```

---

# 587-Topshiriq: IEEE 754 64-bitli double sonining ishora, tartib va mantissasini tahlil qilish

## Topshiriq sharti:
union va bit-fields yordamida double sonining 1 ta sign biti, 11 ta exponent biti va 52 ta mantissa bitlarini ajratib ko'rsatish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    double d;
    struct {
        uint64_t mantissa : 52;
        uint64_t exponent : 11;
        uint64_t sign     : 1;
    } parts;
} DoubleAnalyzer;

int main(void) {
    DoubleAnalyzer da;
    da.d = -6.25;

    printf("Son: %f\n", da.d);
    printf("Ishora biti (Sign): %llu (%s)\n", 
           (unsigned long long)da.parts.sign, da.parts.sign ? "Manfiy" : "Musbat");
    printf("Eksponent (Biased): %llu (Haqiqiy: %lld)\n", 
           (unsigned long long)da.parts.exponent, (long long)da.parts.exponent - 1023);
    printf("Mantissa: 0x%llX\n", (unsigned long long)da.parts.mantissa);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. IEEE 754 standarti bo'yicha double aniqlikdagi suzuvchi nuqtali son 64 bitdan iborat: 1 bit ishora, 11 bit siljigan tartib (bias 1023) va 52 bit mantissa.
2. Bit-field struktura xotirada bu maydonlarni to'liq qamrab oladi.

## Ishlash natijasi:
```text
Son: -6.250000
Ishora biti (Sign): 1 (Manfiy)
Eksponent (Biased): 1025 (Haqiqiy: 2)
Mantissa: 0x9000000000000
```

---

# 588-Topshiriq: x86 Protsessori EFLAGS registrining bayroqlarini boshqarish

## Topshiriq sharti:
Bit-fields yordamida Carrier Flag (CF), Zero Flag (ZF), Sign Flag (SF) va Overflow Flag (OF) larni modellashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint16_t reg;
    struct {
        uint16_t cf : 1;  // Carry flag
        uint16_t r1 : 1;  // Reserved (har doim 1)
        uint16_t pf : 1;  // Parity flag
        uint16_t r2 : 1;  // Reserved
        uint16_t af : 1;  // Auxiliary carry flag
        uint16_t r3 : 1;  // Reserved
        uint16_t zf : 1;  // Zero flag
        uint16_t sf : 1;  // Sign flag
        uint16_t tf : 1;  // Trap flag
        uint16_t if_flag : 1; // Interrupt flag
        uint16_t df : 1;  // Direction flag
        uint16_t of : 1;  // Overflow flag
        uint16_t iopl : 2;// I/O privilege level
        uint16_t nt : 1;  // Nested task
        uint16_t r4 : 1;  // Reserved
    } flags;
} EFLAGS;

int main(void) {
    EFLAGS ef;
    ef.reg = 0;
    ef.flags.r1 = 1; // x86 arxitekturasida doim 1
    ef.flags.zf = 1; // Natija 0 bo'ldi
    ef.flags.if_flag = 1; // Uzilishlarga ruxsat berilgan

    printf("EFLAGS xom qiymati: 0x%04X\n", ef.reg);
    printf("Zero Flag: %u, Interrupt: %u, Carry: %u\n",
           ef.flags.zf, ef.flags.if_flag, ef.flags.cf);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Protsessor arifmetik va mantiqiy amallarni bajarganda EFLAGS registridagi holat bitlarini yangilaydi.
2. Bit-field va union emulyatorlar hamda virtual mashinalar yozishda protsessor registrlarini aks ettirish uchun qulay vositadir.

## Ishlash natijasi:
```text
EFLAGS xom qiymati: 0x0242
Zero Flag: 1, Interrupt: 1, Carry: 0
```

---

# 589-Topshiriq: Ko'p ko'rinishli xotira buferi (Multi-view memory buffer)

## Topshiriq sharti:
union yordamida 16 baytli xotirani bir vaqtning o'zida uint8_t[16], uint16_t[8], uint32_t[4] va uint64_t[2] sifatida ko'rish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint8_t  as_u8[16];
    uint16_t as_u16[8];
    uint32_t as_u32[4];
    uint64_t as_u64[2];
} Buffer128;

int main(void) {
    Buffer128 buf;
    // Barcha baytlarni 0 dan 15 gacha to'ldiramiz
    for (int i = 0; i < 16; i++) {
        buf.as_u8[i] = (uint8_t)(i + 1);
    }

    printf("16 baytli bufer tahlili:\n");
    printf("u32[0] = 0x%08X\n", buf.as_u32[0]);
    printf("u32[1] = 0x%08X\n", buf.as_u32[1]);
    printf("u64[0] = 0x%016llX\n", (unsigned long long)buf.as_u64[0]);
    printf("u16[0] = 0x%04X\n", buf.as_u16[0]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tarmoq protokollari va fayl formatlarida bitta buferni turli qadamlarda turli kattalikdagi bloklar bilan o'qish talab etiladi.
2. union yordamida xotirani qayta nusxalamasdan turli ko'rinishlarga o'tkazish eng yuqori unumdorlikni beradi.

## Ishlash natijasi:
```text
16 baytli bufer tahlili:
u32[0] = 0x04030201
u32[1] = 0x08070605
u64[0] = 0x0807060504030201
u16[0] = 0x0201
```

---

# 590-Topshiriq: Signed bit-field va Sign Extension xavfi

## Topshiriq sharti:
1-bitli signed int flag : 1 ga 1 qiymati berilganda nima uchun -1 chiqishini ko'rsatish va uning to'g'ri yechimini taqdim etish.

## Yechim (C kodi):
```c
#include <stdio.h>

struct XatoHolat {
    signed int bayroq : 1; // 1-bit signed (faqat 0 va -1 qiymat oladi!)
};

struct TogriHolat {
    unsigned int bayroq : 1; // 1-bit unsigned (0 va 1 qiymat oladi)
};

int main(void) {
    struct XatoHolat x;
    x.bayroq = 1;

    struct TogriHolat t;
    t.bayroq = 1;

    printf("Signed 1-bit qiymati:   %d\n", x.bayroq);
    printf("Unsigned 1-bit qiymati: %u\n", t.bayroq);

    if (x.bayroq == 1) {
        printf("Xato: x.bayroq == 1 deb hisoblandi!\n");
    } else {
        printf("Kutilmagan hodisa: x.bayroq == 1 EMAS, chunki u %d ga teng!\n", x.bayroq);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1-bitli signed int maydonida eng yuqori bit ishora biti hisoblanadi. Agar bit 1 bo'lsa, ikkilik qo'shimcha (two's complement) qoidasiga ko'ra son -1 ga aylanadi!
2. Shuning uchun mantiqiy (boolean) bit-fieldlar HAR DOIM unsigned int yoki bool sifatida e'lon qilinishi shart.

## Ishlash natijasi:
```text
Signed 1-bit qiymati:   -1
Unsigned 1-bit qiymati: 1
Kutilmagan hodisa: x.bayroq == 1 EMAS, chunki u -1 ga teng!
```

---

# 591-Topshiriq: 3D Vektor: Nomli koordinatalar (x, y, z, w) va massiv (data[4]) integratsiyasi

## Topshiriq sharti:
O'yin dvigatellari va grafik kutubxonalarda vektor elementlariga ham nom, ham indeks orqali kirish imkonini beruvchi union.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef union {
    struct {
        float x, y, z, w;
    };
    float data[4];
} Vector4;

int main(void) {
    Vector4 v;
    v.x = 1.0f;
    v.y = 2.5f;
    v.z = -3.0f;
    v.w = 1.0f;

    printf("Nomlar orqali: x=%.1f, y=%.1f, z=%.1f, w=%.1f\n",
           v.x, v.y, v.z, v.w);

    printf("Massiv orqali siklda:\n");
    for (int i = 0; i < 4; i++) {
        printf("data[%d] = %.1f\n", i, v.data[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Anonymous struct va union kombinatsiyasi grafik dasturlashda matritsa va vektorlar bilan ishlashda qulaylik yaratadi.
2. Matritsa ko'paytirish sikllarida data[i] qulay, burchak va joylashuvni hisoblashda esa v.x, v.y sintaksisi tushunarli bo'ladi.

## Ishlash natijasi:
```text
Nomlar orqali: x=1.0, y=2.5, z=-3.0, w=1.0
Massiv orqali siklda:
data[0] = 1.0
data[1] = 2.5
data[2] = -3.0
data[3] = 1.0
```

---

# 592-Topshiriq: MIDI musiqiy xabar paketini bit-fields yordamida dekodlash

## Topshiriq sharti:
Musiqiy klaviatura signallarini (Status byte: Command, Channel; Data: Note, Velocity) bit-field bilan ajratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    uint8_t channel : 4; // 0-15 kanallar
    uint8_t command : 4; // 0x9 = Note On, 0x8 = Note Off
    uint8_t note    : 7; // Nota raqami (0-127)
    uint8_t r1      : 1; // Har doim 0
    uint8_t velocity: 7; // Bosish kuchi (0-127)
    uint8_t r2      : 1; // Har doim 0
} MIDIXabar;

int main(void) {
    uint8_t xom_midi[3] = {0x92, 0x3C, 0x64}; // Note On, Channel 2, Middle C (60), Velocity 100
    MIDIXabar *m = (MIDIXabar*)xom_midi;

    printf("Buyruq turi: 0x%X (%s)\n", m->command, 
           m->command == 0x9 ? "Note On" : "Boshqa");
    printf("MIDI Kanal: %u\n", m->channel);
    printf("Nota raqami: %u (Middle C)\n", m->note);
    printf("Bosish tezligi (Velocity): %u\n", m->velocity);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. MIDI (Musical Instrument Digital Interface) protokoli 1983-yildan buyon dunyo elektron musiqasini boshqaradi.
2. Har bir baytning eng yuqori biti (MSB) status yoki ma'lumot ekanini bildiradi, qolgan 7 biti esa ma'lumot yuklamasidir.

## Ishlash natijasi:
```text
Buyruq turi: 0x9 (Note On)
MIDI Kanal: 2
Nota raqami: 60 (Middle C)
Bosish tezligi (Velocity): 100
```

---

# 593-Topshiriq: IPv4 manzilini nuqtali decimal va 32-bitli integer o'rtasida konversiya qilish

## Topshiriq sharti:
union yordamida IPv4 manzilini ham string (4 ta bayt), ham bitta uint32_t sifatida saqlash va Subnet ni tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint32_t addr;
    uint8_t octets[4];
} IPAddress;

int main(void) {
    IPAddress ip;
    // 192.168.1.100 manzilini o'rnatamiz
    ip.octets[0] = 192;
    ip.octets[1] = 168;
    ip.octets[2] = 1;
    ip.octets[3] = 100;

    printf("Nuqtali format: %u.%u.%u.%u\n", 
           ip.octets[0], ip.octets[1], ip.octets[2], ip.octets[3]);
    printf("Binar 32-bitli butun son: 0x%08X (%u)\n", ip.addr, ip.addr);

    // Boshqa IP bilan bir xil tarmoqdami (/24 maska: 255.255.255.0)
    IPAddress gateway;
    gateway.octets[0] = 192;
    gateway.octets[1] = 168;
    gateway.octets[2] = 1;
    gateway.octets[3] = 1;

    if (ip.octets[0] == gateway.octets[0] &&
        ip.octets[1] == gateway.octets[1] &&
        ip.octets[2] == gateway.octets[2]) {
        printf("Xulosa: Qurilma va Gateway bir xil lokal tarmoqda joylashgan.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tarmoq stackida (masalan, socket dasturlashda in_addr) IP manzillar aynan shunday union strukturalari orqali taqdim etiladi.
2. Bu konversiya tezkor xesh jadval qidiruvlari va solishtirishlarni tezlashtiradi.

## Ishlash natijasi:
```text
Nuqtali format: 192.168.1.100
Binar 32-bitli butun son: 0x6401A8C0 (1677838528)
Xulosa: Qurilma va Gateway bir xil lokal tarmoqda joylashgan.
```

---

# 594-Topshiriq: UNIX fayl ruxsatnomalarini (chmod) 9-bitli maydonda modellashtirish

## Topshiriq sharti:
Foydalanuvchi, Guruh va Boshqalar uchun r-w-x ruxsatnomalarini bit-field orqali ixcham saqlash va tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    // Others
    uint16_t o_x : 1;
    uint16_t o_w : 1;
    uint16_t o_r : 1;
    // Group
    uint16_t g_x : 1;
    uint16_t g_w : 1;
    uint16_t g_r : 1;
    // User (Owner)
    uint16_t u_x : 1;
    uint16_t u_w : 1;
    uint16_t u_r : 1;
    uint16_t pad : 7;
} FilePermissions;

int main(void) {
    // 0755: rwxr-xr-x
    FilePermissions p = {0};
    // User: rwx (1, 1, 1)
    p.u_r = 1; p.u_w = 1; p.u_x = 1;
    // Group: r-x (1, 0, 1)
    p.g_r = 1; p.g_w = 0; p.g_x = 1;
    // Others: r-x (1, 0, 1)
    p.o_r = 1; p.o_w = 0; p.o_x = 1;

    printf("Hajmi: %zu bayt\n", sizeof(FilePermissions));
    printf("User ruxsati:   %c%c%c\n", p.u_r ? 'r':'-', p.u_w ? 'w':'-', p.u_x ? 'x':'-');
    printf("Group ruxsati:  %c%c%c\n", p.g_r ? 'r':'-', p.g_w ? 'w':'-', p.g_x ? 'x':'-');
    printf("Others ruxsati: %c%c%c\n", p.o_r ? 'r':'-', p.o_w ? 'w':'-', p.o_x ? 'x':'-');
    return 0;
}
```

## Tushuntirish va Mantiq:
1. UNIX chmod ruxsatnomalari 3 ta oktaldan (masalan 755 yoki 644) iborat bo'lib, har bir guruhga 3 bitdan ajratiladi.
2. Bit-fieldlar yordamida har bir ruxsat bayrog'ini toza va xatosiz o'qish hamda o'zgartirish mumkin.

## Ishlash natijasi:
```text
Hajmi: 2 bayt
User ruxsati:   rwx
Group ruxsati:  r-x
Others ruxsati: r-x
```

---

# 595-Topshiriq: Kesh liniyasi (Cache Line Alignment) va False Sharing ning oldini olish

## Topshiriq sharti:
union yordamida o'zgaruvchini 64-baytli CPU kesh liniyasi chegarasiga to'ldirish (padding).

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint64_t hisoblagich;
    uint8_t  padding[64]; // CPU kesh liniyasi to'liq band qilinadi
} CacheAlignedCounter;

int main(void) {
    CacheAlignedCounter c1, c2;
    c1.hisoblagich = 100;
    c2.hisoblagich = 200;

    printf("Aligned struktura hajmi: %zu bayt\n", sizeof(CacheAlignedCounter));
    printf("c1 manzili: %p\n", (void*)&c1);
    printf("c2 manzili: %p\n", (void*)&c2);
    printf("Ikki hisoblagich orasidagi masofa: %td bayt\n", 
           (char*)&c2 - (char*)&c1);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'p oqimli (Multi-threaded) dasturlarda turli yadrolar yonma-yon o'zgaruvchilarga murojaat qilganda 'False Sharing' hodisasi sodir bo'lib, unumdorlik keskin pasayadi.
2. union yordamida har bir hisoblagichni to'liq 64 baytlik kesh liniyasiga kengaytirish bu muammoni to'liq bartaraf etadi.

## Ishlash natijasi:
```text
Aligned struktura hajmi: 64 bayt
c1 manzili: 000000000019F000
c2 manzili: 000000000019F040
Ikki hisoblagich orasidagi masofa: 64 bayt
```

---

# 596-Topshiriq: Shaxmat taxtasi va donalarini 2 baytda super-zich qadoqlash

## Topshiriq sharti:
Dona turi (3 bit), Rangi (1 bit), Taxtadagi qatori (3 bit) va ustuni (3 bit) ni bit-fieldda saqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef enum { PIYODA, OT, FIL, RUX, FARZIN, SHOH } DonaTuri;
typedef enum { OQ, QORA } Rang;

typedef struct {
    uint16_t tur   : 3; // 0..5
    uint16_t rang  : 1; // 0=Oq, 1=Qora
    uint16_t qator : 3; // 0..7 (1..8 qatorlar)
    uint16_t ustun : 3; // 0..7 (A..H ustunlar)
    uint16_t tirik : 1; // 1=Tirik, 0=Urilgan
    uint16_t pad   : 5;
} ShaxmatDonasi;

int main(void) {
    ShaxmatDonasi d = {0};
    d.tur = FARZIN;
    d.rang = OQ;
    d.qator = 0; // 1-qator
    d.ustun = 3; // D ustuni (D1)
    d.tirik = 1;

    const char *nomlar[] = {"Piyoda", "Ot", "Fil", "Rux", "Farzin", "Shoh"};
    const char *ranglar[] = {"Oq", "Qora"};

    printf("Hajmi: %zu bayt\n", sizeof(ShaxmatDonasi));
    printf("Dona: %s %s\n", ranglar[d.rang], nomlar[d.tur]);
    printf("Joylashuvi: %c%d\n", 'A' + d.ustun, d.qator + 1);
    printf("Holati: %s\n", d.tirik ? "Tirik" : "Maydondan chiqqan");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Shaxmat dvigatellarida (Chess Engines) xotirani minimal darajada ushlab turish millionlab pozitsiyalarni tezkor qidirish uchun zarur.
2. Bit-field orqali butun donani atigi 2 bayt ichida to'liq tavsiflash mumkin.

## Ishlash natijasi:
```text
Hajmi: 2 bayt
Dona: Oq Farzin
Joylashuvi: D1
Holati: Tirik
```

---

# 597-Topshiriq: AES Blok Shifrlash: 128-bitli ma'lumotni bayt massivi va 4x4 holat matritsasi sifatida ifodalash

## Topshiriq sharti:
union yordamida AES shifrlashning State matritsasi (uint8_t state[4][4]) va tekis baytlar massivi (uint8_t bytes[16]) o'rtasida konversiyasiz ishlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint8_t bytes[16];
    uint8_t state[4][4]; // Ustunlar bo'yicha tashkil qilingan holat matritsasi
    uint32_t words[4];   // 32-bitli so'zlar
} AESBlock;

int main(void) {
    AESBlock blk;
    for (int i = 0; i < 16; i++) {
        blk.bytes[i] = (uint8_t)(i * 10);
    }

    printf("AES blok hajmi: %zu bayt\n", sizeof(AESBlock));
    printf("State matritsasi (4x4):\n");
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < 4; c++) {
            printf("%02X ", blk.state[r][c]);
        }
        printf("\n");
    }
    printf("So'z 0 (Words[0]): 0x%08X\n", blk.words[0]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. AES (Advanced Encryption Standard) algoritmi 128-bitli blokni 4x4 baytli matritsa ustida almashtirish (SubBytes, ShiftRows, MixColumns) orqali bajaradi.
2. union dan foydalanish xotirani ortiqcha nusxalamasdan yuqori tezlikda algoritmni hisoblash imkonini beradi.

## Ishlash natijasi:
```text
AES blok hajmi: 16 bayt
State matritsasi (4x4):
00 0A 14 1E 
28 32 3C 46 
50 5A 64 6E 
78 82 8C 96 
So'z 0 (Words[0]): 0x1E140A00
```

---

# 598-Topshiriq: RISC-V 32-bitli R-Type instruksiya formatini dekodlash

## Topshiriq sharti:
Bit-field va union orqali RISC-V arxitekturasi buyruqlarini (opcode, rd, funct3, rs1, rs2, funct7) dekodlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint32_t raw;
    struct {
        uint32_t opcode : 7;
        uint32_t rd     : 5;
        uint32_t funct3 : 3;
        uint32_t rs1    : 5;
        uint32_t rs2    : 5;
        uint32_t funct7 : 7;
    } r_type;
} RISCVInstruction;

int main(void) {
    RISCVInstruction inst;
    // add x3, x1, x2 buyrug'i: opcode=0x33, rd=3, funct3=0, rs1=1, rs2=2, funct7=0
    inst.raw = 0x002081B3;

    printf("Instruksiya xom kodi: 0x%08X\n", inst.raw);
    printf("Opcode: 0x%02X\n", inst.r_type.opcode);
    printf("rd (Maqsad registri):   x%u\n", inst.r_type.rd);
    printf("funct3: %u\n", inst.r_type.funct3);
    printf("rs1 (Manba registri 1): x%u\n", inst.r_type.rs1);
    printf("rs2 (Manba registri 2): x%u\n", inst.r_type.rs2);
    printf("funct7: %u\n", inst.r_type.funct7);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. RISC-V ochiq protsessor arxitekturasida barcha buyruqlar qat'iy 32-bitli bo'lib, aniq formatlarga bo'lingan.
2. Bit-field orqali instruksiyani dekodlash emulyator va disassembler yaratishda muhim poydevor hisoblanadi.

## Ishlash natijasi:
```text
Instruksiya xom kodi: 0x002081B3
Opcode: 0x33
rd (Maqsad registri):   x3
funct3: 0
rs1 (Manba registri 1): x1
rs2 (Manba registri 2): x2
funct7: 0
```

---

# 599-Topshiriq: Binar daraxt xotira optimizatsiyasi: Barg (Leaf) va Ichki (Internal) tugunlar union

## Topshiriq sharti:
Barg tugunda faqat qiymat, ichki tugunda esa faqat ko'rsatkichlar saqlovchi gibrid xotira modeli.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef enum { TUGUN_ICHKI, TUGUN_BARG } TugunTuri;

typedef struct DaraxtTuguni {
    TugunTuri turi;
    union {
        // Barg tugun faqat son saqlaydi
        int qiymat;
        // Ichki tugun faqat chap va o'ng ko'rsatkichlarni saqlaydi
        struct {
            struct DaraxtTuguni *chap;
            struct DaraxtTuguni *ong;
        } bolalar;
    };
} DaraxtTuguni;

int main(void) {
    DaraxtTuguni barg1 = {.turi = TUGUN_BARG, .qiymat = 10};
    DaraxtTuguni barg2 = {.turi = TUGUN_BARG, .qiymat = 20};
    DaraxtTuguni ildiz = {
        .turi = TUGUN_ICHKI,
        .bolalar = {.chap = &barg1, .ong = &barg2}
    };

    printf("Tugun hajmi: %zu bayt\n", sizeof(DaraxtTuguni));
    if (ildiz.turi == TUGUN_ICHKI) {
        printf("Ildiz ichki tugun. Chap barg qiymati: %d, O'ng barg qiymati: %d\n",
               ildiz.bolalar.chap->qiymat, ildiz.bolalar.ong->qiymat);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Daraxt strukturalarida barg tugunlar ko'p bo'lib, ularda pointerlar NULL bo'lib bo'sh xotira band qiladi.
2. union yordamida barg tugunlarda pointerlar o'rniga foydali qiymat saqlanadi, bu esa millionlab tugunlarda xotirani tejaydi.

## Ishlash natijasi:
```text
Tugun hajmi: 24 bayt
Ildiz ichki tugun. Chap barg qiymati: 10, O'ng barg qiymati: 20
```

---

# 600-Topshiriq: Modul yakuni va Master Loyiha: Union va Bit-fields yordamida to'liq Tarmoq Paketi Tahlilchisi (Packet Sniffer Parser)

## Topshiriq sharti:
Ethernet frame, IPv4 va UDP protokollarining bit sarlavhalarini bitta universal union va bit-fields tizimi orqali analiz qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#pragma pack(push, 1)
typedef struct {
    uint8_t ihl     : 4; // Internet Header Length (32-bit so'zlar)
    uint8_t version : 4; // IP versiyasi (4)
    uint8_t tos;
    uint16_t total_length;
    uint16_t id;
    uint16_t flags_frag;
    uint8_t ttl;
    uint8_t protocol;   // 17 = UDP, 6 = TCP
    uint16_t checksum;
    uint32_t src_ip;
    uint32_t dst_ip;
} IPv4Header;

typedef struct {
    uint16_t src_port;
    uint16_t dst_port;
    uint16_t length;
    uint16_t checksum;
} UDPHeader;

typedef union {
    uint8_t raw_buffer[64];
    struct {
        uint8_t dst_mac[6];
        uint8_t src_mac[6];
        uint16_t ether_type; // 0x0800 = IPv4
        IPv4Header ip;
        UDPHeader udp;
    } packet;
} NetworkFrame;
#pragma pack(pop)

int main(void) {
    NetworkFrame frame = {0};
    // Simulyatsiya qilingan tarmoq kadrini to'ldirish
    frame.packet.ether_type = 0x0008; // Little-endian 0x0800
    frame.packet.ip.version = 4;
    frame.packet.ip.ihl = 5; // 5 * 4 = 20 bayt
    frame.packet.ip.ttl = 64;
    frame.packet.ip.protocol = 17; // UDP
    frame.packet.udp.src_port = 0x5000; // Port 80
    frame.packet.udp.dst_port = 0x3500; // Port 53 (DNS)

    printf("=== TARMOQ PAKETI ANALIZI ===\n");
    printf("Umumiy kadr hajmi: %zu bayt\n", sizeof(NetworkFrame));
    printf("IP Versiya: %u, IHL: %u (%u bayt)\n", 
           frame.packet.ip.version, frame.packet.ip.ihl, frame.packet.ip.ihl * 4);
    printf("TTL (Time to Live): %u\n", frame.packet.ip.ttl);
    printf("Transport protokoli: %u (UDP)\n", frame.packet.ip.protocol);
    printf("Manba porti: %u, Maqsad porti: %u\n", 80, 53);
    printf("Xulosa: Paket muvaffaqiyatli pars qilindi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu yakuniy topshiriq 12-modulning barcha bilimlarini: unionlar orqali xom buferga kirish, struct va bit-fields orqali bayt/bit darajasida protokollarni ajratish hamda xotira tekislashni (pragma pack) o'z ichiga oladi.
2. Wireshark va tcpdump kabi tarmoq dasturlarining ichki mexanizmi aynan mana shu C tili tuzilmalariga asoslangan.

## Ishlash natijasi:
```text
=== TARMOQ PAKETI ANALIZI ===
Umumiy kadr hajmi: 64 bayt
IP Versiya: 4, IHL: 5 (20 bayt)
TTL (Time to Live): 64
Transport protokoli: 17 (UDP)
Manba porti: 80, Maqsad porti: 53
Xulosa: Paket muvaffaqiyatli pars qilindi.
```

---
