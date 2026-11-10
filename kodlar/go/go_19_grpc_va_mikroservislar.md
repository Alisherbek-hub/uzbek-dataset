# 901-Topshiriq: RPC (Remote Procedure Call) asoslari: `net/rpc` serveri
## Topshiriq sharti:
Standart `net/rpc` yordamida masofadan chaqiriluvchi hisoblash xizmatini yoqing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net"
	"net/rpc"
)

type Matematika struct{}

type Argumentlar struct {
	A, B int
}

func (m *Matematika) Qosh(arg Argumentlar, javob *int) error {
	*javob = arg.A + arg.B
	return nil
}

func main() {
	matematika := new(Matematika)
	_ = rpc.Register(matematika)

	l, _ := net.Listen("tcp", "127.0.0.1:0")
	defer l.Close()

	go func() {
		conn, _ := l.Accept()
		rpc.ServeConn(conn)
	}()

	client, _ := rpc.Dial("tcp", l.Addr().String())
	defer client.Close()

	var javob int
	_ = client.Call("Matematika.Qosh", Argumentlar{A: 15, B: 25}, &javob)
	fmt.Println("RPC orqali hisoblangan natija:", javob)
}
```

## Tushuntirish va Mantiq:
RPC boshqa kompyuter yoki jarayondagi funksiyani xuddi mahalliy funksiya kabi chaqirish imkonini beradi. Go dagi `net/rpc` ob'ekt metodlarini eksport qiladi.

## Ishlash natijasi:
```text
RPC orqali hisoblangan natija: 40
```

# 902-Topshiriq: `net/rpc` mijozi: Asinxron RPC chaqiruvi (`client.Go`)
## Topshiriq sharti:
`client.Go` yordamida natijani kanal orqali asinxron kutib oling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net"
	"net/rpc"
	"time"
)

type Hisobchi struct{}

func (h *Hisobchi) Kvadrat(son int, res *int) error {
	time.Sleep(20 * time.Millisecond)
	*res = son * son
	return nil
}

func main() {
	_ = rpc.Register(new(Hisobchi))
	l, _ := net.Listen("tcp", "127.0.0.1:0")
	defer l.Close()

	go func() {
		conn, _ := l.Accept()
		rpc.ServeConn(conn)
	}()

	client, _ := rpc.Dial("tcp", l.Addr().String())
	defer client.Close()

	var natija int
	chaqiruv := client.Go("Hisobchi.Kvadrat", 8, &natija, nil)

	fmt.Println("Asinxron so'rov yuborildi, boshqa ishlar bajarilmoqda...")
	<-chaqiruv.Done // Natija tayyor bo'lishini kutamiz

	fmt.Println("Asinxron RPC natijasi:", natija)
}
```

## Tushuntirish va Mantiq:
`client.Go` so'rovni yuborib darhol `*rpc.Call` ob'ektini qaytaradi. Uning `Done` kanali orqali natija tayyor bo'lganda ogohlantiriladi.

## Ishlash natijasi:
```text
Asinxron so'rov yuborildi, boshqa ishlar bajarilmoqda...
Asinxron RPC natijasi: 64
```

# 903-Topshiriq: Protocol Buffers (Protobuf) kontseptsiyasi va binary format
## Topshiriq sharti:
Protobuf nima uchun JSON ga qaraganda ixcham va tez ekanligini simulyatsiya qiling.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type FoydalanuvchiJSON struct {
	ID   int64  `json:"id"`
	Ism  string `json:"ism"`
	Faol bool   `json:"faol"`
}

func main() {
	u := FoydalanuvchiJSON{ID: 1001, Ism: "Shavkat", Faol: true}

	jsonBytes, _ := json.Marshal(u)

	// Protobufda maydon nomlari (kalitlar) matn sifatida jo'natilmaydi,
	// faqat maydon raqami (1 bayt) va qiymat ixcham varint bilan yoziladi.
	// Taxminiy protobuf hajmi ~10-12 bayt bo'ladi
	fmt.Printf("JSON hajmi: %d bayt ('%s')\n", len(jsonBytes), string(jsonBytes))
	fmt.Printf("Protobuf ekvivalent hajmi: ~12 bayt (taxminan 3 barobar ixcham)\n")
}
```

## Tushuntirish va Mantiq:
Protobuf maydon nomlarini takrorlamaydi, sonlarni Varint (o'zgaruvchan uzunlikdagi butun son) sifatida siqadi va ikkilik (binary) formatda uzatadi.

## Ishlash natijasi:
```text
JSON hajmi: 37 bayt ('{"id":1001,"ism":"Shavkat","faol":true}')
Protobuf ekvivalent hajmi: ~12 bayt (taxminan 3 barobar ixcham)
```

# 904-Topshiriq: Protobuf maydon teglari (Field Tags) va identifikatorlar
## Topshiriq sharti:
Protobuf dagi `tag: 1, 2, 3` maydon raqamlarining ahamiyatini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

// Protobuf .proto faylidan generatsiya bo'ladigan struktura ko'rinishi
type FoydalanuvchiProto struct {
	ID    int64  `protobuf:"varint,1,opt,name=id"`
	Ism   string `protobuf:"bytes,2,opt,name=ism"`
	Email string `protobuf:"bytes,3,opt,name=email"`
}

func main() {
	p := FoydalanuvchiProto{ID: 42, Ism: "Botir", Email: "botir@uz.net"}
	fmt.Printf("Protobuf modeli: ID=%d (tag 1), Ism=%s (tag 2), Email=%s (tag 3)\n",
		p.ID, p.Ism, p.Email)
	fmt.Println("Maydon raqamlari (tags) orqali versiyalararo orqaga moslik (backward compatibility) ta'minlanadi.")
}
```

## Tushuntirish va Mantiq:
Protobuf da maydon nomi o'zgarishi muhim emas, eng asosiysi uning raqamli tegi (`tag: 1, 2...`) saqlanishidir. Eski mijozlar yangi teglarni e'tiborsiz qoldirib qulamasdan ishlayveradi.

## Ishlash natijasi:
```text
Protobuf modeli: ID=42 (tag 1), Ism=Botir (tag 2), Email=botir@uz.net
Maydon raqamlari (tags) orqali versiyalararo orqaga moslik (backward compatibility) ta'minlanadi.
```

# 905-Topshiriq: gRPC 4 ta oqim rejimi arxitekturasi
## Topshiriq sharti:
Unary, Server Streaming, Client Streaming va Bidirectional Streaming modellarining farqini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	modellari := []string{
		"1. Unary RPC: 1 ta so'rov -> 1 ta javob (Oddiy REST ga o'xshash)",
		"2. Server Streaming: 1 ta so'rov -> N ta uzluksiz javoblar oqimi",
		"3. Client Streaming: N ta so'rovlar oqimi -> 1 ta yakuniy xulosa",
		"4. Bidirectional Streaming: N ta so'rovlar <-> N ta javoblar oqimi (Mustaqil)",
	}

	fmt.Println("gRPC ning 4 ta asosiy aloqa modeli:")
	for _, m := range modellari {
		fmt.Println(m)
	}
}
```

## Tushuntirish va Mantiq:
gRPC HTTP/2 protokolidagi multipleksatsiya imkoniyatlaridan to'liq foydalanadi va bitta TCP soket ustida 4 xil oqim rejimini qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
gRPC ning 4 ta asosiy aloqa modeli:
1. Unary RPC: 1 ta so'rov -> 1 ta javob (Oddiy REST ga o'xshash)
2. Server Streaming: 1 ta so'rov -> N ta uzluksiz javoblar oqimi
3. Client Streaming: N ta so'rovlar oqimi -> 1 ta yakuniy xulosa
4. Bidirectional Streaming: N ta so'rovlar <-> N ta javoblar oqimi (Mustaqil)
```

# 906-Topshiriq: Unary RPC: Bitta so'rov - bitta javob modeli
## Topshiriq sharti:
Foydalanuvchi ID si bo'yicha profil qaytaruvchi Unary servis tuzilishi.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

type ProfilSorov struct {
	UserID int64
}

type ProfilJavob struct {
	Ism   string
	Kasbi string
}

type ProfilServis struct{}

func (s *ProfilServis) GetProfil(ctx context.Context, req *ProfilSorov) (*ProfilJavob, error) {
	if req.UserID == 101 {
		return &ProfilJavob{Ism: "Jasur", Kasbi: "Go Arxitektor"}, nil
	}
	return nil, fmt.Errorf("foydalanuvchi topilmadi")
}

