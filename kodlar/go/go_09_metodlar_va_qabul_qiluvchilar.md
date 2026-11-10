# 9-Mavzu: Metodlar va Qabul Qiluvchilar (Methods & Receivers) (401-450)

Go tilida metodlar qabul qiluvchiga (Receiver) ega bo'lgan maxsus funksiyalardir. Qiymat qabul qiluvchi (Value Receiver) va Ko'rsatkich qabul qiluvchi (Pointer Receiver) farqlari, struktura bo'lmagan tiplarga metod qo'shish, Nil Receiver xavfsizligi, metodlarning ko'tarilishi (Method Promotion), Method Values va Method Expressions, `fmt.Stringer` interfeysi bo'yicha 50 ta amaliy topshiriq.

# 401-Topshiriq: Metodlar asoslari: Funksiya va Metod o'rtasidagi farq
## Topshiriq sharti:
To'g'ri to'rtburchak yuzasini hisoblashni oddiy funksiya va metod ko'rinishida yozib farqini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Tortburchak struct {
	Eni, Boyi float64
}

// 1. Oddiy funksiya
func yuzaFunksiya(t Tortburchak) float64 {
	return t.Eni * t.Boyi
}

// 2. Metod: Tortburchak turiga biriktirilgan
func (t Tortburchak) Yuza() float64 {
	return t.Eni * t.Boyi
}

func main() {
	tb := Tortburchak{Eni: 10, Boyi: 5}

	fmt.Println("Funksiya orqali:", yuzaFunksiya(tb))
	fmt.Println("Metod orqali:", tb.Yuza())
}
```

## Tushuntirish va Mantiq:
Metod `func (qabulQiluvchi Tur) MetodNomi()` sintaksisi bilan e'lon qilinadi va `obyekt.Metod()` ko'rinishida chaqiriladi.

## Ishlash natijasi:
```text
Funksiya orqali: 50
Metod orqali: 50
```

# 402-Topshiriq: Qiymat qabul qiluvchi metod (Value Receiver)
## Topshiriq sharti:
Obyektning asl holatini o'zgartirmaydigan faqat o'quvchi metod yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Foydalanuvchi struct {
	Ism  string
	Yosh int
}

// Value Receiver: nusxa bilan ishlaydi
func (f Foydalanuvchi) Tanishtir() string {
	return fmt.Sprintf("Mening ismim %s, yoshim %d da.", f.Ism, f.Yosh)
}

func main() {
	u := Foydalanuvchi{Ism: "Jasurbek", Yosh: 24}
	fmt.Println(u.Tanishtir())
}
```

## Tushuntirish va Mantiq:
Value receiver metod chaqirilganda strukturaning to'liq nusxasini oladi, shu sababli asl obyekt mutatsiyadan himoyalangan bo'ladi.

## Ishlash natijasi:
```text
Mening ismim Jasurbek, yoshim 24 da.
```

# 403-Topshiriq: Ko'rsatkich qabul qiluvchi metod (Pointer Receiver)
## Topshiriq sharti:
Obyektning ichki maydonini o'zgartiruvchi ko'rsatkichli metod yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Hisoblagich struct {
	qiymat int
}

// Pointer Receiver: asl obyektni o'zgartiradi
func (h *Hisoblagich) Oshir() {
	h.qiymat++
}

func main() {
	h := &Hisoblagich{qiymat: 10}
	fmt.Println("Boshlang'ich:", h.qiymat)

	h.Oshir()
	h.Oshir()

	fmt.Println("Oshirilgandan keyin:", h.qiymat)
}
```

## Tushuntirish va Mantiq:
`(h *Hisoblagich)` pointer receiver ko'rsatkich orqali xotiradagi haqiqiy obyektni mutatsiya qiladi.

## Ishlash natijasi:
```text
Boshlang'ich: 10
Oshirilgandan keyin: 12
```

# 404-Topshiriq: Qachon Value, qachon Pointer Receiver ishlatish qat'iy qoidalari
## Topshiriq sharti:
Mutatsiya va xotira hajmiga qarab to'g'ri tanlovni kod bilan ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Nuqta struct {
	X, Y int
}

// Qoida 1: Kichik va o'zgarmas structlar uchun Value Receiver
func (n Nuqta) MasofaKvadrat() int {
	return n.X*n.X + n.Y*n.Y
}

// Qoida 2: Mutatsiya qilinadigan yoki katta structlar uchun Pointer Receiver
func (n *Nuqta) Siljit(dx, dy int) {
	n.X += dx
	n.Y += dy
}

func main() {
	p := Nuqta{X: 3, Y: 4}
	fmt.Println("Masofa kvadrati (Value):", p.MasofaKvadrat())

	p.Siljit(2, 1)
	fmt.Printf("Siljigandan keyin (Pointer): %+v\n", p)
}
```

## Tushuntirish va Mantiq:
Qoida: agar turdagi birorta metod pointer receiver bo'lsa, konsistentlik uchun barcha metodlarni pointer receiver qilish tavsiya etiladi.

## Ishlash natijasi:
```text
Masofa kvadrati (Value): 25
Siljigandan keyin (Pointer): {X:5 Y:5}
```

# 405-Topshiriq: Metod chaqiriqlarida avtomatik manzil olish va dereferensiya
## Topshiriq sharti:
Qiymat ustida pointer metod, yoki ko'rsatkich ustida value metod chaqirishda Go qulayligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Doira struct {
	Radius float64
}

func (d Doira) Yuza() float64 {
	return 3.14159 * d.Radius * d.Radius
}

func (d *Doira) Kengaytir(faktor float64) {
	d.Radius *= faktor
}

func main() {
	// 1. Oddiy qiymat:
	d1 := Doira{Radius: 5.0}
	d1.Kengaytir(2.0) // Go avtomatik (&d1).Kengaytir() qiladi!
	fmt.Println("d1 yangi radiusi:", d1.Radius)

	// 2. Ko'rsatkich:
	d2 := &Doira{Radius: 10.0}
	fmt.Println("d2 yuzasi:", d2.Yuza()) // Go avtomatik (*d2).Yuza() qiladi!
}
```

## Tushuntirish va Mantiq:
Go dasturchini `(&d).Metod()` yoki `(*p).Metod()` deb yozish mashaqqatidan xalos qiladi; kompilyator kerakli konvertatsiyani avtomatik bajaradi.

## Ishlash natijasi:
```text
d1 yangi radiusi: 10
d2 yuzasi: 314.159
```

# 406-Topshiriq: Struktura bo'lmagan (Non-Struct) turlarga metod biriktirish
## Topshiriq sharti:
`type Sekund int` va `type Harorat float64` turlariga metodlar yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Soniya int

func (s Soniya) Daqiqaga() float64 {
	return float64(s) / 60.0
}

type Selsiy float64

func (c Selsiy) ToFahrenheit() float64 {
	return float64(c)*9.0/5.0 + 32.0
}

func main() {
	var vaqt Soniya = 150
	fmt.Printf("%d soniya = %.2f daqiqa\n", vaqt, vaqt.Daqiqaga())

	var temp Selsiy = 100.0
	fmt.Printf("%.1f°C = %.1f°F\n", temp, temp.ToFahrenheit())
}
```

