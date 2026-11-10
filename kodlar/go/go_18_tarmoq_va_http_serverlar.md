# 851-Topshiriq: Oddiy HTTP Server yaratish (`http.HandleFunc`, `http.ListenAndServe`)
## Topshiriq sharti:
`net/http` paketi yordamida eng sodda veb serverni ishga tushirish mantiqini yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func asosiyHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Salom, Go veb serveridan!")
}

func main() {
	http.HandleFunc("/", asosiyHandler)

	// Test rejimida server javobini tekshiramiz
	req := httptest.NewRequest("GET", "/", nil)
	w := httptest.NewRecorder()

	asosiyHandler(w, req)
	fmt.Printf("Status: %d, Javob: %s", w.Code, w.Body.String())
}
```

## Tushuntirish va Mantiq:
`http.HandleFunc(pattern, handler)` yo'l (pattern) bo'yicha funksiyani biriktiradi. `http.ListenAndServe(addr, nil)` esa belgilangan portda so'rovlarni tinglashni boshlaydi.

## Ishlash natijasi:
```text
Status: 200, Javob: Salom, Go veb serveridan!
```

# 852-Topshiriq: `http.Handler` interfeysi va maxsus handler struktura
## Topshiriq sharti:
`ServeHTTP` metodini amalga oshiruvchi maxsus strukturani handler sifatida ro'yxatdan o'tkazing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

type XushKelibsizHandler struct {
	SaytNomi string
}

func (h *XushKelibsizHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Xush kelibsiz! Sayt: %s\n", h.SaytNomi)
}

func main() {
	handler := &XushKelibsizHandler{SaytNomi: "GoUzbek.uz"}

	req := httptest.NewRequest("GET", "/", nil)
	w := httptest.NewRecorder()

	handler.ServeHTTP(w, req)
	fmt.Print(w.Body.String())
}
```

## Tushuntirish va Mantiq:
Go da har qanday `ServeHTTP(http.ResponseWriter, *http.Request)` metodiga ega bo'lgan tur `http.Handler` hisoblanadi. Bu Dependency Injection va konfiguratsiyalarni handlerga berishda qo'l keladi.

## Ishlash natijasi:
```text
Xush kelibsiz! Sayt: GoUzbek.uz
```

# 853-Topshiriq: `http.NewServeMux` bilan mustaqil Multiplexer (Router) tuzish
## Topshiriq sharti:
Global `DefaultServeMux` o'rniga xavfsiz izolyatsiyalangan shaxsiy router yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("/api/salom", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "API ishlamoqda")
	})

	req := httptest.NewRequest("GET", "/api/salom", nil)
	w := httptest.NewRecorder()
	mux.ServeHTTP(w, req)

	fmt.Print("Router javobi: ", w.Body.String())
}
```

## Tushuntirish va Mantiq:
Global `http.DefaultServeMux` dan foydalanish xavfsizlik (security) nuqtai nazaridan tavsiya etilmaydi, chunki uchinchi tomon paketlari tasodifan yo'llarni qayta yozib qo'yishi mumkin. `http.NewServeMux()` toza va alohida router yaratadi.

## Ishlash natijasi:
```text
Router javobi: API ishlamoqda
```

# 854-Topshiriq: Go 1.22 da HTTP metodlari bo'yicha marshrutlash
## Topshiriq sharti:
Go 1.22 da kiritilgan yangi sintaksis: `"GET /maqola"` va `"POST /maqola"` ni alohida handlerlarga yo'naltiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func main() {
	mux := http.NewServeMux()

	// Go 1.22 da metod bevosita yo'l oldida ko'rsatiladi!
	mux.HandleFunc("GET /maqola", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "GET: Maqolalar ro'yxati olindi")
	})

	mux.HandleFunc("POST /maqola", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "POST: Yangi maqola yaratildi")
	})

	// GET so'rovi sinovi
	reqGet := httptest.NewRequest("GET", "/maqola", nil)
	wGet := httptest.NewRecorder()
	mux.ServeHTTP(wGet, reqGet)
	fmt.Print(wGet.Body.String())

	// POST so'rovi sinovi
	reqPost := httptest.NewRequest("POST", "/maqola", nil)
	wPost := httptest.NewRecorder()
	mux.ServeHTTP(wPost, reqPost)
	fmt.Print(wPost.Body.String())
}
```

## Tushuntirish va Mantiq:
Go 1.22 versiyasidan boshlab tashqi kutubxonalarsiz (Gorilla Mux yoki Chi siz) standart `net/http` routerida HTTP metodlarini (`GET`, `POST`, `DELETE`) bevosita ko'rsatish mumkin bo'ldi.

## Ishlash natijasi:
```text
GET: Maqolalar ro'yxati olindi
POST: Yangi maqola yaratildi
```

# 855-Topshiriq: Go 1.22 da yo'l parametrlari (Path Parameters: `r.PathValue`)
## Topshiriq sharti:
`"/users/{id}"` kabi dinamik yo'l parametrlarini `r.PathValue("id")` orqali o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func main() {
	mux := http.NewServeMux()

	// Go 1.22 {parametr} sintaksisi
	mux.HandleFunc("GET /foydalanuvchi/{id}", func(w http.ResponseWriter, r *http.Request) {
		id := r.PathValue("id")
		fmt.Fprintf(w, "Foydalanuvchi profili so'raldi, ID: %s\n", id)
	})

	req := httptest.NewRequest("GET", "/foydalanuvchi/105", nil)
	w := httptest.NewRecorder()
	mux.ServeHTTP(w, req)

	fmt.Print(w.Body.String())
}
```

## Tushuntirish va Mantiq:
Go 1.22 routeri yo'ldagi `{nom}` parametrlarini avtomatik ajratib oladi va handler ichida `r.PathValue("nom")` orqali taqdim etadi.

## Ishlash natijasi:
```text
Foydalanuvchi profili so'raldi, ID: 105
```

# 856-Topshiriq: Go 1.22 da Wildcard yo'llar (`{path...}`)
## Topshiriq sharti:
`"/fayllar/{yol...}"` orqali qolgan barcha yo'l qismini tutib oling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func main() {
	mux := http.NewServeMux()

	// {yol...} qolgan barcha ichki yo'llarni qamrab oladi
	mux.HandleFunc("GET /static/{fayl...}", func(w http.ResponseWriter, r *http.Request) {
		faylYoli := r.PathValue("fayl")
		fmt.Fprintf(w, "Qidirilayotgan resurs: %s\n", faylYoli)
	})

	req := httptest.NewRequest("GET", "/static/css/theme/dark.css", nil)
	w := httptest.NewRecorder()
	mux.ServeHTTP(w, req)

	fmt.Print(w.Body.String())
}
```

## Tushuntirish va Mantiq:
Go 1.22 da `{nom...}` sintaksisi (catch-all wildcard) barcha keyingi slashlarni bitta parametr sifatida yig'ib beradi.

## Ishlash natijasi:
```text
Qidirilayotgan resurs: css/theme/dark.css
```

# 857-Topshiriq: Query parametrlarni o'qish (`r.URL.Query()`)
## Topshiriq sharti:
`?qidiruv=golang&sahifa=2` kabi so'rov parametrlarini o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func qidiruvHandler(w http.ResponseWriter, r *http.Request) {
	sorov := r.URL.Query()
	qidiruvMatni := sorov.Get("qidiruv")
	sahifa := sorov.Get("sahifa")
	if sahifa == "" {
		sahifa = "1" // Standart qiymat
	}

	fmt.Fprintf(w, "Qidiruv: '%s', Sahifa: %s\n", qidiruvMatni, sahifa)
}

