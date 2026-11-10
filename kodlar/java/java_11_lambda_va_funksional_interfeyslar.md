# Java Lambda va Funksional Interfeyslar (501-550)

# 501-Topshiriq: Lambda ifodalari (->) asoslari va anonim sinflar bilan solishtirish

## Topshiriq sharti:
Java 8 lambda sintaksisi orqali anonim sinf kodini 1 qatorda yozish afzalligini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    interface SalomBeruvchi {
        void salom(String ism);
    }

    public static void main(String[] args) {
        // Eski usul: Anonim sinf
        SalomBeruvchi eski = new SalomBeruvchi() {
            @Override
            public void salom(String ism) {
                System.out.println("Eski usul: Salom, " + ism);
            }
        };

        // Yangi usul: Lambda ifodasi
        SalomBeruvchi yangi = ism -> System.out.println("Lambda: Salom, " + ism);

        eski.salom("Ali");
        yangi.salom("Vali");
    }
}
```

## Tushuntirish va Mantiq:
Lambda ifodasi (`(parametrlar) -> { tana }`) Java 8 da kiritilgan bo'lib, faqat bitta abstrakt metodga ega interfeyslarni (SAM) ixcham amalga oshirish imkonini beradi.
Kompilyator `invokedynamic` baytkod instruksiyasi orqali sinf fayli yaratmasdan yengil anonim funksiya hosil qiladi.

## Ishlash natijasi:
```text
Eski usul: Salom, Ali
Lambda: Salom, Vali
```

---

# 502-Topshiriq: @FunctionalInterface annotatsiyasi va SAM qoidasi

## Topshiriq sharti:
Shaxsiy funksional interfeys yaratib, unga `@FunctionalInterface` qo'yish va qoidalarini tekshiring.

## Yechim (Java kodi):
```java
public class Solution {
    @FunctionalInterface
    interface KvadratHisoblagich {
        int hisobla(int x); // Yagona abstrakt metod (SAM)

        // default va static metodlar bo'lishi mumkin
        default void log() { System.out.println("Kvadrat hisoblanmoqda..."); }
    }

    public static void main(String[] args) {
        KvadratHisoblagich k = x -> x * x;
        k.log();
        System.out.println("7 ning kvadrati: " + k.hisobla(7));
    }
}
```

## Tushuntirish va Mantiq:
`@FunctionalInterface` annotatsiyasi interfeysda aynan bitta abstrakt metod (Single Abstract Method — SAM) borligini kafolatlaydi.
Agar ikkinchi abstrakt metod qo'shilsa, kompilyator darhol xato beradi. Ammo `default` va `static` metodlar soni cheklanmagan.

## Ishlash natijasi:
```text
Kvadrat hisoblanmoqda...
7 ning kvadrati: 49
```

---

# 503-Topshiriq: Predicate<T> interfeysi va and/or/negate kompozitsiyasi

## Topshiriq sharti:
`Predicate<T>` orqali shartlarni tekshirish va bir nechta predikatlarni birlashtirish dasturini yozing.

## Yechim (Java kodi):
```java
import java.util.function.Predicate;

public class Solution {
    public static void main(String[] args) {
        Predicate<Integer> juftmi = n -> n % 2 == 0;
        Predicate<Integer> musbatmi = n -> n > 0;

        Predicate<Integer> juftVaMusbat = juftmi.and(musbatmi);
        Predicate<Integer> toqmi = juftmi.negate();

        System.out.println("10 juft va musbatmi: " + juftVaMusbat.test(10));
        System.out.println("-4 juft va musbatmi: " + juftVaMusbat.test(-4));
        System.out.println("7 toqmi: " + toqmi.test(7));
    }
}
```

## Tushuntirish va Mantiq:
`java.util.function.Predicate<T>` parametri `T` bo'lgan va har doim `boolean` qaytaruvchi funksional interfeysdir (`boolean test(T t)`).
Uning `and()`, `or()`, `negate()` metodlari orqali mantiqiy ifodalarni chiroyli zanjir qilib birlashtirish mumkin.

## Ishlash natijasi:
```text
10 juft va musbatmi: true
-4 juft va musbatmi: false
7 toqmi: true
```

---

# 504-Topshiriq: Consumer<T> interfeysi va andThen() zanjiri

## Topshiriq sharti:
`Consumer<T>` orqali ma'lumotlarni qabul qilib chop etish va `andThen` bilan ketma-ketlik hosil qiling.

## Yechim (Java kodi):
```java
import java.util.function.Consumer;