## Tushuntirish va Mantiq:
Go da faqat structlarga emas, balki bir xil paketda e'lon qilingan har qanday maxsus tiplarga metod qo'shish mumkin.

## Ishlash natijasi:
```text
150 soniya = 2.50 daqiqa
100.0°C = 212.0°F
```

# 407-Topshiriq: Method Sets (Metod To'plamlari) qoidasi
## Topshiriq sharti:
`T` va `*T` turlarining metod to'plamlari orasidagi nozik farqni tushuntiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Element struct {
	Nomi string
}

func (e Element) Oqi() {
	fmt.Println("O'qildi:", e.Nomi)
}

func (e *Element) Yoz(nom string) {
	e.Nomi = nom
}

func main() {
	// *Element metod to'plami: Oqi() va Yoz()
	// Element metod to'plami: faqat Oqi()!
	var elem Element = Element{Nomi: "Fayl 1"}
	elem.Oqi()

	pElem := &elem
	pElem.Yoz("Fayl 2")
	elem.Oqi()
}
```

## Tushuntirish va Mantiq:
`*T` turi ham qiymat, ham ko'rsatkich metodlarini o'z ichiga oladi. `T` qiymat turi esa faqat value receiver metodlarga ega bo'ladi.

## Ishlash natijasi:
```text
O'qildi: Fayl 1
O'qildi: Fayl 2
```

# 408-Topshiriq: Nil Receiver ustida metod chaqirish va xavfsizlik
## Topshiriq sharti:
Ko'rsatkich `nil` bo'lgan holatda ham xatoliksiz ishlovchi metod yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Tugun struct {
	Qiymat int
}

func (t *Tugun) XavfsizQiymat() int {
	if t == nil {
		return 0 // Nil holati uchun xavfsiz qiymat
	}
	return t.Qiymat
}

func main() {
	var t *Tugun = nil
	fmt.Println("Nil tugun qiymati:", t.XavfsizQiymat())

	t = &Tugun{Qiymat: 42}
	fmt.Println("Haqiqiy tugun qiymati:", t.XavfsizQiymat())
}
```

## Tushuntirish va Mantiq:
Boshqa tillarda `null.method()` darhol NullPointerException bersa, Go da metod `nil` receiver bilan xavfsiz chaqirilishi va o'zini himoyalashi mumkin.

## Ishlash natijasi:
```text
Nil tugun qiymati: 0
Haqiqiy tugun qiymati: 42
```

# 409-Topshiriq: O'rnatilgan strukturalarda metodlarning ko'tarilishi (Method Promotion)
## Topshiriq sharti:
Ichki struktura metodi tashqi obyektga to'g'ridan-to'g'ri ko'tarilishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Dvigatel struct {
	OtKuchi int
}

func (d Dvigatel) IshgaTush() {
	fmt.Printf("Dvigatel ishga tushdi (%d ot kuchi)\n", d.OtKuchi)
}

type Avtomobil struct {
	Dvigatel // Embedded
	Model    string
}

func main() {
	avto := Avtomobil{
		Dvigatel: Dvigatel{OtKuchi: 250},
		Model:    "Malibu",
	}

	// Metod ko'tarilishi tufayli:
	avto.IshgaTush()
}
```

## Tushuntirish va Mantiq:
O'rnatilgan turning metodlari tashqi obyekt metodlari sifatida to'g'ridan-to'g'ri chaqirilishi kompozitsiyaning eng kuchli qulayligidir.

## Ishlash natijasi:
```text
Dvigatel ishga tushdi (250 ot kuchi)
```

# 410-Topshiriq: Metodlarni qayta aniqlash (Method Overriding / Shadowing)
## Topshiriq sharti:
Tashqi struktura ichki struktura metodini xuddi shu nom bilan qayta aniqlashini namoyish qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

type AsosiyXizmat struct{}

func (a AsosiyXizmat) Salom() {
	fmt.Println("Asosiy xizmat salomi")
}

type KengaytirilganXizmat struct {
	AsosiyXizmat
}

// Metodni qayta aniqlaymiz:
func (k KengaytirilganXizmat) Salom() {
	fmt.Println("Kengaytirilgan xizmat salomi (Overridden)")
}

func main() {
	k := KengaytirilganXizmat{}

	k.Salom()              // Tashqi metod ishlaydi
	k.AsosiyXizmat.Salom() // Asl ichki metodga ham murojaat qilish mumkin
}
```

## Tushuntirish va Mantiq:
Tashqi metod ichki metodni yashiradi (shadowing), biroq ichkisiga to'liq yo'l bilan baribir kirish mumkin.

## Ishlash natijasi:
```text
Kengaytirilgan xizmat salomi (Overridden)
Asosiy xizmat salomi
```

# 411-Topshiriq: Metod qiymatlari (Method Values: fn := obj.Method)
## Topshiriq sharti:
Muayyan obyektga bog'langan metodni funksiya o'zgaruvchisiga o'zlashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Hisob struct {
	balans int
}

func (h *Hisob) Qosh(n int) {
	h.balans += n
}

func main() {
	h := &Hisob{balans: 100}

	// Metod qiymati: h obyektiga avtomatik birikadi
	amal := h.Qosh

	amal(50)
	amal(25)

	fmt.Println("Yakuniy balans:", h.balans)
}
```

## Tushuntirish va Mantiq:
Method Value obyekt bilan metodni birlashtirib, bitta oddiy funksiya kabi uzatish imkonini beradi.

## Ishlash natijasi:
```text
Yakuniy balans: 175
```

# 412-Topshiriq: Metod ifodalari (Method Expressions: fn := Type.Method)
## Topshiriq sharti:
Obyektsiz, turning o'zidan metodni qabul qiluvchi birinchi parametr bo'lgan funksiya sifatida ajrating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Kalkulyator struct{}

func (k Kalkulyator) Qosh(a, b int) int {
	return a + b
}

func main() {
	// Method Expression:
	f := Kalkulyator.Qosh

	k := Kalkulyator{}
	// Birinchi argument sifatida receiver obyekti uzatiladi:
	natija := f(k, 10, 20)

	fmt.Println("10 + 20 =", natija)
}
```

## Tushuntirish va Mantiq:
`Type.Method` ifodasi oddiy funksiya qaytaradi, unda birinchi argument qabul qiluvchining o'zi bo'ladi.

## Ishlash natijasi:
```text
10 + 20 = 30
```

# 413-Topshiriq: Metod zanjirlanishi (Method Chaining / Fluent Interface)
## Topshiriq sharti:
`return this` orqali metodlarni bir qatorda zanjir kabi ketma-ket chaqirishni yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type MatnBuilder struct {
	matn string
}

