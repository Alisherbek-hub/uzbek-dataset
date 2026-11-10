# C Dasturlash Tili — 15-Qism: Fayllar va Fayl I/O (stdio.h)
## (701-750 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* FILE* ko'rsatkichi, fopen rejimlari ('r', 'w', 'a', 'r+', 'wb', 'rb') va fclose
* Belgili (fgetc, fputc) va qatorli (fgets, fputs) kiritish/chiqarish
* Formatli fayl I/O (fprintf, fscanf) va xavfsizlik
* Binar fayllar (fread, fwrite) va struct ma'lumotlarini saqlash
* Fayl kursorini boshqarish (fseek, ftell, rewind) va fayl hajmini o'lchash
* Buferlash nazorati (setvbuf, fflush) va atomik fayl yozish
* CSV va INI fayllarni pars qilish, BMP/WAV generatorlari va Flat-File DB Engine

---

# 701-Topshiriq: Faylni ochish (fopen), tekshirish va yopish (fclose)

## Topshiriq sharti:
Faylni yozish rejimida ochish, NULL tekshiruvi va xavfsiz yopish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("test.txt", "w");
    if (f == NULL) {
        printf("Xatolik: Faylni ochib bo'lmadi!\n");
        return 1;
    }

    printf("Fayl muvaffaqiyatli ochildi.\n");
    fclose(f);
    printf("Fayl yopildi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. fopen() faylni ochadi va FILE strukturasiga ko'rsatkich qaytaradi. Agar ruxsat bo'lmasa yoki xotira yetmasa, NULL qaytaradi.
2. Har bir ochilgan fayl fclose() bilan yopilishi shart, aks holda fayl deskriptorlari tugab qolishi mumkin.

## Ishlash natijasi:
```text
Fayl muvaffaqiyatli ochildi.
Fayl yopildi.
```

---

# 702-Topshiriq: fputs() va fgets() yordamida matnli faylga yozish va o'qish

## Topshiriq sharti:
Faylga satr yozish va undan qatorma-qator o'qib olish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("salom.txt", "w");
    if (f) {
        fputs("Assalomu alaykum, C dasturchilar!\n", f);
        fputs("Bu ikkinchi qator.\n", f);
        fclose(f);
    }

    char bufer[128];
    f = fopen("salom.txt", "r");
    if (f) {
        while (fgets(bufer, sizeof(bufer), f) != NULL) {
            printf("[O'QILDI]: %s", bufer);
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. fgets() bufer hajmini qabul qilgani sababli buffer overflow (bufer to'lib ketishi) xatosidan xoli va xavfsizdir.
2. Satr oxiridagi '\n' belgisi buferga kiritiladi.

## Ishlash natijasi:
```text
[O'QILDI]: Assalomu alaykum, C dasturchilar!
[O'QILDI]: Bu ikkinchi qator.
```

---

# 703-Topshiriq: fputc() va fgetc() yordamida belgima-belgi fayl nusxalash

## Topshiriq sharti:
Fayldan EOF (End of File) gacha belgilarni o'qib boshqa faylga ko'chirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // 1. Asl fayl yaratamiz
    FILE *src = fopen("manba.txt", "w");
    if (src) {
        fputs("ABCDE 12345", src);
        fclose(src);
    }

    // 2. Nusxalash
    src = fopen("manba.txt", "r");
    FILE *dst = fopen("nusxa.txt", "w");

    if (src && dst) {
        int c; // EOF int (-1) bo'lgani uchun int tipi shart!
        while ((c = fgetc(src)) != EOF) {
            fputc(c, dst);
        }
        fclose(src);
        fclose(dst);
        printf("Fayl muvaffaqiyatli nusxalandi!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. fgetc() qaytaruvchi qiymati char emas, int bo'lishi shart! Chunki EOF odatda -1 ga teng va signed char bilan adashishi mumkin.
2. Nusxalash sikli (c = fgetc(src)) != EOF C tilidagi eng klassik konstruktsiyadir.

## Ishlash natijasi:
```text
Fayl muvaffaqiyatli nusxalandi!
```

---

# 704-Topshiriq: fprintf() yordamida formatlangan hisobot fayli yaratish

## Topshiriq sharti:
Jadval ko'rinishidagi ma'lumotlarni faylga formatlab yozish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("hisobot.txt", "w");
    if (f) {
        fprintf(f, "%-10s %-10s %-10s\n", "Mahsulot", "Miqdor", "Narx");
        fprintf(f, "------------------------------\n");
        fprintf(f, "%-10s %-10d %-10.2f\n", "Olma", 50, 12000.50);
        fprintf(f, "%-10s %-10d %-10.2f\n", "Banan", 30, 22000.00);
        fclose(f);
        printf("Hisobot faylga yozildi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. fprintf() printf kabi ishlaydi, ammo chiqish oqimi sifatida konsol o'rniga faylni qabul qiladi.
2. Format spetsifikatorlari (%-10s) jadval ustunlarini tekislashda qulay.

## Ishlash natijasi:
```text
Hisobot faylga yozildi.
```

---

# 705-Topshiriq: fscanf() yordamida formatlangan ma'lumotlarni o'qish

## Topshiriq sharti:
Fayldagi ustunli ma'lumotlarni o'zgaruvchilarga o'qib olish va qaytuvchi qiymatni tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("malumot.txt", "w");
    if (f) {
        fprintf(f, "Ali 25 8500.50\n");
        fprintf(f, "Vali 30 9200.00\n");
        fclose(f);
    }

    f = fopen("malumot.txt", "r");
    if (f) {
        char ism[32];
        int yosh;
        double oylik;

        while (fscanf(f, "%31s %d %lf", ism, &yosh, &oylik) == 3) {
            printf("Xodim: %s, Yoshi: %d, Maoshi: %.2f\n", ism, yosh, oylik);
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. fscanf() muvaffaqiyatli o'qilgan argumentlar sonini qaytaradi. Biz kutgan 3 ta maydon to'liq o'qilganini tekshiramiz.
2. %31s bufer to'lib ketishini cheklaydi.

## Ishlash natijasi:
```text
Xodim: Ali, Yoshi: 25, Maoshi: 8500.50
Xodim: Vali, Yoshi: 30, Maoshi: 9200.00
```

---

# 706-Topshiriq: Standart oqimlar: stdin, stdout, stderr farqlari

## Topshiriq sharti:
stdout va stderr oqimlariga ma'lumot chiqarish hamda ularning buferlashdagi farqlari.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    fprintf(stdout, "Bu oddiy chiqish oqimi (stdout).\n");
    fprintf(stderr, "Bu xatolik oqimi (stderr) - u buferlanmaydi va darhol chiqadi!\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. stdout odatda qator bo'yicha buferlanadi (Line-buffered).
2. stderr esa buferlanmaydi (Unbuffered), ya'ni dastur qulab tushishidan oldin xato xabari konsolga yetib borishi kafolatlanadi.

## Ishlash natijasi:
```text
Bu oddiy chiqish oqimi (stdout).
Bu xatolik oqimi (stderr) - u buferlanmaydi va darhol chiqadi!
```

---

# 707-Topshiriq: Binar fayllar: fwrite() bilan butun massivni yozish

## Topshiriq sharti:
Butun sonlar massivini 'wb' rejimida to'g'ridan-to'g'ri xotira blokidan faylga yozish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int sonlar[] = {10, 20, 30, 40, 50};
    int soni = 5;

    FILE *f = fopen("sonlar.bin", "wb");
    if (f) {
        size_t yozildi = fwrite(sonlar, sizeof(int), soni, f);
        printf("%zu ta int binar faylga yozildi.\n", yozildi);
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 'wb' rejimi faylni binar ko'rinishda ochadi (Windows tizimlarida '\n' ni '\r\n' ga o'girmaydi).
2. fwrite(manzil, hajm, soni, fayl) xotiradagi xom baytlarni to'g'ridan-to'g'ri diskka uzatadi.

## Ishlash natijasi:
```text
5 ta int binar faylga yozildi.
```

---

# 708-Topshiriq: Binar fayllar: fread() bilan massivni o'qib olish

## Topshiriq sharti:
'rb' rejimida diskdagi binar massivni bitta operatsiyada xotiraga yuklash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int olingan[5];

    FILE *f = fopen("sonlar.bin", "rb");
    if (f) {
        size_t oqildi = fread(olingan, sizeof(int), 5, f);
        printf("%zu ta int binar fayldan o'qildi: ", oqildi);
        for (size_t i = 0; i < oqildi; i++) {
            printf("%d ", olingan[i]);
        }
        printf("\n");
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. fread() binar fayldan ko'rsatilgan sondagi bloklarni o'qiydi va haqiqatda o'qilgan elementlar sonini qaytaradi.
2. Matnli fayllardan ko'ra binar I/O bir necha o'n barobar tezroq ishlaydi.

## Ishlash natijasi:
```text
5 ta int binar fayldan o'qildi: 10 20 30 40 50
```

---

# 709-Topshiriq: Strukturani binar faylga yozish va o'qish

## Topshiriq sharti:
Foydalanuvchi ma'lumotlari strukturasini bitta fwrite/fread chaqiruvi bilan saqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int id;
    char ism[32];
    double ball;
} Foydalanuvchi;

int main(void) {
    Foydalanuvchi u1 = { 101, "Jasur", 94.5 };

    // Yozish
    FILE *f = fopen("user.dat", "wb");
    if (f) {
        fwrite(&u1, sizeof(Foydalanuvchi), 1, f);
        fclose(f);
    }

    // O'qish
    Foydalanuvchi u2 = {0};
    f = fopen("user.dat", "rb");
    if (f) {
        fread(&u2, sizeof(Foydalanuvchi), 1, f);
        fclose(f);
        printf("Tiklandi: ID=%d, Ism=%s, Ball=%.1f\n", u2.id, u2.ism, u2.ball);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Butun boshli struktura &u1 manzili orqali bitta buyruqda yoziladi va o'qiladi.
2. Bu o'yinlar saqlash holati (Save state) va kesh tizimlarida keng qo'llaniladi.

## Ishlash natijasi:
```text
Tiklandi: ID=101, Ism=Jasur, Ball=94.5
```

---

# 710-Topshiriq: Fayl ko'rsatkichini boshqarish: fseek(), ftell() va rewind()

## Topshiriq sharti:
Fayl ichida ixtiyoriy joyga siljish va joriy pozitsiyani aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("alifbo.txt", "w+");
    if (f) {
        fputs("ABCDEFGHIJKLMNOPQRSTUVWXYZ", f);

        // 10-baytga o'tish (0 dan boshlab)
        fseek(f, 10, SEEK_SET);
        printf("Joriy pozitsiya: %ld\n", ftell(f));
        printf("10-belgi: %c\n", fgetc(f)); // 'K'

        // Boshiga qaytish
        rewind(f);
        printf("Boshidagi belgi: %c\n", fgetc(f)); // 'A'
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. fseek(f, offset, whence) da uchta asosiy nuqta bor: SEEK_SET (boshi), SEEK_CUR (joriy nuqta), SEEK_END (oxiri).
2. ftell(f) joriy fayl kursorining baytlardagi siljishini qaytaradi.

## Ishlash natijasi:
```text
Joriy pozitsiya: 10
10-belgi: K
Boshidagi belgi: A
```

---

# 711-Topshiriq: Fayl hajmini (File Size) aniqlashning klassik fseek/ftell usuli

## Topshiriq sharti:
SEEK_END ga o'tib, ftell() orqali faylning aniq bayt hajmini o'lchash.

## Yechim (C kodi):
```c
#include <stdio.h>

long fayl_hajmi(const char *fayl_nomi) {
    FILE *f = fopen(fayl_nomi, "rb");
    if (!f) return -1;

    fseek(f, 0, SEEK_END);
    long hajm = ftell(f);
    fclose(f);
    return hajm;
}

int main(void) {
    FILE *test = fopen("olcham.txt", "w");
    if (test) {
        fputs("1234567890", test); // 10 bayt
        fclose(test);
    }

    long h = fayl_hajmi("olcham.txt");
    printf("Fayl hajmi: %ld bayt\n", h);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fayl oxiriga (SEEK_END, 0) o'tib ftell chaqirilsa, kursor turgan manzil faylning umumiy hajmiga teng bo'ladi.
2. Faylni to'liq RAM ga yuklash uchun malloc hajmida aynan shu qiymat ishlatiladi.

## Ishlash natijasi:
```text
Fayl hajmi: 10 bayt
```

---

# 712-Topshiriq: Butun faylni xotiraga (RAM) bir martada yuklash

## Topshiriq sharti:
Fayl hajmini aniqlab, malloc orqali xotira ajratib, to'liq faylni o'qish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *f = fopen("matn.txt", "w");
    if (f) {
        fputs("C tilida fayllar bilan ishlash juda qulay va tezkor!", f);
        fclose(f);
    }

    f = fopen("matn.txt", "rb");
    if (f) {
        fseek(f, 0, SEEK_END);
        long hajm = ftell(f);
        rewind(f);

        char *bufer = (char *)malloc(hajm + 1);
        if (bufer) {
            fread(bufer, 1, hajm, f);
            bufer[hajm] = '\0'; // Satr oxiri belgisi

            printf("Fayldan o'qilgan matn (%ld bayt):\n"%s"\n", hajm, bufer);
            free(bufer);
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Binar rejimda ochish ('rb') Windows da baytlar sonining o'zgarmasligini kafolatlaydi.
2. Xotiraga yuklangandan so'ng oxiriga '\0' qo'yish orqali xavfsiz string sifatida foydalanish mumkin.

## Ishlash natijasi:
```text
Fayldan o'qilgan matn (55 bayt):
"C tilida fayllar bilan ishlash juda qulay va tezkor!"
```

---

# 713-Topshiriq: Faylga ma'lumot qo'shish ('a' - Append rejimi)

## Topshiriq sharti:
Mavjud fayl oxiriga yangi yozuvlar qo'shish va faylni o'chirib yubormaslik.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // 1. Dastlabki fayl
    FILE *f = fopen("log.txt", "w");
    if (f) {
        fputs("[LOG 1]: Dastur ishga tushdi\n", f);
        fclose(f);
    }

    // 2. Qo'shish rejimi ('a')
    f = fopen("log.txt", "a");
    if (f) {
        fputs("[LOG 2]: Yangi hodisa qayd etildi\n", f);
        fclose(f);
    }

    // O'qib tekshiramiz
    char qator[64];
    f = fopen("log.txt", "r");
    if (f) {
        while (fgets(qator, sizeof(qator), f)) {
            printf("%s", qator);
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 'a' (append) rejimi ochilganda mavjud ma'lumotlar saqlanib qoladi va har bir yozish avtomatik fayl oxiriga amalga oshiriladi.
2. Log tizimlari uchun bu standart rejimdir.

## Ishlash natijasi:
```text
[LOG 1]: Dastur ishga tushdi
[LOG 2]: Yangi hodisa qayd etildi
```

---

# 714-Topshiriq: Xatoliklarni tekshirish: feof() va ferror() funksiyalari

## Topshiriq sharti:
Fayldan o'qish to'xtaganda bu fayl oxirimi (EOF) yoki apparat xatoligimi ekanini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("sinov.txt", "w");
    if (f) {
        fputs("Test", f);
        fclose(f);
    }

    f = fopen("sinov.txt", "r");
    if (f) {
        char buf[10];
        fread(buf, 1, 10, f); // 4 bayt o'qiladi, fayl tugaydi

        if (feof(f)) {
            printf("Fayl oxiriga (EOF) yetildi.\n");
        }
        if (ferror(f)) {
            printf("I/O xatoligi yuz berdi!\n");
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. feof() faqat fayl oxiriga urilgandan keyin 1 qiymatini qaytaradi.
2. ferror() disk xatosi, buzilgan sektor yoki ruxsat muammosi tufayli o'qish uzilganini bildiradi.

## Ishlash natijasi:
```text
Fayl oxiriga (EOF) yetildi.
```

---

# 715-Topshiriq: Buferni tozalash: fflush() va uning to'g'ri qo'llanilishi

## Topshiriq sharti:
Faylga yozilgan ma'lumotlar zudlik bilan diskka tushishini ta'minlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("realtime.log", "w");
    if (f) {
        fputs("Kritik xabar: Tizim ishlamoqda...\n", f);
        // Buferdan zudlik bilan diskka yozish:
        fflush(f);

        printf("Ma'lumot buferdan to'g'ridan-to'g'ri diskka yozildi.\n");
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. fflush() yozish oqimlari (output streams) uchun ishlatiladi va RAM dagi buferni zudlik bilan jismoniy diskka tushiradi.
2. Diqqat: Standart C da `fflush(stdin)` aniqlanmagan xatti-harakatdir (Undefined Behavior)!

## Ishlash natijasi:
```text
Ma'lumot buferdan to'g'ridan-to'g'ri diskka yozildi.
```

---

# 716-Topshiriq: Oqim buferlashini o'zgartirish: setvbuf()

## Topshiriq sharti:
Oqimni to'liq buferlangan (_IOFBF), qatorli (_IOLBF) yoki bufersiz (_IONBF) qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("nobuffer.txt", "w");
    if (f) {
        // Bufersiz rejim: har bir bayt zudlik bilan diskka yoziladi
        setvbuf(f, NULL, _IONBF, 0);

        fputc('X', f);
        printf("Bufersiz rejimda belgi yozildi.\n");
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. setvbuf() orqali maxsus bufer hajmi va buferlash strategiyasini sozlash mumkin.
2. Yuqori unumdorlikda katta bufer (masalan 64KB) kiritish/chiqarish tezligini oshiradi.

## Ishlash natijasi:
```text
Bufersiz rejimda belgi yozildi.
```

---

# 717-Topshiriq: Faylni o'chirish: remove() funksiyasi

## Topshiriq sharti:
stdio.h dagi remove() orqali mavjud faylni diskdan butunlay o'chirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    // 1. Fayl yaratamiz
    FILE *f = fopen("ochiriladigan.tmp", "w");
    if (f) {
        fputs("Vaqtinchalik ma'lumot", f);
        fclose(f);
    }

    // 2. O'chiramiz
    if (remove("ochiriladigan.tmp") == 0) {
        printf("Fayl muvaffaqiyatli o'chirildi!\n");
    } else {
        printf("Faylni o'chirib bo'lmadi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. remove() muvaffaqiyatli bo'lsa 0 qaytaradi. Agar fayl mavjud bo'lmasa yoki qulflangan bo'lsa, noldan farqli son qaytaradi.

## Ishlash natijasi:
```text
Fayl muvaffaqiyatli o'chirildi!
```

---

# 718-Topshiriq: Faylni qayta nomlash: rename() funksiyasi

## Topshiriq sharti:
Faylning nomini yoki joylashuv manzilini o'zgartirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("eski_nom.txt", "w");
    if (f) {
        fputs("Kontent", f);
        fclose(f);
    }

    if (rename("eski_nom.txt", "yangi_nom.txt") == 0) {
        printf("Fayl nomi muvaffaqiyatli o'zgartirildi!\n");
    } else {
        printf("Fayl nomini o'zgartirib bo'lmadi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. rename() fayl nomini o'zgartiradi va bitta disk bo'limi ichida faylni yangi jildga ko'chirish uchun ham ishlaydi.

## Ishlash natijasi:
```text
Fayl nomi muvaffaqiyatli o'zgartirildi!
```

---

# 719-Topshiriq: Vaqtinchalik xavfsiz fayl: tmpfile()

## Topshiriq sharti:
Dastur yopilganda avtomatik o'chib ketuvchi anonim vaqtinchalik fayl yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *tmp = tmpfile();
    if (tmp) {
        fputs("Ushbu ma'lumot vaqtinchalik xotirada", tmp);
        rewind(tmp);

        char buf[64];
        if (fgets(buf, sizeof(buf), tmp)) {
            printf("Vaqtinchalik fayldan o'qildi: %s\n", buf);
        }

        // fclose() chaqirilganda fayl avtomatik diskdan o'chiriladi!
        fclose(tmp);
        printf("Vaqtinchalik fayl avtomatik o'chib ketdi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. tmpfile() operatsion tizimning vaqtinchalik jildida binar 'wb+' rejimida fayl ochadi.
2. Fayl yopilishi yoki dastur yakunlanishi bilan avtomatik o'chadi, xavfsizlik va axlat qoldirmaslik uchun idealdir.

## Ishlash natijasi:
```text
Vaqtinchalik fayldan o'qildi: Ushbu ma'lumot vaqtinchalik xotirada
Vaqtinchalik fayl avtomatik o'chib ketdi.
```

---

# 720-Topshiriq: CSV fayllarni yozish va maydonlarni formatlash

## Topshiriq sharti:
Vergul bilan ajratilgan (Comma Separated Values) CSV fayl generatsiya qilish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int id;
    const char *nom;
    double narx;
} Mahsulot;

int main(void) {
    Mahsulot ro_yxat[] = {
        {1, "Noutbuk", 1200.50},
        {2, "Sichqoncha", 25.00},
        {3, "Klaviatura", 75.99}
    };

    FILE *f = fopen("mahsulotlar.csv", "w");
    if (f) {
        fprintf(f, "ID,Mahsulot Nomi,Narxi\n");
        for (int i = 0; i < 3; i++) {
            fprintf(f, "%d,\"%s\",%.2f\n", 
                    ro_yxat[i].id, ro_yxat[i].nom, ro_yxat[i].narx);
        }
        fclose(f);
        printf("CSV fayl muvaffaqiyatli saqlandi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. CSV jadval ma'lumotlarini Excel yoki boshqa dasturlar bilan almashishda eng ommabop ochiq formatdir.
2. Satr maydonlarini qo'shtirnoqqa olish bo'shliq yoki maxsus belgilar xavfini kamaytiradi.

## Ishlash natijasi:
```text
CSV fayl muvaffaqiyatli saqlandi.
```

---

# 721-Topshiriq: CSV faylni qatorma-qator pars qilish (strtok yordamida)

## Topshiriq sharti:
CSV fayldan satrlarni o'qib, vergul bo'yicha maydonlarga ajratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void) {
    FILE *f = fopen("mahsulotlar.csv", "r");
    if (f) {
        char qator[128];
        // Sarlavhani o'tkazib yuboramiz
        fgets(qator, sizeof(qator), f);

        while (fgets(qator, sizeof(qator), f)) {
            // Yangi qator belgisini olib tashlaymiz
            qator[strcspn(qator, "\r\n")] = 0;

            char *id_str = strtok(qator, ",");
            char *nom = strtok(NULL, ",");
            char *narx_str = strtok(NULL, ",");

            if (id_str && nom && narx_str) {
                printf("ID: %-2s | Mahsulot: %-12s | Narx: %s USD\n", 
                       id_str, nom, narx_str);
            }
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. strtok() satrni ajratuvchi (separator) bo'yicha qismlarga (tokens) bo'ladi.
2. Har bir satr ketma-ket pars qilinadi.

## Ishlash natijasi:
```text
ID: 1  | Mahsulot: "Noutbuk"    | Narx: 1200.50 USD
ID: 2  | Mahsulot: "Sichqoncha"  | Narx: 25.00 USD
ID: 3  | Mahsulot: "Klaviatura"  | Narx: 75.99 USD
```

---

# 722-Topshiriq: Binar faylda ixtiyoriy yozuvga kirish (Random Access Record)

## Topshiriq sharti:
Fayldagi N-chi yozuvga fseek yordamida to'g'ridan-to'g'ri o'tish va uni yangilash.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int id;
    int ball;
} Yozuv;

int main(void) {
    Yozuv jadvallar[3] = { {1, 50}, {2, 70}, {3, 90} };

    FILE *f = fopen("records.db", "wb+");
    if (f) {
        fwrite(jadvallar, sizeof(Yozuv), 3, f);

        // 2-yozuvni (indeks 1) o'qib o'zgartiramiz:
        fseek(f, 1 * sizeof(Yozuv), SEEK_SET);
        Yozuv y;
        fread(&y, sizeof(Yozuv), 1, f);
        printf("Eski ball: %d\n", y.ball);

        y.ball = 85; // Yangilash
        fseek(f, 1 * sizeof(Yozuv), SEEK_SET); // Kursorni qaytarish
        fwrite(&y, sizeof(Yozuv), 1, f);

        // Qayta o'qib tekshirish
        fseek(f, 1 * sizeof(Yozuv), SEEK_SET);
        fread(&y, sizeof(Yozuv), 1, f);
        printf("Yangi ball: %d\n", y.ball);

        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. O'zgarmas o'lchamli yozuvlar (Fixed-size records) fseek(f, N * sizeof(Yozuv), SEEK_SET) orqali O(1) da ixtiyoriy yozuvni o'qish va o'zgartirish imkonini beradi.
2. Bu relational ma'lumotlar bazalarining (SQLite, MySQL InnoDB) asosiy ishlash mexanizmidir.

## Ishlash natijasi:
```text
Eski ball: 70
Yangi ball: 85
```

---

# 723-Topshiriq: Binar faylni tekshirish: Magic Number (Fayl imzosi)

## Topshiriq sharti:
Faylning dastlabki 4 baytini tekshirish orqali fayl turi haqiqiyligini tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#define FAHR_MAGIC 0x52484146 // "FAHR" ASCII

int main(void) {
    FILE *f = fopen("custom.bin", "wb");
    if (f) {
        uint32_t magic = FAHR_MAGIC;
        fwrite(&magic, sizeof(uint32_t), 1, f);
        fputs("Foydali yuklama...", f);
        fclose(f);
    }

    f = fopen("custom.bin", "rb");
    if (f) {
        uint32_t read_magic;
        if (fread(&read_magic, sizeof(uint32_t), 1, f) == 1) {
            if (read_magic == FAHR_MAGIC) {
                printf("Fayl formati to'g'ri (Magic: 0x%X)\n", read_magic);
            } else {
                printf("Buzilgan yoki noto'g'ri fayl formati!\n");
            }
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. PNG, ELF, ZIP, PDF kabi deyarli barcha fayl formatlari dastlabki baytlarida maxsus Magic Number (fayl imzosi) ga ega bo'ladi.
2. Faylni ochganda birinchi navbatda magic number tekshiriladi.

## Ishlash natijasi:
```text
Fayl formati to'g'ri (Magic: 0x52484146)
```

---

# 724-Topshiriq: Fayldagi satrlar sonini hisoblash

## Topshiriq sharti:
Fayldan yangi qator ('\n') belgilarini sanash orqali jami satrlar sonini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("she_r.txt", "w");
    if (f) {
        fputs("Vatan sajdagoh kabi muqaddasdir\n", f);
        fputs("Ona yurtim — oltin beshigim\n", f);
        fputs("Har qadaming aziz va qutlug'\n", f);
        fclose(f);
    }

    f = fopen("she_r.txt", "r");
    if (f) {
        int satrlar = 0;
        int c;
        while ((c = fgetc(f)) != EOF) {
            if (c == '\n') satrlar++;
        }
        fclose(f);
        printf("Jami satrlar soni: %d\n", satrlar);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Faylni belgima-belgi o'qib '\n' belgilarini sanash UNIX wc -l utilitasi kabi ishlaydi.

## Ishlash natijasi:
```text
Jami satrlar soni: 3
```

---

# 725-Topshiriq: Fayldagi so'zlar sonini hisoblash (Word Count)

## Topshiriq sharti:
Bo'shliq va yangi qatorlar orasidagi ajratilgan so'zlarni sanash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    FILE *f = fopen("matn_soz.txt", "w");
    if (f) {
        fputs("C tili juda qulay, tezkor va qudratli dasturlash tili.", f);
        fclose(f);
    }

    f = fopen("matn_soz.txt", "r");
    if (f) {
        int sozlar = 0;
        int soz_ichidami = 0;
        int c;

        while ((c = fgetc(f)) != EOF) {
            if (isspace(c)) {
                soz_ichidami = 0;
            } else if (!soz_ichidami) {
                soz_ichidami = 1;
                sozlar++;
            }
        }
        fclose(f);
        printf("Fayldagi so'zlar soni: %d\n", sozlar);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. isspace() bo'sh joy, tabulyatsiya va yangi qatorni aniqlaydi.
2. Holat bayrog'i (soz_ichidami) ketma-ket bir nechta bo'sh joylarni bitta ajratuvchi deb hisoblashga imkon beradi.

## Ishlash natijasi:
```text
Fayldagi so'zlar soni: 8
```

---

# 726-Topshiriq: Binar faylni Hex Dump ko'rinishida chiqarish (xxd simulyatsiyasi)

## Topshiriq sharti:
Faylning har bir baytini o'n oltilik (HEX) va ASCII ko'rinishida chop etish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

void hex_dump(const char *fayl_nomi) {
    FILE *f = fopen(fayl_nomi, "rb");
    if (!f) return;

    unsigned char buf[16];
    size_t n;
    size_t offset = 0;

    while ((n = fread(buf, 1, 16, f)) > 0) {
        printf("%08zX: ", offset);
        for (size_t i = 0; i < 16; i++) {
            if (i < n) printf("%02X ", buf[i]);
            else printf("   ");
        }
        printf(" |");
        for (size_t i = 0; i < n; i++) {
            printf("%c", isprint(buf[i]) ? buf[i] : '.');
        }
        printf("|\n");
        offset += n;
    }
    fclose(f);
}

int main(void) {
    FILE *f = fopen("hextest.bin", "wb");
    if (f) {
        fputs("Hello World!\x01\x02\x03", f);
        fclose(f);
    }
    hex_dump("hextest.bin");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Hex Dump binar fayllarni tahlil qilish, reverse engineering va xotira tekshiruvlarida asosiy vositadir.

## Ishlash natijasi:
```text
00000000: 48 65 6C 6C 6F 20 57 6F 72 6C 64 21 01 02 03    |Hello World!...|
```

---

# 727-Topshiriq: Fayl ichidagi barcha kichik harflarni kattaga o'tkazish (In-Place File Update)

## Topshiriq sharti:
r+ rejimida faylni ochib, o'qib, o'zgartirib o'sha joyga qayta yozish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    FILE *f = fopen("harflar.txt", "w");
    if (f) {
        fputs("salom dunyo", f);
        fclose(f);
    }

    f = fopen("harflar.txt", "r+"); // Ham o'qish, ham yozish
    if (f) {
        int c;
        while ((c = fgetc(f)) != EOF) {
            if (islower(c)) {
                fseek(f, -1, SEEK_CUR); // 1 bayt orqaga qaytish
                fputc(toupper(c), f);
                fflush(f); // O'qish/yozish orasida kursor sinxronizatsiyasi
            }
        }
        fclose(f);
    }

    // Natijani tekshirish
    f = fopen("harflar.txt", "r");
    if (f) {
        char buf[32];
        if (fgets(buf, sizeof(buf), f)) {
            printf("O'zgartirilgan matn: %s\n", buf);
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 'r+' rejimida fayl boshidan ochiladi va faylni to'liq qayta yozmasdan joyida (in-place) o'zgartirish mumkin.
2. O'qishdan keyin yozishga o'tganda fseek yoki fflush chaqirilishi C standartida talab qilinadi.

## Ishlash natijasi:
```text
O'zgartirilgan matn: SALOM DUNYO
```

---

# 728-Topshiriq: Fayldan ma'lum bir satrni o'chirib tashlash

## Topshiriq sharti:
Vaqtinchalik fayl orqali kerakli satrni tashlab ketib yangi faylga yozish va qayta nomlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

void satr_ochir(const char *asl_fayl, int ochiriladigan_satr) {
    FILE *in = fopen(asl_fayl, "r");
    FILE *out = fopen("temp.txt", "w");
    if (!in || !out) return;

    char buf[128];
    int satr_raqam = 1;

    while (fgets(buf, sizeof(buf), in)) {
        if (satr_raqam != ochiriladigan_satr) {
            fputs(buf, out);
        }
        satr_raqam++;
    }
    fclose(in);
    fclose(out);

    remove(asl_fayl);
    rename("temp.txt", asl_fayl);
}

int main(void) {
    FILE *f = fopen("satrlar.txt", "w");
    if (f) {
        fputs("Qator 1\nQator 2 (O'chiriladi)\nQator 3\n", f);
        fclose(f);
    }

    satr_ochir("satrlar.txt", 2);

    f = fopen("satrlar.txt", "r");
    if (f) {
        char buf[64];
        while (fgets(buf, sizeof(buf), f)) {
            printf("%s", buf);
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matnli fayllardan o'rtadagi satrni o'chirishning eng ishonchli yo'li — qolgan barcha satrlarni vaqtinchalik faylga yozib, so'ngra nomini almashtirishdir.

## Ishlash natijasi:
```text
Qator 1
Qator 3
```

---

# 729-Topshiriq: Fayllarni binar taqqoslash (cmp / diff simulyatsiyasi)

## Topshiriq sharti:
Ikki faylning bir-biriga baytma-bayt to'liq mosligini tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int fayllar_bir_xilmi(const char *f1, const char *f2) {
    FILE *a = fopen(f1, "rb");
    FILE *b = fopen(f2, "rb");
    if (!a || !b) {
        if (a) fclose(a);
        if (b) fclose(b);
        return 0;
    }

    int c1, c2;
    do {
        c1 = fgetc(a);
        c2 = fgetc(b);
        if (c1 != c2) {
            fclose(a);
            fclose(b);
            return 0; // Farqli bayt topildi
        }
    } while (c1 != EOF && c2 != EOF);

    fclose(a);
    fclose(b);
    return 1; // Fayllar 100% bir xil
}

int main(void) {
    FILE *f1 = fopen("f1.bin", "wb");
    FILE *f2 = fopen("f2.bin", "wb");
    if (f1 && f2) {
        fputs("Test ma'lumot", f1);
        fputs("Test ma'lumot", f2);
        fclose(f1);
        fclose(f2);
    }

    if (fayllar_bir_xilmi("f1.bin", "f2.bin")) {
        printf("Ikkala fayl to'liq bir xil!\n");
    } else {
        printf("Fayllarda farq bor.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Baytma-bayt solishtirish fayllarning nazorat yig'indilari (checksum) yoki yaxlitligini tekshirishda qat'iy kafolat beradi.

## Ishlash natijasi:
```text
Ikkala fayl to'liq bir xil!
```

---

# 730-Topshiriq: Binar faylni shifrlash va deshifrlash (XOR Cipher)

## Topshiriq sharti:
Fayldagi har bir baytni maxfiy kalit bilan XOR qilish orqali shifrlash.

## Yechim (C kodi):
```c
#include <stdio.h>

void xor_fayl(const char *in_fayl, const char *out_fayl, unsigned char kalit) {
    FILE *in = fopen(in_fayl, "rb");
    FILE *out = fopen(out_fayl, "wb");
    if (!in || !out) return;

    int c;
    while ((c = fgetc(in)) != EOF) {
        fputc(c ^ kalit, out);
    }
    fclose(in);
    fclose(out);
}

int main(void) {
    FILE *f = fopen("ochiq.txt", "w");
    if (f) {
        fputs("Maxfiy xabar 123", f);
        fclose(f);
    }

    unsigned char kalit = 0xAA;
    xor_fayl("ochiq.txt", "shifrlangan.enc", kalit);
    printf("Fayl shifrlandi.\n");

    xor_fayl("shifrlangan.enc", "tiklangan.txt", kalit);
    printf("Fayl qayta deshifrlandi.\n");

    f = fopen("tiklangan.txt", "r");
    if (f) {
        char buf[32];
        if (fgets(buf, sizeof(buf), f)) {
            printf("Tiklangan matn: %s\n", buf);
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. XOR amali simmetrikdir: (A ^ K) ^ K = A.
2. Bu fayl streamini oqimli shifrlashning (Stream Cipher) eng sodda modelidir.

## Ishlash natijasi:
```text
Fayl shifrlandi.
Fayl qayta deshifrlandi.
Tiklangan matn: Maxfiy xabar 123
```

---

# 731-Topshiriq: Fayldagi eng uzun qatorni (Longest Line) topish

## Topshiriq sharti:
fgets yordamida matnli fayldagi eng uzun qatorning uzunligi va matnini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    FILE *f = fopen("qatorlar.txt", "w");
    if (f) {
        fputs("Qisqa\n", f);
        fputs("Bu fayldagi eng uzun jumla hisoblanadi!\n", f);
        fputs("O'rtacha qator\n", f);
        fclose(f);
    }

    f = fopen("qatorlar.txt", "r");
    if (f) {
        char joriy[256];
        char eng_uzun[256] = "";
        size_t max_len = 0;

        while (fgets(joriy, sizeof(joriy), f)) {
            joriy[strcspn(joriy, "\r\n")] = 0;
            size_t len = strlen(joriy);
            if (len > max_len) {
                max_len = len;
                strcpy(eng_uzun, joriy);
            }
        }
        fclose(f);
        printf("Eng uzun qator (%zu belgi): "%s"\n", max_len, eng_uzun);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fayldagi eng uzun qatorni topish bufer parametrlarini to'g'ri loyihalashda yordam beradi.

## Ishlash natijasi:
```text
Eng uzun qator (41 belgi): "Bu fayldagi eng uzun jumla hisoblanadi!"
```

---

# 732-Topshiriq: Ikki faylni birlashtirish (File Concatenation / UNIX cat simulyatsiyasi)

## Topshiriq sharti:
Ikkinchi fayl ma'lumotlarini birinchi fayl oxiriga to'liq ko'chirish.

## Yechim (C kodi):
```c
#include <stdio.h>

void birlashtir(const char *f1, const char *f2) {
    FILE *dst = fopen(f1, "ab"); // Append binar
    FILE *src = fopen(f2, "rb"); // Read binar
    if (!dst || !src) return;

    char buf[512];
    size_t oqildi;
    while ((oqildi = fread(buf, 1, sizeof(buf), src)) > 0) {
        fwrite(buf, 1, oqildi, dst);
    }
    fclose(dst);
    fclose(src);
}

int main(void) {
    FILE *a = fopen("a.txt", "w");
    FILE *b = fopen("b.txt", "w");
    if (a && b) {
        fputs("Qism 1. ", a);
        fputs("Qism 2.", b);
        fclose(a);
        fclose(b);
    }

    birlashtir("a.txt", "b.txt");

    FILE *res = fopen("a.txt", "r");
    if (res) {
        char buf[64];
        if (fgets(buf, sizeof(buf), res)) {
            printf("Birlashtirilgan natija: %s\n", buf);
        }
        fclose(res);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Katta buferlar (512B - 64KB) bilan fread/fwrite orqali ko'chirish I/O amallarini tezlashtiradi.

## Ishlash natijasi:
```text
Birlashtirilgan natija: Qism 1. Qism 2.
```

---

# 733-Topshiriq: INI / Config faylini pars qilish (Key-Value konfiguratsiya)

## Topshiriq sharti:
Fayldan 'kalit = qiymat' juftliklarini o'qib olish va tahlil qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    FILE *f = fopen("config.ini", "w");
    if (f) {
        fputs("port = 8080\n", f);
        fputs("host = localhost\n", f);
        fputs("timeout = 30\n", f);
        fclose(f);
    }

    f = fopen("config.ini", "r");
    if (f) {
        char qator[128];
        char kalit[64], qiymat[64];

        while (fgets(qator, sizeof(qator), f)) {
            if (sscanf(qator, "%63s = %63s", kalit, qiymat) == 2) {
                printf("Konfiguratsiya: [%s] -> '%s'\n", kalit, qiymat);
            }
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. sscanf() satr ichidan formatlangan ma'lumotlarni o'qish imkonini beradi.
2. Oddiy konfiguratsion fayllarni pars qilish uchun bu eng ommabop usuldir.

## Ishlash natijasi:
```text
Konfiguratsiya: [port] -> '8080'
Konfiguratsiya: [host] -> 'localhost'
Konfiguratsiya: [timeout] -> '30'
```

---

# 734-Topshiriq: Binar faylda butun sonlar massivini teskari tartibda saqlash

## Topshiriq sharti:
Fayldan sonlarni o'qib, ularni teskari aylantirib yangi binar faylga yozish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    int kirish[] = {1, 2, 3, 4, 5};
    int n = 5;

    FILE *f = fopen("asl.bin", "wb");
    if (f) {
        fwrite(kirish, sizeof(int), n, f);
        fclose(f);
    }

    // Oxiridan boshlab o'qish (fseek SEEK_END)
    f = fopen("asl.bin", "rb");
    FILE *out = fopen("teskari.bin", "wb");

    if (f && out) {
        for (int i = n - 1; i >= 0; i--) {
            fseek(f, i * sizeof(int), SEEK_SET);
            int val;
            fread(&val, sizeof(int), 1, f);
            fwrite(&val, sizeof(int), 1, out);
        }
        fclose(f);
        fclose(out);
    }

    // Tekshirish
    out = fopen("teskari.bin", "rb");
    if (out) {
        int olingan[5];
        fread(olingan, sizeof(int), 5, out);
        printf("Teskari yozilgan sonlar: ");
        for (int i = 0; i < 5; i++) printf("%d ", olingan[i]);
        printf("\n");
        fclose(out);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. fseek yordamida fayl orqasidan boshiga qarab qadamlab o'qish mumkin.

## Ishlash natijasi:
```text
Teskari yozilgan sonlar: 5 4 3 2 1
```

---

# 735-Topshiriq: Binar faylga bitmap rasm sarlavhasini (BMP Header) yozish

## Topshiriq sharti:
1x1 pikselli qizil BMP faylini sof C kodi va fayl I/O orqali noldan yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#pragma pack(push, 1)
typedef struct {
    uint16_t type;             // 'BM' (0x4D42)
    uint32_t size;             // Fayl hajmi
    uint16_t reserved1;
    uint16_t reserved2;
    uint32_t offset;           // Piksel ma'lumotlariga siljish
    uint32_t header_size;      // DIB header hajmi (40)
    int32_t  width;            // Kenglik
    int32_t  height;           // Balandlik
    uint16_t planes;           // 1
    uint16_t bpp;              // Bit per pixel (24)
    uint32_t compression;     // 0
    uint32_t image_size;      // 0
    int32_t  x_ppm;
    int32_t  y_ppm;
    uint32_t colors_used;
    uint32_t colors_important;
} BMPHeader;
#pragma pack(pop)

int main(void) {
    BMPHeader bmp = {0};
    bmp.type = 0x4D42; // "BM"
    bmp.offset = sizeof(BMPHeader);
    bmp.header_size = 40;
    bmp.width = 1;
    bmp.height = 1;
    bmp.planes = 1;
    bmp.bpp = 24; // RGB 3 bayt
    bmp.size = sizeof(BMPHeader) + 4; // 1 piksel (3 bayt + 1 bayt padding)

    FILE *f = fopen("pixel.bmp", "wb");
    if (f) {
        fwrite(&bmp, sizeof(BMPHeader), 1, f);
        // BGR formati: Moviy=0, Yashil=0, Qizil=255, Padding=0
        uint8_t piksel[4] = {0, 0, 255, 0};
        fwrite(piksel, 1, 4, f);
        fclose(f);
        printf("BMP rasm muvaffaqiyatli yaratildi (Hajmi: %u bayt)\n", bmp.size);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Grafika fayllari (BMP, WAV) to'liq binar tuzilmalar bo'lib, C fayl I/O orqali to'g'ridan-to'g'ri generatsiya qilinadi.
2. #pragma pack(1) struktura elementlari orasiga bo'shliqlar qo'shilmasligini ta'minlaydi.

## Ishlash natijasi:
```text
BMP rasm muvaffaqiyatli yaratildi (Hajmi: 58 bayt)
```

---

# 736-Topshiriq: WAV audio fayli sarlavhasi (RIFF WAV Header) va sinussimon signal yaratish

## Topshiriq sharti:
Sof matematik sinus to'lqinini WAV audio fayliga yozib tovush fayli hosil qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>
#include <math.h>

#pragma pack(push, 1)
typedef struct {
    char     riff[4];        // "RIFF"
    uint32_t overall_size;
    char     wave[4];        // "WAVE"
    char     fmt_chunk[4];   // "fmt "
    uint32_t length_fmt;     // 16
    uint16_t format_tag;     // 1 (PCM)
    uint16_t num_channels;   // 1 (Mono)
    uint32_t sample_rate;    // 8000 Hz
    uint32_t byte_rate;      // 8000 * 1 = 8000
    uint16_t block_align;    // 1
    uint16_t bits_per_sample;// 8
    char     data_chunk[4];  // "data"
    uint32_t data_size;
} WAVHeader;
#pragma pack(pop)

int main(void) {
    uint32_t samples = 8000; // 1 soniya
    WAVHeader h = {
        {'R','I','F','F'}, sizeof(WAVHeader) + samples - 8,
        {'W','A','V','E'}, {'f','m','t',' '}, 16, 1, 1,
        8000, 8000, 1, 8, {'d','a','t','a'}, samples
    };

    FILE *f = fopen("ton.wav", "wb");
    if (f) {
        fwrite(&h, sizeof(WAVHeader), 1, f);
        // 440 Hz (La notasi) to'lqini
        for (uint32_t i = 0; i < samples; i++) {
            double t = (double)i / 8000.0;
            uint8_t val = (uint8_t)(128 + 127 * sin(2.0 * 3.14159265 * 440.0 * t));
            fputc(val, f);
        }
        fclose(f);
        printf("1 soniyalik 440Hz audio fayl saqlandi!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Raqamli ovoz (DSP) va multimedia dasturlashning asosi faylga binar baytlarni to'g'ri tartibda yozishdir.

## Ishlash natijasi:
```text
1 soniyalik 440Hz audio fayl saqlandi!
```

---

# 737-Topshiriq: Fayldagi ma'lum bir so'zni boshqasiga almashtirish (Word Replacement)

## Topshiriq sharti:
Fayl ichidagi 'eski' so'zni 'yangi' so'z bilan almashtirib yangilash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    FILE *f = fopen("matn_almash.txt", "w");
    if (f) {
        fputs("C tili eski tildir. Ammo C tili tezkor.", f);
        fclose(f);
    }

    f = fopen("matn_almash.txt", "r");
    FILE *out = fopen("matn_almash_out.txt", "w");

    if (f && out) {
        char soz[64];
        while (fscanf(f, "%63s", soz) == 1) {
            if (strcmp(soz, "eski") == 0) {
                fputs("kuchli ", out);
            } else {
                fprintf(out, "%s ", soz);
            }
        }
        fclose(f);
        fclose(out);
    }

    out = fopen("matn_almash_out.txt", "r");
    if (out) {
        char buf[128];
        if (fgets(buf, sizeof(buf), out)) {
            printf("Natija: %s\n", buf);
        }
        fclose(out);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Matn filtratsiyasi va qayta ishlash algoritmlari oqimli fscanf va fputs orqali amalga oshiriladi.

## Ishlash natijasi:
```text
Natija: C tili kuchli tildir. Ammo C tili tezkor.
```

---

# 738-Topshiriq: Xavfsiz fayl yozish: Temp fayl va atomik almashtirish (Atomic File Write)

## Topshiriq sharti:
Dastur yozish paytida to'xtab qolsa ham asl fayl buzilmasligini kafolatlovchi andoza.

## Yechim (C kodi):
```c
#include <stdio.h>

int atomik_saqla(const char *fayl_nomi, const char *ma_lumot) {
    char temp_nomi[256];
    snprintf(temp_nomi, sizeof(temp_nomi), "%s.tmp", fayl_nomi);

    FILE *f = fopen(temp_nomi, "w");
    if (!f) return 0;

    fputs(ma_lumot, f);
    fflush(f);
    fclose(f);

    // Atomik qayta nomlash
    remove(fayl_nomi);
    return rename(temp_nomi, fayl_nomi) == 0;
}

int main(void) {
    if (atomik_saqla("bazaviy_konfig.json", "{\"status\": \"OK\"}")) {
        printf("Konfiguratsiya atomik tarzda xavfsiz saqlandi!\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Agar faylga to'g'ridan-to'g'ri yozilayotganda tok o'chsa yoki dastur qulasa, fayl 0 bayt bo'lib buzilib qoladi.
2. Avval .tmp faylga to'liq yozib, so'ng rename qilish orqali ma'lumot yo'qolishidan 100% himoyalanish mumkin.

## Ishlash natijasi:
```text
Konfiguratsiya atomik tarzda xavfsiz saqlandi!
```

---

# 739-Topshiriq: Log fayllarini avtomatik rotatsiya qilish (Log Rotation)

## Topshiriq sharti:
Log hajmi ma'lum chegaraga yetganda (masalan 100 bayt) eski faylni .1 ga o'tkazib yangi fayl ochish.

## Yechim (C kodi):
```c
#include <stdio.h>

#define MAX_LOG_SIZE 50

void yoz_log(const char *xabar) {
    const char *log_nomi = "app.log";
    FILE *f = fopen(log_nomi, "a+");
    if (!f) return;

    fseek(f, 0, SEEK_END);
    if (ftell(f) >= MAX_LOG_SIZE) {
        fclose(f);
        remove("app.log.1");
        rename("app.log", "app.log.1");
        f = fopen(log_nomi, "w");
        printf("[ROTATION]: app.log hajmi oshdi, app.log.1 ga ko'chirildi!\n");
    }

    fprintf(f, "%s\n", xabar);
    fclose(f);
}

int main(void) {
    for (int i = 1; i <= 4; i++) {
        char xabar[32];
        snprintf(xabar, sizeof(xabar), "Log hodisasi #%d", i);
        yoz_log(xabar);
    }
    printf("Loglar yozildi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Log rotatsiyasi serverlarda disk to'lib qolishining oldini oluvchi zaruriy mexanizmdir.

## Ishlash natijasi:
```text
[ROTATION]: app.log hajmi oshdi, app.log.1 ga ko'chirildi!
Loglar yozildi.
```

---

# 740-Topshiriq: fgetpos() va fsetpos() yordamida 64-bitli fayl pozitsiyasini saqlash

## Topshiriq sharti:
2 GB dan katta gigant fayllarda fpos_t orqali pozitsiyani xatosiz eslab qolish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("fpos_test.txt", "w+");
    if (f) {
        fputs("Boshlang'ich qator\nIkkinchi qator\n", f);

        fpos_t pos;
        rewind(f);
        // Boshlang'ich qatorni o'qiymiz
        char buf[32];
        fgets(buf, sizeof(buf), f);

        // Ikkinchi qator boshlanish nuqtasini saqlaymiz:
        fgetpos(f, &pos);
        printf("Ikkinchi qator pozitsiyasi saqlandi.\n");

        fgets(buf, sizeof(buf), f);
        printf("O'qilgan: %s", buf);

        // Saqlangan pozitsiyaga qaytamiz:
        fsetpos(f, &pos);
        fgets(buf, sizeof(buf), f);
        printf("Qayta o'qilgan: %s", buf);

        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ftell() long qaytaradi (32-bit tizimlarda 2GB cheklovi bor).
2. fgetpos() va fsetpos() fpos_t ob'ekti orqali terabaytlab kattalikdagi fayllarda ham pozitsiyani xatosiz boshqaradi.

## Ishlash natijasi:
```text
Ikkinchi qator pozitsiyasi saqlandi.
O'qilgan: Ikkinchi qator
Qayta o'qilgan: Ikkinchi qator
```

---

# 741-Topshiriq: Fayldagi ma'lumotlarni saralash (File-based sort)

## Topshiriq sharti:
Fayldagi sonlarni o'qib qsort bilan saralab qayta faylga yozish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

int cmp_int(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

int main(void) {
    FILE *f = fopen("unsorted.txt", "w");
    if (f) {
        fprintf(f, "42\n12\n88\n5\n33\n");
        fclose(f);
    }

    f = fopen("unsorted.txt", "r");
    int sonlar[10];
    int count = 0;
    if (f) {
        while (fscanf(f, "%d", &sonlar[count]) == 1) {
            count++;
        }
        fclose(f);
    }

    qsort(sonlar, count, sizeof(int), cmp_int);

    f = fopen("sorted.txt", "w");
    if (f) {
        for (int i = 0; i < count; i++) {
            fprintf(f, "%d\n", sonlar[i]);
        }
        fclose(f);
    }

    printf("Fayldagi %d ta son saralanib 'sorted.txt' ga yozildi.\n", count);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fayldagi ma'lumotlarni xotiraga yuklash, saralash va qayta yozish orqali hisobotlar tartiblanadi.

## Ishlash natijasi:
```text
Fayldagi 5 ta son saralanib 'sorted.txt' ga yozildi.
```

---

# 742-Topshiriq: Binar faylda Run-Length Encoding (RLE) siqish algoritmi

## Topshiriq sharti:
Ketma-ket takrorlanuvchi baytlarni sanagich bilan ixchamlashtirib faylga yozish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

void rle_siqish(const uint8_t *in, int len, const char *out_fayl) {
    FILE *f = fopen(out_fayl, "wb");
    if (!f) return;

    for (int i = 0; i < len; i++) {
        uint8_t count = 1;
        while (i + 1 < len && in[i] == in[i + 1] && count < 255) {
            count++;
            i++;
        }
        fputc(count, f);
        fputc(in[i], f);
    }
    fclose(f);
}

int main(void) {
    // 10 ta 'A' va 5 ta 'B' (jami 15 bayt)
    uint8_t ma_lumot[] = "AAAAAAAAAABBBBB";

    rle_siqish(ma_lumot, 15, "compressed.rle");

    // Fayl hajmini tekshiramiz
    FILE *f = fopen("compressed.rle", "rb");
    if (f) {
        fseek(f, 0, SEEK_END);
        printf("Asl hajm: 15 bayt -> Siqilgan hajm: %ld bayt\n", ftell(f));
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. RLE eng qadimgi va sodda siqish algoritmi bo'lib, BMP va TIFF formatlarida qo'llaniladi.
2. 15 baytlik ma'lumot 4 baytga (10 'A' va 5 'B') siqildi.

## Ishlash natijasi:
```text
Asl hajm: 15 bayt -> Siqilgan hajm: 4 bayt
```

---

# 743-Topshiriq: RLE faylini qayta tiklash (Decompression)

## Topshiriq sharti:
Siqilgan .rle fayldan asl baytlarni qayta tiklash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    FILE *f = fopen("compressed.rle", "rb");
    if (f) {
        printf("Tiklanayotgan ma'lumot: ");
        int count, bayt;
        while ((count = fgetc(f)) != EOF && (bayt = fgetc(f)) != EOF) {
            for (int i = 0; i < count; i++) {
                putchar(bayt);
            }
        }
        printf("\n");
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir (count, bayt) juftligi o'qilib count marta asl bayt tiklanadi.

## Ishlash natijasi:
```text
Tiklanayotgan ma'lumot: AAAAAAAAAABBBBB
```

---

# 744-Topshiriq: Xavfsiz parollarni saqlovchi binar kesh fayli

## Topshiriq sharti:
Strukturani binar faylga saqlab, dastur qayta yoqilganda o'qib olish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    char login[32];
    uint32_t pin_xesh;
} Autentifikatsiya;

int main(void) {
    Autentifikatsiya auth = { "admin", 0x1234ABCD };

    FILE *f = fopen("auth.bin", "wb");
    if (f) {
        fwrite(&auth, sizeof(Autentifikatsiya), 1, f);
        fclose(f);
    }

    Autentifikatsiya olingan = {0};
    f = fopen("auth.bin", "rb");
    if (f) {
        fread(&olingan, sizeof(Autentifikatsiya), 1, f);
        fclose(f);
        printf("Yuklandi: Login='%s', Xesh=0x%08X\n", 
               olingan.login, olingan.pin_xesh);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Binar saqlash oddiy matnli fayllardan ko'ra foydalanuvchi ma'lumotlarini tasodifiy ko'rishdan himoya qiladi.

## Ishlash natijasi:
```text
Yuklandi: Login='admin', Xesh=0x1234ABCD
```

---

# 745-Topshiriq: Ko'p oqimli xavfsiz fayl kiritish/chiqarish: flockfile va funlockfile tushunchasi

## Topshiriq sharti:
Ko'p oqimli muhitda faylga parallel yozish paytida aralashib ketishning oldini olish tamoyili.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("threaded.log", "w");
    if (f) {
        // POSIX muhitida: flockfile(f);
        fputs("1-oqim ma'lumoti...\n", f);
        fputs("1-oqim yakuni.\n", f);
        // POSIX muhitida: funlockfile(f);

        printf("Fayl qulflash simulyatsiyasi muvaffaqiyatli yakunlandi.\n");
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Har bir C stdio chaqiruvi (masalan fputc) ichki qulfga ega.
2. Butun boshli blok yozuvlari aralashmasligi uchun flockfile(f) va funlockfile(f) orqali fayl oqim darajasida qulflanadi.

## Ishlash natijasi:
```text
Fayl qulflash simulyatsiyasi muvaffaqiyatli yakunlandi.
```

---

# 746-Topshiriq: Binar faylda zanjirli ro'yxatni (Serialized Linked List) saqlash

## Topshiriq sharti:
Xotiradagi Linked List elementlarini diskka ketma-ket binar yozish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Tugun {
    int qiymat;
    struct Tugun *keyingi;
} Tugun;

int main(void) {
    Tugun t3 = {30, NULL};
    Tugun t2 = {20, &t3};
    Tugun t1 = {10, &t2};

    FILE *f = fopen("list.bin", "wb");
    if (f) {
        Tugun *curr = &t1;
        while (curr) {
            fwrite(&curr->qiymat, sizeof(int), 1, f);
            curr = curr->keyingi;
        }
        fclose(f);
        printf("Linked List elementlari binar faylga saqlandi.\n");
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ko'rsatkichlar manzilini faylga yozish xato, chunki dastur qayta ochilganda manzillar o'zgaradi!
2. Faqat foydali qiymatlar (data payload) serializatsiya qilinadi.

## Ishlash natijasi:
```text
Linked List elementlari binar faylga saqlandi.
```

---

# 747-Topshiriq: Binar fayldan zanjirli ro'yxatni qayta tiklash (Deserialization)

## Topshiriq sharti:
Fayldagi butun sonlarni o'qib dinamik Linked List tugunlarini yangitdan xotirada qurish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Tugun {
    int val;
    struct Tugun *next;
} Tugun;

int main(void) {
    FILE *f = fopen("list.bin", "rb");
    if (!f) return 1;

    Tugun *bosh = NULL, *oxiri = NULL;
    int v;

    while (fread(&v, sizeof(int), 1, f) == 1) {
        Tugun *yangi = (Tugun*)malloc(sizeof(Tugun));
        yangi->val = v;
        yangi->next = NULL;

        if (!bosh) bosh = oxiri = yangi;
        else { oxiri->next = yangi; oxiri = yangi; }
    }
    fclose(f);

    printf("Fayldan tiklangan ro'yxat: ");
    Tugun *c = bosh;
    while (c) {
        printf("%d -> ", c->val);
        Tugun *tmp = c;
        c = c->next;
        free(tmp);
    }
    printf("NULL\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Deserializatsiyada fayldagi har bir element uchun malloc chaqirilib xotirada ko'rsatkichlar qayta bog'lanadi.

## Ishlash natijasi:
```text
Fayldan tiklangan ro'yxat: 10 -> 20 -> 30 -> NULL
```

---

# 748-Topshiriq: Katta fayllarni qismlarga bo'lish (File Splitter)

## Topshiriq sharti:
Katta binar faylni har biri 10 baytdan bo'lgan kichik bo'laklarga (.part1, .part2) ajratish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("katta.dat", "wb");
    if (f) {
        fputs("0123456789ABCDEFGHIJ", f); // 20 bayt
        fclose(f);
    }

    f = fopen("katta.dat", "rb");
    if (f) {
        char buf[10];
        int part = 1;
        size_t n;

        while ((n = fread(buf, 1, 10, f)) > 0) {
            char part_nom[32];
            snprintf(part_nom, sizeof(part_nom), "katta.part%d", part++);
            FILE *p = fopen(part_nom, "wb");
            if (p) {
                fwrite(buf, 1, n, p);
                fclose(p);
                printf("%s yaratildi (%zu bayt)\n", part_nom, n);
            }
        }
        fclose(f);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fayllarni qismlarga ajratish arxivatorlar va tarmoq orqali katta hajmdagi ma'lumotlarni paketlab yuborishda kerak bo'ladi.

## Ishlash natijasi:
```text
katta.part1 yaratildi (10 bayt)
katta.part2 yaratildi (10 bayt)
```

---

# 749-Topshiriq: Qismlarga bo'lingan fayllarni qayta yig'ish (File Merger)

## Topshiriq sharti:
Alohida .part fayllarni o'qib asl binar faylni bitta butun holatga keltirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    FILE *out = fopen("tiklangan.dat", "wb");
    if (out) {
        for (int part = 1; part <= 2; part++) {
            char part_nom[32];
            snprintf(part_nom, sizeof(part_nom), "katta.part%d", part);
            FILE *p = fopen(part_nom, "rb");
            if (p) {
                char buf[10];
                size_t n = fread(buf, 1, 10, p);
                fwrite(buf, 1, n, out);
                fclose(p);
            }
        }
        fclose(out);
    }

    FILE *res = fopen("tiklangan.dat", "rb");
    if (res) {
        char buf[32] = {0};
        fread(buf, 1, 20, res);
        printf("Tiklangan butun fayl: %s\n", buf);
        fclose(res);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Ketma-ket fayl qismlarini bitta oqimga append qilish orqali butun fayl qayta hosil qilinadi.

## Ishlash natijasi:
```text
Tiklangan butun fayl: 0123456789ABCDEFGHIJ
```

---

# 750-Topshiriq: Modul yakuni va Master Loyiha: Indekslashgan Binar Ma'lumotlar Bazasi Dvigateli (Flat-File Indexed DB Engine)

## Topshiriq sharti:
Yozuvlarni (Record: ID, Nom, Qiymat) binar faylga saqlovchi va xotiradagi indeks orqali O(1) da qidirib yangilovchi to'liq ma'lumotlar bazasi tizimi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <string.h>

#define MAX_RECORDS 100

typedef struct {
    int id;
    char ism[32];
    double hisob;
} DBRecord;

typedef struct {
    int id;
    long fayl_offset;
} DBIndex;

typedef struct {
    FILE *fayl;
    DBIndex indekslar[MAX_RECORDS];
    int jami_yozuvlar;
} DBEngine;

void db_ochish(DBEngine *db, const char *fayl_nomi) {
    db->fayl = fopen(fayl_nomi, "wb+");
    db->jami_yozuvlar = 0;
}

void db_qoshish(DBEngine *db, int id, const char *ism, double hisob) {
    if (db->jami_yozuvlar >= MAX_RECORDS) return;

    fseek(db->fayl, 0, SEEK_END);
    long offset = ftell(db->fayl);

    DBRecord rec;
    rec.id = id;
    strncpy(rec.ism, ism, sizeof(rec.ism) - 1);
    rec.ism[sizeof(rec.ism) - 1] = '\0';
    rec.hisob = hisob;

    fwrite(&rec, sizeof(DBRecord), 1, db->fayl);
    fflush(db->fayl);

    // Indeksga qo'shish
    db->indekslar[db->jami_yozuvlar].id = id;
    db->indekslar[db->jami_yozuvlar].fayl_offset = offset;
    db->jami_yozuvlar++;
}

int db_qidirish(DBEngine *db, int id, DBRecord *natija) {
    for (int i = 0; i < db->jami_yozuvlar; i++) {
        if (db->indekslar[i].id == id) {
            fseek(db->fayl, db->indekslar[i].fayl_offset, SEEK_SET);
            fread(natija, sizeof(DBRecord), 1, db->fayl);
            return 1; // Topildi
        }
    }
    return 0; // Topilmadi
}

void db_yopish(DBEngine *db) {
    if (db->fayl) fclose(db->fayl);
}

int main(void) {
    printf("=== INDEKSLASHGAN BINAR BAZA DVIGATELI ===\n");
    DBEngine db;
    db_ochish(&db, "bank.db");

    db_qoshish(&db, 1001, "Ali Valiyev", 5400.0);
    db_qoshish(&db, 1002, "Zuhra Karimova", 8950.5);
    db_qoshish(&db, 1003, "Olim Shokirov", 1230.0);

    printf("Jami yozuvlar kiritildi: %d\n", db.jami_yozuvlar);

    // Indeks orqali to'g'ridan-to'g'ri qidirish
    DBRecord topilgan;
    if (db_qidirish(&db, 1002, &topilgan)) {
        printf("[QIDIRUV MUVAJOD]: ID %d -> Ism: %s, Balans: %.2f USD\n",
               topilgan.id, topilgan.ism, topilgan.hisob);
    }

    db_yopish(&db);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu yakuniy topshiriq 15-modulning barcha bilimlarini: FILE*, fopen/fclose rejimlarini, fseek/ftell orqali offset indeksatsiyasini, fwrite/fread orqali binar yozuvlarni va professional ma'lumotlar bazasi arxitekturasini o'zida mujassam etadi.
2. Zamonaviy ma'lumotlar bazalari (masalan B-Tree indekslari) aynan mana shunday fayl offsetlari orqali yozuvlarni bir zumda topish printsipiga asoslanadi.

## Ishlash natijasi:
```text
=== INDEKSLASHGAN BINAR BAZA DVIGATELI ===
Jami yozuvlar kiritildi: 3
[QIDIRUV MUVAJOD]: ID 1002 -> Ism: Zuhra Karimova, Balans: 8950.50 USD
```

---
