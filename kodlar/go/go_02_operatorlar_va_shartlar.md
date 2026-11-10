# 2-Mavzu: Operatorlar va Shart Konstruksiyalari (51-100)

Go dasturlash tilining operatorlari (arifmetik, taqqoslash, mantiqiy, inkrement/dekrement xususiyatlari), `if`, `if-else`, qisqa e'lonli `if` konstruksiyalari, `switch-case`, `fallthrough`, turli murakkab mantiqiy tekshiruvlar va shartli algoritmlar bo'yicha 50 ta amaliy topshiriq.

# 51-Topshiriq: Arifmetik operatorlar (+, -, *, /, %) va ularning ishlashi
## Topshiriq sharti:
Ikkita butun son ustida barcha arifmetik amallarni bajaring va qoldiqli bo'lish natijasini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	a := 23
	b := 5

	fmt.Printf("%d + %d = %d\n", a, b, a+b)
	fmt.Printf("%d - %d = %d\n", a, b, a-b)
	fmt.Printf("%d * %d = %d\n", a, b, a*b)
	fmt.Printf("%d / %d = %d (butun bo'lish)\n", a, b, a/b)
	fmt.Printf("%d %% %d = %d (qoldiq)\n", a, b, a%b)
}
```

## Tushuntirish va Mantiq:
Go tilida `%` operatori faqat butun sonlar uchun amal qiladi. Butun sonlarni bo'lishda natija har doim pastga yaxlitlanib butun qismi olinadi.

## Ishlash natijasi:
```text
23 + 5 = 28
23 - 5 = 18
23 * 5 = 115
23 / 5 = 4 (butun bo'lish)
23 % 5 = 3 (qoldiq)
```

# 52-Topshiriq: Taqqoslash operatorlari (==, !=, <, <=, >, >=)
## Topshiriq sharti:
Ikkita o'zgaruvchini solishtirib barcha taqqoslash natijalarini `bool` shaklida ekranga chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	x := 15
	y := 20

	fmt.Printf("%d == %d : %t\n", x, y, x == y)
	fmt.Printf("%d != %d : %t\n", x, y, x != y)
	fmt.Printf("%d <  %d : %t\n", x, y, x < y)
	fmt.Printf("%d <= %d : %t\n", x, y, x <= y)
	fmt.Printf("%d >  %d : %t\n", x, y, x > y)
	fmt.Printf("%d >= %d : %t\n", x, y, x >= y)
}
```

## Tushuntirish va Mantiq:
Taqqoslash operatorlari ikkita qiymatni o'zaro solishtiradi va mantiqiy `true` yoki `false` qaytaradi. Taqqoslanayotgan tomonlarning turlari bir xil bo'lishi shart.

## Ishlash natijasi:
```text
15 == 20 : false
15 != 20 : true
15 <  20 : true
15 <= 20 : true
15 >  20 : false
15 >= 20 : false
```

# 53-Topshiriq: Mantiqiy operatorlar: &&, ||, !
## Topshiriq sharti:
Foydalanuvchining hisob holati va obunasi asosida tizimga kirish ruxsatini hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	faol := true
	obunaBor := false
	bloklangan := false

	kirishRuxsati := faol && (obunaBor || !bloklangan)

	fmt.Printf("Hisob faol: %t\n", faol)
	fmt.Printf("Obuna mavjud: %t\n", obunaBor)
	fmt.Printf("Bloklangan: %t\n", bloklangan)
	fmt.Printf("Kirishga ruxsat bormi: %t\n", kirishRuxsati)
}
```

## Tushuntirish va Mantiq:
`&&` har ikkala shart to'g'ri bo'lganda `true`, `||` kamida bittasi to'g'ri bo'lganda `true`, `!` esa qiymatni teskarisiga o'zgartiradi.

## Ishlash natijasi:
```text
Hisob faol: true
Obuna mavjud: false
Bloklangan: false
Kirishga ruxsat bormi: true
```

# 54-Topshiriq: O'zlashtirish bilan birgalikdagi operatorlar (+=, -=, *=, /=, %=)
## Topshiriq sharti:
O'zgaruvchi qiymatini qisqartirilgan arifmetik operatorlar orqali yangilang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	balans := 1000

	balans += 250 // balans = balans + 250
	fmt.Println("Kirimdan keyin:", balans)

	balans -= 150 // balans = balans - 150
	fmt.Println("Xarajatdan keyin:", balans)

	balans *= 2   // 2 barobar oshirish
	fmt.Println("Ikki baravardan keyin:", balans)

	balans /= 4   // 4 ga bo'lish
	fmt.Println("Bo'lingandan keyin:", balans)

	balans %= 70  // 70 ga bo'lgandagi qoldiq
	fmt.Println("Qoldiq:", balans)
}
```

## Tushuntirish va Mantiq:
`op=` ko'rinishidagi operatorlar kodni ixchamlashtiradi va hisoblangan natijani o'zgaruvchining o'ziga qayta yozadi.

## Ishlash natijasi:
```text
Kirimdan keyin: 1250
Xarajatdan keyin: 1100
Ikki baravardan keyin: 2200
Bo'lingandan keyin: 550
Qoldiq: 60
```

# 55-Topshiriq: Go da Inkrement (++) va Dekrement (--) operatorlarining o'ziga xosligi
## Topshiriq sharti:
Go tilida `++` va `--` faqat operator/statement ekanligini va nima uchun `b = a++` xato ekanligini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	i := 10

	i++ // To'g'ri: statement
	fmt.Println("Inkrementdan keyin i:", i)

	i-- // To'g'ri: statement
	fmt.Println("Dekrementdan keyin i:", i)

	// DIQQAT: Quyidagilar Go da sintaktik XATOLIK:
	// ++i       (Go da prefiks shakli mavjud emas!)
	// b := i++  (i++ qiymat qaytarmaydi, shuning uchun boshqa o'zgaruvchiga tenglab bo'lmaydi!)
}
```

## Tushuntirish va Mantiq:
C, C++ va Java dan farqli ravishda Go da kod chalkashliklarini yo'qotish uchun `++` va `--` faqat postfiks statement hisoblanadi. Ular ifoda (expression) emas.

## Ishlash natijasi:
```text
Inkrementdan keyin i: 11
Dekrementdan keyin i: 10
```

# 56-Topshiriq: Oddiy if sharti bilan tekshiruv
## Topshiriq sharti:
Harorat 30 darajadan yuqori bo'lsa 'Konditsionerni yoqing' degan xabar chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	harorat := 34.5

	if harorat > 30.0 {
		fmt.Printf("Harorat %.1f°C - juda issiq! Konditsionerni yoqing.\n", harorat)
	}
}
```

## Tushuntirish va Mantiq:
Go tilida `if` sharti atrofida qavslar `()` qo'yilmaydi, lekin jingalak qavslar `{}` majburiydir.

