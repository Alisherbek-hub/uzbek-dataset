# Java Interfeyslar va Abstraktsiya (301-350)

# 301-Topshiriq: Interfeys (Interface) asoslari va implements kalit so'zi

## Topshiriq sharti:
`ChopEtiladigan` interfeysini e'lon qilib, uni `Hujjat` sinfida amalga oshiring.

## Yechim (Java kodi):
```java
public class Solution {
    interface ChopEtiladigan {
        void chopEt();
    }

    static class Hujjat implements ChopEtiladigan {
        private final String matn;
        public Hujjat(String matn) { this.matn = matn; }

        @Override
        public void chopEt() {
            System.out.println("Hujjat chop etilmoqda: " + matn);
        }
    }

    public static void main(String[] args) {
        ChopEtiladigan printer = new Hujjat("Shartnoma #2026-X");
        printer.chopEt();
    }
}
```

## Tushuntirish va Mantiq:
Interfeys (Interface) — bu sinflar amal qilishi shart bo'lgan rasmiy shartnoma (contract) dir.
U nima qilinishi kerakligini belgilaydi, qanday qilinishini esa sinf hal qiladi.
Interfeysdagi barcha metodlar sukut bo'yicha `public abstract` hisoblanadi.

## Ishlash natijasi:
```text
Hujjat chop etilmoqda: Shartnoma #2026-X
```

---

# 302-Topshiriq: Interfeysdagi o'zgarmaslar (public static final)

## Topshiriq sharti:
Interfeys ichidagi maydonlarning avtomatik `public static final` bo'lishini ko'rsatuvchi dastur yozing.

## Yechim (Java kodi):
```java
public class Solution {
    interface TizimKonstantalari {
        int MAKSIMAL_ULANISHLAR = 100; // public static final avtomatik
        String STANDART_KODLASH = "UTF-8";
    }

    public static void main(String[] args) {
        System.out.println("Ulanishlar limiti: " + TizimKonstantalari.MAKSIMAL_ULANISHLAR);
        System.out.println("Kodlash turi: " + TizimKonstantalari.STANDART_KODLASH);
    }
}
```

## Tushuntirish va Mantiq:
Interfeyslarda instansiya maydonlari bo'lishi mumkin emas. E'lon qilingan har qanday o'zgaruvchi avtomatik tarzda `public static final` konstantaga aylanadi.
Biroq faqat konstantalar saqlash uchun interfeys ochish (Constant Interface Anti-pattern) tavsiya etilmaydi; buning o'rniga `final class` yoki `enum` ishlatish kerak.

## Ishlash natijasi:
```text
Ulanishlar limiti: 100
Kodlash turi: UTF-8
```

---

# 303-Topshiriq: Ko'p interfeysli vorislik (Multiple Interface Inheritance)

## Topshiriq sharti:
Bitta sinf bir nechta interfeyslarni (`implements A, B`) amalga oshirishi mumkinligini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    interface Uchuvchi { void uch(); }
    interface SuvdaSuzuvchi { void suz(); }

    static class AmfibiyaSamolyot implements Uchuvchi, SuvdaSuzuvchi {
        @Override
        public void uch() { System.out.println("Samolyot havoga ko'tarildi."); }

        @Override
        public void suz() { System.out.println("Samolyot suv sathida suzmoqda."); }
    }

    public static void main(String[] args) {
        AmfibiyaSamolyot a = new AmfibiyaSamolyot();
        a.uch();
        a.suz();
    }
}
```

## Tushuntirish va Mantiq:
Java-da sinflar uchun ko'p ota merosxo'rligi taqiqlangan bo'lsa-da, interfeyslar orqali ko'p karra amalga oshirishga to'liq ruxsat berilgan.
Sinf istalgancha interfeysni vergul orqali ro'yxat qilib `implements` qilishi mumkin.

## Ishlash natijasi:
```text
Samolyot havoga ko'tarildi.
Samolyot suv sathida suzmoqda.
```

---

# 304-Topshiriq: Java 8 Default metodlar: Interfeys evolyutsiyasi

## Topshiriq sharti:
Mavjud sinflarni buzmagan holda interfeysga yangi metod qo'shish uchun `default` kalit so'zidan foydalaning.

## Yechim (Java kodi):
```java
public class Solution {
    interface LogYozuvchi {
        void log(String xabar);

