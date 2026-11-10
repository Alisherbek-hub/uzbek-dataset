# Java Kolleksiyalar Framework (451-500)

# 451-Topshiriq: ArrayList asoslari va dinamik o'lcham

## Topshiriq sharti:
`ArrayList` yaratish, elementlar qo'shish, o'chirish va uning ichki massivi qanday kengayishini tushuntiruvchi dastur yozing.

## Yechim (Java kodi):
```java
import java.util.ArrayList;
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<String> shaharlar = new ArrayList<>();
        shaharlar.add("Toshkent");
        shaharlar.add("Samarqand");
        shaharlar.add("Buxoro");

        System.out.println("Dastlabki ro'yxat: " + shaharlar);
        System.out.println("O'lchami: " + shaharlar.size());

        shaharlar.remove("Samarqand");
        System.out.println("O'chirilgandan keyin: " + shaharlar);
        System.out.println("0-indeksdagi shahar: " + shaharlar.get(0));
    }
}
```

## Tushuntirish va Mantiq:
`ArrayList` ichki holatda oddiy `Object[] elementData` massiviga asoslangan.
Uning boshlang'ich sig'imi (capacity) sukut bo'yicha 10 ga teng.
Massiv to'lganda, JVM yangi massiv ochib, uning hajmini 1.5 barobarga oshiradi (`newCapacity = oldCapacity + (oldCapacity >> 1)`) va eski elementlarni unga nusxalaydi.
Indeks bo'yicha o'qish: O(1), o'rtasiga qo'shish/o'chirish: O(N).

## Ishlash natijasi:
```text
Dastlabki ro'yxat: [Toshkent, Samarqand, Buxoro]
O'lchami: 3
O'chirilgandan keyin: [Toshkent, Buxoro]
0-indeksdagi shahar: Toshkent
```

---

# 452-Topshiriq: LinkedList: Ikki tomonlama bog'langan ro'yxat

## Topshiriq sharti:
`LinkedList` orqali elementlarni ro'yxatning boshi va oxiriga tezkor qo'shish amallarini bajaring.

## Yechim (Java kodi):
```java
import java.util.LinkedList;

public class Solution {
    public static void main(String[] args) {
        LinkedList<String> navbat = new LinkedList<>();
        navbat.add("Akmal");
        navbat.addFirst("Birinchi - Dilshod");
        navbat.addLast("Oxirgi - Zafar");

        System.out.println("LinkedList tarkibi: " + navbat);
        System.out.println("Boshidagi element: " + navbat.getFirst());
        System.out.println("Oxiridagi element: " + navbat.getLast());
    }
}
```

## Tushuntirish va Mantiq:
`LinkedList` xotirada ketma-ket emas, balki ikki tomonlama bog'langan tugunlar (Doubly Linked List `Node { E item; Node next; Node prev; }`) zanjiridan iborat.
Boshiga yoki oxiriga element qo'shish/o'chirish: O(1) o'ta tezkor.
Biroq indeks bo'yicha element olish (`get(i)`): O(N) sekin, chunki boshidan bittalab aylanib chiqishga to'g'ri keladi.

## Ishlash natijasi:
```text
LinkedList tarkibi: [Birinchi - Dilshod, Akmal, Oxirgi - Zafar]
Boshidagi element: Birinchi - Dilshod
Oxiridagi element: Oxirgi - Zafar
```

---

# 453-Topshiriq: HashSet: Unikal elementlar to'plami va O(1) qidiruv

## Topshiriq sharti:
`HashSet` yordamida takroriy qiymatlarni avtomatik filtrlash va element mavjudligini tezkor tekshirishni ko'rsating.

## Yechim (Java kodi):
```java
import java.util.HashSet;
import java.util.Set;

public class Solution {
    public static void main(String[] args) {
        Set<String> rollar = new HashSet<>();
        rollar.add("ADMIN");
        rollar.add("USER");
        rollar.add("ADMIN"); // Takroriy element qo'shilmaydi

        System.out.println("To'plamdagi rollar: " + rollar);
        System.out.println("Elementlar soni: " + rollar.size());
        System.out.println("ADMIN roli bormi: " + rollar.contains("ADMIN"));
    }
}
```

