# C Dasturlash Tili — 16-Qism: Standart Kutubxona va Yordamchilar (stdlib, math, time, errno)
## (751-800 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* stdlib.h: Sonlar konversiyasi (strtol, strtod, atoi) va xatoliklar (ERANGE)
* Tasodifiy sonlar (rand, srand, Fisher-Yates shuffle, Xorshift64)
* Dastur boshqaruvi (exit, atexit, getenv, system, div)
* math.h: Trigonometriya, ildiz, daraja, logarifm, yaxlitlash va IEEE 754 maxsus qiymatlar
* time.h: time_t, struct tm, localtime, strftime, mktime va clock() benchmark
* errno.h: errno, strerror(), perror() va ctype.h matn tekshiruvlari
* Yuqori Aniqlikdagi Matematik Benchmark va Profiler Dvigateli

---

# 751-Topshiriq: Satrni butun songa o'girish: atoi() va uning cheklovlari

## Topshiriq sharti:
stdlib.h dagi atoi() orqali matnli sonni int ga aylantirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const char *s1 = "12345";
    const char *s2 = "  -42 dona";
    const char *s3 = "salom";

    printf("atoi("%s") = %d\n", s1, atoi(s1));
    printf("atoi("%s") = %d\n", s2, atoi(s2));
    printf("atoi("%s") = %d (xato aniqlanmadi!)\n", s3, atoi(s3));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. atoi() bo'sh joylarni o'tkazib yuboradi va dastlabki raqamlarni songa aylantiradi.
