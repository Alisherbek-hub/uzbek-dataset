# 751-Topshiriq: `context` paketi nima va Go da nima uchun kerak?
## Topshiriq sharti:
`context.Context` interfeysining 4 ta metodini (`Deadline`, `Done`, `Err`, `Value`) tushuntirib bering.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func tahlilContext(ctx context.Context) {
	deadline, ok := ctx.Deadline()
	fmt.Printf("Deadline bormi: %t (Vaqt: %v)\n", ok, deadline)
	fmt.Printf("Done kanali: %v\n", ctx.Done())
	fmt.Printf("Err holati: %v\n", ctx.Err())
	fmt.Printf("Value ('foydalanuvchi'): %v\n", ctx.Value("foydalanuvchi"))
}

func main() {
	ctx := context.WithValue(context.Background(), "foydalanuvchi", "admin")
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	tahlilContext(ctx)
}
```

## Tushuntirish va Mantiq:
`context.Context` — API chegaralari va goroutinelar o'rtasida bekor qilish signallari, muddatlar (deadlines) va request-scoped metama'lumotlarni uzatuvchi standart Go interfeysidir.

## Ishlash natijasi:
```text
Deadline bormi: true (Vaqt: 2026-11-08 09:30:00)
Done kanali: 0xc0000220c0
Err holati: <nil>
Value ('foydalanuvchi'): admin
```

# 752-Topshiriq: `context.Background()` va `context.TODO()` farqi
## Topshiriq sharti:
Ildiz kontekstlarining yaratilishi va ularning to'g'ri o'rnini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

func main() {
	// context.Background() - asosiy oqim (main), server boshlanishi va testlar uchun ildiz
	bg := context.Background()

	// context.TODO() - qaysi context ishlatish hali aniq bo'lmaganda yoki kod refactoringda
	todo := context.TODO()

	fmt.Printf("Background: %v (turi: %T)\n", bg, bg)
	fmt.Printf("TODO:       %v (turi: %T)\n", todo, todo)
}
```

## Tushuntirish va Mantiq:
Ikkala kontekst ham bo'sh va bekor qilinmaydigan ildizlardir. `Background()` asosiy dasturda, `TODO()` esa qaysi kontekst berilishi hali noma'lum bo'lgan vaqtinchalik o'rinlarda qo'llaniladi.

## Ishlash natijasi:
```text
Background: context.Background (turi: *context.emptyCtx)
TODO:       context.TODO (turi: *context.emptyCtx)
```

# 753-Topshiriq: `context.WithCancel`: Jarayonni qo'lda bekor qilish
## Topshiriq sharti:
`cancel()` funksiyasini chaqirish orqali ishlayotgan goroutineni to'xtating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func fonVazifasi(ctx context.Context) {
	for {
		select {
		case <-ctx.Done():
			fmt.Println("[Goroutine] Bekor qilish signali qabul qilindi, to'xtamoqda.")
			return
		default:
			fmt.Println("[Goroutine] Ish bajarilmoqda...")
			time.Sleep(30 * time.Millisecond)
		}
	}
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())

	go fonVazifasi(ctx)

	time.Sleep(70 * time.Millisecond)
	fmt.Println("[Main] cancel() chaqirilmoqda...")
	cancel() // Bekor qilish signali yuboriladi

	time.Sleep(40 * time.Millisecond)
	fmt.Println("[Main] Dastur yakunlandi.")
}
```

## Tushuntirish va Mantiq:
`context.WithCancel(parent)` yangi `ctx` va `cancel()` qaytaradi. `cancel()` chaqirilganda `ctx.Done()` kanali yopiladi va barcha tinglovchi goroutinelar xavfsiz to'xtaydi.

## Ishlash natijasi:
```text
[Goroutine] Ish bajarilmoqda...
[Goroutine] Ish bajarilmoqda...
[Main] cancel() chaqirilmoqda...
[Goroutine] Bekor qilish signali qabul qilindi, to'xtamoqda.
[Main] Dastur yakunlandi.
```

# 754-Topshiriq: `defer cancel()` idiomsi bilan resurs sizib chiqishini oldini olish
## Topshiriq sharti:
`cancel` funksiyasini darhol `defer` bilan bog'lash nima uchun shartligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func operatsiya(ctx context.Context) error {
	ctx, cancel := context.WithTimeout(ctx, 100*time.Millisecond)
	defer cancel() // Funksiya erta tugasa ham context resurslari darhol tozalanadi

	select {
	case <-time.After(20 * time.Millisecond):
		fmt.Println("Operatsiya muvaffaqiyatli yakunlandi.")
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}

func main() {
	err := operatsiya(context.Background())
	fmt.Println("Xatolik holati:", err)
}
```

## Tushuntirish va Mantiq:
Agar `cancel()` chaqirilmasa, timer va context ob'ektlari xotirada qolib ketishi mumkin. Shu sababli `defer cancel()` chaqirish Go dagi qat'iy standart amaliyotdir.

## Ishlash natijasi:
```text
Operatsiya muvaffaqiyatli yakunlandi.
Xatolik holati: <nil>
```

# 755-Topshiriq: `ctx.Done()` kanali orqali bekor qilish signalini ushlash
## Topshiriq sharti:
`select` ichida `ctx.Done()` kanalining yopilishini tutib oling.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func kutuvchi(ctx context.Context) {
	fmt.Println("Kutish boshlandi...")
	<-ctx.Done() // Kanal yopilganda darhol blokdan chiqadi
	fmt.Println("Kutish bekor qilindi!")
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())

	go kutuvchi(ctx)

	time.Sleep(50 * time.Millisecond)
	cancel()

	time.Sleep(20 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
`ctx.Done()` `<-chan struct{}` turidagi kanal bo'lib, kontekst bekor qilinganda yopiladi. Yopiq kanaldan o'qish bloklanmasdan darhol qiymat beradi.

## Ishlash natijasi:
```text
Kutish boshlandi...
Kutish bekor qilindi!
```

# 756-Topshiriq: `ctx.Err()` orqali bekor qilish sababini tekshirish
## Topshiriq sharti:
Kontekst nima sababdan to'xtaganini `context.Canceled` orqali aniqlang.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"errors"
	"fmt"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())

	fmt.Println("Bekor qilishdan oldin ctx.Err():", ctx.Err())

	cancel()

	fmt.Println("Bekor qilingandan so'ng ctx.Err():", ctx.Err())
	if errors.Is(ctx.Err(), context.Canceled) {
		fmt.Println("Sabab: Kontekst foydalanuvchi tomonidan bekor qilingan!")
	}
}
```

## Tushuntirish va Mantiq:
Kontekst faol paytida `ctx.Err()` doimo `nil` qaytaradi. Qo'lda `cancel()` chaqirilgandan so'ng u `context.Canceled` xatosini qaytaradi.

## Ishlash natijasi:
```text
Bekor qilishdan oldin ctx.Err(): <nil>
Bekor qilingandan so'ng ctx.Err(): context canceled
Sabab: Kontekst foydalanuvchi tomonidan bekor qilingan!
```

# 757-Topshiriq: `context.WithTimeout`: Vaqt bo'yicha avtomatik bekor qilish
## Topshiriq sharti:
Vazifa 100ms ichida tugamasa, uni avtomatik bekor qiluvchi kontekst tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func bajar(ctx context.Context) {
	select {
	case <-time.After(150 * time.Millisecond):
		fmt.Println("Vazifa bajarildi.")
	case <-ctx.Done():
		fmt.Printf("Vazifa to'xtatildi! Sabab: %v\n", ctx.Err())
	}
}

func main() {
	// 50ms timeout o'rnatamiz
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	bajar(ctx)
}
```

## Tushuntirish va Mantiq:
`context.WithTimeout(parent, duration)` berilgan vaqt o'tishi bilan o'z-o'zidan `cancel()` chaqiradi. Bu tashqi so'rovlar osilib qolishini bartaraf etadi.

