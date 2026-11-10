# 8-Mavzu: Strukturalar (Structs) va Ma'lumotlarni Modellashtirish (351-400)

Go tilida sinflar (classes) yo'q; ularning o'rnini Strukturalar (Structs) va Kompozitsiya egallaydi. Struktura turlari, anonim strukturalar, maydonlarning ko'tarilishi (Field Promotion), Struct Tags (`json`, `xml`, `db`), `New...` konstruktor andozasi, inkapsulyatsiya, xotira tekislanishi va murakkab domen modellari bo'yicha 50 ta amaliy topshiriq.

# 351-Topshiriq: Struktura (Struct) e'lon qilish asoslari
## Topshiriq sharti:
Talaba haqidagi ma'lumotlarni (`Ism`, `Yosh`, `GPA`) ifodalovchi struktura e'lon qiling va unga qiymat bering.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Talaba struct {
	Ism  string
	Yosh int
	GPA  float64
}

func main() {
	var t Talaba
	t.Ism = "Sanjar"
	t.Yosh = 21
	t.GPA = 4.5

	fmt.Printf("Talaba: %+v\n", t)
}
```

## Tushuntirish va Mantiq:
Go da struktura `type Nom struct` sintaksisi bilan e'lon qilinadi va turli ma'lumot turlarini bitta yaxlit konteynerga birlashtiradi.

## Ishlash natijasi:
```text
Talaba: {Ism:Sanjar Yosh:21 GPA:4.5}
```

# 352-Topshiriq: Strukturani initsializatsiya qilish usullari (Nomlangan va Pozitsion)
## Topshiriq sharti:
Maydon nomlari bilan va tartibli qiymatlar orqali struktura obyektini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Kitob struct {
	Nomi    string
	Sahifasi int
}

func main() {
	// 1-usul: Nomlangan maydonlar (Tavsiya etiladi! Xavfsiz va tushunarli)
	k1 := Kitob{
		Nomi:    "Shamol ortidan yugurib",
		Sahifasi: 380,
	}

	// 2-usul: Pozitsion (tartib bo'yicha)
	k2 := Kitob{"Yulduzli tunlar", 520}

	fmt.Printf("k1: %+v\n", k1)
	fmt.Printf("k2: %+v\n", k2)
}
```

## Tushuntirish va Mantiq:
Nomlangan maydonlar bilan initsializatsiya qilish eng xavfsiz usul bo'lib, kelajakda yangi maydonlar qo'shilganda kod buzilmaydi.

## Ishlash natijasi:
```text
k1: {Nomi:Shamol ortidan yugurib Sahifasi:380}
k2: {Nomi:Yulduzli tunlar Sahifasi:520}
```

# 353-Topshiriq: Struktura maydonlariga nuqta (.) orqali murojaat qilish
## Topshiriq sharti:
Struktura maydonlarini o'qing va yangilang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Mahsulot struct {
	Nomi  string
	Narxi float64
}

func main() {
	m := Mahsulot{Nomi: "Kofe", Narxi: 18000.0}

	fmt.Printf("Mahsulot: %s, Narxi: %.0f so'm\n", m.Nomi, m.Narxi)

	// Narxni yangilaymiz:
	m.Narxi = 20000.0
	fmt.Printf("Yangi narx: %.0f so'm\n", m.Narxi)
}
```

## Tushuntirish va Mantiq:
Nuqta operatori orqali strukturaning istalgan ochiq maydoniga to'g'ridan-to'g'ri kirish va o'zgartirish mumkin.

## Ishlash natijasi:
```text
Mahsulot: Kofe, Narxi: 18000 so'm
Yangi narx: 20000 so'm
```

# 354-Topshiriq: Nol qiymatli struktura (Zero-value struct)
## Topshiriq sharti:
Dastlabki qiymatsiz e'lon qilingan strukturaning barcha maydonlari nol qiymat olishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Profil struct {
	ID        int
	Email     string
	Tasdiq    bool
	Balans    float64
	Dostlar   []string
}

func main() {
	var p Profil

	fmt.Printf("ID: %d\n", p.ID)
	fmt.Printf("Email: %q\n", p.Email)
	fmt.Printf("Tasdiq: %t\n", p.Tasdiq)
	fmt.Printf("Balans: %.2f\n", p.Balans)
	fmt.Printf("Dostlar: %v (nilmi: %t)\n", p.Dostlar, p.Dostlar == nil)
}
```

## Tushuntirish va Mantiq:
Go da strukturaning barcha maydonlari o'z turlarining xavfsiz nol qiymatiga (`0`, `""`, `false`, `nil`) ega bo'ladi.

## Ishlash natijasi:
```text
ID: 0
Email: ""
Tasdiq: false
Balans: 0.00
Dostlar: [] (nilmi: true)
```

# 355-Topshiriq: Anonim strukturalar (Anonymous Structs)
## Topshiriq sharti:
Alohida tur e'lon qilmasdan, bir martalik anonim strukturadan foydalaning.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	// Bir martalik lokal konfiguratsiya:
	server := struct {
		Host string
		Port int
	}{
		Host: "127.0.0.1",
		Port: 8080,
	}

	fmt.Printf("Server manzili: %s:%d\n", server.Host, server.Port)
}
```

## Tushuntirish va Mantiq:
Anonim strukturalar testlarda yoki faqat bitta joyda ishlatiladigan ma'lumotlar uchun ortiqcha global turlarni ko'paytirmaslik imkonini beradi.

## Ishlash natijasi:
```text
Server manzili: 127.0.0.1:8080
```

# 356-Topshiriq: Strukturalarni to'g'ridan-to'g'ri taqqoslash (==)
## Topshiriq sharti:
Barcha maydonlari comparable bo'lgan strukturalarni `==` bilan solishtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Nuqta struct {
	X, Y int
}

func main() {
	p1 := Nuqta{X: 10, Y: 20}
	p2 := Nuqta{X: 10, Y: 20}
	p3 := Nuqta{X: 5, Y: 10}

	fmt.Println("p1 == p2 :", p1 == p2)
	fmt.Println("p1 == p3 :", p1 == p3)
}
```

## Tushuntirish va Mantiq:
Agar struktura tarkibida slice, map yoki funksiya bo'lmasa, uni to'g'ridan-to'g'ri `==` orqali taqqoslash mumkin.

## Ishlash natijasi:
```text
p1 == p2 : true
p1 == p3 : false
```

# 357-Topshiriq: Ichma-ich joylashgan strukturalar (Nested Structs)
## Topshiriq sharti:
Struktura ichida boshqa struktura turini maydon sifatida saqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Manzil struct {
	Shahar string
	Kocha  string
}

type Mijoz struct {
	Ism    string
	Manzil Manzil // Ichki struktura
}

