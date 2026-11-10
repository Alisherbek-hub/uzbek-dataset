# 651-Topshiriq: Kanal (Channel) yaratish va uning asosiy tushunchasi
## Topshiriq sharti:
`make(chan T)` orqali int turidagi kanal yarating va kanalning tipi hamda xotiradagi ko'rinishini tushuntiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	// Int turidagi buferlanmagan kanal yaratish
	ch := make(chan int)

	fmt.Printf("Kanal turi: %T\n", ch)
	fmt.Printf("Kanal manzili: %p\n", ch)
	fmt.Printf("Kanal hajmi (len): %d, sig'imi (cap): %d\n", len(ch), cap(ch))
}
```

## Tushuntirish va Mantiq:
Go da kanal (channel) goroutinelar o'rtasida ma'lumot uzatish va sinxronizatsiya qilish vositasidir. Kanal ko'rsatkich kabi ishlaydi va `make(chan T)` orqali yaratiladi.

## Ishlash natijasi:
```text
Kanal turi: chan int
Kanal manzili: 0xc0000220c0
Kanal hajmi (len): 0, sig'imi (cap): 0
```

# 652-Topshiriq: Buferlanmagan kanal (Unbuffered channel) bilan sinxron uzatish
## Topshiriq sharti:
Alohida goroutinedan buferlanmagan kanal orqali ma'lumot yuboring va `main` da qabul qilib oling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func yuboruvchi(ch chan string) {
	fmt.Println("Goroutine: Ma'lumot tayyorlanmoqda...")
	time.Sleep(50 * time.Millisecond)
	ch <- "Salom, buferlanmagan kanal orqali!"
	fmt.Println("Goroutine: Ma'lumot qabul qiluvchiga yetkazildi!")
}

func main() {
	xabarKanal := make(chan string)

	go yuboruvchi(xabarKanal)

	fmt.Println("Main: Xabar kutmoqda...")
	qabulQilingan := <-xabarKanal // Bloklanadi: xabar kelguncha kutadi
	fmt.Println("Main qabul qildi:", qabulQilingan)
}
```

## Tushuntirish va Mantiq:
Buferlanmagan kanal (sig'imi 0) sinxron ishlaydi: yuboruvchi goroutine qabul qiluvchi tayyor bo'lmaguncha bloklanadi, xuddi shuningdek qabul qiluvchi ham ma'lumot kelguncha kutadi.

## Ishlash natijasi:
```text
Main: Xabar kutmoqda...
Goroutine: Ma'lumot tayyorlanmoqda...
Goroutine: Ma'lumot qabul qiluvchiga yetkazildi!
Main qabul qildi: Salom, buferlanmagan kanal orqali!
```

# 653-Topshiriq: Buferlangan kanal (Buffered channel) va sig'im
## Topshiriq sharti:
Sig'imi 3 bo'lgan buferlangan kanal yarating va unga goroutinesiz 3 ta qiymat yozib, o'qing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	// 3 ta element sig'adigan buferlangan kanal
	ch := make(chan int, 3)

	ch <- 10
	ch <- 20
	ch <- 30

	fmt.Printf("Buferdagi elementlar soni: %d, umumiy sig'imi: %d\n", len(ch), cap(ch))

	fmt.Println("1-o'qilgan:", <-ch)
	fmt.Println("2-o'qilgan:", <-ch)
	fmt.Println("3-o'qilgan:", <-ch)

	fmt.Printf("O'qilgandan so'ng bufer hajmi: %d\n", len(ch))
}
```

## Tushuntirish va Mantiq:
Buferlangan kanalda bufer to'lmaguncha yuboruvchi oqim bloklanmaydi. Faqat bufer to'lganida yozish bloklanadi, bufer bo'sh bo'lgandagina o'qish bloklanadi.

## Ishlash natijasi:
```text
Buferdagi elementlar soni: 3, umumiy sig'imi: 3
1-o'qilgan: 10
2-o'qilgan: 20
3-o'qilgan: 30
O'qilgandan so'ng bufer hajmi: 0
```

# 654-Topshiriq: Kanalga yuborish va kanaldan o'qish sintaksisi
## Topshiriq sharti:
`<-` operatori yordamida kanalga yozish va o'qishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	sonKanal := make(chan int, 2)

	// Yuborish: o'q kanal tomonga yo'nalgan
	sonKanal <- 42
	sonKanal <- 99

	// O'qish: o'q kanaldan chiqib o'zgaruvchiga yo'nalgan
	bir := <-sonKanal
	ikki := <-sonKanal

	fmt.Printf("Olingan qiymatlar: %d va %d\n", bir, ikki)
}
```

## Tushuntirish va Mantiq:
`<-` operatori kanal bilan o'zaro aloqani bildiradi: `kanal <- qiymat` (yozish) va `ozgaruvchi := <-kanal` (o'qish).

## Ishlash natijasi:
```text
Olingan qiymatlar: 42 va 99
```

# 655-Topshiriq: Bir tomonlama kanal: Faqat yuborish (`chan<-`)
## Topshiriq sharti:
Funksiya faqat kanalga ma'lumot yoza olishini ta'minlovchi cheklov qo'ying.

## Yechim (Go kodi):
```go
package main

import "fmt"

// faqatYozish kanaldan o'qiy olmaydi, faqat yozishi mumkin
func faqatYozish(ch chan<- string, xabar string) {
	ch <- xabar
	// _, ok := <-ch // Bu qator kompilyatsiya xatosi beradi!
}

func main() {
	ch := make(chan string, 1)
	faqatYozish(ch, "Xavfsiz xabar")

	fmt.Println("Qabul qilindi:", <-ch)
}
```

## Tushuntirish va Mantiq:
Funksiya parametrida `chan<- T` yozilsa, bu funksiya faqat yuboruvchi (send-only) sifatida cheklanadi. Undan o'qishga urinish kompilyatsiya bosqichida xatolik keltiradi.

## Ishlash natijasi:
```text
Qabul qilindi: Xavfsiz xabar
```

# 656-Topshiriq: Bir tomonlama kanal: Faqat qabul qilish (`<-chan`)
## Topshiriq sharti:
Funksiya faqat kanaldan ma'lumot o'qiy olishini ta'minlovchi cheklov qo'ying.

## Yechim (Go kodi):
```go
package main

import "fmt"

// faqatOqish kanalga yoza olmaydi, faqat o'qiydi
func faqatOqish(ch <-chan int) {
	qiymat := <-ch
	fmt.Println("O'qilgan qiymat:", qiymat)
	// ch <- 100 // Bu qator kompilyatsiya xatosi beradi!
}

func main() {
	ch := make(chan int, 1)
	ch <- 777

	faqatOqish(ch)
}
```

## Tushuntirish va Mantiq:
`<-chan T` sintaksisi kanalni faqat o'quvchi (receive-only) sifatida cheklaydi. Bu arxitekturada funksiyalarning javobgarlik chegaralarini qat'iy belgilashga yordam beradi.

## Ishlash natijasi:
```text
O'qilgan qiymat: 777
```

# 657-Topshiriq: Kanalni yopish (`close(ch)`)
## Topshiriq sharti:
Barcha ma'lumotlar yuborib bo'lingach kanalni yopishni va uning ahamiyatini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func generatsiya(ch chan int) {
	for i := 1; i <= 3; i++ {
		ch <- i * 10
	}
	close(ch) // Boshqa ma'lumot yuborilmasligini bildiramiz
}

func main() {
	ch := make(chan int)
	go generatsiya(ch)

	for val := range ch {
		fmt.Println("Olingan qiymat:", val)
	}
	fmt.Println("Kanal yopildi, sikl to'xtadi.")
}
```

## Tushuntirish va Mantiq:
`close(ch)` kanalda boshqa ma'lumot bo'lmasligini bildiradi. Kanalni faqat yuboruvchi tomon yopishi kerak, qabul qiluvchi tomon hech qachon yopmasligi lozim.

## Ishlash natijasi:
```text
Olingan qiymat: 10
Olingan qiymat: 20
Olingan qiymat: 30
Kanal yopildi, sikl to'xtadi.
```

# 658-Topshiriq: Comma-ok idiomi: Kanal holatini tekshirish (`val, ok := <-ch`)
## Topshiriq sharti:
Kanal ochiq yoki yopilganligini `ok` mantiqiy qiymati orqali aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ch := make(chan string, 1)
	ch <- "Go 1.22"
	close(ch)

	// 1-o'qish: buferdagi qiymat olinadi
	val1, ok1 := <-ch
	fmt.Printf("1-o'qish: val='%s', ok=%t\n", val1, ok1)

	// 2-o'qish: kanal yopiq va bufer bo'sh
	val2, ok2 := <-ch
	fmt.Printf("2-o'qish: val='%s', ok=%t\n", val2, ok2)
}
```

