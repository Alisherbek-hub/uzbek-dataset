# 7-Mavzu: Ko'rsatkichlar (Pointers) va Xotira Samarasini Oshirish (301-350)

Go dasturlash tilida xotirani bevosita boshqarish vositasi: `&` (manzil olish) va `*` (dereferensiya) operatorlari, `nil` ko'rsatkichlar, xavfsiz escape analysis (stack va heap o'rtasida avtomatik taqsimlash), pointer arifmetikasining xavfsizlik uchun cheklanishi, bog'langan ro'yxatlar (Linked Lists), daraxtlar (Trees) hamda `unsafe` paketi bo'yicha 50 ta amaliy topshiriq.

# 301-Topshiriq: Ko'rsatkichlar asoslari: Xotira manzili va & operatori
## Topshiriq sharti:
O'zgaruvchining operativ xotiradagi manzilini `&` operatori va `%p` spetsifikatori orqali chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	yosh := 25

	fmt.Printf("O'zgaruvchi qiymati: %d\n", yosh)
	fmt.Printf("O'zgaruvchi xotira manzili: %p\n", &yosh)
}
```

## Tushuntirish va Mantiq:
`&` operatori (address-of) o'zgaruvchi joylashgan xotira baytining boshlang'ich manzilini qaytaradi.

## Ishlash natijasi:
```text
O'zgaruvchi qiymati: 25
O'zgaruvchi xotira manzili: 0xc000012088
```

# 302-Topshiriq: Dereferencing (Ko'rsatkich qiymatini olish) va * operatori
## Topshiriq sharti:
Ko'rsatkich orqali uning manzilidagi haqiqiy qiymatni o'qing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	son := 42
	p := &son // p - son ning xotira manzilini saqlovchi ko'rsatkich

	fmt.Printf("p ko'rsatkichi manzili: %p\n", p)
	fmt.Printf("*p orqali o'qilgan qiymat: %d\n", *p)
}
```

## Tushuntirish va Mantiq:
`*p` (dereferencing) ko'rsatkich ko'rsatib turgan manzilga borib, u yerdagi qiymatni o'qib oladi.

## Ishlash natijasi:
```text
p ko'rsatkichi manzili: 0xc000012088
*p orqali o'qilgan qiymat: 42
```

# 303-Topshiriq: Ko'rsatkich turlari: *int, *string, *bool
## Topshiriq sharti:
Turli ma'lumot turlari uchun ko'rsatkichlar e'lon qiling va ularning turlarini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var i int = 100
	var s string = "Golang"
	var b bool = true

	pInt := &i
	pStr := &s
	pBool := &b

	fmt.Printf("pInt turi: %T, qiymati: %d\n", pInt, *pInt)
	fmt.Printf("pStr turi: %T, qiymati: %s\n", pStr, *pStr)
	fmt.Printf("pBool turi: %T, qiymati: %t\n", pBool, *pBool)
}
```

## Tushuntirish va Mantiq:
Har bir ma'lumot turining o'z ko'rsatkich turi mavjud: `*T` bu `T` turidagi qiymatning xotira manzilini saqlovchi turdir.

## Ishlash natijasi:
```text
pInt turi: *int, qiymati: 100
pStr turi: *string, qiymati: Golang
pBool turi: *bool, qiymati: true
```

# 304-Topshiriq: Nil ko'rsatkich va xavfsiz tekshiruv (p != nil)
## Topshiriq sharti:
Boshlang'ich qiymat berilmagan ko'rsatkich `nil` ekanligini va uni xavfsiz tekshirishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func chopEtXavfsiz(p *int) {
	if p == nil {
		fmt.Println("[OGOHLANTIRISH] Ko'rsatkich nil, xotiraga murojaat qilib bo'lmaydi!")
		return
	}
	fmt.Printf("Qiymat: %d\n", *p)
}

func main() {
	var ptr *int
	chopEtXavfsiz(ptr)

	qiymat := 77
	ptr = &qiymat
	chopEtXavfsiz(ptr)
}
```

## Tushuntirish va Mantiq:
Ko'rsatkichning nol qiymati `nil` hisoblanadi. Xotiraga murojaat qilishdan oldin `if p != nil` tekshiruvi shart.

## Ishlash natijasi:
```text
[OGOHLANTIRISH] Ko'rsatkich nil, xotiraga murojaat qilib bo'lmaydi!
Qiymat: 77
```

# 305-Topshiriq: Nil Pointer Dereference xatosi tahlili
## Topshiriq sharti:
`nil` ko'rsatkich dereferensiya qilinganda qanday panic yuz berishini recover orqali ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("[XATO USHLANDI] Panik: %v\n", r)
		}
	}()

	var p *string
	// p nil holatda dereferensiya qilmoqchimiz:
	fmt.Println(*p)
}
```

## Tushuntirish va Mantiq:
Nil ko'rsatkichga murojaat qilish dasturni favqulodda to'xtatadi (`nil pointer dereference runtime error`).

## Ishlash natijasi:
```text
[XATO USHLANDI] Panik: runtime error: invalid memory address or nil pointer dereference
```

# 306-Topshiriq: Xotiradagi qiymatni ko'rsatkich orqali o'zgartirish (*p = yangi)
## Topshiriq sharti:
Ko'rsatkich orqali o'zgaruvchi qiymatini to'g'ridan-to'g'ri yangilang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	balans := 5000
	p := &balans

	*p = 8000 // balans ning xotirasiga borib 8000 yozamiz

	fmt.Printf("Balansning yangi qiymati: %d so'm\n", balans)
}
```

## Tushuntirish va Mantiq:
`*p = yangi_qiymat` ifodasi ko'rsatkich manzili orqali borib, asl o'zgaruvchini mutatsiya qiladi.

## Ishlash natijasi:
```text
Balansning yangi qiymati: 8000 so'm
```

# 307-Topshiriq: Funksiyaga ko'rsatkich uzatish orqali tashqi o'zgaruvchini o'zgartirish
## Topshiriq sharti:
Ko'rsatkich qabul qilib, o'zgaruvchini ikki barobar oshiruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ikkiBarobar(p *int) {
	*p = *p * 2
}

