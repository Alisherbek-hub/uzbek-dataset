# Java Metodlar va Parametrlari (151-200)

# 151-Topshiriq: Metod signaturasi va qaytuvchi qiymat turlari

## Topshiriq sharti:
Java-da metod signaturasi nimalardan tashkil topishini va `void` hamda qiymat qaytaruvchi metodlarni yozing.

## Yechim (Java kodi):
```java
public class Solution {
    // Metod signaturasi: qoshish(int, int)
    public static int qoshish(int a, int b) {
        return a + b;
    }

    // Metod signaturasi: salomBer(String)
    public static void salomBer(String ism) {
        System.out.println("Assalomu alaykum, " + ism + "!");
    }

    public static void main(String[] args) {
        salomBer("Otabek");
        int natija = qoshish(15, 25);
        System.out.println("Yig'indi: " + natija);
    }
}
```

## Tushuntirish va Mantiq:
Metod signaturasi (Method Signature) metodning nomi va uning parametrlar ro'yxatidan (tiplari va tartibi) iborat.
E'tibor bering: metodning qaytarish turi (`return type`) va uning modifikatorlari (`public`, `static`) signaturaga kirmaydi!
`void` kalit so'zi metod hech qanday qiymat qaytarmasligini bildiradi.

## Ishlash natijasi:
```text
Assalomu alaykum, Otabek!
Yig'indi: 40
```

---

# 152-Topshiriq: Java-da Pass-by-Value mexanizmi: Primitiv tiplar

## Topshiriq sharti:
Java-da metodga primitiv o'zgaruvchi uzatilganda faqat uning qiymat nusxasi uzatilishini va asl o'zgaruvchi o'zgarmasligini isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void ozgartir(int son) {
        son = son + 100;
        System.out.println("Metod ichida: " + son);
    }

    public static void main(String[] args) {
        int x = 50;
        System.out.println("Chaqirishdan oldin x: " + x);
        ozgartir(x);
        System.out.println("Chaqirilgandan keyin x: " + x);
    }
}
```

## Tushuntirish va Mantiq:
Java QAT'IY RAVIShDA faqat "Pass-by-Value" (qiymat bo'yicha uzatish) tamoyilida ishlaydi.
Metod chaqirilganda parametr uchun yangi Stack freymda alohida xotira ajratiladi va unga o'zgaruvchining joriy nusxasi ko'chiriladi. Metod ichida bu nusxani o'zgartirish chaqiruvchining `x` o'zgaruvchisiga mutlaqo ta'sir qilmaydi.

## Ishlash natijasi:
```text
Chaqirishdan oldin x: 50
Metod ichida: 150
Chaqirilgandan keyin x: 50
```

---

# 153-Topshiriq: Pass-by-Value: Ob'ekt ko'rsatkichlari (References)

## Topshiriq sharti:
Metodga obyekt uzatilganda obyektning o'zi emas, uning xotira manzili nusxasi (copy of reference) uzatilishini va ichki holat o'zgarishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Talaba {
        String ism;
        Talaba(String ism) { this.ism = ism; }
    }

    public static void ismniYangila(Talaba t) {
        t.ism = "Sanjar"; // Heap dagi o'sha obyekt maydoni o'zgaradi
    }

    public static void main(String[] args) {
        Talaba talaba = new Talaba("Jahongir");
        System.out.println("Dastlabki ism: " + talaba.ism);
        ismniYangila(talaba);
        System.out.println("Metoddan keyin ism: " + talaba.ism);
    }
}
```

## Tushuntirish va Mantiq:
Obyekt metodga uzatilganda, Stack freymdagi ko'rsatkich (havola) nusxalanadi. Ikkala ko'rsatkich ham Heap xotiradagi aynan bitta obyektga qarab turadi.
Shu sababli `t.ism = "Sanjar"` qilinganda, Heap dagi haqiqiy obyekt holati o'zgaradi.

## Ishlash natijasi:
```text
Dastlabki ism: Jahongir
Metoddan keyin ism: Sanjar
```

---

# 154-Topshiriq: Pass-by-Value: Ko'rsatkichni qayta biriktirish (Reassignment)

## Topshiriq sharti:
Metod ichida obyekt parametriga yangi obyekt berilsa (`t = new Talaba()`), tashqaridagi asl ko'rsatkich nima uchun o'zgarmasligini isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    static class Talaba {
        String ism;
        Talaba(String ism) { this.ism = ism; }
    }

    public static void yangiObyektBiriktir(Talaba t) {
        t = new Talaba("Yangi Talaba"); // Faqat lokal ko'rsatkich yangi obyektga o'tdi
        System.out.println("Metod ichidagi yangi obyekt: " + t.ism);
    }

    public static void main(String[] args) {
        Talaba talaba = new Talaba("Asl Talaba");
        yangiObyektBiriktir(talaba);
        System.out.println("Tashqaridagi asl talaba: " + talaba.ism);
    }
}
```

## Tushuntirish va Mantiq:
Bu Java-ning Pass-by-Reference EMASLIGINING eng yaqqol isbotidir.
`t` o'zgaruvchisi havolaning mustaqil nusxasi bo'lgani sababli, `t = new ...` qilinganda faqat shu nusxa boshqa manzilga qarab qoladi. Asosiy `main` metodidagi `talaba` havolasi esa o'zining eski obyektiga ko'rsatishda davom etadi.

## Ishlash natijasi:
```text
Metod ichidagi yangi obyekt: Yangi Talaba
Tashqaridagi asl talaba: Asl Talaba
```

---

# 155-Topshiriq: Metodlarni haddan tashqari yuklash (Method Overloading)

## Topshiriq sharti:
Bir xil nomli, ammo har xil parametrlarga ega `qoshish` metodlarini yuklash (overload qilish) dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static int qoshish(int a, int b) {
        return a + b;
    }

    public static double qoshish(double a, double b) {
        return a + b;
    }

    public static int qoshish(int a, int b, int c) {
        return a + b + c;
    }

    public static void main(String[] args) {
        System.out.println("2 ta int: " + qoshish(10, 20));
        System.out.println("2 ta double: " + qoshish(10.5, 20.3));
        System.out.println("3 ta int: " + qoshish(10, 20, 30));
    }
}
```

## Tushuntirish va Mantiq:
Metodlarni haddan tashqari yuklash (Method Overloading) — bir xil nomli metodning turli xil argumentlar ro'yxatiga ega bo'lishidir.
Qoidalar:
- Parametrlar soni har xil bo'lishi mumkin;
- Parametrlar turlari har xil bo'lishi mumkin;
- Parametrlar ketma-ketligi har xil bo'lishi mumkin.
Muhim: Faqat qaytarish turini o'zgartirish orqali overload qilib bo'lmaydi!

## Ishlash natijasi:
```text
2 ta int: 30
2 ta double: 30.8
3 ta int: 60
```

---

# 156-Topshiriq: Overloading da ustuvorlik qoidalari (Resolution Order)

## Topshiriq sharti:
Kompilyator metod tanlashda: Exact match -> Widening -> Autoboxing -> Varargs ketma-ketligini qanday tanlashini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void test(long x) { System.out.println("Widening (long)"); }
    public static void test(Integer x) { System.out.println("Autoboxing (Integer)"); }
    public static void test(int... x) { System.out.println("Varargs (int...)"); }

    public static void main(String[] args) {
        int son = 10;
        test(son);
    }
}
```

## Tushuntirish va Mantiq:
Java kompilyatori mos metodni qidirishda quyidagi 4 ta qat'iy ustuvorlik bosqichidan o'tadi:
1. Exact match (aniq mos kelish - `int`)
2. Widening (kengaytirish - `long`, `float`, `double`)
3. Autoboxing (o'rash - `Integer`)
4. Varargs (`int...`)
Shu sababli `int son` uzatilganda `Integer` dan oldin `long` (Widening) tanlanadi, chunki bu Java 1.0 dan beri mavjud eng qadimiy qoidadir.

## Ishlash natijasi:
```text
Widening (long)
```

---

# 157-Topshiriq: O'zgaruvchan parametrlar (Varargs `...`)

## Topshiriq sharti:
Ixtiyoriy sondagi butun sonlarni qabul qilib ularning yig'indisini hisoblovchi varargs metodini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static int yigindi(int... sonlar) {
        int total = 0;
        for (int s : sonlar) {
            total += s;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println("0 ta parametr: " + yigindi());
        System.out.println("2 ta parametr: " + yigindi(5, 10));
        System.out.println("4 ta parametr: " + yigindi(1, 2, 3, 4));
        System.out.println("Massiv uzatilganda: " + yigindi(new int[]{10, 20, 30}));
    }
}
```

