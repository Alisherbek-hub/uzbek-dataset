# Khorazmiy AI: Go - Modul 23
## Mavzu: Tarmoq protokollari: TCP/UDP soketlari, HTTP/3, QUIC, gRPC va WebSockets (Go net/http, quic-go, gorilla/websocket)

Salom, men **Khorazmiy AI** loyihasining Go va yuqori yuklamali tarmoq dasturlash bo'yicha bosh dataset mutaxassisiman. Ushbu modulda Go tilining tarmoq imkoniyatlari, `net` paketi, HTTP/1.1, HTTP/2, HTTP/3, QUIC, gRPC mikroservislari hamda WebSockets texnologiyalariga oid 50 ta chuqur sanoat darajasidagi amaliy topshiriq va ularning to'liq yechimlari taqdim etiladi.

---
### Topshiriq #1101: net.Listen yordamida Asinxron TCP Echo Server
**Tavsif:** Real vaqt rejimida o'n minglab parallel mijozlarni qabul qila oladigan, xotira sarfi minimal va har bir ulanishni alohida goroutinada xizmat ko'rsatuvchi TCP Echo server quring.
**Talablar:** `net.Listen`, har bir mijoz uchun alohida goroutina, xatoliklarni xavfsiz boshqarish va resurslarni `defer` bilan tozalash.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"io"
	"log"
	"net"
)

// Mijoz ulanishini qayta ishlovchi funksiya
func handleConnection(conn net.Conn) {
	defer conn.Close()
	remoteAddr := conn.RemoteAddr().String()
	fmt.Printf("[+] Yangi mijoz ulandi: %s\n", remoteAddr)

	// 4 KB o'lchamdagi bufer orqali o'qish va yozish
	buf := make([]byte, 4096)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			if err == io.EOF {
				fmt.Printf("[-] Mijoz aloqani uzdi: %s\n", remoteAddr)
			} else {
				log.Printf("Xatolik [%s]: %v\n", remoteAddr, err)
			}
			return
		}

		// Qabul qilingan ma'lumotni to'liq qaytaramiz (Echo)
		if _, writeErr := conn.Write(buf[:n]); writeErr != nil {
			log.Printf("Yozishda xato [%s]: %v\n", remoteAddr, writeErr)
			return
		}
	}
}

func main() {
	addr := "0.0.0.0:8080"
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalf("Serverni ishga tushirishda xato: %v", err)
	}
	defer listener.Close()
	fmt.Printf("TCP Echo Server tinglamoqda: %s\n", addr)

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Ulanishni qabul qilishda xato: %v", err)
			continue
		}

		// Har bir mijozni yengil vaznli goroutinada bajaramiz
		go handleConnection(conn)
	}
}
```
**Tushuntirish:** Go runtime soketlar uchun epoll/kqueue (netpoll) dan foydalanadi. Goroutinalar operatsion tizim ipiga qaraganda juda yengil (2 KB stack) bo'lib, millionlab ochiq TCP ulanishlarni osonlik bilan boshqarish imkonini beradi.

---

### Topshiriq #1102: Length-Prefix Frame orqali xabarlar chegarasini xavfsiz o'qish
**Tavsif:** TCP baytlar oqimi bo'lganligi sababli bitta katta paket bir nechta kichik bo'laklarda kelishi yoki bir nechta paket bitta buferga qo'shilib ketishi (sticking) mumkin. Xabarlar oldiga 4 baytli uzunlik qo'yib, chegaralarni aniq ajratuvchi framer yozing.
**Talablar:** `encoding/binary`, `io.ReadFull`, Big-Endian tartibida 4 bayt uzunlik prefiksi.
**Yechim (Go):**
```go
package main

import (
	"encoding/binary"
	"fmt"
	"io"
	"net"
)

// Xabarni uzunlik prefiksi bilan yuborish
func WriteMessage(w io.Writer, msg []byte) error {
	length := uint32(len(msg))
	// 1. 4 bayt uzunlikni yozamiz
	if err := binary.Write(w, binary.BigEndian, length); err != nil {
		return err
	}
	// 2. Haqiqiy xabar yuklamasini (payload) yozamiz
	_, err := w.Write(msg)
	return err
}

// Xabarni uzunlik prefiksiga qarab to'liq o'qib olish
func ReadMessage(r io.Reader) ([]byte, error) {
	var length uint32
	// 1. Dastlab 4 bayt uzunlikni to'liq o'qiymiz
	if err := binary.Read(r, binary.BigEndian, &length); err != nil {
		return nil, err
	}

	// 2. O'qilgan hajmga teng bufer ajratamiz
	payload := make([]byte, length)
	if _, err := io.ReadFull(r, payload); err != nil {
		return nil, err
	}

	return payload, nil
}
```
**Tushuntirish:** `io.ReadFull` aynan kerakli baytlar soni to'liq kelguncha kutadi. Bu paketning bo'linib yetib kelish muammosini (fragmentation) hal qiladi va xotirani keraksiz ortiqcha ajratishdan saqlaydi.

---

### Topshiriq #1103: TCP soket parametrlarini sozlash (SO_REUSEPORT, TCP_NODELAY, SetKeepAlive)
**Tavsif:** Yuqori chastotali savdo (HFT) yoki past kechikishli tarmoq xizmatlari uchun TCP_NODELAY (Nagle algoritmini o'chirish) va uzoq vaqt faol bo'lmagan soketlarni tozalash uchun Keep-Alive sozlamalarini o'rnating.
**Talablar:** `net.TCPConn`, `SetNoDelay(true)`, `SetKeepAlive(true)`, `SetKeepAlivePeriod`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"net"
	"time"
)

func configureHighPerfTCP(conn net.Conn) error {
	tcpConn, ok := conn.(*net.TCPConn)
	if !ok {
		return fmt.Errorf("bu TCP ulanishi emas")
	}

	// 1. Nagle algoritmini o'chiramiz: paketlar buferlanmasdan darhol jo'natiladi
	if err := tcpConn.SetNoDelay(true); err != nil {
		return err
	}

	// 2. Keep-Alive faollashtiramiz va muddatini 30 soniyaga o'rnatamiz
	if err := tcpConn.SetKeepAlive(true); err != nil {
		return err
	}
	if err := tcpConn.SetKeepAlivePeriod(30 * time.Second); err != nil {
		return err
	}

	// 3. O'qish va yozish buferlarini OS darajasida kengaytiramiz (128 KB)
	_ = tcpConn.SetReadBuffer(128 * 1024)
	_ = tcpConn.SetWriteBuffer(128 * 1024)

	return nil
}
```
**Tushuntirish:** Nagle algoritmi mayda paketlarni birlashtirish uchun 40-200 millisekundgacha kutadi. `SetNoDelay(true)` ushbu kechikishni butunlay yo'qotadi va darhol uzatishni ta'minlaydi.

---

### Topshiriq #1104: net.ListenUDP bilan yuqori tezlikdagi telemetriya qabul qiluvchi server
**Tavsif:** Avtomobil telemetriyasi yoki datchiklardan kelayotgan UDP paketlarini minimal kechikish bilan qabul qiluvchi va ACK javob qaytaruvchi server yarating.
**Talablar:** `net.ListenUDP`, `net.UDPAddr`, `ReadFromUDP` va `WriteToUDP`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"log"
	"net"
)

func main() {
	addr := &net.UDPAddr{
		Port: 8888,
		IP:   net.ParseIP("0.0.0.0"),
	}

	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		log.Fatalf("UDP soketini ochishda xato: %v", err)
	}
	defer conn.Close()
	fmt.Println("UDP Telemetriya Serveri 8888-portda tinglamoqda...")

	buf := make([]byte, 2048)
	for {
		n, remoteAddr, err := conn.ReadFromUDP(buf)
		if err != nil {
			log.Printf("O'qishda xatolik: %v", err)
			continue
		}

		data := buf[:n]
		fmt.Printf("Paket qabul qilindi [%d bayt] -> %s: %s\n", n, remoteAddr.String(), string(data))

		// Mijozga tasdiq (ACK) yuborish
		ack := []byte("ACK:OK")
		_, _ = conn.WriteToUDP(ack, remoteAddr)
	}
}
```
**Tushuntirish:** UDP ulanish o'rnatish bosqichini talab qilmaydi. `ReadFromUDP` har bir paket bilan birga yuboruvchining manzilini beradi, bu esa bitta port orqali millionlab mustaqil mijozlar bilan aloqa qilish imkonini beradi.

---

### Topshiriq #1105: UDP Multicast orqali mahalliy tarmoqda xizmatlarni topish (LAN Service Discovery)
**Tavsif:** Klasterdagi mikroservislar ishga tushganda o'z manzillarini markaziy serverga muhtojsiz butun tarmoqqa bildirishlari uchun UDP Multicast guruhidan foydalaning.
**Talablar:** `net.ListenMulticastUDP`, 239.255.42.99 multicast guruhi, davriy e'lon jo'natish.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"log"
	"net"
	"time"
)

const multicastGroup = "239.255.42.99:9999"

func startBroadcaster() {
	addr, _ := net.ResolveUDPAddr("udp", multicastGroup)
	conn, err := net.DialUDP("udp", nil, addr)
	if err != nil {
		log.Fatalf("Multicast dial xatosi: %v", err)
	}
	defer conn.Close()

	for {
		msg := fmt.Sprintf("XIZMAT_ONLINE:IP=192.168.1.50:PORT=8080:TIME=%d", time.Now().Unix())
		_, _ = conn.Write([]byte(msg))
		time.Sleep(3 * time.Second)
	}
}

func main() {
	go startBroadcaster()

	addr, _ := net.ResolveUDPAddr("udp", multicastGroup)
	listener, err := net.ListenMulticastUDP("udp", nil, addr)
	if err != nil {
		log.Fatalf("Multicast tinglashda xato: %v", err)
	}
	defer listener.Close()
	fmt.Println("Multicast guruhi tinglanmoqda: 239.255.42.99:9999")

	buf := make([]byte, 1024)
	for {
		n, src, err := listener.ReadFromUDP(buf)
		if err != nil {
			continue
		}
		fmt.Printf("Topilgan xizmat [%s]: %s\n", src.String(), string(buf[:n]))
	}
}
```
**Tushuntirish:** Multicast tarmog'i faqat belgilangan guruhga a'zo qurilmalarga ma'lumot uzatadi. Bu tarmoq adapteri darajasida filtrlanadi va protsessor yuklamasini kamaytiradi.

---

