# Java OOP: Sinflar va Obyektlar (201-250)

# 201-Topshiriq: Sinf va Obyekt: new operatori va Heap xotirada joy ajratilishi

## Topshiriq sharti:
Oddiy `Avtomobil` sinfini e'lon qilib, `new` operatori orqali ikkita mustaqil obyekt yarating va ularning maydonlarini to'ldiring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Avtomobil {
        String model;
        String rang;
        int ishlabChiqarilganYil;
    }

    public static void main(String[] args) {
        Avtomobil avto1 = new Avtomobil();
        avto1.model = "Cobalt";
        avto1.rang = "Oq";
        avto1.ishlabChiqarilganYil = 2023;

        Avtomobil avto2 = new Avtomobil();
        avto2.model = "Malibu";
        avto2.rang = "Qora";
        avto2.ishlabChiqarilganYil = 2024;

        System.out.println("1-avto: " + avto1.model + " (" + avto1.rang + ", " + avto1.ishlabChiqarilganYil + ")");
        System.out.println("2-avto: " + avto2.model + " (" + avto2.rang + ", " + avto2.ishlabChiqarilganYil + ")");
    }
}
```

## Tushuntirish va Mantiq:
Sinf (Class) — bu obyektning chizmasi (qolipi).
Obyekt (Instance) — bu Heap xotirada shu qolip asosida yaratilgan haqiqiy tirik namunadir.
`new Avtomobil()` buyrug'i berilganda:
1. JVM Heap xotiradan kerakli hajmda xotira bloki ajratadi.
2. Barcha maydonlarni sukut bo'yicha nol/null bilan to'ldiradi.
3. Konstruktorni ishga tushiradi.
4. Xotira manzilini Stack dagi `avto1` o'zgaruvchisiga qaytaradi.

## Ishlash natijasi:
```text
1-avto: Cobalt (Oq, 2023)
2-avto: Malibu (Qora, 2024)
```

---

# 202-Topshiriq: Default konstruktor vs Parametrli konstruktor

## Topshiriq sharti:
Agar parametrli konstruktor yozilsa, standart parametrlariz konstruktor yo'qolib qolishini va uni qayta yozish zaruratini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Kitob {
        String nom;
        double narx;

        // Parametrli konstruktor
        public Kitob(String nom, double narx) {
            this.nom = nom;
            this.narx = narx;
        }

        // Standart parametrlariz konstruktorni ham saqlab qolish
        public Kitob() {
            this.nom = "Noma'lum kitob";
            this.narx = 0.0;
        }
    }

    public static void main(String[] args) {
        Kitob k1 = new Kitob("O'tkan kunlar", 45000.0);
        Kitob k2 = new Kitob();

        System.out.println("k1: " + k1.nom + " - " + k1.narx + " so'm");
        System.out.println("k2: " + k2.nom + " - " + k2.narx + " so'm");
    }
}
```

## Tushuntirish va Mantiq:
Agar sinfda hech qanday konstruktor yozilmasa, Java kompilyatori o'zi avtomatik bo'sh default konstruktor (`Kitob() {}`) qo'shadi.
Ammo kamida bitta parametrli konstruktor yozilishi bilanoq, avtomatik konstruktor bekor qilinadi.
Agar parametrlariz obyekt yaratish kerak bo'lsa, `Kitob() {}` konstruktorini qo'lda yozish shart.

## Ishlash natijasi:
```text
k1: O'tkan kunlar - 45000.0 so'm
k2: Noma'lum kitob - 0.0 so'm
```

---

# 203-Topshiriq: this kalit so'zi va Shadowing muammosi

## Topshiriq sharti:
Konstruktor parametrlarining sinf maydonlari nomlari bilan bir xil bo'lishi va `this` orqali ularni to'g'ri initsializatsiya qilishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Mahsulot {
        private String nom;
        private double narx;

        public Mahsulot(String nom, double narx) {
            this.nom = nom;   // this.nom - obyekt maydoni, nom - lokal parametr
            this.narx = narx;
        }

        public void malumot() {
            System.out.println("Mahsulot: " + this.nom + ", Narxi: " + this.narx);
        }
    }

    public static void main(String[] args) {
        Mahsulot m = new Mahsulot("Noutbuk", 8500000.0);
        m.malumot();
    }
}
```

## Tushuntirish va Mantiq:
`this` kalit so'zi joriy chaqirilayotgan obyekt nusxasining xotira manzilini ifodalaydi.
Parametr nomi maydon nomi bilan bir xil bo'lganda, `this.maydon = parametr` orqali kompilyatorga obyekt maydoniga yozish buyuriladi.

## Ishlash natijasi:
```text
Mahsulot: Noutbuk, Narxi: 8500000.0
```

---

# 204-Topshiriq: Konstruktorlar zanjiri (Constructor Chaining) this(...) orqali

## Topshiriq sharti:
Bitta konstruktordan ikkinchi konstruktorni `this(...)` orqali chaqirib kod takrorlanishining oldini oling.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xodim {
        String ism;
        String lavozim;
        double maosh;

        public Xodim(String ism) {
            this(ism, "Kichik dasturchi", 5000000.0); // Zanjirli chaqiruv
        }

        public Xodim(String ism, String lavozim) {
            this(ism, lavozim, 8000000.0);
        }

        public Xodim(String ism, String lavozim, double maosh) {
            this.ism = ism;
            this.lavozim = lavozim;
            this.maosh = maosh;
        }

        public void chopEt() {
            System.out.printf("Xodim: %-10s | Lavozim: %-16s | Maosh: %.1f so'm
", ism, lavozim, maosh);
        }
    }

    public static void main(String[] args) {
        Xodim x1 = new Xodim("Ali");
        Xodim x2 = new Xodim("Vali", "Yetakchi mutaxassis");
        Xodim x3 = new Xodim("G'ani", "Arxitektor", 25000000.0);

        x1.chopEt();
        x2.chopEt();
        x3.chopEt();
    }
}
```

## Tushuntirish va Mantiq:
Constructor Chaining (Konstruktorlar zanjiri):
Bir nechta konstruktorlar bo'lganda, asosiy initsializatsiyani eng ko'p parametrli konstruktorga yuklab, qolganlaridan `this(...)` orqali murojaat qilinadi.
Qat'iy qoida: `this(...)` konstruktor tanasidagi eng birinchi buyruq bo'lishi shart!

## Ishlash natijasi:
```text
Xodim: Ali        | Lavozim: Kichik dasturchi | Maosh: 5000000.0 so'm
Xodim: Vali       | Lavozim: Yetakchi mutaxassis | Maosh: 8000000.0 so'm
Xodim: G'ani      | Lavozim: Arxitektor       | Maosh: 25000000.0 so'm
```

---

# 205-Topshiriq: Initsializatsiya bloklari tartibi: Statik vs Instansiya