## Ishlash natijasi:
```text
Harorat 34.5°C - juda issiq! Konditsionerni yoqing.
```

# 57-Topshiriq: if - else konstruksiyasi bilan balandlik tekshiruvi
## Topshiriq sharti:
Attraksionga kirish uchun bola bo'yi 120 sm dan kam bo'lmasligi kerakligini tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	boyi := 115

	if boyi >= 120 {
		fmt.Println("Attraksionga kirishingiz mumkin!")
	} else {
		fmt.Printf("Kechirasiz, bo'yingiz %d sm. Minimal talab: 120 sm.\n", boyi)
	}
}
```

## Tushuntirish va Mantiq:
`else` kalit so'zi doimo `if` blokining yopilish jingalak qavsi `}` bilan bir qatorda yozilishi shart (`} else {`), aks holda Go kompilyatori nuqtali vergul qo'yib xato beradi.

## Ishlash natijasi:
```text
Kechirasiz, bo'yingiz 115 sm. Minimal talab: 120 sm.
```

# 58-Topshiriq: if - else if - else zanjiri bilan baholash
## Topshiriq sharti:
Ballga qarab bahoni aniqlang: 90+ (A), 80+ (B), 70+ (C), 60+ (D), qolgani (F).

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ball := 84

	if ball >= 90 {
		fmt.Println("Baho: A (A'lo)")
	} else if ball >= 80 {
		fmt.Println("Baho: B (Yaxshi)")
	} else if ball >= 70 {
		fmt.Println("Baho: C (Qoniqarli)")
	} else if ball >= 60 {
		fmt.Println("Baho: D (Yetarli)")
	} else {
		fmt.Println("Baho: F (Qoniqarsiz)")
	}
}
```

## Tushuntirish va Mantiq:
`else if` zanjiri birinchi to'g'ri kelgan shartni bajaradi va qolganlarini tashlab o'tadi.

## Ishlash natijasi:
```text
Baho: B (Yaxshi)
```

# 59-Topshiriq: if ichida qisqa o'zgaruvchi e'lon qilish (Short Statement)
## Topshiriq sharti:
`if` boshida o'zgaruvchi e'lon qilib, uni shu `if` va `else` bloklari doirasida cheklang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func kvadrat(n int) int {
	return n * n
}

func main() {
	if res := kvadrat(7); res > 40 {
		fmt.Printf("Kvadrat %d - 40 dan katta!\n", res)
	} else {
		fmt.Printf("Kvadrat %d - 40 dan kichik yoki teng.\n", res)
	}

	// Bu yerda `res` mavjud emas, uning skopi faqat if/else ichidadir!
}
```

## Tushuntirish va Mantiq:
Go tilida `if qisqa_statement; shart` andozasi o'zgaruvchining ko'rinish sohasini (scope) qisqartirish orqali kod tozaligini ta'minlaydi.

## Ishlash natijasi:
```text
Kvadrat 49 - 40 dan katta!
```

# 60-Topshiriq: Idiomatik Go: if orqali xatolikni tekshirish (Error Handling Pattern)
## Topshiriq sharti:
`strconv.Atoi` chaqiruvini `if` ichida qisqa e'lon qilib xatolik bor-yo'qligini tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	matn := "2026yil"

	if son, err := strconv.Atoi(matn); err != nil {
		fmt.Println("[XATO] Raqamga aylantirib bo'lmadi:", err)
	} else {
		fmt.Println("[MUVAFFAQIN] Olingan son:", son)
	}
}
```

## Tushuntirish va Mantiq:
Go da `if err := ...; err != nil` eng mashhur andoza bo'lib, xatolik yuz berganda uni darhol ushlaydi.

## Ishlash natijasi:
```text
[XATO] Raqamga aylantirib bo'lmadi: strconv.Atoi: parsing "2026yil": invalid syntax
```

# 61-Topshiriq: Ichma-ich joylashgan (Nested) if shartlari
## Topshiriq sharti:
Haydovchilik guvohnomasi va mastlik holatini ichma-ich `if` orqali tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	pravaBor := true
	mastlikDarajasi := 0.0

	if pravaBor {
		if mastlikDarajasi == 0.0 {
			fmt.Println("Haydashga to'liq ruxsat beriladi.")
		} else {
			fmt.Println("Harakatlanish taqiqlanadi: spirtli ichimlik aniqlandi!")
		}
	} else {
		fmt.Println("Harakatlanish taqiqlanadi: haydovchilik guvohnomasi yo'q!")
	}
}
```

## Tushuntirish va Mantiq:
Ichma-ich `if` larda har bir daraja mantiqiy aniqlikni tekshiradi, lekin kod tozaligi uchun chuqur nestingdan qochish tavsiya etiladi.

## Ishlash natijasi:
```text
Haydashga to'liq ruxsat beriladi.
```

# 62-Topshiriq: Mantiqiy ifodalarning qisqa tutashuvi (Short-Circuit Evaluation)
## Topshiriq sharti:
`&&` va `||` amallarida ikkinchi ifoda qachon hisoblanmasligini isbotlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func xabar(tekshiruvNomi string) bool {
	fmt.Println("Funksiya chaqirildi:", tekshiruvNomi)
	return true
}

func main() {
	fmt.Println("--- && tekshiruvi (birinchisi false) ---")
	if false && xabar("AND_IKKINCHI") {
		// xabar() chaqirilmaydi
	}

	fmt.Println("--- || tekshiruvi (birinchisi true) ---")
	if true || xabar("OR_IKKINCHI") {
		// xabar() chaqirilmaydi
	}
}
```

## Tushuntirish va Mantiq:
Go tilida `&&` da birinchi qiymat `false` bo'lsa, ikkinchisi umuman hisoblanmaydi. `||` da birinchisi `true` bo'lsa, ikkinchisi bajarilmaydi.

## Ishlash natijasi:
```text
--- && tekshiruvi (birinchisi false) ---
--- || tekshiruvi (birinchisi true) ---
```

# 63-Topshiriq: Go da Ternary operator (`?:`) yo'qligi va uning o'rni
## Topshiriq sharti:
Boshqa tillardagi `a ? b : c` o'rniga Go da qanday toza usul qo'llanilishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ball := 75

	// Go da `holat = ball >= 60 ? "O'tdi" : "Yiqildi"` YO'Q!
	// O'rniga oddiy if-else:
	holat := "Yiqildi"
	if ball >= 60 {
		holat = "O'tdi"
	}

	fmt.Printf("Imtihon natijasi: %s (Ball: %d)\n", holat, ball)
}
```

## Tushuntirish va Mantiq:
Go tili dizaynerlari o'qilishi noaniq va qatorlarni chalkashtiruvchi ternary operatorni ongli ravishda tilga kiritishmagan.

## Ishlash natijasi:
```text
Imtihon natijasi: O'tdi (Ball: 75)
```

# 64-Topshiriq: Oddiy switch - case konstruksiyasi
## Topshiriq sharti:
Hafta kuni raqami bo'yicha kun nomini aniqlovchi `switch` yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	kunRaqami := 3
	kunNomi := ""

	switch kunRaqami {
	case 1:
		kunNomi = "Dushanba"
	case 2:
		kunNomi = "Seshanba"
	case 3:
		kunNomi = "Chorshanba"
	case 4:
		kunNomi = "Payshanba"
	case 5:
		kunNomi = "Juma"
	case 6:
		kunNomi = "Shanba"
	case 7:
		kunNomi = "Yakshanba"
	}

	fmt.Printf("%d-kun bu: %s\n", kunRaqami, kunNomi)
}
```