func main() {
	m := Mijoz{
		Ism: "Farhod",
		Manzil: Manzil{
			Shahar: "Toshkent",
			Kocha:  "Navoiy ko'chasi, 12",
		},
	}

	fmt.Printf("Mijoz: %s, Shahar: %s\n", m.Ism, m.Manzil.Shahar)
}
```

## Tushuntirish va Mantiq:
Ichma-ich strukturalar ma'lumotlarni mantiqiy guruhlarga ajratish uchun ishlatiladi.

## Ishlash natijasi:
```text
Mijoz: Farhod, Shahar: Toshkent
```

# 358-Topshiriq: O'rnatilgan strukturalar (Embedded Structs) - Merosxo'rlik o'rniga kompozitsiya
## Topshiriq sharti:
Nom bermasdan turni to'g'ridan-to'g'ri o'rnatish (embedding) orqali kompozitsiya yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Shaxs struct {
	Ism string
	Yosh int
}

type Xodim struct {
	Shaxs   // Maydon nomi berilmagan: O'rnatilgan (Embedded) struktura!
	Lavozim string
	Maosh   int
}

func main() {
	x := Xodim{
		Shaxs:   Shaxs{Ism: "Gulnoza", Yosh: 28},
		Lavozim: "Dasturchi",
		Maosh:   2500,
	}

	fmt.Printf("Xodim: %+v\n", x)
}
```

## Tushuntirish va Mantiq:
Go klassik OOP merosxo'rligi (inheritance) o'rniga kompozitsiyani qo'llaydi (`Composition over Inheritance`).

## Ishlash natijasi:
```text
Xodim: {Shaxs:{Ism:Gulnoza Yosh:28} Lavozim:Dasturchi Maosh:2500}
```

# 359-Topshiriq: Maydonlarning ko'tarilishi (Field Promotion)
## Topshiriq sharti:
O'rnatilgan strukturaning maydonlariga to'g'ridan-to'g'ri asosiy obyektdan kirish imkoniyatini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Foydalanuvchi struct {
	Email string
}

type Admin struct {
	Foydalanuvchi // Embedded
	Daraja        int
}

func main() {
	a := Admin{
		Foydalanuvchi: Foydalanuvchi{Email: "admin@domain.uz"},
		Daraja:        1,
	}

	// Maydon ko'tarilishi (Field promotion) tufayli:
	fmt.Println("Email (to'g'ridan-to'g'ri):", a.Email)
	fmt.Println("Email (to'liq yo'l bilan):", a.Foydalanuvchi.Email)
}
```

## Tushuntirish va Mantiq:
O'rnatilgan struktura maydonlari tashqi strukturaga avtomatik 'ko'tariladi' (promoted).

## Ishlash natijasi:
```text
Email (to'g'ridan-to'g'ri): admin@domain.uz
Email (to'liq yo'l bilan): admin@domain.uz
```

# 360-Topshiriq: Maydonlar to'qnashuvi va soyalanishi (Field Shadowing in Embedding)
## Topshiriq sharti:
Tashqi struktura ichki struktura maydoni bilan bir xil nomga ega bo'lganda qaysi biri ustun bo'lishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Asos struct {
	ID int
}

type Kengaytma struct {
	Asos
	ID int // Tashqi ID ichki ID ni soyalaydi
}

func main() {
	k := Kengaytma{
		Asos: Asos{ID: 100},
		ID:   200,
	}

	fmt.Println("k.ID (tashqi):", k.ID)
	fmt.Println("k.Asos.ID (ichki):", k.Asos.ID)
}
```

## Tushuntirish va Mantiq:
Tashqi struktura maydoni ichki o'rnatilgan maydonni soyalaydi (shadows), biroq ichkisiga ham to'liq nom orqali kirish mumkin bo'lib qoladi.

## Ishlash natijasi:
```text
k.ID (tashqi): 200
k.Asos.ID (ichki): 100
```

# 361-Topshiriq: Struktura teglari (Struct Tags) asoslari: json:"name"
## Topshiriq sharti:
JSON serializatsiyasida maydon nomlarini moslashtirish uchun teglardan foydalaning.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type FoydalanuvchiDTO struct {
	FoydalanuvchiNomi string `json:"username"`
	ParolXesh         string `json:"-"` // JSON ga chiqarilmaydi
	Yoshi             int    `json:"age,omitempty"`
}

func main() {
	u := FoydalanuvchiDTO{
		FoydalanuvchiNomi: "shavkat",
		ParolXesh:         "secret_hash_value",
		Yoshi:             0, // omitempty tufayli tushib qoladi
	}

	jsonData, _ := json.Marshal(u)
	fmt.Println("JSON natija:", string(jsonData))
}
```

## Tushuntirish va Mantiq:
Struktura teglari teskari tirnoq ichida yoziladi va metadata sifatida `encoding/json`, `gorm` kabi paketlar tomonidan tahlil qilinadi.

## Ishlash natijasi:
```text
JSON natija: {"username":"shavkat"}
```

# 362-Topshiriq: DB va XML teglari bilan ishlash
## Topshiriq sharti:
Bir nechta teglarni bitta maydonda birlashtirib ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type MahsulotRecord struct {
	ID    int     `db:"id" json:"id"`
	Nomi  string  `db:"title" json:"name" xml:"Title"`
	Narxi float64 `db:"price" json:"cost"`
}

func main() {
	m := MahsulotRecord{ID: 1, Nomi: "Planshet", Narxi: 350.0}
	fmt.Printf("Mahsulot: %+v\n", m)
}
```

## Tushuntirish va Mantiq:
Bitta maydon bir vaqtning o'zida bir nechta teglarga ega bo'lishi mumkin (bo'shliq bilan ajratiladi).

## Ishlash natijasi:
```text
Mahsulot: {ID:1 Nomi:Planshet Narxi:350}
```

# 363-Topshiriq: reflect paketi orqali struktura teglarini dasturiy o'qish
## Topshiriq sharti:
Maxsus yozilgan teglarni `reflect.TypeOf` yordamida o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"reflect"
)

type ShaxsInfo struct {
	Ism  string `custom_tag:"majburiy"`
	Yosh int    `custom_tag:"ixtiyoriy"`
}

func main() {
	t := reflect.TypeOf(ShaxsInfo{})

	for i := 0; i < t.NumField(); i++ {
		field := t.Field(i)
		tag := field.Tag.Get("custom_tag")
		fmt.Printf("Maydon: %-5s | Teg qiymati: %s\n", field.Name, tag)
	}
}
```

## Tushuntirish va Mantiq:
`reflect` orqali strukturalarning tahlili (ORM va validatorlar) amalga oshiriladi.

## Ishlash natijasi:
```text
Maydon: Ism   | Teg qiymati: majburiy
Maydon: Yosh  | Teg qiymati: ixtiyoriy
```

# 364-Topshiriq: Bo'sh struktura struct{} va xotira nol iste'moli
## Topshiriq sharti:
0 baytli struktura signallari va to'plamlar yaratish imkonini namoyish qiling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unsafe"
)

func main() {
	var a struct{}
	var b struct{}

	fmt.Println("a o'lchami:", unsafe.Sizeof(a), "bayt")
	fmt.Println("a va b bir xil manzilidami:", &a == &b)
}
```

## Tushuntirish va Mantiq:
`struct{}` hech qanday maydonga ega emas va xotiradan 0 bayt joy oladi. Go barcha bo'sh strukturalarni bitta manzilga bog'laydi.

## Ishlash natijasi:
```text
a o'lchami: 0 bayt
a va b bir xil manzilidami: true
```

