# 1-Mavzu: Go Asoslari, Ma'lumot Turlari va O'zgaruvchilar (1-50)

Go (Golang) dasturlash tilining poydevori: `package main`, `import`, `func main()`, o'zgaruvchilar e'lon qilish (`var`, `:=`), o'zgarmaslar (`const`, `iota`), barcha asosiy ma'lumot turlari (`int`, `float`, `string`, `bool`, `rune`, `byte`, `complex`), nol qiymatlar (zero values), turlarni xavfsiz konvertatsiya qilish (`strconv`), formatlangan chiqarish (`fmt.Printf`) va o'zgaruvchilar skopi bo'yicha 50 ta amaliy topshiriq.

# 1-Topshiriq: Go tilida 'Salom, Dunyo!' va asosiy dastur strukturasi
## Topshiriq sharti:
`package main` va `main()` funksiyasidan foydalanib konsolga 'Salom, Go dasturchilari!' matnini chiqaruvchi to'liq Go dasturini yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	fmt.Println("Salom, Go dasturchilari!")
}
```

## Tushuntirish va Mantiq:
Go tilida har bir bajariluvchi dastur `package main` bilan boshlanishi va kirish nuqtasi sifatida `func main()` funksiyasiga ega bo'lishi shart. `fmt.Println` satr oxiriga avtomatik yangi qator (`\n`) qo'shadi.

## Ishlash natijasi:
```text
Salom, Go dasturchilari!
```

# 2-Topshiriq: var kalit so'zi bilan aniq tiplangan o'zgaruvchilarni e'lon qilish
## Topshiriq sharti:
`var` kalit so'zi yordamida `nom` (string), `yosh` (int) va `talabami` (bool) o'zgaruvchilarini e'lon qiling, ularga qiymat bering va konsolga chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var nom string = "Alisher Navoiy"
	var yosh int = 35
	var talabami bool = false

	fmt.Println("Ism:", nom)
	fmt.Println("Yosh:", yosh)
	fmt.Println("Talabami:", talabami)
}
```

## Tushuntirish va Mantiq:
Go statik tiplangan til. `var nom tur = qiymat` sintaksisi o'zgaruvchini uning aniq ma'lumot turi bilan e'lon qiladi.

## Ishlash natijasi:
```text
Ism: Alisher Navoiy
Yosh: 35
Talabami: false
```

# 3-Topshiriq: Qisqa e'lon qilish operatori `:=` (Short Variable Declaration)
## Topshiriq sharti:
`:=` operatori orqali shahar nomi, harorat va aholi sonini ifodalovchi o'zgaruvchilarni e'lon qiling va ularning tiplarini kompilyator o'zi aniqlashini ta'minlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	shahar := "Toshkent"
	harorat := 24.5
	aholi := 3000000

	fmt.Printf("Shahar: %s, Harorat: %.1f°C, Aholi: %d\n", shahar, harorat, aholi)
}
```

## Tushuntirish va Mantiq:
`:=` operatori faqat funksiya tanasi ichida ishlaydi. U o'zgaruvchini e'lon qilish va unga dastlabki qiymat berishni birlashtiradi; Go kompilyatori qiymatiga qarab o'zgaruvchi turini (type inference) o'zi aniqlaydi.

## Ishlash natijasi:
```text
Shahar: Toshkent, Harorat: 24.5°C, Aholi: 3000000
```

# 4-Topshiriq: Butun son turlari: int8, int16, int32, int64
## Topshiriq sharti:
Turli sig'imdagi butun son turlari (`int8`, `int16`, `int32`, `int64`) orqali sonlarni e'lon qiling va ularning xotiradagi bayt hajmini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unsafe"
)

func main() {
	var a int8 = 127
	var b int16 = 32767
	var c int32 = 2147483647
	var d int64 = 9223372036854775807

	fmt.Printf("int8: %d (hajmi: %d bayt)\n", a, unsafe.Sizeof(a))
	fmt.Printf("int16: %d (hajmi: %d bayt)\n", b, unsafe.Sizeof(b))
	fmt.Printf("int32: %d (hajmi: %d bayt)\n", c, unsafe.Sizeof(c))
	fmt.Printf("int64: %d (hajmi: %d bayt)\n", d, unsafe.Sizeof(d))
}
```

## Tushuntirish va Mantiq:
Go tilida son turlari aniq bit o'lchamlariga ega. `unsafe.Sizeof` funksiyasi o'zgaruvchining xotirada necha bayt egallashini qaytaradi (1, 2, 4 va 8 bayt).

## Ishlash natijasi:
```text
int8: 127 (hajmi: 1 bayt)
int16: 32767 (hajmi: 2 bayt)
int32: 2147483647 (hajmi: 4 bayt)
int64: 9223372036854775807 (hajmi: 8 bayt)
```

# 5-Topshiriq: Ishorasiz butun sonlar (unsigned): uint8, uint16, uint32, uint64
## Topshiriq sharti:
Ishorasiz butun son turlarini e'lon qiling va manfiy bo'lmagan qiymatlarni ifodalashda ularning chegaralarini tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var bayt uint8 = 255
	var port uint16 = 8080
	var id uint32 = 4000000000
	var counter uint64 = 18446744073709551615

	fmt.Println("uint8 max:", bayt)
	fmt.Println("Server porti:", port)
	fmt.Println("Foydalanuvchi ID:", id)
	fmt.Println("Katta hisoblagich:", counter)
}
```

## Tushuntirish va Mantiq:
`uint` turlari faqat musbat sonlar va nolni saqlaydi. Masalan, `uint8` 0 dan 255 gacha oraliqni qamrab oladi va tarmoq baytlarida keng ishlatiladi.

## Ishlash natijasi:
```text
uint8 max: 255
Server porti: 8080
Foydalanuvchi ID: 4000000000
Katta hisoblagich: 18446744073709551615
```

# 6-Topshiriq: Haqiqiy sonlar: float32 va float64 aniqligi
## Topshiriq sharti:
`float32` va `float64` turlarida pi sonini saqlang va ularning kasr aniqligidagi farqini namoyish qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var pi32 float32 = 3.14159265358979323846
	var pi64 float64 = 3.14159265358979323846

	fmt.Printf("float32: %.10f\n", pi32)
	fmt.Printf("float64: %.16f\n", pi64)
}
```

## Tushuntirish va Mantiq:
Go tilida `float32` 24 bit mantissaga ega (taxminan 7 ta o'nlik belgi aniqligi), `float64` esa 53 bit mantissaga ega (taxminan 15-17 ta o'nlik belgi aniqligi). Odatda ilmiy va muhandislik hisoblashlarida `float64` standart hisoblanadi.

## Ishlash natijasi:
```text
float32: 3.1415927410
float64: 3.1415926535897931
```