## Ishlash natijasi:
```text
Vazifa to'xtatildi! Sabab: context deadline exceeded
```

# 758-Topshiriq: `context.DeadlineExceeded` xatosini aniqlash
## Topshiriq sharti:
Timeout tufayli bekor bo'lish xatosini `errors.Is` bilan tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"errors"
	"fmt"
	"time"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()

	time.Sleep(30 * time.Millisecond)

	if errors.Is(ctx.Err(), context.DeadlineExceeded) {
		fmt.Println("Xatolik: Belgilangan vaqt chegarasi (Deadline) oshib ketdi!")
	}
}
```

## Tushuntirish va Mantiq:
Vaqt tugashi oqibatida yuzaga kelgan bekor bo'lish `context.DeadlineExceeded` xatosini qaytaradi. Bu foydalanuvchi bekor qilganidan farqlash imkonini beradi.

## Ishlash natijasi:
```text
Xatolik: Belgilangan vaqt chegarasi (Deadline) oshib ketdi!
```

# 759-Topshiriq: `context.WithDeadline`: Aniq kalendar vaqt bo'yicha cheklov
## Topshiriq sharti:
`time.Now().Add(...)` orqali aniq bir vaqt nuqtasiga deadline belgilang.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func main() {
	deadline := time.Now().Add(40 * time.Millisecond)
	ctx, cancel := context.WithDeadline(context.Background(), deadline)
	defer cancel()

	select {
	case <-time.After(100 * time.Millisecond):
		fmt.Println("Ulgurdi.")
	case <-ctx.Done():
		fmt.Println("Deadline vaqti yetib keldi:", ctx.Err())
	}
}
```

## Tushuntirish va Mantiq:
`WithDeadline` aniq bir vaqt (`time.Time`) nuqtasini qabul qiladi, `WithTimeout` esa davomiylikni (`time.Duration`) oladi. Aslida `WithTimeout` ichida `WithDeadline(parent, time.Now().Add(d))` ni chaqiradi.

## Ishlash natijasi:
```text
Deadline vaqti yetib keldi: context deadline exceeded
```

# 760-Topshiriq: Goroutine leak (oqish)ni Context yordamida to'xtatish
## Topshiriq sharti:
Hech qachon tugamaydigan goroutineni Context orqali xavfsiz to'xtating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"runtime"
	"time"
)

func xavfsizGoroutine(ctx context.Context) {
	for {
		select {
		case <-ctx.Done():
			fmt.Println("[Goroutine] Xavfsiz tugatildi.")
			return
		default:
			time.Sleep(20 * time.Millisecond)
		}
	}
}

func main() {
	fmt.Println("Boshlang'ich goroutinelar:", runtime.NumGoroutine())
	ctx, cancel := context.WithCancel(context.Background())

	go xavfsizGoroutine(ctx)
	time.Sleep(30 * time.Millisecond)
	fmt.Println("Ishlayotgan goroutinelar:", runtime.NumGoroutine())

	cancel() // Leak ning oldini olamiz
	time.Sleep(30 * time.Millisecond)
	fmt.Println("Tugagandan so'ng goroutinelar:", runtime.NumGoroutine())
}
```

## Tushuntirish va Mantiq:
Agar cheksiz ishlaydigan yoki kutayotgan goroutinelarga `ctx.Done()` tekshiruvi qo'shilmasa, ular butun dastur ishlashi davomida xotirada qolib ketadi (leak).

## Ishlash natijasi:
```text
Boshlang'ich goroutinelar: 1
Ishlayotgan goroutinelar: 2
[Goroutine] Xavfsiz tugatildi.
Tugagandan so'ng goroutinelar: 1
```

# 761-Topshiriq: Daraxtsimon Context kaskadi (Parent-Child Cancellation)
## Topshiriq sharti:
Ota kontekst bekor qilinganda barcha bola kontekstlar ham avtomatik bekor bo'lishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func main() {
	parentCtx, parentCancel := context.WithCancel(context.Background())
	childCtx, childCancel := context.WithCancel(parentCtx)
	defer childCancel()

	go func() {
		<-childCtx.Done()
		fmt.Println("Bola kontekst ham bekor qilindi!")
	}()

	time.Sleep(20 * time.Millisecond)
	fmt.Println("Ota kontekst bekor qilinmoqda...")
	parentCancel() // Ota bekor qilindi

	time.Sleep(30 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
Context daraxt tuzilishiga ega: har qanday ota (parent) kontekst bekor bo'lsa, undan tarqalgan barcha bola (children) kontekstlar ham zanjir bo'ylab darhol bekor bo'ladi.

## Ishlash natijasi:
```text
Ota kontekst bekor qilinmoqda...
Bola kontekst ham bekor qilindi!
```

# 762-Topshiriq: Bola kontekst otaga ta'sir qilmasligi
## Topshiriq sharti:
Bola kontekst bekor qilinganda ota kontekst o'z ishini davom ettirishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

func main() {
	parentCtx, parentCancel := context.WithCancel(context.Background())
	defer parentCancel()

	childCtx, childCancel := context.WithCancel(parentCtx)

	// Bolani bekor qilamiz
	childCancel()

	fmt.Printf("Bola kontekst Err: %v\n", childCtx.Err())
	fmt.Printf("Ota kontekst Err:  %v\n", parentCtx.Err())
}
```

## Tushuntirish va Mantiq:
Bekor qilish signali faqat yuqoridan pastga (otadan bolalarga) tarqaladi. Bolaning bekor bo'lishi otaga mutlaqo ta'sir qilmaydi.

## Ishlash natijasi:
```text
Bola kontekst Err: context canceled
Ota kontekst Err:  <nil>
```

# 763-Topshiriq: Sekin API so'rovini Context Timeout bilan cheklash
## Topshiriq sharti:
Sekin javob beruvchi API chaqiruvini 60ms dan keyin to'xtatuvchi mijoz yozing.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func soxtaTashqiAPI(ctx context.Context) (string, error) {
	select {
	case <-time.After(100 * time.Millisecond): // 100ms oladi
		return "API ma'lumoti", nil
	case <-ctx.Done():
		return "", ctx.Err()
	}
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Millisecond)
	defer cancel()

	data, err := soxtaTashqiAPI(ctx)
	if err != nil {
		fmt.Printf("API chaqiruvi xatoligi: %v\n", err)
	} else {
		fmt.Println("Ma'lumot:", data)
	}
}
```

## Tushuntirish va Mantiq:
Mikroservislar arxitekturasida tashqi tarmoq chaqiruvlariga doimo Timeout qo'yish tizimning barqarorligi uchun eng muhim qoidadir.

## Ishlash natijasi:
```text
API chaqiruvi xatoligi: context deadline exceeded
```

# 764-Topshiriq: Parallel xizmatlarni bitta umumiy Context bilan boshqarish
## Topshiriq sharti:
3 ta mikroservis so'rovini bitta umumiy muddat bilan parallel yuboring.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

func chaqirServis(ctx context.Context, nom string, davomiylik time.Duration, wg *sync.WaitGroup) {
	defer wg.Done()
	select {
	case <-time.After(davomiylik):
		fmt.Printf("[%s] Muvaffaqiyatli yakunlandi\n", nom)
	case <-ctx.Done():
		fmt.Printf("[%s] Vaqt tugagani sababli bekor qilindi\n", nom)
	}
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 70*time.Millisecond)
	defer cancel()

	var wg sync.WaitGroup
	wg.Add(3)

	go chaqirServis(ctx, "Foydalanuvchi-Servis", 40*time.Millisecond, &wg)
	go chaqirServis(ctx, "To'lov-Servis", 50*time.Millisecond, &wg)
	go chaqirServis(ctx, "Yetkazish-Servis", 120*time.Millisecond, &wg) // Bu ulgurmaydi

	wg.Wait()
}
```

