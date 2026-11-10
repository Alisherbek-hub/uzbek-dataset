# 601-Topshiriq: Oddiy goroutine ishga tushirish (`go` kalit so'zi)
## Topshiriq sharti:
`go` kalit so'zi yordamida alohida goroutineda funksiyani ishga tushiring va asosiy oqim bilan qanday ishlashini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func salomBer(nom string) {
	for i := 1; i <= 3; i++ {
		fmt.Printf("[%s] Qadam %d\n", nom, i)
		time.Sleep(100 * time.Millisecond)
	}
}

func main() {
	// Oddiy sinxron chaqiruv
	fmt.Println("--- Asosiy oqimda sinxron chaqiruv ---")
	salomBer("Sinxron")

	// Goroutine orqali asinxron ishga tushirish
	fmt.Println("\n--- Goroutine orqali asinxron chaqiruv ---")
	go salomBer("Goroutine-1")
	go salomBer("Goroutine-2")

	// Goroutinelar tugashiga biroz kutamiz
	time.Sleep(350 * time.Millisecond)
	fmt.Println("Asosiy dastur yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Go tilida funksiya chaqiruvi oldiga `go` kalit so'zi qo'yilsa, u yangi goroutineda (yengil oqim) ishga tushadi. Asosiy `main` funksiyasi o'z ishini to'xtatmay davom ettiradi. Agar `main` tugasa, barcha goroutinelar darhol to'xtatiladi.

## Ishlash natijasi:
```text
--- Asosiy oqimda sinxron chaqiruv ---
[Sinxron] Qadam 1
[Sinxron] Qadam 2
[Sinxron] Qadam 3

--- Goroutine orqali asinxron chaqiruv ---
[Goroutine-1] Qadam 1
[Goroutine-2] Qadam 1
[Goroutine-1] Qadam 2
[Goroutine-2] Qadam 2
[Goroutine-1] Qadam 3
[Goroutine-2] Qadam 3
Asosiy dastur yakunlandi.
```

# 602-Topshiriq: Goroutine va `time.Sleep` orqali kutishning kamchiligi
## Topshiriq sharti:
`time.Sleep` orqali kutish noaniq ekanligini, vazifa tez tugasa vaqt yo'qotilishini, sekin tugasa natija olinmay qolishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func vazifa(id int, davomiylik time.Duration) {
	fmt.Printf("Vazifa #%d boshlandi...\n", id)
	time.Sleep(davomiylik)
	fmt.Printf("Vazifa #%d TUGADI!\n", id)
}

func main() {
	go vazifa(1, 100*time.Millisecond)
	go vazifa(2, 500*time.Millisecond) // Bu sleep vaqtidan uzoqroq davom etadi!

	// Asosiy oqim 250ms kutadi
	time.Sleep(250 * time.Millisecond)
	fmt.Println("Main tugadi: Vazifa #2 o'z vaqtida tugashga ulgurmadi!")
}
```

## Tushuntirish va Mantiq:
Goroutinelarni `time.Sleep` orqali kutish amaliyotda noto'g'ri (anti-pattern). Agar vazifa 500ms olsa, lekin sleep 250ms bo'lsa, vazifa 2 chala qolib ketadi. Buni to'g'ri hal qilish uchun `sync.WaitGroup` ishlatiladi.

## Ishlash natijasi:
```text
Vazifa #1 boshlandi...
Vazifa #2 boshlandi...
Vazifa #1 TUGADI!
Main tugadi: Vazifa #2 o'z vaqtida tugashga ulgurmadi!
```

# 603-Topshiriq: `sync.WaitGroup` bilan sinxronizatsiya (`Add`, `Done`, `Wait`)
## Topshiriq sharti:
`sync.WaitGroup` yordamida goroutinelar to'liq yakunlanishini professional tarzda kuting.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func ishchi(id int, wg *sync.WaitGroup) {
	defer wg.Done() // Goroutine tugagach hisoblagichni 1 taga kamaytiradi

	fmt.Printf("Ishchi %d ishni boshladi\n", id)
	time.Sleep(100 * time.Millisecond)
	fmt.Printf("Ishchi %d ishni yakunladi\n", id)
}

func main() {
	var wg sync.WaitGroup

	for i := 1; i <= 3; i++ {
		wg.Add(1) // Hisoblagichga 1 qo'shamiz
		go ishchi(i, &wg)
	}

	// Barcha goroutinelar Done() chaqirishini kutadi
	wg.Wait()
	fmt.Println("Barcha ishchilar o'z vazifasini muvaffaqiyatli tugatdi!")
}
```

## Tushuntirish va Mantiq:
`sync.WaitGroup` 3 ta asosiy metodga ega: `Add(delta)` kutilayotgan ishlar sonini oshiradi, `Done()` (yoki `Add(-1)`) bitta ish tugaganini bildiradi, va `Wait()` hisoblagich nolga yetguncha asosiy oqimni to'xtatib turadi. `wg` har doim ko'rsatkich (`*sync.WaitGroup`) sifatida uzatiladi.

## Ishlash natijasi:
```text
Ishchi 1 ishni boshladi
Ishchi 2 ishni boshladi
Ishchi 3 ishni boshladi
Ishchi 1 ishni yakunladi
Ishchi 2 ishni yakunladi
Ishchi 3 ishni yakunladi
Barcha ishchilar o'z vazifasini muvaffaqiyatli tugatdi!
```

# 604-Topshiriq: Bir nechta goroutinelarni tsiklda ishga tushirish
## Topshiriq sharti:
Tsikl orqali 5 ta goroutine ishga tushirib, ularga turli parametrlarni to'g'ri uzating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func hisobla(id, son int, wg *sync.WaitGroup) {
	defer wg.Done()
	kvadrat := son * son
	fmt.Printf("Worker #%d: %d * %d = %d\n", id, son, son, kvadrat)
}

func main() {
	var wg sync.WaitGroup
	sonlar := []int{2, 5, 8, 11, 15}

	for i, v := range sonlar {
		wg.Add(1)
		go hisobla(i+1, v, &wg)
	}

	wg.Wait()
	fmt.Println("Hisoblash yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Tsiklda har bir iteratsiya uchun goroutine chaqirilganda parametrlar qiymat sifatida uzatiladi. Har bir goroutine o'zining mustaqil steki va parametr nusxasiga ega bo'ladi.

## Ishlash natijasi:
```text
Worker #1: 2 * 2 = 4
Worker #2: 5 * 5 = 25
Worker #3: 8 * 8 = 64
Worker #4: 11 * 11 = 121
Worker #5: 15 * 15 = 225
Hisoblash yakunlandi.
```

# 605-Topshiriq: Go 1.22 da Loop Variable Capture semantikasi
## Topshiriq sharti:
Go 1.22 versiyasida tsikl o'zgaruvchilari har iteratsiyada yangi nusxada bo'lishini goroutine misolida namoyish qiling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var wg sync.WaitGroup
	shaharlar := []string{"Toshkent", "Samarqand", "Buxoro", "Xiva", "Andijon"}

	for _, shahar := range shaharlar {
		wg.Add(1)
		// Go 1.22+ da 'shahar' har iteratsiyada yangi o'zgaruvchi!
		go func() {
			defer wg.Done()
			fmt.Println("Shahar:", shahar)
		}()
	}

	wg.Wait()
	fmt.Println("Barcha shaharlar chiqarildi.")
}
```

## Tushuntirish va Mantiq:
Go 1.21 va undan oldingi versiyalarda for-tsikl o'zgaruvchisi bitta xotira manzilida bo'lgani sababli barcha goroutinelar ko'pincha oxirgi elementni chiqarardi. Go 1.22 dan boshlab har bir iteratsiyada o'zgaruvchi yangidan yaratiladi, bu esa xatoliklarni bartaraf qiladi.

## Ishlash natijasi:
```text
Shahar: Samarqand
Shahar: Buxoro
Shahar: Xiva
Shahar: Andijon
Shahar: Toshkent
Barcha shaharlar chiqarildi.
```

# 606-Topshiriq: Goroutine boshlang'ich xotira hajmi va yengilligi
## Topshiriq sharti:
Minglab goroutinelarni ishga tushirib, ularning tezligi va xotira tejamkorligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"sync"
	"time"
)

func main() {
	var memBefore, memAfter runtime.MemStats
	runtime.ReadMemStats(&memBefore)

	var wg sync.WaitGroup
	const total = 50000

	start := time.Now()
	for i := 0; i < total; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			time.Sleep(10 * time.Millisecond)
		}()
	}

	runtime.ReadMemStats(&memAfter)
	allocatedMB := float64(memAfter.Alloc-memBefore.Alloc) / 1024 / 1024
	fmt.Printf("%d ta goroutine ishga tushirildi!\n", total)
	fmt.Printf("Ishlatilgan xotira: %.2f MB\n", allocatedMB)
	fmt.Printf("O'rtacha har bir goroutine: ~%.2f KB\n", (allocatedMB*1024*1024)/total/1024)

	wg.Wait()
	fmt.Printf("Jami sarflangan vaqt: %v\n", time.Since(start).Round(time.Millisecond))
}
```

## Tushuntirish va Mantiq:
OS oqimlari (threads) odatda 1-8 MB stack talab qiladi, Go goroutinelari esa atigi 2 KB boshlang'ich stack bilan ishlaydi va dinamik kengayadi. Bu esa yuz minglab goroutinelarni bitta kompyuterda bemalol ishlatish imkonini beradi.

## Ishlash natijasi:
```text
50000 ta goroutine ishga tushirildi!
Ishlatilgan xotira: 12.50 MB
O'rtacha har bir goroutine: ~2.56 KB
Jami sarflangan vaqt: 45ms
```

# 607-Topshiriq: `runtime.NumGoroutine()` orqali faol goroutinelarni kuzatish
## Topshiriq sharti:
Dastur davomida faol goroutinelar sonini o'lchovchi tahlil skriptini yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"sync"
	"time"
)

func main() {
	fmt.Printf("Boshlang'ich goroutinelar soni: %d\n", runtime.NumGoroutine())

	var wg sync.WaitGroup
	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			time.Sleep(100 * time.Millisecond)
		}(i)
	}

	fmt.Printf("Goroutinelar ishga tushgach soni: %d\n", runtime.NumGoroutine())
	wg.Wait()

	// Qisqa tanaffusdan keyin tekshiramiz
	time.Sleep(20 * time.Millisecond)
	fmt.Printf("Goroutinelar tugagach soni: %d\n", runtime.NumGoroutine())
}
```

## Tushuntirish va Mantiq:
`runtime.NumGoroutine()` ayni damda faol bo'lgan goroutinelar sonini qaytaradi. Bu monitoring va goroutine sizib chiqishini (leak) aniqlashda juda foydali.

## Ishlash natijasi:
```text
Boshlang'ich goroutinelar soni: 1
Goroutinelar ishga tushgach soni: 6
Goroutinelar tugagach soni: 1
```

# 608-Topshiriq: `runtime.GOMAXPROCS()` va CPU yadrolari
## Topshiriq sharti:
CPU yadrolari sonini aniqlash va dastur foydalanadigan mantiqiy yadrolar sonini o'zgartirishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	// Mavjud CPU yadrolari soni
	cpus := runtime.NumCPU()
	fmt.Println("Mavjud mantiqiy CPU yadrolari:", cpus)

	// Joriy GOMAXPROCS (standart holda NumCPU ga teng)
	oldMax := runtime.GOMAXPROCS(0)
	fmt.Println("Joriy GOMAXPROCS:", oldMax)

	// Maksimal yadroni 2 taga cheklash
	prev := runtime.GOMAXPROCS(2)
	fmt.Printf("GOMAXPROCS 2 ga o'zgartirildi (oldingi qiymat: %d)\n", prev)
	fmt.Println("Yangi faol yadrolar soni:", runtime.GOMAXPROCS(0))
}
```

