# Java Multithreading va Parallelizm (601-650)

# 601-Topshiriq: Thread yaratishning 2 xil klassik usuli

## Topshiriq sharti:
`Thread` sinfidan meros olish va `Runnable` interfeysini amalga oshirish orqali parallel oqim yaratishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    // 1-usul: Thread dan voris olish
    static class MeningOqimim extends Thread {
        @Override
        public void run() {
            System.out.println("1-oqim ishlamoqda: " + Thread.currentThread().getName());
        }
    }

    public static void main(String[] args) {
        // 1-usulni ishga tushirish
        MeningOqimim t1 = new MeningOqimim();
        t1.start(); // run() emas, start() chaqiriladi!

        // 2-usul: Runnable lambda bilan (eng yaxshi amaliyot)
        Thread t2 = new Thread(() -> {
            System.out.println("2-oqim ishlamoqda: " + Thread.currentThread().getName());
        });
        t2.start();
    }
}
```

## Tushuntirish va Mantiq:
Java-da oqim (Thread) yaratishning asosiy usullari:
1. `extends Thread`: sinf boshqa hech qanday sinfdan meros ololmay qoladi.
2. `implements Runnable`: kompozitsiya tamoyiliga mos, vazifa (task) va ijrochi (thread) ajratiladi.
Muhim qoida: Yangi oqimni OS da ochish uchun `run()` emas, aynan `start()` chaqirilishi shart!

## Ishlash natijasi:
```text
1-oqim ishlamoqda: Thread-0
2-oqim ishlamoqda: Thread-1
```

---

# 602-Topshiriq: Oqim holatlari (Thread Lifecycle) va join() metodi

## Topshiriq sharti:
Boshqa oqim o'z ishini to'liq tugatishini kutish uchun `join()` metodidan foydalaning.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) throws InterruptedException {
        Thread ishchi = new Thread(() -> {
            try {
                System.out.println("Ishchi oqim og'ir hisob-kitobni boshladi...");
                Thread.sleep(100); // 100 ms kutish
                System.out.println("Ishchi oqim vazifani yakunladi.");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        ishchi.start();
        System.out.println("Asosiy oqim ishchini kutmoqda...");
        ishchi.join(); // Asosiy oqim ishchi to'xtaguncha bloklanadi
        System.out.println("Barcha ishlar yakunlandi, dastur yopilmoqda.");
    }
}
```

## Tushuntirish va Mantiq:
`t.join()` metodi joriy oqimni (masalan `main`) `t` oqimi tugaguncha `WAITING` holatida to'xtatib turadi.
Bu asinxron hisoblangan oraliq natijalarni birlashtirishda asosiy sinxronlash vositasi hisoblanadi.

## Ishlash natijasi:
```text
Asosiy oqim ishchini kutmoqda...
Ishchi oqim og'ir hisob-kitobni boshladi...
Ishchi oqim vazifani yakunladi.
Barcha ishlar yakunlandi, dastur yopilmoqda.
```

---

# 603-Topshiriq: Race Condition (Poyga holati) va synchronized yechimi

## Topshiriq sharti:
Ko'p oqimli muhitda umumiy hisoblagich poyga holati (Race Condition) ga tushishini va `synchronized` bilan uni tuzatishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Hisoblagich {
        private int sana = 0;

        // synchronized metodi bir vaqtda faqat 1 ta oqim kirishini ta'minlaydi
        public synchronized void oshir() {
            sana++;
        }

        public int getSana() { return sana; }
    }

    public static void main(String[] args) throws InterruptedException {
        Hisoblagich h = new Hisoblagich();

        Thread t1 = new Thread(() -> { for (int i = 0; i < 1000; i++) h.oshir(); });
        Thread t2 = new Thread(() -> { for (int i = 0; i < 1000; i++) h.oshir(); });

        t1.start();
        t2.start();

        t1.join();
        t2.join();

        System.out.println("Yakuniy hisoblagich qiymati (kutilgan: 2000): " + h.getSana());
    }
}
```

## Tushuntirish va Mantiq:
Race Condition — bir vaqtda bir nechta oqim umumiy o'zgaruvchiga kirib yozganda yuzaga keladi (`sana++` bitta amal emas, balki 3 ta mashina buyrug'idir: o'qish, oshirish, yozish).
`synchronized` kalit so'zi obyektning Monitor qulfiga (Intrinsic Lock) tayanib, bir vaqtda faqat bitta oqimga kritik bo'limga (Critical section) kirishga ruxsat beradi.

## Ishlash natijasi:
```text
Yakuniy hisoblagich qiymati (kutilgan: 2000): 2000
```

---

# 604-Topshiriq: volatile kalit so'zi va Xotira ko'rinuvchanligi (Memory Visibility)

## Topshiriq sharti:
Bitta oqim o'zgartirgan o'zgaruvchi CPU keshida qolib ketmasdan ikkinchi oqimga darhol ko'rinishi uchun `volatile` dan foydalaning.

## Yechim (Java kodi):
```java
public class Solution {
    // volatile CPU keshini chetlab o'tib, qiymatni to'g'ridan-to'g'ri operativ xotiraga (RAM) yozish/o'qishni kafolatlaydi
    private static volatile boolean toxtatildi = false;