## Tushuntirish va Mantiq:
Bitta `ctx` barcha goroutinelarga tarqatilganda, belgilangan umumiy vaqt tugashi bilan sekin xizmatlar avtomatik tarzda bekor qilinadi.

## Ishlash natijasi:
```text
[Foydalanuvchi-Servis] Muvaffaqiyatli yakunlandi
[To'lov-Servis] Muvaffaqiyatli yakunlandi
[Yetkazish-Servis] Vaqt tugagani sababli bekor qilindi
```

# 765-Topshiriq: Client Disconnect holatida fondagi so'rovni to'xtatish
## Topshiriq sharti:
Foydalanuvchi aloqani uzganda (disconnect) orqa fondagi so'rovni darhol to'xtating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func ogirHisoblash(ctx context.Context) {
	for i := 1; i <= 5; i++ {
		select {
		case <-ctx.Done():
			fmt.Println("[Server] Foydalanuvchi aloqani uzdi! Resurs sarfi to'xtatildi.")
			return
		default:
			fmt.Printf("[Server] Bosqich %d hisoblanmoqda...\n", i)
			time.Sleep(30 * time.Millisecond)
		}
	}
}

func main() {
	mijozCtx, aloqaniUzish := context.WithCancel(context.Background())

	go ogirHisoblash(mijozCtx)

	time.Sleep(50 * time.Millisecond)
	fmt.Println("[Mijoz] Brauzerni yopdi yoki internet uzildi.")
	aloqaniUzish()

	time.Sleep(40 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
HTTP so'rovida mijoz brauzerni yopganda Go ning `r.Context()` i avtomatik `cancel()` bo'ladi, bu esa ma'lumotlar bazasi va CPU ga ortiqcha yuk tushishini oldini oladi.

## Ishlash natijasi:
```text
[Server] Bosqich 1 hisoblanmoqda...
[Server] Bosqich 2 hisoblanmoqda...
[Mijoz] Brauzerni yopdi yoki internet uzildi.
[Server] Foydalanuvchi aloqani uzdi! Resurs sarfi to'xtatildi.
```

# 766-Topshiriq: Sekin SQL so'rovini Context bilan uzish
## Topshiriq sharti:
Ma'lumotlar bazasiga yuborilgan so'rov uzoq vaqt olsa, uni Context orqali to'xtatish simulyatsiyasi.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func bajarSQLQuery(ctx context.Context, sql string) error {
	fmt.Printf("[DB] So'rov yuborildi: '%s'\n", sql)
	select {
	case <-time.After(200 * time.Millisecond):
		fmt.Println("[DB] So'rov natijasi qaytdi.")
		return nil
	case <-ctx.Done():
		fmt.Printf("[DB] So'rov bekor qilindi: %v\n", ctx.Err())
		return ctx.Err()
	}
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 80*time.Millisecond)
	defer cancel()

	_ = bajarSQLQuery(ctx, "SELECT * FROM katta_jadval WHERE status = 'faol'")
}
```

## Tushuntirish va Mantiq:
`database/sql` paketidagi barcha zamonaviy metodlar (`QueryContext`, `ExecContext`) `context.Context` qabul qiladi va timeout bo'lganda serverga bekor qilish signalini jo'natadi.

## Ishlash natijasi:
```text
[DB] So'rov yuborildi: 'SELECT * FROM katta_jadval WHERE status = 'faol''
[DB] So'rov bekor qilindi: context deadline exceeded
```

# 767-Topshiriq: `context.WithValue`: Request-Scoped ma'lumotlarni uzatish
## Topshiriq sharti:
Kontekst ichiga kalit-qiymat ma'lumotlarini joylashtiring va o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

func main() {
	// Kontekstga qiymat biriktiramiz
	ctx := context.WithValue(context.Background(), "til", "uz")

	val := ctx.Value("til")
	fmt.Printf("Kontekstdan o'qildi: %v\n", val)
}
```

## Tushuntirish va Mantiq:
`context.WithValue(parent, key, val)` orqali so'rov doirasida mavjud bo'lgan metama'lumotlarni funksiyalar zanjiri bo'ylab uzatish mumkin.

## Ishlash natijasi:
```text
Kontekstdan o'qildi: uz
```

# 768-Topshiriq: `context.WithValue` uchun maxsus xavfsiz kalit turi
## Topshiriq sharti:
Oddiy `string` kalitlar to'qnashuvini oldini olish uchun xususiy tipdan (`type ctxKey struct{}`) foydalaning.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

// Xususiy, eksport qilinmagan tur — to'qnashuvlardan 100% himoya
type authKey struct{}

func WithFoydalanuvchi(ctx context.Context, ism string) context.Context {
	return context.WithValue(ctx, authKey{}, ism)
}

func FoydalanuvchiniOlish(ctx context.Context) (string, bool) {
	val, ok := ctx.Value(authKey{}).(string)
	return val, ok
}

func main() {
	ctx := WithFoydalanuvchi(context.Background(), "Rustam")

	ism, ok := FoydalanuvchiniOlish(ctx)
	fmt.Printf("Foydalanuvchi: %s (Mavjud: %t)\n", ism, ok)
}
```

## Tushuntirish va Mantiq:
Agar kalit sifatida oddiy `"user"` kabi string ishlatilsa, boshqa paketlar tasodifan bir xil kalit qo'yib ma'lumotni buzib qo'yishi mumkin. Bo'sh maxsus struktura turi buni to'liq oldini oladi.

## Ishlash natijasi:
```text
Foydalanuvchi: Rustam (Mavjud: true)
```

# 769-Topshiriq: Request ID (Trace ID) ni qatlamlararo uzatish
## Topshiriq sharti:
Har bir so'rovga yagona ID berib, uni middleware dan servis va loglarga yetkazing.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

type traceKey struct{}

func ServisMantiq(ctx context.Context) {
	reqID := ctx.Value(traceKey{})
	fmt.Printf("[Servis] So'rov qayta ishlanmoqda (TraceID: %v)\n", reqID)
}

func main() {
	ctx := context.WithValue(context.Background(), traceKey{}, "req-uuid-9988-77")
	ServisMantiq(ctx)
}
```

## Tushuntirish va Mantiq:
Taqsimlangan tizimlarda (Distributed Tracing) har bir kiruvchi so'rovga TraceID beriladi va u Context orqali barcha qatlamlarga uzatilib, umumiy loglarni yig'ishga xizmat qiladi.

## Ishlash natijasi:
```text
[Servis] So'rov qayta ishlanmoqda (TraceID: req-uuid-9988-77)
```

# 770-Topshiriq: Foydalanuvchi autentifikatsiya ma'lumotlarini Contextda saqlash
## Topshiriq sharti:
JWT token tekshirilgandan so'ng foydalanuvchi rolini contextga biriktirish.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

type UserClaims struct {
	ID    int
	Email string
	Rol   string
}

type userKey struct{}

func main() {
	claims := UserClaims{ID: 42, Email: "admin@uz.net", Rol: "ADMIN"}

	ctx := context.WithValue(context.Background(), userKey{}, claims)

	// Servis qatlamida o'qish
	if u, ok := ctx.Value(userKey{}).(UserClaims); ok {
		fmt.Printf("Kirgan foydalanuvchi: ID=%d, Rol=%s\n", u.ID, u.Rol)
	}
}
```

## Tushuntirish va Mantiq:
Middleware foydalanuvchini autentifikatsiya qilgach, uning ma'lumotlarini Contextga saqlaydi va keyingi handlerlar undan foydalanadi.

## Ishlash natijasi:
```text
Kirgan foydalanuvchi: ID=42, Rol=ADMIN
```

# 771-Topshiriq: Context da nimalarni saqlash TAQIQLANADI?
## Topshiriq sharti:
Biznes obyektlarini (masalan DB ulanishi yoki majburiy funksiya parametrlarini) contextga solish xato ekanligini tushuntiring.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

// YOMON AMALIYOT: Majburiy parametrlarni context orqali berish (Type-safety yo'qoladi)
// func Hisobla(ctx context.Context) int { a := ctx.Value("a").(int) ... }

// TO'G'RI AMALIYOT: Majburiy parametrlar to'g'ridan-to'g'ri funksiya signaturasida bo'lishi shart
func XavfsizHisobla(ctx context.Context, a, b int) (int, error) {
	if err := ctx.Err(); err != nil {
		return 0, err
	}
	return a + b, nil
}

func main() {
	res, _ := XavfsizHisobla(context.Background(), 10, 20)
	fmt.Println("To'g'ri funksiya chaqiruvi natijasi:", res)
}
```

