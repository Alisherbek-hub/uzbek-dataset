# Java Operatorlar va Boshqaruv Oqimlari (51-100)

# 51-Topshiriq: Arifmetik operatorlar va qoldiqli bo'lish

## Topshiriq sharti:
Java-da asosiy arifmetik amallar (`+`, `-`, `*`, `/`, `%`) va ayniqsa qoldiq olish (`%`) operatorining manfiy sonlardagi xulqini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int a = 17;
        int b = 5;
        
        System.out.println("Qo'shish: " + (a + b));
        System.out.println("Ayirish: " + (a - b));
        System.out.println("Ko'paytirish: " + (a * b));
        System.out.println("Butun bo'lish (17 / 5): " + (a / b));
        System.out.println("Qoldiq (17 % 5): " + (a % b));
        
        // Manfiy sonlarda qoldiq
        System.out.println("-17 % 5 = " + (-17 % 5));
        System.out.println("17 % -5 = " + (17 % -5));
    }
}
```

## Tushuntirish va Mantiq:
Java-da butun sonli bo'lish (`/`) kasr qismini e'tiborsiz qoldiradi va faqat butun natijani qaytaradi.
Qoldiq olish operatori (`%`) da natijaning ishorasi faqat chap tomondagi dividend (bo'linuvchi) ishorasiga bog'liq.
Shu sababli `-17 % 5` natijasi `-2` bo'ladi, `17 % -5` esa musbat `2` bo'ladi.

## Ishlash natijasi:
```text
Qo'shish: 22
Ayirish: 12
Ko'paytirish: 85
Butun bo'lish (17 / 5): 3
Qoldiq (17 % 5): 2
-17 % 5 = -2
17 % -5 = 2
```

---

# 52-Topshiriq: Butun sonlarda nolga bo'lish va ArithmeticException

## Topshiriq sharti:
Butun sonlarda nolga bo'lish paytida yuz beradigan `ArithmeticException` ni tutib olish dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int a = 10;
        int b = 0;
        
        try {
            int natija = a / b;
            System.out.println("Natija: " + natija);
        } catch (ArithmeticException e) {
            System.out.println("Xatolik ushlandi: " + e.getMessage());
            System.out.println("Istisno sinfi: " + e.getClass().getSimpleName());
        }
    }
}
```

## Tushuntirish va Mantiq:
Java-da butun sonlar ustida nolga bo'lish (`a / 0` yoki `a % 0`) JVM tomonidan taqiqlanadi va `ArithmeticException: / by zero` tashlanadi.
Suzuvchi nuqtali sonlardan farqli o'laroq (ular `Infinity` beradi), butun sonlarda bu qat'iy dasturiy xato hisoblanadi va `try-catch` yoki shartli tekshirish orqali oldi olinishi shart.

## Ishlash natijasi:
```text
Xatolik ushlandi: / by zero
Istisno sinfi: ArithmeticException
```

---

# 53-Topshiriq: Prefiks va Postfiks inkrement farqi

## Topshiriq sharti:
`++x` va `x++` operatorlarining ifoda ichida qatnashganda qiymat qaytarish ketma-ketligidagi tub farqlarini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int x = 5;
        int a = ++x; // Prefiks: oldin x oshadi, keyin a ga yoziladi
        System.out.println("Prefiks: x=" + x + ", a=" + a);
        
        int y = 5;
        int b = y++; // Postfiks: oldin y qiymati b ga yoziladi, so'ng y oshadi
        System.out.println("Postfiks: y=" + y + ", b=" + b);
        
        int z = 10;
        int natija = z++ + ++z; // 10 + 12
        System.out.println("Murakkab ifoda natijasi: " + natija + ", z=" + z);
    }
}
```

## Tushuntirish va Mantiq:
Prefiks inkrement (`++x`): Avval o'zgaruvchi qiymati 1 ga oshiriladi, so'ngra yangi qiymat ifodada ishlatiladi.
Postfiks inkrement (`x++`): Avval joriy qiymat ifodaga beriladi, so'ngra o'zgaruvchi xotirada 1 ga oshadi.
`z++ + ++z` ifodasida: birinchi `z++` qiymati 10 bo'ladi (z 11 ga aylanadi), keyin `++z` uni 12 qilib ifodaga 12 beradi. 10 + 12 = 22.

## Ishlash natijasi:
```text
Prefiks: x=6, a=6
Postfiks: y=6, b=5
Murakkab ifoda natijasi: 22, z=12
```

---

# 54-Topshiriq: Prefiks va Postfiks dekrement

## Topshiriq sharti:
`--x` va `x--` operatorlari bilan hisoblashlarni amalga oshiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son = 10;
        System.out.println("Dastlabki: " + son);
        System.out.println("Postfiks dekrement (son--): " + son--);
        System.out.println("Postfiks amalidan keyin: " + son);
        System.out.println("Prefiks dekrement (--son): " + --son);
    }
}
```

## Tushuntirish va Mantiq:
Dekrement operatori qiymatni 1 ga kamaytiradi.
`son--` chop etish vaqtida eski 10 qiymatini chiqaradi, ekranga chiqib bo'lgach xotirada 9 ga aylanadi.
`--son` esa avval 9 ni 8 ga tushiradi va ekranga 8 qiymatini chiqaradi.

## Ishlash natijasi:
```text
Dastlabki: 10
Postfiks dekrement (son--): 10
Postfiks amalidan keyin: 9
Prefiks dekrement (--son): 8
```

---

# 55-Topshiriq: Birikmali tayinlash operatorlari va yashirin kasting

## Topshiriq sharti:
`+=`, `-=`, `*=` kabi compound assignment operatorlarida Java yashirin tarzda kasting qilishini tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        byte b = 10;
        // b = b + 5; // XATO: (b + 5) natijasi int!
        b += 5; // To'g'ri: yashirin ravishda (byte)(b + 5) bajariladi
        System.out.println("byte += 5 natijasi: " + b);
        
        b += 200; // E'tibor bering: 15 + 200 = 215, byte to'lib toshadi!
        System.out.println("Kasting tufayli to'lib toshgan qiymat: " + b);
    }
}
```

## Tushuntirish va Mantiq:
Java-da `E1 op= E2` ifodasi aslida `E1 = (T)((E1) op (E2))` ko'rinishida bajariladi, bu yerda `T` - chap tarafdagi `E1` ning tipidir.
Shu sababli `b += 5` hech qanday xatosiz ishlaydi. Ammo bu xavfli bo'lishi mumkin: agar o'ng tarafdagi son katta bo'lsa, ogohlantirishsiz toraytiruvchi kasting sodir bo'lib ma'lumot buziladi.

## Ishlash natijasi:
```text
byte += 5 natijasi: 15
Kasting tufayli to'lib toshgan qiymat: -41
```

---

# 56-Topshiriq: Taqqoslash operatorlari va ularning qo'llanilishi

## Topshiriq sharti:
Asosiy taqqoslash operatorlari (`==`, `!=`, `>`, `<`, `>=`, `<=`) orqali sonlarni solishtiruvchi dastur yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int yosh = 18;
        
        System.out.println("Voyaga yetganmi (yosh >= 18): " + (yosh >= 18));
        System.out.println("Yosh 20 ga tengmi (yosh == 20): " + (yosh == 20));
        System.out.println("Yosh 0 dan farqlimi (yosh != 0): " + (yosh != 0));
        System.out.println("Yosh 18 dan kichikmi (yosh < 18): " + (yosh < 18));
    }
}
```

## Tushuntirish va Mantiq:
Taqqoslash operatorlari ikkita qiymatni o'zaro solishtiradi va har doim `boolean` (`true` yoki `false`) qiymat hosil qiladi.
Ular shartli operatorlar (`if`, `while`) ning poydevori hisoblanadi. E'tibor bering: tenglikni tekshirish uchun bitta `=` emas, ikkita `==` yoziladi.

## Ishlash natijasi:
```text
Voyaga yetganmi (yosh >= 18): true
Yosh 20 ga tengmi (yosh == 20): false
Yosh 0 dan farqlimi (yosh != 0): true
Yosh 18 dan kichikmi (yosh < 18): false
```

---

# 57-Topshiriq: Short-circuit VA (`&&`) vs Bitwise VA (`&`)