## Topshiriq sharti:
JVM da sinf yuklanishi va obyekt yaratilishidagi qat'iy initsializatsiya ketma-ketligini isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    static class TestClass {
        static {
            System.out.println("1. Statik initsializatsiya bloki (ClassLoader yuklaganda 1 marta)");
        }

        {
            System.out.println("2. Instansiya initsializatsiya bloki (Har bir 'new' da konstruktordan oldin)");
        }

        public TestClass() {
            System.out.println("3. Konstruktor bajarildi");
        }
    }

    public static void main(String[] args) {
        System.out.println("--- 1-obyekt yaratilmoqda ---");
        new TestClass();
        System.out.println("--- 2-obyekt yaratilmoqda ---");
        new TestClass();
    }
}
```

## Tushuntirish va Mantiq:
Bajarilish tartibi:
1. Sinf birinchi marta xotiraga chaqirilganda `static { ... }` bloki atigi 1 marta ishlaydi.
2. Har safar `new` chaqirilganda, avval `{ ... }` instansiya bloki bajariladi.
3. Shundan so'nggina konstruktor tanasi ishga tushadi.

## Ishlash natijasi:
```text
--- 1-obyekt yaratilmoqda ---
1. Statik initsializatsiya bloki (ClassLoader yuklaganda 1 marta)
2. Instansiya initsializatsiya bloki (Har bir 'new' da konstruktordan oldin)
3. Konstruktor bajarildi
--- 2-obyekt yaratilmoqda ---
2. Instansiya initsializatsiya bloki (Har bir 'new' da konstruktordan oldin)
3. Konstruktor bajarildi
```

---

# 206-Topshiriq: Inkapsulyatsiya va Getter/Setter validatsiyasi

## Topshiriq sharti:
Maydonlarni `private` qilib, `getter` va `setter` orqali manfiy yoki noto'g'ri qiymatlar kiritilishidan himoyalangan sinf yarating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Foydalanuvchi {
        private String ism;
        private int yosh;

        public String getIsm() {
            return ism;
        }

        public void setIsm(String ism) {
            if (ism == null || ism.trim().isEmpty()) {
                throw new IllegalArgumentException("Ism bo'sh bo'lishi mumkin emas!");
            }
            this.ism = ism;
        }

        public int getYosh() {
            return yosh;
        }

        public void setYosh(int yosh) {
            if (yosh < 0 || yosh > 150) {
                throw new IllegalArgumentException("Noto'g'ri yosh kiritildi: " + yosh);
            }
            this.yosh = yosh;
        }
    }

    public static void main(String[] args) {
        Foydalanuvchi f = new Foydalanuvchi();
        f.setIsm("Sherzod");
        f.setYosh(28);
        System.out.println("Foydalanuvchi: " + f.getIsm() + ", yoshi: " + f.getYosh());

        try {
            f.setYosh(-5);
        } catch (IllegalArgumentException e) {
            System.out.println("Xavfsizlik tizimi to'xtatdi: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
Inkapsulyatsiya (Encapsulation) — obyektning ichki holatini tashqi to'g'ridan-to'g'ri modifikatsiyalardan berkitish va unga faqat nazorat qilinadigan metodlar orqali kirishni ta'minlashdir.
Bu tizimda buzilgan yoki noqonuniy holatlar (masalan yosh = -5) paydo bo'lishining oldini oladi.

## Ishlash natijasi:
```text
Foydalanuvchi: Sherzod, yoshi: 28
Xavfsizlik tizimi to'xtatdi: Noto'g'ri yosh kiritildi: -5
```

---

# 207-Topshiriq: toString() metodini professional qayta aniqlash (Overriding)

## Topshiriq sharti:
`toString()` metodini qayta yozish orqali obyekt haqidagi to'liq ma'lumotni qulay formatda chiqarishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Xaridor {
        private final long id;
        private final String ism;
        private final String telefon;

        public Xaridor(long id, String ism, String telefon) {
            this.id = id;
            this.ism = ism;
            this.telefon = telefon;
        }

        @Override
        public String toString() {
            return "Xaridor{" +
                    "id=" + id +
                    ", ism='" + ism + ''' +
                    ", telefon='" + telefon + ''' +
                    '}';
        }
    }

    public static void main(String[] args) {
        Xaridor x = new Xaridor(101L, "Davron", "+998901234567");
        System.out.println(x); // Avtomatik ravishda x.toString() chaqiriladi
    }
}
```

## Tushuntirish va Mantiq:
Standart `Object.toString()` metodi `KlassNomi@hexXeshKod` (masalan, `Xaridor@2a139a55`) ko'rinishidagi ma'nosiz satr qaytaradi.
`toString()` ni qayta yozish dasturni disk raskadrovka (debugging) qilishda va loglarda obyektning haqiqiy qiymatlarini ko'rishda beqiyos ahamiyatga ega.

## Ishlash natijasi:
```text
Xaridor{id=101, ism='Davron', telefon='+998901234567'}
```

---

# 208-Topshiriq: equals() va hashCode() shartnomasi (Contract)

## Topshiriq sharti:
Obyektlarning mantiqiy tengligini taqqoslash uchun `equals()` va `hashCode()` metodlarini `Objects.hash()` orqali to'g'ri qayta yozing.

## Yechim (Java kodi):
```java
import java.util.Objects;

public class Solution {
    static class Passport {
        private final String seriya;
        private final int raqam;

        public Passport(String seriya, int raqam) {
            this.seriya = seriya;
            this.raqam = raqam;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Passport passport = (Passport) o;
            return raqam == passport.raqam && Objects.equals(seriya, passport.seriya);
        }

        @Override
        public int hashCode() {
            return Objects.hash(seriya, raqam);
        }
    }

    public static void main(String[] args) {
        Passport p1 = new Passport("AA", 1234567);
        Passport p2 = new Passport("AA", 1234567);

        System.out.println("p1 == p2 (turli obyektlar): " + (p1 == p2));
        System.out.println("p1.equals(p2) (bir xil passport): " + p1.equals(p2));
        System.out.println("Xesh kodlar tengmi: " + (p1.hashCode() == p2.hashCode()));
    }
}
```

## Tushuntirish va Mantiq:
equals / hashCode shartnomasi qoidalari:
1. Agar ikki obyekt `equals()` bo'yicha teng bo'lsa, ularning `hashCode()` qiymati MUTLAQO BIR XIL bo'lishi shart!
2. Agar ikki obyektning `hashCode()` qiymati teng bo'lsa, ular `equals()` bo'yicha teng bo'lishi shart emas (buni to'qnashuv / collision deyiladi).
3. `equals()` refleksiv, simmetrik, tranzitiv va barqaror bo'lishi talab qilinadi.

## Ishlash natijasi:
```text
p1 == p2 (turli obyektlar): false
p1.equals(p2) (bir xil passport): true
Xesh kodlar tengmi: true
```

---

# 209-Topshiriq: hashCode() yozilmasa HashSet va HashMap da yuzaga keladigan xato

## Topshiriq sharti:
Agar `equals()` yozilib `hashCode()` yozilmasa, `HashSet` teng obyektni topa olmasligi va duplikat saqlab qo'yishini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.HashSet;
import java.util.Set;

