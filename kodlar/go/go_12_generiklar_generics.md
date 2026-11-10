# 12-Mavzu: Generiklar (Generics) va Parametrlangan Turlar (551-600)

Go 1.18 talqini bilan kiritilgan eng muhim yangilik: Generiklar (Parametric Polymorphism). Tip parametrlari (`[T any]`), cheklovlar (`comparable`, `cmp.Ordered`, tip birlashmalari `|`, tilda `~`), generik funksiyalar (Min, Max, Filter, Map, Reduce), generik ma'lumotlar tuzilmalari (Stack, Queue, Cache, Set) va Go dagi metod cheklovlari bo'yicha 50 ta amaliy topshiriq.

# 551-Topshiriq: Generiklar nima va Go da kod takrorlanishini qanday yechadi?
## Topshiriq sharti:
Ikkita int va ikkita float64 sonlarini alohida funksiyalarsiz bitta generik funksiya bilan taqqoslang.

## Yechim (Go kodi):
```go
package main

import (
	"cmp"
	"fmt"
)

// Generik funksiya: T har qanday tartiblanuvchi tur bo'lishi mumkin
func KattaSon[T cmp.Ordered](a, b T) T {
	if a > b {
		return a
	}
	return b
}

func main() {
	fmt.Println("Int solishtiruvi:", KattaSon(10, 25))
	fmt.Println("Float solishtiruvi:", KattaSon(3.14, 2.71))
	fmt.Println("String solishtiruvi:", KattaSon("olma", "anor"))
}
```

## Tushuntirish va Mantiq:
Generiklar kiritilgunga qadar dasturchilar har bir tur uchun alohida funksiya yozishi yoki xavfli `any` casting qilishga majbur edi. Generiklar tur xavfsizligini (Type-safety) to'liq saqlaydi.

## Ishlash natijasi:
```text
Int solishtiruvi: 25
Float solishtiruvi: 3.14
String solishtiruvi: olma
```

# 552-Topshiriq: any cheklovi bilan umumiy generik funksiya yozish
## Topshiriq sharti:
Har qanday turdagi ikkita qiymatni chop etuvchi `ChopEt[T any]` funksiyasini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ChopEtJuftlik[T any](birinchi, ikkinchi T) {
	fmt.Printf("1: %v, 2: %v (turi: %T)\n", birinchi, ikkinchi, birinchi)
}

func main() {
	ChopEtJuftlik("Go", "Python")
	ChopEtJuftlik(100, 200)
}
```

## Tushuntirish va Mantiq:
`[T any]` da `T` ixtiyoriy tur bo'lishi mumkinligini bildiradi. Biroq `any` turida `>` yoki `<` kabi operatorlarni ishlatib bo'lmaydi.

## Ishlash natijasi:
```text
1: Go, 2: Python (turi: string)
1: 100, 2: 200 (turi: int)
```

# 553-Topshiriq: comparable cheklovi bilan tenglikni tekshirish
## Topshiriq sharti:
Sliceda element bor-yo'qligini tekshiruvchi `Mavjudmi[T comparable]` funksiyasini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func Mavjudmi[T comparable](slice []T, maqsad T) bool {
	for _, element := range slice {
		if element == maqsad {
			return true
		}
	}
	return false
}

func main() {
	sonlar := []int{1, 2, 3, 4, 5}
	fmt.Println("3 bormi:", Mavjudmi(sonlar, 3))
	fmt.Println("10 bormi:", Mavjudmi(sonlar, 10))

	ismlar := []string{"Ali", "Vali"}
	fmt.Println("'Ali' bormi:", Mavjudmi(ismlar, "Ali"))
}
```

## Tushuntirish va Mantiq:
`comparable` faqat `==` va `!=` operatorlari orqali taqqoslana oladigan turlarga (int, string, bool, pointer, struct) ruxsat beradi.

## Ishlash natijasi:
```text
3 bormi: true
10 bormi: false
'Ali' bormi: true
```

# 554-Topshiriq: Standart cmp.Ordered cheklovi (Go 1.21+)
## Topshiriq sharti:
`cmp.Ordered` yordamida `<, <=, >, >=` operatorlarini qo'llab minimal elementni toping.

## Yechim (Go kodi):
```go
package main

import (
	"cmp"
	"fmt"
)

func MinQiymat[T cmp.Ordered](a, b T) T {
	if a < b {
		return a
	}
	return b
}

func main() {
	fmt.Println("Min int:", MinQiymat(45, 12))
	fmt.Println("Min float:", MinQiymat(19.5, 42.1))
	fmt.Println("Min string:", MinQiymat("banan", "anor"))
}
```

## Tushuntirish va Mantiq:
`cmp.Ordered` Go 1.21 da kiritilgan bo'lib, barcha butun sonlar, kasr sonlar va satrlarni birlashtiradi.

## Ishlash natijasi:
```text
Min int: 12
Min float: 19.5
Min string: anor
```

# 555-Topshiriq: Maxsus tip cheklovlari (Type Unions: int | float64)
## Topshiriq sharti:
Faqat raqamli turlar uchun amal qiluvchi maxsus `Son` interfeysini e'lon qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Son interface {
	int | int32 | int64 | float32 | float64
}

func Qosh[T Son](a, b T) T {
	return a + b
}

func main() {
	fmt.Println("Butun sonlar yig'indisi:", Qosh(15, 30))
	fmt.Println("Haqiqiy sonlar yig'indisi:", Qosh(1.5, 2.5))
}
```

## Tushuntirish va Mantiq:
Interfeys ichida `|` (yoki) belgisi orqali ruxsat etilgan turlar ro'yxati (Type Union) belgilanadi.

## Ishlash natijasi:
```text
Butun sonlar yig'indisi: 45
Haqiqiy sonlar yig'indisi: 4
```

# 556-Topshiriq: Taxallus turlar va tilda (~) belgisi (Underlying Type Approximation)
## Topshiriq sharti:
`~int` yordamida `type Yosh int` kabi yangi turlarni ham cheklovga kiritishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Raqam interface {
	~int | ~float64 // ~ belgisi shu turga asoslangan har qanday yangi turni qabul qiladi
}

type MeningYoshim int

func IkkiBarobar[T Raqam](val T) T {
	return val * 2
}

func main() {
	var yosh MeningYoshim = 20
	fmt.Println("Natija:", IkkiBarobar(yosh))
}
```

## Tushuntirish va Mantiq:
`~T` sintaksisi turning tagidagi (underlying) turini tekshiradi, bu orqali `type X int` turlari ham generik funksiyaga bemalol uzatiladi.