func main() {
	x := 15
	fmt.Println("Chaqirishdan oldin x:", x)

	ikkiBarobar(&x)

	fmt.Println("Chaqirishdan keyin x:", x)
}
```

## Tushuntirish va Mantiq:
Funksiyaga `&x` uzatilganda manzil ko'chiriladi va funksiya ichidan turib tashqi blokdagi qiymat yangilanadi.

## Ishlash natijasi:
```text
Chaqirishdan oldin x: 15
Chaqirishdan keyin x: 30
```

# 308-Topshiriq: Pass by Value va Pass by Pointer tezlik va nusxalash farqi
## Topshiriq sharti:
Katta massivni nusxalash va ko'rsatkich orqali uzatishning xotiradagi farqini namoyish qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

type KattaHujjat struct {
	data [1000]int
}

func nusxaBilan(h KattaHujjat) {
	// 8000 bayt to'liq nusxalandi
}

func korsatkichBilan(h *KattaHujjat) {
	// Faqat 8 baytlik ko'rsatkich uzatildi!
}

func main() {
	doc := KattaHujjat{}
	doc.data[0] = 1

	korsatkichBilan(&doc)
	fmt.Println("Ko'rsatkich orqali ortiqcha nusxalashsiz xavfsiz bajarildi.")
}
```

## Tushuntirish va Mantiq:
Katta hajmdagi ma'lumotlarni ko'rsatkich bilan uzatish xotira va protsessor resurslarini tejaydi.

## Ishlash natijasi:
```text
Ko'rsatkich orqali ortiqcha nusxalashsiz xavfsiz bajarildi.
```

# 309-Topshiriq: new() funksiyasi orqali xotira ajratish va nol ko'rsatkich olish
## Topshiriq sharti:
`new()` funksiyasi xotira ajratib unga toza nol qiymat berishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	pInt := new(int)
	pStr := new(string)

	fmt.Printf("pInt: %p -> %d\n", pInt, *pInt)
	fmt.Printf("pStr: %p -> %q\n", pStr, *pStr)

	*pInt = 99
	*pStr = "Yangi Qiymat"

	fmt.Println("O'zgartirilgach:", *pInt, *pStr)
}
```

## Tushuntirish va Mantiq:
`new(T)` xotiradan `T` uchun joy ajratadi, uni tozalaydi va `*T` ko'rsatkichini qaytaradi.

## Ishlash natijasi:
```text
pInt: 0xc000012088 -> 0
pStr: 0xc000014070 -> ""
O'zgartirilgach: 99 Yangi Qiymat
```

# 310-Topshiriq: Kompozit literal orqali ko'rsatkich olish: &Struct{} vs new(Struct)
## Topshiriq sharti:
Go da `&Struct{...}` va `new(Struct)` o'rtasidagi idiomatik farqni ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Konfig struct {
	Host string
	Port int
}

func main() {
	// 1-usul: new() - faqat nol qiymatlar bilan
	k1 := new(Konfig)
	k1.Host = "localhost"
	k1.Port = 8080

	// 2-usul: &Konfig{} - boshlang'ich qiymatlar bilan (Ko'proq tavsiya etiladi!)
	k2 := &Konfig{
		Host: "api.olam.uz",
		Port: 443,
	}

	fmt.Printf("k1: %+v\n", k1)
	fmt.Printf("k2: %+v\n", k2)
}
```

## Tushuntirish va Mantiq:
Go hamjamiyatida `&T{Field: val}` sintaksisi `new(T)` ga qaraganda ancha ko'proq ishlatiladi.

## Ishlash natijasi:
```text
k1: &{Host:localhost Port:8080}
k2: &{Host:api.olam.uz Port:443}
```

# 311-Topshiriq: Struktura ko'rsatkichlarida avtomatik dereferensiya
## Topshiriq sharti:
Go da `ptr.Field` avtomatik `(*ptr).Field` sifatida ishlashini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Mashina struct {
	Model string
	Tezlik int
}

func main() {
	m := &Mashina{Model: "BYD Song Plus", Tezlik: 180}

	// C tilidagi (*m).Tezlik yoki m->Tezlik o'rniga:
	fmt.Println("Model:", m.Model) // Go o'zi avtomatik dereferensiya qiladi
	fmt.Println("Tezlik:", m.Tezlik)

	m.Tezlik = 200 // To'g'ridan-to'g'ri maydon yangilanadi
	fmt.Println("Yangi tezlik:", m.Tezlik)
}
```

## Tushuntirish va Mantiq:
Go sintaksisi qulayligi uchun `ptr.Maydon` yozilganda kompilyator uni avtomatik `(*ptr).Maydon` ga o'giradi.

## Ishlash natijasi:
```text
Model: BYD Song Plus
Tezlik: 180
Yangi tezlik: 200
```

# 312-Topshiriq: Massivga ko'rsatkich (*[N]T)
## Topshiriq sharti:
Massiv ko'rsatkichi orqali massiv elementlariga murojaat qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	massiv := [3]int{10, 20, 30}
	pArr := &massiv

	// Avtomatik dereferensiya indekslashda ham ishlaydi:
	pArr[0] = 99 // (*pArr)[0] = 99 bilan bir xil

	fmt.Println("Asl massiv:", massiv)
	fmt.Println("Ko'rsatkich orqali:", *pArr)
}
```

## Tushuntirish va Mantiq:
Massiv ko'rsatkichi `*[N]T` indekslanganda ham Go qulay sintaksisni ta'minlaydi.

## Ishlash natijasi:
```text
Asl massiv: [99 20 30]
Ko'rsatkich orqali: [99 20 30]
```

# 313-Topshiriq: Funksiyadan lokal o'zgaruvchi ko'rsatkichini qaytarish xavfsizligi
## Topshiriq sharti:
Go da lokal o'zgaruvchi ko'rsatkichini bemalol qaytarish mumkinligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func yaratFoydalanuvchi(ism string) *string {
	// C da bu xato (dangling pointer) bo'lardi, lekin Go da to'liq xavfsiz!
	lokalIsm := ism + " (tasdiqlangan)"
	return &lokalIsm
}

func main() {
	p := yaratFoydalanuvchi("Aziza")
	fmt.Println("Qaytarilgan matn ko'rsatkichi:", *p)
}
```

## Tushuntirish va Mantiq:
Go kompilyatori escape analysis orqali agar o'zgaruvchi funksiyadan tashqariga chiqsa, uni avtomatik Heap xotiraga ko'chiradi.

## Ishlash natijasi:
```text
Qaytarilgan matn ko'rsatkichi: Aziza (tasdiqlangan)
```

# 314-Topshiriq: Escape Analysis tushunchasi (Stack vs Heap)
## Topshiriq sharti:
Qaysi o'zgaruvchilar stakda qolishi va qaysilari xipga chiqishini tushuntiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func stackAllocation() int {
	x := 42 // Funksiya tugashi bilan stakdan o'chadi
	return x
}

func heapAllocation() *int {
	y := 100 // Tashqariga chiqadi (escapes to heap)
	return &y
}

func main() {
	a := stackAllocation()
	b := heapAllocation()

	fmt.Println("Stakdan qiymat:", a)
	fmt.Println("Xipdan ko'rsatkich:", *b)
}
```

