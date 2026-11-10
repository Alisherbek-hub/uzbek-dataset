# Java Asoslari: Tiplar va O'zgaruvchilar (1-50)

# 1-Topshiriq: Byte tipi diapazoni va to'lishi (Overflow)

## Topshiriq sharti:
Java-da `byte` primitiv tipining eng kichik va eng katta qiymatlarini konsolga chiqaring. Eng katta qiymatga 1 qo'shilganda ro'y beradigan overflow (to'lib toshish) holatini namoyish eting.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        byte min = Byte.MIN_VALUE;
        byte max = Byte.MAX_VALUE;
        System.out.println("Minimal byte: " + min);
        System.out.println("Maksimal byte: " + max);
        
        byte overflow = (byte) (max + 1);
        System.out.println("Maksimal byte + 1 (overflow): " + overflow);
    }
}
```

## Tushuntirish va Mantiq:
Java-da `byte` tipi 8-bitli ishorali (signed) butun son bo'lib, uning qiymatlar diapazoni -128 dan 127 gacha (-2^7 dan 2^7 - 1 gacha) bo'ladi.
Ikki komplementli (two's complement) arifmetika tufayli, eng katta musbat son bo'lmish 127 (ikkilik sanoq sistemasida `01111111`) ustiga 1 qo'shilganda `10000000` hosil bo'ladi. Bu esa eng kichik manfiy son -128 ni ifodalaydi.
E'tibor bering, `max + 1` amali bajarilganda Java avtomatik ravishda operatsiyani `int` tipiga o'tkazadi (type promotion), shu sababli natijani yana `byte` ga yozish uchun aniq kasting `(byte)` talab etiladi.

## Ishlash natijasi:
```text
Minimal byte: -128
Maksimal byte: 127
Maksimal byte + 1 (overflow): -128
```

---

# 2-Topshiriq: Short va Int tiplarining xotira hajmi va taqqoslanishi

## Topshiriq sharti:
`short` va `int` tiplarining xotiradagi hajmini (bayt va bitlarda) hamda ularning minimal va maksimal qiymatlarini aniqlab beruvchi dastur tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        System.out.println("short hajmi: " + Short.BYTES + " bayt (" + Short.SIZE + " bit)");
        System.out.println("short diapazoni: " + Short.MIN_VALUE + " dan " + Short.MAX_VALUE + " gacha");
        
        System.out.println("int hajmi: " + Integer.BYTES + " bayt (" + Integer.SIZE + " bit)");
        System.out.println("int diapazoni: " + Integer.MIN_VALUE + " dan " + Integer.MAX_VALUE + " gacha");
    }
}
```

## Tushuntirish va Mantiq:
`short` tipi 16 bit (2 bayt) hajmga ega va -32,768 dan 32,767 gacha bo'lgan qiymatlarni qamrab oladi.
`int` tipi esa 32 bit (4 bayt) hajmga ega bo'lib, -2,147,483,648 dan 2,147,483,647 gacha bo'lgan diapazonga ega.
Java-da standart butun sonli hisob-kitoblar protsessor registrlari unumdorligini oshirish maqsadida 32-bitli `int` tipida bajariladi. Wrapper sinflardagi `BYTES` va `SIZE` konstantalari xotira parametrlarini dasturiy aniqlashda qo'llaniladi.

## Ishlash natijasi:
```text
short hajmi: 2 bayt (16 bit)
short diapazoni: -32768 dan 32767 gacha
int hajmi: 4 bayt (32 bit)
int diapazoni: -2147483648 dan 2147483647 gacha
```

---

# 3-Topshiriq: Long tipi va 'L' harfining ahamiyati

## Topshiriq sharti:
Juda katta sonli hisob-kitoblarda `long` tipini to'g'ri e'lon qilish va 'L' suffiksi qo'yilmaganda yuzaga keladigan xatolikni bartaraf etish dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        long aholi = 8000000000L;
        long millisekundlar = 24L * 60 * 60 * 1000 * 1000;
        
        System.out.println("Yer yuzi taxminiy aholisi: " + aholi);
        System.out.println("Bir kundagi mikrosekundlar: " + millisekundlar);
    }
}
```

## Tushuntirish va Mantiq:
Java-da butun sonli literallar sukut bo'yicha (by default) `int` deb qabul qilinadi. Agar son `int` diapazonidan (2 milliarddan) katta bo'lsa va oxiriga `L` yoki `l` qo'yilmasa, kompilyatsiya xatosi (integer number too large) yuz beradi.
Katta hisob-kitoblarda, masalan, ko'paytirish amallarida agar ko'paytuvchilardan kamida bittasi `long` qilib belgilanmasa (masalan, `24L`), hisob-kitob `int` da bajarilib to'lib toshadi (overflow) va noto'g'ri manfiy natija chiqadi.

## Ishlash natijasi:
```text
Yer yuzi taxminiy aholisi: 8000000000
Bir kundagi mikrosekundlar: 86400000000
```

---

# 4-Topshiriq: Float va Double: IEEE 754 suzuvchi nuqta aniqligi

## Topshiriq sharti:
0.1 va 0.2 sonlarini qo'shganda suzuvchi nuqtali sonlar (IEEE 754) sababli yuzaga keladigan noaniqlikni va `float` bilan `double` farqini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        double a = 0.1;
        double b = 0.2;
        double yigindi = a + b;
        
        System.out.println("0.1 + 0.2 = " + yigindi);
        System.out.println("Tenglik (0.1 + 0.2 == 0.3): " + (yigindi == 0.3));
        
        float fa = 0.1f;
        float fb = 0.2f;
        System.out.println("Float yig'indi: " + (fa + fb));
    }
}
```

## Tushuntirish va Mantiq:
Java-da `float` (32 bit, 7 ta raqam aniqlik) va `double` (64 bit, 15-17 ta raqam aniqlik) IEEE 754 xalqaro standartiga asoslanadi.
O'nlik kasrlar (masalan, 0.1) ikkilik sanoq tizimida cheksiz davriy kasrga aylanadi. Shuning uchun kompyuter xotirasida ular yaxlitlanadi. 0.1 + 0.2 amali `0.30000000000000004` natijasini beradi.
Shu sababli moliyaviy va aniq hisob-kitoblarda hech qachon `float` yoki `double` dan foydalanilmaydi; buning o'rniga `BigDecimal` qo'llaniladi.

## Ishlash natijasi:
```text
0.1 + 0.2 = 0.30000000000000004
Tenglik (0.1 + 0.2 == 0.3): false
Float yig'indi: 0.3
```

---

# 5-Topshiriq: Char tipi va Unicode arifmetikasi

## Topshiriq sharti:
Java-da `char` tipi orqali harflar, Unicode kodlari va ular ustidagi arifmetik amallarni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        char belgi = 'A';
        int kod = belgi;
        char keyingiBelgi = (char) (belgi + 1);
        char uzbekHarf = 'Ў'; // Ў
        
        System.out.println("Belgi: " + belgi + ", uning kodi: " + kod);
        System.out.println("Keyingi belgi (A + 1): " + keyingiBelgi);
        System.out.println("Unicode orqali olingan harf: " + uzbekHarf);
    }
}
```

## Tushuntirish va Mantiq:
Java-da `char` 16-bitli ishorasiz (unsigned) butun sonli tip bo'lib, UTF-16 kodlash birligini ifodalaydi (0 dan 65,535 gacha).
Char tipi to'g'ridan-to'g'ri sonli qiymatga ega bo'lganligi sababli, u arifmetik amallarda qatnasha oladi. `belgi + 1` amali bajarilganda natija `int` ga ko'tariladi, so'ng `(char)` kasting orqali keyingi belgiga (masalan, 'B') o'tkaziladi.

## Ishlash natijasi:
```text
Belgi: A, uning kodi: 65
Keyingi belgi (A + 1): B
Unicode orqali olingan harf: Ў
```

---

# 6-Topshiriq: Boolean tipi va mantiqiy amallar

## Topshiriq sharti:
`boolean` o'zgaruvchilari orqali asosiy mantiqiy amallarni (AND, OR, NOT, XOR) bajaruvchi dastur tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        boolean rost = true;
        boolean yolgon = false;
        
        System.out.println("rost AND yolg'on: " + (rost && yolgon));
        System.out.println("rost OR yolg'on: " + (rost || yolgon));
        System.out.println("NOT rost: " + (!rost));
        System.out.println("rost XOR yolg'on: " + (rost ^ yolgon));
        System.out.println("rost XOR rost: " + (rost ^ rost));
    }
}
```

## Tushuntirish va Mantiq:
`boolean` tipi faqat ikkita qiymatni qabul qiladi: `true` yoki `false`.
JVM spesifikatsiyasida alohida bitta bit uchun instruksiya bo'lmagani sababli, xotirada ko'pincha 1 bayt (yoki massivlarda ixcham) o'lcham egallaydi.
XOR (`^`) amali operandlarning faqat bittasi `true` bo'lgandagina `true` qaytaradi, ikkalasi bir xil bo'lsa `false` beradi.