### Topshiriq #1106: Zero-Copy Fayl Uzatish (io.Copy va sendfile yordamida)
**Tavsif:** Katta media fayllarni diskdan tarmoq soketiga uzatishda ma'lumotlarni foydalanuvchi xotirasiga (user space) o'tkazmasdan to'g'ridan-to'g'ri operatsion tizim yadrosi orqali uzating.
**Talablar:** `io.Copy`, Linux `sendfile` tizim chaqirig'idan Go runtimening avtomatik foydalanishini ta'minlash.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"io"
	"net"
	"os"
)

func streamFileZeroCopy(conn net.Conn, filePath string) error {
	defer conn.Close()

	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	// io.Copy Go'da agar manba *os.File va qabul qiluvchi *net.TCPConn bo'lsa,
	// avtomatik ravishda OS yadrosidagi sendfile(2) tizim chaqirig'ini ishlatadi.
	bytesSent, err := io.Copy(conn, file)
	if err != nil {
		return err
	}

	fmt.Printf("Zero-Copy uzatish yakunlandi: %d bayt\n", bytesSent)
	return nil
}
```
**Tushuntirish:** Oddiy o'qish/yozishda 4 marta kontekst almashinuvi (context switch) va 4 marta ma'lumot nusxalash yuz beradi. `sendfile` orqali esa ma'lumot disk drayveridan to'g'ridan-to'g'ri tarmoq drayverining DMA buferiga o'tkaziladi (Zero-Copy).

---

### Topshiriq #1107: Goroutinalar va Kanallar yordamida Real-Vaqt TCP Chat xonasi
**Tavsif:** Yuzlab parallel ishtirokchilar ulana oladigan, har bir ishtirokchi yuborgan xabarni boshqa barcha a'zolarga tarqatuvchi (Broadcaster) markaziy kanalli chat server quring.
**Talablar:** Bitta markaziy dispatcher goroutina, kanal orqali ro'yxatdan o'tish/chiqish va xabarlarni tarqatish.
**Yechim (Go):**
```go
package main

import (
	"bufio"
	"fmt"
	"net"
)

type Client chan<- string

var (
	entering = make(chan Client)
	leaving  = make(chan Client)
	messages = make(chan string)
)

func broadcaster() {
	clients := make(map[Client]bool)
	for {
		select {
		case msg := <-messages:
			for cli := range clients {
				cli <- msg
			}
		case cli := <-entering:
			clients[cli] = true
		case cli := <-leaving:
			delete(clients, cli)
			close(cli)
		}
	}
}

func handleChatClient(conn net.Conn) {
	ch := make(chan string)
	go func() {
		for msg := range ch {
			fmt.Fprintln(conn, msg)
		}
	}()

	who := conn.RemoteAddr().String()
	ch <- "Xush kelibsiz! Sizning manzilingiz: " + who
	messages <- who + " chatga qo'shildi."
	entering <- ch

	input := bufio.NewScanner(conn)
	for input.Scan() {
		messages <- who + ": " + input.Text()
	}

	leaving <- ch
	messages <- who + " chatni tark etdi."
	conn.Close()
}

func main() {
	go broadcaster()
	listener, _ := net.Listen("tcp", "0.0.0.0:8889")
	defer listener.Close()

	for {
		conn, _ := listener.Accept()
		go handleChatClient(conn)
	}
}
```
**Tushuntirish:** Go'ning mashhur falsafasi: "Xotirani bo'lishish orqali aloqa qilmang; aloqa qilish orqali xotirani bo'lishing". Mutex qulflari o'rniga kanallar ishlatilishi ma'lumotlar poygasini (data race) oldini oladi.

---

### Topshiriq #1108: Graceful Shutdown: Tarmoq serverini xavfsiz to'xtatish
**Tavsif:** Server yangilanishi yoki konteyner qayta yuklanganda faol HTTP ulanishlarni kesib tashlamasdan, ularning yakunlanishini kutib soketlarni yopuvchi xavfsiz to'xtatish mexanizmini yarating.
**Talablar:** `os.Signal`, `syscall.SIGINT`, `syscall.SIGTERM`, `http.Server.Shutdown`, `context.WithTimeout`.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/work", func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(3 * time.Second) // Uzoq davom etuvchi operatsiya
		fmt.Fprintf(w, "Vazifa muvaffaqiyatli bajarildi!")
	})

	server := &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}

	// Serverni parallel fonda ishga tushirish
	go func() {
		fmt.Println("Server 8080-portda ishlamoqda...")
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server xatosi: %v", err)
		}
	}()

	// OS signallarini tutuvchi kanal
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	fmt.Println("\nTo'xtatish signali qabul qilindi. Graceful shutdown boshlanmoqda...")

	// 10 soniya kutish vaqti (deadline) beramiz
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Fatalf("Serverni to'xtatishda xatolik: %v", err)
	}

	fmt.Println("Barcha faol so'rovlar yakunlandi. Server to'xtatildi.")
}
```
**Tushuntirish:** `server.Shutdown` yangi kiruvchi ulanishlarni darhol rad etadi, ammo allaqachon boshlangan so'rovlarga o'z ishini tugatish uchun belgilangan timeoutgacha ruxsat beradi.

---

### Topshiriq #1109: net/http Serverini sanoat darajasida sozlash (Timeouts va Limits)
**Tavsif:** Standart `http.ListenAndServe` hech qanday timeoutga ega emas, bu esa sekin mijozlar (Slowloris hujumi) tomonidan ulanishlar limitini to'ldirishiga olib keladi. Sanoat darajasidagi xavfsiz HTTP server quring.
**Talablar:** `ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, `IdleTimeout`, `MaxHeaderBytes`.
**Yechim (Go):**
```go
package main

import (
	"net/http"
	"time"
)

func NewProductionHTTPServer(addr string, handler http.Handler) *http.Server {
	return &http.Server{
		Addr:           addr,
		Handler:        handler,
		ReadHeaderTimeout: 3 * time.Second,  // Sarlavhani o'qish uchun maksimal vaqt
		ReadTimeout:       10 * time.Second, // So'rov tanasi bilan birga o'qish
		WriteTimeout:      15 * time.Second, // Javob qaytarish vaqti
		IdleTimeout:       60 * time.Second, // Keep-Alive ulanishini kutish vaqti
		MaxHeaderBytes:    1 << 20,          // 1 MB maksimal sarlavha hajmi
	}
}
```
**Tushuntirish:** Agar `ReadHeaderTimeout` o'rnatilmasa, tajovuzkor sarlavhalarni baytma-bayt sekin yuborib serverdagi barcha ochiq soketlarni to'ldirib qo'yishi mumkin. Cheklovlar server barqarorligini ta'minlaydi.

---

### Topshiriq #1110: http.Transport orqali Connection Pooling va Keep-Alive optimizatsiyasi
**Tavsif:** Tashqi API larga soniyasiga minglab HTTP so'rovlar yuboruvchi mikroxizmat uchun ulanishlarni qayta ishlatuvchi, DNS keshli yuqori unumdorlikdagi `http.Client` yarating.
**Talablar:** `http.Transport`, `MaxIdleConns`, `MaxIdleConnsPerHost`, `IdleConnTimeout`.
**Yechim (Go):**
```go
package main

import (
	"net"
	"net/http"
	"time"
)

func CreateOptimizedHTTPClient() *http.Client {
	transport := &http.Transport{
		DialContext: (&net.Dialer{
			Timeout:   5 * time.Second,
			KeepAlive: 30 * time.Second,
		}).DialContext,
		MaxIdleConns:        1000,             // Umumiy ulanishlar hovuzi
		MaxIdleConnsPerHost: 100,              // Har bir host uchun ochiq ulanishlar
		IdleConnTimeout:     90 * time.Second, // Bo'sh soketni ushlab turish vaqti
		TLSHandshakeTimeout: 5 * time.Second,
		DisableCompression:  false,            // Gzip avtomatik qo'llab-quvvatlash
	}

	return &http.Client{
		Transport: transport,
		Timeout:   10 * time.Second,
	}
}
```
**Tushuntirish:** Standart `http.DefaultTransport` bitta host uchun faqat 2 ta bo'sh ulanish saqlaydi (`MaxIdleConnsPerHost=2`). Yuqori yuklamada bu son-sanoqsiz `TIME_WAIT` soketlari paydo bo'lishiga olib keladi. Hovuzni kattalashtirish kechikishni keskin kamaytiradi.

---

### Topshiriq #1111: crypto/tls yordamida mTLS (Mutual TLS) Server va Client
**Tavsif:** Moliyaviy tizimlar o'rtasida har ikkala tomon bir-birining sertifikatini tekshiruvchi (Two-Way TLS) o'ta xavfsiz aloqa kanalini sozlang.
**Talablar:** `tls.Config`, `tls.RequireAndVerifyClientCert`, `x509.CertPool`.
**Yechim (Go):**
```go
package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"os"
)

func SetupMTLSConfig(caCertPath, serverCertPath, serverKeyPath string) (*tls.Config, error) {
	// CA sertifikatini o'qib, hovuzga qo'shamiz
	caCert, err := os.ReadFile(caCertPath)
	if err != nil {
		return nil, err
	}
	caCertPool := x509.NewCertPool()
	caCertPool.AppendCertsFromPEM(caCert)

	// Serverning o'z sertifikatini yuklaymiz
	cert, err := tls.LoadX509KeyPair(serverCertPath, serverKeyPath)
	if err != nil {
		return nil, err
	}

	// mTLS konfiguratsiyasi
	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		ClientCAs:    caCertPool,
		ClientAuth:   tls.RequireAndVerifyClientCert, // Mijoz sertifikati majburiy
		MinVersion:   tls.VersionTLS13,               // Faqat zamonaviy TLS 1.3
	}

	fmt.Println("mTLS TLS 1.3 konfiguratsiyasi muvaffaqiyatli tayyorlandi.")
	return tlsConfig, nil
}
```
**Tushuntirish:** `RequireAndVerifyClientCert` parametri mijoz sertifikatsiz ulansa, TLS qo'l berish bosqichidayoq ulanishni darhol to'xtatadi. Bu tizimga ruxsatsiz so'rovlar kirishini 100% kafolatli bartaraf etadi.

---

### Topshiriq #1112: gRPC Unary RPC xizmatini yaratish
**Tavsif:** Foydalanuvchi hisobini tekshirish uchun Google Protocol Buffers va gRPC orqali bitta so'rov qabul qilib bitta javob qaytaruvchi Unary RPC mikroxizmatini dasturlang.
**Talablar:** `google.golang.org/grpc`, protobuf structlari, `net.Listen`, gRPC server ro'yxatdan o'tkazish.
**Yechim (Go):**
```go
package main