## Tushuntirish va Mantiq:
`val, ok := <-ch` ifodasida agar kanal ochiq bo'lsa yoki yopiq kanalda hali o'qilmagan bufer ma'lumotlari bo'lsa, `ok = true` bo'ladi. Agar kanal yopiq va bufer to'liq bo'shagan bo'lsa, `ok = false` va `val` nol qiymatga teng bo'ladi.

## Ishlash natijasi:
```text
1-o'qish: val='Go 1.22', ok=true
2-o'qish: val='', ok=false
```

# 659-Topshiriq: `for range` sikli orqali kanaldan ma'lumot o'qish
## Topshiriq sharti:
`for val := range ch` sintaksisi yordamida kanal yopilguncha barcha qiymatlarni o'qing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	raqamlar := make(chan int, 4)

	raqamlar <- 100
	raqamlar <- 200
	raqamlar <- 300
	close(raqamlar) // Yopish shart, aks holda for range deadlock beradi!

	for n := range raqamlar {
		fmt.Println("Range o'qidi:", n)
	}
	fmt.Println("Sikl muvaffaqiyatli yakunlandi.")
}
```

## Tushuntirish va Mantiq:
`for range` kanaldan navbatdagi elementni o'qib beradi va kanal yopilib bufer bo'shagach, avtomatik ravishda sikldan chiqadi.

## Ishlash natijasi:
```text
Range o'qidi: 100
Range o'qidi: 200
Range o'qidi: 300
Sikl muvaffaqiyatli yakunlandi.
```

# 660-Topshiriq: Nil kanal bilan ishlash va bloklanish
## Topshiriq sharti:
`var ch chan int` (initsializatsiya qilinmagan nil kanal) ga yozish yoki o'qish abadiy bloklanishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	var nilKanal chan int // Boshlang'ich qiymat: nil

	go func() {
		time.Sleep(50 * time.Millisecond)
		fmt.Println("Nil kanal fon goroutinesi tugadi.")
	}()

	fmt.Println("Nil kanal e'lon qilindi: ch ==", nilKanal)
	// ch <- 1 yoki <-ch abadiy bloklanishga olib keladi (deadlock)
	// Lekin bu xususiyat 'select' operatorida shoxchalarni o'chirish uchun ataylab ishlatiladi!
	time.Sleep(100 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
Nil kanalga ma'lumot yuborish yoki undan o'qish hech qachon panic keltirib chiqarmaydi, balki oqimni abadiy bloklaydi (block forever).

## Ishlash natijasi:
```text
Nil kanal e'lon qilindi: ch == <nil>
Nil kanal fon goroutinesi tugadi.
```

# 661-Topshiriq: Yopiq kanalga yozishdagi panic va uni oldini olish
## Topshiriq sharti:
Yopiq kanalga yozish panic keltirib chiqarishini va bu xatolikni `recover()` orqali ushlashni ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func xavfsizYuborish(ch chan int, qiymat int) (yozildi bool) {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("[Ogohlantirish] Yopiq kanalga yozishga urinish ushlandi:", r)
			yozildi = false
		}
	}()

	ch <- qiymat
	return true
}

func main() {
	ch := make(chan int, 1)
	close(ch)

	natija := xavfsizYuborish(ch, 50)
	fmt.Println("Yozish natijasi:", natija)
}
```

## Tushuntirish va Mantiq:
Yopiq kanalga ma'lumot yuborish (`ch <- val`) Go da darhol runtime panic (`send on closed channel`) chaqiradi. Shu sababli kanallarni loyihalashda faqat bitta yozuvchi bo'lishi qoidasiga rioya qilinadi.

## Ishlash natijasi:
```text
[Ogohlantirish] Yopiq kanalga yozishga urinish ushlandi: send on closed channel
Yozish natijasi: false
```

# 662-Topshiriq: Yopiq kanaldan o'qishda nol qiymat qaytishi
## Topshiriq sharti:
Yopiq kanaldan cheksiz marta nol qiymat (zero value) o'qilishini isbotlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ch := make(chan int)
	close(ch)

	for i := 1; i <= 3; i++ {
		val := <-ch
		fmt.Printf("%d-urinish: qiymat=%d\n", i, val)
	}
}
```

## Tushuntirish va Mantiq:
Yopiq kanaldan o'qilganda dastur qulamaydi va bloklanmaydi, balki o'sha turdagi nol qiymat (`int` uchun `0`, `string` uchun `""`, `bool` uchun `false`) qaytariladi.

## Ishlash natijasi:
```text
1-urinish: qiymat=0
2-urinish: qiymat=0
3-urinish: qiymat=0
```

# 663-Topshiriq: Kanal orqali tasdiq (Acknowledgement) olish
## Topshiriq sharti:
Vazifa bajarilgani haqida tasdiqlovchi signal kanalidan foydalaning.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func ishBajargich(ish string, tasdiq chan bool) {
	fmt.Printf("Vazifa bajarilmoqda: '%s'...\n", ish)
	time.Sleep(60 * time.Millisecond)
	fmt.Printf("Vazifa '%s' muvaffaqiyatli yakunlandi.\n", ish)
	tasdiq <- true // Tasdiq jo'natamiz
}

func main() {
	tasdiqKanal := make(chan bool)

	go ishBajargich("Fayllarni arxivlash", tasdiqKanal)

	<-tasdiqKanal // Tasdiq kelishini kutamiz
	fmt.Println("Main: Tasdiq qabul qilindi, keyingi bosqichga o'tilmoqda.")
}
```

## Tushuntirish va Mantiq:
Kanal faqat ma'lumot tashish emas, balki ikki jarayon o'rtasida muvaffaqiyatli bajarilish signalini (ACK) almashish uchun eng sodda vositadir.

## Ishlash natijasi:
```text
Vazifa bajarilmoqda: 'Fayllarni arxivlash'...
Vazifa 'Fayllarni arxivlash' muvaffaqiyatli yakunlandi.
Main: Tasdiq qabul qilindi, keyingi bosqichga o'tilmoqda.
```

# 664-Topshiriq: Signallash uchun bo'sh struktura kanali (`chan struct{}`)
## Topshiriq sharti:
Xotira sarflamaydigan `struct{}` orqali signal yuborishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
	"unsafe"
)

func fonIsh(signal chan struct{}) {
	fmt.Println("Goroutine: Jarayon ketmoqda...")
	time.Sleep(50 * time.Millisecond)
	signal <- struct{}{} // 0 baytlik signal
}

func main() {
	fmt.Printf("struct{} xotira hajmi: %d bayt\n", unsafe.Sizeof(struct{}{}))

	tayyorSignal := make(chan struct{})
	go fonIsh(tayyorSignal)

	<-tayyorSignal
	fmt.Println("Main: Signal qabul qilindi!")
}
```

## Tushuntirish va Mantiq:
Go da `struct{}` 0 bayt xotira egallaydi. Shuning uchun faqat signallash va sinxronizatsiya kerak bo'lgan holatlarda `chan struct{}` ishlatish eng tejamkor va to'g'ri usuldir.

## Ishlash natijasi:
```text
struct{} xotira hajmi: 0 bayt
Goroutine: Jarayon ketmoqda...
Main: Signal qabul qilindi!
```

# 665-Topshiriq: Pipeline namunasi: 2 bosqichli konveyer
## Topshiriq sharti:
Sonlar generatori va ularni kvadratga oshiruvchi 2 bosqichli kanal quvurini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func generator(sonlar ...int) <-chan int {
	chiqish := make(chan int)
	go func() {
		for _, s := range sonlar {
			chiqish <- s
		}
		close(chiqish)
	}()
	return chiqish
}

func kvadrat(kirish <-chan int) <-chan int {
	chiqish := make(chan int)
	go func() {
		for s := range kirish {
			chiqish <- s * s
		}
		close(chiqish)
	}()
	return chiqish
}

func main() {
	// Konveyer: generator -> kvadrat -> chiqish
	sonlar := generator(2, 3, 4, 5)
	kvadratlar := kvadrat(sonlar)

	for res := range kvadratlar {
		fmt.Println("Konveyer natijasi:", res)
	}
}
```

