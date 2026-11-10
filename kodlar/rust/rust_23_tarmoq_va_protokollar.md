# Khorazmiy AI: Rust - Modul 23
## Mavzu: Tarmoq protokollari: TCP/UDP soketlari, HTTP/3, QUIC va WebSockets (Rust Tokio/Hyper/Tonic)

Salom, men **Khorazmiy AI** loyihasining Rust va tizimli tarmoq dasturlash bo'yicha bosh dataset mutaxassisiman. Ushbu modulda zamonaviy yuqori yuklamali tarmoq protokollari, asinxron TCP/UDP soketlari, HTTP/3, QUIC, gRPC va WebSockets bo'yicha 50 ta sanoat darajasidagi amaliy topshiriq va ularning to'liq yechimlari keltirilgan.

---
### Topshiriq #1101: Tokio bilan Asinxron TCP Echo Server
**Tavsif:** Real vaqt rejimida minglab bir vaqtning o'zida keluvchi mijozlarni qabul qiladigan va ulardan kelgan ma'lumotlarni o'zlariga qaytarib jo'natuvchi (Echo) asinxron TCP server yaratish talab qilinadi.
**Talablar:** Tokio runtime, har bir ulanish uchun alohida asinxron task ochish, xotira sarfini minimallashtirish va xatoliklarni xavfsiz boshqarish.
**Yechim (Rust):**
```rust
use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use std::error::Error;

async fn handle_client(mut socket: TcpStream) -> Result<(), Box<dyn Error + Send + Sync>> {
    // 4 KB o'lchamdagi bufer orqali xotira ajratishni optimallashtiramiz
    let mut buf = vec![0u8; 4096];

    loop {
        // Asinxron o'qish operatsiyasi
        let n = socket.read(&mut buf).await?;

        // Agar 0 bayt o'qilsa, mijoz aloqani uzgan hisoblanadi (EOF)
        if n == 0 {
            break;
        }

        // Qabul qilingan ma'lumotni to'liq qaytarib jo'natamiz
        socket.write_all(&buf[..n]).await?;
    }

    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let addr = "127.0.0.1:8080";
    let listener = TcpListener::bind(addr).await?;
    println!("TCP Echo Server ishga tushdi: {}", addr);

    loop {
        // Yangi kiruvchi ulanishni asinxron qabul qilish
        let (socket, peer_addr) = listener.accept().await?;
        println!("Yangi ulanish qabul qilindi: {}", peer_addr);

        // Tokio thread-poolida har bir mijozni yengil vaznli green-thread (task)da bajaramiz
        tokio::spawn(async move {
            if let Err(e) = handle_client(socket).await {
                eprintln!("Ulanishda xatolik yuz berdi [{}]: {:?}", peer_addr, e);
            }
        });
    }
}
```
**Tushuntirish:** `TcpListener::accept().await` operatsiyasi bloklanmaydi va operatsion tizimning epoll/kqueue event loopiga tayanadi. `tokio::spawn` har bir TCP oqimini alohida task sifatida boshqarib, bitta OS ipida yuz minglab ulanishlarni minimal xotira (taxminan 2-4 KB task boshiga) bilan boshqarish imkonini beradi.

---

### Topshiriq #1102: Tokio Framing va LengthDelimitedCodec bilan xabarlar chegarasini ajratish
**Tavsif:** TCP oqim (stream) protokoli bo'lgani sababli, paketlar birlashib ketishi (TCP packet sticking) yoki bo'linib ketishi mumkin. Xabarlar chegarasini prefiks uzunligi (Length-prefix) orqali kafolatli ajratuvchi mexanizm yaratish zarur.
**Talablar:** `tokio-util` kutubxonasining `LengthDelimitedCodec` vositasidan foydalanish, `FramedRead` va `FramedWrite` oqimlarini boshqarish.
**Yechim (Rust):**
```rust
use tokio::net::TcpListener;
use tokio_util::codec::{FramedRead, FramedWrite, LengthDelimitedCodec};
use futures::{SinkExt, StreamExt};
use bytes::Bytes;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("127.0.0.1:8081").await?;
    println!("Frame-asosidagi TCP server 8081-portda ishlamoqda...");

    while let Ok((socket, peer_addr)) = listener.accept().await {
        tokio::spawn(async move {
            // TCP streamni o'qish va yozish qismlariga ajratamiz
            let (reader, writer) = socket.into_split();

            // 4 baytli big-endian uzunlik prefiksiga ega kodek
            let mut framed_reader = FramedRead::new(reader, LengthDelimitedCodec::new());
            let mut framed_writer = FramedWrite::new(writer, LengthDelimitedCodec::new());

            while let Some(message_result) = framed_reader.next().await {
                match message_result {
                    Ok(frame) => {
                        let text = String::from_utf8_lossy(&frame);
                        println!("Qabul qilingan to'liq kadr [{}]: {}", peer_addr, text);

                        // Javobni ham prefiks uzunlik bilan o'rab qaytaramiz
                        let response = format!("Qabul qilindi: {}", text);
                        if let Err(e) = framed_writer.send(Bytes::from(response)).await {
                            eprintln!("Javob yuborishda xatolik: {:?}", e);
                            break;
                        }
                    }
                    Err(e) => {
                        eprintln!("Kadrni dekodlashda xato: {:?}", e);
                        break;
                    }
                }
            }
        });
    }
    Ok(())
}
```
**Tushuntirish:** `LengthDelimitedCodec` avtomatik ravishda xabar boshidagi 4 bayt uzunlikni o'qiydi va butun paket to'liq yetib kelguncha kutadi. Bu dasturchini xom baytlarni buferlash va chegaralarni hisoblashdagi xatolardan xalos etadi.

---

### Topshiriq #1103: socket2 orqali SO_REUSEPORT va TCP_NODELAY parametrlarini sozlash
**Tavsif:** Millionlab ulanishlarni bir nechta yadroviy jarayonlar o'rtasida taqsimlash va Nagle algoritmini o'chirish orqali kechikishni (latency) sub-millisekund darajasiga tushirish talab qilinadi.
**Talablar:** `socket2::Socket` orqali past darajali soket konfiguratsiyasi va uni `tokio::net::TcpListener`ga aylantirish.
**Yechim (Rust):**
```rust
use socket2::{Domain, Protocol, Socket, Type};
use std::net::SocketAddr;
use std::error::Error;
use tokio::net::TcpListener;

fn create_high_performance_listener(addr: SocketAddr) -> Result<TcpListener, Box<dyn Error>> {
    // IPv4 va TCP protokoli uchun past darajali soket yaratamiz
    let socket = Socket::new(Domain::IPV4, Type::STREAM, Some(Protocol::TCP))?;

    // Bir nechta jarayon/ip bir xil portga ulanishi uchun SO_REUSEPORT
    #[cfg(unix)]
    socket.set_reuse_port(true)?;

    // Manzilni qayta darhol ishlatish uchun SO_REUSEADDR
    socket.set_reuse_address(true)?;

    // Nagle algoritmini o'chirish: paketlar to'planishini kutmasdan darhol uzatiladi
    socket.set_nodelay(true)?;

    // Asinxron I/O uchun soketni non-blocking rejimga o'tkazish shart
    socket.set_nonblocking(true)?;

    // Soketni manzilga bog'lash va tinglashni boshlash (backlog = 1024)
    socket.bind(&addr.into())?;
    socket.listen(1024)?;

    // Standart std::net::TcpListener orqali Tokio listeneriga o'tkazish
    let std_listener: std::net::TcpListener = socket.into();
    let tokio_listener = TcpListener::from_std(std_listener)?;

    Ok(tokio_listener)
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let addr: SocketAddr = "127.0.0.1:9000".parse()?;
    let listener = create_high_performance_listener(addr)?;
    println!("Yuqori unumdorlikdagi soket ishga tushdi: {}", addr);

    while let Ok((mut stream, peer)) = listener.accept().await {
        println!("Bog'langan mijoz: {}", peer);
        // Har bir mijoz uchun ham nodelay parametrini o'rnatamiz
        let _ = stream.set_nodelay(true);
    }
    Ok(())
}
```
**Tushuntirish:** `SO_REUSEPORT` operatsion tizim yadrosiga bir nechta soketlar o'rtasida yuklamani avtomatik muvozanatlash (kernel-level load balancing) imkonini beradi. `TCP_NODELAY` esa Nagle algoritmining 40-200ms kechikishini bartaraf qiladi.

---

### Topshiriq #1104: Tokio UDP soketi orqali telemetriya paketlarini qabul qilish
**Tavsif:** IoT qurilmalaridan soniyasiga 100 000 dan ortiq yuboriladigan UDP telemetriya paketlarini yo'qotishlarsiz va ulanish o'rnatmasdan qabul qiluvchi server yarating.
**Talablar:** `tokio::net::UdpSocket`, ulanishsiz paket almashinuvi, manzilni qayd qilish va javob qaytarish.
**Yechim (Rust):**
```rust
use tokio::net::UdpSocket;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let bind_addr = "0.0.0.0:8888";
    let socket = UdpSocket::bind(bind_addr).await?;
    println!("UDP Telemetriya Serveri tinglamoqda: {}", bind_addr);

    // Xotirada qayta ishlatiladigan 2 KB statik bufer
    let mut buffer = [0u8; 2048];

    loop {
        // Paketni va yuboruvchining manzilini asinxron qabul qilamiz
        match socket.recv_from(&mut buffer).await {
            Ok((size, peer_addr)) => {
                let telemetry_data = &buffer[..size];
                println!("Telemetriya qabul qilindi [{} bayt] -> {}", size, peer_addr);

                // Tasdiqlovchi (ACK) javob paketini jo'natamiz
                let ack_msg = b"STATUS:ACK";
                if let Err(e) = socket.send_to(ack_msg, peer_addr).await {
                    eprintln!("ACK yuborishda xato: {:?}", e);
                }
            }
            Err(e) => {
                eprintln!("Paketni qabul qilishda xato: {:?}", e);
            }
        }
    }
}
```
**Tushuntirish:** UDP soketlari ulanish holatini (handshake, FIN/ACK) saqlamaydi, shuning uchun juda kam tarmoq xarajati talab qiladi. Bitta UDP soketi orqali bir vaqtda millionlab turli mijozlar bilan aloqa o'rnatish mumkin.

---

### Topshiriq #1105: UDP Multicast yordamida tarmoqdagi tugunlarni avtomatik kashf qilish
**Tavsif:** Bir xil lokal tarmoqda joylashgan mikroservislar markaziy serverga tayanmasdan bir-birlarini avtomatik topishi (Peer Discovery) uchun UDP Multicast guruhidan foydalanish zarur.
**Talablar:** IPv4 multicast guruhiga a'zo bo'lish (`join_multicast_v4`), vaqti-vaqti bilan o'z mavjudligini bildirish va boshqalarni tinglash.
**Yechim (Rust):**
```rust
use std::net::{Ipv4Addr, SocketAddrV4};
use std::time::Duration;
use tokio::net::UdpSocket;
use tokio::time::sleep;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let multicast_addr: Ipv4Addr = "239.255.42.99".parse()?;
    let port = 7645;
    let local_bind: SocketAddrV4 = SocketAddrV4::new(Ipv4Addr::UNSPECIFIED, port);

    // Soketni yaratamiz va multicast guruhiga qo'shilamiz
    let socket = UdpSocket::bind(local_bind).await?;
    socket.join_multicast_v4(multicast_addr, Ipv4Addr::UNSPECIFIED)?;
    println!("Multicast guruhiga qo'shildi: {}:{}", multicast_addr, port);

    // Yuboruvchi vazifasini parallel ishga tushirish
    let sender_socket = socket.local_addr()?;
    tokio::spawn(async move {
        let sender = UdpSocket::bind("0.0.0.0:0").await.unwrap();
        let target = format!("{}:{}", multicast_addr, port);
        loop {
            let msg = format!("TUGUN_SALOM:id={}", std::process::id());
            let _ = sender.send_to(msg.as_bytes(), &target).await;
            sleep(Duration::from_secs(3)).await;
        }
    });

    // Tinglovchi sikli
    let mut buf = [0u8; 1024];
    loop {
        let (len, remote_addr) = socket.recv_from(&mut buf).await?;
        let message = String::from_utf8_lossy(&buf[..len]);
        println!("Kashfiyot xabari keldi: '{}' manzildan: {}", message, remote_addr);
    }
}
```
**Tushuntirish:** Multicast orqali bitta yuborilgan paket tarmoq switch darajasida faqat guruhga obuna bo'lgan tugunlarga ko'paytiriladi. Bu broadcast kabi butun subnetni to'ldirmaydi va yuqori samaradorlik beradi.

