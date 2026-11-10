# C Dasturlash Tili — 1-Qism: Asoslar, Tiplar va O'zgaruvchilar
## (1-50 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* Asosiy ma'lumot turlari: int, char, float, double
* Modifikatorlar: short, long, long long, signed, unsigned
* stdint.h va inttypes.h: qat'iy o'lchamli butun sonlar (int8_t, int32_t, int64_t, uintptr_t)
* sizeof operatori va xotira segmentlari (Stack, BSS, Data)
* Format specifiers: %d, %u, %f, %lf, %c, %s, %x, %p, %e, va maydon tekislashlari
* limits.h va float.h doimiylari, aniqlik chegaralari va xotira xavfsizligi

---

# 1-Topshiriq: C tilida 'Salom Dunyo!' dasturi va main funksiyasi

## Topshiriq sharti:
Konsolga 'Salom, Dunyo!' jumlasini chiqaruvchi va 0 qaytaruvchi klassik C dasturini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Salom, Dunyo!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `#include <stdio.h>` — standart kiritish-chiqarish sarlavha faylini ulaydi (printf funksiyasi shu yerda e'lon qilingan).
2. `int main(void)` — C dasturining boshlang'ich nuqtasi bo'lib, operatsion tizim tomonidan chaqiriladi. `void` argument qabul qilmasligini bildiradi.
3. `printf("Salom, Dunyo!\n")` — matnni terminalga chiqaradi, `\n` esa yangi qatorga o'tish belgisidir.
4. `return 0;` — dastur muvaffaqiyatli yakunlanganini operatsion tizimga bildiradi.

## Ishlash natijasi:
```text
Salom, Dunyo!
```

---

# 2-Topshiriq: Standart kiritish va chiqarish (printf formatlash mexanizmi)

## Topshiriq sharti:
Bitta printf chaqiruvi orqali foydalanuvchi ismi va yoshini formatlab chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char ism[] = "Ali";
    int yosh = 20;
    printf("Foydalanuvchi: %s, Yoshi: %d yoshda.\n", ism, yosh);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `printf` funksiyasining birinchi argumenti format satri (format string) hisoblanadi.
2. `%s` formati string (satr) o'rniga `ism` massivining qiymatini joylashtiradi.
3. `%d` formati butun son (decimal integer) o'rniga `yosh` o'zgaruvchisining qiymatini qo'yadi.
4. Parametrlar format satridagi spetsifikatorlar tartibiga mos ravishda uzatiladi.

## Ishlash natijasi:
```text
Foydalanuvchi: Ali, Yoshi: 20 yoshda.
```

---

# 3-Topshiriq: Butun sonli tiplar (int) va asosiy arifmetik amallar

## Topshiriq sharti:
Ikkita butun sonli o'zgaruvchi e'lon qiling, ularning yig'indisi, ayirmasi va ko'paytmasini hisoblab chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son1 = 45;
    int son2 = 15;
    int yigindi = son1 + son2;
    int ayirma = son1 - son2;
    int kopaytma = son1 * son2;

    printf("Sonlar: %d va %d\n", son1, son2);
    printf("Yig'indi: %d\n", yigindi);
    printf("Ayirma: %d\n", ayirma);
    printf("Ko'paytma: %d\n", kopaytma);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int` turi zamonaviy arxitekturalarda 4 bayt (32 bit) xotira egallaydi.
2. Arifmetik amallar natijalari tegishli o'zgaruvchilarga saqlanadi.
3. Natijalar konsolga aniq va formatlangan shaklda chiqariladi.

## Ishlash natijasi:
```text
Sonlar: 45 va 15
Yig'indi: 60
Ayirma: 30
Ko'paytma: 675
```

---

# 4-Topshiriq: Belgilar (char) va ASCII kodlash tizimi

## Topshiriq sharti:
Belgi o'zgaruvchisini e'lon qiling va uning harfiy hamda sonli ASCII kodini birgalikda ekranga chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char belgi = 'Z';
    printf("Belgi: %c\n", belgi);
    printf("ASCII kodi (o'nlikda): %d\n", belgi);
    printf("ASCII kodi (o'n oltilikda): 0x%X\n", belgi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida `char` turi 1 bayt (8 bit) xotira egallaydi va aslida kichik butun son hisoblanadi.
2. `%c` spetsifikatori sonni unga mos ASCII belgisi sifatida chop etadi.
3. `%d` spetsifikatori ayni shu xotira baytidagi sonli qiymatni o'nlik tizimda chiqaradi.
4. `%X` esa katta harfli o'n oltilik tizimda namoyish etadi ('Z' = 90 = 0x5A).

## Ishlash natijasi:
```text
Belgi: Z
ASCII kodi (o'nlikda): 90
ASCII kodi (o'n oltilikda): 0x5A
```

---

# 5-Topshiriq: Haqiqiy sonlar (float va double) va aniqlik darajasi

## Topshiriq sharti:
float va double turlarida pi sonini e'lon qilib, ularni 7 xona va 15 xona aniqlikda chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    float pi_float = 3.14159265358979323846f;
    double pi_double = 3.14159265358979323846;

    printf("Float (7 xona): %.7f\n", pi_float);
    printf("Double (15 xona): %.15lf\n", pi_double);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `float` — bir karrali aniqlikdagi suzuvchi nuqtali son (4 bayt, IEEE 754 bo'yicha ~7 ta aniq raqam).
2. `double` — ikki karrali aniqlikdagi suzuvchi nuqtali son (8 bayt, ~15-17 ta aniq raqam).
3. `f` suffiksi sonning float literal ekanligini belgilaydi.
4. Format satridagi `%.7f` va `%.15lf` nuqtadan keyin necha xona chiqarish kerakligini boshqaradi.

## Ishlash natijasi:
```text
Float (7 xona): 3.1415927
Double (15 xona): 3.141592653589793
```

---

# 6-Topshiriq: O'zgaruvchilarni e'lon qilish va initsializatsiya turlari

## Topshiriq sharti:
O'zgaruvchilarni bir vaqtning o'zida e'lon qilish, nolga tenglashtirish va keyin qiymat berish usullarini namoyish eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 10, b = 20, c = 30; // Bir qatorda initsializatsiya
    int d;                       // E'lon qilish
    d = a + b + c;               // Keyin qiymat berish

    printf("a = %d, b = %d, c = %d, d = %d\n", a, b, c, d);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bir xil turdagi bir nechta o'zgaruvchilarni vergul bilan ajratib bitta qatorda e'lon qilish mumkin.
2. O'zgaruvchini e'lon qilishda boshlang'ich qiymat berish (initsializatsiya) axlat qiymatlardan (garbage values) saqlaydi.
3. `d` o'zgaruvchisiga ifoda hisoblangach qiymat berildi.

## Ishlash natijasi:
```text
a = 10, b = 20, c = 30, d = 60
```

---

# 7-Topshiriq: const kalit so'zi va o'zgarmas kattaliklar

## Topshiriq sharti:
const o'zgaruvchi e'lon qiling, doira yuzini hisoblang va o'zgarmaslik mohiyatini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    const double PI = 3.1415926535;
    double radius = 4.0;
    double yuza = PI * radius * radius;

    printf("Radius: %.2f\n", radius);
    printf("Doira yuzi: %.4f\n", yuza);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const` kalit so'zi o'zgaruvchini faqat o'qish uchun (read-only) qilib belgilaydi.
2. Agar `PI = 3.14;` deb qiymatni o'zgartirishga urinsak, C kompilyatori xatolik (assignment of read-only variable) qaytaradi.
3. Bu xavfsiz kod yozish va dastur parametrlarini himoyalashning eng yaxshi usullaridan biridir.

## Ishlash natijasi:
```text
Radius: 4.00
Doira yuzi: 50.2655
```

---

# 8-Topshiriq: #define preprotsessor makrosi orqali konstantalar belgilash

## Topshiriq sharti:
#define orqali yorug'lik tezligi va Plank doimiysini aniqlab, energiyani hisoblang (E = h * nu).

## Yechim (C kodi):
```c
#include <stdio.h>

#define YORUGLIK_TEZLIGI 299792458.0 // m/s
#define PLANK_DOIMIYSI 6.626e-34     // J*s

int main(void) {
    double chastota = 5.0e14; // Gerts
    double energiya = PLANK_DOIMIYSI * chastota;

    printf("Chastota: %.1e Hz\n", chastota);
    printf("Foton energiyasi: %.3e J\n", energiya);
    printf("Yorug'lik tezligi: %.0f m/s\n", YORUGLIK_TEZLIGI);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `#define` preprotsessor direktivasi bo'lib, kompilyatsiyadan oldin matn almashtirishni bajaradi.
2. Preprotsessor doimiylari xotiradan joy olmaydi, ular kod ichiga to'g'ridan-to'g'ri qiymat sifatida qo'yiladi.
3. `%e` ilmiy (eksponensial) ko'rinishda chop etish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Chastota: 5.0e+14 Hz
Foton energiyasi: 3.313e-19 J
Yorug'lik tezligi: 299792458 m/s
```

---

# 9-Topshiriq: sizeof operatori va asosiy ma'lumot turlari hajmi

## Topshiriq sharti:
C tilining barcha standart asosiy turlarining xotiradagi hajmini sizeof yordamida aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("char hajmi: %zu bayt\n", sizeof(char));
    printf("short hajmi: %zu bayt\n", sizeof(short));
    printf("int hajmi: %zu bayt\n", sizeof(int));
    printf("long hajmi: %zu bayt\n", sizeof(long));
    printf("long long hajmi: %zu bayt\n", sizeof(long long));
    printf("float hajmi: %zu bayt\n", sizeof(float));
    printf("double hajmi: %zu bayt\n", sizeof(double));
    printf("long double hajmi: %zu bayt\n", sizeof(long double));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `sizeof` bu funksiya emas, balki kompilyatsiya vaqtida hisoblanadigan C operatoridir.
2. Uning qaytaradigan qiymati `size_t` tipida bo'ladi va uni chop etish uchun `%zu` spetsifikatori ishlatiladi.
3. Zamonaviy 64-bitli tizimlarda: char=1, short=2, int=4, long=4 yoki 8, long long=8, float=4, double=8 baytdir.

## Ishlash natijasi:
```text
char hajmi: 1 bayt
short hajmi: 2 bayt
int hajmi: 4 bayt
long hajmi: 4 bayt
long long hajmi: 8 bayt
float hajmi: 4 bayt
double hajmi: 8 bayt
long double hajmi: 16 bayt
```

---

# 10-Topshiriq: short int modifikatori va xotira tejamkorligi

## Topshiriq sharti:
short int turidan foydalanib kichik diapazondagi qiymatlarni saqlang va %hd formati orqali chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    short int harorat = -15;
    unsigned short port = 8080;

    printf("Harorat: %hd daraja C\n", harorat);
    printf("Server porti: %hu\n", port);
    printf("short xotira hajmi: %zu bayt\n", sizeof(harorat));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `short int` (yoki oddiygina `short`) 2 bayt (16 bit) joy egallaydi.
2. `signed short` diapazoni: -32,768 dan +32,767 gacha.
3. `unsigned short` diapazoni: 0 dan 65,535 gacha.
4. Chop etishda signed uchun `%hd`, unsigned uchun `%hu` qo'llaniladi.

## Ishlash natijasi:
```text
Harorat: -15 daraja C
Server porti: 8080
short xotira hajmi: 2 bayt
```

---

# 11-Topshiriq: long int va long long int modifikatorlari

## Topshiriq sharti:
Katta sonlar uchun long long int turidan foydalanib hisoblash bajaring va %lld orqali chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    long long int yer_aholisi = 8100000000LL;
    unsigned long long int yulduzlar_soni = 10000000000000000000ULL;

    printf("Yer aholisi taxminan: %lld kishi\n", yer_aholisi);
    printf("Koinotdagi yulduzlar: %llu ta\n", yulduzlar_soni);
    printf("long long hajmi: %zu bayt\n", sizeof(long long int));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `long long int` kamida 64 bit (8 bayt) xotira egallashini C99 standarti kafolatlaydi.
2. `LL` va `ULL` suffikslari butun son literallarini mos ravishda signed va unsigned 64-bit sifatida aniqlaydi.
3. `%lld` va `%llu` format spetsifikatorlari 64-bitli sonlarni xatolarsiz chop etish uchun kerak.

## Ishlash natijasi:
```text
Yer aholisi taxminan: 8100000000 kishi
Koinotdagi yulduzlar: 10000000000000000000 ta
long long hajmi: 8 bayt
```

---

# 12-Topshiriq: signed va unsigned modifikatorlari farqi

## Topshiriq sharti:
Bir xil bit naqshiga ega bo'lgan signed char va unsigned char qiymatlarini solishtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    signed char s_son = -1;
    unsigned char u_son = 255;

    printf("signed char %%d sifatida: %d\n", s_son);
    printf("unsigned char %%d sifatida: %d\n", u_son);
    printf("Ikkalasining bayt xotirasi (Hex): 0x%02X va 0x%02X\n", (unsigned char)s_son, u_son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Xotirada ikkala o'zgaruvchi ham `0xFF` (11111111 ikkilik) qiymatiga ega.
2. `signed char` eng yuqori bitni (MSB) ishora biti (sign bit) sifatida qaraydi: Two's complement bo'yicha bu -1.
3. `unsigned char` eng yuqori bitni ham qiymat biti sifatida o'qiydi: 2^7 + ... + 2^0 = 255.

## Ishlash natijasi:
```text
signed char %d sifatida: -1
unsigned char %d sifatida: 255
Ikkalasining bayt xotirasi (Hex): 0xFF va 0xFF
```

---

# 13-Topshiriq: unsigned int chegarasidan oshish (Overflow / Wrap-around) xususiyati

## Topshiriq sharti:
unsigned int o'zgaruvchisini maksimal qiymatiga yetkazib, unga 1 qo'shganda nolga qaytishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    unsigned char max_bayt = 255;
    printf("Boshlang'ich qiymat: %u\n", max_bayt);

    max_bayt = max_bayt + 1;
    printf("1 qo'shilgandan so'ng (wrap-around): %u\n", max_bayt);

    max_bayt = max_bayt - 1;
    printf("Qayta 1 ayrilgandan so'ng (underflow): %u\n", max_bayt);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C standartida `unsigned` sonlarning chegaradan oshishi aniq belgilangan (Well-defined modulo 2^N behavior).
2. 255 ga 1 qo'shilganda 256 bo'ladi, lekin 8-bitda faqat pastki 8 bit saqlanadi (256 mod 256 = 0).
3. Bu hodisa 'wrap-around' (aylanib boshiga qaytish) deb ataladi. E'tibor bering: `signed` overflow esa Undefined Behavior (UB) hisoblanadi!

## Ishlash natijasi:
```text
Boshlang'ich qiymat: 255
1 qo'shilgandan so'ng (wrap-around): 0
Qayta 1 ayrilgandan so'ng (underflow): 255
```

---

# 14-Topshiriq: stdint.h: int8_t va uint8_t aniq o'lchamli turlari

## Topshiriq sharti:
stdint.h kutubxonasidan int8_t va uint8_t turlarini chaqirib, ularning xotira hajmi va qiymatlarini chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    int8_t a = -128;
    uint8_t b = 250;

    printf("int8_t: %d (hajmi: %zu bayt)\n", a, sizeof(a));
    printf("uint8_t: %u (hajmi: %zu bayt)\n", b, sizeof(b));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C99 standartida kiritilgan `<stdint.h>` har qanday platformada aniq bir xil bit soniga ega bo'lgan turlarni beradi.
2. `int8_t` har doim aynan 8 bit (1 bayt) signed bo'ladi (-128 dan 127 gacha).
3. `uint8_t` har doim aynan 8 bit unsigned bo'ladi (0 dan 255 gacha).
4. Bu turlar mikrokontrollerlar va tarmoq protokollarida xotira aniqligi uchun o'ta muhim.

## Ishlash natijasi:
```text
int8_t: -128 (hajmi: 1 bayt)
uint8_t: 250 (hajmi: 1 bayt)
```

---

# 15-Topshiriq: stdint.h: int16_t va uint16_t turlari bilan ishlash

## Topshiriq sharti:
16-bitli audio namuna (sample) qiymatini int16_t yordamida modellashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    int16_t audio_sample = -32000;
    uint16_t datchik_kodi = 65000;

    printf("Audio namuna: %d\n", audio_sample);
    printf("Datchik kodi: %u\n", datchik_kodi);
    printf("int16_t hajmi: %zu bayt\n", sizeof(int16_t));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int16_t` aniq 16 bit (2 bayt) bo'lib, audio signallari (masalan, 16-bit PCM WAV) formatida standart hisoblanadi.
2. `uint16_t` esa 0 dan 65535 gacha bo'lgan apparat datchiklari ma'lumotlarini qabul qilishda ishlatiladi.

## Ishlash natijasi:
```text
Audio namuna: -32000
Datchik kodi: 65000
int16_t hajmi: 2 bayt
```

---

# 16-Topshiriq: stdint.h: int32_t va uint32_t turlari

## Topshiriq sharti:
32-bitli IPv4 manzilini uint32_t orqali ifodalang va uni butun son hamda hex formatida chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint32_t ip_manzil = 0x7F000001; // 127.0.0.1 (Localhost)
    int32_t balans = -1500000;

    printf("IP (Hex): 0x%08X\n", ip_manzil);
    printf("IP (O'nlikda): %u\n", ip_manzil);
    printf("Balans: %d\n", balans);
    printf("int32_t hajmi: %zu bayt\n", sizeof(int32_t));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `int32_t` va `uint32_t` aniq 4 bayt (32 bit) kenglikni kafolatlaydi.
2. IPv4 manzili 32 bit bo'lib, uni bitta `uint32_t` ga to'liq joylashtirish mumkin.
3. `%08X` formati 8 xonali o'n oltilik son ko'rinishida, yetishmagan xonalarni 0 bilan to'ldirib chiqaradi.

## Ishlash natijasi:
```text
IP (Hex): 0x7F000001
IP (O'nlikda): 2130706433
Balans: -1500000
int32_t hajmi: 4 bayt
```

---

# 17-Topshiriq: stdint.h: int64_t va uint64_t katta ma'lumotlar uchun

## Topshiriq sharti:
Katta hajmdagi baytlar (masalan 1 Terabayt) sonini uint64_t da saqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

int main(void) {
    uint64_t terabayt = 1024ULL * 1024ULL * 1024ULL * 1024ULL;
    int64_t nanosekundlar = 5000000000LL;

    printf("1 Terabayt: %" PRIu64 " bayt\n", terabayt);
    printf("Nanosekundlar: %" PRId64 " ns\n", nanosekundlar);
    printf("uint64_t hajmi: %zu bayt\n", sizeof(uint64_t));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `uint64_t` 8 bayt (64 bit) xotira oladi va 18 kvintilliongacha sonlarni saqlay oladi.
2. `<inttypes.h>` sarlavha faylidagi `PRIu64` va `PRId64` makroslari platformadan qat'i nazar to'g'ri format spetsifikatorini tanlaydi.
3. Bu 32-bit va 64-bit kompilyatorlar o'rtasida ko'chuvchan (portable) kod yozish kafolatidir.

## Ishlash natijasi:
```text
1 Terabayt: 1099511627776 bayt
Nanosekundlar: 5000000000 ns
uint64_t hajmi: 8 bayt
```

---

# 18-Topshiriq: stdint.h: intptr_t va uintptr_t — pointerlarni butun son sifatida saqlash

## Topshiriq sharti:
O'zgaruvchining manzilini uintptr_t o'zgaruvchisiga o'zlashtiring va xavfsiz sonli konvertatsiyani ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    int qiymat = 999;
    int *ptr = &qiymat;
    uintptr_t manzil_son = (uintptr_t)ptr;

    printf("Pointer asl ko'rinishda: %p\n", (void*)ptr);
    printf("uintptr_t orqali (Hex): 0x%lx\n", (unsigned long)manzil_son);
    printf("uintptr_t hajmi: %zu bayt, pointer hajmi: %zu bayt\n", 
           sizeof(uintptr_t), sizeof(ptr));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `uintptr_t` — joriy arxitekturadagi ixtiyoriy ko'rsatkichni (pointer) hech qanday ma'lumot yo'qotmasdan saqlashga qodir bo'lgan butun son turidir.
2. 32-bitli tizimda uning hajmi 4 bayt, 64-bitli tizimda esa 8 bayt bo'ladi.
3. Oddiy `int` ga pointerni o'girish xavfli, chunki 64-bitda `int` (4 bayt) pointerning (8 bayt) yuqori qismini qirqib yuboradi.

## Ishlash natijasi:
```text
Pointer asl ko'rinishda: 000000000012FFE4
uintptr_t orqali (Hex): 0x12ffe4
uintptr_t hajmi: 8 bayt, pointer hajmi: 8 bayt
```

---

# 19-Topshiriq: stdbool.h: bool, true va false mantiqiy turlari

## Topshiriq sharti:
C99 stdbool.h kutubxonasidan foydalanib mantiqiy bayroq (flag) holatini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    bool tizim_faol = true;
    bool xatolik_bormi = false;

    printf("Tizim faol: %d\n", tizim_faol);
    printf("Xatolik bormi: %d\n", xatolik_bormi);
    printf("bool turi hajmi: %zu bayt\n", sizeof(bool));

    if (tizim_faol && !xatolik_bormi) {
        printf("Tizim barqaror ishlamoqda!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Klassik C89 da `bool` turi yo'q edi (0 yolg'on, 0 dan farqli har qanday son rost hisoblangan).
2. C99 standarti `<stdbool.h>` orqali `bool`, `true` (1) va `false` (0) ni rasmiylashtirdi.
3. `sizeof(bool)` odatda 1 bayt xotira oladi.

## Ishlash natijasi:
```text
Tizim faol: 1
Xatolik bormi: 0
bool turi hajmi: 1 bayt
Tizim barqaror ishlamoqda!
```

---

# 20-Topshiriq: char turi bilan arifmetik amallar va harf registrini almashtirish

## Topshiriq sharti:
Kichik harfni ASCII arifmetikasi yordamida katta harfga o'tkazing ('a' -> 'A').

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char kichik_harf = 'm';
    // ASCII da 'a' va 'A' orasidagi farq 32 ga teng ('a' - 'A' = 32)
    char katta_harf = kichik_harf - ('a' - 'A');

    printf("Kichik harf: %c (ASCII: %d)\n", kichik_harf, kichik_harf);
    printf("Katta harf: %c (ASCII: %d)\n", katta_harf, katta_harf);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ASCII jadvalida lotin 'a' harfi 97, 'A' esa 65 kodi bilan ifodalanadi.
2. Harflar o'rtasidagi siljish (`'a' - 'A'`) aynan 32 ga teng bo'lib, bu 5-bitning holati bilan bog'liq.
3. Kichik harfdan 32 ayirilsa, uning katta ko'rinishi hosil bo'ladi.

## Ishlash natijasi:
```text
Kichik harf: m (ASCII: 109)
Katta harf: M (ASCII: 77)
```

---

# 21-Topshiriq: Escape sequences (Maxsus boshqaruv belgilari)

## Topshiriq sharti:
Tabulyatsiya, qo'shtirnoq, teskari slesh va yangi qator belgilarini ekranga chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Qator 1:\tIsm\tFamiliya\n");
    printf("Qator 2:\tAli\tValiyev\n");
    printf("Fayl yo'li: C:\\tizim\\dastur.exe\n");
    printf("U dediki: \"C tili juda tezkor!\"\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `\t` (tab) matnni ustunlar bo'yicha tekislash uchun gorizontal bo'shliq qo'shadi.
2. `\\` bitta teskari slesh belgisini chiqarish uchun ishlatiladi (chunki yolg'iz `\` maxsus belgi hisoblanadi).
3. `\"` satr ichida qo'shtirnoq belgisini aks ettirish imkonini beradi.
4. `\n` kursor keyingi qator boshiga o'tishini ta'minlaydi.

## Ishlash natijasi:
```text
Qator 1:	Ism	Familiya
Qator 2:	Ali	Valiyev
Fayl yo'li: C:\tizim\dastur.exe
U dediki: "C tili juda tezkor!"
```

---

# 22-Topshiriq: Format specifier: O'n oltilik (Hexadecimal: %x, %X) sanoq sistemasi

## Topshiriq sharti:
Sonni o'nlik tizimdan kichik va katta harfli o'n oltilik shaklda chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 305419896; // 0x12345678

    printf("O'nlikda: %d\n", son);
    printf("O'n oltilikda (kichik): %x\n", son);
    printf("O'n oltilikda (katta): %X\n", son);
    printf("Prefiks bilan (#): %#X\n", son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `%x` o'n oltilik raqamlarni kichik harflar bilan (`a-f`), `%X` esa katta harflar bilan (`A-F`) chiqaradi.
2. `%#X` formatidagi `#` bayrog'i son oldiga avtomatik ravishda `0X` prefiksini qo'shadi.
3. Bu apparat darajasida baytlarni tahlil qilishda qulaylik yaratadi.

## Ishlash natijasi:
```text
O'nlikda: 305419896
O'n oltilikda (kichik): 12345678
O'n oltilikda (katta): 12345678
Prefiks bilan (#): 0X12345678
```

---

# 23-Topshiriq: Format specifier: Sakkizlik (Octal: %o) sanoq sistemasi

## Topshiriq sharti:
Fayl ruxsat huquqlarini (Linux chmod: 755) sakkizlik sanoq sistemasida chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int ruxsat = 0755; // 0 prefiksi C da sakkizlik literalni bildiradi

    printf("Sakkizlikda: %o\n", ruxsat);
    printf("Prefiks bilan: %#o\n", ruxsat);
    printf("O'nlikdagi qiymati: %d\n", ruxsat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida 0 raqami bilan boshlangan butun sonlar (masalan `0755`) sakkizlik (octal) literal hisoblanadi.
2. `%o` spetsifikatori sonni sakkizlik tizimda chop etadi.
3. `%#o` son oldiga `0` prefiksini qo'shib chiqaradi.

## Ishlash natijasi:
```text
Sakkizlikda: 755
Prefiks bilan: 0755
O'nlikdagi qiymati: 493
```

---

# 24-Topshiriq: Format specifier: Ko'rsatkich manzili (%p) bilan xotirani ko'rish

## Topshiriq sharti:
Stackdagi uchta ketma-ket butun son o'zgaruvchisining xotira manzillarini chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 10;
    int b = 20;
    int c = 30;

    printf("a manzili: %p\n", (void*)&a);
    printf("b manzili: %p\n", (void*)&b);
    printf("c manzili: %p\n", (void*)&c);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `&` operatori o'zgaruvchining operativ xotiradagi virtual manzilini oladi.
2. `%p` ko'rsatkichlar (pointer) manzillarini chop etish uchun maxsus spetsifikator bo'lib, unga argument `(void*)` ga o'girilib berilishi lozim.
3. Manzillar farqi `int` tipi 4 bayt ekanligini xotiradagi siljish orqali ko'rsatadi.

## Ishlash natijasi:
```text
a manzili: 000000000012FFE4
b manzili: 000000000012FFE0
c manzili: 000000000012FFDC
```

---

# 25-Topshiriq: Format specifier: Eksponensial ilmiy shakl (%e va %E)

## Topshiriq sharti:
Juda kichik (Avogadro, elektron zaryadi) va katta sonlarni ilmiy shaklda chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double elektron_zaryadi = 1.602176634e-19;
    double avogadro = 6.02214076e23;

    printf("Elektron zaryadi: %e C\n", elektron_zaryadi);
    printf("Avogadro soni: %E mol^-1\n", avogadro);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `%e` kichik 'e' bilan eksponensial formatda (masalan `1.602177e-19`), `%E` esa katta 'E' bilan chop etadi.
2. Bu juda katta yoki juda kichik sonlarni ixcham va xatolarsiz ko'rsatish imkonini beradi.

## Ishlash natijasi:
```text
Elektron zaryadi: 1.602177e-19 C
Avogadro soni: 6.022141E+23 mol^-1
```

---

# 26-Topshiriq: Format specifier: Maydon kengligini belgilash (%5d) orqali ustun hosil qilish

## Topshiriq sharti:
Sonlarni o'ng tomonga tekislab, 6 xonali ustun ko'rinishida chop etuvchi dastur tuzing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 7, b = 84, c = 1290, d = 45000;

    printf("|%6d|\n", a);
    printf("|%6d|\n", b);
    printf("|%6d|\n", c);
    printf("|%6d|\n", d);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `%6d` ifodasi son uchun kamida 6 ta pozitsiya (belgi kengligi) ajratilishini bildiradi.
2. Standart holatda son o'ng tomonga tekislanadi va chapdan bo'sh joylar (probellar) qo'yiladi.
3. Bu usul jadvallar va hisobotlarni chiroyli ko'rsatishda juda qulaydir.

## Ishlash natijasi:
```text
|     7|
|    84|
|  1290|
| 45000|
```

---

# 27-Topshiriq: Format specifier: Chapga tekislash minus (-) bayrog'i bilan

## Topshiriq sharti:
Matn va sonlarni chap tomonga tekislab (%-10s, %-6d) jadval hosil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("%-10s %-8s %-6s\n", "Mahsulot", "Miqdor", "Narx");
    printf("%-10s %-8d %-6d\n", "Olma", 15, 12000);
    printf("%-10s %-8d %-6d\n", "Nok", 8, 25000);
    printf("%-10s %-8d %-6d\n", "Anor", 24, 18000);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Maydon kengligi oldiga qo'yilgan minus belgisi (`-`) qiymatni chap tomonga tekislashni bildiradi.
2. `%-10s` 10 ta belgi ajratib, satrni chapdan yozadi, qolgan qismiga o'ngdan probellar qo'shadi.

## Ishlash natijasi:
```text
Mahsulot   Miqdor   Narx  
Olma       15       12000 
Nok        8        25000 
Anor       24       18000
```

---

# 28-Topshiriq: Format specifier: Nollar bilan to'ldirish (Zero-padding: %06d)

## Topshiriq sharti:
Vaqt yoki seriya raqamlarini yetishmagan xonalari oldiga nollar qo'yib chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int soat = 9;
    int minut = 5;
    int sekund = 7;
    int id = 42;

    printf("Vaqt: %02d:%02d:%02d\n", soat, minut, sekund);
    printf("Buyurtma ID: #%06d\n", id);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `%02d` kamida 2 xona ajratadi, agar son 1 xonali bo'lsa, oldiga bo'shliq o'rniga 0 qo'yadi.
2. `%06d` esa 6 xonali qilib to'ldiradi (masalan 42 -> 000042).
3. Bu vaqt (09:05:07) va hisob-faktura raqamlarini standartlashtirishda qo'llaniladi.

## Ishlash natijasi:
```text
Vaqt: 09:05:07
Buyurtma ID: #000042
```

---

# 29-Topshiriq: Haqiqiy sonlarda aniqlik darajasi (%.2f va %.4lf)

## Topshiriq sharti:
Valyuta summasini ikki xona va ilmiy koeffitsientni to'rt xona aniqlikda chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double narx = 199.9876;
    double foiz = 0.052345;

    printf("Narx: %.2f USD\n", narx);
    printf("Koeffitsient: %.4lf\n", foiz);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `.` dan keyingi raqam kasr qismidan necha xona qoldirilishini belgilaydi.
2. 199.9876 soni `%.2f` bilan chop etilganda avtomatik yaxlitlanib 199.99 ko'rinishiga keladi.
3. `%.4lf` esa to'rtinchi xonagacha aniq chiqaradi.

## Ishlash natijasi:
```text
Narx: 199.99 USD
Koeffitsient: 0.0523
```

---

# 30-Topshiriq: Format specifier: Dinamik kenglik va aniqlik (* belgisi bilan: %*.*f)

## Topshiriq sharti:
Kenglik va kasr qismi aniqligini o'zgaruvchilar orqali dinamik uzating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double qiymat = 12.3456789;
    int kenglik = 10;
    int aniqlik = 3;

    printf("[%*.*f]\n", kenglik, aniqlik, qiymat);

    kenglik = 12;
    aniqlik = 5;
    printf("[%*.*f]\n", kenglik, aniqlik, qiymat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Format satrida son o'rniga `*` yulduzcha qo'yilsa, `printf` uning qiymatini parametrlar ro'yxatidan kutadi.
2. `%*.*f` da birinchi argument kenglik, ikkinchi argument aniqlik, uchinchisi esa sonning o'zidir.
3. Bu usul dastur davomida jadval o'lchamlarini moslashtirish imkonini beradi.

## Ishlash natijasi:
```text
[    12.346]
[    12.34568]
```

---

# 31-Topshiriq: Implicit type conversion (Avtomatik tur o'zgartirish qoidalari)

## Topshiriq sharti:
int va double ishtirokidagi amalda kichik tur katta turga qanday aylanishini namoyish eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int butun = 5;
    double haqiqiy = 2.5;

    // 'butun' avtomatik ravishda double ga keltiriladi
    double natija = butun + haqiqiy;

    printf("Natija: %.2f\n", natija);
    printf("Natija hajmi: %zu bayt\n", sizeof(butun + haqiqiy));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da turli turlar qatnashgan amallarda 'Type Promotion' (turni ko'tarish) sodir bo'ladi.
2. Kichikroq va torroq tur (int) kattaroq va aniqroq turga (double) avtomatik o'zgartiriladi.
3. Natijada `sizeof(butun + haqiqiy)` ifodasi `sizeof(double)` ga teng bo'lib, 8 bayt chiqadi.

## Ishlash natijasi:
```text
Natija: 7.50
Natija hajmi: 8 bayt
```

---

# 32-Topshiriq: Explicit type casting (Majburiy tur konvertatsiyasi)

## Topshiriq sharti:
Ikki butun son bo'linishida majburiy casting qilib, kasr qismini saqlab qoling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int jami_ball = 95;
    int fanlar_soni = 4;

    // Butun sonli bo'linish (95 / 4 = 23)
    double notogri_orta = jami_ball / fanlar_soni;

    // Majburiy cast (95.0 / 4 = 23.75)
    double togri_orta = (double)jami_ball / fanlar_soni;

    printf("Noto'g'ri o'rtacha: %.2f\n", notogri_orta);
    printf("To'g'ri o'rtacha: %.2f\n", togri_orta);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida ikkita `int` o'zaro bo'linganda natija har doim butun son bo'ladi va kasr qismi tashlab yuboriladi (truncated).
2. `(double)jami_ball` ifodasi uning qiymatini vaqtincha double ga aylantiradi.
3. Shundan so'ng qoida bo'yicha `double / int` amali bajarilib, to'g'ri kasrli natija (23.75) hosil bo'ladi.

## Ishlash natijasi:
```text
Noto'g'ri o'rtacha: 23.00
To'g'ri o'rtacha: 23.75
```

---

# 33-Topshiriq: Butun sonli bo'linish va qoldiq olish (%) amali mohiyati

## Topshiriq sharti:
Daqiqalarni soat va qoldiq daqiqalarga ajratuvchi dastur tuzing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int umumiy_daqiqa = 135;
    int soat = umumiy_daqiqa / 60;
    int daqiqa = umumiy_daqiqa % 60;

    printf("%d daqiqa = %d soat va %d daqiqa\n", umumiy_daqiqa, soat, daqiqa);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `/` operatori butun sonlarda bo'linmaning faqat butun qismini oladi (135 / 60 = 2).
2. `%` (modulo) operatori esa faqat butun sonlar uchun ishlaydi va bo'lishdan qolgan qoldiqni qaytaradi (135 % 60 = 15).
3. Bu vaqt, masofa va pul birliklarini maydalashda eng asosiy vositadir.

## Ishlash natijasi:
```text
135 daqiqa = 2 soat va 15 daqiqa
```

---

# 34-Topshiriq: limits.h kutubxonasi: INT_MAX va INT_MIN qiymatlari

## Topshiriq sharti:
limits.h dan foydalanib int turining minimal va maksimal qiymatlarini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <limits.h>

int main(void) {
    printf("int o'lchami: %zu bayt\n", sizeof(int));
    printf("Minimal int: %d\n", INT_MIN);
    printf("Maksimal int: %d\n", INT_MAX);
    printf("Maksimal unsigned int: %u\n", UINT_MAX);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `<limits.h>` sarlavha fayli arxitekturaga xos butun sonli turlarning chegaralarini aniq makroslar orqali taqdim etadi.
2. 32-bitli signed int uchun: INT_MIN = -2,147,483,648 va INT_MAX = 2,147,483,647.
3. UINT_MAX esa 4,294,967,295 ga teng.

## Ishlash natijasi:
```text
int o'lchami: 4 bayt
Minimal int: -2147483648
Maksimal int: 2147483647
Maksimal unsigned int: 4294967295
```

---

# 35-Topshiriq: limits.h kutubxonasi: CHAR_BIT, CHAR_MIN va CHAR_MAX

## Topshiriq sharti:
Bitta baytdagi bitlar sonini (CHAR_BIT) va char chegaralarini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <limits.h>

int main(void) {
    printf("Bitta baytdagi bitlar soni: %d\n", CHAR_BIT);
    printf("CHAR_MIN: %d\n", CHAR_MIN);
    printf("CHAR_MAX: %d\n", CHAR_MAX);
    printf("UCHAR_MAX: %d\n", UCHAR_MAX);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `CHAR_BIT` har doim standart arxitekturalarda 8 ga teng bo'ladi (kamdan-kam DSP larda farq qilishi mumkin).
2. Platformaga qarab `char` standart holatda signed yoki unsigned bo'lishi mumkin.
3. `UCHAR_MAX` esa har doim 255 ga teng.

## Ishlash natijasi:
```text
Bitta baytdagi bitlar soni: 8
CHAR_MIN: -128
CHAR_MAX: 127
UCHAR_MAX: 255
```

---

# 36-Topshiriq: limits.h kutubxonasi: LLONG_MAX va ULLONG_MAX

## Topshiriq sharti:
64-bitli butun sonlarning maksimal chegaralarini ekranga chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <limits.h>

int main(void) {
    printf("LLONG_MIN: %lld\n", LLONG_MIN);
    printf("LLONG_MAX: %lld\n", LLONG_MAX);
    printf("ULLONG_MAX: %llu\n", ULLONG_MAX);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `LLONG_MAX` 2^63 - 1 ga teng (9 kvintilliondan ortiq).
2. `ULLONG_MAX` 2^64 - 1 ga teng (18 kvintilliondan ortiq).
3. Bu chegaralar katta hajmdagi xotira yoki vaqt hisob-kitoblarida to'lib ketishning oldini olish uchun tekshiriladi.

## Ishlash natijasi:
```text
LLONG_MIN: -9223372036854775808
LLONG_MAX: 9223372036854775807
ULLONG_MAX: 18446744073709551615
```

---

# 37-Topshiriq: float.h kutubxonasi: FLT_MAX, FLT_MIN va FLT_EPSILON

## Topshiriq sharti:
float turining minimal ijobiy qiymati, maksimal qiymati va epsilonini chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <float.h>

int main(void) {
    printf("FLT_MIN (eng kichik musbat): %e\n", FLT_MIN);
    printf("FLT_MAX (eng katta musbat): %e\n", FLT_MAX);
    printf("FLT_EPSILON: %e\n", FLT_EPSILON);
    printf("DBL_EPSILON: %e\n", DBL_EPSILON);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `FLT_MIN` — normallashtirilgan eng kichik musbat float son (~1.17e-38).
2. `FLT_MAX` — eng katta ko'rsatilishi mumkin bo'lgan float son (~3.40e+38).
3. `FLT_EPSILON` — 1.0 ga qo'shilganda 1.0 dan farq qiladigan eng kichik musbat son (mashina aniqligi chegarasi).

## Ishlash natijasi:
```text
FLT_MIN (eng kichik musbat): 1.175494e-38
FLT_MAX (eng katta musbat): 3.402823e+38
FLT_EPSILON: 1.192093e-07
DBL_EPSILON: 2.220446e-16
```

---

# 38-Topshiriq: Suzuvchi nuqtali sonlarda aniqlik yo'qolishi (0.1 + 0.2 muammosi)

## Topshiriq sharti:
0.1 va 0.2 yig'indisi 0.3 ga teng yoki teng emasligini tahlil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double a = 0.1;
    double b = 0.2;
    double c = a + b;

    printf("a + b = %.17f\n", c);
    printf("0.3   = %.17f\n", 0.3);

    if (c == 0.3) {
        printf("Teng!\n");
    } else {
        printf("Teng emas! (Suzuvchi nuqta aniqligi tufayli)\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ikkilik tizimda (IEEE 754) 0.1 va 0.2 sonlari cheksiz davriy kasr bo'lib qoladi va aniq ifodalanmaydi.
2. 0.1 + 0.2 natijasi aslida 0.3000000000000000444... bo'ladi.
3. Shuning uchun haqiqiy sonlarni to'g'ridan-to'g'ri `==` bilan taqqoslash xavfli; ularning ayirmasi epsilon dan kichikligi tekshirilishi kerak: `fabs(c - 0.3) < 1e-9`.

## Ishlash natijasi:
```text
a + b = 0.30000000000000004
0.3   = 0.29999999999999999
Teng emas! (Suzuvchi nuqta aniqligi tufayli)
```

---

# 39-Topshiriq: scanf() orqali bitta butun son o'qish va manzil operatori (&)

## Topshiriq sharti:
Konsoldan son o'qish mexanizmini va & operatori nima uchun kerakligini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int yosh;
    printf("Yoshingizni kiriting: ");
    // scanf manzil qabul qiladi, shuning uchun &yosh yoziladi
    // Ushbu amaliy dasturda simulyatsiya uchun 21 qiymati berilgan deb qaraymiz
    yosh = 21;
    printf("Qabul qilingan yosh: %d\n", yosh);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `scanf("%d", &yosh)` funksiyasi o'zgaruvchining qiymatini emas, uning xotira manzilini (`&yosh`) talab qiladi.
2. Sababi: C da funksiyalar parametrlarni qiymat bo'yicha qabul qiladi; agar manzil uzatilmasa, `scanf` o'zgaruvchini o'zgartira olmaydi.
3. Manzil operatori `&` o'zgaruvchi joylashgan bayt koordinatasini beradi.

## Ishlash natijasi:
```text
Yoshingizni kiriting: Qabul qilingan yosh: 21
```

---

# 40-Topshiriq: scanf() orqali bir nechta qiymat o'qish va qaytarish kodini tekshirish

## Topshiriq sharti:
scanf nechta qiymatni muvaffaqiyatli o'qiganini tekshirish usulini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 10, b = 20;
    // scanf muvaffaqiyatli o'qilgan elementlar sonini qaytaradi
    int oqildi = 2; // Simulyatsiya qilingan scanf qaytishi

    if (oqildi == 2) {
        printf("Ikkala son ham to'g'ri o'qildi: a = %d, b = %d\n", a, b);
    } else {
        printf("Kiritishda xatolik yuz berdi!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `scanf` funksiyasi int qiymat qaytaradi: bu format spetsifikatorlariga mos kelib, muvaffaqiyatli o'qilgan o'zgaruvchilar sonidir.
2. Agar foydalanuvchi son o'rniga harf kiritsa, `scanf` o'qishni to'xtatadi va kutilgandan kamroq son qaytaradi.
3. `if (scanf(...) != 2)` tekshiruvi xavfsiz C dasturlarining poydevoridir.

## Ishlash natijasi:
```text
Ikkala son ham to'g'ri o'qildi: a = 10, b = 20
```

---

# 41-Topshiriq: Kiritish buferida qolib ketgan yangi qator (\n) belgisini tozalash

## Topshiriq sharti:
Son kiritilgandan so'ng belgi kiritishda yuzaga keladigan bufer muammosini hal qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 42;
    char belgi = 'K';

    printf("Son: %d\n", son);
    // Buferda qolgan \n ni tozalash usuli:
    // while ((ch = getchar()) != '\n' && ch != EOF);
    // Yoki scanf formatida bo'shliq: scanf(" %c", &belgi);
    printf("Belgi to'g'ri qabul qilindi: %c\n", belgi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Foydalanuvchi son kiritib 'Enter' tugmasini bosganda, son o'zgaruvchiga tushadi, lekin `\n` belgisi standart kiritish buferida (stdin) qoladi.
2. Keyingi `%c` o'sha `\n` ni yangi belgi deb o'qib yuboradi.
3. Yechim: `%c` oldiga bitta bo'shliq qo'yish (`scanf(" %c", &belgi)`) — bu oraliqdagi barcha bo'shliq va `\n` larni o'tkazib yuboradi.

## Ishlash natijasi:
```text
Son: 42
Belgi to'g'ri qabul qilindi: K
```

---

# 42-Topshiriq: typedef orqali mavjud tiplarga yangi nom berish

## Topshiriq sharti:
typedef yordamida o'lchov birliklari va tushunarli nomlar hosil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef unsigned long long int Bayt;
typedef unsigned short int PortTuri;

int main(void) {
    Bayt xotira_hajmi = 16777216ULL; // 16 MB
    PortTuri http_port = 80;

    printf("Xotira hajmi: %llu bayt\n", xotira_hajmi);
    printf("Port: %hu\n", http_port);
    printf("Bayt turi hajmi: %zu bayt\n", sizeof(Bayt));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `typedef` yangi tur yaratmaydi, balki mavjud turga yangi ma'noli nom (alias) beradi.
2. Bu kodning o'qiluvchanligini oshiradi va apparat o'zgarganda faqat `typedef` qatorini o'zgartirish orqali butun kodni moslashtirish imkonini beradi.

## Ishlash natijasi:
```text
Xotira hajmi: 16777216 bayt
Port: 80
Bayt turi hajmi: 8 bayt
```

---

# 43-Topshiriq: Butun sonli literallarning prefikslari (0x, 0, 0b)

## Topshiriq sharti:
Bitta sonni o'nlik, o'n oltilik, sakkizlik va ikkilik (C23 da 0b) ko'rinishida ifodalang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int onlik = 42;
    int on_oltilik = 0x2A;
    int sakkizlik = 052;

    printf("O'nlik 42: %d\n", onlik);
    printf("0x2A qiymati: %d\n", on_oltilik);
    printf("052 qiymati: %d\n", sakkizlik);

    if (onlik == on_oltilik && onlik == sakkizlik) {
        printf("Barcha yozuv shakllari bir xil 42 sonini bildiradi!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `0x` yoki `0X` prefiksi sonning 16 lik asosda ekanligini bildiradi (`0x2A = 2*16 + 10 = 42`).
2. `0` prefiksi sonning 8 lik asosda ekanligini bildiradi (`052 = 5*8 + 2 = 42`).
3. Kompilyatordan so'ng barcha sonlar kompyuter xotirasida bir xil binar qiymatga aylanadi.

## Ishlash natijasi:
```text
O'nlik 42: 42
0x2A qiymati: 42
052 qiymati: 42
Barcha yozuv shakllari bir xil 42 sonini bildiradi!
```

---

# 44-Topshiriq: Butun sonli literallarning suffikslari (U, L, UL, ULL)

## Topshiriq sharti:
Turli suffikslar yordamida literal turlarini aniq belgilang va chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    unsigned int a = 100U;
    long b = 200000L;
    unsigned long c = 3000000UL;
    unsigned long long d = 4000000000ULL;

    printf("U: %u\n", a);
    printf("L: %ld\n", b);
    printf("UL: %lu\n", c);
    printf("ULL: %llu\n", d);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Suffikslar kompilyatorga son literalini qaysi turda talqin qilishni aniq ko'rsatadi.
2. Agar katta songa `ULL` qo'yilmasa, 32-bitli kompilyator uni oddiy `int` deb hisoblab, ogohlantirish berishi mumkin.
3. Bu xavfsiz va platformadan xoli hisoblashlar uchun zarurdir.

## Ishlash natijasi:
```text
U: 100
L: 200000
UL: 3000000
ULL: 4000000000
```

---

# 45-Topshiriq: Suzuvchi sonli literallarning suffikslari (F, L)

## Topshiriq sharti:
float va long double literallarini suffikslar orqali farqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    float f = 1.25F;
    double d = 1.25;
    long double ld = 1.25L;

    printf("float hajmi: %zu bayt\n", sizeof(f));
    printf("double hajmi: %zu bayt\n", sizeof(d));
    printf("long double hajmi: %zu bayt\n", sizeof(ld));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Suffikssiz har qanday o'nlik kasr (masalan `1.25`) standart bo'yicha `double` tipiga ega bo'ladi.
2. `F` suffiksi uni `float` (4 bayt) ga aylantiradi.
3. `L` suffiksi esa `long double` (ko'pincha 12 yoki 16 bayt) ga aylantiradi.

## Ishlash natijasi:
```text
float hajmi: 4 bayt
double hajmi: 8 bayt
long double hajmi: 16 bayt
```

---

# 46-Topshiriq: O'zgaruvchilarning ko'rinish sohasi (Scope: lokal va global o'zgaruvchilar)

## Topshiriq sharti:
Global va blok ichidagi lokal o'zgaruvchilarning o'zaro ta'sirini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int son = 100; // Global o'zgaruvchi

int main(void) {
    int son = 50; // Lokal o'zgaruvchi (globalni soyalaydi - shadowing)
    printf("Lokal son: %d\n", son);

    {
        int son = 25; // Ichki blokdagi lokal o'zgaruvchi
        printf("Ichki blokdagi son: %d\n", son);
    }

    printf("Qayta lokal son: %d\n", son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Global o'zgaruvchi barcha funksiyalardan tashqarida e'lon qilinadi va butun dasturda ko'rinadi.
2. Funksiya yoki figurali qavs `{}` ichida e'lon qilingan o'zgaruvchi faqat shu blok doirasida yashaydi.
3. Bir xil nomli lokal o'zgaruvchi tashqi yoki global o'zgaruvchini soyalaydi (variable shadowing).

## Ishlash natijasi:
```text
Lokal son: 50
Ichki blokdagi son: 25
Qayta lokal son: 50
```

---

# 47-Topshiriq: Global o'zgaruvchilarning avtomatik nol initsializatsiyasi (BSS segmenti)

## Topshiriq sharti:
Initsializatsiya qilinmagan global o'zgaruvchining boshlang'ich qiymatini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int global_son;
float global_haqiqiy;
char global_satr[10];

int main(void) {
    printf("Global int: %d\n", global_son);
    printf("Global float: %.2f\n", global_haqiqiy);
    printf("Global char massiv birinchi belgisi: %d\n", global_satr[0]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C standartiga ko'ra, qiymat berilmagan global va static o'zgaruvchilar BSS (Block Started by Symbol) segmentiga joylashadi.
2. Dastur ishga tushganda operatsion tizim BSS segmentini to'liq nollar bilan to'ldiradi.
3. Shuning uchun `global_son` har doim 0, `global_haqiqiy` esa 0.0 ga teng bo'ladi.

## Ishlash natijasi:
```text
Global int: 0
Global float: 0.00
Global char massiv birinchi belgisi: 0
```

---

# 48-Topshiriq: Initsializatsiya qilinmagan lokal o'zgaruvchilar xavfi (Garbage values)

## Topshiriq sharti:
Initsializatsiya qilinmagan lokal o'zgaruvchining nima uchun tasodifiy qiymat olishini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

void funksiya_a(void) {
    int x = 12345;
    (void)x;
}

void funksiya_b(void) {
    int xavfli_son; // Initsializatsiya qilinmagan!
    // Bu yerda xavfli_son stackdagi avvalgi funksiyadan qolgan axlat qiymatni oladi
    printf("Xavfli lokal son xotirada: %d\n", xavfli_son);
}

int main(void) {
    funksiya_a();
    funksiya_b();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Lokal o'zgaruvchilar chaqiruv steki (Stack) ustida ajratiladi va ularga avtomatik nol berilmaydi.
2. Xotiraning o'sha manzilida avval nima saqlangan bo'lsa (axlat qiymat - garbage value), o'shani o'qiydi.
3. Qoida: barcha lokal o'zgaruvchilarni e'lon qilish paytida kamida `0` bilan initsializatsiya qilish zarur!

## Ishlash natijasi:
```text
Xavfli lokal son xotirada: 12345
```

---

# 49-Topshiriq: const o'zgaruvchi va xotirani o'zgartirishdan himoya

## Topshiriq sharti:
const int o'zgaruvchisini xavfsiz o'qish va uning o'zgarmaslik himoyasini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    const int cheklov = 500;
    const int *ptr = &cheklov;

    printf("Cheklov qiymati: %d\n", *ptr);
    printf("Cheklov manzili: %p\n", (void*)ptr);
    // *ptr = 600; // Kompilyatsiya xatosi: read-only location
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `const int cheklov = 500;` qiymati kompilyator tomonidan himoyalanadi.
2. `const int *ptr` ko'rsatkichi 'ushbu ko'rsatkich orqali qiymatni o'zgartirib bo'lmaydi' degan ma'noni anglatadi.
3. Bu tizim xavfsizligini ta'minlab, tasodifiy o'zgarishlarning oldini oladi.

## Ishlash natijasi:
```text
Cheklov qiymati: 500
Cheklov manzili: 000000000012FFE4
```

---

# 50-Topshiriq: C tili asosiy ma'lumot turlarining to'liq xotira jadvali

## Topshiriq sharti:
Barcha asosiy tiplar hajmi va format spetsifikatorlarini chiroyli jadval ko'rinishida chop eting.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    printf("--------------------------------------------------\n");
    printf("| %-16s | %-12s | %-12s |\n", "Ma'lumot turi", "Hajmi (bayt)", "Format belgisi");
    printf("--------------------------------------------------\n");
    printf("| %-16s | %-12zu | %-12s |\n", "char", sizeof(char), "%c / %d");
    printf("| %-16s | %-12zu | %-12s |\n", "short", sizeof(short), "%hd");
    printf("| %-16s | %-12zu | %-12s |\n", "int", sizeof(int), "%d / %i");
    printf("| %-16s | %-12zu | %-12s |\n", "unsigned int", sizeof(unsigned int), "%u");
    printf("| %-16s | %-12zu | %-12s |\n", "long", sizeof(long), "%ld");
    printf("| %-16s | %-12zu | %-12s |\n", "long long", sizeof(long long), "%lld");
    printf("| %-16s | %-12zu | %-12s |\n", "float", sizeof(float), "%f");
    printf("| %-16s | %-12zu | %-12s |\n", "double", sizeof(double), "%lf");
    printf("| %-16s | %-12zu | %-12s |\n", "pointer (void*)", sizeof(void*), "%p");
    printf("--------------------------------------------------\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Jadval orqali C tilidagi barcha asosiy tiplar, ularning xotira sig'imi va format spetsifikatorlari umumlashtiriladi.
2. 64-bitli arxitekturada ko'rsatkichlar (`void*`) 8 bayt bo'ladi.
3. Bu bilimlar barcha keyingi modullarning poydevori hisoblanadi.

## Ishlash natijasi:
```text
--------------------------------------------------
| Ma'lumot turi    | Hajmi (bayt) | Format belgisi |
--------------------------------------------------
| char             | 1            | %c / %d      |
| short            | 2            | %hd          |
| int              | 4            | %d / %i      |
| unsigned int     | 4            | %u           |
| long             | 4            | %ld          |
| long long        | 8            | %lld         |
| float            | 4            | %f           |
| double           | 8            | %lf          |
| pointer (void*)  | 8            | %p           |
--------------------------------------------------
```

---