## Topshiriq sharti:
`&&` operatori birinchi shart `false` bo'lganda ikkinchisini tekshirmasligini va bu `NullPointerException` dan saqlashini isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String matn = null;
        
        // Short-circuit: matn != null yolg'on bo'lgani uchun matn.length() chaqirilmaydi
        if (matn != null && matn.length() > 0) {
            System.out.println("Matn mavjud");
        } else {
            System.out.println("Matn bo'sh yoki null (xavfsiz tekshirildi)");
        }
        
        // Agar & ishlatilsa, ikkala tomon ham tekshirilib NullPointerException bo'ladi
    }
}
```

## Tushuntirish va Mantiq:
Short-circuit (qisqa tutashuv) baholash:
`&&` operatorida agar chap tomon `false` bo'lsa, umumiy natija allaqachon `false` ekani aniq, shuning uchun JVM o'ng tomonni umuman bajarmaydi.
Bu juda muhim xususiyat bo'lib, `null` tekshiruvlarida xatoliklarni oldini olishda asosiy xavfsizlik qalqonidir.

## Ishlash natijasi:
```text
Matn bo'sh yoki null (xavfsiz tekshirildi)
```

---

# 58-Topshiriq: Short-circuit YOKI (`||`) vs Bitwise YOKI (`|`)

## Topshiriq sharti:
`||` operatorining birinchi shart `true` bo'lganda ikkinchi og'ir funksiyani chaqirmasligini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    static boolean qimmatliFunksiya() {
        System.out.println("--> Og'ir funksiya ishga tushdi!");
        return true;
    }

    public static void main(String[] args) {
        boolean keshdaBor = true;
        
        System.out.println("Tekshirish boshlandi:");
        if (keshdaBor || qimmatliFunksiya()) {
            System.out.println("Ma'lumot topildi!");
        }
    }
}
```

## Tushuntirish va Mantiq:
`||` operatorida agar chap tomon `true` bo'lsa, umumiy natija albatta `true` bo'lishi ma'lum. Shu sababli JVM o'ng tomondagi `qimmatliFunksiya()` ni mutlaqo chaqirmaydi va resurslarni tejaydi.
Agar `|` ishlatilsa, chap tomon nima bo'lishidan qat'i nazar o'ng tomon ham baribir chaqirilgan bo'lar edi.

## Ishlash natijasi:
```text
Tekshirish boshlandi:
Ma'lumot topildi!
```

---

# 59-Topshiriq: Mantiqiy EMAS (`!`) va De Morgan qonunlari

## Topshiriq sharti:
De Morgan qonunlarini (`!(A && B) == (!A || !B)`) kod misolida tekshiruvchi dastur yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        boolean A = true;
        boolean B = false;
        
        boolean qonun1Chap = !(A && B);
        boolean qonun1Ong = !A || !B;
        
        boolean qonun2Chap = !(A || B);
        boolean qonun2Ong = !A && !B;
        
        System.out.println("!(A && B) == (!A || !B): " + (qonun1Chap == qonun1Ong));
        System.out.println("!(A || B) == (!A && !B): " + (qonun2Chap == qonun2Ong));
    }
}
```

## Tushuntirish va Mantiq:
De Morgan qonunlari murakkab shartli ifodalarni soddalashtirishda qo'llaniladi:
1. `!(A && B)` ifodasi `!A || !B` ga teng.
2. `!(A || B)` ifodasi `!A && !B` ga teng.
Kodni refaktoring qilishda ushbu qoidalar yordamida chalkash `if` shartlarini o'qishga oson holatga keltirish mumkin.

## Ishlash natijasi:
```text
!(A && B) == (!A || !B): true
!(A || B) == (!A && !B): true
```

---

# 60-Topshiriq: Bitwise operatorlar: VA, YOKI, XOR amallari

## Topshiriq sharti:
Ikkilik sanoq tizimidagi sonlar ustida bit darajasidagi amallar (`&`, `|`, `^`) qanday bajarilishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int a = 0b1100; // 12
        int b = 0b1010; // 10
        
        int va = a & b;  // 0b1000 = 8
        int yoki = a | b; // 0b1110 = 14
        int xor = a ^ b;  // 0b0110 = 6
        
        System.out.println("a & b = " + va + " (binar: " + Integer.toBinaryString(va) + ")");
        System.out.println("a | b = " + yoki + " (binar: " + Integer.toBinaryString(yoki) + ")");
        System.out.println("a ^ b = " + xor + " (binar: " + Integer.toBinaryString(xor) + ")");
    }
}
```

## Tushuntirish va Mantiq:
Bit darajasidagi amallar sonlarning har bir juft bitiga alohida qo'llaniladi:
- `&` (AND): ikkala bit ham 1 bo'lsagina 1 beradi.
- `|` (OR): kamida bitta bit 1 bo'lsa 1 beradi.
- `^` (XOR): bitlar bir-biridan farq qilsa 1, bir xil bo'lsa 0 beradi.

## Ishlash natijasi:
```text
a & b = 8 (binar: 1000)
a | b = 14 (binar: 1110)
a ^ b = 6 (binar: 110)
```

---

# 61-Topshiriq: Bitwise NOT (`~`) va ikkining to'ldiruvchisi

## Topshiriq sharti:
Barcha bitlarni teskarisiga o'giruvchi `~` operatori natijasi nima sababdan `~x = -(x + 1)` bo'lishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son = 5;
        int inkor = ~son;
        
        System.out.println("5 ning inkor qilingan qiymati (~5): " + inkor);
        System.out.println("Qoida bo'yicha -(5 + 1): " + (-(son + 1)));
        
        int manfiy = -1;
        System.out.println("~(-1) = " + (~manfiy));
    }
}
```

## Tushuntirish va Mantiq:
Java-da butun sonlar ikki to'ldiruvchisi (two's complement) ko'rinishida saqlanadi.
Eng chapdagi yuqori bit ishora biti (0 - musbat, 1 - manfiy) hisoblanadi.
`~` operatori barcha 32 bitni teskarisiga aylantiradi (0 ni 1 ga, 1 ni 0 ga). Natijada har doim `~x = -(x + 1)` formulasi kelib chiqadi. Masalan, `~5 = -6`, `~(-1) = 0`.

## Ishlash natijasi:
```text
5 ning inkor qilingan qiymati (~5): -6
Qoida bo'yicha -(5 + 1): -6
~(-1) = 0
```

---

# 62-Topshiriq: Chapga bitli siljitish (`<<`) va tezkor ko'paytirish

## Topshiriq sharti:
Sonni chapga `k` ta bitga surish uni `2^k` ga ko'paytirish bilan teng kuchli ekanligini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son = 7;
        int surilgan1 = son << 1; // 7 * 2 = 14
        int surilgan3 = son << 3; // 7 * 8 = 56
        
        System.out.println("7 << 1 = " + surilgan1);
        System.out.println("7 << 3 = " + surilgan3);
    }
}
```

## Tushuntirish va Mantiq:
Chapga siljitish (`x << k`) operatori sonning barcha bitlarini chapga suradi va o'ng tarafdan yangi bo'shagan o'rinlarga nollarni to'ldiradi.
Bu arifmetik jihatdan `x * 2^k` amalini bajarishga teng.
Bitli surish protsessor darajasida ko'paytirish instruksiyasiga qaraganda ancha kam takt oladi va o'ta tez ishlaydi.

## Ishlash natijasi:
```text
7 << 1 = 14
7 << 3 = 56
```

---

# 63-Topshiriq: O'ngga ishorali siljitish (`>>`) va butun bo'lish

## Topshiriq sharti:
O'ngga siljitish (`>>`) operatori ishorani saqlagan holda 2 ning darajalariga bo'lishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int musbat = 64;
        int manfiy = -64;
        
        System.out.println("64 >> 2 (64 / 4): " + (musbat >> 2));
        System.out.println("-64 >> 2 (-64 / 4): " + (manfiy >> 2));
    }
}
```

## Tushuntirish va Mantiq:
`>>` (Signed Right Shift) barcha bitlarni o'ngga suradi.
Muhim jihati: u sonning ishorasini (sign bit) saqlab qoladi. Ya'ni musbat son bo'lsa chapdan 0 lar, manfiy son bo'lsa chapdan 1 lar bilan to'ldiriladi.
Bu arifmetik `x / 2^k` amalini ifodalaydi.

## Ishlash natijasi:
```text
64 >> 2 (64 / 4): 16
-64 >> 2 (-64 / 4): -16
```

---

# 64-Topshiriq: O'ngga ishorasiz siljitish (`>>>` Unsigned Right Shift)

## Topshiriq sharti:
Ishorasiz siljitish (`>>>`) ning manfiy sonlarda chapdan har doim nollarni kiritib, uni katta musbat songa aylantirishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son = -1;
        
        int ishorali = son >> 1;
        int ishorasiz = son >>> 1;
        
        System.out.println("-1 >> 1: " + ishorali);
        System.out.println("-1 >>> 1: " + ishorasiz);
        System.out.println("Ikkilikda ishorasiz: " + Integer.toBinaryString(ishorasiz));
    }
}
```

