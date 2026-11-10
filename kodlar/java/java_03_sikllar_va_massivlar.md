# Java Sikllar va Massivlar (101-150)

# 101-Topshiriq: Klassik for sikli: 1 dan N gacha yig'indini hisoblash

## Topshiriq sharti:
Klassik `for` sikli yordamida 1 dan 100 gacha bo'lgan barcha natural sonlar yig'indisini hisoblovchi dastur yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int n = 100;
        int yigindi = 0;
        
        for (int i = 1; i <= n; i++) {
            yigindi += i;
        }
        
        System.out.println("1 dan " + n + " gacha sonlar yig'indisi: " + yigindi);
    }
}
```

## Tushuntirish va Mantiq:
Klassik `for` sikli 3 ta asosiy bo'limdan iborat:
1. Initsializatsiya (`int i = 1`): faqat bir marta, sikl boshida ishga tushadi.
2. Shart (`i <= n`): har bir iteratsiya oldidan tekshiriladi.
3. Yangilanish (`i++`): sikl tanasi bajarib bo'lingach hisoblagichni o'zgartiradi.
Bu konstruksiya aniq sonli takrorlanishlar uchun eng maqbul vositadir.

## Ishlash natijasi:
```text
1 dan 100 gacha sonlar yig'indisi: 5050
```

---

# 102-Topshiriq: Teskari yo'nalishdagi for sikli

## Topshiriq sharti:
Berilgan sonli qiymatdan 1 gacha orqaga qarab sanovchi teskari `for` siklini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        System.out.print("Kosmik kema parvoziga start: ");
        for (int i = 5; i >= 1; i--) {
            System.out.print(i + " ");
        }
        System.out.println("-> Start!");
    }
}
```

## Tushuntirish va Mantiq:
Teskari siklda boshlang'ich qiymat katta son qilib belgilanadi, shart `i >= 1` ko'rinishida kamayib borishni nazorat qiladi va har bir qadamda dekrement (`i--`) qo'llaniladi.

## Ishlash natijasi:
```text
Kosmik kema parvoziga start: 5 4 3 2 1 -> Start!
```

---

# 103-Topshiriq: Bir nechta hisoblagichli for sikli

## Topshiriq sharti:
Bitta `for` sikli ichida ikkita o'zgaruvchini parallel o'zgartirib borish (`i++`, `j--`) namunasini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        for (int i = 1, j = 10; i <= 5 && j >= 6; i++, j--) {
            System.out.println("i = " + i + ", j = " + j + " -> Ko'paytma: " + (i * j));
        }
    }
}
```

## Tushuntirish va Mantiq:
Java-da `for` siklining initsializatsiya va iteratsiya qismlarida vergul bilan ajratilgan holda bir nechta bir xil tipdagi o'zgaruvchilarni e'lon qilish va o'zgartirish mumkin.
Bu qidiruv algoritmlarida ikkita ko'rsatkichni qarama-qarshi tomondan harakatlantirishda juda qo'l keladi.

## Ishlash natijasi:
```text
i = 1, j = 10 -> Ko'paytma: 10
i = 2, j = 9 -> Ko'paytma: 18
i = 3, j = 8 -> Ko'paytma: 24
i = 4, j = 7 -> Ko'paytma: 28
i = 5, j = 6 -> Ko'paytma: 30
```

---

# 104-Topshiriq: While sikli: Son raqamlari yig'indisini hisoblash

## Topshiriq sharti:
`while` sikli yordamida berilgan ixtiyoriy musbat butun sonning raqamlari yig'indisini hisoblovchi dastur tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son = 98765;
        int nusha = son;
        int yigindi = 0;
        
        while (son > 0) {
            int oxirgiRaqam = son % 10;
            yigindi += oxirgiRaqam;
            son /= 10;
        }
        
        System.out.println(nusha + " sonining raqamlari yig'indisi: " + yigindi);
    }
}
```

## Tushuntirish va Mantiq:
`while` sikli qadamlar soni oldindan aniq bo'lmagan, lekin ma'lum bir mantiqiy shartga bog'liq bo'lgan holatlarda ishlatiladi.
Har bir qadamda `son % 10` orqali oxirgi raqam olinadi, `son /= 10` orqali son 10 barobarga qisqartiriladi va son 0 bo'lganda sikl avtomatik to'xtaydi.

## Ishlash natijasi:
```text
98765 sonining raqamlari yig'indisi: 35
```

---

# 105-Topshiriq: While sikli bilan sonni teskarisiga o'girish (Reverse Number)

## Topshiriq sharti:
Matnga aylantirmasdan, sof arifmetik amallar va `while` sikli yordamida sonni teskarisiga o'giring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son = 12345;
        int teskari = 0;
        
        int temp = son;
        while (temp != 0) {
            int qoldiq = temp % 10;
            teskari = teskari * 10 + qoldiq;
            temp /= 10;
        }
        
        System.out.println("Dastlabki: " + son);
        System.out.println("Teskari o'girilgan: " + teskari);
    }
}
```

## Tushuntirish va Mantiq:
`teskari * 10 + qoldiq` formulasi har bir iteratsiyada yangi olingan raqamni bir xona yuqoriga surib, yangi raqamni birliklar xonasiga qo'shadi. Natijada son to'liq teskari o'giriladi.

## Ishlash natijasi:
```text
Dastlabki: 12345
Teskari o'girilgan: 54321
```

---

# 106-Topshiriq: Do-While sikli va shartdan oldin kamida 1 marta bajarilish

## Topshiriq sharti:
`do-while` sikli shart hatto boshidanoq `false` bo'lsa ham uning tanasi kamida 1 marta bajarilishini ko'rsatuvchi dastur tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son = 100;
        
        System.out.println("do-while boshlandi:");
        do {
            System.out.println("Sikl tanasi bajarildi! Qiymat: " + son);
            son++;
        } while (son < 50); // Shart boshidanoq yolg'on!
        
        System.out.println("do-while yakunlandi.");
    }
}
```

## Tushuntirish va Mantiq:
`do-while` siklining `while` dan tub farqi: uning sharti eng oxirida tekshiriladi (post-condition loop).
Shu bois shart qanday bo'lishidan qat'i nazar uning tanasi kamida bir marta bajarilishi 100% kafolatlanadi. Bu foydalanuvchidan ma'lumot kiritishni so'rash yoki tizimni ishga tushirish menyusida keng qo'llaniladi.

## Ishlash natijasi:
```text
do-while boshlandi:
Sikl tanasi bajarildi! Qiymat: 100
do-while yakunlandi.
```

---

# 107-Topshiriq: Cheksiz sikl va break bilan to'xtatish

## Topshiriq sharti:
`while (true)` cheksiz siklini ma'lum shart bajarilganda `break` bilan xavfsiz to'xtatish mexanizmini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int hisoblagich = 1;
        
        while (true) {
            System.out.print(hisoblagich + " ");
            if (hisoblagich == 7) {
                System.out.println("
7 soniga yetildi, sikl to'xtatildi!");
                break;
            }
            hisoblagich++;
        }
    }
}
```

## Tushuntirish va Mantiq:
Cheksiz sikllar hodisalar kutish (event loop), tarmoq soketlarini tinglash yoki qidiruv algoritmlarida ishlatiladi.
Ulardan chiqib ketish uchun ichki qismda qat'iy tekshiruv va `break` bo'lishi shart, aks holda dastur abadiy qotib qoladi (infinite loop) va CPU ni to'ldiradi.

## Ishlash natijasi:
```text
1 2 3 4 5 6 7 
7 soniga yetildi, sikl to'xtatildi!
```

---

# 108-Topshiriq: Enhanced for-each sikli asoslari

## Topshiriq sharti:
Massiv elementlarini indekslarsiz, toza va xavfsiz o'qish uchun `for-each` siklidan foydalaning.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String[] shaharlar = {"Toshkent", "Samarqand", "Buxoro", "Xiva"};
        
        System.out.println("Shaharlar ro'yxati:");
        for (String shahar : shaharlar) {
            System.out.println("- " + shahar);
        }
    }
}
```