func (b *MatnBuilder) Qosh(s string) *MatnBuilder {
	b.matn += s
	return b // Zanjir uchun o'zini qaytaradi
}

func (b *MatnBuilder) YangiQator() *MatnBuilder {
	b.matn += "\n"
	return b
}

func (b *MatnBuilder) Natija() string {
	return b.matn
}

func main() {
	mb := &MatnBuilder{}
	natija := mb.Qosh("Salom,").Qosh(" Go ").Qosh("Dasturchi!").Natija()

	fmt.Println(natija)
}
```

## Tushuntirish va Mantiq:
Fluent API andozasi kodni o'qish va konfiguratsiya qilishni juda osonlashtiradi.

## Ishlash natijasi:
```text
Salom, Go Dasturchi!
```

# 414-Topshiriq: fmt.Stringer interfeysini amalga oshiruvchi String() metodi
## Topshiriq sharti:
Obyekt `fmt.Println` ga uzatilganda chiroyli formatda chiqishi uchun `String()` metodini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Valyuta struct {
	Kod    string
	Qiymat float64
}

// fmt.Stringer interfeysini qanoatlantiradi
func (v Valyuta) String() string {
	return fmt.Sprintf("%.2f %s", v.Qiymat, v.Kod)
}

func main() {
	v := Valyuta{Kod: "USD", Qiymat: 1250.75}

	// fmt paketi avtomatik String() metodini chaqiradi:
	fmt.Println("Joriy summa:", v)
}
```

## Tushuntirish va Mantiq:
Go standart kutubxonasidagi `fmt.Stringer` interfeysi bitta `String() string` metodidan iborat bo'lib, uning yordamida obyekt matnli ko'rinishga ega bo'ladi.

## Ishlash natijasi:
```text
Joriy summa: 1250.75 USD
```

# 415-Topshiriq: Getter va Setter konvensiyasi metodlar orqali
## Topshiriq sharti:
Yopiq maydonni nazoratli o'zgartirish va o'qish metodlari.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Foydalanuvchi struct {
	yosh int
}

func (f *Foydalanuvchi) Yosh() int {
	return f.yosh // Getter
}

func (f *Foydalanuvchi) SetYosh(y int) error {
	if y < 0 || y > 150 {
		return fmt.Errorf("noto'g'ri yosh: %d", y)
	}
	f.yosh = y
	return nil
}

func main() {
	u := &Foydalanuvchi{}
	_ = u.SetYosh(25)

	fmt.Println("Foydalanuvchi yoshi:", u.Yosh())
}
```

## Tushuntirish va Mantiq:
Go tilida getter nomiga `Get` qo'shilmaydi (`Yosh()`), setter esa `SetYosh(...)` deb nomlanadi.

## Ishlash natijasi:
```text
Foydalanuvchi yoshi: 25
```

# 416-Topshiriq: Holatni tekshiruvchi validator metodlari (IsValid)
## Topshiriq sharti:
Struktura to'g'ri to'ldirilganini tekshiruvchi metod yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type EmailSo'rovi struct {
	Kimga   string
	Mavzu   string
	Xabar   string
}

func (e EmailSo'rovi) IsValid() bool {
	return e.Kimga != "" && e.Mavzu != "" && e.Xabar != ""
}

func main() {
	s1 := EmailSo'rovi{Kimga: "admin@uz", Mavzu: "Salom", Xabar: "Test"}
	s2 := EmailSo'rovi{Kimga: "", Mavzu: "Xato", Xabar: ""}

	fmt.Println("s1 yuborishga yaroqlimi:", s1.IsValid())
	fmt.Println("s2 yuborishga yaroqlimi:", s2.IsValid())
}
```

## Tushuntirish va Mantiq:
Validator metodlari biznes mantig'ini domen modeli ichida saqlashga xizmat qiladi.

## Ishlash natijasi:
```text
s1 yuborishga yaroqlimi: true
s2 yuborishga yaroqlimi: false
```

# 417-Topshiriq: Reset() metodi orqali obyektni tozalash
## Topshiriq sharti:
Obyekt maydonlarini boshlang'ich nol holatga qaytaruvchi metod yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Bufer struct {
	data []byte
}

func (b *Bufer) Reset() {
	b.data = b.data[:0] // Xotira sig'imini saqlab tozalash
}

func main() {
	buf := &Bufer{data: []byte("muhim ma'lumotlar")}
	fmt.Println("Tozalashdan oldin len:", len(buf.data))

	buf.Reset()
	fmt.Println("Tozalangandan keyin len:", len(buf.data))
}
```

## Tushuntirish va Mantiq:
`Reset()` metodi obyektlarni qayta ishlatishda (object pooling) asosiy vositadir.

## Ishlash natijasi:
```text
Tozalashdan oldin len: 17
Tozalangandan keyin len: 0
```

# 418-Topshiriq: Maxsus tip uchun arifmetik metodlar
## Topshiriq sharti:
Vektor koordinatalari ustida `Add` va `Dot` metodlarini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Vektor2D struct {
	X, Y float64
}

func (v Vektor2D) Add(boshqa Vektor2D) Vektor2D {
	return Vektor2D{X: v.X + boshqa.X, Y: v.Y + boshqa.Y}
}

func (v Vektor2D) Dot(boshqa Vektor2D) float64 {
	return v.X*boshqa.X + v.Y*boshqa.Y
}

func main() {
	v1 := Vektor2D{X: 1, Y: 2}
	v2 := Vektor2D{X: 3, Y: 4}

	v3 := v1.Add(v2)
	skalyar := v1.Dot(v2)

	fmt.Printf("V1 + V2 = %+v\n", v3)
	fmt.Printf("Skalyar ko'paytma: %.1f\n", skalyar)
}
```

## Tushuntirish va Mantiq:
Metodlar matematik modellashtirishni juda ixcham va tushunarli qiladi.

## Ishlash natijasi:
```text
V1 + V2 = {X:4 Y:6}
Skalyar ko'paytma: 11.0
```

# 419-Topshiriq: Slice maxsus turiga metod qo'shish (type IntSlice []int)
## Topshiriq sharti:
Butun sonlar slicesiga `Sum` va `Average` metodlarini biriktiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type SonlarToplami []int

func (s SonlarToplami) Sum() int {
	jami := 0
	for _, v := range s {
		jami += v
	}
	return jami
}

func (s SonlarToplami) Average() float64 {
	if len(s) == 0 {
		return 0
	}
	return float64(s.Sum()) / float64(len(s))
}

func main() {
	toplam := SonlarToplami{10, 20, 30, 40}

	fmt.Println("Yig'indi:", toplam.Sum())
	fmt.Printf("O'rtacha: %.1f\n", toplam.Average())
}
```

## Tushuntirish va Mantiq:
Slicelarga metod qo'shish orqali kolleksiyalar ustida qulay kengaytmalar yaratiladi.

## Ishlash natijasi:
```text
Yig'indi: 100
O'rtacha: 25.0
```

# 420-Topshiriq: Map maxsus turiga metod qo'shish
## Topshiriq sharti:
Lug'atga yangi xavfsiz metodlar biriktiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type SozlamaMap map[string]string

func (s SozlamaMap) GetDefault(kalit, standart string) string {
	if val, mavjud := s[kalit]; mavjud {
		return val
	}
	return standart
}

func main() {
	sozlamalar := SozlamaMap{"til": "uz"}

	fmt.Println("Til:", sozlamalar.GetDefault("til", "en"))
	fmt.Println("Mavzu:", sozlamalar.GetDefault("mavzu", "light"))
}
```