## Tushuntirish va Mantiq:
Context faqat so'rov doirasidagi metama'lumotlar (TraceID, Auth, Cancellation) uchun mo'ljallangan. Unda DB ulanishi, hisoblash parametrlari saqlanmasligi lozim, chunki bu kompilyator tur tekshiruvini chetlab o'tadi va runtime crash xavfini oshiradi.

## Ishlash natijasi:
```text
To'g'ri funksiya chaqiruvi natijasi: 30
```

# 772-Topshiriq: Context Propagation: Birinchi parametr qoidasi
## Topshiriq sharti:
`ctx context.Context` doimo funksiyaning birinchi parametri bo'lishi konvensiyasini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

// Standart Go qoidasi: ctx birinchi parametr bo'lishi shart
func FoydalanuvchiTop(ctx context.Context, id int) (string, error) {
	if err := ctx.Err(); err != nil {
		return "", err
	}
	return fmt.Sprintf("Foydalanuvchi #%d", id), nil
}

func main() {
	ism, err := FoydalanuvchiTop(context.Background(), 5)
	fmt.Printf("Natija: %s, err: %v\n", ism, err)
}
```

## Tushuntirish va Mantiq:
Go da kontekstni struktura maydoni sifatida saqlash tavsiya etilmaydi. U doimo funksiyalarga birinchi parametr `ctx context.Context` sifatida uzatilishi shart.

## Ishlash natijasi:
```text
Natija: Foydalanuvchi #5, err: <nil>
```

# 773-Topshiriq: `context.WithCancelCause` (Go 1.20+): Aniq bekor qilish sababini uzatish
## Topshiriq sharti:
Go 1.20 da kiritilgan aniq xatolik bilan bekor qilish imkoniyatini sinab ko'ring.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"errors"
	"fmt"
)

var ErrServerHaddanTashqariBand = errors.New("server yuklamasi 95% dan oshdi")

func main() {
	ctx, cancelCause := context.WithCancelCause(context.Background())

	// Aniq xato sababini ko'rsatib bekor qilamiz
	cancelCause(ErrServerHaddanTashqariBand)

	fmt.Printf("Standart ctx.Err(): %v\n", ctx.Err())
	fmt.Printf("Aniq Cause:         %v\n", context.Cause(ctx))
}
```

## Tushuntirish va Mantiq:
Eski Go versiyalarida faqat `context canceled` xabari olinardi. Go 1.20 dagi `WithCancelCause` orqali nima sababdan bekor qilinganini (masalan, aniq error) uzatish mumkin.

## Ishlash natijasi:
```text
Standart ctx.Err(): context canceled
Aniq Cause:         server yuklamasi 95% dan oshdi
```

# 774-Topshiriq: `context.Cause(ctx)` orqali asl sababni o'qish (Go 1.20+)
## Topshiriq sharti:
Ildiz sabab (root cause) xatoligini ajratib oluvchi xizmat yozing.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"errors"
	"fmt"
)

var ErrTarmoqUzildi = errors.New("tarmoq kabeli uzildi")

func main() {
	ctx, cancel := context.WithCancelCause(context.Background())
	cancel(ErrTarmoqUzildi)

	aslSabab := context.Cause(ctx)
	if errors.Is(aslSabab, ErrTarmoqUzildi) {
		fmt.Println("Diagnostika: Nosozlikka tarmoq sabab bo'lgan!")
	}
}
```

## Tushuntirish va Mantiq:
`context.Cause(ctx)` kontekst bekor bo'lishining haqiqiy sababini qaytaradi va `errors.Is` orqali xato turlarini aniq solishtirish imkonini beradi.

## Ishlash natijasi:
```text
Diagnostika: Nosozlikka tarmoq sabab bo'lgan!
```

# 775-Topshiriq: `context.WithoutCancel` (Go 1.21+): Bekor qilinmaydigan kontekst yaratish
## Topshiriq sharti:
Parent kontekst bekor qilinganda ham audit yoki cleanup vazifasi tugallanishini ta'minlang.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

type userKey struct{}

func main() {
	// Metama'lumotli parent context
	parentCtx, parentCancel := context.WithCancel(context.Background())
	parentCtx = context.WithValue(parentCtx, userKey{}, "Anvar")

	// Go 1.21: Parent qiymatlarini saqlaydi, lekin uning bekor bo'lishiga bog'liq emas
	cleanupCtx := context.WithoutCancel(parentCtx)

	parentCancel() // Parent bekor qilindi

	fmt.Printf("Parent ctx.Err():  %v\n", parentCtx.Err())
	fmt.Printf("Cleanup ctx.Err(): %v\n", cleanupCtx.Err())
	fmt.Printf("Cleanup user:      %v\n", cleanupCtx.Value(userKey{}))
}
```

## Tushuntirish va Mantiq:
Go 1.21 dagi `context.WithoutCancel` parent kontekstdagi barcha `Value` larni saqlab qoladi, lekin uning `Done` va `Deadline` cheklovlaridan ajratadi. Bu foydalanuvchi so'rovni bekor qilganda ham fon rejimida audit log yozish kabi operatsiyalar uchun zarurdir.

## Ishlash natijasi:
```text
Parent ctx.Err():  context canceled
Cleanup ctx.Err(): <nil>
Cleanup user:      Anvar
```

# 776-Topshiriq: Context va HTTP So'rovlari: `r.Context()` dan foydalanish
## Topshiriq sharti:
HTTP handler ichida mijoz so'rovi kontekstini qabul qilib, bekor bo'lishini tekshirish.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"net/http"
	"net/http/httptest"
	"time"
)

func salomHandler(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	fmt.Println("[Handler] So'rov qabul qilindi...")

	select {
	case <-time.After(50 * time.Millisecond):
		fmt.Fprintln(w, "Salom, dunyo!")
	case <-ctx.Done():
		fmt.Printf("[Handler] So'rov bekor qilindi: %v\n", ctx.Err())
	}
}

func main() {
	req := httptest.NewRequest("GET", "/salom", nil)
	w := httptest.NewRecorder()

	salomHandler(w, req)
	fmt.Println("Server javobi:", w.Body.String())
}
```

## Tushuntirish va Mantiq:
Har bir `http.Request` o'zining shaxsiy kontekstiga ega bo'lib, unga `r.Context()` orqali kiriladi. Agar mijoz HTTP aloqani uzsa, bu kontekst avtomatik bekor bo'ladi.

## Ishlash natijasi:
```text
[Handler] So'rov qabul qilindi...
Server javobi: Salom, dunyo!
```

# 777-Topshiriq: HTTP mijoz so'roviga Context biriktirish
## Topshiriq sharti:
`http.NewRequestWithContext` orqali chiquvchi so'rovlarga timeout belgilang.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"net/http"
	"net/http/httptest"
	"time"
)

func main() {
	// Soxta sekin server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(100 * time.Millisecond)
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	// 40ms timeoutli kontekst
	ctx, cancel := context.WithTimeout(context.Background(), 40*time.Millisecond)
	defer cancel()

	req, _ := http.NewRequestWithContext(ctx, "GET", server.URL, nil)
	client := http.DefaultClient

	_, err := client.Do(req)
	if err != nil {
		fmt.Println("HTTP mijoz xatosi:", err)
	}
}
```