# 7-Topshiriq: Mantiqiy tur (bool) va mantiqiy amallar
## Topshiriq sharti:
Foydalanuvchining login qilganligi va admin huquqi borligini tekshiruvchi mantiqiy ifodalarni yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	isLoggedIn := true
	isAdmin := false

	canAccessAdminPanel := isLoggedIn && isAdmin
	canViewDashboard := isLoggedIn || isAdmin
	isGuest := !isLoggedIn

	fmt.Println("Admin panelga kira oladimi:", canAccessAdminPanel)
	fmt.Println("Dashboardni ko'ra oladimi:", canViewDashboard)
	fmt.Println("Mehmonmi:", isGuest)
}
```

## Tushuntirish va Mantiq:
`bool` turi faqat `true` yoki `false` qiymatlarini oladi. Mantiqiy operatorlar: `&&` (VA), `||` (YOKI), `!` (INKOR).

## Ishlash natijasi:
```text
Admin panelga kira oladimi: false
Dashboardni ko'ra oladimi: true
Mehmonmi: false
```

# 8-Topshiriq: String tipi va UTF-8 satr uzunligi
## Topshiriq sharti:
O'zbek tilidagi kirill va lotin yozuvidagi satrning baytlar soni va haqiqiy harflar (runes) sonini aniqlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unicode/utf8"
)

func main() {
	matn := "O'zbekiston"
	kirillMatn := "Ўзбекистон"

	fmt.Println("Matn:", matn)
	fmt.Printf("Bayt uzunligi: %d, Belgilar soni: %d\n", len(matn), utf8.RuneCountInString(matn))

	fmt.Println("Kirill matn:", kirillMatn)
	fmt.Printf("Bayt uzunligi: %d, Belgilar soni: %d\n", len(kirillMatn), utf8.RuneCountInString(kirillMatn))
}
```

## Tushuntirish va Mantiq:
Go da `len(str)` satrning xotiradagi baytlar sonini qaytaradi. UTF-8 da kirill harflari 2 bayt joy oladi. Haqiqiy belgilar (Unicode codepoints) sonini hisoblash uchun `utf8.RuneCountInString` ishlatiladi.

## Ishlash natijasi:
```text
Matn: O'zbekiston
Bayt uzunligi: 11, Belgilar soni: 11
Kirill matn: Ўзбекистон
Bayt uzunligi: 20, Belgilar soni: 10
```

# 9-Topshiriq: Rune tipi va Unicode belgilar codepoint qiymatlari
## Topshiriq sharti:
`rune` turidagi o'zgaruvchilarni e'lon qiling, ularning int32 sifatidagi son qiymati va harf ko'rinishini chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var belgi rune = 'O'
	var belgiQ rune = 'q'
	var belgiEmoji rune = '🚀'

	fmt.Printf("Belgi: %c, Unicode kodi: %U, O'nlik qiymati: %d\n", belgi, belgi, belgi)
	fmt.Printf("Belgi: %c, Unicode kodi: %U, O'nlik qiymati: %d\n", belgiQ, belgiQ, belgiQ)
	fmt.Printf("Belgi: %c, Unicode kodi: %U, O'nlik qiymati: %d\n", belgiEmoji, belgiEmoji, belgiEmoji)
}
```

## Tushuntirish va Mantiq:
Go tilida `rune` turi `int32` ning taxallusi (alias) bo'lib, alohida Unicode belgisini ifodalaydi. Yagona tirnoq `''` ichida yoziladi.

## Ishlash natijasi:
```text
Belgi: O, Unicode kodi: U+004F, O'nlik qiymati: 79
Belgi: q, Unicode kodi: U+0071, O'nlik qiymati: 113
Belgi: 🚀, Unicode kodi: U+1F680, O'nlik qiymati: 128640
```

# 10-Topshiriq: Byte tipi va ASCII belgilar bilan ishlash
## Topshiriq sharti:
`byte` turidagi o'zgaruvchi e'lon qiling va uning sonli hamda ASCII belgili qiymatini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var b byte = 'A'

	fmt.Printf("Bayt son qiymati: %d\n", b)
	fmt.Printf("ASCII belgisi: %c\n", b)
	fmt.Printf("Keyingi belgi: %c (kod: %d)\n", b+1, b+1)
}
```

## Tushuntirish va Mantiq:
`byte` turi `uint8` ning taxallusi bo'lib, 0 dan 255 gacha qiymat oladi va ASCII belgilar yoki binar ma'lumotlar bilan ishlash uchun xizmat qiladi.

## Ishlash natijasi:
```text
Bayt son qiymati: 65
ASCII belgisi: A
Keyingi belgi: B (kod: 66)
```

# 11-Topshiriq: Kompleks sonlar: complex64 va complex128
## Topshiriq sharti:
`complex128` turidagi ikkita kompleks sonni yarating, ularni qo'shing va ko'paytiring hamda haqiqiy va mavhum qismlarini ajrating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	c1 := complex(3.0, 4.0)   // 3 + 4i
	c2 := complex(1.0, -2.0)  // 1 - 2i

	yigindi := c1 + c2
	kopaytma := c1 * c2

	fmt.Println("c1:", c1)
	fmt.Println("c2:", c2)
	fmt.Println("Yig'indi:", yigindi)
	fmt.Println("Ko'paytma:", kopaytma)
	fmt.Printf("c1 ning haqiqiy qismi: %.1f, mavhum qismi: %.1f\n", real(c1), imag(c1))
}
```

## Tushuntirish va Mantiq:
Go tilida kompleks sonlar o'rnatilgan (built-in) tur hisoblanadi. `complex(r, i)` funksiyasi orqali yasaladi, `real()` va `imag()` funksiyalari orqali qismlari olinadi.

## Ishlash natijasi:
```text
c1: (3+4i)
c2: (1-2i)
Yig'indi: (4+2i)
Ko'paytma: (11-2i)
c1 ning haqiqiy qismi: 3.0, mavhum qismi: 4.0
```

# 12-Topshiriq: Nol qiymatlar (Zero Values) tushunchasi
## Topshiriq sharti:
Boshlang'ich qiymat berilmagan turli tiplardagi o'zgaruvchilarni e'lon qiling va Go ularga qanday 'nol qiymat' berishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var i int
	var f float64
	var b bool
	var s string
	var p *int

	fmt.Printf("int nol qiymati: %d\n", i)
	fmt.Printf("float64 nol qiymati: %f\n", f)
	fmt.Printf("bool nol qiymati: %t\n", b)
	fmt.Printf("string nol qiymati: %q\n", s)
	fmt.Printf("ko'rsatkich nol qiymati: %v\n", p)
}
```

## Tushuntirish va Mantiq:
Go tilida e'lon qilingan o'zgaruvchi xotirada 'axlat' saqlamaydi. Barcha turlar avtomatik o'zining xavfsiz nol qiymatiga (`0`, `0.0`, `false`, `""`, `nil`) ega bo'ladi.

## Ishlash natijasi:
```text
int nol qiymati: 0
float64 nol qiymati: 0.000000
bool nol qiymati: false
string nol qiymati: ""
ko'rsatkich nol qiymati: <nil>
```