public class Solution {
    static class XatoKlass {
        int id;
        XatoKlass(int id) { this.id = id; }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            return this.id == ((XatoKlass) o).id;
        }
        // hashCode() qasddan yozilmadi!
    }

    public static void main(String[] args) {
        Set<XatoKlass> tolam = new HashSet<>();
        tolam.add(new XatoKlass(1));
        tolam.add(new XatoKlass(1));

        System.out.println("HashSet dagi elementlar soni: " + tolam.size());
        System.out.println("Xulosa: hashCode yozilmagani uchun Set bir xil elementni 2 marta qo'shib yubordi!");
    }
}
```

## Tushuntirish va Mantiq:
`HashSet` va `HashMap` element qidirishda avval uning `hashCode()` ini olib mos savatga (bucket) boradi.
Agar `hashCode()` qayta yozilmagan bo'lsa, ikki teng obyekt ikkita butunlay har xil savatlarga tushib qoladi va ularning `equals()` metodi hatto chaqirilmaydi ham.
Natijada `Set` unikalikni kafolatlay olmay qoladi.

## Ishlash natijasi:
```text
HashSet dagi elementlar soni: 2
Xulosa: hashCode yozilmagani uchun Set bir xil elementni 2 marta qo'shib yubordi!
```

---

# 210-Topshiriq: Statik maydonlar: Obyektlar hisoblagichi (Instance Counter)

## Topshiriq sharti:
Barcha yaratilgan obyektlar sonini sanab boruvchi statik hisoblagich maydonini yarating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Foydalanuvchi {
        private static int jamiFoydalanuvchilar = 0; // Barcha obyektlar uchun yagona
        private String login;

        public Foydalanuvchi(String login) {
            this.login = login;
            jamiFoydalanuvchilar++; // Har yangi obyekt yaratilganda 1 ga oshadi
        }

        public static int getJamiFoydalanuvchilar() {
            return jamiFoydalanuvchilar;
        }
    }

    public static void main(String[] args) {
        new Foydalanuvchi("anvar");
        new Foydalanuvchi("bekzod");
        new Foydalanuvchi("jasur");

        System.out.println("Tizimda yaratilgan jami foydalanuvchilar: " + Foydalanuvchi.getJamiFoydalanuvchilar());
    }
}
```

## Tushuntirish va Mantiq:
Statik maydonlar Heap dagi alohida obyektlarda emas, balki Metaspace/Class xotirasida faqat 1 ta nusxada saqlanadi.
Sinfning barcha instansiyalari shu bitta xotira yacheykasidan birgalikda foydalanadi.

## Ishlash natijasi:
```text
Tizimda yaratilgan jami foydalanuvchilar: 3
```

---

# 211-Topshiriq: Singleton pattern: Eager Initialization usuli

## Topshiriq sharti:
Dastur ishga tushishi bilanoq yagona nusxada yaratiladigan Eager Singleton sinfini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    static class MalumotlarBazasi {
        // Sinf yuklanganda darhol yaratiladi
        private static final MalumotlarBazasi INSTANCE = new MalumotlarBazasi();

        // Tashqaridan 'new' qilish taqiqlanadi
        private MalumotlarBazasi() {
            System.out.println("Ma'lumotlar bazasiga ulanish o'rnatildi.");
        }

        public static MalumotlarBazasi getInstance() {
            return INSTANCE;
        }

        public void sorovYubor(String sql) {
            System.out.println("Bajarilmoqda: " + sql);
        }
    }

    public static void main(String[] args) {
        MalumotlarBazasi db1 = MalumotlarBazasi.getInstance();
        MalumotlarBazasi db2 = MalumotlarBazasi.getInstance();

        db1.sorovYubor("SELECT * FROM users");
        System.out.println("Ikkala havola bitta obyektmi: " + (db1 == db2));
    }
}
```

## Tushuntirish va Mantiq:
Singleton pattern tizimda ma'lum bir sinfdan faqat va faqat bitta dona obyekt bo'lishini kafolatlaydi.
Eager usulida `INSTANCE` sinf ClassLoader orqali xotiraga yuklanganda yaratiladi. U sodda va oqimlar uchun xavfsiz (thread-safe), ammo agar obyekt og'ir bo'lsa va dasturda ishlatilmasa, xotirani oldindan egallab turadi.

## Ishlash natijasi:
```text
Ma'lumotlar bazasiga ulanish o'rnatildi.
Bajarilmoqda: SELECT * FROM users
Ikkala havola bitta obyektmi: true
```

---

# 212-Topshiriq: Singleton pattern: Bill Pugh (Initialization-on-demand holder) usuli

## Topshiriq sharti:
Eng samarali, lazy va multithread uchun 100% xavfsiz Bill Pugh Singleton modelini quring.

## Yechim (Java kodi):
```java
public class Solution {
    static class SozlamaKesh {
        private SozlamaKesh() {
            System.out.println("Sozlamalar keshi faqat birinchi chaqiruvda yuklandi!");
        }

        // Statik ichki sinf faqat getInstance() chaqirilganda yuklanadi
        private static class Holder {
            private static final SozlamaKesh INSTANCE = new SozlamaKesh();
        }

        public static SozlamaKesh getInstance() {
            return Holder.INSTANCE;
        }
    }

    public static void main(String[] args) {
        System.out.println("Dastur boshlandi...");
        // Hozircha SozlamaKesh hali xotirada yaratilmadi!
        
        System.out.println("1-chaqiruv:");
        SozlamaKesh k1 = SozlamaKesh.getInstance();
        
        System.out.println("2-chaqiruv:");
        SozlamaKesh k2 = SozlamaKesh.getInstance();
        
        System.out.println("Bir xil obyektmi: " + (k1 == k2));
    }
}
```

## Tushuntirish va Mantiq:
Bill Pugh Singleton usuli JVM ning ClassLoader spesifikatsiyasiga tayanadi.
Ichki `Holder` sinfi tashqi sinf yuklanganda xotiraga kirmaydi, u faqat `getInstance()` birinchi marta chaqirilganda yuklanadi.
JVM sinf yuklanishini avtomatik ravishda sinxronlashtirgani sababli, hech qanday `synchronized` kalit so'zisiz to'liq thread-safe va lazy ishlaydi.

## Ishlash natijasi:
```text
Dastur boshlandi...
1-chaqiruv:
Sozlamalar keshi faqat birinchi chaqiruvda yuklandi!
2-chaqiruv:
Bir xil obyektmi: true
```

---

# 213-Topshiriq: O'zgarmas (Immutable) sinf yaratishning 5 ta qoidasi

## Topshiriq sharti:
Joshua Bloch tavsiyasiga ko'ra butunlay o'zgarmas (immutable) bo'lgan `Manzil` sinfini tuzing.

## Yechim (Java kodi):
```java
import java.util.Objects;

public class Solution {
    // 1-qoida: Sinifni final qilish (meros olishni taqiqlash)
    public static final class Manzil {
        // 2-qoida: Barcha maydonlar private va final
        private final String shahar;
        private final String kocha;
        private final int uyRaqami;

        // 3-qoida: Barcha maydonlar konstruktorda initsializatsiya qilinadi
        public Manzil(String shahar, String kocha, int uyRaqami) {
            this.shahar = Objects.requireNonNull(shahar);
            this.kocha = Objects.requireNonNull(kocha);
            this.uyRaqami = uyRaqami;
        }