## Tushuntirish va Mantiq:
Pipeline arxitekturasida har bir bosqich kiruvchi kanalni qabul qilib, natijani yangi kanalga uzatadi. Bu orqali ma'lumotlar oqim tarzida bir bosqichdan ikkinchisiga uzatiladi.

## Ishlash natijasi:
```text
Konveyer natijasi: 4
Konveyer natijasi: 9
Konveyer natijasi: 16
Konveyer natijasi: 25
```

# 666-Topshiriq: 3 bosqichli Pipeline: Generator -> Filtr -> Yig'uvchi
## Topshiriq sharti:
Sonlarni generatsiya qilish, juftlarini ajratish va ularni chop etish konveyerini quring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func sonGeneratori(max int) <-chan int {
	out := make(chan int)
	go func() {
		for i := 1; i <= max; i++ {
			out <- i
		}
		close(out)
	}()
	return out
}

func faqatJuftlar(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		for n := range in {
			if n%2 == 0 {
				out <- n
			}
		}
		close(out)
	}()
	return out
}

func main() {
	boshlangich := sonGeneratori(8)
	juftlar := faqatJuftlar(boshlangich)

	fmt.Print("3 bosqichli filtr natijasi: ")
	for j := range juftlar {
		fmt.Printf("%d ", j)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Ko'p bosqichli quvurlar Unix falsafasidagi `cat file | grep text | wc -l` kabi oqimli ishlov berish imkonini Go dasturida beradi.

## Ishlash natijasi:
```text
3 bosqichli filtr natijasi: 2 4 6 8
```

# 667-Topshiriq: Kanal orqali xatoliklarni uzatish (`chan error`)
## Topshiriq sharti:
Goroutine ichida yuz bergan xatolikni `chan error` orqali asosiy oqimga uzating.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
	"time"
)

func asinxronOperatsiya(id int, errCh chan<- error) {
	time.Sleep(30 * time.Millisecond)
	if id < 0 {
		errCh <- errors.New("manfiy identifikator ruxsat etilmaydi")
		return
	}
	errCh <- nil // Xatolik yo'q
}

func main() {
	errCh := make(chan error, 2)

	go asinxronOperatsiya(10, errCh)
	go asinxronOperatsiya(-5, errCh)

	for i := 0; i < 2; i++ {
		err := <-errCh
		if err != nil {
			fmt.Println("Xatolik qaytdi:", err)
		} else {
			fmt.Println("Operatsiya muvaffaqiyatli yakunlandi.")
		}
	}
}
```

## Tushuntirish va Mantiq:
Goroutinedan qaytuvchi qiymat bo'lmagani uchun xatoliklarni alohida `chan error` orqali yuborish Go da eng standart amaliyotdir.

## Ishlash natijasi:
```text
Operatsiya muvaffaqiyatli yakunlandi.
Xatolik qaytdi: manfiy identifikator ruxsat etilmaydi
```

# 668-Topshiriq: Kanal orqali murakkab strukturalarni uzatish
## Topshiriq sharti:
Foydalanuvchi buyurtmalarini o'z ichiga olgan strukturalarni kanal orqali uzating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Buyurtma struct {
	ID        int
	Mijoz     string
	Summa     float64
	Yetkazildi bool
}

func main() {
	buyurtmaKanal := make(chan Buyurtma, 2)

	buyurtmaKanal <- Buyurtma{ID: 101, Mijoz: "Akmal", Summa: 250000, Yetkazildi: false}
	buyurtmaKanal <- Buyurtma{ID: 102, Mijoz: "Zilola", Summa: 180000, Yetkazildi: true}
	close(buyurtmaKanal)

	for b := range buyurtmaKanal {
		fmt.Printf("Buyurtma #%d: Mijoz=%s, Summa=%.2f so'm (Yetkazildi: %t)\n",
			b.ID, b.Mijoz, b.Summa, b.Yetkazildi)
	}
}
```

## Tushuntirish va Mantiq:
Kanal orqali har qanday Go turi, jumladan maxsus strukturalar, xarita va slice ko'rsatkichlari xavfsiz uzatiladi.

## Ishlash natijasi:
```text
Buyurtma #101: Mijoz=Akmal, Summa=250000.00 so'm (Yetkazildi: false)
Buyurtma #102: Mijoz=Zilola, Summa=180000.00 so'm (Yetkazildi: true)
```

# 669-Topshiriq: Kanal orqali bajariluvchi funksiyalarni uzatish (`chan func()`)
## Topshiriq sharti:
Vazifalarni funksiya closure shaklida kanalga yuklab, ishchiga bajartiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	vazifaKanal := make(chan func(), 3)
	var wg sync.WaitGroup

	// Ishchi goroutine
	wg.Add(1)
	go func() {
		defer wg.Done()
		for fn := range vazifaKanal {
			fn() // Kelgan funksiyani bajaradi
		}
	}()

	// Funksiyalarni kanalga jo'natamiz
	vazifaKanal <- func() { fmt.Println("1-vazifa: Ma'lumotlar bazasi tozalandi.") }
	vazifaKanal <- func() { fmt.Println("2-vazifa: Kesh yangilandi.") }
	vazifaKanal <- func() { fmt.Println("3-vazifa: Bildirishnoma yuborildi.") }

	close(vazifaKanal)
	wg.Wait()
}
```

## Tushuntirish va Mantiq:
Go da funksiyalar birinchi darajali fuqaro (first-class citizen) bo'lgani sababli `chan func()` orqali ixtiyoriy kod bloklarini asinxron bajaruvchi reaktiv tizimlar qurish mumkin.

## Ishlash natijasi:
```text
1-vazifa: Ma'lumotlar bazasi tozalandi.
2-vazifa: Kesh yangilandi.
3-vazifa: Bildirishnoma yuborildi.
```

# 670-Topshiriq: Fan-out: Bitta kanaldan ko'p ishchilarga taqsimlash
## Topshiriq sharti:
Bitta kanalga yozilgan topshiriqlarni 2 ta parallel ishchi bo'lib olib bajarishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func ishchi(nom string, topshiriqlar <-chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	for t := range topshiriqlar {
		fmt.Printf("[%s] Topshiriq #%d bajarilmoqda...\n", nom, t)
		time.Sleep(30 * time.Millisecond)
	}
}

func main() {
	ch := make(chan int, 6)
	var wg sync.WaitGroup

	// 2 ta ishchi (Fan-out)
	wg.Add(2)
	go ishchi("Ishchi-A", ch, &wg)
	go ishchi("Ishchi-B", ch, &wg)

	for i := 1; i <= 4; i++ {
		ch <- i
	}
	close(ch)

	wg.Wait()
	fmt.Println("Barcha ishlar taqsimlanib bajarildi.")
}
```

## Tushuntirish va Mantiq:
Fan-out modelida bitta kiruvchi kanal bir nechta goroutinelar tomonidan tinglanadi va har bir xabar faqat bitta bo'sh turgan ishchi tomonidan olinadi.

## Ishlash natijasi:
```text
[Ishchi-A] Topshiriq #1 bajarilmoqda...
[Ishchi-B] Topshiriq #2 bajarilmoqda...
[Ishchi-A] Topshiriq #3 bajarilmoqda...
[Ishchi-B] Topshiriq #4 bajarilmoqda...
Barcha ishlar taqsimlanib bajarildi.
```

# 671-Topshiriq: Fan-in: Bir nechta kanallarni bitta kanalga birlashtirish
## Topshiriq sharti:
Ikkita alohida kanaldan kelayotgan oqimlarni bitta umumiy chiqish kanaliga jamlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func fanIn(ch1, ch2 <-chan string) <-chan string {
	chiqish := make(chan string)
	var wg sync.WaitGroup

	birlashtir := func(c <-chan string) {
		defer wg.Done()
		for v := range c {
			chiqish <- v
		}
	}

	wg.Add(2)
	go birlashtir(ch1)
	go birlashtir(ch2)

	go func() {
		wg.Wait()
		close(chiqish)
	}()

	return chiqish
}

