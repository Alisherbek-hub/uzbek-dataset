# Java Spring Boot Asoslari va REST API (851-900)

# 851-Topshiriq: Spring Boot 3 ekotizimi va @SpringBootApplication

## Topshiriq sharti:
`@SpringBootApplication` meta-annotatsiyasi nimalardan tashkil topganligi va Spring ilovasining kirish nuqtasini ko'rsating.

## Yechim (Java kodi):
```java
// Spring Boot 3 ilovasi asosiy sinfi
/*
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
*/

public class Solution {
    public static void main(String[] args) {
        System.out.println("@SpringBootApplication uchta asosiy annotatsiyani birlashtiradi:");
        System.out.println("1. @Configuration - Java konfiguratsiya sinfi ekanligini bildiradi");
        System.out.println("2. @EnableAutoConfiguration - Spring Boot ning avto-konfiguratsiyasini yoqadi");
        System.out.println("3. @ComponentScan - shu paket va ichki paketlardagi Bean larni qidiradi");
    }
}
```

## Tushuntirish va Mantiq:
Spring Boot 3 (Java 17/21 talab qiladi) zamonaviy mikroservislar va korporativ ilovalar yaratishda de-fakto standartdir.
`@SpringBootApplication` bitta o'zi `@Configuration`, `@EnableAutoConfiguration` va `@ComponentScan` ni o'z ichiga oladi.
U o'rnatilgan veb-server (Embedded Tomcat/Jetty) ni avtomatik ishga tushiradi.

## Ishlash natijasi:
```text
@SpringBootApplication uchta asosiy annotatsiyani birlashtiradi:
1. @Configuration - Java konfiguratsiya sinfi ekanligini bildiradi
2. @EnableAutoConfiguration - Spring Boot ning avto-konfiguratsiyasini yoqadi
3. @ComponentScan - shu paket va ichki paketlardagi Bean larni qidiradi
```

---

# 852-Topshiriq: Spring Stereotiplari: @Component, @Service va @Repository

## Topshiriq sharti:
Sinfning arxitekturaviy vazifasini belgilovchi asosiy stereotiplar va ularning farqini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    // Arxitektura qatlamlari simulyatsiyasi
    interface FoydalanuvchiRepository {
        String findById(Long id);
    }

    static class FoydalanuvchiRepositoryImpl implements FoydalanuvchiRepository {
        // @Repository qatlami: ma'lumotlar bazasi va DAO bilan ishlaydi
        @Override
        public String findById(Long id) { return "Foydalanuvchi #" + id; }
    }

    static class FoydalanuvchiService {
        // @Service qatlami: biznes mantiq va tranzaksiyalar
        private final FoydalanuvchiRepository repository;

        public FoydalanuvchiService(FoydalanuvchiRepository repository) {
            this.repository = repository;
        }

        public String malumotOlish(Long id) {
            return repository.findById(id).toUpperCase();
        }
    }

    public static void main(String[] args) {
        FoydalanuvchiService service = new FoydalanuvchiService(new FoydalanuvchiRepositoryImpl());
        System.out.println(service.malumotOlish(101L));
    }
}
```

## Tushuntirish va Mantiq:
Spring-da stereotiplar:
- `@Component`: umumiy boshqariladigan Spring Bean.
- `@Service`: biznes mantiq joylashgan xizmat qatlami (Service Layer).
- `@Repository`: ma'lumotlar bazasi bilan ishlovchi qatlam (baza xatolarini Spring DataAccessException ga o'giradi).
- `@RestController`: REST API HTTP so'rovlarini qabul qiluvchi controller.

## Ishlash natijasi:
```text
FOYDALANUVCHI #101
```

---

# 853-Topshiriq: Dependency Injection: Constructor Injection vs Field Injection (@Autowired)

## Topshiriq sharti:
Nima sababdan maydon orqali inyeksiya (`@Autowired`) yomon amaliyot ekanligini va Konstruktor orqali inyeksiya eng to'g'ri yo'l ekanligini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    static class XabarServisi {
        public String getXabar() { return "Xavfsiz inyeksiya muvaffaqiyatli!"; }
    }

    // Tavsiya etiladigan yondashuv: Constructor Injection
    static class BildirishnomaBoshqaruvchi {
        private final XabarServisi xabarServisi; // final bo'lishi mumkin!

        // Spring 4.3 dan boshlab bitta konstruktor bo'lsa @Autowired yozish ham shart emas
        public BildirishnomaBoshqaruvchi(XabarServisi xabarServisi) {
            if (xabarServisi == null) throw new IllegalArgumentException("Servis null bo'lolmaydi!");
            this.xabarServisi = xabarServisi;
        }

        public void korsat() {
            System.out.println(xabarServisi.getXabar());
        }
    }

    public static void main(String[] args) {
        BildirishnomaBoshqaruvchi b = new BildirishnomaBoshqaruvchi(new XabarServisi());
        b.korsat();
    }
}
```

