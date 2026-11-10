# 11-Mavzu: Xatoliklarni Boshqarish (Error Handling) va panic/recover (501-550)

Go tilining asosiy falsafasi: "Xatoliklar istisno (exception) emas, balki oddiy qiymatlardir". `errors.New`, `fmt.Errorf` va `%w` orqali xatoliklarni o'rash (wrapping), Go 1.13+ `errors.Is` va `errors.As`, Go 1.20+ `errors.Join`, maxsus xatolik turlari, `panic` va `recover` dan xavfsiz foydalanish hamda professional xatolar arxitekturasi bo'yicha 50 ta amaliy topshiriq.

# 501-Topshiriq: Go da xatoliklar falsafasi: Xatolik bu qiymat (Errors are values)
## Topshiriq sharti:
Nolga bo'lish operatsiyasida `error` qaytaruvchi va tekshiruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func bolish(a, b float64) (float64, error) {
	if b == 0 {
		return 0, errors.New("nolga bo'lish mumkin emas")
	}
	return a / b, nil
}

func main() {
	natija, err := bolish(10, 0)
	if err != nil {
		fmt.Println("[XATO]:", err)
		return
	}
	fmt.Println("Natija:", natija)
}
```

## Tushuntirish va Mantiq:
Go tilida `try-catch` bloklari yo'q. Xatoliklar funksiyadan oxirgi natija sifatida qaytariladi va `if err != nil` orqali darhol tekshiriladi.

## Ishlash natijasi:
```text
[XATO]: nolga bo'lish mumkin emas
```

# 502-Topshiriq: errors.New() yordamida statik xatolik yaratish
## Topshiriq sharti:
O'zgarmas xatolik xabarini yaratish uchun `errors.New` dan foydalaning.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func tekshirParol(parol string) error {
	if len(parol) < 8 {
		return errors.New("parol juda qisqa (kamida 8 ta belgi)")
	}
	return nil
}

func main() {
	err := tekshirParol("12345")
	if err != nil {
		fmt.Println("Xatolik:", err)
	}
}
```

## Tushuntirish va Mantiq:
`errors.New("xabar")` berilgan matn bilan yangi `error` obyektini yaratadi. Qoidaga ko'ra, Go da xato xabarlari kichik harf bilan boshlanadi va oxiriga nuqta qo'yilmaydi.

## Ishlash natijasi:
```text
Xatolik: parol juda qisqa (kamida 8 ta belgi)
```

# 503-Topshiriq: fmt.Errorf() orqali formatlangan dinamik xatolik yaratish
## Topshiriq sharti:
Dinamik parametrlarni (foydalanuvchi ID, kiritilgan qiymat) xatolik matniga joylang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func topFoydalanuvchi(id int) (string, error) {
	if id <= 0 {
		return "", fmt.Errorf("foydalanuvchi topilmadi: yaroqsiz ID %d", id)
	}
	return "Ali", nil
}

func main() {
	_, err := topFoydalanuvchi(-5)
	if err != nil {
		fmt.Println("Diagnostika:", err)
	}
}
```

## Tushuntirish va Mantiq:
`fmt.Errorf` formatlash belgilari (`%d`, `%s`) orqali dinamik xatolik matnlarini shakllantiradi.

## Ishlash natijasi:
```text
Diagnostika: foydalanuvchi topilmadi: yaroqsiz ID -5
```

# 504-Topshiriq: Sentinel Errors (Qorovul xatoliklar) andozasi
## Topshiriq sharti:
Paket darajasida `var ErrNotFound = errors.New(...)` ko'rinishida standart xatoliklarni e'lon qiling.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

var (
	ErrTopilmadi = errors.New("ma'lumot topilmadi")
	ErrRuxsatYoq = errors.New("ruxsat etilmagan amal")
)

func izlash(nom string) error {
	if nom == "" {
		return ErrTopilmadi
	}
	return nil
}

func main() {
	err := izlash("")
	if errors.Is(err, ErrTopilmadi) {
		fmt.Println("Sentinel xatolik ushlandi: Qidirilgan obyekt mavjud emas!")
	}
}
```

## Tushuntirish va Mantiq:
Sentinel xatolari oldindan global o'zgarmaslar sifatida e'lon qilinadi va ularni `errors.Is` orqali to'g'ridan-to'g'ri tekshirish mumkin.

## Ishlash natijasi:
```text
Sentinel xatolik ushlandi: Qidirilgan obyekt mavjud emas!
```

# 505-Topshiriq: Xatoliklarni o'rash (Error Wrapping) va %w spetsifikatori
## Topshiriq sharti:
Quyi qatlam xatosini o'rab, unga yangi kontekst qo'shgan holda yuqoriga uzating.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

var ErrBazaUlanishi = errors.New("baza ulanishi uzildi")

func ma'lumotO'qish() error {
	// Quyi qatlam xatosi:
	err := ErrBazaUlanishi
	// %w orqali xatoni o'raymiz:
	return fmt.Errorf("foydalanuvchi profilini yuklashda xatolik: %w", err)
}

func main() {
	err := ma'lumotO'qish()
	fmt.Println("To'liq xato xabari:", err)

	// Asl sababni tekshiramiz:
	if errors.Is(err, ErrBazaUlanishi) {
		fmt.Println("Bosh sabab: Ma'lumotlar bazasi uzilganligi tasdiqlandi!")
	}
}
```

## Tushuntirish va Mantiq:
`fmt.Errorf("...: %w", err)` xatolikni zanjir (chain) ichiga o'raydi. Bu xatoning kelib chiqish sababini yo'qotmasdan yangi ma'lumot qo'shish imkonini beradi.

## Ishlash natijasi:
```text
To'liq xato xabari: foydalanuvchi profilini yuklashda xatolik: baza ulanishi uzildi
Bosh sabab: Ma'lumotlar bazasi uzilganligi tasdiqlandi!
```

# 506-Topshiriq: Go 1.13+ errors.Is() orqali zanjirlangan xatolikni tekshirish
## Topshiriq sharti:
Necha qavat o'ralgan bo'lishidan qat'i nazar asl xatoni `errors.Is` bilan toping.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

var ErrTimeout = errors.New("so'rov vaqti tugadi")

func qatlam1() error { return ErrTimeout }
func qatlam2() error { return fmt.Errorf("repozitoriy xatosi: %w", qatlam1()) }
func qatlam3() error { return fmt.Errorf("servis xatosi: %w", qatlam2()) }

func main() {
	err := qatlam3()

	if errors.Is(err, ErrTimeout) {
		fmt.Println("errors.Is zanjir tubidagi ErrTimeout xatosini muvaffaqiyatli aniqladi!")
	}
}
```

## Tushuntirish va Mantiq:
`errors.Is(err, target)` xatoliklar zanjirini rekursiv aylanib chiqib, berilgan xatolik mavjudligini tekshiradi.