## Ishlash natijasi:
```text
Natija: 40
```

# 557-Topshiriq: Generik Reverse funksiyasi (Sliceni teskari o'girish)
## Topshiriq sharti:
Har qanday turdagi sliceni joyida teskari qiluvchi umumiy funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func Reverse[T any](s []T) {
	for i, j := 0, len(s)-1; i < j; i, j = i+1, j-1 {
		s[i], s[j] = s[j], s[i]
	}
}

func main() {
	sonlar := []int{1, 2, 3, 4, 5}
	Reverse(sonlar)
	fmt.Println("Teskari sonlar:", sonlar)

	sozlar := []string{"A", "B", "C"}
	Reverse(sozlar)
	fmt.Println("Teskari so'zlar:", sozlar)
}
```

## Tushuntirish va Mantiq:
`Reverse[T any]` har qanday ma'lumot turi uchun alohida kod yozmasdan xotirani samarali o'zgartiradi.

## Ishlash natijasi:
```text
Teskari sonlar: [5 4 3 2 1]
Teskari so'zlar: [C B A]
```

# 558-Topshiriq: Generik Filter funksiyasi
## Topshiriq sharti:
Predikat funksiya shartiga ko'ra elementlarni filtrlovchi umumiy funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func Filter[T any](slice []T, shart func(T) bool) []T {
	var natija []T
	for _, item := range slice {
		if shart(item) {
			natija = append(natija, item)
		}
	}
	return natija
}

func main() {
	sonlar := []int{1, 2, 3, 4, 5, 6, 7, 8}
	juftlar := Filter(sonlar, func(n int) bool { return n%2 == 0 })
	fmt.Println("Juft sonlar:", juftlar)

	tillari := []string{"Go", "Python", "Rust", "Java"}
	uzunlar := Filter(tillari, func(s string) bool { return len(s) > 3 })
	fmt.Println("Uzun nomli tillar:", uzunlar)
}
```

## Tushuntirish va Mantiq:
Generik `Filter` barcha turlar ustida funksional filtrlash imkonini beradi.

## Ishlash natijasi:
```text
Juft sonlar: [2 4 6 8]
Uzun nomli tillar: [Python Rust Java]
```

# 559-Topshiriq: Generik Map funksiyasi: [T, R any] (Boshqa turga o'girish)
## Topshiriq sharti:
T turidagi massivni R turidagi yangi massivga aylantiruvchi ikki parametrli generik yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strconv"
)

func Map[T, R any](slice []T, f func(T) R) []R {
	natija := make([]R, len(slice))
	for i, item := range slice {
		natija[i] = f(item)
	}
	return natija
}

func main() {
	sonlar := []int{10, 20, 30}

	// int slice -> string slice ga o'tkazamiz:
	satrlar := Map(sonlar, func(n int) string {
		return "Son: " + strconv.Itoa(n)
	})

	fmt.Println("Natija:", satrlar)
}
```

## Tushuntirish va Mantiq:
`[T, R any]` da kiruvchi va chiquvchi turlar turlicha bo'lishi mumkin (masalan `int` dan `string` ga).

## Ishlash natijasi:
```text
Natija: [Son: 10 Son: 20 Son: 30]
```

# 560-Topshiriq: Generik Reduce funksiyasi
## Topshiriq sharti:
Kolleksiyani bitta natijaga yig'uvchi generik akkumulyator yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func Reduce[T, R any](slice []T, boshlangich R, f func(akkumulyator R, joriy T) R) R {
	res := boshlangich
	for _, item := range slice {
		res = f(res, item)
	}
	return res
}

func main() {
	sonlar := []int{1, 2, 3, 4}
	yigindi := Reduce(sonlar, 0, func(acc, val int) int { return acc + val })
	fmt.Println("Yig'indi:", yigindi)
}
```

## Tushuntirish va Mantiq:
Generik `Reduce` funksional dasturlashning eng qudratli vositalaridan biridir.

## Ishlash natijasi:
```text
Yig'indi: 10
```

# 561-Topshiriq: Generik Stek (Stack[T]) ma'lumot tuzilmasi
## Topshiriq sharti:
Har qanday turdagi elementlarni saqlay oluvchi `Stack[T]` strukturasini loyihalang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Stack[T any] struct {
	elementlar []T
}

func (s *Stack[T]) Push(item T) {
	s.elementlar = append(s.elementlar, item)
}

func (s *Stack[T]) Pop() (T, bool) {
	if len(s.elementlar) == 0 {
		var nol T // T ning nol qiymati
		return nol, false
	}
	oxirgiIdx := len(s.elementlar) - 1
	qiymat := s.elementlar[oxirgiIdx]
	s.elementlar = s.elementlar[:oxirgiIdx]
	return qiymat, true
}

func main() {
	intStack := &Stack[int]{}
	intStack.Push(100)
	intStack.Push(200)

	val, _ := intStack.Pop()
	fmt.Println("Int stackdan:", val)

	strStack := &Stack[string]{}
	strStack.Push("Birinchi")
	strVal, _ := strStack.Pop()
	fmt.Println("String stackdan:", strVal)
}
```

## Tushuntirish va Mantiq:
Bitta generik struktura orqali int, string yoki maxsus strukturalar uchun alohida stek yozish zarurati yo'qoladi.

## Ishlash natijasi:
```text
Int stackdan: 200
String stackdan: Birinchi
```

# 562-Topshiriq: Generik Navbat (Queue[T]) tuzilmasi
## Topshiriq sharti:
FIFO tamoyilidagi generik navbat tizimini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Queue[T any] struct {
	data []T
}

func (q *Queue[T]) Enqueue(item T) {
	q.data = append(q.data, item)
}

func (q *Queue[T]) Dequeue() (T, bool) {
	if len(q.data) == 0 {
		var zero T
		return zero, false
	}
	birinchi := q.data[0]
	q.data = q.data[1:]
	return birinchi, true
}

func main() {
	navbat := &Queue[string]{}
	navbat.Enqueue("Mijoz 1")
	navbat.Enqueue("Mijoz 2")

	m, _ := navbat.Dequeue()
	fmt.Println("Xizmat ko'rsatildi:", m)
}
```

## Tushuntirish va Mantiq:
Generik `Queue[T]` har qanday turdagi vazifalar navbatini tur xavfsiz boshqaradi.

## Ishlash natijasi:
```text
Xizmat ko'rsatildi: Mijoz 1
```

# 563-Topshiriq: Generik Kesh xaritasi: Cache[K comparable, V any]
## Topshiriq sharti:
Kaliti va qiymati generik bo'lgan tur-xavfsiz xotira keshini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Cache[K comparable, V any] struct {
	baza map[K]V
}

