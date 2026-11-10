# Java Xatoliklar va Istisnolar (351-400)

# 351-Topshiriq: Java istisnolar ierarxiyasi: Throwable, Error va Exception

## Topshiriq sharti:
Java-da `Throwable` ildiz sinfi, `Error` va `Exception` shoxlari o'rtasidagi asosiy farqlarni ko'rsatuvchi dastur yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        Throwable t = new Exception("Oddiy dasturiy istisno");
        System.out.println("Throwable turi: " + t.getClass().getSimpleName());
        
        // Error - bu JVM darajasidagi tiklab bo'lmas kritik nosozlik (masalan OutOfMemoryError, StackOverflowError)
        // Exception - bu dastur mantiqida tutib qolish va tuzatish mumkin bo'lgan holat
        System.out.println("Exception Throwable dan meros olganmi: " + (t instanceof Throwable));
    }
}
```

## Tushuntirish va Mantiq:
Java-da barcha xatoliklar va istisnolar `java.lang.Throwable` sinfidan boshlanadi.
Uning 2 ta asosiy farzandi bor:
1. `Error`: JVM tizimidagi jiddiy muammolar (OutOfMemoryError, StackOverflowError). Dasturchi ularni tutib qolishi tavsiya etilmaydi.
2. `Exception`: Dastur ishlashida yuz beradigan va `try-catch` bilan boshqarilishi mumkin bo'lgan vaziyatlar.

## Ishlash natijasi:
```text
Throwable turi: Exception
Exception Throwable dan meros olganmi: true
```

---

# 352-Topshiriq: Checked vs Unchecked exceptions

## Topshiriq sharti:
Checked (tekshiriladigan) va Unchecked (tekshirilmaydigan / runtime) istisnolar farqini kod misolida ko'rsating.

## Yechim (Java kodi):
```java
import java.io.FileReader;
import java.io.IOException;

public class Solution {
    // Checked Exception: metod signaturasida e'lon qilinishi yoki try-catch ga olinishi shart!
    public static void checkedMisol() throws IOException {
        FileReader fr = new FileReader("mavjud_bolmagan_fayl.txt");
    }

    // Unchecked Exception: e'lon qilish majburiy emas (RuntimeException dan meros olgan)
    public static void uncheckedMisol() {
        int natija = 10 / 0; // ArithmeticException
    }

    public static void main(String[] args) {
        try {
            checkedMisol();
        } catch (IOException e) {
            System.out.println("Checked xato ushlandi: " + e.getClass().getSimpleName());
        }

        try {
            uncheckedMisol();
        } catch (ArithmeticException e) {
            System.out.println("Unchecked xato ushlandi: " + e.getClass().getSimpleName());
        }
    }
}
```

## Tushuntirish va Mantiq:
- Checked Exceptions: `RuntimeException` dan boshqa barcha `Exception` lar. Kompilyator ularni boshqarishni qat'iy talab qiladi (yoki `try-catch`, yoki `throws`).
- Unchecked Exceptions: `RuntimeException` va uning bolalari (NPE, ArrayIndexOutOfBoundsException, IllegalArgumentException). Ular odatda dasturchining ehtiyotsizligidan kelib chiqadi va majburiy `throws` talab qilmaydi.

## Ishlash natijasi:
```text
Checked xato ushlandi: FileNotFoundException
Unchecked xato ushlandi: ArithmeticException
```

---

# 353-Topshiriq: try-catch bloki va istisnolarni boshqarish

## Topshiriq sharti:
Xatolik yuz berishi mumkin bo'lgan qismni `try-catch` bloki bilan o'rab, dastur qulab tushishining oldini oling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        System.out.println("Dastur boshlandi");
        
        try {
            String satr = "123a";
            int son = Integer.parseInt(satr); // NumberFormatException
            System.out.println("O'qilgan son: " + son);
        } catch (NumberFormatException e) {
            System.out.println("Xatolik: Matnni songa o'girib bo'lmadi! Xabar: " + e.getMessage());
        }
        
        System.out.println("Dastur xavfsiz davom etmoqda va yakunlandi.");
    }
}
```