## Tushuntirish va Mantiq:
Java 5 da kiritilgan Enhanced for-each sikli `for (Tip element : to'plam)` sintaksisiga ega.
U `ArrayIndexOutOfBoundsException` xatolarini butunlay istisno qiladi va kodni o'qishni juda osonlashtiradi.

## Ishlash natijasi:
```text
Shaharlar ro'yxati:
- Toshkent
- Samarqand
- Buxoro
- Xiva
```

---

# 109-Topshiriq: For-each siklining cheklovi: Elementlarni o'zgartirib bo'lmasligi

## Topshiriq sharti:
`for-each` siklida aylanuvchi o'zgaruvchiga yangi qiymat berish massivning o'zidagi asl elementni o'zgartirmasligini isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[] sonlar = {1, 2, 3, 4, 5};
        
        // for-each orqali o'zgartirishga urinish
        for (int s : sonlar) {
            s = s * 10; // Bu faqat lokal nusxani o'zgartiradi!
        }
        
        System.out.print("for-each dan keyingi asl massiv: ");
        for (int s : sonlar) {
            System.out.print(s + " ");
        }
        System.out.println();
    }
}
```

## Tushuntirish va Mantiq:
`for-each` siklidagi `s` o'zgaruvchisi massiv elementining qiymat nusxasi (copy by value) hisoblanadi.
Unga boshqa qiymat berish asl massivdagi yacheykaga ta'sir qilmaydi. Agar massiv elementlarini o'zgartirish kerak bo'lsa, klassik indeksli `for (int i = 0; ...)` siklidan foydalanish shart.

## Ishlash natijasi:
```text
for-each dan keyingi asl massiv: 1 2 3 4 5
```

---

# 110-Topshiriq: Ichma-ich for sikllari: Karra jadvali

## Topshiriq sharti:
Ichma-ich joylashgan ikkita `for` sikli yordamida 1 dan 5 gacha bo'lgan sonlarning karra jadvalini chiroyli formatlab chiqaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) {
            for (int j = 1; j <= 5; j++) {
                System.out.printf("%4d", i * j);
            }
            System.out.println();
        }
    }
}
```

## Tushuntirish va Mantiq:
Tashqi sikl qatorlarni (`i`), ichki sikl esa har bir qatordagi ustunlarni (`j`) ifodalaydi.
Tashqi siklning har bir qadami uchun ichki sikl to'liq boshidan oxirigacha aylanib chiqadi. `%4d` formatlash belgisi har bir sonni 4 ta katakcha kenglikda tekislaydi.

## Ishlash natijasi:
```text
1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
   4   8  12  16  20
   5  10  15  20  25
```

---

# 111-Topshiriq: 1D massiv e'lon qilish, xotira ajratish va length xossasi

## Topshiriq sharti:
Massiv yaratishning turli usullarini ko'rsating va uning o'zgarmas `length` xossasini tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[] m1 = new int[5]; // Standart bo'sh massiv (0 lar bilan to'ladi)
        int[] m2 = {10, 20, 30, 40, 50}; // Literal bilan initsializatsiya
        
        System.out.println("m1 uzunligi: " + m1.length);
        System.out.println("m2 uzunligi: " + m2.length);
        System.out.println("m1 ning 0-elementi default qiymati: " + m1[0]);
    }
}
```

## Tushuntirish va Mantiq:
Java-da massivlar obyekt hisoblanadi va Heap xotirada ketma-ket (contiguous) yacheykalarda joylashadi.
Massiv uzunligi (`length`) obyekt yaratilganda bir marta belgilanadi va keyinchalik o'zgarmaydi (`final`). U metod emas, ommaviy maydondir (shuning uchun qavssiz yoziladi).

## Ishlash natijasi:
```text
m1 uzunligi: 5
m2 uzunligi: 5
m1 ning 0-elementi default qiymati: 0
```

---

# 112-Topshiriq: ArrayIndexOutOfBoundsException va undan himoyalanish

## Topshiriq sharti:
Massiv chegarasidan tashqariga chiqish xatosini ko'rsating va to'g'ri chegara nazoratini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[] sonlar = {10, 20, 30};
        
        try {
            int xato = sonlar[3]; // Indekslar 0, 1, 2 bo'ladi
            System.out.println(xato);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Diqqat! Massiv chegarasidan chiqildi: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
Java-da massiv indeksatsiyasi har doim `0` dan boshlanadi va `length - 1` da tugaydi.
Mavjud bo'lmagan indeksga murojaat qilish vaqtida JVM xotira xavfsizligini ta'minlash maqsadida darhol `ArrayIndexOutOfBoundsException` tashlaydi (C/C++ dan farqli o'laroq, begona xotirani o'qishga yo'l qo'ymaydi).

## Ishlash natijasi:
```text
Diqqat! Massiv chegarasidan chiqildi: Index 3 out of bounds for length 3
```

---

# 113-Topshiriq: Massivdagi eng katta va eng kichik elementlarni topish

## Topshiriq sharti:
Bitta sikl ichida massivning minimal va maksimal qiymatlarini topuvchi optimal dastur yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[] sonlar = {45, 12, 89, -5, 67, 102, 33};
        
        int min = sonlar[0];
        int max = sonlar[0];
        
        for (int i = 1; i < sonlar.length; i++) {
            if (sonlar[i] < min) min = sonlar[i];
            if (sonlar[i] > max) max = sonlar[i];
        }
        
        System.out.println("Minimal element: " + min);
        System.out.println("Maksimal element: " + max);
    }
}
```

## Tushuntirish va Mantiq:
Dastlabki `min` va `max` qiymatlar uchun 0 emas, massivning birinchi elementi (`sonlar[0]`) olinadi (bu barcha sonlar manfiy bo'lgan taqdirda ham to'g'ri ishlashini kafolatlaydi).
Sikl 1-indeksdan boshlanib, har bir son bilan solishtirib boriladi (O(N) vaqt).

## Ishlash natijasi:
```text
Minimal element: -5
Maksimal element: 102
```

---

# 114-Topshiriq: Massiv elementlarining o'rta arifmetigini hisoblash

## Topshiriq sharti:
Butun sonli massiv elementlari yig'indisi va o'rta arifmetik qiymatini haqiqiy son (`double`) aniqligida hisoblang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[] baholar = {85, 90, 78, 92, 88};
        int yigindi = 0;
        
        for (int b : baholar) {
            yigindi += b;
        }
        
        double ortaArifmetik = (double) yigindi / baholar.length;
        System.out.println("Jami ball: " + yigindi);
        System.out.printf("O'rtacha ball: %.2f
", ortaArifmetik);
    }
}
```

## Tushuntirish va Mantiq:
O'rta arifmetikani hisoblashda `yigindi / baholar.length` amali butun sonli bo'lish bo'lib kasr qismini yo'qotmasligi uchun, kamida bitta operand `(double)` kasting qilinishi zarur.

## Ishlash natijasi:
```text
Jami ball: 433
O'rtacha ball: 86.60
```

---

# 115-Topshiriq: Chiziqli qidiruv (Linear Search) algoritmi

## Topshiriq sharti:
Massivdan berilgan elementni chiziqli qidiruv usulida topib, uning indeksini qaytaruvchi metod yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i; // Element topildi
            }
        }
        return -1; // Element topilmadi
    }

    public static void main(String[] args) {
        int[] massiv = {14, 88, 23, 42, 99};
        System.out.println("42 ning indeksi: " + linearSearch(massiv, 42));
        System.out.println("100 ning indeksi: " + linearSearch(massiv, 100));
    }
}
```