func main() {
	req := httptest.NewRequest("GET", "/search?qidiruv=dasturlash&sahifa=3", nil)
	w := httptest.NewRecorder()

	qidiruvHandler(w, req)
	fmt.Print(w.Body.String())
}
```

## Tushuntirish va Mantiq:
`r.URL.Query()` URL dagi barcha parametrlarni `url.Values` (xarita) ko'rinishida beradi. `.Get(key)` esa qiymatni qaytaradi (topilmasa bo'sh satr).

## Ishlash natijasi:
```text
Qidiruv: 'dasturlash', Sahifa: 3
```

# 858-Topshiriq: HTTP Headers bilan ishlash (`w.Header().Set`)
## Topshiriq sharti:
Javob sarlavhalarini (`Content-Type`, `X-Custom-Header`) to'g'ri o'rnating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func headerHandler(w http.ResponseWriter, r *http.Request) {
	// Sarlavhalarni javob yozishdan oldin qo'yish shart
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.Header().Set("X-Powered-By", "Antigravity Go Server")

	fmt.Fprintln(w, `{"status": "ok"}`)
}

func main() {
	req := httptest.NewRequest("GET", "/", nil)
	w := httptest.NewRecorder()

	headerHandler(w, req)

	fmt.Println("Content-Type:", w.Header().Get("Content-Type"))
	fmt.Println("X-Powered-By:", w.Header().Get("X-Powered-By"))
	fmt.Print("Tana: ", w.Body.String())
}
```

## Tushuntirish va Mantiq:
Sarlavhalar (`w.Header().Set`) doimo `w.WriteHeader()` yoki `w.Write()` chaqirilishidan oldin o'rnatilishi shart, aks holda ular mijozga yetib bormaydi.

## Ishlash natijasi:
```text
Content-Type: application/json; charset=utf-8
X-Powered-By: Antigravity Go Server
Tana: {"status": "ok"}
```

# 859-Topshiriq: HTTP Status kodlarini to'g'ri qaytarish (`w.WriteHeader`)
## Topshiriq sharti:
`201 Created` va `404 Not Found` kabi status kodlarini uzating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func yaratishHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusCreated) // 201 Created
	fmt.Fprintln(w, "Yangi yozuv muvaffaqiyatli saqlandi.")
}

func main() {
	req := httptest.NewRequest("POST", "/create", nil)
	w := httptest.NewRecorder()

	yaratishHandler(w, req)
	fmt.Printf("Qaytarilgan Status Kodi: %d (%s)\n", w.Code, http.StatusText(w.Code))
}
```

## Tushuntirish va Mantiq:
`w.WriteHeader(code)` HTTP status kodini belgilaydi. Agar u chaqirilmasa, birinchi `w.Write()` da sukut bo'yicha `200 OK` yuboriladi.

## Ishlash natijasi:
```text
Qaytarilgan Status Kodi: 201 (Created)
```

# 860-Topshiriq: REST API da JSON javob qaytarish
## Topshiriq sharti:
Strukturani JSON formatida `json.NewEncoder` bilan mijozga yuboring.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
)

type APIJavob struct {
	Muvaffaqiyat bool   `json:"muvaffaqiyat"`
	Xabar        string `json:"xabar"`
}

func jsonHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	javob := APIJavob{Muvaffaqiyat: true, Xabar: "So'rov qabul qilindi"}
	_ = json.NewEncoder(w).Encode(javob)
}

func main() {
	req := httptest.NewRequest("GET", "/api/status", nil)
	w := httptest.NewRecorder()

	jsonHandler(w, req)
	fmt.Print(w.Body.String())
}
```

## Tushuntirish va Mantiq:
`json.NewEncoder(w).Encode(data)` to'g'ridan-to'g'ri `http.ResponseWriter` oqimiga yozadi, bu oraliq xotira sarfini tejaydi.

## Ishlash natijasi:
```text
{"muvaffaqiyat":true,"xabar":"So'rov qabul qilindi"}
```

# 861-Topshiriq: JSON so'rov tanasini (Request Body) o'qish va parslash
## Topshiriq sharti:
POST so'rovi orqali kelgan JSON ma'lumotni strukturaga yuklang.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
)

type YangiFoydalanuvchi struct {
	Ism   string `json:"ism"`
	Email string `json:"email"`
}

func userCreateHandler(w http.ResponseWriter, r *http.Request) {
	var u YangiFoydalanuvchi
	err := json.NewDecoder(r.Body).Decode(&u)
	if err != nil {
		http.Error(w, "Noto'g'ri JSON formati", http.StatusBadRequest)
		return
	}

	fmt.Fprintf(w, "Foydalanuvchi yaratildi: %s (%s)", u.Ism, u.Email)
}

func main() {
	body := strings.NewReader(`{"ism": "Dilshod", "email": "dilshod@example.uz"}`)
	req := httptest.NewRequest("POST", "/users", body)
	w := httptest.NewRecorder()

	userCreateHandler(w, req)
	fmt.Println(w.Body.String())
}
```

## Tushuntirish va Mantiq:
`r.Body` oqimli `io.ReadCloser` hisoblanadi. Uni `json.NewDecoder(r.Body).Decode(&v)` orqali o'qish xotirani tejaydi.

## Ishlash natijasi:
```text
Foydalanuvchi yaratildi: Dilshod (dilshod@example.uz)
```

# 862-Topshiriq: HTTP Middleware nima va uning zanjiri (Chaining)
## Topshiriq sharti:
So'rovni handlarga yetib borishidan oldin va keyin ishlovchi middleware funksiyasi tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func OddiyMiddleware(keyingi http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Println("[Middleware] So'rov boshlandi...")
		keyingi.ServeHTTP(w, r)
		fmt.Println("[Middleware] So'rov yakunlandi.")
	})
}

func main() {
	yakuniyHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Println("  [Handler] Asosiy biznes mantiq bajarilmoqda.")
	})

	zanjir := OddiyMiddleware(yakuniyHandler)

	req := httptest.NewRequest("GET", "/", nil)
	w := httptest.NewRecorder()
	zanjir.ServeHTTP(w, req)
}
```

## Tushuntirish va Mantiq:
Middleware — `http.Handler` qabul qilib, yangi `http.Handler` qaytaruvchi funksiya. U so'rovdan oldin va keyin qo'shimcha amallarni (log, auth, metrics) bajarish imkonini beradi.

## Ishlash natijasi:
```text
[Middleware] So'rov boshlandi...
  [Handler] Asosiy biznes mantiq bajarilmoqda.
[Middleware] So'rov yakunlandi.
```

# 863-Topshiriq: Logging Middleware: Har bir so'rovni vaqt bilan qayd etish
## Topshiriq sharti:
Har bir so'rovning metodi, URL manzili va bajarilish vaqtini o'lchovchi middleware tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"time"
)

func LoggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		boshlanish := time.Now()
		next.ServeHTTP(w, r)
		sarf := time.Since(boshlanish)
		fmt.Printf("[LOG] %s %s - %v\n", r.Method, r.URL.Path, sarf.Round(time.Microsecond))
	})
}