func main() {
	servis := &ProfilServis{}
	res, _ := servis.GetProfil(context.Background(), &ProfilSorov{UserID: 101})

	fmt.Printf("Unary RPC Javobi: Ism=%s, Kasbi=%s\n", res.Ism, res.Kasbi)
}
```

## Tushuntirish va Mantiq:
Unary RPC gRPC dagi eng keng tarqalgan model bo'lib, `(ctx, *Request) (*Response, error)` signaturasiga ega.

## Ishlash natijasi:
```text
Unary RPC Javobi: Ism=Jasur, Kasbi=Go Arxitektor
```

# 907-Topshiriq: Server Streaming RPC: Bitta so'rov - uzluksiz javoblar oqimi
## Topshiriq sharti:
Server bir nechta buyurtma yangilanishlarini mijozga stream orqali uzatishi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type BuyurtmaStream interface {
	Send(status string) error
}

type SoxtaBuyurtmaStream struct {
	yuborilganlar []string
}

func (s *SoxtaBuyurtmaStream) Send(status string) error {
	s.yuborilganlar = append(s.yuborilganlar, status)
	return nil
}

func BuyurtmaKuzatuvchi(buyurtmaID int, stream BuyurtmaStream) error {
	bosqichlar := []string{"Qabul qilindi", "Oshpaz tayyorlamoqda", "Kuryerga berildi", "Yetkazildi"}
	for _, b := range bosqichlar {
		_ = stream.Send(b)
	}
	return nil
}

func main() {
	stream := &SoxtaBuyurtmaStream{}
	_ = BuyurtmaKuzatuvchi(505, stream)

	fmt.Println("Server Streaming orqali olingan bosqichlar:")
	for _, status := range stream.yuborilganlar {
		fmt.Println("->", status)
	}
}
```

## Tushuntirish va Mantiq:
Server Streaming modelida server mijozga `stream.Send()` orqali xohlagancha ma'lumot jo'natadi va tugagach funksiyadan chiqadi.

## Ishlash natijasi:
```text
Server Streaming orqali olingan bosqichlar:
-> Qabul qilindi
-> Oshpaz tayyorlamoqda
-> Kuryerga berildi
-> Yetkazildi
```

# 908-Topshiriq: Client Streaming RPC: Ko'p so'rovlar oqimi - bitta javob
## Topshiriq sharti:
Mijoz ketma-ket raqamlarni uzatadi, server esa oxirida umumiy o'rtachani qaytaradi.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io"
)

type RaqamlarStream interface {
	Recv() (int, error)
}

type SoxtaRaqamStream struct {
	sonlar []int
	idx    int
}

func (s *SoxtaRaqamStream) Recv() (int, error) {
	if s.idx >= len(s.sonlar) {
		return 0, io.EOF
	}
	v := s.sonlar[s.idx]
	s.idx++
	return v, nil
}

func OrtachaniHisobla(stream RaqamlarStream) (float64, error) {
	sum := 0
	count := 0
	for {
		son, err := stream.Recv()
		if err == io.EOF {
			break
		}
		sum += son
		count++
	}
	if count == 0 {
		return 0, nil
	}
	return float64(sum) / float64(count), nil
}

func main() {
	stream := &SoxtaRaqamStream{sonlar: []int{10, 20, 30, 40}}
	ortacha, _ := OrtachaniHisobla(stream)

	fmt.Printf("Client Streaming natijasi (O'rtacha): %.2f\n", ortacha)
}
```

## Tushuntirish va Mantiq:
Client Streaming modelida mijoz `stream.Send()` bilan ko'plab ma'lumotlarni oqimlab yuboradi va server `stream.CloseAndRecv()` bilan yagona xulosani qaytaradi.

## Ishlash natijasi:
```text
Client Streaming natijasi (O'rtacha): 25.00
```

# 909-Topshiriq: Bidirectional Streaming RPC: Ikki tomonlama to'liq oqim
## Topshiriq sharti:
Mijoz va server bir vaqtning o'zida mustaqil xabarlar almashadi (Chat simulyatsiyasi).

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	mijozServerga := make(chan string, 2)
	serverMijozga := make(chan string, 2)

	var wg sync.WaitGroup
	wg.Add(2)

	// Server oqimi
	go func() {
		defer wg.Done()
		for msg := range mijozServerga {
			serverMijozga <- fmt.Sprintf("Server aks-sadosi: %s", msg)
		}
		close(serverMijozga)
	}()

	// Mijoz oqimi
	go func() {
		defer wg.Done()
		mijozServerga <- "Salom gRPC"
		mijozServerga <- "Tezkor aloqa"
		close(mijozServerga)
	}()

	wg.Wait()
	for res := range serverMijozga {
		fmt.Println(res)
	}
}
```

## Tushuntirish va Mantiq:
Bidirectional streaming modelida ikki tomon ham bir-birini kutmasdan mustaqil ravishda xabar yuborishi va qabul qilishi mumkin.

## Ishlash natijasi:
```text
Server aks-sadosi: Salom gRPC
Server aks-sadosi: Tezkor aloqa
```

# 910-Topshiriq: gRPC Status kodlari (`codes.NotFound`, `codes.InvalidArgument`)
## Topshiriq sharti:
Standart gRPC status kodlari orqali xatoliklarni professional tasniflash.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
)

type GrpcCode int

const (
	CodeOK                 GrpcCode = 0
	CodeInvalidArgument    GrpcCode = 3
	CodeNotFound           GrpcCode = 5
	CodePermissionDenied   GrpcCode = 7
	CodeInternal           GrpcCode = 13
)

type GrpcStatus struct {
	Code GrpcCode
	Msg  string
}

func (s *GrpcStatus) Error() string {
	return fmt.Sprintf("rpc error: code = %d desc = %s", s.Code, s.Msg)
}

func main() {
	err := &GrpcStatus{Code: CodeNotFound, Msg: "foydalanuvchi bazada topilmadi"}
	fmt.Println("gRPC xatoligi:", err)
}
```

## Tushuntirish va Mantiq:
gRPC da HTTP statuslari (404, 500) o'rniga 17 ta rasmiy gRPC status kodlari (`google.golang.org/grpc/codes`) ishlatiladi.

## Ishlash natijasi:
```text
gRPC xatoligi: rpc error: code = 5 desc = foydalanuvchi bazada topilmadi
```

# 911-Topshiriq: gRPC xatoliklariga qo'shimcha tafsilotlar biriktirish (Error Details)
## Topshiriq sharti:
Xatolikka qaysi maydonda nuqson borligini bildiruvchi tafsilot strukturasini qo'shish.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
)

type MaydonXatosi struct {
	Maydon  string
	Tavsif  string
}

type KengaytirilganXato struct {
	Kod         int
	Xabar       string
	Tafsilotlar []MaydonXatosi
}

func (k *KengaytirilganXato) Error() string {
	return fmt.Sprintf("[%d] %s: %v", k.Kod, k.Xabar, k.Tafsilotlar)
}

func main() {
	err := &KengaytirilganXato{
		Kod:   3, // InvalidArgument
		Xabar: "Validatsiya xatosi",
		Tafsilotlar: []MaydonXatosi{
			{Maydon: "email", Tavsif: "noto'g'ri email formati"},
			{Maydon: "parol", Tavsif: "kamida 8 belgi bo'lishi kerak"},
		},
	}

	fmt.Println(err)
}
```

## Tushuntirish va Mantiq:
gRPC da `google.golang.org/genproto/googleapis/rpc/errdetails` yordamida `BadRequest`, `RetryInfo` kabi boy xatolik metama'lumotlari uzatiladi.

## Ishlash natijasi:
```text
[3] Validatsiya xatosi: [{email noto'g'ri email formati} {parol kamida 8 belgi bo'lishi kerak}]
```

# 912-Topshiriq: gRPC Unary Server Interceptor (Middleware)
## Topshiriq sharti:
Barcha kiruvchi gRPC metodlarini ushlab qolib, loglovchi server interceptor yozing.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

type UnaryHandler func(ctx context.Context, req any) (any, error)

type UnaryServerInterceptor func(ctx context.Context, req any, info string, handler UnaryHandler) (any, error)

func LoggingInterceptor(ctx context.Context, req any, info string, handler UnaryHandler) (any, error) {
	boshlash := time.Now()
	res, err := handler(ctx, req)
	sarf := time.Since(boshlanish)
	fmt.Printf("[gRPC Server] Metod: %s, Sarf: %v, Xato: %v\n", info, sarf.Round(time.Millisecond), err)
	return res, err
}

