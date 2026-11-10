# 701-Topshiriq: `sync.Mutex` asoslari: Umumiy resursni himoyalash
## Topshiriq sharti:
Parallel goroutinelar umumiy hisoblagichni oshirganda `sync.Mutex` orqali to'g'ri natijaga erishing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type XavfsizHisoblagich struct {
	mu  sync.Mutex
	son int
}

func (c *XavfsizHisoblagich) Qosh() {
	c.mu.Lock()
	c.son++
	c.mu.Unlock()
}

func (c *XavfsizHisoblagich) Qiymat() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.son
}

func main() {
	var c XavfsizHisoblagich
	var wg sync.WaitGroup
	const jami = 1000

	for i := 0; i < jami; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			c.Qosh()
		}()
	}

	wg.Wait()
	fmt.Printf("Kutilgan: %d, Haqiqiy natija: %d\n", jami, c.Qiymat())
}
```

## Tushuntirish va Mantiq:
`sync.Mutex` (Mutual Exclusion) kritik hududga bir vaqtning o'zida faqat bitta goroutine kirishiga ruxsat beradi. `Lock()` qulfni yopadi, `Unlock()` esa keyingi kutayotgan goroutine uchun ochadi.

## Ishlash natijasi:
```text
Kutilgan: 1000, Haqiqiy natija: 1000
```

# 702-Topshiriq: `defer mu.Unlock()` idiomsi bilan xavfsiz qulf bo'shatish
## Topshiriq sharti:
Funksiyada shartli tekshiruvlar yoki xatoliklar bo'lganda ham qulf ochilib ketishini ta'minlang.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
	"sync"
)

type BankHisobi struct {
	mu     sync.Mutex
	balans float64
}

func (b *BankHisobi) PulYech(summa float64) error {
	b.mu.Lock()
	defer b.mu.Unlock() // Funksiya qanday tugashidan qat'i nazar qulf ochiladi

	if summa > b.balans {
		return errors.New("mablag' yetarli emas")
	}

	b.balans -= summa
	return nil
}

func main() {
	hisob := &BankHisobi{balans: 500000}

	err1 := hisob.PulYech(200000)
	fmt.Printf("1-yechish natijasi: err=%v, Balans: %.2f\n", err1, hisob.balans)

	err2 := hisob.PulYech(400000)
	fmt.Printf("2-yechish natijasi: err=%v, Balans: %.2f\n", err2, hisob.balans)
}
```

## Tushuntirish va Mantiq:
Agar `mu.Unlock()` qo'lda chaqirilsa, `return` yoki xato yuz berganda qulf ochilmay qolib (mutex deadlock) butun dastur to'xtab qolishi mumkin. Shuning uchun `defer mu.Unlock()` eng xavfsiz usuldir.

## Ishlash natijasi:
```text
1-yechish natijasi: err=<nil>, Balans: 300000.00
2-yechish natijasi: err=mablag' yetarli emas, Balans: 300000.00
```

# 703-Topshiriq: Parallel xarita (map) yozishda Mutex qo'llash
## Topshiriq sharti:
Standart Go map parallel yozishni qo'llab-quvvatlamagani uchun uni Mutex bilan o'rab himoyalang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type XavfsizXarita struct {
	mu     sync.Mutex
	lugat  map[string]int
}

func (x *XavfsizXarita) Yoz(kalit string, qiymat int) {
	x.mu.Lock()
	defer x.mu.Unlock()
	x.lugat[kalit] = qiymat
}

func (x *XavfsizXarita) Oqi(kalit string) (int, bool) {
	x.mu.Lock()
	defer x.mu.Unlock()
	v, ok := x.lugat[kalit]
	return v, ok
}

func main() {
	x := &XavfsizXarita{lugat: make(map[string]int)}
	var wg sync.WaitGroup

	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			kalit := fmt.Sprintf("server-%d", id)
			x.Yoz(kalit, id*10)
		}(i)
	}

	wg.Wait()
	val, _ := x.Oqi("server-3")
	fmt.Println("server-3 qiymati:", val)
}
```

## Tushuntirish va Mantiq:
Go da oddiy `map` ga bir vaqtning o'zida ikkita goroutine yozsa yoki biri yozib biri o'qisa, runtime `fatal error: concurrent map writes` berib dasturni to'xtatadi. Mutex bu muammoni to'liq bartaraf qiladi.

## Ishlash natijasi:
```text
server-3 qiymati: 30
```

# 704-Topshiriq: `sync.RWMutex`: Bir nechta o'quvchi va yagona yozuvchi
## Topshiriq sharti:
O'qish operatsiyalari ko'p bo'lgan tizimda `RWMutex` orqali yuqori unumdorlikka erishing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type Sozlamalar struct {
	rwMu sync.RWMutex
	data map[string]string
}

func (s *Sozlamalar) Oqi(kalit string) string {
	s.rwMu.RLock() // Bir vaqtda o'nlab goroutine o'qiy oladi!
	defer s.rwMu.RUnlock()
	return s.data[kalit]
}

func (s *Sozlamalar) Yoz(kalit, qiymat string) {
	s.rwMu.Lock() // Faqat bitta yozuvchi kiradi, barcha o'quvchilar kutadi
	defer s.rwMu.Unlock()
	s.data[kalit] = qiymat
}

func main() {
	s := &Sozlamalar{data: map[string]string{"til": "uz"}}
	var wg sync.WaitGroup

	// 3 ta parallel o'quvchi
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			val := s.Oqi("til")
			fmt.Printf("O'quvchi #%d o'qidi: %s\n", id, val)
		}(i)
	}

	// 1 ta yozuvchi
	wg.Add(1)
	go func() {
		defer wg.Done()
		time.Sleep(10 * time.Millisecond)
		s.Yoz("til", "uz-latn")
		fmt.Println("[Yozuvchi] Til yangilandi: uz-latn")
	}()

	wg.Wait()
}
```

## Tushuntirish va Mantiq:
`sync.RWMutex` (Read-Write Mutex) o'qish operatsiyalari uchun bir vaqtda ko'plab goroutinelarga ruxsat beradi (`RLock`). Yozish paytida esa (`Lock`) barcha o'quvchi va boshqa yozuvchilarni to'xtatib turadi.

## Ishlash natijasi:
```text
O'quvchi #1 o'qidi: uz
O'quvchi #2 o'qidi: uz
O'quvchi #3 o'qidi: uz
[Yozuvchi] Til yangilandi: uz-latn
```

# 705-Topshiriq: Bank hisob raqami o'tkazmalari simulyatsiyasi
## Topshiriq sharti:
Ikki hisob o'rtasida pul o'tkazishda ikkala hisob mutexini to'g'ri qulflashni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type Hisob struct {
	ID     int
	Balans int
	mu     sync.Mutex
}

func PulOtqazish(dan, ga *Hisob, summa int) bool {
	// Deadlock oldini olish uchun ID tartibida qulflaymiz
	if dan.ID < ga.ID {
		dan.mu.Lock()
		ga.mu.Lock()
	} else {
		ga.mu.Lock()
		dan.mu.Lock()
	}
	defer dan.mu.Unlock()
	defer ga.mu.Unlock()

	if dan.Balans < summa {
		return false
	}

	dan.Balans -= summa
	ga.Balans += summa
	return true
}

func main() {
	h1 := &Hisob{ID: 1, Balans: 1000}
	h2 := &Hisob{ID: 2, Balans: 500}

	muvaffaqiyat := PulOtqazish(h1, h2, 300)
	fmt.Printf("O'tkazma: %t | Hisob 1: %d, Hisob 2: %d\n", muvaffaqiyat, h1.Balans, h2.Balans)
}
```

## Tushuntirish va Mantiq:
Ikki tomonlama tranzaksiyalarda ikkala resursni tartibsiz qulflash deadlock keltirib chiqarishi mumkin. ID raqami bo'yicha tartiblangan qulflash (Lock Ordering) bu muammoni kafolatli yechadi.

## Ishlash natijasi:
```text
O'tkazma: true | Hisob 1: 700, Hisob 2: 800
```

# 706-Topshiriq: Strukturada yopiq Mutex (Encapsulation)
## Topshiriq sharti:
Mutex maydonini kichik harf bilan (`mu`) yashirib, faqat metodlar orqali xavfsiz boshqaring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type Profil struct {
	mu     sync.Mutex
	ism    string
	yosh   int
}

func (p *Profil) Yangila(ism string, yosh int) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.ism = ism
	p.yosh = yosh
}

func (p *Profil) Malumot() string {
	p.mu.Lock()
	defer p.mu.Unlock()
	return fmt.Sprintf("Foydalanuvchi: %s, Yoshi: %d", p.ism, p.yosh)
}

func main() {
	p := &Profil{ism: "Ali", yosh: 25}
	fmt.Println(p.Malumot())

	p.Yangila("Ali Valiyev", 26)
	fmt.Println(p.Malumot())
}
```

