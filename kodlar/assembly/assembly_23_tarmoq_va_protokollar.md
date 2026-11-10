# Khorazmiy AI: Assembly - Modul 23
## Mavzu: Tarmoq protokollari: TCP/UDP soketlari, HTTP/3, QUIC va WebSockets

### Topshiriq #1101: TCP soketini ochish (Socket Creation)
**Tavsif:** Linux tizimida `socket()` tizim chaqiruvi orqali IPv4 TCP soketini yaratish. Tarmoq xizmatlari uchun poydevor.
**Talablar:** `AF_INET` (2), `SOCK_STREAM` (1), `IPPROTO_TCP` (6) parametrlaridan foydalanish.
**Yechim (Assembly):**
```assembly
section .text
global _start
_start:
    mov rax, 41        ; sys_socket
    mov rdi, 2         ; AF_INET
    mov rsi, 1         ; SOCK_STREAM
    mov rdx, 0         ; Protocol (0 = default)
    syscall            ; Soket yaratish
    ; rax da soket fayl deskriptori qaytadi
```
**Tushuntirish:** `sys_socket` chaqiruvi yadro darajasida tarmoq resursini ajratadi. 0-protokol avtomatik ravishda TCP ni tanlaydi.

### Topshiriq #1102: TCP soketini bog'lash (Bind)
**Tavsif:** Soketni ma'lum bir IP va portga (masalan, 8080) bog'lash.
**Talablar:** `sockaddr_in` strukturasi xotirada to'g'ri joylashuvi (Big-Endian port).
**Yechim (Assembly):**
```assembly
; sockaddr_in strukturasi:
; port 8080 (0x1F90 -> 0x901F)
push word 0x901F    ; Port
push word 2         ; AF_INET
push dword 0        ; INADDR_ANY (0.0.0.0)
; ... bind chaqiruvi ...
mov rax, 49         ; sys_bind
```
**Tushuntirish:** Tarmoq bayt tartibi (Network Byte Order) muhim, shuning uchun portni `bswap` qilish yoki to'g'ridan-to'g'ri teskari yozish kerak.

### Topshiriq #1103: TCP tinglash (Listen)
**Tavsif:** Kiruvchi ulanishlar uchun soketni tinglash holatiga o'tkazish.
**Talablar:** `backlog` parametrini 128 (standart) qilib belgilash.
**Yechim (Assembly):**
```assembly
mov rax, 50         ; sys_listen
mov rdi, [sockfd]   ; Soket deskriptori
mov rsi, 128        ; Backlog
syscall
```
**Tushuntirish:** `backlog` navbatdagi ulanishlar sonini belgilaydi, bu yuqori yuklamali serverlarda xavfsizlik uchun muhim.

### Topshiriq #1104: TCP ulanishni qabul qilish (Accept)
**Tavsif:** Mijozdan kelgan ulanishni qabul qilish va yangi deskriptor olish.
**Talablar:** Bloklanmaydigan rejimda ishlash imkoniyati.
**Yechim (Assembly):**
```assembly
mov rax, 43         ; sys_accept
mov rdi, [sockfd]
xor rsi, rsi        ; sockaddr = NULL
xor rdx, rdx        ; addrlen = NULL
syscall
```
**Tushuntirish:** `accept` yangi soket yaratadi, bu orqali mijoz bilan ma'lumot almashiniladi.

### Topshiriq #1105: UDP soketini yaratish
**Tavsif:** `SOCK_DGRAM` yordamida ulanishsiz (connectionless) protokolni ishga tushirish.
**Talablar:** `IPPROTO_UDP` (17) dan foydalanish.
**Yechim (Assembly):**
```assembly
mov rax, 41
mov rdi, 2          ; AF_INET
mov rsi, 2          ; SOCK_DGRAM
mov rdx, 17         ; IPPROTO_UDP
syscall
```
**Tushuntirish:** UDP tezkor, ammo ishonchsiz, shuning uchun xatolarni qayta ishlash dastur darajasida bo'lishi kerak.

### Topshiriq #1106: HTTP/3 (QUIC) uchun UDP paket yuborish
**Tavsif:** QUIC protokoli uchun `sendto` tizim chaqiruvidan foydalanish.
**Talablar:** Manzil (sockaddr) ko'rsatilishi shart.
**Yechim (Assembly):**
```assembly
mov rax, 44         ; sys_sendto
mov rdi, [sockfd]
mov rsi, buffer     ; Ma'lumot manzili
mov rdx, len        ; Uzunlik
mov r10, 0          ; Flags
syscall
```
**Tushuntirish:** QUIC UDP ustiga qurilgani uchun `sendto` orqali paketlar yuboriladi.

