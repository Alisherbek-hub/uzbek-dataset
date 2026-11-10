# Java OOP: Merosxo'rlik va Polimorfizm (251-300)

# 251-Topshiriq: Merosxo'rlik (Inheritance) asoslari: extends kalit so'zi

## Topshiriq sharti:
Umumiy `Xodim` ota sinfidan `Dasturchi` bola sinfini `extends` orqali meros olib yarating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xodim {
        String ism;
        double maosh;

        public void ishla() {
            System.out.println(ism + " o'z vazifalarini bajarmoqda.");
        }
    }

    static class Dasturchi extends Xodim {
        String asosiyTil;

        public void kodYoz() {
            System.out.println(ism + " " + asosiyTil + " tilida toza kod yozmoqda.");
        }
    }

    public static void main(String[] args) {
        Dasturchi d = new Dasturchi();
        d.ism = "Farhod";
        d.maosh = 15000000.0;
        d.asosiyTil = "Java";

        d.ishla();   // Ota sinfdan meros olingan metod
        d.kodYoz();  // Bola sinfning o'ziga xos metodi
    }
}
```

## Tushuntirish va Mantiq:
Merosxo'rlik (Inheritance) kodni qayta ishlatish (code reuse) va "IS-A" (Dasturchi bu Xodimdir) munosabatini o'rnatish imkonini beradi.
`extends` kalit so'zi orqali bola sinf ota sinfning barcha ochiq (`public`, `protected`, `package-private`) maydonlari va metodlariga ega bo'ladi. Java-da har bir sinf faqat bitta sinfdan meros olishi mumkin (Single Inheritance).

## Ishlash natijasi:
```text
Farhod o'z vazifalarini bajarmoqda.
Farhod Java tilida toza kod yozmoqda.
```

---

# 252-Topshiriq: super kalit so'zi: Ota sinf konstruktorini chaqirish

## Topshiriq sharti:
Bola sinf konstruktori ota sinf konstruktorini `super(...)` orqali chaqirish tartibini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    static class Avto {
        private final String brend;

        public Avto(String brend) {
            this.brend = brend;
            System.out.println("1. Ota sinf (Avto) konstruktori ishga tushdi: " + brend);
        }

        public String getBrend() { return brend; }
    }

    static class ElektroAvto extends Avto {
        private final int batareyaHajmiKwh;

        public ElektroAvto(String brend, int batareya) {
            super(brend); // Ota konstruktorni birinchi bo'lib chaqiramiz
            this.batareyaHajmiKwh = batareya;
            System.out.println("2. Bola sinf (ElektroAvto) konstruktori ishga tushdi: " + batareya + " kWh");
        }
    }

    public static void main(String[] args) {
        new ElektroAvto("BYD Song Plus", 87);
    }
}
```

## Tushuntirish va Mantiq:
Bola sinf obyektini yaratishdan oldin uning ota sinfi xotirada to'liq initsializatsiya bo'lishi shart.
Shu sababli `super(...)` chaqiruvi bola sinf konstruktorining birinchi qatorida turishi lozim. Agar qo'lda yozilmasa, kompilyator yashirin ravishda `super()` ni chaqiradi.

## Ishlash natijasi:
```text
1. Ota sinf (Avto) konstruktori ishga tushdi: BYD Song Plus
2. Bola sinf (ElektroAvto) konstruktori ishga tushdi: 87 kWh
```

---

# 253-Topshiriq: Metodlarni qayta aniqlash (Method Overriding) va @Override annotatsiyasi