## Tushuntirish va Mantiq:
`go build -gcflags="-m"` buyrug'i orqali qaysi o'zgaruvchilar xipga o'tganini (escapes to heap) ko'rish mumkin.

## Ishlash natijasi:
```text
Stakdan qiymat: 42
Xipdan ko'rsatkich: 100
```

# 315-Topshiriq: Ikki karra ko'rsatkichlar (Double Pointers: **T)
## Topshiriq sharti:
Ko'rsatkichning manzilini saqlovchi ikkinchi ko'rsatkich bilan ishlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	son := 500
	p1 := &son  // *int
	p2 := &p1   // **int

	fmt.Printf("son: %d\n", son)
	fmt.Printf("*p1: %d\n", *p1)
	fmt.Printf("**p2: %d\n", **p2)

	**p2 = 700 // Ikki qadam chuqurlikdagi qiymatni o'zgartirish
	fmt.Println("Yangilangan son:", son)
}
```

## Tushuntirish va Mantiq:
`**p` orqali ko'rsatkichning o'zini ham almashtirish yoki chuqur qiymatni boshqarish mumkin.

## Ishlash natijasi:
```text
son: 500
*p1: 500
**p2: 500
Yangilangan son: 700
```

# 316-Topshiriq: Ko'rsatkichlarni taqqoslash (p1 == p2)
## Topshiriq sharti:
Ikkita ko'rsatkich qachon teng bo'lishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	a := 10
	b := 10

	p1 := &a
	p2 := &a
	p3 := &b

	fmt.Println("p1 == p2 (bir xil manzil):", p1 == p2)
	fmt.Println("p1 == p3 (turli manzil, lekin qiymati bir xil):", p1 == p3)
	fmt.Println("*p1 == *p3 (qiymatlar tengligi):", *p1 == *p3)
}
```

## Tushuntirish va Mantiq:
Ko'rsatkichlar solishtirilganda ularning ichidagi xotira manzillari tengligi tekshiriladi.

## Ishlash natijasi:
```text
p1 == p2 (bir xil manzil): true
p1 == p3 (turli manzil, lekin qiymati bir xil): false
*p1 == *p3 (qiymatlar tengligi): true
```

# 317-Topshiriq: Go da Pointer Arifmetikasi yo'qligi va xavfsizlik
## Topshiriq sharti:
Nima uchun `p++` yoki `p + 1` Go da taqiqlanganini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	sonlar := [3]int{10, 20, 30}
	p := &sonlar[0]

	// C tilida: p++ qilib keyingi elementga o'tish mumkin edi.
	// Go da: p++ sintaktik XATOLIK!
	// Go xotira xavfsizligi (memory safety) uchun bunga ruxsat bermaydi.

	fmt.Println("0-element ko'rsatkichi:", *p)
	fmt.Println("Keyingi elementga faqat indeks orqali xavfsiz o'tiladi:", sonlar[1])
}
```

## Tushuntirish va Mantiq:
Pointer arifmetikasi bufer to'lib ketishi (buffer overflow) va xotira xatolarining 80% sababchisidir. Go uni xavfsizlik uchun bloklagan.

## Ishlash natijasi:
```text
0-element ko'rsatkichi: 10
Keyingi elementga faqat indeks orqali xavfsiz o'tiladi: 20
```

# 318-Topshiriq: Bog'langan ro'yxat (Singly Linked List) tugun tuzilmasi
## Topshiriq sharti:
Ko'rsatkichlar orqali bir-biriga ulangan zanjir tugunini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Tugun struct {
	Qiymat  int
	Keyingi *Tugun
}

func main() {
	t3 := &Tugun{Qiymat: 30, Keyingi: nil}
	t2 := &Tugun{Qiymat: 20, Keyingi: t3}
	t1 := &Tugun{Qiymat: 10, Keyingi: t2}

	fmt.Printf("1-tugun: %d -> 2-tugun: %d -> 3-tugun: %d\n",
		t1.Qiymat, t1.Keyingi.Qiymat, t1.Keyingi.Keyingi.Qiymat)
}
```

## Tushuntirish va Mantiq:
Linked List tugunlari o'zidan keyingi elementga `*Tugun` ko'rsatkichi orqali ulanadi.

## Ishlash natijasi:
```text
1-tugun: 10 -> 2-tugun: 20 -> 3-tugun: 30
```

# 319-Topshiriq: Linked List boshiga element qo'shish (Prepend)
## Topshiriq sharti:
Ro'yxat boshiga O(1) tezlikda yangi element qo'shuvchi metod yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Node struct {
	val  int
	next *Node
}

type LinkedList struct {
	head *Node
}

func (ll *LinkedList) Prepend(v int) {
	yangi := &Node{val: v, next: ll.head}
	ll.head = yangi
}

func main() {
	ll := &LinkedList{}
	ll.Prepend(30)
	ll.Prepend(20)
	ll.Prepend(10)

	fmt.Println("Bosh tugun qiymati:", ll.head.val)
	fmt.Println("Ikkinchi tugun qiymati:", ll.head.next.val)
}
```

## Tushuntirish va Mantiq:
Ro'yxat boshiga qo'shish yangi tugunning `next` ini eski boshga qaratib, `head` ni yangilash orqali bir zumda bajariladi.

## Ishlash natijasi:
```text
Bosh tugun qiymati: 10
Ikkinchi tugun qiymati: 20
```

# 320-Topshiriq: Linked List bo'ylab harakatlanish va chop etish
## Topshiriq sharti:
Ro'yxat boshidan to oxirigacha aylanib barcha elementlarni chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Node struct {
	val  int
	next *Node
}

func chopEtList(head *Node) {
	joriy := head
	for joriy != nil {
		fmt.Printf("%d -> ", joriy.val)
		joriy = joriy.next
	}
	fmt.Println("nil")
}

func main() {
	n3 := &Node{val: 300}
	n2 := &Node{val: 200, next: n3}
	n1 := &Node{val: 100, next: n2}

	chopEtList(n1)
}
```