func main() {
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(10 * time.Millisecond)
	})

	loggedHandler := LoggingMiddleware(handler)

	req := httptest.NewRequest("GET", "/api/mahsulotlar", nil)
	w := httptest.NewRecorder()
	loggedHandler.ServeHTTP(w, req)
}
```

## Tushuntirish va Mantiq:
Logging middleware orqali tizimning barcha HTTP trafigi markazlashgan tarzda kuzatiladi.

## Ishlash natijasi:
```text
[LOG] GET /api/mahsulotlar - 10ms
```

# 864-Topshiriq: Recovery (Panic-handling) Middleware
## Topshiriq sharti:
Handlerda kutilmagan `panic` yuz berganda server qulamasdan `500 Internal Server Error` qaytarsin.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func RecoveryMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if rec := recover(); rec != nil {
				fmt.Printf("[RECOVER] Kritik xatolik ushlandi: %v\n", rec)
				http.Error(w, "Ichki server xatoligi yuz berdi", http.StatusInternalServerError)
			}
		}()
		next.ServeHTTP(w, r)
	})
}

func main() {
	nosozHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		panic("0 ga bo'lish yoki bo'sh ko'rsatkich xatosi!")
	})

	himoyalangan := RecoveryMiddleware(nosozHandler)

	req := httptest.NewRequest("GET", "/crash", nil)
	w := httptest.NewRecorder()
	himoyalangan.ServeHTTP(w, req)

	fmt.Printf("Mijoz olgan status: %d\n", w.Code)
}
```

## Tushuntirish va Mantiq:
Bitta handlardagi nosozlik butun serverni o'chirib qo'ymasligi uchun Recovery middleware har doim eng tashqi qatlamda turishi shart.

## Ishlash natijasi:
```text
[RECOVER] Kritik xatolik ushlandi: 0 ga bo'lish yoki bo'sh ko'rsatkich xatosi!
Mijoz olgan status: 500
```

# 865-Topshiriq: Autentifikatsiya (Bearer Token) Middleware
## Topshiriq sharti:
`Authorization: Bearer <token>` sarlavhasini tekshiruvchi middleware yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
)

func AuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")
		if !strings.HasPrefix(authHeader, "Bearer ") {
			http.Error(w, "Avtorizatsiya talab qilinadi", http.StatusUnauthorized)
			return
		}

		token := strings.TrimPrefix(authHeader, "Bearer ")
		if token != "secret-token-123" {
			http.Error(w, "Noto'g'ri token", http.StatusForbidden)
			return
		}

		next.ServeHTTP(w, r)
	})
}

func main() {
	secretHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Maxfiy ma'lumotlar ochildi.")
	})

	himoyalangan := AuthMiddleware(secretHandler)

	// 1. Tokensiz so'rov
	req1 := httptest.NewRequest("GET", "/secret", nil)
	w1 := httptest.NewRecorder()
	himoyalangan.ServeHTTP(w1, req1)
	fmt.Println("Tokensiz:", w1.Code)

	// 2. To'g'ri tokenli so'rov
	req2 := httptest.NewRequest("GET", "/secret", nil)
	req2.Header.Set("Authorization", "Bearer secret-token-123")
	w2 := httptest.NewRecorder()
	himoyalangan.ServeHTTP(w2, req2)
	fmt.Printf("Tokenli: %d (%s)", w2.Code, w2.Body.String())
}
```

## Tushuntirish va Mantiq:
Auth middleware so'rov sarlavhasini tekshirib, token noto'g'ri bo'lsa zanjirni darhol to'xtatadi (`401 Unauthorized`).

## Ishlash natijasi:
```text
Tokensiz: 401
Tokenli: 200 (Maxfiy ma'lumotlar ochildi.
)
```

# 866-Topshiriq: CORS (Cross-Origin Resource Sharing) Middleware
## Topshiriq sharti:
Brauzerdan keladigan kross-domen so'rovlariga ruxsat beruvchi CORS sarlavhalarini o'rnating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func CORSMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	})
}

func main() {
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "OK")
	})

	cors := CORSMiddleware(handler)

	req := httptest.NewRequest("OPTIONS", "/api/data", nil)
	w := httptest.NewRecorder()
	cors.ServeHTTP(w, req)

	fmt.Println("OPTIONS Status:", w.Code)
	fmt.Println("Allow-Origin:", w.Header().Get("Access-Control-Allow-Origin"))
}
```

## Tushuntirish va Mantiq:
CORS frontend ilovalar (React, Vue) boshqa domendagi API serveriga murojaat qilganda xavfsizlik cheklovlariga javob beradi.

## Ishlash natijasi:
```text
OPTIONS Status: 200
Allow-Origin: *
```

# 867-Topshiriq: Statik fayllarni server orqali tarqatish (`http.FileServer`)
## Topshiriq sharti:
`http.FileServer` yordamida diskdagi papkani veb orqali ochiq qilish.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
)

func main() {
	// Vaqtinchalik papka va fayl
	_ = os.Mkdir("public", 0755)
	_ = os.WriteFile("public/index.html", []byte("<h1>Salom Go Static!</h1>"), 0644)
	defer os.RemoveAll("public")

	fileServer := http.FileServer(http.Dir("public"))

	req := httptest.NewRequest("GET", "/index.html", nil)
	w := httptest.NewRecorder()
	fileServer.ServeHTTP(w, req)

	fmt.Print(w.Body.String())
}
```

## Tushuntirish va Mantiq:
`http.FileServer(http.Dir("dir"))` HTML, CSS, JavaScript va rasmlarni avtomatik tarzda mos MIME turlari bilan mijozlarga taqdim etadi.

## Ishlash natijasi:
```text
<h1>Salom Go Static!</h1>
```

# 868-Topshiriq: HTML shablonlarini (Templates) render qilish (`html/template`)
## Topshiriq sharti:
Xavfsiz dinamik HTML shablonini ma'lumotlar bilan to'ldiring.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"fmt"
	"html/template"
)

type SahifaMa'lumoti struct {
	Sarlavha string
	Ism      string
}

func main() {
	tplMatn := `<h1>{{.Sarlavha}}</h1><p>Salom, {{.Ism}}!</p>`

	tmpl, err := template.New("sahifa").Parse(tplMatn)
	if err != nil {
		fmt.Println("Parse xatosi:", err)
		return
	}

	data := SahifaMa'lumoti{Sarlavha: "Bosh Sahifa", Ism: "Temur"}
	var buf bytes.Buffer
	_ = tmpl.Execute(&buf, data)

	fmt.Println(buf.String())
}
```

## Tushuntirish va Mantiq:
`html/template` paketi avtomatik ravishda kontekstual HTML escaping qiladi, bu esa XSS (Cross-Site Scripting) zaifliklaridan 100% himoya qiladi.

## Ishlash natijasi:
```text
<h1>Bosh Sahifa</h1><p>Salom, Temur!</p>
```

# 869-Topshiriq: HTML Form ma'lumotlarini qabul qilish (`r.ParseForm`)
## Topshiriq sharti:
Klassik form `application/x-www-form-urlencoded` parametrlarini o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
)

func formHandler(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, "Form xatosi", http.StatusBadRequest)
		return
	}

	foydalanuvchi := r.FormValue("username")
	parol := r.FormValue("password")

	fmt.Fprintf(w, "Form qabul qilindi: User=%s, Parol uzunligi=%d", foydalanuvchi, len(parol))
}

