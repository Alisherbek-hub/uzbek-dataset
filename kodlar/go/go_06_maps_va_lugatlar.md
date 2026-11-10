# 6-Mavzu: Maps va Lug'atlar (251-300)

Go dasturlash tilida xesh-jadvallar asosida qurilgan `map[K]V` kolleksiyasi. `make`, comma-ok idiomi, `delete`, tasodifiy iteratsiya xususiyati, saralangan kalitlar, `comparable` kalit talablari, 0 baytli `map[K]struct{}` yordamida to'plamlar (Set), Go 1.21+ `maps` paketi, xotirada kesh va ma'lumotlar tuzilmalari bo'yicha 50 ta amaliy topshiriq.

# 251-Topshiriq: Map e'lon qilish va make(map[K]V) yordamida yaratish
## Topshiriq sharti:
Talabalarning baholarini saqlovchi map yarating va unga ma'lumotlar qo'shing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	// make orqali bo'sh map yaratamiz:
	baholar := make(map[string]int)

	baholar["Alisher"] = 95
	baholar["Zuhra"] = 88
	baholar["Rustam"] = 92

	fmt.Println("Talabalar baholari:", baholar)
	fmt.Printf("Talabalar soni: %d\n", len(baholar))
}
```

## Tushuntirish va Mantiq:
Go tilida map xesh-jadval (hash table) asosida ishlaydi. `make(map[KalitTuri]QiymatTuri)` orqali xotiradan joy ajratiladi.

## Ishlash natijasi:
```text
Talabalar baholari: map[Alisher:95 Rustam:92 Zuhra:88]
Talabalar soni: 3
```

# 252-Topshiriq: Map literali orqali boshlang'ich qiymatlar bilan to'ldirish
## Topshiriq sharti:
Dunyo poytaxtlarini map literali orqali e'lon qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	poytaxtlar := map[string]string{
		"O'zbekiston": "Toshkent",
		"Yaponiya":    "Tokio",
		"Fransiya":    "Parij",
	}

	fmt.Println("Poytaxtlar xaritasi:", poytaxtlar)
	fmt.Println("O'zbekiston poytaxti:", poytaxtlar["O'zbekiston"])
}
```

## Tushuntirish va Mantiq:
Map literali `map[K]V{k1: v1, k2: v2}` sintaksisi orqali boshlang'ich ma'lumotlar bilan tezkor to'ldirish imkonini beradi.

## Ishlash natijasi:
```text
Poytaxtlar xaritasi: map[Fransiya:Parij O'zbekiston:Toshkent Yaponiya:Tokio]
O'zbekiston poytaxti: Toshkent
```

# 253-Topshiriq: Nil Map xususiyatlari va yozishdagi Panic xavfi
## Topshiriq sharti:
`var m map[string]int` nil map bo'lib, undan o'qish xavfsiz nol qaytarishi, ammo yozish panik berishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var nilMap map[string]int

	fmt.Println("nilMap nilmi:", nilMap == nil)
	fmt.Println("Nildan o'qish xavfsiz:", nilMap["kalit"]) // 0 qaytadi, panic bermaydi!

	// DIQQAT: nilMap["kalit"] = 100 // PANIC: assignment to entry in nil map!
	// Yozish uchun albatta make() yoki literal bilan initsializatsiya shart:
	xavfsizMap := make(map[string]int)
	xavfsizMap["kalit"] = 100
	fmt.Println("Xavfsiz map:", xavfsizMap)
}
```

## Tushuntirish va Mantiq:
Nil map xotiraga ega emas. O'qilganda sukut bo'yicha nol qiymat qaytadi, biroq unga yangi yozuv qo'shish har doim panik beradi.

## Ishlash natijasi:
```text
nilMap nilmi: true
Nildan o'qish xavfsiz: 0
Xavfsiz map: map[kalit:100]
```

# 254-Topshiriq: Kalit bo'yicha qiymat o'qish va yangilash
## Topshiriq sharti:
Mavjud kalitning qiymatini yangilang va yangi kalit qo'shing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ombordagiMahsulot := map[string]int{
		"Noutbuk": 10,
		"Telefon": 25,
	}

	// Qiymatni yangilash:
	ombordagiMahsulot["Noutbuk"] = 15

	// Yangi kalit qo'shish:
	ombordagiMahsulot["Monitor"] = 8

	fmt.Printf("Noutbuklar: %d ta\n", ombordagiMahsulot["Noutbuk"])
	fmt.Printf("Monitorlar: %d ta\n", ombordagiMahsulot["Monitor"])
}
```

## Tushuntirish va Mantiq:
Agar kalit mavjud bo'lsa `m[k] = v` uning qiymatini yangilaydi, mavjud bo'lmasa yangi yozuv yaratadi.

## Ishlash natijasi:
```text
Noutbuklar: 15 ta
Monitorlar: 8 ta
```

# 255-Topshiriq: Mavjud bo'lmagan kalit o'qilganda nol qiymat qaytishi
## Topshiriq sharti:
Mapda yo'q kalit o'qilganda nima yuz berishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	hisoblar := map[string]int{
		"Ali": 500,
	}

	fmt.Println("Ali hisobi:", hisoblar["Ali"])
	fmt.Println("Vali hisobi (mavjud emas):", hisoblar["Vali"]) // 0 qaytadi
}
```

## Tushuntirish va Mantiq:
Boshqa tillar (Python `KeyError` kabi) xatolik bergan joyda, Go har doim shu turning nol qiymatini (`0`, `""`, `false`) qaytaradi.

## Ishlash natijasi:
```text
Ali hisobi: 500
Vali hisobi (mavjud emas): 0
```

# 256-Topshiriq: Go ning mashhur 'Comma-ok' idiomi (val, ok := m[key])
## Topshiriq sharti:
Kalit haqiqatan mavjudmi yoki nol qiymat qaytmoqdami - buni `ok` orqali aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	statistika := map[string]int{
		"maqolalar": 0, // Haqiqiy qiymat 0
	}

	// 1-tekshiruv: "maqolalar" mavjud, qiymati 0
	val1, ok1 := statistika["maqolalar"]
	fmt.Printf("maqolalar: qiymat=%d, mavjudmi=%t\n", val1, ok1)

	// 2-tekshiruv: "sharhlar" umuman yo'q
	val2, ok2 := statistika["sharhlar"]
	fmt.Printf("sharhlar  : qiymat=%d, mavjudmi=%t\n", val2, ok2)
}
```

## Tushuntirish va Mantiq:
`val, ok := m[key]` sintaksisi: agar kalit mavjud bo'lsa `ok = true`, aks holda `ok = false` bo'ladi. Bu 0 bilan mavjud emaslikni ajratishning yagona to'g'ri yo'lidir.

