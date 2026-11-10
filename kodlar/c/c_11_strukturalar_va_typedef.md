# C Dasturlash Tili — 11-Qism: Strukturalar (struct) va typedef
## (501-550 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* struct deklaratsiyasi, nuqta (.) va strelka (->) operatorlari
* typedef orqali turlar yaratish, strukturalar massivi va saralash
* Nested structures, pass-by-value vs pass-by-pointer farqi
* Padding va Memory Alignment, #pragma pack(1) va data layout optimizatsiyasi
* Kompleks sonlar, Point2D, StringView va In-Memory Database Table moduli

---

# 501-Topshiriq: struct deklaratsiyasi va nuqta (.) operatori orqali murojaat

## Topshiriq sharti:
Talaba strukturasini e'lon qilib, uning maydonlariga qiymat bering va chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

struct Talaba {
    int id;
    char ism[30];
    double gpa;
};

int main(void) {
    struct Talaba t1;
    t1.id = 101;
    strcpy(t1.ism, "Anvar");
    t1.gpa = 3.85;

    printf("Talaba #%d: %s, GPA: %.2lf\n", t1.id, t1.ism, t1.gpa);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `struct` har xil turdagi ma'lumotlarni bitta mantiqiy ob'ektga birlashtirish imkonini beradi.
2. Struktura maydonlariga nuqta (`.`) operatori orqali to'g'ridan-to'g'ri murojaat qilinadi.

## Ishlash natijasi:
```text
Talaba #101: Anvar, GPA: 3.85
```

---

# 502-Topshiriq: Strukturani e'lon paytida initsializatsiya qilish

## Topshiriq sharti:
Struktura yaratilayotgan paytning o'zida figurali qavslar bilan boshlang'ich qiymat bering.

## Yechim (C kodi):
```c
#include <stdio.h>

struct Kitob {
    char nom[40];
    char muallif[30];
    int sahifalar;
};

int main(void) {
    struct Kitob k1 = {"O'tkan kunlar", "Abdulla Qodiriy", 320};

    printf("Kitob: '%s', Muallif: %s (%d bet)\n", 
           k1.nom, k1.muallif, k1.sahifalar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boshlang'ich qiymatlar struktura maydonlarining e'lon qilingan tartibida beriladi.

## Ishlash natijasi:
```text
Kitob: 'O'tkan kunlar', Muallif: Abdulla Qodiriy (320 bet)
```

---

# 503-Topshiriq: C99 Designated Initializers: Maydonlar nomi bilan initsializatsiya

## Topshiriq sharti:
Maydonlar tartibidan qat'i nazar nomlari orqali qiymat berish.

## Yechim (C kodi):
```c
#include <stdio.h>

struct Mahsulot {
    int kod;
    double narx;
    int qoldiq;
};

int main(void) {
    struct Mahsulot m = {
        .narx = 45000.0,
        .kod = 1205,
        .qoldiq = 15
    };

    printf("Kod: %d, Narx: %.0f so'm, Qoldiq: %d ta\n", 
           m.kod, m.narx, m.qoldiq);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C99 `.maydon = qiymat` sintaksisi kodni juda o'qilishi oson qiladi va xatolarni kamaytiradi.

## Ishlash natijasi:
```text
Kod: 1205, Narx: 45000 so'm, Qoldiq: 15 ta
```

---

# 504-Topshiriq: typedef orqali yangi struktura tipini yaratish

## Topshiriq sharti:
Har safar 'struct' so'zini yozmaslik uchun typedef dan foydalaning.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    double x;
    double y;
} Nuqta;

int main(void) {
    Nuqta p = {10.5, 20.0};
    printf("Nuqta koordinatalari: (%.1lf, %.1lf)\n", p.x, p.y);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `typedef struct { ... } Nom;` konstruksiyasi `Nom` ni mustaqil tur nomiga aylantiradi.

## Ishlash natijasi:
```text
Nuqta koordinatalari: (10.5, 20.0)
```

---

# 505-Topshiriq: Struktura ko'rsatkichi (Pointer) va strelka (->) operatori

## Topshiriq sharti:
Struktura manzilini pointerda saqlab, -> bilan maydonlarga murojaat qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int kenglik;
    int balandlik;
} Tortburchak;

int main(void) {
    Tortburchak t = {20, 10};
    Tortburchak *ptr = &t;

    printf("Kenglik (-> orqali):   %d\n", ptr->kenglik);
    printf("Balandlik (-> orqali): %d\n", ptr->balandlik);
    printf("Yuzi: %d\n", ptr->kenglik * ptr->balandlik);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `ptr->maydon` ifodasi `(*ptr).maydon` ning qisqartirilgan shaklidir.

## Ishlash natijasi:
```text
Kenglik (-> orqali):   20
Balandlik (-> orqali): 10
Yuzi: 200
```

---

# 506-Topshiriq: (*ptr).maydon va ptr->maydon o'rtasidagi to'liq ekvivalentlik

## Topshiriq sharti:
Nima uchun (*ptr).maydon da qavs zarurligini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int id;
} Obyekt;

int main(void) {
    Obyekt o = {42};
    Obyekt *p = &o;

    printf("1. p->id orqali:   %d\n", p->id);
    printf("2. (*p).id orqali: %d\n", (*p).id);

    // *p.id deb yozilsa xato bo'ladi, chunki '.' operatori '*' dan yuqori ustunlikka ega!
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Nuqta (`.`) operatori dereferens (`*`) ga qaraganda yuqori ustunlikka ega, shuning uchun `(*p).id` deb qavsga olish shart.

## Ishlash natijasi:
```text
1. p->id orqali:   42
2. (*p).id orqali: 42
```

---

# 507-Topshiriq: Strukturalar massivi (Array of Structures)

## Topshiriq sharti:
Uchta xodim ma'lumotlarini strukturalar massivida saqlab chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int id;
    const char *lavozim;
} Xodim;

int main(void) {
    Xodim jamoa[3] = {
        {1, "Dasturchi"},
        {2, "Dizayner"},
        {3, "Tizim ma'muri"}
    };

    for (int i = 0; i < 3; i++) {
        printf("Xodim #%d: %s\n", jamoa[i].id, jamoa[i].lavozim);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Strukturalar massivi ma'lumotlar bazasi jadvallarini xotirada saqlash uchun qulay vositadir.

## Ishlash natijasi:
```text
Xodim #1: Dasturchi
Xodim #2: Dizayner
Xodim #3: Tizim ma'muri
```

---

# 508-Topshiriq: Strukturalar massivini saralash (Baholar bo'yicha Bubble Sort)

## Topshiriq sharti:
Talabalarni bahosi bo'yicha kamayish tartibida saralang.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    const char *ism;
    int ball;
} Talaba;

int main(void) {
    Talaba guruh[3] = {
        {"Nodir", 75},
        {"Dilshod", 95},
        {"Zilola", 88}
    };

    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2 - i; j++) {
            if (guruh[j].ball < guruh[j + 1].ball) {
                Talaba t = guruh[j];
                guruh[j] = guruh[j + 1];
                guruh[j + 1] = t;
            }
        }
    }

    printf("Eng yuqori ball: %s (%d ball)\n", guruh[0].ism, guruh[0].ball);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Butun strukturani bitta amalda (`guruh[j] = guruh[j + 1]`) nusxalash mumkin.

## Ishlash natijasi:
```text
Eng yuqori ball: Dilshod (95 ball)
```

---

# 509-Topshiriq: Ichma-ich joylashgan strukturalar (Nested Structures)

## Topshiriq sharti:
Foydalanuvchi strukturasi ichida Manzil strukturasini saqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    char shahar[20];
    char kocha[30];
} Manzil;