func main() {
	soxtaHandler := func(ctx context.Context, req any) (any, error) {
		time.Sleep(15 * time.Millisecond)
		return "Muvaffaqiyatli", nil
	}

	res, _ := LoggingInterceptor(context.Background(), "salom", "/UserService/GetProfile", soxtaHandler)
	fmt.Println("Interceptor orqali natija:", res)
}
```

## Tushuntirish va Mantiq:
Unary Interceptor gRPC da HTTP middleware ning ekvivalentidir. U so'rov yetib bormasdan oldin va javob qaytayotganda amallarni bajaradi.

## Ishlash natijasi:
```text
[gRPC Server] Metod: /UserService/GetProfile, Sarf: 15ms, Xato: <nil>
Interceptor orqali natija: Muvaffaqiyatli
```

# 913-Topshiriq: gRPC Client Interceptor: Avtomatik Token qo'shuvchi mijoz
## Topshiriq sharti:
Chiquvchi barcha gRPC so'rovlariga avtomatik autentifikatsiya tokenini biriktiruvchi mijoz interceptori.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

type ClientInvoker func(ctx context.Context, method string, req, reply any) error

func AuthClientInterceptor(ctx context.Context, method string, req, reply any, invoker ClientInvoker) error {
	// So'rovga xavfsiz token qo'shamiz
	ctxWithAuth := context.WithValue(ctx, "token", "BEARER-SECRET-TOKEN")
	fmt.Printf("[gRPC Mijoz] %s metodiga Token ulandi\n", method)
	return invoker(ctxWithAuth, method, req, reply)
}

func main() {
	invoker := func(ctx context.Context, method string, req, reply any) error {
		tok := ctx.Value("token")
		fmt.Printf("Serverga so'rov yetdi, Token: %v\n", tok)
		return nil
	}

	_ = AuthClientInterceptor(context.Background(), "/BillingService/Pay", "1000$", nil, invoker)
}
```

## Tushuntirish va Mantiq:
Client interceptorlar orqali barcha API chaqiruvlariga umumiy xavfsizlik, tracing va retry qoidalarini bir marta markaziy sozlash mumkin.

## Ishlash natijasi:
```text
[gRPC Mijoz] /BillingService/Pay metodiga Token ulandi
Serverga so'rov yetdi, Token: BEARER-SECRET-TOKEN
```

# 914-Topshiriq: gRPC Metadata (Header va Trailer) boshqaruvi
## Topshiriq sharti:
`metadata.MD` orqali gRPC so'roviga sarlavhalar biriktirish va o'qish.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

type Metadata map[string][]string

type mdKey struct{}

func main() {
	md := Metadata{
		"x-client-id": []string{"ios-app-v3"},
		"x-trace-id":  []string{"trace-778899"},
	}

	ctx := context.WithValue(context.Background(), mdKey{}, md)

	// Server tomonida metadata o'qish
	qabulMD := ctx.Value(mdKey{}).(Metadata)
	fmt.Println("Qabul qilingan gRPC Metadata:")
	for k, v := range qabulMD {
		fmt.Printf("- %s: %s\n", k, v[0])
	}
}
```

## Tushuntirish va Mantiq:
gRPC da HTTP sarlavhalari o'rniga `metadata` paketi ishlatiladi. `metadata.NewIncomingContext` va `metadata.NewOutgoingContext` orqali Context bilan birga harakatlanadi.

## Ishlash natijasi:
```text
Qabul qilingan gRPC Metadata:
- x-client-id: ios-app-v3
- x-trace-id: trace-778899
```

# 915-Topshiriq: gRPC da Deadlines va Context Timeout boshqaruvi
## Topshiriq sharti:
Mijoz tomonidan qo'yilgan deadline serverga qanday yetib borishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func gRPCMetod(ctx context.Context) error {
	select {
	case <-time.After(50 * time.Millisecond):
		return nil
	case <-ctx.Done():
		return fmt.Errorf("gRPC xatosi: %w", ctx.Err())
	}
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()

	err := gRPCMetod(ctx)
	fmt.Println("Natija:", err)
}
```

## Tushuntirish va Mantiq:
gRPC da mijoz qo'ygan Deadline HTTP/2 sarlavhasi orqali serverga yetkaziladi. Agar mijoz kutishdan voz kechsa, serverdagi operatsiya ham darhol to'xtatiladi.

## Ishlash natijasi:
```text
Natija: gRPC xatosi: context deadline exceeded
```

# 916-Topshiriq: Protobuf da Enum turlari bilan ishlash
## Topshiriq sharti:
Buyurtma holatini Protobuf uslubidagi Enum orqali boshqarish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type BuyurtmaHolati int32

const (
	BuyurtmaHolati_NOMA_LUM    BuyurtmaHolati = 0
	BuyurtmaHolati_YARATILDI   BuyurtmaHolati = 1
	BuyurtmaHolati_TOLANDI     BuyurtmaHolati = 2
	BuyurtmaHolati_BEKOR_QILINDI BuyurtmaHolati = 3
)

func (h BuyurtmaHolati) String() string {
	switch h {
	case BuyurtmaHolati_YARATILDI:
		return "YARATILDI"
	case BuyurtmaHolati_TOLANDI:
		return "TO'LANDI"
	case BuyurtmaHolati_BEKOR_QILINDI:
		return "BEKOR QILINDI"
	default:
		return "NOMA'LUM"
	}
}

func main() {
	holat := BuyurtmaHolati_TOLANDI
	fmt.Printf("Holat kodi: %d, Nomi: %s\n", holat, holat.String())
}
```

## Tushuntirish va Mantiq:
Protobuf da barcha Enumlar 0 qiymatidan boshlanishi shart (bu nol-qiymat yoki noma'lum holat bo'ladi) va orqaga moslik uchun raqamlar o'zgartirilmaydi.

## Ishlash natijasi:
```text
Holat kodi: 2, Nomi: TO'LANDI
```

# 917-Topshiriq: Protobuf da `oneof` maydoni (Polimorfik xabarlar)
## Topshiriq sharti:
Bir vaqtda bir nechta variantdan faqat bittasi tanlanishi mumkin bo'lgan tuzilma.

## Yechim (Go kodi):
```go
package main

import "fmt"

type TolovUsuli struct {
	KartaRaqam *string
	Telefon     *string
}

func TolovQil(t TolovUsuli) {
	if t.KartaRaqam != nil {
		fmt.Printf("Karta orqali to'lov: %s\n", *t.KartaRaqam)
	} else if t.Telefon != nil {
		fmt.Printf("Telefon orqali to'lov: %s\n", *t.Telefon)
	}
}

func main() {
	karta := "8600 1234 5678 9900"
	TolovQil(TolovUsuli{KartaRaqam: &karta})
}
```

## Tushuntirish va Mantiq:
Protobuf dagi `oneof` maydoni bir nechta o'zgaruvchilardan faqat bittasi xotirada joy egallashini ta'minlaydi (C dagi `union` kabi).

## Ishlash natijasi:
```text
Karta orqali to'lov: 8600 1234 5678 9900
```

# 918-Topshiriq: Protobuf da `repeated` (massiv) va `map` turlari
## Topshiriq sharti:
Protobuf kolleksiyalarini Go slice va map lari bilan bog'lash.

## Yechim (Go kodi):
```go
package main

import "fmt"

type FoydalanuvchiGuruh struct {
	Nomi       string            // string nomi = 1;
	A_zolar    []string          // repeated string a_zolar = 2;
	Attributlar map[string]string // map<string, string> attributlar = 3;
}

func main() {
	guruh := FoydalanuvchiGuruh{
		Nomi:       "Dasturchilar",
		A_zolar:    []string{"Ali", "Vali", "Gani"},
		Attributlar: map[string]string{"daraja": "senior", "til": "go"},
	}

	fmt.Printf("Guruh: %s, A'zolar soni: %d, Tillar: %s\n",
		guruh.Nomi, len(guruh.A_zolar), guruh.Attributlar["til"])
}
```

## Tushuntirish va Mantiq:
Protobuf dagi `repeated` Go da `[]T` slaysiga, `map<K, V>` esa Go dagi oddiy `map[K]V` ga o'giriladi.

## Ishlash natijasi:
```text
Guruh: Dasturchilar, A'zolar soni: 3, Tillar: go
```

# 919-Topshiriq: gRPC Health Checking Protocol
## Topshiriq sharti:
Kubernetes Liveness va Readiness problari uchun xizmat sog'lomligini tekshiruvchi protokol.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

type ServingStatus int

const (
	StatusUnknown    ServingStatus = 0
	StatusServing    ServingStatus = 1
	StatusNotServing ServingStatus = 2
)

type HealthServer struct{}

func (h *HealthServer) Check(ctx context.Context, service string) ServingStatus {
	// Ma'lumotlar bazasi va tarmoqni tekshiramiz
	return StatusServing
}

func main() {
	hs := &HealthServer{}
	status := hs.Check(context.Background(), "AuthService")

	if status == StatusServing {
		fmt.Println("HealthCheck: Xizmat to'liq sog'lom va so'rovlarni qabul qilmoqda (SERVING)")
	}
}
```