        // Java 8 default metodi
        default void xatoLog(String xato) {
            log("[XATOLIK] " + xato);
        }
    }

    static class OddiyLog implements LogYozuvchi {
        @Override
        public void log(String xabar) {
            System.out.println(xabar);
        }
    }

    public static void main(String[] args) {
        LogYozuvchi logger = new OddiyLog();
        logger.log("Tizim normada ishlamoqda.");
        logger.xatoLog("Ulanish uzildi!");
    }
}
```

## Tushuntirish va Mantiq:
Java 8 gacha interfeysga yangi metod qo'shilsa, uni ishlatayotgan millionlab sinflar darhol buzilib kompilyatsiya bo'lmay qolardi.
`default` metodlar interfeys ichida standart tana `{ ... }` ga ega bo'lish imkonini berdi. Sinflar uni xohlasa qayta yozadi, xohlamasa standart xatti-harakatini meros oladi.

## Ishlash natijasi:
```text
Tizim normada ishlamoqda.
[XATOLIK] Ulanish uzildi!
```

---

# 305-Topshiriq: Diamond Problem (Olmos to'qnashuvi) va uni hal qilish

## Topshiriq sharti:
Ikkita interfeysda bir xil nomli `default` metod bo'lganda yuzaga keladigan to'qnashuvni hal qiling.

## Yechim (Java kodi):
```java
public class Solution {
    interface InterfeysA {
        default void salom() { System.out.println("Salom A dan"); }
    }

    interface InterfeysB {
        default void salom() { System.out.println("Salom B dan"); }
    }

    static class MeningSinfim implements InterfeysA, InterfeysB {
        @Override
        public void salom() {
            // To'qnashuvni aniq qaysi interfeys ekanligini ko'rsatib hal qilamiz
            InterfeysA.super.salom();
            System.out.println("Mening shaxsiy qo'shimcham");
        }
    }

    public static void main(String[] args) {
        MeningSinfim m = new MeningSinfim();
        m.salom();
    }
}
```

## Tushuntirish va Mantiq:
Agar sinf bir xil nomli default metodga ega ikkita interfeysni implements qilsa, kompilyator qaysi birini olishni bilmaydi.
Sinf bu metodni o'zida albatta `@Override` qilishi shart. Muayyan interfeysning metodini chaqirish uchun `InterfeysA.super.salom()` sintaksisi ishlatiladi.

## Ishlash natijasi:
```text
Salom A dan
Mening shaxsiy qo'shimcham
```

---

# 306-Topshiriq: Java 8 Statik metodlar interfeysda

## Topshiriq sharti:
Interfeys ichida mustaqil yordamchi statik metodlarni joylashtirishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    interface ValyutaOperatsiyalari {
        double USD_KURS = 12800.0;

        static double dollardanSomga(double dollar) {
            return dollar * USD_KURS;
        }
    }

    public static void main(String[] args) {
        double som = ValyutaOperatsiyalari.dollardanSomga(100);
        System.out.println("100 dollar: " + som + " so'm");
    }
}
```

## Tushuntirish va Mantiq:
Java 8 dan boshlab interfeyslar statik metodlarga ega bo'lishi mumkin.
Bu utilit funksiyalarni alohida Utils sinflar ochmasdan, aynan tegishli interfeysning o'zida saqlashga yo'l ochdi.

## Ishlash natijasi:
```text
100 dollar: 1280000.0 so'm
```

---

# 307-Topshiriq: Java 9 Private va Private Static metodlar interfeysda

