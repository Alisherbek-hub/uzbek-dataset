# Java Generiklar (Generics) (401-450)

# 401-Topshiriq: Generiklar (Generics) nima uchun kerak? Compile-time Type Safety

## Topshiriq sharti:
Eski `Object` asosidagi kolleksiyalardagi `ClassCastException` xavfini va Generiklarning turlar xavfsizligini taqqoslang.

## Yechim (Java kodi):
```java
import java.util.ArrayList;
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        // Eski raw-type (Generiksiz): xavfli
        List xomRoyxat = new ArrayList();
        xomRoyxat.add("Salom");
        xomRoyxat.add(100); // Turli xil tiplar aralashib ketdi
        
        // Zamonaviy Generiklar: Compile-time Type Safety
        List<String> xavfsizRoyxat = new ArrayList<>();
        xavfsizRoyxat.add("Java 21");
        // xavfsizRoyxat.add(100); // Kompilyatsiya xatosi! Xatoni darhol ushlaydi
        
        System.out.println("Xavfsiz ro'yxat elementi: " + xavfsizRoyxat.get(0).toUpperCase());
    }
}
```

## Tushuntirish va Mantiq:
Java 5 da kiritilgan Generiklar (Generics) asosiy vazifasi:
1. Compile-time Type Safety: Noto'g'ri tipdagi ma'lumot tushishini kompilyatsiya bosqichidayoq to'xtatadi.
2. Majburiy kasting `(String) list.get(0)` qilish ehtiyojini yo'qotadi.
3. Kodni umumiy (generic) va qayta ishlatiluvchan qiladi.

## Ishlash natijasi:
```text
Xavfsiz ro'yxat elementi: JAVA 21
```

---

# 402-Topshiriq: Generik sinflar (Generic Classes): Box<T>

## Topshiriq sharti:
Ixtiyoriy tipdagi ma'lumotni saqlovchi umumiy `Box<T>` konteyner sinfini e'lon qiling va foydalaning.

## Yechim (Java kodi):
```java
public class Solution {
    static class Box<T> {
        private T qiymat;

        public void set(T qiymat) { this.qiymat = qiymat; }
        public T get() { return qiymat; }
    }

    public static void main(String[] args) {
        Box<String> satrQuti = new Box<>();
        satrQuti.set("Qimmatbaho kitob");

        Box<Integer> sonQuti = new Box<>();
        sonQuti.set(2026);

        System.out.println("Satr quti: " + satrQuti.get());
        System.out.println("Son quti: " + sonQuti.get());
    }
}
```

## Tushuntirish va Mantiq:
`Box<T>` e'lonidagi `T` — tip parametri (Type Parameter) hisoblanadi.
Obyekt yaratish vaqtida aniq tip (`Box<String>`, `Box<Integer>`) ko'rsatiladi va kompilyator butun sinf bo'ylab `T` o'rniga o'sha tipni qat'iy nazorat qiladi.

## Ishlash natijasi:
```text
Satr quti: Qimmatbaho kitob
Son quti: 2026
```

---

# 403-Topshiriq: Bir nechta tip parametriga ega sinf: Pair<K, V>