func NewCache[K comparable, V any]() *Cache[K, V] {
	return &Cache[K, V]{baza: make(map[K]V)}
}

func (c *Cache[K, V]) Set(k K, v V) {
	c.baza[k] = v
}

func (c *Cache[K, V]) Get(k K) (V, bool) {
	val, ok := c.baza[k]
	return val, ok
}

func main() {
	kesh := NewCache[string, int]()
	kesh.Set("harorat", 24)

	t, _ := kesh.Get("harorat")
	fmt.Println("O'qilgan harorat:", t)
}
```

## Tushuntirish va Mantiq:
`[K comparable, V any]` kalitning xesh-jadval talablariga mosligini kafolatlaydi, qiymat esa erkin tanlanadi.

## Ishlash natijasi:
```text
O'qilgan harorat: 24
```

# 564-Topshiriq: Generik To'plam (Set[T comparable]) ma'lumot tuzilmasi
## Topshiriq sharti:
Dublikatsiz elementlarni saqlovchi generik Set yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Set[T comparable] struct {
	elementlar map[T]struct{}
}

func NewSet[T comparable]() *Set[T] {
	return &Set[T]{elementlar: make(map[T]struct{})}
}

func (s *Set[T]) Add(val T) {
	s.elementlar[val] = struct{}{}
}

func (s *Set[T]) Contains(val T) bool {
	_, ok := s.elementlar[val]
	return ok
}

func main() {
	set := NewSet[int]()
	set.Add(10)
	set.Add(20)

	fmt.Println("10 bormi:", set.Contains(10))
	fmt.Println("30 bormi:", set.Contains(30))
}
```

## Tushuntirish va Mantiq:
Generik Set int, string va boshqa barcha taqqoslanuvchi turlar uchun mukammal ishlaydi.

## Ishlash natijasi:
```text
10 bormi: true
30 bormi: false
```

# 565-Topshiriq: Type Inference (Turni avtomatik aniqlash) qanday ishlaydi?
## Topshiriq sharti:
Kompilyator argument qiymatlariga qarab generik turni o'zi topishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func Juftlik[T any](a, b T) []T {
	return []T{a, b}
}

func main() {
	// 1. Ochiq ko'rsatish (Explicit):
	res1 := Juftlik[int](10, 20)

	// 2. Avtomatik aniqlash (Type inference):
	res2 := Juftlik("Salom", "Dunyo")

	fmt.Println("res1:", res1)
	fmt.Println("res2:", res2)
}
```

## Tushuntirish va Mantiq:
Go kompilyatori uzatilgan argumentlardan parametr turini o'zi aniqlay oladi, shuning uchun `[int]` deb yozish ko'p hollarda shart emas.

## Ishlash natijasi:
```text
res1: [10 20]
res2: [Salom Dunyo]
```

# 566-Topshiriq: Generik Interfeyslar: Repository[T any]
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash uchun umumiy generik repozitoriy interfeysini e'lon qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Repository[T any] interface {
	Save(item T) error
	GetByID(id int) (T, bool)
}

type Mahsulot struct {
	ID   int
	Nomi string
}

type MahsulotRepo struct {
	baza map[int]Mahsulot
}

func (m *MahsulotRepo) Save(item Mahsulot) error {
	m.baza[item.ID] = item
	return nil
}

func (m *MahsulotRepo) GetByID(id int) (Mahsulot, bool) {
	val, ok := m.baza[id]
	return val, ok
}

func main() {
	var repo Repository[Mahsulot] = &MahsulotRepo{baza: make(map[int]Mahsulot)}
	_ = repo.Save(Mahsulot{ID: 1, Nomi: "Planshet"})

	item, _ := repo.GetByID(1)
	fmt.Printf("Topildi: %+v\n", item)
}
```

## Tushuntirish va Mantiq:
Generik interfeyslar Clean Architecture repozitoriylarini bir xil andozada modellashtirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Topildi: {ID:1 Nomi:Planshet}
```

# 567-Topshiriq: Go da Metodlar Generik Bo'la Olmasligi cheklovi va uning yechimi
## Topshiriq sharti:
Nima uchun metod o'zining mustaqil tip parametriga ega bo'la olmasligini va buni qanday chetlab o'tishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Quti[T any] struct {
	Qiymat T
}

// XATO: func (q Quti[T]) Transform[R any](f func(T) R) R // Go da taqiqlangan!
// TO'G'RI YECHIM: Oddiy generik funksiya ishlatish:
func TransformQuti[T, R any](q Quti[T], f func(T) R) R {
	return f(q.Qiymat)
}

func main() {
	q := Quti[int]{Qiymat: 42}
	satr := TransformQuti(q, func(n int) string {
		return fmt.Sprintf("Qiymat: %d", n)
	})

	fmt.Println(satr)
}
```

## Tushuntirish va Mantiq:
Go interfeys jadvallari (itab) ning haddan tashqari kattalashib ketmasligi uchun metod darajasida yangi tip parametrlariga ruxsat bermagan. O'rniga oddiy funksiyalar ishlatiladi.

## Ishlash natijasi:
```text
Qiymat: 42
```

# 568-Topshiriq: Generik Pair / Tuple tuzilmasi: Pair[T, U any]
## Topshiriq sharti:
Turli turdagi ikkita qiymatni birlashtiruvchi generik juftlik yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Pair[T, U any] struct {
	Birinchi T
	Ikkinchi U
}

func main() {
	p := Pair[string, int]{Birinchi: "Baho", Ikkinchi: 95}
	fmt.Printf("Juftlik: %s -> %d\n", p.Birinchi, p.Ikkinchi)
}
```

## Tushuntirish va Mantiq:
`Pair[T, U]` ikki xil turdagi qiymatlarni bitta ixcham obyektdan qaytarish uchun qulaydir.

## Ishlash natijasi:
```text
Juftlik: Baho -> 95
```

# 569-Topshiriq: Generik Option / Maybe turi: Option[T]
## Topshiriq sharti:
Qiymat mavjud yoki yo'qligini xavfsiz ifodalovchi Option turini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Option[T any] struct {
	qiymat   T
	mavjudmi bool
}

func Some[T any](val T) Option[T] {
	return Option[T]{qiymat: val, mavjudmi: true}
}

func None[T any]() Option[T] {
	return Option[T]{mavjudmi: false}
}

func (o Option[T]) Get() (T, bool) {
	return o.qiymat, o.mavjudmi
}

func main() {
	o1 := Some("Salom")
	o2 := None[string]()

	v1, ok1 := o1.Get()
	fmt.Printf("o1: %s (bor: %t)\n", v1, ok1)

	_, ok2 := o2.Get()
	fmt.Printf("o2 mavjudmi: %t\n", ok2)
}
```