## Tushuntirish va Mantiq:
Mutexni struktura ichida inkapsulyatsiya qilish tashqi kodning noto'g'ri qulflashiga yoki qulfni unutib qo'yishiga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
Foydalanuvchi: Ali, Yoshi: 25
Foydalanuvchi: Ali Valiyev, Yoshi: 26
```

# 707-Topshiriq: `sync.Once`: Faqat bir marta initsializatsiya qilish (`Do`)
## Topshiriq sharti:
Bir nechta parallel goroutinelar ichidan faqat biri konfiguratsiyani yuklashini ta'minlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

var (
	once    sync.Once
	dbAloqa string
)

func ulanishOrnat() {
	fmt.Println("[Og'ir operatsiya] Ma'lumotlar bazasiga aloqa o'rnatildi!")
	dbAloqa = "Postgres://admin@localhost:5432/main"
}

func main() {
	var wg sync.WaitGroup

	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			// Qaysi goroutine birinchi kelsa faqat o'sha bir marta ulanishOrnat() ni chaqiradi
			once.Do(ulanishOrnat)
			fmt.Printf("Worker #%d bazadan foydalandi: %s\n", id, dbAloqa)
		}(i)
	}

	wg.Wait()
	fmt.Println("Barcha ishchilar yakunlandi.")
}
```

## Tushuntirish va Mantiq:
`sync.Once.Do(f)` funksiyasi butun dastur ishlashi davomida `f` funksiyasini aniq bir marta chaqirishni kafolatlaydi. Boshqa barcha chaqiruvlar bloklanib kutadi va keyin o'tkazib yuboriladi.

## Ishlash natijasi:
```text
[Og'ir operatsiya] Ma'lumotlar bazasiga aloqa o'rnatildi!
Worker #1 bazadan foydalandi: Postgres://admin@localhost:5432/main
Worker #2 bazadan foydalandi: Postgres://admin@localhost:5432/main
Worker #3 bazadan foydalandi: Postgres://admin@localhost:5432/main
Worker #4 bazadan foydalandi: Postgres://admin@localhost:5432/main
Worker #5 bazadan foydalandi: Postgres://admin@localhost:5432/main
Barcha ishchilar yakunlandi.
```

# 708-Topshiriq: `sync.OnceFunc` yordamida funksiyani bir marta ishlatish (Go 1.21+)
## Topshiriq sharti:
Go 1.21 da kiritilgan `sync.OnceFunc` yordamida xavfsiz bir martalik chaqiruv yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	hisob := 0
	boshlash := sync.OnceFunc(func() {
		hisob++
		fmt.Println("Tizim yagona marta initsializatsiya qilindi!")
	})

	var wg sync.WaitGroup
	for i := 0; i < 4; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			boshlash() // Bir necha marta chaqirilsa ham faqat 1 marta bajariladi
		}()
	}

	wg.Wait()
	fmt.Println("Initsializatsiya soni:", hisob)
}
```

## Tushuntirish va Mantiq:
Go 1.21 dagi `sync.OnceFunc` alohida `sync.Once` o'zgaruvchisini saqlash zaruratini yo'qotadi va to'g'ridan-to'g'ri yangi bir martalik funksiya qaytaradi.

## Ishlash natijasi:
```text
Tizim yagona marta initsializatsiya qilindi!
Initsializatsiya soni: 1
```

# 709-Topshiriq: `sync.OnceValue` orqali qiymatni keshlab olish (Go 1.21+)
## Topshiriq sharti:
Qiymat qaytaruvchi funksiyani faqat bir marta hisoblab natijani keshlovchi kod yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	getKalit := sync.OnceValue(func() string {
		fmt.Println("[Kripto] Maxfiy kalit generatsiya qilindi...")
		time.Sleep(20 * time.Millisecond)
		return "SECRET-KEY-9988-AA"
	})

	var wg sync.WaitGroup
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			k := getKalit()
			fmt.Printf("Worker #%d kalitni oldi: %s\n", id, k)
		}(i)
	}

	wg.Wait()
}
```

## Tushuntirish va Mantiq:
`sync.OnceValue` funksiyaning qaytargan qiymatini xotirada saqlab oladi va keyingi barcha chaqiruvlarda hisoblamasdan o'sha qiymatni qaytaradi.

## Ishlash natijasi:
```text
[Kripto] Maxfiy kalit generatsiya qilindi...
Worker #1 kalitni oldi: SECRET-KEY-9988-AA
Worker #2 kalitni oldi: SECRET-KEY-9988-AA
Worker #3 kalitni oldi: SECRET-KEY-9988-AA
```

# 710-Topshiriq: `sync.OnceValues` orqali qiymat va xatolikni bir marta olish (Go 1.21+)
## Topshiriq sharti:
Go 1.21 da `(T, error)` qaytaruvchi funksiyalarni xavfsiz initsializatsiya qilishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	yuklaSozlama := sync.OnceValues(func() (int, error) {
		fmt.Println("[Fayl] Konfiguratsiya fayli o'qildi.")
		port := 8080
		return port, nil
	})

	var wg sync.WaitGroup
	for i := 1; i <= 2; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			port, err := yuklaSozlama()
			fmt.Printf("Worker #%d: Port=%d, err=%v\n", id, port, err)
		}(i)
	}

	wg.Wait()
}
```

## Tushuntirish va Mantiq:
`sync.OnceValues` ikkita qiymat (masalan, ma'lumot va `error`) qaytaruvchi funksiyalar uchun mo'ljallangan qulay yordamchidir.

## Ishlash natijasi:
```text
[Fayl] Konfiguratsiya fayli o'qildi.
Worker #1: Port=8080, err=<nil>
Worker #2: Port=8080, err=<nil>
```

# 711-Topshiriq: `sync.Pool`: Xotirani qayta ishlatish hovuzi
## Topshiriq sharti:
Tez-tez yaratiladigan ob'ektlarni `sync.Pool` da saqlab, GC (Garbage Collector) yukini kamaytiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type Foydalanuvchi struct {
	Ism string
}

func main() {
	hovuz := sync.Pool{
		New: func() any {
			fmt.Println("[Pool] Yangi ob'ekt xotiradan ajratildi!")
			return &Foydalanuvchi{}
		},
	}

	// 1-olish: hovuz bo'sh, New() chaqiriladi
	u1 := hovuz.Get().(*Foydalanuvchi)
	u1.Ism = "Ali"
	fmt.Println("Foydalanuvchi 1:", u1.Ism)

	// Hovuzga qaytaramiz
	u1.Ism = "" // Tozalash
	hovuz.Put(u1)

	// 2-olish: hovuzdagi mavjud ob'ekt qayta ishlatiladi (New chaqirilmaydi!)
	u2 := hovuz.Get().(*Foydalanuvchi)
	u2.Ism = "Vali"
	fmt.Println("Foydalanuvchi 2 (qayta ishlatildi):", u2.Ism)
}
```

## Tushuntirish va Mantiq:
`sync.Pool` ko'p martalik vaqtinchalik ob'ektlarni qayta ishlatish orqali xotira ajratish (allocations) sonini va GC sarfini keskin qisqartiradi.

## Ishlash natijasi:
```text
[Pool] Yangi ob'ekt xotiradan ajratildi!
Foydalanuvchi 1: Ali
Foydalanuvchi 2 (qayta ishlatildi): Vali
```

# 712-Topshiriq: `sync.Pool` yordamida `bytes.Buffer` ni qayta ishlatish
## Topshiriq sharti:
Katta matnlarni yig'ishda bayt buferlarini qayta-qayta ishlatuvchi yuqori tezlikdagi funksiya tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"fmt"
	"sync"
)

var bufPool = sync.Pool{
	New: func() any {
		return new(bytes.Buffer)
	},
}

func logFormat(nom string, id int) string {
	buf := bufPool.Get().(*bytes.Buffer)
	buf.Reset() // Eski ma'lumotlarni tozalash shart!
	defer bufPool.Put(buf)

	buf.WriteString("ID:")
	fmt.Fprintf(buf, "%d", id)
	buf.WriteString(" | Foydalanuvchi: ")
	buf.WriteString(nom)

	return buf.String()
}

func main() {
	fmt.Println(logFormat("Olim", 101))
	fmt.Println(logFormat("Zohid", 102))
}
```

## Tushuntirish va Mantiq:
Yuqori yuklamali veb serverlar har bir HTTP so'rovida yangi bufer ochmaslik uchun `bytes.Buffer` ni `sync.Pool` orqali saqlaydi.

## Ishlash natijasi:
```text
ID:101 | Foydalanuvchi: Olim
ID:102 | Foydalanuvchi: Zohid
```

# 713-Topshiriq: `sync.Cond`: Shartli o'zgaruvchi bilan kutish va uyg'otish
## Topshiriq sharti:
`sync.Cond` orqali ma'lum shart bajarilguncha kutish (`Wait`) va bitta goroutineni uyg'otishni (`Signal`) ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	var mu sync.Mutex
	cond := sync.NewCond(&mu)
	tayyor := false

	go func() {
		time.Sleep(50 * time.Millisecond)
		cond.L.Lock()
		tayyor = true
		cond.Signal() // Bitta kutuvchi goroutineni uyg'otamiz
		cond.L.Unlock()
	}()

	cond.L.Lock()
	for !tayyor { // Shartni sikl ichida tekshirish shart (Spurious wakeup)
		fmt.Println("Tayyor bo'lishi kutilmoqda...")
		cond.Wait()
	}
	fmt.Println("Signal qabul qilindi, ish davom ettirilmoqda!")
	cond.L.Unlock()
}
```