## Tushuntirish va Mantiq:
Go dagi `switch` da `break` yozish shart emas! Case mos kelishi bilan blok avtomatik tugaydi.

## Ishlash natijasi:
```text
3-kun bu: Chorshanba
```

# 65-Topshiriq: switch ichida default bloki
## Topshiriq sharti:
Noma'lum komanda kiritilganda `default` orqali ogohlantirish bering.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	buyruq := "restart"

	switch buyruq {
	case "start":
		fmt.Println("Tizim ishga tushirilmoqda...")
	case "stop":
		fmt.Println("Tizim to'xtatilmoqda...")
	default:
		fmt.Printf("Noma'lum buyruq: %q. Faqat start yoki stop mumkin.\n", buyruq)
	}
}
```

## Tushuntirish va Mantiq:
Hech qaysi `case` mos kelmasa, `default` bloki ishlaydi.

## Ishlash natijasi:
```text
Noma'lum buyruq: "restart". Faqat start yoki stop mumkin.
```

# 66-Topshiriq: Bitta case da bir nechta qiymatni sanash
## Topshiriq sharti:
Ish kuni yoki dam olish kuni ekanligini bitta case da bir nechta kunlarni ko'rsatib aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	kun := "Shanba"

	switch kun {
	case "Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma":
		fmt.Printf("%s - Ish kuni.\n", kun)
	case "Shanba", "Yakshanba":
		fmt.Printf("%s - Dam olish kuni!\n", kun)
	default:
		fmt.Println("Bunday kun mavjud emas.")
	}
}
```

## Tushuntirish va Mantiq:
Go da `case v1, v2, v3:` orqali bir necha qiymatlarni vergul bilan ajratib tekshirish mumkin.

## Ishlash natijasi:
```text
Shanba - Dam olish kuni!
```

# 67-Topshiriq: Shartsiz switch (Switch without Condition)
## Topshiriq sharti:
O'zgaruvchisiz `switch` orqali toza va o'qilishi oson `if-else` muqobilini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	soat := 14

	switch {
	case soat < 6:
		fmt.Println("Xayrli tun")
	case soat < 12:
		fmt.Println("Xayrli tong")
	case soat < 18:
		fmt.Println("Xayrli kun")
	default:
		fmt.Println("Xayrli oqshom")
	}
}
```

## Tushuntirish va Mantiq:
`switch` dan keyin hech narsa yozilmasa, u `switch true` deb qaraladi. Har bir `case` da mustaqil boolean ifoda tekshiriladi.

## Ishlash natijasi:
```text
Xayrli kun
```

# 68-Topshiriq: switch boshida qisqa o'zgaruvchi e'lon qilish
## Topshiriq sharti:
Operatsion tizim turini aniqlashda `switch` ichida qisqa o'zgaruvchi e'lon qiling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("Apple macOS tizimi")
	case "linux":
		fmt.Println("Linux tizimi")
	case "windows":
		fmt.Println("Microsoft Windows tizimi")
	default:
		fmt.Printf("Boshqa tizim: %s\n", os)
	}
}
```

## Tushuntirish va Mantiq:
`switch os := runtime.GOOS; os` sintaksisi o'zgaruvchini faqat switch bloki ichida ko'rinadigan qiladi.

## Ishlash natijasi:
```text
Microsoft Windows tizimi
```

# 69-Topshiriq: fallthrough kalit so'zi va keyingi case ga o'tish
## Topshiriq sharti:
`fallthrough` orqali bir case dan keyingi case ga majburiy o'tishni namoyish qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	bosqich := 1

	switch bosqich {
	case 1:
		fmt.Println("1-bosqich: Baza yaratildi.")
		fallthrough
	case 2:
		fmt.Println("2-bosqich: Migratsiyalar bajarildi.")
		fallthrough
	case 3:
		fmt.Println("3-bosqich: Server ishga tushdi.")
	}
}
```

## Tushuntirish va Mantiq:
`fallthrough` operatori shartni qayta tekshirmasdan darhol keyingi `case` kodini bajaradi.

## Ishlash natijasi:
```text
1-bosqich: Baza yaratildi.
2-bosqich: Migratsiyalar bajarildi.
3-bosqich: Server ishga tushdi.
```

# 70-Topshiriq: switch orqali sonlar oralig'ini tekshirish
## Topshiriq sharti:
Xarid summasiga qarab chegirma foizini aniqlovchi switch yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	xaridSummasi := 750000.0
	chegirmaFoizi := 0

	switch {
	case xaridSummasi >= 1000000:
		chegirmaFoizi = 20
	case xaridSummasi >= 500000:
		chegirmaFoizi = 15
	case xaridSummasi >= 200000:
		chegirmaFoizi = 10
	default:
		chegirmaFoizi = 0
	}

	chegirmaSummasi := xaridSummasi * float64(chegirmaFoizi) / 100.0
	fmt.Printf("Xarid: %.0f so'm | Chegirma: %d%% (%.0f so'm)\n", xaridSummasi, chegirmaFoizi, chegirmaSummasi)
}
```

## Tushuntirish va Mantiq:
Oraliq shartlari yuqoridan pastga qarab tekshiriladi va eng birinchi mos kelgan case bajariladi.

## Ishlash natijasi:
```text
Xarid: 750000 so'm | Chegirma: 15% (112500 so'm)
```

# 71-Topshiriq: Type Switch orqali noaniq turning haqiqiy toifasini aniqlash
## Topshiriq sharti:
`any` (bo'sh interfeys) turidagi qiymatning asl turini `switch v := i.(type)` orqali aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func turiniTekshir(i any) {
	switch v := i.(type) {
	case int:
		fmt.Printf("Butun son: %d (ikki baravari: %d)\n", v, v*2)
	case string:
		fmt.Printf("Satr: %q (uzunligi: %d)\n", v, len(v))
	case bool:
		fmt.Printf("Mantiqiy qiymat: %t\n", v)
	default:
		fmt.Printf("Noma'lum tur: %T\n", v)
	}
}

