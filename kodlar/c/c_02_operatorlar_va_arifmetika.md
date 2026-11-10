# C Dasturlash Tili — 2-Qism: Operatorlar va Arifmetika
## (51-100 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* Arifmetik amallar, bo'lish va qoldiq olish (%) xususiyatlari
* Pre va post inkrement/dekrement (++x, x++, --x, x--)
* Mantiqiy operatorlar: &&, ||, ! va qisqa tutashuv (Short-circuit)
* Bitwise operatorlar: &, |, ^, ~, <<, >> va bitmask amallari (SET, CLEAR, TOGGLE)
* Brian Kernighan popcount algoritmi, Branchless ABS va MIN usullari
* Endianness, baytlarni teskarilash va XOR shifrlash

---

# 51-Topshiriq: Asosiy arifmetik operatorlar va ularning birgalikdagi hisobi

## Topshiriq sharti:
To'rtta asosiy arifmetik amalni (+, -, *, /) bitta ifodada qo'llab, amallar tartibini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 20, b = 10, c = 5, d = 2;
    int natija = a + b * c - a / d;

    printf("a = %d, b = %d, c = %d, d = %d\n", a, b, c, d);
    printf("Hisob: %d + %d * %d - %d / %d\n", a, b, c, a, d);
    printf("Natija: %d\n", natija);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matematikadagi kabi C tilida ham ko'paytirish `*` va bo'lish `/` operatorlari qo'shish `+` va ayirish `-` ga nisbatan yuqori ustunlikka (precedence) ega.
2. Bajarilish tartibi: birinchi bo'lib `b * c` (10 * 5 = 50) va `a / d` (20 / 2 = 10) hisoblanadi.
3. So'ngra chapdan o'ngga: 20 + 50 - 10 = 60 hosil bo'ladi.

## Ishlash natijasi:
```text
a = 20, b = 10, c = 5, d = 2
Hisob: 20 + 10 * 5 - 20 / 2
Natija: 60
```

---

# 52-Topshiriq: Qoldiqli bo'lish (%) operatori va sonning juft/toqligini aniqlash

