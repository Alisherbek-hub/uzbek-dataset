# Java Reflection va Annotatsiyalar (751-800)

# 751-Topshiriq: Reflection API: Class<?> obyektini olish va sinf tuzilishini tekshirish

## Topshiriq sharti:
Java Reflection API orqali sinfning nomi, paketlari va modifikatorlarini dastur ishlab turgan paytda (runtime) aniqlang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        Class<?> satrKlassi = String.class;

        System.out.println("To'liq nomi: " + satrKlassi.getName());
        System.out.println("Oddiy nomi: " + satrKlassi.getSimpleName());
        System.out.println("Ota sinfi: " + satrKlassi.getSuperclass().getSimpleName());
        System.out.println("Interfeyslar soni: " + satrKlassi.getInterfaces().length);
    }
}
```

## Tushuntirish va Mantiq:
Java Reflection API dasturga o'zining tuzilishini (metama'lumotlarini) ish vaqtida tekshirish va manipulyatsiya qilish imkonini beradi.
`Class<?>` obyektini olishning 3 xil usuli bor:
1. `String.class` (literal)
2. `obj.getClass()` (obyekt orqali)
3. `Class.forName("java.lang.String")` (dinamik yuklash).

## Ishlash natijasi:
```text
To'liq nomi: java.lang.String
Oddiy nomi: String
Ota sinfi: Object
Interfeyslar soni: 3
```

---

# 752-Topshiriq: Private maydonlarni o'qish va setAccessible(true)

## Topshiriq sharti:
Reflection yordamida obyektning `private` maydonini tashqaridan buzib o'qish va qiymatini o'zgartirishni ko'rsating.

## Yechim (Java kodi):
```java
import java.lang.reflect.Field;

public class Solution {
    static class MaxfiyXazina {
        private String parol = "SuperMaxfiy2026";
    }

    public static void main(String[] args) throws Exception {
        MaxfiyXazina xazina = new MaxfiyXazina();

        Field parolMaydoni = MaxfiyXazina.class.getDeclaredField("parol");
        parolMaydoni.setAccessible(true); // Private himoyani chetlab o'tish

        // O'qish
        String eskiParol = (String) parolMaydoni.get(xazina);
        System.out.println("Buzib o'qilgan parol: " + eskiParol);

        // Yozish
        parolMaydoni.set(xazina, "YangiBuzilganParol");
        System.out.println("Yangi o'rnatilgan parol: " + parolMaydoni.get(xazina));
    }
}
```

## Tushuntirish va Mantiq:
`getDeclaredField("nom")` sinfda e'lon qilingan barcha (shu jumladan `private`) maydonlarni topadi.
`setAccessible(true)` Java Access Control tekshiruvini o'chirib qo'yadi.
Bu Spring, Hibernate va test kutubxonalarida (JUnit, Mockito) obyektlarni initsializatsiya qilishda keng qo'llaniladi (ammo xavfsizlik nuqtai nazaridan Java modullarida qat'iy cheklanadi).

## Ishlash natijasi:
```text
Buzib o'qilgan parol: SuperMaxfiy2026
Yangi o'rnatilgan parol: YangiBuzilganParol
```

---

# 753-Topshiriq: Dinamik metod chaqirish: Method.invoke()

## Topshiriq sharti:
Metod nomini satr ko'rinishida bilgan holda, uni Reflection orqali dinamik chaqiruvchi dastur tuzing.

## Yechim (Java kodi):
```java
import java.lang.reflect.Method;

public class Solution {
    static class Hisoblagich {
        public int kopaytir(int a, int b) {
            return a * b;
        }
    }

    public static void main(String[] args) throws Exception {
        Hisoblagich h = new Hisoblagich();

        // Metodni nomi va parametr turlari bo'yicha topamiz
        Method metod = Hisoblagich.class.getMethod("kopaytir", int.class, int.class);

        // Dinamik ishga tushirish (invoke)
        Object natija = metod.invoke(h, 6, 7);
        System.out.println("Metod chaqirildi, natija: " + natija);
    }
}
```

## Tushuntirish va Mantiq:
`Method.invoke(obyekt, argumentlar)` dinamik ravishda metodni chaqiradi.
Agar metod `static` bo'lsa, birinchi parametrga `null` beriladi.
Bu Dependency Injection va RPC (Remote Procedure Call) protokollarining asosi hisoblanadi.

## Ishlash natijasi:
```text
Metod chaqirildi, natija: 42
```

---

# 754-Topshiriq: Konstruktor orqali dinamik obyekt yaratish: Constructor.newInstance()

## Topshiriq sharti:
`Class.newInstance()` ning eskirganligi sababi va zamonaviy `getConstructor().newInstance()` bilan obyekt yasashni ko'rsating.

## Yechim (Java kodi):
```java
import java.lang.reflect.Constructor;