func main() {
	turiniTekshir(42)
	turiniTekshir("Salom Go")
	turiniTekshir(true)
}
```

## Tushuntirish va Mantiq:
Type switch Go da polimorfizmni boshqarishning eng qulay va xavfsiz mexanizmidir.

## Ishlash natijasi:
```text
Butun son: 42 (ikki baravari: 84)
Satr: "Salom Go" (uzunligi: 8)
Mantiqiy qiymat: true
```

# 72-Topshiriq: Satrlarni leksikografik taqqoslash (<, >)
## Topshiriq sharti:
Ikki satrni alifbo tartibida solishtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	soz1 := "Olma"
	soz2 := "Anor"

	if soz1 < soz2 {
		fmt.Printf("%q so'zi %q dan oldin keladi.\n", soz1, soz2)
	} else if soz1 > soz2 {
		fmt.Printf("%q so'zi %q dan keyin keladi.\n", soz1, soz2)
	} else {
		fmt.Println("So'zlar bir xil.")
	}
}
```

## Tushuntirish va Mantiq:
Go satrlarni baytma-bayt (Unicode kodlariga ko'ra) solishtiradi. 'A' (65) 'O' (79) dan kichik bo'lgani uchun 'Anor' oldin keladi.

## Ishlash natijasi:
```text
"Olma" so'zi "Anor" dan keyin keladi.
```

# 73-Topshiriq: strings.EqualFold bilan registrga sezgir bo'lmagan solishtirish
## Topshiriq sharti:
Katta va kichik harflarni farqlamasdan (case-insensitive) foydalanuvchi buyrug'ini tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	kiritilgan := "YeS"
	kutilgan := "yes"

	if strings.EqualFold(kiritilgan, kutilgan) {
		fmt.Printf("%q va %q bir xil ma'noda (EqualFold = true)\n", kiritilgan, kutilgan)
	} else {
		fmt.Println("Mos emas.")
	}
}
```

## Tushuntirish va Mantiq:
`strings.EqualFold` Unicode qoidalariga binoan katta-kichik harflarni teng deb hisoblaydi.

## Ishlash natijasi:
```text
"YeS" va "yes" bir xil ma'noda (EqualFold = true)
```

# 74-Topshiriq: Sonning juft yoki toqligini aniqlash
## Topshiriq sharti:
`%` operatori orqali berilgan son juft yoki toq ekanligini aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	son := 47

	if son%2 == 0 {
		fmt.Printf("%d - juft son.\n", son)
	} else {
		fmt.Printf("%d - toq son.\n", son)
	}
}
```

## Tushuntirish va Mantiq:
2 ga bo'lgandagi qoldiq 0 bo'lsa son juft, aks holda toq hisoblanadi.

## Ishlash natijasi:
```text
47 - toq son.
```

# 75-Topshiriq: Kabisa yilini aniqlash algoritmi
## Topshiriq sharti:
Yil kabisa yili (366 kun) yoki oddiy yil (365 kun) ekanligini mantiqiy shartlar orqali hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func isLeapYear(yil int) bool {
	// 400 ga bo'linsa kabisa, YOKI (4 ga bo'linib 100 ga bo'linmasa) kabisa
	return (yil%400 == 0) || (yil%4 == 0 && yil%100 != 0)
}

func main() {
	yillar := []int{2020, 2024, 2025, 2026, 2000, 1900}

	for _, y := range yillar {
		fmt.Printf("%d-yil: kabisami? -> %t\n", y, isLeapYear(y))
	}
}
```

## Tushuntirish va Mantiq:
Kabisa yili qoidasi: yil 4 ga qoldiqsiz bo'linishi kerak, biroq 100 ga bo'linuvchi yillar faqat 400 ga ham bo'lingandagina kabisa hisoblanadi.

## Ishlash natijasi:
```text
2020-yil: kabisami? -> true
2024-yil: kabisami? -> true
2025-yil: kabisami? -> false
2026-yil: kabisami? -> false
2000-yil: kabisami? -> true
1900-yil: kabisami? -> false
```

# 76-Topshiriq: Uchta sondan eng kattasini topish (Max of Three)
## Topshiriq sharti:
Uchta turli son berilgan. Shartli operatorlar yordamida ularning eng kattasini aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func maxUchta(a, b, c int) int {
	katta := a
	if b > katta {
		katta = b
	}
	if c > katta {
		katta = c
	}
	return katta
}

func main() {
	x, y, z := 45, 89, 32
	engKatta := maxUchta(x, y, z)
	fmt.Printf("%d, %d va %d sonlaridan eng kattasi: %d\n", x, y, z, engKatta)
}
```

## Tushuntirish va Mantiq:
Dastlab birinchi son eng katta deb qabul qilinadi, so'ngra qolgan sonlar ketma-ket u bilan taqqoslanadi.

## Ishlash natijasi:
```text
45, 89 va 32 sonlaridan eng kattasi: 89
```

# 77-Topshiriq: Sonning ishorasini aniqlash (Musbat, Manfiy, Nol)
## Topshiriq sharti:
Berilgan son musbat, manfiy yoki nolga teng ekanligini aniqlovchi shart tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ishora(son float64) string {
	if son > 0 {
		return "Musbat"
	} else if son < 0 {
		return "Manfiy"
	}
	return "Nol"
}

func main() {
	fmt.Println("15.5:", ishora(15.5))
	fmt.Println("-7.2:", ishora(-7.2))
	fmt.Println("0.0:", ishora(0.0))
}
```

## Tushuntirish va Mantiq:
Son 0 dan katta bo'lsa musbat, kichik bo'lsa manfiy, aks holda nol bo'ladi.

## Ishlash natijasi:
```text
15.5: Musbat
-7.2: Manfiy
0.0: Nol
```

# 78-Topshiriq: Uchburchak mavjudlik shartini tekshirish (Triangle Inequality)
## Topshiriq sharti:
Berilgan uchta tomon uzunliklari orqali haqiqiy uchburchak yasash mumkinligini tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func uchburchakMavjudmi(a, b, c float64) bool {
	return (a+b > c) && (a+c > b) && (b+c > a)
}

func main() {
	fmt.Println("Tomonlar 3, 4, 5:", uchburchakMavjudmi(3, 4, 5))
	fmt.Println("Tomonlar 1, 2, 10:", uchburchakMavjudmi(1, 2, 10))
}
```

## Tushuntirish va Mantiq:
Uchburchak tengsizligi qoidasi: har qanday ikki tomonining yig'indisi uchinchi tomondan qat'iy katta bo'lishi shart.

## Ishlash natijasi:
```text
Tomonlar 3, 4, 5: true
Tomonlar 1, 2, 10: false
```

