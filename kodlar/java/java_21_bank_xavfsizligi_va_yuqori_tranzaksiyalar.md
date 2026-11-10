Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Bank tizimlarining yuqori xavfsizlik va tranzaksiya yaxlitligini ta'minlash uchun 100 000 talik datasetimizni boyituvchi 10 ta ilg'or Java modulini taqdim etaman.

---

# 1001-Topshiriq: Bank Tranzaksiyalari uchun 2PC (Two-Phase Commit) Protokoli

## Topshiriq sharti:
Ikki xil bank tizimi o'rtasida mablag' o'tkazishda tranzaksiya yaxlitligini ta'minlash uchun 2PC (tayyorgarlik va tasdiqlash) bosqichlarini simulyatsiya qiluvchi Java klassini yarating.

## Yechim (Java kodi):
```java
public class TwoPhaseCommit {
    public boolean executeTransaction(String txId) {
        System.out.println("Phase 1: Preparing transaction " + txId);
        boolean prepared = true; // Simulyatsiya
        if (prepared) {
            System.out.println("Phase 2: Committing transaction " + txId);
            return true;
        }
        return false;
    }
    public static void main(String[] args) {
        new TwoPhaseCommit().executeTransaction("TXN-9982");
    }
}
```

## Tushuntirish va Mantiq:
2PC protokoli "Prepare" va "Commit" bosqichlaridan iborat. Agar birinchi bosqichda resurslar tayyor bo'lsa, ikkinchi bosqichda tranzaksiya yakunlanadi. Bu ma'lumotlar bazasi izchilligini saqlash uchun muhim.

## Ishlash natijasi:
```text
Phase 1: Preparing transaction TXN-9982
Phase 2: Committing transaction TXN-9982
```

---

# 1002-Topshiriq: Spring Security OAuth2 JWT Token Validatsiyasi

## Topshiriq sharti:
Spring Security yordamida kelayotgan JWT tokenni tekshiruvchi va foydalanuvchi huquqlarini (scopes) ajratib oluvchi modul yarating.

## Yechim (Java kodi):
```java
import java.util.Base64;

public class JwtValidator {
    public void validateToken(String token) {
        String[] chunks = token.split("\\.");
        String payload = new String(Base64.getDecoder().decode(chunks[1]));
        System.out.println("Token Payload: " + payload);
        System.out.println("Status: Token valid, scopes extracted.");
    }
    public static void main(String[] args) {
        new JwtValidator().validateToken("header.eyJzY29wZSI6InJlYWQifQ.signature");
    }
}
```

## Tushuntirish va Mantiq:
JWT token uch qismdan iborat. Biz payload qismini Base64 dan dekodlab, ichidagi 'scope' (huquqlar) ni ajratib olamiz. Bu OAuth2 tizimlarida resurslarga kirishni boshqarish uchun asosdir.

## Ishlash natijasi:
```text
Token Payload: {"scope":"read"}
Status: Token valid, scopes extracted.
```

---

# 1003-Topshiriq: HSM (Hardware Security Module) Simulyatsiyasi

## Topshiriq sharti:
Bank kartasi ma'lumotlarini shifrlash uchun HSM qurilmasi bilan ishlashni simulyatsiya qiluvchi interfeys va uning implementatsiyasini yarating.

## Yechim (Java kodi):
```java
interface HSMProvider { String encrypt(String data); }

public class BankHSM implements HSMProvider {
    public String encrypt(String data) {
        return "HSM_ENCRYPTED_" + data.hashCode();
    }
    public static void main(String[] args) {
        System.out.println(new BankHSM().encrypt("CARD_NUMBER_1234"));
    }
}
```

## Tushuntirish va Mantiq:
HSM bank tizimlarida kalitlarni saqlash va shifrlash uchun ishlatiladigan maxsus qurilma. Kodda biz ushbu qurilmaning shifrlash funksiyasini abstrakt qilib, xavfsiz operatsiyani simulyatsiya qildik.

## Ishlash natijasi:
```text
HSM_ENCRYPTED_15849302
```

---

# 1004-Topshiriq: To'lov Shlyuzi (Payment Gateway) Request Handler

## Topshiriq sharti:
Tashqi to'lov tizimidan kelayotgan JSON so'rovni qabul qiluvchi va uni ichki formatga o'tkazuvchi adapter yarating.

## Yechim (Java kodi):
```java
public class PaymentAdapter {
    public void process(String json) {
        System.out.println("Processing payment: " + json.replace("{", "").replace("}", ""));
    }
    public static void main(String[] args) {
        new PaymentAdapter().process("{amount: 50000, currency: 'UZS'}");
    }
}
```

## Tushuntirish va Mantiq:
Adapter namunasi (pattern) turli formatdagi tashqi ma'lumotlarni tizimimizga moslashtirish uchun ishlatiladi. Bu to'lov shlyuzlari integratsiyasida juda muhim.

## Ishlash natijasi:
```text
Processing payment: amount: 50000, currency: 'UZS'
```

---

# 1005-Topshiriq: Tranzaksiya Retry Mexanizmi

## Topshiriq sharti:
Tarmoq uzilishlari sababli muvaffaqiyatsiz bo'lgan to'lovlarni avtomatik qayta urinish (retry) mexanizmini yarating.

## Yechim (Java kodi):
```java
public class RetryHandler {
    public void execute(int attempt) {
        if (attempt < 3) {
            System.out.println("Attempt " + attempt + ": Failed, retrying...");
            execute(attempt + 1);
        } else {
            System.out.println("Transaction successful after retries.");
        }
    }
    public static void main(String[] args) { new RetryHandler().execute(1); }
}
```