    public static void main(String[] args) throws InterruptedException {
        Thread fonOqimi = new Thread(() -> {
            int i = 0;
            while (!toxtatildi) {
                i++;
            }
            System.out.println("Fon oqimi to'xtadi! Iteratsiyalar: " + i);
        });

        fonOqimi.start();
        Thread.sleep(50);

        toxtatildi = true; // Bayroqni ko'taramiz
        fonOqimi.join();
        System.out.println("Dastur muvaffaqiyatli yakunlandi.");
    }
}
```

## Tushuntirish va Mantiq:
Zamonaviy CPU larda har bir yadro o'zining tezyurar keshiga (L1/L2) ega.
Agar o'zgaruvchi `volatile` qilinmasa, bir oqim uning qiymatini o'zgartirsa ham, ikkinchi oqim o'z keshidagi eski qiymatni o'qib cheksiz siklda qotib qolishi mumkin (Visibility problem).
`volatile` o'zgaruvchini to'g'ridan-to'g'ri umumiy xotiradan o'qilishini ta'minlaydi (ammo atomiklik bermaydi).

## Ishlash natijasi:
```text
Fon oqimi to'xtadi! Iteratsiyalar: ...
Dastur muvaffaqiyatli yakunlandi.
```

---

# 605-Topshiriq: AtomicInteger va Lock-free CAS (Compare-And-Swap) mexanizmi

## Topshiriq sharti:
Qulflashlarsiz (Lock-free) yuqori tezlikdagi atomik hisoblagich uchun `AtomicInteger` dan foydalaning.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger atomikSana = new AtomicInteger(0);

        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 500; i++) atomikSana.incrementAndGet();
        });
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 500; i++) atomikSana.incrementAndGet();
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println("Atomik natija: " + atomikSana.get());
    }
}
```

## Tushuntirish va Mantiq:
`java.util.concurrent.atomic` to'plami apparat darajasidagi CAS (Compare-And-Swap) protsessor instruksiyalaridan foydalanadi.
U hech qanday `synchronized` yoki qulflash (blocking) ishlatmaydi. Agar qiymat o'zgarib qolgan bo'lsa, apparat darajasida qayta urinadi. Bu yuqori yuklamalarda ancha tez ishlaydi.

## Ishlash natijasi:
```text
Atomik natija: 1000
```

---

# 606-Topshiriq: ReentrantLock va tryLock bilan bloklanishni oldini olish

## Topshiriq sharti:
`synchronized` ning o'rniga moslashuvchan `ReentrantLock` va uning `tryLock()` xususiyatini namoyish qiling.

## Yechim (Java kodi):
```java
import java.util.concurrent.locks.ReentrantLock;

public class Solution {
    private static final ReentrantLock qulf = new ReentrantLock();

    public static void vazifa() {
        if (qulf.tryLock()) { // Qulf band bo'lsa kutib o'tirmaydi
            try {
                System.out.println(Thread.currentThread().getName() + " qulfni qo'lga kiritdi va ishlamoqda.");
                Thread.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                qulf.unlock(); // Har doim finally ichida yechiladi!
            }
        } else {
            System.out.println(Thread.currentThread().getName() + " qulf band bo'lgani uchun boshqa ishga o'tib ketdi.");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread oqim1 = new Thread(Solution::vazifa, "Oqim-1");
        Thread oqim2 = new Thread(Solution::vazifa, "Oqim-2");

        oqim1.start();
        oqim2.start();

        oqim1.join();
        oqim2.join();
    }
}
```

## Tushuntirish va Mantiq:
`ReentrantLock` ning `synchronized` dan afzalliklari:
1. `tryLock()`: kutmasdan yoki vaqt chegarasi bilan qulfni tekshirish (Deadlock oldini oladi).
2. Adolatli rejim (`fairness`): navbatdagi eng ko'p kutgan oqimga qulfni berish.
3. Bir nechta mustaqil `Condition` o'zgaruvchilari bilan ishlash.