## Tushuntirish va Mantiq:
`>>>` (Unsigned Right Shift) Java-ga xos noyob operator bo'lib, u ishora bitiga e'tibor bermaydi. Chap tomondan har doim nollarni to'ldirib suradi.
`-1` ning barcha 32 biti 1 lardan iborat (`0xFFFFFFFF`).
Uni 1 ta o'ngga surish chapdagi eng yuqori bitni 0 ga aylantiradi va `Integer.MAX_VALUE` (2147483647) ga aylanadi.

## Ishlash natijasi:
```text
-1 >> 1: -1
-1 >>> 1: 2147483647
Ikkilikda ishorasiz: 1111111111111111111111111111111
```

---

# 65-Topshiriq: Bit maskalari (Bitmasks) yordamida ruxsatlarni boshqarish

## Topshiriq sharti:
Foydalanuvchi huquqlarini (O'qish, Yozish, O'chirish) 1 ta butun son ichida bit maskalari orqali saqlash va tekshirish tizimini quring.

## Yechim (Java kodi):
```java
public class Solution {
    public static final int OQISH = 1 << 0;     // 001 = 1
    public static final int YOZISH = 1 << 1;    // 010 = 2
    public static final int OCHIRISH = 1 << 2;  // 100 = 4

    public static void main(String[] args) {
        int ruxsatlar = OQISH | YOZISH; // 3 (O'qish va Yozish berildi)
        
        boolean oqishBormi = (ruxsatlar & OQISH) != 0;
        boolean ochirishBormi = (ruxsatlar & OCHIRISH) != 0;
        
        System.out.println("O'qish ruxsati bormi: " + oqishBormi);
        System.out.println("O'chirish ruxsati bormi: " + ochirishBormi);
        
        // O'chirish ruxsatini qo'shish
        ruxsatlar |= OCHIRISH;
        System.out.println("O'chirish qo'shilgach tekshiruv: " + ((ruxsatlar & OCHIRISH) != 0));
    }
}
```

## Tushuntirish va Mantiq:
Bit maskalari orqali bitta 32-bitli `int` o'zgaruvchisida 32 tagacha boolean bayroqlarni (flags) saqlash mumkin.
- Qo'shish: `ruxsatlar |= BAYROQ`
- Tekshirish: `(ruxsatlar & BAYROQ) != 0`
- O'chirish: `ruxsatlar &= ~BAYROQ`
Bu operatsion tizimlar, tarmoq protokollari va yuqori unumdor tizimlarda xotirani keskin tejaydi.

## Ishlash natijasi:
```text
O'qish ruxsati bormi: true
O'chirish ruxsati bormi: false
O'chirish qo'shilgach tekshiruv: true
```

---

# 66-Topshiriq: Ternary operatori asoslari

## Topshiriq sharti:
`condition ? val1 : val2` shartli operatori yordamida ikkita sondan kattasini topuvchi ixcham dastur tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int a = 25;
        int b = 40;
        
        int katta = (a > b) ? a : b;
        String xabar = (katta % 2 == 0) ? "Juft son" : "Toq son";
        
        System.out.println("Katta son: " + katta);
        System.out.println("Holati: " + xabar);
    }
}
```

## Tushuntirish va Mantiq:
Ternary operatori (uchlik operator) Java-dagi yagona 3 ta operand qabul qiluvchi operatordir.
U `if-else` ning ixcham ifoda (expression) ko'rinishi bo'lib, to'g'ridan-to'g'ri qiymat qaytaradi va o'zgaruvchiga biriktirish imkonini beradi. Qoidasi: ikkala shoxdagi qiymatlar bir-biriga mos tipda bo'lishi shart.

## Ishlash natijasi:
```text
Katta son: 40
Holati: Juft son
```

---

# 67-Topshiriq: Ichma-ich ternary operatori (Nested Ternary)

## Topshiriq sharti:
Sonning musbat, manfiy yoki nol ekanligini aniqlash uchun ichma-ich ternary ifodasini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son = -15;
        
        String tavsif = (son > 0) ? "Musbat son" 
                      : (son < 0) ? "Manfiy son" 
                      : "Nol";
                      
        System.out.println(son + " - bu: " + tavsif);
    }
}
```

## Tushuntirish va Mantiq:
Ternary operatorlarini bir-birining ichiga joylashtirish mumkin.
Garchi u kodni qisqartirsa-da, haddan tashqari ko'p pog'onali ternary kodning o'qilishini qiyinlashtiradi. Shu sababli 2 tadan ko'p shartlarda `if-else` yoki `switch` afzal hisoblanadi.

## Ishlash natijasi:
```text
-15 - bu: Manfiy son
```

---

# 68-Topshiriq: Oddiy if va if-else shartli boshqaruvi

## Topshiriq sharti:
Foydalanuvchining paroli uzunligini tekshiruvchi va xavfsizlik talablariga javob berishini baholovchi `if-else` dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String parol = "SuperParol2026";
        
        if (parol.length() >= 8) {
            System.out.println("Parol uzunligi yetarli va xavfsiz.");
        } else {
            System.out.println("Xatolik: Parol kamida 8 ta belgidan iborat bo'lishi kerak!");
        }
    }
}
```

## Tushuntirish va Mantiq:
`if-else` operatori berilgan mantiqiy shart `true` bo'lganda birinchi blokni, `false` bo'lganda esa `else` blokini bajaradi.
Har doim bloklarni jingalak qavslar `{ ... }` bilan o'rash tavsiya etiladi, hatto ichida 1 ta qator bo'lsa ham (bu keyinchalik xato qo'shilib qolishini oldini oladi).

## Ishlash natijasi:
```text
Parol uzunligi yetarli va xavfsiz.
```

---

# 69-Topshiriq: Ko'p tarmoqli if - else if - else zanjiri

## Topshiriq sharti:
Hafta kuni tartib raqamiga (1-7) qarab kun nomini aniqlovchi ko'p tarmoqli shartlar zanjirini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int kun = 5;
        String kunNomi;
        
        if (kun == 1) kunNomi = "Dushanba";
        else if (kun == 2) kunNomi = "Seshanba";
        else if (kun == 3) kunNomi = "Chorshanba";
        else if (kun == 4) kunNomi = "Payshanba";
        else if (kun == 5) kunNomi = "Juma";
        else if (kun == 6) kunNomi = "Shanba";
        else if (kun == 7) kunNomi = "Yakshanba";
        else kunNomi = "Noto'g'ri kun";
        
        System.out.println("Tanlangan kun: " + kunNomi);
    }
}
```

## Tushuntirish va Mantiq:
`if - else if - else` ketma-ketligi yuqoridan pastga qarab tekshirib kelinadi.
Birinchi `true` bergan shart bloki bajariladi va butun zanjirdan chiqiladi. Hech qaysi shart bajarilmasa, yakuniy `else` bloki ishga tushadi.

## Ishlash natijasi:
```text
Tanlangan kun: Juma
```

---

# 70-Topshiriq: Guard Clauses (Qo'riqlovchi shartlar) bilan chuqur if larni bartaraf qilish