public class Solution {
    static class Foydalanuvchi {
        private final String ism;
        public Foydalanuvchi(String ism) { this.ism = ism; }
        @Override
        public String toString() { return "Foydalanuvchi[" + ism + "]"; }
    }

    public static void main(String[] args) throws Exception {
        // Parametrli konstruktorni topamiz
        Constructor<Foydalanuvchi> c = Foydalanuvchi.class.getConstructor(String.class);

        // Yangi obyekt yaratamiz
        Foydalanuvchi f = c.newInstance("Temur");
        System.out.println("Dinamik yaratilgan obyekt: " + f);
    }
}
```

## Tushuntirish va Mantiq:
Eski `Class.newInstance()` metodining ko'plab kamchiliklari bo'lgan (checked exceptionlarni yashirgan, faqat no-arg konstruktorlar bilan ishlagan).
Java 9 dan boshlab `getConstructor().newInstance(...)` standarti qat'iy tavsiya etiladi.

## Ishlash natijasi:
```text
Dinamik yaratilgan obyekt: Foydalanuvchi[Temur]
```

---

# 755-Topshiriq: Custom Annotatsiya yaratish va uning atributlari

## Topshiriq sharti:
Metodning muallifi va versiyasini belgilovchi maxsus `@Muallif` annotatsiyasini e'lon qiling va qo'llang.

## Yechim (Java kodi):
```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

public class Solution {
    @Retention(RetentionPolicy.RUNTIME) // Dastur ishlab turganda o'qish uchun
    @Target(ElementType.METHOD)          // Faqat metodlarga qo'yilishi mumkin
    @interface Muallif {
        String ism();
        String versiya() default "1.0";
    }

    static class Xizmat {
        @Muallif(ism = "Bobur", versiya = "2.5")
        public void ishBajar() {
            System.out.println("Xizmat ishi bajarildi.");
        }
    }

    public static void main(String[] args) throws Exception {
        var metod = Xizmat.class.getMethod("ishBajar");
        Muallif annotatsiya = metod.getAnnotation(Muallif.class);

        System.out.println("Metod muallifi: " + annotatsiya.ism());
        System.out.println("Metod versiyasi: " + annotatsiya.versiya());
    }
}
```

## Tushuntirish va Mantiq:
Annotatsiyalar — Java kodiga biriktiriladigan metama'lumotlardir (`@interface`).
Meta-annotatsiyalar:
- `@Retention(RUNTIME)`: baytkodda saqlanadi va Reflection orqali o'qiladi.
- `@Target`: annotatsiya qayerga (sinfga, metodga, maydonga) qo'yilishini cheklaydi.

## Ishlash natijasi:
```text
Metod muallifi: Bobur
Metod versiyasi: 2.5
```

---

# 756-Topshiriq: Mini Dependency Injection (IoC) konteynerini Reflection bilan qurish

## Topshiriq sharti:
Oddiy `@Inject` annotatsiyasi orqali sinf maydonlariga bog'liqliklarni avtomatik joylovchi (Autowiring) tizim tuzing.

## Yechim (Java kodi):
```java
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.reflect.Field;

public class Solution {
    @Retention(RetentionPolicy.RUNTIME)
    @interface Inject {}

    static class EmailXizmati {
        public void xabarYubor(String kimgadir) {
            System.out.println("Email yuborildi: " + kimgadir);
        }
    }

    static class BuyurtmaXizmati {
        @Inject
        private EmailXizmati emailXizmati;

        public void buyurtma(String mijoz) {
            emailXizmati.xabarYubor(mijoz);
        }
    }

    // Mini IoC DI konteyneri
    public static <T> T konteynerYarat(Class<T> klass) throws Exception {
        T obyekt = klass.getConstructor().newInstance();
        for (Field f : klass.getDeclaredFields()) {
            if (f.isAnnotationPresent(Inject.class)) {
                f.setAccessible(true);
                Object bogliqlik = f.getType().getConstructor().newInstance();
                f.set(obyekt, bogliqlik); // Inyeksiya
            }
        }
        return obyekt;
    }