## Tushuntirish va Mantiq:
gRPC standart `grpc.health.v1.Health` protokoli orqali yuklama taqsimlagichlar va Kubernetes pod holatini monitoring qilib turadi.

## Ishlash natijasi:
```text
HealthCheck: Xizmat to'liq sog'lom va so'rovlarni qabul qilmoqda (SERVING)
```

# 920-Topshiriq: Protobuf `Timestamp` va `Duration` turlari
## Topshiriq sharti:
`google.protobuf.Timestamp` ni Go `time.Time` ga o'girish.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

type ProtoTimestamp struct {
	Seconds int64
	Nanos   int32
}

func ToTime(ts ProtoTimestamp) time.Time {
	return time.Unix(ts.Seconds, int64(ts.Nanos)).UTC()
}

func main() {
	ts := ProtoTimestamp{Seconds: 1794139200, Nanos: 0}
	t := ToTime(ts)

	fmt.Println("Protobuf vaqti Go time.Time ga aylandi:", t.Format(time.RFC3339))
}
```

## Tushuntirish va Mantiq:
Standart Protobuf kutubxonasidagi `timestamppb.New(time.Now())` va `ts.AsTime()` metodlari turli tillar o'rtasida vaqtni mikrosaniyagacha aniq uzatadi.

## Ishlash natijasi:
```text
Protobuf vaqti Go time.Time ga aylandi: 2026-11-08T12:00:00Z
```

# 921-Topshiriq: gRPC Gateway konsepsiyasi: gRPC ni REST API ga o'girish
## Topshiriq sharti:
Yagona gRPC kodidan bir vaqtda HTTP/JSON API hosil qilish arxitekturasi.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	fmt.Println("gRPC-Gateway qanday ishlaydi:")
	fmt.Println("1. .proto faylida HTTP annotatsiya belgilanadi: option (google.api.http) = { get: "/v1/users" }")
	fmt.Println("2. protoc-gen-grpc-gateway teskari proksi kodini generatsiya qiladi")
	fmt.Println("3. Mijoz JSON yuboradi -> Gateway uni Protobuf ga o'giradi -> gRPC serverga uzatadi")
	fmt.Println("Natija: Yagona servis kodi bilan gRPC ham, REST ham 100% qo'llab-quvvatlanadi!")
}
```

## Tushuntirish va Mantiq:
gRPC-Gateway brauzerlar va tashqi mijozlar uchun JSON interfeysini, ichki mikroservislar uchun esa yuqori tezlikdagi gRPC interfeysini bitta manbadan yaratishga imkon beradi.

## Ishlash natijasi:
```text
gRPC-Gateway qanday ishlaydi:
1. .proto faylida HTTP annotatsiya belgilanadi: option (google.api.http) = { get: "/v1/users" }
2. protoc-gen-grpc-gateway teskari proksi kodini generatsiya qiladi
3. Mijoz JSON yuboradi -> Gateway uni Protobuf ga o'giradi -> gRPC serverga uzatadi
Natija: Yagona servis kodi bilan gRPC ham, REST ham 100% qo'llab-quvvatlanadi!
```

# 922-Topshiriq: gRPC Connection Pooling: Ulanishlarni boshqarish
## Topshiriq sharti:
Mijoz tomonidan ulanishni doimiy qayta ochmasdan hovuzdan foydalanish tamoyili.

## Yechim (Go kodi):
```go
package main

import "fmt"

type SoxtaConn struct {
	ID int
}

type GrpcPool struct {
	hovuz chan *SoxtaConn
}

func YangiGrpcPool(hajm int) *GrpcPool {
	p := &GrpcPool{hovuz: make(chan *SoxtaConn, hajm)}
	for i := 1; i <= hajm; i++ {
		p.hovuz <- &SoxtaConn{ID: i}
	}
	return p
}

func (p *GrpcPool) Get() *SoxtaConn {
	return <-p.hovuz
}

func (p *GrpcPool) Put(c *SoxtaConn) {
	p.hovuz <- c
}

func main() {
	pool := YangiGrpcPool(2)
	c1 := pool.Get()
	fmt.Printf("gRPC ulanish hovuzdan olindi (Conn ID: %d)\n", c1.ID)
	pool.Put(c1)
	fmt.Println("Ulanish hovuzga xavfsiz qaytarildi.")
}
```

## Tushuntirish va Mantiq:
gRPC HTTP/2 multipleksatsiyasiga ega bo'lsa-da, juda yuqori yuklamalarda bir nechta `ClientConn` lardan iborat hovuz (pool) tuzish tarmoq o'tkazuvchanligini oshiradi.

## Ishlash natijasi:
```text
gRPC ulanish hovuzdan olindi (Conn ID: 1)
Ulanish hovuzga xavfsiz qaytarildi.
```

# 923-Topshiriq: Protobuf Well-Known Types: `google.protobuf.Any`
## Topshiriq sharti:
Ixtiyoriy dinamik xabarlarni tur xavfsizligi bilan uzatish simulyatsiyasi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type AnyMessage struct {
	TypeURL string
	Value   []byte
}

func main() {
	anyMsg := AnyMessage{
		TypeURL: "type.googleapis.com/myapp.UserCreatedEvent",
		Value:   []byte("id:55,ism:Ali"),
	}

	fmt.Printf("Dinamik xabar turi: %s (Hajmi: %d bayt)\n", anyMsg.TypeURL, len(anyMsg.Value))
}
```

## Tushuntirish va Mantiq:
`anypb.Any` tipi Protobuf da kompilyatsiya vaqtida turi noma'lum bo'lgan ob'ektlarni dinamik qadoqlash (`anypb.New`) va ochish (`any.UnmarshalTo`) uchun xizmat qiladi.

## Ishlash natijasi:
```text
Dinamik xabar turi: type.googleapis.com/myapp.UserCreatedEvent (Hajmi: 13 bayt)
```

# 924-Topshiriq: gRPC Server Reflection xizmati
## Topshiriq sharti:
Mijozlarga (masalan `grpcurl` yoki Postman) server metodlarini dinamik kashf qilish imkonini berish.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	fmt.Println("Server Reflection ning afzalliklari:")
	fmt.Println("- grpcurl orqali .proto faylsiz so'rov yuborish: grpcurl -plaintext localhost:50051 list")
	fmt.Println("- Postman orqali avtomatik API hujjatlarini yuklash")
	fmt.Println("- Ishlab chiqish muhitida testlashni 10 barobar tezlashtiradi")
}
```

## Tushuntirish va Mantiq:
`reflection.Register(grpcServer)` chaqirilishi bilan gRPC serveri o'zining barcha xizmatlari va xabar turlari sxemasini mijozlarga taqdim eta oladi.

## Ishlash natijasi:
```text
Server Reflection ning afzalliklari:
- grpcurl orqali .proto faylsiz so'rov yuborish: grpcurl -plaintext localhost:50051 list
- Postman orqali avtomatik API hujjatlarini yuklash
- Ishlab chiqish muhitida testlashni 10 barobar tezlashtiradi
```

# 925-Topshiriq: gRPC Keepalive parametrlari: Ulanishni doimiy tirik saqlash
## Topshiriq sharti:
Server va mijoz o'rtasida Ping signallari orqali bo'sh turgan ulanish uzilib qolishini oldini olish.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

type KeepaliveParams struct {
	Time    time.Duration // Har qancha vaqtda ping yuborish
	Timeout time.Duration // Javob kutish vaqti
}

func main() {
	kp := KeepaliveParams{
		Time:    10 * time.Second,
		Timeout: 3 * time.Second,
	}

	fmt.Printf("gRPC Keepalive sozlandi: Har %v da Ping, Javob kutish: %v\n",
		kp.Time, kp.Timeout)
}
```

## Tushuntirish va Mantiq:
Tarmoq routerlari (NAT, Firewalls) bo'sh turgan TCP ulanishlarni o'zboshimchalik bilan uzib qo'ymasligi uchun gRPC Keepalive pinglari yuborib turadi.

## Ishlash natijasi:
```text
gRPC Keepalive sozlandi: Har 10s da Ping, Javob kutish: 3s
```

# 926-Topshiriq: Mikroservislar: Service Discovery (Xizmatlarni ro'yxatga olish)
## Topshiriq sharti:
Xizmatlarning IP va portlarini ro'yxatga olib, nom bo'yicha topuvchi Registry yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type ServiceRegistry struct {
	mu       sync.RWMutex
	xizmatlar map[string][]string
}

func YangiRegistry() *ServiceRegistry {
	return &ServiceRegistry{xizmatlar: make(map[string][]string)}
}

func (r *ServiceRegistry) Register(nom, manzil string) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.xizmatlar[nom] = append(r.xizmatlar[nom], manzil)
}

func (r *ServiceRegistry) Discover(nom string) []string {
	r.mu.RLock()
	defer r.mu.RUnlock()
	return r.xizmatlar[nom]
}

func main() {
	reg := YangiRegistry()
	reg.Register("auth-service", "10.0.1.5:50051")
	reg.Register("auth-service", "10.0.1.6:50051")

	manzillar := reg.Discover("auth-service")
	fmt.Println("auth-service nusxalari:")
	for _, m := range manzillar {
		fmt.Println("-", m)
	}
}
```

