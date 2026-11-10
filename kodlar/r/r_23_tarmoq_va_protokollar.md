# Khorazmiy AI: R - Modul 23
## Mavzu: Tarmoq protokollari: TCP/UDP soketlari, HTTP/3, QUIC va WebSockets

### Topshiriq #1101: TCP soketlari orqali real vaqtda ma'lumotlar oqimini qabul qilish
**Tavsif:** Milliy serverlar o'rtasida TCP protokoli orqali uzluksiz telemetriya ma'lumotlarini qabul qilish va buferlash.
**Talablar:** `parallel` va `tcltk` kutubxonalaridan foydalanmasdan, `socketConnection` yordamida bloklanmaydigan (non-blocking) o'qish mexanizmini joriy etish.
**Yechim (R):**
```r
# TCP soketini ochish va ma'lumotlarni qabul qilish
con <- socketConnection(host="localhost", port=6011, blocking=FALSE, server=TRUE, open="r")

# Ma'lumotlarni o'qish funksiyasi
read_stream <- function(connection) {
  data <- readLines(connection, n=1)
  if (length(data) > 0) {
    message("Qabul qilindi: ", data)
  }
}

# 10 soniya davomida tinglash
for(i in 1:100) {
  read_stream(con)
  Sys.sleep(0.1)
}
close(con)
```
**Tushuntirish:** `blocking=FALSE` parametri tizimning qotib qolmasligini ta'minlaydi, bu esa yuqori yuklamali tizimlarda muhimdir.

### Topshiriq #1102: UDP orqali paketli ma'lumotlarni qayta ishlash
**Tavsif:** IoT qurilmalaridan kelayotgan UDP paketlarini yo'qotishlarsiz tahlil qilish.
**Talablar:** `nws` (NetWorkSpaces) yoki `parallel` paketlaridan foydalanib, paketlar ketma-ketligini tekshirish.
**Yechim (R):**
```r
# UDP soket simulyatsiyasi (R da UDP uchun 'nanonext' tavsiya etiladi)
library(nanonext)
s <- socket("pull", listen = "inproc://telemetry")
# Paketni qabul qilish
msg <- recv(s)
cat("UDP paketi tarkibi:", msg$data, "\n")
```
**Tushuntirish:** UDP ishonchsiz protokol bo'lgani uchun, `nanonext` orqali xabarlar navbatini (queue) boshqarish eng samarali yo'ldir.

### Topshiriq #1103: HTTP/3 protokoli orqali ma'lumotlar uzatish
**Tavsif:** Zamonaviy milliy API xizmatlari uchun HTTP/3 (QUIC asosida) orqali ma'lumotlarni tezkor so'rash.
**Talablar:** `httr2` kutubxonasi yordamida HTTP/3 qo'llab-quvvatlanadigan so'rovlarni amalga oshirish.
**Yechim (R):**
```r
library(httr2)
# HTTP/3 so'rovini shakllantirish
req <- request("https://api.milliy-server.uz/v1/data") %>%
  req_method("GET") %>%
  req_headers("Accept" = "application/json")

resp <- req_perform(req)
print(resp_body_json(resp))
```
**Tushuntirish:** `httr2` zamonaviy HTTP standartlarini qo'llab-quvvatlaydi, bu esa ma'lumotlar uzatish tezligini oshiradi.

### Topshiriq #1104: WebSockets orqali ikki tomonlama aloqa
**Tavsif:** Foydalanuvchi interfeysi va R backend o'rtasida real vaqtda ma'lumot almashish.
**Talablar:** `httpuv` kutubxonasi yordamida WebSocket serverini ishga tushirish.
**Yechim (R):**
```r
library(httpuv)
app <- list(
  onWSOpen = function(ws) {
    ws$onMessage(function(binary, message) {
      ws$send(paste("Server qabul qildi:", message))
    })
  }
)
runServer("0.0.0.0", 8080, app)
```
**Tushuntirish:** `httpuv` asinxron ishlash qobiliyatiga ega bo'lib, u yuqori konkurentlikni ta'minlaydi.

### Topshiriq #1105: QUIC protokoli orqali xavfsiz ma'lumotlar uzatish
**Tavsif:** Ma'lumotlar uzatishda paketlar yo'qolishini minimallashtirish uchun QUIC protokoli implementatsiyasi.
**Talablar:** TLS 1.3 shifrlash qatlamini qo'llash.
**Yechim (R):**
```r
# QUIC uchun 'quicr' (yoki mos keluvchi wrapper) ishlatiladi
# Bu yerda xavfsizlik sertifikatlari bilan ulanish
secure_conn <- quic_connect("https://secure.data.uz", cert = "path/to/cert.pem")
send_data(secure_conn, payload = "KhorazmiyAI_Data_Packet")
```
**Tushuntirish:** QUIC TCP ga qaraganda tezroq ulanishni o'rnatadi, chunki u 0-RTT (Round Trip Time) texnologiyasidan foydalanadi.

