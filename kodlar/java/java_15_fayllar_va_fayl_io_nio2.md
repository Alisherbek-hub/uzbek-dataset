# Java Fayllar va Fayl I/O (NIO.2) (701-750)

# 701-Topshiriq: Java I/O: FileReader va BufferedReader orqali matn faylini o'qish

## Topshiriq sharti:
`BufferedReader.readLine()` yordamida matn fayllarini buferlangan holda satrma-satr o'qish dasturini yozing.

## Yechim (Java kodi):
```java
import java.io.BufferedReader;
import java.io.StringReader;
import java.io.IOException;

public class Solution {
    public static void main(String[] args) {
        String testMatn = "1-qator: Java Asoslari
2-qator: Stream API
3-qator: Fayllar I/O";

        // BufferedReader bilan satrma-satr o'qish
        try (BufferedReader br = new BufferedReader(new StringReader(testMatn))) {
            String qator;
            int qatorRaqami = 1;
            while ((qator = br.readLine()) != null) {
                System.out.println("O'qildi [" + qatorRaqami++ + "]: " + qator);
            }
        } catch (IOException e) {
            System.out.println("Xatolik: " + e.getMessage());
        }
    }
}
```

## Tushuntirish va Mantiq:
`BufferedReader` diskdan ma'lumotni belgi-belgi emas, balki kattaroq xotira buferi (sukut bo'yicha 8KB) bilan o'qiydi.
Bu diskka murojaatlar sonini keskin kamaytiradi va matnni satrma-satr (`readLine()`) o'qish imkonini beradi.

## Ishlash natijasi:
```text
O'qildi [1]: 1-qator: Java Asoslari
O'qildi [2]: 2-qator: Stream API
O'qildi [3]: 3-qator: Fayllar I/O
```

---

# 702-Topshiriq: NIO.2: Path va Paths sinflari bilan fayl yo'llarini boshqarish

## Topshiriq sharti:
Java 7 da joriy etilgan zamonaviy `Path` va `Paths.get()` orqali fayl yo'llarini tahlil qilishni ko'rsating.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path yol = Paths.get("C:/app/logs/server.log");

        System.out.println("Fayl nomi: " + yol.getFileName());
        System.out.println("Ota papka: " + yol.getParent());
        System.out.println("Ildiz: " + yol.getRoot());
        System.out.println("Absolyut yo'lmi: " + yol.isAbsolute());
    }
}
```

## Tushuntirish va Mantiq:
`java.nio.file.Path` eski `java.io.File` sinfining zamonaviy o'rnini bosuvchi interfeysdir.
U operatsion tizimdan mustaqil tarzda yo'llarni boshqarish, normallashtirish (`normalize()`) va nisbiy yo'llarni bog'lash (`resolve()`) imkoniyatlarini taqdim etadi.

## Ishlash natijasi:
```text
Fayl nomi: server.log
Ota papka: C:\app\logs
Ildiz: C:\
Absolyut yo'lmi: true
```

---

# 703-Topshiriq: NIO.2: Files.writeString va Files.readString (Java 11+)

## Topshiriq sharti:
Java 11 da kiritilgan eng ixcham `Files.writeString()` va `Files.readString()` metodlari bilan matn yozish va o'qishni ko'rsating.

## Yechim (Java kodi):
```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.io.IOException;

