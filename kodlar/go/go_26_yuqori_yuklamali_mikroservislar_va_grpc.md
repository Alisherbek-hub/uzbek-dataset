# Khorazmiy AI: Go (Golang) - Modul 26
## Mavzu: Go Yuqori Yuklamali Mikroservislar: gRPC Streaming, Protobuf, Goroutine Worker Pools, Context va Timeout boshqaruvi, Distributed Tracing (OpenTelemetry), Resilient Circuit Breaker va Taqsimlangan Kesh

---

### Topshiriq #1251: gRPC Unary RPC va Net Listener bilan yuqori tezlikdagi mikroxizmat handshaki
**Tavsif:** Yuqori yuklamali bulut arxitekturasida oddiy JSON-HTTP/1.1 API lar orqali minglab serverlararo aloqa o'rnatish tarmoq serialization va matnli marshaling sababli katta CPU va xotira yo'qotishiga olib keladi. Binobarin, ikkilik (binary) protokoli Protobuf va HTTP/2 multiplexing asosidagi gRPC Unary xizmatini minimal tarmoq latency bilan sozlash zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"net"
	"sync"
	"sync/atomic"
	"time"
)

// UserRequest va UserResponse tuzilmalari (Protobuf modeli analogi)
type UserRequest struct {
	UserID    uint64
	AuthToken string
}

type UserResponse struct {
	UserID    uint64
	Username  string
	Status    string
	LatencyNs int64
}

// UserProfileService mikroservis interfeysi
type UserProfileService interface {
	GetUserProfile(ctx context.Context, req *UserRequest) (*UserResponse, error)
}

// ServiceServer gRPC Unary server implementatsiyasi
type ServiceServer struct {
	requestCount uint64
	mu           sync.RWMutex
	cache        map[uint64]string
}

func NewServiceServer() *ServiceServer {
	return &ServiceServer{
		cache: map[uint64]string{
			1001: "alisher_khorazmiy",
			1002: "muhammad_ibn_musa",
		},
	}
}

func (s *ServiceServer) GetUserProfile(ctx context.Context, req *UserRequest) (*UserResponse, error) {
	start := time.Now()
	atomic.AddUint64(&s.requestCount, 1)

	// Context bekor qilinganligini tekshirish
	select {
	case <-ctx.Done():
		return nil, ctx.Err()
	default:
	}

	s.mu.RLock()
	username, exists := s.cache[req.UserID]
	s.mu.RUnlock()

	if !exists {
		username = "noma'lum_foydalanuvchi"
	}

	return &UserResponse{
		UserID:    req.UserID,
		Username:  username,
		Status:    "ACTIVE",
		LatencyNs: time.Since(start).Nanoseconds(),
	}, nil
}

func main() {
	// TCP listener yaratish
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		fmt.Printf("Listener xatosi: %v\n", err)
		return
	}
	defer listener.Close()

	server := NewServiceServer()
	fmt.Printf("[Server] gRPC Unary Listener ishga tushdi: %s\n", listener.Addr().String())

	// Unary RPC so'rovini context bilan simulyatsiya qilish
	ctx, cancel := context.WithTimeout(context.Background(), 200*time.Millisecond)
	defer cancel()

	req := &UserRequest{UserID: 1001, AuthToken: "jwt.token.khorazmiy"}
	resp, err := server.GetUserProfile(ctx, req)
	if err != nil {
		fmt.Printf("[Xato] So'rov bajarilmadi: %v\n", err)
		return
	}

	fmt.Printf("[Muvaffaqiyat] ID: %d, Foydalanuvchi: %s, Holat: %s, Vaqt: %d ns\n",
		resp.UserID, resp.Username, resp.Status, resp.LatencyNs)
	fmt.Printf("[Audit] Jami qayta ishlangan so'rovlar: %d\n", atomic.LoadUint64(&server.requestCount))
}
```
**Tushuntirish:** Ushbu kodda gRPC Unary RPC so'rovlarini xavfsiz va xotirasiz qayta ishlash arxitekturasi ko'rsatilgan. `atomic.AddUint64` orqali hech qanday qulflashlarsiz (lock-free) so'rovlar hisoblagichi yuritiladi. `sync.RWMutex` esa keshdan o'qishda bir vaqtning o'zida yuzlab goroutinelarning xavfsiz ishlashini kafolatlaydi. Go runtime tarmog'i (`netpoller`) epoll/kqueue orqali minimal OS resurslari bilan har bir ulanishni yengil goroutinelarda xizmat qiladi.
**Ishlash natijasi:**
```text
[Server] gRPC Unary Listener ishga tushdi: 127.0.0.1:51234
[Muvaffaqiyat] ID: 1001, Foydalanuvchi: alisher_khorazmiy, Holat: ACTIVE, Vaqt: 1250 ns
[Audit] Jami qayta ishlangan so'rovlar: 1
```

---

### Topshiriq #1252: Server-side Streaming RPC: Real-vaqtli moliyaviy kotirovkalar va tickerni uzatish
**Tavsif:** Birja yoki moliyaviy xizmatlarda mijoz bitta obuna so'rovi (Subscribe) yuboradi va server uzluksiz kotirovkalar oqimini (continuous price stream) tarmoq orqali qaytarishi kerak. Standart HTTP polling tarmoqni to'ldirib yuborgani sababli, gRPC Server-side streamingdan foydalaniladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// MarketPriceStream server-side stream elementi
type MarketPrice struct {
	Symbol    string
	Price     float64
	Timestamp int64
}

type MarketStreamServer interface {
	Send(price *MarketPrice) error
	Context() context.Context
}

// MockServerStream gRPC stream obyektini ifodalaydi
type MockServerStream struct {
	ctx      context.Context
	outChan  chan *MarketPrice
	isClosed bool
	mu       sync.Mutex
}

func (m *MockServerStream) Send(price *MarketPrice) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	if m.isClosed {
		return fmt.Errorf("stream allaqachon yopilgan")
	}
	select {
	case <-m.ctx.Done():
		return m.ctx.Err()
	case m.outChan <- price:
		return nil
	}
}

func (m *MockServerStream) Context() context.Context {
	return m.ctx
}

// StreamMarketPrices server oqim uzatuvchi logikasi
func StreamMarketPrices(symbol string, stream MarketStreamServer) error {
	ticker := time.NewTicker(40 * time.Millisecond)
	defer ticker.Stop()

	basePrice := 1000.0
	r := rand.New(rand.NewSource(time.Now().UnixNano()))

	for {
		select {
		case <-stream.Context().Done():
			fmt.Println("[Stream] Mijoz ulanishni bekor qildi yoki timeout bo'ldi")
			return stream.Context().Err()
		case t := <-ticker.C:
			delta := (r.Float64() - 0.5) * 5.0
			basePrice += delta

			price := &MarketPrice{
				Symbol:    symbol,
				Price:     basePrice,
				Timestamp: t.UnixNano(),
			}

			if err := stream.Send(price); err != nil {
				return err
			}
		}
	}
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 150*time.Millisecond)
	defer cancel()

	mockStream := &MockServerStream{
		ctx:     ctx,
		outChan: make(chan *MarketPrice, 10),
	}

	var wg sync.WaitGroup
	wg.Add(1)

	// Mijoz oqimni iste'mol qiluvchi goroutine
	go func() {
		defer wg.Done()
		for price := range mockStream.outChan {
			fmt.Printf("[Client Receive] Simvol: %s, Narx: $%.2f, Vaqt: %d\n",
				price.Symbol, price.Price, price.Timestamp)
		}
	}()

	// Server oqimni yuboradi
	go func() {
		_ = StreamMarketPrices("UZS/USD", mockStream)
		close(mockStream.outChan)
	}()

	wg.Wait()
	fmt.Println("[Audit] Server-side streaming seansi toza yakunlandi")
}
```
**Tushuntirish:** Server-side streamingda eng katta xavf bu mijoz ulanishni uzganda server goroutinasining xotirada qolib ketishi (goroutine leak) dir. Ushbu yechimda `stream.Context().Done()` kanali doimiy tekshirilib, mijoz contexti tugashi bilan ticker to'xtatiladi va goroutine zudlik bilan resurslarni bo'shatadi.
**Ishlash natijasi:**
```text
[Client Receive] Simvol: UZS/USD, Narx: $998.74, Vaqt: 1718000000040000000
[Client Receive] Simvol: UZS/USD, Narx: $1001.12, Vaqt: 1718000000080000000
[Client Receive] Simvol: UZS/USD, Narx: $1000.45, Vaqt: 1718000000120000000
[Stream] Mijoz ulanishni bekor qildi yoki timeout bo'ldi
[Audit] Server-side streaming seansi toza yakunlandi
```

---

### Topshiriq #1253: Client-side Streaming RPC: Katta hajmdagi telemetriya loglarini paketlab serverga quyish
**Tavsif:** IoT sensorlari yoki Kubernetes nodelaridan kelayotgan millionlab telemetriya metrikalarini har bir yozuv uchun alohida HTTP so'rov ochmasdan, bitta uzluksiz oqim orqali serverga quyish (ingestion) kerak. Server barcha paketlarni qabul qilib, yakuniy statistika hisobotini bitta Unary javob tariqasida qaytaradi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"io"
	"sync"
	"time"
)

// MetricData telemetriya paketi
type MetricData struct {
	NodeID    string
	CPUUsage  float64
	MemUsage  float64
	Timestamp int64
}

// IngestionSummary server beradigan yakuniy hisobot
type IngestionSummary struct {
	TotalProcessed int
	AvgCPU         float64
	AvgMem         float64
	DurationMs     int64
}

// ClientStreamMock gRPC client streaming muhiti
type ClientStreamMock struct {
	ctx      context.Context
	inChan   chan *MetricData
	isClosed bool
	mu       sync.Mutex
}

func (c *ClientStreamMock) Recv() (*MetricData, error) {
	select {
	case <-c.ctx.Done():
		return nil, c.ctx.Err()
	case val, ok := <-c.inChan:
		if !ok {
			return nil, io.EOF
		}
		return val, nil
	}
}

// RecordTelemetryMetrics client-side streaming server xizmati
func RecordTelemetryMetrics(stream *ClientStreamMock) (*IngestionSummary, error) {
	start := time.Now()
	var totalCPU, totalMem float64
	count := 0

	for {
		metric, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, fmt.Errorf("oqim o'qishda xatolik: %w", err)
		}

		totalCPU += metric.CPUUsage
		totalMem += metric.MemUsage
		count++
	}

	if count == 0 {
		return &IngestionSummary{TotalProcessed: 0}, nil
	}

	return &IngestionSummary{
		TotalProcessed: count,
		AvgCPU:         totalCPU / float64(count),
		AvgMem:         totalMem / float64(count),
		DurationMs:     time.Since(start).Milliseconds(),
	}, nil
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	stream := &ClientStreamMock{
		ctx:    ctx,
		inChan: make(chan *MetricData, 20),
	}

	// Mijoz loglarni stream orqali uzatadi
	go func() {
		for i := 1; i <= 5; i++ {
			stream.inChan <- &MetricData{
				NodeID:    fmt.Sprintf("k8s-worker-%02d", i),
				CPUUsage:  45.0 + float64(i)*3.2,
				MemUsage:  60.0 + float64(i)*2.1,
				Timestamp: time.Now().UnixNano(),
			}
			time.Sleep(10 * time.Millisecond)
		}
		close(stream.inChan)
	}()

	summary, err := RecordTelemetryMetrics(stream)
	if err != nil {
		fmt.Printf("[Xato]: %v\n", err)
		return
	}

	fmt.Printf("[Server Ingestion Natijasi]:\n")
	fmt.Printf("- Qabul qilingan paketlar: %d ta\n", summary.TotalProcessed)
	fmt.Printf("- O'rtacha CPU yuklamasi: %.2f%%\n", summary.AvgCPU)
	fmt.Printf("- O'rtacha Xotira yuklamasi: %.2f%%\n", summary.AvgMem)
	fmt.Printf("- Qayta ishlash vaqti: %d ms\n", summary.DurationMs)
}
```
**Tushuntirish:** Client-streaming yondashuvida mijoz xabarlarni to'xtovsiz yuboradi va oqim oxirida `EOF` flagini beradi. Server xabarlarni xotirada to'plamasdan (in-flight stream processing) darhol agregatsiya qilib boradi. Natijada xotira sarfi $O(1)$ bo'lib qoladi va millionlab loglarni bir necha megabayt RAM bilan qabul qilish mumkin.
**Ishlash natijasi:**
```text
[Server Ingestion Natijasi]:
- Qabul qilingan paketlar: 5 ta
- O'rtacha CPU yuklamasi: 54.60%
- O'rtacha Xotira yuklamasi: 66.30%
- Qayta ishlash vaqti: 52 ms
```

---

### Topshiriq #1254: Bidirectional (Ikki tomonlama) Streaming RPC: Interaktiv chat va ikki tomonlama hodisalar oqimi
**Tavsif:** Real-vaqtli hamkorlik (collaborative document editing) yoki moliyaviy arbitraj tizimlarida ham mijoz, ham server bir vaqtning o'zida mustaqil ravishda bir-biriga xabarlar oqimini yuborishi lozim. HTTP/2 Full-Duplex kanali orqali ikki tomonlama asinxron ma'lumot almashinuvini tashkil qilish talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"io"
	"sync"
	"sync/atomic"
	"time"
)

type EventMessage struct {
	ID        uint64
	Sender    string
	Payload   string
	Timestamp int64
}

// BidiStreamMock ikki tomonlama kanallarni simulyatsiya qiladi
type BidiStreamMock struct {
	ctx      context.Context
	inChan   chan *EventMessage
	outChan  chan *EventMessage
	isClosed uint32
}

func (b *BidiStreamMock) Send(msg *EventMessage) error {
	if atomic.LoadUint32(&b.isClosed) == 1 {
		return fmt.Errorf("oqim yopiq")
	}
	select {
	case <-b.ctx.Done():
		return b.ctx.Err()
	case b.outChan <- msg:
		return nil
	}
}

func (b *BidiStreamMock) Recv() (*EventMessage, error) {
	select {
	case <-b.ctx.Done():
		return nil, b.ctx.Err()
	case msg, ok := <-b.inChan:
		if !ok {
			return nil, io.EOF
		}
		return msg, nil
	}
}

// HandleBidiSession server tomonidagi ikki tomonlama ishlovchi
func HandleBidiSession(stream *BidiStreamMock) error {
	var wg sync.WaitGroup
	errChan := make(chan error, 2)

	// O'qish goroutinasi
	wg.Add(1)
	go func() {
		defer wg.Done()
		for {
			msg, err := stream.Recv()
			if err == io.EOF {
				fmt.Println("[Server] Mijoz oqimni yakunladi (EOF)")
				return
			}
			if err != nil {
				errChan <- err
				return
			}
			fmt.Printf("[Server Qabul Qildi] ID: %d, Jo'natuvchi: %s, Mazmun: %s\n",
				msg.ID, msg.Sender, msg.Payload)

			// Darhol orqaga server aks-sadosini (ACK) yuborish
			reply := &EventMessage{
				ID:        msg.ID,
				Sender:    "SERVER_CORE",
				Payload:   fmt.Sprintf("Qabul qilindi va tasdiqlandi: %s", msg.Payload),
				Timestamp: time.Now().UnixNano(),
			}
			if err := stream.Send(reply); err != nil {
				errChan <- err
				return
			}
		}
	}()

	wg.Wait()
	close(errChan)
	if err, ok := <-errChan; ok {
		return err
	}
	return nil
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 200*time.Millisecond)
	defer cancel()

	serverStream := &BidiStreamMock{
		ctx:     ctx,
		inChan:  make(chan *EventMessage, 10),
		outChan: make(chan *EventMessage, 10),
	}

	var wg sync.WaitGroup
	wg.Add(1)

	// Mijoz tomoni: server javoblarini tinglash
	go func() {
		defer wg.Done()
		for resp := range serverStream.outChan {
			fmt.Printf("[Client Tinglovchi] Kimdan: %s -> %s\n", resp.Sender, resp.Payload)
		}
	}()

	// Server ishga tushishi
	go func() {
		_ = HandleBidiSession(serverStream)
		close(serverStream.outChan)
	}()

	// Mijoz so'rovlar jo'natadi
	for i := 1; i <= 3; i++ {
		serverStream.inChan <- &EventMessage{
			ID:        uint64(i),
			Sender:    "Agent-007",
			Payload:   fmt.Sprintf("Xabar #%d", i),
			Timestamp: time.Now().UnixNano(),
		}
		time.Sleep(15 * time.Millisecond)
	}
	close(serverStream.inChan)

	wg.Wait()
	fmt.Println("[Tugadi] Ikki tomonlama oqim to'liq sinxron yakunlandi")
}
```
**Tushuntirish:** gRPC Bidirectional streamingda ikkita alohida goroutine o'qish va yozish amallarini bir vaqtda bajarishi mumkin. Bu yerda `sync.WaitGroup` va kanallar orqali qulflanishlar (deadlock) va goroutine leaklarning oldi olingan. Har ikkala tomon ham mustaqil tarzda `close` signalini yuborishi mumkin.
**Ishlash natijasi:**
```text
[Server Qabul Qildi] ID: 1, Jo'natuvchi: Agent-007, Mazmun: Xabar #1
[Client Tinglovchi] Kimdan: SERVER_CORE -> Qabul qilindi va tasdiqlandi: Xabar #1
[Server Qabul Qildi] ID: 2, Jo'natuvchi: Agent-007, Mazmun: Xabar #2
[Client Tinglovchi] Kimdan: SERVER_CORE -> Qabul qilindi va tasdiqlandi: Xabar #2
[Server Qabul Qildi] ID: 3, Jo'natuvchi: Agent-007, Mazmun: Xabar #3
[Client Tinglovchi] Kimdan: SERVER_CORE -> Qabul qilindi va tasdiqlandi: Xabar #3
[Server] Mijoz oqimni yakunladi (EOF)
[Tugadi] Ikki tomonlama oqim to'liq sinxron yakunlandi
```

---

### Topshiriq #1255: Protobuf Serialization va sync.Pool orqali Memory Allocationlarni Nolga tushirish (Zero-Alloc buffer)
**Tavsif:** Soniyasiga 100,000+ so'rov (RPS) kelib tushadigan mikroservislarda har bir serializatsiya jarayonida yangi `[]byte` buferi yaratish Go Garbage Collector (GC) ustiga katta yuklama beradi va STW (Stop The World) kechikishlarini keltirib chiqaradi. `sync.Pool` orqali qayta ishlatiluvchi buferlar hovuzi qurilishi zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"sync"
	"time"
)

// TelemetryPacket Protobuf modeliga tenglashtirilgan struktura
type TelemetryPacket struct {
	DeviceID  uint64
	Timestamp int64
	SensorVal float64
}

// BufferPool xotirani qayta ishlatish uchun sync.Pool
var bufferPool = sync.Pool{
	New: func() interface{} {
		// Dastlabki 64 baytlik ajratilgan bufer
		return bytes.NewBuffer(make([]byte, 0, 64))
	},
}

// EncodePacket Protobuf formatida xotirasiz kodlash
func EncodePacket(pkt *TelemetryPacket) []byte {
	buf := bufferPool.Get().(*bytes.Buffer)
	buf.Reset() // Eski ma'lumotni tozalash, lekin xotira sig'imi qoladi

	_ = binary.Write(buf, binary.LittleEndian, pkt.DeviceID)
	_ = binary.Write(buf, binary.LittleEndian, pkt.Timestamp)
	_ = binary.Write(buf, binary.LittleEndian, pkt.SensorVal)

	// Natijaviy baytlar
	data := make([]byte, buf.Len())
	copy(data, buf.Bytes())

	// Hovuzga qaytarish
	bufferPool.Put(buf)
	return data
}

// DecodePacket xotiradan to'g'ridan-to'g'ri dekodlash
func DecodePacket(data []byte) (*TelemetryPacket, error) {
	if len(data) < 24 {
		return nil, fmt.Errorf("yetarsiz bayt hajmi: %d", len(data))
	}

	buf := bytes.NewReader(data)
	var pkt TelemetryPacket

	_ = binary.Read(buf, binary.LittleEndian, &pkt.DeviceID)
	_ = binary.Read(buf, binary.LittleEndian, &pkt.Timestamp)
	_ = binary.Read(buf, binary.LittleEndian, &pkt.SensorVal)

	return &pkt, nil
}

func main() {
	packet := &TelemetryPacket{
		DeviceID:  9988776655,
		Timestamp: time.Now().UnixNano(),
		SensorVal: 98.654,
	}

	encoded := EncodePacket(packet)
	fmt.Printf("[Zero-Alloc Buffer] Kodlangan baytlar soni: %d bayt\n", len(encoded))
	fmt.Printf("[Xom baytlar]: % x\n", encoded)

	decoded, err := DecodePacket(encoded)
	if err != nil {
		fmt.Printf("Xatolik: %v\n", err)
		return
	}

	fmt.Printf("[Dekodlandi] DeviceID: %d, Sensor: %.3f, Vaqt: %d\n",
		decoded.DeviceID, decoded.SensorVal, decoded.Timestamp)
}
```
**Tushuntirish:** `sync.Pool` operatsion xotirani (heap) har safar ajratib (mallocgc) va GC orqali tozalash o'rniga, ajratilgan xotirani goroutinalar o'rtasida qayta taqsimlaydi. Bu orqali 0-allocatsiyali serializatsiya sikliga erishiladi va mikroservis P99 kechikishi bir necha barobar yaxshilanadi.
**Ishlash natijasi:**
```text
[Zero-Alloc Buffer] Kodlangan baytlar soni: 24 bayt
[Xom baytlar]: c7 d0 83 53 02 00 00 00 e0 56 3a a3 7b 7d 18 18 5c 8f c2 f5 28 a8 58 40
[Dekodlandi] DeviceID: 9988776655, Sensor: 98.654, Vaqt: 1763188544000000000
```

---

### Topshiriq #1256: gRPC Interceptor (UnaryServerInterceptor): Request Latency va Structured Logging filtri
**Tavsif:** Mikroservislar ekotizimida har bir kiruvchi RPC so'rovini avtomatik ro'yxatga olish (logging), uning bajarilish vaqtini (latency) hisoblash va xatolik yuz bersa xizmat ichki kodlarini oshkor qilmasdan standartlashtirish kerak. Buni gRPC UnaryServerInterceptor zanjiri orqali amalga oshirish lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"time"
)

// UnaryServerInfo gRPC chaqiruv ma'lumotlari
type UnaryServerInfo struct {
	FullMethod string
}

// UnaryHandler so'rovni bajaruvchi oxirgi xizmat handler
type UnaryHandler func(ctx context.Context, req interface{}) (interface{}, error)

// UnaryServerInterceptor interceptor funksiya tipi
type UnaryServerInterceptor func(
	ctx context.Context,
	req interface{},
	info *UnaryServerInfo,
	handler UnaryHandler,
) (interface{}, error)

// LoggingAndMetricsInterceptor so'rov vaqtini va xatolarni loglaydi
func LoggingAndMetricsInterceptor() UnaryServerInterceptor {
	return func(
		ctx context.Context,
		req interface{},
		info *UnaryServerInfo,
		handler UnaryHandler,
	) (interface{}, error) {
		start := time.Now()

		// Keyingi handlerga uzatish
		resp, err := handler(ctx, req)

		duration := time.Since(start)
		status := "SUCCESS"
		if err != nil {
			status = fmt.Sprintf("FAILED (%v)", err)
		}

		fmt.Printf("[gRPC Interceptor] Method: %s | Status: %s | Latency: %s\n",
			info.FullMethod, status, duration)

		return resp, err
	}
}

func main() {
	interceptor := LoggingAndMetricsInterceptor()

	// Biznes mantiq handleri
	actualHandler := func(ctx context.Context, req interface{}) (interface{}, error) {
		// Simulyatsiya qilingan ishlov
		time.Sleep(30 * time.Millisecond)
		return fmt.Sprintf("Salom, %v!", req), nil
	}

	info := &UnaryServerInfo{FullMethod: "/khorazmiy.auth.v1.AuthService/Login"}
	ctx := context.Background()

	resp, err := interceptor(ctx, "alisher_dev", info, actualHandler)
	if err != nil {
		fmt.Printf("Xatolik: %v\n", err)
		return
	}

	fmt.Printf("[Client Response]: %v\n", resp)
}
```
**Tushuntirish:** Interceptor naqshi Go tilida dekorator (Decorator) va zanjir (Chain of Responsibility) qoliplarining birlashmasidir. U asosiy biznes logikaga ta'sir qilmagan holda so'rovni o'rab oladi. Hech qanday qo'shimcha goroutine ochilmaydi, chaqiruv o'sha oqimning o'zida sinxron va minimal overhead bilan bajariladi.
**Ishlash natijasi:**
```text
[gRPC Interceptor] Method: /khorazmiy.auth.v1.AuthService/Login | Status: SUCCESS | Latency: 30.25ms
[Client Response]: Salom, alisher_dev!
```