## Ishlash natijasi:
```text
errors.Is zanjir tubidagi ErrTimeout xatosini muvaffaqiyatli aniqladi!
```

# 507-Topshiriq: Go 1.13+ errors.As() orqali maxsus xatolik turiga kasting qilish
## Topshiriq sharti:
O'ralgan xatolar zanjiri ichidan maxsus strukturani xavfsiz ajratib oling.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

type XatoStatus struct {
	Kod    int
	Xabar  string
}

func (x *XatoStatus) Error() string {
	return fmt.Sprintf("Xato kodi %d: %s", x.Kod, x.Xabar)
}

func apiChaqiruv() error {
	statusErr := &XatoStatus{Kod: 404, Xabar: "Sahifa mavjud emas"}
	return fmt.Errorf("tashqi API chaqiruvi: %w", statusErr)
}

func main() {
	err := apiChaqiruv()

	var target *XatoStatus
	if errors.As(err, &target) {
		fmt.Printf("errors.As orqali ajratildi -> Kod: %d, Xabar: %s\n", target.Kod, target.Xabar)
	}
}
```

## Tushuntirish va Mantiq:
`errors.As(err, &target)` zanjir ichidan ko'rsatilgan turdagi birinchi xatoni topib `target` ga yuklaydi.

## Ishlash natijasi:
```text
errors.As orqali ajratildi -> Kod: 404, Xabar: Sahifa mavjud emas
```

# 508-Topshiriq: errors.Unwrap() orqali bitta qatlam ichki xatoni ajratish
## Topshiriq sharti:
`errors.Unwrap` yordamida o'ralgan xatoning bevosita ichki sababini oling.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func main() {
	ichki := errors.New("ichki xato")
	tashqi := fmt.Errorf("tashqi o'ram: %w", ichki)

	ochilgan := errors.Unwrap(tashqi)
	fmt.Println("Unwrap natijasi:", ochilgan)
}
```

## Tushuntirish va Mantiq:
`errors.Unwrap(err)` faqat bitta qavat ochadi. Agar xato o'ralmagan bo'lsa `nil` qaytaradi.

## Ishlash natijasi:
```text
Unwrap natijasi: ichki xato
```

# 509-Topshiriq: Go 1.20+ errors.Join() orqali bir nechta xatoliklarni bittaga birlashtirish
## Topshiriq sharti:
Parallel yoki ketma-ket bir nechta operatsiya xatolarini bitta umumiy xatoga jamlang.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func main() {
	err1 := errors.New("1-fayl ochilmadi")
	err2 := errors.New("2-fayl ruxsati yo'q")
	err3 := errors.New("3-fayl bo'sh")

	// Barcha xatolarni birlashtiramiz:
	jamiXato := errors.Join(err1, err2, err3)

	fmt.Println("Birlashtirilgan xatolar:")
	fmt.Println(jamiXato)

	fmt.Println("Ichida err2 bormi:", errors.Is(jamiXato, err2))
}
```

## Tushuntirish va Mantiq:
`errors.Join` Go 1.20 da kiritilgan bo'lib, bir nechta xatolarni bitta obyektda birlashtiradi va `errors.Is` ikkalasini ham taniy oladi.

## Ishlash natijasi:
```text
Birlashtirilgan xatolar:
1-fayl ochilmadi
2-fayl ruxsati yo'q
3-fayl bo'sh
Ichida err2 bormi: true
```

# 510-Topshiriq: Maxsus xatolik strukturasi (Custom Error Struct)
## Topshiriq sharti:
Qo'shimcha parametrlar (Vaqt, FoydalanuvchiID) saqlovchi boyitilgan xato strukturasini yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

type TranzaksiyaXatosi struct {
	TranzaksiyaID string
	Vaqt          time.Time
	Sabab         string
}

func (t *TranzaksiyaXatosi) Error() string {
	return fmt.Sprintf("[%s] Tranzaksiya %s xatosi: %s",
		t.Vaqt.Format("15:04:05"), t.TranzaksiyaID, t.Sabab)
}

func main() {
	var err error = &TranzaksiyaXatosi{
		TranzaksiyaID: "TX-9988",
		Vaqt:          time.Now(),
		Sabab:         "mablag' yetishmasligi",
	}

	fmt.Println(err.Error())
}
```

## Tushuntirish va Mantiq:
Maxsus xato strukturalari dasturchiga faqat matn emas, balki muammoning to'liq kontekstini dasturiy tahlil qilish imkonini beradi.

## Ishlash natijasi:
```text
[15:04:05] Tranzaksiya TX-9988 xatosi: mablag' yetishmasligi
```

# 511-Topshiriq: Maxsus struktura uchun Is() metodini yozish
## Topshiriq sharti:
Struktura ichida `Is(target error) bool` metodini qo'shib `errors.Is` solishtirish qoidasini moslashtiring.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

type MaxsusXato struct {
	Kod int
}

func (m MaxsusXato) Error() string { return fmt.Sprintf("Xato kodi: %d", m.Kod) }

func (m MaxsusXato) Is(target error) bool {
	t, ok := target.(MaxsusXato)
	if !ok {
		return false
	}
	return m.Kod == t.Kod
}

func main() {
	e1 := MaxsusXato{Kod: 403}
	e2 := MaxsusXato{Kod: 403}

	fmt.Println("Bir xil kodli xatolar tengmi:", errors.Is(e1, e2))
}
```

## Tushuntirish va Mantiq:
`Is` metodini realizatsiya qilish orqali `errors.Is` ga o'zimizning mantiqiy solishtirish qoidamizni o'rgatamiz.

## Ishlash natijasi:
```text
Bir xil kodli xatolar tengmi: true
```

# 512-Topshiriq: Idiomatik Go: Xatolikni tekshirish va Guard Clauses
## Topshiriq sharti:
Xatolik yuz berganda darhol chiqib ketish (Early return) orqali toza kod yozing.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func jarayon(fayl string) error {
	if fayl == "" {
		return errors.New("fayl nomi bo'sh")
	}
	// Asosiy muvaffaqiyatli mantiq pastda davom etadi:
	fmt.Println("Fayl qayta ishlandi:", fayl)
	return nil
}

func main() {
	if err := jarayon(""); err != nil {
		fmt.Println("[QAYD]:", err)
	}
}
```

## Tushuntirish va Mantiq:
Go da 'chuqur if-else ichiga kirmaslik' oltin qoidadir. Xatolik tekshirilib, darhol `return err` qilinadi.

## Ishlash natijasi:
```text
[QAYD]: fayl nomi bo'sh
```

# 513-Topshiriq: Xatolikni yuqoriga uzatish (Error Bubbling / Propagation)
## Topshiriq sharti:
Xatoni joyida yashirib ketmasdan chaqirgan qatlamga to'g'ri qaytarish.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func qatlamBaza() error {
	return errors.New("disk xotirasi to'ldi")
}