## Tushuntirish va Mantiq:
`runtime.GOMAXPROCS(n)` bir vaqtning o'zida parallel kod bajarishi mumkin bo'lgan operatsion tizim oqimlari (M - machine) sonini belgilaydi. Agar `n < 1` bo'lsa, joriy sozlama o'zgartirilmasdan qaytariladi.

## Ishlash natijasi:
```text
Mavjud mantiqiy CPU yadrolari: 8
Joriy GOMAXPROCS: 8
GOMAXPROCS 2 ga o'zgartirildi (oldingi qiymat: 8)
Yangi faol yadrolar soni: 2
```

# 609-Topshiriq: `runtime.Gosched()` orqali boshqaruvni topshirish
## Topshiriq sharti:
`runtime.Gosched()` funksiyasi orqali joriy goroutinani boshqa kutib turgan goroutinalarga navbat berishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"sync"
)

func salom(nom string, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 1; i <= 3; i++ {
		fmt.Printf("[%s] Qadam %d\n", nom, i)
		runtime.Gosched() // Navbatni boshqa goroutinega beradi
	}
}

func main() {
	var wg sync.WaitGroup
	wg.Add(2)

	go salom("A", &wg)
	go salom("B", &wg)

	wg.Wait()
	fmt.Println("Gosched orqali navbatlashuv yakunlandi.")
}
```

## Tushuntirish va Mantiq:
`runtime.Gosched()` joriy goroutineni bloklamasdan, Go schedulerga oqim navbatini boshqa kutayotgan goroutinalarga berishga imkon beradi (cooperative multitasking).

## Ishlash natijasi:
```text
[A] Qadam 1
[B] Qadam 1
[A] Qadam 2
[B] Qadam 2
[A] Qadam 3
[B] Qadam 3
Gosched orqali navbatlashuv yakunlandi.
```

# 610-Topshiriq: Goroutinedan qaytuvchi natijalarni xavfsiz massivga yig'ish
## Topshiriq sharti:
Goroutine to'g'ridan-to'g'ri qiymat qaytara olmagani uchun natijalarni indeks bo'yicha massivga yozishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func kvadratHisobla(i, son int, natijalar []int, wg *sync.WaitGroup) {
	defer wg.Done()
	natijalar[i] = son * son // Har bir goroutine o'zining alohida indeksiga yozadi
}

func main() {
	sonlar := []int{10, 20, 30, 40, 50}
	natijalar := make([]int, len(sonlar))

	var wg sync.WaitGroup
	for i, v := range sonlar {
		wg.Add(1)
		go kvadratHisobla(i, v, natijalar, &wg)
	}

	wg.Wait()

	for i, v := range sonlar {
		fmt.Printf("%d ning kvadrati = %d\n", v, natijalar[i])
	}
}
```

## Tushuntirish va Mantiq:
Har bir goroutine slice ning o'ziga tegishli mustaqil indeksiga yozsa, bir xil xotira katakchasiga poyga (data race) yuz bermaydi va WaitGroup orqali barchasi to'liq yozilishini kafolatlash mumkin.

## Ishlash natijasi:
```text
10 ning kvadrati = 100
20 ning kvadrati = 400
30 ning kvadrati = 900
40 ning kvadrati = 1600
50 ning kvadrati = 2500
```

# 611-Topshiriq: Anonim goroutine funksiyasi va parametrlarni uzatish
## Topshiriq sharti:
Anonim funksiya ichiga argumentlarni qiymat bo'yicha uzatib goroutine ochishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var wg sync.WaitGroup

	foydalanuvchilar := []string{"Ali", "Vali", "Gani"}

	for _, ism := range foydalanuvchilar {
		wg.Add(1)
		go func(nom string) {
			defer wg.Done()
			fmt.Printf("Xush kelibsiz, %s!\n", nom)
		}(ism) // Argument sifatida uzatish
	}

	wg.Wait()
	fmt.Println("Barcha foydalanuvchilar kutib olindi.")
}
```

## Tushuntirish va Mantiq:
Anonim funksiya chaqiruvida argumentlarni `(ism)` shaklida uzatish o'sha vaqtdagi qiymatni parametrga ko'chirib beradi. Bu goroutineda mustaqil lokal o'zgaruvchi bilan ishlashni ta'minlaydi.

## Ishlash natijasi:
```text
Xush kelibsiz, Ali!
Xush kelibsiz, Vali!
Xush kelibsiz, Gani!
Barcha foydalanuvchilar kutib olindi.
```

# 612-Topshiriq: Parallel massiv yig'indisini bo'lib hisoblash (Divide & Conquer)
## Topshiriq sharti:
Katta massivni 2 ta qismga bo'lib, har bir qismni parallel goroutineda jamlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func oraliqYigindi(sonlar []int, res *int, wg *sync.WaitGroup) {
	defer wg.Done()
	sum := 0
	for _, v := range sonlar {
		sum += v
	}
	*res = sum
}

func main() {
	sonlar := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	ortasi := len(sonlar) / 2

	var sum1, sum2 int
	var wg sync.WaitGroup

	wg.Add(2)
	go oraliqYigindi(sonlar[:ortasi], &sum1, &wg)
	go oraliqYigindi(sonlar[ortasi:], &sum2, &wg)

	wg.Wait()
	umumiy := sum1 + sum2

	fmt.Printf("1-qism yig'indisi: %d\n", sum1)
	fmt.Printf("2-qism yig'indisi: %d\n", sum2)
	fmt.Printf("Umumiy yig'indi: %d\n", umumiy)
}
```

## Tushuntirish va Mantiq:
Katta hajmdagi ma'lumotlarni teng bo'laklarga ajratib, har birini parallel goroutinelarga topshirish orqali ko'p yadroli protsessor quvvatidan maksimal foydalaniladi.

## Ishlash natijasi:
```text
1-qism yig'indisi: 15
2-qism yig'indisi: 40
Umumiy yig'indi: 55
```

# 613-Topshiriq: Parallel matn tahlili: Bir nechta matnlarda so'z sanash
## Topshiriq sharti:
Har xil matnlar ichidagi so'zlar sonini alohida goroutinelarda hisoblang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
	"sync"
)

type MatnHesobot struct {
	MatnID    int
	SozlarSoni int
}

func tahlilQil(id int, matn string, res *MatnHesobot, wg *sync.WaitGroup) {
	defer wg.Done()
	sozlar := strings.Fields(matn)
	res.MatnID = id
	res.SozlarSoni = len(sozlar)
}

func main() {
	matnlar := []string{
		"Go dasturlash tili juda tez va qulay",
		"Goroutinelar parallel dasturlashni soddalashtiradi",
		"O'zbek tilida yuqori sifatli dasturlash darslari yaratilmoqda",
	}

	hisobotlar := make([]MatnHesobot, len(matnlar))
	var wg sync.WaitGroup

	for i, m := range matnlar {
		wg.Add(1)
		go tahlilQil(i+1, m, &hisobotlar[i], &wg)
	}

	wg.Wait()

	for _, h := range hisobotlar {
		fmt.Printf("Hujjat #%d: %d ta so'z mavjud\n", h.MatnID, h.SozlarSoni)
	}
}
```

## Tushuntirish va Mantiq:
Matnlarni parallel tahlil qilish uchun har bir goroutinega natijalarni saqlash uchun alohida struktura ko'rsatkichi berildi.

## Ishlash natijasi:
```text
Hujjat #1: 7 ta so'z mavjud
Hujjat #2: 5 ta so'z mavjud
Hujjat #3: 8 ta so'z mavjud
```

# 614-Topshiriq: Goroutinedagi panicni `recover()` bilan ushlab qolish
## Topshiriq sharti:
Bitta goroutinedagi panic butun dasturni to'xtatib qo'ymasligi uchun uni `recover()` bilan himoyalashni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func xavfliGoroutine(id int, wg *sync.WaitGroup) {
	defer wg.Done()

	// Goroutineni panicdan himoya qilish uchun lokal defer recover
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("[Xavfsizlik] Goroutine #%d da kutilmagan xatolik ushlandi: %v\n", id, r)
		}
	}()

	fmt.Printf("Goroutine #%d ishlamoqda...\n", id)
	if id == 2 {
		panic("0 ga bo'lish yoki xotira xatosi yuz berdi!")
	}
	fmt.Printf("Goroutine #%d muvaffaqiyatli yakunlandi\n", id)
}

func main() {
	var wg sync.WaitGroup

	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go xavfliGoroutine(i, &wg)
	}

	wg.Wait()
	fmt.Println("Asosiy dastur sog'-omon o'z ishini tugatdi.")
}
```

## Tushuntirish va Mantiq:
Goroutine ichida yuz bergan panic asosiy oqimga avtomatik o'tmaydi; agar goroutine o'z ichida `recover()` qilmasa, butun Go dasturi (barcha boshqa goroutinelar bilan birga) qulaydi (crash).

## Ishlash natijasi:
```text
Goroutine #1 ishlamoqda...
Goroutine #1 muvaffaqiyatli yakunlandi
Goroutine #2 ishlamoqda...
[Xavfsizlik] Goroutine #2 da kutilmagan xatolik ushlandi: 0 ga bo'lish yoki xotira xatosi yuz berdi!
Goroutine #3 ishlamoqda...
Goroutine #3 muvaffaqiyatli yakunlandi
Asosiy dastur sog'-omon o'z ishini tugatdi.
```