## Tushuntirish va Mantiq:
`for joriy != nil; joriy = joriy.next` Linked List bo'ylab harakatlanishning standart andozasidir.

## Ishlash natijasi:
```text
100 -> 200 -> 300 -> nil
```

# 321-Topshiriq: Ikki tomonlama bog'langan ro'yxat (Doubly Linked List)
## Topshiriq sharti:
Oldingi va keyingi ko'rsatkichlarga ega tugun yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type DNode struct {
	val   string
	prev  *DNode
	next  *DNode
}

func main() {
	bir := &DNode{val: "Birinchi"}
	ikki := &DNode{val: "Ikkinchi"}

	bir.next = ikki
	ikki.prev = bir

	fmt.Printf("Oldinga: %s -> %s\n", bir.val, bir.next.val)
	fmt.Printf("Orqaga:  %s <- %s\n", ikki.prev.val, ikki.val)
}
```

## Tushuntirish va Mantiq:
Doubly Linked List har ikki tomonga harakatlanish imkonini beradi.

## Ishlash natijasi:
```text
Oldinga: Birinchi -> Ikkinchi
Orqaga:  Birinchi <- Ikkinchi
```

# 322-Topshiriq: Binar Qidiruv Daraxti (Binary Search Tree - BST) tuguni
## Topshiriq sharti:
Chap va o'ng ko'rsatkichlarga ega BST tugunini aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type TreeNode struct {
	Qiymat int
	Chap   *TreeNode
	Ong    *TreeNode
}

func main() {
	ildiz := &TreeNode{Qiymat: 10}
	ildiz.Chap = &TreeNode{Qiymat: 5}
	ildiz.Ong = &TreeNode{Qiymat: 15}

	fmt.Printf("Ildiz: %d, Chap: %d, O'ng: %d\n", ildiz.Qiymat, ildiz.Chap.Qiymat, ildiz.Ong.Qiymat)
}
```

## Tushuntirish va Mantiq:
BST qoidasi: chap tugun ildizdan kichik, o'ng tugun ildizdan katta bo'ladi.

## Ishlash natijasi:
```text
Ildiz: 10, Chap: 5, O'ng: 15
```

# 323-Topshiriq: BST ga yangi tugun qo'shish (Insert)
## Topshiriq sharti:
Rekursiv ko'rsatkichlar orqali BST ga yangi elementlarni tartibli joylashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type BSTNode struct {
	Val   int
	Left  *BSTNode
	Right *BSTNode
}

func insertBST(root *BSTNode, val int) *BSTNode {
	if root == nil {
		return &BSTNode{Val: val}
	}
	if val < root.Val {
		root.Left = insertBST(root.Left, val)
	} else {
		root.Right = insertBST(root.Right, val)
	}
	return root
}

func main() {
	var root *BSTNode
	qiymatlar := []int{50, 30, 70, 20, 40}

	for _, v := range qiymatlar {
		root = insertBST(root, v)
	}

	fmt.Println("BST ildizi:", root.Val)
	fmt.Println("Ildizning chap bolasi:", root.Left.Val)
}
```

## Tushuntirish va Mantiq:
Yangi tugun o'z qiymatiga ko'ra mos bo'sh joyga (nil ko'rsatkich o'rniga) joylashadi.

## Ishlash natijasi:
```text
BST ildizi: 50
Ildizning chap bolasi: 30
```

# 324-Topshiriq: BST ni In-Order (Tartibli) aylanib chiqish
## Topshiriq sharti:
Daraxtdagi elementlarni o'sish tartibida chop etuvchi In-Order traversal yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type BNode struct {
	Val   int
	Left  *BNode
	Right *BNode
}

func inOrder(root *BNode) {
	if root == nil {
		return
	}
	inOrder(root.Left)
	fmt.Printf("%d ", root.Val)
	inOrder(root.Right)
}

func main() {
	root := &BNode{Val: 50}
	root.Left = &BNode{Val: 20}
	root.Right = &BNode{Val: 80}
	root.Left.Right = &BNode{Val: 35}

	fmt.Print("In-Order saralangan: ")
	inOrder(root)
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Chap -> Ildiz -> O'ng tartibi BST dagi barcha qiymatlarni avtomatik saralangan holda chiqaradi.

## Ishlash natijasi:
```text
In-Order saralangan: 20 35 50 80
```

# 325-Topshiriq: Nil Receiver ustida metod chaqirish imkoniyati
## Topshiriq sharti:
Ko'rsatkich qabul qiluvchi metod `nil` bo'lganda ham xavfsiz ishlashini ta'minlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Talaba struct {
	Ism string
}

func (t *Talaba) IsmniOlish() string {
	if t == nil {
		return "Noma'lum talaba (nil)"
	}
	return t.Ism
}

func main() {
	var t1 *Talaba
	fmt.Println("t1 nomi:", t1.IsmniOlish()) // Nil bo'lsa ham panic bermaydi!

	t2 := &Talaba{Ism: "Zuhra"}
	fmt.Println("t2 nomi:", t2.IsmniOlish())
}
```

## Tushuntirish va Mantiq:
Go da metod ko'rsatkichi `nil` bo'lsa ham metod chaqirilishi mumkin. Metod ichida `if t == nil` tekshiruvi bo'lsa u xavfsiz ishlaydi.

## Ishlash natijasi:
```text
t1 nomi: Noma'lum talaba (nil)
t2 nomi: Zuhra
```

# 326-Topshiriq: unsafe.Pointer asoslari va tur xavfsizligini chetlab o'tish
## Topshiriq sharti:
`unsafe.Pointer` orqali turli turlar o'rtasidagi to'g'ridan-to'g'ri xotira ko'rsatkichini bog'lang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unsafe"
)