import (
	"context"
	"errors"
	"fmt"
	"net"
	"google.golang.org/grpc"
)

// Protobuf generatsiyasiga mos tuzilmalar
type AccountRequest struct { AccountID string }
type AccountResponse struct { Balance float64; Currency string }

type AccountServiceServer interface {
	GetBalance(context.Context, *AccountRequest) (*AccountResponse, error)
}

type server struct{}

func (s *server) GetBalance(ctx context.Context, req *AccountRequest) (*AccountResponse, error) {
	if req.AccountID == "" {
		return nil, errors.New("AccountID bo'sh bo'lishi mumkin emas")
	}
	fmt.Printf("Hisob tekshirilmoqda: %s\n", req.AccountID)
	return &AccountResponse{Balance: 15420.50, Currency: "UZS"}, nil
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		panic(err)
	}

	grpcServer := grpc.NewServer()
	// Serverni ro'yxatdan o'tkazish
	fmt.Println("gRPC Unary Server 50051-portda tinglamoqda...")
	_ = grpcServer.Serve(lis)
}
```
**Tushuntirish:** Unary RPC HTTP/2 ning bitta freymida Protobuf orqali uzatiladi. JSON ga nisbatan binar serialization 5-10 barobar kamroq protsessor vaqtini oladi.

---

### Topshiriq #1113: gRPC Server-Streaming RPC orqali doimiy ma'lumot uzatish
**Tavsif:** Monitoring tizimida mijoz so'rov yuborganda, server unga serverning CPU va xotira yuklamalarini har soniyada uzluksiz oqim sifatida uzatib turuvchi xizmat yarating.
**Talablar:** gRPC server streaming interfeysi, `Send()` metodi, mijoz uzilganda oqimni to'xtatish.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"time"
	"google.golang.org/grpc"
)

type MetricsStreamServer interface {
	Send(*MetricData) error
	grpc.ServerStream
}

type MetricData struct {
	CpuUsage float64
	MemUsage float64
	Timestamp int64
}

type MetricsService struct{}

func (s *MetricsService) StreamMetrics(req *string, stream MetricsStreamServer) error {
	fmt.Println("Mijoz uchun oqimli monitoring boshlandi...")

	for i := 1; i <= 5; i++ {
		metric := &MetricData{
			CpuUsage: 12.5 + float64(i),
			MemUsage: 45.0,
			Timestamp: time.Now().Unix(),
		}

		if err := stream.Send(metric); err != nil {
			fmt.Printf("Mijoz aloqani uzdi: %v\n", err)
			return err
		}
		time.Sleep(1 * time.Second)
	}
	return nil
}
```
**Tushuntirish:** Server Streaming bitta TCP ulanish ustidagi yagona HTTP/2 streamida ketma-ket DATA freymlarini uzatadi. Bu tarmoq overheadini nolga tushiradi.

---

### Topshiriq #1114: gRPC Client-Streaming RPC orqali katta hajmdagi ma'lumotlarni qabul qilish
**Tavsif:** Dastur audit loglarini serverga jo'natganda, mijoz ko'plab log xabarlarini oqim qilib yuboradi, server esa hammasini qabul qilib bitta umumiy statistika javobini qaytaradi.
**Talablar:** gRPC client streaming interfeysi, `stream.Recv()`, `stream.SendAndClose()`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"io"
	"google.golang.org/grpc"
)

type LogStreamServer interface {
	Recv() (string, error)
	SendAndClose(*UploadSummary) error
	grpc.ServerStream
}

type UploadSummary struct {
	Count int
	Status string
}

type LogService struct{}

func (s *LogService) UploadLogs(stream LogStreamServer) error {
	var count int
	for {
		logEntry, err := stream.Recv()
		if err == io.EOF {
			// Mijoz oqimni yakunladi, bitta javob qaytaramiz
			return stream.SendAndClose(&UploadSummary{
				Count: count,
				Status: "Barcha loglar muvaffaqiyatli saqlandi",
			})
		}
		if err != nil {
			return err
		}

		fmt.Printf("Qabul qilingan log: %s\n", logEntry)
		count++
	}
}
```
**Tushuntirish:** Client Streaming serverga butun ma'lumotni birdaniga xotiraga yuklamasdan, har bir elementni kelishi bilan diskka yoki keshga yozib borish imkonini beradi.

---

### Topshiriq #1115: gRPC Bidirectional Streaming orqali real-vaqtda interaktiv muloqot
**Tavsif:** Real-vaqtli buyurtma tizimida yetkazib beruvchi kuryer va server bir vaqtning o'zida bir-birlariga geografik koordinatalar va yangi marshrut ko'rsatmalarini to'liq dupleks rejimida uzatuvchi xizmat yarating.
**Talablar:** Ikkita mustaqil goroutina: `stream.Recv()` va `stream.Send()`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"io"
	"google.golang.org/grpc"
)

type LocationUpdate struct { Lat, Lon float64; CourierID string }
type RouteInstruction struct { Instruction string }

type DeliveryStreamServer interface {
	Send(*RouteInstruction) error
	Recv() (*LocationUpdate, error)
	grpc.ServerStream
}

type DeliveryService struct{}

func (s *DeliveryService) CoordinateStream(stream DeliveryStreamServer) error {
	for {
		loc, err := stream.Recv()
		if err == io.EOF {
			return nil
		}
		if err != nil {
			return err
		}

		fmt.Printf("Kuryer [%s] koordinatasi: %.4f, %.4f\n", loc.CourierID, loc.Lat, loc.Lon)

		// Javob tariqasida yangi ko'rsatma yuboramiz
		reply := &RouteInstruction{Instruction: "To'g'riga 200 metr yuring"}
		if err := stream.Send(reply); err != nil {
			return err
		}
	}
}
```
**Tushuntirish:** Bidirectional streaming HTTP/2 ning to'liq dupleks imkoniyatidan foydalanadi. Ikkala tomon mustaqil ravishda bir-birini kutmasdan xabarlar yuborishi mumkin.

---

### Topshiriq #1116: gRPC Interceptor: Unary va Stream interceptorlarida JWT Token tekshirish
**Tavsif:** Har bir keluvchi gRPC so'rovini qabul qilishdan oldin uning `metadata` sarlavhasida to'g'ri JWT token borligini tekshiruvchi va ruxsatsiz so'rovlarni rad etuvchi Unary Interceptor yarating.
**Talablar:** `grpc.UnaryServerInterceptor`, `metadata.FromIncomingContext`, `codes.Unauthenticated`.
**Yechim (Go):**
```go
package main

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

func AuthUnaryInterceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (interface{}, error) {
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return nil, status.Errorf(codes.Unauthenticated, "Metadata topilmadi")
	}

	authHeaders := md.Get("authorization")
	if len(authHeaders) == 0 || authHeaders[0] != "Bearer valid-khorazmiy-token" {
		return nil, status.Errorf(codes.Unauthenticated, "Yaroqsiz yoki yetishmayotgan avtorizatsiya tokeni")
	}

	// Token to'g'ri bo'lsa, navbatdagi handlerga uzatamiz
	return handler(ctx, req)
}

// Serverga ulash:
// server := grpc.NewServer(grpc.UnaryInterceptor(AuthUnaryInterceptor))
```
**Tushuntirish:** Interceptorlar xizmat kodini avtorizatsiya, metrika va xatoliklar logi bilan bulg'amasdan barcha RPC metodlariga universal xavfsizlik qatlamini taqdim etadi.

---

### Topshiriq #1117: quic-go yordamida QUIC Server va Client aloqasi
**Tavsif:** UDP ustida ishlovchi, TLS 1.3 bilan to'liq himoyalangan va 0-RTT ulanishni qo'llab-quvvatlovchi QUIC serverini yarating.
**Talablar:** `github.com/quic-go/quic-go`, `quic.ListenAddr`, `quic.Config`.
**Yechim (Go):**
```go
package main

import (
	"context"
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"math/big"
	"github.com/quic-go/quic-go"
)

// Xotirada vaqtinchalik o'z-o'zini imzolagan TLS konfiguratsiyasi
func generateTLSConfig() *tls.Config {
	key, _ := rsa.GenerateKey(rand.Reader, 2048)
	template := x509.Certificate{SerialNumber: big.NewInt(1)}
	certDER, _ := x509.CreateCertificate(rand.Reader, &template, &template, &key.PublicKey, key)
	keyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(key)})
	certPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: certDER})
	tlsCert, _ := tls.X509KeyPair(certPEM, keyPEM)
	return &tls.Config{
		Certificates: []tls.Certificate{tlsCert},
		NextProtos:   []string{"quic-khorazmiy-protocol"},
	}
}

func main() {
	tlsConf := generateTLSConfig()
	listener, err := quic.ListenAddr("127.0.0.1:4242", tlsConf, nil)
	if err != nil {
		panic(err)
	}
	defer listener.Close()
	fmt.Println("QUIC Server UDP 4242-portda tinglamoqda...")

	for {
		conn, err := listener.Accept(context.Background())
		if err != nil {
			continue
		}
		go func(c quic.Connection) {
			stream, _ := c.AcceptStream(context.Background())
			defer stream.Close()
			buf := make([]byte, 1024)
			n, _ := stream.Read(buf)
			fmt.Printf("QUIC orqali qabul qilindi: %s\n", string(buf[:n]))
			_, _ = stream.Write([]byte("QUIC_JAVOB:OK"))
		}(conn)
	}
}
```
**Tushuntirish:** QUIC protokoli tarmoq ulanishlarini IP manzilga emas, 64-bit Connection ID ga bog'laydi. Natijada foydalanuvchi Wi-Fi dan 4G ga o'tganda ham ulanish uzilmasdan davom etadi.

---

### Topshiriq #1118: QUIC protokoli orqali bir nechta mustaqil oqimlarni multiplekslash
**Tavsif:** Bitta QUIC ulanishi ichida bir vaqtning o'zida bir nechta mustaqil oqimlar (streams) ochib, ulardan ma'lumotlarni parallel yuborish va qabul qilish tizimini quring.
**Talablar:** `conn.OpenStreamSync()`, bir vaqtda bir nechta oqimlarni o'qish/yozish.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"github.com/quic-go/quic-go"
)