## Topshiriq sharti:
Ichma-ich ketgan 4 qavatli `if` ni Guard Clauses yondashuvi orqali toza va tekis kodga aylantiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void royxatdanOtish(String ism, int yosh, boolean emailTasdiqlangan) {
        if (ism == null || ism.isBlank()) {
            System.out.println("Rad etildi: Ism kiritilmagan");
            return;
        }
        if (yosh < 18) {
            System.out.println("Rad etildi: Yosh 18 dan kichik");
            return;
        }
        if (!emailTasdiqlangan) {
            System.out.println("Rad etildi: Email tasdiqlanmagan");
            return;
        }
        
        System.out.println("Muvaffaqiyatli ro'yxatdan o'tdingiz, " + ism + "!");
    }

    public static void main(String[] args) {
        royxatdanOtish("Akmal", 22, true);
        royxatdanOtish("Lola", 16, true);
    }
}
```

## Tushuntirish va Mantiq:
Guard Clauses (Early Return) - bu xato va rad etish shartlarini metodning boshida tekshirib, darhol `return` qilib chiqib ketish texnikasidir.
Bu usul kodni "Arrow Anti-pattern" (o'ng tomonga qarab chuqurlashib ketadigan piramida) ga aylanishidan saqlaydi va kodning o'qilishini ancha soddalashtiradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli ro'yxatdan o'tdingiz, Akmal!
Rad etildi: Yosh 18 dan kichik
```

---

# 71-Topshiriq: Klassik switch operatori va break kalit so'zi

## Topshiriq sharti:
Fasllar raqamiga qarab fasl nomini chop etuvchi klassik `switch-case` dasturini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int faslKodi = 2;
        String faslNomi;
        
        switch (faslKodi) {
            case 1:
                faslNomi = "Bahor";
                break;
            case 2:
                faslNomi = "Yoz";
                break;
            case 3:
                faslNomi = "Kuz";
                break;
            case 4:
                faslNomi = "Qish";
                break;
            default:
                faslNomi = "Noma'lum fasl";
                break;
        }
        
        System.out.println("Tanlangan fasl: " + faslNomi);
    }
}
```

## Tushuntirish va Mantiq:
Klassik `switch` ifodasi berilgan o'zgaruvchini case qiymatlari bilan solishtiradi.
Mos kelgan holatdan so'ng `break` operatori qo'yilmasa, dastur keyingi barcha case larni shartini tekshirmasdan bajarib yuboradi (Fall-through).
`default` bloki esa birorta ham case mos kelmaganda ishlaydi.

## Ishlash natijasi:
```text
Tanlangan fasl: Yoz
```

---

# 72-Topshiriq: Switch fall-through hodisasi va undan ongli foydalanish

## Topshiriq sharti:
`break` ning tushirib qoldirilishi orqali bir nechta oylarni bitta faslga birlashtirish namunasini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int oy = 4; // Aprel
        String fasl;
        
        switch (oy) {
            case 12:
            case 1:
            case 2:
                fasl = "Qish";
                break;
            case 3:
            case 4:
            case 5:
                fasl = "Bahor";
                break;
            case 6:
            case 7:
            case 8:
                fasl = "Yoz";
                break;
            case 9:
            case 10:
            case 11:
                fasl = "Kuz";
                break;
            default:
                fasl = "Noto'g'ri oy raqami";
        }
        
        System.out.println(oy + "-oy fasli: " + fasl);
    }
}
```

## Tushuntirish va Mantiq:
Fall-through - bu `break` bo'lmagani sababli pastdagi case larning avtomatik bajarilishidir.
Bu xususiyatdan bir nechta turli qiymatlar uchun ayni bir xil mantiqni bajarish kerak bo'lganda (masalan, 3, 4, 5 oylar uchun "Bahor") ongli ravishda guruhlashda foydalaniladi.

## Ishlash natijasi:
```text
4-oy fasli: Bahor
```

---

# 73-Topshiriq: Switch operatorida String bilan ishlash

## Topshiriq sharti:
Java 7 da joriy qilingan `String` parametrli `switch` operatori yordamida buyruqlarni qayta ishlang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String buyruq = "START";
        
        switch (buyruq.toUpperCase()) {
            case "START":
                System.out.println("Tizim ishga tushirildi");
                break;
            case "STOP":
                System.out.println("Tizim to'xtatildi");
                break;
            case "PAUSE":
                System.out.println("Tizim vaqtincha to'xtatildi");
                break;
            default:
                System.out.println("Noma'lum buyruq");
        }
    }
}
```

## Tushuntirish va Mantiq:
Java 7 dan boshlab `String` tiplari switch ichida qo'llab-quvvatlanadi.
JVM darajasida kompilyator buni satrning `hashCode()` qiymatini tekshirish va to'qnashuvlarni (hash collision) oldini olish uchun `equals()` orqali solishtirishga aylantiradi.
Muhim: agar uzatilgan satr `null` bo'lsa, switch darhol `NullPointerException` tashlaydi.

## Ishlash natijasi:
```text
Tizim ishga tushirildi
```

---

# 74-Topshiriq: Switch operatorida Enum bilan ishlash

## Topshiriq sharti:
Buyurtma holatini ko'rsatuvchi `enum` bilan xavfsiz `switch` tuzilmasini yarating.

## Yechim (Java kodi):
```java
public class Solution {
    enum Holat { KUTILMOQDA, TOLANDI, YETKAZILDI }

    public static void main(String[] args) {
        Holat holat = Holat.TOLANDI;
        
        switch (holat) {
            case KUTILMOQDA:
                System.out.println("To'lov qilinishini kuting");
                break;
            case TOLANDI:
                System.out.println("To'lov qabul qilindi, buyurtma yig'ilmoqda");
                break;
            case YETKAZILDI:
                System.out.println("Buyurtma manzilga yetkazildi");
                break;
        }
    }
}
```

## Tushuntirish va Mantiq:
`enum` bilan ishlaganda `case` yonida enum sinfining nomini yozish talab etilmaydi (ya'ni `case Holat.TOLANDI:` emas, shunchaki `case TOLANDI:` yoziladi).
Kompilyator barcha holatlar qamrab olinganligini tekshira oladi va yozuv xatolaridan to'liq himoya qiladi.

## Ishlash natijasi:
```text
To'lov qabul qilindi, buyurtma yig'ilmoqda
```

---

# 75-Topshiriq: Zamonaviy Switch Expressions (Java 14+ Arrow sintaksisi)

## Topshiriq sharti:
Java 14 da standart bo'lgan `->` strelkali switch sintaksisi yordamida `break` siz xavfsiz qiymat qaytarishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int kunRaqami = 3;
        
        String kunTuri = switch (kunRaqami) {
            case 1, 2, 3, 4, 5 -> "Ish kuni";
            case 6, 7 -> "Dam olish kuni";
            default -> "Noto'g'ri kun";
        };
        
        System.out.println("3-kun: " + kunTuri);
    }
}
```

## Tushuntirish va Mantiq:
Zamonaviy Switch Expression larning afzalliklari:
1. `->` (arrow) sintaksisida `break` yozish shart emas va fall-through xatolari butunlay yo'q qilingan.
2. Switch endi ifoda (expression) bo'lib, o'zidan to'g'ridan-to'g'ri qiymat qaytaradi va o'zgaruvchiga yoziladi.
3. Vergul bilan bir nechta qiymatni bitta satrda guruhlash mumkin (`case 1, 2, 3...`).
4. Oxirida nuqta-vergul `;` qo'yiladi, chunki bu tayinlash ifodasidir.

## Ishlash natijasi:
```text
3-kun: Ish kuni
```

---

# 76-Topshiriq: Switch Expression va yield kalit so'zi

## Topshiriq sharti:
Murakkab hisob-kitob talab qilinadigan case blogi ichidan `yield` orqali qiymat qaytarish dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String valyuta = "USD";
        double miqdor = 100.0;
        
        double somdagiQiymat = switch (valyuta) {
            case "USD" -> {
                double kurs = 12800.0;
                yield miqdor * kurs;
            }
            case "EUR" -> {
                double kurs = 13900.0;
                yield miqdor * kurs;
            }
            default -> {
                System.out.println("Noma'lum valyuta!");
                yield 0.0;
            }
        };
        
        System.out.println(miqdor + " " + valyuta + " = " + somdagiQiymat + " so'm");
    }
}
```

## Tushuntirish va Mantiq:
Agar switch ning biror shoxida ko'p qatorli kod yoki blok `{ ... }` mavjud bo'lsa, undan natijaviy qiymatni qaytarish uchun `yield` kalit so'zi ishlatiladi.
`yield` faqat switch expression lar ichida qiymat qaytarish uchun xizmat qiladi (metoddan chiqib ketuvchi `return` dan farq qiladi).

## Ishlash natijasi:
```text
100.0 USD = 1280000.0 so'm
```

---

# 77-Topshiriq: Pattern Matching for switch: Tiplar bo'yicha saralash (Java 17/21)

## Topshiriq sharti:
`Object` tipidagi obyektning qaysi sinfga tegishli ekanligini switch orqali tekshirish va to'g'ridan-to'g'ri o'zgaruvchiga bog'lashni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static String obektniTahlilQil(Object obj) {
        return switch (obj) {
            case Integer i -> "Butun son: " + i + ", uning kvadrati: " + (i * i);
            case String s -> "Satr: " + s + ", belgilar soni: " + s.length();
            case Double d -> "Haqiqiy son: " + d;
            case null -> "Obyekt null ga teng!";
            default -> "Noma'lum tip: " + obj.getClass().getSimpleName();
        };
    }

    public static void main(String[] args) {
        System.out.println(obektniTahlilQil(10));
        System.out.println(obektniTahlilQil("Salom Java 21"));
        System.out.println(obektniTahlilQil(null));
    }
}
```