## Tushuntirish va Mantiq:
Option turi nil ko'rsatkichlar xavfisiz qiymatning mavjudligini kafolatlaydi.

## Ishlash natijasi:
```text
o1: Salom (bor: true)
o2 mavjudmi: false
```

# 570-Topshiriq: Generik Keys va Values funksiyalari (Map dan slice ajratish)
## Topshiriq sharti:
Har qanday mapdan barcha kalitlar va barcha qiymatlar slicesini generik orqali oling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func MapKeys[K comparable, V any](m map[K]V) []K {
	kalitlar := make([]K, 0, len(m))
	for k := range m {
		kalitlar = append(kalitlar, k)
	}
	return kalitlar
}

func main() {
	narxlar := map[string]int{"olma": 5000, "anor": 12000}
	kalitlar := MapKeys(narxlar)

	fmt.Println("Map kalitlari:", kalitlar)
}
```

## Tushuntirish va Mantiq:
Generik yordamida barcha turdagi xaritalar uchun bitta umumiy `MapKeys` funksiyasi yetarlidir.

## Ishlash natijasi:
```text
Map kalitlari: [olma anor]
```

# 571-Topshiriq: Generik Deduplicate / Distinct funksiyasi
## Topshiriq sharti:
Sliceda takrorlangan elementlarni generik orqali tozalang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func Distinct[T comparable](s []T) []T {
	korilgan := make(map[T]struct{})
	var natija []T

	for _, item := range s {
		if _, ok := korilgan[item]; !ok {
			korilgan[item] = struct{}{}
			natija = append(natija, item)
		}
	}
	return natija
}

func main() {
	sonlar := []int{1, 2, 2, 3, 1, 4}
	fmt.Println("Noyob sonlar:", Distinct(sonlar))

	sozlar := []string{"go", "rust", "go", "python"}
	fmt.Println("Noyob so'zlar:", Distinct(sozlar))
}
```

## Tushuntirish va Mantiq:
`Distinct[T comparable]` xesh-to'plam yordamida O(N) vaqtda dublikatlarni tozalaydi.

## Ishlash natijasi:
```text
Noyob sonlar: [1 2 3 4]
Noyob so'zlar: [go rust python]
```

# 572-Topshiriq: Generik Bog'langan Ro'yxat (LinkedList[T])
## Topshiriq sharti:
Har qanday turdagi qiymatlarni saqlay oluvchi bittalik zanjirli ro'yxat tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Node[T any] struct {
	Val  T
	Next *Node[T]
}

type LinkedList[T any] struct {
	Head *Node[T]
}

func (l *LinkedList[T]) Add(val T) {
	newNode := &Node[T]{Val: val, Next: l.Head}
	l.Head = newNode
}

func main() {
	ll := &LinkedList[string]{}
	ll.Add("O'zbekiston")
	ll.Add("Salom")

	fmt.Println("Ro'yxat boshi:", ll.Head.Val)
	fmt.Println("Keyingi element:", ll.Head.Next.Val)
}
```

## Tushuntirish va Mantiq:
Tugunlar va ro'yxat generik tur bilan parametrlanadi va to'liq tur xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
Ro'yxat boshi: Salom
Keyingi element: O'zbekiston
```

# 573-Topshiriq: Generik Binar Qidiruv Daraxti (BST[T cmp.Ordered])
## Topshiriq sharti:
Tartiblangan generik daraxt tuzilmasini yarating.

## Yechim (Go kodi):
```go
package main

import (
	"cmp"
	"fmt"
)

type BSTNode[T cmp.Ordered] struct {
	Val   T
	Left  *BSTNode[T]
	Right *BSTNode[T]
}

func Insert[T cmp.Ordered](root *BSTNode[T], val T) *BSTNode[T] {
	if root == nil {
		return &BSTNode[T]{Val: val}
	}
	if val < root.Val {
		root.Left = Insert(root.Left, val)
	} else {
		root.Right = Insert(root.Right, val)
	}
	return root
}

func main() {
	var root *BSTNode[int]
	root = Insert(root, 50)
	root = Insert(root, 30)

	fmt.Printf("Ildiz: %d, Chap bola: %d\n", root.Val, root.Left.Val)
}
```

## Tushuntirish va Mantiq:
`cmp.Ordered` cheklovi tufayli BST int, float yoki string turlarida bir xil ishlaydi.

## Ishlash natijasi:
```text
Ildiz: 50, Chap bola: 30
```

# 574-Topshiriq: Generik Chunking: Katta sliceni bo'laklarga ajratish
## Topshiriq sharti:
Har qanday turdagi sliceni K o'lchamli qismlarga bo'luvchi generik funksiya.

## Yechim (Go kodi):
```go
package main

import "fmt"

func Chunk[T any](s []T, size int) [][]T {
	var natija [][]T
	for i := 0; i < len(s); i += size {
		end := i + size
		if end > len(s) {
			end = len(s)
		}
		natija = append(natija, s[i:end])
	}
	return natija
}

func main() {
	raqamlar := []int{1, 2, 3, 4, 5, 6, 7}
	fmt.Println("Bo'laklar:", Chunk(raqamlar, 3))
}
```

## Tushuntirish va Mantiq:
Batch processing uchun eng ko'p ishlatiluvchi generik yordamchi funksiyalardan biridir.

## Ishlash natijasi:
```text
Bo'laklar: [[1 2 3] [4 5 6] [7]]
```

# 575-Topshiriq: Generik Find: Shart bo'yicha birinchi mos elementni topish
## Topshiriq sharti:
Sliceda predikat funksiyaga mos keluvchi birinchi elementni toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

func Find[T any](s []T, shart func(T) bool) (T, bool) {
	for _, item := range s {
		if shart(item) {
			return item, true
		}
	}
	var zero T
	return zero, false
}