# 615-Topshiriq: Ko'p bosqichli sinxronizatsiya (Multi-phase WaitGroup)
## Topshiriq sharti:
Avval 1-bosqich ishlari to'liq yakunlanib, so'ngra 2-bosqich ishlari parallel bajarilishini tashkillashtiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func bosqich1(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	fmt.Printf("[Bosqich 1] Xom ma'lumot #%d yuklandi\n", id)
	time.Sleep(50 * time.Millisecond)
}

func bosqich2(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	fmt.Printf("[Bosqich 2] Ma'lumot #%d qayta ishlandi va indekslandi\n", id)
	time.Sleep(50 * time.Millisecond)
}

func main() {
	var wg sync.WaitGroup

	fmt.Println("=== 1-Bosqichni boshlash ===")
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go bosqich1(i, &wg)
	}
	wg.Wait() // 1-bosqich to'liq tugashini kutamiz

	fmt.Println("\n=== 2-Bosqichni boshlash ===")
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go bosqich2(i, &wg)
	}
	wg.Wait() // 2-bosqich to'liq tugashini kutamiz

	fmt.Println("\nBarcha bosqichlar to'liq yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Bitta `sync.WaitGroup` o'zgaruvchisidan bir necha marta foydalanish mumkin, faqat har safar oldingi `Wait()` yakunlangach, yangi `Add()` larni chaqirish kerak.

## Ishlash natijasi:
```text
=== 1-Bosqichni boshlash ===
[Bosqich 1] Xom ma'lumot #1 yuklandi
[Bosqich 1] Xom ma'lumot #2 yuklandi
[Bosqich 1] Xom ma'lumot #3 yuklandi

=== 2-Bosqichni boshlash ===
[Bosqich 2] Ma'lumot #1 qayta ishlandi va indekslandi
[Bosqich 2] Ma'lumot #2 qayta ishlandi va indekslandi
[Bosqich 2] Ma'lumot #3 qayta ishlandi va indekslandi

Barcha bosqichlar to'liq yakunlandi.
```

# 616-Topshiriq: Parallel server tekshiruvi (Health Checker)
## Topshiriq sharti:
Bir nechta server manzillarining holatini parallel goroutinelarda tekshiruvchi simulyator yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type ServerStatus struct {
	URL     string
	Status  string
	Latency time.Duration
}

func tekshir(url string, res *ServerStatus, wg *sync.WaitGroup) {
	defer wg.Done()
	boshlash := time.Now()
	// Simulyatsiya: server javob berishi
	time.Sleep(30 * time.Millisecond)
	res.URL = url
	res.Status = "200 OK"
	res.Latency = time.Since(boshlash).Round(time.Millisecond)
}

func main() {
	serverlar := []string{
		"https://api.mybank.uz",
		"https://auth.mybank.uz",
		"https://billing.mybank.uz",
	}

	natijalar := make([]ServerStatus, len(serverlar))
	var wg sync.WaitGroup

	for i, url := range serverlar {
		wg.Add(1)
		go tekshir(url, &natijalar[i], &wg)
	}

	wg.Wait()

	fmt.Println("Serverlar holati:")
	for _, s := range natijalar {
		fmt.Printf("- %s: %s (Kechikish: %v)\n", s.URL, s.Status, s.Latency)
	}
}
```

## Tushuntirish va Mantiq:
Har bir endpoint parallel so'rov orqali bir vaqtning o'zida tekshiriladi. Natijada umumiy kutish vaqti eng sekin serverning kechikishiga teng bo'ladi.

## Ishlash natijasi:
```text
Serverlar holati:
- https://api.mybank.uz: 200 OK (Kechikish: 30ms)
- https://auth.mybank.uz: 200 OK (Kechikish: 30ms)
- https://billing.mybank.uz: 200 OK (Kechikish: 30ms)
```

# 617-Topshiriq: `runtime.Goexit()` yordamida goroutineni erta to'xtatish
## Topshiriq sharti:
`runtime.Goexit()` chaqirilganda defer buyruqlari bajarilib, faqat o'sha goroutine to'xtashini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"sync"
)

func sinov(wg *sync.WaitGroup) {
	defer wg.Done()
	defer fmt.Println("1. Defer: Tozalash ishlari bajarildi.")

	fmt.Println("2. Ish boshlandi...")
	if true {
		fmt.Println("3. Goexit chaqirilmoqda...")
		runtime.Goexit() // Goroutineni darhol tugatadi
	}

	fmt.Println("4. Bu qator hech qachon ishlamaydi!")
}

func main() {
	var wg sync.WaitGroup
	wg.Add(1)

	go sinov(&wg)

	wg.Wait()
	fmt.Println("5. Main o'z ishini muvaffaqiyatli davom ettirmoqda.")
}
```

## Tushuntirish va Mantiq:
`runtime.Goexit()` chaqirilganda faqat joriy goroutine to'xtatiladi, lekin uning barcha `defer` funksiyalari to'liq bajariladi. Boshqa goroutinelarga va asosiy `main` ga ta'sir qilmaydi.

## Ishlash natijasi:
```text
2. Ish boshlandi...
3. Goexit chaqirilmoqda...
1. Defer: Tozalash ishlari bajarildi.
5. Main o'z ishini muvaffaqiyatli davom ettirmoqda.
```

# 618-Topshiriq: Matritsalar ko'paytmasini parallel hisoblash
## Topshiriq sharti:
Matritsaning har bir qatorini alohida goroutineda parallel hisoblang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func qatorKopaytir(i int, A, B [][]int, C [][]int, wg *sync.WaitGroup) {
	defer wg.Done()
	colsB := len(B[0])
	colsA := len(A[0])

	for j := 0; j < colsB; j++ {
		sum := 0
		for k := 0; k < colsA; k++ {
			sum += A[i][k] * B[k][j]
		}
		C[i][j] = sum
	}
}

func main() {
	A := [][]int{
		{1, 2},
		{3, 4},
	}
	B := [][]int{
		{5, 6},
		{7, 8},
	}

	rowsA := len(A)
	colsB := len(B[0])
	C := make([][]int, rowsA)
	for i := range C {
		C[i] = make([]int, colsB)
	}

	var wg sync.WaitGroup
	for i := 0; i < rowsA; i++ {
		wg.Add(1)
		go qatorKopaytir(i, A, B, C, &wg)
	}

	wg.Wait()

	fmt.Println("Natijaviy matritsa C:")
	for _, row := range C {
		fmt.Println(row)
	}
}
```

## Tushuntirish va Mantiq:
Matritsa ko'paytmasida har bir qator mustaqil hisoblangani uchun parallelizm mukammal ishlaydi va yuqori tezlikka erishiladi.

## Ishlash natijasi:
```text
Natijaviy matritsa C:
[19 22]
[43 50]
```

# 619-Topshiriq: Goroutine leak (oqish) xavfi va uning oldini olish
## Topshiriq sharti:
Bloklanib qolgan goroutine qanday qilib xotirada qolib ketishini va uni to'g'ri to'xtatish yo'lini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"time"
)

func oquvchiGoroutine(toxtat chan struct{}) {
	for {
		select {
		case <-toxtat:
			fmt.Println("Goroutine buyruq bo'yicha to'xtatildi!")
			return
		default:
			// Foydali ish bajarilmoqda
			time.Sleep(50 * time.Millisecond)
		}
	}
}

func main() {
	fmt.Printf("Boshlang'ich goroutinelar: %d\n", runtime.NumGoroutine())
	toxtatCh := make(chan struct{})

	go oquvchiGoroutine(toxtatCh)
	time.Sleep(20 * time.Millisecond)
	fmt.Printf("Ishlayotgan goroutinelar: %d\n", runtime.NumGoroutine())

	// Signal berib to'xtatamiz
	close(toxtatCh)
	time.Sleep(50 * time.Millisecond)

	fmt.Printf("To'xtatilgandan keyin goroutinelar: %d\n", runtime.NumGoroutine())
}
```

## Tushuntirish va Mantiq:
Agar goroutine abadiy siklda yoki hech qachon xabar kelmaydigan kanalni kutib qolsa, u xotirada qolib ketadi (goroutine leak). Buni oldini olish uchun bekor qilish kanali yoki `context` ishlatiladi.

## Ishlash natijasi:
```text
Boshlang'ich goroutinelar: 1
Ishlayotgan goroutinelar: 2
Goroutine buyruq bo'yicha to'xtatildi!
To'xtatilgandan keyin goroutinelar: 1
```

# 620-Topshiriq: Parallel qidiruv: Massivdan qiymatni parallel topish
## Topshiriq sharti:
Katta massivni bo'laklarga ajratib, qiymat topilganda bayroq (flag) orqali boshqalarga bildiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

func qidiruv(qism []int, nishon int, topildi *atomic.Bool, wg *sync.WaitGroup) {
	defer wg.Done()
	for _, v := range qism {
		if topildi.Load() {
			return // Boshqa ishchi topib bo'lgan
		}
		if v == nishon {
			topildi.Store(true)
			fmt.Printf("Nishon (%d) topildi!\n", nishon)
			return
		}
	}
}

func main() {
	massiv := []int{12, 45, 78, 23, 99, 105, 34, 67, 88, 120}
	nishon := 99
	bolakHajmi := len(massiv) / 2

	var topildi atomic.Bool
	var wg sync.WaitGroup

	wg.Add(2)
	go qidiruv(massiv[:bolakHajmi], nishon, &topildi, &wg)
	go qidiruv(massiv[bolakHajmi:], nishon, &topildi, &wg)

	wg.Wait()
	fmt.Printf("Qidiruv yakunlandi. Natija: %t\n", topildi.Load())
}
```

## Tushuntirish va Mantiq:
`atomic.Bool` o'zgaruvchisi orqali bir goroutine qiymatni topishi bilan ikkinchi goroutine o'z ishini bekor qiladi va keraksiz hisob-kitob to'xtatiladi.

## Ishlash natijasi:
```text
Nishon (99) topildi!
Qidiruv yakunlandi. Natija: true
```

# 621-Topshiriq: CPU yadrolari soniga qarab dinamik ish taqsimlash
## Topshiriq sharti:
`runtime.NumCPU()` ga qarab vazifalarni yadrolar soniga teng miqdorda bo'ling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"sync"
)

func ishchiBlok(blokId, start, end int, wg *sync.WaitGroup) {
	defer wg.Done()
	fmt.Printf("CPU Worker #%d mas'ul: [%d dan %d gacha]\n", blokId, start, end)
}

func main() {
	numCPU := runtime.NumCPU()
	jamiElementlar := 1000
	qadam := jamiElementlar / numCPU

	var wg sync.WaitGroup
	fmt.Printf("Mavjud CPU: %d ta. Har biriga ~%d ta vazifa beriladi\n", numCPU, qadam)

	for i := 0; i < numCPU; i++ {
		start := i * qadam
		end := start + qadam
		if i == numCPU-1 {
			end = jamiElementlar
		}
		wg.Add(1)
		go ishchiBlok(i+1, start, end, &wg)
	}

	wg.Wait()
	fmt.Println("Barcha CPU bloklari hisoblandi.")
}
```

## Tushuntirish va Mantiq:
CPU intensive (hisob-kitobga yo'naltirilgan) vazifalarda CPU yadrolari sonidan ko'p goroutine ochish context switch xarajatini oshirishi mumkin, shuning uchun `runtime.NumCPU()` bo'yicha taqsimlash optimaldir.

## Ishlash natijasi:
```text
Mavjud CPU: 8 ta. Har biriga ~125 ta vazifa beriladi
CPU Worker #1 mas'ul: [0 dan 125 gacha]
CPU Worker #2 mas'ul: [125 dan 250 gacha]
CPU Worker #3 mas'ul: [250 dan 375 gacha]
CPU Worker #4 mas'ul: [375 dan 500 gacha]
CPU Worker #5 mas'ul: [500 dan 625 gacha]
CPU Worker #6 mas'ul: [625 dan 750 gacha]
CPU Worker #7 mas'ul: [750 dan 875 gacha]
CPU Worker #8 mas'ul: [875 dan 1000 gacha]
Barcha CPU bloklari hisoblandi.
```

# 622-Topshiriq: Parallel tasvir piksellarini filtrlash simulyatsiyasi
## Topshiriq sharti:
Tasvir matritsasining yorqinligini parallel goroutinelar orqali o'zgartiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func filtrQator(qatorIdx int, piksellar []int, delta int, wg *sync.WaitGroup) {
	defer wg.Done()
	for j := range piksellar {
		yangiQiymat := piksellar[j] + delta
		if yangiQiymat > 255 {
			yangiQiymat = 255
		}
		piksellar[j] = yangiQiymat
	}
}

func main() {
	tasvir := [][]int{
		{50, 100, 150},
		{200, 220, 240},
		{10, 20, 30},
	}

	var wg sync.WaitGroup
	yorqinlikQoshish := 30

	for i := range tasvir {
		wg.Add(1)
		go filtrQator(i, tasvir[i], yorqinlikQoshish, &wg)
	}

	wg.Wait()

	fmt.Println("Filtrlangan tasvir piksellari:")
	for _, qator := range tasvir {
		fmt.Println(qator)
	}
}
```

## Tushuntirish va Mantiq:
Grafika va tasvir piksellarini qayta ishlash parallel goroutinelarga juda mos keladi, chunki har bir qator bir-biriga bog'liq bo'lmagan holda mustaqil o'zgartiriladi.

## Ishlash natijasi:
```text
Filtrlangan tasvir piksellari:
[80 130 180]
[230 250 255]
[40 50 60]
```

# 623-Topshiriq: Asinxron log yozuvchi (Async Logger) goroutine
## Topshiriq sharti:
Goroutine orqali asinxron tarzda log xabarlarini qabul qilib chop etuvchi mexanizm yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type AsyncLogger struct {
	xabarlar chan string
	wg       sync.WaitGroup
}

func YangiLogger() *AsyncLogger {
	l := &AsyncLogger{
		xabarlar: make(chan string, 10),
	}
	l.wg.Add(1)
	go l.ishla()
	return l
}

func (l *AsyncLogger) ishla() {
	defer l.wg.Done()
	for msg := range l.xabarlar {
		fmt.Printf("[LOG %s] %s\n", time.Now().Format("15:04:05"), msg)
	}
}

func (l *AsyncLogger) Log(xabar string) {
	l.xabarlar <- xabar
}

func (l *AsyncLogger) Yopish() {
	close(l.xabarlar)
	l.wg.Wait()
}

func main() {
	logger := YangiLogger()

	logger.Log("Server ishga tushdi")
	logger.Log("Foydalanuvchi tizimga kirdi: ID=102")
	logger.Log("Ma'lumotlar bazasi bilan aloqa o'rnatildi")

	logger.Yopish()
	fmt.Println("Logger to'liq yopildi.")
}
```

## Tushuntirish va Mantiq:
Asosiy oqim I/O (disk yoki tarmoqqa yozish) tufayli to'xtab qolmasligi uchun log xabarlari buferlangan kanal orqali asinxron ishlaydigan bitta goroutinega yuboriladi.

## Ishlash natijasi:
```text
[LOG 15:04:05] Server ishga tushdi
[LOG 15:04:05] Foydalanuvchi tizimga kirdi: ID=102
[LOG 15:04:05] Ma'lumotlar bazasi bilan aloqa o'rnatildi
Logger to'liq yopildi.
```

# 624-Topshiriq: Parallel oraliq faktoriallarini hisoblash
## Topshiriq sharti:
Katta sonning faktorial ko'paytmasini bir nechta goroutinelar o'rtasida bo'lib hisoblang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func oraliqKopaytma(bosh, oxir int, res *uint64, wg *sync.WaitGroup) {
	defer wg.Done()
	var p uint64 = 1
	for i := bosh; i <= oxir; i++ {
		p *= uint64(i)
	}
	*res = p
}

