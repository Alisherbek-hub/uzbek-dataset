# 10-Mavzu: Interfeyslar (Interfaces) va Polimorfizm (451-500)

Go tilida interfeyslar implitsit (yashirin) tarzda amalga oshiriladi (`implements` so'zi yo'q - agar tur metodlarga ega bo'lsa, u interfeysni avtomatik qanoatlantiradi). `any` (bo'sh interfeys), Type Assertion (`comma-ok`), Type Switch, Nil Interface tuzilishi (`iface`), `io.Reader`/`io.Writer` kompozitsiyasi, Rob Pike ning bir metodli interfeyslar falsafasi va Dependency Inversion bo'yicha 50 ta amaliy topshiriq.

# 451-Topshiriq: Interfeyslar asoslari: Go da interfeys nima?
## Topshiriq sharti:
Xatti-harakat shartnomasini belgilovchi `Gapiruvchi` interfeysini e'lon qiling va uni ikkita struktura orqali namoyish eting.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Gapiruvchi interface {
	Gapir() string
}

type Inson struct {
	Ism string
}

func (i Inson) Gapir() string {
	return "Salom, mening ismim " + i.Ism
}

type Robot struct {
	Model string
}

func (r Robot) Gapir() string {
	return "Bip-bup! Model: " + r.Model
}

func main() {
	var g1 Gapiruvchi = Inson{Ism: "Davron"}
	var g2 Gapiruvchi = Robot{Model: "T-800"}

	fmt.Println(g1.Gapir())
	fmt.Println(g2.Gapir())
}
```

## Tushuntirish va Mantiq:
Interfeys - bu faqat metodlar imzolarini (signatures) saqlovchi turdir. Unda maydonlar (fields) bo'lmaydi.

## Ishlash natijasi:
```text
Salom, mening ismim Davron
Bip-bup! Model: T-800
```

# 452-Topshiriq: Implitsit (Yashirin) Duck Typing: Nega 'implements' kalit so'zi yo'q?
## Topshiriq sharti:
Hech qanday maxsus kalit so'zsiz turning interfeysni avtomatik amalga oshirishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Qush interface {
	Uch()
}

type Qaldirgoch struct{}

// Qaldirgoch "implements Qush" deb yozmadi, lekin Uch() metodiga ega bo'lgani uchun Qush hisoblanadi!
func (q Qaldirgoch) Uch() {
	fmt.Println("Qaldirg'och osmonda baland uchmoqda.")
}

func Parvoz(q Qush) {
	q.Uch()
}

func main() {
	q := Qaldirgoch{}
	Parvoz(q)
}
```

## Tushuntirish va Mantiq:
Go mashhur 'O'rdak testiga' tayanadi: 'Agar u o'rdakdek suzsa va o'rdakdek qaqillasa, demak u o'rdakdir'. Bu modullar o'rtasida mutlaq erkinlik beradi.

## Ishlash natijasi:
```text
Qaldirg'och osmonda baland uchmoqda.
```

# 453-Topshiriq: Geometrik shakllar polimorfizmi: Shakl interfeysi
## Topshiriq sharti:
`Yuza()` va `Perimetr()` metodlariga ega `Shakl` interfeysi orqali Doira va To'rtburchakni umumiy hisoblang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"math"
)

type Shakl interface {
	Yuza() float64
	Perimetr() float64
}

type Doira struct {
	Radius float64
}

func (d Doira) Yuza() float64     { return math.Pi * d.Radius * d.Radius }
func (d Doira) Perimetr() float64 { return 2 * math.Pi * d.Radius }

type Tortburchak struct {
	Eni, Boyi float64
}

func (t Tortburchak) Yuza() float64     { return t.Eni * t.Boyi }
func (t Tortburchak) Perimetr() float64 { return 2 * (t.Eni + t.Boyi) }

func MalumotChiqar(s Shakl) {
	fmt.Printf("Shakl yuzasi: %.2f | Perimetri: %.2f\n", s.Yuza(), s.Perimetr())
}

func main() {
	d := Doira{Radius: 5}
	tb := Tortburchak{Eni: 4, Boyi: 6}

	MalumotChiqar(d)
	MalumotChiqar(tb)
}
```

## Tushuntirish va Mantiq:
Polimorfizm bitta funksiyaga (`MalumotChiqar`) har qanday mos keluvchi strukturani qabul qilish imkonini beradi.

## Ishlash natijasi:
```text
Shakl yuzasi: 78.54 | Perimetri: 31.42
Shakl yuzasi: 24.00 | Perimetri: 20.00
```

# 454-Topshiriq: Bo'sh interfeys: any (va interface{})
## Topshiriq sharti:
Har qanday turdagi ma'lumotni qabul qila oladigan bo'sh interfeys bilan ishlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func chopEtHarQanday(qiymatlar ...any) {
	for i, q := range qiymatlar {
		fmt.Printf("[%d] Qiymat: %v (Turi: %T)\n", i, q, q)
	}
}

func main() {
	chopEtHarQanday(42, "Salom Go", true, 3.14)
}
```

## Tushuntirish va Mantiq:
Go 1.18 dan boshlab `any` `interface{}` ning to'liq taxallusidir. 0 ta metod talab qilgani uchun har qanday tur uni avtomatik qanoatlantiradi.

## Ishlash natijasi:
```text
[0] Qiymat: 42 (Turi: int)
[1] Qiymat: Salom Go (Turi: string)
[2] Qiymat: true (Turi: bool)
[3] Qiymat: 3.14 (Turi: float64)
```

# 455-Topshiriq: Type Assertion asoslari va Panic xavfi
## Topshiriq sharti:
`any` ichidagi haqiqiy qiymatni o'z turiga o'tkazish va xato turda qanday panik yuz berishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var i any = "Go tili"

	// To'g'ri assertion:
	s := i.(string)
	fmt.Println("Satr qiymati:", s)

	// DIQQAT: Xato assertion:
	// n := i.(int) // PANIC: interface conversion: interface {} is string, not int!
}
```

## Tushuntirish va Mantiq:
`v := i.(Tur)` sintaksisi to'g'ri bo'lsa qiymatni o'zlashtiradi, aks holda dastur panik beradi.

## Ishlash natijasi:
```text
Satr qiymati: Go tili
```

# 456-Topshiriq: Xavfsiz Type Assertion (Comma-ok idiomi)
## Topshiriq sharti:
`val, ok := i.(Tur)` orqali xatoliksiz tur tekshiruvini bajaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var i any = 12345

	if s, ok := i.(string); ok {
		fmt.Println("Bu satr:", s)
	} else {
		fmt.Println("Bu satr emas!")
	}

	if n, ok := i.(int); ok {
		fmt.Println("Bu butun son:", n)
	}
}
```