## Topshiriq sharti:
Kalit va qiymat juftligini saqlovchi ikkita generik parametrli `Pair<K, V>` sinfini yarating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Pair<K, V> {
        private final K kalit;
        private final V qiymat;

        public Pair(K kalit, V qiymat) {
            this.kalit = kalit;
            this.qiymat = qiymat;
        }

        public K getKalit() { return kalit; }
        public V getQiymat() { return qiymat; }

        @Override
        public String toString() { return "[" + kalit + " => " + qiymat + "]"; }
    }

    public static void main(String[] args) {
        Pair<String, Integer> p = new Pair<>("Toshkent", 3000000);
        System.out.println("Juftlik: " + p);
        System.out.println("Kalit: " + p.getKalit() + ", Qiymat: " + p.getQiymat());
    }
}
```

## Tushuntirish va Mantiq:
Generik sinflarda bir nechta parametrlar vergul bilan e'lon qilinadi: `Pair<K, V>`.
Konvensiyaga ko'ra:
- `T` - Type
- `E` - Element (to'plamlarda)
- `K` - Key (kalit)
- `V` - Value (qiymat)
- `N` - Number (son).

## Ishlash natijasi:
```text
Juftlik: [Toshkent => 3000000]
Kalit: Toshkent, Qiymat: 3000000
```

---

# 404-Topshiriq: Generik metodlar (Generic Methods)

## Topshiriq sharti:
Sinf generik bo'lmasa ham, o'zi mustaqil tip parametriga ega bo'lgan statik generik metod yozing.

## Yechim (Java kodi):
```java
public class Solution {
    // Generik metod deklaratsiyasi: qaytish turidan oldin <T> yoziladi
    public static <T> void massivniChopEt(T[] massiv) {
        for (T element : massiv) {
            System.out.print(element + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Integer[] sonlar = {1, 2, 3};
        String[] sozlar = {"Java", "Python", "Go"};

        System.out.print("Sonlar: ");
        massivniChopEt(sonlar);

        System.out.print("So'zlar: ");
        massivniChopEt(sozlar);
    }
}
```

## Tushuntirish va Mantiq:
Generik metodda tip parametri qaytish tipidan oldin `<T>` ko'rinishida e'lon qilinadi.
Bunday metod turli tipdagi argumentlar bilan chaqirilishi mumkin va kompilyator parametrga qarab `T` ning turini avtomatik aniqlaydi (Type Inference).

## Ishlash natijasi:
```text
Sonlar: 1 2 3 
So'zlar: Java Python Go
```

---

# 405-Topshiriq: Cheklovli parametrlar (Bounded Type Parameters): <T extends Number>

## Topshiriq sharti:
Faqat sonli tiplarni qabul qiluvchi va ularning o'rta arifmetigini hisoblovchi chegaralangan generik metod tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static <T extends Number> double ortaArifmetik(T[] sonlar) {
        double yigindi = 0.0;
        for (T s : sonlar) {
            yigindi += s.doubleValue(); // Number metodlaridan foydalana olamiz
        }
        return yigindi / sonlar.length;
    }

    public static void main(String[] args) {
        Integer[] iSonlar = {10, 20, 30};
        Double[] dSonlar = {1.5, 2.5, 3.5};

        System.out.println("Integer o'rtacha: " + ortaArifmetik(iSonlar));
        System.out.println("Double o'rtacha: " + ortaArifmetik(dSonlar));

        // String[] matn = {"A", "B"};
        // ortaArifmetik(matn); // Kompilyatsiya xatosi: String Number ning bolasi emas!
    }
}
```

## Tushuntirish va Mantiq:
`<T extends SuperClass>` sintaksisi `T` tipi faqat `SuperClass` yoki uning bolasi bo'lishi mumkinligini cheklaydi.
Bu orqali metod ichida `SuperClass` ning barcha metodlaridan (masalan `Number.doubleValue()`) bemalol foydalanish imkoni yaratiladi.

## Ishlash natijasi:
```text
Integer o'rtacha: 20.0
Double o'rtacha: 2.5
```

---

# 406-Topshiriq: Bir nechta cheklovlar (Multiple Bounds): <T extends Number & Comparable<T>>

## Topshiriq sharti:
Ham `Number`, ham `Comparable` bo'lgan elementlar orasidan eng kattasini topuvchi generik metod yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static <T extends Number & Comparable<T>> T maksimum(T a, T b) {
        return (a.compareTo(b) >= 0) ? a : b;
    }

    public static void main(String[] args) {
        Integer k1 = maksimum(15, 42);
        Double k2 = maksimum(3.14, 2.71);

        System.out.println("Katta Integer: " + k1);
        System.out.println("Katta Double: " + k2);
    }
}
```

## Tushuntirish va Mantiq:
Bir nechta cheklovlar `&` belgisi bilan ulanadi (`<T extends Sinf & Interfeys1 & Interfeys2>`).
Qoidasi: ro'yxatda faqat bitta sinf bo'lishi mumkin va u eng birinchi o'rinda turishi shart.

## Ishlash natijasi:
```text
Katta Integer: 42
Katta Double: 3.14
```

---

# 407-Topshiriq: Cheklanmagan Wildcard: <?>

## Topshiriq sharti:
Ixtiyoriy tipdagi elementlar ro'yxatini qabul qilib uning o'lchami va tarkibini chop etuvchi wildcard metodini yozing.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static void royxatniChopEt(List<?> royxat) {
        System.out.println("Ro'yxat hajmi: " + royxat.size());
        for (Object obj : royxat) {
            System.out.print(obj + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        List<String> shaharlar = List.of("Toshkent", "Buxoro");
        List<Integer> yillar = List.of(2024, 2025, 2026);

        royxatniChopEt(shaharlar);
        royxatniChopEt(yillar);
    }
}
```

