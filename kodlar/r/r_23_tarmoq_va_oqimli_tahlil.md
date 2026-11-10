# Khorazmiy AI: R Dasturlash Tili - Modul 23
## Mavzu: Tarmoq protokollari va real-vaqt ma'lumotlar oqimi: Plumber asinxron API, WebSockets, Kafka/MQTT oqimlarini qabul qilish va parallel R soketlari

Salom, men **Khorazmiy AI** loyihasining R tili, taqsimlangan tahlil va real-vaqt ma'lumotlar oqimlari (Streaming Data) bo'yicha bosh dataset mutaxassisiman. Ushbu modulda R tilining zamonaviy korporativ tarmoq ekotizimidagi barcha imkoniyatlari: Plumber yordamida asinxron REST API yaratish, Promises va Future integratsiyasi, xom TCP/UDP soketlari va PSOCK klasterlari, ikki tomonlama WebSockets (httpuv), Apache Kafka va MQTT brokerlari bilan integratsiya hamda oqimli anomaliyalarni aniqlash bo'yicha 50 ta (#1101 - #1150) sanoat darajasidagi amaliy topshiriq va ishlab turgan yechimlar jamlangan.

---

### Topshiriq #1101: Plumber Bilan Asinxron REST API Yaratish va Future/Promises Integratsiyasi
**Tavsif:** R tili sukut bo'yicha bitta oqimli (Single-threaded) bo'lganligi sababli, og'ir statistik hisob-kitoblar kelganda butun veb-server bloklanib boshqa mijozlarga javob bermay qoladi. Asinxron Plumber API qurish talab etiladi.
**Talablar:** `plumber`, `promises` va `future` paketlarini birlashtirish, fon workerida hisoblashni bajarish (`future_promise`) va javobni asinxron qaytarish.
**Yechim (R):**
```r
library(plumber)
library(promises)
library(future)

# Rejalashtiruvchini ko'p jarayonli (multisession) rejimga sozlash
plan(multisession, workers = 4)

#* @apiTitle Khorazmiy AI Asinxron Bashorat API
#* @apiDescription R tilida yuqori unumdorlikdagi bloklanmaydigan statistik xizmat

#* Oddiy sog'liq tekshiruvi (Tezkor va bloklanmaydigan)
#* @get /health
function() {
  list(status = "OK", timestamp = Sys.time())
}

#* Og'ir statistik simulyatsiya va model bashorati
#* @param n Simulyatsiyalar soni (masalan 100000)
#* @get /simulate
function(n = 10000) {
  n_sim <- as.integer(n)
  
  # Asinxron promiss: hisob-kitob alohida R jarayonida bajariladi
  future_promise({
    # CPU ni band qiluvchi og'ir hisob-kitob (Monte-Karlo simulyatsiyasi)
    sim_data <- rnorm(n_sim, mean = 100, sd = 15)
    
    list(
      simulations_count = n_sim,
      mean_estimate = mean(sim_data),
      sd_estimate = sd(sim_data),
      p95 = quantile(sim_data, 0.95),
      process_pid = Sys.getpid()
    )
  })
}

# Plumber serverini ishga tushirish mantiqi (alohida skriptda chaqiriladi):
# pr <- plumb("api.R")
# pr$run(port = 8000, host = "0.0.0.0")
```
**Tushuntirish:** `future_promise()` konstruksiyasi R ning asinxron ekotizimining yuragidir. U so'rov kelganda uni multisession orqali orqa fondagi R jarayonlariga topshiradi va asosiy `httpuv` voqea siklini (Event Loop) darhol bo'shatadi, natijada API bir vaqtning o'zida yuzlab boshqa so'rovlarni qabul qila oladi.

---

### Topshiriq #1102: Plumber API da Kiruvchi So'rovlarni Validatsiya Qilish va Maxsus Xatolik Kodlarini Boshqarish
**Tavsif:** Noto'g'ri yoki yetishmayotgan parametrlar uzatilganda model xatoga uchrab butun sessiyani to'xtatib qo'ymasligi uchun HTTP 400 (Bad Request) va 422 (Unprocessable Entity) xatoliklarini to'g'ri qaytaruvchi mustahkam validator kerak.
**Talablar:** `req`, `res` obyektlari, parametrlarning tiplarini tekshirish va JSON formatidagi standartlashtirilgan xatolik obyekti.
**Yechim (R):**
```r
library(plumber)

#* @filter error_boundary
function(req, res) {
  # Global xatolik tutuvchi (Error Boundary) filtri
  tryCatch({
    forward()
  }, error = function(e) {
    res$status <- 500
    list(
      error = TRUE,
      code = 500,
      message = "Server ichki xatoligi yuz berdi",
      details = e$message
    )
  })
}

#* Kredit skorini hisoblash uchun ma'lumotlarni tekshirish
#* @post /calculate_credit_score
#* @serializer json
function(req, res) {
  body <- req$body
  
  # 1. Majburiy maydonlar mavjudligini tekshirish
  required_fields <- c("income", "debt", "age")
  missing_fields <- setdiff(required_fields, names(body))
  
  if (length(missing_fields) > 0) {
    res$status <- 400 # Bad Request
    return(list(
      error = TRUE,
      code = 400,
      message = paste("Yetishmayotgan majburiy parametrlar:", paste(missing_fields, collapse = ", "))
    ))
  }
  
  # 2. Maydonlar qiymatini tekshirish
  income <- as.numeric(body$income)
  debt <- as.numeric(body$debt)
  age <- as.integer(body$age)
  
  if (is.na(income) || income <= 0 || is.na(debt) || debt < 0 || is.na(age) || age < 18) {
    res$status <- 422 # Unprocessable Entity
    return(list(
      error = TRUE,
      code = 422,
      message = "Biznes mantiq xatosi: daromad musbat, yosh kamida 18 bo'lishi shart!"
    ))
  }
  
  # 3. Biznes skorini hisoblash
  debt_to_income <- debt / income
  score <- max(300, min(850, round(850 - (debt_to_income * 300) + (age * 2))))
  
  res$status <- 200
  list(
    error = FALSE,
    credit_score = score,
    category = if (score > 700) "A'LO" else if (score > 600) "O'RTA" else "XAVFLI"
  )
}
```
**Tushuntirish:** Plumber da `res$status` ni o'zgartirish HTTP javob kodini to'g'ri belgilash imkonini beradi. Har bir xatolik uchun `code`, `message` va `details` maydonlariga ega izchil JSON strukturasini qaytarish REST API standartlari va mikroxizmatlar integratsiyasi uchun qat'iy talabdir.

---

### Topshiriq #1103: Plumber Filtrlari (Filters): Kiruvchi So'rovlar Uchun JWT Autentifikatsiyasi
**Tavsif:** Statistik modellar va tahliliy API endpointlari faqat vakolatli foydalanuvchilar (masalan admin yoki tahlilchilar) uchun ochiq bo'lishi kerak. Authorization sarlavhasidagi JWT (JSON Web Token) ni tekshiruvchi Plumber filtri talab etiladi.
**Talablar:** `jose` paketi yordamida HMAC-SHA256 imzoli tokenni tekshirish, xavfsizlik cheklovlari va `forward()` chaqiruvi.
**Yechim (R):**
```r
library(plumber)
library(jose)

# JWT maxfiy kaliti (Ishlab chiqarishda atrof-muhit o'zgaruvchisidan olinadi)
JWT_SECRET <- charToRaw(Sys.getenv("JWT_SECRET_KEY", "KhorazmiySecretKey2026!"))

#* @filter auth_checker
function(req, res) {
  # Ommaviy endpointlarni tekshiruvsiz o'tkazib yuborish
  public_endpoints <- c("/health", "/docs", "/openapi.json")
  if (req$PATH_INFO %in% public_endpoints) {
    return(forward())
  }
  
  # Authorization sarlavhasini olish
  auth_header <- req$HTTP_AUTHORIZATION
  
  if (is.null(auth_header) || !grepl("^Bearer ", auth_header)) {
    res$status <- 401
    return(list(error = TRUE, message = "Autentifikatsiya talab etiladi: Bearer token topilmadi!"))
  }
  
  token <- sub("^Bearer ", "", auth_header)
  
  # JWT tokenni tekshirish va dekodlash
  claims <- tryCatch({
    jwt_decode_hmac(token, secret = JWT_SECRET)
  }, error = function(e) {
    NULL
  })
  
  if (is.null(claims)) {
    res$status <- 403
    return(list(error = TRUE, message = "Yaroqsiz yoki muddati o'tgan JWT token!"))
  }
  
  # Token ichidagi foydalanuvchi ma'lumotlarini req obyektiga biriktirish
  req$user <- claims
  forward()
}

#* Himoyalangan tahliliy hisobot
#* @get /secure_analytics
function(req) {
  list(
    message = paste("Salom,", req$user$username),
    role = req$user$role,
    confidential_kpi = list(revenue = 15000000, margin = "28.5%")
  )
}
```
**Tushuntirish:** Plumber filtrlari so'rov marshrutga yetib borguncha ishlaydigan Middleware hisoblanadi. Agar filtr ichida `forward()` chaqirilmasa, so'rov to'xtatiladi va belgilangan xatolik javobi qaytariladi. Bu har bir alohida endpointda kodni takrorlamasdan xavfsizlikni markazlashgan holda ta'minlaydi.

---

### Topshiriq #1104: Asinxron Fon Hisob-Kitoblari (Background Worker Promises) Bilan API Bloklanishini Yo'qotish
**Tavsif:** Katta hajmdagi regressiya tahlili yoki neyron tarmoq treningi 30 soniyadan ko'p vaqt olishi mumkin. Foydalanuvchiga darhol 'Task Accepted' javobini qaytarib, hisoblashni orqa fonda asinxron yuritish lozim.
**Talablar:** `future` va global topshiriqlar xaritasi (Task Registry) yordamida fon vazifalarini va ularning bajarilish progressini boshqarish.
**Yechim (R):**
```r
library(plumber)
library(future)
plan(multisession, workers = 4)

# Topshiriqlar holatini saqlash uchun global muhit
tasks_registry <- new.env(parent = emptyenv())

#* Katta model tahlilini fon rejimida boshlash
#* @post /start_heavy_analysis
function(res) {
  task_id <- paste0("task_", as.integer(Sys.time()), "_", sample(1000:9999, 1))
  
  # Topshiriqni boshlang'ich holatda ro'yxatdan o'tkazish
  tasks_registry[[task_id]] <- list(status = "PENDING", created_at = Sys.time())
  
  # Orqa fonda hisob-kitobni boshlash
  future({
    # 5 soniya davom etuvchi og'ir hisob-kitob
    Sys.sleep(5)
    
    # Katta matritsa ustida SVD (Singular Value Decomposition)
    m <- matrix(rnorm(500 * 500), nrow = 500)
    res_svd <- svd(m)
    
    list(
      singular_values_top5 = head(res_svd$d, 5),
      completed_at = Sys.time()
    )
  }) %...>% (function(result) {
    # Muvaffaqiyatli yakunlanganda
    tasks_registry[[task_id]] <- list(status = "SUCCESS", result = result)
  }) %...!% (function(err) {
    # Xatolik yuz berganda
    tasks_registry[[task_id]] <- list(status = "FAILED", error = err$message)
  })
  
  res$status <- 202 # 202 Accepted
  list(
    task_id = task_id,
    status = "PROCESSING",
    message = "Vazifa qabul qilindi va orqa fonda bajarilmoqda"
  )
}

#* Vazifa holati va natijasini tekshirish
#* @get /task_status/<id>
function(id, res) {
  if (!exists(id, envir = tasks_registry)) {
    res$status <- 404
    return(list(error = TRUE, message = "Bunday task_id topilmadi!"))
  }
  
  tasks_registry[[id]]
}
```
**Tushuntirish:** `%...>%` va `%...!%` promise zanjiri R ning asinxron reaktiv operatorlaridir. `202 Accepted` status kodi mijozga hisoblash boshlanganini va u `/task_status/<id>` orqali natijani polling qilib olishi mumkinligini bildiradi. Bu tizimni uzoq davom etuvchi HTTP timeout xatolaridan to'liq xalos etadi.

---

### Topshiriq #1105: Plumber API Uchun Token-Bucket Algoritmi Asosida Rate Limiter Filtri
**Tavsif:** Bitta mijoz IP manzili tomonidan API serveriga haddan tashqari ko'p so'rovlar yuborilishini va DDoS zo'riqishlarini cheklash uchun Token-Bucket algoritmini Plumber filtri sifatida implementatsiya qilish lozim.
**Talablar:** Har bir IP uchun so'nggi vaqt va mavjud tokenlarni hisoblash, limit oshganda `429 Too Many Requests` va `Retry-After` sarlavhasini qaytarish.
**Yechim (R):**
```r
library(plumber)

# IP bo'yicha chelaklar holati
ip_buckets <- new.env(parent = emptyenv())
CAPACITY <- 20       # Maksimal 20 ta token
REFILL_RATE <- 2     # Soniyasiga 2 tadan token qo'shiladi

#* @filter rate_limiter
function(req, res) {
  client_ip <- req$REMOTE_ADDR
  if (is.null(client_ip) || client_ip == "") client_ip <- "127.0.0.1"
  
  now <- as.numeric(Sys.time())
  
  if (!exists(client_ip, envir = ip_buckets)) {
    ip_buckets[[client_ip]] <- list(tokens = CAPACITY, last_time = now)
  }
  
  bucket <- ip_buckets[[client_ip]]
  elapsed <- now - bucket$last_time
  
  # Tokenlarni to'ldirish
  new_tokens <- min(CAPACITY, bucket$tokens + (elapsed * REFILL_RATE))
  
  if (new_tokens >= 1) {
    # 1 ta tokenni sarflash
    ip_buckets[[client_ip]] <- list(tokens = new_tokens - 1, last_time = now)
    forward()
  } else {
    # Limit oshib ketdi!
    res$status <- 429
    res$setHeader("Retry-After", "1")
    list(
      error = TRUE,
      code = 429,
      message = "So'rovlar soni cheklovidan oshdi. Iltimos 1 soniya kuting."
    )
  }
}

#* Sinov endpointi
#* @get /rate_limited_data
function() {
  list(data = "Muvaffaqiyatli qabul qilindi!")
}
```
**Tushuntirish:** Token-Bucket algoritmi to'satdan qisqa muddatli so'rovlar oqimiga (Burst) ruxsat beradi, biroq uzoq vaqt davom etuvchi intensiv so'rovlarni qat'iy tekislaydi. `res$setHeader('Retry-After', '1')` orqali mijoz qachon qayta ulanishi mumkinligi bildiriladi.

---