func main() {
	var son int64 = 42
	// int64 ko'rsatkichini unsafe.Pointer orqali *uint64 ga o'giramiz:
	pUnsafe := unsafe.Pointer(&son)
	pUint := (*uint64)(pUnsafe)

	fmt.Printf("Asl son: %d, Konvertatsiya qilingan: %d\n", son, *pUint)
}
```

## Tushuntirish va Mantiq:
`unsafe.Pointer` Go tip tizimini chetlab o'tib, har qanday ko'rsatkichni boshqa tur ko'rsatkichiga aylantirish imkonini beradi.

## Ishlash natijasi:
```text
Asl son: 42, Konvertatsiya qilingan: 42
```

# 327-Topshiriq: uintptr va xotira manzillari arifmetikasi
## Topshiriq sharti:
Struktura ichidagi ikkinchi maydon manzilini `unsafe.Offsetof` va `uintptr` orqali hisoblang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unsafe"
)

type Nuqta struct {
	X int32
	Y int32
}

func main() {
	n := Nuqta{X: 10, Y: 20}

	pBosh := unsafe.Pointer(&n)
	offsetY := unsafe.Offsetof(n.Y)

	pY := (*int32)(unsafe.Pointer(uintptr(pBosh) + offsetY))

	fmt.Println("Offset orqali olingan Y qiymati:", *pY)
}
```

## Tushuntirish va Mantiq:
`uintptr` xotira manzilini saqlovchi butun son bo'lib, offset qo'shish orqali xotira bo'ylab siljishga xizmat qiladi.

## Ishlash natijasi:
```text
Offset orqali olingan Y qiymati: 20
```

# 328-Topshiriq: unsafe.Sizeof va unsafe.Offsetof bilan xotira tahlili
## Topshiriq sharti:
Struktura maydonlarining o'lchami va ofsetlarini tahlil qiling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unsafe"
)

type XodimInfo struct {
	Faol  bool    // 1 bayt
	Maosh float64 // 8 bayt
}

func main() {
	var x XodimInfo
	fmt.Println("Jami struktura hajmi:", unsafe.Sizeof(x), "bayt")
	fmt.Println("Maosh maydonining siljishi (offset):", unsafe.Offsetof(x.Maosh), "bayt")
}
```

## Tushuntirish va Mantiq:
Padding tufayli `Faol` dan keyin 7 bayt bo'shliq qo'shilib, `Maosh` 8-baytdan boshlanadi.

## Ishlash natijasi:
```text
Jami struktura hajmi: 16 bayt
Maosh maydonining siljishi (offset): 8 bayt
```

# 329-Topshiriq: Zero-Copy: []byte ni string ga nusxalashsiz aylantirish (unsafe.String)
## Topshiriq sharti:
Go 1.20+ `unsafe.String` orqali baytlar massividan 0 bayt qo'shimcha xotira bilan satr hosil qiling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unsafe"
)

func baytlarSatrga(b []byte) string {
	if len(b) == 0 {
		return ""
	}
	return unsafe.String(&b[0], len(b))
}

func main() {
	baytlar := []byte("Yuqori tezlikdagi Go!")
	satr := baytlarSatrga(baytlar)

	fmt.Println("Zero-copy satr:", satr)
}
```

## Tushuntirish va Mantiq:
`unsafe.String` Go 1.20 da standart kiritilgan bo'lib, xotirani qayta nusxalamasdan string sarlavhasi yasaydi.

## Ishlash natijasi:
```text
Zero-copy satr: Yuqori tezlikdagi Go!
```

# 330-Topshiriq: Zero-Copy: string ni []byte ga nusxalashsiz o'tkazish (unsafe.Slice)
## Topshiriq sharti:
Go 1.20+ `unsafe.SliceData` va `unsafe.Slice` bilan satr baytlarini o'qish.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unsafe"
)

func satrBaytlarga(s string) []byte {
	return unsafe.Slice(unsafe.StringData(s), len(s))
}

func main() {
	matn := "Salom"
	b := satrBaytlarga(matn)

	fmt.Println("Baytlar:", b)
}
```

## Tushuntirish va Mantiq:
Satr ichidagi mavjud xotiraga bevosita oyna (slice) bog'lanadi va 0 ta yangi xotira ajratiladi.

## Ishlash natijasi:
```text
Baytlar: [83 97 108 111 109]
```

# 331-Topshiriq: Qachon ko'rsatkich, qachon qiymat ishlatish kerak?
## Topshiriq sharti:
Qaysi holatlarda Pointer, qaysi holatlarda Value ishlatish qoidalarini namoyish qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

// Kichik turlar (int, float, kichik struct) - QIYMAT bo'yicha:
type Nuqta struct {
	X, Y int
}

func yangiNuqta(x, y int) Nuqta {
	return Nuqta{x, y} // Kichik struct nusxalanishi juda arzon
}

// O'zgaruvchan yoki katta turlar - KO'RSATKICH bo'yicha:
type Hisoblagich struct {
	soni int
}

func (h *Hisoblagich) Oshir() {
	h.soni++
}

func main() {
	p := yangiNuqta(10, 20)
	fmt.Printf("Nuqta: %+v\n", p)

	h := &Hisoblagich{}
	h.Oshir()
	fmt.Println("Hisoblagich:", h.soni)
}
```

## Tushuntirish va Mantiq:
Kichik, o'zgarmas ma'lumotlar qiymat (Value) bo'yicha; katta obyektlar yoki holati o'zgaruvchi ma'lumotlar ko'rsatkich (Pointer) orqali uzatiladi.

## Ishlash natijasi:
```text
Nuqta: {X:10 Y:20}
Hisoblagich: 1
```

# 332-Topshiriq: Immutability (O'zgarmaslik) andozasi
## Topshiriq sharti:
Qiymat bo'yicha nusxalash orqali tashqi mutatsiyalardan to'liq himoyalangan tuzilma yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Valyuta struct {
	qiymat int
}

func (v Valyuta) Qosh(miqdor int) Valyuta {
	return Valyuta{qiymat: v.qiymat + miqdor} // Yangi nusxa qaytaradi
}

func main() {
	v1 := Valyuta{qiymat: 100}
	v2 := v1.Qosh(50)

	fmt.Println("Asl v1:", v1.qiymat)
	fmt.Println("Yangi v2:", v2.qiymat)
}
```

## Tushuntirish va Mantiq:
Qiymat qabul qiluvchi metodlar asl obyektni o'zgartirmaydi, doimo yangi nusxa beradi (funksional uslub).

## Ishlash natijasi:
```text
Asl v1: 100
Yangi v2: 150
```

# 333-Topshiriq: Ko'rsatkich orqali Singleton andozasi
## Topshiriq sharti:
Tizimda yagona nusxada mavjud bo'lgan ma'lumotlar bazasi ulanishini boshqaring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type BazaUlanishi struct {
	Nom string
}

var (
	ulanishNusxasi *BazaUlanishi
	birMarta       sync.Once
)

func GetBaza() *BazaUlanishi {
	birMarta.Do(func() {
		ulanishNusxasi = &BazaUlanishi{Nom: "PostgreSQL Production"}
	})
	return ulanishNusxasi
}

func main() {
	b1 := GetBaza()
	b2 := GetBaza()

	fmt.Println("b1 va b2 bir xil xotira manzilidami:", b1 == b2)
}
```