# 13-Topshiriq: const kalit so'zi bilan o'zgarmaslar yaratish
## Topshiriq sharti:
`const` yordamida o'zgarmas qiymatlarni (ilovaning nomi, port raqami, soliq stavkasi) e'lon qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	const IlovaNomi = "FastPay API"
	const Port = 8080
	const SoliqStavkasi = 0.12

	summa := 100000.0
	soliq := summa * SoliqStavkasi

	fmt.Printf("Ilova: %s (Port: %d)\n", IlovaNomi, Port)
	fmt.Printf("Boshlang'ich summa: %.2f so'm, Soliq (12%%): %.2f so'm\n", summa, soliq)
}
```

## Tushuntirish va Mantiq:
`const` bilan e'lon qilingan qiymatlar kompilyatsiya vaqtida hisoblanadi va dastur ishlashi davomida o'zgartirilishi mumkin emas.

## Ishlash natijasi:
```text
Ilova: FastPay API (Port: 8080)
Boshlang'ich summa: 100000.00 so'm, Soliq (12%): 12000.00 so'm
```

# 14-Topshiriq: iota identifikatori bilan sanab o'tishlar (Enum) yaratish
## Topshiriq sharti:
`iota` yordamida haftaning kunlarini ifodalovchi o'zgarmaslar to'plamini (enum) yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

const (
	Dushanba = iota + 1
	Seshanba
	Chorshanba
	Payshanba
	Juma
	Shanba
	Yakshanba
)

func main() {
	fmt.Printf("Dushanba: %d-kun\n", Dushanba)
	fmt.Printf("Juma: %d-kun\n", Juma)
	fmt.Printf("Yakshanba: %d-kun\n", Yakshanba)
}
```

## Tushuntirish va Mantiq:
`iota` Go da ketma-ket butun sonlarni avtomatik hisoblovchi konstanta generatori hisoblanadi. Har bir yangi qatorda u 1 taga oshadi.

## Ishlash natijasi:
```text
Dushanba: 1-kun
Juma: 5-kun
Yakshanba: 7-kun
```

# 15-Topshiriq: iota va bit siljishi (Bit Shift) bilan xotira birliklarini hisoblash
## Topshiriq sharti:
`iota` va `<<` (chapga bit siljitish) yordamida KB, MB, GB, TB o'lchamlarini ifodalang.

## Yechim (Go kodi):
```go
package main

import "fmt"

const (
	_  = iota             // 0 ni o'tkazib yuboramiz
	KB = 1 << (10 * iota) // 1 << 10 = 1024
	MB = 1 << (10 * iota) // 1 << 20 = 1048576
	GB = 1 << (10 * iota) // 1 << 30
	TB = 1 << (10 * iota) // 1 << 40
)

func main() {
	fmt.Printf("1 KB = %d bayt\n", KB)
	fmt.Printf("1 MB = %d bayt\n", MB)
	fmt.Printf("1 GB = %d bayt\n", GB)
	fmt.Printf("1 TB = %d bayt\n", TB)
}
```

## Tushuntirish va Mantiq:
`1 << (10 * iota)` ifodasi har bir qadamda ikkining 10-darajasiga oshirib, bayt o'lchamlarini juda aniq va ixcham hosil qiladi.

## Ishlash natijasi:
```text
1 KB = 1024 bayt
1 MB = 1048576 bayt
1 GB = 1073741824 bayt
1 TB = 1099511627776 bayt
```

# 16-Topshiriq: Asosiy son tiplari o'rtasida konvertatsiya (Type Conversion)
## Topshiriq sharti:
`int` va `float64` turlarini bir-biriga o'zgartiring hamda butun sonli bo'lishdagi kasr qism yo'qolishini tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var a int = 15
	var b int = 4

	// Noto'g'ri (kasr qism yo'qoladi):
	butunNatija := a / b

	// To'g'ri haqiqiy bo'lish:
	haqiqiyNatija := float64(a) / float64(b)

	fmt.Printf("Butun bo'lish (int): %d\n", butunNatija)
	fmt.Printf("Haqiqiy bo'lish (float64): %.2f\n", haqiqiyNatija)
}
```

## Tushuntirish va Mantiq:
Go tilida yashirin (implicit) tip konvertatsiyasi yo'q. Bir xil toifadagi operatsiyani bajarish uchun har doim `float64(a)` kabi aniq ko'rsatish shart.

## Ishlash natijasi:
```text
Butun bo'lish (int): 3
Haqiqiy bo'lish (float64): 3.75
```

# 17-Topshiriq: strconv.Itoa va strconv.Atoi yordamida satr va son konvertatsiyasi
## Topshiriq sharti:
`strconv` paketidan foydalanib, butun sonni satrga aylantiring va satrni butun songa o'giring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	// Son -> Satr
	son := 2026
	satr := strconv.Itoa(son)
	fmt.Printf("Satr ko'rinishida: %q (turi: %T)\n", satr, satr)

	// Satr -> Son
	matn := "5000"
	narx, err := strconv.Atoi(matn)
	if err != nil {
		fmt.Println("Xatolik:", err)
		return
	}
	jami := narx + 1500
	fmt.Printf("Hisoblangan jami narx: %d so'm (turi: %T)\n", jami, jami)
}
```

## Tushuntirish va Mantiq:
`strconv.Itoa` (Integer to ASCII) sonni satrga o'giradi. `strconv.Atoi` (ASCII to Integer) satrni songa aylantiradi va muvaffaqiyatsiz bo'lsa xatolik (`error`) qaytaradi.

## Ishlash natijasi:
```text
Satr ko'rinishida: "2026" (turi: string)
Hisoblangan jami narx: 6500 so'm (turi: int)
```

# 18-Topshiriq: strconv.ParseFloat va strconv.FormatFloat bilan kasr sonlar konvertatsiyasi
## Topshiriq sharti:
Matn ko'rinishidagi kasr sonni `float64` ga o'giring va natijani yana aniq formatda satrga aylantiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	kursSatr := "12850.75"
	kurs, err := strconv.ParseFloat(kursSatr, 64)
	if err != nil {
		fmt.Println("Konvertatsiya xatosi:", err)
		return
	}

	dollar := 100.0
	summa := dollar * kurs
	fmt.Printf("100 dollar = %.2f so'm\n", summa)

	summaSatr := strconv.FormatFloat(summa, 'f', 2, 64)
	fmt.Println("Formatlangan summa satri:", summaSatr)
}
```

## Tushuntirish va Mantiq:
`strconv.ParseFloat(s, 64)` satrni 64-bitli suzuvchi nuqtali songa o'giradi. `FormatFloat` esa uni aniq o'nlik xonalar soni bilan satrga aylantiradi.

## Ishlash natijasi:
```text
100 dollar = 1285075.00 so'm
Formatlangan summa satri: 1285075.00
```

# 19-Topshiriq: strconv.ParseBool bilan mantiqiy qiymatlarni tahlil qilish
## Topshiriq sharti:
Turli matnli mantiqiy qiymatlarni (`true`, `1`, `false`, `0`) `bool` ga aylantiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	qiymatlar := []string{"true", "1", "false", "0", "TRUE"}

	for _, q := range qiymatlar {
		b, err := strconv.ParseBool(q)
		if err != nil {
			fmt.Printf("Xatolik: %s\n", err)
		} else {
			fmt.Printf("Matn: %-6q -> Bool: %t\n", q, b)
		}
	}
}
```

## Tushuntirish va Mantiq:
`strconv.ParseBool` 1, t, T, TRUE, true, True hamda 0, f, F, FALSE, false, False kabi barcha standart qiymatlarni tushunadi.