### Topshiriq #1106: Soketlar uchun bufer hajmini optimallashtirish
**Tavsif:** Katta hajmdagi datasetlarni uzatishda tarmoq tiqilishini oldini olish.
**Talablar:** `socketOptions` yordamida TCP buferini 64KB ga sozlash.
**Yechim (R):**
```r
con <- socketConnection(host="localhost", port=9000, blocking=TRUE)
# Bufer hajmini sozlash (OS darajasida)
options(socket_buffer_size = 65536)
writeLines("Dataset_Chunk_001", con)
close(con)
```
**Tushuntirish:** Bufer hajmini optimallashtirish tarmoq paketlarining yo'qolish ehtimolini kamaytiradi.

### Topshiriq #1107: WebSocket orqali JSON oqimini tahlil qilish
**Tavsif:** WebSocket orqali kelayotgan JSON ma'lumotlarini `jsonlite` yordamida tezkor pars qilish.
**Talablar:** Xatolarni boshqarish (tryCatch) bloklarini qo'shish.
**Yechim (R):**
```r
library(jsonlite)
process_ws_msg <- function(raw_json) {
  tryCatch({
    data <- fromJSON(raw_json)
    return(data$value * 1.05) # Hisob-kitob
  }, error = function(e) return(NULL))
}
```
**Tushuntirish:** `fromJSON` funksiyasi R obyektlariga tez konvertatsiya qiladi, bu esa real vaqt tizimlari uchun muhim.

### Topshiriq #1108: Tarmoq kechikishini (Latency) o'lchash
**Tavsif:** Serverlar o'rtasidagi tarmoq sifatini monitoring qilish.
**Talablar:** `ping` buyrug'ini R orqali chaqirib, natijani `data.frame` ga yozish.
**Yechim (R):**
```r
measure_latency <- function(host) {
  res <- system(paste("ping -c 4", host), intern = TRUE)
  # Natijani ajratib olish
  avg_time <- as.numeric(gsub(".*= ", "", res[length(res)]))
  return(data.frame(host=host, latency=avg_time))
}
```
**Tushuntirish:** Tizim monitoringi uchun `system` chaqiruvlari eng ishonchli usul hisoblanadi.

### Topshiriq #1109: TCP soketlarida "Keep-Alive" mexanizmi
**Tavsif:** Uzoq muddatli ulanishlarda soket uzilib qolmasligi uchun "Keep-Alive" paketlarini yuborish.
**Talablar:** Har 30 soniyada "heartbeat" xabarini yuborish.
**Yechim (R):**
```r
# Heartbeat funksiyasi
send_heartbeat <- function(con) {
  writeLines("PING", con)
  message("Heartbeat yuborildi.")
}
# Davriy vazifa (tashqi scheduler bilan ishlatiladi)
```
**Tushuntirish:** "Keep-Alive" ulanishning faol ekanligini tasdiqlaydi va firewall tomonidan uzilishlarning oldini oladi.

### Topshiriq #1110: HTTP/3 orqali katta fayllarni yuklash (Multipart)
**Tavsif:** Katta dataset fayllarini HTTP/3 orqali bo'laklab yuklash.
**Talablar:** `httr2` ning `req_body_multipart` funksiyasidan foydalanish.
**Yechim (R):**
```r
req <- request("https://storage.milliy.uz/upload") %>%
  req_body_multipart(
    file = curl::form_file("dataset_part1.csv")
  ) %>%
  req_perform()
```
**Tushuntirish:** Multipart yuklash xotira sarfini kamaytiradi va yuklash jarayonini xavfsizroq qiladi.

---

### Topshiriq #1111: TCP soketlari orqali ma'lumotlar uzatish
**Tavsif:** Server va mijoz o'rtasida ishonchli ma'lumot almashinuvini ta'minlash uchun TCP soketlarini sozlash.
**Talablar:** `parallel` va `tcltk` kutubxonalaridan foydalangan holda bloklanmaydigan ulanishni amalga oshirish.
**Yechim (R):**
```r
# TCP serverini ishga tushirish
server <- socketConnection(host="localhost", port=6011, blocking=TRUE, server=TRUE, open="r+")
# Mijozdan xabar kutish
xabar <- readLines(server, n=1)
cat("Qabul qilindi:", xabar, "\n")
writeLines("Salom, mijoz!", server)
close(server)
```
**Tushuntirish:** TCP ulanishda `blocking=TRUE` ma'lumot to'liq kelguncha kutishni ta'minlaydi, bu esa ma'lumotlar yaxlitligini kafolatlaydi.

### Topshiriq #1112: UDP orqali tezkor paket uzatish
**Tavsif:** Real vaqt rejimida telemetriya ma'lumotlarini uzatish uchun UDP protokolidan foydalanish.
**Talablar:** Paket yo'qolishi ehtimolini hisobga olgan holda ma'lumotlarni ketma-ketlik raqami bilan yuborish.
**Yechim (R):**
```r
# UDP soketini simulyatsiya qilish (R da 'nanonext' paketi tavsiya etiladi)
library(nanonext)
s <- socket("push", listen = "inproc://telemetry")
send(s, data.frame(id=1, val=100.5))
# Ma'lumot yuborilgach soketni yopish
close(s)
```
**Tushuntirish:** UDP tezlik uchun mo'ljallangan, shuning uchun `nanonext` kabi zamonaviy kutubxonalar orqali asinxron uzatish optimallashtiriladi.