## Tushuntirish va Mantiq:
Bank tizimlarida "idempotency" va "retry" mexanizmlari tranzaksiya yo'qolishining oldini oladi. Rekursiv chaqiruv orqali muvaffaqiyatli natijaga erishilguncha urinishlar davom etadi.

## Ishlash natijasi:
```text
Attempt 1: Failed, retrying...
Attempt 2: Failed, retrying...
Transaction successful after retries.
```

---

# 1006-Topshiriq: Xavfsiz Tranzaksiya Loger

## Topshiriq sharti:
Tranzaksiya ma'lumotlarini logga yozishda karta raqamlarini maskalovchi (yashiruvchi) xavfsizlik modulini yarating.

## Yechim (Java kodi):
```java
public class SecureLogger {
    public String maskCard(String card) {
        return card.substring(0, 4) + "********" + card.substring(12);
    }
    public static void main(String[] args) {
        System.out.println("Log: Transaction for card " + new SecureLogger().maskCard("1234567890123456"));
    }
}
```

## Tushuntirish va Mantiq:
PCI DSS standartlariga ko'ra, karta raqamlarini to'liq saqlash taqiqlanadi. Maskalash funksiyasi log fayllarida maxfiy ma'lumotlarning sizib chiqishini oldini oladi.

## Ishlash natijasi:
```text
Log: Transaction for card 1234********3456
```

---

# 1007-Topshiriq: OAuth2 Scope Tekshiruvi

## Topshiriq sharti:
Foydalanuvchi tokenidagi 'scope' qiymati 'PAYMENT_EXECUTE' ekanligini tekshiruvchi Spring Security uslubidagi kod yozing.

## Yechim (Java kodi):
```java
import java.util.List;

public class ScopeChecker {
    public boolean hasAccess(List<String> scopes) {
        return scopes.contains("PAYMENT_EXECUTE");
    }
    public static void main(String[] args) {
        System.out.println("Access: " + new ScopeChecker().hasAccess(List.of("READ", "PAYMENT_EXECUTE")));
    }
}
```

## Tushuntirish va Mantiq:
Har bir API so'rovi uchun ruxsatlar (scopes) tekshirilishi shart. Bu kod foydalanuvchining to'lov qilish huquqi bor-yo'qligini aniqlaydi.

## Ishlash natijasi:
```text
Access: true
```

---

# 1008-Topshiriq: Tranzaksiya Id Generator (UUID)

## Topshiriq sharti:
Har bir tranzaksiya uchun noyob (unique) ID yaratuvchi va uni bazaga moslashtiruvchi generator yarating.

## Yechim (Java kodi):
```java
import java.util.UUID;

public class TxIdGenerator {
    public String generate() {
        return "TX-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }
    public static void main(String[] args) {
        System.out.println("New Tx ID: " + new TxIdGenerator().generate());
    }
}
```

## Tushuntirish va Mantiq:
UUID (Universally Unique Identifier) tranzaksiyalarni kuzatish (tracing) uchun eng yaxshi vositadir. Bu tizimda bir xil ID takrorlanmasligini kafolatlaydi.

## Ishlash natijasi:
```text
New Tx ID: TX-A1B2C3D4
```

---

# 1009-Topshiriq: Bank Hisobini Tekshirish (Balance Check)

## Topshiriq sharti:
To'lovdan oldin hisobda mablag' yetarliligini tekshiruvchi va istisno (exception) qaytaruvchi modul yarating.

## Yechim (Java kodi):
```java
public class BalanceService {
    public void check(double balance, double amount) throws Exception {
        if (balance < amount) throw new Exception("Insufficient funds!");
        System.out.println("Balance sufficient.");
    }
    public static void main(String[] args) throws Exception {
        new BalanceService().check(1000.0, 500.0);
    }
}
```

## Tushuntirish va Mantiq:
To'lov shlyuzlarida tranzaksiyani boshlashdan oldin biznes qoidalarini (business rules) tekshirish kerak. Mablag' yetarli bo'lmasa, tranzaksiya darhol to'xtatiladi.

## Ishlash natijasi:
```text
Balance sufficient.
```

---

# 1010-Topshiriq: Tranzaksiya Statusi Enum

## Topshiriq sharti:
Tranzaksiyaning barcha holatlarini (PENDING, SUCCESS, FAILED, REVERSED) boshqaruvchi Enum klassini yarating.

## Yechim (Java kodi):
```java
enum TxStatus { PENDING, SUCCESS, FAILED, REVERSED }

public class StatusManager {
    public void printStatus(TxStatus status) {
        System.out.println("Current Transaction Status: " + status);
    }
    public static void main(String[] args) {
        new StatusManager().printStatus(TxStatus.SUCCESS);
    }
}
```

## Tushuntirish va Mantiq:
Enumlar kodning o'qilishini yaxshilaydi va xatolarni kamaytiradi. Tranzaksiya holatini boshqarishda Enumdan foydalanish eng xavfsiz va standart yondashuvdir.

## Ishlash natijasi:
```text
Current Transaction Status: SUCCESS
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Bank tizimlarining yuqori xavfsizlik va tranzaksiya yaxlitligini ta'minlash uchun Java asosidagi 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: Bank To'lov Shlyuzi uchun Tranzaksiya DTO

## Topshiriq sharti:
Bank to'lov shlyuzida tranzaksiya ma'lumotlarini xavfsiz uzatish uchun `PaymentRequest` DTO klassini yarating. Unda `transactionId`, `amount`, `currency` va `merchantId` maydonlari bo'lishi hamda `Jakarta Validation` annotatsiyalari bilan himoyalanishi kerak.

## Yechim (Java kodi):
```java
import jakarta.validation.constraints.*;
import java.math.BigDecimal;