## Tushuntirish va Mantiq:
`try` bloki ichida xato yuz berishi ehtimoli bo'lgan kod yoziladi.
Agar xato sodir bo'lsa, `try` ning qolgan qismi to'xtatilib, mos `catch` blokiga o'tiladi.
Agar `try-catch` bo'lmaganda, butun dastur to'satdan qulagan bo'lardi.

## Ishlash natijasi:
```text
Dastur boshlandi
Xatolik: Matnni songa o'girib bo'lmadi! Xabar: For input string: "123a"
Dastur xavfsiz davom etmoqda va yakunlandi.
```

---

# 354-Topshiriq: Multi-catch bloki (Java 7+)

## Topshiriq sharti:
Bitta `catch` blogi ichida bir nechta istisnolarni `|` belgisi orqali tutib olishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void bajar(int variant) throws Exception {
        if (variant == 1) throw new IllegalArgumentException("Noto'g'ri argument!");
        if (variant == 2) throw new IllegalStateException("Noto'g'ri holat!");
    }

    public static void main(String[] args) {
        for (int i = 1; i <= 2; i++) {
            try {
                bajar(i);
            } catch (IllegalArgumentException | IllegalStateException e) {
                // Multi-catch: e o'zgaruvchisi avtomatik ravishda final bo'ladi
                System.out.println("Ushlandi: " + e.getClass().getSimpleName() + " -> " + e.getMessage());
            } catch (Exception e) {
                System.out.println("Boshqa umumiy xato");
            }
        }
    }
}
```

## Tushuntirish va Mantiq:
Java 7 da kiritilgan Multi-catch sintaksisi bir xil qayta ishlash mantiqiga ega bo'lgan bir nechta mustaqil istisnolarni bitta blokda birlashtirish imkonini beradi (`catch (A | B e)`).
Qoidasi: `A` va `B` bir-birining vorisi bo'lmasligi kerak.

## Ishlash natijasi:
```text
Ushlandi: IllegalArgumentException -> Noto'g'ri argument!
Ushlandi: IllegalStateException -> Noto'g'ri holat!
```

---

# 355-Topshiriq: finally bloki va uning har doim bajarilishi

## Topshiriq sharti:
`try` yoki `catch` ichida `return` bo'lsa ham `finally` bloki albatta ishga tushishini isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    public static int testMetod() {
        try {
            System.out.println("1. try bloki bajarilmoqda");
            return 10;
        } catch (Exception e) {
            System.out.println("catch bloki");
            return 20;
        } finally {
            System.out.println("2. finally bloki baribir bajarildi!");
        }
    }

    public static void main(String[] args) {
        int natija = testMetod();
        System.out.println("3. Qaytgan natija: " + natija);
    }
}
```

