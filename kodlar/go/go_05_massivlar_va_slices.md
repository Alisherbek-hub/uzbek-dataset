# 5-Mavzu: Massivlar (Arrays) va Slices (201-250)

Go tilida massivlar (qat'iy o'lchamli va qiymat semantikasiga ega) va dinamik Slices (ko'rsatkich, uzunlik va sig'imdan iborat eng muhim ma'lumot tuzilmasi). `make`, `len`, `cap`, `append`, `copy`, 3-indeksli kesish, Go 1.21+ dagi standart `slices` paketi, stek va navbat tuzilmalari hamda xotirani boshqarish bo'yicha 50 ta amaliy topshiriq.

# 201-Topshiriq: Massiv (Array) e'lon qilish va qat'iy o'lcham [N]T
## Topshiriq sharti:
5 ta butun sondan iborat massiv e'lon qiling, elementlariga qiymat bering va ekranga chiqaring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var sonlar [5]int

	sonlar[0] = 10
	sonlar[1] = 20
	sonlar[2] = 30
	sonlar[3] = 40
	sonlar[4] = 50

	fmt.Println("Massiv:", sonlar)
	fmt.Printf("Uzunligi: %d, Turi: %T\n", len(sonlar), sonlar)
}
```

## Tushuntirish va Mantiq:
Go tilida massivning o'lchami uning turining ajralmas qismidir. `[5]int` va `[10]int` butunlay boshqa-boshqa turlar hisoblanadi.

## Ishlash natijasi:
```text
Massiv: [10 20 30 40 50]
Uzunligi: 5, Turi: [5]int
```

# 202-Topshiriq: Massiv o'lchamini [...] bilan kompilyatorga hisoblatish
## Topshiriq sharti:
`[...]` sintaksisi orqali boshlang'ich qiymatlar soniga qarab massiv hajmini avtomatik belgilang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	mevalar := [...]string{"Olma", "Anor", "Uzum", "Nok"}

	fmt.Printf("Massiv hajmi: %d ta element\n", len(mevalar))
	fmt.Printf("Elementlar: %v\n", mevalar)
}
```

## Tushuntirish va Mantiq:
`[...]` kompilyatorga elementlar sonini o'zi sanab, qat'iy o'lchamdagi massiv yaratishni buyuradi.

## Ishlash natijasi:
```text
Massiv hajmi: 4 ta element
Elementlar: [Olma Anor Uzum Nok]
```

# 203-Topshiriq: Massivlarning qiymat semantikasi (Value Semantics)
## Topshiriq sharti:
Massiv boshqa o'zgaruvchiga o'zlashtirilganda yoki funksiyaga uzatilganda to'liq nusxalanishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ozgartirMassiv(arr [3]int) {
	arr[0] = 999 // Faqat nusxasi o'zgaradi!
}

func main() {
	asl := [3]int{1, 2, 3}
	nusxa := asl

	nusxa[0] = 100 // Faqat nusxaga ta'sir qiladi

	fmt.Println("Asl massiv:", asl)
	fmt.Println("Nusxa massiv:", nusxa)

	ozgartirMassiv(asl)
	fmt.Println("Funksiyadan keyin asl massiv:", asl)
}
```

## Tushuntirish va Mantiq:
C tilidan farqli ravishda Go da massiv ko'rsatkich emas, balki yaxlit qiymatdir. Har qanday o'zlashtirish butun massivni xotirada nusxalaydi.

## Ishlash natijasi:
```text
Asl massiv: [1 2 3]
Nusxa massiv: [100 2 3]
Funksiyadan keyin asl massiv: [1 2 3]
```

# 204-Topshiriq: Massivlarni taqqoslash (== va !=)
## Topshiriq sharti:
Bir xil tur va o'lchamdagi massivlarni to'g'ridan-to'g'ri `==` bilan solishtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	a := [3]int{1, 2, 3}
	b := [3]int{1, 2, 3}
	c := [3]int{1, 2, 4}

	fmt.Println("a == b :", a == b)
	fmt.Println("a == c :", a == c)
}
```

## Tushuntirish va Mantiq:
Agar massiv elementlarining turi taqqoslanuvchi bo'lsa, massivlar `==` operatori orqali to'liq elementma-element tekshiriladi.

## Ishlash natijasi:
```text
a == b : true
a == c : false
```

# 205-Topshiriq: Ko'p o'lchamli massivlar (2D Arrays)
## Topshiriq sharti:
2x3 o'lchamli matritsa massivini e'lon qiling va uning elementlarini chop eting.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var matritsa [2][3]int = [2][3]int{
		{1, 2, 3},
		{4, 5, 6},
	}

	for i := 0; i < len(matritsa); i++ {
		for j := 0; j < len(matritsa[i]); j++ {
			fmt.Printf("%d ", matritsa[i][j])
		}
		fmt.Println()
	}
}
```

## Tushuntirish va Mantiq:
Ko'p o'lchamli massivlar bir xil qator va ustunlarga ega bo'lgan to'g'ri to'rtburchak shakldagi qat'iy xotira blokidir.

## Ishlash natijasi:
```text
1 2 3 
4 5 6
```

# 206-Topshiriq: Slice tushunchasi: Pointer, Len va Cap sarlavhasi
## Topshiriq sharti:
Slice massiv ustidagi dinamik 'oyna' (view) ekanligini namoyish qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	massiv := [5]int{10, 20, 30, 40, 50}

	// Massivdan slice olamiz:
	kesma := massiv[1:4] // 1-indeksdan 4-indeksgacha (4 kirmaydi: 20, 30, 40)

	fmt.Println("Asl massiv:", massiv)
	fmt.Println("Olingan kesma (slice):", kesma)
}
```

## Tushuntirish va Mantiq:
Slice 3 ta qismdan iborat kichik sarlavhadir (24 bayt): asosiy massivga ko'rsatkich (Pointer), uzunlik (Length) va sig'im (Capacity).

## Ishlash natijasi:
```text
Asl massiv: [10 20 30 40 50]
Olingan kesma (slice): [20 30 40]
```