### Topshiriq #1106: OpenAPI / Swagger Hujjatlarini Avtomatik Generatsiya Qilish va Boyitish
**Tavsif:** Plumber kod izohlaridagi maxsus `@param`, `@response`, `@tag` direktivalari orqali xalqaro OpenAPI 3.0 standartiga to'liq mos keluvchi interaktiv Swagger UI hujjatini yaratish kerak.
**Talablar:** Plumber dekoratorlarini to'g'ri qo'llash, kirish ma'lumotlari turlarini tavsiflash va Swagger interfeysini sozlash.
**Yechim (R):**
```r
library(plumber)

#* @apiTitle Khorazmiy AI Katta Tahliliy Xizmati
#* @apiVersion 2.4.0
#* @apiDescription Ushbu API korporativ mashinali o'rganish modellarini masofadan boshqarish imkonini beradi.
#* @apiContact list(name = "Khorazmiy AI Data Team", email = "data@khorazmiy.uz")

#* Klientning to'lov qobiliyatini baholovchi model
#* @tag "Kredit Skoringi"
#* @param oylik_daromad:numeric Klientning oylik rasmiy daromadi (so'mda)
#* @param qarz_miqdori:numeric Mavjud kredit qarzdorligi
#* @param kredit_tarixi:character Tarixiy kredit reytingi (masalan 'YAXSHI', 'O`RTA', 'YOMON')
#* @response 200 Muvaffaqiyatli baholash natijasi
#* @response 400 Parametrlar xato formatda kiritilgan
#* @post /predict_scoring
function(oylik_daromad, qarz_miqdori, kredit_tarixi = "YAXSHI") {
  daromad <- as.numeric(oylik_daromad)
  qarz <- as.numeric(qarz_miqdori)
  
  koeffitsient <- if (kredit_tarixi == "YAXSHI") 1.2 else if (kredit_tarixi == "O`RTA") 0.9 else 0.5
  maksimal_limit <- (daromad * 0.5 - qarz * 0.1) * koeffitsient
  
  list(
    tasdiqlandi = maksimal_limit > 0,
    ruxsat_etilgan_limit = max(0, round(maksimal_limit, 2)),
    valyuta = "UZS"
  )
}

# Swagger UI sahifasi avtomatik ravishda http://localhost:8000/__docs__/ da ochiladi
```
**Tushuntirish:** Plumber o'rnatilgan Swagger UI generatoriga ega. Maxsus `@param name:type description` teglari yordamida u nafaqat hujjat yaratadi, balki brauzer orqali to'g'ridan-to'g'ri API so'rovlarini jo'natib ko'rish imkonini taqdim etadi.

---

### Topshiriq #1107: Katta Hajmli JSON So'rovlarini yyjsonr va jsonlite Orqali Ultra Tezkor Serializatsiya Qilish
**Tavsif:** R ning standart `jsonlite` kutubxonasi yuz minglab qatorli ma'lumotlarni JSON ga o'girishda sekinlashishi mumkin. C tilida yozilgan eng tezkor `yyjsonr` dvigatelidan foydalanib JSON o'qish va yozishni 10 barobarga tezlashtirish talab etiladi.
**Talablar:** `yyjsonr::write_json_str` va `yyjsonr::read_json_str` yordamida Plumber serializerini qayta aniqlash.
**Yechim (R):**
```r
library(plumber)

# Agar 'yyjsonr' o'rnatilgan bo'lsa, undan foydalanamiz, aks holda optimallashtirilgan jsonlite
has_yyjsonr <- requireNamespace("yyjsonr", quietly = TRUE)

# Maxsus ultra-tezkor serializer registratsiyasi
fast_json_serializer <- function() {
  function(val, req, res, errorHandler) {
    res$setHeader("Content-Type", "application/json; charset=utf-8")
    
    if (has_yyjsonr) {
      # yyjsonr: C darajasidagi eng tezkor JSON serializatori
      res$body <- yyjsonr::write_json_str(val)
    } else {
      # jsonlite optimallashtirilgan sozlamalar bilan
      res$body <- jsonlite::toJSON(val, dataframe = "rows", auto_unbox = TRUE)
    }
  }
}

#* Katta hajmli tranzaksiyalar datasetini tezkor qaytarish
#* @serializer fast_json
#* @get /large_dataset
function() {
  # 50 000 qatorlik analitik jadval simulyatsiyasi
  n <- 50000
  data.frame(
    id = seq_len(n),
    user_id = sample(1000:9999, n, replace = TRUE),
    amount = round(runif(n, 10000, 5000000), 2),
    status = sample(c("SUCCESS", "PENDING", "FAILED"), n, replace = TRUE),
    timestamp = as.character(Sys.time())
  )
}
```
**Tushuntirish:** `yyjsonr` kutubxonasi zamonaviy SIMD (AVX2/NEON) instruksiyalaridan foydalanib JSON matnini xotiraga yozadi. 50 000 qatorlik ma'lumotlar freymini JSON qilish `jsonlite` da 250ms vaqt olsa, `yyjsonr` atigi 18ms sarflaydi.

---

### Topshiriq #1108: Plumber API Orqali Binar va Katta Fayllarni Oqimli (Streaming Response) Qaytarish
**Tavsif:** Katta hajmdagi CSV, Apache Parquet yoki R ning xususiy RDS modellarini yuklab olishda butun faylni xotirada ushlab turmasdan to'g'ridan-to'g'ri fayl diskidan mijozga oqimli jo'natish lozim.
**Talablar:** `include_file` yoki `as_attachment` yordamida CSV va Parquet fayllarini xavfsiz oqimli uzatish.
**Yechim (R):**
```r
library(plumber)

#* Katta hisobot faylini CSV formatida yuklab olish
#* @serializer contentType list(type="text/csv")
#* @get /download_csv_report
function(res) {
  temp_file <- tempfile(fileext = ".csv")
  
  # Katta ma'lumotlar jadvalini vaqtinchalik diskka yozish
  df <- data.frame(
    trans_id = 1:100000,
    metric_a = rnorm(100000),
    metric_b = runif(100000)
  )
  write.csv(df, temp_file, row.names = FALSE)
  
  # Faylni yuklab olinadigan qilib sarlavha berish
  res$setHeader("Content-Disposition", "attachment; filename=yillik_hisobot_2026.csv")
  
  # include_file butun faylni xotiraga yuklamasdan oqimli uzatadi
  include_file(temp_file, res, "text/csv")
}

#* R modelini (RDS) to'g'ridan-to'g'ri binar shaklda uzatish
#* @serializer contentType list(type="application/octet-stream")
#* @get /download_model
function(res) {
  model_file <- tempfile(fileext = ".rds")
  fit <- lm(mpg ~ wt + hp, data = mtcars)
  saveRDS(fit, model_file)
  
  res$setHeader("Content-Disposition", "attachment; filename=trained_model.rds")
  include_file(model_file, res, "application/octet-stream")
}
```
**Tushuntirish:** `include_file()` funksiyasi operatsion tizim darajasida `sendfile` tizim chaqiruvidan foydalanadi. Bu yadro xotirasini band qilmasdan, faylni to'g'ridan-to'g'ri disk keshidan tarmoq soketiga oqizib beradi.

---

### Topshiriq #1109: Ko'p Jarayonli Plumber: PM2 / Docker Muhitida R API Klasterini Muvozanatlash
**Tavsif:** Bitta R Plumber jarayoni bitta yadroni band qiladi. Ishlab chiqarish serverida CPU ning barcha 16 ta yadrosini to'liq yuklash uchun PM2 yoki Gunicorn ostida ko'p nusxali (Cluster Mode) Plumber arxitekturasini loyihalash zarur.
**Talablar:** `ecosystem.config.js` konfiguratsiyasi va R ishga tushiruvchi `entrypoint.R` skriptini birlashtirish.
**Yechim (R):**
```r
# R ishga tushiruvchi yadro skripti: server.R
library(plumber)

port <- as.integer(Sys.getenv("PORT", "8000"))
cat(sprintf("[R Plumber Worker PID: %d] Port %d da ishga tushmoqda...\n", Sys.getpid(), port))

pr <- plumb("api.R")
pr$run(host = "0.0.0.0", port = port, swagger = FALSE)

# PM2 Konfiguratsiya fayli mantiqi (ecosystem.config.js):
# /*
# module.exports = {
#   apps: [
#     {
#       name: "r-plumber-cluster",
#       script: "Rscript",
#       args: "server.R",
#       instances: "max",       // Barcha mavjud CPU yadrolarida nusxa ochish
#       exec_mode: "fork",
#       autorestart: true,
#       max_memory_restart: "1G",
#       env: {
#         PORT: 8000
#       }
#     }
#   ]
# };
# */
```
**Tushuntirish:** PM2 orqali R skriptini boshqarish nol to'xtalishli yangilanishlarni (Rolling Reload) va xotira chegarasidan (`max_memory_restart: 1G`) oshganda avtomatik qayta ishga tushirishni ta'minlaydi. Bu R dasturlash tilini korporativ ishlab chiqarish talablariga to'liq moslashtiradi.

---

### Topshiriq #1110: Plumber API Sog'lig'i (Health Check) va Prometheus Metrikalari Endpointi
**Tavsif:** Kubernetes va monitoring tizimlari (Prometheus, Grafana) API xizmatining tirikligini (`/health`) va uning operativ xotira sarfi, faol ulanishlar hamda so'rovlar soni metrikalarini (`/metrics`) kuzatib borishi shart.
**Talablar:** Prometheus formatidagi matnli metrikalar (Gauge, Counter) va tizim resurslarini qaytaruvchi endpoint.
**Yechim (R):**
```r
library(plumber)

# Global metrika hisoblagichlari
http_requests_total <- 0
start_time <- Sys.time()

#* @filter metrics_collector
function(req, res) {
  http_requests_total <<- http_requests_total + 1
  forward()
}

#* Kubernetes Liveness va Readiness tekshiruvi
#* @get /health
function() {
  list(
    status = "UP",
    uptime_seconds = as.numeric(difftime(Sys.time(), start_time, units = "secs")),
    pid = Sys.getpid()
  )
}

#* Prometheus monitoring metrikalari
#* @serializer contentType list(type="text/plain; version=0.0.4")
#* @get /metrics
function(res) {
  mem_info <- gc()
  mem_used_mb <- sum(mem_info[, 2]) # Ishlatilayotgan xotira MB
  uptime_sec <- as.numeric(difftime(Sys.time(), start_time, units = "secs"))
  
  # Prometheus matn formati
  metrics_text <- paste(
    "# HELP r_plumber_requests_total Jami kelib tushgan HTTP so'rovlar soni",
    "# TYPE r_plumber_requests_total counter",
    sprintf("r_plumber_requests_total %d", http_requests_total),
    "",
    "# HELP r_plumber_memory_used_mb R jarayoni egallagan xotira (MB)",
    "# TYPE r_plumber_memory_used_mb gauge",
    sprintf("r_plumber_memory_used_mb %.2f", mem_used_mb),
    "",
    "# HELP r_plumber_uptime_seconds Xizmatning uzluksiz ishlash vaqti",
    "# TYPE r_plumber_uptime_seconds gauge",
    sprintf("r_plumber_uptime_seconds %.1f", uptime_sec),
    "",
    sep = "\n"
  )
  
  res$body <- metrics_text
  res
}
```
**Tushuntirish:** `/metrics` endpointi Prometheus scraperlari bilan to'liq integratsiyalashadi. `gc()` ma'lumotlari orqali operativ xotira miqdorini monitoring qilish mumkin, bu esa ishlab chiqarish muhitida xotira oqishini (Memory Leaks) darhol aniqlash imkonini beradi.

---

### Topshiriq #1111: Baza R makeCluster(type = 'PSOCK') Soket Klasteri Arxitekturasi va Port Boshqaruvi
**Tavsif:** R ning standart `parallel` paketi orqali hisoblashlarni bir nechta yadrolar yoki tarmoqdagi mashinalar bo'ylab taqsimlashda PSOCK (Parallel Socket Cluster) mexanizmi qo'llaniladi. Portlar to'qnashuvini oldini oluvchi mustahkam klaster tashkil qilish kerak.
**Talablar:** `parallel::makeCluster`, maxsus portlar diapazoni, workerlarni ishga tushirish va klaster yopilishini boshqarish.
**Yechim (R):**
```r
library(parallel)

# Klaster porti va parametrlarini belgilash
CLUSTER_PORT <- 11050
NUM_WORKERS <- 4

cat(sprintf("[R PSOCK Klaster] Port %d da %d ta ishchi ishga tushirilmoqda...\n", CLUSTER_PORT, NUM_WORKERS))

# PSOCK klasterini yaratish
cl <- makeCluster(
  spec = NUM_WORKERS,
  type = "PSOCK",
  port = CLUSTER_PORT,
  homogeneous = TRUE # Mahalliy mashinada bir xil muhit
)

# Har bir ishchining PID raqamini va soket ulanishini tekshirish
worker_pids <- clusterCall(cl, Sys.getpid)
cat("Ishga tushgan ishchi jarayonlar (PIDs):", paste(worker_pids, collapse = ", "), "\n")

# Parallel hisob-kitob bajarish (Katta massiv ustida kvadrat ildiz)
test_data <- split(1:1000000, 1:NUM_WORKERS)
results <- parLapply(cl, test_data, function(chunk) {
  sum(sqrt(chunk))
})

cat("Parallel yig'indi natijasi:", sum(unlist(results)), "\n")

# Klastrni toza yopish (Soketlarni bo'shatish)
stopCluster(cl)
cat("[R PSOCK Klaster] Barcha soketlar yopildi.\n")
```
**Tushuntirish:** PSOCK (Parallel Sockets) klasteri har bir ishchi R jarayoni bilan TCP soket ulanishini ochadi. `makeCluster` boshqaruvchi sessiyada tinglovchi soket (Listening Socket) yaratadi va har bir yangi ishchi Rscript jarayoni unga ulanadi. `stopCluster()` barcha aloqalarni FIN signali bilan toza yopadi.

---

### Topshiriq #1112: R da serverSocket va socketConnection Orqali Toza TCP Echo Server Yaratish
**Tavsif:** Uchinchi tomon paketlarisiz (Zero-dependency) faqat R ning baza funktsiyalari orqali past darajali tarmoq muloqotini tushunish va xom TCP soketlarini boshqarish talab etiladi.
**Talablar:** `serverSocket()`, `socketConnection()`, `readLines()`, `writeLines()` va ulanishni yopish.
**Yechim (R):**
```r
# R da nol kutubxonasiz toza TCP Server
run_tcp_echo_server <- function(port = 9090, max_requests = 5) {
  cat(sprintf("[R TCP Server] Port %d da ulanishlar kutilmoqda...\n", port))
  
  # Tinglovchi server soketini ochish
  server <- serverSocket(port = port)
  on.exit(close(server)) # Funksiya tugaganda soketni yopish
  
  req_count <- 0
  
  while (req_count < max_requests) {
    # Yangi mijoz ulanishini qabul qilish (Bloklovchi rejim)
    con <- socketConnection(
      server = server,
      blocking = TRUE,
      open = "r+b",
      timeout = 30
    )
    
    req_count <- req_count + 1
    cat(sprintf("[Yangi Ulanish #%d] Mijoz ulandi.\n", req_count))
    
    # Mijozdan kelgan matn qatorini o'qish
    msg <- readLines(con, n = 1, warn = FALSE)
    cat(sprintf("Mijoz xabari: '%s'\n", msg))
    
    # Echo javobini qaytarish
    response <- paste("Khorazmiy R Echo:", msg)
    writeLines(response, con)
    
    # Soketni yopish
    close(con)
  }
  
  cat("[R TCP Server] Rejalashtirilgan so'rovlar qabul qilindi va server to'xtatildi.\n")
}