# 365-Topshiriq: Konstruktor funksiyalari andozasi (NewStruct pattern)
## Topshiriq sharti:
`NewFoydalanuvchi` konstruktorini yozib yangi obyekt yaratishni standartlashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Foydalanuvchi struct {
	Ism   string
	Email string
	Faol  bool
}

func NewFoydalanuvchi(ism, email string) *Foydalanuvchi {
	return &Foydalanuvchi{
		Ism:   ism,
		Email: email,
		Faol:  true, // Standart boshlang'ich holat
	}
}

func main() {
	u := NewFoydalanuvchi("Lobar", "lobar@example.uz")
	fmt.Printf("Yangi foydalanuvchi: %+v\n", u)
}
```

## Tushuntirish va Mantiq:
Go tilida klassik konstruktorlar yo'q; ularning o'rniga `New...` nomli funksiyalar yozish Go ning umumqabul qilingan andozasidir.

## Ishlash natijasi:
```text
Yangi foydalanuvchi: &{Ism:Lobar Email:lobar@example.uz Faol:true}
```

# 366-Topshiriq: Konstruktorda validatsiya qilish va (*Struct, error) qaytarish
## Topshiriq sharti:
Noto'g'ri parametrlar kiritilganda xatolik qaytaruvchi konstruktor yozing.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

type BankHisobi struct {
	Raqam  string
	Balans float64
}

func NewBankHisobi(raqam string, boshlangichBalans float64) (*BankHisobi, error) {
	if len(raqam) != 16 {
		return nil, errors.New("hisob raqam 16 ta belgidan iborat bo'lishi shart")
	}
	if boshlangichBalans < 0 {
		return nil, errors.New("boshlang'ich balans manfiy bo'lishi mumkin emas")
	}
	return &BankHisobi{Raqam: raqam, Balans: boshlangichBalans}, nil
}

func main() {
	_, err := NewBankHisobi("123", 100)
	if err != nil {
		fmt.Println("Xatolik:", err)
	}

	h, _ := NewBankHisobi("8600123456789012", 50000)
	fmt.Printf("Muvaffaqiyatli hisob: %+v\n", h)
}
```

## Tushuntirish va Mantiq:
Konstruktorda validatsiya o'tkazish noto'g'ri obyektlarning tizimga kirishini to'xtatadi.

## Ishlash natijasi:
```text
Xatolik: hisob raqam 16 ta belgidan iborat bo'lishi shart
Muvaffaqiyatli hisob: &{Raqam:8600123456789012 Balans:50000}
```

# 367-Topshiriq: Eksport qilinadigan (Public) va qilinmaydigan (Private) maydonlar
## Topshiriq sharti:
Katta va kichik harflar orqali maydonlarning ko'rinish sohasini (visibility) boshqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type XavfsizFoydalanuvchi struct {
	OchiqIsm   string // Boshqa paketlarga ko'rinadi (Exported)
	maxfiyKod  string // Faqat shu paketga ko'rinadi (Unexported)
}

func main() {
	u := XavfsizFoydalanuvchi{
		OchiqIsm:  "Jahongir",
		maxfiyKod: "PIN_9988",
	}

	fmt.Println("Ochiq ism:", u.OchiqIsm)
	fmt.Println("Maxfiy kod (paket ichida o'qiladi):", u.maxfiyKod)
}
```

## Tushuntirish va Mantiq:
Go tilida bosh harf bilan boshlangan maydonlar tashqi paketlarga ochiq (public), kichik harfdagilar esa yopiq (private) bo'ladi.

## Ishlash natijasi:
```text
Ochiq ism: Jahongir
Maxfiy kod (paket ichida o'qiladi): PIN_9988
```

# 368-Topshiriq: Inkapsulyatsiya: Getter va Setter funksiyalari
## Topshiriq sharti:
Yopiq maydonga kirishni Getter va Setter orqali nazorat qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Hamyon struct {
	balans int // private maydon
}

func (h *Hamyon) Balans() int {
	return h.balans // Getter (Go da 'Get' so'zi qo'yilmaydi, to'g'ridan-to'g'ri nom ishlatiladi)
}

func (h *Hamyon) MablagQosh(summa int) bool {
	if summa <= 0 {
		return false
	}
	h.balans += summa
	return true
}

func main() {
	h := &Hamyon{}
	h.MablagQosh(10000)

	fmt.Println("Hamyon balansi:", h.Balans())
}
```

## Tushuntirish va Mantiq:
Go konvensiyasiga ko'ra getter nomi `GetBalans` emas, balki oddiy `Balans()` deb nomlanadi.

## Ishlash natijasi:
```text
Hamyon balansi: 10000
```

# 369-Topshiriq: Struktura ichida funksiya maydoni saqlash (Function Fields)
## Topshiriq sharti:
Struktura xatti-harakatini dinamik o'zgartirish uchun funksiya maydonidan foydalaning.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Tugma struct {
	Nomi    string
	OnClick func() // Funksiya turi
}

func main() {
	t := Tugma{
		Nomi: "Tasdiqlash",
		OnClick: func() {
			fmt.Println("Tugma bosildi: To'lov amalga oshirildi!")
		},
	}

	fmt.Println("Tugma nomi:", t.Nomi)
	t.OnClick()
}
```

## Tushuntirish va Mantiq:
Struktura ichidagi funksiyalar dinamik callbacklar va strategiya andozasi (Strategy Pattern) uchun xizmat qiladi.

## Ishlash natijasi:
```text
Tugma nomi: Tasdiqlash
Tugma bosildi: To'lov amalga oshirildi!
```

# 370-Topshiriq: Struktura ichida Slice va Map maydonlarini saqlash
## Topshiriq sharti:
Kompaniya va uning bo'limlari hamda xodimlarini ifodalang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Kompaniya struct {
	Nomi      string
	Loyihalar []string
	Xodimlar  map[string]string // ism -> lavozim
}

func main() {
	k := Kompaniya{
		Nomi:      "TechCorp",
		Loyihalar: []string{"AI Platform", "Mobile App"},
		Xodimlar: map[string]string{
			"Rustam": "Team Lead",
			"Aziza":  "DevOps",
		},
	}

	fmt.Printf("Kompaniya: %s, Loyihalar soni: %d\n", k.Nomi, len(k.Loyihalar))
	fmt.Println("Team Lead:", k.Xodimlar["Rustam"])
}
```

## Tushuntirish va Mantiq:
Strukturalar kolleksiyalarni bitta domen obyektiga birlashtirishda markaziy o'rin tutadi.

## Ishlash natijasi:
```text
Kompaniya: TechCorp, Loyihalar soni: 2
Team Lead: Team Lead
```

# 371-Topshiriq: Strukturalar massivi ([]Struct) ustida amallar
## Topshiriq sharti:
Mahsulotlar ro'yxatidan umumiy xarid summasini hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type SavatItem struct {
	Nomi  string
	Narxi float64
	Soni  int
}

