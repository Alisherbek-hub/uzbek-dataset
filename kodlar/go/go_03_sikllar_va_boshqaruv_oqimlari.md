# 3-Mavzu: Sikllar va Boshqaruv Oqimlari (101-150)

Go tilida takrorlanishlar faqat `for` kalit so'zi orqali amalga oshiriladi (klassik 3-qismli, while-uslubidagi, cheksiz `for`), Go 1.22 dagi yangi `range int` imkoniyati, `break`, `continue`, belgilangan (labeled) sakrashlar, `goto` va amaliy algoritmlar bo'yicha 50 ta mukammal topshiriq.

# 101-Topshiriq: Go tilida takrorlanishlarning yagona operatori: for
## Topshiriq sharti:
1 dan 5 gacha bo'lgan sonlarni klassik `for` yordamida ekranga chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	for i := 1; i <= 5; i++ {
		fmt.Printf("Qadam: %d\n", i)
	}
}
```

## Tushuntirish va Mantiq:
Go tilida `while` yoki `do-while` kalit so'zlari yo'q. Barcha takrorlanishlar faqat `for` orqali amalga oshiriladi.

## Ishlash natijasi:
```text
Qadam: 1
Qadam: 2
Qadam: 3
Qadam: 4
Qadam: 5
```

# 102-Topshiriq: Klassik 3-qismli for sikli (init; condition; post)
## Topshiriq sharti:
10 dan 0 gacha 2 qadam bilan kamayib boruvchi sikl yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	for i := 10; i >= 0; i -= 2 {
		fmt.Printf("%d ", i)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Klassik `for` uch qismdan iborat: initsializatsiya (`i := 10`), shart (`i >= 0`) va qadam (`i -= 2`).

## Ishlash natijasi:
```text
10 8 6 4 2 0
```

# 103-Topshiriq: while uslubidagi for sikli (faqat shartli for)
## Topshiriq sharti:
Boshqa tillardagi `while (n < 100)` kabi ishlaydigan faqat shartdan iborat `for` yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	son := 1

	for son < 100 {
		son *= 2
		fmt.Printf("Joriy qiymat: %d\n", son)
	}
}
```

## Tushuntirish va Mantiq:
Go da `init` va `post` qismlarini tashlab ketish orqali toza `while` sikli hosil qilinadi: `for shart { ... }`.

## Ishlash natijasi:
```text
Joriy qiymat: 2
Joriy qiymat: 4
Joriy qiymat: 8
Joriy qiymat: 16
Joriy qiymat: 32
Joriy qiymat: 64
Joriy qiymat: 128
```

# 104-Topshiriq: Cheksiz for sikli va break bilan to'xtatish
## Topshiriq sharti:
`for { ... }` cheksiz siklidan berilgan shart bajarilganda `break` orqali chiqing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	hisoblagich := 0

	for {
		hisoblagich++
		if hisoblagich == 4 {
			fmt.Println("To'xtash nuqtasiga yetdi (break)")
			break
		}
		fmt.Printf("Hisob: %d\n", hisoblagich)
	}
}
```

## Tushuntirish va Mantiq:
`for {}` hech qanday shartsiz cheksiz davom etadi. Dasturdan chiqish faqat `break`, `return` yoki `panic` orqali bo'ladi.

## Ishlash natijasi:
```text
Hisob: 1
Hisob: 2
Hisob: 3
To'xtash nuqtasiga yetdi (break)
```

# 105-Topshiriq: continue operatori bilan joriy iteratsiyani tashlab o'tish
## Topshiriq sharti:
1 dan 10 gacha bo'lgan sonlardan faqat toqlarini `continue` orqali chop eting.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	for i := 1; i <= 10; i++ {
		if i%2 == 0 {
			continue // Juft sonlarni tashlab o'tamiz
		}
		fmt.Printf("%d ", i)
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
`continue` siklning joriy qadamidagi qolgan amallarni o'tkazib yuborib, darhol keyingi iteratsiyaga o'tadi.

## Ishlash natijasi:
```text
1 3 5 7 9
```

# 106-Topshiriq: Go 1.22 yangiligi: Butun sonlar ustida range (for i := range N)
## Topshiriq sharti:
Go 1.22 talqini bilan kiritilgan `range N` imkoniyati orqali 0 dan 4 gacha siklni ixcham yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	// Go 1.22+ sintaksisi
	for i := range 5 {
		fmt.Printf("Indeks: %d\n", i)
	}
}
```

## Tushuntirish va Mantiq:
Go 1.22 dan boshlab `for i := range N` sintaksisi qo'llab-quvvatlanadi. U 0 dan N-1 gacha qulay takrorlanish beradi.

## Ishlash natijasi:
```text
Indeks: 0
Indeks: 1
Indeks: 2
Indeks: 3
Indeks: 4
```

# 107-Topshiriq: Go 1.22 Loop Variable Scoping o'zgarishi
## Topshiriq sharti:
Goroutine yoki closure larda avvalgi Go versiyalaridagi sikl o'zgaruvchisi xatosining Go 1.22 da qanday bartaraf qilinganini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var funksiyalar []func()

	for i := 1; i <= 3; i++ {
		// Go 1.22 da har bir iteratsiya yangi 'i' o'zgaruvchisiga ega
		funksiyalar = append(funksiyalar, func() {
			fmt.Printf("Qiymat: %d\n", i)
		})
	}

	for _, f := range funksiyalar {
		f()
	}
}
```

## Tushuntirish va Mantiq:
Go 1.22 ga qadar sikl o'zgaruvchisi bitta xotira manzilida turgan va closure larda oxirgi qiymat (3 3 3) chiqardi. Go 1.22 dan boshlab har bir iteratsiya uchun yangi nusxa yaratiladi (1 2 3).

## Ishlash natijasi:
```text
Qiymat: 1
Qiymat: 2
Qiymat: 3
```

# 108-Topshiriq: Satr ustida for range (indeks va rune ajratib olish)
## Topshiriq sharti:
O'zbekcha 'Salom' satri ustida `range` yordamida har bir harfning bayt indeksi va Unicode belgilarini chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	matn := "G'olib"

	for baytIndex, belgi := range matn {
		fmt.Printf("Bayt indeksi: %d -> Belgi: %c (Unicode: %U)\n", baytIndex, belgi, belgi)
	}
}
```