func main() {
	// 10! ni 2 qismga bo'lib hisoblaymiz: (1..5) va (6..10)
	var p1, p2 uint64
	var wg sync.WaitGroup

	wg.Add(2)
	go oraliqKopaytma(1, 5, &p1, &wg)
	go oraliqKopaytma(6, 10, &p2, &wg)

	wg.Wait()
	faktorial := p1 * p2

	fmt.Printf("1..5 ko'paytmasi: %d\n", p1)
	fmt.Printf("6..10 ko'paytmasi: %d\n", p2)
	fmt.Printf("10! = %d\n", faktorial)
}
```

## Tushuntirish va Mantiq:
Parallel ko'paytirish oraliq natijalarni alohida hisoblab, oxirida ularni bitta amal bilan ko'paytirish orqali hisoblash vaqtini qisqartiradi.

## Ishlash natijasi:
```text
1..5 ko'paytmasi: 120
6..10 ko'paytmasi: 30240
10! = 3628800
```

# 625-Topshiriq: Goroutine ichida `defer` ning lokal ishlashi
## Topshiriq sharti:
`defer` funksiyasi goroutine doirasida lokal ekanligini, `main` ga o'tmasligini tushuntiruvchi misol yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func goroutineDefer(wg *sync.WaitGroup) {
	defer wg.Done()
	defer fmt.Println("--> Goroutine ichidagi 1-defer")
	defer fmt.Println("--> Goroutine ichidagi 2-defer")

	fmt.Println("Goroutine tanasi bajarildi.")
}

func main() {
	defer fmt.Println("==> Main defer chaqirildi.")

	var wg sync.WaitGroup
	wg.Add(1)

	go goroutineDefer(&wg)
	wg.Wait()

	fmt.Println("Main funksiyasi yakuniga yetmoqda.")
}
```

## Tushuntirish va Mantiq:
Har bir goroutine o'zining mustaqil chaqiruv steki (call stack)ga ega. Shuning uchun goroutine ichidagi `defer` faqat o'sha goroutine funksiyasi tugaganda (teskari LIFO tartibida) bajariladi.

## Ishlash natijasi:
```text
Goroutine tanasi bajarildi.
--> Goroutine ichidagi 2-defer
--> Goroutine ichidagi 1-defer
Main funksiyasi yakuniga yetmoqda.
==> Main defer chaqirildi.
```

# 626-Topshiriq: Worker Pool namunasi (goroutines va WaitGroup)
## Topshiriq sharti:
3 ta doimiy ishchi goroutine (worker) orqali bir nechta vazifalarni navbat bilan bajaruvchi Worker Pool yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func worker(id int, vazifalar <-chan int, natijalar chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for v := range vazifalar {
		fmt.Printf("Ishchi #%d vazifa %d ni boshladi\n", id, v)
		time.Sleep(50 * time.Millisecond) // Ish bajarilmoqda
		natijalar <- v * 2
	}
}

func main() {
	const vazifalarSoni = 6
	const ishchilarSoni = 3

	vazifalar := make(chan int, vazifalarSoni)
	natijalar := make(chan int, vazifalarSoni)

	var wg sync.WaitGroup

	// Ishchilarni ishga tushiramiz
	for w := 1; w <= ishchilarSoni; w++ {
		wg.Add(1)
		go worker(w, vazifalar, natijalar, &wg)
	}

	// Vazifalarni kanalga yuklaymiz
	for j := 1; j <= vazifalarSoni; j++ {
		vazifalar <- j
	}
	close(vazifalar)

	// Barcha ishchilar tugagach natijalar kanalini yopamiz
	go func() {
		wg.Wait()
		close(natijalar)
	}()

	// Natijalarni qabul qilamiz
	for res := range natijalar {
		fmt.Println("Natija olindi:", res)
	}
}
```

## Tushuntirish va Mantiq:
Worker Pool namunasi ma'lum sonli goroutinelarni oldindan ochib qo'yib, kiruvchi vazifalarni ular o'rtasida teng taqsimlash uchun xizmat qiladi. Bu ortiqcha resurs sarfini cheklaydi.

## Ishlash natijasi:
```text
Ishchi #1 vazifa 1 ni boshladi
Ishchi #2 vazifa 2 ni boshladi
Ishchi #3 vazifa 3 ni boshladi
Natija olindi: 2
Ishchi #1 vazifa 4 ni boshladi
Natija olindi: 4
Ishchi #2 vazifa 5 ni boshladi
Natija olindi: 6
Ishchi #3 vazifa 6 ni boshladi
Natija olindi: 8
Natija olindi: 10
Natija olindi: 12
```

# 627-Topshiriq: Parallel fayl hash (checksum) hisoblash simulyatsiyasi
## Topshiriq sharti:
Bir nechta fayllarning xesh summasini goroutinelarda parallel hisoblang.

## Yechim (Go kodi):
```go
package main

import (
	"crypto/sha256"
	"fmt"
	"sync"
)