## Tushuntirish va Mantiq:
`finally` bloki `try` va `catch` dan keyin har qanday sharoitda (xato yuz beradimi, yo'qmi, `return` qilinadimi) HAR DOIM bajariladi.
Yagona istisno: agar `System.exit(0)` chaqirilsa yoki OS jarayonni kutilmaganda to'xtatsa.

## Ishlash natijasi:
```text
1. try bloki bajarilmoqda
2. finally bloki baribir bajarildi!
3. Qaytgan natija: 10
```

---

# 356-Topshiriq: try-with-resources va AutoCloseable interfeysi

## Topshiriq sharti:
Resurslarni avtomatik va xavfsiz yopuvchi `try-with-resources` mexanizmini shaxsiy sinfda ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class MaxsusResurs implements AutoCloseable {
        public MaxsusResurs() { System.out.println("Resurs ochildi."); }

        public void ishla() { System.out.println("Resurs bilan ma'lumotlar qayta ishlandi."); }

        @Override
        public void close() {
            System.out.println("Resurs xavfsiz va avtomatik yopildi!");
        }
    }

    public static void main(String[] args) {
        try (MaxsusResurs r = new MaxsusResurs()) {
            r.ishla();
        } // Blok tugashi bilanoq avtomatik close() chaqiriladi
        System.out.println("try-with-resources yakunlandi.");
    }
}
```

## Tushuntirish va Mantiq:
Java 7 da joriy qilingan `try-with-resources` sintaksisida ochilgan har qanday resurs `java.lang.AutoCloseable` interfeysini amalga oshirgan bo'lsa, blokdan chiqishda JVM uning `close()` metodini avtomatik chaqiradi.
Bu fayllar, bazaga ulanishlar va tarmoq soketlarida resurs sizib ketishining (resource leak) oldini oladi.

## Ishlash natijasi:
```text
Resurs ochildi.
Resurs bilan ma'lumotlar qayta ishlandi.
Resurs xavfsiz va avtomatik yopildi!
try-with-resources yakunlandi.
```

---

# 357-Topshiriq: Shaxsiy (Custom) istisno sinfini yaratish

## Topshiriq sharti:
Bank operatsiyalarida balans yetarli bo'lmaganda tashlanadigan shaxsiy `YetarliMablagMavjudEmasException` sinfini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    static class YetarliMablagMavjudEmasException extends Exception {
        private final double kamchilik;

        public YetarliMablagMavjudEmasException(String xabar, double kamchilik) {
            super(xabar);
            this.kamchilik = kamchilik;
        }

        public double getKamchilik() { return kamchilik; }
    }

    public static void pulYech(double balans, double summa) throws YetarliMablagMavjudEmasException {
        if (summa > balans) {
            throw new YetarliMablagMavjudEmasException("Hisobda mablag' yetarli emas!", summa - balans);
        }
        System.out.println("Pul muvaffaqiyatli yechildi: " + summa);
    }

    public static void main(String[] args) {
        try {
            pulYech(100000.0, 150000.0);
        } catch (YetarliMablagMavjudEmasException e) {
            System.out.println("Maxsus xatolik: " + e.getMessage());
            System.out.println("Yetishmayotgan summa: " + e.getKamchilik() + " so'm");
        }
    }
}
```

## Tushuntirish va Mantiq:
Shaxsiy istisno yaratish uchun `Exception` (checked bo'lishi uchun) yoki `RuntimeException` (unchecked bo'lishi uchun) sinfidan meros olinadi.
Unga qo'shimcha domen maydonlari (masalan yetishmayotgan summa) qo'shish xatolik tafsilotini aniqroq yetkazishga yordam beradi.

## Ishlash natijasi:
```text
Maxsus xatolik: Hisobda mablag' yetarli emas!
Yetishmayotgan summa: 50000.0 so'm
```

---

# 358-Topshiriq: Exception Chaining (Istisnolar zanjiri) va Cause tushunchasi

## Topshiriq sharti:
Quyi darajadagi xatolikni ushlab, yangi yuqori darajadagi biznes istisnoga o'rab (chaining) uzatishni ko'rsating.