## Tushuntirish va Mantiq:
`sync.Once` va ko'rsatkich orqali Singleton barcha chaqiriqlarda yagona xotira manzilini taqsimlaydi.

## Ishlash natijasi:
```text
b1 va b2 bir xil xotira manzilidami: true
```

# 334-Topshiriq: Funksiya ko'rsatkichlari (Function Pointers)
## Topshiriq sharti:
Funksiyani ko'rsatkich sifatida saqlash va chaqirish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type MatematikAmal func(int, int) int

func qosh(a, b int) int { return a + b }

func main() {
	var f MatematikAmal = qosh
	ptrToFunc := &f

	fmt.Println("Chaqirish natijasi:", (*ptrToFunc)(20, 30))
}
```

## Tushuntirish va Mantiq:
Go da funksiyalar ham birinchi darajali obyekt bo'lib ularga ham ko'rsatkichlar orqali murojaat qilish mumkin.

## Ishlash natijasi:
```text
Chaqirish natijasi: 50
```

# 335-Topshiriq: Struktura ichida o'z turiga ko'rsatkich saqlash (Recursive Types)
## Topshiriq sharti:
O'z-o'ziga bog'langan tashkiliy iyerarxiya (Xodim va uning Rahbari) modelini tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Xodim struct {
	Ism     string
	Rahbari *Xodim // O'z turiga ko'rsatkich
}

func main() {
	direktor := &Xodim{Ism: "Aziz Rahbarov", Rahbari: nil}
	muhandis := &Xodim{Ism: "Jamshid", Rahbari: direktor}

	fmt.Printf("Xodim: %s | Rahbari: %s\n", muhandis.Ism, muhandis.Rahbari.Ism)
}
```

## Tushuntirish va Mantiq:
Rekursiv strukturalarda o'lcham cheksiz bo'lmasligi uchun albatta ko'rsatkich (`*Xodim`) ishlatilishi shart.

## Ishlash natijasi:
```text
Xodim: Jamshid | Rahbari: Aziz Rahbarov
```

# 336-Topshiriq: Ko'rsatkichlar massivi ([]*T) va Qiymatlar massivi ([]T) farqi
## Topshiriq sharti:
Xotira joylashuvi va kesh samaradorligidagi farqni solishtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Element struct {
	ID int
}

func main() {
	// Qiymatlar slicesi: xotirada ketma-ket yotadi (Cache-friendly)
	qiymatlar := []Element{{1}, {2}, {3}}

	// Ko'rsatkichlar slicesi: xotirada tarqoq bo'lishi mumkin
	korsatkichlar := []*Element{{1}, {2}, {3}}

	fmt.Printf("Qiymatlar: %v\n", qiymatlar)
	fmt.Printf("Ko'rsatkichlar: %p, %p\n", korsatkichlar[0], korsatkichlar[1])
}
```

## Tushuntirish va Mantiq:
`[]T` protsessor keshiga juda mos tushadi (Cache locality). `[]*T` esa katta elementlarda ortiqcha nusxalashdan saqlaydi.

## Ishlash natijasi:
```text
Qiymatlar: [{1} {2} {3}]
Ko'rsatkichlar: 0xc000012088, 0xc000012090
```

# 337-Topshiriq: Optional / Nullable maydonlarni ko'rsatkich orqali ifodalash
## Topshiriq sharti:
Qiymat mavjud emasligini (null) ko'rsatish uchun `*string` maydonidan foydalaning.

## Yechim (Go kodi):
```go
package main

import "fmt"

type FoydalanuvchiProfil struct {
	Ism           string
	OtasiningIsmi *string // Majburiy emas (optional)
}

func main() {
	otasiningIsmi := "Karimovich"
	u1 := FoydalanuvchiProfil{Ism: "Botir", OtasiningIsmi: &otasiningIsmi}
	u2 := FoydalanuvchiProfil{Ism: "Sarvar", OtasiningIsmi: nil}

	if u1.OtasiningIsmi != nil {
		fmt.Printf("%s otasining ismi: %s\n", u1.Ism, *u1.OtasiningIsmi)
	}

	if u2.OtasiningIsmi == nil {
		fmt.Printf("%s otasining ismi kiritilmagan (nil)\n", u2.Ism)
	}
}
```

## Tushuntirish va Mantiq:
Go da `nil` ko'rsatkich ma'lumotlar bazasidagi `NULL` qiymatlarini aniq ifodalash uchun standart usuldir.

## Ishlash natijasi:
```text
Botir otasining ismi: Karimovich
Sarvar otasining ismi kiritilmagan (nil)
```

# 338-Topshiriq: Ko'rsatkichlar yordamida chuqur klonlash (Deep Clone with Pointers)
## Topshiriq sharti:
Ichki ko'rsatkichli obyektlarning to'liq mustaqil nusxasini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Manzil struct {
	Shahar string
}

type TalabaProfil struct {
	Ism    string
	Manzil *Manzil
}

func (tp *TalabaProfil) DeepClone() *TalabaProfil {
	yangi := &TalabaProfil{Ism: tp.Ism}
	if tp.Manzil != nil {
		yangi.Manzil = &Manzil{Shahar: tp.Manzil.Shahar}
	}
	return yangi
}

func main() {
	t1 := &TalabaProfil{Ism: "Ali", Manzil: &Manzil{Shahar: "Toshkent"}}
	t2 := t1.DeepClone()

	t2.Manzil.Shahar = "Samarqand"

	fmt.Println("t1 shahri:", t1.Manzil.Shahar)
	fmt.Println("t2 shahri (mustaqil):", t2.Manzil.Shahar)
}
```

## Tushuntirish va Mantiq:
Deep clone ichki barcha ko'rsatkichlar uchun yangi xotira ajratib ma'lumotlarni ko'chiradi.

## Ishlash natijasi:
```text
t1 shahri: Toshkent
t2 shahri (mustaqil): Samarqand
```

# 339-Topshiriq: Aylana bog'liqliklar (Circular References) tahlili
## Topshiriq sharti:
Ikki obyekt bir-biriga ko'rsatib turgan holatda Go Garbage Collector qanday ishlashini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type TugunA struct {
	B *TugunB
}