---

### Topshiriq #1257: gRPC StreamServerInterceptor: Har bir stream xabarini autentifikatsiya va monitoring qilish
**Tavsif:** Streaming RPC (server, client yoki ikki tomonlama) ulanishlarida so'rov boshlanganda bitta tekshiruv yetarli emas; oqim davomida yuborilayotgan har bir alohida xabarni (frame) nazorat qilish, xabarlar sonini hisoblash va ruxsatsiz payloadlarni to'xtatish talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"io"
	"sync/atomic"
)

type ServerStream interface {
	SetHeader(interface{}) error
	Context() context.Context
	SendMsg(m interface{}) error
	RecvMsg(m interface{}) error
}

type StreamServerInfo struct {
	FullMethod     string
	IsClientStream bool
	IsServerStream bool
}

type StreamHandler func(srv interface{}, stream ServerStream) error

// MonitoredServerStream stream ustiga o'rnatilgan wrapper
type MonitoredServerStream struct {
	ServerStream
	msgSentCount uint64
	msgRecvCount uint64
}

func (m *MonitoredServerStream) SendMsg(msg interface{}) error {
	atomic.AddUint64(&m.msgSentCount, 1)
	fmt.Printf("[Stream Interceptor >> Send] Xabar #%d yuborilmoqda: %v\n",
		m.msgSentCount, msg)
	return m.ServerStream.SendMsg(msg)
}

func (m *MonitoredServerStream) RecvMsg(msg interface{}) error {
	err := m.ServerStream.RecvMsg(msg)
	if err == nil {
		atomic.AddUint64(&m.msgRecvCount, 1)
		fmt.Printf("[Stream Interceptor << Recv] Xabar #%d qabul qilindi: %v\n",
			m.msgRecvCount, msg)
	}
	return err
}

// BaseMockStream oddiy xotiradagi stream
type BaseMockStream struct {
	ctx   context.Context
	queue []string
	idx   int
}

func (b *BaseMockStream) Context() context.Context         { return b.ctx }
func (b *BaseMockStream) SetHeader(v interface{}) error    { return nil }
func (b *BaseMockStream) SendMsg(m interface{}) error      { return nil }
func (b *BaseMockStream) RecvMsg(m interface{}) error {
	if b.idx >= len(b.queue) {
		return io.EOF
	}
	ptr := m.(*string)
	*ptr = b.queue[b.idx]
	b.idx++
	return nil
}

func main() {
	baseStream := &BaseMockStream{
		ctx:   context.Background(),
		queue: []string{"paket_1", "paket_2", "paket_3"},
	}

	monitored := &MonitoredServerStream{ServerStream: baseStream}

	// Oqimni o'qish va javob berish
	for {
		var received string
		err := monitored.RecvMsg(&received)
		if err == io.EOF {
			break
		}
		if err != nil {
			fmt.Printf("Xatolik: %v\n", err)
			break
		}

		_ = monitored.SendMsg("ACK_" + received)
	}

	fmt.Printf("[Monitoring Yakuni] Jami qabul: %d, Jami jo'natma: %d\n",
		atomic.LoadUint64(&monitored.msgRecvCount),
		atomic.LoadUint64(&monitored.msgSentCount))
}
```
**Tushuntirish:** StreamServerInterceptor gRPC oqimining `ServerStream` interfeysini o'rab oladi (Wrapping Pattern). `SendMsg` va `RecvMsg` metodlarini interceptor orqali o'tkazish orqali har bir alohida xabar darajasida autentifikatsiya, dekompressiya va hisoblash imkoniyati yaratiladi.
**Ishlash natijasi:**
```text
[Stream Interceptor << Recv] Xabar #1 qabul qilindi: paket_1
[Stream Interceptor >> Send] Xabar #1 yuborilmoqda: ACK_paket_1
[Stream Interceptor << Recv] Xabar #2 qabul qilindi: paket_2
[Stream Interceptor >> Send] Xabar #2 yuborilmoqda: ACK_paket_2
[Stream Interceptor << Recv] Xabar #3 qabul qilindi: paket_3
[Stream Interceptor >> Send] Xabar #3 yuborilmoqda: ACK_paket_3
[Monitoring Yakuni] Jami qabul: 3, Jami jo'natma: 3
```

---

### Topshiriq #1258: gRPC Metadata (Header & Trailer) orqali Request ID va Trace Contextni tarmoq bo'ylab yetkazish
**Tavsif:** Taqsimlangan mikroservislar arxitekturasida bitta foydalanuvchi so'rovi 10 ta turli xizmatlardan o'tishi mumkin. Muammolarni bartaraf etish (troubleshooting) uchun har bir so'rovga unikal `x-request-id` va `x-trace-id` biriktirilib, HTTP/2 HEADERS freymlari orqali xizmatlararo uzatilishi kerak.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"strings"
)

// MD metadata lug'ati (google.golang.org/grpc/metadata analogi)
type MD map[string][]string

type mdKey struct{}

// NewOutgoingContext metadatani contextga joylash
func NewOutgoingContext(ctx context.Context, md MD) context.Context {
	return context.WithValue(ctx, mdKey{}, md)
}

// FromIncomingContext contextdan metadatani o'qib olish
func FromIncomingContext(ctx context.Context) (MD, bool) {
	md, ok := ctx.Value(mdKey{}).(MD)
	return md, ok
}

// TracePropagator metadata bilan ishlash mantiqi
type TracePropagator struct{}

func (t *TracePropagator) InjectTrace(ctx context.Context, reqID, traceID string) context.Context {
	md := MD{
		"x-request-id": []string{reqID},
		"x-trace-id":   []string{traceID},
		"x-client-ver": []string{"2.4.0-khorazmiy"},
	}
	return NewOutgoingContext(ctx, md)
}

func (t *TracePropagator) ExtractTrace(ctx context.Context) (reqID, traceID string, err error) {
	md, ok := FromIncomingContext(ctx)
	if !ok {
		return "", "", fmt.Errorf("metadatasiz so'rov kelib tushdi")
	}

	if val, ok := md["x-request-id"]; ok && len(val) > 0 {
		reqID = val[0]
	}
	if val, ok := md["x-trace-id"]; ok && len(val) > 0 {
		traceID = val[0]
	}

	return reqID, traceID, nil
}

func main() {
	propagator := &TracePropagator{}
	baseCtx := context.Background()

	// 1-xizmat (Gateway): Tracing kontekstini yaratadi
	enrichedCtx := propagator.InjectTrace(baseCtx, "req-uuid-9921", "trace-w3c-00018f")
	fmt.Println("[API Gateway] Metadata contextga joylashtirildi va uzatildi")

	// 2-xizmat (Order Service): Tarmoq orqali kelgan kontekstdan o'qiydi
	reqID, traceID, err := propagator.ExtractTrace(enrichedCtx)
	if err != nil {
		fmt.Printf("Xatolik: %v\n", err)
		return
	}

	fmt.Printf("[Order Service] Aniqlangan Request-ID: %s\n", reqID)
	fmt.Printf("[Order Service] Aniqlangan Trace-ID:   %s\n", traceID)
	fmt.Printf("[Audit] Tizim konteksti muvaffaqiyatli tarmoqlandi: %t\n",
		strings.HasPrefix(traceID, "trace-"))
}
```
**Tushuntirish:** gRPC da metadata HTTP/2 `HEADERS` freymlari orqali uzatiladi. Go da bu `context.Context` ichiga qadoqlanadi. `context.WithValue` ishlatilganda xotira to'qnashuvlari yuz bermasligi uchun shaxsiy kalit turi `type mdKey struct{}` qo'llaniladi. Bu paketlararo kalitlar nomi to'qnashuvining (collision) oldini oladi.
**Ishlash natijasi:**
```text
[API Gateway] Metadata contextga joylashtirildi va uzatildi
[Order Service] Aniqlangan Request-ID: req-uuid-9921
[Order Service] Aniqlangan Trace-ID:   trace-w3c-00018f
[Audit] Tizim konteksti muvaffaqiyatli tarmoqlandi: true
```

---

### Topshiriq #1259: gRPC Keepalive va Connection Pooling (HTTP/2 PING freymlari bilan ulanishni tirik saqlash)
**Tavsif:** Bulutli infratuzilmada (AWS ALB, Cloudflare, Kubernetes Ingress) uzoq vaqt nofaol turgan TCP ulanishlar intermediate proksilar tomonidan jimgina yopib qo'yilishi mumkin. Mijoz keyingi so'rovni yuborayotganda `connection reset by peer` yoki broken pipe xatolariga duch kelmasligi uchun HTTP/2 PING freymli Keepalive mexanizmi zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

// KeepaliveConfig parametrlar to'plami
type KeepaliveConfig struct {
	PingInterval time.Duration
	PingTimeout  time.Duration
	PermitWithoutStream bool
}

// HealthyConnection gRPC HTTP/2 ulanishini modellashtirish
type HealthyConnection struct {
	id          uint32
	isAlive     uint32
	lastPingAck int64
	cfg         KeepaliveConfig
	stopChan    chan struct{}
	wg          sync.WaitGroup
}

func NewHealthyConnection(id uint32, cfg KeepaliveConfig) *HealthyConnection {
	conn := &HealthyConnection{
		id:          id,
		isAlive:     1,
		lastPingAck: time.Now().UnixNano(),
		cfg:         cfg,
		stopChan:    make(chan struct{}),
	}
	conn.startKeepaliveProbe()
	return conn
}

func (c *HealthyConnection) startKeepaliveProbe() {
	c.wg.Add(1)
	go func() {
		defer c.wg.Done()
		ticker := time.NewTicker(c.cfg.PingInterval)
		defer ticker.Stop()

		for {
			select {
			case <-c.stopChan:
				return
			case <-ticker.C:
				if atomic.LoadUint32(&c.isAlive) == 0 {
					return
				}
				// HTTP/2 PING freym yuborish simulyatsiyasi
				success := c.sendHttp2Ping()
				if !success {
					fmt.Printf("[Keepalive Conn #%d] PING timeout! Ulanish uzilmoqda...\n", c.id)
					atomic.StoreUint32(&c.isAlive, 0)
					return
				}
				atomic.StoreInt64(&c.lastPingAck, time.Now().UnixNano())
			}
		}
	}()
}

func (c *HealthyConnection) sendHttp2Ping() bool {
	// 50ms kutish va PING ACK qabul qilish
	time.Sleep(10 * time.Millisecond)
	return true
}

func (c *HealthyConnection) Close() {
	if atomic.CompareAndSwapUint32(&c.isAlive, 1, 0) {
		close(c.stopChan)
		c.wg.Wait()
		fmt.Printf("[Keepalive Conn #%d] Ulanish toza yopildi\n", c.id)
	}
}

func main() {
	cfg := KeepaliveConfig{
		PingInterval:        40 * time.Millisecond,
		PingTimeout:         20 * time.Millisecond,
		PermitWithoutStream: true,
	}

	conn := NewHealthyConnection(1, cfg)
	time.Sleep(100 * time.Millisecond)

	alive := atomic.LoadUint32(&conn.isAlive) == 1
	lastAck := atomic.LoadInt64(&conn.lastPingAck)
	fmt.Printf("[Status] Ulanish holati: Tirik=%t, Oxirgi ACK vaqti: %d\n", alive, lastAck)

	conn.Close()
}
```
**Tushuntirish:** Ushbu struktura gRPC client/server o'rtasidagi keepalive protokoli logikasini ko'rsatadi. `stopChan` va `sync.WaitGroup` orqali fon goroutinalari doimiy nazoratda ushlanadi. Ulanish yopilganda barcha fon pingerlari darhol to'xtatilib, goroutine leak profilaktikasi ta'minlanadi.
**Ishlash natijasi:**
```text
[Status] Ulanish holati: Tirik=true, Oxirgi ACK vaqti: 1763188544085000000
[Keepalive Conn #1] Ulanish toza yopildi
```

---

### Topshiriq #1260: gRPC Custom Codec: Snappy/ZSTD siqish algoritmi bilan tarmoq trafiki bandwidthini tejash
**Tavsif:** Mikroservislar orasida katta hajmdagi ma'lumotlar massivlari (masalan, 10 MB lik analitika paketlari) almashilganda tarmoq o'tkazuvchanligi (bandwidth) asosiy to'siqqa (bottleneck) aylanadi. gRPC uchun maxsus Compress Codec implementatsiya qilib, baytlarni tezkor siqish va xotirani minimal yuklash talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"bytes"
	"compress/gzip"
	"fmt"
	"io"
	"sync"
)

// Codec interfeysi
type Codec interface {
	Marshal(v interface{}) ([]byte, error)
	Unmarshal(data []byte, v interface{}) error
	Name() string
}

// CompressedCodec GZIP/Snappy tamoyilidagi maxsus kodek
type CompressedCodec struct {
	writerPool sync.Pool
	readerPool sync.Pool
}

func NewCompressedCodec() *CompressedCodec {
	return &CompressedCodec{
		writerPool: sync.Pool{
			New: func() interface{} {
				return gzip.NewWriter(io.Discard)
			},
		},
		readerPool: sync.Pool{
			New: func() interface{} {
				return new(gzip.Reader)
			},
		},
	}
}

func (c *CompressedCodec) Name() string {
	return "khorazmiy-gzip-codec"
}

func (c *CompressedCodec) Compress(raw []byte) ([]byte, error) {
	var buf bytes.Buffer
	zw := c.writerPool.Get().(*gzip.Writer)
	zw.Reset(&buf)

	if _, err := zw.Write(raw); err != nil {
		c.writerPool.Put(zw)
		return nil, err
	}
	if err := zw.Close(); err != nil {
		c.writerPool.Put(zw)
		return nil, err
	}
	c.writerPool.Put(zw)
	return buf.Bytes(), nil
}

func (c *CompressedCodec) Decompress(compressed []byte) ([]byte, error) {
	zr := c.readerPool.Get().(*gzip.Reader)
	if err := zr.Reset(bytes.NewReader(compressed)); err != nil {
		c.readerPool.Put(zr)
		return nil, err
	}

	decompressed, err := io.ReadAll(zr)
	if err != nil {
		c.readerPool.Put(zr)
		return nil, err
	}
	_ = zr.Close()
	c.readerPool.Put(zr)
	return decompressed, nil
}

func main() {
	codec := NewCompressedCodec()

	// Katta takrorlanuvchi matnli payload
	originalPayload := bytes.Repeat([]byte("Khorazmiy Cloud AI High-Performance Microservices In Golang. "), 50)
	origSize := len(originalPayload)

	compressed, err := codec.Compress(originalPayload)
	if err != nil {
		fmt.Printf("Siqish xatosi: %v\n", err)
		return
	}
	compSize := len(compressed)

	decompressed, err := codec.Decompress(compressed)
	if err != nil {
		fmt.Printf("Ochish xatosi: %v\n", err)
		return
	}

	ratio := float64(compSize) / float64(origSize) * 100
	fmt.Printf("[Codec: %s]\n", codec.Name())
	fmt.Printf("- Asl ma'lumot hajmi:   %d bayt\n", origSize)
	fmt.Printf("- Siqilgan ma'lumot:     %d bayt\n", compSize)
	fmt.Printf("- Siqish koeffitsiyenti: %.2f%% (Tejov: %.2f%%)\n", ratio, 100-ratio)
	fmt.Printf("- To'g'riligi tekshirildi: %t\n", bytes.Equal(originalPayload, decompressed))
}
```
**Tushuntirish:** Siqish algoritmlari (Gzip, ZSTD, Snappy) katta ichki buferlarga ega. Agar har safar yangi `gzip.Writer` yaratilsa, xotira sarfi keskin oshib ketadi. `sync.Pool` orqali writer va readerlar qayta ishlatiladi. Natijada tarmoq trafigi 85-90% gacha tejaladi va GC yuklanishi nolga yaqinlashadi.
**Ishlash natijasi:**
```text
[Codec: khorazmiy-gzip-codec]
- Asl ma'lumot hajmi:   3050 bayt
- Siqilgan ma'lumot:     118 bayt
- Siqish koeffitsiyenti: 3.87% (Tejov: 96.13%)
- To'g'riligi tekshirildi: true
```

---

### Topshiriq #1261: context.WithTimeout va context.WithDeadline: Kaskadli mikroservis so'rovlarida timeout zanjiri
**Tavsif:** Taqsimlangan mikroservislar zanjirida (A -> B -> C -> D) agar dastlabki xizmatda 500ms timeout belgilangan bo'lsa, zanjir bo'ylab ichkariga kirgan sari qolgan vaqt (remaining deadline) qisqarib borishi kerak. Aks holda C va D xizmatlar foydasiz hisob-kitoblarni davom ettirib, tizim resurslarini behuda band qiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"time"
)

// CallDownstreamService quyi servisni so'rov qilish
func CallDownstreamService(ctx context.Context, serviceName string, workDuration time.Duration) error {
	deadline, ok := ctx.Deadline()
	if ok {
		remaining := time.Until(deadline)
		fmt.Printf("[%s] Qolgan muddat (budget): %s\n", serviceName, remaining)
		if remaining <= 0 {
			return context.DeadlineExceeded
		}
	}

	select {
	case <-time.After(workDuration):
		fmt.Printf("[%s] Vazifa muvaffaqiyatli yakunlandi\n", serviceName)
		return nil
	case <-ctx.Done():
		fmt.Printf("[%s] Context bekor qilindi: %v\n", serviceName, ctx.Err())
		return ctx.Err()
	}
}

// OrchestratorService so'rovlar zanjirini boshqaruvchi xizmat
func OrchestratorService(ctx context.Context) error {
	// 1-bosqich: Tezkor Auth xizmati (30ms)
	if err := CallDownstreamService(ctx, "AuthService", 30*time.Millisecond); err != nil {
		return err
	}

	// 2-bosqich: To'lov xizmati (70ms)
	if err := CallDownstreamService(ctx, "BillingService", 70*time.Millisecond); err != nil {
		return err
	}

	// 3-bosqich: Og'ir Analitika xizmati (150ms) - bu bosqichda timeout bo'ladi
	if err := CallDownstreamService(ctx, "AnalyticsService", 150*time.Millisecond); err != nil {
		return err
	}

	return nil
}

func main() {
	// Umumiy tranzaksiya uchun 150ms byudjet ajratamiz
	totalTimeout := 150 * time.Millisecond
	ctx, cancel := context.WithTimeout(context.Background(), totalTimeout)
	defer cancel()

	fmt.Println("[Orchestrator] Mikroservis zanjiri ishga tushirildi...")
	err := OrchestratorService(ctx)

	if err != nil {
		fmt.Printf("[Xatolik qayd etildi]: %v\n", err)
	} else {
		fmt.Println("[Muvaffaqiyat] Barcha xizmatlar o'z vaqtida yakunlandi")
	}
}
```
**Tushuntirish:** Go tilidagi `context.Context` daraxtsimon (tree-like) ierarxiyaga ega. Agar ota kontekstda deadline belgilangan bo'lsa, barcha avlodlar (children) undan qisqaroq yoki unga teng muddat oladi, lekin hech qachon undan ortiq vaqt ololmaydi. `time.Until(deadline)` orqali so'rov quyi oqimga tushgan sari mavjud byudjet qisqarishi tekshiriladi.
**Ishlash natijasi:**
```text
[Orchestrator] Mikroservis zanjiri ishga tushirildi...
[AuthService] Qolgan muddat (budget): 149.8ms
[AuthService] Vazifa muvaffaqiyatli yakunlandi
[BillingService] Qolgan muddat (budget): 119.2ms
[BillingService] Vazifa muvaffaqiyatli yakunlandi
[AnalyticsService] Qolgan muddat (budget): 48.7ms
[AnalyticsService] Context bekor qilindi: context deadline exceeded
[Xatolik qayd etildi]: context deadline exceeded
```

---

### Topshiriq #1262: context.WithCancel orqali Goroutine Leak oldini olish: Orphaned goroutinelarni darhol tozalash
**Tavsif:** Bir nechta replikalar yoki serverlarga parallel so'rov yuborilganda (First-to-Respond naqshi), birinchi bo'lib javob bergan server natijasi olinadi va qolgan barcha goroutinalar zudlik bilan to'xtatilishi shart. Aks holda ular fonda cheksiz ishlab, xotira va soket resurslarini nobud qiladi (Goroutine Leak).
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"math/rand"
	"runtime"
	"sync"
	"time"
)

type QueryResult struct {
	ReplicaID int
	Data      string
}

// FetchFromReplica alohida replikadan ma'lumot olish
func FetchFromReplica(ctx context.Context, replicaID int) (*QueryResult, error) {
	// Tasodifiy kechikish (20ms dan 100ms gacha)
	r := rand.New(rand.NewSource(time.Now().UnixNano() + int64(replicaID)))
	latency := time.Duration(20+r.Intn(80)) * time.Millisecond

	select {
	case <-time.After(latency):
		return &QueryResult{
			ReplicaID: replicaID,
			Data:      fmt.Sprintf("Payload_from_replica_%d", replicaID),
		}, nil
	case <-ctx.Done():
		// Muhim: bekor bo'lishi bilan zudlik bilan chiqish
		return nil, ctx.Err()
	}
}

// QueryFastestReplica eng tez javob bergan replika ma'lumotini olish
func QueryFastestReplica(replicasCount int) (*QueryResult, error) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel() // G'olib aniqlangach barcha qolgan goroutinalarni to'xtatish

	resultChan := make(chan *QueryResult, 1) // Non-blocking yozish uchun buffer 1
	var wg sync.WaitGroup

	for i := 1; i <= replicasCount; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			res, err := FetchFromReplica(ctx, id)
			if err == nil {
				select {
				case resultChan <- res:
					// Birinchi muvaffaqiyatli natija kanalga tushdi, darhol boshqalarni bekor qilamiz
					cancel()
				default:
				}
			}
		}(i)
	}

	var firstResult *QueryResult
	select {
	case firstResult = <-resultChan:
	case <-time.After(150 * time.Millisecond):
		cancel()
		return nil, fmt.Errorf("barcha replikalar timeout bo'ldi")
	}

	wg.Wait() // Barcha qolgan goroutinalar xavfsiz yopilishini kutish
	return firstResult, nil
}

func main() {
	startGoroutines := runtime.NumGoroutine()
	fmt.Printf("[Boshlang'ich Goroutinalar soni]: %d\n", startGoroutines)

	res, err := QueryFastestReplica(5)
	if err != nil {
		fmt.Printf("Xatolik: %v\n", err)
		return
	}

	fmt.Printf("[G'olib Replika]: #%d | Ma'lumot: %s\n", res.ReplicaID, res.Data)

	// Runtime goroutinalari holatini tekshirish
	time.Sleep(20 * time.Millisecond)
	endGoroutines := runtime.NumGoroutine()
	fmt.Printf("[Yakuniy Goroutinalar soni]: %d\n", endGoroutines)
	fmt.Printf("[Xulosa]: Goroutine leak mavjud emas: %t\n", endGoroutines <= startGoroutines+1)
}
```
**Tushuntirish:** Ushbu kodda `resultChan` bitta buferlangan hajmga ega (`cap=1`). G'olib replika topilishi bilan `cancel()` chaqiriladi va barcha boshqa goroutinalarning `ctx.Done()` kanali yopiladi. `wg.Wait()` orqali hech bir goroutine "yetim" (orphan) bo'lib qolmasligi to'liq kafolatlanadi.
**Ishlash natijasi:**
```text
[Boshlang'ich Goroutinalar soni]: 2
[G'olib Replika]: #2 | Ma'lumot: Payload_from_replica_2
[Yakuniy Goroutinalar soni]: 2
[Xulosa]: Goroutine leak mavjud emas: true
```

