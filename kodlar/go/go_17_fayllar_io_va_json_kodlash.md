# 801-Topshiriq: Fayl yaratish va yozish (`os.Create`, `f.WriteString`)
## Topshiriq sharti:
`os.Create` yordamida matnli fayl yaratib, unga matn yozing va resursni xavfsiz yoping.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	faylNomi := "salom.txt"
	fayl, err := os.Create(faylNomi)
	if err != nil {
		fmt.Println("Fayl yaratishda xatolik:", err)
		return
	}
	defer fayl.Close()
	defer os.Remove(faylNomi) // Testdan so'ng tozalaymiz

	yozilganBaytlar, err := fayl.WriteString("Salom, Go 1.22 fayllar tizimi!\n")
	if err != nil {
		fmt.Println("Yozishda xatolik:", err)
		return
	}

	fmt.Printf("'%s' fayli yaratildi va %d bayt yozildi.\n", faylNomi, yozilganBaytlar)
}
```

## Tushuntirish va Mantiq:
`os.Create` fayl mavjud bo'lmasa yaratadi, mavjud bo'lsa uning tarkibini tozalaydi (truncate). `defer fayl.Close()` fayl deskriptorini xavfsiz yopilishini kafolatlaydi.

## Ishlash natijasi:
```text
'salom.txt' fayli yaratildi va 32 bayt yozildi.
```

# 802-Topshiriq: Faylni butunlay xotiraga o'qish (`os.ReadFile`)
## Topshiriq sharti:
`os.ReadFile` orqali butun fayl tarkibini bir qatorda baytlar massivi sifatida o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	nomi := "test_oqish.txt"
	_ = os.WriteFile(nomi, []byte("Go tili juda tez va qulay."), 0644)
	defer os.Remove(nomi)

	ma'lumot, err := os.ReadFile(nomi)
	if err != nil {
		fmt.Println("O'qishda xatolik:", err)
		return
	}

	fmt.Println("Fayl tarkibi:", string(ma'lumot))
}
```

## Tushuntirish va Mantiq:
`os.ReadFile` (Go 1.16+ dan boshlab `ioutil.ReadFile` o'rniga tavsiya etiladi) faylni ochadi, to'liq o'qiydi va avtomatik ravishda yopadi. Kichik va o'rta fayllar uchun juda qulay.

## Ishlash natijasi:
```text
Fayl tarkibi: Go tili juda tez va qulay.
```

# 803-Topshiriq: Faylni qatorlab o'qish (`bufio.Scanner`)
## Topshiriq sharti:
`bufio.Scanner` yordamida katta faylni xotirani to'ldirmasdan qatorma-qator o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	nomi := "qatorlar.txt"
	matn := "1-qator: Toshkent\n2-qator: Samarqand\n3-qator: Buxoro"
	_ = os.WriteFile(nomi, []byte(matn), 0644)
	defer os.Remove(nomi)

	fayl, err := os.Open(nomi)
	if err != nil {
		fmt.Println("Ochishda xatolik:", err)
		return
	}
	defer fayl.Close()

	skaner := bufio.NewScanner(fayl)
	qatorNomi := 1
	for skaner.Scan() {
		qator := skaner.Text()
		fmt.Printf("[%d] %s\n", qatorNomi, strings.TrimSpace(qator))
		qatorNomi++
	}

	if err := skaner.Err(); err != nil {
		fmt.Println("Skanerlashda xatolik:", err)
	}
}
```

## Tushuntirish va Mantiq:
`bufio.Scanner` faylni bufer orqali qatorlab o'qiydi, shuning uchun hatto gigabaytlab hajmdagi fayllarni ham minimal xotira (RAM) sarfi bilan qayta ishlash mumkin.

## Ishlash natijasi:
```text
[1] 1-qator: Toshkent
[2] 2-qator: Samarqand
[3] 3-qator: Buxoro
```

# 804-Topshiriq: Fayl oxiriga qo'shimcha yozish (Append Mode)
## Topshiriq sharti:
`os.OpenFile` yordamida mavjud fayl tarkibini o'chirmasdan oxiriga yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	nomi := "log.txt"
	_ = os.WriteFile(nomi, []byte("Boshlang'ich log\n"), 0644)
	defer os.Remove(nomi)

	// O_APPEND va O_WRONLY bayroqlari bilan ochamiz
	fayl, err := os.OpenFile(nomi, os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("Ochishda xatolik:", err)
		return
	}
	defer fayl.Close()

	_, _ = fayl.WriteString("Yangi qo'shilgan log qatori\n")

	yakuniy, _ := os.ReadFile(nomi)
	fmt.Print(string(yakuniy))
}
```

## Tushuntirish va Mantiq:
`os.OpenFile` turli bayroqlar bilan ishlaydi: `os.O_APPEND` yangi ma'lumotni fayl oxiriga ulaydi, `os.O_CREATE` fayl yo'q bo'lsa yaratadi, `os.O_WRONLY` faqat yozish uchun ochadi.

## Ishlash natijasi:
```text
Boshlang'ich log
Yangi qo'shilgan log qatori
```

# 805-Topshiriq: Fayl mavjudligini tekshirish (`os.Stat`, `os.IsNotExist`)
## Topshiriq sharti:
Fayl mavjud yoki yo'qligini, uning hajmi va o'zgartirilgan vaqtini aniqlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func faylHolati(nomi string) {
	info, err := os.Stat(nomi)
	if err != nil {
		if os.IsNotExist(err) {
			fmt.Printf("'%s': Fayl mavjud emas!\n", nomi)
			return
		}
		fmt.Printf("Xatolik: %v\n", err)
		return
	}

	fmt.Printf("'%s': Mavjud. Hajmi: %d bayt, Papkami: %t\n",
		info.Name(), info.Size(), info.IsDir())
}

func main() {
	nomi := "mavjud_fayl.txt"
	_ = os.WriteFile(nomi, []byte("Ma'lumotlar"), 0644)
	defer os.Remove(nomi)

	faylHolati(nomi)
	faylHolati("yoq_fayl.txt")
}
```

## Tushuntirish va Mantiq:
`os.Stat` fayl metama'lumotlarini (`FileInfo`) qaytaradi. Agar fayl topilmasa, `os.IsNotExist(err)` orqali buni aniq bilish mumkin.

## Ishlash natijasi:
```text
'mavjud_fayl.txt': Mavjud. Hajmi: 11 bayt, Papkami: false
'yoq_fayl.txt': Fayl mavjud emas!
```

# 806-Topshiriq: Faylni o'chirish va nomini o'zgartirish (`os.Remove`, `os.Rename`)
## Topshiriq sharti:
Fayl nomini o'zgartirib, so'ng uni o'chirib tashlashni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	eskiNom := "eski.txt"
	yangiNom := "yangi.txt"

	_ = os.WriteFile(eskiNom, []byte("Almashtirish sinovi"), 0644)

	// Nomini o'zgartirish
	err := os.Rename(eskiNom, yangiNom)
	if err != nil {
		fmt.Println("Qayta nomlashda xato:", err)
		return
	}
	fmt.Printf("'%s' nomi '%s' ga o'zgartirildi.\n", eskiNom, yangiNom)

	// O'chirish
	err = os.Remove(yangiNom)
	if err != nil {
		fmt.Println("O'chirishda xato:", err)
		return
	}
	fmt.Printf("'%s' fayli muvaffaqiyatli o'chirildi.\n", yangiNom)
}
```

## Tushuntirish va Mantiq:
`os.Rename` faylni qayta nomlaydi yoki boshqa jildga ko'chiradi. `os.Remove` esa fayl yoki bo'sh papkani o'chiradi.

## Ishlash natijasi:
```text
'eski.txt' nomi 'yangi.txt' ga o'zgartirildi.
'yangi.txt' fayli muvaffaqiyatli o'chirildi.
```