## Ishlash natijasi:
```text
rost AND yolg'on: false
rost OR yolg'on: true
NOT rost: false
rost XOR yolg'on: true
rost XOR rost: false
```

---

# 7-Topshiriq: Local Variable Type Inference (var kalit so'zi)

## Topshiriq sharti:
Java 10 da kiritilgan `var` kalit so'zi yordamida turli xil tiplarni kompilyator tomonidan avtomatik aniqlanishini (type inference) namoyish eting.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        var matn = "Salom, O'zbekiston!";
        var son = 42;
        var haqiqiySon = 3.14159;
        var holat = true;
        
        System.out.println("matn turi: " + matn.getClass().getSimpleName() + " -> " + matn);
        System.out.println("son: " + son);
        System.out.println("haqiqiy son: " + haqiqiySon);
        System.out.println("holat: " + holat);
    }
}
```

## Tushuntirish va Mantiq:
`var` kalit so'zi JavaScript-dagi dinamik tiplash emas, balki kompilyatsiya bosqichida statik tiplashdir. Kompilyator o'ng tomondagi qiymatga qarab o'zgaruvchining aniq tipini o'zi belgilaydi.
Kod baytkodga o'tganda `var` o'rniga aniq tip yoziladi, shuning uchun dastur tezligiga zarracha ta'sir qilmaydi. `var` faqat boshlang'ich qiymat berilgan lokal o'zgaruvchilar uchun ruxsat etiladi.

## Ishlash natijasi:
```text
matn turi: String -> Salom, O'zbekiston!
son: 42
haqiqiy son: 3.14159
holat: true
```

---

# 8-Topshiriq: Var kalit so'zining cheklovlari va qoidalari

## Topshiriq sharti:
`var` kalit so'zidan foydalanishda initsializatsiyasiz e'lon qilish va null qiymat berish mumkin emasligini tushuntiruvchi misol yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        var ism = "Alisher";
        // var yosh; // XATO: initsializatsiya shart!
        // var obekt = null; // XATO: null qaysi tip ekanligi noma'lum!
        
        String boshqa = null; // To'g'ri
        var aniqMatn = (String) null; // Kasting bilan mumkin, ammo tavsiya etilmaydi
        
        System.out.println("Ism: " + ism);
        System.out.println("Boshqa: " + boshqa);
        System.out.println("Aniq matn: " + aniqMatn);
    }
}
```

## Tushuntirish va Mantiq:
`var` kalit so'zining asosiy cheklovlari:
1. U sinf maydonlarida (field) yoki metod parametrlari hamda metodning qaytish tipida ishlatilmaydi.
2. Initsializatsiyasiz e'lon qilib bo'lmaydi (`var x;` xato).
3. To'g'ridan-to'g'ri `null` berib bo'lmaydi, chunki kompilyator `null` qaysi klass ekanini bila olmaydi.
4. Massiv initsializatorlarida `{1, 2}` ko'rinishida to'g'ridan-to'g'ri ishlatib bo'lmaydi, `new int[]{1, 2}` ko'rinishida aniq belgilash zarur.

## Ishlash natijasi:
```text
Ism: Alisher
Boshqa: null
Aniq matn: null
```

---

# 9-Topshiriq: Final o'zgaruvchilar: O'zgarmas qiymatlar

## Topshiriq sharti:
`final` kalit so'zi yordamida o'zgarmas primitiv o'zgaruvchilar yaratish va ularning qayta o'zgartirilmasligini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        final double PI = 3.141592653589793;
        final int MAX_FOYDALANUVCHILAR = 1000;
        
        System.out.println("PI o'zgarmasi: " + PI);
        System.out.println("Maksimal foydalanuvchilar: " + MAX_FOYDALANUVCHILAR);
        
        // PI = 3.14; // Kompilyatsiya xatosi: cannot assign a value to final variable PI
    }
}
```

## Tushuntirish va Mantiq:
`final` kalit so'zi o'zgaruvchiga bir marta qiymat biriktirilgandan so'ng, uni boshqa o'zgartirib bo'lmasligini kafolatlaydi.
Konstantalar odatda `UPPER_SNAKE_CASE` formatida yoziladi. Primitiv tiplar uchun `final` uning qiymati stack xotirada qat'iy o'zgarmas bo'lib qolishini anglatadi.

## Ishlash natijasi:
```text
PI o'zgarmasi: 3.141592653589793
Maksimal foydalanuvchilar: 1000
```

---

# 10-Topshiriq: Final Reference tipi va ob'ekt holatining o'zgarishi

## Topshiriq sharti:
`final` reference o'zgaruvchining ko'rsatkichi o'zgarmasligi, ammo Heap xotiradagi ob'ektning ichki holati o'zgarishi mumkinligini isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    static class Talaba {
        String ism;
        Talaba(String ism) { this.ism = ism; }
    }

    public static void main(String[] args) {
        final Talaba talaba = new Talaba("Javohir");
        System.out.println("Dastlabki ism: " + talaba.ism);
        
        // Ob'ekt ichki holati o'zgaradi
        talaba.ism = "Sardor";
        System.out.println("O'zgartirilgan ism: " + talaba.ism);
        
        // talaba = new Talaba("Bobur"); // XATO: final ko'rsatkichni yangi manzilga yo'naltirib bo'lmaydi
    }
}
```

## Tushuntirish va Mantiq:
`final` kalit so'zi reference o'zgaruvchiga qo'llanganda, u faqat xotira ko'rsatkichini (manzilini) o'zgarmas qiladi. Ya'ni o'zgaruvchi boshqa yangi obyektga ishora qila olmaydi.
Biroq bu Heap xotiradagi ob'ektning ichki maydonlari o'zgarmas (immutable) bo'lib qoladi degani emas. Obyektning o'zi butunlay o'zgarmas bo'lishi uchun uning maydonlari ham `final` qilinishi va tashqaridan modifikatsiya yopilishi kerak.

## Ishlash natijasi:
```text
Dastlabki ism: Javohir
O'zgartirilgan ism: Sardor
```

---

# 11-Topshiriq: Widening Type Casting (Avtomatik kengaytiruvchi o'tkazish)

## Topshiriq sharti:
Kichik o'lchamli primitiv tipdan kattaroq o'lchamli tipga ma'lumot yo'qotishsiz avtomatik o'tishni (Widening casting) namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        byte baytQiymat = 42;
        short shortQiymat = baytQiymat;
        int intQiymat = shortQiymat;
        long longQiymat = intQiymat;
        float floatQiymat = longQiymat;
        double doubleQiymat = floatQiymat;
        
        System.out.println("byte: " + baytQiymat);
        System.out.println("int: " + intQiymat);
        System.out.println("long: " + longQiymat);
        System.out.println("double: " + doubleQiymat);
    }
}
```

## Tushuntirish va Mantiq:
Widening (kengaytiruvchi) kasting xavfsiz hisoblanadi, chunki kichikroq sig'imdagi qiymat kattaroq sig'imga bemalol sig'adi (`byte -> short -> int -> long -> float -> double`).
Bunda hech qanday qo'shimcha sintaktik kasting kodi talab qilinmaydi va Java kompilyatori buni avtomatik amalga oshiradi.

## Ishlash natijasi:
```text
byte: 42
int: 42
long: 42
double: 42.0
```

---

# 12-Topshiriq: Narrowing Type Casting (Qat'iy toraytiruvchi o'tkazish)

## Topshiriq sharti:
Katta o'lchamli tipdan kichik o'lchamli tipga ma'lumot o'tkazishda ma'lumot yo'qotilishi (bit truncation) holatini tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        double d = 130.85;
        int i = (int) d;
        byte b = (byte) i;
        
        System.out.println("Double qiymat: " + d);
        System.out.println("Int ga o'tkazilganda (kasr qismi yo'qoladi): " + i);
        System.out.println("Byte ga o'tkazilganda (to'lib toshish): " + b);
    }
}
```

## Tushuntirish va Mantiq:
Narrowing (toraytiruvchi) kastingda dasturchi `(int)` yoki `(byte)` kabi qat'iy kasting operatorini yozishi shart.
Double dan int ga o'tganda kasr qismi kesib tashlanadi (truncation).
Int dan byte ga o'tganda esa faqat oxirgi 8 bit saqlanadi. 130 sonining ikkilik ko'rinishi 8 bitlik doirada manfiy son (-126) bo'lib talqin qilinadi.

## Ishlash natijasi:
```text
Double qiymat: 130.85
Int ga o'tkazilganda (kasr qismi yo'qoladi): 130
Byte ga o'tkazilganda (to'lib toshish): -126
```

---

# 13-Topshiriq: Butun sonlar to'lib toshishi va Math.addExact