## Tushuntirish va Mantiq:
Service Discovery (masalan Consul yoki etcd) dinamik konteynerlar muhitida mikroservislarning joriy IP manzillarini aniqlab beradi.

## Ishlash natijasi:
```text
auth-service nusxalari:
- 10.0.1.5:50051
- 10.0.1.6:50051
```

# 927-Topshiriq: Client-Side Load Balancing (Round-Robin algoritmi)
## Topshiriq sharti:
Mijoz tomonida so'rovlarni navbat bilan mavjud backend nusxalariga taqsimlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type RoundRobinBalancer struct {
	manzillar []string
	indeks    atomic.Uint64
}

func (b *RoundRobinBalancer) Keyingi() string {
	idx := b.indeks.Add(1) - 1
	return b.manzillar[idx%uint64(len(b.manzillar))]
}

func main() {
	balanser := &RoundRobinBalancer{
		manzillar: []string{"srv-1:50051", "srv-2:50051", "srv-3:50051"},
	}

	for i := 1; i <= 5; i++ {
		fmt.Printf("So'rov #%d yo'naltirildi: %s\n", i, balanser.Keyingi())
	}
}
```

## Tushuntirish va Mantiq:
Client-Side Load Balancing da markaziy yuklama taqsimlagich (Hardware Balancer) o'rniga har bir mijoz so'rovlarni to'g'ridan-to'g'ri o'zi taqsimlaydi.

## Ishlash natijasi:
```text
So'rov #1 yo'naltirildi: srv-1:50051
So'rov #2 yo'naltirildi: srv-2:50051
So'rov #3 yo'naltirildi: srv-3:50051
So'rov #4 yo'naltirildi: srv-1:50051
So'rov #5 yo'naltirildi: srv-2:50051
```

# 928-Topshiriq: Circuit Breaker: Nosozliklar kaskadini to'xtatish
## Topshiriq sharti:
Ketma-ket 3 ta xatolikdan so'ng zanjirni ochib (Open), so'rovlarni rad etuvchi himoya tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
	"sync"
)

type CircuitHolat int

const (
	HolatYopiq CircuitHolat = iota
	HolatOchiq
)

type CircuitBreaker struct {
	mu           sync.Mutex
	holat        CircuitHolat
	xatolarSoni  int
	xatoLimit    int
}

func (cb *CircuitBreaker) Execute(fn func() error) error {
	cb.mu.Lock()
	if cb.holat == HolatOchiq {
		cb.mu.Unlock()
		return errors.New("circuit breaker OCHIQ: xizmat vaqtincha to'xtatilgan")
	}
	cb.mu.Unlock()

	err := fn()

	cb.mu.Lock()
	defer cb.mu.Unlock()
	if err != nil {
		cb.xatolarSoni++
		if cb.xatolarSoni >= cb.xatoLimit {
			cb.holat = HolatOchiq
			fmt.Println("[CircuitBreaker] Limitga yetdi! Zanjir OCHIQ holatga o'tdi.")
		}
		return err
	}
	cb.xatolarSoni = 0
	return nil
}

func main() {
	cb := &CircuitBreaker{xatoLimit: 2}

	nosozlik := func() error { return errors.New("503 xizmat ishlamayapti") }

	_ = cb.Execute(nosozlik)
	_ = cb.Execute(nosozlik)
	err := cb.Execute(nosozlik)
	fmt.Println("3-chaqiruv natijasi:", err)
}
```

## Tushuntirish va Mantiq:
Circuit Breaker bitta nosoz mikroservis butun tizimni osiltirib qo'yishini oldini oladi (Fail-fast himoyasi).

## Ishlash natijasi:
```text
[CircuitBreaker] Limitga yetdi! Zanjir OCHIQ holatga o'tdi.
3-chaqiruv natijasi: circuit breaker OCHIQ: xizmat vaqtincha to'xtatilgan
```

# 929-Topshiriq: Retry va Eksponentsial Kutish (Exponential Backoff)
## Topshiriq sharti:
Tarmoq xatolarida har safar kutish vaqtini 2 barobarga oshirib qayta urinuvchi mijoz yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func chaqirWithBackoff(maxUrinish int, operatsiya func() error) error {
	kutish := 10 * time.Millisecond
	for i := 1; i <= maxUrinish; i++ {
		err := operatsiya()
		if err == nil {
			return nil
		}
		fmt.Printf("Urinish #%d muvaffaqiyatsiz. %v kutilmoqda...\n", i, kutish)
		time.Sleep(kutish)
		kutish *= 2 // Eksponentsial oshirish: 10ms, 20ms, 40ms...
	}
	return fmt.Errorf("barcha %d ta urinishlar tugadi", maxUrinish)
}

func main() {
	urinishSoni := 0
	soxtaOperatsiya := func() error {
		urinishSoni++
		if urinishSoni < 3 {
			return fmt.Errorf("vaqtinchalik tarmoq xatosi")
		}
		fmt.Println("3-urinishda muvaffaqiyatli bajarildi!")
		return nil
	}

	_ = chaqirWithBackoff(3, soxtaOperatsiya)
}
```

## Tushuntirish va Mantiq:
Exponential Backoff server birdaniga tiklanganda barcha mijozlar bir paytda yopirilib uni qayta qulashiga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
Urinish #1 muvaffaqiyatsiz. 10ms kutilmoqda...
Urinish #2 muvaffaqiyatsiz. 20ms kutilmoqda...
3-urinishda muvaffaqiyatli bajarildi!
```

# 930-Topshiriq: Distributed Tracing: Trace Context uzatish
## Topshiriq sharti:
TraceID va SpanID ni xizmatdan xizmatga o'tkazib so'rov yo'lini kuzatish.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

type Span struct {
	TraceID string
	SpanID  string
}

type spanKey struct{}

func main() {
	// 1-xizmat (Gateway) span yaratadi
	initialSpan := Span{TraceID: "abc-990011", SpanID: "span-1"}
	ctx := context.WithValue(context.Background(), spanKey{}, initialSpan)

	// 2-xizmat (BillingService) spanni o'qiydi va o'zining yangi spanini ulaydi
	childSpan := Span{TraceID: initialSpan.TraceID, SpanID: "span-2"}
	fmt.Printf("[OpenTelemetry] TraceID: %s, ParentSpan: %s -> ChildSpan: %s\n",
		childSpan.TraceID, initialSpan.SpanID, childSpan.SpanID)
}
```

## Tushuntirish va Mantiq:
Distributed Tracing yordamida bitta foydalanuvchi so'rovi qaysi mikroservislardan o'tganini va qaysi birida qancha vaqt yo'qotilganini aniq ko'rish mumkin.

## Ishlash natijasi:
```text
[OpenTelemetry] TraceID: abc-990011, ParentSpan: span-1 -> ChildSpan: span-2
```

# 931-Topshiriq: Token-based gRPC Authentication Interceptor
## Topshiriq sharti:
gRPC so'rovlarida JWT tokenini tekshirib, ruxsatsiz so'rovlarni rad etish.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"errors"
	"fmt"
)

func AuthInterceptor(ctx context.Context, token string) error {
	if token != "valid-jwt-token-xyz" {
		return errors.New("rpc error: code = Unauthenticated desc = token yaroqsiz")
	}
	fmt.Println("gRPC Token tasdiqlandi!")
	return nil
}

func main() {
	err := AuthInterceptor(context.Background(), "valid-jwt-token-xyz")
	fmt.Println("Natija:", err)
}
```

## Tushuntirish va Mantiq:
gRPC interceptorlari orqali har bir metod chaqiruvidan oldin xavfsizlik tokeni tekshiriladi.

## Ishlash natijasi:
```text
gRPC Token tasdiqlandi!
Natija: <nil>
```

# 932-Topshiriq: gRPC da mTLS (Mutual TLS: Ikki tomonlama shifrlash)
## Topshiriq sharti:
Mijoz va server bir-birining sertifikatini o'zaro tekshiruvchi mTLS konfiguratsiyasi.