func main() {
	ismlar := []string{"Bobur", "Jasur", "Madina"}

	topildi, ok := Find(ismlar, func(nom string) bool {
		return len(nom) > 5
	})

	fmt.Printf("5 tadan uzun ism: %s (topildi: %t)\n", topildi, ok)
}
```

## Tushuntirish va Mantiq:
Element topilmasa turning nol qiymati va `false` qaytariladi.

## Ishlash natijasi:
```text
5 tadan uzun ism: Madina (topildi: true)
```

# 576-Topshiriq: Generik MergeMaps funksiyasi
## Topshiriq sharti:
Ikkita generik mapni bir-biriga birlashtiruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func MergeMaps[K comparable, V any](m1, m2 map[K]V) map[K]V {
	natija := make(map[K]V)
	for k, v := range m1 {
		natija[k] = v
	}
	for k, v := range m2 {
		natija[k] = v
	}
	return natija
}

func main() {
	a := map[string]int{"x": 1, "y": 2}
	b := map[string]int{"y": 20, "z": 3}

	fmt.Println("Birlashtirilgan map:", MergeMaps(a, b))
}
```

## Tushuntirish va Mantiq:
Generik `MergeMaps` har qanday kalit va qiymat turidagi xaritalarni toza birlashtiradi.

## Ishlash natijasi:
```text
Birlashtirilgan map: map[x:1 y:20 z:3]
```

# 577-Topshiriq: Generik InvertMap: Kalit va qiymat o'rnini almashtirish
## Topshiriq sharti:
Qiymati ham `comparable` bo'lgan mapni teskarisiga o'giruvchi funksiya.

## Yechim (Go kodi):
```go
package main

import "fmt"

func InvertMap[K, V comparable](m map[K]V) map[V]K {
	res := make(map[V]K, len(m))
	for k, v := range m {
		res[v] = k
	}
	return res
}

func main() {
	shaharlar := map[string]int{"Toshkent": 1, "Samarqand": 2}
	fmt.Println("Teskari map:", InvertMap(shaharlar))
}
```

## Tushuntirish va Mantiq:
`[K, V comparable]` har ikkala tomonning ham taqqoslanuvchi bo'lishini talab qiladi.

## Ishlash natijasi:
```text
Teskari map: map[1:Toshkent 2:Samarqand]
```

# 578-Topshiriq: Generik GroupBy funksiyasi
## Topshiriq sharti:
Kolleksiya elementlarini berilgan kalit funksiyasi bo'yicha guruhlovchi generik yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func GroupBy[T any, K comparable](items []T, keyFn func(T) K) map[K][]T {
	guruhlar := make(map[K][]T)
	for _, item := range items {
		kalit := keyFn(item)
		guruhlar[kalit] = append(guruhlar[kalit], item)
	}
	return guruhlar
}

func main() {
	sozlar := []string{"olma", "anor", "behi", "nok", "shaftoli"}

	// Uzunligi bo'yicha guruhlash:
	uzunlikBoyicha := GroupBy(sozlar, func(s string) int { return len(s) })

	for uz, g := range uzunlikBoyicha {
		fmt.Printf("Uzunlik %d: %v\n", uz, g)
	}
}
```

## Tushuntirish va Mantiq:
Generik `GroupBy` ixtiyoriy mezonlar bo'yicha ma'lumotlarni tasniflaydi.

## Ishlash natijasi:
```text
Uzunlik 4: [olma anor behi]
Uzunlik 3: [nok]
Uzunlik 8: [shaftoli]
```

# 579-Topshiriq: Generik Binar Qidiruv (BinarySearch[T cmp.Ordered])
## Topshiriq sharti:
Tartiblangan har qanday turdagi massivda binar qidiruv algoritmi.

## Yechim (Go kodi):
```go
package main

import (
	"cmp"
	"fmt"
)

func GenericBinarySearch[T cmp.Ordered](arr []T, target T) int {
	chap, ong := 0, len(arr)-1

	for chap <= ong {
		orta := chap + (ong-chap)/2
		if arr[orta] == target {
			return orta
		}
		if arr[orta] < target {
			chap = orta + 1
		} else {
			ong = orta - 1
		}
	}
	return -1
}

func main() {
	sonlar := []int{10, 20, 30, 40, 50}
	fmt.Println("30 indeksi:", GenericBinarySearch(sonlar, 30))

	harflar := []string{"a", "b", "c", "d"}
	fmt.Println("'c' indeksi:", GenericBinarySearch(harflar, "c"))
}
```

## Tushuntirish va Mantiq:
Bitta algoritm barcha tartiblanuvchi turlar uchun O(log N) tezlikda ishlaydi.

## Ishlash natijasi:
```text
30 indeksi: 2
'c' indeksi: 2
```

# 580-Topshiriq: Generik Aylana Bufer: RingBuffer[T]
## Topshiriq sharti:
Cheklangan sig'imli generik aylanma xotira buferi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type RingBuffer[T any] struct {
	data []T
	size int
	pos  int
	full bool
}

func NewRingBuffer[T any](size int) *RingBuffer[T] {
	return &RingBuffer[T]{data: make([]T, size), size: size}
}

func (r *RingBuffer[T]) Push(item T) {
	r.data[r.pos] = item
	r.pos = (r.pos + 1) % r.size
	if r.pos == 0 {
		r.full = true
	}
}

func main() {
	rb := NewRingBuffer[string](2)
	rb.Push("A")
	rb.Push("B")
	rb.Push("C") // A o'rniga yoziladi

	fmt.Printf("Buferdagi data: %v\n", rb.data)
}
```

## Tushuntirish va Mantiq:
Generik RingBuffer xotirada so'nggi ma'lumotlarni saqlashda har qanday tur uchun moslashadi.

## Ishlash natijasi:
```text
Buferdagi data: [C B]
```

# 581-Topshiriq: Generik Worker Pool vazifalar navbati (Task[T, R])
## Topshiriq sharti:
Kiruvchi T va chiquvchi R turlariga ega parallel vazifa ishlovchi tizim.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Task[T, R any] struct {
	Input  T
	Action func(T) R
}

func (t Task[T, R]) Execute() R {
	return t.Action(t.Input)
}

func main() {
	vazifa := Task[int, string]{
		Input: 100,
		Action: func(n int) string {
			return fmt.Sprintf("Natija: %d", n*2)
		},
	}

	fmt.Println(vazifa.Execute())
}
```

## Tushuntirish va Mantiq:
Generik vazifalar har xil kirish-chiqish turlari bilan asinxron konveyerlarni boshqaradi.

## Ishlash natijasi:
```text
Natija: 200
```

# 582-Topshiriq: Generik Atomic Pointer (sync/atomic.Pointer[T])
## Topshiriq sharti:
Go 1.19+ generik atomik ko'rsatkichi bilan qulfsiz holat almashish.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type ServerConfig struct {
	Port int
}

func main() {
	var ptr atomic.Pointer[ServerConfig]

	ptr.Store(&ServerConfig{Port: 8080})
	fmt.Println("Boshlang'ich port:", ptr.Load().Port)

	ptr.Store(&ServerConfig{Port: 9090})
	fmt.Println("Yangilangan port:", ptr.Load().Port)
}
```