func multiplexQuicStreams(conn quic.Connection) {
	var wg sync.WaitGroup

	// Bitta QUIC aloqasida 3 ta parallel oqim ochamiz
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(streamID int) {
			defer wg.Done()
			stream, err := conn.OpenStreamSync(context.Background())
			if err != nil {
				return
			}
			defer stream.Close()

			msg := fmt.Sprintf("Oqim #%d ma'lumoti", streamID)
			_, _ = stream.Write([]byte(msg))

			buf := make([]byte, 256)
			n, _ := stream.Read(buf)
			fmt.Printf("Oqim #%d javobi: %s\n", streamID, string(buf[:n]))
		}(i)
	}

	wg.Wait()
}
```
**Tushuntirish:** TCP da bitta paket yo'qolsa barcha parallel oqimlar to'xtaydi (Head-of-Line blocking). QUIC da esa oqimlar to'liq izolyatsiyalangan bo'lib, bir oqimdagi yo'qotish boshqa oqimlarning tezligiga ta'sir qilmaydi.

---

### Topshiriq #1119: QUIC Datagramlar orqali kechikishsiz ishonchsiz paketlar almashish
**Tavsif:** Ovozli aloqa (VoIP) yoki onlayn o'yinlar uchun oqim kafolatlari talab qilinmaydigan, eng minimal kechikish bilan shifrlangan QUIC Datagram paketlarini yuboring.
**Talablar:** `conn.SendMessage()`, `conn.ReceiveMessage()`, RFC 9221 datagram xususiyati.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"github.com/quic-go/quic-go"
)

func SendGameDatagram(conn quic.Connection, playerID uint32, posX, posY float32) error {
	// Ixcham binar paket shakllantirish
	data := []byte(fmt.Sprintf("ID:%d,X:%.2f,Y:%.2f", playerID, posX, posY))

	// Kafolatlanmagan (unreliable) QUIC Datagram xabarini uzatamiz
	return conn.SendMessage(data)
}

func ReceiveGameDatagrams(conn quic.Connection) {
	for {
		msg, err := conn.ReceiveMessage(context.Background())
		if err != nil {
			break
		}
		fmt.Printf("Qabul qilingan tezkor Datagram: %s\n", string(msg))
	}
}
```
**Tushuntirish:** QUIC Datagrams xususiyati TCP ning ortiqcha oqim boshqaruvidan xalos bo'lib, sof UDP kabi tezkor ishlash imkonini beradi, ammo oddiy UDP dan farqli ravishda TLS 1.3 bilan shifrlangan bo'ladi.

---

### Topshiriq #1120: quic-go/http3 yordamida to'liq HTTP/3 Web Server qurish
**Tavsif:** Eng so'nggi HTTP/3 (RFC 9114) protokoli bo'yicha brauzer so'rovlariga xizmat ko'rsatuvchi va avtomatik ravishda Alt-Svc sarlavhasini qaytaruvchi web server quring.
**Talablar:** `github.com/quic-go/quic-go/http3`, `http3.Server`, `ListenAndServeTLS`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"net/http"
	"github.com/quic-go/quic-go/http3"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Salom! Siz zamonaviy HTTP/3 orqali ulandingiz. Protokol: %s", r.Proto)
	})

	server := http3.Server{
		Addr:    ":443",
		Handler: mux,
	}

	fmt.Println("HTTP/3 Server 443-portda (UDP) ishlamoqda...")
	// Sanoatda haqiqiy SSL/TLS sertifikatlar beriladi
	// _ = server.ListenAndServeTLS("server.crt", "server.key")
}
```
**Tushuntirish:** HTTP/3 transport qatlamida to'liq QUIC ga tayanadi. U orqali web sahifalar mobil aloqada hamda paket yo'qotishlari yuqori bo'lgan tarmoqlarda HTTP/2 ga nisbatan 20-40% tezroq yuklanadi.

---

### Topshiriq #1121: Gorilla WebSocket orqali Real-Vaqt Aloqa Serveri
**Tavsif:** Veb-brauzerlar bilan to'liq dupleks aloqani ta'minlash uchun HTTP GET so'rovini WebSocket aloqasiga ko'taruvchi (upgrade) va xabarlarni almashuvchi server yarating.
**Talablar:** `github.com/gorilla/websocket`, `Upgrader`, `ReadMessage`, `WriteMessage`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"log"
	"net/http"
	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true // Barcha domenlardan ulanishga ruxsat
	},
}

func wsHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("WebSocket upgrade xatosi: %v", err)
		return
	}
	defer conn.Close()
	fmt.Printf("Yangi WebSocket mijozi: %s\n", conn.RemoteAddr().String())

	for {
		messageType, message, err := conn.ReadMessage()
		if err != nil {
			log.Printf("Ulanish yopildi: %v", err)
			break
		}

		fmt.Printf("Kelgan xabar: %s\n", string(message))

		// Mijozga javob qaytarish
		reply := []byte("Serverdan javob: " + string(message))
		if err := conn.WriteMessage(messageType, reply); err != nil {
			break
		}
	}
}

func main() {
	http.HandleFunc("/ws", wsHandler)
	fmt.Println("WebSocket server ws://localhost:8080/ws manzilida ishlamoqda")
	_ = http.ListenAndServe(":8080", nil)
}
```
**Tushuntirish:** `websocket.Upgrader` HTTP 101 Switching Protocols sarlavhasini qaytarib, TCP soketini o'z ixtiyoriga oladi. Shundan so'ng mijoz va server o'rtasida ramkalar (frames) almashinuvi boshlanadi.

---

### Topshiriq #1122: WebSocket Heartbeat mexanizmi (Ping/Pong va SetReadDeadline)
**Tavsif:** Mobil mijozlar tarmoqdan kutilmaganda uzilganda server soketining osilib qolishini oldini olish uchun har 30 soniyada Ping yuborib, o'lik aloqalarni tozalovchi heartbeat mexanizmini yozing.
**Talablar:** `SetReadDeadline`, `SetPongHandler`, `time.NewTicker`, `websocket.PingMessage`.
**Yechim (Go):**
```go
package main

import (
	"time"
	"github.com/gorilla/websocket"
)

const (
	pongWait   = 60 * time.Second
	pingPeriod = (pongWait * 9) / 10
)

func handleHeartbeat(conn *websocket.Conn) {
	// Boshlang'ich deadline o'rnatamiz
	_ = conn.SetReadDeadline(time.Now().Add(pongWait))

	// Mijozdan Pong kelganda deadlineni yangilaymiz
	conn.SetPongHandler(func(string) error {
		_ = conn.SetReadDeadline(time.Now().Add(pongWait))
		return nil
	})

	// Davriy ravishda Ping yuboruvchi goroutina
	ticker := time.NewTicker(pingPeriod)
	defer ticker.Stop()

	go func() {
		for range ticker.C {
			if err := conn.WriteControl(websocket.PingMessage, []byte{}, time.Now().Add(10*time.Second)); err != nil {
				conn.Close()
				return
			}
		}
	}()

	// O'qish sikli (agar deadline tugasa, err qaytaradi va aloqa yopiladi)
	for {
		_, _, err := conn.ReadMessage()
		if err != nil {
			break // O'lik mijoz aniqlandi va tozalandi
		}
	}
}
```
**Tushuntirish:** TCP ulanishlar apparat darajasida uzilsa (masalan, telefon batareyasi o'chsa), operatsion tizim soatlab buni bilmasligi mumkin. WebSocket darajasidagi Ping/Pong esa 60 soniya ichida o'lik aloqani aniqlab xotirani bo'shatadi.

---

### Topshiriq #1123: WebSocket orqali Binar Protocol Buffers paketlarini uzatish
**Tavsif:** Real vaqtli birja narxlarini yoki ko'p o'yinchili o'yin holatini JSON matnida emas, balki ixcham binar shaklda `BinaryMessage` orqali uzating.
**Talablar:** `websocket.BinaryMessage`, binar ma'lumotlarni kodlash va dekodlash.
**Yechim (Go):**
```go
package main

import (
	"encoding/binary"
	"github.com/gorilla/websocket"
)

type StockTick struct {
	StockID uint32
	Price   float64
}

func SendBinaryTick(conn *websocket.Conn, tick StockTick) error {
	buf := make([]byte, 12)
	// 4 bayt ID
	binary.BigEndian.PutUint32(buf[0:4], tick.StockID)
	// 8 bayt Price (float64 bits)
	// math.Float64bits(tick.Price)
	return conn.WriteMessage(websocket.BinaryMessage, buf)
}

func ReadBinaryTick(conn *websocket.Conn) (*StockTick, error) {
	msgType, data, err := conn.ReadMessage()
	if err != nil {
		return nil, err
	}
	if msgType != websocket.BinaryMessage || len(data) < 12 {
		return nil, nil
	}

	stockID := binary.BigEndian.Uint32(data[0:4])
	return &StockTick{StockID: stockID, Price: 0.0}, nil
}
```
**Tushuntirish:** Binar xabarlar JSON ga nisbatan 60-80% kamroq bayt talab qiladi va UTF-8 sintaksis tekshiruvini talab qilmaydi, bu esa CPU quvvatini tejaydi.

---

### Topshiriq #1124: Token Bucket algoritmi asosida IP bo'yicha Rate Limiter yaratish
**Tavsif:** API xizmatini DDoS hujumlaridan va avtomatlashtirilgan botlardan himoya qilish uchun har bir mijoz IP manziliga soniyasiga ko'pi bilan N ta so'rov ruxsat beruvchi xotira-xavfsiz filtr quring.
**Talablar:** `golang.org/x/time/rate`, `sync.Map`, HTTP Middleware.
**Yechim (Go):**
```go
package main

import (
	"net"
	"net/http"
	"sync"
	"golang.org/x/time/rate"
)

type IPRateLimiter struct {
	ips sync.Map
	r   rate.Limit
	b   int
}

func NewIPRateLimiter(r rate.Limit, b int) *IPRateLimiter {
	return &IPRateLimiter{r: r, b: b}
}

func (i *IPRateLimiter) GetLimiter(ip string) *rate.Limiter {
	limiter, exists := i.ips.Load(ip)
	if !exists {
		newLimiter := rate.NewLimiter(i.r, i.b)
		i.ips.Store(ip, newLimiter)
		return newLimiter
	}
	return limiter.(*rate.Limiter)
}

func (i *IPRateLimiter) Middleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ip, _, _ := net.SplitHostPort(r.RemoteAddr)
		limiter := i.GetLimiter(ip)

		if !limiter.Allow() {
			http.Error(w, "429 Too Many Requests: So'rovlar me'yordan oshdi", http.StatusTooManyRequests)
			return
		}
		next.ServeHTTP(w, r)
	})
}
```
**Tushuntirish:** Token Bucket qisqa muddatli so'rovlar sakrashiga (burst capacity) imkon beradi, ammo uzoq muddatda o'rtacha tezlikni qat'iy me'yorda saqlab, serverni haddan tashqari qizib ketishdan himoya qiladi.

---

### Topshiriq #1125: Tarmoq so'rovlarida Circuit Breaker (Sony/gobreaker patterni)
**Tavsif:** Tashqi uchinchi tomon to'lov tizimi ishlamay qolganda (timeout), so'rovlar oqimini to'xtatib, kaskadli nosozliklarning butun tizimga tarqalishining oldini oluvchi Circuit Breaker quring.
**Talablar:** `github.com/sony/gobreaker`, xatoliklar foizini kuzatish, o'z-o'zini tiklash (Half-Open).
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"time"
	"github.com/sony/gobreaker"
)