# 79-Topshiriq: Yosh va huquq bo'yicha tizimga kirish shartlari
## Topshiriq sharti:
Yosh 18 dan katta va tasdiqlangan profilga ega foydalanuvchiga to'liq ruxsat bering.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ruxsatHolati(yosh int, tasdiqlangan bool) string {
	if yosh >= 18 && tasdiqlangan {
		return "To'liq ruxsat berildi"
	} else if yosh >= 18 && !tasdiqlangan {
		return "Profil tasdiqlanmagan: faqat o'qish rejimi"
	}
	return "Yosh chegarasi yetarli emas"
}

func main() {
	fmt.Println("Foydalanuvchi 1 (22 yosh, tasdiqlangan):", ruxsatHolati(22, true))
	fmt.Println("Foydalanuvchi 2 (20 yosh, tasdiqlanmagan):", ruxsatHolati(20, false))
	fmt.Println("Foydalanuvchi 3 (16 yosh, tasdiqlangan):", ruxsatHolati(16, true))
}
```

## Tushuntirish va Mantiq:
Mantiqiy shartlar biznes qoidalarini aniq darajalarga ajratib boshqaradi.

## Ishlash natijasi:
```text
Foydalanuvchi 1 (22 yosh, tasdiqlangan): To'liq ruxsat berildi
Foydalanuvchi 2 (20 yosh, tasdiqlanmagan): Profil tasdiqlanmagan: faqat o'qish rejimi
Foydalanuvchi 3 (16 yosh, tasdiqlangan): Yosh chegarasi yetarli emas
```

# 80-Topshiriq: Harorat shkalalarini (Selsiy, Farengeyt, Kelvin) switch orqali konvertatsiya qilish
## Topshiriq sharti:
Selsiydagi haroratni tanlangan shkalaga o'giruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func convertTemp(celsius float64, scale string) float64 {
	switch scale {
	case "F", "Fahrenheit":
		return (celsius * 9 / 5) + 32
	case "K", "Kelvin":
		return celsius + 273.15
	default:
		return celsius
	}
}

func main() {
	c := 25.0
	fmt.Printf("%.1f°C = %.1f°F\n", c, convertTemp(c, "F"))
	fmt.Printf("%.1f°C = %.2f K\n", c, convertTemp(c, "K"))
	fmt.Printf("%.1f°C = %.1f°C\n", c, convertTemp(c, "C"))
}
```

## Tushuntirish va Mantiq:
Switch harorat o'lchov birligini aniqlab tegishli matematik formulani qo'llaydi.

## Ishlash natijasi:
```text
25.0°C = 77.0°F
25.0°C = 298.15 K
25.0°C = 25.0°C
```

# 81-Topshiriq: Kredit olish imkoniyatini baholash algoritmi
## Topshiriq sharti:
Oylik daromad, so'ralgan summa va qarz yukiga qarab kredit berish qarorini chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func kreditQarori(oylikDaromad, oylikQarz, talabQilinganKredit float64) string {
	qarzYuki := oylikQarz / oylikDaromad
	oylikTolashQobiliyati := (oylikDaromad - oylikQarz) * 0.5

	if qarzYuki > 0.5 {
		return "Rad etildi: mavjud qarz yuki 50% dan yuqori"
	}

	if talabQilinganKredit/12.0 > oylikTolashQobiliyati {
		return "Rad etildi: oylik to'lov daromadga nisbatan juda katta"
	}

	return "Ma'qullandi"
}

func main() {
	fmt.Println("Mijoz 1:", kreditQarori(10000000, 2000000, 24000000))
	fmt.Println("Mijoz 2:", kreditQarori(8000000, 5000000, 10000000))
}
```

## Tushuntirish va Mantiq:
Kredit skoringida qat'iy ko'rsatkichlar ketma-ket tekshiriladi.

## Ishlash natijasi:
```text
Mijoz 1: Ma'qullandi
Mijoz 2: Rad etildi: mavjud qarz yuki 50% dan yuqori
```

# 82-Topshiriq: Mijoz maqomi va xaridiga qarab chegirma hisoblash
## Topshiriq sharti:
Bronze, Silver, Gold mijozlar va xarid summasiga ko'ra chegirma beruvchi shartlar yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func hisoblaChegirma(maqom string, summa float64) float64 {
	foiz := 0.0

	switch maqom {
	case "Gold":
		foiz = 0.15
	case "Silver":
		foiz = 0.10
	case "Bronze":
		foiz = 0.05
	}

	// Agar summa 1 milliondan oshsa qo'shimcha 5% chegirma:
	if summa > 1000000 {
		foiz += 0.05
	}

	return summa * foiz
}

func main() {
	summa := 1500000.0
	chegirma := hisoblaChegirma("Gold", summa)
	fmt.Printf("Gold mijoz uchun 1,500,000 so'mga chegirma: %.0f so'm (To'lov: %.0f so'm)\n", chegirma, summa-chegirma)
}
```

## Tushuntirish va Mantiq:
Asosiy chegirma switch orqali belgilanadi va xarid miqdoriga ko'ra qo'shimcha if bilan kengaytiriladi.

## Ishlash natijasi:
```text
Gold mijoz uchun 1,500,000 so'mga chegirma: 300000 so'm (To'lov: 1200000 so'm)
```

# 83-Topshiriq: Parol xavfsizligini tekshiruvchi validator
## Topshiriq sharti:
Parolda kamida 8 ta belgi, kamida bitta katta harf va bitta raqam borligini tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unicode"
)

func parolXavfsizmi(parol string) (bool, string) {
	if len(parol) < 8 {
		return false, "Parol uzunligi kamida 8 ta belgi bo'lishi shart"
	}

	kattaHarf, raqam := false, false
	for _, ch := range parol {
		if unicode.IsUpper(ch) {
			kattaHarf = true
		}
		if unicode.IsDigit(ch) {
			raqam = true
		}
	}

	if !kattaHarf {
		return false, "Kamida bitta bosh harf bo'lishi shart"
	}
	if !raqam {
		return false, "Kamida bitta raqam bo'lishi shart"
	}

	return true, "Parol xavfsiz"
}