### Topshiriq #1113: HTTP/3 protokoli orqali so'rov yuborish
**Tavsif:** Zamonaviy HTTP/3 (QUIC asosida) protokoli orqali API bilan bog'lanish.
**Talablar:** `curl` kutubxonasi orqali HTTP/3 qo'llab-quvvatlanadigan so'rovni amalga oshirish.
**Yechim (R):**
```r
library(curl)
h <- new_handle()
handle_setopt(h, http_version = 3) # HTTP/3 ni majburiy tanlash
res <- curl_fetch_memory("https://google.com", handle = h)
cat("Status kodi:", res$status_code)
```
**Tushuntirish:** HTTP/3 (QUIC) TCP dagi "Head-of-line blocking" muammosini hal qiladi, bu esa yuqori tezlikdagi ma'lumotlar almashinuvini ta'minlaydi.

### Topshiriq #1114: QUIC protokoli orqali xavfsiz ulanish
**Tavsif:** TLS 1.3 shifrlash qatlamiga ega QUIC protokoli orqali ma'lumotlar xavfsizligini ta'minlash.
**Talablar:** Xavfsizlik sertifikatlarini tekshirish va shifrlangan kanalni ochish.
**Yechim (R):**
```r
# QUIC ulanishini simulyatsiya qilish
# 'httr2' kutubxonasi zamonaviy protokollarni qo'llab-quvvatlaydi
library(httr2)
req <- request("https://api.example.com") %>%
  req_options(http_version = 3) %>%
  req_perform()
```
**Tushuntirish:** QUIC o'z ichiga TLS 1.3 ni oladi, bu esa ulanish vaqtini qisqartiradi va xavfsizlikni oshiradi.

### Topshiriq #1115: WebSockets orqali ikki tomonlama aloqa
**Tavsif:** Serverdan mijozga real vaqtda ma'lumot push qilish (masalan, birja narxlari).
**Talablar:** `httpuv` kutubxonasi yordamida WebSocket serverini yaratish.
**Yechim (R):**
```r
library(httpuv)
app <- list(onWSOpen = function(ws) {
  ws$onMessage(function(binary, message) {
    ws$send("Serverdan javob: " %+% message)
  })
})
runServer("0.0.0.0", 8080, app)
```
**Tushuntirish:** WebSocket doimiy ulanishni ushlab turadi, bu esa HTTP so'rovlaridagi ortiqcha header yuklamalarini kamaytiradi.

### Topshiriq #1116: TCP soketlarida ma'lumotlar buferizatsiyasi
**Tavsif:** Katta hajmdagi ma'lumotlarni TCP orqali uzatishda xotira to'lib ketishining oldini olish.
**Talablar:** `readBin` funksiyasi yordamida ma'lumotlarni bo'laklab (chunk) o'qish.
**Yechim (R):**
```r
con <- socketConnection(port=6012, server=TRUE)
while(TRUE) {
  chunk <- readBin(con, what="raw", n=1024) # 1KB dan o'qish
  if(length(chunk) == 0) break
  # Ma'lumotni qayta ishlash
}
close(con)
```
**Tushuntirish:** Buferizatsiya xotira sarfini nazorat qilishga va tarmoq o'tkazuvchanligini optimallashtirishga yordam beradi.

### Topshiriq #1117: WebSocket orqali JSON ma'lumotlarini uzatish
**Tavsif:** WebSocket orqali strukturaviy ma'lumotlarni (JSON) uzatish va pars qilish.
**Talablar:** `jsonlite` kutubxonasi bilan integratsiya.
**Yechim (R):**
```r
library(jsonlite)
# WebSocket orqali kelgan JSON ni pars qilish
data <- fromJSON('{"sensor": "temp", "value": 25.4}')
cat("Sensor qiymati:", data$value)
```
**Tushuntirish:** WebSocket orqali yuborilgan JSON ma'lumotlari real vaqtda tahlil qilinishi uchun eng samarali format hisoblanadi.

### Topshiriq #1118: Tarmoq protokollarida xatolarni qayta ishlash
**Tavsif:** Tarmoq uzilishlari sodir bo'lganda soket ulanishini avtomatik tiklash.
**Talablar:** `tryCatch` bloklari yordamida ulanish xatolarini boshqarish.
**Yechim (R):**
```r
tryCatch({
  con <- socketConnection(host="localhost", port=6013)
}, error = function(e) {
  message("Ulanishda xato, qayta urinilmoqda...")
  Sys.sleep(2)
})
```
**Tushuntirish:** Suveren tizimlarda barqarorlik birinchi o'rinda, shuning uchun avtomatik qayta ulanish (reconnection) mexanizmi majburiy.

### Topshiriq #1119: HTTP/3 orqali katta fayllarni yuklash
**Tavsif:** HTTP/3 protokoli yordamida katta hajmdagi dataset fayllarini serverga yuklash.
**Talablar:** `curl` orqali `multi-handle` funksiyasidan foydalanish.
**Yechim (R):**
```r
library(curl)
h <- new_handle()
handle_setopt(h, http_version = 3, upload = TRUE)
curl_upload("dataset.csv", "https://server.uz/upload", handle = h)
```
**Tushuntirish:** HTTP/3 parallel oqimlarni qo'llab-quvvatlaydi, bu katta fayllarni yuklashda TCP ga qaraganda tezroq natija beradi.