# 207-Topshiriq: len() va cap() funksiyalarining farqi
## Topshiriq sharti:
Slicening joriy uzunligi (`len`) va uning maksimal sig'imi (`cap`) qanday o'zgarishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	massiv := [6]int{10, 20, 30, 40, 50, 60}
	s := massiv[1:4] // [20, 30, 40]

	fmt.Printf("Elementlar: %v\n", s)
	fmt.Printf("Uzunlik (len): %d\n", len(s))
	fmt.Printf("Sig'im  (cap): %d\n", cap(s))
}
```

## Tushuntirish va Mantiq:
`len` - hozirda ochiq bo'lgan elementlar soni. `cap` - slice boshlangan joydan to tagidagi massivning oxirigacha bo'lgan jami elementlar sig'imi.

## Ishlash natijasi:
```text
Elementlar: [20 30 40]
Uzunlik (len): 3
Sig'im  (cap): 5
```

# 208-Topshiriq: Slice yaratish usullari: Literal va var
## Topshiriq sharti:
Slice literali va e'lon qilish usullarini solishtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	// Literal orqali:
	s1 := []string{"Go", "Python", "Rust"}

	// var orqali (boshlang'ich nil slice):
	var s2 []int

	fmt.Printf("s1: %v (len: %d, cap: %d)\n", s1, len(s1), cap(s1))
	fmt.Printf("s2 nilmi: %t (len: %d, cap: %d)\n", s2 == nil, len(s2), cap(s2))
}
```

## Tushuntirish va Mantiq:
`[]T{...}` sintaksisi orqa fonda anonim massiv yaratadi va unga bog'langan yangi sliceni qaytaradi.

## Ishlash natijasi:
```text
s1: [Go Python Rust] (len: 3, cap: 3)
s2 nilmi: true (len: 0, cap: 0)
```

# 209-Topshiriq: make() funksiyasi bilan slice yaratish: make([]T, len, cap)
## Topshiriq sharti:
`make` orqali oldindan aniq sig'im ajratilgan holda xotirani optimallashtiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	// Uzunligi 3, sig'imi 5 bo'lgan slice:
	s := make([]int, 3, 5)

	fmt.Printf("Boshlang'ich s: %v (len: %d, cap: %d)\n", s, len(s), cap(s))

	s[0] = 100
	s[1] = 200
	s[2] = 300

	fmt.Printf("To'ldirilgan s: %v\n", s)
}
```

## Tushuntirish va Mantiq:
`make([]T, len, cap)` orqali sig'imni oldindan belgilash kelajakdagi ortiqcha xotira qayta ajratilishlarining oldini oladi.

## Ishlash natijasi:
```text
Boshlang'ich s: [0 0 0] (len: 3, cap: 5)
To'ldirilgan s: [100 200 300]
```

# 210-Topshiriq: Nil slice va Bo'sh (Empty) slice o'rtasidagi farq
## Topshiriq sharti:
`var s []int` (nil) va `s := []int{}` (empty non-nil) ning JSON va xotiradagi farqini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var sNil []int
	sEmpty := []int{}

	fmt.Printf("sNil   == nil: %-5t | len: %d, cap: %d\n", sNil == nil, len(sNil), cap(sNil))
	fmt.Printf("sEmpty == nil: %-5t | len: %d, cap: %d\n", sEmpty == nil, len(sEmpty), cap(sEmpty))
}
```

## Tushuntirish va Mantiq:
Nil slice xotirada ko'rsatkichga ega emas (null). Bo'sh slice esa 0 o'lchamli haqiqiy xotira manziliga ko'rsatadi. JSON ga o'girilganda `nil` `null` bo'ladi, empty esa `[]` bo'ladi.

## Ishlash natijasi:
```text
sNil   == nil: true  | len: 0, cap: 0
sEmpty == nil: false | len: 0, cap: 0
```

# 211-Topshiriq: Sliceni kesish sintaksisi (s[low:high])
## Topshiriq sharti:
Indekslar chegaralari bilan turli kesmalar oling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	sonlar := []int{0, 1, 2, 3, 4, 5, 6, 7}

	fmt.Println("Hammasi     :", sonlar[:])
	fmt.Println("Boshidan 4 ta:", sonlar[:4])
	fmt.Println("3 dan oxirigacha:", sonlar[3:])
	fmt.Println("2 dan 5 gacha  :", sonlar[2:5])
}
```

## Tushuntirish va Mantiq:
`s[low:high]` da `low` kiradi, `high` esa kirmaydi. Yangi hosil bo'lgan kesmaning uzunligi `high - low` bo'ladi.

## Ishlash natijasi:
```text
Hammasi     : [0 1 2 3 4 5 6 7]
Boshidan 4 ta: [0 1 2 3]
3 dan oxirigacha: [3 4 5 6 7]
2 dan 5 gacha  : [2 3 4]
```

# 212-Topshiriq: 3-indeksli to'liq kesish (Full Slice Expression: s[low:high:max])
## Topshiriq sharti:
Slicening sig'imini cheklash uchun uchinchi indeksdan foydalaning.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	asl := []int{10, 20, 30, 40, 50, 60}

	// [1:3:3] -> low=1, high=3, max=3 -> len = 2, cap = 2
	cheklangan := asl[1:3:3]

	fmt.Printf("cheklangan: %v (len: %d, cap: %d)\n", cheklangan, len(cheklangan), cap(cheklangan))
}
```

## Tushuntirish va Mantiq:
`s[low:high:max]` yangi kesmaning sig'imini `max - low` ga teng qilib qat'iy cheklaydi, bu esa keyinchalik `append` qilinganda asl massiv buzilishidan asraydi.

## Ishlash natijasi:
```text
cheklangan: [20 30] (len: 2, cap: 2)
```

# 213-Topshiriq: append() funksiyasi orqali elementlar qo'shish
## Topshiriq sharti:
Slicening oxiriga bir yoki bir nechta yangi elementlar qo'shing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var shaharlar []string

	shaharlar = append(shaharlar, "Toshkent")
	shaharlar = append(shaharlar, "Samarqand", "Buxoro")

	fmt.Println("Shaharlar:", shaharlar)
	fmt.Printf("Jami soni: %d\n", len(shaharlar))
}
```

## Tushuntirish va Mantiq:
`append` built-in funksiyasi doimo yangilangan sliceni qaytaradi, shuning uchun `s = append(s, val)` tarzida qayta o'zlashtiriladi.

## Ishlash natijasi:
```text
Shaharlar: [Toshkent Samarqand Buxoro]
Jami soni: 3
```

# 214-Topshiriq: append() orqali ikki sliceni birlashtirish (s1 = append(s1, s2...))
## Topshiriq sharti:
Ikkinchi sliceni `...` bilan yoyib, birinchi slice oxiriga qo'shing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	guruh1 := []int{1, 2, 3}
	guruh2 := []int{4, 5, 6}

	jami := append(guruh1, guruh2...)

	fmt.Println("Birlashtirilgan:", jami)
}
```