## Tushuntirish va Mantiq:
`atomic.Pointer[T]` orqali har qanday struktura ko'rsatkichini qulfsiz xavfsiz yangilash mumkin.

## Ishlash natijasi:
```text
Boshlang'ich port: 8080
Yangilangan port: 9090
```

# 583-Topshiriq: Generik Sync.Pool o'rami (Type-Safe Object Pool)
## Topshiriq sharti:
Standart `sync.Pool` ning `any` turini xavfsiz generik qolip bilan o'rab chiqing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type GenericPool[T any] struct {
	pool sync.Pool
}

func NewGenericPool[T any](newFn func() T) *GenericPool[T] {
	return &GenericPool[T]{
		pool: sync.Pool{
			New: func() any { return newFn() },
		},
	}
}

func (p *GenericPool[T]) Get() T {
	return p.pool.Get().(T)
}

func (p *GenericPool[T]) Put(item T) {
	p.pool.Put(item)
}

func main() {
	pool := NewGenericPool(func() []byte {
		return make([]byte, 1024)
	})

	bufer := pool.Get()
	fmt.Printf("Olingan bufer hajmi: %d bayt\n", len(bufer))
	pool.Put(bufer)
}
```

## Tushuntirish va Mantiq:
Xavfsiz generik o'ram type assertion yozish zaruratini butunlay yo'qotadi.

## Ishlash natijasi:
```text
Olingan bufer hajmi: 1024 bayt
```

# 584-Topshiriq: Generik Event Bus (Hodisalar shinasi)
## Topshiriq sharti:
T turidagi voqealarni tarqatuvchi tur-xavfsiz hodisa boshqaruvchisi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type EventBus[T any] struct {
	handlers []func(T)
}

func (b *EventBus[T]) Subscribe(h func(T)) {
	b.handlers = append(b.handlers, h)
}

func (b *EventBus[T]) Publish(event T) {
	for _, h := range b.handlers {
		h(event)
	}
}

func main() {
	bus := &EventBus[string]{}
	bus.Subscribe(func(msg string) { fmt.Println("Handler 1:", msg) })
	bus.Publish("Tizim yangilandi")
}
```

## Tushuntirish va Mantiq:
Generik EventBus xabarlar turlarini kompilyatsiya bosqichidayoq qat'iy nazorat qiladi.

## Ishlash natijasi:
```text
Handler 1: Tizim yangilandi
```

# 585-Topshiriq: Generik Konveyer (Pipeline[T])
## Topshiriq sharti:
Ma'lumotlar oqimini bir necha generik bosqichlardan o'tkazuvchi tizim.

## Yechim (Go kodi):
```go
package main

import "fmt"

type PipeStage[T any] func(T) T

func RunPipeline[T any](input T, stages ...PipeStage[T]) T {
	res := input
	for _, stage := range stages {
		res = stage(res)
	}
	return res
}

func main() {
	natija := RunPipeline(5,
		func(n int) int { return n * 2 },
		func(n int) int { return n + 10 },
	)
	fmt.Println("(5 * 2) + 10 =", natija)
}
```

## Tushuntirish va Mantiq:
Pipeline bosqichlari umumiy generik tur orqali xavfsiz ulanadi.

## Ishlash natijasi:
```text
(5 * 2) + 10 = 20
```

# 586-Topshiriq: Generik Pagination modeli: PagedResult[T any]
## Topshiriq sharti:
Har qanday turdagi ma'lumotlar ro'yxatini sahifalash konteyneriga joylang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type PagedResult[T any] struct {
	Items      []T `json:"items"`
	Page       int `json:"page"`
	TotalItems int `json:"total_items"`
}

func main() {
	natija := PagedResult[string]{
		Items:      []string{"Toshkent", "Buxoro"},
		Page:       1,
		TotalItems: 14,
	}

	fmt.Printf("Sahifa %d, elementlar: %v\n", natija.Page, natija.Items)
}
```

## Tushuntirish va Mantiq:
REST API larida foydalanuvchilar, mahsulotlar va buyurtmalar uchun bitta umumiy sahifalash modeli xizmat qiladi.

## Ishlash natijasi:
```text
Sahifa 1, elementlar: [Toshkent Buxoro]
```

# 587-Topshiriq: Generik API Response: APIResponse[T any]
## Topshiriq sharti:
Muvaffaqiyatli ma'lumot yukini tur xavfsiz qaytaruvchi API javob qolipi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type APIResponse[T any] struct {
	Success bool   `json:"success"`
	Data    T      `json:"data"`
	Error   string `json:"error,omitempty"`
}

func Success[T any](data T) APIResponse[T] {
	return APIResponse[T]{Success: true, Data: data}
}

func main() {
	resp := Success(map[string]int{"hisob": 500})
	fmt.Printf("API Natijasi: %+v\n", resp)
}
```

## Tushuntirish va Mantiq:
`any` o'rniga aniq `T` parametri qo'yilganda mijoz kodi xavfsiz va aniq turga ega bo'ladi.

## Ishlash natijasi:
```text
API Natijasi: {Success:true Data:map[hisob:500] Error:}
```

# 588-Topshiriq: Generik 2D Matritsa: Matrix[T Number]
## Topshiriq sharti:
Faqat sonli turlarda ishlaydigan generik matritsa strukturasini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Number interface {
	~int | ~float64
}

type Matrix[T Number] struct {
	rows, cols int
	data       [][]T
}

func NewMatrix[T Number](r, c int) *Matrix[T] {
	d := make([][]T, r)
	for i := range d {
		d[i] = make([]T, c)
	}
	return &Matrix[T]{rows: r, cols: c, data: d}
}

func (m *Matrix[T]) Set(r, c int, val T) {
	m.data[r][c] = val
}