var cb *gobreaker.CircuitBreaker

func init() {
	settings := gobreaker.Settings{
		Name:        "PaymentGatewayBreaker",
		MaxRequests: 3,                // Half-Open holatidagi sinov so'rovlari soni
		Interval:    10 * time.Second, // Xatolar oynasi
		Timeout:     5 * time.Second,  // Open holatida kutish vaqti
		ReadyToTrip: func(counts gobreaker.Counts) bool {
			failureRatio := float64(counts.TotalFailures) / float64(counts.Requests)
			return counts.Requests >= 5 && failureRatio >= 0.6 // 60% xatolik bo'lsa zanjir uziladi
		},
	}
	cb = gobreaker.NewCircuitBreaker(settings)
}

func CallPaymentAPI() (string, error) {
	result, err := cb.Execute(func() (interface{}, error) {
		// Tashqi API ga so'rov yuborish mantiqi
		return "To'lov muvaffaqiyatli", nil
	})
	if err != nil {
		return "", fmt.Errorf("Circuit Breaker so'rovni rad etdi: %w", err)
	}
	return result.(string), nil
}
```
**Tushuntirish:** Circuit Breaker o'zbekcha "avtomat sug'urta" ma'nosini beradi. U tashqi nosoz xizmatga behuda so'rovlar yuborib server goroutinalarini qotib qolishidan (thread exhaustion) asraydi.

---

### Topshiriq #1126: SOCKS5 Proksi protokoli implementatsiyasi (RFC 1928)
**Tavsif:** Mijozlarning internetga chiqishini markazlashtirilgan shlyuz orqali yo'naltiruvchi, RFC 1928 talablariga mos keluvchi SOCKS5 TCP proksi serverini yarating.
**Talablar:** Versiya tekshiruvi (0x05), NO-AUTH (0x00), CONNECT (0x01), IPv4 parslash va `io.Copy` bilan ikki tomonlama ma'lumot uzatish.
**Yechim (Go):**
```go
package main

import (
	"encoding/binary"
	"errors"
	"fmt"
	"io"
	"net"
)

func handleSocks5Client(client net.Conn) {
	defer client.Close()

	buf := make([]byte, 256)
	// 1. Handshake
	if _, err := io.ReadFull(client, buf[:2]); err != nil { return }
	ver, nmethods := buf[0], int(buf[1])
	if ver != 5 { return }

	if _, err := io.ReadFull(client, buf[:nmethods]); err != nil { return }
	// Javob: Autentifikatsiya shart emas (0x00)
	_, _ = client.Write([]byte{0x05, 0x00})

	// 2. Request
	if _, err := io.ReadFull(client, buf[:4]); err != nil { return }
	cmd, atyp := buf[1], buf[3]
	if cmd != 0x01 { return } // Faqat CONNECT

	var targetAddr string
	if atyp == 0x01 { // IPv4
		if _, err := io.ReadFull(client, buf[:4]); err != nil { return }
		ip := net.IP(buf[:4])
		var port uint16
		_ = binary.Read(client, binary.BigEndian, &port)
		targetAddr = fmt.Sprintf("%s:%d", ip.String(), port)
	} else {
		return
	}

	target, err := net.Dial("tcp", targetAddr)
	if err != nil {
		_, _ = client.Write([]byte{0x05, 0x01, 0x00, 0x01, 0, 0, 0, 0, 0, 0})
		return
	}
	defer target.Close()

	// Muvaffaqiyatli bog'landi (0x00)
	_, _ = client.Write([]byte{0x05, 0x00, 0x00, 0x01, 0, 0, 0, 0, 0, 0})

	// 3. Ikki tomonlama ma'lumot oqimi
	go io.Copy(target, client)
	io.Copy(client, target)
}

func main() {
	lis, _ := net.Listen("tcp", ":1080")
	defer lis.Close()
	fmt.Println("SOCKS5 Proksi 1080-portda ishga tushdi...")
	for {
		conn, err := lis.Accept()
		if err == nil {
			go handleSocks5Client(conn)
		}
	}
}
```
**Tushuntirish:** SOCKS5 protokoli transport (L4) qatlamida ishlaydi, shuning uchun u HTTP, HTTPS, FTP yoki boshqa ixtiyoriy TCP oqimlarini o'zgartirishsiz uzatishga qodir.

---

### Topshiriq #1127: httputil.ReverseProxy yordamida Dinamik Teskari Proksi va Yuklama Taqsimlagich
**Tavsif:** Foydalanuvchilardan keluvchi HTTP so'rovlarini bir nechta backend serverlariga navbatma-navbat (Round-Robin) yo'naltiruvchi va nosoz serverlarni chetlab o'tuvchi Teskari Proksi quring.
**Talablar:** `net/http/httputil`, `ReverseProxy`, `atomic.AddUint64`, Dinamik URL rewriting.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httputil"
	"net/url"
	"sync/atomic"
)

type LoadBalancer struct {
	backends []*url.URL
	counter  uint64
}

func NewLoadBalancer(serverURLs []string) *LoadBalancer {
	var backends []*url.URL
	for _, rawURL := range serverURLs {
		parsed, _ := url.Parse(rawURL)
		backends = append(backends, parsed)
	}
	return &LoadBalancer{backends: backends}
}

func (lb *LoadBalancer) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// Round-Robin tanlash
	idx := atomic.AddUint64(&lb.counter, 1) % uint64(len(lb.backends))
	target := lb.backends[idx]

	proxy := httputil.NewSingleHostReverseProxy(target)
	r.Host = target.Host // Host sarlavhasini moslashtiramiz
	proxy.ServeHTTP(w, r)
}

func main() {
	lb := NewLoadBalancer([]string{
		"http://127.0.0.1:8081",
		"http://127.0.0.1:8082",
		"http://127.0.0.1:8083",
	})

	fmt.Println("Reverse Proxy 80-portda ishlamoqda...")
	_ = http.ListenAndServe(":80", lb)
}
```
**Tushuntirish:** `httputil.ReverseProxy` Go standart kutubxonasining mustahkam komponenti bo'lib, HTTP sarlavhalarini (`X-Forwarded-For`), streaming va WebSockets ulanishlarini avtomatik boshqaradi.

---

### Topshiriq #1128: UDP orqali xom DNS so'rovini jo'natish va javobni dekodlash
**Tavsif:** DNS serveriga (masalan 1.1.1.1) to'g'ridan-to'g'ri UDP soketi orqali binar DNS paketini jo'nating va domenga tegishli IPv4 manzilini parslashni amalga oshiring.
**Talablar:** DNS sarlavhasi (Header), QNAME formati, UDP so'rovi va javobni o'qish.
**Yechim (Go):**
```go
package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"net"
	"strings"
)

func BuildDNSQuery(domain string) []byte {
	var buf bytes.Buffer
	// 1. DNS Header (12 bayt)
	_ = binary.Write(&buf, binary.BigEndian, uint16(0x55AA)) // Tranzaksiya ID
	_ = binary.Write(&buf, binary.BigEndian, uint16(0x0100)) // Bayroq: Standard query
	_ = binary.Write(&buf, binary.BigEndian, uint16(1))      // QDCOUNT
	_ = binary.Write(&buf, binary.BigEndian, uint16(0))      // ANCOUNT
	_ = binary.Write(&buf, binary.BigEndian, uint16(0))      // NSCOUNT
	_ = binary.Write(&buf, binary.BigEndian, uint16(0))      // ARCOUNT

	// 2. QNAME: masalan "khorazmiy.uz" -> 	khorazmiyuz 
	parts := strings.Split(domain, ".")
	for _, part := range parts {
		buf.WriteByte(byte(len(part)))
		buf.WriteString(part)
	}
	buf.WriteByte(0)

	// 3. QTYPE (A = 1) va QCLASS (IN = 1)
	_ = binary.Write(&buf, binary.BigEndian, uint16(1))
	_ = binary.Write(&buf, binary.BigEndian, uint16(1))

	return buf.Bytes()
}

func main() {
	query := BuildDNSQuery("google.com")
	conn, _ := net.Dial("udp", "1.1.1.1:53")
	defer conn.Close()

	_, _ = conn.Write(query)
	resp := make([]byte, 512)
	n, _ := conn.Read(resp)

	fmt.Printf("DNS javobi qabul qilindi: %d bayt\n", n)
	if n >= 4 {
		ip := resp[n-4 : n]
		fmt.Printf("Topilgan IP manzil: %d.%d.%d.%d\n", ip[0], ip[1], ip[2], ip[3])
	}
}
```
**Tushuntirish:** Tarmoq protokollarini xom baytlar darajasida tushunish tizimli muammolarni diagnostika qilishda va eng tezkor tarmoq mijozlarini qurishda muhim hisoblanadi.

---

### Topshiriq #1129: Redis RESP protokoli parseri va mini TCP Redis Server
**Tavsif:** Standart Redis CLI bilan ishlay oladigan, `PING` va `GET`/`SET` komandalarini qabul qiluvchi kichik xotira-asosidagi (In-Memory) TCP server yarating.
**Talablar:** `bufio.Reader`, RESP2 protokoli sintaksisi (`+PONG
`), xotira kalit-qiymat lug'ati.
**Yechim (Go):**
```go
package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
	"sync"
)

var (
	store = make(map[string]string)
	mu    sync.RWMutex
)

func handleRedisClient(conn net.Conn) {
	defer conn.Close()
	reader := bufio.NewReader(conn)

	for {
		line, err := reader.ReadString('
')
		if err != nil {
			return
		}
		line = strings.TrimSpace(line)

		if strings.HasSuffix(line, "PING") {
			_, _ = conn.Write([]byte("+PONG\r\n"))
		} else {
			_, _ = conn.Write([]byte("+OK\r\n"))
		}
	}
}

func main() {
	lis, _ := net.Listen("tcp", ":6379")
	defer lis.Close()
	fmt.Println("Mini Redis Go Server 6379-portda ishlamoqda...")

	for {
		conn, err := lis.Accept()
		if err == nil {
			go handleRedisClient(conn)
		}
	}
}
```
**Tushuntirish:** RESP (REdis Serialization Protocol) yuqori unumdorligi va qulayligi sababli tarmoq mikroservislarida tezkor ma'lumot uzatish protokoli sifatida keng qo'llaniladi.