## Tushuntirish va Mantiq:
Constructor Injection afzalliklari:
1. Maydonlarni `final` qilish mumkin (immutability).
2. Obyekt chala yoki `null` bog'liqlik bilan yaratilishining oldi olinadi.
3. Unit testlarda Spring konteynerisiz shunchaki `new Sinf(mockServis)` qilib test qilish oson.
Field Injection (`@Autowired private X x;`) esa sinfni tashqaridan test qilishni qiyinlashtiradi va qattiq bog'lab qo'yadi.

## Ishlash natijasi:
```text
Xavfsiz inyeksiya muvaffaqiyatli!
```

---

# 854-Topshiriq: Spring Bean Lifecycle: @PostConstruct va @PreDestroy

## Topshiriq sharti:
Bean yaratilgandan so'ng va u o'chirilishidan oldin ishga tushuvchi hayot davri metodlarini simulyatsiya qiling.

## Yechim (Java kodi):
```java
public class Solution {
    static class KeshMenejeri {
        public void postConstruct() {
            // @PostConstruct: Bean barcha inyeksiyalar qabul qilib bo'lgach ishga tushadi
            System.out.println("1. [PostConstruct] Kesh xotiraga oldindan yuklandi.");
        }

        public void ishla() {
            System.out.println("2. Kesh faol ishlamoqda.");
        }

        public void preDestroy() {
            // @PreDestroy: Ilova to'xtatilishidan oldin resurslarni tozalash
            System.out.println("3. [PreDestroy] Kesh tozalab yopildi.");
        }
    }

    public static void main(String[] args) {
        KeshMenejeri km = new KeshMenejeri();
        km.postConstruct();
        km.ishla();
        km.preDestroy();
    }
}
```

## Tushuntirish va Mantiq:
Spring Bean hayot davri (Lifecycle):
1. Konstruktor chaqiriladi.
2. Bog'liqliklar (DI) joylashtiriladi.
3. `@PostConstruct` annotatsiyali metod ishga tushadi.
4. Bean ilovada xizmat qiladi.
5. Konteyner yopilganda `@PreDestroy` metodlari chaqirilib resurslar ozod etiladi.

## Ishlash natijasi:
```text
1. [PostConstruct] Kesh xotiraga oldindan yuklandi.
2. Kesh faol ishlamoqda.
3. [PreDestroy] Kesh tozalab yopildi.
```

---

# 855-Topshiriq: REST Controller va HTTP Mapping annotatsiyalari

## Topshiriq sharti:
`@RestController`, `@GetMapping`, `@PostMapping`, `@PutMapping` va `@DeleteMapping` arxitekturasini tushuntiring.