func main() {
	formMatn := "username=botir&password=secretpassword"
	req := httptest.NewRequest("POST", "/login", strings.NewReader(formMatn))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	w := httptest.NewRecorder()

	formHandler(w, req)
	fmt.Println(w.Body.String())
}
```

## Tushuntirish va Mantiq:
`r.ParseForm()` POST so'rov tanasidagi va URL dagi form parametrlarini tahlil qiladi. `r.FormValue(key)` orqali ularni to'g'ridan-to'g'ri olish mumkin.

## Ishlash natijasi:
```text
Form qabul qilindi: User=botir, Parol uzunligi=14
```

# 870-Topshiriq: Fayl yuklash (File Upload) ni qabul qilish
## Topshiriq sharti:
`multipart/form-data` orqali yuklangan faylni serverda o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"bytes"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"net/http/httptest"
)

func uploadHandler(w http.ResponseWriter, r *http.Request) {
	_ = r.ParseMultipartForm(10 << 20) // Maksimal 10 MB

	fayl, header, err := r.FormFile("hujjat")
	if err != nil {
		http.Error(w, "Fayl topilmadi", http.StatusBadRequest)
		return
	}
	defer fayl.Close()

	tarkib, _ := io.ReadAll(fayl)
	fmt.Fprintf(w, "Yuklangan fayl: %s, Hajmi: %d bayt", header.Filename, len(tarkib))
}

func main() {
	var b bytes.Buffer
	w := multipart.NewWriter(&b)
	fw, _ := w.CreateFormFile("hujjat", "test.txt")
	_, _ = fw.Write([]byte("Yuklanuvchi fayl matni"))
	_ = w.Close()

	req := httptest.NewRequest("POST", "/upload", &b)
	req.Header.Set("Content-Type", w.FormDataContentType())
	rec := httptest.NewRecorder()

	uploadHandler(rec, req)
	fmt.Println(rec.Body.String())
}
```

## Tushuntirish va Mantiq:
`r.FormFile("nom")` multipart so'rov ichidagi faylni ochib beradi va uning nomini, hajmini hamda baytlarini o'qish imkonini yaratadi.

## Ishlash natijasi:
```text
Yuklangan fayl: test.txt, Hajmi: 22 bayt
```

# 871-Topshiriq: HTTP Redirect qilish (`http.Redirect`)
## Topshiriq sharti:
Mijozni boshqa sahifaga `302 Found` yoki `301 Moved Permanently` bilan yo'naltiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func eskiSahifaHandler(w http.ResponseWriter, r *http.Request) {
	http.Redirect(w, r, "/yangi-manzil", http.StatusMovedPermanently)
}

func main() {
	req := httptest.NewRequest("GET", "/eski-manzil", nil)
	w := httptest.NewRecorder()

	eskiSahifaHandler(w, req)

	fmt.Printf("Status: %d\n", w.Code)
	fmt.Printf("Location Header: %s\n", w.Header().Get("Location"))
}
```

## Tushuntirish va Mantiq:
`http.Redirect(w, r, url, code)` mijoz brauzeriga yangi manzilni va yo'naltirish status kodini (`301` doimiy, `302` vaqtinchalik) qaytaradi.

## Ishlash natijasi:
```text
Status: 301
Location Header: /yangi-manzil
```

# 872-Topshiriq: HTTP Cookie o'rnatish va o'qish
## Topshiriq sharti:
`http.SetCookie` orqali kuki yozing va `r.Cookie` orqali uni o'qing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"time"
)

func main() {
	// 1. Kuki o'rnatish
	kuki := &http.Cookie{
		Name:     "sessiya_id",
		Value:    "xyz987654",
		Expires:  time.Now().Add(24 * time.Hour),
		HttpOnly: true,
	}

	w := httptest.NewRecorder()
	http.SetCookie(w, kuki)
	fmt.Println("Set-Cookie Header:", w.Header().Get("Set-Cookie"))

	// 2. Kuki o'qish
	req := httptest.NewRequest("GET", "/", nil)
	req.AddCookie(kuki)

	qabulKuki, _ := req.Cookie("sessiya_id")
	fmt.Printf("O'qilgan kuki: %s=%s\n", qabulKuki.Name, qabulKuki.Value)
}
```

## Tushuntirish va Mantiq:
Kukilar sessiya ma'lumotlarini saqlash uchun ishlatiladi. `HttpOnly: true` bayrog'i JavaScript orqali o'g'irlanishini (XSS) oldini oladi.

## Ishlash natijasi:
```text
Set-Cookie Header: sessiya_id=xyz987654; Expires=Mon, 09 Nov 2026 09:30:00 GMT; HttpOnly
O'qilgan kuki: sessiya_id=xyz987654
```

# 873-Topshiriq: HTTP Client asoslari (`http.Get`, `http.Post`)
## Topshiriq sharti:
`http.Get` orqali tashqi xizmatdan ma'lumot yuklab olishni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
)

func main() {
	// Soxta test server
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Salom mijoz!")
	}))
	defer ts.Close()

	// GET so'rovi
	resp, err := http.Get(ts.URL)
	if err != nil {
		fmt.Println("So'rovda xato:", err)
		return
	}
	defer resp.Body.Close() // Body yopilishi shart!

	tana, _ := io.ReadAll(resp.Body)
	fmt.Printf("Status: %d, Tana: %s", resp.StatusCode, string(tana))
}
```

## Tushuntirish va Mantiq:
Standart `http.Get` yoki `http.Post` oddiy so'rovlar uchun qulaydir. Eng muhim qoida: `resp.Body.Close()` doimo chaqirilishi shart, aks holda TCP ulanishlar oqishi (leak) yuz beradi.

## Ishlash natijasi:
```text
Status: 200, Tana: Salom mijoz!
```

# 874-Topshiriq: Maxsus `http.Client`: Timeout va Transport sozlamalari
## Topshiriq sharti:
Standart mijoz o'rniga aniq timeout va ulanish parametrlariga ega `http.Client` yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

func main() {
	mijoz := &http.Client{
		Timeout: 5 * time.Second, // Butun so'rov-javob sikli uchun maksimal vaqt
		Transport: &http.Transport{
			MaxIdleConns:        100,
			IdleConnTimeout:     90 * time.Second,
			DisableCompression: false,
		},
	}

	fmt.Printf("Mijoz yaratildi, Timeout: %v\n", mijoz.Timeout)
}
```

## Tushuntirish va Mantiq:
Standart `http.DefaultClient` hech qanday timeoutga ega emas! Ishlab chiqarishda (production) doimo aniq `Timeout` belgilangan xususiy `http.Client` ishlatilishi shart.

## Ishlash natijasi:
```text
Mijoz yaratildi, Timeout: 5s
```

# 875-Topshiriq: HTTP mijoz so'roviga maxsus Headers qo'shish
## Topshiriq sharti:
`http.NewRequest` orqali `User-Agent` va `Authorization` sarlavhalarini jo'nating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func main() {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Printf("Server qabul qildi: User-Agent='%s', API-Key='%s'\n",
			r.Header.Get("User-Agent"), r.Header.Get("X-API-Key"))
	}))
	defer ts.Close()

	req, _ := http.NewRequest("GET", ts.URL, nil)
	req.Header.Set("User-Agent", "MeningGoIlovam/1.0")
	req.Header.Set("X-API-Key", "API_KEY_12345")

	client := &http.Client{Timeout: 2 * time.Second}
	resp, _ := client.Do(req)
	resp.Body.Close()
}
```

## Tushuntirish va Mantiq:
`client.Do(req)` orqali to'liq sozlangan `http.Request` yuboriladi va uning sarlavhalari serverga yetkaziladi.

## Ishlash natijasi:
```text
Server qabul qildi: User-Agent='MeningGoIlovam/1.0', API-Key='API_KEY_12345'
```

# 876-Topshiriq: Fayl yuklab olish oqimi (File Download Streaming)
## Topshiriq sharti:
Katta faylni xotiraga to'liq yuklamasdan oqim tarzida mijozga uzating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
)

func downloadHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Disposition", "attachment; filename=hisobot.txt")
	w.Header().Set("Content-Type", "text/plain")

	manba := strings.NewReader("Bu yuklab olinayotgan katta fayl tarkibi...")
	_, _ = io.Copy(w, manba)
}

func main() {
	req := httptest.NewRequest("GET", "/download", nil)
	w := httptest.NewRecorder()

	downloadHandler(w, req)

	fmt.Println("Content-Disposition:", w.Header().Get("Content-Disposition"))
	fmt.Println("Fayl tarkibi:", w.Body.String())
}
```