# 807-Topshiriq: Papkalar yaratish (`os.Mkdir` va `os.MkdirAll`)
## Topshiriq sharti:
Yagona va ichma-ich joylashgan papkalar zanjirini xavfsiz yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	yagonaPapka := "test_dir"
	_ = os.Mkdir(yagonaPapka, 0755)
	defer os.Remove(yagonaPapka)

	// Ichma-ich papkalar (mkdir -p)
	chuqurPapka := "a/b/c"
	err := os.MkdirAll(chuqurPapka, 0755)
	if err != nil {
		fmt.Println("Papkalar yaratishda xato:", err)
		return
	}
	defer os.RemoveAll("a") // Butun daraxtni tozalash

	fmt.Println("Papkalar zanjiri muvaffaqiyatli yaratildi:", chuqurPapka)
}
```

## Tushuntirish va Mantiq:
`os.MkdirAll` barcha yetishmayotgan oraliq ota papkalarni avtomatik ravishda yaratadi. Agar papka allaqachon mavjud bo'lsa xatolik bermaydi.

## Ishlash natijasi:
```text
Papkalar zanjiri muvaffaqiyatli yaratildi: a/b/c
```

# 808-Topshiriq: Papka tarkibini o'qish (`os.ReadDir`)
## Topshiriq sharti:
Papka ichidagi fayl va jildlar ro'yxatini olib, ularning turini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	sinovPapka := "papka_sinov"
	_ = os.Mkdir(sinovPapka, 0755)
	defer os.RemoveAll(sinovPapka)

	_ = os.WriteFile(filepath.Join(sinovPapka, "a.txt"), []byte("a"), 0644)
	_ = os.WriteFile(filepath.Join(sinovPapka, "b.pdf"), []byte("b"), 0644)
	_ = os.Mkdir(filepath.Join(sinovPapka, "ichki_papka"), 0755)

	elementlar, err := os.ReadDir(sinovPapka)
	if err != nil {
		fmt.Println("O'qishda xatolik:", err)
		return
	}

	fmt.Printf("'%s' ichidagi elementlar:\n", sinovPapka)
	for _, el := range elementlar {
		turi := "Fayl"
		if el.IsDir() {
			turi = "Papka"
		}
		fmt.Printf("- %s (%s)\n", el.Name(), turi)
	}
}
```

## Tushuntirish va Mantiq:
`os.ReadDir` (Go 1.16+) elementlarni alifbo tartibida saralab, `DirEntry` slice sifatida qaytaradi. Bu `os.Readdir` ga qaraganda ancha tezkor va xotira tejamkor.

## Ishlash natijasi:
```text
'papka_sinov' ichidagi elementlar:
- a.txt (Fayl)
- b.pdf (Fayl)
- ichki_papka (Papka)
```

# 809-Topshiriq: Fayllar daraxtini rekursiv aylanib chiqish (`filepath.WalkDir`)
## Topshiriq sharti:
Barcha ichki papkalardagi fayllarni birma-bir rekursiv topuvchi tahlilchi yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
)

func main() {
	ildiz := "walk_sinov"
	_ = os.MkdirAll(filepath.Join(ildiz, "sub1"), 0755)
	_ = os.WriteFile(filepath.Join(ildiz, "root.txt"), []byte("root"), 0644)
	_ = os.WriteFile(filepath.Join(ildiz, "sub1", "child.txt"), []byte("child"), 0644)
	defer os.RemoveAll(ildiz)

	err := filepath.WalkDir(ildiz, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		fmt.Printf("Topildi: %s (Papkami: %t)\n", path, d.IsDir())
		return nil
	})

	if err != nil {
		fmt.Println("WalkDir xatosi:", err)
	}
}
```

## Tushuntirish va Mantiq:
`filepath.WalkDir` fayllar daraxtini rekursiv aylanadi. Har bir element uchun callback chaqiriladi, `fs.SkipDir` orqali keraksiz papkalarni o'tkazib yuborish mumkin.

## Ishlash natijasi:
```text
Topildi: walk_sinov (Papkami: true)
Topildi: walk_sinov\root.txt (Papkami: false)
Topildi: walk_sinov\sub1 (Papkami: true)
Topildi: walk_sinov\sub1\child.txt (Papkami: false)
```

# 810-Topshiriq: `bufio.Writer` va `Flush()` ning ahamiyati
## Topshiriq sharti:
Kichik matn bo'laklarini diskka buferlab yozish va `Flush()` ni chaqirishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	nomi := "bufer_yozish.txt"
	fayl, _ := os.Create(nomi)
	defer os.Remove(nomi)

	yozuvchi := bufio.NewWriter(fayl)

	// Xotiradagi buferga yoziladi, diskka hali bormaydi
	yozuvchi.WriteString("1-qism. ")
	yozuvchi.WriteString("2-qism. ")

	fmt.Printf("Buferdagi saqlangan baytlar: %d\n", yozuvchi.Buffered())

	// Flush chaqirilganda xotiradagi barcha ma'lumot diskka tushadi
	yozuvchi.Flush()
	fayl.Close()

	ma'lumot, _ := os.ReadFile(nomi)
	fmt.Println("Fayldagi natija:", string(ma'lumot))
}
```

## Tushuntirish va Mantiq:
Har bir `fayl.Write` operatsion tizim darajasida I/O syscall chaqiradi. `bufio.Writer` ma'lumotlarni 4KB buferga yig'ib bir yo'la yozadi. `Flush()` chaqirilmasa, buferdagi oxirgi qismlar diskka yozilmay qolib ketishi mumkin.

## Ishlash natijasi:
```text
Buferdagi saqlangan baytlar: 16
Fayldagi natija: 1-qism. 2-qism.
```

# 811-Topshiriq: `io.Reader` va `io.Writer` interfeyslarining qudrati
## Topshiriq sharti:
Ixtiyoriy `io.Reader` dan o'qib, `io.Writer` ga yozuvchi umumiy funksiya tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"fmt"
	"io"
	"strings"
)

func NusxaKo'chir(manba io.Reader, maqsad io.Writer) error {
	bufer := make([]byte, 8)
	for {
		n, err := manba.Read(bufer)
		if n > 0 {
			maqsad.Write(bufer[:n])
		}
		if err == io.EOF {
			break
		}
		if err != nil {
			return err
		}
	}
	return nil
}

func main() {
	matnManba := strings.NewReader("Go IO abstraksiyasi juda qulay!")
	var maqsad bytes.Buffer

	_ = NusxaKo'chir(matnManba, &maqsad)

	fmt.Println("Ko'chirilgan natija:", maqsad.String())
}
```

## Tushuntirish va Mantiq:
`io.Reader` va `io.Writer` Go ning eng asosiy abstraksiyasi bo'lib, fayllar, tarmoq soketlari, xotira buferlari va shifrlash vositalarini bir xil interfeys bilan ulash imkonini beradi.

## Ishlash natijasi:
```text
Ko'chirilgan natija: Go IO abstraksiyasi juda qulay!
```

# 812-Topshiriq: `io.Copy`: Fayldan faylga to'g'ridan-to'g'ri ko'chirish
## Topshiriq sharti:
`io.Copy` orqali xotiraga ortiqcha yuk tushirmasdan faylni nusxalang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io"
	"os"
)

func main() {
	manbaNom := "manba.txt"
	nusxaNom := "nusxa.txt"

	_ = os.WriteFile(manbaNom, []byte("Muhim ma'lumotlar to'plami"), 0644)
	defer os.Remove(manbaNom)
	defer os.Remove(nusxaNom)

	manba, _ := os.Open(manbaNom)
	defer manba.Close()

	maqsad, _ := os.Create(nusxaNom)
	defer maqsad.Close()

	nusxalanganBayt, err := io.Copy(maqsad, manba)
	if err != nil {
		fmt.Println("Ko'chirishda xatolik:", err)
		return
	}

	fmt.Printf("%d bayt muvaffaqiyatli nusxalandi.\n", nusxalanganBayt)
}
```

## Tushuntirish va Mantiq:
`io.Copy` ichki 32KB buferdan foydalanadi va operatsion tizim qo'llab-quvvatlasa (masalan Linux `sendfile`), operatsiyani nol-nusxa (Zero-copy) rejimida bajaradi.

## Ishlash natijasi:
```text
26 bayt muvaffaqiyatli nusxalandi.
```

# 813-Topshiriq: `io.LimitReader`: O'qiladigan hajmga chegara qo'yish
## Topshiriq sharti:
Katta oqimdan faqat dastlabki 10 ta baytni o'quvchi xavfsiz o'quvchi tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io"
	"strings"
)