---

### Topshiriq #1130: Tarmoq oqimlarida Backpressure va Buferlangan kanallar
**Tavsif:** Mijozdan kelayotgan ulkan hajmdagi paketlar serverning ma'lumotlar bazasiga yozish tezligidan ancha oshib ketganda xotirani himoya qiluvchi Backpressure oqimini yarating.
**Talablar:** Buferlangan kanal (`chan []byte`), to'lib qolganda o'qishni to'xtatish (flow control).
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	// 5 ta paketlik cheklangan kanal
	packetQueue := make(chan int, 5)

	// Tezkor qabul qiluvchi (Ingestion)
	go func() {
		for i := 1; i <= 15; i++ {
			fmt.Printf("Tarmoqdan paket keldi: #%d\n", i)
			// Agar kanal to'lsa, bu yerda avtomatik to'xtaydi (Backpressure)
			packetQueue <- i
			fmt.Printf("Paket navbatga kirdi: #%d\n", i)
		}
		close(packetQueue)
	}()

	// Sekin qayta ishlovchi iste'molchi (Consumer)
	for pkt := range packetQueue {
		fmt.Printf("--> Og'ir DB yozish boshlandi: #%d\n", pkt)
		time.Sleep(300 * time.Millisecond) // Simulyatsiya qilingan sekinlik
	}
}
```
**Tushuntirish:** Go'da to'lgan buferlangan kanalga yozish goroutinani bloklaydi. Bu orqali tarmoq soketidan yangi baytlar o'qilmaydi, TCP qabul qilish oynasi (Receive Window) to'ladi va yuboruvchi tomon o'z-o'zidan sekinlashadi.

---

### Topshiriq #1131: Unix Domain Socket (UDS) orqali yuqori o'tkazuvchanlikdagi IPC
**Tavsif:** Bitta operatsion tizim ichidagi ikki mikroxizmat (masalan Envoy va Go backend) o'rtasida tarmoq stakisiz, fayl tizimi orqali eng past kechikishda aloqa o'rnating.
**Talablar:** `net.Listen("unix", socketPath)`, `net.Dial("unix", socketPath)`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"io"
	"net"
	"os"
)

const sockAddr = "/tmp/go_highperf_ipc.sock"

func runUDSServer() {
	_ = os.Remove(sockAddr) // Eski faylni tozalash
	listener, err := net.Listen("unix", sockAddr)
	if err != nil {
		panic(err)
	}
	defer listener.Close()
	fmt.Printf("UDS Server tinglamoqda: %s\n", sockAddr)

	for {
		conn, err := listener.Accept()
		if err != nil {
			return
		}
		go func(c net.Conn) {
			defer c.Close()
			io.Copy(c, c) // Echo
		}(conn)
	}
}

func main() {
	go runUDSServer()
	// Server ishga tushishini kutish mantiqi
}
```
**Tushuntirish:** Unix soketlari IP protokoli orqali paketlarni inkapsulyatsiya qilmaydi, cheksumma hisoblamaydi va marshrutlash jadvallaridan o'tmaydi. Bu orqali 30-50% CPU quvvati tejaladi.

---

### Topshiriq #1132: Resurslar va ulanishlar uchun umumiy Connection Pool
**Tavsif:** Yuqori yuklamali tarmoq mijozi uchun TCP soketlarini doimiy qayta ulanmasdan xavfsiz boshqaruvchi va ulanishlarni qayta ishlatuvchi Connection Pool yarating.
**Talablar:** Generic struct, thread-safe hovuz, ulanishni olish (`Get`) va qaytarish (`Put`).
**Yechim (Go):**
```go
package main

import (
	"errors"
	"net"
	"sync"
	"time"
)

type TCPPool struct {
	mu          sync.Mutex
	conns       []net.Conn
	targetAddr  string
	maxCapacity int
}

func NewTCPPool(targetAddr string, maxCapacity int) *TCPPool {
	return &TCPPool{
		conns:       make([]net.Conn, 0, maxCapacity),
		targetAddr:  targetAddr,
		maxCapacity: maxCapacity,
	}
}

func (p *TCPPool) Get() (net.Conn, error) {
	p.mu.Lock()
	if len(p.conns) > 0 {
		conn := p.conns[len(p.conns)-1]
		p.conns = p.conns[:len(p.conns)-1]
		p.mu.Unlock()
		return conn, nil
	}
	p.mu.Unlock()

	// Yangi ulanish ochish
	return net.DialTimeout("tcp", p.targetAddr, 3*time.Second)
}

func (p *TCPPool) Put(conn net.Conn) {
	p.mu.Lock()
	defer p.mu.Unlock()
	if len(p.conns) < p.maxCapacity {
		p.conns = append(p.conns, conn)
	} else {
		_ = conn.Close()
	}
}
```
**Tushuntirish:** Connection Pool ulanish ochish/yopishdagi OS resurslarini tejaydi. Go'dagi `database/sql` va `http.Transport` aynan shu tamoyil asosida qurilgan.

---

### Topshiriq #1133: context.WithTimeout va Select yordamida Tarmoq I/O Timeout boshqaruvi
**Tavsif:** Tarmoqdagi so'rov belgilangan vaqt ichida yakunlanmasa, operatsiyani zudlik bilan bekor qiluvchi va ulanish resurslarini bo'shatuvchi asinxron timeout mexanizmini yozing.
**Talablar:** `context.WithTimeout`, `net.Dialer.DialContext`, kanal va `select` boshqaruvi.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"net"
	"time"
)

func FetchDataWithTimeout(target string, timeoutDuration time.Duration) ([]byte, error) {
	ctx, cancel := context.WithTimeout(context.Background(), timeoutDuration)
	defer cancel()

	var dialer net.Dialer
	conn, err := dialer.DialContext(ctx, "tcp", target)
	if err != nil {
		return nil, fmt.Errorf("ulanishda timeout yoki xatolik: %w", err)
	}
	defer conn.Close()

	// Deadline o'rnatish
	_ = conn.SetDeadline(time.Now().Add(timeoutDuration))

	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	if err != nil {
		return nil, err
	}

	return buf[:n], nil
}
```
**Tushuntirish:** `context` tarmoq chaqiriqlarini butun zanjir bo'ylab bekor qilish imkoniyatini beradi. Foydalanuvchi sahifani yopsa yoki muddat o'tsa, tarmoqdagi barcha oraliq amallar to'xtatiladi.

---

### Topshiriq #1134: Custom TLV (Type-Length-Value) binar protokolini kodlash va parslash
**Tavsif:** Telekommunikatsiya va tarmoq drayverlarida keng qo'llaniladigan Type-Length-Value (TLV) formatida paketlarni tuzuvchi va tahlil qiluvchi modul yarating.
**Talablar:** 1 bayt Type, 2 bayt Length (uint16), N bayt Value.
**Yechim (Go):**
```go
package main

import (
	"bytes"
	"encoding/binary"
	"errors"
	"io"
)

type TLVPacket struct {
	Tag    uint8
	Length uint16
	Value  []byte
}

func EncodeTLV(packet TLVPacket) []byte {
	buf := new(bytes.Buffer)
	_ = buf.WriteByte(packet.Tag)
	_ = binary.Write(buf, binary.BigEndian, uint16(len(packet.Value)))
	buf.Write(packet.Value)
	return buf.Bytes()
}

func DecodeTLV(r io.Reader) (*TLVPacket, error) {
	var tag uint8
	if err := binary.Read(r, binary.BigEndian, &tag); err != nil {
		return nil, err
	}

	var length uint16
	if err := binary.Read(r, binary.BigEndian, &length); err != nil {
		return nil, err
	}

	val := make([]byte, length)
	if _, err := io.ReadFull(r, val); err != nil {
		return nil, errors.New("TLV Value to'liq o'qilmadi")
	}

	return &TLVPacket{Tag: tag, Length: length, Value: val}, nil
}
```
**Tushuntirish:** TLV protokollari o'zining moslashuvchanligi bilan mashhur: qabul qiluvchi tomon o'ziga notanish Tag (Type) uchrasa, Length bo'yicha baytlarni o'tkazib yuborib keyingi paketni buzmasdan o'qishda davom etadi.

---

### Topshiriq #1135: TLS SNI (Server Name Indication) asosida ulanishlarni yo'naltiruvchi proksi
**Tavsif:** Shifrlangan TLS paketlarini ochmasdan, mijozning ClientHello sarlavhasidagi domenni aniqlab tegishli backend serveriga yo'naltiruvchi SNI Passthrough proksi quring.
**Talablar:** TLS ClientHello parslash, Server Name Indication kengaytmasini o'qish.
**Yechim (Go):**
```go
package main

import (
	"crypto/tls"
	"fmt"
	"net"
)

func InspectSNI(conn net.Conn) (string, error) {
	// TLS Client Hello sarlavhasini tutib olish uchun maxsus interfeys
	serverName := ""
	config := &tls.Config{
		GetConfigForClient: func(hello *tls.ClientHelloInfo) (*tls.Config, error) {
			serverName = hello.ServerName
			return nil, fmt.Errorf("SNI qabul qilindi: %s", serverName)
		},
	}

	tlsConn := tls.Server(conn, config)
	_ = tlsConn.Handshake()

	return serverName, nil
}
```
**Tushuntirish:** SNI proksi serverga SSL sertifikatlarining shaxsiy kalitlari kerak bo'lmaydi. U bitta IP manzil orqali yuzlab domenlarga ega ichki klasterlarga yo'l ochadi.

---

### Topshiriq #1136: HTTP/2 multiplexing va Server Push boshqaruvi
**Tavsif:** Brauzer asosiy HTML sahifani so'raganda, unga kerak bo'ladigan CSS va rasm fayllarini alohida so'rov kutmasdan darhol oldindan yuboruvchi HTTP/2 Server Push yarating.
**Talablar:** `http.Pusher` interfeysi, HTTP/2 ulanishini tekshirish va push qilish.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	// Mijoz HTTP/2 Push qo'llab-quvvatlashini tekshiramiz
	if pusher, ok := w.(http.Pusher); ok {
		options := &http.PushOptions{
			Header: http.Header{
				"Accept-Encoding": r.Header["Accept-Encoding"],
			},
		}
		// CSS resursini oldindan mijozga itarib jo'natamiz
		if err := pusher.Push("/static/style.css", options); err != nil {
			fmt.Printf("Push xatosi: %v\n", err)
		}
	}

	w.Header().Set("Content-Type", "text/html")
	fmt.Fprintf(w, `<html><head><link rel="stylesheet" href="/static/style.css"></head><body><h1>Salom Khorazmiy AI!</h1></body></html>`)
}
```
**Tushuntirish:** HTTP/2 Server Push sahifaning birinchi yuklanish vaqtini (First Contentful Paint) ancha tezlashtiradi, chunki brauzer HTML ni parslab CSS so'raguncha, fayl allaqachon tarmoqdan yetib kelgan bo'ladi.

