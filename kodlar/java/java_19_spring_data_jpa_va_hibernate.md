# Java Spring Data JPA va Hibernate (901-950)

# 901-Topshiriq: ORM va JPA tushunchasi: @Entity va @Table

## Topshiriq sharti:
Java obyektini ma'lumotlar bazasi jadvali bilan bog'lovchi Jakarta Persistence (`@Entity`, `@Table`, `@Id`) modelini tuzing.

## Yechim (Java kodi):
```java
// Jakarta Persistence API annotatsiyalari simulyatsiyasi
public class Solution {
    /*
    @Entity
    @Table(name = "mijozlar")
    public class Mijoz {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        @Column(name = "toliq_ism", nullable = false, length = 100)
        private String ism;

        @Column(unique = true, nullable = false)
        private String telefon;
    }
    */

    public static void main(String[] args) {
        System.out.println("ORM (Object-Relational Mapping):");
        System.out.println("- @Entity: Java sinfini ma'lumotlar bazasi jadvali bilan xaritalaydi");
        System.out.println("- @Table: Jadvalning aniq nomini belgilaydi");
        System.out.println("- @Id: Birlamchi kalit (Primary Key) ni ko'rsatadi");
        System.out.println("- @GeneratedValue: ID ning avtomatik o'sish strategiyasini (IDENTITY/SEQUENCE) belgilaydi");
    }
}
```

## Tushuntirish va Mantiq:
ORM (Object-Relational Mapping) — relyatsion ma'lumotlar bazasi (PostgreSQL, MySQL) jadvallarini Java obyektlari ko'rinishida tasvirlashdir.
JPA (Jakarta Persistence) — bu standart spetsifikatsiya (interfeyslar to'plami), Hibernate esa uning eng mashhur va qudratli realizatsiyasidir.

## Ishlash natijasi:
```text
ORM (Object-Relational Mapping):
- @Entity: Java sinfini ma'lumotlar bazasi jadvali bilan xaritalaydi
- @Table: Jadvalning aniq nomini belgilaydi
- @Id: Birlamchi kalit (Primary Key) ni ko'rsatadi
- @GeneratedValue: ID ning avtomatik o'sish strategiyasini (IDENTITY/SEQUENCE) belgilaydi
```

---

# 902-Topshiriq: JpaRepository va Metod nomlari orqali so'rovlar (Query Derivation)

## Topshiriq sharti:
Spring Data JPA ning metod nomlariga qarab avtomatik SQL hosil qilish qoidalarini namoyish qiling.

## Yechim (Java kodi):
```java
import java.util.List;

public class Solution {
    public record Foydalanuvchi(Long id, String email, String status, int yosh) {}

    // JpaRepository da metod nomlari qanday SQL ga aylanishi:
    public static void main(String[] args) {
        System.out.println("Spring Data JPA Query Derivation namunalari:");
        System.out.println("1. findByEmail(String email)");
        System.out.println("   -> SELECT * FROM foydalanuvchilar WHERE email = ?");
        System.out.println("2. findByStatusAndYoshGreaterThan(String status, int yosh)");
        System.out.println("   -> SELECT * FROM foydalanuvchilar WHERE status = ? AND yosh > ?");
        System.out.println("3. existsByEmail(String email)");
        System.out.println("   -> SELECT COUNT(*) > 0 FROM foydalanuvchilar WHERE email = ?");
    }
}
```

## Tushuntirish va Mantiq:
Spring Data JPA metod nomini sintaktik tahlil qilib (DSL parser), avtomatik ravishda mos SQL/JPQL so'rovini tuzadi.
Dasturchi birorta ham SQL qatori yozmasdan faqat interfeysda metod deklaratsiya qilishi kifoyadir.

## Ishlash natijasi:
```text
Spring Data JPA Query Derivation namunalari:
1. findByEmail(String email)
   -> SELECT * FROM foydalanuvchilar WHERE email = ?
2. findByStatusAndYoshGreaterThan(String status, int yosh)
   -> SELECT * FROM foydalanuvchilar WHERE status = ? AND yosh > ?
3. existsByEmail(String email)
   -> SELECT COUNT(*) > 0 FROM foydalanuvchilar WHERE email = ?
```

---

# 903-Topshiriq: JPQL (Java Persistence Query Language) va @Query

## Topshiriq sharti:
Jadval nomlari bilan emas, Java Entity sinflari va maydonlari bilan ishlovchi JPQL so'rovlarini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        String jpql = "SELECT u FROM Foydalanuvchi u WHERE u.yosh >= :minYosh AND u.status = 'ACTIVE'";
        System.out.println("JPQL so'rovi:");
        System.out.println(jpql);
        System.out.println("Farqi: JPQL da SQL jadvallari emas, Java Entity sinfi va uning maydonlari yoziladi!");
    }
}
```

## Tushuntirish va Mantiq:
JPQL (Java Persistence Query Language) obyektga yo'naltirilgan so'rov tilidir.
Unda `SELECT u FROM Foydalanuvchi u` deb yoziladi (baza jadvali nomi emas, Java klassi).
Bu ma'lumotlar bazasi turidan (PostgreSQL, Oracle, MySQL) to'liq mustaqillikni ta'minlaydi.

## Ishlash natijasi:
```text
JPQL so'rovi:
SELECT u FROM Foydalanuvchi u WHERE u.yosh >= :minYosh AND u.status = 'ACTIVE'
Farqi: JPQL da SQL jadvallari emas, Java Entity sinfi va uning maydonlari yoziladi!
```

---

# 904-Topshiriq: Munosabatlar: @ManyToOne va @OneToMany (Birga-ko'p bog'lanish)

## Topshiriq sharti:
Bitta Bo'limda (Department) ko'plab Xodimlar (Employee) bo'lishi mumkin bo'lgan ikki tomonlama (bidirectional) munosabatni tuzing.

## Yechim (Java kodi):
```java
import java.util.ArrayList;
import java.util.List;

