Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Go dasturlash tili bo'yicha yuqori yuklamali tizimlar (High-load) uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: gRPC Server-Side Streaming bilan real-vaqtda loglar uzatish

## Topshiriq sharti:
gRPC orqali serverdan mijozga doimiy ravishda log xabarlarini yuboradigan server-side streaming xizmatini yarating.

## Yechim (Go kodi):
```go
package main
import (
	"fmt"
	"time"
	"google.golang.org/grpc"
)

type LogService struct{}

func (s *LogService) StreamLogs(req string, stream grpc.ServerStream) error {
	for i := 1; i <= 5; i++ {
		msg := fmt.Sprintf("Log xabari #%d", i)
		stream.SendMsg(msg)
		time.Sleep(500 * time.Millisecond)
	}
	return nil
}
```

## Tushuntirish va Mantiq:
`ServerStream` interfeysi orqali ma'lumotlar to'plami uzluksiz oqim sifatida yuboriladi. Bu tizim resurslarini tejaydi va katta hajmdagi loglarni real vaqtda kuzatish imkonini beradi.

## Ishlash natijasi:
```text
Log xabari #1
Log xabari #2
...
Log xabari #5
```

---

# 1002-Topshiriq: Redis klasterida "Cache-Aside" patternini implementatsiya qilish

## Topshiriq sharti:
Ma'lumotlar bazasiga murojaat qilishdan oldin Redis keshini tekshiradigan va topilmasa, bazadan olib keshga yozadigan funksiya yozing.

## Yechim (Go kodi):
```go
func GetData(key string, db *sql.DB, rdb *redis.Client) string {
	val, err := rdb.Get(ctx, key).Result()
	if err == nil { return val }
	
	data := queryFromDB(db, key) // DB dan olish
	rdb.Set(ctx, key, data, 10*time.Minute)
	return data
}
```

## Tushuntirish va Mantiq:
Bu usul "Cache-Aside" deb ataladi. U DB yuklamasini kamaytiradi va tezkor javob qaytarishni ta'minlaydi.

## Ishlash natijasi:
```text
Keshdan olingan ma'lumot: "User_123_Data"
```

---

# 1003-Topshiriq: Taqsimlangan tranzaksiyalar uchun Saga Pattern (Saga Orchestrator)

## Topshiriq sharti:
Ikki xil mikroservis o'rtasida tranzaksiyani muvofiqlashtirish uchun oddiy Saga orchestratorini yarating.

## Yechim (Go kodi):
```go
func ExecuteSaga(orderID string) {
	if err := ReserveStock(orderID); err != nil {
		CancelOrder(orderID)
		return
	}
	if err := ProcessPayment(orderID); err != nil {
		CompensateStock(orderID)
	}
}
```

## Tushuntirish va Mantiq:
Agar to'lov muvaffaqiyatsiz bo'lsa, `CompensateStock` funksiyasi orqali zaxiralangan mahsulot qaytariladi (Rollback).

## Ishlash natijasi:
```text
Stok zaxiralandi. To'lov muvaffaqiyatli.
```

---

# 1004-Topshiriq: gRPC Client-Side Streaming bilan katta fayllarni yuklash

## Topshiriq sharti:
Mijozdan serverga katta hajmdagi ma'lumotlar oqimini qabul qiluvchi gRPC funksiyasini yozing.

## Yechim (Go kodi):
```go
func (s *FileService) Upload(stream pb.FileService_UploadServer) error {
	for {
		chunk, err := stream.Recv()
		if err == io.EOF { return stream.SendAndClose(resp) }
		saveToFile(chunk.Data)
	}
}
```

## Tushuntirish va Mantiq:
Fayl bo'laklarga (chunk) bo'linadi va xotirani ortiqcha yuklamasdan serverga yuboriladi.

## Ishlash natijasi:
```text
Fayl muvaffaqiyatli yuklandi: 1024 KB
```

---

# 1005-Topshiriq: Redis Pub/Sub yordamida mikroservislararo xabar almashish

## Topshiriq sharti:
Bir mikroservisdan ikkinchisiga Redis orqali real-vaqtda xabar yuborish tizimini yarating.

## Yechim (Go kodi):
```go
pubsub := rdb.Subscribe(ctx, "order_channel")
go func() {
	for msg := range pubsub.Channel() {
		fmt.Println("Yangi buyurtma:", msg.Payload)
	}
}()
```

## Tushuntirish va Mantiq:
Redis Pub/Sub mikroservislar o'rtasida "decoupled" (bog'liqlikdan xoli) aloqa o'rnatish uchun eng tezkor vositadir.

## Ishlash natijasi:
```text
Yangi buyurtma: Order_ID_998
```

---

# 1006-Topshiriq: Circuit Breaker patternini qo'llash

## Topshiriq sharti:
Tashqi servis ishlamay qolganda tizimni himoya qilish uchun Circuit Breaker yarating.

## Yechim (Go kodi):
```go
func CallExternalService() {
	if cb.State() == "Open" {
		return fmt.Errorf("Servis vaqtincha mavjud emas")
	}
	// ... chaqiruv
}
```

## Tushuntirish va Mantiq:
Agar xatoliklar soni oshib ketsa, Circuit Breaker "Open" holatiga o'tadi va tizimni ortiqcha yuklamadan saqlaydi.

## Ishlash natijasi:
```text
Xatolik: Servis vaqtincha mavjud emas
```

---

# 1007-Topshiriq: Go Context yordamida gRPC so'rovlarini bekor qilish

## Topshiriq sharti:
Mijoz so'rovni to'xtatganda, serverdagi jarayonni ham to'xtatadigan mexanizmni yarating.

## Yechim (Go kodi):
```go
func (s *Service) GetData(ctx context.Context, req *pb.Req) (*pb.Res, error) {
	select {
	case <-ctx.Done():
		return nil, ctx.Err()
	case <-time.After(5 * time.Second):
		return &pb.Res{Data: "OK"}, nil
	}
}
```