type TugunB struct {
	A *TugunA
}

func main() {
	a := &TugunA{}
	b := &TugunB{}

	a.B = b
	b.A = a

	fmt.Println("Aylana bog'liqlik muvaffaqiyatli o'rnatildi.")
	// Go ning Tri-color Mark & Sweep Garbage Collectori aylana bog'liqliklarni ham bemalol tozalay oladi!
}
```

## Tushuntirish va Mantiq:
Reference Counting (masalan, Python yoki Swift) dan farqli ravishda Go ning Trilinear Mark & Sweep GC si aylana bog'langan obyektlarni ham xotiradan to'g'ri tozalaydi.

## Ishlash natijasi:
```text
Aylana bog'liqlik muvaffaqiyatli o'rnatildi.
```

# 340-Topshiriq: Ko'rsatkichni nil qilish orqali Garbage Collectorga yordam berish
## Topshiriq sharti:
Katta xotira blokini ishlatib bo'lgach ko'rsatkichni `nil` ga tenglab resursni bo'shating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	kattaData := new([1000]int)
	kattaData[0] = 999

	fmt.Println("Ma'lumotlar bilan ishlandi:", kattaData[0])

	// Resurs endi kerak emas:
	kattaData = nil

	fmt.Println("Ko'rsatkich nil qilindi, xotira GC uchun bo'shatildi.")
}
```

## Tushuntirish va Mantiq:
Uzoq yashovchi goroutinelarda katta obyektlar ko'rsatkichini `nil` qilish xotira sizishining oldini oladi.

## Ishlash natijasi:
```text
Ma'lumotlar bilan ishlandi: 999
Ko'rsatkich nil qilindi, xotira GC uchun bo'shatildi.
```

# 341-Topshiriq: Slice Header ko'rsatkichini xotiradan bevosita o'qish
## Topshiriq sharti:
Slicening tagidagi massiv manzilini `%p` orqali ko'ring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	s := []int{10, 20, 30}

	fmt.Printf("Slicening o'z manzili: %p\n", &s)
	fmt.Printf("Birinchi element manzili (tagidagi massiv): %p\n", &s[0])
}
```

## Tushuntirish va Mantiq:
Slicening o'zi 3 ta qiymatli stak o'zgaruvchisidir, uning ichidagi pointer esa xipdagi haqiqiy massivga qaratilgan.

## Ishlash natijasi:
```text
Slicening o'z manzili: 0xc000014070
Birinchi element manzili (tagidagi massiv): 0xc000012088
```

# 342-Topshiriq: Bog'langan ro'yxatdan elementni o'chirish (Delete Node)
## Topshiriq sharti:
Qiymati mos kelgan tugunni ko'rsatkichlarni chetlab o'tkazish orqali o'chiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Node struct {
	val  int
	next *Node
}

func ochirTugun(head *Node, maqsad int) *Node {
	if head == nil {
		return nil
	}
	if head.val == maqsad {
		return head.next
	}

	joriy := head
	for joriy.next != nil && joriy.next.val != maqsad {
		joriy = joriy.next
	}

	if joriy.next != nil {
		joriy.next = joriy.next.next // O'chiriladigan tugunni chetlab o'tamiz
	}
	return head
}

func main() {
	n3 := &Node{val: 30}
	n2 := &Node{val: 20, next: n3}
	n1 := &Node{val: 10, next: n2}

	bosh := ochirTugun(n1, 20)

	for p := bosh; p != nil; p = p.next {
		fmt.Printf("%d ", p.val)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Tugunni o'chirish oldingi elementning `next` ko'rsatkichini keyingi tugunga qaratish orqali O(1) da amalga oshadi.

## Ishlash natijasi:
```text
10 30
```

# 343-Topshiriq: Bog'langan ro'yxatni joyida teskari o'girish (Reverse Linked List)
## Topshiriq sharti:
Ko'rsatkichlar yo'nalishini 180 darajaga o'zgartiruvchi klassik algoritm yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Node struct {
	val  int
	next *Node
}

func reverseList(head *Node) *Node {
	var prev *Node
	curr := head

	for curr != nil {
		nextTemp := curr.next
		curr.next = prev
		prev = curr
		curr = nextTemp
	}
	return prev
}

func main() {
	n3 := &Node{val: 3}
	n2 := &Node{val: 2, next: n3}
	n1 := &Node{val: 1, next: n2}

	yangibosh := reverseList(n1)

	for p := yangibosh; p != nil; p = p.next {
		fmt.Printf("%d ", p.val)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
`prev`, `curr`, `nextTemp` uch ko'rsatkichi yordamida ro'yxat bir o'tishda teskari qilinadi.

## Ishlash natijasi:
```text
3 2 1
```

# 344-Topshiriq: Linked List siklini (Cycle Detection) aniqlash - Floyd algoritmi
## Topshiriq sharti:
Tez va sekin yuruvchi ikki ko'rsatkich (Tortoise and Hare) orqali zanjirdagi siklni toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Node struct {
	val  int
	next *Node
}

func hasCycle(head *Node) bool {
	sekin, tez := head, head

	for tez != nil && tez.next != nil {
		sekin = sekin.next
		tez = tez.next.next
		if sekin == tez {
			return true // Uchrashdi -> sikl bor!
		}
	}
	return false
}

func main() {
	n1 := &Node{val: 1}
	n2 := &Node{val: 2}
	n3 := &Node{val: 3}

	n1.next = n2
	n2.next = n3
	n3.next = n1 // Sikl hosil qilamiz

	fmt.Println("Sikl mavjudmi:", hasCycle(n1))
}
```

## Tushuntirish va Mantiq:
Floyd algoritmi O(1) xotira bilan cheksiz aylanib qolgan zanjirlarni aniqlaydi.

## Ishlash natijasi:
```text
Sikl mavjudmi: true
```

# 345-Topshiriq: Ikki saralangan bog'langan ro'yxatni birlashtirish (Merge Two Lists)
## Topshiriq sharti:
Ikki saralangan ro'yxatni ko'rsatkichlar orqali tartibli birlashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Node struct {
	val  int
	next *Node
}

func mergeSorted(l1, l2 *Node) *Node {
	dummy := &Node{}
	tail := dummy

	for l1 != nil && l2 != nil {
		if l1.val < l2.val {
			tail.next = l1
			l1 = l1.next
		} else {
			tail.next = l2
			l2 = l2.next
		}
		tail = tail.next
	}

	if l1 != nil {
		tail.next = l1
	} else {
		tail.next = l2
	}
	return dummy.next
}