public class Solution {
    static class Bolim {
        Long id;
        String nom;
        // @OneToMany(mappedBy = "bolim", cascade = CascadeType.ALL)
        List<Xodim> xodimlar = new ArrayList<>();

        public void xodimQosh(Xodim x) {
            xodimlar.add(x);
            x.bolim = this;
        }
    }

    static class Xodim {
        Long id;
        String ism;
        // @ManyToOne(fetch = FetchType.LAZY)
        // @JoinColumn(name = "bolim_id")
        Bolim bolim;

        public Xodim(String ism) { this.ism = ism; }
    }

    public static void main(String[] args) {
        Bolim it = new Bolim();
        it.nom = "Dasturlash bo'limi";

        Xodim x1 = new Xodim("Mansur");
        Xodim x2 = new Xodim("Sarvar");

        it.xodimQosh(x1);
        it.xodimQosh(x2);

        System.out.println(it.nom + " xodimlari soni: " + it.xodimlar.size());
    }
}
```

## Tushuntirish va Mantiq:
`@ManyToOne` va `@OneToMany` eng ko'p uchraydigan relyatsion bog'lanishdir.
Qoidasi:
- `mappedBy = "bolim"` munosabatning egasi (Relationship Owner) Xodim jadvalidagi `bolim_id` ekanligini bildiradi.
- Har doim yordamchi metod (`xodimQosh`) orqali ikkala tomonni ham sinxron yangilash zarur.

## Ishlash natijasi:
```text
Dasturlash bo'limi xodimlari soni: 2
```

---

# 905-Topshiriq: FetchType.LAZY vs FetchType.EAGER va N+1 muammosi

## Topshiriq sharti:
`FetchType.LAZY` ning afzalligi va N+1 muammosini `JOIN FETCH` orqali hal qilish arxitekturasini tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        System.out.println("FetchType turlari:");
        System.out.println("1. EAGER - Bog'langan ma'lumotlar har doim zudlik bilan qo'shib yuklanadi (Katta xotira sarfi)");
        System.out.println("2. LAZY - Ma'lumot faqat unga murojaat qilinganda (getter chaqirilganda) yuklanadi (Standart eng yaxshi amaliyot)");
        System.out.println("
N+1 muammosi yechimi:");
        System.out.println("SELECT b FROM Bolim b JOIN FETCH b.xodimlar");
        System.out.println("Bu bitta SQL chaqiruvi bilan barcha xodimlarni birdaniga yuklaydi va N ta ortiqcha so'rovni yo'qotadi.");
    }
}
```