## Tushuntirish va Mantiq:
Maxsus map turlari yordamida qulay yordamchi API larni shakllantirish mumkin.

## Ishlash natijasi:
```text
Til: uz
Mavzu: light
```

# 421-Topshiriq: Ko'rsatkich qabul qiluvchi metod orqali xotirani tejash
## Topshiriq sharti:
Katta massivga ega struktura uchun Pointer Receiver samaradorligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type KattaMatritsa struct {
	katakchalar [1000][1000]byte
}

func (km *KattaMatritsa) BoshlangichQiymat() byte {
	return km.katakchalar[0][0]
}

func main() {
	m := &KattaMatritsa{}
	fmt.Println("Nusxalanmasdan tezkor o'qildi:", kmVal(m))
}

func kmVal(m *KattaMatritsa) byte {
	return m.BoshlangichQiymat()
}
```

## Tushuntirish va Mantiq:
1 million baytli matritsa har metod chaqirilganda nusxalanmasligi uchun pointer receiver ishlatiladi.

## Ishlash natijasi:
```text
Nusxalanmasdan tezkor o'qildi: 0
```

# 422-Topshiriq: Immutability kafolati: Qiymat qabul qiluvchi metod
## Topshiriq sharti:
Qiymat qabul qiluvchi metod asl holatni o'zgartira olmasligini amalda ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Nuqta struct {
	X int
}

func (n Nuqta) SinovOshir() {
	n.X = 100 // Faqat lokal nusxa o'zgaradi!
}

func main() {
	nuqta := Nuqta{X: 10}
	nuqta.SinovOshir()

	fmt.Println("Asl qiymat o'zgarmadi:", nuqta.X)
}
```

## Tushuntirish va Mantiq:
Xavfsiz va o'zgarmas arxitekturada qiymat qabul qiluvchilar nojo'ya ta'sirlardan (side-effects) to'liq asraydi.

## Ishlash natijasi:
```text
Asl qiymat o'zgarmadi: 10
```

# 423-Topshiriq: Ko'p qiymat va error qaytaruvchi metodlar
## Topshiriq sharti:
Bank hisobidan pul yechish amalini error qaytaruvchi metod sifatida yozing.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

type Hisob struct {
	Mablag float64
}

func (h *Hisob) PulYech(miqdor float64) (float64, error) {
	if miqdor > h.Mablag {
		return h.Mablag, errors.New("mablag' yetarli emas")
	}
	h.Mablag -= miqdor
	return h.Mablag, nil
}

func main() {
	h := &Hisob{Mablag: 1000}

	qoldiq, err := h.PulYech(1500)
	if err != nil {
		fmt.Println("Xatolik:", err)
	} else {
		fmt.Println("Qoldiq:", qoldiq)
	}
}
```

## Tushuntirish va Mantiq:
Metodlar xatoliklarni xuddi funksiyalar kabi `error` orqali xavfsiz qaytaradi.

## Ishlash natijasi:
```text
Xatolik: mablag' yetarli emas
```

# 424-Topshiriq: Metod ichida tashqi paketlar bilan integratsiya
## Topshiriq sharti:
Vaqt oralig'ini tekshiruvchi metod yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

type Sessiya struct {
	Yaratilgan time.Time
	Muddati    time.Duration
}

func (s Sessiya) Eskirdimi() bool {
	return time.Since(s.Yaratilgan) > s.Muddati
}

func main() {
	sess := Sessiya{
		Yaratilgan: time.Now().Add(-2 * time.Hour),
		Muddati:    1 * time.Hour,
	}

	fmt.Println("Sessiya muddati o'tganmi:", sess.Eskirdimi())
}
```

## Tushuntirish va Mantiq:
Metodlar standart kutubxona bilan uzviy integratsiyalashib domen mantiqini ifodalaydi.

## Ishlash natijasi:
```text
Sessiya muddati o'tganmi: true
```

# 425-Topshiriq: Struktura ichki holatini tahlil qiluvchi diagnostika metodi
## Topshiriq sharti:
Tizim sog'lomligini hisobot sifatida chiqaruvchi metod.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Klaster struct {
	Nomi        string
	FaolTugunlar int
	JamiTugunlar int
}

func (k Klaster) SalomatlikHisoboti() string {
	foiz := (float64(k.FaolTugunlar) / float64(k.JamiTugunlar)) * 100
	return fmt.Sprintf("Klaster %s: %.1f%% faol (%d/%d)", k.Nomi, foiz, k.FaolTugunlar, k.JamiTugunlar)
}

func main() {
	kl := Klaster{Nomi: "Prod-Kubernetes", FaolTugunlar: 9, JamiTugunlar: 10}
	fmt.Println(kl.SalomatlikHisoboti())
}
```

## Tushuntirish va Mantiq:
Diagnostika va monitoring metodlari obyektdan mustaqil tahliliy xulosa chiqarish imkonini beradi.

## Ishlash natijasi:
```text
Klaster Prod-Kubernetes: 90.0% faol (9/10)
```

# 426-Topshiriq: sort.Interface metodlari: Len, Less, Swap
## Topshiriq sharti:
Maxsus turni saralash uchun uchta kerakli metodni yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sort"
)

type Shaxs struct {
	Ism  string
	Yosh int
}

type ShaxslarRoyxati []Shaxs

func (s ShaxslarRoyxati) Len() int           { return len(s) }
func (s ShaxslarRoyxati) Less(i, j int) bool { return s[i].Yosh < s[j].Yosh }
func (s ShaxslarRoyxati) Swap(i, j int)      { s[i], s[j] = s[j], s[i] }

func main() {
	odamlar := ShaxslarRoyxati{
		{"Bekzod", 28},
		{"Anvar", 21},
		{"Sardor", 25},
	}

	sort.Sort(odamlar)
	fmt.Println("Yosh bo'yicha saralangan:", odamlar)
}
```

## Tushuntirish va Mantiq:
`sort.Interface` Go ning klassik interfeyslaridan biri bo'lib, `Len()`, `Less()`, `Swap()` metodlari orqali har qanday kolleksiyani saralash imkonini beradi.

## Ishlash natijasi:
```text
Yosh bo'yicha saralangan: [{Anvar 21} {Sardor 25} {Bekzod 28}]
```

# 427-Topshiriq: io.Reader interfeysini amalga oshiruvchi Read metodi
## Topshiriq sharti:
Maxsus satr o'quvchi strukturasiga `Read(p []byte) (n int, err error)` metodini biriktiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io"
)