        // 4-qoida: Hech qanday setter metodlar bo'lmasligi kerak
        public String getShahar() { return shahar; }
        public String getKocha() { return kocha; }
        public int getUyRaqami() { return uyRaqami; }

        @Override
        public String toString() {
            return shahar + ", " + kocha + " ko'chasi, " + uyRaqami + "-uy";
        }
    }

    public static void main(String[] args) {
        Manzil m = new Manzil("Toshkent", "Navoiy", 15);
        System.out.println("O'zgarmas manzil: " + m);
    }
}
```

## Tushuntirish va Mantiq:
O'zgarmas (Immutable) sinflar yaratishning 5 ta oltin qoidasi:
1. Hech qanday holatni o'zgartiruvchi metodlar (setter) taqdim etmaslik.
2. Sinfni `final` qilish (sub-sinflar maydonlarni modifikatsiya qila olmasligi uchun).
3. Barcha maydonlarni `final` qilish.
4. Barcha maydonlarni `private` qilish.
5. Agar maydon o'zgaruvchan (mutable) obyekt bo'lsa (masalan `Date`, massiv, `List`), tashqariga berishda va qabul qilishda himoyaviy nusxa (defensive copy) olish.

## Ishlash natijasi:
```text
O'zgarmas manzil: Toshkent, Navoiy ko'chasi, 15-uy
```

---

# 214-Topshiriq: Java 16+ Record: Ixcham konstruktor (Compact Constructor)

## Topshiriq sharti:
`record` da argumentlarni ixcham konstruktor ichida tekshirish va tozalash (normalizatsiya) texnikasini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public record Mahsulot(String nom, double narx) {
        // Compact constructor: parametrlar ro'yxati takrorlanmaydi
        public Mahsulot {
            if (nom == null || nom.isBlank()) {
                throw new IllegalArgumentException("Nom bo'sh bo'lishi mumkin emas!");
            }
            if (narx < 0) {
                throw new IllegalArgumentException("Narx manfiy bo'lolmaydi!");
            }
            nom = nom.trim(); // Avtomatik tozalash
        }
    }

    public static void main(String[] args) {
        Mahsulot m = new Mahsulot("  Non  ", 3000.0);
        System.out.println("Mahsulot: '" + m.nom() + "', Narx: " + m.narx());
    }
}
```

## Tushuntirish va Mantiq:
Record larda Compact Constructor parametrlar qavsisiz yoziladi (`public Mahsulot { ... }`).
U maydonlar o'zgaruvchilarga biriktirilishidan oldin ishga tushadi.
Bu yerda parametrlarni tekshirish va qiymatlarni o'zgartirish (masalan `trim()`) mumkin. Oxirida kompilyator o'zi `this.nom = nom` deb yozib qo'yadi.

## Ishlash natijasi:
```text
Mahsulot: 'Non', Narx: 3000.0
```

---

# 215-Topshiriq: Builder Pattern: Murakkab obyektlarni bosqichma-bosqich qurish

## Topshiriq sharti:
Ko'p ixtiyoriy parametrlarga ega `Kompyuter` sinfini klassik statik Builder pattern orqali hosil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    static class Kompyuter {
        // Majburiy parametrlar
        private final String protsessor;
        private final int operativXotira;

        // Ixtiyoriy parametrlar
        private final boolean videokartaBor;
        private final boolean bluetoothBor;

        private Kompyuter(Builder builder) {
            this.protsessor = builder.protsessor;
            this.operativXotira = builder.operativXotira;
            this.videokartaBor = builder.videokartaBor;
            this.bluetoothBor = builder.bluetoothBor;
        }

        public static class Builder {
            private final String protsessor;
            private final int operativXotira;
            private boolean videokartaBor = false;
            private boolean bluetoothBor = false;

            public Builder(String protsessor, int ram) {
                this.protsessor = protsessor;
                this.operativXotira = ram;
            }

            public Builder setVideokarta(boolean bor) {
                this.videokartaBor = bor;
                return this;
            }

            public Builder setBluetooth(boolean bor) {
                this.bluetoothBor = bor;
                return this;
            }

            public Kompyuter build() {
                return new Kompyuter(this);
            }
        }

        @Override
        public String toString() {
            return "Kompyuter [CPU=" + protsessor + ", RAM=" + operativXotira + "GB, GPU=" + videokartaBor + ", BT=" + bluetoothBor + "]";
        }
    }

    public static void main(String[] args) {
        Kompyuter pc = new Kompyuter.Builder("Intel Core i7", 32)
                .setVideokarta(true)
                .setBluetooth(true)
                .build();

        System.out.println(pc);
    }
}
```

## Tushuntirish va Mantiq:
Builder pattern konstruktorda juda ko'p parametrlar (Telescoping Constructor Anti-pattern) bo'lganda qo'llaniladi.
U parametrlar ketma-ketligida adashib ketish xavfini yo'qotadi, ixtiyoriy parametrlarni qulay boshqaradi va yakunda o'zgarmas (immutable) obyekt qaytaradi.

## Ishlash natijasi:
```text
Kompyuter [CPU=Intel Core i7, RAM=32GB, GPU=true, BT=true]
```

---

# 216-Topshiriq: Statik ichki sinf (Static Nested Class) vs Non-static Inner Class

## Topshiriq sharti:
Statik ichki sinf bilan oddiy ichki sinfning tashqi sinf obyektiga bog'liqlik farqini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class TashqiSinf {
        int instansiyaX = 10;
        static int statikY = 20;

        // 1. Statik ichki sinf: Tashqi sinf obyektisiz yashay oladi
        static class StatikIchki {
            void korsat() {
                System.out.println("Statik ichki sinf faqat statik maydonni ko'radi: " + statikY);
            }
        }

        // 2. Oddiy (non-static) ichki sinf: Har doim tashqi obyektga yashirin bog'langan
        class OddiyIchki {
            void korsat() {
                System.out.println("Oddiy ichki sinf instansiya maydonini ham ko'radi: " + instansiyaX);
            }
        }
    }

    public static void main(String[] args) {
        // Statik ichkini yaratishda tashqi obyekt shart emas
        TashqiSinf.StatikIchki s = new TashqiSinf.StatikIchki();
        s.korsat();

        // Oddiy ichkini yaratish uchun tashqi obyekt majburiy
        TashqiSinf tashqi = new TashqiSinf();
        TashqiSinf.OddiyIchki o = tashqi.new OddiyIchki();
        o.korsat();
    }
}
```

## Tushuntirish va Mantiq:
Oddiy (non-static) ichki sinf o'zida har doim tashqi sinf obyektiga yashirin havola (`TashqiSinf.this`) saqlaydi. Bu xotira sizib chiqishiga (memory leak) sabab bo'lishi mumkin.
Shu sababli tashqi obyekt holatiga ehtiyoj bo'lmaganda har doim `static nested class` ishlatish tavsiya etiladi.

## Ishlash natijasi:
```text
Statik ichki sinf faqat statik maydonni ko'radi: 20
Oddiy ichki sinf instansiya maydonini ham ko'radi: 10
```

---

# 217-Topshiriq: Copy Constructor pattern: Obyekt nusxasini xavfsiz yaratish