## Topshiriq sharti:
Oddiy qo'shishdagi overflow bilan `Math.addExact()` xavfsiz arifmetik metodi o'rtasidagi farqni ko'rsatuvchi dastur tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int max = Integer.MAX_VALUE;
        int oddiyNatija = max + 1;
        System.out.println("Oddiy qo'shish (noto'g'ri manfiy): " + oddiyNatija);
        
        try {
            int xavfsizNatija = Math.addExact(max, 1);
            System.out.println("Natija: " + xavfsizNatija);
        } catch (ArithmeticException e) {
            System.out.println("Xavfsiz usul xatolikni ushladi: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
Java-da odatiy arifmetika to'lib-toshish (overflow) sodir bo'lganda jimgina aylanib (wrap-around) teskari manfiy songa o'tib ketadi va hech qanday istisno (exception) tashlamaydi. Bu moliyaviy tizimlarda juda xavfli.
Java 8 da kiritilgan `Math.addExact()`, `Math.multiplyExact()`, `Math.subtractExact()` metodlari esa bunday holatda `ArithmeticException` tashlab, xatoning oldini oladi.

## Ishlash natijasi:
```text
Oddiy qo'shish (noto'g'ri manfiy): -2147483648
Xavfsiz usul xatolikni ushladi: integer overflow
```

---

# 14-Topshiriq: Underflow hodisasi va uning oqibatlari

## Topshiriq sharti:
Suzuvchi nuqtali sonlarda eng kichik musbat sondan kichiklashib ketish (Underflow) va nolga aylanish jarayonini namoyish eting.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        float engKichikMusbat = Float.MIN_VALUE;
        System.out.println("Eng kichik musbat float: " + engKichikMusbat);
        
        float nolgaTeng = engKichikMusbat / 2;
        System.out.println("Yarimga bo'linganda underflow: " + nolgaTeng);
    }
}
```

## Tushuntirish va Mantiq:
Underflow - bu hisoblanayotgan son apparat darajasida ifodalanishi mumkin bo'lgan eng kichik musbat noldan farqli qiymatdan ham kichiklashib ketganda sodir bo'ladi.
Bunday paytda qiymat mashina noli (`0.0`) ga aylanadi. Bu hodisa hisob-kitoblar aniqligining yo'qolishiga sabab bo'ladi.

## Ishlash natijasi:
```text
Eng kichik musbat float: 1.4E-45
Yarimga bo'linganda underflow: 0.0
```

---

# 15-Topshiriq: Wrapper sinflar va ularning statik utilit metodlari

## Topshiriq sharti:
`Integer`, `Double` va `Boolean` wrapper sinflarining ma'lumotlarni tahlil qilish (parse) va konvertatsiya qilish imkoniyatlarini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int son = Integer.parseInt("12345");
        double haqiqiy = Double.parseDouble("99.95");
        boolean holat = Boolean.parseBoolean("true");
        
        String binarSatr = Integer.toBinaryString(42);
        String hexSatr = Integer.toHexString(255);
        
        System.out.println("O'qilgan son: " + son);
        System.out.println("O'qilgan double: " + haqiqiy);
        System.out.println("O'qilgan mantiqiy: " + holat);
        System.out.println("42 ning ikkilik ko'rinishi: " + binarSatr);
        System.out.println("255 ning 16 lik ko'rinishi: " + hexSatr);
    }
}
```

## Tushuntirish va Mantiq:
Wrapper sinflar primitiv tiplarni obyekt ko'rinishida o'rab berishdan tashqari, boy statik funksiyalar to'plamini taqdim etadi.
`parseInt()`, `parseDouble()` satrlarni mos songa aylantiradi. `toBinaryString()`, `toHexString()` esa sonlarni turli sanoq tizimlariga o'tkazishda qo'l keladi.

## Ishlash natijasi:
```text
O'qilgan son: 12345
O'qilgan double: 99.95
O'qilgan mantiqiy: true
42 ning ikkilik ko'rinishi: 101010
255 ning 16 lik ko'rinishi: ff
```

---

# 16-Topshiriq: Autoboxing mexanizmi

## Topshiriq sharti:
Java-da primitiv `int` ning avtomatik tarzda `Integer` wrapper obyektiga o'ralishi (Autoboxing) va baytkoddagi `valueOf()` chaqiruvini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int oddiySon = 100;
        Integer obektSon = oddiySon; // Autoboxing: Integer.valueOf(oddiySon)
        
        System.out.println("Primitiv qiymat: " + oddiySon);
        System.out.println("O'ralgan obyekt qiymati: " + obektSon);
        System.out.println("Obyekt klassi: " + obektSon.getClass().getName());
    }
}
```

## Tushuntirish va Mantiq:
Autoboxing - bu primitiv tipning unga mos keluvchi Wrapper obyektiga avtomatik ravishda aylantirilishidir (Java 5 da kiritilgan).
Kompilyator orqa fonda `Integer obektSon = Integer.valueOf(oddiySon);` chaqiruvini generatsiya qiladi. Bu kolleksiyalar (masalan, `List<Integer>`) bilan ishlashda qulaylik yaratadi.

## Ishlash natijasi:
```text
Primitiv qiymat: 100
O'ralgan obyekt qiymati: 100
Obyekt klassi: java.lang.Integer
```

---

# 17-Topshiriq: Unboxing mexanizmi va NullPointerException xavfi

## Topshiriq sharti:
Wrapper obyektidan primitiv qiymatni ajratib olish (Unboxing) va `null` wrapper unboxing qilinganda yuzaga keladigan `NullPointerException` ni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        Integer raqam = Integer.valueOf(50);
        int primitivRaqam = raqam; // Unboxing: raqam.intValue()
        System.out.println("Unboxed natija: " + primitivRaqam);
        
        Integer nullWrapper = null;
        try {
            int xato = nullWrapper; // NullPointerException!
            System.out.println(xato);
        } catch (NullPointerException e) {
            System.out.println("Diqqat! Null wrapper unboxing qilinganda xatolik: " + e.getClass().getSimpleName());
        }
    }
}
```

## Tushuntirish va Mantiq:
Unboxing - Wrapper obyektdan primitiv qiymatni avtomatik ajratib olishdir. Kompilyator buni `raqam.intValue()` orqali bajaradi.
Agar wrapper o'zgaruvchi `null` bo'lsa, `null.intValue()` chaqiriladi va JVM darhol `NullPointerException` istisnosini tashlaydi. Shuning uchun shartli operatorlarda va hisob-kitoblarda null tekshiruvini unutmaslik zarur.

## Ishlash natijasi:
```text
Unboxed natija: 50
Diqqat! Null wrapper unboxing qilinganda xatolik: NullPointerException
```

---

# 18-Topshiriq: Integer Cache mexanizmi va == taqqoslashi

## Topshiriq sharti:
-128 dan 127 gacha bo'lgan oraliqda `Integer` keshlanishi va `==` operatori orqali tekshirilganda kutilmagan `true` natija berishini isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        Integer a = 127;
        Integer b = 127;
        System.out.println("127 == 127 (keshlangan): " + (a == b));
        
        Integer c = 128;
        Integer d = 128;
        System.out.println("128 == 128 (keshlanmagan): " + (c == d));
        System.out.println("128 equals 128: " + c.equals(d));
    }
}
```

## Tushuntirish va Mantiq:
JVM xotirani tejash va unumdorlikni oshirish uchun -128 dan 127 gacha bo'lgan `Integer` obyektlarini `IntegerCache` da keshlaydi.
`Integer.valueOf(127)` chaqirilganda keshdagi bir xil obyekt havolasi qaytadi, shu bois `a == b` true bo'ladi.
128 soni esa oraliqdan tashqarida bo'lgani uchun yangi obyekt yaratiladi va `c == d` ikkita har xil heap manzilini taqqoslab `false` beradi. Har doim obyektlarni `equals()` bilan taqqoslash shart!

## Ishlash natijasi:
```text
127 == 127 (keshlangan): true
128 == 128 (keshlanmagan): false
128 equals 128: true
```

---

# 19-Topshiriq: Boolean va Byte keshlarining xatti-harakati

## Topshiriq sharti:
`Boolean.valueOf()` va `Byte.valueOf()` keshlarini tekshiruvchi dastur tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        Boolean b1 = Boolean.valueOf(true);
        Boolean b2 = Boolean.valueOf(true);
        System.out.println("Boolean kesh b1 == b2: " + (b1 == b2));
        
        Byte byte1 = Byte.valueOf((byte) 50);
        Byte byte2 = Byte.valueOf((byte) 50);
        System.out.println("Byte kesh byte1 == byte2: " + (byte1 == byte2));
    }
}
```

## Tushuntirish va Mantiq:
Java-da `Boolean` sinfida faqat ikkita statik doimiy instansiya mavjud: `Boolean.TRUE` va `Boolean.FALSE`. Ular har doim bir xil manzilga ega.
`Byte` sinfida esa barcha mumkin bo'lgan 256 ta qiymat (-128 dan 127 gacha) to'liq keshlanadi. Shu sababli `Byte.valueOf()` har doim keshdan obyekt beradi.