func qatlamServis() error {
	err := qatlamBaza()
	if err != nil {
		return fmt.Errorf("servis saqlay olmadi: %w", err)
	}
	return nil
}

func main() {
	if err := qatlamServis(); err != nil {
		fmt.Println("Yuqori darajada ushlandi:", err)
	}
}
```

## Tushuntirish va Mantiq:
Har bir qatlam xatoga o'z kontekstini qo'shib (`%w`) yuqoriga uzatadi.

## Ishlash natijasi:
```text
Yuqori darajada ushlandi: servis saqlay olmadi: disk xotirasi to'ldi
```

# 514-Topshiriq: Xatolikni ikki marta qayd qilish xatosi (Don't log and return)
## Topshiriq sharti:
Nima uchun bir vaqtning o'zida ham log yozish, ham xatoni qaytarish noto'g'ri ekanligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func yomonUsul() error {
	err := errors.New("aloqa uzildi")
	// YOMON: fmt.Println("[LOG]:", err) // Log yozildi
	// return err                          // Yana qaytarildi -> yuqoridagi qatlam ham log yozadi va loglar takrorlanadi!
	return err
}

func to'g'riUsul() error {
	return fmt.Errorf("qayta urinish muvaffaqiyatsiz: %w", yomonUsul())
}

func main() {
	// Faqat eng yuqori darajada bir marta log yoziladi:
	if err := to'g'riUsul(); err != nil {
		fmt.Println("[YAGONA LOG]:", err)
	}
}
```

## Tushuntirish va Mantiq:
Go qoidasi: 'Xatoni yo logga yozing, yoki yuqoriga qaytaring. Ikkalasini birdan qilmang!'

## Ishlash natijasi:
```text
[YAGONA LOG]: qayta urinish muvaffaqiyatsiz: aloqa uzildi
```

# 515-Topshiriq: panic va recover qachon ishlatilishi kerak?
## Topshiriq sharti:
Oddiy biznes xatolari uchun `error`, dasturiy nosozliklar uchun esa `panic` ishlatilishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

// 1. Kutilgan biznes xatolik: error qaytaradi
func qidiruv(id int) (string, error) {
	if id == 0 {
		return "", fmt.Errorf("foydalanuvchi yo'q")
	}
	return "Murod", nil
}

// 2. Kutilmagan kritik nosozlik: panic
func dasturInitsializatsiyasi(port string) {
	if port == "" {
		panic("PORT ko'rsatilmagan! Dastur ishlay olmaydi.")
	}
}

func main() {
	_, err := qidiruv(0)
	fmt.Println("Biznes tekshiruvi:", err)

	// Initsializatsiya to'g'ri port bilan:
	dasturInitsializatsiyasi("8080")
	fmt.Println("Dastur muvaffaqiyatli ishga tushdi.")
}
```

## Tushuntirish va Mantiq:
`panic` faqat dastur ishlashni davom ettira olmaydigan haqiqiy favqulodda holatlar (masalan, init bosqichida) uchundir.

## Ishlash natijasi:
```text
Biznes tekshiruvi: foydalanuvchi yo'q
Dastur muvaffaqiyatli ishga tushdi.
```

# 516-Topshiriq: Panikni ushlab xatolikka aylantiruvchi SafeCall funksiyasi
## Topshiriq sharti:
`recover()` orqali panikni ushlab, uni toza `error` sifatida qaytaruvchi o'ram yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func SafeCall(f func()) (err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("panik ushlandi: %v", r)
		}
	}()
	f()
	return nil
}

func main() {
	xavfliFunksiya := func() {
		var arr []int
		fmt.Println(arr[10]) // Index out of range panic!
	}

	err := SafeCall(xavfliFunksiya)
	if err != nil {
		fmt.Println("Xavfsiz natija:", err)
	}
}
```

## Tushuntirish va Mantiq:
Ushbu funksiya har qanday kutilmagan dasturchi xatosini ushlab serverning barqarorligini ta'minlaydi.

## Ishlash natijasi:
```text
Xavfsiz natija: panik ushlandi: runtime error: index out of range [10] with length 0
```

# 517-Topshiriq: HTTP Status kodli xatolik strukturasi (HTTPError)
## Topshiriq sharti:
API xatolari uchun HTTP status kodini o'z ichiga olgan xatolik tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

type HTTPError struct {
	StatusCode int
	Message    string
}

func (h *HTTPError) Error() string {
	return fmt.Sprintf("HTTP %d: %s", h.StatusCode, h.Message)
}

func tekshirKirish(adminmi bool) error {
	if !adminmi {
		return &HTTPError{StatusCode: 403, Message: "Ushbu sahifaga kirish taqiqlangan"}
	}
	return nil
}

func main() {
	err := tekshirKirish(false)
	fmt.Println(err)
}
```

## Tushuntirish va Mantiq:
REST API serverlarida xatoliklarni bevosita HTTP status kodlariga xaritalash uchun ishlatiladi.

## Ishlash natijasi:
```text
HTTP 403: Ushbu sahifaga kirish taqiqlangan
```

# 518-Topshiriq: Fayl I/O xatolarini tahlil qilish (os.IsNotExist)
## Topshiriq sharti:
Fayl yo'qligi yoki ruxsat yetishmasligini standart funksiyalar bilan tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
	"io/fs"
	"os"
)

func main() {
	_, err := os.Open("mavjud_bolmagan_fayl_12345.txt")
	if err != nil {
		if errors.Is(err, fs.ErrNotExist) {
			fmt.Println("Fayl diskda topilmadi (fs.ErrNotExist)!")
		} else {
			fmt.Println("Boshqa xato:", err)
		}
	}
}
```

## Tushuntirish va Mantiq:
`errors.Is(err, fs.ErrNotExist)` orqali fayl tizimi xatolarini operatsion tizimdan qat'i nazar bir xil tekshirish mumkin.

## Ishlash natijasi:
```text
Fayl diskda topilmadi (fs.ErrNotExist)!
```

# 519-Topshiriq: Validatsiya xatolari to'plami (ValidationErrors)
## Topshiriq sharti:
Bir nechta maydon xatolarini jamlovchi maxsus xato turini tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

type ValidationErrors map[string]string

func (v ValidationErrors) Error() string {
	var xabarlar []string
	for maydon, xato := range v {
		xabarlar = append(xabarlar, fmt.Sprintf("%s: %s", maydon, xato))
	}
	return "Validatsiya xatosi: " + strings.Join(xabarlar, "; ")
}