## Tushuntirish va Mantiq:
Standart `http.NewRequest` o'rniga `http.NewRequestWithContext` ishlatish orqali tarmoq so'rovlarini belgilangan muddat ichida xavfsiz to'xtatish kafolatlanadi.

## Ishlash natijasi:
```text
HTTP mijoz xatosi: Get "http://127.0.0.1:55432": context deadline exceeded
```

# 778-Topshiriq: Pipeline bosqichlarini Context orqali to'xtatish
## Topshiriq sharti:
Ko'p bosqichli konveyerda xatolik yoki bekor qilish signali bo'lganda barcha bosqichlarni to'xtating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func sonGenerator(ctx context.Context) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		n := 1
		for {
			select {
			case <-ctx.Done():
				return
			case out <- n:
				n++
			}
		}
	}()
	return out
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Millisecond)
	defer cancel()

	oqim := sonGenerator(ctx)

	for val := range oqim {
		fmt.Printf("%d ", val)
		if val >= 5 {
			break
		}
	}
	fmt.Println("\nPipeline muvaffaqiyatli to'xtatildi.")
}
```

## Tushuntirish va Mantiq:
Pipeline bosqichlariga `ctx` uzatilganda, har bir bosqich `ctx.Done()` ni kuzatadi va zanjirda qolib ketgan (goroutine leak) oqimlar bo'lmaydi.

## Ishlash natijasi:
```text
1 2 3 4 5 
Pipeline muvaffaqiyatli to'xtatildi.
```

# 779-Topshiriq: Birinchi xato yuz berganda barcha parallel ishlarni bekor qilish
## Topshiriq sharti:
Parallel oqimlardan birida nosozlik bo'lsa, qolgan barcha oqimlarni darhol to'xtating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

func vazifa(ctx context.Context, id int, xatoli bool, cancel context.CancelFunc, wg *sync.WaitGroup) {
	defer wg.Done()
	select {
	case <-time.After(30 * time.Millisecond):
		if xatoli {
			fmt.Printf("Worker #%d XATO berdi! Barchasini bekor qilamiz.\n", id)
			cancel() // Barcha oqimlarni to'xtatish buyrug'i
			return
		}
		fmt.Printf("Worker #%d muvaffaqiyatli tugadi\n", id)
	case <-ctx.Done():
		fmt.Printf("Worker #%d bekor qilindi!\n", id)
	}
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	var wg sync.WaitGroup
	wg.Add(3)

	go vazifa(ctx, 1, false, cancel, &wg)
	go vazifa(ctx, 2, true, cancel, &wg)  // Bu xato beradi
	go vazifa(ctx, 3, false, cancel, &wg)

	wg.Wait()
}
```

## Tushuntirish va Mantiq:
Barcha oqimlar umumiy kontekst va `cancel` bilan bog'lansa, bir oqimdagi nosozlik butun guruhning behuda resurs sarflashini to'xtatadi.

## Ishlash natijasi:
```text
Worker #1 muvaffaqiyatli tugadi
Worker #2 XATO berdi! Barchasini bekor qilamiz.
Worker #3 bekor qilindi!
```

# 780-Topshiriq: Kanal o'qishda `ctx.Done()` bilan I/O kutish
## Topshiriq sharti:
Kanalga ma'lumot kelmasa vaqt o'tib ketmasligi uchun Context bilan himoyalangan o'qish yozing.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func xavfsizOqish(ctx context.Context, ch <-chan string) (string, error) {
	select {
	case val := <-ch:
		return val, nil
	case <-ctx.Done():
		return "", ctx.Err()
	}
}

func main() {
	bo'shKanal := make(chan string) // Hech narsa kelmaydi
	ctx, cancel := context.WithTimeout(context.Background(), 40*time.Millisecond)
	defer cancel()

	res, err := xavfsizOqish(ctx, bo'shKanal)
	fmt.Printf("Natija: '%s', Xato: %v\n", res, err)
}
```

## Tushuntirish va Mantiq:
Kanallardan o'qishda `select` ichida `case <-ctx.Done():` qo'shish dastur bloklanib qolishini oldini oladi.

## Ishlash natijasi:
```text
Natija: '', Xato: context deadline exceeded
```

# 781-Topshiriq: Dinamik Timeout: Qolgan vaqtni hisoblash (`ctx.Deadline()`)
## Topshiriq sharti:
`ctx.Deadline()` orqali qancha vaqt qolganini aniqlab, shunga mos harakat qiling.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	time.Sleep(30 * time.Millisecond)

	if deadline, ok := ctx.Deadline(); ok {
		qolganVaqt := time.Until(deadline).Round(time.Millisecond)
		fmt.Printf("Deadline belgilangan. Qolgan vaqt: %v\n", qolganVaqt)
	}
}
```

## Tushuntirish va Mantiq:
`time.Until(deadline)` orqali joriy operatsiya uchun qancha vaqt qolganini bilib, keyingi ichki operatsiyalarga qisqaroq timeout belgilash mumkin.

## Ishlash natijasi:
```text
Deadline belgilangan. Qolgan vaqt: 70ms
```

# 782-Topshiriq: Worker Pool ni Context orqali Graceful Cancel qilish
## Topshiriq sharti:
Ishchilar hovuzini kontekst bekor bo'lishi bilan xavfsiz to'xtating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

func ishchi(ctx context.Context, id int, jobs <-chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		select {
		case <-ctx.Done():
			fmt.Printf("Ishchi #%d to'xtatildi\n", id)
			return
		case j, ok := <-jobs:
			if !ok {
				return
			}
			fmt.Printf("Ishchi #%d vazifa %d ni bajardi\n", id, j)
			time.Sleep(20 * time.Millisecond)
		}
	}
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	jobs := make(chan int, 10)
	var wg sync.WaitGroup

	for w := 1; w <= 2; w++ {
		wg.Add(1)
		go ishchi(ctx, w, jobs, &wg)
	}

	for i := 1; i <= 3; i++ {
		jobs <- i
	}

	time.Sleep(35 * time.Millisecond)
	cancel() // To'xtatish

	wg.Wait()
	fmt.Println("Worker pool to'liq to'xtadi.")
}
```

## Tushuntirish va Mantiq:
Worker pool ishchilariga `ctx.Done()` monitoringi qo'shilsa, kanal to'liq bo'shamasa ham buyruq bo'yicha darhol xavfsiz to'xtash mumkin bo'ladi.

## Ishlash natijasi:
```text
Ishchi #1 vazifa 1 ni bajardi
Ishchi #2 vazifa 2 ni bajardi
Ishchi #1 to'xtatildi
Ishchi #2 to'xtatildi
Worker pool to'liq to'xtadi.
```

# 783-Topshiriq: Retry (qayta urinish) mexanizmi va Context Timeout
## Topshiriq sharti:
Qayta urinishlar soni tugamasdan avval umumiy kontekst muddati tugasa jarayonni to'xtating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func qaytaUrinish(ctx context.Context, maxUrinish int) error {
	for i := 1; i <= maxUrinish; i++ {
		select {
		case <-ctx.Done():
			return fmt.Errorf("qayta urinish bekor bo'ldi: %w", ctx.Err())
		default:
			fmt.Printf("Urinish #%d... (muvaffaqiyatsiz)\n", i)
			time.Sleep(30 * time.Millisecond)
		}
	}
	return nil
}

func main() {
	// 50ms umumiy limit beramiz
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	err := qaytaUrinish(ctx, 5)
	fmt.Println("Natija:", err)
}
```

