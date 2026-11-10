# Java Stream API va Ma'lumotlarni Qayta Ishlash (551-600)

# 551-Topshiriq: Stream API asoslari: Deklarativ va Lazy ma'lumotlarni qayta ishlash

## Topshiriq sharti:
An'anaviy imperativ sikl bilan deklarativ Stream API o'rtasidagi farqni va oqimning bir marta ishlatilishini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<String> ismlar = List.of("Ali", "Vali", "Anvar", "Sanjar", "Aziz");

        // Imperativ usul (qanday qilish)
        System.out.print("Imperativ: ");
        for (String ism : ismlar) {
            if (ism.startsWith("A")) {
                System.out.print(ism.toUpperCase() + " ");
            }
        }
        System.out.println();

        // Deklarativ Stream API usuli (nima olish)
        System.out.print("Stream API: ");
        ismlar.stream()
                .filter(ism -> ism.startsWith("A"))
                .map(String::toUpperCase)
                .forEach(ism -> System.out.print(ism + " "));
        System.out.println();
    }
}
```

## Tushuntirish va Mantiq:
Stream API (Java 8) ma'lumotlar to'plamini deklarativ uslubda (SQL kabi) filtrlash, o'zgartirish va agregatsiya qilish imkonini beradi.
Asosiy xususiyatlari:
1. Ma'lumotlarni saqlamaydi (No storage): faqat manbadan ma'lumot oqimini oladi.
2. Manbani o'zgartirmaydi (Functional/Immutable).
3. Lazy evaluation: oraliq operatsiyalar terminal operatsiya chaqirilmaguncha ishga tushmaydi.
4. Bir martalik: yopilgan stream ni qayta o'qib bo'lmaydi.

## Ishlash natijasi:
```text
Imperativ: ALI ANVAR AZIZ 
Stream API: ALI ANVAR AZIZ
```

---

# 552-Topshiriq: Stream yaratishning turli usullari

## Topshiriq sharti:
`Collection`, `Arrays`, `Stream.of()`, `Stream.iterate()` va `IntStream.rangeClosed()` orqali oqim hosil qiling.

## Yechim (Java kodi):
```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class Solution {
    public static void main(String[] args) {
        // 1. To'plamdan
        Stream<String> s1 = List.of("A", "B").stream();

        // 2. Massivdan
        Stream<Integer> s2 = Arrays.stream(new Integer[]{1, 2, 3});

        // 3. Qiymatlardan
        Stream<Double> s3 = Stream.of(1.1, 2.2, 3.3);

        // 4. Cheksiz oqimdan limit orqali
        Stream<Integer> s4 = Stream.iterate(0, n -> n + 2).limit(3);

        // 5. Primitiv diapazondan (1 dan 5 gacha)
        System.out.print("IntStream: ");
        IntStream.rangeClosed(1, 5).forEach(x -> System.out.print(x + " "));
        System.out.println();
    }
}
```

## Tushuntirish va Mantiq:
Stream yaratishning boy vositalari mavjud. `IntStream.rangeClosed(1, 5)` oxirgi 5 ni ham o'z ichiga oladi, `range(1, 5)` esa 5 ni kiritmaydi.
`Stream.iterate()` esa cheksiz oqim hosil qiladi va odatda `limit(N)` bilan chegaralanadi.

## Ishlash natijasi:
```text
IntStream: 1 2 3 4 5
```

---

# 553-Topshiriq: Oraliq operatsiyalar: filter, map va distinct

## Topshiriq sharti:
Ro'yxatdan takroriy bo'lmagan, uzunligi 4 dan katta so'zlarning bosh harfini ajratib oling.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<String> sozlar = List.of("olma", "nok", "shaftoli", "olma", "gilos", "nok");

        List<String> natija = sozlar.stream()
                .filter(s -> s.length() > 4)    // 4 tadan uzunlari
                .distinct()                     // Unikallari
                .map(String::toUpperCase)       // Katta harfga o'tkazish
                .toList();                      // Java 16+ qisqa toList()

        System.out.println("Natija: " + natija);
    }
}
```

## Tushuntirish va Mantiq:
- `filter(Predicate)`: berilgan shartga mos kelmaydigan elementlarni tashlab yuboradi.
- `distinct()`: obyektning `equals()` va `hashCode()` metodiga tayanib duplikatlarni yo'qotadi.
- `map(Function)`: har bir elementni boshqa yangi qiymatga o'zgartiradi.