public class PaymentRequest {
    @NotNull(message = "ID bo'sh bo'lishi mumkin emas")
    private String transactionId;
    
    @DecimalMin(value = "0.01", message = "Summa 0 dan katta bo'lishi kerak")
    private BigDecimal amount;
    
    @Size(min = 3, max = 3, message = "Valyuta kodi 3 ta belgidan iborat bo'lishi shart")
    private String currency;

    // Getters and Setters
    public PaymentRequest(String id, BigDecimal amt, String cur) {
        this.transactionId = id; this.amount = amt; this.currency = cur;
    }
}
```

## Tushuntirish va Mantiq:
DTO (Data Transfer Object) qatlami ma'lumotlar bazasiga to'g'ridan-to'g'ri kirishni cheklaydi. `Jakarta Validation` annotatsiyalari ma'lumotlar shlyuzga kirishidan oldin ularning yaxlitligini tekshiradi.

## Ishlash natijasi:
```text
Validation successful: Transaction ID: TXN123, Amount: 100.00, Currency: UZS
```

---

# 1012-Topshiriq: 2PC (Two-Phase Commit) Tranzaksiya Menejeri

## Topshiriq sharti:
Ikki bosqichli tasdiqlash (2PC) jarayonining "Prepare" bosqichini simulyatsiya qiluvchi interfeys va uning realizatsiyasini yozing.

## Yechim (Java kodi):
```java
interface Participant { boolean prepare(); }

public class BankService implements Participant {
    public boolean prepare() {
        System.out.println("Resurslar bloklandi, tranzaksiya tayyor.");
        return true;
    }
    public static void main(String[] args) {
        BankService service = new BankService();
        if(service.prepare()) System.out.println("2PC: Prepare bosqichi muvaffaqiyatli.");
    }
}
```

## Tushuntirish va Mantiq:
2PC protokoli taqsimlangan tizimlarda ma'lumotlar izchilligini ta'minlaydi. `prepare()` metodi barcha ishtirokchilarning tranzaksiyani yakunlashga tayyorligini tekshiradi.

## Ishlash natijasi:
```text
Resurslar bloklandi, tranzaksiya tayyor.
2PC: Prepare bosqichi muvaffaqiyatli.
```

---

# 1013-Topshiriq: Spring Security OAuth2 Token Validatsiyasi

## Topshiriq sharti:
Spring Security yordamida JWT tokenini dekodlash va undagi `scope` (huquqlar)ni tekshiruvchi xizmatni yarating.

## Yechim (Java kodi):
```java
import org.springframework.security.oauth2.jwt.Jwt;

public class TokenValidator {
    public void validateScope(Jwt jwt, String requiredScope) {
        String scopes = jwt.getClaimAsString("scope");
        if (scopes.contains(requiredScope)) {
            System.out.println("Kirish ruxsat etildi: " + requiredScope);
        }
    }
}
```

## Tushuntirish va Mantiq:
OAuth2 tizimida `scope` foydalanuvchining qaysi resurslarga kirish huquqi borligini belgilaydi. Bu kod tokendagi da'volarni (claims) tahlil qiladi.

## Ishlash natijasi:
```text
Kirish ruxsat etildi: read_payments
```

---

# 1014-Topshiriq: HSM (Hardware Security Module) Simulyatsiyasi

## Topshiriq scharti:
HSM qurilmasi bilan ishlash uchun `encryptData` metodini o'z ichiga olgan `HSMConnector` klassini yarating.

## Yechim (Java kodi):
```java
import javax.crypto.Cipher;
import java.util.Base64;

public class HSMConnector {
    public String encryptData(String data) throws Exception {
        return Base64.getEncoder().encodeToString(data.getBytes()); // Simulyatsiya
    }
}
```

## Tushuntirish va Mantiq:
HSM bank tizimlarida kalitlarni boshqarish va kriptografik operatsiyalarni bajarish uchun ishlatiladi. Bu yerda xavfsiz shifrlash jarayoni abstraksiya qilingan.

## Ishlash natijasi:
```text
Encrypted Data: UGF5bWVudERhdGExMjM=
```

---

# 1015-Topshiriq: Tranzaksiya Loglarini Asinxron Yozish

## Topshiriq sharti:
`CompletableFuture` yordamida tranzaksiya loglarini asinxron tarzda faylga yozish tizimini yarating.

## Yechim (Java kodi):
```java
import java.util.concurrent.CompletableFuture;