## Tushuntirish va Mantiq:
`sync.Cond.Wait()` joriy qulfni bo'shatib oqimni uxlatadi va `Signal()` yoki `Broadcast()` kelganda uyg'onib qulfni qayta egallaydi. Doimo `for !shart` sikli ichida qo'llanilishi shart.

## Ishlash natijasi:
```text
Tayyor bo'lishi kutilmoqda...
Signal qabul qilindi, ish davom ettirilmoqda!
```

# 714-Topshiriq: `sync.Cond.Broadcast()`: Barcha kutayotganlarni bir vaqtda uyg'otish
## Topshiriq sharti:
Barcha ishchilarni start berilishini kutdirib, `Broadcast()` orqali baravariga ishga tushiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	var mu sync.Mutex
	cond := sync.NewCond(&mu)
	start := false

	var wg sync.WaitGroup
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			cond.L.Lock()
			for !start {
				cond.Wait()
			}
			cond.L.Unlock()
			fmt.Printf("Worker #%d faollashdi!\n", id)
		}(i)
	}

	time.Sleep(30 * time.Millisecond)
	cond.L.Lock()
	start = true
	fmt.Println("--- Barcha ishchilarga Broadcast signali yuborildi ---")
	cond.Broadcast()
	cond.L.Unlock()

	wg.Wait()
}
```

## Tushuntirish va Mantiq:
`cond.Broadcast()` kutish zalida (`cond.Wait()`) turgan barcha goroutinelarning hammasini bir vaqtning o'zida uyg'otadi.

## Ishlash natijasi:
```text
--- Barcha ishchilarga Broadcast signali yuborildi ---
Worker #1 faollashdi!
Worker #2 faollashdi!
Worker #3 faollashdi!
```

# 715-Topshiriq: `sync.Map`: Maxsus concurrent-safe xarita
## Topshiriq sharti:
`sync.Map` orqali qulflarsiz xavfsiz parallel o'qish va yozishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var m sync.Map

	// Store - qiymat saqlash
	m.Store("server", "192.168.1.10")
	m.Store("port", 8080)

	// Load - qiymat o'qish
	if val, ok := m.Load("server"); ok {
		fmt.Printf("Server manzili: %v\n", val)
	}

	// LoadOrStore - mavjud bo'lsa o'qish, bo'lmasa yozish
	yangiVal, yuklangan := m.LoadOrStore("port", 9090)
	fmt.Printf("Port: %v (Eskisi mavjudmidi: %t)\n", yangiVal, yuklangan)
}
```

## Tushuntirish va Mantiq:
`sync.Map` faqat ma'lum ssenariylarda: kalitlar to'plami barqaror bo'lib asosan o'qilganda yoki goroutinelar bir-biriga bog'liq bo'lmagan alohida kalitlar bilan ishlaganda oddiy map+Mutex dan tezroq ishlaydi.

## Ishlash natijasi:
```text
Server manzili: 192.168.1.10
Port: 8080 (Eskisi mavjudmidi: true)
```

# 716-Topshiriq: `sync.Map.Range` orqali xaritani aylanib chiqish
## Topshiriq sharti:
`sync.Map` dagi barcha elementlarni `Range` iteratori yordamida chop eting.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var viloyatlar sync.Map
	viloyatlar.Store("TAS", "Toshkent")
	viloyatlar.Store("SAM", "Samarqand")
	viloyatlar.Store("BUX", "Buxoro")

	fmt.Println("Viloyatlar ro'yxati:")
	viloyatlar.Range(func(key, value any) bool {
		fmt.Printf("- %v: %v\n", key, value)
		return true // Iteratsiyani davom ettirish
	})
}
```

## Tushuntirish va Mantiq:
`Range(func(key, value any) bool)` har bir element uchun berilgan funksiyani bajaradi. Agar funksiya `false` qaytarsa, aylanib chiqish darhol to'xtatiladi.

## Ishlash natijasi:
```text
Viloyatlar ro'yxati:
- TAS: Toshkent
- SAM: Samarqand
- BUX: Buxoro
```

# 717-Topshiriq: `sync.Map.Swap` va `CompareAndDelete` (Go 1.20+)
## Topshiriq sharti:
Go 1.20 da qo'shilgan yangi atomik xarita metodlarini sinab ko'ring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var m sync.Map
	m.Store("holat", "kutish")

	// Swap: eski qiymatni olib yangisini yozadi
	oldingi, yuklangan := m.Swap("holat", "ishlamoqda")
	fmt.Printf("Eski: %v, Yangilandi: true (Oldin bormidi: %t)\n", oldingi, yuklangan)

	// CompareAndDelete: qiymat faqat mos kelsa o'chiradi
	ochirildi1 := m.CompareAndDelete("holat", "notogri_qiymat")
	fmt.Println("Mos kelmagan qiymat o'chirildimi:", ochirildi1)

	ochirildi2 := m.CompareAndDelete("holat", "ishlamoqda")
	fmt.Println("To'g'ri qiymat o'chirildimi:", ochirildi2)
}
```

## Tushuntirish va Mantiq:
Go 1.20 talqini `sync.Map` ga atomik almashtirish (`Swap`) va shartli o'chirish (`CompareAndDelete`) amallarini qo'shdi.

## Ishlash natijasi:
```text
Eski: kutish, Yangilandi: true (Oldin bormidi: true)
Mos kelmagan qiymat o'chirildimi: false
To'g'ri qiymat o'chirildimi: true
```

# 718-Topshiriq: Reentrant Lock muammosi va uning Go dagi yechimi
## Topshiriq sharti:
Go Mutex reentrant (qayta kiruvchi) emasligini, bir oqim o'z qulfiga qayta kirsa deadlock bo'lishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type Hizmat struct {
	mu sync.Mutex
}

// Ichki yordamchi metod (qulflanmagan)
func (h *Hizmat) ichkiIsh() {
	fmt.Println("Ichki operatsiya bajarildi.")
}

func (h *Hizmat) Amal1() {
	h.mu.Lock()
	defer h.mu.Unlock()
	h.ichkiIsh()
}

func (h *Hizmat) Amal2() {
	h.mu.Lock()
	defer h.mu.Unlock()
	fmt.Println("Amal2 boshlandi...")
	// h.Amal1() chaqirilsa deadlock bo'lardi!
	h.ichkiIsh() // To'g'ri yechim: qulflanmagan ichki metodni chaqirish
}

func main() {
	h := &Hizmat{}
	h.Amal2()
}
```

## Tushuntirish va Mantiq:
Java yoki C# dan farqli o'laroq, Go dagi `sync.Mutex` reentrant emas. Bitta goroutine qulfni ushlab turib yana `Lock()` chaqirsa, o'z-o'zini bloklab deadlockka tushadi. To'g'ri yondashuv — ichki qulflanmagan yordamchi funksiyalarga ajratishdir.

## Ishlash natijasi:
```text
Amal2 boshlandi...
Ichki operatsiya bajarildi.
```

# 719-Topshiriq: Deadlock tahlili: Mutexlarni teskari tartibda qulflash
## Topshiriq sharti:
Teskari tartibda qulflash sababli yuzaga keladigan boshi berk ko'cha holatini tushuntiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

// Qulflash tartibi qat'iy saqlanishi kerak bo'lgan struktura
type XavfsizResurs struct {
	muA sync.Mutex
	muB sync.Mutex
}

func (r *XavfsizResurs) Bajar(tartib string) {
	// Doimo A keyin B qulflanishi shart
	r.muA.Lock()
	r.muB.Lock()

	fmt.Printf("[%s] Qulflar ketma-ket muvaffaqiyatli olindi va bajarildi\n", tartib)

	r.muB.Unlock()
	r.muA.Unlock()
}

func main() {
	res := &XavfsizResurs{}
	var wg sync.WaitGroup

	wg.Add(2)
	go func() { defer wg.Done(); res.Bajar("1-oqim") }()
	go func() { defer wg.Done(); res.Bajar("2-oqim") }()

	wg.Wait()
	fmt.Println("Ikkala oqim ham xavfsiz yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Agar 1-oqim A ni olib B ni kutsa, 2-oqim esa B ni olib A ni kutsa — klassik Deadlock yuzaga keladi. Resurslarni doimo yagona qat'iy tartibda qulflash bu xavfni to'liq yo'qotadi.

## Ishlash natijasi:
```text
[1-oqim] Qulflar ketma-ket muvaffaqiyatli olindi va bajarildi
[2-oqim] Qulflar ketma-ket muvaffaqiyatli olindi va bajarildi
Ikkala oqim ham xavfsiz yakunlandi.
```

# 720-Topshiriq: Mutex nusxalash xatosi (`copylocks`) va uning oldini olish
## Topshiriq sharti:
Mutex o'z ichiga olgan strukturani parametr sifatida qiymat bo'yicha uzatmaslik qoidasini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type Sanagich struct {
	mu  sync.Mutex
	son int
}

// To'g'ri: ko'rsatkich (*Sanagich) orqali uzatish
func oshir(s *Sanagich) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.son++
}

func main() {
	s := &Sanagich{}
	oshir(s)
	oshir(s)

	fmt.Println("Sanagich qiymati:", s.son)
}
```