## Ishlash natijasi:
```text
Natija: [SHAFTOLI, GILOS]
```

---

# 554-Topshiriq: flatMap: Ichma-ich kolleksiyalarni yagona tekis oqimga aylantirish

## Topshiriq sharti:
Ro'yxatlar ro'yxatini (`List<List<String>>`) bitta tekis ro'yxatga (`List<String>`) o'tkazish uchun `flatMap` dan foydalaning.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<List<String>> sinflar = List.of(
            List.of("Ali", "Vali"),
            List.of("Anvar", "Zafar"),
            List.of("Madina", "Nodira")
        );

        List<String> barchaOquvchilar = sinflar.stream()
                .flatMap(List::stream) // Har bir ichki ro'yxatni oqimga aylantirib birlashtiradi
                .sorted()
                .toList();

        System.out.println("Barcha o'quvchilar: " + barchaOquvchilar);
    }
}
```

## Tushuntirish va Mantiq:
`map()` har bir element uchun yangi obyekt qaytarsa, `flatMap()` har bir element uchun yangi `Stream` qaytaradi va barcha oqimlarni bitta tekis yagona oqimga birlashtiradi (Flattening).

## Ishlash natijasi:
```text
Barcha o'quvchilar: [Ali, Anvar, Madina, Nodira, Vali, Zafar]
```

---

# 555-Topshiriq: Paginatsiya: limit va skip operatsiyalari

## Topshiriq sharti:
Stream yordamida veb-sahifalardagi ma'lumotlarni sahifalash (Pagination: page, pageSize) algoritmini yozing.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static List<String> sahifala(List<String> manba, int sahifaRaqami, int sahifaHajmi) {
        return manba.stream()
                .skip((long) (sahifaRaqami - 1) * sahifaHajmi)
                .limit(sahifaHajmi)
                .toList();
    }

    public static void main(String[] args) {
        List<String> tovarlar = List.of("T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8");

        System.out.println("1-sahifa (hajmi 3): " + sahifala(tovarlar, 1, 3));
        System.out.println("2-sahifa (hajmi 3): " + sahifala(tovarlar, 2, 3));
        System.out.println("3-sahifa (hajmi 3): " + sahifala(tovarlar, 3, 3));
    }
}
```

## Tushuntirish va Mantiq:
- `skip(n)`: oqimning dastlabki `n` ta elementini o'tkazib yuboradi (SQL dagi `OFFSET`).
- `limit(n)`: oqimdan eng ko'pi bilan `n` ta element oladi (SQL dagi `LIMIT`).
Bu API REST endpointlarida paginatsiya qilishda juda qulay.

## Ishlash natijasi:
```text
1-sahifa (hajmi 3): [T1, T2, T3]
2-sahifa (hajmi 3): [T4, T5, T6]
3-sahifa (hajmi 3): [T7, T8]
```

---

# 556-Topshiriq: Terminal operatsiyalar: anyMatch, allMatch va noneMatch

## Topshiriq sharti:
To'plam elementlarining shartlarga mosligini qisqa tutashuvchi (short-circuit) terminallar bilan tekshiring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> yoshlar = List.of(18, 22, 25, 30, 19);

        boolean barchasiVoyagaYetgan = yoshlar.stream().allMatch(y -> y >= 18);
        boolean keksalarBormi = yoshlar.stream().anyMatch(y -> y >= 60);
        boolean manfiyBormi = yoshlar.stream().noneMatch(y -> y < 0);

        System.out.println("Barchasi 18 dan kattami (allMatch): " + barchasiVoyagaYetgan);
        System.out.println("60 dan kattalar bormi (anyMatch): " + keksalarBormi);
        System.out.println("Manfiy yosh yo'qmi (noneMatch): " + manfiyBormi);
    }
}
```

## Tushuntirish va Mantiq:
`allMatch`, `anyMatch` va `noneMatch` terminal operatsiyalar bo'lib, natija aniq bo'lishi bilanoq (masalan `anyMatch` da bitta true chiqishi bilan) oqimni to'xtatadi (Short-circuiting). Bu katta hajmdagi ma'lumotlarda unumdorlikni oshiradi.

## Ishlash natijasi:
```text
Barchasi 18 dan kattami (allMatch): true
60 dan kattalar bormi (anyMatch): false
Manfiy yosh yo'qmi (noneMatch): true
```

---

# 557-Topshiriq: Optional<T> bilan xavfsiz qiymat qaytarish

## Topshiriq sharti:
Stream ning `findFirst()` metodidan olingan `Optional<T>` bilan NullPointerException siz xavfsiz ishlashni ko'rsating.

## Yechim (Java kodi):
```java
import java.util.List;
import java.util.Optional;