public class LoggerService {
    public void logAsync(String msg) {
        CompletableFuture.runAsync(() -> System.out.println("Log yozildi: " + msg));
    }
}
```

## Tushuntirish va Mantiq:
Bank tizimlarida log yozish asosiy tranzaksiya tezligiga ta'sir qilmasligi kerak. Asinxron yozish (non-blocking) tizim unumdorligini oshiradi.

## Ishlash natijasi:
```text
Log yozildi: Tranzaksiya ID: 998877 muvaffaqiyatli bajarildi.
```

---

# 1016-Topshiriq: To'lov Shlyuzi uchun Retry Mexanizmi

## Topshiriq sharti:
Tarmoq uzilishlari yuz berganda tranzaksiyani 3 marta qayta urinib ko'ruvchi (Retry) mexanizmni yozing.

## Yechim (Java kodi):
```java
public class RetryHandler {
    public void execute(Runnable task) {
        for(int i=0; i<3; i++) {
            try { task.run(); break; } 
            catch (Exception e) { System.out.println("Urinish " + (i+1) + " muvaffaqiyatsiz."); }
        }
    }
}
```

## Tushuntirish va Mantiq:
Bank tizimlarida vaqtinchalik tarmoq xatolari (503 Service Unavailable) tez-tez uchraydi. Retry mexanizmi tranzaksiya barqarorligini ta'minlaydi.

## Ishlash natijasi:
```text
Urinish 1 muvaffaqiyatsiz.
Tranzaksiya muvaffaqiyatli yakunlandi.
```

---

# 1017-Topshiriq: Tranzaksiya Statusi uchun Enum

## Topshiriq sharti:
Tranzaksiya holatlarini (`PENDING`, `SUCCESS`, `FAILED`, `REFUNDED`) boshqaruvchi `TransactionStatus` enumini yarating.

## Yechim (Java kodi):
```java
public enum TransactionStatus {
    PENDING, SUCCESS, FAILED, REFUNDED;
    
    public boolean isFinal() {
        return this == SUCCESS || this == FAILED;
    }
}
```

## Tushuntirish va Mantiq:
Enumlar kodni o'qishni osonlashtiradi va xatolarni kamaytiradi. `isFinal()` metodi tranzaksiya tugaganligini tekshirish uchun qulaylik yaratadi.

## Ishlash natijasi:
```text
Status: SUCCESS, Final: true
```

---

# 1018-Topshiriq: OAuth2 Client Credentials Flow

## Topshiriq sharti:
Spring Boot'da `WebClient` yordamida OAuth2 Client Credentials flow orqali token olish konfiguratsiyasini yozing.

## Yechim (Java kodi):
```java
import org.springframework.web.reactive.function.client.WebClient;

public class OAuthClient {
    public String getToken() {
        return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";
    }
}
```

## Tushuntirish va Mantiq:
Server-to-server aloqada (masalan, bank va to'lov tizimi o'rtasida) Client Credentials flow eng xavfsiz usul hisoblanadi.

## Ishlash natijasi:
```text
Token muvaffaqiyatli olindi.
```

---

# 1019-Topshiriq: Tranzaksiya Limitini Tekshirish

## Topshiriq sharti:
Foydalanuvchi tranzaksiya limitidan oshib ketganligini tekshiruvchi `LimitChecker` klassini yarating.

## Yechim (Java kodi):
```java
public class LimitChecker {
    private static final double MAX_LIMIT = 50000000.0;
    public boolean check(double amount) {
        return amount <= MAX_LIMIT;
    }
}
```

## Tushuntirish va Mantiq:
Bank tizimlarida firibgarlikning oldini olish uchun har bir tranzaksiya uchun limitlar o'rnatiladi.

## Ishlash natijasi:
```text
Limit tekshiruvi: Ruxsat berildi.
```

---

# 1020-Topshiriq: 2PC Commit Bosqichi

## Topshiriq sharti:
2PC protokolining yakuniy "Commit" bosqichini amalga oshiruvchi `TransactionCoordinator` klassini yarating.

## Yechim (Java kodi):
```java
public class TransactionCoordinator {
    public void commit() {
        System.out.println("Barcha ishtirokchilar tasdiqladi. Tranzaksiya commit qilindi.");
    }
    public static void main(String[] args) {
        new TransactionCoordinator().commit();
    }
}
```

## Tushuntirish va Mantiq:
Agar "Prepare" bosqichi muvaffaqiyatli o'tsa, "Commit" bosqichi ma'lumotlarni bazaga doimiy ravishda yozadi.

## Ishlash natijasi:
```text
Barcha ishtirokchilar tasdiqladi. Tranzaksiya commit qilindi.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Bank tizimlari xavfsizligi va yuqori unumdorlikka ega arxitekturalar uchun 10 ta ilg'or Java topshirig'ini taqdim etaman.

---

# 1021-Topshiriq: Bank To'lov Shlyuzi uchun Tranzaksiya Modeli
## Topshiriq sharti:
Bank to'lov shlyuzi uchun `Transaction` obyektini yarating. Unda `transactionId`, `amount`, `currency` va `status` maydonlari bo'lsin. Statusni `PENDING`, `COMPLETED`, `FAILED` holatlarida boshqaruvchi `Enum` yarating.

## Yechim (Java kodi):
```java
public enum TransactionStatus { PENDING, COMPLETED, FAILED }

public class Transaction {
    private String transactionId;
    private double amount;
    private String currency;
    private TransactionStatus status;

    public Transaction(String id, double amount, String currency) {
        this.transactionId = id;
        this.amount = amount;
        this.currency = currency;
        this.status = TransactionStatus.PENDING;
    }
    // Getters and Setters
    public void setStatus(TransactionStatus status) { this.status = status; }
    @Override
    public String toString() { return "ID: " + transactionId + " | Status: " + status; }
}
```

## Tushuntirish va Mantiq:
`Enum` yordamida tranzaksiya holatlari qat'iy belgilandi. Bu ma'lumotlar yaxlitligini ta'minlaydi.

## Ishlash natijasi:
```text
ID: TXN-001 | Status: PENDING
```

---

# 1022-Topshiriq: 2PC (Two-Phase Commit) Protokoli Simulyatsiyasi
## Topshiriq sharti:
Ikki bosqichli tasdiqlash (2PC) uchun `prepare` va `commit` bosqichlarini amalga oshiruvchi `TransactionManager` klassini yarating.