## Topshiriq sharti:
Berilgan sonning juft yoki toq ekanligini qoldiqli bo'lish operatori orqali aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 17;
    int qoldiq = son % 2;

    printf("Tekshirilayotgan son: %d\n", son);
    printf("2 ga bo'lgandagi qoldiq: %d\n", qoldiq);

    if (qoldiq == 0) {
        printf("%d — Juft son.\n", son);
    } else {
        printf("%d — Toq son.\n", son);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `%` operatori butun sonni boshqa butun songa bo'lgandagi qoldiqni qaytaradi.
2. Har qanday juft son 2 ga qoldiqsiz bo'linadi (qoldiq 0).
3. Toq sonlar 2 ga bo'linganda qoldiq 1 (yoki manfiy toq sonlarda -1) bo'ladi.

## Ishlash natijasi:
```text
Tekshirilayotgan son: 17
2 ga bo'lgandagi qoldiq: 1
17 — Toq son.
```

---

# 53-Topshiriq: Pre-increment (++x) va Post-increment (x++) amaliy farqi

## Topshiriq sharti:
Pre va post inkrementning ifoda ichidagi farqini aniq namoyish eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 5;
    int y = 5;

    int natija_post = x++; // Avval x ning eski qiymati olinadi, keyin x 1 ga oshadi
    int natija_pre = ++y;  // Avval y 1 ga oshadi, keyin yangi qiymat olinadi

    printf("Post-inkrement: natija = %d, x ning yangi qiymati = %d\n", natija_post, x);
    printf("Pre-inkrement:  natija = %d, y ning yangi qiymati = %d\n", natija_pre, y);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `x++` (post-increment): o'zgaruvchining joriy qiymati ifodada ishlatiladi, so'ngra uning qiymati 1 taga oshiriladi.
2. `++y` (pre-increment): dastlab o'zgaruvchi qiymati 1 taga oshiriladi, keyin oshgan qiymat ifodada ishlatiladi.
3. Sikllarda bir o'zi turganda tezlik jihatidan farq qilmaydi, lekin ifoda ichida butunlay boshqa natija beradi.

## Ishlash natijasi:
```text
Post-inkrement: natija = 5, x ning yangi qiymati = 6
Pre-inkrement:  natija = 6, y ning yangi qiymati = 6
```

---

# 54-Topshiriq: Pre-decrement (--x) va Post-decrement (x--)

## Topshiriq sharti:
Dekrement operatorlari orqali orqaga sanash va ifoda qiymatlarini solishtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 10;
    int b = 10;

    int res1 = a--;
    int res2 = --b;

    printf("res1 (a--): %d, a oxiri: %d\n", res1, a);
    printf("res2 (--b): %d, b oxiri: %d\n", res2, b);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Dekrement qiymatni 1 taga kamaytiradi.
2. `a--` avvalgi 10 qiymatini qaytaradi, `a` esa 9 bo'lib qoladi.
3. `--b` avval 9 ga kamaytirib, keyin 9 qiymatini qaytaradi.

## Ishlash natijasi:
```text
res1 (a--): 10, a oxiri: 9
res2 (--b): 9, b oxiri: 9
```

---

# 55-Topshiriq: Qisqartirilgan o'zlashtirish operatorlari (+=, -=, *=, /=, %=)

## Topshiriq sharti:
Hisoblagichni turli qisqartirilgan operatorlar bilan yangilab boring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int hisob = 100;

    hisob += 50;  // hisob = hisob + 50 (150)
    hisob -= 30;  // hisob = hisob - 30 (120)
    hisob *= 2;   // hisob = hisob * 2  (240)
    hisob /= 4;   // hisob = hisob / 4  (60)
    hisob %= 7;   // hisob = hisob % 7  (4)

    printf("Yakuniy hisob: %d\n", hisob);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Qisqartirilgan operatorlar kodni ixchamlashtiradi va kompyuter tiliga yaqinroq hisoblanadi.
2. `x op= y` amali ekvivalent ravishda `x = x op (y)` deb baholanadi.

## Ishlash natijasi:
```text
Yakuniy hisob: 4
```

---

# 56-Topshiriq: Tenglik (==) va o'zlashtirish (=) farqi va xavfli xatolik

## Topshiriq sharti:
Shart ichida xato ravishda = qo'yish oqibatini va uni oldini olish usulini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int status = 0;

    // To'g'ri taqqoslash: status == 1
    if (status == 1) {
        printf("Bu qator chiqmaydi\n");
    } else {
        printf("Status 1 ga teng emas (To'g'ri tekshiruv).\n");
    }

    // Yoda shart uslubi (Yoda conditions): doimiyni chapga qo'yish
    // if (1 == status) - agar tasodifan 1 = status yozilsa, kompilyator xato beradi!
    if (0 == status) {
        printf("Yoda sharti xavfsiz ishladi: status 0 ga teng!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `==` bu mantiqiy taqqoslash operatori, `=` esa qiymat berish (o'zlashtirish) operatoridir.
2. Agar `if (status = 1)` yozilsa, `status` ga 1 o'zlashtiriladi va shart har doim `true` bo'lib qoladi.
3. 'Yoda conditions' (`if (1 == status)`) uslubi doimiyni chapga qo'yish orqali xato yozilganda kompilyatsiyada xatolik chiqarishni ta'minlaydi.

## Ishlash natijasi:
```text
Status 1 ga teng emas (To'g'ri tekshiruv).
Yoda sharti xavfsiz ishladi: status 0 ga teng!
```

---

# 57-Topshiriq: Taqqoslash (munosabat) operatorlari: !=, <, >, <=, >=

## Topshiriq sharti:
Harorat ko'rsatkichi asosida barcha taqqoslash operatorlarini sinab ko'ring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int t1 = 25;
    int t2 = 30;

    printf("t1 == t2: %d\n", t1 == t2);
    printf("t1 != t2: %d\n", t1 != t2);
    printf("t1 < t2:  %d\n", t1 < t2);
    printf("t1 > t2:  %d\n", t1 > t2);
    printf("t1 <= 25: %d\n", t1 <= 25);
    printf("t2 >= 30: %d\n", t2 >= 30);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida mantiqiy rost shart 1 butun soni, yolg'on shart esa 0 butun soni bilan ifodalanadi.
2. Taqqoslash operatorlari har doim 1 yoki 0 natija qaytaradi.

## Ishlash natijasi:
```text
t1 == t2: 0
t1 != t2: 1
t1 < t2:  1
t1 > t2:  0
t1 <= 25: 1
t2 >= 30: 1
```

---

# 58-Topshiriq: Mantiqiy VA (&&) operatori va oraliqni tekshirish

## Topshiriq sharti:
Ballning [60, 100] oralig'ida ekanligini mantiqiy VA orqali tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int ball = 85;

    if (ball >= 60 && ball <= 100) {
        printf("Talaba imtihondan o'tdi! (Ball: %d)\n", ball);
    } else {
        printf("Talaba yiqildi yoki ball noto'g'ri!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `&&` (Mantiqiy VA) ikkala tomonidagi ifoda ham rost (nol bo'lmagan) bo'lgandagina 1 qaytaradi.
2. Matematikadagi `60 <= ball <= 100` ifodasi C da ishlamaydi (chunki `60 <= ball` 1 bo'lib, keyin `1 <= 100` har doim rost bo'ladi).
3. C da har bir shart alohida yozilib, `&&` orqali birlashtiriladi.

## Ishlash natijasi:
```text
Talaba imtihondan o'tdi! (Ball: 85)
```

---

# 59-Topshiriq: Mantiqiy YOKI (||) operatori va dam olish kunlarini aniqlash

## Topshiriq sharti:
Hafta kuni raqami bo'yicha shanba (6) yoki yakshanba (7) ekanligini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int hafta_kuni = 7; // Yakshanba

    if (hafta_kuni == 6 || hafta_kuni == 7) {
        printf("Bugun dam olish kuni!\n");
    } else {
        printf("Bugun ish kuni.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `||` (Mantiqiy YOKI) shartlardan kamida bittasi rost bo'lsa, butun ifoda rost (1) bo'ladi.
2. Faqat ikkala tomon ham yolg'on (0) bo'lgandagina 0 qaytaradi.

## Ishlash natijasi:
```text
Bugun dam olish kuni!
```

---

# 60-Topshiriq: Mantiqiy INKOR (!) operatori va qiymatni inkor qilish

## Topshiriq sharti:
Mantiqiy inkor operatori sonlarni qanday o'zgartirishini tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int bayroq = 0;
    int son = 42;

    printf("!bayroq: %d\n", !bayroq);
    printf("!son:    %d\n", !son);
    printf("!!son (bool ga normallashtirish): %d\n", !!son);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `!` operatori 0 ni 1 ga, har qanday 0 dan farqli sonni esa 0 ga aylantiradi.
2. `!!son` (ikkita inkor) har qanday sonni uning ekvivalent sof bool qiymatiga (0 yoki 1) normallashtiradi.

## Ishlash natijasi:
```text
!bayroq: 1
!son:    0
!!son (bool ga normallashtirish): 1
```

---

# 61-Topshiriq: Short-circuit evaluation (Qisqa tutashuvli baholash) xususiyati

## Topshiriq sharti:
Nolga bo'linish xatosining mantiqiy VA orqali qanday oldi olinishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int boluvchi = 0;
    int bolinuvchi = 100;

    // Agar boluvchi != 0 yolg'on bo'lsa, ikkinchi qism umuman hisoblanmaydi!
    if (boluvchi != 0 && (bolinuvchi / boluvchi) > 1) {
        printf("Bo'linma 1 dan katta\n");
    } else {
        printf("Xavfsiz tekshiruv: nolga bo'lish xatosi ro'y bermadi!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da `&&` operatori birinchi argument `0` (yolg'on) ekanligini ko'rishi bilan ikkinchi argumentni hisoblab o'tirmaydi (Short-circuit).
2. Xuddi shunday `||` operatori birinchi argument `1` (rost) bo'lsa, ikkinchi tomonni hisoblamaydi.
3. Bu xususiyat ko'rsatkichlarning NULL emasligini yoki nolga bo'linishni bitta qatorda xavfsiz tekshirish imkonini beradi.

## Ishlash natijasi:
```text
Xavfsiz tekshiruv: nolga bo'lish xatosi ro'y bermadi!
```

---

# 62-Topshiriq: Bitwise VA (&) operatori: Bitlarni filtrlash va niqoblash

## Topshiriq sharti:
Ikki bayt ustida bitli VA amalini bajarib, uning ikkilik mohiyatini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    unsigned char a = 0x0F; // 00001111
    unsigned char b = 0x36; // 00110110
    unsigned char res = a & b; // 00000110 (0x06 = 6)

    printf("a = 0x%02X, b = 0x%02X\n", a, b);
    printf("a & b = 0x%02X (O'nlikda: %d)\n", res, res);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitwise `&` ikkala operandning mos bitlari bir vaqtda 1 bo'lgandagina natijaviy bitni 1 qiladi.
2. `0x0F` bilan bitli VA qilish yuqori 4 bitni tozalab, faqat pastki 4 bitni (quyi nibble) qoldiradi.

## Ishlash natijasi:
```text
a = 0x0F, b = 0x36
a & b = 0x06 (O'nlikda: 6)
```

---

# 63-Topshiriq: Bitwise YOKI (|) operatori: Bitlarni yoqish

## Topshiriq sharti:
Bitli YOKI amali orqali alohida bitlarni 1 ga aylantiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    unsigned char a = 0x40; // 01000000 (64)
    unsigned char b = 0x08; // 00001000 (8)
    unsigned char res = a | b; // 01001000 (72)

    printf("a = 0x%02X, b = 0x%02X\n", a, b);
    printf("a | b = 0x%02X (O'nlikda: %d)\n", res, res);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitwise `|` kamida bitta operanddagi bit 1 bo'lsa, natijaviy bitni 1 qiladi.
2. Bu apparatda registrlarga yangi sozlamalar va bayroqlarni kiritishda keng qo'llaniladi.

## Ishlash natijasi:
```text
a = 0x40, b = 0x08
a | b = 0x48 (O'nlikda: 72)
```

---

# 64-Topshiriq: Bitwise XOR (^) operatori va o'ziga xos xususiyatlari

## Topshiriq sharti:
XOR ning farqli bitlarni 1 qilish va x ^ x == 0 xususiyatini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    unsigned char a = 0x55; // 01010101
    unsigned char b = 0x0F; // 00001111
    unsigned char res = a ^ b; // 01011010 (0x5A)

    printf("a ^ b = 0x%02X\n", res);
    printf("a ^ a = %u (O'z-o'ziga XOR har doim nol!)\n", a ^ a);
    printf("(a ^ b) ^ b = 0x%02X (Qayta tiklash!)\n", (a ^ b) ^ b);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bitwise `^` mos bitlar har xil (biri 0, biri 1) bo'lsa 1, bir xil bo'lsa 0 beradi.
2. Har qanday sonni o'ziga XOR qilsak har doim 0 chiqadi (`x ^ x = 0`).
3. Sonni boshqa son bilan ikki marta ketma-ket XOR qilish yana boshlang'ich sonni qaytaradi (`(x ^ y) ^ y = x`).

## Ishlash natijasi:
```text
a ^ b = 0x5A
a ^ a = 0 (O'z-o'ziga XOR har doim nol!)
(a ^ b) ^ b = 0x55 (Qayta tiklash!)
```

---

# 65-Topshiriq: Ikki o'zgaruvchi qiymatini qo'shimcha o'zgaruvchisiz almashtirish (XOR Swap)

## Topshiriq sharti:
XOR operatori yordamida uchinchi vaqtinchalik o'zgaruvchisiz a va b ni almashtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 15;
    int b = 27;

    printf("Boshida: a = %d, b = %d\n", a, b);

    a = a ^ b;
    b = a ^ b;
    a = a ^ b;

    printf("Almashgach: a = %d, b = %d\n", a, b);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 1-qadam: `a = a ^ b` (a ichida ikkala sonning farq kombinatsiyasi saqlanadi).
2. 2-qadam: `b = (a ^ b) ^ b = a` (b ga a ning asl qiymati o'tadi).
3. 3-qadam: `a = (a ^ b) ^ a = b` (a ga b ning asl qiymati o'tadi).
4. Bu algoritm registrlar yetishmagan mikrokontrollerlarda qo'shimcha xotira sarflamaslik uchun xizmat qiladi.

## Ishlash natijasi:
```text
Boshida: a = 15, b = 27
Almashgach: a = 27, b = 15
```

---

# 66-Topshiriq: Bitwise inkor (~) operatori (One's complement)

## Topshiriq sharti:
Barcha bitlarni teskarilash va ~x = -(x + 1) qonuniyatini namoyish eting.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 10;
    int res = ~x;

    printf("x = %d, ~x = %d\n", x, res);
    printf("-(x + 1) formulasi bo'yicha: %d\n", -(x + 1));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `~` (tilda) operatori o'zgaruvchining barcha 0 bitlarini 1 ga, barcha 1 bitlarini 0 ga aylantiradi.
2. Two's complement xotira tizimida har qanday `x` uchun `~x` qiymati aniq `-(x + 1)` ga teng bo'ladi.

## Ishlash natijasi:
```text
x = 10, ~x = -11
-(x + 1) formulasi bo'yicha: -11
```

---

# 67-Topshiriq: Chapga surish (<<) operatori: 2 ning darajasiga ko'paytirish

## Topshiriq sharti:
Sonni 1, 2 va 3 pozitsiyaga chapga surib, natijalarni ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 5;

    printf("son << 1 (5 * 2^1): %d\n", son << 1);
    printf("son << 2 (5 * 2^2): %d\n", son << 2);
    printf("son << 3 (5 * 2^3): %d\n", son << 3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `x << k` amali sonning barcha bitlarini chap tomonga `k` ta katak suradi, o'ng tomondan bo'sh qolgan o'rinlarga 0 larni to'ldiradi.
2. Bu matematik jihatdan sonni 2^k ga ko'paytirish bilan bir xildir.
3. Protsessor apparatida bitli surish ko'paytirish buyrug'idan ancha tezroq bajariladi.

## Ishlash natijasi:
```text
son << 1 (5 * 2^1): 10
son << 2 (5 * 2^2): 20
son << 3 (5 * 2^3): 40
```

---

# 68-Topshiriq: O'ngga surish (>>) operatori: 2 ning darajasiga butunli bo'lish

## Topshiriq sharti:
Sonni o'ngga surish orqali 2, 4 va 8 ga bo'ling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int son = 80;

    printf("son >> 1 (80 / 2^1): %d\n", son >> 1);
    printf("son >> 2 (80 / 2^2): %d\n", son >> 2);
    printf("son >> 3 (80 / 2^3): %d\n", son >> 3);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `x >> k` amali son bitlarini o'ngga suradi, bu sonni 2^k ga butunli bo'lishga tengdir.
2. Qoldiqlar shunchaki tashlab yuboriladi.

## Ishlash natijasi:
```text
son >> 1 (80 / 2^1): 40
son >> 2 (80 / 2^2): 20
son >> 3 (80 / 2^3): 10
```

---

# 69-Topshiriq: Unsigned va signed sonlarda o'ngga surish (Mantiqiy vs Arifmetik surish)

## Topshiriq sharti:
Manfiy signed son va unsigned sonni o'ngga surishdagi muhim farqni ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    signed char s = -16;
    unsigned char u = (unsigned char)-16;

    signed char s_surilgan = s >> 2;
    unsigned char u_surilgan = u >> 2;

    printf("Signed s: %d, o'ngga surilgach: %d (Arifmetik surish - ishora saqlanadi)\n", 
           s, s_surilgan);
    printf("Unsigned u: %u, o'ngga surilgach: %u (Mantiqiy surish - chapdan 0 keladi)\n", 
           u, u_surilgan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `unsigned` turlarda o'ngga surish mantiqiy (Logical shift) bo'lib, chapdan har doim 0 bitlar kiradi.
2. `signed` manfiy turlarda o'ngga surish ko'pgina tizimlarda arifmetik (Arithmetic shift) bo'lib, sonning manfiyligini saqlash uchun chapdan 1 bitlar kiradi.
3. Shuning uchun bitlar bilan ishlaganda har doim `unsigned` turlardan foydalanish tavsiya etiladi!

## Ishlash natijasi:
```text
Signed s: -16, o'ngga surilgach: -4 (Arifmetik surish - ishora saqlanadi)
Unsigned u: 240, o'ngga surilgach: 60 (Mantiqiy surish - chapdan 0 keladi)
```

---

# 70-Topshiriq: Bitmask: n-chi bitning qiymatini tekshirish ((x >> n) & 1)

## Topshiriq sharti:
Berilgan sonning 3-biti (0 dan boshlab) 1 yoki 0 ekanligini aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    unsigned int son = 0x2A; // 00101010
    int n = 3; // 3-bit

    int bit_qiymati = (son >> n) & 1;

    printf("Son: 0x%02X\n", son);
    printf("%d-chi bit qiymati: %d\n", n, bit_qiymati);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sonni `n` marta o'ngga sursak, qiziqtirgan `n`-chi bit eng pastki (0-chi) pozitsiyaga keladi.
2. Keyin `& 1` bilan bitli VA qilinsa, qolgan barcha yuqori bitlar o'chib, faqat shu bitning 0 yoki 1 qiymati qoladi.

## Ishlash natijasi:
```text
Son: 0x2A
3-chi bit qiymati: 1
```

---

# 71-Topshiriq: Bitmask: n-chi bitni 1 ga tenglashtirish (SET BIT: x |= (1 << n))

## Topshiriq sharti:
Sonning 2-bitini 1 ga aylantiring va natijani ko'ring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    unsigned char x = 0x00; // 00000000
    int n = 2;

    x |= (1 << n); // 00000100 (4)

    printf("SET qilingach x: 0x%02X (%d)\n", x, x);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `(1 << n)` ifodasi faqat `n`-chi biti 1 bo'lgan binar niqob (mask) yaratadi.
2. `x |= mask` amali boshqa hech bir bitga tegmasdan, aynan `n`-chi bitni 1 ga aylantiradi.

## Ishlash natijasi:
```text
SET qilingach x: 0x04 (4)
```

---

# 72-Topshiriq: Bitmask: n-chi bitni 0 ga tenglashtirish (CLEAR BIT: x &= ~(1 << n))

## Topshiriq sharti:
Sonning 3-bitini boshqa bitlarga tegmasdan 0 ga aylantiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    unsigned char x = 0x0F; // 00001111 (15)
    int n = 3;

    x &= ~(1 << n); // ~(00001000) = 11110111, natija: 00000111 (7)

    printf("CLEAR qilingach x: 0x%02X (%d)\n", x, x);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `(1 << n)` niqobida faqat `n`-chi bit 1 bo'ladi.
2. `~(1 << n)` qilinganda esa aksincha faqat `n`-chi bit 0, qolgan barcha bitlar 1 bo'ladi.
3. `x &= niqob` amali faqat o'sha 0 bo'lgan bitni o'chiradi, 1 bo'lgan barcha bitlarni o'z holicha saqlaydi.

## Ishlash natijasi:
```text
CLEAR qilingach x: 0x07 (7)
```

---

# 73-Topshiriq: Bitmask: n-chi bitni teskarilash (TOGGLE BIT: x ^= (1 << n))

## Topshiriq sharti:
Chiroq holatini (0 yoki 1) TOGGLE operatori orqali ketma-ket o'zgartiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    unsigned char chiroq = 0; // O'chiq
    int n = 0; // 0-bit

    chiroq ^= (1 << n); // Yoqildi (1)
    printf("1-bosqich: %d\n", chiroq);

    chiroq ^= (1 << n); // O'chirildi (0)
    printf("2-bosqich: %d\n", chiroq);

    chiroq ^= (1 << n); // Qayta yoqildi (1)
    printf("3-bosqich: %d\n", chiroq);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. XOR (`^`) operatori agar niqobdagi bit 1 bo'lsa, mos bitni teskari aylantiradi (0 bo'lsa 1, 1 bo'lsa 0).
2. Bu mikrokontrollerlarda LED svetodiodlarni miltillatishning klassik standartidir.

## Ishlash natijasi:
```text
1-bosqich: 1
2-bosqich: 0
3-bosqich: 1
```

---

# 74-Topshiriq: Sonning 2 ning darajasi ekanligini bit bilan tekshirish (x & (x - 1))

## Topshiriq sharti:
Son 2 ning darajasi (1, 2, 4, 8, 16...) ekanligini bitta bitli amal bilan aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool ikki_darajasimi(unsigned int x) {
    return (x > 0) && ((x & (x - 1)) == 0);
}

int main(void) {
    unsigned int a = 16;
    unsigned int b = 18;

    printf("%u 2 ning darajasimi: %s\n", a, ikki_darajasimi(a) ? "Ha" : "Yo'q");
    printf("%u 2 ning darajasimi: %s\n", b, ikki_darajasimi(b) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 2 ning har qanday darajasi binar shaklda faqat bitta 1 bitga ega (masalan 16 = 00010000).
2. Undan 1 ayrilsa, o'sha 1-bit 0 bo'lib, undan pastki barcha bitlar 1 bo'ladi (15 = 00001111).
3. Ularni `&` qilsak aynan 0 chiqadi (`16 & 15 == 0`). Agar son 2 ning darajasi bo'lmasa, natija noldan farqli bo'ladi.

## Ishlash natijasi:
```text
16 2 ning darajasimi: Ha
18 2 ning darajasimi: Yo'q
```

---

# 75-Topshiriq: Sonning eng quyi 1-bitini ajratib olish (x & (-x))

## Topshiriq sharti:
Sonning eng o'ngdagi faol 1-bitini alohida ajratib oling.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 40; // 00101000 (eng quyi 1-bit 8 pozitsiyasida)
    int pastki_bit = x & (-x);

    printf("x = %d\n", x);
    printf("x & (-x) = %d\n", pastki_bit);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Two's complement xotira tizimida `-x = ~x + 1` bo'ladi.
2. Bu amal eng quyi 1-bitdan pastdagi barcha bitlarni teskarilab, o'sha 1-bitni saqlab qoladi.
3. Shuning uchun `x & (-x)` faqat eng quyi 1-bitni qoldirib, boshqa hamma bitlarni 0 qiladi (Fenwick Tree / Binary Indexed Tree da ishlatiladi).

## Ishlash natijasi:
```text
x = 40
x & (-x) = 8
```

---

# 76-Topshiriq: Sonning eng quyi 1-bitini tozalash (x & (x - 1))

## Topshiriq sharti:
Sonning eng pastki 1-bitini o'chirib, natijani kuzating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int x = 12; // 00001100
    int tozalangan = x & (x - 1); // 12 & 11 -> 00001000 (8)

    printf("Boshlang'ich: %d\n", x);
    printf("Quyi 1-bit tozalandi: %d\n", tozalangan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `x - 1` amali eng quyi 1-bitni 0 qiladi va uning o'ngidagi barcha bitlarni 1 ga aylantiradi.
2. `x & (x - 1)` esa bu eng quyi 1-bitni o'chirib tashlaydi.

## Ishlash natijasi:
```text
Boshlang'ich: 12
Quyi 1-bit tozalandi: 8
```

---

# 77-Topshiriq: Bitlarni sanash: Brian Kernighan algoritmi (Hamming Weight / Popcount)

## Topshiriq sharti:
Son ichidagi 1-bitlar sonini minimal qadamda sanovchi funksiyani yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int bitlarni_sana(unsigned int n) {
    int hisob = 0;
    while (n > 0) {
        n = n & (n - 1); // Har bir qadamda bitta 1-bit yo'qotiladi
        hisob++;
    }
    return hisob;
}

int main(void) {
    unsigned int son = 0x5B; // 01011011 (5 ta 1)
    printf("0x%02X sonidagi 1-bitlar soni: %d\n", son, bitlarni_sana(son));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oddiy sikl barcha 32 bitni tekshiradi, Brian Kernighan algoritmi esa faqat 1 ga teng bo'lgan bitlar sonichagina iteratsiya qiladi.
2. Har bir `n = n & (n - 1)` amali navbatdagi 1-bitni o'chiradi.
3. Bu kriptografiya va ma'lumotlarni siqishda juda yuqori unumdorlik beradi.

## Ishlash natijasi:
```text
0x5B sonidagi 1-bitlar soni: 5
```

---

# 78-Topshiriq: Baytni ikkilik (binary) ko'rinishda ekranga chop etuvchi yordamchi funksiya

## Topshiriq sharti:
8-bitli sonni 0 va 1 lardan iborat satr shaklida terminalga chiqaring.

## Yechim (C kodi):
```c
#include <stdio.h>

void chop_et_binar8(unsigned char bayt) {
    for (int i = 7; i >= 0; i--) {
        int bit = (bayt >> i) & 1;
        printf("%d", bit);
    }
    printf("\n");
}

int main(void) {
    unsigned char qiymat = 170; // 10101010
    printf("170 sonining binar ko'rinishi: ");
    chop_et_binar8(qiymat);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 7-bitdan (eng yuqori bit - MSB) boshlab 0-bitgacha (LSB) teskari tartibda sikl aylanadi.
2. Har bir bit `(bayt >> i) & 1` orqali olinadi va raqam sifatida chop etiladi.

## Ishlash natijasi:
```text
170 sonining binar ko'rinishi: 10101010
```

---

# 79-Topshiriq: Ikki sonning belgilari bir xil yoki qarama-qarshi ekanligini XOR bilan bilish

## Topshiriq sharti:
Ikki son turli ishoraga ega ekanligini shartsiz tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdbool.h>

bool qarama_qarshi_ishorami(int x, int y) {
    return ((x ^ y) < 0);
}

int main(void) {
    int a = 10, b = -20;
    int c = 15, d = 30;

    printf("%d va %d qarama-qarshi ishoradami: %s\n", 
           a, b, qarama_qarshi_ishorami(a, b) ? "Ha" : "Yo'q");
    printf("%d va %d qarama-qarshi ishoradami: %s\n", 
           c, d, qarama_qarshi_ishorami(c, d) ? "Ha" : "Yo'q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Butun sonning ishora biti (eng chapdagi 31-bit) musbat sonlarda 0, manfiylarda 1 bo'ladi.
2. Agar ikkala son har xil ishorada bo'lsa, ularni XOR qilganda natijaning ishora biti 1 bo'ladi (ya'ni natija < 0).
3. Bu shart tarmoqlanishsiz (branchless) tezkor ishora tahlilini beradi.

## Ishlash natijasi:
```text
10 va -20 qarama-qarshi ishoradami: Ha
15 va 30 qarama-qarshi ishoradami: Yo'q
```

---

# 80-Topshiriq: Sonning modulini (abs) if siz, bitli amallar bilan topish (Branchless ABS)

## Topshiriq sharti:
Tarmoqlanishsiz (if siz) son modulini hisoblash usulini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int branchless_abs(int n) {
    int mask = n >> 31; // Agar n >= 0 bo'lsa 0x00000000, manfiy bo'lsa 0xFFFFFFFF (-1)
    return (n + mask) ^ mask;
}

int main(void) {
    int a = -42;
    int b = 15;

    printf("abs(%d) = %d\n", a, branchless_abs(a));
    printf("abs(%d) = %d\n", b, branchless_abs(b));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar `n` manfiy bo'lsa, arifmetik surish `n >> 31` natijasi -1 (barcha bitlari 1) bo'ladi.
2. `(n - 1) ^ (-1)` amali esa `-(n)` ga teng bo'ladi (Two's complement xossasi).
3. Zamonaviy CPU larda bu protsessor konveyerida branch misprediction (noto'g'ri bashorat) xarajatlarini yo'qotadi.

## Ishlash natijasi:
```text
abs(-42) = 42
abs(15) = 15
```

---

# 81-Topshiriq: Ikki sonning minimumini shartsiz (Branchless MIN) topish

## Topshiriq sharti:
if ishlatmasdan ikki sonning kichigini topuvchi kod yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int branchless_min(int x, int y) {
    return y ^ ((x ^ y) & -(x < y));
}

int main(void) {
    int a = 25, b = 14;
    printf("min(%d, %d) = %d\n", a, b, branchless_min(a, b));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar `x < y` rost bo'lsa, `-(1)` barcha bitlari 1 bo'lgan niqobni beradi.
2. U holda `y ^ (x ^ y) = x` bo'ladi.
3. Agar `x < y` yolg'on bo'lsa, `-0 = 0` bo'lib, `y ^ 0 = y` qaytadi.

## Ishlash natijasi:
```text
min(25, 14) = 14
```

---

# 82-Topshiriq: Vergul operatori (Comma operator: expr1, expr2) xususiyati

## Topshiriq sharti:
Vergul operatorining chapdan o'ngga hisoblanishi va oxirgi qiymatni qaytarishini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a, b;
    // Vergul operatori ifodalarni navbat bilan bajaradi va eng oxirgi ifoda qiymatini qaytaradi
    int natija = (a = 5, b = 10, a + b);

    printf("a = %d, b = %d, natija = %d\n", a, b, natija);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Vergul operatori C tilidagi eng past ustunlikka (lowest precedence) ega operator hisoblanadi.
2. U barcha ifodalarni chapdan o'ngga hisoblaydi va eng o'ngdagi ifodaning qiymatini butun guruh qiymati sifatida beradi.
3. Ko'pincha `for` sikllarida bir nechta hisoblagichni birga o'zgartirishda ishlatiladi: `for(i=0, j=10; ...; i++, j--)`.

## Ishlash natijasi:
```text
a = 5, b = 10, natija = 15
```

---

# 83-Topshiriq: Operatorlar ustunligi (Precedence) va qavslarning zarurati

## Topshiriq sharti:
Qavssiz va qavsli mantiqiy-arifmetik ifodalarning natijalarini solishtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int a = 1, b = 2, c = 3;

    int res1 = a + b * c;   // Ko'paytirish ustun: 1 + 6 = 7
    int res2 = (a + b) * c; // Qavs ustun: 3 * 3 = 9

    int val = 0x05; // 00000101
    // Bitli surish `+` ga qaraganda pastroq ustunlikka ega!
    int xato = val << 1 + 2;   // Aslida: val << (1 + 2) = 5 << 3 = 40
    int togri = (val << 1) + 2; // (5 * 2) + 2 = 12

    printf("res1: %d, res2: %d\n", res1, res2);
    printf("xato: %d, togri: %d\n", xato, togri);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C tilida `+` va `-` operatorlari `<<` va `>>` bitli surish operatorlaridan ko'ra yuqori ustunlikka ega.
2. Shuning uchun `val << 1 + 2` yozilsa, avval `1 + 2 = 3` qo'shiladi va son 3 ta suriladi.
3. Qoida: bitli amallarda har doim qavslardan foydalanish shart!

## Ishlash natijasi:
```text
res1: 7, res2: 9
xato: 40, togri: 12
```

---

# 84-Topshiriq: Ternary operatori (shart ? ifoda1 : ifoda2)

## Topshiriq sharti:
Ternary operatori orqali do'konda chegirma hisoblash kodini yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    double summa = 120.0;
    // Agar summa 100 dan oshsa 10% chegirma, aks holda chegirmasiz
    double chegirma = (summa > 100.0) ? (summa * 0.10) : 0.0;
    double yakuniy = summa - chegirma;

    printf("Boshlang'ich summa: %.2f\n", summa);
    printf("Chegirma: %.2f\n", chegirma);
    printf("To'lov: %.2f\n", yakuniy);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Uchlik (ternary) operatori C dagi yagona 3 ta operand qabul qiluvchi operatordir.
2. U `if-else` konstruktsiyasining ifoda ko'rinishi bo'lib, o'zgaruvchiga qiymat biriktirishda to'g'ridan-to'g'ri ishlatiladi.

## Ishlash natijasi:
```text
Boshlang'ich summa: 120.00
Chegirma: 12.00
To'lov: 108.00
```

---

# 85-Topshiriq: Murakkab shartli ternary zanjirlari

## Topshiriq sharti:
Ballga qarab baho harfini (A, B, C, F) ternary zanjiri orqali aniqlang.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int ball = 78;
    char baho = (ball >= 90) ? 'A' :
                (ball >= 80) ? 'B' :
                (ball >= 70) ? 'C' : 'F';

    printf("Ball: %d, Baho: %c\n", ball, baho);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ternary operatorlarini zanjirband qilib ketma-ket ulash mumkin.
2. Kod ixcham bo'ladi, lekin haddan tashqari ko'p zanjirlar kod o'qilishini qiyinlashtirishi sababli me'yorda qo'llanilishi kerak.

## Ishlash natijasi:
```text
Ball: 78, Baho: C
```

---

# 86-Topshiriq: Butun sonlarda to'lib ketishni (Integer Overflow) oldindan sezish

## Topshiriq sharti:
Ikki int sonini qo'shishdan oldin overflow bo'lishini xavfsiz tekshiring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <limits.h>
#include <stdbool.h>

bool xavfsiz_qoshish(int a, int b, int *natija) {
    if ((b > 0 && a > INT_MAX - b) || (b < 0 && a < INT_MIN - b)) {
        return false; // To'lib ketish yuz beradi!
    }
    *natija = a + b;
    return true;
}

int main(void) {
    int x = INT_MAX - 5;
    int y = 10;
    int res;

    if (xavfsiz_qoshish(x, y, &res)) {
        printf("Natija: %d\n", res);
    } else {
        printf("XATO: Qo'shishda INT_MAX chegarasidan oshib ketadi!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Signed sonlar chegaradan oshganda C standartiga ko'ra Undefined Behavior (noaniq holat) yuz beradi.
2. `a + b > INT_MAX` deb tekshirib bo'lmaydi, chunki `a + b` ning o'zi allaqachon to'lib ketgan bo'ladi!
3. To'g'ri tekshirish: `a > INT_MAX - b` algebraik qoidasidan foydalanishdir.

## Ishlash natijasi:
```text
XATO: Qo'shishda INT_MAX chegarasidan oshib ketadi!
```

---

# 87-Topshiriq: Sonni n-chi karralisiga yuqoriga tekislash (Alignment: (x + a - 1) & ~(a - 1))

## Topshiriq sharti:
Xotira manzilini 8 bayt yoki 64 bayt chegarasiga tekislash formulasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

size_t tekisla(size_t son, size_t alignment) {
    return (son + alignment - 1) & ~(alignment - 1);
}

int main(void) {
    size_t xotira_talabi = 35;
    size_t tekislangan_8 = tekisla(xotira_talabi, 8);
    size_t tekislangan_64 = tekisla(xotira_talabi, 64);

    printf("Asl hajm: %zu bayt\n", xotira_talabi);
    printf("8-baytga tekislangan: %zu bayt\n", tekislangan_8);
    printf("64-baytga tekislangan: %zu bayt\n", tekislangan_64);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. CPU xotirani o'qishda 8 yoki 64 bayt (kesh liniyasi) chegarasiga to'g'irlangan ma'lumotlarni ancha tez o'qiydi.
2. Agar `alignment` 2 ning darajasi bo'lsa, `~(alignment - 1)` eng pastki bitlarni tozalovchi niqob hosil qiladi.
3. 35 soni 8 ga karrali yuqoridagi 40 ga, 64 ga karrali yuqoridagi 64 ga aylanadi.

## Ishlash natijasi:
```text
Asl hajm: 35 bayt
8-baytga tekislangan: 40 bayt
64-baytga tekislangan: 64 bayt
```

---

# 88-Topshiriq: 32-bitli sonning baytlari tartibini teskarilash (Byte Swap / Endianness)

## Topshiriq sharti:
Bitli surish va niqoblash orqali 32-bitli son baytlarini teskari o'giring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

uint32_t byte_swap32(uint32_t x) {
    return ((x & 0x000000FF) << 24) |
           ((x & 0x0000FF00) << 8)  |
           ((x & 0x00FF0000) >> 8)  |
           ((x & 0xFF000000) >> 24);
}

int main(void) {
    uint32_t son = 0x12345678;
    uint32_t teskari = byte_swap32(son);

    printf("Asl son:    0x%08X\n", son);
    printf("Almashgani: 0x%08X\n", teskari);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Tarmoq protokollari (TCP/IP) Big-Endian formatidan, x86/ARM protsessorlar esa Little-Endian formatidan foydalanadi.
2. Baytlarni almashtirish uchun har bir bayt o'zining mos niqobi bilan ajratilib, yangi joyiga suriladi va `|` bilan birlashtiriladi.

## Ishlash natijasi:
```text
Asl son:    0x12345678
Almashgani: 0x78563412
```

---

# 89-Topshiriq: Paritet (Parity bit) — 1 lar sonining juft yoki toqligini hisoblash

## Topshiriq sharti:
Ma'lumotlar uzatishdagi xatoliklarni tekshiruvchi paritet bitini toping.

## Yechim (C kodi):
```c
#include <stdio.h>

int hisobla_paritet(unsigned char bayt) {
    // Agar 1 lar soni toq bo'lsa 1, juft bo'lsa 0 qaytaradi
    int p = 0;
    while (bayt) {
        p ^= (bayt & 1);
        bayt >>= 1;
    }
    return p;
}

int main(void) {
    unsigned char b1 = 0x07; // 00000111 (3 ta 1 -> toq, paritet 1)
    unsigned char b2 = 0x0F; // 00001111 (4 ta 1 -> juft, paritet 0)

    printf("0x%02X pariteti: %d\n", b1, hisobla_paritet(b1));
    printf("0x%02X pariteti: %d\n", b2, hisobla_paritet(b2));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Paritet biti UART yoki xotira xatolarini aniqlashda qo'shiladigan qo'shimcha nazorat bitidir.
2. Har bir 1-bit XOR qilinganda, XOR ning xossasiga ko'ra toq sonli 1-lar 1 ni, juft sonli 1-lar 0 ni qoldiradi.

## Ishlash natijasi:
```text
0x07 pariteti: 1
0x0F pariteti: 0
```

---

# 90-Topshiriq: Gray kodi va binar songa o'zaro konvertatsiya

## Topshiriq sharti:
Binar sonni Gray kodiga va qayta binar songa o'giruvchi funksiya yozing.

## Yechim (C kodi):
```c
#include <stdio.h>

unsigned int binary_to_gray(unsigned int n) {
    return n ^ (n >> 1);
}

unsigned int gray_to_binary(unsigned int g) {
    unsigned int b = 0;
    for (; g; g >>= 1) {
        b ^= g;
    }
    return b;
}

int main(void) {
    unsigned int son = 13; // 1101 binar
    unsigned int gray = binary_to_gray(son);
    unsigned int orqaga = gray_to_binary(gray);

    printf("Asl son: %u\n", son);
    printf("Gray kodi: %u\n", gray);
    printf("Qayta binar: %u\n", orqaga);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Gray kodi shunday ketma-ketlikki, har bir keyingi son avvalgisidan faqatgina 1 ta bit o'zgarishi bilan farq qiladi.
2. Bu aylanuvchi enkoderlarda (rotary encoders) va apparat datchiklarida xatoliklarni bartaraf qilish uchun qo'llaniladi.
3. `n ^ (n >> 1)` formulasi binar sonni darhol Gray kodiga aylantiradi.

## Ishlash natijasi:
```text
Asl son: 13
Gray kodi: 11
Qayta binar: 13
```

---

# 91-Topshiriq: Bir nechta boolean bayroqni bitta baytda bitmask bilan boshqarish

## Topshiriq sharti:
Bitta uint8_t ichida 4 xil holatni saqlang va boshqaring.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#define FLAG_FAOL     (1 << 0) // 0x01
#define FLAG_ADMIN    (1 << 1) // 0x02
#define FLAG_TASDIQ   (1 << 2) // 0x04
#define FLAG_BLOKLANGAN (1 << 3) // 0x08

int main(void) {
    uint8_t foydalanuvchi = 0;

    // Faol va Tasdiqlangan bayroqlarini yoqish
    foydalanuvchi |= (FLAG_FAOL | FLAG_TASDIQ);

    printf("Foydalanuvchi bayroqlari: 0x%02X\n", foydalanuvchi);

    if (foydalanuvchi & FLAG_FAOL) {
        printf("Foydalanuvchi faol.\n");
    }
    if (!(foydalanuvchi & FLAG_ADMIN)) {
        printf("Foydalanuvchi admin emas.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 4 ta alohida boolean o'zgaruvchi 4 bayt xotira olgan bo'lardi.
2. Bitmasklar yordamida bitta 1 baytli o'zgaruvchida 8 tagacha turli bayroqni saqlash mumkin.
3. Bu operatsion tizim yadrolari (Linux task flags) va o'yin dvigatellarida standart amaliyotdir.

## Ishlash natijasi:
```text
Foydalanuvchi bayroqlari: 0x05
Foydalanuvchi faol.
Foydalanuvchi admin emas.
```

---

# 92-Topshiriq: Fayl ruxsat tizimini (Read, Write, Execute) bitlar bilan modellashtirish

## Topshiriq sharti:
Faylga o'qish, yozish va bajarish huquqlarini berish va tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define RUXSAT_OQISH   4 // 100 binar
#define RUXSAT_YOZISH  2 // 010 binar
#define RUXSAT_IJRO    1 // 001 binar

int main(void) {
    int ruxsat = RUXSAT_OQISH | RUXSAT_YOZISH; // 6 (rw-)

    printf("Joriy ruxsat: %d\n", ruxsat);

    if (ruxsat & RUXSAT_OQISH)  printf("O'qish mumkin.\n");
    if (ruxsat & RUXSAT_YOZISH) printf("Yozish mumkin.\n");
    if (ruxsat & RUXSAT_IJRO)   printf("Ijro etish mumkin.\n");
    else                        printf("Ijro etish man etilgan!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Unix fayl tizimidagi `chmod 755` aynan mana shu bitli mantiq asosida ishlaydi (4=Read, 2=Write, 1=Execute).
2. Bitli `&` orqali muayyan ruxsat bor-yo'qligi bir zumda tekshiriladi.

## Ishlash natijasi:
```text
Joriy ruxsat: 6
O'qish mumkin.
Yozish mumkin.
Ijro etish man etilgan!
```

---

# 93-Topshiriq: Bitlarni aylanma surish (Circular Bit Shift / Rotation: ROL va ROR)

## Topshiriq sharti:
8-bitli sonni chapga aylanma suruvchi (Rotate Left) funksiya yozing.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

uint8_t rotl8(uint8_t val, unsigned int count) {
    count %= 8;
    return (val << count) | (val >> (8 - count));
}

int main(void) {
    uint8_t son = 0x81; // 10000001
    uint8_t surilgan = rotl8(son, 1); // 00000011 (0x03)

    printf("Boshlang'ich: 0x%02X\n", son);
    printf("1 ta chapga aylanma surilgach: 0x%02X\n", surilgan);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oddiy surishda chetdan chiqqan bitlar yo'qoladi, aylanma surishda esa chapdan chiqqan bit o'ng tomondan qayta kiradi.
2. `(val << count) | (val >> (8 - count))` formulasi buni hech qanday shartlarsiz amalga oshiradi.
3. Kriptografik hash funksiyalarida (SHA-256, MD5) aylanma surish muhim qadam hisoblanadi.

## Ishlash natijasi:
```text
Boshlang'ich: 0x81
1 ta chapga aylanma surilgach: 0x03
```

---

# 94-Topshiriq: Sonning juft/toqligini tekshirishda (x & 1) ning afzalligi

## Topshiriq sharti:
Bitli tekshiruvning manfiy sonlarda ham qanday xatosiz ishlashini ko'rsating.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int musbat_toq = 7;
    int manfiy_toq = -7;

    printf("musbat_toq %% 2 = %d, (musbat_toq & 1) = %d\n", 
           musbat_toq % 2, musbat_toq & 1);
    printf("manfiy_toq %% 2 = %d, (manfiy_toq & 1) = %d\n", 
           manfiy_toq % 2, manfiy_toq & 1);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C da manfiy toq sonni 2 ga bo'lganda qoldiq `-1` chiqadi, shuning uchun `if (n % 2 == 1)` xato ishlashi mumkin.
2. `(n & 1)` esa har doim eng quyi bitni tekshiradi va barcha toq sonlar uchun (musbat yoki manfiy bo'lishidan qat'i nazar) har doim aniq `1` qaytaradi.
3. Qolaversa, bitli VA bo'lish amalidan ancha tez bajariladi.

## Ishlash natijasi:
```text
musbat_toq % 2 = 1, (musbat_toq & 1) = 1
manfiy_toq % 2 = -1, (manfiy_toq & 1) = 1
```

---

# 95-Topshiriq: Yon ta'sirlar (Side effects) va tartib kafolatlari

## Topshiriq sharti:
Funksiya chaqiruvlari oralig'idagi vergul va mantiqiy operatorlar tartibini tahlil qiling.

## Yechim (C kodi):
```c
#include <stdio.h>

int hisoblagich = 0;

int oshir(void) {
    return ++hisoblagich;
}

int main(void) {
    // Mantiqiy && qisqa tutashuvi tufayli ikkinchi funksiya chaqiriladimi?
    if (0 && oshir()) {
        // Ishlamaydi
    }
    printf("1-holatdan so'ng hisoblagich: %d\n", hisoblagich);

    if (1 || oshir()) {
        // Birinchi qism rost bo'lgani uchun oshir() yana chaqirilmaydi!
    }
    printf("2-holatdan so'ng hisoblagich: %d\n", hisoblagich);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yon ta'sir (side effect) bu ifodani hisoblash jarayonida o'zgaruvchining qiymati o'zgarishi yoki xotiraga yozilishidir.
2. `&&` va `||` operatorlarida qisqa tutashuv tufayli o'ng tomondagi ifodaning yon ta'siri sodir bo'lmasligi mumkin.
3. Bu qoidani bilmaslik murakkab mantiqiy xatoliklarga olib keladi.

## Ishlash natijasi:
```text
1-holatdan so'ng hisoblagich: 0
2-holatdan so'ng hisoblagich: 0
```

---

# 96-Topshiriq: i = i++ xatosi va noaniq xatti-harakat (Undefined Behavior)

## Topshiriq sharti:
Nima uchun bitta ifodada bitta o'zgaruvchini bir necha bor o'zgartirish qat'iyan man etilishini tushuntiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int i = 5;
    // XAVFLI: i = i++; yoki a[i] = i++;
    // Bu C standartida Undefined Behavior (UB) hisoblanadi!
    
    // To'g'ri va xavfsiz uslub:
    i++;
    printf("Xavfsiz oshirilgan i: %d\n", i);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C standartida ketma-ketlik nuqtalari (Sequence points) qoidasi mavjud: bitta o'zgaruvchini bitta ifoda ichida birdan ortiq o'zgartirish mumkin emas.
2. Har xil kompilyatorlar (GCC, Clang, MSVC) `i = i++` ifodasiga har xil natija berishi yoki optimallashtirishda kodni butunlay buzib yuborishi mumkin.
3. Qat'iy qoida: inkrement yoki dekrementni o'zlashtirish bilan bir qatorda aralashtirmang!

## Ishlash natijasi:
```text
Xavfsiz oshirilgan i: 6
```

---

# 97-Topshiriq: Bo'lish amalini o'ngga surish bilan almashtirishda manfiy sonlar o'ziga xosligi

## Topshiriq sharti:
Manfiy sonlarda / 2 va >> 1 natijalarini solishtiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int manfiy = -5;

    int bolish_natijasi = manfiy / 2; // -2 (nolga qarab yaxlitlanadi)
    int surish_natijasi = manfiy >> 1; // -3 (manfiy cheksizlikka qarab yaxlitlanadi)

    printf("-5 / 2  = %d\n", bolish_natijasi);
    printf("-5 >> 1 = %d\n", surish_natijasi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. C99 standartiga ko'ra butun sonli bo'lish `/` nolga qarab yaxlitlanadi (`-5 / 2 = -2`).
2. O'ngga surish `>>` esa manfiy cheksizlik tomonga yaxlitlanadi (floor: `-5 >> 1 = -3`).
3. Shuning uchun manfiy sonlarni 2 ga bo'lishda `>>` ni ehtiyotkorlik bilan ishlatish kerak.

## Ishlash natijasi:
```text
-5 / 2  = -2
-5 >> 1 = -3
```

---

# 98-Topshiriq: Satr harflarini bitli amal orqali kichik harfga o'tkazish (c | 0x20)

## Topshiriq sharti:
Katta harfni bitli YOKI amali orqali kichik harfga aylantiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char katta = 'G'; // ASCII 71 (01000111)
    // 5-bitni yoqish orqali kichik harfga o'tish (0x20 = 32 = 00100000)
    char kichik = katta | 0x20; // 01100111 (103 = 'g')

    printf("Katta harf: %c\n", katta);
    printf("Kichik harf (bitli | bilan): %c\n", kichik);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ASCII jadvalida lotin bosh harflari va kichik harflari faqatgina 5-bitning (qiymati 32) holati bilan farqlanadi.
2. `c | 0x20` amali bu 5-bitni har doim 1 qiladi, natijada katta harf avtomatik kichik harfga aylanadi.
3. Bu shartli `if` siz va tezkor usuldir.

## Ishlash natijasi:
```text
Katta harf: G
Kichik harf (bitli | bilan): g
```

---

# 99-Topshiriq: Satr harflarini bitli amal orqali katta harfga o'tkazish (c & ~0x20)

## Topshiriq sharti:
Kichik harfni bitli VA amali orqali katta harfga aylantiring.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    char kichik = 'w'; // ASCII 119
    // 5-bitni tozalash orqali katta harfga o'tish (~0x20)
    char katta = kichik & ~0x20;

    printf("Kichik harf: %c\n", kichik);
    printf("Katta harf (bitli & bilan): %c\n", katta);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. `~0x20` niqobi 5-bitdan tashqari barcha bitlari 1 bo'lgan qiymatni beradi.
2. `c & ~0x20` amali belgining 5-bitini 0 ga aylantiradi, natijada kichik harf katta harfga aylanadi.

## Ishlash natijasi:
```text
Kichik harf: w
Katta harf (bitli & bilan): W
```

---

# 100-Topshiriq: Bitlar, mantiq va arifmetikani birlashtiruvchi mini shifrlash (XOR cipher) dasturi

## Topshiriq sharti:
Satrni kalit (key) yordamida XOR bilan shifrlab, so'ngra qayta tiklang.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void xor_shifrlash(char *matn, char kalit) {
    for (size_t i = 0; matn[i] != '\0'; i++) {
        matn[i] ^= kalit;
    }
}

int main(void) {
    char xabar[] = "Maxfiy_C_Kodi";
    char kalit = 0x5A;

    printf("Asl xabar: %s\n", xabar);

    xor_shifrlash(xabar, kalit);
    printf("Shifrlangan binar holat (matn sifatida): %s\n", xabar);

    xor_shifrlash(xabar, kalit);
    printf("Qayta tiklangan asl xabar: %s\n", xabar);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. XOR shifrlash (Symmetric cipher) simmetrik shifrlashning eng sodda va poydevor shaklidir.
2. Bitta funksiyaning o'zi ham shifrlash, ham shifrdan chiqarish vazifasini bajaradi, chunki `(matn ^ kalit) ^ kalit = matn`.
3. Bu topshiriq 2-qismda o'rganilgan barcha arifmetik, mantiqiy va bitli tushunchalarni mustahkamlaydi.

## Ishlash natijasi:
```text
Asl xabar: Maxfiy_C_Kodi
Shifrlangan binar holat (matn sifatida): o[RPLCT]qUZE
Qayta tiklangan asl xabar: Maxfiy_C_Kodi
```

---