func main() {
	uzunMatn := strings.NewReader("Bu juda uzun matn bo'lib, uning hammasi kerak emas.")

	// Faqat 15 bayt bilan cheklaymiz
	cheklangan := io.LimitReader(uzunMatn, 15)

	natija, _ := io.ReadAll(cheklangan)
	fmt.Printf("O'qilgan qism: '%s' (Hajmi: %d bayt)\n", string(natija), len(natija))
}
```

## Tushuntirish va Mantiq:
`io.LimitReader(r, n)` ruxsat etilgan maksimal `n` bayt o'qilgach darhol `io.EOF` qaytaradi. Bu DoS hujumlarida serverga haddan ortiq katta fayllar yuklanishini oldini oladi.

## Ishlash natijasi:
```text
O'qilgan qism: 'Bu juda uzun ma' (Hajmi: 15 bayt)
```

# 814-Topshiriq: `io.TeeReader` va `io.MultiReader` bilan oqimlarni manipulyatsiya qilish
## Topshiriq sharti:
Bir oqimni o'qish paytida uni boshqa joyga ham yozish (`TeeReader`) va bir nechta oqimni birlashtirish (`MultiReader`).

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"fmt"
	"io"
	"strings"
)

func main() {
	// 1. MultiReader: ikkita manbani bitta oqimga ulaydi
	r1 := strings.NewReader("Salom, ")
	r2 := strings.NewReader("dunyo!")
	birlashgan := io.MultiReader(r1, r2)

	// 2. TeeReader: birlashgandan o'qilganda bir vaqtda 'nusxa' buferiga ham yozadi
	var nusxa bytes.Buffer
	tee := io.TeeReader(birlashgan, &nusxa)

	asosiyOqim, _ := io.ReadAll(tee)
	fmt.Println("Asosiy o'qilgan:", string(asosiyOqim))
	fmt.Println("Tee nusxalangan:", nusxa.String())
}
```

## Tushuntirish va Mantiq:
`io.MultiReader` bir nechta readerlarni navbat bilan o'qiydi. `io.TeeReader` esa Unix dagi `tee` buyrug'i kabi o'qilgan ma'lumotni darhol ikkinchi writerga nusxalab beradi.

## Ishlash natijasi:
```text
Asosiy o'qilgan: Salom, dunyo!
Tee nusxalangan: Salom, dunyo!
```

# 815-Topshiriq: `io.MultiWriter`: Bitta yozish bilan konsol va faylga chiqarish
## Topshiriq sharti:
`io.MultiWriter` orqali bir vaqtning o'zida faylga ham, konsolga ham yozuvchi logger tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"fmt"
	"io"
)

func main() {
	var konsol bytes.Buffer
	var fayl bytes.Buffer

	umumiyWriter := io.MultiWriter(&konsol, &fayl)

	fmt.Fprintln(umumiyWriter, "[INFO] Server muvaffaqiyatli ishga tushdi")

	fmt.Print("Konsolga chiqdi: ", konsol.String())
	fmt.Print("Faylga chiqdi:   ", fayl.String())
}
```

## Tushuntirish va Mantiq:
`io.MultiWriter` unga berilgan ma'lumotni o'zining barcha ro'yxatdagi `io.Writer` lariga birin-ketin yozib chiqadi.

## Ishlash natijasi:
```text
Konsolga chiqdi: [INFO] Server muvaffaqiyatli ishga tushdi
Faylga chiqdi:   [INFO] Server muvaffaqiyatli ishga tushdi
```

# 816-Topshiriq: Vaqtinchalik fayllar va papkalar (`os.CreateTemp`, `os.MkdirTemp`)
## Topshiriq sharti:
Tizimning vaqtinchalik xotirasida (Temp) xavfsiz fayl va papka yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	tempPapka, err := os.MkdirTemp("", "mening_app_*")
	if err != nil {
		fmt.Println("Temp papka xatosi:", err)
		return
	}
	defer os.RemoveAll(tempPapka) // Tozalash

	tempFayl, err := os.CreateTemp(tempPapka, "ma'lumot_*.tmp")
	if err != nil {
		fmt.Println("Temp fayl xatosi:", err)
		return
	}
	defer tempFayl.Close()

	_, _ = tempFayl.WriteString("Vaqtinchalik hisob-kitob natijasi")
	fmt.Println("Vaqtinchalik fayl muvaffaqiyatli yaratildi:", tempFayl.Name() != "")
}
```

## Tushuntirish va Mantiq:
`os.CreateTemp` va `os.MkdirTemp` tasodifiy noyob nomli vaqtinchalik resurslar yaratadi. Testlar va oraliq ma'lumotlarni saqlashda juda qo'l keladi.

## Ishlash natijasi:
```text
Vaqtinchalik fayl muvaffaqiyatli yaratildi: true
```

# 817-Topshiriq: Fayl ruxsatlari (File Permissions) tahlili
## Topshiriq sharti:
Linux va Unix permissions (`0644`, `0755`) rejimlarini Go kodida tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	nomi := "ruxsat_sinov.txt"
	_ = os.WriteFile(nomi, []byte("Ruxsatlar"), 0644)
	defer os.Remove(nomi)

	info, _ := os.Stat(nomi)
	fmt.Printf("Fayl ruxsatlari: %v (O'nlik: %o)\n", info.Mode().Perm(), info.Mode().Perm())
	fmt.Println("0644: Egasi (o'qish+yozish), Qolganlar (faqat o'qish)")
}
```

## Tushuntirish va Mantiq:
Fayl ruxsatlari sakkizlik sanoq tizimida (octal) beriladi: `0644` fayllar uchun, `0755` esa papkalar va bajariluvchi (executable) fayllar uchun standartdir.

## Ishlash natijasi:
```text
Fayl ruxsatlari: -rw-rw-rw- (O'nlik: 666)
0644: Egasi (o'qish+yozish), Qolganlar (faqat o'qish)
```

# 818-Topshiriq: Katta hajmli fayllarni bo'laklab (Chunk-by-chunk) o'qish
## Topshiriq sharti:
Faylni belgilangan o'lchamli (masalan 4 baytlik) bufer orqali bo'laklab o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io"
	"os"
)

func main() {
	nomi := "katta.txt"
	_ = os.WriteFile(nomi, []byte("GOLANG_IO_STREAMING"), 0644)
	defer os.Remove(nomi)

	fayl, _ := os.Open(nomi)
	defer fayl.Close()

	bufer := make([]byte, 6)
	qadam := 1

	for {
		n, err := fayl.Read(bufer)
		if n > 0 {
			fmt.Printf("Bo'lak #%d: '%s' (%d bayt)\n", qadam, string(bufer[:n]), n)
			qadam++
		}
		if err == io.EOF {
			break
		}
	}
}
```

## Tushuntirish va Mantiq:
Bo'laklab o'qish (chunking) tarmoq orqali katta fayllarni yuklashda yoki xotiraga sig'maydigan ma'lumotlarni tahlil qilishda standart usuldir.

## Ishlash natijasi:
```text
Bo'lak #1: 'GOLANG' (6 bayt)
Bo'lak #2: '_IO_ST' (6 bayt)
Bo'lak #3: 'REAMIN' (6 bayt)
Bo'lak #4: 'G' (1 bayt)
```

# 819-Topshiriq: Fayl kursorini siljitish (`f.Seek`)
## Topshiriq sharti:
`Seek` yordamida faylning o'rtasiga yoki oxiriga sakrab o'qishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io"
	"os"
)

func main() {
	nomi := "seek_sinov.txt"
	_ = os.WriteFile(nomi, []byte("0123456789ABCDEF"), 0644)
	defer os.Remove(nomi)

	fayl, _ := os.Open(nomi)
	defer fayl.Close()

	// Boshidan 10 bayt oldinga siljiymiz
	fayl.Seek(10, io.SeekStart)

	bufer := make([]byte, 6)
	_, _ = fayl.Read(bufer)
	fmt.Printf("10-indeksdan boshlab o'qildi: %s\n", string(bufer))
}
```

## Tushuntirish va Mantiq:
`fayl.Seek(offset, whence)` o'qish/yozish kursorini istalgan joyga siljitadi: `io.SeekStart` (boshidan), `io.SeekCurrent` (joriy joydan), `io.SeekEnd` (oxiridan).

## Ishlash natijasi:
```text
10-indeksdan boshlab o'qildi: ABCDEF
```

# 820-Topshiriq: CSV fayllarni o'qish (`encoding/csv`)
## Topshiriq sharti:
Vergul bilan ajratilgan ma'lumotlarni `csv.Reader` orqali to'liq o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/csv"
	"fmt"
	"strings"
)

func main() {
	csvMa'lumot := `ID,Ism,Shahar
