# 4-Mavzu: Funksiyalar va defer Konstruksiyasi (151-200)

Go dasturlash tilida funksiyalar birinchi darajali fuqarolardir (first-class citizens). Ko'p qiymat qaytarish, nomlangan natijalar, o'zgaruvchan parametrlar (variadic), anonim funksiyalar va yopilishlar (closures), `defer` ning LIFO stak mexanizmi, argumentlarning erta hisoblanishi, `panic` va `recover` orqali favqulodda vaziyatlarni boshqarish hamda rekursiya bo'yicha 50 ta amaliy topshiriq.

# 151-Topshiriq: Funksiya e'lon qilish va chaqirish asoslari
## Topshiriq sharti:
Ikkita sonni qo'shib natijani qaytaruvchi oddiy `qoshish` funksiyasini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func qoshish(a int, b int) int {
	return a + b
}

func main() {
	natija := qoshish(15, 25)
	fmt.Println("15 + 25 =", natija)
}
```

## Tushuntirish va Mantiq:
Go tilida funksiya `func nom(parametrlar) qaytish_turi` sintaksisi bilan e'lon qilinadi va `return` orqali natija qaytaradi.

## Ishlash natijasi:
```text
15 + 25 = 40
```

# 152-Topshiriq: Bir xil turdagi parametrlarni qisqartirib yozish
## Topshiriq sharti:
Bir nechta bir xil turdagi parametrlarning turini eng oxirida bir marta ko'rsatuvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func kopaytirishUchta(x, y, z int) int {
	return x * y * z
}

func main() {
	fmt.Println("2 * 3 * 4 =", kopaytirishUchta(2, 3, 4))
}
```

## Tushuntirish va Mantiq:
Parametrlar ketma-ket bir xil turda bo'lsa, `x int, y int, z int` o'rniga `x, y, z int` deb qisqartirish mumkin.

## Ishlash natijasi:
```text
2 * 3 * 4 = 24
```

# 153-Topshiriq: Ko'p qiymat qaytaruvchi funksiya (Multiple Return Values)
## Topshiriq sharti:
Sonni bo'lish natijasini va qoldig'ini bir vaqtning o'zida qaytaruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func bolishVaQoldiq(a, b int) (int, int) {
	bolinma := a / b
	qoldiq := a % b
	return bolinma, qoldiq
}

func main() {
	bol, qol := bolishVaQoldiq(27, 4)
	fmt.Printf("27 / 4 = %d (qoldiq: %d)\n", bol, qol)
}
```

## Tushuntirish va Mantiq:
Go tilida funksiyalar bir vaqtda bir nechta qiymat qaytara oladi: `(tur1, tur2)` qavs ichida ko'rsatiladi.

## Ishlash natijasi:
```text
27 / 4 = 6 (qoldiq: 3)
```

# 154-Topshiriq: Nomlangan qaytish qiymatlari (Named Return Values)
## Topshiriq sharti:
Funksiya sarlavhasida qaytish qiymatlariga nom berib, to'rtburchak perimetri va yuzasini hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func tortburchak(boyi, eni float64) (yuza float64, perimetr float64) {
	yuza = boyi * eni
	perimetr = 2 * (boyi + eni)
	return // Naked return
}

func main() {
	y, p := tortburchak(5.0, 3.0)
	fmt.Printf("Yuza: %.1f, Perimetr: %.1f\n", y, p)
}
```

## Tushuntirish va Mantiq:
Qaytish o'zgaruvchilari funksiya boshida avtomatik nol qiymat bilan e'lon qilinadi va `return` deb yozilganda shu nomlar qaytariladi.

## Ishlash natijasi:
```text
Yuza: 15.0, Perimetr: 16.0
```

# 155-Topshiriq: Naked Return va undan ehtiyotkorlik bilan foydalanish
## Topshiriq sharti:
Kichik funksiyalarda naked return qulay bo'lsa-da, katta funksiyalarda o'qilishini qiyinlashtirishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func bolishXavfsiz(a, b float64) (natija float64, ok bool) {
	if b == 0 {
		return // natija=0, ok=false qaytadi
	}
	natija = a / b
	ok = true
	return // ochiq return
}

func main() {
	r1, ok1 := bolishXavfsiz(10, 2)
	fmt.Printf("10 / 2 = %.1f (ok: %t)\n", r1, ok1)

	r2, ok2 := bolishXavfsiz(10, 0)
	fmt.Printf("10 / 0 = %.1f (ok: %t)\n", r2, ok2)
}
```

## Tushuntirish va Mantiq:
Naked return kichik va sodda funksiyalarda kodni qisqartiradi, biroq katta funksiyalarda aniq `return natija, ok` deb yozish tavsiya etiladi.

## Ishlash natijasi:
```text
10 / 2 = 5.0 (ok: true)
10 / 0 = 0.0 (ok: false)
```

# 156-Topshiriq: O'zgaruvchan sondagi parametrlar (Variadic Functions: ...int)
## Topshiriq sharti:
Ixtiyoriy miqdordagi sonlarni qabul qilib, ularning yig'indisini hisoblovchi `yigindi` funksiyasini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func yigindi(sonlar ...int) int {
	jami := 0
	for _, s := range sonlar {
		jami += s
	}
	return jami
}

func main() {
	fmt.Println("Bo'sh chaqiriq:", yigindi())
	fmt.Println("2 ta son:", yigindi(10, 20))
	fmt.Println("5 ta son:", yigindi(1, 2, 3, 4, 5))
}
```

## Tushuntirish va Mantiq:
`...T` sintaksisi funksiya ichida shu turdagi slice (`[]T`) sifatida qabul qilinadi.

## Ishlash natijasi:
```text
Bo'sh chaqiriq: 0
2 ta son: 30
5 ta son: 15
```

# 157-Topshiriq: Sliceni variadic funksiyaga yoyish (Slice Unpacking: nums...)
## Topshiriq sharti:
Mavjud `[]int` sliceni variadic funksiyaga `...` operatori orqali uzating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func engKatta(sonlar ...int) int {
	if len(sonlar) == 0 {
		return 0
	}
	katta := sonlar[0]
	for _, s := range sonlar[1:] {
		if s > katta {
			katta = s
		}
	}
	return katta
}