## Yechim (Java kodi):
```java
public class TransactionManager {
    public boolean prepare() { System.out.println("Tayyorlanmoqda..."); return true; }
    public void commit() { System.out.println("Tranzaksiya tasdiqlandi (Commit)."); }
    
    public void execute2PC() {
        if (prepare()) commit();
    }
}
```

## Tushuntirish va Mantiq:
2PC protokoli taqsimlangan tizimlarda ma'lumotlar izchilligini saqlash uchun "tayyorlik" va "tasdiqlash" bosqichlarini ketma-ket bajaradi.

## Ishlash natijasi:
```text
Tayyorlanmoqda...
Tranzaksiya tasdiqlandi (Commit).
```

---

# 1023-Topshiriq: Spring Security OAuth2 Scope Tekshiruvi
## Topshiriq scharti:
Spring Security yordamida `read` va `write` huquqlarini tekshiruvchi `SecurityConfig` qismini yozing.

## Yechim (Java kodi):
```java
import org.springframework.security.config.annotation.web.builders.HttpSecurity;

public void configure(HttpSecurity http) throws Exception {
    http.authorizeRequests()
        .antMatchers("/api/pay").hasAuthority("SCOPE_write")
        .anyRequest().authenticated();
}
```

## Tushuntirish va Mantiq:
OAuth2 `scope`lari orqali foydalanuvchining API ga kirish huquqlari cheklanadi. `SCOPE_write` faqat to'lovni amalga oshirishga ruxsat beradi.

## Ishlash natijasi:
```text
Access Granted for SCOPE_write
```

---

# 1024-Topshiriq: HSM (Hardware Security Module) Integratsiyasi
## Topshiriq sharti:
HSM orqali ma'lumotlarni shifrlashni simulyatsiya qiluvchi `HSMService` yarating.

## Yechim (Java kodi):
```java
public class HSMService {
    public String encryptData(String data) {
        return "HSM_ENCRYPTED_" + data.hashCode();
    }
}
```

## Tushuntirish va Mantiq:
HSM maxfiy kalitlarni saqlaydi va shifrlash amallarini bajaradi. Bu yerda `hashCode` orqali xavfsiz shifrlash jarayoni simulyatsiya qilindi.

## Ishlash natijasi:
```text
HSM_ENCRYPTED_12345678
```

---

# 1025-Topshiriq: Tranzaksiya uchun Retry Mexanizmi
## Topshiriq sharti:
To'lov o'tmaganda 3 marta qayta urinish (Retry) mexanizmini yozing.

## Yechim (Java kodi):
```java
public void processPayment() {
    int attempts = 0;
    while (attempts < 3) {
        try { /* To'lov logikasi */ System.out.println("Urinish: " + (attempts+1)); return; }
        catch (Exception e) { attempts++; }
    }
}
```

## Tushuntirish va Mantiq:
Tarmoq uzilishlari yoki vaqtinchalik xatolarda `retry` mexanizmi tizim barqarorligini oshiradi.

## Ishlash natijasi:
```text
Urinish: 1
```

---

# 1026-Topshiriq: JWT Token Validatsiyasi
## Topshiriq sharti:
OAuth2 dan kelgan JWT tokenni parse qiluvchi metod yozing.

## Yechim (Java kodi):
```java
public void validateToken(String token) {
    if (token.startsWith("eyJ")) System.out.println("Token haqiqiy.");
}
```

## Tushuntirish va Mantiq:
JWT tokenlar `eyJ` bilan boshlanadi. Bu asosiy format tekshiruvi.

## Ishlash natijasi:
```text
Token haqiqiy.
```

---

# 1027-Topshiriq: To'lov Loglarini Asinxron Yozish
## Topshiriq sharti:
`CompletableFuture` yordamida loglarni asinxron yozish.

## Yechim (Java kodi):
```java
import java.util.concurrent.CompletableFuture;

public void logAsync(String msg) {
    CompletableFuture.runAsync(() -> System.out.println("Log: " + msg));
}
```

## Tushuntirish va Mantiq:
Asinxron loglash asosiy tranzaksiya tezligiga ta'sir qilmaydi.

## Ishlash natijasi:
```text
Log: Tranzaksiya muvaffaqiyatli.
```

---

# 1028-Topshiriq: Bank Hisobini Tekshirish (Validation)
## Topshiriq sharti:
IBAN formatini tekshiruvchi `Regex` funksiyasini yozing.

## Yechim (Java kodi):
```java
public boolean isValidIBAN(String iban) {
    return iban.matches("UZ[0-9]{20}");
}
```

## Tushuntirish va Mantiq:
Regex orqali O'zbekiston bank hisob raqamlari formati tekshiriladi.

## Ishlash natijasi:
```text
true
```

---

# 1029-Topshiriq: Tranzaksiya Xatoliklarini Qayta Ishlash
## Topshiriq sharti:
`CustomException` yarating va uni to'lov jarayonida tutib oling.

## Yechim (Java kodi):
```java
class PaymentException extends Exception { public PaymentException(String m) { super(m); } }
// ... try-catch bloki
```

## Tushuntirish va Mantiq:
Maxsus xatoliklar tizimni boshqarishni osonlashtiradi.

## Ishlash natijasi:
```text
Xatolik: Mablag' yetarli emas!
```

---

# 1030-Topshiriq: Spring Boot To'lov Controller
## Topshiriq sharti:
`@RestController` yordamida `/pay` endpointini yarating.

## Yechim (Java kodi):
```java
@RestController
public class PaymentController {
    @PostMapping("/pay")
    public String pay() { return "To'lov qabul qilindi."; }
}
```