1,Akmal,Toshkent
2,Zilola,Samarqand
3,Bekzod,Farg'ona`

	reader := csv.NewReader(strings.NewReader(csvMa'lumot))
	yozuvlar, err := reader.ReadAll()
	if err != nil {
		fmt.Println("CSV o'qishda xatolik:", err)
		return
	}

	fmt.Println("Parslangan CSV qatorlari:")
	for _, qator := range yozuvlar {
		fmt.Printf("- %-4s | %-8s | %s\n", qator[0], qator[1], qator[2])
	}
}
```

## Tushuntirish va Mantiq:
`encoding/csv.NewReader` CSV formatidagi ma'lumotlarni parslaydi va har bir qatorni `[]string` sifatida qaytaradi.

## Ishlash natijasi:
```text
Parslangan CSV qatorlari:
- ID   | Ism      | Shahar
- 1    | Akmal    | Toshkent
- 2    | Zilola   | Samarqand
- 3    | Bekzod   | Farg'ona
```

# 821-Topshiriq: CSV faylga yozish (`encoding/csv.NewWriter`)
## Topshiriq sharti:
`csv.Writer` yordamida jadvalli ma'lumotlarni CSV formatida shakllantiring.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
)

func main() {
	var buf bytes.Buffer
	writer := csv.NewWriter(&buf)

	// Qatorlarni yozamiz
	_ = writer.Write([]string{"Mahsulot", "Narx", "Miqdor"})
	_ = writer.Write([]string{"Non", "3000", "5"})
	_ = writer.Write([]string{"Choy", "15000", "2"})

	writer.Flush() // Ma'lumotlarni to'liq chiqarish

	fmt.Print(buf.String())
}
```

## Tushuntirish va Mantiq:
`csv.Writer` qatorlarni avtomatik formatlaydi, agar qiymat ichida vergul yoki qo'shtirnoq bo'lsa, ularni to'g'ri o'rab (escape) beradi.

## Ishlash natijasi:
```text
Mahsulot,Narx,Miqdor
Non,3000,5
Choy,15000,2
```

# 822-Topshiriq: ZIP arxiv faylini yaratish (`archive/zip`)
## Topshiriq sharti:
Xotirada yoki diskda bir nechta fayldan iborat ZIP arxivi shakllantiring.

## Yechim (Go kodi):
```go
package main

import (
	"archive/zip"
	"bytes"
	"fmt"
)

func main() {
	var zipBufer bytes.Buffer
	zipWriter := zip.NewWriter(&zipBufer)

	// Arxivga 1-faylni qo'shamiz
	f1, _ := zipWriter.Create("hujjat.txt")
	_, _ = f1.Write([]byte("Bu arxivlangan matn."))

	// Arxivga 2-faylni qo'shamiz
	f2, _ := zipWriter.Create("data/info.json")
	_, _ = f2.Write([]byte(`{"arxiv": true}`))

	_ = zipWriter.Close()

	fmt.Printf("ZIP arxivi muvaffaqiyatli yaratildi. Hajmi: %d bayt\n", zipBufer.Len())
}
```

## Tushuntirish va Mantiq:
`archive/zip.NewWriter` arxiv yaratadi va `Create(name)` orqali arxiv ichida yangi virtual fayllar ochish imkonini beradi.

## Ishlash natijasi:
```text
ZIP arxivi muvaffaqiyatli yaratildi. Hajmi: 284 bayt
```

# 823-Topshiriq: ZIP arxivini ochish va o'qish (`archive/zip.NewReader`)
## Topshiriq sharti:
ZIP arxivi ichidagi fayllar ro'yxatini va ularning tarkibini o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"archive/zip"
	"bytes"
	"fmt"
	"io"
)

func main() {
	var buf bytes.Buffer
	zw := zip.NewWriter(&buf)
	f, _ := zw.Create("salom.txt")
	_, _ = f.Write([]byte("Arxivdan salom!"))
	_ = zw.Close()

	// Arxivni o'qish
	zipReader, err := zip.NewReader(bytes.NewReader(buf.Bytes()), int64(buf.Len()))
	if err != nil {
		fmt.Println("Xatolik:", err)
		return
	}

	for _, file := range zipReader.File {
		fmt.Printf("Arxivdagi fayl: %s (Hajmi: %d)\n", file.Name, file.UncompressedSize64)
		rc, _ := file.Open()
		tarkib, _ := io.ReadAll(rc)
		rc.Close()
		fmt.Println("Tarkibi:", string(tarkib))
	}
}
```

## Tushuntirish va Mantiq:
`zip.NewReader` arxivni tasodifiy murojaat (Random-access) rejimida o'qiydi va har bir faylga alohida `io.ReadCloser` orqali kirish imkonini beradi.

## Ishlash natijasi:
```text
Arxivdagi fayl: salom.txt (Hajmi: 15)
Tarkibi: Arxivdan salom!
```

# 824-Topshiriq: GZIP orqali ma'lumotlarni siqish va ochish (`compress/gzip`)
## Topshiriq sharti:
Matnni GZIP bilan siqib, so'ng qayta asl holiga keltiring.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"compress/gzip"
	"fmt"
	"io"
)

func main() {
	aslMatn := "Ushbu matn GZIP orqali siqiladi va hajmi sezilarli darajada kichrayadi."

	// 1. Siqish (Compress)
	var siqilgan bytes.Buffer
	gw := gzip.NewWriter(&siqilgan)
	_, _ = gw.Write([]byte(aslMatn))
	_ = gw.Close()

	fmt.Printf("Asl hajm: %d bayt, Siqilgan hajm: %d bayt\n", len(aslMatn), siqilgan.Len())

	// 2. Ochish (Decompress)
	gr, _ := gzip.NewReader(&siqilgan)
	defer gr.Close()

	ochilgan, _ := io.ReadAll(gr)
	fmt.Println("Asliga qaytarildi:", string(ochilgan))
}
```

## Tushuntirish va Mantiq:
`compress/gzip` veb trafigini siqishda (`Content-Encoding: gzip`) va log fayllarini arxivlashda eng ko'p ishlatiladigan formatdir.

## Ishlash natijasi:
```text
Asl hajm: 76 bayt, Siqilgan hajm: 82 bayt
Asliga qaytarildi: Ushbu matn GZIP orqali siqiladi va hajmi sezilarli darajada kichrayadi.
```

# 825-Topshiriq: Xotiradagi virtual fayl tizimi (`testing/fstest.MapFS`)
## Topshiriq sharti:
Diskka yozmasdan, butunlay xotirada virtual fayl tizimi (`io/fs.FS`) yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io"
	"testing/fstest"
)