## Tushuntirish va Mantiq:
Chiziqli qidiruv saralanmagan massivlarda barcha elementlarni boshidan oxirigacha birma-bir tekshirib chiqadi.
Vaqt murakkabligi: eng yaxshi holatda O(1), eng yomon va o'rtacha holatda O(N).

## Ishlash natijasi:
```text
42 ning indeksi: 3
100 ning indeksi: -1
```

---

# 116-Topshiriq: Binar qidiruv (Binary Search) algoritmi

## Topshiriq sharti:
Saralangan massivda logarifmik tezlikda ishlovchi binar qidiruv algoritmini noldan yarating.

## Yechim (Java kodi):
```java
public class Solution {
    public static int binarySearch(int[] arr, int target) {
        int chap = 0;
        int ong = arr.length - 1;
        
        while (chap <= ong) {
            int orta = chap + (ong - chap) / 2;
            
            if (arr[orta] == target) return orta;
            if (arr[orta] < target) chap = orta + 1;
            else ong = orta - 1;
        }
        
        return -1;
    }

    public static void main(String[] args) {
        int[] saralangan = {12, 25, 34, 48, 59, 72, 88, 91};
        int target = 72;
        int indeks = binarySearch(saralangan, target);
        System.out.println(target + " soni indeksi: " + indeks);
    }
}
```

## Tushuntirish va Mantiq:
Binar qidiruv faqat SARALANGAN massivlarda ishlaydi.
Har bir qadamda qidiruv maydoni teng ikkiga qisqaradi:
O'rta indeks `chap + (ong - chap) / 2` formulasi orqali to'lib toshishdan (overflow) himoyalangan holda hisoblanadi.
Vaqt murakkabligi: O(log N).

## Ishlash natijasi:
```text
72 soni indeksi: 5
```

---

# 117-Topshiriq: Massivni teskari o'girish (In-place Array Reversal)

## Topshiriq sharti:
Qo'shimcha massiv ochmasdan, xotirani tejagan holda massiv elementlarini o'z joyida (in-place) teskarisiga o'giring.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void reverse(int[] arr) {
        int bosh = 0;
        int oxir = arr.length - 1;
        
        while (bosh < oxir) {
            int temp = arr[bosh];
            arr[bosh] = arr[oxir];
            arr[oxir] = temp;
            bosh++;
            oxir--;
        }
    }

    public static void main(String[] args) {
        int[] sonlar = {1, 2, 3, 4, 5, 6};
        System.out.println("Asl holat: " + Arrays.toString(sonlar));
        
        reverse(sonlar);
        System.out.println("Teskari o'girilgan: " + Arrays.toString(sonlar));
    }
}
```

## Tushuntirish va Mantiq:
Ikki ko'rsatkich (Two Pointers) texnikasi:
Biri boshidan (`bosh = 0`), ikkinchisi oxiridan (`oxir = length - 1`) boshlab o'rtaga qarab yuradi va elementlar qiymati almashtiriladi.
Xotira sarfi: O(1) (qo'shimcha xotira talab qilinmaydi), Vaqt sarfi: O(N/2) = O(N).

## Ishlash natijasi:
```text
Asl holat: [1, 2, 3, 4, 5, 6]
Teskari o'girilgan: [6, 5, 4, 3, 2, 1]
```

---

# 118-Topshiriq: Massivda elementlarning uchrash chastotasi

## Topshiriq sharti:
Massiv ichidagi har bir element necha marta takrorlanganini hisoblovchi dastur yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[] sonlar = {2, 5, 2, 8, 5, 2, 9};
        boolean[] tashrifBuyurilgan = new boolean[sonlar.length];
        
        System.out.println("Elementlar chastotasi:");
        for (int i = 0; i < sonlar.length; i++) {
            if (tashrifBuyurilgan[i]) continue;
            
            int sana = 1;
            for (int j = i + 1; j < sonlar.length; j++) {
                if (sonlar[i] == sonlar[j]) {
                    tashrifBuyurilgan[j] = true;
                    sana++;
                }
            }
            System.out.println(sonlar[i] + " soni: " + sana + " marta");
        }
    }
}
```

## Tushuntirish va Mantiq:
Tashrif buyurilgan elementlarni qayta hisoblamaslik uchun `boolean[] tashrifBuyurilgan` massividan foydalaniladi.
Bu saralanmagan massivda takrorlanishlarni aniqlashning klassik usulidir.

## Ishlash natijasi:
```text
Elementlar chastotasi:
2 soni: 3 marta
5 soni: 2 marta
8 soni: 1 marta
9 soni: 1 marta
```

---

# 119-Topshiriq: Massivdan takrorlangan elementlarni o'chirish

## Topshiriq sharti:
Saralangan massivdagi duplikat elementlarni in-place o'chirib, unikal elementlar sonini qaytaruvchi dastur tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static int removeDuplicates(int[] arr) {
        if (arr.length == 0) return 0;
        
        int unikalIndeks = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] != arr[unikalIndeks]) {
                unikalIndeks++;
                arr[unikalIndeks] = arr[i];
            }
        }
        return unikalIndeks + 1;
    }

    public static void main(String[] args) {
        int[] saralangan = {1, 1, 2, 2, 3, 4, 4, 5};
        int unikalSoni = removeDuplicates(saralangan);
        
        System.out.print("Unikal elementlar (" + unikalSoni + " ta): ");
        for (int i = 0; i < unikalSoni; i++) {
            System.out.print(saralangan[i] + " ");
        }
        System.out.println();
    }
}
```

## Tushuntirish va Mantiq:
Ushbu algoritm O(N) vaqt va O(1) qo'shimcha xotira sarflaydi.
`unikalIndeks` faqat yangi element uchraganda oldinga suriladi va o'sha yerga yangi qiymat yoziladi. Bu LeetCode dagi klassik intervyu masalalaridan biridir.

## Ishlash natijasi:
```text
Unikal elementlar (5 ta): 1 2 3 4 5
```

---

# 120-Topshiriq: Massiv elementlarini chapga 1 qadam siljitish (Left Shift)

## Topshiriq sharti:
Massivning 0-elementini oxiriga o'tkazib, qolgan barcha elementlarni 1 qadam chapga suruvchi dastur tuzing.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[] arr = {10, 20, 30, 40, 50};
        int birinchi = arr[0];
        
        for (int i = 0; i < arr.length - 1; i++) {
            arr[i] = arr[i + 1];
        }
        arr[arr.length - 1] = birinchi;
        
        System.out.println("Chapga 1 qadam surilgan: " + Arrays.toString(arr));
    }
}
```

## Tushuntirish va Mantiq:
Birinchi element `birinchi` o'zgaruvchisiga saqlab olinadi.
So'ngra sikl orqali har bir `i` yacheykaga o'ngdagi `i + 1` qiymati ko'chiriladi.
Eng oxirgi yacheykaga esa birinchi element yoziladi.

## Ishlash natijasi:
```text
Chapga 1 qadam surilgan: [20, 30, 40, 50, 10]
```