## Tushuntirish va Mantiq:
`guruh2...` sintaksisi ikkinchi slicening barcha elementlarini alohida argumentlar sifatida `append` ga uzatadi.

## Ishlash natijasi:
```text
Birlashtirilgan: [1 2 3 4 5 6]
```

# 215-Topshiriq: Slice sig'imining o'sish mexanizmi (Reallocation)
## Topshiriq sharti:
`append` qilinganda sig'im qanday sakrab borishini kuzating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var s []int
	eskiCap := 0

	for i := 0; i < 9; i++ {
		s = append(s, i)
		if cap(s) != eskiCap {
			fmt.Printf("Element: %d | len: %d -> Yangi cap: %d\n", i, len(s), cap(s))
			eskiCap = cap(s)
		}
	}
}
```

## Tushuntirish va Mantiq:
Sig'im yetmay qolganda Go yangi kattaroq xotira bloki ajratadi (kichik slicelar uchun 2 barobar) va barcha elementlarni ko'chirib o'tadi.

## Ishlash natijasi:
```text
Element: 0 | len: 1 -> Yangi cap: 1
Element: 1 | len: 2 -> Yangi cap: 2
Element: 2 | len: 3 -> Yangi cap: 4
Element: 4 | len: 5 -> Yangi cap: 8
Element: 8 | len: 9 -> Yangi cap: 16
```

# 216-Topshiriq: Slicening tagidagi massiv bilan aloqasi va kutilmagan yon ta'sirlar
## Topshiriq sharti:
Bitta massivdan olingan ikki slice bittasini o'zgartirganda ikkinchisiga ham ta'sir qilishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	asl := []int{1, 2, 3, 4, 5}
	kesma := asl[1:4] // [2, 3, 4]

	kesma[0] = 99 // kesmaning 0-elementi asl massivning 1-elementidir!

	fmt.Println("Kesma o'zgardi:", kesma)
	fmt.Println("Asl massiv ham o'zgardi:", asl)
}
```

## Tushuntirish va Mantiq:
Kesmalar tagidagi umumiy massivga ko'rsatib turadi. Agar mustaqil bo'lishi kerak bo'lsa, `copy()` ishlatiladi.

## Ishlash natijasi:
```text
Kesma o'zgardi: [99 3 4]
Asl massiv ham o'zgardi: [1 99 3 4 5]
```

# 217-Topshiriq: copy() funksiyasi orqali to'liq mustaqil nusxa olish (Deep Copy)
## Topshiriq sharti:
`copy(maqsad, manba)` yordamida yangi xotira ajratib mustaqil nusxa oling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	asl := []int{10, 20, 30}
	nusxa := make([]int, len(asl)) // Xotira oldindan ajratilgan bo'lishi shart!

	nusxalanganSoni := copy(nusxa, asl)

	nusxa[0] = 999 // Asl massivga mutlaqo ta'sir qilmaydi

	fmt.Printf("Nusxalandi: %d ta element\n", nusxalanganSoni)
	fmt.Println("Asl:", asl)
	fmt.Println("Nusxa:", nusxa)
}
```

## Tushuntirish va Mantiq:
`copy()` faqat maqsad slicening `len` o'lchamigacha nusxalaydi. Shuning uchun `make` bilan bo'sh joy tayyorlanishi shart.

## Ishlash natijasi:
```text
Nusxalandi: 3 ta element
Asl: [10 20 30]
Nusxa: [999 20 30]
```

# 218-Topshiriq: Slicedan elementni indeks bo'yicha o'chirish (Tartibni saqlagan holda)
## Topshiriq sharti:
`append` va kesish yordamida berilgan indeksdagi elementni o'chirib tashlang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func ochirIndeks(arr []int, i int) []int {
	return append(arr[:i], arr[i+1:]...)
}

func main() {
	sonlar := []int{10, 20, 30, 40, 50}
	fmt.Println("Boshlang'ich:", sonlar)

	// 2-indeksdagi (30) sonni o'chiramiz:
	sonlar = ochirIndeks(sonlar, 2)
	fmt.Println("O'chirilgach:", sonlar)
}
```

## Tushuntirish va Mantiq:
`append(arr[:i], arr[i+1:]...)` i-elementdan keyingilarni oldinga suradi va elementlar tartibini to'liq saqlaydi.

## Ishlash natijasi:
```text
Boshlang'ich: [10 20 30 40 50]
O'chirilgach: [10 20 40 50]
```

# 219-Topshiriq: Slicedan tez o'chirish (Tartib muhim bo'lmaganda: Swap with Last)
## Topshiriq sharti:
O'chiriladigan element o'rniga eng oxirgi elementni ko'chirib qo'yish orqali O(1) tezlikda o'chirish.

## Yechim (Go kodi):
```go
package main

import "fmt"

func tezOchir(arr []string, i int) []string {
	arr[i] = arr[len(arr)-1] // Oxirgisini i o'rniga ko'chiramiz
	return arr[:len(arr)-1]  // Oxirgi elementni qirqib tashlaymiz
}

func main() {
	mevalar := []string{"olma", "banan", "nok", "uzum", "shaftoli"}
	fmt.Println("Oldin:", mevalar)

	// 1-indeksdagi ("banan") ni tez o'chirish:
	mevalar = tezOchir(mevalar, 1)
	fmt.Println("Keyin:", mevalar)
}
```

## Tushuntirish va Mantiq:
Elementlarni surib chiqish (O(N)) o'rniga oxirgisini qo'yish O(1) vaqt oladi va katta ro'yxatlarda juda samaralidir.

## Ishlash natijasi:
```text
Oldin: [olma banan nok uzum shaftoli]
Keyin: [olma shaftoli nok uzum]
```

# 220-Topshiriq: Slicening o'rtasiga yangi element qistirib qo'yish (Insert at index)
## Topshiriq sharti:
Berilgan indeksga yangi elementni joylashtiruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func qistir(arr []int, indeks, qiymat int) []int {
	arr = append(arr[:indeks+1], arr[indeks:]...)
	arr[indeks] = qiymat
	return arr
}