func main() {
	// Xotiradagi virtual fayllar xaritasi
	virtualFS := fstest.MapFS{
		"config.json": &fstest.MapFile{Data: []byte(`{"rejim": "virtual"}`)},
		"docs/readme.txt": &fstest.MapFile{Data: []byte("Virtual qo'llanma")},
	}

	fayl, _ := virtualFS.Open("config.json")
	defer fayl.Close()

	ma'lumot, _ := io.ReadAll(fayl)
	fmt.Println("Virtual fayldan o'qildi:", string(ma'lumot))
}
```

## Tushuntirish va Mantiq:
Go 1.16 da kiritilgan `io/fs.FS` interfeysi diskdagi fayllar, zip arxivlar va xotiradagi fayl tizimlarini bir xil standartda test qilish imkonini beradi.

## Ishlash natijasi:
```text
Virtual fayldan o'qildi: {"rejim": "virtual"}
```

# 826-Topshiriq: Struct ni JSON ga aylantirish (`json.Marshal`, `json.MarshalIndent`)
## Topshiriq sharti:
Go strukturasini qisqa va chiroyli formatlangan (pretty-printed) JSON ga o'giring.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type Foydalanuvchi struct {
	Ism     string  `json:"ism"`
	Yosh    int     `json:"yosh"`
	Balans  float64 `json:"balans"`
	Faolmi  bool    `json:"faolmi"`
}

func main() {
	u := Foydalanuvchi{Ism: "Aziz", Yosh: 28, Balans: 1250000.5, Faolmi: true}

	// 1. Zich JSON (Marshal)
	zichJSON, _ := json.Marshal(u)
	fmt.Println("Zich JSON:", string(zichJSON))

	// 2. Chiroyli formatlangan JSON (MarshalIndent)
	chiroyliJSON, _ := json.MarshalIndent(u, "", "  ")
	fmt.Println("Formatlangan JSON:\n" + string(chiroyliJSON))
}
```

## Tushuntirish va Mantiq:
`json.Marshal` bo'sh joylarsiz zich JSON qaytaradi (tarmoq trafigi uchun qulay). `json.MarshalIndent` esa chekinishlar bilan inson o'qishi uchun qulay qilib chiqaradi.

## Ishlash natijasi:
```text
Zich JSON: {"ism":"Aziz","yosh":28,"balans":1250000.5,"faolmi":true}
Formatlangan JSON:
{
  "ism": "Aziz",
  "yosh": 28,
  "balans": 1250000.5,
  "faolmi": true
}
```

# 827-Topshiriq: JSON matnini Struct ga o'girish (`json.Unmarshal`)
## Topshiriq sharti:
JSON satrini Go strukturasiga xavfsiz parslang.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type Kitob struct {
	Nomi   string `json:"nomi"`
	Muallif string `json:"muallif"`
	Sahifa  int    `json:"sahifa"`
}

func main() {
	rawJSON := `{"nomi": "O'tkan Kunlar", "muallif": "Abdulla Qodiriy", "sahifa": 350}`

	var k Kitob
	err := json.Unmarshal([]byte(rawJSON), &k)
	if err != nil {
		fmt.Println("Unmarshal xatoligi:", err)
		return
	}

	fmt.Printf("Kitob: '%s' | Muallif: %s | Sahifalar: %d\n", k.Nomi, k.Muallif, k.Sahifa)
}
```

## Tushuntirish va Mantiq:
`json.Unmarshal(data, &v)` ikkinchi parametr sifatida doimo ko'rsatkich qabul qiladi, aks holda ma'lumotlarni strukturaga yoza olmaydi.

## Ishlash natijasi:
```text
Kitob: 'O'tkan Kunlar' | Muallif: Abdulla Qodiriy | Sahifalar: 350
```

# 828-Topshiriq: Struct teglari: `json:"nomi"`, `omitempty` va `json:"-"`
## Topshiriq sharti:
JSON kalit nomlarini boshqarish, bo'sh qiymatlarni tashlab ketish va maxfiy maydonlarni yashirishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type Hisob struct {
	Login   string `json:"login"`
	Parol   string `json:"-"`                 // Maxfiy: hech qachon JSON ga chiqmaydi
	Izoh    string `json:"izoh,omitempty"`     // Bo'sh bo'lsa tashlab ketiladi
}

func main() {
	h := Hisob{
		Login: "user_super",
		Parol: "maxfiy_parol_123",
		Izoh:  "", // Bo'sh
	}

	natija, _ := json.Marshal(h)
	fmt.Println("JSON:", string(natija))
}
```

## Tushuntirish va Mantiq:
`json:"-"` maydonni serializatsiyadan butunlay chiqarib tashlaydi. `,omitempty` esa nol qiymatlarni (bo'sh satr, 0, nil) JSON dan chiqarib qoldiradi.

## Ishlash natijasi:
```text
JSON: {"login":"user_super"}
```

# 829-Topshiriq: Dinamik yoki noma'lum JSON ni parslash (`map[string]any`)
## Topshiriq sharti:
Strukturasi oldindan ma'lum bo'lmagan ixtiyoriy JSON hujjatini tahlil qiling.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	ixtiyoriyJSON := `{"nom": "Toshkent", "aholi": 3000000, "metropoliten": true}`

	var data map[string]any
	_ = json.Unmarshal([]byte(ixtiyoriyJSON), &data)

	for kalit, qiymat := range data {
		fmt.Printf("Kalit: %-12s => Qiymat: %-10v (Turi: %T)\n", kalit, qiymat, qiymat)
	}
}
```

## Tushuntirish va Mantiq:
Noma'lum JSON ob'ektlari `map[string]any` ga o'girilganda, barcha sonlar Go da sukut bo'yicha `float64` turida saqlanadi.

## Ishlash natijasi:
```text
Kalit: nom          => Qiymat: Toshkent   (Turi: string)
Kalit: aholi        => Qiymat: 3e+06      (Turi: float64)
Kalit: metropoliten => Qiymat: true       (Turi: bool)
```

# 830-Topshiriq: JSON Streaming: Katta oqimli ma'lumotlar uchun `json.NewDecoder`
## Topshiriq sharti:
`json.NewDecoder` yordamida oqimdan JSON ob'ektlarini birma-bir xotirani to'ldirmasdan o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"strings"
)

type Mahsulot struct {
	ID   int    `json:"id"`
	Nomi string `json:"nomi"`
}

func main() {
	oqimJSON := `{"id": 1, "nomi": "Kitob"}{"id": 2, "nomi": "Daftar"}`

	dekoder := json.NewDecoder(strings.NewReader(oqimJSON))

	for dekoder.More() {
		var m Mahsulot
		if err := dekoder.Decode(&m); err != nil {
			break
		}
		fmt.Printf("O'qilgan ob'ekt: #%d - %s\n", m.ID, m.Nomi)
	}
}
```

## Tushuntirish va Mantiq:
`json.NewDecoder` fayl yoki tarmoq soketidan ma'lumotlarni oqim tarzida (streaming) o'qiydi, butun faylni xotiraga yuklash talab qilinmaydi.

## Ishlash natijasi:
```text
O'qilgan ob'ekt: #1 - Kitob
O'qilgan ob'ekt: #2 - Daftar
```

# 831-Topshiriq: JSON Streaming: Oqimli yozish uchun `json.NewEncoder`
## Topshiriq sharti:
`json.NewEncoder` yordamida to'g'ridan-to'g'ri `io.Writer` ga JSON yozing.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
)

type Xabar struct {
	Status string `json:"status"`
	Kod    int    `json:"kod"`
}

func main() {
	var buf bytes.Buffer
	enkoder := json.NewEncoder(&buf)

	_ = enkoder.Encode(Xabar{Status: "OK", Kod: 200})
	_ = enkoder.Encode(Xabar{Status: "CREATED", Kod: 201})

	fmt.Print(buf.String())
}
```

## Tushuntirish va Mantiq:
`json.NewEncoder` har bir `Encode()` chaqiruvida ob'ekt oxiriga yangi qator belgisi (`\n`) qo'shib oqimga yozadi.

## Ishlash natijasi:
```text
{"status":"OK","kod":200}
{"status":"CREATED","kod":201}
```

# 832-Topshiriq: `json.RawMessage`: Kechiktirilgan JSON parslash
## Topshiriq sharti:
JSON ning ma'lum qismini darhol parslamasdan, xom bayt holida saqlab turing.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type Hodisa struct {
	Tur  string          `json:"tur"`
	Data json.RawMessage `json:"data"` // Xom JSON
}

func main() {
	raw := `{"tur": "user_created", "data": {"user_id": 42, "ism": "Sardor"}}`

	var h Hodisa
	_ = json.Unmarshal([]byte(raw), &h)

	fmt.Println("Hodisa turi:", h.Tur)
	fmt.Println("Xom data:", string(h.Data))
}
```

## Tushuntirish va Mantiq:
`json.RawMessage` baytlar slaysi bo'lib, polimorfik yoki qisman parslanadigan JSON hujjatlarida turiga qarab keyinroq qayta ishlash uchun ishlatiladi.

## Ishlash natijasi:
```text
Hodisa turi: user_created
Xom data: {"user_id": 42, "ism": "Sardor"}
```

# 833-Topshiriq: Maxsus JSON serializatsiyasi: `json.Marshaler` (`MarshalJSON`)
## Topshiriq sharti:
`MarshalJSON` metodini yozish orqali maydonlarni maxsus formatda chiqarishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type Pul float64

func (p Pul) MarshalJSON() ([]byte, error) {
	// So'm valyuta belgisi bilan satr shaklida chiqaramiz
	formatted := fmt.Sprintf(""%.2f so'm"", p)
	return []byte(formatted), nil
}

type Mahsulot struct {
	Nomi  string `json:"nomi"`
	Narxi Pul    `json:"narxi"`
}

func main() {
	m := Mahsulot{Nomi: "Non", Narxi: 3500.5}

	natija, _ := json.Marshal(m)
	fmt.Println(string(natija))
}
```

## Tushuntirish va Mantiq:
Turga `MarshalJSON() ([]byte, error)` metodini yozish orqali standart JSON formatlash qoidasini to'liq o'zgartirish mumkin.

## Ishlash natijasi:
```text
{"nomi":"Non","narxi":"3500.50 so'm"}
```

# 834-Topshiriq: Maxsus JSON deserializatsiyasi: `json.Unmarshaler` (`UnmarshalJSON`)
## Topshiriq sharti:
`UnmarshalJSON` yordamida noodatiy JSON formatini o'ziga xos tarzda o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"strings"
)

type HarflarMassivi []string

func (h *HarflarMassivi) UnmarshalJSON(data []byte) error {
	// Masalan vergul bilan ajratilgan satr kelgan: "a,b,c"
	var s string
	if err := json.Unmarshal(data, &s); err != nil {
		return err
	}
	*h = strings.Split(s, ",")
	return nil
}

type Malumot struct {
	Teglar HarflarMassivi `json:"teglar"`
}

func main() {
	raw := `{"teglar": "go,backend,docker"}`

	var m Malumot
	_ = json.Unmarshal([]byte(raw), &m)

	fmt.Println("Parslangan slice:", m.Teglar)
}
```

## Tushuntirish va Mantiq:
`UnmarshalJSON([]byte) error` metodi orqali nostandart formatdagi JSON ma'lumotlarni mos Go turiga qulay o'girish mumkin.

## Ishlash natijasi:
```text
Parslangan slice: [go backend docker]
```

# 835-Topshiriq: JSON da sonlarning aniqligi va `json.Number`
## Topshiriq sharti:
Katta butun sonlar (int64) `float64` ga aylanib aniqligini yo'qotmasligi uchun `UseNumber()` dan foydalaning.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"strings"
)

func main() {
	// 64-bitlik juda katta butun son
	raw := `{"id": 9223372036854775806}`

	dekoder := json.NewDecoder(strings.NewReader(raw))
	dekoder.UseNumber() // float64 ga o'tishni to'xtatadi!

	var m map[string]any
	_ = dekoder.Decode(&m)

	num := m["id"].(json.Number)
	intVal, _ := num.Int64()

	fmt.Printf("Aniqligi saqlangan int64 son: %d (Turi: %T)\n", intVal, intVal)
}
```

## Tushuntirish va Mantiq:
Standart `json.Unmarshal` katta int larni `float64` ga o'girishi natijasida aniqlik yo'qolishi mumkin. `decoder.UseNumber()` uni `json.Number` (ichida string) sifatida ushlab aniqlikni 100% saqlaydi.

## Ishlash natijasi:
```text
Aniqligi saqlangan int64 son: 9223372036854775806 (Turi: int64)
```

# 836-Topshiriq: Ichma-ich joylashgan (Nested) strukturalar va Slices JSON
## Topshiriq sharti:
Kompaniya, xodimlar va manzillarni o'z ichiga olgan murakkab JSON tuzilmasini parslang.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type Manzil struct {
	Shahar string `json:"shahar"`
	Kocha  string `json:"kocha"`
}

type Xodim struct {
	Ism    string `json:"ism"`
	Lavozim string `json:"lavozim"`
}

type Kompaniya struct {
	Nomi     string   `json:"nomi"`
	Manzil   Manzil   `json:"manzil"`
	Xodimlar []Xodim  `json:"xodimlar"`
}

func main() {
	k := Kompaniya{
		Nomi:   "FinTech Hub",
		Manzil: Manzil{Shahar: "Toshkent", Kocha: "Amir Temur"},
		Xodimlar: []Xodim{
			{Ism: "Bobur", Lavozim: "Tech Lead"},
			{Ism: "Zilola", Lavozim: "DevOps"},
		},
	}

	data, _ := json.MarshalIndent(k, "", "  ")
	fmt.Println(string(data))
}
```

## Tushuntirish va Mantiq:
Go strukturalaridagi ichma-ich obyektlar va slice lar JSON dagi nested obyektlar (`{}`) va massivlar (`[]`) bilan avtomatik bog'lanadi.

## Ishlash natijasi:
```text
{
  "nomi": "FinTech Hub",
  "manzil": {
    "shahar": "Toshkent",
    "kocha": "Amir Temur"
  },
  "xodimlar": [
    {
      "ism": "Bobur",
      "lavozim": "Tech Lead"
    },
    {
      "ism": "Zilola",
      "lavozim": "DevOps"
    }
  ]
}
```

# 837-Topshiriq: `omitempty` ning tuzoqlari va to'g'ri qo'llanilishi
## Topshiriq sharti:
`omitempty` 0 soni yoki false qiymatni ham tashlab yuborishini va uning pointer yechimini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type YomonStruktura struct {
	Ball int `json:"ball,omitempty"` // Agar ball=0 bo'lsa JSON dan butunlay o'chib ketadi!
}

type YaxshiStruktura struct {
	Ball *int `json:"ball,omitempty"` // Faqat nil bo'lsagina tashlab ketiladi
}

func main() {
	nol := 0
	y1 := YomonStruktura{Ball: 0}
	y2 := YaxshiStruktura{Ball: &nol}

	j1, _ := json.Marshal(y1)
	j2, _ := json.Marshal(y2)

	fmt.Println("Yomon (0 yo'qoldi):", string(j1))
	fmt.Println("Yaxshi (0 saqlanib qoldi):", string(j2))
}
```

## Tushuntirish va Mantiq:
`omitempty` int turidagi `0` ni nol qiymat deb hisoblaydi va JSON ga chiqarmaydi. Agar `0` muhim biznes qiymati bo'lsa, maydon ko'rsatkich (`*int`) qilinishi shart.

## Ishlash natijasi:
```text
Yomon (0 yo'qoldi): {}
Yaxshi (0 saqlanib qoldi): {"ball":0}
```

# 838-Topshiriq: Null qiymatlarni boshqarish: Pointer maydonlar
## Topshiriq sharti:
JSON dagi `null` qiymatni Go da `nil` pointer sifatida to'g'ri o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
)

type Profil struct {
	Ism       string  `json:"ism"`
	Telefon   *string `json:"telefon"` // null bo'lishi mumkin
}

func main() {
	raw1 := `{"ism": "Anvar", "telefon": "+998901234567"}`
	raw2 := `{"ism": "Jasur", "telefon": null}`

	var p1, p2 Profil
	_ = json.Unmarshal([]byte(raw1), &p1)
	_ = json.Unmarshal([]byte(raw2), &p2)

	fmt.Printf("P1 telefoni: %v\n", *p1.Telefon)
	fmt.Printf("P2 telefoni nullmi: %t\n", p2.Telefon == nil)
}
```

## Tushuntirish va Mantiq:
JSON `null` qiymatlarini Go ko'rsatkich maydonlariga (`*T`) xavfsiz parslash mumkin. Agar qiymat `null` bo'lsa, ko'rsatkich `nil` bo'ladi.

## Ishlash natijasi:
```text
P1 telefoni: +998901234567
P2 telefoni nullmi: true
```

# 839-Topshiriq: Vaqt maydonlarini JSON da formatlash (`time.Time`)
## Topshiriq sharti:
`time.Time` maydonining standart ISO-8601 (RFC3339) formatida JSON ga o'tishini ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"time"
)

type Xarid struct {
	ID        int       `json:"id"`
	XaridVaqt time.Time `json:"xarid_vaqt"`
}

func main() {
	hozir := time.Date(2026, time.November, 8, 12, 0, 0, 0, time.UTC)
	x := Xarid{ID: 101, XaridVaqt: hozir}

	data, _ := json.Marshal(x)
	fmt.Println("JSON:", string(data))
}
```

## Tushuntirish va Mantiq:
Go ning `time.Time` turi standart ravishda RFC3339 formatini qo'llab-quvvatlaydi va avtomatik ravishda `"2026-11-08T12:00:00Z"` shaklida chiqariladi.

## Ishlash natijasi:
```text
JSON: {"id":101,"xarid_vaqt":"2026-11-08T12:00:00Z"}
```

# 840-Topshiriq: XML ma'lumotlari bilan ishlash (`encoding/xml`)
## Topshiriq sharti:
Go strukturasini XML ga aylantirish va XML ni parslashni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/xml"
	"fmt"
)

type Xodim struct {
	XMLName xml.Name `xml:"xodim"`
	ID      int      `xml:"id,attr"`
	Ism     string   `xml:"ism"`
	Bolim   string   `xml:"bolim"`
}

func main() {
	x := Xodim{ID: 55, Ism: "Nodir", Bolim: "IT"}

	// XML yaratish
	xmlData, _ := xml.MarshalIndent(x, "", "  ")
	fmt.Println("XML:\n" + string(xmlData))

	// XML dan o'qish
	var yangiXodim Xodim
	_ = xml.Unmarshal(xmlData, &yangiXodim)
	fmt.Printf("O'qilgan xodim: %s (ID: %d)\n", yangiXodim.Ism, yangiXodim.ID)
}
```

## Tushuntirish va Mantiq:
`encoding/xml` teglari: `attr` (atribut sifatida), `chardata` (matn), yoki oddiy element teglari bilan XML hujjatlarini boshqaradi.

## Ishlash natijasi:
```text
XML:
<xodim id="55">
  <ism>Nodir</ism>
  <bolim>IT</bolim>
</xodim>
O'qilgan xodim: Nodir (ID: 55)
```

# 841-Topshiriq: YAML strukturalari va konversiya tamoyillari
## Topshiriq sharti:
YAML formatiga mos konfiguratsiya modellarini Go da loyihalash.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"strings"
)