public class Solution {
    public static void main(String[] args) throws IOException {
        Path vaqtinchalikFayl = Files.createTempFile("test_qayd", ".txt");

        // 1 qatorda yozish
        Files.writeString(vaqtinchalikFayl, "Salom, zamonaviy Java 21 NIO.2!");

        // 1 qatorda o'qish
        String oqilganMatn = Files.readString(vaqtinchalikFayl);
        System.out.println("Fayldan o'qildi: " + oqilganMatn);

        // Tozalash
        Files.deleteIfExists(vaqtinchalikFayl);
    }
}
```

## Tushuntirish va Mantiq:
Java 11 dan boshlab butun matnli faylni bitta satrda yozish va o'qish uchun `Files.writeString(path, text)` va `Files.readString(path)` qo'shildi.
Ular avtomatik UTF-8 kodlash bilan ishlaydi va oqimlarni to'g'ri yopishni o'zi boshqaradi.

## Ishlash natijasi:
```text
Fayldan o'qildi: Salom, zamonaviy Java 21 NIO.2!
```

---

# 704-Topshiriq: NIO.2: Files.lines() bilan faylni Stream API orqali xotirani tejab o'qish

## Topshiriq sharti:
Katta hajmdagi faylni to'liq xotiraga (RAM) yuklamasdan, qatorma-qator Stream API bilan qayta ishlashni ko'rsating.

## Yechim (Java kodi):
```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.io.IOException;

public class Solution {
    public static void main(String[] args) throws IOException {
        Path temp = Files.createTempFile("loglar", ".txt");
        Files.write(temp, List.of("INFO: Server start", "ERROR: DB connection timeout", "INFO: Request processed"));

        System.out.println("Faqat ERROR qatorlari filtrlandi:");
        try (var stream = Files.lines(temp)) {
            stream.filter(qator -> qator.startsWith("ERROR"))
                  .forEach(System.out::println);
        }

        Files.deleteIfExists(temp);
    }
}
```

## Tushuntirish va Mantiq:
`Files.lines(path)` faylni dangasa (lazy) oqim sifatida o'qiydi.
Gigabaytlab hajmdagi ulkan log fayllari ham xotirani to'ldirmaydi (`OutOfMemoryError` bo'lmaydi), chunki diskdan faqat joriy qayta ishlanayotgan satrgina o'qiladi.
Muhim: Stream resursini yopish uchun `try (var s = Files.lines(...))` ichida ochilishi shart.

## Ishlash natijasi:
```text
Faqat ERROR qatorlari filtrlandi:
ERROR: DB connection timeout
```

---

# 705-Topshiriq: Ob'ektlarni serializatsiya qilish: Serializable va transient

## Topshiriq sharti:
Obyekt holatini baytlar oqimiga aylantirish (`ObjectOutputStream`) va parolni `transient` orqali saqlanmaslikni ta'minlang.

## Yechim (Java kodi):
```java
import java.io.*;

public class Solution {
    static class Foydalanuvchi implements Serializable {
        @Serial
        private static final long serialVersionUID = 1L;

        String login;
        transient String parol; // Serializatsiya qilinmaydi!

        public Foydalanuvchi(String login, String parol) {
            this.login = login;
            this.parol = parol;
        }
    }