    public static void main(String[] args) throws Exception {
        BuyurtmaXizmati xizmat = konteynerYarat(BuyurtmaXizmati.class);
        xizmat.buyurtma("Ulug'bek");
    }
}
```

## Tushuntirish va Mantiq:
Spring Framework va Google Guice kabi kutubxonalar aynan shu Reflection mexanizmi asosida ishlaydi.
Konteyner `@Inject` yoki `@Autowired` qo'yilgan maydonlarni topadi, mos obyektni yaratadi va `field.set()` orqali inyeksiya qiladi.

## Ishlash natijasi:
```text
Email yuborildi: Ulug'bek
```

---

# 757-Topshiriq: Dynamic Proxy (Dinamik proksi) va InvocationHandler

## Topshiriq sharti:
Java ning standart `java.lang.reflect.Proxy` vositasi orqali metod chaqiruvlarini tutib oluvchi (Logging AOP) proksi yarating.

## Yechim (Java kodi):
```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

public class Solution {
    interface Xizmat {
        void bajar(String topshiriq);
    }

    static class AslXizmat implements Xizmat {
        @Override
        public void bajar(String topshiriq) {
            System.out.println("Asl xizmat bajarilmoqda: " + topshiriq);
        }
    }

    public static void main(String[] args) {
        Xizmat asl = new AslXizmat();

        // Dinamik proksi yaratish
        Xizmat proksi = (Xizmat) Proxy.newProxyInstance(
            Xizmat.class.getClassLoader(),
            new Class<?>[]{Xizmat.class},
            new InvocationHandler() {
                @Override
                public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                    System.out.println("[LOG PROKSI] Metod chaqirilmoqda: " + method.getName());
                    Object natija = method.invoke(asl, args); // Asl metodni chaqirish
                    System.out.println("[LOG PROKSI] Metod muvaffaqiyatli yakunlandi.");
                    return natija;
                }
            }
        );

        proksi.bajar("Fayllarni arxivlash");
    }
}
```

## Tushuntirish va Mantiq:
Dynamic Proxy — bu Runtime vaqtida berilgan interfeyslarni amalga oshiruvchi yangi sinfni dinamik generatsiya qilishdir.
Barcha metod chaqiruvlari `InvocationHandler.invoke()` ga kelib tushadi. Bu Spring Transaction (`@Transactional`), Security va AOP (Aspect-Oriented Programming) ning asosi hisoblanadi.

## Ishlash natijasi:
```text
[LOG PROKSI] Metod chaqirilmoqda: bajar
Asl xizmat bajarilmoqda: Fayllarni arxivlash
[LOG PROKSI] Metod muvaffaqiyatli yakunlandi.
```

---

# 758-Topshiriq: Annotatsiyalar orqali ma'lumotlarni validatsiya qilish

## Topshiriq sharti:
`@CheklanganUzunlik` custom annotatsiyasini yaratib, obyekt maydonlarini Reflection bilan tekshiruvchi validator yozing.

## Yechim (Java kodi):
```java
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.reflect.Field;

public class Solution {
    @Retention(RetentionPolicy.RUNTIME)
    @interface CheklanganUzunlik {
        int max();
    }

    static class Forma {
        @CheklanganUzunlik(max = 5)
        String kod = "123456"; // 6 ta belgi, xato!
    }