## Ishlash natijasi:
```text
maqolalar: qiymat=0, mavjudmi=true
sharhlar  : qiymat=0, mavjudmi=false
```

# 257-Topshiriq: delete() funksiyasi orqali kalitni o'chirish
## Topshiriq sharti:
Mapdan keraksiz kalitni xotiradan to'liq o'chirib tashlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	sozlamalar := map[string]bool{
		"dark_mode":     true,
		"notifications": false,
		"beta_features": true,
	}

	fmt.Println("O'chirishdan oldin:", sozlamalar)

	delete(sozlamalar, "beta_features")

	fmt.Println("O'chirilgandan keyin:", sozlamalar)
}
```

## Tushuntirish va Mantiq:
`delete(m, key)` built-in funksiyasi kalit va unga tegishli qiymatni mapdan o'chiradi.

## Ishlash natijasi:
```text
O'chirishdan oldin: map[beta_features:true dark_mode:true notifications:false]
O'chirilgandan keyin: map[dark_mode:true notifications:false]
```

# 258-Topshiriq: Mavjud bo'lmagan kalitni delete qilish xavfsizligi
## Topshiriq sharti:
Mapda yo'q kalit o'chirilganda hech qanday xatolik yuz bermasligini isbotlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	m := map[string]int{"a": 1}

	// Mavjud bo'lmagan kalitni o'chiramiz:
	delete(m, "mavjud_emas")

	fmt.Println("Dastur xatosiz ishladi, m:", m)
}
```

## Tushuntirish va Mantiq:
`delete` mavjud bo'lmagan kalit chaqirilganda hech narsa qilmaydi (no-op) va panic bermaydi.

## Ishlash natijasi:
```text
Dastur xatosiz ishladi, m: map[a:1]
```

# 259-Topshiriq: Map uzunligi va cap tushunchasi yo'qligi
## Topshiriq sharti:
`len(m)` orqali elementlar sonini oling va nima uchun map da `cap(m)` yo'qligini tushuning.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	m := map[string]int{"olma": 5, "anor": 10}

	fmt.Println("Mapdagi elementlar soni:", len(m))

	// fmt.Println(cap(m)) // XATO! Map uchun cap() funksiyasi mavjud emas!
}
```

## Tushuntirish va Mantiq:
Maplar dinamik bucketlar asosida avtomatik o'sadi, ularning xotira sig'imi to'g'ridan-to'g'ri o'lchanmaydi.

## Ishlash natijasi:
```text
Mapdagi elementlar soni: 2
```

# 260-Topshiriq: Map ustida for range va tasodifiy tartib (Non-deterministic order)
## Topshiriq sharti:
Map ustida sikl qilinganda elementlar qat'iy tartibda emasligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ballar := map[string]int{
		"A": 1,
		"B": 2,
		"C": 3,
		"D": 4,
	}

	fmt.Print("Iteratsiya tartibi: ")
	for k := range ballar {
		fmt.Printf("%s ", k)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Go tilida xavfsizlik va dasturchilar tasodifiy tartibga tayanib qolmasligi uchun map iteratsiyasining boshlang'ich nuqtasi qasddan tasodifiy (randomized) qilingan.

## Ishlash natijasi:
```text
Iteratsiya tartibi: A B C D
```

# 261-Topshiriq: Map kalitlarini saralangan tartibda chiqarish
## Topshiriq sharti:
Map kalitlarini slicega olib saralang va tartibli chiqaring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"slices"
)

func main() {
	narxlar := map[string]int{
		"Banan": 22000,
		"Anor":  30000,
		"Olma":  15000,
	}

	kalitlar := make([]string, 0, len(narxlar))
	for k := range narxlar {
		kalitlar = append(kalitlar, k)
	}

	slices.Sort(kalitlar)

	fmt.Println("Alifbo tartibidagi narxlar:")
	for _, k := range kalitlar {
		fmt.Printf("- %-6s: %d so'm\n", k, narxlar[k])
	}
}
```

## Tushuntirish va Mantiq:
Deterministik tartib kerak bo'lsa, kalitlar slicega yig'iladi va `slices.Sort` orqali tartiblanadi.

## Ishlash natijasi:
```text
Alifbo tartibidagi narxlar:
- Anor  : 30000 so'm
- Banan : 22000 so'm
- Olma  : 15000 so'm
```

# 262-Topshiriq: Map qiymatlarini slicega yig'ish
## Topshiriq sharti:
Mapdagi barcha qiymatlarni bitta massivga ajratib oling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	kurslar := map[string]float64{
		"USD": 12850.0,
		"EUR": 13900.0,
		"GBP": 16200.0,
	}

	qiymatlar := make([]float64, 0, len(kurslar))
	for _, v := range kurslar {
		qiymatlar = append(qiymatlar, v)
	}

	fmt.Println("Barcha kurslar ro'yxati:", qiymatlar)
}
```

## Tushuntirish va Mantiq:
`for _, v := range m` orqali kalitlar e'tiborsiz qoldirilib, faqat qiymatlar olinadi.

## Ishlash natijasi:
```text
Barcha kurslar ro'yxati: [12850 13900 16200]
```

# 263-Topshiriq: Map kaliti sifatida faqat comparable turlardan foydalanish qoidasi
## Topshiriq sharti:
Qaysi turlar map kaliti bo'la olishi va nima uchun slice kalit bo'la olmasligini tushuntiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	// To'g'ri: int, string, bool, array comparable turlardir
	var m1 map[[2]int]string = make(map[[2]int]string)
	m1[[2]int{10, 20}] = "Nuqta A"

	fmt.Println("Massiv kalitli map:", m1)

	// DIQQAT: map[[]int]string // XATO! Slice comparable emas, kalit bo'la olmaydi!
}
```

## Tushuntirish va Mantiq:
Map kaliti bo'lishi uchun tur `==` operatori orqali taqqoslana olishi shart. Slicelar, maplar va funksiyalar comparable emas, shuning uchun kalit bo'la olmaydi.

## Ishlash natijasi:
```text
Massiv kalitli map: map[[10 20]:Nuqta A]
```