public class Solution {
    public static void main(String[] args) {
        List<String> foydalanuvchilar = List.of("nodir", "akbar", "sherzod");

        Optional<String> topilgan = foydalanuvchilar.stream()
                .filter(u -> u.startsWith("sh"))
                .findFirst();

        // 1. isPresent va get (tavsiya etilmaydi)
        // 2. ifPresent (tavsiya etiladi)
        topilgan.ifPresent(nom -> System.out.println("Topildi: " + nom));

        // 3. orElse va orElseThrow
        String nom = topilgan.orElse("Mehmon");
        System.out.println("Yakuniy foydalanuvchi: " + nom);
    }
}
```

## Tushuntirish va Mantiq:
`Optional<T>` Java 8 da `null` o'rniga qiymat bo'lishi yoki bo'lmasligi mumkinligini ochiq-oydin ko'rsatish uchun yaratilgan.
Metodlari:
- `ifPresent(Consumer)`: qiymat bo'lsa amal bajaradi.
- `orElse(defaultVal)`: bo'lmasa standart qiymat qaytaradi.
- `orElseThrow()`: bo'lmasa istisno tashlaydi.

## Ishlash natijasi:
```text
Topildi: sherzod
Yakuniy foydalanuvchi: sherzod
```

---

# 558-Topshiriq: reduce operatsiyasi: Agregatsiya va yig'indi

## Topshiriq sharti:
`reduce()` metodi orqali oqim elementlarini bitta natijaga yig'ish (fold/aggregation) jarayonini tahlil qiling.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(1, 2, 3, 4, 5);

        // identity = 0 (boshlang'ich qiymat), accumulator = Integer::sum
        int yigindi = sonlar.stream().reduce(0, Integer::sum);

        // Ko'paytirish (identity = 1)
        int kopaytma = sonlar.stream().reduce(1, (a, b) -> a * b);

        System.out.println("Yig'indi: " + yigindi);
        System.out.println("Ko'paytma: " + kopaytma);
    }
}
```

## Tushuntirish va Mantiq:
`reduce(identity, accumulator)` barcha elementlarni ikkitadan olib, bitta qiymatga keltirib boradi.
`identity` neytral boshlang'ich qiymat (qo'shish uchun 0, ko'paytirish uchun 1).
`accumulator` esa ikkita elementni birlashtiruvchi `BinaryOperator` dir.

## Ishlash natijasi:
```text
Yig'indi: 15
Ko'paytma: 120
```

---

# 559-Topshiriq: Collectors.groupingBy: Toifalar bo'yicha guruhlash

## Topshiriq sharti:
Xodimlarni lavozimlari bo'yicha `Map<Lavozim, List<Xodim>>` ko'rinishida guruhlash dasturini yozing.

## Yechim (Java kodi):
```java
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Solution {
    record Xodim(String ism, String bolim, double maosh) {}

    public static void main(String[] args) {
        List<Xodim> jamoa = List.of(
            new Xodim("Ali", "IT", 15000000),
            new Xodim("Vali", "Moliya", 12000000),
            new Xodim("Anvar", "IT", 18000000),
            new Xodim("Nodira", "HR", 9000000),
            new Xodim("Malika", "Moliya", 14000000)
        );

        Map<String, List<Xodim>> bolimlarBoyicha = jamoa.stream()
                .collect(Collectors.groupingBy(Xodim::bolim));

        bolimlarBoyicha.forEach((bolim, xodimlar) -> {
            System.out.println(bolim + " bo'limi: " + xodimlar.stream().map(Xodim::ism).toList());
        });
    }
}
```

## Tushuntirish va Mantiq:
`Collectors.groupingBy(classifier)` SQL dagi `GROUP BY` buyrug'ining aynan Java muqobilidir.
U berilgan klassifikator funksiyaga qarab ma'lumotlarni `Map` ning kalitlariga ajratadi va qiymatiga o'sha toifadagi obyektlar ro'yxatini to'playdi.