### Topshiriq #1120: WebSocket orqali xavfsizlik tokenlarini tekshirish
**Tavsif:** WebSocket ulanishini ochishdan oldin mijoz autentifikatsiyasini tekshirish.
**Talablar:** `headers` orqali yuborilgan JWT tokenini validatsiya qilish.
**Yechim (R):**
```r
# Autentifikatsiya funksiyasi
check_auth <- function(token) {
  if(token == "suveren_token_2024") return(TRUE)
  return(FALSE)
}
# WebSocket ulanishida token tekshiruvi
# (httpuv ichida headerlarni tahlil qilish orqali)
```
**Tushuntirish:** Har qanday tarmoq protokoli uchun autentifikatsiya qatlami xavfsizlikning asosiy bo'g'ini hisoblanadi.

---

### Topshiriq #1121: TCP soketlari orqali ma'lumotlar oqimini boshqarish
**Tavsif:** Real vaqt rejimida serverdan kelayotgan sensor ma'lumotlarini qabul qilish uchun TCP soketini ochish va ma'lumotlar yaxlitligini tekshirish.
**Talablar:** `parallel` va `socketConnection` kutubxonalaridan foydalanish, xatolarni qayta ishlash (error handling).
**Yechim (R):**
```r
# TCP soketini ochish
con <- socketConnection(host = "localhost", port = 6011, blocking = TRUE, server = FALSE)

# Ma'lumotlarni o'qish funksiyasi
read_sensor_data <- function(connection) {
  tryCatch({
    data <- readLines(connection, n = 1)
    return(as.numeric(data))
  }, error = function(e) return(NA))
}

# Ma'lumotni olish va yopish
val <- read_sensor_data(con)
close(con)
```
**Tushuntirish:** `blocking = TRUE` rejimi ma'lumotlar to'liq kelguncha kutishni ta'minlaydi, bu esa paket yo'qolishining oldini oladi.

### Topshiriq #1122: UDP orqali tezkor telemetriya uzatish
**Tavsif:** Yuqori tezlikdagi, ammo yo'qotishlarga chidamli telemetriya ma'lumotlarini yuborish.
**Talablar:** `nanonext` paketidan foydalanish, UDP protokoli xususiyatlarini hisobga olish.
**Yechim (R):**
```r
library(nanonext)
# UDP soketini sozlash
s <- socket("push", listen = "udp://127.0.0.1:5555")
send(s, "Telemetriya: 24.5C")
close(s)
```
**Tushuntirish:** UDP ulanishsiz protokol bo'lgani uchun `nanonext` orqali xabarni tezkor yuborish va resursni darhol bo'shatish samaraliroq.

### Topshiriq #1123: HTTP/3 protokoli orqali API so'rovlarini optimallashtirish
**Tavsif:** Zamonaviy HTTP/3 (QUIC asosidagi) protokoli orqali katta hajmdagi JSON ma'lumotlarini olish.
**Talablar:** `httr2` kutubxonasi, HTTP/3 qo'llab-quvvatlanadigan server bilan ishlash.
**Yechim (R):**
```r
library(httr2)
# HTTP/3 so'rovini amalga oshirish
req <- request("https://api.milliy-server.uz/v1/data") %>%
  req_options(http_version = 3) %>%
  req_perform()

data <- resp_body_json(req)
```
**Tushuntirish:** HTTP/3 "Head-of-line blocking" muammosini hal qiladi, bu esa tarmoq kechikishlari yuqori bo'lgan holatlarda tezlikni oshiradi.

### Topshiriq #1124: QUIC protokoli orqali xavfsiz ma'lumotlar almashinuvi
**Tavsif:** QUIC protokoli yordamida TLS 1.3 shifrlash qatlamini qo'llagan holda ma'lumot uzatish.
**Talablar:** Xavfsizlik sertifikatlarini tekshirish va ma'lumotlar yaxlitligini ta'minlash.
**Yechim (R):**
```r
# QUIC protokoli uchun konfiguratsiya
config <- list(tls_verify = TRUE, protocol = "quic")
# Ulanishni amalga oshirish (simulyatsiya)
# 'quicR' kutubxonasi orqali xavfsiz kanal ochish
secure_conn <- quic_connect("secure.uz", config)
send_secure(secure_conn, "Maxfiy ma'lumot")
```
**Tushuntirish:** QUIC o'zida TLS 1.3 ni mujassam etgani uchun alohida qo'shimcha qatlamlarsiz xavfsizlikni ta'minlaydi.

### Topshiriq #1125: WebSockets orqali ikki tomonlama aloqa
**Tavsif:** Foydalanuvchi interfeysi va R backend o'rtasida real vaqtda yangilanuvchi ma'lumotlar kanali.
**Talablar:** `httpuv` paketidan foydalanish, asinxron hodisalarni boshqarish.
**Yechim (R):**
```r
library(httpuv)
# WebSocket serverini ishga tushirish
ws_server <- startServer("0.0.0.0", 8080, list(
  onMessage = function(ws, binary, message) {
    ws$send(paste("Qabul qilindi:", message))
  }
))
```
**Tushuntirish:** `httpuv` asinxron ishlash imkonini beradi, bu esa ko'p foydalanuvchili tizimlarda bloklanishni oldini oladi.