### Topshiriq #1107: WebSocket handshake (Handshake)
**Tavsif:** HTTP so'rovini WebSocket'ga yangilash (Upgrade header).
**Talablar:** `Sec-WebSocket-Key` ni qayta ishlash.
**Yechim (Assembly):**
```assembly
; HTTP GET so'rovini bufferga yozish
mov rax, 1          ; sys_write
mov rdi, [sockfd]
mov rsi, http_req   ; "GET / HTTP/1.1..."
mov rdx, req_len
syscall
```
**Tushuntirish:** WebSocket - bu HTTP orqali boshlanadigan ikki tomonlama TCP ulanishdir.

### Topshiriq #1108: Soketni yopish (Close)
**Tavsif:** Resurslarni bo'shatish va ulanishni uzish.
**Talablar:** Xotira sizishining oldini olish.
**Yechim (Assembly):**
```assembly
mov rax, 3          ; sys_close
mov rdi, [sockfd]
syscall
```
**Tushuntirish:** Har bir ochilgan soket fayl deskriptori yopilishi shart, aks holda OS resurslari tugaydi.

### Topshiriq #1109: Ma'lumot qabul qilish (Recv)
**Tavsif:** TCP soketidan ma'lumot o'qish.
**Talablar:** Buffer to'lib qolishidan himoya qilish.
**Yechim (Assembly):**
```assembly
mov rax, 45         ; sys_recvfrom
mov rdi, [sockfd]
mov rsi, buffer
mov rdx, 1024       ; Buffer hajmi
xor r10, r10
syscall
```
**Tushuntirish:** `recv` chaqiruvi ma'lumot kelguncha kutib turadi (bloklaydi).