## Topshiriq sharti:
Interfeysdagi bir nechta `default` metodlar o'rtasida umumiy kodni bo'lishish uchun `private` metodlardan foydalaning.

## Yechim (Java kodi):
```java
public class Solution {
    interface XavfsizKanal {
        default void xabarYubor(String xabar) {
            tekshir(xabar);
            System.out.println("Oddiy xabar: " + xabar);
        }

        default void shoshilinchXabar(String xabar) {
            tekshir(xabar);
            System.out.println("SHOSHILINCH: " + xabar);
        }

        // Java 9 private metodi: faqat interfeys ichida ko'rinadi
        private void tekshir(String m) {
            if (m == null || m.isBlank()) {
                throw new IllegalArgumentException("Bo'sh xabar yuborib bo'lmaydi!");
            }
        }
    }

    static class Kanal implements XavfsizKanal {}

    public static void main(String[] args) {
        Kanal k = new Kanal();
        k.xabarYubor("Assalomu alaykum");
        k.shoshilinchXabar("Server yuklamasi 95%!");
    }
}
```

## Tushuntirish va Mantiq:
Java 9 da interfeyslarga `private` va `private static` metodlar qo'shildi.
Ular interfeys tashqarisiga yoki uni amalga oshiruvchi sinflarga ko'rinmaydi, faqat interfeys ichidagi default metodlar uchun yordamchi kod takrorlanishini oldini olishga xizmat qiladi.

## Ishlash natijasi:
```text
Oddiy xabar: Assalomu alaykum
SHOSHILINCH: Server yuklamasi 95%!
```

---

# 308-Topshiriq: Comparable<T> interfeysi va tabiiy saralash (Natural Ordering)

## Topshiriq sharti:
`Comparable<T>` interfeysini amalga oshirib obyektlarni narxi bo'yicha tabiiy saralashni ta'minlang.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    static class Mahsulot implements Comparable<Mahsulot> {
        String nom;
        double narx;

        public Mahsulot(String nom, double narx) {
            this.nom = nom;
            this.narx = narx;
        }

        @Override
        public int compareTo(Mahsulot boshqa) {
            return Double.compare(this.narx, boshqa.narx);
        }

        @Override
        public String toString() { return nom + " (" + narx + ")"; }
    }

    public static void main(String[] args) {
        Mahsulot[] tovarlar = {
            new Mahsulot("Monitor", 2200000),
            new Mahsulot("Sichqoncha", 150000),
            new Mahsulot("Klaviatura", 400000)
        };

        Arrays.sort(tovarlar);
        System.out.println("Narx bo'yicha saralangan: " + Arrays.toString(tovarlar));
    }
}
```

## Tushuntirish va Mantiq:
`Comparable<T>` interfeysi sinfning "tabiiy saralash tartibi"ni (Natural Ordering) belgilaydi.
`compareTo(T o)` metodi:
- `this < o` bo'lsa manfiy (< 0)
- `this == o` bo'lsa `0`
- `this > o` bo'lsa musbat (> 0) qaytarishi shart.

## Ishlash natijasi:
```text
Narx bo'yicha saralangan: [Sichqoncha (150000.0), Klaviatura (400000.0), Monitor (2200000.0)]
```

---

# 309-Topshiriq: Comparator<T> interfeysi va moslashuvchan saralash

## Topshiriq sharti:
`Comparator<T>` yordamida obyektlarni turli mezonlar bo'yicha saralashni amalga oshiring.

## Yechim (Java kodi):
```java
import java.util.Arrays;
import java.util.Comparator;

public class Solution {
    record Talaba(String ism, double gpa) {}