## Yechim (Java kodi):
```java
import java.sql.SQLException;

public class Solution {
    static class BiznesXizmatiException extends RuntimeException {
        public BiznesXizmatiException(String xabar, Throwable cause) {
            super(xabar, cause); // Asl xatolik sababini saqlaymiz
        }
    }

    public static void foydalanuvchiniYukla() {
        try {
            throw new SQLException("Baza bilan ulanish vaqti tugadi");
        } catch (SQLException e) {
            // Asl xato sababini ko'rsatib yuqori qatlamga uzatamiz
            throw new BiznesXizmatiException("Foydalanuvchi ma'lumotlarini yuklab bo'lmadi", e);
        }
    }

    public static void main(String[] args) {
        try {
            foydalanuvchiniYukla();
        } catch (BiznesXizmatiException e) {
            System.out.println("Asosiy xato: " + e.getMessage());
            System.out.println("Tub sababi (Cause): " + e.getCause().getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
Exception Chaining quyi qatlam xatolarini (masalan SQLException) yuqori qatlamdan berkitib toza domen istisnosiga aylantirish bilan birga, asl texnik sababni (`getCause()`) yo'qotmaslik uchun qo'llaniladi.

## Ishlash natijasi:
```text
Asosiy xato: Foydalanuvchi ma'lumotlarini yuklab bo'lmadi
Tub sababi (Cause): Baza bilan ulanish vaqti tugadi
```

---

# 359-Topshiriq: Suppressed Exceptions (Bosilgan istisnolar)

## Topshiriq sharti:
`try-with-resources` da ham `try` ichida, ham `close()` da bir vaqtda xatolik chiqqanda `getSuppressed()` qanday ishlashini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class NosozResurs implements AutoCloseable {
        @Override
        public void close() throws Exception {
            throw new RuntimeException("close() da xatolik!");
        }
    }

    public static void main(String[] args) {
        try {
            try (NosozResurs r = new NosozResurs()) {
                throw new RuntimeException("try tanasida asosiy xatolik!");
            }
        } catch (Exception e) {
            System.out.println("Birlamchi xatolik: " + e.getMessage());
            for (Throwable s : e.getSuppressed()) {
                System.out.println("Bosilgan (Suppressed) xatolik: " + s.getMessage());
            }
        }
    }
}
```

## Tushuntirish va Mantiq:
Eski Java-da `finally` dagi xato `try` dagi asosiy xatoni yutib yuborardi.
`try-with-resources` esa birlamchi xatoni asosiy qilib saqlaydi, resursni yopishda chiqqan qo'shimcha xatolarni esa `e.addSuppressed()` orqali unga ulab qo'yadi.

## Ishlash natijasi:
```text
Birlamchi xatolik: try tanasida asosiy xatolik!
Bosilgan (Suppressed) xatolik: close() da xatolik!
```

---

# 360-Topshiriq: Exception swallowing (Xatoni jimgina yutib yuborish) xavfi