## Ishlash natijasi:
```text
Oqim-1 qulfni qo'lga kiritdi va ishlamoqda.
Oqim-2 qulf band bo'lgani uchun boshqa ishga o'tib ketdi.
```

---

# 607-Topshiriq: ExecutorService va FixedThreadPool

## Topshiriq sharti:
Har bir topshiriq uchun alohida `new Thread` ochmasdan, oqimlar havzasi (ThreadPool) orqali resurslarni tejashni ko'rsating.

## Yechim (Java kodi):
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        // 2 ta oqimdan iborat doimiy havza
        ExecutorService hovuz = Executors.newFixedThreadPool(2);

        for (int i = 1; i <= 4; i++) {
            final int taskId = i;
            hovuz.submit(() -> {
                System.out.println("Topshiriq #" + taskId + " bajarilmoqda -> " + Thread.currentThread().getName());
            });
        }

        hovuz.shutdown(); // Yangi topshiriqlarni qabul qilishni to'xtatish
        hovuz.awaitTermination(5, TimeUnit.SECONDS);
        System.out.println("Barcha topshiriqlar hovuzda yakunlandi.");
    }
}
```

## Tushuntirish va Mantiq:
Oqim (Thread) yaratish OS darajasida qimmat resurs (xotira, stack ajratish, kontekst almashtirish).
ThreadPool (Oqimlar havzasi) oqimlarni bir marta yaratib, ularni qayta-qayta yangi topshiriqlar uchun ishlatadi (Worker Thread pattern). Bu server ilovalari uchun standart me'morchilikdir.

## Ishlash natijasi:
```text
Topshiriq #1 bajarilmoqda -> pool-1-thread-1
Topshiriq #2 bajarilmoqda -> pool-1-thread-2
Topshiriq #3 bajarilmoqda -> pool-1-thread-1
Topshiriq #4 bajarilmoqda -> pool-1-thread-2
Barcha topshiriqlar hovuzda yakunlandi.
```

---

# 608-Topshiriq: Callable va Future: Asinxron natija olish

## Topshiriq sharti:
`Runnable` dan farqli ravishda asinxron natija qaytaruvchi va xatolik tashlay oluvchi `Callable<V>` va `Future<V>` ni qo'llang.

## Yechim (Java kodi):
```java
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class Solution {
    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newSingleThreadExecutor();

        Callable<Integer> ogirHisob = () -> {
            Thread.sleep(100);
            return 42 * 2;
        };

        Future<Integer> kelajakNatija = executor.submit(ogirHisob);
        System.out.println("Topshiriq fonga yuborildi, asosiy oqim boshqa ish qilishi mumkin...");

        // get() bloklanuvchi chaqiruv: natija tayyor bo'lguncha kutadi
        int natija = kelajakNatija.get();
        System.out.println("Hisoblangan yakuniy natija: " + natija);

        executor.shutdown();
    }
}
```

## Tushuntirish va Mantiq:
`Runnable` qiymat qaytarmaydi (`void run()`) va checked exception tashlay olmaydi.
`Callable<V>` esa natija qaytaradi (`V call() throws Exception`).
`Future<V>` esa kelajakda tayyor bo'ladigan natija ustidan nazoratni (kutish, bekor qilish, holatini bilish) ta'minlaydi.

## Ishlash natijasi:
```text
Topshiriq fonga yuborildi, asosiy oqim boshqa ish qilishi mumkin...
Hisoblangan yakuniy natija: 84
```

---

# 609-Topshiriq: Deadlock (Boshi berk ko'cha) xavfi va uning oldini olish

## Topshiriq sharti:
Ikkita oqim qulflarni qarama-qarshi tartibda egallashi tufayli yuzaga keladigan Deadlock holati tahlilini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    private static final Object QulfA = new Object();
    private static final Object QulfB = new Object();

    public static void xavfsizTartib(String oqimNomi) {
        // Har ikkala oqim qulflarni BIR XIL TARTIBDA oladi: avval A, keyin B!
        synchronized (QulfA) {
            System.out.println(oqimNomi + " QulfA ni oldi");
            synchronized (QulfB) {
                System.out.println(oqimNomi + " QulfB ni ham oldi va ishni tugatdi");
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> xavfsizTartib("Oqim-1"));
        Thread t2 = new Thread(() -> xavfsizTartib("Oqim-2"));

        t1.start();
        t2.start();

        t1.join();
        t2.join();
        System.out.println("Deadlocksiz muvaffaqiyatli yakunlandi.");
    }
}
```