func main() {
	ro'yxat := []int{12, 45, 78, 23, 89, 5}
	maxSon := engKatta(ro'yxat...) // Sliceni yoyib uzatish

	fmt.Printf("Massiv %v ichidan eng kattasi: %d\n", ro'yxat, maxSon)
}
```

## Tushuntirish va Mantiq:
`slice...` sintaksisi massiv elementlarini alohida argumentlar qatoriga yoyib beradi.

## Ishlash natijasi:
```text
Massiv [12 45 78 23 89 5] ichidan eng kattasi: 89
```

# 158-Topshiriq: Anonim funksiyalar (Anonymous Functions)
## Topshiriq sharti:
Nom berilmagan lokal funksiyani o'zgaruvchiga yuklang va chaqiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	salomBer := func(ism string) string {
		return fmt.Sprintf("Assalomu alaykum, %s!", ism)
	}

	fmt.Println(salomBer("Madina"))
	fmt.Println(salomBer("Bobur"))
}
```

## Tushuntirish va Mantiq:
Anonim funksiyalar boshqa funksiya tanasi ichida yaratilishi va o'zgaruvchilarga o'zlashtirilishi mumkin.

## Ishlash natijasi:
```text
Assalomu alaykum, Madina!
Assalomu alaykum, Bobur!
```

# 159-Topshiriq: Darhol bajariluvchi anonim funksiya (IIFE)
## Topshiriq sharti:
Yaratilgan joyining o'zidayoq chaqiriluvchi IIFE funksiyasidan foydalaning.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	natija := func(a, b int) int {
		return a*a + b*b
	}(3, 4) // E'lon qilingan zahoti chaqiriladi

	fmt.Println("3^2 + 4^2 =", natija)
}
```

## Tushuntirish va Mantiq:
IIFE kod bloklarini izolyatsiya qilish va vaqtinchalik o'zgaruvchilarni global sohaga chiqarmaslik uchun xizmat qiladi.

## Ishlash natijasi:
```text
3^2 + 4^2 = 25
```

# 160-Topshiriq: Yopilishlar (Closures) va tashqi holatni ushlab qolish
## Topshiriq sharti:
Har chaqirilganda 1 taga oshib boruvchi hisoblagich generatori yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func yangiHisoblagich() func() int {
	hisob := 0
	return func() int {
		hisob++
		return hisob
	}
}

func main() {
	h1 := yangiHisoblagich()
	fmt.Println("h1:", h1())
	fmt.Println("h1:", h1())
	fmt.Println("h1:", h1())

	h2 := yangiHisoblagich() // Yangi mustaqil nusxa
	fmt.Println("h2:", h2())
}
```

## Tushuntirish va Mantiq:
Closure funksiyasi o'zining leksik kontekstidagi o'zgaruvchilarni (`hisob`) xotirada saqlab qoladi va ularga murojaat qila oladi.

## Ishlash natijasi:
```text
h1: 1
h1: 2
h1: 3
h2: 1
```

# 161-Topshiriq: Funksiyalar birinchi darajali fuqarolar (First-Class Citizens) sifatida
## Topshiriq sharti:
Matematik amallarni o'zgaruvchilarda saqlang va ularni almashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var amal func(int, int) int

	amal = func(a, b int) int { return a + b }
	fmt.Println("Qo'shish:", amal(10, 5))

	amal = func(a, b int) int { return a * b }
	fmt.Println("Ko'paytirish:", amal(10, 5))
}
```

## Tushuntirish va Mantiq:
Go tilida funksiyalar boshqa har qanday ma'lumot turi (int, string) kabi o'zgaruvchilarga yuklanishi mumkin.

## Ishlash natijasi:
```text
Qo'shish: 10 + 5 = 15
Ko'paytirish: 10 * 5 = 50
```

# 162-Topshiriq: Funksiyani boshqa funksiyaga argument sifatida uzatish (Callback)
## Topshiriq sharti:
Massiv elementlarini berilgan tekshiruvchi funksiya orqali filtrlovchi `filtr` funksiyasini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func filtr(sonlar []int, shart func(int) bool) []int {
	var natija []int
	for _, s := range sonlar {
		if shart(s) {
			natija = append(natija, s)
		}
	}
	return natija
}

func main() {
	raqamlar := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

	juftlar := filtr(raqamlar, func(n int) bool { return n%2 == 0 })
	beshdanKattalar := filtr(raqamlar, func(n int) bool { return n > 5 })

	fmt.Println("Juft sonlar:", juftlar)
	fmt.Println("5 dan kattalar:", beshdanKattalar)
}
```

## Tushuntirish va Mantiq:
Callback andozasi funksional dasturlash imkoniyatini beradi va kodning qayta ishlatilishini oshiradi.

## Ishlash natijasi:
```text
Juft sonlar: [2 4 6 8 10]
5 dan kattalar: [6 7 8 9 10]
```

# 163-Topshiriq: Funksiyadan funksiya qaytarish (Higher-Order Functions)
## Topshiriq sharti:
Berilgan songa ko'paytiruvchi yangi funksiya yasovchi `multiplikator` yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func kopaytiruvchiYarat(faktor int) func(int) int {
	return func(x int) int {
		return x * faktor
	}
}

func main() {
	ikkiBarobar := kopaytiruvchiYarat(2)
	uchBarobar := kopaytiruvchiYarat(3)

	fmt.Println("5 * 2 =", ikkiBarobar(5))
	fmt.Println("5 * 3 =", uchBarobar(5))
}
```

## Tushuntirish va Mantiq:
Yuqori tartibli funksiyalar (higher-order functions) yangi xatti-harakatga ega bo'lgan yangi funksiyalarni generatsiya qiladi.

## Ishlash natijasi:
```text
5 * 2 = 10
5 * 3 = 15
```

# 164-Topshiriq: Maxsus funksiya turlari (Function Types: type Operator func)
## Topshiriq sharti:
`type Amal func(int, int) int` e'lon qilib, kalkulyator amallarini xaritaga joylashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Amal func(int, int) int

func main() {
	amallar := map[string]Amal{
		"+": func(a, b int) int { return a + b },
		"-": func(a, b int) int { return a - b },
		"*": func(a, b int) int { return a * b },
	}

	fmt.Println("10 + 20 =", amallar["+"](10, 20))
	fmt.Println("20 - 5  =", amallar["-"](20, 5))
	fmt.Println("6 * 7   =", amallar["*"](6, 7))
}
```

## Tushuntirish va Mantiq:
`type` yordamida funksiya signaturasiga nom berish kodni o'ta toza va tushunarli qiladi.

## Ishlash natijasi:
```text
10 + 20 = 30
20 - 5  = 15
6 * 7   = 42
```