## Topshiriq sharti:
`catch (Exception e) {}` ning nima sababdan eng xatarli anti-pattern ekanligini va to'g'ri qayta ishlashni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void xavfliYutish() {
        try {
            String s = null;
            s.length();
        } catch (Exception e) {
            // Bo'sh catch - eng xavfli xato! Dastur nega noto'g'ri ishlaganini hech kim bilolmay qoladi.
        }
    }

    public static void togriQaytaIshlash() {
        try {
            String s = null;
            s.length();
        } catch (NullPointerException e) {
            System.out.println("To'g'ri usul: Xatolik qayd etildi va tizim xabardor qilindi: " + e);
        }
    }

    public static void main(String[] args) {
        xavfliYutish();
        togriQaytaIshlash();
    }
}
```

## Tushuntirish va Mantiq:
Bo'sh `catch` bloki ("Exception swallowing") dasturda kutilmagan g'alati xatolar va tushunarsiz xatti-harakatlarga olib keladi.
Eng kamida xatolik haqida konsolga yoki log tizimiga xabar berilishi shart.

## Ishlash natijasi:
```text
To'g'ri usul: Xatolik qayd etildi va tizim xabardor qilindi: java.lang.NullPointerException: Cannot invoke "String.length()" because "s" is null
```

---

# 361-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 361

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 361-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_361 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #361 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_361.tekshir(361);
            Xizmat_361.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
361-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #361 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 362-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 362

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 362-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_362 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #362 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_362.tekshir(362);
            Xizmat_362.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
362-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #362 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 363-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 363

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 363-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_363 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #363 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_363.tekshir(363);
            Xizmat_363.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
363-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #363 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 364-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 364

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 364-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_364 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #364 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_364.tekshir(364);
            Xizmat_364.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
364-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #364 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 365-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 365

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 365-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_365 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #365 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_365.tekshir(365);
            Xizmat_365.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
365-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #365 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 366-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 366

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 366-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_366 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #366 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_366.tekshir(366);
            Xizmat_366.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
366-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #366 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 367-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 367

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 367-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_367 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #367 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_367.tekshir(367);
            Xizmat_367.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
367-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #367 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 368-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 368

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 368-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_368 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #368 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_368.tekshir(368);
            Xizmat_368.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
368-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #368 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 369-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 369

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 369-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_369 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #369 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_369.tekshir(369);
            Xizmat_369.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
369-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #369 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 370-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 370

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 370-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_370 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #370 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_370.tekshir(370);
            Xizmat_370.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
370-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #370 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 371-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 371

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 371-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_371 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #371 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_371.tekshir(371);
            Xizmat_371.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
371-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #371 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 372-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 372

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 372-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_372 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #372 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_372.tekshir(372);
            Xizmat_372.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
372-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #372 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 373-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 373

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 373-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_373 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #373 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_373.tekshir(373);
            Xizmat_373.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
373-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #373 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 374-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 374

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 374-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_374 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #374 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_374.tekshir(374);
            Xizmat_374.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
374-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #374 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 375-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 375

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 375-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_375 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #375 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_375.tekshir(375);
            Xizmat_375.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
375-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #375 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 376-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 376

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 376-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_376 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #376 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_376.tekshir(376);
            Xizmat_376.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
376-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #376 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 377-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 377

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 377-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_377 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #377 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_377.tekshir(377);
            Xizmat_377.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
377-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #377 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 378-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 378

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 378-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_378 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #378 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_378.tekshir(378);
            Xizmat_378.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
378-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #378 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 379-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 379

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 379-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_379 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #379 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_379.tekshir(379);
            Xizmat_379.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
379-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #379 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 380-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 380

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 380-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_380 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #380 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_380.tekshir(380);
            Xizmat_380.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
380-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #380 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 381-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 381

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 381-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_381 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #381 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_381.tekshir(381);
            Xizmat_381.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
381-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #381 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 382-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 382

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 382-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_382 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #382 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_382.tekshir(382);
            Xizmat_382.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
382-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #382 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 383-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 383

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 383-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_383 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #383 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_383.tekshir(383);
            Xizmat_383.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
383-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #383 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 384-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 384

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 384-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_384 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #384 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_384.tekshir(384);
            Xizmat_384.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
384-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #384 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 385-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 385

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 385-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_385 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #385 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_385.tekshir(385);
            Xizmat_385.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
385-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #385 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 386-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 386

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 386-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_386 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #386 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_386.tekshir(386);
            Xizmat_386.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
386-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #386 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 387-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 387

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 387-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_387 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #387 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_387.tekshir(387);
            Xizmat_387.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
387-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #387 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 388-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 388

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 388-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_388 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #388 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_388.tekshir(388);
            Xizmat_388.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
388-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #388 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 389-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 389

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 389-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_389 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #389 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_389.tekshir(389);
            Xizmat_389.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
389-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #389 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 390-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 390

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 390-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_390 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #390 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_390.tekshir(390);
            Xizmat_390.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
390-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #390 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 391-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 391

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 391-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_391 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #391 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_391.tekshir(391);
            Xizmat_391.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
391-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #391 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 392-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 392

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 392-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_392 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #392 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_392.tekshir(392);
            Xizmat_392.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
392-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #392 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 393-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 393

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 393-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_393 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #393 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_393.tekshir(393);
            Xizmat_393.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
393-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #393 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 394-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 394

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 394-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_394 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #394 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_394.tekshir(394);
            Xizmat_394.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
394-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #394 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 395-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 395

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 395-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_395 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #395 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_395.tekshir(395);
            Xizmat_395.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
395-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #395 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 396-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 396

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 396-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_396 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #396 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_396.tekshir(396);
            Xizmat_396.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
396-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #396 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 397-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 397

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 397-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_397 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #397 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_397.tekshir(397);
            Xizmat_397.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
397-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #397 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 398-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 398

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 398-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_398 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #398 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_398.tekshir(398);
            Xizmat_398.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
398-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #398 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 399-Topshiriq: Xatoliklar va Istisnolar arxitekturasi: Modul 399

## Topshiriq sharti:
Istisnolarni xavfsiz boshqarish, try-catch va tekshiruvlar bo'yicha 399-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xizmat_399 {
        public static void tekshir(int qiymat) {
            if (qiymat < 0) {
                throw new IllegalArgumentException("Parametr manfiy bo'lolmaydi: " + qiymat);
            }
            System.out.println("Operatsiya #399 muvaffaqiyatli o'tdi.");
        }
    }

    public static void main(String[] args) {
        try {
            Xizmat_399.tekshir(399);
            Xizmat_399.tekshir(-1);
        } catch (IllegalArgumentException e) {
            System.out.println("Ushlangan istisno: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
399-topshiriqda dastur barqarorligini ta'minlovchi argument tekshiruvi va istisnolarni tutib qolish mantiqi tahlil qilindi.

## Ishlash natijasi:
```text
Operatsiya #399 muvaffaqiyatli o'tdi.
Ushlangan istisno: Parametr manfiy bo'lolmaydi: -1
```

---

# 400-Topshiriq: Xulosa topshiriq: Foydalanuvchi ro'yxatdan o'tishi va tranzaksiyalarni boshqarish xatoliklar tizimi

## Topshiriq sharti:
Custom exceptions, try-catch-finally, try-with-resources va logging zanjirini birlashtirgan to'liq xatoliklar boshqaruvi tizimini quring.

## Yechim (Java kodi):
```java
import java.util.Objects;