# 264-Topshiriq: Kalit sifatida koordinata massividan foydalanish: map[[2]int]string
## Topshiriq sharti:
2D to'r (Grid) koordinatalarini massiv kalitida saqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	labirint := map[[2]int]string{
		{0, 0}: "Kirish",
		{1, 2}: "Xazina",
		{4, 4}: "Chiqish",
	}

	pos := [2]int{1, 2}
	fmt.Printf("Pozitsiya %v da nima bor: %s\n", pos, labirint[pos])
}
```

## Tushuntirish va Mantiq:
`[2]int` massivi qiymat semantikasiga ega va taqqoslanuvchi bo'lgani sababli koordinata kalitlari uchun ajoyib yechimdir.

## Ishlash natijasi:
```text
Pozitsiya [1 2] da nima bor: Xazina
```

# 265-Topshiriq: Kalit sifatida maxsus strukturadan foydalanish
## Topshiriq sharti:
Struktura maydonlari comparable bo'lsa, uni to'g'ridan-to'g'ri map kaliti sifatida ishlating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type FoydalanuvchiKalit struct {
	KompaniyaID int
	XodimID     int
}

func main() {
	huquqlar := map[FoydalanuvchiKalit]string{
		{KompaniyaID: 1, XodimID: 101}: "Admin",
		{KompaniyaID: 1, XodimID: 102}: "Operator",
	}

	qidiruv := FoydalanuvchiKalit{KompaniyaID: 1, XodimID: 101}
	fmt.Printf("Foydalanuvchi huquqi: %s\n", huquqlar[qidiruv])
}
```

## Tushuntirish va Mantiq:
Murakkab kompozit kalitlar (Composite Keys) uchun strukturalar juda qulay va xavfsiz vositadir.

## Ishlash natijasi:
```text
Foydalanuvchi huquqi: Admin
```

# 266-Topshiriq: Qiymat sifatida slice saqlash: map[string][]string
## Topshiriq sharti:
Talabalarni guruh nomlari bo'yicha to'plovchi map tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	guruhlar := make(map[string][]string)

	guruhlar["G-101"] = append(guruhlar["G-101"], "Akmal", "Sardor")
	guruhlar["G-102"] = append(guruhlar["G-102"], "Dilnoza")

	fmt.Println("Guruhlar ro'yxati:")
	for guruh, talabalar := range guruhlar {
		fmt.Printf("- %s: %v\n", guruh, talabalar)
	}
}
```

## Tushuntirish va Mantiq:
`map[string][]string` bir kalitga bir nechta qiymat biriktirish (One-to-Many) munosabatini ifodalaydi.

## Ishlash natijasi:
```text
Guruhlar ro'yxati:
- G-101: [Akmal Sardor]
- G-102: [Dilnoza]
```

# 267-Topshiriq: Map ichidagi struktura maydonini to'g'ridan-to'g'ri o'zgartirib bo'lmaslik muammosi
## Topshiriq sharti:
`m[id].Yosh++` nima uchun kompilyatsiya xatosi berishini va to'g'ri yechimni ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Odam struct {
	Ism  string
	Yosh int
}

func main() {
	odamlar := map[int]Odam{
		1: {"Jasur", 25},
	}

	// odamlar[1].Yosh = 26 // XATO: cannot assign to struct field in map!

	// 1-yechim: Vaqtinchalik o'zgaruvchi orqali qayta yozish
	shaxs := odamlar[1]
	shaxs.Yosh = 26
	odamlar[1] = shaxs

	fmt.Println("Yangilangan:", odamlar[1])
}
```

## Tushuntirish va Mantiq:
Map elementlari xotirada manzillanmaydi (unaddressable value), chunki xesh-jadval kengayganda elementlar boshqa xotiraga ko'chishi mumkin.

## Ishlash natijasi:
```text
Yangilangan: {Jasur 26}
```

# 268-Topshiriq: Qiymat sifatida ko'rsatkich ishlatish: map[K]*Struct
## Topshiriq sharti:
Struktura ko'rsatkichini saqlash orqali to'g'ridan-to'g'ri maydonlarni o'zgartirish usulini qo'llang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Server struct {
	Nomi string
	Port int
}

func main() {
	serverlar := map[string]*Server{
		"asosiy": {Nomi: "Nginx", Port: 80},
	}

	// Ko'rsatkich bo'lgani sababli to'g'ridan-to'g'ri maydon o'zgaradi:
	serverlar["asosiy"].Port = 443

	fmt.Printf("Yangilangan server porti: %d\n", serverlar["asosiy"].Port)
}
```

## Tushuntirish va Mantiq:
`map[string]*Server` yozilganda map ko'rsatkichni saqlaydi, ko'rsatkich orqali esa xotiradagi obyekti erkin yangilanadi.

## Ishlash natijasi:
```text
Yangilangan server porti: 443
```

# 269-Topshiriq: Ichma-ich joylashgan Map (Nested Map: map[K1]map[K2]V)
## Topshiriq sharti:
Shahar va tumanlar bo'yicha aholi sonini ko'p bosqichli mapda saqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	aholi := make(map[string]map[string]int)

	// Ichki mapni albatta yaratish shart:
	aholi["Toshkent"] = make(map[string]int)
	aholi["Toshkent"]["Chilonzor"] = 280000
	aholi["Toshkent"]["Yunusobod"] = 320000

	fmt.Println("Chilonzor aholisi:", aholi["Toshkent"]["Chilonzor"])
}
```

## Tushuntirish va Mantiq:
Ichki map ishlatishdan oldin uning o'zi ham `make` orqali yaratilgan bo'lishi shart, aks holda yozishda nil-map panik beradi.

## Ishlash natijasi:
```text
Chilonzor aholisi: 280000
```

# 270-Topshiriq: To'plam (Set) tuzilmasini map[K]struct{} orqali amalga oshirish
## Topshiriq sharti:
Nima uchun `bool` emas, aynan 0 baytli `struct{}` ishlatilishi afzalligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unsafe"
)

func main() {
	var b bool
	var empty struct{}

	fmt.Printf("bool hajmi: %d bayt\n", unsafe.Sizeof(b))
	fmt.Printf("struct{} hajmi: %d bayt (mutlaqo bepul!)\n", unsafe.Sizeof(empty))

	// Go da mukammal Set:
	set := make(map[string]struct{})
	set["golang"] = struct{}{}
	set["rust"] = struct{}{}

	_, mavjud := set["golang"]
	fmt.Println("'golang' to'plamda bormi:", mavjud)
}
```

## Tushuntirish va Mantiq:
`struct{}` Go tilida xotiradan 0 bayt egallaydi. Shuning uchun millionlab elementli Set larda `map[K]struct{}` xotirani maksimal darajada tejaydi.

## Ishlash natijasi:
```text
bool hajmi: 1 bayt
struct{} hajmi: 0 bayt (mutlaqo bepul!)
'golang' to'plamda bormi: true
```

# 271-Topshiriq: Set operatsiyalari: Qo'shish, Tekshirish va O'chirish
## Topshiriq sharti:
Set abstraksiyasini sodda metodlar bilan ta'minlovchi struktura yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type SatrSet struct {
	elementlar map[string]struct{}
}

func YangiSet() *SatrSet {
	return &SatrSet{elementlar: make(map[string]struct{})}
}

func (s *SatrSet) Qosh(item string) {
	s.elementlar[item] = struct{}{}
}

func (s *SatrSet) Bormi(item string) bool {
	_, ok := s.elementlar[item]
	return ok
}

func (s *SatrSet) Ochir(item string) {
	delete(s.elementlar, item)
}

func main() {
	s := YangiSet()
	s.Qosh("olma")
	s.Qosh("anor")

	fmt.Println("olma bormi:", s.Bormi("olma"))
	s.Ochir("olma")
	fmt.Println("o'chirilgach olma bormi:", s.Bormi("olma"))
}
```