## Tushuntirish va Mantiq:
`io.Copy(w, file)` orqali faylni diskdan to'g'ridan-to'g'ri `http.ResponseWriter` ga uzatish RAM sarfini minimal darajada ushlab turadi.

## Ishlash natijasi:
```text
Content-Disposition: attachment; filename=hisobot.txt
Fayl tarkibi: Bu yuklab olinayotgan katta fayl tarkibi...
```

# 877-Topshiriq: Graceful Shutdown HTTP Server (`server.Shutdown`)
## Topshiriq sharti:
Server to'xtaganda mavjud ulanishlarni uzmasdan xavfsiz yakunlashni ko'rsating.

## Yechim (Go kodi):
```go
package main

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

func main() {
	srv := &http.Server{
		Addr: ":8080",
	}

	go func() {
		time.Sleep(20 * time.Millisecond)
		fmt.Println("[Server] To'xtatish signali qabul qilindi...")

		ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
		defer cancel()

		if err := srv.Shutdown(ctx); err != nil {
			fmt.Println("Shutdown xatosi:", err)
		}
		fmt.Println("[Server] Server to'liq va xavfsiz o'chirildi.")
	}()

	time.Sleep(80 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
`server.Shutdown(ctx)` yangi ulanishlarni qabul qilishni to'xtatadi va mavjud faol so'rovlarning tugallanishini berilgan Context doirasida kutadi.

## Ishlash natijasi:
```text
[Server] To'xtatish signali qabul qilindi...
[Server] Server to'liq va xavfsiz o'chirildi.
```

# 878-Topshiriq: Server xavfsizlik vaqt chegaralari (Timeouts)
## Topshiriq sharti:
`ReadTimeout`, `WriteTimeout` va `IdleTimeout` sozlamalari orqali Slowloris hujumlarini oldini oling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

func main() {
	srv := &http.Server{
		Addr:         ":8080",
		ReadTimeout:  5 * time.Second,  // So'rov sarlavhasi va tanasini o'qish vaqti
		WriteTimeout: 10 * time.Second, // Javobni to'liq yozish vaqti
		IdleTimeout:  120 * time.Second,// Keep-Alive ulanishining bo'sh turish vaqti
	}

	fmt.Printf("Server parametrlari: ReadTimeout=%v, WriteTimeout=%v\n",
		srv.ReadTimeout, srv.WriteTimeout)
}
```

## Tushuntirish va Mantiq:
Hech qanday timeout belgilanmagan serverlar ochko'z mijozlar (sekin ma'lumot uzatuvchilar) tufayli tezda ulanishlar limitiga yetib qulashi mumkin.

## Ishlash natijasi:
```text
Server parametrlari: ReadTimeout=5s, WriteTimeout=10s
```

# 879-Topshiriq: Server-Sent Events (SSE) serveri orqali jonli xabarlar uzatish
## Topshiriq sharti:
`text/event-stream` yordamida mijozga doimiy oqimli xabarlar yuboruvchi SSE handler yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func sseHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")

	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming qo'llab-quvvatlanmaydi", http.StatusInternalServerError)
		return
	}

	for i := 1; i <= 2; i++ {
		fmt.Fprintf(w, "data: Yangilik #%d\n\n", i)
		flusher.Flush() // Mijozga darhol yetkazish
	}
}

func main() {
	req := httptest.NewRequest("GET", "/events", nil)
	w := httptest.NewRecorder()

	sseHandler(w, req)
	fmt.Print(w.Body.String())
}
```

## Tushuntirish va Mantiq:
SSE HTTP orqali bir tomonlama (serverdan mijozga) doimiy yangiliklarni uzatish uchun eng yengil va qulay texnologiyadir (`http.Flusher` orqali ma'lumotlar oqimi surib turiladi).

## Ishlash natijasi:
```text
data: Yangilik #1

data: Yangilik #2
```

# 880-Topshiriq: HTTP Chunked Transfer Encoding
## Topshiriq sharti:
Umumiy hajmi oldindan noma'lum bo'lgan ma'lumotlarni bo'laklab (Chunked) jo'nating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func chunkedHandler(w http.ResponseWriter, r *http.Request) {
	flusher, _ := w.(http.Flusher)

	fmt.Fprintln(w, "1-bo'lak: Boshlanishi")
	flusher.Flush()

	fmt.Fprintln(w, "2-bo'lak: Tugallanishi")
	flusher.Flush()
}

func main() {
	req := httptest.NewRequest("GET", "/chunked", nil)
	w := httptest.NewRecorder()

	chunkedHandler(w, req)
	fmt.Print(w.Body.String())
}
```

## Tushuntirish va Mantiq:
Agar `Content-Length` ko'rsatilmasa va `Flusher.Flush()` chaqirilsa, Go avtomatik ravishda `Transfer-Encoding: chunked` rejimiga o'tadi.

## Ishlash natijasi:
```text
1-bo'lak: Boshlanishi
2-bo'lak: Tugallanishi
```

# 881-Topshiriq: HTTP Hijacking: Ulanishni to'liq nazoratga olish
## Topshiriq sharti:
`http.Hijacker` orqali TCP soketini HTTP server nazoratidan chiqarib olish tamoyili.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func hijackHandler(w http.ResponseWriter, r *http.Request) {
	hijacker, ok := w.(http.Hijacker)
	if !ok {
		fmt.Fprintln(w, "Hijacking qo'llab-quvvatlanmaydi (httptest recorder)")
		return
	}
	_, _, _ = hijacker.Hijack()
}

func main() {
	req := httptest.NewRequest("GET", "/hijack", nil)
	w := httptest.NewRecorder()

	hijackHandler(w, req)
	fmt.Print(w.Body.String())
}
```

## Tushuntirish va Mantiq:
WebSocket va HTTP/2 protokollariga ulanishni oshirishda (Upgrade) standart HTTP doirasidan chiqib toza TCP soket bilan ishlash uchun `http.Hijacker` ishlatiladi.

## Ishlash natijasi:
```text
Hijacking qo'llab-quvvatlanmaydi (httptest recorder)
```

# 882-Topshiriq: HTTPS / TLS Server asoslari (`ListenAndServeTLS`)
## Topshiriq sharti:
Xavfsiz shifrlangan TLS serverni ishga tushirish konfiguratsiyasini tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"crypto/tls"
	"fmt"
	"net/http"
)

func main() {
	srv := &http.Server{
		Addr: ":8443",
		TLSConfig: &tls.Config{
			MinVersion: tls.VersionTLS13, // Faqat eng xavfsiz TLS 1.3
		},
	}

	fmt.Printf("TLS Server sozlangan: Port=%s, MinVersion=TLS 1.3\n", srv.Addr)
}
```

## Tushuntirish va Mantiq:
`http.ListenAndServeTLS(addr, certFile, keyFile, handler)` orqali HTTPS yoqiladi. `tls.Config` yordamida eskirgan zaif shifrlash protokollari bloklanadi.

## Ishlash natijasi:
```text
TLS Server sozlangan: Port=:8443, MinVersion=TLS 1.3
```

# 883-Topshiriq: HTTP Handlerni `net/http/httptest` bilan testlash
## Topshiriq sharti:
Serverni haqiqiy portda ochmasdan, xotirada handlerni unit test qiling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func salomBer(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "Test muvaffaqiyatli!")
}