## Tushuntirish va Mantiq:
`comma-ok` idiomi panik bermaydi: agar tur to'g'ri kelsa `ok = true`, aks holda `ok = false` bo'ladi.

## Ishlash natijasi:
```text
Bu satr emas!
Bu butun son: 12345
```

# 457-Topshiriq: Type Switch konstruksiyasi (switch v := x.(type))
## Topshiriq sharti:
Interfeys ichidagi turni ko'p tarmoqli switch orqali tahlil qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func tahlilTur(x any) {
	switch v := x.(type) {
	case int:
		fmt.Printf("Butun son: %d (Kvadrat: %d)\n", v, v*v)
	case string:
		fmt.Printf("Satr: %q (Uzunlik: %d)\n", v, len(v))
	case bool:
		fmt.Printf("Mantiqiy: %t\n", v)
	default:
		fmt.Printf("Boshqa tur: %T\n", v)
	}
}

func main() {
	tahlilTur(10)
	tahlilTur("Golang")
	tahlilTur(true)
}
```

## Tushuntirish va Mantiq:
Type Switch bir necha castinglarni bitta toza konstruksiyada bajarish uchun qulaydir.

## Ishlash natijasi:
```text
Butun son: 10 (Kvadrat: 100)
Satr: "Golang" (Uzunlik: 6)
Mantiqiy: true
```

# 458-Topshiriq: Go ning eng mashhur tuzog'i: Nil Pointer saqlovchi interfeys Nil EMAS!
## Topshiriq sharti:
`nil` ko'rsatkich interfeysga yuklanganda `interfeys == nil` tekshiruvi nega false bo'lishini isbotlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Xatolar interface {
	Xato() string
}

type MeningXatom struct{}
func (m *MeningXatom) Xato() string { return "xatolik" }

func qaytarXato(bormi bool) Xatolar {
	var p *MeningXatom = nil
	if bormi {
		p = &MeningXatom{}
	}
	return p // DIQQAT: p nil bo'lsa ham interfeys nil emas!
}

func main() {
	err := qaytarXato(false)

	if err != nil {
		fmt.Println("[TUZOQ!] err != nil bo'lib chiqdi, chunki interfeys ichida tur ma'lumoti bor!")
	} else {
		fmt.Println("err to'liq nil.")
	}
}
```

## Tushuntirish va Mantiq:
Interfeys xotirada ikkita narsadan iborat: (Tur, Qiymat). Interfeys faqat ikkalasi ham nil bo'lgandagina nil hisoblanadi. Agar `Tur = *MeningXatom`, `Qiymat = nil` bo'lsa, interfeysning o'zi nil EMAS!

## Ishlash natijasi:
```text
[TUZOQ!] err != nil bo'lib chiqdi, chunki interfeys ichida tur ma'lumoti bor!
```

# 459-Topshiriq: Standart error interfeysi va uning soddaligi
## Topshiriq sharti:
Go tilidagi `error` aslida bitta metodli oddiy interfeys ekanligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

// Go ning standart ta'rifi:
// type error interface {
//     Error() string
// }

type ValidatsiyaXatosi struct {
	Maydon string
	Sabab  string
}

func (v ValidatsiyaXatosi) Error() string {
	return fmt.Sprintf("Maydon '%s' xatosi: %s", v.Maydon, v.Sabab)
}

func main() {
	var err error = ValidatsiyaXatosi{Maydon: "Email", Sabab: "noto'g'ri format"}
	fmt.Println("Xatolik xabari:", err.Error())
}
```

## Tushuntirish va Mantiq:
Go da istalgan tur `Error() string` metodini yozish orqali standart `error` ga aylanadi.

## Ishlash natijasi:
```text
Xatolik xabari: Maydon 'Email' xatosi: noto'g'ri format
```

# 460-Topshiriq: Interfeyslarni o'rnatish / kompozitsiya qilish (Interface Embedding)
## Topshiriq sharti:
`Reader` va `Writer` dan `ReadWriter` interfeysini hosil qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Oquvchi interface {
	Oqi() string
}

type Yozuvchi interface {
	Yoz(string)
}

// Interfeyslar kompozitsiyasi:
type OquvchiYozuvchi interface {
	Oquvchi
	Yozuvchi
}

type XotiraBuferi struct {
	matn string
}

func (x *XotiraBuferi) Oqi() string  { return x.matn }
func (x *XotiraBuferi) Yoz(s string) { x.matn = s }

func main() {
	var rw OquvchiYozuvchi = &XotiraBuferi{}
	rw.Yoz("Yangi ma'lumot")
	fmt.Println("O'qildi:", rw.Oqi())
}
```

## Tushuntirish va Mantiq:
Interfeyslarni birlashtirish orqali kengroq shartnomalar yasaladi (masalan, standart `io.ReadWriter`).

## Ishlash natijasi:
```text
O'qildi: Yangi ma'lumot
```

# 461-Topshiriq: Rob Pike ning bir metodli interfeyslar falsafasi
## Topshiriq sharti:
Nima uchun Go da kichik interfeyslar (`Reader`, `Writer`, `Closer`) eng kuchli ekanligini tushuntiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Yopuvchi interface {
	Close() error
}

type Fayl struct{ Nom string }
func (f Fayl) Close() error { fmt.Println(f.Nom, "yopildi"); return nil }

type Soket struct{ Port int }
func (s Soket) Close() error { fmt.Printf("Port %d yopildi\n", s.Port); return nil }

func ResursniTozala(y Yopuvchi) {
	_ = y.Close()
}

func main() {
	ResursniTozala(Fayl{Nom: "data.txt"})
	ResursniTozala(Soket{Port: 8080})
}
```

## Tushuntirish va Mantiq:
Kichik interfeyslar turli tizimlarni bir-biriga bog'lashda maksimal moslashuvchanlik beradi.

## Ishlash natijasi:
```text
data.txt yopildi
Port 8080 yopildi
```

# 462-Topshiriq: Qiymat turi va Ko'rsatkich turi interfeysni amalga oshirishidagi farq
## Topshiriq sharti:
Pointer receiver li metod interfeysga faqat ko'rsatkich orqali qabul qilinishini isbotlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type O'zgartiruvchi interface {
	Ozgartir()
}

type Sinov struct{}

func (s *Sinov) Ozgartir() {} // Pointer receiver

func main() {
	// var o1 O'zgartiruvchi = Sinov{} // XATO! Sinov turi O'zgartiruvchini to'liq amalga oshirmagan (chunki metod *Sinov da)
	var o2 O'zgartiruvchi = &Sinov{} // TO'G'RI!
	fmt.Printf("Muvaffaqiyatli interfeysga yuklandi: %T\n", o2)
}
```