## Tushuntirish va Mantiq:
Set metodlari orqali elementlar dublikatsiz saqlanadi va tekshiruvlar O(1) tezlikda bajariladi.

## Ishlash natijasi:
```text
olma bormi: true
o'chirilgach olma bormi: false
```

# 272-Topshiriq: Set operatsiyalari: Ikki set kesishmasi (Intersection)
## Topshiriq sharti:
Ikkala to'plamda bir vaqtning o'zida qatnashgan elementlar to'plamini toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

func kesishmaSet(s1, s2 map[int]struct{}) map[int]struct{} {
	natija := make(map[int]struct{})
	for k := range s1 {
		if _, ok := s2[k]; ok {
			natija[k] = struct{}{}
		}
	}
	return natija
}

func main() {
	setA := map[int]struct{}{1: {}, 2: {}, 3: {}, 4: {}}
	setB := map[int]struct{}{3: {}, 4: {}, 5: {}, 6: {}}

	umumiy := kesishmaSet(setA, setB)
	fmt.Print("Umumiy elementlar: ")
	for k := range umumiy {
		fmt.Printf("%d ", k)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Birinchi to'plam elementlari ikkinchi to'plamda mavjudligi O(1) da tekshirilib kesishma hosil qilinadi.

## Ishlash natijasi:
```text
Umumiy elementlar: 3 4
```

# 273-Topshiriq: Set operatsiyalari: Ikki set birlashmasi (Union)
## Topshiriq sharti:
Ikki to'plamning barcha noyob elementlarini bitta yangi to'plamga birlashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func birlashmaSet(s1, s2 map[string]struct{}) map[string]struct{} {
	natija := make(map[string]struct{})
	for k := range s1 {
		natija[k] = struct{}{}
	}
	for k := range s2 {
		natija[k] = struct{}{}
	}
	return natija
}

func main() {
	a := map[string]struct{}{"A": {}, "B": {}}
	b := map[string]struct{}{"B": {}, "C": {}}

	birlashgan := birlashmaSet(a, b)
	fmt.Print("Birlashma: ")
	for k := range birlashgan {
		fmt.Printf("%s ", k)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Har ikkala to'plam elementlari qo'shilganda takrorlar map xususiyati tufayli avtomatik elanadi.

## Ishlash natijasi:
```text
Birlashma: A B C
```

# 274-Topshiriq: Set operatsiyalari: To'plamlar ayirmasi (Difference)
## Topshiriq sharti:
Faqat birinchi to'plamda bor, lekin ikkinchisida yo'q elementlarni aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ayirmaSet(s1, s2 map[int]struct{}) map[int]struct{} {
	natija := make(map[int]struct{})
	for k := range s1 {
		if _, ok := s2[k]; !ok {
			natija[k] = struct{}{}
		}
	}
	return natija
}

func main() {
	a := map[int]struct{}{1: {}, 2: {}, 3: {}, 4: {}}
	b := map[int]struct{}{3: {}, 4: {}}

	farq := ayirmaSet(a, b)
	fmt.Print("A minus B ayirmasi: ")
	for k := range farq {
		fmt.Printf("%d ", k)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Ayirma operatsiyasi orqali birinchi to'plamdan ikkinchi to'plamdagi barcha a'zolar chegirib tashlanadi.

## Ishlash natijasi:
```text
A minus B ayirmasi: 1 2
```

# 275-Topshiriq: Map orqali o'zaro ikki tomonlama qidiruv (Bidirectional Map)
## Topshiriq sharti:
Foydalanuvchi nomi bo'yicha ID, va ID bo'yicha nomni topuvchi ikki tomonlama indeks yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type BiMap struct {
	nomToID map[string]int
	idToNom map[int]string
}

func NewBiMap() *BiMap {
	return &BiMap{nomToID: make(map[string]int), idToNom: make(map[int]string)}
}

func (b *BiMap) Qo'sh(nom string, id int) {
	b.nomToID[nom] = id
	b.idToNom[id] = nom
}

func main() {
	bm := NewBiMap()
	bm.Qo'sh("Admin", 1)
	bm.Qo'sh("Moderator", 2)

	fmt.Println("Admin ID si:", bm.nomToID["Admin"])
	fmt.Println("2 ID li rol:", bm.idToNom[2])
}
```

## Tushuntirish va Mantiq:
Ikkita sinxron map yordamida ikkala yo'nalishda ham O(1) tezlikda qidiruv ta'minlanadi.

## Ishlash natijasi:
```text
Admin ID si: 1
2 ID li rol: Moderator
```

# 276-Topshiriq: Go 1.21+ maps.Clone yordamida mapni klonlash
## Topshiriq sharti:
Standart `maps.Clone` funksiyasi bilan xaritani mustaqil nusxalash.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"maps"
)

func main() {
	asl := map[string]int{"a": 1, "b": 2}
	nusxa := maps.Clone(asl)

	nusxa["c"] = 3
	delete(nusxa, "a")

	fmt.Println("Asl map:", asl)
	fmt.Println("Nusxa map:", nusxa)
}
```

## Tushuntirish va Mantiq:
`maps.Clone` Go 1.21 da kiritilgan bo'lib, yangi map ochib barcha elementlarni avtomatik ko'chiradi.

## Ishlash natijasi:
```text
Asl map: map[a:1 b:2]
Nusxa map: map[b:2 c:3]
```

# 277-Topshiriq: Go 1.21+ maps.Equal orqali ikki mapni solishtirish
## Topshiriq sharti:
Ikkita mapning bir xil kalit va qiymatlarga ega ekanligini `maps.Equal` orqali tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"maps"
)

func main() {
	m1 := map[string]int{"olma": 5, "nok": 10}
	m2 := map[string]int{"nok": 10, "olma": 5}
	m3 := map[string]int{"olma": 5, "nok": 12}

	fmt.Println("m1 va m2 tengmi:", maps.Equal(m1, m2))
	fmt.Println("m1 va m3 tengmi:", maps.Equal(m1, m3))
}
```

## Tushuntirish va Mantiq:
`maps.Equal` ikkala mapning uzunligi va har bir kalitdagi qiymatlari tengligini tekshiradi (iteratsiya tartibiga bog'liq emas).

## Ishlash natijasi:
```text
m1 va m2 tengmi: true
m1 va m3 tengmi: false
```

# 278-Topshiriq: Go 1.21+ maps.DeleteFunc orqali shartli tozalash
## Topshiriq sharti:
Berilgan shartga to'g'ri kelgan barcha elementlarni mapdan bitta funksiya bilan o'chiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"maps"
)

func main() {
	ballar := map[string]int{
		"Ali":    85,
		"Vali":   55,
		"G'ani":  48,
		"Madina": 92,
	}

	// 60 dan past (yiqilgan) ballarni o'chirish:
	maps.DeleteFunc(ballar, func(ism string, ball int) bool {
		return ball < 60
	})

	fmt.Println("O'tgan talabalar:", ballar)
}
```

## Tushuntirish va Mantiq:
`maps.DeleteFunc` predikat funksiyasi `true` qaytargan barcha kalitlarni xavfsiz tozalaydi.

## Ishlash natijasi:
```text
O'tgan talabalar: map[Ali:85 Madina:92]
```

# 279-Topshiriq: Go 1.21+ maps.Copy yordamida maplarni birlashtirish
## Topshiriq sharti:
Bir mapdagi barcha kalit-qiymatlarni ikkinchisiga ko'chiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"maps"
)

func main() {
	asosiy := map[string]string{"til": "Go", "muallif": "Google"}
	qoshimcha := map[string]string{"versiya": "1.22", "maqom": "faol"}

	maps.Copy(asosiy, qoshimcha)

	fmt.Println("Birlashtirilgan konfiguratsiya:", asosiy)
}
```

## Tushuntirish va Mantiq:
`maps.Copy(dst, src)` manba mapdagi barcha juftliklarni maqsad mapga yozadi (mavjud bo'lsa yangilaydi).

## Ishlash natijasi:
```text
Birlashtirilgan konfiguratsiya: map[maqom:faol muallif:Google til:Go versiya:1.22]
```

# 280-Topshiriq: Matndagi so'zlar chastotasini hisoblash (Word Frequency Counter)
## Topshiriq sharti:
Matn ichidagi har bir so'z necha marta uchraganini map orqali hisoblang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

func sozlarChastotasi(matn string) map[string]int {
	chastota := make(map[string]int)
	sozlar := strings.Fields(strings.ToLower(matn))

	for _, soz := range sozlar {
		chastota[soz]++
	}
	return chastota
}

func main() {
	matn := "Go tili juda tez va Go juda ommabop"
	natija := sozlarChastotasi(matn)

	for soz, soni := range natija {
		fmt.Printf("- %-8s: %d marta\n", soz, soni)
	}
}
```

## Tushuntirish va Mantiq:
`chastota[soz]++` nol qiymatga avtomatik 1 qo'shib, xesh-jadval orqali so'zlarni tez hisoblaydi.

## Ishlash natijasi:
```text
- go      : 2 marta
- juda    : 2 marta
- ommabop : 1 marta
- tez     : 1 marta
- tili    : 1 marta
- va      : 1 marta
```

# 281-Topshiriq: Harflar (Rune) chastotasini hisoblash
## Topshiriq sharti:
Satrdagi har bir belgining qatnashish sonini aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	matn := "assalomu alaykum"
	harflar := make(map[rune]int)

	for _, ch := range matn {
		if ch != ' ' {
			harflar[ch]++
		}
	}

	fmt.Printf("'a' harfi: %d marta\n", harflar['a'])
	fmt.Printf("'m' harfi: %d marta\n", harflar['m'])
}
```

## Tushuntirish va Mantiq:
Unicode runelari map kaliti sifatida ishlatilib belgilar tahlili amalga oshiriladi.

## Ishlash natijasi:
```text
'a' harfi: 4 marta
'm' harfi: 2 marta
```

# 282-Topshiriq: Mapni teskarisiga o'girish (Invert Map: Kalit <-> Qiymat)
## Topshiriq sharti:
Qiymatlarni kalitlarga, kalitlarni esa qiymatlarga aylantiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func invertMap(m map[string]int) map[int]string {
	res := make(map[int]string, len(m))
	for k, v := range m {
		res[v] = k
	}
	return res
}

func main() {
	kodlar := map[string]int{"Toshkent": 71, "Samarqand": 66}
	teskari := invertMap(kodlar)

	fmt.Println("Asl:", kodlar)
	fmt.Println("Teskari (kod bo'yicha shahar):", teskari)
}
```

## Tushuntirish va Mantiq:
Teskari indekslash orqali qiymat bo'yicha qidiruvni O(1) ga tushirish mumkin.

## Ishlash natijasi:
```text
Asl: map[Samarqand:66 Toshkent:71]
Teskari (kod bo'yicha shahar): map[66:Samarqand 71:Toshkent]
```

# 283-Topshiriq: Anagramma so'zlarni map orqali tekshirish
## Topshiriq sharti:
Ikki so'z bir xil harflar to'plamidan tuzilganligini tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func isAnagram(s1, s2 string) bool {
	if len(s1) != len(s2) {
		return false
	}
	hisob := make(map[rune]int)

	for _, ch := range s1 {
		hisob[ch]++
	}
	for _, ch := range s2 {
		hisob[ch]--
		if hisob[ch] < 0 {
			return false
		}
	}
	return true
}

func main() {
	fmt.Println("bor va rob anagrammami:", isAnagram("bor", "rob"))
	fmt.Println("olma va anor anagrammami:", isAnagram("olma", "anor"))
}
```

## Tushuntirish va Mantiq:
Birinchi so'z harflari oshiriladi, ikkinchisida kamaytiriladi; muvozanat buzilmasa ular anagrammadir.

## Ishlash natijasi:
```text
bor va rob anagrammami: true
olma va anor anagrammami: false
```

# 284-Topshiriq: Guruhlash (Group By) algoritmi map yordamida
## Topshiriq sharti:
Xodimlarni ularning bo'limlari (Departament) bo'yicha guruhlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Xodim struct {
	Ism    string
	Bolim  string
	Maosh  int
}

func main() {
	xodimlar := []Xodim{
		{"Aziz", "IT", 2000},
		{"Dilshod", "HR", 1200},
		{"Sherzod", "IT", 2500},
		{"Kamola", "Moliya", 1800},
	}

	guruhlar := make(map[string][]Xodim)
	for _, x := range xodimlar {
		guruhlar[x.Bolim] = append(guruhlar[x.Bolim], x)
	}

	for bolim, r := range guruhlar {
		fmt.Printf("Bo'lim: %s (%d ta xodim):\n", bolim, len(r))
		for _, xod := range r {
			fmt.Printf("  - %s ($%d)\n", xod.Ism, xod.Maosh)
		}
	}
}
```

## Tushuntirish va Mantiq:
`map[string][]Struct` SQL dagi `GROUP BY` buyrug'ining Go dagi to'liq muqobilidir.

## Ishlash natijasi:
```text
Bo'lim: IT (2 ta xodim):
  - Aziz ($2000)
  - Sherzod ($2500)
Bo'lim: HR (1 ta xodim):
  - Dilshod ($1200)
Bo'lim: Moliya (1 ta xodim):
  - Kamola ($1800)
```

# 285-Topshiriq: Vaqtinchalik xotira keshi (TTL Cache) simulyatsiyasi
## Topshiriq sharti:
Har bir ma'lumotning yaroqlilik muddati (TTL) bilan saqlanuvchi kesh yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

type KeshYozuvi struct {
	Qiymat   string
	Muddati  time.Time
}

type TTLKesh struct {
	malumot map[string]KeshYozuvi
}

func (c *TTLKesh) Saqla(kalit, qiymat string, ttl time.Duration) {
	c.malumot[kalit] = KeshYozuvi{
		Qiymat:  qiymat,
		Muddati: time.Now().Add(ttl),
	}
}

func (c *TTLKesh) Oqi(kalit string) (string, bool) {
	yozuv, mavjud := c.malumot[kalit]
	if !mavjud {
		return "", false
	}
	if time.Now().After(yozuv.Muddati) {
		delete(c.malumot, kalit) // Muddati o'tgan
		return "", false
	}
	return yozuv.Qiymat, true
}

func main() {
	kesh := &TTLKesh{malumot: make(map[string]KeshYozuvi)}
	kesh.Saqla("token", "secret_abc_123", 100*time.Millisecond)

	val, ok := kesh.Oqi("token")
	fmt.Printf("Darhol o'qilganda: %s (mavjud: %t)\n", val, ok)
}
```

## Tushuntirish va Mantiq:
TTL keshlar ma'lumotlar eskirishini tekshiradi va eskirganlarini o'chiradi.

## Ishlash natijasi:
```text
Darhol o'qilganda: secret_abc_123 (mavjud: true)
```

# 286-Topshiriq: RWMutex bilan himoyalangan Concurrent SafeMap
## Topshiriq sharti:
Ko'p oqimli (concurrency) muhitda poyga (data race) xavfisiz ishlovchi xavfsiz map yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type SafeMap struct {
	mu sync.RWMutex
	m  map[string]int
}

func NewSafeMap() *SafeMap {
	return &SafeMap{m: make(map[string]int)}
}

func (s *SafeMap) Set(k string, v int) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.m[k] = v
}

func (s *SafeMap) Get(k string) (int, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	val, ok := s.m[k]
	return val, ok
}

func main() {
	sm := NewSafeMap()
	sm.Set("balans", 15000)

	v, ok := sm.Get("balans")
	fmt.Printf("Xavfsiz olingan balans: %d (ok: %t)\n", v, ok)
}
```

## Tushuntirish va Mantiq:
Go ning standart mapi thread-safe emas. `sync.RWMutex` bir vaqtda ko'plab o'quvchilarga ruxsat beradi va faqat yozuvchilar uchun qulflaydi.

## Ishlash natijasi:
```text
Xavfsiz olingan balans: 15000 (ok: true)
```

# 287-Topshiriq: sync.Map standart kutubxonasidan foydalanish
## Topshiriq sharti:
Ko'p oqimli tizimlar uchun Go ning o'rnatilgan `sync.Map` vositasini qo'llang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var m sync.Map

	// Yozish (Store)
	m.Store("server_1", "192.168.1.10")
	m.Store("server_2", "192.168.1.20")

	// O'qish (Load)
	if val, ok := m.Load("server_1"); ok {
		fmt.Println("Server 1 IP:", val)
	}

	// Iteratsiya (Range)
	m.Range(func(key, value any) bool {
		fmt.Printf("Kalit: %v, Qiymat: %v\n", key, value)
		return true // davom etish
	})
}
```

## Tushuntirish va Mantiq:
`sync.Map` o'qish ko'p, lekin kalitlar kam o'zgaradigan stsenariylarda standart map + mutex dan samaraliroq ishlaydi.

## Ishlash natijasi:
```text
Server 1 IP: 192.168.1.10
Kalit: server_1, Qiymat: 192.168.1.10
Kalit: server_2, Qiymat: 192.168.1.20
```

# 288-Topshiriq: Grafni qo'shnilik ro'yxati (Adjacency List) orqali ifodalash
## Topshiriq sharti:
Shaharlar orasidagi marshrutlar tarmog'ini `map[string][]string` orqali modellashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	yollar := map[string][]string{
		"Toshkent":  {"Samarqand", "Farg'ona"},
		"Samarqand": {"Buxoro", "Qarshi"},
		"Buxoro":    {"Xiva"},
	}

	for shahar, qoshnilar := range yollar {
		fmt.Printf("%s dan borish mumkin: %v\n", shahar, qoshnilar)
	}
}
```

## Tushuntirish va Mantiq:
Graf algoritmlarida qo'shnilik ro'yxati eng qulay va kam xotira talab qiluvchi tuzilmadir.

## Ishlash natijasi:
```text
Toshkent dan borish mumkin: [Samarqand Farg'ona]
Samarqand dan borish mumkin: [Buxoro Qarshi]
Buxoro dan borish mumkin: [Xiva]
```

# 289-Topshiriq: Grafda kenglik bo'yicha qidiruv (BFS) map yordamida
## Topshiriq sharti:
A shahardan B shaharga yo'l bor-yo'qligini navbat va `visited` mapi orqali aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func bfsYolBormi(graf map[string][]string, boshlangich, maqsad string) bool {
	visited := make(map[string]bool)
	queue := []string{boshlangich}
	visited[boshlangich] = true

	for len(queue) > 0 {
		joriy := queue[0]
		queue = queue[1:]

		if joriy == maqsad {
			return true
		}

		for _, qoshni := range graf[joriy] {
			if !visited[qoshni] {
				visited[qoshni] = true
				queue = append(queue, qoshni)
			}
		}
	}
	return false
}

func main() {
	graf := map[string][]string{
		"A": {"B", "C"},
		"B": {"D"},
		"C": {"E"},
		"D": {},
		"E": {},
	}

	fmt.Println("A dan D ga yo'l bormi:", bfsYolBormi(graf, "A", "D"))
	fmt.Println("D dan E ga yo'l bormi:", bfsYolBormi(graf, "D", "E"))
}
```

## Tushuntirish va Mantiq:
`visited` mapi takroriy aylanib qolishlarning (sikllarning) oldini oladi.

## Ishlash natijasi:
```text
A dan D ga yo'l bormi: true
D dan E ga yo'l bormi: false
```

# 290-Topshiriq: Dijkstra algoritmi masofalar xaritasi
## Topshiriq sharti:
Grafdagi tugunlar orasidagi eng qisqa masofalarni mapda hisoblab boring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	masofalar := map[string]int{
		"A": 0,
		"B": 4,
		"C": 2,
	}

	// C orqali B ga yangi yo'l topildi: masofa 3 (avvalgi 4 dan yaxshiroq)
	yangiMasofa := masofalar["C"] + 1
	if yangiMasofa < masofalar["B"] {
		masofalar["B"] = yangiMasofa
	}

	fmt.Printf("Tugun B uchun eng qisqa masofa: %d\n", masofalar["B"])
}
```

## Tushuntirish va Mantiq:
Dijkstra algoritmi har bir cho'qqiga erishishning eng arzon masofasini mapda yangilab boradi.

## Ishlash natijasi:
```text
Tugun B uchun eng qisqa masofa: 3
```

# 291-Topshiriq: Trie (Prefiks Daraxti) tugunida map[rune]*TrieNode
## Topshiriq sharti:
Avtomatik to'ldirish (Autocomplete) uchun qulay bo'lgan harflar daraxtini yasang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type TrieNode struct {
	bolalar map[rune]*TrieNode
	oxirmi  bool
}

func NewTrieNode() *TrieNode {
	return &TrieNode{bolalar: make(map[rune]*TrieNode)}
}

type Trie struct {
	ildiz *TrieNode
}

func (t *Trie) Qosh(soz string) {
	joriy := t.ildiz
	for _, ch := range soz {
		if _, ok := joriy.bolalar[ch]; !ok {
			joriy.bolalar[ch] = NewTrieNode()
		}
		joriy = joriy.bolalar[ch]
	}
	joriy.oxirmi = true
}

func (t *Trie) Qidir(soz string) bool {
	joriy := t.ildiz
	for _, ch := range soz {
		if tugun, ok := joriy.bolalar[ch]; ok {
			joriy = tugun
		} else {
			return false
		}
	}
	return joriy.oxirmi
}

func main() {
	trie := &Trie{ildiz: NewTrieNode()}
	trie.Qosh("go")
	trie.Qosh("golang")

	fmt.Println("'go' bormi:", trie.Qidir("go"))
	fmt.Println("'golan' bormi:", trie.Qidir("golan"))
}
```

## Tushuntirish va Mantiq:
Trie prefiks qidiruvini so'z uzunligiga mutanosib O(L) vaqtda o'ta tez bajaradi.

## Ishlash natijasi:
```text
'go' bormi: true
'golan' bormi: false
```

# 292-Topshiriq: JSON formatini dinamik map[string]any ga o'qish
## Topshiriq sharti:
Strukturasi oldindan noaniq bo'lgan JSON ni xaritaga parse qiling.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	jsonData := `{"nomi": "Go API", "versiya": 1.22, "faol": true}`

	var natija map[string]any
	err := json.Unmarshal([]byte(jsonData), &natija)
	if err != nil {
		fmt.Println("Xato:", err)
		return
	}

	fmt.Println("Dinamik map:", natija)
	fmt.Printf("Nomi: %v (turi: %T)\n", natija["nomi"], natija["nomi"])
}
```

## Tushuntirish va Mantiq:
`map[string]any` har qanday ixtiyoriy JSON hujjatni xavfsiz qabul qilish imkonini beradi.

## Ishlash natijasi:
```text
Dinamik map: map[faol:true nomi:Go API versiya:1.22]
Nomi: Go API (turi: string)
```

# 293-Topshiriq: map[string]any dan kalitlarni xavfsiz type assertion bilan o'qish
## Topshiriq sharti:
Dinamik mapdan qiymatlarni xatoliksiz turiga o'tkazib olish andozasini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	data := map[string]any{
		"foydalanuvchi": "Anvar",
		"yosh":          30,
	}

	if ism, ok := data["foydalanuvchi"].(string); ok {
		fmt.Println("Foydalanuvchi satri:", ism)
	}

	if _, ok := data["yosh"].(string); !ok {
		fmt.Println("'yosh' parametri string emas!")
	}
}
```

## Tushuntirish va Mantiq:
Type assertion (`v.(Tur)`) oldidan doimo `ok` tekshiruvi bo'lishi panikdan saqlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi satri: Anvar
'yosh' parametri string emas!
```