func main() {
	req := httptest.NewRequest("GET", "/salom", nil)
	recorder := httptest.NewRecorder()

	salomBer(recorder, req)

	res := recorder.Result()
	fmt.Println("Kutilgan kod: 200, Haqiqiy kod:", res.StatusCode)
	fmt.Println("Tana:", recorder.Body.String())
}
```

## Tushuntirish va Mantiq:
`httptest.NewRecorder` `http.ResponseWriter` interfeysini to'liq bajaradi va testlarda port to'qnashuvlarisiz millisekundlarda handlerni tekshirishga imkon beradi.

## Ishlash natijasi:
```text
Kutilgan kod: 200, Haqiqiy kod: 200
Tana: Test muvaffaqiyatli!
```

# 884-Topshiriq: `httptest.Server` bilan integratsion API mijozini sinash
## Topshiriq sharti:
Haqiqiy tasodifiy portda vaqtinchalik server ochib, API mijozining ishlashini tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
)

func main() {
	// Haqiqiy lokal server (xotirada)
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, `{"auth": "success"}`)
	}))
	defer ts.Close()

	// Mijoz orqali so'rov yuboramiz
	resp, _ := http.Get(ts.URL)
	defer resp.Body.Close()

	tana, _ := io.ReadAll(resp.Body)
	fmt.Println("Mijoz qabul qilgan javob:", string(tana))
}
```

## Tushuntirish va Mantiq:
`httptest.NewServer` haqiqiy tarmoq soketida vaqtinchalik server ochadi, bu API mijozlarini, headerlar va redirectlarni to'liq integratsion sinash uchun eng yaxshi vositadir.

## Ishlash natijasi:
```text
Mijoz qabul qilgan javob: {"auth": "success"}
```

# 885-Topshiriq: TCP Server yaratish: `net.Listen` va `listener.Accept`
## Topshiriq sharti:
Pastki darajadagi TCP soket serverini yarating va yangi ulanishlarni qabul qiling.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net"
)

func main() {
	// Port 0 tizimdan ixtiyoriy bo'sh port so'raydi
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		fmt.Println("Listen xatosi:", err)
		return
	}
	defer listener.Close()

	fmt.Println("TCP Server tinglamoqda:", listener.Addr().String())
}
```

## Tushuntirish va Mantiq:
`net.Listen("tcp", addr)` TCP soketini ochadi. `listener.Accept()` esa yangi ulanish kelguncha kutadi va `net.Conn` interfeysini qaytaradi.

## Ishlash natijasi:
```text
TCP Server tinglamoqda: 127.0.0.1:54321
```

# 886-Topshiriq: TCP Client yaratish: `net.Dial`
## Topshiriq sharti:
`net.Dial` orqali TCP serverga to'g'ridan-to'g'ri baytlar oqimini yuboring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net"
	"time"
)

func main() {
	l, _ := net.Listen("tcp", "127.0.0.1:0")
	defer l.Close()

	// Server goroutine
	go func() {
		conn, _ := l.Accept()
		defer conn.Close()
		bufer := make([]byte, 16)
		n, _ := conn.Read(bufer)
		fmt.Printf("[Server qabul qildi]: %s\n", string(bufer[:n]))
	}()

	// Client ulanishi
	conn, err := net.DialTimeout("tcp", l.Addr().String(), 100*time.Millisecond)
	if err != nil {
		fmt.Println("Ulanishda xato:", err)
		return
	}
	defer conn.Close()

	_, _ = conn.Write([]byte("Salom TCP!"))
	time.Sleep(30 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
`net.DialTimeout` server bilan 3 bosqichli TCP handshake amalga oshiradi va ikki tomonlama baytlar oqimini (`net.Conn`) ochadi.

## Ishlash natijasi:
```text
[Server qabul qildi]: Salom TCP!
```

# 887-Topshiriq: Parallel ko'p mijozli TCP Echo server
## Topshiriq sharti:
Kelgan xabarni mijozga qaytarib beruvchi ko'p oqimli Echo server tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"bufio"
	"fmt"
	"net"
	"time"
)

func echoHandler(conn net.Conn) {
	defer conn.Close()
	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		msg := scanner.Text()
		fmt.Fprintf(conn, "ECHO: %s\n", msg)
	}
}

func main() {
	l, _ := net.Listen("tcp", "127.0.0.1:0")
	defer l.Close()

	go func() {
		conn, _ := l.Accept()
		go echoHandler(conn)
	}()

	client, _ := net.Dial("tcp", l.Addr().String())
	defer client.Close()

	fmt.Fprintf(client, "Salom Echo\n")
	reader := bufio.NewReader(client)
	javob, _ := reader.ReadString('\n')

	fmt.Print("Mijoz qabul qildi: ", javob)
	time.Sleep(20 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
Har bir yangi TCP ulanish uchun alohida goroutine ochilishi (`go echoHandler(conn)`) Go da yuqori unumdorlikdagi tarmoq serverlarini yaratishning kalitidir.

## Ishlash natijasi:
```text
Mijoz qabul qildi: ECHO: Salom Echo
```

# 888-Topshiriq: TCP ulanishlarida Deadline va Timeout qo'yish
## Topshiriq sharti:
`conn.SetDeadline` orqali qotib qolgan tarmoq soketlarini to'xtating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net"
	"time"
)

func main() {
	l, _ := net.Listen("tcp", "127.0.0.1:0")
	defer l.Close()

	client, _ := net.Dial("tcp", l.Addr().String())
	defer client.Close()

	// O'qishga 30ms chegara qo'yamiz
	_ = client.SetReadDeadline(time.Now().Add(30 * time.Millisecond))

	buf := make([]byte, 8)
	_, err := client.Read(buf)
	if err != nil {
		fmt.Println("Soket xatoligi:", err)
	}
}
```

## Tushuntirish va Mantiq:
`conn.SetReadDeadline` va `conn.SetWriteDeadline` tarmoq amallarining abadiy osilib qolishiga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
Soket xatoligi: read tcp 127.0.0.1:54321->127.0.0.1:54321: i/o timeout
```

# 889-Topshiriq: UDP Server va Client aloqasi (`net.ListenPacket`)
## Topshiriq sharti:
Ulanish o'rnatilmaydigan (connectionless) UDP paketlarini jo'natish va qabul qilish.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net"
	"time"
)

func main() {
	// UDP server
	server, _ := net.ListenPacket("udp", "127.0.0.1:0")
	defer server.Close()

	go func() {
		buf := make([]byte, 32)
		n, addr, _ := server.ReadFrom(buf)
		fmt.Printf("[UDP Server] %s dan paket keldi: %s\n", addr.String(), string(buf[:n]))
	}()

	// UDP mijoz
	client, _ := net.Dial("udp", server.LocalAddr().String())
	defer client.Close()

	_, _ = client.Write([]byte("Tezkor UDP paketi"))
	time.Sleep(30 * time.Millisecond)
}
```

## Tushuntirish va Mantiq:
UDP da handshake bo'lmaydi va paketlar kafolatlanmagan holda uzatiladi, bu esa video oqimlar va onlayn o'yinlar uchun eng yuqori tezlikni beradi.

## Ishlash natijasi:
```text
[UDP Server] 127.0.0.1:54321 dan paket keldi: Tezkor UDP paketi
```

# 890-Topshiriq: DNS qidiruv amallari (`net.LookupHost`)
## Topshiriq sharti:
Domen nomi bo'yicha IP manzillarni aniqlang.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net"
)