## Ishlash natijasi:
```text
Boolean kesh b1 == b2: true
Byte kesh byte1 == byte2: true
```

---

# 20-Topshiriq: Sonli literallar: O'nlik, O'n oltilik, Sakkizlik va Ikkilik

## Topshiriq sharti:
Java-da 4 xil sanoq tizimidagi literallarni (decimal, hex `0x`, octal `0`, binary `0b`) e'lon qiling va ularning o'nlikdagi qiymatini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        int onlik = 100;
        int onOltilik = 0x64; // 100 o'nlikda
        int sakkizlik = 0144; // 100 o'nlikda
        int ikkilik = 0b01100100; // 100 o'nlikda
        
        System.out.println("O'nlik: " + onlik);
        System.out.println("O'n oltilik (0x64): " + onOltilik);
        System.out.println("Sakkizlik (0144): " + sakkizlik);
        System.out.println("Ikkilik (0b01100100): " + ikkilik);
    }
}
```

## Tushuntirish va Mantiq:
Java sonli literallarni qulay kiritish uchun bir nechta prefikslarni qo'llab-quvvatlaydi:
- `0x` yoki `0X` - 16 lik sanoq tizimi (0-9, A-F)
- `0` - 8 lik sanoq tizimi (0-7). Ehtiyot bo'ling: oddiy son oldiga `0` qo'yilsa, u 8 lik deb tushuniladi!
- `0b` yoki `0B` - 2 lik sanoq tizimi (0 va 1).

## Ishlash natijasi:
```text
O'nlik: 100
O'n oltilik (0x64): 100
Sakkizlik (0144): 100
Ikkilik (0b01100100): 100
```

---

# 21-Topshiriq: Sonli literallarda pastki chiziq (Underscore) ajratgichi

## Topshiriq sharti:
Katta sonlarni o'qishni osonlashtirish uchun Java 7 da kiritilgan pastki chiziq (`_`) belgisidan foydalanishni namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        long kartaRaqam = 8600_1234_5678_9012L;
        double kattaMablag = 1_000_000.50;
        int hexBaytlar = 0xFF_EC_DE_5E;
        
        System.out.println("Karta raqami: " + kartaRaqam);
        System.out.println("Katta mablag': " + kattaMablag);
        System.out.println("Hex qiymat: " + hexBaytlar);
    }
}
```

## Tushuntirish va Mantiq:
Java 7 dan boshlab raqamlar orasida `_` belgisini qo'yish mumkin. Bu faqat kodning inson tomonidan o'qilishini yaxshilash (readability) uchundir.
Kompilyator baytkodga o'tkazishda barcha pastki chiziqlarni olib tashlaydi. Qoidasi: chiziq faqat raqamlar orasida bo'lishi kerak (boshida, oxirida yoki nuqta yonida bo'lishi mumkin emas).

## Ishlash natijasi:
```text
Karta raqami: 8600123456789012
Katta mablag': 1000000.5
Hex qiymat: -1253794
```

---

# 22-Topshiriq: Escape ketma-ketliklari va maxsus belgilar

## Topshiriq sharti:
Matnlarda maxsus escape ketma-ketliklaridan (`\n`, `\t`, `\"`, `\\`) foydalanish dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String xabar = "Bo'limlar:
	1. Kirish
	2. "Java Asoslari"
	3. Fayl yo'li: C:\\app\\data";
        System.out.println(xabar);
    }
}
```

## Tushuntirish va Mantiq:
Java-da ba'zi belgilar satr ichida maxsus ma'noga ega bo'lgani sababli, ularning oldiga teskari slesh (`\`) qo'yish talab etiladi:
- `\n` - yangi qatorga o'tish (newline)
- `\t` - tabulyatsiya (tab)
- `\"` - qo'shtirnoq belgisi
- `\\` - bitta teskari slesh

## Ishlash natijasi:
```text
Bo'limlar:
	1. Kirish
	2. "Java Asoslari"
	3. Fayl yo'li: C:\app\data
```

---

# 23-Topshiriq: String Pool va intern() metodi

## Topshiriq sharti:
String Pool (Satrlar havzasi) qanday ishlashini va `new String()` bilan literal orasidagi farqni hamda `intern()` metodini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String s1 = "Toshkent";
        String s2 = "Toshkent";
        String s3 = new String("Toshkent");
        String s4 = s3.intern();
        
        System.out.println("s1 == s2 (String Pool): " + (s1 == s2));
        System.out.println("s1 == s3 (Heap vs Pool): " + (s1 == s3));
        System.out.println("s1 == s4 (intern orqali Pool ga): " + (s1 == s4));
    }
}
```

## Tushuntirish va Mantiq:
Java-da `""` orqali e'lon qilingan barcha satr literallari Heap xotira ichidagi maxsus String Pool (satrlar havzasi) ga joylashadi. Agar xuddi shu satr yana uchrasa, yangi obyekt yaratilmasdan o'sha havzadagi manzil qaytariladi (`s1 == s2`).
`new String(...)` esa String Pooldan tashqarida alohida yangi obyekt yaratadi.
`intern()` metodi esa mavjud obyektning String Pooldagi kanonik vakilini qaytaradi.

## Ishlash natijasi:
```text
s1 == s2 (String Pool): true
s1 == s3 (Heap vs Pool): false
s1 == s4 (intern orqali Pool ga): true
```

---

# 24-Topshiriq: String o'zgarmasligi (Immutability)

## Topshiriq sharti:
String obyektining o'zgarmasligi (immutable) va uning ustida bajarilgan har bir amal yangi obyekt yaratishini isbotlang.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String shahar = "Samarqand";
        String ozgartirilgan = shahar.concat(" - qadimiy shahar");
        
        System.out.println("Dastlabki satr o'zgarmadi: " + shahar);
        System.out.println("Natijaviy yangi satr: " + ozgartirilgan);
    }
}
```

## Tushuntirish va Mantiq:
Java-da `String` klassi `final` qilingan va uning ichidagi belgilar massivi (`byte[] value`) o'zgarmasdir.
`concat()`, `replace()`, `toUpperCase()` kabi har qanday metod eski satrni o'zgartirmaydi, balki Heap xotirada mutlaqo yangi `String` obyektini hosil qilib qaytaradi.
Bu xavfsizlik (security), multithreading va String Pool ishlashi uchun poydevor hisoblanadi.

## Ishlash natijasi:
```text
Dastlabki satr o'zgarmadi: Samarqand
Natijaviy yangi satr: Samarqand - qadimiy shahar
```

---

# 25-Topshiriq: String vs StringBuilder unumdorligi