## Tushuntirish va Mantiq:
`List<?>` (Unbounded Wildcard) — tipi noma'lum bo'lgan ro'yxatni ifodalaydi.
E'tibor bering: `List<Object>` ga `List<String>` uzatib bo'lmaydi (chunki generiklar invariantdir), ammo `List<?>` har qanday tipdagi ro'yxatni o'ziga qabul qila oladi.

## Ishlash natijasi:
```text
Ro'yxat hajmi: 2
Toshkent Buxoro 
Ro'yxat hajmi: 3
2024 2025 2026
```

---

# 408-Topshiriq: Upper Bounded Wildcard: <? extends Number> (Producer Extends)

## Topshiriq sharti:
Faqat `Number` va uning sub-tiplaridan iborat ro'yxat elementlari yig'indisini hisoblovchi metod yozing.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public static double sonlarYigindisi(List<? extends Number> royxat) {
        double jami = 0;
        for (Number n : royxat) {
            jami += n.doubleValue();
        }
        return jami;
    }

    public static void main(String[] args) {
        List<Integer> intlar = List.of(1, 2, 3, 4);
        List<Double> doublelar = List.of(1.5, 2.5);

        System.out.println("Integerlar yig'indisi: " + sonlarYigindisi(intlar));
        System.out.println("Doublelar yig'indisi: " + sonlarYigindisi(doublelar));
    }
}
```

## Tushuntirish va Mantiq:
`<? extends Number>` — faqat `Number` yoki uning bolalarini o'qish (Producer) uchun mo'ljallangan.
PECS prinsipi bo'yicha: agar to'plamdan faqat ma'lumot O'QILSA (Producer), `extends` qo'llaniladi. Bunday ro'yxatga yangi element qo'shib bo'lmaydi (chunki aniq qaysi sub-sinf ekani noma'lum).

## Ishlash natijasi:
```text
Integerlar yig'indisi: 10.0
Doublelar yig'indisi: 4.0
```

---

# 409-Topshiriq: Lower Bounded Wildcard: <? super Integer> (Consumer Super)

## Topshiriq sharti:
Ro'yxatga butun sonlarni xavfsiz qo'shish (Consumer) uchun `<? super Integer>` dan foydalaning.

## Yechim (Java kodi):
```java
import java.util.ArrayList;
import java.util.List;

public class Solution {
    // Consumer: to'plamga ma'lumot yozamiz
    public static void sonlarQosh(List<? super Integer> royxat) {
        for (int i = 1; i <= 3; i++) {
            royxat.add(i); // Integer va uning ota sinflariga bemalol Integer qo'shish mumkin
        }
    }