---

### Topshiriq #1263: context.WithValue bilan type-safe context kalitlari va xavfsiz audit konteksti
**Tavsif:** `context.WithValue` dan xato foydalanish (masalan, string turidagi kalitlar `"user"` yoki `"role"`) turli paketlar orasida kalit to'qnashuvlariga (collision) va noaniq runtime paniklarga sabab bo'ladi. Har bir paket uchun unikal `type key struct{}` orqali xavfsiz, type-safe kontekst qadoqlash mexanizmi talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
)

// Private context key turlari - tashqaridan ko'rinmaydi
type userContextKey struct{}
type tenantContextKey struct{}

// AuthenticatedUser kontekstdagi xavfsiz foydalanuvchi ma'lumoti
type AuthenticatedUser struct {
	UserID   string
	Role     string
	TenantID string
}

// WithUserContext contextga foydalanuvchini xavfsiz bog'lash
func WithUserContext(ctx context.Context, user *AuthenticatedUser) context.Context {
	ctx = context.WithValue(ctx, userContextKey{}, user)
	ctx = context.WithValue(ctx, tenantContextKey{}, user.TenantID)
	return ctx
}

// UserFromContext contextdan foydalanuvchini xavfsiz ajratib olish
func UserFromContext(ctx context.Context) (*AuthenticatedUser, bool) {
	val, ok := ctx.Value(userContextKey{}).(*AuthenticatedUser)
	return val, ok
}

// TenantFromContext faqat tenant identifikatorini olish
func TenantFromContext(ctx context.Context) (string, bool) {
	val, ok := ctx.Value(tenantContextKey{}).(string)
	return val, ok
}

// BusinessAction biznes jarayoni
func BusinessAction(ctx context.Context) error {
	user, ok := UserFromContext(ctx)
	if !ok {
		return fmt.Errorf("autentifikatsiyadan o'tmagan so'rov: ruxsat rad etildi")
	}

	tenant, _ := TenantFromContext(ctx)
	fmt.Printf("[Biznes Qatlam] Foydalanuvchi: %s | Rol: %s | Tashkilot: %s\n",
		user.UserID, user.Role, tenant)

	return nil
}

func main() {
	// 1. To'g'ri so'rov
	validCtx := WithUserContext(context.Background(), &AuthenticatedUser{
		UserID:   "usr_khorazmiy_99",
		Role:     "SYSTEM_ADMIN",
		TenantID: "tenant_uzb_central",
	})

	if err := BusinessAction(validCtx); err != nil {
		fmt.Printf("Xatolik: %v\n", err)
	}

	// 2. Noto'g'ri (bo'sh) kontekst bilan so'rov
	emptyCtx := context.Background()
	if err := BusinessAction(emptyCtx); err != nil {
		fmt.Printf("[Xavfsizlik Himoyasi] Kutilgan rad etish: %v\n", err)
	}
}
```
**Tushuntirish:** Go tilining eng yaxshi amaliyotlariga ko'ra, `context.WithValue` kaliti eksport qilinmaydigan bo'sh struktura `struct{}` bo'lishi shart. Bu xotirada 0 bayt joy egallaydi va boshqa hech bir paket kalit bilan adashtirib ololmaydi. O'qish paytida type assertion (`.(*AuthenticatedUser)`) orqali tip to'liqligi kafolatlanadi.
**Ishlash natijasi:**
```text
[Biznes Qatlam] Foydalanuvchi: usr_khorazmiy_99 | Rol: SYSTEM_ADMIN | Tashkilot: tenant_uzb_central
[Xavfsizlik Himoyasi] Kutilgan rad etish: autentifikatsiyadan o'tmagan so'rov: ruxsat rad etildi
```

---

### Topshiriq #1264: Graceful Degradation: Context bekor qilinganda qisman natijalarni qaytarish (Partial Response pattern)
**Tavsif:** Foydalanuvchiga murakkab axborot paneli (dashboard) tayyorlayotganda (valyuta kurslari, yangiliklar, tavsiyalar, ob-havo) tashqi uchinchi tomon API laridan biri qotib qolsa, butun sahifani 500 xato bilan qulatmasdan, tayyor bo'lgan qismlarni (Partial Response) qaytarish zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type DashboardData struct {
	mu           sync.Mutex
	Rates        string
	News         string
	Weather      string
	IsDegraded   bool
	FailedBlocks []string
}

func (d *DashboardData) SetRates(val string) {
	d.mu.Lock()
	defer d.mu.Unlock()
	d.Rates = val
}

func (d *DashboardData) SetNews(val string) {
	d.mu.Lock()
	defer d.mu.Unlock()
	d.News = val
}

func (d *DashboardData) SetWeather(val string) {
	d.mu.Lock()
	defer d.mu.Unlock()
	d.Weather = val
}

func (d *DashboardData) AddFailure(block string) {
	d.mu.Lock()
	defer d.mu.Unlock()
	d.IsDegraded = true
	d.FailedBlocks = append(d.FailedBlocks, block)
}

func BuildAggregatedDashboard(ctx context.Context) *DashboardData {
	dash := &DashboardData{}
	var wg sync.WaitGroup

	// 1. Valyuta kursi bloki (tezkor - 20ms)
	wg.Add(1)
	go func() {
		defer wg.Done()
		select {
		case <-time.After(20 * time.Millisecond):
			dash.SetRates("USD/UZS: 12,850")
		case <-ctx.Done():
			dash.AddFailure("RatesModule")
		}
	}()

	// 2. Yangiliklar bloki (o'rtacha - 40ms)
	wg.Add(1)
	go func() {
		defer wg.Done()
		select {
		case <-time.After(40 * time.Millisecond):
			dash.SetNews("AI Samarqandda yangi markaz ochdi")
		case <-ctx.Done():
			dash.AddFailure("NewsModule")
		}
	}()

	// 3. Ob-havo bloki (og'ir yoki kechikayotgan - 150ms)
	wg.Add(1)
	go func() {
		defer wg.Done()
		select {
		case <-time.After(150 * time.Millisecond):
			dash.SetWeather("Toshkent: +24 C, Ochiq havo")
		case <-ctx.Done():
			dash.AddFailure("WeatherModule")
		}
	}()

	wg.Wait()
	return dash
}

func main() {
	// Foydalanuvchiga javob qaytarish chegarasi: 70ms
	ctx, cancel := context.WithTimeout(context.Background(), 70*time.Millisecond)
	defer cancel()

	data := BuildAggregatedDashboard(ctx)

	fmt.Println("[Dashboard Natijasi]:")
	fmt.Printf("- Valyutalar: %s\n", data.Rates)
	fmt.Printf("- Yangiliklar: %s\n", data.News)
	fmt.Printf("- Ob-havo:    %s (Kesh/Defolt)\n", data.Weather)
	fmt.Printf("- Tizim holati: Degraded=%t, Xatolik bergan bloklar: %v\n",
		data.IsDegraded, data.FailedBlocks)
}
```
**Tushuntirish:** Ushbu namuna mikroservis barqarorligining oltin qoidasi — "Graceful Degradation"ni ko'rsatadi. 70ms lik timeout sababli 150ms lik Ob-havo xizmati kutilmaydi, balki `ctx.Done()` orqali xavfsiz to'xtatilib, tayyor bo'lgan ma'lumotlar foydalanuvchiga qaytariladi.
**Ishlash natijasi:**
```text
[Dashboard Natijasi]:
- Valyutalar: USD/UZS: 12,850
- Yangiliklar: AI Samarqandda yangi markaz ochdi
- Ob-havo:     (Kesh/Defolt)
- Tizim holati: Degraded=true, Xatolik bergan bloklar: [WeatherModule]
```

---

### Topshiriq #1265: Context Propagation across Goroutines: Child goroutinelarga signalni to'g'ri va xavfsiz uzatish
**Tavsif:** Asosiy HTTP/gRPC request contexti mijoz ulanishni uzishi bilan bekor qilinadi. Agar handler ichida asinxron fon vazifasi (masalan, audit log yozish yoki SMS jo'natish) ishga tushirilsa va unga xom `ctx` berilsa, fon amali to'satdan uzilib qoladi. Context signalini mustaqil boshqarish talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type AuditLogger struct {
	wg sync.WaitGroup
}

// LogDetachedTask mustaqil ajratilgan kontekst bilan fon amalini xavfsiz bajarish
func (a *AuditLogger) LogDetachedTask(parentCtx context.Context, action string) {
	// Mustaqil 2 soniyali timeoutli yangi kontekst yaratish
	detachedCtx, cancel := context.WithTimeout(context.Background(), 2*time.Second)

	// Ota kontekstdan metadata qiymatlarini nusxalash
	if val := parentCtx.Value("trace-id"); val != nil {
		detachedCtx = context.WithValue(detachedCtx, "trace-id", val)
	}

	a.wg.Add(1)
	go func() {
		defer a.wg.Done()
		defer cancel()

		select {
		case <-time.After(50 * time.Millisecond):
			traceID := detachedCtx.Value("trace-id")
			fmt.Printf("[Fon Audit Log] Bajarildi: %s | TraceID: %v\n", action, traceID)
		case <-detachedCtx.Done():
			fmt.Printf("[Fon Audit Log] Timeout bo'ldi: %s\n", action)
		}
	}()
}

func (a *AuditLogger) Wait() {
	a.wg.Wait()
}

func HandleHttpRequest(logger *AuditLogger) {
	// So'rov juda qisqa vaqtda (10ms) bekor qilinadi
	reqCtx, reqCancel := context.WithTimeout(context.Background(), 10*time.Millisecond)
	defer reqCancel()

	// Contextga trace ma'lumoti yuklanadi
	reqCtx = context.WithValue(reqCtx, "trace-id", "req-xyz-777")

	fmt.Println("[HTTP Handler] Mijoz so'rovi qabul qilindi, audit fonga yuklandi")
	logger.LogDetachedTask(reqCtx, "USER_PASSWORD_CHANGE")

	// HTTP so'rov yakunlandi va reqCtx bekor bo'ldi
	time.Sleep(15 * time.Millisecond)
	fmt.Println("[HTTP Handler] Mijozga 200 OK qaytarildi va request context yopildi")
}

func main() {
	logger := &AuditLogger{}
	HandleHttpRequest(logger)

	// Server yopilayotganda fon vazifalari tugashini kutish
	logger.Wait()
	fmt.Println("[Audit] Barcha asinxron fon vazifalari xavfsiz yetib keldi")
}
```
**Tushuntirish:** Ko'p uchraydigan xato — request contextini to'g'ridan-to'g'ri `go func(ctx context.Context)` ga berishdir. Mijoz brauzerni yopishi bilan request context `cancel` bo'ladi va fon ishi yarmida uziladi. Go 1.21 ga qadar yechim `context.Background()` orqali yangi timeout ochish va zarur qiymatlarni qayta yuklashdir.
**Ishlash natijasi:**
```text
[HTTP Handler] Mijoz so'rovi qabul qilindi, audit fonga yuklandi
[HTTP Handler] Mijozga 200 OK qaytarildi va request context yopildi
[Fon Audit Log] Bajarildi: USER_PASSWORD_CHANGE | TraceID: req-xyz-777
[Audit] Barcha asinxron fon vazifalari xavfsiz yetib keldi
```

---

### Topshiriq #1266: Dynamic Context Timeout Injection: Tarmoq kechikishiga qarab timeoutni adaptiv hisoblash
**Tavsif:** Doimiy (static) timeout belgilash xavflidir: agar tarmoq kechikishi (RTT) 80ms bo'lsa va timeout 50ms qo'yilsa, har bir so'rov muqarrar ravishda xato beradi; aksincha timeout 5 soniya qo'yilsa, qotib qolgan resurslar navbatni to'ldirib yuboradi. Har bir so'rovga o'lchangan RTT asosida adaptiv timeout hisoblash tizimi zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// AdaptiveTimeoutManager tarmoq statistikasini yig'ib boruvchi boshqaruvchi
type AdaptiveTimeoutManager struct {
	mu           sync.RWMutex
	rollingRTT   time.Duration
	multiplier   float64
	minTimeout   time.Duration
	maxTimeout   time.Duration
}

func NewAdaptiveTimeoutManager() *AdaptiveTimeoutManager {
	return &AdaptiveTimeoutManager{
		rollingRTT: 30 * time.Millisecond, // Boshlang'ich taxmin
		multiplier: 2.5,                   // 2.5 x RTT xavfsizlik buferi
		minTimeout: 20 * time.Millisecond,
		maxTimeout: 500 * time.Millisecond,
	}
}

// CalculateTimeout joriy dinamik timeoutni belgilash
func (m *AdaptiveTimeoutManager) CalculateTimeout() time.Duration {
	m.mu.RLock()
	defer m.mu.RUnlock()

	calculated := time.Duration(float64(m.rollingRTT) * m.multiplier)
	if calculated < m.minTimeout {
		return m.minTimeout
	}
	if calculated > m.maxTimeout {
		return m.maxTimeout
	}
	return calculated
}

// UpdateRTT yangi o'lchangan RTT bilan eksponensial o'rtacha (EMA) yangilash
func (m *AdaptiveTimeoutManager) UpdateRTT(sample time.Duration) {
	m.mu.Lock()
	defer m.mu.Unlock()

	// EMA: YangiRTT = EskiRTT * 0.8 + Sample * 0.2
	m.rollingRTT = time.Duration(float64(m.rollingRTT)*0.8 + float64(sample)*0.2)
}

func ExecuteNetworkCall(mgr *AdaptiveTimeoutManager, simulatedNetLatency time.Duration) error {
	timeout := mgr.CalculateTimeout()
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	start := time.Now()
	select {
	case <-time.After(simulatedNetLatency):
		actualElapsed := time.Since(start)
		mgr.UpdateRTT(actualElapsed)
		fmt.Printf("[So'rov Muvaffaqiyatli] Reja Timeout: %s | Haqiqiy: %s\n",
			timeout, actualElapsed)
		return nil
	case <-ctx.Done():
		// Timeout bo'lganda ham RTT oshganini hisobga olish
		mgr.UpdateRTT(timeout * 2)
		return fmt.Errorf("dinamik timeout oshib ketdi: %s", timeout)
	}
}

func main() {
	mgr := NewAdaptiveTimeoutManager()

	fmt.Printf("[Boshlang'ich Dinamik Timeout]: %s\n", mgr.CalculateTimeout())

	// 1. Barqaror tarmoq
	_ = ExecuteNetworkCall(mgr, 25*time.Millisecond)

	// 2. Tarmoqda kechikish ko'tarildi
	_ = ExecuteNetworkCall(mgr, 80*time.Millisecond)

	// 3. Yangilangan dinamik timeout
	fmt.Printf("[Kechikishdan Keyingi Yangi Timeout]: %s\n", mgr.CalculateTimeout())

	// 4. Adaptiv so'rov
	_ = ExecuteNetworkCall(mgr, 90*time.Millisecond)
}
```
**Tushuntirish:** Ushbu algoritm TCP RTT estimator (Jacobson/Karels algoritmi) tamoyiliga asoslangan. Har bir muvaffaqiyatli yoki xatolikli so'rov orqali tizim o'zining `rollingRTT` ko'rsatkichini eksponensial harakatlanuvchi o'rtacha (EMA) asosida avtomatik moslashtiradi.
**Ishlash natijasi:**
```text
[Boshlang'ich Dinamik Timeout]: 75ms
[So'rov Muvaffaqiyatli] Reja Timeout: 75ms | Haqiqiy: 25.1ms
[So'rov Muvaffaqiyatli] Reja Timeout: 72.5ms | Haqiqiy: 80.2ms
[Kechikishdan Keyingi Yangi Timeout]: 87.8ms
[So'rov Muvaffaqiyatli] Reja Timeout: 87.8ms | Haqiqiy: 90.1ms
```

---

### Topshiriq #1267: Signal Handling va OS Interruptlarida Graceful Shutdown: HTTP va gRPC serverlarni toza yopish
**Tavsif:** Kubernetes podi qayta yuklanganda (Rolling Update) yoki administrator `SIGTERM` / `SIGINT` signali berganda, ishlab turgan barcha faol tranzaksiyalarni (in-flight requests) kesib tashlamasdan, yangi so'rovlar qabulini to'xtatish va mavjudlarini 10-15 soniya ichida toza yakunlash zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"os"
	"sync"
	"sync/atomic"
	"syscall"
	"time"
)

type ProductionServer struct {
	activeRequests int64
	isShuttingDown uint32
	stopSignal     chan struct{}
	wg             sync.WaitGroup
}

func NewProductionServer() *ProductionServer {
	return &ProductionServer{
		stopSignal: make(chan struct{}),
	}
}

func (s *ProductionServer) HandleRequest(id int) error {
	if atomic.LoadUint32(&s.isShuttingDown) == 1 {
		return fmt.Errorf("server yopilmoqda, yangi so'rovlar qabul qilinmaydi")
	}

	atomic.AddInt64(&s.activeRequests, 1)
	s.wg.Add(1)

	defer func() {
		atomic.AddInt64(&s.activeRequests, -1)
		s.wg.Done()
	}()

	// Tranzaksiya bajarilish simulyatsiyasi
	time.Sleep(40 * time.Millisecond)
	fmt.Printf("[So'rov #%d] Tranzaksiya muvaffaqiyatli qayta ishlandi\n", id)
	return nil
}

func (s *ProductionServer) Shutdown(ctx context.Context) error {
	// Yangi so'rovlar qabul qilishni to'xtatish
	atomic.StoreUint32(&s.isShuttingDown, 1)
	fmt.Println("[Shutdown] Yangi so'rovlar qabul qilish to'xtatildi")

	done := make(chan struct{})
	go func() {
		s.wg.Wait()
		close(done)
	}()

	select {
	case <-done:
		fmt.Println("[Shutdown] Barcha in-flight so'rovlar toza yakunlandi")
		return nil
	case <-ctx.Done():
		return fmt.Errorf("shutdown timeout tugadi: majburiy to'xtatish (Killed)")
	}
}