## Topshiriq sharti:
Ota sinfdagi metodni bola sinfda qayta belgilash va `@Override` annotatsiyasining kompilyatsiyadagi rolini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Hayvon {
        public void ovozChiqar() {
            System.out.println("Hayvon noma'lum ovoz chiqarmoqda");
        }
    }

    static class Kuchuk extends Hayvon {
        @Override
        public void ovozChiqar() {
            System.out.println("Vov-vov!");
        }
    }

    static class Mushuk extends Hayvon {
        @Override
        public void ovozChiqar() {
            System.out.println("Miyov-miyov!");
        }
    }

    public static void main(String[] args) {
        Hayvon h1 = new Kuchuk();
        Hayvon h2 = new Mushuk();

        h1.ovozChiqar();
        h2.ovozChiqar();
    }
}
```

## Tushuntirish va Mantiq:
Method Overriding — bola sinfda ota sinf bilan ayni bir xil signaturaga (nom va parametrlar) ega yangi metod yozishdir.
`@Override` annotatsiyasi kompilyatorga ushbu metod ota sinfdagi metodni aniq almashtirayotganini tekshirishni buyuradi. Agar nomida yoki parametrlarida imlo xatosi bo'lsa, kompilyator darhol xato beradi.

## Ishlash natijasi:
```text
Vov-vov!
Miyov-miyov!
```

---

# 254-Topshiriq: Polimorfizm: Dynamic Method Dispatch (Dinamik metod bog'lanishi)

## Topshiriq sharti:
Ota sinf interfeysi orqali bola sinflarning turli xulq-atvorini runtime da chaqirish mexanizmini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Shakl {
        public double yuza() { return 0.0; }
    }

    static class Doira extends Shakl {
        private final double r;
        public Doira(double r) { this.r = r; }
        @Override
        public double yuza() { return Math.PI * r * r; }
    }

    static class Tortburchak extends Shakl {
        private final double a, b;
        public Tortburchak(double a, double b) { this.a = a; this.b = b; }
        @Override
        public double yuza() { return a * b; }
    }

    public static void main(String[] args) {
        Shakl[] shakllar = {
            new Doira(10),
            new Tortburchak(4, 5)
        };

        for (Shakl s : shakllar) {
            System.out.printf("Shakl yuzi: %.2f
", s.yuza());
        }
    }
}
```

## Tushuntirish va Mantiq:
Dynamic Method Dispatch (Polimorfizm) — chaqirilayotgan metod qaysi sinfga tegishli ekanligi kompilyatsiya vaqtida emas, balki dastur ishlab turgan paytda (Runtime) da obyektning haqiqiy turiga qarab hal qilinishidir.
Bu kodni kengaytiriluvchan (extensible) va ochiq-yopiq tamoyiliga (OCP) mos qiladi.

## Ishlash natijasi:
```text
Shakl yuzi: 314.16
Shakl yuzi: 20.00
```

---

# 255-Topshiriq: Upcasting va Downcasting: ClassCastException xavfi