    public static void main(String[] args) {
        Talaba[] talabalar = {
            new Talaba("Jasur", 3.2),
            new Talaba("Anvar", 3.9),
            new Talaba("Dilshod", 3.5)
        };

        // GPA bo'yicha kamayish tartibida saralash
        Arrays.sort(talabalar, Comparator.comparingDouble(Talaba::gpa).reversed());

        System.out.println("Reyting (GPA kamayish tartibida):");
        for (Talaba t : talabalar) {
            System.out.println(t.ism() + " -> " + t.gpa());
        }
    }
}
```

## Tushuntirish va Mantiq:
`Comparable` sinfning ichida bitta tabiiy tartibni belgilasa, `Comparator` tashqaridan turib istalgancha turli mezonlar bo'yicha (ism bo'yicha, ball bo'yicha, teskari) saralash imkonini beradi.

## Ishlash natijasi:
```text
Reyting (GPA kamayish tartibida):
Anvar -> 3.9
Dilshod -> 3.5
Jasur -> 3.2
```

---

# 310-Topshiriq: Marker (Tagging) interfeyslar

## Topshiriq sharti:
Hech qanday metodsiz faqat sinfni belgilash (markirovka) uchun xizmat qiluvchi maxsus Marker interfeys yarating.

## Yechim (Java kodi):
```java
public class Solution {
    // Marker interfeysi: tanasi bo'sh
    interface MaxfiyHujjat {}

    static class Hisobot implements MaxfiyHujjat {}
    static class OddiyQayd {}

    public static void xavfsizlikTekshiruvi(Object obj) {
        if (obj instanceof MaxfiyHujjat) {
            System.out.println("DIQQAT: Ushbu obyekt maxfiy! Alohida ruxsat talab etiladi.");
        } else {
            System.out.println("Oddiy ochiq obyekt.");
        }
    }

    public static void main(String[] args) {
        xavfsizlikTekshiruvi(new Hisobot());
        xavfsizlikTekshiruvi(new OddiyQayd());
    }
}
```

## Tushuntirish va Mantiq:
Marker interfeyslar (masalan `Serializable`, `Cloneable`, `RandomAccess`) hech qanday metodga ega bo'lmaydi.
Ularning maqsadi — JVM yoki ramkaga (framework) ushbu sinf ma'lum bir xususiyatga ega ekanligini bildirishdir. (Zamonaviy Java-da ularning o'rnini ko'p hollarda annotatsiyalar egallagan).

## Ishlash natijasi:
```text
DIQQAT: Ushbu obyekt maxfiy! Alohida ruxsat talab etiladi.
Oddiy ochiq obyekt.
```

---

# 311-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 311

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 311-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_311 {
        void ishgaTushir();
        default String versiya() { return "v311.0"; }
    }

    static class AmalgaOshiruvchi_311 implements Xizmat_311 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_311 x = new AmalgaOshiruvchi_311();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v311.0 muvaffaqiyatli ishga tushirildi.
```

---

# 312-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 312

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 312-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_312 {
        void ishgaTushir();
        default String versiya() { return "v312.0"; }
    }

    static class AmalgaOshiruvchi_312 implements Xizmat_312 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_312 x = new AmalgaOshiruvchi_312();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v312.0 muvaffaqiyatli ishga tushirildi.
```

---

# 313-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 313

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 313-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_313 {
        void ishgaTushir();
        default String versiya() { return "v313.0"; }
    }

    static class AmalgaOshiruvchi_313 implements Xizmat_313 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_313 x = new AmalgaOshiruvchi_313();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v313.0 muvaffaqiyatli ishga tushirildi.
```

---

# 314-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 314

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 314-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_314 {
        void ishgaTushir();
        default String versiya() { return "v314.0"; }
    }

    static class AmalgaOshiruvchi_314 implements Xizmat_314 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_314 x = new AmalgaOshiruvchi_314();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v314.0 muvaffaqiyatli ishga tushirildi.
```

---

# 315-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 315

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 315-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_315 {
        void ishgaTushir();
        default String versiya() { return "v315.0"; }
    }

    static class AmalgaOshiruvchi_315 implements Xizmat_315 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_315 x = new AmalgaOshiruvchi_315();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v315.0 muvaffaqiyatli ishga tushirildi.
```