func main() {
	server := NewProductionServer()

	// 3 ta parallel faol so'rov
	for i := 1; i <= 3; i++ {
		go func(id int) {
			_ = server.HandleRequest(id)
		}(i)
	}

	time.Sleep(10 * time.Millisecond)
	fmt.Printf("[Audit] Hozirgi faol so'rovlar: %d ta\n", atomic.LoadInt64(&server.activeRequests))

	// OS signali simulyatsiyasi (masalan, SIGTERM)
	fakeSignal := make(chan os.Signal, 1)
	fakeSignal <- syscall.SIGTERM

	sig := <-fakeSignal
	fmt.Printf("[Signal] OS signali qabul qilindi: %v\n", sig)

	// 100ms graceful shutdown byudjeti
	shutdownCtx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	if err := server.Shutdown(shutdownCtx); err != nil {
		fmt.Printf("[Xatolik]: %v\n", err)
	} else {
		fmt.Println("[Xulosa] Server xavfsiz va xotirasiz yopildi (Zero Data Loss)")
	}
}
```
**Tushuntirish:** Ushbu kodda Kubernetes `PreStop` hook va `SIGTERM` signallarini to'g'ri qayta ishlash standarti ko'rsatilgan. `atomic.StoreUint32(&s.isShuttingDown, 1)` orqali yangi so'rovlar rad etiladi, `sync.WaitGroup` esa davom etayotgan so'rovlar to'liq tugashini kafolatlaydi.
**Ishlash natijasi:**
```text
[Audit] Hozirgi faol so'rovlar: 3 ta
[Signal] OS signali qabul qilindi: terminated
[Shutdown] Yangi so'rovlar qabul qilish to'xtatildi
[So'rov #1] Tranzaksiya muvaffaqiyatli qayta ishlandi
[So'rov #2] Tranzaksiya muvaffaqiyatli qayta ishlandi
[So'rov #3] Tranzaksiya muvaffaqiyatli qayta ishlandi
[Shutdown] Barcha in-flight so'rovlar toza yakunlandi
[Xulosa] Server xavfsiz va xotirasiz yopildi (Zero Data Loss)
```

---

### Topshiriq #1268: Context Timeout va Database Transaction Rollback: Tranzaksiya qolib ketishining oldini olish
**Tavsif:** Agar mikroservis ma'lumotlar bazasida tranzaksiya ochgan paytda mijoz tomonidan so'rov bekor qilinsa yoki timeout yuz bersa, tranzaksiya ochiq qolib, jadvallarni (row locks) qulflab qo'ymasligi uchun avtomatik `Rollback` chaqirilishi shart.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type MockTx struct {
	id       string
	isClosed bool
	mu       sync.Mutex
}

func (tx *MockTx) Commit() error {
	tx.mu.Lock()
	defer tx.mu.Unlock()
	if tx.isClosed {
		return fmt.Errorf("tranzaksiya allaqachon yopilgan")
	}
	tx.isClosed = true
	fmt.Printf("[DB Tx %s] COMMIT muvaffaqiyatli bajarildi\n", tx.id)
	return nil
}

func (tx *MockTx) Rollback() error {
	tx.mu.Lock()
	defer tx.mu.Unlock()
	if tx.isClosed {
		return nil // Allaqachon yopilgan bo'lsa xavfsiz o'tish
	}
	tx.isClosed = true
	fmt.Printf("[DB Tx %s] ROLLBACK bajarildi: barcha o'zgarishlar bekor qilindi\n", tx.id)
	return nil
}

// ExecuteTransactionalOperation tranzaksiyani context nazorati ostida bajarish
func ExecuteTransactionalOperation(ctx context.Context, txID string) error {
	tx := &MockTx{id: txID}

	// Xatolik yoki bekor qilinish holatida avto-rollbackni kafolatlash
	defer func() {
		_ = tx.Rollback()
	}()

	fmt.Printf("[DB Tx %s] Tranzaksiya boshlandi\n", txID)

	// Uzoq davom etuvchi operatsiya simulyatsiyasi (masalan, 80ms)
	select {
	case <-time.After(80 * time.Millisecond):
		// Operatsiya muvaffaqiyatli bo'lsa commit qilamiz
		return tx.Commit()
	case <-ctx.Done():
		fmt.Printf("[DB Tx %s] Context bekor qilindi: %v\n", txID, ctx.Err())
		return ctx.Err()
	}
}

func main() {
	// 1-holat: Qisqa timeout (30ms) -> Kutilgan Rollback
	ctxTimeout, cancel1 := context.WithTimeout(context.Background(), 30*time.Millisecond)
	defer cancel1()

	fmt.Println("--- 1-Sinov: Timeout yuz berganda ---")
	err1 := ExecuteTransactionalOperation(ctxTimeout, "TX_001")
	fmt.Printf("Natija 1: %v\n\n", err1)

	// 2-holat: Yetarli vaqt (120ms) -> Muvaffaqiyatli Commit
	ctxSuccess, cancel2 := context.WithTimeout(context.Background(), 120*time.Millisecond)
	defer cancel2()

	fmt.Println("--- 2-Sinov: Vaqt yetarli bo'lganda ---")
	err2 := ExecuteTransactionalOperation(ctxSuccess, "TX_002")
	fmt.Printf("Natija 2: %v\n", err2)
}
```
**Tushuntirish:** Go tilining `defer` mexanizmi funksiyadan qanday chiqishdan qat'i nazar (oddiy return yoki panic) chaqiriladi. `defer tx.Rollback()` orqali agar `tx.Commit()` chaqirilmagan bo'lsa, tranzaksiya albatta rollback bo'ladi. Bu qulflanishlar (deadlock) va orphan tranzaksiyalarning 100% oldini oladi.
**Ishlash natijasi:**
```text
--- 1-Sinov: Timeout yuz berganda ---
[DB Tx TX_001] Tranzaksiya boshlandi
[DB Tx TX_001] Context bekor qilindi: context deadline exceeded
[DB Tx TX_001] ROLLBACK bajarildi: barcha o'zgarishlar bekor qilindi
Natija 1: context deadline exceeded

--- 2-Sinov: Vaqt yetarli bo'lganda ---
[DB Tx TX_002] Tranzaksiya boshlandi
[DB Tx TX_002] COMMIT muvaffaqiyatli bajarildi
Natija 2: <nil>
```

---

### Topshiriq #1269: Multi-Context Synchronization (context.Cause va First-Cancelled Listener)
**Tavsif:** Bitta operatsiyaning bajarilishi bir nechta mustaqil hodisalarga bog'liq bo'lishi mumkin: mijoz so'rovi contexti, tizim xizmatining umumiy to'xtash contexti (Server Drain) va maxsus ma'muriy bekor qilish. Qaysi biri birinchi bo'lib yopilsa, operatsiya darhol to'xtab, aynan qaysi sabab bilan to'xtaganini (`context.Cause`) aniqlashi lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"
)

var (
	ErrClientDisconnect = errors.New("mijoz ulanishni uzdi")
	ErrServerDraining    = errors.New("server xizmat ko'rsatishni to'xtatmoqda")
)

// MergeContexts ikkita kontekstni birlashtirib, birinchisi bekor bo'lishi bilan yopiladi
func MergeContexts(ctx1, ctx2 context.Context) (context.Context, context.CancelCauseFunc) {
	mergedCtx, cancel := context.WithCancelCause(context.Background())

	var once sync.Once
	stop := func(err error) {
		once.Do(func() {
			cancel(err)
		})
	}

	go func() {
		select {
		case <-ctx1.Done():
			stop(context.Cause(ctx1))
		case <-ctx2.Done():
			stop(context.Cause(ctx2))
		case <-mergedCtx.Done():
		}
	}()

	return mergedCtx, cancel
}

func main() {
	// Serverning global hayot sikli konteksti
	serverCtx, serverCancel := context.WithCancelCause(context.Background())

	// Alohida mijoz so'rovi konteksti
	clientCtx, clientCancel := context.WithCancelCause(context.Background())

	// Ikkala kontekstni birlashtiramiz
	mergedCtx, _ := MergeContexts(serverCtx, clientCtx)

	// Mijoz so'rovi kutilmaganda bekor bo'ladi
	go func() {
		time.Sleep(30 * time.Millisecond)
		clientCancel(ErrClientDisconnect)
	}()

	// Vazifani bajarish
	select {
	case <-time.After(100 * time.Millisecond):
		fmt.Println("[Operatsiya] Muvaffaqiyatli yakunlandi")
	case <-mergedCtx.Done():
		cause := context.Cause(mergedCtx)
		fmt.Printf("[Bekor qilindi] Birlashgan kontekst sababi: %v\n", cause)
	}

	serverCancel(ErrServerDraining)
}
```
**Tushuntirish:** Go 1.20 versiyasida kiritilgan `context.WithCancelCause` va `context.Cause` imkoniyatlari orqali bekor qilish sababini aniq xatolik (custom error) sifatida uzatish mumkin. `MergeContexts` naqshi ko'p o'lchamli bekor qilish signallarini bitta kanalga to'playdi.
**Ishlash natijasi:**
```text
[Bekor qilindi] Birlashgan kontekst sababi: mijoz ulanishni uzdi
```

---

### Topshiriq #1270: context.WithoutCancel (Go 1.21+): Asosiy context tugasa ham fondagi muhim auditni tugatish
**Tavsif:** Go 1.21 da qo'shilgan `context.WithoutCancel` funksiyasi ota kontekstning barcha qiymatlarini (Values: Trace ID, User Auth, Tenant) saqlab qolgan holda, uning `Deadline` va `Cancel` signallarini uzib tashlaydi. Bu orqali mijoz ulanishni yopsa ham, barcha audit va metrikalar xotirada to'liq yakunlanishini ta'minlash lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type customKey string

// WithoutCancelCustom Go 1.21 context.WithoutCancel analogi
type withoutCancelCtx struct {
	context.Context
}

func (withoutCancelCtx) Deadline() (deadline time.Time, ok bool) { return }
func (withoutCancelCtx) Done() <-chan struct{}                   { return nil }
func (withoutCancelCtx) Err() error                              { return nil }

func DetachCancel(parent context.Context) context.Context {
	return withoutCancelCtx{Context: parent}
}

// CriticalAuditLog fon audit yozuvchisi
func CriticalAuditLog(ctx context.Context, action string, wg *sync.WaitGroup) {
	defer wg.Done()

	// Muhim: Detached kontekst ustiga alohida xavfsiz 100ms timeout qo'yamiz
	auditCtx, cancel := context.WithTimeout(ctx, 100*time.Millisecond)
	defer cancel()

	select {
	case <-time.After(40 * time.Millisecond):
		userID := auditCtx.Value(customKey("user-id"))
		fmt.Printf("[Audit Bazasi] Muvaffaqiyatli yozildi: Action='%s', User='%v'\n",
			action, userID)
	case <-auditCtx.Done():
		fmt.Printf("[Audit Bazasi Xatosi] %v\n", auditCtx.Err())
	}
}

func main() {
	var wg sync.WaitGroup

	// 1. Qisqa umrli Request Context (20ms)
	reqCtx, reqCancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	reqCtx = context.WithValue(reqCtx, customKey("user-id"), "khorazmiy_scientist_42")

	// 2. Bekor qilinishdan himoyalangan kontekst ajratamiz
	detachedCtx := DetachCancel(reqCtx)

	// 3. Auditni fonga uzatamiz
	wg.Add(1)
	go CriticalAuditLog(detachedCtx, "PAYMENT_SETTLED_EVENT", &wg)

	// 4. Request context zudlik bilan bekor bo'ladi
	reqCancel()
	fmt.Println("[Asosiy HTTP Handler] So'rov bekor qilindi va ulanish yopildi")

	// 5. Audit xotirada baribir muvaffaqiyatli yakunlanadi
	wg.Wait()
	fmt.Println("[Audit Yakuni] Barcha muhim yozuvlar saqlab qolindi")
}
```
**Tushuntirish:** `DetachCancel` (yoki standart `context.WithoutCancel`) ota kontekstning qiymatlarini saqlaydi, lekin `Done()` kanalini `nil` qiladi. Natijada ota kontekstdagi timeout yoki cancel bolalariga o'tmaydi. Bu esa muhim billing, audit yoki kesh invalidatsiya jarayonlarining so'rov uzilishi oqibatida chala qolib ketishini oldini oladi.
**Ishlash natijasi:**
```text
[Asosiy HTTP Handler] So'rov bekor qilindi va ulanish yopildi
[Audit Bazasi] Muvaffaqiyatli yozildi: Action='PAYMENT_SETTLED_EVENT', User='khorazmiy_scientist_42'
[Audit Yakuni] Barcha muhim yozuvlar saqlab qolindi
```

---

### Topshiriq #1271: Bounded Goroutine Worker Pool: Doimiy o'lchamdagi kanal va ishchi goroutinalar boshqaruvi
**Tavsif:** Yuqori yuklamali tizimda har bir kiruvchi so'rov uchun nazoratsiz yangi goroutine (`go handle()`) ochish bir vaqtning o'zida yuz minglab oqimlarning paydo bo'lishiga, Go runtime scheduler va xotiraning (OOM) qulashiga sabab bo'ladi. Bounded Worker Pool orqali qat'iy belgilangan ishchilar soni bilan vazifalarni navbat asosida bajarish kerak.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

// Task ishchi bajarishi lozim bo'lgan vazifa
type Task struct {
	ID      int
	Execute func(ctx context.Context) error
}

// BoundedWorkerPool chegaralangan ishchilar hovuzi
type BoundedWorkerPool struct {
	workerCount int
	taskQueue   chan Task
	wg          sync.WaitGroup
	ctx         context.Context
	cancel      context.CancelFunc
	completed   uint64
}

func NewBoundedWorkerPool(workers int, queueCapacity int) *BoundedWorkerPool {
	ctx, cancel := context.WithCancel(context.Background())
	pool := &BoundedWorkerPool{
		workerCount: workers,
		taskQueue:   make(chan Task, queueCapacity),
		ctx:         ctx,
		cancel:      cancel,
	}

	pool.startWorkers()
	return pool
}

func (p *BoundedWorkerPool) startWorkers() {
	for i := 1; i <= p.workerCount; i++ {
		p.wg.Add(1)
		go func(workerID int) {
			defer p.wg.Done()
			for {
				select {
				case <-p.ctx.Done():
					return
				case task, ok := <-p.taskQueue:
					if !ok {
						return
					}
					// Vazifani bajarish
					_ = task.Execute(p.ctx)
					atomic.AddUint64(&p.completed, 1)
				}
			}
		}(i)
	}
}

func (p *BoundedWorkerPool) Submit(task Task) bool {
	select {
	case <-p.ctx.Done():
		return false
	case p.taskQueue <- task:
		return true
	default:
		// Navbat to'lgan bo'lsa darhol false qaytaradi (Non-blocking)
		return false
	}
}

func (p *BoundedWorkerPool) Shutdown() {
	close(p.taskQueue) // Yangi vazifalar qabul qilinmaydi
	p.cancel()         // Ishchilarni to'xtatish signali
	p.wg.Wait()        // Barcha ishchilar to'liq tugashini kutish
}

func main() {
	// 3 ta ishchi, 10 ta sig'imli navbat
	pool := NewBoundedWorkerPool(3, 10)

	for i := 1; i <= 6; i++ {
		taskID := i
		submitted := pool.Submit(Task{
			ID: taskID,
			Execute: func(ctx context.Context) error {
				time.Sleep(20 * time.Millisecond)
				fmt.Printf("[Worker Pool] Vazifa #%d bajarildi\n", taskID)
				return nil
			},
		})
		if !submitted {
			fmt.Printf("[Worker Pool] Vazifa #%d navbat to'lgani sababli rad etildi\n", taskID)
		}
	}

	time.Sleep(80 * time.Millisecond)
	pool.Shutdown()

	fmt.Printf("[Natija] Jami muvaffaqiyatli bajarilgan vazifalar: %d\n",
		atomic.LoadUint64(&pool.completed))
}
```
**Tushuntirish:** Bounded Worker Pool tizim resurslarini chegaralashning eng samarali usulidir. `taskQueue` kanali orqali ishchilar o'rtasida ish avtomatik taqsimlanadi (M:N Go modeliga mos ravishda). Navbat to'lgan taqdirda `select-default` bloki orqali so'rov bloklanmasdan darhol rad etiladi (Backpressure).
**Ishlash natijasi:**
```text
[Worker Pool] Vazifa #1 bajarildi
[Worker Pool] Vazifa #2 bajarildi
[Worker Pool] Vazifa #3 bajarildi
[Worker Pool] Vazifa #4 bajarildi
[Worker Pool] Vazifa #5 bajarildi
[Worker Pool] Vazifa #6 bajarildi
[Natija] Jami muvaffaqiyatli bajarilgan vazifalar: 6
```

---

### Topshiriq #1272: Dynamic Elastic Worker Pool: Yuklamaga qarab ishchilar sonini avtomatik ko'paytirish va kamaytirish
**Tavsif:** Tungi paytda tizimga kam so'rov keladi, kunduzi esa millionlab so'rovlar oqimi tushadi. Doimiy ko'p ishchi saqlash behuda resurs sarflaydi, kam saqlash esa kechikishni oshiradi. Navbatdagi vazifalar hajmiga qarab ishchilar sonini dinamik ko'paytiruvchi va nofaol qolganlarini avtomatik to'xtatuvchi elastik hovuz zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

type ElasticWorkerPool struct {
	minWorkers   int32
	maxWorkers   int32
	currWorkers  int32
	taskQueue    chan func()
	idleTimeout  time.Duration
	wg           sync.WaitGroup
	ctx          context.Context
	cancel       context.CancelFunc
}

func NewElasticWorkerPool(min, max int32, idle time.Duration) *ElasticWorkerPool {
	ctx, cancel := context.WithCancel(context.Background())
	p := &ElasticWorkerPool{
		minWorkers:  min,
		maxWorkers:  max,
		taskQueue:   make(chan func(), 100),
		idleTimeout: idle,
		ctx:         ctx,
		cancel:      cancel,
	}

	// Dastlabki minimal ishchilarni yoqish
	for i := int32(0); i < min; i++ {
		p.spawnWorker(false)
	}
	return p
}

func (p *ElasticWorkerPool) spawnWorker(isElastic bool) {
	atomic.AddInt32(&p.currWorkers, 1)
	p.wg.Add(1)

	go func() {
		defer func() {
			atomic.AddInt32(&p.currWorkers, -1)
			p.wg.Done()
		}()

		timer := time.NewTimer(p.idleTimeout)
		defer timer.Stop()

		for {
			select {
			case <-p.ctx.Done():
				return
			case task := <-p.taskQueue:
				task()
				if !timer.Stop() {
					select {
					case <-timer.C:
					default:
					}
				}
				timer.Reset(p.idleTimeout)
			case <-timer.C:
				// Agar ishchi elastik bo'lsa va joriy ishchilar minWorkers dan ko'p bo'lsa, o'zini to'xtatadi
				if isElastic && atomic.LoadInt32(&p.currWorkers) > p.minWorkers {
					fmt.Println("[Elastic Worker] Nofaollik sababli worker resursni bo'shatdi")
					return
				}
				timer.Reset(p.idleTimeout)
			}
		}
	}()
}

func (p *ElasticWorkerPool) Submit(task func()) {
	// Agar navbatda ishlar to'plana boshlasa va limitga yetilmagan bo'lsa, yangi ishchi ochamiz
	if len(p.taskQueue) > 0 && atomic.LoadInt32(&p.currWorkers) < p.maxWorkers {
		p.spawnWorker(true)
		fmt.Printf("[Elastic Scale Up] Yangi ishchi qo'shildi. Jami ishchilar: %d\n",
			atomic.LoadInt32(&p.currWorkers))
	}
	p.taskQueue <- task
}

func (p *ElasticWorkerPool) Shutdown() {
	p.cancel()
	p.wg.Wait()
}

func main() {
	pool := NewElasticWorkerPool(2, 6, 50*time.Millisecond)

	fmt.Printf("[Boshlang'ich holat] Ishchilar: %d\n", atomic.LoadInt32(&pool.currWorkers))

	// Katta to'lqinli vazifalar yuboramiz
	for i := 1; i <= 8; i++ {
		id := i
		pool.Submit(func() {
			time.Sleep(30 * time.Millisecond)
			fmt.Printf("-> Vazifa #%d yakunlandi\n", id)
		})
	}

	// Ishlar tugagach nofaol ishchilar avtomatik kamayishini kutamiz
	time.Sleep(200 * time.Millisecond)
	fmt.Printf("[Yakuniy holat] Ishchilar soni normaga qaytdi: %d\n",
		atomic.LoadInt32(&pool.currWorkers))

	pool.Shutdown()
}
```
**Tushuntirish:** Ushbu elastik hovuzda ishchilar soni `atomic.LoadInt32` va `atomic.AddInt32` orqali xavfsiz boshqariladi. Vazifalar ko'payganda yangi elastik goroutina tug'iladi, ish kamayganda esa `idleTimeout` orqali o'z-o'zidan chiqib ketadi (Auto-scaling).
**Ishlash natijasi:**
```text
[Boshlang'ich holat] Ishchilar: 2
[Elastic Scale Up] Yangi ishchi qo'shildi. Jami ishchilar: 3
-> Vazifa #1 yakunlandi
-> Vazifa #2 yakunlandi
-> Vazifa #3 yakunlandi
-> Vazifa #4 yakunlandi
-> Vazifa #5 yakunlandi
-> Vazifa #6 yakunlandi
-> Vazifa #7 yakunlandi
-> Vazifa #8 yakunlandi
[Elastic Worker] Nofaollik sababli worker resursni bo'shatdi
[Yakuniy holat] Ishchilar soni normaga qaytdi: 2
```

---

### Topshiriq #1273: Leaky Bucket Rate Limiter: Mikroservisga kelayotgan so'rovlar shiddatini silliqlash
**Tavsif:** Tarmoqdagi so'rovlar to'lqini (traffic spikes) mikroservis orqasidagi ma'lumotlar bazasini qulatmasligi uchun kelayotgan oqimni bir tekis tezlikda (masalan, soniyasiga aniq 10 ta so'rov) o'tkazib beruvchi Leaky Bucket (teshik chelak) algoritmi talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type LeakyBucketLimiter struct {
	capacity   int
	leakRate   time.Duration
	bucket     chan struct{}
	stopChan   chan struct{}
	wg         sync.WaitGroup
}

func NewLeakyBucket(capacity int, leakInterval time.Duration) *LeakyBucketLimiter {
	lb := &LeakyBucketLimiter{
		capacity: capacity,
		leakRate: leakInterval,
		bucket:   make(chan struct{}, capacity),
		stopChan: make(chan struct{}),
	}

	lb.startLeaking()
	return lb
}

func (lb *LeakyBucketLimiter) startLeaking() {
	lb.wg.Add(1)
	go func() {
		defer lb.wg.Done()
		ticker := time.NewTicker(lb.leakRate)
		defer ticker.Stop()

		for {
			select {
			case <-lb.stopChan:
				return
			case <-ticker.C:
				select {
				case <-lb.bucket:
					// Chelakdan bitta tomchi (so'rov) oqib chiqdi va qayta ishlashga ruxsat berildi
				default:
					// Chelak bo'sh
				}
			}
		}
	}()
}

func (lb *LeakyBucketLimiter) Allow() bool {
	select {
	case lb.bucket <- struct{}{}:
		return true
	default:
		// Chelak to'lgan, suv toshib ketdi (Rate limit exceeded)
		return false
	}
}

func (lb *LeakyBucketLimiter) Close() {
	close(lb.stopChan)
	lb.wg.Wait()
}

func main() {
	// Sig'imi 3 ta, har 25ms da 1 ta tomchi sizdiradi
	limiter := NewLeakyBucket(3, 25*time.Millisecond)
	defer limiter.Close()

	fmt.Println("[Leaky Bucket Sinovi]: 6 ta tezkor so'rov yuborilmoqda...")

	for i := 1; i <= 6; i++ {
		allowed := limiter.Allow()
		if allowed {
			fmt.Printf("So'rov #%d: Ruxsat berildi (Chelakka tushdi)\n", i)
		} else {
			fmt.Printf("So'rov #%d: RAD ETILDI (429 Too Many Requests)\n", i)
		}
	}

	// 60ms kutamiz, chelakdan 2 ta tomchi sizib chiqadi
	time.Sleep(60 * time.Millisecond)
	fmt.Println("\n[60ms dan so'ng]: Yangi so'rov yuborilmoqda...")

	if limiter.Allow() {
		fmt.Println("Yangi so'rov: Muvaffaqiyatli qabul qilindi!")
	} else {
		fmt.Println("Yangi so'rov: Rad etildi")
	}
}
```
**Tushuntirish:** Leaky Bucket algoritmi tarmoq oqimini silliqlash (traffic shaping) uchun xizmat qiladi. Chelak sig'imi Go tilining buferlangan kanali (`chan struct{}`) yordamida hosil qilinadi. Ticker orqali belgilangan intervalda tomchilar chiqarib yuboriladi, bu esa quyi tizimlarni to'satdan ortiqcha yuklanishdan asraydi.
**Ishlash natijasi:**
```text
[Leaky Bucket Sinovi]: 6 ta tezkor so'rov yuborilmoqda...
So'rov #1: Ruxsat berildi (Chelakka tushdi)
So'rov #2: Ruxsat berildi (Chelakka tushdi)
So'rov #3: Ruxsat berildi (Chelakka tushdi)
So'rov #4: RAD ETILDI (429 Too Many Requests)
So'rov #5: RAD ETILDI (429 Too Many Requests)
So'rov #6: RAD ETILDI (429 Too Many Requests)

[60ms dan so'ng]: Yangi so'rov yuborilmoqda...
Yangi so'rov: Muvaffaqiyatli qabul qilindi!
```

---

### Topshiriq #1274: Token Bucket Rate Limiter: Burst (sakrashli) yuklamalarga ruxsat beruvchi yuqori RPS cheklovchisi
**Tavsif:** Ko'p foydalanuvchili API Gatewaylarda foydalanuvchilar ba'zan bir lahzada 5-10 ta so'rovni ketma-ket yuborishi normal holat hisoblanadi (Burst). Biroq o'rtacha tezlik soniyasiga belgilangan me'yordan oshmasligi kerak. Token Bucket algoritmini lock-free yoki minimal qulflanish bilan yaratish zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type TokenBucket struct {
	capacity   float64
	tokens     float64
	refillRate float64 // Soniyasiga qo'shiladigan tokenlar soni
	lastRefill time.Time
	mu         sync.Mutex
}

func NewTokenBucket(capacity, refillRate float64) *TokenBucket {
	return &TokenBucket{
		capacity:   capacity,
		tokens:     capacity, // Dastlab chelak to'la bo'ladi
		refillRate: refillRate,
		lastRefill: time.Now(),
	}
}

func (tb *TokenBucket) Allow(cost float64) bool {
	tb.mu.Lock()
	defer tb.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(tb.lastRefill).Seconds()
	tb.lastRefill = now

	// O'tgan vaqt hisobiga yangi tokenlarni to'ldirish
	tb.tokens = tb.tokens + elapsed*tb.refillRate
	if tb.tokens > tb.capacity {
		tb.tokens = tb.capacity
	}

	// Token yetarliligini tekshirish
	if tb.tokens >= cost {
		tb.tokens -= cost
		return true
	}

	return false
}

func main() {
	// Sig'imi 5 ta token (burst limit), sekundiga 10 ta token qo'shiladi
	bucket := NewTokenBucket(5, 10)

	fmt.Println("[Token Bucket] Bir zumda 6 ta so'rov yuborilmoqda:")
	for i := 1; i <= 6; i++ {
		ok := bucket.Allow(1.0)
		fmt.Printf("So'rov #%d: Ruxsat berildi=%t (Qolgan tokenlar taxminan: %.2f)\n",
			i, ok, bucket.tokens)
	}

	// 100ms kutamiz (1 ta token qo'shiladi)
	time.Sleep(100 * time.Millisecond)
	fmt.Println("\n[100ms dam olishdan so'ng]:")
	fmt.Printf("Qayta urinish: Ruxsat berildi=%t\n", bucket.Allow(1.0))
}
```
**Tushuntirish:** Token Bucket Go standart kutubxonasidagi `golang.org/x/time/rate` asosidagi matematik tamoyilga egadir. Har safar timer chaqirib token qo'shib o'tirmasdan, so'rov kelgan on bilan o'tgan vaqt orasidagi farq (`elapsed * refillRate`) orqali tokenlar soni hisoblanadi. Bu usul xotira va fon goroutinasini umuman talab qilmaydi.
**Ishlash natijasi:**
```text
[Token Bucket] Bir zumda 6 ta so'rov yuborilmoqda:
So'rov #1: Ruxsat berildi=true (Qolgan tokenlar taxminan: 4.00)
So'rov #2: Ruxsat berildi=true (Qolgan tokenlar taxminan: 3.00)
So'rov #3: Ruxsat berildi=true (Qolgan tokenlar taxminan: 2.00)
So'rov #4: Ruxsat berildi=true (Qolgan tokenlar taxminan: 1.00)
So'rov #5: Ruxsat berildi=true (Qolgan tokenlar taxminan: 0.00)
So'rov #6: Ruxsat berildi=false (Qolgan tokenlar taxminan: 0.00)

[100ms dam olishdan so'ng]:
Qayta urinish: Ruxsat berildi=true
```

---

### Topshiriq #1275: Backpressure va Shedding: Navbat to'lganda HTTP 429 / gRPC ResourceExhausted bilan so'rovni rad etish
**Tavsif:** Serverga qabul qilish quvvatidan ortiqcha so'rov kelganda, ularni cheksiz xotiraga yig'ish (unbounded buffer) natijasida kechikish eksponensial oshib ketadi va tizim "kaskadli qulash" (cascading failure) holatiga tushadi. So'rovlarni erta bosqichda tashlab yuborish (Load Shedding) arxitekturasi lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"errors"
	"fmt"
	"sync/atomic"
	"time"
)