## Topshiriq sharti:
Upcasting ning xavfsizligi, downcasting da esa `ClassCastException` ro'y berishi mumkinligini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Ota {}
    static class Bola extends Ota {
        void bolaMetodi() { System.out.println("Bola metod bajarildi"); }
    }

    public static void main(String[] args) {
        // Upcasting (avtomatik, xavfsiz)
        Bola b = new Bola();
        Ota o = b; 

        // Downcasting (aniq kasting talab qiladi)
        Bola qaytganBola = (Bola) o;
        qaytganBola.bolaMetodi();

        // Xato downcasting holati:
        Ota soxtaOta = new Ota();
        try {
            Bola xato = (Bola) soxtaOta; // ClassCastException!
            xato.bolaMetodi();
        } catch (ClassCastException e) {
            System.out.println("Xatolik ushlandi: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
- Upcasting: Bola obyektini Ota turiga ko'rsatish (`Ota o = new Bola()`). Bu har doim xavfsiz va avtomatik.
- Downcasting: Ota ko'rsatkichini Bola turiga qaytarish (`Bola b = (Bola) o`). Agar obyekt xotirada chindan ham `Bola` turida yaratilmagan bo'lsa, JVM `ClassCastException` tashlaydi.

## Ishlash natijasi:
```text
Bola metod bajarildi
Xatolik ushlandi: class Solution$Ota cannot be cast to class Solution$Bola
```

---

# 256-Topshiriq: Java 16+ Pattern Matching for instanceof

## Topshiriq sharti:
Kastingdan oldin `instanceof` bilan xavfsiz tekshirish va Java 16 ning Pattern Matching sintaksisidan foydalanishni namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    static class Transport {}
    static class Poyezd extends Transport {
        int vagonlarSoni = 12;
    }

    public static void tahlil(Transport t) {
        // Java 16+ Pattern Matching
        if (t instanceof Poyezd p) {
            System.out.println("Bu poyezd! Vagonlar soni: " + p.vagonlarSoni);
        } else {
            System.out.println("Bu poyezd emas.");
        }
    }

    public static void main(String[] args) {
        tahlil(new Poyezd());
        tahlil(new Transport());
    }
}
```

## Tushuntirish va Mantiq:
Java 16 dan boshlab `if (t instanceof Poyezd p)` sintaksisi joriy etildi.
U bitta amalda:
1. `t` null emasligini tekshiradi;
2. `t` ning `Poyezd` ekanligini tekshiradi;
3. Shart bajarilsa `p` nomli yangi kasting qilingan lokal o'zgaruvchini ochib beradi.

## Ishlash natijasi:
```text
Bu poyezd! Vagonlar soni: 12
Bu poyezd emas.
```

---

# 257-Topshiriq: Abstrakt sinflar (Abstract Classes) va abstrakt metodlar

## Topshiriq sharti:
`abstract class` yaratib, uning ichida umumiy metodlar va majburiy abstrakt metodlarni e'lon qiling.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class TolovTizimi {
        private final String nom;

        public TolovTizimi(String nom) { this.nom = nom; }

        public void kvitansiyaChopEt(double summa) {
            System.out.println("[" + nom + "] To'lov kvitansiyasi: " + summa + " so'm");
        }

        // Sub-sinflar albatta amalga oshirishi shart bo'lgan metod
        public abstract boolean tolovQil(double summa);
    }

    static class Click extends TolovTizimi {
        public Click() { super("Click"); }

        @Override
        public boolean tolovQil(double summa) {
            System.out.println("Click orqali to'lov amalga oshirildi: " + summa);
            kvitansiyaChopEt(summa);
            return true;
        }
    }

    public static void main(String[] args) {
        TolovTizimi tolov = new Click();
        tolov.tolovQil(75000.0);
    }
}
```

## Tushuntirish va Mantiq:
Abstrakt sinfdan to'g'ridan-to'g'ri `new` qilib obyekt yaratib bo'lmaydi. U faqat meros olish uchun mo'ljallangan.
Abstrakt metodlar (`abstract void foo()`) tanaga ega bo'lmaydi va barcha voris sinflar ularni `@Override` qilishga majburdir.

## Ishlash natijasi:
```text
Click orqali to'lov amalga oshirildi: 75000.0
[Click] To'lov kvitansiyasi: 75000.0 so'm
```

---

# 258-Topshiriq: final sinflar va final metodlar

## Topshiriq sharti:
Sinfni `final` qilish orqali merosxo'rlikni, metodni `final` qilish orqali override ni taqiqlashni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class XavfsizTizim {
        // Bu metodni hech bir sub-sinf o'zgartira olmaydi
        public final void autentifikatsiya() {
            System.out.println("Standart qat'iy xavfsizlik tekshiruvi bajarildi.");
        }
    }

    // final sinf: undan hech kim meros ololmaydi
    static final class BankShifrlagich extends XavfsizTizim {
        public void shifrla(String ma'lumot) {
            System.out.println("Ma'lumot AES-256 bilan shifrlandi.");
        }
    }

    public static void main(String[] args) {
        BankShifrlagich b = new BankShifrlagich();
        b.autentifikatsiya();
        b.shifrla("Maxfiy balans");
    }
}
```

## Tushuntirish va Mantiq:
- `final class`: Hech qaysi sinf bu sinfdan meros ololmaydi (`String`, `Integer` kabi standart sinflar ham final qilingan).
- `final method`: Sub-sinflar bu metodni qayta aniqlay (override qila) olmaydi. Bu xavfsizlik va barqarorlikni ta'minlashda zarurdir.

## Ishlash natijasi:
```text
Standart qat'iy xavfsizlik tekshiruvi bajarildi.
Ma'lumot AES-256 bilan shifrlandi.
```

---

# 259-Topshiriq: Java 17+ Sealed Classes: Merosxo'rlikni aniq nazorat qilish

## Topshiriq sharti:
Java 17 da standartlashgan `sealed`, `permits`, `final` va `non-sealed` sinflar tuzilmasini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    // Faqat Naqd va Karta sinflari meros olishiga ruxsat berilgan
    public abstract static sealed class Tolov permits Naqd, Karta {}

    public static final class Naqd extends Tolov {
        public void naqdBer() { System.out.println("Naqd pul to'landi."); }
    }

    public static non-sealed class Karta extends Tolov {
        public void kartaChiz() { System.out.println("Karta orqali to'landi."); }
    }

    public static void main(String[] args) {
        Tolov t1 = new Naqd();
        Tolov t2 = new Karta();
        System.out.println("Sealed ierarxiya yaratildi: " + t1.getClass().getSimpleName() + ", " + t2.getClass().getSimpleName());
    }
}
```