## Tushuntirish va Mantiq:
`for idx, ch := range str` satrni UTF-8 runelar bo'yicha dekodlaydi va harflarning haqiqiy bayt siljishini beradi.

## Ishlash natijasi:
```text
Bayt indeksi: 0 -> Belgi: G (Unicode: U+0047)
Bayt indeksi: 1 -> Belgi: ' (Unicode: U+0027)
Bayt indeksi: 2 -> Belgi: o (Unicode: U+006F)
Bayt indeksi: 3 -> Belgi: l (Unicode: U+006C)
Bayt indeksi: 4 -> Belgi: i (Unicode: U+0069)
Bayt indeksi: 5 -> Belgi: b (Unicode: U+0062)
```

# 109-Topshiriq: Satr ustida klassik baytma-bayt sikl
## Topshiriq sharti:
`for i := 0; i < len(s); i++` orqali satrning xom baytlarini o'qing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	s := "Go!"

	for i := 0; i < len(s); i++ {
		fmt.Printf("%d-bayt: %d ('%c')\n", i, s[i], s[i])
	}
}
```

## Tushuntirish va Mantiq:
Satrni indekslash (`s[i]`) faqat 1 baytni qaytaradi. Agar belgi ko'p baytli bo'lsa (kirill, emoji), u noto'g'ri kesiladi.

## Ishlash natijasi:
```text
0-bayt: 71 ('G')
1-bayt: 111 ('o')
2-bayt: 33 ('!')
```

# 110-Topshiriq: Slice ustida for range bilan indeks va qiymatni olish
## Topshiriq sharti:
Shaharlar ro'yxatini indekslari bilan birga chiroyli tartibda chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	shaharlar := []string{"Samarqand", "Buxoro", "Xiva", "Toshkent"}

	for idx, shahar := range shaharlar {
		fmt.Printf("%d) %s\n", idx+1, shahar)
	}
}
```

## Tushuntirish va Mantiq:
`range slice` birinchi qiymatda indeksni (0 dan boshlab), ikkinchisida element nusxasini qaytaradi.

## Ishlash natijasi:
```text
1) Samarqand
2) Buxoro
3) Xiva
4) Toshkent
```

# 111-Topshiriq: range da indeksni tashlab ketish (faqat qiymat bilan ishlash)
## Topshiriq sharti:
Massivdagi barcha sonlarning yig'indisini hisoblashda indeksni `_` orqali inkor qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	sonlar := []int{10, 20, 30, 40, 50}
	yigindi := 0

	for _, qiymat := range sonlar {
		yigindi += qiymat
	}

	fmt.Println("Jami yig'indi:", yigindi)
}
```

## Tushuntirish va Mantiq:
Agar indeks kerak bo'lmasa, `for _, v := range` orqali ortiqcha o'zgaruvchilardan qochiladi.

## Ishlash natijasi:
```text
Jami yig'indi: 150
```

# 112-Topshiriq: range da faqat indeksni olish
## Topshiriq sharti:
Slice o'lchamini bilgan holda faqat uning indekslari bo'yicha yuring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ballar := []int{85, 92, 78}

	for i := range ballar {
		ballar[i] += 5 // To'g'ridan-to'g'ri asl elementni o'zgartiramiz
	}

	fmt.Println("Oshirilgan ballar:", ballar)
}
```

## Tushuntirish va Mantiq:
Faqat `for i := range slice` yozilsa, Go faqat indeksni beradi. Bu elementni to'g'ridan-to'g'ri o'zgartirish uchun qulay.

## Ishlash natijasi:
```text
Oshirilgan ballar: [90 97 83]
```

# 113-Topshiriq: Map ustida for range takrorlanishi
## Topshiriq sharti:
Lug'at (map) ichidagi kalit-qiymat juftliklarini siklda aylanib chiqing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	kurslar := map[string]int{
		"USD": 12850,
		"EUR": 13900,
	}

	for valyuta, kurs := range kurslar {
		fmt.Printf("%s kursi: %d so'm\n", valyuta, kurs)
	}
}
```

## Tushuntirish va Mantiq:
Map ustida `for range` qilinganda elementlar tasodifiy tartibda chiqadi (Go map iteratsiyasi qasddan deterministik emas).

## Ishlash natijasi:
```text
USD kursi: 12850 so'm
EUR kursi: 13900 so'm
```

# 114-Topshiriq: Kanal (Channel) ustida for range takrorlanishi
## Topshiriq sharti:
Kanalga yuborilgan ma'lumotlarni u yopilgunga qadar `for range` orqali qabul qilib oling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	ch := make(chan int, 3)
	ch <- 100
	ch <- 200
	ch <- 300
	close(ch) // Kanal yopilishi shart, aks holda deadlock bo'ladi

	for qiymat := range ch {
		fmt.Println("Kanaldan o'qildi:", qiymat)
	}
}
```

## Tushuntirish va Mantiq:
`for v := range ch` kanaldan ma'lumotlarni ketma-ket o'qiydi va kanal yopilgach (`close`) siklni avtomatik to'xtatadi.