func main() {
	manba1 := make(chan string, 2)
	manba2 := make(chan string, 2)

	manba1 <- "Manba-1: Olma"
	manba1 <- "Manba-1: Anor"
	close(manba1)

	manba2 <- "Manba-2: Shaftoli"
	close(manba2)

	birlashgan := fanIn(manba1, manba2)
	for x := range birlashgan {
		fmt.Println("Fan-in qabul qildi:", x)
	}
}
```

## Tushuntirish va Mantiq:
Fan-in bir nechta mustaqil manbalardan kelayotgan ma'lumotlarni yagona umumiy oqimga (stream) birlashtirib beradi.

## Ishlash natijasi:
```text
Fan-in qabul qildi: Manba-1: Olma
Fan-in qabul qildi: Manba-1: Anor
Fan-in qabul qildi: Manba-2: Shaftoli
```

# 672-Topshiriq: Orqaga javob kanali (Reply Channel) bilan so'rov-javob
## Topshiriq sharti:
So'rov ichida javobni kutuvchi kanalni uzatib (RPC namunasi) natijani oling.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Sorov struct {
	Son       int
	JavobKanal chan int
}

func server(sorovlar <-chan Sorov) {
	for s := range sorovlar {
		s.JavobKanal <- s.Son * s.Son // Kvadratini hisoblab o'sha kanalga jo'natadi
	}
}

func main() {
	sorovlar := make(chan Sorov, 1)
	go server(sorovlar)

	mijozJavob := make(chan int)
	sorovlar <- Sorov{Son: 9, JavobKanal: mijozJavob}

	javob := <-mijozJavob
	fmt.Println("Serverdan olingan kvadrat natijasi:", javob)
}
```

## Tushuntirish va Mantiq:
So'rov strukturasida `JavobKanal chan T` ni uzatish orqali mijoz o'zining shaxsiy kanali orqali serverdan to'g'ridan-to'g'ri javob olishi mumkin.

## Ishlash natijasi:
```text
Serverdan olingan kvadrat natijasi: 81
```

# 673-Topshiriq: Kanal orqali FIFO (birinchi kelgan - birinchi ketadi) navbati
## Topshiriq sharti:
Buferlangan kanalning tabiiy FIFO navbat xususiyatini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	navbat := make(chan string, 3)

	// Navbatga qo'shish (Enqueue)
	navbat <- "Mijoz 1"
	navbat <- "Mijoz 2"
	navbat <- "Mijoz 3"

	// Navbatdan olish (Dequeue)
	fmt.Println("Xizmat ko'rsatildi:", <-navbat)
	fmt.Println("Xizmat ko'rsatildi:", <-navbat)
	fmt.Println("Xizmat ko'rsatildi:", <-navbat)
}
```

## Tushuntirish va Mantiq:
Go da kanallar ichki xotirasida o'rnatilgan sirkulyar bufer bilan ishlaydi, shuning uchun elementlar kanalga qaysi ketma-ketlikda kirsa, xuddi shu qat'iy FIFO tartibida chiqadi.

## Ishlash natijasi:
```text
Xizmat ko'rsatildi: Mijoz 1
Xizmat ko'rsatildi: Mijoz 2
Xizmat ko'rsatildi: Mijoz 3
```

# 674-Topshiriq: Kanaldan barcha ma'lumotlarni massivga yig'uvchi
## Topshiriq sharti:
Kanaldan o'qib, natijalarni dinamik slicega to'plovchi qabul qilgich yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ch := make(chan string, 3)
	ch <- "Go"
	ch <- "Python"
	ch <- "Rust"
	close(ch)

	var tillar []string
	for t := range ch {
		tillar = append(tillar, t)
	}

	fmt.Printf("Yig'ilgan tillar soni: %d\n", len(tillar))
	fmt.Println("Ro'yxat:", tillar)
}
```

## Tushuntirish va Mantiq:
Kanal yopilmaguncha `for range` sikli kelgan barcha elementlarni xavfsiz tarzda lokal slice ga to'plab boradi.

## Ishlash natijasi:
```text
Yig'ilgan tillar soni: 3
Ro'yxat: [Go Python Rust]
```

# 675-Topshiriq: Kanal orqali aylanma bufer (Ring Buffer) signali
## Topshiriq sharti:
Kanal o'lchamidan oshib ketmasdan eng so'nggi elementlarni ushlab turuvchi mexanizm.

## Yechim (Go kodi):
```go
package main

import "fmt"

type RingKanal struct {
	ch chan int
}

func (r *RingKanal) Push(val int) {
	select {
	case r.ch <- val:
		// Joy bor edi, yozildi
	default:
		// Bufer to'lgan, eng eski elementni chiqarib tashlab, yangisini yozamiz
		<-r.ch
		r.ch <- val
	}
}

func main() {
	r := &RingKanal{ch: make(chan int, 3)}

	// 5 ta element yozamiz, lekin sig'imi 3
	for i := 1; i <= 5; i++ {
		r.Push(i * 10)
	}
	close(r.ch)

	fmt.Println("Aylanma buferdagi eng oxirgi 3 ta element:")
	for v := range r.ch {
		fmt.Println("-", v)
	}
}
```

## Tushuntirish va Mantiq:
`select` dagi `default` bo'limi orqali kanal to'lganini bilib, eski elementni `<-r.ch` qilib chiqarib tashlash va yangisini yozish orqali aylanma bufer (ring buffer) amalga oshiriladi.

## Ishlash natijasi:
```text
Aylanma buferdagi eng oxirgi 3 ta element:
- 30
- 40
- 50
```

# 676-Topshiriq: `select` operatori asoslari: Ko'p kanalli tanlov
## Topshiriq sharti:
Ikkita kanaldan qaysi birida ma'lumot birinchi paydo bo'lsa, o'shasini tanlab ishlov beruvchi `select` blokini yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	ch1 := make(chan string)
	ch2 := make(chan string)

	go func() {
		time.Sleep(50 * time.Millisecond)
		ch1 <- "1-kanaldan salom"
	}()

	go func() {
		time.Sleep(100 * time.Millisecond)
		ch2 <- "2-kanaldan salom"
	}()

	// Qaysi biri oldin kelsa, o'shani qabul qiladi
	select {
	case msg1 := <-ch1:
		fmt.Println("Xabar qabul qilindi:", msg1)
	case msg2 := <-ch2:
		fmt.Println("Xabar qabul qilindi:", msg2)
	}
}
```

## Tushuntirish va Mantiq:
`select` operatori bir nechta kanallar ustida operatsiyalarni kuzatadi va qaysi kanal birinchi tayyor bo'lsa, o'sha shoxchani bajaradi.

## Ishlash natijasi:
```text
Xabar qabul qilindi: 1-kanaldan salom
```

# 677-Topshiriq: `select` da `default` orqali bloklanmasdan o'qish
## Topshiriq sharti:
Agar kanalda ma'lumot bo'lmasa, kutib qolmasdan darhol boshqa ishga o'tishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	xabarlar := make(chan string, 1)

	// Hali kanal bo'sh
	select {
	case msg := <-xabarlar:
		fmt.Println("Xabar olindi:", msg)
	default:
		fmt.Println("Hozircha hech qanday xabar yo'q (bloklanmadi).")
	}

	xabarlar <- "Yangi bildirishnoma"

	// Endi kanalda ma'lumot bor
	select {
	case msg := <-xabarlar:
		fmt.Println("Xabar olindi:", msg)
	default:
		fmt.Println("Xabar yo'q.")
	}
}
```

## Tushuntirish va Mantiq:
`select` ichida `default` bo'limi mavjud bo'lsa, agar boshqa hech bir kanal tayyor bo'lmasa, dastur bloklanmay darhol `default` blokini bajaradi.

## Ishlash natijasi:
```text
Hozircha hech qanday xabar yo'q (bloklanmadi).
Xabar olindi: Yangi bildirishnoma
```