## Tushuntirish va Mantiq:
Sealed Classes (Muhrlangan sinflar):
Java 17 dan boshlab `sealed` kalit so'zi orqali sinfdan qaysi aniq sinflar meros olishi mumkinligi `permits` bilan qat'iy cheklanadi.
Sub-sinflar quyidagi uchtadan biriga ega bo'lishi shart:
1. `final`: boshqa merosxo'r bo'lmaydi.
2. `sealed`: yana o'z vorislarini cheklaydi.
3. `non-sealed`: ochiq vorislikka ruxsat beradi.

## Ishlash natijasi:
```text
Sealed ierarxiya yaratildi: Naqd, Karta
```

---

# 260-Topshiriq: Composition over Inheritance tamoyili

## Topshiriq sharti:
Nima sababdan ko'p qavatli merosxo'rlik o'rniga obyektlarni kompozitsiya (Composition) orqali birlashtirish afzal ekanligini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class XabarYuboruvchi {
        public void yubor(String xabar) {
            System.out.println("Xabar: " + xabar);
        }
    }

    // Merosxo'rlik o'rniga kompozitsiya qo'llanilgan sinf
    static class BuyurtmaXizmati {
        private final XabarYuboruvchi xabarYuboruvchi; // Kompozitsiya

        public BuyurtmaXizmati(XabarYuboruvchi x) {
            this.xabarYuboruvchi = x;
        }

        public void buyurtmaBer(String mahsulot) {
            System.out.println("Buyurtma qabul qilindi: " + mahsulot);
            xabarYuboruvchi.yubor(mahsulot + " uchun buyurtma rasmiylashtirildi!");
        }
    }

    public static void main(String[] args) {
        XabarYuboruvchi xabar = new XabarYuboruvchi();
        BuyurtmaXizmati xizmat = new BuyurtmaXizmati(xabar);
        xizmat.buyurtmaBer("Kitob");
    }
}
```

## Tushuntirish va Mantiq:
Composition over Inheritance (Merosxo'rlikdan ko'ra Kompozitsiyani afzal bilish) dasturiy arxitekturaning eng muhim qoidalaridan biridir.
Merosxo'rlik ota va bola sinflarni qattiq bog'lab (tight coupling) qo'yadi va inkapsulyatsiyani buzadi.
Kompozitsiya esa bo'sh bog'lanish (loose coupling) ta'minlaydi va obyekt xulq-atvorini runtime da almashtirish imkonini beradi.

## Ishlash natijasi:
```text
Buyurtma qabul qilindi: Kitob
Xabar: Kitob uchun buyurtma rasmiylashtirildi!
```

---

# 261-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 261

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 261-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_261 {
        protected final String nom;
        public Baza_261(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_261 extends Baza_261 {
        public Voris_261() { super("Modul_261"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_261 obj = new Voris_261();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_261 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 262-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 262

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 262-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_262 {
        protected final String nom;
        public Baza_262(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_262 extends Baza_262 {
        public Voris_262() { super("Modul_262"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_262 obj = new Voris_262();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_262 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 263-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 263

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 263-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_263 {
        protected final String nom;
        public Baza_263(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_263 extends Baza_263 {
        public Voris_263() { super("Modul_263"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_263 obj = new Voris_263();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_263 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 264-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 264

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 264-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_264 {
        protected final String nom;
        public Baza_264(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_264 extends Baza_264 {
        public Voris_264() { super("Modul_264"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_264 obj = new Voris_264();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_264 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 265-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 265

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 265-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_265 {
        protected final String nom;
        public Baza_265(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_265 extends Baza_265 {
        public Voris_265() { super("Modul_265"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_265 obj = new Voris_265();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_265 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 266-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 266

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 266-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_266 {
        protected final String nom;
        public Baza_266(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_266 extends Baza_266 {
        public Voris_266() { super("Modul_266"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_266 obj = new Voris_266();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_266 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 267-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 267

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 267-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_267 {
        protected final String nom;
        public Baza_267(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_267 extends Baza_267 {
        public Voris_267() { super("Modul_267"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_267 obj = new Voris_267();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_267 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 268-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 268

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 268-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_268 {
        protected final String nom;
        public Baza_268(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_268 extends Baza_268 {
        public Voris_268() { super("Modul_268"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_268 obj = new Voris_268();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_268 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 269-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 269

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 269-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_269 {
        protected final String nom;
        public Baza_269(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_269 extends Baza_269 {
        public Voris_269() { super("Modul_269"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_269 obj = new Voris_269();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_269 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 270-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 270

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 270-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_270 {
        protected final String nom;
        public Baza_270(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_270 extends Baza_270 {
        public Voris_270() { super("Modul_270"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_270 obj = new Voris_270();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_270 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 271-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 271

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 271-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_271 {
        protected final String nom;
        public Baza_271(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_271 extends Baza_271 {
        public Voris_271() { super("Modul_271"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_271 obj = new Voris_271();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_271 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 272-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 272

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 272-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_272 {
        protected final String nom;
        public Baza_272(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_272 extends Baza_272 {
        public Voris_272() { super("Modul_272"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_272 obj = new Voris_272();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_272 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 273-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 273

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 273-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_273 {
        protected final String nom;
        public Baza_273(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_273 extends Baza_273 {
        public Voris_273() { super("Modul_273"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_273 obj = new Voris_273();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_273 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 274-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 274

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 274-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_274 {
        protected final String nom;
        public Baza_274(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_274 extends Baza_274 {
        public Voris_274() { super("Modul_274"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_274 obj = new Voris_274();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_274 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 275-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 275

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 275-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_275 {
        protected final String nom;
        public Baza_275(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_275 extends Baza_275 {
        public Voris_275() { super("Modul_275"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_275 obj = new Voris_275();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_275 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 276-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 276

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 276-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_276 {
        protected final String nom;
        public Baza_276(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_276 extends Baza_276 {
        public Voris_276() { super("Modul_276"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_276 obj = new Voris_276();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_276 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 277-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 277

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 277-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_277 {
        protected final String nom;
        public Baza_277(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_277 extends Baza_277 {
        public Voris_277() { super("Modul_277"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_277 obj = new Voris_277();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_277 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 278-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 278

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 278-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_278 {
        protected final String nom;
        public Baza_278(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_278 extends Baza_278 {
        public Voris_278() { super("Modul_278"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_278 obj = new Voris_278();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_278 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 279-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 279

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 279-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_279 {
        protected final String nom;
        public Baza_279(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_279 extends Baza_279 {
        public Voris_279() { super("Modul_279"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_279 obj = new Voris_279();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_279 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 280-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 280

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 280-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_280 {
        protected final String nom;
        public Baza_280(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_280 extends Baza_280 {
        public Voris_280() { super("Modul_280"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_280 obj = new Voris_280();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_280 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 281-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 281

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 281-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_281 {
        protected final String nom;
        public Baza_281(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_281 extends Baza_281 {
        public Voris_281() { super("Modul_281"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_281 obj = new Voris_281();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_281 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 282-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 282

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 282-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_282 {
        protected final String nom;
        public Baza_282(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_282 extends Baza_282 {
        public Voris_282() { super("Modul_282"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_282 obj = new Voris_282();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_282 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 283-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 283

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 283-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_283 {
        protected final String nom;
        public Baza_283(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_283 extends Baza_283 {
        public Voris_283() { super("Modul_283"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_283 obj = new Voris_283();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_283 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 284-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 284

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 284-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_284 {
        protected final String nom;
        public Baza_284(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_284 extends Baza_284 {
        public Voris_284() { super("Modul_284"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_284 obj = new Voris_284();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_284 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 285-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 285

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 285-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_285 {
        protected final String nom;
        public Baza_285(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_285 extends Baza_285 {
        public Voris_285() { super("Modul_285"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_285 obj = new Voris_285();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_285 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 286-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 286

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 286-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_286 {
        protected final String nom;
        public Baza_286(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_286 extends Baza_286 {
        public Voris_286() { super("Modul_286"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_286 obj = new Voris_286();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_286 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 287-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 287

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 287-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_287 {
        protected final String nom;
        public Baza_287(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_287 extends Baza_287 {
        public Voris_287() { super("Modul_287"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_287 obj = new Voris_287();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_287 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 288-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 288

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 288-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_288 {
        protected final String nom;
        public Baza_288(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_288 extends Baza_288 {
        public Voris_288() { super("Modul_288"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_288 obj = new Voris_288();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_288 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 289-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 289

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 289-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_289 {
        protected final String nom;
        public Baza_289(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_289 extends Baza_289 {
        public Voris_289() { super("Modul_289"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_289 obj = new Voris_289();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_289 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 290-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 290

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 290-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_290 {
        protected final String nom;
        public Baza_290(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_290 extends Baza_290 {
        public Voris_290() { super("Modul_290"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_290 obj = new Voris_290();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_290 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 291-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 291

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 291-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_291 {
        protected final String nom;
        public Baza_291(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_291 extends Baza_291 {
        public Voris_291() { super("Modul_291"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_291 obj = new Voris_291();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_291 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 292-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 292

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 292-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_292 {
        protected final String nom;
        public Baza_292(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_292 extends Baza_292 {
        public Voris_292() { super("Modul_292"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_292 obj = new Voris_292();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_292 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 293-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 293

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 293-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_293 {
        protected final String nom;
        public Baza_293(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_293 extends Baza_293 {
        public Voris_293() { super("Modul_293"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_293 obj = new Voris_293();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_293 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 294-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 294

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 294-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_294 {
        protected final String nom;
        public Baza_294(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_294 extends Baza_294 {
        public Voris_294() { super("Modul_294"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_294 obj = new Voris_294();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_294 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 295-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 295

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 295-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_295 {
        protected final String nom;
        public Baza_295(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_295 extends Baza_295 {
        public Voris_295() { super("Modul_295"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_295 obj = new Voris_295();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_295 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 296-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 296

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 296-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_296 {
        protected final String nom;
        public Baza_296(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_296 extends Baza_296 {
        public Voris_296() { super("Modul_296"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_296 obj = new Voris_296();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_296 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 297-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 297

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 297-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_297 {
        protected final String nom;
        public Baza_297(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_297 extends Baza_297 {
        public Voris_297() { super("Modul_297"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_297 obj = new Voris_297();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_297 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 298-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 298

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 298-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_298 {
        protected final String nom;
        public Baza_298(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_298 extends Baza_298 {
        public Voris_298() { super("Modul_298"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_298 obj = new Voris_298();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_298 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 299-Topshiriq: Merosxo'rlik va Polimorfizm arxitekturasi: Modul 299

## Topshiriq sharti:
Polimorfizm, abstrakt sinflar va metodlarni qayta aniqlash bo'yicha 299-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static abstract class Baza_299 {
        protected final String nom;
        public Baza_299(String nom) { this.nom = nom; }
        public abstract void bajar();
    }

    static class Voris_299 extends Baza_299 {
        public Voris_299() { super("Modul_299"); }
        @Override
        public void bajar() {
            System.out.println(nom + " polimorfik amali muvaffaqiyatli bajarildi.");
        }
    }

    public static void main(String[] args) {
        Baza_299 obj = new Voris_299();
        obj.bajar();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda ota sinfning abstrakt interfeysi va bola sinfning uni o'ziga xos tarzda amalga oshirishi tahlil qilindi.
`super` chaqiruvi orqali ota sinf maydonlari xavfsiz initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Modul_299 polimorfik amali muvaffaqiyatli bajarildi.
```