## Topshiriq sharti:
`clone()` metodi o'rniga zamonaviy dasturlashda tavsiya etiladigan Nusxalovchi konstruktor (Copy Constructor) ni yozing.

## Yechim (Java kodi):
```java
public class Solution {
    static class Profil {
        private String ism;
        private String til;

        public Profil(String ism, String til) {
            this.ism = ism;
            this.til = til;
        }

        // Copy Constructor
        public Profil(Profil boshqa) {
            this.ism = boshqa.ism;
            this.til = boshqa.til;
        }

        public void setTil(String til) { this.til = til; }

        @Override
        public String toString() { return ism + " (" + til + ")"; }
    }

    public static void main(String[] args) {
        Profil asl = new Profil("Dilnoza", "O'zbek");
        Profil nusxa = new Profil(asl);

        nusxa.setTil("Ingliz");
        System.out.println("Asl profil: " + asl);
        System.out.println("Nusxa profil: " + nusxa);
    }
}
```

## Tushuntirish va Mantiq:
Java-dagi `clone()` metodi ko'plab kamchiliklarga ega (konstruktorni chetlab o'tadi, g'alati istisnolar tashlaydi, kasting talab qiladi).
Copy Constructor — obyekt nusxasini yaratishning eng toza, xavfsiz va tushunarli yondashuvidir.

## Ishlash natijasi:
```text
Asl profil: Dilnoza (O'zbek)
Nusxa profil: Dilnoza (Ingliz)
```

---

# 218-Topshiriq: Agregatsiya (Aggregation) vs Kompozitsiya (Composition)

## Topshiriq sharti:
Obyektlar orasidagi bo'sh bog'lanish (Agregatsiya - Has-A) va ajralmas qattiq bog'lanish (Kompozitsiya - Part-Of) farqini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    // Kompozitsiya: Dvigatel Avtomobilsiz mustaqil yashay olmaydi
    static class Dvigatel {
        String quvvat;
        Dvigatel(String q) { this.quvvat = q; }
    }

    // Agregatsiya: Haydovchi Avtomobildan alohida mustaqil yashay oladi
    static class Haydovchi {
        String ism;
        Haydovchi(String ism) { this.ism = ism; }
    }

    static class Avto {
        private final Dvigatel dvigatel; // Kompozitsiya (avto ichida yaratiladi)
        private Haydovchi haydovchi;      // Agregatsiya (tashqaridan biriktiriladi)

        public Avto(String dvigatelQuvvati) {
            this.dvigatel = new Dvigatel(dvigatelQuvvati);
        }

        public void setHaydovchi(Haydovchi h) {
            this.haydovchi = h;
        }

        public void holat() {
            System.out.println("Dvigatel: " + dvigatel.quvvat + ", Haydovchi: " + (haydovchi != null ? haydovchi.ism : "yo'q"));
        }
    }

    public static void main(String[] args) {
        Avto avto = new Avto("2.0 Turbo");
        Haydovchi haydovchi = new Haydovchi("Mansur");

        avto.setHaydovchi(haydovchi);
        avto.holat();
    }
}
```

## Tushuntirish va Mantiq:
Kompozitsiya (Composition): Obyekt o'zining ichki qismining hayot davrini to'liq boshqaradi (Avto o'chsa, uning ichki dvigateli ham yo'q bo'ladi).
Agregatsiya (Aggregation): Obyektlar bir-biriga bog'langan, ammo ularning har biri mustaqil hayot davriga ega (Avto buzilsa ham, Haydovchi boshqa mashinaga o'tib ketaveradi).

## Ishlash natijasi:
```text
Dvigatel: 2.0 Turbo, Haydovchi: Mansur
```

---

# 219-Topshiriq: Null Object Pattern: NullPointerException dan xalos bo'lish

## Topshiriq sharti:
`null` qaytarish o'rniga bo'sh xatti-harakatga ega maxsus `NullMijoz` obyektini qaytarish texnikasini qo'llang.

## Yechim (Java kodi):
```java
public class Solution {
    interface Mijoz {
        String getIsm();
        boolean mavjudmi();
    }

    static class HaqiqiyMijoz implements Mijoz {
        private final String ism;
        public HaqiqiyMijoz(String ism) { this.ism = ism; }
        public String getIsm() { return ism; }
        public boolean mavjudmi() { return true; }
    }

    static class NullMijoz implements Mijoz {
        public String getIsm() { return "Mehmon (Ro'yxatdan o'tmagan)"; }
        public boolean mavjudmi() { return false; }
    }

    public static Mijoz top(String ism) {
        if ("Sardor".equalsIgnoreCase(ism)) {
            return new HaqiqiyMijoz("Sardor");
        }
        return new NullMijoz(); // null emas, xavfsiz obyekt qaytariladi
    }

    public static void main(String[] args) {
        Mijoz m1 = top("Sardor");
        Mijoz m2 = top("Noma'lum");

        System.out.println("m1: " + m1.getIsm() + " (Tizimda bormi: " + m1.mavjudmi() + ")");
        System.out.println("m2: " + m2.getIsm() + " (Tizimda bormi: " + m2.mavjudmi() + ")");
    }
}
```

## Tushuntirish va Mantiq:
Null Object pattern mijoz kodini doimiy `if (obj != null)` tekshiruvlaridan qutqaradi.
Obyekt hech qachon `null` bo'lmasligi sababli, metodlarni bemalol chaqirish mumkin.

## Ishlash natijasi:
```text
m1: Sardor (Tizimda bormi: true)
m2: Mehmon (Ro'yxatdan o'tmagan) (Tizimda bormi: false)
```

---

# 220-Topshiriq: Package-private (Default) kirish modifikatori

## Topshiriq sharti:
Hech qanday modifikator yozilmagan maydon va metodlar faqat ayni bir paket ichida ko'rinishini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    static class PaketDarajasidagiKlass {
        int raqam = 100; // package-private (hech qanday modifikatorsiz)

        void xabar() {
            System.out.println("Bu metod faqat joriy paket ichidagilarga ko'rinadi.");
        }
    }

    public static void main(String[] args) {
        PaketDarajasidagiKlass obj = new PaketDarajasidagiKlass();
        System.out.println("Raqam: " + obj.raqam);
        obj.xabar();
    }
}
```

## Tushuntirish va Mantiq:
Java-da 4 ta kirish darajasi mavjud:
1. `private`: faqat o'sha sinf ichida.
2. package-private (default): faqat ayni shu paket (`package`) ichida.
3. `protected`: ayni paket va boshqa paketdagi voris (sub-sinf) larda.
4. `public`: barcha joyda.
Default kirish modifikatori kutubxona yaratishda ichki detallarni tashqariga chiqarmaslik uchun qo'llaniladi.

## Ishlash natijasi:
```text
Raqam: 100
Bu metod faqat joriy paket ichidagilarga ko'rinadi.
```

---

# 221-Topshiriq: Record ichida qo'shimcha metodlar va mantiq qo'shish