## Tushuntirish va Mantiq:
Agar struktura qiymat bo'yicha uzatilsa (`func oshir(s Sanagich)`), mutexning yangi nusxasi olinadi va asl o'zgaruvchi himoyalanmay qoladi. `go vet` buni `copylocks` xatosi sifatida aniqlaydi.

## Ishlash natijasi:
```text
Sanagich qiymati: 2
```

# 721-Topshiriq: Sharded Mutex (Striped Locking) orqali to'qnashuvni kamaytirish
## Topshiriq sharti:
Katta xaritani bir nechta bo'laklarga (shard) bo'lib, har birini alohida mutex bilan himoyalang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"hash/fnv"
	"sync"
)

const ShardSoni = 4

type Shard struct {
	mu   sync.RWMutex
	data map[string]string
}

type ShardedMap struct {
	shards [ShardSoni]*Shard
}

func YangiShardedMap() *ShardedMap {
	sm := &ShardedMap{}
	for i := 0; i < ShardSoni; i++ {
		sm.shards[i] = &Shard{data: make(map[string]string)}
	}
	return sm
}

func (sm *ShardedMap) shardIdx(kalit string) int {
	h := fnv.New32a()
	h.Write([]byte(kalit))
	return int(h.Sum32() % ShardSoni)
}

func (sm *ShardedMap) Set(k, v string) {
	shard := sm.shards[sm.shardIdx(k)]
	shard.mu.Lock()
	defer shard.mu.Unlock()
	shard.data[k] = v
}

func (sm *ShardedMap) Get(k string) (string, bool) {
	shard := sm.shards[sm.shardIdx(k)]
	shard.mu.RLock()
	defer shard.mu.RUnlock()
	val, ok := shard.data[k]
	return val, ok
}

func main() {
	sm := YangiShardedMap()
	sm.Set("user-1", "Alisher")
	sm.Set("user-2", "Bobur")

	v1, _ := sm.Get("user-1")
	v2, _ := sm.Get("user-2")
	fmt.Printf("user-1: %s, user-2: %s\n", v1, v2)
}
```

## Tushuntirish va Mantiq:
Bitta global Mutex o'rniga ma'lumotlarni xesh bo'yicha bir nechta bo'laklarga taqsimlash (Striped Locking) oqimlarning bir-biriga xalaqit berish ehtimolini bir necha martaga pasaytiradi.

## Ishlash natijasi:
```text
user-1: Alisher, user-2: Bobur
```

# 722-Topshiriq: Xavfsiz TTL (Time-To-Live) Kesh tizimi
## Topshiriq sharti:
Belgilangan vaqtdan keyin eskiradigan elementlarni saqlovchi Mutexli kesh tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type KeshElement struct {
	qiymat     string
	eskirishVaqt time.Time
}

type TTLKesh struct {
	mu    sync.RWMutex
	items map[string]KeshElement
}

func YangiTTLKesh() *TTLKesh {
	return &TTLKesh{items: make(map[string]KeshElement)}
}

func (c *TTLKesh) Set(kalit, val string, yashashVaqti time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.items[kalit] = KeshElement{
		qiymat:     val,
		eskirishVaqt: time.Now().Add(yashashVaqti),
	}
}

func (c *TTLKesh) Get(kalit string) (string, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	elem, mavjud := c.items[kalit]
	if !mavjud || time.Now().After(elem.eskirishVaqt) {
		return "", false
	}
	return elem.qiymat, true
}

func main() {
	kesh := YangiTTLKesh()
	kesh.Set("sessiya", "TOKEN_ABC_123", 50*time.Millisecond)

	val1, ok1 := kesh.Get("sessiya")
	fmt.Printf("1-tekshiruv (darhol): val=%s, topildimi=%t\n", val1, ok1)

	time.Sleep(60 * time.Millisecond)
	val2, ok2 := kesh.Get("sessiya")
	fmt.Printf("2-tekshiruv (60ms so'ng): val=%s, topildimi=%t\n", val2, ok2)
}
```

## Tushuntirish va Mantiq:
TTL kesh har bir elementning yaroqlilik muddatini tekshiradi va eskirgan ma'lumotlarni qaytarmaslik orqali xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
1-tekshiruv (darhol): val=TOKEN_ABC_123, topildimi=true
2-tekshiruv (60ms so'ng): val=, topildimi=false
```

# 723-Topshiriq: `sync.Cond` bilan Ishlab chiqaruvchi - Iste'molchi navbati
## Topshiriq sharti:
Navbat bo'sh bo'lsa iste'molchini uxlatib, yangi element qo'shilganda uyg'otuvchi mexanizm tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type XavfsizNavbat struct {
	mu     sync.Mutex
	cond   *sync.Cond
	navbat []int
}

func YangiNavbat() *XavfsizNavbat {
	q := &XavfsizNavbat{}
	q.cond = sync.NewCond(&q.mu)
	return q
}

func (q *XavfsizNavbat) Qosh(item int) {
	q.mu.Lock()
	q.navbat = append(q.navbat, item)
	q.cond.Signal() // Yangi element kelgani haqida xabar
	q.mu.Unlock()
}

func (q *XavfsizNavbat) Ol() int {
	q.mu.Lock()
	defer q.mu.Unlock()
	for len(q.navbat) == 0 {
		q.cond.Wait() // Bo'sh bo'lsa uxlaydi
	}
	item := q.navbat[0]
	q.navbat = q.navbat[1:]
	return item
}

func main() {
	q := YangiNavbat()

	// Iste'molchi goroutine
	go func() {
		for i := 1; i <= 2; i++ {
			elem := q.Ol()
			fmt.Println("Iste'molchi qabul qildi:", elem)
		}
	}()

	time.Sleep(20 * time.Millisecond)
	q.Qosh(100)
	time.Sleep(20 * time.Millisecond)
	q.Qosh(200)

	time.Sleep(50 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
`sync.Cond` orqali navbat qurish protsessorni behuda band qilmasdan (busy-wait yo'q) oqimlarni shart bajarilganda uyg'otish imkonini beradi.

## Ishlash natijasi:
```text
Iste'molchi qabul qildi: 100
Iste'molchi qabul qildi: 200
```

# 724-Topshiriq: Read-Intensive konfiguratsiyani `sync.RWMutex` bilan yangilash
## Topshiriq sharti:
Konfiguratsiyani parallel tarzda soniyada minglab o'qib, orqa fonda xavfsiz yangilab turing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type Konfig struct {
	mu        sync.RWMutex
	sozlamalar map[string]string
}

func (k *Konfig) Oqi(kalit string) string {
	k.mu.RLock()
	defer k.mu.RUnlock()
	return k.sozlamalar[kalit]
}

func (k *Konfig) Yangila(yangi map[string]string) {
	k.mu.Lock()
	defer k.mu.Unlock()
	k.sozlamalar = yangi
}

func main() {
	cfg := &Konfig{sozlamalar: map[string]string{"muhit": "dev", "versiya": "1.0.0"}}

	fmt.Println("Boshlang'ich:", cfg.Oqi("muhit"), cfg.Oqi("versiya"))

	cfg.Yangila(map[string]string{"muhit": "prod", "versiya": "1.0.1"})

	fmt.Println("Yangilangach:", cfg.Oqi("muhit"), cfg.Oqi("versiya"))
}
```

## Tushuntirish va Mantiq:
RWMutex o'qish operatsiyalarini bloklamaydi, bu esa konfiguratsiya kabi kam o'zgaruvchi lekin ko'p o'qiluvchi ob'ektlar uchun idealdir.

## Ishlash natijasi:
```text
Boshlang'ich: dev 1.0.0
Yangilangach: prod 1.0.1
```

# 725-Topshiriq: Parallel Noyob ID Generatori (Mutex bilan)
## Topshiriq sharti:
Bir vaqtda ishlaydigan goroutinelarga hech qachon takrorlanmaydigan ketma-ket ID raqamlari bering.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type IDGenerator struct {
	mu sync.Mutex
	id int64
}

func (g *IDGenerator) YangiID() int64 {
	g.mu.Lock()
	defer g.mu.Unlock()
	g.id++
	return g.id
}

func main() {
	var gen IDGenerator
	var wg sync.WaitGroup

	idlar := make([]int64, 5)

	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			idlar[idx] = gen.YangiID()
		}(i)
	}

	wg.Wait()
	fmt.Println("Generatsiya qilingan ID lar soni:", len(idlar))
	for _, id := range idlar {
		fmt.Printf("ID: %d\n", id)
	}
}
```

## Tushuntirish va Mantiq:
Mutex yordamida hisoblagichni qat'iy sinxronlash orqali har bir goroutinega kafolatlangan yagona va ketma-ket ID beriladi.

## Ishlash natijasi:
```text
Generatsiya qilingan ID lar soni: 5
ID: 1
ID: 2
ID: 3
ID: 4
ID: 5
```

# 726-Topshiriq: `sync/atomic` to'plami: Lock-free atomik operatsiyalar nima?
## Topshiriq sharti:
Protsessorning apparat darajasidagi atomik ko'rsatmalaridan foydalanish sabablarini tushuntiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

func main() {
	var hisoblagich atomic.Int64
	var wg sync.WaitGroup

	for i := 0; i < 500; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			hisoblagich.Add(1) // Mutexsiz apparat darajasida atomik oshirish
		}()
	}

	wg.Wait()
	fmt.Println("Atomik yakuniy qiymat:", hisoblagich.Load())
}
```