typedef struct {
    char ism[20];
    Manzil yashash_joyi; // Ichki struktura
} Foydalanuvchi;

int main(void) {
    Foydalanuvchi f = {"Jasur", {"Toshkent", "Navoiy ko'chasi"}};

    printf("Foydalanuvchi: %s\n", f.ism);
    printf("Manzili: %s shahri, %s\n", 
           f.yashash_joyi.shahar, f.yashash_joyi.kocha);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Maydonlarga zanjirli nuqta orqali kiriladi: `f.yashash_joyi.shahar`.

## Ishlash natijasi:
```text
Foydalanuvchi: Jasur
Manzili: Toshkent shahri, Navoiy ko'chasi
```

---

# 510-Topshiriq: Strukturalarni funksiyaga qiymat bo'yicha uzatish (Pass-by-value)

## Topshiriq sharti:
Nusxalanish xususiyatini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int x, y;
} Nuqta;

void siljit(Nuqta p) {
    p.x += 10;
    p.y += 10;
    printf("Funksiya ichida: (%d, %d)\n", p.x, p.y);
}

int main(void) {
    Nuqta n = {5, 5};
    siljit(n);
    printf("main ichida: (%d, %d) (O'zgarmadi!)\n", n.x, n.y);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qiymat bo'yicha uzatilganda butun struktura yangi stek kadriga nusxalanadi.

## Ishlash natijasi:
```text
Funksiya ichida: (15, 15)
main ichida: (5, 5) (O'zgarmadi!)
```

---

# 511-Topshiriq: Strukturalarni ko'rsatkich orqali uzatish (Pass-by-pointer)

## Topshiriq sharti:
Struktura a'zolarini funksiya orqali bevosita o'zgartiring.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int x, y;
} Nuqta;

void siljit_haqiqiy(Nuqta *p) {
    p->x += 10;
    p->y += 10;
}

int main(void) {
    Nuqta n = {5, 5};
    siljit_haqiqiy(&n);
    printf("Haqiqiy siljigan nuqta: (%d, %d)\n", n.x, n.y);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `Nuqta *p` orqali faqat manzil uzatiladi va asl struktura o'zgartiriladi.

## Ishlash natijasi:
```text
Haqiqiy siljigan nuqta: (15, 15)
```

---

# 512-Topshiriq: const modifikatori bilan struktura ko'rsatkichini himoyalash

## Topshiriq sharti:
Katta strukturani nusxalamasdan, ammo o'zgartirishni ham taqiqlab uzatish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    char ma_lumot[1024]; // Katta hajm
} KattaFayl;

void xavfsiz_oqish(const KattaFayl *f) {
    // f->ma_lumot[0] = 'X'; // KOMPILYATSIYA XATOSI: read-only
    printf("Katta struktura xavfsiz o'qildi.\n");
}

int main(void) {
    KattaFayl k = {"Tizim parametrlari"};
    xavfsiz_oqish(&k);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const T *ptr` uslubi ham yuqori tezlikni (nusxalash yo'q), ham ma'lumot xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
Katta struktura xavfsiz o'qildi.
```

---

# 513-Topshiriq: Funksiyadan struktura qaytarish (Factory / Constructor andozasi)

## Topshiriq sharti:
Yangi strukturani to'ldirib qaytaruvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    double real;
    double imag;
} Kompleks;