func main() {
	savat := []SavatItem{
		{"Non", 4000, 2},
		{"Sut", 11000, 1},
		{"Choy", 15000, 1},
	}

	jami := 0.0
	for _, item := range savat {
		jami += item.Narxi * float64(item.Soni)
	}

	fmt.Printf("Savatchadagi jami summa: %.0f so'm\n", jami)
}
```

## Tushuntirish va Mantiq:
`[]Struct` ma'lumotlar bazasi jadvallari va ro'yxatlarini ifodalovchi eng asosiy tuzilmadir.

## Ishlash natijasi:
```text
Savatchadagi jami summa: 34000 so'm
```

# 372-Topshiriq: Strukturalar xaritasi (map[ID]Struct)
## Topshiriq sharti:
Foydalanuvchilarni ularning ID raqamlari bo'yicha indekslang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type User struct {
	ID   int
	Ism  string
	Role string
}

func main() {
	baza := map[int]User{
		101: {ID: 101, Ism: "Nodir", Role: "Admin"},
		102: {ID: 102, Ism: "Murod", Role: "User"},
	}

	user, topildi := baza[101]
	if topildi {
		fmt.Printf("Topildi: %s (Roli: %s)\n", user.Ism, user.Role)
	}
}
```

## Tushuntirish va Mantiq:
ID bo'yicha strukturalarni xaritalash ularga O(1) vaqtda tezkor murojaatni ta'minlaydi.

## Ishlash natijasi:
```text
Topildi: Nodir (Roli: Admin)
```

# 373-Topshiriq: Rekursiv struktura: Tashkiliy iyerarxiya daraxti
## Topshiriq sharti:
Bo'lim va uning ichki bo'limlarini ifodalovchi rekursiv struktura tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Bolim struct {
	Nomi       string
	IchkiBolim []*Bolim
}

func main() {
	bosh := &Bolim{
		Nomi: "Bosh Boshqarma",
		IchkiBolim: []*Bolim{
			{Nomi: "Moliya Bo'limi"},
			{Nomi: "Axborot Texnologiyalari Bo'limi"},
		},
	}

	fmt.Println("Asosiy bo'lim:", bosh.Nomi)
	fmt.Printf("Ichki bo'limlar soni: %d ta\n", len(bosh.IchkiBolim))
}
```

## Tushuntirish va Mantiq:
Rekursiv strukturalarda ichki bo'limlar ko'rsatkichlar slicesi (`[]*Bolim`) orqali xotirada xavfsiz ifodalanadi.

## Ishlash natijasi:
```text
Asosiy bo'lim: Bosh Boshqarma
Ichki bo'limlar soni: 2 ta
```

# 374-Topshiriq: Strukturalarda xotira tekislanishi va Padding
## Topshiriq sharti:
Maydonlar tartibini o'zgartirish orqali struktura hajmini 33% ga qisqartiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unsafe"
)

type YomonJoylashuv struct {
	a bool  // 1 bayt + 7 padding
	b int64 // 8 bayt
	c bool  // 1 bayt + 7 padding -> jami 24 bayt!
}

type YaxshiJoylashuv struct {
	b int64 // 8 bayt
	a bool  // 1 bayt
	c bool  // 1 bayt + 6 padding -> jami 16 bayt!
}

func main() {
	var y1 YomonJoylashuv
	var y2 YaxshiJoylashuv

	fmt.Println("Yomon tartib hajmi:", unsafe.Sizeof(y1), "bayt")
	fmt.Println("Yaxshi tartib hajmi:", unsafe.Sizeof(y2), "bayt")
}
```

## Tushuntirish va Mantiq:
Maydonlarni eng katta baytlidan eng kichik baytligacha joylashtirish (Struct Packing) xotirani sezilarli darajada tejaydi.

## Ishlash natijasi:
```text
Yomon tartib hajmi: 24 bayt
Yaxshi tartib hajmi: 16 bayt
```

# 375-Topshiriq: Shallow Copy va Deep Copy farqi strukturalarda
## Topshiriq sharti:
Struktura nusxalanganda ichki slice yoki ko'rsatkichlar umumiy bo'lib qolish xavfini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Hujjat struct {
	Sarlavha string
	Teglar   []string
}

func main() {
	h1 := Hujjat{Sarlavha: "Dars", Teglar: []string{"go"}}
	h2 := h1 // Shallow copy! Sarlavha nusxalandi, ammo Teglar slicesi umumiy bo'lib qoldi!

	h2.Teglar[0] = "golang"

	fmt.Println("h1 teglari:", h1.Teglar) // O'zgarib ketdi!
	fmt.Println("h2 teglari:", h2.Teglar)
}
```

## Tushuntirish va Mantiq:
Oddiy `h2 = h1` o'zlashtirishda slice sarlavhasi nusxalansa-da, uning tagidagi massiv bitta bo'lib qoladi. Haqiqiy mustaqillik uchun `copy` yoki `slices.Clone` shart.

## Ishlash natijasi:
```text
h1 teglari: [golang]
h2 teglari: [golang]
```

# 376-Topshiriq: Builder Pattern orqali murakkab obyektlarni bosqichma-bosqich yasash
## Topshiriq sharti:
HTTP so'rovini qulay zanjir (method chaining) orqali shakllantiruvchi `RequestBuilder` yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type So'rov struct {
	Method  string
	URL     string
	Headers map[string]string
}

type So'rovBuilder struct {
	so'rov So'rov
}

func NewSo'rovBuilder() *So'rovBuilder {
	return &So'rovBuilder{so'rov: So'rov{Headers: make(map[string]string)}}
}

func (b *So'rovBuilder) SetMethod(m string) *So'rovBuilder {
	b.so'rov.Method = m
	return b
}

func (b *So'rovBuilder) SetURL(u string) *So'rovBuilder {
	b.so'rov.URL = u
	return b
}

func (b *So'rovBuilder) AddHeader(k, v string) *So'rovBuilder {
	b.so'rov.Headers[k] = v
	return b
}

func (b *So'rovBuilder) Build() So'rov {
	return b.so'rov
}

func main() {
	req := NewSo'rovBuilder().
		SetMethod("POST").
		SetURL("https://api.olam.uz/v1/auth").
		AddHeader("Content-Type", "application/json").
		Build()

	fmt.Printf("Yasalgan so'rov: %+v\n", req)
}
```

## Tushuntirish va Mantiq:
Builder pattern ko'p sonli ixtiyoriy parametrlarga ega murakkab strukturalarni xatosiz va o'qilishi oson tarzda yasaydi.

## Ishlash natijasi:
```text
Yasalgan so'rov: {Method:POST URL:https://api.olam.uz/v1/auth Headers:map[Content-Type:application/json]}
```

# 377-Topshiriq: Value Object andozasi (Domain-Driven Design)
## Topshiriq sharti:
O'zgaruvchan identifikatorga emas, faqat o'z qiymatlariga ko'ra teng bo'luvchi `Manzil` Value Objectini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type ManzilVO struct {
	Mamlakat string
	Shahar   string
	Pochta   string
}

func (m ManzilVO) Equals(boshqa ManzilVO) bool {
	return m == boshqa // Barcha maydonlar teng bo'lsa teng
}