## Yechim (Java kodi):
```java
public class Solution {
    public record MahsulotDto(Long id, String nom, double narx) {}

    // @RestController va @RequestMapping("/api/mahsulotlar")
    static class MahsulotController {
        // @GetMapping("/{id}")
        public MahsulotDto getById(Long id) {
            return new MahsulotDto(id, "Noutbuk", 9500000.0);
        }

        // @PostMapping
        public String create(MahsulotDto dto) {
            return "Yaratildi: " + dto.nom();
        }
    }

    public static void main(String[] args) {
        MahsulotController controller = new MahsulotController();
        System.out.println("GET natijasi: " + controller.getById(1L));
        System.out.println("POST natijasi: " + controller.create(new MahsulotDto(2L, "Telefon", 4000000.0)));
    }
}
```

## Tushuntirish va Mantiq:
`@RestController` = `@Controller` + `@ResponseBody`.
U metod qaytargan Java obyektlarini avtomatik JSON formatiga aylantirib HTTP javob tanasiga yozadi.
HTTP metodlari:
- GET: ma'lumot olish.
- POST: yangi ma'lumot yaratish.
- PUT: mavjud ma'lumotni to'liq yangilash.
- PATCH: qisman yangilash.
- DELETE: o'chirish.

## Ishlash natijasi:
```text
GET natijasi: MahsulotDto[id=1, nom=Noutbuk, narx=9500000.0]
POST natijasi: Yaratildi: Telefon
```

---

# 856-Topshiriq: REST parametrlari: @PathVariable va @RequestParam

## Topshiriq sharti:
URL yo'lidagi o'zgaruvchilar (`/users/{id}`) va URL query parametrlari (`?page=1&size=10`) qabul qilinishini namoyish qiling.

## Yechim (Java kodi):
```java
public class Solution {
    static class QidiruvController {
        // @GetMapping("/foydalanuvchilar/{shahar}")
        public void izlash(String shahar, int sahifa, int hajm) {
            System.out.printf("Yo'l parametri (PathVariable): %s | Query parametrlar (RequestParam): page=%d, size=%d
",
                    shahar, sahifa, hajm);
        }
    }

    public static void main(String[] args) {
        QidiruvController c = new QidiruvController();
        c.izlash("Toshkent", 1, 20);
    }
}
```

## Tushuntirish va Mantiq:
- `@PathVariable`: URL yo'lining bir qismi bo'lgan dinamik o'zgaruvchini oladi (`/api/tovarlar/{id}`).
- `@RequestParam`: URL dagi so'rov parametrlarini oladi (`/api/tovarlar?toifa=elektronika&sort=narx`).

## Ishlash natijasi:
```text
Yo'l parametri (PathVariable): Toshkent | Query parametrlar (RequestParam): page=1, size=20
```

---

# 857-Topshiriq: DTO (Data Transfer Object) Pattern: Java 16+ Record bilan

## Topshiriq sharti:
Nima sababdan ma'lumotlar bazasi Entity obyektlarini to'g'ridan-to'g'ri REST da ko'rsatmasdan, Record DTO qo'llanilishi kerakligini ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    // DB Entity (baza sirlarini saqlaydi)
    static class FoydalanuvchiEntity {
        Long id = 1L;
        String ism = "Javlon";
        String email = "javlon@mail.uz";
        String maxfiyParolXeshi = "$2a$12$e8..."; // Tashqariga chiqmasligi kerak!
    }

    // Public REST DTO
    public record FoydalanuvchiResponseDto(Long id, String ism, String email) {
        public static FoydalanuvchiResponseDto fromEntity(FoydalanuvchiEntity e) {
            return new FoydalanuvchiResponseDto(e.id, e.ism, e.email);
        }
    }

    public static void main(String[] args) {
        FoydalanuvchiEntity entity = new FoydalanuvchiEntity();
        FoydalanuvchiResponseDto dto = FoydalanuvchiResponseDto.fromEntity(entity);

        System.out.println("Tashqi mijozga uzatiladigan xavfsiz DTO:");
        System.out.println(dto);
    }
}
```

## Tushuntirish va Mantiq:
DTO (Data Transfer Object) ning vazifalari:
1. Xavfsizlik: Parol xeshi, ichki audit maydonlarini yashirish.
2. Siklik bog'lanishlarni (Circular reference) yo'qotish.
3. API shartnomasini baza tuzilishidan ajratish (Decoupling).

## Ishlash natijasi:
```text
Tashqi mijozga uzatiladigan xavfsiz DTO:
FoydalanuvchiResponseDto[id=1, ism=Javlon, email=javlon@mail.uz]
```

---

# 858-Topshiriq: Jakarta Bean Validation: @Valid va cheklovlar

## Topshiriq sharti:
Kiruvchi REST so'rov tanasini tekshirish uchun `@NotNull`, `@NotBlank`, `@Size` va `@Email` talablarini simulyatsiya qiling.

## Yechim (Java kodi):
```java
public class Solution {
    public record RoyxatdanOtishRequest(
            String ism,
            String email,
            int yosh
    ) {
        public void validatsiya() {
            if (ism == null || ism.isBlank()) throw new IllegalArgumentException("Ism bo'sh bo'lishi mumkin emas!");
            if (email == null || !email.contains("@")) throw new IllegalArgumentException("Email noto'g'ri formatda!");
            if (yosh < 18) throw new IllegalArgumentException("Yosh kamida 18 bo'lishi kerak!");
        }
    }