## Tushuntirish va Mantiq:
Agar metod `(s *Sinov)` bo'lsa, faqat `*Sinov` interfeysga mos keladi, oddiy `Sinov` emas.

## Ishlash natijasi:
```text
Muvaffaqiyatli interfeysga yuklandi: *main.Sinov
```

# 463-Topshiriq: Kompilyatsiya vaqtida interfeys mosligini tekshirish (Compile-Time Interface Check)
## Topshiriq sharti:
`var _ Interface = (*Type)(nil)` idiomi orqali kompilyatsiya paytidayoq metodlar to'liqligini kafolatlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Xizmat interface {
	Ishla()
}

type MeningXizmatim struct{}

func (m *MeningXizmatim) Ishla() {}

// Kompilyatsiya vaqtida tekshirish: agar Ishla() bo'lmasa kompilyator xato beradi!
var _ Xizmat = (*MeningXizmatim)(nil)

func main() {
	fmt.Println("MeningXizmatim Xizmat interfeysini 100% qanoatlantirishi kafolatlangan.")
}
```

## Tushuntirish va Mantiq:
Ushbu qator 0 bayt ishlatadi va kompilyatsiya bosqichidayoq interfeys buzilishini aniqlaydi.

## Ishlash natijasi:
```text
MeningXizmatim Xizmat interfeysini 100% qanoatlantirishi kafolatlangan.
```

# 464-Topshiriq: Polimorfizm: Bir xil interfeysli turlarni slice da saqlash
## Topshiriq sharti:
Turli shakllarni bitta `[]Shakl` massivida saqlab ularning umumiy yuzasini hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type YuzaOlcami interface {
	Yuza() float64
}

type Kvadrat struct{ Tomon float64 }
func (k Kvadrat) Yuza() float64 { return k.Tomon * k.Tomon }

type Doira struct{ Radius float64 }
func (d Doira) Yuza() float64 { return 3.14 * d.Radius * d.Radius }

func main() {
	shakllar := []YuzaOlcami{
		Kvadrat{Tomon: 4},
		Doira{Radius: 2},
		Kvadrat{Tomon: 5},
	}

	jami := 0.0
	for _, s := range shakllar {
		jami += s.Yuza()
	}

	fmt.Printf("Jami yuzalar: %.2f\n", jami)
}
```

## Tushuntirish va Mantiq:
Interfeys slicesi orqali har xil turlar bitta kolleksiyaga yig'iladi va bir xil boshqariladi.

## Ishlash natijasi:
```text
Jami yuzalar: 53.56
```

# 465-Topshiriq: Dependency Inversion Principle (DIP) va Mocking
## Topshiriq sharti:
Haqiqiy ma'lumotlar bazasi o'rniga test uchun Fake (Mock) interfeys yasang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type FoydalanuvchiRepo interface {
	GetEmail(id int) string
}

// Test uchun qalbaki repozitoriy:
type MockRepo struct{}
func (m MockRepo) GetEmail(id int) string { return "test@mock.uz" }

type BildirishnomaServis struct {
	repo FoydalanuvchiRepo
}

func (b BildirishnomaServis) XabarYubor(id int) {
	email := b.repo.GetEmail(id)
	fmt.Printf("Xabar %s ga yuborildi\n", email)
}

func main() {
	servis := BildirishnomaServis{repo: MockRepo{}}
	servis.XabarYubor(1)
}
```

## Tushuntirish va Mantiq:
Interfeyslar tufayli tashqi bog'liqliklarni o'chirib testlarni tez va mustaqil o'tkazish mumkin.

## Ishlash natijasi:
```text
Xabar test@mock.uz ga yuborildi
```

# 466-Topshiriq: Interfeys qayerda e'lon qilinishi kerak? (Consumer vs Producer)
## Topshiriq sharti:
Go qoidasi: Interfeysni ma'lumotni ishlab chiqaruvchi emas, balki undan foydalanuvchi paket e'lon qilishi kerak.

## Yechim (Go kodi):
```go
package main

import "fmt"

// Foydalanuvchi tomonida talab qilinadigan kichik interfeys:
type Oqituvchi interface {
	DarsOt()
}

type Domla struct{}
func (d Domla) DarsOt() { fmt.Println("Universitetda Go darsi o'tilmoqda.") }

func DarsJarayoni(o Oqituvchi) {
	o.DarsOt()
}

func main() {
	d := Domla{}
	DarsJarayoni(d)
}
```

## Tushuntirish va Mantiq:
Boshqa tillardan farqli ravishda Go da paketlar ulkan interfeyslarni eksport qilmaydi; har bir iste'molchi o'ziga kerakli kichik interfeysni o'zi belgilaydi.

## Ishlash natijasi:
```text
Universitetda Go darsi o'tilmoqda.
```

# 467-Topshiriq: Anonim interfeyslar (Inline Anonymous Interfaces)
## Topshiriq sharti:
Alohida nom berilmagan vaqtinchalik parametr interfeysidan foydalaning.

## Yechim (Go kodi):
```go
package main

import "fmt"

func salomBer(shaxs interface{ Ism() string }) {
	fmt.Println("Assalomu alaykum,", shaxs.Ism())
}

type Mehmon struct{ nom string }
func (m Mehmon) Ism() string { return m.nom }

func main() {
	salomBer(Mehmon{nom: "Sherzod"})
}
```

## Tushuntirish va Mantiq:
Anonim interfeyslar faqat bitta funksiya uchun zarur bo'lgan minimal shartnomani tezkor belgilaydi.

## Ishlash natijasi:
```text
Assalomu alaykum, Sherzod
```

# 468-Topshiriq: Dynamic Dispatch xarajati va interfeys samaradorligi
## Topshiriq sharti:
Interfeys chaqiruvi virtual metod jadvali (`itab`) orqali bajarilishini tushunish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Amal interface {
	Hisobla(a, b int) int
}

type Qoshuvchi struct{}
func (Qoshuvchi) Hisobla(a, b int) int { return a + b }

func main() {
	var a Amal = Qoshuvchi{}
	res := a.Hisobla(10, 20)
	fmt.Println("Interfeys orqali natija:", res)
}
```

## Tushuntirish va Mantiq:
Interfeys chaqiruvlari to'g'ridan-to'g'ri statik chaqiruvdan bir necha nanosekund sekinroq ishlaydi, ammo beradigan moslashuvchanligi cheksizdir.

## Ishlash natijasi:
```text
Interfeys orqali natija: 30
```

# 469-Topshiriq: Kesh interfeysi va ko'p qatlamli xotira
## Topshiriq sharti:
Kesh interfeysi orqali xotirada (In-Memory) keshlovchi tizim yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Kesh interface {
	Get(key string) (string, bool)
	Set(key, val string)
}

type MemoryKesh struct {
	baza map[string]string
}