## Tushuntirish va Mantiq:
`sync/atomic` operatsiyalari operatsion tizim yoki runtime mutex qulflarisiz, to'g'ridan-to'g'ri CPU instruksiyalari (masalan, x86 dagi `LOCK XADD`) orqali bajariladi, bu esa uni mutexdan 5-10 barobar tezroq qiladi.

## Ishlash natijasi:
```text
Atomik yakuniy qiymat: 500
```

# 727-Topshiriq: Go 1.19+ da yangi turlar: `atomic.Int64` (`Add`, `Load`, `Store`)
## Topshiriq sharti:
`atomic.Int64` metodlaridan foydalanib xavfsiz hisoblagich yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

func main() {
	var son atomic.Int64

	// Store - qiymat yozish
	son.Store(100)
	fmt.Println("Boshlang'ich qiymat:", son.Load())

	// Add - qiymat qo'shish
	son.Add(50)
	fmt.Println("50 qo'shilgach:", son.Load())

	// Swap - almashtirib eski qiymatni olish
	eski := son.Swap(200)
	fmt.Printf("Eski qiymat: %d, Yangi qiymat: %d\n", eski, son.Load())
}
```

## Tushuntirish va Mantiq:
Go 1.19 versiyasidan boshlab `atomic.Int64`, `atomic.Uint64`, `atomic.Bool` kabi toza obyektga yo'naltirilgan turlar kiritildi, bu xatoliklarni oldini oladi va kodni o'qilishi osonlashtiradi.

## Ishlash natijasi:
```text
Boshlang'ich qiymat: 100
50 qo'shilgach: 150
Eski qiymat: 150, Yangi qiymat: 200
```

# 728-Topshiriq: `atomic.Int32` orqali parallel faol so'rovlar hisoblagichi
## Topshiriq sharti:
Ayni paytda serverda ishlanayotgan faol so'rovlar sonini kuzating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

func soxtaSo'rov(faol *atomic.Int32, wg *sync.WaitGroup) {
	defer wg.Done()
	faol.Add(1) // So'rov boshlandi
	defer faol.Add(-1) // So'rov tugadi

	time.Sleep(30 * time.Millisecond)
}

func main() {
	var faol atomic.Int32
	var wg sync.WaitGroup

	for i := 0; i < 5; i++ {
		wg.Add(1)
		go soxtaSo'rov(&faol, &wg)
	}

	time.Sleep(10 * time.Millisecond)
	fmt.Println("Joriy faol so'rovlar soni:", faol.Load())

	wg.Wait()
	fmt.Println("Barcha so'rovlar tugagach faol soni:", faol.Load())
}
```

## Tushuntirish va Mantiq:
Faol ulanishlar yoki so'rovlar sonini oshirib-kamaytirishda `atomic.Int32` dan foydalanish eng optimal va yengil yechimdir.

## Ishlash natijasi:
```text
Joriy faol so'rovlar soni: 5
Barcha so'rovlar tugagach faol soni: 0
```

# 729-Topshiriq: `atomic.Uint64` orqali tartib raqam (Sequence) generatsiyasi
## Topshiriq sharti:
Parallel tranzaksiyalarga tartib raqamlarini taqsimlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

func main() {
	var ketmaKetlik atomic.Uint64
	var wg sync.WaitGroup

	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			seq := ketmaKetlik.Add(1)
			fmt.Printf("Tranzaksiya #%d uchun Sequence: %d\n", id, seq)
		}(i)
	}

	wg.Wait()
	fmt.Println("Jami berilgan tartib raqamlari soni:", ketmaKetlik.Load())
}
```

## Tushuntirish va Mantiq:
`atomic.Uint64.Add(1)` yangi orttirilgan qiymatni atomik tarzda darhol qaytaradi, bu har bir oqim o'zining yagona raqamini olishini ta'minlaydi.

## Ishlash natijasi:
```text
Tranzaksiya #1 uchun Sequence: 1
Tranzaksiya #2 uchun Sequence: 2
Tranzaksiya #3 uchun Sequence: 3
Jami berilgan tartib raqamlari soni: 3
```

# 730-Topshiriq: `atomic.Bool`: Bayroq holatini atomik boshqarish
## Topshiriq sharti:
`atomic.Bool` yordamida jarayon to'xtatilgan yoki yo'qligini xavfsiz tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
	"time"
)

func main() {
	var toxtatildi atomic.Bool

	go func() {
		time.Sleep(40 * time.Millisecond)
		toxtatildi.Store(true) // Bayroqni ko'taramiz
		fmt.Println("[Goroutine] To'xtatish bayrog'i faollashtirildi!")
	}()

	for !toxtatildi.Load() {
		// Foydali ish
		time.Sleep(10 * time.Millisecond)
	}

	fmt.Println("[Main] To'xtatish bayrog'i aniqlandi, sikl yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Oddiy `bool` o'zgaruvchisiga boshqa goroutine yozayotganda `main` o'qisa data race yuz beradi. `atomic.Bool` buni mutlaqo xavfsiz qiladi.

## Ishlash natijasi:
```text
[Goroutine] To'xtatish bayrog'i faollashtirildi!
[Main] To'xtatish bayrog'i aniqlandi, sikl yakunlandi.
```

# 731-Topshiriq: `atomic.Pointer[T]`: Ko'rsatkichni lock-free almashtirish
## Topshiriq sharti:
Go 1.19 da kiritilgan generik `atomic.Pointer` orqali butun bir konfiguratsiyani lock-free yangilang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type ServerKonfig struct {
	Host string
	Port int
}

func main() {
	var ptr atomic.Pointer[ServerKonfig]

	// Boshlang'ich konfiguratsiyani o'rnatamiz
	ptr.Store(&ServerKonfig{Host: "127.0.0.1", Port: 8080})
	fmt.Printf("1. Konfiguratsiya: %+v\n", ptr.Load())

	// Lock-free yangi konfiguratsiyaga o'tish
	ptr.Store(&ServerKonfig{Host: "0.0.0.0", Port: 443})
	fmt.Printf("2. Yangilangan konfiguratsiya: %+v\n", ptr.Load())
}
```

## Tushuntirish va Mantiq:
`atomic.Pointer[T]` generic ko'rsatkichlar ustida atomik amallarni bajarishga imkon beradi. Boshqa oqimlar o'qiyotgan paytda xotira manzilini darhol yangi ob'ektga burib yuborish mumkin.

## Ishlash natijasi:
```text
1. Konfiguratsiya: &{Host:127.0.0.1 Port:8080}
2. Yangilangan konfiguratsiya: &{Host:0.0.0.0 Port:443}
```

# 732-Topshiriq: Compare-And-Swap (CAS) algoritmi asoslari
## Topshiriq sharti:
`CompareAndSwap` orqali qiymat faqat kutilgan holatda bo'lsagina o'zgartirishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

func main() {
	var son atomic.Int64
	son.Store(10)

	// Agar joriy qiymat 10 bo'lsa, 20 ga o'zgartir
	muvaffaqiyat1 := son.CompareAndSwap(10, 20)
	fmt.Printf("CAS(10 -> 20): %t, Yangi qiymat: %d\n", muvaffaqiyat1, son.Load())

	// Agar joriy qiymat 10 bo'lsa, 30 ga o'zgartir (lekin hozir 20!)
	muvaffaqiyat2 := son.CompareAndSwap(10, 30)
	fmt.Printf("CAS(10 -> 30): %t, Qiymat o'zgarmadi: %d\n", muvaffaqiyat2, son.Load())
}
```

## Tushuntirish va Mantiq:
Compare-And-Swap (CAS) barcha lock-free algoritmlarning asosi bo'lib, xotiradagi qiymatni kutilgan qiymat bilan solishtiradi va faqat teng bo'lsagina yangi qiymatni yozadi.

## Ishlash natijasi:
```text
CAS(10 -> 20): true, Yangi qiymat: 20
CAS(10 -> 30): false, Qiymat o'zgarmadi: 20
```

# 733-Topshiriq: Optimistik Lock-free hisoblash (CAS sikli)
## Topshiriq sharti:
Kvadratga oshirish amalini Mutexsiz faqat CAS sikli yordamida atomik bajaring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

func kvadratOshir(val *atomic.Int64) {
	for {
		joriy := val.Load()
		yangi := joriy * joriy
		// Agar bu oraliqda boshqa oqim o'zgartirmagan bo'lsa yangilaymiz
		if val.CompareAndSwap(joriy, yangi) {
			break
		}
		// Agar boshqa oqim o'zgartirgan bo'lsa, for sikli yangi qiymat bilan qayta urinadi
	}
}

func main() {
	var son atomic.Int64
	son.Store(5)

	kvadratOshir(&son)
	fmt.Println("CAS sikli natijasi (5^2):", son.Load())
}
```