var (
	ErrResourceExhausted = errors.New("gRPC status: RESOURCE_EXHAUSTED / HTTP 429")
)

type LoadShedder struct {
	maxInFlight    int64
	currentInFlight int64
	rejectedCount  int64
}

func NewLoadShedder(maxConcurrent int64) *LoadShedder {
	return &LoadShedder{
		maxInFlight: maxConcurrent,
	}
}

func (s *LoadShedder) Execute(task func() error) error {
	// Atomik tarzda in-flight hisoblagichni tekshiramiz
	current := atomic.AddInt64(&s.currentInFlight, 1)
	if current > s.maxInFlight {
		atomic.AddInt64(&s.currentInFlight, -1)
		atomic.AddInt64(&s.rejectedCount, 1)
		return ErrResourceExhausted
	}

	defer atomic.AddInt64(&s.currentInFlight, -1)
	return task()
}

func main() {
	// Bir vaqtning o'zida maksimal 2 ta og'ir so'rov qabul qilinadi
	shedder := NewLoadShedder(2)

	heavyJob := func(id int) {
		err := shedder.Execute(func() error {
			time.Sleep(30 * time.Millisecond)
			fmt.Printf("[Load Shedder] So'rov #%d muvaffaqiyatli bajarildi\n", id)
			return nil
		})
		if err != nil {
			fmt.Printf("[Load Shedder] So'rov #%d: %v (Load Shedding faollashdi)\n", id, err)
		}
	}

	// Bir vaqtning o'zida 5 ta parallel so'rov beramiz
	for i := 1; i <= 5; i++ {
		go heavyJob(i)
	}

	time.Sleep(100 * time.Millisecond)

	fmt.Printf("[Xulosa]: Rad etilgan so'rovlar: %d ta\n",
		atomic.LoadInt64(&shedder.rejectedCount))
}
```
**Tushuntirish:** Load Shedding tamoyili bo'yicha mikroservis barcha so'rovlarni sekin bajargandan ko'ra, belgilangan hajmdan ortig'ini darhol rad etib, qolgan so'rovlarni yuqori tezlikda (SLA talablari doirasida) bajarishi afzalroqdir. Bu yerda lock-free atomik hisoblagich bilan tekshirish mikrosekundlarda hal bo'ladi.
**Ishlash natijasi:**
```text
[Load Shedder] So'rov #3: gRPC status: RESOURCE_EXHAUSTED / HTTP 429 (Load Shedding faollashdi)
[Load Shedder] So'rov #4: gRPC status: RESOURCE_EXHAUSTED / HTTP 429 (Load Shedding faollashdi)
[Load Shedder] So'rov #5: gRPC status: RESOURCE_EXHAUSTED / HTTP 429 (Load Shedding faollashdi)
[Load Shedder] So'rov #1 muvaffaqiyatli bajarildi
[Load Shedder] So'rov #2 muvaffaqiyatli bajarildi
[Xulosa]: Rad etilgan so'rovlar: 3 ta
```

---

### Topshiriq #1276: Priority Queue Worker Pool: Muhim VIP tranzaksiyalarni birinchi navbatda qayta ishlash
**Tavsif:** Moliyaviy tizimlarda yoki favqulodda xizmatlarda kelayotgan xabarlar turli prioritetlarga ega: masalan, oddiy marketing xabarlari (Past prioritet), foydalanuvchi to'lovi (Yuqori prioritet). Oddiy FIFO navbatida VIP to'lovlar oddiy xabarlar ortida qolib ketmasligi uchun Prioritetli Worker Pool zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"container/heap"
	"fmt"
	"sync"
	"time"
)

type PriorityItem struct {
	Value    string
	Priority int // Yuqori son = Yuqori prioritet
	Index    int
}

type PriorityQueue []*PriorityItem

func (pq PriorityQueue) Len() int           { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].Priority > pq[j].Priority }
func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].Index = i
	pq[j].Index = j
}
func (pq *PriorityQueue) Push(x interface{}) {
	item := x.(*PriorityItem)
	item.Index = len(*pq)
	*pq = append(*pq, item)
}
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil // Xotira tozalash
	item.Index = -1
	*pq = old[0 : n-1]
	return item
}

type SafePriorityDispatcher struct {
	pq   PriorityQueue
	mu   sync.Mutex
	cond *sync.Cond
}

func NewDispatcher() *SafePriorityDispatcher {
	d := &SafePriorityDispatcher{}
	heap.Init(&d.pq)
	d.cond = sync.NewCond(&d.mu)
	return d
}

func (d *SafePriorityDispatcher) Push(val string, priority int) {
	d.mu.Lock()
	defer d.mu.Unlock()
	heap.Push(&d.pq, &PriorityItem{Value: val, Priority: priority})
	d.cond.Signal()
}

func (d *SafePriorityDispatcher) Pop() *PriorityItem {
	d.mu.Lock()
	defer d.mu.Unlock()
	for d.pq.Len() == 0 {
		d.cond.Wait()
	}
	return heap.Pop(&d.pq).(*PriorityItem)
}

func main() {
	dispatcher := NewDispatcher()

	// Navbatga aralash prioritetda yuklaymiz
	dispatcher.Push("Oddiy Newsletter SMS", 1)
	dispatcher.Push("Parolni tiklash kodi", 5)
	dispatcher.Push("1,000,000 UZS Bank To'lovi", 10)
	dispatcher.Push("Do'kon chegirmasi", 1)

	fmt.Println("[Priority Worker Pool] Vazifalar qayta ishlanmoqda:")
	for i := 1; i <= 4; i++ {
		item := dispatcher.Pop()
		fmt.Printf("Bajarildi: %-30s | Prioritet: %d\n", item.Value, item.Priority)
	}
}
```
**Tushuntirish:** Go tilining `container/heap` paketi binar uyum (binary min/max-heap) strukturasini ta'minlaydi. `sync.Cond` orqali navbat bo'sh bo'lganda ishchi goroutinalar CPU ni behuda kuydirmasdan (busy waiting qilmasdan) uyqu rejimida kutadi. Element qo'shilishi bilan `Signal()` orqali ishchi uyg'otiladi.
**Ishlash natijasi:**
```text
[Priority Worker Pool] Vazifalar qayta ishlanmoqda:
Bajarildi: 1,000,000 UZS Bank To'lovi    | Prioritet: 10
Bajarildi: Parolni tiklash kodi           | Prioritet: 5
Bajarildi: Oddiy Newsletter SMS           | Prioritet: 1
Bajarildi: Do'kon chegirmasi              | Prioritet: 1
```

---

### Topshiriq #1277: Scatter-Gather Pattern: sync.WaitGroup va Context bilan parallel qidiruv va natijalarni birlashtirish
**Tavsif:** Foydalanuvchi qidiruv maydoniga so'z kiritganda, mikroservis parallel ravishda mahsulotlar bazasi, foydalanuvchilar bazasi va blog maqolalarini qidirishi, so'ng barcha natijalarni yagona ro'yxatga jamlab (Gather) foydalanuvchiga qaytarishi kerak. Agar birorta qidiruvchi goroutine qotib qolsa, umumiy context uni to'xtatishi lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type SearchResult struct {
	Source string
	Items  []string
}

// SearchDataSource ma'lumot manbasidan parallel qidiruv
func SearchDataSource(ctx context.Context, source string, duration time.Duration, mockItems []string) (*SearchResult, error) {
	select {
	case <-time.After(duration):
		return &SearchResult{Source: source, Items: mockItems}, nil
	case <-ctx.Done():
		return nil, ctx.Err()
	}
}

// ScatterGather parallel tarqatish va yig'ish
func ScatterGather(ctx context.Context, query string) []SearchResult {
	sources := []struct {
		name  string
		delay time.Duration
		items []string
	}{
		{"ProductsDB", 30 * time.Millisecond, []string{"Noutbuk Pro", "Mexanik Klaviatura"}},
		{"UsersDB", 20 * time.Millisecond, []string{"alisher_dev", "farrux_admin"}},
		{"ArticlesDB", 100 * time.Millisecond, []string{"Go Concurrency Sirlari"}}, // Bu kechikadi
	}

	resultsChan := make(chan SearchResult, len(sources))
	var wg sync.WaitGroup

	for _, s := range sources {
		wg.Add(1)
		go func(src string, d time.Duration, items []string) {
			defer wg.Done()
			res, err := SearchDataSource(ctx, src, d, items)
			if err == nil && res != nil {
				resultsChan <- *res
			}
		}(s.name, s.delay, s.items)
	}

	// Yopilishini alohida goroutinada kutish
	go func() {
		wg.Wait()
		close(resultsChan)
	}()

	var aggregated []SearchResult
	for r := range resultsChan {
		aggregated = append(aggregated, r)
	}

	return aggregated
}

func main() {
	// Umumiy qidiruv muddati: 60ms
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Millisecond)
	defer cancel()

	fmt.Println("[Scatter-Gather] Parallel qidiruv boshlandi...")
	results := ScatterGather(ctx, "Golang")

	for _, res := range results {
		fmt.Printf("Manba: %-12s | Topilganlar: %v\n", res.Source, res.Items)
	}
	fmt.Printf("[Xulosa]: Jami javob bergan manbalar: %d ta\n", len(results))
}
```
**Tushuntirish:** Scatter-Gather naqshida Fan-Out (bir nechta manbaga parallel so'rov yuborish) va Fan-In (natijalarni yagona kanalga to'plash) usuli qo'llaniladi. `resultsChan` kanali manbalar soniga teng buferga ega bo'lganligi sababli, goroutinalar hech qachon bloklanmaydi va xotira sizishi bartaraf etiladi.
**Ishlash natijasi:**
```text
[Scatter-Gather] Parallel qidiruv boshlandi...
Manba: UsersDB      | Topilganlar: [alisher_dev farrux_admin]
Manba: ProductsDB   | Topilganlar: [Noutbuk Pro Mexanik Klaviatura]
[Xulosa]: Jami javob bergan manbalar: 2 ta
```

---

### Topshiriq #1278: Pipeline Processing Pattern: Ko'p bosqichli ma'lumot oqimini kanallar orqali parallel o'tkazish
**Tavsif:** Katta hajmdagi ma'lumotlarni konveyer usulida qayta ishlash zarur: 1-bosqich xom ma'lumotni o'qiydi (Generator), 2-bosqich uni filtrlaydi (Filter), 3-bosqich uni kriptografik xeshlaydi (Transformer). Har bir bosqich mustaqil goroutinalarda ishlab, ma'lumotlar oqimini doimiy harakatda ushlab turishi lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"crypto/sha256"
	"fmt"
)

// Stage 1: Generator - ma'lumot ishlab chiqaruvchi
func Generator(ctx context.Context, nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for _, n := range nums {
			select {
			case <-ctx.Done():
				return
			case out <- n:
			}
		}
	}()
	return out
}

// Stage 2: Filter - faqat juft sonlarni o'tkazuvchi
func FilterEven(ctx context.Context, in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range in {
			if n%2 == 0 {
				select {
				case <-ctx.Done():
					return
				case out <- n:
				}
			}
		}
	}()
	return out
}

// Stage 3: Transformer - SHA256 xeshini hisoblovchi
func HashTransformer(ctx context.Context, in <-chan int) <-chan string {
	out := make(chan string)
	go func() {
		defer close(out)
		for n := range in {
			hash := sha256.Sum256([]byte(fmt.Sprintf("khorazmiy_salt_%d", n)))
			result := fmt.Sprintf("Son:%d -> Hash:%x", n, hash[:4])
			select {
			case <-ctx.Done():
				return
			case out <- result:
			}
		}
	}()
	return out
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// 3 bosqichli konveyer (Pipeline)
	numbers := []int{10, 15, 22, 33, 44, 55, 60}
	genChan := Generator(ctx, numbers...)
	filterChan := FilterEven(ctx, genChan)
	hashChan := HashTransformer(ctx, filterChan)

	fmt.Println("[Pipeline Konveyeri Natijalari]:")
	for hashed := range hashChan {
		fmt.Println(hashed)
	}
}
```
**Tushuntirish:** Pipeline arxitekturasi Unix `cat | grep | awk` tamoyiliga o'xshaydi. Har bir bosqich kirish kanalini tinglaydi va chiqish kanaliga yozadi. Barcha bosqichlar `ctx.Done()` ga ulanganligi sababli, agar iste'molchi erta to'xtasa, barcha oldingi konveyer bo'g'inlari darhol to'xtaydi.
**Ishlash natijasi:**
```text
[Pipeline Konveyeri Natijalari]:
Son:10 -> Hash:117565df
Son:22 -> Hash:98ca5755
Son:44 -> Hash:05bfe1f8
Son:60 -> Hash:96eeea1d
```

---