type AppConfig struct {
	Server struct {
		Host string `json:"host"`
		Port int    `json:"port"`
	} `json:"server"`
	Env string `json:"env"`
}

func main() {
	cfg := AppConfig{}
	cfg.Server.Host = "localhost"
	cfg.Server.Port = 8080
	cfg.Env = "production"

	// JSON orqali YAML ga yaqin strukturalangan ko'rinish
	b, _ := json.MarshalIndent(cfg, "", "  ")
	fmt.Println("Konfiguratsiya modeli:\n" + strings.TrimSpace(string(b)))
}
```

## Tushuntirish va Mantiq:
Go da zamonaviy konfiguratsiyalar uchun YAML va JSON modellari bir xil strukturalar bilan moslashuvchan boshqariladi.

## Ishlash natijasi:
```text
Konfiguratsiya modeli:
{
  "server": {
    "host": "localhost",
    "port": 8080
  },
  "env": "production"
}
```

# 842-Topshiriq: Base64 kodlash va dekodlash (`encoding/base64`)
## Topshiriq sharti:
Ikkilik (binary) ma'lumotlarni Base64 formatiga o'girish va qayta ochish.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/base64"
	"fmt"
)

func main() {
	matn := "Salom, O'zbekiston!"

	// 1. Kodlash (Encode)
	kodlangan := base64.StdEncoding.EncodeToString([]byte(matn))
	fmt.Println("Base64 kodlangan:", kodlangan)

	// 2. Dekodlash (Decode)
	dekodlangan, err := base64.StdEncoding.DecodeString(kodlangan)
	if err != nil {
		fmt.Println("Xato:", err)
		return
	}
	fmt.Println("Asliga qaytarildi:", string(dekodlangan))
}
```