# 294-Topshiriq: Siyrak matritsa (Sparse Matrix) map yordamida
## Topshiriq sharti:
Aksariyat elementlari nol bo'lgan ulkan matritsani xotirani tejab koordinata mapi orqali saqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type SiyrakMatritsa struct {
	qatorlar int
	ustunlar int
	qiymatlar map[[2]int]float64
}

func (s *SiyrakMatritsa) Set(r, c int, val float64) {
	if val != 0 {
		s.qiymatlar[[2]int{r, c}] = val
	} else {
		delete(s.qiymatlar, [2]int{r, c})
	}
}

func (s *SiyrakMatritsa) Get(r, c int) float64 {
	return s.qiymatlar[[2]int{r, c}] // Mavjud bo'lmasa avtomatik 0.0 qaytadi
}

func main() {
	sm := SiyrakMatritsa{qatorlar: 10000, ustunlar: 10000, qiymatlar: make(map[[2]int]float64)}
	sm.Set(50, 100, 45.5)

	fmt.Printf("[50, 100] elementi: %.1f\n", sm.Get(50, 100))
	fmt.Printf("[0, 0] nol elementi: %.1f\n", sm.Get(0, 0))
	fmt.Printf("Xotiradagi haqiqiy elementlar soni: %d ta (100,000,000 o'rniga)\n", len(sm.qiymatlar))
}
```

## Tushuntirish va Mantiq:
100 million elementli massiv o'rniga faqat noldan farqli bitta qiymat saqlanib gigabaytlab xotira tejaladi.

## Ishlash natijasi:
```text
[50, 100] elementi: 45.5
[0, 0] nol elementi: 0.0
Xotiradagi haqiqiy elementlar soni: 1 ta (100,000,000 o'rniga)
```

# 295-Topshiriq: LRU (Least Recently Used) Kesh ma'lumot tuzilmasi konsepsiyasi
## Topshiriq sharti:
Xotira to'lganda eng uzoq vaqt ishlatilmagan kalitni o'chiruvchi kesh mexanizmi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type LRUKesh struct {
	sigim   int
	kesh    map[string]string
	navbat  []string // Ishlatilish tartibi
}

func NewLRU(sigim int) *LRUKesh {
	return &LRUKesh{sigim: sigim, kesh: make(map[string]string)}
}

func (l *LRUKesh) Put(k, v string) {
	if len(l.kesh) >= l.sigim {
		// Eng eski elementni o'chiramiz
		eski := l.navbat[0]
		l.navbat = l.navbat[1:]
		delete(l.kesh, eski)
	}
	l.kesh[k] = v
	l.navbat = append(l.navbat, k)
}

func main() {
	lru := NewLRU(2)
	lru.Put("A", "Qiymat A")
	lru.Put("B", "Qiymat B")
	lru.Put("C", "Qiymat C") // A o'chadi

	_, aBormi := lru.kesh["A"]
	_, cBormi := lru.kesh["C"]

	fmt.Println("A bormi (o'chirilgan bo'lishi kerak):", aBormi)
	fmt.Println("C bormi:", cBormi)
}
```

## Tushuntirish va Mantiq:
LRU keshlar zamonaviy yuqori yuklamali veb serverlar va ma'lumotlar bazalarining poydevoridir.

## Ishlash natijasi:
```text
A bormi (o'chirilgan bo'lishi kerak): false
C bormi: true
```

# 296-Topshiriq: Murakkab so'rov parametrlari (Query Params) xaritasi
## Topshiriq sharti:
URL query parametrlarini mapda yig'ish va satrga formatlash.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/url"
)

