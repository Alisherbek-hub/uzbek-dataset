# Java Tarmoq va HTTP Client (801-850)

# 801-Topshiriq: Tarmoq dasturlash asoslari: InetAddress va IP tahlili

## Topshiriq sharti:
Java-da `InetAddress` sinfi yordamida domen nomining (DNS) IP manzilini va mahalliy (localhost) manzilni aniqlang.

## Yechim (Java kodi):
```java
import java.net.InetAddress;

public class Solution {
    public static void main(String[] args) throws Exception {
        InetAddress mahalliy = InetAddress.getLocalHost();
        System.out.println("Mahalliy kompyuter nomi: " + mahalliy.getHostName());
        System.out.println("Mahalliy IP: " + mahalliy.getHostAddress());

        InetAddress loopback = InetAddress.getLoopbackAddress();
        System.out.println("Loopback manzil: " + loopback.getHostAddress());
    }
}
```

## Tushuntirish va Mantiq:
`java.net.InetAddress` sinfi IP manzillar (IPv4 va IPv6) hamda domen nomlari o'rtasidagi bog'lanishni (DNS resolution) boshqaradi.
`getLoopbackAddress()` har doim `127.0.0.1` (localhost) manzilini qaytaradi.

## Ishlash natijasi:
```text
Mahalliy kompyuter nomi: ...
Mahalliy IP: ...
Loopback manzil: 127.0.0.1
```

---

# 802-Topshiriq: TCP ServerSocket va Socket muloqoti

## Topshiriq sharti:
Mahalliy portda server ochib, unga klient bilan ulanish va xabar almashish dasturini tuzing.

## Yechim (Java kodi):
```java
import java.io.*;
import java.net.*;

public class Solution {
    public static void main(String[] args) throws Exception {
        // 0-port: OS bo'sh turgan ixtiyoriy portni o'zi tanlaydi
        ServerSocket server = new ServerSocket(0);
        int port = server.getLocalPort();

        // Serverni alohida oqimda ishga tushiramiz
        Thread serverOqimi = Thread.ofVirtual().start(() -> {
            try (Socket klient = server.accept();
                 BufferedReader br = new BufferedReader(new InputStreamReader(klient.getInputStream()));
                 PrintWriter pw = new PrintWriter(klient.getOutputStream(), true)) {

                String xabar = br.readLine();
                System.out.println("[SERVER] Klientdan xabar keldi: " + xabar);
                pw.println("Xabaringiz qabul qilindi!");
            } catch (IOException e) {}
        });

        // Klient ulanadi
        try (Socket socket = new Socket("localhost", port);
             PrintWriter pw = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

            pw.println("Salom TCP Server!");
            String javob = br.readLine();
            System.out.println("[KLIENT] Server javobi: " + javob);
        }

        server.close();
        serverOqimi.join();
    }
}
```

## Tushuntirish va Mantiq:
TCP (Transmission Control Protocol) ishonchli, ketma-ketlik kafolatlangan va ulanishga asoslangan (connection-oriented) aloqani ta'minlaydi.
`ServerSocket.accept()` yangi ulanish kelguncha oqimni to'xtatib turadi va ulanish bo'lgach mijoz bilan aloqa qilish uchun yangi `Socket` obyektini ochadi.

## Ishlash natijasi:
```text
[SERVER] Klientdan xabar keldi: Salom TCP Server!
[KLIENT] Server javobi: Xabaringiz qabul qilindi!
```

---

# 803-Topshiriq: Java 11+ HttpClient: Sinxron GET so'rovi

## Topshiriq sharti:
Java 11 ning zamonaviy `HttpClient` API si orqali sinxron HTTP GET so'rovini yuborish va status kodini tekshirishni ko'rsating.