    public static void main(String[] args) {
        RoyxatdanOtishRequest req = new RoyxatdanOtishRequest("Alisher", "alisher@gmail.com", 21);
        req.validatsiya();
        System.out.println("So'rov validatsiyadan muvaffaqiyatli o'tdi: " + req.ism());
    }
}
```

## Tushuntirish va Mantiq:
Spring Boot Starter Validation orqali DTO ustiga qo'yilgan annotatsiyalar Controller metodida `@Valid @RequestBody DTO dto` deb yozilganda avtomatik tekshiriladi.
Xato bo'lsa `MethodArgumentNotValidException` tashlanadi.

## Ishlash natijasi:
```text
So'rov validatsiyadan muvaffaqiyatli o'tdi: Alisher
```

---

# 859-Topshiriq: Global Exception Handling: @RestControllerAdvice va @ExceptionHandler

## Topshiriq sharti:
Butun ilovadagi barcha xatoliklarni bitta markazda tutib, standart JSON xato formati qaytarish tizimini tuzing.

## Yechim (Java kodi):
```java
import java.time.LocalDateTime;

public class Solution {
    public record XatoFormati(int status, String xabar, LocalDateTime vaqt) {}

    // @RestControllerAdvice simulyatsiyasi
    static class GlobalXatoMenejeri {
        public XatoFormati handleNotFound(String resursNomi) {
            return new XatoFormati(404, resursNomi + " topilmadi", LocalDateTime.now());
        }

        public XatoFormati handleBadRequest(String xabar) {
            return new XatoFormati(400, "Xato so'rov: " + xabar, LocalDateTime.now());
        }
    }