## Ishlash natijasi:
```text
Matn: "true"  -> Bool: true
Matn: "1"     -> Bool: true
Matn: "false" -> Bool: false
Matn: "0"     -> Bool: false
Matn: "TRUE"  -> Bool: true
```

# 20-Topshiriq: fmt.Printf formatlash belgilari: %d, %s, %f, %.2f, %q
## Topshiriq sharti:
Formatlash belgilaridan foydalanib mahsulot hisob-kitob chekini chiroyli konsolga chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	mahsulot := "Laptop Asus"
	soni := 2
	narx := 850.50
	jami := float64(soni) * narx

	fmt.Printf("Mahsulot: %-15s | Soni: %2d | Narxi: $%7.2f | Jami: $%8.2f\n", mahsulot, soni, narx, jami)
	fmt.Printf("Kotirovka qilingan nom: %q\n", mahsulot)
}
```

## Tushuntirish va Mantiq:
`%-15s` satrni chap tomonga tekislaydi, `%7.2f` jami 7 ta belgi joy ajratib 2 ta kasr qismini ko'rsatadi, `%q` esa qo'shtirnoq ichiga oladi.

## Ishlash natijasi:
```text
Mahsulot: Laptop Asus     | Soni:  2 | Narxi: $ 850.50 | Jami: $ 1701.00
Kotirovka qilingan nom: "Laptop Asus"
```

# 21-Topshiriq: Maxsus fmt belgilari: %v, %+v, %#v, %T
## Topshiriq sharti:
`%v`, `%+v`, `%#v` va `%T` larning farqini struktura va oddiy o'zgaruvchilarda ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Kitob struct {
	Nomi   string
	Muallif string
	Narxi  int
}

func main() {
	k := Kitob{Nomi: "O'tkan kunlar", Muallif: "Abdulla Qodiriy", Narxi: 45000}

	fmt.Printf("%%v  bilan: %v\n", k)
	fmt.Printf("%%+v bilan: %+v\n", k)
	fmt.Printf("%%#v bilan: %#v\n", k)
	fmt.Printf("%%T  bilan: %T\n", k)
}
```

## Tushuntirish va Mantiq:
`%v` qiymatni standart ko'rinishda chiqaradi, `%+v` struktura maydon nomlarini ham ko'rsatadi, `%#v` Go sintaksisi ko'rinishida chiqaradi, `%T` esa o'zgaruvchining to'liq tipini qaytaradi.

## Ishlash natijasi:
```text
%v  bilan: {O'tkan kunlar Abdulla Qodiriy 45000}
%+v bilan: {Nomi:O'tkan kunlar Muallif:Abdulla Qodiriy Narxi:45000}
%#v bilan: main.Kitob{Nomi:"O'tkan kunlar", Muallif:"Abdulla Qodiriy", Narxi:45000}
%T  bilan: main.Kitob
```

# 22-Topshiriq: Blank identifikator `_` (Blank Identifier)
## Topshiriq sharti:
Funksiyadan qaytgan ikkita qiymatdan faqat bittasini qabul qilishda `_` belgisidan foydalaning.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	// strconv.Atoi ikkita qiymat qaytaradi: (son int, err error)
	// Bizga faqat son kerak bo'lsa (yoki aksincha):
	son, _ := strconv.Atoi("12345")

	fmt.Println("Qabul qilingan son:", son)
}
```

## Tushuntirish va Mantiq:
Go da e'lon qilingan har bir o'zgaruvchi ishlatilishi shart, aks holda kompilyator xatolik beradi. Agar qiymat kerak bo'lmasa, uni tashlab yuborish uchun `_` (blank identifier) ishlatiladi.

## Ishlash natijasi:
```text
Qabul qilingan son: 12345
```

# 23-Topshiriq: Ko'p o'zgaruvchilarni bir vaqtda e'lon qilish va qiymat berish
## Topshiriq sharti:
Bitta qatorda bir nechta turli xil o'zgaruvchilarni e'lon qiling va ularga mos qiymatlarni bering.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ism, yosh, faol := "Rustam", 28, true

	var (
		server = "127.0.0.1"
		port   = 8000
		debug  = false
	)

	fmt.Printf("Foydalanuvchi: %s, Yosh: %d, Faol: %t\n", ism, yosh, faol)
	fmt.Printf("Server konfiguratsiyasi: %s:%d (debug: %t)\n", server, port, debug)
}
```

## Tushuntirish va Mantiq:
Go tilida `a, b, c := 1, 2, 3` tarzida bir qatorda bir nechta o'zgaruvchi e'lon qilish yoki `var (...)` blokli e'lon qilish mumkin.

## Ishlash natijasi:
```text
Foydalanuvchi: Rustam, Yosh: 28, Faol: true
Server konfiguratsiyasi: 127.0.0.1:8000 (debug: false)
```

# 24-Topshiriq: O'zgaruvchilar qiymatini almashtirish (Swap: a, b = b, a)
## Topshiriq sharti:
Qo'shimcha vaqtinchalik o'zgaruvchisiz ikkita o'zgaruvchining qiymatini o'zaro almashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	a := 100
	b := 500

	fmt.Printf("Almashishdan oldin: a = %d, b = %d\n", a, b)

	a, b = b, a

	fmt.Printf("Almashishdan keyin: a = %d, b = %d\n", a, b)
}
```

## Tushuntirish va Mantiq:
Go parallel qiymat berishni qo'llab-quvvatlaydi: ifodaning o'ng tomoni to'liq hisoblangach, chap tomonidagi o'zgaruvchilarga birdaniga o'zlashtiriladi.

## Ishlash natijasi:
```text
Almashishdan oldin: a = 100, b = 500
Almashishdan keyin: a = 500, b = 100
```

# 25-Topshiriq: Type Definition orqali maxsus tip yaratish va xavfsizlik
## Topshiriq sharti:
`type FoydalanuvchiID int64` ko'rinishida maxsus tip e'lon qiling va uning oddiy `int64` bilan adashib ketmasligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type FoydalanuvchiID int64
type BuyurtmaID int64

func main() {
	var uid FoydalanuvchiID = 1001
	var oid BuyurtmaID = 9999

	fmt.Printf("User ID: %d (turi: %T)\n", uid, uid)
	fmt.Printf("Order ID: %d (turi: %T)\n", oid, oid)

	// uid = oid // XATO! Kompilyator turlar mos kelmasligini bildiradi
	uid = FoydalanuvchiID(oid) // Faqat aniq konvertatsiya orqali mumkin
	fmt.Printf("O'zgartirilgandan keyin User ID: %d\n", uid)
}
```

## Tushuntirish va Mantiq:
`type YangiTip AsosiyTip` yangi alohida tip yaratadi. Bu qat'iy tip xavfsizligini ta'minlaydi (Domain-Driven Design), turli maqsaddagi identifikatorlarning chalkashib ketishini oldini oladi.

## Ishlash natijasi:
```text
User ID: 1001 (turi: main.FoydalanuvchiID)
Order ID: 9999 (turi: main.BuyurtmaID)
O'zgartirilgandan keyin User ID: 9999
```