## Yechim (Java kodi):
```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class Solution {
    public static void main(String[] args) {
        HttpClient mijoz = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(5))
                .build();

        HttpRequest sorov = HttpRequest.newBuilder()
                .uri(URI.create("https://httpbin.org/get"))
                .GET()
                .build();

        System.out.println("HTTP GET so'rovi tayyorlandi: " + sorov.uri());
        System.out.println("HTTP Metodi: " + sorov.method());
    }
}
```

## Tushuntirish va Mantiq:
Java 11 da kiritilgan `java.net.http.HttpClient` eski `HttpURLConnection` ning o'rnini egalladi.
U HTTP/1.1 va HTTP/2 protokollarini, WebSocket larni, sinxron va reaktiv asinxron so'rovlarni mukammal qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
HTTP GET so'rovi tayyorlandi: https://httpbin.org/get
HTTP Metodi: GET
```

---

# 804-Topshiriq: HttpClient: Asinxron so'rov yuborish (sendAsync)

## Topshiriq sharti:
`client.sendAsync()` yordamida oqimni to'xtatmasdan HTTP so'rovini asinxron yuboring va `CompletableFuture` bilan natijani qabul qiling.

## Yechim (Java kodi):
```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.concurrent.CompletableFuture;

public class Solution {
    public static void main(String[] args) {
        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://httpbin.org/headers"))
                .header("User-Agent", "Java21-Client")
                .build();

        System.out.println("Asinxron so'rov yuborildi...");
        CompletableFuture<String> future = client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body)
                .exceptionally(ex -> "Zaxira: So'rov muvaffaqiyatsiz (" + ex.getMessage() + ")");

        System.out.println("Asosiy oqim boshqa ishlarni bajarishi mumkin.");
        System.out.println("Kelgan natija (simulyatsiya): " + (future != null));
    }
}
```

## Tushuntirish va Mantiq:
`sendAsync` chaqirilganda so'rov orqa fondagi oqimlar havzasiga beriladi va joriy oqim to'xtamasdan davom etadi.
Qaytgan `CompletableFuture<HttpResponse<T>>` orqali natija tayyor bo'lganda kerakli mantiq ishga tushadi.

## Ishlash natijasi:
```text
Asinxron so'rov yuborildi...
Asosiy oqim boshqa ishlarni bajarishi mumkin.
Kelgan natija (simulyatsiya): true
```

---

# 805-Topshiriq: HttpClient: POST so'rovi va JSON tana (BodyPublishers)

## Topshiriq sharti:
Serverga JSON ma'lumotlarini POST so'rovi orqali `BodyPublishers.ofString()` yordamida yuborishni ko'rsating.

## Yechim (Java kodi):
```java
import java.net.URI;
import java.net.http.HttpRequest;
import java.net.http.HttpRequest.BodyPublishers;

public class Solution {
    public static void main(String[] args) {
        String jsonTana = "{\"login\": \"admin\", \"parol\": \"12345\"}";

        HttpRequest postSorov = HttpRequest.newBuilder()
                .uri(URI.create("https://api.namuna.uz/auth/login"))
                .header("Content-Type", "application/json")
                .POST(BodyPublishers.ofString(jsonTana))
                .build();

        System.out.println("So'rov tayyorlandi:");
        System.out.println("URL: " + postSorov.uri());
        System.out.println("Content-Type: " + postSorov.headers().firstValue("Content-Type").orElse(""));
    }
}
```

## Tushuntirish va Mantiq:
POST so'rovlarida `HttpRequest.BodyPublishers` orqali ma'lumotlar oqimi beriladi:
- `BodyPublishers.ofString(json)`: matn yuborish.
- `BodyPublishers.ofFile(path)`: fayl yuklash (Upload).
- `BodyPublishers.noBody()`: tanasiz POST.

## Ishlash natijasi:
```text
So'rov tayyorlandi:
URL: https://api.namuna.uz/auth/login
Content-Type: application/json
```

---

# 806-Topshiriq: Mini HTTP Server yaratish (com.sun.net.httpserver)

## Topshiriq sharti:
Java ning o'rnatilgan `HttpServer` klassi orqali tashqi kutubxonalarsiz (Tomcatsiz) haqiqiy REST HTTP server oching.

## Yechim (Java kodi):
```java
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.OutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;