func main() {
	l1 := &Node{val: 1, next: &Node{val: 3}}
	l2 := &Node{val: 2, next: &Node{val: 4}}

	merged := mergeSorted(l1, l2)
	for p := merged; p != nil; p = p.next {
		fmt.Printf("%d ", p.val)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
`dummy` nina tuguni yordamida birlashtirish kodi o'ta toza va chekka holatlarsiz yoziladi.

## Ishlash natijasi:
```text
1 2 3 4
```

# 346-Topshiriq: BST dan minimal qiymatli tugunni topish
## Topshiriq sharti:
Ko'rsatkich bo'ylab eng chapki tugunga qadar borib eng kichik sonni toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

type BSTNode struct {
	val   int
	left  *BSTNode
	right *BSTNode
}

func findMin(root *BSTNode) int {
	if root == nil {
		return -1
	}
	joriy := root
	for joriy.left != nil {
		joriy = joriy.left
	}
	return joriy.val
}

func main() {
	root := &BSTNode{val: 50}
	root.left = &BSTNode{val: 25}
	root.left.left = &BSTNode{val: 12}
	root.right = &BSTNode{val: 75}

	fmt.Println("Daraxtdagi minimal qiymat:", findMin(root))
}
```

## Tushuntirish va Mantiq:
BST xususiyatiga ko'ra eng kichik element doimo eng chapki tugunda joylashadi.

## Ishlash natijasi:
```text
Daraxtdagi minimal qiymat: 12
```

# 347-Topshiriq: Binar daraxt chuqurligini (Max Depth) rekursiv ko'rsatkichlar bilan hisoblash
## Topshiriq sharti:
Daraxtning maksimal balandligini aniqlovchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type TreeNode struct {
	val   int
	left  *TreeNode
	right *TreeNode
}

func maxDepth(root *TreeNode) int {
	if root == nil {
		return 0
	}
	chap := maxDepth(root.left)
	ong := maxDepth(root.right)
	if chap > ong {
		return chap + 1
	}
	return ong + 1
}

func main() {
	root := &TreeNode{val: 1}
	root.left = &TreeNode{val: 2}
	root.right = &TreeNode{val: 3}
	root.left.left = &TreeNode{val: 4}

	fmt.Println("Daraxt chuqurligi:", maxDepth(root))
}
```

## Tushuntirish va Mantiq:
Har bir qavatda chap va o'ng shoxlarning kattasiga 1 qo'shib boriladi.

## Ishlash natijasi:
```text
Daraxt chuqurligi: 3
```

# 348-Topshiriq: Ko'rsatkichlar orqali xavfsiz qiymat almashtirish (Swap via Pointers)
## Topshiriq sharti:
Funksiyaga ikkita ko'rsatkich uzatib ularning manzillaridagi qiymatlarini almashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func almash(a, b *int) {
	*a, *b = *b, *a
}

func main() {
	x, y := 10, 20
	fmt.Printf("Oldin: x=%d, y=%d\n", x, y)
	almash(&x, &y)
	fmt.Printf("Keyin: x=%d, y=%d\n", x, y)
}
```

## Tushuntirish va Mantiq:
Ko'rsatkichlar orqali har qanday turlar ustida to'g'ridan-to'g'ri qiymat almashtirish oson bajariladi.

## Ishlash natijasi:
```text
Oldin: x=10, y=20
Keyin: x=20, y=10
```

# 349-Topshiriq: Pointer Wrapper orqali Generic Atomic Pointer tushunchasi
## Topshiriq sharti:
Ko'rsatkichni xavfsiz almashtirish konsepsiyasi.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync/atomic"
)

type Konfiguratsiya struct {
	Versiya string
}

func main() {
	var atomikPtr atomic.Pointer[Konfiguratsiya]

	k1 := &Konfiguratsiya{Versiya: "1.0"}
	atomikPtr.Store(k1)

	fmt.Println("Joriy versiya:", atomikPtr.Load().Versiya)

	k2 := &Konfiguratsiya{Versiya: "2.0"}
	atomikPtr.Store(k2)

	fmt.Println("Yangilangan versiya:", atomikPtr.Load().Versiya)
}
```

## Tushuntirish va Mantiq:
`atomic.Pointer` Go 1.19 da kiritilgan bo'lib, ko'rsatkichlarni bir vaqtda qulfsiz (lock-free) xavfsiz yangilash imkonini beradi.

## Ishlash natijasi:
```text
Joriy versiya: 1.0
Yangilangan versiya: 2.0
```

# 350-Topshiriq: Yakuniy amaliy vazifa: Ko'rsatkichlar asosidagi dinamik Navbat (Linked Queue)
## Topshiriq sharti:
O(1) qo'shish va O(1) olish tezligiga ega to'liq xotira boshqaruvchi ko'rsatkichli navbat tizimini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Tugun struct {
	qiymat string
	keyingi *Tugun
}

type BoglanganNavbat struct {
	boshi  *Tugun
	oxiri  *Tugun
	hajmi  int
}

func (q *BoglanganNavbat) Qosh(v string) {
	yangi := &Tugun{qiymat: v}
	if q.oxiri == nil {
		q.boshi = yangi
		q.oxiri = yangi
	} else {
		q.oxiri.keyingi = yangi
		q.oxiri = yangi
	}
	q.hajmi++
}

func (q *BoglanganNavbat) Olish() (string, bool) {
	if q.boshi == nil {
		return "", false
	}
	val := q.boshi.qiymat
	q.boshi = q.boshi.keyingi
	if q.boshi == nil {
		q.oxiri = nil
	}
	q.hajmi--
	return val, true
}

func main() {
	navbat := &BoglanganNavbat{}
	navbat.Qosh("Birinchi buyruq")
	navbat.Qosh("Ikkinchi buyruq")

	for {
		item, ok := navbat.Olish()
		if !ok {
			break
		}
		fmt.Println("Navbatdan bajarildi:", item)
	}
}
```

## Tushuntirish va Mantiq:
Ushbu ko'rsatkichli navbat xotirani qayta ko'chirmasdan va o'lcham cheklovisiz O(1) barqaror tezlikda ishlaydi.

## Ishlash natijasi:
```text
Navbatdan bajarildi: Birinchi buyruq
Navbatdan bajarildi: Ikkinchi buyruq
```