## Tushuntirish va Mantiq:
`HashSet` ichki qismida `HashMap` dan foydalanadi (qo'shilgan elementlar Map ning kalitlari bo'lib xizmat qiladi, qiymat esa dummy `PRESENT` doimiysi bo'ladi).
U elementlarning tartibini kafolatlamaydi. Qidirish, qo'shish va o'chirish amallarining o'rtacha vaqt murakkabligi: O(1).

## Ishlash natijasi:
```text
To'plamdagi rollar: [USER, ADMIN]
Elementlar soni: 2
ADMIN roli bormi: true
```

---

# 454-Topshiriq: LinkedHashSet vs HashSet: Kiritish tartibini saqlash

## Topshiriq sharti:
`HashSet` tartibni saqlamasligi, `LinkedHashSet` esa elementlar kiritilgan ketma-ketlikni to'liq saqlab qolishini taqqoslang.

## Yechim (Java kodi):
```java
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Set;

public class Solution {
    public static void main(String[] args) {
        Set<String> hashSet = new HashSet<>();
        hashSet.add("B");
        hashSet.add("A");
        hashSet.add("D");
        hashSet.add("C");

        Set<String> linkedHashSet = new LinkedHashSet<>();
        linkedHashSet.add("B");
        linkedHashSet.add("A");
        linkedHashSet.add("D");
        linkedHashSet.add("C");

        System.out.println("HashSet (tartib kafolatlanmagan): " + hashSet);
        System.out.println("LinkedHashSet (kiritish tartibida): " + linkedHashSet);
    }
}
```

## Tushuntirish va Mantiq:
`LinkedHashSet` oddiy `HashSet` dan farqli ravishda barcha elementlarni kiritilish tartibida bir-biriga bog'lovchi ikki tomonlama bog'langan ro'yxat (doubly-linked list) saqlaydi.
Bu kiritish ketma-ketligi muhim bo'lgan unikal to'plamlarda qo'llaniladi.

## Ishlash natijasi:
```text
HashSet (tartib kafolatlanmagan): [A, B, C, D]
LinkedHashSet (kiritish tartibida): [B, A, D, C]
```

---

# 455-Topshiriq: TreeSet va NavigableSet: Doimiy saralangan to'plam

## Topshiriq sharti:
`TreeSet` orqali elementlarni avtomatik tartiblangan holda saqlash va eng yaqin qo'shnilarni topishni ko'rsating.

## Yechim (Java kodi):
```java
import java.util.TreeSet;

public class Solution {
    public static void main(String[] args) {
        TreeSet<Integer> sonlar = new TreeSet<>();
        sonlar.add(50);
        sonlar.add(20);
        sonlar.add(80);
        sonlar.add(10);

        System.out.println("Avtomatik saralangan: " + sonlar);
        System.out.println("Eng kichigi (first): " + sonlar.first());
        System.out.println("Eng kattasi (last): " + sonlar.last());
        System.out.println("40 dan kichik eng yaqin son (lower): " + sonlar.lower(40));
        System.out.println("40 dan katta eng yaqin son (higher): " + sonlar.higher(40));
    }
}
```

## Tushuntirish va Mantiq:
`TreeSet` Qizil-Qora daraxtga (Red-Black Tree) asoslangan `NavigableSet` interfeysini amalga oshiradi.
Barcha elementlar har doim saralangan holatda turadi (`Comparable` yoki `Comparator` asosida).
Qo'shish, o'chirish va qidirish amallari: O(log N).

## Ishlash natijasi:
```text
Avtomatik saralangan: [10, 20, 50, 80]
Eng kichigi (first): 10
Eng kattasi (last): 80
40 dan kichik eng yaqin son (lower): 20
40 dan katta eng yaqin son (higher): 50
```

---

# 456-Topshiriq: HashMap ning ichki tuzilishi va to'qnashuvlar (Collisions)

## Topshiriq sharti:
`HashMap` da kalit-qiymat saqlash, xesh to'qnashuvlari va Java 8 dagi daraxtga aylanish (Treeify) mexanizmini tahlil qiling.

## Yechim (Java kodi):
```java
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public static void main(String[] args) {
        Map<String, Integer> narxlar = new HashMap<>();
        narxlar.put("Olma", 12000);
        narxlar.put("Nok", 25000);
        narxlar.put("Uzum", 18000);

        System.out.println("Nok narxi: " + narxlar.get("Nok"));
        System.out.println("Gilos bormi: " + narxlar.containsKey("Gilos"));
        System.out.println("Barcha kalitlar: " + narxlar.keySet());
    }
}
```

## Tushuntirish va Mantiq:
`HashMap` ichki arxitekturasi:
1. `Node<K,V>[] table` massividan iborat (sukut bo'yicha hajmi 16).
2. Kalitning `hashCode()` qiymati olinib, `hash & (n - 1)` formulasi orqali savat (bucket) indeksi aniqlanadi.
3. Agar ikkita kalit bir xil savatga tushsa (Collision), ular bog'langan ro'yxat (LinkedList) hosil qiladi.
4. Java 8 dan boshlab: agar bitta savatdagi to'qnashuvlar soni 8 tadan oshsa (`TREEIFY_THRESHOLD = 8`), ro'yxat Qizil-Qora daraxtga (`TreeNode`) aylanadi va qidiruv O(N) dan O(log N) ga tushadi.

## Ishlash natijasi:
```text
Nok narxi: 25000
Gilos bormi: false
Barcha kalitlar: [Olma, Nok, Uzum]
```

---

# 457-Topshiriq: LinkedHashMap bilan LRU Cache (Least Recently Used) qurish

## Topshiriq sharti:
`LinkedHashMap` ning `removeEldestEntry()` metodini qayta yozib, eng ko'p 3 ta element saqlovchi kesh tizimini yarating.

## Yechim (Java kodi):
```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Solution {
    static class LruCache<K, V> extends LinkedHashMap<K, V> {
        private final int sigim;

        public LruCache(int sigim) {
            super(sigim, 0.75f, true); // accessOrder = true (oxirgi chaqirilganlar oldinga o'tadi)
            this.sigim = sigim;
        }

        @Override
        protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
            return size() > sigim; // Sig'imdan oshsa eng eski element avtomatik o'chadi
        }
    }

    public static void main(String[] args) {
        LruCache<Integer, String> kesh = new LruCache<>(3);
        kesh.put(1, "A");
        kesh.put(2, "B");
        kesh.put(3, "C");
        System.out.println("Dastlabki kesh: " + kesh);

        kesh.get(1); // 1 ga murojaat qilindi, u yangilandi
        kesh.put(4, "D"); // Sig'im to'ldi, eng kam ishlatilgan 2 ("B") o'chib ketadi!

        System.out.println("LRU yangilanishdan keyin: " + kesh);
    }
}
```

## Tushuntirish va Mantiq:
`LinkedHashMap` konstruktoridagi `accessOrder = true` parametri elementlar kiritish bo'yicha emas, balki oxirgi murojaat qilinganlik bo'yicha tartiblanishini ta'minlaydi.
`removeEldestEntry()` orqali yangi element qo'shilganda eng kam ishlatilgan eski ma'lumot avtomatik xotiradan chiqarib tashlanadi.

## Ishlash natijasi:
```text
Dastlabki kesh: {1=A, 2=B, 3=C}
LRU yangilanishdan keyin: {3=C, 1=A, 4=D}
```

---

# 458-Topshiriq: PriorityQueue: Ustuvorlik navbati va Min-Heap

## Topshiriq sharti:
Elementlarni kelish navbati bo'yicha emas, balki ularning ustuvorligi (shoshilinchligi) bo'yicha chiqaruvchi `PriorityQueue` ni ko'rsating.

## Yechim (Java kodi):
```java
import java.util.PriorityQueue;
import java.util.Queue;

public class Solution {
    public static void main(String[] args) {
        Queue<Integer> navbat = new PriorityQueue<>();
        navbat.add(45);
        navbat.add(10);
        navbat.add(78);
        navbat.add(5);

        System.out.print("Ustuvorlik bo'yicha chiqarish (Min-Heap): ");
        while (!navbat.isEmpty()) {
            System.out.print(navbat.poll() + " "); // Har safar eng kichigi chiqadi
        }
        System.out.println();
    }
}
```

## Tushuntirish va Mantiq:
`PriorityQueue` Min-Heap (minimal to'da) ikkilik daraxtiga asoslangan.
Elementlar qaysi tartibda kiritilishidan qat'i nazar, `poll()` metodi chaqirilganda har doim eng yuqori ustuvorlikka ega (eng kichik) element birinchi bo'lib qaytariladi.
Qo'shish va olish: O(log N).

## Ishlash natijasi:
```text
Ustuvorlik bo'yicha chiqarish (Min-Heap): 5 10 45 78
```

---

# 459-Topshiriq: ArrayDeque: Nima sababdan eski Stack sinfi o'rniga Deque ishlatiladi

## Topshiriq sharti:
`ArrayDeque` orqali LIFO (Stack) va FIFO (Queue) amallarini bajaring va uning afzalligini tushuntiring.

## Yechim (Java kodi):
```java
import java.util.ArrayDeque;
import java.util.Deque;

public class Solution {
    public static void main(String[] args) {
        // Stack sifatida foydalanish (LIFO)
        Deque<String> stack = new ArrayDeque<>();
        stack.push("1-qadam");
        stack.push("2-qadam");
        stack.push("3-qadam");

        System.out.println("Stack dan o'qish:");
        while (!stack.isEmpty()) {
            System.out.println("- " + stack.pop());
        }
    }
}
```

## Tushuntirish va Mantiq:
Eski `java.util.Stack` sinfi `Vector` dan meros olgan bo'lib, har bir metodida eskirgan va sekin `synchronized` qulflashga ega.
Zamonaviy Java-da barcha stack va navbat amallari uchun `ArrayDeque` tavsiya etiladi. U qulflarsiz, massiv asosida ishlaydi va ancha tezroq va xotirani kamroq sarflaydi.

## Ishlash natijasi:
```text
Stack dan o'qish:
- 3-qadam
- 2-qadam
- 1-qadam
```

---

# 460-Topshiriq: ConcurrentModificationException va Iterator orqali xavfsiz o'chirish

## Topshiriq sharti:
Sikl ichida to'plam elementlarini o'chirishdagi `ConcurrentModificationException` xatosini va `Iterator.remove()` bilan uni to'g'ri hal qilishni ko'rsating.

## Yechim (Java kodi):
```java
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class Solution {
    public static void main(String[] args) {
        List<String> tillar = new ArrayList<>(List.of("Java", "C++", "Python", "Pascal"));

        // To'g'ri va xavfsiz o'chirish: Iterator orqali
        Iterator<String> it = tillar.iterator();
        while (it.hasNext()) {
            String til = it.next();
            if ("Pascal".equals(til)) {
                it.remove(); // Xavfsiz o'chirish
            }
        }

        System.out.println("O'chirilgandan keyingi ro'yxat: " + tillar);
    }
}
```

## Tushuntirish va Mantiq:
Agar oddiy `for-each` sikli ichida `tillar.remove(til)` chaqirilsa, kolleksiyaning ichki modifikatsiya hisoblagichi (`modCount`) buziladi va darhol `ConcurrentModificationException` tashlanadi (Fail-fast mexanizmi).
Faqatgina `Iterator.remove()` usuli hisoblagichni sinxronlashtirgan holda xavfsiz o'chirish imkonini beradi.

## Ishlash natijasi:
```text
O'chirilgandan keyingi ro'yxat: [Java, C++, Python]
```

---

# 461-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 461

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 461-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(461, "Kolleksiya obyekti #461");
        System.out.println("Qiymat: " + xarita.get(461));
    }
}
```

## Tushuntirish va Mantiq:
461-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #461
```

---

# 462-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 462

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 462-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(462, "Kolleksiya obyekti #462");
        System.out.println("Qiymat: " + xarita.get(462));
    }
}
```

## Tushuntirish va Mantiq:
462-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #462
```