## Topshiriq sharti:
Siklda ko'p marta satrlarni ulashda `String` ning sekinligi va `StringBuilder` ning samaradorligini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= 5; i++) {
            sb.append("Son: ").append(i).append("; ");
        }
        String natija = sb.toString();
        System.out.println("Yig'ilgan satr: " + natija);
    }
}
```

## Tushuntirish va Mantiq:
Siklda `str += i` usulida satr ulash har bir iteratsiyada yangi `String` obyekti yaratadi va xotirani tez to'ldiradi (O(N^2) murakkablik).
`StringBuilder` esa o'zgaruvchan (mutable) ichki buferga ega bo'lib, xotirani qayta ajratmasdan satrlarni juda tez ulaydi (O(N) unumdorlik). Multithread muhitida esa `StringBuffer` qo'llaniladi.

## Ishlash natijasi:
```text
Yig'ilgan satr: Son: 1; Son: 2; Son: 3; Son: 4; Son: 5;
```

---

# 26-Topshiriq: Java 15+ Text Blocks (Matn bloklari)

## Topshiriq sharti:
Java 15 da standartlashtirilgan ko'p qatorli matn bloklari (`"""`) bilan JSON ma'lumotlarini chiroyli formatlash dasturini yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String json = """
                {
                    "ism": "Dilshod",
                    "rol": "Dasturchi",
                    "tajribaYillari": 5
                }
                """;
        System.out.println("Formatlangan JSON:");
        System.out.println(json.stripIndent());
    }
}
```

## Tushuntirish va Mantiq:
Java 15 gacha bo'lgan davrda ko'p qatorli matn yozish uchun har bir qatorga `\n` va `+` qo'yish kerak bo'lgan.
Text Blocks (`""" ... """`) matnni HTML, SQL, JSON kabi formatlarda aynan qanday bo'lsa shunday yozish imkonini beradi. Shuningdek u avtomatik ravishda boshlang'ich bo'sh joylarni (incidental whitespace) kesib tashlaydi.

## Ishlash natijasi:
```text
Formatlangan JSON:
{
    "ism": "Dilshod",
    "rol": "Dasturchi",
    "tajribaYillari": 5
}
```

---

# 27-Topshiriq: BigDecimal bilan moliyaviy hisob-kitoblar

## Topshiriq sharti:
Bank va to'lov tizimlarida nima sababdan `double` emas, `BigDecimal` qo'llanilishini aniq hisob misolida ko'rsating.

## Yechim (Java kodi):
```java
import java.math.BigDecimal;
import java.math.RoundingMode;

public class Solution {
    public static void main(String[] args) {
        BigDecimal balans = new BigDecimal("100.05");
        BigDecimal tolov = new BigDecimal("40.03");
        
        BigDecimal qoldiq = balans.subtract(tolov);
        System.out.println("Qoldiq mablag': " + qoldiq);
        
        BigDecimal son = new BigDecimal("10");
        BigDecimal bolish = son.divide(new BigDecimal("3"), 4, RoundingMode.HALF_UP);
        System.out.println("10 / 3 (4 ta kasr raqami): " + bolish);
    }
}
```

## Tushuntirish va Mantiq:
`BigDecimal` ixtiyoriy aniqlikdagi o'nlik kasrlar bilan xatosiz ishlash uchun mo'ljallangan klassdir.
Muhim qoida: `BigDecimal` konstruktoriga `double` emas, `String` uzatish shart (masalan `new BigDecimal("100.05")`). Aks holda double ning noaniqligi BigDecimal ga ham ko'chadi.
Bo'lish amallarida cheksiz davriy kasrlar bo'lmasligi uchun yaxlitlash rejimi (`RoundingMode`) ko'rsatiladi.

## Ishlash natijasi:
```text
Qoldiq mablag': 60.02
10 / 3 (4 ta kasr raqami): 3.3333
```

---

# 28-Topshiriq: BigInteger bilan o'ta ulkan sonlar ustida amallar

## Topshiriq sharti:
64-bitli `long` sig'dira olmaydigan o'ta yirik sonlarning (masalan, 50 ning faktoriali) ko'paytmasini `BigInteger` yordamida hisoblang.

## Yechim (Java kodi):
```java
import java.math.BigInteger;

public class Solution {
    public static void main(String[] args) {
        BigInteger a = new BigInteger("123456789012345678901234567890");
        BigInteger b = new BigInteger("987654321098765432109876543210");
        
        BigInteger kopaytma = a.multiply(b);
        System.out.println("Katta sonlar ko'paytmasi:
" + kopaytma);
    }
}
```

## Tushuntirish va Mantiq:
`BigInteger` xotira yetarli bo'lgan barcha o'lchamdagi butun sonlarni saqlay oladi va ustida arifmetik amallar bajaradi.
U o'zgarmas (immutable) bo'lib, har bir amal (`add`, `multiply`, `pow`) yangi `BigInteger` obyektini qaytaradi. U kriptografiya va ilmiy tadqiqotlarda keng qo'llaniladi.

## Ishlash natijasi:
```text
Katta sonlar ko'paytmasi:
121932631137021795226185032733622923332237463801111263526900
```

---

# 29-Topshiriq: Math sinfi metodlari va trigonometrik amallar

## Topshiriq sharti:
`Math.sqrt()`, `Math.pow()`, `Math.abs()` va `Math.max()` metodlaridan foydalanib to'g'ri burchakli uchburchak gipotenuzasini toping.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        double katet1 = 3.0;
        double katet2 = 4.0;
        
        double gipotenuza = Math.sqrt(Math.pow(katet1, 2) + Math.pow(katet2, 2));
        System.out.println("Katetlar: " + katet1 + ", " + katet2);
        System.out.println("Gipotenuza: " + gipotenuza);
        System.out.println("Kattasi: " + Math.max(katet1, katet2));
    }
}
```

## Tushuntirish va Mantiq:
`java.lang.Math` sinfi barcha matematik hisoblashlar uchun statik metodlar to'plamini taqdim etadi.
Uning konstruktori `private` qilingan bo'lib, undan obyekt olinmaydi (Utility class pattern).
Metodlar apparat darajasida protsessorning FPU (Floating Point Unit) instruksiyalari bilan tez bajariladi.

## Ishlash natijasi:
```text
Katetlar: 3.0, 4.0
Gipotenuza: 5.0
Kattasi: 4.0
```

---

# 30-Topshiriq: Primitiv tiplarning default qiymatlari vs Local o'zgaruvchilar

## Topshiriq sharti:
Sinf maydonlarining (fields) sukut bo'yicha oladigan default qiymatlarini hamda mahalliy (local) o'zgaruvchilar initsializatsiya qilinishi shartligini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static byte dByte;
    static short dShort;
    static int dInt;
    static long dLong;
    static float dFloat;
    static double dDouble;
    static char dChar;
    static boolean dBoolean;
    static String dString;

    public static void main(String[] args) {
        System.out.println("byte: " + dByte);
        System.out.println("int: " + dInt);
        System.out.println("double: " + dDouble);
        System.out.println("boolean: " + dBoolean);
        System.out.println("char kodi: " + (int) dChar);
        System.out.println("reference (String): " + dString);
        
        // int local;
        // System.out.println(local); // XATO: local variable might not have been initialized
    }
}
```

## Tushuntirish va Mantiq:
Java-da sinf darajasidagi (static yoki instance) maydonlar obyekt yaratilganda avtomatik ravishda xotirada nol bilan to'ldiriladi:
- Sonlar: `0` yoki `0.0`
- char: `\u0000` (nol belgisi)
- boolean: `false`
- Reference tiplar: `null`
Lokal (metod ichidagi) o'zgaruvchilar esa avtomatik qiymat olmaydi; ulardan foydalanishdan oldin qiymat berish majburiydir.

## Ishlash natijasi:
```text
byte: 0
int: 0
double: 0.0
boolean: false
char kodi: 0
reference (String): null
```

---

# 31-Topshiriq: Null ko'rsatkichi va xotira arxitekturasi

## Topshiriq sharti:
`null` ko'rsatkichining Stack va Heap xotiradagi ma'nosini va ob'ektga murojaat qilishda xatolik yuz berishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String havola = null;
        System.out.println("Havola qiymati: " + havola);
        
        try {
            int uzunlik = havola.length();
            System.out.println(uzunlik);
        } catch (NullPointerException e) {
            System.out.println("Xotirada mavjud bo'lmagan manzilga murojaat: " + e);
        }
    }
}
```

## Tushuntirish va Mantiq:
Java-da har qanday reference o'zgaruvchi Stack xotirada joylashadi. U Heap xotiradagi obyektning manzilini o'zida saqlaydi.
`null` kalit so'zi o'zgaruvchining Stack da mavjudligini, ammo u Heap dagi hech qanday xotira manziliga ko'rsatmayotganini (0x0 manzili) bildiradi.
Bo'sh manzil ustida biron metod chaqirish JVM da `NullPointerException` keltirib chiqaradi.

## Ishlash natijasi:
```text
Havola qiymati: null
Xotirada mavjud bo'lmagan manzilga murojaat: java.lang.NullPointerException: Cannot invoke "String.length()" because "havola" is null
```

---

# 32-Topshiriq: Double.NaN va Cheksizlik (Infinity) holatlari

## Topshiriq sharti:
Suzuvchi nuqtali sonlarda nolga bo'lish va kvadrat ildizdan manfiy son olishdagi `Infinity` va `NaN` xatti-harakatlarini tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        double cheksiz = 10.0 / 0.0;
        double manfiyCheksiz = -10.0 / 0.0;
        double sonEmas = Math.sqrt(-4);
        
        System.out.println("10.0 / 0.0 = " + cheksiz);
        System.out.println("-10.0 / 0.0 = " + manfiyCheksiz);
        System.out.println("sqrt(-4) = " + sonEmas);
        System.out.println("NaN == NaN: " + (sonEmas == Double.NaN));
        System.out.println("Double.isNaN(): " + Double.isNaN(sonEmas));
    }
}
```

## Tushuntirish va Mantiq:
Butun sonlarda (`int`) nolga bo'lish `ArithmeticException` tashlaydi. Ammo suzuvchi nuqtali `double` va `float` da istisno tashlanmaydi, buning o'rniga IEEE 754 bo'yicha `Infinity` yoki `-Infinity` hosil bo'ladi.
Noma'lum amallar natijasi esa `NaN` (Not a Number) bo'ladi.
`NaN` o'ziga ham teng bo'lmagan yagona qiymatdir (`NaN == NaN` har doim `false`), shu sababli tekshirish uchun `Double.isNaN()` metodi ishlatiladi.

## Ishlash natijasi:
```text
10.0 / 0.0 = Infinity
-10.0 / 0.0 = -Infinity
sqrt(-4) = NaN
NaN == NaN: false
Double.isNaN(): true
```

---

# 33-Topshiriq: Math.round, Math.floor va Math.ceil farqlari

## Topshiriq sharti:
Haqiqiy sonlarni yaxlitlashdagi uch xil yondashuv: `round` (eng yaqin butun), `floor` (pastga yaxlitlash) va `ceil` (yuqoriga yaxlitlash) farqlarini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        double son1 = 5.3;
        double son2 = 5.8;
        double son3 = -5.8;
        
        System.out.println("Math.round(5.3): " + Math.round(son1));
        System.out.println("Math.floor(5.8): " + Math.floor(son2));
        System.out.println("Math.ceil(5.3): " + Math.ceil(son1));
        
        System.out.println("Math.floor(-5.8): " + Math.floor(son3));
        System.out.println("Math.ceil(-5.8): " + Math.ceil(son3));
    }
}
```

## Tushuntirish va Mantiq:
- `Math.floor()`: Sonni o'zidan kichik yoki teng bo'lgan eng yaqin butun songa pastga qarab yaxlitlaydi (-5.8 -> -6.0).
- `Math.ceil()`: Sonni o'zidan katta yoki teng bo'lgan eng yaqin butun songa yuqoriga qarab yaxlitlaydi (-5.8 -> -5.0).
- `Math.round()`: Arifmetik qoida bo'yicha eng yaqin butun songa yaxlitlaydi (0.5 va undan katta bo'lsa yuqoriga).

## Ishlash natijasi:
```text
Math.round(5.3): 5
Math.floor(5.8): 5.0
Math.ceil(5.3): 6.0
Math.floor(-5.8): -6.0
Math.ceil(-5.8): -5.0
```

---

# 34-Topshiriq: Character utilitasi bilan belgilarni tahlil qilish

## Topshiriq sharti:
`Character.isDigit()`, `isLetter()`, `isWhitespace()` va `toUpperCase()` metodlaridan foydalanib matn belgilarini tahlil qiluvchi dastur yozing.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        char c1 = '7';
        char c2 = 'A';
        char c3 = ' ';
        
        System.out.println(c1 + " raqammi: " + Character.isDigit(c1));
        System.out.println(c2 + " harfmi: " + Character.isLetter(c2));
        System.out.println(c3 + " bo'sh joymi: " + Character.isWhitespace(c3));
        System.out.println("Kichik harfga o'tkazish: " + Character.toLowerCase(c2));
    }
}
```

## Tushuntirish va Mantiq:
`Character` sinfi Unicode standartidagi belgilarni tekshirish va o'zgartirish uchun qulay metodlarni taqdim etadi.
Bu metodlar Unicode belgilar jadvalini to'liq biladi, ya'ni faqat ASCII emas, balki boshqa alifbolardagi raqam va harflarni ham to'g'ri ajrata oladi.

## Ishlash natijasi:
```text
7 raqammi: true
A harfmi: true
  bo'sh joymi: true
Kichik harfga o'tkazish: a
```

---

# 35-Topshiriq: Arifmetikada Type Promotion (Tiplarning ko'tarilishi)

## Topshiriq sharti:
`byte` va `short` tiplari arifmetik amallarda qatnashganda qanday qilib avtomatik ravishda `int` ga ko'tarilishini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        byte a = 10;
        byte b = 20;
        // byte c = a + b; // Kompilyatsiya xatosi! Natija int bo'ldi!
        int c = a + b;
        byte d = (byte) (a + b);
        
        System.out.println("int natija: " + c);
        System.out.println("byte kasting qilingan natija: " + d);
    }
}
```

## Tushuntirish va Mantiq:
Java-da binar operatorlar (`+`, `-`, `*`, `/`) ishlaganda quyidagi Type Promotion qoidalari amal qiladi:
1. Agar biron operand `double` bo'lsa, hammasi `double` ga o'tadi.
2. Aks holda, agar `float` bo'lsa, `float` ga o'tadi.
3. Aks holda, agar `long` bo'lsa, `long` ga o'tadi.
4. Aks holda, barcha `byte`, `short`, `char` lar operatsiyadan oldin darhol `int` ga ko'tariladi!
Shu sababli `a + b` natijasi `int` bo'ladi.

## Ishlash natijasi:
```text
int natija: 30
byte kasting qilingan natija: 30
```

---

# 36-Topshiriq: Random sonlar: Math.random() vs ThreadLocalRandom

## Topshiriq sharti:
Java-da tasodifiy sonlar hosil qilishning ikki xil usulini (`Math.random()` va yuqori unumdorlikdagi `ThreadLocalRandom`) ko'rsating.

## Yechim (Java kodi):
```java
import java.util.concurrent.ThreadLocalRandom;

public class Solution {
    public static void main(String[] args) {
        // 1 dan 10 gacha tasodifiy butun son
        int r1 = (int) (Math.random() * 10) + 1;
        
        // ThreadLocalRandom (eng zamonaviy va tezkor usul)
        int r2 = ThreadLocalRandom.current().nextInt(1, 11);
        
        System.out.println("Math.random() orqali olingan son (1-10 oralig'ida): " + (r1 >= 1 && r1 <= 10));
        System.out.println("ThreadLocalRandom orqali olingan son (1-10 oralig'ida): " + (r2 >= 1 && r2 <= 10));
    }
}
```

## Tushuntirish va Mantiq:
`Math.random()` ichki holatda bitta global `Random` obyekti bilan ishlaydi. Ko'p oqimli (multithreading) tizimlarda bir nechta oqim ayni bir vaqtda son so'rasa, contention (raqobat) tufayli tezlik pasayadi.
`ThreadLocalRandom` esa har bir oqim uchun alohida generator urug'ini (seed) saqlaydi, qulflashsiz (lock-free) ishlaydi va ancha tez hisoblanadi.

## Ishlash natijasi:
```text
Math.random() orqali olingan son (1-10 oralig'ida): true
ThreadLocalRandom orqali olingan son (1-10 oralig'ida): true
```

---

# 37-Topshiriq: Formatlangan chiqarish: String.format va printf

## Topshiriq sharti:
Jadval ko'rinishidagi ma'lumotlarni `System.out.printf()` va `String.format()` yordamida aniq ustun kengligi bilan formatlab chiqaring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String mahsulot = "Olma";
        int miqdor = 15;
        double narx = 12500.50;
        
        String satr = String.format("%-10s | %5d dona | %10.2f so'm", mahsulot, miqdor, narx);
        System.out.println("Formatlangan qator:");
        System.out.println(satr);
    }
}
```

## Tushuntirish va Mantiq:
Formatlash modifikatorlari:
- `%-10s`: 10 ta belgilik maydonda chap tomonga tekislangan satr
- `%5d`: 5 ta belgilik maydonda o'ng tomonga tekislangan butun son
- `%10.2f`: 10 ta belgilik maydonda 2 ta kasr raqami bilan haqiqiy son
Bu usul hisobotlar va konsol jadvallarini tekis chiqarishda juda qo'l keladi.

## Ishlash natijasi:
```text
Formatlangan qator:
Olma       |    15 dona |   12500.50 so'm
```

---

# 38-Topshiriq: System.identityHashCode() va haqiqiy obyekt identifikatori

## Topshiriq sharti:
`hashCode()` qayta yozilgan (overridden) holatda ham obyektning asl xotira identifikatorini `System.identityHashCode()` orqali aniqlashni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Shaxs {
        String passport;
        Shaxs(String passport) { this.passport = passport; }
        
        @Override
        public int hashCode() { return 42; } // Qasddan soxta qilingan
    }

    public static void main(String[] args) {
        Shaxs s1 = new Shaxs("AA123");
        Shaxs s2 = new Shaxs("AA123");
        
        System.out.println("s1.hashCode(): " + s1.hashCode());
        System.out.println("s2.hashCode(): " + s2.hashCode());
        System.out.println("Asl s1 identityHashCode: " + (System.identityHashCode(s1) != 0));
        System.out.println("Asl s2 identityHashCode: " + (System.identityHashCode(s2) != 0));
        System.out.println("Ular turli obyektlarmi: " + (System.identityHashCode(s1) != System.identityHashCode(s2)));
    }
}
```

## Tushuntirish va Mantiq:
`hashCode()` metodi sinfda qayta yozilishi mumkin. Ammo JVM ning asl unikal obyekt identifikatori (default Object.hashCode()) kerak bo'lsa, `System.identityHashCode(obj)` chaqiriladi.
U obyektning xotiradagi asl manzilidan hosil bo'ladi va ikkita har xil yangi obyekt uchun turlicha bo'ladi.

## Ishlash natijasi:
```text
s1.hashCode(): 42
s2.hashCode(): 42
Asl s1 identityHashCode: true
Asl s2 identityHashCode: true
Ular turli obyektlarmi: true
```

---

# 39-Topshiriq: Enum tipi bilan xavfsiz konstantalar

## Topshiriq sharti:
Oddiy `int` konstantalari o'rniga tur xavfsizligini ta'minlovchi `enum` (sanab o'tiladigan tip) yaratish va uning qiymatlarini ekranga chiqarish dasturini tuzing.

## Yechim (Java kodi):
```java
public class Solution {
    enum BuyurtmaHolati {
        YANGI,
        TOLANDI,
        YETKAZILMOQDA,
        YAKUNLANDI
    }

    public static void main(String[] args) {
        BuyurtmaHolati joriyHolat = BuyurtmaHolati.TOLANDI;
        System.out.println("Joriy holat: " + joriyHolat);
        System.out.println("Holat tartib raqami (ordinal): " + joriyHolat.ordinal());
        System.out.println("Holat nomi (name): " + joriyHolat.name());
    }
}
```

## Tushuntirish va Mantiq:
Java-da `enum` maxsus sinf turi hisoblanadi. U `java.lang.Enum` dan meros oladi.
U turlar xavfsizligini (Type Safety) kafolatlaydi, ya'ni o'zgaruvchiga ro'yxatda bo'lmagan soxta qiymat berib bo'lmaydi.
Har bir enum elementi statik yagona (singleton) instansiya bo'lib, xotirada faqat bitta nusxada mavjud bo'ladi.

## Ishlash natijasi:
```text
Joriy holat: TOLANDI
Holat tartib raqami (ordinal): 1
Holat nomi (name): TOLANDI
```

---

# 40-Topshiriq: O'zgaruvchilarning ko'rinish sohasi (Variable Scope)

## Topshiriq sharti:
Blok darajasidagi, metod darajasidagi va sinf darajasidagi o'zgaruvchilarning hayot davri va ko'rinish chegaralarini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    static int sinfMaydoni = 100; // Sinf darajasi

    public static void main(String[] args) {
        int metodOzgaruvchisi = 50; // Metod darajasi
        
        {
            int blokOzgaruvchisi = 25; // Blok darajasi
            System.out.println("Blok ichida barchasi ko'rinadi: " + (sinfMaydoni + metodOzgaruvchisi + blokOzgaruvchisi));
        }
        
        // blokOzgaruvchisi bu yerda mavjud emas!
        System.out.println("Blok tashqarisida: " + (sinfMaydoni + metodOzgaruvchisi));
    }
}
```

## Tushuntirish va Mantiq:
O'zgaruvchining ko'rinish sohasi (scope) u e'lon qilingan jingalak qavslar `{ ... }` bilan belgilanadi:
- Sinf maydoni: Dastur ishlash davrida yashaydi.
- Metod o'zgaruvchisi: Metod chaqirilganda Stack freymda ochiladi va metod tugashi bilan o'chiriladi.
- Blok o'zgaruvchisi: Faqat o'sha blok ichida ko'rinadi va blok tugashi bilan Stack dan yo'qotiladi.

## Ishlash natijasi:
```text
Blok ichida barchasi ko'rinadi: 175
Blok tashqarisida: 150
```

---

# 41-Topshiriq: Shadowing (O'zgaruvchini to'sib qo'yish) hodisasi

## Topshiriq sharti:
Mahalliy o'zgaruvchi sinf maydoni bilan bir xil nomlanganda yuz beradigan Shadowing hodisasini va `this` orqali uni ajratishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Avto {
        String model = "Noma'lum";
        
        void setModel(String model) {
            // model = model; // XATO: Shadowing tufayli o'ziga o'zi yozilyapti!
            this.model = model; // 'this' orqali sinf maydoniga murojaat qilinadi
        }
    }

    public static void main(String[] args) {
        Avto avto = new Avto();
        avto.setModel("Cobalt");
        System.out.println("Avtomobil modeli: " + avto.model);
    }
}
```

## Tushuntirish va Mantiq:
Shadowing - bir xil nomli lokal o'zgaruvchi tashqi (masalan, sinf maydoni) o'zgaruvchini to'sib qo'yishidir.
Bu holda shunchaki nom bilan murojaat qilinsa, eng yaqin ko'rinish sohasidagi (lokal) o'zgaruvchi olinadi. Obyekt maydonini aniq ko'rsatish uchun `this.maydon` sintaksisi qo'llaniladi.

## Ishlash natijasi:
```text
Avtomobil modeli: Cobalt
```

---

# 42-Topshiriq: Konstanta ifodalar (Constant Inlining)

## Topshiriq sharti:
Kompilyatsiya vaqtida hisoblab qo'yiladigan o'zgarmaslar (Compile-time constants) va ularning baytkoddagi inlining optimizatsiyasini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static final int SOAT = 24;
    public static final int DAQIQA = 60;
    public static final int BIR_KUNDAGI_DAQIQALAR = SOAT * DAQIQA; // Compile-time constant

    public static void main(String[] args) {
        System.out.println("Bir kundagi daqiqalar soni: " + BIR_KUNDAGI_DAQIQALAR);
    }
}
```

## Tushuntirish va Mantiq:
Agar `final` o'zgaruvchining qiymati kompilyatsiya vaqtida ma'lum bo'lgan literallardan tashkil topsa, kompilyator uning natijasini hisoblab to'g'ridan-to'g'ri baytkodga yozib qo'yadi.
Dastur ishga tushganda hech qanday ko'paytirish amali bajarilmaydi, to'g'ridan-to'g'ri `1440` doimiysi yuklanadi.

## Ishlash natijasi:
```text
Bir kundagi daqiqalar soni: 1440
```

---

# 43-Topshiriq: Tiplarni xavfsiz o'girish: valueOf vs parseXxx

## Topshiriq sharti:
Satrni songa o'girishda `Integer.parseInt()` (primitiv qaytaruvchi) va `Integer.valueOf()` (obyekt keshini qaytaruvchi) orasidagi farqni tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String matn = "100";
        
        int p = Integer.parseInt(matn); // int qaytaradi
        Integer v = Integer.valueOf(matn); // Integer keshdan qaytaradi
        
        System.out.println("parseInt natijasi: " + p);
        System.out.println("valueOf natijasi: " + v);
        System.out.println("Bir xil obyektmi: " + (v == Integer.valueOf(100)));
    }
}
```

## Tushuntirish va Mantiq:
- `Integer.parseInt(s)`: To'g'ridan-to'g'ri primitiv `int` tipidagi qiymat qaytaradi. Ortiqcha xotira va obyekt sarflanmaydi.
- `Integer.valueOf(s)`: `Integer` wrapper obyektini qaytaradi va -128..127 oraliqda keshdan foydalanadi.
Kolleksiyalarga qo'shish uchun `valueOf()`, oddiy hisob-kitoblar uchun esa `parseInt()` tavsiya etiladi.

## Ishlash natijasi:
```text
parseInt natijasi: 100
valueOf natijasi: 100
Bir xil obyektmi: true
```

---

# 44-Topshiriq: Garbage Collection ga nomzod bo'lish mexanizmi

## Topshiriq sharti:
Heap xotiradagi ob'ektning havolasini uzish (`null` qilish) orqali ob'ektni Garbage Collector (Chiqindi yig'uvchi) uchun nomzod qilishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class Resurs {
        String nom;
        Resurs(String nom) { this.nom = nom; }
    }

    public static void main(String[] args) {
        Resurs r1 = new Resurs("Fayl Ma'lumotlari");
        System.out.println("Obyekt mavjud: " + r1.nom);
        
        // Havola uziladi
        r1 = null; 
        System.out.println("r1 endi null ga ko'rsatmoqda, Heap dagi obyekt GC uchun ochiq.");
    }
}
```

## Tushuntirish va Mantiq:
Java-da xotirani tozalash avtomatik ravishda Garbage Collector (GC) tomonidan boshqariladi.
Agar Heap xotiradagi biror obyektga Stack freymlardan, statik maydonlardan yoki boshqa tirik obyektlardan hech qanday havola (root reference) qolmasa, u ob'ekt "yetib bo'lmas" (unreachable) deb hisoblanadi va GC uni xotiradan tozalaydi.

## Ishlash natijasi:
```text
Obyekt mavjud: Fayl Ma'lumotlari
r1 endi null ga ko'rsatmoqda, Heap dagi obyekt GC uchun ochiq.
```

---

# 45-Topshiriq: Record sinfi asoslari (Java 16+)

## Topshiriq sharti:
Java 16 da rasmiy joriy etilgan `record` yordamida o'zgarmas (immutable) ma'lumotlar modelini 1 qatorda e'lon qiling va uning getter hamda `toString()` metodlarini namoyish eting.

## Yechim (Java kodi):
```java
public class Solution {
    record Foydalanuvchi(String login, String email, int yosh) {}

    public static void main(String[] args) {
        Foydalanuvchi user = new Foydalanuvchi("bobur_dev", "bobur@gmail.com", 25);
        
        System.out.println("Foydalanuvchi: " + user);
        System.out.println("Login: " + user.login());
        System.out.println("Email: " + user.email());
        System.out.println("Yosh: " + user.yosh());
    }
}
```

## Tushuntirish va Mantiq:
`record` - faqat ma'lumotlarni tashish uchun mo'ljallangan ixcham sinf konstruksiyasidir.
Kompilyator avtomatik ravishda:
- Barcha maydonlarni `private final` qilib yaratadi;
- Kanonik konstruktorni hosil qiladi;
- Getter metodlarni (`user.login()` - 'get' prefiksisiz) yaratadi;
- `equals()`, `hashCode()` va `toString()` metodlarini to'liq generatsiya qiladi.

## Ishlash natijasi:
```text
Foydalanuvchi: Foydalanuvchi[login=bobur_dev, email=bobur@gmail.com, yosh=25]
Login: bobur_dev
Email: bobur@gmail.com
Yosh: 25
```

---

# 46-Topshiriq: Bitwise amallarda int Type Promotion ta'siri

## Topshiriq sharti:
`byte` ustida bitli surish (`<<` yoki `>>`) amali bajarilganda nima sababdan `(byte)` kasting talab etilishini tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        byte b = 1;
        // byte surilgan = b << 2; // Kompilyatsiya xatosi: int byte ga to'g'ridan to'g'ri o'tmaydi!
        byte surilgan = (byte) (b << 2);
        
        System.out.println("Dastlabki: " + b);
        System.out.println("2 bit chapga surilganda (1 * 4): " + surilgan);
    }
}
```

## Tushuntirish va Mantiq:
Java-da bitli siljitish (`<<`, `>>`, `>>>`) va bitli mantiqiy (`&`, `|`, `^`) operatorlar `byte` yoki `short` uchun alohida instruksiyalarga ega emas. Ular har doim operandni `int` ga ko'tarib (32-bitga) bajaradi.
Shuning uchun natija 32-bitli `int` bo'ladi va uni yana `byte` ga yozish uchun aniq kasting talab qilinadi.

## Ishlash natijasi:
```text
Dastlabki: 1
2 bit chapga surilganda (1 * 4): 4
```

---

# 47-Topshiriq: String.intern() va xotirani tejash

## Topshiriq sharti:
Ko'p takrorlanuvchi satrlarni xotirada optimallashtirish uchun `intern()` metodining amaliy qo'llanilishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String mamlakat1 = new String("O'zbekiston").intern();
        String mamlakat2 = new String("O'zbekiston").intern();
        
        System.out.println("Ikkita mustaqil yaratilgan satr intern orqali bir xil manzilga keldimi: " + (mamlakat1 == mamlakat2));
    }
}
```

## Tushuntirish va Mantiq:
Katta hajmdagi ma'lumotlar o'qilganda (masalan, CSV yoki bazadan millionlab "O'zbekiston" satri) har bir satr uchun yangi `String` obyekti yaratilsa xotira to'lib ketadi.
`intern()` metodi barcha bir xil satrlarni String Pooldagi bitta manzilga bog'laydi va qolgan ortiqcha nusxalarni GC tozalashiga imkon yaratadi.

## Ishlash natijasi:
```text
Ikkita mustaqil yaratilgan satr intern orqali bir xil manzilga keldimi: true
```

---

# 48-Topshiriq: O'nlik sonlarni yaxlitlashdagi toq/juft qoidasi (Banker's Rounding)

## Topshiriq sharti:
`BigDecimal` da `RoundingMode.HALF_EVEN` (Bankirlar yaxlitlashi) qanday ishlashini va nega moliya sohasida standart ekanini ko'rsating.

## Yechim (Java kodi):
```java
import java.math.BigDecimal;
import java.math.RoundingMode;

public class Solution {
    public static void main(String[] args) {
        BigDecimal son1 = new BigDecimal("2.5");
        BigDecimal son2 = new BigDecimal("1.5");
        
        System.out.println("2.5 HALF_EVEN yaxlitlanganda: " + son1.setScale(0, RoundingMode.HALF_EVEN));
        System.out.println("1.5 HALF_EVEN yaxlitlanganda: " + son2.setScale(0, RoundingMode.HALF_EVEN));
    }
}
```

## Tushuntirish va Mantiq:
Bankir yaxlitlashi (Half-Even) o'rtadagi `.5` qiymatini har doim eng yaqin JUFT butun songa qarab yaxlitlaydi.
Shu sababli 2.5 ham 2 ga, 1.5 ham 2 ga yaxlitlanadi.
Bu katta moliyaviy hisob-kitoblarda doim yuqoriga yaxlitlashdan kelib chiqadigan statistik xatolik (bias) ni muvozanatlash uchun IEEE standarti sifatida tan olingan.

## Ishlash natijasi:
```text
2.5 HALF_EVEN yaxlitlanganda: 2
1.5 HALF_EVEN yaxlitlanganda: 2
```

---

# 49-Topshiriq: Final parametrlar va nojo'ya ta'sirlarni oldini olish

## Topshiriq sharti:
Metod parametrlarini `final` deb e'lon qilish orqali xatoliklarning oldini olish texnikasini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static int hisobla(final int asosiyNarx, final int chegirmaFoizi) {
        // asosiyNarx = 0; // Kompilyatsiya xatosi: final parametrni o'zgartirib bo'lmaydi!
        return asosiyNarx - (asosiyNarx * chegirmaFoizi / 100);
    }

    public static void main(String[] args) {
        int natija = hisobla(200000, 15);
        System.out.println("15% chegirma bilan yakuniy narx: " + natija);
    }
}
```

## Tushuntirish va Mantiq:
Metod parametrlariga `final` kalit so'zini qo'yish ishlab chiquvchining ehtiyotsizlik qilib parametr qiymatini metod tanasida qayta yozib yuborishining (reassigning parameters) oldini oladi.
Bu toza kod (Clean Code) yozishda va funksional dasturlash tamoyillarini saqlashda juda foydali amaliyotdir.

## Ishlash natijasi:
```text
15% chegirma bilan yakuniy narx: 170000
```

---

# 50-Topshiriq: Xulosa topshiriq: Do'kon savdo chekini hisoblovchi to'liq tizim

## Topshiriq sharti:
Barcha o'rganilgan asosiy tiplar (int, double, String, boolean, final, BigDecimal) dan foydalanib xarid chekini to'liq hisoblovchi va chop etuvchi dastur tuzing.

## Yechim (Java kodi):
```java
import java.math.BigDecimal;
import java.math.RoundingMode;

public class Solution {
    public static void main(String[] args) {
        final String DOKON_NOMI = "Supermarket 'Oazis'";
        String tovarNomi = "Kungaboqar yog'i (1L)";
        int dona = 3;
        BigDecimal birDonaNarxi = new BigDecimal("18500.00");
        BigDecimal soliqStavkasi = new BigDecimal("0.12"); // 12% QQS
        boolean chegirmaBormi = true;
        double chegirmaFoizi = 5.0; // 5%
        
        BigDecimal jamiSofNarx = birDonaNarxi.multiply(BigDecimal.valueOf(dona));
        BigDecimal chegirmaMablagi = chegirmaBormi 
                ? jamiSofNarx.multiply(BigDecimal.valueOf(chegirmaFoizi / 100))
                : BigDecimal.ZERO;
        BigDecimal chegirmaliNarx = jamiSofNarx.subtract(chegirmaMablagi);
        BigDecimal qqsMablagi = chegirmaliNarx.multiply(soliqStavkasi);
        BigDecimal yakuniyTolash = chegirmaliNarx.add(qqsMablagi).setScale(2, RoundingMode.HALF_UP);
        
        System.out.println("=========================================");
        System.out.println("             " + DOKON_NOMI);
        System.out.println("=========================================");
        System.out.println("Mahsulot: " + tovarNomi);
        System.out.println("Miqdor: " + dona + " dona x " + birDonaNarxi + " so'm");
        System.out.println("Oraliq summa: " + jamiSofNarx + " so'm");
        System.out.println("Chegirma (5%): -" + chegirmaMablagi.setScale(2, RoundingMode.HALF_UP) + " so'm");
        System.out.println("QQS (12%): +" + qqsMablagi.setScale(2, RoundingMode.HALF_UP) + " so'm");
        System.out.println("-----------------------------------------");
        System.out.println("JAMI TO'LOV: " + yakuniyTolash + " so'm");
        System.out.println("=========================================");
    }
}
```

## Tushuntirish va Mantiq:
Ushbu kompleks topshiriqda:
1. `final` konstanta orqali do'kon nomi belgilandi.
2. Moliyaviy aniqlik uchun `BigDecimal` dan foydalanildi, bu suzuvchi nuqtali noaniqliklarni istisno qiladi.
3. Shartli mantiq (`boolean` va ternary operator) orqali chegirma hisoblandi.
4. QQS solig'i hisoblanib, yakuniy summa `RoundingMode.HALF_UP` bilan yaxlitlandi.
5. Chiqarish matnlari orqali xarid cheki professional ko'rinishda taqdim etildi.

## Ishlash natijasi:
```text
=========================================
             Supermarket 'Oazis'
=========================================
Mahsulot: Kungaboqar yog'i (1L)
Miqdor: 3 dona x 18500.00 so'm
Oraliq summa: 55500.00 so'm
Chegirma (5%): -2775.00 so'm
QQS (12%): +6327.00 so'm
-----------------------------------------
JAMI TO'LOV: 59052.00 so'm
=========================================
```