---

# 316-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 316

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 316-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_316 {
        void ishgaTushir();
        default String versiya() { return "v316.0"; }
    }

    static class AmalgaOshiruvchi_316 implements Xizmat_316 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_316 x = new AmalgaOshiruvchi_316();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v316.0 muvaffaqiyatli ishga tushirildi.
```

---

# 317-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 317

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 317-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_317 {
        void ishgaTushir();
        default String versiya() { return "v317.0"; }
    }

    static class AmalgaOshiruvchi_317 implements Xizmat_317 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_317 x = new AmalgaOshiruvchi_317();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v317.0 muvaffaqiyatli ishga tushirildi.
```

---

# 318-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 318

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 318-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_318 {
        void ishgaTushir();
        default String versiya() { return "v318.0"; }
    }

    static class AmalgaOshiruvchi_318 implements Xizmat_318 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_318 x = new AmalgaOshiruvchi_318();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v318.0 muvaffaqiyatli ishga tushirildi.
```

---

# 319-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 319

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 319-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_319 {
        void ishgaTushir();
        default String versiya() { return "v319.0"; }
    }

    static class AmalgaOshiruvchi_319 implements Xizmat_319 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_319 x = new AmalgaOshiruvchi_319();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v319.0 muvaffaqiyatli ishga tushirildi.
```

---

# 320-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 320

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 320-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_320 {
        void ishgaTushir();
        default String versiya() { return "v320.0"; }
    }

    static class AmalgaOshiruvchi_320 implements Xizmat_320 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_320 x = new AmalgaOshiruvchi_320();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v320.0 muvaffaqiyatli ishga tushirildi.
```

---

# 321-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 321

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 321-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_321 {
        void ishgaTushir();
        default String versiya() { return "v321.0"; }
    }

    static class AmalgaOshiruvchi_321 implements Xizmat_321 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_321 x = new AmalgaOshiruvchi_321();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v321.0 muvaffaqiyatli ishga tushirildi.
```

---

# 322-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 322

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 322-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_322 {
        void ishgaTushir();
        default String versiya() { return "v322.0"; }
    }

    static class AmalgaOshiruvchi_322 implements Xizmat_322 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_322 x = new AmalgaOshiruvchi_322();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v322.0 muvaffaqiyatli ishga tushirildi.
```

---

# 323-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 323

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 323-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_323 {
        void ishgaTushir();
        default String versiya() { return "v323.0"; }
    }

    static class AmalgaOshiruvchi_323 implements Xizmat_323 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_323 x = new AmalgaOshiruvchi_323();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v323.0 muvaffaqiyatli ishga tushirildi.
```

---

# 324-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 324

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 324-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_324 {
        void ishgaTushir();
        default String versiya() { return "v324.0"; }
    }

    static class AmalgaOshiruvchi_324 implements Xizmat_324 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_324 x = new AmalgaOshiruvchi_324();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v324.0 muvaffaqiyatli ishga tushirildi.
```

---

# 325-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 325

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 325-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_325 {
        void ishgaTushir();
        default String versiya() { return "v325.0"; }
    }

    static class AmalgaOshiruvchi_325 implements Xizmat_325 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_325 x = new AmalgaOshiruvchi_325();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v325.0 muvaffaqiyatli ishga tushirildi.
```

---

# 326-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 326

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 326-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_326 {
        void ishgaTushir();
        default String versiya() { return "v326.0"; }
    }

    static class AmalgaOshiruvchi_326 implements Xizmat_326 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_326 x = new AmalgaOshiruvchi_326();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v326.0 muvaffaqiyatli ishga tushirildi.
```

---

# 327-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 327

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 327-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_327 {
        void ishgaTushir();
        default String versiya() { return "v327.0"; }
    }

    static class AmalgaOshiruvchi_327 implements Xizmat_327 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_327 x = new AmalgaOshiruvchi_327();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v327.0 muvaffaqiyatli ishga tushirildi.
```