---

# 121-Topshiriq: Massiv elementlarini k qadam o'ngga aylanma siljitish (Cyclic Rotation)

## Topshiriq sharti:
Massivni `k` qadam aylanma o'ngga siljitish algoritmini Reverse (teskari o'girish) usulida O(N) vaqt va O(1) xotirada bajaring.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void rotate(int[] nums, int k) {
        int n = nums.length;
        k = k % n;
        
        reverse(nums, 0, n - 1);
        reverse(nums, 0, k - 1);
        reverse(nums, k, n - 1);
    }
    
    private static void reverse(int[] nums, int start, int end) {
        while (start < end) {
            int temp = nums[start];
            nums[start] = nums[end];
            nums[end] = temp;
            start++;
            end--;
        }
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5, 6, 7};
        rotate(arr, 3);
        System.out.println("3 qadam o'ngga siljitilgan: " + Arrays.toString(arr));
    }
}
```

## Tushuntirish va Mantiq:
3 marta teskari o'girish (Reversal algorithm):
1. Butun massivni teskari o'giramiz: `[7, 6, 5, 4, 3, 2, 1]`
2. Dastlabki `k` ta elementni teskari o'giramiz: `[5, 6, 7, 4, 3, 2, 1]`
3. Qolgan elementlarni teskari o'giramiz: `[5, 6, 7, 1, 2, 3, 4]`.
Bu optimal usul qo'shimcha massiv talab qilmaydi.

## Ishlash natijasi:
```text
3 qadam o'ngga siljitilgan: [5, 6, 7, 1, 2, 3, 4]
```

---

# 122-Topshiriq: Massivlarni nusxalash: System.arraycopy()

## Topshiriq sharti:
Java-dagi eng tezkor mahalliy (native) massiv nusxalash vositasi `System.arraycopy()` dan foydalaning.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[] manba = {10, 20, 30, 40, 50};
        int[] nishon = new int[5];
        
        // manba dan 1-indeksdan boshlab 3 ta elementni nishon ning 2-indeksiga nusxalash
        System.arraycopy(manba, 1, nishon, 2, 3);
        
        System.out.println("Nishon massivi: " + Arrays.toString(nishon));
    }
}
```

## Tushuntirish va Mantiq:
`System.arraycopy()` Java-da massiv nusxalashning eng tezkor usuli hisoblanadi, chunki u C++ darajasidagi to'g'ridan-to'g'ri xotira bloklarini ko'chirish (memmove) orqali ishlaydi.

## Ishlash natijasi:
```text
Nishon massivi: [0, 0, 20, 30, 40]
```

---

# 123-Topshiriq: Arrays.copyOf va Arrays.copyOfRange metodlari

## Topshiriq sharti:
`Arrays.copyOf()` orqali massiv hajmini oshirish va `copyOfRange()` orqali ma'lum oraliqni kesib olishni ko'rsating.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[] sonlar = {1, 2, 3};
        
        // Massiv hajmini 5 taga kengaytirish
        int[] kengaytirilgan = Arrays.copyOf(sonlar, 5);
        System.out.println("Kengaytirilgan: " + Arrays.toString(kengaytirilgan));
        
        // 1-indeksdan 4-indeksgacha (4 kirmaydi) kesib olish
        int[] qism = Arrays.copyOfRange(kengaytirilgan, 1, 4);
        System.out.println("Kesib olingan oraliq: " + Arrays.toString(qism));
    }
}
```

## Tushuntirish va Mantiq:
`Arrays.copyOf()` yangi massiv yaratadi va eski ma'lumotlarni unga ko'chiradi. Agar yangi hajm kattaroq bo'lsa, qolgan joylar 0 bilan to'ldiriladi. Bu `ArrayList` ning ichki kengayish mexanizmining asosidir.

## Ishlash natijasi:
```text
Kengaytirilgan: [1, 2, 3, 0, 0]
Kesib olingan oraliq: [2, 3, 0]
```

---

# 124-Topshiriq: Massivlarni taqqoslash: Arrays.equals() vs ==

## Topshiriq sharti:
Nima sababdan `==` massivlar uchun ishlamasligini va to'g'ri taqqoslash uchun `Arrays.equals()` qo'llanilishini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = {1, 2, 3};
        
        System.out.println("a == b (manzillar solishtiriladi): " + (a == b));
        System.out.println("Arrays.equals(a, b) (elementlar solishtiriladi): " + Arrays.equals(a, b));
    }
}
```

## Tushuntirish va Mantiq:
Massivlar ob'ekt bo'lgani uchun `a == b` ularning Heap xotiradagi manzillarini solishtiradi va ikkita mustaqil massiv uchun har doim `false` beradi.
`Arrays.equals()` esa ularning uzunligi va har bir indeksdagi elementlari bir-biriga tengligini tekshiradi.

## Ishlash natijasi:
```text
a == b (manzillar solishtiriladi): false
Arrays.equals(a, b) (elementlar solishtiriladi): true
```

---

# 125-Topshiriq: Arrays.fill() bilan massivni to'ldirish

## Topshiriq sharti:
Massivning barcha yacheykalarini yoki ma'lum bir oralig'ini bir xil qiymat bilan to'ldirish dasturini yozing.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[] arr = new int[7];
        
        Arrays.fill(arr, -1);
        System.out.println("To'liq to'ldirilgan: " + Arrays.toString(arr));
        
        // 2-indeksdan 5-indeksgacha 99 bilan to'ldirish
        Arrays.fill(arr, 2, 5, 99);
        System.out.println("Qisman to'ldirilgan: " + Arrays.toString(arr));
    }
}
```

## Tushuntirish va Mantiq:
`Arrays.fill()` massivni initsializatsiya qilishda (masalan, dinamik dasturlash jadvallarini dastlab -1 bilan to'ldirishda) qulay va tezkor hisoblanadi.

## Ishlash natijasi:
```text
To'liq to'ldirilgan: [-1, -1, -1, -1, -1, -1, -1]
Qisman to'ldirilgan: [-1, -1, 99, 99, 99, -1, -1]
```

---

# 126-Topshiriq: Arrays.sort() va Dual-Pivot Quicksort

## Topshiriq sharti:
Java-ning standart `Arrays.sort()` metodidan foydalanib massivni o'sish tartibida saralang.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[] sonlar = {64, 25, 12, 22, 11, 90};
        System.out.println("Saralashdan oldin: " + Arrays.toString(sonlar));
        
        Arrays.sort(sonlar);
        System.out.println("Saralangandan keyin: " + Arrays.toString(sonlar));
    }
}
```

## Tushuntirish va Mantiq:
Primitiv tiplar uchun `Arrays.sort()` Vladimir Yaroslavskiy tomonidan ishlab chiqilgan Dual-Pivot Quicksort algoritmidan foydalanadi.
U klassik Quicksort ga qaraganda ancha tez ishlaydi va O(N log N) vaqt murakkabligini ta'minlaydi.

## Ishlash natijasi:
```text
Saralashdan oldin: [64, 25, 12, 22, 11, 90]
Saralangandan keyin: [11, 12, 22, 25, 64, 90]
```

---

# 127-Topshiriq: Arrays.binarySearch() ning manfiy natijasi siri