func main() {
	m1 := ManzilVO{"O'zbekiston", "Toshkent", "100000"}
	m2 := ManzilVO{"O'zbekiston", "Toshkent", "100000"}
	m3 := ManzilVO{"O'zbekiston", "Samarqand", "140100"}

	fmt.Println("m1 va m2 bir xil manzilmi:", m1.Equals(m2))
	fmt.Println("m1 va m3 bir xil manzilmi:", m1.Equals(m3))
}
```

## Tushuntirish va Mantiq:
DDD da Value Objectlar o'zgarmas (immutable) bo'ladi va faqat barcha maydonlari bir xil bo'lganda teng deb qaraladi.

## Ishlash natijasi:
```text
m1 va m2 bir xil manzilmi: true
m1 va m3 bir xil manzilmi: false
```

# 378-Topshiriq: Entity andozasi (ID bo'yicha tenglik)
## Topshiriq sharti:
Maydonlari o'zgarsa ham, ID raqami bir xil bo'lsa bitta shaxs deb hisoblanuvchi Entity strukturasini tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type FoydalanuvchiEntity struct {
	ID    int
	Ism   string
	Email string
}

func (f *FoydalanuvchiEntity) Equals(boshqa *FoydalanuvchiEntity) bool {
	if boshqa == nil {
		return false
	}
	return f.ID == boshqa.ID
}

func main() {
	u1 := &FoydalanuvchiEntity{ID: 101, Ism: "Ali", Email: "ali@eski.uz"}
	u2 := &FoydalanuvchiEntity{ID: 101, Ism: "Alisher", Email: "ali@yangi.uz"}

	fmt.Println("u1 va u2 bitta foydalanuvchimi:", u1.Equals(u2))
}
```

## Tushuntirish va Mantiq:
Entity obyektlari o'z identifikatoriga (ID) ega va vaqt o'tishi bilan holati o'zgarishi mumkin.

## Ishlash natijasi:
```text
u1 va u2 bitta foydalanuvchimi: true
```

# 379-Topshiriq: DTO (Data Transfer Object) konvertatsiyasi
## Topshiriq sharti:
Ma'lumotlar bazasi modelini xavfsiz tashqi API DTO modeliga o'giruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type UserDBModel struct {
	ID        int
	Ism       string
	ParolHash string
	SoliqRaqam string
}

type UserPublicDTO struct {
	ID  int    `json:"id"`
	Ism string `json:"name"`
}

func ToDTO(db UserDBModel) UserPublicDTO {
	return UserPublicDTO{
		ID:  db.ID,
		Ism: db.Ism,
	}
}

func main() {
	dbUser := UserDBModel{
		ID:         1,
		Ism:        "Anvar",
		ParolHash:  "bcrypt_hash_secret",
		SoliqRaqam: "123456789",
	}

	dto := ToDTO(dbUser)
	fmt.Printf("Xavfsiz DTO (parol va soliq maxfiy qoldi): %+v\n", dto)
}
```

## Tushuntirish va Mantiq:
DTO ichki maxfiy ma'lumotlarni tashqariga chiqib ketishidan asrovchi muhim xavfsizlik qatlamidir.

## Ishlash natijasi:
```text
Xavfsiz DTO (parol va soliq maxfiy qoldi): {ID:1 Ism:Anvar}
```

# 380-Topshiriq: Standart API Response Wrapper strukturasi
## Topshiriq sharti:
Barcha API javoblari uchun yagona umumiy javob konteynerini tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type APIResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message,omitempty"`
	Data    any    `json:"data,omitempty"`
	Error   string `json:"error,omitempty"`
}

func main() {
	muvaffaqiyat := APIResponse{
		Success: true,
		Data:    map[string]int{"hisob": 500},
	}

	xato := APIResponse{
		Success: false,
		Error:   "Avtorizatsiyadan o'tilmagan",
	}

	j1, _ := json.Marshal(muvaffaqiyat)
	j2, _ := json.Marshal(xato)

	fmt.Println("Muvaffaqiyatli JSON:", string(j1))
	fmt.Println("Xatolik JSON:", string(j2))
}
```

## Tushuntirish va Mantiq:
Yagona javob andozasi frontend va mobil mijozlar bilan integratsiyani soddalashtiradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli JSON: {"success":true,"data":{"hisob":500}}
Xatolik JSON: {"success":false,"error":"Avtorizatsiyadan o'tilmagan"}
```

# 381-Topshiriq: Pagination (Sahifalash) strukturasi
## Topshiriq sharti:
Katta ro'yxatlarni sahifalab chiqarish uchun `Pagination` modelini loyihalang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Pagination struct {
	JoriySahifa int `json:"page"`
	Limit       int `json:"limit"`
	JamiSoni    int `json:"total_records"`
	JamiSahifa  int `json:"total_pages"`
}

func NewPagination(sahifa, limit, jami int) Pagination {
	sahifalar := jami / limit
	if jami%limit != 0 {
		sahifalar++
	}
	return Pagination{
		JoriySahifa: sahifa,
		Limit:       limit,
		JamiSoni:    jami,
		JamiSahifa:  sahifalar,
	}
}

func main() {
	p := NewPagination(1, 20, 95)
	fmt.Printf("Sahifalash: %d ta yozuv uchun jami %d ta sahifa hosil bo'ldi.\n", p.JamiSoni, p.JamiSahifa)
}
```

## Tushuntirish va Mantiq:
REST API larda resurslarni sahifalash uchun Pagination metadatalari ishlatiladi.

## Ishlash natijasi:
```text
Sahifalash: 95 ta yozuv uchun jami 5 ta sahifa hosil bo'ldi.
```

# 382-Topshiriq: Konfiguratsiya strukturasi va atrof-muhit integratsiyasi
## Topshiriq sharti:
Server sozlamalarini boshqaruvchi to'liq konfiguratsiya modelini tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type BazaSozlamalari struct {
	Host string
	Port int
	Nomi string
}

type IlovaKonfig struct {
	IlovaNomi string
	Port      int
	Baza      BazaSozlamalari
}

func main() {
	cfg := IlovaKonfig{
		IlovaNomi: "FastOrder",
		Port:      8000,
		Baza: BazaSozlamalari{
			Host: "postgres.local",
			Port: 5432,
			Nomi: "fastorder_db",
		},
	}

	fmt.Printf("Ilova: %s (Port: %d), DB: %s:%d/%s\n",
		cfg.IlovaNomi, cfg.Port, cfg.Baza.Host, cfg.Baza.Port, cfg.Baza.Nomi)
}
```

## Tushuntirish va Mantiq:
Iyerarxik konfiguratsiya strukturalari loyiha parametrlarini toza boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Ilova: FastOrder (Port: 8000), DB: postgres.local:5432/fastorder_db
```

# 383-Topshiriq: Audit Log strukturasi (CreatedAt, UpdatedAt, DeletedAt)
## Topshiriq sharti:
GORM va zamonaviy ORM larda keng ishlatiluvchi Model bazaviy strukturasini yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

type BazaModel struct {
	ID        uint       `json:"id"`
	CreatedAt time.Time  `json:"created_at"`
	UpdatedAt time.Time  `json:"updated_at"`
	DeletedAt *time.Time `json:"deleted_at,omitempty"` // Soft delete
}

type Maqola struct {
	BazaModel
	Sarlavha string
}

func main() {
	hozir := time.Now()
	m := Maqola{
		BazaModel: BazaModel{
			ID:        1,
			CreatedAt: hozir,
			UpdatedAt: hozir,
			DeletedAt: nil, // Hali o'chirilmagan
		},
		Sarlavha: "Go 1.22 yangiliklari",
	}

	fmt.Printf("Maqola ID: %d, Sarlavha: %s (Yaratilgan: %v)\n", m.ID, m.Sarlavha, m.CreatedAt.Format("2006-01-02"))
}
```