## Tushuntirish va Mantiq:
Varargs (`...`) Java 5 da kiritilgan bo'lib, kompilyator orqa fonda uni mos turdagi massivga (`int[]`) aylantiradi.
Qoidasi:
1. Metodda faqat bitta varargs parametri bo'lishi mumkin.
2. Varargs parametri har doim parametrlar ro'yxatining eng oxirida turishi shart (`String xabar, int... sonlar`).

## Ishlash natijasi:
```text
0 ta parametr: 0
2 ta parametr: 15
4 ta parametr: 10
Massiv uzatilganda: 60
```

---

# 158-Topshiriq: Rekursiya asoslari: Faktorial hisoblash

## Topshiriq sharti:
Sonning faktorialini hisoblovchi rekursiv metod va uning tayanch shartini (base case) tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static long faktorial(int n) {
        if (n <= 1) { // Base case (tayanch shart)
            return 1;
        }
        return n * faktorial(n - 1); // Recursive case
    }

    public static void main(String[] args) {
        int son = 6;
        System.out.println(son + "! = " + faktorial(son));
    }
}
```

## Tushuntirish va Mantiq:
Rekursiya — bu funksiyaning o'z-o'zini chaqirishi.
Har qanday rekursiv funksiyada 2 ta narsa bo'lishi shart:
1. Base case: rekursiyani to'xtatuvchi shart (`n <= 1`).
2. Recursive step: masalani kichikroq qismga bo'lib o'zini chaqirish (`n * faktorial(n - 1)`).
Agar tayanch shart bo'lmasa, funksiya cheksiz chaqirilib, Stack to'lib ketadi.

## Ishlash natijasi:
```text
6! = 720
```

---

# 159-Topshiriq: StackOverflowError sabablari va uning tahlili

## Topshiriq sharti:
Noto'g'ri rekursiya tufayli JVM Stack xotirasi to'lishi (`StackOverflowError`) holatini xavfsiz namoyish eting.

## Yechim (Java kodi):
```java
public class Solution {
    public static void cheksizRekursiya(int qadam) {
        cheksizRekursiya(qadam + 1);
    }

    public static void main(String[] args) {
        try {
            cheksizRekursiya(1);
        } catch (StackOverflowError e) {
            System.out.println("Xatolik ushlandi: Stack xotira chegarasidan toshib ketdi!");
            System.out.println("Xato turi: " + e.getClass().getSimpleName());
        }
    }
}
```

## Tushuntirish va Mantiq:
Har bir metod chaqiruvi joriy oqimning Stack xotirasida yangi Stack Frame (freym) ochadi.
Freym o'zida lokal o'zgaruvchilar va qaytish manzilini saqlaydi.
Agar rekursiya to'xtamasdan minglab marta chaqirilsa, ajratilgan Stack xotira (sukut bo'yicha odatda 1MB) to'ladi va JVM `StackOverflowError` tashlaydi.

## Ishlash natijasi:
```text
Xatolik ushlandi: Stack xotira chegarasidan toshib ketdi!
Xato turi: StackOverflowError
```

---

# 160-Topshiriq: Evklid algoritmi: EKUB (Eng Katta Umumiy Bo'luvchi)

## Topshiriq sharti:
Ikkita sonning eng katta umumiy bo'luvchisini (EKUB / GCD) Evklid algoritmi orqali rekursiv toping.

## Yechim (Java kodi):
```java
public class Solution {
    public static int ekub(int a, int b) {
        if (b == 0) {
            return a;
        }
        return ekub(b, a % b);
    }

    public static void main(String[] args) {
        int a = 48;
        int b = 18;
        System.out.println("EKUB(" + a + ", " + b + ") = " + ekub(a, b));
    }
}
```

## Tushuntirish va Mantiq:
Evklid algoritmi: `ekub(a, b) = ekub(b, a % b)`.
Qachonki qoldiq 0 bo'lsa, o'sha paytdagi `a` soni ikkala sonning eng katta umumiy bo'luvchisi bo'ladi.
Bu algoritm logarifmik qadamda O(log(min(a, b))) o'ta tez ishlaydi.

## Ishlash natijasi:
```text
EKUB(48, 18) = 6
```

---

# 161-Topshiriq: Fibonachchi ketma-ketligi va eksponentsial rekursiya muammosi

## Topshiriq sharti:
Oddiy rekursiv Fibonachchi metodini yozing va nega u katta sonlarda juda sekinlashib qolishini tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static long fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }

    public static void main(String[] args) {
        int n = 8;
        System.out.println(n + "-Fibonachchi soni: " + fib(n));
    }
}
```

## Tushuntirish va Mantiq:
Oddiy rekursiv Fibonachchi har bir qadamda ikkita yangi chaqiruv hosil qiladi va daraxtsimon o'sadi.
Uning vaqt murakkabligi O(2^N) (eksponentsial) bo'lib, `n = 50` bo'lganda dastur milliardlab takroriy hisoblashlar sababli daqiqalar davomida qotib qoladi.

## Ishlash natijasi:
```text
8-Fibonachchi soni: 21
```

---

# 162-Topshiriq: Rekursiya optimizatsiyasi: Memoization (Keshlash)

## Topshiriq sharti:
Fibonachchi ketma-ketligini hisoblashda hisoblangan natijalarni massivda keshlash orqali vaqtni O(N) ga tushiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static long fibMemo(int n, long[] kesh) {
        if (n <= 1) return n;
        if (kesh[n] != 0) return kesh[n]; // Oldin hisoblangan bo'lsa keshdan olamiz
        
        kesh[n] = fibMemo(n - 1, kesh) + fibMemo(n - 2, kesh);
        return kesh[n];
    }

    public static void main(String[] args) {
        int n = 50;
        long[] kesh = new long[n + 1];
        long natija = fibMemo(n, kesh);
        System.out.println("50-Fibonachchi soni (tezkor): " + natija);
    }
}
```

## Tushuntirish va Mantiq:
Memoization (keshlash) — oraliq natijalarni saqlab qo'yish texnikasidir.
Bir marta hisoblangan `fib(k)` qayta hisoblanmasdan keshdan O(1) da olinadi.
Natijada rekursiya daraxti chiziqli zanjirga aylanadi va vaqt O(2^N) dan O(N) ga tushadi.

## Ishlash natijasi:
```text
50-Fibonachchi soni (tezkor): 12586269025
```

---

# 163-Topshiriq: Satrni rekursiv teskari o'girish

## Topshiriq sharti:
Sikllarsiz, faqat rekursiya va `substring()` yordamida matnni teskari qilib qaytaruvchi metod yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static String reverseString(String str) {
        if (str == null || str.length() <= 1) {
            return str;
        }
        return reverseString(str.substring(1)) + str.charAt(0);
    }

    public static void main(String[] args) {
        String matn = "SAMARQAND";
        System.out.println("Asl: " + matn);
        System.out.println("Teskari: " + reverseString(matn));
    }
}
```

## Tushuntirish va Mantiq:
Metod matnning 1-belgisidan keyingi qismini rekursiyaga beradi va eng birinchi belgini (`charAt(0)`) natijaning oxiriga ulaydi.
Base case: satr bo'sh yoki 1 ta belgidan iborat bo'lsa, o'zi qaytariladi.

## Ishlash natijasi:
```text
Asl: SAMARQAND
Teskari: DNAQRAMAS
```

---

# 164-Topshiriq: Palindrom tekshiruvi rekursiv usulda