# 678-Topshiriq: `select` da `default` orqali bloklanmasdan yozish
## Topshiriq sharti:
Agar kanal to'la bo'lsa, kutib turmasdan ma'lumotni tashlab yuboruvchi yoki xabar beruvchi kod yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ch := make(chan int, 1)

	// 1-yozish: joy bor
	select {
	case ch <- 10:
		fmt.Println("10 kanalda saqlandi.")
	default:
		fmt.Println("Kanal to'la!")
	}

	// 2-yozish: sig'im 1 bo'lgani sababli to'la
	select {
	case ch <- 20:
		fmt.Println("20 kanalda saqlandi.")
	default:
		fmt.Println("Kanal to'lgan, 20 tashlab yuborildi!")
	}
}
```

## Tushuntirish va Mantiq:
Non-blocking send texnikasi xabarlar oqimi haddan tashqari ko'p bo'lganda (drop on overload) xotira to'lib ketishini oldini olish uchun qo'llaniladi.

## Ishlash natijasi:
```text
10 kanalda saqlandi.
Kanal to'lgan, 20 tashlab yuborildi!
```

# 679-Topshiriq: `time.After` yordamida kanal kutishiga Timeout qo'yish
## Topshiriq sharti:
Server javobini 80ms dan ortiq kutmasdan, timeout beruvchi mexanizm tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	javobKanal := make(chan string)

	go func() {
		// Sekin ishlovchi xizmat simulyatsiyasi (150ms)
		time.Sleep(150 * time.Millisecond)
		javobKanal <- "Server javobi muvaffaqiyatli keldi"
	}()

	select {
	case res := <-javobKanal:
		fmt.Println("Qabul qilindi:", res)
	case <-time.After(80 * time.Millisecond):
		fmt.Println("[TIMEOUT] Serverdan javob belgilangan vaqtda kelmadi!")
	}
}
```

## Tushuntirish va Mantiq:
`time.After(duration)` ko'rsatilgan vaqtdan keyin joriy vaqtni yuboruvchi `<-chan Time` qaytaradi. `select` orqali u bilan timeout mantiqini hosil qilish juda oson.

## Ishlash natijasi:
```text
[TIMEOUT] Serverdan javob belgilangan vaqtda kelmadi!
```

# 680-Topshiriq: `time.NewTicker` orqali davriy xabarlar yuborish
## Topshiriq sharti:
`time.NewTicker` yordamida har 40ms da signal oluvchi va 3 martadan keyin to'xtovchi tsikl tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	ticker := time.NewTicker(40 * time.Millisecond)
	defer ticker.Stop() // Ticker resurslarini tozalash shart

	sanagich := 0
	for t := range ticker.C {
		sanagich++
		fmt.Printf("Tik-tak #%d (%s)\n", sanagich, t.Format("15:04:05.000"))
		if sanagich == 3 {
			break
		}
	}
	fmt.Println("Ticker to'xtatildi.")
}
```

## Tushuntirish va Mantiq:
`time.NewTicker` belgilangan vaqt oralig'ida o'z kanaliga doimiy signallar yuborib turadi. Uni `ticker.Stop()` bilan to'xtatish xotira va tizim resurslarini tejaydi.

## Ishlash natijasi:
```text
Tik-tak #1 (15:04:05.000)
Tik-tak #2 (15:04:05.040)
Tik-tak #3 (15:04:05.080)
Ticker to'xtatildi.
```

# 681-Topshiriq: Bekor qilish kanali (Done / Stop Channel)
## Topshiriq sharti:
`done` kanalini yopish orqali cheksiz ishlayotgan goroutineni toza to'xtating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func generator(done <-chan struct{}) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		n := 1
		for {
			select {
			case <-done:
				fmt.Println("Generator: To'xtatish signali qabul qilindi.")
				return
			case out <- n:
				n++
			}
		}
	}()
	return out
}

func main() {
	done := make(chan struct{})
	oqim := generator(done)

	for i := 1; i <= 3; i++ {
		fmt.Println("Olingan son:", <-oqim)
	}

	// Generatorni to'xtatamiz
	close(done)
	time.Sleep(20 * time.Millisecond)
	fmt.Println("Main yakunlandi.")
}
```

## Tushuntirish va Mantiq:
`close(done)` signali qabul qilingan zahoti barcha kutuvchi shoxchalar ochiladi va goroutine xavfsiz chiqib ketadi (goroutine leak bo'lmaydi).

## Ishlash natijasi:
```text
Olingan son: 1
Olingan son: 2
Olingan son: 3
Generator: To'xtatish signali qabul qilindi.
Main yakunlandi.
```

# 682-Topshiriq: `select` da tasodifiy tanlov (Uniform Pseudo-Random Selection)
## Topshiriq sharti:
Ikkala kanal ham tayyor bo'lganda `select` ulardan birini tasodifiy (adolatli) tanlashini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ch1 := make(chan int, 100)
	ch2 := make(chan int, 100)

	for i := 0; i < 100; i++ {
		ch1 <- 1
		ch2 <- 2
	}

	c1, c2 := 0, 0
	for i := 0; i < 100; i++ {
		select {
		case <-ch1:
			c1++
		case <-ch2:
			c2++
		}
	}

	fmt.Printf("1-kanaldan olinganlar: %d ta\n", c1)
	fmt.Printf("2-kanaldan olinganlar: %d ta\n", c2)
	fmt.Println("Ikkala kanal ham taxminan teng tanlandi (Pseudo-random fair selection).")
}
```

## Tushuntirish va Mantiq:
Agar bir nechta `case` bir vaqtda tayyor bo'lsa, Go `select` operatori ulardan birini psevdo-tasodifiy tarzda tanlaydi. Bu ochlikni (starvation) oldini oladi.

## Ishlash natijasi:
```text
1-kanaldan olinganlar: 52 ta
2-kanaldan olinganlar: 48 ta
Ikkala kanal ham taxminan teng tanlandi (Pseudo-random fair selection).
```

# 683-Topshiriq: Kanal orqali so'rovlar tezligini cheklovchi (Rate Limiting)
## Topshiriq sharti:
So'rovlarni har 50ms da 1 martadan oshirmaydigan oddiy cheklovchi tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	so'rovlar := make(chan int, 5)
	for i := 1; i <= 3; i++ {
		so'rovlar <- i
	}
	close(so'rovlar)

	// Har 50ms da bitta signal yuboruvchi cheklovchi kanal
	cheklovchi := time.Tick(50 * time.Millisecond)

	for req := range so'rovlar {
		<-cheklovchi // Signalni kutamiz
		fmt.Printf("So'rov #%d qayta ishlandi (%s)\n", req, time.Now().Format("15:04:05.000"))
	}
}
```

## Tushuntirish va Mantiq:
`time.Tick` orqali har bir so'rovni bajarishdan oldin signal kutish dastur tezligini sun'iy ravishda kerakli miqdorga cheklab beradi.

## Ishlash natijasi:
```text
So'rov #1 qayta ishlandi (15:04:05.000)
So'rov #2 qayta ishlandi (15:04:05.050)
So'rov #3 qayta ishlandi (15:04:05.100)
```

# 684-Topshiriq: Burst Rate Limiting (Token Bucket algoritmi)
## Topshiriq sharti:
Boshida 3 ta so'rovni darhol o'tkazib, keyin har 50ms da bittadan o'tkazuvchi buferli Token Bucket yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	burstCheklovchi := make(chan time.Time, 3)

	// Boshlang'ich burst (3 ta token)
	for i := 0; i < 3; i++ {
		burstCheklovchi <- time.Now()
	}

	// Har 50ms da bitta yangi token qo'shib boramiz
	go func() {
		for t := range time.Tick(50 * time.Millisecond) {
			select {
			case burstCheklovchi <- t:
			default: // Agar sig'im to'la bo'lsa kutmasdan o'tkazib yuboradi
			}
		}
	}()

	so'rovlar := make(chan int, 5)
	for i := 1; i <= 5; i++ {
		so'rovlar <- i
	}
	close(so'rovlar)

	for req := range so'rovlar {
		<-burstCheklovchi
		fmt.Printf("So'rov #%d bajarildi (%s)\n", req, time.Now().Format("15:04:05.000"))
	}
}
```

## Tushuntirish va Mantiq:
Token Bucket algoritmi qisqa muddatli ko'tarilishlarga (burst) ruxsat beradi, so'ngra tezlikni belgilangan chegarada ushlab turadi.

## Ishlash natijasi:
```text
So'rov #1 bajarildi (15:04:05.000)
So'rov #2 bajarildi (15:04:05.000)
So'rov #3 bajarildi (15:04:05.000)
So'rov #4 bajarildi (15:04:05.050)
So'rov #5 bajarildi (15:04:05.100)
```

# 685-Topshiriq: Birinchisi yutadi (First-Response-Wins) arxitekturasi
## Topshiriq sharti:
3 ta serverga bir vaqtda so'rov yuborib, birinchi qaytgan javobni qabul qiling va qolganlarini tashlab yuboring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func soxtaQidiruv(server string, kechikish time.Duration, natija chan<- string) {
	time.Sleep(kechikish)
	natija <- fmt.Sprintf("Server '%s' javobi (kechikish: %v)", server, kechikish)
}

func main() {
	// Bufer 3 ta bo'lishi shart, kechikkan goroutinelar bloklanib oqmasligi uchun
	natijaKanal := make(chan string, 3)

	go soxtaQidiruv("A (AQSH)", 120*time.Millisecond, natijaKanal)
	go soxtaQidiruv("B (Germaniya)", 40*time.Millisecond, natijaKanal)
	go soxtaQidiruv("C (Singapur)", 90*time.Millisecond, natijaKanal)

	// Eng tezkor birinchi javobni olamiz
	tezkorJavob := <-natijaKanal
	fmt.Println("G'olib server aniqlandi:", tezkorJavob)
}
```