## Tushuntirish va Mantiq:
Java 21 da rasmiylashgan Pattern Matching for switch imkoniyati orqali ob'ekt turi tekshiriladi va darhol lokal o'zgaruvchiga o'tkaziladi (`case Integer i`).
Bunda hech qanday qo'shimcha `(Integer) obj` kabi xunuk kasting yozish shart emas.
Shuningdek, `case null` orqali alohida null holatini xavfsiz ushlash mumkin.

## Ishlash natijasi:
```text
Butun son: 10, uning kvadrati: 100
Satr: Salom Java 21, belgilar soni: 13
Obyekt null ga teng!
```

---

# 78-Topshiriq: Switch Pattern Matching da when kalit so'zi (Guarded patterns)

## Topshiriq sharti:
Tipni tekshirish bilan bir vaqtda qo'shimcha mantiqiy shart qo'yuvchi `when` sintaksisini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static String tekshir(Object obj) {
        return switch (obj) {
            case String s when s.length() > 5 -> "Uzun satr: " + s;
            case String s -> "Qisqa satr: " + s;
            case Integer i when i > 0 -> "Musbat son: " + i;
            case Integer i when i < 0 -> "Manfiy son: " + i;
            case Integer i -> "Nol";
            default -> "Boshqa qiymat";
        };
    }

    public static void main(String[] args) {
        System.out.println(tekshir("Toshkent"));
        System.out.println(tekshir("Salom"));
        System.out.println(tekshir(42));
        System.out.println(tekshir(-7));
    }
}
```

## Tushuntirish va Mantiq:
Guarded patterns (`when` kalit so'zi):
Faqat tip to'g'ri kelishi yetarli bo'lmagan hollarda, `case Tip o'zgaruvchi when shart` ko'rinishida qo'shimcha filtr qo'yish mumkin.
Shart `true` bo'lsagina shu shox bajariladi, aks holda keyingi case larga o'tadi.

## Ishlash natijasi:
```text
Uzun satr: Toshkent
Qisqa satr: Salom
Musbat son: 42
Manfiy son: -7
```

---

# 79-Topshiriq: Klassik break bilan siklni muddatidan oldin to'xtatish

## Topshiriq sharti:
Massiv ichidan qidirilayotgan son topilgach, `break` orqali siklni darhol to'xtatuvchi dastur yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[] sonlar = {10, 45, 89, 32, 99, 14};
        int qidirilayotgan = 32;
        int topilganIndeks = -1;
        
        for (int i = 0; i < sonlar.length; i++) {
            if (sonlar[i] == qidirilayotgan) {
                topilganIndeks = i;
                break; // Keraksiz qolgan iteratsiyalarni to'xtatamiz
            }
        }
        
        System.out.println(qidirilayotgan + " soni indeksi: " + topilganIndeks);
    }
}
```

## Tushuntirish va Mantiq:
`break` operatori bajarilayotgan joriy siklni (`for`, `while`, `do-while`) zudlik bilan to'xtatadi va boshqaruvni sikldan keyingi qatorga uzatadi.
Bu qidiruv algoritmlarida unumdorlikni oshirish uchun kerak.

## Ishlash natijasi:
```text
32 soni indeksi: 3
```

---

# 80-Topshiriq: Klassik continue bilan joriy iteratsiyani o'tkazib yuborish

## Topshiriq sharti:
1 dan 10 gacha bo'lgan sonlar ichidan toq sonlarni `continue` yordamida tashlab ketib, faqat juft sonlarni chop eting.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        System.out.print("Juft sonlar: ");
        for (int i = 1; i <= 10; i++) {
            if (i % 2 != 0) {
                continue; // Toq son bo'lsa keyingi qadamga o'tamiz
            }
            System.out.print(i + " ");
        }
        System.out.println();
    }
}
```

## Tushuntirish va Mantiq:
`continue` operatori sikl tanasidagi qolgan amallarni bajarmay, darhol siklning keyingi iteratsiyasiga (qadamiga) o'tkazadi.
Sikl butunlay to'xtamaydi, faqat o'sha qadam o'tkazib yuboriladi.

## Ishlash natijasi:
```text
Juft sonlar: 2 4 6 8 10
```

---

# 81-Topshiriq: Yorliqli (Labeled) break bilan tashqi sikldan chiqish

## Topshiriq sharti:
2D matritsa ichida qidiruv bajarilayotganda ichki sikldan turib barcha tashqi sikllarni ham to'xtatuvchi `labeled break` dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int[][] matritsa = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        int target = 5;
        boolean topildi = false;
        
        qidiruvSikli:
        for (int qator = 0; qator < matritsa.length; qator++) {
            for (int ustun = 0; ustun < matritsa[qator].length; ustun++) {
                if (matritsa[qator][ustun] == target) {
                    System.out.println("Topildi! Qator: " + qator + ", Ustun: " + ustun);
                    topildi = true;
                    break qidiruvSikli; // Tashqi qidiruvSikli ni to'xtatadi
                }
            }
        }
        
        System.out.println("Qidiruv yakunlandi, holat: " + topildi);
    }
}
```

## Tushuntirish va Mantiq:
Oddiy `break` faqat o'zi joylashgan eng ichki sikldan chiqaradi.
Agar bir nechta ichma-ich sikllardan to'liq chiqib ketish kerak bo'lsa, tashqi sikl oldiga yorliq (masalan `qidiruvSikli:`) qo'yiladi va `break qidiruvSikli;` buyrug'i beriladi.

## Ishlash natijasi:
```text
Topildi! Qator: 1, Ustun: 1
Qidiruv yakunlandi, holat: true
```

---

# 82-Topshiriq: Yorliqli (Labeled) continue bilan tashqi sikl iteratsiyasini davom ettirish

## Topshiriq sharti:
Ichki sikldan turib tashqi siklning keyingi qadamiga o'tish dasturini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        tashqi:
        for (int i = 1; i <= 3; i++) {
            for (int j = 1; j <= 3; j++) {
                if (j == 2) {
                    continue tashqi; // Tashqi siklning keyingi qadamiga o'tish
                }
                System.out.println("i=" + i + ", j=" + j);
            }
        }
    }
}
```

## Tushuntirish va Mantiq:
`continue label;` buyrug'i yorliq bilan ko'rsatilgan tashqi siklning yangi iteratsiyasiga o'tadi.
Ichki sikl qolgan qadamlarini to'xtatadi va tashqi siklning hisoblagichi oshiriladi.

## Ishlash natijasi:
```text
i=1, j=1
i=2, j=1
i=3, j=1
```

---

# 83-Topshiriq: Bitli amallar bilan sonning juft yoki toqligini aniqlash