func main() {
	mat := NewMatrix[float64](2, 2)
	mat.Set(0, 0, 1.5)
	fmt.Printf("Matritsa [0,0] elementi: %.1f\n", mat.data[0][0])
}
```

## Tushuntirish va Mantiq:
Matematik hisob-kitoblar generiklar orqali int yoki float uchun alohida nusxalarsiz yoziladi.

## Ishlash natijasi:
```text
Matritsa [0,0] elementi: 1.5
```

# 589-Topshiriq: Generik LRU Kesh: LRUCache[K comparable, V any]
## Topshiriq sharti:
Tur-xavfsiz va eng uzoq ishlatilmagan elementni tozalovchi kesh tizimi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type LRUCache[K comparable, V any] struct {
	capacity int
	cache    map[K]V
	keys     []K
}

func NewLRU[K comparable, V any](cap int) *LRUCache[K, V] {
	return &LRUCache[K, V]{capacity: cap, cache: make(map[K]V)}
}

func (c *LRUCache[K, V]) Put(k K, v V) {
	if len(c.cache) >= c.capacity {
		oldest := c.keys[0]
		c.keys = c.keys[1:]
		delete(c.cache, oldest)
	}
	c.cache[k] = v
	c.keys = append(c.keys, k)
}

func main() {
	lru := NewLRU[string, int](2)
	lru.Put("bir", 1)
	lru.Put("ikki", 2)
	lru.Put("uch", 3) // "bir" o'chiriladi

	_, ok := lru.cache["bir"]
	fmt.Println("'bir' bormi:", ok)
}
```

## Tushuntirish va Mantiq:
Generik LRU kesh har qanday kalit va qiymat juftliklarida type assertion talab qilmasdan ishlaydi.

## Ishlash natijasi:
```text
'bir' bormi: false
```

# 590-Topshiriq: Generik FlatMap funksiyasi
## Topshiriq sharti:
Elementlarni yangi slicelarga o'girib, ularni bitta tekis massivga yig'ish.

## Yechim (Go kodi):
```go
package main

import "fmt"

func FlatMap[T, R any](items []T, f func(T) []R) []R {
	var natija []R
	for _, item := range items {
		natija = append(natija, f(item)...)
	}
	return natija
}

func main() {
	matnlar := []string{"Go til", "yaxshi til"}

	// So'zlarga ajratish:
	sozlar := FlatMap(matnlar, func(s string) []string {
		return []string{s + "!"}
	})

	fmt.Println("FlatMap natijasi:", sozlar)
}
```

## Tushuntirish va Mantiq:
`FlatMap` ma'lumotlarni o'zgartirish va bir vaqtda tekislash (flatten) uchun xizmat qiladi.

## Ishlash natijasi:
```text
FlatMap natijasi: [Go til! yaxshi til!]
```

# 591-Topshiriq: Generik Prioritetli Navbat (Min-Heap sodda modeli)
## Topshiriq sharti:
Tartiblangan eng kichik elementni birinchi chiqaruvchi generik tuzilma.

## Yechim (Go kodi):
```go
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type MinHeap[T cmp.Ordered] struct {
	items []T
}

func (h *MinHeap[T]) Push(v T) {
	h.items = append(h.items, v)
	slices.Sort(h.items) // Sodda ko'rinish
}

func (h *MinHeap[T]) PopMin() (T, bool) {
	if len(h.items) == 0 {
		var zero T
		return zero, false
	}
	minVal := h.items[0]
	h.items = h.items[1:]
	return minVal, true
}

func main() {
	heap := &MinHeap[int]{}
	heap.Push(45)
	heap.Push(12)
	heap.Push(89)

	m, _ := heap.PopMin()
	fmt.Println("Eng kichik element:", m)
}
```

## Tushuntirish va Mantiq:
Generik Heap orqali vazifalar ularning prioritetiga ko'ra avtomatik tartibda olinadi.

## Ishlash natijasi:
```text
Eng kichik element: 12
```

# 592-Topshiriq: Generik Clamp funksiyasi: Qiymatni chegaralar oralig'ida ushlab qolish
## Topshiriq sharti:
Qiymatni Min va Max oralig'ida cheklovchi generik algoritm.

## Yechim (Go kodi):
```go
package main

import (
	"cmp"
	"fmt"
)

func Clamp[T cmp.Ordered](val, minVal, maxVal T) T {
	if val < minVal {
		return minVal
	}
	if val > maxVal {
		return maxVal
	}
	return val
}

func main() {
	fmt.Println("Clamp(15, 0, 10):", Clamp(15, 0, 10))
	fmt.Println("Clamp(-5, 0, 10):", Clamp(-5, 0, 10))
	fmt.Println("Clamp(7, 0, 10):", Clamp(7, 0, 10))
}
```

## Tushuntirish va Mantiq:
`Clamp` sonlarni belgilangan xavfsiz diapazonda ushlab qolish uchun barcha sonli turlarda ishlaydi.

## Ishlash natijasi:
```text
Clamp(15, 0, 10): 10
Clamp(-5, 0, 10): 0
Clamp(7, 0, 10): 7
```

# 593-Topshiriq: Generik All va Any predikat funksiyalari
## Topshiriq sharti:
Barcha elementlar yoki kamida bittasi shartni qanoatlantirishini tekshiruvchi generiklar.

## Yechim (Go kodi):
```go
package main

import "fmt"

func All[T any](s []T, p func(T) bool) bool {
	for _, v := range s {
		if !p(v) {
			return false
		}
	}
	return true
}

func Any[T any](s []T, p func(T) bool) bool {
	for _, v := range s {
		if p(v) {
			return true
		}
	}
	return false
}

func main() {
	musbatlar := []int{2, 4, 6, 8}
	fmt.Println("Hammasi juftmi:", All(musbatlar, func(n int) bool { return n%2 == 0 }))
	fmt.Println("Kamida bittasi 5 dan kattami:", Any(musbatlar, func(n int) bool { return n > 5 }))
}
```

## Tushuntirish va Mantiq:
Matematik mantiqdagi barcha (forall) va mavjud (exists) amallari generik tarzda ifodalanadi.

## Ishlash natijasi:
```text
Hammasi juftmi: true
Kamida bittasi 5 dan kattami: true
```

# 594-Topshiriq: Generik Zip funksiyasi (Ikki sliceni juftliklarga birlashtirish)
## Topshiriq sharti:
Ikki massivni parallel birlashtirib `[]Pair[T, U]` hosil qiluvchi generik.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Pair[T, U any] struct {
	A T
	B U
}

func Zip[T, U any](a []T, b []U) []Pair[T, U] {
	minLen := len(a)
	if len(b) < minLen {
		minLen = len(b)
	}
	res := make([]Pair[T, U], minLen)
	for i := 0; i < minLen; i++ {
		res[i] = Pair[T, U]{A: a[i], B: b[i]}
	}
	return res
}