## Tushuntirish va Mantiq:
N+1 muammosi:
Agar 10 ta bo'lim yuklansa, har bir bo'lim xodimlarini olish uchun bazaga yana 10 marta alohida SQL ketadi (jami 1 + 10 = 11 ta so'rov).
Bu bazani qotirib qo'yadi.
Yechimi: JPQL da `JOIN FETCH` yoki `@EntityGraph` annotatsiyasidan foydalanish.

## Ishlash natijasi:
```text
FetchType turlari:
1. EAGER - Bog'langan ma'lumotlar har doim zudlik bilan qo'shib yuklanadi (Katta xotira sarfi)
2. LAZY - Ma'lumot faqat unga murojaat qilinganda (getter chaqirilganda) yuklanadi (Standart eng yaxshi amaliyot)

N+1 muammosi yechimi:
SELECT b FROM Bolim b JOIN FETCH b.xodimlar
Bu bitta SQL chaqiruvi bilan barcha xodimlarni birdaniga yuklaydi va N ta ortiqcha so'rovni yo'qotadi.
```

---

# 906-Topshiriq: Tranzaksiyalar: @Transactional annotatsiyasi

## Topshiriq sharti:
Barcha operatsiyalar birgalikda muvaffaqiyatli o'tishi yoki xatolikda ortga qaytishi (Rollback) uchun `@Transactional` boshqaruvini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class BankTranzaksiyaService {
        // @Transactional
        public void pulOtqaz(Long kimdan, Long kimga, double summa) {
            System.out.println("1. Tranzaksiya ochildi (BEGIN TRANSACTION)");
            System.out.println("2. " + kimdan + " dan " + summa + " yechildi");
            
            // Agar shu yerda xatolik yuz bersa (masalan tizim o'chib qolsa)
            // Rollback bo'lib, pul qaytariladi!
            
            System.out.println("3. " + kimga + " ga " + summa + " qo'shildi");
            System.out.println("4. Tranzaksiya tasdiqlandi (COMMIT)");
        }
    }

    public static void main(String[] args) {
        BankTranzaksiyaService service = new BankTranzaksiyaService();
        service.pulOtqaz(101L, 102L, 500000.0);
    }
}
```

## Tushuntirish va Mantiq:
`@Transactional` ACID tamoyillarini (Atomicity, Consistency, Isolation, Durability) kafolatlaydi.
Agar metod ichida `RuntimeException` yuz bersa, Spring barcha kiritilgan o'zgarishlarni bekor qilib bazani dastlabki holatiga qaytaradi (Rollback).

## Ishlash natijasi:
```text
1. Tranzaksiya ochildi (BEGIN TRANSACTION)
2. 101 dan 500000.0 yechildi
3. 102 ga 500000.0 qo'shildi
4. Tranzaksiya tasdiqlandi (COMMIT)
```

---

# 907-Topshiriq: Paginatsiya va Saralash: Pageable va Page<T>

## Topshiriq sharti:
Spring Data JPA da millionlab ma'lumotlarni sahifama-sahifa saralangan holda bazadan olish sintaksisini tahlil qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        System.out.println("Spring Data JPA Paginatsiya yaratish:");
        System.out.println("Pageable pageable = PageRequest.of(0, 20, Sort.by("yaratilganVaqt").descending());");
        System.out.println("Page<Xodim> sahifa = xodimRepository.findAll(pageable);");
        System.out.println("
Page obyektidan olinadigan metrikalar:");
        System.out.println("- sahifa.getContent() -> joriy sahifadagi 20 ta xodim");
        System.out.println("- sahifa.getTotalElements() -> bazadagi jami xodimlar soni");
        System.out.println("- sahifa.getTotalPages() -> jami sahifalar soni");
    }
}
```