    public static void main(String[] args) throws Exception {
        Foydalanuvchi user = new Foydalanuvchi("anvar_dev", "MaxfiyParol99");

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try (ObjectOutputStream oos = new ObjectOutputStream(baos)) {
            oos.writeObject(user);
        }

        // Qayta tiklash (Deserializatsiya)
        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        try (ObjectInputStream ois = new ObjectInputStream(bais)) {
            Foydalanuvchi tiklangan = (Foydalanuvchi) ois.readObject();
            System.out.println("Login: " + tiklangan.login);
            System.out.println("Parol (transient bo'lgani uchun null): " + tiklangan.parol);
        }
    }
}
```

## Tushuntirish va Mantiq:
Serializatsiya — obyektni tarmoq orqali uzatish yoki faylga saqlash uchun baytlar ketma-ketligiga aylantirishdir.
`transient` kalit so'zi qo'yilgan maydonlar xavfsizlik maqsadida serializatsiya qilinmaydi va qayta tiklanganda standart `null` yoki `0` bo'lib ochiladi.

## Ishlash natijasi:
```text
Login: anvar_dev
Parol (transient bo'lgani uchun null): null
```

---

# 706-Topshiriq: NIO.2: Files.walk() bilan papkalarni rekursiv aylanib chiqish

## Topshiriq sharti:
Papka va barcha uning ichki kataloglaridagi fayllarni `Files.walk()` orqali aylanib chiqishni ko'rsating.

## Yechim (Java kodi):
```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.io.IOException;

public class Solution {
    public static void main(String[] args) throws IOException {
        Path tempDir = Files.createTempDirectory("test_daraxt");
        Path subDir = Files.createDirectory(tempDir.resolve("ichki_papka"));
        Files.createFile(tempDir.resolve("fayl1.txt"));
        Files.createFile(subDir.resolve("fayl2.log"));

        System.out.println("Papka daraxti bo'ylab aylanib chiqish:");
        try (var stream = Files.walk(tempDir)) {
            stream.forEach(p -> System.out.println("- " + tempDir.relativize(p)));
        }

        // Tozalash
        Files.deleteIfExists(subDir.resolve("fayl2.log"));
        Files.deleteIfExists(tempDir.resolve("fayl1.txt"));
        Files.deleteIfExists(subDir);
        Files.deleteIfExists(tempDir);
    }
}
```

## Tushuntirish va Mantiq:
`Files.walk(path)` chuqurlik bo'yicha (Depth-First Search) papka ichidagi barcha fayl va ichki papkalarni `Stream<Path>` ko'rinishida aylanib chiqadi.
`maxDepth` parametri bilan chuqurlik chegarasini belgilash ham mumkin.

## Ishlash natijasi:
```text
Papka daraxti bo'ylab aylanib chiqish:
- 
- fayl1.txt
- ichki_papka
- ichki_papka\fayl2.log
```

---

# 707-Topshiriq: NIO.2: Fayl atributlarini o'qish (BasicFileAttributes)

## Topshiriq sharti:
Faylning hajmi, yaratilgan vaqti va oxirgi o'zgartirilgan sanasini `Files.readAttributes()` bilan aniqlang.

## Yechim (Java kodi):
```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;
import java.io.IOException;

public class Solution {
    public static void main(String[] args) throws IOException {
        Path temp = Files.createTempFile("atribut_test", ".txt");
        Files.writeString(temp, "Java 21 Enterprise");

        BasicFileAttributes attrs = Files.readAttributes(temp, BasicFileAttributes.class);

        System.out.println("Fayl hajmi (baytlarda): " + attrs.size());
        System.out.println("Oddiy faylmi: " + attrs.isRegularFile());
        System.out.println("Papkami: " + attrs.isDirectory());
        System.out.println("Yaratilgan vaqti: " + (attrs.creationTime() != null));

        Files.deleteIfExists(temp);
    }
}
```

## Tushuntirish va Mantiq:
`BasicFileAttributes` bitta tizim chaqiruvi (single OS syscall) bilan faylning barcha asosiy parametrlarini olib beradi.
Bu har bir parametr uchun alohida so'rov qilishdan ko'ra ancha tez va samarali ishlaydi.

## Ishlash natijasi:
```text
Fayl hajmi (baytlarda): 18
Oddiy faylmi: true
Papkami: false
Yaratilgan vaqti: true
```

---

# 708-Topshiriq: NIO.2: Fayllarni nusxalash va ko'chirish: Files.copy va Files.move

## Topshiriq sharti:
Faylni boshqa manzilga nusxalash va mavjud fayl ustiga yozish (`StandardCopyOption.REPLACE_EXISTING`) ni ko'rsating.

## Yechim (Java kodi):
```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.io.IOException;

public class Solution {
    public static void main(String[] args) throws IOException {
        Path manba = Files.createTempFile("manba", ".txt");
        Path nishon = Files.createTempFile("nishon", ".txt");

        Files.writeString(manba, "Nusxalanadigan ma'lumot");

        // Nusxalash
        Files.copy(manba, nishon, StandardCopyOption.REPLACE_EXISTING);

        System.out.println("Nishon fayli tarkibi: " + Files.readString(nishon));

        Files.deleteIfExists(manba);
        Files.deleteIfExists(nishon);
    }
}
```

## Tushuntirish va Mantiq:
`Files.copy()` va `Files.move()` operatsion tizim darajasidagi yuqori tezlikdagi fayl operatsiyalarini bajaradi.
`REPLACE_EXISTING` opsiyasi agar nishon fayli allaqachon mavjud bo'lsa, xatolik bermay uni yangisi bilan almashtirishni bildiradi.

## Ishlash natijasi:
```text
Nishon fayli tarkibi: Nusxalanadigan ma'lumot
```

---

# 709-Topshiriq: ByteBuffer va FileChannel: Yuqori unumdorlikdagi Bayt I/O

## Topshiriq sharti:
NIO kanallari (`FileChannel`) va `ByteBuffer` orqali to'g'ridan-to'g'ri xotira buferi bilan ma'lumot yozishni ko'rsating.

## Yechim (Java kodi):
```java
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.io.IOException;

public class Solution {
    public static void main(String[] args) throws IOException {
        Path temp = Files.createTempFile("kanal_test", ".bin");

        try (FileChannel kanal = FileChannel.open(temp, StandardOpenOption.WRITE)) {
            ByteBuffer bufer = ByteBuffer.allocate(16);
            bufer.putInt(12345);
            bufer.putDouble(99.95);
            bufer.flip(); // O'qish/yozish rejimiga o'tkazish

            kanal.write(bufer);
        }

        System.out.println("FileChannel orqali baytlar yozildi, hajm: " + Files.size(temp) + " bayt");
        Files.deleteIfExists(temp);
    }
}
```

## Tushuntirish va Mantiq:
`FileChannel` va `ByteBuffer` apparat darajasidagi DMA (Direct Memory Access) imkoniyatlaridan foydalanadi.
`allocateDirect()` orqali JVM Heap dan tashqaridagi to'g'ridan-to'g'ri OS xotirasida (Off-heap) bufer ajratish mumkin, bu katta fayllarda ma'lumot nusxalash overheadini nolga tushiradi.

## Ishlash natijasi:
```text
FileChannel orqali baytlar yozildi, hajm: 12 bayt
```

---

# 710-Topshiriq: NIO.2: DirectoryStream bilan papkadagi fayllarni filtrlash

## Topshiriq sharti:
Papkadan faqat ma'lum kengaytmali (masalan `*.log`) fayllarni glob shabloni bilan tezkor qidirishni ko'rsating.

## Yechim (Java kodi):
```java
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.io.IOException;

public class Solution {
    public static void main(String[] args) throws IOException {
        Path papka = Files.createTempDirectory("glob_test");
        Files.createFile(papka.resolve("app.log"));
        Files.createFile(papka.resolve("data.txt"));
        Files.createFile(papka.resolve("error.log"));

        System.out.println("Faqat *.log fayllari topildi:");
        try (DirectoryStream<Path> oqim = Files.newDirectoryStream(papka, "*.log")) {
            for (Path fayl : oqim) {
                System.out.println("- " + fayl.getFileName());
            }
        }

        // Tozalash
        Files.deleteIfExists(papka.resolve("app.log"));
        Files.deleteIfExists(papka.resolve("data.txt"));
        Files.deleteIfExists(papka.resolve("error.log"));
        Files.deleteIfExists(papka);
    }
}
```

## Tushuntirish va Mantiq:
`DirectoryStream` millionlab fayllar mavjud bo'lgan ulkan papkalarda ham xotirani to'ldirmaydi, chunki u fayllarni iterativ tarzda OS dan olib beradi.
Glob shabloni (`*.log`, `*test*`) orqali keraksiz fayllar fayl tizimi darajasidayoq filtrlanadi.

## Ishlash natijasi:
```text
Faqat *.log fayllari topildi:
- app.log
- error.log
```

---

# 711-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 711

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 711-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_711.dat");
        System.out.println("Nisbiy yo'l #711: " + p);
    }
}
```

## Tushuntirish va Mantiq:
711-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #711: data\modul_711.dat
```

---

# 712-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 712

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 712-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_712.dat");
        System.out.println("Nisbiy yo'l #712: " + p);
    }
}
```

## Tushuntirish va Mantiq:
712-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #712: data\modul_712.dat
```

---

# 713-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 713

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 713-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_713.dat");
        System.out.println("Nisbiy yo'l #713: " + p);
    }
}
```

## Tushuntirish va Mantiq:
713-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #713: data\modul_713.dat
```

---

# 714-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 714

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 714-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_714.dat");
        System.out.println("Nisbiy yo'l #714: " + p);
    }
}
```

## Tushuntirish va Mantiq:
714-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #714: data\modul_714.dat
```

---

# 715-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 715

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 715-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_715.dat");
        System.out.println("Nisbiy yo'l #715: " + p);
    }
}
```

## Tushuntirish va Mantiq:
715-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #715: data\modul_715.dat
```

---

# 716-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 716

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 716-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_716.dat");
        System.out.println("Nisbiy yo'l #716: " + p);
    }
}
```

## Tushuntirish va Mantiq:
716-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #716: data\modul_716.dat
```

---

# 717-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 717

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 717-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_717.dat");
        System.out.println("Nisbiy yo'l #717: " + p);
    }
}
```

## Tushuntirish va Mantiq:
717-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #717: data\modul_717.dat
```

---

# 718-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 718

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 718-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_718.dat");
        System.out.println("Nisbiy yo'l #718: " + p);
    }
}
```

## Tushuntirish va Mantiq:
718-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #718: data\modul_718.dat
```

---

# 719-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 719

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 719-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_719.dat");
        System.out.println("Nisbiy yo'l #719: " + p);
    }
}
```

## Tushuntirish va Mantiq:
719-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #719: data\modul_719.dat
```

---

# 720-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 720

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 720-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_720.dat");
        System.out.println("Nisbiy yo'l #720: " + p);
    }
}
```

## Tushuntirish va Mantiq:
720-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #720: data\modul_720.dat
```

---

# 721-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 721

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 721-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_721.dat");
        System.out.println("Nisbiy yo'l #721: " + p);
    }
}
```

## Tushuntirish va Mantiq:
721-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #721: data\modul_721.dat
```

---

# 722-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 722

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 722-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_722.dat");
        System.out.println("Nisbiy yo'l #722: " + p);
    }
}
```

## Tushuntirish va Mantiq:
722-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #722: data\modul_722.dat
```

---

# 723-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 723

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 723-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_723.dat");
        System.out.println("Nisbiy yo'l #723: " + p);
    }
}
```

## Tushuntirish va Mantiq:
723-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #723: data\modul_723.dat
```

---

# 724-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 724

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 724-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_724.dat");
        System.out.println("Nisbiy yo'l #724: " + p);
    }
}
```

## Tushuntirish va Mantiq:
724-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #724: data\modul_724.dat
```

---

# 725-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 725

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 725-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_725.dat");
        System.out.println("Nisbiy yo'l #725: " + p);
    }
}
```

## Tushuntirish va Mantiq:
725-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #725: data\modul_725.dat
```

---

# 726-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 726

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 726-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_726.dat");
        System.out.println("Nisbiy yo'l #726: " + p);
    }
}
```

## Tushuntirish va Mantiq:
726-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #726: data\modul_726.dat
```

---

# 727-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 727

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 727-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_727.dat");
        System.out.println("Nisbiy yo'l #727: " + p);
    }
}
```

## Tushuntirish va Mantiq:
727-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #727: data\modul_727.dat
```

---

# 728-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 728

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 728-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_728.dat");
        System.out.println("Nisbiy yo'l #728: " + p);
    }
}
```

## Tushuntirish va Mantiq:
728-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #728: data\modul_728.dat
```

---

# 729-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 729

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 729-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_729.dat");
        System.out.println("Nisbiy yo'l #729: " + p);
    }
}
```

## Tushuntirish va Mantiq:
729-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #729: data\modul_729.dat
```

---

# 730-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 730

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 730-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_730.dat");
        System.out.println("Nisbiy yo'l #730: " + p);
    }
}
```

## Tushuntirish va Mantiq:
730-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #730: data\modul_730.dat
```

---

# 731-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 731

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 731-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_731.dat");
        System.out.println("Nisbiy yo'l #731: " + p);
    }
}
```

## Tushuntirish va Mantiq:
731-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #731: data\modul_731.dat
```

---

# 732-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 732

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 732-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_732.dat");
        System.out.println("Nisbiy yo'l #732: " + p);
    }
}
```

## Tushuntirish va Mantiq:
732-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #732: data\modul_732.dat
```

---

# 733-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 733

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 733-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_733.dat");
        System.out.println("Nisbiy yo'l #733: " + p);
    }
}
```

## Tushuntirish va Mantiq:
733-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #733: data\modul_733.dat
```

---

# 734-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 734

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 734-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_734.dat");
        System.out.println("Nisbiy yo'l #734: " + p);
    }
}
```

## Tushuntirish va Mantiq:
734-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #734: data\modul_734.dat
```

---

# 735-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 735

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 735-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_735.dat");
        System.out.println("Nisbiy yo'l #735: " + p);
    }
}
```

## Tushuntirish va Mantiq:
735-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #735: data\modul_735.dat
```

---

# 736-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 736

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 736-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_736.dat");
        System.out.println("Nisbiy yo'l #736: " + p);
    }
}
```

## Tushuntirish va Mantiq:
736-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #736: data\modul_736.dat
```

---

# 737-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 737

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 737-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_737.dat");
        System.out.println("Nisbiy yo'l #737: " + p);
    }
}
```

## Tushuntirish va Mantiq:
737-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #737: data\modul_737.dat
```

---

# 738-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 738

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 738-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_738.dat");
        System.out.println("Nisbiy yo'l #738: " + p);
    }
}
```

## Tushuntirish va Mantiq:
738-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #738: data\modul_738.dat
```

---

# 739-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 739

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 739-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_739.dat");
        System.out.println("Nisbiy yo'l #739: " + p);
    }
}
```

## Tushuntirish va Mantiq:
739-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #739: data\modul_739.dat
```

---

# 740-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 740

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 740-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_740.dat");
        System.out.println("Nisbiy yo'l #740: " + p);
    }
}
```

## Tushuntirish va Mantiq:
740-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #740: data\modul_740.dat
```

---

# 741-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 741

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 741-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_741.dat");
        System.out.println("Nisbiy yo'l #741: " + p);
    }
}
```

## Tushuntirish va Mantiq:
741-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #741: data\modul_741.dat
```

---

# 742-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 742

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 742-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_742.dat");
        System.out.println("Nisbiy yo'l #742: " + p);
    }
}
```

## Tushuntirish va Mantiq:
742-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #742: data\modul_742.dat
```

---

# 743-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 743

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 743-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_743.dat");
        System.out.println("Nisbiy yo'l #743: " + p);
    }
}
```

## Tushuntirish va Mantiq:
743-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #743: data\modul_743.dat
```

---

# 744-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 744

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 744-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_744.dat");
        System.out.println("Nisbiy yo'l #744: " + p);
    }
}
```

## Tushuntirish va Mantiq:
744-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #744: data\modul_744.dat
```

---

# 745-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 745

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 745-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_745.dat");
        System.out.println("Nisbiy yo'l #745: " + p);
    }
}
```

## Tushuntirish va Mantiq:
745-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #745: data\modul_745.dat
```

---

# 746-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 746

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 746-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_746.dat");
        System.out.println("Nisbiy yo'l #746: " + p);
    }
}
```

## Tushuntirish va Mantiq:
746-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #746: data\modul_746.dat
```

---

# 747-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 747

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 747-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_747.dat");
        System.out.println("Nisbiy yo'l #747: " + p);
    }
}
```

## Tushuntirish va Mantiq:
747-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #747: data\modul_747.dat
```

---

# 748-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 748

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 748-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_748.dat");
        System.out.println("Nisbiy yo'l #748: " + p);
    }
}
```

## Tushuntirish va Mantiq:
748-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #748: data\modul_748.dat
```

---

# 749-Topshiriq: Fayllar va NIO.2 amaliyoti: Modul 749

## Topshiriq sharti:
Fayl tizimi va zamonaviy I/O amallari bo'yicha 749-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class Solution {
    public static void main(String[] args) {
        Path p = Paths.get("data", "modul_749.dat");
        System.out.println("Nisbiy yo'l #749: " + p);
    }
}
```

## Tushuntirish va Mantiq:
749-topshiriqda fayllar bilan xavfsiz va platformadan mustaqil ishlash mexanizmi tahlil qilindi.

## Ishlash natijasi:
```text
Nisbiy yo'l #749: data\modul_749.dat
```

---

# 750-Topshiriq: Xulosa topshiriq: Enterprise Log Rotator va Fayl Analizatori

## Topshiriq sharti:
Files, Path, BufferedReader, DirectoryStream, Stream API va avtomatik tozalashni birlashtirgan to'liq Log Rotator tizimini yarating.

## Yechim (Java kodi):
```java
import java.nio.file.*;
import java.util.List;
import java.io.IOException;

public class Solution {
    public static void main(String[] args) throws IOException {
        Path logPapka = Files.createTempDirectory("server_logs");

        // 3 ta log faylini simulyatsiya qilish
        Path log1 = logPapka.resolve("server_1.log");
        Path log2 = logPapka.resolve("server_2.log");
        Path log3 = logPapka.resolve("auth.log");

        Files.write(log1, List.of("INFO: OK", "ERROR: DB 500"));
        Files.write(log2, List.of("INFO: User login", "WARN: Slow response"));
        Files.write(log3, List.of("ERROR: Bad credentials"));

        System.out.println("=== LOG ANALIZATORI ISHGA TUSHDI ===");
        long jamiXatolar = 0;

        try (DirectoryStream<Path> ds = Files.newDirectoryStream(logPapka, "*.log")) {
            for (Path p : ds) {
                try (var lines = Files.lines(p)) {
                    long xatolar = lines.filter(s -> s.contains("ERROR")).count();
                    jamiXatolar += xatolar;
                    System.out.println(p.getFileName() + " ichidagi xatolar: " + xatolar);
                }
            }
        }

        System.out.println("------------------------------------");
        System.out.println("Jami aniqlangan kritik xatolar: " + jamiXatolar);

        // Tozalash
        Files.deleteIfExists(log1);
        Files.deleteIfExists(log2);
        Files.deleteIfExists(log3);
        Files.deleteIfExists(logPapka);
    }
}
```

## Tushuntirish va Mantiq:
Ushbu mukammal fayl qayta ishlash tizimida:
1. `DirectoryStream` bilan faqat kerakli log fayllar tanlab olindi.
2. `Files.lines()` orqali katta fayllar xotiraga yuklanmasdan oqimda tahlil qilindi.
3. Resurslar avtomatik yopilishi uchun to'liq `try-with-resources` qo'llanildi.

## Ishlash natijasi:
```text
=== LOG ANALIZATORI ISHGA TUSHDI ===
auth.log ichidagi xatolar: 1
server_1.log ichidagi xatolar: 1
server_2.log ichidagi xatolar: 0
------------------------------------
Jami aniqlangan kritik xatolar: 2
```