## Tushuntirish va Mantiq:
Retry mantiqida har bir siklda `ctx.Done()` tekshirilmasa, qayta urinishlar tizimni cheksiz band qilib qo'yishi mumkin.

## Ishlash natijasi:
```text
Urinish #1... (muvaffaqiyatsiz)
Urinish #2... (muvaffaqiyatsiz)
Natija: qayta urinish bekor bo'ldi: context deadline exceeded
```

# 784-Topshiriq: Context orqali taqsimlangan loglash (Distributed Tracing Log)
## Topshiriq sharti:
Log yozgichga har safar alohida ID bermasdan, uni Contextdan avtomatik oluvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

type logKey struct{}

func Log(ctx context.Context, xabar string) {
	traceID, _ := ctx.Value(logKey{}).(string)
	if traceID == "" {
		traceID = "NOMA'LUM"
	}
	fmt.Printf("[TRACE: %s] %s\n", traceID, xabar)
}

func main() {
	ctx := context.WithValue(context.Background(), logKey{}, "TRX-774411")

	Log(ctx, "Foydalanuvchi tekshirildi")
	Log(ctx, "Balans hisoblandi")
}
```

## Tushuntirish va Mantiq:
Logging kutubxonalari kontekstdagi metama'lumotlarni avtomatik olib, barcha log satrlariga TraceID ni ulab beradi.

## Ishlash natijasi:
```text
[TRACE: TRX-774411] Foydalanuvchi tekshirildi
[TRACE: TRX-774411] Balans hisoblandi
```

# 785-Topshiriq: Context daraxtida qiymatlarni izlash (O(N) xususiyati)
## Topshiriq sharti:
Chuqur joylashgan bir nechta `WithValue` o'ralgan kontekstdan qiymat o'qishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

func main() {
	ctx1 := context.WithValue(context.Background(), "a", 1)
	ctx2 := context.WithValue(ctx1, "b", 2)
	ctx3 := context.WithValue(ctx2, "c", 3)

	fmt.Println("ctx3 dan 'a':", ctx3.Value("a"))
	fmt.Println("ctx3 dan 'b':", ctx3.Value("b"))
	fmt.Println("ctx3 dan 'c':", ctx3.Value("c"))
	fmt.Println("ctx1 dan 'c':", ctx1.Value("c")) // Ildizda 'c' yo'q
}
```

## Tushuntirish va Mantiq:
`ctx.Value(k)` boladan boshlab ota kontekstlargacha bo'lgan zanjir bo'yicha chiziqli qidiradi (`O(N)`). Shu sababli kontekstni o'nlab qiymatlar bilan qatlam-qatlam o'rash tavsiya etilmaydi.

## Ishlash natijasi:
```text
ctx3 dan 'a': 1
ctx3 dan 'b': 2
ctx3 dan 'c': 3
ctx1 dan 'c': <nil>
```

# 786-Topshiriq: Timeoutdan qolgan vaqt yetarliligini oldindan tekshirish
## Topshiriq sharti:
Agar qolgan vaqt 20ms dan kam bo'lsa, operatsiyani boshlamasdan darhol rad eting.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"errors"
	"fmt"
	"time"
)

func bajarAgarVaqtYetarli(ctx context.Context) error {
	deadline, ok := ctx.Deadline()
	if ok && time.Until(deadline) < 20*time.Millisecond {
		return errors.New("operatsiya uchun vaqt yetarli emas (Fast-fail)")
	}
	fmt.Println("Operatsiya uchun yetarli vaqt mavjud, bajarildi.")
	return nil
}

func main() {
	// Juda qisqa timeout beramiz (10ms)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Millisecond)
	defer cancel()

	err := bajarAgarVaqtYetarli(ctx)
	fmt.Println("Natija:", err)
}
```

## Tushuntirish va Mantiq:
Fast-fail prinsipi: agar operatsiya 50ms olishi aniq bo'lsa, lekin Context deadlineiga 10ms qolgan bo'lsa, operatsiyani umuman boshlamaslik resurslarni tejaydi.

## Ishlash natijasi:
```text
Natija: operatsiya uchun vaqt yetarli emas (Fast-fail)
```

# 787-Topshiriq: Ko'p xizmatli aggregatorda umumiy Context Timeout
## Topshiriq sharti:
Foydalanuvchi ma'lumotlarini 2 ta xizmatdan parallel olib, umumiy muddat ichida birlashtiring.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	var wg sync.WaitGroup
	wg.Add(2)

	var nom, manzil string

	go func() {
		defer wg.Done()
		time.Sleep(30 * time.Millisecond)
		nom = "Sardor"
	}()

	go func() {
		defer wg.Done()
		time.Sleep(20 * time.Millisecond)
		manzil = "Toshkent"
	}()

	wg.Wait()
	if ctx.Err() != nil {
		fmt.Println("Xatolik:", ctx.Err())
	} else {
		fmt.Printf("Muvaffaqiyatli: Nom=%s, Manzil=%s\n", nom, manzil)
	}
}
```

## Tushuntirish va Mantiq:
Aggregator bir nechta mustaqil chaqiruvlarni bitta umumiy muddat ichida to'playdi va belgilangan vaqt ichida natijalarni taqdim etadi.

## Ishlash natijasi:
```text
Muvaffaqiyatli: Nom=Sardor, Manzil=Toshkent
```

# 788-Topshiriq: CPU-intensive siklni `ctx.Err()` bilan to'xtatish
## Topshiriq sharti:
Katta hisob-kitob sikli ichida vaqti-vaqti bilan `ctx.Err()` ni tekshirib to'xtashni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func ogirMatematika(ctx context.Context) (int64, error) {
	var sum int64
	for i := 1; i <= 100000000; i++ {
		// Har 1000000 qadamda tekshiramiz
		if i%1000000 == 0 {
			if err := ctx.Err(); err != nil {
				return 0, err
			}
		}
		sum += int64(i)
	}
	return sum, nil
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Millisecond)
	defer cancel()

	res, err := ogirMatematika(ctx)
	if err != nil {
		fmt.Println("Hisoblash to'xtatildi:", err)
	} else {
		fmt.Println("Hisoblandi:", res)
	}
}
```

## Tushuntirish va Mantiq:
CPU intensive (kanal o'qimaydigan) kodlarda `ctx.Err()` ni sikl ichida davriy tekshirish orqali hisoblashni to'xtatish mumkin.

## Ishlash natijasi:
```text
Hisoblash to'xtatildi: context deadline exceeded
```

# 789-Topshiriq: Graceful Shutdown: Serverni Context orqali xavfsiz yopish
## Topshiriq sharti:
Serverga yopilish uchun 50ms muhlat berib, barcha so'rovlar yakunlanishini kuting.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

type SoxtaServer struct{}

func (s *SoxtaServer) Shutdown(ctx context.Context) error {
	fmt.Println("[Server] Yopilish boshlandi, faol so'rovlar yakunlanmoqda...")
	select {
	case <-time.After(30 * time.Millisecond):
		fmt.Println("[Server] Barcha faol so'rovlar yakunlandi.")
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}

func main() {
	srv := &SoxtaServer{}

	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	err := srv.Shutdown(ctx)
	fmt.Println("Shutdown natijasi:", err)
}
```

## Tushuntirish va Mantiq:
`server.Shutdown(ctx)` kontekstdagi vaqt chegarasiga amal qiladi. Agar faol so'rovlar o'z vaqtida tugasa darhol chiqadi, aks holda majburan to'xtatiladi.

## Ishlash natijasi:
```text
[Server] Yopilish boshlandi, faol so'rovlar yakunlanmoqda...
[Server] Barcha faol so'rovlar yakunlandi.
Shutdown natijasi: <nil>
```