# 165-Topshiriq: defer kalit so'zi asoslari
## Topshiriq sharti:
`defer` orqali chaqirilgan funksiya asosiy funksiya tugashidan oldin bajarilishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	defer fmt.Println("Bu satr eng oxirida chiqadi (defer)")

	fmt.Println("1-satr: Dastur boshlandi")
	fmt.Println("2-satr: Asosiy hisoblar bajarilmoqda")
}
```

## Tushuntirish va Mantiq:
`defer` orqali belgilangan ifoda o'zi joylashgan funksiya to'liq tugashidan (yoki `return` bo'lgandan) so'ng bajariladi.

## Ishlash natijasi:
```text
1-satr: Dastur boshlandi
2-satr: Asosiy hisoblar bajarilmoqda
Bu satr eng oxirida chiqadi (defer)
```

# 166-Topshiriq: Bir nechta defer larning teskari tartibda (LIFO) ishlashi
## Topshiriq sharti:
Bir nechta ketma-ket `defer` yozing va ularning stak tartibida (Last In First Out) bajarilishini tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	fmt.Println("Boshlanish")

	defer fmt.Println("Defer 1")
	defer fmt.Println("Defer 2")
	defer fmt.Println("Defer 3")

	fmt.Println("Tugash")
}
```

## Tushuntirish va Mantiq:
Go defer larni stakka joylaydi: oxirgi qo'shilgan defer birinchi bo'lib bajariladi (LIFO: 3 -> 2 -> 1).

## Ishlash natijasi:
```text
Boshlanish
Tugash
Defer 3
Defer 2
Defer 1
```

# 167-Topshiriq: defer argumentlarining darhol hisoblanishi (Immediate Evaluation)
## Topshiriq sharti:
`defer` chaqirilgan paytdagi parametr qiymati keyinchalik o'zgarsa ham saqlanib qolishini isbotlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	i := 10
	defer fmt.Println("Defer ichida i qiymati:", i)

	i = 20
	fmt.Println("Asosiy kodda i qiymati:", i)
}
```

## Tushuntirish va Mantiq:
`defer` argumentlari `defer` satri o'qilgan paytning o'zidayoq hisoblanadi (evaluate bo'ladi), lekin funksiyaning o'zi oxirida ishga tushadi.

## Ishlash natijasi:
```text
Asosiy kodda i qiymati: 20
Defer ichida i qiymati: 10
```

# 168-Topshiriq: defer yordamida resurslarni tozalash (Cleanup pattern)
## Topshiriq sharti:
Fayl yoki ulanish ochilgach darhol uning yopilishini defer ga topshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func simulyatsiyaFaylOchish(nom string) {
	fmt.Printf("[OCHILDI] %s fayli ochildi\n", nom)
	defer fmt.Printf("[YOPILDI] %s fayli xavfsiz yopildi\n", nom)

	fmt.Println("[JARAYON] Ma'lumotlar o'qilmoqda...")
	fmt.Println("[JARAYON] Ma'lumotlar qayta ishlandi.")
}

func main() {
	simulyatsiyaFaylOchish("hisobot.pdf")
}
```

## Tushuntirish va Mantiq:
Resurs ochilgach darhol `defer resurs.Close()` yozish Go ning eng mashhur va xavfsiz qoidalaridan biridir.

## Ishlash natijasi:
```text
[OCHILDI] hisobot.pdf fayli ochildi
[JARAYON] Ma'lumotlar o'qilmoqda...
[JARAYON] Ma'lumotlar qayta ishlandi.
[YOPILDI] hisobot.pdf fayli xavfsiz yopildi
```

# 169-Topshiriq: defer orqali funksiyaning bajarilish vaqtini o'lchash
## Topshiriq sharti:
Anonim funksiya va `time.Since` orqali bajarilish vaqtini avtomatik hisoblovchi defer yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func vaqtniOlcha(funksiyaNomi string) func() {
	boshlanish := time.Now()
	return func() {
		fmt.Printf("[%s] Bajarilish vaqti: %v\n", funksiyaNomi, time.Since(boshlanish))
	}
}

func ogirHisoblash() {
	defer vaqtniOlcha("ogirHisoblash")() // Birinchi qism darhol, ikkinchisi defer da

	yigindi := 0
	for i := 0; i < 1000000; i++ {
		yigindi += i
	}
}

func main() {
	ogirHisoblash()
}
```

## Tushuntirish va Mantiq:
`defer fn()()` andozasi: tashqi funksiya kirish vaqtini belgilaydi, qaytgan ichki funksiya esa chiqishda vaqt farqini hisoblaydi.

## Ishlash natijasi:
```text
[ogirHisoblash] Bajarilish vaqti: 1.2ms
```

# 170-Topshiriq: defer orqali nomlangan qaytish qiymatini (Named Return) o'zgartirish
## Topshiriq sharti:
`defer` ichida funksiya qaytarayotgan qiymatni o'zgartirish imkoniyatini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func hisobla() (natija int) {
	defer func() {
		natija *= 2 // Qaytishdan oldin natijani 2 ga ko'paytiramiz
	}()

	return 25 // Dastlab 25 qaytmoqchi
}

func main() {
	fmt.Println("Yakuniy natija:", hisobla())
}
```

## Tushuntirish va Mantiq:
Nomlangan qaytish qiymatlari funksiya skopida mavjud bo'lgani sababli, `defer` dagi anonim funksiya uni `return` dan keyin ham o'zgartira oladi.

## Ishlash natijasi:
```text
Yakuniy natija: 50
```

# 171-Topshiriq: panic chaqiruvi va favqulodda to'xtash
## Topshiriq sharti:
Tiklab bo'lmaydigan jiddiy xatolikda `panic()` chaqiruvini namoyish qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func serverniUlash(manzil string) {
	if manzil == "" {
		panic("Server manzili bo'sh bo'lishi mumkin emas!")
	}
	fmt.Println("Serverga ulandi:", manzil)
}

func main() {
	defer fmt.Println("Dastur to'xtashidan oldin defer baribir ishladi!")
	serverniUlash("127.0.0.1:8080")
	// serverniUlash("") // Panic beradi
}
```

## Tushuntirish va Mantiq:
`panic` dasturning normal oqimini to'xtatadi, barcha defer larni bajaradi va stack trace bilan dasturni yakunlaydi.

## Ishlash natijasi:
```text
Serverga ulandi: 127.0.0.1:8080
Dastur to'xtashidan oldin defer baribir ishladi!
```

# 172-Topshiriq: recover() orqali panicni ushlash va bartaraf etish
## Topshiriq sharti:
`recover()` yordamida nolga bo'lish paytidagi panikni ushlab, dasturni o'chib ketishdan saqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func xavfsizBolish(a, b int) {
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("[RECOVER] Favqulodda xato ushlandi: %v\n", r)
		}
	}()

	fmt.Printf("%d / %d = %d\n", a, b, a/b)
}

func main() {
	xavfsizBolish(10, 2)
	xavfsizBolish(10, 0) // Panic yuz beradi, ammo recover ushlaydi
	fmt.Println("Dastur barqaror ishlashda davom etmoqda!")
}
```