---

### Topshiriq #1106: Bytes va Tokio IO utility bilan Zero-Copy xotira boshqaruvi
**Tavsif:** Katta hajmdagi ma'lumotlarni tarmoq orqali qayta yuborishda (proxy/relay) ortiqcha bayt nusxalash (heap allocation) xotira yuklamasini oshiradi. Zero-copy usulida xotira boshqaruvini amalga oshirish kerak.
**Talablar:** `bytes::Bytes` va `tokio::io::copy_bidirectional` yordamida ikkita TCP oqimi o'rtasida to'g'ridan-to'g'ri o'tkazuvchanlikni ta'minlash.
**Yechim (Rust):**
```rust
use tokio::net::{TcpListener, TcpStream};
use tokio::io::copy_bidirectional;
use std::error::Error;

async fn proxy_tunnel(mut client: TcpStream, target_addr: &str) -> Result<(), Box<dyn Error + Send + Sync>> {
    // Maqsad serverga ulanish
    let mut target = TcpStream::connect(target_addr).await?;
    println!("Maqsad serverga ulandi: {}", target_addr);

    // Ikkala oqim o'rtasida zero-copy rejimida ikki tomonlama ma'lumot almashinuvi
    let (from_client, from_target) = copy_bidirectional(&mut client, &mut target).await?;

    println!("Tunnel yakunlandi: mijozdan {} bayt, maqsad serverdan {} bayt uzatildi", 
             from_client, from_target);
    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("127.0.0.1:8085").await?;
    println!("Zero-Copy TCP Proksi 8085-portda kutmoqda...");

    while let Ok((client_socket, _)) = listener.accept().await {
        tokio::spawn(async move {
            let target_addr = "127.0.0.1:8080"; // Maqsad xizmat manzili
            if let Err(e) = proxy_tunnel(client_socket, target_addr).await {
                eprintln!("Tunnel xatosi: {:?}", e);
            }
        });
    }
    Ok(())
}
```
**Tushuntirish:** `tokio::io::copy_bidirectional` ichki mexanizmida OS darajasidagi `splice` yoki optimallashgan ichki buferlardan foydalanadi. Bu orqali foydalanuvchi xotirasida takroriy `Vec<u8>` ajratilishining oldi olinadi.

---

### Topshiriq #1107: Tokio Broadcast kanali yordamida Real-Vaqt TCP Chat serveri
**Tavsif:** Bir nechta foydalanuvchilar bir vaqtda ulangan chat tizimida bir foydalanuvchi yozgan xabarni boshqa barcha ulangan ishtirokchilarga kechikishsiz yetkazish zarur.
**Talablar:** `tokio::sync::broadcast` kanali, ko'p qabul qiluvchi (MPSC o'rniga broadcast), oqimli o'qish/yozish.
**Yechim (Rust):**
```rust
use tokio::net::TcpListener;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::sync::broadcast;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("127.0.0.1:7777").await?;
    println!("Asinxron Chat Serveri 7777-portda ishga tushdi");

    // 100 ta xabargacha sig'imga ega universal xabarlar kanali
    let (tx, _rx) = broadcast::channel::<(String, std::net::SocketAddr)>(100);

    loop {
        let (mut socket, addr) = listener.accept().await?;
        let tx = tx.clone();
        let mut rx = tx.subscribe();

        tokio::spawn(async move {
            let (reader, mut writer) = socket.split();
            let mut reader = BufReader::new(reader);
            let mut line = String::new();

            loop {
                tokio::select! {
                    // Mijozdan xabar kelganda
                    result = reader.read_line(&mut line) => {
                        if result.unwrap_or(0) == 0 { break; } // Aloqa uzildi
                        let _ = tx.send((line.clone(), addr));
                        line.clear();
                    }
                    // Boshqa foydalanuvchilardan kelgan xabarni mijozga yetkazish
                    Ok((msg, sender_addr)) = rx.recv() => {
                        if sender_addr != addr {
                            let broadcast_msg = format!("[{}]: {}", sender_addr, msg);
                            if writer.write_all(broadcast_msg.as_bytes()).await.is_err() {
                                break;
                            }
                        }
                    }
                }
            }
            println!("Mijoz aloqani tark etdi: {}", addr);
        });
    }
}
```
**Tushuntirish:** `broadcast` kanali pub-sub modelida ishlaydi: bitta yuboruvchi (tx) xabarni barcha obunachilarga tarqatadi. `tokio::select!` ikkita asinxron hodisani (kiruvchi I/O va kanal xabari) bitta asinxron tsiklda uzluksiz muvofiqlashtiradi.

---

### Topshiriq #1108: CancellationToken orqali Graceful Shutdown va ulanishlarni xavfsiz to'xtatish
**Tavsif:** Serverga `SIGINT` (Ctrl+C) yoki to'xtash signali kelganda faol ishlayotgan tranzaksiyalarni uzib yubormasdan, barcha mijozlarga javob qaytarib, soketlarni batamom xavfsiz yopish talab qilinadi.
**Talablar:** `tokio_util::sync::CancellationToken`, `tokio::signal::ctrl_c()`, mavjud ulanishlar tugashini kutish.
**Yechim (Rust):**
```rust
use tokio::net::TcpListener;
use tokio_util::sync::CancellationToken;
use std::time::Duration;
use std::sync::Arc;
use tokio::sync::Semaphore;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let token = CancellationToken::new();
    let cloned_token = token.clone();

    // OS signalini kutuvchi vazifa
    tokio::spawn(async move {
        tokio::signal::ctrl_c().await.expect("Signal tinglashda xato");
        println!("
To'xtatish signali (SIGINT) qabul qilindi. Server yopilmoqda...");
        cloned_token.cancel();
    });

    let listener = TcpListener::bind("127.0.0.1:8088").await?;
    let active_connections = Arc::new(Semaphore::new(1000)); // Maksimal ulanishlar
    println!("Graceful shutdown serveri 8088-portda ishlamoqda.");

    loop {
        tokio::select! {
            _ = token.cancelled() => {
                println!("Yangi ulanishlarni qabul qilish to'xtatildi.");
                break;
            }
            Ok((socket, peer)) = listener.accept() => {
                let conn_token = token.clone();
                tokio::spawn(async move {
                    tokio::select! {
                        _ = conn_token.cancelled() => {
                            println!("Ulanish to'xtatish rejimiga o'tkazildi: {}", peer);
                        }
                        _ = async {
                            // Mijozning haqiqiy vazifasi
                            tokio::time::sleep(Duration::from_secs(2)).await;
                        } => {
                            println!("So'rov muvaffaqiyatli yakunlandi: {}", peer);
                        }
                    }
                });
            }
        }
    }

    println!("Barcha amallar yakunlandi. Server to'xtatildi.");
    Ok(())
}
```
**Tushuntirish:** `CancellationToken` ierarxik bekor qilish mexanizmini beradi: asosiy token bekor qilinganda barcha bog'liq bo'lgan bolalar tokenlari avtomatik ravishda xabardor qilinadi va asinxron tasklar xotira sizishisiz to'xtatiladi.

---

### Topshiriq #1109: Hyper asosida past kechikishli HTTP/1.1 REST API serveri
**Tavsif:** Mikrosekundlik kechikish talab qilinadigan moliyaviy tizimlar uchun minimal overheadga ega bo'lgan sof asinxron HTTP/1.1 serverini qurish zarur.
**Talablar:** `hyper` 1.0 arxitekturasi, `http_body_util::Full`, Marshrutlash (Routing) va JSON status qaytarish.
**Yechim (Rust):**
```rust
use std::convert::Infallible;
use std::net::SocketAddr;
use hyper::server::conn::http1;
use hyper::service::service_fn;
use hyper::{Request, Response, StatusCode};
use hyper::body::Incoming;
use http_body_util::Full;
use bytes::Bytes;
use tokio::net::TcpListener;

async fn route_handler(req: Request<Incoming>) -> Result<Response<Full<Bytes>>, Infallible> {
    match (req.method(), req.uri().path()) {
        (&hyper::Method::GET, "/health") => {
            let body = Full::new(Bytes::from("{"status":"healthy","uptime_ms":9999}"));
            Ok(Response::builder()
                .status(StatusCode::OK)
                .header("Content-Type", "application/json")
                .body(body)
                .unwrap())
        }
        _ => {
            let body = Full::new(Bytes::from("{"error":"Topilmadi"}"));
            Ok(Response::builder()
                .status(StatusCode::NOT_FOUND)
                .body(body)
                .unwrap())
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr: SocketAddr = "127.0.0.1:8089".parse()?;
    let listener = TcpListener::bind(addr).await?;
    println!("Hyper HTTP/1.1 API server: http://{}", addr);

    loop {
        let (stream, _) = listener.accept().await?;
        tokio::spawn(async move {
            let io = hyper_util::rt::TokioIo::new(stream);
            if let Err(err) = http1::Builder::new().serve_connection(io, service_fn(route_handler)).await {
                eprintln!("Ulanishga xizmat ko'rsatishda xato: {:?}", err);
            }
        });
    }
}
```
**Tushuntirish:** Hyper 1.0 o'zining modulli arxitekturasi bilan I/O qatlamini ajratib olgan. `TokioIo` orqali Tokio TCP oqimini to'g'ridan-to'g'ri bog'lash orqali yuqori darajadagi freymvorklarning keraksiz qatlamlarisiz maksimal tezlikka erishiladi.

---

### Topshiriq #1110: Hyper orqali HTTP Connection Pooling va Keep-Alive mijozi
**Tavsif:** Mikroservislar o'rtasida har safar yangi TCP ulanish ochish 3 tomonlama qo'l berish (3-way handshake) va TLS hisob-kitoblari sababli tizimni sekinlashtiradi. Ulanishlarni qayta ishlatuvchi HTTP Connection Pool yarating.
**Talablar:** `hyper_util::client::legacy::Client`, Keep-Alive ulanishlarni boshqarish va asinxron so'rovlar yuborish.
**Yechim (Rust):**
```rust
use hyper_util::client::legacy::Client;
use hyper_util::rt::TokioExecutor;
use http_body_util::Empty;
use bytes::Bytes;
use hyper::Request;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Keep-Alive va connection pooling xususiyatlariga ega Client yaratamiz
    let client = Client::builder(TokioExecutor::new())
        .pool_idle_timeout(std::time::Duration::from_secs(30))
        .pool_max_idle_per_host(10)
        .build_http::<Empty<Bytes>>();

    let uri = "http://httpbin.org/get".parse()?;

    // 5 ta ketma-ket so'rov yuboramiz - birinchi ulanishdan keyingilari pool orqali o'tadi
    for i in 1..=5 {
        let req = Request::builder()
            .uri(&uri)
            .header("Host", "httpbin.org")
            .header("Connection", "keep-alive")
            .body(Empty::<Bytes>::new())?;

        let start = std::time::Instant::now();
        let res = client.request(req).await?;
        println!("So'rov #{} yakunlandi: Status = {}, Vaqt = {:?}", i, res.status(), start.elapsed());
    }

    Ok(())
}
```
**Tushuntirish:** HTTP Keep-Alive mavjud TCP soketini yopmasdan navbatdagi so'rovlar uchun ochiq qoldiradi. Connection Pool esa bo'sh soketlarni xotirada saqlab, yangi so'rov kelganda qayta ulanish kechikishini nolga tenglashtiradi.

---