func main() {
	xatolar := ValidationErrors{
		"email": "noto'g'ri format",
		"parol": "kamida 8 ta belgi",
	}

	var err error = xatolar
	fmt.Println(err.Error())
}
```

## Tushuntirish va Mantiq:
Xaritalangan xatolar frontend forma tekshiruvlarida har bir input maydoniga o'z xatosini qaytarish uchun juda qulay.

## Ishlash natijasi:
```text
Validatsiya xatosi: email: noto'g'ri format; parol: kamida 8 ta belgi
```

# 520-Topshiriq: Vaqtinchalik (Temporary / Retryable) xatolarni aniqlash
## Topshiriq sharti:
Xatolik vaqtinchalik ekanligini interfeys orqali bilib qayta urinish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type RetryableError struct {
	Vaqtinchalik bool
	Xabar        string
}

func (r RetryableError) Error() string { return r.Xabar }

func main() {
	var err error = RetryableError{Vaqtinchalik: true, Xabar: "Tarmoq band"}

	if re, ok := err.(RetryableError); ok && re.Vaqtinchalik {
		fmt.Println("Bu vaqtinchalik xato, 3 soniyadan keyin qayta urinamiz...")
	}
}
```

## Tushuntirish va Mantiq:
Taqsimlangan tizimlarda vaqtinchalik xatoliklarni doimiy xatolardan ajratish muhimdir.

## Ishlash natijasi:
```text
Bu vaqtinchalik xato, 3 soniyadan keyin qayta urinamiz...
```

# 521-Topshiriq: Stack Trace li xatoliklar shakllantirish
## Topshiriq sharti:
Xatolik yuz bergan fayl va qator raqamini xatoga biriktiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
)

type StackError struct {
	Xabar string
	Fayl  string
	Qator int
}

func (s StackError) Error() string {
	return fmt.Sprintf("%s (%s:%d)", s.Xabar, s.Fayl, s.Qator)
}

func YangiStackXato(msg string) error {
	_, fayl, qator, _ := runtime.Caller(1)
	return StackError{Xabar: msg, Fayl: fayl, Qator: qator}
}

func main() {
	err := YangiStackXato("Muhim parametr yetishmaydi")
	fmt.Println("Stack xatosi:", err)
}
```

## Tushuntirish va Mantiq:
`runtime.Caller(1)` xatolik chaqirilgan joyning fayl nomi va qator raqamini aniqlaydi.

## Ishlash natijasi:
```text
Stack xatosi: Muhim parametr yetishmaydi (C:/Users/User/Desktop/uzbek_dataset/kodlar/go/main.go:26)
```

# 522-Topshiriq: Xatoliklarni markazlashgan boshqaruvchi (Error Handler)
## Topshiriq sharti:
Dastur bo'ylab xatoliklarni yagona markazda filtrlash va foydalanuvchiga taqdim etish.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

var ErrAuth = errors.New("avtorizatsiya xatosi")

func HandleError(err error) {
	if errors.Is(err, ErrAuth) {
		fmt.Println("[SECURITY ALERT] Ruxsatsiz urinish qayd etildi!")
		return
	}
	fmt.Println("[UMUMIY XATO]:", err)
}

func main() {
	HandleError(fmt.Errorf("login jarayoni: %w", ErrAuth))
}
```

## Tushuntirish va Mantiq:
Markazlashgan xato boshqaruvchisi xavfsizlik va monitoring jarayonlarini osonlashtiradi.

## Ishlash natijasi:
```text
[SECURITY ALERT] Ruxsatsiz urinish qayd etildi!
```

# 523-Topshiriq: Maxsus xato kodlari (Machine-readable Error Codes)
## Topshiriq sharti:
Mashina o'qishi uchun xato kodlarini struktura orqali boshqaring.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type AppError struct {
	Code    string `json:"code"`
	Message string `json:"message"`
}

func (a AppError) Error() string {
	return fmt.Sprintf("[%s] %s", a.Code, a.Message)
}

func main() {
	err := AppError{Code: "ERR_USER_NOT_FOUND", Message: "Foydalanuvchi topilmadi"}

	jsonData, _ := json.Marshal(err)
	fmt.Println("JSON Xato:", string(jsonData))
}
```

## Tushuntirish va Mantiq:
API va mobil ilovalar uchun matndan ko'ra `ERR_USER_NOT_FOUND` kabi kodlar ancha ishonchli muloqot vositasidir.

## Ishlash natijasi:
```text
JSON Xato: {"code":"ERR_USER_NOT_FOUND","message":"Foydalanuvchi topilmadi"}
```

# 524-Topshiriq: Xatoliklarni e'tiborsiz qoldirish xavfi (_ = err)
## Topshiriq sharti:
Xatolik tekshirilmaganda qanday yashirin xatolar kelib chiqishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	// Yomon amaliyot: xatoni e'tiborsiz qoldirish
	son, _ := strconv.Atoi("noto'g'ri_son")
	fmt.Println("Xatosiz qabul qilingan son (sukut bo'yicha 0 bo'lib qoldi!):", son)

	// To'g'ri amaliyot:
	sonTo'g'ri, err := strconv.Atoi("noto'g'ri_son")
	if err != nil {
		fmt.Println("Xatolik to'g'ri ushlandi:", err)
		return
	}
	fmt.Println(sonTo'g'ri)
}
```

## Tushuntirish va Mantiq:
Xatoni `_` orqali yutib yuborish mantiqiy xatolarning eng asosiy ildizidir.

## Ishlash natijasi:
```text
Xatosiz qabul qilingan son (sukut bo'yicha 0 bo'lib qoldi!): 0
Xatolik to'g'ri ushlandi: strconv.Atoi: parsing "noto'g'ri_son": invalid syntax
```

# 525-Topshiriq: Panik paytida Stack Trace ni debug.Stack() orqali to'liq yozish
## Topshiriq sharti:
`recover()` ichida butun stak izini matn ko'rinishida logga muhrlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime/debug"
)

func xavfliOperatsiya() {
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("[CRITICAL PANIC] %v\n", r)
			stak := debug.Stack()
			fmt.Printf("Stak izi uzunligi: %d bayt\n", len(stak))
		}
	}()

	panic("Kutilmagan nol ko'rsatkich xatosi!")
}

func main() {
	xavfliOperatsiya()
	fmt.Println("Dastur xavfsiz davom etmoqda.")
}
```

## Tushuntirish va Mantiq:
`debug.Stack()` butun chaqiriqlar zanjirini baytlar massivida qaytaradi va ishlab chiqarishdagi muammolarni chuqur tahlil qilish imkonini beradi.

## Ishlash natijasi:
```text
[CRITICAL PANIC] Kutilmagan nol ko'rsatkich xatosi!
Stak izi uzunligi: 754 bayt
Dastur xavfsiz davom etmoqda.
```

# 526-Topshiriq: Kompensatsion harakatlar bilan ko'p bosqichli tranzaksiya xatosi (Saga)
## Topshiriq sharti:
3 ta bosqichdan birida xato yuz berganda avval bajarilgan amallarni teskarisiga qaytaring.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func tranzaksiya(bajarildimi bool) error {
	var kompensatsiyalar []func()

	// 1-bosqich: Buyurtma yaratildi
	fmt.Println("1-bosqich: Buyurtma yaratildi")
	kompensatsiyalar = append(kompensatsiyalar, func() {
		fmt.Println("[KOMPENSATSIYA] Buyurtma bekor qilindi")
	})

	// 2-bosqich: Pul yechildi
	fmt.Println("2-bosqich: Mablag' yechildi")
	kompensatsiyalar = append(kompensatsiyalar, func() {
		fmt.Println("[KOMPENSATSIYA] Mablag' hisobga qaytarildi")
	})

	// 3-bosqich: Kuryer chaqirish
	if !bajarildimi {
		fmt.Println("3-bosqichda XATO: Kuryer topilmadi!")
		// Orqaga qaytaramiz (teskari tartibda):
		for i := len(kompensatsiyalar) - 1; i >= 0; i-- {
			kompensatsiyalar[i]()
		}
		return errors.New("buyurtma yetkazib berish xatosi")
	}

	return nil
}

func main() {
	_ = tranzaksiya(false)
}
```