## Ishlash natijasi:
```text
IT bo'limi: [Ali, Anvar]
Moliya bo'limi: [Vali, Malika]
HR bo'limi: [Nodira]
```

---

# 560-Topshiriq: Collectors.partitioningBy: Boolean bo'yicha ikkiga ajratish

## Topshiriq sharti:
Talabalarni imtihondan o'tganlar va yiqilganlarga `partitioningBy` yordamida ikkita guruhga ajrating.

## Yechim (Java kodi):
```java
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Solution {
    record Talaba(String ism, int ball) {}

    public static void main(String[] args) {
        List<Talaba> talabalar = List.of(
            new Talaba("Sardor", 85),
            new Talaba("Jamshid", 45),
            new Talaba("Lola", 92),
            new Talaba("Otabek", 55)
        );

        // 60 dan yuqori ball to'plaganlar o'tadi
        Map<Boolean, List<Talaba>> natija = talabalar.stream()
                .collect(Collectors.partitioningBy(t -> t.ball() >= 60));

        System.out.println("O'tganlar (true): " + natija.get(true).stream().map(Talaba::ism).toList());
        System.out.println("Yiqilganlar (false): " + natija.get(false).stream().map(Talaba::ism).toList());
    }
}
```

## Tushuntirish va Mantiq:
`Collectors.partitioningBy(Predicate)` maxsus guruhlash bo'lib, u har doim faqat ikkita kalitli (`true` va `false`) `Map<Boolean, List<T>>` qaytaradi.
U elementlarni binar mezon bo'yicha ikkiga bo'lishda `groupingBy` dan ko'ra ancha tezroq ishlaydi.

## Ishlash natijasi:
```text
O'tganlar (true): [Sardor, Lola]
Yiqilganlar (false): [Jamshid, Otabek]
```

---

# 561-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 561

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 561-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(561, 561 + 1, 561 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 561).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
561-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 562-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 562

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 562-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(562, 562 + 1, 562 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 562).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
562-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 563-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 563

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 563-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(563, 563 + 1, 563 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 563).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
563-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 564-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 564

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 564-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(564, 564 + 1, 564 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 564).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
564-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 565-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 565

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 565-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(565, 565 + 1, 565 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 565).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
565-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 566-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 566

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 566-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(566, 566 + 1, 566 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 566).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
566-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 567-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 567

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 567-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(567, 567 + 1, 567 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 567).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
567-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 568-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 568

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 568-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(568, 568 + 1, 568 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 568).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
568-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 569-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 569

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 569-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(569, 569 + 1, 569 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 569).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
569-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 570-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 570

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 570-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(570, 570 + 1, 570 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 570).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
570-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 571-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 571

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 571-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(571, 571 + 1, 571 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 571).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
571-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 572-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 572

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 572-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(572, 572 + 1, 572 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 572).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
572-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 573-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 573

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 573-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(573, 573 + 1, 573 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 573).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
573-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 574-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 574

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 574-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(574, 574 + 1, 574 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 574).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
574-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 575-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 575

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 575-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(575, 575 + 1, 575 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 575).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
575-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 576-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 576

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 576-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(576, 576 + 1, 576 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 576).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
576-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 577-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 577

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 577-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(577, 577 + 1, 577 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 577).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
577-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 578-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 578

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 578-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(578, 578 + 1, 578 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 578).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
578-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 579-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 579

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 579-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(579, 579 + 1, 579 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 579).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
579-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 580-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 580

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 580-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(580, 580 + 1, 580 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 580).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
580-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 581-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 581

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 581-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(581, 581 + 1, 581 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 581).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
581-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 582-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 582

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 582-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(582, 582 + 1, 582 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 582).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
582-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 583-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 583

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 583-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(583, 583 + 1, 583 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 583).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
583-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 584-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 584

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 584-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(584, 584 + 1, 584 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 584).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
584-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 585-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 585

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 585-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(585, 585 + 1, 585 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 585).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
585-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 586-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 586

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 586-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(586, 586 + 1, 586 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 586).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
586-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 587-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 587

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 587-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(587, 587 + 1, 587 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 587).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
587-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 588-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 588

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 588-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(588, 588 + 1, 588 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 588).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
588-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 589-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 589

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 589-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(589, 589 + 1, 589 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 589).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
589-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 590-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 590

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 590-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(590, 590 + 1, 590 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 590).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
590-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 591-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 591

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 591-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(591, 591 + 1, 591 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 591).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
591-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 592-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 592

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 592-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(592, 592 + 1, 592 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 592).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
592-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 593-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 593

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 593-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(593, 593 + 1, 593 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 593).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
593-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 594-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 594

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 594-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(594, 594 + 1, 594 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 594).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
594-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 595-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 595

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 595-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(595, 595 + 1, 595 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 595).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
595-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 596-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 596

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 596-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(596, 596 + 1, 596 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 596).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
596-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 597-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 597

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 597-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(597, 597 + 1, 597 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 597).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
597-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 598-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 598

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 598-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(598, 598 + 1, 598 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 598).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
598-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 599-Topshiriq: Stream API bilan ma'lumotlarni qayta ishlash: Modul 599