## Ishlash natijasi:
```text
Kanaldan o'qildi: 100
Kanaldan o'qildi: 200
Kanaldan o'qildi: 300
```

# 115-Topshiriq: Ichma-ich (Nested) for sikllari va ko'paytirish jadvali
## Topshiriq sharti:
Ichma-ich joylashgan ikki for sikli yordamida 3x3 ko'paytirish jadvalini chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	for i := 1; i <= 3; i++ {
		for j := 1; j <= 3; j++ {
			fmt.Printf("%d * %d = %-2d  ", i, j, i*j)
		}
		fmt.Println()
	}
}
```

## Tushuntirish va Mantiq:
Tashqi sikl har bir qator uchun, ichki sikl esa shu qatordagi ustunlar uchun javob beradi.

## Ishlash natijasi:
```text
1 * 1 = 1   1 * 2 = 2   1 * 3 = 3   
2 * 1 = 2   2 * 2 = 4   2 * 3 = 6   
3 * 1 = 3   3 * 2 = 6   3 * 3 = 9
```

# 116-Topshiriq: Belgilangan break (Labeled Break) bilan tashqi sikldan chiqish
## Topshiriq sharti:
Ichma-ich sikllarda qidirilayotgan qiymat topilganda darhol barcha sikllarni to'xtatish uchun Label qo'llang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	matritsa := [][]int{
		{1, 2, 3},
		{4, 55, 6},
		{7, 8, 9},
	}

	qidiruv := 55

TashqiSikl:
	for i, qator := range matritsa {
		for j, son := range qator {
			if son == qidiruv {
				fmt.Printf("Topildi: %d! Koordinatasi: [%d][%d]\n", son, i, j)
				break TashqiSikl // Tashqi siklni ham birdan to'xtatadi
			}
		}
	}
	fmt.Println("Qidiruv yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Oddiy `break` faqat o'zi turgan eng yaqin ichki siklni to'xtatadi. `break Label` esa belgilangan tashqi siklni darhol yakunlaydi.

## Ishlash natijasi:
```text
Topildi: 55! Koordinatasi: [1][1]
Qidiruv yakunlandi.
```

# 117-Topshiriq: Belgilangan continue (Labeled Continue) bilan tashqi iteratsiyaga o'tish
## Topshiriq sharti:
Ichki shart bajarilganda darhol tashqi siklning keyingi qadamiga sakrang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
KeyingiQator:
	for qator := 1; qator <= 3; qator++ {
		for ustun := 1; ustun <= 3; ustun++ {
			if ustun == 2 {
				fmt.Printf("[Qator %d da ustun 2 tashlab ketildi]\n", qator)
				continue KeyingiQator
			}
			fmt.Printf("(%d,%d) ", qator, ustun)
		}
		fmt.Println()
	}
}
```

## Tushuntirish va Mantiq:
`continue Label` tashqi siklning navbatdagi iteratsiyasiga darhol o'tkazadi.

## Ishlash natijasi:
```text
(1,1) [Qator 1 da ustun 2 tashlab ketildi]
(2,1) [Qator 2 da ustun 2 tashlab ketildi]
(3,1) [Qator 3 da ustun 2 tashlab ketildi]
```

# 118-Topshiriq: goto operatori va uning qo'llanilishi
## Topshiriq sharti:
`goto` orqali to'g'ridan-to'g'ri belgilangan nishonga sakrash va xatolikdan tozalash bloki.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	i := 0

Nishon:
	if i < 3 {
		fmt.Printf("i = %d\n", i)
		i++
		goto Nishon
	}

	fmt.Println("goto sikli muvaffaqiyatli tugadi.")
}
```

## Tushuntirish va Mantiq:
Go tilida `goto` mavjud, lekin u yangi e'lon qilingan o'zgaruvchilarni chetlab o'ta olmaydi. Odatda faqat murakkab xatolik tozalashlarida ishlatiladi.

## Ishlash natijasi:
```text
i = 0
i = 1
i = 2
goto sikli muvaffaqiyatli tugadi.
```

# 119-Topshiriq: 1 dan N gacha bo'lgan sonlar yig'indisini for bilan hisoblash
## Topshiriq sharti:
N = 100 gacha sonlar yig'indisini for sikli orqali hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	n := 100
	yigindi := 0

	for i := 1; i <= n; i++ {
		yigindi += i
	}

	fmt.Printf("1 dan %d gacha sonlar yig'indisi: %d\n", n, yigindi)
}
```

## Tushuntirish va Mantiq:
Sikl har bir qadamda `i` ni akkumulyator o'zgaruvchiga qo'shib boradi.

## Ishlash natijasi:
```text
1 dan 100 gacha sonlar yig'indisi: 5050
```

# 120-Topshiriq: Faktorialni iterativ for sikli bilan hisoblash
## Topshiriq sharti:
N sonining faktorialini (`N! = 1 * 2 * ... * N`) hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func factorial(n int) uint64 {
	var natija uint64 = 1
	for i := 1; i <= n; i++ {
		natija *= uint64(i)
	}
	return natija
}

func main() {
	for i := 1; i <= 6; i++ {
		fmt.Printf("%d! = %d\n", i, factorial(i))
	}
}
```

## Tushuntirish va Mantiq:
Iterativ faktorial hisoblash xotira stekini tejaydi va rekursiyadan tezroq ishlaydi.

## Ishlash natijasi:
```text
1! = 1
2! = 2
3! = 6
4! = 24
5! = 120
6! = 720
```

# 121-Topshiriq: Fibonachchi sonlari ketma-ketligini for orqali generatsiya qilish
## Topshiriq sharti:
Dastlabki 10 ta Fibonachchi sonini chop eting (0, 1, 1, 2, 3, 5, ...).

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	n := 10
	a, b := 0, 1

	fmt.Printf("Dastlabki %d ta Fibonachchi soni: ", n)
	for i := 0; i < n; i++ {
		fmt.Printf("%d ", a)
		a, b = b, a+b
	}
	fmt.Println()
}
```