## Topshiriq sharti:
Standart `Arrays.binarySearch()` metodi qidirilayotgan element topilmaganda qanday qiymat (`-(insertion point) - 1`) qaytarishini tahlil qiling.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[] saralangan = {10, 20, 30, 40, 50};
        
        int topilgan = Arrays.binarySearch(saralangan, 30);
        int topilmagan = Arrays.binarySearch(saralangan, 25);
        
        System.out.println("30 soni indeksi: " + topilgan);
        System.out.println("25 soni qidiruv natijasi: " + topilmagan);
        
        int qoyilishiKerakBolganIndeks = -topilmagan - 1;
        System.out.println("25 soni tartib buzilmasdan tushishi kerak bo'lgan indeks: " + qoyilishiKerakBolganIndeks);
    }
}
```

## Tushuntirish va Mantiq:
`Arrays.binarySearch()` agar element massivda bo'lmasa, manfiy qiymat qaytaradi: `-(joylashtirish_indeksi) - 1`.
Bu dasturchiga yangi elementni saralangan massivning aynan qaysi o'rniga qo'yish kerakligini darhol hisoblash imkonini beradi.

## Ishlash natijasi:
```text
30 soni indeksi: 2
25 soni qidiruv natijasi: -3
25 soni tartib buzilmasdan tushishi kerak bo'lgan indeks: 2
```

---

# 128-Topshiriq: Arrays.mismatch() metodi (Java 9+)

## Topshiriq sharti:
Ikkita massiv bir-biridan qaysi birinchi indeksda farq qilishini `Arrays.mismatch()` orqali aniqlang.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[] a = {1, 2, 3, 4, 5};
        int[] b = {1, 2, 3, 9, 5};
        int[] c = {1, 2, 3, 4, 5};
        
        System.out.println("a va b farqlangan indeks: " + Arrays.mismatch(a, b));
        System.out.println("a va c solishtirilganda (to'liq teng bo'lsa): " + Arrays.mismatch(a, c));
    }
}
```

## Tushuntirish va Mantiq:
Java 9 da qo'shilgan `Arrays.mismatch()` ikkita massivni solishtiradi va ular birinchi marta farq qilgan indeksni qaytaradi.
Agar ikkala massiv to'liq bir xil bo'lsa, `-1` qaytaradi. Bu massivlarni solishtirishni tezlashtiradi.

## Ishlash natijasi:
```text
a va b farqlangan indeks: 3
a va c solishtirilganda (to'liq teng bo'lsa): -1
```

---

# 129-Topshiriq: Arrays.compare() leksikografik taqqoslash (Java 9+)

## Topshiriq sharti:
Ikkita massivni alifbo/tartib (leksikografik) bo'yicha taqqoslash dasturini yozing.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = {1, 2, 4};
        int[] c = {1, 2, 3};
        
        System.out.println("compare(a, b): " + Arrays.compare(a, b));
        System.out.println("compare(b, a): " + Arrays.compare(b, a));
        System.out.println("compare(a, c): " + Arrays.compare(a, c));
    }
}
```

## Tushuntirish va Mantiq:
`Arrays.compare()` leksikografik taqqoslashni amalga oshiradi:
- Agar birinchi massiv kichik bo'lsa: manfiy son (< 0)
- Agar birinchi massiv katta bo'lsa: musbat son (> 0)
- Agar ikkalasi teng bo'lsa: `0` qaytaradi.

## Ishlash natijasi:
```text
compare(a, b): -1
compare(b, a): 1
compare(a, c): 0
```

---

# 130-Topshiriq: 2D massiv (Matritsa) asoslari va xotira strukturasi

## Topshiriq sharti:
3x3 o'lchamli 2D matritsa yaratib, unga qiymatlar yozish va ekranga jadval ko'rinishida chiqarish dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[][] matritsa = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        
        System.out.println("2D Matritsa ko'rinishi:");
        for (int i = 0; i < matritsa.length; i++) {
            for (int j = 0; j < matritsa[i].length; j++) {
                System.out.print(matritsa[i][j] + "	");
            }
            System.out.println();
        }
    }
}
```

## Tushuntirish va Mantiq:
Java-da haqiqiy ko'p o'lchovli bitta tekis massiv yo'q. 2D massiv aslida massivlarning massividir (array of arrays).
Tashqi massiv Heap xotirada qatorlarga havola saqlaydi, har bir qator esa mustaqil 1D massiv obyektidir.

## Ishlash natijasi:
```text
2D Matritsa ko'rinishi:
1	2	3	
4	5	6	
7	8	9
```

---

# 131-Topshiriq: Matritsa diagonallari yig'indisi

## Topshiriq sharti:
Kvadrat matritsaning bosh (asosiy) va yordamchi diagonallari yig'indisini bitta siklda hisoblang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[][] m = {
            {2, 1, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        
        int asosiyYigindi = 0;
        int yordamchiYigindi = 0;
        int n = m.length;
        
        for (int i = 0; i < n; i++) {
            asosiyYigindi += m[i][i];
            yordamchiYigindi += m[i][n - 1 - i];
        }
        
        System.out.println("Asosiy diagonal yig'indisi: " + asosiyYigindi);
        System.out.println("Yordamchi diagonal yig'indisi: " + yordamchiYigindi);
    }
}
```

## Tushuntirish va Mantiq:
Asosiy diagonalda `i == j` bo'ladi.
Yordamchi diagonalda esa ustun indeksi `n - 1 - i` ga teng bo'ladi.
Bitta `for` sikli bilan ikkala diagonalni ham O(N) vaqtda hisoblash mumkin.

## Ishlash natijasi:
```text
Asosiy diagonal yig'indisi: 16
Yordamchi diagonal yig'indisi: 15
```

---

# 132-Topshiriq: Matritsani transponirlash (Matrix Transpose)

## Topshiriq sharti:
Matritsa qatorlari va ustunlari o'rnini almashtirib (transponirlab) yangi matritsa hosil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[][] original = {
            {1, 2, 3},
            {4, 5, 6}
        }; // 2x3 o'lcham
        
        int qator = original.length;
        int ustun = original[0].length;
        int[][] transponirlangan = new int[ustun][qator]; // 3x2 o'lcham
        
        for (int i = 0; i < qator; i++) {
            for (int j = 0; j < ustun; j++) {
                transponirlangan[j][i] = original[i][j];
            }
        }
        
        System.out.println("Transponirlangan matritsa (3x2):");
        for (int[] q : transponirlangan) {
            for (int val : q) {
                System.out.print(val + " ");
            }
            System.out.println();
        }
    }
}
```

## Tushuntirish va Mantiq:
Transponirlashda `A[i][j]` elementi `A_T[j][i]` o'rniga o'tadi.
Dastlabki matritsa `N x M` bo'lsa, yangi transponirlangan matritsa `M x N` o'lchamga ega bo'ladi.

## Ishlash natijasi:
```text
Transponirlangan matritsa (3x2):
1 4 
2 5 
3 6
```

---

# 133-Topshiriq: Ikki matritsani qo'shish