func main() {
	shaharlar := []string{"Toshkent", "Samarqand"}
	kodlar := []int{71, 66}

	juftliklar := Zip(shaharlar, kodlar)
	fmt.Printf("Zip natijasi: %+v\n", juftliklar)
}
```

## Tushuntirish va Mantiq:
`Zip` massivlarni parallel bog'lashda yuqori qulaylik beradi.

## Ishlash natijasi:
```text
Zip natijasi: [{A:Toshkent B:71} {A:Samarqand B:66}]
```

# 595-Topshiriq: Generik ToAnySlice funksiyasi
## Topshiriq sharti:
Aniq turdagi `[]T` sliceni `[]any` ga o'tkazuvchi generik yordamchi.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ToAnySlice[T any](s []T) []any {
	res := make([]any, len(s))
	for i, v := range s {
		res[i] = v
	}
	return res
}

func main() {
	sonlar := []int{1, 2, 3}
	anySlice := ToAnySlice(sonlar)

	fmt.Printf("Any slice: %v (uzunligi: %d)\n", anySlice, len(anySlice))
}
```

## Tushuntirish va Mantiq:
Go da `[]int` ni to'g'ridan-to'g'ri `[]any` ga kasting qilib bo'lmaydi (chunki xotira tartibi boshqacha). Generik funksiya buni xavfsiz o'giradi.

## Ishlash natijasi:
```text
Any slice: [1 2 3] (uzunligi: 3)
```

# 596-Topshiriq: Generik EqualBy funksiyasi: Maxsus taqqoslovchi bilan tenglik
## Topshiriq sharti:
Elementlarni maxsus funksiya orqali solishtirib ikkita sliceni tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func EqualBy[T, U any](s1 []T, s2 []U, eq func(T, U) bool) bool {
	if len(s1) != len(s2) {
		return false
	}
	for i := range s1 {
		if !eq(s1[i], s2[i]) {
			return false
		}
	}
	return true
}

func main() {
	sonlar := []int{1, 2, 3}
	satrlar := []string{"1", "2", "3"}

	tengmi := EqualBy(sonlar, satrlar, func(n int, s string) bool {
		return fmt.Sprintf("%d", n) == s
	})

	fmt.Println("Tengmi:", tengmi)
}
```

## Tushuntirish va Mantiq:
`EqualBy` turli turlardagi slicelarni maxsus taqqoslash mantig'i bilan solishtirishga imkon beradi.

## Ishlash natijasi:
```text
Tengmi: true
```

# 597-Topshiriq: Generik Interfeyslar Kompozitsiyasi
## Topshiriq sharti:
Bir nechta generik interfeyslarni birlashtirish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Reader[T any] interface {
	ReadItem() T
}

type Writer[T any] interface {
	WriteItem(T)
}

type ReadWriter[T any] interface {
	Reader[T]
	Writer[T]
}

type Quti[T any] struct {
	data T
}

func (q *Quti[T]) ReadItem() T     { return q.data }
func (q *Quti[T]) WriteItem(val T) { q.data = val }

func main() {
	var rw ReadWriter[string] = &Quti[string]{}
	rw.WriteItem("Generik interfeys kompozitsiyasi!")
	fmt.Println(rw.ReadItem())
}
```

## Tushuntirish va Mantiq:
Generik interfeyslar kompozitsiyasi ma'lumotlar oqimini to'liq tur xavfsizligi bilan ta'minlaydi.

## Ishlash natijasi:
```text
Generik interfeys kompozitsiyasi!
```

# 598-Topshiriq: Generik Coalesce (Birinchi noldan farqli qiymatni topish)
## Topshiriq sharti:
Uzatilgan qiymatlardan birinchi nol bo'lmaganini tanlab oluvchi funksiya.

## Yechim (Go kodi):
```go
package main

import "fmt"

func Coalesce[T comparable](qiymatlar ...T) T {
	var zero T
	for _, q := range qiymatlar {
		if q != zero {
			return q
		}
	}
	return zero
}

func main() {
	fmt.Println("Satr Coalesce:", Coalesce("", "", "Standart Qiymat", "Zaxira"))
	fmt.Println("Son Coalesce:", Coalesce(0, 0, 42, 100))
}
```

## Tushuntirish va Mantiq:
SQL dagi `COALESCE` funksiyasining Go dagi generik toza muqobilidir.

## Ishlash natijasi:
```text
Satr Coalesce: Standart Qiymat
Son Coalesce: 42
```

# 599-Topshiriq: Generik Interfeys orqali Mock Factory
## Topshiriq sharti:
Testlar uchun generik xizmat obyektlarini yasovchi andoza.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Service[T any] interface {
	Process(T) string
}

type MockService[T any] struct {
	Res string
}

func (m MockService[T]) Process(T) string {
	return m.Res
}

func main() {
	var s Service[int] = MockService[int]{Res: "Mock qilingan natija"}
	fmt.Println(s.Process(10))
}
```

## Tushuntirish va Mantiq:
Generik Mock servicelar test yozish jarayonini bir necha barobar qisqartiradi.

## Ishlash natijasi:
```text
Mock qilingan natija
```

# 600-Topshiriq: Yakuniy amaliy vazifa: To'liq Type-Safe Linq/Stream Ma'lumotlar Oqimi Kutubxonasi
## Topshiriq sharti:
Generik `Stream[T]` zanjiri: Filter, Map, Sort va Collect metodlari bilan funksional oqim tizimi.

## Yechim (Go kodi):
```go
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type Stream[T any] struct {
	items []T
}

func From[T any](items []T) *Stream[T] {
	return &Stream[T]{items: items}
}

func (s *Stream[T]) Filter(p func(T) bool) *Stream[T] {
	var filtered []T
	for _, it := range s.items {
		if p(it) {
			filtered = append(filtered, it)
		}
	}
	s.items = filtered
	return s
}

func (s *Stream[T]) Sort(less func(a, b T) int) *Stream[T] {
	slices.SortFunc(s.items, less)
	return s
}

func (s *Stream[T]) Collect() []T {
	return s.items
}

func main() {
	sonlar := []int{8, 3, 1, 9, 2, 6, 4, 7, 5}

	// 1. Faqat juft sonlarni filtrlaymiz
	// 2. O'sish tartibida saralaymiz
	// 3. Yakuniy natijani yig'ib olamiz
	natija := From(sonlar).
		Filter(func(n int) bool { return n%2 == 0 }).
		Sort(func(a, b int) int { return cmp.Compare(a, b) }).
		Collect()

	fmt.Println("Stream orqali qayta ishlangan natija:", natija)
}
```

## Tushuntirish va Mantiq:
Generiklar tufayli Go da Java Stream yoki C# LINQ kabi go'zal, ravon va to'liq type-safe ma'lumotlar oqimini yaratish mumkin bo'ldi.

## Ishlash natijasi:
```text
Stream orqali qayta ishlangan natija: [2 4 6 8]
```