## Tushuntirish va Mantiq:
Go ning `a, b = b, a+b` parallel o'zlashtirishi Fibonachchi ketma-ketligini bir qatorda yozishga imkon beradi.

## Ishlash natijasi:
```text
Dastlabki 10 ta Fibonachchi soni: 0 1 1 2 3 5 8 13 21 34
```

# 122-Topshiriq: Berilgan sonning barcha bo'luvchilarini topish
## Topshiriq sharti:
Butun sonning barcha qoldiqsiz bo'luvchilarini for orqali aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func boluvchilari(n int) []int {
	var res []int
	for i := 1; i <= n; i++ {
		if n%i == 0 {
			res = append(res, i)
		}
	}
	return res
}

func main() {
	son := 36
	fmt.Printf("%d sonining bo'luvchilari: %v\n", son, boluvchilari(son))
}
```

## Tushuntirish va Mantiq:
1 dan N gacha har bir son tekshirilib, qoldiq 0 bo'lganda natijaga qo'shiladi.

## Ishlash natijasi:
```text
36 sonining bo'luvchilari: [1 2 3 4 6 9 12 18 36]
```

# 123-Topshiriq: Sonning raqamlar yig'indisini hisoblash
## Topshiriq sharti:
Butun sonning raqamlari yig'indisini while-for sikli orqali toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

func raqamlarYigindisi(n int) int {
	yigindi := 0
	for n > 0 {
		yigindi += n % 10 // Oxirgi raqamni olish
		n /= 10           // Oxirgi raqamni o'chirish
	}
	return yigindi
}

func main() {
	son := 4892
	fmt.Printf("%d ning raqamlar yig'indisi: %d\n", son, raqamlarYigindisi(son))
}
```

## Tushuntirish va Mantiq:
10 ga bo'lgandagi qoldiq oxirgi raqamni beradi, 10 ga butun bo'lish esa sonni 1 ta raqamga qisqartiradi.

## Ishlash natijasi:
```text
4892 ning raqamlar yig'indisi: 23
```

# 124-Topshiriq: Sonni teskari o'girish (masalan 12345 -> 54321)
## Topshiriq sharti:
Butun sonni matematik amallar orqali teskarisiga aylantiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func teskariSon(n int) int {
	teskari := 0
	for n > 0 {
		oxirgi := n % 10
		teskari = teskari*10 + oxirgi
		n /= 10
	}
	return teskari
}

func main() {
	son := 12345
	fmt.Printf("%d teskarisi: %d\n", son, teskariSon(son))
}
```

## Tushuntirish va Mantiq:
Teskari son har qadamda 10 ga ko'paytirilib yangi oxirgi raqam qo'shiladi.

## Ishlash natijasi:
```text
12345 teskarisi: 54321
```

# 125-Topshiriq: Palindrom sonni aniqlash
## Topshiriq sharti:
Son o'ngdan ham, chapdan ham bir xil o'qilishini (palindrom) tekshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func isPalindrome(n int) bool {
	if n < 0 {
		return false
	}
	asl, teskari := n, 0
	for n > 0 {
		teskari = teskari*10 + (n % 10)
		n /= 10
	}
	return asl == teskari
}

func main() {
	fmt.Println("121 palindrommi:", isPalindrome(121))
	fmt.Println("12321 palindrommi:", isPalindrome(12321))
	fmt.Println("12345 palindrommi:", isPalindrome(12345))
}
```

## Tushuntirish va Mantiq:
Asl son bilan uning teskarisi teng bo'lsa u palindrom hisoblanadi.

## Ishlash natijasi:
```text
121 palindrommi: true
12321 palindrommi: true
12345 palindrommi: false
```

# 126-Topshiriq: Berilgan oraliqdagi barcha tub sonlarni topish (Eratosfen g'alviri)
## Topshiriq sharti:
N = 30 gacha bo'lgan barcha tub sonlarni g'alvir algoritmi orqali toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

func eratosfen(n int) []int {
	tub := make([]bool, n+1)
	for i := 2; i <= n; i++ {
		tub[i] = true
	}

	for p := 2; p*p <= n; p++ {
		if tub[p] {
			for i := p * p; i <= n; i += p {
				tub[i] = false
			}
		}
	}

	var natija []int
	for i := 2; i <= n; i++ {
		if tub[i] {
			natija = append(natija, i)
		}
	}
	return natija
}

func main() {
	fmt.Println("30 gacha tub sonlar:", eratosfen(30))
}
```

## Tushuntirish va Mantiq:
Eratosfen g'alviri murakkab sonlarni ularning karralilari orqali elaydi va juda tezkor natija beradi.

## Ishlash natijasi:
```text
30 gacha tub sonlar: [2 3 5 7 11 13 17 19 23 29]
```

# 127-Topshiriq: Eng Katta Umumiy Bo'luvchi (EKUB / GCD) - Evklid algoritmi
## Topshiriq sharti:
Ikki sonning EKUB qiymatini for sikli orqali hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ekub(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func main() {
	fmt.Printf("EKUB(48, 18) = %d\n", ekub(48, 18))
	fmt.Printf("EKUB(100, 25) = %d\n", ekub(100, 25))
}
```

## Tushuntirish va Mantiq:
Evklid algoritmi qoldiq 0 bo'lgunga qadar `a, b = b, a%b` almashtirishini davom ettiradi.

## Ishlash natijasi:
```text
EKUB(48, 18) = 6
EKUB(100, 25) = 25
```