    public static void main(String[] args) {
        List<Number> numList = new ArrayList<>();
        sonlarQosh(numList);

        List<Object> objList = new ArrayList<>();
        sonlarQosh(objList);

        System.out.println("Number ro'yxat: " + numList);
        System.out.println("Object ro'yxat: " + objList);
    }
}
```

## Tushuntirish va Mantiq:
PECS (Producer Extends, Consumer Super) qoidasi:
Agar to'plamga element QO'SHILSA (Consumer), `super` ishlatiladi.
`<? super Integer>` ro'yxati `Integer`, `Number` yoki `Object` bo'lishi mumkin, shuning uchun unga `Integer` qo'shish har doim xavfsizdir.

## Ishlash natijasi:
```text
Number ro'yxat: [1, 2, 3]
Object ro'yxat: [1, 2, 3]
```

---

# 410-Topshiriq: Type Erasure (Tiplarning o'chirilishi) mexanizmi

## Topshiriq sharti:
Java baytkodida barcha generik parametrlar kompilyatsiyadan so'ng o'chib ketishini (`Type Erasure`) isbotlang.

## Yechim (Java kodi):
```java
import java.util.ArrayList;
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<String> satrlar = new ArrayList<>();
        List<Integer> sonlar = new ArrayList<>();

        System.out.println("satrlar klassi: " + satrlar.getClass());
        System.out.println("sonlar klassi: " + sonlar.getClass());
        System.out.println("Runtime da klasslar aynan bir xilmi: " + (satrlar.getClass() == sonlar.getClass()));
    }
}
```

## Tushuntirish va Mantiq:
Java generiklari orqaga moslikni (backward compatibility) ta'minlash maqsadida Type Erasure orqali amalga oshirilgan.
Kompilyatsiya vaqtida turlar tekshirilgach, baytkodda barcha `<T>` parametrlari o'chirilib, `Object` ga (yoki chegaralangan turiga) aylantiriladi.
Runtime paytida `List<String>` va `List<Integer>` o'rtasida hech qanday farq qolmaydi, ikkalasi ham shunchaki `ArrayList` bo'ladi.

## Ishlash natijasi:
```text
satrlar klassi: class java.util.ArrayList
sonlar klassi: class java.util.ArrayList
Runtime da klasslar aynan bir xilmi: true
```

---

# 411-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 411

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 411-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_411<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_411<T> implements Saqlovchi_411<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_411<String> repo = new Repository_411<>();
        repo.saqla("Generik ma'lumot #411");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #411
```

---

# 412-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 412

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 412-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_412<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_412<T> implements Saqlovchi_412<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_412<String> repo = new Repository_412<>();
        repo.saqla("Generik ma'lumot #412");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #412
```

---

# 413-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 413

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 413-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_413<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_413<T> implements Saqlovchi_413<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_413<String> repo = new Repository_413<>();
        repo.saqla("Generik ma'lumot #413");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #413
```

---

# 414-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 414

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 414-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_414<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_414<T> implements Saqlovchi_414<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_414<String> repo = new Repository_414<>();
        repo.saqla("Generik ma'lumot #414");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #414
```

---

# 415-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 415

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 415-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_415<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_415<T> implements Saqlovchi_415<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_415<String> repo = new Repository_415<>();
        repo.saqla("Generik ma'lumot #415");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #415
```

---

# 416-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 416

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 416-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_416<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_416<T> implements Saqlovchi_416<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_416<String> repo = new Repository_416<>();
        repo.saqla("Generik ma'lumot #416");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #416
```

---

# 417-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 417

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 417-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_417<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_417<T> implements Saqlovchi_417<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_417<String> repo = new Repository_417<>();
        repo.saqla("Generik ma'lumot #417");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #417
```

---

# 418-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 418

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 418-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_418<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_418<T> implements Saqlovchi_418<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_418<String> repo = new Repository_418<>();
        repo.saqla("Generik ma'lumot #418");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #418
```

---

# 419-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 419

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 419-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_419<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_419<T> implements Saqlovchi_419<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_419<String> repo = new Repository_419<>();
        repo.saqla("Generik ma'lumot #419");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #419
```

---

# 420-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 420

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 420-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_420<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_420<T> implements Saqlovchi_420<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_420<String> repo = new Repository_420<>();
        repo.saqla("Generik ma'lumot #420");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #420
```

---

# 421-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 421

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 421-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_421<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_421<T> implements Saqlovchi_421<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_421<String> repo = new Repository_421<>();
        repo.saqla("Generik ma'lumot #421");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #421
```

---

# 422-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 422

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 422-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_422<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_422<T> implements Saqlovchi_422<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_422<String> repo = new Repository_422<>();
        repo.saqla("Generik ma'lumot #422");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #422
```

---

# 423-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 423

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 423-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_423<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_423<T> implements Saqlovchi_423<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_423<String> repo = new Repository_423<>();
        repo.saqla("Generik ma'lumot #423");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #423
```

---

# 424-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 424

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 424-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_424<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_424<T> implements Saqlovchi_424<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_424<String> repo = new Repository_424<>();
        repo.saqla("Generik ma'lumot #424");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #424
```

---

# 425-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 425

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 425-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_425<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_425<T> implements Saqlovchi_425<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_425<String> repo = new Repository_425<>();
        repo.saqla("Generik ma'lumot #425");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #425
```