## Topshiriq sharti:
Bir xil o'lchamdagi ikkita 2D matritsaning mos elementlarini qo'shib natijaviy matritsa hosil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[][] a = {
            {1, 2},
            {3, 4}
        };
        int[][] b = {
            {5, 6},
            {7, 8}
        };
        
        int[][] yigindi = new int[2][2];
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                yigindi[i][j] = a[i][j] + b[i][j];
            }
        }
        
        System.out.println("Matritsalar yig'indisi:");
        for (int[] row : yigindi) {
            System.out.println(row[0] + " " + row[1]);
        }
    }
}
```

## Tushuntirish va Mantiq:
Matritsalarni qo'shish uchun ularning o'lchamlari aynan bir xil bo'lishi shart.
Natijaviy matritsaning `(i, j)` elementi `a[i][j] + b[i][j]` ga teng bo'ladi.

## Ishlash natijasi:
```text
Matritsalar yig'indisi:
6 8
10 12
```

---

# 134-Topshiriq: Ikki matritsani ko'paytirish (Matrix Multiplication)

## Topshiriq sharti:
Chiziqli algebraning matritsalarni ko'paytirish qoidasi bo'yicha A (2x3) va B (3x2) matritsalar ko'paytmasini hisoblang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[][] A = {
            {1, 2, 3},
            {4, 5, 6}
        }; // 2x3
        
        int[][] B = {
            {7, 8},
            {9, 1},
            {2, 3}
        }; // 3x2
        
        int[][] C = new int[2][2]; // 2x2
        
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                for (int k = 0; k < 3; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        
        System.out.println("A x B ko'paytma matritsa:");
        for (int[] qator : C) {
            System.out.println(qator[0] + "	" + qator[1]);
        }
    }
}
```

## Tushuntirish va Mantiq:
Matritsalarni ko'paytirish sharti: A ning ustunlar soni B ning qatorlar soniga teng bo'lishi kerak.
`C[i][j]` elementi A ning i-qatori bilan B ning j-ustunining skalyar ko'paytmasidan iborat bo'ladi.
Uch karra ichma-ich sikl orqali O(N^3) murakkablikda bajariladi.

## Ishlash natijasi:
```text
A x B ko'paytma matritsa:
31	19
85	55
```

---

# 135-Topshiriq: Jagged (Zinasimon) massivlar

## Topshiriq sharti:
Har bir qatori turlicha uzunlikka ega bo'lgan Jagged massiv yaratish va uni to'ldirish dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[][] zinasimon = new int[3][];
        zinasimon[0] = new int[2]; // 1-qator 2 ta
        zinasimon[1] = new int[4]; // 2-qator 4 ta
        zinasimon[2] = new int[1]; // 3-qator 1 ta
        
        int qiymat = 1;
        for (int i = 0; i < zinasimon.length; i++) {
            for (int j = 0; j < zinasimon[i].length; j++) {
                zinasimon[i][j] = qiymat++;
            }
        }
        
        System.out.println("Jagged massiv:");
        for (int[] qator : zinasimon) {
            for (int x : qator) {
                System.out.print(x + " ");
            }
            System.out.println();
        }
    }
}
```

## Tushuntirish va Mantiq:
Java-da `new int[3][]` e'lon qilinganda ikkinchi qavs bo'sh qoldiriladi.
So'ngra har bir qatorga ixtiyoriy o'lchamdagi mustaqil 1D massiv biriktiriladi.
Bu xotirani behuda sarflamaslik (masalan, uchburchak ma'lumotlar saqlash) uchun juda qulaydir.

## Ishlash natijasi:
```text
Jagged massiv:
1 2 
3 4 5 6 
7
```

---

# 136-Topshiriq: Paskal uchburchagini jagged massivda hosil qilish

## Topshiriq sharti:
Jagged massiv yordamida N qatorli Paskal uchburchagini generatsiya qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int n = 5;
        int[][] paskal = new int[n][];
        
        for (int i = 0; i < n; i++) {
            paskal[i] = new int[i + 1];
            paskal[i][0] = 1;
            paskal[i][i] = 1;
            
            for (int j = 1; j < i; j++) {
                paskal[i][j] = paskal[i - 1][j - 1] + paskal[i - 1][j];
            }
        }
        
        System.out.println("Paskal uchburchagi:");
        for (int[] qator : paskal) {
            for (int son : qator) {
                System.out.print(son + " ");
            }
            System.out.println();
        }
    }
}
```

## Tushuntirish va Mantiq:
Paskal uchburchagida har bir qatorning chetlari `1` ga teng, o'rtadagi elementlar esa yuqoridagi ikkita qo'shni element yig'indisidan hosil bo'ladi: `paskal[i][j] = paskal[i-1][j-1] + paskal[i-1][j]`.

## Ishlash natijasi:
```text
Paskal uchburchagi:
1 
1 1 
1 2 1 
1 3 3 1 
1 4 6 4 1
```

---

# 137-Topshiriq: 2D massivlarni chop etish: Arrays.deepToString()

## Topshiriq sharti:
Ko'p o'lchovli massivlarni bitta qatorda to'liq o'qish uchun `Arrays.deepToString()` utilitasidan foydalaning.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[][] matrix = {
            {10, 20},
            {30, 40}
        };
        
        // Oddiy toString xotira xeshini chiqaradi
        System.out.println("Oddiy toString: " + Arrays.toString(matrix));
        
        // deepToString barcha ichki massivlarni chiroyli ko'rsatadi
        System.out.println("deepToString: " + Arrays.deepToString(matrix));
    }
}
```

## Tushuntirish va Mantiq:
`Arrays.toString()` faqat 1D massivlar uchun mo'ljallangan. 2D massivga qo'llanganda ichki massivlarning ob'ekt manzillarini chiqaradi (masalan, `[[I@1b6d3586...`).
`Arrays.deepToString()` rekursiv tarzda barcha qatlamlarni ochib, to'liq qiymatlarni chiqaradi.

## Ishlash natijasi:
```text
Oddiy toString: [[I@...
deepToString: [[10, 20], [30, 40]]
```

---

# 138-Topshiriq: 2D massivlarni chuqur taqqoslash: Arrays.deepEquals()

## Topshiriq sharti:
Ko'p o'lchovli massivlarning barcha ichki elementlari bir-biriga tengligini tekshiring.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void main(String[] args) {
        int[][] m1 = {{1, 2}, {3, 4}};
        int[][] m2 = {{1, 2}, {3, 4}};
        
        System.out.println("Arrays.equals: " + Arrays.equals(m1, m2));
        System.out.println("Arrays.deepEquals: " + Arrays.deepEquals(m1, m2));
    }
}
```

## Tushuntirish va Mantiq:
`Arrays.equals()` 2D massivda faqat 1-darajali havolalarni tekshiradi va ular turli obyektlar bo'lgani uchun `false` beradi.
`Arrays.deepEquals()` esa ichki barcha qatorlarni rekursiv solishtirib, haqiqiy tenglikni aniqlaydi.

## Ishlash natijasi:
```text
Arrays.equals: false
Arrays.deepEquals: true
```

---

# 139-Topshiriq: 2D massivni klonlash: Shallow Copy muammosi va Deep Copy

## Topshiriq sharti:
`matrix.clone()` ning faqat yuzaki nusxa (shallow copy) olishini va chinakam mustaqil (deep copy) nusxa olish yo'lini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[][] asl = {{1, 2}, {3, 4}};
        int[][] yuzaki = asl.clone();
        
        // Yuzaki nusxaning ichki elementini o'zgartirish
        yuzaki[0][0] = 99;
        System.out.println("Asl massiv [0][0] ham o'zgarib qoldi: " + asl[0][0]);
        
        // To'g'ri Deep Copy
        int[][] chuqur = new int[asl.length][];
        for (int i = 0; i < asl.length; i++) {
            chuqur[i] = asl[i].clone();
        }
        chuqur[0][0] = 55;
        System.out.println("Chuqur nusxa o'zgarganda asl massiv daxlsiz: " + asl[0][0]);
    }
}
```

## Tushuntirish va Mantiq:
Massivning `.clone()` metodi 2D massivda faqat tashqi massivni nusxalaydi, ichki qatorlar esa o'sha eski xotira manzillariga ko'rsatib qoladi (Shallow copy).
Haqiqiy Deep copy uchun har bir qator alohida klonlanishi yoki yangidan yaratilishi kerak.

## Ishlash natijasi:
```text
Asl massiv [0][0] ham o'zgarib qoldi: 99
Chuqur nusxa o'zgarganda asl massiv daxlsiz: 99
```

---

# 140-Topshiriq: Pufakchali saralash (Bubble Sort) algoritmi

## Topshiriq sharti:
Eng mashhur pufakchali saralash algoritmini bayroqcha (flag) orqali optimallashtirilgan holda yozing.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            boolean almashtirildimi = false;
            for (int j = 0; j < n - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    almashtirildimi = true;
                }
            }
            if (!almashtirildimi) break; // Agar almashtirish bo'lmasa, massiv allaqachon saralangan!
        }
    }

    public static void main(String[] args) {
        int[] sonlar = {64, 34, 25, 12, 22, 11, 90};
        bubbleSort(sonlar);
        System.out.println("Bubble sort natijasi: " + Arrays.toString(sonlar));
    }
}
```

## Tushuntirish va Mantiq:
Pufakchali saralash qo'shni elementlarni solishtirib, kattasini o'ng tomonga siljitadi.
`almashtirildimi` bayrog'i qo'shilishi orqali eng yaxshi holatdagi vaqt O(N) ga tushadi (aks holda har doim O(N^2) bo'lar edi).

## Ishlash natijasi:
```text
Bubble sort natijasi: [11, 12, 22, 25, 34, 64, 90]
```

---

# 141-Topshiriq: Tanlash orqali saralash (Selection Sort) algoritmi

## Topshiriq sharti:
Har bir iteratsiyada qolgan qismning eng kichik elementini topib boshiga qo'yuvchi Selection Sort algoritmini tuzing.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void selectionSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int minIndeks = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndeks]) {
                    minIndeks = j;
                }
            }
            int temp = arr[minIndeks];
            arr[minIndeks] = arr[i];
            arr[i] = temp;
        }
    }

    public static void main(String[] args) {
        int[] arr = {29, 10, 14, 37, 13};
        selectionSort(arr);
        System.out.println("Selection sort natijasi: " + Arrays.toString(arr));
    }
}
```

## Tushuntirish va Mantiq:
Selection Sort saralanmagan qismdan minimal elementning indeksini topadi va uni i-o'rindagi element bilan almashtiradi.
Almashtirishlar (swaps) soni jami N-1 ta bo'lgani sababli, xotiraga yozish amali juda kam bajariladi.

## Ishlash natijasi:
```text
Selection sort natijasi: [10, 13, 14, 29, 37]
```

---

# 142-Topshiriq: Qo'yish orqali saralash (Insertion Sort) algoritmi

## Topshiriq sharti:
Karta o'yinida qo'ldagi kartalarni tartiblash kabi ishlovchi Insertion Sort algoritmini yozing.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void insertionSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int kalit = arr[i];
            int j = i - 1;
            
            while (j >= 0 && arr[j] > kalit) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = kalit;
        }
    }

    public static void main(String[] args) {
        int[] arr = {12, 11, 13, 5, 6};
        insertionSort(arr);
        System.out.println("Insertion sort natijasi: " + Arrays.toString(arr));
    }
}
```