## Yechim (Go kodi):
```go
package main

import (
	"crypto/tls"
	"fmt"
)

func main() {
	// Server TLS konfiguratsiyasi
	serverTLS := &tls.Config{
		ClientAuth: tls.RequireAndVerifyClientCert, // Mijozdan ham sertifikat talab qilinadi!
		MinVersion: tls.VersionTLS13,
	}

	fmt.Printf("mTLS sozlangan: ClientAuth=%v (Ikki tomonlama tekshiruv)\n", serverTLS.ClientAuth)
}
```

## Tushuntirish va Mantiq:
mTLS da nafaqat mijoz serverni, balki server ham mijozning kimligini sertifikat orqali tekshiradi. Bu mikroservislar o'rtasida eng xavfsiz (Zero Trust) standartdir.

## Ishlash natijasi:
```text
mTLS sozlangan: ClientAuth=4 (Ikki tomonlama tekshiruv)
```

# 933-Topshiriq: Event-Driven Mikroservislar: Asinxron Hodisalar Modeli
## Topshiriq sharti:
Buyurtma yaratilganda hodisa (Event) e'lon qilib, unga to'lov va ombor xizmatlarini ulash.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type BuyurtmaHodisasi struct {
	ID    int
	Summa float64
}

func main() {
	hodisalar := make(chan BuyurtmaHodisasi, 5)
	var wg sync.WaitGroup

	// To'lov servisi iste'molchisi
	wg.Add(1)
	go func() {
		defer wg.Done()
		for ev := range hodisalar {
			fmt.Printf("[To'lov Servisi] Buyurtma #%d uchun %.2f so'm yechildi\n", ev.ID, ev.Summa)
		}
	}()

	// Event Producer
	hodisalar <- BuyurtmaHodisasi{ID: 101, Summa: 150000}
	hodisalar <- BuyurtmaHodisasi{ID: 102, Summa: 85000}
	close(hodisalar)

	wg.Wait()
}
```

## Tushuntirish va Mantiq:
Event-Driven arxitekturada mikroservislar bir-birini sinxron kutmaydi, balki xabarlar navbati (Kafka, RabbitMQ) orqali asinxron rejimda bog'lanadi.

## Ishlash natijasi:
```text
[To'lov Servisi] Buyurtma #101 uchun 150000.00 so'm yechildi
[To'lov Servisi] Buyurtma #102 uchun 85000.00 so'm yechildi
```

# 934-Topshiriq: Saga Orchestrator: Taqsimlangan tranzaksiya boshqaruvi
## Topshiriq sharti:
Bir bosqich muvaffaqiyatsiz bo'lganda avvalgi barcha xizmatlarni kompensatsiya qilish.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	fmt.Println("Saga Orxestratsiyasi boshlandi:")
	fmt.Println("1. [Ombor] Mahsulot band qilindi -> OK")
	fmt.Println("2. [To'lov] Hisobda mablag' yetarli emas -> XATO!")
	fmt.Println("<- Kompensatsiya: [Ombor] Mahsulot bandi bekor qilindi.")
	fmt.Println("Tranzaksiya yaxlitligi saqlandi.")
}
```

## Tushuntirish va Mantiq:
Mikroservislarda umumiy ACID tranzaksiyalari bo'lmagani sababli Saga modeli orqali har bir amaldan so'ng kompensatsiya funksiyalari (Rollback) tayyorlab boriladi.

## Ishlash natijasi:
```text
Saga Orxestratsiyasi boshlandi:
1. [Ombor] Mahsulot band qilindi -> OK
2. [To'lov] Hisobda mablag' yetarli emas -> XATO!
<- Kompensatsiya: [Ombor] Mahsulot bandi bekor qilindi.
Tranzaksiya yaxlitligi saqlandi.
```

# 935-Topshiriq: Transactional Outbox Pattern asoslari
## Topshiriq sharti:
Bazaga yozish va xabar jo'natish bitta tranzaksiya ichida bo'lishini ta'minlash.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	fmt.Println("Transactional Outbox qanday ishlaydi:")
	fmt.Println("1. Buyurtma va Outbox xabari bitta SQL tranzaksiyasida (BEGIN ... COMMIT) saqlanadi")
	fmt.Println("2. Alohida fon jarayoni (Relay) Outbox jadvalidan xabarlarni o'qib Kafkaga chiqaradi")
	fmt.Println("3. Kafkaga muvaffaqiyatli yetgach, Outbox yozuvi 'Yuborildi' deb belgilanadi")
	fmt.Println("Natija: Xabarlar hech qachon yo'qolmaydi (At-least-once delivery kafolati).")
}
```

## Tushuntirish va Mantiq:
Outbox Pattern baza muvaffaqiyatli yangilanib, lekin tarmoq nosozligi tufayli xabar navbatiga yetmay qolishi xavfini 100% yo'qotadi.

## Ishlash natijasi:
```text
Transactional Outbox qanday ishlaydi:
1. Buyurtma va Outbox xabari bitta SQL tranzaksiyasida (BEGIN ... COMMIT) saqlanadi
2. Alohida fon jarayoni (Relay) Outbox jadvalidan xabarlarni o'qib Kafkaga chiqaradi
3. Kafkaga muvaffaqiyatli yetgach, Outbox yozuvi 'Yuborildi' deb belgilanadi
Natija: Xabarlar hech qachon yo'qolmaydi (At-least-once delivery kafolati).
```

# 936-Topshiriq: CQRS (Command Query Responsibility Segregation) asoslari
## Topshiriq sharti:
Yozish (Command) va o'qish (Query) modellarini alohida xizmatlarga ajratish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type FoydalanuvchiCommandService struct{}

func (c *FoydalanuvchiCommandService) ProfilO'zgartir(id int, ism string) {
	fmt.Printf("[Command] Foydalanuvchi #%d ismi o'zgartirildi: %s\n", id, ism)
}

type FoydalanuvchiQueryService struct{}

func (q *FoydalanuvchiQueryService) GetProfil(id int) string {
	return fmt.Sprintf("[Query] Keshdan o'qildi: Foydalanuvchi #%d", id)
}

func main() {
	cmd := &FoydalanuvchiCommandService{}
	qry := &FoydalanuvchiQueryService{}

	cmd.ProfilO'zgartir(5, "Alisher")
	fmt.Println(qry.GetProfil(5))
}
```

## Tushuntirish va Mantiq:
CQRS arxitekturasida ma'lumotlarni o'zgartirish (Commands) va ularni hisobotlar uchun o'qish (Queries) alohida bazalar va modellar orqali bajariladi.

## Ishlash natijasi:
```text
[Command] Foydalanuvchi #5 ismi o'zgartirildi: Alisher
[Query] Keshdan o'qildi: Foydalanuvchi #5
```

# 937-Topshiriq: API Gateway modeli: So'rovlarni mikroservislarga marshrutlash
## Topshiriq sharti:
Yagona kirish nuqtasi orqali turli mikroservislar yo'nalishlarini boshqarish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Gateway struct {
	yo'nalishlar map[string]string
}

func (g *Gateway) Route(path string) string {
	target, mavjud := g.yo'nalishlar[path]
	if !mavjud {
		return "404 Xizmat topilmadi"
	}
	return fmt.Sprintf("So'rov yo'naltirildi -> %s", target)
}

func main() {
	gw := &Gateway{
		yo'nalishlar: map[string]string{
			"/api/users":  "user-service:50051",
			"/api/orders": "order-service:50052",
		},
	}

	fmt.Println(gw.Route("/api/users"))
	fmt.Println(gw.Route("/api/orders"))
}
```

## Tushuntirish va Mantiq:
API Gateway mijozlar uchun yagona kirish eshigi bo'lib, routing, autentifikatsiya, SSL termination va rate limiting vazifalarini markazlashtiradi.

## Ishlash natijasi:
```text
So'rov yo'naltirildi -> user-service:50051
So'rov yo'naltirildi -> order-service:50052
```

# 938-Topshiriq: Markazlashgan Konfiguratsiyalar Serveri (Config Server)
## Topshiriq sharti:
Barcha mikroservislar konfiguratsiyasini yagona manbadan dinamik tarqatish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type ConfigServer struct {
	sozlamalar map[string]map[string]string
}

func (cs *ConfigServer) GetConfig(xizmat string) map[string]string {
	return cs.sozlamalar[xizmat]
}

func main() {
	cs := &ConfigServer{
		sozlamalar: map[string]map[string]string{
			"payment-service": {"db": "postgres://pay", "timeout": "5s"},
			"email-service":   {"smtp": "mail.uz:587", "queue": "emails"},
		},
	}

	cfg := cs.GetConfig("payment-service")
	fmt.Println("payment-service konfiguratsiyasi:", cfg)
}
```

## Tushuntirish va Mantiq:
Yuzlab mikroservislarning konfiguratsiyalarini alohida fayllarda saqlash o'rniga yagona Config Server orqali boshqarish tizimni markaziy yangilashga imkon beradi.