func (m *MemoryKesh) Get(k string) (string, bool) {
	v, ok := m.baza[k]
	return v, ok
}

func (m *MemoryKesh) Set(k, v string) {
	m.baza[k] = v
}

func main() {
	var kesh Kesh = &MemoryKesh{baza: make(map[string]string)}
	kesh.Set("sessiya_1", "user_101")

	val, _ := kesh.Get("sessiya_1")
	fmt.Println("Keshdan olindi:", val)
}
```

## Tushuntirish va Mantiq:
Kesh interfeysi keyinchalik Redis yoki Memcached ga o'tishni kodni o'zgartirmasdan ta'minlaydi.

## Ishlash natijasi:
```text
Keshdan olindi: user_101
```

# 470-Topshiriq: Logger interfeysi va moslashuvchan log yozuvchi
## Topshiriq sharti:
Har xil darajadagi xabarlarni loglovchi interfeys tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Logger interface {
	Info(msg string)
	Error(msg string)
}

type StandartLogger struct{}

func (s StandartLogger) Info(msg string)  { fmt.Println("[INFO]:", msg) }
func (s StandartLogger) Error(msg string) { fmt.Println("[ERROR]:", msg) }

func main() {
	var log Logger = StandartLogger{}
	log.Info("Server 8080-portda boshlandi")
	log.Error("Ma'lumotlar bazasiga ulanib bo'lmadi")
}
```

## Tushuntirish va Mantiq:
Logger interfeysi tufayli dasturni istalgan tashqi log tizimiga (Zap, Slog, Logrus) ulash oson.

## Ishlash natijasi:
```text
[INFO]: Server 8080-portda boshlandi
[ERROR]: Ma'lumotlar bazasiga ulanib bo'lmadi
```

# 471-Topshiriq: Notifier interfeysi: Email, SMS, Telegram
## Topshiriq sharti:
Xabarnoma yuboruvchi turli kanallarni polimorfik boshqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Notifier interface {
	Send(kimga, xabar string)
}

type SMSNotifier struct{}
func (s SMSNotifier) Send(k, x string) { fmt.Printf("[SMS -> %s]: %s\n", k, x) }

type TelegramNotifier struct{}
func (t TelegramNotifier) Send(k, x string) { fmt.Printf("[TG -> %s]: %s\n", k, x) }

func main() {
	kanallar := []Notifier{
		SMSNotifier{},
		TelegramNotifier{},
	}

	for _, k := range kanallar {
		k.Send("+998901234567", "Sizning parolingiz: 7788")
	}
}
```

## Tushuntirish va Mantiq:
Barcha xabar yuborish kanallari yagona interfeys orqali parallel ishlatiladi.

## Ishlash natijasi:
```text
[SMS -> +998901234567]: Sizning parolingiz: 7788
[TG -> +998901234567]: Sizning parolingiz: 7788
```

# 472-Topshiriq: Shifrlash (Crypto) interfeysi
## Topshiriq sharti:
Ma'lumotlarni shifrlash va deshifrlash shartnomasini belgilang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Shifrlovchi interface {
	Encrypt(data []byte) []byte
	Decrypt(data []byte) []byte
}

type XorShifr struct {
	Kalit byte
}

func (x XorShifr) Encrypt(d []byte) []byte {
	res := make([]byte, len(d))
	for i, b := range d {
		res[i] = b ^ x.Kalit
	}
	return res
}

func (x XorShifr) Decrypt(d []byte) []byte {
	return x.Encrypt(d) // XOR qayta qo'llansa ochiladi
}

func main() {
	var s Shifrlovchi = XorShifr{Kalit: 0xAA}
	asl := []byte("Maxfiy Matn")

	shifr := s.Encrypt(asl)
	ochiq := s.Decrypt(shifr)

	fmt.Println("Ochilgan matn:", string(ochiq))
}
```

## Tushuntirish va Mantiq:
Shifrlash interfeysi har qanday simmetrik yoki asimmetrik algoritmni xavfsiz o'rash imkonini beradi.

## Ishlash natijasi:
```text
Ochilgan matn: Maxfiy Matn
```

# 473-Topshiriq: Repozitoriy (Repository) interfeysi va CRUD operatsiyalari
## Topshiriq sharti:
Foydalanuvchi ma'lumotlarini saqlash va olish shartnomasini tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Foydalanuvchi struct {
	ID  int
	Ism string
}

type UserRepository interface {
	Save(u Foydalanuvchi) error
	FindByID(id int) (Foydalanuvchi, bool)
}

type InMemUserRepo struct {
	baza map[int]Foydalanuvchi
}

func (r *InMemUserRepo) Save(u Foydalanuvchi) error {
	r.baza[u.ID] = u
	return nil
}

func (r *InMemUserRepo) FindByID(id int) (Foydalanuvchi, bool) {
	u, ok := r.baza[id]
	return u, ok
}

func main() {
	var repo UserRepository = &InMemUserRepo{baza: make(map[int]Foydalanuvchi)}
	_ = repo.Save(Foydalanuvchi{ID: 1, Ism: "Dilshod"})

	user, _ := repo.FindByID(1)
	fmt.Printf("Repozitoriydan topildi: %+v\n", user)
}
```

## Tushuntirish va Mantiq:
Repository andozasi biznes logikani ma'lumotlar bazasi implementatsiyasidan to'liq ajratadi.

## Ishlash natijasi:
```text
Repozitoriydan topildi: {ID:1 Ism:Dilshod}
```

# 474-Topshiriq: Validatsiya interfeysi: Validatable
## Topshiriq sharti:
Har qanday ma'lumot o'zini tekshira olishi uchun interfeys yozing.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

type Validatable interface {
	Validate() error
}

type RegistratsiyaSo'rovi struct {
	Login string
	Yosh  int
}

func (r RegistratsiyaSo'rovi) Validate() error {
	if len(r.Login) < 3 {
		return errors.New("login kamida 3 ta belgi bo'lishi shart")
	}
	if r.Yosh < 18 {
		return errors.New("yosh kamida 18 bo'lishi shart")
	}
	return nil
}

func QabulQil(v Validatable) {
	if err := v.Validate(); err != nil {
		fmt.Println("[RAD ETILDI]:", err)
	} else {
		fmt.Println("[QABUL QILINDI]: Ma'lumotlar to'g'ri!")
	}
}

func main() {
	QabulQil(RegistratsiyaSo'rovi{Login: "ab", Yosh: 20})
	QabulQil(RegistratsiyaSo'rovi{Login: "kamron", Yosh: 22})
}
```

## Tushuntirish va Mantiq:
Validatable interfeysi kiruvchi DTO obyektlarining to'g'riligini umumiy nazorat qilish imkonini beradi.