## Topshiriq sharti:
So'zning chapdan va o'ngdan bir xil o'qilishini (palindrom) rekursiv tekshiruvchi metod tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static boolean isPalindrome(String s, int start, int end) {
        if (start >= end) return true;
        if (s.charAt(start) != s.charAt(end)) return false;
        return isPalindrome(s, start + 1, end - 1);
    }

    public static void main(String[] args) {
        String s1 = "kiyik";
        String s2 = "kitob";
        
        System.out.println(s1 + " palindrommi: " + isPalindrome(s1, 0, s1.length() - 1));
        System.out.println(s2 + " palindrommi: " + isPalindrome(s2, 0, s2.length() - 1));
    }
}
```

## Tushuntirish va Mantiq:
Ikki chetdagi belgilar solishtiriladi:
- Agar teng bo'lmasa, darhol `false`.
- Agar teng bo'lsa, ichkari tomon `start + 1` va `end - 1` bilan rekursiya davom etadi.
- Ko'rsatkichlar kesishganda (`start >= end`), barcha belgilar mos kelgani uchun `true` qaytadi.

## Ishlash natijasi:
```text
kiyik palindrommi: true
kitob palindrommi: false
```

---

# 165-Topshiriq: Static metodlar va ularning instansiya metodlaridan farqi

## Topshiriq sharti:
`static` metodlarning sinfga bog'liqligi va ularning `this` kalit so'ziga ega emasligini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    int instansiyaMaydoni = 10;
    static int statikMaydon = 20;

    public static void statikMetod() {
        System.out.println("Statik maydon: " + statikMaydon);
        // System.out.println(instansiyaMaydoni); // XATO: non-static field cannot be referenced from a static context
        // System.out.println(this); // XATO: static contextda 'this' mavjud emas!
    }

    public static void main(String[] args) {
        Solution.statikMetod();
    }
}
```

## Tushuntirish va Mantiq:
`static` metodlar muayyan obyektga emas, balki sinfning o'ziga tegishlidir.
Ular `new` orqali obyekt yaratmasdan sinf nomi orqali chaqiriladi (`Solution.statikMetod()`).
Chunki ular obyekt yaratilmasdan oldin xotiraga yuklanadi, shu sababli ularning ichida obyektga ishora qiluvchi `this` yoki instansiya maydonlari to'g'ridan-to'g'ri mavjud bo'lmaydi.

## Ishlash natijasi:
```text
Statik maydon: 20
```

---

# 166-Topshiriq: Statik initsializatsiya bloki (Static Initializer Block)

## Topshiriq sharti:
Sinf xotiraga birinchi marta yuklanganda ishga tushuvchi `static { ... }` blokining tartibini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static int x;
    
    static {
        System.out.println("1. Statik initsializatsiya bloki bajarildi");
        x = 500;
    }

    public static void main(String[] args) {
        System.out.println("2. main() metodi boshlandi");
        System.out.println("x ning qiymati: " + x);
    }
}
```

## Tushuntirish va Mantiq:
Statik blok (`static { ... }`) sinf JVM ClassLoader tomonidan xotiraga yuklangan vaqtda (Initialization bosqichida) atigi bir marta bajariladi.
U hatto `main` metodidan ham oldin ishga tushadi va og'ir statik resurslar, drayverlar yoki konfiguratsiyalarni oldindan sozlashda qo'llaniladi.

## Ishlash natijasi:
```text
1. Statik initsializatsiya bloki bajarildi
2. main() metodi boshlandi
x ning qiymati: 500
```

---

# 167-Topshiriq: Statik import (Static Import) va uning to'g'ri qo'llanilishi

## Topshiriq sharti:
`import static` yordamida sinf nomini yozmasdan metodlarni to'g'ridan-to'g'ri chaqirish dasturini yozing.

## Yechim (Java kodi):
```java
import static java.lang.Math.PI;
import static java.lang.Math.sqrt;
import static java.lang.Math.pow;

public class Solution {
    public static void main(String[] args) {
        // Math.sqrt o'rniga shunchaki sqrt
        double radius = 5.0;
        double yuza = PI * pow(radius, 2);
        double ildiz = sqrt(64);
        
        System.out.printf("Doira yuzi: %.2f
", yuza);
        System.out.println("64 ning ildizi: " + ildiz);
    }
}
```

## Tushuntirish va Mantiq:
Statik import Java 5 da kiritilgan bo'lib, o'zgarmaslar va utilit metodlarni sinf prefiksisiz chaqirish imkonini beradi.
Uni haddan tashqari ko'p ishlatish kodda metodning qayerdan kelganini noaniq qilib qo'yishi mumkin, ammo testlarda (masalan `Assertions.assertEquals`) va matematik hisoblarda qulaylik yaratadi.

## Ishlash natijasi:
```text
Doira yuzi: 78.54
64 ning ildizi: 8.0
```

---

# 168-Topshiriq: Objects.requireNonNull() bilan argumentlarni tekshirish

## Topshiriq sharti:
Metodga `null` kelganda o'z vaqtida aniq tushunarli xabar bilan xatolik otish uchun `Objects.requireNonNull()` dan foydalaning.

## Yechim (Java kodi):
```java
import java.util.Objects;

public class Solution {
    public static void foydalanuvchiQosh(String ism) {
        Objects.requireNonNull(ism, "Foydalanuvchi ismi null bo'lishi mumkin emas!");
        System.out.println("Foydalanuvchi muvaffaqiyatli qo'shildi: " + ism);
    }