func main() {
	sonlar := []int{1, 2, 4, 5}
	// 2-indeksga 3 sonini qistiramiz:
	sonlar = qistir(sonlar, 2, 3)
	fmt.Println("Natija:", sonlar)
}
```

## Tushuntirish va Mantiq:
Qistirib qo'yishda orqa qism bir qadam o'ngga suriladi va bo'shagan o'ringa yangi qiymat yoziladi.

## Ishlash natijasi:
```text
Natija: [1 2 3 4 5]
```

# 221-Topshiriq: Ko'p o'lchamli slice (Slice of Slices: [][]T)
## Topshiriq sharti:
Har bir qatori turli uzunlikda bo'lishi mumkin bo'lgan dinamik jadval tuzing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	jadval := [][]int{
		{1},
		{2, 3},
		{4, 5, 6},
	}

	for i, qator := range jadval {
		fmt.Printf("%d-qator: %v\n", i, qator)
	}
}
```

## Tushuntirish va Mantiq:
Massivlardan farqli ravishda `[][]T` ko'rinishidagi slicelar har bir qatori alohida o'lchamga ega bo'lgan 'jagged array' bo'la oladi.

## Ishlash natijasi:
```text
0-qator: [1]
1-qator: [2 3]
2-qator: [4 5 6]
```

# 222-Topshiriq: Go 1.21+ slices.Clone orqali sliceni tez klonlash
## Topshiriq sharti:
Standart `slices.Clone` funksiyasidan foydalanib slicening chuqur nusxasini oling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"slices"
)

func main() {
	asl := []string{"Go", "Kubernetes", "Docker"}
	nusxa := slices.Clone(asl)

	nusxa[0] = "Terraform"

	fmt.Println("Asl:", asl)
	fmt.Println("Nusxa:", nusxa)
}
```

## Tushuntirish va Mantiq:
`slices.Clone` Go 1.21 da kiritilgan bo'lib, `make` va `copy` yozmasdan bir chaqiriqda yangi mustaqil nusxa yaratadi.

## Ishlash natijasi:
```text
Asl: [Go Kubernetes Docker]
Nusxa: [Terraform Kubernetes Docker]
```

# 223-Topshiriq: Go 1.21+ slices.Contains bilan elementni qidirish
## Topshiriq sharti:
Sliceda element mavjudligini for siklisiz bir qatorda tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"slices"
)

func main() {
	tillari := []string{"Go", "Python", "Rust", "C++"}

	fmt.Println("Go bormi:", slices.Contains(tillari, "Go"))
	fmt.Println("Java bormi:", slices.Contains(tillari, "Java"))
}
```

## Tushuntirish va Mantiq:
`slices.Contains` generik funksiya bo'lib, har qanday `comparable` turdagi slicelar uchun ishlaydi.

## Ishlash natijasi:
```text
Go bormi: true
Java bormi: false
```

# 224-Topshiriq: Go 1.21+ slices.Index orqali indeksni aniqlash
## Topshiriq sharti:
Qidirilayotgan qiymat birinchi uchragan indeksini `slices.Index` orqali toping.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"slices"
)

func main() {
	sonlar := []int{10, 20, 30, 40, 50}

	fmt.Println("30 indeksi:", slices.Index(sonlar, 30))
	fmt.Println("99 indeksi:", slices.Index(sonlar, 99))
}
```

## Tushuntirish va Mantiq:
Element topilsa uning indeksi (0..N-1), topilmasa `-1` qaytariladi.

## Ishlash natijasi:
```text
30 indeksi: 2
99 indeksi: -1
```

# 225-Topshiriq: Go 1.21+ slices.Equal orqali ikki sliceni solishtirish
## Topshiriq sharti:
Ikkita mustaqil slicening barcha elementlari tengligini `slices.Equal` bilan tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"slices"
)

func main() {
	s1 := []int{1, 2, 3}
	s2 := []int{1, 2, 3}
	s3 := []int{1, 2, 4}

	fmt.Println("s1 va s2 tengmi:", slices.Equal(s1, s2))
	fmt.Println("s1 va s3 tengmi:", slices.Equal(s1, s3))
}
```

## Tushuntirish va Mantiq:
Go da slicelarni `s1 == s2` deb bo'lmaydi (faqat `s1 == nil` mumkin). Shuning uchun `slices.Equal` standart vositadir.

## Ishlash natijasi:
```text
s1 va s2 tengmi: true
s1 va s3 tengmi: false
```

# 226-Topshiriq: Go 1.21+ slices.Sort va slices.SortFunc orqali saralash
## Topshiriq sharti:
Butun sonlar va maxsus strukturalarni `slices` paketi yordamida saralang.

## Yechim (Go kodi):
```go
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type Foydalanuvchi struct {
	Ism  string
	Yosh int
}

func main() {
	sonlar := []int{5, 2, 8, 1, 9}
	slices.Sort(sonlar)
	fmt.Println("Saralangan sonlar:", sonlar)

	odamlar := []Foydalanuvchi{
		{"Vali", 25},
		{"Ali", 20},
		{"G'ani", 30},
	}
	// Yosh bo'yicha saralash:
	slices.SortFunc(odamlar, func(a, b Foydalanuvchi) int {
		return cmp.Compare(a.Yosh, b.Yosh)
	})
	fmt.Println("Yosh bo'yicha:", odamlar)
}
```

## Tushuntirish va Mantiq:
`slices.Sort` ichki tezkor pdqsort algoritmidan foydalanadi va qo'shimcha xotira ajratmasdan joyida tartiblaydi.

## Ishlash natijasi:
```text
Saralangan sonlar: [1 2 5 8 9]
Yosh bo'yicha: [{Ali 20} {Vali 25} {G'ani 30}]
```

# 227-Topshiriq: Go 1.21+ slices.Reverse orqali sliceni joyida teskari o'girish
## Topshiriq sharti:
Standart `slices.Reverse` yordamida massivni tezkor teskarisiga aylantiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"slices"
)

func main() {
	harflar := []string{"A", "B", "C", "D", "E"}
	slices.Reverse(harflar)
	fmt.Println("Teskari:", harflar)
}
```

## Tushuntirish va Mantiq:
`slices.Reverse` ikki ko'rsatkichli algoritmni apparat darajasida optimallashtirilgan holda bajaradi.

## Ishlash natijasi:
```text
Teskari: [E D C B A]
```

# 228-Topshiriq: Go 1.21+ slices.Compact orqali ketma-ket takrorlarni tozalash
## Topshiriq sharti:
Saralangan sliceda ketma-ket kelgan bir xil elementlarni bittaga qisqartiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"slices"
)

func main() {
	takrorlar := []int{1, 1, 2, 2, 2, 3, 4, 4, 5}
	toza := slices.Compact(takrorlar)
	fmt.Println("Qisqartirilgan:", toza)
}
```