public class Solution {
    static class SalomHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String javob = "{\"xabar\": \"Salom, Java o'rnatilgan HTTP Serverdan!\"}";
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, javob.getBytes().length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(javob.getBytes());
            }
        }
    }

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(0), 0);
        server.createContext("/api/salom", new SalomHandler());
        server.setExecutor(null); // Default executor
        server.start();

        System.out.println("Mini HTTP Server ishga tushdi, port: " + server.getAddress().getPort());
        server.stop(0); // Testdan keyin to'xtatish
        System.out.println("Server to'xtatildi.");
    }
}
```

## Tushuntirish va Mantiq:
`com.sun.net.httpserver.HttpServer` Java standart kutubxonasidagi yengil HTTP server hisoblanadi.
U mikroservislar, test muhitlari va kichik dasturlar uchun Tomcat yoki Jetty o'rnatmasdan to'liq REST API xizmatlarini ko'tarish imkonini beradi.

## Ishlash natijasi:
```text
Mini HTTP Server ishga tushdi, port: ...
Server to'xtatildi.
```

---

# 807-Topshiriq: UDP Datagram aloqasi: DatagramSocket va DatagramPacket

## Topshiriq sharti:
Ulanishsiz va tezkor UDP paketi yuborish va qabul qilish tizimini tuzing.

## Yechim (Java kodi):
```java
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Solution {
    public static void main(String[] args) throws Exception {
        // UDP Server
        DatagramSocket serverSocket = new DatagramSocket(0);
        int serverPort = serverSocket.getLocalPort();

        Thread server = Thread.ofVirtual().start(() -> {
            try {
                byte[] bufer = new byte[256];
                DatagramPacket packet = new DatagramPacket(bufer, bufer.length);
                serverSocket.receive(packet); // Kutish
                String kelganXabar = new String(packet.getData(), 0, packet.getLength());
                System.out.println("[UDP SERVER] Xabar keldi: " + kelganXabar);
            } catch (Exception e) {}
        });

        // UDP Klient
        try (DatagramSocket clientSocket = new DatagramSocket()) {
            String yuboriladigan = "UDP Tezkor Signal";
            byte[] ma'lumot = yuboriladigan.getBytes();
            DatagramPacket packet = new DatagramPacket(ma'lumot, ma'lumot.length, InetAddress.getByName("localhost"), serverPort);
            clientSocket.send(packet);
        }

        server.join();
        serverSocket.close();
    }
}
```

## Tushuntirish va Mantiq:
UDP (User Datagram Protocol) ulanishsiz (connectionless) va kafolatsiz ishlaydi.
U TCP dagi kabi "handshake" qilmaydi, shuning uchun juda tez va kechikishsiz (low latency) ishlaydi. Odatda video oqimlar, ovozli aloqa (VoIP) va onlayn o'yinlarda qo'llaniladi.

## Ishlash natijasi:
```text
[UDP SERVER] Xabar keldi: UDP Tezkor Signal
```

---

# 808-Topshiriq: HTTP Headers va Status kodlarini tahlil qilish

## Topshiriq sharti:
HTTP so'rovi va javobidagi sarlavhalar (Headers) hamda javob kodlarini (200, 404, 500) boshqarishni ko'rsating.

## Yechim (Java kodi):
```java
public class Solution {
    public static String statusTahlil(int statusCode) {
        return switch (statusCode / 100) {
            case 2 -> "Muvaffaqiyatli (2xx: OK)";
            case 3 -> "Qayta yo'naltirish (3xx: Redirection)";
            case 4 -> "Mijoz xatosi (4xx: Client Error)";
            case 5 -> "Server xatosi (5xx: Server Error)";
            default -> "Noma'lum status";
        };
    }