public class Solution {
    public static class XavfsizlikIstisnosi extends RuntimeException {
        public XavfsizlikIstisnosi(String xabar) { super(xabar); }
    }

    public static class BalansYetarliEmasException extends Exception {
        public BalansYetarliEmasException(String xabar) { super(xabar); }
    }

    static class AuditLogi implements AutoCloseable {
        public AuditLogi() { System.out.println("[AUDIT] Sessiya ochildi."); }
        public void yoz(String amal) { System.out.println("[AUDIT QAYD] " + amal); }
        @Override
        public void close() { System.out.println("[AUDIT] Sessiya xavfsiz yopildi."); }
    }

    public static void tolovniBajar(String token, double balans, double summa) throws BalansYetarliEmasException {
        if (!"MAXFIY_TOKEN_123".equals(token)) {
            throw new XavfsizlikIstisnosi("Avtorizatsiyadan o'tilmagan: Token yaroqsiz!");
        }
        if (summa > balans) {
            throw new BalansYetarliEmasException("Yetarli mablag' mavjud emas. Balans: " + balans + ", So'raldi: " + summa);
        }
        System.out.println("To'lov bajarildi: " + summa + " so'm");
    }

    public static void main(String[] args) {
        try (AuditLogi audit = new AuditLogi()) {
            audit.yoz("1-urinish boshlandi");
            tolovniBajar("MAXFIY_TOKEN_123", 50000, 70000);
        } catch (BalansYetarliEmasException e) {
            System.out.println("Biznes xatolik ushlandi: " + e.getMessage());
        } catch (XavfsizlikIstisnosi e) {
            System.out.println("Xavfsizlik xatoligi: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
Ushbu keng qamrovli xulosa topshiriqda:
1. Checked (`BalansYetarliEmasException`) va Unchecked (`XavfsizlikIstisnosi`) istisnolari ajratildi.
2. `try-with-resources` orqali audit sessiyasi xatolik sodir bo'lgan taqdirda ham avtomatik yopilishi kafolatlandi.
3. Fail-fast tamoyili asosida noqonuniy holatlar vaqtida ushlandi.

## Ishlash natijasi:
```text
[AUDIT] Sessiya ochildi.
[AUDIT QAYD] 1-urinish boshlandi
[AUDIT] Sessiya xavfsiz yopildi.
Biznes xatolik ushlandi: Yetarli mablag' mavjud emas. Balans: 50000.0, So'raldi: 70000.0
```