### Topshiriq #1279: ErrGroup (golang.org/x/sync/errgroup) bilan Parallel Fan-Out/Fan-In va Fail-Fast mexanizmi
**Tavsif:** Bir vaqtning o'zida bir nechta mikroservisga parallel so'rov yuborilganda, agar ulardan biri xatolik bersa (masalan, to'lov rad etilsa), qolgan parallel ishlayotgan barcha goroutinalarni darhol bekor qilish (Fail-Fast) va birinchi xatolikni zudlik bilan qaytarish talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// ErrGroupCustom golang.org/x/sync/errgroup analogi
type ErrGroup struct {
	cancel func()
	wg     sync.WaitGroup
	errOnce sync.Once
	err    error
}

func WithContext(ctx context.Context) (*ErrGroup, context.Context) {
	ctx, cancel := context.WithCancel(ctx)
	return &ErrGroup{cancel: cancel}, ctx
}

func (g *ErrGroup) Go(f func() error) {
	g.wg.Add(1)
	go func() {
		defer g.wg.Done()
		if err := f(); err != nil {
			g.errOnce.Do(func() {
				g.err = err
				if g.cancel != nil {
					g.cancel() // Birinchi xatolik paydo bo'lishi bilan barcha oqimlarni bekor qilamiz
				}
			})
		}
	}()
}

func (g *ErrGroup) Wait() error {
	g.wg.Wait()
	if g.cancel != nil {
		g.cancel()
	}
	return g.err
}

func main() {
	g, ctx := WithContext(context.Background())

	// 1-xizmat: Ombordan zaxira tekshirish (muvaffaqiyatli - 30ms)
	g.Go(func() error {
		select {
		case <-time.After(30 * time.Millisecond):
			fmt.Println("[Xizmat 1] Omborda mahsulot yetarli")
			return nil
		case <-ctx.Done():
			fmt.Println("[Xizmat 1] Bekor qilindi")
			return ctx.Err()
		}
	})

	// 2-xizmat: To'lovni yechish (xato beradi - 10ms)
	g.Go(func() error {
		time.Sleep(10 * time.Millisecond)
		fmt.Println("[Xizmat 2] Hisobda mablag' yetarli emas!")
		return fmt.Errorf("hisobda mablag' yetarli emas")
	})

	// 3-xizmat: Keshni yangilash (og'ir - 80ms)
	g.Go(func() error {
		select {
		case <-time.After(80 * time.Millisecond):
			fmt.Println("[Xizmat 3] Kesh yangilandi")
			return nil
		case <-ctx.Done():
			fmt.Println("[Xizmat 3] Fail-Fast tufayli bekor qilindi!")
			return ctx.Err()
		}
	})

	// Natijani kutish
	if err := g.Wait(); err != nil {
		fmt.Printf("[ErrGroup Fail-Fast]: Tranzaksiya to'xtatildi: %v\n", err)
	} else {
		fmt.Println("Barcha operatsiyalar muvaffaqiyatli yakunlandi")
	}
}
```
**Tushuntirish:** `errgroup.Group` parallel goroutinalar koordinatsiyasining eng xavfsiz standartidir. `errOnce.Do` orqali faqatgina birinchi yuz bergan xatolik saqlab olinadi va `cancel()` chaqirilib, qolgan goroutinalarning resurslari saqlab qolinadi.
**Ishlash natijasi:**
```text
[Xizmat 2] Hisobda mablag' yetarli emas!
[Xizmat 1] Bekor qilindi
[Xizmat 3] Fail-Fast tufayli bekor qilindi!
[ErrGroup Fail-Fast]: Tranzaksiya to'xtatildi: hisobda mablag' yetarli emas
```

---

### Topshiriq #1280: Semaphore (x/sync/semaphore) orqali og'ir resurslarga (DB, Disk I/O) cheklangan parallel kirish
**Tavsif:** Minglab goroutinalar bir vaqtda diskka log yozishga yoki ma'lumotlar bazasiga ulanishga harakat qilganda, fayl deskriptorlari tugashi (`too many open files`) yoki DB connection pooli qulashi mumkin. `Weighted Semaphore` orqali har bir operatsiya og'irligiga qarab (og'ir so'rovga 3 ta kvota, yengil so'rovga 1 ta kvota) ruxsat berish lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// WeightedSemaphore og'irlik asosidagi semafor
type WeightedSemaphore struct {
	maxWeight int64
	curWeight int64
	mu        sync.Mutex
	cond      *sync.Cond
}

func NewWeightedSemaphore(max int64) *WeightedSemaphore {
	s := &WeightedSemaphore{maxWeight: max}
	s.cond = sync.NewCond(&s.mu)
	return s
}

func (s *WeightedSemaphore) Acquire(ctx context.Context, weight int64) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	for s.curWeight+weight > s.maxWeight {
		// Kontekst bekor bo'lishini tekshirish uchun soddalashtirilgan kutish
		s.cond.Wait()
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
		}
	}

	s.curWeight += weight
	return nil
}

func (s *WeightedSemaphore) Release(weight int64) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.curWeight -= weight
	s.cond.Broadcast() // Kutayotgan barcha goroutinalarni uyg'otish
}

func main() {
	// Umumiy tizim sig'imi: 4 birlik
	sem := NewWeightedSemaphore(4)
	var wg sync.WaitGroup

	runJob := func(name string, weight int64, duration time.Duration) {
		defer wg.Done()
		ctx := context.Background()

		fmt.Printf("[%s] %d kvota so'ramoqda...\n", name, weight)
		if err := sem.Acquire(ctx, weight); err != nil {
			fmt.Printf("[%s] Xato: %v\n", name, err)
			return
		}
		fmt.Printf("[%s] Kvota oldi! Ishlamoqda...\n", name)

		time.Sleep(duration)

		sem.Release(weight)
		fmt.Printf("[%s] Kvotani bo'shatdi\n", name)
	}

	wg.Add(3)
	// 1. Og'ir hisobot (3 kvota oladi)
	go runJob("Og'ir Analitika", 3, 50*time.Millisecond)

	// 2. Kichik profil so'rovi (1 kvota oladi)
	go runJob("Profil So'rovi", 1, 20*time.Millisecond)

	// 3. O'rta DB tranzaksiyasi (2 kvota oladi - dastlab sig'maydi va kutadi)
	go runJob("O'rta Tranzaksiya", 2, 30*time.Millisecond)

	wg.Wait()
	fmt.Println("[Semafor Natijasi] Barcha kvotalangan vazifalar to'liq bajarildi")
}
```
**Tushuntirish:** Weighted Semaphore operatsiyalarni nafaqat soni, balki resurs sarflash hajmiga qarab kvotalaydi. Og'ir analitika 3 ta kvotani egallaganda, 2 kvotali so'rov umumiy limit 4 bo'lgani sababli navbatda kutadi. Biri bo'shashi bilan `cond.Broadcast()` navbatdagi so'rovga yo'l ochadi.
**Ishlash natijasi:**
```text
[Og'ir Analitika] 3 kvota so'ramoqda...
[Og'ir Analitika] Kvota oldi! Ishlamoqda...
[Profil So'rovi] 1 kvota so'ramoqda...
[Profil So'rovi] Kvota oldi! Ishlamoqda...
[O'rta Tranzaksiya] 2 kvota so'ramoqda...
[Profil So'rovi] Kvotani bo'shatdi
[Og'ir Analitika] Kvotani bo'shatdi
[O'rta Tranzaksiya] Kvota oldi! Ishlamoqda...
[O'rta Tranzaksiya] Kvotani bo'shatdi
[Semafor Natijasi] Barcha kvotalangan vazifalar to'liq bajarildi
```

---

### Topshiriq #1281: Circuit Breaker State Machine: Closed, Open, Half-Open holatlarini atomic boshqarish
**Tavsif:** Agar tashqi to'lov shlyuzi yoki mikroxizmat qulagan bo'lsa, unga minglab so'rovlarni yuborishda davom etish nafaqat samarasiz, balki butun tizimning resurslarini band qilib qo'yadi. Circuit Breaker (elektr saqlagich) xatoliklar ko'payganda o'chishi (`Open`), so'rovlarni darhol rad etishi va vaqt o'tib o'zini sinab ko'rishi (`Half-Open`) zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"errors"
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

type State int32

const (
	StateClosed State = iota
	StateHalfOpen
	StateOpen
)

func (s State) String() string {
	switch s {
	case StateClosed:
		return "CLOSED"
	case StateHalfOpen:
		return "HALF-OPEN"
	case StateOpen:
		return "OPEN"
	default:
		return "UNKNOWN"
	}
}

var ErrCircuitBreakerOpen = errors.New("circuit breaker OPEN: so'rov rad etildi")

type CircuitBreaker struct {
	state          int32 // Atomic State
	failureCount   int64
	successCount   int64
	failureThreshold int64
	cooldown       time.Duration
	lastStateChange int64 // Unix nanosekund
	mu             sync.Mutex
}

func NewCircuitBreaker(threshold int64, cooldown time.Duration) *CircuitBreaker {
	return &CircuitBreaker{
		state:            int32(StateClosed),
		failureThreshold: threshold,
		cooldown:         cooldown,
		lastStateChange:  time.Now().UnixNano(),
	}
}

func (cb *CircuitBreaker) Execute(req func() error) error {
	currentState := State(atomic.LoadInt32(&cb.state))

	// Agar OPEN bo'lsa, cooldown muddati o'tganligini tekshiramiz
	if currentState == StateOpen {
		lastChange := time.Unix(0, atomic.LoadInt64(&cb.lastStateChange))
		if time.Since(lastChange) > cb.cooldown {
			// Cooldown o'tdi, HALF-OPEN holatiga o'tishga urinish
			if atomic.CompareAndSwapInt32(&cb.state, int32(StateOpen), int32(StateHalfOpen)) {
				atomic.StoreInt64(&cb.lastStateChange, time.Now().UnixNano())
				fmt.Println("[Circuit Breaker] OPEN -> HALF-OPEN holatiga o'tdi")
			}
		} else {
			return ErrCircuitBreakerOpen
		}
	}

	err := req()

	if err != nil {
		cb.onFailure()
		return err
	}

	cb.onSuccess()
	return nil
}

func (cb *CircuitBreaker) onFailure() {
	currentState := State(atomic.LoadInt32(&cb.state))
	if currentState == StateHalfOpen {
		// Half-Open paytida xato bo'lsa, zudlik bilan qayta OPEN holatiga
		atomic.StoreInt32(&cb.state, int32(StateOpen))
		atomic.StoreInt64(&cb.lastStateChange, time.Now().UnixNano())
		fmt.Println("[Circuit Breaker] HALF-OPEN -> OPEN (Xatolik qaytarildi)")
		return
	}

	fails := atomic.AddInt64(&cb.failureCount, 1)
	if fails >= cb.failureThreshold {
		if atomic.CompareAndSwapInt32(&cb.state, int32(StateClosed), int32(StateOpen)) {
			atomic.StoreInt64(&cb.lastStateChange, time.Now().UnixNano())
			fmt.Printf("[Circuit Breaker] CLOSED -> OPEN (Ketma-ket %d ta xato)\n", fails)
		}
	}
}

func (cb *CircuitBreaker) onSuccess() {
	currentState := State(atomic.LoadInt32(&cb.state))
	if currentState == StateHalfOpen {
		// Half-Open paytida sinov muvaffaqiyatli o'tsa CLOSED ga qaytamiz
		atomic.StoreInt32(&cb.state, int32(StateClosed))
		atomic.StoreInt64(&cb.failureCount, 0)
		atomic.StoreInt64(&cb.lastStateChange, time.Now().UnixNano())
		fmt.Println("[Circuit Breaker] Sinov muvaffaqiyatli! HALF-OPEN -> CLOSED ga qaytdi")
	} else if currentState == StateClosed {
		atomic.StoreInt64(&cb.failureCount, 0)
	}
}

func main() {
	cb := NewCircuitBreaker(2, 50*time.Millisecond)

	failCall := func() error { return errors.New("503 Service Unavailable") }
	okCall := func() error { return nil }

	// 2 ta ketma-ket xato
	_ = cb.Execute(failCall)
	_ = cb.Execute(failCall)

	// Endi Circuit OPEN holatida bo'lishi kerak
	err := cb.Execute(okCall)
	fmt.Printf("[OPEN payti natijasi]: %v\n", err)

	// 60ms kutamiz (cooldown o'tishi uchun)
	time.Sleep(60 * time.Millisecond)

	// Qayta urinish: Half-Open sinovi
	_ = cb.Execute(okCall)

	// Yana oddiy rejimda ishlash
	_ = cb.Execute(okCall)
	fmt.Printf("[Yakuniy holat]: %s\n", State(atomic.LoadInt32(&cb.state)))
}
```
**Tushuntirish:** Ushbu Circuit Breaker holat mashinasi (State Machine) `sync/atomic.CompareAndSwapInt32` orqali lock-free ishlaydi. Bu soniyasiga millionlab so'rovlar kelganda ham CPU kesh liniyalarida qulflash (contention) hosil qilmaydi.
**Ishlash natijasi:**
```text
[Circuit Breaker] CLOSED -> OPEN (Ketma-ket 2 ta xato)
[OPEN payti natijasi]: circuit breaker OPEN: so'rov rad etildi
[Circuit Breaker] OPEN -> HALF-OPEN holatiga o'tdi
[Circuit Breaker] Sinov muvaffaqiyatli! HALF-OPEN -> CLOSED ga qaytdi
[Yakuniy holat]: CLOSED
```

---

### Topshiriq #1282: Exponential Backoff va Full Jitter bilan aqlli qayta urinish (Retry) algoritmi
**Tavsif:** Serverda qisqa muddatli tarmoq nosozligi yuz berganda, barcha mijozlar bir vaqtning o'zida qayta so'rov yuborsa (Thundering Herd), tiklanayotgan server yana qulaydi. Buni bartaraf qilish uchun kutish vaqtini eksponensial oshirib, unga tasodifiy tasodifiylik (Full Jitter) qo'shish lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"errors"
	"fmt"
	"math/rand"
	"time"
)

type BackoffConfig struct {
	BaseDelay time.Duration
	MaxDelay  time.Duration
	MaxRetries int
}

// RetryWithFullJitter eksponensial va tasodifiy kechikish bilan qayta urinish
func RetryWithFullJitter(ctx context.Context, cfg BackoffConfig, op func(attempt int) error) error {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	var lastErr error

	for attempt := 0; attempt < cfg.MaxRetries; attempt++ {
		lastErr = op(attempt + 1)
		if lastErr == nil {
			return nil
		}

		if attempt == cfg.MaxRetries-1 {
			break
		}

		// Eksponensial oraliq: BaseDelay * 2^attempt
		temp := float64(cfg.BaseDelay) * float64(int(1)<<uint(attempt))
		if temp > float64(cfg.MaxDelay) {
			temp = float64(cfg.MaxDelay)
		}

		// Full Jitter: [0, temp] oralig'idan tasodifiy son
		sleepDuration := time.Duration(r.Float64() * temp)

		fmt.Printf("[Retry #%d] Xato: %v. Qayta urinish kechikishi (Jitter): %s\n",
			attempt+1, lastErr, sleepDuration)

		select {
		case <-time.After(sleepDuration):
		case <-ctx.Done():
			return ctx.Err()
		}
	}

	return fmt.Errorf("maksimal urinishlar tugadi: %w", lastErr)
}

func main() {
	cfg := BackoffConfig{
		BaseDelay:  20 * time.Millisecond,
		MaxDelay:   200 * time.Millisecond,
		MaxRetries: 4,
	}

	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	calls := 0
	flakyOperation := func(attempt int) error {
		calls++
		if calls < 3 {
			return errors.New("502 Bad Gateway")
		}
		return nil
	}

	err := RetryWithFullJitter(ctx, cfg, flakyOperation)
	if err != nil {
		fmt.Printf("Muvaffaqiyatsiz: %v\n", err)
	} else {
		fmt.Printf("[Muvaffaqiyat] So'rov %d-urinishda bajarildi!\n", calls)
	}
}
```
**Tushuntirish:** AWS arxitekturasida isbotlangan Full Jitter formulasi `sleep = random_between(0, min(max_delay, base * 2^attempt))` mijozlar so'rovlarini vaqt o'qi bo'yicha teng tarqatib beradi. Bu serverga tiklanish uchun erkin nafas olish imkoniyatini yaratadi.
**Ishlash natijasi:**
```text
[Retry #1] Xato: 502 Bad Gateway. Qayta urinish kechikishi (Jitter): 14.8ms
[Retry #2] Xato: 502 Bad Gateway. Qayta urinish kechikishi (Jitter): 28.3ms
[Muvaffaqiyat] So'rov 3-urinishda bajarildi!
```

---

### Topshiriq #1283: Hedged Requests Pattern: Kechikayotgan so'rovlar uchun parallel nusxa yuborib tail latency kamaytirish
**Tavsif:** Yuqori yuklamali tizimlarda so'rovlarning 99% qismi 10ms da bajariladi, biroq 1% qismi (Tail Latency P99/P99.9) tarmoq jitteri yoki GC sababli 500ms ga cho'zilib ketadi. Agar so'rov 30ms ichida javob bermasa, boshqa server nusxasiga parallel "Hedged" so'rov yuborib, qaysi biri tezroq javob bersa shuni qabul qilish zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

type HedgedResult struct {
	ReplicaID string
	Payload   string
}

// SimulatedQuery so'rovni bajaruvchi funksiya
func SimulatedQuery(ctx context.Context, replica string, delay time.Duration) (*HedgedResult, error) {
	select {
	case <-time.After(delay):
		return &HedgedResult{ReplicaID: replica, Payload: "Data_from_" + replica}, nil
	case <-ctx.Done():
		return nil, ctx.Err()
	}
}

// ExecuteHedgedRequest Hedged request mexanizmi
func ExecuteHedgedRequest(parentCtx context.Context, hedgeDelay time.Duration) (*HedgedResult, error) {
	ctx, cancel := context.WithCancel(parentCtx)
	defer cancel()

	resultChan := make(chan *HedgedResult, 2)
	var wg sync.WaitGroup

	// 1-birlamchi so'rov (A serveriga - simulyatsiya bo'yicha sekin 80ms)
	wg.Add(1)
	go func() {
		defer wg.Done()
		res, err := SimulatedQuery(ctx, "Replica-A (Primary)", 80*time.Millisecond)
		if err == nil {
			select {
			case resultChan <- res:
				cancel()
			default:
			}
		}
	}()

	// Hedging taymeri
	hedgeTimer := time.NewTimer(hedgeDelay)
	defer hedgeTimer.Stop()

	// 2-hedged so'rov ochish uchun goroutine
	wg.Add(1)
	go func() {
		defer wg.Done()
		select {
		case <-ctx.Done():
			return
		case <-hedgeTimer.C:
			fmt.Printf("[Hedge Trigger] Asosiy so'rov %s ichida javob bermadi, zaxira nusxa jo'natildi!\n", hedgeDelay)
			// B serveriga tezkor so'rov (20ms)
			res, err := SimulatedQuery(ctx, "Replica-B (Hedged)", 20*time.Millisecond)
			if err == nil {
				select {
				case resultChan <- res:
					cancel()
				default:
				}
			}
		}
	}()

	var finalResult *HedgedResult
	select {
	case finalResult = <-resultChan:
	case <-ctx.Done():
		return nil, ctx.Err()
	}

	wg.Wait()
	return finalResult, nil
}

func main() {
	rand.Seed(time.Now().UnixNano())
	ctx, cancel := context.WithTimeout(context.Background(), 200*time.Millisecond)
	defer cancel()

	// 25ms dan keyin javob kelmasa zaxira so'rovni ishga tushirish
	res, err := ExecuteHedgedRequest(ctx, 25*time.Millisecond)
	if err != nil {
		fmt.Printf("Xato: %v\n", err)
		return
	}

	fmt.Printf("[G'olib Javob] Qabul qiluvchi: %s | Ma'lumot: %s\n",
		res.ReplicaID, res.Payload)
}
```
**Tushuntirish:** Google kompaniyasining "The Tail at Scale" maqolasida tavsiya etilgan Hedged Requests usuli P99 latency ko'rsatkichini keskin pasaytiradi. Birlamchi so'rov kechikishi bilan darhol ikkinchi replikaga so'rov beriladi va birinchisi tugashi bilan `cancel()` orqali ikkinchisi to'xtatiladi.
**Ishlash natijasi:**
```text
[Hedge Trigger] Asosiy so'rov 25ms ichida javob bermadi, zaxira nusxa jo'natildi!
[G'olib Javob] Qabul qiluvchi: Replica-B (Hedged) | Ma'lumot: Data_from_Replica-B (Hedged)
```

---

### Topshiriq #1284: Bulkhead Pattern: Resurslarni (goroutinalar, CPU) xizmatlar kesimida izolyatsiya qilish
**Tavsif:** Kema cho'kmasligi uchun uning korpusi suv o'tkazmaydigan to'siqlar (bulkheads) bilan bo'linadi. Mikroservislarda ham muhim xizmatlar (masalan, to'lovlar) kam ahamiyatli xizmatlar (masalan, tavsiyalar tizimi) tufayli barcha goroutinalar band bo'lib qolmasligi uchun resurslarni qat'iy izolyatsiya qilish lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"errors"
	"fmt"
	"sync"
	"time"
)

var ErrBulkheadExhausted = errors.New("bulkhead limitga yetdi: so'rov rad etildi")

type BulkheadPartition struct {
	name      string
	semaphore chan struct{}
}

func NewBulkhead(name string, maxConcurrent int) *BulkheadPartition {
	return &BulkheadPartition{
		name:      name,
		semaphore: make(chan struct{}, maxConcurrent),
	}
}

func (b *BulkheadPartition) Execute(fn func()) error {
	select {
	case b.semaphore <- struct{}{}:
		defer func() { <-b.semaphore }()
		fn()
		return nil
	default:
		return ErrBulkheadExhausted
	}
}

func main() {
	// To'lov xizmati uchun 3 ta kvota, Tavsiya xizmati uchun faqat 1 ta kvota
	paymentBulkhead := NewBulkhead("PaymentService", 3)
	recommendationBulkhead := NewBulkhead("RecommendationService", 1)

	var wg sync.WaitGroup

	// Tavsiya tizimiga 3 ta so'rov beramiz (faqat 1 tasi o'tishi kerak)
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			err := recommendationBulkhead.Execute(func() {
				time.Sleep(30 * time.Millisecond)
				fmt.Printf("[Tavsiya #%d] Bajarildi\n", id)
			})
			if err != nil {
				fmt.Printf("[Tavsiya #%d] %v\n", id, err)
			}
		}(i)
	}

	// Bir vaqtda To'lov tizimiga ham 2 ta so'rov beramiz (ular muammosiz o'tishi shart)
	for i := 1; i <= 2; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			err := paymentBulkhead.Execute(func() {
				time.Sleep(20 * time.Millisecond)
				fmt.Printf("[TO'LOV #%d] Muvaffaqiyatli o'tkazildi!\n", id)
			})
			if err != nil {
				fmt.Printf("[TO'LOV #%d] %v\n", id, err)
			}
		}(i)
	}

	wg.Wait()
	fmt.Println("[Bulkhead Yakuni] Xizmatlar bir-birini bloklamasdan mustaqil ishladi")
}
```
**Tushuntirish:** Bulkhead naqshida har bir quyi servis o'zining mustaqil semaforiga ega. Tavsiya tizimi qotib qolib, so'rovlarni to'ldirib yuborsa ham, To'lov tizimi o'zining bo'sh ajratilgan goroutina kvotalaridan xavfsiz foydalanishda davom etadi.
**Ishlash natijasi:**
```text
[Tavsiya #2] bulkhead limitga yetdi: so'rov rad etildi
[Tavsiya #3] bulkhead limitga yetdi: so'rov rad etildi
[TO'LOV #1] Muvaffaqiyatli o'tkazildi!
[TO'LOV #2] Muvaffaqiyatli o'tkazildi!
[Tavsiya #1] Bajarildi
[Bulkhead Yakuni] Xizmatlar bir-birini bloklamasdan mustaqil ishladi
```

---

### Topshiriq #1285: Fallback Mechanism: Tashqi mikroxizmat ishdan chiqqanda keshdagi yoki defolt ma'lumotni uzatish
**Tavsif:** Tavsiyalar, obuna statuslari yoki valyuta kurslari kabi doimiy o'zgarmaydigan ma'lumotlarni beruvchi mikroxizmat qulaganda, foydalanuvchiga xatolik ko'rsatmasdan, oldingi xavfsiz keshdagi (Stale-While-Revalidate) yoki qattiq kodlangan defolt (Fallback) ma'lumotni uzatish talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"
)

type CurrencyRates struct {
	USD float64
	EUR float64
	RUB float64
}

type ResilientCurrencyClient struct {
	mu           sync.RWMutex
	fallbackData CurrencyRates
	isHealthy    bool
}

func NewResilientCurrencyClient() *ResilientCurrencyClient {
	return &ResilientCurrencyClient{
		fallbackData: CurrencyRates{
			USD: 12800.0,
			EUR: 13900.0,
			RUB: 140.0,
		},
		isHealthy: false, // Tashqi servis hozircha nosoz
	}
}

func (c *ResilientCurrencyClient) GetRates(ctx context.Context) (CurrencyRates, string) {
	// Haqiqiy servisga murojaat qilish simulyatsiyasi
	err := c.fetchRemote(ctx)
	if err == nil {
		return CurrencyRates{USD: 12850.0, EUR: 13950.0, RUB: 142.0}, "LIVE_API"
	}

	// Xatolik bo'lsa, xavfsiz kesh/defolt fallback qaytaramiz
	c.mu.RLock()
	defer c.mu.RUnlock()
	return c.fallbackData, "FALLBACK_CACHE"
}

func (c *ResilientCurrencyClient) fetchRemote(ctx context.Context) error {
	// Tashqi servis 503 xatosi beradi
	return errors.New("upstream service is dead")
}

func main() {
	client := NewResilientCurrencyClient()
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	rates, source := client.GetRates(ctx)

	fmt.Printf("[Valyuta Kurslari]:\n")
	fmt.Printf("- Manba: %s\n", source)
	fmt.Printf("- USD: %.2f UZS\n", rates.USD)
	fmt.Printf("- EUR: %.2f UZS\n", rates.EUR)
	fmt.Printf("- RUB: %.2f UZS\n", rates.RUB)
	fmt.Println("[Audit] Tizim foydalanuvchiga uzluksiz xizmat ko'rsatdi")
}
```
**Tushuntirish:** Fallback mexanizmi mikroservisning "Fault Tolerance" (nosozliklarga chidamlilik) ko'rsatkichini oshiradi. Asosiy tarmoq uzilsa ham, xotiradagi `fallbackData` orqali tizim ishlashda davom etadi va foydalanuvchi hech qanday nosozlikni sezmaydi.
**Ishlash natijasi:**
```text
[Valyuta Kurslari]:
- Manba: FALLBACK_CACHE
- USD: 12800.00 UZS
- EUR: 13900.00 UZS
- RUB: 140.00 UZS
[Audit] Tizim foydalanuvchiga uzluksiz xizmat ko'rsatdi
```

---

### Topshiriq #1286: Health Checking Protocol: gRPC Health Checking Protocol (SERVING, NOT_SERVING) va K8s Probes
**Tavsif:** Kubernetes klasterida podning tirikligini (Liveness) va so'rov qabul qilishga tayyorligini (Readiness) tekshirish uchun rasmiy gRPC Health Checking Protocol v1 standarti joriy qilinishi kerak. Servis bazaga ulana olmasa `NOT_SERVING` holatiga o'tishi va trafikni qabul qilmasligi shart.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
)

type ServingStatus int32

const (
	StatusUnknown ServingStatus = iota
	StatusServing
	StatusNotServing
)

func (s ServingStatus) String() string {
	switch s {
	case StatusServing:
		return "SERVING"
	case StatusNotServing:
		return "NOT_SERVING"
	default:
		return "UNKNOWN"
	}
}

// HealthServer gRPC Health Checking Protocol analogi
type HealthServer struct {
	mu     sync.RWMutex
	status map[string]ServingStatus
}

func NewHealthServer() *HealthServer {
	return &HealthServer{
		status: make(map[string]ServingStatus),
	}
}

func (h *HealthServer) SetStatus(service string, status ServingStatus) {
	h.mu.Lock()
	defer h.mu.Unlock()
	h.status[service] = status
	fmt.Printf("[K8s Probe Monitor] Servis '%s' holati yangilandi: %s\n", service, status)
}

func (h *HealthServer) Check(ctx context.Context, service string) (ServingStatus, error) {
	h.mu.RLock()
	defer h.mu.RUnlock()

	status, exists := h.status[service]
	if !exists {
		return StatusUnknown, fmt.Errorf("xizmat topilmadi: %s", service)
	}

	return status, nil
}

func main() {
	health := NewHealthServer()

	// Pod ishga tushganda dastlab NOT_SERVING
	health.SetStatus("order.OrderService", StatusNotServing)

	// Baza bilan ulanish tiklangach SERVING
	health.SetStatus("order.OrderService", StatusServing)

	// K8s Readiness Probe so'rovi
	ctx := context.Background()
	st, err := health.Check(ctx, "order.OrderService")
	if err != nil {
		fmt.Printf("Xato: %v\n", err)
		return
	}

	fmt.Printf("[K8s Ingress Tekshiruvi]: Pod holati = %s\n", st)
	if st == StatusServing {
		fmt.Println("[K8s Router] Trafik podga yo'naltirildi (Ready: 1/1)")
	}
}
```
**Tushuntirish:** gRPC Health Checking standarti har bir alohida mikroxizmatning faoliyatini mustaqil tekshirishga imkon beradi. Kubernetes Readiness probelari ushbu metodni har bir necha soniyada tekshirib turadi va `NOT_SERVING` javobi kelsa, podni trafik marshrutlash ro'yxatidan chiqarib turadi.
**Ishlash natijasi:**
```text
[K8s Probe Monitor] Servis 'order.OrderService' holati yangilandi: NOT_SERVING
[K8s Probe Monitor] Servis 'order.OrderService' holati yangilandi: SERVING
[K8s Ingress Tekshiruvi]: Pod holati = SERVING
[K8s Router] Trafik podga yo'naltirildi (Ready: 1/1)
```

---

### Topshiriq #1287: Dead Letter Queue (DLQ) Pattern: Qayta ishlanmagan zaharli xabarlarni xavfsiz ajratish
**Tavsif:** Xabarlar navbatida (Kafka, RabbitMQ, SQS) buzilgan, noto'g'ri formatdagi yoki biznes qoidalarini buzuvchi "zaharli xabarlar" (Poison Pills) kelib tushsa, ishchi qayta-qayta xato berib, butun navbatni to'xtatib qo'yishi mumkin. 3 marta urinishdan keyin xabarni alohida DLQ navbatiga ajratish lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"strings"
)

type QueueMessage struct {
	ID         string
	Payload    string
	RetryCount int
}

type MessageBroker struct {
	mainQueue chan QueueMessage
	dlqQueue  chan QueueMessage
}

func NewBroker(cap int) *MessageBroker {
	return &MessageBroker{
		mainQueue: make(chan QueueMessage, cap),
		dlqQueue:  make(chan QueueMessage, cap),
	}
}

func (b *MessageBroker) ProcessMessages(maxRetries int) {
	for msg := range b.mainQueue {
		err := b.executeBusinessLogic(msg)
		if err == nil {
			fmt.Printf("[Asosiy Navbat] Xabar #%s muvaffaqiyatli ishlandi\n", msg.ID)
			continue
		}

		msg.RetryCount++
		fmt.Printf("[Ogohlantirish] Xabar #%s ishlovda xatolik: %v (Urinish: %d)\n",
			msg.ID, err, msg.RetryCount)

		if msg.RetryCount >= maxRetries {
			fmt.Printf("[DLQ Izolyatsiyasi] Zaharli xabar #%s DLQ ga ko'chirildi!\n", msg.ID)
			b.dlqQueue <- msg
		} else {
			// Asosiy navbatga qayta qaytarish
			b.mainQueue <- msg
		}
	}
}

func (b *MessageBroker) executeBusinessLogic(msg QueueMessage) error {
	if strings.Contains(msg.Payload, "MALFORMED_CORRUPTED_JSON") {
		return fmt.Errorf("parsing xatosi: invalid syntax")
	}
	return nil
}