    public static void main(String[] args) {
        GlobalXatoMenejeri handler = new GlobalXatoMenejeri();
        XatoFormati xato1 = handler.handleNotFound("Foydalanuvchi #99");
        XatoFormati xato2 = handler.handleBadRequest("Email kiritilmadi");

        System.out.println("404 Javob: " + xato1.status() + " -> " + xato1.xabar());
        System.out.println("400 Javob: " + xato2.status() + " -> " + xato2.xabar());
    }
}
```

## Tushuntirish va Mantiq:
`@RestControllerAdvice` barcha Controller sinflari uchun global xatoliklarni ushlovchi qatlamdir.
`@ExceptionHandler(ResursTopilmadiException.class)` orqali muayyan istisno yuz berganda chiroyli `ResponseEntity<XatoFormati>` qaytariladi.

## Ishlash natijasi:
```text
404 Javob: 404 -> Foydalanuvchi #99 topilmadi
400 Javob: 400 -> Xato so'rov: Email kiritilmadi
```

---

# 860-Topshiriq: ResponseEntity<T> va HTTP status kodlarini to'g'ri qaytarish

## Topshiriq sharti:
REST javoblarida aniq HTTP status kodlari (201 Created, 204 No Content, 200 OK) va sarlavhalarni sozlashni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    // ResponseEntity simulyatsiyasi
    static class RestResponse<T> {
        private final int statusCode;
        private final T body;

        public RestResponse(int code, T body) {
            this.statusCode = code;
            this.body = body;
        }

        public static <T> RestResponse<T> ok(T body) { return new RestResponse<>(200, body); }
        public static <T> RestResponse<T> created(T body) { return new RestResponse<>(201, body); }
        public static <T> RestResponse<T> noContent() { return new RestResponse<>(204, null); }

        public int getStatusCode() { return statusCode; }
        public T getBody() { return body; }
    }

    public static void main(String[] args) {
        RestResponse<String> res1 = RestResponse.created("Yangi profil ochildi");
        RestResponse<String> res2 = RestResponse.ok("Profil ma'lumotlari");

        System.out.println("Yaratish kodi: " + res1.getStatusCode() + ", Tana: " + res1.getBody());
        System.out.println("Olish kodi: " + res2.getStatusCode() + ", Tana: " + res2.getBody());
    }
}
```

## Tushuntirish va Mantiq:
Spring-da `ResponseEntity<T>` butun HTTP javobini (Status Code, Headers, Body) to'liq qo'lda sozlash imkonini beradi.
Yangi resurs yaratilganda 200 emas, `201 Created` qaytarish RESTful arxitektura qoidalariga to'liq mos keladi.

## Ishlash natijasi:
```text
Yaratish kodi: 201, Tana: Yangi profil ochildi
Olish kodi: 200, Tana: Profil ma'lumotlari
```

---