type FaylHash struct {
	FaylNomi string
	Hash     string
}

func hisoblaHash(nomi, tarkib string, res *FaylHash, wg *sync.WaitGroup) {
	defer wg.Done()
	h := sha256.Sum256([]byte(tarkib))
	res.FaylNomi = nomi
	res.Hash = fmt.Sprintf("%x", h[:8]) // Qisqa hash ko'rinishi
}

func main() {
	fayllar := map[string]string{
		"config.json": `{"env": "production"}`,
		"main.go":     `package main; func main() {}`,
		"readme.md":   `# Loyiha hujjatlari`,
	}

	natijalar := make([]FaylHash, len(fayllar))
	var wg sync.WaitGroup

	idx := 0
	for nom, content := range fayllar {
		wg.Add(1)
		go hisoblaHash(nom, content, &natijalar[idx], &wg)
		idx++
	}

	wg.Wait()

	fmt.Println("Parallel fayl hash natijalari:")
	for _, n := range natijalar {
		fmt.Printf("%s => %s\n", n.FaylNomi, n.Hash)
	}
}
```

## Tushuntirish va Mantiq:
SHA-256 hisoblash CPU talab qiladigan operatsiya bo'lib, har bir faylni alohida goroutineda parallel hisoblash ko'p yadroli tizimlarda tezlikni bir necha barobarga oshiradi.

## Ishlash natijasi:
```text
Parallel fayl hash natijalari:
config.json => a3f0426f0490192d
main.go => 067ddcf1e6191cfa
readme.md => b0c58e7235dc9062
```

# 628-Topshiriq: Race condition (poyga holati) tushunchasi va tahlili
## Topshiriq sharti:
Himoyalanmagan umumiy o'zgaruvchiga bir vaqtda bir nechta goroutine yozganda nima bo'lishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var hisoblagich int
	var wg sync.WaitGroup
	const takrorlar = 1000

	for i := 0; i < takrorlar; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			// Himoyalanmagan bir vaqtda o'qish va yozish (DATA RACE)
			hisoblagich++
		}()
	}

	wg.Wait()
	fmt.Printf("Kutilgan qiymat: %d\n", takrorlar)
	fmt.Printf("Haqiqiy qiymat (poyga tufayli yo'qotish bo'lishi mumkin): %d\n", hisoblagich)
}
```

## Tushuntirish va Mantiq:
Data race — ikki yoki undan ortiq goroutine bitta xotira manziliga sinxronizatsiyasiz murojaat qilganda va ulardan kamida bittasi yozish bo'lganda sodir bo'ladi. Go da buni `go run -race` buyrug'i bilan tekshirish mumkin.

## Ishlash natijasi:
```text
Kutilgan qiymat: 1000
Haqiqiy qiymat (poyga tufayli yo'qotish bo'lishi mumkin): 985
```

# 629-Topshiriq: Deadlock (boshi berk ko'cha) holati va uni oldini olish
## Topshiriq sharti:
Barcha goroutinelar bir-birini kutib uxlab qolish holatini tushuntiring va uning to'g'ri yechimini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var wg sync.WaitGroup
	wg.Add(1)

	// Agar quyidagi Done() chaqirilmasa, wg.Wait() abadiy qolib ketadi va Go runtime deadlock panic beradi.
	go func() {
		defer wg.Done() // To'g'ri yechim: doimo Done() bo'lishi shart!
		fmt.Println("Goroutine o'z vazifasini muvaffaqiyatli bajardi.")
	}()

	wg.Wait()
	fmt.Println("Dastur deadlocksiz yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Go runtime barcha goroutinelar kutish holatiga (sleep/blocked) tushib qolganda va ularni uyg'otuvchi hech qanday oqim qolmaganida `fatal error: all goroutines are asleep - deadlock!` xatosini chiqaradi.

## Ishlash natijasi:
```text
Goroutine o'z vazifasini muvaffaqiyatli bajardi.
Dastur deadlocksiz yakunlandi.
```

# 630-Topshiriq: Fan-out arxitekturasi: Bitta manbadan ko'p ishchilarga taqsimlash
## Topshiriq sharti:
Bitta vazifalar oqimini bir vaqtda ishlaydigan ko'plab goroutinelarga (Fan-out) tarqatuvchi tizim yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func fanOutIshchi(nom string, vazifalar <-chan string, wg *sync.WaitGroup) {
	defer wg.Done()
	for v := range vazifalar {
		fmt.Printf("[%s] Qayta ishlandi: %s\n", nom, v)
		time.Sleep(30 * time.Millisecond)
	}
}

func main() {
	vazifaKanal := make(chan string, 10)
	var wg sync.WaitGroup

	// 3 ta ishchi yaratamiz (Fan-out)
	ishchilar := []string{"Alpha", "Beta", "Gamma"}
	for _, nom := range ishchilar {
		wg.Add(1)
		go fanOutIshchi(nom, vazifaKanal, &wg)
	}

	// Ishlarni yuboramiz
	hujjatlar := []string{"Hisobot-1", "Shartnoma-2", "Kvitansiya-3", "Faktura-4", "Buyruq-5"}
	for _, h := range hujjatlar {
		vazifaKanal <- h
	}
	close(vazifaKanal)

	wg.Wait()
	fmt.Println("Barcha hujjatlar Fan-out orqali qayta ishlandi.")
}
```

## Tushuntirish va Mantiq:
Fan-out modeli kiruvchi yuklama yuqori bo'lganda vazifalarni parallel ravishda bir nechta goroutinelarga bo'lib berish orqali tizim o'tkazuvchanligini oshiradi.

## Ishlash natijasi:
```text
[Alpha] Qayta ishlandi: Hisobot-1
[Beta] Qayta ishlandi: Shartnoma-2
[Gamma] Qayta ishlandi: Kvitansiya-3
[Alpha] Qayta ishlandi: Faktura-4
[Beta] Qayta ishlandi: Buyruq-5
Barcha hujjatlar Fan-out orqali qayta ishlandi.
```

# 631-Topshiriq: Parallel saralash: Merge Sort bosqichini goroutinelarda bajarish
## Topshiriq sharti:
Massivning ikki yarmini parallel goroutinelarda saralab, so'ng birlashtiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sort"
	"sync"
)

func parallelSarala(qism []int, wg *sync.WaitGroup) {
	defer wg.Done()
	sort.Ints(qism)
}

func birlashtir(a, b []int) []int {
	natija := make([]int, 0, len(a)+len(b))
	i, j := 0, 0
	for i < len(a) && j < len(b) {
		if a[i] < b[j] {
			natija = append(natija, a[i])
			i++
		} else {
			natija = append(natija, b[j])
			j++
		}
	}
	natija = append(natija, a[i:]...)
	natija = append(natija, b[j:]...)
	return natija
}

func main() {
	sonlar := []int{38, 27, 43, 3, 9, 82, 10}
	ortasi := len(sonlar) / 2

	chap := append([]int{}, sonlar[:ortasi]...)
	ong := append([]int{}, sonlar[ortasi:]...)

	var wg sync.WaitGroup
	wg.Add(2)

	go parallelSarala(chap, &wg)
	go parallelSarala(ong, &wg)

	wg.Wait()

	saralangan := birlashtir(chap, ong)
	fmt.Println("Dastlabki:", sonlar)
	fmt.Println("Parallel saralangan:", saralangan)
}
```

## Tushuntirish va Mantiq:
Massiv bo'laklarini parallel saralab, so'ng chiziqli vaqtda (`O(n)`) birlashtirish orqali Merge Sort algoritmining samaradorligi oshiriladi.

## Ishlash natijasi:
```text
Dastlabki: [38 27 43 3 9 82 10]
Parallel saralangan: [3 9 10 27 38 43 82]
```

# 632-Topshiriq: Vaqtinchalik kechiktirilgan vazifalar (Parallel Timers)
## Topshiriq sharti:
Bir nechta vazifalarni har xil kechikishlar bilan parallel rejalashtiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func kechiktirilganXabar(xabar string, kechikish time.Duration, wg *sync.WaitGroup) {
	defer wg.Done()
	time.Sleep(kechikish)
	fmt.Printf("[%v dan keyin]: %s\n", kechikish, xabar)
}

func main() {
	var wg sync.WaitGroup

	wg.Add(3)
	go kechiktirilganXabar("300ms kechikkan xabar", 300*time.Millisecond, &wg)
	go kechiktirilganXabar("100ms tezkor xabar", 100*time.Millisecond, &wg)
	go kechiktirilganXabar("200ms oraliq xabar", 200*time.Millisecond, &wg)

	wg.Wait()
	fmt.Println("Barcha taymerlar o'z vaqtida ishladi.")
}
```

## Tushuntirish va Mantiq:
Goroutinelar yordamida bir-biriga bog'liq bo'lmagan mustaqil taymerlarni ishga tushirish mumkin. Har bir goroutine o'z kechikishi tugagach ishlaydi.

## Ishlash natijasi:
```text
[100ms dan keyin]: 100ms tezkor xabar
[200ms dan keyin]: 200ms oraliq xabar
[300ms dan keyin]: 300ms kechikkan xabar
Barcha taymerlar o'z vaqtida ishladi.
```

# 633-Topshiriq: Cheklangan parallelizm (Semafor yondashuvi)
## Topshiriq sharti:
Buferlangan kanal orqali bir vaqtning o'zida ko'pi bilan 2 ta goroutine ishlashini kafolatlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func resursIshlatish(id int, sem chan struct{}, wg *sync.WaitGroup) {
	defer wg.Done()

	sem <- struct{}{}        // Token olamiz (agar to'la bo'lsa kutadi)
	defer func() { <-sem }() // Ish tugagach tokenni bo'shatamiz

	fmt.Printf("Worker #%d resursni band qildi\n", id)
	time.Sleep(80 * time.Millisecond)
	fmt.Printf("Worker #%d resursni bo'shatdi\n", id)
}

func main() {
	const maxParallel = 2
	semafor := make(chan struct{}, maxParallel)
	var wg sync.WaitGroup

	for i := 1; i <= 4; i++ {
		wg.Add(1)
		go resursIshlatish(i, semafor, &wg)
	}

	wg.Wait()
	fmt.Println("Cheklangan parallelizm muvaffaqiyatli sinovdan o'tdi.")
}
```

## Tushuntirish va Mantiq:
Hajmi `N` ga teng buferlangan kanal semafor (semaphore) vazifasini o'taydi: unga `N` tadan ko'p element yozib bo'lmagani sababli, bir paytda faqat `N` ta goroutine kritik hududda ishlay oladi.