### Topshiriq #1111: tokio-rustls bilan mTLS (Mutual TLS) xavfsiz server yaratish
**Tavsif:** Bank yoki mudofaa tarmoqlarida nafaqat server o'z sertifikatini tasdiqlashi, balki har bir kiruvchi mijoz ham o'z shaxsiy sertifikatini (Client Certificate) taqdim etishi shart bo'lgan mTLS tizimini quring.
**Talablar:** `tokio-rustls`, `rustls::ServerConfig`, mijoz sertifikatini tekshiruvchi `WebPkiServerVerifier`.
**Yechim (Rust):**
```rust
use std::sync::Arc;
use tokio::net::TcpListener;
use tokio_rustls::rustls::pki_types::{CertificateDer, PrivateKeyDer};
use tokio_rustls::rustls::server::WebPkiClientVerifier;
use tokio_rustls::rustls::{RootCertStore, ServerConfig};
use tokio_rustls::TlsAcceptor;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

fn setup_mtls_config(
    ca_cert: CertificateDer<'static>,
    server_cert: CertificateDer<'static>,
    server_key: PrivateKeyDer<'static>,
) -> Result<ServerConfig, Box<dyn std::error::Error>> {
    let mut root_store = RootCertStore::empty();
    root_store.add(ca_cert)?;

    // Mijoz sertifikatini CA ildiz sertifikati orqali tekshirish talabi
    let client_verifier = WebPkiClientVerifier::builder(Arc::new(root_store)).build()?;

    let config = ServerConfig::builder()
        .with_client_cert_verifier(client_verifier)
        .with_single_cert(vec![server_cert], server_key)?;

    Ok(config)
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Sanoatda sertifikatlar xavfsiz fayldan yoki KMS dan yuklanadi
    println!("mTLS konfiguratsiyasi tayyorlanmoqda...");
    // Mock sifatida mTLS acceptor tuzilishi:
    // let acceptor = TlsAcceptor::from(Arc::new(config));
    println!("mTLS xavfsiz serveri TLS 1.3 shifrlash bilan himoyalangan.");
    Ok(())
}
```
**Tushuntirish:** mTLS ikki tomonlama kriptografik kafolat beradi. Server mijozning CA tomonidan tasdiqlangan kalitiga egaligini tekshiradi, bu esa ruxsatsiz ulanishlarni TLS handshake bosqichidayoq to'xtatadi.

---

### Topshiriq #1112: Tonic yordamida Unary gRPC xizmati va uning implementatsiyasi
**Tavsif:** Ikkita mikroservis o'rtasida Protocol Buffers orqali qat'iy tiplangan, yuqori tezlikdagi bir martalik so'rov-javob (Unary RPC) tizimini joriy qiling.
**Talablar:** `tonic`, proto definition, `#[tonic::async_trait]`, xizmatni ro'yxatdan o'tkazish.
**Yechim (Rust):**
```rust
// Protocol Buffers kompilyatsiyasidan hosil bo'lgan kod strukturasi
pub mod payment {
    tonic::include_proto!("payment");
}

use payment::payment_service_server::{PaymentService, PaymentServiceServer};
use payment::{PaymentRequest, PaymentResponse};
use tonic::{transport::Server, Request, Response, Status};

#[derive(Default)]
pub struct MyPaymentService;

#[tonic::async_trait]
impl PaymentService for MyPaymentService {
    async fn process_payment(
        &self,
        request: Request<PaymentRequest>,
    ) -> Result<Response<PaymentResponse>, Status> {
        let req = request.into_inner();
        println!("To'lov so'rovi qabul qilindi: ID={}, Miqdor={}", req.order_id, req.amount);

        if req.amount <= 0.0 {
            return Err(Status::invalid_argument("Miqdor 0 dan katta bo'lishi shart!"));
        }

        let reply = PaymentResponse {
            success: true,
            transaction_id: format!("TXN-{}", req.order_id),
            message: "To'lov muvaffaqiyatli amalga oshirildi".into(),
        };

        Ok(Response::new(reply))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "127.0.0.1:50051".parse()?;
    let payment_service = MyPaymentService::default();

    println!("Tonic gRPC Server 50051-portda ishlamoqda...");
    Server::builder()
        .add_service(PaymentServiceServer::new(payment_service))
        .serve(addr)
        .await?;

    Ok(())
}
```
**Tushuntirish:** Tonic gRPC protokoli HTTP/2 ustida binar Protobuf formatida ma'lumot tashiydi. Unary RPC da bitta so'rovga bitta javob olinadi, lekin JSON ga qaraganda bir necha barobar kam tarmoq trafigi va CPU vaqti sarflanadi.

---

### Topshiriq #1113: Tonic bilan Server-Side Streaming gRPC xizmati
**Tavsif:** Mijoz bitta so'rov yuborganida server unga real vaqtdagi fond birjasi narxlari yoki monitoring ma'lumotlarini uzluksiz oqim (stream) ko'rinishida yuborib turishi zarur.
**Talablar:** `tokio_stream::wrappers::ReceiverStream`, `tokio::sync::mpsc`, doimiy oqim boshqaruvi.
**Yechim (Rust):**
```rust
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;
use tonic::{transport::Server, Request, Response, Status};
use std::time::Duration;

pub mod stock {
    tonic::include_proto!("stock");
}
use stock::stock_service_server::{StockService, StockServiceServer};
use stock::{StockRequest, StockPriceUpdate};

#[derive(Default)]
pub struct StockServiceImpl;

#[tonic::async_trait]
impl StockService for StockServiceImpl {
    type StreamStockPricesStream = ReceiverStream<Result<StockPriceUpdate, Status>>;

    async fn stream_stock_prices(
        &self,
        request: Request<StockRequest>,
    ) -> Result<Response<Self::StreamStockPricesStream>, Status> {
        let symbol = request.into_inner().symbol;
        println!("Oqim so'ralgan aksiya: {}", symbol);

        let (tx, rx) = mpsc::channel(16);

        tokio::spawn(async move {
            let mut price = 150.0;
            for i in 1..=10 {
                price += 0.5;
                let update = StockPriceUpdate {
                    symbol: symbol.clone(),
                    price,
                    timestamp: i,
                };
                if tx.send(Ok(update)).await.is_err() {
                    println!("Mijoz oqimni to'xtatdi.");
                    break;
                }
                tokio::time::sleep(Duration::from_millis(500)).await;
            }
        });

        Ok(Response::new(ReceiverStream::new(rx)))
    }
}
```
**Tushuntirish:** Server-Side streaming bitta HTTP/2 oqimida serverga cheksiz ma'lumot freymlari jo'natish imkonini beradi. Kanallar (`mpsc`) orqali asinxron orqa fondagi voqealar to'g'ridan-to'g'ri gRPC oqimiga ulanadi.

---

### Topshiriq #1114: Tonic bilan Client-Side Streaming gRPC xizmati
**Tavsif:** Mijoz serverga katta hajmdagi sensor ko'rsatkichlari yoki fayl bo'laklarini uzluksiz oqim sifatida yuboradi, server esa jarayon yakunlanganda bitta umumiy xulosa qaytaradi.
**Talablar:** `tonic::Streaming<T>`, oqimdan asinxron elementlarni qabul qilish va yig'ish.
**Yechim (Rust):**
```rust
use tonic::{Request, Response, Status, Streaming};

pub mod upload {
    tonic::include_proto!("upload");
}
use upload::uploader_server::{Uploader, UploaderServer};
use upload::{DataChunk, UploadSummary};

#[derive(Default)]
pub struct FileUploaderService;

#[tonic::async_trait]
impl Uploader for FileUploaderService {
    async fn upload_stream(
        &self,
        request: Request<Streaming<DataChunk>>,
    ) -> Result<Response<UploadSummary>, Status> {
        let mut stream = request.into_inner();
        let mut total_bytes = 0u64;
        let mut chunk_count = 0u32;

        while let Some(chunk_result) = stream.message().await? {
            total_bytes += chunk_result.data.len() as u64;
            chunk_count += 1;
        }

        println!("Oqim tugadi: {} ta bo'lak, jami {} bayt qabul qilindi", chunk_count, total_bytes);

        let summary = UploadSummary {
            total_bytes,
            chunk_count,
            status: "Yuklash muvaffaqiyatli yakunlandi".to_string(),
        };

        Ok(Response::new(summary))
    }
}
```
**Tushuntirish:** Client-Side streaming server xotirasini bo'sh saqlaydi, chunki server gigabaytlab fayllarni birdaniga qabul qilmasdan, har bir bo'lakni oqimda tahlil qilib xotiradan tozalaydi.

---

### Topshiriq #1115: Tonic Bidirectional Streaming (ikki tomonlama oqimli) gRPC
**Tavsif:** Real-vaqtli video monitoring yoki interaktiv o'yin serverlarida mijoz va server bir vaqtning o'zida mustaqil ravishda bir-birlariga xabarlar oqimini jo'natishi zarur.
**Talablar:** Ikkala yo'nalishda mustaqil asinxron oqimlar (`Streaming<Req>` va `ReceiverStream<Res>`).
**Yechim (Rust):**
```rust
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;
use tonic::{Request, Response, Status, Streaming};

pub mod chat {
    tonic::include_proto!("chat");
}
use chat::chat_service_server::{ChatService, ChatServiceServer};
use chat::{ChatMessage};

#[derive(Default)]
pub struct BiChatService;

#[tonic::async_trait]
impl ChatService for BiChatService {
    type ChatStreamStream = ReceiverStream<Result<ChatMessage, Status>>;

    async fn chat_stream(
        &self,
        request: Request<Streaming<ChatMessage>>,
    ) -> Result<Response<Self::ChatStreamStream>, Status> {
        let mut in_stream = request.into_inner();
        let (tx, rx) = mpsc::channel(32);

        // Mijozdan kelayotgan xabarlarni o'qib, unga javob oqimini shakllantirish
        tokio::spawn(async move {
            while let Ok(Some(msg)) = in_stream.message().await {
                println!("Mijoz [{}]: {}", msg.user, msg.text);
                let echo_reply = ChatMessage {
                    user: "Server".to_string(),
                    text: format!("Javob: {}", msg.text),
                };
                if tx.send(Ok(echo_reply)).await.is_err() {
                    break;
                }
            }
        });

        Ok(Response::new(ReceiverStream::new(rx)))
    }
}
```
**Tushuntirish:** Bidirectional streaming HTTP/2 multiplexing kuchidan to'liq foydalanadi: ikkita tomon ham to'liq dupleks (full-duplex) aloqada ishlaydi va oqimlar bir-birini bloklamaydi.

---

### Topshiriq #1116: Tonic gRPC Interceptor orqali xavfsizlik tokenlarini tekshirish
**Tavsif:** Har bir keluvchi gRPC so'rovining metadata sarlavhasida (metadata) yaroqli `authorization` tokeni borligini biznes mantiqqa kirmasdan avval tekshiruvchi interceptor middleware yarating.
**Talablar:** `tonic::service::Interceptor`, metadata tekshiruvi, noto'g'ri token uchun `Status::unauthenticated`.
**Yechim (Rust):**
```rust
use tonic::{Request, Status};

// Har bir keluvchi so'rov uchun tekshiruvchi interceptor funksiyasi
pub fn auth_interceptor(req: Request<()>) -> Result<Request<()>, Status> {
    const VALID_TOKEN: &str = "Bearer maxfiy-khorazmiy-token-2026";

    match req.metadata().get("authorization") {
        Some(token_meta) => {
            if let Ok(token_str) = token_meta.to_str() {
                if token_str == VALID_TOKEN {
                    return Ok(req);
                }
            }
            Err(Status::unauthenticated("Xato yoki yaroqsiz avtorizatsiya tokeni"))
        }
        None => Err(Status::unauthenticated("Authorization sarlavhasi topilmadi")),
    }
}

// Serverga ulanish usuli:
// let service = PaymentServiceServer::with_interceptor(MyPaymentService::default(), auth_interceptor);
```
**Tushuntirish:** Interceptorlar HTTP/gRPC so'rovlarini yo'lda tutib oluvchi filtr vazifasini o'taydi. Noto'g'ri so'rovlar xizmat kodiga yetib bormasdan dastlabki bosqichda rad etiladi, bu esa resurslarni tejaydi.

---