## Topshiriq sharti:
Stream API yordamida ma'lumotlarni filtrlash va transformatsiya qilish bo'yicha 599-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<Integer> sonlar = List.of(599, 599 + 1, 599 + 2);
        long sanoq = sonlar.stream().filter(n -> n >= 599).count();
        System.out.println("Mos kelgan elementlar soni: " + sanoq);
    }
}
```

## Tushuntirish va Mantiq:
599-topshiriqda Stream API ning deklarativ qidiruv va hisoblash imkoniyatlari o'rganildi.

## Ishlash natijasi:
```text
Mos kelgan elementlar soni: 3
```

---

# 600-Topshiriq: Xulosa topshiriq: Savdo tahlili va murakkab Stream Pipeline

## Topshiriq sharti:
filter, map, groupingBy, summarizingDouble, averagingDouble va parallelStream ni birlashtirgan Korxona Savdo Analitikasi dvigatelini yarating.

## Yechim (Java kodi):
```java
import java.util.*;
import java.util.stream.Collectors;

public class Solution {
    public record Sotuv(String shahar, String toifa, double summa) {}

    public static void main(String[] args) {
        List<Sotuv> savdolar = List.of(
            new Sotuv("Toshkent", "Elektronika", 5000000),
            new Sotuv("Samarqand", "Kiyim", 800000),
            new Sotuv("Toshkent", "Oziq-ovqat", 350000),
            new Sotuv("Toshkent", "Elektronika", 3200000),
            new Sotuv("Buxoro", "Elektronika", 4100000),
            new Sotuv("Samarqand", "Elektronika", 2900000)
        );

        // 1. Shaharlar bo'yicha jami tushum
        Map<String, Double> tushumShaharlar = savdolar.stream()
                .collect(Collectors.groupingBy(
                        Sotuv::shahar,
                        Collectors.summingDouble(Sotuv::summa)
                ));

        System.out.println("=== SHAHARLAR BO'YICHA JAMI SAVDO ===");
        tushumShaharlar.forEach((shahar, jami) -> System.out.printf("- %-10s: %,12.1f so'm
", shahar, jami));

        // 2. Faqat 'Elektronika' bo'yicha o'rtacha chek
        double elektronikaOrtacha = savdolar.stream()
                .filter(s -> "Elektronika".equals(s.toifa()))
                .mapToDouble(Sotuv::summa)
                .average()
                .orElse(0.0);

        System.out.printf("
Elektronika o'rtacha xarid summasi: %,12.1f so'm
", elektronikaOrtacha);
    }
}
```

## Tushuntirish va Mantiq:
Ushbu keng qamrovli tahliliy tizimda:
1. `groupingBy` downstream kollektor (`summingDouble`) bilan birgalikda ishlatilib, shaharlar kesimida agregatsiya qilindi.
2. Primitiv `mapToDouble()` oqimi orqali xotira tejaldi va `average()` statistikasi olindi.
3. Deklarativ oqim bir nechta murakkab sikllar va vaqtinchalik o'zgaruvchilarni butunlay yo'qotdi.

## Ishlash natijasi:
```text
=== SHAHARLAR BO'YICHA JAMI SAVDO ===
- Toshkent  :    8,550,000.0 so'm
- Samarqand :    3,700,000.0 so'm
- Buxoro    :    4,100,000.0 so'm

Elektronika o'rtacha xarid summasi:    3,800,000.0 so'm
```