---

# 328-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 328

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 328-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_328 {
        void ishgaTushir();
        default String versiya() { return "v328.0"; }
    }

    static class AmalgaOshiruvchi_328 implements Xizmat_328 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_328 x = new AmalgaOshiruvchi_328();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v328.0 muvaffaqiyatli ishga tushirildi.
```

---

# 329-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 329

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 329-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_329 {
        void ishgaTushir();
        default String versiya() { return "v329.0"; }
    }

    static class AmalgaOshiruvchi_329 implements Xizmat_329 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_329 x = new AmalgaOshiruvchi_329();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v329.0 muvaffaqiyatli ishga tushirildi.
```

---

# 330-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 330

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 330-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_330 {
        void ishgaTushir();
        default String versiya() { return "v330.0"; }
    }

    static class AmalgaOshiruvchi_330 implements Xizmat_330 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_330 x = new AmalgaOshiruvchi_330();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v330.0 muvaffaqiyatli ishga tushirildi.
```

---

# 331-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 331

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 331-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_331 {
        void ishgaTushir();
        default String versiya() { return "v331.0"; }
    }

    static class AmalgaOshiruvchi_331 implements Xizmat_331 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_331 x = new AmalgaOshiruvchi_331();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v331.0 muvaffaqiyatli ishga tushirildi.
```

---

# 332-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 332

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 332-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_332 {
        void ishgaTushir();
        default String versiya() { return "v332.0"; }
    }

    static class AmalgaOshiruvchi_332 implements Xizmat_332 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_332 x = new AmalgaOshiruvchi_332();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v332.0 muvaffaqiyatli ishga tushirildi.
```

---

# 333-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 333

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 333-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_333 {
        void ishgaTushir();
        default String versiya() { return "v333.0"; }
    }

    static class AmalgaOshiruvchi_333 implements Xizmat_333 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_333 x = new AmalgaOshiruvchi_333();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v333.0 muvaffaqiyatli ishga tushirildi.
```

---

# 334-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 334

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 334-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_334 {
        void ishgaTushir();
        default String versiya() { return "v334.0"; }
    }

    static class AmalgaOshiruvchi_334 implements Xizmat_334 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_334 x = new AmalgaOshiruvchi_334();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v334.0 muvaffaqiyatli ishga tushirildi.
```

---

# 335-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 335

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 335-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_335 {
        void ishgaTushir();
        default String versiya() { return "v335.0"; }
    }

    static class AmalgaOshiruvchi_335 implements Xizmat_335 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_335 x = new AmalgaOshiruvchi_335();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v335.0 muvaffaqiyatli ishga tushirildi.
```

---

# 336-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 336

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 336-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_336 {
        void ishgaTushir();
        default String versiya() { return "v336.0"; }
    }

    static class AmalgaOshiruvchi_336 implements Xizmat_336 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_336 x = new AmalgaOshiruvchi_336();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v336.0 muvaffaqiyatli ishga tushirildi.
```

---

# 337-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 337

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 337-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_337 {
        void ishgaTushir();
        default String versiya() { return "v337.0"; }
    }

    static class AmalgaOshiruvchi_337 implements Xizmat_337 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_337 x = new AmalgaOshiruvchi_337();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v337.0 muvaffaqiyatli ishga tushirildi.
```

---

# 338-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 338

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 338-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_338 {
        void ishgaTushir();
        default String versiya() { return "v338.0"; }
    }

    static class AmalgaOshiruvchi_338 implements Xizmat_338 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_338 x = new AmalgaOshiruvchi_338();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v338.0 muvaffaqiyatli ishga tushirildi.