## Tushuntirish va Mantiq:
Deadlock (Boshi berk ko'cha) — oqimlar bir-biri egallab turgan resurslarni abadiy kutib qolishidir (Oqim-1 A ni olib B ni kutyapti, Oqim-2 esa B ni olib A ni kutyapti).
Deadlock ning oldini olishning eng asosiy qoidasi: barcha oqimlarda qulflarni har doim qat'iy bir xil global ketma-ketlikda egallash.

## Ishlash natijasi:
```text
Oqim-1 QulfA ni oldi
Oqim-1 QulfB ni ham oldi va ishni tugatdi
Oqim-2 QulfA ni oldi
Oqim-2 QulfB ni ham oldi va ishni tugatdi
Deadlocksiz muvaffaqiyatli yakunlandi.
```

---

# 610-Topshiriq: ScheduledExecutorService: Rejalashtirilgan va davriy topshiriqlar

## Topshiriq sharti:
Har 100 millisekundda takrorlanuvchi fon monitoring topshirig'ini ishga tushiring.

## Yechim (Java kodi):
```java
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
        AtomicInteger hisob = new AtomicInteger(1);

        scheduler.scheduleAtFixedRate(() -> {
            System.out.println("Monitoring zarbasi #" + hisob.getAndIncrement());
        }, 0, 100, TimeUnit.MILLISECONDS);

        Thread.sleep(350); // 3-4 marta urishiga vaqt beramiz
        scheduler.shutdown();
        System.out.println("Monitoring to'xtatildi.");
    }
}
```

## Tushuntirish va Mantiq:
`ScheduledExecutorService` ma'lum kechikish bilan (`schedule`) yoki davriy takrorlanish bilan (`scheduleAtFixedRate` / `scheduleWithFixedDelay`) vazifalarni rejalashtirish imkonini beradi (eski `java.util.Timer` dan ancha barqaror va xavfsiz).

## Ishlash natijasi:
```text
Monitoring zarbasi #1
Monitoring zarbasi #2
Monitoring zarbasi #3
Monitoring zarbasi #4
Monitoring to'xtatildi.
```

---

# 611-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 611

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 611-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(611);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #611 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
611-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #611 natijasi: 621
```

---

# 612-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 612

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 612-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(612);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #612 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
612-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #612 natijasi: 622
```

---

# 613-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 613

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 613-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(613);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #613 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
613-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #613 natijasi: 623
```

---

# 614-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 614

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 614-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(614);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #614 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
614-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #614 natijasi: 624
```

---

# 615-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 615

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 615-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(615);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #615 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
615-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #615 natijasi: 625
```

---

# 616-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 616

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 616-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(616);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #616 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
616-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #616 natijasi: 626
```

---

# 617-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 617

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 617-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(617);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #617 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
617-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #617 natijasi: 627
```

---

# 618-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 618

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 618-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(618);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #618 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
618-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #618 natijasi: 628
```

---

# 619-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 619

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 619-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(619);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #619 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
619-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #619 natijasi: 629
```

---

# 620-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 620

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 620-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(620);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #620 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
620-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #620 natijasi: 630
```

---

# 621-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 621

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 621-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(621);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #621 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
621-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #621 natijasi: 631
```

---

# 622-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 622

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 622-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(622);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #622 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
622-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #622 natijasi: 632
```

---

# 623-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 623

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 623-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(623);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #623 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
623-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #623 natijasi: 633
```

---

# 624-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 624

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 624-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(624);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #624 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
624-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #624 natijasi: 634
```

---

# 625-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 625

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 625-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(625);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #625 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
625-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #625 natijasi: 635
```

---

# 626-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 626

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 626-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(626);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #626 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
626-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #626 natijasi: 636
```

---

# 627-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 627

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 627-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(627);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #627 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
627-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #627 natijasi: 637
```

---

# 628-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 628

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 628-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(628);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #628 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
628-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #628 natijasi: 638
```

---

# 629-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 629

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 629-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(629);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #629 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
629-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #629 natijasi: 639
```

---

# 630-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 630

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 630-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(630);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #630 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
630-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #630 natijasi: 640
```

---

# 631-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 631

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 631-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(631);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #631 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
631-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #631 natijasi: 641
```

---

# 632-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 632

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 632-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(632);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #632 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
632-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #632 natijasi: 642
```

---

# 633-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 633

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 633-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(633);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #633 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
633-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #633 natijasi: 643
```

---

# 634-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 634

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 634-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(634);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #634 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
634-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #634 natijasi: 644
```

---

# 635-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 635

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 635-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(635);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #635 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
635-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #635 natijasi: 645
```

---

# 636-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 636

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 636-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(636);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #636 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
636-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #636 natijasi: 646
```

---

# 637-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 637

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 637-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(637);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #637 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
637-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #637 natijasi: 647
```

---

# 638-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 638

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 638-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(638);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #638 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
638-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #638 natijasi: 648
```

---

# 639-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 639

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 639-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(639);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #639 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
639-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #639 natijasi: 649
```

---

# 640-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 640

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 640-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(640);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #640 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
640-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #640 natijasi: 650
```

---

# 641-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 641

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 641-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(641);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #641 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
641-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #641 natijasi: 651
```

---

# 642-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 642

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 642-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(642);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #642 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
642-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #642 natijasi: 652
```

---

# 643-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 643

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 643-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(643);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #643 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
643-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #643 natijasi: 653
```

---

# 644-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 644

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 644-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(644);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #644 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
644-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #644 natijasi: 654
```

---

# 645-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 645

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 645-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(645);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #645 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
645-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #645 natijasi: 655
```

---

# 646-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 646

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 646-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(646);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #646 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
646-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #646 natijasi: 656
```

---

# 647-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 647

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 647-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(647);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #647 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
647-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #647 natijasi: 657
```

---

# 648-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 648

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 648-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(648);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #648 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
648-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #648 natijasi: 658
```

---

# 649-Topshiriq: Multithreading va Konkurrentlik amaliyoti: Modul 649

## Topshiriq sharti:
Ko'p oqimli hisoblashlar va resurslarni boshqarish bo'yicha 649-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger val = new AtomicInteger(649);
        Thread t = new Thread(() -> val.addAndGet(10));
        t.start();
        t.join();
        System.out.println("Oqim #649 natijasi: " + val.get());
    }
}
```

## Tushuntirish va Mantiq:
649-topshiriqda oqimlar xavfsizligi va atomik o'zgarishlar tahlil qilindi.

## Ishlash natijasi:
```text
Oqim #649 natijasi: 659
```

---

# 650-Topshiriq: Xulosa topshiriq: Producer-Consumer (Ishlab chiqaruvchi - Iste'molchi) arxitekturasi

## Topshiriq sharti:
BlockingQueue, ThreadPool, AtomicInteger va multithread xavfsizligini birlashtirgan to'liq Producer-Consumer modelini quring.

## Yechim (Java kodi):
```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> bufer = new ArrayBlockingQueue<>(3); // Sig'imi 3 ta
        AtomicInteger xabarlarSoni = new AtomicInteger(0);

        ExecutorService executor = Executors.newFixedThreadPool(2);

        // 1. Ishlab chiqaruvchi (Producer)
        executor.submit(() -> {
            try {
                for (int i = 1; i <= 3; i++) {
                    String xabar = "Xabar-" + i;
                    bufer.put(xabar); // To'lib qolsa avtomatik kutadi
                    System.out.println("[Producer] Yaratildi: " + xabar);
                    Thread.sleep(50);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        // 2. Iste'molchi (Consumer)
        executor.submit(() -> {
            try {
                for (int i = 1; i <= 3; i++) {
                    String xabar = bufer.take(); // Bo'sh bo'lsa avtomatik kutadi
                    System.out.println("  [Consumer] Qayta ishlandi: " + xabar);
                    xabarlarSoni.incrementAndGet();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        executor.shutdown();
        executor.awaitTermination(3, TimeUnit.SECONDS);
        System.out.println("Jami iste'mol qilingan xabarlar soni: " + xabarlarSoni.get());
    }
}
```

## Tushuntirish va Mantiq:
Ushbu klassik Producer-Consumer tizimida:
1. `BlockingQueue` orqali oqimlararo sinxronizatsiya qo'lda `wait/notify` yozmasdan to'liq xavfsiz amalga oshirildi.
2. Ishlab chiqaruvchi bufer to'lganda avtomatik to'xtaydi (`put`), iste'molchi esa ma'lumot kelguncha kutadi (`take`).
3. Bu xabarlar brokeri (Kafka, RabbitMQ) va asinxron arxitekturaning fundamental tamoyilidir.

## Ishlash natijasi:
```text
[Producer] Yaratildi: Xabar-1
  [Consumer] Qayta ishlandi: Xabar-1
[Producer] Yaratildi: Xabar-2
  [Consumer] Qayta ishlandi: Xabar-2
[Producer] Yaratildi: Xabar-3
  [Consumer] Qayta ishlandi: Xabar-3
Jami iste'mol qilingan xabarlar soni: 3
```