### Topshiriq #1126: TCP paketlarini buferlash va qayta yig'ish
**Tavsif:** Tarmoqdan kelayotgan bo'lingan TCP paketlarini to'liq xabarga aylantirish.
**Talablar:** Bufer hajmini nazorat qilish va xotira oqishini (memory leak) oldini olish.
**Yechim (R):**
```r
buffer <- raw(0)
# Paketlarni yig'ish
process_packet <- function(new_data) {
  buffer <<- c(buffer, new_data)
  if (length(buffer) >= 1024) { # 1KB to'lganda qayta ishlash
    # Ma'lumotni qayta ishlash logikasi
    buffer <<- raw(0)
  }
}
```
**Tushuntirish:** Katta hajmdagi ma'lumotlar bilan ishlashda buferlash xotirani tejash va CPU yuklamasini kamaytirish uchun zarur.

### Topshiriq #1127: HTTP/3 orqali oqimli (streaming) ma'lumotlarni yuklash
**Tavsif:** Katta hajmdagi fayllarni HTTP/3 orqali qismlarga bo'lib yuklash.
**Talablar:** `curl` kutubxonasi orqali stream rejimini yoqish.
**Yechim (R):**
```r
library(curl)
h <- new_handle()
handle_setopt(h, http_version = 3, verbose = TRUE)
curl_download("https://data.uz/large_file.zip", "local_file.zip", handle = h)
```
**Tushuntirish:** `curl_download` funksiyasi HTTP/3 bilan birlashganda, paketlar yo'qolishi kuzatilsa ham, yuklash jarayoni to'xtab qolmaydi.

### Topshiriq #1128: WebSocket orqali JSON serializatsiyasi
**Tavsif:** WebSocket orqali kelayotgan JSON obyektlarini R ro'yxatlariga (list) tezkor aylantirish.
**Talablar:** `jsonlite` kutubxonasi, xatolarni tekshirish (valid JSON).
**Yechim (R):**
```r
library(jsonlite)
handle_ws_json <- function(msg) {
  data <- tryCatch(fromJSON(msg), error = function(e) NULL)
  if (!is.null(data)) {
    print(data$timestamp)
  }
}
```
**Tushuntirish:** `fromJSON` funksiyasi WebSocket oqimlarida tezkor ma'lumotlar almashinuvi uchun eng optimallashtirilgan yechimdir.

### Topshiriq #1129: Tarmoq kechikishini (latency) o'lchash
**Tavsif:** TCP ulanishining RTT (Round Trip Time) vaqtini o'lchash.
**Talablar:** `microbenchmark` va `tictoc` kutubxonalaridan foydalanish.
**Yechim (R):**
```r
library(tictoc)
tic()
# TCP so'rovini yuborish
socketConnection("google.com", port = 80, timeout = 5)
toc() # Kechikish vaqtini ko'rsatadi
```
**Tushuntirish:** Tarmoq protokollarini sozlashda RTT ni bilish, timeout qiymatlarini to'g'ri belgilash uchun muhimdir.

### Topshiriq #1130: Xavfsiz WebSocket (WSS) ulanishini o'rnatish
**Tavsif:** SSL/TLS sertifikatlari bilan himoyalangan WebSocket ulanishini yaratish.
**Talablar:** `openssl` kutubxonasi va xavfsiz soket sozlamalari.
**Yechim (R):**
```r
# WSS ulanishi uchun sertifikatni yuklash
ctx <- openssl::ssl_ctx(ca = "cert.pem")
# WebSocket ulanishini xavfsiz rejimda ochish
ws_secure <- httpuv::startServer("0.0.0.0", 443, list(ssl_ctx = ctx))
```
**Tushuntirish:** Suveren tizimlarda ma'lumotlar maxfiyligi uchun WSS majburiy hisoblanadi, `ssl_ctx` esa ulanishni shifrlangan holda ushlab turadi.

---

### Topshiriq #1131: TCP soketlari yordamida ma'lumotlar uzatish
**Tavsif:** Server va mijoz o'rtasida TCP protokoli orqali xavfsiz ma'lumot almashinuvini ta'minlash. Real vaqt rejimida loglarni yig'ish uchun zarur.
**Talablar:** `parallel` va `tcltk` kutubxonalaridan foydalanmasdan, `socketConnection` funksiyasi orqali bloklanmaydigan (non-blocking) ulanishni amalga oshirish.
**Yechim (R):**
```r
# TCP serverni ishga tushirish
server_socket <- socketConnection(host="localhost", port=6011, blocking=TRUE, server=TRUE, open="r+")
# Mijozdan xabar kutish
xabar <- readLines(server_socket, n=1)
print(paste("Qabul qilindi:", xabar))
# Javob qaytarish
writeLines("Ma'lumot qabul qilindi", server_socket)
close(server_socket)
```
**Tushuntirish:** TCP ulanishida `blocking=TRUE` tanlandi, chunki ma'lumotlarning to'liq yetib kelishi ma'lumotlar yaxlitligi (integrity) uchun muhimdir.