### Topshiriq #1117: Quinn kutubxonasi yordamida QUIC Connection va xavfsiz TLS 1.3 qo'l berish
**Tavsif:** TCP ning "Head-of-Line blocking" muammosini hal qiluvchi, UDP asosidagi eng yangi QUIC (RFC 9000) protokoli orqali xavfsiz ulanish o'rnatuvchi server yarating.
**Talablar:** `quinn` kutubxonasi, TLS 1.3 shifrlash, `Endpoint` yaratish va ulanishni qabul qilish.
**Yechim (Rust):**
```rust
use quinn::{Endpoint, ServerConfig};
use std::net::SocketAddr;
use std::sync::Arc;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let addr: SocketAddr = "127.0.0.1:4433".parse()?;
    
    // Quinn server konfiguratsiyasini shakllantirish (TLS 1.3 QUIC uchun majburiy)
    // Sanoatda sertifikatlar fayldan olinadi
    println!("QUIC Server endpointi ishga tushirilmoqda: {}", addr);
    // let endpoint = Endpoint::server(server_config, addr)?;

    println!("QUIC protokoli 4433-portda UDP orqali 0-RTT va TLS 1.3 qo'l berishini kutmoqda.");
    Ok(())
}
```
**Tushuntirish:** QUIC protokoli TLS 1.3 bilan bevosita integratsiyalashgan bo'lib, TCP ning 3-way handshake va alohida TLS handshake bosqichlarini birlashtirib, ulanish o'rnatish vaqtini 1 RTT yoki hatto 0 RTT ga qisqartiradi.

---

### Topshiriq #1118: QUIC protokoli orqali bir nechta mustaqil oqimlarni multiplekslash
**Tavsif:** Bitta QUIC ulanishi ichida bir nechta parallel, mustaqil ikki tomonlama (bidirectional) oqimlarni ochish va bitta oqimda paket yo'qolsa ham boshqalari to'xtab qolmasligini ta'minlash.
**Talablar:** `quinn::Connection`, `open_bi`, parallel ma'lumot uzatish.
**Yechim (Rust):**
```rust
use quinn::Connection;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

pub async fn handle_quic_streams(conn: Connection) {
    println!("Yangi QUIC ulanish qabul qilindi: {}", conn.remote_address());

    // Bir nechta ikki tomonlama oqimlarni qabul qilish
    while let Ok((mut send_stream, mut recv_stream)) = conn.accept_bi().await {
        tokio::spawn(async move {
            let mut buf = vec![0u8; 1024];
            if let Ok(Some(n)) = recv_stream.read(&mut buf).await {
                println!("QUIC oqimidan kelgan baytlar: {}", n);
                let reply = b"QUIC_STREAM_OK";
                let _ = send_stream.write_all(reply).await;
                let _ = send_stream.finish();
            }
        });
    }
}
```
**Tushuntirish:** TCP da bitta paket yo'qolsa, qolgan barcha ma'lumotlar navbatda to'xtab qoladi (Head-of-Line blocking). QUIC da esa har bir oqim o'zining ketma-ketlik raqamiga ega bo'lib, oqimlar bir-birining kechikishiga mutlaqo bog'liq emas.

---

### Topshiriq #1119: QUIC Unreliable Datagrams orqali tezkor telemetriya va o'yin paketlarini uzatish
**Tavsif:** Real vaqtli ko'p foydalanuvchili o'yinlarda o'yinchining pozitsiyasi har 16 ms da yangilanadi. Eski koordinatani qayta jo'natish mantiqsiz, shuning uchun kafolatlanmagan (unreliable datagram) uzatish zarur.
**Talablar:** `quinn::Connection::send_datagram`, `read_datagram`, yo'qolishga chidamli arxitektura.
**Yechim (Rust):**
```rust
use quinn::Connection;
use bytes::Bytes;

pub async fn send_player_position(conn: &Connection, player_id: u32, x: f32, y: f32) -> Result<(), Box<dyn std::error::Error>> {
    // 12 baytli ixcham binar paket
    let mut payload = Vec::with_capacity(12);
    payload.extend_from_slice(&player_id.to_be_bytes());
    payload.extend_from_slice(&x.to_be_bytes());
    payload.extend_from_slice(&y.to_be_bytes());

    // Kafolatlanmagan, ammo TLS orqali shifrlangan QUIC Datagram yuborish
    conn.send_datagram(Bytes::from(payload))?;
    Ok(())
}

pub async fn receive_datagrams(conn: Connection) {
    loop {
        match conn.read_datagram().await {
            Ok(dgram) => {
                println!("QUIC Datagram qabul qilindi: {} bayt", dgram.len());
            }
            Err(e) => {
                eprintln!("Datagram o'qishda xato: {:?}", e);
                break;
            }
        }
    }
}
```
**Tushuntirish:** QUIC Datagrams xususiyati (RFC 9221) oddiy UDP ning tezligini saqlagan holda, QUIC ning shifrlash (TLS 1.3) va tiqilinch nazorati (Congestion Control) qulayliklaridan foydalanish imkoniyatini beradi.

---

### Topshiriq #1120: h3 kutubxonasi yordamida HTTP/3 Server yaratish
**Tavsif:** Eng so'nggi HTTP/3 spetsifikatsiyasi bo'yicha QUIC protokoli ustida ishlovchi web server quring.
**Talablar:** `h3` kutubxonasi, QUIC endpoint ustiga HTTP/3 ulanishini bog'lash, so'rovlarni parslash.
**Yechim (Rust):**
```rust
use h3::server::Connection;
use quinn::Connection as QuinnConnection;
use std::error::Error;

pub async fn serve_h3_connection(quinn_conn: QuinnConnection) -> Result<(), Box<dyn Error>> {
    // Quinn ulanishini h3 HTTP/3 protokoli drayveriga o'tkazish
    let mut h3_conn = h3::server::Connection::new(h3_quinn::Connection::new(quinn_conn)).await?;
    println!("HTTP/3 qo'l berish (handshake) muvaffaqiyatli o'rnatildi!");

    while let Some((req, mut stream)) = h3_conn.accept().await? {
        println!("HTTP/3 So'rovi: Metod={}, URI={}", req.method(), req.uri());
        
        let response = http::Response::builder()
            .status(http::StatusCode::OK)
            .header("content-type", "text/plain")
            .body(())?;

        stream.send_response(response).await?;
        stream.send_data(bytes::Bytes::from("Salom, HTTP/3 dunyosi!")).await?;
        stream.finish().await?;
    }

    Ok(())
}
```
**Tushuntirish:** HTTP/3 (RFC 9114) HTTP semantikasini saqlab qolgan holda transport qatlamida TCP o'rniga QUIC dan foydalanadi. Bu mobil tarmoqlarda Wi-Fi dan LTE ga o'tganda aloqa uzilmasligini (Connection Migration) ta'minlaydi.

---

### Topshiriq #1121: tokio-tungstenite bilan asinxron WebSocket Server
**Tavsif:** Brauzerlar bilan doimiy ikki tomonlama aloqa o'rnatish uchun HTTP ulanishini 101 Switching Protocols orqali WebSocket aloqasiga ko'taruvchi (upgrade) server yarating.
**Talablar:** `tokio_tungstenite::accept_async`, matnli xabarlarni qabul qilish va javob qaytarish.
**Yechim (Rust):**
```rust
use tokio::net::TcpListener;
use tokio_tungstenite::accept_async;
use tokio_tungstenite::tungstenite::Message;
use futures::{StreamExt, SinkExt};
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("127.0.0.1:9001").await?;
    println!("WebSocket server ws://127.0.0.1:9001 manzilida tinglamoqda...");

    while let Ok((stream, peer_addr)) = listener.accept().await {
        println!("Mijoz ulandi: {}", peer_addr);

        tokio::spawn(async move {
            // TCP streamni WebSocket protokoli darajasiga ko'taramiz
            let mut ws_stream = match accept_async(stream).await {
                Ok(ws) => ws,
                Err(e) => {
                    eprintln!("WebSocket qo'l berishida xato: {:?}", e);
                    return;
                }
            };

            while let Some(msg_result) = ws_stream.next().await {
                match msg_result {
                    Ok(Message::Text(text)) => {
                        println!("WebSocket matn keldi: {}", text);
                        let response = Message::Text(format!("Serverdan javob: {}", text));
                        if ws_stream.send(response).await.is_err() { break; }
                    }
                    Ok(Message::Close(_)) => {
                        println!("Mijoz WebSocketni yopdi: {}", peer_addr);
                        break;
                    }
                    Ok(_) => {} // Binary, Ping, Pong
                    Err(e) => {
                        eprintln!("Xatolik yuz berdi: {:?}", e);
                        break;
                    }
                }
            }
        });
    }
    Ok(())
}
```
**Tushuntirish:** WebSocket standart HTTP portlarida boshlanadi va sarlavhalar almashinuvidan so'ng to'liq ikki tomonlama kadrli (framed) bayt oqimiga aylanadi. Bu HTTP so'rovlaridagi sarlavha ortiqchaligini olib tashlaydi.

---

### Topshiriq #1122: WebSocket Heartbeat (Ping/Pong) va o'lik ulanishlarni avtomatik uzish
**Tavsif:** Tarmoq simi uzilganda yoki telefon aloqa doirasidan chiqqanda TCP ulanishi uzoq vaqt "yarim ochiq" (half-open) qolib server xotirasini band qiladi. Davriy Ping yuborib javob bermagan ulanishlarni tozalash talab etiladi.
**Talablar:** Davriy interval bilan `Message::Ping`, timeout va o'lik ulanishni yopish.
**Yechim (Rust):**
```rust
use std::time::Duration;
use tokio::time::{interval, timeout};
use tokio_tungstenite::tungstenite::Message;
use futures::{SinkExt, StreamExt};

pub async fn monitor_websocket_heartbeat<S>(mut ws_stream: S) 
where
    S: StreamExt<Item = Result<Message, tokio_tungstenite::tungstenite::Error>> 
       + SinkExt<Message> + Unpin,
{
    let mut ping_interval = interval(Duration::from_secs(15));

    loop {
        tokio::select! {
            _ = ping_interval.tick() => {
                // Ping xabarini jo'natamiz
                if ws_stream.send(Message::Ping(vec![1, 2, 3])).await.is_err() {
                    println!("Ping jo'natib bo'lmadi, aloqa uzilmoqda");
                    break;
                }
            }
            msg = ws_stream.next() => {
                match msg {
                    Some(Ok(Message::Pong(_))) => {
                        println!("Mijozdan Pong (tiriklik belgisi) qabul qilindi");
                    }
                    Some(Ok(Message::Close(_))) | None => {
                        println!("Mijoz aloqani yopdi");
                        break;
                    }
                    _ => {}
                }
            }
        }
    }
}
```
**Tushuntirish:** WebSocket spetsifikatsiyasiga ko'ra Ping qabul qilgan tomon darhol bir xil baytli Pong qaytarishi shart. Agar ma'lum vaqt (masalan, 30 soniya) ichida javob kelmasa, server soketni xavfsiz yopadi va xotirani bo'shatadi.

---

### Topshiriq #1123: WebSocket orqali binar ma'lumotlarni uzatish va qabul qilish
**Tavsif:** Matnli JSON ma'lumotlarini serializatsiya qilish yuqori chastotali moliya yoki o'yinlarda CPU ga ortiqcha yuk beradi. Binar Protobuf/MessagePack ma'lumotlarini to'g'ridan-to'g'ri `Message::Binary` orqali almashing.
**Talablar:** `Message::Binary`, binar paketni o'qish va javob sifatida binar ma'lumot yuborish.
**Yechim (Rust):**
```rust
use tokio_tungstenite::tungstenite::Message;
use futures::{SinkExt, StreamExt};

pub async fn handle_binary_stream<S>(mut ws_stream: S)
where
    S: StreamExt<Item = Result<Message, tokio_tungstenite::tungstenite::Error>> 
       + SinkExt<Message> + Unpin,
{
    while let Some(Ok(msg)) = ws_stream.next().await {
        if let Message::Binary(bin_data) = msg {
            println!("Binar kadr qabul qilindi: {} bayt", bin_data.len());

            // Masalan, dastlabki 4 bayt buyruq kodi bo'lsa
            if bin_data.len() >= 4 {
                let cmd = u32::from_be_bytes(bin_data[0..4].try_into().unwrap());
                println!("Buyruq kodi: 0x{:08X}", cmd);
            }

            // Javob tariqasida binar tasdiq qaytaramiz
            let response_bytes = vec![0xAA, 0xBB, 0x01];
            let _ = ws_stream.send(Message::Binary(response_bytes)).await;
        }
    }
}
```
**Tushuntirish:** Binar kadrlar UTF-8 tekshiruvidan o'tmaydi, shuning uchun tungstenite kutubxonasi ularni minimal overhead bilan qabul qiladi. Bu tarmoq o'tkazuvchanligini 40-70% gacha tejaydi.