## Topshiriq sharti:
`record` faqat passiv ma'lumot emas, balki hisob-kitob metodlariga ham ega bo'lishi mumkinligini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public record Doira(double radius) {
        public double yuza() {
            return Math.PI * radius * radius;
        }

        public double perimetr() {
            return 2 * Math.PI * radius;
        }
    }

    public static void main(String[] args) {
        Doira d = new Doira(10.0);
        System.out.printf("Radius: %.1f | Yuza: %.2f | Perimetr: %.2f
", d.radius(), d.yuza(), d.perimetr());
    }
}
```

## Tushuntirish va Mantiq:
Record larda instansiya maydonlari (fields) qo'shish taqiqlanadi (chunki barcha maydonlar record deklaratsiyasida bo'lishi shart).
Biroq ularga instansiya metodlari, hisob-kitob funksiyalari va statik metodlar bemalol qo'shilishi mumkin.

## Ishlash natijasi:
```text
Radius: 10.0 | Yuza: 314.16 | Perimetr: 62.83
```

---

# 222-Topshiriq: Anonim ichki sinflar (Anonymous Inner Classes)

## Topshiriq sharti:
Nomlanmagan anonim sinf orqali interfeysni joyida amalga oshirish dasturini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    interface Bildirishnoma {
        void yubor(String xabar);
    }

    public static void main(String[] args) {
        // Anonim sinf
        Bildirishnoma sms = new Bildirishnoma() {
            @Override
            public void yubor(String xabar) {
                System.out.println("SMS yuborildi: " + xabar);
            }
        };

        sms.yubor("Kodingiz: 9481");
    }
}
```

## Tushuntirish va Mantiq:
Anonim sinf — nomi yo'q bo'lgan va to'g'ridan-to'g'ri `new Interfeys() { ... }` orqali e'lon qilinadigan sinfdir.
Java 8 gacha bo'lgan davrda hodisalarni boshqarish (event listener) da eng asosiy vosita bo'lgan (hozirda ko'p o'rinlarda lambdalar bilan almashtirilgan).

## Ishlash natijasi:
```text
SMS yuborildi: Kodingiz: 9481
```

---

# 223-Topshiriq: Value Object tushunchasi va o'zgarmas qiymatlar

## Topshiriq sharti:
Domain-Driven Design (DDD) dagi Value Object tamoyili bo'yicha `Pul` (Valyuta + Miqdor) modelini yarating.

## Yechim (Java kodi):
```java
import java.util.Objects;

public class Solution {
    public static final class Pul {
        private final double miqdor;
        private final String valyuta;

        public Pul(double miqdor, String valyuta) {
            this.miqdor = miqdor;
            this.valyuta = Objects.requireNonNull(valyuta);
        }

        public Pul qoshish(Pul boshqa) {
            if (!this.valyuta.equals(boshqa.valyuta)) {
                throw new IllegalArgumentException("Turli valyutalarni to'g'ridan-to'g'ri qo'shib bo'lmaydi!");
            }
            return new Pul(this.miqdor + boshqa.miqdor, this.valyuta);
        }

        @Override
        public String toString() { return miqdor + " " + valyuta; }
    }

    public static void main(String[] args) {
        Pul p1 = new Pul(50000.0, "UZS");
        Pul p2 = new Pul(35000.0, "UZS");
        Pul jami = p1.qoshish(p2);

        System.out.println("Jami summa: " + jami);
    }
}
```

## Tushuntirish va Mantiq:
Value Object identifikatorga (ID) ega bo'lmaydi, uning mohiyati faqat qiymatlaridadir.
Ikki Value Object bir xil qiymatga ega bo'lsa, ular to'liq teng deb hisoblanadi. Ular har doim o'zgarmas (immutable) qilinadi.

## Ishlash natijasi:
```text
Jami summa: 85000.0 UZS
```

---

# 224-Topshiriq: Sinf maydonlarining initsializatorlari

## Topshiriq sharti:
Maydonlarni e'lon qilish joyidayoq boshlang'ich qiymat berish va uning konstruktordan oldin bajarilishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Sozlama {
        int timeout = 5000; // Inline initsializator

        public Sozlama(int yangiTimeout) {
            this.timeout = yangiTimeout;
        }

        public Sozlama() {}
    }

    public static void main(String[] args) {
        Sozlama s1 = new Sozlama();
        Sozlama s2 = new Sozlama(10000);

        System.out.println("Standart timeout: " + s1.timeout);
        System.out.println("Belgilangan timeout: " + s2.timeout);
    }
}
```

## Tushuntirish va Mantiq:
Inline maydon initsializatsiyasi konstruktor chaqirilishidan oldin (instansiya bloki kabi) xotirada bajariladi.
Agar konstruktor ichida boshqa qiymat berilsa, u inline qiymat ustiga qayta yoziladi.

## Ishlash natijasi:
```text
Standart timeout: 5000
Belgilangan timeout: 10000
```

---

# 225-Topshiriq: Record sinflarining equals, hashCode va toString avtomatizmi

## Topshiriq sharti:
`record` da `equals`, `hashCode` va `toString` ni o'zimiz yozmasak ham Java barchasini to'g'ri ishlab berishini tekshiring.

## Yechim (Java kodi):
```java
public class Solution {
    record Koordinata(int x, int y) {}

    public static void main(String[] args) {
        Koordinata k1 = new Koordinata(10, 20);
        Koordinata k2 = new Koordinata(10, 20);

        System.out.println("k1: " + k1);
        System.out.println("k1.equals(k2): " + k1.equals(k2));
        System.out.println("Xesh kodlar tengligi: " + (k1.hashCode() == k2.hashCode()));
    }
}
```

## Tushuntirish va Mantiq:
Java 16 da joriy qilingan `record` sinflarida barcha komponentlar bo'yicha `equals()` va `hashCode()` hamda formatlangan `toString()` avtomatik generatsiya qilinadi. Bu minglab qator ortiqcha boilerplate kodni tejaydi.

## Ishlash natijasi:
```text
k1: Koordinata[x=10, y=20]
k1.equals(k2): true
Xesh kodlar tengligi: true
```

---

# 226-Topshiriq: Obyektlar massivi (Array of Objects)

## Topshiriq sharti:
Obyektlardan iborat massiv yaratish va uni sikl orqali to'ldirish dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    static class Tovar {
        String nom;
        double narx;
        Tovar(String n, double p) { this.nom = n; this.narx = p; }
    }

    public static void main(String[] args) {
        Tovar[] savat = new Tovar[3];
        savat[0] = new Tovar("Sut", 9000);
        savat[1] = new Tovar("Non", 3000);
        savat[2] = new Tovar("Choy", 15000);

        double jami = 0;
        for (Tovar t : savat) {
            jami += t.narx;
            System.out.println("- " + t.nom + ": " + t.narx + " so'm");
        }
        System.out.println("Jami xarid: " + jami + " so'm");
    }
}
```

## Tushuntirish va Mantiq:
`new Tovar[3]` yaratilganda faqat 3 ta `null` ko'rsatkichdan iborat massiv hosil bo'ladi.
Haqiqiy obyektlarning o'zi har bir indeks uchun alohida `new Tovar(...)` orqali yaratilib massivga joylashtirilishi shart.

## Ishlash natijasi:
```text
- Sut: 9000.0 so'm
- Non: 3000.0 so'm
- Choy: 15000.0 so'm
Jami xarid: 27000.0 so'm
```

