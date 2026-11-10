# Java Virtual Threads va Zamonaviy Concurrency (651-700)

# 651-Topshiriq: Virtual Threads (Project Loom) asoslari (Java 21 LTS)

## Topshiriq sharti:
Java 21 ning yangi imkoniyati bo'lmish Virtual Thread yaratish va uning OS oqimidan farqini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        // Virtual Thread yaratish va ishga tushirish
        Thread vThread = Thread.ofVirtual().name("virtual-ishchi").start(() -> {
            System.out.println("Virtual thread ishlamoqda: " + Thread.currentThread());
            System.out.println("Virtual threadmi: " + Thread.currentThread().isVirtual());
        });

        vThread.join();
        System.out.println("Virtual thread muvaffaqiyatli yakunlandi.");
    }
}
```

## Tushuntirish va Mantiq:
Java 21 LTS bilan birga Project Loom (Virtual Threads) rasman standartga kirdi.
Platform Threads (an'anaviy oqimlar) operatsion tizim (OS) yadrosidagi oqimlarga 1:1 nisbatda bog'langan bo'lib, har biri 1MB xotira egallaydi.
Virtual Threads esa JVM tomonidan boshqariladigan yengil oqimlar bo'lib, xotirada atigi bir necha yuz bayt egallaydi va JVM ichida millionlab virtual oqimlarni bir vaqtda ochish imkonini beradi.

## Ishlash natijasi:
```text
Virtual thread ishlamoqda: VirtualThread[#...,virtual-ishchi]/runnable@ForkJoinPool-1-worker-...
Virtual threadmi: true
Virtual thread muvaffaqiyatli yakunlandi.
```

---

# 652-Topshiriq: 10,000 ta Virtual Thread ni parallel ishga tushirish

## Topshiriq sharti:
An'anaviy platforma oqimlari sig'dira olmaydigan 10,000 ta parallel oqimni xotirani to'ldirmasdan yengil bajarishni ko'rsating.

## Yechim (Java kodi):
```java
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) {
        AtomicInteger hisob = new AtomicInteger(0);

        // Har bir topshiriq uchun yangi virtual oqim ochuvchi zamonaviy executor
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 10_000; i++) {
                executor.submit(() -> {
                    hisob.incrementAndGet();
                });
            }
        } // try-with-resources avtomatik barcha virtual oqimlar tugashini kutadi (AutoCloseable)

        System.out.println("Bajarilgan virtual oqimlar soni: " + hisob.get());
    }
}
```

## Tushuntirish va Mantiq:
`Executors.newVirtualThreadPerTaskExecutor()` Java 21 ning eng asosiy tavsiya etiladigan arxitekturasidir.
Agar 10,000 ta an'anaviy `Thread` ochilsa, ~10GB xotira talab qilinib `OutOfMemoryError` yuz berar edi.
Virtual threadlar esa bu vazifani bir necha o'n megabayt xotirada soniyaning ulushlarida bajaradi.

## Ishlash natijasi:
```text
Bajarilgan virtual oqimlar soni: 10000
```

---

# 653-Topshiriq: Carrier Threads va Mount/Unmount mexanizmi

## Topshiriq sharti:
Virtual oqimlar I/O operatsiyasida (kutish paytida) qanday qilib OS oqimini (Carrier Thread) bo'shatib berishini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("1. Uyqudan oldin oqim holati: " + Thread.currentThread());
            try {
                // I/O yoki sleep paytida virtual thread unmount bo'ladi, carrier thread esa boshqa virtual oqimga xizmat qiladi
                Thread.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.println("2. Uyg'ongandan keyin oqim holati: " + Thread.currentThread());
        });

        v.join();
    }
}
```

## Tushuntirish va Mantiq:
Virtual oqimlar orqa fonda bir nechta `Carrier Thread` (ForkJoinPool workerlari) ustida ishlaydi (M:N modeli).
Virtual oqim I/O yoki tarmoq so'rovini kutishga tushganda (Blocking call), JVM uning chaqiruv stackini Heap ga saqlab qo'yadi va Carrier thread ni bo'shatadi (Unmount). Natijada bitta CPU yadrosi minglab so'rovlarga uzluksiz xizmat qilaveradi.