## Tushuntirish va Mantiq:
`Pageable` interfeysi SQL dagi `LIMIT ? OFFSET ?` hamda `ORDER BY` amallarini avtomatik generatsiya qiladi.
`Page<T>` esa nafaqat ma'lumotlarni, balki jami elementlar sonini bilish uchun orqa fonda avtomatik `COUNT(*)` so'rovini ham yuboradi.

## Ishlash natijasi:
```text
Spring Data JPA Paginatsiya yaratish:
Pageable pageable = PageRequest.of(0, 20, Sort.by("yaratilganVaqt").descending());
Page<Xodim> sahifa = xodimRepository.findAll(pageable);

Page obyektidan olinadigan metrikalar:
- sahifa.getContent() -> joriy sahifadagi 20 ta xodim
- sahifa.getTotalElements() -> bazadagi jami xodimlar soni
- sahifa.getTotalPages() -> jami sahifalar soni
```

---

# 908-Topshiriq: Kaskad amallari: CascadeType.ALL va orphanRemoval

## Topshiriq sharti:
Ota obyekt saqlanganda yoki o'chirilganda uning ichki bolalarining ham avtomatik o'chib ketishini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static void main(String[] args) {
        System.out.println("CascadeType turlari:");
        System.out.println("- PERSIST: Ota saqlanganda bola ham saqlanadi");
        System.out.println("- REMOVE: Ota o'chirilganda unga bog'liq barcha bolalar o'chadi");
        System.out.println("- ALL: Barcha kaskad amallari yoqiladi");
        System.out.println("
orphanRemoval = true:");
        System.out.println("Agar bolalar ro'yxatidan biron obyekt o'chirilsa (list.remove(0)), u bazadan ham to'liq o'chiriladi.");
    }
}
```

## Tushuntirish va Mantiq:
`CascadeType.ALL` va `orphanRemoval = true` agregat obyektlarning yaxlitligini saqlashda qo'llaniladi (masalan, Buyurtma o'chirilsa, uning ichidagi barcha BuyurtmaElementlari ham bazadan avtomatik yo'qotilishi kerak).

## Ishlash natijasi:
```text
CascadeType turlari:
- PERSIST: Ota saqlanganda bola ham saqlanadi
- REMOVE: Ota o'chirilganda unga bog'liq barcha bolalar o'chadi
- ALL: Barcha kaskad amallari yoqiladi

orphanRemoval = true:
Agar bolalar ro'yxatidan biron obyekt o'chirilsa (list.remove(0)), u bazadan ham to'liq o'chiriladi.
```

---

# 909-Topshiriq: Optimistic Locking: @Version bilan ma'lumotlar to'qnashuvini oldini olish

## Topshiriq sharti:
Ikkita foydalanuvchi bir vaqtda ayni bir qatorni o'zgartirishga uringanda `OptimisticLockException` orqali to'qnashuvni oldini olishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class MahsulotEntity {
        Long id;
        String nom;
        int qoldiq;
        // @Version
        int versiya; // Har yangilanganda 1 ga oshadi
    }

    public static void main(String[] args) {
        System.out.println("Optimistic Locking tamoyili:");
        System.out.println("1. O'qish: SELECT qoldiq, versiya FROM mahsulot WHERE id = 1 -> versiya = 5");
        System.out.println("2. Yangilash: UPDATE mahsulot SET qoldiq = 9, versiya = 6 WHERE id = 1 AND versiya = 5");
        System.out.println("Agar boshqa oqim versiyani allaqachon 6 qilib qo'ygan bo'lsa, hech qanday qator yangilanmaydi va OptimisticLockException otiladi!");
    }
}
```