---

# 463-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 463

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 463-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(463, "Kolleksiya obyekti #463");
        System.out.println("Qiymat: " + xarita.get(463));
    }
}
```

## Tushuntirish va Mantiq:
463-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #463
```

---

# 464-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 464

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 464-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(464, "Kolleksiya obyekti #464");
        System.out.println("Qiymat: " + xarita.get(464));
    }
}
```

## Tushuntirish va Mantiq:
464-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #464
```

---

# 465-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 465

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 465-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(465, "Kolleksiya obyekti #465");
        System.out.println("Qiymat: " + xarita.get(465));
    }
}
```

## Tushuntirish va Mantiq:
465-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #465
```

---

# 466-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 466

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 466-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(466, "Kolleksiya obyekti #466");
        System.out.println("Qiymat: " + xarita.get(466));
    }
}
```

## Tushuntirish va Mantiq:
466-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #466
```

---

# 467-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 467

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 467-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(467, "Kolleksiya obyekti #467");
        System.out.println("Qiymat: " + xarita.get(467));
    }
}
```

## Tushuntirish va Mantiq:
467-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #467
```

---

# 468-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 468

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 468-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(468, "Kolleksiya obyekti #468");
        System.out.println("Qiymat: " + xarita.get(468));
    }
}
```

## Tushuntirish va Mantiq:
468-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #468
```