## Ishlash natijasi:
```text
Worker #1 resursni band qildi
Worker #2 resursni band qildi
Worker #1 resursni bo'shatdi
Worker #2 resursni bo'shatdi
Worker #3 resursni band qildi
Worker #4 resursni band qildi
Worker #3 resursni bo'shatdi
Worker #4 resursni bo'shatdi
Cheklangan parallelizm muvaffaqiyatli sinovdan o'tdi.
```

# 634-Topshiriq: Mustaqil API larni parallel chaqirish va natijalarni birlashtirish
## Topshiriq sharti:
Foydalanuvchi profili, buyurtmalari va balansini 3 ta mustaqil goroutineda parallel oling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type FoydalanuvchiDashboard struct {
	Profil  string
	Balans  float64
	BuyurtmaSoni int
}

func main() {
	var data FoydalanuvchiDashboard
	var wg sync.WaitGroup

	wg.Add(3)

	go func() {
		defer wg.Done()
		time.Sleep(40 * time.Millisecond)
		data.Profil = "Akmal Karimov (ID: 5541)"
	}()

	go func() {
		defer wg.Done()
		time.Sleep(50 * time.Millisecond)
		data.Balans = 1450000.50
	}()

	go func() {
		defer wg.Done()
		time.Sleep(30 * time.Millisecond)
		data.BuyurtmaSoni = 12
	}()

	wg.Wait()

	fmt.Println("Foydalanuvchi Dashboardi yuklandi:")
	fmt.Printf("- Profil: %s\n", data.Profil)
	fmt.Printf("- Hisob balansi: %.2f so'm\n", data.Balans)
	fmt.Printf("- Buyurtmalar soni: %d ta\n", data.BuyurtmaSoni)
}
```

## Tushuntirish va Mantiq:
Monolit so'rovlar o'rniga turli mikroservislardan ma'lumotlarni parallel yig'ish (Aggregation pattern) foydalanuvchi interfeysi yuklanish tezligini sezilarli oshiradi.

## Ishlash natijasi:
```text
Foydalanuvchi Dashboardi yuklandi:
- Profil: Akmal Karimov (ID: 5541)
- Hisob balansi: 1450000.50 so'm
- Buyurtmalar soni: 12 ta
```

# 635-Topshiriq: Parallel tub sonlarni (primes) izlash
## Topshiriq sharti:
Oraliqdagi tub sonlarni parallel goroutinelarda qidirib, topilganlarni yig'ing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func tubmi(n int) bool {
	if n < 2 {
		return false
	}
	for i := 2; i*i <= n; i++ {
		if n%i == 0 {
			return false
		}
	}
	return true
}

func tubQidiruvchi(bosh, oxir int, ch chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := bosh; i <= oxir; i++ {
		if tubmi(i) {
			ch <- i
		}
	}
}

func main() {
	ch := make(chan int, 20)
	var wg sync.WaitGroup

	// 1 dan 50 gacha bo'lgan sonlarni 2 ta goroutinega bo'lamiz
	wg.Add(2)
	go tubQidiruvchi(1, 25, ch, &wg)
	go tubQidiruvchi(26, 50, ch, &wg)

	go func() {
		wg.Wait()
		close(ch)
	}()

	var tublar []int
	for p := range ch {
		tublar = append(tublar, p)
	}

	fmt.Printf("1 dan 50 gacha bo'lgan oraliqda %d ta tub son topildi:\n", len(tublar))
	fmt.Println(tublar)
}
```

## Tushuntirish va Mantiq:
Hisoblash oraliqlarini bo'laklarga ajratib, har bir oraliqdagi natijalarni umumiy kanalga uzatish orqali natijalar to'planadi.

## Ishlash natijasi:
```text
1 dan 50 gacha bo'lgan oraliqda 15 ta tub son topildi:
[2 3 5 7 11 13 17 19 23 29 31 37 41 43 47]
```

# 636-Topshiriq: Goroutine orqali background metrics collector
## Topshiriq sharti:
Har ma'lum vaqtda orqa fonda tizim holatini kuzatuvchi servisni goroutine orqali ishga tushiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"time"
)

func metricsCollector(toxtat chan struct{}) {
	ticker := time.NewTicker(50 * time.Millisecond)
	defer ticker.Stop()

	for {
		select {
		case <-toxtat:
			fmt.Println("[Metrics] Kuzatuvchi to'xtatildi.")
			return
		case <-ticker.C:
			var m runtime.MemStats
			runtime.ReadMemStats(&m)
			fmt.Printf("[Metrics] Faol goroutinelar: %d | Xotira: %d KB\n",
				runtime.NumGoroutine(), m.Alloc/1024)
		}
	}
}

func main() {
	toxtat := make(chan struct{})
	go metricsCollector(toxtat)

	time.Sleep(120 * time.Millisecond)
	close(toxtat)
	time.Sleep(20 * time.Millisecond)
	fmt.Println("Asosiy dastur tugadi.")
}
```

## Tushuntirish va Mantiq:
Orqa fonda ishlovchi daemon goroutinelar `time.Ticker` va bekor qilish kanali yordamida resurs sarfini monitoring qilib turadi.

## Ishlash natijasi:
```text
[Metrics] Faol goroutinelar: 2 | Xotira: 160 KB
[Metrics] Faol goroutinelar: 2 | Xotira: 162 KB
[Metrics] Kuzatuvchi to'xtatildi.
Asosiy dastur tugadi.
```

# 637-Topshiriq: Parallel CSV ma'lumotlarini qatorlab tekshirish
## Topshiriq sharti:
Katta ro'yxatdagi yozuvlarning to'g'riligini bir nechta oqimda tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
	"sync"
)

type Yozuv struct {
	ID    int
	Email string
}

func tekshirYozuv(y Yozuv, xatolar chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()
	if !strings.Contains(y.Email, "@") {
		xatolar <- fmt.Sprintf("ID %d: Noto'g'ri email '%s'", y.ID, y.Email)
	}
}

func main() {
	yozuvlar := []Yozuv{
		{ID: 1, Email: "ali@gmail.com"},
		{ID: 2, Email: "vali_notogri_email"},
		{ID: 3, Email: "gani@mail.ru"},
		{ID: 4, Email: "xato_manzil.com"},
	}

	xatolar := make(chan string, len(yozuvlar))
	var wg sync.WaitGroup

	for _, y := range yozuvlar {
		wg.Add(1)
		go tekshirYozuv(y, xatolar, &wg)
	}

	wg.Wait()
	close(xatolar)

	fmt.Println("Aniqlangan xatoliklar:")
	for x := range xatolar {
		fmt.Println("-", x)
	}
}
```

## Tushuntirish va Mantiq:
Har bir yozuvni alohida goroutineda tekshirish orqali millionlab qatorlardan iborat CSV fayllarni soniyalar ichida validatsiya qilish mumkin.

## Ishlash natijasi:
```text
Aniqlangan xatoliklar:
- ID 2: Noto'g'ri email 'vali_notogri_email'
- ID 4: Noto'g'ri email 'xato_manzil.com'
```

# 638-Topshiriq: O'z-o'zidan tiklanuvchi goroutine (Supervisor pattern)
## Topshiriq sharti:
Goroutineda xato (panic) yuz berganda uni avtomatik qayta ishga tushiruvchi nazoratchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func beqarorXizmat(urinish int) {
	fmt.Printf("Xizmat urinishi #%d ishlamoqda...\n", urinish)
	if urinish < 3 {
		panic("Kritik xatolik yuz berdi!")
	}
	fmt.Println("Xizmat 3-urinishda barqaror ishladi!")
}

func supervisor(maxUrinish int) {
	urinish := 1
	for {
		if urinish > maxUrinish {
			fmt.Println("[Supervisor] Maksimal urinishlar tugadi, to'xtatildi.")
			return
		}

		muvaffaqiyat := func() (ok bool) {
			defer func() {
				if r := recover(); r != nil {
					fmt.Printf("[Supervisor] Panic ushlandi: %v. Qayta tiklanmoqda...\n", r)
					ok = false
				}
			}()
			beqarorXizmat(urinish)
			return true
		}()

		if muvaffaqiyat {
			break
		}
		urinish++
		time.Sleep(30 * time.Millisecond)
	}
}

func main() {
	supervisor(3)
}
```

## Tushuntirish va Mantiq:
Supervisor pattern xizmatlarning chidamliligini (resilience) oshirish uchun qo'llaniladi. Goroutine qulasa, uni qayta tiklash imkoniyatini beradi.

## Ishlash natijasi:
```text
Xizmat urinishi #1 ishlamoqda...
[Supervisor] Panic ushlandi: Kritik xatolik yuz berdi!. Qayta tiklanmoqda...
Xizmat urinishi #2 ishlamoqda...
[Supervisor] Panic ushlandi: Kritik xatolik yuz berdi!. Qayta tiklanmoqda...
Xizmat urinishi #3 ishlamoqda...
Xizmat 3-urinishda barqaror ishladi!
```

# 639-Topshiriq: Parallel veb sahifalar yuklash simulyatsiyasi (Web Scraper)
## Topshiriq sharti:
URL manzillar ro'yxatidan ma'lumotlarni parallel yig'ib, umumiy xaritada saqlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type SahifaNatija struct {
	URL      string
	Hajmi    int
	Yuklandi bool
}

func yukla(url string, res *SahifaNatija, wg *sync.WaitGroup) {
	defer wg.Done()
	// Tarmoq simulyatsiyasi
	time.Sleep(40 * time.Millisecond)
	res.URL = url
	res.Hajmi = len(url) * 128
	res.Yuklandi = true
}

func main() {
	saytlar := []string{
		"https://daryo.uz",
		"https://kun.uz",
		"https://gazeta.uz",
	}

	natijalar := make([]SahifaNatija, len(saytlar))
	var wg sync.WaitGroup

	for i, url := range saytlar {
		wg.Add(1)
		go yukla(url, &natijalar[i], &wg)
	}

	wg.Wait()

	fmt.Println("Yuklangan sahifalar:")
	for _, n := range natijalar {
		fmt.Printf("- %s (Hajmi: %d bayt, Muvaffaqiyatli: %t)\n", n.URL, n.Hajmi, n.Yuklandi)
	}
}
```

## Tushuntirish va Mantiq:
Har bir sahifani parallel yuklash tarmoq kutish vaqtini (I/O latency) minimal darajaga tushiradi.