    public static void main(String[] args) {
        foydalanuvchiQosh("Madina");
        
        try {
            foydalanuvchiQosh(null);
        } catch (NullPointerException e) {
            System.out.println("Ushlangan xatolik: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
`Objects.requireNonNull(obj, message)` zamonaviy Java-da argumentlarni validatsiya qilishning standart usulidir.
U argument `null` bo'lsa darhol ko'rsatilgan xabar bilan `NullPointerException` tashlaydi va xatoning keyinchalik chuqur qatlamlarda yashirin yuz berishining oldini oladi (Fail-fast tamoyili).

## Ishlash natijasi:
```text
Foydalanuvchi muvaffaqiyatli qo'shildi: Madina
Ushlangan xatolik: Foydalanuvchi ismi null bo'lishi mumkin emas!
```

---

# 169-Topshiriq: Argument validatsiyasi va IllegalArgumentException

## Topshiriq sharti:
Metod qabul qiladigan qiymatlar mantiqiy doirada bo'lishini tekshiruvchi himoyalangan metod tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void foizBelgila(int foiz) {
        if (foiz < 0 || foiz > 100) {
            throw new IllegalArgumentException("Foiz 0 va 100 orasida bo'lishi shart! Kiritildi: " + foiz);
        }
        System.out.println("Muvaffaqiyatli o'rnatildi: " + foiz + "%");
    }

    public static void main(String[] args) {
        foizBelgila(45);
        
        try {
            foizBelgila(120);
        } catch (IllegalArgumentException e) {
            System.out.println("Validatsiya xatosi: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
Agar metodga uzatilgan argument noto'g'ri qiymatga ega bo'lsa (masalan manfiy yosh, 100 dan katta foiz), Java-da standart `IllegalArgumentException` istisnosi tashlanadi.

## Ishlash natijasi:
```text
Muvaffaqiyatli o'rnatildi: 45%
Validatsiya xatosi: Foiz 0 va 100 orasida bo'lishi shart! Kiritildi: 120
```

---

# 170-Topshiriq: Professional Utility sinf arxitekturasi

## Topshiriq sharti:
Obyekt olinishi taqiqlangan, faqat statik metodlardan iborat toza Utility sinf modelini yarating.

## Yechim (Java kodi):
```java
public class Solution {
    public static final class MathUtils {
        // Shaxsiy konstruktor: instansiya olishni taqiqlaydi
        private MathUtils() {
            throw new UnsupportedOperationException("Utility sinfidan instansiya yaratib bo'lmaydi!");
        }

        public static boolean isEven(int n) {
            return (n & 1) == 0;
        }

        public static int kvadrat(int n) {
            return n * n;
        }
    }

    public static void main(String[] args) {
        System.out.println("16 juftmi: " + MathUtils.isEven(16));
        System.out.println("7 ning kvadrati: " + MathUtils.kvadrat(7));
        
        // new MathUtils(); // Kompilyatsiya xatosi: constructor MathUtils() is private
    }
}
```

## Tushuntirish va Mantiq:
Utility sinf yaratish qoidalari (Joshua Bloch, Effective Java):
1. Sinfni `final` qilish (meros olishni taqiqlash).
2. Konstruktorni `private` qilish (hech kim `new` qila olmasligi uchun).
3. Konstruktor ichida `UnsupportedOperationException` tashlash (hatto reflection orqali ham chaqirishni to'sish).
4. Barcha metod va konstantalarni `public static` qilish.

## Ishlash natijasi:
```text
16 juftmi: true
7 ning kvadrati: 49
```

---

# 171-Topshiriq: Sof funksiya (Pure Function) konsepsiyasi

## Topshiriq sharti:
Tashqi holatga bog'liq bo'lmagan va hech qanday nojo'ya ta'sir (side effect) ko'rsatmaydigan sof funksiya namunasini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    // Pure function: har doim bir xil kirishga bir xil chiqish beradi, tashqi holatga tegmaydi
    public static int hisoblaNarx(int asosiy, int soliqFoizi) {
        return asosiy + (asosiy * soliqFoizi / 100);
    }

    public static void main(String[] args) {
        int natija1 = hisoblaNarx(100000, 12);
        int natija2 = hisoblaNarx(100000, 12);
        
        System.out.println("Natija 1: " + natija1);
        System.out.println("Natija 2: " + natija2);
        System.out.println("Determinizm: " + (natija1 == natija2));
    }
}
```

## Tushuntirish va Mantiq:
Pure Function (Sof funksiya):
1. Deterministik: bir xil argumentlar uchun har doim aynan bir xil natija qaytaradi.
2. Side-effect free: hech qanday global o'zgaruvchini o'zgartirmaydi, konsolga yozmaydi, fayl/baza bilan bog'lanmaydi.
Bu funksional dasturlash va ko'p oqimli (concurrency) muhitlarda xavfsizlikning garovidir.

## Ishlash natijasi:
```text
Natija 1: 112000
Natija 2: 112000
Determinizm: true
```

---

# 172-Topshiriq: Metoddan bir nechta qiymat qaytarish: Java 16+ Record orqali

## Topshiriq sharti:
Metoddan bitta emas, bir nechta qiymatlarni (masalan, Min va Max) xavfsiz qaytarish uchun `record` dan foydalaning.

## Yechim (Java kodi):
```java
public class Solution {
    public record MinMax(int min, int max) {}

    public static MinMax findMinMax(int[] arr) {
        int min = arr[0];
        int max = arr[0];
        for (int x : arr) {
            if (x < min) min = x;
            if (x > max) max = x;
        }
        return new MinMax(min, max);
    }

    public static void main(String[] args) {
        int[] sonlar = {45, 12, 89, 3, 77};
        MinMax natija = findMinMax(sonlar);
        
        System.out.println("Minimal: " + natija.min());
        System.out.println("Maksimal: " + natija.max());
    }
}
```

## Tushuntirish va Mantiq:
Java-da metod rasman faqat bitta qiymat qaytaradi.
Bir nechta bog'liq qiymatlarni qaytarishning eng zamonaviy va toza usuli — Java 16 da kiritilgan lokal `record` yaratishdir. Bu ortiqcha sinflar va boilerplate kod yaratish zaruratini yo'qotadi.

## Ishlash natijasi:
```text
Minimal: 3
Maksimal: 89
```

---

# 173-Topshiriq: Hanoi minoralari (Towers of Hanoi) rekursiyasi

## Topshiriq sharti:
Klassik Hanoi minoralari boshqotirmasini rekursiv metod orqali hal qiluvchi dastur tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void hanoi(int n, char boshlangich, char yordamchi, char nishon) {
        if (n == 1) {
            System.out.println("Disk 1: " + boshlangich + " -> " + nishon);
            return;
        }
        hanoi(n - 1, boshlangich, nishon, yordamchi);
        System.out.println("Disk " + n + ": " + boshlangich + " -> " + nishon);
        hanoi(n - 1, yordamchi, boshlangich, nishon);
    }

    public static void main(String[] args) {
        int disklarSoni = 3;
        System.out.println("3 ta disk uchun qadamlar ketma-ketligi:");
        hanoi(disklarSoni, 'A', 'B', 'C');
    }
}
```

## Tushuntirish va Mantiq:
Hanoi minoralari algoritmi rekursiyaning qudratini ko'rsatadi:
1. `n-1` ta diskni boshlang'ichdan yordamchiga o'tkazish.
2. Eng katta n-diskni nishonga qo'yish.
3. `n-1` ta diskni yordamchidan nishonga ko'chirish.
Jami qadamlar soni `2^n - 1` ta bo'ladi (3 ta disk uchun 7 qadam).

## Ishlash natijasi:
```text
3 ta disk uchun qadamlar ketma-ketligi:
Disk 1: A -> C
Disk 2: A -> B
Disk 1: C -> B
Disk 3: A -> C
Disk 1: B -> A
Disk 2: B -> C
Disk 1: A -> C
```

---

# 174-Topshiriq: Rekursiv darajaga ko'tarish: Binary Exponentiation

## Topshiriq sharti:
`a^b` amalini O(log b) vaqtda tezkor hisoblovchi ikkilik darajaga ko'tarish algoritmini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static long tezkorDaraja(long asos, int daraja) {
        if (daraja == 0) return 1;
        if (daraja % 2 == 0) {
            long yarim = tezkorDaraja(asos, daraja / 2);
            return yarim * yarim;
        } else {
            return asos * tezkorDaraja(asos, daraja - 1);
        }
    }

    public static void main(String[] args) {
        long asos = 2;
        int daraja = 10;
        System.out.println(asos + "^" + daraja + " = " + tezkorDaraja(asos, daraja));
    }
}
```

## Tushuntirish va Mantiq:
Oddiy siklda `a^b` hisoblash `b` ta amal talab qiladi (O(b)).
Ikkilik daraja algoritmi (Binary Exponentiation) esa har bir juft darajada darajani 2 ga bo'ladi (`a^10 = (a^5)^2`).
Bu vaqt sarfini O(log b) gacha qisqartiradi.

## Ishlash natijasi:
```text
2^10 = 1024
```

---

# 175-Topshiriq: Varargs bilan oddiy parametrlarning birgalikda ishlatilishi

## Topshiriq sharti:
Formatlash satri va ixtiyoriy sondagi parametrlarni qabul qiluvchi custom logger metodini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void log(String prefiks, Object... xabarlar) {
        System.out.print("[" + prefiks + "] ");
        for (Object xabar : xabarlar) {
            System.out.print(xabar + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        log("INFO", "Tizim ishga tushdi", "Versiya: 2.1");
        log("ERROR", "Ulanish xatosi", 404, "Server javob bermadi");
    }
}
```

## Tushuntirish va Mantiq:
Varargs oldidan oddiy parametrlar (masalan `String prefiks`) qo'yilishi mumkin.
Bunda birinchi uzatilgan argument oddiy parametrga tushadi, qolgan barcha argumentlar esa avtomatik ravishda varargs massiviga yig'iladi.

## Ishlash natijasi:
```text
[INFO] Tizim ishga tushdi Versiya: 2.1 
[ERROR] Ulanish xatosi 404 Server javob bermadi
```

---

# 176-Topshiriq: Rekursiv massiv elementlari yig'indisini hisoblash

## Topshiriq sharti:
Massiv elementlari yig'indisini Divide and Conquer (bo'lib tashla va hukmronlik qil) tamoyilida rekursiv hisoblang.

## Yechim (Java kodi):
```java
public class Solution {
    public static int yigindi(int[] arr, int bosh, int oxir) {
        if (bosh == oxir) {
            return arr[bosh];
        }
        int orta = bosh + (oxir - bosh) / 2;
        return yigindi(arr, bosh, orta) + yigindi(arr, orta + 1, oxir);
    }

    public static void main(String[] args) {
        int[] sonlar = {5, 10, 15, 20, 25};
        int jami = yigindi(sonlar, 0, sonlar.length - 1);
        System.out.println("Massiv yig'indisi: " + jami);
    }
}
```

## Tushuntirish va Mantiq:
Massiv o'rtasidan ikkiga bo'linadi va chap hamda o'ng qismlarining yig'indisi alohida hisoblanib qo'shiladi.
Bu yondashuv parallel hisoblashlarga (ForkJoinPool) oson moslashadi.

## Ishlash natijasi:
```text
Massiv yig'indisi: 75
```

---

# 177-Topshiriq: Metodlarni haddan tashqari yuklashda noaniqlik (Ambiguity) xatosi

## Topshiriq sharti:
Kompilyator ikkita overload metod orasida qaysi birini tanlashni bilolmay qoladigan holatni tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void korsat(int a, long b) {
        System.out.println("int, long");
    }

    public static void korsat(long a, int b) {
        System.out.println("long, int");
    }

    public static void main(String[] args) {
        korsat(10, 20L); // Aniq mos keladi: (int, long)
        korsat(10L, 20); // Aniq mos keladi: (long, int)
        // korsat(10, 20); // KOMPILYATSIYA XATOSI: reference to korsat is ambiguous!
    }
}
```

## Tushuntirish va Mantiq:
Agar chaqiruv `korsat(10, 20)` ko'rinishida qilinsa, ikkala argument ham `int` bo'ladi.
Kompilyator birinchi argumentni widening qilib ikkinchisiga moslashtirishi ham, yoki ikkinchisini widening qilishi ham mumkin. Ikkala variant ham teng huquqli bo'lgani sababli kompilyator `ambiguous method call` xatosi bilan to'xtaydi.

## Ishlash natijasi:
```text
int, long
long, int
```

---

# 178-Topshiriq: Rekursiv ravishda ikkilik sanoq tizimiga o'tkazish

## Topshiriq sharti:
Butun musbat sonni rekursiya yordamida ikkilik satr ko'rinishiga o'tkazuvchi metod tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static String toBinary(int n) {
        if (n <= 1) return String.valueOf(n);
        return toBinary(n / 2) + (n % 2);
    }

    public static void main(String[] args) {
        int son = 45;
        System.out.println(son + " sonining ikkilik ko'rinishi: " + toBinary(son));
    }
}
```

## Tushuntirish va Mantiq:
Son har safar 2 ga butun bo'linadi va qoldig'i oxiriga ulab boriladi.
Rekursiyaning qaytish bosqichida qoldiqlar teskari tartibda (to'g'ri binar ketma-ketlikda) birlashadi.

## Ishlash natijasi:
```text
45 sonining ikkilik ko'rinishi: 101101
```

---

# 179-Topshiriq: Statik metodlarda instansiya obyektini qabul qilish

## Topshiriq sharti:
Statik metod obyekt nusxasini parametr sifatida qabul qilib uning maydonlari ustida amal bajarishi mumkinligini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class BankHisob {
        double balans;
        BankHisob(double b) { this.balans = b; }
    }

    public static void pulOtqaz(BankHisob qayerdan, BankHisob qayerga, double summa) {
        if (qayerdan.balans >= summa) {
            qayerdan.balans -= summa;
            qayerga.balans += summa;
            System.out.println("Muvaffaqiyatli o'tkazildi: " + summa);
        }
    }

    public static void main(String[] args) {
        BankHisob h1 = new BankHisob(1000);
        BankHisob h2 = new BankHisob(500);
        
        pulOtqaz(h1, h2, 300);
        System.out.println("h1 balans: " + h1.balans + ", h2 balans: " + h2.balans);
    }
}
```

## Tushuntirish va Mantiq:
Statik metod `this` ga ega bo'lmasa-da, metod parametrida uzatilgan ixtiyoriy instansiya obyektiga murojaat qila oladi va uning ochiq maydonlarini o'zgartira oladi.

## Ishlash natijasi:
```text
Muvaffaqiyatli o'tkazildi: 300.0
h1 balans: 700.0, h2 balans: 800.0
```

---

# 180-Topshiriq: Rekursiv massivda binar qidiruv

## Topshiriq sharti:
Binar qidiruv algoritmining rekursiv versiyasini amalga oshiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static int binarySearchRecursive(int[] arr, int target, int chap, int ong) {
        if (chap > ong) return -1;
        
        int orta = chap + (ong - chap) / 2;
        if (arr[orta] == target) return orta;
        
        if (arr[orta] > target) {
            return binarySearchRecursive(arr, target, chap, orta - 1);
        } else {
            return binarySearchRecursive(arr, target, orta + 1, ong);
        }
    }

    public static void main(String[] args) {
        int[] saralangan = {3, 9, 15, 27, 33, 49, 70};
        int target = 33;
        int indeks = binarySearchRecursive(saralangan, target, 0, saralangan.length - 1);
        System.out.println(target + " topilgan indeks: " + indeks);
    }
}
```

## Tushuntirish va Mantiq:
Rekursiv binar qidiruvda har bir qadamda oraliq chegaralari (`chap` va `ong`) o'zgaradi.
Base case: `chap > ong` bo'lsa element massivda yo'q (`-1`).

## Ishlash natijasi:
```text
33 topilgan indeks: 4
```

---

# 181-Topshiriq: Metod ichida o'zgaruvchilarni samarali qaytarish (Tail Call tushunchasi)

## Topshiriq sharti:
Java da Tail Call Optimization (TCO) rasman mavjud emasligini va uning o'rniga nima uchun iteratsiya afzalligini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    // Tail-recursive ko'rinishi
    public static long faktorialTail(int n, long akkumulyator) {
        if (n <= 1) return akkumulyator;
        return faktorialTail(n - 1, n * akkumulyator);
    }