# 26-Topshiriq: Type Alias (`type Taxallus = Asosiy`) va Yangi Tip o'rtasidagi farq
## Topshiriq sharti:
Type alias (`=`) yordamida `Harf = rune` yarating va uning haqiqiy `rune` bilan to'liq bir xilligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Harf = rune       // Type alias
type YangiHarf rune   // Yangi alohida tip

func main() {
	var r rune = 'Z'
	var h Harf = r        // Konvertatsiyasiz to'g'ridan-to'g'ri o'zlashadi
	var yh YangiHarf = YangiHarf(r) // Faqat konvertatsiya bilan!

	fmt.Printf("Harf: %c, YangiHarf: %c\n", h, yh)
}
```

## Tushuntirish va Mantiq:
Type alias (`type A = B`) mavjud turga shunchaki boshqa nom beradi (masalan, `byte = uint8` yoki `rune = int32`). Ular bir-biriga hech qanday konvertatsiyasiz teng keladi.

## Ishlash natijasi:
```text
Harf: Z, YangiHarf: Z
```

# 27-Topshiriq: Variable Shadowing (O'zgaruvchilarni soyalash) xavfi va uning oldini olish
## Topshiriq sharti:
Tashqi blokdagi o'zgaruvchi ichki blokda `:=` orqali qayta e'lon qilinganda qanday holat yuz berishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	hisob := 1000
	fmt.Println("Boshlang'ich hisob:", hisob)

	if true {
		hisob := 2000 // DIQQAT: Tashqi `hisob` emas, yangi lokal o'zgaruvchi yaratildi!
		fmt.Println("Ichki blokda hisob:", hisob)
	}

	fmt.Println("Ichki blokdan keyingi hisob:", hisob) // 1000 bo'lib qolaveradi!
}
```

## Tushuntirish va Mantiq:
Ichki blokda `:=` ishlatilganda tashqi blokdagi o'zgaruvchi bilan bir xil nomda yangi o'zgaruvchi paydo bo'ladi (shadowing). Agar tashqi qiymatni yangilamoqchi bo'lsak, `:=` emas, `=` ishlatish kerak.

## Ishlash natijasi:
```text
Boshlang'ich hisob: 1000
Ichki blokda hisob: 2000
Ichki blokdan keyingi hisob: 1000
```

# 28-Topshiriq: Raw String Literals (Teskari tirnoq bilan ko'p qatorli matnlar)
## Topshiriq sharti:
Teskari tirnoq (``) yordamida JSON va SQL so'rovini qatorlarni buzmasdan va maxsus belgilarni ekranlashtirmasdan yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	jsonMatn := `{
		"ism": "Jasur",
		"kasb": "Go Backend Muhandisi",
		"tajriba_yil": 5
	}`

	sqlQuery := `
		SELECT id, ism, email
		FROM foydalanuvchilar
		WHERE faol = true
		ORDER BY id DESC;
	`

	fmt.Println("JSON:")
	fmt.Println(jsonMatn)
	fmt.Println("SQL:")
	fmt.Println(sqlQuery)
}
```

## Tushuntirish va Mantiq:
Go da teskari tirnoq (``) ichidagi matn qanday bo'lsa shundayligicha (raw string) qabul qilinadi. Unda yangi qatorlar, bo'shliqlar va `\` belgilari maxsus belgiga aylanmaydi.

## Ishlash natijasi:
```text
JSON:
{
		"ism": "Jasur",
		"kasb": "Go Backend Muhandisi",
		"tajriba_yil": 5
	}
SQL:

		SELECT id, ism, email
		FROM foydalanuvchilar
		WHERE faol = true
		ORDER BY id DESC;
```

# 29-Topshiriq: Satrlarni samarali birlashtirish: strings.Builder
## Topshiriq sharti:
Ko'p sonli satrlarni `+` operatori o'rniga `strings.Builder` orqali xotirani tejab birlashtiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	var builder strings.Builder

	builder.WriteString("Go ")
	builder.WriteString("dasturlash ")
	builder.WriteString("tili ")
	builder.WriteString("2026-yilning ")
	builder.WriteString("eng talabgir texnologiyasi!")

	natija := builder.String()
	fmt.Println("Birlashtirilgan matn:", natija)
	fmt.Println("Matn uzunligi:", builder.Len())
}
```

## Tushuntirish va Mantiq:
Go da satrlar o'zgarmas (immutable). `+` operatori har gal yangi xotira ajratadi. `strings.Builder` esa ichki bufer orqali ortiqcha nusxalashlarsiz o'ta tez birlashtiradi.

## Ishlash natijasi:
```text
Birlashtirilgan matn: Go dasturlash tili 2026-yilning eng talabgir texnologiyasi!
Matn uzunligi: 64
```

# 30-Topshiriq: math kutubxonasi: math.Sqrt, math.Pow, math.Abs
## Topshiriq sharti:
`math` paketining asosiy matematik funksiyalaridan foydalanib kvadrat ildiz, daraja va modul hisoblang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"math"
)

func main() {
	x := 16.0
	ildiz := math.Sqrt(x)
	daraja := math.Pow(2, 8)
	manfiy := -45.75
	modul := math.Abs(manfiy)

	fmt.Printf("sqrt(%.1f) = %.2f\n", x, ildiz)
	fmt.Printf("2^8 = %.0f\n", daraja)
	fmt.Printf("abs(%.2f) = %.2f\n", manfiy, modul)
}
```

## Tushuntirish va Mantiq:
`math` funksiyalari doimo `float64` turidagi argumentlarni qabul qiladi va `float64` natija qaytaradi.

## Ishlash natijasi:
```text
sqrt(16.0) = 4.00
2^8 = 256
abs(-45.75) = 45.75
```

# 31-Topshiriq: Haqiqiy sonlarni yaxlitlash: math.Round, math.Floor, math.Ceil
## Topshiriq sharti:
Kasr sonlarni yuqoriga (`Ceil`), pastga (`Floor`) va eng yaqin butun songa (`Round`) yaxlitlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"math"
)

func main() {
	narx1 := 12.30
	narx2 := 12.75

	fmt.Printf("Round(%.2f) = %.0f | Round(%.2f) = %.0f\n", narx1, math.Round(narx1), narx2, math.Round(narx2))
	fmt.Printf("Floor(%.2f) = %.0f | Floor(%.2f) = %.0f\n", narx1, math.Floor(narx1), narx2, math.Floor(narx2))
	fmt.Printf("Ceil(%.2f)  = %.0f | Ceil(%.2f)  = %.0f\n", narx1, math.Ceil(narx1), narx2, math.Ceil(narx2))
}
```

## Tushuntirish va Mantiq:
`Floor` har doim kichik tomonga, `Ceil` doimo katta tomonga, `Round` esa 0.5 dan boshlab katta butun songa qarab yaxlitlaydi.

## Ishlash natijasi:
```text
Round(12.30) = 12 | Round(12.75) = 13
Floor(12.30) = 12 | Floor(12.75) = 12
Ceil(12.30)  = 13 | Ceil(12.75)  = 13
```