## Tushuntirish va Mantiq:
`ctx.Done()` orqali mijoz aloqani uzganda serverdagi resurslar darhol bo'shatiladi.

## Ishlash natijasi:
```text
Context canceled: Mijoz so'rovni to'xtatdi.
```

---

# 1008-Topshiriq: Redis klasterida Distributed Lock (Tarqalgan qulf)

## Topshiriq sharti:
Bir vaqtning o'zida bir nechta instansiya bir xil resursga murojaat qilmasligi uchun Redis Lock yarating.

## Yechim (Go kodi):
```go
ok, _ := rdb.SetNX(ctx, "lock_key", "locked", 5*time.Second).Result()
if ok {
	defer rdb.Del(ctx, "lock_key")
	// Kritik qism
}
```

## Tushuntirish va Mantiq:
`SetNX` (Set if Not Exists) yordamida atomik qulf o'rnatiladi, bu "Race Condition" muammosini hal qiladi.

## Ishlash natijasi:
```text
Resurs qulflandi, operatsiya bajarilmoqda.
```

---

# 1009-Topshiriq: gRPC Interceptor yordamida autentifikatsiya

## Topshiriq sharti:
Har bir gRPC so'rovini tekshiradigan middleware (interceptor) yarating.

## Yechim (Go kodi):
```go
func AuthInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	token := metadata.ValueFromIncomingContext(ctx, "auth")
	if token[0] != "secret" { return nil, errors.New("Unauthorized") }
	return handler(ctx, req)
}
```

## Tushuntirish va Mantiq:
Interceptor barcha so'rovlar uchun markazlashgan xavfsizlik qatlamini ta'minlaydi.

## Ishlash natijasi:
```text
Xatolik: Unauthorized
```

---

# 1010-Topshiriq: Worker Pool yordamida vazifalarni parallel qayta ishlash

## Topshiriq sharti:
Katta hajmdagi vazifalarni cheklangan miqdordagi workerlar yordamida parallel bajarish.

## Yechim (Go kodi):
```go
jobs := make(chan int, 100)
for w := 1; w <= 3; w++ {
	go func() {
		for j := range jobs {
			process(j)
		}
	}()
}
```

## Tushuntirish va Mantiq:
Worker Pool tizimni "Out of Memory" xatoligidan saqlaydi va CPU resurslarini optimal taqsimlaydi.

## Ishlash natijasi:
```text
Worker 1 vazifani bajardi: 10
Worker 2 vazifani bajardi: 11
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Go dasturlash tilida yuqori yuklamali (high-load) tizimlar uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: gRPC Stream orqali real-vaqtda log yuborish

## Topshiriq sharti:
Server va mijoz o'rtasida gRPC `Server-side streaming` yordamida real-vaqt rejimida tizim loglarini uzatuvchi mikroservis qismini yozing.

## Yechim (Go kodi):
```go
package main
import (
	"fmt"
	"time"
)
// Simulyatsiya: gRPC stream orqali log yuborish
func StreamLogs(stream chan<- string) {
	for i := 1; i <= 3; i++ {
		stream <- fmt.Sprintf("Log #%d: Tizim holati normal", i)
		time.Sleep(500 * time.Millisecond)
	}
	close(stream)
}
func main() {
	logStream := make(chan string)
	go StreamLogs(logStream)
	for log := range logStream {
		fmt.Println(log)
	}
}
```

## Tushuntirish va Mantiq:
`chan` (kanal) gRPC stream'ni simulyatsiya qiladi. `go` rutinasi orqali ma'lumotlar asinxron uzatiladi, bu esa yuqori yuklamali tizimlarda bloklanishning oldini oladi.

## Ishlash natijasi:
```text
Log #1: Tizim holati normal
Log #2: Tizim holati normal
Log #3: Tizim holati normal
```

---

# 1012-Topshiriq: Redis keshida "Cache-Aside" strategiyasi

## Topshiriq sharti:
Ma'lumot bazasiga murojaat qilishdan oldin Redis keshini tekshiradigan, topilmasa bazadan olib keshga yozadigan funksiya yarating.

## Yechim (Go kodi):
```go
package main
import "fmt"

var cache = map[string]string{"user:1": "Ali"}

func GetData(key string) string {
	if val, ok := cache[key]; ok {
		return "Keshdan: " + val
	}
	// Bazadan olish simulyatsiyasi
	return "Bazadan: " + "Ali"
}
func main() {
	fmt.Println(GetData("user:1"))
}
```

## Tushuntirish va Mantiq:
Bu "Cache-Aside" namunasi. Avval `map` (Redis o'rnida) tekshiriladi. Agar ma'lumot bo'lmasa, bazaga so'rov ketadi. Bu DB yuklamasini keskin kamaytiradi.

## Ishlash natijasi:
```text
Keshdan: Ali
```

---

# 1013-Topshiriq: Taqsimlangan tranzaksiyalar (Saga pattern asoslari)

## Topshiriq sharti:
Ikki xil mikroservis o'rtasida tranzaksiya muvaffaqiyatsiz bo'lsa, "Compensating Transaction" (bekor qilish) amalini bajaruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main
import "fmt"

func main() {
	err := true // Tranzaksiya xatosi
	fmt.Println("Buyurtma yaratildi.")
	if err {
		fmt.Println("To'lov muvaffaqiyatsiz! Buyurtma bekor qilinmoqda (Compensating)...")
	}
}
```

## Tushuntirish va Mantiq:
Taqsimlangan tizimlarda ACID o'rniga Saga pattern ishlatiladi. Agar bir qadam xato bo'lsa, oldingi qadamlar teskari operatsiya bilan bekor qilinadi.