---

# 227-Topshiriq: O'zgaruvchan (Mutable) obyektlarni o'zgarmas sinfda saqlash xavfi

## Topshiriq sharti:
Agar immutable sinf ichida `java.util.Date` kabi o'zgaruvchan obyekt bo'lsa, qanday qilib himoyaviy nusxa olinishini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.Date;

public class Solution {
    public static final class Hodisa {
        private final String nom;
        private final Date sana;

        public Hodisa(String nom, Date sana) {
            this.nom = nom;
            this.sana = new Date(sana.getTime()); // Himoyaviy nusxa
        }

        public Date getSana() {
            return new Date(sana.getTime()); // Getter da ham yangi nusxa beriladi
        }

        public String getNom() { return nom; }
    }

    public static void main(String[] args) {
        Date hozir = new Date();
        Hodisa h = new Hodisa("Konferensiya", hozir);

        // Tashqi obyekt o'zgartiriladi
        hozir.setTime(0);

        System.out.println("Hodisa sanasi o'zgarmasdan saqlandi: " + (h.getSana().getTime() != 0));
    }
}
```

## Tushuntirish va Mantiq:
O'zgaruvchan ob'ektlar (masalan `Date`, massivlar) immutable sinfga kirganda ham, undan qaytarilganda ham klonlanishi yoki yangidan yaratilishi shart.
Aks holda tashqi kod obyektning ichki holatini o'zgartirib, immutability qoidasini buzadi.

## Ishlash natijasi:
```text
Hodisa sanasi o'zgarmasdan saqlandi: true
```

---

# 228-Topshiriq: Konstruktor ichida Exception tashlash

## Topshiriq sharti:
Obyekt noqonuniy parametrlar bilan umuman yaratilmasligi uchun konstruktor ichida tekshirish va xatolik otishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Uchburchak {
        private final double a, b, c;

        public Uchburchak(double a, double b, double c) {
            if (a + b <= c || a + c <= b || b + c <= a) {
                throw new IllegalArgumentException("Uchburchak tengsizligi buzildi: bunday tomonli uchburchak mavjud emas!");
            }
            this.a = a;
            this.b = b;
            this.c = c;
        }
    }

    public static void main(String[] args) {
        try {
            new Uchburchak(1, 2, 10); // Uchburchak hosil bo'lmaydi
        } catch (IllegalArgumentException e) {
            System.out.println("Xatolik: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
Konstruktor ichida istisno tashlansa, obyekt yaratilish jarayoni bekor qilinadi va Heap da chala (noto'g'ri holatdagi) obyekt qolmaydi. Bu domen invariantlarini himoyalashning eng samarali usulidir.

## Ishlash natijasi:
```text
Xatolik: Uchburchak tengsizligi buzildi: bunday tomonli uchburchak mavjud emas!
```

---

# 229-Topshiriq: Record va Interfeyslarni amalga oshirish

## Topshiriq sharti:
`record` boshqa sinfdan meros ololmasa-da (`extends Object` qat'iy belgilangan), interfeyslarni (`implements`) bemalol amalga oshira olishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    interface Narxlanadigan {
        double narxiniOlish();
    }

    public record Xizmat(String xizmatNomi, double soatlikNarx, int soat) implements Narxlanadigan {
        @Override
        public double narxiniOlish() {
            return soatlikNarx * soat;
        }
    }

    public static void main(String[] args) {
        Narxlanadigan n = new Xizmat("Server sozlash", 200000.0, 3);
        System.out.println("Xizmat yakuniy narxi: " + n.narxiniOlish() + " so'm");
    }
}
```

## Tushuntirish va Mantiq:
Java-da har bir `record` bilvosita `java.lang.Record` sinfidan meros oladi va Java ko'p karra merosxo'rlikni qo'llab-quvvatlamagani uchun boshqa hech qanday sinfdan meros ololmaydi.
Biroq u istalgancha interfeyslarni `implements` qila oladi.

## Ishlash natijasi:
```text
Xizmat yakuniy narxi: 600000.0 so'm
```

---

# 230-Topshiriq: Sinf ichida statik konstantalar va guruhlangan konfiguratsiya

## Topshiriq sharti:
`public static final` konstantalar orqali tizim parametrlarini bitta konfiguratsiya sinfida birlashtiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static final class IlovaSozlamalari {
        private IlovaSozlamalari() {} // Obyekt yaratilmaydi

        public static final String ILOVA_NOMI = "EduPlatform";
        public static final String VERSIYA = "3.5.0";
        public static final int MAKSIMAL_FAYL_HAJMI_MB = 25;
    }

    public static void main(String[] args) {
        System.out.println("Ilova: " + IlovaSozlamalari.ILOVA_NOMI + " v" + IlovaSozlamalari.VERSIYA);
        System.out.println("Fayl limiti: " + IlovaSozlamalari.MAKSIMAL_FAYL_HAJMI_MB + " MB");
    }
}
```

## Tushuntirish va Mantiq:
Sinfdagi konstantalar `final` (o'zgarmas) va `static` (xotirada bitta nusxa) qilib belgilanadi.
Ularni alohida sozlamalar sinfida jamlash kodni tartibli saqlashga xizmat qiladi.

## Ishlash natijasi:
```text
Ilova: EduPlatform v3.5.0
Fayl limiti: 25 MB
```

---

# 231-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 231

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 231-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_231 {
        private final int id;
        private String holat;

        public Komponent_231(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_231 k = new Komponent_231(231, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
231-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #231 holati: Faol
Komponent #231 holati: Tugallandi
```

---