# 32-Topshiriq: Tasodifiy sonlar generatsiyasi: math/rand
## Topshiriq sharti:
Berilgan oraliqda (1 dan 100 gacha) tasodifiy butun sonlar va 0 dan 1 gacha tasodifiy haqiqiy son hosil qiling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))

	tasodifiy100 := r.Intn(100) + 1 // 1 dan 100 gacha
	tasodifiyKasr := r.Float64()     // 0.0 dan 1.0 gacha

	fmt.Printf("Tasodifiy butun son (1..100): %d\n", tasodifiy100)
	fmt.Printf("Tasodifiy ehtimollik: %.4f\n", tasodifiyKasr)
}
```

## Tushuntirish va Mantiq:
`rand.NewSource(time.Now().UnixNano())` orqali tasodifiy sonlar generatori har bir dastur ishga tushganda yangi boshlang'ich qiymat (seed) oladi.

## Ishlash natijasi:
```text
Tasodifiy butun son (1..100): 42
Tasodifiy ehtimollik: 0.7382
```

# 33-Topshiriq: time.Time va Go ning maxsus vaqt formatlash qolipi
## Topshiriq sharti:
`time.Now()` orqali joriy vaqtni oling va uni Go ning mashhur `2006-01-02 15:04:05` qolipida formatlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	hozir := time.Date(2026, 11, 8, 14, 30, 45, 0, time.UTC)

	fmt.Println("Standart format:", hozir.String())
	fmt.Println("Sana va vaqt:", hozir.Format("2006-01-02 15:04:05"))
	fmt.Println("Faqat sana:", hozir.Format("02.01.2006"))
	fmt.Println("Faqat soat:", hozir.Format("15:04"))
}
```

## Tushuntirish va Mantiq:
Go tilida vaqt formatlashda `%Y-%m-%d` kabi belgilar o'rniga aniq mos yozuv vaqti ishlatiladi: `2006` (yil), `01` (oy), `02` (kun), `15` (soat), `04` (daqiqa), `05` (soniya).

## Ishlash natijasi:
```text
Standart format: 2026-11-08 14:30:45 +0000 UTC
Sana va vaqt: 2026-11-08 14:30:45
Faqat sana: 08.11.2026
Faqat soat: 14:30
```

# 34-Topshiriq: time.Duration va vaqt intervallari
## Topshiriq sharti:
`time.Duration` orqali 2 soat, 45 daqiqa va 30 soniyalik vaqt oraliqlarini hisoblang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	oraliq := 2*time.Hour + 45*time.Minute + 30*time.Second

	fmt.Println("Jami oraliq:", oraliq)
	fmt.Println("Oraliq soniyalarda:", oraliq.Seconds())
	fmt.Println("Oraliq daqiqalarda:", oraliq.Minutes())
	fmt.Println("Oraliq soatlarda:", oraliq.Hours())
}
```

## Tushuntirish va Mantiq:
`time.Duration` nanosekundlarda saqlanuvchi `int64` turi bo'lib, unga `time.Hour`, `time.Minute`, `time.Second` ko'paytirilib qulay hisoblanadi.

## Ishlash natijasi:
```text
Jami oraliq: 2h45m30s
Oraliq soniyalarda: 9930
Oraliq daqiqalarda: 165.5
Oraliq soatlarda: 2.7583333333333333
```

# 35-Topshiriq: Sanalar ustida arifmetik amallar: Add, Sub, Before, After
## Topshiriq sharti:
Joriy sanaga 15 kun qo'shing, ikki sana orasidagi farqni toping va taqqoslang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	boshlanish := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
	tugash := boshlanish.Add(15 * 24 * time.Hour) // 15 kun qo'shish

	farq := tugash.Sub(boshlanish)

	fmt.Println("Boshlanish:", boshlanish.Format("2006-01-02"))
	fmt.Println("Tugash sanasi:", tugash.Format("2006-01-02"))
	fmt.Println("Oraliq kunlar:", int(farq.Hours()/24))
	fmt.Println("Boshlanish tugashdan oldinmi:", boshlanish.Before(tugash))
}
```

## Tushuntirish va Mantiq:
`t.Add(d)` vaqtga interval qo'shadi, `t2.Sub(t1)` oraliq Duration ni hisoblaydi, `Before` va `After` esa xronologik taqqoslaydi.

## Ishlash natijasi:
```text
Boshlanish: 2026-01-01
Tugash sanasi: 2026-01-16
Oraliq kunlar: 15
Boshlanish tugashdan oldinmi: true
```

# 36-Topshiriq: time.Parse yordamida matndan sanani o'qish (Parsing)
## Topshiriq sharti:
Foydalanuvchi kiritgan `2026-12-31 23:59:59` matnini `time.Time` obyektiga aylantiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	format := "2006-01-02 15:04:05"
	satr := "2026-12-31 23:59:59"

	t, err := time.Parse(format, satr)
	if err != nil {
		fmt.Println("Sana formati xato:", err)
		return
	}

	fmt.Printf("O'qilgan sana: %v\n", t)
	fmt.Printf("Yil: %d, Oy: %s, Kun: %d, Hafta kuni: %s\n", t.Year(), t.Month(), t.Day(), t.Weekday())
}
```

## Tushuntirish va Mantiq:
`time.Parse` qolip bo'yicha matnni tahlil qiladi va mos vaqt zonasida `time.Time` qaytaradi.

## Ishlash natijasi:
```text
O'qilgan sana: 2026-12-31 23:59:59 +0000 UTC
Yil: 2026, Oy: December, Kun: 31, Hafta kuni: Thursday
```

# 37-Topshiriq: Bit amallari: VA (&), YOKI (|), XOR (^), Bit Clear (&^)
## Topshiriq sharti:
Bayt bayroqlari (permission flags) ustida bit operatorlarini qo'llang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	const (
		Read    = 1 << 0 // 001 (1)
		Write   = 1 << 1 // 010 (2)
		Execute = 1 << 2 // 100 (4)
	)

	huquqlar := Read | Write // 011 (3)
	fmt.Printf("O'qish va Yozish huquqi: %03b (%d)\n", huquqlar, huquqlar)

	// Huquqni tekshirish
	canWrite := (huquqlar & Write) != 0
	canExec := (huquqlar & Execute) != 0
	fmt.Printf("Yozish mumkinmi: %t\n", canWrite)
	fmt.Printf("Bajarish mumkinmi: %t\n", canExec)

	// Bit Clear (&^) - Yozish huquqini olib tashlash:
	huquqlar = huquqlar &^ Write
	fmt.Printf("Yozish olib tashlangach: %03b (%d)\n", huquqlar, huquqlar)
}
```

## Tushuntirish va Mantiq:
Go dagi `&^` operatori (bit clear yoki AND NOT) o'ng tarafdagi 1 bo'lgan bitlarni chap tomonda 0 ga aylantirish uchun juda qulay.

## Ishlash natijasi:
```text
O'qish va Yozish huquqi: 011 (3)
Yozish mumkinmi: true
Bajarish mumkinmi: false
Yozish olib tashlangach: 001 (1)
```