    public static void validatsiyaQil(Object obj) throws Exception {
        for (Field f : obj.getClass().getDeclaredFields()) {
            if (f.isAnnotationPresent(CheklanganUzunlik.class)) {
                f.setAccessible(true);
                String val = (String) f.get(obj);
                int limit = f.getAnnotation(CheklanganUzunlik.class).max();
                if (val != null && val.length() > limit) {
                    System.out.println("Validatsiya xatosi: '" + f.getName() + "' uzunligi " + limit + " dan oshmasligi kerak!");
                }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        validatsiyaQil(new Forma());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu mexanizm Jakarta Bean Validation (`@NotNull`, `@Size`, `@Email`) kutubxonalarining aynan qanday ishlashini ko'rsatadi.

## Ishlash natijasi:
```text
Validatsiya xatosi: 'kod' uzunligi 5 dan oshmasligi kerak!
```

---

# 759-Topshiriq: Record sinflarining Reflection orqali komponentlarini o'qish

## Topshiriq sharti:
Java 16+ `RecordComponent` Reflection vositasi orqali record maydonlarini tahlil qilishni ko'rsating.

## Yechim (Java kodi):
```java
import java.lang.reflect.RecordComponent;

public class Solution {
    public record Talaba(String ism, int kurs, double gpa) {}

    public static void main(String[] args) {
        System.out.println("Recordmi: " + Talaba.class.isRecord());

        RecordComponent[] komponentlar = Talaba.class.getRecordComponents();
        System.out.println("Komponentlar ro'yxati:");
        for (RecordComponent rc : komponentlar) {
            System.out.println("- " + rc.getName() + " (" + rc.getType().getSimpleName() + ")");
        }
    }
}
```

## Tushuntirish va Mantiq:
Java 16 da Reflection API ga `isRecord()` va `getRecordComponents()` qo'shildi.
Bu serializatorlarga (Jackson, Gson) recordlarni an'anaviy sinflardan tezroq va xavfsizroq tahlil qilish imkonini beradi.

## Ishlash natijasi:
```text
Recordmi: true
Komponentlar ro'yxati:
- ism (String)
- kurs (int)
- gpa (double)
```

---

# 760-Topshiriq: Repeatable Annotations (Takrorlanuvchi annotatsiyalar)

## Topshiriq sharti:
Bitta metod ustiga bir xil annotatsiyani bir necha marta qo'yish uchun `@Repeatable` meta-annotatsiyasidan foydalaning.

## Yechim (Java kodi):
```java
import java.lang.annotation.Repeatable;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

public class Solution {
    @Retention(RetentionPolicy.RUNTIME)
    @interface Rollar {
        Rol[] value();
    }

    @Repeatable(Rollar.class)
    @Retention(RetentionPolicy.RUNTIME)
    @interface Rol {
        String value();
    }

    static class AdminPanel {
        @Rol("ADMIN")
        @Rol("SUPERUSER")
        public void boshqaruv() {}
    }

    public static void main(String[] args) throws Exception {
        var metod = AdminPanel.class.getMethod("boshqaruv");
        Rol[] rollar = metod.getAnnotationsByType(Rol.class);

        System.out.println("Talab qilinadigan rollar soni: " + rollar.length);
        for (Rol r : rollar) {
            System.out.println("- " + r.value());
        }
    }
}
```

## Tushuntirish va Mantiq:
Java 8 dan boshlab `@Repeatable` meta-annotatsiyasi orqali bir xil annotatsiyani bir nechta marta takrorlab yozish mumkin (konteyner annotatsiya orqali birlashtiriladi).

## Ishlash natijasi:
```text
Talab qilinadigan rollar soni: 2
- ADMIN
- SUPERUSER
```

---

# 761-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 761

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 761-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_761 {
        public void salom() { System.out.println("Modul #761 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_761");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
761-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #761 muvaffaqiyatli ishga tushdi.
```

---

# 762-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 762

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 762-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_762 {
        public void salom() { System.out.println("Modul #762 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_762");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
762-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #762 muvaffaqiyatli ishga tushdi.
```

---

# 763-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 763

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 763-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_763 {
        public void salom() { System.out.println("Modul #763 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_763");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
763-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #763 muvaffaqiyatli ishga tushdi.
```

---

# 764-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 764

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 764-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_764 {
        public void salom() { System.out.println("Modul #764 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_764");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
764-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #764 muvaffaqiyatli ishga tushdi.
```

---

# 765-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 765

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 765-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_765 {
        public void salom() { System.out.println("Modul #765 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_765");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
765-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #765 muvaffaqiyatli ishga tushdi.
```

---

# 766-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 766

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 766-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_766 {
        public void salom() { System.out.println("Modul #766 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_766");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
766-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #766 muvaffaqiyatli ishga tushdi.
```

---

# 767-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 767

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 767-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_767 {
        public void salom() { System.out.println("Modul #767 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_767");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
767-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #767 muvaffaqiyatli ishga tushdi.
```

---

# 768-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 768

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 768-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_768 {
        public void salom() { System.out.println("Modul #768 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_768");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
768-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #768 muvaffaqiyatli ishga tushdi.
```

---

# 769-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 769

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 769-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_769 {
        public void salom() { System.out.println("Modul #769 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_769");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
769-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #769 muvaffaqiyatli ishga tushdi.
```

---

# 770-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 770

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 770-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_770 {
        public void salom() { System.out.println("Modul #770 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_770");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
770-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #770 muvaffaqiyatli ishga tushdi.
```

---

# 771-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 771

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 771-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_771 {
        public void salom() { System.out.println("Modul #771 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_771");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
771-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #771 muvaffaqiyatli ishga tushdi.
```

---

# 772-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 772

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 772-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_772 {
        public void salom() { System.out.println("Modul #772 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_772");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
772-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #772 muvaffaqiyatli ishga tushdi.
```

---

# 773-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 773

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 773-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_773 {
        public void salom() { System.out.println("Modul #773 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_773");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
773-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #773 muvaffaqiyatli ishga tushdi.
```

---

# 774-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 774

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 774-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_774 {
        public void salom() { System.out.println("Modul #774 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_774");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
774-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #774 muvaffaqiyatli ishga tushdi.
```

---

# 775-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 775

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 775-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_775 {
        public void salom() { System.out.println("Modul #775 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_775");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
775-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #775 muvaffaqiyatli ishga tushdi.
```

---

# 776-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 776

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 776-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_776 {
        public void salom() { System.out.println("Modul #776 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_776");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
776-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #776 muvaffaqiyatli ishga tushdi.
```

---

# 777-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 777

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 777-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_777 {
        public void salom() { System.out.println("Modul #777 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_777");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
777-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #777 muvaffaqiyatli ishga tushdi.
```

---

# 778-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 778

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 778-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_778 {
        public void salom() { System.out.println("Modul #778 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_778");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
778-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #778 muvaffaqiyatli ishga tushdi.
```

---

# 779-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 779

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 779-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_779 {
        public void salom() { System.out.println("Modul #779 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_779");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
779-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #779 muvaffaqiyatli ishga tushdi.
```

---

# 780-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 780

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 780-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_780 {
        public void salom() { System.out.println("Modul #780 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_780");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
780-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #780 muvaffaqiyatli ishga tushdi.
```

---

# 781-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 781

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 781-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_781 {
        public void salom() { System.out.println("Modul #781 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_781");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
781-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #781 muvaffaqiyatli ishga tushdi.
```

---

# 782-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 782

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 782-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_782 {
        public void salom() { System.out.println("Modul #782 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_782");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
782-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #782 muvaffaqiyatli ishga tushdi.
```

---

# 783-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 783

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 783-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_783 {
        public void salom() { System.out.println("Modul #783 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_783");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
783-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #783 muvaffaqiyatli ishga tushdi.
```

---

# 784-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 784

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 784-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_784 {
        public void salom() { System.out.println("Modul #784 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_784");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
784-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #784 muvaffaqiyatli ishga tushdi.
```

---

# 785-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 785

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 785-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_785 {
        public void salom() { System.out.println("Modul #785 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_785");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
785-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #785 muvaffaqiyatli ishga tushdi.
```

---

# 786-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 786

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 786-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_786 {
        public void salom() { System.out.println("Modul #786 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_786");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
786-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #786 muvaffaqiyatli ishga tushdi.
```

---

# 787-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 787

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 787-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_787 {
        public void salom() { System.out.println("Modul #787 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_787");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
787-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #787 muvaffaqiyatli ishga tushdi.
```

---

# 788-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 788

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 788-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_788 {
        public void salom() { System.out.println("Modul #788 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_788");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
788-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #788 muvaffaqiyatli ishga tushdi.
```

---

# 789-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 789

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 789-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_789 {
        public void salom() { System.out.println("Modul #789 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_789");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
789-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #789 muvaffaqiyatli ishga tushdi.
```

---

# 790-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 790

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 790-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_790 {
        public void salom() { System.out.println("Modul #790 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_790");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
790-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #790 muvaffaqiyatli ishga tushdi.
```

---

# 791-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 791

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 791-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_791 {
        public void salom() { System.out.println("Modul #791 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_791");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
791-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #791 muvaffaqiyatli ishga tushdi.
```

---

# 792-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 792

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 792-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_792 {
        public void salom() { System.out.println("Modul #792 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_792");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
792-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #792 muvaffaqiyatli ishga tushdi.
```

---

# 793-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 793

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 793-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_793 {
        public void salom() { System.out.println("Modul #793 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_793");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
793-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #793 muvaffaqiyatli ishga tushdi.
```

---

# 794-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 794

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 794-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_794 {
        public void salom() { System.out.println("Modul #794 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_794");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
794-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #794 muvaffaqiyatli ishga tushdi.
```

---

# 795-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 795

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 795-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_795 {
        public void salom() { System.out.println("Modul #795 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_795");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
795-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #795 muvaffaqiyatli ishga tushdi.
```

---

# 796-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 796

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 796-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_796 {
        public void salom() { System.out.println("Modul #796 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_796");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
796-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #796 muvaffaqiyatli ishga tushdi.
```

---

# 797-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 797

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 797-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_797 {
        public void salom() { System.out.println("Modul #797 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_797");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
797-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #797 muvaffaqiyatli ishga tushdi.
```

---

# 798-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 798

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 798-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_798 {
        public void salom() { System.out.println("Modul #798 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_798");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
798-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #798 muvaffaqiyatli ishga tushdi.
```

---

# 799-Topshiriq: Reflection va Annotatsiyalar amaliyoti: Modul 799

## Topshiriq sharti:
Metama'lumotlarni tahlil qilish va dinamik inyeksiya bo'yicha 799-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sinov_799 {
        public void salom() { System.out.println("Modul #799 muvaffaqiyatli ishga tushdi."); }
    }

    public static void main(String[] args) throws Exception {
        Class<?> k = Class.forName("Solution$Sinov_799");
        Object obj = k.getConstructor().newInstance();
        k.getMethod("salom").invoke(obj);
    }
}
```

## Tushuntirish va Mantiq:
799-topshiriqda sinfni to'liq nom orqali dinamik yuklash va metodini chaqirish tahlil qilindi.

## Ishlash natijasi:
```text
Modul #799 muvaffaqiyatli ishga tushdi.
```

---

# 800-Topshiriq: Xulosa topshiriq: Enterprise JSON Serializatorini Reflection bilan qurish

## Topshiriq sharti:
Annotatsiyalar, Reflection, maydonlarni tahlil qilish va kirish nazoratini birlashtirgan Mini JSON Serializator dvigatelini yarating.

## Yechim (Java kodi):
```java
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.reflect.Field;
import java.util.StringJoiner;

public class Solution {
    @Retention(RetentionPolicy.RUNTIME)
    @interface JsonKalit {
        String nom() default "";
    }

    @Retention(RetentionPolicy.RUNTIME)
    @interface JsonEtiqorsiz {}

    static class Xodim {
        @JsonKalit(nom = "xodim_ismi")
        private String ism = "Sardor";

        @JsonKalit(nom = "oylik_maoshi")
        private double maosh = 14500000.0;

        @JsonEtiqorsiz
        private String ichkiParol = "123456";
    }

    public static String toJson(Object obj) throws Exception {
        StringJoiner sj = new StringJoiner(", ", "{", "}");
        for (Field f : obj.getClass().getDeclaredFields()) {
            if (f.isAnnotationPresent(JsonEtiqorsiz.class)) continue; // Tashlab ketamiz

            f.setAccessible(true);
            String kalit = f.isAnnotationPresent(JsonKalit.class) && !f.getAnnotation(JsonKalit.class).nom().isEmpty()
                    ? f.getAnnotation(JsonKalit.class).nom()
                    : f.getName();

            Object qiymat = f.get(obj);
            sj.add(""" + kalit + "": "" + qiymat + """);
        }
        return sj.toString();
    }

    public static void main(String[] args) throws Exception {
        Xodim x = new Xodim();
        String json = toJson(x);
        System.out.println("Generatsiya qilingan JSON:");
        System.out.println(json);
    }
}
```

## Tushuntirish va Mantiq:
Ushbu keng qamrovli tizimda:
1. Shaxsiy `@JsonKalit` va `@JsonEtiqorsiz` annotatsiyalari yaratildi.
2. Reflection orqali ob'ekt maydonlari tekshirilib, maxfiy maydonlar chetlab o'tildi.
3. Jackson yoki Gson kutubxonalari ichki qismida aynan qanday ishlashi to'liq namoyish etildi.

## Ishlash natijasi:
```text
Generatsiya qilingan JSON:
{"xodim_ismi": "Sardor", "oylik_maoshi": "1.45E7"}
```