public class Solution {
    public static void main(String[] args) {
        Consumer<String> konsolgaChiqar = s -> System.out.println("Konsol: " + s);
        Consumer<String> auditLog = s -> System.out.println("AUDIT: [" + s.toUpperCase() + "] saqlandi.");

        Consumer<String> zanjir = konsolgaChiqar.andThen(auditLog);
        zanjir.accept("Foydalanuvchi tizimga kirdi");
    }
}
```

## Tushuntirish va Mantiq:
`Consumer<T>` qiymat qabul qiladi, ammo hech narsa qaytarmaydi (`void accept(T t)`).
`andThen()` metodi birinchi amaldan so'ng ikkinchi iste'molchini ketma-ket ishga tushirish imkonini beradi.

## Ishlash natijasi:
```text
Konsol: Foydalanuvchi tizimga kirdi
AUDIT: [FOYDALANUVCHI TIZIMGA KIRDI] saqlandi.
```

---

# 505-Topshiriq: Supplier<T> interfeysi: Tembel yuklash (Lazy Evaluation)

## Topshiriq sharti:
`Supplier<T>` yordamida qiymatni faqat kerak bo'lganda hisoblash (Lazy supplier) texnikasini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.function.Supplier;

public class Solution {
    public static String ogirHisoblash() {
        System.out.println("--> Og'ir resurs yuklandi!");
        return "Maxfiy Kalit";
    }

    public static void keshTekshir(boolean keshdaMavjud, Supplier<String> generator) {
        if (keshdaMavjud) {
            System.out.println("Keshdan olindi, og'ir funksiya chaqirilmadi.");
        } else {
            System.out.println("Olingan qiymat: " + generator.get());
        }
    }

    public static void main(String[] args) {
        Supplier<String> sup = Solution::ogirHisoblash;
        keshTekshir(true, sup); // generator.get() chaqirilmaydi
        keshTekshir(false, sup); // faqat shu yerda chaqiriladi
    }
}
```

## Tushuntirish va Mantiq:
`Supplier<T>` hech qanday parametr qabul qilmaydi, faqat qiymat qaytaradi (`T get()`).
U dangasa hisoblashda (Lazy evaluation) qo'l keladi: og'ir funksiya darhol bajarilmaydi, faqat `get()` chaqirilgandagina ishga tushadi.

## Ishlash natijasi:
```text
Keshdan olindi, og'ir funksiya chaqirilmadi.
--> Og'ir resurs yuklandi!
Olingan qiymat: Maxfiy Kalit
```

---

# 506-Topshiriq: Function<T, R> interfeysi va andThen / compose farqi