## Tushuntirish va Mantiq:
Insertion Sort kichik o'lchamli yoki deyarli saralangan massivlar uchun eng tezkor algoritmlardan biridir.
Java-ning o'zida ham qisqa massivlarni saralashda ichki qismda Insertion Sort ishlatiladi.

## Ishlash natijasi:
```text
Insertion sort natijasi: [5, 6, 11, 12, 13]
```

---

# 143-Topshiriq: Ikki saralangan massivni birlashtirish (Merge Step)

## Topshiriq sharti:
Ikkita allaqachon saralangan massivni bitta yangi saralangan massivga O(N + M) vaqtda birlashtiring.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static int[] merge(int[] a, int[] b) {
        int[] res = new int[a.length + b.length];
        int i = 0, j = 0, k = 0;
        
        while (i < a.length && j < b.length) {
            if (a[i] <= b[j]) res[k++] = a[i++];
            else res[k++] = b[j++];
        }
        
        while (i < a.length) res[k++] = a[i++];
        while (j < b.length) res[k++] = b[j++];
        
        return res;
    }

    public static void main(String[] args) {
        int[] m1 = {1, 3, 5, 7};
        int[] m2 = {2, 4, 6, 8, 10};
        int[] birlashgan = merge(m1, m2);
        System.out.println("Birlashtirilgan saralangan massiv: " + Arrays.toString(birlashgan));
    }
}
```

## Tushuntirish va Mantiq:
Bu amaliyot Merge Sort (birlashtirib saralash) algoritmining asosiy bosqichi hisoblanadi.
Ikkala massiv ko'rsatkichlari solishtirilib, kichigi yangi massivga yozib boriladi. Vaqt murakkabligi: O(N + M).

## Ishlash natijasi:
```text
Birlashtirilgan saralangan massiv: [1, 2, 3, 4, 5, 6, 7, 8, 10]
```

---

# 144-Topshiriq: Massivdagi ikkinchi eng katta elementni topish

## Topshiriq sharti:
Massivni saralamasdan, bitta sikl davomida ikkinchi eng katta (second largest) elementni toping.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[] arr = {12, 35, 1, 10, 34, 1};
        
        int birinchi = Integer.MIN_VALUE;
        int ikkinchi = Integer.MIN_VALUE;
        
        for (int son : arr) {
            if (son > birinchi) {
                ikkinchi = birinchi;
                birinchi = son;
            } else if (son > ikkinchi && son != birinchi) {
                ikkinchi = son;
            }
        }
        
        System.out.println("Eng katta: " + birinchi);
        System.out.println("Ikkinchi eng katta: " + ikkinchi);
    }
}
```

## Tushuntirish va Mantiq:
Massivni saralash O(N log N) vaqt oladi.
Ushbu bitta siklli yondashuv esa masalani O(N) vaqt va O(1) xotirada hal qiladi.
Yangi maksimal topilganda eski maksimal darhol ikkinchi o'ringa suriladi.

## Ishlash natijasi:
```text
Eng katta: 35
Ikkinchi eng katta: 34
```

---

# 145-Topshiriq: Nollarni massiv oxiriga surish (Move Zeroes)

## Topshiriq sharti:
Massivdagi barcha 0 larni uning oxiriga suruvchi va qolgan sonlar tartibini saqlovchi in-place dastur yozing.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void moveZeroes(int[] nums) {
        int nolsizIndeks = 0;
        
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != 0) {
                nums[nolsizIndeks++] = nums[i];
            }
        }
        
        while (nolsizIndeks < nums.length) {
            nums[nolsizIndeks++] = 0;
        }
    }

    public static void main(String[] args) {
        int[] sonlar = {0, 1, 0, 3, 12};
        moveZeroes(sonlar);
        System.out.println("Nollar oxiriga surilgan: " + Arrays.toString(sonlar));
    }
}
```

## Tushuntirish va Mantiq:
Dastlab barcha 0 bo'lmagan elementlar oldinga ketma-ket yoziladi.
So'ngra qolgan barcha bo'sh o'rinlar 0 lar bilan to'ldiriladi.
Vaqt murakkabligi: O(N), qo'shimcha xotira sarfi: O(1).

## Ishlash natijasi:
```text
Nollar oxiriga surilgan: [1, 3, 12, 0, 0]
```

---

# 146-Topshiriq: Kadane algoritmi: Eng katta yig'indiga ega qism-massiv

## Topshiriq sharti:
Manfiy va musbat sonlar aralash kelgan massivda ketma-ket joylashgan maksimal yig'indili qism-massiv yig'indisini toping.

## Yechim (Java kodi):
```java
public class Solution {
    public static int maxSubArray(int[] nums) {
        int maxJami = nums[0];
        int joriyYigindi = nums[0];
        
        for (int i = 1; i < nums.length; i++) {
            joriyYigindi = Math.max(nums[i], joriyYigindi + nums[i]);
            maxJami = Math.max(maxJami, joriyYigindi);
        }
        
        return maxJami;
    }