## Tushuntirish va Mantiq:
`slices.Compact` faqat yonma-yon turgan takror elementlarni tozalaydi (Unix `uniq` utilitasi kabi).

## Ishlash natijasi:
```text
Qisqartirilgan: [1 2 3 4 5]
```

# 229-Topshiriq: Go 1.21+ slices.Min va slices.Max funksiyalari
## Topshiriq sharti:
Slicening minimal va maksimal elementlarini bitta chaqiriqda oling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"slices"
)

func main() {
	narxlar := []float64{120.5, 45.0, 890.0, 15.5, 300.2}

	engArzon := slices.Min(narxlar)
	engQimmat := slices.Max(narxlar)

	fmt.Printf("Eng arzon: %.2f | Eng qimmat: %.2f\n", engArzon, engQimmat)
}
```

## Tushuntirish va Mantiq:
`slices.Min` va `slices.Max` `cmp.Ordered` turidagi barcha taqqoslanuvchi turlarda ishlaydi.

## Ishlash natijasi:
```text
Eng arzon: 15.50 | Eng qimmat: 890.00
```

# 230-Topshiriq: Katta massivdan kichik kesma olishdagi xotira sizishi (Memory Leak)
## Topshiriq sharti:
Katta massivning kichik qismi ushlab turilganda butun massiv GC tomonidan o'chirilmay qolishi muammosini hal qiling.

## Yechim (Go kodi):
```go
package main

import "fmt"

func xavfliKesma() []int {
	kattaMassiv := make([]int, 1_000_000)
	kattaMassiv[0] = 42
	return kattaMassiv[:2] // 1 millionlik massiv xotirada qolib ketadi!
}

func xavfsizKesma() []int {
	kattaMassiv := make([]int, 1_000_000)
	kattaMassiv[0] = 42

	// To'g'ri usul: faqat kerakli 2 ta elementni yangi kichik slicega nusxalash
	kichik := make([]int, 2)
	copy(kichik, kattaMassiv[:2])
	return kichik // Katta massiv Garbage Collector tomonidan tozalanadi
}

func main() {
	res := xavfsizKesma()
	fmt.Printf("Xavfsiz kesma: %v (len: %d, cap: %d)\n", res, len(res), cap(res))
}
```

## Tushuntirish va Mantiq:
Kichik kesma asl katta massivga ko'rsatib tursa, GC butun massivni xotiradan o'chira olmaydi. Buni tuzatish uchun `copy()` bilan yangi kichik slice ajratish shart.

## Ishlash natijasi:
```text
Xavfsiz kesma: [42 0] (len: 2, cap: 2)
```

# 231-Topshiriq: In-Place filtr (Qo'shimcha xotira ajratmasdan filtrlash)
## Topshiriq sharti:
Mavjud slicening o'zidan foydalanib, yangi massiv yaratmasdan juft sonlarni qoldiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func filtrJuftInPlace(sonlar []int) []int {
	n := 0
	for _, x := range sonlar {
		if x%2 == 0 {
			sonlar[n] = x
			n++
		}
	}
	return sonlar[:n]
}

func main() {
	raqamlar := []int{1, 2, 3, 4, 5, 6, 7, 8}
	juftlar := filtrJuftInPlace(raqamlar)
	fmt.Println("Filtrlangan:", juftlar)
}
```

## Tushuntirish va Mantiq:
Slicening tagidagi xotirani qayta ishlatish orqali 0 bayt qo'shimcha xotira bilan saralash va filtrlash amalga oshiriladi.

## Ishlash natijasi:
```text
Filtrlangan: [2 4 6 8]
```

# 232-Topshiriq: Sliceni qismlarga bo'lish (Chunking)
## Topshiriq sharti:
Katta sliceni har biri K o'lchamli kichik bo'laklarga ajratuvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func chunkSlice(arr []int, hajm int) [][]int {
	var natija [][]int
	for i := 0; i < len(arr); i += hajm {
		oxirgi := i + hajm
		if oxirgi > len(arr) {
			oxirgi = len(arr)
		}
		natija = append(natija, arr[i:oxirgi])
	}
	return natija
}

func main() {
	malumotlar := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	bolaklar := chunkSlice(malumotlar, 3)

	for i, b := range bolaklar {
		fmt.Printf("%d-bo'lak: %v\n", i+1, b)
	}
}
```

## Tushuntirish va Mantiq:
Chunking ma'lumotlarni paketlab (batch processing) bazaga yozish yoki API orqali jo'natishda keng qo'llaniladi.

## Ishlash natijasi:
```text
1-bo'lak: [1 2 3]
2-bo'lak: [4 5 6]
3-bo'lak: [7 8 9]
4-bo'lak: [10]
```

# 233-Topshiriq: Ko'p o'lchamli sliceni tekislash (Flattening: [][]int -> []int)
## Topshiriq sharti:
Ichma-ich joylashgan qatorlarni bitta yaxlit 1D massivga aylantiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

func tekislash(matritsa [][]int) []int {
	var natija []int
	for _, qator := range matritsa {
		natija = append(natija, qator...)
	}
	return natija
}

func main() {
	m := [][]int{
		{1, 2},
		{3, 4, 5},
		{6},
	}
	fmt.Println("Tekislangan:", tekislash(m))
}
```

## Tushuntirish va Mantiq:
`append(natija, qator...)` har bir ichki qatorni yoyib bitta o'lchamli ro'yxatga qo'shadi.

## Ishlash natijasi:
```text
Tekislangan: [1 2 3 4 5 6]
```

# 234-Topshiriq: Slice orqali Stek (Stack LIFO) ma'lumot tuzilmasi
## Topshiriq sharti:
`Push` va `Pop` operatsiyalarini slice asosida amalga oshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Stack struct {
	elementlar []string
}

func (s *Stack) Push(v string) {
	s.elementlar = append(s.elementlar, v)
}

func (s *Stack) Pop() (string, bool) {
	if len(s.elementlar) == 0 {
		return "", false
	}
	oxirgiIdx := len(s.elementlar) - 1
	qiymat := s.elementlar[oxirgiIdx]
	s.elementlar = s.elementlar[:oxirgiIdx]
	return qiymat, true
}