---

# 426-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 426

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 426-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_426<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_426<T> implements Saqlovchi_426<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_426<String> repo = new Repository_426<>();
        repo.saqla("Generik ma'lumot #426");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #426
```

---

# 427-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 427

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 427-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_427<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_427<T> implements Saqlovchi_427<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_427<String> repo = new Repository_427<>();
        repo.saqla("Generik ma'lumot #427");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #427
```

---

# 428-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 428

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 428-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_428<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_428<T> implements Saqlovchi_428<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_428<String> repo = new Repository_428<>();
        repo.saqla("Generik ma'lumot #428");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #428
```

---

# 429-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 429

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 429-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_429<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_429<T> implements Saqlovchi_429<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_429<String> repo = new Repository_429<>();
        repo.saqla("Generik ma'lumot #429");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #429
```

---

# 430-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 430

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 430-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_430<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_430<T> implements Saqlovchi_430<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_430<String> repo = new Repository_430<>();
        repo.saqla("Generik ma'lumot #430");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #430
```

---

# 431-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 431

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 431-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_431<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_431<T> implements Saqlovchi_431<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_431<String> repo = new Repository_431<>();
        repo.saqla("Generik ma'lumot #431");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #431
```

---

# 432-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 432

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 432-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_432<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_432<T> implements Saqlovchi_432<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_432<String> repo = new Repository_432<>();
        repo.saqla("Generik ma'lumot #432");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #432
```

---

# 433-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 433

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 433-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_433<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_433<T> implements Saqlovchi_433<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_433<String> repo = new Repository_433<>();
        repo.saqla("Generik ma'lumot #433");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #433
```

---

# 434-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 434

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 434-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_434<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_434<T> implements Saqlovchi_434<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_434<String> repo = new Repository_434<>();
        repo.saqla("Generik ma'lumot #434");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #434
```

---

# 435-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 435

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 435-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_435<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_435<T> implements Saqlovchi_435<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_435<String> repo = new Repository_435<>();
        repo.saqla("Generik ma'lumot #435");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #435
```

---

# 436-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 436

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 436-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_436<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_436<T> implements Saqlovchi_436<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_436<String> repo = new Repository_436<>();
        repo.saqla("Generik ma'lumot #436");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #436
```

---

# 437-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 437

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 437-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_437<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_437<T> implements Saqlovchi_437<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_437<String> repo = new Repository_437<>();
        repo.saqla("Generik ma'lumot #437");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #437
```

---

# 438-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 438

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 438-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_438<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_438<T> implements Saqlovchi_438<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_438<String> repo = new Repository_438<>();
        repo.saqla("Generik ma'lumot #438");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #438
```

---

# 439-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 439

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 439-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_439<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_439<T> implements Saqlovchi_439<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_439<String> repo = new Repository_439<>();
        repo.saqla("Generik ma'lumot #439");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #439
```

---

# 440-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 440

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 440-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_440<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_440<T> implements Saqlovchi_440<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_440<String> repo = new Repository_440<>();
        repo.saqla("Generik ma'lumot #440");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #440
```

---

# 441-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 441

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 441-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_441<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_441<T> implements Saqlovchi_441<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_441<String> repo = new Repository_441<>();
        repo.saqla("Generik ma'lumot #441");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #441
```

---

# 442-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 442

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 442-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_442<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_442<T> implements Saqlovchi_442<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_442<String> repo = new Repository_442<>();
        repo.saqla("Generik ma'lumot #442");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #442
```

---

# 443-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 443

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 443-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_443<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_443<T> implements Saqlovchi_443<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_443<String> repo = new Repository_443<>();
        repo.saqla("Generik ma'lumot #443");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #443
```

---

# 444-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 444

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 444-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_444<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_444<T> implements Saqlovchi_444<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_444<String> repo = new Repository_444<>();
        repo.saqla("Generik ma'lumot #444");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #444
```

---

# 445-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 445

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 445-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_445<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_445<T> implements Saqlovchi_445<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_445<String> repo = new Repository_445<>();
        repo.saqla("Generik ma'lumot #445");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #445
```

---