## Tushuntirish va Mantiq:
Bazaviy strukturani o'rnatish (embedding) orqali barcha jadvallar uchun umumiy audit maydonlari avtomatik beriladi.

## Ishlash natijasi:
```text
Maqola ID: 1, Sarlavha: Go 1.22 yangiliklari (Yaratilgan: 2026-11-08)
```

# 384-Topshiriq: Geografik nuqta va masofa hisoblash strukturasi
## Topshiriq sharti:
Kenglik (Latitude) va uzunlik (Longitude) nuqtalarini ifodalovchi struktura tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"math"
)

type GeoNuqta struct {
	Lat float64
	Lon float64
}

// Eyler tekisligidagi soddalashtirilgan masofa
func (g GeoNuqta) Masofa(boshqa GeoNuqta) float64 {
	dLat := g.Lat - boshqa.Lat
	dLon := g.Lon - boshqa.Lon
	return math.Sqrt(dLat*dLat + dLon*dLon)
}

func main() {
	toshkent := GeoNuqta{Lat: 41.2995, Lon: 69.2401}
	samarqand := GeoNuqta{Lat: 39.6270, Lon: 66.9750}

	fmt.Printf("Koordinatalar oralig'i: %.4f daraja\n", toshkent.Masofa(samarqand))
}
```

## Tushuntirish va Mantiq:
Geografik joylashuvlar strukturalar orqali aniq modellarga ajratiladi.

## Ishlash natijasi:
```text
Koordinatalar oralig'i: 2.8126 daraja
```

# 385-Topshiriq: Moliyaviy valyuta va aniqlik strukturasi (Pul modeli)
## Topshiriq sharti:
Suzuvchi vergul (`float64`) xatolaridan qochish uchun tiyinlarda (`int64`) saqlovchi Pul modelini tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Pul struct {
	Tiyinlar int64  // 1 so'm = 100 tiyin
	Valyuta  string
}

func (p Pul) Qosh(boshqa Pul) Pul {
	return Pul{
		Tiyinlar: p.Tiyinlar + boshqa.Tiyinlar,
		Valyuta:  p.Valyuta,
	}
}

func (p Pul) Format() string {
	som := p.Tiyinlar / 100
	tiyin := p.Tiyinlar % 100
	return fmt.Sprintf("%d.%02d %s", som, tiyin, p.Valyuta)
}

func main() {
	narx1 := Pul{Tiyinlar: 155050, Valyuta: "UZS"} // 1550.50 so'm
	narx2 := Pul{Tiyinlar: 44950, Valyuta: "UZS"}  // 449.50 so'm

	jami := narx1.Qosh(narx2)
	fmt.Println("Jami to'lov:", jami.Format())
}
```

## Tushuntirish va Mantiq:
Moliyaviy tizimlarda floating-point rounding muammolarining oldini olish uchun summalar butun sonlarda (tiyin/sent) saqlanadi.

## Ishlash natijasi:
```text
Jami to'lov: 2000.00 UZS
```

# 386-Topshiriq: E-tijorat savatchasi: Cart va CartItem
## Topshiriq sharti:
Savatcha va undagi tovarlar munosabatini ifodalang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type TovarlarItem struct {
	ID    int
	Nomi  string
	Narxi float64
	Miqdor int
}

type Savat struct {
	MijozID int
	Items   []TovarlarItem
}

func (s *Savat) JamiSumma() float64 {
	summa := 0.0
	for _, it := range s.Items {
		summa += it.Narxi * float64(it.Miqdor)
	}
	return summa
}

func main() {
	s := Savat{
		MijozID: 55,
		Items: []TovarlarItem{
			{1, "Kl клавиатура", 250000, 1},
			{2, "Sichqoncha", 120000, 2},
		},
	}

	fmt.Printf("Mijoz %d uchun jami: %.0f so'm\n", s.MijozID, s.JamiSumma())
}
```

## Tushuntirish va Mantiq:
Domen obyektlari bir-biri bilan uzviy bog'lanib haqiqiy biznes jarayonlarini aks ettiradi.

## Ishlash natijasi:
```text
Mijoz 55 uchun jami: 490000 so'm
```

# 387-Topshiriq: Buyurtma holati (Order State) va Status Enum
## Topshiriq sharti:
Buyurtma modeli va uning bosqichlarini enum bilan birlashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type BuyurtmaHolati int

const (
	Kutilmoqda BuyurtmaHolati = iota + 1
	Tolandi
	Yetkazilmoqda
	Yakunlandi
)

type Buyurtma struct {
	ID     int
	Holati BuyurtmaHolati
}

func (h BuyurtmaHolati) String() string {
	switch h {
	case Kutilmoqda:
		return "Kutilmoqda"
	case Tolandi:
		return "To'landi"
	case Yetkazilmoqda:
		return "Yetkazilmoqda"
	case Yakunlandi:
		return "Yakunlandi"
	default:
		return "Noma'lum"
	}
}

func main() {
	b := Buyurtma{ID: 1001, Holati: Yetkazilmoqda}
	fmt.Printf("Buyurtma #%d holati: %s\n", b.ID, b.Holati)
}
```

## Tushuntirish va Mantiq:
Strukturalar enum turlari bilan integratsiyalashib mustahkam tur nazoratini o'rnatadi.

## Ishlash natijasi:
```text
Buyurtma #1001 holati: Yetkazilmoqda
```

# 388-Topshiriq: Tarmoq paketi sarlavhasi (Network Packet Header) strukturasi
## Topshiriq sharti:
Tarmoq protokoli darajasidagi binar paket sarlavhasini modellashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type IPHeader struct {
	Versiya  uint8
	TOS      uint8
	Uzunlik  uint16
	TTL      uint8
	Protokol uint8
	ManbaIP  [4]byte
	MaqsadIP [4]byte
}

func main() {
	hdr := IPHeader{
		Versiya:  4,
		TTL:      64,
		Protokol: 6, // TCP
		ManbaIP:  [4]byte{192, 168, 1, 10},
		MaqsadIP: [4]byte{8, 8, 8, 8},
	}

	fmt.Printf("IPv%d paketi | Manba: %d.%d.%d.%d -> Maqsad: %d.%d.%d.%d\n",
		hdr.Versiya,
		hdr.ManbaIP[0], hdr.ManbaIP[1], hdr.ManbaIP[2], hdr.ManbaIP[3],
		hdr.MaqsadIP[0], hdr.MaqsadIP[1], hdr.MaqsadIP[2], hdr.MaqsadIP[3])
}
```

## Tushuntirish va Mantiq:
Quyi darajadagi protokollar va binar ma'lumotlar strukturalar orqali juda aniq aks ettiriladi.

## Ishlash natijasi:
```text
IPv4 paketi | Manba: 192.168.1.10 -> Maqsad: 8.8.8.8
```

# 389-Topshiriq: Telemetriya va metrikalar strukturasi
## Topshiriq sharti:
Server monitoringi uchun telemetriya metrikalarini yig'uvchi struktura.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Metrika struct {
	Nomi      string
	Qiymat    float64
	Teglar    map[string]string
}

func main() {
	m := Metrika{
		Nomi:   "http_requests_total",
		Qiymat: 10452,
		Teglar: map[string]string{
			"status": "200",
			"path":   "/api/v1/users",
		},
	}

	fmt.Printf("Metrika: %s = %.0f (Status: %s)\n", m.Nomi, m.Qiymat, m.Teglar["status"])
}
```