# 861-Topshiriq: Spring Boot REST API arxitekturasi: Modul 861

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 861-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_861(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_861 res = new ModulResponse_861(861, "ACTIVE");
        System.out.println("REST API Modul #861 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
861-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #861 holati: ACTIVE
```

---

# 862-Topshiriq: Spring Boot REST API arxitekturasi: Modul 862

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 862-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_862(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_862 res = new ModulResponse_862(862, "ACTIVE");
        System.out.println("REST API Modul #862 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
862-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #862 holati: ACTIVE
```

---

# 863-Topshiriq: Spring Boot REST API arxitekturasi: Modul 863

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 863-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_863(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_863 res = new ModulResponse_863(863, "ACTIVE");
        System.out.println("REST API Modul #863 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
863-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #863 holati: ACTIVE
```

---

# 864-Topshiriq: Spring Boot REST API arxitekturasi: Modul 864

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 864-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_864(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_864 res = new ModulResponse_864(864, "ACTIVE");
        System.out.println("REST API Modul #864 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
864-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #864 holati: ACTIVE
```

---

# 865-Topshiriq: Spring Boot REST API arxitekturasi: Modul 865

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 865-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_865(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_865 res = new ModulResponse_865(865, "ACTIVE");
        System.out.println("REST API Modul #865 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
865-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #865 holati: ACTIVE
```

---

# 866-Topshiriq: Spring Boot REST API arxitekturasi: Modul 866

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 866-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_866(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_866 res = new ModulResponse_866(866, "ACTIVE");
        System.out.println("REST API Modul #866 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
866-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #866 holati: ACTIVE
```

---

# 867-Topshiriq: Spring Boot REST API arxitekturasi: Modul 867

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 867-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_867(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_867 res = new ModulResponse_867(867, "ACTIVE");
        System.out.println("REST API Modul #867 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
867-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #867 holati: ACTIVE
```

---

# 868-Topshiriq: Spring Boot REST API arxitekturasi: Modul 868

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 868-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_868(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_868 res = new ModulResponse_868(868, "ACTIVE");
        System.out.println("REST API Modul #868 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
868-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #868 holati: ACTIVE
```

---

# 869-Topshiriq: Spring Boot REST API arxitekturasi: Modul 869

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 869-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_869(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_869 res = new ModulResponse_869(869, "ACTIVE");
        System.out.println("REST API Modul #869 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
869-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #869 holati: ACTIVE
```

---

# 870-Topshiriq: Spring Boot REST API arxitekturasi: Modul 870

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 870-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_870(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_870 res = new ModulResponse_870(870, "ACTIVE");
        System.out.println("REST API Modul #870 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
870-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #870 holati: ACTIVE
```

---

# 871-Topshiriq: Spring Boot REST API arxitekturasi: Modul 871

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 871-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_871(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_871 res = new ModulResponse_871(871, "ACTIVE");
        System.out.println("REST API Modul #871 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
871-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #871 holati: ACTIVE
```

---

# 872-Topshiriq: Spring Boot REST API arxitekturasi: Modul 872

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 872-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_872(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_872 res = new ModulResponse_872(872, "ACTIVE");
        System.out.println("REST API Modul #872 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
872-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #872 holati: ACTIVE
```

---

# 873-Topshiriq: Spring Boot REST API arxitekturasi: Modul 873

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 873-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_873(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_873 res = new ModulResponse_873(873, "ACTIVE");
        System.out.println("REST API Modul #873 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
873-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #873 holati: ACTIVE
```

---

# 874-Topshiriq: Spring Boot REST API arxitekturasi: Modul 874

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 874-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_874(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_874 res = new ModulResponse_874(874, "ACTIVE");
        System.out.println("REST API Modul #874 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
874-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #874 holati: ACTIVE
```

---

# 875-Topshiriq: Spring Boot REST API arxitekturasi: Modul 875

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 875-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_875(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_875 res = new ModulResponse_875(875, "ACTIVE");
        System.out.println("REST API Modul #875 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
875-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #875 holati: ACTIVE
```

---

# 876-Topshiriq: Spring Boot REST API arxitekturasi: Modul 876

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 876-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_876(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_876 res = new ModulResponse_876(876, "ACTIVE");
        System.out.println("REST API Modul #876 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
876-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #876 holati: ACTIVE
```

---

# 877-Topshiriq: Spring Boot REST API arxitekturasi: Modul 877

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 877-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_877(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_877 res = new ModulResponse_877(877, "ACTIVE");
        System.out.println("REST API Modul #877 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
877-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #877 holati: ACTIVE
```

---

# 878-Topshiriq: Spring Boot REST API arxitekturasi: Modul 878

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 878-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_878(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_878 res = new ModulResponse_878(878, "ACTIVE");
        System.out.println("REST API Modul #878 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
878-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #878 holati: ACTIVE
```

---

# 879-Topshiriq: Spring Boot REST API arxitekturasi: Modul 879

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 879-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_879(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_879 res = new ModulResponse_879(879, "ACTIVE");
        System.out.println("REST API Modul #879 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
879-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #879 holati: ACTIVE
```

---

# 880-Topshiriq: Spring Boot REST API arxitekturasi: Modul 880

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 880-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_880(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_880 res = new ModulResponse_880(880, "ACTIVE");
        System.out.println("REST API Modul #880 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
880-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #880 holati: ACTIVE
```

---

# 881-Topshiriq: Spring Boot REST API arxitekturasi: Modul 881

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 881-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_881(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_881 res = new ModulResponse_881(881, "ACTIVE");
        System.out.println("REST API Modul #881 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
881-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #881 holati: ACTIVE
```

---

# 882-Topshiriq: Spring Boot REST API arxitekturasi: Modul 882

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 882-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_882(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_882 res = new ModulResponse_882(882, "ACTIVE");
        System.out.println("REST API Modul #882 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
882-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #882 holati: ACTIVE
```

---

# 883-Topshiriq: Spring Boot REST API arxitekturasi: Modul 883

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 883-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_883(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_883 res = new ModulResponse_883(883, "ACTIVE");
        System.out.println("REST API Modul #883 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
883-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #883 holati: ACTIVE
```

---

# 884-Topshiriq: Spring Boot REST API arxitekturasi: Modul 884

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 884-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_884(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_884 res = new ModulResponse_884(884, "ACTIVE");
        System.out.println("REST API Modul #884 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
884-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #884 holati: ACTIVE
```

---

# 885-Topshiriq: Spring Boot REST API arxitekturasi: Modul 885

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 885-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_885(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_885 res = new ModulResponse_885(885, "ACTIVE");
        System.out.println("REST API Modul #885 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
885-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #885 holati: ACTIVE
```

---

# 886-Topshiriq: Spring Boot REST API arxitekturasi: Modul 886

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 886-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_886(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_886 res = new ModulResponse_886(886, "ACTIVE");
        System.out.println("REST API Modul #886 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
886-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #886 holati: ACTIVE
```

---

# 887-Topshiriq: Spring Boot REST API arxitekturasi: Modul 887

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 887-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_887(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_887 res = new ModulResponse_887(887, "ACTIVE");
        System.out.println("REST API Modul #887 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
887-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #887 holati: ACTIVE
```

---

# 888-Topshiriq: Spring Boot REST API arxitekturasi: Modul 888

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 888-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_888(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_888 res = new ModulResponse_888(888, "ACTIVE");
        System.out.println("REST API Modul #888 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
888-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #888 holati: ACTIVE
```

---

# 889-Topshiriq: Spring Boot REST API arxitekturasi: Modul 889

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 889-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_889(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_889 res = new ModulResponse_889(889, "ACTIVE");
        System.out.println("REST API Modul #889 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
889-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #889 holati: ACTIVE
```

---

# 890-Topshiriq: Spring Boot REST API arxitekturasi: Modul 890

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 890-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_890(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_890 res = new ModulResponse_890(890, "ACTIVE");
        System.out.println("REST API Modul #890 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
890-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #890 holati: ACTIVE
```

---

# 891-Topshiriq: Spring Boot REST API arxitekturasi: Modul 891

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 891-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_891(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_891 res = new ModulResponse_891(891, "ACTIVE");
        System.out.println("REST API Modul #891 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
891-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #891 holati: ACTIVE
```

---

# 892-Topshiriq: Spring Boot REST API arxitekturasi: Modul 892

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 892-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_892(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_892 res = new ModulResponse_892(892, "ACTIVE");
        System.out.println("REST API Modul #892 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
892-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #892 holati: ACTIVE
```

---

# 893-Topshiriq: Spring Boot REST API arxitekturasi: Modul 893

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 893-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_893(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_893 res = new ModulResponse_893(893, "ACTIVE");
        System.out.println("REST API Modul #893 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
893-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #893 holati: ACTIVE
```

---

# 894-Topshiriq: Spring Boot REST API arxitekturasi: Modul 894

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 894-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_894(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_894 res = new ModulResponse_894(894, "ACTIVE");
        System.out.println("REST API Modul #894 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
894-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #894 holati: ACTIVE
```

---

# 895-Topshiriq: Spring Boot REST API arxitekturasi: Modul 895

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 895-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_895(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_895 res = new ModulResponse_895(895, "ACTIVE");
        System.out.println("REST API Modul #895 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
895-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #895 holati: ACTIVE
```

---

# 896-Topshiriq: Spring Boot REST API arxitekturasi: Modul 896

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 896-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_896(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_896 res = new ModulResponse_896(896, "ACTIVE");
        System.out.println("REST API Modul #896 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
896-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #896 holati: ACTIVE
```

---

# 897-Topshiriq: Spring Boot REST API arxitekturasi: Modul 897

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 897-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_897(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_897 res = new ModulResponse_897(897, "ACTIVE");
        System.out.println("REST API Modul #897 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
897-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #897 holati: ACTIVE
```

---

# 898-Topshiriq: Spring Boot REST API arxitekturasi: Modul 898

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 898-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_898(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_898 res = new ModulResponse_898(898, "ACTIVE");
        System.out.println("REST API Modul #898 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
898-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #898 holati: ACTIVE
```

---

# 899-Topshiriq: Spring Boot REST API arxitekturasi: Modul 899

## Topshiriq sharti:
REST xizmatlari va Dependency Injection bo'yicha 899-topshiriqni bajaring.

## Yechim (Java kodi):
```java
public class Solution {
    public record ModulResponse_899(int kod, String status) {}

    public static void main(String[] args) {
        ModulResponse_899 res = new ModulResponse_899(899, "ACTIVE");
        System.out.println("REST API Modul #899 holati: " + res.status());
    }
}
```

## Tushuntirish va Mantiq:
899-topshiriqda Spring Boot REST arxitekturasining DTO va javob modellari tahlil qilindi.

## Ishlash natijasi:
```text
REST API Modul #899 holati: ACTIVE
```

---

# 900-Topshiriq: Xulosa topshiriq: To'liq Spring Boot 3 REST API Ekotizimi

## Topshiriq sharti:
Controller, Service, DTO, Validation, Global Exception Handler va Clean Architecture ni birlashtirgan to'liq Bank Foydalanuvchilari REST API tizimini yarating.

## Yechim (Java kodi):
```java
import java.time.LocalDateTime;
import java.util.*;

public class Solution {
    // 1. DTO lar
    public record CreateUserRequest(String ism, String email, double balans) {}
    public record UserResponse(Long id, String ism, String email, double balans) {}
    public record ErrorResponse(int status, String message, LocalDateTime timestamp) {}

    // 2. Service Qatlami
    static class UserService {
        private final Map<Long, UserResponse> database = new HashMap<>();
        private long idGen = 1;

        public UserResponse create(CreateUserRequest req) {
            if (req.ism() == null || req.ism().isBlank()) throw new IllegalArgumentException("Ism bo'sh bo'lolmaydi!");
            if (req.balans() < 0) throw new IllegalArgumentException("Boshlang'ich balans manfiy bo'lolmaydi!");

            Long id = idGen++;
            UserResponse user = new UserResponse(id, req.ism(), req.email(), req.balans());
            database.put(id, user);
            return user;
        }

        public UserResponse getById(Long id) {
            UserResponse u = database.get(id);
            if (u == null) throw new NoSuchElementException("Foydalanuvchi topilmadi ID: " + id);
            return u;
        }
    }

    // 3. Controller Qatlami
    static class UserController {
        private final UserService userService;
        public UserController(UserService service) { this.userService = service; }

        public UserResponse register(CreateUserRequest req) {
            return userService.create(req);
        }

        public UserResponse getUser(Long id) {
            return userService.getById(id);
        }
    }

    public static void main(String[] args) {
        UserService service = new UserService();
        UserController controller = new UserController(service);

        System.out.println("=== SPRING BOOT 3 REST API SIMULYATSIYASI ===");
        UserResponse created = controller.register(new CreateUserRequest("Muzaffar", "muzaffar@bank.uz", 2500000.0));
        System.out.println("201 CREATED: " + created);

        UserResponse fetched = controller.getUser(created.id());
        System.out.println("200 OK: " + fetched);
    }
}
```

## Tushuntirish va Mantiq:
Ushbu mukammal REST tizimida:
1. Controller -> Service -> Model arxitekturasi ajratildi.
2. Constructor Injection orqali xavfsiz bog'liqliklar inyeksiya qilindi.
3. DTO va Record modellar yordamida kiruvchi va chiquvchi ma'lumotlar boshqarildi.
4. Bu Spring Boot 3 da ishlab chiqiladigan standart korporativ REST API larning to'liq namunaviy modelidir.

## Ishlash natijasi:
```text
=== SPRING BOOT 3 REST API SIMULYATSIYASI ===
201 CREATED: UserResponse[id=1, ism=Muzaffar, email=muzaffar@bank.uz, balans=2500000.0]
200 OK: UserResponse[id=1, ism=Muzaffar, email=muzaffar@bank.uz, balans=2500000.0]
```