type MatnOquvchi struct {
	matn   string
	siljish int
}

func (m *MatnOquvchi) Read(p []byte) (int, error) {
	if m.siljish >= len(m.matn) {
		return 0, io.EOF // O'qish yakunlandi
	}
	n := copy(p, m.matn[m.siljish:])
	m.siljish += n
	return n, nil
}

func main() {
	r := &MatnOquvchi{matn: "Salom io.Reader!"}
	bufer := make([]byte, 8)

	for {
		n, err := r.Read(bufer)
		if n > 0 {
			fmt.Printf("O'qildi (%d bayt): %s\n", n, string(bufer[:n]))
		}
		if err == io.EOF {
			break
		}
	}
}
```

## Tushuntirish va Mantiq:
`Read` metodi Go ning butun I/O oqimlari (fayllar, tarmoq ulanishlari, HTTP) poydevori hisoblanadi.

## Ishlash natijasi:
```text
O'qildi (8 bayt): Salom io
O'qildi (7 bayt): .Reader!
```

# 428-Topshiriq: io.Writer interfeysini amalga oshiruvchi Write metodi
## Topshiriq sharti:
Baytlar oqimini yig'uvchi maxsus `Write(p []byte) (n int, err error)` metodini yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
)

type MaxsusYozuvchi struct {
	jamiBaytlar int
}

func (m *MaxsusYozuvchi) Write(p []byte) (int, error) {
	m.jamiBaytlar += len(p)
	fmt.Printf("[YOZILDI] %s\n", string(p))
	return len(p), nil
}

func main() {
	yozuvchi := &MaxsusYozuvchi{}
	fmt.Fprintln(yozuvchi, "Salom Go I/O!")

	fmt.Printf("Jami yozilgan hajm: %d bayt\n", yozuvchi.jamiBaytlar)
}
```

## Tushuntirish va Mantiq:
`io.Writer` orqali `fmt.Fprintf` kabi standart funksiyalar har qanday maxsus struktura bilan ishlay oladi.

## Ishlash natijasi:
```text
[YOZILDI] Salom Go I/O!

Jami yozilgan hajm: 14 bayt
```

# 429-Topshiriq: io.Closer interfeysini amalga oshiruvchi Close metodi
## Topshiriq sharti:
Resurslarni xavfsiz yopuvchi `Close() error` metodini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Ulanish struct {
	Ochiqmi bool
}

func (u *Ulanish) Close() error {
	if !u.Ochiqmi {
		return fmt.Errorf("ulanish allaqachon yopilgan")
	}
	u.Ochiqmi = false
	fmt.Println("[ULANISH] Tarmoq ulanishi xavfsiz yopildi.")
	return nil
}

func main() {
	u := &Ulanish{Ochiqmi: true}
	_ = u.Close()
}
```

## Tushuntirish va Mantiq:
`Close()` metodi defer bilan birgalikda resurslar sizishining oldini oluvchi standartdir.

## Ishlash natijasi:
```text
[ULANISH] Tarmoq ulanishi xavfsiz yopildi.
```

# 430-Topshiriq: json.Marshaler interfeysi: Maxsus MarshalJSON() metodi
## Topshiriq sharti:
Vaqt yoki sanani o'zingiz xohlagan formatda JSON ga chiqaruvchi metod yozing.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"time"
)

type MaxsusSana struct {
	time.Time
}

func (s MaxsusSana) MarshalJSON() ([]byte, error) {
	formatlangan := fmt.Sprintf(""%s"", s.Format("02.01.2006"))
	return []byte(formatlangan), nil
}

func main() {
	sana := MaxsusSana{Time: time.Date(2026, 11, 8, 0, 0, 0, 0, time.UTC)}
	data, _ := json.Marshal(sana)

	fmt.Println("Maxsus formatlangan JSON:", string(data))
}
```

## Tushuntirish va Mantiq:
`MarshalJSON` orqali standart JSON formatlash o'rniga o'zimizning maxsus qoidalarimizni o'rnatishimiz mumkin.

## Ishlash natijasi:
```text
Maxsus formatlangan JSON: "08.11.2026"
```

# 431-Topshiriq: json.Unmarshaler interfeysi: Maxsus UnmarshalJSON() metodi
## Topshiriq sharti:
Kiritilgan JSON qiymatini maxsus tahlil qilib obyektga yuklang.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"strings"
)

type KattaHarfMatn string

func (k *KattaHarfMatn) UnmarshalJSON(b []byte) error {
	var s string
	if err := json.Unmarshal(b, &s); err != nil {
		return err
	}
	*k = KattaHarfMatn(strings.ToUpper(s))
	return nil
}

func main() {
	jsonSatr := `"golang juda kuchli"`
	var matn KattaHarfMatn

	_ = json.Unmarshal([]byte(jsonSatr), &matn)
	fmt.Println("Avtomatik katta harflarga o'tdi:", matn)
}
```

## Tushuntirish va Mantiq:
`UnmarshalJSON` kiruvchi JSON ma'lumotlarini qabul qilish paytida avtomatik qayta ishlash imkonini beradi.

## Ishlash natijasi:
```text
Avtomatik katta harflarga o'tdi: GOLANG JUDA KUCHLI
```

# 432-Topshiriq: Metodlar orqali Chekli Avtomat (Finite State Machine) holatlarini boshqarish
## Topshiriq sharti:
Turniket (Turnstile) holatlarini (Qulflangan / Ochiq) metodlar orqali boshqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type TurniketHolati int

const (
	Qulflangan TurniketHolati = iota
	Ochiq
)

type Turniket struct {
	holat TurniketHolati
}

func (t *Turniket) TangaTashla() {
	if t.holat == Qulflangan {
		t.holat = Ochiq
		fmt.Println("[TURNIKET] Tanga qabul qilindi. Eshik ochildi!")
	} else {
		fmt.Println("[TURNIKET] Eshik allaqachon ochiq, tanga qaytarildi.")
	}
}

func (t *Turniket) ItaribOt() {
	if t.holat == Ochiq {
		t.holat = Qulflangan
		fmt.Println("[TURNIKET] Odam o'tdi. Eshik qulflandi.")
	} else {
		fmt.Println("[TURNIKET] Qulflangan! Avval tanga tashlang.")
	}
}

func main() {
	t := &Turniket{holat: Qulflangan}
	t.ItaribOt()
	t.TangaTashla()
	t.ItaribOt()
}
```

## Tushuntirish va Mantiq:
FSM holat mashinalari metodlar ichida qoidalarni tekshirish orqali tizimning xavfsiz ishlashini kafolatlaydi.

## Ishlash natijasi:
```text
[TURNIKET] Qulflangan! Avval tanga tashlang.
[TURNIKET] Tanga qabul qilindi. Eshik ochildi!
[TURNIKET] Odam o'tdi. Eshik qulflandi.
```