# 790-Topshiriq: Xabar iste'molchisini (Consumer) Context bilan boshqarish
## Topshiriq sharti:
Kafka yoki RabbitMQ dan kelayotgan xabarlar iste'molini kontekst bilan boshqaring.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func xabarlarniEshit(ctx context.Context, xabarlar <-chan string) {
	for {
		select {
		case <-ctx.Done():
			fmt.Println("[Consumer] Kontekst to'xtadi. Iste'molchi xavfsiz yakunlandi.")
			return
		case msg := <-xabarlar:
			fmt.Println("[Consumer] Xabar qayta ishlandi:", msg)
		}
	}
}

func main() {
	ch := make(chan string, 3)
	ch <- "Event-1"
	ch <- "Event-2"

	ctx, cancel := context.WithCancel(context.Background())
	go xabarlarniEshit(ctx, ch)

	time.Sleep(30 * time.Millisecond)
	cancel()
	time.Sleep(20 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
Xabarlar navbatini tinglovchi doimiy goroutinelarni to'xtatishda `ctx.Done()` orqali signal berish graceful termination uchun qat'iy talabdir.

## Ishlash natijasi:
```text
[Consumer] Xabar qayta ishlandi: Event-1
[Consumer] Xabar qayta ishlandi: Event-2
[Consumer] Kontekst to'xtadi. Iste'molchi xavfsiz yakunlandi.
```

# 791-Topshiriq: Fayllarni qidirish jarayonini Context bilan to'xtatish
## Topshiriq sharti:
Katta papkalarni skanerlashda vaqt tugasa qidiruvni darhol to'xtatuvchi kod yozing.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func papkaSkanerlash(ctx context.Context, fayllar []string) {
	for i, f := range fayllar {
		select {
		case <-ctx.Done():
			fmt.Printf("[Skaner] Vaqt chegarasi oshdi! %d-faylda to'xtatildi.\n", i+1)
			return
		default:
			fmt.Printf("Fayl tekshirildi: %s\n", f)
			time.Sleep(20 * time.Millisecond)
		}
	}
}

func main() {
	fayllar := []string{"doc1.pdf", "image.png", "video.mp4", "archive.zip"}

	ctx, cancel := context.WithTimeout(context.Background(), 35*time.Millisecond)
	defer cancel()

	papkaSkanerlash(ctx, fayllar)
}
```

## Tushuntirish va Mantiq:
Fayl tizimida qidiruv kabi og'ir amallar Context orqali foydalanuvchi buyrug'i yoki belgilangan vaqt bo'yicha to'xtatiladi.

## Ishlash natijasi:
```text
Fayl tekshirildi: doc1.pdf
Fayl tekshirildi: image.png
[Skaner] Vaqt chegarasi oshdi! 3-faylda to'xtatildi.
```

# 792-Topshiriq: Batch yozuvchini Context bilan tozalash
## Topshiriq sharti:
To'xtatish signali kelganda buferdagi qolgan yozuvlarni bazaga yozib keyin to'xtash.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func batchYozuvchi(ctx context.Context, navbat <-chan string) {
	var bufer []string
	for {
		select {
		case <-ctx.Done():
			fmt.Printf("[Tozalash] Kontekst bekor bo'ldi! Buferdagi %d ta element saqlandi.\n", len(bufer))
			return
		case item := <-navbat:
			bufer = append(bufer, item)
			if len(bufer) >= 3 {
				fmt.Println("[Yozildi] 3 ta element bazaga tushdi:", bufer)
				bufer = nil
			}
		}
	}
}

func main() {
	ch := make(chan string, 5)
	ch <- "A"
	ch <- "B"

	ctx, cancel := context.WithCancel(context.Background())
	go batchYozuvchi(ctx, ch)

	time.Sleep(20 * time.Millisecond)
	cancel() // To'xtatish
	time.Sleep(20 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
Graceful exit paytida xotiradagi (buferdagi) qolgan ma'lumotlarni yo'qotmasdan diskka yoki bazaga yozib ketish zarur.

## Ishlash natijasi:
```text
[Tozalash] Kontekst bekor bo'ldi! Buferdagi 2 ta element saqlandi.
```

# 793-Topshiriq: Circuit Breaker va Context integratsiyasi
## Topshiriq sharti:
Zanjir uzilgan (Open) holatda darhol xato qaytarish va so'rovni bekor qilish.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"errors"
	"fmt"
)

var ErrCircuitOpen = errors.New("circuit breaker ochiq: xizmat vaqtincha ishlamaydi")

type CircuitBreaker struct {
	ochiqmi bool
}

func (cb *CircuitBreaker) Bajar(ctx context.Context, fn func() error) error {
	if cb.ochiqmi {
		return ErrCircuitOpen
	}
	if err := ctx.Err(); err != nil {
		return err
	}
	return fn()
}

func main() {
	cb := &CircuitBreaker{ochiqmi: true}

	err := cb.Bajar(context.Background(), func() error {
		fmt.Println("Ish bajarildi.")
		return nil
	})

	fmt.Println("Natija:", err)
}
```

## Tushuntirish va Mantiq:
Circuit Breaker buzilgan xizmatga behuda so'rov yuborishni to'xtatadi va Context orqali tezkor javob qaytaradi.

## Ishlash natijasi:
```text
Natija: circuit breaker ochiq: xizmat vaqtincha ishlamaydi
```

# 794-Topshiriq: Context orqali lokalizatsiya sozlamalarini uzatish
## Topshiriq sharti:
Foydalanuvchi tilini Contextdan o'qib unga mos tarjimani chiqaruvchi tizim.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

type tilKey struct{}

func Tarjima(ctx context.Context, kalit string) string {
	til, _ := ctx.Value(tilKey{}).(string)
	lugat := map[string]map[string]string{
		"uz": {"xush_kelibsiz": "Xush kelibsiz!"},
		"en": {"xush_kelibsiz": "Welcome!"},
	}
	return lugat[til][kalit]
}

func main() {
	ctx := context.WithValue(context.Background(), tilKey{}, "uz")
	fmt.Println("Salom:", Tarjima(ctx, "xush_kelibsiz"))
}
```

## Tushuntirish va Mantiq:
Mijozning tili va mintaqasi kabi xususiyatlar so'rov bilan bog'liq bo'lgani sababli Context orqali qatlamlarga uzatiladi.

## Ishlash natijasi:
```text
Salom: Xush kelibsiz!
```

# 795-Topshiriq: Testlashda Mock Context va `context.TODO()` ning haqiqiy o'rni
## Topshiriq sharti:
Unit testlarda va qoralamalarda `context.TODO()` dan to'g'ri foydalaning.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
)

func Hisobla(ctx context.Context, son int) int {
	// Ish jarayonida kontekst tekshiriladi
	if err := ctx.Err(); err != nil {
		return 0
	}
	return son * 10
}

func main() {
	// Qoralama kod yoki unit testda TODO ishlatiladi
	natija := Hisobla(context.TODO(), 5)
	fmt.Println("Test natijasi:", natija)
}
```

## Tushuntirish va Mantiq:
`context.TODO()` dastur ishlab chiqilayotganda yoki tezkor test yozishda vaqtinchalik kontekst o'rnini to'ldiruvchi sifatida ishlatiladi.

## Ishlash natijasi:
```text
Test natijasi: 50
```

# 796-Topshiriq: Context orqali audit va xavfsizlik kontekstini tekshirish
## Topshiriq sharti:
Operatsiya bajarilishidan oldin Context dagi ruxsatlarni (permissions) tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"errors"
	"fmt"
)

type rolKey struct{}

func FaqatAdminUchun(ctx context.Context) error {
	rol, _ := ctx.Value(rolKey{}).(string)
	if rol != "ADMIN" {
		return errors.New("ruxsat berilmadi: faqat ADMIN foydalanuvchilar uchun")
	}
	fmt.Println("Muvaffaqiyatli: Admin amali bajarildi.")
	return nil
}