# 128-Topshiriq: Eng Kichik Umumiy Karrali (EKUK / LCM)
## Topshiriq sharti:
EKUB orqali ikki sonning EKUK qiymatini hisoblang: `EKUK(a, b) = (a * b) / EKUB(a, b)`.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ekub(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func ekuk(a, b int) int {
	return (a * b) / ekub(a, b)
}

func main() {
	fmt.Printf("EKUK(12, 18) = %d\n", ekuk(12, 18))
	fmt.Printf("EKUK(15, 20) = %d\n", ekuk(15, 20))
}
```

## Tushuntirish va Mantiq:
EKUK har ikkala songa qoldiqsiz bo'linadigan eng kichik musbat sondir.

## Ishlash natijasi:
```text
EKUK(12, 18) = 36
EKUK(15, 20) = 60
```

# 129-Topshiriq: Yulduzchalar (*) bilan piramida shaklini chizish
## Topshiriq sharti:
N qavatli simmetrik piramidani ichma-ich for sikllari orqali konsolga chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func piramida(qavatlar int) {
	for i := 1; i <= qavatlar; i++ {
		// Bo'sh joylar
		for j := 1; j <= qavatlar-i; j++ {
			fmt.Print(" ")
		}
		// Yulduzchalar (2*i - 1)
		for k := 1; k <= 2*i-1; k++ {
			fmt.Print("*")
		}
		fmt.Println()
	}
}

func main() {
	piramida(4)
}
```

## Tushuntirish va Mantiq:
Piramida qavati uchun oldingi bo'shliqlar va yulduzchalar soni matematik formula bo'yicha chiqariladi.

## Ishlash natijasi:
```text
*
  ***
 *****
*******
```

# 130-Topshiriq: Teskari to'g'ri burchakli uchburchak chizish
## Topshiriq sharti:
5 qatorli kamayib boruvchi yulduzchalar uchburchagini chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	n := 5
	for i := n; i >= 1; i-- {
		for j := 1; j <= i; j++ {
			fmt.Print("*")
		}
		fmt.Println()
	}
}
```

## Tushuntirish va Mantiq:
Tashqi sikl 5 dan 1 gacha kamayib boradi, ichki sikl esa shuncha yulduzcha chiqaradi.

## Ishlash natijasi:
```text
*****
****
***
**
*
```

# 131-Topshiriq: Romb (Diamond) shaklini konsolga chizish
## Topshiriq sharti:
Yuqori va pastki qismlardan iborat 7 qatorli romb shaklini yasang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	n := 3 // Yarim balandlik

	// Yuqori qism
	for i := 0; i <= n; i++ {
		for j := 0; j < n-i; j++ {
			fmt.Print(" ")
		}
		for k := 0; k < 2*i+1; k++ {
			fmt.Print("*")
		}
		fmt.Println()
	}

	// Pastki qism
	for i := n - 1; i >= 0; i-- {
		for j := 0; j < n-i; j++ {
			fmt.Print(" ")
		}
		for k := 0; k < 2*i+1; k++ {
			fmt.Print("*")
		}
		fmt.Println()
	}
}
```

## Tushuntirish va Mantiq:
Romb piramida va teskari piramidaning birlashmasidan hosil bo'ladi.

## Ishlash natijasi:
```text
*
  ***
 *****
*******
 *****
  ***
   *
```

# 132-Topshiriq: Paskal uchburchagini generatsiya qilish
## Topshiriq sharti:
N = 5 qatordan iborat Paskal uchburchagini massiv va for orqali hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func paskal(n int) [][]int {
	uchburchak := make([][]int, n)

	for i := 0; i < n; i++ {
		uchburchak[i] = make([]int, i+1)
		uchburchak[i][0] = 1
		uchburchak[i][i] = 1

		for j := 1; j < i; j++ {
			uchburchak[i][j] = uchburchak[i-1][j-1] + uchburchak[i-1][j]
		}
	}
	return uchburchak
}

func main() {
	res := paskal(5)
	for _, qator := range res {
		fmt.Println(qator)
	}
}
```

## Tushuntirish va Mantiq:
Paskal uchburchagida har bir son yuqorisidagi ikki sonning yig'indisiga teng.

## Ishlash natijasi:
```text
[1]
[1 1]
[1 2 1]
[1 3 3 1]
[1 4 6 4 1]
```

# 133-Topshiriq: Matndagi unli harflarni sanash
## Topshiriq sharti:
O'zbek tilidagi matndan unli harflar (a, e, i, o, u, o') sonini `for range` orqali sanang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
)

func unlilarSoni(matn string) int {
	unlilar := "aeiouo'AEIOUO'"
	hisob := 0

	for _, ch := range matn {
		if strings.ContainsRune(unlilar, ch) {
			hisob++
		}
	}
	return hisob
}

func main() {
	gap := "Dasturlash - kelajak kasbi"
	fmt.Printf("%q matnidagi unlilar: %d ta\n", gap, unlilarSoni(gap))
}
```

## Tushuntirish va Mantiq:
`strings.ContainsRune` har bir belgi unlilar to'plamiga kirishini tekshiradi.

## Ishlash natijasi:
```text
"Dasturlash - kelajak kasbi" matnidagi unlilar: 8 ta
```

# 134-Topshiriq: Matndagi har bir so'zning uzunligini hisoblash
## Topshiriq sharti:
`strings.Fields` orqali so'zlarga ajratib, har bir so'z uzunligini chiqaring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"strings"
	"unicode/utf8"
)