    public static void main(String[] args) {
        int[] arr = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        int maksimal = maxSubArray(arr);
        System.out.println("Maksimal qism-massiv yig'indisi: " + maksimal);
    }
}
```

## Tushuntirish va Mantiq:
Kadane algoritmi dinamik dasturlash tamoyiliga asoslangan.
Har bir qadamda yangi elementdan yangi qism-massiv boshlash yoki mavjud qism-massivga qo'shilish qarori qabul qilinadi: `Math.max(nums[i], joriy + nums[i])`.
O(N) vaqtda ishlaydi.

## Ishlash natijasi:
```text
Maksimal qism-massiv yig'indisi: 6
```

---

# 147-Topshiriq: Saralangan massivda yig'indisi K ga teng juftlikni topish (Two Sum)

## Topshiriq sharti:
Saralangan massivda berilgan `target` ga teng bo'lgan ikki elementni Two Pointers usuli bilan O(N) vaqtda toping.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[] saralangan = {2, 7, 11, 15, 20};
        int target = 22; // 7 + 15
        
        int chap = 0;
        int ong = saralangan.length - 1;
        boolean topildi = false;
        
        while (chap < ong) {
            int yigindi = saralangan[chap] + saralangan[ong];
            if (yigindi == target) {
                System.out.println("Topildi: " + saralangan[chap] + " + " + saralangan[ong] + " = " + target);
                topildi = true;
                break;
            } else if (yigindi < target) {
                chap++;
            } else {
                ong--;
            }
        }
        
        if (!topildi) System.out.println("Bunday juftlik yo'q");
    }
}
```

## Tushuntirish va Mantiq:
Agar yig'indi kichik bo'lsa, `chap` ko'rsatkichni oshirib kattaroq songa o'tiladi.
Agar yig'indi katta bo'lsa, `ong` ko'rsatkichni kamaytirib kichikroq songa o'tiladi.
Bu ikki ko'rsatkich usulining eng go'zal amaliy namunasidir.

## Ishlash natijasi:
```text
Topildi: 7 + 15 = 22
```

---

# 148-Topshiriq: 2D kvadrat matritsani 90 gradusga burish (Rotate Matrix)

## Topshiriq sharti:
N x N o'lchamli matritsani soat mili bo'yicha 90 gradusga buruvchi in-place algoritmni yozing.

## Yechim (Java kodi):
```java
import java.util.Arrays;

public class Solution {
    public static void rotate(int[][] matrix) {
        int n = matrix.length;
        
        // 1-qadam: Transponirlash
        for (int i = 0; i < n; i++) {
            for (int j = i; j < n; j++) {
                int temp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = temp;
            }
        }
        
        // 2-qadam: Har bir qatorni teskari o'girish
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n / 2; j++) {
                int temp = matrix[i][j];
                matrix[i][j] = matrix[i][n - 1 - j];
                matrix[i][n - 1 - j] = temp;
            }
        }
    }

    public static void main(String[] args) {
        int[][] m = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        rotate(m);
        System.out.println("90 gradusga burilgan matritsa:");
        for (int[] row : m) {
            System.out.println(Arrays.toString(row));
        }
    }
}
```

## Tushuntirish va Mantiq:
Matritsani 90 gradusga o'ngga burish formulasi:
1. Matritsani bosh diagonal bo'yicha transponirlash.
2. Har bir qatorning elementlarini gorizontal teskari o'girish (reverse).
Hech qanday qo'shimcha matritsa talab qilinmaydi (in-place).

## Ishlash natijasi:
```text
90 gradusga burilgan matritsa:
[7, 4, 1]
[8, 5, 2]
[9, 6, 3]
```

---

# 149-Topshiriq: Massivda yetishmayotgan sonni topish (Missing Number)

## Topshiriq sharti:
0 dan n gacha bo'lgan sonlar ichidan bitta yetishmayotgan sonni arifmetik progressiya yoki XOR yordamida O(N) vaqtda toping.

## Yechim (Java kodi):
```java
public class Solution {
    public static int findMissing(int[] nums) {
        int n = nums.length;
        int kutilganYigindi = n * (n + 1) / 2;
        int haqiqiyYigindi = 0;
        
        for (int x : nums) {
            haqiqiyYigindi += x;
        }
        
        return kutilganYigindi - haqiqiyYigindi;
    }

    public static void main(String[] args) {
        int[] sonlar = {3, 0, 1}; // 0 dan 3 gacha, 2 soni yetishmayapti
        System.out.println("Yetishmayotgan son: " + findMissing(sonlar));
    }
}
```

## Tushuntirish va Mantiq:
Gauss formulasi bo'yicha 0 dan N gacha sonlar yig'indisi `N * (N + 1) / 2` bo'ladi.
Kutilgan yig'indidan massivdagi barcha sonlarning haqiqiy yig'indisini ayirilsa, yetishmayotgan son darhol topiladi.

## Ishlash natijasi:
```text
Yetishmayotgan son: 2
```

---

# 150-Topshiriq: Xulosa topshiriq: Spiral (chig'anoq) shaklida N x N matritsani to'ldirish

## Topshiriq sharti:
Berilgan N soni uchun N x N matritsani 1 dan N^2 gacha bo'lgan sonlar bilan spiral ko'rinishida soat mili bo'yicha to'ldiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int n = 4;
        int[][] spiral = new int[n][n];
        
        int tepa = 0, past = n - 1;
        int chap = 0, ong = n - 1;
        int qiymat = 1;
        
        while (tepa <= past && chap <= ong) {
            // Chapdan o'ngga
            for (int j = chap; j <= ong; j++) spiral[tepa][j] = qiymat++;
            tepa++;
            
            // Tepadang pastga
            for (int i = tepa; i <= past; i++) spiral[i][ong] = qiymat++;
            ong--;
            
            // O'ngdan chapga
            if (tepa <= past) {
                for (int j = ong; j >= chap; j--) spiral[past][j] = qiymat++;
                past--;
            }
            
            // Pastdan tepaga
            if (chap <= ong) {
                for (int i = past; i >= tepa; i--) spiral[i][chap] = qiymat++;
                chap++;
            }
        }
        
        System.out.println("4x4 Spiral Matritsa:");
        for (int[] row : spiral) {
            for (int val : row) {
                System.out.printf("%4d", val);
            }
            System.out.println();
        }
    }
}
```

## Tushuntirish va Mantiq:
Ushbu murakkab algoritm 4 ta harakat yo'nalishini (o'ngga, pastga, chapga, tepaga) boshqaruvchi 4 ta chegara ko'rsatkichidan (`tepa`, `past`, `chap`, `ong`) foydalanadi.
Har bir yo'nalish tugagach tegishli chegara toraytiriladi va butun jadval spiral tarzida to'ldiriladi.

## Ishlash natijasi:
```text
4x4 Spiral Matritsa:
   1   2   3   4
  12  13  14   5
  11  16  15   6
  10   9   8   7
```