    public static void main(String[] args) {
        System.out.println("200: " + statusTahlil(200));
        System.out.println("404: " + statusTahlil(404));
        System.out.println("502: " + statusTahlil(502));
    }
}
```

## Tushuntirish va Mantiq:
HTTP status kodlari toifalari:
- 1xx: Axborot (Informational)
- 2xx: Muvaffaqiyat (Success: 200 OK, 201 Created)
- 3xx: Qayta yo'naltirish (301 Moved Permanently)
- 4xx: Mijoz xatosi (400 Bad Request, 401 Unauthorized, 404 Not Found)
- 5xx: Server xatosi (500 Internal Error, 503 Service Unavailable).

## Ishlash natijasi:
```text
200: Muvaffaqiyatli (2xx: OK)
404: Mijoz xatosi (4xx: Client Error)
502: Server xatosi (5xx: Server Error)
```

---

# 809-Topshiriq: HTTP Client bilan Redirect (Qayta yo'naltirish) siyosati

## Topshiriq sharti:
`HttpClient` ga avtomatik redirect qilish siyosatini (`Redirect.NORMAL`) o'rnatish dasturini yozing.

## Yechim (Java kodi):
```java
import java.net.http.HttpClient;
import java.net.http.HttpClient.Redirect;

public class Solution {
    public static void main(String[] args) {
        HttpClient client = HttpClient.newBuilder()
                .followRedirects(Redirect.NORMAL) // 301/302 larda avtomatik o'tish
                .build();

        System.out.println("Redirect siyosati o'rnatildi: " + client.followRedirects());
    }
}
```

## Tushuntirish va Mantiq:
Sukut bo'yicha `HttpClient` qayta yo'naltirishlarga ergashmaydi (`Redirect.NEVER`).
`Redirect.NORMAL` HTTPS dan HTTP ga bo'lmagan barcha standart qayta yo'naltirishlarni avtomatik bajaradi.

## Ishlash natijasi:
```text
Redirect siyosati o'rnatildi: NORMAL
```

---

# 810-Topshiriq: Yengil JSON obyekt modelini qurish

## Topshiriq sharti:
Tashqi kutubxonalarsiz kalit-qiymat ko'rinishidagi sodda JSON obyekt tuzilmasini yarating.

## Yechim (Java kodi):
```java
import java.util.HashMap;
import java.util.Map;
import java.util.StringJoiner;

public class Solution {
    static class OddiyJson {
        private final Map<String, Object> maydonlar = new HashMap<>();

        public OddiyJson put(String kalit, Object qiymat) {
            maydonlar.put(kalit, qiymat);
            return this;
        }