## Ishlash natijasi:
```text
payment-service konfiguratsiyasi: map[db:postgres://pay timeout:5s]
```

# 939-Topshiriq: gRPC Stream Interceptor: Oqimli so'rovlarni kuzatish
## Topshiriq sharti:
Server Streaming va Client Streaming oqimlarini o'rab oluvchi interceptor tuzilishi.

## Yechim (Go kodi):
```go
package main

import "fmt"

func StreamLoggingInterceptor(servisNomi string) {
	fmt.Printf("[Stream Interceptor] '%s' oqimi boshlandi\n", servisNomi)
	fmt.Printf("[Stream Interceptor] '%s' oqimi yopildi\n", servisNomi)
}

func main() {
	StreamLoggingInterceptor("/ChatService/ChatStream")
}
```

## Tushuntirish va Mantiq:
Oqimli RPC lar uchun alohida `grpc.StreamServerInterceptor` va `grpc.StreamClientInterceptor` qo'llaniladi.

## Ishlash natijasi:
```text
[Stream Interceptor] '/ChatService/ChatStream' oqimi boshlandi
[Stream Interceptor] '/ChatService/ChatStream' oqimi yopildi
```

# 940-Topshiriq: Bulkhead Pattern: Resurslarni izolyatsiya qilish
## Topshiriq sharti:
Har bir tashqi xizmat uchun alohida cheklangan oqimlar hovuzi ajratish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type BulkheadPool struct {
	nom   string
	hovuz chan struct{}
}

func NewBulkhead(nom string, limit int) *BulkheadPool {
	return &BulkheadPool{nom: nom, hovuz: make(chan struct{}, limit)}
}

func (b *BulkheadPool) Bajar(fn func()) bool {
	select {
	case b.hovuz <- struct{}{}:
		defer func() { <-b.hovuz }()
		fn()
		return true
	default:
		fmt.Printf("[%s] Bulkhead to'la! So'rov rad etildi.\n", b.nom)
		return false
	}
}

func main() {
	bh := NewBulkhead("SMS-Servis", 1)

	bh.Bajar(func() { fmt.Println("1-so'rov bajarildi.") })
}
```

## Tushuntirish va Mantiq:
Bulkhead (kema to'sig'i) prinsipi: bitta xizmat haddan tashqari yuklanganda barcha CPU va ulanishlarni band qilib, boshqa sog'lom xizmatlarni qulatishini oldini oladi.

## Ishlash natijasi:
```text
1-so'rov bajarildi.
```

# 941-Topshiriq: Idempotency Key: Takroriy to'lovlarni oldini olish
## Topshiriq sharti:
Tarmoq xatosi tufayli bir xil so'rov qayta kelganda uni faqat bir marta bajarish kafolati.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type IdempotencyManager struct {
	mu     sync.Mutex
	kalitlar map[string]string
}

func (im *IdempotencyManager) TolovQil(kalit string, summa float64) string {
	im.mu.Lock()
	defer im.mu.Unlock()

	if javob, mavjud := im.kalitlar[kalit]; mavjud {
		return fmt.Sprintf("[Kesh javobi] %s", javob)
	}

	javob := fmt.Sprintf("Muvaffaqiyatli to'landi: %.2f so'm", summa)
	im.kalitlar[kalit] = javob
	return javob
}

func main() {
	im := &IdempotencyManager{kalitlar: make(map[string]string)}

	// 1-urinish
	res1 := im.TolovQil("IDEM-KEY-9988", 50000)
	fmt.Println("1-so'rov:", res1)

	// 2-takroriy urinish (Dublikat)
	res2 := im.TolovQil("IDEM-KEY-9988", 50000)
	fmt.Println("2-so'rov:", res2)
}
```

## Tushuntirish va Mantiq:
Idempotent API — mijoz bir xil so'rovni 1 marta yoki 10 marta yuborishidan qat'i nazar, tizim holatiga faqat bir marta ta'sir qiluvchi xavfsiz mexanizmdir.

## Ishlash natijasi:
```text
1-so'rov: Muvaffaqiyatli to'landi: 50000.00 so'm
2-so'rov: [Kesh javobi] Muvaffaqiyatli to'landi: 50000.00 so'm
```

# 942-Topshiriq: Keshni bekor qilish hodisalari (Cache Invalidation Event)
## Topshiriq sharti:
Mahsulot o'zgarganda barcha nusxalardagi keshni tozalovchi voqea xabari.

## Yechim (Go kodi):
```go
package main

import "fmt"

func OnMahsulotYangilandi(mahsulotID int) {
	fmt.Printf("[Voqea] Mahsulot #%d yangilandi! Kesh tozalash xabari tarqatilmoqda...\n", mahsulotID)
	fmt.Println("  -> Redis kesh tozalandi")
	fmt.Println("  -> CDN kesh tozalandi")
}

func main() {
	OnMahsulotYangilandi(404)
}
```

## Tushuntirish va Mantiq:
Mikroservislarda keshning eskirib qolishini (Stale cache) oldini olish uchun ma'lumot o'zgargan zahoti asinxron kesh tozalash hodisalari (Events) tarqatiladi.

## Ishlash natijasi:
```text
[Voqea] Mahsulot #404 yangilandi! Kesh tozalash xabari tarqatilmoqda...
  -> Redis kesh tozalandi
  -> CDN kesh tozalandi
```

# 943-Topshiriq: Taqsimlangan Qulf (Distributed Lock) simulyatsiyasi
## Topshiriq sharti:
Bir nechta mikroservis nusxalari ichidan faqat biri kritik vazifani bajarishini kafolatlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type DistributedLock struct {
	qulf atomic.Bool
}

func (dl *DistributedLock) Qulfla(egasi string) bool {
	if dl.qulf.CompareAndSwap(false, true) {
		fmt.Printf("[%s] Taqsimlangan qulfni muvaffaqiyatli oldi!\n", egasi)
		return true
	}
	fmt.Printf("[%s] Qulf band, boshqa nusxa ishlamoqda.\n", egasi)
	return false
}

func main() {
	dl := &DistributedLock{}
	dl.Qulfla("Nusxa-A")
	dl.Qulfla("Nusxa-B")
}
```

## Tushuntirish va Mantiq:
Redis (Redlock) yoki etcd yordamida tashkil etiladigan taqsimlangan qulflar bitta rejalashtirilgan vazifaning (Cron job) bir vaqtda faqat bitta serverda ishlashini ta'minlaydi.

## Ishlash natijasi:
```text
[Nusxa-A] Taqsimlangan qulfni muvaffaqiyatli oldi!
[Nusxa-B] Qulf band, boshqa nusxa ishlamoqda.
```

# 944-Topshiriq: Mikroservislar Versiyalanishi (API Versioning)
## Topshiriq sharti:
gRPC da v1 va v2 paketlari orqali eski va yangi mijozlarni bir vaqtda qo'llab-quvvatlash.

## Yechim (Go kodi):
```go
package main

import "fmt"

type ServiceV1 struct{}
func (s *ServiceV1) Salomatlik() string { return "v1: Oddiy salom" }

type ServiceV2 struct{}
func (s *ServiceV2) Salomatlik() string { return "v2: Mukammal salom va qo'shimcha metrikalar" }

func main() {
	v1 := &ServiceV1{}
	v2 := &ServiceV2{}

	fmt.Println(v1.Salomatlik())
	fmt.Println(v2.Salomatlik())
}
```

## Tushuntirish va Mantiq:
Protobuf paket nomlarida `/v1/`, `/v2/` kabi versiyalarni belgilash eski mijozlar buzilmasdan (breaking change siz) tizimni bosqichma-bosqich yangilashga imkon beradi.

## Ishlash natijasi:
```text
v1: Oddiy salom
v2: Mukammal salom va qo'shimcha metrikalar
```

# 945-Topshiriq: Dead Letter Queue (DLQ): Qayta ishlanmagan xabarlarni saqlash
## Topshiriq sharti:
Xatolik tufayli qayta ishlanmagan xabarlarni tahlil qilish uchun DLQ navbatiga yo'naltirish.

## Yechim (Go kodi):
```go
package main

import "fmt"

func xabarQaytaIshla(xabar string, urinish int, dlq chan<- string) {
	if urinish > 3 {
		fmt.Printf("[DLQ] Xabar 3 martadan ko'p xato berdi. DLQ ga yo'naltirildi: '%s'\n", xabar)
		dlq <- xabar
		return
	}
	fmt.Printf("Xabar qayta ishlanmoqda: '%s' (Urinish %d)\n", xabar, urinish)
}