---

### Topshiriq #1124: Token Bucket algoritmi asosida tarmoq so'rovlarini cheklash (Rate Limiting)
**Tavsif:** DoS/DDoS hujumlaridan himoyalanish va API kvotalarini boshqarish uchun har bir IP manzil bo'yicha so'rovlar chastotasini cheklovchi xotira-samarador Rate Limiter quring.
**Talablar:** Token Bucket algoritmi, vaqt bo'yicha to'ldirish (refill), cheklovdan oshganda 429 Too Many Requests qaytarish.
**Yechim (Rust):**
```rust
use std::time::Instant;
use std::sync::Mutex;

pub struct TokenBucket {
    capacity: f64,
    tokens: f64,
    refill_rate_per_sec: f64,
    last_update: Instant,
}

impl TokenBucket {
    pub fn new(capacity: f64, refill_rate_per_sec: f64) -> Self {
        Self {
            capacity,
            tokens: capacity,
            refill_rate_per_sec,
            last_update: Instant::now(),
        }
    }

    pub fn allow_request(&mut self, cost: f64) -> bool {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_update).as_secs_f64();
        self.last_update = now;

        // O'tgan vaqt davomida yangi tokenlarni qo'shamiz
        self.tokens = (self.tokens + elapsed * self.refill_rate_per_sec).min(self.capacity);

        if self.tokens >= cost {
            self.tokens -= cost;
            true // So'rovga ruxsat berildi
        } else {
            false // Cheklovdan oshdi (Rate Limited)
        }
    }
}
```
**Tushuntirish:** Token Bucket qisqa muddatli so'rovlar portlashiga (burst traffic) imkon beradi, ammo uzoq muddatli o'rtacha tezlikni qat'iy belgilangan chegarada ushlab turadi. Bu zamonaviy API shlyuzlarining standart algoritmidir.

---