    public static void main(String[] args) {
        long res = faktorialTail(5, 1);
        System.out.println("Tail-rekursiv natija: " + res);
    }
}
```

## Tushuntirish va Mantiq:
Tail Call — rekursiv chaqiruv funksiyaning eng so'nggi amali bo'lishidir.
Ba'zi tillar (Scala, Kotlin) buni bitta stack freymga yig'adi (TCO).
Biroq Java JVM xavfsizlik va stack trace yaxlitligini saqlash uchun TCO ni qo'llab-quvvatlamaydi. Shuning uchun Java-da chuqur rekursiyalar o'rniga oddiy iterativ sikllar (`while`/`for`) tavsiya etiladi.

## Ishlash natijasi:
```text
Tail-rekursiv natija: 120
```

---

# 182-Topshiriq: Massiv parametrlarini himoyalash: Defensive Copying

## Topshiriq sharti:
Metod qabul qilgan massivni tashqi modifikatsiyalardan saqlash uchun himoyaviy nusxa (defensive copy) olishni ko'rsating.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    static class TalabalarGuruhi {
        private final int[] baholar;

        public TalabalarGuruhi(int[] kiruvchiBaholar) {
            // Defensive copying: tashqi massivdan nusxa olamiz
            this.baholar = kiruvchiBaholar.clone();
        }

        public void chopEt() {
            System.out.println("Guruh baholari: " + Arrays.toString(baholar));
        }
    }

    public static void main(String[] args) {
        int[] original = {4, 5, 3};
        TalabalarGuruhi guruh = new TalabalarGuruhi(original);
        
        // Tashqaridagi massiv o'zgartiriladi
        original[0] = 1;
        
        guruh.chopEt(); // Ichki baholar o'zgarmay qolishi kerak!
    }
}
```

## Tushuntirish va Mantiq:
Agar konstruktor yoki metod kiruvchi massivni to'g'ridan-to'g'ri saqlab qo'ysa, tashqaridagi kod asl massivni o'zgartirganda ob'ekt ichidagi ma'lumot ham buziladi.
Buning oldini olish uchun har doim `kiruvchi.clone()` yoki `Arrays.copyOf()` orqali himoyaviy nusxa olinadi.

## Ishlash natijasi:
```text
Guruh baholari: [4, 5, 3]
```

---

# 183-Topshiriq: Rekursiv ravishda eng katta umumiy bo'luvchi yordamida EKUK topish

## Topshiriq sharti:
EKUB orqali ikki sonning eng kichik umumiy karralisini (EKUK / LCM) hisoblang.

## Yechim (Java kodi):
```java
public class Solution {
    public static int ekub(int a, int b) {
        return (b == 0) ? a : ekub(b, a % b);
    }

    public static int ekuk(int a, int b) {
        return (a * b) / ekub(a, b);
    }

    public static void main(String[] args) {
        int a = 12;
        int b = 18;
        System.out.println("EKUK(" + a + ", " + b + ") = " + ekuk(a, b));
    }
}
```

## Tushuntirish va Mantiq:
Matematik qoidaga ko'ra: `a * b = EKUB(a, b) * EKUK(a, b)`.
Demak, `EKUK(a, b) = (a * b) / EKUB(a, b)` formulasi orqali darhol topiladi.

## Ishlash natijasi:
```text
EKUK(12, 18) = 36
```

---

# 184-Topshiriq: Varargs da bo'sh argumentlarni boshqarish

## Topshiriq sharti:
Varargs metodiga umuman argument uzatilmaganda xatolik bermasdan bo'sh massiv hosil bo'lishini tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void tekshir(String... parametrlar) {
        System.out.println("Massiv null emas: " + (parametrlar != null));
        System.out.println("Massiv uzunligi: " + parametrlar.length);
    }