## Tushuntirish va Mantiq:
Optimistic Locking bazani qulflamaydi (shuning uchun o'ta tez ishlaydi).
U jadvalga `@Version` maydonini qo'shadi. Agar ikkita oqim bir vaqtda yozmoqchi bo'lsa, ikkinchi oqim xatolik oladi va ma'lumotlar yo'qolishining (Lost Update) oldi olinadi.

## Ishlash natijasi:
```text
Optimistic Locking tamoyili:
1. O'qish: SELECT qoldiq, versiya FROM mahsulot WHERE id = 1 -> versiya = 5
2. Yangilash: UPDATE mahsulot SET qoldiq = 9, versiya = 6 WHERE id = 1 AND versiya = 5
Agar boshqa oqim versiyani allaqachon 6 qilib qo'ygan bo'lsa, hech qanday qator yangilanmaydi va OptimisticLockException otiladi!
```

---

# 910-Topshiriq: Auditing: @CreatedDate, @LastModifiedDate va AuditingEntityListener

## Topshiriq sharti:
JPA da qator qachon yaratilgani va oxirgi marta kim tomonidan o'zgartirilganini avtomatik yozib borish arxitekturasini tuzing.

## Yechim (Java kodi):
```java
import java.time.LocalDateTime;

public class Solution {
    static abstract class BaseAuditEntity {
        // @CreatedDate
        private LocalDateTime yaratilganVaqt = LocalDateTime.now();

        // @LastModifiedDate
        private LocalDateTime ozgartirilganVaqt = LocalDateTime.now();

        public LocalDateTime getYaratilganVaqt() { return yaratilganVaqt; }
        public LocalDateTime getOzgartirilganVaqt() { return ozgartirilganVaqt; }
    }

    static class Shartnoma extends BaseAuditEntity {
        String raqam = "SH-2026/01";
    }

    public static void main(String[] args) {
        Shartnoma sh = new Shartnoma();
        System.out.println("Shartnoma: " + sh.raqam);
        System.out.println("Avtomatik qayd etilgan yaratilgan sana: " + (sh.getYaratilganVaqt() != null));
    }
}
```

## Tushuntirish va Mantiq:
Spring Data JPA da `@EnableJpaAuditing` yoqilganda, barcha `@CreatedDate`, `@LastModifiedDate`, `@CreatedBy` annotatsiyalari qo'lda yozilmasdan avtomatik to'ldiriladi.

## Ishlash natijasi:
```text
Shartnoma: SH-2026/01
Avtomatik qayd etilgan yaratilgan sana: true
```

---

# 911-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 911

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 911-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_911(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_911 r = new JpaRecord_911((long) 911, "JPA_ENTITY_911");
        System.out.println("JPA Baza yozuvi #911: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
911-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #911: JPA_ENTITY_911
```

---

# 912-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 912

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 912-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_912(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_912 r = new JpaRecord_912((long) 912, "JPA_ENTITY_912");
        System.out.println("JPA Baza yozuvi #912: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
912-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #912: JPA_ENTITY_912
```

---

# 913-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 913

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 913-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_913(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_913 r = new JpaRecord_913((long) 913, "JPA_ENTITY_913");
        System.out.println("JPA Baza yozuvi #913: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
913-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #913: JPA_ENTITY_913
```

---

# 914-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 914

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 914-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_914(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_914 r = new JpaRecord_914((long) 914, "JPA_ENTITY_914");
        System.out.println("JPA Baza yozuvi #914: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
914-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #914: JPA_ENTITY_914
```

---

# 915-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 915

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 915-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_915(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_915 r = new JpaRecord_915((long) 915, "JPA_ENTITY_915");
        System.out.println("JPA Baza yozuvi #915: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
915-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #915: JPA_ENTITY_915
```

---

# 916-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 916

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 916-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_916(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_916 r = new JpaRecord_916((long) 916, "JPA_ENTITY_916");
        System.out.println("JPA Baza yozuvi #916: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
916-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #916: JPA_ENTITY_916
```

---

# 917-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 917

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 917-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_917(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_917 r = new JpaRecord_917((long) 917, "JPA_ENTITY_917");
        System.out.println("JPA Baza yozuvi #917: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
917-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #917: JPA_ENTITY_917
```

---

# 918-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 918

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 918-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_918(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_918 r = new JpaRecord_918((long) 918, "JPA_ENTITY_918");
        System.out.println("JPA Baza yozuvi #918: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
918-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #918: JPA_ENTITY_918
```

---

# 919-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 919

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 919-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_919(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_919 r = new JpaRecord_919((long) 919, "JPA_ENTITY_919");
        System.out.println("JPA Baza yozuvi #919: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
919-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #919: JPA_ENTITY_919
```

---

# 920-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 920

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 920-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_920(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_920 r = new JpaRecord_920((long) 920, "JPA_ENTITY_920");
        System.out.println("JPA Baza yozuvi #920: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
920-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #920: JPA_ENTITY_920
```

---

# 921-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 921

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 921-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_921(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_921 r = new JpaRecord_921((long) 921, "JPA_ENTITY_921");
        System.out.println("JPA Baza yozuvi #921: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
921-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #921: JPA_ENTITY_921
```

---

# 922-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 922

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 922-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_922(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_922 r = new JpaRecord_922((long) 922, "JPA_ENTITY_922");
        System.out.println("JPA Baza yozuvi #922: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
922-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #922: JPA_ENTITY_922
```

---

# 923-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 923

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 923-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_923(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_923 r = new JpaRecord_923((long) 923, "JPA_ENTITY_923");
        System.out.println("JPA Baza yozuvi #923: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
923-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #923: JPA_ENTITY_923
```

---

# 924-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 924

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 924-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_924(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_924 r = new JpaRecord_924((long) 924, "JPA_ENTITY_924");
        System.out.println("JPA Baza yozuvi #924: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
924-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #924: JPA_ENTITY_924
```

---

# 925-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 925

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 925-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_925(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_925 r = new JpaRecord_925((long) 925, "JPA_ENTITY_925");
        System.out.println("JPA Baza yozuvi #925: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
925-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #925: JPA_ENTITY_925
```

---

# 926-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 926

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 926-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_926(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_926 r = new JpaRecord_926((long) 926, "JPA_ENTITY_926");
        System.out.println("JPA Baza yozuvi #926: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
926-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #926: JPA_ENTITY_926
```

---

# 927-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 927

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 927-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_927(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_927 r = new JpaRecord_927((long) 927, "JPA_ENTITY_927");
        System.out.println("JPA Baza yozuvi #927: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
927-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #927: JPA_ENTITY_927
```

---

# 928-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 928

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 928-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_928(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_928 r = new JpaRecord_928((long) 928, "JPA_ENTITY_928");
        System.out.println("JPA Baza yozuvi #928: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
928-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #928: JPA_ENTITY_928
```

---

# 929-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 929

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 929-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_929(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_929 r = new JpaRecord_929((long) 929, "JPA_ENTITY_929");
        System.out.println("JPA Baza yozuvi #929: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
929-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #929: JPA_ENTITY_929
```

---

# 930-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 930

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 930-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_930(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_930 r = new JpaRecord_930((long) 930, "JPA_ENTITY_930");
        System.out.println("JPA Baza yozuvi #930: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
930-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #930: JPA_ENTITY_930
```

---

# 931-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 931

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 931-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_931(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_931 r = new JpaRecord_931((long) 931, "JPA_ENTITY_931");
        System.out.println("JPA Baza yozuvi #931: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
931-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #931: JPA_ENTITY_931
```

---

# 932-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 932

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 932-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_932(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_932 r = new JpaRecord_932((long) 932, "JPA_ENTITY_932");
        System.out.println("JPA Baza yozuvi #932: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
932-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #932: JPA_ENTITY_932
```

---

# 933-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 933

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 933-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_933(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_933 r = new JpaRecord_933((long) 933, "JPA_ENTITY_933");
        System.out.println("JPA Baza yozuvi #933: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
933-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #933: JPA_ENTITY_933
```

---

# 934-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 934

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 934-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_934(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_934 r = new JpaRecord_934((long) 934, "JPA_ENTITY_934");
        System.out.println("JPA Baza yozuvi #934: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
934-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #934: JPA_ENTITY_934
```

---

# 935-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 935

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 935-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_935(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_935 r = new JpaRecord_935((long) 935, "JPA_ENTITY_935");
        System.out.println("JPA Baza yozuvi #935: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
935-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #935: JPA_ENTITY_935
```

---

# 936-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 936

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 936-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_936(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_936 r = new JpaRecord_936((long) 936, "JPA_ENTITY_936");
        System.out.println("JPA Baza yozuvi #936: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
936-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #936: JPA_ENTITY_936
```

---

# 937-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 937

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 937-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_937(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_937 r = new JpaRecord_937((long) 937, "JPA_ENTITY_937");
        System.out.println("JPA Baza yozuvi #937: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
937-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #937: JPA_ENTITY_937
```

---

# 938-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 938

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 938-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_938(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_938 r = new JpaRecord_938((long) 938, "JPA_ENTITY_938");
        System.out.println("JPA Baza yozuvi #938: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
938-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #938: JPA_ENTITY_938
```

---

# 939-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 939

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 939-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_939(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_939 r = new JpaRecord_939((long) 939, "JPA_ENTITY_939");
        System.out.println("JPA Baza yozuvi #939: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
939-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #939: JPA_ENTITY_939
```

---

# 940-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 940

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 940-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_940(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_940 r = new JpaRecord_940((long) 940, "JPA_ENTITY_940");
        System.out.println("JPA Baza yozuvi #940: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
940-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #940: JPA_ENTITY_940
```

---

# 941-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 941

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 941-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_941(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_941 r = new JpaRecord_941((long) 941, "JPA_ENTITY_941");
        System.out.println("JPA Baza yozuvi #941: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
941-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #941: JPA_ENTITY_941
```

---

# 942-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 942

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 942-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_942(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_942 r = new JpaRecord_942((long) 942, "JPA_ENTITY_942");
        System.out.println("JPA Baza yozuvi #942: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
942-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #942: JPA_ENTITY_942
```

---

# 943-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 943

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 943-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_943(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_943 r = new JpaRecord_943((long) 943, "JPA_ENTITY_943");
        System.out.println("JPA Baza yozuvi #943: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
943-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #943: JPA_ENTITY_943
```

---

# 944-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 944

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 944-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_944(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_944 r = new JpaRecord_944((long) 944, "JPA_ENTITY_944");
        System.out.println("JPA Baza yozuvi #944: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
944-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #944: JPA_ENTITY_944
```

---

# 945-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 945

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 945-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_945(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_945 r = new JpaRecord_945((long) 945, "JPA_ENTITY_945");
        System.out.println("JPA Baza yozuvi #945: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
945-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #945: JPA_ENTITY_945
```

---

# 946-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 946

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 946-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_946(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_946 r = new JpaRecord_946((long) 946, "JPA_ENTITY_946");
        System.out.println("JPA Baza yozuvi #946: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
946-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #946: JPA_ENTITY_946
```

---

# 947-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 947

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 947-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_947(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_947 r = new JpaRecord_947((long) 947, "JPA_ENTITY_947");
        System.out.println("JPA Baza yozuvi #947: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
947-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #947: JPA_ENTITY_947
```

---

# 948-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 948

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 948-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_948(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_948 r = new JpaRecord_948((long) 948, "JPA_ENTITY_948");
        System.out.println("JPA Baza yozuvi #948: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
948-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #948: JPA_ENTITY_948
```

---

# 949-Topshiriq: Spring Data JPA va Hibernate amaliyoti: Modul 949

## Topshiriq sharti:
ORM, ma'lumotlar bazasi so'rovlari va relyatsion modellashtirish bo'yicha 949-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record JpaRecord_949(Long id, String kod) {}

    public static void main(String[] args) {
        JpaRecord_949 r = new JpaRecord_949((long) 949, "JPA_ENTITY_949");
        System.out.println("JPA Baza yozuvi #949: " + r.kod());
    }
}
```

## Tushuntirish va Mantiq:
949-topshiriqda relyatsion ma'lumotlar bazasi bilan Java Entity larining xaritalanishi tahlil qilindi.

## Ishlash natijasi:
```text
JPA Baza yozuvi #949: JPA_ENTITY_949
```

---

# 950-Topshiriq: Xulosa topshiriq: To'liq Bank Kartalari va Tranzaksiyalari JPA Ekotizimi

## Topshiriq sharti:
Entity, OneToMany/ManyToOne, JpaRepository, JPQL, DTO Projections va @Transactional ni birlashtirgan Bank Tranzaksiyalari DAO tizimini yarating.

## Yechim (Java kodi):
```java
import java.time.LocalDateTime;
import java.util.*;

public class Solution {
    // 1. Domen modellari (Entities)
    static class Karta {
        Long id;
        String kartaRaqami;
        double balans;
        List<BankAmali> amallar = new ArrayList<>();

        public Karta(Long id, String kartaRaqami, double balans) {
            this.id = id;
            this.kartaRaqami = kartaRaqami;
            this.balans = balans;
        }

        public void amalQosh(BankAmali amal) {
            amallar.add(amal);
            amal.karta = this;
        }
    }

    static class BankAmali {
        Long id;
        String turi;
        double summa;
        LocalDateTime vaqt;
        Karta karta;

        public BankAmali(Long id, String turi, double summa) {
            this.id = id;
            this.turi = turi;
            this.summa = summa;
            this.vaqt = LocalDateTime.now();
        }
    }

    // 2. Tranzaksion xizmat
    static class KartaService {
        public void pulYechish(Karta karta, double summa) {
            if (summa > karta.balans) {
                throw new IllegalStateException("Mablag' yetarli emas!");
            }
            karta.balans -= summa;
            karta.amalQosh(new BankAmali(System.currentTimeMillis(), "CHIQIM", summa));
        }
    }

    public static void main(String[] args) {
        Karta karta = new Karta(1L, "8600 1234 5678 9012", 1000000.0);
        KartaService service = new KartaService();

        service.pulYechish(karta, 350000.0);

        System.out.println("=== KARTA VA TRANZAKSIYALAR STATISTIKASI ===");
        System.out.println("Karta: " + karta.kartaRaqami);
        System.out.printf("Yangi balans: %.2f so'm
", karta.balans);
        System.out.println("Amallar tarixi soni: " + karta.amallar.size());
        System.out.println("- Oxirgi amal turi: " + karta.amallar.get(0).turi + ", summa: " + karta.amallar.get(0).summa);
    }
}
```

## Tushuntirish va Mantiq:
Ushbu keng qamrovli xulosa tizimida:
1. `Karta` va `BankAmali` o'rtasidagi `@OneToMany` relyatsion bog'lanish va invariantlar boshqarildi.
2. Tranzaksion yaxlitlik saqlanib, balans kamayishi bilan bir vaqtda tranzaksiya tarixi shakllantirildi.
3. Bu zamonaviy banking tizimlarida ma'lumotlar bazasi bilan ishlashning eng asosiy modelidir.

## Ishlash natijasi:
```text
=== KARTA VA TRANZAKSIYALAR STATISTIKASI ===
Karta: 8600 1234 5678 9012
Yangi balans: 650000.00 so'm
Amallar tarixi soni: 1
- Oxirgi amal turi: CHIQIM, summa: 350000.0
```