## Topshiriq sharti:
`% 2` amalisiz, faqat bitli `n & 1` yordamida sonning juft yoki toqligini o'ta tezkor tekshiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son1 = 48;
        int son2 = 77;
        
        System.out.println(son1 + " juftmi: " + ((son1 & 1) == 0));
        System.out.println(son2 + " juftmi: " + ((son2 & 1) == 0));
    }
}
```

## Tushuntirish va Mantiq:
Ikkilik sanoq sistemasida toq sonlarning eng oxirgi biti (0-bit) har doim 1 bo'ladi, juft sonlarda esa har doim 0 bo'ladi.
`son & 1` amali sonning faqat eng oxirgi bitini tekshiradi:
- Agar natija 0 bo'lsa - son juft.
- Agar natija 1 bo'lsa - son toq.
Bu amaliyot apparat darajasida bo'lish (`%`) amalidan ko'ra bir necha baravar tezroq bajariladi.

## Ishlash natijasi:
```text
48 juftmi: true
77 juftmi: false
```

---

# 84-Topshiriq: Ikkining darajasi ekanligini bitli tekshirish

## Topshiriq sharti:
Musbat butun sonning ikkining darajasi (1, 2, 4, 8, 16...) ekanligini `(n & (n - 1)) == 0` formulasi bilan tekshiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static boolean ikkiningDarajasimi(int n) {
        return n > 0 && (n & (n - 1)) == 0;
    }

    public static void main(String[] args) {
        System.out.println("16 ikkining darajasimi: " + ikkiningDarajasimi(16));
        System.out.println("18 ikkining darajasimi: " + ikkiningDarajasimi(18));
        System.out.println("1024 ikkining darajasimi: " + ikkiningDarajasimi(1024));
    }
}
```

## Tushuntirish va Mantiq:
Ikkining darajasi bo'lgan har qanday sonning ikkilik ko'rinishida faqat bitta dona `1` biti bo'ladi (masalan, 16 = `10000`).
Undan 1 ayrilganda o'sha 1 biti 0 bo'lib, o'ngdagi barcha bitlar 1 ga aylanadi (15 = `01111`).
Ularni `&` (AND) qilganda aynan 0 hosil bo'ladi: `10000 & 01111 == 0`.
Bu algoritm O(1) vaqtda ishlaydigan eng go'zal bit hiylalaridan biridir.

## Ishlash natijasi:
```text
16 ikkining darajasimi: true
18 ikkining darajasimi: false
1024 ikkining darajasimi: true
```

---

# 85-Topshiriq: XOR Swap: Uchinchi o'zgaruvchisiz qiymatlarni almashtirish

## Topshiriq sharti:
Ikkita o'zgaruvchi qiymatini qo'shimcha xotira (temp) ishlatmasdan faqat XOR (`^`) amali bilan o'zaro almashtiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int a = 15;
        int b = 27;
        
        System.out.println("Almashishdan oldin: a=" + a + ", b=" + b);
        
        a = a ^ b;
        b = a ^ b;
        a = a ^ b;
        
        System.out.println("Almashgandan keyin: a=" + a + ", b=" + b);
    }
}
```

## Tushuntirish va Mantiq:
XOR ning asosiy xossasi: `x ^ x = 0` va `x ^ 0 = x`.
1-qadam: `a = a ^ b` (a ikkala sonning yig'indi xor ni saqlaydi)
2-qadam: `b = a ^ b = (a ^ b) ^ b = a` (b ga eski a o'tdi)
3-qadam: `a = a ^ b = (a ^ b) ^ a = b` (a ga eski b o'tdi).
Qo'shimcha temp o'zgaruvchisiz ikkala qiymat xotirada joy almashdi.

## Ishlash natijasi:
```text
Almashishdan oldin: a=15, b=27
Almashgandan keyin: a=27, b=15
```

---

# 86-Topshiriq: Operator Precedence (Operatorlar ustuvorligi)

## Topshiriq sharti:
Ko'paytirish, qo'shish, taqqoslash va mantiqiy amallarning bajarilish ketma-ketligini tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int natija1 = 10 + 5 * 2; // Ko'paytirish ustun: 10 + 10 = 20
        int natija2 = (10 + 5) * 2; // Qavs ustun: 15 * 2 = 30
        
        boolean mantiq = 5 + 3 > 7 && 10 - 2 == 8;
        // 8 > 7 (true) && 8 == 8 (true) -> true
        
        System.out.println("natija1: " + natija1);
        System.out.println("natija2: " + natija2);
        System.out.println("mantiqiy natija: " + mantiq);
    }
}
```

## Tushuntirish va Mantiq:
Java-da operatorlarning bajarilish tartibi quyidagicha:
1. Qavslar `()`
2. Postfiks `x++`, `x--`
3. Prefiks `++x`, `--x`, bir o'rinli `+`, `-`, `!`, `~`
4. Multiplikativ `*`, `/`, `%`
5. Additiv `+`, `-`
6. Siljitish `<<`, `>>`, `>>>`
7. Taqqoslash `<`, `>`, `<=`, `>=`, `instanceof`
8. Tenglik `==`, `!=`
9. Bitwise `&`, `^`, `|`
10. Mantiqiy `&&`, `||`
11. Ternary `?:`
12. Tayinlash `=`, `+=` va boshqalar.

## Ishlash natijasi:
```text
natija1: 20
natija2: 30
mantiqiy natija: true
```

---

# 87-Topshiriq: Early Return bilan murakkab shartlarni tozalash

## Topshiriq sharti:
Chegirma hisoblash funksiyasini bir nechta qavatli `else` lardasiz, erta qaytish (`return`) orqali ixcham yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static double chegirmaHisobla(double summa, boolean vipMijoz) {
        if (summa <= 0) return 0.0;
        if (vipMijoz) return summa * 0.20; // VIP mijozga 20%
        if (summa >= 1000000) return summa * 0.15; // 1 mln dan oshsa 15%
        if (summa >= 500000) return summa * 0.10; // 500 mingdan oshsa 10%
        
        return 0.0; // Chegirma yo'q
    }

    public static void main(String[] args) {
        System.out.println("VIP chegirmasi: " + chegirmaHisobla(300000, true));
        System.out.println("Katta xarid chegirmasi: " + chegirmaHisobla(1200000, false));
        System.out.println("Oddiy chegirma: " + chegirmaHisobla(200000, false));
    }
}
```

## Tushuntirish va Mantiq:
Erta qaytish usuli funksiya kodini chiziqli va ravon qiladi. Har bir maxsus holat o'z vaqtida tekshirilib natija qaytariladi, ortiqcha `else` bloklari umuman talab qilinmaydi.

## Ishlash natijasi:
```text
VIP chegirmasi: 60000.0
Katta xarid chegirmasi: 180000.0
Oddiy chegirma: 0.0
```

---

# 88-Topshiriq: Klassik instanceof va java 16+ pattern matching farqi

## Topshiriq sharti:
Eski uslubdagi `instanceof` + kasting bilan zamonaviy Smart Cast (`instanceof String s`) farqini solishtiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void eskiTekshiruv(Object obj) {
        if (obj instanceof String) {
            String s = (String) obj; // Majburiy kasting
            System.out.println("Eski usul: " + s.toUpperCase());
        }
    }

    public static void yangiTekshiruv(Object obj) {
        // Java 16+ Pattern Matching
        if (obj instanceof String s) {
            System.out.println("Yangi usul: " + s.toUpperCase());
        }
    }

    public static void main(String[] args) {
        Object nom = "Java Ekotizimi";
        eskiTekshiruv(nom);
        yangiTekshiruv(nom);
    }
}
```

## Tushuntirish va Mantiq:
Eski Java-da `instanceof` bilan tekshirgandan so'ng yana bir marta `(String) obj` deb kasting qilish talab qilinar edi (ortiqcha boilerplate kod).
Java 16 dan boshlab `obj instanceof String s` deb yozilsa, shart qanoatlantirilgan taqdirda darhol `s` o'zgaruvchisi ochiladi va avtomatik kasting qilinadi.

## Ishlash natijasi:
```text
Eski usul: JAVA EKOTIZIMI
Yangi usul: JAVA EKOTIZIMI
```

---

# 89-Topshiriq: Integer.signum() bilan sonning ishorasini aniqlash