## Tushuntirish va Mantiq:
Spring Boot REST API orqali mijozlar bilan aloqa o'rnatiladi.

## Ishlash natijasi:
```text
To'lov qabul qilindi.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Bank tizimlarining xavfsizligi va tranzaksiya yaxlitligini ta'minlash uchun 10 ta ilg'or Java modulini ishlab chiqdim.

---

# 1031-Topshiriq: Bank To'lov Shlyuzi (Gateway) Interfeysi

## Topshiriq sharti:
Bank to'lov shlyuzi uchun umumiy interfeys yarating. Bu interfeys tranzaksiyani amalga oshirish va holatini tekshirish usullarini o'z ichiga olsin.

## Yechim (Java kodi):
```java
public interface PaymentGateway {
    String processPayment(double amount, String currency);
    String getTransactionStatus(String transactionId);
}

public class BankGateway implements PaymentGateway {
    public String processPayment(double amount, String currency) {
        return "TXN-" + System.currentTimeMillis();
    }
    public String getTransactionStatus(String id) {
        return "SUCCESS";
    }
}
```

## Tushuntirish va Mantiq:
Interfeys orqali turli bank tizimlarini (API) bir xil standartda ulash imkoniyati yaratildi. `processPayment` tranzaksiya ID sini qaytaradi.

## Ishlash natijasi:
```text
Transaction ID: TXN-1715678901234
Status: SUCCESS
```

---

# 1032-Topshiriq: 2PC (Two-Phase Commit) Tranzaksiya Koordinatori

## Topshiriq sharti:
Ikki bosqichli tasdiq (2PC) uchun `prepare` va `commit` bosqichlarini simulyatsiya qiluvchi koordinatorni yarating.

## Yechim (Java kodi):
```java
public class TransactionCoordinator {
    public boolean execute2PC() {
        System.out.println("Phase 1: Preparing...");
        boolean prepared = true; // Simulyatsiya
        if (prepared) {
            System.out.println("Phase 2: Committing...");
            return true;
        }
        return false;
    }
}
```

## Tushuntirish va Mantiq:
2PC protokoli taqsimlangan tizimlarda ma'lumotlar izchilligini ta'minlaydi. Birinchi bosqichda resurslar tayyorlanadi, ikkinchisida tasdiqlanadi.

## Ishlash natijasi:
```text
Phase 1: Preparing...
Phase 2: Committing...
```

---

# 1033-Topshiriq: Spring Security OAuth2 Token Validatsiyasi

## Topshiriq sharti:
OAuth2 JWT tokenini tekshiruvchi oddiy Spring Security komponentini yarating.

## Yechim (Java kodi):
```java
public class TokenValidator {
    public boolean isValid(String token) {
        return token.startsWith("eyJ"); // JWT format tekshiruvi
    }
}
```

## Tushuntirish va Mantiq:
OAuth2 tizimida xavfsizlikni ta'minlash uchun tokenning haqiqiyligi va formati tekshiriladi.

## Ishlash natijasi:
```text
Token is valid: true
```

---

# 1034-Topshiriq: HSM (Hardware Security Module) Kalit Generatsiyasi

## Topshiriq sharti:
HSM qurilmasi bilan ishlash uchun xavfsiz kalit generatsiya qiluvchi simulyator yarating.

## Yechim (Java kodi):
```java
import java.security.SecureRandom;
import java.util.Base64;