## Tushuntirish va Mantiq:
`recover()` faqat `defer` qilingan funksiya ichida chaqirilgandagina panikni to'xtata oladi va xato obyekti (`r`) ni qaytaradi.

## Ishlash natijasi:
```text
10 / 2 = 5
[RECOVER] Favqulodda xato ushlandi: runtime error: integer divide by zero
Dastur barqaror ishlashda davom etmoqda!
```

# 173-Topshiriq: Safe Wrapper Decorator (Panikni Error ga aylantirish)
## Topshiriq sharti:
Har qanday xavfli funksiyani o'rab olib, panikni oddiy `error` ga aylantiruvchi decorator yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
)

func safeExecute(f func()) (err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("panik yuz berdi: %v", r)
		}
	}()
	f()
	return nil
}

func main() {
	xavfliFunksiya := func() {
		var p *int
		*p = 100 // Nil pointer dereference panic!
	}

	err := safeExecute(xavfliFunksiya)
	if err != nil {
		fmt.Println("Xatolik xavfsiz qayd etildi:", err)
	} else {
		fmt.Println("Muvaffaqiyatli bajarildi.")
	}
}
```

## Tushuntirish va Mantiq:
Ushbu andoza HTTP serverlar va mikroservislarda har bir so'rovni alohida himoyalash uchun keng qo'llaniladi.

## Ishlash natijasi:
```text
Xatolik xavfsiz qayd etildi: panik yuz berdi: runtime error: invalid memory address or nil pointer dereference
```

# 174-Topshiriq: Rekursiv funksiya: Faktorial hisoblash
## Topshiriq sharti:
O'z-o'zini chaqiruvchi rekursiv funksiya orqali faktorialni hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func faktorialRekursiv(n int) int {
	if n <= 1 {
		return 1 // Asosiy holat (Base case)
	}
	return n * faktorialRekursiv(n-1)
}

func main() {
	fmt.Println("5! =", faktorialRekursiv(5))
}
```

## Tushuntirish va Mantiq:
Rekursiyada doimo to'xtash sharti (base case) bo'lishi shart, aks holda cheksiz chaqiruv va stack overflow yuz beradi.

## Ishlash natijasi:
```text
5! = 120
```

# 175-Topshiriq: Rekursiv funksiya: Fibonachchi soni
## Topshiriq sharti:
N-chi Fibonachchi sonini rekursiv toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

func fibRekursiv(n int) int {
	if n <= 0 {
		return 0
	}
	if n == 1 {
		return 1
	}
	return fibRekursiv(n-1) + fibRekursiv(n-2)
}

func main() {
	fmt.Println("7-Fibonachchi soni:", fibRekursiv(7))
}
```

## Tushuntirish va Mantiq:
Rekursiv Fibonachchi daraxtsimon chaqiruv hosil qiladi (`F(n-1) + F(n-2)`).

## Ishlash natijasi:
```text
7-Fibonachchi soni: 13
```

# 176-Topshiriq: Rekursiv funksiya: Ichma-ich kataloglar iyerarxiyasini chop etish
## Topshiriq sharti:
Daraxtsimon ma'lumot tuzilmasini rekursiv aylanib chiqib, bo'shliqlar bilan iyerarxik ko'rinishda chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Tugun struct {
	Nomi   string
	Bolalar []Tugun
}

func chopEtDaraxt(t Tugun, chuqurlik int) {
	for i := 0; i < chuqurlik; i++ {
		fmt.Print("  ")
	}
	fmt.Println("-", t.Nomi)

	for _, bola := range t.Bolalar {
		chopEtDaraxt(bola, chuqurlik+1)
	}
}

func main() {
	ildiz := Tugun{
		Nomi: "Loyiha",
		Bolalar: []Tugun{
			{Nomi: "cmd", Bolalar: []Tugun{{Nomi: "main.go"}}},
			{Nomi: "internal", Bolalar: []Tugun{{Nomi: "app"}, {Nomi: "service"}}},
		},
	}

	chopEtDaraxt(ildiz, 0)
}
```

## Tushuntirish va Mantiq:
Rekursiya iyerarxik va daraxtsimon strukturalarni aylanib chiqish uchun eng tabiiy va qulay yondashuvdir.

## Ishlash natijasi:
```text
- Loyiha
  - cmd
    - main.go
  - internal
    - app
    - service
```

# 177-Topshiriq: Rekursiv funksiya: Satr palindromligini tekshirish
## Topshiriq sharti:
Satrning bosh va oxirgi harflarini solishtirib boruvchi rekursiv tekshiruv yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func isPalindromeRekursiv(s string) bool {
	if len(s) <= 1 {
		return true
	}
	if s[0] != s[len(s)-1] {
		return false
	}
	return isPalindromeRekursiv(s[1 : len(s)-1])
}

func main() {
	fmt.Println("radar:", isPalindromeRekursiv("radar"))
	fmt.Println("golang:", isPalindromeRekursiv("golang"))
}
```

## Tushuntirish va Mantiq:
Har bir rekursiv qadamda birinchi va oxirgi belgilar tekshirilib, o'rtadagi kichikroq qism qayta uzatiladi.

## Ishlash natijasi:
```text
radar: true
golang: false
```

# 178-Topshiriq: Funksional dasturlash: Map funksiyasi (elementlarni o'zgartirish)
## Topshiriq sharti:
Massivning barcha elementlariga funksiyani qo'llab yangi massiv qaytaruvchi `xaritalash` funksiyasini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func xaritalash(sonlar []int, f func(int) int) []int {
	natija := make([]int, len(sonlar))
	for i, s := range sonlar {
		natija[i] = f(s)
	}
	return natija
}

func main() {
	raqamlar := []int{1, 2, 3, 4, 5}
	kvadratlar := xaritalash(raqamlar, func(n int) int { return n * n })
	onBarobar := xaritalash(raqamlar, func(n int) int { return n * 10 })

	fmt.Println("Kvadratlar:", kvadratlar)
	fmt.Println("10 barobar:", onBarobar)
}
```