func main() {
	satr := "Go juda tez va o'rganishga oson"
	sozlar := strings.Fields(satr)

	for _, soz := range sozlar {
		harflar := utf8.RuneCountInString(soz)
		fmt.Printf("So'z: %-12s | Uzunligi: %d\n", soz, harflar)
	}
}
```

## Tushuntirish va Mantiq:
`strings.Fields` bo'shliqlar bo'yicha matnni ajratadi, `utf8.RuneCountInString` esa belgilar sonini to'g'ri o'lchaydi.

## Ishlash natijasi:
```text
So'z: Go           | Uzunligi: 2
So'z: juda         | Uzunligi: 4
So'z: tez          | Uzunligi: 3
So'z: va           | Uzunligi: 2
So'z: o'rganishga  | Uzunligi: 11
So'z: oson         | Uzunligi: 4
```

# 135-Topshiriq: Binar qidiruv (Binary Search) algoritmi for sikli orqali
## Topshiriq sharti:
Saralangan massivda elementni O(log N) tezlikda binar qidiruv bilan toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

func binarQidiruv(arr []int, maqsad int) int {
	chap := 0
	ong := len(arr) - 1

	for chap <= ong {
		orta := chap + (ong-chap)/2

		if arr[orta] == maqsad {
			return orta // Topilgan indeks
		}
		if arr[orta] < maqsad {
			chap = orta + 1
		} else {
			ong = orta - 1
		}
	}
	return -1 // Topilmadi
}

func main() {
	sonlar := []int{2, 5, 8, 12, 16, 23, 38, 56, 72, 91}
	idx := binarQidiruv(sonlar, 23)
	fmt.Printf("23 soni indeksi: %d\n", idx)

	idx2 := binarQidiruv(sonlar, 100)
	fmt.Printf("100 soni indeksi: %d\n", idx2)
}
```

## Tushuntirish va Mantiq:
Binar qidiruv har bir qadamda qidiruv sohasini ikkiga qisqartiradi.

## Ishlash natijasi:
```text
23 soni indeksi: 5
100 soni indeksi: -1
```

# 136-Topshiriq: Chiziqli qidiruv (Linear Search) va element indeksini topish
## Topshiriq sharti:
Tartiblanmagan ro'yxatda birinchi uchragan element indeksini qaytaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func chiziqliQidiruv(arr []string, kalit string) int {
	for i, v := range arr {
		if v == kalit {
			return i
		}
	}
	return -1
}

func main() {
	mevalar := []string{"olma", "banan", "anor", "anjir"}
	fmt.Println("'anor' indeksi:", chiziqliQidiruv(mevalar, "anor"))
	fmt.Println("'shaftoli' indeksi:", chiziqliQidiruv(mevalar, "shaftoli"))
}
```

## Tushuntirish va Mantiq:
Chiziqli qidiruv massivni boshidan oxirigacha O(N) vaqtda ketma-ket ko'rib chiqadi.

## Ishlash natijasi:
```text
'anor' indeksi: 2
'shaftoli' indeksi: -1
```

# 137-Topshiriq: Pufakchali saralash (Bubble Sort) algoritmi
## Topshiriq sharti:
Massivni o'sish tartibida pufakchali saralash orqali tartiblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func bubbleSort(arr []int) {
	n := len(arr)
	for i := 0; i < n-1; i++ {
		almashdimi := false
		for j := 0; j < n-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
				almashdimi = true
			}
		}
		if !almashdimi {
			break // Allaqachon tartiblangan bo'lsa to'xtash
		}
	}
}

func main() {
	sonlar := []int{64, 34, 25, 12, 22, 11, 90}
	fmt.Println("Oldin:", sonlar)
	bubbleSort(sonlar)
	fmt.Println("Keyin:", sonlar)
}
```

## Tushuntirish va Mantiq:
Katta elementlar ketma-ket qo'shnilari bilan almashib massiv oxiriga 'qalqib' chiqadi.

## Ishlash natijasi:
```text
Oldin: [64 34 25 12 22 11 90]
Keyin: [11 12 22 25 34 64 90]
```

# 138-Topshiriq: Tanlash orqali saralash (Selection Sort) algoritmi
## Topshiriq sharti:
Har bir qadamda qolgan qismning eng kichigini topib boshiga qo'yuvchi saralash.

## Yechim (Go kodi):
```go
package main

import "fmt"

func selectionSort(arr []int) {
	n := len(arr)
	for i := 0; i < n-1; i++ {
		minIdx := i
		for j := i + 1; j < n; j++ {
			if arr[j] < arr[minIdx] {
				minIdx = j
			}
		}
		arr[i], arr[minIdx] = arr[minIdx], arr[i]
	}
}

func main() {
	sonlar := []int{29, 10, 14, 37, 13}
	selectionSort(sonlar)
	fmt.Println("Tartiblangan:", sonlar)
}
```

## Tushuntirish va Mantiq:
Selection sort har bir iteratsiyada eng kichik element indeksini aniqlab bitta almashtirish bajaradi.

## Ishlash natijasi:
```text
Tartiblangan: [10 13 14 29 37]
```

# 139-Topshiriq: Qo'shish orqali saralash (Insertion Sort) algoritmi
## Topshiriq sharti:
Karta o'yinidagi tartiblashga o'xshash qistirib qo'yish saralashini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func insertionSort(arr []int) {
	for i := 1; i < len(arr); i++ {
		kalit := arr[i]
		j := i - 1

		for j >= 0 && arr[j] > kalit {
			arr[j+1] = arr[j]
			j--
		}
		arr[j+1] = kalit
	}
}