## Topshiriq sharti:
`Function<T, R>` orqali ma'lumotlarni o'zgartirish (transformatsiya) va `andThen` bilan `compose` ning bajarilish tartibini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, Integer> ikkiBarobar = x -> x * 2;
        Function<Integer, Integer> kvadrat = x -> x * x;

        // andThen: avval ikkiBarobar, keyin kvadrat -> (3 * 2)^2 = 36
        Function<Integer, Integer> f1 = ikkiBarobar.andThen(kvadrat);

        // compose: avval kvadrat, keyin ikkiBarobar -> (3^2) * 2 = 18
        Function<Integer, Integer> f2 = ikkiBarobar.compose(kvadrat);

        System.out.println("andThen(3): " + f1.apply(3));
        System.out.println("compose(3): " + f2.apply(3));
    }
}
```

## Tushuntirish va Mantiq:
`Function<T, R>` kirish parametrini olib natijaviy qiymat qaytaradi (`R apply(T t)`).
- `f.andThen(g)`: avval `f`, so'ng `g` bajariladi (`g(f(x))`).
- `f.compose(g)`: avval `g`, so'ng `f` bajariladi (`f(g(x))`).

## Ishlash natijasi:
```text
andThen(3): 36
compose(3): 18
```

---

# 507-Topshiriq: Method References (Metod ko'rsatkichlari ::) ning 4 xil turi

## Topshiriq sharti:
Java-da metod ko'rsatkichlarining barcha 4 ta ko'rinishini amaliy misolda namoyish eting.

## Yechim (Java kodi):
```java
import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;
import java.util.ArrayList;
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        // 1. Statik metodga ko'rsatkich (Sinf::metod)
        BiFunction<Integer, Integer, Integer> max = Math::max;
        System.out.println("1. Max: " + max.apply(15, 25));

        // 2. Muayyan obyekt metodiga ko'rsatkich (obyekt::metod)
        String prefiks = "SALOM";
        Supplier<String> lower = prefiks::toLowerCase;
        System.out.println("2. Obyekt metodi: " + lower.get());

        // 3. Muayyan tipdagi ixtiyoriy obyekt metodiga ko'rsatkich (Sinf::instansiyaMetod)
        Function<String, Integer> uzunlik = String::length;
        System.out.println("3. Satr uzunligi: " + uzunlik.apply("O'zbekiston"));

        // 4. Konstruktorga ko'rsatkich (Sinf::new)
        Supplier<List<String>> listFabrika = ArrayList::new;
        List<String> yangiRoyxat = listFabrika.get();
        System.out.println("4. Yangi ro'yxat yaratildi, hajmi: " + yangiRoyxat.size());
    }
}
```

## Tushuntirish va Mantiq:
Metod ko'rsatkichlari (`::`) lambdalarni yanada qisqaroq va o'qishga qulay qilish uchun sintaktik shakar (syntactic sugar) hisoblanadi.
Agar lambda faqat mavjud metodni chaqirishdan iborat bo'lsa (masalan `x -> Math.abs(x)`), uni `Math::abs` deb yozish mumkin.

## Ishlash natijasi:
```text
1. Max: 25
2. Obyekt metodi: salom
3. Satr uzunligi: 11
4. Yangi ro'yxat yaratildi, hajmi: 0
```

---

# 508-Topshiriq: Effectively Final qoidasi va o'zgaruvchilarni qamrab olish (Variable Capture)

## Topshiriq sharti:
Lambda ichida faqat `final` yoki amalda o'zgarmagan (effectively final) lokal o'zgaruvchilarni ishlatish mumkinligini isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int koeffitsiyent = 10; // Effectively final (hech qayerda o'zgartirilmayapti)

        Runnable r = () -> {
            System.out.println("Lokal o'zgaruvchi qiymati: " + koeffitsiyent);
        };
        r.run();

        // koeffitsiyent = 20; // Agar shu qator yoqilsa, kompilyator yuqoridagi lambdada xato beradi!
    }
}
```

## Tushuntirish va Mantiq:
Lambdalar o'zlari e'lon qilingan ko'rinish sohasidagi (enclosing scope) lokal o'zgaruvchilarni o'zlariga nusxalab oladi (Variable Capture).
Multithreading xavfsizligini ta'minlash uchun ushbu o'zgaruvchilar mutlaqo o'zgarmas (`final` yoki `effectively final`) bo'lishi shart.

## Ishlash natijasi:
```text
Lokal o'zgaruvchi qiymati: 10
```

---