## Ishlash natijasi:
```text
[RAD ETILDI]: login kamida 3 ta belgi bo'lishi shart
[QABUL QILINDI]: Ma'lumotlar to'g'ri!
```

# 475-Topshiriq: DB Driver interfeysi abstraksiyasi
## Topshiriq sharti:
Turli ma'lumotlar bazalari (Postgres, MySQL) uchun yagona drayver interfeysini modellashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type DBDriver interface {
	Connect(dsn string) error
	Execute(query string) string
}

type PostgresDriver struct{}
func (p PostgresDriver) Connect(dsn string) error { return nil }
func (p PostgresDriver) Execute(q string) string  { return "PostgreSQL natijasi: " + q }

func main() {
	var db DBDriver = PostgresDriver{}
	_ = db.Connect("postgres://localhost:5432/db")

	fmt.Println(db.Execute("SELECT * FROM users"))
}
```

## Tushuntirish va Mantiq:
Go ning standart `database/sql` drayverlari aynan shu xil interfeyslar orqali ulanadi.

## Ishlash natijasi:
```text
PostgreSQL natijasi: SELECT * FROM users
```

# 476-Topshiriq: http.Handler interfeysi: ServeHTTP metodining kuchi
## Topshiriq sharti:
Go ning standart `net/http` paketi asosi bo'lgan `http.Handler` interfeysini amalga oshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

type SalomHandler struct{}

func (s SalomHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Salom, bu maxsus http.Handler!")
}

func main() {
	handler := SalomHandler{}

	req := httptest.NewRequest("GET", "/", nil)
	rec := httptest.NewRecorder()

	handler.ServeHTTP(rec, req)

	fmt.Println("HTTP Status:", rec.Code)
	fmt.Println("Javob tanasi:", rec.Body.String())
}
```

## Tushuntirish va Mantiq:
`http.Handler` bitta `ServeHTTP(ResponseWriter, *Request)` metodidan iborat bo'lib, butun Go veb infratuzilmasi shu interfeys atrofida qurilgan.

## Ishlash natijasi:
```text
HTTP Status: 200
Javob tanasi: Salom, bu maxsus http.Handler!
```

# 477-Topshiriq: http.HandlerFunc adapter turi: Funksiyani interfeysga aylantirish
## Topshiriq sharti:
Oddiy funksiyani `http.HandlerFunc` orqali `http.Handler` interfeysiga o'giring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func meningFunksiyam(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Funksiya handlerga aylantirildi")
}

func main() {
	var handler http.Handler = http.HandlerFunc(meningFunksiyam)

	req := httptest.NewRequest("GET", "/test", nil)
	rec := httptest.NewRecorder()

	handler.ServeHTTP(rec, req)
	fmt.Println("Natija:", rec.Body.String())
}
```

## Tushuntirish va Mantiq:
`http.HandlerFunc` bu funksiya turi bo'lib, uning o'zida `ServeHTTP` metodi mavjud. Bu Go dagi eng go'zal adapter andozasidir.

## Ishlash natijasi:
```text
Natija: Funksiya handlerga aylantirildi
```

# 478-Topshiriq: Serializator interfeysi: JSON va XML
## Topshiriq sharti:
Ma'lumotlarni turli formatlarga serializatsiya qiluvchi interfeys tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"encoding/xml"
	"fmt"
)

type Serializer interface {
	Serialize(v any) ([]byte, error)
}

type JSONSerializer struct{}
func (JSONSerializer) Serialize(v any) ([]byte, error) { return json.Marshal(v) }

type XMLSerializer struct{}
func (XMLSerializer) Serialize(v any) ([]byte, error) { return xml.Marshal(v) }

type Xodim struct {
	Ism string `json:"name" xml:"Name"`
}

func main() {
	x := Xodim{Ism: "Sherzod"}

	var s1 Serializer = JSONSerializer{}
	var s2 Serializer = XMLSerializer{}

	j, _ := s1.Serialize(x)
	xData, _ := s2.Serialize(x)

	fmt.Println("JSON:", string(j))
	fmt.Println("XML:", string(xData))
}
```

## Tushuntirish va Mantiq:
Serializer interfeysi formatlash texnologiyasini mustaqil almashtirish imkonini beradi.

## Ishlash natijasi:
```text
JSON: {"name":"Sherzod"}
XML: <Xodim><Name>Sherzod</Name></Xodim>
```

# 479-Topshiriq: Konfiguratsiya provayderi interfeysi: Env va Memory
## Topshiriq sharti:
Turli manbalardan sozlamalarni o'quvchi konfiguratsiya interfeysi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type ConfigProvider interface {
	GetString(key string) string
}

type MemoryConfig struct {
	data map[string]string
}
func (m MemoryConfig) GetString(k string) string { return m.data[k] }

func main() {
	var cfg ConfigProvider = MemoryConfig{data: map[string]string{"PORT": "9090"}}
	fmt.Println("O'qilgan port:", cfg.GetString("PORT"))
}
```

## Tushuntirish va Mantiq:
Konfiguratsiya interfeysi dasturni turli muhitlarda (dev, test, prod) bir xil ishlashini ta'minlaydi.

## Ishlash natijasi:
```text
O'qilgan port: 9090
```

# 480-Topshiriq: Xabarlar navbati (Message Queue Producer) interfeysi
## Topshiriq sharti:
Kafka va RabbitMQ drayverlari uchun umumiy navbat interfeysini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type MessageQueue interface {
	Publish(topic string, data []byte) error
}

type MockKafka struct{}

func (m MockKafka) Publish(topic string, data []byte) error {
	fmt.Printf("[KAFKA] '%s' mavzusiga %d bayt yuborildi\n", topic, len(data))
	return nil
}

func main() {
	var mq MessageQueue = MockKafka{}
	_ = mq.Publish("orders.created", []byte(`{"order_id": 55}`))
}
```

## Tushuntirish va Mantiq:
Taqsimlangan arxitekturalarda navbat provayderlari interfeys orqali ajratiladi.

## Ishlash natijasi:
```text
[KAFKA] 'orders.created' mavzusiga 17 bayt yuborildi
```

# 481-Topshiriq: Autentifikatsiya tekshiruvchisi interfeysi: Authenticator
## Topshiriq sharti:
API Token va Basic Auth tekshiruvlarini interfeys orqali amalga oshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Authenticator interface {
	Authenticate(token string) (string, bool)
}

type TokenAuth struct {
	validTokens map[string]string
}

func (t TokenAuth) Authenticate(token string) (string, bool) {
	user, ok := t.validTokens[token]
	return user, ok
}