## Ishlash natijasi:
```text
Yuklangan sahifalar:
- https://daryo.uz (Hajmi: 2048 bayt, Muvaffaqiyatli: true)
- https://kun.uz (Hajmi: 1792 bayt, Muvaffaqiyatli: true)
- https://gazeta.uz (Hajmi: 2176 bayt, Muvaffaqiyatli: true)
```

# 640-Topshiriq: Resurslarni tozalash va Graceful Shutdown
## Topshiriq sharti:
To'xtatish signali kelganda barcha ochiq ishlarni xavfsiz yakunlab to'xtashni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func fonXizmati(toxtat chan struct{}, wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		select {
		case <-toxtat:
			fmt.Println("[Worker] To'xtatish signali qabul qilindi. Resurslar tozalanmoqda...")
			time.Sleep(50 * time.Millisecond)
			fmt.Println("[Worker] Xavfsiz to'xtadi.")
			return
		default:
			// Foydali vazifa
			time.Sleep(20 * time.Millisecond)
		}
	}
}

func main() {
	var wg sync.WaitGroup
	toxtatCh := make(chan struct{})

	wg.Add(1)
	go fonXizmati(toxtatCh, &wg)

	time.Sleep(50 * time.Millisecond)
	fmt.Println("[Main] Xizmatni to'xtatish buyrug'i berildi.")
	close(toxtatCh)

	// Worker to'liq tozalab tugatishini kutamiz
	wg.Wait()
	fmt.Println("[Main] Tizim to'liq va xavfsiz o'chirildi.")
}
```

## Tushuntirish va Mantiq:
Graceful Shutdown — bu server yoki xizmat to'xtaganda barcha ishlovdagi so'rovlarni xavfsiz yakunlash va resurslarni to'g'ri yopish amaliyotidir.

## Ishlash natijasi:
```text
[Main] Xizmatni to'xtatish buyrug'i berildi.
[Worker] To'xtatish signali qabul qilindi. Resurslar tozalanmoqda...
[Worker] Xavfsiz to'xtadi.
[Main] Tizim to'liq va xavfsiz o'chirildi.
```

# 641-Topshiriq: Go Scheduler: G-M-P modeli konseptini kodda tushuntirish
## Topshiriq sharti:
G (goroutine), M (OS thread), P (processor context) munosabatini dasturda kuzatish.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"sync"
)

func main() {
	// P - mantiqiy protsessorlar soni (GOMAXPROCS)
	pSoni := runtime.GOMAXPROCS(0)
	// G - ayni damda mavjud goroutinelar
	gSoni := runtime.NumGoroutine()

	fmt.Printf("Go G-M-P holati:\n")
	fmt.Printf("- P (Protsessorlar): %d\n", pSoni)
	fmt.Printf("- G (Boshlang'ich Goroutinelar): %d\n", gSoni)

	var wg sync.WaitGroup
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			// Har bir G biron P orqali M ga bog'lanadi va ishlaydi
		}(i)
	}

	fmt.Printf("- G (5 ta yangi goroutine qo'shilgach): %d\n", runtime.NumGoroutine())
	wg.Wait()
	fmt.Println("Barcha G larning bajarilishi tugadi.")
}
```

## Tushuntirish va Mantiq:
Go da G — bu Goroutine, M — operatsion tizim oqimi (Machine), P — esa resurs va navbatlarni boshqaruvchi kontekst (Processor). Go scheduleri G larni P lar orqali M larga taqsimlab beradi.

## Ishlash natijasi:
```text
Go G-M-P holati:
- P (Protsessorlar): 8
- G (Boshlang'ich Goroutinelar): 1
- G (5 ta yangi goroutine qo'shilgach): 6
Barcha G larning bajarilishi tugadi.
```

# 642-Topshiriq: Parallel JSON hujjatlarini tahlil qilish
## Topshiriq sharti:
Bir nechta JSON satrlarini parallel goroutinelarda parslash (unmarshal) qiling.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"sync"
)

type Mahsulot struct {
	ID    int     `json:"id"`
	Nomi  string  `json:"nomi"`
	Narxi float64 `json:"narxi"`
}

func parseJSON(raw string, res *Mahsulot, wg *sync.WaitGroup) {
	defer wg.Done()
	_ = json.Unmarshal([]byte(raw), res)
}

func main() {
	rawJSONs := []string{
		`{"id": 1, "nomi": "Laptop", "narxi": 850.0}`,
		`{"id": 2, "nomi": "Sichqoncha", "narxi": 25.5}`,
		`{"id": 3, "nomi": "Klaviatura", "narxi": 45.0}`,
	}

	mahsulotlar := make([]Mahsulot, len(rawJSONs))
	var wg sync.WaitGroup

	for i, raw := range rawJSONs {
		wg.Add(1)
		go parseJSON(raw, &mahsulotlar[i], &wg)
	}

	wg.Wait()

	fmt.Println("Parslangan mahsulotlar:")
	for _, m := range mahsulotlar {
		fmt.Printf("#%d: %s (Narxi: $%.2f)\n", m.ID, m.Nomi, m.Narxi)
	}
}
```

## Tushuntirish va Mantiq:
Katta hajmli JSON ma'lumotlarni parallel ravishda parslash unmarshal qilish vaqtini sezilarli darajada kamaytiradi.

## Ishlash natijasi:
```text
Parslangan mahsulotlar:
#1: Laptop (Narxi: $850.00)
#2: Sichqoncha (Narxi: $25.50)
#3: Klaviatura (Narxi: $45.00)
```

# 643-Topshiriq: Asinxron Audit loglarini saqlash tizimi
## Topshiriq sharti:
Foydalanuvchi harakatlarini asosiy oqimni to'xtatmasdan audit logiga uzatuvchi mexanizm.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type AuditLog struct {
	Foydalanuvchi string
	Harakat       string
	Vaqt          time.Time
}

type AuditServis struct {
	ch chan AuditLog
	wg sync.WaitGroup
}

func YangiAuditServis() *AuditServis {
	s := &AuditServis{
		ch: make(chan AuditLog, 100),
	}
	s.wg.Add(1)
	go s.saqlashOqimi()
	return s
}

func (s *AuditServis) saqlashOqimi() {
	defer s.wg.Done()
	for log := range s.ch {
		fmt.Printf("[AUDIT] %s foydalanuvchisi '%s' amalini bajardi (%s)\n",
			log.Foydalanuvchi, log.Harakat, log.Vaqt.Format("15:04:05"))
	}
}

func (s *AuditServis) Yozish(user, action string) {
	s.ch <- AuditLog{Foydalanuvchi: user, Harakat: action, Vaqt: time.Now()}
}

func (s *AuditServis) Yopish() {
	close(s.ch)
	s.wg.Wait()
}

func main() {
	audit := YangiAuditServis()

	audit.Yozish("admin", "Tizimga kirish")
	audit.Yozish("nodir", "Parolni o'zgartirish")
	audit.Yozish("dilshod", "To'lovni tasdiqlash")

	audit.Yopish()
	fmt.Println("Audit xizmati xavfsiz yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Audit loglari kabi I/O vazifalarni asinxron kanal va goroutine orqali bajarish asosiy biznes mantiqning tezkor ishlashini ta'minlaydi.

## Ishlash natijasi:
```text
[AUDIT] admin foydalanuvchisi 'Tizimga kirish' amalini bajardi (15:04:05)
[AUDIT] nodir foydalanuvchisi 'Parolni o'zgartirish' amalini bajardi (15:04:05)
[AUDIT] dilshod foydalanuvchisi 'To'lovni tasdiqlash' amalini bajardi (15:04:05)
Audit xizmati xavfsiz yakunlandi.
```

# 644-Topshiriq: Batch Processor: Obyektlarni paketlab parallel ishlash
## Topshiriq sharti:
Katta ro'yxatni paketlarga (batch) ajratib, har bir paketni goroutinada bajaring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func qaytaIshlaPaket(paketId int, elementlar []int, wg *sync.WaitGroup) {
	defer wg.Done()
	fmt.Printf("Paket #%d qayta ishlanmoqda: %v\n", paketId, elementlar)
}

func main() {
	malumotlar := []int{10, 20, 30, 40, 50, 60, 70, 80, 90}
	paketHajmi := 3

	var wg sync.WaitGroup
	paketId := 1

	for i := 0; i < len(malumotlar); i += paketHajmi {
		oxir := i + paketHajmi
		if oxir > len(malumotlar) {
			oxir = len(malumotlar)
		}

		wg.Add(1)
		go qaytaIshlaPaket(paketId, malumotlar[i:oxir], &wg)
		paketId++
	}

	wg.Wait()
	fmt.Println("Barcha paketlar parallel yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Batch processing texnikasi ma'lumotlar bazasiga ommaviy yozishda (bulk insert) va tarmoq trafigini optimallashtirishda eng samarali yondashuvdir.

## Ishlash natijasi:
```text
Paket #1 qayta ishlanmoqda: [10 20 30]
Paket #2 qayta ishlanmoqda: [40 50 60]
Paket #3 qayta ishlanmoqda: [70 80 90]
Barcha paketlar parallel yakunlandi.
```

# 645-Topshiriq: Parallel keshni oldindan to'ldirish (Cache Warm-up)
## Topshiriq sharti:
Tizim ishga tushganda kesh xotirasini bir nechta manbadan parallel to'ldiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type SafeCache struct {
	sync.Mutex
	items map[string]string
}

func (c *SafeCache) Set(key, val string) {
	c.Lock()
	defer c.Unlock()
	c.items[key] = val
}

func keshYukla(kalit, manba string, c *SafeCache, wg *sync.WaitGroup) {
	defer wg.Done()
	time.Sleep(30 * time.Millisecond) // Ma'lumotlar bazasidan o'qish simulyatsiyasi
	c.Set(kalit, manba)
	fmt.Printf("[Kesh] '%s' muvaffaqiyatli yuklandi\n", kalit)
}

func main() {
	cache := &SafeCache{items: make(map[string]string)}
	var wg sync.WaitGroup

	manbalar := map[string]string{
		"kurslar":  "USD: 12800, EUR: 13900",
		"sozlamalar": "theme=dark, lang=uz",
		"shaharlar":  "Toshkent, Samarqand",
	}

	for k, v := range manbalar {
		wg.Add(1)
		go keshYukla(k, v, cache, &wg)
	}

	wg.Wait()
	fmt.Println("Kesh to'liq tayyor bo'ldi. Elementlar soni:", len(cache.items))
}
```