## Tushuntirish va Mantiq:
`Map` andozasi ma'lumotlar oqimini toza funksional uslubda o'zgartirishga xizmat qiladi.

## Ishlash natijasi:
```text
Kvadratlar: [1 4 9 16 25]
10 barobar: [10 20 30 40 50]
```

# 179-Topshiriq: Funksional dasturlash: Reduce funksiyasi (akkumulyatsiya)
## Topshiriq sharti:
Massivdagi barcha qiymatlarni bitta umumiy qiymatga keltiruvchi `qisqartirish` funksiyasini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func qisqartirish(sonlar []int, boshlangich int, f func(akkumulyator, joriy int) int) int {
	res := boshlangich
	for _, s := range sonlar {
		res = f(res, s)
	}
	return res
}

func main() {
	sonlar := []int{1, 2, 3, 4, 5}

	yigindi := qisqartirish(sonlar, 0, func(a, b int) int { return a + b })
	kopaytma := qisqartirish(sonlar, 1, func(a, b int) int { return a * b })

	fmt.Println("Yig'indi (Reduce):", yigindi)
	fmt.Println("Ko'paytma (Reduce):", kopaytma)
}
```

## Tushuntirish va Mantiq:
`Reduce` (yoki Fold) har bir elementni akkumulyator bilan birlashtirib yakuniy yagona natija hosil qiladi.

## Ishlash natijasi:
```text
Yig'indi (Reduce): 15
Ko'paytma (Reduce): 120
```

# 180-Topshiriq: Go da Functional Options Pattern (Funksional Opsiyalar Andozasi)
## Topshiriq sharti:
Server konfiguratsiyasini moslashuvchan, kengaytiriladigan va xavfsiz qilish uchun Functional Options andozasini qo'llang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Server struct {
	Host    string
	Port    int
	Timeout int
}

type ServerOption func(*Server)

func WithPort(port int) ServerOption {
	return func(s *Server) {
		s.Port = port
	}
}

func WithTimeout(timeout int) ServerOption {
	return func(s *Server) {
		s.Timeout = timeout
	}
}

func NewServer(host string, opts ...ServerOption) *Server {
	srv := &Server{
		Host:    host,
		Port:    8080, // Standart port
		Timeout: 30,   // Standart timeout
	}
	for _, opt := range opts {
		opt(srv)
	}
	return srv
}

func main() {
	s1 := NewServer("localhost")
	s2 := NewServer("api.production.uz", WithPort(443), WithTimeout(60))

	fmt.Printf("Standart server: %+v\n", s1)
	fmt.Printf("Moslashtirilgan server: %+v\n", s2)
}
```

## Tushuntirish va Mantiq:
Functional Options Go hamjamiyatida kutubxonalar va serverlarni konfiguratsiya qilishning eng ilg'or uslubidir.

## Ishlash natijasi:
```text
Standart server: &{Host:localhost Port:8080 Timeout:30}
Moslashtirilgan server: &{Host:api.production.uz Port:443 Timeout:60}
```

# 181-Topshiriq: Memoizatsiya (Memoization) closure orqali natijalarni keshlovchi funksiya
## Topshiriq sharti:
Qimmat hisoblashlar natijalarini map da keshlab, qayta chaqirilganda keshdan beruvchi funksiya yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func keshliKvadrat() func(int) int {
	kesh := make(map[int]int)

	return func(n int) int {
		if val, mavjud := kesh[n]; mavjud {
			fmt.Printf("[KESH] %d natijasi keshdan olindi\n", n)
			return val
		}
		fmt.Printf("[HISOBLASH] %d uchun hisoblandi\n", n)
		natija := n * n
		kesh[n] = natija
		return natija
	}
}

func main() {
	kv := keshliKvadrat()
	fmt.Println("Natija 1:", kv(5))
	fmt.Println("Natija 2:", kv(5)) // Keshdan olinadi
	fmt.Println("Natija 3:", kv(8))
}
```

## Tushuntirish va Mantiq:
Closure o'z ichida `kesh` xaritasini saqlab turadi va bir xil argument bilan qayta murojaat qilinganda hisoblashni chetlab o'tadi.

## Ishlash natijasi:
```text
[HISOBLASH] 5 uchun hisoblandi
Natija 1: 25
[KESH] 5 natijasi keshdan olindi
Natija 2: 25
[HISOBLASH] 8 uchun hisoblandi
Natija 3: 64
```

# 182-Topshiriq: Argumentlarni qiymat bo'yicha uzatish (Pass-By-Value) isboti
## Topshiriq sharti:
Funksiyaga uzatilgan o'zgaruvchi funksiya ichida o'zgartirilsa ham tashqarida o'zgarmasligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func oshir(son int) {
	son += 10
	fmt.Println("Funksiya ichida:", son)
}

func main() {
	x := 5
	oshir(x)
	fmt.Println("Funksiyadan keyin tashqarida x:", x)
}
```

## Tushuntirish va Mantiq:
Go tilida hamma narsa faqat qiymat bo'yicha (by-value) uzatiladi. Funksiya o'zgaruvchining to'liq mustaqil nusxasini oladi.

## Ishlash natijasi:
```text
Funksiya ichida: 15
Funksiyadan keyin tashqarida x: 5
```

# 183-Topshiriq: Ko'rsatkich orqali argument qiymatini o'zgartirish (Pass-By-Pointer)
## Topshiriq sharti:
Ko'rsatkich (`*int`) uzatish orqali tashqi o'zgaruvchini funksiya ichidan yangilang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func oshirKorsatkich(p *int) {
	*p += 10
}

func main() {
	x := 5
	fmt.Println("Dastlabki x:", x)
	oshirKorsatkich(&x)
	fmt.Println("Yangilangan x:", x)
}
```

## Tushuntirish va Mantiq:
Ko'rsatkichning o'zi ham qiymat bo'yicha uzatiladi, biroq u xotira manzilini ko'rsatib turganligi sababli asl qiymat o'zgaradi.

## Ishlash natijasi:
```text
Dastlabki x: 5
Yangilangan x: 15
```

# 184-Topshiriq: Ko'p xatoliklarni birlashtiruvchi funksiya
## Topshiriq sharti:
Forma validatsiyasida barcha maydon xatolarini bitta ro'yxatda yig'uvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

func tekshirFoydalanuvchi(ism string, yosh int) []string {
	var xatolar []string
	if strings.TrimSpace(ism) == "" {
		xatolar = append(xatolar, "Ism bo'sh bo'lishi mumkin emas")
	}
	if yosh < 18 {
		xatolar = append(xatolar, "Yosh kamida 18 bo'lishi shart")
	}
	return xatolar
}

func main() {
	xatolar := tekshirFoydalanuvchi("", 16)
	if len(xatolar) > 0 {
		fmt.Printf("Topilgan %d ta xatolik:\n", len(xatolar))
		for _, x := range xatolar {
			fmt.Println("-", x)
		}
	}
}
```