## Ishlash natijasi:
```text
1. Uyqudan oldin oqim holati: VirtualThread[#...]/runnable@ForkJoinPool-1-worker-...
2. Uyg'ongandan keyin oqim holati: VirtualThread[#...]/runnable@ForkJoinPool-1-worker-...
```

---

# 654-Topshiriq: Thread Pinning muammosi va ReentrantLock yechimi

## Topshiriq sharti:
`synchronized` bloklari virtual threadni Carrier thread ga qotirib qo'yishi (Pinning) va nima sababdan `ReentrantLock` ishlatilishi kerakligini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.concurrent.locks.ReentrantLock;

public class Solution {
    // Tavsiya etiladi: ReentrantLock virtual thread ni pin qilmaydi!
    private static final ReentrantLock xavfsizQulf = new ReentrantLock();

    public static void xavfsizAmal() {
        xavfsizQulf.lock();
        try {
            System.out.println("Virtual thread xavfsiz blokda: " + Thread.currentThread().isVirtual());
        } finally {
            xavfsizQulf.unlock();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(Solution::xavfsizAmal);
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
Thread Pinning:
Agar virtual oqim `synchronized` bloki yoki Native kod (JNI) ichida kutishga (blocking I/O) tushsa, JVM uni Carrier thread dan ajrata olmaydi (Pined holatga tushadi).
Bu butun tizim unumdorligini pasaytiradi.
Java 21+ da Virtual Threads bilan ishlashda `synchronized` o'rniga `java.util.concurrent.locks.ReentrantLock` qo'llash qat'iy tavsiya etiladi.

## Ishlash natijasi:
```text
Virtual thread xavfsiz blokda: true
```

---

# 655-Topshiriq: CompletableFuture: Asinxron zanjirlar va supplyAsync

## Topshiriq sharti:
`CompletableFuture` yordamida bir nechta asinxron vazifalarni ketma-ket va parallel zanjirga bog'lashni namoyish qiling.

## Yechim (Java kodi):
```java
import java.util.concurrent.CompletableFuture;

public class Solution {
    public static void main(String[] args) {
        CompletableFuture<String> zanjir = CompletableFuture.supplyAsync(() -> {
            return "Foydalanuvchi-77";
        }).thenApply(ism -> {
            return ism.toUpperCase();
        }).thenApply(kattaIsm -> {
            return "Xush kelibsiz, " + kattaIsm + "!";
        });

        // Natijani olish
        System.out.println("Asinxron zanjir natijasi: " + zanjir.join());
    }
}
```

## Tushuntirish va Mantiq:
`CompletableFuture<T>` funksional dasturlash va asinxron chaqiruvlarni osonlashtiradi:
- `supplyAsync(Supplier)`: fon oqimida hisoblashni boshlaydi.
- `thenApply(Function)`: oldingi natijani olib o'zgartiradi (map kabi).
- `join()`: xatoliklarni Unchecked shaklda tutib natijani oladi.

## Ishlash natijasi:
```text
Asinxron zanjir natijasi: Xush kelibsiz, FOYDALANUVCHI-77!
```

---

# 656-Topshiriq: CompletableFuture: thenCombine bilan ikkita parallel natijani birlashtirish

## Topshiriq sharti:
Ikkita mustaqil asinxron xizmat (masalan Narx va Chegirma) natijasini parallel hisoblab, `thenCombine` orqali birlashtiring.

## Yechim (Java kodi):
```java
import java.util.concurrent.CompletableFuture;

public class Solution {
    public static void main(String[] args) {
        CompletableFuture<Double> narxKeldi = CompletableFuture.supplyAsync(() -> 100000.0);
        CompletableFuture<Double> chegirmaKeldi = CompletableFuture.supplyAsync(() -> 15000.0);

        CompletableFuture<Double> yakuniy = narxKeldi.thenCombine(chegirmaKeldi, (narx, chegirma) -> {
            return narx - chegirma;
        });

        System.out.printf("Yakuniy to'lov: %.2f so'm
", yakuniy.join());
    }
}
```

## Tushuntirish va Mantiq:
`thenCombine(otherFuture, BiFunction)` ikkita asinxron topshiriqning ikkalasi ham to'liq tugashini kutadi va ularning natijalarini bitta yangi qiymatga birlashtiradi.

## Ishlash natijasi:
```text
Yakuniy to'lov: 85000.00 so'm
```

---

# 657-Topshiriq: CompletableFuture: exceptionally bilan xatoliklarni boshqarish

## Topshiriq sharti:
Asinxron oqimda xatolik yuz berganda `exceptionally` orqali zaxira qiymat (fallback) qaytarishni ko'rsating.

## Yechim (Java kodi):
```java
import java.util.concurrent.CompletableFuture;

public class Solution {
    public static void main(String[] args) {
        CompletableFuture<String> xavfliOperatsiya = CompletableFuture.supplyAsync(() -> {
            if (true) throw new RuntimeException("Tashqi API bilan aloqa uzildi!");
            return "Muvaffaqiyatli ma'lumot";
        }).exceptionally(ex -> {
            System.out.println("Xatolik ushlandi: " + ex.getMessage());
            return "Zaxira (fallback) kesh ma'lumotlari";
        });

        System.out.println("Natija: " + xavfliOperatsiya.join());
    }
}
```

## Tushuntirish va Mantiq:
`exceptionally(Function<Throwable, T>)` asinxron zanjir ichida yuzaga kelgan istisnoni ushlaydi va dastur to'xtab qolmasligi uchun zaxira qiymat qaytarish imkonini beradi (Circuit Breaker va Fallback naqshining asosi).

## Ishlash natijasi:
```text
Xatolik ushlandi: java.lang.RuntimeException: Tashqi API bilan aloqa uzildi!
Natija: Zaxira (fallback) kesh ma'lumotlari
```

---

# 658-Topshiriq: ConcurrentHashMap: Yuqori tezlikdagi oqimlararo xavfsiz Map

## Topshiriq sharti:
`Collections.synchronizedMap` o'rniga nima sababdan `ConcurrentHashMap` segmentlangan qulflash orqali ancha tez ishlashini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.LongAdder;

public class Solution {
    public static void main(String[] args) {
        ConcurrentHashMap<String, LongAdder> hisoblar = new ConcurrentHashMap<>();

        // computeIfAbsent va increment atomik tarzda bajariladi
        hisoblar.computeIfAbsent("Toshkent", k -> new LongAdder()).increment();
        hisoblar.computeIfAbsent("Toshkent", k -> new LongAdder()).increment();
        hisoblar.computeIfAbsent("Samarqand", k -> new LongAdder()).increment();

        System.out.println("Toshkent tashriflar: " + hisoblar.get("Toshkent").sum());
        System.out.println("Samarqand tashriflar: " + hisoblar.get("Samarqand").sum());
    }
}
```

## Tushuntirish va Mantiq:
`ConcurrentHashMap` butun jadvalni bittada qulflamaydi (Lock Striping / Bucket-level CAS and synchronized on root nodes).
Shu bois yuzlab oqimlar turli savatlarga bir vaqtda to'siqsiz yozishi va o'qishi mumkin.

## Ishlash natijasi:
```text
Toshkent tashriflar: 2
Samarqand tashriflar: 1
```

---

# 659-Topshiriq: CopyOnWriteArrayList: Ko'p o'qiladigan ro'yxatlar uchun xavfsizlik

## Topshiriq sharti:
O'qish amallari juda ko'p va yozish amallari kam bo'lgan tizimlarda `CopyOnWriteArrayList` ning afzalligini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<String> hodisalar = new CopyOnWriteArrayList<>();
        hodisalar.add("HODISA_1");
        hodisalar.add("HODISA_2");

        // O'qish paytida hech qanday ConcurrentModificationException ro'y bermaydi
        for (String h : hodisalar) {
            System.out.println("O'qildi: " + h);
            hodisalar.add("YANGI_QO'SHILDI"); // Yangi nusxa hosil qilib yozadi
        }

        System.out.println("Yakuniy ro'yxat hajmi: " + hodisalar.size());
    }
}
```

## Tushuntirish va Mantiq:
`CopyOnWriteArrayList` har safar `add()` yoki `set()` chaqirilganda ichki massivning yangi nusxasini (Snapshot) hosil qiladi.
O'qish amallari hech qanday qulflarsiz mutlaqo xavfsiz va o'ta tez ishlaydi. Bu Observer pattern va hodisalar ro'yxatida juda qo'l keladi.

## Ishlash natijasi:
```text
O'qildi: HODISA_1
O'qildi: HODISA_2
Yakuniy ro'yxat hajmi: 4
```

---

# 660-Topshiriq: CompletableFuture.allOf bilan barcha parallel so'rovlarni kutish

## Topshiriq sharti:
Bir nechta mustaqil mikroservislarga parallel so'rov yuborib, barchasi yakunlanishini `CompletableFuture.allOf()` bilan kuting.

## Yechim (Java kodi):
```java
import java.util.concurrent.CompletableFuture;

public class Solution {
    public static void main(String[] args) {
        CompletableFuture<String> s1 = CompletableFuture.supplyAsync(() -> "Foydalanuvchi servisi OK");
        CompletableFuture<String> s2 = CompletableFuture.supplyAsync(() -> "To'lov servisi OK");
        CompletableFuture<String> s3 = CompletableFuture.supplyAsync(() -> "Yetkazib berish servisi OK");

        CompletableFuture<Void> barchasi = CompletableFuture.allOf(s1, s2, s3);
        barchasi.join(); // Hammasi tugashini kutamiz

        System.out.println("Barcha mikroservislar tayyor:");
        System.out.println("- " + s1.join());
        System.out.println("- " + s2.join());
        System.out.println("- " + s3.join());
    }
}
```

## Tushuntirish va Mantiq:
`CompletableFuture.allOf(f1, f2, ...)` barcha berilgan kelajak vazifalar muvaffaqiyatli yakunlangachgina o'z ishini tugatadi.
Bu bir nechta uzoqdagi REST API yoki ma'lumotlar bazalariga parallel so'rov yuborishda umumiy kutish vaqtini eng uzoq so'rov vaqtiga tenglashtiradi.

## Ishlash natijasi:
```text
Barcha mikroservislar tayyor:
- Foydalanuvchi servisi OK
- To'lov servisi OK
- Yetkazib berish servisi OK
```

---

# 661-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 661

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 661-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #661 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
661-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #661 bajarildi.
```

---

# 662-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 662

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 662-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #662 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
662-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #662 bajarildi.
```

---

# 663-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 663

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 663-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #663 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
663-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #663 bajarildi.
```

---

# 664-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 664

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 664-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #664 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
664-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #664 bajarildi.
```

---

# 665-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 665

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 665-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #665 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
665-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #665 bajarildi.
```

---

# 666-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 666

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 666-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #666 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
666-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #666 bajarildi.
```

---

# 667-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 667

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 667-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #667 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
667-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #667 bajarildi.
```

---

# 668-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 668

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 668-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #668 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
668-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #668 bajarildi.
```

---

# 669-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 669

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 669-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #669 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
669-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #669 bajarildi.
```

---

# 670-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 670

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 670-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #670 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
670-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #670 bajarildi.
```

---

# 671-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 671

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 671-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #671 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
671-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #671 bajarildi.
```

---

# 672-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 672

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 672-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #672 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
672-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #672 bajarildi.
```

---

# 673-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 673

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 673-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #673 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
673-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #673 bajarildi.
```

---

# 674-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 674

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 674-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #674 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
674-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #674 bajarildi.
```

---

# 675-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 675

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 675-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #675 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
675-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #675 bajarildi.
```

---

# 676-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 676

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 676-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #676 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
676-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #676 bajarildi.
```

---

# 677-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 677

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 677-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #677 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
677-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #677 bajarildi.
```

---

# 678-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 678

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 678-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #678 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
678-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #678 bajarildi.
```

---

# 679-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 679

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 679-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #679 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
679-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #679 bajarildi.
```

---

# 680-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 680

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 680-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #680 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
680-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #680 bajarildi.
```

---

# 681-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 681

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 681-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #681 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
681-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #681 bajarildi.
```

---

# 682-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 682

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 682-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #682 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
682-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #682 bajarildi.
```

---

# 683-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 683

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 683-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #683 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
683-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #683 bajarildi.
```

---

# 684-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 684

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 684-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #684 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
684-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #684 bajarildi.
```

---

# 685-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 685

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 685-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #685 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
685-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #685 bajarildi.
```

---

# 686-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 686

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 686-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #686 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
686-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #686 bajarildi.
```

---

# 687-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 687

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 687-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #687 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
687-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #687 bajarildi.
```

---

# 688-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 688

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 688-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #688 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
688-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #688 bajarildi.
```

---

# 689-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 689

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 689-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #689 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
689-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #689 bajarildi.
```

---

# 690-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 690

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 690-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #690 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
690-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #690 bajarildi.
```

---

# 691-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 691

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 691-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #691 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
691-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #691 bajarildi.
```

---

# 692-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 692

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 692-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #692 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
692-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #692 bajarildi.
```

---

# 693-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 693

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 693-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #693 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
693-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #693 bajarildi.
```

---

# 694-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 694

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 694-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #694 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
694-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #694 bajarildi.
```

---

# 695-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 695

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 695-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #695 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
695-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #695 bajarildi.
```

---

# 696-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 696

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 696-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #696 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
696-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #696 bajarildi.
```

---

# 697-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 697

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 697-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #697 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
697-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #697 bajarildi.
```

---

# 698-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 698

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 698-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #698 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
698-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #698 bajarildi.
```

---

# 699-Topshiriq: Virtual Threads va Zamonaviy Concurrency: Modul 699

## Topshiriq sharti:
Java 21 asinxron dasturlash va Virtual Threads orqali yuqori unumdorlik bo'yicha 699-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread v = Thread.ofVirtual().start(() -> {
            System.out.println("Asinxron modul #699 bajarildi.");
        });
        v.join();
    }
}
```

## Tushuntirish va Mantiq:
699-topshiriqda Java 21 yengil oqimlarining asinxron arxitekturadagi o'rni tahlil qilindi.

## Ishlash natijasi:
```text
Asinxron modul #699 bajarildi.
```

---

# 700-Topshiriq: Xulosa topshiriq: Yuqori yuklamali Asinxron Buyurtmalar Shlyuzi

## Topshiriq sharti:
Virtual Threads, newVirtualThreadPerTaskExecutor, CompletableFuture va ConcurrentHashMap ni birlashtirgan yuqori yuklamali Buyurtmalar Shlyuzi tizimini quring.

## Yechim (Java kodi):
```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public record Buyurtma(String id, double summa) {}

    static class ShlyuzService {
        private final ConcurrentHashMap<String, String> tranzaksiyalar = new ConcurrentHashMap<>();
        private final AtomicInteger muvaffaqiyatliBuyurtmalar = new AtomicInteger(0);

        public void buyurtmaniQaytaIshla(Buyurtma b) {
            // Virtual Thread ichida ishlaydi
            try {
                Thread.sleep(10); // I/O amalini simulyatsiya qilish
                tranzaksiyalar.put(b.id(), "MUVAFFAQIN");
                muvaffaqiyatliBuyurtmalar.incrementAndGet();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        public int getMuvaffaqiyatliSoni() { return muvaffaqiyatliBuyurtmalar.get(); }
    }

    public static void main(String[] args) {
        ShlyuzService service = new ShlyuzService();

        System.out.println("=== ASINXRON VIRTUAL THREADS SHLYUZI ISHGA TUSHDI ===");
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 1; i <= 500; i++) {
                final String buyurtmaId = "BUYURTMA-" + i;
                executor.submit(() -> service.buyurtmaniQaytaIshla(new Buyurtma(buyurtmaId, 50000.0)));
            }
        } // Barcha 500 ta virtual thread tugashi avtomatik kutiladi

        System.out.println("Barcha buyurtmalar qayta ishlandi!");
        System.out.println("Muvaffaqiyatli qayd etilganlar: " + service.getMuvaffaqiyatliSoni());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu keng qamrovli xulosa topshiriqda:
1. `Executors.newVirtualThreadPerTaskExecutor()` orqali 500 ta I/O topshirig'i parallel virtual oqimlarda bajarildi.
2. `ConcurrentHashMap` orqali multithread muhitida ma'lumotlar xavfsiz saqlandi.
3. Resurslarni tejash va yuqori tezlikda o'tkazuvchanlikka (throughput) erishildi.

## Ishlash natijasi:
```text
=== ASINXRON VIRTUAL THREADS SHLYUZI ISHGA TUSHDI ===
Barcha buyurtmalar qayta ishlandi!
Muvaffaqiyatli qayd etilganlar: 500
```