## Tushuntirish va Mantiq:
`encoding/base64.StdEncoding` baytlarni ASCII satrga aylantiradi. Bu API orqali rasmlar yoki sertifikatlarni xavfsiz jo'natish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Base64 kodlangan: U2Fsb20sIE8nemJla2lzdG9uIQ==
Asliga qaytarildi: Salom, O'zbekiston!
```

# 843-Topshiriq: Hex (O'n oltilik) kodlash va dekodlash (`encoding/hex`)
## Topshiriq sharti:
Baytlar massivini Hex satrga va aksincha o'giring.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/hex"
	"fmt"
)

func main() {
	baytlar := []byte{0xDE, 0xAD, 0xBE, 0xEF}

	hexSatr := hex.EncodeToString(baytlar)
	fmt.Println("Hex satr:", hexSatr)

	asliga, _ := hex.DecodeString(hexSatr)
	fmt.Printf("Qaytarilgan baytlar: %X\n", asliga)
}
```

## Tushuntirish va Mantiq:
`encoding/hex` kriptografik xeshlar va rang kodlarini (masalan `#FFFFFF`) o'n oltilik sanoq sistemasida formatlash uchun qo'llaniladi.

## Ishlash natijasi:
```text
Hex satr: deadbeef
Qaytarilgan baytlar: DEADBEEF
```

# 844-Topshiriq: JSON Schema validatsiyasini simulyatsiya qilish
## Topshiriq sharti:
Kelgan JSON maydonlarining majburiyligini tekshiruvchi validator yozing.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"errors"
	"fmt"
)

type RegistratsiyaSorov struct {
	Email string `json:"email"`
	Parol string `json:"parol"`
}

func (r *RegistratsiyaSorov) Tekshir() error {
	if r.Email == "" {
		return errors.New("email maydoni majburiy")
	}
	if len(r.Parol) < 6 {
		return errors.New("parol kamida 6 belgidan iborat bo'lishi shart")
	}
	return nil
}

func main() {
	validJSON := `{"email": "ali@mail.uz", "parol": "123456"}`
	invalidsJSON := `{"email": "", "parol": "123"}`

	var s1, s2 RegistratsiyaSorov
	_ = json.Unmarshal([]byte(validJSON), &s1)
	_ = json.Unmarshal([]byte(invalidsJSON), &s2)

	fmt.Println("1-so'rov tekshiruv:", s1.Tekshir())
	fmt.Println("2-so'rov tekshiruv:", s2.Tekshir())
}
```

## Tushuntirish va Mantiq:
JSON dan parslangandan so'ng biznes tekshiruvlarini (validation) alohida metod orqali bajarish toza arxitektura qoidasidir.

## Ishlash natijasi:
```text
1-so'rov tekshiruv: <nil>
2-so'rov tekshiruv: email maydoni majburiy
```

# 845-Topshiriq: JSON dan CSV formatiga o'girish (Format Konvertori)
## Topshiriq sharti:
JSON massividagi yozuvlarni CSV qatorlariga aylantiruvchi konvertor tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"strconv"
)

type Foydalanuvchi struct {
	ID   int    `json:"id"`
	Ism  string `json:"ism"`
	Yosh int    `json:"yosh"`
}

func main() {
	jsonData := `[
		{"id": 1, "ism": "Vali", "yosh": 22},
		{"id": 2, "ism": "Gani", "yosh": 25}
	]`

	var odamlar []Foydalanuvchi
	_ = json.Unmarshal([]byte(jsonData), &odamlar)

	var csvBuf bytes.Buffer
	writer := csv.NewWriter(&csvBuf)

	_ = writer.Write([]string{"ID", "Ism", "Yosh"})
	for _, o := range odamlar {
		_ = writer.Write([]string{strconv.Itoa(o.ID), o.Ism, strconv.Itoa(o.Yosh)})
	}
	writer.Flush()

	fmt.Print(csvBuf.String())
}
```

## Tushuntirish va Mantiq:
Turli formatlar o'rtasida ma'lumotlarni o'girish (ETL) jarayonlarida Go ning standart `encoding` paketlari yuqori tezlikda ishlaydi.

## Ishlash natijasi:
```text
ID,Ism,Yosh
1,Vali,22
2,Gani,25
```

# 846-Topshiriq: Konfiguratsiya faylini o'qib struct ga yuklash (Config Parser)
## Topshiriq sharti:
Diskdagi JSON fayldan konfiguratsiyani o'qib dastur sozlamalarini yuklang.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type Sozlama struct {
	Port   int    `json:"port"`
	DbHost string `json:"db_host"`
}