## Tushuntirish va Mantiq:
Birinchi xatoda to'xtamasdan barcha xatoliklarni yig'ib foydalanuvchiga to'liq hisobot berish qulay uslubdir.

## Ishlash natijasi:
```text
Topilgan 2 ta xatolik:
- Ism bo'sh bo'lishi mumkin emas
- Yosh kamida 18 bo'lishi shart
```

# 185-Topshiriq: Retry (Qayta Urinish) Decorator funksiyasi
## Topshiriq sharti:
Xatolik yuz berganda operatsiyani berilgan miqdorgacha qayta takrorlovchi yuqori tartibli funksiya yozing.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func retry(urinishlar int, f func() error) error {
	var err error
	for i := 1; i <= urinishlar; i++ {
		err = f()
		if err == nil {
			return nil
		}
		fmt.Printf("%d-urinish xato bilan tugadi: %v\n", i, err)
	}
	return fmt.Errorf("%d urinishdan keyin ham bajarilmadi: %w", urinishlar, err)
}

func main() {
	hisob := 0
	tarmoqOperatsiyasi := func() error {
		hisob++
		if hisob < 3 {
			return errors.New("aloqa yo'q")
		}
		return nil // 3-urinishda muvaffaqiyat
	}

	err := retry(3, tarmoqOperatsiyasi)
	if err == nil {
		fmt.Println("Muvaffaqiyatli yakunlandi!")
	}
}
```

## Tushuntirish va Mantiq:
Taqsimlangan tizimlarda vaqtincha uzilishlarni yengib o'tish uchun retry decoratorlari ishlatiladi.

## Ishlash natijasi:
```text
1-urinish xato bilan tugadi: aloqa yo'q
2-urinish xato bilan tugadi: aloqa yo'q
Muvaffaqiyatli yakunlandi!
```

# 186-Topshiriq: Funksiyalarni konveyer (Pipeline) usulida zanjirlash
## Topshiriq sharti:
Matnni ketma-ket tozalovchi, kichik harfga o'tkazuvchi va qirquvchi funksiyalar zanjirini yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

type MatnTransformatsiyasi func(string) string

func qatorTransform(matn string, qadamlar ...MatnTransformatsiyasi) string {
	res := matn
	for _, qadam := range qadamlar {
		res = qadam(res)
	}
	return res
}

func main() {
	kiruvchi := "   SALOM GO DASTURCHI   "

	tozalangan := qatorTransform(
		kiruvchi,
		strings.TrimSpace,
		strings.ToLower,
	)

	fmt.Printf("Asl: %q\n", kiruvchi)
	fmt.Printf("Natija: %q\n", tozalangan)
}
```

## Tushuntirish va Mantiq:
Pipeline andozasi murakkab jarayonlarni sodda va alohida testlanuvchi bosqichlarga ajratadi.

## Ishlash natijasi:
```text
Asl: "   SALOM GO DASTURCHI   "
Natija: "salom go dasturchi"
```

# 187-Topshiriq: Funksiyaga bo'sh interfeys (any) uzatish va tahlil qilish
## Topshiriq sharti:
Har qanday turdagi parametrni qabul qilib uning xususiyatlarini chop etuvchi umumiy funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func tahlilEt(qiymat any) {
	fmt.Printf("Qiymat: %v, Turi: %T\n", qiymat, qiymat)
}

func main() {
	tahlilEt(42)
	tahlilEt("Go 1.22+")
	tahlilEt([]int{1, 2, 3})
}
```

## Tushuntirish va Mantiq:
`any` (`interface{}` ning Go 1.18+ taxallusi) har qanday qiymatni qabul qila oladi.

## Ishlash natijasi:
```text
Qiymat: 42, Turi: int
Qiymat: Go 1.22+, Turi: string
Qiymat: [1 2 3], Turi: []int
```

# 188-Topshiriq: Panic yuz berganda defer larning to'liq bajarilishi kafolati
## Topshiriq sharti:
Panik sodir bo'lganda ham `defer` bloklari birortasi qolib ketmasdan to'liq chaqirilishini isbotlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func testPanicDefer() {
	defer fmt.Println("1-defer bajarildi")
	defer fmt.Println("2-defer bajarildi")

	fmt.Println("Panikdan oldingi amal")
	panic("Kutilmagan favqulodda holat!")
}

func main() {
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("Panik ushlandi: %v\n", r)
		}
	}()

	testPanicDefer()
}
```

## Tushuntirish va Mantiq:
Go da funksiya qanday tugashidan qat'i nazar (oddiy return yoki panic), barcha ro'yxatga olingan defer lar 100% bajariladi.

## Ishlash natijasi:
```text
Panikdan oldingi amal
2-defer bajarildi
1-defer bajarildi
Panik ushlandi: Kutilmagan favqulodda holat!
```

# 189-Topshiriq: Currying (Karlash) konsepsiyasi
## Topshiriq sharti:
Ko'p parametrli funksiyani bitta parametrlik zanjirga ajratuvchi usul.

## Yechim (Go kodi):
```go
package main

import "fmt"

func prefiksQosh(prefiks string) func(string) string {
	return func(matn string) string {
		return prefiks + ": " + matn
	}
}

func main() {
	xatoLog = prefiksQosh("[XATO]")
	infoLog = prefiksQosh("[MA'LUMOT]")

	fmt.Println(xatoLog("Fayl topilmadi"))
	fmt.Println(infoLog("Tizim ishga tushdi"))
}

var xatoLog func(string) string
var infoLog func(string) string
```

## Tushuntirish va Mantiq:
Currying bir argumentni fiksatsiya qilib, ixtisoslashgan yangi funksiyalar yasashga xizmat qiladi.

## Ishlash natijasi:
```text
[XATO]: Fayl topilmadi
[MA'LUMOT]: Tizim ishga tushdi
```

# 190-Topshiriq: Logger Middleware Decorator funksiyasi
## Topshiriq sharti:
Har qanday funksiyani o'rab, uning boshlanishi va tugashini avtomatik loglovchi wrapper yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func logWrapper(nom string, f func()) func() {
	return func() {
		fmt.Printf("--> [%s] boshlandi\n", nom)
		f()
		fmt.Printf("<-- [%s] yakunlandi\n", nom)
	}
}