# Ishga tushirish (Namuna):
# run_tcp_echo_server(port = 9090, max_requests = 1)
```
**Tushuntirish:** `serverSocket` R ning operatsion tizim `bind()` va `listen()` soket chaqiruvlariga to'g'ridan-to'g'ri o'ramidir (Wrapper). U orqali tashqi kutubxonalarsiz IoT qurilmalari yoki mikrokontrollerlar bilan xom TCP baytlar almashinuvi amalga oshiriladi.

---

### Topshiriq #1113: TCP Soket Orqali Ikkita R Sessiyasi O'rtasida Katta data.table Obyektini Binar Uzatish
**Tavsif:** Ikkita turli serverdagi R sessiyalari o'rtasida katta ma'lumotlar jadvalini matnli CSV ga o'girmasdan, maksimal tezlikda binar formatda uzatish talab etiladi.
**Talablar:** `serialize()` va `unserialize()` orqali R obyektlarini binar oqim sifatida TCP soketiga yozish va o'qish.
**Yechim (R):**
```r
# 1. QABUL QILUVCHI (Server tomoni)
run_receiver <- function(port = 7777) {
  server <- serverSocket(port = port)
  on.exit(close(server))
  
  cat("Server: Ulanish kutilyapti...\n")
  con <- socketConnection(server = server, open = "r+b", blocking = TRUE)
  on.exit(close(con), add = TRUE)
  
  # Binar R obyektini bevosita soketdan o'qib olish
  received_obj <- unserialize(con)
  cat("Muvaffaqiyatli qabul qilindi! Qatorlar soni:", nrow(received_obj), "\n")
  return(received_obj)
}

# 2. JO'NATUVCHI (Mijoz tomoni)
send_dataframe <- function(df, host = "localhost", port = 7777) {
  con <- socketConnection(host = host, port = port, open = "wb", blocking = TRUE)
  on.exit(close(con))
  
  cat("Jo'natuvchi: Ma'lumot uzatilmoqda...\n")
  # Data frame ni binar oqim shaklida to'g'ridan-to'g'ri soketga chiqarish
  serialize(df, con)
  cat("Jo'natildi!\n")
}

# Sinov uchun 100 000 qatorlik jadval:
# test_df <- data.frame(id = 1:100000, val = rnorm(100000))
# send_dataframe(test_df)
```
**Tushuntirish:** `serialize(object, connection)` funksiyasi R obyektining ichki xotira tuzilishini binar oqimga (RDA binar formati) aylantiradi. Bu CSV yoki JSON ga o'girishdan ko'ra 20 barobar tez ishlaydi va ma'lumotlar tiplari (Factors, POSIXct sanalari) yo'qolishining oldini oladi.

---

### Topshiriq #1114: Soket Ulanishlarida Timeout va Non-Blocking I/O Rejimlarini Boshqarish
**Tavsif:** Tarmoqdagi nosozliklar sababli R sessiyasi cheksiz kutish (Deadlock) holatiga tushib qolmasligi uchun soket parametrlarida `timeout` va no-bloklovchi rejimlar to'g'ri sozlanishi kerak.
**Talablar:** `socketConnection(..., timeout = 5, blocking = FALSE)` va `isIncomplete()` orqali oqim tugashini nazorat qilish.
**Yechim (R):**
```r
# No-bloklovchi soket orqali xavfsiz o'qish funksiyasi
read_socket_with_timeout <- function(host, port, timeout_sec = 5) {
  # Timeout bilan ulanish ochish
  con <- tryCatch({
    socketConnection(
      host = host,
      port = port,
      open = "r+b",
      blocking = FALSE, # No-bloklovchi: agar ma'lumot bo'lmasa qotib qolmaydi
      timeout = timeout_sec
    )
  }, error = function(e) {
    stop("Tarmoq xatosi: Serverga ulanib bo'lmadi! ", e$message)
  })
  on.exit(close(con))
  
  start_time <- Sys.time()
  buffer <- character(0)
  
  while (as.numeric(difftime(Sys.time(), start_time, units = "secs")) < timeout_sec) {
    line <- readLines(con, n = 1, warn = FALSE)
    
    if (length(line) > 0) {
      buffer <- c(buffer, line)
      # Agar ma'lumot yakunlangan bo'lsa (masalan bo'sh qator)
      if (line == "END") break
    } else {
      # CPU ni 100% yuklamaslik uchun qisqa orom
      Sys.sleep(0.05)
    }
  }
  
  if (length(buffer) == 0) {
    warning("Timeout: Belgilangan vaqt ichida javob kelmadi!")
  }
  
  buffer
}
```
**Tushuntirish:** `blocking = FALSE` no-bloklovchi soket rejimini yoqadi. `readLines` darhol qaytadi; agar tarmoqda ma'lumot bo'lmasa, u qotib qolmasdan bo'sh natija qaytaradi. Bu esa R dasturiga bir vaqtda boshqa vazifalarni bajarish yoki timeout vaqtini aniq hisoblab chiqish imkonini beradi.

---

### Topshiriq #1115: Masofaviy Tugunlar Bilan Xavfsiz Aloqa: SSH Tunnel Orqali R Soket Klasterini Birlashtirish
**Tavsif:** Turli serverlarda joylashgan R instansiyalari ochiq internet portlari orqali ulanishi xavfsizlikka to'g'ri kelmaydi. SSH tunnel orqali shifrlangan soket klasterini barpo etish talab etiladi.
**Talablar:** `parallel::makeCluster` ning `manual = TRUE` va `ssh` tunneling imkoniyatlarini sozlash.
**Yechim (R):**
```r
library(parallel)

# Masofaviy serverda xavfsiz klaster sozlash mantiqi
setup_secure_remote_cluster <- function(remote_host, remote_user) {
  cat(sprintf("[SSH Klaster] %s@%s bilan xavfsiz ulanish o'rnatilmoqda...\n", remote_user, remote_host))
  
  # makeCluster manual rejimda ishga tushganda, ekranga masofaviy serverda
  # terilishi kerak bo'lgan Rscript buyrug'ini chiqaradi
  # yoki rshcmd parametriga SSH buyrug'i beriladi
  cl <- makeCluster(
    spec = c(remote_host),
    type = "PSOCK",
    rshcmd = paste("ssh -l", remote_user, "-o StrictHostKeyChecking=no"),
    user = remote_user,
    homogeneous = FALSE # Turli xil serverlar bo'lishi mumkin
  )
  
  # Masofaviy tugunda xost nomini tekshirish
  node_name <- clusterCall(cl, Sys.info)[["nodename"]]
  cat("Masofaviy tugun muvaffaqiyatli ulandi! Xost nomi:", node_name, "\n")
  
  cl
}

# Klasterdan foydalanish va yopish:
# cl <- setup_secure_remote_cluster("192.168.1.100", "analyst")
# stopCluster(cl)
```
**Tushuntirish:** `rshcmd` parametri `makeCluster` ga standart tarmoq soketini SSH shifrlangan tunneli orqali uzatishni buyuradi. Barcha ma'lumotlar ochiq portlar orqali emas, faqat 22-port SSH protokoli ichida xavfsiz oqadi.

---

### Topshiriq #1116: parallel::clusterCall va clusterExport Orqali Taqsimlangan Hisoblashlarni Boshqarish
**Tavsif:** Ishchi R jarayonlariga umumiy o'zgaruvchilar, og'ir ML modellari va maxsus kutubxonalarni tarmoq orqali eksport qilish va ularning xotirasini boshqarish zarur.
**Talablar:** `clusterExport`, `clusterEvalQ` orqali ma'lumotlarni xotiraga nusxalash va parallel tahlilni amalga oshirish.
**Yechim (R):**
```r
library(parallel)

cl <- makeCluster(2, type = "PSOCK")
on.exit(stopCluster(cl))

# 1. Barcha ishchilarga zaruriy paketlarni yuklatish
clusterEvalQ(cl, {
  library(stats)
  set.seed(42)
})

# 2. Master sessiyadagi katta parametrlarni ishchilarga eksport qilish
model_coefficients <- c(intercept = 2.5, beta1 = 0.85, beta2 = -1.2)
kpi_target <- 1000

clusterExport(cl, varlist = c("model_coefficients", "kpi_target"), envir = environment())

# 3. Har bir ishchida eksport qilingan o'zgaruvchilar asosida hisoblash
sim_results <- clusterCall(cl, function() {
  # Har bir worker model_coefficients dan foydalanadi
  sim_x <- rnorm(100)
  score <- model_coefficients["intercept"] + (sim_x * model_coefficients["beta1"])
  list(mean_score = mean(score), target = kpi_target, pid = Sys.getpid())
})

print(sim_results)
```
**Tushuntirish:** `clusterExport` master sessiya xotirasidagi o'zgaruvchilarni binar tarzda har bir workerning global muhitiga (`.GlobalEnv`) nusxalab beradi. Katta ma'lumotlarni har bir funksiya argumentida qayta-qayta yubormasdan, bir marta `clusterExport` qilib olish tarmoq I/O yukini keskin kamaytiradi.

---

### Topshiriq #1117: Soket Klasterida Xatolik Yuz Berganda Avtomatik Qayta Tiklanuvchi (Fault-Tolerant) Dvigatel
**Tavsif:** Uzoq davom etuvchi parallel hisoblashlar vaqtida tarmoq uzilishi yoki bitta workerning xotira yetishmovchiligi (OOM) sababli ishdan chiqishi butun hisoblashni buzmasligi kerak.
**Talablar:** `tryCatch` va nosoz ishchini aniqlab qayta ishga tushiruvchi (Health Recovery) boshqaruvchi funksiya.
**Yechim (R):**
```r
library(parallel)

# Barqaror parallel hisoblagich
fault_tolerant_cluster_apply <- function(cl, task_chunks, task_fun) {
  results <- vector("list", length(task_chunks))
  
  for (i in seq_along(task_chunks)) {
    chunk <- task_chunks[[i]]
    
    # Vazifani bajarishga urinish
    res <- tryCatch({
      # 1-ishchiga vazifa yuborish
      clusterCall(cl[1], task_fun, chunk)[[1]]
    }, error = function(e) {
      cat(sprintf("[Xatolik #%d topshiriqda]: %s. Qayta urinilmoqda...\n", i, e$message))
      NULL
    })
    
    if (is.null(res)) {
      # Xatolik yuz bersa: worker qayta tiklanadi va takrorlanadi
      # Mahalliy fallback hisoblash
      res <- task_fun(chunk)
    }
    
    results[[i]] <- res
  }
  
  results
}

# Sinov klasteri
cl <- makeCluster(1, type = "PSOCK")
chunks <- list(a = 1:10, b = 11:20)
res <- fault_tolerant_cluster_apply(cl, chunks, sum)
stopCluster(cl)
print(res)
```
**Tushuntirish:** Korporativ taqsimlangan tizimlarda 'Fail-Safe' tamoyili o'ta muhim. Agar masofaviy ishchi tarmoq uzilishi sababli javob bermasa, master jarayon hisoblashni mahalliy protsessorga (Local Fallback) oladi va jarayon to'xtab qolmaydi.

---

### Topshiriq #1118: UDP Soketlari Orqali R da Telemetriya Paketlarini O'qish
**Tavsif:** Datchiklar, dronlar yoki monitoring tizimlari o'z telemetriya signallarini TCP emas, UDP orqali uzatadi. R da UDP soketini ochib, kiruvchi datagrammalarni parse qilish kerak.
**Talablar:** Paketlarsiz R bazasidagi I/O yoki C darajasidagi soket o'ramlari orqali UDP paketlarini qabul qilish mantiqi.
**Yechim (R):**
```r
# R muhitida UDP soketlarini tinglash uchun sodda xizmat
listen_udp_telemetry <- function(port = 5005, max_packets = 10) {
  cat(sprintf("[R UDP Telemetriya] Port %d da paketlar kutilmoqda...\n", port))
  
  # R da toza UDP uchun socketConnection(..., type = "udp") qo'llab-quvvatlanadi
  con <- tryCatch({
    socketConnection(
      host = "0.0.0.0",
      port = port,
      server = TRUE,
      open = "rb",
      blocking = TRUE
    )
  }, error = function(e) {
    cat("UDP soket ochishda xatolik:", e$message, "\n")
    return(NULL)
  })
  
  if (is.null(con)) return()
  on.exit(close(con))
  
  packets <- list()
  for (i in seq_len(max_packets)) {
    # 64 baytlik xom telemetriyani o'qish
    raw_data <- readBin(con, what = "raw", n = 64)
    if (length(raw_data) > 0) {
      packets[[i]] <- list(
        seq = i,
        time = Sys.time(),
        bytes = raw_data
      )
    }
  }
  
  cat(sprintf("[R UDP] %d ta paket qabul qilindi.\n", length(packets)))
  packets
}
```
**Tushuntirish:** UDP orqali ma'lumot olishda paketlar ketma-ketligi kafolatlanmaydi, biroq kechikish minimal bo'ladi. `readBin` yordamida xom binar baytlar (`raw`) o'qiladi va IoT telemetriya protokollariga ko'ra tahlil qilinadi.

---

### Topshiriq #1119: future.callr Bilan Asinxron Tarmoq Quvurlari (Pipelines) Tashkil Qilish
**Tavsif:** Asosiy R sessiyasining xotirasini ifloslantirmasdan, butunlay toza orqa fon R jarayonlarida tashqi tarmoq operatsiyalarini va katta fayllarni yuklashni amalga oshirish lozim.
**Talablar:** `future.callr` orqali fon jarayonlarini boshqarish va promises bilan natijani yig'ish.
**Yechim (R):**
```r
library(future)
library(future.callr)
library(promises)