func main() {
	auth := TokenAuth{validTokens: map[string]string{"sekret_123": "Ali"}}

	if user, ok := auth.Authenticate("sekret_123"); ok {
		fmt.Println("Muvaffaqiyatli avtorizatsiya, foydalanuvchi:", user)
	}
}
```

## Tushuntirish va Mantiq:
Xavfsizlik qatlamlari autentifikatsiya interfeyslari orqali modulli quriladi.

## Ishlash natijasi:
```text
Muvaffaqiyatli avtorizatsiya, foydalanuvchi: Ali
```

# 482-Topshiriq: Unit of Work (Tranzaksiya boshqaruvchisi) interfeysi
## Topshiriq sharti:
Baza tranzaksiyalarini boshqaruvchi interfeys.

## Yechim (Go kodi):
```go
package main

import "fmt"

type UnitOfWork interface {
	Commit() error
	Rollback() error
}

type FakeTx struct{}
func (FakeTx) Commit() error   { fmt.Println("[TX] Commit bajarildi"); return nil }
func (FakeTx) Rollback() error { fmt.Println("[TX] Rollback bajarildi"); return nil }

func main() {
	var uow UnitOfWork = FakeTx{}
	_ = uow.Commit()
}
```

## Tushuntirish va Mantiq:
Unit of Work bir nechta repozitoriylarning yagona atomik tranzaksiyada ishlashini ta'minlaydi.

## Ishlash natijasi:
```text
[TX] Commit bajarildi
```

# 483-Topshiriq: Metrikalar kollektori (Metrics Collector) interfeysi
## Topshiriq sharti:
Statistika va o'lchovlarni yig'uvchi interfeys.

## Yechim (Go kodi):
```go
package main

import "fmt"

type MetricsCollector interface {
	IncCounter(name string)
	SetGauge(name string, val float64)
}

type ConsoleMetrics struct{}
func (ConsoleMetrics) IncCounter(n string)        { fmt.Println("[METRIKA] Counter oshdi:", n) }
func (ConsoleMetrics) SetGauge(n string, v float64) { fmt.Printf("[METRIKA] Gauge %s = %.2f\n", n, v) }

func main() {
	var m MetricsCollector = ConsoleMetrics{}
	m.IncCounter("login_attempts")
	m.SetGauge("cpu_load", 45.2)
}
```

## Tushuntirish va Mantiq:
Monitoring infratuzilmasi interfeys orqali dasturdan to'liq ajratiladi.

## Ishlash natijasi:
```text
[METRIKA] Counter oshdi: login_attempts
[METRIKA] Gauge cpu_load = 45.20
```

# 484-Topshiriq: Rate Limiter interfeysi
## Topshiriq sharti:
So'rovlar chastotasini cheklovchi interfeys.

## Yechim (Go kodi):
```go
package main

import "fmt"

type RateLimiter interface {
	Allow(ip string) bool
}

type SimpleLimiter struct {
	maxRequests int
}

func (s SimpleLimiter) Allow(ip string) bool {
	return true // Simulyatsiya: har doim ruxsat berish
}

func main() {
	var rl RateLimiter = SimpleLimiter{maxRequests: 100}
	fmt.Println("So'rovga ruxsat bormi:", rl.Allow("192.168.1.1"))
}
```

## Tushuntirish va Mantiq:
DDoS himoyasi va API kvotalarini boshqarishda RateLimiter interfeysi qo'llaniladi.

## Ishlash natijasi:
```text
So'rovga ruxsat bormi: true
```

# 485-Topshiriq: Circuit Breaker interfeysi
## Topshiriq sharti:
Xizmat ishlamay qolganda kaskadli nosozliklarni to'xtatuvchi interfeys.

## Yechim (Go kodi):
```go
package main

import "fmt"

type CircuitBreaker interface {
	CanExecute() bool
	RecordSuccess()
	RecordFailure()
}

type MockCB struct{ Ochiqmi bool }
func (m MockCB) CanExecute() bool   { return !m.Ochiqmi }
func (m MockCB) RecordSuccess()     {}
func (m MockCB) RecordFailure()     {}

func main() {
	var cb CircuitBreaker = MockCB{Ochiqmi: false}
	fmt.Println("Tashqi servisga so'rov yuborish mumkinmi:", cb.CanExecute())
}
```

## Tushuntirish va Mantiq:
Mikroservislarda nosozliklarni izolyatsiya qilish uchun Circuit Breaker standarti qo'llaniladi.

## Ishlash natijasi:
```text
Tashqi servisga so'rov yuborish mumkinmi: true
```

# 486-Topshiriq: Health Checker interfeysi
## Topshiriq sharti:
Servis sog'lomligini tekshiruvchi umumiy shartnoma.

## Yechim (Go kodi):
```go
package main

import "fmt"

type HealthChecker interface {
	Name() string
	Check() error
}

type DBCheck struct{}
func (DBCheck) Name() string { return "PostgreSQL" }
func (DBCheck) Check() error { return nil }

func main() {
	checkers := []HealthChecker{DBCheck{}}

	for _, c := range checkers {
		if err := c.Check(); err == nil {
			fmt.Printf("[HEALTH] %s sog'lom va faol (OK)\n", c.Name())
		}
	}
}
```

## Tushuntirish va Mantiq:
Kubernetes liveness va readiness problari uchun HealthChecker interfeyslari ishlatiladi.

## Ishlash natijasi:
```text
[HEALTH] PostgreSQL sog'lom va faol (OK)
```

# 487-Topshiriq: Event Publisher va Subscriber interfeyslari
## Topshiriq sharti:
Hodisalarni chiqaruvchi va qabul qiluvchi interfeyslar juftligi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Event struct {
	Nomi string
}

type EventPublisher interface {
	Publish(e Event)
}

type EventSubscriber interface {
	Handle(e Event)
}

type LoggerSubscriber struct{}
func (LoggerSubscriber) Handle(e Event) { fmt.Println("Hodisa qayd etildi:", e.Nomi) }

func main() {
	var sub EventSubscriber = LoggerSubscriber{}
	sub.Handle(Event{Nomi: "UserLoggedIn"})
}
```

## Tushuntirish va Mantiq:
Hodisaga asoslangan tizimlarda publisher va subscriber alohida interfeyslar bilan belgilanadi.

## Ishlash natijasi:
```text
Hodisa qayd etildi: UserLoggedIn
```