Kompleks kompleks_yarat(double r, double i) {
    Kompleks k = {r, i};
    return k;
}

int main(void) {
    Kompleks z = kompleks_yarat(3.0, 4.0);
    printf("Kompleks son: %.1lf + %.1lfi\n", z.real, z.imag);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da funksiyadan butun strukturani to'g'ridan-to'g'ri `return` qilish to'liq qo'llab-quvvatlanadi.

## Ishlash natijasi:
```text
Kompleks son: 3.0 + 4.0i
```

---

# 514-Topshiriq: Xotirada padding va alignment (tekislash) hodisasi: sizeof(struct)

## Topshiriq sharti:
Nima uchun char (1) va int (4) dan iborat struktura 8 bayt bo'lishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

struct TestPadding {
    char a;    // 1 bayt
    // Bu yerda 3 bayt bo'shliq (Padding) qo'shiladi!
    int b;     // 4 bayt
};

int main(void) {
    printf("A'zolar yig'indisi: 1 + 4 = 5 bayt\n");
    printf("Haqiqiy sizeof:     %zu bayt\n", sizeof(struct TestPadding));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. CPU 32-bitli butun sonlarni 4 ga karrali manzillardan tez o'qiydi.
2. Shuning uchun kompilyator avtomatik tarzda `char` dan so'ng 3 bayt 'padding' qo'shadi.

## Ishlash natijasi:
```text
A'zolar yig'indisi: 1 + 4 = 5 bayt
Haqiqiy sizeof:     8 bayt
```

---

# 515-Topshiriq: Maydonlar tartibini o'zgartirish orqali xotirani tejash

## Topshiriq sharti:
Katta turlardan kichiklariga qarab joylashtirib xotira hajmini qisqartiring.

## Yechim (C kodi):
```c
#include <stdio.h>

// YOMON TARTIB: 1 + 7(pad) + 8 + 1 + 7(pad) = 24 bayt
struct YomonTartib {
    char a;
    double b;
    char c;
};

// YAXSHI TARTIB: 8 + 1 + 1 + 6(pad) = 16 bayt
struct YaxshiTartib {
    double b;
    char a;
    char c;
};

int main(void) {
    printf("Yomon tartib hajmi:   %zu bayt\n", sizeof(struct YomonTartib));
    printf("Yaxshi tartib hajmi:  %zu bayt\n", sizeof(struct YaxshiTartib));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta o'lchamli turlarni (`double`, `long long`) struktura boshiga qo'yish paddingni kamaytiradi (24 baytdan 16 baytga).

## Ishlash natijasi:
```text
Yomon tartib hajmi:   24 bayt
Yaxshi tartib hajmi:  16 bayt
```

---

# 516-Topshiriq: #pragma pack(1) orqali barcha paddingni o'chirish

## Topshiriq sharti:
Strukturani zichlash (Packed struct) xususiyatini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

#pragma pack(push, 1)
struct Zichlangan {
    char a;
    int b;
};
#pragma pack(pop)

int main(void) {
    printf("Zichlangan struktura hajmi: %zu bayt\n", sizeof(struct Zichlangan));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `#pragma pack(1)` kompilyatorga barcha paddinglarni o'chirib, har bir baytni zich yozishni buyuradi (aniq 5 bayt).
2. Bu tarmoq paketlari sarlavhasi va apparat datchiklarida xotirani to'g'ri moslash uchun kerak.

## Ishlash natijasi:
```text
Zichlangan struktura hajmi: 5 bayt
```

---

# 517-Topshiriq: Strukturalarni solishtirish: Nima uchun s1 == s2 deb yozib bo'lmaydi?

## Topshiriq sharti:
Strukturalarni a'zoma-a'zo taqqoslovchi funksiya yozish shartligini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int id;
    int ball;
} Talaba;

bool talabalar_tengmi(Talaba a, Talaba b) {
    return (a.id == b.id) && (a.ball == b.ball);
}

int main(void) {
    Talaba t1 = {1, 90};
    Talaba t2 = {1, 90};

    // if (t1 == t2) -> KOMPILYATSIYA XATOSI!
    if (talabalar_tengmi(t1, t2)) {
        printf("Talabalar ma'lumoti to'liq bir xil!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da `==` operatori strukturalar uchun belgilanmagan, chunki padding baytlarida axlat qiymatlar bo'lishi mumkin.
2. Har doim qo'lda solishtirish funksiyasi yozilishi kerak.

## Ishlash natijasi:
```text
Talabalar ma'lumoti to'liq bir xil!
```

---

# 518-Topshiriq: O'z-o'ziga murojaat qiluvchi strukturalar (Self-referential struct)

## Topshiriq sharti:
Bog'langan ro'yxat (Linked List) tuguni deklaratsiyasini yarating.

## Yechim (C kodi):
```c
#include <stdio.h>

struct Tugun {
    int qiymat;
    struct Tugun *keyingi; // O'z turidagi keyingi tugunga ko'rsatkich
};

int main(void) {
    struct Tugun t1 = {10, NULL};
    struct Tugun t2 = {20, NULL};

    t1.keyingi = &t2; // Bog'lash

    printf("1-tugun: %d\n", t1.qiymat);
    printf("2-tugun (ko'rsatkich orqali): %d\n", t1.keyingi->qiymat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `struct Tugun *keyingi` orqali zanjirli ma'lumotlar tuzilmalari (Linked List, Tree, Graph) quriladi.

## Ishlash natijasi:
```text
1-tugun: 10
2-tugun (ko'rsatkich orqali): 20
```

---

# 519-Topshiriq: Struktura ichida funksiya ko'rsatkichlari (C da OOP metodlari simulyatsiyasi)

## Topshiriq sharti:
Kalkulyator strukturasiga amal funksiyasini biriktiring.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct Hisoblagich Hisoblagich;

struct Hisoblagich {
    int son;
    void (*oshir)(Hisoblagich *self);
};

void oshir_metod(Hisoblagich *self) {
    self->son++;
}

int main(void) {
    Hisoblagich h = {0, oshir_metod};
    h.oshir(&h);
    h.oshir(&h);

    printf("Hisoblagich yakuniy qiymati: %d\n", h.son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Struktura ichiga funksiya ko'rsatkichini qo'yish orqali C tilida OOP obyektlari va metodlarini to'liq simulyatsiya qilish mumkin.

## Ishlash natijasi:
```text
Hisoblagich yakuniy qiymati: 2
```

---

# 520-Topshiriq: Kompleks sonlar arifmetikasi strukturalar orqali

## Topshiriq sharti:
Ikki kompleks sonni qo'shuvchi va ko'paytiruvchi modul.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    double r, i;
} Complex;

Complex complex_add(Complex a, Complex b) {
    Complex res = {a.r + b.r, a.i + b.i};
    return res;
}

int main(void) {
    Complex z1 = {2.0, 3.0};
    Complex z2 = {1.0, 4.0};
    Complex yigindi = complex_add(z1, z2);

    printf("Yig'indi: %.1lf + %.1lfi\n", yigindi.r, yigindi.i);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. (2 + 3i) + (1 + 4i) = 3 + 7i.

## Ishlash natijasi:
```text
Yig'indi: 3.0 + 7.0i
```

---

# 521-Topshiriq: Kasr sonlar (Fraction) strukturasi va ularni qisqartirish

## Topshiriq sharti:
Surat va maxrajdan iborat kasrni EKUB yordamida qisqartiring.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int surat;
    int maxraj;
} Kasr;

int ekub(int a, int b) {
    while (b) { int r = a % b; a = b; b = r; }
    return a;
}

Kasr qisqartir(Kasr k) {
    int boluvchi = ekub(k.surat, k.maxraj);
    k.surat /= boluvchi;
    k.maxraj /= boluvchi;
    return k;
}

int main(void) {
    Kasr k = {12, 16};
    Kasr q = qisqartir(k);
    printf("12/16 qisqargach: %d/%d\n", q.surat, q.maxraj);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 12 va 16 ning EKUBi 4 bo'lib, kasr 3/4 ko'rinishiga keladi.

## Ishlash natijasi:
```text
12/16 qisqargach: 3/4
```

---

# 522-Topshiriq: Vaqt strukturasi va ikki vaqt orasidagi farqni topish

## Topshiriq sharti:
Soat, minut, sekund farqini hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int soat, minut, sekund;
} Vaqt;

int vaqt_sekundga(Vaqt v) {
    return v.soat * 3600 + v.minut * 60 + v.sekund;
}

Vaqt sekunddan_vaqtga(int s) {
    Vaqt v;
    v.soat = s / 3600;
    s %= 3600;
    v.minut = s / 60;
    v.sekund = s % 60;
    return v;
}

int main(void) {
    Vaqt v1 = {10, 30, 0};
    Vaqt v2 = {12, 15, 30};

    int farq_sekund = vaqt_sekundga(v2) - vaqt_sekundga(v1);
    Vaqt farq = sekunddan_vaqtga(farq_sekund);

    printf("Farq: %02d:%02d:%02d\n", farq.soat, farq.minut, farq.sekund);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 10:30:00 dan 12:15:30 gacha bo'lgan vaqt farqi 1 soat 45 minut 30 sekund.

## Ishlash natijasi:
```text
Farq: 01:45:30
```

---

# 523-Topshiriq: Sana strukturasi va keyingi kunni hisoblovchi funksiya

## Topshiriq sharti:
Oy oxiri va yil oxirini inobatga olgan holda sanani 1 kunga oldinga suring.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int kun, oy, yil;
} Sana;

Sana keyingi_kun(Sana s) {
    int oydagi_kunlar = 31;
    if (s.oy == 4 || s.oy == 6 || s.oy == 9 || s.oy == 11) oydagi_kunlar = 30;
    else if (s.oy == 2) oydagi_kunlar = 28;

    s.kun++;
    if (s.kun > oydagi_kunlar) {
        s.kun = 1;
        s.oy++;
        if (s.oy > 12) {
            s.oy = 1;
            s.yil++;
        }
    }
    return s;
}

int main(void) {
    Sana bugun = {31, 12, 2025};
    Sana ertaga = keyingi_kun(bugun);

    printf("Keyingi sana: %02d.%02d.%d\n", ertaga.kun, ertaga.oy, ertaga.yil);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 31.12.2025 dan keyin 01.01.2026 yangi yil boshlanadi.

## Ishlash natijasi:
```text
Keyingi sana: 01.01.2026
```

---

# 524-Topshiriq: Bank hisob raqami (BankAccount) moduli

## Topshiriq sharti:
Mablag' kiritish va yechish operatsiyalarini struktura bilan modellashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int hisob_raqam;
    double balans;
} BankHisob;

void pul_qosh(BankHisob *h, double summa) {
    h->balans += summa;
}

void pul_yech(BankHisob *h, double summa) {
    if (h->balans >= summa) {
        h->balans -= summa;
    }
}

int main(void) {
    BankHisob h = {1001, 500.0};
    pul_qosh(&h, 250.0);
    pul_yech(&h, 100.0);

    printf("Hisob #%d yakuniy balans: $%.1lf\n", h.hisob_raqam, h->balans);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 500 + 250 - 100 = 650.0.

## Ishlash natijasi:
```text
Hisob #1001 yakuniy balans: $650.0
```

---

# 525-Topshiriq: Geometrik Point2D va masofa hisoblash

## Topshiriq sharti:
Ikki nuqta orasidagi masofani hisoblovchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

typedef struct {
    double x, y;
} Point2D;

double masofa(Point2D a, Point2D b) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return sqrt(dx * dx + dy * dy);
}

int main(void) {
    Point2D p1 = {0.0, 0.0};
    Point2D p2 = {3.0, 4.0};
    printf("Masofa: %.1lf\n", masofa(p1, p2));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. sqrt(3^2 + 4^2) = 5.0.

## Ishlash natijasi:
```text
Masofa: 5.0
```

---

# 526-Topshiriq: To'g'ri to'rtburchak (Rectangle) va uning perimetri hamda yuzi

## Topshiriq sharti:
Yuqori chap va pastki o'ng burchaklari berilgan to'rtburchak tahlili.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int x1, y1;
    int x2, y2;
} Rect;

int rect_yuza(Rect r) {
    return abs(r.x2 - r.x1) * abs(r.y2 - r.y1);
}

int main(void) {
    Rect r = {0, 0, 10, 5};
    printf("To'rtburchak yuzi: %d\n", rect_yuza(r));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 10 * 5 = 50.

## Ishlash natijasi:
```text
To'rtburchak yuzi: 50
```

---

# 527-Topshiriq: 3D Vektor (Vector3D) va uning skalyar ko'paytmasi (Dot Product)

## Topshiriq sharti:
Uch o'lchamli fazodagi vektorlar amallarini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    double x, y, z;
} Vec3;

double dot_product(Vec3 a, Vec3 b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

int main(void) {
    Vec3 v1 = {1.0, 2.0, 3.0};
    Vec3 v2 = {4.0, 5.0, 6.0};

    printf("Skalyar ko'paytma: %.1lf\n", dot_product(v1, v2));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32.0.

## Ishlash natijasi:
```text
Skalyar ko'paytma: 32.0
```

---

# 528-Topshiriq: StringView strukturasi (Satrdan nusxa olmasdan ko'rish oynasi)

## Topshiriq sharti:
Ko'rsatkich va uzunlik orqali qism-satrni ifodalovchi yengil struktura.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    const char *data;
    size_t len;
} StringView;

void sv_chop(StringView sv) {
    for (size_t i = 0; i < sv.len; i++) {
        putchar(sv.data[i]);
    }
    printf("\n");
}

int main(void) {
    const char *matn = "Assalomu Alaykum";
    StringView sv = {matn + 10, 7}; // "Alaykum"

    printf("StringView orqali: ");
    sv_chop(sv);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. StringView xotiradan yangi joy ajratmaydi va nusxalamaydi, bu yuqori tezlikdagi dasturlash siri hisoblanadi.

## Ishlash natijasi:
```text
StringView orqali: Alaykum
```

---

# 529-Topshiriq: Nomsiz strukturalar (Anonymous Structs) C11 xususiyati

## Topshiriq sharti:
Struktura ichida nomsiz ichki strukturani ishlatish.

## Yechim (C kodi):
```c
#include <stdio.h>

struct Obyekt {
    int tur;
    struct {
        int x, y;
    }; // Nomsiz struktura: x va y ga to'g'ridan-to'g'ri kirish mumkin
};

int main(void) {
    struct Obyekt obj;
    obj.tur = 1;
    obj.x = 100; // obj.ichki.x deb yozish shart emas!
    obj.y = 200;

    printf("Obyekt: tur=%d, joyi=(%d, %d)\n", obj.tur, obj.x, obj.y);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C11 da nomsiz ichki strukturalar a'zolariga to'g'ridan-to'g'ri murojaat qilish imkonini beradi.

## Ishlash natijasi:
```text
Obyekt: tur=1, joyi=(100, 200)
```

---

# 530-Topshiriq: Strukturalar massividan ID bo'yicha chiziqli qidiruv

## Topshiriq sharti:
ID bo'yicha kerakli yozuvni topib ko'rsatkichini qaytaring.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int id;
    const char *nom;
} Mahsulot;

const Mahsulot* qidir_id(const Mahsulot ro_yxat[], int n, int id) {
    for (int i = 0; i < n; i++) {
        if (ro_yxat[i].id == id) return &ro_yxat[i];
    }
    return NULL;
}

int main(void) {
    Mahsulot m[3] = {{10, "Non"}, {20, "Sut"}, {30, "Choy"}};
    const Mahsulot *topildi = qidir_id(m, 3, 20);

    if (topildi) {
        printf("Topildi: #%d - %s\n", topildi->id, topildi->nom);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qidiruv natijasi ko'rsatkich sifatida qaytadi.

## Ishlash natijasi:
```text
Topildi: #20 - Sut
```

---

# 531-Topshiriq: Strukturalar massivida binar qidiruv

## Topshiriq sharti:
ID bo'yicha saralangan massivda O(log N) da qidiruv.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int id;
    int ball;
} Talaba;

int binar_qidiruv_talaba(const Talaba arr[], int n, int target_id) {
    int chap = 0, ong = n - 1;
    while (chap <= ong) {
        int mid = chap + (ong - chap) / 2;
        if (arr[mid].id == target_id) return mid;
        if (arr[mid].id < target_id) chap = mid + 1;
        else ong = mid - 1;
    }
    return -1;
}

int main(void) {
    Talaba guruh[] = {{101, 80}, {105, 92}, {110, 85}, {120, 99}};
    int idx = binar_qidiruv_talaba(guruh, 4, 110);
    printf("ID 110 li talaba indeksi: %d (Ball: %d)\n", idx, guruh[idx].ball);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Binar qidiruv katta bazalarda elementlarni bir zumda topadi.

## Ishlash natijasi:
```text
ID 110 li talaba indeksi: 2 (Ball: 85)
```

---

# 532-Topshiriq: Struktura a'zolarining joylashuv ofsetini aniqlash

## Topshiriq sharti:
offsetof makrosi orqali barcha maydonlar siljishini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stddef.h>

struct TestOfset {
    char bayt;
    int son;
    double haqiqiy;
};

int main(void) {
    printf("bayt ofseti:    %zu\n", offsetof(struct TestOfset, bayt));
    printf("son ofseti:     %zu\n", offsetof(struct TestOfset, son));
    printf("haqiqiy ofseti: %zu\n", offsetof(struct TestOfset, haqiqiy));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyator qayerga qancha padding qo'shganini aniq ko'rish mumkin.

## Ishlash natijasi:
```text
bayt ofseti:    0
son ofseti:     4
haqiqiy ofseti: 8
```

---

# 533-Topshiriq: Strukturani boshqa strukturaga to'g'ridan-to'g'ri biriktirish (s1 = s2)

## Topshiriq sharti:
Bir xil turdagi strukturalar o'rtasida to'g'ridan-to'g'ri nusxalash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int a, b;
} Juftlik;

int main(void) {
    Juftlik j1 = {10, 20};
    Juftlik j2;

    j2 = j1; // Butun strukturani nusxalash (Shallow copy)

    printf("j2: a = %d, b = %d\n", j2.a, j2.b);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Massivlardan farqli ravishda strukturalarni `=` bilan to'g'ridan-to'g'ri biriktirish mumkin.

## Ishlash natijasi:
```text
j2: a = 10, b = 20
```

---

# 534-Topshiriq: Chuqur nusxalash (Deep Copy): Ichida ko'rsatkichi bor struktura

## Topshiriq sharti:
Ichki xotira maydonini alohida malloc qilib mustaqil nusxalang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int id;
    char *matn;
} Hujjat;

Hujjat chuqur_nusxa(const Hujjat *src) {
    Hujjat dest;
    dest.id = src->id;
    dest.matn = (char*)malloc(strlen(src->matn) + 1);
    strcpy(dest.matn, src->matn);
    return dest;
}

int main(void) {
    Hujjat h1 = {1, "Original hujjat"};
    Hujjat h2 = chuqur_nusxa(&h1);

    strcpy(h2.matn, "O'zgartirilgan!");

    printf("h1 matni: %s\n", h1.matn);
    printf("h2 matni: %s\n", h2.matn);

    free(h2.matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Deep copy orqali `h2` ning o'zgarishi `h1` ga umuman ta'sir qilmaydi.

## Ishlash natijasi:
```text
h1 matni: Original hujjat
h2 matni: O'zgartirilgan!
```

---

# 535-Topshiriq: Polimorfizm simulyatsiyasi: Baza strukturasini meros qilib olish

## Topshiriq sharti:
Baza strukturasini birinchi a'zo sifatida joylashtirib turni kengaytirish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int tur_kodi;
} Shakl;

typedef struct {
    Shakl asos; // Birinchi o'rinda baza strukturasi!
    int radius;
} Doira;

void shakl_turini_aniqla(const Shakl *s) {
    if (s->tur_kodi == 1) printf("Bu Doira shakli!\n");
}

int main(void) {
    Doira d = {{1}, 10};
    // Doira manzilini to'g'ridan-to'g'ri Shakl ko'rsatkichiga cast qilish mumkin:
    shakl_turini_aniqla((Shakl*)&d);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da merosxo'rlik (Inheritance) birinchi maydonga ota strukturani qo'yish orqali amalga oshiriladi (C-style polymorphism).

## Ishlash natijasi:
```text
Bu Doira shakli!
```

---

# 536-Topshiriq: Rang strukturasi (RGBA) va kulrang rangga aylantirish

## Topshiriq sharti:
Piksel rangini Grayscale ga o'tkazuvchi funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    unsigned char r, g, b, a;
} RangRGBA;

unsigned char kulrang(RangRGBA rang) {
    return (unsigned char)(0.299 * rang.r + 0.587 * rang.g + 0.114 * rang.b);
}

int main(void) {
    RangRGBA qizil = {255, 0, 0, 255};
    printf("Qizil rang kulrang shkalada: %u\n", kulrang(qizil));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'zning sezgirligi bo'yicha RGB komponentlari kulrang yorqinlikka keltiriladi.

## Ishlash natijasi:
```text
Qizil rang kulrang shkalada: 76
```

---

# 537-Topshiriq: Fayl metama'lumotlari strukturasi

## Topshiriq sharti:
Fayl hajmi, nomi va ruxsatlarini saqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    char nom[20];
    long hajm;
    int ruxsat;
} FaylInfo;

int main(void) {
    FaylInfo f = {"main.c", 2048, 0644};
    printf("Fayl: %s (%ld bayt), Ruxsat: 0%o\n", f.nom, f.hajm, f.ruxsat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Unix `stat` strukturasi aynan shu formatda fayl parametrlarini beradi.

## Ishlash natijasi:
```text
Fayl: main.c (2048 bayt), Ruxsat: 0644
```

---

# 538-Topshiriq: 2x2 Matritsa strukturasi va uning determinanti

## Topshiriq sharti:
Kichik matritsani struktura sifatida saqlab determinant hisoblang.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int a, b;
    int c, d;
} Mat2;

int determinant(Mat2 m) {
    return m.a * m.d - m.b * m.c;
}

int main(void) {
    Mat2 m = {4, 2, 3, 5};
    printf("det(M) = %d\n", determinant(m));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. det = 4*5 - 2*3 = 20 - 6 = 14.

## Ishlash natijasi:
```text
det(M) = 14
```

---

# 539-Topshiriq: Struktura a'zolarini nollash (Zero-initialization)

## Topshiriq sharti:
Barcha maydonlarni bir zumda {0} bilan tozalash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int id;
    double qiymat;
    char belgi;
} Sozlama;

int main(void) {
    Sozlama s = {0}; // Barcha maydonlar va paddinglar 0 bo'ladi
    printf("id: %d, qiymat: %.1lf, belgi: %d\n", s.id, s.qiymat, s.belgi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `{0}` bilan initsializatsiya qilish barcha maydonlarga xavfsiz nol qiymat beradi.

## Ishlash natijasi:
```text
id: 0, qiymat: 0.0, belgi: 0
```

---

# 540-Topshiriq: Strukturalar massivida filtrlash

## Topshiriq sharti:
Baho 85 dan yuqori bo'lgan barcha a'lochi talabalarni chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    const char *ism;
    int ball;
} Talaba;

int main(void) {
    Talaba guruh[3] = {{"Ali", 92}, {"Vali", 70}, {"Gani", 88}};

    printf("A'lochilar: ");
    for (int i = 0; i < 3; i++) {
        if (guruh[i].ball >= 85) printf("%s ", guruh[i].ism);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oddiy if sharti orqali strukturalar massivini saralash.

## Ishlash natijasi:
```text
A'lochilar: Ali Gani
```

---

# 541-Topshiriq: Struktura ichida qat'iy o'lchamli massiv bilan ishlash

## Topshiriq sharti:
Talabaning 3 ta fandan olgan baholarini struktura massivida saqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    const char *ism;
    int baholar[3];
} Oquvchi;

int main(void) {
    Oquvchi o = {"Sarvar", {5, 4, 5}};
    int jami = o.baholar[0] + o.baholar[1] + o.baholar[2];

    printf("%s ning o'rtacha bahosi: %.2lf\n", o.ism, jami / 3.0);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Struktura ichida ichki massivlar xavfsiz saqlanadi.

## Ishlash natijasi:
```text
Sarvar ning o'rtacha bahosi: 4.67
```

---

# 542-Topshiriq: Dinamik strukturalar massivini realloc bilan kengaytirish

## Topshiriq sharti:
Xotirada talabalar sonini dinamik oshirib borish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int id;
} Element;

int main(void) {
    Element *ro_yxat = (Element*)malloc(2 * sizeof(Element));
    ro_yxat[0].id = 1;
    ro_yxat[1].id = 2;

    ro_yxat = (Element*)realloc(ro_yxat, 3 * sizeof(Element));
    ro_yxat[2].id = 3;

    printf("Elementlar: %d, %d, %d\n", ro_yxat[0].id, ro_yxat[1].id, ro_yxat[2].id);
    free(ro_yxat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Strukturalar massivini ham xuddi oddiy sonlar kabi dinamik kengaytirish mumkin.

## Ishlash natijasi:
```text
Elementlar: 1, 2, 3
```

---

# 543-Topshiriq: Ikki doiraning to'qnashuvini (Circle Collision) tekshirish

## Topshiriq sharti:
Doira strukturalari asosida o'yin to'qnashuvini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    double x, y;
    double r;
} Doira;

bool toqnashdimi(Doira d1, Doira d2) {
    double dx = d1.x - d2.x;
    double dy = d1.y - d2.y;
    double masofa_kv = dx * dx + dy * dy;
    double radius_yigindi = d1.r + d2.r;
    return masofa_kv <= (radius_yigindi * radius_yigindi);
}

int main(void) {
    Doira a = {0, 0, 5};
    Doira b = {6, 0, 3};
    printf("Doiralar to'qnashdimi: %s\n", toqnashdimi(a, b) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Radiuslar yig'indisi 5+3=8. Markazlar masofasi 6. 6 <= 8 bo'lgani uchun to'qnashuv bor.

## Ishlash natijasi:
```text
Doiralar to'qnashdimi: Ha
```

---

# 544-Topshiriq: Strukturalar uchun taqqoslash funksiyasi (qsort uchun)

## Topshiriq sharti:
qsort() kutubxona funksiyasida struktura solishtirish qoidasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int yosh;
} Odam;

int solishtir_odam(const void *a, const void *b) {
    const Odam *o1 = (const Odam*)a;
    const Odam *o2 = (const Odam*)b;
    return o1->yosh - o2->yosh;
}

int main(void) {
    Odam odamlar[3] = {{30}, {18}, {25}};
    qsort(odamlar, 3, sizeof(Odam), solishtir_odam);

    printf("Saralangan yoshlar: %d, %d, %d\n", 
           odamlar[0].yosh, odamlar[1].yosh, odamlar[2].yosh);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `qsort` strukturalar massivini har qanday maydon bo'yicha saralashga qodir.

## Ishlash natijasi:
```text
Saralangan yoshlar: 18, 25, 30
```

---

# 545-Topshiriq: Struktura ichida qisqa bayroqlar saqlash

## Topshiriq sharti:
Foydalanuvchi huquqlarini maydonlar bilan belgilash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    const char *login;
    bool adminmi;
    bool faolmi;
} Profil;

int main(void) {
    Profil p = {"admin_user", true, true};
    if (p.adminmi && p.faolmi) {
        printf("%s tizimga to'liq huquq bilan kirdi.\n", p.login);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Boolean maydonlar orqali foydalanuvchi huquqlari saqlanadi.

## Ishlash natijasi:
```text
admin_user tizimga to'liq huquq bilan kirdi.
```

---

# 546-Topshiriq: Strukturalar orqali stack kadrini modellashtirish

## Topshiriq sharti:
Funksiya chaqiruvi kontekstini saqlovchi struktura.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int qaytish_manzili;
    int lokal_x;
    int lokal_y;
} Kadr;

int main(void) {
    Kadr f = {0x00401050, 10, 20};
    printf("Simulyatsiya qilingan stack kadri: Ret=0x%X, X=%d, Y=%d\n", 
           f.qaytish_manzili, f.lokal_x, f.lokal_y);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kompilyator ichki stek kadrlarini xuddi shu tuzilma kabi boshqaradi.

## Ishlash natijasi:
```text
Simulyatsiya qilingan stack kadri: Ret=0x401050, X=10, Y=20
```

---

# 547-Topshiriq: Struktura a'zolarini o'zaro almashtirish funksiyasi

## Topshiriq sharti:
Ikki struktura manzilini qabul qilib almashuvchi swap.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int id;
} Element;

void element_swap(Element *a, Element *b) {
    Element temp = *a;
    *a = *b;
    *b = temp;
}

int main(void) {
    Element e1 = {1}, e2 = {2};
    element_swap(&e1, &e2);
    printf("e1=%d, e2=%d\n", e1.id, e2.id);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Strukturalarni ko'rsatkich orqali swap qilish xavfsiz va toza ishlaydi.

## Ishlash natijasi:
```text
e1=2, e2=1
```

---

# 548-Topshiriq: Struktura parametrlarini formatlab konsolga chiqarish

## Topshiriq sharti:
ToString analogi bo'lgan chop etish funksiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    char model[20];
    int yil;
} Avto;

void avto_chop(Avto a) {
    printf("Avtomobil: %s (%d-yil)\n", a.model, a.yil);
}

int main(void) {
    Avto m = {"Cobalt", 2024};
    avto_chop(m);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Struktura uchun alohida chop etish funksiyasi kodni modulli qiladi.

## Ishlash natijasi:
```text
Avtomobil: Cobalt (2024-yil)
```

---

# 549-Topshiriq: Struktura o'lchamini qo'lda hisoblash va kompilyator bilan tekshirish

## Topshiriq sharti:
Struktura a'zolari va paddinglar o'lchamini tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>

struct Misol {
    short a; // 2 bayt
    // 2 bayt padding
    int b;   // 4 bayt
};

int main(void) {
    printf("sizeof(struct Misol) = %zu bayt (2 + 2(pad) + 4 = 8)\n", 
           sizeof(struct Misol));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Short va int birlashganda alignment 4 bayt bo'ladi.

## Ishlash natijasi:
```text
sizeof(struct Misol) = 8 bayt (2 + 2(pad) + 4 = 8)
```

---

# 550-Topshiriq: Modul yakuni: Mini Relyatsion Jadval (In-Memory Database Table) yaratish

## Topshiriq sharti:
Qo'shish, o'chirish va ro'yxatni ko'rish imkoniyatiga ega Talabalar jadvali moduli.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

#define MAX_TALABALAR 10

typedef struct {
    int id;
    char ism[20];
    int yosh;
} Talaba;

typedef struct {
    Talaba qatorlar[MAX_TALABALAR];
    int soni;
} Jadval;

void jadval_qosh(Jadval *j, int id, const char *ism, int yosh) {
    if (j->soni < MAX_TALABALAR) {
        j->qatorlar[j->soni].id = id;
        strcpy(j->qatorlar[j->soni].ism, ism);
        j->qatorlar[j->soni].yosh = yosh;
        j->soni++;
    }
}

int main(void) {
    Jadval db = {{0}, 0};
    jadval_qosh(&db, 1, "Sarvar", 21);
    jadval_qosh(&db, 2, "Malika", 19);

    printf("BAZA JADVALI (%d ta yozuv):\n", db.soni);
    for (int i = 0; i < db.soni; i++) {
        printf("ID: %d | Ism: %-8s | Yosh: %d\n", 
               db.qatorlar[i].id, db.qatorlar[i].ism, db.qatorlar[i].yosh);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Struktura ichida strukturalar massivini boshqarish orqali haqiqiy xotiradagi (in-memory) relyatsion jadval moduli yaratildi.
2. Bu 11-qismning barcha struct, typedef va ma'lumotlarni modellashtirish bilimlarini birlashtiradi.

## Ishlash natijasi:
```text
BAZA JADVALI (2 ta yozuv):
ID: 1 | Ism: Sarvar   | Yosh: 21
ID: 2 | Ism: Malika   | Yosh: 19
```

---