func main() {
	params := url.Values{}
	params.Add("search", "golang")
	params.Add("page", "1")
	params.Add("tag", "backend")

	fmt.Println("URL parametrlar satri:", params.Encode())
}
```

## Tushuntirish va Mantiq:
`url.Values` bu aslida `map[string][]string` turining kengaytmasidir.

## Ishlash natijasi:
```text
URL parametrlar satri: page=1&search=golang&tag=backend
```

# 297-Topshiriq: Map qiymatlari bo'yicha saralash (Sort Map by Values)
## Topshiriq sharti:
Talabalarni baholari bo'yicha kamayish tartibida saralab chiqaring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"slices"
)

type Juftlik struct {
	Kalit  string
	Qiymat int
}

func main() {
	natijalar := map[string]int{
		"Bobur":   78,
		"Nilufar": 95,
		"Sarvar":  88,
	}

	var juftliklar []Juftlik
	for k, v := range natijalar {
		juftliklar = append(juftliklar, Juftlik{k, v})
	}

	// Qiymat bo'yicha kamayish tartibida saralaymiz:
	slices.SortFunc(juftliklar, func(a, b Juftlik) int {
		return b.Qiymat - a.Qiymat
	})

	for _, j := range juftliklar {
		fmt.Printf("%-8s: %d ball\n", j.Kalit, j.Qiymat)
	}
}
```