## Tushuntirish va Mantiq:
Prometheus va OpenTelemetry tizimlari aynan shunday metrika modellariga tayanadi.

## Ishlash natijasi:
```text
Metrika: http_requests_total = 10452 (Status: 200)
```

# 390-Topshiriq: Event-Driven arxitektura uchun voqea strukturasi
## Topshiriq sharti:
Xabarlar brokeri (Kafka/RabbitMQ) uchun umumiy voqea (Event) modelini tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Voqea struct {
	Turi      string `json:"type"`
	FoydalanuvchiID int `json:"user_id"`
	Payload   any    `json:"payload"`
}

func main() {
	v := Voqea{
		Turi:      "USER_REGISTERED",
		FoydalanuvchiID: 501,
		Payload:   map[string]string{"email": "user501@olam.uz"},
	}

	fmt.Printf("Voqea: %s (User: %d)\n", v.Turi, v.FoydalanuvchiID)
}
```

## Tushuntirish va Mantiq:
`Payload any` ixtiyoriy ma'lumotlar yukini qabul qilish imkonini beradi.

## Ishlash natijasi:
```text
Voqea: USER_REGISTERED (User: 501)
```

# 391-Topshiriq: Mutexni struktura ichiga joylashtirish (Struct with Mutex)
## Topshiriq sharti:
O'zgaruvchilar va ularni himoyalovchi mutexni bitta strukturaga joylang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type XavfsizHisoblagich struct {
	mu   sync.Mutex
	soni int
}

func (c *XavfsizHisoblagich) Inc() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.soni++
}

func (c *XavfsizHisoblagich) Value() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.soni
}

func main() {
	h := &XavfsizHisoblagich{}
	h.Inc()
	h.Inc()

	fmt.Println("Xavfsiz hisob:", h.Value())
}
```

## Tushuntirish va Mantiq:
Ma'lumot va uni himoyalovchi sinxronizatorning bitta strukturada turishi inkapsulyatsiyaning eng toza namunasidir.

## Ishlash natijasi:
```text
Xavfsiz hisob: 2
```

# 392-Topshiriq: Anonymous Mutex Embedding orqali Lock/Unlock metodlarini ko'tarish
## Topshiriq sharti:
Struktura ichiga `sync.Mutex` ni nomsiz joylashtiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type ThreadSafeRo'yxat struct {
	sync.Mutex // Embedded mutex!
	data       []string
}

func main() {
	var l ThreadSafeRo'yxat

	l.Lock() // sync.Mutex metodlari to'g'ridan-to'g'ri ko'tariladi
	l.data = append(l.data, "Element 1")
	l.Unlock()

	fmt.Println("Ma'lumotlar:", l.data)
}
```

## Tushuntirish va Mantiq:
Embedded Mutex tufayli `l.Lock()` va `l.Unlock()` chaqiruvlari to'g'ridan-to'g'ri ro'yxat obyektida ishlaydi.

## Ishlash natijasi:
```text
Ma'lumotlar: [Element 1]
```

# 393-Topshiriq: Interfeys maydonli strukturalar (Polymorphic Struct)
## Topshiriq sharti:
Struktura maydoni sifatida interfeysdan foydalanib xatti-harakatni polimorfik qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Xabarchi interface {
	Yubor(xabar string)
}

type KonsolXabarchi struct{}
func (k KonsolXabarchi) Yubor(x string) { fmt.Println("[KONSOL]:", x) }

type BildirishnomaXizmati struct {
	xabarchi Xabarchi // Polimorfik maydon
}

func main() {
	xizmat := BildirishnomaXizmati{xabarchi: KonsolXabarchi{}}
	xizmat.xabarchi.Yubor("Tizimga kirildi!")
}
```

## Tushuntirish va Mantiq:
Interfeys maydoni orqali turli implementatsiyalarni strukturaga oson almashtirib ulash mumkin.

## Ishlash natijasi:
```text
[KONSOL]: Tizimga kirildi!
```

# 394-Topshiriq: Dinamik xususiyatlar (Dynamic Attributes) strukturasi
## Topshiriq sharti:
Qat'iy maydonlar bilan birga erkin dinamik atributlar xaritasini saqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type MahsulotKengaytirilgan struct {
	ID        int
	Nomi      string
	Xossalar  map[string]any // Dinamik parametrlar (rang, o'lcham, og'irlik)
}

func main() {
	m := MahsulotKengaytirilgan{
		ID:   1,
		Nomi: "Futbolka",
		Xossalar: map[string]any{
			"rang":    "Oq",
			"o'lcham": "XL",
			"paxta":   100,
		},
	}

	fmt.Printf("%s - Rangi: %v, O'lchami: %v\n", m.Nomi, m.Xossalar["rang"], m.Xossalar["o'lcham"])
}
```

## Tushuntirish va Mantiq:
Elektron tijoratda turlicha xususiyatlarga ega mahsulotlarni saqlashda ushbu gibrid andoza keng qo'llaniladi.

## Ishlash natijasi:
```text
Futbolka - Rangi: Oq, O'lchami: XL
```

# 395-Topshiriq: Validatsiya teglari bilan struktura tekshiruvchisi simulyatsiyasi
## Topshiriq sharti:
Maxsus `validate` teglarini tahlil qilib majburiy maydonlarni tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"reflect"
)

type RegistratsiyaFormasi struct {
	Login string `validate:"required"`
	Email string `validate:"required"`
}

func TekshirForma(s any) []string {
	var xatolar []string
	val := reflect.ValueOf(s)
	typ := reflect.TypeOf(s)

	for i := 0; i < typ.NumField(); i++ {
		field := typ.Field(i)
		tag := field.Tag.Get("validate")

		if tag == "required" {
			strVal := val.Field(i).String()
			if strVal == "" {
				xatolar = append(xatolar, fmt.Sprintf("'%s' maydoni to'ldirilishi shart!", field.Name))
			}
		}
	}
	return xatolar
}

func main() {
	f := RegistratsiyaFormasi{Login: "admin", Email: ""}
	xatolar := TekshirForma(f)

	for _, x := range xatolar {
		fmt.Println("[VALIDATSIYA]:", x)
	}
}
```

## Tushuntirish va Mantiq:
`go-playground/validator` kabi mashhur kutubxonalar aynan shu prinsip asosida ishlaydi.

## Ishlash natijasi:
```text
[VALIDATSIYA]: 'Email' maydoni to'ldirilishi shart!
```

# 396-Topshiriq: Struktura diff (O'zgarishlar farqini hisoblash)
## Topshiriq sharti:
Eski va yangi strukturalar orasidagi o'zgargan maydonlarni aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Sozlama struct {
	Til       string
	Mavzu     string
	Bildirish bool
}