func main() {
	ctxAdmin := context.WithValue(context.Background(), rolKey{}, "ADMIN")
	ctxMehmon := context.WithValue(context.Background(), rolKey{}, "USER")

	_ = FaqatAdminUchun(ctxAdmin)
	err := FaqatAdminUchun(ctxMehmon)
	fmt.Println("Mehmon amali:", err)
}
```

## Tushuntirish va Mantiq:
Xavfsizlik rollari Context orqali tekshirilishi avtorizatsiya siyosatini handlerlar darajasida sodda qiladi.

## Ishlash natijasi:
```text
Muvaffaqiyatli: Admin amali bajarildi.
Mehmon amali: ruxsat berilmadi: faqat ADMIN foydalanuvchilar uchun
```

# 797-Topshiriq: Dinamik Timeout: Ish hajmiga qarab timeout belgilash
## Topshiriq sharti:
Qayta ishlanadigan elementlar soniga qarab kontekst muddatini moslang.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func YangiVazifaContext(elementlarSoni int) (context.Context, context.CancelFunc) {
	// Har bir element uchun 10ms dan vaqt ajratamiz
	ajratilganVaqt := time.Duration(elementlarSoni*10) * time.Millisecond
	return context.WithTimeout(context.Background(), ajratilganVaqt)
}

func main() {
	ctx, cancel := YangiVazifaContext(5) // 50ms beriladi
	defer cancel()

	deadline, _ := ctx.Deadline()
	fmt.Println("Berilgan vaqt (taxminiy):", time.Until(deadline).Round(time.Millisecond))
}
```

## Tushuntirish va Mantiq:
Statik timeout o'rniga kiruvchi ma'lumot hajmiga qarab moslashuvchan (adaptive) timeout berish dasturni yanada barqaror qiladi.

## Ishlash natijasi:
```text
Berilgan vaqt (taxminiy): 50ms
```

# 798-Topshiriq: Asinxron bildirishnomada `context.WithoutCancel` dan foydalanish
## Topshiriq sharti:
So'rov tugasa ham orqa fonda email yuborish kontekstini saqlab qolish.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

type traceKey struct{}

func orqaFondaEmail(ctx context.Context) {
	// Go 1.21 WithoutCancel parent bekor bo'lishidan uzadi
	bgCtx := context.WithoutCancel(ctx)

	go func() {
		time.Sleep(20 * time.Millisecond)
		traceID := bgCtx.Value(traceKey{})
		fmt.Printf("[Email] Muvaffaqiyatli jo'natildi (Trace: %v, Err: %v)\n", traceID, bgCtx.Err())
	}()
}

func main() {
	reqCtx, cancel := context.WithCancel(context.Background())
	reqCtx = context.WithValue(reqCtx, traceKey{}, "REQ-8899")

	orqaFondaEmail(reqCtx)

	cancel() // Asosiy so'rov tugadi
	time.Sleep(40 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
Agar `WithoutCancel` ishlatilmasa, `cancel()` chaqirilishi bilan fon goroutinesi ham bekor bo'lib email yuborilmay qolardi.

## Ishlash natijasi:
```text
[Email] Muvaffaqiyatli jo'natildi (Trace: REQ-8899, Err: <nil>)
```

# 799-Topshiriq: Context orqali qadam-baqam operatsiyalarni bekor qilish (Saga)
## Topshiriq sharti:
Tranzaksiya to'xtatilganda bajarilgan amallarni teskari tartibda bekor qiling.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"time"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 25*time.Millisecond)
	defer cancel()

	var kompensatsiyalar []func()

	// 1-bosqich: Omborda mahsulot band qilindi
	fmt.Println("1. Mahsulot band qilindi.")
	kompensatsiyalar = append(kompensatsiyalar, func() {
		fmt.Println("<- Kompensatsiya: Ombordan mahsulot bandi yechildi.")
	})

	// 2-bosqich: To'lov (uzoq vaqt oladi)
	time.Sleep(30 * time.Millisecond)

	if ctx.Err() != nil {
		fmt.Printf("Tranzaksiya bekor qilindi: %v. Bekor qilish amallari:\n", ctx.Err())
		for i := len(kompensatsiyalar) - 1; i >= 0; i-- {
			kompensatsiyalar[i]()
		}
	}
}
```

## Tushuntirish va Mantiq:
Taqsimlangan tranzaksiyalarda (Saga pattern) Context bekor bo'lganda oldingi muvaffaqiyatli bosqichlar kompensatsiya qilinishi (rollback) shart.

## Ishlash natijasi:
```text
1. Mahsulot band qilindi.
Tranzaksiya bekor qilindi: context deadline exceeded. Bekor qilish amallari:
<- Kompensatsiya: Ombordan mahsulot bandi yechildi.
```

# 800-Topshiriq: Taqsimlangan Microservice Orchestrator (Tracing, Timeout, Cancellation)
## Topshiriq sharti:
Keng qamrovli yakuniy loyiha: So'rovlar kontekstini trace qilish, qatlamlararo timeout, xatoliklarni aniqlash va xavfsiz bekor qilishni to'liq mujassam etgan Orxestrator yarating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type traceKey struct{}
type userKey struct{}

type Orchestrator struct{}

func (o *Orchestrator) Bajar(ctx context.Context, buyurtmaID int) error {
	traceID, _ := ctx.Value(traceKey{}).(string)
	user, _ := ctx.Value(userKey{}).(string)
	fmt.Printf("[Orchestrator] Boshlandi: Buyurtma=%d, Trace=%s, User=%s\n", buyurtmaID, traceID, user)

	var wg sync.WaitGroup
	errCh := make(chan error, 2)

	// 1. To'lov xizmati (40ms)
	wg.Add(1)
	go func() {
		defer wg.Done()
		select {
		case <-time.After(40 * time.Millisecond):
			fmt.Println("  -> [To'lov] To'lov qabul qilindi.")
		case <-ctx.Done():
			errCh <- fmt.Errorf("to'lov to'xtatildi: %w", ctx.Err())
		}
	}()

	// 2. Kvitansiya yaratish (30ms)
	wg.Add(1)
	go func() {
		defer wg.Done()
		select {
		case <-time.After(30 * time.Millisecond):
			fmt.Println("  -> [Kvitansiya] Kvitansiya shakllantirildi.")
		case <-ctx.Done():
			errCh <- fmt.Errorf("kvitansiya to'xtatildi: %w", ctx.Err())
		}
	}()

	wg.Wait()
	close(errCh)

	for err := range errCh {
		if err != nil {
			return err
		}
	}

	fmt.Println("[Orchestrator] Barcha xizmatlar muvaffaqiyatli yakunlandi.")
	return nil
}

func main() {
	// Ildiz kontekstga metama'lumotlar va timeout qo'shamiz
	rootCtx := context.Background()
	rootCtx = context.WithValue(rootCtx, traceKey{}, "TRC-ORCH-5511")
	rootCtx = context.WithValue(rootCtx, userKey{}, "jasur")

	ctx, cancel := context.WithTimeout(rootCtx, 60*time.Millisecond)
	defer cancel()

	orc := &Orchestrator{}
	err := orc.Bajar(ctx, 9901)
	if err != nil {
		fmt.Println("Orxestratsiya xatoligi:", err)
	}
}
```

## Tushuntirish va Mantiq:
Zamonaviy Go mikroservis orxestratorlari Tracing, Authorization, Timeout va Cancellation boshqaruvining barchasini `context.Context` daraxti orqali yagona va xavfsiz mexanizmda hal qiladi.

## Ishlash natijasi:
```text
[Orchestrator] Boshlandi: Buyurtma=9901, Trace=TRC-ORCH-5511, User=jasur
  -> [Kvitansiya] Kvitansiya shakllantirildi.
  -> [To'lov] To'lov qabul qilindi.
[Orchestrator] Barcha xizmatlar muvaffaqiyatli yakunlandi.
```