# 488-Topshiriq: HTTP Middleware interfeysi
## Topshiriq sharti:
HTTP so'rovlarini filtrlovchi o'ram interfeysi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Middleware interface {
	Intercept(so'rov string) string
}

type AuthMiddleware struct{}
func (AuthMiddleware) Intercept(s string) string { return "[Auth Tekshirildi] -> " + s }

func main() {
	var mw Middleware = AuthMiddleware{}
	fmt.Println(mw.Intercept("GET /profil"))
}
```

## Tushuntirish va Mantiq:
Middleware zanjiri interfeyslar orqali moslashuvchan ulanadi.

## Ishlash natijasi:
```text
[Auth Tekshirildi] -> GET /profil
```

# 489-Topshiriq: Interfeys ustida Type Assertion orqali ixtiyoriy qobiliyatlarni tekshirish
## Topshiriq sharti:
Obyekt maxsus interfeysni (masalan `Flusher`) qo'llab-quvvatlashini assertion orqali aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type OddiyYozuvchi interface {
	WriteData(s string)
}

type FlushQobiliyati interface {
	Flush()
}

type MurakkabYozuvchi struct{}
func (MurakkabYozuvchi) WriteData(s string) { fmt.Println("Yozildi:", s) }
func (MurakkabYozuvchi) Flush()             { fmt.Println("Bufer tozalandi (Flush)") }

func Jarayon(w OddiyYozuvchi) {
	w.WriteData("Salom")

	// Agar obyekti Flush() ni ham bilsa:
	if f, ok := w.(FlushQobiliyati); ok {
		f.Flush()
	}
}

func main() {
	Jarayon(MurakkabYozuvchi{})
}
```

## Tushuntirish va Mantiq:
Go da `http.Flusher` va `http.Hijacker` aynan shu xil interfeys type assertion orqali ixtiyoriy qobiliyatlarni tekshiradi.

## Ishlash natijasi:
```text
Yozildi: Salom
Bufer tozalandi (Flush)
```

# 490-Topshiriq: Nil qiymat bilan ishlay oladigan interfeys implementatsiyasi
## Topshiriq sharti:
Interfeys ichidagi ko'rsatkich nil bo'lsa ham xavfsiz ishlovchi metod.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Hisoblagich interface {
	Hisob() int
}

type XavfsizRaqam struct {
	son int
}

func (x *XavfsizRaqam) Hisob() int {
	if x == nil {
		return 0
	}
	return x.son
}

func main() {
	var p *XavfsizRaqam = nil
	var h Hisoblagich = p

	fmt.Println("Hisob (nil ko'rsatkich bilan):", h.Hisob())
}
```

## Tushuntirish va Mantiq:
Nil ko'rsatkich interfeysga o'ralganda ham uning metodlari chaqirilishi va xavfsiz qiymat berishi mumkin.

## Ishlash natijasi:
```text
Hisob (nil ko'rsatkich bilan): 0
```

# 491-Topshiriq: Fayl tizimi abstraksiyasi (io/fs.FS interfeysi)
## Topshiriq sharti:
Go 1.16+ `fs.FS` interfeysini tushunish va xotiradagi fayl tizimi.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io/fs"
	"testing/fstest"
)

func main() {
	// Xotiradagi virtual fayl tizimi (fs.FS interfeysini qanoatlantiradi):
	virtualFS := fstest.MapFS{
		"config.json": {Data: []byte(`{"env": "prod"}`)},
	}

	data, err := fs.ReadFile(virtualFS, "config.json")
	if err != nil {
		fmt.Println("Xato:", err)
		return
	}

	fmt.Println("Virtual fayldan o'qildi:", string(data))
}
```

## Tushuntirish va Mantiq:
`io/fs.FS` Go da diskdagi fayllar, zip arxivlari va xotiradagi resurslarni bitta interfeys ostida birlashtiradi.

## Ishlash natijasi:
```text
Virtual fayldan o'qildi: {"env": "prod"}
```

# 492-Topshiriq: Interfeys orqali Plugin tizimi (Dinamik kengaytmalar)
## Topshiriq sharti:
Plaginlar interfeysi orqali yangi modullarni yuklash.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Plugin interface {
	Name() string
	Execute()
}

type AuditPlugin struct{}
func (AuditPlugin) Name() string { return "AuditPlagin" }
func (AuditPlugin) Execute()     { fmt.Println("[PLUGIN]: Audit amallari bajarildi.") }

func main() {
	plaginlar := []Plugin{AuditPlugin{}}

	for _, p := range plaginlar {
		fmt.Printf("Plagin yuklandi: %s\n", p.Name())
		p.Execute()
	}
}
```

## Tushuntirish va Mantiq:
Plagin tizimlari asosiy dasturni qayta kompilyatsiya qilmasdan kengaytirish imkonini beradi.

## Ishlash natijasi:
```text
Plagin yuklandi: AuditPlagin
[PLUGIN]: Audit amallari bajarildi.
```

# 493-Topshiriq: Comparator interfeysi orqali maxsus taqqoslash
## Topshiriq sharti:
Ikki obyektni solishtiruvchi interfeys.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Solishtiruvchi interface {
	CompareTo(boshqa any) int
}

type Mahsulot struct {
	Narx int
}

func (m Mahsulot) CompareTo(b any) int {
	other := b.(Mahsulot)
	if m.Narx < other.Narx {
		return -1
	} else if m.Narx > other.Narx {
		return 1
	}
	return 0
}

func main() {
	m1 := Mahsulot{Narx: 100}
	m2 := Mahsulot{Narx: 200}

	fmt.Println("m1 va m2 solishtiruvi:", m1.CompareTo(m2))
}
```

## Tushuntirish va Mantiq:
Comparator interfeysi tartiblash algoritmlarida elementlarni o'zaro solishtirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
m1 va m2 solishtiruvi: -1
```

# 494-Topshiriq: Interfeyslar kompozitsiyasida metod nomlari to'qnashuvi qoidasi
## Topshiriq sharti:
Ikki bir xil metodga ega interfeyslarni birlashtirganda Go ning xatti-harakati.

## Yechim (Go kodi):
```go
package main

import "fmt"

type A interface {
	Salom() string
}

type B interface {
	Salom() string
}

// Go 1.14 dan boshlab bir xil metod imzosi bo'lsa kompozitsiyaga ruxsat berilgan!
type AB interface {
	A
	B
}

type Amal struct{}
func (Amal) Salom() string { return "Birlashtirilgan salom!" }

func main() {
	var ab AB = Amal{}
	fmt.Println(ab.Salom())
}
```

## Tushuntirish va Mantiq:
Go 1.14 dan boshlab agar birlashtirilayotgan interfeyslardagi metodlarning imzolari bir xil bo'lsa, xatolik yuz bermaydi.

## Ishlash natijasi:
```text
Birlashtirilgan salom!
```

# 495-Topshiriq: Shifrlangan Token generatori interfeysi
## Topshiriq sharti:
JWT va OAuth tokenlari uchun umumiy generator interfeysi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type TokenGenerator interface {
	Generate(userID int) string
}

type FakeJWTGenerator struct{}
func (FakeJWTGenerator) Generate(uid int) string {
	return fmt.Sprintf("jwt.header.user_%d.signature", uid)
}

func main() {
	var tg TokenGenerator = FakeJWTGenerator{}
	token := tg.Generate(42)
	fmt.Println("Hosil qilingan token:", token)
}
```

## Tushuntirish va Mantiq:
Autentifikatsiya tokenlari ishlab chiqaruvchi interfeys.

## Ishlash natijasi:
```text
Hosil qilingan token: jwt.header.user_42.signature
```

# 496-Topshiriq: Xotira Keshi uchun Eviction Policy (Chiqarib tashlash qoidasi) interfeysi
## Topshiriq sharti:
Kesh to'lganda qaysi elementni o'chirishni belgilovchi qoida interfeysi.

## Yechim (Go kodi):
```go
package main

import "fmt"

type EvictionPolicy interface {
	Evict(keys []string) string
}

type FIFOEviction struct{}
func (FIFOEviction) Evict(keys []string) string { return keys[0] }

func main() {
	var ep EvictionPolicy = FIFOEviction{}
	eski := ep.Evict([]string{"kalit_1", "kalit_2"})
	fmt.Println("Chiqarib tashlanadigan kalit:", eski)
}
```

## Tushuntirish va Mantiq:
Kesh siyosatlari (LRU, LFU, FIFO) interfeyslar orqali ajratiladi.

## Ishlash natijasi:
```text
Chiqarib tashlanadigan kalit: kalit_1
```

# 497-Topshiriq: Validator Chain interfeysi
## Topshiriq sharti:
Ketma-ket validatorlar zanjirini interfeys orqali ishga tushiring.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

type StepValidator interface {
	ValidateStep(input string) error
}

type NonEmptyStep struct{}
func (NonEmptyStep) ValidateStep(s string) error {
	if s == "" {
		return errors.New("matn bo'sh")
	}
	return nil
}

func main() {
	steps := []StepValidator{NonEmptyStep{}}

	for _, step := range steps {
		if err := step.ValidateStep("Go"); err == nil {
			fmt.Println("Bosqich validatsiyadan muvaffaqiyatli o'tdi.")
		}
	}
}
```

## Tushuntirish va Mantiq:
Zanjirli tekshiruvlar interfeyslar orqali oson tashkil qilinadi.

## Ishlash natijasi:
```text
Bosqich validatsiyadan muvaffaqiyatli o'tdi.
```

# 498-Topshiriq: Dynamic Dispatch da interfeys ko'rsatkichi (*Interface) ishlatilmaslik qoidasi
## Topshiriq sharti:
Nima uchun `*Interface` deyarli hech qachon ishlatilmasligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Runner interface {
	Run()
}

type MyRunner struct{}
func (MyRunner) Run() { fmt.Println("Yugurmoqda...") }

func Start(r Runner) { // TO'G'RI: Runner o'zi pointer saqlay oladi
	r.Run()
}

func main() {
	// DIQQAT: *Runner yozish xato va keraksiz, chunki Runner ning o'zi interfeys!
	var r Runner = MyRunner{}
	Start(r)
}
```

## Tushuntirish va Mantiq:
Interfeysning o'zi xotirada ko'rsatkichlar juftligidan iborat, shuning uchun `*Runner` deb ko'rsatkichga ko'rsatkich olish mutlaqo noto'g'ri hisoblanadi.

## Ishlash natijasi:
```text
Yugurmoqda...
```

# 499-Topshiriq: Interfeys orqali qayta urinish (Retryable) qobiliyati
## Topshiriq sharti:
Amal xatolik berganda qayta urinish mumkinligini bildiruvchi interfeys.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Retryable interface {
	CanRetry() bool
}

type TarmoqXatosi struct {
	Urinishlar int
}

func (t TarmoqXatosi) Error() string { return "tarmoq uzildi" }
func (t TarmoqXatosi) CanRetry() bool { return t.Urinishlar < 3 }

func main() {
	var err error = TarmoqXatosi{Urinishlar: 1}

	if r, ok := err.(Retryable); ok && r.CanRetry() {
		fmt.Println("Xatolik vaqtincha, qayta urinish mumkin!")
	}
}
```

## Tushuntirish va Mantiq:
Xatoliklarni maxsus interfeyslar orqali tekshirish Go da xatolarni tasniflashning eng qulay usulidir.

## Ishlash natijasi:
```text
Xatolik vaqtincha, qayta urinish mumkin!
```

# 500-Topshiriq: Yakuniy amaliy vazifa: To'liq Clean Architecture va Dependency Injection
## Topshiriq sharti:
Domain Entity, Repository interfeysi, Servis qatlami va Mock repozitoriy bilan to'liq toza arxitektura yarating.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

// 1. Domain Entity
type Foydalanuvchi struct {
	ID    int
	Ism   string
	Balans float64
}

// 2. Repository Interface
type FoydalanuvchiRepository interface {
	GetByID(id int) (*Foydalanuvchi, error)
	Update(u *Foydalanuvchi) error
}

// 3. Service Layer (Faqat interfeysga bog'langan!)
type TolovXizmati struct {
	repo FoydalanuvchiRepository
}

func NewTolovXizmati(r FoydalanuvchiRepository) *TolovXizmati {
	return &TolovXizmati{repo: r}
}

func (s *TolovXizmati) To'lovQil(userID int, summa float64) error {
	user, err := s.repo.GetByID(userID)
	if err != nil {
		return err
	}
	if user.Balans < summa {
		return errors.New("balans yetarli emas")
	}
	user.Balans -= summa
	return s.repo.Update(user)
}

// 4. Mock Repository (Test uchun xotiradagi baza)
type InMemoryRepo struct {
	users map[int]*Foydalanuvchi
}

func (m *InMemoryRepo) GetByID(id int) (*Foydalanuvchi, error) {
	u, ok := m.users[id]
	if !ok {
		return nil, errors.New("foydalanuvchi topilmadi")
	}
	return u, nil
}

func (m *InMemoryRepo) Update(u *Foydalanuvchi) error {
	m.users[u.ID] = u
	return nil
}

func main() {
	mockDB := &InMemoryRepo{
		users: map[int]*Foydalanuvchi{
			1: {ID: 1, Ism: "Nodirbek", Balans: 100000},
		},
	}

	xizmat := NewTolovXizmati(mockDB)
	err := xizmat.To'lovQil(1, 40000)

	if err != nil {
		fmt.Println("To'lov xatosi:", err)
	} else {
		user, _ := mockDB.GetByID(1)
		fmt.Printf("To'lov muvaffaqiyatli! Yangi balans: %.0f so'm\n", user.Balans)
	}
}
```

## Tushuntirish va Mantiq:
Ushbu topshiriq Go tilida interfeyslar, Dependency Injection va Clean Architecture qanday mukammal uyg'unlashishini amalda to'liq isbotlaydi.

## Ishlash natijasi:
```text
To'lov muvaffaqiyatli! Yangi balans: 60000 so'm
```