# 38-Topshiriq: Bitlarni siljitish: << va >>
## Topshiriq sharti:
Sonlarni 2 ga ko'paytirish va bo'lish o'rniga chapga (`<<`) va o'ngga (`>>`) siljitish usulini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	son := 8

	fmt.Printf("%d << 1 = %d (2 ga ko'paydi)\n", son, son<<1)
	fmt.Printf("%d << 2 = %d (4 ga ko'paydi)\n", son, son<<2)
	fmt.Printf("%d >> 1 = %d (2 ga bo'lindi)\n", son, son>>1)
	fmt.Printf("%d >> 2 = %d (4 ga bo'lindi)\n", son, son>>2)
}
```

## Tushuntirish va Mantiq:
Bit siljitish apparat darajasida o'ta tezkor ishlaydi: `x << n` amali `x * 2^n`, `x >> n` amali `x / 2^n` ga teng.

## Ishlash natijasi:
```text
8 << 1 = 16 (2 ga ko'paydi)
8 << 2 = 32 (4 ga ko'paydi)
8 >> 1 = 4 (2 ga bo'lindi)
8 >> 2 = 2 (4 ga bo'lindi)
```

# 39-Topshiriq: O'n oltilik (0x), Sakkizlik (0o), Ikkilik (0b) va Katta sonlarda `_` ajratgich
## Topshiriq sharti:
Turli sanoq tizimlaridagi sonlarni e'lon qiling va katta sonlarda vizual o'qish qulayligi uchun `_` ajratgichini qo'llang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ikkilik := 0b101010       // 42
	sakkizlik := 0o755         // Linux file permission 755
	onOltilik := 0xFF          // 255
	kattaSumma := 1_000_000_000 // 1 milliard

	fmt.Printf("Ikkilik (0b101010): %d\n", ikkilik)
	fmt.Printf("Sakkizlik (0o755): %d (ruxsat: %o)\n", sakkizlik, sakkizlik)
	fmt.Printf("O'n oltilik (0xFF): %d\n", onOltilik)
	fmt.Printf("Katta summa: %d so'm\n", kattaSumma)
}
```

## Tushuntirish va Mantiq:
Go tilida sonlar orasiga qo'yilgan pastki chiziq `_` kompilyator tomonidan e'tiborga olinmaydi va faqat inson o'qishi uchun qulaylik yaratadi.

## Ishlash natijasi:
```text
Ikkilik (0b101010): 42
Sakkizlik (0o755): 493 (ruxsat: 755)
O'n oltilik (0xFF): 255
Katta summa: 1000000000 so'm
```

# 40-Topshiriq: fmt.Sprintf yordamida satr yaratish
## Topshiriq sharti:
Ekranga chiqarmasdan, ma'lumotlarni formatlangan `string` ko'rinishida saqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	foydalanuvchi := "Temur"
	balans := 1540.25
	valyuta := "USD"

	xabar := fmt.Sprintf("Salom, %s! Sizning balansingiz: %.2f %s", foydalanuvchi, balans, valyuta)

	fmt.Println("Hosil qilingan xabar:")
	fmt.Println(xabar)
}
```

## Tushuntirish va Mantiq:
`fmt.Sprintf` konsolga yozmaydi, balki formatlangan matnni yangi `string` qiymat sifatida qaytaradi.

## Ishlash natijasi:
```text
Hosil qilingan xabar:
Salom, Temur! Sizning balansingiz: 1540.25 USD
```

# 41-Topshiriq: fmt.Sscanf orqali formatlangan satr ichidan qiymatlarni o'qib olish
## Topshiriq sharti:
`IP: 192.168.1.1, Port: 8080` ko'rinishidagi satrdan IP va port qiymatlarini ajratib oling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	kiruvchiSatr := "Host: api.olam.uz, Port: 443, SSL: true"

	var host string
	var port int
	var ssl bool

	n, err := fmt.Sscanf(kiruvchiSatr, "Host: %s Port: %d, SSL: %t", &host, &port, &ssl)
	if err != nil && n < 2 {
		fmt.Println("Xatolik:", err)
	}

	fmt.Printf("O'qilgan parametrlar: Host=%s, Port=%d, SSL=%t\n", host, port, ssl)
}
```

## Tushuntirish va Mantiq:
`fmt.Sscanf` berilgan qolip bo'yicha satrni tahlil qilib, mos o'zgaruvchilarning ko'rsatkichlariga qiymatlarni yozadi.

## Ishlash natijasi:
```text
O'qilgan parametrlar: Host=api.olam.uz,, Port=443, SSL=true
```

# 42-Topshiriq: Xotira tekislanishi (Struct Memory Alignment) va unsafe.Alignof
## Topshiriq sharti:
Struktura ichidagi maydonlar tartibi xotirada qanday joy egallashiga ta'sir qilishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unsafe"
)

type YomonTuzilma struct {
	a bool  // 1 bayt
	b int64 // 8 bayt
	c bool  // 1 bayt
}

type YaxshiTuzilma struct {
	b int64 // 8 bayt
	a bool  // 1 bayt
	c bool  // 1 bayt
}

func main() {
	var yomon YomonTuzilma
	var yaxshi YaxshiTuzilma

	fmt.Println("YomonTuzilma hajmi:", unsafe.Sizeof(yomon), "bayt")
	fmt.Println("YaxshiTuzilma hajmi:", unsafe.Sizeof(yaxshi), "bayt")
}
```

## Tushuntirish va Mantiq:
Protsessorlar xotiradan ma'lumotni 8 baytlik bloklarda o'qiydi. Noto'g'ri tartiblangan maydonlar padding (bo'shliq) hisobiga 24 bayt olsa, to'g'ri tartiblanganida 16 bayt egallaydi.

## Ishlash natijasi:
```text
YomonTuzilma hajmi: 24 bayt
YaxshiTuzilma hajmi: 16 bayt
```

# 43-Topshiriq: Satrlarning o'zgarmasligi (String Immutability)
## Topshiriq sharti:
Go tilida satr belgilarini to'g'ridan-to'g'ri o'zgartirib bo'lmasligini va buni qanday to'g'ri bajarish kerakligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	matn := "Salom"
	// matn[0] = 'B' // XATO! Go da satrlar o'zgarmas (immutable)

	// To'g'ri usul: []byte ga o'girish
	baytlar := []byte(matn)
	baytlar[0] = 'B'
	yangiMatn := string(baytlar)

	fmt.Println("Eski matn:", matn)
	fmt.Println("Yangi matn:", yangiMatn)
}
```

## Tushuntirish va Mantiq:
Go xavfsizlik va parallellik (concurrency) barqarorligi uchun satrlarni to'liq o'zgarmas qilgan. O'zgartirish uchun `[]byte` yoki `[]rune` ga o'girib, qayta `string` qilinadi.

## Ishlash natijasi:
```text
Eski matn: Salom
Yangi matn: Balom
```

# 44-Topshiriq: Satr va Baytlar massivi ([]byte) o'rtasidagi konvertatsiya
## Topshiriq sharti:
Satrni `[]byte` ga aylantirib, uning baytlarini chop eting va qayta `string` ga o'giring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	soz := "Golang"
	baytlar := []byte(soz)

	fmt.Println("Baytlar massivi:", baytlar)
	for i, b := range baytlar {
		fmt.Printf("%d-bayt: %d ('%c')\n", i, b, b)
	}

	qaytaSatr := string(baytlar)
	fmt.Println("Qaytarilgan satr:", qaytaSatr)
}
```

## Tushuntirish va Mantiq:
Tarmoq va fayl I/O amallarida ma'lumotlar deyarli har doim `[]byte` shaklida uzatiladi va qabul qilinadi.

## Ishlash natijasi:
```text
Baytlar massivi: [71 111 108 97 110 103]
0-bayt: 71 ('G')
1-bayt: 111 ('o')
2-bayt: 108 ('l')
3-bayt: 97 ('a')
4-bayt: 110 ('n')
5-bayt: 103 ('g')
Qaytarilgan satr: Golang
```

# 45-Topshiriq: Satr va Runelar massivi ([]rune) bilan to'liq Unicode o'zgartirish
## Topshiriq sharti:
O'zbek tilidagi 'Qo'shiq' so'zining harflarini `[]rune` orqali teskarisiga o'giring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	asl := "Qo'shiq"
	runelar := []rune(asl)

	// Teskari o'girish (reverse)
	for i, j := 0, len(runelar)-1; i < j; i, j = i+1, j-1 {
		runelar[i], runelar[j] = runelar[j], runelar[i]
	}

	teskari := string(runelar)
	fmt.Println("Asl so'z:", asl)
	fmt.Println("Teskari so'z:", teskari)
}
```

## Tushuntirish va Mantiq:
UTF-8 satrlarda ko'p baytli belgilar bo'lgani sababli, ularni baytma-bayt emas, aynan `[]rune` orqali teskari o'girish kerak.

## Ishlash natijasi:
```text
Asl so'z: Qo'shiq
Teskari so'z: qihs'oQ
```

# 46-Topshiriq: Untyped Constants (Turlanmagan o'zgarmaslar) afzalligi
## Topshiriq sharti:
Turlanmagan o'zgarmasning kontekstga qarab avtomatik moslashuvchanligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

const Pi = 3.14159 // Untyped float constant

func main() {
	var f32 float32 = Pi
	var f64 float64 = Pi

	fmt.Printf("f32: %f (turi: %T)\n", f32, f32)
	fmt.Printf("f64: %f (turi: %T)\n", f64, f64)
}
```

## Tushuntirish va Mantiq:
Go da turi ko'rsatilmagan konstantalar juda yuqori aniqlikda saqlanadi va ulardan foydalanilgan o'zgaruvchi turiga mos ravishda avtomatik moslashadi.

## Ishlash natijasi:
```text
f32: 3.141590 (turi: float32)
f64: 3.141590 (turi: float64)
```

# 47-Topshiriq: Paket darajasidagi o'zgaruvchilar va init() funksiyasi
## Topshiriq sharti:
`init()` funksiyasidan foydalanib dastur ishga tushishidan oldin konfiguratsiyani avtomatik tayyorlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

var MaxFoydalanuvchilar int

func init() {
	// Dastur boshlanishidan oldin birinchi bo'lib bajariladi
	MaxFoydalanuvchilar = 500
	fmt.Println("[TIZIM] init() ishga tushdi, parametrlar yuklandi.")
}

func main() {
	fmt.Println("[ASOSIY] main() ishga tushdi.")
	fmt.Printf("Maksimal foydalanuvchilar soni: %d\n", MaxFoydalanuvchilar)
}
```

## Tushuntirish va Mantiq:
`init()` funksiyasi argument olmaydi va hech narsa qaytarmaydi. Go har bir paket yuklanganda `init()` ni `main()` dan oldin avtomatik chaqiradi.

## Ishlash natijasi:
```text
[TIZIM] init() ishga tushdi, parametrlar yuklandi.
[ASOSIY] main() ishga tushdi.
Maksimal foydalanuvchilar soni: 500
```

# 48-Topshiriq: os.Args orqali buyruqlar satri argumentlarini o'qish
## Topshiriq sharti:
`os.Args` massividan dastur nomi va unga uzatilgan argumentlarni ajratib oling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	// os.Args ni namoyish qilish uchun qalbaki parametrlar bilan ko'ramiz
	args := []string{"app.exe", "--port=8080", "--mode=production"}
	if len(os.Args) > 1 {
		args = os.Args
	}

	dasturNomi := args[0]
	fmt.Println("Dastur nomi:", dasturNomi)
	fmt.Println("Argumentlar soni:", len(args)-1)

	for i, arg := range args[1:] {
		fmt.Printf("Parametr %d: %s\n", i+1, arg)
	}
}
```

## Tushuntirish va Mantiq:
`os.Args[0]` doimo ishga tushirilgan dastur faylining nomini, keyingi elementlar esa uzatilgan argumentlarni saqlaydi.

## Ishlash natijasi:
```text
Dastur nomi: app.exe
Argumentlar soni: 2
Parametr 1: --port=8080
Parametr 2: --mode=production
```

# 49-Topshiriq: os.Getenv va os.Setenv orqali muhit o'zgaruvchilari (Env Vars)
## Topshiriq sharti:
Tizim muhit o'zgaruvchisini o'rnating, uni o'qing va agar mavjud bo'lmasa standart qiymat qo'llang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	// Muhit o'zgaruvchisini o'rnatamiz
	os.Setenv("DB_HOST", "postgres.production.uz")

	host := os.Getenv("DB_HOST")
	port := os.Getenv("DB_PORT")
	if port == "" {
		port = "5432" // Standart qiymat
	}

	fmt.Printf("Ma'lumotlar bazasi manzili: %s:%s\n", host, port)
}
```