func main() {
	hisobAmali := func() {
		fmt.Println("    Muhim hisob-kitoblar bajarilmoqda...")
	}

	o'ralganAmal := logWrapper("BalansHisoblash", hisobAmali)
	o'ralganAmal()
}
```

## Tushuntirish va Mantiq:
Middleware decoratorlari veb routerlarda, so'rovlarni avtorizatsiya va monitoring qilishda asosiy vositadir.

## Ishlash natijasi:
```text
--> [BalansHisoblash] boshlandi
    Muhim hisob-kitoblar bajarilmoqda...
<-- [BalansHisoblash] yakunlandi
```

# 191-Topshiriq: Qaytish xatoligini e'tiborsiz qoldirmaslik qoidasi
## Topshiriq sharti:
Funksiya qaytargan xatolikni tekshirish va uni bekorga `_` bilan yopib ketmaslik zaruratini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func pulYechish(hisob, miqdor int) (int, error) {
	if miqdor > hisob {
		return hisob, errors.New("balans yetarli emas")
	}
	return hisob - miqdor, nil
}

func main() {
	hisob := 100
	miqdor := 150

	qoldiq, err := pulYechish(hisob, miqdor)
	if err != nil {
		fmt.Printf("Tranzaksiya rad etildi: %v\n", err)
		return
	}
	fmt.Printf("Yangi hisob: %d\n", qoldiq)
}
```

## Tushuntirish va Mantiq:
Go da `error` qiymatini tekshirmaslik eng ko'p uchraydigan xatolarga sabab bo'ladi. Har doim `if err != nil` tekshiruvi tavsiya etiladi.

## Ishlash natijasi:
```text
Tranzaksiya rad etildi: balans yetarli emas
```

# 192-Topshiriq: Dependency Injection (Bog'liqlikni kiritish) sodda funksiya orqali
## Topshiriq sharti:
Xabarnoma yuboruvchi funksiyaga SMS yoki Email xizmatini parametr sifatida uzating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type XabarYuboruvchi func(kimga, matn string)

func smsYubor(kimga, matn string) {
	fmt.Printf("[SMS] %s ga yuborildi: %s\n", kimga, matn)
}

func emailYubor(kimga, matn string) {
	fmt.Printf("[EMAIL] %s ga yuborildi: %s\n", kimga, matn)
}

func xushKelibsiz(foydalanuvchi, aloqa string, yuboruvchi XabarYuboruvchi) {
	matn := "Platformamizga xush kelibsiz, " + foydalanuvchi + "!"
	yuboruvchi(aloqa, matn)
}

func main() {
	xushKelibsiz("Anvar", "+998901234567", smsYubor)
	xushKelibsiz("Dilnoza", "dilnoza@example.uz", emailYubor)
}
```

## Tushuntirish va Mantiq:
Funksiyalar parametr sifatida uzatilganda tashqi tizimlar bilan bog'liqlik yumshaydi va test yozish juda osonlashadi.

## Ishlash natijasi:
```text
[SMS] +998901234567 ga yuborildi: Platformamizga xush kelibsiz, Anvar!
[EMAIL] dilnoza@example.uz ga yuborildi: Platformamizga xush kelibsiz, Dilnoza!
```

# 193-Topshiriq: Validatsiya zanjiri (Validation Chain)
## Topshiriq sharti:
Ro'yxatdan o'tayotgan foydalanuvchi ma'lumotlarini ketma-ket tekshiruvchi validatorlar massividan foydalaning.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

type Validator func(string) error

func minUzunlik(l int) Validator {
	return func(s string) error {
		if len(s) < l {
			return fmt.Errorf("uzunlik kamida %d bo'lishi shart", l)
		}
		return nil
	}
}

func main() {
	tekshiruvlar := []Validator{
		minUzunlik(6),
	}

	parol := "123"
	for _, v := range tekshiruvlar {
		if err := v(parol); err != nil {
			fmt.Printf("Xatolik: %v\n", err)
		}
	}
}
```

## Tushuntirish va Mantiq:
Validator funksiyalari to'plami dinamik ravishda kengaytirilishi va qayta qo'llanilishi mumkin.

## Ishlash natijasi:
```text
Xatolik: uzunlik kamida 6 bo'lishi shart
```

# 194-Topshiriq: Nil funksiya ko'rsatkichini tekshirish
## Topshiriq sharti:
Funksiya turi o'zgaruvchisi `nil` bo'lganda uni chaqirish panic bermasligi uchun tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func bajarXavfsiz(fn func()) {
	if fn == nil {
		fmt.Println("[OGOHLANTIRISH] Funksiya berilmagan (nil)")
		return
	}
	fn()
}

func main() {
	var f func()
	bajarXavfsiz(f) // Panic bermaydi!

	f = func() { fmt.Println("Funksiya muvaffaqiyatli ishladi!") }
	bajarXavfsiz(f)
}
```

## Tushuntirish va Mantiq:
`nil` bo'lgan funksiyani chaqirish (`fn()`) bevosita panic keltirib chiqaradi, shuning uchun oldindan tekshirish zarur.

## Ishlash natijasi:
```text
[OGOHLANTIRISH] Funksiya berilmagan (nil)
Funksiya muvaffaqiyatli ishladi!
```

# 195-Topshiriq: Rekursiyada chuqurlik chegarasi (Stack Overflow himoyasi)
## Topshiriq sharti:
Cheksiz chuqurlikka tushib ketmaslik uchun rekursiyada maksimal chuqurlik chegarasini qo'llang.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func xavfsizRekursiya(qadam, maxChuqurlik int) error {
	if qadam > maxChuqurlik {
		return errors.New("maksimal chaqiruv chuqurligi oshib ketdi")
	}
	fmt.Printf("Chuqurlik darajasi: %d\n", qadam)
	return xavfsizRekursiya(qadam+1, maxChuqurlik)
}

func main() {
	err := xavfsizRekursiya(1, 3)
	if err != nil {
		fmt.Println("To'xtatildi:", err)
	}
}
```

## Tushuntirish va Mantiq:
Chuqurlik chegarasi (depth limit) stak to'lib qolishining oldini oluvchi muhim himoya usulidir.

## Ishlash natijasi:
```text
Chuqurlik darajasi: 1
Chuqurlik darajasi: 2
Chuqurlik darajasi: 3
To'xtatildi: maksimal chaqiruv chuqurligi oshib ketdi
```