func main() {
	st := &Stack{}
	st.Push("Sahifa 1")
	st.Push("Sahifa 2")
	st.Push("Sahifa 3")

	for {
		elem, ok := st.Pop()
		if !ok {
			break
		}
		fmt.Println("Pop:", elem)
	}
}
```

## Tushuntirish va Mantiq:
Stek LIFO (oxirgi kirgan - birinchi chiqadi) tamoyilida ishlaydi va slice oxiriga qo'shish/o'chirish orqali oson yasaladi.

## Ishlash natijasi:
```text
Pop: Sahifa 3
Pop: Sahifa 2
Pop: Sahifa 1
```

# 235-Topshiriq: Slice orqali Navbat (Queue FIFO) ma'lumot tuzilmasi
## Topshiriq sharti:
`Enqueue` va `Dequeue` operatsiyalarini slice bilan amalga oshiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type Queue struct {
	elementlar []int
}

func (q *Queue) Enqueue(v int) {
	q.elementlar = append(q.elementlar, v)
}

func (q *Queue) Dequeue() (int, bool) {
	if len(q.elementlar) == 0 {
		return 0, false
	}
	birinchi := q.elementlar[0]
	q.elementlar = q.elementlar[1:]
	return birinchi, true
}

func main() {
	navbat := &Queue{}
	navbat.Enqueue(100)
	navbat.Enqueue(200)
	navbat.Enqueue(300)

	for {
		v, ok := navbat.Dequeue()
		if !ok {
			break
		}
		fmt.Println("Dequeue:", v)
	}
}
```

## Tushuntirish va Mantiq:
Navbat FIFO (birinchi kelgan - birinchi ketadi) tamoyilida ishlaydi.

## Ishlash natijasi:
```text
Dequeue: 100
Dequeue: 200
Dequeue: 300
```

# 236-Topshiriq: Aylana bufer (Circular Ring Buffer) slice orqali
## Topshiriq sharti:
Qat'iy sig'imli va oxirgi N ta elementni saqlovchi bufer yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type RingBuffer struct {
	data []int
	hajm int
	pos  int
	tola bool
}

func NewRingBuffer(hajm int) *RingBuffer {
	return &RingBuffer{data: make([]int, hajm), hajm: hajm}
}

func (r *RingBuffer) Yozish(val int) {
	r.data[r.pos] = val
	r.pos = (r.pos + 1) % r.hajm
	if r.pos == 0 {
		r.tola = true
	}
}

func (r *RingBuffer) Oqish() []int {
	if !r.tola {
		return r.data[:r.pos]
	}
	res := make([]int, r.hajm)
	for i := 0; i < r.hajm; i++ {
		res[i] = r.data[(r.pos+i)%r.hajm]
	}
	return res
}

func main() {
	rb := NewRingBuffer(3)
	rb.Yozish(1)
	rb.Yozish(2)
	rb.Yozish(3)
	rb.Yozish(4) // 1 o'rniga yoziladi

	fmt.Println("Aylana buferdagi oxirgi 3 ta son:", rb.Oqish())
}
```

## Tushuntirish va Mantiq:
Aylana buferlar log fayllar va sensor ma'lumotlarida oxirgi N ta voqeani xotirada saqlash uchun eng tejamkor vositadir.

## Ishlash natijasi:
```text
Aylana buferdagi oxirgi 3 ta son: [2 3 4]
```

# 237-Topshiriq: Slice elementlarini siljitish (Rotate Left)
## Topshiriq sharti:
Massivni K qadam chapga siljituvchi funksiya yozing (masalan, [1,2,3,4,5] -> [3,4,5,1,2]).

## Yechim (Go kodi):
```go
package main

import "fmt"

func rotateLeft(arr []int, k int) []int {
	n := len(arr)
	if n == 0 {
		return arr
	}
	k = k % n
	return append(arr[k:], arr[:k]...)
}

func main() {
	sonlar := []int{1, 2, 3, 4, 5}
	fmt.Println("2 qadam chapga:", rotateLeft(sonlar, 2))
}
```

## Tushuntirish va Mantiq:
Slicing va `append` yordamida massivni qismlarga ajratib o'rnini almashtirish orqali siljitish juda oson erishiladi.

## Ishlash natijasi:
```text
2 qadam chapga: [3 4 5 1 2]
```

# 238-Topshiriq: Slicelarning simmetrik farqi (Symmetric Difference)
## Topshiriq sharti:
Faqat birinchi yoki faqat ikkinchi slicedagina bor elementlarni toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

func simmetrikFarq(a, b []int) []int {
	hisob := make(map[int]int)
	for _, x := range a {
		hisob[x]++
	}
	for _, y := range b {
		hisob[y]++
	}

	var natija []int
	for k, v := range hisob {
		if v == 1 {
			natija = append(natija, k)
		}
	}
	return natija
}

func main() {
	s1 := []int{1, 2, 3, 4}
	s2 := []int{3, 4, 5, 6}
	fmt.Println("Simmetrik farq:", simmetrikFarq(s1, s2))
}
```

## Tushuntirish va Mantiq:
Har ikkala to'plamdan faqat umumiy bo'lmagan elementlar ajratib olinadi.

## Ishlash natijasi:
```text
Simmetrik farq: [1 2 5 6]
```

# 239-Topshiriq: Slicelar birlashmasi (Union)
## Topshiriq sharti:
Ikki slicening barcha takrorlanmas elementlarini birlashtiruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func birlashma(a, b []int) []int {
	mavjud := make(map[int]bool)
	var natija []int

	for _, x := range append(a, b...) {
		if !mavjud[x] {
			mavjud[x] = true
			natija = append(natija, x)
		}
	}
	return natija
}

func main() {
	a := []int{10, 20, 30}
	b := []int{20, 30, 40, 50}
	fmt.Println("Birlashma:", birlashma(a, b))
}
```

## Tushuntirish va Mantiq:
To'plamlar birlashmasida ikkala ro'yxatdagi elementlar yig'iladi va takrorlari elanadi.

## Ishlash natijasi:
```text
Birlashma: [10 20 30 40 50]
```

# 240-Topshiriq: Fisher-Yates Shuffle algoritmi bilan sliceni tasodifiy aralashtirish
## Topshiriq sharti:
Karta o'yinlari kabi slice elementlarini teng ehtimollikda chalkashtiruvchi algoritm yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"math/rand"
)

func shuffle(arr []int) {
	r := rand.New(rand.NewSource(42)) // Deterministik seed namoyish uchun
	for i := len(arr) - 1; i > 0; i-- {
		j := r.Intn(i + 1)
		arr[i], arr[j] = arr[j], arr[i]
	}
}

func main() {
	kartalar := []int{1, 2, 3, 4, 5, 6, 7}
	shuffle(kartalar)
	fmt.Println("Aralashtirilgan:", kartalar)
}
```