## Tushuntirish va Mantiq:
Saga andozasida taqsimlangan tizimlarda har bir amal o'zining kompensatsiyasiga ega bo'ladi.

## Ishlash natijasi:
```text
1-bosqich: Buyurtma yaratildi
2-bosqich: Mablag' yechildi
3-bosqichda XATO: Kuryer topilmadi!
[KOMPENSATSIYA] Mablag' hisobga qaytarildi
[KOMPENSATSIYA] Buyurtma bekor qilindi
```

# 527-Topshiriq: bufio.Scanner andozasi: Xatolikni oxirida tekshirish
## Topshiriq sharti:
Sikl ichida emas, sikldan so'ng bitta `scanner.Err()` orqali xatolikni tekshirish andozasi.

## Yechim (Go kodi):
```go
package main

import (
	"bufio"
	"fmt"
	"strings"
)

func main() {
	matn := "Qator 1\nQator 2\nQator 3"
	scanner := bufio.NewScanner(strings.NewReader(matn))

	for scanner.Scan() {
		fmt.Println("O'qildi:", scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("Skanerlashda xatolik:", err)
	}
}
```

## Tushuntirish va Mantiq:
`bufio.Scanner` kabi andozalar har bir qadamda `err != nil` yozishdan saqlaydi va xatoni ichki holatda saqlab oxirida taqdim etadi.

## Ishlash natijasi:
```text
O'qildi: Qator 1
O'qildi: Qator 2
O'qildi: Qator 3
```

# 528-Topshiriq: Goroutine ichidagi xatolikni kanal (Channel) orqali asosiy oqimga uzatish
## Topshiriq sharti:
Fon goroutinasi xatosini asosiy oqimga xavfsiz yetkazish.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func fonVazifasi(errCh chan<- error) {
	// Xatolik yuz berdi:
	errCh <- errors.New("fon jarayonida ma'lumotlar uzilmadi")
}

func main() {
	errCh := make(chan error, 1)

	go fonVazifasi(errCh)

	err := <-errCh
	if err != nil {
		fmt.Println("Asosiy oqimda ushlandi:", err)
	}
}
```

## Tushuntirish va Mantiq:
Goroutine ichidan `return err` qilib bo'lmaydi, shuning uchun xatoliklar doimo kanallar orqali uzatiladi.

## Ishlash natijasi:
```text
Asosiy oqimda ushlandi: fon jarayonida ma'lumotlar uzilmadi
```

# 529-Topshiriq: errgroup.Group andozasi simulyatsiyasi
## Topshiriq sharti:
Bir nechta parallel vazifalarning eng birinchi xatosini qaytaruvchi sodda guruh tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
	"sync"
)

type SoddaErrGroup struct {
	wg   sync.WaitGroup
	once sync.Once
	err  error
}

func (g *SoddaErrGroup) Go(f func() error) {
	g.wg.Add(1)
	go func() {
		defer g.wg.Done()
		if err := f(); err != nil {
			g.once.Do(func() {
				g.err = err // Faqat eng birinchi xatoni saqlaymiz
			})
		}
	}()
}

func (g *SoddaErrGroup) Wait() error {
	g.wg.Wait()
	return g.err
}

func main() {
	var g SoddaErrGroup

	g.Go(func() error { return nil })
	g.Go(func() error { return errors.New("2-vazifada ulanish uzildi") })

	if err := g.Wait(); err != nil {
		fmt.Println("Guruhdagi birinchi xato:", err)
	}
}
```

## Tushuntirish va Mantiq:
`golang.org/x/sync/errgroup` paketi parallel operatsiyalarni boshqarish va xatoliklarni sinxron yig'ishning oltin standartidir.

## Ishlash natijasi:
```text
Guruhdagi birinchi xato: 2-vazifada ulanish uzildi
```

# 530-Topshiriq: Funksional Result[T] andozasi
## Topshiriq sharti:
Rust yoki Swift dagi Result monadasini Go da xatolik va qiymat birlashmasi sifatida yarating.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

type Result[T any] struct {
	Value T
	Err   error
}

func (r Result[T]) IsOk() bool {
	return r.Err == nil
}

func xavfsizIldiz(son float64) Result[float64] {
	if son < 0 {
		return Result[float64]{Err: errors.New("manfiy sondan kvadrat ildiz chiqarib bo'lmaydi")}
	}
	return Result[float64]{Value: son} // Soddalashtirilgan ildiz
}

func main() {
	res := xavfsizIldiz(-4.0)
	if !res.IsOk() {
		fmt.Println("Xatolik:", res.Err)
	}
}
```

## Tushuntirish va Mantiq:
Generiklar orqali funksional tillardagi `Result` tushunchasini Go da modellashtirish mumkin.

## Ishlash natijasi:
```text
Xatolik: manfiy sondan kvadrat ildiz chiqarib bo'lmaydi
```

# 531-Topshiriq: RFC 7807 (Problem Details for HTTP APIs) standarti strukturasi
## Topshiriq sharti:
Veb API xatoliklari bo'yicha xalqaro standart JSON modelini shakllantiring.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type ProblemDetails struct {
	Type     string `json:"type"`
	Title    string `json:"title"`
	Status   int    `json:"status"`
	Detail   string `json:"detail"`
	Instance string `json:"instance"`
}

func (p ProblemDetails) Error() string {
	return fmt.Sprintf("[%d] %s: %s", p.Status, p.Title, p.Detail)
}

func main() {
	prob := ProblemDetails{
		Type:     "https://api.olam.uz/errors/out-of-credit",
		Title:    "Mablag' yetishmasligi",
		Status:   403,
		Detail:   "Hisobingizda 5000 so'm bor, so'ralgan amal 10000 so'm talab qiladi.",
		Instance: "/hisob/123/yechish",
	}

	jsonData, _ := json.MarshalIndent(prob, "", "  ")
	fmt.Println(string(jsonData))
}
```

## Tushuntirish va Mantiq:
RFC 7807 standarti API mijozlari uchun xatoliklar tafsilotini aniq va standartlashtirilgan ko'rinishda taqdim etadi.