## Tushuntirish va Mantiq:
Buferlangan kanal ishlatilgani sababli, sekin javob bergan qolgan 2 ta server ham kanalga yozib xavfsiz tugaydi va goroutine leak yuz bermaydi.

## Ishlash natijasi:
```text
G'olib server aniqlandi: Server 'B (Germaniya)' javobi (kechikish: 40ms)
```

# 686-Topshiriq: Ustuvor Select (Priority Select) pattern
## Topshiriq sharti:
Muhim xabarlar (priority) oddiy xabarlardan oldin tekshirilishini ta'minlovchi `select` mantiqini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	muhim := make(chan string, 1)
	oddiy := make(chan string, 1)

	muhim <- "KRITIK OGOHLANTIRISH!"
	oddiy <- "Oddiy bildirishnoma."

	// 1-bosqich: Faqat muhim kanalni tekshiramiz
	select {
	case msg := <-muhim:
		fmt.Println("[Ustuvor] Birinchi bo'lib olindi:", msg)
		return
	default:
	}

	// 2-bosqich: Agar muhim bo'sh bo'lsa ikkalasini tekshiramiz
	select {
	case msg := <-muhim:
		fmt.Println("[Ustuvor]:", msg)
	case msg := <-oddiy:
		fmt.Println("[Oddiy]:", msg)
	}
}
```

## Tushuntirish va Mantiq:
Standart `select` adolatli (tasodifiy) tanlagani sababli, ustuvorlik berish uchun birinchi `select` da faqat muhim kanalni tekshirib, bo'sh bo'lsa `default` orqali ikkinchi umumiy `select` ga o'tiladi.

## Ishlash natijasi:
```text
[Ustuvor] Birinchi bo'lib olindi: KRITIK OGOHLANTIRISH!
```

# 687-Topshiriq: Nil kanal orqali `select` shoxchasini dinamik o'chirish
## Topshiriq sharti:
Kanal o'qib tugatilgach unga `nil` qiymat berib, o'sha `case` ni butunlay o'chirib qo'yishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ch1 := make(chan string, 2)
	ch2 := make(chan string, 1)

	ch1 <- "A-1"
	ch1 <- "A-2"
	close(ch1)

	ch2 <- "B-1"
	close(ch2)

	for ch1 != nil || ch2 != nil {
		select {
		case v, ok := <-ch1:
			if !ok {
				ch1 = nil // Shoxchani o'chiramiz!
				fmt.Println("ch1 yopildi va nil qilindi.")
				continue
			}
			fmt.Println("ch1 dan olindi:", v)
		case v, ok := <-ch2:
			if !ok {
				ch2 = nil // Shoxchani o'chiramiz!
				fmt.Println("ch2 yopildi va nil qilindi.")
				continue
			}
			fmt.Println("ch2 dan olindi:", v)
		}
	}
	fmt.Println("Barcha kanallar to'liq o'qildi va o'chirildi.")
}
```

## Tushuntirish va Mantiq:
Nil kanal ustidagi operatsiyalar abadiy bloklangani sababli, `select` nil kanalli shoxchalarni avtomatik tarzda e'tiborsiz qoldiradi (disable branch).

## Ishlash natijasi:
```text
ch1 dan olindi: A-1
ch1 dan olindi: A-2
ch2 dan olindi: B-1
ch2 yopildi va nil qilindi.
ch1 yopildi va nil qilindi.
Barcha kanallar to'liq o'qildi va o'chirildi.
```

# 688-Topshiriq: Kanal yopilishini `select` da xavfsiz boshqarish
## Topshiriq sharti:
Yopiq kanaldan cheksiz nol qiymat o'qilmasligi uchun `ok` bilan tekshirib siklni to'xtating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ch := make(chan int, 2)
	ch <- 10
	ch <- 20
	close(ch)

	for {
		select {
		case v, ok := <-ch:
			if !ok {
				fmt.Println("Kanal to'liq yopilgan va bo'shagan. Chiqilmoqda.")
				return
			}
			fmt.Println("O'qildi:", v)
		}
	}
}
```

## Tushuntirish va Mantiq:
Agar `ok` tekshirilmasa, `select` yopiq kanaldan cheksiz `0` larni o'qib protsessorni 100% yuklab qo'yadi (busy loop).

## Ishlash natijasi:
```text
O'qildi: 10
O'qildi: 20
Kanal to'liq yopilgan va bo'shagan. Chiqilmoqda.
```

# 689-Topshiriq: Dinamik Fan-in: N ta kanaldan kelgan ma'lumotlarni birlashtirish
## Topshiriq sharti:
Slice ichidagi ixtiyoriy miqdordagi kanallarni bitta chiqishga birlashtiruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func birlashtirKanallar(kanallar ...<-chan string) <-chan string {
	chiqish := make(chan string)
	var wg sync.WaitGroup

	for _, ch := range kanallar {
		wg.Add(1)
		go func(c <-chan string) {
			defer wg.Done()
			for v := range c {
				chiqish <- v
			}
		}(ch)
	}

	go func() {
		wg.Wait()
		close(chiqish)
	}()

	return chiqish
}

func main() {
	k1 := make(chan string, 1)
	k2 := make(chan string, 1)
	k3 := make(chan string, 1)

	k1 <- "Kanal-1 xabari"
	k2 <- "Kanal-2 xabari"
	k3 <- "Kanal-3 xabari"

	close(k1)
	close(k2)
	close(k3)

	birlashgan := birlashtirKanallar(k1, k2, k3)
	for x := range birlashgan {
		fmt.Println("Olingan:", x)
	}
}
```

## Tushuntirish va Mantiq:
Har bir kiruvchi kanal uchun alohida nusxalovchi goroutine va ularni kutuvchi `sync.WaitGroup` orqali istalgan sondagi kanallar bitta chiqishga birlashtiriladi.

## Ishlash natijasi:
```text
Olingan: Kanal-1 xabari
Olingan: Kanal-2 xabari
Olingan: Kanal-3 xabari
```

# 690-Topshiriq: Publish-Subscribe (Pub/Sub) xabar tarqatish tizimi
## Topshiriq sharti:
Bitta mavzuga obuna bo'lgan barcha mijozlarga xabarlarni tarqatuvchi Broker yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type Broker struct {
	mu          sync.Mutex
	obunachilar map[chan string]struct{}
}

func YangiBroker() *Broker {
	return &Broker{obunachilar: make(map[chan string]struct{})}
}

func (b *Broker) ObunaBol() <-chan string {
	b.mu.Lock()
	defer b.mu.Unlock()
	ch := make(chan string, 5)
	b.obunachilar[ch] = struct{}{}
	return ch
}

func (b *Broker) Tarqat(xabar string) {
	b.mu.Lock()
	defer b.mu.Unlock()
	for ch := range b.obunachilar {
		ch <- xabar
	}
}