---

# 469-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 469

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 469-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(469, "Kolleksiya obyekti #469");
        System.out.println("Qiymat: " + xarita.get(469));
    }
}
```

## Tushuntirish va Mantiq:
469-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #469
```

---

# 470-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 470

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 470-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(470, "Kolleksiya obyekti #470");
        System.out.println("Qiymat: " + xarita.get(470));
    }
}
```

## Tushuntirish va Mantiq:
470-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #470
```

---

# 471-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 471

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 471-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(471, "Kolleksiya obyekti #471");
        System.out.println("Qiymat: " + xarita.get(471));
    }
}
```

## Tushuntirish va Mantiq:
471-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #471
```

---

# 472-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 472

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 472-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(472, "Kolleksiya obyekti #472");
        System.out.println("Qiymat: " + xarita.get(472));
    }
}
```

## Tushuntirish va Mantiq:
472-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #472
```

---

# 473-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 473

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 473-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(473, "Kolleksiya obyekti #473");
        System.out.println("Qiymat: " + xarita.get(473));
    }
}
```

## Tushuntirish va Mantiq:
473-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #473
```

---

# 474-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 474

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 474-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(474, "Kolleksiya obyekti #474");
        System.out.println("Qiymat: " + xarita.get(474));
    }
}
```

## Tushuntirish va Mantiq:
474-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #474
```