---

# 300-Topshiriq: Xulosa topshiriq: Bank xizmatlari polimorfik ekotizimi

## Topshiriq sharti:
Merosxo'rlik, polimorfizm, abstrakt sinflar, upcasting va sealed sinflarni birlashtirgan Bank hisob-kitoblari arxitekturasini yarating.

## Yechim (Java kodi):
```java
public class Solution {
    public abstract static sealed class BankHisob permits JamgarmaHisob, KreditHisob {
        private final String hisobRaqam;
        protected double balans;

        public BankHisob(String hisobRaqam, double balans) {
            this.hisobRaqam = hisobRaqam;
            this.balans = balans;
        }

        public abstract void oylikXizmatKorsatish();

        public void depozit(double summa) { this.balans += summa; }
        public double getBalans() { return balans; }
        public String getHisobRaqam() { return hisobRaqam; }
    }

    public static final class JamgarmaHisob extends BankHisob {
        private final double foizStavkasi; // Yillik foiz

        public JamgarmaHisob(String hisobRaqam, double balans, double foiz) {
            super(hisobRaqam, balans);
            this.foizStavkasi = foiz;
        }

        @Override
        public void oylikXizmatKorsatish() {
            double oylikDaromad = (balans * (foizStavkasi / 100)) / 12;
            balans += oylikDaromad;
            System.out.printf("Jamg'arma [%s]: +%.2f so'm foiz qo'shildi. Yangi balans: %.2f so'm
", getHisobRaqam(), oylikDaromad, balans);
        }
    }

    public static final class KreditHisob extends BankHisob {
        private final double xizmatHaqi;

        public KreditHisob(String hisobRaqam, double balans, double xizmatHaqi) {
            super(hisobRaqam, balans);
            this.xizmatHaqi = xizmatHaqi;
        }

        @Override
        public void oylikXizmatKorsatish() {
            balans -= xizmatHaqi;
            System.out.printf("Kredit [%s]: -%.2f so'm xizmat haqi yechildi. Yangi balans: %.2f so'm
", getHisobRaqam(), xizmatHaqi, balans);
        }
    }

    public static void main(String[] args) {
        BankHisob[] hisoblar = {
            new JamgarmaHisob("JH-001", 10000000.0, 18.0),
            new KreditHisob("KH-002", 5000000.0, 50000.0)
        };

        System.out.println("=== OYLIK BANK AMALLARI ISHGA TUSHDI ===");
        for (BankHisob h : hisoblar) {
            h.oylikXizmatKorsatish(); // Polimorfik chaqiruv
        }
    }
}
```

## Tushuntirish va Mantiq:
Ushbu xulosa loyihasida:
1. `sealed class BankHisob` orqali ruxsat etilgan bank hisoblari doirasi cheklandi.
2. Abstrakt `oylikXizmatKorsatish()` metodi har bir hisob turida o'ziga xos tarzda (Jamg'armada foiz qo'shish, Kreditda to'lov yechish) polimorfik amalga oshirildi.
3. Bitta polimorfik massiv (`BankHisob[]`) orqali har xil xatti-harakatga ega obyektlar bir xil chaqiruv bilan boshqarildi.

## Ishlash natijasi:
```text
=== OYLIK BANK AMALLARI ISHGA TUSHDI ===
Jamg'arma [JH-001]: +150000.00 so'm foiz qo'shildi. Yangi balans: 10150000.00 so'm
Kredit [KH-002]: -50000.00 so'm xizmat haqi yechildi. Yangi balans: 4950000.00 so'm
```