func main() {
	ok, msg := parolXavfsizmi("GoLang2026")
	fmt.Printf("GoLang2026: %t (%s)\n", ok, msg)

	ok2, msg2 := parolXavfsizmi("pass")
	fmt.Printf("pass: %t (%s)\n", ok2, msg2)
}
```

## Tushuntirish va Mantiq:
Unicode paketidagi `IsUpper` va `IsDigit` yordamida belgilar tahlil qilinadi.

## Ishlash natijasi:
```text
GoLang2026: true (Parol xavfsiz)
pass: false (Parol uzunligi kamida 8 ta belgi bo'lishi shart)
```

# 84-Topshiriq: Email manzilining tuzilishini shartlar orqali tekshirish
## Topshiriq sharti:
Email manzilida `@` belgisi va undan keyin `.` nuqta borligini hamda boshida belgi mavjudligini tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

func emailTogrimi(email string) bool {
	atIndex := strings.Index(email, "@")
	if atIndex <= 0 {
		return false // @ yo'q yoki eng boshida
	}

	dotIndex := strings.LastIndex(email, ".")
	if dotIndex <= atIndex+1 || dotIndex >= len(email)-1 {
		return false // nuqta @ dan keyin emas yoki eng oxirida
	}

	return true
}

func main() {
	fmt.Println("info@google.com:", emailTogrimi("info@google.com"))
	fmt.Println("@notogri.com:", emailTogrimi("@notogri.com"))
	fmt.Println("test@uz:", emailTogrimi("test@uz"))
}
```

## Tushuntirish va Mantiq:
`strings.Index` va `LastIndex` pozitsiyalari tekshirilib qat'iy mantiqiy ifodalar bilan tasdiqlanadi.

## Ishlash natijasi:
```text
info@google.com: true
@notogri.com: false
test@uz: false
```

# 85-Topshiriq: HTTP status kodlarini toifalarga ajratish
## Topshiriq sharti:
HTTP status kodiga qarab (2xx, 3xx, 4xx, 5xx) tegishli xabarni qaytaruvchi switch yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func tahlilHTTP(status int) string {
	switch {
	case status >= 200 && status < 300:
		return "Muvaffaqiyatli (Success)"
	case status >= 300 && status < 400:
		return "Qayta yo'naltirish (Redirection)"
	case status >= 400 && status < 500:
		return "Mijoz xatoligi (Client Error)"
	case status >= 500 && status < 600:
		return "Server xatoligi (Server Error)"
	default:
		return "Noma'lum status kodi"
	}
}

func main() {
	fmt.Println("Status 200:", tahlilHTTP(200))
	fmt.Println("Status 404:", tahlilHTTP(404))
	fmt.Println("Status 502:", tahlilHTTP(502))
}
```

## Tushuntirish va Mantiq:
HTTP protokoli standart kodlari oraliqlari switch orqali toza ifodalanadi.

## Ishlash natijasi:
```text
Status 200: Muvaffaqiyatli (Success)
Status 404: Mijoz xatoligi (Client Error)
Status 502: Server xatoligi (Server Error)
```

# 86-Topshiriq: Valyuta ayirboshlash kalkulyatori
## Topshiriq sharti:
So'mni USD, EUR, RUB va GBP valyutalariga o'giruvchi shartli konvertor yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func konvertatsiyaSom(som float64, valyuta string) (float64, bool) {
	switch valyuta {
	case "USD":
		return som / 12850.0, true
	case "EUR":
		return som / 13900.0, true
	case "RUB":
		return som / 135.0, true
	default:
		return 0, false
	}
}

func main() {
	som := 1285000.0
	if usd, ok := konvertatsiyaSom(som, "USD"); ok {
		fmt.Printf("%.0f so'm = %.2f USD\n", som, usd)
	}
	if eur, ok := konvertatsiyaSom(som, "EUR"); ok {
		fmt.Printf("%.0f so'm = %.2f EUR\n", som, eur)
	}
}
```

## Tushuntirish va Mantiq:
Ko'p qiymat qaytarish (`val, ok`) orqali noma'lum valyutalarni xavfsiz boshqarish ta'minlanadi.

## Ishlash natijasi:
```text
1285000 so'm = 100.00 USD
1285000 so'm = 92.45 EUR
```

# 87-Topshiriq: Shaxmat doskasida katak rangini aniqlash
## Topshiriq sharti:
Ustun ('a'-'h') va satr (1-8) koordinatalari bo'yicha katak oq yoki qora ekanligini aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func katakRangi(ustun rune, satr int) string {
	ustunSon := int(ustun - 'a' + 1)
	if (ustunSon+satr)%2 == 0 {
		return "Qora"
	}
	return "Oq"
}

func main() {
	fmt.Printf("a1: %s\n", katakRangi('a', 1))
	fmt.Printf("e4: %s\n", katakRangi('e', 4))
	fmt.Printf("h8: %s\n", katakRangi('h', 8))
}
```

## Tushuntirish va Mantiq:
Shaxmat doskasida gorizontal va vertikal koordinatalar yig'indisi juft bo'lsa katak qora, toq bo'lsa oq bo'ladi.

## Ishlash natijasi:
```text
a1: Qora
e4: Oq
h8: Qora
```

# 88-Topshiriq: Talabaning GPA ko'rsatkichini hisoblash
## Topshiriq sharti:
Fanlar baholari va kreditlari bo'yicha stipendiya toifasini aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func stipendiyaToifasi(gpa float64) string {
	if gpa >= 4.8 {
		return "Prezident stipendiyasi tavsiyasi"
	} else if gpa >= 4.0 {
		return "A'lo stipendiya"
	} else if gpa >= 3.0 {
		return "Oddiy stipendiya"
	}
	return "Stipendiyasiz"
}

func main() {
	fmt.Println("GPA 4.9:", stipendiyaToifasi(4.9))
	fmt.Println("GPA 4.2:", stipendiyaToifasi(4.2))
	fmt.Println("GPA 2.8:", stipendiyaToifasi(2.8))
}
```

## Tushuntirish va Mantiq:
GPA ko'rsatkichlari bo'yicha qat'iy oraliqlar tekshirilib talabaga mos status beriladi.

## Ishlash natijasi:
```text
GPA 4.9: Prezident stipendiyasi tavsiyasi
GPA 4.2: A'lo stipendiya
GPA 2.8: Stipendiyasiz
```

# 89-Topshiriq: Yil faslini oy raqami bo'yicha aniqlash
## Topshiriq sharti:
1 dan 12 gacha bo'lgan oy raqamiga qarab faslni aniqlovchi switch yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func fasl(oy int) string {
	switch oy {
	case 12, 1, 2:
		return "Qish"
	case 3, 4, 5:
		return "Bahor"
	case 6, 7, 8:
		return "Yoz"
	case 9, 10, 11:
		return "Kuz"
	default:
		return "Noto'g'ri oy raqami"
	}
}

func main() {
	fmt.Printf("4-oy: %s\n", fasl(4))
	fmt.Printf("7-oy: %s\n", fasl(7))
	fmt.Printf("12-oy: %s\n", fasl(12))
}
```

## Tushuntirish va Mantiq:
Guruhlangan case larda oylar fasllarga ajratiladi.

## Ishlash natijasi:
```text
4-oy: Bahor
7-oy: Yoz
12-oy: Qish
```

# 90-Topshiriq: BMI (Tana vazni indeksi) hisoblash va tibbiy tasnif
## Topshiriq sharti:
Vazn (kg) va bo'y (metr) bo'yicha BMI = vazn / bo'y^2 formulasini hisoblang va xulosa bering.

## Yechim (Go kodi):
```go
package main

import "fmt"