# 433-Topshiriq: Obunachi (Observer) andozasi: Subscribe va Notify metodlari
## Topshiriq sharti:
Voqea sodir bo'lganda barcha obunachilarga xabar tarqatuvchi tizim yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Obunachi func(xabar string)

type YangiliklarKanal struct {
	obunachilar []Obunachi
}

func (y *YangiliklarKanal) ObunaBol(o Obunachi) {
	y.obunachilar = append(y.obunachilar, o)
}

func (y *YangiliklarKanal) XabarTarqat(xabar string) {
	for _, o := range y.obunachilar {
		o(xabar)
	}
}

func main() {
	kanal := &YangiliklarKanal{}

	kanal.ObunaBol(func(x string) { fmt.Println("Foydalanuvchi A oldi:", x) })
	kanal.ObunaBol(func(x string) { fmt.Println("Foydalanuvchi B oldi:", x) })

	kanal.XabarTarqat("Go 1.23 versiyasi chiqdi!")
}
```

## Tushuntirish va Mantiq:
Observer andozasi hodisalar (events) asosidagi tizimlarda xabarlarni tarqatish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Foydalanuvchi A oldi: Go 1.23 versiyasi chiqdi!
Foydalanuvchi B oldi: Go 1.23 versiyasi chiqdi!
```

# 434-Topshiriq: Komanda (Command) andozasi: Execute va Undo metodlari
## Topshiriq sharti:
Amalni bajarish va uni orqaga qaytarish (Undo) imkoniyatiga ega komanda metodi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type MatnMuharriri struct {
	matn string
}

type MatnQoshishBuyrugi struct {
	muharrir *MatnMuharriri
	qoshildi string
}

func (c *MatnQoshishBuyrugi) Execute() {
	c.muharrir.matn += c.qoshildi
}

func (c *MatnQoshishBuyrugi) Undo() {
	l := len(c.muharrir.matn) - len(c.qoshildi)
	c.muharrir.matn = c.muharrir.matn[:l]
}

func main() {
	editor := &MatnMuharriri{}
	cmd := &MatnQoshishBuyrugi{muharrir: editor, qoshildi: "Salom Dunyo!"}

	cmd.Execute()
	fmt.Println("Execute dan so'ng:", editor.matn)

	cmd.Undo()
	fmt.Println("Undo dan so'ng:", editor.matn)
}
```

## Tushuntirish va Mantiq:
Command andozasi foydalanuvchi amallarini qaytarish (Ctrl+Z) va tranzaksiyalar boshqaruvida keng qo'llaniladi.

## Ishlash natijasi:
```text
Execute dan so'ng: Salom Dunyo!
Undo dan so'ng:
```

# 435-Topshiriq: Iterator andozasi: HasNext va Next metodlari
## Topshiriq sharti:
Kolleksiya ichki tuzilishini oshkor qilmasdan elementlarni ketma-ket o'qish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type IntIterator struct {
	sonlar []int
	indeks int
}

func (it *IntIterator) HasNext() bool {
	return it.indeks < len(it.sonlar)
}

func (it *IntIterator) Next() int {
	val := it.sonlar[it.indeks]
	it.indeks++
	return val
}

func main() {
	iter := &IntIterator{sonlar: []int{10, 20, 30}}

	for iter.HasNext() {
		fmt.Printf("%d ", iter.Next())
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Iterator andozasi ma'lumotlar oqimini bir tekis aylanib chiqishni ta'minlaydi.

## Ishlash natijasi:
```text
10 20 30
```

# 436-Topshiriq: Strategiya (Strategy) andozasi metodlari
## Topshiriq sharti:
To'lov tizimlarini dinamik tanlash uchun metodlar majmuasi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type TolovStrategiyasi interface {
	Tola(summa float64)
}

type ClickTolov struct{}
func (c ClickTolov) Tola(s float64) { fmt.Printf("Click orqali %.0f so'm to'landi\n", s) }

type PaymeTolov struct{}
func (p PaymeTolov) Tola(s float64) { fmt.Printf("Payme orqali %.0f so'm to'landi\n", s) }

type BuyurtmaTo'lov struct {
	strategiya TolovStrategiyasi
}

func (b *BuyurtmaTo'lov) AmalgaOshir(summa float64) {
	b.strategiya.Tola(summa)
}

func main() {
	bt := &BuyurtmaTo'lov{strategiya: ClickTolov{}}
	bt.AmalgaOshir(50000)

	bt.strategiya = PaymeTolov{}
	bt.AmalgaOshir(75000)
}
```

## Tushuntirish va Mantiq:
Strategiya andozasi algoritmni dastur ishlashi davomida dinamik almashtirishga imkon beradi.

## Ishlash natijasi:
```text
Click orqali 50000 so'm to'landi
Payme orqali 75000 so'm to'landi
```

# 437-Topshiriq: Adapter andozasi metodlari
## Topshiriq sharti:
Eski interfeysni yangi talabga moslashtiruvchi adapter metodi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type EskiPrinter struct{}
func (e EskiPrinter) ChopEtEski(matn string) { fmt.Println("[ESKI]:", matn) }

type YangiPrinter interface {
	ChopEt(matn string)
}

type PrinterAdapter struct {
	eski EskiPrinter
}

func (a PrinterAdapter) ChopEt(matn string) {
	a.eski.ChopEtEski(matn) // Metodlar o'rtasida ko'prik
}

func main() {
	var p YangiPrinter = PrinterAdapter{eski: EskiPrinter{}}
	p.ChopEt("Moslashtirilgan xabar")
}
```

## Tushuntirish va Mantiq:
Adapter andozasi mos kelmaydigan interfeyslarni o'zaro bog'laydi.

## Ishlash natijasi:
```text
[ESKI]: Moslashtirilgan xabar
```

# 438-Topshiriq: Dekorator (Decorator) andozasi metodlari
## Topshiriq sharti:
Obyektga yangi xatti-harakatlarni qo'shimcha metod qatlamlari bilan yuklang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Qahva interface {
	Narx() float64
}

type OddiyQahva struct{}
func (o OddiyQahva) Narx() float64 { return 15000.0 }

type SutliQahva struct {
	asos Qahva
}
func (s SutliQahva) Narx() float64 { return s.asos.Narx() + 5000.0 }

func main() {
	q := OddiyQahva{}
	sutli := SutliQahva{asos: q}

	fmt.Printf("Oddiy qahva: %.0f so'm\n", q.Narx())
	fmt.Printf("Sutli qahva: %.0f so'm\n", sutli.Narx())
}
```

## Tushuntirish va Mantiq:
Dekorator andozasi mavjud kodni o'zgartirmasdan funksionallikni kengaytiradi (Open-Closed Principle).

## Ishlash natijasi:
```text
Oddiy qahva: 15000 so'm
Sutli qahva: 20000 so'm
```

# 439-Topshiriq: Factory Method andozasi struktura metodi sifatida
## Topshiriq sharti:
Kerakli turdagi obyektni yaratib beruvchi zavod metodi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Transport interface {
	YetkazibBer() string
}