## Tushuntirish va Mantiq:
Fisher-Yates algoritmi har bir permutatsiyaning paydo bo'lish ehtimolligini teng kafolatlaydi.

## Ishlash natijasi:
```text
Aralashtirilgan: [5 2 7 1 3 6 4]
```

# 241-Topshiriq: Sliceda eng ko'p takrorlangan elementni (Moda) topish
## Topshiriq sharti:
Eng yuqori chastota bilan qatnashgan elementni map va for orqali hisoblang.

## Yechim (Go kodi):
```go
package main

import "fmt"

func topModa(arr []int) (int, int) {
	chastota := make(map[int]int)
	for _, v := range arr {
		chastota[v]++
	}

	maxSon, maxTakror := arr[0], 0
	for k, soni := range chastota {
		if soni > maxTakror {
			maxTakror = soni
			maxSon = k
		}
	}
	return maxSon, maxTakror
}

func main() {
	qiymatlar := []int{3, 5, 2, 3, 8, 3, 2, 5, 3}
	son, takror := topModa(qiymatlar)
	fmt.Printf("Moda: %d (takrorlanish soni: %d marta)\n", son, takror)
}
```

## Tushuntirish va Mantiq:
Statistikada eng ko'p uchraydigan qiymat moda deyiladi.

## Ishlash natijasi:
```text
Moda: 3 (takrorlanish soni: 4 marta)
```

# 242-Topshiriq: 2D Matritsani transponirlash (Transpose)
## Topshiriq sharti:
Qator va ustunlarning o'rnini almashtiruvchi (A[i][j] -> A[j][i]) funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func transpose(m [][]int) [][]int {
	qatorlar := len(m)
	ustunlar := len(m[0])

	natija := make([][]int, ustunlar)
	for i := range natija {
		natija[i] = make([]int, qatorlar)
	}

	for i := 0; i < qatorlar; i++ {
		for j := 0; j < ustunlar; j++ {
			natija[j][i] = m[i][j]
		}
	}
	return natija
}

func main() {
	matritsa := [][]int{
		{1, 2, 3},
		{4, 5, 6},
	}
	tr := transpose(matritsa)
	fmt.Println("Transponirlangan:")
	for _, q := range tr {
		fmt.Println(q)
	}
}
```

## Tushuntirish va Mantiq:
Transponirlashda NxM matritsa MxN matritsaga aylanadi.

## Ishlash natijasi:
```text
Transponirlangan:
[1 4]
[2 5]
[3 6]
```

# 243-Topshiriq: Matritsalarni ko'paytirish (Matrix Multiplication)
## Topshiriq sharti:
Ikki mos o'lchamli matritsani ko'paytiruvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func kopaytirMatritsa(a, b [][]int) [][]int {
	qA, uA := len(a), len(a[0])
	uB := len(b[0])

	natija := make([][]int, qA)
	for i := range natija {
		natija[i] = make([]int, uB)
		for j := 0; j < uB; j++ {
			for k := 0; k < uA; k++ {
				natija[i][j] += a[i][k] * b[k][j]
			}
		}
	}
	return natija
}

func main() {
	a := [][]int{{1, 2}, {3, 4}}
	b := [][]int{{2, 0}, {1, 2}}

	res := kopaytirMatritsa(a, b)
	fmt.Println("Ko'paytma:")
	for _, row := range res {
		fmt.Println(row)
	}
}
```

## Tushuntirish va Mantiq:
Chiziqli algebra va AI hisob-kitoblarida matritsalar ko'paytmasi asosiy operatsiya hisoblanadi.

## Ishlash natijasi:
```text
Ko'paytma:
[4 4]
[10 8]
```

# 244-Topshiriq: Go 1.21+ slices.BinarySearch orqali saralangan sliceda tezkor qidiruv
## Topshiriq sharti:
Saralangan sliceda elementni qidirib, agar topilmasa qayerga qo'shilishi kerakligini aniqlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"slices"
)

func main() {
	saralangan := []int{10, 20, 30, 40, 50}

	idx1, topildimi1 := slices.BinarySearch(saralangan, 30)
	fmt.Printf("30 qidiruvi: topildimi=%t, indeks=%d\n", topildimi1, idx1)

	idx2, topildimi2 := slices.BinarySearch(saralangan, 25)
	fmt.Printf("25 qidiruvi: topildimi=%t, qistirilar o'rni=%d\n", topildimi2, idx2)
}
```

## Tushuntirish va Mantiq:
`slices.BinarySearch` element topilmasa ham, saralanish buzilmasligi uchun yangi qiymat qaysi indeksga qo'shilishi kerakligini qaytaradi.

## Ishlash natijasi:
```text
30 qidiruvi: topildimi=true, indeks=2
25 qidiruvi: topildimi=false, qistirilar o'rni=2
```

# 245-Topshiriq: Slice bilan ikkita ko'rsatkichli (Two-Pointer) juftlik qidiruvi
## Topshiriq sharti:
Saralangan massivda yig'indisi Target ga teng bo'lgan ikki sonni O(N) vaqtda toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

func topJuftlik(arr []int, target int) (int, int, bool) {
	chap := 0
	ong := len(arr) - 1

	for chap < ong {
		yigindi := arr[chap] + arr[ong]
		if yigindi == target {
			return arr[chap], arr[ong], true
		}
		if yigindi < target {
			chap++
		} else {
			ong--
		}
	}
	return 0, 0, false
}

func main() {
	sonlar := []int{2, 7, 11, 15, 20}
	a, b, ok := topJuftlik(sonlar, 22)
	fmt.Printf("Yig'indisi 22 bo'lgan juftlik: %d va %d (topildi: %t)\n", a, b, ok)
}
```

## Tushuntirish va Mantiq:
Two-pointer uslubi saralangan massivlarda kvadratik (O(N^2)) qidiruvni chiziqli (O(N)) tezlikka tushiradi.

## Ishlash natijasi:
```text
Yig'indisi 22 bo'lgan juftlik: 2 va 20 (topildi: true)
```

# 246-Topshiriq: Sliding Window (Sirpanuvchi Darcha) algoritmi slice ustida
## Topshiriq sharti:
K uzunlikdagi ketma-ket elementlarning maksimal yig'indisini toping.