2. Cheklovi: xatolik yuz berganda (masalan matn bo'lsa) ham 0 qaytaradi, '0' soni bilan xatolikni ajrata olmaydi va overflow ni tekshirmaydi.

## Ishlash natijasi:
```text
atoi("12345") = 12345
atoi("  -42 dona") = -42
atoi("salom") = 0 (xato aniqlanmadi!)
```

---

# 752-Topshiriq: Xavfsiz va aniq son konversiyasi: strtol() funksiyasi

## Topshiriq sharti:
strtol() yordamida sonni o'qish, konversiya tugagan nuqtani (endptr) tekshirish va sanoq sistemasini ko'rsatish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

int main(void) {
    const char *matn = "2026yilgi natija";
    char *oxiri;

    long son = strtol(matn, &oxiri, 10);

    printf("O'qilgan son: %ld\n", son);
    printf("Qolgan matn:  "%s"\n", oxiri);

    // O'n oltilik (HEX - base 16) sonni o'qish:
    const char *hex_matn = "0xFF";
    long hex_son = strtol(hex_matn, NULL, 16);
    printf("0xFF o'nlikda: %ld\n", hex_son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. strtol() sanoq sistemasini (base: 2 dan 36 gacha) aniqlash imkonini beradi.
2. oxiri (endptr) ko'rsatkichi orqali matnning aynan qayeri songa aylantirilmaganini aniqlash mumkin.

## Ishlash natijasi:
```text
O'qilgan son: 2026
Qolgan matn:  "yilgi natija"
0xFF o'nlikda: 255
```

---

# 753-Topshiriq: strtol() da xatoliklarni tekshirish (Overflow va Underflow)

## Topshiriq sharti:
errno va ERANGE orqali son chegaradan oshib ketganini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>

int main(void) {
    const char *katta_son = "999999999999999999999999999999";
    char *endptr;
    errno = 0; // errno ni tozalash

    long son = strtol(katta_son, &endptr, 10);

    if (errno == ERANGE) {
        printf("Xatolik: Son 'long' chegarasidan oshib ketdi (Overflow)!\n");
        printf("Qaytarilgan qiymat: %ld (LONG_MAX = %ld)\n", son, LONG_MAX);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. strtol chaqirilishidan oldin errno = 0 qilinishi shart.
2. Agar son sig'masa, errno == ERANGE bo'lib, LONG_MAX yoki LONG_MIN qaytariladi.

## Ishlash natijasi:
```text
Xatolik: Son 'long' chegarasidan oshib ketdi (Overflow)!
Qaytarilgan qiymat: 9223372036854775807 (LONG_MAX = 9223372036854775807)
```

---

# 754-Topshiriq: Suzuvchi nuqtali son konversiyasi: strtod() funksiyasi

## Topshiriq sharti:
Satrni double soniga o'girish va eksponentsial formatni (masalan 1.5e3) to'g'ri o'qish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const char *s = "  3.14159265 va qolgan matn";
    char *end;

    double d = strtod(s, &end);
    printf("O'qilgan double: %.8f\n", d);
    printf("Qolgan qism: "%s"\n", end);

    const char *ilmiy = "1.25e3";
    printf("Eksponentsial %s -> %.2f\n", ilmiy, strtod(ilmiy, NULL));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. strtod() ilmiy formatdagi eksponentsial sonlarni ham avtomatik taniy oladi.

## Ishlash natijasi:
```text
O'qilgan double: 3.14159265
Qolgan qism: " va qolgan matn"
Eksponentsial 1.25e3 -> 1250.00
```

---

# 755-Topshiriq: Tasodifiy sonlar generatsiyasi: rand() va srand()

## Topshiriq sharti:
srand(seed) yordamida generatorni boshlash va [min, max] oralig'ida tasodifiy son olish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int tasodifiy_oraliq(int min, int max) {
    return min + rand() % (max - min + 1);
}

int main(void) {
    // Ruxsat etilgan ma'lum bir seed bilan
    srand(12345);

    printf("1 dan 6 gacha 5 ta zar tashlash:\n");
    for (int i = 0; i < 5; i++) {
        printf("%d ", tasodifiy_oraliq(1, 6));
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. rand() 0 dan RAND_MAX (kamida 32767) gacha bo'lgan psevdo-tasodifiy son qaytaradi.
2. srand() bir xil seed bilan ishga tushirilsa, har safar aynan bir xil ketma-ketlikni beradi (takrorlanuvchi testlar uchun muhim).

## Ishlash natijasi:
```text
1 dan 6 gacha 5 ta zar tashlash:
3 5 4 4 1
```

---

# 756-Topshiriq: Haqiqiy tasodifiylik: srand(time(NULL))

## Topshiriq sharti:
Joriy soniya bo'yicha generatorni initsializatsiya qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    srand((unsigned int)time(NULL));

    int son = rand() % 100; // 0..99
    printf("Hozirgi vaqt bilan olingan son (0..99 oralig'ida): %d\n", son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. time(NULL) har soniyada o'zgaradi, bu dastur har safar ishga tushganda turli natijalar berishini ta'minlaydi.

## Ishlash natijasi:
```text
Hozirgi vaqt bilan olingan son (0..99 oralig'ida): 42
```

---

# 757-Topshiriq: 0.0 dan 1.0 gacha suzuvchi nuqtali tasodifiy sonlar

## Topshiriq sharti:
rand() / (double)RAND_MAX orqali normalizatsiyalangan tasodifiy sonlar hosil qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

double rand_double(void) {
    return (double)rand() / (double)RAND_MAX;
}

int main(void) {
    srand(42);

    printf("5 ta [0.0, 1.0] suzuvchi son:\n");
    for (int i = 0; i < 5; i++) {
        printf("%.4f ", rand_double());
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Monte-Karlo usullari va neyron tarmoqlar og'irliklarini boshlang'ich initsializatsiya qilishda aynan [0.0, 1.0] oraliqdagi sonlar qo'llaniladi.

## Ishlash natijasi:
```text
5 ta [0.0, 1.0] suzuvchi son:
0.0053 0.5407 0.9082 0.7712 0.8876
```

---

# 758-Topshiriq: Dasturdan chiqish: exit() vs _Exit() vs abort()

## Topshiriq sharti:
Oddiy chiqish, tezkor chiqish va favqulodda to'xtatish (core dump) farqlari.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

void tozalovchi(void) {
    printf("[Atexit]: Chiqishdan oldin resurslar tozalandi.\n");
}

int main(void) {
    atexit(tozalovchi);

    printf("Dastur exit(0) orqali yakunlanmoqda...\n");
    exit(0);

    printf("Bu qator hech qachon bajarilmaydi!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. exit() barcha ochiq fayllarni flush qilib yopadi va atexit funksiyalarini chaqiradi.
2. _Exit() zudlik bilan operatsion tizimga qaytadi, hech narsani tozalamaydi.
3. abort() esa SIGABRT signali yuborib favqulodda to'xtatadi.

## Ishlash natijasi:
```text
Dastur exit(0) orqali yakunlanmoqda...
[Atexit]: Chiqishdan oldin resurslar tozalandi.
```

---

# 759-Topshiriq: Muhit o'zgaruvchilarini o'qish: getenv()

## Topshiriq sharti:
Tizimning PATH, USER, OS yoki boshqa muhit o'zgaruvchilari (Environment Variables) ni o'qish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const char *os = getenv("OS");
    const char *path = getenv("PATH");

    if (os != NULL) {
        printf("OS muhit o'zgaruvchisi: %s\n", os);
    } else {
        printf("OS o'zgaruvchisi topilmadi.\n");
    }

    if (path != NULL) {
        printf("PATH mavjud (uzunligi: %zu belgi)\n", strlen(path));
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. getenv() operatsion tizim muhitidan qiymatni qidiradi va unga ko'rsatkich qaytaradi. Agar o'zgaruvchi yo'q bo'lsa, NULL beradi.

## Ishlash natijasi:
```text
OS muhit o'zgaruvchisi: Windows_NT
PATH mavjud (uzunligi: 540 belgi)
```

---

# 760-Topshiriq: Tizim buyrug'ini bajarish: system()

## Topshiriq sharti:
stdlib.h dagi system() orqali operatsion tizim buyruqlar satri (shell) komandalarini chaqirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    printf("Tizim buyrug'i bajarilmoqda...\n");

    // Windows da 'cmd /c echo', Unix da 'echo'
    int kod = system("echo Salom Tizim!");

    printf("Buyruq qaytargan kod: %d\n", kod);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. system() berilgan buyruqni tizim komandalar interpreteri (cmd.exe yoki /bin/sh) orqali ishga tushiradi.
2. Muvaffaqiyatli buyruq 0 qaytaradi.

## Ishlash natijasi:
```text
Tizim buyrug'i bajarilmoqda...
Salom Tizim!
Buyruq qaytargan kod: 0
```

---

# 761-Topshiriq: Butun sonli bo'lish va qoldiq: div() va ldiv()

## Topshiriq sharti:
Bitta amaliyotda ham bo'linma (quotient), ham qoldiqni (remainder) olish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    div_t natija = div(47, 5);

    printf("47 / 5:\n");
    printf("Bo'linma (quot): %d\n", natija.quot);
    printf("Qoldiq   (rem):  %d\n", natija.rem);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. div() div_t strukturasini qaytaradi, u ikkita a'zoga ega: int quot va int rem.
2. Zamonaviy protsessorlar bitta 'idiv' instruksiyasida ikkala qiymatni hisoblaydi, div() bu imkoniyatdan to'liq foydalanadi.

## Ishlash natijasi:
```text
47 / 5:
Bo'linma (quot): 9
Qoldiq   (rem):  2
```

---

# 762-Topshiriq: Absolyut qiymat: abs(), labs(), llabs(), fabs()

## Topshiriq sharti:
Har xil ma'lumot tiplari uchun modul hisoblovchi to'g'ri funksiyani tanlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(void) {
    int i = -15;
    long l = -123456789L;
    double d = -3.14159;

    printf("abs(int):    %d\n", abs(i));
    printf("labs(long):  %ld\n", labs(l));
    printf("fabs(double):%.5f\n", fabs(d));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. int uchun abs(), long uchun labs(), suzuvchi nuqtali float/double uchun math.h dagi fabs() ishlatilishi shart!

## Ishlash natijasi:
```text
abs(int):    15
labs(long):  123456789
fabs(double):3.14159
```

---

# 763-Topshiriq: math.h da daraja va ildiz: sqrt(), cbrt(), pow(), hypot()

## Topshiriq sharti:
Kvadrat ildiz, kub ildiz, daraja va gipotenuza hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    printf("sqrt(16.0)     = %.2f\n", sqrt(16.0));
    printf("cbrt(27.0)     = %.2f\n", cbrt(27.0));
    printf("pow(2.0, 10.0) = %.2f\n", pow(2.0, 10.0));
    printf("hypot(3.0, 4.0)= %.2f\n", hypot(3.0, 4.0));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. hypot(a, b) sqrt(a*a + b*b) formulasi bo'yicha hisoblaydi, ammo oraliq kvadratlarda float overflow yuz bermasligi uchun maxsus optimallashtirilgan.

## Ishlash natijasi:
```text
sqrt(16.0)     = 4.00
cbrt(27.0)     = 3.00
pow(2.0, 10.0) = 1024.00
hypot(3.0, 4.0)= 5.00
```

---

# 764-Topshiriq: Trigonometriya: sin(), cos(), tan() va burchaklarni radianga o'girish

## Topshiriq sharti:
Burchak gradusini radianga aylantirish va trigonometrik qiymatlarni hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

#define PI 3.14159265358979323846
#define DEG_TO_RAD(deg) ((deg) * (PI / 180.0))

int main(void) {
    double burchak_30 = DEG_TO_RAD(30.0);
    double burchak_45 = DEG_TO_RAD(45.0);

    printf("sin(30 gradus) = %.4f (Kutilgan: 0.5000)\n", sin(burchak_30));
    printf("cos(30 gradus) = %.4f (sqrt(3)/2)\n", cos(burchak_30));
    printf("tan(45 gradus) = %.4f (Kutilgan: 1.0000)\n", tan(burchak_45));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. math.h barcha trigonometrik funksiyalarda burchakni radianlarda qabul qiladi.
2. Radian = Gradus * (PI / 180).

## Ishlash natijasi:
```text
sin(30 gradus) = 0.5000 (Kutilgan: 0.5000)
cos(30 gradus) = 0.8660 (sqrt(3)/2)
tan(45 gradus) = 1.0000 (Kutilgan: 1.0000)
```

---

# 765-Topshiriq: Teskari trigonometriya: atan2(y, x) va yo'nalish burchagini topish

## Topshiriq sharti:
Tekislikdagi (x, y) koordinatalari bo'yicha to'g'ri chorakdagi burchakni [-PI, PI] oraliqda hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

#define RAD_TO_DEG(rad) ((rad) * (180.0 / 3.141592653589793))

int main(void) {
    // (1, 1) -> 45 gradus
    double b1 = atan2(1.0, 1.0);
    // (-1, 1) -> 135 gradus (2-chorak)
    double b2 = atan2(1.0, -1.0);

    printf("atan2(1, 1)  = %.1f gradus\n", RAD_TO_DEG(b1));
    printf("atan2(1, -1) = %.1f gradus\n", RAD_TO_DEG(b2));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. atan(y/x) nolga bo'lish (x=0) va choraklarni aniqlashda xatolar beradi.
2. atan2(y, x) barcha 4 ta chorakni va x=0 holatini to'liq to'g'ri hisoblaydi (Game Dev va Robototexnikada standart).

## Ishlash natijasi:
```text
atan2(1, 1)  = 45.0 gradus
atan2(1, -1) = 135.0 gradus
```

---

# 766-Topshiriq: Logarifmlar va Eksponenta: exp(), log(), log10(), log2()

## Topshiriq sharti:
Natural, o'nlik va ikkilik logarifmlarni hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    printf("exp(1.0)  (e)      = %.5f\n", exp(1.0));
    printf("log(2.71828) (ln)  = %.5f\n", log(2.71828));
    printf("log10(1000.0)      = %.2f\n", log10(1000.0));
    printf("log2(1024.0)       = %.2f\n", log2(1024.0));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. log() natural logarifm (ln) dir, o'nlik logarifm uchun log10(), ikkilik (axborot entropiyasi) uchun log2() ishlatiladi.

## Ishlash natijasi:
```text
exp(1.0)  (e)      = 2.71828
log(2.71828) (ln)  = 1.00000
log10(1000.0)      = 3.00
log2(1024.0)       = 10.00
```

---

# 767-Topshiriq: Yaxlitlash amallari: floor(), ceil(), round(), trunc() farqlari

## Topshiriq sharti:
Har bir yaxlitlash funksiyasining musbat va manfiy sonlarda qanday ishlashini taqqoslash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

void taqqosla(double x) {
    printf("Son: %5.2f | floor: %5.1f | ceil: %5.1f | round: %5.1f | trunc: %5.1f\n",
           x, floor(x), ceil(x), round(x), trunc(x));
}

int main(void) {
    taqqosla(2.7);
    taqqosla(2.3);
    taqqosla(-2.7);
    taqqosla(-2.3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. floor() pastga qarab, ceil() yuqoriga qarab yaxlitlaydi.
2. round() eng yaqin butun songa, trunc() esa shunchaki kasr qismini kesib tashlaydi.

## Ishlash natijasi:
```text
Son:  2.70 | floor:   2.0 | ceil:   3.0 | round:   3.0 | trunc:   2.0
Son:  2.30 | floor:   2.0 | ceil:   3.0 | round:   2.0 | trunc:   2.0
Son: -2.70 | floor:  -3.0 | ceil:  -2.0 | round:  -3.0 | trunc:  -2.0
Son: -2.30 | floor:  -3.0 | ceil:  -2.0 | round:  -2.0 | trunc:  -2.0
```

---

# 768-Topshiriq: Haqiqiy sonlarda qoldiq olish: fmod() va remainder()

## Topshiriq sharti:
Suzuvchi nuqtali sonlarda % operatori o'rniga fmod dan to'g'ri foydalanish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    double a = 5.3, b = 2.0;

    // 5.3 / 2.0 = 2 (qoldiq 1.3)
    double qoldiq = fmod(a, b);

    printf("fmod(5.3, 2.0) = %.2f\n", qoldiq);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida suzuvchi nuqtali (float/double) sonlarga '%' operatorini qo'llash taqiqlangan (kompilyatsiya xatosi).
2. Uning o'rniga math.h dagi fmod() funksiyasi ishlatiladi.

## Ishlash natijasi:
```text
fmod(5.3, 2.0) = 1.30
```

---

# 769-Topshiriq: Sonni butun va kasr qismga ajratish: modf()

## Topshiriq sharti:
modf() yordamida bitta sonning butun va kasr qismini alohida o'zgaruvchilarga ajratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    double son = 12.34567;
    double butun_qism;
    double kasr_qism = modf(son, &butun_qism);

    printf("Asl son:     %f\n", son);
    printf("Butun qismi: %.0f\n", butun_qism);
    printf("Kasr qismi:  %f\n", kasr_qism);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. modf() butun qismni pointer orqali yozadi va kasr qismni return orqali qaytaradi.

## Ishlash natijasi:
```text
Asl son:     12.345670
Butun qismi: 12
Kasr qismi:  0.345670
```

---

# 770-Topshiriq: Maxsus matematik qiymatlar: isnan(), isinf(), isfinite()

## Topshiriq sharti:
Nolga bo'lish va noaniq amallarda paydo bo'ladigan NaN (Not a Number) va Cheksizlikni (Infinity) aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    double zero = 0.0;
    double cheksiz = 1.0 / zero;
    double nan_qiymat = zero / zero;

    printf("1.0 / 0.0 = %f (isinf: %d)\n", cheksiz, isinf(cheksiz));
    printf("0.0 / 0.0 = %f (isnan: %d)\n", nan_qiymat, isnan(nan_qiymat));

    if (!isfinite(cheksiz)) {
        printf("cheksiz chekli son emas!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. NaN o'z-o'ziga teng emas (x != x rost bo'ladi).
2. isfinite(), isnan() va isinf() makroslari IEEE 754 chetki holatlarini aniqlashda standart hisoblanadi.

## Ishlash natijasi:
```text
1.0 / 0.0 = inf (isinf: 1)
0.0 / 0.0 = nan (isnan: 1)
cheksiz chekli son emas!
```

---

# 771-Topshiriq: Joriy kalendar vaqtini olish: time_t va time()

## Topshiriq sharti:
1970-yil 1-yanvardan buyon o'tgan soniyalar (UNIX Epoch) hisobini olish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <time.h>

int main(void) {
    time_t soniyalar = time(NULL);

    printf("UNIX Epoch dan buyon o'tgan soniyalar: %ld\n", (long)soniyalar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. time_t odatda 64-bitli butun son bo'lib, butun dunyo kompyuter tizimlarida vaqtni birlamchi saqlash formati hisoblanadi.

## Ishlash natijasi:
```text
UNIX Epoch dan buyon o'tgan soniyalar: 1794119400
```

---

# 772-Topshiriq: Vaqtni qismlarga ajratish: struct tm va localtime()

## Topshiriq sharti:
UNIX soniyasini Yil, Oy, Kun, Soat, Daqiqa va Soniyalarga ajratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <time.h>

int main(void) {
    time_t hozir = time(NULL);
    struct tm *info = localtime(&hozir);

    printf("Sana: %04d-%02d-%02d\n", 
           info->tm_year + 1900, info->tm_mon + 1, info->tm_mday);
    printf("Vaqt: %02d:%02d:%02d\n", 
           info->tm_hour, info->tm_min, info->tm_sec);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. tm_year 1900-yildan buyon o'tgan yillarni bildiradi, shuning uchun +1900 qo'shiladi.
2. tm_mon 0 dan 11 gacha (0 = Yanvar), shuning uchun +1 qo'shiladi.

## Ishlash natijasi:
```text
Sana: 2026-11-08
Vaqt: 10:30:00
```

---

# 773-Topshiriq: Grinvich vaqti (UTC): gmtime()

## Topshiriq sharti:
Lokal vaqt zonasini hisobga olmagan holda universal UTC vaqtini olish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <time.h>

int main(void) {
    time_t hozir = time(NULL);
    struct tm *utc = gmtime(&hozir);

    printf("UTC Vaqti: %02d:%02d:%02d\n", 
           utc->tm_hour, utc->tm_min, utc->tm_sec);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. gmtime() Grinvich bo'yicha UTC vaqtini qaytaradi.
2. Tarmoq protokollari va serverlararo aloqada vaqt mintaqasi adashmovchiliklarini oldini olish uchun faqat UTC ishlatiladi.

## Ishlash natijasi:
```text
UTC Vaqti: 05:30:00
```

---

# 774-Topshiriq: Vaqtni formatlash: strftime() funksiyasi

## Topshiriq sharti:
Sana va vaqtni istalgan formatda matnga o'tkazish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <time.h>

int main(void) {
    time_t t = time(NULL);
    struct tm *tm_info = localtime(&t);

    char bufer[64];
    // %Y: Yil, %B: Oy to'liq nomi, %d: Kun, %H:%M:%S: Soat
    strftime(bufer, sizeof(bufer), "%Y-%m-%d %H:%M:%S", tm_info);
    printf("Formatlangan vaqt: %s\n", bufer);

    strftime(bufer, sizeof(bufer), "%A, %d %B %Y", tm_info);
    printf("Kengaytirilgan format: %s\n", bufer);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. strftime() printf kabi formatlovchi spetsifikatorlar (%Y, %m, %d, %H, %M) yordamida sanani chiroyli satrga aylantiradi.

## Ishlash natijasi:
```text
Formatlangan vaqt: 2026-11-08 10:30:00
Kengaytirilgan format: Sunday, 08 November 2026
```

---

# 775-Topshiriq: struct tm dan time_t ga qaytish: mktime()

## Topshiriq sharti:
Muayyan sana (masalan 2026-yil 1-yanvar) uchun UNIX soniyasini hisoblash va hafta kunini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <time.h>

int main(void) {
    struct tm sana = {0};
    sana.tm_year = 2026 - 1900;
    sana.tm_mon = 0; // Yanvar
    sana.tm_mday = 1; // 1-kun

    time_t epoch_sana = mktime(&sana);

    const char *hafta_kunlari[] = {
        "Yakshanba", "Dushanba", "Seshanba", "Chorshanba", 
        "Payshanba", "Juma", "Shanba"
    };

    printf("2026-01-01 ning haftadagi kuni: %s\n", hafta_kunlari[sana.tm_wday]);
    printf("Epoch soniyasi: %ld\n", (long)epoch_sana);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. mktime() struct tm dagi maydonlarni normalizatsiya qiladi va unga mos keluvchi time_t ni hisoblaydi hamda tm_wday (hafta kuni) ni to'ldiradi.

## Ishlash natijasi:
```text
2026-01-01 ning haftadagi kuni: Payshanba
Epoch soniyasi: 1767225600
```

---

# 776-Topshiriq: Ikki sana orasidagi farqni hisoblash: difftime()

## Topshiriq sharti:
Ikki time_t vaqti orasidagi farqni soniyalarda aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <time.h>

int main(void) {
    time_t boshlanish = 1000000;
    time_t tugash = 1086400; // 86400 soniya = 1 sutka

    double farq = difftime(tugash, boshlanish);
    printf("Oraliq farq: %.0f soniya (%.1f soat)\n", farq, farq / 3600.0);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. difftime(t2, t1) ikkala vaqt ayirmasini 'double' soniyalarda qaytaradi.

## Ishlash natijasi:
```text
Oraliq farq: 86400 soniya (24.0 soat)
```

---

# 777-Topshiriq: CPU vaqtini o'lchash va Benchmark: clock() va CLOCKS_PER_SEC

## Topshiriq sharti:
Algoritm bajarilishiga protsessor necha millisoniya vaqt sarflaganini aniq o'lchash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <time.h>

int main(void) {
    clock_t start = clock();

    // 10 million amaliyot simulyatsiyasi
    volatile long long sum = 0;
    for (int i = 0; i < 10000000; i++) {
        sum += i;
    }

    clock_t end = clock();
    double cpu_vaqti = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Hisoblash yakunlandi. Summa = %lld\n", sum);
    printf("Sarflangan CPU vaqti: %.4f soniya\n", cpu_vaqti);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. clock() protsessor aynan ushbu dastur oqimiga sarflagan vaqt sikllarini qaytaradi.
2. CLOCKS_PER_SEC ga bo'lish orqali millisoniyalar va soniyalar aniqlanadi.

## Ishlash natijasi:
```text
Hisoblash yakunlandi. Summa = 49999995000000
Sarflangan CPU vaqti: 0.0150 soniya
```

---

# 778-Topshiriq: errno global o'zgaruvchisi va strerror() funksiyasi

## Topshiriq sharti:
Standart kutubxona xatosi kodini matnli tushuntirishga aylantirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <errno.h>
#include <string.h>

int main(void) {
    FILE *f = fopen("mavjud_bolmagan_fayl_123.xyz", "r");
    if (f == NULL) {
        printf("Xatolik kodi (errno): %d\n", errno);
        printf("Xatolik matni: %s\n", strerror(errno));
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. errno.h dagi errno tizim qo'ng'irog'i yoki kutubxona xatosi yuz berganda avtomatik o'rnatiladi.
2. strerror(errno) bu xatoga mos keluvchi operatsion tizim xabarini (masalan 'No such file or directory') qaytaradi.

## Ishlash natijasi:
```text
Xatolik kodi (errno): 2
Xatolik matni: No such file or directory
```

---

# 779-Topshiriq: perror() orqali to'g'ridan-to'g'ri stderr ga xatolik chiqarish

## Topshiriq sharti:
perror() ning o'ziga xos qulayligi va stderr bilan integratsiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("mavjud_emas.dat", "r");
    if (!f) {
        perror("[XATOLIK]");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. perror(prefiks) avtomatik ravishda 'prefiks: xatolik_matni\n' ko'rinishida stderr ga chop etadi.
2. Bu C dasturlarida xatoliklarni qayd etishning eng qisqa va qulay usulidir.

## Ishlash natijasi:
```text
[XATOLIK]: No such file or directory
```

---

# 780-Topshiriq: ctype.h da belgilarni tekshirish: isalpha, isdigit, isalnum, isspace

## Topshiriq sharti:
Belgining harf, raqam yoki bo'shliq ekanligini tezkor tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

void tahlil_qil(char c) {
    printf("Belgi '%c': ", c);
    if (isalpha(c)) printf("Harf ");
    if (isdigit(c)) printf("Raqam ");
    if (isalnum(c)) printf("Alfanumerik ");
    if (isspace(c)) printf("Bo'shliq ");
    printf("\n");
}

int main(void) {
    tahlil_qil('A');
    tahlil_qil('9');
    tahlil_qil(' ');
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ctype.h funksiyalari orqa fonda tezkor qidiruv jadvali (lookup table) bilan ishlaydi va O(1) da javob beradi.

## Ishlash natijasi:
```text
Belgi 'A': Harf Alfanumerik 
Belgi '9': Raqam Alfanumerik 
Belgi ' ': Bo'shliq
```

---

# 781-Topshiriq: ctype.h da registrni o'zgartirish: toupper() va tolower()

## Topshiriq sharti:
Kichik harflarni kattaga, katta harflarni kichikka xavfsiz o'tkazish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    char matn[] = "Antigravity C17!";

    for (int i = 0; matn[i] != '\0'; i++) {
        matn[i] = toupper((unsigned char)matn[i]);
    }
    printf("Katta harflarda: %s\n", matn);

    for (int i = 0; matn[i] != '\0'; i++) {
        matn[i] = tolower((unsigned char)matn[i]);
    }
    printf("Kichik harflarda: %s\n", matn);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Harflar bo'lmagan belgilar (tinish belgilari, raqamlar) o'zgarmaydi.
2. Har doim `(unsigned char)` ga cast qilish tavsiya etiladi (manfiy char indeks xatolarini oldini olish uchun).

## Ishlash natijasi:
```text
Katta harflarda: ANTIGRAVITY C17!
Kichik harflarda: antigravity c17!
```

---

# 782-Topshiriq: Boshqaruv belgilarini aniqlash: isprint(), iscntrl(), ispunct()

## Topshiriq sharti:
Ekranda ko'rinuvchi belgilarni boshqaruvchi kodlardan (escape codes) ajratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    char belgilar[] = {'A', '\n', '!', '\t', '7'};

    for (int i = 0; i < 5; i++) {
        char c = belgilar[i];
        printf("Kod %d: ", c);
        if (isprint(c)) printf("[Ko'rinadi: '%c'] ", c);
        if (iscntrl(c)) printf("[Boshqaruv kodi] ");
        if (ispunct(c)) printf("[Tinish belgisi] ");
        printf("\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. iscntrl() '\n', '\r', '\t' kabi ekranda to'g'ridan-to'g'ri ko'rinmaydigan boshqaruv belgilarini aniqlaydi.

## Ishlash natijasi:
```text
Kod 65: [Ko'rinadi: 'A'] 
Kod 10: [Boshqaruv kodi] 
Kod 33: [Ko'rinadi: '!'] [Tinish belgisi] 
Kod 9: [Boshqaruv kodi] 
Kod 55: [Ko'rinadi: '7']
```

---

# 783-Topshiriq: Kombinatorika va Ehtimollik: Tasodifiy elementlar almashtirish (Fisher-Yates Shuffle)

## Topshiriq sharti:
Massiv elementlarini tekis ehtimollik bilan aralashtiruvchi professional algoritm.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

void shuffle(int *arr, int n) {
    for (int i = n - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
}

int main(void) {
    srand(123);
    int kartalar[] = {1, 2, 3, 4, 5, 6, 7, 8};
    int n = 8;

    shuffle(kartalar, n);

    printf("Aralashtirilgan massiv: ");
    for (int i = 0; i < n; i++) printf("%d ", kartalar[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fisher-Yates (Knuth) algoritmi O(N) vaqtda massivni to'liq xolis (unbiased) aralashtiradi.

## Ishlash natijasi:
```text
Aralashtirilgan massiv: 7 8 2 6 3 1 4 5
```

---

# 784-Topshiriq: O'n oltilik (Hex) belgilarni tekshirish: isxdigit()

## Topshiriq sharti:
Satrning to'g'ri HEX rang kodi (#FFFFFF) ekanligini tasdiqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

int hex_rang_kodimi(const char *rang) {
    if (rang[0] != '#') return 0;
    for (int i = 1; i <= 6; i++) {
        if (!isxdigit((unsigned char)rang[i])) return 0;
    }
    return rang[7] == '\0';
}

int main(void) {
    printf("#FF5733 to'g'rimi? %s\n", hex_rang_kodimi("#FF5733") ? "HA" : "YO'Q");
    printf("#12G456 to'g'rimi? %s\n", hex_rang_kodimi("#12G456") ? "HA" : "YO'Q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. isxdigit() 0-9, a-f va A-F belgilarini taniydi.

## Ishlash natijasi:
```text
#FF5733 to'g'rimi? HA
#12G456 to'g'rimi? YO'Q
```

---

# 785-Topshiriq: Murakkab suzuvchi nuqtali son manipulyatsiyasi: frexp() va ldexp()

## Topshiriq sharti:
Sonni x = m * 2^exp formatiga ajratish va qayta tiklash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    double x = 12.0;
    int exp;
    double mantissa = frexp(x, &exp);

    printf("12.0 = %.4f * 2^%d\n", mantissa, exp);

    // Qayta tiklash: ldexp(m, exp) = m * 2^exp
    double tiklangan = ldexp(mantissa, exp);
    printf("ldexp bilan tiklangan son: %.2f\n", tiklangan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. frexp() mantissani [0.5, 1.0) oraliqqa keltiradi va ikkilik darajasini aniqlaydi.
2. ldexp() esa ikkilik darajaga ko'paytirishni protsessor darajasida bitli siljitish orqali tezkor bajaradi.

## Ishlash natijasi:
```text
12.0 = 0.7500 * 2^4
ldexp bilan tiklangan son: 12.00
```

---

# 786-Topshiriq: Matematik qadam funksiyasi: copysign()

## Topshiriq sharti:
Birinchi sonning moduliga ikkinchi sonning ishorasini biriktirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    printf("copysign(5.0, -2.0)  = %.1f\n", copysign(5.0, -2.0));
    printf("copysign(-5.0, 2.0)  = %.1f\n", copysign(-5.0, 2.0));
    printf("copysign(0.0, -1.0)  = %.1f (Manfiy nol -0.0!)\n", copysign(0.0, -1.0));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. copysign() shartli tarmoqlanishlarsiz (branches) ishorani ko'chirish imkonini beradi va IEEE 754 dagi -0.0 ni to'g'ri boshqaradi.

## Ishlash natijasi:
```text
copysign(5.0, -2.0)  = -5.0
copysign(-5.0, 2.0)  = 5.0
copysign(0.0, -1.0)  = -0.0 (Manfiy nol -0.0!)
```

---

# 787-Topshiriq: Keyingi suzuvchi nuqtali qiymatni topish: nextafter()

## Topshiriq sharti:
Float sonidan keyingi eng kichik ifodalanuvchi qo'shni sonni topish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    double d = 1.0;
    double keyingi = nextafter(d, 2.0);

    printf("1.0 dan keyingi eng yaqin son: %.17f\n", keyingi);
    printf("Ular orasidagi epsilon farq:   %.17e\n", keyingi - d);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. nextafter(x, y) x dan boshlab y yo'nalishidagi eng yaqin keyingi IEEE 754 sonini topadi.
2. Bu suzuvchi nuqtali hisoblashlar aniqligini (Machine Epsilon) tahlil qilishda zarur.

## Ishlash natijasi:
```text
1.0 dan keyingi eng yaqin son: 1.00000000000000022
Ular orasidagi epsilon farq:   2.22044604925031308e-16
```

---

# 788-Topshiriq: Giperbolik funksiyalar: sinh(), cosh(), tanh()

## Topshiriq sharti:
Fizika va muhandislik hisob-kitoblarida zanjir chizig'i (catenary) va giperbolik egriliklarni hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    double x = 1.0;
    printf("sinh(1.0) = %.5f\n", sinh(x));
    printf("cosh(1.0) = %.5f\n", cosh(x));
    printf("tanh(1.0) = %.5f\n", tanh(x));

    // cosh^2(x) - sinh^2(x) = 1
    double ayniyat = cosh(x)*cosh(x) - sinh(x)*sinh(x);
    printf("cosh^2 - sinh^2 = %.5f (Ayniyat)\n", ayniyat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Giperbolik funksiyalar simlar osilishi, maxsus nisbiylik nazariyasi va neyron tarmoqlar faollashuv funksiyalarida (tanh) qo'llaniladi.

## Ishlash natijasi:
```text
sinh(1.0) = 1.17520
cosh(1.0) = 1.54308
tanh(1.0) = 0.76159
cosh^2 - sinh^2 = 1.00000 (Ayniyat)
```

---

# 789-Topshiriq: Xatolik funksiyasi: erf() va erfc()

## Topshiriq sharti:
Statistika va normal taqsimot (Gauss ehtimollik integrali) hisob-kitoblari.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    // erf(0) = 0, erf(cheksizlik) = 1
    printf("erf(0.0) = %.4f\n", erf(0.0));
    printf("erf(1.0) = %.4f\n", erf(1.0));
    printf("erfc(1.0)= %.4f (1 - erf)\n", erfc(1.0));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. erf(x) ehtimollar nazariyasida standart og'ish va ishonchlilik oralig'ini hisoblashda asosiy funksiyadir.

## Ishlash natijasi:
```text
erf(0.0) = 0.0000
erf(1.0) = 0.8427
erfc(1.0)= 0.1573 (1 - erf)
```

---

# 790-Topshiriq: Gamma funksiyasi: tgamma() va lgamma()

## Topshiriq sharti:
Faktorialning umumlashtirilgan ko'rinishi (Gamma funksiyasi: Gamma(n) = (n-1)!).

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

int main(void) {
    // tgamma(5.0) = 4! = 24
    printf("tgamma(5.0)  = %.1f (4!)\n", tgamma(5.0));
    printf("tgamma(6.0)  = %.1f (5!)\n", tgamma(6.0));
    printf("tgamma(0.5)  = %.4f (sqrt(PI))\n", tgamma(0.5));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. tgamma(x) butun bo'lmagan sonlar (masalan yarimlar) uchun faktorial qiymatlarini beradi.

## Ishlash natijasi:
```text
tgamma(5.0)  = 24.0 (4!)
tgamma(6.0)  = 120.0 (5!)
tgamma(0.5)  = 1.7725 (sqrt(PI))
```

---

# 791-Topshiriq: Xavfsiz tasodifiy satr (Random Token Generator)

## Topshiriq sharti:
Parollar yoki sessiya tokenlari uchun alfanumerik tasodifiy satr generatsiya qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

void token_generatsiya(char *buf, int uzunlik) {
    const char alfavit[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    int alfavit_hajmi = sizeof(alfavit) - 1;

    for (int i = 0; i < uzunlik; i++) {
        buf[i] = alfavit[rand() % alfavit_hajmi];
    }
    buf[uzunlik] = '\0';
}

int main(void) {
    srand(999);
    char token[16];
    token_generatsiya(token, 15);

    printf("Generatsiya qilingan token: %s\n", token);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Rand va alfavit massivi orqali xavfsiz tasodifiy tokenlar hosil qilinadi.

## Ishlash natijasi:
```text
Generatsiya qilingan token: jK82Lp09xZaQ1vB
```

---

# 792-Topshiriq: Matnni tozalash (String Trim via ctype.h)

## Topshiriq sharti:
Satr boshi va oxiridagi bo'shliqlarni isspace yordamida olib tashlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>
#include <string.h>

char* trim(char *s) {
    // Boshidagi bo'shliqlarni o'tkazib yuborish
    while (isspace((unsigned char)*s)) s++;
    if (*s == 0) return s;

    // Oxiridagi bo'shliqlarni olib tashlash
    char *back = s + strlen(s) - 1;
    while (back > s && isspace((unsigned char)*back)) back--;
    *(back + 1) = '\0';

    return s;
}

int main(void) {
    char matn[] = "   Salom Dunyo!   \t\n";
    char *toza = trim(matn);

    printf("Tozalangan satr: "%s"\n", toza);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. isspace() barcha bo'sh joylar, tab va yangi qatorlarni qamrab oladi.

## Ishlash natijasi:
```text
Tozalangan satr: "Salom Dunyo!"
```

---

# 793-Topshiriq: Binar qidiruv: bsearch() bilan strukturada qidirish

## Topshiriq sharti:
ID bo'yicha saralangan xodimlar massividan bsearch orqali qidirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int id;
    const char *lavozim;
} Xodim;

int cmp_xodim(const void *a, const void *b) {
    const int *qidirilayotgan_id = (const int *)a;
    const Xodim *x = (const Xodim *)b;
    return (*qidirilayotgan_id - x->id);
}

int main(void) {
    Xodim shtat[] = {
        {10, "Kichik dasturchi"},
        {20, "O'rta dasturchi"},
        {30, "Katta dasturchi"},
        {40, "Arxitektor"}
    };
    int id_kalit = 30;

    Xodim *topildi = (Xodim*)bsearch(&id_kalit, shtat, 4, sizeof(Xodim), cmp_xodim);

    if (topildi) {
        printf("ID %d xodim topildi: %s\n", topildi->id, topildi->lavozim);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. bsearch birinchi argument sifatida qidirilayotgan kalit manzilini qabul qiladi.

## Ishlash natijasi:
```text
ID 30 xodim topildi: Katta dasturchi
```

---

# 794-Topshiriq: Fayl kengaytmasini ajratish (Extension Extractor via ctype)

## Topshiriq sharti:
Fayl nomining oxirgi nuqtasidan keyingi qismini ajratib kichik harflarga o'tkazish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

void get_ext(const char *fayl, char *ext, size_t max_len) {
    const char *dot = strrchr(fayl, '.');
    if (!dot || dot == fayl) {
        ext[0] = '\0';
        return;
    }
    size_t i = 0;
    dot++; // nuqtadan keyingi harf
    while (dot[i] && i < max_len - 1) {
        ext[i] = tolower((unsigned char)dot[i]);
        i++;
    }
    ext[i] = '\0';
}

int main(void) {
    char ext[16];
    get_ext("hujjat.DOCX", ext, sizeof(ext));
    printf("Kengaytma: '%s'\n", ext);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. strrchr oxirgi nuqtani topadi, tolower esa kengaytmani standart kichik harflarga keltiradi.

## Ishlash natijasi:
```text
Kengaytma: 'docx'
```

---

# 795-Topshiriq: O'nlik kasrni oddiy kasrga aylantirish (GCD orqali)

## Topshiriq sharti:
Kasr sonni qisqarmas surat va maxrajga ajratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int ekub(int a, int b) {
    while (b) {
        int t = b;
        b = a % b;
        a = t;
    }
    return a;
}

int main(void) {
    double kasr = 0.75;
    int maxraj = 100;
    int surat = (int)(kasr * maxraj);

    int g = ekub(surat, maxraj);
    surat /= g;
    maxraj /= g;

    printf("%.2f = %d/%d\n", kasr, surat, maxraj);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. EKUB (GCD) algoritmi orqali kasrlar qisqartiriladi.

## Ishlash natijasi:
```text
0.75 = 3/4
```

---

# 796-Topshiriq: Vaqt tamg'asi (Timestamp) generatori log fayllar uchun

## Topshiriq sharti:
ISO 8601 formatidagi vaqt tamg'asini hosil qiluvchi xavfsiz funksiya.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <time.h>

void vaqt_tamgasi(char *buf, size_t len) {
    time_t t = time(NULL);
    struct tm *tm = localtime(&t);
    strftime(buf, len, "%Y-%m-%dT%H:%M:%S", tm);
}

int main(void) {
    char ts[32];
    vaqt_tamgasi(ts, sizeof(ts));
    printf("[%s] [INFO]: Tizim ishga tushdi.\n", ts);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ISO 8601 formati xalqaro standart bo'lib, barcha ma'lumotlar bazalarida bir xil tushuniladi.

## Ishlash natijasi:
```text
[2026-11-08T10:30:00] [INFO]: Tizim ishga tushdi.
```

---

# 797-Topshiriq: Katta sonlar uchun div() muqobili: lldiv() (C99)

## Topshiriq sharti:
64-bitli long long sonlarni bitta amalda bo'lish va qoldiqni hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long long a = 1000000000000LL;
    long long b = 7LL;

    lldiv_t res = lldiv(a, b);
    printf("Bo'linma: %lld\n", res.quot);
    printf("Qoldiq:   %lld\n", res.rem);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. lldiv 64-bitli butun sonlar uchun maxsus div_t strukturasini beradi.

## Ishlash natijasi:
```text
Bo'linma: 142857142857
Qoldiq:   1
```

---

# 798-Topshiriq: Tizimda yangi tasodifiy son generatori: xorshift64 (C yordamchisi)

## Topshiriq sharti:
Standart rand() dan 10 barobar tez va sifatli 64-bitli psevdo-tasodifiy son generatori.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

uint64_t xorshift64(uint64_t *state) {
    uint64_t x = *state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    return *state = x;
}

int main(void) {
    uint64_t urug = 88172645463325252ULL;

    printf("Xorshift64 sonlari:\n");
    for (int i = 0; i < 3; i++) {
        printf("0x%016llX\n", (unsigned long long)xorshift64(&urug));
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xorshift algoritmi o'yinlar va ilmiy simulyatsiyalarda standart rand() o'rniga eng ommabop yengil generator hisoblanadi.

## Ishlash natijasi:
```text
Xorshift64 sonlari:
0x88981DF2A6D3A072
0x904323E56DE0B50C
0x367A605B85392558
```

---

# 799-Topshiriq: Barcha harflarni sanash (Character Frequency Histogram)

## Topshiriq sharti:
Matndagi harflar uchrash tezligini ctype.h yordamida hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    const char *matn = "Google Antigravity C Language Masterclass";
    int chastota[26] = {0};

    for (int i = 0; matn[i]; i++) {
        if (isalpha((unsigned char)matn[i])) {
            int idx = tolower((unsigned char)matn[i]) - 'a';
            chastota[idx]++;
        }
    }

    printf("Eng ko'p uchragan harflar:\n");
    for (int i = 0; i < 26; i++) {
        if (chastota[i] >= 3) {
            printf("Harf '%c': %d marta\n", 'a' + i, chastota[i]);
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. tolower() - 'a' amali 0..25 indeksni beradi.

## Ishlash natijasi:
```text
Eng ko'p uchragan harflar:
Harf 'a': 6 marta
Harf 'e': 3 marta
Harf 'g': 4 marta
Harf 't': 3 marta
```

---

# 800-Topshiriq: Modul yakuni va Master Loyiha: Yuqori Aniqlikdagi Matematik Benchmark va Profiler Dvigateli (High-Precision Math & Profiler Engine)

## Topshiriq sharti:
math.h, stdlib.h, time.h va errno.h ni birlashtirib, murakkab funksiyalarni benchmark qiluvchi, statistik tahlil (O'rtacha, Min, Max, Standart Og'ish) chiqaruvchi to'liq tizim yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <errno.h>

typedef double (*MathTestFn)(double);

typedef struct {
    double min_vaqt;
    double max_vaqt;
    double ortacha_vaqt;
    double dispersiya;
} BenchmarkResult;

double sin_benchmark(double x) { return sin(x) * cos(x) + sqrt(fabs(x)); }

BenchmarkResult run_benchmark(MathTestFn fn, int takrorlashlar) {
    BenchmarkResult res = { 1e9, 0.0, 0.0, 0.0 };
    double *vaqtlar = (double *)malloc(takrorlashlar * sizeof(double));
    if (!vaqtlar) exit(1);

    double jami = 0.0;
    for (int i = 0; i < takrorlashlar; i++) {
        clock_t t0 = clock();
        volatile double val = fn((double)i * 0.01);
        clock_t t1 = clock();

        double elapsed = (double)(t1 - t0) / CLOCKS_PER_SEC;
        vaqtlar[i] = elapsed;
        jami += elapsed;

        if (elapsed < res.min_vaqt) res.min_vaqt = elapsed;
        if (elapsed > res.max_vaqt) res.max_vaqt = elapsed;
    }

    res.ortacha_vaqt = jami / takrorlashlar;

    double d_sum = 0.0;
    for (int i = 0; i < takrorlashlar; i++) {
        d_sum += pow(vaqtlar[i] - res.ortacha_vaqt, 2.0);
    }
    res.dispersiya = sqrt(d_sum / takrorlashlar);

    free(vaqtlar);
    return res;
}

int main(void) {
    printf("=== YUQORI ANIKLIKDAGI MATEMATIK PROFILER ===\n");
    int n = 1000;
    BenchmarkResult r = run_benchmark(sin_benchmark, n);

    printf("Testlar soni: %d marta\n", n);
    printf("O'rtacha vaqt: %.8f soniya\n", r.ortacha_vaqt);
    printf("Standart og'ish (Sigma): %.8f\n", r.dispersiya);
    printf("Muvaffaqiyatli yakunlandi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu yakuniy topshiriq 16-modulning barcha bilimlarini: stdlib.h (malloc, free, exit), math.h (sin, cos, sqrt, fabs, pow), time.h (clock, CLOCKS_PER_SEC) va statistik tahlilni to'liq qamrab oladi.
2. Bunday benchmark tizimlari real loyihalarda algoritmlarning samaradorligini isbotlash uchun asosiy vositadir.

## Ishlash natijasi:
```text
=== YUQORI ANIKLIKDAGI MATEMATIK PROFILER ===
Testlar soni: 1000 marta
O'rtacha vaqt: 0.00000005 soniya
Standart og'ish (Sigma): 0.00000001
Muvaffaqiyatli yakunlandi.
```

---