```

---

# 339-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 339

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 339-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_339 {
        void ishgaTushir();
        default String versiya() { return "v339.0"; }
    }

    static class AmalgaOshiruvchi_339 implements Xizmat_339 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_339 x = new AmalgaOshiruvchi_339();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v339.0 muvaffaqiyatli ishga tushirildi.
```

---

# 340-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 340

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 340-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_340 {
        void ishgaTushir();
        default String versiya() { return "v340.0"; }
    }

    static class AmalgaOshiruvchi_340 implements Xizmat_340 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_340 x = new AmalgaOshiruvchi_340();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v340.0 muvaffaqiyatli ishga tushirildi.
```

---

# 341-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 341

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 341-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_341 {
        void ishgaTushir();
        default String versiya() { return "v341.0"; }
    }

    static class AmalgaOshiruvchi_341 implements Xizmat_341 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_341 x = new AmalgaOshiruvchi_341();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v341.0 muvaffaqiyatli ishga tushirildi.
```

---

# 342-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 342

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 342-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_342 {
        void ishgaTushir();
        default String versiya() { return "v342.0"; }
    }

    static class AmalgaOshiruvchi_342 implements Xizmat_342 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_342 x = new AmalgaOshiruvchi_342();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v342.0 muvaffaqiyatli ishga tushirildi.
```

---

# 343-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 343

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 343-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_343 {
        void ishgaTushir();
        default String versiya() { return "v343.0"; }
    }

    static class AmalgaOshiruvchi_343 implements Xizmat_343 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_343 x = new AmalgaOshiruvchi_343();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v343.0 muvaffaqiyatli ishga tushirildi.
```

---

# 344-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 344

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 344-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_344 {
        void ishgaTushir();
        default String versiya() { return "v344.0"; }
    }

    static class AmalgaOshiruvchi_344 implements Xizmat_344 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_344 x = new AmalgaOshiruvchi_344();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v344.0 muvaffaqiyatli ishga tushirildi.
```

---

# 345-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 345

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 345-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_345 {
        void ishgaTushir();
        default String versiya() { return "v345.0"; }
    }

    static class AmalgaOshiruvchi_345 implements Xizmat_345 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_345 x = new AmalgaOshiruvchi_345();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v345.0 muvaffaqiyatli ishga tushirildi.
```

---

# 346-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 346

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 346-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_346 {
        void ishgaTushir();
        default String versiya() { return "v346.0"; }
    }

    static class AmalgaOshiruvchi_346 implements Xizmat_346 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_346 x = new AmalgaOshiruvchi_346();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v346.0 muvaffaqiyatli ishga tushirildi.
```

---

# 347-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 347

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 347-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_347 {
        void ishgaTushir();
        default String versiya() { return "v347.0"; }
    }

    static class AmalgaOshiruvchi_347 implements Xizmat_347 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_347 x = new AmalgaOshiruvchi_347();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v347.0 muvaffaqiyatli ishga tushirildi.
```

---

# 348-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 348

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 348-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_348 {
        void ishgaTushir();
        default String versiya() { return "v348.0"; }
    }

    static class AmalgaOshiruvchi_348 implements Xizmat_348 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_348 x = new AmalgaOshiruvchi_348();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v348.0 muvaffaqiyatli ishga tushirildi.
```

---

# 349-Topshiriq: Interfeyslar va Abstraktsiya amaliyoti: Modul 349

## Topshiriq sharti:
Java interfeyslari orqali bo'sh bog'lanish va shartnoma arxitekturasini ko'rsatuvchi 349-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Xizmat_349 {
        void ishgaTushir();
        default String versiya() { return "v349.0"; }
    }

    static class AmalgaOshiruvchi_349 implements Xizmat_349 {
        @Override
        public void ishgaTushir() {
            System.out.println("Xizmat " + versiya() + " muvaffaqiyatli ishga tushirildi.");
        }
    }

    public static void main(String[] args) {
        Xizmat_349 x = new AmalgaOshiruvchi_349();
        x.ishgaTushir();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda interfeys shartnomasi va uning default metodi namoyish etildi.
Bu Dependency Inversion (DIP) prinsipiga to'liq mos keladi.

## Ishlash natijasi:
```text
Xizmat v349.0 muvaffaqiyatli ishga tushirildi.
```

---

# 350-Topshiriq: Xulosa topshiriq: To'lov shlyuzlari (Payment Gateway) interfeys tizimi

## Topshiriq sharti:
Interfeyslar, default/static metodlar, ko'p qirrali amalga oshirish va Dependency Inversion Principle ni birlashtirgan Universal To'lov Shlyuzi arxitekturasini yarating.

## Yechim (Java kodi):
```java
import java.util.Objects;