### Topshiriq #1132: UDP orqali tezkor telemetriya uzatish
**Tavsif:** IoT qurilmalardan kelayotgan yuqori chastotali sensor ma'lumotlarini yo'qotishlarga chidamli tarzda qabul qilish.
**Talablar:** UDP paketlarini qabul qilishda `nmap` yoki `sys` kutubxonalaridan foydalanmasdan, `socketConnection` (type="udp") parametrini qo'llash.
**Yechim (R):**
```r
# UDP soketini ochish
udp_socket <- socketConnection(host="localhost", port=6012, server=TRUE, blocking=FALSE, open="a+b")
# Paketni o'qish (UDP uchun buffer hajmi muhim)
paket <- readBin(udp_socket, what="raw", n=1024)
print(paste("UDP paketi hajmi:", length(paket)))
close(udp_socket)
```
**Tushuntirish:** UDP "connectionless" bo'lgani uchun `blocking=FALSE` ishlatildi, bu esa serverning paket kutib qotib qolmasligini ta'minlaydi.

### Topshiriq #1133: HTTP/3 protokoli simulyatsiyasi
**Tavsif:** HTTP/3 (QUIC asosida) protokoli orqali ma'lumotlar uzatishni modellashtirish.
**Talablar:** `httr2` paketidan foydalanib, HTTP/3 headerlarini simulyatsiya qilish va ulanishni tekshirish.
**Yechim (R):**
```r
library(httr2)
# HTTP/3 so'rovini simulyatsiya qilish
req <- request("https://api.khorazmiy.uz") |>
  req_headers("Alt-Svc" = 'h3=":443"; ma=86400')
# So'rovni yuborish
resp <- req_perform(req)
print(resp$status_code)
```
**Tushuntirish:** HTTP/3 ning asosiy xususiyati `Alt-Svc` headeridir, bu kodda serverning HTTP/3 ni qo'llab-quvvatlashini tekshirish mexanizmi ko'rsatilgan.

### Topshiriq #1134: QUIC protokoli orqali 0-RTT ma'lumot uzatish
**Tavsif:** Latentlikni kamaytirish uchun 0-RTT (Zero Round Trip Time) mexanizmini tushunish.
**Talablar:** Ulanishni qayta tiklashda xavfsizlik tokenlarini boshqarish.
**Yechim (R):**
```r
# 0-RTT uchun sessiya tokenini yaratish
session_token <- digest::digest(Sys.time(), algo="sha256")
# Tokenni headerga joylash
header_0rtt <- list("QUIC-0RTT-Token" = session_token)
print(paste("Sessiya tiklandi, token:", header_0rtt))
```
**Tushuntirish:** QUIC protokoli tezligining siri oldingi sessiya ma'lumotlarini qayta ishlatishda, bu kodda token boshqaruvi aks etgan.

### Topshiriq #1135: WebSockets orqali real vaqtda ma'lumotlar oqimi
**Tavsif:** `httpuv` kutubxonasi yordamida WebSocket serverini qurish.
**Talablar:** Asinxron hodisalarni (events) boshqarish.
**Yechim (R):**
```r
library(httpuv)
app <- list(
  onWSOpen = function(ws) {
    ws$onMessage(function(binary, message) {
      ws$send(paste("Echo:", message))
    })
  }
)
# Serverni ishga tushirish (port 8080)
runServer("0.0.0.0", 8080, app)
```
**Tushuntirish:** `httpuv` asinxron ishlash uchun eng samarali R kutubxonasi bo'lib, WebSocket ulanishlarini bloklamasdan boshqaradi.

### Topshiriq #1136: TCP paketlarini filtrlash
**Tavsif:** Kiruvchi TCP paketlaridan zararli so'rovlarni ajratib olish.
**Talablar:** Regex yordamida `payload` tarkibini tekshirish.
**Yechim (R):**
```r
filter_tcp_payload <- function(payload) {
  # SQL injection yoki XSS belgilarini tekshirish
  if (grepl("SELECT|DROP|SCRIPT", payload, ignore.case = TRUE)) {
    return("Xavfli paket bloklandi")
  }
  return("Paket qabul qilindi")
}
print(filter_tcp_payload("SELECT * FROM users"))
```
**Tushuntirish:** Tarmoq xavfsizligi darajasida payloadni tekshirish server resurslarini himoya qiladi.

### Topshiriq #1137: WebSocket orqali JSON ma'lumot almashinuvi
**Tavsif:** WebSocket orqali strukturaviy ma'lumotlarni (JSON) uzatish va pars qilish.
**Talablar:** `jsonlite` kutubxonasi bilan integratsiya.
**Yechim (R):**
```r
library(jsonlite)
data <- list(sensor_id = 1, value = 23.5)
json_data <- toJSON(data)
# WebSocket orqali yuborish simulyatsiyasi
cat("Yuborilayotgan JSON:", json_data)
```
**Tushuntirish:** WebSocket orqali xom matn emas, balki JSON formatida ma'lumot uzatish tizimlararo moslikni ta'minlaydi.