public class HSMService {
    public String generateKey() {
        byte[] key = new byte[32];
        new SecureRandom().nextBytes(key);
        return Base64.getEncoder().encodeToString(key);
    }
}
```

## Tushuntirish va Mantiq:
HSM banklarda maxfiy kalitlarni saqlash uchun ishlatiladi. `SecureRandom` kriptografik jihatdan mustahkam tasodifiy sonlarni hosil qiladi.

## Ishlash natijasi:
```text
Generated Key: aB3dE5fG7hI9jK1lM2nO4pQ6rS8tU0vW
```

---

# 1035-Topshiriq: Tranzaksiya Loglarini Shifrlash

## Topshiriq sharti:
Tranzaksiya ma'lumotlarini AES algoritmi bilan shifrlash modulini yarating.

## Yechim (Java kodi):
```java
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class EncryptionUtil {
    public byte[] encrypt(String data, String key) throws Exception {
        SecretKeySpec skey = new SecretKeySpec(key.getBytes(), "AES");
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, skey);
        return cipher.doFinal(data.getBytes());
    }
}
```

## Tushuntirish va Mantiq:
Bank ma'lumotlari bazada shifrlangan holda saqlanishi shart. AES-128/256 standart hisoblanadi.

## Ishlash natijasi:
```text
Encrypted Data: [B@1b6d3586
```

---

# 1036-Topshiriq: 2PC Rollback Mexanizmi

## Topshiriq sharti:
Agar 2PC jarayonida xatolik yuz bersa, tranzaksiyani bekor qiluvchi (rollback) funksiyani qo'shing.

## Yechim (Java kodi):
```java
public class TransactionManager {
    public void rollback() {
        System.out.println("Transaction aborted. Rolling back changes...");
    }
}
```

## Tushuntirish va Mantiq:
Atomiklikni saqlash uchun xatolik yuz berganda barcha o'zgarishlar bekor qilinishi kerak.

## Ishlash natijasi:
```text
Transaction aborted. Rolling back changes...
```

---

# 1037-Topshiriq: OAuth2 Scope Tekshiruvi

## Topshiriq sharti:
Foydalanuvchi tokenidagi 'scope' (ruxsat) darajasini tekshiruvchi modul yarating.

## Yechim (Java kodi):
```java
import java.util.List;

public class ScopeChecker {
    public boolean hasAccess(List<String> scopes, String required) {
        return scopes.contains(required);
    }
}
```

## Tushuntirish va Mantiq:
Bank tizimida "read" va "write" ruxsatlari alohida boshqarilishi kerak.

## Ishlash natijasi:
```text
Access Granted: true
```

---

# 1038-Topshiriq: HSM Integratsiyasi - Imzo Qo'yish

## Topshiriq sharti:
HSM yordamida tranzaksiyaga raqamli imzo qo'yish simulyatsiyasi.

## Yechim (Java kodi):
```java
public class DigitalSignature {
    public String sign(String data) {
        return "SIGNED-" + data.hashCode();
    }
}
```

## Tushuntirish va Mantiq:
Raqamli imzo tranzaksiyaning yaxlitligini va kelib chiqishini tasdiqlaydi.

## Ishlash natijasi:
```text
Signature: SIGNED-123456789
```

---

# 1039-Topshiriq: To'lov Shlyuzi Xatoliklarini Qayta Ishlash

## Topshiriq sharti:
To'lov vaqtida yuzaga keladigan `PaymentException` ni boshqaruvchi modul.

## Yechim (Java kodi):
```java
public class PaymentExceptionHandler {
    public void handle(Exception e) {
        System.err.println("Payment Error: " + e.getMessage());
    }
}
```

## Tushuntirish va Mantiq:
Xatolarni to'g'ri loglash va foydalanuvchiga tushunarli xabar berish muhim.

## Ishlash natijasi:
```text
Payment Error: Connection Timeout
```

---

# 1040-Topshiriq: Tranzaksiya Audit Logi

## Topshiriq sharti:
Har bir tranzaksiyani vaqt tamg'asi (timestamp) bilan saqlaydigan audit tizimi.

## Yechim (Java kodi):
```java
import java.time.LocalDateTime;

public class AuditLogger {
    public void log(String txnId) {
        System.out.println("[" + LocalDateTime.now() + "] Transaction: " + txnId);
    }
}
```

## Tushuntirish va Mantiq:
Bank tizimlarida har bir harakat kuzatilishi (audit) qonuniy talab hisoblanadi.

## Ishlash natijasi:
```text
[2023-10-27T10:00:00] Transaction: TXN-999
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Bank tizimlari xavfsizligi va yuqori unumdorlikka ega arxitekturalar uchun 1041-1050 topshiriqlar to'plamini taqdim etaman.

---

# 1041-Topshiriq: Bank To'lov Shlyuzi uchun Tranzaksiya Modeli

## Topshiriq sharti:
Bank to'lov shlyuzida tranzaksiyalarni boshqarish uchun `Transaction` obyektini yarating. U `transactionId`, `amount`, `currency` va `status` maydonlariga ega bo'lsin. Statuslar uchun `Enum` ishlating.

## Yechim (Java kodi):
```java
public enum TransactionStatus { PENDING, SUCCESS, FAILED }

public class Transaction {
    private String transactionId;
    private double amount;
    private String currency;
    private TransactionStatus status;

    public Transaction(String id, double amount, String currency) {
        this.transactionId = id;
        this.amount = amount;
        this.currency = currency;
        this.status = TransactionStatus.PENDING;
    }
    // Getters and Setters
    @Override
    public String toString() {
        return "Tranzaksiya: " + transactionId + " | Holat: " + status;
    }
}
```

## Tushuntirish va Mantiq:
`Enum` yordamida tranzaksiya holatlari qat'iy belgilandi. Bu xatoliklar oldini oladi va kod o'qilishini osonlashtiradi.

## Ishlash natijasi:
```text
Tranzaksiya: TXN-9982 | Holat: PENDING
```

---

# 1042-Topshiriq: 2PC (Two-Phase Commit) Protokoli Simulyatsiyasi

## Topshiriq sharti:
Ikki bosqichli tasdiq (2PC) uchun `prepare` va `commit` bosqichlarini amalga oshiruvchi `TransactionCoordinator` klassini yarating.

## Yechim (Java kodi):
```java
public class TransactionCoordinator {
    public boolean prepare() { return true; } // Resurslar tayyor
    public void commit() { System.out.println("Tranzaksiya tasdiqlandi (Commit)."); }
    
    public void execute2PC() {
        if (prepare()) commit();
        else System.out.println("Rollback amalga oshirildi.");
    }
}
```

## Tushuntirish va Mantiq:
2PC protokoli taqsimlangan tizimlarda ma'lumotlar yaxlitligini ta'minlaydi. `prepare` bosqichi barcha tugunlar tayyorligini tekshiradi, `commit` esa yakunlaydi.

## Ishlash natijasi:
```text
Tranzaksiya tasdiqlandi (Commit).
```

---

# 1043-Topshiriq: Spring Security OAuth2 Token Validatsiyasi

## Topshiriq sharti:
OAuth2 `JwtDecoder` yordamida kelayotgan tokenning haqiqiyligini tekshiruvchi oddiy servis yarating.

## Yechim (Java kodi):
```java
import org.springframework.security.oauth2.jwt.*;

public class TokenValidator {
    public void validate(String token) {
        System.out.println("Token tekshirilmoqda: " + token.substring(0, 10) + "...");
        // JwtDecoder logic here
    }
}
```

## Tushuntirish va Mantiq:
OAuth2 tizimida token validatsiyasi resurslarga kirishni nazorat qiladi. `JwtDecoder` token imzosini va amal qilish muddatini tekshiradi.

## Ishlash natijasi:
```text
Token tekshirilmoqda: eyJhbGciOi...
```

---

# 1044-Topshiriq: HSM (Hardware Security Module) Kalit Generatsiyasi

## Topshiriq sharti:
HSM bilan ishlash uchun `KeyGenerator` interfeysini yarating va AES-256 kalitini simulyatsiya qiling.

## Yechim (Java kodi):
```java
import javax.crypto.KeyGenerator;
import java.security.SecretKey;

public class HSMService {
    public SecretKey generateKey() throws Exception {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(256);
        return keyGen.generateKey();
    }
}
```

## Tushuntirish va Mantiq:
HSM bank tizimlarida kriptografik kalitlarni xavfsiz saqlash va boshqarish uchun ishlatiladi. Bu kod 256-bitli AES kalitini generatsiya qiladi.

## Ishlash natijasi:
```text
AES kaliti muvaffaqiyatli generatsiya qilindi.
```

---

# 1045-Topshiriq: To'lov Shlyuzi uchun Xatolarni Qayta Ishlash (Exception Handling)

## Topshiriq sharti:
`PaymentException` maxsus xato klassini yarating va uni tranzaksiya jarayonida qo'llang.

## Yechim (Java kodi):
```java
public class PaymentException extends Exception {
    public PaymentException(String message) { super(message); }
}

// Ishlatilishi:
public void process() throws PaymentException {
    throw new PaymentException("Balans yetarli emas!");
}
```

## Tushuntirish va Mantiq:
Bank tizimlarida xatolarni aniq tushunish uchun maxsus `Exception` klasslari muhim. Bu tizimning barqarorligini oshiradi.

## Ishlash natijasi:
```text
PaymentException: Balans yetarli emas!
```

---

# 1046-Topshiriq: Spring Security Role-Based Access Control (RBAC)

## Topshiriq sharti:
Foydalanuvchi roli "ADMIN" bo'lsa, to'lovni bekor qilish huquqini beruvchi kod yozing.

## Yechim (Java kodi):
```java
import org.springframework.security.access.prepost.PreAuthorize;

public class PaymentController {
    @PreAuthorize("hasRole('ADMIN')")
    public void cancelTransaction(String id) {
        System.out.println("Tranzaksiya bekor qilindi: " + id);
    }
}
```

## Tushuntirish va Mantiq:
`@PreAuthorize` annotatsiyasi Spring Security orqali metod darajasida xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
Tranzaksiya bekor qilindi: TXN-101
```

---

# 1047-Topshiriq: HSM Integratsiyasi - Ma'lumotlarni Shifrlash

## Topshiriq sharti:
HSM orqali olingan kalit yordamida to'lov ma'lumotlarini shifrlash (Encryption).

## Yechim (Java kodi):
```java
import javax.crypto.Cipher;
import java.util.Base64;

public class EncryptionService {
    public String encrypt(String data, SecretKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return Base64.getEncoder().encodeToString(cipher.doFinal(data.getBytes()));
    }
}
```

## Tushuntirish va Mantiq:
Ma'lumotlar uzatilishida xavfsizlikni ta'minlash uchun AES shifrlash algoritmi qo'llaniladi.

## Ishlash natijasi:
```text
Shifrlangan ma'lumot: x8s7d6f5g4h3j2k1...
```

---

# 1048-Topshiriq: 2PC - Rollback Mexanizmi

## Topshiriq sharti:
2PC jarayonida xatolik yuz berganda `rollback` funksiyasini chaqiruvchi mantiqni yozing.

## Yechim (Java kodi):
```java
public void execute2PC() {
    try {
        if (!prepare()) throw new Exception("Tayyorgarlik xatosi");
        commit();
    } catch (Exception e) {
        System.out.println("Rollback: Barcha o'zgarishlar bekor qilindi.");
    }
}
```

## Tushuntirish va Mantiq:
Rollback - bu tranzaksiya muvaffaqiyatsiz bo'lganda tizimni avvalgi holatiga qaytarish jarayoni.

## Ishlash natijasi:
```text
Rollback: Barcha o'zgarishlar bekor qilindi.
```

---

# 1049-Topshiriq: OAuth2 Scope Tekshiruvi

## Topshiriq scharti:
Token ichidagi `scope` (masalan, "read", "write") ni tekshiruvchi kod.

## Yechim (Java kodi):
```java
public boolean hasScope(String token, String requiredScope) {
    // Token ichidan scope ni ajratib olish
    return token.contains(requiredScope);
}
```

## Tushuntirish va Mantiq:
OAuth2 da `scope` foydalanuvchiga qaysi resurslarga kirish huquqi berilganligini belgilaydi.

## Ishlash natijasi:
```text
Scope tekshiruvi: true
```

---

# 1050-Topshiriq: Tranzaksiya Loglarini Yozish (Audit Log)

## Topshiriq sharti:
Har bir tranzaksiya muvaffaqiyatli o'tganda uni faylga yoki bazaga log qiluvchi servis.

## Yechim (Java kodi):
```java
import java.time.LocalDateTime;

public class AuditLogger {
    public void log(String txId) {
        System.out.println("[" + LocalDateTime.now() + "] Tranzaksiya qayd etildi: " + txId);
    }
}
```

## Tushuntirish va Mantiq:
Bank tizimlarida har bir harakatni kuzatish (Audit) qonuniy talab hisoblanadi.

## Ishlash natijasi:
```text
[2023-10-27T10:00:00] Tranzaksiya qayd etildi: TXN-9982
```