## Topshiriq sharti:
Sonning musbat (+1), manfiy (-1) yoki nol (0) ekanligini if-elselarsiz `Integer.signum()` orqali aniqlang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int a = 150;
        int b = -85;
        int c = 0;
        
        System.out.println("signum(150): " + Integer.signum(a));
        System.out.println("signum(-85): " + Integer.signum(b));
        System.out.println("signum(0): " + Integer.signum(c));
    }
}
```

## Tushuntirish va Mantiq:
`Integer.signum(int i)` matematik signum funksiyasini ifodalaydi:
- Agar son > 0 bo'lsa: `1`
- Agar son < 0 bo'lsa: `-1`
- Agar son == 0 bo'lsa: `0`
Bu funksiya saralash komparatorlarida (`Comparable.compareTo`) natija qaytarishda juda qulay hisoblanadi.

## Ishlash natijasi:
```text
signum(150): 1
signum(-85): -1
signum(0): 0
```

---

# 90-Topshiriq: Oraliqqa tushishini tekshirish (Range Checking)

## Topshiriq sharti:
Foydalanuvchi yoshi berilgan oraliqqa (masalan, 18 dan 65 gacha) to'g'ri kelishini tekshiruvchi metod tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static boolean oraliqdami(int qiymat, int min, int max) {
        return qiymat >= min && qiymat <= max;
    }

    public static void main(String[] args) {
        int yosh = 28;
        boolean mehnatgaLayoqatli = oraliqdami(yosh, 18, 65);
        System.out.println(yosh + " yosh mehnat oralig'idami: " + mehnatgaLayoqatli);
    }
}
```

## Tushuntirish va Mantiq:
Matematikadagi `min <= x <= max` qo'shaloq tengsizligi Java-da ikkita alohida mantiqiy shart va `&&` operatori orqali ifodalanadi (`x >= min && x <= max`).

## Ishlash natijasi:
```text
28 yosh mehnat oralig'idami: true
```

---

# 91-Topshiriq: Tenglik taqqoslash: == vs Objects.equals()

## Topshiriq sharti:
`null` xavfisiz ikkita ob'ektning tengligini tekshirishda `Objects.equals()` utilitasining ahamiyatini ko'rsating.

## Yechim (Java kodi):
```java
import java.util.Objects;

public class Solution {
    public static void main(String[] args) {
        String a = null;
        String b = "Salom";
        
        // a.equals(b); // NullPointerException!
        
        boolean tengmi = Objects.equals(a, b);
        System.out.println("Xavfsiz tenglik: " + tengmi);
        
        String c = "Salom";
        System.out.println("Ikki bir xil satr: " + Objects.equals(b, c));
    }
}
```

## Tushuntirish va Mantiq:
`Objects.equals(a, b)` metodi `(a == b) || (a != null && a.equals(b))` shartini bajaradi.
Agar `a` null bo'lsa, hech qanday `NullPointerException` otilmaydi, balki xavfsiz `false` qaytadi. Ikkala parametr ham `null` bo'lsa `true` qaytaradi.

## Ishlash natijasi:
```text
Xavfsiz tenglik: false
Ikki bir xil satr: true
```

---

# 92-Topshiriq: Sealed interfeys bilan Switch Pattern Matching (Java 21)

## Topshiriq sharti:
Java 17/21 dagi `sealed` interfeys va uning barcha turlarini qamrab oluvchi to'liq switch dasturini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    sealed interface Shakl permits Aylana, Tortburchak {}
    record Aylana(double radius) implements Shakl {}
    record Tortburchak(double boyi, double eni) implements Shakl {}

    public static double yuzaHisobla(Shakl shakl) {
        return switch (shakl) {
            case Aylana a -> Math.PI * a.radius() * a.radius();
            case Tortburchak t -> t.boyi() * t.eni();
            // default talab qilinmaydi, chunki sealed interface barcha variantlarni cheklab qo'ygan!
        };
    }

    public static void main(String[] args) {
        Shakl a = new Aylana(10);
        Shakl t = new Tortburchak(5, 8);
        
        System.out.printf("Aylana yuzi: %.2f
", yuzaHisobla(a));
        System.out.printf("To'rtburchak yuzi: %.2f
", yuzaHisobla(t));
    }
}
```

## Tushuntirish va Mantiq:
`sealed` (muhrlangan) interfeyslar faqat `permits` qilingan sub-sinflarga meros olishga ruxsat beradi.
Kompilyator barcha mumkin bo'lgan shakllarni aniq bilgani uchun, `switch` da `default` shoxini yozish talab qilinmaydi (exhaustiveness check). Agar kelajakda yangi sub-sinf qo'shilsa, switch darhol kompilyatsiya xatosi beradi.

## Ishlash natijasi:
```text
Aylana yuzi: 314.16
To'rtburchak yuzi: 40.00
```

---

# 93-Topshiriq: Switch operatorida null qiymatni qabul qilish

## Topshiriq sharti:
Java 21 da switch ichida `case null` qanday ishlashini va `NullPointerException` dan qutqarishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void bahola(String matn) {
        switch (matn) {
            case null -> System.out.println("Matn yo'q (null)");
            case "JAVA" -> System.out.println("Java tanlandi");
            default -> System.out.println("Boshqa: " + matn);
        }
    }

    public static void main(String[] args) {
        bahola(null);
        bahola("JAVA");
        bahola("PYTHON");
    }
}
```

## Tushuntirish va Mantiq:
Klassik Java switch operatorlariga `null` uzatilsa, hali biron case tekshirilmasdan darhol `NullPointerException` ro'y berar edi.
Java 21 dan boshlab switch da alohida `case null` shoxi qo'llab-quvvatlanadi.

## Ishlash natijasi:
```text
Matn yo'q (null)
Java tanlandi
Boshqa: PYTHON
```

---

# 94-Topshiriq: Sonning bitlar sonini hisoblash: Integer.bitCount()

## Topshiriq sharti:
Berilgan sonning ikkilik tasviridagi '1' bitlari sonini `Integer.bitCount()` orqali toping.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son = 29; // 0b11101 -> to'rtta 1 biti bor
        int birlarSoni = Integer.bitCount(son);
        
        System.out.println(son + " ning ikkilik ko'rinishi: " + Integer.toBinaryString(son));
        System.out.println("1 bitlar soni: " + birlarSoni);
    }
}
```

## Tushuntirish va Mantiq:
`Integer.bitCount()` (Popcount algoritmi) sonning ikkilik tasvirida nechta 1 biti borligini hisoblab beradi.
Zamonaviy protsessorlarda bu bitta apparat instruksiyasi (`POPCNT`) orqali bajariladi va kriptografiya hamda qidiruv indekslarida o'ta tez ishlaydi.

## Ishlash natijasi:
```text
29 ning ikkilik ko'rinishi: 11101
1 bitlar soni: 4
```

---

# 95-Topshiriq: Sonni ma'lum oraliqqa chegaralash (Clamping)

## Topshiriq sharti:
Matematik `clamp` amalini (qiymatni `[min, max]` oralig'ida ushlab qolish) `Math.clamp()` (Java 21) yoki shartli operatorlar bilan yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static int chegarala(int qiymat, int min, int max) {
        return Math.max(min, Math.min(max, qiymat));
    }

    public static void main(String[] args) {
        System.out.println("150 [0, 100] oralig'ida: " + chegarala(150, 0, 100));
        System.out.println("-20 [0, 100] oralig'ida: " + chegarala(-20, 0, 100));
        System.out.println("45 [0, 100] oralig'ida: " + chegarala(45, 0, 100));
    }
}
```

## Tushuntirish va Mantiq:
Clamping - bu berilgan qiymatni belgilangan min va max chegaralaridan oshib ketmasligini ta'minlashdir.
Agar qiymat min dan kichik bo'lsa min, max dan katta bo'lsa max, oraliqda bo'lsa o'zi olinadi. (Java 21 da `Math.clamp()` standarti ham mavjud).

## Ishlash natijasi:
```text
150 [0, 100] oralig'ida: 100
-20 [0, 100] oralig'ida: 0
45 [0, 100] oralig'ida: 45
```

---

# 96-Topshiriq: Ko'p tarmoqli valyuta konvertori