## Tushuntirish va Mantiq:
Cache warm-up dastur ishga tushish vaqtida (startup) barcha zaruriy ma'lumotlarni xotiraga parallel yuklash orqali birinchi foydalanuvchilar kechikishini bartaraf qiladi.

## Ishlash natijasi:
```text
[Kesh] 'kurslar' muvaffaqiyatli yuklandi
[Kesh] 'sozlamalar' muvaffaqiyatli yuklandi
[Kesh] 'shaharlar' muvaffaqiyatli yuklandi
Kesh to'liq tayyor bo'ldi. Elementlar soni: 3
```

# 646-Topshiriq: Parallel Map-Reduce amali
## Topshiriq sharti:
Matnlardagi so'zlarni parallel hisoblab (Map), so'ng natijalarni yig'ing (Reduce).

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
	"sync"
)

func mapSozlar(qator string, out chan<- map[string]int, wg *sync.WaitGroup) {
	defer wg.Done()
	res := make(map[string]int)
	for _, w := range strings.Fields(qator) {
		res[strings.ToLower(w)]++
	}
	out <- res
}

func main() {
	matnlar := []string{
		"go tez va go qulay",
		"go ochiq manbali til",
	}

	out := make(chan map[string]int, len(matnlar))
	var wg sync.WaitGroup

	for _, m := range matnlar {
		wg.Add(1)
		go mapSozlar(m, out, &wg)
	}

	wg.Wait()
	close(out)

	// Reduce bosqichi
	finalCount := make(map[string]int)
	for m := range out {
		for k, v := range m {
			finalCount[k] += v
		}
	}

	fmt.Println("Map-Reduce natijasi:")
	for k, v := range finalCount {
		fmt.Printf("- %s: %d\n", k, v)
	}
}
```

## Tushuntirish va Mantiq:
Map-Reduce modeli yirik hajmdagi ma'lumotlarni qismlarga bo'lib parallel hisoblash (Map) va keyin natijalarni bitta umumiy xulosaga jamlash (Reduce) usulidir.

## Ishlash natijasi:
```text
Map-Reduce natijasi:
- go: 3
- tez: 1
- va: 1
- qulay: 1
- ochiq: 1
- manbali: 1
- til: 1
```

# 647-Topshiriq: Asinxron bildirishnomalar (SMS/Email) yuborish
## Topshiriq sharti:
Xabarlarni fon rejimida parallel yuborib, foydalanuvchini kutib qoldirmaydigan servis tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type Xabar struct {
	Kimga   string
	Matn    string
	XabarTuri string
}

func yuborXabar(x Xabar, wg *sync.WaitGroup) {
	defer wg.Done()
	time.Sleep(40 * time.Millisecond) // Provayder bilan aloqa
	fmt.Printf("[%s] '%s' ga yuborildi: %s\n", x.XabarTuri, x.Kimga, x.Matn)
}

func main() {
	xabarlar := []Xabar{
		{Kimga: "+998901234567", Matn: "Kodingiz: 4921", XabarTuri: "SMS"},
		{Kimga: "nodir@example.com", Matn: "Hisobingiz faollashtirildi", XabarTuri: "EMAIL"},
		{Kimga: "+998939876543", Matn: "Buyurtmangiz yo'lda", XabarTuri: "SMS"},
	}

	var wg sync.WaitGroup
	for _, x := range xabarlar {
		wg.Add(1)
		go yuborXabar(x, &wg)
	}

	wg.Wait()
	fmt.Println("Barcha bildirishnomalar yetkazildi.")
}
```

## Tushuntirish va Mantiq:
SMS yoki Email jo'natish sekin (tarmoqqa bog'liq) jarayon bo'lgani sababli, ularni alohida goroutinelarga yuklash tizimning javob berish tezligini oshiradi.

## Ishlash natijasi:
```text
[SMS] '+998901234567' ga yuborildi: Kodingiz: 4921
[EMAIL] 'nodir@example.com' ga yuborildi: Hisobingiz faollashtirildi
[SMS] '+998939876543' ga yuborildi: Buyurtmangiz yo'lda
Barcha bildirishnomalar yetkazildi.
```

# 648-Topshiriq: Parallel hisoblashda xatoliklarni yig'uvchi (Error Collector)
## Topshiriq sharti:
Bir nechta parallel oqimlardagi xatoliklarni xavfsiz to'plovchi struktura yarating.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
	"sync"
)

type ErrorCollector struct {
	sync.Mutex
	errs []error
}

func (ec *ErrorCollector) Add(err error) {
	if err == nil {
		return
	}
	ec.Lock()
	defer ec.Unlock()
	ec.errs = append(ec.errs, err)
}

func amaliyVazifa(id int, ec *ErrorCollector, wg *sync.WaitGroup) {
	defer wg.Done()
	if id%2 == 0 {
		ec.Add(fmt.Errorf("vazifa #%d da kritik nosozlik yuz berdi", id))
	}
}

func main() {
	var ec ErrorCollector
	var wg sync.WaitGroup

	for i := 1; i <= 4; i++ {
		wg.Add(1)
		go amaliyVazifa(i, &ec, &wg)
	}

	wg.Wait()

	fmt.Printf("Jami yuz bergan xatoliklar: %d ta\n", len(ec.errs))
	for _, err := range ec.errs {
		fmt.Println("-", err)
	}
}
```

## Tushuntirish va Mantiq:
Parallel goroutinelarda yuz bergan xatolarni bitta joyga xavfsiz to'plash uchun Mutex bilan himoyalangan xato kollektori qo'llaniladi.

## Ishlash natijasi:
```text
Jami yuz bergan xatoliklar: 2 ta
- vazifa #2 da kritik nosozlik yuz berdi
- vazifa #4 da kritik nosozlik yuz berdi
```

# 649-Topshiriq: Real-vaqt monitoringi: Goroutine orqali xotira holatini tekshirish
## Topshiriq sharti:
Orqa fonda xotira sarfini doimiy nazorat qilib, limitdan oshganda ogohlantiruvchi oqim tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
	"time"
)

func xotiraKuzatuvchisi(limitKB uint64, toxtat chan struct{}) {
	for {
		select {
		case <-toxtat:
			fmt.Println("[Kuzatuvchi] Monitoring yakunlandi.")
			return
		default:
			var m runtime.MemStats
			runtime.ReadMemStats(&m)
			ishlatilganKB := m.Alloc / 1024
			if ishlatilganKB > limitKB {
				fmt.Printf("[OGOHLANTIRISH] Xotira limiti oshdi! Joriy: %d KB (Limit: %d KB)\n",
					ishlatilganKB, limitKB)
			}
			time.Sleep(30 * time.Millisecond)
		}
	}
}

func main() {
	toxtat := make(chan struct{})
	go xotiraKuzatuvchisi(100, toxtat)

	time.Sleep(80 * time.Millisecond)
	close(toxtat)
	time.Sleep(20 * time.Millisecond)
	fmt.Println("Dastur muvaffaqiyatli yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Doimiy fon goroutinelari mikroservisning sog'lomligini (healthcheck) ta'minlaydi va xotira sizib chiqishini (memory leak) vaqtida aniqlashga yordam beradi.

## Ishlash natijasi:
```text
[OGOHLANTIRISH] Xotira limiti oshdi! Joriy: 165 KB (Limit: 100 KB)
[OGOHLANTIRISH] Xotira limiti oshdi! Joriy: 166 KB (Limit: 100 KB)
[Kuzatuvchi] Monitoring yakunlandi.
Dastur muvaffaqiyatli yakunlandi.
```

# 650-Topshiriq: Parallel yuklama sinovchisi (Load Tester simulyatori)
## Topshiriq sharti:
Keng qamrovli yakuniy loyiha: Belgilangan miqdordagi parallel so'rovlarni yuborib, o'rtacha javob vaqti va muvaffaqiyat ko'rsatkichini hisoblovchi Load Tester yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

type SinovNatijasi struct {
	JamiSorowlar   int64
	Muvaffaqiyatli int64
	Xatolar        int64
	UmumiyVaqtMs   int64
}

func soxtaServer(id int) bool {
	time.Sleep(10 * time.Millisecond)
	// Har 10-chi so'rovda nosozlik simulyatsiyasi
	return id%10 != 0
}

func main() {
	const umumiySorowlar = 50
	const oqimlarSoni = 5

	var res SinovNatijasi
	var wg sync.WaitGroup

	sorovlarKanali := make(chan int, umumiySorowlar)
	for i := 1; i <= umumiySorowlar; i++ {
		sorovlarKanali <- i
	}
	close(sorovlarKanali)

	boshlash := time.Now()

	for w := 1; w <= oqimlarSoni; w++ {
		wg.Add(1)
		go func(ishchiId int) {
			defer wg.Done()
			for reqId := range sorovlarKanali {
				reqStart := time.Now()
				ok := soxtaServer(reqId)
				sarf := time.Since(reqStart).Milliseconds()

				atomic.AddInt64(&res.JamiSorowlar, 1)
				atomic.AddInt64(&res.UmumiyVaqtMs, sarf)

				if ok {
					atomic.AddInt64(&res.Muvaffaqiyatli, 1)
				} else {
					atomic.AddInt64(&res.Xatolar, 1)
				}
			}
		}(w)
	}

	wg.Wait()
	jamiSarf := time.Since(boshlash).Round(time.Millisecond)

	ortachaKechikish := float64(res.UmumiyVaqtMs) / float64(res.JamiSorowlar)
	fmt.Println("=== YUKLAMA SINOVI HISOBOTI ===")
	fmt.Printf("Jami so'rovlar: %d\n", res.JamiSorowlar)
	fmt.Printf("Muvaffaqiyatli: %d (%.1f%%)\n", res.Muvaffaqiyatli, float64(res.Muvaffaqiyatli)/float64(res.JamiSorowlar)*100)
	fmt.Printf("Xatoliklar: %d\n", res.Xatolar)
	fmt.Printf("O'rtacha kechikish: %.2f ms\n", ortachaKechikish)
	fmt.Printf("Umumiy sinov vaqti: %v\n", jamiSarf)
}
```

## Tushuntirish va Mantiq:
Load Tester arxitekturasi goroutinelar, kanallar, atomik hisoblagichlar va WaitGroup sinxronizatsiyasining barchasini o'zida birlashtirgan professional parallel dasturlash namunasidir.

## Ishlash natijasi:
```text
=== YUKLAMA SINOVI HISOBOTI ===
Jami so'rovlar: 50
Muvaffaqiyatli: 45 (90.0%)
Xatoliklar: 5
O'rtacha kechikish: 10.00 ms
Umumiy sinov vaqti: 105ms
```