### Topshiriq #1138: TCP ulanishlarida timeout boshqaruvi
**Tavsif:** Ulanishlar osilib qolmasligi uchun timeout mexanizmini joriy etish.
**Talablar:** `setTimeLimit` funksiyasidan foydalanish.
**Yechim (R):**
```r
# 5 soniyalik timeout o'rnatish
setTimeLimit(elapsed = 5)
tryCatch({
  con <- socketConnection(host="localhost", port=6013)
}, error = function(e) print("Ulanish vaqti tugadi!"))
```
**Tavsif:** `setTimeLimit` serverning resurslarini bo'shatish va "zombi" ulanishlarning oldini olish uchun muhimdir.

### Topshiriq #1139: QUIC oqimlarini (Streams) boshqarish
**Tavsif:** Bitta QUIC ulanishida bir nechta parallel oqimlarni boshqarish.
**Talablar:** Oqim IDlarini (Stream ID) kuzatish.
**Yechim (R):**
```r
streams <- list(s1 = "data_stream_1", s2 = "data_stream_2")
# Oqimni tanlab ma'lumot yuborish
send_quic <- function(stream_id, data) {
  print(paste("Oqim", stream_id, "orqali yuborildi:", data))
}
send_quic("s1", "Sensor_A_Data")
```
**Tushuntirish:** QUIC ning asosiy afzalligi - Head-of-line blocking muammosini hal qilish uchun oqimlarni mustaqil boshqarishdir.

### Topshiriq #1140: Tarmoq protokoli loglarini tahlil qilish
**Tavsif:** Server loglarini tahlil qilib, protokollar bo'yicha trafik taqsimotini aniqlash.
**Talablar:** `dplyr` yordamida guruhlash.
**Yechim (R):**
```r
library(dplyr)
logs <- data.frame(protocol = c("TCP", "UDP", "WS", "TCP"), size = c(100, 50, 200, 120))
summary_stats <- logs |> 
  group_by(protocol) |> 
  summarise(total_size = sum(size))
print(summary_stats)
```
**Tushuntirish:** `dplyr` ning tezkorligi katta hajmdagi tarmoq loglarini real vaqtda tahlil qilish uchun eng optimal yondashuvdir.

---

### Topshiriq #1141: TCP soketlari orqali ma'lumotlar oqimini boshqarish
**Tavsif:** Server va mijoz o'rtasida uzluksiz ma'lumot almashinuvini ta'minlash uchun TCP soketlarini sozlash.
**Talablar:** `parallel` va `tcltk` paketlaridan foydalanib, bloklanmaydigan (non-blocking) ulanishni amalga oshirish.
**Yechim (R):**
```r
# TCP serverini yaratish
server_socket <- make.socket(host = "localhost", port = 8080, server = TRUE)
on.exit(close.socket(server_socket))

# Mijozdan ma'lumot kutish
repeat {
  client <- accept.socket(server_socket)
  data <- read.socket(client, maxlen = 1024)
  if (nchar(data) > 0) {
    write.socket(client, paste("Qabul qilindi:", data))
    close.socket(client)
    break
  }
}
```
**Tushuntirish:** TCP ulanishida `make.socket` funksiyasi barqaror kanalni ta'minlaydi. `on.exit` xavfsizlik uchun soketni avtomatik yopishni kafolatlaydi.

### Topshiriq #1142: UDP orqali paketli ma'lumot uzatish
**Tavsif:** Real vaqt rejimida monitoring tizimlari uchun UDP protokoli orqali tezkor ma'lumot uzatish.
**Talablar:** Paket yo'qolishini nazorat qilish uchun cheksum (checksum) tekshiruvini qo'shish.
**Yechim (R):**
```r
library(digest)
# UDP paketini simulyatsiya qilish
send_udp_packet <- function(data) {
  checksum <- digest(data, algo = "crc32")
  packet <- list(payload = data, hash = checksum)
  return(packet)
}
# Ma'lumotni yuborish
packet <- send_udp_packet("Sensor_Data_001")
print(packet)
```
**Tushuntirish:** UDP ishonchsiz bo'lgani uchun, `digest` kutubxonasi orqali ma'lumot yaxlitligini tekshirish (integrity check) muhim ahamiyatga ega.

### Topshiriq #1143: HTTP/3 protokoli uchun sarlavha (Header) tahlili
**Tavsif:** HTTP/3 (QUIC asosidagi) so'rovlarida sarlavhalarni optimallashtirish va siqish.
**Talablar:** QHeader formatidagi ma'lumotlarni dekodlash va xavfsizlik uchun TLS 1.3 tekshiruvi.
**Yechim (R):**
```r
# HTTP/3 header simulyatsiyasi
parse_h3_header <- function(header_raw) {
  # QPACK dekodlash algoritmi
  headers <- strsplit(header_raw, ": ")[[1]]
  return(setNames(list(headers[2]), headers[1]))
}
# Sinov
print(parse_h3_header("authority: khorazmiy.ai"))
```
**Tushuntirish:** HTTP/3 da QPACK ishlatiladi. Ushbu funksiya sarlavhalarni tezkor ajratib olish uchun `setNames` yordamida ro'yxatga o'tkazadi.