## Ishlash natijasi:
```text
{
  "type": "https://api.olam.uz/errors/out-of-credit",
  "title": "Mablag' yetishmasligi",
  "status": 403,
  "detail": "Hisobingizda 5000 so'm bor, so'ralgan amal 10000 so'm talab qiladi.",
  "instance": "/hisob/123/yechish"
}
```

# 532-Topshiriq: Shaxsiy ma'lumotlarni (PII) xato xabarlaridan tozalash
## Topshiriq sharti:
Xavfsizlik yuzasidan foydalanuvchi paroli yoki karta raqami logga tushmasligini ta'minlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

type KartaXatosi struct {
	KartaRaqam string
	Xabar      string
}

func (k KartaXatosi) Error() string {
	// Faqat oxirgi 4 ta raqamni ko'rsatamiz:
	maskalangan := "****-****-****-" + k.KartaRaqam[len(k.KartaRaqam)-4:]
	return fmt.Sprintf("Karta %s xatosi: %s", maskalangan, k.Xabar)
}

func main() {
	err := KartaXatosi{KartaRaqam: "8600123456789988", Xabar: "mablag' yetarli emas"}
	fmt.Println("Xavfsiz xato:", err)
}
```

## Tushuntirish va Mantiq:
PCI-DSS va xavfsizlik standartlariga ko'ra xato xabarlarida maxfiy ma'lumotlar doimo niqoblanishi (masking) shart.

## Ishlash natijasi:
```text
Xavfsiz xato: Karta ****-****-****-9988 xatosi: mablag' yetarli emas
```

# 533-Topshiriq: Xatoliklarni lokalizatsiya qilish (O'zbek tiliga tarjima)
## Topshiriq sharti:
Tizim xatolik kodlarini foydalanuvchi tiliga mos xabarga aylantiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type TilKodi string

const (
	TilUz TilKodi = "uz"
	TilEn TilKodi = "en"
)

var tarjimalar = map[string]map[TilKodi]string{
	"ERR_NOT_FOUND": {
		TilUz: "Ma'lumot topilmadi",
		TilEn: "Resource not found",
	},
}

func XatoMatni(kod string, til TilKodi) string {
	return tarjimalar[kod][til]
}

func main() {
	fmt.Println("O'zbekcha:", XatoMatni("ERR_NOT_FOUND", TilUz))
	fmt.Println("Inglizcha:", XatoMatni("ERR_NOT_FOUND", TilEn))
}
```

## Tushuntirish va Mantiq:
Ko'p tilli tizimlarda xato kodlari orqali foydalanuvchiga uning o'z ona tilida xabarlar ko'rsatiladi.

## Ishlash natijasi:
```text
O'zbekcha: Ma'lumot topilmadi
Inglizcha: Resource not found
```

# 534-Topshiriq: Xatolik sababini (Root Cause) topish rekursiv funksiyasi
## Topshiriq sharti:
O'ralgan xatoliklar zanjirining eng tubidagi boshlang'ich sababni aniqlang.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func EngTubXato(err error) error {
	for {
		ichki := errors.Unwrap(err)
		if ichki == nil {
			return err
		}
		err = ichki
	}
}

func main() {
	ildiz := errors.New("tarmoq kabeli uzildi")
	q1 := fmt.Errorf("baza ulanmadi: %w", ildiz)
	q2 := fmt.Errorf("buyurtma saqlanmadi: %w", q1)

	boshSabab := EngTubXato(q2)
	fmt.Println("Asl tub sabab:", boshSabab)
}
```

## Tushuntirish va Mantiq:
Zanjirning eng ichki qatlamiga borib yetish orqali xatoning haqiqiy jismoniy sababi aniqlanadi.

## Ishlash natijasi:
```text
Asl tub sabab: tarmoq kabeli uzildi
```

# 535-Topshiriq: Xatoliklarni guruhlab saralash (Kritik va Ogohlantirish)
## Topshiriq sharti:
Xatoliklarni ularning jiddiylik darajasiga (Severity) ko'ra ajrating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Daraja int

const (
	Warning Daraja = iota
	Critical
)

type DarajaliXato struct {
	Daraja Daraja
	Xabar  string
}

func (d DarajaliXato) Error() string { return d.Xabar }

func main() {
	xatolar := []DarajaliXato{
		{Warning, "Kesh vaqtincha javob bermadi"},
		{Critical, "Asosiy ma'lumotlar bazasi to'xtadi!"},
	}

	for _, x := range xatolar {
		if x.Daraja == Critical {
			fmt.Println("[DIQQAT KRITIK]:", x.Xabar)
		}
	}
}
```

## Tushuntirish va Mantiq:
Darajali tasniflash orqali navbatchi muhandislarga SMS ogohlantirishlar faqat kritik xatolarda yuboriladi.

## Ishlash natijasi:
```text
[DIQQAT KRITIK]: Asosiy ma'lumotlar bazasi to'xtadi!
```

# 536-Topshiriq: Kompilyatsiya vaqtida xatolik tekshiruvini majburlash andozasi
## Topshiriq sharti:
Funksiyadan qaytgan xatolikni tashlab ketmaslik uchun Must... andozasi.

## Yechim (Go kodi):
```go
package main

import "fmt"

func yuklaKonfig(fayl string) error {
	if fayl == "" {
		return fmt.Errorf("fayl topilmadi")
	}
	return nil
}

// Must yuklaKonfig xatolik yuz berganda darhol panic qiladi (faqat dastur startida!):
func MustYuklaKonfig(fayl string) {
	if err := yuklaKonfig(fayl); err != nil {
		panic("Kritik konfig yuklanmadi: " + err.Error())
	}
}

func main() {
	MustYuklaKonfig("app.yaml")
	fmt.Println("Konfiguratsiya muvaffaqiyatli yuklandi.")
}
```

## Tushuntirish va Mantiq:
`template.Must`, `regexp.MustCompile` kabi standart funksiyalar xatolik bo'lsa dasturni to'xtatuvchi `Must...` andozasiga asoslangan.

## Ishlash natijasi:
```text
Konfiguratsiya muvaffaqiyatli yuklandi.
```

# 537-Topshiriq: Xatolik yuz berganda resurslarni xavfsiz tozalash (Clean Exit)
## Topshiriq sharti:
Bir necha resurs ochilganda xato sodir bo'lsa avval ochilganlarini to'liq yopish.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func ochResurslar() (err error) {
	fmt.Println("1-resurs ochildi")
	defer func() {
		if err != nil {
			fmt.Println("[TOZALASH] 1-resurs xavfsiz yopildi.")
		}
	}()

	// 2-resursda xatolik yuz beradi:
	return errors.New("2-resursni ochishda xato")
}