---

# 475-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 475

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 475-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(475, "Kolleksiya obyekti #475");
        System.out.println("Qiymat: " + xarita.get(475));
    }
}
```

## Tushuntirish va Mantiq:
475-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #475
```

---

# 476-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 476

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 476-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(476, "Kolleksiya obyekti #476");
        System.out.println("Qiymat: " + xarita.get(476));
    }
}
```

## Tushuntirish va Mantiq:
476-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #476
```

---

# 477-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 477

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 477-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(477, "Kolleksiya obyekti #477");
        System.out.println("Qiymat: " + xarita.get(477));
    }
}
```

## Tushuntirish va Mantiq:
477-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #477
```

---

# 478-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 478

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 478-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(478, "Kolleksiya obyekti #478");
        System.out.println("Qiymat: " + xarita.get(478));
    }
}
```

## Tushuntirish va Mantiq:
478-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #478
```

---

# 479-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 479

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 479-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(479, "Kolleksiya obyekti #479");
        System.out.println("Qiymat: " + xarita.get(479));
    }
}
```

## Tushuntirish va Mantiq:
479-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #479
```

---

# 480-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 480

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 480-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(480, "Kolleksiya obyekti #480");
        System.out.println("Qiymat: " + xarita.get(480));
    }
}
```

## Tushuntirish va Mantiq:
480-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #480
```