func main() {
	sonlar := []int{12, 11, 13, 5, 6}
	insertionSort(sonlar)
	fmt.Println("Tartiblangan:", sonlar)
}
```

## Tushuntirish va Mantiq:
Insertion sort kichik hajmdagi yoki qisman tartiblangan massivlarda juda yuqori samaradorlik ko'rsatadi.

## Ishlash natijasi:
```text
Tartiblangan: [5 6 11 12 13]
```

# 140-Topshiriq: Ikki massivning umumiy elementlarini (kesishmasini) topish
## Topshiriq sharti:
Ikkita massivda bir vaqtning o'zida qatnashgan elementlarni ajratib oling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func kesishma(a, b []int) []int {
	mavjud := make(map[int]bool)
	for _, x := range a {
		mavjud[x] = true
	}

	var natija []int
	for _, y := range b {
		if mavjud[y] {
			natija = append(natija, y)
			delete(mavjud, y) // Bir marta qo'shish uchun
		}
	}
	return natija
}

func main() {
	m1 := []int{1, 2, 3, 4, 5}
	m2 := []int{3, 4, 5, 6, 7}
	fmt.Println("Umumiy elementlar:", kesishma(m1, m2))
}
```

## Tushuntirish va Mantiq:
Map yordamida birinchi massiv O(N) vaqtda xotiralanadi va ikkinchi massiv O(M) da tekshiriladi.

## Ishlash natijasi:
```text
Umumiy elementlar: [3 4 5]
```

# 141-Topshiriq: Massiv elementlarini joyida teskari o'girish (In-Place Reverse)
## Topshiriq sharti:
Qo'shimcha massiv ajratmasdan, ikki ko'rsatkich (two-pointers) usuli bilan massivni teskarisiga aylantiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func reverseSlice(arr []int) {
	for chap, ong := 0, len(arr)-1; chap < ong; chap, ong = chap+1, ong-1 {
		arr[chap], arr[ong] = arr[ong], arr[chap]
	}
}

func main() {
	sonlar := []int{1, 2, 3, 4, 5, 6}
	fmt.Println("Asl holat:", sonlar)
	reverseSlice(sonlar)
	fmt.Println("Teskari holat:", sonlar)
}
```

## Tushuntirish va Mantiq:
Ikki tomonlama ko'rsatkichlar o'rtaga qarab harakatlanib elementlarni o'zaro almashtiradi.

## Ishlash natijasi:
```text
Asl holat: [1 2 3 4 5 6]
Teskari holat: [6 5 4 3 2 1]
```

# 142-Topshiriq: Eng katta va eng kichik qiymatni bitta o'tishda (Single Pass) topish
## Topshiriq sharti:
Massivni faqat bitta for sikli orqali aylanib chiqib Min va Max qiymatlarni aniqlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func minMax(arr []int) (int, int) {
	if len(arr) == 0 {
		return 0, 0
	}
	minVal, maxVal := arr[0], arr[0]

	for _, v := range arr[1:] {
		if v < minVal {
			minVal = v
		}
		if v > maxVal {
			maxVal = v
		}
	}
	return minVal, maxVal
}

func main() {
	qiymatlar := []int{34, 12, 89, 5, 77, 92, 18}
	kichik, katta := minMax(qiymatlar)
	fmt.Printf("Min: %d, Max: %d\n", kichik, katta)
}
```

## Tushuntirish va Mantiq:
Bitta sikl ichida ikkala chegarani tekshirish eng optimal O(N) yechimdir.

## Ishlash natijasi:
```text
Min: 5, Max: 92
```

# 143-Topshiriq: O'rtacha arifmetik qiymatni hisoblash
## Topshiriq sharti:
Haroratlar ro'yxatidan umumiy o'rtacha qiymatni hisoblab chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ortacha(haroratlar []float64) float64 {
	if len(haroratlar) == 0 {
		return 0
	}
	yigindi := 0.0
	for _, h := range haroratlar {
		yigindi += h
	}
	return yigindi / float64(len(haroratlar))
}

func main() {
	haftalikHarorat := []float64{22.5, 24.0, 26.5, 23.0, 25.5, 28.0, 27.0}
	fmt.Printf("Haftalik o'rtacha harorat: %.2f°C\n", ortacha(haftalikHarorat))
}
```

## Tushuntirish va Mantiq:
Barcha elementlar yig'indisi ularning soniga bo'linadi.

## Ishlash natijasi:
```text
Haftalik o'rtacha harorat: 25.21°C
```

# 144-Topshiriq: Takrorlangan elementlarni tozalash (Deduplication)
## Topshiriq sharti:
Massivdagi takrorlangan elementlarni for va map orqali noyob (unique) holga keltiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func noyobElementlar(arr []int) []int {
	korilgan := make(map[int]bool)
	var natija []int

	for _, item := range arr {
		if !korilgan[item] {
			korilgan[item] = true
			natija = append(natija, item)
		}
	}
	return natija
}

func main() {
	takrorli := []int{1, 2, 2, 3, 4, 4, 4, 5, 1, 6}
	fmt.Println("Tozalangan ro'yxat:", noyobElementlar(takrorli))
}
```

## Tushuntirish va Mantiq:
`korilgan[item]` orqali har bir yangi element birinchi marta uchraganda natijaga qo'shiladi.

## Ishlash natijasi:
```text
Tozalangan ro'yxat: [1 2 3 4 5 6]
```

# 145-Topshiriq: Collatz gipotezasi (3n + 1 muammosi)
## Topshiriq sharti:
Berilgan N soni 1 ga yetguncha qadamlar sonini hisoblang (juft bo'lsa /2, toq bo'lsa 3n+1).

## Yechim (Go kodi):
```go
package main

import "fmt"

func collatz(n int) int {
	qadamlar := 0
	for n != 1 {
		if n%2 == 0 {
			n /= 2
		} else {
			n = 3*n + 1
		}
		qadamlar++
	}
	return qadamlar
}

func main() {
	fmt.Printf("N = 6 uchun Collatz qadamlari: %d\n", collatz(6))
	fmt.Printf("N = 27 uchun Collatz qadamlari: %d\n", collatz(27))
}
```