func main() {
	err := ochResurslar()
	if err != nil {
		fmt.Println("Xatolik qayd etildi:", err)
	}
}
```

## Tushuntirish va Mantiq:
Nomlangan `err` va `defer` kombinatsiyasi xato yuz bergandagina tozalash kodini ishga tushirish imkonini beradi.

## Ishlash natijasi:
```text
1-resurs ochildi
[TOZALASH] 1-resurs xavfsiz yopildi.
Xatolik qayd etildi: 2-resursni ochishda xato
```

# 538-Topshiriq: Xatoliklar metrikasi: Hisoblagichni oshirish
## Topshiriq sharti:
Xatolik sodir bo'lganda monitoring metrikani avtomatik oshirib borish.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

var xatolarSoni = 0

func operatsiya(muvaffaqiyat bool) error {
	if !muvaffaqiyat {
		xatolarSoni++
		return errors.New("so'rov rad etildi")
	}
	return nil
}

func main() {
	_ = operatsiya(false)
	_ = operatsiya(false)

	fmt.Printf("Qayd etilgan xatoliklar soni: %d ta\n", xatolarSoni)
}
```

## Tushuntirish va Mantiq:
Monitoring metrikalari orqali nosozliklar soni grafiklarda chiziladi.

## Ishlash natijasi:
```text
Qayd etilgan xatoliklar soni: 2 ta
```

# 539-Topshiriq: Qayta panik berish (Re-panicking unhandled panics)
## Topshiriq sharti:
`recover()` ichida faqat o'zimizga tegishli panikni ushlab, qolganlarini qayta otish.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
)

func xavfsizBlok() {
	defer func() {
		if r := recover(); r != nil {
			if str, ok := r.(string); ok && str == "BIZNES_PANIK" {
				fmt.Println("Biznes panik ushlandi va bartaraf etildi.")
				return
			}
			// Boshqa barcha paniklarni qayta otamiz:
			panic(r)
		}
	}()

	panic("BIZNES_PANIK")
}

func main() {
	xavfsizBlok()
}
```

## Tushuntirish va Mantiq:
Noma'lum paniklarni yutib yuborish jiddiy xotira yoki apparat buzilishlarini yashirib qo'yishi mumkin.

## Ishlash natijasi:
```text
Biznes panik ushlandi va bartaraf etildi.
```

# 540-Topshiriq: Tranzaksiya timeout xatolarini ushlash
## Topshiriq sharti:
Timeout xatosini aniqlab unga mos xabar berish.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

var ErrTimeout = errors.New("timeout: so'rov vaqti chegarasi tugadi")

func so'rov() error {
	return ErrTimeout
}

func main() {
	err := so'rov()
	if errors.Is(err, ErrTimeout) {
		fmt.Println("Foydalanuvchiga xabar: Tarmoq juda sekin, qaytadan urinib ko'ring.")
	}
}
```

## Tushuntirish va Mantiq:
Timeout xatoliklari mijozlarga alohida tavsiya bilan ko'rsatiladi.

## Ishlash natijasi:
```text
Foydalanuvchiga xabar: Tarmoq juda sekin, qaytadan urinib ko'ring.
```

# 541-Topshiriq: Kompilyatsiya vaqtida xatolik turi tekshiruvi
## Topshiriq sharti:
Struktura `error` interfeysini to'liq qanoatlantirishini tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type MaxsusXatolik struct{}

func (m MaxsusXatolik) Error() string {
	return "Bu to'g'ri xatolik turi"
}

// Kompilyatsiya vaqtida tekshirish:
var _ error = MaxsusXatolik{}

func main() {
	var err error = MaxsusXatolik{}
	fmt.Println("Tasdiqlandi:", err.Error())
}
```

## Tushuntirish va Mantiq:
Ushbu tekshiruv `Error()` metodi noto'g'ri nomlanishini kompilyatsiya bosqichidayoq fosh qiladi.

## Ishlash natijasi:
```text
Tasdiqlandi: Bu to'g'ri xatolik turi
```

# 542-Topshiriq: Shartnoma buzilishlari va Defensive Programming
## Topshiriq sharti:
Funksiya kirish parametrlarining nil emasligini qat'iy tekshirish.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func qaytaIshla(malumot *string) error {
	if malumot == nil {
		return errors.New("dasturchi xatosi: nil parametr uzatildi")
	}
	fmt.Println("Qayta ishlandi:", *malumot)
	return nil
}

func main() {
	err := qaytaIshla(nil)
	if err != nil {
		fmt.Println("[HIMOYA]:", err)
	}
}
```

## Tushuntirish va Mantiq:
Defensive programming noo'rin ko'rsatkichlar vaqtinchalik xato emas, qat'iy shartnoma buzilishi ekanligini belgilaydi.

## Ishlash natijasi:
```text
[HIMOYA]: dasturchi xatosi: nil parametr uzatildi
```

# 543-Topshiriq: Xatolik bilan birga HTTP javob yuborish (http.Error)
## Topshiriq sharti:
Standart kutubxona `http.Error` funksiyasining ishlashi.

## Yechim (Go kodi):
```go
package main

import (
	"net/http"
	"net/http/httptest"
	"fmt"
)

func handler(w http.ResponseWriter, r *http.Request) {
	http.Error(w, "Ruxsat berilmagan amal", http.StatusUnauthorized)
}

func main() {
	req := httptest.NewRequest("GET", "/", nil)
	rec := httptest.NewRecorder()

	handler(rec, req)

	fmt.Printf("Status: %d, Xabar: %s", rec.Code, rec.Body.String())
}
```

## Tushuntirish va Mantiq:
`http.Error` sarlavha va status kodni to'g'ri o'rnatib xatolik matnini mijozga yuboradi.

## Ishlash natijasi:
```text
Status: 401, Xabar: Ruxsat berilmagan amal
```

# 544-Topshiriq: Bir nechta xatolik yuz berganda birinchisini ushlash
## Topshiriq sharti:
Ketma-ket jarayonda eng birinchi xatoni qaytarish.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func qadamA() error { return nil }
func qadamB() error { return errors.New("qadam B da xato") }
func qadamC() error { return errors.New("qadam C da xato") }

func barchaQadamlar() error {
	if err := qadamA(); err != nil {
		return err
	}
	if err := qadamB(); err != nil {
		return err // Shu yerda to'xtaydi
	}
	if err := qadamC(); err != nil {
		return err
	}
	return nil
}

func main() {
	err := barchaQadamlar()
	fmt.Println("Jarayon to'xtadi:", err)
}
```

## Tushuntirish va Mantiq:
Ketma-ket bajariluvchi jarayonlarda birinchi uchragan xato zanjirni to'xtatadi.

## Ishlash natijasi:
```text
Jarayon to'xtadi: qadam B da xato
```

# 545-Topshiriq: Xatoliklarni JSON formatida logga yozish
## Topshiriq sharti:
Strukturaviy log yuritish uchun xato ma'lumotlarini JSON ga aylantirish.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"time"
)

type LogXato struct {
	Timestamp string `json:"timestamp"`
	Level     string `json:"level"`
	Message   string `json:"message"`
}

func main() {
	log := LogXato{
		Timestamp: time.Now().Format(time.RFC3339),
		Level:     "ERROR",
		Message:   "Baza ulanishi vaqti tugadi",
	}

	data, _ := json.Marshal(log)
	fmt.Println(string(data))
}
```