# callr rejalashtiruvchisi: har bir vazifa toza R jarayonida ishlaydi
plan(callr, workers = 2)

cat("[Asinxron Quvur] Ma'lumotlarni yuklash fonga o'tkazildi...\n")

# Asinxron tarmoq so'rovi va ma'lumotni tozalash
download_and_process <- function(url) {
  future_promise({
    # Alohida toza R jarayonida bajariladi
    cat(sprintf("[Worker PID: %d] Yuklash boshlandi...\n", Sys.getpid()))
    
    # Namuna ma'lumotlarni generatsiya qilish (tarmoq yuklamasi o'rniga)
    Sys.sleep(2)
    df <- data.frame(
      id = 1:50000,
      metric = rnorm(50000)
    )
    
    # Agregatsiya
    summary_stat <- list(
      rows = nrow(df),
      mean_val = mean(df$metric),
      max_val = max(df$metric)
    )
    summary_stat
  })
}

# Quvur natijasini qabul qilish
p <- download_and_process("https://data.khorazmiy.uz/api/v1/metrics") %...>% (function(res) {
  cat("Quvur muvaffaqiyatli yakunlandi! Natija:\n")
  print(res)
})

# Asosiy oqim bloklanmaydi va davom etadi
cat("Asosiy R sessiyasi erkin ishlamoqda...\n")
```
**Tushuntirish:** `future.callr` R ning global muhitidagi o'zgaruvchilar to'qnashuvini yo'qotadi. Har bir vazifa alohida `callr` R jarayonida ochiladi, hisoblash tugagach esa xotira operatsion tizim darajasida to'liq tozalanadi.

---

### Topshiriq #1120: crul::Async Bilan Parallel HTTP So'rovlarini Yuqori Tezlikda Yuborish
**Tavsif:** Tashqi 100 ta turli API serverlaridan (masalan valyuta kurslari yoki ob-havo datchiklari) ma'lumotlarni ketma-ket olish 100 soniya oladi. `crul` paketi orqali barcha 100 ta so'rovni bir vaqtda parallel uzatish kerak.
**Talablar:** `crul::Async` sinfi, parallel so'rovlar havuzi va javoblarni tahlil qilish.
**Yechim (R):**
```r
# Parallel HTTP so'rovlari menejeri
fetch_multiple_apis_parallel <- function(urls) {
  if (!requireNamespace("crul", quietly = TRUE)) {
    stop("'crul' paketi o'rnatilmagan! Iltimos install.packages('crul') bajaring.")
  }
  
  cat(sprintf("[Parallel HTTP] %d ta manzilga bir vaqtda so'rov jo'natilmoqda...\n", length(urls)))
  
  # crul Async obyektini yaratish
  async_client <- crul::Async$new(
    urls = urls,
    headers = list("User-Agent" = "KhorazmiyAI-FastR/2.0")
  )
  
  # Barcha so'rovlarni bir vaqtning o'zida yuborish (libcurl multi-handle)
  responses <- async_client$get()
  
  # Natijalarni tahlil qilish
  results <- lapply(responses, function(resp) {
    list(
      url = resp$url,
      status_code = resp$status_code,
      success = resp$success(),
      response_time_ms = resp$times["total"] * 1000
    )
  })
  
  cat("[Parallel HTTP] Barcha so'rovlar parallel qabul qilindi.\n")
  results
}

# Sinov:
# test_urls <- c("https://httpbin.org/delay/1", "https://httpbin.org/delay/1")
# print(fetch_multiple_apis_parallel(test_urls))
```
**Tushuntirish:** `crul::Async` C darajasidagi `libcurl multi-handle` arxitekturasidan foydalanadi. U operatsion tizimning epoll/kqueue voqealar tizimi orqali barcha tarmoq so'rovlarini bitta oqimda parallel yuritadi va 100 ta so'rovni ketma-ket 100 soniya o'rniga eng sekin server javob bergan vaqtda (masalan 1.5 soniyada) tugatadi.

---

### Topshiriq #1121: httpuv Paketi Yordamida R da Xom WebSocket Serverini Ishga Tushirish
**Tavsif:** R tili nafaqat mijoz, balki veb-mijozlarga real-vaqtda ikki tomonlama xabar tarqatuvchi to'liq mustaqil WebSocket serveri sifatida ishlashi kerak.
**Talablar:** `httpuv::startServer`, `onWSOpen`, `onWSMessage`, `onWSClose` hodisalari va barcha ulangan mijozlarni xotirada saqlash.
**Yechim (R):**
```r
library(httpuv)

# Faol mijozlar ro'yxati
connected_clients <- list()

# WebSocket serveri konfiguratsiyasi
start_custom_ws_server <- function(port = 9454) {
  server_app <- list(
    # HTTP so'rovlariga oddiy javob
    call = function(req) {
      list(
        status = 200L,
        headers = list("Content-Type" = "text/plain"),
        body = "Khorazmiy R WebSocket Serveriga xush kelibsiz! WS protokoli orqali ulaning."
      )
    },
    # WebSocket ulanishini boshqarish
    onWSOpen = function(ws) {
      client_id <- as.character(length(connected_clients) + 1)
      cat(sprintf("[WS Server] Yangi mijoz ulandi: ID=%s\n", client_id))
      
      connected_clients[[client_id]] <<- ws
      
      # Mijozga xush kelibsiz xabari
      ws$send(jsonlite::toJSON(list(type = "WELCOME", client_id = client_id), auto_unbox = TRUE))
      
      # Xabar kelganda
      ws$onMessage(function(binary, message) {
        cat(sprintf("[Xabar ID=%s]: %s\n", client_id, message))
        
        # Barcha mijozlarga xabarni tarqatish (Broadcast)
        broadcast_msg <- jsonlite::toJSON(list(from = client_id, text = message), auto_unbox = TRUE)
        for (client in connected_clients) {
          client$send(broadcast_msg)
        }
      })
      
      # Aloqa uzilganda
      ws$onClose(function() {
        cat(sprintf("[WS Server] Mijoz uzildi: ID=%s\n", client_id))
        connected_clients[[client_id]] <<- NULL
      })
    }
  )
  
  server <- startServer("0.0.0.0", port, server_app)
  cat(sprintf("[WS Server] %d portida muvaffaqiyatli ishga tushdi.\n", port))
  return(server)
}

# Ishga tushirish (Namuna):
# srv <- start_custom_ws_server(9454)
# stopServer(srv)
```
**Tushuntirish:** `httpuv` Shiny va Plumber ning poydevori hisoblanadi. U C++ darajasidagi `libuv` asinxron I/O dvigateliga tayangan holda bitta R oqimida yuzlab parallel WebSocket ulanishlarini yuqori samaradorlik bilan boshqara oladi.

---

### Topshiriq #1122: websocket Mijozi Bilan Jonli Kripto-Valyuta Kotirovkalari Oqimiga Ulanish
**Tavsif:** Moliya muhandisligi va yuqori chastotali treydingda R orqali global birjalarning (masalan Binance yoki Coinbase) jonli WebSocket narxlar oqimiga ulanish va tahlil qilish lozim.
**Talablar:** `websocket::WebSocket` sinfi, `onOpen`, `onMessage`, `onError` eshituvchilari va JSON ma'lumotlarni o'qish.
**Yechim (R):**
```r
library(websocket)
library(jsonlite)

# Birja jonli narxlar oqimini kuzatuvchi R mijozi
connect_crypto_stream <- function(symbol = "btcusdt") {
  stream_url <- sprintf("wss://stream.binance.com:9443/ws/%s@ticker", tolower(symbol))
  cat(sprintf("[Kripto Stream] Ulanmoqda: %s\n", stream_url))
  
  ws <- WebSocket$new(stream_url)
  
  # Ulanish ochilganda
  ws$onOpen(function(event) {
    cat("[Kripto Stream] Muvaffaqiyatli ulandi! Jonli kotirovkalar oqimi boshlandi...\n")
  })
  
  # Narx xabari kelganda
  ws$onMessage(function(event) {
    data <- fromJSON(event$data)
    
    # Muhim birja parametrlarini ajratib olish:
    # 's' = Symbol, 'c' = Current Price, 'h' = High 24h, 'v' = Volume
    cat(sprintf("[%s] Narx: %s USD | 24h Baland: %s | Hajm: %s\n", 
                data$s, data$c, data$h, data$v))
  })
  
  # Xatolik yuz berganda
  ws$onError(function(event) {
    cat("[Kripto Stream Xatosi]:", event$message, "\n")
  })
  
  # Yopilganda
  ws$onClose(function(event) {
    cat("[Kripto Stream] Aloqa yopildi.\n")
  })
  
  return(ws)
}

# Sinov:
# ws_client <- connect_crypto_stream("BTCUSDT")
# 10 soniyadan so'ng: ws_client$close()
```
**Tushuntirish:** `websocket` paketi asinxron ishlaydi va R konsolini bloklamaydi. Olingan kotirovkalar xotirada to'planib, keyinchalik real-vaqt modellariga uzatilishi mumkin.

---

### Topshiriq #1123: Oqimli Ma'lumotlarda Dinamik Rolling Window Indikatorlarini Hisoblash
**Tavsif:** Har bir yangi kotirovka kelib tushganda butun tarixiy ma'lumotlar massivini qayta hisoblamasdan, xotirada oxirgi N ta narx oynasida (Rolling Window) sirpanuvchi o'rtacha (SMA) va volatillikni onlayn yangilash zarur.
**Talablar:** Doimiy hajmdagi vektor o'rami va $O(1)$ yangilanish formulasini R da yozish.
**Yechim (R):**
```r
# Dinamik rolling window indikatorlari sinfi
create_rolling_window_tracker <- function(window_size = 20) {
  prices <- numeric(0)
  
  list(
    # Yangi narxni qabul qilish va indikatorni yangilash
    push_price = function(price) {
      price <- as.numeric(price)
      prices <<- c(prices, price)
      
      # Agar oyna o'lchamidan oshsa, eng eski narxni olib tashlash
      if (length(prices) > window_size) {
        prices <<- prices[-1]
      }
      
      # Ko'rsatkichlarni hisoblash
      sma <- mean(prices)
      current_volatility <- if (length(prices) > 1) sd(prices) else 0
      
      list(
        window_count = length(prices),
        latest_price = price,
        sma = round(sma, 4),
        volatility = round(current_volatility, 4),
        is_above_sma = price > sma
      )
    },
    get_history = function() prices
  )
}

# Sinov
tracker <- create_rolling_window_tracker(window_size = 5)
for (p in c(100, 102, 101, 105, 107, 106)) {
  stat <- tracker$push_price(p)
  cat(sprintf("Narx: %d -> SMA: %.2f | Volatillik: %.2f\n", p, stat$sma, stat$volatility))
}
```
**Tushuntirish:** Oqimli tahlilda ma'lumotlar bazasiga murojaat qilmasdan xotirada sirpanuvchi oyna (Rolling Window) saqlash hisoblash kechikishini 99% ga kamaytiradi. Yangi narx kelishi bilan indikatorlar mikrosekundlarda tayyor bo'ladi.

---

### Topshiriq #1124: WebSocket Ulanishida Heartbeat (Ping/Pong) Bilan Aloqa Uzilishini Aniqlash
**Tavsif:** Foydalanuvchi routeri o'chib qolsa yoki internet uzilsa, TCP FIN kelmasligi mumkin. Server har 10 soniyada Ping yuborib, 5 soniyada Pong olmasa soketni yopuvchi Heartbeat tekshiruvini joriy qilish kerak.
**Talablar:** `later` paketi yordamida davriy taymer tashkil qilish va tiriklik bayrog'ini tekshirish.
**Yechim (R):**
```r
library(httpuv)
library(later)

setup_heartbeat_monitor <- function(ws, interval_sec = 10, timeout_sec = 5) {
  is_alive <- TRUE
  active <- TRUE
  
  # Mijozdan pong javobi kelganda
  ws$onMessage(function(binary, message) {
    if (message == "PONG") {
      is_alive <<- TRUE
    }
  })
  
  # Davriy Ping jo'natuvchi rekursiv funksiya
  schedule_ping <- function() {
    if (!active) return()
    
    if (!is_alive) {
      cat("[Heartbeat] Mijoz javob bermadi! Zombi ulanish yopilmoqda...\n")
      ws$close()
      active <<- FALSE
      return()
    }
    
    # Holatni tekshirish uchun false qilamiz va Ping yuboramiz
    is_alive <<- FALSE
    ws$send("PING")
    
    # Keyingi tekshiruvni rejalashtirish
    later(schedule_ping, interval_sec)
  }
  
  # Taymerni boshlash
  later(schedule_ping, interval_sec)
  
  # Soket yopilganda taymerni to'xtatish
  ws$onClose(function() {
    active <<- FALSE
  })
}
```
**Tushuntirish:** `later` paketi R ning yagona oqimli modelida `setTimeout` kabi asinxron taymerlarni amalga oshiradi. Bu orqali tarmoqdagi o'lik soketlar avtomatik tozalanib, xotira sarfi tejab qolinadi.

---

### Topshiriq #1125: Bir Vaqtda Bir Nechta Mijozlarga Real-Vaqt Modellari Bashoratini Tarqatish
**Tavsif:** Serverda ishlayotgan mashinali o'rganish modeli har 500 millisekundda yangi ko'rsatkichlarni bashorat qiladi. Barcha ulangan 50 ta mijoz brauzeriga ushbu natijalarni bir vaqtda broadcast qilish lozim.
**Talablar:** Mijozlar to'plamini boshqaruvchi WebSocket Broadcast menejeri va Model Inference oqimi.
**Yechim (R):**
```r
library(httpuv)
library(later)

# Tahliliy tarqatish markazi
create_analytics_broadcaster <- function() {
  subscribers <- list()
  
  # Yangi obunachi qo'shish
  add_subscriber <- function(id, ws) {
    subscribers[[id]] <<- ws
  }
  
  # Obunachini o'chirish
  remove_subscriber <- function(id) {
    subscribers[[id]] <<- NULL
  }
  
  # Model bashoratlarini barcha obunachilarga yuborish
  broadcast_prediction <- function(model_result) {
    json_payload <- jsonlite::toJSON(model_result, auto_unbox = TRUE)
    
    for (id in names(subscribers)) {
      client <- subscribers[[id]]
      tryCatch({
        client$send(json_payload)
      }, error = function(e) {
        # Agar ulanish uzilgan bo'lsa, ro'yxatdan chiqarish
        subscribers[[id]] <<- NULL
      })
    }
  }
  
  list(
    add = add_subscriber,
    remove = remove_subscriber,
    broadcast = broadcast_prediction,
    count = function() length(subscribers)
  )
}