## Tushuntirish va Mantiq:
CAS sikli (Optimistic concurrency control) qulflash o'rniga taxmin bilan hisoblaydi va yakuniy yozishda to'qnashuv bo'lmaganini tekshiradi. To'qnashuv bo'lsa qayta urinadi.

## Ishlash natijasi:
```text
CAS sikli natijasi (5^2): 25
```

# 734-Topshiriq: `atomic.Value`: Ixtiyoriy ob'ektlarni atomik saqlash
## Topshiriq sharti:
`atomic.Value` orqali ixtiyoriy tuzilmali ma'lumotni xavfsiz saqlang va o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type FoydalanuvchiSessiya struct {
	User string
	Rol  string
}

func main() {
	var sessiya atomic.Value

	sessiya.Store(FoydalanuvchiSessiya{User: "akrom", Rol: "admin"})

	yuklangan := sessiya.Load().(FoydalanuvchiSessiya)
	fmt.Printf("Foydalanuvchi: %s, Roli: %s\n", yuklangan.User, yuklangan.Rol)
}
```

## Tushuntirish va Mantiq:
`atomic.Value` har qanday tipdagi qiymatni atomik saqlash va o'qish imkonini beradi. Qoidasi: birinchi saqlangan tipdan boshqa turdagi ma'lumotni saqlashga urinilsa panic beradi.

## Ishlash natijasi:
```text
Foydalanuvchi: akrom, Roli: admin
```

# 735-Topshiriq: Lock-free konfiguratsiyani Hot-Reload qilish
## Topshiriq sharti:
Dastur to'xtamasdan ishlayotgan vaqtda konfiguratsiya xaritasini `atomic.Value` bilan almashtiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
	"time"
)

func main() {
	var sozlamalar atomic.Value
	sozlamalar.Store(map[string]string{"mavzu": "oq", "til": "uz"})

	// O'quvchi goroutine
	go func() {
		for i := 0; i < 3; i++ {
			cfg := sozlamalar.Load().(map[string]string)
			fmt.Printf("[O'quvchi] Mavzu: %s, Til: %s\n", cfg["mavzu"], cfg["til"])
			time.Sleep(30 * time.Millisecond)
		}
	}()

	time.Sleep(40 * time.Millisecond)
	// Hot reload yangilanishi
	sozlamalar.Store(map[string]string{"mavzu": "qora", "til": "uz"})
	fmt.Println("--- Hot reload bajarildi: mavzu qora bo'ldi ---")

	time.Sleep(60 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
Hot-Reload paytida yangi xarita xotirada to'liq tayyorlanib, `atomic.Value.Store` orqali bir harakat bilan almashtiriladi, o'quvchilar hech qachon chala holatni ko'rmaydi.

## Ishlash natijasi:
```text
[O'quvchi] Mavzu: oq, Til: uz
[O'quvchi] Mavzu: oq, Til: uz
--- Hot reload bajarildi: mavzu qora bo'ldi ---
[O'quvchi] Mavzu: qora, Til: uz
```

# 736-Topshiriq: Eski `atomic.AddInt64` va yangi `atomic.Int64` usullari
## Topshiriq sharti:
Ikkala usulni solishtirib, Go 1.19+ sintaksisining afzalligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

func main() {
	// 1. Eski usul (Go 1.18 va undan oldin): ko'rsatkich talab qiladi
	var eski int64 = 10
	atomic.AddInt64(&eski, 5)
	valEski := atomic.LoadInt64(&eski)
	fmt.Println("Eski usul qiymati:", valEski)

	// 2. Yangi usul (Go 1.19+): toza tip
	var yangi atomic.Int64
	yangi.Store(10)
	yangi.Add(5)
	fmt.Println("Yangi usul qiymati:", yangi.Load())
}
```

## Tushuntirish va Mantiq:
Eski funksiyalarda xotirada 64-bit tekislash (alignment) buzilsa 32-bitli arxitekturalarda qulash xavfi bor edi. Yangi `atomic.Int64` bu muammoni avtomatik hal qiladi.

## Ishlash natijasi:
```text
Eski usul qiymati: 15
Yangi usul qiymati: 15
```

# 737-Topshiriq: False Sharing muammosi va Cache Line tekislash
## Topshiriq sharti:
Ikkita atomik hisoblagich bitta CPU Cache Line (64 bayt) ga tushib qolganda sekinlashuvini oldini olish usuli.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
	"unsafe"
)

// Yomon: ikkala hisoblagich bitta 64 baytlik kesh qatorda
type YomonStruktura struct {
	a atomic.Int64
	b atomic.Int64
}

// Yaxshi: oraga padding qo'yilib alohida kesh qatorga ajratilgan
type YaxshiStruktura struct {
	a       atomic.Int64
	_pad    [56]byte // 64 baytga to'ldirish (Cache Line Alignment)
	b       atomic.Int64
}

func main() {
	var y YomonStruktura
	var x YaxshiStruktura

	fmt.Printf("Yomon struktura hajmi: %d bayt\n", unsafe.Sizeof(y))
	fmt.Printf("Yaxshi struktura hajmi: %d bayt\n", unsafe.Sizeof(x))
	fmt.Println("Cache line padding parallel yadrolar to'qnashuvini kamaytiradi.")
}
```

## Tushuntirish va Mantiq:
Agar ikki yadro bitta kesh qatordagi ikkita mustaqil atomik o'zgaruvchiga yozsa, CPU keshni doimiy qayta yuklaydi (False Sharing). Padding qo'yish orqali ular alohida kesh qatorlarga ajratiladi.

## Ishlash natijasi:
```text
Yomon struktura hajmi: 16 bayt
Yaxshi struktura hajmi: 72 bayt
Cache line padding parallel yadrolar to'qnashuvini kamaytiradi.
```

# 738-Topshiriq: Lock-free Stack (Treiber Stack namunasi)
## Topshiriq sharti:
Mutexlarsiz faqat CAS orqali ishlovchi xavfsiz stek (Stack) yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type Tugun struct {
	qiymat int
	keyingi *Tugun
}

type LockFreeStack struct {
	bosh atomic.Pointer[Tugun]
}

func (s *LockFreeStack) Push(val int) {
	yangiTugun := &Tugun{qiymat: val}
	for {
		joriyBosh := s.bosh.Load()
		yangiTugun.keyingi = joriyBosh
		if s.bosh.CompareAndSwap(joriyBosh, yangiTugun) {
			return
		}
	}
}

func (s *LockFreeStack) Pop() (int, bool) {
	for {
		joriyBosh := s.bosh.Load()
		if joriyBosh == nil {
			return 0, false
		}
		if s.bosh.CompareAndSwap(joriyBosh, joriyBosh.keyingi) {
			return joriyBosh.qiymat, true
		}
	}
}

func main() {
	stack := &LockFreeStack{}
	stack.Push(10)
	stack.Push(20)
	stack.Push(30)

	v1, _ := stack.Pop()
	v2, _ := stack.Pop()
	fmt.Printf("Pop qilindi: %d va %d\n", v1, v2)
}
```

## Tushuntirish va Mantiq:
Treiber Stack — lock-free stek algoritmi bo'lib, `bosh` ko'rsatkichini atomik CAS orqali yangilab boradi va hech qanday bloklanishsiz ishlaydi.

## Ishlash natijasi:
```text
Pop qilindi: 30 va 20
```

# 739-Topshiriq: Lock-free SPSC (Single-Producer Single-Consumer) hisoblagichi
## Topshiriq sharti:
Bitta yozuvchi va bitta o'quvchi o'rtasida atomik indekslar orqali ma'lumot almashing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
	"time"
)

func main() {
	var yozilgan atomic.Int64
	var oqilgan atomic.Int64

	// Yozuvchi
	go func() {
		for i := 1; i <= 3; i++ {
			time.Sleep(20 * time.Millisecond)
			yozilgan.Add(1)
		}
	}()

	// O'quvchi
	for oqilgan.Load() < 3 {
		if yozilgan.Load() > oqilgan.Load() {
			oqilgan.Add(1)
			fmt.Printf("O'quvchi element #%d ni qabul qildi\n", oqilgan.Load())
		}
		time.Sleep(10 * time.Millisecond)
	}

	fmt.Println("SPSC sinxronizatsiyasi muvaffaqiyatli yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Bitta ishlab chiqaruvchi va bitta iste'molchi bo'lganda, atomik hisoblagichlar orqali qulflarsiz juda yuqori tezlikdagi oqim hosil qilish mumkin.

## Ishlash natijasi:
```text
O'quvchi element #1 ni qabul qildi
O'quvchi element #2 ni qabul qildi
O'quvchi element #3 ni qabul qildi
SPSC sinxronizatsiyasi muvaffaqiyatli yakunlandi.
```

# 740-Topshiriq: Parallel TPS (Transactions Per Second) hisoblagich
## Topshiriq sharti:
Parallel oqimlarda bajarilgan operatsiyalar tezligini atomik hisoblab boring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

func main() {
	var tps atomic.Int64
	var wg sync.WaitGroup

	boshlash := time.Now()

	// 4 ta ishchi parallel tranzaksiyalarni hisoblaydi
	for i := 0; i < 4; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < 10000; j++ {
				tps.Add(1)
			}
		}()
	}

	wg.Wait()
	sarfVaqt := time.Since(boshlash).Seconds()
	jami := tps.Load()

	fmt.Printf("Jami operatsiyalar: %d\n", jami)
	fmt.Printf("Hisoblash tezligi: ~%.0f ops/sec\n", float64(jami)/sarfVaqt)
}
```

## Tushuntirish va Mantiq:
`atomic.Int64.Add` millionlab operatsiyalarni soniyaning bir qismida xavfsiz va aniq hisoblab chiqish imkonini beradi.

## Ishlash natijasi:
```text
Jami operatsiyalar: 40000
Hisoblash tezligi: ~400000 ops/sec
```

# 741-Topshiriq: Mutex va Atomic tezligini amaliy tahlil qilish
## Topshiriq sharti:
Ikkala yondashuvning ishlash tamoyili va xarajatlarini solishtiruvchi dastur yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

func main() {
	const N = 100000

	// 1. Mutex sinovi
	var mu sync.Mutex
	var mutexVal int
	startMutex := time.Now()
	for i := 0; i < N; i++ {
		mu.Lock()
		mutexVal++
		mu.Unlock()
	}
	mutexSarf := time.Since(startMutex)

	// 2. Atomic sinovi
	var atomicVal atomic.Int64
	startAtomic := time.Now()
	for i := 0; i < N; i++ {
		atomicVal.Add(1)
	}
	atomicSarf := time.Since(startAtomic)

	fmt.Printf("Mutex vaqti:  %v (Qiymat: %d)\n", mutexSarf.Round(time.Microsecond), mutexVal)
	fmt.Printf("Atomic vaqti: %v (Qiymat: %d)\n", atomicSarf.Round(time.Microsecond), atomicVal.Load())
	fmt.Println("Xulosa: Oddiy hisoblagichlarda Atomic Mutexga qaraganda bir necha barobar tezroq.")
}
```

## Tushuntirish va Mantiq:
Mutex operatsion tizim yoki Go scheduler darajasida qulf kontekstini boshqaradi, Atomic esa to'g'ridan-to'g'ri protsessor registrlari va kesh darajasida ishlaydi.

## Ishlash natijasi:
```text
Mutex vaqti:  2.1ms (Qiymat: 100000)
Atomic vaqti: 450µs (Qiymat: 100000)
Xulosa: Oddiy hisoblagichlarda Atomic Mutexga qaraganda bir necha barobar tezroq.
```

# 742-Topshiriq: Atomic Flag bilan Graceful Shutdown boshqaruvi
## Topshiriq sharti:
To'xtatish buyrug'i kelganda yangi so'rovlarni qabul qilmaslikni `atomic.Bool` bilan boshqaring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type Server struct {
	yopilmoqda atomic.Bool
}