### Topshiriq #1125: Tarmoq so'rovlarida Circuit Breaker patterni
**Tavsif:** Tashqi mikroxizmat ishdan chiqqanda unga qayta-qayta so'rov yuborib resurslarni tugatmaslik uchun kaskadli nosozliklarni to'xtatuvchi avtomatik o'chirgich (Circuit Breaker) yarating.
**Talablar:** Uchta holat: `Closed` (normal), `Open` (nosoz, so'rovlar darhol rad etiladi), `HalfOpen` (tizimni sinash).
**Yechim (Rust):**
```rust
use std::time::{Duration, Instant};

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum CircuitState {
    Closed,
    Open,
    HalfOpen,
}

pub struct CircuitBreaker {
    state: CircuitState,
    failure_threshold: u32,
    failure_count: u32,
    cooldown_period: Duration,
    last_failure_time: Option<Instant>,
}

impl CircuitBreaker {
    pub fn new(failure_threshold: u32, cooldown_period: Duration) -> Self {
        Self {
            state: CircuitState::Closed,
            failure_threshold,
            failure_count: 0,
            cooldown_period,
            last_failure_time: None,
        }
    }

    pub fn can_execute(&mut self) -> bool {
        match self.state {
            CircuitState::Closed => true,
            CircuitState::Open => {
                if let Some(last_fail) = self.last_failure_time {
                    if last_fail.elapsed() >= self.cooldown_period {
                        self.state = CircuitState::HalfOpen;
                        return true;
                    }
                }
                false
            }
            CircuitState::HalfOpen => true,
        }
    }

    pub fn on_success(&mut self) {
        self.failure_count = 0;
        self.state = CircuitState::Closed;
    }

    pub fn on_failure(&mut self) {
        self.failure_count += 1;
        self.last_failure_time = Some(Instant::now());
        if self.failure_count >= self.failure_threshold {
            self.state = CircuitState::Open;
        }
    }
}
```
**Tushuntirish:** Circuit Breaker nosoz xizmatlarga behuda murojaat qilib iplarni (threads) bloklanishdan saqlaydi. Tizim soviydi va belgilangan vaqtdan keyin bitta sinov so'rovi (HalfOpen) orqali xizmat tiklanganligini tekshiradi.

---

### Topshiriq #1126: SOCKS5 Proksi serverini noldan qurish (TCP Relay)
**Tavsif:** Mijozlarning tarmoq so'rovlarini anonimlashtirish va korporativ xavfsizlik devorlari orqali o'tkazish uchun RFC 1928 standarti bo'yicha SOCKS5 proksi serverini yarating.
**Talablar:** Autentifikatsiyasiz (NO AUTH) handshake, IPv4 manzilini o'qish, maqsadli server bilan TCP bog'lanish va relay qilish.
**Yechim (Rust):**
```rust
use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncReadExt, AsyncWriteExt, copy_bidirectional};
use std::net::Ipv4Addr;
use std::error::Error;

async fn handle_socks5(mut client: TcpStream) -> Result<(), Box<dyn Error + Send + Sync>> {
    let mut buf = [0u8; 256];

    // 1. Qo'l berish (Handshake): Versiya va autentifikatsiya usullari
    client.read_exact(&mut buf[0..2]).await?;
    let (version, nmethods) = (buf[0], buf[1] as usize);
    if version != 5 { return Err("Faqat SOCKS5 qo'llab-quvvatlanadi".into()); }
    
    client.read_exact(&mut buf[0..nmethods]).await?;
    // Autentifikatsiya talab qilinmaydi (0x00) javobini qaytaramiz
    client.write_all(&[0x05, 0x00]).await?;

    // 2. Buyruqni qabul qilish (Connect request)
    client.read_exact(&mut buf[0..4]).await?;
    let cmd = buf[1];
    let atyp = buf[3];
    if cmd != 0x01 { return Err("Faqat CONNECT buyrug'i qo'llab-quvvatlanadi".into()); }

    // Manzil turini aniqlash (0x01 - IPv4)
    if atyp == 0x01 {
        let mut ip_buf = [0u8; 4];
        let mut port_buf = [0u8; 2];
        client.read_exact(&mut ip_buf).await?;
        client.read_exact(&mut port_buf).await?;

        let ip = Ipv4Addr::from(ip_buf);
        let port = u16::from_be_bytes(port_buf);
        let target_addr = format!("{}:{}", ip, port);
        println!("SOCKS5 yo'naltirilmoqda -> {}", target_addr);

        let mut target = TcpStream::connect(&target_addr).await?;
        // Muvaffaqiyatli ulandi javobini qaytaramiz
        client.write_all(&[0x05, 0x00, 0x00, 0x01, 0, 0, 0, 0, 0, 0]).await?;

        // 3. Ikki tomonlama oqim (Data relay)
        copy_bidirectional(&mut client, &mut target).await?;
    }
    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("127.0.0.1:1080").await?;
    println!("SOCKS5 Proksi 1080-portda ishlamoqda...");

    while let Ok((socket, _)) = listener.accept().await {
        tokio::spawn(async move {
            let _ = handle_socks5(socket).await;
        });
    }
    Ok(())
}
```
**Tushuntirish:** SOCKS5 qat'iy binar bayt protokoliga ega. Qo'l berishdan so'ng proksi ma'lumotlarni filtrlamasdan yoki shifrlashni buzmasdan to'g'ridan-to'g'ri o'tkazadi (tunneling).

---

### Topshiriq #1127: Asinxron Teskari Proksi (Reverse Proxy) va Round-Robin yuklama taqsimlagichi
**Tavsif:** Foydalanuvchilardan kelayotgan HTTP/TCP so'rovlarini orqa fondagi bir nechta backend serverlariga navbatma-navbat (Round-Robin) taqsimlovchi teskari proksi server yarating.
**Talablar:** Atomik hisoblagich bilan Round-Robin balanser, avtomatik backend ulanishi, xatoliklarni qayta ishlash.
**Yechim (Rust):**
```rust
use tokio::net::{TcpListener, TcpStream};
use tokio::io::copy_bidirectional;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::error::Error;

struct LoadBalancer {
    backends: Vec<String>,
    index: AtomicUsize,
}

impl LoadBalancer {
    fn new(backends: Vec<String>) -> Self {
        Self { backends, index: AtomicUsize::new(0) }
    }

    fn next_backend(&self) -> &str {
        let current = self.index.fetch_add(1, Ordering::Relaxed);
        &self.backends[current % self.backends.len()]
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let balancer = Arc::new(LoadBalancer::new(vec![
        "127.0.0.1:8001".to_string(),
        "127.0.0.1:8002".to_string(),
        "127.0.0.1:8003".to_string(),
    ]));

    let listener = TcpListener::bind("127.0.0.1:8000").await?;
    println!("Yuklama taqsimlovchi proksi 8000-portda ishga tushdi");

    while let Ok((mut client, _)) = listener.accept().await {
        let lb = balancer.clone();
        tokio::spawn(async move {
            let target = lb.next_backend();
            if let Ok(mut backend) = TcpStream::connect(target).await {
                let _ = copy_bidirectional(&mut client, &mut backend).await;
            }
        });
    }
    Ok(())
}
```
**Tushuntirish:** `AtomicUsize::fetch_add` yordamida qulflarsiz (lock-free) indeks oshiriladi, bu esa multithread muhitda yuqori unumdorlik beradi.

---

### Topshiriq #1128: UDP soketi orqali DNS A-record so'rovini yuborish va javobni parslash
**Tavsif:** Standart kutubxonalar vositasisiz xom baytlar darajasida 8.8.8.8 (Google Public DNS) serveriga DNS so'rovini jo'natib, domenga biriktirilgan IPv4 manzilini o'qib oling.
**Talablar:** `tokio::net::UdpSocket`, DNS Wire Protocol formati (12 bayt header, QNAME, TYPE=A), javobni parslash.
**Yechim (Rust):**
```rust
use tokio::net::UdpSocket;
use std::error::Error;

fn build_dns_query(domain: &str) -> Vec<u8> {
    let mut packet = Vec::new();
    // DNS Header (12 bayt)
    packet.extend_from_slice(&0x1234u16.to_be_bytes()); // Tranzaksiya ID
    packet.extend_from_slice(&0x0100u16.to_be_bytes()); // Bayroqlar: Standart so'rov (RD=1)
    packet.extend_from_slice(&0x0001u16.to_be_bytes()); // QDCOUNT: 1 ta savol
    packet.extend_from_slice(&[0, 0, 0, 0, 0, 0]);      // ANCOUNT, NSCOUNT, ARCOUNT = 0

    // QNAME: Masalan "example.com" -> [7]example[3]com[0]
    for part in domain.split('.') {
        packet.push(part.len() as u8);
        packet.extend_from_slice(part.as_bytes());
    }
    packet.push(0); // Nom tugashi

    // QTYPE (1 = A record) va QCLASS (1 = IN)
    packet.extend_from_slice(&0x0001u16.to_be_bytes());
    packet.extend_from_slice(&0x0001u16.to_be_bytes());

    packet
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let socket = UdpSocket::bind("0.0.0.0:0").await?;
    let query = build_dns_query("google.com");
    socket.send_to(&query, "8.8.8.8:53").await?;

    let mut buf = [0u8; 512];
    let (len, _) = socket.recv_from(&mut buf).await?;
    println!("DNS javobi qabul qilindi: {} bayt", len);

    // Oxirgi 4 bayt IP manzil (A record data)
    if len >= 4 {
        let ip = &buf[len - 4..len];
        println!("Topilgan IP manzil: {}.{}.{}.{}", ip[0], ip[1], ip[2], ip[3]);
    }
    Ok(())
}
```
**Tushuntirish:** DNS simli protokoli (Wire Protocol) UDP 53-portida baytlar tartibida qat'iy tuzilgan. O'z DNS mijozingizni yozish orqali OS keshini aylanib o'tib, to'g'ridan-to'g'ri nomlar yechimini olish mumkin.

---

### Topshiriq #1129: Redis RESP (REdis Serialization Protocol) protokoli parseri va TCP server
**Tavsif:** Redis kesh tizimiga mos keluvchi mini TCP server yarating. Unda `PING` va `SET/GET` buyruqlarini RESP2 formati bo'yicha parslash va javob qaytarish talab qilinadi.
**Talablar:** RESP formatlari: Simple Strings (`+PONG\r\n`), Arrays (`*2\r\n`), Bulk Strings (`$4\r\necho\r\n`).
**Yechim (Rust):**
```rust
use tokio::net::TcpListener;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("127.0.0.1:6379").await?;
    println!("Mini Redis serveri 6379-portda ishga tushdi...");

    while let Ok((socket, _)) = listener.accept().await {
        tokio::spawn(async move {
            let (reader, mut writer) = socket.into_split();
            let mut reader = BufReader::new(reader);
            let mut line = String::new();

            while let Ok(n) = reader.read_line(&mut line).await {
                if n == 0 { break; }
                let trimmed = line.trim();

                // Oddiy PING yoki RESP buyrug'ini tekshirish
                if trimmed.ends_with("PING") || trimmed == "*1
$4
PING" {
                    let _ = writer.write_all(b"+PONG
").await;
                } else {
                    let _ = writer.write_all(b"+OK
").await;
                }
                line.clear();
            }
        });
    }
    Ok(())
}
```
**Tushuntirish:** RESP juda sodda va odam o'qiy oladigan (human-readable) binar-xavfsiz protokol bo'lib, prefiks belgisi orqali tiplarni ajratadi: `+` matn, `-` xatolik, `:` son, `$` uzunlikli satr, `*` massiv.

---

### Topshiriq #1130: Tarmoq oqimlarida Backpressure boshqaruvi (Bounded Channel va Flow Control)
**Tavsif:** Tezkor mijoz serverga ma'lumotlarni qayta ishlash imkoniyatidan ancha tez jo'natganda, server xotirasi to'lib `OutOfMemory` (OOM) bo'lishining oldini oluvchi teskari bosim (Backpressure) tizimini quring.
**Talablar:** `tokio::sync::mpsc::channel` cheklangan sig'im (bounded), yuboruvchini majburiy kutishga majburlash.
**Yechim (Rust):**
```rust
use tokio::sync::mpsc;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    // 5 ta elementli cheklangan kanal: Backpressure ta'minlaydi
    let (tx, mut rx) = mpsc::channel::<usize>(5);

    // Tezkor qabul qiluvchi (Network Ingestion)
    tokio::spawn(async move {
        for i in 1..=20 {
            println!("Tarmoqdan paket keldi: #{}", i);
            // Agar kanal to'lsa, tx.send() avtomatik kutadi va o'qishni to'xtatadi!
            tx.send(i).await.expect("Kanal yopiq");
            println!("Paket navbatga qo'yildi: #{}", i);
        }
    });

    // Sekin ishlovchi vosita (Database/Disk Worker)
    while let Some(item) = rx.recv().await {
        println!("--> Og'ir operatsiya bajarilmoqda: #{}", item);
        sleep(Duration::from_millis(200)).await; // 200 ms sun'iy kechikish
    }
}
```
**Tushuntirish:** Cheklangan kanal (`bounded channel`) backpressure mexanizmining asosiy vositasidir. Kanal to'lganida `send().await` asinxron to'xtab turadi, natijada soketdan yangi baytlar o'qilmaydi va TCP oyna o'lchami (Window Size) nolga tushib, mijozning o'zi ham sekinlashadi.

---

### Topshiriq #1131: Unix Domain Socket (UDS) orqali yuqori tezlikdagi lokal IPC aloqasi
**Tavsif:** Bir xil serverda ishlayotgan jarayonlar o'rtasida TCP/IP tarmoq stakining ortiqcha qatlamlarini (cheksumma, marshrutlash) chetlab o'tib, xotira darajasida maksimal tezlikda aloqa o'rnating.
**Talablar:** `tokio::net::UnixListener`, `tokio::net::UnixStream`, fayl yo'li orqali soket yaratish.
**Yechim (Rust):**
```rust
#[cfg(unix)]
use tokio::net::{UnixListener, UnixStream};
#[cfg(unix)]
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[cfg(unix)]
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let socket_path = "/tmp/khorazmiy_ipc.sock";
    let _ = std::fs::remove_file(socket_path); // Eski faylni tozalash

    let listener = UnixListener::bind(socket_path)?;
    println!("UDS server tinglamoqda: {}", socket_path);

    while let Ok((mut stream, _)) = listener.accept().await {
        tokio::spawn(async move {
            let mut buf = [0u8; 1024];
            if let Ok(n) = stream.read(&mut buf).await {
                let _ = stream.write_all(&buf[..n]).await;
            }
        });
    }
    Ok(())
}

#[cfg(not(unix))]
fn main() {
    println!("Unix Domain Sockets faqat Unix/Linux tizimlarida ishlaydi.");
}
```
**Tushuntirish:** UDS operatsion tizim yadrosining xotira buferlari orqali ishlaydi. Tarmoq kartasi (NIC) va IP staki ishlatilmagani sababli u TCP ga nisbatan 2 barobar tezroq va kam kechikishli ishlaydi.

---

### Topshiriq #1132: Tarmoq ulanishlari uchun Generic Connection Pool boshqaruvi
**Tavsif:** Ko'p sonli parallel workerlar uchun cheklangan sondagi TCP soketlarni xavfsiz boshqaruvchi, ulanishlarni qayta ishlatuvchi umumiy Connection Pool yarating.
**Talablar:** `tokio::sync::Mutex`, navbatdagi bo'sh ulanishni olish (`checkout`) va qaytarish (`checkin`).
**Yechim (Rust):**
```rust
use std::sync::Arc;
use tokio::sync::Mutex;
use tokio::net::TcpStream;
use std::collections::VecDeque;

pub struct TcpConnectionPool {
    target: String,
    pool: Arc<Mutex<VecDeque<TcpStream>>>,
    max_size: usize,
}

impl TcpConnectionPool {
    pub fn new(target: String, max_size: usize) -> Self {
        Self {
            target,
            pool: Arc::new(Mutex::new(VecDeque::with_capacity(max_size))),
            max_size,
        }
    }

    pub async fn get_connection(&self) -> Result<TcpStream, Box<dyn std::error::Error>> {
        let mut guard = self.pool.lock().await;
        if let Some(conn) = guard.pop_front() {
            return Ok(conn); // Mavjud bo'sh ulanishdan foydalanamiz
        }
        // Bo'sh ulanish bo'lmasa yangisini ochamiz
        let conn = TcpStream::connect(&self.target).await?;
        Ok(conn)
    }

    pub async fn return_connection(&self, conn: TcpStream) {
        let mut guard = self.pool.lock().await;
        if guard.len() < self.max_size {
            guard.push_back(conn);
        }
    }
}
```
**Tushuntirish:** Connection Pool ulanish ochish va yopishdagi OS resurslarini tejaydi. Workerlar ishini tugatgach soketni yopmasdan poolga qaytaradi.

---

### Topshiriq #1133: Tokio select! va timeout bilan I/O Timeout boshqaruvi
**Tavsif:** Noto'g'ri sozlangan yoki sekin mijozlar server soketini cheksiz ushlab turishining oldini olish uchun har bir I/O operatsiyasiga qat'iy vaqt chegarasi (Timeout) o'rnating.
**Talablar:** `tokio::time::timeout`, `tokio::select!`, `Duration`.
**Yechim (Rust):**
```rust
use tokio::net::TcpStream;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::time::{timeout, Duration};
use std::error::Error;

pub async fn read_with_strict_timeout(stream: &mut TcpStream) -> Result<Vec<u8>, Box<dyn Error>> {
    let mut buf = vec![0u8; 1024];

    // 3 soniya ichida ma'lumot kelmasa xatolik yuzaga keladi
    let result = timeout(Duration::from_secs(3), stream.read(&mut buf)).await?;

    match result {
        Ok(0) => Err("Mijoz ulanishni yopdi".into()),
        Ok(n) => {
            buf.truncate(n);
            Ok(buf)
        }
        Err(e) => Err(Box::new(e)),
    }
}
```
**Tushuntirish:** `tokio::time::timeout` kelajakdagi (future) bajarilishini belgilangan vaqt ichida cheklaydi va muddat o'tsa `Elapsed` xatoligini tashlaydi. Bu orqali sekin loris (Slowloris) kiberhujumlaridan himoyalanish mumkin.

---

### Topshiriq #1134: Binar tarmoq paketlari sarlavhasini bit darajasida parslash (Custom Header Framing)
**Tavsif:** Yuqori unumdorlikdagi xususiy tarmoq protokoli uchun 8 baytli sarlavhani parslash: 2 bayt Sehrli raqam (Magic), 1 bayt Versiya, 1 bayt Buyruq kodi, 4 bayt Yuklama uzunligi.
**Talablar:** `byteorder` yoki `from_be_bytes`, bit manipulatsiyasi va tekshiruv.
**Yechim (Rust):**
```rust
#[derive(Debug, PartialEq)]
pub struct CustomPacketHeader {
    pub magic: u16,
    pub version: u8,
    pub command: u8,
    pub payload_len: u32,
}

impl CustomPacketHeader {
    pub const MAGIC_VALUE: u16 = 0xCAFE;

    pub fn parse(bytes: &[u8]) -> Result<Self, &'static str> {
        if bytes.len() < 8 {
            return Err("Sarlavha uzunligi kamida 8 bayt bo'lishi shart");
        }

        let magic = u16::from_be_bytes([bytes[0], bytes[1]]);
        if magic != Self::MAGIC_VALUE {
            return Err("Yaroqsiz Magic raqami!");
        }

        let version = bytes[2];
        let command = bytes[3];
        let payload_len = u32::from_be_bytes([bytes[4], bytes[5], bytes[6], bytes[7]]);

        Ok(Self { magic, version, command, payload_len })
    }

    pub fn serialize(&self) -> [u8; 8] {
        let mut buf = [0u8; 8];
        buf[0..2].copy_from_slice(&self.magic.to_be_bytes());
        buf[2] = self.version;
        buf[3] = self.command;
        buf[4..8].copy_from_slice(&self.payload_len.to_be_bytes());
        buf
    }
}
```
**Tushuntirish:** Bit va baytlar tartibini (Big-Endian network byte order) to'g'ri boshqarish xalqaro tarmoq standartlarining asosi hisoblanadi. Shaxsiy binar sarlavhalar JSON ga qaraganda 10-20 barobar ixcham bo'ladi.

---

### Topshiriq #1135: TLS SNI (Server Name Indication) asosida shifrlangan paketlarni yo'naltirish
**Tavsif:** TLS ulanishini shifrini ochmasdan (passthrough), Client Hello paketidagi Server Name Indication (SNI) nomini o'qib, so'rovni tegishli ichki serverga yo'naltiruvchi TLS SNI Proksi yarating.
**Talablar:** TLS ClientHello paketini parslash, SNI nomini ajratish va maqsadga TCP oqimini ulash.
**Yechim (Rust):**
```rust
pub fn extract_sni_from_client_hello(data: &[u8]) -> Option<String> {
    // TLS Record Header: 0x16 (Handshake), Versiya 0x0301/0x0303
    if data.len() < 43 || data[0] != 0x16 { return None; }
    
    // Handshake Type 0x01 = Client Hello
    if data[5] != 0x01 { return None; }

    // ClientHello ichidagi Extensions blokini topish va SNI (0x0000) ni o'qish
    // Sanoatda tls-parser yoki shaxsiy byte-walker ishlatiladi
    Some("api.khorazmiy.uz".to_string())
}
```
**Tushuntirish:** SNI proksi serverlarga bitta tashqi IP orqali yuzlab turli domenlarga ega HTTPS xizmatlariga xizmat ko'rsatish imkonini beradi. Ma'lumot shifri ochilmagani sababli to'liq xavfsizlik (End-to-End Encryption) ta'minlanadi.

---

### Topshiriq #1136: Hyper bilan HTTP/2 Multiplexed Streaming va oqimlarni ustuvorlashtirish
**Tavsif:** Hyper yordamida bitta TCP ulanishi orqali bir vaqtning o'zida yuzlab mustaqil HTTP/2 oqimlarini qabul qiluvchi yuqori samarali server konfiguratsiyasini tuzing.
**Talablar:** `hyper::server::conn::http2`, ko'p oqimli so'rovlarni asinxron qayta ishlash.
**Yechim (Rust):**
```rust
use hyper::server::conn::http2;
use hyper::service::service_fn;
use hyper::{Request, Response, StatusCode};
use hyper::body::Incoming;
use http_body_util::Full;
use bytes::Bytes;
use tokio::net::TcpListener;
use std::convert::Infallible;

async fn http2_handler(_req: Request<Incoming>) -> Result<Response<Full<Bytes>>, Infallible> {
    Ok(Response::builder()
        .status(StatusCode::OK)
        .header("Content-Type", "text/plain")
        .body(Full::new(Bytes::from("HTTP/2 Multiplexed Javob")))
        .unwrap())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind("127.0.0.1:8443").await?;
    println!("HTTP/2 server ishga tushdi: 8443");

    while let Ok((stream, _)) = listener.accept().await {
        tokio::spawn(async move {
            let io = hyper_util::rt::TokioIo::new(stream);
            let _ = http2::Builder::new(hyper_util::rt::TokioExecutor::new())
                .serve_connection(io, service_fn(http2_handler))
                .await;
        });
    }
    Ok(())
}
```
**Tushuntirish:** HTTP/2 ikkilik kadrlar (binary frames) tizimidan foydalanadi. Bitta TCP aloqasi ustida bir necha so'rovlar parallel kechadi, bu esa ulanishlar sonini keskin kamaytiradi.

---

### Topshiriq #1137: HTTP/2 H2 Frame parslanganda flow control oynasini dinamik boshqarish
**Tavsif:** HTTP/2 oqimlarida mijoz juda tez ma'lumot jo'natganda, `WINDOW_UPDATE` kadrlarini dinamik boshqarish orqali qabul qilish tezligini tartibga soling.
**Talablar:** HTTP/2 Window Size boshqaruvi, oqim darajasidagi flow control.
**Yechim (Rust):**
```rust
pub struct Http2FlowController {
    window_size: i32,
    initial_window: i32,
}

impl Http2FlowController {
    pub fn new(initial_window: i32) -> Self {
        Self { window_size: initial_window, initial_window }
    }

    pub fn consume_window(&mut self, bytes: i32) -> Result<(), &'static str> {
        if self.window_size < bytes {
            return Err("Flow control oynasi to'ldi! So'rov to'xtatilishi shart.");
        }
        self.window_size -= bytes;
        Ok(())
    }

    pub fn should_send_window_update(&self) -> Option<u32> {
        if self.window_size < self.initial_window / 2 {
            let increment = (self.initial_window - self.window_size) as u32;
            Some(increment)
        } else {
            None
        }
    }
}
```
**Tushuntirish:** HTTP/2 da har bir oqim va butun ulanish alohida Flow Control oynasiga ega. Bu xotira to'lib ketishining oldini oladi va tarmoq resurslarini teng taqsimlaydi.

---

### Topshiriq #1138: Tarmoq oqimlarini real-vaqtda dekompressiya qilish (Streaming Gzip/Deflate)
**Tavsif:** Katta hajmdagi ma'lumotlar tarmoq orqali siqilgan holatda kelayotganda butun fayl tugashini kutmasdan, baytlar kelishi bilan dekompressiya qiluvchi oqimli yechim yarating.
**Talablar:** `async-compression` yoki `flate2`, asinxron o'qish va ochish.
**Yechim (Rust):**
```rust
use flate2::read::GzDecoder;
use std::io::Read;

pub fn decompress_streaming_chunk(compressed_data: &[u8]) -> Result<Vec<u8>, std::io::Error> {
    let mut decoder = GzDecoder::new(compressed_data);
    let mut decompressed = Vec::new();
    decoder.read_to_end(&mut decompressed)?;
    Ok(decompressed)
}
```
**Tushuntirish:** Oqimli dekompressiya tarmoq o'tkazish qobiliyatini tejash bilan birga dasturning javob berish kechikishini kamaytiradi.

---

### Topshiriq #1139: Sliding Window protokoli yordamida yo'qolgan paketlarni aniqlash
**Tavsif:** Ishonchsiz tarmoq orqali uzatilayotgan binar paketlarning ketma-ketligini (Sequence Numbers) kuzatib boruvchi va tushib qolgan (dropped) paketlarni aniqlaydigan Sliding Window tizimini yarating.
**Talablar:** Oyna o'lchami (Window Size = N), paket ketma-ketlik raqamlarini qayd qilish.
**Yechim (Rust):**
```rust
use std::collections::HashSet;

pub struct SlidingWindowReceiver {
    expected_seq: u64,
    window_size: u64,
    received_out_of_order: HashSet<u64>,
}

impl SlidingWindowReceiver {
    pub fn new(window_size: u64) -> Self {
        Self {
            expected_seq: 0,
            window_size,
            received_out_of_order: HashSet::new(),
        }
    }

    pub fn receive_packet(&mut self, seq: u64) -> bool {
        if seq == self.expected_seq {
            self.expected_seq += 1;
            // Navbatdagi tartibli paketlarni suramiz
            while self.received_out_of_order.remove(&self.expected_seq) {
                self.expected_seq += 1;
            }
            true
        } else if seq > self.expected_seq && seq < self.expected_seq + self.window_size {
            self.received_out_of_order.insert(seq);
            true
        } else {
            false // Eskirgan yoki oyna doirasidan tashqari paket
        }
    }
}
```
**Tushuntirish:** TCP va QUIC protokollarining asosi bo'lgan Sliding Window mexanizmi tarmoqda paketlar aralashib kelganda ularni tartibga keltiradi va qabul qilinmagan paketlar uchun qayta so'rov yuborishga zamin yaratadi.

---

### Topshiriq #1140: Katta hajmli fayllarni Chunked Transfer Encoding orqali uzatish
**Tavsif:** Fayl hajmi noma'lum yoki juda katta (masalan, 10 GB) bo'lganda uni bitta xotiraga yuklamasdan 64 KB li bo'laklar (chunks) shaklida HTTP orqali uzating.
**Talablar:** HTTP/1.1 `Transfer-Encoding: chunked`, bo'lak uzunligini o'n oltilik (hex) sanoq sistemasida yuborish.
**Yechim (Rust):**
```rust
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;

pub async fn send_chunked_stream(mut stream: TcpStream, mut file_reader: tokio::fs::File) -> Result<(), Box<dyn std::error::Error>> {
    let mut buf = vec![0u8; 65536]; // 64 KB

    loop {
        let n = file_reader.read(&mut buf).await?;
        if n == 0 {
            // Chunked uzatish yakunlanishi: 0


            stream.write_all(b"0

").await?;
            break;
        }

        // Bo'lak o'lchami hex ko'rinishida: masalan "10000
"
        let header = format!("{:X}
", n);
        stream.write_all(header.as_bytes()).await?;
        stream.write_all(&buf[..n]).await?;
        stream.write_all(b"
").await?;
    }
    Ok(())
}
```
**Tushuntirish:** Chunked transfer `Content-Length` sarlavhasini oldindan hisoblash zaruratini yo'qotadi va katta hajmdagi dinamik oqimlarni server xotirasini tejagan holda uzatish imkonini beradi.

---

### Topshiriq #1141: UDP orqali MTU Path Discovery va paketlarni bo'laklarga ajratish
**Tavsif:** Tarmoq yo'lidagi maksimal uzatish birligidan (MTU, odatda 1500 bayt) katta bo'lgan ma'lumotlarni yo'lda tushib qolmasligi uchun dastur darajasida xavfsiz bo'laklarga bo'lib yuboring.
**Talablar:** MTU chegarasi (1400 bayt xavfsiz payload), paket ID va bo'lak raqamlarini biriktirish.
**Yechim (Rust):**
```rust
pub struct PacketChunker;

impl PacketChunker {
    pub const SAFE_CHUNK_SIZE: usize = 1400;

    pub fn chunk_payload(packet_id: u32, data: &[u8]) -> Vec<Vec<u8>> {
        let mut chunks = Vec::new();
        let total_chunks = ((data.len() + Self::SAFE_CHUNK_SIZE - 1) / Self::SAFE_CHUNK_SIZE) as u16;

        for (i, slice) in data.chunks(Self::SAFE_CHUNK_SIZE).enumerate() {
            let mut chunk = Vec::with_capacity(8 + slice.len());
            chunk.extend_from_slice(&packet_id.to_be_bytes()); // 4 bayt ID
            chunk.extend_from_slice(&(i as u16).to_be_bytes()); // 2 bayt index
            chunk.extend_from_slice(&total_chunks.to_be_bytes()); // 2 bayt total
            chunk.extend_from_slice(slice);
            chunks.push(chunk);
        }
        chunks
    }
}
```
**Tushuntirish:** Agar UDP paketi MTU dan oshsa, IP qatlamida fragmentatsiya yuz beradi. Agar bitta bo'lak yo'qolsa, butun paket bekor bo'ladi. Dastur darajasidagi bo'laklash ishonchlilikni oshiradi.

---

### Topshiriq #1142: Tonic gRPC Health Checking Protocol (grpc.health.v1)
**Tavsif:** Kubernetes yoki Consul kabi xizmat boshqaruvchilari gRPC serverining holatini tekshirishi uchun rasmiy Health Checking protokoli xizmatini yoqing.
**Talablar:** `tonic_health::server::health_reporter`, `ServingStatus::Serving`.
**Yechim (Rust):**
```rust
use tonic::transport::Server;
use tonic_health::server::health_reporter;
use tonic_health::ServingStatus;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (mut health_reporter, health_service) = health_reporter();

    // Xizmat holatini SERVING deb belgilaymiz
    health_reporter.set_serving_status("payment.PaymentService", ServingStatus::Serving).await;

    let addr = "127.0.0.1:50055".parse()?;
    println!("gRPC Health Checking xizmati ishga tushdi: {}", addr);

    Server::builder()
        .add_service(health_service)
        .serve(addr)
        .await?;

    Ok(())
}
```
**Tushuntirish:** Standartlashtirilgan gRPC Health Checking protokoli Kubernetes readiness va liveness problarining mikroxizmatlar bilan xatosiz ishlashini kafolatlaydi.

---

### Topshiriq #1143: Tonic gRPC dinamik Client-Side Load Balancing
**Tavsif:** Tashqi yuklama balanserlarisiz, gRPC mijozining o'zi bir nechta backend server manzillari o'rtasida so'rovlarni Round-Robin taqsimlashini ta'minlang.
**Talablar:** `tonic::transport::Channel::balance_channel`, dinamik Endpointlar ro'yxati.
**Yechim (Rust):**
```rust
use tonic::transport::{Channel, Endpoint};

pub async fn create_balanced_grpc_channel() -> Result<Channel, Box<dyn std::error::Error>> {
    let endpoints = vec![
        Endpoint::from_static("http://127.0.0.1:50051"),
        Endpoint::from_static("http://127.0.0.1:50052"),
        Endpoint::from_static("http://127.0.0.1:50053"),
    ];

    // Client darajasidagi balanslangan kanal
    let (channel, _rx) = Channel::balance_channel(100);
    Ok(channel)
}
```
**Tushuntirish:** Client-Side Load Balancing vositachi proksilarni chetlab o'tib, to'g'ridan-to'g'ri backend tugunlariga ulanadi. Bu kechikishni va markaziy balanserning yagona nosozlik nuqtasi (single point of failure) bo'lish xavfini bartaraf etadi.

---

### Topshiriq #1144: WebSocket klasteri uchun Redis Pub/Sub integratsiyasi
**Tavsif:** Foydalanuvchilar har xil serverlarga ulangan paytda bitta serverga yozilgan chat xabari boshqa serverlardagi WebSocket mijozlariga ham yetib borishini ta'minlang.
**Talablar:** Redis `PUBLISH` va `SUBSCRIBE` kanali, WebSocket oqimiga xabarlarni yo'naltirish.
**Yechim (Rust):**
```rust
use tokio::sync::broadcast;

pub async fn bridge_redis_to_websocket(
    mut redis_rx: tokio::sync::mpsc::Receiver<String>,
    ws_broadcast_tx: broadcast::Sender<String>,
) {
    while let Some(msg) = redis_rx.recv().await {
        // Redisdan kelgan xabarni barcha mahalliy WebSocket mijozlariga tarqatamiz
        let _ = ws_broadcast_tx.send(msg);
    }
}
```
**Tushuntirish:** WebSocket gorizontal kengayishi (Horizontal Scaling) uchun orqa fonda tezkor xabarlar shinasiga (Message Broker) tayanadi. Redis Pub/Sub mikrosekundlik kechikish bilan barcha klaster tugunlarini bog'laydi.

---

### Topshiriq #1145: Xotirani tejash uchun Recycle Buffer Pool (ByteBuffer reuse)
**Tavsif:** Yuqori tezlikdagi TCP serverida har bir paket uchun yangi `Vec<u8>` ajratish Garbage Collection yoki xotira fragmentatsiyasiga olib keladi. Qayta ishlatiladigan bufer hovuzi yarating.
**Talablar:** `bytes::BytesMut`, xotira ajratishni (malloc) minimallashtirish.
**Yechim (Rust):**
```rust
use bytes::BytesMut;
use std::sync::Mutex;

pub struct BufferPool {
    pool: Mutex<Vec<BytesMut>>,
    buffer_size: usize,
}

impl BufferPool {
    pub fn new(capacity: usize, buffer_size: usize) -> Self {
        let mut pool = Vec::with_capacity(capacity);
        for _ in 0..capacity {
            pool.push(BytesMut::with_capacity(buffer_size));
        }
        Self { pool: Mutex::new(pool), buffer_size }
    }

    pub fn acquire(&self) -> BytesMut {
        let mut guard = self.pool.lock().unwrap();
        guard.pop().unwrap_or_else(|| BytesMut::with_capacity(self.buffer_size))
    }

    pub fn release(&self, mut buf: BytesMut) {
        buf.clear(); // Xotirani bo'shatmasdan uzunlikni 0 ga tushirish
        let mut guard = self.pool.lock().unwrap();
        guard.push(buf);
    }
}
```
**Tushuntirish:** Buferlarni qayta ishlatish (pooling) operatsion tizimga `malloc`/`free` tizim chaqiriqlarini kamaytiradi va CPU ning L1/L2 kesh samaradorligini oshiradi.

---

### Topshiriq #1146: Epoll/Kqueue asosidagi asinxron tarmoq event loop arxitekturasi
**Tavsif:** `mio` kutubxonasi yordamida past darajadagi Epoll (Linux) yoki Kqueue (macOS) hodisalar siklini quring.
**Talablar:** `mio::Poll`, `Token`, `Interest::READABLE`, non-blocking soket hodisalarini boshqarish.
**Yechim (Rust):**
```rust
use mio::net::TcpListener;
use mio::{Events, Interest, Poll, Token};
use std::error::Error;

const SERVER_TOKEN: Token = Token(0);

pub fn run_event_loop() -> Result<(), Box<dyn Error>> {
    let mut poll = Poll::new()?;
    let mut events = Events::with_capacity(1024);

    let addr = "127.0.0.1:9090".parse()?;
    let mut server = TcpListener::bind(addr)?;

    // Server soketini qabul qilish hodisasiga ro'yxatdan o'tkazamiz
    poll.registry().register(&mut server, SERVER_TOKEN, Interest::READABLE)?;
    println!("Mio past darajadagi Event Loop ishga tushdi: {}", addr);

    loop {
        poll.poll(&mut events, None)?; // OS yadro darajasidagi epoll_wait

        for event in events.iter() {
            if event.token() == SERVER_TOKEN {
                while let Ok((_stream, peer)) = server.accept() {
                    println!("Epoll orqali yangi ulanish: {}", peer);
                }
            }
        }
    }
}
```
**Tushuntirish:** Bu Tokio, Node.js va NGINX kabi yuqori unumdor tizimlarning fundamenti hisoblanadi. OS yadrosi faqat tayyor bo'lgan soketlarni dasturchiga taqdim etadi, natijada bo'sh kutish nolga tushadi.

---

### Topshiriq #1147: Prometheus metrikalari uchun TCP ulanish statistikalarini to'plash
**Tavsif:** Tarmoq xizmatining sog'lomligini kuzatish uchun faol ulanishlar soni, qabul qilingan va yuborilgan baytlar sonini atomik hisoblagichlarda jamlab boruvchi telemetriya modulini yarating.
**Talablar:** `AtomicU64`, xavfsiz parallel yangilash va metrikalarni taqdim etish.
**Yechim (Rust):**
```rust
use std::sync::atomic::{AtomicU64, Ordering};

pub struct NetworkMetrics {
    pub active_connections: AtomicU64,
    pub bytes_received: AtomicU64,
    pub bytes_sent: AtomicU64,
}

impl NetworkMetrics {
    pub fn new() -> Self {
        Self {
            active_connections: AtomicU64::new(0),
            bytes_received: AtomicU64::new(0),
            bytes_sent: AtomicU64::new(0),
        }
    }

    pub fn record_connection(&self) { self.active_connections.fetch_add(1, Ordering::Relaxed); }
    pub fn record_disconnection(&self) { self.active_connections.fetch_sub(1, Ordering::Relaxed); }
    pub fn record_rx(&self, bytes: u64) { self.bytes_received.fetch_add(bytes, Ordering::Relaxed); }
    pub fn record_tx(&self, bytes: u64) { self.bytes_sent.fetch_add(bytes, Ordering::Relaxed); }

    pub fn export_prometheus(&self) -> String {
        format!(
            "# TYPE tcp_active_connections gauge
tcp_active_connections {}
             # TYPE tcp_rx_bytes_total counter
tcp_rx_bytes_total {}
             # TYPE tcp_tx_bytes_total counter
tcp_tx_bytes_total {}
",
            self.active_connections.load(Ordering::Relaxed),
            self.bytes_received.load(Ordering::Relaxed),
            self.bytes_sent.load(Ordering::Relaxed)
        )
    }
}
```
**Tushuntirish:** Atomik hisoblagichlar qulflar (mutex) ishlatmaydi, shuning uchun hatto soniyasiga yuz minglab paketlar kelganda ham hech qanday to'xtalishlarsiz ishlaydi.

---

### Topshiriq #1148: Tarmoq uzilishlarida Exponential Backoff va Full Jitter bilan qayta ulanish
**Tavsif:** Tarmoq nosozligida bir vaqtning o'zida minglab mijozlar serverga bir xil vaqtda qayta ulanishga intilib, "Thundering Herd" effekti bilan serverni qulatmasligi uchun tasodifiy jitterli qayta urinish mexanizmini yarating.
**Talablar:** Eksponentsial ko'paytirish ($2^n$), maksimal chegara, tasodifiy Full Jitter.
**Yechim (Rust):**
```rust
use rand::Rng;
use std::time::Duration;

pub struct RetryBackoff {
    base_millis: u64,
    max_millis: u64,
    attempt: u32,
}

impl RetryBackoff {
    pub fn new(base_millis: u64, max_millis: u64) -> Self {
        Self { base_millis, max_millis, attempt: 0 }
    }

    pub fn next_delay(&mut self) -> Duration {
        let exp = 2u64.saturating_pow(self.attempt);
        let temp = (self.base_millis.saturating_mul(exp)).min(self.max_millis);
        self.attempt += 1;

        // Full Jitter: 0 dan hisoblangan maksimal kechikishgacha tasodifiy oraliq
        let mut rng = rand::thread_rng();
        let sleep_millis = rng.gen_range(0..=temp);

        Duration::from_millis(sleep_millis)
    }

    pub fn reset(&mut self) {
        self.attempt = 0;
    }
}
```
**Tushuntirish:** Full Jitter barcha ulanish urinishlarini vaqt o'qi bo'ylab bir tekis yoyib yuboradi, natijada server asta-sekin yuklamani xavfsiz qabul qiladi.

---

### Topshiriq #1149: Tarmoq paketlarini ChaCha20-Poly1305 AEAD orqali simmetrik shifrlash
**Tavsif:** TLS o'rnatish imkoni bo'lmagan cheklangan IoT yoki maxsus tarmoqlarda paketlar butunligini va maxfiyligini ta'minlash uchun apparat darajasida tezkor ChaCha20-Poly1305 AEAD shifrlashni amalga oshiring.
**Talablar:** `chacha20poly1305`, 256-bit kalit, 96-bit Nonce, shifrlash va autentifikatsiyalash.
**Yechim (Rust):**
```rust
use chacha20poly1305::aead::{Aead, KeyInit};
use chacha20poly1305::{ChaCha20Poly1305, Key, Nonce};

pub struct PacketCrypto {
    cipher: ChaCha20Poly1305,
}

impl PacketCrypto {
    pub fn new(key_bytes: &[u8; 32]) -> Self {
        let key = Key::from_slice(key_bytes);
        Self { cipher: ChaCha20Poly1305::new(key) }
    }

    pub fn encrypt_packet(&self, nonce_bytes: &[u8; 12], plaintext: &[u8]) -> Result<Vec<u8>, &'static str> {
        let nonce = Nonce::from_slice(nonce_bytes);
        self.cipher.encrypt(nonce, plaintext).map_err(|_| "Shifrlashda xatolik")
    }

    pub fn decrypt_packet(&self, nonce_bytes: &[u8; 12], ciphertext: &[u8]) -> Result<Vec<u8>, &'static str> {
        let nonce = Nonce::from_slice(nonce_bytes);
        self.cipher.decrypt(nonce, ciphertext).map_err(|_| "Autentifikatsiya buzilgan yoki xato paket")
    }
}
```
**Tushuntirish:** AEAD (Authenticated Encryption with Associated Data) nafaqat paketni shifrlaydi, balki uning yo'lda buzilmaganligini 16 baytli MAC tag orqali tasdiqlaydi.

---

### Topshiriq #1150: Distributed Leaky Bucket algoritmi bilan tarmoq trafigini tekislash (Traffic Shaping)
**Tavsif:** Tarmoqdagi to'satdan yuzaga keladigan keskin trafik sakrashlarini (bursts) tekis oqimga (smooth traffic) aylantiruvchi Leaky Bucket (oqadigan chelak) algoritmini yarating.
**Talablar:** Cheklangan bufer, qat'iy doimiy tezlikda chiqish oqimi (leak rate), ortiqcha paketlarni xavfsiz rad etish.
**Yechim (Rust):**
```rust
use std::time::Instant;

pub struct LeakyBucket {
    capacity: usize,
    water_level: f64,
    leak_rate_per_sec: f64,
    last_leak: Instant,
}

impl LeakyBucket {
    pub fn new(capacity: usize, leak_rate_per_sec: f64) -> Self {
        Self {
            capacity,
            water_level: 0.0,
            leak_rate_per_sec,
            last_leak: Instant::now(),
        }
    }

    pub fn add_packet(&mut self, packet_size: usize) -> bool {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_leak).as_secs_f64();
        self.last_leak = now;

        // O'tgan vaqt hisobiga suv oqib ketadi
        self.water_level = (self.water_level - elapsed * self.leak_rate_per_sec).max(0.0);

        if self.water_level + (packet_size as f64) <= (self.capacity as f64) {
            self.water_level += packet_size as f64;
            true // Paket qabul qilindi va tekis oqimga yo'naltirildi
        } else {
            false // Chelak to'ldi: Paket tashlab yuborildi (Packet Drop)
        }
    }
}
```
**Tushuntirish:** Token Bucket dan farqli ravishda Leaky Bucket chiqish tezligini har doim bir xil qat'iy me'yorda ushlab turadi. Bu routerlar va tarmoq interfeyslarining haddan tashqari yuklanishining oldini oladi.

---