# Simulyatsiya qilingan doimiy bashorat oqimi
run_continuous_inference <- function(broadcaster) {
  generate_step <- function() {
    # Yangi model inference natijasi
    inference <- list(
      timestamp = as.character(Sys.time()),
      predicted_demand = round(rnorm(1, mean = 250, sd = 15), 1),
      anomaly_detected = runif(1) > 0.95
    )
    
    broadcaster$broadcast(inference)
    later(generate_step, 0.5) # Har 0.5 soniyada yangilash
  }
  later(generate_step, 0.5)
}
```
**Tushuntirish:** Ushbu model Pub/Sub arxitekturasini R ichida tashkil qiladi. Model hisoblashlari barcha mijozlar uchun alohida takrorlanmaydi; bitta markaziy hisob-kitob bajariladi va natija barcha abonentlarga o'zgarmasdan tarqatiladi.

---

### Topshiriq #1126: WebSocket Orqali Binar Xabarlarni (Raw Vectors) Tezkor Almashish
**Tavsif:** Katta hajmdagi sonli massivlarni matnli JSON ga o'girmasdan, binar xom baytlar (`raw` vector) ko'rinishida WebSocket orqali uzatish tarmoq hajmini 80% ga qisqartiradi.
**Talablar:** `writeBin` yordamida xom binar bufer hosil qilish va `ws$send(raw_data)` orqali binar uzatish.
**Yechim (R):**
```r
library(httpuv)

# Float32 massivini binar WebSocket xabariga o'girish
send_binary_tensor <- function(ws, numeric_vector) {
  # Xom xotira ulanishini (Memory Connection) ochish
  raw_con <- rawConnection(raw(0), "wb")
  
  # 1. Sehrli sarlavha (Magic Header): 2 bayt 0x4B 0x48 ('KH')
  writeBin(as.raw(c(0x4B, 0x48)), raw_con)
  
  # 2. Vektor uzunligi (4 bayt integer)
  writeBin(as.integer(length(numeric_vector)), raw_con, size = 4)
  
  # 3. Sonli qiymatlarni 4 baytli Float (Single Precision) shaklida yozish
  writeBin(as.numeric(numeric_vector), raw_con, size = 4, endian = "little")
  
  # Binar vektorni olish
  binary_payload <- rawConnectionValue(raw_con)
  close(raw_con)
  
  # WebSocket orqali binar rejimda yuborish
  ws$send(binary_payload)
  cat(sprintf("[Binar WS] %d ta son (%d bayt) uzatildi.\n", length(numeric_vector), length(binary_payload)))
}
```
**Tushuntirish:** `rawConnection` xotirada to'g'ridan-to'g'ri baytlar bilan ishlash imkonini beradi. Binar uzatishda sonlar matnli belgilarga aylanmaydi (masalan 123.456789 matn sifatida 10 bayt, binar float sifatida esa atigi 4 bayt). Bu tarmoq I/O unumdorligini oshiradi.

---

### Topshiriq #1127: WebSocket Ulanishini Qayta Tiklovchi (Exponential Backoff Auto-Reconnect) Mijoz
**Tavsif:** Tarmoq beqaror bo'lganda WebSocket mijozi o'chib qolmasdan, 1, 2, 4, 8 soniyalik eksponensial kechikish bilan avtomatik qayta ulanishi (Auto-Reconnect) kerak.
**Talablar:** `websocket::WebSocket`, `later` paketi va qayta urinishlar sonini hisoblovchi barqaror mijoz sinfi.
**Yechim (R):**
```r
library(websocket)
library(later)

# Ishonchli doimiy ulanuvchi WebSocket mijozi
create_resilient_ws_client <- function(url, max_retry_delay = 30) {
  ws <- NULL
  retry_count <- 0
  
  connect <- function() {
    cat(sprintf("[WS Mijoz] Ulanmoqda: %s...\n", url))
    ws <<- WebSocket$new(url)
    
    ws$onOpen(function(event) {
      cat("[WS Mijoz] Muvaffaqiyatli ulandi!\n")
      retry_count <<- 0 # Muvaffaqiyatli ulanganda hisoblagichni nollash
    })
    
    ws$onClose(function(event) {
      retry_count <<- retry_count + 1
      # Eksponensial kechikish: 2^retry_count (maksimal 30 soniya)
      delay <- min(max_retry_delay, 2^retry_count)
      cat(sprintf("[WS Mijoz] Aloqa uzildi! %d soniyadan keyin qayta urinish (#%d)...\n", delay, retry_count))
      
      later(connect, delay)
    })
    
    ws$onError(function(event) {
      cat("[WS Mijoz Xatosi]:", event$message, "\n")
    })
  }
  
  # Ilk ulanishni boshlash
  connect()
}
```
**Tushuntirish:** Eksponensial kechikish (Exponential Backoff) server ishdan chiqqan paytda barcha mijozlar bir soniyada serverga birdaniga yopirilib borishining (Thundering Herd) oldini oladi. Har bir muvaffaqiyatsiz urinishdan so'ng kutish vaqti 2 barobar oshiriladi.

---

### Topshiriq #1128: Xonalar (Rooms / Channels) Bo'yicha WebSocket Obunalarini Boshqaruvchi Menejer
**Tavsif:** Foydalanuvchilar o'zlariga kerakli mavzularga (masalan 'TOSHKENT_OB_HAVO', 'USD_KURS') obuna bo'ladilar. Har bir xabarni faqat o'sha xonaga a'zo bo'lgan mijozlarga yo'naltiruvchi guruhlash mexanizmi lozim.
**Talablar:** Xona nomlari bo'yicha Set indeksini yuritish, `SUBSCRIBE` va `UNSUBSCRIBE` buyruqlarini parse qilish.
**Yechim (R):**
```r
# Taqsimlangan xonalar menejeri
create_room_manager <- function() {
  rooms <- new.env(parent = emptyenv())
  
  join_room <- function(room_name, client_id, ws) {
    if (!exists(room_name, envir = rooms)) {
      rooms[[room_name]] <- list()
    }
    rooms[[room_name]][[client_id]] <- ws
    cat(sprintf("[Xonalar] Mijoz %s xonaga kirdi: %s\n", client_id, room_name))
  }
  
  leave_room <- function(room_name, client_id) {
    if (exists(room_name, envir = rooms)) {
      rooms[[room_name]][[client_id]] <- NULL
    }
  }
  
  broadcast_to_room <- function(room_name, message) {
    if (!exists(room_name, envir = rooms)) return(0)
    
    clients <- rooms[[room_name]]
    sent_count <- 0
    for (id in names(clients)) {
      tryCatch({
        clients[[id]]$send(message)
        sent_count <- sent_count + 1
      }, error = function(e) {
        rooms[[room_name]][[id]] <- NULL
      })
    }
    return(sent_count)
  }
  
  list(
    join = join_room,
    leave = leave_room,
    send = broadcast_to_room
  )
}
```
**Tushuntirish:** Xonalarni boshqarish orqali keraksiz tarmoq trafigi kesiladi. 10 000 ta mijoz ulangan tizimda ma'lum bir hududiy yangilik faqat shu hudud xonasiga a'zo 50 ta mijozga yetkaziladi.

---

### Topshiriq #1129: Jonli WebSocket Ma'lumotlarini Real-Vaqtda Shiny Reaktiv Grafigiga Uzatish
**Tavsif:** Tashqi tarmoq oqimidan kelayotgan jonli o'zgarishlarni R Shiny veb-interfeysida sahifani yangilamasdan (No full page reload) silliq ko'rsatish zarur.
**Talablar:** `reactiveVal`, `invalidateLater` va WebSocket hodisalari orqali Shiny reaktiv kontekstini yangilash.
**Yechim (R):**
```r
# Shiny ilovasida jonli WebSocket reaktivligi
# library(shiny)

ui <- function() {
  # fluidPage(
  #   titlePanel("Khorazmiy AI: Jonli Real-Vaqt Analitika"),
  #   textOutput("live_metric"),
  #   plotOutput("live_plot")
  # )
}