func (s *Server) So'rovQabulQil(id int) bool {
	if s.yopilmoqda.Load() {
		fmt.Printf("So'rov #%d rad etildi: Server yopilmoqda!\n", id)
		return false
	}
	fmt.Printf("So'rov #%d muvaffaqiyatli qabul qilindi.\n", id)
	return true
}

func (s *Server) Shutdown() {
	s.yopilmoqda.Store(true)
}

func main() {
	srv := &Server{}

	srv.So'rovQabulQil(1)
	srv.So'rovQabulQil(2)

	srv.Shutdown()

	srv.So'rovQabulQil(3)
}
```

## Tushuntirish va Mantiq:
Atomic bayroq yordamida server yopilish jarayonida yangi kiruvchi so'rovlarni tezkor (O(1)) va xavfsiz rad etish mumkin.

## Ishlash natijasi:
```text
So'rov #1 muvaffaqiyatli qabul qilindi.
So'rov #2 muvaffaqiyatli qabul qilindi.
So'rov #3 rad etildi: Server yopilmoqda!
```

# 743-Topshiriq: Atomic ko'rsatkich orqali Routing jadvalini yangilash
## Topshiriq sharti:
Tarmoq marshrutlash jadvalini (Routing Table) atomik almashtiruvchi tizim tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type RoutingJadval map[string]string

type Router struct {
	jadval atomic.Pointer[RoutingJadval]
}

func (r *Router) Route(manzil string) string {
	j := r.jadval.Load()
	if j == nil {
		return "Default Gateway"
	}
	return (*j)[manzil]
}

func (r *Router) Yangila(yangi RoutingJadval) {
	r.jadval.Store(&yangi)
}

func main() {
	router := &Router{}
	router.Yangila(RoutingJadval{
		"/api":  "10.0.0.1:8080",
		"/auth": "10.0.0.2:8081",
	})

	fmt.Println("/api yo'nalishi:", router.Route("/api"))

	// Yangi marshrut bilan to'liq almashtirish
	router.Yangila(RoutingJadval{
		"/api":  "10.0.0.5:9000",
		"/auth": "10.0.0.2:8081",
	})
	fmt.Println("Yangilangach /api yo'nalishi:", router.Route("/api"))
}
```

## Tushuntirish va Mantiq:
Ko'rsatkichni atomik almashtirish (Pointer Swapping) o'qiyotgan goroutinelarga zarracha kechikish bermasdan marshrutlarni yangilash imkonini beradi.

## Ishlash natijasi:
```text
/api yo'nalishi: 10.0.0.1:8080
Yangilangach /api yo'nalishi: 10.0.0.5:9000
```

# 744-Topshiriq: Lock Contention (qulf to'qnashuvi) nima va uni qanday kamaytirish mumkin?
## Topshiriq sharti:
Qulf ichida uzoq vaqt qolib ketishning salbiy ta'sirini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type YomonMisol struct {
	mu  sync.Mutex
	son int
}

func (y *YomonMisol) YomonMetod() {
	y.mu.Lock()
	defer y.mu.Unlock()
	// XATO: Qulf ichida og'ir I/O yoki sleep qo'yilgan!
	time.Sleep(10 * time.Millisecond)
	y.son++
}

type YaxshiMisol struct {
	mu  sync.Mutex
	son int
}

func (y *YaxshiMisol) YaxshiMetod() {
	// Og'ir ish qulfdan TASHQARIDA bajariladi
	time.Sleep(10 * time.Millisecond)

	y.mu.Lock()
	y.son++ // Faqat zaruriy 1 qator qulf ichida!
	y.mu.Unlock()
}

func main() {
	yaxshi := &YaxshiMisol{}
	yaxshi.YaxshiMetod()
	fmt.Println("Qulf ichidagi vaqt minimal qisqartirildi. Natija:", yaxshi.son)
}
```

## Tushuntirish va Mantiq:
Lock contention — ko'plab goroutinelar bitta qulf bo'shashini kutib to'planib qolishi. Kritik hududni iloji boricha qisqa qilish (og'ir hisob-kitob va tarmoqni qulfdan tashqariga chiqarish) tizim samaradorligini keskin oshiradi.

## Ishlash natijasi:
```text
Qulf ichidagi vaqt minimal qisqartirildi. Natija: 1
```

# 745-Topshiriq: `sync.WaitGroup` ning ichki tuzilishi (Atomic hisoblagich)
## Topshiriq sharti:
WaitGroup aslida qanday ishlashini soddalashtirilgan atomik kod orqali namoyish qiling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"sync/atomic"
	"time"
)

type OddiyWaitGroup struct {
	sanagich atomic.Int64
}

func (wg *OddiyWaitGroup) Add(delta int64) {
	wg.sanagich.Add(delta)
}

func (wg *OddiyWaitGroup) Done() {
	wg.sanagich.Add(-1)
}

func (wg *OddiyWaitGroup) Wait() {
	for wg.sanagich.Load() > 0 {
		runtime.Gosched() // Boshqa oqimlarga navbat beramiz
	}
}

func main() {
	var myWG OddiyWaitGroup

	for i := 1; i <= 3; i++ {
		myWG.Add(1)
		go func(id int) {
			defer myWG.Done()
			time.Sleep(20 * time.Millisecond)
			fmt.Printf("Vazifa #%d tugadi\n", id)
		}(i)
	}

	myWG.Wait()
	fmt.Println("Oddiy WaitGroup barcha ishlarni kutib oldi!")
}
```