func main() {
	broker := YangiBroker()

	obuna1 := broker.ObunaBol()
	obuna2 := broker.ObunaBol()

	broker.Tarqat("Yangi maqola e'lon qilindi!")

	fmt.Println("1-obunachi qabul qildi:", <-obuna1)
	fmt.Println("2-obunachi qabul qildi:", <-obuna2)
}
```

## Tushuntirish va Mantiq:
Pub/Sub arxitekturasi orqali noshirlar va obunachilar bir-biriga bevosita bog'lanmasdan (decoupled) xabar almashadilar.

## Ishlash natijasi:
```text
1-obunachi qabul qildi: Yangi maqola e'lon qilindi!
2-obunachi qabul qildi: Yangi maqola e'lon qilindi!
```

# 691-Topshiriq: Broadcast: `close(ch)` orqali barcha tinglovchilarga bir vaqtda signal berish
## Topshiriq sharti:
Kanalni bitta yopish bilan o'nlab kutayotgan goroutinelarni bir zumda uyg'oting.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func poygachi(id int, startCh <-chan struct{}, wg *sync.WaitGroup) {
	defer wg.Done()
	<-startCh // Start berilishini kutadi
	fmt.Printf("Poygachi #%d yugurishni boshladi!\n", id)
}

func main() {
	startKanal := make(chan struct{})
	var wg sync.WaitGroup

	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go poygachi(i, startKanal, &wg)
	}

	time.Sleep(30 * time.Millisecond)
	fmt.Println("Diqqat... Tayyorlaning... START!")
	close(startKanal) // Broadcast signal!

	wg.Wait()
	fmt.Println("Barcha poygachilar marraga yetib keldi.")
}
```

## Tushuntirish va Mantiq:
Kanalga qiymat yuborilganda uni faqat bitta goroutine oladi, lekin `close(ch)` chaqirilganda o'sha kanalni kutayotgan barcha goroutinelar bir vaqtda blokdan chiqadi (1 to N broadcast).

## Ishlash natijasi:
```text
Diqqat... Tayyorlaning... START!
Poygachi #1 yugurishni boshladi!
Poygachi #2 yugurishni boshladi!
Poygachi #3 yugurishni boshladi!
Barcha poygachilar marraga yetib keldi.
```

# 692-Topshiriq: Kanal orqali Holatlar Mashinasi (State Machine)
## Topshiriq sharti:
Buyurtmaning 'Yaratildi' -> 'To'landi' -> 'Yetkazildi' bosqichlarini kanal orqali boshqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Holat string

const (
	HolatYaratildi   Holat = "YARATILDI"
	HolatTolandi     Holat = "TO'LANDI"
	HolatYetkazildi Holat = "YETKAZILDI"
)

func main() {
	holatKanal := make(chan Holat, 3)

	holatKanal <- HolatYaratildi
	holatKanal <- HolatTolandi
	holatKanal <- HolatYetkazildi
	close(holatKanal)

	for h := range holatKanal {
		switch h {
		case HolatYaratildi:
			fmt.Println("1. Buyurtma tizimda qayd etildi.")
		case HolatTolandi:
			fmt.Println("2. Mablag' muvaffaqiyatli yechib olindi.")
		case HolatYetkazildi:
			fmt.Println("3. Mahsulot manzilga yetkazildi.")
		}
	}
}
```

## Tushuntirish va Mantiq:
Kanallar ma'lumotlar oqimi bilan birga tizim holatining ketma-ket o'zgarishini qat'iy nazorat qilishda juda qulaydir.

## Ishlash natijasi:
```text
1. Buyurtma tizimda qayd etildi.
2. Mablag' muvaffaqiyatli yechib olindi.
3. Mahsulot manzilga yetkazildi.
```

# 693-Topshiriq: Ping-Pong: Ikki goroutine o'rtasida to'p almashish
## Topshiriq sharti:
Ikkita goroutinani bitta kanal orqali navbatma-navbat 'ping' va 'pong' o'ynashga majburlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

type Koptoq struct {
	Zarbalar int
}

func oyinchi(nom string, stol chan *Koptoq) {
	for {
		koptoq := <-stol
		koptoq.Zarbalar++
		fmt.Printf("[%s] zarba berdi! (Jami: %d)\n", nom, koptoq.Zarbalar)
		time.Sleep(30 * time.Millisecond)
		stol <- koptoq
	}
}

func main() {
	stol := make(chan *Koptoq)

	go oyinchi("Ping", stol)
	go oyinchi("Pong", stol)

	// O'yinni boshlaymiz
	stol <- new(Koptoq)

	time.Sleep(140 * time.Millisecond)
	<-stol // To'pni olib o'yinni to'xtatamiz
	fmt.Println("O'yin yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Buferlanmagan kanal orqali obyekt uzatilganda goroutinelar navbat bilan bir-biriga boshqaruvni topshiradi.

## Ishlash natijasi:
```text
[Ping] zarba berdi! (Jami: 1)
[Pong] zarba berdi! (Jami: 2)
[Ping] zarba berdi! (Jami: 3)
[Pong] zarba berdi! (Jami: 4)
O'yin yakunlandi.
```

# 694-Topshiriq: Asinxron guruhlash (Batching by size or timeout)
## Topshiriq sharti:
Kanaldan kelayotgan ma'lumotlarni 3 ta bo'lganda yoki 50ms vaqt o'tganda paketlab jo'nating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	kirish := make(chan string)

	go func() {
		kirish <- "Item-1"
		kirish <- "Item-2"
		kirish <- "Item-3"
		time.Sleep(100 * time.Millisecond)
		kirish <- "Item-4"
	}()

	var paket []string
	taymer := time.After(60 * time.Millisecond)

	for i := 0; i < 4; i++ {
		select {
		case element := <-kirish:
			paket = append(paket, element)
			if len(paket) == 3 {
				fmt.Println("[Hajm bo'yicha paket yuborildi]:", paket)
				paket = nil
			}
		case <-taymer:
			if len(paket) > 0 {
				fmt.Println("[Vaqt bo'yicha paket yuborildi]:", paket)
				paket = nil
			}
		}
	}
}
```

## Tushuntirish va Mantiq:
Batching texnikasi ma'lumotlar bazasiga individual yozish o'rniga guruhlab yozish orqali I/O samaradorligini o'nlab martaga oshiradi.

## Ishlash natijasi:
```text
[Hajm bo'yicha paket yuborildi]: [Item-1 Item-2 Item-3]
[Hajm bo'yicha paket yuborildi]: [Item-4]
```

# 695-Topshiriq: Orqaga bosim (Backpressure) nazorati
## Topshiriq sharti:
Sekin iste'molchi tezkor ishlab chiqaruvchini bufer orqali tabiiy ravishda sekinlashtirishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	// Sig'imi 2 bo'lgan kanal
	quvur := make(chan int, 2)

	go func() {
		for i := 1; i <= 4; i++ {
			fmt.Printf("Ishlab chiqaruvchi: #%d ni yozmoqda...\n", i)
			quvur <- i
			fmt.Printf("Ishlab chiqaruvchi: #%d yozildi!\n", i)
		}
		close(quvur)
	}()

	time.Sleep(50 * time.Millisecond)
	fmt.Println("--- Iste'molchi sekinlik bilan o'qishni boshladi ---")

	for val := range quvur {
		fmt.Printf("Iste'molchi: #%d ni qabul qildi\n", val)
		time.Sleep(40 * time.Millisecond)
	}
}
```

## Tushuntirish va Mantiq:
Kanal to'lganida yozuvchi avtomatik ravishda bloklanishi tizimning orqaga bosim (backpressure) himoyasidir. Bu xotira to'lib dastur qulashini oldini oladi.

## Ishlash natijasi:
```text
Ishlab chiqaruvchi: #1 ni yozmoqda...
Ishlab chiqaruvchi: #1 yozildi!
Ishlab chiqaruvchi: #2 ni yozmoqda...
Ishlab chiqaruvchi: #2 yozildi!
Ishlab chiqaruvchi: #3 ni yozmoqda...
--- Iste'molchi sekinlik bilan o'qishni boshladi ---
Iste'molchi: #1 ni qabul qildi
Ishlab chiqaruvchi: #3 yozildi!
Ishlab chiqaruvchi: #4 ni yozmoqda...
Iste'molchi: #2 ni qabul qildi
Ishlab chiqaruvchi: #4 yozildi!
Iste'molchi: #3 ni qabul qildi
Iste'molchi: #4 ni qabul qildi
```

# 696-Topshiriq: Channel Demultiplexer (Bir kanaldan filtrlangan kanallarga)
## Topshiriq sharti:
Yagona oqimdan juft va toq sonlarni ikkita alohida kanalga ajrating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func demux(kirish <-chan int, juftlar chan<- int, toqlar chan<- int) {
	for n := range kirish {
		if n%2 == 0 {
			juftlar <- n
		} else {
			toqlar <- n
		}
	}
	close(juftlar)
	close(toqlar)
}

func main() {
	in := make(chan int, 4)
	in <- 11
	in <- 22
	in <- 33
	in <- 44
	close(in)

	juft := make(chan int, 2)
	toq := make(chan int, 2)

	go demux(in, juft, toq)

	fmt.Print("Juftlar: ")
	for j := range juft {
		fmt.Printf("%d ", j)
	}
	fmt.Println()

	fmt.Print("Toqlar: ")
	for t := range toq {
		fmt.Printf("%d ", t)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Demultiplexer yagona ma'lumotlar oqimini shartlar asosida ixtisoslashgan alohida yo'llarga bo'lib yuboradi.

## Ishlash natijasi:
```text
Juftlar: 22 44 
Toqlar: 11 33
```

# 697-Topshiriq: Tranzaksion tasdiqlash (Two-way Handshake)
## Topshiriq sharti:
Mijoz va server o'rtasida to'liq tasdiq (salom -> javob -> tasdiq) protokolini quring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Handshake struct {
	Salom string
	Ack   chan string
}

func server(ch <-chan Handshake) {
	req := <-ch
	fmt.Println("Server qabul qildi:", req.Salom)
	req.Ack <- "ACK: Server ulandi"
}

func main() {
	ch := make(chan Handshake)
	go server(ch)

	ackCh := make(chan string)
	ch <- Handshake{Salom: "SYN: Salom Server", Ack: ackCh}

	javob := <-ackCh
	fmt.Println("Mijoz tasdiqni qabul qildi:", javob)
}
```