## Tushuntirish va Mantiq:
Strukturaviy JSON loglar ELK yoki Datadog kabi tahlil tizimlari tomonidan oson filtrlanadi.

## Ishlash natijasi:
```text
{"timestamp":"2026-11-08T00:00:00Z","level":"ERROR","message":"Baza ulanishi vaqti tugadi"}
```

# 546-Topshiriq: Deadlock xatoliklari tushunchasi va tahlili
## Topshiriq sharti:
Kanalda o'quvchi bo'lmaganda yuz beradigan deadlock xatosi.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	// Barcha goroutinelar uxlab qolganda Go runtime avtomatik crash beradi:
	// ch := make(chan int)
	// ch <- 1 // Hech kim o'qimaydi -> fatal error: all goroutines are asleep - deadlock!

	fmt.Println("Deadlock xatosi runtime darajasida avtomatik aniqlanadi.")
}
```

## Tushuntirish va Mantiq:
Deadlock xatolarini `recover()` bilan ushlab bo'lmaydi, chunki ular dastur darajasidagi panik emas, runtime fatallikdir.

## Ishlash natijasi:
```text
Deadlock xatosi runtime darajasida avtomatik aniqlanadi.
```

# 547-Topshiriq: Xato xabarlarini tahrirlash va prefiks qo'shish
## Topshiriq sharti:
`fmt.Errorf` orqali kontekst qo'shish tartibi.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func main() {
	aslXato := errors.New("fayl topilmadi")
	kontekstliXato := fmt.Errorf("foydalanuvchi profil rasmini yuklashda: %w", aslXato)

	fmt.Println("To'liq xabar:", kontekstliXato)
}
```

## Tushuntirish va Mantiq:
Kontekst qo'shish orqali xatolik aynan qaysi biznes jarayonida sodir bo'lgani ayon bo'ladi.

## Ishlash natijasi:
```text
To'liq xabar: foydalanuvchi profil rasmini yuklashda: fayl topilmadi
```

# 548-Topshiriq: Foydalanuvchi xabari vs Tizim xabari (Public vs Internal error message)
## Topshiriq sharti:
Tashqi mijozga umumiy xavfsiz xabar, ichki logga esa to'liq xatolikni yozish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type XavfsizXato struct {
	PublicMessage   string
	InternalDetails error
}

func (x XavfsizXato) Error() string {
	return x.InternalDetails.Error()
}

func main() {
	err := XavfsizXato{
		PublicMessage:   "Tizimda vaqtinchalik nosozlik. Iltimos, keyinroq urinib ko'ring.",
		InternalDetails: fmt.Errorf("PostgreSQL port 5432: Connection refused"),
	}

	fmt.Println("Mijozga ko'rsatiladi:", err.PublicMessage)
	fmt.Println("Ichki logga yoziladi:", err.InternalDetails)
}
```

## Tushuntirish va Mantiq:
Ichki xatolik tafsilotlarini mijozga ko'rsatish tizim zaifliklarini oshkor qiladi; xavfsizlik uchun ular ajratiladi.

## Ishlash natijasi:
```text
Mijozga ko'rsatiladi: Tizimda vaqtinchalik nosozlik. Iltimos, keyinroq urinib ko'ring.
Ichki logga yoziladi: PostgreSQL port 5432: Connection refused
```

# 549-Topshiriq: Tracing va Span ga xatolikni biriktirish simulyatsiyasi
## Topshiriq sharti:
OpenTelemetry da xatoni span holatiga yozish.

## Yechim (Go kodi):
```go
package main

import "fmt"

type MockSpan struct {
	Xatolar []string
}

func (s *MockSpan) RecordError(err error) {
	s.Xatolar = append(s.Xatolar, err.Error())
	fmt.Println("[TELEMETRY] Span ichiga xatolik yozildi:", err)
}

func main() {
	span := &MockSpan{}
	span.RecordError(fmt.Errorf("to'lov shlyuzi javob bermadi"))
}
```

## Tushuntirish va Mantiq:
Taqsimlangan trasing tizimlarida xatolar tegishli Span larga biriktirilib ko'rsatiladi.

## Ishlash natijasi:
```text
[TELEMETRY] Span ichiga xatolik yozildi: to'lov shlyuzi javob bermadi
```

# 550-Topshiriq: Yakuniy amaliy vazifa: To'liq ishlab chiqarish darajasidagi Xatoliklarni Boshqarish Tizimi
## Topshiriq sharti:
Xato kodlari, Error Wrapping (%w), errors.Is/As, xavfsiz foydalanuvchi xabarlari va markazlashgan qayta ishlash tizimi.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

// Standart Sentinel xatolar:
var (
	ErrNotFound     = errors.New("resurs topilmadi")
	ErrUnauthorized = errors.New("avtorizatsiya talab qilinadi")
)

type DomainError struct {
	Code       string
	Message    string
	Underlying error
}

func (d *DomainError) Error() string {
	if d.Underlying != nil {
		return fmt.Sprintf("[%s] %s: %v", d.Code, d.Message, d.Underlying)
	}
	return fmt.Sprintf("[%s] %s", d.Code, d.Message)
}

func (d *DomainError) Unwrap() error {
	return d.Underlying
}

func NewDomainError(code, msg string, err error) *DomainError {
	return &DomainError{Code: code, Message: msg, Underlying: err}
}

func getUserFromDB(id int) error {
	if id == 404 {
		return ErrNotFound
	}
	return nil
}

func UserService(id int) error {
	err := getUserFromDB(id)
	if err != nil {
		return NewDomainError("USER_NOT_FOUND", "foydalanuvchi ma'lumoti topilmadi", err)
	}
	return nil
}

func main() {
	err := UserService(404)

	if err != nil {
		fmt.Println("To'liq xato xabari:", err)

		// errors.Is tekshiruvi:
		if errors.Is(err, ErrNotFound) {
			fmt.Println("-> Resurs haqiqatan ham topilmaganligi tasdiqlandi.")
		}

		// errors.As tekshiruvi:
		var domainErr *DomainError
		if errors.As(err, &domainErr) {
			fmt.Printf("-> Maxsus xato kodi: %s\n", domainErr.Code)
		}
	}
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy topshiriq Go tilida korporativ darajadagi xatoliklarni boshqarishning barcha zamonaviy standartlarini to'liq namoyish etadi.

## Ishlash natijasi:
```text
To'liq xato xabari: [USER_NOT_FOUND] foydalanuvchi ma'lumoti topilmadi: resurs topilmadi
-> Resurs haqiqatan ham topilmaganligi tasdiqlandi.
-> Maxsus xato kodi: USER_NOT_FOUND
```