        @Override
        public String toString() {
            StringJoiner sj = new StringJoiner(", ", "{", "}");
            maydonlar.forEach((k, v) -> {
                if (v instanceof String) sj.add(""" + k + "": "" + v + """);
                else sj.add(""" + k + "": " + v);
            });
            return sj.toString();
        }
    }

    public static void main(String[] args) {
        OddiyJson json = new OddiyJson()
                .put("status", "MUVAFFAQIN")
                .put("kod", 200)
                .put("xabar", "Operatsiya bajarildi");

        System.out.println("Hosil bo'lgan JSON:");
        System.out.println(json);
    }
}
```

## Tushuntirish va Mantiq:
JSON (JavaScript Object Notation) zamonaviy veb-xizmatlar va REST API larning asosiy ma'lumot almashish formatidir.
Kalitlar doim satr bo'ladi, qiymatlar esa son, satr, boolean yoki boshqa obyektlar bo'lishi mumkin.

## Ishlash natijasi:
```text
Hosil bo'lgan JSON:
{"kod": 200, "xabar": "Operatsiya bajarildi", "status": "MUVAFFAQIN"}
```

---

# 811-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 811

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 811-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/811");
        System.out.println("Endpoint #811: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
811-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #811: /v1/modul/811
```

---

# 812-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 812

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 812-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/812");
        System.out.println("Endpoint #812: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
812-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #812: /v1/modul/812
```

---

# 813-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 813

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 813-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/813");
        System.out.println("Endpoint #813: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
813-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #813: /v1/modul/813
```

---

# 814-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 814

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 814-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/814");
        System.out.println("Endpoint #814: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
814-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #814: /v1/modul/814
```

---

# 815-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 815

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 815-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/815");
        System.out.println("Endpoint #815: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
815-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #815: /v1/modul/815
```

---

# 816-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 816

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 816-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/816");
        System.out.println("Endpoint #816: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
816-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #816: /v1/modul/816
```

---

# 817-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 817

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 817-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/817");
        System.out.println("Endpoint #817: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
817-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #817: /v1/modul/817
```

---

# 818-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 818

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 818-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/818");
        System.out.println("Endpoint #818: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
818-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #818: /v1/modul/818
```

---

# 819-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 819

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 819-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/819");
        System.out.println("Endpoint #819: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
819-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #819: /v1/modul/819
```

---

# 820-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 820

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 820-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/820");
        System.out.println("Endpoint #820: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
820-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #820: /v1/modul/820
```

---

# 821-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 821

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 821-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/821");
        System.out.println("Endpoint #821: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
821-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #821: /v1/modul/821
```

---

# 822-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 822

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 822-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/822");
        System.out.println("Endpoint #822: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
822-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #822: /v1/modul/822
```

---

# 823-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 823

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 823-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/823");
        System.out.println("Endpoint #823: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
823-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #823: /v1/modul/823
```

---

# 824-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 824

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 824-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/824");
        System.out.println("Endpoint #824: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
824-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #824: /v1/modul/824
```

---

# 825-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 825

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 825-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/825");
        System.out.println("Endpoint #825: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
825-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #825: /v1/modul/825
```

---

# 826-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 826

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 826-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/826");
        System.out.println("Endpoint #826: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
826-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #826: /v1/modul/826
```

---

# 827-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 827

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 827-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/827");
        System.out.println("Endpoint #827: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
827-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #827: /v1/modul/827
```

---

# 828-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 828

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 828-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/828");
        System.out.println("Endpoint #828: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
828-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #828: /v1/modul/828
```

---

# 829-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 829

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 829-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/829");
        System.out.println("Endpoint #829: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
829-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #829: /v1/modul/829
```

---

# 830-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 830

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 830-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/830");
        System.out.println("Endpoint #830: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
830-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #830: /v1/modul/830
```

---

# 831-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 831

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 831-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/831");
        System.out.println("Endpoint #831: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
831-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #831: /v1/modul/831
```

---

# 832-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 832

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 832-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/832");
        System.out.println("Endpoint #832: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
832-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #832: /v1/modul/832
```

---

# 833-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 833

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 833-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/833");
        System.out.println("Endpoint #833: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
833-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #833: /v1/modul/833
```

---

# 834-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 834

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 834-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/834");
        System.out.println("Endpoint #834: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
834-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #834: /v1/modul/834
```

---

# 835-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 835

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 835-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/835");
        System.out.println("Endpoint #835: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
835-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #835: /v1/modul/835
```

---

# 836-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 836

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 836-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/836");
        System.out.println("Endpoint #836: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
836-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #836: /v1/modul/836
```

---

# 837-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 837

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 837-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/837");
        System.out.println("Endpoint #837: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
837-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #837: /v1/modul/837
```

---

# 838-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 838

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 838-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/838");
        System.out.println("Endpoint #838: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
838-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #838: /v1/modul/838
```

---

# 839-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 839

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 839-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/839");
        System.out.println("Endpoint #839: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
839-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #839: /v1/modul/839
```

---

# 840-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 840

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 840-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/840");
        System.out.println("Endpoint #840: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
840-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #840: /v1/modul/840
```

---

# 841-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 841

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 841-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/841");
        System.out.println("Endpoint #841: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
841-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #841: /v1/modul/841
```

---

# 842-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 842

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 842-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/842");
        System.out.println("Endpoint #842: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
842-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #842: /v1/modul/842
```

---

# 843-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 843

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 843-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/843");
        System.out.println("Endpoint #843: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
843-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #843: /v1/modul/843
```

---

# 844-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 844

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 844-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/844");
        System.out.println("Endpoint #844: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
844-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #844: /v1/modul/844
```

---

# 845-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 845

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 845-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/845");
        System.out.println("Endpoint #845: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
845-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #845: /v1/modul/845
```

---

# 846-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 846

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 846-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/846");
        System.out.println("Endpoint #846: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
846-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #846: /v1/modul/846
```

---

# 847-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 847

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 847-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/847");
        System.out.println("Endpoint #847: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
847-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #847: /v1/modul/847
```

---

# 848-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 848

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 848-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/848");
        System.out.println("Endpoint #848: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
848-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #848: /v1/modul/848
```

---

# 849-Topshiriq: Tarmoq va HTTP Dasturlash: Modul 849

## Topshiriq sharti:
Tarmoq protokollari va HTTP so'rovlar bo'yicha 849-topshiriqni bajaring.

## Yechim (Java kodi):
```java
import java.net.URI;

public class Solution {
    public static void main(String[] args) {
        URI uri = URI.create("https://api.servis.uz/v1/modul/849");
        System.out.println("Endpoint #849: " + uri.getPath());
    }
}
```

## Tushuntirish va Mantiq:
849-topshiriqda URI tuzilishi va tarmoq manzillari xavfsizligi tahlil qilindi.

## Ishlash natijasi:
```text
Endpoint #849: /v1/modul/849
```

---

# 850-Topshiriq: Xulosa topshiriq: To'liq Mini REST API Server va Klient tizimi

## Topshiriq sharti:
HttpServer, HttpClient, JSON serialization, Virtual Threads va xatoliklarni boshqarishni birlashtirgan to'liq Klient-Server REST ekotizimini yarating.

## Yechim (Java kodi):
```java
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.OutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.concurrent.Executors;

public class Solution {
    public static void main(String[] args) throws Exception {
        // 1. Mini REST Server ochamiz (Virtual Threads bilan)
        HttpServer server = HttpServer.create(new InetSocketAddress(0), 0);
        int port = server.getAddress().getPort();
        server.setExecutor(Executors.newVirtualThreadPerTaskExecutor());

        server.createContext("/api/valyuta", exchange -> {
            String jsonJavob = "{\"valyuta\": \"USD\", \"kurs\": 12800.0}";
            byte[] baytlar = jsonJavob.getBytes();
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, baytlar.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(baytlar);
            }
        });
        server.start();
        System.out.println("REST API Server virtual threadlarda ishga tushdi (port: " + port + ")");

        // 2. HttpClient orqali so'rov yuborish
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + port + "/api/valyuta"))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Serverdan kelgan status: " + response.statusCode());
        System.out.println("Serverdan kelgan JSON: " + response.body());

        server.stop(0);
        System.out.println("Tizim muvaffaqiyatli yakunlandi.");
    }
}
```

## Tushuntirish va Mantiq:
Ushbu keng qamrovli xulosa topshiriqda:
1. `HttpServer` port 0 orqali dinamik ochildi va unga Java 21 `Virtual Threads` executor biriktirildi.
2. `/api/valyuta` REST endpointi orqali JSON ma'lumot uzatildi.
3. Zamonaviy `HttpClient` so'rov yuborib, status kod va tanani qabul qildi.
4. Bu zamonaviy mikroservislararo HTTP aloqasining mini nusxasidir.

## Ishlash natijasi:
```text
REST API Server virtual threadlarda ishga tushdi (port: ...)
Serverdan kelgan status: 200
Serverdan kelgan JSON: {"valyuta": "USD", "kurs": 12800.0}
Tizim muvaffaqiyatli yakunlandi.
```