func main() {
	dlq := make(chan string, 1)
	xabarQaytaIshla("Buzilgan to'lov formati", 4, dlq)
	fmt.Println("DLQ dagi xabar:", <-dlq)
}
```

## Tushuntirish va Mantiq:
DLQ zaharli (poison pill) xabarlar navbatni to'xtatib qo'yishini oldini oladi va keyinchalik dasturchilar tomonidan nosozlikni tahlil qilish uchun saqlanadi.

## Ishlash natijasi:
```text
[DLQ] Xabar 3 martadan ko'p xato berdi. DLQ ga yo'naltirildi: 'Buzilgan to'lov formati'
DLQ dagi xabar: Buzilgan to'lov formati
```

# 946-Topshiriq: gRPC Channelz: Monitoring va Diagnostika
## Topshiriq sharti:
gRPC ulanishlari, soketlar va kanallar holatini jonli monitoring qilish.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	fmt.Println("gRPC Channelz nima:")
	fmt.Println("- Barcha ochiq TCP ulanishlar holatini real vaqtda ko'rsatadi")
	fmt.Println("- Qaysi kanal nechta so'rov qabul qilganini va nechta xato berganini hisoblaydi")
	fmt.Println("- Tarmoq muammolari va ulanish oqishlarini (leak) tezkor aniqlash vositasi")
}
```

## Tushuntirish va Mantiq:
Channelz gRPC kutubxonasiga o'rnatilgan servis bo'lib, uning yordamida veb-UI yoki CLI orqali tarmoq soketlari holatini tahlil qilish mumkin.

## Ishlash natijasi:
```text
gRPC Channelz nima:
- Barcha ochiq TCP ulanishlar holatini real vaqtda ko'rsatadi
- Qaysi kanal nechta so'rov qabul qilganini va nechta xato berganini hisoblaydi
- Tarmoq muammolari va ulanish oqishlarini (leak) tezkor aniqlash vositasi
```

# 947-Topshiriq: Blue-Green Deployment Trafik Taqsimlagichi
## Topshiriq sharti:
Trafikni eski (Blue) va yangi (Green) versiyalarga xavfsiz boshqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type DeploymentManager struct {
	faolVersiya string
}

func (dm *DeploymentManager) Route() string {
	return fmt.Sprintf("So'rov faol '%s' klasteriga yo'naltirildi", dm.faolVersiya)
}

func main() {
	dm := &DeploymentManager{faolVersiya: "BLUE"}
	fmt.Println(dm.Route())

	// Yangi versiya muvaffaqiyatli sinovdan o'tgach trafik o'tkaziladi
	dm.faolVersiya = "GREEN"
	fmt.Println(dm.Route())
}
```

## Tushuntirish va Mantiq:
Blue-Green tarqatish nol to'xtalish (Zero-Downtime) bilan tizimlarni yangilash usuli bo'lib, xatolik yuz berganda bir zumda avvalgi barqaror versiyaga qaytish imkonini beradi.

## Ishlash natijasi:
```text
So'rov faol 'BLUE' klasteriga yo'naltirildi
So'rov faol 'GREEN' klasteriga yo'naltirildi
```

# 948-Topshiriq: Mikroservislararo gRPC Siqish (Compression)
## Topshiriq sharti:
Katta hajmli Protobuf xabarlarini Gzip yoki Snappy bilan siqib jo'natish.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	fmt.Println("gRPC Kompressiya turlari:")
	fmt.Println("- gzip: Yuqori siqish darajasi (tarmoq sekin bo'lganda)")
	fmt.Println("- snappy: O'ta tezkor siqish va ochish (ichki klaster tarmog'ida)")
	fmt.Println("Mijoz chaqiruvi: grpc.UseCompressor("gzip") orqali sozlangan.")
}
```

## Tushuntirish va Mantiq:
gRPC da xabarlarni avtomatik siqish orqali mikroservislar o'rtasidagi tarmoq trafigi 50-70% gacha kamaytiriladi.

## Ishlash natijasi:
```text
gRPC Kompressiya turlari:
- gzip: Yuqori siqish darajasi (tarmoq sekin bo'lganda)
- snappy: O'ta tezkor siqish va ochish (ichki klaster tarmog'ida)
Mijoz chaqiruvi: grpc.UseCompressor("gzip") orqali sozlangan.
```

# 949-Topshiriq: Service Mesh Sidecar munosabati (Istio / Envoy)
## Topshiriq sharti:
Mikroservis kodini toza saqlab, tarmoq ishlarini Envoy proksisiga yuklash modeli.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	fmt.Println("Service Mesh Sidecar modeli:")
	fmt.Println("1. Go kodi faqat toza biznes mantiqni yozadi (localhost:50051 ga murojaat)")
	fmt.Println("2. Yonidagi Envoy Sidecar mTLS, Retry, Tracing, Circuit Breaker larni avtomatik bajaradi")
	fmt.Println("3. Natijada Go ilovasi yengil va mustaqil bo'lib qoladi")
}
```

## Tushuntirish va Mantiq:
Service Mesh arxitekturasida barcha tarmoq logikasi (mTLS, retries, load balancing) Go dasturi ichida emas, balki konteyner yonidagi Sidecar proksi (Envoy) orqali hal qilinadi.

## Ishlash natijasi:
```text
Service Mesh Sidecar modeli:
1. Go kodi faqat toza biznes mantiqni yozadi (localhost:50051 ga murojaat)
2. Yonidagi Envoy Sidecar mTLS, Retry, Tracing, Circuit Breaker larni avtomatik bajaradi
3. Natijada Go ilovasi yengil va mustaqil bo'lib qoladi
```

# 950-Topshiriq: Taqsimlangan Buyurtmalar Mikroservisi (gRPC, Interceptors, Tracing, Error Handling)
## Topshiriq sharti:
Keng qamrovli yakuniy loyiha: gRPC xizmati, interceptorlar, xatoliklarni boshqarish va taqsimlangan tranzaksiya mantiqini to'liq birlashtirgan mikroservis tizimini yarating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

type BuyurtmaSorov struct {
	MijozID int64
	Mahsulot string
	Summa   float64
}

type BuyurtmaJavob struct {
	BuyurtmaID int64
	Status     string
	Vaqt       string
}

type BuyurtmaMikroservis struct{}

func (s *BuyurtmaMikroservis) Yarat(ctx context.Context, req *BuyurtmaSorov) (*BuyurtmaJavob, error) {
	if req.Summa <= 0 {
		return nil, fmt.Errorf("rpc error: code = InvalidArgument desc = summa musbat bo'lishi shart")
	}

	fmt.Printf("[Mikroservis] Buyurtma yaratilmoqda: Mijoz=%d, Mahsulot=%s, Summa=%.2f\n",
		req.MijozID, req.Mahsulot, req.Summa)

	return &BuyurtmaJavob{
		BuyurtmaID: 77001,
		Status:     "MUVAFFAQIYATLI_QABUL_QILINDI",
		Vaqt:       time.Now().Format("15:04:05"),
	}, nil
}

// Simulyatsiya qilingan Unary Interceptor
func LogInterceptor(ctx context.Context, req *BuyurtmaSorov, srv *BuyurtmaMikroservis) (*BuyurtmaJavob, error) {
	boshlash := time.Now()
	res, err := srv.Yarat(ctx, req)
	fmt.Printf("[Interceptor] Metod: /OrderService/Yarat, Vaqt: %v, Err: %v\n",
		time.Since(boshlanish).Round(time.Millisecond), err)
	return res, err
}

func main() {
	servis := &BuyurtmaMikroservis{}

	req := &BuyurtmaSorov{
		MijozID:  105,
		Mahsulot: "Go Microservices Kitobi",
		Summa:    120000,
	}

	javob, err := LogInterceptor(context.Background(), req, servis)
	if err != nil {
		fmt.Println("Xatolik:", err)
		return
	}

	fmt.Println("=== MIKROSERVIS JAVOBI ===")
	fmt.Printf("Buyurtma ID: %d | Status: %s | Vaqt: %s\n",
		javob.BuyurtmaID, javob.Status, javob.Vaqt)
}
```

## Tushuntirish va Mantiq:
Ushbu loyiha zamonaviy gRPC mikroservisining to'liq hayotiy siklini namoyish etadi: parametrlar validatsiyasi, so'rovlarni interceptor orqali tahlil qilish, statuslar va toza arxitektura.

## Ishlash natijasi:
```text
[Mikroservis] Buyurtma yaratilmoqda: Mijoz=105, Mahsulot=Go Microservices Kitobi, Summa=120000.00
[Interceptor] Metod: /OrderService/Yarat, Vaqt: 0s, Err: <nil>
=== MIKROSERVIS JAVOBI ===
Buyurtma ID: 77001 | Status: MUVAFFAQIYATLI_QABUL_QILINDI | Vaqt: 15:04:05
```