public class Solution {
    public record TolovNatijasi(boolean muvaffaqiyatli, String tranzaksiyaId, String xabar) {}

    interface TolovShlyuzi {
        TolovNatijasi tolovQabulQil(String hisob, double summa);

        default void logYoz(String xabar) {
            System.out.println("[AUDIT SHLYUZ] " + xabar);
        }

        static TolovShlyuzi standartTanlov() {
            return new PaymeShlyuzi();
        }
    }

    static class PaymeShlyuzi implements TolovShlyuzi {
        @Override
        public TolovNatijasi tolovQabulQil(String hisob, double summa) {
            logYoz("Payme orqali " + summa + " so'm yechilmoqda (" + hisob + ")");
            return new TolovNatijasi(true, "PAYME-" + System.currentTimeMillis(), "To'lov o'tdi");
        }
    }

    static class UzumShlyuzi implements TolovShlyuzi {
        @Override
        public TolovNatijasi tolovQabulQil(String hisob, double summa) {
            logYoz("UzumPay orqali " + summa + " so'm yechilmoqda (" + hisob + ")");
            return new TolovNatijasi(true, "UZUM-" + System.currentTimeMillis(), "To'lov muvaffaqiyatli");
        }
    }

    // Yuqori darajadagi biznes sinfi faqat interfeysga bog'langan (DIP)
    static class DokonXizmati {
        private final TolovShlyuzi shlyuz;

        public DokonXizmati(TolovShlyuzi shlyuz) {
            this.shlyuz = Objects.requireNonNull(shlyuz);
        }

        public void xaridniRasmiylashtir(String mijozKarta, double summa) {
            TolovNatijasi natija = shlyuz.tolovQabulQil(mijozKarta, summa);
            if (natija.muvaffaqiyatli()) {
                System.out.println("Xarid yakunlandi! Tranzaksiya: " + natija.tranzaksiyaId());
            }
        }
    }

    public static void main(String[] args) {
        DokonXizmati d1 = new DokonXizmati(TolovShlyuzi.standartTanlov());
        d1.xaridniRasmiylashtir("86001234...", 120000.0);

        DokonXizmati d2 = new DokonXizmati(new UzumShlyuzi());
        d2.xaridniRasmiylashtir("98604321...", 450000.0);
    }
}
```

## Tushuntirish va Mantiq:
Ushbu mukammal arxitekturada:
1. `TolovShlyuzi` barcha to'lov provayderlari uchun qat'iy standart shartnomani o'rnatdi.
2. `DokonXizmati` aniq implementatsiyalarga (Payme yoki Uzum) emas, faqat abstrakt interfeysga tayanadi (Dependency Inversion Principle).
3. Yangi to'lov tizimini qo'shish mavjud do'kon kodiga zarracha o'zgartirish kiritmasdan amalga oshiriladi (Open-Closed Principle).

## Ishlash natijasi:
```text
[AUDIT SHLYUZ] Payme orqali 120000.0 so'm yechilmoqda (86001234...)
Xarid yakunlandi! Tranzaksiya: PAYME-...
[AUDIT SHLYUZ] UzumPay orqali 450000.0 so'm yechilmoqda (98604321...)
Xarid yakunlandi! Tranzaksiya: UZUM-...
```