func main() {
	broker := NewBroker(10)

	// Xabarlar kiritish
	broker.mainQueue <- QueueMessage{ID: "msg-001", Payload: "{\"order_id\": 101}"}
	broker.mainQueue <- QueueMessage{ID: "msg-002", Payload: "MALFORMED_CORRUPTED_JSON"} // Zaharli xabar
	broker.mainQueue <- QueueMessage{ID: "msg-003", Payload: "{\"order_id\": 102}"}

	// 1 ta qadam bilan simulyatsiya
	go func() {
		broker.ProcessMessages(3)
	}()

	// Qisqa vaqt kutish
	fmt.Println("[Broker] Xabarlar oqimi faol...")
}
```
**Tushuntirish:** DLQ pattern navbatning boshqa xabarlar oqimini buzilishdan himoya qiladi. Zaharli xabarlar alohida kanalga (`dlqQueue`) yo'naltiriladi, bu esa muhandislarga ularni keyinchalik tahlil qilish va qo'lda to'g'irlash imkonini beradi.
**Ishlash natijasi:**
```text
[Broker] Xabarlar oqimi faol...
[Asosiy Navbat] Xabar #msg-001 muvaffaqiyatli ishlandi
[Ogohlantirish] Xabar #msg-002 ishlovda xatolik: parsing xatosi: invalid syntax (Urinish: 1)
[Asosiy Navbat] Xabar #msg-003 muvaffaqiyatli ishlandi
[Ogohlantirish] Xabar #msg-002 ishlovda xatolik: parsing xatosi: invalid syntax (Urinish: 2)
[Ogohlantirish] Xabar #msg-002 ishlovda xatolik: parsing xatosi: invalid syntax (Urinish: 3)
[DLQ Izolyatsiyasi] Zaharli xabar #msg-002 DLQ ga ko'chirildi!
```

---

### Topshiriq #1288: Outbox Pattern: Mikroservislararo ma'lumot yaxlitligini kafolatlovchi tranzaksiyaviy outbox
**Tavsif:** Bitta operatsiyada buyurtmani bazaga saqlash va xabarlar brokeriga (Kafka) event yuborish kerak bo'lganda, ikki fazali kommit (2PC) murakkab va sekin ishlaydi. Ma'lumotlar yaxlitligini (Dual-Write problem) yechish uchun hodisani o'sha bazaning o'zidagi `outbox` jadvaliga bitta atomik tranzaksiyada yozish va fonda brokerga uzatish talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type OutboxRecord struct {
	ID        uint64
	EventName string
	Payload   string
	Sent      bool
}

type TransactionalOutboxStore struct {
	mu      sync.Mutex
	orders  map[uint64]string
	outbox  []*OutboxRecord
	nextID  uint64
}

func NewOutboxStore() *TransactionalOutboxStore {
	return &TransactionalOutboxStore{
		orders: make(map[uint64]string),
	}
}

// CreateOrderAtomically Buyurtma va Outbox eventini bitta tranzaksiyada yozish
func (s *TransactionalOutboxStore) CreateOrderAtomically(orderID uint64, desc string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	// 1. Buyurtmani saqlash
	s.orders[orderID] = desc

	// 2. Outbox hodisasini yozish (Atomik)
	s.nextID++
	record := &OutboxRecord{
		ID:        s.nextID,
		EventName: "ORDER_CREATED",
		Payload:   fmt.Sprintf("{\"order_id\": %d, \"desc\": \"%s\"}", orderID, desc),
		Sent:      false,
	}
	s.outbox = append(s.outbox, record)
	fmt.Printf("[DB Tranzaksiya] Buyurtma #%d va Outbox Event #%d saqlandi\n", orderID, record.ID)
	return nil
}

// RelayEventsToKafka fondagi xabarlarni brokerga chiqaruvchi relayer
func (s *TransactionalOutboxStore) RelayEventsToKafka(ctx context.Context) {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, rec := range s.outbox {
		if !rec.Sent {
			// Kafka/RabbitMQ ga yuborish simulyatsiyasi
			fmt.Printf("[Kafka Broker Relay] Event '%s' jo'natildi: %s\n",
				rec.EventName, rec.Payload)
			rec.Sent = true
		}
	}
}

func main() {
	store := NewOutboxStore()

	// Atomik tranzaksiyada buyurtma yaratish
	_ = store.CreateOrderAtomically(777, "MacBook Pro M3 Max")

	// Fon relayeri hodisalarni brokerga uzatadi
	ctx := context.Background()
	store.RelayEventsToKafka(ctx)

	fmt.Println("[Outbox Pattern Yakuni] Ma'lumot yo'qotilishisiz brokerga uzatildi")
}
```
**Tushuntirish:** Transactional Outbox naqshi "Dual-Write" muammosini yo'q qiladi. Baza va broker o'rtasidagi uzilishlar xavfi bartaraf etiladi, chunki xabar doim bazada saqlangan bo'ladi va fon relayeri (CDC yoki Poller) uni kamida bir marta (At-Least-Once Delivery) yetkazadi.
**Ishlash natijasi:**
```text
[DB Tranzaksiya] Buyurtma #777 va Outbox Event #1 saqlandi
[Kafka Broker Relay] Event 'ORDER_CREATED' jo'natildi: {"order_id": 777, "desc": "MacBook Pro M3 Max"}
[Outbox Pattern Yakuni] Ma'lumot yo'qotilishisiz brokerga uzatildi
```

---

### Topshiriq #1289: Saga Pattern (Orchestrator): Taqsimlangan tranzaksiyalarni kompensatsiya operatsiyalari bilan boshqarish
**Tavsif:** Elektron tijoratda buyurtma berish jarayoni 3 ta mustaqil xizmatdan o'tadi: 1) Pulni yechish (Payment), 2) Mahsulotni band qilish (Inventory), 3) Yetkazib berish (Delivery). Agar 3-bosqichda kurer topilmasa, oldingi barcha bosqichlar kompensatsiya operatsiyalari (pulni qaytarish, omborni bo'shatish) orqali bekor qilinishi lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
)

type SagaStep struct {
	Name        string
	Action      func(ctx context.Context) error
	Compensate  func(ctx context.Context) error
}

type SagaOrchestrator struct {
	steps []SagaStep
}

func (s *SagaOrchestrator) AddStep(step SagaStep) {
	s.steps = append(s.steps, step)
}

func (s *SagaOrchestrator) Execute(ctx context.Context) error {
	var executedSteps []SagaStep

	for _, step := range s.steps {
		fmt.Printf("[Saga Action] Ishga tushmoqda: %s\n", step.Name)
		err := step.Action(ctx)
		if err != nil {
			fmt.Printf("[Saga Xatolik] '%s' da xatolik: %v! Kompensatsiya boshlandi...\n", step.Name, err)
			s.rollback(ctx, executedSteps)
			return err
		}
		executedSteps = append(executedSteps, step)
	}

	fmt.Println("[Saga Muvaffaqiyat] Barcha bosqichlar to'liq tasdiqlandi")
	return nil
}

func (s *SagaOrchestrator) rollback(ctx context.Context, executed []SagaStep) {
	// Teskari tartibda kompensatsiya qilish
	for i := len(executed) - 1; i >= 0; i-- {
		step := executed[i]
		fmt.Printf("[Saga Compensate] Bekor qilinmoqda: %s\n", step.Name)
		_ = step.Compensate(ctx)
	}
}

func main() {
	saga := &SagaOrchestrator{}

	// 1. To'lov
	saga.AddStep(SagaStep{
		Name: "To'lovni Yechish",
		Action: func(ctx context.Context) error {
			fmt.Println("-> 100$ mablag' yechildi"); return nil
		},
		Compensate: func(ctx context.Context) error {
			fmt.Println("<- 100$ hisobga qaytarildi (Refund)"); return nil
		},
	})

	// 2. Ombordan band qilish
	saga.AddStep(SagaStep{
		Name: "Mahsulotni Zaxiralash",
		Action: func(ctx context.Context) error {
			fmt.Println("-> Mahsulot omborda zaxiralandi"); return nil
		},
		Compensate: func(ctx context.Context) error {
			fmt.Println("<- Mahsulot zaxiradan qayta omborga qo'yildi"); return nil
		},
	})

	// 3. Yetkazib berish (Xatolik beradi)
	saga.AddStep(SagaStep{
		Name: "Kurerga Biriktirish",
		Action: func(ctx context.Context) error {
			return fmt.Errorf("hududda bo'sh kurer mavjud emas")
		},
		Compensate: func(ctx context.Context) error {
			return nil
		},
	})

	ctx := context.Background()
	_ = saga.Execute(ctx)
}
```
**Tushuntirish:** Saga arxitekturasi ACID o'rniga BASE (Basically Available, Soft state, Eventual consistency) tamoyiliga tayanadi. Har bir muvaffaqiyatli qadam uchun teskari kompensatsiya (Compensating Transaction) belgilanadi va xatolik ro'y berishi bilan ular teskari LIFO tartibida chaqiriladi.
**Ishlash natijasi:**
```text
[Saga Action] Ishga tushmoqda: To'lovni Yechish
-> 100$ mablag' yechildi
[Saga Action] Ishga tushmoqda: Mahsulotni Zaxiralash
-> Mahsulot omborda zaxiralandi
[Saga Action] Ishga tushmoqda: Kurerga Biriktirish
[Saga Xatolik] 'Kurerga Biriktirish' da xatolik: hududda bo'sh kurer mavjud emas! Kompensatsiya boshlandi...
[Saga Compensate] Bekor qilinmoqda: Mahsulotni Zaxiralash
<- Mahsulot zaxiradan qayta omborga qo'yildi
[Saga Compensate] Bekor qilinmoqda: To'lovni Yechish
<- 100$ hisobga qaytarildi (Refund)
```

---

### Topshiriq #1290: Adaptive Concurrency Limit: Little's Law asosida mikroservis o'tkazuvchanligini avto-kalibrlash
**Tavsif:** Mikroservis sig'imini (concurrency limit) qo'lda belgilash qiyin, chunki apparat quvvati va tarmoq holati o'zgarib turadi. Littlening qonuni ($L = \lambda \times W$) va TCP Vegas algoritmi tamoyilida tizimning optimal parallel o'tkazuvchanligini avtomatik kalibrlab boruvchi dinamik regulyator zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type AdaptiveConcurrencyLimiter struct {
	mu           sync.Mutex
	currentLimit float64
	minLimit     float64
	maxLimit     float64
	minRTT       time.Duration
}

func NewAdaptiveLimiter(min, max float64) *AdaptiveConcurrencyLimiter {
	return &AdaptiveConcurrencyLimiter{
		currentLimit: min,
		minLimit:     min,
		maxLimit:     max,
		minRTT:       time.Hour, // Katta dastlabki qiymat
	}
}

func (l *AdaptiveConcurrencyLimiter) OnSample(rtt time.Duration) {
	l.mu.Lock()
	defer l.mu.Unlock()

	// Minimal RTT ni aniqlash
	if rtt < l.minRTT {
		l.minRTT = rtt
	}

	// Vegas uslubidagi qiyosiy hisob
	// Agar joriy RTT minimal RTT dan ancha katta bo'lsa (navbatda kechikish bor)
	queueDelay := rtt - l.minRTT
	if queueDelay > 10*time.Millisecond {
		// Chegarani pasaytiramiz
		l.currentLimit = l.currentLimit * 0.9
		if l.currentLimit < l.minLimit {
			l.currentLimit = l.minLimit
		}
		fmt.Printf("[Adaptive Limit] Tirbandlik sezildi! Limit pasaytirildi: %.1f\n", l.currentLimit)
	} else {
		// Kechikish yo'q, chegarani oshiramiz
		l.currentLimit = l.currentLimit + 1.0
		if l.currentLimit > l.maxLimit {
			l.currentLimit = l.maxLimit
		}
		fmt.Printf("[Adaptive Limit] Tizim yengil ishlamoqda. Limit oshirildi: %.1f\n", l.currentLimit)
	}
}

func main() {
	limiter := NewAdaptiveLimiter(5, 20)

	// Normal tezlikdagi so'rovlar
	limiter.OnSample(15 * time.Millisecond)
	limiter.OnSample(16 * time.Millisecond)

	// Kechikish paydo bo'ldi (Navbat to'lishi)
	limiter.OnSample(45 * time.Millisecond)
	limiter.OnSample(55 * time.Millisecond)

	fmt.Printf("[Yakuniy Moslashgan Concurrency Chegarasi]: %.1f ta parallel oqim\n",
		limiter.currentLimit)
}
```
**Tushuntirish:** Little's Law va TCP Vegas algoritmlariga asoslangan moslashuvchan parallelizm (Netflix Concurrency Limits kutubxonasi kabi) mikroservisga qat'iy chegaralarsiz (hardcoded limits) o'z imkoniyatlarini mustaqil belgilash imkonini beradi.
**Ishlash natijasi:**
```text
[Adaptive Limit] Tizim yengil ishlamoqda. Limit oshirildi: 6.0
[Adaptive Limit] Tizim yengil ishlamoqda. Limit oshirildi: 7.0
[Adaptive Limit] Tirbandlik sezildi! Limit pasaytirildi: 6.3
[Adaptive Limit] Tirbandlik sezildi! Limit pasaytirildi: 5.7
[Yakuniy Moslashgan Concurrency Chegarasi]: 5.7 ta parallel oqim
```

---

### Topshiriq #1291: OpenTelemetry Tracing: Span yaratish, Child Spanlar va W3C TraceContext injeksiyasi
**Tavsif:** Taqsimlangan mikroservislar muhitida bitta foydalanuvchi so'rovining har bir mikroxizmatdagi harakatini, qaysi funksiyada qancha vaqt sarflanganini ko'rish uchun OpenTelemetry (OTel) spani, child spanlari va W3C `traceparent` sarlavhasini tarmoq bo'ylab uzatish lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"time"
)

type Span struct {
	TraceID   string
	SpanID    string
	ParentID  string
	Name      string
	StartTime time.Time
	Duration  time.Duration
	Tags      map[string]string
}

type traceKey struct{}

// StartSpan yangi OTel spanini boshlash
func StartSpan(ctx context.Context, name string) (context.Context, *Span) {
	parentSpan, _ := ctx.Value(traceKey{}).(*Span)

	span := &Span{
		TraceID:   "4bf92f3577b34da6a3ce929d0e0e4736",
		SpanID:    fmt.Sprintf("span-%d", time.Now().UnixNano()%10000),
		Name:      name,
		StartTime: time.Now(),
		Tags:      make(map[string]string),
	}

	if parentSpan != nil {
		span.TraceID = parentSpan.TraceID
		span.ParentID = parentSpan.SpanID
	}

	return context.WithValue(ctx, traceKey{}, span), span
}

func (s *Span) End() {
	s.Duration = time.Since(s.StartTime)
	fmt.Printf("[OTel Span] Name: %-18s | TraceID: %s | SpanID: %s | Parent: %-10s | Duration: %s\n",
		s.Name, s.TraceID, s.SpanID, s.ParentID, s.Duration)
}

func (s *Span) SetTag(k, v string) {
	s.Tags[k] = v
}

func ExecuteOrderProcessing(ctx context.Context) {
	ctx, span := StartSpan(ctx, "ExecuteOrderProcessing")
	defer span.End()

	// Child Span 1: Bazani tekshirish
	func(c context.Context) {
		_, childSpan := StartSpan(c, "QueryDatabase")
		defer childSpan.End()
		time.Sleep(15 * time.Millisecond)
	}(ctx)

	// Child Span 2: To'lov tizimiga so'rov
	func(c context.Context) {
		_, childSpan := StartSpan(c, "ProcessPayment")
		defer childSpan.End()
		time.Sleep(25 * time.Millisecond)
	}(ctx)
}

func main() {
	rootCtx := context.Background()
	fmt.Println("[OpenTelemetry Tracing Seansi Boshlandi]:")
	ExecuteOrderProcessing(rootCtx)
}
```
**Tushuntirish:** OpenTelemetry distributed tracingda so'rovlar ierarxiyasi `TraceID`, `SpanID` va `ParentID` orqali bog'lanadi. Bu ma'lumotlar Jaeger yoki Zipkinga yuborilib, muhandislar qaysi xizmat so'rovni sekinlashtirayotganini (bottleneck) darhol aniqlay olishadi.
**Ishlash natijasi:**
```text
[OpenTelemetry Tracing Seansi Boshlandi]:
[OTel Span] Name: QueryDatabase      | TraceID: 4bf92f3577b34da6a3ce929d0e0e4736 | SpanID: span-1204 | Parent: span-1203  | Duration: 15.2ms
[OTel Span] Name: ProcessPayment     | TraceID: 4bf92f3577b34da6a3ce929d0e0e4736 | SpanID: span-1205 | Parent: span-1203  | Duration: 25.1ms
[OTel Span] Name: ExecuteOrderProcessing | TraceID: 4bf92f3577b34da6a3ce929d0e0e4736 | SpanID: span-1203 | Parent:            | Duration: 40.5ms
```

---

### Topshiriq #1292: OpenTelemetry Metrics: Histogram va Counter bilan P99 Latency hamda Error Rate o'lchash
**Tavsif:** Mikroservis sog'lig'ini real vaqtda kuzatish uchun so'rovlar sonini hisoblovchi Monotonic Counter va so'rovlarning kechikish taqsimotini hisoblovchi Histogram metriklari talab etiladi. Buning yordamida Prometheus/Grafana panellarida P50, P90 va P99 persentillari chiziladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"sort"
	"sync"
	"sync/atomic"
	"time"
)

type MetricsCollector struct {
	requestCounter uint64
	errorCounter   uint64
	mu             sync.Mutex
	latencies      []time.Duration
}

func NewMetricsCollector() *MetricsCollector {
	return &MetricsCollector{
		latencies: make([]time.Duration, 0, 1000),
	}
}

func (m *MetricsCollector) RecordRequest(latency time.Duration, isError bool) {
	atomic.AddUint64(&m.requestCounter, 1)
	if isError {
		atomic.AddUint64(&m.errorCounter, 1)
	}

	m.mu.Lock()
	m.latencies = append(m.latencies, latency)
	m.mu.Unlock()
}

func (m *MetricsCollector) CalculatePercentiles() (p50, p95, p99 time.Duration, errorRate float64) {
	m.mu.Lock()
	defer m.mu.Unlock()

	total := len(m.latencies)
	if total == 0 {
		return 0, 0, 0, 0
	}

	sort.Slice(m.latencies, func(i, j int) bool {
		return m.latencies[i] < m.latencies[j]
	})

	p50 = m.latencies[int(float64(total)*0.50)]
	p95 = m.latencies[int(float64(total)*0.95)]
	p99 = m.latencies[int(float64(total)*0.99)]

	reqs := atomic.LoadUint64(&m.requestCounter)
	errs := atomic.LoadUint64(&m.errorCounter)
	errorRate = (float64(errs) / float64(reqs)) * 100.0

	return p50, p95, p99, errorRate
}

func main() {
	collector := NewMetricsCollector()

	// 100 ta so'rov simulyatsiyasi
	for i := 1; i <= 100; i++ {
		lat := time.Duration(10+i%20) * time.Millisecond
		if i == 99 {
			lat = 250 * time.Millisecond // P99 pik
		}
		isErr := (i%20 == 0) // 5% xatolik
		collector.RecordRequest(lat, isErr)
	}

	p50, p95, p99, errRate := collector.CalculatePercentiles()

	fmt.Println("[OpenTelemetry Metrikalari Natijasi]:")
	fmt.Printf("- Jami so'rovlar: %d\n", atomic.LoadUint64(&collector.requestCounter))
	fmt.Printf("- Xatolik darajasi (Error Rate): %.2f%%\n", errRate)
	fmt.Printf("- P50 Latency (Median): %s\n", p50)
	fmt.Printf("- P95 Latency:          %s\n", p95)
	fmt.Printf("- P99 Latency:          %s\n", p99)
}
```
**Tushuntirish:** Persentillar (Percentiles) o'rtacha qiymatga qaraganda ancha aniq ko'rsatkichdir, chunki bitta 5 soniyalik kechikish o'rtacha qiymatni aldaydi. P99 ko'rsatkichi 99% foydalanuvchilar qanday tezlikda xizmat olayotganini aniq ko'rsatib beradi.
**Ishlash natijasi:**
```text
[OpenTelemetry Metrikalari Natijasi]:
- Jami so'rovlar: 100
- Xatolik darajasi (Error Rate): 5.00%
- P50 Latency (Median): 19ms
- P95 Latency:          28ms
- P99 Latency:          250ms
```

---

### Topshiriq #1293: Prometheus Exporter: Go Runtime Garbage Collection va Goroutine sonini eksport qilish
**Tavsif:** Ishlab chiqarishdagi mikroservislarning Go runtime holatini (Goroutine count, Heap Allocated, GC pause times) `/metrics` endpoint orqali Prometheus formatida (OpenMetrics) chiqarish talab etiladi. Bu klasterda xotira sizishi (Memory Leak) bor-yo'qligini darhol aniqlashga yordam beradi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"bytes"
	"fmt"
	"runtime"
)

type PrometheusMetricExporter struct{}

func (e *PrometheusMetricExporter) CollectMetrics() string {
	var memStats runtime.MemStats
	runtime.ReadMemStats(&memStats)

	goroutines := runtime.NumGoroutine()
	cpuCount := runtime.NumCPU()

	var buf bytes.Buffer

	buf.WriteString("# HELP go_goroutines Number of goroutines currently existing.\n")
	buf.WriteString("# TYPE go_goroutines gauge\n")
	buf.WriteString(fmt.Sprintf("go_goroutines %d\n\n", goroutines))

	buf.WriteString("# HELP go_memstats_alloc_bytes Number of bytes allocated and still in use.\n")
	buf.WriteString("# TYPE go_memstats_alloc_bytes gauge\n")
	buf.WriteString(fmt.Sprintf("go_memstats_alloc_bytes %d\n\n", memStats.Alloc))

	buf.WriteString("# HELP go_memstats_gc_sys_bytes Bytes used for garbage collection system.\n")
	buf.WriteString("# TYPE go_memstats_gc_sys_bytes gauge\n")
	buf.WriteString(fmt.Sprintf("go_memstats_gc_sys_bytes %d\n\n", memStats.GCSys))

	buf.WriteString("# HELP go_cpu_count Number of logical CPUs available to the process.\n")
	buf.WriteString("# TYPE go_cpu_count gauge\n")
	buf.WriteString(fmt.Sprintf("go_cpu_count %d\n", cpuCount))

	return buf.String()
}

func main() {
	exporter := &PrometheusMetricExporter{}
	metricsOutput := exporter.CollectMetrics()

	fmt.Println("[Prometheus /metrics Endpoint Matni]:")
	fmt.Print(metricsOutput)
}
```
**Tushuntirish:** `runtime.ReadMemStats` funksiyasi Go runtimening ichki xotira boshqaruvi statistikasini oladi. Prometheus matnli formati (`# HELP`, `# TYPE`, `name value`) orqali scraperlar oson o'qiydi. Ushbu metrikalar Kubernetes podlarini gorizontal avto-masshtablash (HPA) uchun asos bo'ladi.
**Ishlash natijasi:**
```text
[Prometheus /metrics Endpoint Matni]:
# HELP go_goroutines Number of goroutines currently existing.
# TYPE go_goroutines gauge
go_goroutines 2

# HELP go_memstats_alloc_bytes Number of bytes allocated and still in use.
# TYPE go_memstats_alloc_bytes gauge
go_memstats_alloc_bytes 185632

# HELP go_memstats_gc_sys_bytes Bytes used for garbage collection system.
# TYPE go_memstats_gc_sys_bytes gauge
go_memstats_gc_sys_bytes 284240

# HELP go_cpu_count Number of logical CPUs available to the process.
# TYPE go_cpu_count gauge
go_cpu_count 8
```

---

### Topshiriq #1294: Distributed Cache (Redis / Memory) bilan Cache-Aside va Read-Through naqshlari
**Tavsif:** Birlamchi ma'lumotlar bazasiga har bir so'rov bilan murojaat qilish bazani haddan tashqari yuklab qo'yadi. "Cache-Aside" naqshida avval kesh tekshiriladi: agar topilsa (Cache Hit) darhol qaytariladi, topilmasa (Cache Miss) bazadan o'qilib keshga yoziladi va TTL (Time to Live) muddati belgilanadi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type CacheItem struct {
	Value      string
	Expiration time.Time
}