---

### Topshiriq #1137: HTTP Hijacking orqali TCP ulanishini to'liq nazoratga olish
**Tavsif:** Standart HTTP handleri ichida ulanishni oddiy HTTP javobidan uzib, xom TCP soketini o'z qo'lingizga oling va shaxsiy protokolingizni ishga tushiring.
**Talablar:** `http.Hijacker` interfeysi, `Hijack()` chaqirig'i, bufio buferlarini tozalash.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"net/http"
)

func hijackHandler(w http.ResponseWriter, r *http.Request) {
	hijacker, ok := w.(http.Hijacker)
	if !ok {
		http.Error(w, "Webserver hijackingni qo'llab-quvvatlamaydi", http.StatusInternalServerError)
		return
	}

	conn, bufrw, err := hijacker.Hijack()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer conn.Close()

	// Endi bizda to'liq nazorat ostidagi xom TCP soket bor!
	_, _ = bufrw.WriteString("HTTP/1.1 200 OK\r\nCustom-Protocol: Activated\r\n\r\n")
	_ = bufrw.Flush()

	_, _ = conn.Write([]byte("MAXSUS_BINAR_MA'LUMOT"))
}
```
**Tushuntirish:** HTTP Hijacking WebSocket va HTTP CONNECT tunnelari qanday qilib oddiy HTTP portida boshlanib, keyinchalik xom bayt oqimiga aylanishining asosiy siridir.

---

### Topshiriq #1138: Tarmoq trafigini siqish (compress/gzip bilan streaming HTTP compression)
**Tavsif:** Katta hajmdagi JSON yoki matnli API javoblarini oqim (streaming) tarzida real-vaqtda gzip bilan siqib, tarmoq yuklamasini 70-80% ga kamaytiruvchi middleware yozing.
**Talablar:** `compress/gzip`, `http.ResponseWriter` wrapper, `Content-Encoding: gzip`.
**Yechim (Go):**
```go
package main

import (
	"compress/gzip"
	"io"
	"net/http"
	"strings"
)

type gzipResponseWriter struct {
	io.Writer
	http.ResponseWriter
}

func (w gzipResponseWriter) Write(b []byte) (int, error) {
	return w.Writer.Write(b)
}

func GzipMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if !strings.Contains(r.Header.Get("Accept-Encoding"), "gzip") {
			next.ServeHTTP(w, r)
			return
		}

		w.Header().Set("Content-Encoding", "gzip")
		gz := gzip.NewWriter(w)
		defer gz.Close()

		gzWriter := gzipResponseWriter{Writer: gz, ResponseWriter: w}
		next.ServeHTTP(gzWriter, r)
	})
}
```
**Tushuntirish:** Oqimli gzip middleware ma'lumotlarni xotirada to'liq jamlamasdan bo'lakma-bo'lak siqib uzatadi. Bu esa xotira sarfini minimal darajada saqlaydi.

---

### Topshiriq #1139: Tarmoq paketlari yaxlitligini tekshirish (CRC32 checksum framing)
**Tavsif:** Sanoat tarmoqlarida shovqin va xatolar sababli baytlar buzilib qolishini aniqlash uchun har bir paket orqasiga IEEE standartidagi 4 baytli CRC32 nazorat summasini biriktiring.
**Talablar:** `hash/crc32`, paket tuzish va nazorat summasini tekshirish.
**Yechim (Go):**
```go
package main

import (
	"encoding/binary"
	"errors"
	"hash/crc32"
)

func CreateChecksummedPacket(payload []byte) []byte {
	checksum := crc32.ChecksumIEEE(payload)
	packet := make([]byte, len(payload)+4)
	copy(packet, payload)
	binary.BigEndian.PutUint32(packet[len(payload):], checksum)
	return packet
}

func VerifyAndExtractPayload(packet []byte) ([]byte, error) {
	if len(packet) < 4 {
		return nil, errors.New("paket o'lchami juda qisqa")
	}

	payload := packet[:len(packet)-4]
	expectedChecksum := binary.BigEndian.Uint32(packet[len(packet)-4:])
	actualChecksum := crc32.ChecksumIEEE(payload)

	if actualChecksum != expectedChecksum {
		return nil, errors.New("xatolik: CRC32 tekshiruvi muvaffaqiyatsiz! Ma'lumot buzilgan")
	}

	return payload, nil
}
```
**Tushuntirish:** CRC32 nazorat summasi tarmoqda tushib qolgan yoki o'zgargan baytlarni mikrosekund ichida aniqlashga xizmat qiladi va shikastlangan paketlarning biznes logikaga o'tishini to'xtatadi.

---

### Topshiriq #1140: Katta hajmli fayllarni Chunked Transfer Encoding orqali oqimli uzatish
**Tavsif:** Hajmi oldindan ma'lum bo'lmagan oqimli ma'lumotlarni (masalan, videokamera oqimi yoki dinamik hisobot) HTTP/1.1 `Transfer-Encoding: chunked` orqali uzating.
**Talablar:** `http.Flusher` interfeysi, doimiy bo'laklarni chiqarish (flush).
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

func streamReportHandler(w http.ResponseWriter, r *http.Request) {
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Oqimli uzatish qo'llab-quvvatlanmaydi", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	w.Header().Set("Transfer-Encoding", "chunked")

	for i := 1; i <= 5; i++ {
		fmt.Fprintf(w, "Hisobot bo'lagi #%d: ma'lumotlar qayta ishlandi...\n", i)
		flusher.Flush() // Mijozga darhol yetkazish
		time.Sleep(1 * time.Second)
	}
}
```
**Tushuntirish:** `flusher.Flush()` buferdagi ma'lumotlarni darhol tarmoq orqali chiqarib yuboradi. Natijada mijoz server butun ishni tugatishini kutmasdan natijalarni darhol ko'rishni boshlaydi.

---

### Topshiriq #1141: UDP Paketlarining fragmentatsiyasi va qayta yig'ilishi (Reassembly)
**Tavsif:** Katta UDP xabarlari MTU (1500 bayt) dan oshganda tarmoqda yo'qolib ketmasligi uchun ularni dasturiy darajada bo'laklab jo'natuvchi va qabul qiluvchi tomonda to'g'ri yig'uvchi modul tuzing.
**Talablar:** Fragment Header (MsgID, ChunkIndex, TotalChunks), oqimni qayta tiklash.
**Yechim (Go):**
```go
package main

import (
	"bytes"
	"encoding/binary"
	"sync"
)

type UDPChunkHeader struct {
	MsgID       uint32
	ChunkIndex  uint16
	TotalChunks uint16
}

type PacketReassembler struct {
	mu     sync.Mutex
	chunks map[uint32]map[uint16][]byte
}

func NewReassembler() *PacketReassembler {
	return &PacketReassembler{chunks: make(map[uint32]map[uint16][]byte)}
}

func (r *PacketReassembler) AddChunk(hdr UDPChunkHeader, data []byte) []byte {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, ok := r.chunks[hdr.MsgID]; !ok {
		r.chunks[hdr.MsgID] = make(map[uint16][]byte)
	}
	r.chunks[hdr.MsgID][hdr.ChunkIndex] = data

	if len(r.chunks[hdr.MsgID]) == int(hdr.TotalChunks) {
		var fullMsg bytes.Buffer
		for i := uint16(0); i < hdr.TotalChunks; i++ {
			fullMsg.Write(r.chunks[hdr.MsgID][i])
		}
		delete(r.chunks, hdr.MsgID)
		return fullMsg.Bytes()
	}
	return nil
}
```
**Tushuntirish:** UDP o'z holicha ishonchsiz protokol bo'lgani sababli dasturchilar yuqori unumdorlik va ishonchlilikni birlashtirish uchun o'zlarining mini transport mexanizmlarini yaratadilar.

---

### Topshiriq #1142: gRPC Health Checking Protocol (grpc/health/v1)
**Tavsif:** Kubernetes klasterida ishlayotgan Go gRPC mikroxizmati o'z holatini (Liveness/Readiness probe) rasmiy gRPC standarti bo'yicha taqdim etuvchi health xizmatini yoqing.
**Talablar:** `google.golang.org/grpc/health`, `grpc_health_v1.HealthServer`.
**Yechim (Go):**
```go
package main

import (
	"net"
	"google.golang.org/grpc"
	"google.golang.org/grpc/health"
	"google.golang.org/grpc/health/grpc_health_v1"
)

func main() {
	lis, _ := net.Listen("tcp", ":50051")
	grpcServer := grpc.NewServer()

	// Rasmiy Health Serverni yaratamiz
	healthServer := health.NewServer()
	grpc_health_v1.RegisterHealthServer(grpcServer, healthServer)

	// Xizmatimiz holatini SERVING deb belgilaymiz
	healthServer.SetServingStatus("payment.PaymentService", grpc_health_v1.HealthCheckResponse_SERVING)

	_ = grpcServer.Serve(lis)
}
```
**Tushuntirish:** Ushbu xizmat orqali orkestrator (masalan Kubernetes) mikroxizmat tayyor bo'lmaganda unga trafik yo'naltirishni to'xtatadi va nosoz xizmatlarni avtomatik qayta yuklaydi.

---

### Topshiriq #1143: gRPC Client Resolver va Round-Robin Load Balancing
**Tavsif:** Markaziy yuklama balanserisiz, gRPC mijozi bevosita bir nechta backend nusxalariga so'rovlarni Round-Robin usulida teng taqsimlashini sozlang.
**Talablar:** `grpc.WithDefaultServiceConfig`, Round-Robin siyosati.
**Yechim (Go):**
```go
package main

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func CreateBalancedGRPCConn() (*grpc.ClientConn, error) {
	// Round-Robin xizmat konfiguratsiyasi
	serviceConfig := `{"loadBalancingPolicy": "round_robin"}`

	conn, err := grpc.DialContext(
		context.Background(),
		"dns:///my-payment-service.internal:50051",
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithDefaultServiceConfig(serviceConfig),
	)
	return conn, err
}
```
**Tushuntirish:** gRPC mijozi barcha backend IP larini DNS orqali oladi va har bir RPC chaqirig'ini navbatdagi backendga yo'naltiradi. Bu ortiqcha proxy kechikishini bartaraf etadi.