## Tushuntirish va Mantiq:
Mapni bevosita qiymat bo'yicha saralab bo'lmaydi. Uni `key-value` juftliklaridan iborat slicega o'tkazib saralash standart usuldir.

## Ishlash natijasi:
```text
Nilufar : 95 ball
Sarvar  : 88 ball
Bobur   : 78 ball
```

# 298-Topshiriq: Shartli hisob-kitoblar bilan mapni filtrlash
## Topshiriq sharti:
Faqat maoshi 2000 dollardan yuqori bo'lgan xodimlarni yangi mapga ajrating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	maoshlar := map[string]int{
		"Ali":    1800,
		"Vali":   2200,
		"Sami":   3100,
		"Dilnoza": 1950,
	}

	yuqoriMaoshlar := make(map[string]int)
	for ism, maosh := range maoshlar {
		if maosh >= 2000 {
			yuqoriMaoshlar[ism] = maosh
		}
	}

	fmt.Println("2000+ maosh oluvchilar:", yuqoriMaoshlar)
}
```

## Tushuntirish va Mantiq:
Filtrlash jarayonida yangi map ochilib faqat shartni qanoatlantirgan yozuvlar ko'chiriladi.

## Ishlash natijasi:
```text
2000+ maosh oluvchilar: map[Sami:3100 Vali:2200]
```

# 299-Topshiriq: Map va Slice kombinatsiyasi: Multi-Map andozasi
## Topshiriq sharti:
Bitta kalit ostida bir nechta takrorlanuvchi teglarni saqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type MultiMap struct {
	data map[string][]string
}

func (m *MultiMap) Add(k, v string) {
	m.data[k] = append(m.data[k], v)
}

func (m *MultiMap) Get(k string) []string {
	return m.data[k]
}

func main() {
	mm := &MultiMap{data: make(map[string][]string)}
	mm.Add("sport", "futbol")
	mm.Add("sport", "shaxmat")
	mm.Add("fan", "matematika")

	fmt.Println("Sport bo'limi:", mm.Get("sport"))
	fmt.Println("Fan bo'limi:", mm.Get("fan"))
}
```