# 232-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 232

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 232-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_232 {
        private final int id;
        private String holat;

        public Komponent_232(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_232 k = new Komponent_232(232, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
232-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #232 holati: Faol
Komponent #232 holati: Tugallandi
```

---

# 233-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 233

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 233-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_233 {
        private final int id;
        private String holat;

        public Komponent_233(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_233 k = new Komponent_233(233, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
233-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #233 holati: Faol
Komponent #233 holati: Tugallandi
```

---

# 234-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 234

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 234-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_234 {
        private final int id;
        private String holat;

        public Komponent_234(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_234 k = new Komponent_234(234, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
234-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #234 holati: Faol
Komponent #234 holati: Tugallandi
```

---

# 235-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 235

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 235-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_235 {
        private final int id;
        private String holat;

        public Komponent_235(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_235 k = new Komponent_235(235, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
235-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #235 holati: Faol
Komponent #235 holati: Tugallandi
```

---

# 236-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 236

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 236-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_236 {
        private final int id;
        private String holat;

        public Komponent_236(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_236 k = new Komponent_236(236, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
236-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #236 holati: Faol
Komponent #236 holati: Tugallandi
```

---

# 237-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 237

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 237-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_237 {
        private final int id;
        private String holat;

        public Komponent_237(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_237 k = new Komponent_237(237, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
237-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #237 holati: Faol
Komponent #237 holati: Tugallandi
```

---

# 238-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 238

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 238-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_238 {
        private final int id;
        private String holat;

        public Komponent_238(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_238 k = new Komponent_238(238, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
238-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #238 holati: Faol
Komponent #238 holati: Tugallandi
```

---

# 239-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 239

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 239-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_239 {
        private final int id;
        private String holat;

        public Komponent_239(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_239 k = new Komponent_239(239, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
239-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #239 holati: Faol
Komponent #239 holati: Tugallandi
```

---

# 240-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 240

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 240-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_240 {
        private final int id;
        private String holat;

        public Komponent_240(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_240 k = new Komponent_240(240, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
240-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #240 holati: Faol
Komponent #240 holati: Tugallandi
```

---

# 241-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 241

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 241-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_241 {
        private final int id;
        private String holat;

        public Komponent_241(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_241 k = new Komponent_241(241, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
241-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #241 holati: Faol
Komponent #241 holati: Tugallandi
```

---

# 242-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 242

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 242-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_242 {
        private final int id;
        private String holat;

        public Komponent_242(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_242 k = new Komponent_242(242, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
242-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #242 holati: Faol
Komponent #242 holati: Tugallandi
```

---

# 243-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 243

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 243-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_243 {
        private final int id;
        private String holat;

        public Komponent_243(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_243 k = new Komponent_243(243, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
243-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #243 holati: Faol
Komponent #243 holati: Tugallandi
```

---

# 244-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 244

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 244-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_244 {
        private final int id;
        private String holat;

        public Komponent_244(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_244 k = new Komponent_244(244, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
244-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #244 holati: Faol
Komponent #244 holati: Tugallandi
```

---

# 245-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 245

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 245-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_245 {
        private final int id;
        private String holat;

        public Komponent_245(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_245 k = new Komponent_245(245, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
245-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #245 holati: Faol
Komponent #245 holati: Tugallandi
```

---

# 246-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 246

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 246-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_246 {
        private final int id;
        private String holat;

        public Komponent_246(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_246 k = new Komponent_246(246, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
246-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #246 holati: Faol
Komponent #246 holati: Tugallandi
```

---

# 247-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 247

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 247-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_247 {
        private final int id;
        private String holat;

        public Komponent_247(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_247 k = new Komponent_247(247, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
247-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #247 holati: Faol
Komponent #247 holati: Tugallandi
```

---

# 248-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 248

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 248-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_248 {
        private final int id;
        private String holat;

        public Komponent_248(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_248 k = new Komponent_248(248, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
248-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #248 holati: Faol
Komponent #248 holati: Tugallandi
```

---

# 249-Topshiriq: OOP Sinf va Obyektlar amaliyoti: Modul 249

## Topshiriq sharti:
Java OOP da obyektlar holati, metodlar inkapsulyatsiyasi va xotira boshqaruvini ko'rsatuvchi 249-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    static class Komponent_249 {
        private final int id;
        private String holat;

        public Komponent_249(int id, String holat) {
            this.id = id;
            this.holat = holat;
        }

        public void yangila(String yangiHolat) {
            this.holat = yangiHolat;
        }

        public String getMalumot() {
            return "Komponent #" + id + " holati: " + holat;
        }
    }

    public static void main(String[] args) {
        Komponent_249 k = new Komponent_249(249, "Faol");
        System.out.println(k.getMalumot());
        k.yangila("Tugallandi");
        System.out.println(k.getMalumot());
    }
}
```

## Tushuntirish va Mantiq:
249-topshiriqda obyekt maydonlarining inkapsulyatsiyasi, final xususiyatlar va holat o'zgarishi tahlil qilindi.
`id` maydoni `final` qilingani sababli bir marta berilgach o'zgarmaydi. `holat` maydoni esa xavfsiz metod orqali boshqariladi.

## Ishlash natijasi:
```text
Komponent #249 holati: Faol
Komponent #249 holati: Tugallandi
```

---

# 250-Topshiriq: Xulosa topshiriq: Elektron tijorat savatchasi va buyurtma modeli

## Topshiriq sharti:
Sinflar, obyektlar, inkapsulyatsiya, `record`, `equals`/`hashCode`, `toString` va kompozitsiyani birlashtirgan to'liq E-Commerce savatcha va buyurtma tizimini yarating.

## Yechim (Java kodi):
```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

public class Solution {
    public record Mahsulot(long id, String nom, double narx) {}

    static class SavatchaElementi {
        private final Mahsulot mahsulot;
        private int miqdor;

        public SavatchaElementi(Mahsulot mahsulot, int miqdor) {
            this.mahsulot = Objects.requireNonNull(mahsulot);
            this.miqdor = miqdor;
        }

        public Mahsulot getMahsulot() { return mahsulot; }
        public int getMiqdor() { return miqdor; }
        public void miqdorniOshir(int qoshimcha) { this.miqdor += qoshimcha; }
        public double jamiSumma() { return mahsulot.narx() * miqdor; }
    }

    static class Savatcha {
        private final List<SavatchaElementi> elementlar = new ArrayList<>();

        public void mahsulotQosh(Mahsulot m, int miqdor) {
            for (SavatchaElementi e : elementlar) {
                if (e.getMahsulot().equals(m)) {
                    e.miqdorniOshir(miqdor);
                    return;
                }
            }
            elementlar.add(new SavatchaElementi(m, miqdor));
        }

        public double jamiHisob() {
            double total = 0;
            for (SavatchaElementi e : elementlar) total += e.jamiSumma();
            return total;
        }

        public List<SavatchaElementi> getElementlar() {
            return Collections.unmodifiableList(elementlar);
        }
    }

    public static void main(String[] args) {
        Mahsulot telefon = new Mahsulot(1L, "Smartphone", 3500000.0);
        Mahsulot quloqchin = new Mahsulot(2L, "Quloqchin", 300000.0);

        Savatcha savat = new Savatcha();
        savat.mahsulotQosh(telefon, 1);
        savat.mahsulotQosh(quloqchin, 2);
        savat.mahsulotQosh(telefon, 1); // Miqdor oshadi

        System.out.println("=== XARID SAVATCHASI ===");
        for (SavatchaElementi e : savat.getElementlar()) {
            System.out.printf("- %-12s: %d dona x %.1f = %.1f so'm
",
                    e.getMahsulot().nom(), e.getMiqdor(), e.getMahsulot().narx(), e.jamiSumma());
        }
        System.out.println("----------------------------------------");
        System.out.printf("JAMI TO'LOV: %.1f so'm
", savat.jamiHisob());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu keng qamrovli topshiriqda:
1. `Mahsulot` modeli Java 16 `record` orqali o'zgarmas ma'lumotlar strukturasida qurildi.
2. `SavatchaElementi` mahsulot va miqdorni inkapsulyatsiya qildi.
3. `Savatcha` ro'yxatni boshqarib, bir xil tovar qayta kiritilganda uning miqdorini oshirdi.
4. `Collections.unmodifiableList()` orqali ichki holat tashqi modifikatsiyalardan himoyalandi.

## Ishlash natijasi:
```text
=== XARID SAVATCHASI ===
- Smartphone  : 2 dona x 3500000.0 = 7000000.0 so'm
- Quloqchin    : 2 dona x 300000.0 = 600000.0 so'm
----------------------------------------
JAMI TO'LOV: 7600000.0 so'm
```