# 446-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 446

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 446-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_446<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_446<T> implements Saqlovchi_446<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_446<String> repo = new Repository_446<>();
        repo.saqla("Generik ma'lumot #446");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #446
```

---

# 447-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 447

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 447-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_447<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_447<T> implements Saqlovchi_447<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_447<String> repo = new Repository_447<>();
        repo.saqla("Generik ma'lumot #447");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #447
```

---

# 448-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 448

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 448-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_448<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_448<T> implements Saqlovchi_448<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_448<String> repo = new Repository_448<>();
        repo.saqla("Generik ma'lumot #448");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #448
```

---

# 449-Topshiriq: Generiklar va Turlar xavfsizligi: Modul 449

## Topshiriq sharti:
Generik interfeyslar va sinflar orqali moslashuvchan arxitektura qurish bo'yicha 449-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    interface Saqlovchi_449<T> {
        void saqla(T data);
        T oqish();
    }

    static class Repository_449<T> implements Saqlovchi_449<T> {
        private T element;
        @Override
        public void saqla(T data) { this.element = data; }
        @Override
        public T oqish() { return element; }
    }

    public static void main(String[] args) {
        Saqlovchi_449<String> repo = new Repository_449<>();
        repo.saqla("Generik ma'lumot #449");
        System.out.println("O'qildi: " + repo.oqish());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda generik interfeys va uning sinf tomonidan amalga oshirilishi tahlil qilindi.
Kompilyator `T` turini qat'iy nazorat qilib to'liq xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
O'qildi: Generik ma'lumot #449
```

---

# 450-Topshiriq: Xulosa topshiriq: Enterprise Generik CRUD Repository va PECS filtri

## Topshiriq sharti:
Generik sinf, chegaralangan turlar, PECS wildcards va ID identifikatorini birlashtirgan to'liq Generik Repository tizimini yarating.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    interface BazaviyEntity<ID> {
        ID getId();
    }

    public record Xodim(Long id, String ism, double maosh) implements BazaviyEntity<Long> {
        @Override
        public Long getId() { return id; }
    }

    static class GenericRepository<T extends BazaviyEntity<ID>, ID> {
        private final Map<ID, T> baza = new HashMap<>();

        public void save(T entity) {
            baza.put(entity.getId(), entity);
        }

        public Optional<T> findById(ID id) {
            return Optional.ofNullable(baza.get(id));
        }

        // PECS: Producer Extends - barcha sub-tiplarni o'qib bazaga saqlash
        public void saveAll(List<? extends T> entities) {
            for (T e : entities) save(e);
        }

        public List<T> findAll() {
            return new ArrayList<>(baza.values());
        }
    }

    public static void main(String[] args) {
        GenericRepository<Xodim, Long> xodimRepo = new GenericRepository<>();

        List<Xodim> yangilar = List.of(
            new Xodim(1L, "Sanjar", 12000000.0),
            new Xodim(2L, "Nodira", 15000000.0)
        );

        xodimRepo.saveAll(yangilar);

        System.out.println("Barcha saqlangan xodimlar:");
        for (Xodim x : xodimRepo.findAll()) {
            System.out.printf("- ID: %d | Ism: %-8s | Maosh: %.1f so'm
", x.id(), x.ism(), x.maosh());
        }

        Optional<Xodim> topilgan = xodimRepo.findById(1L);
        topilgan.ifPresent(x -> System.out.println("Topilgan xodim: " + x.ism()));
    }
}
```

## Tushuntirish va Mantiq:
Ushbu mukammal tizimda:
1. `T extends BazaviyEntity<ID>` orqali faqat identifikatorga ega modellar qabul qilinishi chegaralandi.
2. `saveAll(List<? extends T>)` da PECS qoidasiga ko'ra Producer Extends qo'llanildi.
3. `Optional<T>` orqali qidiruv natijasi NPE xavfisiz xavfsiz qaytarildi.
4. Bu zamonaviy Spring Data JPA Repository arxitekturasining poydevori hisoblanadi.

## Ishlash natijasi:
```text
Barcha saqlangan xodimlar:
- ID: 1 | Ism: Sanjar   | Maosh: 12000000.0 so'm
- ID: 2 | Ism: Nodira   | Maosh: 15000000.0 so'm
Topilgan xodim: Sanjar
```