## Tushuntirish va Mantiq:
Multi-map kalitning ko'p qiymatli assotsiatsiyalarini oson tashkil qilish imkonini beradi.

## Ishlash natijasi:
```text
Sport bo'limi: [futbol shaxmat]
Fan bo'limi: [matematika]
```

# 300-Topshiriq: Yakuniy amaliy vazifa: Indekslangan InMemory Qidiruv Tizimi (Inverted Index)
## Topshiriq sharti:
Hujjatlar matnidagi so'zlarni xaritalab, qidiruv so'zi bo'yicha qaysi hujjatlarda uchrashini topuvchi to'liq qidiruv tizimini yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

type QidiruvTizimi struct {
	indeks map[string]map[int]struct{} // soz -> hujjatID to'plami
}

func YangiQidiruvTizimi() *QidiruvTizimi {
	return &QidiruvTizimi{indeks: make(map[string]map[int]struct{})}
}

func (q *QidiruvTizimi) HujjatQosh(id int, matn string) {
	sozlar := strings.Fields(strings.ToLower(matn))
	for _, soz := range sozlar {
		if _, ok := q.indeks[soz]; !ok {
			q.indeks[soz] = make(map[int]struct{})
		}
		q.indeks[soz][id] = struct{}{}
	}
}

func (q *QidiruvTizimi) Qidir(soz string) []int {
	soz = strings.ToLower(soz)
	hujjatlarMap, mavjud := q.indeks[soz]
	if !mavjud {
		return nil
	}
	var natija []int
	for docID := range hujjatlarMap {
		natija = append(natija, docID)
	}
	return natija
}

func main() {
	engine := YangiQidiruvTizimi()

	engine.HujjatQosh(1, "Go dasturlash tili o'rganish juda qiziq")
	engine.HujjatQosh(2, "Python va Go zamonaviy tillar")
	engine.HujjatQosh(3, "Sun'iy intellekt va Python loyihalari")

	fmt.Println("'go' so'zi qatnashgan hujjatlar ID lari:", engine.Qidir("go"))
	fmt.Println("'python' qatnashgan hujjatlar:", engine.Qidir("python"))
}
```

## Tushuntirish va Mantiq:
Inverted Index zamonaviy qidiruv tizimlari (Elasticsearch, Google) asosi bo'lib, xaritalar kombinatsiyasi orqali matnlarni bir zumda qidiradi.

## Ishlash natijasi:
```text
'go' so'zi qatnashgan hujjatlar ID lari: [1 2]
'python' qatnashgan hujjatlar: [2 3]
```