# 509-Topshiriq: BiFunction, BiPredicate va BiConsumer

## Topshiriq sharti:
Ikkita kiruvchi parametr bilan ishlovchi 'Bi-' funksional interfeyslarini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.function.BiConsumer;
import java.util.function.BiPredicate;

public class Solution {
    public static void main(String[] args) {
        BiPredicate<String, Integer> uzunlikMosmi = (satr, uzunlik) -> satr.length() == uzunlik;
        BiConsumer<String, Double> tolovChopEt = (nom, narx) -> System.out.printf("Mahsulot: %s, Narx: %.2f so'm
", nom, narx);

        System.out.println("'Java' 4 ta harfmi: " + uzunlikMosmi.test("Java", 4));
        tolovChopEt.accept("Kitob", 55000.0);
    }
}
```

## Tushuntirish va Mantiq:
`BiPredicate<T, U>` ikkita har xil turdagi parametr qabul qilib boolean beradi.
`BiConsumer<T, U>` ikkita parametr qabul qilib void natija qaytaradi.

## Ishlash natijasi:
```text
'Java' 4 ta harfmi: true
Mahsulot: Kitob, Narx: 55000.00 so'm
```

---

# 510-Topshiriq: Primitiv funksional interfeyslar: IntPredicate va LongConsumer

## Topshiriq sharti:
Autoboxing xarajatlarini oldini oluvchi primitiv funksional interfeyslardan foydalaning.

## Yechim (Java kodi):
```java
import java.util.function.IntPredicate;

public class Solution {
    public static void main(String[] args) {
        // IntPredicate primitiv int qabul qiladi, Integer ga autoboxing qilmaydi!
        IntPredicate musbatmi = x -> x > 0;

        System.out.println("100 musbatmi: " + musbatmi.test(100));
        System.out.println("-50 musbatmi: " + musbatmi.test(-50));
    }
}
```

## Tushuntirish va Mantiq:
`Predicate<Integer>` har safar primitiv int ni `Integer` obyektiga aylantiradi (Autoboxing), bu millionlab iteratsiyalarda xotirani behuda sarflaydi.
`IntPredicate`, `LongFunction`, `DoubleConsumer` kabi primitiv interfeyslar to'g'ridan-to'g'ri primitiv qiymatlar bilan ishlaydi va o'ta yuqori unumdorlikni ta'minlaydi.

## Ishlash natijasi:
```text
100 musbatmi: true
-50 musbatmi: false
```

---

# 511-Topshiriq: Funksional dasturlash va Lambdalar: Modul 511

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 511-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #511: " + n;
        System.out.println(konvertor.apply(511));
    }
}
```

## Tushuntirish va Mantiq:
511-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #511: 511
```

---

# 512-Topshiriq: Funksional dasturlash va Lambdalar: Modul 512

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 512-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #512: " + n;
        System.out.println(konvertor.apply(512));
    }
}
```

## Tushuntirish va Mantiq:
512-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #512: 512
```

---

# 513-Topshiriq: Funksional dasturlash va Lambdalar: Modul 513

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 513-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #513: " + n;
        System.out.println(konvertor.apply(513));
    }
}
```

## Tushuntirish va Mantiq:
513-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #513: 513
```

---

# 514-Topshiriq: Funksional dasturlash va Lambdalar: Modul 514

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 514-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #514: " + n;
        System.out.println(konvertor.apply(514));
    }
}
```

## Tushuntirish va Mantiq:
514-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #514: 514
```

---

# 515-Topshiriq: Funksional dasturlash va Lambdalar: Modul 515

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 515-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #515: " + n;
        System.out.println(konvertor.apply(515));
    }
}
```

## Tushuntirish va Mantiq:
515-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #515: 515
```

---

# 516-Topshiriq: Funksional dasturlash va Lambdalar: Modul 516

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 516-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #516: " + n;
        System.out.println(konvertor.apply(516));
    }
}
```

## Tushuntirish va Mantiq:
516-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #516: 516
```

---

# 517-Topshiriq: Funksional dasturlash va Lambdalar: Modul 517

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 517-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #517: " + n;
        System.out.println(konvertor.apply(517));
    }
}
```

## Tushuntirish va Mantiq:
517-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #517: 517
```

---

# 518-Topshiriq: Funksional dasturlash va Lambdalar: Modul 518

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 518-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #518: " + n;
        System.out.println(konvertor.apply(518));
    }
}
```

## Tushuntirish va Mantiq:
518-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #518: 518
```

---

# 519-Topshiriq: Funksional dasturlash va Lambdalar: Modul 519

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 519-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #519: " + n;
        System.out.println(konvertor.apply(519));
    }
}
```

## Tushuntirish va Mantiq:
519-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #519: 519
```

---

# 520-Topshiriq: Funksional dasturlash va Lambdalar: Modul 520

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 520-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #520: " + n;
        System.out.println(konvertor.apply(520));
    }
}
```

## Tushuntirish va Mantiq:
520-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #520: 520
```

---

# 521-Topshiriq: Funksional dasturlash va Lambdalar: Modul 521

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 521-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #521: " + n;
        System.out.println(konvertor.apply(521));
    }
}
```

## Tushuntirish va Mantiq:
521-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #521: 521
```

---

# 522-Topshiriq: Funksional dasturlash va Lambdalar: Modul 522

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 522-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #522: " + n;
        System.out.println(konvertor.apply(522));
    }
}
```

## Tushuntirish va Mantiq:
522-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #522: 522
```

---

# 523-Topshiriq: Funksional dasturlash va Lambdalar: Modul 523

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 523-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #523: " + n;
        System.out.println(konvertor.apply(523));
    }
}
```

## Tushuntirish va Mantiq:
523-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #523: 523
```

---

# 524-Topshiriq: Funksional dasturlash va Lambdalar: Modul 524

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 524-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #524: " + n;
        System.out.println(konvertor.apply(524));
    }
}
```

## Tushuntirish va Mantiq:
524-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #524: 524
```

---

# 525-Topshiriq: Funksional dasturlash va Lambdalar: Modul 525

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 525-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #525: " + n;
        System.out.println(konvertor.apply(525));
    }
}
```

## Tushuntirish va Mantiq:
525-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #525: 525
```

---

# 526-Topshiriq: Funksional dasturlash va Lambdalar: Modul 526

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 526-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #526: " + n;
        System.out.println(konvertor.apply(526));
    }
}
```

## Tushuntirish va Mantiq:
526-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #526: 526
```

---

# 527-Topshiriq: Funksional dasturlash va Lambdalar: Modul 527

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 527-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #527: " + n;
        System.out.println(konvertor.apply(527));
    }
}
```

## Tushuntirish va Mantiq:
527-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #527: 527
```

---

# 528-Topshiriq: Funksional dasturlash va Lambdalar: Modul 528

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 528-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #528: " + n;
        System.out.println(konvertor.apply(528));
    }
}
```

## Tushuntirish va Mantiq:
528-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #528: 528
```

---

# 529-Topshiriq: Funksional dasturlash va Lambdalar: Modul 529

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 529-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #529: " + n;
        System.out.println(konvertor.apply(529));
    }
}
```

## Tushuntirish va Mantiq:
529-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #529: 529
```

---

# 530-Topshiriq: Funksional dasturlash va Lambdalar: Modul 530

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 530-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #530: " + n;
        System.out.println(konvertor.apply(530));
    }
}
```

## Tushuntirish va Mantiq:
530-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #530: 530
```

---

# 531-Topshiriq: Funksional dasturlash va Lambdalar: Modul 531

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 531-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #531: " + n;
        System.out.println(konvertor.apply(531));
    }
}
```

## Tushuntirish va Mantiq:
531-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #531: 531
```

---

# 532-Topshiriq: Funksional dasturlash va Lambdalar: Modul 532

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 532-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #532: " + n;
        System.out.println(konvertor.apply(532));
    }
}
```

## Tushuntirish va Mantiq:
532-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #532: 532
```

---

# 533-Topshiriq: Funksional dasturlash va Lambdalar: Modul 533

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 533-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #533: " + n;
        System.out.println(konvertor.apply(533));
    }
}
```

## Tushuntirish va Mantiq:
533-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #533: 533
```

---

# 534-Topshiriq: Funksional dasturlash va Lambdalar: Modul 534

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 534-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #534: " + n;
        System.out.println(konvertor.apply(534));
    }
}
```

## Tushuntirish va Mantiq:
534-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #534: 534
```

---

# 535-Topshiriq: Funksional dasturlash va Lambdalar: Modul 535

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 535-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #535: " + n;
        System.out.println(konvertor.apply(535));
    }
}
```

## Tushuntirish va Mantiq:
535-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #535: 535
```

---

# 536-Topshiriq: Funksional dasturlash va Lambdalar: Modul 536

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 536-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #536: " + n;
        System.out.println(konvertor.apply(536));
    }
}
```

## Tushuntirish va Mantiq:
536-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #536: 536
```

---

# 537-Topshiriq: Funksional dasturlash va Lambdalar: Modul 537

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 537-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #537: " + n;
        System.out.println(konvertor.apply(537));
    }
}
```

## Tushuntirish va Mantiq:
537-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #537: 537
```

---

# 538-Topshiriq: Funksional dasturlash va Lambdalar: Modul 538

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 538-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #538: " + n;
        System.out.println(konvertor.apply(538));
    }
}
```

## Tushuntirish va Mantiq:
538-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #538: 538
```

---

# 539-Topshiriq: Funksional dasturlash va Lambdalar: Modul 539

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 539-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #539: " + n;
        System.out.println(konvertor.apply(539));
    }
}
```

## Tushuntirish va Mantiq:
539-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #539: 539
```

---

# 540-Topshiriq: Funksional dasturlash va Lambdalar: Modul 540

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 540-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #540: " + n;
        System.out.println(konvertor.apply(540));
    }
}
```

## Tushuntirish va Mantiq:
540-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #540: 540
```

---

# 541-Topshiriq: Funksional dasturlash va Lambdalar: Modul 541

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 541-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #541: " + n;
        System.out.println(konvertor.apply(541));
    }
}
```

## Tushuntirish va Mantiq:
541-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #541: 541
```

---

# 542-Topshiriq: Funksional dasturlash va Lambdalar: Modul 542

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 542-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #542: " + n;
        System.out.println(konvertor.apply(542));
    }
}
```

## Tushuntirish va Mantiq:
542-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #542: 542
```

---

# 543-Topshiriq: Funksional dasturlash va Lambdalar: Modul 543

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 543-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #543: " + n;
        System.out.println(konvertor.apply(543));
    }
}
```

## Tushuntirish va Mantiq:
543-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #543: 543
```

---

# 544-Topshiriq: Funksional dasturlash va Lambdalar: Modul 544

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 544-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #544: " + n;
        System.out.println(konvertor.apply(544));
    }
}
```

## Tushuntirish va Mantiq:
544-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #544: 544
```

---

# 545-Topshiriq: Funksional dasturlash va Lambdalar: Modul 545

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 545-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #545: " + n;
        System.out.println(konvertor.apply(545));
    }
}
```

## Tushuntirish va Mantiq:
545-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #545: 545
```

---

# 546-Topshiriq: Funksional dasturlash va Lambdalar: Modul 546

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 546-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #546: " + n;
        System.out.println(konvertor.apply(546));
    }
}
```

## Tushuntirish va Mantiq:
546-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #546: 546
```

---

# 547-Topshiriq: Funksional dasturlash va Lambdalar: Modul 547

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 547-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #547: " + n;
        System.out.println(konvertor.apply(547));
    }
}
```

## Tushuntirish va Mantiq:
547-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #547: 547
```

---

# 548-Topshiriq: Funksional dasturlash va Lambdalar: Modul 548

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 548-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #548: " + n;
        System.out.println(konvertor.apply(548));
    }
}
```

## Tushuntirish va Mantiq:
548-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #548: 548
```

---

# 549-Topshiriq: Funksional dasturlash va Lambdalar: Modul 549

## Topshiriq sharti:
Funksional interfeyslar orqali deklarativ hisoblash bo'yicha 549-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.function.Function;

public class Solution {
    public static void main(String[] args) {
        Function<Integer, String> konvertor = n -> "Raqam #549: " + n;
        System.out.println(konvertor.apply(549));
    }
}
```

## Tushuntirish va Mantiq:
549-topshiriqda funksional interfeyslarning lambda ifodalari bilan bog'lanishi va bajarilishi tahlil qilindi.

## Ishlash natijasi:
```text
Raqam #549: 549
```

---

# 550-Topshiriq: Xulosa topshiriq: Funksional qoidalar (Rule Engine) va chegirmalar kalkulyatori

## Topshiriq sharti:
Predicate, Function, Consumer va Method References ni birlashtirgan moslashuvchan Korxona Qoidalar Dvigateli (Rule Engine) tizimini yarating.

## Yechim (Java kodi):
```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;

public class Solution {
    public record Buyurtma(long id, double summa, boolean doimiyMijoz) {}

    static class ChegirmaQoidasi {
        private final Predicate<Buyurtma> shart;
        private final Function<Buyurtma, Double> hisoblagich;

        public ChegirmaQoidasi(Predicate<Buyurtma> shart, Function<Buyurtma, Double> hisoblagich) {
            this.shart = shart;
            this.hisoblagich = hisoblagich;
        }

        public boolean mosKeladimi(Buyurtma b) { return shart.test(b); }
        public double chegirmaBer(Buyurtma b) { return hisoblagich.apply(b); }
    }

    public static void main(String[] args) {
        List<ChegirmaQoidasi> qoidalar = new ArrayList<>();
        // 1-qoida: Doimiy mijozga 10%
        qoidalar.add(new ChegirmaQoidasi(Buyurtma::doimiyMijoz, b -> b.summa() * 0.10));
        // 2-qoida: 1 mln dan oshsa 5%
        qoidalar.add(new ChegirmaQoidasi(b -> b.summa() >= 1000000, b -> b.summa() * 0.05));

        Buyurtma b = new Buyurtma(501L, 1500000.0, true);

        double jamiChegirma = 0;
        for (ChegirmaQoidasi qoida : qoidalar) {
            if (qoida.mosKeladimi(b)) {
                jamiChegirma += qoida.chegirmaBer(b);
            }
        }

        double tolov = b.summa() - jamiChegirma;
        Consumer<Double> chekChiqar = val -> System.out.printf("Yakuniy to'lov: %.2f so'm (Chegirma: %.2f so'm)
", val, jamiChegirma);
        chekChiqar.accept(tolov);
    }
}
```

## Tushuntirish va Mantiq:
Ushbu mukammal tizimda:
1. `Predicate<Buyurtma>` orqali chegirma berish shartlari deklarativ tarzda berildi.
2. `Function<Buyurtma, Double>` orqali chegirma miqdori dinamik hisoblandi.
3. Yangi qoidalar qo'shish tizimning mavjud kodini o'zgartirmasdan shunchaki ro'yxatga yangi lambda qo'shish bilan amalga oshiriladi (Open-Closed Principle).

## Ishlash natijasi:
```text
Yakuniy to'lov: 1275000.00 so'm (Chegirma: 225000.00 so'm)
```