## Topshiriq sharti:
Switch expression orqali turli valyutalarni (USD, EUR, RUB) so'mga (UZS) o'giruvchi konvertor dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static double konvertatsiya(double summa, String valyuta) {
        return switch (valyuta.toUpperCase()) {
            case "USD" -> summa * 12800.0;
            case "EUR" -> summa * 13900.0;
            case "RUB" -> summa * 140.0;
            case "UZS" -> summa;
            default -> throw new IllegalArgumentException("Noma'lum valyuta: " + valyuta);
        };
    }

    public static void main(String[] args) {
        System.out.println("50 USD = " + konvertatsiya(50, "USD") + " UZS");
        System.out.println("100 EUR = " + konvertatsiya(100, "EUR") + " UZS");
    }
}
```

## Tushuntirish va Mantiq:
Switch expression orqali valyutalarning joriy kursi hisoblanadi.
Agar ro'yxatda mavjud bo'lmagan valyuta kelsa, `throw` operatori orqali `IllegalArgumentException` xatosi tashlanadi.

## Ishlash natijasi:
```text
50 USD = 640000.0 UZS
100 EUR = 1390000.0 UZS
```

---

# 97-Topshiriq: Talabalar baholash tizimi (GPA Calculator)

## Topshiriq sharti:
Talabaning 0 dan 100 gacha bo'lgan ballini an'anaviy harfli bahoga (A, B, C, D, F) o'tkazuvchi shartli algoritmni yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static String bahoniAniqlash(int ball) {
        if (ball < 0 || ball > 100) return "Noto'g'ri ball";
        
        int onlik = ball / 10;
        return switch (onlik) {
            case 10, 9 -> "A (A'lo)";
            case 8 -> "B (Yaxshi)";
            case 7 -> "C (Qoniqarli)";
            case 6 -> "D (Yetarli)";
            default -> "F (Qoniqarsiz)";
        };
    }

    public static void main(String[] args) {
        System.out.println("95 ball: " + bahoniAniqlash(95));
        System.out.println("82 ball: " + bahoniAniqlash(82));
        System.out.println("58 ball: " + bahoniAniqlash(58));
    }
}
```

## Tushuntirish va Mantiq:
Ballni 10 ga butun bo'lish (`ball / 10`) orqali 0 dan 10 gacha bo'lgan toifaga o'tkaziladi.
So'ngra zamonaviy switch yordamida guruhlangan holatlar tekshiriladi (10 va 9 -> "A"). Bu uzun `if-else` lar yozishdan ancha qulayroqdir.

## Ishlash natijasi:
```text
95 ball: A (A'lo)
82 ball: B (Yaxshi)
58 ball: F (Qoniqarsiz)
```

---

# 98-Topshiriq: Progressiv daromad solig'i hisoblash algoritmi

## Topshiriq sharti:
Daromad miqdoriga qarab bosqichma-bosqich oshib boruvchi progressiv soliq hisoblash dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static double soliqHisobla(double daromad) {
        double soliq = 0;
        
        if (daromad <= 5000000) {
            soliq = daromad * 0.05; // 5 mln gacha 5%
        } else if (daromad <= 15000000) {
            soliq = (5000000 * 0.05) + ((daromad - 5000000) * 0.12); // 12%
        } else {
            soliq = (5000000 * 0.05) + (10000000 * 0.12) + ((daromad - 15000000) * 0.20); // 20%
        }
        
        return soliq;
    }

    public static void main(String[] args) {
        System.out.printf("4 mln daromad solig'i: %.2f so'm
", soliqHisobla(4000000));
        System.out.printf("10 mln daromad solig'i: %.2f so'm
", soliqHisobla(10000000));
        System.out.printf("20 mln daromad solig'i: %.2f so'm
", soliqHisobla(20000000));
    }
}
```

## Tushuntirish va Mantiq:
Progressiv soliq tizimida butun summa birdaniga yuqori foizga solinmaydi, balki har bir qatlam (bracket) o'z foiz stavkasi bo'yicha ayri-ayri hisoblanadi.

## Ishlash natijasi:
```text
4 mln daromad solig'i: 200000.00 so'm
10 mln daromad solig'i: 850000.00 so'm
20 mln daromad solig'i: 2450000.00 so'm
```

---

# 99-Topshiriq: Bank PIN-kodini tekshirish va urinishlar sonini nazorat qilish

## Topshiriq sharti:
Foydalanuvchiga 3 marta imkoniyat beruvchi va noto'g'ri kiritilganda kartani bloklovchi shartli boshqaruv tizimini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        final String ASL_PIN = "7788";
        String[] kiritilganUrinishlar = {"1111", "0000", "7788"};
        
        boolean bloklandi = false;
        boolean kirdi = false;
        
        for (int urinish = 0; urinish < kiritilganUrinishlar.length; urinish++) {
            String pin = kiritilganUrinishlar[urinish];
            if (pin.equals(ASL_PIN)) {
                System.out.println("PIN to'g'ri! Tizimga xush kelibsiz (urinish: " + (urinish + 1) + ")");
                kirdi = true;
                break;
            } else {
                System.out.println("Noto'g'ri PIN: " + pin + ". Qolgan urinishlar: " + (2 - urinish));
            }
        }
        
        if (!kirdi) {
            bloklandi = true;
            System.out.println("XAVFSIZLIK: Karta bloklandi!");
        }
    }
}
```

## Tushuntirish va Mantiq:
Ushbu xavfsizlik logikasida for sikli va `equals()` orqali har bir urinish tekshiriladi.
To'g'ri PIN topilganda `break` bilan chiqiladi. Agar 3 ta urinish ham xato bo'lsa, `kirdi` bayrog'i `false` qoladi va karta bloklanadi.

## Ishlash natijasi:
```text
Noto'g'ri PIN: 1111. Qolgan urinishlar: 2
Noto'g'ri PIN: 0000. Qolgan urinishlar: 1
PIN to'g'ri! Tizimga xush kelibsiz (urinish: 3)
```

---

# 100-Topshiriq: Xulosa topshiriq: Bankomat (ATM) boshqaruv oqimi to'liq simulyatsiyasi

## Topshiriq sharti:
Operatorlar, switch, if-else, yorliqlar va hisob-kitoblarni birlashtirib Bankomat (ATM) foydalanuvchi menyusi va balans boshqaruv tizimini yarating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        double balans = 500000.0;
        int[] amallar = {1, 2, 2, 3, 4}; // 1: Balans, 2: Yechish, 3: Kiritish, 4: Chiqish
        double[] summalar = {0, 200000.0, 400000.0, 150000.0, 0};
        
        System.out.println("=== BANKOMAT TIZIMI ISHGA TUSHDI ===");
        
        boshqaruv:
        for (int i = 0; i < amallar.length; i++) {
            int buyruq = amallar[i];
            double mablag = summalar[i];
            
            switch (buyruq) {
                case 1 -> System.out.printf("Joriy balans: %.2f so'm
", balans);
                case 2 -> {
                    if (mablag > balans) {
                        System.out.printf("Xatolik: Balansda yetarli mablag' yo'q! So'raldi: %.2f so'm, Balans: %.2f so'm
", mablag, balans);
                    } else {
                        balans -= mablag;
                        System.out.printf("Muvaffaqiyatli yechildi: %.2f so'm. Yangi balans: %.2f so'm
", mablag, balans);
                    }
                }
                case 3 -> {
                    balans += mablag;
                    System.out.printf("Hisob to'ldirildi: %.2f so'm. Yangi balans: %.2f so'm
", mablag, balans);
                }
                case 4 -> {
                    System.out.println("Xizmatdan foydalanganingiz uchun rahmat. Kartangizni oling!");
                    break boshqaruv;
                }
                default -> System.out.println("Noto'g'ri buyruq tanlandi.");
            }
        }
        System.out.println("=== SEANS YAKUNLANDI ===");
    }
}
```

## Tushuntirish va Mantiq:
Ushbu keng qamrovli topshiriqda:
1. `switch` ifodasi orqali foydalanuvchi buyruqlari qabul qilinadi.
2. `if-else` sharti orqali balansda pul yetarliligi tekshiriladi.
3. Mablag' yechish va to'ldirish amallarida arifmetik operatorlar (`+=`, `-=`) xavfsiz qo'llaniladi.
4. `break boshqaruv;` yorlig'i orqali sessiya o'z vaqtida to'xtatiladi.

## Ishlash natijasi:
```text
=== BANKOMAT TIZIMI ISHGA TUSHDI ===
Joriy balans: 500000.00 so'm
Muvaffaqiyatli yechildi: 200000.00 so'm. Yangi balans: 300000.00 so'm
Xatolik: Balansda yetarli mablag' yo'q! So'raldi: 400000.00 so'm, Balans: 300000.00 so'm
Hisob to'ldirildi: 150000.00 so'm. Yangi balans: 450000.00 so'm
Xizmatdan foydalanganingiz uchun rahmat. Kartangizni oling!
=== SEANS YAKUNLANDI ===
```