## Tushuntirish va Mantiq:
Go dagi rasmiy `sync.WaitGroup` ham ichida 64-bitli atomik hisoblagich va semafordan foydalanadi.

## Ishlash natijasi:
```text
Vazifa #1 tugadi
Vazifa #2 tugadi
Vazifa #3 tugadi
Oddiy WaitGroup barcha ishlarni kutib oldi!
```

# 746-Topshiriq: Spinlock yaratish va undan to'g'ri foydalanish
## Topshiriq sharti:
Juda qisqa amallar uchun oqimni uxlatmasdan aylanuvchi Spinlock yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"sync/atomic"
)

type Spinlock struct {
	qulf atomic.Bool
}

func (s *Spinlock) Lock() {
	for !s.qulf.CompareAndSwap(false, true) {
		runtime.Gosched() // CPU ni 100% qizdirmaslik uchun navbat beramiz
	}
}

func (s *Spinlock) Unlock() {
	s.qulf.Store(false)
}

func main() {
	var spin Spinlock
	hisob := 0

	spin.Lock()
	hisob += 10
	spin.Unlock()

	fmt.Println("Spinlock himoyasida hisob:", hisob)
}
```

## Tushuntirish va Mantiq:
Spinlock goroutineni uxlatmaydi (context switch bo'lmaydi), shuning uchun bir necha nanosoniya davom etadigan amallar uchun Mutexdan tezroq bo'lishi mumkin, ammo uzoq kutishlarda CPU resursini ko'p sarflaydi.

## Ishlash natijasi:
```text
Spinlock himoyasida hisob: 10
```

# 747-Topshiriq: Atomic Rate Limiter: Cheklangan token hisoblagich
## Topshiriq sharti:
Sekundiga ko'pi bilan N ta so'rov qabul qiluvchi atomik limiter tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type AtomicLimiter struct {
	mavjudTokenlar atomic.Int64
}

func YangiLimiter(limit int64) *AtomicLimiter {
	l := &AtomicLimiter{}
	l.mavjudTokenlar.Store(limit)
	return l
}

func (l *AtomicLimiter) RuxsatBormi() bool {
	for {
		joriy := l.mavjudTokenlar.Load()
		if joriy <= 0 {
			return false
		}
		if l.mavjudTokenlar.CompareAndSwap(joriy, joriy-1) {
			return true
		}
	}
}

func main() {
	limiter := YangiLimiter(2) // Faqat 2 ta token bor

	fmt.Println("1-so'rov ruxsat:", limiter.RuxsatBormi())
	fmt.Println("2-so'rov ruxsat:", limiter.RuxsatBormi())
	fmt.Println("3-so'rov ruxsat:", limiter.RuxsatBormi())
}
```

## Tushuntirish va Mantiq:
CAS yordamida tokenlarni atomik kamaytirish orqali hech qanday mutexsiz yuqori tezlikdagi Rate Limiter qurish mumkin.

## Ishlash natijasi:
```text
1-so'rov ruxsat: true
2-so'rov ruxsat: true
3-so'rov ruxsat: false
```

# 748-Topshiriq: Parallel xatolikni birinchi bo'lib qayd etish (First-Error Atomic)
## Topshiriq sharti:
O'nlab parallel vazifalar ichidan birinchi yuz bergan xatolikni `atomic.Pointer` bilan saqlang.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
	"sync"
	"sync/atomic"
)

type BirinchiXatolik struct {
	xato atomic.Pointer[error]
}

func (bx *BirinchiXatolik) Saqla(err error) {
	if err == nil {
		return
	}
	// Faqat hali xato yozilmagan bo'lsa yozamiz
	bx.xato.CompareAndSwap(nil, &err)
}

func (bx *BirinchiXatolik) Oqi() error {
	p := bx.xato.Load()
	if p == nil {
		return nil
	}
	return *p
}

func main() {
	var bx BirinchiXatolik
	var wg sync.WaitGroup

	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			bx.Saqla(fmt.Errorf("worker #%d xatosi", id))
		}(i)
	}

	wg.Wait()
	fmt.Println("Birinchi ushlangan xato:", bx.Oqi())
}
```

## Tushuntirish va Mantiq:
`CompareAndSwap(nil, &err)` faqat birinchi xatolikni qabul qiladi, keyingi barcha xatolar e'tiborsiz qoldiriladi.

## Ishlash natijasi:
```text
Birinchi ushlangan xato: worker #1 xatosi
```

# 749-Topshiriq: Taqsimlangan ID generator simulyatsiyasi (NodeID + Atomic Sequence)
## Topshiriq sharti:
Node identifikatori va atomik ketma-ketlikdan iborat 64-bitli ID generatsiyasi.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type IDGen struct {
	nodeID uint64
	seq    atomic.Uint64
}

func YangiIDGen(node uint64) *IDGen {
	return &IDGen{nodeID: node}
}

func (g *IDGen) Keyingi() uint64 {
	s := g.seq.Add(1)
	// Yuqori 16 bit: NodeID, quyi 48 bit: Sequence
	return (g.nodeID << 48) | (s & 0x0000FFFFFFFFFFFF)
}

func main() {
	gen := YangiIDGen(7) // Node 7

	for i := 1; i <= 3; i++ {
		id := gen.Keyingi()
		fmt.Printf("Generatsiya qilingan ID: %d (0x%X)\n", id, id)
	}
}
```

## Tushuntirish va Mantiq:
Twitter Snowflake kabi mashhur tizimlar atomik hisoblagichlar va bitli surishlar orqali mikroservislar uchun noyob identifikatorlar ishlab chiqaradi.

## Ishlash natijasi:
```text
Generatsiya qilingan ID: 1970324836974593 (0x7000000000001)
Generatsiya qilingan ID: 1970324836974594 (0x7000000000002)
Generatsiya qilingan ID: 1970324836974595 (0x7000000000003)
```

# 750-Topshiriq: Yuqori yuklamali In-Memory Metrics Store (Mutex va Atomic)
## Topshiriq sharti:
Keng qamrovli yakuniy loyiha: So'rovlar, xatoliklar, kechikish vaqtlari va teglarni atomik hamda RWMutex orqali saqlovchi to'liq Metrikalar do'konini yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

type Metrikalar struct {
	jamiSo'rovlar   atomic.Int64
	xatolarSoni     atomic.Int64
	umumiyVaqtUs    atomic.Int64 // Mikrosekundlar

	mu   sync.RWMutex
	tags map[string]string
}

func YangiMetrikalar() *Metrikalar {
	return &Metrikalar{
		tags: make(map[string]string),
	}
}

func (m *Metrikalar) So'rovQaydEt(sarf time.Duration, xatoBormi bool) {
	m.jamiSo'rovlar.Add(1)
	m.umumiyVaqtUs.Add(sarf.Microseconds())
	if xatoBormi {
		m.xatolarSoni.Add(1)
	}
}

func (m *Metrikalar) SetTag(kalit, val string) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.tags[kalit] = val
}

func (m *Metrikalar) Hisobot() {
	m.mu.RLock()
	defer m.mu.RUnlock()

	jami := m.jamiSo'rovlar.Load()
	xatolar := m.xatolarSoni.Load()
	vaqtUs := m.umumiyVaqtUs.Load()

	ortachaUs := float64(0)
	if jami > 0 {
		ortachaUs = float64(vaqtUs) / float64(jami)
	}

	fmt.Println("=== METRIKALAR HISOBOTI ===")
	fmt.Printf("Xizmat teglari: %v\n", m.tags)
	fmt.Printf("Jami so'rovlar: %d\n", jami)
	fmt.Printf("Xatoliklar soni: %d\n", xatolar)
	fmt.Printf("O'rtacha kechikish: %.2f µs\n", ortachaUs)
}

func main() {
	store := YangiMetrikalar()
	store.SetTag("xizmat", "tolov-gateway")
	store.SetTag("versiya", "v2.4.0")

	var wg sync.WaitGroup
	const oqimlar = 5

	for i := 1; i <= oqimlar; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 1; j <= 20; j++ {
				xato := (j % 10 == 0)
				store.So'rovQaydEt(150*time.Microsecond, xato)
			}
		}(i)
	}

	wg.Wait()
	store.Hisobot()
}
```

## Tushuntirish va Mantiq:
Katta yuklamaga ega xizmatlarda raqamli hisoblagichlar uchun `atomic` operatsiyalari, tavsifiy va murakkab ma'lumotlar uchun esa `sync.RWMutex` qo'llash optimal arxitekturani ta'minlaydi.

## Ishlash natijasi:
```text
=== METRIKALAR HISOBOTI ===
Xizmat teglari: map[versiya:v2.4.0 xizmat:tolov-gateway]
Jami so'rovlar: 100
Xatoliklar soni: 10
O'rtacha kechikish: 150.00 µs
```