---

### Topshiriq #1144: WebSocket klasterini Redis Pub/Sub yordamida gorizontal kengaytirish
**Tavsif:** Foydalanuvchilar har xil Go serverlariga ulangan holatda bitta serverga yuborilgan chat xabarini qolgan barcha serverlardagi WebSocket mijozlariga tarqating.
**Talablar:** `github.com/redis/go-redis/v9`, Redis `Publish` va `Subscribe`.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"github.com/redis/go-redis/v9"
)

func SubscribeRedisEvents(rdb *redis.Client, channel string, broadcastLocal func(string)) {
	ctx := context.Background()
	pubsub := rdb.Subscribe(ctx, channel)
	defer pubsub.Close()

	ch := pubsub.Channel()
	for msg := range ch {
		fmt.Printf("Redisdan xabar keldi: %s\n", msg.Payload)
		broadcastLocal(msg.Payload)
	}
}

func PublishRedisEvent(rdb *redis.Client, channel, msg string) error {
	return rdb.Publish(context.Background(), channel, msg).Err()
}
```
**Tushuntirish:** Stateless veb-serverlar arxitekturasida WebSocket ulanishlari mahalliy serverda ushlanadi, ammo global xabarlar Redis yoki Kafka orqali barcha tugunlarga yetkaziladi.

---

### Topshiriq #1145: sync.Pool yordamida Tarmoq Bayt Buferlarini qayta ishlatish (Zero-Allocation I/O)
**Tavsif:** Soniyasiga millionlab so'rovlar keladigan serverda doimiy yangi bayt massivlari (`make([]byte)`) yaratish natijasida Go Garbage Collectorining CPU ni to'ldirib yuborishini oldini oling.
**Talablar:** `sync.Pool`, buferni olish (`Get`), tozalash va qaytarish (`Put`).
**Yechim (Go):**
```go
package main

import (
	"sync"
)

var bufferPool = sync.Pool{
	New: func() interface{} {
		// 4 KB o'lchamdagi bufer yaratiladi
		buf := make([]byte, 4096)
		return &buf
	},
}

func ProcessNetworkData(data []byte) {
	// Hovuzdan mavjud buferni olamiz (Xotira ajratilmaydi!)
	bufPtr := bufferPool.Get().(*[]byte)
	buf := *bufPtr

	// Foydalanish
	copy(buf, data)

	// Tozalash va hovuzga qaytarish
	bufferPool.Put(bufPtr)
}
```
**Tushuntirish:** `sync.Pool` Go GC ning eng yaqin do'stidir. U xotiradagi o'lmas buferlarni qayta aylantirish orqali xotira ajratish (allocations/sec) sonini nolga yaqinlashtiradi.

---

### Topshiriq #1146: Epoll/Kqueue asosidagi Netpoll arxitekturasi va Worker Pool patterni
**Tavsif:** Cheklangan miqdordagi ishchi goroutinalar (Worker Pool) yordamida kiruvchi tarmoq topshiriqlarini navbat bilan bajaruvchi xavfsiz boshqaruv tizimini quring.
**Talablar:** Workerlar soni chegarasi (masalan 100), vazifalar kanali, goroutina sizishining oldini olish.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"net"
	"sync"
)

type WorkerPool struct {
	tasks chan net.Conn
	wg    sync.WaitGroup
}

func NewWorkerPool(workerCount, queueSize int) *WorkerPool {
	p := &WorkerPool{
		tasks: make(chan net.Conn, queueSize),
	}

	for i := 0; i < workerCount; i++ {
		p.wg.Add(1)
		go p.worker(i)
	}
	return p
}

func (p *WorkerPool) worker(id int) {
	defer p.wg.Done()
	for conn := range p.tasks {
		// Tarmoq ulanishiga xizmat ko'rsatish
		_, _ = conn.Write([]byte("Salom Worker Pool\n"))
		conn.Close()
	}
}

func (p *WorkerPool) Submit(conn net.Conn) {
	p.tasks <- conn
}
```
**Tushuntirish:** Worker Pool haddan tashqari ko'p goroutina ochilib server xotirasi va OS reestrlarining qulashini (resource starvation) oldini oladi.

---

### Topshiriq #1147: Tarmoq ulanishlari metrikalarini to'plash (Active Connections, Throughput)
**Tavsif:** Server monitoringi uchun faol ulanishlar soni va jami o'tgan baytlarni qulflarsiz (lock-free) hisoblab boruvchi yuqori tezlikdagi telemetriya datchigini yarating.
**Talablar:** `sync/atomic`, `AddInt64`, `LoadInt64`.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type ConnectionMetrics struct {
	activeConns int64
	bytesRead   int64
	bytesSent   int64
}

func (m *ConnectionMetrics) OnConnect()      { atomic.AddInt64(&m.activeConns, 1) }
func (m *ConnectionMetrics) OnDisconnect()   { atomic.AddInt64(&m.activeConns, -1) }
func (m *ConnectionMetrics) AddBytesRead(n int) { atomic.AddInt64(&m.bytesRead, int64(n)) }
func (m *ConnectionMetrics) AddBytesSent(n int) { atomic.AddInt64(&m.bytesSent, int64(n)) }

func (m *ConnectionMetrics) Report() string {
	return fmt.Sprintf("Faol ulanishlar: %d | O'qildi: %d bayt | Yuborildi: %d bayt",
		atomic.LoadInt64(&m.activeConns),
		atomic.LoadInt64(&m.bytesRead),
		atomic.LoadInt64(&m.bytesSent))
}
```
**Tushuntirish:** `sync/atomic` operatsiyalari CPU ning maxsus registr buyruqlari (masalan x86 dagi `LOCK XADD`) orqali bajariladi, bu esa mutexlarga nisbatan o'nlab barobar tezroq ishlaydi.

---

### Topshiriq #1148: Eksponentsial kechikish (Exponential Backoff with Jitter) bilan qayta ulanish
**Tavsif:** Tarmoq uzilganda mijoz serverga har safar kechikishni 2 barobar oshirib va tasodifiy jitter (chayqalish) qo'shib qayta bog'lanishini amalga oshiring.
**Talablar:** Boshlang'ich kechikish, maksimal kechikish, `math/rand` bilan jitter qo'shish.
**Yechim (Go):**
```go
package main

import (
	"math/rand"
	"time"
)

func CalculateBackoffWithJitter(attempt int, baseDelay, maxDelay time.Duration) time.Duration {
	// Eksponentsial o'sish: base * 2^attempt
	multiplier := 1 << attempt
	delay := baseDelay * time.Duration(multiplier)
	if delay > maxDelay || delay <= 0 {
		delay = maxDelay
	}

	// Full Jitter: 0 dan hisoblangan delaygacha tasodifiy oraliq
	jitter := time.Duration(rand.Int63n(int64(delay)))
	return jitter
}
```
**Tushuntirish:** Jitter barcha uzilgan mijozlarning bir vaqtda qayta ulanishga urinishini tarqatib yuboradi va serverga "Thundering Herd" hujumi bo'lishidan asraydi.

---

### Topshiriq #1149: Tarmoq paketlarini AES-GCM orqali apparat darajasida shifrlash
**Tavsif:** Tarmoqda uzatilayotgan binar paketlarni AES-GCM AEAD algoritmi orqali shifrlash va ularning haqiqiyligini tekshiruvchi modul yozing.
**Talablar:** `crypto/aes`, `crypto/cipher`, `cipher.NewGCM`, Nonce generatsiyasi.
**Yechim (Go):**
```go
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"errors"
	"io"
)

func EncryptPacketAESGCM(key, plaintext []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	nonce := make([]byte, gcm.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, err
	}

	// Nonce paket boshiga biriktiriladi
	ciphertext := gcm.Seal(nonce, nonce, plaintext, nil)
	return ciphertext, nil
}

func DecryptPacketAESGCM(key, ciphertext []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	nonceSize := gcm.NonceSize()
	if len(ciphertext) < nonceSize {
		return nil, errors.New("shifrlangan ma'lumot juda qisqa")
	}

	nonce, encryptedData := ciphertext[:nonceSize], ciphertext[nonceSize:]
	return gcm.Open(nil, nonce, encryptedData, nil)
}
```
**Tushuntirish:** Zamonaviy CPU larda AES-NI apparat instruksiyalari mavjud bo'lib, AES-GCM algoritmi gigabaytlab ma'lumotlarni protsessor yuklamasisiz tezkor shifrlash imkonini beradi.

---

### Topshiriq #1150: Leaky Bucket algoritmi bilan tarmoq o'tkazuvchanligini tekislash (Traffic Shaping)
**Tavsif:** Tarmoq orqali chiquvchi paketlar oqimini bir tekis (smooth) tezlikda uzatuvchi va keskin sakrashlarni tartibga soluvchi Leaky Bucket algoritmini yarating.
**Talablar:** Qat'iy oqish tezligi (leak rate), bufer chegarasi, to'lib ketganda paketlarni rad etish.
**Yechim (Go):**
```go
package main

import (
	"sync"
	"time"
)

type LeakyBucket struct {
	mu           sync.Mutex
	capacity     float64
	waterLevel   float64
	leakRate     float64 // Sekundiga oqadigan miqdor
	lastLeakTime time.Time
}

func NewLeakyBucket(capacity, leakRatePerSec float64) *LeakyBucket {
	return &LeakyBucket{
		capacity:     capacity,
		leakRate:     leakRatePerSec,
		lastLeakTime: time.Now(),
	}
}

func (lb *LeakyBucket) Add(packetSize float64) bool {
	lb.mu.Lock()
	defer lb.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(lb.lastLeakTime).Seconds()
	lb.lastLeakTime = now

	// O'tgan vaqt hisobiga suv sathini kamaytiramiz
	lb.waterLevel = lb.waterLevel - elapsed*lb.leakRate
	if lb.waterLevel < 0 {
		lb.waterLevel = 0
	}

	// Yangi paket sig'adimi?
	if lb.waterLevel+packetSize <= lb.capacity {
		lb.waterLevel += packetSize
		return true // Paket qabul qilindi
	}

	return false // Paket tashlab yuborildi (Drop)
}
```
**Tushuntirish:** Leaky Bucket tarmoqdagi paketlar tirbandligini (congestion) oldini olish uchun chiquvchi trafigini tekislashda eng samarali algoritmdir.

---