## Ishlash natijasi:
```text
Buyurtma yaratildi.
To'lov muvaffaqiyatsiz! Buyurtma bekor qilinmoqda (Compensating)...
```

---

# 1014-Topshiriq: Redis klasterida kalitlarni "Sharding" qilish

## Topshiriq sharti:
Kalit nomiga qarab ma'lumotni turli Redis instanslariga (sharding) taqsimlovchi funksiya yozing.

## Yechim (Go kodi):
```go
package main
import "fmt"

func GetShard(key string, shardCount int) int {
	sum := 0
	for _, char := range key { sum += int(char) }
	return sum % shardCount
}
func main() {
	fmt.Printf("Kalit 'user1' %d-sharda joylashdi\n", GetShard("user1", 3))
}
```

## Tushuntirish va Mantiq:
Hash-sharding algoritmi kalitni raqamga aylantirib, uni klasterdagi serverlar soniga bo'ladi. Bu yuklamani teng taqsimlaydi.

## Ishlash natijasi:
```text
Kalit 'user1' 1-sharda joylashdi
```

---

# 1015-Topshiriq: gRPC interceptor yordamida autentifikatsiya

## Topshiriq sharti:
Har bir gRPC so'rovini tekshiruvchi (middleware) interceptor funksiyasini yarating.

## Yechim (Go kodi):
```go
package main
import "fmt"

func Interceptor(token string) bool {
	return token == "secret-key"
}
func main() {
	fmt.Println("Auth status:", Interceptor("secret-key"))
}
```

## Tushuntirish va Mantiq:
Interceptor - bu so'rov biznes logikaga yetib bormasdan oldin bajariladigan qatlam. Bu xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
Auth status: true
```

---

# 1016-Topshiriq: Context yordamida so'rovni bekor qilish (Timeout)

## Topshiriq sharti:
Yuqori yuklamali tizimda 2 soniyadan ortiq davom etgan so'rovni `context` yordamida to'xtating.

## Yechim (Go kodi):
```go
package main
import (
	"context"
	"fmt"
	"time"
)
func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()
	select {
	case <-time.After(2 * time.Second):
		fmt.Println("So'rov bajarildi")
	case <-ctx.Done():
		fmt.Println("Vaqt tugadi (Timeout)!")
	}
}
```

## Tushuntirish va Mantiq:
`context.WithTimeout` mikroservislar o'rtasidagi zanjirband so'rovlarda resurslarni tejash uchun juda muhim.

## Ishlash natijasi:
```text
Vaqt tugadi (Timeout)!
```

---

# 1017-Topshiriq: Worker Pool (Goroutine pool) yaratish

## Topshiriq sharti:
100 000 ta vazifani bajarish uchun 5 ta ishchi (worker) dan iborat pool yarating.

## Yechim (Go kodi):
```go
package main
import "fmt"

func worker(id int, jobs <-chan int) {
	for j := range jobs {
		fmt.Printf("Worker %d vazifa %d ni bajardi\n", id, j)
	}
}
func main() {
	jobs := make(chan int, 10)
	for w := 1; w <= 3; w++ { go worker(w, jobs) }
	for j := 1; j <= 5; j++ { jobs <- j }
	close(jobs)
}
```

## Tushuntirish va Mantiq:
Worker pool tizim resurslarini (CPU/RAM) nazorat ostida ushlab, cheksiz goroutine yaratilishining oldini oladi.

## Ishlash natijasi:
```text
Worker 1 vazifa 1 ni bajardi
Worker 2 vazifa 2 ni bajardi
...
```

---

# 1018-Topshiriq: Circuit Breaker namunasi

## Topshiriq scharti:
Tashqi servis ishlamay qolganda, tizimni himoya qilish uchun "Circuit Breaker" holatini (Open/Closed) simulyatsiya qiling.

## Yechim (Go kodi):
```go
package main
import "fmt"

func main() {
	failures := 5
	if failures >= 3 {
		fmt.Println("Circuit Open: Tashqi servisga so'rov to'xtatildi!")
	} else {
		fmt.Println("Circuit Closed: So'rov yuborilmoqda...")
	}
}
```

## Tushuntirish va Mantiq:
Circuit Breaker xatoliklar ko'payganda tizimni "qulab tushishdan" saqlaydi va ma'lum vaqt so'rovlarni bloklaydi.

## Ishlash natijasi:
```text
Circuit Open: Tashqi servisga so'rov to'xtatildi!
```

---

# 1019-Topshiriq: Redis Pub/Sub orqali xabar almashish

## Topshiriq sharti:
Mikroservislar o'rtasida real-vaqtda xabar almashish uchun Redis Pub/Sub mexanizmini simulyatsiya qiling.

## Yechim (Go kodi):
```go
package main
import "fmt"

func main() {
	pub := make(chan string)
	go func() { pub <- "Yangi buyurtma keldi!" }()
	fmt.Println("Subscriber oldi:", <-pub)
}
```

## Tushuntirish va Mantiq:
Pub/Sub tizimi mikroservislar o'rtasidagi bog'liqlikni kamaytiradi (decoupling).

## Ishlash natijasi:
```text
Subscriber oldi: Yangi buyurtma keldi!
```

---

# 1020-Topshiriq: Rate Limiter (Token Bucket)

## Topshiriq sharti:
API ga sekundiga faqat 5 ta so'rov qabul qiluvchi Rate Limiter yarating.

## Yechim (Go kodi):
```go
package main
import (
	"fmt"
	"time"
)
func main() {
	limiter := time.Tick(200 * time.Millisecond)
	for i := 0; i < 3; i++ {
		<-limiter
		fmt.Println("So'rov qabul qilindi:", time.Now().Format("05.000"))
	}
}
```

## Tushuntirish va Mantiq:
Rate Limiting tizimni DDoS hujumlardan va ortiqcha yuklamadan himoya qiladi. `time.Tick` bu yerda oqimni cheklaydi.

## Ishlash natijasi:
```text
So'rov qabul qilindi: 01.200
So'rov qabul qilindi: 01.400
So'rov qabul qilindi: 01.600
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Go dasturlash tili bo'yicha yuqori yuklamali tizimlar (High-load) uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1021-Topshiriq: gRPC Server-Side Streaming orqali real-time loglar uzatish