func bmiTahlil(vaznKg, boyMetr float64) (float64, string) {
	bmi := vaznKg / (boyMetr * boyMetr)

	var toifa string
	switch {
	case bmi < 18.5:
		toifa = "Vazn yetishmasligi"
	case bmi < 25.0:
		toifa = "Me'yordagi vazn"
	case bmi < 30.0:
		toifa = "Ortiqcha vazn"
	default:
		toifa = "Semizlik"
	}

	return bmi, toifa
}

func main() {
	vazn := 72.0
	boy := 1.78
	bmi, toifa := bmiTahlil(vazn, boy)

	fmt.Printf("Vazn: %.1f kg, Bo'y: %.2f m\n", vazn, boy)
	fmt.Printf("BMI: %.2f - %s\n", bmi, toifa)
}
```

## Tushuntirish va Mantiq:
Jahon Sog'liqni Saqlash Tashkiloti (JSST) mezonlari shartsiz switch orqali qulay modellashtiriladi.

## Ishlash natijasi:
```text
Vazn: 72.0 kg, Bo'y: 1.78 m
BMI: 22.72 - Me'yordagi vazn
```

# 91-Topshiriq: Kun qismini vaqt bo'yicha aniqlash
## Topshiriq sharti:
Soat va daqiqaga qarab kun qismi va salomlashuv matnini chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func salomlashuv(soat int) string {
	switch {
	case soat >= 5 && soat < 11:
		return "Xayrli tong!"
	case soat >= 11 && soat < 17:
		return "Xayrli kun!"
	case soat >= 17 && soat < 22:
		return "Xayrli oqshom!"
	default:
		return "Xayrli tun!"
	}
}

func main() {
	fmt.Println("Soat 08:00 ->", salomlashuv(8))
	fmt.Println("Soat 15:30 ->", salomlashuv(15))
	fmt.Println("Soat 23:15 ->", salomlashuv(23))
}
```

## Tushuntirish va Mantiq:
Vaqt oraliqlari bo'yicha mos tabrik matni tanlanadi.

## Ishlash natijasi:
```text
Soat 08:00 -> Xayrli tong!
Soat 15:30 -> Xayrli kun!
Soat 23:15 -> Xayrli tun!
```

# 92-Topshiriq: IPv4 oktet oralig'ini tekshirish
## Topshiriq sharti:
Oktet qiymati 0 dan 255 gacha oraliqda ekanligini tekshiruvchi shart tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func isValidOctet(oktet int) bool {
	return oktet >= 0 && oktet <= 255
}

func main() {
	fmt.Printf("Oktet 192 to'g'rimi: %t\n", isValidOctet(192))
	fmt.Printf("Oktet 300 to'g'rimi: %t\n", isValidOctet(300))
	fmt.Printf("Oktet -5 to'g'rimi: %t\n", isValidOctet(-5))
}
```

## Tushuntirish va Mantiq:
IPv4 manzilining har bir qismi 8 bit bo'lgani uchun 0 va 255 orasida bo'lishi shart.

## Ishlash natijasi:
```text
Oktet 192 to'g'rimi: true
Oktet 300 to'g'rimi: false
Oktet -5 to'g'rimi: false
```

# 93-Topshiriq: Oy kunlari sonini kabisa yilini inobatga olgan holda hisoblash
## Topshiriq sharti:
Berilgan yil va oy uchun oydagi kunlar sonini aniqlang (Fevral: 28 yoki 29).

## Yechim (Go kodi):
```go
package main

import "fmt"

func oyKunlari(yil, oy int) int {
	switch oy {
	case 1, 3, 5, 7, 8, 10, 12:
		return 31
	case 4, 6, 9, 11:
		return 30
	case 2:
		if (yil%400 == 0) || (yil%4 == 0 && yil%100 != 0) {
			return 29
		}
		return 28
	default:
		return 0
	}
}

func main() {
	fmt.Printf("2024-yil Fevral: %d kun\n", oyKunlari(2024, 2))
	fmt.Printf("2025-yil Fevral: %d kun\n", oyKunlari(2025, 2))
	fmt.Printf("2026-yil Iyul: %d kun\n", oyKunlari(2026, 7))
}
```

## Tushuntirish va Mantiq:
Fevral oyida yil kabisa ekanligi tekshirilib mos ravishda 28 yoki 29 qaytariladi.

## Ishlash natijasi:
```text
2024-yil Fevral: 29 kun
2025-yil Fevral: 28 kun
2026-yil Iyul: 31 kun
```

# 94-Topshiriq: Oddiy arifmetik kalkulyator amallarini bajarish
## Topshiriq sharti:
Operator (`+`, `-`, `*`, `/`) va ikkita son qabul qilib hisoblovchi kalkulyator yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func hisobla(a, b float64, op rune) (float64, error) {
	switch op {
	case '+':
		return a + b, nil
	case '-':
		return a - b, nil
	case '*':
		return a * b, nil
	case '/':
		if b == 0 {
			return 0, fmt.Errorf("nolga bo'lish mumkin emas")
		}
		return a / b, nil
	default:
		return 0, fmt.Errorf("noma'lum amal: %c", op)
	}
}

func main() {
	res1, _ := hisobla(10, 5, '+')
	fmt.Println("10 + 5 =", res1)

	res2, err := hisobla(10, 0, '/')
	if err != nil {
		fmt.Println("Xatolik:", err)
	} else {
		fmt.Println("10 / 0 =", res2)
	}
}
```

## Tushuntirish va Mantiq:
Nolga bo'lish xavfi shart orqali ushlanadi va xatolik obyekti bilan qaytariladi.

## Ishlash natijasi:
```text
10 + 5 = 15
Xatolik: nolga bo'lish mumkin emas
```

# 95-Topshiriq: Guard Clauses (Taqiqlovchi Qoidalar) orqali toza kod yozish
## Topshiriq sharti:
Chuqur qatlamli `if-else` o'rniga kirish parametrlari xatosini boshida qaytaruvchi idiomani qo'llang.

## Yechim (Go kodi):
```go
package main

import (
	"errors"
	"fmt"
)

func pulOtkazish(balans, summa float64, faol bool) (float64, error) {
	// Guard clauses: salbiy holatlarni boshidayoq to'xtatamiz
	if !faol {
		return balans, errors.New("hisob raqam faol emas")
	}
	if summa <= 0 {
		return balans, errors.New("o'tkazma summasi musbat bo'lishi shart")
	}
	if summa > balans {
		return balans, errors.New("balansda yetarli mablag' mavjud emas")
	}

	// Asosiy 'baxtli yo'l' (happy path) to'g'ri chiziqda qoladi
	balans -= summa
	return balans, nil
}

func main() {
	balans, err := pulOtkazish(500000, 150000, true)
	if err != nil {
		fmt.Println("Xatolik:", err)
	} else {
		fmt.Printf("O'tkazma muvaffaqiyatli! Qoldiq balans: %.0f so'm\n", balans)
	}
}
```