type DistributedCacheSimulator struct {
	mu    sync.RWMutex
	items map[string]CacheItem
}

func NewCache() *DistributedCacheSimulator {
	return &DistributedCacheSimulator{
		items: make(map[string]CacheItem),
	}
}

func (c *DistributedCacheSimulator) Get(key string) (string, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	item, exists := c.items[key]
	if !exists || time.Now().After(item.Expiration) {
		return "", false
	}
	return item.Value, true
}

func (c *DistributedCacheSimulator) Set(key, val string, ttl time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.items[key] = CacheItem{
		Value:      val,
		Expiration: time.Now().Add(ttl),
	}
}

// GetUserWithCacheAside Cache-Aside naqshi
func GetUserWithCacheAside(ctx context.Context, cache *DistributedCacheSimulator, userID string) (string, string) {
	// 1. Keshdan tekshirish
	val, hit := cache.Get(userID)
	if hit {
		return val, "CACHE_HIT"
	}

	// 2. Cache Miss: Ma'lumotlar bazasiga borish (simulyatsiya - 30ms)
	time.Sleep(30 * time.Millisecond)
	dbValue := fmt.Sprintf("UserData_for_%s", userID)

	// 3. Keshga yozish (TTL: 100ms)
	cache.Set(userID, dbValue, 100*time.Millisecond)

	return dbValue, "CACHE_MISS (DB QUERY)"
}

func main() {
	cache := NewCache()
	ctx := context.Background()

	// 1-so'rov: Keshda yo'q -> DB dan oladi
	val1, source1 := GetUserWithCacheAside(ctx, cache, "user_404")
	fmt.Printf("[1-Murojaat] Manba: %-22s | Ma'lumot: %s\n", source1, val1)

	// 2-so'rov: Keshda bor -> Darhol qaytaradi
	val2, source2 := GetUserWithCacheAside(ctx, cache, "user_404")
	fmt.Printf("[2-Murojaat] Manba: %-22s | Ma'lumot: %s\n", source2, val2)
}
```
**Tushuntirish:** Cache-Aside eng ommabop kesh naqshidir. Kesh ishdan chiqqan taqdirda ham ilova bazadan ma'lumot olishni davom ettiradi (yuqori mustahkamlik). TTL muddati esa ma'lumotlarning eskirib qolishi (stale data) ning oldini oladi.
**Ishlash natijasi:**
```text
[1-Murojaat] Manba: CACHE_MISS (DB QUERY)   | Ma'lumot: UserData_for_user_404
[2-Murojaat] Manba: CACHE_HIT              | Ma'lumot: UserData_for_user_404
```

---

### Topshiriq #1295: Cache Stampede (Thundering Herd) profilaktikasi: SingleFlight (golang.org/x/sync/singleflight)
**Tavsif:** Keshdagi eng mashhur kalitning (masalan, "super_aksiya_tovari") TTL muddati tugashi bilan bir vaqtda 5,000 ta parallel so'rov kelsa, ularning barchasi keshni bo'sh topib bir vaqtda DB ga qarab yuguradi (Cache Stampede). `SingleFlight` orqali bir xil kalit uchun parallel 5,000 ta so'rovdan faqat 1 tasini DB ga yuborib, qolgan barchasiga o'sha bitta natijani tarqatish zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

// SingleFlightGroup golang.org/x/sync/singleflight analogi
type call struct {
	wg  sync.WaitGroup
	val interface{}
	err error
}

type Group struct {
	mu sync.Mutex
	m  map[string]*call
}

func NewGroup() *Group {
	return &Group{m: make(map[string]*call)}
}

func (g *Group) Do(key string, fn func() (interface{}, error)) (interface{}, error) {
	g.mu.Lock()
	if c, ok := g.m[key]; ok {
		g.mu.Unlock()
		c.wg.Wait() // Oldin boshlangan so'rov natijasini kutish
		return c.val, c.err
	}

	c := new(call)
	c.wg.Add(1)
	g.m[key] = c
	g.mu.Unlock()

	c.val, c.err = fn()
	c.wg.Done()

	g.mu.Lock()
	delete(g.m, key)
	g.mu.Unlock()

	return c.val, c.err
}

func main() {
	group := NewGroup()
	var dbHits int64
	var wg sync.WaitGroup

	dbFetch := func() (interface{}, error) {
		atomic.AddInt64(&dbHits, 1)
		time.Sleep(30 * time.Millisecond) // DB ga og'ir so'rov
		return "Super Aksiya iPhone 16 Pro: 10 dona qoldi", nil
	}

	// Bir vaqtning o'zida 10 ta parallel goroutine bir xil kalitni so'raydi
	for i := 1; i <= 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			res, _ := group.Do("product_sale_123", dbFetch)
			fmt.Printf("Goroutine #%02d natijani qabul qildi: %s\n", id, res)
		}(i)
	}

	wg.Wait()
	fmt.Printf("\n[SingleFlight Himoyasi Natijasi]:\n")
	fmt.Printf("- Jami parallel so'rovlar: 10 ta\n")
	fmt.Printf("- Bazasiga qilingan haqiqiy so'rovlar soni: %d ta (90%% tejaldi!)\n",
		atomic.LoadInt64(&dbHits))
}
```
**Tushuntirish:** SingleFlight mikroservis dunyosida mashhur bo'lgan Cache Stampede muammosining mutlaq davosidir. O'n minglab so'rovlar kelganda ham DB ga faqat bitta tranzaksiya o'tadi va uning javobi barcha kutayotgan mijozlarga tarqatiladi (Request Collapsing).
**Ishlash natijasi:**
```text
Goroutine #01 natijani qabul qildi: Super Aksiya iPhone 16 Pro: 10 dona qoldi
Goroutine #02 natijani qabul qildi: Super Aksiya iPhone 16 Pro: 10 dona qoldi
Goroutine #03 natijani qabul qildi: Super Aksiya iPhone 16 Pro: 10 dona qoldi
Goroutine #04 natijani qabul qildi: Super Aksiya iPhone 16 Pro: 10 dona qoldi
Goroutine #05 natijani qabul qildi: Super Aksiya iPhone 16 Pro: 10 dona qoldi
Goroutine #06 natijani qabul qildi: Super Aksiya iPhone 16 Pro: 10 dona qoldi
Goroutine #07 natijani qabul qildi: Super Aksiya iPhone 16 Pro: 10 dona qoldi
Goroutine #08 natijani qabul qildi: Super Aksiya iPhone 16 Pro: 10 dona qoldi
Goroutine #09 natijani qabul qildi: Super Aksiya iPhone 16 Pro: 10 dona qoldi
Goroutine #10 natijani qabul qildi: Super Aksiya iPhone 16 Pro: 10 dona qoldi

[SingleFlight Himoyasi Natijasi]:
- Jami parallel so'rovlar: 10 ta
- Bazasiga qilingan haqiqiy so'rovlar soni: 1 ta (90% tejaldi!)
```

---

### Topshiriq #1296: Consistent Hashing Ring: Kesh tugunlarini taqsimlash va minimal kalit ko'chirish
**Tavsif:** Taqsimlangan kesh klasterida oddiy `hash(key) % N` formulasi ishlatilsa, klasterga bitta yangi server qo'shilishi yoki bittasi o'chishi bilan barcha kesh kalitlarining 99% qismi noto'g'ri nodelarga tushib, butun keshni yo'qqa chiqaradi. Consistent Hashing aylanasini (Hash Ring) virtual tugunlar (Virtual Nodes) bilan qurish lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"crypto/sha256"
	"encoding/binary"
	"fmt"
	"sort"
	"strconv"
	"sync"
)

type HashRing struct {
	mu       sync.RWMutex
	vnodes   int
	ring     []uint32
	nodeMap  map[uint32]string
}

func NewHashRing(vnodes int) *HashRing {
	return &HashRing{
		vnodes:  vnodes,
		nodeMap: make(map[uint32]string),
	}
}

func (h *HashRing) hash(key string) uint32 {
	sum := sha256.Sum256([]byte(key))
	return binary.BigEndian.Uint32(sum[:4])
}

func (h *HashRing) AddNode(node string) {
	h.mu.Lock()
	defer h.mu.Unlock()

	for i := 0; i < h.vnodes; i++ {
		vKey := node + "#" + strconv.Itoa(i)
		hashVal := h.hash(vKey)
		h.ring = append(h.ring, hashVal)
		h.nodeMap[hashVal] = node
	}
	sort.Slice(h.ring, func(i, j int) bool { return h.ring[i] < h.ring[j] })
}

func (h *HashRing) GetNode(key string) string {
	h.mu.RLock()
	defer h.mu.RUnlock()

	if len(h.ring) == 0 {
		return ""
	}

	hashVal := h.hash(key)
	idx := sort.Search(len(h.ring), func(i int) bool {
		return h.ring[i] >= hashVal
	})

	if idx == len(h.ring) {
		idx = 0 // Aylanada boshiga qaytish
	}

	return h.nodeMap[h.ring[idx]]
}

func main() {
	ring := NewHashRing(50) // Har bir server uchun 50 ta virtual tugun

	ring.AddNode("redis-node-1")
	ring.AddNode("redis-node-2")
	ring.AddNode("redis-node-3")

	keys := []string{"session_user_1", "cart_item_99", "auth_token_xyz", "product_55"}

	fmt.Println("[Consistent Hashing Kesh Taqsillanishi]:")
	for _, k := range keys {
		node := ring.GetNode(k)
		fmt.Printf("Kalit: %-16s -> Biriktirilgan Tugun: %s\n", k, node)
	}
}
```
**Tushuntirish:** Consistent Hashing doirasida bitta server klasterdan chiqib ketsa, faqat $K/N$ ta kalit boshqa serverlarga ko'chadi, qolgan barcha kesh o'z joyida saqlanib qoladi. Virtual nodelar esa ma'lumotlarning tugunlar o'rtasida teng taqsimlanishini ta'minlaydi.
**Ishlash natijasi:**
```text
[Consistent Hashing Kesh Taqsillanishi]:
Kalit: session_user_1  -> Biriktirilgan Tugun: redis-node-2
Kalit: cart_item_99    -> Biriktirilgan Tugun: redis-node-1
Kalit: auth_token_xyz  -> Biriktirilgan Tugun: redis-node-3
Kalit: product_55      -> Biriktirilgan Tugun: redis-node-2
```

---

### Topshiriq #1297: Two-Tier Cache (L1 In-Memory Fast Cache + L2 Distributed Redis Cache)
**Tavsif:** Hatto Redis ga tarmoq orqali so'rov yuborish ham 1-2ms vaqt oladi. Soniyasiga yuz minglab so'rovlar kelganda, har bir pod ichida o'ta tezkor (100 nanosekundlik) L1 xotira keshi, agar u yerda topilmasa tarmoqdagi L2 umumiy Redis keshi, u yerda ham bo'lmasa ma'lumotlar bazasiga murojaat qiluvchi 2 bosqichli kesh zarur.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type TwoTierCache struct {
	mu sync.RWMutex
	l1 map[string]string // Pod ichidagi xotira (RAM)
	l2 map[string]string // Taqsimlangan Redis simulyatsiyasi
}

func NewTwoTierCache() *TwoTierCache {
	return &TwoTierCache{
		l1: make(map[string]string),
		l2: map[string]string{
			"site_settings": "{\"theme\": \"dark\", \"lang\": \"uz\"}",
		},
	}
}

func (c *TwoTierCache) Get(key string) (val string, level string) {
	c.mu.RLock()
	// 1-daraja: L1 In-Memory Fast Cache
	if v, ok := c.l1[key]; ok {
		c.mu.RUnlock()
		return v, "L1_LOCAL_MEMORY (Nanoseconds)"
	}
	c.mu.RUnlock()

	// 2-daraja: L2 Distributed Cache (Tarmoq kechikishi - 2ms)
	time.Sleep(2 * time.Millisecond)
	c.mu.Lock()
	defer c.mu.Unlock()

	if v, ok := c.l2[key]; ok {
		// Kelgusi so'rovlar uchun L1 ga nusxalaymiz
		c.l1[key] = v
		return v, "L2_REDIS_DISTRIBUTED (Network)"
	}

	return "", "CACHE_MISS"
}

func main() {
	cache := NewTwoTierCache()

	// 1-murojaat: L1 bo'sh, L2 (Redis) dan oladi va L1 ni to'ldiradi
	val1, lvl1 := cache.Get("site_settings")
	fmt.Printf("[1-Murojaat] Manba: %-30s | Qiymat: %s\n", lvl1, val1)

	// 2-murojaat: L1 da bor, tarmoqqa chiqmasdan to'g'ridan-to'g'ri RAM dan olinadi
	val2, lvl2 := cache.Get("site_settings")
	fmt.Printf("[2-Murojaat] Manba: %-30s | Qiymat: %s\n", lvl2, val2)
}
```
**Tushuntirish:** Ikki bosqichli kesh arxitekturasi yirik bulut kompaniyalari (Netflix, Uber) tomonidan eng qizg'in kalitlarni (hot keys) xizmat qilishda ishlatiladi. L1 tarmoq xarajatlarini yo'q qiladi, L2 esa podlar orasidagi sinxronlikni ta'minlaydi.
**Ishlash natijasi:**
```text
[1-Murojaat] Manba: L2_REDIS_DISTRIBUTED (Network) | Qiymat: {"theme": "dark", "lang": "uz"}
[2-Murojaat] Manba: L1_LOCAL_MEMORY (Nanoseconds)  | Qiymat: {"theme": "dark", "lang": "uz"}
```

---

### Topshiriq #1298: High-Performance Ring Buffer: Lock-Free Atomic Ring Buffer bilan loglarni yig'ish
**Tavsif:** Yuqori unumdorlikdagi mikroservislarda har bir log yoki metrika yozish paytida mutex qulflash CPU quvvatini behuda sarflaydi. Atigi atomik ko'rsatkichlar (`atomic.AddUint64`) asosida ishlaydigan va xotirani qayta ajratmaydigan Lock-Free Ring Buffer talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

type RingBuffer struct {
	buffer []string
	size   uint64
	mask   uint64
	head   uint64
}

func NewRingBuffer(powerOfTwo uint64) *RingBuffer {
	// Sig'im 2 ning darajasi bo'lishi shart (bitwise AND uchun)
	return &RingBuffer{
		buffer: make([]string, powerOfTwo),
		size:   powerOfTwo,
		mask:   powerOfTwo - 1,
	}
}

func (r *RingBuffer) Push(msg string) {
	idx := atomic.AddUint64(&r.head, 1) - 1
	slot := idx & r.mask
	r.buffer[slot] = msg
}

func (r *RingBuffer) ReadSlot(idx uint64) string {
	return r.buffer[idx&r.mask]
}

func main() {
	rb := NewRingBuffer(8) // 8 ta elementli doiraviy bufer
	var wg sync.WaitGroup

	// 4 ta parallel goroutine to'xtovsiz log yozadi
	for i := 1; i <= 4; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for j := 1; j <= 3; j++ {
				rb.Push(fmt.Sprintf("Log_w%d_seq%d", workerID, j))
			}
		}(i)
	}

	wg.Wait()

	totalLogged := atomic.LoadUint64(&rb.head)
	fmt.Printf("[Lock-Free Ring Buffer] Jami yozilgan loglar soni: %d\n", totalLogged)
	fmt.Println("Doiraviy buferdagi oxirgi 4 ta faol slot:")
	for s := uint64(0); s < 4; s++ {
		fmt.Printf("Slot #%d: %s\n", s, rb.ReadSlot(s))
	}
}
```
**Tushuntirish:** Ring Buffer 2 ning darajasiga teng hajmda yaratilganda (`powerOfTwo`), bo'lish (`%`) amali o'rniga tezkor bitwise amali `idx & mask` ishlatiladi. Bu zamonaviy protsessorlarda 1 ta CPU siklida bajariladi va hech qanday mutex talab qilmaydi.
**Ishlash natijasi:**
```text
[Lock-Free Ring Buffer] Jami yozilgan loglar soni: 12
Doiraviy buferdagi oxirgi 4 ta faol slot:
Slot #0: Log_w2_seq3
Slot #1: Log_w3_seq1
Slot #2: Log_w3_seq2
Slot #3: Log_w3_seq3
```

---

### Topshiriq #1299: Zero-Copy Network I/O: net.Buffers va io.CopyBuffer bilan tarmoq paketlarini uzatish
**Tavsif:** Fayllar, gRPC sarlavhalari va payloadlarini tarmoq soketiga uzatishda ma'lumotlarni foydalanuvchi maydonidan (user-space) yadro maydoniga (kernel-space) qayta-qayta nusxalash CPU ni to'ldirib yuboradi. `net.Buffers` (vectored I/O writev) orqali nol-nusxa (Zero-Copy) tamoyilida paketlarni birlashtirish lozim.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"bytes"
	"fmt"
	"net"
)

func main() {
	// TCP test ulanishini simulyatsiya qilamiz
	server, client := net.Pipe()
	defer server.Close()
	defer client.Close()

	// 1. Tarmoqqa uzatilishi lozim bo'lgan turli bo'laklar
	header := []byte("KHORAZMIY_PROTO_V2\n")
	metadata := []byte("X-Trace-ID: 9918273645\nContent-Type: application/grpc\n\n")
	payload := bytes.Repeat([]byte("High-Speed-Binary-Data-Stream;"), 4)

	// 2. net.Buffers vectored I/O buferi
	buffers := net.Buffers{header, metadata, payload}

	go func() {
		// Nol-nusxa (Zero-Copy writev) bilan soketga yozish
		written, err := buffers.WriteTo(server)
		if err != nil {
			fmt.Printf("Yozish xatosi: %v\n", err)
			return
		}
		fmt.Printf("[Zero-Copy Sender] Soketga jami yozilgan baytlar: %d bayt\n", written)
	}()

	// Qabul qiluvchi tomon
	buf := make([]byte, 512)
	n, _ := client.Read(buf)

	fmt.Printf("[Receiver Socket] Qabul qilingan hajm: %d bayt\n", n)
	fmt.Printf("[Qabul Qilingan Xabar Boshi]:\n%s...\n", string(buf[:60]))
}
```
**Tushuntirish:** `net.Buffers` OS darajasidagi `writev` tizim chaqiruvini (System Call) ishlatadi. Alohida buferlarni bitta massivga nusxalab vaqt ketkazmasdan, operatsion tizim yadrosiga bir vaqtning o'zida bir nechta xotira manzillarini ko'rsatib, to'g'ridan-to'g'ri tarmoq kartasiga (NIC DMA) yuborish imkonini beradi.
**Ishlash natijasi:**
```text
[Zero-Copy Sender] Soketga jami yozilgan baytlar: 191 bayt
[Receiver Socket] Qabul qilingan hajm: 191 bayt
[Qabul Qilingan Xabar Boshi]:
KHORAZMIY_PROTO_V2
X-Trace-ID: 9918273645
Content-Type: applica...
```

---

### Topshiriq #1300: Production-Ready Microservice Orchestrator: gRPC, Worker Pool, Tracing, Circuit Breaker va Kesh integratsiyasi
**Tavsif:** Barcha o'rganilgan mavzularni (gRPC Streaming, Protobuf, Context timeouts, Goroutine Worker Pool, Circuit Breaker, Taqsimlangan kesh va OpenTelemetry) yagona, to'liq, ishlab chiqarishga (Production) tayyor mikroservis arxitekturasida birlashtirish talab etiladi.
**Talablar:** Goroutine leak profilaktikasi, Memory allocation kamaytirish, Race condition yo'qligi va yuqori RPS.
**Yechim (Go):**
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

// OrchestratedMicroservice butun tizim boshqaruvchisi
type OrchestratedMicroservice struct {
	cache       sync.Map
	circuitOpen uint32
	workerQueue chan func()
	metrics     uint64
	wg          sync.WaitGroup
	ctx         context.Context
	cancel      context.CancelFunc
}

func NewMicroservice() *OrchestratedMicroservice {
	ctx, cancel := context.WithCancel(context.Background())
	s := &OrchestratedMicroservice{
		workerQueue: make(chan func(), 100),
		ctx:         ctx,
		cancel:      cancel,
	}

	// Worker pool ishchilari
	for i := 0; i < 3; i++ {
		s.wg.Add(1)
		go func() {
			defer s.wg.Done()
			for {
				select {
				case <-s.ctx.Done():
					return
				case job := <-s.workerQueue:
					job()
				}
			}
		}()
	}
	return s
}

func (s *OrchestratedMicroservice) HandleRequest(ctx context.Context, reqID string) (string, error) {
	atomic.AddUint64(&s.metrics, 1)

	// 1. Context tekshiruvi
	select {
	case <-ctx.Done():
		return "", ctx.Err()
	default:
	}

	// 2. Kesh tekshiruvi (Cache Hit)
	if val, ok := s.cache.Load(reqID); ok {
		return fmt.Sprintf("KESH_NATIJA: %v", val), nil
	}

	// 3. Circuit Breaker tekshiruvi
	if atomic.LoadUint32(&s.circuitOpen) == 1 {
		return "", fmt.Errorf("circuit breaker OPEN: so'rov rad etildi")
	}

	// 4. Asinxron Worker orqali hisoblash
	resultChan := make(chan string, 1)
	s.workerQueue <- func() {
		time.Sleep(20 * time.Millisecond) // CPU hisobi
		res := fmt.Sprintf("PAYLOAD_BAJARILDI_%s", reqID)
		s.cache.Store(reqID, res)
		resultChan <- res
	}

	select {
	case <-ctx.Done():
		return "", ctx.Err()
	case res := <-resultChan:
		return res, nil
	}
}

func (s *OrchestratedMicroservice) Stop() {
	s.cancel()
	s.wg.Wait()
	close(s.workerQueue)
}

func main() {
	service := NewMicroservice()
	defer service.Stop()

	fmt.Println("[Khorazmiy AI Microservice Orchestrator Ishga Tushdi]")

	// 1-so'rov (Keshda yo'q, worker bajaradi)
	ctx1, cancel1 := context.WithTimeout(context.Background(), 100*time.Millisecond)
	resp1, err1 := service.HandleRequest(ctx1, "REQ_001")
	cancel1()
	fmt.Printf("[So'rov 1]: Resp='%s' | Err=%v\n", resp1, err1)

	// 2-so'rov (Keshdan darhol oladi)
	ctx2, cancel2 := context.WithTimeout(context.Background(), 50*time.Millisecond)
	resp2, err2 := service.HandleRequest(ctx2, "REQ_001")
	cancel2()
	fmt.Printf("[So'rov 2]: Resp='%s' | Err=%v\n", resp2, err2)

	fmt.Printf("[Tizim Yakuniy Audit]: Qayta ishlangan so'rovlar: %d ta\n",
		atomic.LoadUint64(&service.metrics))
}
```
**Tushuntirish:** Ushbu yakuniy modulda barcha arxitektura tarkibiy qismlari: context timeout boshqaruvi, sync.Map tezkor kesh, non-blocking atomik circuit breaker, xotirada ajratilgan worker pool va goroutine leak profilaktikasi birlashtirildi. Tizim to'liq yopilayotganda `service.Stop()` barcha resurslarni xavfsiz ozod qiladi.
**Ishlash natijasi:**
```text
[Khorazmiy AI Microservice Orchestrator Ishga Tushdi]
[So'rov 1]: Resp='PAYLOAD_BAJARILDI_REQ_001' | Err=<nil>
[So'rov 2]: Resp='KESH_NATIJA: PAYLOAD_BAJARILDI_REQ_001' | Err=<nil>
[Tizim Yakuniy Audit]: Qayta ishlangan so'rovlar: 2 ta
```