# 196-Topshiriq: Funksiya ichida defer va return qiymatini loglash
## Topshiriq sharti:
Funksiya yakunida qanday qiymat qaytarganini defer anonim funksiyasi orqali logga yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func kvadratHisobla(n int) (res int) {
	defer func() {
		fmt.Printf("[AUDIT] kvadratHisobla(%d) natijasi = %d\n", n, res)
	}()

	res = n * n
	return res
}

func main() {
	kvadratHisobla(9)
}
```

## Tushuntirish va Mantiq:
Nomlangan natijalar defer ichida ochiq ko'rinadi, bu esa audit va diagnostika uchun juda qulay.

## Ishlash natijasi:
```text
[AUDIT] kvadratHisobla(9) natijasi = 81
```

# 197-Topshiriq: Xavfsiz Worker funksiyasi (Goroutine panikdan saqlash)
## Topshiriq sharti:
Fon vazifasi ichida paydo bo'lgan panik butun dasturni to'xtatib qo'ymasligini ta'minlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func xavfsizVazifa(id int, vazifa func()) {
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("[FON WORKER %d] Panikdan tiklandi: %v\n", id, r)
		}
	}()
	vazifa()
}

func main() {
	xavfsizVazifa(1, func() {
		fmt.Println("Worker 1: Bajarilmoqda...")
		panic("Kutilmagan nol ko'rsatkich!")
	})
	fmt.Println("Asosiy dastur to'xtamasdan ishlashda davom etmoqda.")
}
```

## Tushuntirish va Mantiq:
Goroutine larda yuz bergan ushlanmagan panik butun operatsion jarayonni (process) qulatadi, shu sababli xavfsiz o'ram zarur.

## Ishlash natijasi:
```text
Worker 1: Bajarilmoqda...
[FON WORKER 1] Panikdan tiklandi: Kutilmagan nol ko'rsatkich!
Asosiy dastur to'xtamasdan ishlashda davom etmoqda.
```

# 198-Topshiriq: Tranzaksiya boshqaruvi: defer bilan Rollback va Commit
## Topshiriq sharti:
Amal muvaffaqiyatsiz bo'lsa avtomatik rollback, muvaffaqiyatli bo'lsa commit qiluvchi defer tuzilmasini yozing.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

type Tranzaksiya struct {
	Bajarildimi bool
}

func (t *Tranzaksiya) Commit()   { fmt.Println("[DB] Tranzaksiya tasdiqlandi (COMMIT)") }
func (t *Tranzaksiya) Rollback() { fmt.Println("[DB] Tranzaksiya bekor qilindi (ROLLBACK)") }

func amaliyot(muvaffaqiyatli bool) (err error) {
	tx := &Tranzaksiya{}
	defer func() {
		if err != nil || !tx.Bajarildimi {
			tx.Rollback()
		} else {
			tx.Commit()
		}
	}()

	if !muvaffaqiyatli {
		return errors.New("to'lov shlyuzida xatolik yuz berdi")
	}

	tx.Bajarildimi = true
	return nil
}

func main() {
	fmt.Println("--- 1-holat: Xatolik bilan ---")
	_ = amaliyot(false)

	fmt.Println("--- 2-holat: Muvaffaqiyatli ---")
	_ = amaliyot(true)
}
```

## Tushuntirish va Mantiq:
Ma'lumotlar bazasi tranzaksiyalarida xatolik yuz berganda xavfsiz bekor qilish uchun defer eng ishonchli mexanizmdir.

## Ishlash natijasi:
```text
--- 1-holat: Xatolik bilan ---
[DB] Tranzaksiya bekor qilindi (ROLLBACK)
--- 2-holat: Muvaffaqiyatli ---
[DB] Tranzaksiya tasdiqlandi (COMMIT)
```

# 199-Topshiriq: Sodda Funksional Kompozitsiya (Function Composition)
## Topshiriq sharti:
Ikki funksiyani f(g(x)) ko'rinishida birlashtiruvchi kompozitor yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func birlashtir(f func(int) int, g func(int) int) func(int) int {
	return func(x int) int {
		return f(g(x))
	}
}

func main() {
	ikkiBarobar := func(x int) int { return x * 2 }
	uchQosh := func(x int) int { return x + 3 }

	// f(g(x)) -> (x + 3) * 2
	amal := birlashtir(ikkiBarobar, uchQosh)

	natija := amal(5) // (5 + 3) * 2 = 16
	fmt.Println("(5 + 3) * 2 =", natija)
}
```

## Tushuntirish va Mantiq:
Kompozitsiya orqali kichik va mustaqil funksiyalardan murakkabroq amallar hosil qilinadi.

## Ishlash natijasi:
```text
(5 + 3) * 2 = 16
```

# 200-Topshiriq: Yakuniy amaliy vazifa: To'liq resurslarni boshqaruvchi xavfsiz kontekst funksiyasi
## Topshiriq sharti:
Resurs ochilishi, bajarilishi, xatolar ushlanishi va har doim tozalanishini ta'minlovchi to'liq funksional tizim yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
)

type Resurs struct {
	Nomi string
}

func (r *Resurs) Close() {
	fmt.Printf("[RESURS] '%s' resursi xavfsiz tozalandi va yopildi.\n", r.Nomi)
}

func BajarResursBilan(nomi string, amal func(r *Resurs) error) (err error) {
	resurs := &Resurs{Nomi: nomi}
	fmt.Printf("[RESURS] '%s' resursi muvaffaqiyatli ochildi.\n", nomi)

	defer resurs.Close()

	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("operatsiyada kutilmagan panik: %v", r)
		}
	}()

	return amal(resurs)
}

func main() {
	err := BajarResursBilan("PostgreSQL_Pool", func(r *Resurs) error {
		fmt.Println("  --> SQL so'rovlar bajarilmoqda...")
		return nil
	})

	if err != nil {
		fmt.Println("Xatolik:", err)
	} else {
		fmt.Println("Vazifa to'liq yakunlandi!")
	}
}
```

## Tushuntirish va Mantiq:
Bu andoza Go ning eng kuchli taraflarini: resurs xavfsizligi, xatoliklar boshqaruvi va defer mexanizmini to'liq namoyon qiladi.

## Ishlash natijasi:
```text
[RESURS] 'PostgreSQL_Pool' resursi muvaffaqiyatli ochildi.
  --> SQL so'rovlar bajarilmoqda...
[RESURS] 'PostgreSQL_Pool' resursi xavfsiz tozalandi va yopildi.
Vazifa to'liq yakunlandi!
```