    public static void main(String[] args) {
        tekshir(); // Hech qanday argument yo'q
    }
}
```

## Tushuntirish va Mantiq:
Agar varargs metodiga hech qanday argument uzatilmasa, JVM avtomatik ravishda 0 uzunlikdagi bo'sh massiv (`new String[0]`) yaratadi.
U hech qachon `null` bo'lmaydi (agar chaqiruvchi atayin `tekshir((String[]) null)` deb yozmasa).

## Ishlash natijasi:
```text
Massiv null emas: true
Massiv uzunligi: 0
```

---

# 185-Topshiriq: Metod ichidan istisno tashlash orqali bajarilishni to'xtatish

## Topshiriq sharti:
Metod shartlari buzilganda `throw new RuntimeException()` orqali boshqaruvni to'xtatishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static double bolish(double a, double b) {
        if (b == 0.0) {
            throw new IllegalArgumentException("Bo'luvchi nol bo'lishi mumkin emas!");
        }
        return a / b;
    }

    public static void main(String[] args) {
        try {
            System.out.println("10 / 2 = " + bolish(10, 2));
            bolish(10, 0);
        } catch (IllegalArgumentException e) {
            System.out.println("Xato ushlandi: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
`throw` operatori metod bajarilishini darhol to'xtatadi va boshqaruvni eng yaqin mos `catch` blokiga uzatadi.
Bu noto'g'ri hisob-kitoblar tarqalishining oldini oladi.

## Ishlash natijasi:
```text
10 / 2 = 5.0
Xato ushlandi: Bo'luvchi nol bo'lishi mumkin emas!
```

---

# 186-Topshiriq: Rekursiv daraxt tuzilmasini aylanib chiqish (Tree Traversal)

## Topshiriq sharti:
Binar daraxt (Binary Tree) tugunlarini in-order tartibda rekursiv chop etuvchi metod yozing.

## Yechim (Java kodi):
```java
public class Solution {
    static class Node {
        int qiymat;
        Node chap, ong;
        Node(int val) { this.qiymat = val; }
    }

    public static void inOrder(Node ildiz) {
        if (ildiz == null) return;
        inOrder(ildiz.chap);
        System.out.print(ildiz.qiymat + " ");
        inOrder(ildiz.ong);
    }

    public static void main(String[] args) {
        Node root = new Node(10);
        root.chap = new Node(5);
        root.ong = new Node(20);
        
        System.out.print("In-order aylanib chiqish: ");
        inOrder(root);
        System.out.println();
    }
}
```

## Tushuntirish va Mantiq:
Daraxtlar va graflarni aylanib chiqish rekursiyaning eng tabiiy va qulay sohasidir.
In-order aylanib chiqishda: chap farzand -> ota tugun -> o'ng farzand tartibida chop etiladi.
Binar qidiruv daraxtida bu sonlarni o'sish tartibida chiqaradi.

## Ishlash natijasi:
```text
In-order aylanib chiqish: 5 10 20
```

---

# 187-Topshiriq: Statik metodlarni polimorfik qayta aniqlash (Override) mumkin emasligi

## Topshiriq sharti:
Statik metodlar qayta aniqlanmasligini (Method Hiding hodisasi) isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    static class Ota {
        public static void salom() { System.out.println("Ota klass statik metodi"); }
    }

    static class Bola extends Ota {
        public static void salom() { System.out.println("Bola klass statik metodi"); }
    }

    public static void main(String[] args) {
        Ota o = new Bola();
        o.salom(); // Ota klassniki chaqiriladi!
    }
}
```

## Tushuntirish va Mantiq:
Java-da statik metodlar obyektga emas, sinf tipiga bog'langan.
`Ota o = new Bola()` holatida ko'rsatkich tipi `Ota` bo'lgani sababli, kompilyatsiya vaqtida `Ota.salom()` bog'lanadi (Static binding).
Statik metodlarda polimorfizm (Overriding) ishlamaydi, bu faqat Method Hiding (yashirish) deb ataladi.

## Ishlash natijasi:
```text
Ota klass statik metodi
```

---

# 188-Topshiriq: Rekursiv ravishda massiv elementlari orasidagi maksimum

## Topshiriq sharti:
Massivning maksimal elementini bo'lib tashla usulida rekursiv topuvchi metod tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static int findMax(int[] arr, int bosh, int oxir) {
        if (bosh == oxir) return arr[bosh];
        int orta = bosh + (oxir - bosh) / 2;
        int chapMax = findMax(arr, bosh, orta);
        int ongMax = findMax(arr, orta + 1, oxir);
        return Math.max(chapMax, ongMax);
    }

    public static void main(String[] args) {
        int[] sonlar = {12, 54, 2, 99, 34};
        System.out.println("Maksimal element: " + findMax(sonlar, 0, sonlar.length - 1));
    }
}
```

## Tushuntirish va Mantiq:
Massiv 1 ta element qolguncha ikkiga bo'linadi. So'ngra pastdan yuqoriga qaytishda har ikkala qismning kattasi `Math.max()` orqali tanlab olinadi.

## Ishlash natijasi:
```text
Maksimal element: 99
```

---

# 189-Topshiriq: Parametrlarni o'zgartirishdan tiyilish (Avoiding Side-effects on Arguments)

## Topshiriq sharti:
Metodga kirgan parametr ro'yxatini to'g'ridan-to'g'ri o'zgartirmasdan, yangi natija hosil qilib qaytarish amaliyotini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    // Noto'g'ri (Side-effect bor)
    public static void yomonUsul(int[] arr) {
        for (int i = 0; i < arr.length; i++) arr[i] *= 2;
    }

    // To'g'ri (Side-effect yo'q, toza funksiya)
    public static int[] yaxshiUsul(int[] arr) {
        int[] yangi = new int[arr.length];
        for (int i = 0; i < arr.length; i++) yangi[i] = arr[i] * 2;
        return yangi;
    }

    public static void main(String[] args) {
        int[] sonlar = {1, 2, 3};
        int[] natija = yaxshiUsul(sonlar);
        
        System.out.println("Asl massiv o'zgarmadi: " + Arrays.toString(sonlar));
        System.out.println("Yangi massiv hosil bo'ldi: " + Arrays.toString(natija));
    }
}
```

## Tushuntirish va Mantiq:
Side-effect (nojo'ya ta'sir) larni kamaytirish dasturda kutilmagan xatoliklarni keskin kamaytiradi.
Metod o'ziga berilgan argumentlarni buzmasdan, natijani yangi obyekt ko'rinishida qaytarishi tavsiya etiladi.

## Ishlash natijasi:
```text
Asl massiv o'zgarmadi: [1, 2, 3]
Yangi massiv hosil bo'ldi: [2, 4, 6]
```

---

# 190-Topshiriq: Metod ichida lokal sinflar (Local Classes)