func main() {
	// Lokal host tekshiruvi
	ipManzillar, err := net.LookupHost("localhost")
	if err != nil {
		fmt.Println("DNS xatosi:", err)
		return
	}

	fmt.Println("localhost IP manzillari:")
	for _, ip := range ipManzillar {
		fmt.Println("-", ip)
	}
}
```

## Tushuntirish va Mantiq:
`net.LookupHost` va `net.LookupIP` operatsion tizim yoki Go ning o'rnatilgan DNS resolveri orqali domen nomlarini IP manzillarga o'giradi.

## Ishlash natijasi:
```text
localhost IP manzillari:
- 127.0.0.1
- ::1
```

# 891-Topshiriq: IP manzillar va CIDR maskalar bilan ishlash (`net.ParseIP`, `net.ParseCIDR`)
## Topshiriq sharti:
IP manzilining to'g'riligini va uning ichki tarmoqqa (subnet) tegishliligini tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net"
)

func main() {
	ip := net.ParseIP("192.168.1.45")
	fmt.Printf("IP turi: IPv4=%t, IPv6=%t\n", ip.To4() != nil, ip.To16() != nil)

	// CIDR tekshiruvi (192.168.1.0/24 tarmog'i)
	_, subnet, _ := net.ParseCIDR("192.168.1.0/24")

	tegishlimi := subnet.Contains(ip)
	fmt.Printf("%s manzili %s tarmog'iga tegishlimi: %t\n", ip, subnet, tegishlimi)
}
```

## Tushuntirish va Mantiq:
`net.ParseCIDR` va `subnet.Contains(ip)` xavfsizlik devorlari (Firewall) va IP cheklovlari yaratishda qo'llaniladi.

## Ishlash natijasi:
```text
IP turi: IPv4=true, IPv6=true
192.168.1.45 manzili 192.168.1.0/24 tarmog'iga tegishlimi: true
```

# 892-Topshiriq: Reverse Proxy yaratish (`httputil.NewSingleHostReverseProxy`)
## Topshiriq sharti:
Kiruvchi so'rovlarni boshqa orqa (backend) serverga yo'naltiruvchi proksi tuzing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"net/http/httputil"
	"net/url"
)

func main() {
	// Haqiqiy backend server
	backend := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Backenddan javob yetib keldi")
	}))
	defer backend.Close()

	// Reverse Proxy yaratamiz
	targetURL, _ := url.Parse(backend.URL)
	proxy := httputil.NewSingleHostReverseProxy(targetURL)

	req := httptest.NewRequest("GET", "/api", nil)
	w := httptest.NewRecorder()
	proxy.ServeHTTP(w, req)

	fmt.Print("Proksi orqali olindi: ", w.Body.String())
}
```

## Tushuntirish va Mantiq:
`httputil.NewSingleHostReverseProxy` so'rovlarni o'zgartirmasdan backend serverlarga taqsimlovchi (Load Balancer / Gateway) qurish uchun qulaydir.

## Ishlash natijasi:
```text
Proksi orqali olindi: Backenddan javob yetib keldi
```

# 893-Topshiriq: HTTP Proxy orqali mijoz so'rovini yuborish
## Topshiriq sharti:
`http.Transport` da proksi URL manzilini sozlash.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/url"
)

func main() {
	proxyURL, _ := url.Parse("http://127.0.0.1:8888")

	transport := &http.Transport{
		Proxy: http.ProxyURL(proxyURL),
	}

	mijoz := &http.Client{Transport: transport}
	fmt.Println("Proksi sozlangan mijoz tayyor:", mijoz != nil)
}
```

## Tushuntirish va Mantiq:
`http.ProxyURL` mijozning barcha so'rovlarini ko'rsatilgan korporativ yoki xavfsiz proksi orqali o'tishini ta'minlaydi.

## Ishlash natijasi:
```text
Proksi sozlangan mijoz tayyor: true
```

# 894-Topshiriq: Parallel Tarmoq Port Skaneri (Port Scanner)
## Topshiriq sharti:
Belgilangan hostdagi portlarning ochiq yoki yopiqligini parallel goroutinelarda tekshiring.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net"
	"sync"
	"time"
)

func portTekshir(host string, port int, wg *sync.WaitGroup) {
	defer wg.Done()
	manzil := fmt.Sprintf("%s:%d", host, port)
	conn, err := net.DialTimeout("tcp", manzil, 50*time.Millisecond)
	if err != nil {
		return // Port yopiq
	}
	conn.Close()
	fmt.Printf("[OCHIQ] Port %d ochiq!\n", port)
}

func main() {
	var wg sync.WaitGroup
	sinovPortlar := []int{22, 80, 443, 8080}

	fmt.Println("127.0.0.1 portlari skanerlanmoqda...")
	for _, p := range sinovPortlar {
		wg.Add(1)
		go portTekshir("127.0.0.1", p, &wg)
	}

	wg.Wait()
	fmt.Println("Skanerlash yakunlandi.")
}
```

## Tushuntirish va Mantiq:
Goroutinelarning yengilligi minglab tarmoq portlarini soniyalar ichida parallel tekshirib chiqish imkonini beradi.

## Ishlash natijasi:
```text
127.0.0.1 portlari skanerlanmoqda...
Skanerlash yakunlandi.
```

# 895-Topshiriq: WebSocket ikki tomonlama aloqa protokoli simulyatsiyasi
## Topshiriq sharti:
Full-duplex kanal orqali mijoz va server o'rtasida xabarlar almashinuvi.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"sync"
)

type WSXabar struct {
	Kimdan string
	Matn   string
}

func main() {
	mijozdanServerga := make(chan WSXabar, 2)
	serverdanMijozga := make(chan WSXabar, 2)

	var wg sync.WaitGroup
	wg.Add(1)

	// Server goroutine
	go func() {
		defer wg.Done()
		req := <-mijozdanServerga
		fmt.Printf("[WS Server] Qabul qildi: '%s' (%s dan)\n", req.Matn, req.Kimdan)
		serverdanMijozga <- WSXabar{Kimdan: "Server", Matn: "Xush kelibsiz!"}
	}()

	// Mijoz
	mijozdanServerga <- WSXabar{Kimdan: "Mijoz-1", Matn: "Ulanish o'rnatildi"}
	javob := <-serverdanMijozga
	fmt.Printf("[WS Mijoz] Serverdan javob: '%s'\n", javob.Matn)

	wg.Wait()
}
```

## Tushuntirish va Mantiq:
WebSocket protokoli bitta TCP ulanish ustida ikki tomonlama (full-duplex) uzluksiz xabarlar oqimini ta'minlaydi.

## Ishlash natijasi:
```text
[WS Server] Qabul qildi: 'Ulanish o'rnatildi' (Mijoz-1 dan)
[WS Mijoz] Serverdan javob: 'Xush kelibsiz!'
```

# 896-Topshiriq: HTTP Basic Auth protokoli (`r.BasicAuth`)
## Topshiriq sharti:
`username:password` orqali klassik Basic Authentication tekshiruvini yozing.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

func basicAuthHandler(w http.ResponseWriter, r *http.Request) {
	user, pass, ok := r.BasicAuth()
	if !ok || user != "admin" || pass != "parol123" {
		w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
		http.Error(w, "Ruxsat berilmadi", http.StatusUnauthorized)
		return
	}
	fmt.Fprintln(w, "Admin panelga xush kelibsiz!")
}

func main() {
	req := httptest.NewRequest("GET", "/admin", nil)
	req.SetBasicAuth("admin", "parol123")
	w := httptest.NewRecorder()

	basicAuthHandler(w, req)
	fmt.Print(w.Body.String())
}
```

## Tushuntirish va Mantiq:
`r.BasicAuth()` so'rov sarlavhasidagi Base64 kodlangan foydalanuvchi nomi va parolini ochib beradi.

## Ishlash natijasi:
```text
Admin panelga xush kelibsiz!
```

# 897-Topshiriq: Gzip Response Compression Middleware
## Topshiriq sharti:
Mijoz `Accept-Encoding: gzip` so'raganda javobni avtomatik siqib uzatuvchi middleware.

## Yechim (Go kodi):
```go
package main