### Topshiriq #1110: Soket opsiyalarini sozlash (Setsockopt)
**Tavsif:** `SO_REUSEADDR` ni yoqish (server qayta ishga tushganda port band bo'lmasligi uchun).
**Talablar:** `SOL_SOCKET` darajasida ishlash.
**Yechim (Assembly):**
```assembly
mov rax, 54         ; sys_setsockopt
mov rdi, [sockfd]
mov rsi, 1          ; SOL_SOCKET
mov rdx, 2          ; SO_REUSEADDR
syscall
```
**Tushuntirish:** Bu parametr serverni to'xtatib qayta yoqqanda "Address already in use" xatosini oldini oladi.

---

### Topshiriq #1111: TCP Soketini Ochish (Socket Syscall)
**Tavsif:** Linux tizimida tarmoq aloqasini boshlash uchun `socket()` tizim chaqiruvini amalga oshirish.
**Talablar:** `AF_INET` (IPv4) va `SOCK_STREAM` (TCP) parametrlarini to'g'ri o'rnatish.
**Yechim (Assembly):**
```assembly
section .text
global _start
_start:
    mov eax, 41         ; sys_socket
    mov edi, 2          ; AF_INET
    mov esi, 1          ; SOCK_STREAM
    mov edx, 0          ; Protocol 0
    syscall             ; Soket fayl deskriptorini yaratish
    mov edi, eax        ; Natijani saqlash
    mov eax, 60         ; sys_exit
    xor edi, edi
    syscall
```
**Tushuntirish:** `socket()` chaqiruvi tarmoq stekini ishga tushiradi. Registerlardan foydalanish xotira sarfini kamaytiradi.

### Topshiriq #1112: TCP Soketini Bog'lash (Bind)
**Tavsif:** Soketni ma'lum bir port va IP manzilga bog'lash.
**Talablar:** `sockaddr_in` strukturasi xotirada to'g'ri joylashishi shart.
**Yechim (Assembly):**
```assembly
; sockaddr_in strukturasi: AF_INET(2), Port(8080), IP(0.0.0.0)
push 0                  ; INADDR_ANY
push word 0x1F90        ; Port 8080 (big-endian)
push word 2             ; AF_INET
mov rsi, rsp            ; Strukturaga ko'rsatkich
mov eax, 49             ; sys_bind
syscall
```
**Tushuntirish:** Port raqami tarmoq bayt tartibida (big-endian) bo'lishi shart, shuning uchun `0x1F90` ishlatildi.

### Topshiriq #1113: UDP Soketida Ma'lumot Yuborish
**Tavsif:** `sendto()` yordamida UDP orqali xabar uzatish.
**Talablar:** Ulanishsiz (connectionless) protokol xususiyatlarini hisobga olish.
**Yechim (Assembly):**
```assembly
mov eax, 44             ; sys_sendto
mov edi, [sockfd]       ; Soket FD
mov rsi, msg            ; Xabar manzili
mov rdx, 10             ; Xabar uzunligi
mov r10, 0              ; Flags
mov r8, sockaddr_ptr    ; Manzil
mov r9, 16              ; Manzil uzunligi
syscall
```
**Tushuntirish:** UDPda `sendto` har bir paket uchun manzilni talab qiladi, bu esa xavfsizlik va tezlik balansini ta'minlaydi.

### Topshiriq #1114: HTTP/3 (QUIC) Header Parsing
**Tavsif:** QUIC paketlaridagi "Long Header" qismini tahlil qilish.
**Talablar:** Bitwise operatsiyalar yordamida paket turini aniqlash.
**Yechim (Assembly):**
```assembly
mov al, [packet_byte]
and al, 0x80            ; Header Form bitini tekshirish
cmp al, 0x80
je is_long_header       ; Agar 1 bo'lsa, Long Header
jmp is_short_header
```
**Tushuntirish:** QUIC protokoli tezlik uchun bit-darajasidagi tekshiruvlarga tayanadi, bu kod eng yuqori unumdorlikni beradi.

### Topshiriq #1115: WebSocket Handshake (Sec-WebSocket-Key)
**Tavsif:** WebSocket ulanishini tasdiqlash uchun Base64 kodlashni simulyatsiya qilish.
**Talablar:** ASCII belgilarni 6-bitli indekslarga o'tkazish.
**Yechim (Assembly):**
```assembly
mov al, [input_char]
shr al, 2               ; Birinchi 6 bitni ajratish
mov rbx, base64_table
xlatb                   ; Jadvaldan mos belgini olish
```
**Tushuntirish:** `xlatb` instruksiyasi tarjima jadvallari bilan ishlashda eng tezkor usul hisoblanadi.

### Topshiriq #1116: Soketni Tinglash (Listen)
**Tavsif:** Server rejimida kiruvchi ulanishlarni kutish.
**Talablar:** `backlog` parametrini 128 qilib belgilash.
**Yechim (Assembly):**
```assembly
mov eax, 50             ; sys_listen
mov edi, [sockfd]
mov esi, 128            ; Backlog hajmi
syscall
```
**Tushuntirish:** `backlog` navbatdagi ulanishlar sonini belgilaydi, bu DDoS hujumlariga qarshi dastlabki himoya.

### Topshiriq #1117: TCP Ulanishini Qabul Qilish (Accept)
**Tavsif:** `accept()` orqali yangi mijoz ulanishini qabul qilish.
**Talablar:** Yangi soket deskriptorini qaytarish.
**Yechim (Assembly):**
```assembly
mov eax, 43             ; sys_accept
mov edi, [sockfd]
xor esi, esi            ; sockaddr = NULL
xor edx, edx            ; addrlen = NULL
syscall
mov [client_fd], eax    ; Mijoz soketini saqlash
```
**Tushuntirish:** `accept` bloklanuvchi chaqiruv bo'lib, ulanish kelguncha jarayonni kutish holatiga o'tkazadi.

### Topshiriq #1118: Ma'lumotlarni Qabul Qilish (Recv)
**Tavsif:** Soketdan buferga ma'lumot o'qish.
**Talablar:** Bufer to'lib qolishining oldini olish (Buffer Overflow).
**Yechim (Assembly):**
```assembly
mov eax, 45             ; sys_recvfrom
mov edi, [client_fd]
mov rsi, buffer
mov rdx, 1024           ; Maksimal hajm
xor r10, r10
syscall
```
**Tushuntirish:** `rdx` orqali bufer hajmini cheklash xavfsizlik uchun muhimdir.

### Topshiriq #1119: Soketni Yopish (Close)
**Tavsif:** Resurslarni bo'shatish uchun soketni yopish.
**Talablar:** Xatolarni tekshirish va deskriptorni tozalash.
**Yechim (Assembly):**
```assembly
mov eax, 3              ; sys_close
mov edi, [sockfd]
syscall
```
**Tushuntirish:** Resurslar sizib chiqishini (leak) oldini olish uchun har bir soket yopilishi shart.

### Topshiriq #1120: QUIC Stream ID Tekshiruvi
**Tavsif:** QUIC protokolidagi Stream ID toq yoki juftligini aniqlash.
**Talablar:** `test` instruksiyasi yordamida samarali tekshiruv.
**Yechim (Assembly):**
```assembly
mov rax, [stream_id]
test rax, 1             ; Oxirgi bitni tekshirish
jnz is_client_initiated ; Agar 1 bo'lsa, mijoz boshlagan
; Server boshlagan
```
**Tushuntirish:** `test` instruksiyasi `cmp` ga qaraganda tezroq ishlaydi va bayroqlarni to'g'ridan-to'g'ri o'rnatadi.

---

### Topshiriq #1121: TCP Soketini Ochish (Socket Syscall)
**Tavsif:** Linux tizimida `socket()` tizim chaqiruvi orqali IPv4 TCP soketini yaratish. Tarmoq dasturlashning poydevori.
**Talablar:** `AF_INET` (2), `SOCK_STREAM` (1) va `IPPROTO_TCP` (6) parametrlaridan foydalanish.
**Yechim (Assembly):**
```assembly
section .text
global _start
_start:
    mov eax, 41         ; sys_socket
    mov edi, 2          ; AF_INET
    mov esi, 1          ; SOCK_STREAM
    mov edx, 6          ; IPPROTO_TCP
    syscall             ; Soket yaratish
    ; EAXda soket fayl deskriptori qaytadi
    mov eax, 60         ; sys_exit
    xor edi, edi
    syscall
```
**Tushuntirish:** `syscall` raqami 41 (x64) orqali yadroga to'g'ridan-to'g'ri murojaat qilindi. Bu eng past darajadagi operatsiya bo'lib, xotira sarfini minimal darajada ushlaydi.

### Topshiriq #1122: TCP Soketini Bog'lash (Bind)
**Tavsif:** Yaratilgan soketni ma'lum bir port va IP manzilga bog'lash.
**Talablar:** `sockaddr_in` strukturasini to'g'ri to'ldirish (Little-endian tartibida).
**Yechim (Assembly):**
```assembly
; sockaddr_in strukturasini stekda tayyorlash
push 0              ; INADDR_ANY (0.0.0.0)
push word 0x5000    ; Port 80 (0x50)
push word 2         ; AF_INET
mov rsi, rsp        ; Struktura manzili
mov rdx, 16         ; Struktura hajmi
mov eax, 49         ; sys_bind
syscall
```
**Tushuntirish:** Port raqami `htons` (host to network short) formatida bo'lishi shart, shuning uchun 80 porti `0x5000` shaklida yozildi.

### Topshiriq #1123: UDP Soketida Ma'lumot Yuborish (sendto)
**Tavsif:** Ulanishsiz (connectionless) UDP protokoli orqali paket yuborish.
**Talablar:** `sendto` chaqiruvidan foydalanish, xavfsizlik uchun bufer chegaralarini tekshirish.
**Yechim (Assembly):**
```assembly
mov eax, 44         ; sys_sendto
mov edi, [sockfd]   ; Soket deskriptori
mov rsi, buffer     ; Yuboriladigan ma'lumot
mov rdx, 10         ; Hajmi
mov r10, 0          ; Flags
mov r8, sockaddr    ; Manzil
mov r9, 16          ; Manzil hajmi
syscall
```
**Tushuntirish:** UDPda `connect` shart emas, shuning uchun har bir paket uchun manzil ko'rsatilishi kerak. Bu tezkor ma'lumot uzatish uchun optimallashtirilgan.

### Topshiriq #1124: HTTP/3 uchun QUIC Header Parsing
**Tavsif:** QUIC paketlaridagi "Short Header" qismini ajratib olish.
**Talablar:** Bitwise operatsiyalar yordamida paket turini aniqlash.
**Yechim (Assembly):**
```assembly
mov al, [packet]    ; Paketning birinchi bayti
and al, 0x40        ; QUIC short header flagini tekshirish
jz .long_header     ; Agar 0 bo'lsa, long header
; Short header logikasi shu yerda
.long_header:
; Long header logikasi
```
**Tushuntirish:** QUIC protokoli tezlikni oshirish uchun bit-maskalardan foydalanadi. Assembly'dagi `AND` operatsiyasi eng tezkor tekshiruv usulidir.

### Topshiriq #1125: WebSocket Handshake (Sec-WebSocket-Key)
**Tavsif:** WebSocket ulanishini boshlash uchun HTTP headerini tahlil qilish.
**Talablar:** String solishtirish va xotira xavfsizligi.
**Yechim (Assembly):**
```assembly
mov rsi, header_ptr
mov rdi, key_string
mov rcx, 24         ; Kalit uzunligi
repe cmpsb          ; Stringlarni solishtirish
je .valid_handshake
```
**Tushuntirish:** `repe cmpsb` ko'rsatmasi CPU darajasida string solishtirishni tezlashtiradi, bu esa yuqori yuklamali serverlar uchun muhim.

### Topshiriq #1126: TCP Listen (Kutish rejimi)
**Tavsif:** Soketni kiruvchi ulanishlarni qabul qilish holatiga o'tkazish.
**Talablar:** `backlog` parametrini 128 (standart) qilib belgilash.
**Yechim (Assembly):**
```assembly
mov eax, 50         ; sys_listen
mov edi, [sockfd]
mov esi, 128        ; Backlog hajmi
syscall
```
**Tushuntirish:** `listen` chaqiruvi operatsion tizimga ushbu soket orqali ulanishlar navbatini boshqarishni buyuradi.

### Topshiriq #1127: Accept (Ulanishni qabul qilish)
**Tavsif:** Navbatdagi ulanishni qabul qilib, yangi deskriptor olish.
**Talablar:** Bloklanmaydigan (non-blocking) rejimni hisobga olish.
**Yechim (Assembly):**
```assembly
mov eax, 43         ; sys_accept
mov edi, [sockfd]
xor esi, esi        ; sockaddr = NULL
xor edx, edx        ; addrlen = NULL
syscall
; EAXda yangi client soketi
```
**Tushuntirish:** `accept` chaqiruvi yangi mijoz bilan muloqot qilish uchun alohida kanal (deskriptor) ajratib beradi.

### Topshiriq #1128: HTTP/3 Stream ID Extraction
**Tavsif:** QUIC oqimlarida Stream ID ni ajratib olish.
**Talablar:** Varint (Variable-length integer) dekodlash.
**Yechim (Assembly):**
```assembly
mov al, [rsi]       ; Birinchi baytni o'qish
test al, 0x80       ; 1-bitni tekshirish
jz .single_byte     ; Agar 0 bo'lsa, 1 baytli ID
; Ko'p baytli ID logikasi
```
**Tushuntirish:** QUIC protokoli xotirani tejash uchun o'zgaruvchan uzunlikdagi integerlardan foydalanadi. Assembly'da `test` va `jz` orqali tarmoq oqimini samarali pars qilish mumkin.

### Topshiriq #1129: TCP Soketini yopish (Close)
**Tavsif:** Resurslarni bo'shatish uchun soketni yopish.
**Talablar:** Xatolarni boshqarish (error handling).
**Yechim (Assembly):**
```assembly
mov eax, 3          ; sys_close
mov edi, [sockfd]
syscall
test eax, eax       ; Xatolikni tekshirish
js .error_handler
```
**Tushuntirish:** `sys_close` chaqiruvi yadro darajasida fayl deskriptorini o'chiradi va tarmoq resursini bo'shatadi.

### Topshiriq #1130: WebSocket Data Framing
**Tavsif:** WebSocket ma'lumotlarini yuborish uchun "Frame" formatlash.
**Talablar:** Fin bit va Opcode qo'shish.
**Yechim (Assembly):**
```assembly
mov byte [buffer], 0x81 ; FIN=1, Opcode=Text (0x1)
mov byte [buffer+1], 0x05 ; Payload uzunligi
; Ma'lumotni bufferga yozish
```
**Tushuntirish:** WebSocket protokoli har bir paket boshiga 2 baytli header qo'shishni talab qiladi. Assembly'da bu `mov` operatsiyalari bilan eng tez bajariladi.

---

### Topshiriq #1131: TCP Soketini Ochish (Socket Creation)
**Tavsif:** Linux x86_64 tizimida `socket()` tizim chaqiruvi orqali IPv4 TCP soketini yaratish. Tarmoq dasturlashning poydevori.
**Talablar:** `AF_INET` (2), `SOCK_STREAM` (1), `IPPROTO_TCP` (6) parametrlarini to'g'ri o'rnatish.
**Yechim (Assembly):**
```assembly
section .text
global _start
_start:
    mov rax, 41          ; sys_socket
    mov rdi, 2           ; AF_INET
    mov rsi, 1           ; SOCK_STREAM
    mov rdx, 6           ; IPPROTO_TCP
    syscall              ; Soket yaratish
    mov rdi, rax         ; Soket deskriptorini saqlash
    mov rax, 60          ; sys_exit
    xor rdi, rdi
    syscall
```
**Tushuntirish:** `rax` registriga 41 yuklanib, `syscall` orqali kernelga soket yaratish buyrug'i berildi. Bu eng past darajadagi tarmoq ulanishini boshlash usulidir.

### Topshiriq #1132: TCP Soketini Bog'lash (Bind)
**Tavsif:** Yaratilgan soketni ma'lum bir port (masalan, 8080) va IP manzilga bog'lash.
**Talablar:** `sockaddr_in` strukturasi xotirada to'g'ri joylashuvi (Big-Endian formatida).
**Yechim (Assembly):**
```assembly
; sockaddr_in strukturasi:
; sin_family: 2 (word), sin_port: 8080 (word, big-endian), sin_addr: 0 (dword)
push 0               ; INADDR_ANY
push word 0x1F1F     ; Port 8080 (0x1F90)
push word 2          ; AF_INET
mov rsi, rsp         ; Strukturaga ko'rsatkich
mov rdx, 16          ; addrlen
mov rax, 49          ; sys_bind
syscall
```
**Tushuntirish:** Port raqami tarmoq bayt tartibida (network byte order) bo'lishi shart, shuning uchun `0x1F90` qiymati ishlatildi.

### Topshiriq #1133: TCP Tinglash (Listen)
**Tavsif:** Soketni kiruvchi ulanishlarni qabul qilish holatiga o'tkazish.
**Talablar:** `backlog` qiymatini 128 qilib belgilash (kutilayotgan ulanishlar navbati).
**Yechim (Assembly):**
```assembly
mov rax, 50          ; sys_listen
mov rsi, 128         ; backlog
syscall
```
**Tushuntirish:** `sys_listen` chaqiruvi soketni passiv holatga o'tkazadi, bu server dasturlari uchun majburiy bosqichdir.

### Topshiriq #1134: UDP Soketini Yaratish
**Tavsif:** `SOCK_DGRAM` yordamida ulanishsiz (connectionless) UDP soketini yaratish.
**Talablar:** Protokol turi 17 (UDP) bo'lishi shart.
**Yechim (Assembly):**
```assembly
mov rax, 41          ; sys_socket
mov rdi, 2           ; AF_INET
mov rsi, 2           ; SOCK_DGRAM
mov rdx, 17          ; IPPROTO_UDP
syscall
```
**Tushuntirish:** UDP tezkor ma'lumot uzatish uchun ishlatiladi, shuning uchun `SOCK_DGRAM` tanlandi.

### Topshiriq #1135: HTTP/3 (QUIC) uchun Soket Tayyorlash
**Tavsif:** QUIC protokoli UDP ustiga qurilgani uchun UDP soketini `non-blocking` rejimga o'tkazish.
**Talablar:** `fcntl` tizim chaqiruvi orqali `O_NONBLOCK` bayrog'ini o'rnatish.
**Yechim (Assembly):**
```assembly
mov rax, 72          ; sys_fcntl
mov rsi, 4           ; F_SETFL
mov rdx, 2048        ; O_NONBLOCK
syscall
```
**Tushuntirish:** QUIC protokoli asinxron ishlashni talab qiladi, shuning uchun soketni bloklanmaydigan rejimga o'tkazish muhim.

### Topshiriq #1136: Ma'lumotlarni Yuborish (Send)
**Tavsif:** Soket orqali "Hello" xabarini yuborish.
**Talablar:** Buffer manzili va uzunligini to'g'ri uzatish.
**Yechim (Assembly):**
```assembly
mov rax, 44          ; sys_sendto
mov rsi, buffer      ; Xabar manzili
mov rdx, 5           ; Uzunlik
xor r10, r10         ; flags
syscall
```
**Tushuntirish:** `sys_sendto` UDP va TCP uchun universal yuborish funksiyasidir.

### Topshiriq #1137: Ma'lumotlarni Qabul Qilish (Recv)
**Tavsif:** Soketdan kelayotgan paketni bufferga o'qish.
**Talablar:** Xavfsizlik uchun buffer chegarasini (buffer overflow oldini olish) nazorat qilish.
**Yechim (Assembly):**
```assembly
mov rax, 45          ; sys_recvfrom
mov rsi, buffer      ; Buffer manzili
mov rdx, 1024        ; Max uzunlik
syscall
```
**Tushuntirish:** `rdx` da ko'rsatilgan 1024 bayt buffer hajmi xotira xavfsizligini ta'minlaydi.

### Topshiriq #1138: WebSocket Handshake (Qisman)
**Tavsif:** HTTP so'rovini tahlil qilish va "Upgrade: websocket" sarlavhasini tekshirish.
**Talablar:** String solishtirish (CMP) operatsiyasi orqali sarlavhani aniqlash.
**Yechim (Assembly):**
```assembly
lea rsi, [buffer]
mov rax, [rsi]       ; Sarlavha boshini o'qish
cmp rax, 0x5570677261647055 ; "Upgrade" so'zini tekshirish
je handshake_ok
```
**Tushuntirish:** WebSocket protokoli HTTP handshake bilan boshlanadi, bu yerda sarlavha tekshiruvi optimallashtirilgan.

### Topshiriq #1139: Soketni Yopish (Close)
**Tavsif:** Resurslarni bo'shatish uchun soket deskriptorini yopish.
**Talablar:** Deskriptor to'g'ri yopilishi va xatolik yuz bersa, uni qayta ishlash.
**Yechim (Assembly):**
```assembly
mov rax, 3           ; sys_close
mov rdi, rbx         ; Soket deskriptori
syscall
```
**Tushuntirish:** `sys_close` chaqiruvi kernel darajasida soket bilan bog'liq barcha resurslarni tozalaydi.

### Topshiriq #1140: TCP Ulanishni Qabul Qilish (Accept)
**Tavsif:** `accept()` chaqiruvi orqali kiruvchi mijoz ulanishini qabul qilish.
**Talablar:** Yangi soket deskriptorini qaytarish va uni boshqarish.
**Yechim (Assembly):**
```assembly
mov rax, 43          ; sys_accept
xor rsi, rsi         ; sockaddr = NULL
xor rdx, rdx         ; addrlen = NULL
syscall
```
**Tushuntirish:** `accept` funksiyasi yangi ulanish uchun alohida soket yaratadi, bu esa serverga bir vaqtning o'zida ko'plab mijozlarga xizmat ko'rsatish imkonini beradi.

---

### Topshiriq #1141: TCP Soketini Ochish (Socket Creation)
**Tavsif:** Linux tizimida `socket()` tizim chaqiruvi orqali IPv4 TCP soketini yaratish. Tarmoq dasturlashning asosi.
**Talablar:** `AF_INET` (2), `SOCK_STREAM` (1), `IPPROTO_TCP` (6) konstantalaridan foydalanish.
**Yechim (Assembly):**
```assembly
section .text
    mov rax, 41          ; sys_socket
    mov rdi, 2           ; AF_INET
    mov rsi, 1           ; SOCK_STREAM
    mov rdx, 6           ; IPPROTO_TCP
    syscall              ; Soket fayl deskriptori RAX da qaytadi
```
**Tushuntirish:** `syscall 41` to'g'ridan-to'g'ri kernelga murojaat qiladi. Registrlarni tozalash va to'g'ri konstantalarni uzatish xavfsizlik uchun muhim.

### Topshiriq #1142: TCP Bog'lanish (Connect)
**Tavsif:** Uzoq masofadagi serverga 80-port orqali ulanish.
**Talablar:** `sockaddr_in` strukturasini to'g'ri to'ldirish (Little-endian tartibida).
**Yechim (Assembly):**
```assembly
    ; sockaddr_in strukturasini stackga joylash
    push 0x0100007f      ; 127.0.0.1 (IP)
    push word 0x5000     ; 80 port (byte-swapped)
    push word 2          ; AF_INET
    mov rsi, rsp         ; Strukturaga ko'rsatkich
    mov rax, 42          ; sys_connect
    syscall
```
**Tushuntirish:** Port raqami `htons` (host to network short) formatida bo'lishi shart, shuning uchun 80 (0x50) 0x5000 ko'rinishida yozildi.

### Topshiriq #1143: UDP Paketini Yuborish (Sendto)
**Tavsif:** `sendto` orqali UDP protokoli yordamida ma'lumot uzatish.
**Talablar:** `sendto` tizim chaqiruvi (44) va manzil strukturasini boshqarish.
**Yechim (Assembly):**
```assembly
    mov rax, 44          ; sys_sendto
    mov rdi, [sockfd]    ; Soket deskriptori
    mov rsi, buffer      ; Ma'lumot manzili
    mov rdx, 10          ; Hajmi
    mov r10, 0           ; Flags
    mov r8, sockaddr     ; Manzil
    mov r9, 16           ; Manzil uzunligi
    syscall
```
**Tushuntirish:** UDP ulanishsiz (connectionless) bo'lgani uchun har bir paketda manzil ko'rsatilishi shart.

### Topshiriq #1144: HTTP/3 Header Sarlavhasini Tayyorlash
**Tavsif:** QUIC protokoli ustida HTTP/3 sarlavhalarini qadoqlash.
**Talablar:** QPACK formatidagi statik jadvaldan foydalanish.
**Yechim (Assembly):**
```assembly
    mov rax, 0x3a6d6568  ; ":hem" (method)
    mov [rdi], rax       ; Sarlavha qismini xotiraga yozish
    ; QPACK kodlash mantiqi bu yerda davom etadi
```
**Tushuntirish:** HTTP/3 tezligi uchun sarlavhalarni ikkilik formatda qadoqlash (QPACK) muhim, bu CPU sikllarini tejaydi.

### Topshiriq #1145: QUIC Stream ID Tekshiruvi
**Tavsif:** QUIC paketlarida Stream ID ning toq yoki juftligini aniqlash.
**Talablar:** Bitwise operatsiyalar orqali tezkor tekshirish.
**Yechim (Assembly):**
```assembly
    mov rax, [stream_id]
    test rax, 1          ; Oxirgi bitni tekshirish
    jz client_stream     ; Agar 0 bo'lsa, mijoz oqimi
    ; Server oqimi mantig'i
```
**Tushuntirish:** `test` instruksiyasi `cmp` ga qaraganda tezroq ishlaydi va flaglarni o'zgartiradi.

### Topshiriq #1146: WebSocket Handshake (Base64)
**Tavsif:** `Sec-WebSocket-Key` ni SHA-1 va Base64 bilan kodlash.
**Talablar:** Xavfsizlik uchun xotira xavfsizligini ta'minlash.
**Yechim (Assembly):**
```assembly
    ; Base64 jadvali orqali konvertatsiya
    mov al, [rsi]        ; Byte ni olish
    shr al, 2            ; 6 bitni ajratish
    mov bl, [base64_table + rax]
```
**Tushuntirish:** WebSocket handshake jarayoni xavfsizlik uchun standartlashtirilgan, Base64 jadvali xotirada tezkor qidiruv uchun indekslangan.

### Topshiriq #1147: TCP Receive (recv)
**Tavsif:** Soketdan kelayotgan ma'lumotlarni buferga qabul qilish.
**Talablar:** `sys_recvfrom` (45) yordamida ma'lumotlarni o'qish.
**Yechim (Assembly):**
```assembly
    mov rax, 45          ; sys_recvfrom
    mov rdi, [sockfd]
    mov rsi, buffer
    mov rdx, 1024        ; Maksimal uzunlik
    xor r10, r10         ; Flags
    syscall
```
**Tushuntirish:** `xor r10, r10` registrlarni tozalashning eng samarali usuli hisoblanadi.

### Topshiriq #1148: QUIC Paketini Shifrlash (Dummy)
**Tavsif:** QUIC paketining "payload" qismini XOR shifrlash.
**Talablar:** Kalit (key) uzunligi 16 bayt bo'lishi shart.
**Yechim (Assembly):**
```assembly
encrypt_loop:
    mov al, [rsi]
    xor al, [key + rcx]
    mov [rdi + rcx], al
    inc rcx
    cmp rcx, 16
    jne encrypt_loop
```
**Tushuntirish:** QUIC protokoli TLS 1.3 ni talab qiladi, bu yerda oddiy XOR shifrlash tushuncha uchun keltirilgan.

### Topshiriq #1149: Soketni Yopish (Close)
**Tavsif:** Resurslar sizib chiqishini oldini olish uchun soketni yopish.
**Talablar:** `sys_close` (3) chaqiruvi.
**Yechim (Assembly):**
```assembly
    mov rax, 3           ; sys_close
    mov rdi, [sockfd]    ; Deskriptor
    syscall
```
**Tushuntirish:** Har bir ochilgan soket yopilishi shart, aks holda "file descriptor leak" yuzaga keladi.

### Topshiriq #1150: Tarmoq Byte Tartibini O'zgartirish (Endianness)
**Tavsif:** Host tartibidan (Little-endian) tarmoq tartibiga (Big-endian) o'tish.
**Talablar:** `bswap` instruksiyasidan foydalanish.
**Yechim (Assembly):**
```assembly
    mov rax, [port]      ; 0x5000 (80)
    bswap rax            ; 0x00000050
    shr rax, 48          ; 0x50 (80)
```
**Tushuntirish:** X86 arxitekturasi Little-endian, tarmoq protokollari esa Big-endian. `bswap` eng tezkor usuldir.