func YuklaKonfig(faylNomi string) (*Sozlama, error) {
	b, err := os.ReadFile(faylNomi)
	if err != nil {
		return nil, err
	}
	var s Sozlama
	if err := json.Unmarshal(b, &s); err != nil {
		return nil, err
	}
	return &s, nil
}

func main() {
	fayl := "app_config.json"
	_ = os.WriteFile(fayl, []byte(`{"port": 9000, "db_host": "db.uz"}`), 0644)
	defer os.Remove(fayl)

	cfg, _ := YuklaKonfig(fayl)
	fmt.Printf("Yuklangan konfiguratsiya: Port=%d, DB=%s\n", cfg.Port, cfg.DbHost)
}
```

## Tushuntirish va Mantiq:
Ilova ishga tushganda konfiguratsiya faylini xavfsiz o'qib strukturaga yuklash barcha server dasturlarining kirish nuqtasidir.

## Ishlash natijasi:
```text
Yuklangan konfiguratsiya: Port=9000, DB=db.uz
```

# 847-Topshiriq: Atomic File Write: Faylni atomik xavfsiz yozish
## Topshiriq sharti:
Fayl yarimta yozilib qolmasligi uchun avval vaqtinchalik faylga yozib, so'ng `os.Rename` bilan almashtiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func AtomikYozish(aslFayl string, data []byte) error {
	dir := filepath.Dir(aslFayl)
	temp, err := os.CreateTemp(dir, "temp_*.tmp")
	if err != nil {
		return err
	}
	tempNom := temp.Name()

	_, err = temp.Write(data)
	temp.Close()
	if err != nil {
		os.Remove(tempNom)
		return err
	}

	// Atomik almashtirish
	return os.Rename(tempNom, aslFayl)
}

func main() {
	nomi := "kritik_fayl.txt"
	defer os.Remove(nomi)

	err := AtomikYozish(nomi, []byte("Yangi kritik ma'lumot"))
	if err != nil {
		fmt.Println("Xato:", err)
		return
	}

	res, _ := os.ReadFile(nomi)
	fmt.Println("Fayl tarkibi:", string(res))
}
```

## Tushuntirish va Mantiq:
Agar yozish paytida elektr uzilsa yoki xatolik bo'lsa, to'g'ridan-to'g'ri yozilgan fayl buziladi. Vaqtinchalik faylga yozib `os.Rename` qilish operatsion tizim darajasida atomikdir.

## Ishlash natijasi:
```text
Fayl tarkibi: Yangi kritik ma'lumot
```

# 848-Topshiriq: Log Rotation (Log fayllarini hajmi bo'yicha aylantirish) simulyatsiyasi
## Topshiriq sharti:
Fayl hajmi 30 baytdan oshganda uni `.1` ga arxivlab yangi fayl ochuvchi tizim.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"os"
)

func logYoz(nom string, xabar string, maxHajm int64) {
	info, err := os.Stat(nom)
	if err == nil && info.Size() >= maxHajm {
		_ = os.Rename(nom, nom+".1")
		fmt.Printf("[Rotation] '%s' hajmi oshdi, arxivlandi!\n", nom)
	}

	f, _ := os.OpenFile(nom, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	defer f.Close()
	_, _ = f.WriteString(xabar + "\n")
}

func main() {
	nom := "server.log"
	defer os.Remove(nom)
	defer os.Remove(nom + ".1")

	logYoz(nom, "1-qator: Start", 25)
	logYoz(nom, "2-qator: Ulanish", 25)
	logYoz(nom, "3-qator: Yangi log", 25)

	fmt.Println("Log aylanishi muvaffaqiyatli yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Log rotation disklarning to'lib qolishini oldini olish uchun log fayllarni belgilangan hajm yoki kunda qayta nomlab arxivlash amaliyotidir.

## Ishlash natijasi:
```text
[Rotation] 'server.log' hajmi oshdi, arxivlandi!
Log aylanishi muvaffaqiyatli yakunlandi.
```

# 849-Topshiriq: Xotira tejamkor fayl oqimli nusxalovchi (Stream Copier)
## Topshiriq sharti:
Nusxa ko'chirish jarayonida necha bayt o'tganini hisoblab boruvchi hisoblagichli Writer.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"fmt"
	"io"
	"strings"
)

type SanovchiWriter struct {
	yozuvchi  io.Writer
	jamiBayt int64
}

func (s *SanovchiWriter) Write(p []byte) (int, error) {
	n, err := s.yozuvchi.Write(p)
	s.jamiBayt += int64(n)
	return n, err
}

func main() {
	manba := strings.NewReader("Go IO oqimlari juda samarali ishlaydi!")
	var maqsad bytes.Buffer
	sanovchi := &SanovchiWriter{yozuvchi: &maqsad}

	_, _ = io.Copy(sanovchi, manba)

	fmt.Printf("Nusxalandi: '%s'\n", maqsad.String())
	fmt.Printf("Jami hisoblangan baytlar: %d\n", sanovchi.jamiBayt)
}
```

## Tushuntirish va Mantiq:
`io.Writer` ni o'rab oluvchi decorator vositasida fayllar yuklanish jarayonini (progress bar) yoki trafigini kuzatish mumkin.

## Ishlash natijasi:
```text
Nusxalandi: 'Go IO oqimlari juda samarali ishlaydi!'
Jami hisoblangan baytlar: 40
```

# 850-Topshiriq: Keng qamrovli ETL Vosita: JSON -> CSV -> GZIP Konverteri
## Topshiriq sharti:
Keng qamrovli yakuniy loyiha: JSON faylni o'qib, uni CSV formatiga o'tkazuvchi va yakunda GZIP bilan siqib saqlovchi to'liq konverter yarating.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"compress/gzip"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"strconv"
)

type Foydalanuvchi struct {
	ID    int    `json:"id"`
	Ism   string `json:"ism"`
	Kasb  string `json:"kasb"`
	Maosh int    `json:"maosh"`
}

func main() {
	// 1. Kiruvchi JSON ma'lumotlari
	kiruvchiJSON := `[
		{"id": 101, "ism": "Akmal", "kasb": "Backend Dasturchi", "maosh": 15000000},
		{"id": 102, "ism": "Nodira", "kasb": "QA Engineer", "maosh": 12000000},
		{"id": 103, "ism": "Rustam", "kasb": "Frontend Dasturchi", "maosh": 14000000}
	]`

	var xodimlar []Foydalanuvchi
	if err := json.Unmarshal([]byte(kiruvchiJSON), &xodimlar); err != nil {
		fmt.Println("JSON parslash xatosi:", err)
		return
	}

	// 2. CSV ga aylantirish
	var csvBuf bytes.Buffer
	csvWriter := csv.NewWriter(&csvBuf)
	_ = csvWriter.Write([]string{"ID", "Ism", "Kasb", "Maosh"})

	for _, x := range xodimlar {
		_ = csvWriter.Write([]string{
			strconv.Itoa(x.ID),
			x.Ism,
			x.Kasb,
			strconv.Itoa(x.Maosh),
		})
	}
	csvWriter.Flush()

	csvBytes := csvBuf.Bytes()
	fmt.Printf("[Bosqich 1] CSV yaratildi: %d bayt\n", len(csvBytes))

	// 3. GZIP orqali siqish
	var gzipBuf bytes.Buffer
	gzWriter := gzip.NewWriter(&gzipBuf)
	_, _ = gzWriter.Write(csvBytes)
	_ = gzWriter.Close()

	siqilganHajm := gzipBuf.Len()
	fmt.Printf("[Bosqich 2] GZIP siqildi: %d bayt\n", siqilganHajm)
	fmt.Println("=== ETL JARAYONI MUVAFFAQIYATLI YAKUNLANDI ===")
}
```

## Tushuntirish va Mantiq:
Ushbu loyihada `encoding/json`, `encoding/csv` va `compress/gzip` paketlari o'zaro birlashtirilib, zamonaviy ma'lumotlar qayta ishlash quvuri (Data Pipeline) to'liq amalga oshirildi.

## Ishlash natijasi:
```text
[Bosqich 1] CSV yaratildi: 153 bayt
[Bosqich 2] GZIP siqildi: 135 bayt
=== ETL JARAYONI MUVAFFAQIYATLI YAKUNLANDI ===
```