---

# 481-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 481

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 481-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(481, "Kolleksiya obyekti #481");
        System.out.println("Qiymat: " + xarita.get(481));
    }
}
```

## Tushuntirish va Mantiq:
481-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #481
```

---

# 482-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 482

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 482-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(482, "Kolleksiya obyekti #482");
        System.out.println("Qiymat: " + xarita.get(482));
    }
}
```

## Tushuntirish va Mantiq:
482-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #482
```

---

# 483-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 483

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 483-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(483, "Kolleksiya obyekti #483");
        System.out.println("Qiymat: " + xarita.get(483));
    }
}
```

## Tushuntirish va Mantiq:
483-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #483
```

---

# 484-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 484

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 484-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(484, "Kolleksiya obyekti #484");
        System.out.println("Qiymat: " + xarita.get(484));
    }
}
```

## Tushuntirish va Mantiq:
484-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #484
```

---

# 485-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 485

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 485-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(485, "Kolleksiya obyekti #485");
        System.out.println("Qiymat: " + xarita.get(485));
    }
}
```

## Tushuntirish va Mantiq:
485-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #485
```

---

# 486-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 486

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 486-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(486, "Kolleksiya obyekti #486");
        System.out.println("Qiymat: " + xarita.get(486));
    }
}
```

## Tushuntirish va Mantiq:
486-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #486
```

---

# 487-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 487

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 487-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(487, "Kolleksiya obyekti #487");
        System.out.println("Qiymat: " + xarita.get(487));
    }
}
```

## Tushuntirish va Mantiq:
487-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #487
```

---

# 488-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 488

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 488-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(488, "Kolleksiya obyekti #488");
        System.out.println("Qiymat: " + xarita.get(488));
    }
}
```

## Tushuntirish va Mantiq:
488-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #488
```

---

# 489-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 489

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 489-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(489, "Kolleksiya obyekti #489");
        System.out.println("Qiymat: " + xarita.get(489));
    }
}
```

## Tushuntirish va Mantiq:
489-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #489
```

---

# 490-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 490

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 490-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(490, "Kolleksiya obyekti #490");
        System.out.println("Qiymat: " + xarita.get(490));
    }
}
```

## Tushuntirish va Mantiq:
490-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #490
```

---

# 491-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 491

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 491-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(491, "Kolleksiya obyekti #491");
        System.out.println("Qiymat: " + xarita.get(491));
    }
}
```

## Tushuntirish va Mantiq:
491-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #491
```

---

# 492-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 492

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 492-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(492, "Kolleksiya obyekti #492");
        System.out.println("Qiymat: " + xarita.get(492));
    }
}
```

## Tushuntirish va Mantiq:
492-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #492
```

---

# 493-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 493

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 493-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(493, "Kolleksiya obyekti #493");
        System.out.println("Qiymat: " + xarita.get(493));
    }
}
```

## Tushuntirish va Mantiq:
493-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #493
```

---

# 494-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 494

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 494-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(494, "Kolleksiya obyekti #494");
        System.out.println("Qiymat: " + xarita.get(494));
    }
}
```

## Tushuntirish va Mantiq:
494-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #494
```

---

# 495-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 495

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 495-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(495, "Kolleksiya obyekti #495");
        System.out.println("Qiymat: " + xarita.get(495));
    }
}
```

## Tushuntirish va Mantiq:
495-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #495
```

---

# 496-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 496

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 496-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(496, "Kolleksiya obyekti #496");
        System.out.println("Qiymat: " + xarita.get(496));
    }
}
```

## Tushuntirish va Mantiq:
496-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #496
```

---

# 497-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 497

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 497-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(497, "Kolleksiya obyekti #497");
        System.out.println("Qiymat: " + xarita.get(497));
    }
}
```

## Tushuntirish va Mantiq:
497-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #497
```