## Topshiriq sharti:
Metod tanasi ichida maxsus yordamchi sinf e'lon qilib undan foydalanishni namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void hisobotTayyorla() {
        class SatrFormatlovchi {
            String qator(String nom, int qiymat) {
                return String.format("%-15s: %d", nom, qiymat);
            }
        }

        SatrFormatlovchi f = new SatrFormatlovchi();
        System.out.println(f.qator("Foydalanuvchilar", 150));
        System.out.println(f.qator("Faol sessiyalar", 42));
    }

    public static void main(String[] args) {
        hisobotTayyorla();
    }
}
```

## Tushuntirish va Mantiq:
Lokal sinf (Local Class) to'g'ridan-to'g'ri metod ichida e'lon qilinadi.
U faqat o'sha metod ichida ko'rinadi va tashqaridan unga murojaat qilib bo'lmaydi.
U metodning lokal `final` yoki `effectively final` o'zgaruvchilariga kirish huquqiga ega.

## Ishlash natijasi:
```text
Foydalanuvchilar   : 150
Faol sessiyalar : 42
```

---

# 191-Topshiriq: Varargs da massiv o'rniga null uzatilganda yuz beradigan xato

## Topshiriq sharti:
Varargs metodga `null` uzatilganda qanday ehtiyot choralari ko'rilishi kerakligini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void chopEt(String... elementlar) {
        if (elementlar == null) {
            System.out.println("Diqqat: Varargs massivi null kirdi!");
            return;
        }
        System.out.println("Elementlar soni: " + elementlar.length);
    }

    public static void main(String[] args) {
        chopEt("A", "B");
        chopEt((String[]) null); // Qasddan null massiv uzatildi
    }
}
```

## Tushuntirish va Mantiq:
Agar dasturchi varargs parametriga aniq kasting bilan `(String[]) null` uzatsa, `elementlar` o'zgaruvchisining o'zi `null` bo'ladi.
Shu bois himoyalangan kodda `if (elementlar == null)` tekshiruvi bo'lishi maqsadga muvofiqdir.

## Ishlash natijasi:
```text
Elementlar soni: 2
Diqqat: Varargs massivi null kirdi!
```

---

# 192-Topshiriq: Rekursiv ravishda sonning raqamlarini chiqarish

## Topshiriq sharti:
Sonning raqamlarini chapdan o'ngga qarab rekursiv tartibda chop etuvchi metod yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void printDigits(int n) {
        if (n < 10) {
            System.out.print(n + " ");
            return;
        }
        printDigits(n / 10);
        System.out.print((n % 10) + " ");
    }

    public static void main(String[] args) {
        System.out.print("7492 ning raqamlari: ");
        printDigits(7492);
        System.out.println();
    }
}
```

## Tushuntirish va Mantiq:
Avval yuqori xonalar rekursiv chaqiriladi (`printDigits(n / 10)`), so'ngra qaytish vaqtida oxirgi raqam (`n % 10`) chop etiladi.
Bu orqali son chapdan o'ngga to'g'ri tartibda chiqadi.

## Ishlash natijasi:
```text
7492 ning raqamlari: 7 4 9 2
```

---

# 193-Topshiriq: Statik factory metodlar (Static Factory Methods)

## Topshiriq sharti:
Konstruktor o'rniga tushunarli nomga ega statik fabrika metodlaridan foydalanish afzalliklarini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Vaqt {
        private final int soniyalar;
        
        private Vaqt(int s) { this.soniyalar = s; }

        public static Vaqt daqiqadan(int daqiqa) {
            return new Vaqt(daqiqa * 60);
        }

        public static Vaqt soatdan(int soat) {
            return new Vaqt(soat * 3600);
        }

        public int getSoniyalar() { return soniyalar; }
    }

    public static void main(String[] args) {
        Vaqt v1 = Vaqt.daqiqadan(5);
        Vaqt v2 = Vaqt.soatdan(2);
        
        System.out.println("5 daqiqa: " + v1.getSoniyalar() + " soniya");
        System.out.println("2 soat: " + v2.getSoniyalar() + " soniya");
    }
}
```

## Tushuntirish va Mantiq:
Statik fabrika metodlarining konstruktordan ustunliklari:
1. Ularning nomi bor (konstruktorda faqat sinf nomi bo'ladi). `daqiqadan(5)` nima yaratayotganini aniq bildiradi.
2. Har safar yangi obyekt yaratishi shart emas, keshlangan obyektni ham qaytarishi mumkin.
3. Sub-sinf obyektlarini qaytarish imkoniyatiga ega.

## Ishlash natijasi:
```text
5 daqiqa: 300 soniya
2 soat: 7200 soniya
```

---

# 194-Topshiriq: Rekursiv ravishda kombinatsiyalarni hisoblash: C(n, k)

## Topshiriq sharti:
Paskal formulasi `C(n, k) = C(n-1, k-1) + C(n-1, k)` asosida kombinatsiyalar sonini rekursiv hisoblang.

## Yechim (Java kodi):
```java
public class Solution {
    public static int kombinatsiya(int n, int k) {
        if (k == 0 || k == n) return 1;
        return kombinatsiya(n - 1, k - 1) + kombinatsiya(n - 1, k);
    }

    public static void main(String[] args) {
        int n = 5;
        int k = 2;
        System.out.println("C(" + n + ", " + k + ") = " + kombinatsiya(n, k));
    }
}
```

## Tushuntirish va Mantiq:
Kombinatorikada `n` ta elementdan `k` tasini tanlash kombinatsiyasi Paskal qoidasi bilan hisoblanadi.
Base case: `k == 0` yoki `k == n` bo'lganda natija `1` ga teng.

## Ishlash natijasi:
```text
C(5, 2) = 10
```

---

# 195-Topshiriq: Metodlarda chaining (zanjirli chaqiruv) texnikasi

## Topshiriq sharti:
Metoddan `this` ni qaytarish orqali zanjir ko'rinishida chaqiriluvchi metodlar (Method Chaining) tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sozlamalar {
        private String server;
        private int port;
        private boolean ssl;

        public Sozlamalar setServer(String s) {
            this.server = s;
            return this;
        }

        public Sozlamalar setPort(int p) {
            this.port = p;
            return this;
        }

        public Sozlamalar setSsl(boolean ssl) {
            this.ssl = ssl;
            return this;
        }

        public void chopEt() {
            System.out.println("Server: " + server + ", Port: " + port + ", SSL: " + ssl);
        }
    }

    public static void main(String[] args) {
        new Sozlamalar()
            .setServer("api.uz")
            .setPort(443)
            .setSsl(true)
            .chopEt();
    }
}
```

## Tushuntirish va Mantiq:
Method Chaining (Fluent Interface pattern):
Har bir setter metod o'z vazifasini bajarib bo'lgach, joriy obyektni (`return this;`) qaytaradi.
Bu metodlarni nuqta orqali bir-biriga ulab zanjir hosil qilish imkonini beradi (Builder pattern poydevori).

## Ishlash natijasi:
```text
Server: api.uz, Port: 443, SSL: true
```

---

# 196-Topshiriq: Rekursiv ravishda 2D matritsada Flood Fill (Bo'yash) algoritmi

## Topshiriq sharti:
Grafik dasturlardagi 'Bucket Fill' (bo'yoq quyish) vositasining rekursiv Flood Fill algoritmini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void floodFill(int[][] rasm, int r, int c, int yangiRang, int eskiRang) {
        if (r < 0 || r >= rasm.length || c < 0 || c >= rasm[0].length) return;
        if (rasm[r][c] != eskiRang || rasm[r][c] == yangiRang) return;
        
        rasm[r][c] = yangiRang;
        
        floodFill(rasm, r + 1, c, yangiRang, eskiRang); // Past
        floodFill(rasm, r - 1, c, yangiRang, eskiRang); // Tepa
        floodFill(rasm, r, c + 1, yangiRang, eskiRang); // O'ng
        floodFill(rasm, r, c - 1, yangiRang, eskiRang); // Chap
    }

    public static void main(String[] args) {
        int[][] rasm = {
            {1, 1, 1},
            {1, 1, 0},
            {1, 0, 1}
        };
        
        floodFill(rasm, 1, 1, 2, 1);
        
        System.out.println("Bo'yalgandan keyingi holat:");
        for (int[] row : rasm) {
            System.out.println(row[0] + " " + row[1] + " " + row[2]);
        }
    }
}
```