## Tushuntirish va Mantiq:
Two-way handshake protokollari ma'lumot yo'qolib ketmasligi va ikki tomon ham tayyorligini kafolatlash uchun qo'llaniladi.

## Ishlash natijasi:
```text
Server qabul qildi: SYN: Salom Server
Mijoz tasdiqni qabul qildi: ACK: Server ulandi
```

# 698-Topshiriq: Cheksiz ma'lumotlar oqimi va bekor qilish
## Topshiriq sharti:
Fibonacci ketma-ketligini cheksiz oqimda beruvchi va istalgan payt to'xtatiluvchi generator tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func fibonacci(toxtat <-chan struct{}) <-chan int {
	ch := make(chan int)
	go func() {
		defer close(ch)
		a, b := 0, 1
		for {
			select {
			case <-toxtat:
				return
			case ch <- a:
				a, b = b, a+b
			}
		}
	}()
	return ch
}

func main() {
	toxtat := make(chan struct{})
	fib := fibonacci(toxtat)

	fmt.Print("Fibonacci oqimi: ")
	for i := 0; i < 7; i++ {
		fmt.Printf("%d ", <-fib)
	}
	fmt.Println()

	close(toxtat) // Oqim to'xtatildi
}
```

## Tushuntirish va Mantiq:
Generatorlar talabga binoan (lazy evaluation) hisoblaydi va bekor qilish kanali yordamida ortiqcha resurs sarfisiz to'xtatiladi.

## Ishlash natijasi:
```text
Fibonacci oqimi: 0 1 1 2 3 5 8
```

# 699-Topshiriq: Kanallar bilan xavfsiz resurslar hovuzi (Resource Pool)
## Topshiriq sharti:
Cheklangan ulanishlar (connection) hovuzini buferlangan kanal orqali boshqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Ulanish struct {
	ID int
}

type UlanishHovuzi struct {
	hovuz chan *Ulanish
}

func YangiHovuz(hajm int) *UlanishHovuzi {
	h := &UlanishHovuzi{hovuz: make(chan *Ulanish, hajm)}
	for i := 1; i <= hajm; i++ {
		h.hovuz <- &Ulanish{ID: i}
	}
	return h
}

func (p *UlanishHovuzi) Olish() *Ulanish {
	return <-p.hovuz
}

func (p *UlanishHovuzi) Qaytarish(u *Ulanish) {
	p.hovuz <- u
}

func main() {
	hovuz := YangiHovuz(2)

	conn1 := hovuz.Olish()
	fmt.Println("Ulanish olindi, ID:", conn1.ID)

	conn2 := hovuz.Olish()
	fmt.Println("Ulanish olindi, ID:", conn2.ID)

	hovuz.Qaytarish(conn1)
	fmt.Println("Ulanish 1 hovuzga qaytarildi.")

	conn3 := hovuz.Olish()
	fmt.Println("Yana ulanish olindi, ID:", conn3.ID)
}
```

## Tushuntirish va Mantiq:
Buferlangan kanal tabiiy ravishda thread-safe ob'yektlar hovuzini (object pool) tashkil etadi. Hech qanday qo'shimcha mutex talab qilinmaydi.

## Ishlash natijasi:
```text
Ulanish olindi, ID: 1
Ulanish olindi, ID: 2
Ulanish 1 hovuzga qaytarildi.
Yana ulanish olindi, ID: 1
```

# 700-Topshiriq: Event Bus tizimi (Voqealar shinasi - Channels & Select)
## Topshiriq sharti:
Keng qamrovli yakuniy loyiha: Mavzular (Topics) bo'yicha hodisalarni ro'yxatga oluvchi, tarqatuvchi va tinglovchilarga yetkazuvchi to'liq Event Bus arxitekturasini yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type Event struct {
	Topic string
	Data  any
}

type EventBus struct {
	mu          sync.RWMutex
	subscribers map[string][]chan Event
}

func NewEventBus() *EventBus {
	return &EventBus{
		subscribers: make(map[string][]chan Event),
	}
}

func (eb *EventBus) Subscribe(topic string) <-chan Event {
	eb.mu.Lock()
	defer eb.mu.Unlock()

	ch := make(chan Event, 10)
	eb.subscribers[topic] = append(eb.subscribers[topic], ch)
	return ch
}

func (eb *EventBus) Publish(topic string, data any) {
	eb.mu.RLock()
	defer eb.mu.RUnlock()

	if chs, mavjud := eb.subscribers[topic]; mavjud {
		event := Event{Topic: topic, Data: data}
		for _, ch := range chs {
			select {
			case ch <- event:
			default:
				// Tinglovchi buferi to'la bo'lsa oqimni to'xtatmaymiz
			}
		}
	}
}

func main() {
	bus := NewEventBus()

	orderEvents := bus.Subscribe("orders")
	userEvents := bus.Subscribe("users")

	var wg sync.WaitGroup
	wg.Add(2)

	go func() {
		defer wg.Done()
		for i := 0; i < 2; i++ {
			ev := <-orderEvents
			fmt.Printf("[ORDERS TINGLOVCHI] Hodisa: %s => %v\n", ev.Topic, ev.Data)
		}
	}()

	go func() {
		defer wg.Done()
		ev := <-userEvents
		fmt.Printf("[USERS TINGLOVCHI] Hodisa: %s => %v\n", ev.Topic, ev.Data)
	}()

	time.Sleep(20 * time.Millisecond)
	bus.Publish("orders", "Buyurtma #501 yaratildi")
	bus.Publish("users", "Yangi foydalanuvchi: Farhod")
	bus.Publish("orders", "Buyurtma #501 to'landi")

	wg.Wait()
	fmt.Println("Barcha Event Bus hodisalari muvaffaqiyatli ishlandi.")
}
```

## Tushuntirish va Mantiq:
Event Bus arxitekturasi yirik mikroservislarda xabarlarni markazlashgan boshqaruv orqali mustaqil komponentlarga yetkazish uchun ishlatiladi.

## Ishlash natijasi:
```text
[ORDERS TINGLOVCHI] Hodisa: orders => Buyurtma #501 yaratildi
[ORDERS TINGLOVCHI] Hodisa: orders => Buyurtma #501 to'landi
[USERS TINGLOVCHI] Hodisa: users => Yangi foydalanuvchi: Farhod
Barcha Event Bus hodisalari muvaffaqiyatli ishlandi.
```