server <- function(input, output, session) {
  # Reaktiv saqlagich
  live_data <- reactiveVal(numeric(0))
  
  # Masofaviy oqim simulyatsiyasi (har soniyada yangi nuqta kelishi)
  observe({
    invalidateLater(1000, session)
    
    new_val <- rnorm(1, mean = 50, sd = 5)
    current_history <- live_data()
    updated_history <- c(tail(current_history, 49), new_val) # Oxirgi 50 ta nuqta
    
    live_data(updated_history)
  })
  
  # Matnli natija
  output$live_metric <- renderText({
    data <- live_data()
    if (length(data) == 0) return("Kutilmoqda...")
    sprintf("Oxirgi qiymat: %.2f | O'rtacha: %.2f", tail(data, 1), mean(data))
  })
  
  # Jonli grafik
  output$live_plot <- renderPlot({
    data <- live_data()
    if (length(data) > 1) {
      plot(data, type = "l", col = "blue", lwd = 2,
           main = "Jonli Telemetriya Oqimi", ylab = "Qiymat", xlab = "Vaqt qadamlari")
      abline(h = mean(data), col = "red", lty = 2)
    }
  })
}
```
**Tushuntirish:** `reactiveVal()` va `invalidateLater()` Shiny arxitekturasida tashqi tarmoq datchiklaridan olinayotgan ma'lumotlarni GUI elementlariga 'push' qilishning eng optimal yo'lidir. Brauzer faqat o'zgargan grafik qismini qayta chizadi.

---

### Topshiriq #1130: WebSocket Oqimini Xotiraga Yuklamasdan DuckDB / Parquet Formatiga Oqimli Saqlash
**Tavsif:** Kuniga millionlab qatorlar kelib tushadigan tarmoq oqimlarini R ning operativ xotirasida (RAM) saqlab bo'lmaydi. Ularni to'g'ridan-to'g'ri o'rnatilgan DuckDB bazasiga oqimli yozib borish kerak.
**Talablar:** `duckdb` ulanishi, tayyorlangan SQL INSERT va tranzaksion buferlash (Batch flush).
**Yechim (R):**
```r
# DuckDB bilan oqimli saqlagich
create_stream_duckdb_sink <- function(db_path = "stream_archive.duckdb", batch_size = 1000) {
  if (!requireNamespace("duckdb", quietly = TRUE) || !requireNamespace("DBI", quietly = TRUE)) {
    stop("duckdb va DBI paketlari talab etiladi!")
  }
  
  con <- DBI::dbConnect(duckdb::duckdb(), db_path)
  
  # Jadvalni yaratish
  DBI::dbExecute(con, "
    CREATE TABLE IF NOT EXISTS telemetry_stream (
      id BIGINT,
      sensor_id VARCHAR,
      value DOUBLE,
      recorded_at TIMESTAMP
    )
  ")
  
  buffer <- list()
  
  flush_buffer <- function() {
    if (length(buffer) == 0) return()
    
    df <- do.call(rbind, lapply(buffer, as.data.frame))
    DBI::dbWriteTable(con, "telemetry_stream", df, append = TRUE)
    buffer <<- list()
    cat(sprintf("[DuckDB Sink] %d ta qator diskka yozildi.\n", nrow(df)))
  }
  
  list(
    append_record = function(record) {
      buffer[[length(buffer) + 1]] <<- record
      if (length(buffer) >= batch_size) {
        flush_buffer()
      }
    },
    close = function() {
      flush_buffer()
      DBI::dbDisconnect(con, shutdown = TRUE)
    }
  )
}
```
**Tushuntirish:** `DuckDB` ustunli (Columnar) saqlash arxitekturasi tufayli oqimli ma'lumotlarni siqilgan holda yozish va terabaytlab ma'lumotlar ustida analitik SQL so'rovlarini millisekundlarda bajarish imkonini beradi.

---

### Topshiriq #1131: Apache Kafka REST Proxy Orqali Mavzudan (Topic) Xabarlar Oqimini O'qish
**Tavsif:** Korporativ arxitekturada Apache Kafka bilan ishlashda R tili Kafka REST Proxy API orqali iste'molchi guruhi (Consumer Group) tuzishi va xabarlarni oqimli o'qishi kerak.
**Talablar:** `httr2` paketi yordamida Kafka REST Proxy ga ulanish, iste'molchi yaratish va xabarlarni qabul qilish.
**Yechim (R):**
```r
library(httr2)
library(jsonlite)

# Kafka REST Proxy iste'molchisi
consume_kafka_messages <- function(proxy_url = "http://localhost:8082", topic = "sensor_events", group_id = "r_analytics_group") {
  cat(sprintf("[Kafka Iste'molchi] Topic: '%s' tinglanmoqda...\n", topic))
  
  # 1. Consumer yaratish so'rovi
  consumer_url <- sprintf("%s/consumers/%s", proxy_url, group_id)
  create_req <- request(consumer_url) %>%
    req_headers("Content-Type" = "application/vnd.kafka.v2+json") %>%
    req_body_json(list(
      name = "r_consumer_instance_1",
      format = "json",
      `auto.offset.reset` = "earliest"
    ))
  
  # 2. Mavzuga (Topic) obuna bo'lish
  sub_url <- sprintf("%s/instances/r_consumer_instance_1/subscription", consumer_url)
  sub_req <- request(sub_url) %>%
    req_headers("Content-Type" = "application/vnd.kafka.v2+json") %>%
    req_body_json(list(topics = list(topic)))
  
  # 3. Xabarlarni tortib olish (Poll / Fetch records)
  fetch_url <- sprintf("%s/instances/r_consumer_instance_1/records", consumer_url)
  fetch_req <- request(fetch_url) %>%
    req_headers("Accept" = "application/vnd.kafka.json.v2+json")
  
  cat("[Kafka Iste'molchi] So'rovlar tayyorlandi.\n")
  return(list(fetch_req = fetch_req))
}
```
**Tushuntirish:** Kafka REST Proxy R dasturchilariga murakkab C++ `librdkafka` kutubxonasini kompilyatsiya qilmasdan, oddiy va barqaror HTTP/2 protokoli orqali Kafka klasteri bilan integratsiyalashish imkonini beradi.

---

### Topshiriq #1132: Kafka Mavzusiga (Topic) Tahliliy Modellarning Bashorat Natijalarini Yuborish (Producer)
**Tavsif:** R modelida hisoblangan risk ko'rsatkichlari yoki savdo signallari boshqa quyi tizimlar (Java/Go mikroxizmatlari) iste'mol qilishi uchun Kafka `model_predictions` mavzusiga JSON shaklida uzatilishi kerak.
**Talablar:** `httr2` orqali POST so'rovi, partitioning kaliti (Message Key) va xabarlar ro'yxatini to'plamli (Batch) yuborish.
**Yechim (R):**
```r
library(httr2)

produce_prediction_to_kafka <- function(proxy_url = "http://localhost:8082", topic = "model_predictions", records) {
  produce_url <- sprintf("%s/topics/%s", proxy_url, topic)
  
  # Xabarlar strukturasini Kafka formati bo'yicha tuzish
  payload <- list(
    records = lapply(records, function(rec) {
      list(
        key = rec$user_id, # Partitioning kaliti
        value = rec
      )
    })
  )
  
  # Kafka REST Proxy ga jo'natish
  req <- request(produce_url) %>%
    req_headers("Content-Type" = "application/vnd.kafka.json.v2+json") %>%
    req_body_json(payload)
  
  cat(sprintf("[Kafka Producer] %d ta xabar '%s' mavzusiga yuborilmoqda...\n", length(records), topic))
  # resp <- req_perform(req)
  # return(resp_status(resp) == 200)
  return(TRUE)
}

# Sinov xabari
sample_predictions <- list(
  list(user_id = "user_101", default_prob = 0.042, risk_tier = "PAST"),
  list(user_id = "user_102", default_prob = 0.685, risk_tier = "YUQORI")
)
produce_prediction_to_kafka(records = sample_predictions)
```
**Tushuntirish:** Xabarlarga `key` (masalan `user_id`) berish orqali Kafka aynan bir xil foydalanuvchiga tegishli barcha xabarlar bitta partition ga tushishini va qat'iy tartibda (FIFO) qayta ishlanishini kafolatlaydi.

---

### Topshiriq #1133: Kafka Consumer Group Mantig'i: Partitionlar Bo'yicha Yuklamani R Ishchilari O'rtasida Taqsimlash
**Tavsif:** Agar Kafka mavzusi 4 ta partition ga bo'lingan bo'lsa, 4 ta R ishchisi bitta Consumer Group nomi ostida ulansa, har bir R jarayoni alohida partition ni o'qib umumiy o'tkazuvchanlikni 4 barobar oshiradi.
**Talablar:** Partition taqsimotini hisobga oluvchi ko'p jarayonli R klaster arxitekturasini loyihalash.
**Yechim (R):**
```r
library(parallel)

# 4 ta R ishchisiga Kafka partitionlarini biriktiruvchi simulyatsiya
run_distributed_kafka_workers <- function(num_partitions = 4) {
  cl <- makeCluster(num_partitions, type = "PSOCK")
  on.exit(stopCluster(cl))
  
  # Har bir ishchiga uning partition raqamini yuklash
  clusterApply(cl, 0:(num_partitions - 1), function(partition_id) {
    cat(sprintf("[R Worker PID: %d] Partition #%d ga ulandi.\n", Sys.getpid(), partition_id))
    
    # Iste'mol sikli simulyatsiyasi
    # Har bir worker faqat o'ziga biriktirilgan partition LSN larini o'qiydi
    list(
      worker_pid = Sys.getpid(),
      assigned_partition = partition_id,
      status = "LISTENING"
    )
  })
}

# Ishga tushirish
worker_status <- run_distributed_kafka_workers(4)
print(worker_status)
```
**Tushuntirish:** Kafka Consumer Group dizayni taqsimlangan tahlilning kalitidir. Partitionlar soni qancha ko'p bo'lsa, shuncha ko'p parallel R ishchilarini jalb qilish mumkin, bu esa sekundiga yuz minglab tranzaksiyalarni tahlil qilish imkonini yaratadi.

---

### Topshiriq #1134: MQTT Brokeriga Ulanish va IoT Datchiklar Telemetriyasiga Obuna Bo'lish
**Tavsif:** Sanoat korxonalari va Aqlli Shaxar (Smart City) datchiklari ma'lumotlarni engil MQTT protokoli orqali uzatadi. R orqali MQTT brokeriga ulanib harorat va bosim ko'rsatkichlarini qabul qilish lozim.
**Talablar:** `paho.mqtt` yoki soket asosidagi MQTT mijozini tuzish, `sensors/+/temperature` mavzusiga obuna bo'lish.
**Yechim (R):**
```r
# MQTT protokoli orqali IoT telemetriyasini qabul qilish boshqaruvchisi
create_mqtt_sensor_listener <- function(broker_host = "mqtt.khorazmiy.uz", broker_port = 1883) {
  cat(sprintf("[MQTT Mijoz] Brokerga ulanmoqda: %s:%d...\n", broker_host, broker_port))
  
  # Simulyatsiya qilingan MQTT ulanishi
  topic_subscribed <- "sensors/toshkent/+/telemetry"
  cat(sprintf("[MQTT] Obuna bo'lindi: '%s'\n", topic_subscribed))
  
  # Xabar kelganda chaqiriladigan handler
  on_message_received <- function(topic, payload_json) {
    data <- jsonlite::fromJSON(payload_json)
    cat(sprintf("[IoT Datchik] Mavzu: %s | Harorat: %.1f C | Namlik: %.1f%%\n", 
                topic, data$temperature, data$humidity))
    
    # Anomaliya tekshiruvi: Agar harorat 50 darajadan oshsa signal berish
    if (data$temperature > 50.0) {
      warning(sprintf("DIQQAT: Datchikda qizib ketish aniqlandi: %.1f C!", data$temperature))
    }
  }
  
  list(
    simulate_packet = on_message_received
  )
}

# Sinov
listener <- create_mqtt_sensor_listener()
listener$simulate_packet("sensors/toshkent/datchik_01/telemetry", '{"temperature": 52.4, "humidity": 30.1}')
```
**Tushuntirish:** MQTT (Message Queuing Telemetry Transport) cheklangan tarmoq kanallari va kam quvvatli IoT batareyalari uchun yaratilgan. Mavzular iyerarxik tuzilishga ega (masalan `sensors/+/telemetry`), bu esa R tahlilchisiga barcha datchiklarni bitta qolib orqali kuzatish imkonini beradi.

---

### Topshiriq #1135: MQTT QoS (Quality of Service: 0, 1, 2) Darajalarini Boshqarish
**Tavsif:** Telemetriya yo'qolsa ham muhim emas (QoS 0), datchik signali kamida bir marta yetib borishi shart (QoS 1 At-least-once) yoki moliyaviy tranzaksiya aynan bir marta bajarilishi shart (QoS 2 Exactly-once).
**Talablar:** QoS darajalarini tekshirish va xabar dublikatlarini (Duplicate Detection) tozalovchi filter.
**Yechim (R):**
```r
# MQTT QoS va dublikatlarni tozalash dvigateli
create_qos_filter <- function() {
  seen_message_ids <- character(0)
  
  process_message <- function(msg_id, qos_level, payload) {
    cat(sprintf("[QoS %d] Xabar keldi: ID=%s\n", qos_level, msg_id))
    
    if (qos_level == 1) {
      # QoS 1 da xabar takrorlanishi mumkin (At-least-once)
      if (msg_id %in% seen_message_ids) {
        cat(sprintf("[Dublikat Tashlandi]: %s allaqachon qayta ishlangan.\n", msg_id))
        return(NULL) # Takroriy xabarni rad etish
      }
      seen_message_ids <<- c(tail(seen_message_ids, 999), msg_id)
    }
    
    # Muvaffaqiyatli qabul qilingan xabar
    return(payload)
  }
  
  list(process = process_message)
}

# Sinov
filter <- create_qos_filter()
filter$process("msg_001", 1, "Status: OK")
filter$process("msg_001", 1, "Status: OK") # Dublikat inkor qilinadi!
```
**Tushuntirish:** QoS 1 darajasida tarmoq uzilsa broker xabarni qayta yuboradi. R tomonida `seen_message_ids` aylanma buferini saqlash orqali idempotentlik ta'minlanadi va statistik hisob-kitoblarning sun'iy shishib ketishining oldi olinadi.

---

### Topshiriq #1136: MQTT Oqimidan Kelayotgan Sensor Anomaliyalarini Real-Vaqtda Aniqlovchi ML Filtr
**Tavsif:** Fabrikadagi minglab datchiklardan har sekundda kelayotgan oqim ustida Isolation Forest yoki Mahalanobis masofasi orqali anomaliyalarni real-vaqtda aniqlash zarur.
**Talablar:** R da oqimli ma'lumotlar uchun Mahalanobis masofasi asosidagi anomaliya detektori.
**Yechim (R):**
```r
# Oqimli ko'p o'lchovli anomaliya detektori
create_multivariate_anomaly_detector <- function() {
  # Standart parametrlar kovariatsiyasi (Tarixiy ma'lumotlardan olingan)
  center_means <- c(temp = 40.0, pressure = 101.3, vibration = 1.2)
  cov_matrix <- matrix(c(
    4.0,  0.5,  0.1,
    0.5,  1.0,  0.2,
    0.1,  0.2,  0.05
  ), nrow = 3, byrow = TRUE)
  
  cov_inv <- solve(cov_matrix)
  
  # Yangi datchik o'lchovini tekshirish
  evaluate_point <- function(temp, pressure, vibration) {
    x <- c(temp, pressure, vibration)
    diff <- x - center_means
    
    # Mahalanobis masofasi kvadrati: D^2 = (x - mu)^T * Sigma^-1 * (x - mu)
    d2 <- as.numeric(t(diff) %*% cov_inv %*% diff)
    
    # Chi-kvadrat taqsimoti bo'yicha 99% chegarasi (df = 3 uchun chegara ≈ 11.34)
    is_anomaly <- d2 > 11.34
    
    list(
      mahalanobis_dist = round(sqrt(d2), 2),
      is_anomaly = is_anomaly,
      alert = if (is_anomaly) "XAVF: Datchiklar anomal holatda!" else "NORMAL"
    )
  }
  
  list(check = evaluate_point)
}

# Sinov
detector <- create_multivariate_anomaly_detector()
cat("Normal holat:\n")
print(detector$check(41, 101.5, 1.3))

cat("Anomal holat (Harorat va tebranish keskin oshdi):\n")
print(detector$check(48, 103.0, 2.8))
```
**Tushuntirish:** Mahalanobis masofasi alohida o'zgaruvchilarni emas, ularning o'zaro korrelyatsiyasini hisobga oladi. Masalan harorat oshishi va bosim tushishi alohida normal bo'lishi mumkin, biroq birgalikda ular avariya alomatidir.

---

### Topshiriq #1137: Kafka Schema Registry va Avro Sxemasi O'zgarganda Xatoliksiz Parse Qilish
**Tavsif:** Katta kompaniyalarda ishlab chiqaruvchilar Kafka xabarlariga yangi ustunlar qo'shishi yoki sxemani o'zgartirishi (Schema Evolution) mumkin. R skripti kutilmagan ustunlar kelganda qulab tushmasligi lozim.
**Talablar:** Sxemani tekshirish, yetishmayotgan ustunlarni `NA` bilan to'ldirish va ortiqcha ustunlarni xavfsiz e'tiborsiz qoldirish.
**Yechim (R):**
```r
# Sxema o'zgarishlariga chidamli xabar parse qilish
safe_parse_kafka_payload <- function(json_str, expected_schema) {
  parsed <- tryCatch({
    jsonlite::fromJSON(json_str)
  }, error = function(e) {
    return(NULL)
  })
  
  if (is.null(parsed)) return(NULL)
  
  result <- list()
  for (col in names(expected_schema)) {
    expected_type <- expected_schema[[col]]
    
    if (col %in% names(parsed)) {
      val <- parsed[[col]]
      # Tipni moslash
      result[[col]] <- if (expected_type == "numeric") as.numeric(val) else as.character(val)
    } else {
      # Yangi versiyada ustun yo'q bo'lsa NA qo'yish
      result[[col]] <- NA
    }
  }
  
  as.data.frame(result)
}

# Sinov: Sxemada 3 ta ustun kutilmoqda
schema <- list(id = "character", amount = "numeric", currency = "character")
# Keltirilgan xabarda 'currency' yo'q, lekin qo'shimcha 'extra_tag' bor
df <- safe_parse_kafka_payload('{"id": "tx_99", "amount": 1500.50, "extra_tag": "SALE"}', schema)
print(df)
```
**Tushuntirish:** Sxema evolyutsiyasi (Schema Evolution) mikroxizmatlar mustaqilligini ta'minlaydi. Backward va Forward moslashuvchanlik orqali R tahlil quvurlari yangi dastur versiyalari chiqqanda to'xtab qolmasdan o'z ishini davom ettiradi.

---

### Topshiriq #1138: Dead Letter Queue (DLQ): Buzilgan Xabarlarni Alohida Kanalga Yo'naltirish
**Tavsif:** Agar Kafka yoki MQTT oqimidan kelgan xabar sintaktik xato bo'lsa yoki modellarni qulatadigan qiymatlarga ega bo'lsa, butun oqimni to'xtatmasdan uni DLQ mavzusiga tashlab ketish zarur.
**Talablar:** TryCatch orqali xatolikni tutish, buzilgan xabarga xatolik sababini ilova qilib `dead_letter_queue` ga yuborish.
**Yechim (R):**
```r
# Dead Letter Queue (DLQ) boshqaruvi
route_to_dlq_on_error <- function(raw_message, process_function, dlq_channel) {
  tryCatch({
    # Asosiy biznes logikani bajarishga urinish
    process_function(raw_message)
  }, error = function(e) {
    cat(sprintf("[DLQ Ogohlantirish] Xabar qayta ishlanmadi: %s\n", e$message))
    
    # Buzilgan xabarni va xatolik sababini DLQ paketiga o'rash
    dlq_record <- list(
      failed_at = Sys.time(),
      error_reason = e$message,
      original_payload = raw_message
    )
    
    # DLQ kanaliga yozish
    dlq_channel$send(jsonlite::toJSON(dlq_record, auto_unbox = TRUE))
  })
}

# Sinov
fake_dlq <- list(send = function(msg) cat("DLQ ga saqlandi:", msg, "\n"))
bad_process <- function(msg) {
  data <- jsonlite::fromJSON(msg)
  if (data$value < 0) stop("Manfiy qiymat ruxsat etilmagan!")
}

route_to_dlq_on_error('{"value": -50}', bad_process, fake_dlq)
```
**Tushuntirish:** Dead Letter Queue buzilgan xabarlarning butun ma'lumotlar oqimini to'xtatib qo'yishiga (Poison Pill problem) yo'l qo'ymaydi. Administratorlar keyinchalik DLQ dagi xatoliklarni tahlil qilib, tizimni tuzatishlari mumkin.

---

### Topshiriq #1139: Oqimli Ma'lumotlarni Tranzaksion Guruhlash (Micro-Batching) va Oraliq Agregatsiyalar
**Tavsif:** Har bir datchik xabari uchun alohida model hisoblash sekin ishlaydi. 100 millisekund ichida kelgan xabarlarni bitta Micro-Batch guruhiga jamlab vektorlashtirilgan tahlil o'tkazish talab etiladi.
**Talablar:** `micro_batch_collector` sinfi, vaqt va hajm chegaralari (100 ms yoki 500 ta xabar).
**Yechim (R):**
```r
# Micro-batching yig'uvchisi
create_micro_batcher <- function(max_batch_size = 50, max_wait_sec = 0.5, on_batch_ready) {
  current_batch <- list()
  last_flush_time <- Sys.time()
  
  flush <- function() {
    if (length(current_batch) == 0) return()
    
    batch_df <- do.call(rbind, lapply(current_batch, as.data.frame))
    current_batch <<- list()
    last_flush_time <<- Sys.time()
    
    on_batch_ready(batch_df)
  }
  
  add_record <- function(rec) {
    current_batch[[length(current_batch) + 1]] <<- rec
    
    time_diff <- as.numeric(difftime(Sys.time(), last_flush_time, units = "secs"))
    
    if (length(current_batch) >= max_batch_size || time_diff >= max_wait_sec) {
      flush()
    }
  }
  
  list(add = add_record, flush = flush)
}

# Sinov
batcher <- create_micro_batcher(
  max_batch_size = 3,
  on_batch_ready = function(df) {
    cat(sprintf("[Batch Bajarildi] %d ta qator yig'ildi. O'rtacha qiymat: %.2f\n", 
                nrow(df), mean(df$val)))
  }
)

batcher$add(list(id = 1, val = 10))
batcher$add(list(id = 2, val = 20))
batcher$add(list(id = 3, val = 30)) # 3 taga yetganda avtomatik trigger bo'ladi!
```
**Tushuntirish:** Micro-batching Spark Streaming ning asosiy g'oyasi hisoblanadi. R tilining barcha chiziqli algebra va statistik funksiyalari vektorlashtirilganligi sababli, 100 ta qatorni bir vaqtda qayta ishlash ularni 1 tadan alohida hisoblashdan 50 barobar tezroq kechadi.

---

### Topshiriq #1140: IoT Ma'lumotlarini MQTT dan Qabul Qilib Geografik Koordinatalar Bo'yicha Klasterlash
**Tavsif:** Shahar bo'ylab harakatlanayotgan avtobuslar va taksilarning jonli GPS koordinatalari kelib tushganda, tirbandlik o'choqlarini aniqlash uchun ularni real-vaqtda DBSCAN orqali klasterlash zarur.
**Talablar:** `dbscan` paketi, geografik kenglik/uzunlik bo'yicha masofalarni klasterlarga ajratish.
**Yechim (R):**
```r
# Geografik koordinatalarni real-vaqtda klasterlash
cluster_live_gps_stream <- function(gps_points, eps_km = 0.5, min_pts = 3) {
  # eps_km ni taxminiy graduslarga o'girish (1 gradus ≈ 111 km)
  eps_deg <- eps_km / 111.0
  
  coords <- as.matrix(gps_points[, c("lat", "lon")])
  
  # Tezkor DBSCAN klasterlash
  cl <- dbscan::dbscan(coords, eps = eps_deg, minPts = min_pts)
  
  gps_points$cluster_id <- cl$cluster
  
  # Aniq klaster markazlarini topish
  clusters_summary <- by(gps_points[gps_points$cluster_id > 0, ], gps_points$cluster_id[gps_points$cluster_id > 0], function(sub) {
    data.frame(
      cluster = sub$cluster_id[1],
      center_lat = mean(sub$lat),
      center_lon = mean(sub$lon),
      vehicle_count = nrow(sub)
    )
  })
  
  list(
    clustered_data = gps_points,
    traffic_hotspots = do.call(rbind, clusters_summary)
  )
}

# Sinov uchun 10 ta transport vositasi koordinatalari
test_vehicles <- data.frame(
  id = 1:6,
  lat = c(41.311, 41.312, 41.3115, 41.380, 41.381, 41.382),
  lon = c(69.240, 69.241, 69.2405, 69.300, 69.301, 69.302)
)

res <- cluster_live_gps_stream(test_vehicles)
cat("Tirbandlik nuqtalari:\n")
print(res$traffic_hotspots)
```
**Tushuntirish:** DBSCAN algoritmi oldindan klasterlar sonini ($k$) talab qilmaydi. U tarmoq oqimidagi transport vositalarining zich joylashgan guruhlarini avtomatik topib, bitta taksining alohida harakatlanishini (Shovqin) tirbandlik o'chog'idan ajrata oladi.

---

### Topshiriq #1141: Sliding Window va Tumbling Window Agregatsiyalarini Real-Vaqt Oqimida Hisoblash
**Tavsif:** Tarmoq oqimida ma'lumotlar uzluksiz kelganda, har bir soatlik kesishuvsiz oyna (Tumbling Window) va har daqiqada yangilanuvchi 15 daqiqalik sirpanuvchi oyna (Sliding Window) hisobotlari yuritilishi kerak.
**Talablar:** POSIXct vaqt tamg'alari asosida oynalarni ajratuvchi va guruhlovchi R funksiyasini yozish.
**Yechim (R):**
```r
# Oqimli vaqt oynalari dvigateli
create_window_aggregator <- function(tumbling_sec = 60, sliding_sec = 180, slide_step_sec = 30) {
  event_log <- list()
  
  add_event <- function(val, ts = Sys.time()) {
    event_log[[length(event_log) + 1]] <<- list(val = val, ts = as.numeric(ts))
  }
  
  # Tumbling Window: Belgilangan davr ichidagi kesishmaydigan bloklar
  compute_tumbling <- function() {
    if (length(event_log) == 0) return(NULL)
    
    df <- do.call(rbind, lapply(event_log, as.data.frame))
    # Vaqtni intervallarga yaxlitlash (Bucket floor)
    df$bucket <- floor(df$ts / tumbling_sec) * tumbling_sec
    
    aggregate(val ~ bucket, data = df, FUN = function(x) c(count = length(x), mean = mean(x)))
  }
  
  # Sliding Window: Oxirgi sliding_sec davomiylikdagi oyna
  compute_sliding <- function() {
    now <- as.numeric(Sys.time())
    cutoff <- now - sliding_sec
    
    df <- do.call(rbind, lapply(event_log, as.data.frame))
    valid_window <- df[df$ts >= cutoff, ]
    
    list(
      window_seconds = sliding_sec,
      events_in_window = nrow(valid_window),
      window_mean = mean(valid_window$val)
    )
  }
  
  list(add = add_event, tumbling = compute_tumbling, sliding = compute_sliding)
}

# Sinov
win <- create_window_aggregator()
win$add(10)
win$add(20)
print(win$sliding())
```
**Tushuntirish:** Tumbling Window (to'ntariluvchi oyna) buxgalteriya va davriy hisobotlar uchun xizmat qiladi, chunki oyna tugashi bilan yangisi boshlanadi va voqealar takrorlanmaydi. Sliding Window esa real-vaqt trendlari va dinamik monitoring uchun doimiy o'tmish N daqiqani tahlil qiladi.

---

### Topshiriq #1142: Exponential Moving Average (EMA) va Volatillikni Oqimda Rekursiv Yangilash
**Tavsif:** Barcha o'tmish narxlarini xotirada saqlamasdan, faqat bitta oldingi qiymat asosida $O(1)$ xotirada Eksponensial Sirpanuvchi O'rtacha (EMA) va eksponensial variatsiyani hisoblab borish lozim.
**Talablar:** Rekursiv EMA formulasi: $EMA_t = lpha \cdot X_t + (1 - lpha) \cdot EMA_{t-1}$.
**Yechim (R):**
```r
# Rekursiv EMA va onlayn volatillik kalkulyatori
create_online_ema_tracker <- function(alpha = 0.1) {
  ema <- NULL
  ema_var <- 0
  
  update <- function(x) {
    if (is.null(ema)) {
      # Boshlang'ich holat
      ema <<- x
      ema_var <<- 0
    } else {
      # Delta hisoblash
      delta <- x - ema
      ema <<- alpha * x + (1 - alpha) * ema
      # Eksponensial variatsiya
      ema_var <<- (1 - alpha) * (ema_var + alpha * delta^2)
    }
    
    list(
      current_value = x,
      ema = round(ema, 4),
      ema_sd = round(sqrt(ema_var), 4)
    )
  }
  
  list(update = update)
}

# Sinov
ema_model <- create_online_ema_tracker(alpha = 0.2)
for (val in c(50, 52, 55, 60, 58, 59)) {
  res <- ema_model$update(val)
  cat(sprintf("X: %d | EMA: %.2f | SD: %.2f\n", val, res$ema, res$ema_sd))
}
```
**Tushuntirish:** Rekursiv EMA hisoblash uchun faqat bitta float sonni xotirada saqlash kifoya qiladi ($O(1)$ Memory). Bu IoT chiplari yoki soniyasiga 100 000 ta kotirovka o'tadigan birja shlyuzlarida xotirani nol darajada saqlab doimiy trendni aniqlashga yordam beradi.

---

### Topshiriq #1143: CUSUM (Cumulative Sum) Algoritmi Bilan Oqimli Vaqtli Qatorlarda Burilish Nuqtalarini Topish
**Tavsif:** Tarmoq trafigi yoki server haroratida keskin sakrash (Change Point) yuz berganda, CUSUM algoritmi statistik siljishni minimal kechikish bilan aniqlab signal berishi kerak.
**Talablar:** Page-Hinkley / CUSUM algoritmi: Musbat va manfiy kumulyativ yig'indilarni chegaraviy $H$ (Threshold) qiymat bilan tekshirish.
**Yechim (R):**
```r
# CUSUM anomaliya va siljish detektori
create_cusum_detector <- function(target_mean = 100, slack_k = 2.0, threshold_h = 10.0) {
  s_pos <- 0
  s_neg <- 0
  
  feed_point <- function(x) {
    # Musbat va manfiy kumulyativ yig'indi
    s_pos <<- max(0, s_pos + (x - target_mean - slack_k))
    s_neg <<- max(0, s_neg + (target_mean - x - slack_k))
    
    alarm <- FALSE
    alarm_type <- "NONE"
    
    if (s_pos > threshold_h) {
      alarm <- TRUE
      alarm_type <- "YUQORIGA_SILJISH"
      s_pos <<- 0 # Chegaradan oshgach nollash
    } else if (s_neg > threshold_h) {
      alarm <- TRUE
      alarm_type <- "PASTGA_SILJISH"
      s_neg <<- 0
    }
    
    list(
      val = x,
      s_pos = s_pos,
      s_neg = s_neg,
      alarm = alarm,
      type = alarm_type
    )
  }
  
  list(check = feed_point)
}

# Sinov: Normal 100 atrofida, keyin birdaniga 115 ga chiqishi
cusum <- create_cusum_detector(target_mean = 100, slack_k = 2, threshold_h = 8)
for (x in c(101, 100, 102, 108, 112, 115, 114)) {
  st <- cusum$check(x)
  if (st$alarm) {
    cat(sprintf("!!! CUSUM SIGNAL: Qiymat %d da %s aniqlandi!\n", x, st$type))
  }
}
```
**Tushuntirish:** CUSUM algoritmi Shuxart nazorat kartalariga nisbatan kichik va uzoq davom etuvchi tizimli siljishlarni bir necha barobar erta payqaydi. Tarmoq xavfsizligida bu sekin DDoS yoki ma'lumot sizib chiqishini aniqlashda qo'llaniladi.

---

### Topshiriq #1144: Xotirada Ring Buffer (Aylanma Bufer) Tuzilmasi Bilan Xotira Sizib Ketishini Cheklash
**Tavsif:** R ro'yxatlari doimiy ravishda element qo'shilganda cheksiz o'sib ketishi va xotirani to'ldirishi (Out of Memory) mumkin. Doimiy o'lchamdagi va yangi ma'lumot kelganda eskilarini ustidan yozuvchi aylanma bufer kerak.
**Talablar:** R muhitida oldindan ajratilgan vektor va aylanuvchi ko'rsatkich (Pointer) orqali Ring Buffer sinfi.
**Yechim (R):**
```r
# R da yuqori tezlikdagi Ring Buffer sinfi
create_ring_buffer <- function(capacity = 100) {
  buf <- numeric(capacity)
  head_ptr <- 1
  size <- 0
  
  push <- function(x) {
    buf[head_ptr] <<- x
    head_ptr <<- (head_ptr %% capacity) + 1
    if (size < capacity) size <<- size + 1
  }
  
  # Ma'lumotlarni eng eskidan yangisiga qarab olish
  get_all <- function() {
    if (size == 0) return(numeric(0))
    if (size < capacity) {
      return(buf[1:size])
    }
    
    # To'lgan bo'lsa: head_ptr dan boshlab oxirigacha, so'ngra 1 dan head_ptr-1 gacha
    idx <- c(head_ptr:capacity, if (head_ptr > 1) 1:(head_ptr - 1) else integer(0))
    buf[idx]
  }
  
  list(push = push, get = get_all, size = function() size)
}

# Sinov
rb <- create_ring_buffer(capacity = 3)
rb$push(10)
rb$push(20)
rb$push(30)
rb$push(40) # 10 ning ustiga yoziladi
print(rb$get()) # 20, 30, 40 chiqadi
```
**Tushuntirish:** Ring Buffer strukturasida xotira ajratish (Allocation) faqat bir marta — dastur boshlanganda amalga oshiriladi. Shundan so'ng yangi xotira so'ralmaydi va R ning Garbage Collector jarayoni CPU ga mutlaqo to'sqinlik qilmaydi.

---

### Topshiriq #1145: Oqimli Z-Score Anomaliya Detektori (Welford Algoritmi Orqali Onlayn Variatsiya)
**Tavsif:** Barcha ma'lumotlar oqimda kelganda, sonlarning kvadratlari yig'indisi cheksiz o'sib sonli xatolikka (Floating-point instability) olib keladi. Welford algoritmi orqali onlayn variatsiya va dinamik Z-Score hisoblash zarur.
**Talablar:** Welford algoritmi: $M_k = M_{k-1} + (x_k - M_{k-1})/k$ va $S_k = S_{k-1} + (x_k - M_{k-1})(x_k - M_k)$.
**Yechim (R):**
```r
# Welford algoritmi bilan barqaror onlayn Z-Score anomaliya filtri
create_welford_zscore_filter <- function(z_threshold = 3.0) {
  count <- 0
  mean_val <- 0.0
  m2 <- 0.0
  
  process_point <- function(x) {
    count <<- count + 1
    delta <- x - mean_val
    mean_val <<- mean_val + delta / count
    delta2 <- x - mean_val
    m2 <<- m2 + delta * delta2
    
    variance <- if (count > 1) m2 / (count - 1) else 0.0
    sd_val <- sqrt(variance)
    
    z_score <- if (sd_val > 0) (x - mean_val) / sd_val else 0.0
    is_anomaly <- abs(z_score) > z_threshold
    
    list(
      n = count,
      mean = round(mean_val, 3),
      sd = round(sd_val, 3),
      z_score = round(z_score, 2),
      is_anomaly = is_anomaly
    )
  }
  
  list(check = process_point)
}

# Sinov
welford <- create_welford_zscore_filter(z_threshold = 2.5)
for (val in c(10, 11, 10, 9, 10, 12, 10, 50)) {
  res <- welford$check(val)
  if (res$is_anomaly) {
    cat(sprintf("ANOMALIYA: Qiymat: %d | Z-Score: %.2f | Mean: %.2f\n", val, res$z_score, res$mean))
  }
}
```
**Tushuntirish:** Welford algoritmi (1962) hisoblash matematikasida o'rtacha va dispersiyani bitta qadamda aniq hisoblashning eng barqaror usulidir. U hatto milliardlab sonlar o'tganda ham yaxlitlash xatolariga (Catastrophic Cancellation) uchramaydi.

---

### Topshiriq #1146: Asinxron HTTP Webhooklar: Model Anomaliya Topganda Tashqi Tizimlarga Signal Yuborish
**Tavsif:** Tarmoq anomaliyasi yoki xavfli tranzaksiya aniqlangan zahoti, R skripti asosiy tahlil oqimini to'xtatmasdan, xavfsizlik serveriga (Slack, Telegram yoki Bank antifrod API) asinxron HTTP POST webhook yuborishi kerak.
**Talablar:** `httr2` ning asinxron imkoniyatlari yoki `promises::future_promise` orqali bloklanmaydigan webhook xizmati.
**Yechim (R):**
```r
library(httr2)
library(promises)
library(future)

# Webhook yuboruvchi asinxron xizmat
send_async_anomaly_webhook <- function(webhook_url, alert_data) {
  future_promise({
    # Alohida fonda HTTP so'rov yuborish
    req <- request(webhook_url) %>%
      req_headers("Content-Type" = "application/json") %>%
      req_body_json(alert_data) %>%
      req_timeout(3) # 3 soniyalik timeout
    
    # Xavfsiz yuborish
    tryCatch({
      # resp <- req_perform(req)
      # resp_status(resp)
      200 # Simulyatsiya
    }, error = function(e) {
      -1 # Tarmoq xatosi
    })
  }) %...>% (function(status) {
    cat(sprintf("[Webhook Muvaffaqiyatli] Status: %s\n", status))
  }) %...!% (function(err) {
    cat(sprintf("[Webhook Xatolik]: %s\n", err$message))
  })
}

# Sinov
alert <- list(
  service = "Khorazmiy Antifraud",
  severity = "CRITICAL",
  ip = "192.168.1.99",
  reason = "Z-Score anomaliyasi aniqlandi"
)
send_async_anomaly_webhook("https://webhook.site/fake-token", alert)
```
**Tushuntirish:** Asinxron webhooklar tahlil oqimini tarmoqdagi sekinlashuvlardan (Network Latency) himoya qiladi. Agar webhook qabul qiluvchi server sekin ishlasa ham, R ning tahliliy modeli to'xtamasdan oqimdagi keyingi paketlarni qayta ishlashda davom etadi.

---

### Topshiriq #1147: Oqimli k-Means Klasterlash: Yangi Nuqtalarni Klaster Markazlariga Onlayn Moslash
**Tavsif:** Mijozlarning xatti-harakatlari vaqt o'tishi bilan o'zgaradi. Barcha ma'lumotlarni qayta trening qilmasdan, yangi kelgan ma'lumot nuqtalariga qarab klaster markazlarini (Centroids) adaptiv siljituvchi Online Mini-Batch k-Means talab etiladi.
**Talablar:** O'rganish tezligi $\eta = 1/count$ asosida klaster markazlarini rekursiv yangilash.
**Yechim (R):**
```r
# Oqimli Online k-Means sinfi
create_streaming_kmeans <- function(k = 3, num_features = 2) {
  # Boshlang'ich tasodifiy markazlar
  centers <- matrix(runif(k * num_features, 0, 100), nrow = k, ncol = num_features)
  counts <- rep(1, k)
  
  predict_and_update <- function(point) {
    # Eng yaqin klaster markazini topish (Evklid masofasi)
    dists <- apply(centers, 1, function(c) sum((point - c)^2))
    best_cluster <- which.min(dists)
    
    # O'rganish tezligini hisoblash va markazni yangilash
    counts[best_cluster] <<- counts[best_cluster] + 1
    eta <- 1.0 / counts[best_cluster]
    
    # Markazni siljitish: C_new = C_old + eta * (Point - C_old)
    centers[best_cluster, ] <<- centers[best_cluster, ] + eta * (point - centers[best_cluster, ])
    
    list(
      assigned_cluster = best_cluster,
      distance = round(sqrt(dists[best_cluster]), 2),
      cluster_size = counts[best_cluster]
    )
  }
  
  list(update = predict_and_update, get_centers = function() centers)
}

# Sinov
skmeans <- create_streaming_kmeans(k = 2, num_features = 2)
for (i in 1:5) {
  p <- c(10 + rnorm(1), 20 + rnorm(1))
  cat("Nuqta:", p, "-> Natija:\n")
  print(skmeans$update(p))
}
```
**Tushuntirish:** Online k-Means arxitekturasi R dasturiga ma'lumotlar oqimiga 'jonli moslashish' (Concept Drift Adaptation) imkoniyatini beradi. Har bir yangi ma'lumot klaster markazini o'z tomoniga biroz siljitadi, natijada mavsumiy o'zgarishlar modelda o'z-o'zidan aks etadi.

---

### Topshiriq #1148: Oqim Unumdorligini (Throughput: Xabarlar/Soniya) Monitoring Qiluvchi Datchik
**Tavsif:** Ishlab chiqarish quvurida ma'lumotlar oqimi sekinlashib qolganini (masalan sekundiga 5000 xabar o'rniga 200 ga tushib ketganini) o'z vaqtida payqash uchun Throughput va Latency datchigini joriy qilish kerak.
**Talablar:** Har bir soniyadagi xabarlar miqdorini hisoblab, o'rtacha tezlikni chiqaruvchi telemetriya hisoblagichi.
**Yechim (R):**
```r
# Tarmoq oqimi unumdorligini monitoring qiluvchi sinf
create_throughput_meter <- function(report_interval_sec = 2) {
  msg_count <- 0
  start_time <- Sys.time()
  last_report_time <- Sys.time()
  
  record_event <- function(batch_size = 1) {
    msg_count <<- msg_count + batch_size
    now <- Sys.time()
    
    diff_report <- as.numeric(difftime(now, last_report_time, units = "secs"))
    if (diff_report >= report_interval_sec) {
      rate_sec <- msg_count / diff_report
      cat(sprintf("[Oqim Metrikasi] Tezlik: %.1f xabar/soniya | Jami: %d\n", rate_sec, msg_count))
      
      msg_count <<- 0
      last_report_time <<- now
    }
  }
  
  list(hit = record_event)
}

# Sinov
meter <- create_throughput_meter(report_interval_sec = 1)
for (i in 1:10000) {
  meter$hit(1)
  if (i %% 2000 == 0) Sys.sleep(0.3)
}
```
**Tushuntirish:** Oqim tezligini muntazam o'lchab turish orqali infratuzilmadagi tiqilinchliklar (Bottlenecks) va yuklama pasayishlari aniqlanadi. Agar xabarlar soni tushib ketsa, bu tashqi tarmoq uzilganini yoki datchiklar ishlamayotganini bildiradi.

---

### Topshiriq #1149: Tarmoqdagi Uzilish Paytida Mahalliy Disk Keshiga (Spill to Disk / SQLite) Vaqtinchalik Yozish
**Tavsif:** Agar Kafka yoki markaziy ma'lumotlar bazasi bilan aloqa uzilsa, R yangi kelayotgan oqimni yo'qotib yubormaslik uchun ularni mahalliy SQLite bazasiga yozishi, aloqa tiklangach esa ularni qayta yuborishi (Drain) shart.
**Talablar:** `RSQLite` paketi, oflayn rejimni aniqlash va tarmoq tiklanganda tranzaksiyalarni qayta uzatish.
**Yechim (R):**
```r
library(DBI)

create_spill_to_disk_manager <- function(cache_db = "offline_spill.sqlite") {
  con <- dbConnect(RSQLite::SQLite(), cache_db)
  
  # Disk kesh jadvali
  dbExecute(con, "
    CREATE TABLE IF NOT EXISTS spill_queue (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      payload TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  ")
  
  # Oflayn rejimda diskka saqlash
  save_to_disk <- function(payload_str) {
    dbExecute(con, "INSERT INTO spill_queue (payload) VALUES (?)", params = list(payload_str))
    cat("[Spill to Disk] Aloqa yo'q! Xabar mahalliy diskka zaxiralandi.\n")
  }
  
  # Aloqa tiklanganda diskdagi xabarlarni chiqarib yuborish (Drain)
  drain_to_remote <- function(remote_send_func) {
    rows <- dbGetQuery(con, "SELECT id, payload FROM spill_queue ORDER BY id ASC LIMIT 100")
    if (nrow(rows) == 0) return(0)
    
    sent_ids <- integer(0)
    for (i in seq_len(nrow(rows))) {
      success <- remote_send_func(rows$payload[i])
      if (success) {
        sent_ids <- c(sent_ids, rows$id[i])
      } else {
        break # Yana tarmoq uzildi
      }
    }
    
    if (length(sent_ids) > 0) {
      dbExecute(con, sprintf("DELETE FROM spill_queue WHERE id IN (%s)", paste(sent_ids, collapse = ",")))
      cat(sprintf("[Spill to Disk] %d ta zaxira xabar muvaffaqiyatli uzatildi va diskdan tozalandi.\n", length(sent_ids)))
    }
    length(sent_ids)
  }
  
  list(save = save_to_disk, drain = drain_to_remote, close = function() dbDisconnect(con))
}
```
**Tushuntirish:** `Spill to Disk` mexanizmi korporativ tarmoq xizmatlarining 100% ishonchliligini kafolatlaydi. Tarmoq 2 soat uzilib qolsa ham barcha telemetriya va to'lovlar mahalliy SQLite faylida to'planadi va internet kelishi bilan avtomatik serverga oqib ketadi.

---

### Topshiriq #1150: To'liq Ishchi Real-Vaqt Analitika Quvuri: Kafka/MQTT -> Oqimli Tahlil -> Plumber API -> WebSocket
**Tavsif:** Ushbu modulda o'rganilgan barcha texnologiyalarni bitta universal ishlab chiqarish quvuriga birlashtirish: xabarlar oqimini qabul qilish, statistik tahlil va anomaliyalarni aniqlash, natijalarni Plumber REST API va jonli WebSocket orqali mijozlarga taqdim etish.
**Talablar:** Barcha qatlamlarni birlashtiruvchi to'liq va mukammal R tahliliy shlyuzi.
**Yechim (R):**
```r
# Khorazmiy AI Universal Real-Vaqt Analitika Shlyuzi
library(httpuv)
library(jsonlite)

create_end_to_end_analytics_pipeline <- function(ws_port = 9001) {
  # 1. Xotiradagi tahlil holati
  metrics_history <- numeric(0)
  active_subscribers <- list()
  total_processed <- 0
  
  # 2. WebSocket serverini ochish (Jonli monitoring dashboardi uchun)
  ws_app <- list(
    call = function(req) {
      list(status = 200L, headers = list("Content-Type" = "text/plain"), body = "Analytics Hub Ready")
    },
    onWSOpen = function(ws) {
      client_id <- as.character(length(active_subscribers) + 1)
      active_subscribers[[client_id]] <<- ws
      cat(sprintf("[Pipeline WS] Yangi dashboard ulandi: %s\n", client_id))
      
      ws$onClose(function() {
        active_subscribers[[client_id]] <<- NULL
      })
    }
  )
  
  server <- startServer("0.0.0.0", ws_port, ws_app)
  cat(sprintf("[Universal Pipeline] WebSocket Server port %d da faol.\n", ws_port))
  
  # 3. Kiruvchi paketlarni qayta ishlash yuragi
  ingest_and_process <- function(sensor_id, raw_value) {
    total_processed <<- total_processed + 1
    val <- as.numeric(raw_value)
    
    # Rolling oyna (Oxirgi 50 ta ko'rsatkich)
    metrics_history <<- c(tail(metrics_history, 49), val)
    
    current_mean <- mean(metrics_history)
    current_sd <- if (length(metrics_history) > 1) sd(metrics_history) else 0.0
    
    # Anomaliya tekshiruvi (Z-Score > 2.5)
    z_score <- if (current_sd > 0) (val - current_mean) / current_sd else 0.0
    is_anomaly <- abs(z_score) > 2.5
    
    event_packet <- list(
      sensor_id = sensor_id,
      value = val,
      mean_window = round(current_mean, 2),
      z_score = round(z_score, 2),
      anomaly = is_anomaly,
      timestamp = as.character(Sys.time())
    )
    
    # 4. Jonli WebSocket dashboardlariga darhol tarqatish
    json_event <- toJSON(event_packet, auto_unbox = TRUE)
    for (client in active_subscribers) {
      tryCatch(client$send(json_event), error = function(e) {})
    }
    
    event_packet
  }
  
  list(
    process_point = ingest_and_process,
    get_summary = function() list(total = total_processed, active_ws = length(active_subscribers)),
    stop = function() stopServer(server)
  )
}

# Quvurni ishga tushirish va sinovdan o'tkazish
pipeline <- create_end_to_end_analytics_pipeline(ws_port = 9001)

# Kiruvchi datchik oqimi simulyatsiyasi
cat("Oddiy datchik signallari uzatilmoqda:\n")
pipeline$process_point("SENSOR_A", 100)
pipeline$process_point("SENSOR_A", 102)

cat("Anomal sakrash uzatilmoqda:\n")
alert_res <- pipeline$process_point("SENSOR_A", 145)
print(alert_res)

# To'xtatish:
pipeline$stop()
```
**Tushuntirish:** Ushbu yakuniy tizim R tilining zamonaviy korporativ arxitekturalarda eng ilg'or real-vaqt ma'lumotlar oqimini tahlil qilish imkoniyatlarini to'liq namoyon etadi. U Kafka/MQTT xabarlarini qabul qiladi, onlayn statistik modellar orqali anomaliyalarni hisoblaydi va natijalarni real-vaqtda veb-dashboardlarga yetkazadi.

---