## Tushuntirish va Mantiq:
Go falsafasining oltin qoidasi: 'Happy path' (muvaffaqiyatli yo'l) ichki bloklarga kirmay, chap tekislikda qolishi kerak.

## Ishlash natijasi:
```text
O'tkazma muvaffaqiyatli! Qoldiq balans: 350000 so'm
```

# 96-Topshiriq: Rolga asoslangan kirish nazorati (RBAC sodda tekshiruvi)
## Topshiriq sharti:
Foydalanuvchi roli (Admin, Editor, Viewer) bo'yicha ruxsat etilgan amallarni aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func huquqniTekshir(rol, amal string) bool {
	switch rol {
	case "Admin":
		return true // Barcha amallarga ruxsat
	case "Editor":
		return amal == "read" || amal == "write" || amal == "update"
	case "Viewer":
		return amal == "read"
	default:
		return false
	}
}

func main() {
	fmt.Println("Viewer 'read' qila oladimi:", huquqniTekshir("Viewer", "read"))
	fmt.Println("Viewer 'write' qila oladimi:", huquqniTekshir("Viewer", "write"))
	fmt.Println("Editor 'update' qila oladimi:", huquqniTekshir("Editor", "update"))
}
```

## Tushuntirish va Mantiq:
Rol va amallar o'rtasidagi matritsa switch orqali aniq va tushunarli boshqariladi.

## Ishlash natijasi:
```text
Viewer 'read' qila oladimi: true
Viewer 'write' qila oladimi: false
Editor 'update' qila oladimi: true
```

# 97-Topshiriq: strings.HasPrefix va HasSuffix bilan fayl turini tekshirish
## Topshiriq sharti:
Fayl nomi `.go` bilan tugashi va test fayli (`_test.go`) emasligini shart orqali tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

func isPureGoSource(fayl string) bool {
	return strings.HasSuffix(fayl, ".go") && !strings.HasSuffix(fayl, "_test.go")
}

func main() {
	f1 := "main.go"
	f2 := "main_test.go"
	f3 := "notes.txt"

	fmt.Printf("%s Go manba kodimi: %t\n", f1, isPureGoSource(f1))
	fmt.Printf("%s Go manba kodimi: %t\n", f2, isPureGoSource(f2))
	fmt.Printf("%s Go manba kodimi: %t\n", f3, isPureGoSource(f3))
}
```

## Tushuntirish va Mantiq:
`strings.HasSuffix` va `HasPrefix` matnlarning boshi va oxirini tekshirish uchun qulay.

## Ishlash natijasi:
```text
main.go Go manba kodimi: true
main_test.go Go manba kodimi: false
notes.txt Go manba kodimi: false
```

# 98-Topshiriq: Sonning tub ekanligini shartlar bilan aniqlash
## Topshiriq sharti:
Berilgan butun son tub (faqat 1 ga va o'ziga bo'linuvchi) son ekanligini aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func isPrime(n int) bool {
	if n <= 1 {
		return false
	}
	if n <= 3 {
		return true
	}
	if n%2 == 0 || n%3 == 0 {
		return false
	}

	for i := 5; i*i <= n; i += 6 {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
	}
	return true
}

func main() {
	sinovlar := []int{2, 11, 15, 29, 31, 49}
	for _, s := range sinovlar {
		fmt.Printf("%d tub sonmi? -> %t\n", s, isPrime(s))
	}
}
```

## Tushuntirish va Mantiq:
Dastlabki shartlar kichik sonlarni filtrlaydi, 6k±1 qoidasi esa hisoblash tezligini oshiradi.

## Ishlash natijasi:
```text
2 tub sonmi? -> true
11 tub sonmi? -> true
15 tub sonmi? -> false
29 tub sonmi? -> true
31 tub sonmi? -> true
49 tub sonmi? -> false
```

# 99-Topshiriq: Server klasterining sog'lomlik holati (Health Check Status)
## Topshiriq sharti:
CPU, RAM va Disk bandligiga qarab server umumiy statusini aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func serverStatus(cpuFoiz, ramFoiz, diskFoiz float64) string {
	if cpuFoiz > 90.0 || ramFoiz > 90.0 || diskFoiz > 95.0 {
		return "CRITICAL"
	}
	if cpuFoiz > 75.0 || ramFoiz > 75.0 || diskFoiz > 85.0 {
		return "WARNING"
	}
	return "HEALTHY"
}

func main() {
	fmt.Println("Server 1 (CPU: 45%, RAM: 50%, Disk: 60%):", serverStatus(45, 50, 60))
	fmt.Println("Server 2 (CPU: 80%, RAM: 60%, Disk: 70%):", serverStatus(80, 60, 70))
	fmt.Println("Server 3 (CPU: 50%, RAM: 95%, Disk: 40%):", serverStatus(50, 95, 40))
}
```

## Tushuntirish va Mantiq:
DevOps va tizim monitoringida resurslar chegaralari qat'iy tekshiriladi.

## Ishlash natijasi:
```text
Server 1 (CPU: 45%, RAM: 50%, Disk: 60%): HEALTHY
Server 2 (CPU: 80%, RAM: 60%, Disk: 70%): WARNING
Server 3 (CPU: 50%, RAM: 95%, Disk: 40%): CRITICAL
```

# 100-Topshiriq: Murakkab biznes qoidalar matritsasi: Yetkazib berish va promo-kod
## Topshiriq sharti:
Buyurtma summasi, yetkazib berish masofasi va promo-kod bo'yicha yakuniy to'lovni hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func hisoblaBuyurtma(summa, masofaKm float64, promoKod string) float64 {
	yetkazibBerish := 15000.0
	if masofaKm > 10.0 {
		yetkazibBerish += (masofaKm - 10.0) * 1500.0
	}

	// Agar xarid 300,000 dan oshsa yetkazib berish bepul:
	if summa >= 300000.0 {
		yetkazibBerish = 0.0
	}

	chegirma := 0.0
	switch promoKod {
	case "BAHOR2026":
		chegirma = summa * 0.10
	case "VIP":
		chegirma = summa * 0.20
	}

	jami := summa - chegirma + yetkazibBerish
	return jami
}

func main() {
	fmt.Printf("Buyurtma 1: %.0f so'm\n", hisoblaBuyurtma(200000, 12, "BAHOR2026"))
	fmt.Printf("Buyurtma 2 (bepul kuryer): %.0f so'm\n", hisoblaBuyurtma(350000, 15, "VIP"))
}
```

## Tushuntirish va Mantiq:
Haqiqiy elektron tijorat qoidalarida shartlar kombinatsiyasi orqali yakuniy hisob-kitob amalga oshiriladi.

## Ishlash natijasi:
```text
Buyurtma 1: 198000 so'm
Buyurtma 2 (bepul kuryer): 280000 so'm
```