## Tushuntirish va Mantiq:
Matematikadagi mashhur gipoteza: har qanday musbat butun son ushbu qoida orqali oxir-oqibat 1 ga yetib keladi.

## Ishlash natijasi:
```text
N = 6 uchun Collatz qadamlari: 8
N = 27 uchun Collatz qadamlari: 111
```

# 146-Topshiriq: Mukammal sonni (Perfect Number) aniqlash
## Topshiriq sharti:
O'zidan boshqa bo'luvchilari yig'indisi o'ziga teng bo'lgan sonni tekshiring (masalan, 6 va 28).

## Yechim (Go kodi):
```go
package main

import "fmt"

func isMukammal(n int) bool {
	if n <= 1 {
		return false
	}
	yigindi := 1
	for i := 2; i*i <= n; i++ {
		if n%i == 0 {
			yigindi += i
			if i*i != n {
				yigindi += n / i
			}
		}
	}
	return yigindi == n
}

func main() {
	sonlar := []int{6, 28, 496, 12, 100}
	for _, s := range sonlar {
		fmt.Printf("%d mukammal sonmi: %t\n", s, isMukammal(s))
	}
}
```

## Tushuntirish va Mantiq:
6 ning bo'luvchilari: 1 + 2 + 3 = 6. 28 ning bo'luvchilari: 1 + 2 + 4 + 7 + 14 = 28.

## Ishlash natijasi:
```text
6 mukammal sonmi: true
28 mukammal sonmi: true
496 mukammal sonmi: true
12 mukammal sonmi: false
100 mukammal sonmi: false
```

# 147-Topshiriq: Armstrong sonini aniqlash
## Topshiriq sharti:
Raqamlarining kublari yig'indisi o'ziga teng bo'lgan 3 xonali sonlarni toping (masalan, 153).

## Yechim (Go kodi):
```go
package main

import "fmt"

func isArmstrong(n int) bool {
	asl := n
	yigindi := 0

	for n > 0 {
		r := n % 10
		yigindi += r * r * r
		n /= 10
	}
	return asl == yigindi
}

func main() {
	for i := 100; i <= 500; i++ {
		if isArmstrong(i) {
			fmt.Printf("Armstrong soni topildi: %d\n", i)
		}
	}
}
```

## Tushuntirish va Mantiq:
153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153.

## Ishlash natijasi:
```text
Armstrong soni topildi: 153
Armstrong soni topildi: 370
Armstrong soni topildi: 371
Armstrong soni topildi: 407
```

# 148-Topshiriq: Matndagi so'zlar sonini holat mashinasi (State Machine) orqali sanash
## Topshiriq sharti:
Kutubxonalarsiz, faqat bitta for sikli va harf/bo'shliq holati orqali so'zlarni sanang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"unicode"
)

func countWords(s string) int {
	soni := 0
	sozIchidami := false

	for _, ch := range s {
		if !unicode.IsSpace(ch) {
			if !sozIchidami {
				sozIchidami = true
				soni++
			}
		} else {
			sozIchidami = false
		}
	}
	return soni
}

func main() {
	matn := "  Go tili juda   kuchli va   tezkor!  "
	fmt.Printf("So'zlar soni: %d ta\n", countWords(matn))
}
```

## Tushuntirish va Mantiq:
Holat o'zgaruvchisi (`sozIchidami`) orqali ketma-ket bir nechta bo'shliqlar to'g'ri filtrlanadi.

## Ishlash natijasi:
```text
So'zlar soni: 6 ta
```

# 149-Topshiriq: Eksponentsial orqaga chekinish (Exponential Backoff) simulyatsiyasi
## Topshiriq sharti:
Tarmoq so'rovi muvaffaqiyatsiz bo'lganda kutish vaqtini 2 barobar oshirib boruvchi for yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	maxUrinishlar := 4
	kutishVaqti := 100 * time.Millisecond

	for urinish := 1; urinish <= maxUrinishlar; urinish++ {
		fmt.Printf("%d-urinish: So'rov yuborilmoqda... (Kutish: %v)\n", urinish, kutishVaqti)
		kutishVaqti *= 2 // Har qadamda 2 barobar oshirish
	}
	fmt.Println("Urinishlar yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Mikroservislar va API mijozlarida serverni ortiqcha yuklamaslik uchun eksponentsial kutish qo'llaniladi.

## Ishlash natijasi:
```text
1-urinish: So'rov yuborilmoqda... (Kutish: 100ms)
2-urinish: So'rov yuborilmoqda... (Kutish: 200ms)
3-urinish: So'rov yuborilmoqda... (Kutish: 400ms)
4-urinish: So'rov yuborilmoqda... (Kutish: 800ms)
Urinishlar yakunlandi.
```

# 150-Topshiriq: Vaqt hisoblagichi (Ticker) bilan davriy vazifalarni bajarish
## Topshiriq sharti:
Muayyan miqdordagi iteratsiya davomida xabarlarni chiqaruvchi boshqariladigan sikl yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
)

func main() {
	vazifalarSoni := 3

	for i := 1; i <= vazifalarSoni; i++ {
		fmt.Printf("[%d] Tizim metriklari tekshirildi (OK)\n", i)
	}
	fmt.Println("Barcha davriy vazifalar bajarildi.")
}
```

## Tushuntirish va Mantiq:
Davriy monitoring va fon jarayonlarida sikllar nazoratli hisoblagich bilan ishlaydi.

## Ishlash natijasi:
```text
[1] Tizim metriklari tekshirildi (OK)
[2] Tizim metriklari tekshirildi (OK)
[3] Tizim metriklari tekshirildi (OK)
Barcha davriy vazifalar bajarildi.
```