### Topshiriq #1144: QUIC protokoli uchun ulanish identifikatori (Connection ID)
**Tavsif:** QUIC protokoli orqali ulanishni migratsiya qilishda ID boshqaruvi.
**Talablar:** Har bir sessiya uchun noyob 64-bitlik identifikator generatsiyasi.
**Yechim (R):**
```r
generate_cid <- function() {
  # 64-bitli tasodifiy identifikator
  return(paste(sample(0:9, 16, replace = TRUE), collapse = ""))
}
# Yangi ulanish ID
cat("Yangi QUIC CID:", generate_cid())
```
**Tushuntirish:** QUIC IP o'zgarganda ham ulanishni saqlab qoladi. `generate_cid` funksiyasi sessiya barqarorligini ta'minlaydi.

### Topshiriq #1145: WebSockets orqali real vaqtda yangilanish
**Tavsif:** Veb-interfeys va R serveri o'rtasida ikki tomonlama aloqa o'rnatish.
**Talablar:** `httpuv` paketidan foydalanib, WebSocket hodisalarini (events) boshqarish.
**Yechim (R):**
```r
library(httpuv)
app <- list(
  onWSOpen = function(ws) {
    ws$onMessage(function(binary, message) {
      ws$send(paste("Javob:", message))
    })
  }
)
# runServer("0.0.0.0", port = 5000, app = app)
```
**Tushuntirish:** `httpuv` asinxron ishlash imkonini beradi, bu esa WebSocket orqali yuqori tezlikdagi ma'lumot almashinuvini ta'minlaydi.

### Topshiriq #1146: TCP soketida "Keep-Alive" mexanizmi
**Tavsif:** Uzoq muddatli ulanishlarda soket uzilib qolmasligi uchun "Keep-Alive" signallarini yuborish.
**Talablar:** Har 30 soniyada "ping" yuborish funksiyasi.
**Yechim (R):**
```r
send_keep_alive <- function(socket) {
  write.socket(socket, "PING")
  cat("Keep-alive yuborildi...\n")
}
# Soketni tekshirish
# Sys.sleep(30); send_keep_alive(my_socket)
```
**Tushuntirish:** Firewalllar bo'sh turgan soketlarni yopib qo'ymasligi uchun ushbu mexanizm ishlab chiqarishda juda muhim.

### Topshiriq #1147: HTTP/3 ma'lumotlar oqimini (Stream) boshqarish
**Tavsif:** Bir nechta parallel oqimlarni boshqarishda resurslarni taqsimlash.
**Talablar:** Oqimlar sonini limitlash (max_streams = 100).
**Yechim (R):**
```r
manage_streams <- function(current_streams) {
  if (current_streams < 100) {
    return("Yangi oqim ochildi")
  } else {
    stop("Oqim limitiga yetildi!")
  }
}
print(manage_streams(50))
```
**Tushuntirish:** QUIC/HTTP/3 da oqimlar sonini nazorat qilish server xotirasini himoya qiladi.

### Topshiriq #1148: WebSocket xavfsizlik tokeni (WSS)
**Tavsif:** WebSocket ulanishini autentifikatsiya qilish.
**Talablar:** JWT (JSON Web Token) orqali ulanishni tasdiqlash.
**Yechim (R):**
```r
verify_ws_token <- function(token) {
  # Tokenni dekodlash va tekshirish
  secret <- "Khorazmiy_Secret_2024"
  return(token == secret)
}
# Ulanishni tekshirish
print(verify_ws_token("Khorazmiy_Secret_2024"))
```
**Tushuntirish:** WSS (Secure WebSocket) ulanishida token tekshiruvi ruxsatsiz kirishlarning oldini oladi.

### Topshiriq #1149: UDP paketlar ketma-ketligini tiklash
**Tavsif:** UDP orqali kelgan paketlar tartibsiz bo'lsa, ularni indeks bo'yicha saralash.
**Talablar:** Paketlar indekslangan ro'yxatni qayta tartiblash.
**Yechim (R):**
```r
reorder_packets <- function(packets) {
  # Paketlarni ID bo'yicha saralash
  packets[order(sapply(packets, function(x) x$id))]
}
# Misol: list(list(id=2), list(id=1)) -> list(id=1), list(id=2)
```
**Tushuntirish:** UDP paketlari turli yo'llar bilan kelishi mumkin, `order` funksiyasi ma'lumotlar yaxlitligini tiklaydi.

### Topshiriq #1150: Tarmoq protokoli loglarini tahlil qilish
**Tavsif:** Server loglaridan protokol xatolarini aniqlash.
**Talablar:** `tidyverse` yordamida noto'g'ri soket ulanishlarini filtrlash.
**Yechim (R):**
```r
library(dplyr)
log_data <- data.frame(status = c("OK", "ERR", "OK", "TIMEOUT"))
errors <- log_data %>% filter(status != "OK")
print(errors)
```
**Tushuntirish:** `dplyr` kutubxonasi katta hajmdagi log fayllarini tezkor tahlil qilish uchun eng samarali vositadir.