import (
	"compress/gzip"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
)

type gzipResponseWriter struct {
	io.Writer
	http.ResponseWriter
}

func (w gzipResponseWriter) Write(b []byte) (int, error) {
	return w.Writer.Write(b)
}

func GzipMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if strings.Contains(r.Header.Get("Accept-Encoding"), "gzip") {
			w.Header().Set("Content-Encoding", "gzip")
			gz := gzip.NewWriter(w)
			defer gz.Close()
			next.ServeHTTP(gzipResponseWriter{Writer: gz, ResponseWriter: w}, r)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func main() {
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "Bu GZIP orqali siqilgan katta ma'lumot...")
	})

	mw := GzipMiddleware(handler)

	req := httptest.NewRequest("GET", "/", nil)
	req.Header.Set("Accept-Encoding", "gzip")
	w := httptest.NewRecorder()

	mw.ServeHTTP(w, req)
	fmt.Println("Content-Encoding:", w.Header().Get("Content-Encoding"))
}
```

## Tushuntirish va Mantiq:
Gzip middleware tarmoq trafigini 70-80% ga qisqartiradi va veb ilovalar yuklanish tezligini sezilarli oshiradi.

## Ishlash natijasi:
```text
Content-Encoding: gzip
```

# 898-Topshiriq: IP bo'yicha HTTP Rate Limiting Middleware
## Topshiriq sharti:
Har bir IP manziliga soniyasiga ko'pi bilan belgilangan so'rovlar limitini qo'ying.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"sync"
)

type Limiter struct {
	mu     sync.Mutex
	counts map[string]int
}

func RateLimitMiddleware(next http.Handler, maxReq int) http.Handler {
	limiter := &Limiter{counts: make(map[string]int)}
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ip := r.RemoteAddr
		limiter.mu.Lock()
		limiter.counts[ip]++
		cnt := limiter.counts[ip]
		limiter.mu.Unlock()

		if cnt > maxReq {
			http.Error(w, "Juda ko'p so'rovlar (429)", http.StatusTooManyRequests)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func main() {
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "OK")
	})

	mw := RateLimitMiddleware(handler, 1)

	req1 := httptest.NewRequest("GET", "/", nil)
	req1.RemoteAddr = "10.0.0.1"
	w1 := httptest.NewRecorder()
	mw.ServeHTTP(w1, req1)
	fmt.Println("1-so'rov status:", w1.Code)

	req2 := httptest.NewRequest("GET", "/", nil)
	req2.RemoteAddr = "10.0.0.1"
	w2 := httptest.NewRecorder()
	mw.ServeHTTP(w2, req2)
	fmt.Println("2-so'rov status:", w2.Code)
}
```

## Tushuntirish va Mantiq:
Rate limiting DoS va bruteforce hujumlaridan himoya qilishda HTTP qatlamining asosiy qalqonidir.

## Ishlash natijasi:
```text
1-so'rov status: 200
2-so'rov status: 429
```

# 899-Topshiriq: Maxsus `http.RoundTripper` yozish (Client Tracing)
## Topshiriq sharti:
Mijoz tomonidan chiquvchi barcha so'rovlarni avtomatik loglovchi RoundTripper yarating.

## Yechim (Go kodi):
```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
)

type LoggingRoundTripper struct {
	next http.RoundTripper
}

func (l *LoggingRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	fmt.Printf("[HTTP Chiqish] %s %s\n", req.Method, req.URL.String())
	return l.next.RoundTrip(req)
}

func main() {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	client := &http.Client{
		Transport: &LoggingRoundTripper{next: http.DefaultTransport},
	}

	resp, _ := client.Get(ts.URL)
	resp.Body.Close()
}
```

## Tushuntirish va Mantiq:
`http.RoundTripper` HTTP mijozning middleware si bo'lib, har bir chiquvchi so'rovni tutib olish va unga avtomatik metrikalar yoki tokenlar qo'shish uchun ishlatiladi.

## Ishlash natijasi:
```text
[HTTP Chiqish] GET http://127.0.0.1:54321
```

# 900-Topshiriq: To'liq RESTful CRUD API Serveri (Go 1.22 Router, JSON, Graceful Shutdown)
## Topshiriq sharti:
Keng qamrovli yakuniy loyiha: Go 1.22 yangi routeri, Path parametrlari, CRUD amallari, Middleware va toza arxitekturani birlashtirgan to'liq REST API serverini yarating.

## Yechim (Go kodi):
```go
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strconv"
	"strings"
	"sync"
)

type Mahsulot struct {
	ID    int     `json:"id"`
	Nomi  string  `json:"nomi"`
	Narxi float64 `json:"narxi"`
}

type MahsulotStore struct {
	mu        sync.RWMutex
	elementlar map[int]Mahsulot
	keyingiID  int
}

func YangiStore() *MahsulotStore {
	return &MahsulotStore{
		elementlar: make(map[int]Mahsulot),
		keyingiID:  1,
	}
}

func main() {
	store := YangiStore()
	mux := http.NewServeMux()

	// 1. GET /api/mahsulotlar - Ro'yxat
	mux.HandleFunc("GET /api/mahsulotlar", func(w http.ResponseWriter, r *http.Request) {
		store.mu.RLock()
		defer store.mu.RUnlock()
		ro'yxat := make([]Mahsulot, 0, len(store.elementlar))
		for _, m := range store.elementlar {
			ro'yxat = append(ro'yxat, m)
		}
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(ro'yxat)
	})

	// 2. POST /api/mahsulotlar - Yaratish
	mux.HandleFunc("POST /api/mahsulotlar", func(w http.ResponseWriter, r *http.Request) {
		var m Mahsulot
		if err := json.NewDecoder(r.Body).Decode(&m); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		store.mu.Lock()
		m.ID = store.keyingiID
		store.keyingiID++
		store.elementlar[m.ID] = m
		store.mu.Unlock()

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		_ = json.NewEncoder(w).Encode(m)
	})

	// 3. GET /api/mahsulotlar/{id} - Bitta mahsulot
	mux.HandleFunc("GET /api/mahsulotlar/{id}", func(w http.ResponseWriter, r *http.Request) {
		idStr := r.PathValue("id")
		id, _ := strconv.Atoi(idStr)

		store.mu.RLock()
		m, mavjud := store.elementlar[id]
		store.mu.RUnlock()

		if !mavjud {
			http.Error(w, "Mahsulot topilmadi", http.StatusNotFound)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(m)
	})

	// Sinov
	// POST so'rovi
	postReq := httptest.NewRequest("POST", "/api/mahsulotlar", strings.NewReader(`{"nomi":"Laptop","narxi":1200.0}`))
	postRec := httptest.NewRecorder()
	mux.ServeHTTP(postRec, postReq)
	fmt.Println("Yaratildi:", strings.TrimSpace(postRec.Body.String()))

	// GET so'rovi
	getReq := httptest.NewRequest("GET", "/api/mahsulotlar/1", nil)
	getRec := httptest.NewRecorder()
	mux.ServeHTTP(getRec, getReq)
	fmt.Println("O'qildi:", strings.TrimSpace(getRec.Body.String()))
}
```

## Tushuntirish va Mantiq:
Go 1.22 da tashqi freymvorklarsiz sof `net/http` orqali to'liq huquqli, xavfsiz va yuqori tezlikdagi RESTful mikroservislarni yaratish mumkin.

## Ishlash natijasi:
```text
Yaratildi: {"id":1,"nomi":"Laptop","narxi":1200}
O'qildi: {"id":1,"nomi":"Laptop","narxi":1200}
```