## Yechim (Go kodi):
```go
package main

import "fmt"

func maxSubarraySum(arr []int, k int) int {
	if len(arr) < k {
		return 0
	}

	darchaYigindi := 0
	for i := 0; i < k; i++ {
		darchaYigindi += arr[i]
	}

	maxYigindi := darchaYigindi
	for i := k; i < len(arr); i++ {
		darchaYigindi += arr[i] - arr[i-k] // Yangi element kiradi, eskisini chiqaramiz
		if darchaYigindi > maxYigindi {
			maxYigindi = darchaYigindi
		}
	}
	return maxYigindi
}

func main() {
	sonlar := []int{2, 1, 5, 1, 3, 2}
	fmt.Println("K=3 uchun maksimal darcha yig'indisi:", maxSubarraySum(sonlar, 3))
}
```

## Tushuntirish va Mantiq:
Sliding window har qadamda qaytadan yig'indi hisoblamay, faqat kirgan va chiqqan elementlar farqini hisoblaydi.

## Ishlash natijasi:
```text
K=3 uchun maksimal darcha yig'indisi: 9
```

# 247-Topshiriq: Slice ustida Prefiks Yig'indilar (Prefix Sum) massivi
## Topshiriq sharti:
Oraliq so'rovlarini O(1) vaqtda hisoblash uchun Prefiks massivini shakllantiring.

## Yechim (Go kodi):
```go
package main

import "fmt"

type PrefixSum struct {
	pref []int
}

func NewPrefixSum(arr []int) *PrefixSum {
	pref := make([]int, len(arr)+1)
	for i, x := range arr {
		pref[i+1] = pref[i] + x
	}
	return &PrefixSum{pref: pref}
}

func (p *PrefixSum) Query(L, R int) int {
	return p.pref[R+1] - p.pref[L]
}

func main() {
	arr := []int{1, 2, 3, 4, 5}
	ps := NewPrefixSum(arr)

	fmt.Println("Index [1..3] yig'indisi (2+3+4):", ps.Query(1, 3))
	fmt.Println("Index [0..4] jami yig'indisi:", ps.Query(0, 4))
}
```

## Tushuntirish va Mantiq:
Prefix sum massivi oldindan bir marta O(N) da tayyorlangach, oraliq yig'indilar bir zumda O(1) da hisoblanadi.

## Ishlash natijasi:
```text
Index [1..3] yig'indisi (2+3+4): 9
Index [0..4] jami yig'indisi: 15
```

# 248-Topshiriq: Slice elementlarini shart bo'yicha ajratish (Partition)
## Topshiriq sharti:
Massivni manfiy va musbat sonlarga ikkiga ajratuvchi funksiya yozing.

## Yechim (Go kodi):
```go
package main

import "fmt"

func partition(arr []int) ([]int, []int) {
	var manfiylar []int
	var musbatlar []int

	for _, x := range arr {
		if x < 0 {
			manfiylar = append(manfiylar, x)
		} else {
			musbatlar = append(musbatlar, x)
		}
	}
	return manfiylar, musbatlar
}

func main() {
	aralash := []int{-5, 12, -3, 0, 45, -1, 8}
	manfiy, musbat := partition(aralash)
	fmt.Println("Manfiylar:", manfiy)
	fmt.Println("Musbatlar:", musbat)
}
```

## Tushuntirish va Mantiq:
Partitioning ma'lumotlarni turli oqimlarga yo'naltirishda qo'llaniladi.

## Ishlash natijasi:
```text
Manfiylar: [-5 -3 -1]
Musbatlar: [12 0 45 8]
```

# 249-Topshiriq: Slicelar ustida Dinamik Massiv (Dynamic Array) bench xatti-harakati
## Topshiriq sharti:
Elementlar soni oshgan sari xotira qanday kengayishini kuzatuvchi funksiya.

## Yechim (Go kodi):
```go
package main

import "fmt"

func main() {
	var s []int
	var o'sishlar []int

	oxirgiCap := 0
	for i := 0; i < 100; i++ {
		s = append(s, i)
		if cap(s) != oxirgiCap {
			oxirgiCap = cap(s)
			o'sishlar = append(o'sishlar, oxirgiCap)
		}
	}

	fmt.Println("100 tagacha qo'shilgandagi sig'im bosqichlari:")
	fmt.Println(o'sishlar)
}
```

## Tushuntirish va Mantiq:
Dinamik massiv eksponentsial o'sish orqali ammortizatsiyalangan O(1) qo'shish vaqtini ta'minlaydi.

## Ishlash natijasi:
```text
100 tagacha qo'shilgandagi sig'im bosqichlari:
[1 2 4 8 16 32 64 128]
```

# 250-Topshiriq: Yakuniy amaliy vazifa: Yuqori unumdorlikdagi Byte Buffer Slice boshqaruvi
## Topshiriq sharti:
Baytlar oqimini yig'uvchi, qayta ishlovchi va xotirani tozalovchi to'liq bufer menejerini yarating.

## Yechim (Go kodi):
```go
package main

import "fmt"

type BaytBufer struct {
	bufer []byte
}

func (b *BaytBufer) Yozish(data []byte) {
	b.bufer = append(b.bufer, data...)
}

func (b *BaytBufer) OqishVaTozalash() []byte {
	natija := make([]byte, len(b.bufer))
	copy(natija, b.bufer)
	b.bufer = b.bufer[:0] // Xotira sig'imini (cap) saqlab uzunlikni nolga tushirish!
	return natija
}

func (b *BaytBufer) Sigim() int {
	return cap(b.bufer)
}

func main() {
	bb := &BaytBufer{}

	bb.Yozish([]byte("Salom "))
	bb.Yozish([]byte("Golang!"))

	fmt.Printf("Bufer hajmi: %d bayt (sig'im: %d)\n", len(bb.bufer), bb.Sigim())

	malumot := bb.OqishVaTozalash()
	fmt.Printf("O'qilgan matn: %s\n", string(malumot))
	fmt.Printf("Tozalangandan keyin uzunlik: %d, sig'im: %d (xotira qayta ishlatiladi)\n", len(bb.bufer), bb.Sigim())
}
```

## Tushuntirish va Mantiq:
`b[:0]` usuli uzunlikni 0 qilib, sig'imni (capacity) saqlab qoladi. Bu esa xotirani qayta ajratmasdan unumdorlikni eng yuqori darajada ushlab turadi.

## Ishlash natijasi:
```text
Bufer hajmi: 13 bayt (sig'im: 16)
O'qilgan matn: Salom Golang!
Tozalangandan keyin uzunlik: 0, sig'im: 16 (xotira qayta ishlatiladi)
```