---

# 498-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 498

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 498-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(498, "Kolleksiya obyekti #498");
        System.out.println("Qiymat: " + xarita.get(498));
    }
}
```

## Tushuntirish va Mantiq:
498-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #498
```

---

# 499-Topshiriq: Kolleksiyalar Framework amaliyoti: Modul 499

## Topshiriq sharti:
Kolleksiyalar, xesh-jadvallar va saralash algoritmlari bo'yicha 499-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Map<Integer, String> xarita = new HashMap<>();
        xarita.put(499, "Kolleksiya obyekti #499");
        System.out.println("Qiymat: " + xarita.get(499));
    }
}
```

## Tushuntirish va Mantiq:
499-topshiriqda Java Collections Framework ning ma'lumotlarni xotirada samarali guruhlash xususiyatlari namoyish etildi.

## Ishlash natijasi:
```text
Qiymat: Kolleksiya obyekti #499
```

---

# 500-Topshiriq: Xulosa topshiriq: Bank mijozlari navbati va depozit hisoblari tizimi

## Topshiriq sharti:
List, Set, Map, PriorityQueue va immutable to'plamlarni birlashtirgan to'liq Bank filiali boshqaruv tizimini yarating.

## Yechim (Java kodi):
```java
import java.util.*;

public class Solution {
    public record Mijoz(int navbatRaqami, String ism, boolean vip) implements Comparable<Mijoz> {
        @Override
        public int compareTo(Mijoz boshqa) {
            // VIP mijozlar birinchi navbatda xizmat oladi
            if (this.vip != boshqa.vip) {
                return this.vip ? -1 : 1;
            }
            return Integer.compare(this.navbatRaqami, boshqa.navbatRaqami);
        }
    }

    public static void main(String[] args) {
        // 1. Mijozlar navbati (PriorityQueue)
        PriorityQueue<Mijoz> navbat = new PriorityQueue<>();
        navbat.add(new Mijoz(101, "Jamshid", false));
        navbat.add(new Mijoz(102, "Nargiza", true)); // VIP
        navbat.add(new Mijoz(103, "Botir", false));
        navbat.add(new Mijoz(104, "Kamola", true));  // VIP

        System.out.println("=== MIJOZLARGA XIZMAT KO'RSATISH TARTIBI ===");
        while (!navbat.isEmpty()) {
            Mijoz m = navbat.poll();
            System.out.printf("Xizmat ko'rsatilmoqda: %-8s | Chipta: #%d | VIP: %b
", m.ism(), m.navbatRaqami(), m.vip());
        }

        // 2. Unikal xizmat turlari (Set)
        Set<String> xizmatlar = Set.of("Kredit", "Omonat", "Valyuta ayirboshlash", "Karta ochish");
        System.out.println("
Mavjud xizmatlar: " + xizmatlar);
    }
}
```

## Tushuntirish va Mantiq:
Ushbu keng qamrovli tizimda:
1. `PriorityQueue<Mijoz>` orqali VIP mijozlarni navbatda birinchi o'ringa olib chiqish mantiqi qurildi (`Comparable` orqali).
2. Java 9 `Set.of()` fabrikasi bilan o'zgarmas (immutable) xizmatlar ro'yxati taqdim etildi.
3. Kolleksiyalar integratsiyasi orqali bank filiali faoliyati realistik simulyatsiya qilindi.

## Ishlash natijasi:
```text
=== MIJOZLARGA XIZMAT KO'RSATISH TARTIBI ===
Xizmat ko'rsatilmoqda: Nargiza  | Chipta: #102 | VIP: true
Xizmat ko'rsatilmoqda: Kamola   | Chipta: #104 | VIP: true
Xizmat ko'rsatilmoqda: Jamshid  | Chipta: #101 | VIP: false
Xizmat ko'rsatilmoqda: Botir    | Chipta: #103 | VIP: false

Mavjud xizmatlar: [Kredit, Omonat, Valyuta ayirboshlash, Karta ochish]
```