type YukMashinasi struct{}
func (y YukMashinasi) YetkazibBer() string { return "Quruqlik orqali yuk tashish" }

type Kema struct{}
func (k Kema) YetkazibBer() string { return "Dengiz orqali konteyner tashish" }

type Logistika struct{}

func (l Logistika) YaratTransport(tur string) Transport {
	if tur == "dengiz" {
		return Kema{}
	}
	return YukMashinasi{}
}

func main() {
	log := Logistika{}
	t1 := log.YaratTransport("quruqlik")
	t2 := log.YaratTransport("dengiz")

	fmt.Println("Transport 1:", t1.YetkazibBer())
	fmt.Println("Transport 2:", t2.YetkazibBer())
}
```

## Tushuntirish va Mantiq:
Factory Method obyekt yaratish mantig'ini chaqiruvchi koddan ajratadi.

## Ishlash natijasi:
```text
Transport 1: Quruqlik orqali yuk tashish
Transport 2: Dengiz orqali konteyner tashish
```

# 440-Topshiriq: Object Pool metodlari: Get va Put
## Topshiriq sharti:
Xotirani tejash uchun obyektlarni qayta ishlatuvchi hovuz (pool) metodlari.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Resurs struct {
	ID int
}

type ResursHovuzi struct {
	hovuz []*Resurs
}

func (h *ResursHovuzi) Get() *Resurs {
	if len(h.hovuz) == 0 {
		return &Resurs{ID: 1} // Yangi yaratish
	}
	r := h.hovuz[len(h.hovuz)-1]
	h.hovuz = h.hovuz[:len(h.hovuz)-1]
	return r
}

func (h *ResursHovuzi) Put(r *Resurs) {
	h.hovuz = append(h.hovuz, r)
}

func main() {
	pool := &ResursHovuzi{}
	res := pool.Get()
	fmt.Printf("Olingan resurs: %+v\n", res)

	pool.Put(res)
	fmt.Printf("Qaytarilgach hovuzdagi resurslar soni: %d\n", len(pool.hovuz))
}
```

## Tushuntirish va Mantiq:
Object Pool Garbage Collector yuklamasini kamaytirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Olingan resurs: &{ID:1}
Qaytarilgach hovuzdagi resurslar soni: 1
```

# 441-Topshiriq: Ruxsatlarni tekshiruvchi Can() metodi
## Topshiriq sharti:
Foydalanuvchi huquqlarini tekshiruvchi sodda va tushunarli metod yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Foydalanuvchi struct {
	Huquqlar map[string]bool
}

func (f Foydalanuvchi) Can(amal string) bool {
	return f.Huquqlar[amal]
}

func main() {
	u := Foydalanuvchi{
		Huquqlar: map[string]bool{"create": true, "delete": false},
	}

	fmt.Println("Yaratish mumkinmi:", u.Can("create"))
	fmt.Println("O'chirish mumkinmi:", u.Can("delete"))
}
```

## Tushuntirish va Mantiq:
`u.Can("write")` sintaksisi o'qilishi eng qulay va ravon xavfsizlik tekshiruvidir.

## Ishlash natijasi:
```text
Yaratish mumkinmi: true
O'chirish mumkinmi: false
```

# 442-Topshiriq: Shifrlash va deshifrlash metodlari
## Topshiriq sharti:
Sezar surilishi (Caesar cipher) orqali matnni shifrlab ochuvchi metodlar.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Shifrlagich struct {
	siljish rune
}

func (s Shifrlagich) Shifrla(matn string) string {
	runelar := []rune(matn)
	for i := range runelar {
		runelar[i] += s.siljish
	}
	return string(runelar)
}

func (s Shifrlagich) Deshifrla(shifr string) string {
	runelar := []rune(shifr)
	for i := range runelar {
		runelar[i] -= s.siljish
	}
	return string(runelar)
}

func main() {
	sh := Shifrlagich{siljish: 3}
	maxfiy := sh.Shifrla("GOLANG")
	asl := sh.Deshifrla(maxfiy)

	fmt.Println("Shifrlangan:", maxfiy)
	fmt.Println("Ochilgan:", asl)
}
```

## Tushuntirish va Mantiq:
Metodlar obyektdagi kalit parametrlarini saqlab shifrlash amallarini bajaradi.

## Ishlash natijasi:
```text
Shifrlangan: JRODQI
Ochilgan: GOLANG
```

# 443-Topshiriq: Metod ichida Goroutine ishga tushirish (Asinxron metod)
## Topshiriq sharti:
Metod chaqirilganda fon jarayonini (goroutine) boshlab yuborish.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

type FonVazifasi struct {
	Nomi string
}

func (f *FonVazifasi) StartAsync() {
	go func() {
		fmt.Printf("[%s] Fon vazifasi boshlandi...\n", f.Nomi)
		time.Sleep(10 * time.Millisecond)
		fmt.Printf("[%s] Fon vazifasi yakunlandi.\n", f.Nomi)
	}()
}

func main() {
	vazifa := &FonVazifasi{Nomi: "LogEksport"}
	vazifa.StartAsync()

	time.Sleep(20 * time.Millisecond) // Goroutine tugashini kutamiz
	fmt.Println("Asosiy dastur tugadi.")
}
```

## Tushuntirish va Mantiq:
Asinxron metodlar orqali og'ir ishlarni orqa fonga jo'natish Go da juda sodda amalga oshiriladi.

## Ishlash natijasi:
```text
[LogEksport] Fon vazifasi boshlandi...
[LogEksport] Fon vazifasi yakunlandi.
Asosiy dastur tugadi.
```

# 444-Topshiriq: Obyekt holatini JSON formatida chiqaruvchi ToJSON metodi
## Topshiriq sharti:
Struktura ichida o'zini JSON satriga aylantiruvchi yordamchi metod yozing.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type Profil struct {
	Ism   string `json:"name"`
	Email string `json:"email"`
}

func (p Profil) ToJSON() (string, error) {
	bytes, err := json.Marshal(p)
	return string(bytes), err
}

func main() {
	pr := Profil{Ism: "Davron", Email: "davron@uz"}
	js, _ := pr.ToJSON()

	fmt.Println("Olingan JSON:", js)
}
```

## Tushuntirish va Mantiq:
`ToJSON()` metodi obyektning o'zini qulay serializatsiya qilish imkonini beradi.

## Ishlash natijasi:
```text
Olingan JSON: {"name":"Davron","email":"davron@uz"}
```

# 445-Topshiriq: Muddati va foizini hisoblovchi Kredit metodi
## Topshiriq sharti:
Kredit strukturasi va uning oylik to'lovini hisoblovchi metod.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Kredit struct {
	AsosiySumma float64
	YillikFoiz  float64
	MuddatOy    int
}

func (k Kredit) OylikTolov() float64 {
	jamiFoiz := k.AsosiySumma * (k.YillikFoiz / 100.0) * (float64(k.MuddatOy) / 12.0)
	jamiQarz := k.AsosiySumma + jamiFoiz
	return jamiQarz / float64(k.MuddatOy)
}

func main() {
	kr := Kredit{AsosiySumma: 12000000, YillikFoiz: 20, MuddatOy: 12}
	fmt.Printf("Oylik to'lov: %.0f so'm\n", kr.OylikTolov())
}
```