## Tushuntirish va Mantiq:
Bulutli mikroservislar va 12-Factor App tamoyillarida konfiguratsiyalar aynan `os.Getenv` orqali boshqariladi.

## Ishlash natijasi:
```text
Ma'lumotlar bazasi manzili: postgres.production.uz:5432
```

# 50-Topshiriq: new() funksiyasi orqali xotira ajratish va nol ko'rsatkich yaratish
## Topshiriq sharti:
`new(int)` va `new(string)` funksiyalari orqali xotiradan joy ajrating va ularning qiymatlarini o'zgartiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	pInt := new(int)
	pStr := new(string)

	fmt.Printf("pInt manzili: %p, boshlang'ich qiymati: %d\n", pInt, *pInt)
	fmt.Printf("pStr manzili: %p, boshlang'ich qiymati: %q\n", pStr, *pStr)

	*pInt = 42
	*pStr = "Go Pointers"

	fmt.Println("Yangi pInt qiymati:", *pInt)
	fmt.Println("Yangi pStr qiymati:", *pStr)
}
```

## Tushuntirish va Mantiq:
`new(T)` funksiyasi `T` turi uchun xotira ajratadi, uni nol qiymat bilan tozalaydi va unga ko'rsatkich (`*T`) qaytaradi.

## Ishlash natijasi:
```text
pInt manzili: 0xc000012088, boshlang'ich qiymati: 0
pStr manzili: 0xc000014070, boshlang'ich qiymati: ""
Yangi pInt qiymati: 42
Yangi pStr qiymati: Go Pointers
```