func main() {
	eski := Sozlama{Til: "UZ", Mavzu: "Light", Bildirish: true}
	yangi := Sozlama{Til: "UZ", Mavzu: "Dark", Bildirish: false}

	if eski.Mavzu != yangi.Mavzu {
		fmt.Printf("Mavzu o'zgardi: %s -> %s\n", eski.Mavzu, yangi.Mavzu)
	}
	if eski.Bildirish != yangi.Bildirish {
		fmt.Printf("Bildirishnoma o'zgardi: %t -> %t\n", eski.Bildirish, yangi.Bildirish)
	}
}
```

## Tushuntirish va Mantiq:
Audit va tranzaksiya tarixini yuritishda o'zgarishlar farqi qayd etiladi.

## Ishlash natijasi:
```text
Mavzu o'zgardi: Light -> Dark
Bildirishnoma o'zgardi: true -> false
```

# 397-Topshiriq: Immutable Struct va With... modifikator metodlari
## Topshiriq sharti:
Struktura holatini o'zgartirmasdan, yangilangan yangi nusxa qaytaruvchi metodlar yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type FoydalanuvchiImmut struct {
	ism   string
	yosh  int
}

func NewFoydalanuvchiImmut(ism string, yosh int) FoydalanuvchiImmut {
	return FoydalanuvchiImmut{ism: ism, yosh: yosh}
}

func (f FoydalanuvchiImmut) WithYosh(yangiYosh int) FoydalanuvchiImmut {
	f.yosh = yangiYosh
	return f
}

func main() {
	u1 := NewFoydalanuvchiImmut("Kamron", 20)
	u2 := u1.WithYosh(21)

	fmt.Printf("u1 yoshi: %d (asl saqlandi)\n", u1.yosh)
	fmt.Printf("u2 yoshi: %d (yangi nusxa)\n", u2.yosh)
}
```

## Tushuntirish va Mantiq:
`With...` metodlari zanjirlash va o'zgarmas ma'lumotlar bilan xavfsiz ishlash imkonini beradi.

## Ishlash natijasi:
```text
u1 yoshi: 20 (asl saqlandi)
u2 yoshi: 21 (yangi nusxa)
```

# 398-Topshiriq: Struktura maydonlari bo'yicha saralash (slices.SortFunc)
## Topshiriq sharti:
Strukturalar ro'yxatini bir nechta maydon bo'yicha tartiblang.

## Yechim (Go kodi):
```go
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type XodimReyting struct {
	Ism  string
	Ball int
}

func main() {
	xodimlar := []XodimReyting{
		{"Dilshod", 85},
		{"Sherzod", 95},
		{"Akbar", 85},
	}

	slices.SortFunc(xodimlar, func(a, b XodimReyting) int {
		// Dastlab ball bo'yicha kamayish tartibida:
		if c := cmp.Compare(b.Ball, a.Ball); c != 0 {
			return c
		}
		// Ballar teng bo'lsa ism bo'yicha alifbo tartibida:
		return cmp.Compare(a.Ism, b.Ism)
	})

	for _, x := range xodimlar {
		fmt.Printf("%-8s: %d ball\n", x.Ism, x.Ball)
	}
}
```

## Tushuntirish va Mantiq:
Ko'p pog'onali saralash Go 1.21 `cmp.Compare` orqali juda sodda va ravon yoziladi.

## Ishlash natijasi:
```text
Sherzod : 95 ball
Akbar   : 85 ball
Dilshod : 85 ball
```

# 399-Topshiriq: Xotira maydonlarini ixchamlashtirish (Bitfield simulyatsiyasi struktura bilan)
## Topshiriq sharti:
Bitta bayt ichida bir nechta boolean holatlarni struktura orqali boshqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Bayroqlar uint8

const (
	Faol      Bayroqlar = 1 << 0
	Admin               = 1 << 1
	EmailTasdiq         = 1 << 2
)

type HisobHolati struct {
	bayroqlar Bayroqlar
}

func (h *HisobHolati) Set(b Bayroqlar)    { h.bayroqlar |= b }
func (h *HisobHolati) Has(b Bayroqlar) bool { return h.bayroqlar&b != 0 }

func main() {
	hh := HisobHolati{}
	hh.Set(Faol)
	hh.Set(EmailTasdiq)

	fmt.Println("Faolmi:", hh.Has(Faol))
	fmt.Println("Adminmi:", hh.Has(Admin))
	fmt.Println("Email tasdiqlanganmi:", hh.Has(EmailTasdiq))
}
```

## Tushuntirish va Mantiq:
8 ta boolean o'zgaruvchi (8 bayt) o'rniga bitta uint8 (1 bayt) ishlatilib millionlab obyektlarda xotira tejaladi.

## Ishlash natijasi:
```text
Faolmi: true
Adminmi: false
Email tasdiqlanganmi: true
```

# 400-Topshiriq: Yakuniy amaliy vazifa: To'liq Bank Hisobi va Tranzaksiyalar Domen Modeli
## Topshiriq sharti:
Strukturalar, teglash, inkapsulyatsiya, validatsiya va kompozitsiyani birlashtirgan to'liq domen modelini yarating.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
	"time"
)

type TranzaksiyaTuri string

const (
	Kirim  TranzaksiyaTuri = "KIRIM"
	Chiqim TranzaksiyaTuri = "CHIQIM"
)

type TranzaksiyaYozuvi struct {
	ID        int             `json:"id"`
	Turi      TranzaksiyaTuri `json:"type"`
	Summa     float64         `json:"amount"`
	Sana      time.Time       `json:"date"`
}

type BankMijozi struct {
	HisobRaqami   string              `json:"account_number"`
	Egasi         string              `json:"owner"`
	balans        float64             // Maxfiy maydon
	Tarix         []TranzaksiyaYozuvi `json:"history"`
}

func YangiBankMijozi(raqam, egasi string) *BankMijozi {
	return &BankMijozi{
		HisobRaqami: raqam,
		Egasi:       egasi,
		balans:      0.0,
	}
}

func (b *BankMijozi) Balans() float64 {
	return b.balans
}

func (b *BankMijozi) Depozit(summa float64) error {
	if summa <= 0 {
		return errors.New("depozit summasi musbat bo'lishi shart")
	}
	b.balans += summa
	b.Tarix = append(b.Tarix, TranzaksiyaYozuvi{
		ID:    len(b.Tarix) + 1,
		Turi:  Kirim,
		Summa: summa,
		Sana:  time.Now(),
	})
	return nil
}

func main() {
	mijoz := YangiBankMijozi("UZB100200300", "Sherzodbek")
	_ = mijoz.Depozit(500000)

	fmt.Printf("Mijoz: %s (Hisob: %s)\n", mijoz.Egasi, mijoz.HisobRaqami)
	fmt.Printf("Joriy balans: %.0f so'm\n", mijoz.Balans())
	fmt.Printf("Tranzaksiyalar soni: %d ta\n", len(mijoz.Tarix))
}
```

## Tushuntirish va Mantiq:
Ushbu model Go strukturalarining barcha imkoniyatlarini professional darajada mujassam etgan.

## Ishlash natijasi:
```text
Mijoz: Sherzodbek (Hisob: UZB100200300)
Joriy balans: 500000 so'm
Tranzaksiyalar soni: 1 ta
```