## Tushuntirish va Mantiq:
Domen hisob-kitoblari metodlar ichida mujassamlashadi.

## Ishlash natijasi:
```text
Oylik to'lov: 1200000 so'm
```

# 446-Topshiriq: Tranzaksiyani bekor qilish va qaytarish (Rollback) metodi
## Topshiriq sharti:
Amal muvaffaqiyatsiz bo'lganda holatni orqaga qaytaruvchi metod.

## Yechim (Go kodi):
```go
package main

import "fmt"

type HamyonTranzaksiya struct {
	balans      float64
	eskiBalans  float64
}

func (h *HamyonTranzaksiya) Ayir(summa float64) {
	h.eskiBalans = h.balans
	h.balans -= summa
}

func (h *HamyonTranzaksiya) Rollback() {
	h.balans = h.eskiBalans
	fmt.Println("[ROLLBACK] Balans avvalgi holatiga qaytarildi.")
}

func main() {
	ht := &HamyonTranzaksiya{balans: 100000}
	ht.Ayir(40000)
	fmt.Println("Ayirilgach:", ht.balans)

	ht.Rollback()
	fmt.Println("Tiklangach:", ht.balans)
}
```

## Tushuntirish va Mantiq:
Rollback metodlari tranzaksiyaviy yaxlitlikni saqlaydi.

## Ishlash natijasi:
```text
Ayirilgach: 60000
[ROLLBACK] Balans avvalgi holatiga qaytarildi.
Tiklangach: 100000
```

# 447-Topshiriq: Hisobot generatsiya qiluvchi metod
## Topshiriq sharti:
Xodimlar ish haqi hisobotini matn shaklida chiqaruvchi metod.

## Yechim (Go kodi):
```go
package main

import "fmt"

type OylikMaoshlar struct {
	xodimlar map[string]int
}

func (o OylikMaoshlar) ChopEtHisobot() {
	fmt.Println("=== ISH HAQI HISOBOTI ===")
	jami := 0
	for ism, maosh := range o.xodimlar {
		fmt.Printf("- %-10s: $%d\n", ism, maosh)
		jami += maosh
	}
	fmt.Printf("JAMI TO'LOV: $%d\n", jami)
}

func main() {
	om := OylikMaoshlar{xodimlar: map[string]int{"Ali": 1500, "Vali": 1800}}
	om.ChopEtHisobot()
}
```

## Tushuntirish va Mantiq:
Hisobot metodlari kolleksiyalarni chiroyli shaklga keltiradi.

## Ishlash natijasi:
```text
=== ISH HAQI HISOBOTI ===
- Ali       : $1500
- Vali      : $1800
JAMI TO'LOV: $3300
```

# 448-Topshiriq: Matnni tozalash va sanitizatsiya qiluvchi metod
## Topshiriq sharti:
HTML teglari va bo'shliqlarni olib tashlovchi metod yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

type MatnKontent struct {
	matn string
}

func (m *MatnKontent) Sanitize() {
	m.matn = strings.TrimSpace(m.matn)
	m.matn = strings.ReplaceAll(m.matn, "<script>", "")
	m.matn = strings.ReplaceAll(m.matn, "</script>", "")
}

func main() {
	k := &MatnKontent{matn: "  <script>alert(1)</script>Salom Dunyo  "}
	k.Sanitize()

	fmt.Println("Tozalangan matn:", k.matn)
}
```

## Tushuntirish va Mantiq:
Sanitizatsiya metodlari xavfli teglarni zararsizlantiradi.

## Ishlash natijasi:
```text
Tozalangan matn: alert(1)Salom Dunyo
```

# 449-Topshiriq: Metod orqali obyekt nusxasini (Clone) yasash
## Topshiriq sharti:
Strukturadan xotirada to'liq mustaqil yangi klon qaytaruvchi metod yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Sozlama struct {
	Port int
	Rejim string
}

func (s Sozlama) Clone() *Sozlama {
	return &Sozlama{
		Port:  s.Port,
		Rejim: s.Rejim,
	}
}

func main() {
	s1 := Sozlama{Port: 8080, Rejim: "dev"}
	s2 := s1.Clone()

	s2.Port = 9000

	fmt.Println("s1 porti:", s1.Port)
	fmt.Println("s2 porti (klon):", s2.Port)
}
```

## Tushuntirish va Mantiq:
Klonlash metodlari prototip andozasini (Prototype pattern) ta'minlaydi.

## Ishlash natijasi:
```text
s1 porti: 8080
s2 porti (klon): 9000
```

# 450-Topshiriq: Yakuniy amaliy vazifa: 2D Fizika Vektorlari va Geometrik Jismlar Dvigateli
## Topshiriq sharti:
Metodlar, Value va Pointer qabul qiluvchilar, `fmt.Stringer` va metod zanjirlanishini birlashtirgan fizika moduli yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"math"
)

type Vektor struct {
	X, Y float64
}

func (v Vektor) String() string {
	return fmt.Sprintf("(%.1f, %.1f)", v.X, v.Y)
}

func (v Vektor) Uzunlik() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

type Jism struct {
	Nomi      string
	Pozitsiya Vektor
	Tezlik    Vektor
}

func NewJism(nomi string, x, y float64) *Jism {
	return &Jism{
		Nomi:      nomi,
		Pozitsiya: Vektor{X: x, Y: y},
	}
}

func (j *Jism) KuchQo'llash(fx, fy float64) *Jism {
	j.Tezlik.X += fx
	j.Tezlik.Y += fy
	return j // Method chaining
}

func (j *Jism) Qadam(vaqtSoniya float64) {
	j.Pozitsiya.X += j.Tezlik.X * vaqtSoniya
	j.Pozitsiya.Y += j.Tezlik.Y * vaqtSoniya
}

func (j *Jism) String() string {
	return fmt.Sprintf("Jism '%s' | O'rni: %s | Tezligi: %s", j.Nomi, j.Pozitsiya, j.Tezlik)
}

func main() {
	raketa := NewJism("Falcon-9", 0, 0)
	raketa.KuchQo'llash(10, 25)

	fmt.Println("Boshlang'ich:", raketa)

	// 2 soniya parvoz:
	raketa.Qadam(2.0)
	fmt.Println("2 soniyadan so'ng:", raketa)
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriq Go dagi metodlar tizimining barcha nozikliklarini bitta to'liq modelda ko'rsatib beradi.

## Ishlash natijasi:
```text
Boshlang'ich: Jism 'Falcon-9' | O'rni: (0.0, 0.0) | Tezligi: (10.0, 25.0)
2 soniyadan so'ng: Jism 'Falcon-9' | O'rni: (20.0, 50.0) | Tezligi: (10.0, 25.0)
```