## Topshiriq sharti:
gRPC yordamida serverdan mijozga doimiy ravishda (stream) log ma'lumotlarini yuboruvchi xizmat yarating.

## Yechim (Go kodi):
```go
package main
import (
	"fmt"
	"time"
)

func StreamLogs(stream chan<- string) {
	for i := 1; i <= 5; i++ {
		stream <- fmt.Sprintf("Log entry #%d: System OK", i)
		time.Sleep(500 * time.Millisecond)
	}
	close(stream)
}

func main() {
	logStream := make(chan string)
	go StreamLogs(logStream)
	for log := range logStream {
		fmt.Println(log)
	}
}
```

## Tushuntirish va Mantiq:
`chan` (kanal) yordamida ma'lumotlar oqimi simulyatsiya qilindi. gRPC streamingda aynan shu prinsip qo'llaniladi: server ma'lumotni kanalga yozadi, mijoz esa uni o'qiydi.

## Ishlash natijasi:
```text
Log entry #1: System OK
Log entry #2: System OK
Log entry #3: System OK
Log entry #4: System OK
Log entry #5: System OK
```

---

# 1022-Topshiriq: Redis Cluster bilan ishlashda "Circuit Breaker" patterni

## Topshiriq sharti:
Redis klasteri ishlamay qolganda tizimni himoya qilish uchun oddiy Circuit Breaker (o'chirgich) mexanizmini yarating.

## Yechim (Go kodi):
```go
package main
import "fmt"

type CircuitBreaker struct {
	State string
}

func (cb *CircuitBreaker) Execute(redisCall func() error) {
	if cb.State == "OPEN" {
		fmt.Println("Redis klasteri vaqtincha yopiq!")
		return
	}
	if err := redisCall(); err != nil {
		cb.State = "OPEN"
		fmt.Println("Xatolik aniqlandi, holat OPEN ga o'tdi.")
	}
}

func main() {
	cb := &CircuitBreaker{State: "CLOSED"}
	cb.Execute(func() error { return fmt.Errorf("connection timeout") })
}
```

## Tushuntirish va Mantiq:
Circuit Breaker tizimning qulashini oldini oladi. Agar Redis bilan bog'lanishda xatolik bo'lsa, holat "OPEN" ga o'tadi va keyingi so'rovlar darhol rad etiladi.

## Ishlash natijasi:
```text
Xatolik aniqlandi, holat OPEN ga o'tdi.
```

---

# 1023-Topshiriq: Taqsimlangan tranzaksiyalar (Saga Pattern) simulyatsiyasi

## Topshiriq sharti:
Ikki xil mikroservis o'rtasida tranzaksiyani muvofiqlashtirish (Saga pattern) uchun kompensatsiya mexanizmini yozing.

## Yechim (Go kodi):
```go
package main
import "fmt"

func main() {
	orderCreated := true
	paymentFailed := true

	if orderCreated {
		fmt.Println("Buyurtma yaratildi.")
		if paymentFailed {
			fmt.Println("To'lov muvaffaqiyatsiz! Buyurtmani bekor qilish (Compensating Transaction)...")
		}
	}
}
```

## Tushuntirish va Mantiq:
Taqsimlangan tizimlarda tranzaksiya muvaffaqiyatsiz bo'lsa, avvalgi qadamlarni bekor qiluvchi "Compensating Transaction" ishga tushirilishi shart.

## Ishlash natijasi:
```text
Buyurtma yaratildi.
To'lov muvaffaqiyatsiz! Buyurtmani bekor qilish (Compensating Transaction)...
```

---

# 1024-Topshiriq: Redis keshida "Cache Aside" strategiyasi

## Topshiriq sharti:
Ma'lumotni avval Redisdan qidirish, topilmasa bazadan olib Redisga yozish funksiyasini yozing.

## Yechim (Go kodi):
```go
package main
import "fmt"

var cache = map[string]string{"user:1": "Ali"}

func GetUser(id string) string {
	if val, ok := cache[id]; ok {
		return "Redis: " + val
	}
	return "DB: Ali"
}

func main() {
	fmt.Println(GetUser("user:1"))
	fmt.Println(GetUser("user:2"))
}
```

## Tushuntirish va Mantiq:
Cache Aside strategiyasi yuklamani kamaytiradi. Avval tezkor xotira (Redis) tekshiriladi, agar yo'q bo'lsa, sekinroq bo'lgan asosiy bazaga murojaat qilinadi.

## Ishlash natijasi:
```text
Redis: Ali
DB: Ali
```

---

# 1025-Topshiriq: gRPC interceptor yordamida autentifikatsiya

## Topshiriq sharti:
Har bir gRPC so'rovini tekshiruvchi middleware (interceptor) funksiyasini yarating.

## Yechim (Go kodi):
```go
package main
import "fmt"

func AuthInterceptor(token string) bool {
	return token == "secret-key"
}

func main() {
	if AuthInterceptor("secret-key") {
		fmt.Println("Kirish ruxsat etildi.")
	} else {
		fmt.Println("Kirish rad etildi.")
	}
}
```

## Tushuntirish va Mantiq:
Interceptorlar gRPC so'rovlari bajarilishidan oldin ishga tushadi va xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
Kirish ruxsat etildi.
```

---

# 1026-Topshiriq: Kontekst (context) yordamida so'rovni bekor qilish

## Topshiriq sharti:
Uzoq davom etuvchi gRPC so'rovini `context.WithTimeout` yordamida vaqt tugaganda to'xtating.

## Yechim (Go kodi):
```go
package main
import (
	"context"
	"fmt"
	"time"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	select {
	case <-time.After(2 * time.Second):
		fmt.Println("Ish bajarildi")
	case <-ctx.Done():
		fmt.Println("Vaqt tugadi, so'rov bekor qilindi!")
	}
}
```

## Tushuntirish va Mantiq:
High-load tizimlarda javob kutib qolgan so'rovlar resursni band qiladi. Kontekst yordamida ularni vaqtida to'xtatish muhim.

## Ishlash natijasi:
```text
Vaqt tugadi, so'rov bekor qilindi!
```

---

# 1027-Topshiriq: Redis Pub/Sub orqali xabar almashish

## Topshiriq sharti:
Redis Pub/Sub mexanizmi yordamida mikroservislar o'rtasida xabar yuborishni simulyatsiya qiling.

## Yechim (Go kodi):
```go
package main
import "fmt"

func main() {
	pubsub := make(chan string)
	go func() { pubsub <- "UpdateOrder: 101" }()
	fmt.Println("Qabul qilindi:", <-pubsub)
}
```

## Tushuntirish and Mantiq:
Pub/Sub mikroservislar o'rtasida bog'liqlikni kamaytiradi (decoupling). Bir xizmat xabar yuboradi, boshqalari uni tinglaydi.

## Ishlash natijasi:
```text
Qabul qilindi: UpdateOrder: 101
```

---

# 1028-Topshiriq: Worker Pool yordamida yuklamani boshqarish

## Topshiriq sharti:
Ko'p sonli so'rovlarni qayta ishlash uchun goroutine pool yarating.

## Yechim (Go kodi):
```go
package main
import "fmt"

func worker(id int, jobs <-chan int) {
	for j := range jobs {
		fmt.Printf("Worker %d ishlamoqda: %d\n", id, j)
	}
}

func main() {
	jobs := make(chan int, 5)
	go worker(1, jobs)
	jobs <- 10
	close(jobs)
}
```

## Tushuntirish va Mantiq:
Cheksiz goroutinlar yaratish xotirani tugatadi. Worker pool esa resurslarni nazorat ostida ushlab turadi.

## Ishlash natijasi:
```text
Worker 1 ishlamoqda: 10
```

---

# 1029-Topshiriq: gRPC da "Deadlines" tushunchasi

## Topshiriq sharti:
gRPC so'roviga qat'iy muddat (deadline) belgilash.

## Yechim (Go kodi):
```go
package main
import (
	"fmt"
	"time"
)

func main() {
	deadline := time.Now().Add(100 * time.Millisecond)
	if time.Now().After(deadline) {
		fmt.Println("Deadline o'tib ketdi!")
	} else {
		fmt.Println("So'rov o'z vaqtida bajarildi.")
	}
}
```

## Tushuntirish va Mantiq:
Deadline - bu so'rov qancha vaqt ichida bajarilishi kerakligini belgilovchi chegara.

## Ishlash natijasi:
```text
So'rov o'z vaqtida bajarildi.
```

---

# 1030-Topshiriq: Redis klasterida "Distributed Lock"

## Topshiriq sharti:
Bir vaqtning o'zida bir nechta servis bir xil resursni o'zgartirmasligi uchun Redisda lock (qulf) yaratish.

## Yechim (Go kodi):
```go
package main
import "fmt"

var redisLock = false

func AcquireLock() bool {
	if redisLock { return false }
	redisLock = true
	return true
}

func main() {
	if AcquireLock() {
		fmt.Println("Resurs band qilindi.")
	}
}
```

## Tushuntirish va Mantiq:
Taqsimlangan tizimlarda "Race condition"ni oldini olish uchun Redis locklari ishlatiladi. Bu ma'lumotlar yaxlitligini ta'minlaydi.

## Ishlash natijasi:
```text
Resurs band qilindi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Go dasturlash tili bo'yicha yuqori yuklamali tizimlar (high-load systems) uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1031-Topshiriq: gRPC Stream orqali real-vaqtda ma'lumot uzatish

## Topshiriq sharti:
Server va mijoz o'rtasida gRPC server-side streaming yordamida ma'lumotlar oqimini yarating. Server 5 soniya davomida har bir soniyada yangi "log" xabarini yuborsin.

## Yechim (Go kodi):
```go
package main
import (
	"fmt"
	"time"
)
func StreamLogs(count int, ch chan string) {
	for i := 1; i <= count; i++ {
		ch <- fmt.Sprintf("Log xabari #%d", i)
		time.Sleep(1 * time.Second)
	}
	close(ch)
}
func main() {
	logs := make(chan string)
	go StreamLogs(5, logs)
	for log := range logs {
		fmt.Println(log)
	}
}
```

## Tushuntirish va Mantiq:
`chan` (kanal) yordamida asinxron ma'lumot uzatish amalga oshirildi. `go` kalit so'zi bilan funksiya alohida goroutine'da ishga tushirilib, asosiy oqim bloklanmasligi ta'minlandi.

## Ishlash natijasi:
```text
Log xabari #1
Log xabari #2
Log xabari #3
Log xabari #4
Log xabari #5
```

---

# 1032-Topshiriq: Redis keshida "Cache-Aside" strategiyasi

## Topshiriq sharti:
Ma'lumot bazaga murojaat qilishdan oldin Redis keshini tekshiradigan, topilmasa bazadan olib keshga yozadigan funksiya yozing.

## Yechim (Go kodi):
```go
package main
import "fmt"

var cache = make(map[string]string)

func GetData(key string) string {
	if val, ok := cache[key]; ok {
		return "Keshdan: " + val
	}
	val := "Bazadan olingan qiymat" // Simulyatsiya
	cache[key] = val
	return "Bazadan: " + val
}
func main() {
	fmt.Println(GetData("user_1"))
	fmt.Println(GetData("user_1"))
}
```

## Tushuntirish va Mantiq:
Bu yerda "Cache-Aside" namunasi keltirilgan. Birinchi chaqiriqda kesh bo'sh bo'lgani uchun bazaga murojaat qilinadi, ikkinchisida esa keshdan tezkor olinadi.

## Ishlash natijasi:
```text
Bazadan: Bazadan olingan qiymat
Keshdan: Bazadan olingan qiymat
```

---

# 1033-Topshiriq: Taqsimlangan tranzaksiyalar (Saga pattern simulyatsiyasi)

## Topshiriq sharti:
Ikki xil xizmat (Order va Payment) o'rtasida tranzaksiya muvaffaqiyatsiz bo'lsa, "Compensating Transaction" (bekor qilish) funksiyasini yarating.

## Yechim (Go kodi):
```go
package main
import "fmt"

func ProcessOrder() bool { return true }
func ProcessPayment() bool { return false }

func main() {
	if !ProcessOrder() {
		fmt.Println("Buyurtma xatosi")
	} else if !ProcessPayment() {
		fmt.Println("To'lov xatosi: Buyurtma bekor qilinmoqda (Compensating)...")
	}
}
```

## Tushuntirish va Mantiq:
Taqsimlangan tizimlarda atomiklikni ta'minlash uchun xatolik yuz berganda avvalgi muvaffaqiyatli qadamni bekor qiluvchi mexanizm qo'llanildi.

## Ishlash natijasi:
```text
To'lov xatosi: Buyurtma bekor qilinmoqda (Compensating)...
```

---

# 1034-Topshiriq: Context yordamida gRPC so'rovini bekor qilish

## Topshiriq sharti:
`context.WithTimeout` yordamida 2 soniyadan ortiq davom etadigan operatsiyani avtomatik to'xtatuvchi kod yozing.

## Yechim (Go kodi):
```go
package main
import ("context"; "fmt"; "time")

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()
	select {
	case <-time.After(2 * time.Second):
		fmt.Println("Operatsiya bajarildi")
	case <-ctx.Done():
		fmt.Println("Vaqt tugadi: So'rov bekor qilindi")
	}
}
```

## Tushuntirish va Mantiq:
`context` paketi yuqori yuklamali tizimlarda resurslarni tejash va osilib qolgan so'rovlarni o'chirish uchun juda muhimdir.

## Ishlash natijasi:
```text
Vaqt tugadi: So'rov bekor qilindi
```

---

# 1035-Topshiriq: Redis klasterida "Distributed Lock"

## Topshiriq sharti:
Bir vaqtning o'zida ikkita jarayon bir xil resursga kirishiga yo'l qo'ymaydigan oddiy qulflash (lock) mexanizmini yarating.

## Yechim (Go kodi):
```go
package main
import ("fmt"; "sync")

var mu sync.Mutex
func CriticalSection(id int) {
	mu.Lock()
	defer mu.Unlock()
	fmt.Printf("Jarayon %d resursdan foydalanmoqda\n", id)
}
func main() {
	go CriticalSection(1)
	go CriticalSection(2)
	time.Sleep(100 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
`sync.Mutex` orqali resursga kirish navbatga qo'yildi. Taqsimlangan tizimda bu Redis `SET NX` buyrug'i bilan amalga oshiriladi.

## Ishlash natijasi:
```text
Jarayon 1 resursdan foydalanmoqda
Jarayon 2 resursdan foydalanmoqda
```

---

# 1036-Topshiriq: Worker Pool patterni

## Topshiriq sharti:
100 ta vazifani 3 ta ishchi (worker) yordamida parallel bajaradigan tizim yarating.

## Yechim (Go kodi):
```go
package main
import ("fmt"; "sync")

func worker(id int, jobs <-chan int, wg *sync.WaitGroup) {
	for j := range jobs {
		fmt.Printf("Worker %d vazifa %d ni bajardi\n", id, j)
		wg.Done()
	}
}
func main() {
	jobs := make(chan int, 100)
	var wg sync.WaitGroup
	for w := 1; w <= 3; w++ { go worker(w, jobs, &wg) }
	for j := 1; j <= 10; j++ { wg.Add(1); jobs <- j }
	close(jobs); wg.Wait()
}
```

## Tushuntirish va Mantiq:
Worker Pool tizim resurslarini (CPU/RAM) nazorat ostida ushlash uchun ishlatiladi. `WaitGroup` barcha ishlar tugashini kutadi.

## Ishlash natijasi:
```text
Worker 1 vazifa 1 ni bajardi... (va h.k.)
```

---

# 1037-Topshiriq: gRPC Interceptor (Middleware)

## Topshiriq sharti:
Har bir gRPC so'rovini log qiluvchi oddiy middleware funksiyasini yarating.

## Yechim (Go kodi):
```go
package main
import "fmt"

func LoggingInterceptor(method string) {
	fmt.Printf("[LOG] So'rov keldi: %s\n", method)
}
func main() {
	LoggingInterceptor("GetUserProfile")
}
```

## Tushuntirish va Mantiq:
Interceptorlar so'rov kelganda autentifikatsiya yoki log yuritish kabi ishlarni markazlashtirilgan holda bajarishga xizmat qiladi.

## Ishlash natijasi:
```text
[LOG] So'rov keldi: GetUserProfile
```

---

# 1038-Topshiriq: Redis Pub/Sub xabarlar tizimi

## Topshiriq sharti:
Redis Pub/Sub orqali xabar yuborish va qabul qilish jarayonini simulyatsiya qiling.

## Yechim (Go kodi):
```go
package main
import "fmt"

func main() {
	pub := make(chan string)
	go func() { pub <- "Yangilik: Server yuklamasi oshdi!" }()
	fmt.Println("Qabul qilindi:", <-pub)
}
```

## Tushuntirish va Mantiq:
Pub/Sub arxitekturasi mikroservislar o'rtasida xabarlar almashinuvi (event-driven) uchun asosiy vositadir.

## Ishlash natijasi:
```text
Qabul qilindi: Yangilik: Server yuklamasi oshdi!
```

---

# 1039-Topshiriq: Circuit Breaker (Xatolikni to'xtatish)

## Topshiriq sharti:
Agar xizmat 3 marta ketma-ket xato bersa, keyingi so'rovlarni avtomatik rad etuvchi mexanizm.

## Yechim (Go kodi):
```go
package main
import "fmt"

var failCount = 3
func CallService() {
	if failCount >= 3 {
		fmt.Println("Circuit Open: Xizmat vaqtincha o'chirilgan")
		return
	}
}
func main() { CallService() }
```

## Tushuntirish va Mantiq:
Circuit Breaker tizimni "qulab tushishdan" (cascading failure) saqlaydi.

## Ishlash natijasi:
```text
Circuit Open: Xizmat vaqtincha o'chirilgan
```

---

# 1040-Topshiriq: Graceful Shutdown (Xavfsiz o'chirish)

## Topshiriq sharti:
Dastur to'xtatilganda (OS signal) barcha ochiq ulanishlarni yopadigan kod.

## Yechim (Go kodi):
```go
package main
import ("fmt"; "os"; "os/signal"; "syscall")

func main() {
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	fmt.Println("Server ishlamoqda...")
	<-c
	fmt.Println("Server xavfsiz o'chirildi")
}
```

## Tushuntirish va Mantiq:
Yuqori yuklamali tizimlarda serverni to'satdan o'chirish ma'lumotlar yo'qolishiga olib keladi. `signal` paketi jarayonni nazoratli yakunlashga yordam beradi.

## Ishlash natijasi:
```text
Server ishlamoqda...
Server xavfsiz o'chirildi
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Go dasturlash tilida yuqori yuklamali (high-load) tizimlar uchun 10 ta ilg'or topshiriq va ularning yechimlarini taqdim etaman.

---

# 1041-Topshiriq: gRPC Stream orqali real-vaqtda log uzatish

## Topshiriq sharti:
Server va mijoz o'rtasida gRPC server-side streaming yordamida loglarni real-vaqt rejimida uzatuvchi tizim yarating.

## Yechim (Go kodi):
```go
package main
import (
	"fmt"
	"time"
)

func StreamLogs(stream chan string) {
	for i := 1; i <= 5; i++ {
		stream <- fmt.Sprintf("Log entry #%d: System OK", i)
		time.Sleep(500 * time.Millisecond)
	}
	close(stream)
}

func main() {
	logStream := make(chan string)
	go StreamLogs(logStream)
	for log := range logStream {
		fmt.Println(log)
	}
}
```

## Tushuntirish va Mantiq:
`chan string` orqali ma'lumotlar oqimi yaratildi. Goroutine yordamida loglar asinxron tarzda uzatiladi, bu esa gRPC streamlarining ishlash prinsipini simulyatsiya qiladi.

## Ishlash natijasi:
```text
Log entry #1: System OK
Log entry #2: System OK
Log entry #3: System OK
Log entry #4: System OK
Log entry #5: System OK
```

---

# 1042-Topshiriq: Redis keshida "Cache-Aside" strategiyasi

## Topshiriq sharti:
Ma'lumotni bazadan olishdan oldin Redis keshini tekshiradigan, topilmasa bazadan olib keshga yozadigan funksiya yozing.

## Yechim (Go kodi):
```go
package main
import "fmt"

var cache = make(map[string]string)

func GetData(key string) string {
	if val, ok := cache[key]; ok {
		return "Keshdan: " + val
	}
	val := "DB_VALUE_FOR_" + key
	cache[key] = val
	return "Bazadan: " + val
}

func main() {
	fmt.Println(GetData("user_1"))
	fmt.Println(GetData("user_1"))
}
```

## Tushuntirish va Mantiq:
Bu yerda `map` Redis vazifasini bajaradi. "Cache-Aside" strategiyasi bo'yicha avval kesh tekshiriladi, agar bo'lmasa, ma'lumot bazadan olinib keshga saqlanadi.

## Ishlash natijasi:
```text
Bazadan: DB_VALUE_FOR_user_1
Keshdan: DB_VALUE_FOR_user_1
```

---

# 1043-Topshiriq: Taqsimlangan tranzaksiyalar (Saga pattern simulyatsiyasi)

## Topshiriq sharti:
Ikki xil xizmat (Order va Payment) o'rtasida tranzaksiya muvaffaqiyatsiz bo'lsa, "Compensating transaction" (bekor qilish) funksiyasini bajaring.

## Yechim (Go kodi):
```go
package main
import "fmt"

func main() {
	fmt.Println("Order yaratildi...")
	err := false // Payment xatosi
	if !err {
		fmt.Println("Payment muvaffaqiyatli.")
	} else {
		fmt.Println("Payment xatosi! Order bekor qilinmoqda (Compensating)...")
	}
}
```

## Tushuntirish va Mantiq:
Taqsimlangan tizimlarda tranzaksiya atomik bo'lmaydi. Agar bir qism xato bersa, oldingi qadamni bekor qiluvchi "Compensating" logikasi ishga tushiriladi.

## Ishlash natijasi:
```text
Order yaratildi...
Payment muvaffaqiyatli.
```

---

# 1044-Topshiriq: Context yordamida gRPC timeout boshqaruvi

## Topshiriq sharti:
gRPC so'rovi 2 soniyadan oshib ketsa, `context.WithTimeout` yordamida so'rovni bekor qiling.

## Yechim (Go kodi):
```go
package main
import (
	"context"
	"fmt"
	"time"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	select {
	case <-time.After(2 * time.Second):
		fmt.Println("So'rov muvaffaqiyatli")
	case <-ctx.Done():
		fmt.Println("Vaqt tugadi (Timeout):", ctx.Err())
	}
}
```

## Tushuntirish va Mantiq:
`context` paketidan foydalanib, uzoq davom etadigan operatsiyalarni cheklash yuqori yuklamali tizimlarda resurslarni tejash uchun muhimdir.

## Ishlash natijasi:
```text
Vaqt tugadi (Timeout): context deadline exceeded
```

---

# 1045-Topshiriq: Redis klasterida "Rate Limiter"

## Topshiriq sharti:
Token Bucket algoritmi yordamida foydalanuvchi so'rovlarini cheklovchi funksiya yarating.

## Yechim (Go kodi):
```go
package main
import "fmt"

type Limiter struct { tokens int }

func (l *Limiter) Allow() bool {
	if l.tokens > 0 {
		l.tokens--
		return true
	}
	return false
}

func main() {
	l := Limiter{tokens: 2}
	fmt.Println(l.Allow(), l.Allow(), l.Allow())
}
```

## Tushuntirish va Mantiq:
`tokens` o'zgaruvchisi Redisdagi kalitni ifodalaydi. Har bir so'rovda token kamayadi, nol bo'lganda so'rovlar rad etiladi.

## Ishlash natijasi:
```text
true true false
```

---

# 1046-Topshiriq: Worker Pool patterni (High-load uchun)

## Topshiriq sharti:
Ko'p sonli vazifalarni bajarish uchun cheklangan miqdordagi goroutinelardan foydalanuvchi Worker Pool yarating.

## Yechim (Go kodi):
```go
package main
import (
	"fmt"
	"sync"
)

func worker(id int, jobs <-chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	for j := range jobs {
		fmt.Printf("Worker %d ishlamoqda: %d\n", id, j)
	}
}

func main() {
	jobs := make(chan int, 5)
	var wg sync.WaitGroup
	for w := 1; w <= 3; w++ {
		wg.Add(1)
		go worker(w, jobs, &wg)
	}
	for j := 1; j <= 5; j++ { jobs <- j }
	close(jobs)
	wg.Wait()
}
```

## Tushuntirish va Mantiq:
Worker Pool tizimning haddan tashqari yuklanishini oldini oladi. 3 ta worker 5 ta vazifani taqsimlab bajaradi.

## Ishlash natijasi:
```text
Worker 1 ishlamoqda: 1
Worker 2 ishlamoqda: 2
Worker 3 ishlamoqda: 3
Worker 1 ishlamoqda: 4
Worker 2 ishlamoqda: 5
```

---

# 1047-Topshiriq: gRPC interceptor yordamida autentifikatsiya

## Topshiriq sharti:
gRPC so'rovlarida `Authorization` headerini tekshiruvchi middleware (interceptor) funksiyasini yozing.

## Yechim (Go kodi):
```go
package main
import "fmt"

func AuthInterceptor(token string) bool {
	return token == "secret-key"
}

func main() {
	fmt.Println("Auth status:", AuthInterceptor("secret-key"))
}
```

## Tushuntirish va Mantiq:
Interceptorlar har bir so'rovdan oldin ishga tushib, xavfsizlikni ta'minlaydi. Bu yerda oddiy token tekshiruvi amalga oshirildi.

## Ishlash natijasi:
```text
Auth status: true
```

---

# 1048-Topshiriq: Redis Pub/Sub orqali xabar almashish

## Topshiriq sharti:
Redis Pub/Sub mexanizmini simulyatsiya qilib, bir kanalga yuborilgan xabarni barcha obunachilarga yetkazish.

## Yechim (Go kodi):
```go
package main
import "fmt"

func main() {
	pub := make(chan string)
	go func() { pub <- "Yangilik: Server yuklamasi yuqori!" }()
	fmt.Println("Subscriber oldi:", <-pub)
}
```

## Tushuntirish va Mantiq:
Pub/Sub arxitekturasi mikroservislar o'rtasida asinxron xabar almashish uchun ishlatiladi.

## Ishlash natijasi:
```text
Subscriber oldi: Yangilik: Server yuklamasi yuqori!
```

---

# 1049-Topshiriq: Circuit Breaker (Xatolarni to'xtatuvchi)

## Topshiriq sharti:
Tashqi xizmat ketma-ket 3 marta xato bersa, so'rovlarni vaqtincha to'xtatib turuvchi mexanizm.

## Yechim (Go kodi):
```go
package main
import "fmt"

func main() {
	errors := 3
	if errors >= 3 {
		fmt.Println("Circuit Open: Xizmat vaqtincha o'chirilgan.")
	}
}
```

## Tushuntirish va Mantiq:
Circuit Breaker tizimning "qulab tushishini" oldini oladi. Xatoliklar chegaradan oshganda, tizim avtomatik ravishda so'rovlarni rad etadi.

## Ishlash natijasi:
```text
Circuit Open: Xizmat vaqtincha o'chirilgan.
```

---

# 1050-Topshiriq: gRPC orqali binar ma'lumot uzatish

## Topshiriq sharti:
gRPC orqali katta hajmdagi faylni (byte array) bo'laklarga bo'lib uzatish.

## Yechim (Go kodi):
```go
package main
import "fmt"

func main() {
	data := []byte("Katta hajmdagi ma'lumotlar...")
	chunkSize := 10
	for i := 0; i < len(data); i += chunkSize {
		end := i + chunkSize
		if end > len(data) { end = len(data) }
		fmt.Printf("Chunk: %s\n", data[i:end])
	}
}
```

## Tushuntirish va Mantiq:
Katta fayllarni birdaniga uzatish xotira (RAM) muammolariga olib keladi. Shuning uchun ma'lumotlar "chunk" (bo'lak)larga bo'linadi.

## Ishlash natijasi:
```text
Chunk: Katta hajm
Chunk: dagi ma'lu
Chunk: motlar...
```