## Tushuntirish va Mantiq:
Flood Fill algoritmi 4 tomonga (tepa, past, o'ng, chap) rekursiv tarqaladi.
Tegishli eski rangdagi barcha bog'langan yacheykalarni yangi rangga bo'yaydi. Bu DFS (Depth-First Search) ning amaliy namunasidir.

## Ishlash natijasi:
```text
Bo'yalgandan keyingi holat:
2 2 2
2 2 0
2 0 1
```

---

# 197-Topshiriq: Rekursiv ravishda 2D matritsa determinanti (Laplas yoyilmasi)

## Topshiriq sharti:
2x2 matritsaning determinantini hisoblovchi metod tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static int determinant2x2(int[][] m) {
        return (m[0][0] * m[1][1]) - (m[0][1] * m[1][0]);
    }

    public static void main(String[] args) {
        int[][] matritsa = {
            {4, 6},
            {3, 8}
        };
        int det = determinant2x2(matritsa);
        System.out.println("Determinant: " + det);
    }
}
```

## Tushuntirish va Mantiq:
2x2 matritsada determinant: `a*d - b*c`.
Ushbu metod yuqori o'lchamli matritsalarning determinantini Laplas bo'yicha rekursiv hisoblashda asosiy tayanch shart (base case) vazifasini o'taydi.

## Ishlash natijasi:
```text
Determinant: 14
```

---

# 198-Topshiriq: Rekursiv ravishda to'plamning barcha qism-to'plamlari (Subsets)

## Topshiriq sharti:
Berilgan sonlar to'plamining barcha mumkin bo'lgan qism-to'plamlarini (Power Set) rekursiv generatsiya qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void generatsiya(int[] arr, int indeks, String joriy) {
        if (indeks == arr.length) {
            System.out.println("{" + joriy + "}");
            return;
        }
        // Elementni olmaymiz
        generatsiya(arr, indeks + 1, joriy);
        
        // Elementni olamiz
        String yangi = joriy.isEmpty() ? "" + arr[indeks] : joriy + ", " + arr[indeks];
        generatsiya(arr, indeks + 1, yangi);
    }

    public static void main(String[] args) {
        int[] tolam = {1, 2};
        System.out.println("Barcha qism-to'plamlar:");
        generatsiya(tolam, 0, "");
    }
}
```

## Tushuntirish va Mantiq:
Har bir element uchun ikkita qaror bor: yo uni to'plamga olamiz, yo olmaymiz.
`N` ta elementdan iborat to'plam jami `2^N` ta qism-to'plamga ega bo'ladi (2 ta element uchun 4 ta: {}, {2}, {1}, {1, 2}).

## Ishlash natijasi:
```text
Barcha qism-to'plamlar:
{}
{2}
{1}
{1, 2}
```

---

# 199-Topshiriq: Metodlarga funksional callback uzatish asoslari

## Topshiriq sharti:
Metodga bajarilishi kerak bo'lgan mantiqni (callback interfeysi) parametr sifatida uzatishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    interface Amal {
        int bajar(int x);
    }

    public static void massivniQaytaIshla(int[] arr, Amal amal) {
        for (int i = 0; i < arr.length; i++) {
            arr[i] = amal.bajar(arr[i]);
        }
    }

    public static void main(String[] args) {
        int[] sonlar = {1, 2, 3, 4};
        
        // Har bir sonni kvadratiga oshirish callback mantiqi
        massivniQaytaIshla(sonlar, x -> x * x);
        
        System.out.print("Qayta ishlangan massiv: ");
        for (int s : sonlar) System.out.print(s + " ");
        System.out.println();
    }
}
```

## Tushuntirish va Mantiq:
Metod parametrlari faqat son yoki satr emas, balki xulq-atvor (behavior) ham bo'lishi mumkin.
Bu interfeys va lambdalar orqali Strategy pattern va funksional dasturlashni amalga oshirishning poydevoridir.

## Ishlash natijasi:
```text
Qayta ishlangan massiv: 1 4 9 16
```

---

# 200-Topshiriq: Xulosa topshiriq: Bank hisob operatsiyalari va audit xizmati

## Topshiriq sharti:
Metodlar, overloading, varargs, pass-by-value, validatsiya va statik yordamchilarni birlashtirgan bank hisob-kitob xizmati tizimini yarating.

## Yechim (Java kodi):
```java
import java.util.Objects;

public class Solution {
    public record Tranzaksiya(String turi, double summa, String tafsilot) {}

    static class BankHisob {
        private final String hisobRaqam;
        private double balans;

        public BankHisob(String hisobRaqam, double boshlangichBalans) {
            this.hisobRaqam = Objects.requireNonNull(hisobRaqam, "Hisob raqam bo'sh bo'lishi mumkin emas!");
            if (boshlangichBalans < 0) throw new IllegalArgumentException("Balans manfiy bo'lolmaydi!");
            this.balans = boshlangichBalans;
        }

        public double getBalans() { return balans; }
        public String getHisobRaqam() { return hisobRaqam; }
        
        protected void depozit(double summa) { this.balans += summa; }
        protected void yechish(double summa) { this.balans -= summa; }
    }

    public static final class BankService {
        private BankService() {}

        public static Tranzaksiya pulKiritish(BankHisob hisob, double summa) {
            if (summa <= 0) throw new IllegalArgumentException("Summa musbat bo'lishi shart!");
            hisob.depozit(summa);
            return new Tranzaksiya("KIRIM", summa, "Hisob to'ldirildi");
        }

        public static Tranzaksiya pulYechish(BankHisob hisob, double summa) {
            if (summa > hisob.getBalans()) throw new IllegalStateException("Mablag' yetarli emas!");
            hisob.yechish(summa);
            return new Tranzaksiya("CHIQIM", summa, "Mablag' yechildi");
        }

        // Overload: pul o'tkazish
        public static void otkazma(BankHisob qayerdan, BankHisob qayerga, double summa) {
            pulYechish(qayerdan, summa);
            pulKiritish(qayerga, summa);
            System.out.printf("O'tkazma: %.2f so'm [%s -> %s]
", summa, qayerdan.getHisobRaqam(), qayerga.getHisobRaqam());
        }

        // Varargs audit
        public static void audit(Tranzaksiya... tranzaksiyalar) {
            System.out.println("=== TRANZAKSIYALAR AUDITI ===");
            for (Tranzaksiya t : tranzaksiyalar) {
                System.out.printf("Turi: %-7s | Summa: %10.2f so'm | Izoh: %s
", t.turi(), t.summa(), t.tafsilot());
            }
        }
    }

    public static void main(String[] args) {
        BankHisob h1 = new BankHisob("202080001001", 500000.0);
        BankHisob h2 = new BankHisob("202080001002", 100000.0);
        
        Tranzaksiya t1 = BankService.pulKiritish(h1, 200000.0);
        BankService.otkazma(h1, h2, 150000.0);
        Tranzaksiya t2 = new Tranzaksiya("OTKAZMA", 150000.0, "Ichki bank o'tkazmasi");
        
        BankService.audit(t1, t2);
        
        System.out.printf("Yakuniy h1 balans: %.2f so'm
", h1.getBalans());
        System.out.printf("Yakuniy h2 balans: %.2f so'm
", h2.getBalans());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu keng qamrovli tizimda:
1. `record Tranzaksiya` ma'lumotlar tashuvchi o'zgarmas model sifatida ishlatildi.
2. `Objects.requireNonNull` va `IllegalArgumentException` bilan kiruvchi ma'lumotlar xavfsizlandi.
3. Utility sinf (`BankService`) orqali biznes mantiq ajratildi.
4. Pass-by-value asosida hisob obyektlari holati boshqarildi.
5. `otkazma` va `audit` (varargs) metodlari orqali modulli arxitektura namoyish etildi.

## Ishlash natijasi:
```text
O'tkazma: 150000.00 so'm [202080001001 -> 202080001002]
=== TRANZAKSIYALAR AUDITI ===
Turi: KIRIM   | Summa:  200000.00 so'm | Izoh: Hisob to'ldirildi
Turi: OTKAZMA | Summa:  150000.00 so'm | Izoh: Ichki bank o'tkazmasi
Yakuniy h1 balans: 550000.00 so'm
Yakuniy h2 balans: 250000.00 so'm
```
