# Khorazmiy AI: Ruby - Modul 23
## Mavzu: Tarmoq protokollari: TCP/UDP soketlari, HTTP/3, QUIC va WebSockets

### Topshiriq #1101: TCP Soket yordamida xavfsiz ma'lumot uzatish
**Tavsif:** TCP soketlari orqali mijoz va server o'rtasida ma'lumot almashinuvini amalga oshirish. Real tizimlarda bu ma'lumotlar oqimini boshqarish va ulanishni to'g'ri yopishni talab qiladi.
**Talablar:** `TCPServer` va `TCPSocket` klasslaridan foydalanish, ulanishni `ensure` bloki orqali yopish.
**Yechim (Ruby):**
```ruby
require 'socket'

# Server qismi
server = TCPServer.new('127.0.0.1', 8080)
puts "Server 8080-portda ishga tushdi..."

loop do
  Thread.start(server.accept) do |client|
    begin
      message = client.gets.chomp
      client.puts "Qabul qilindi: #{message.reverse}" # Ma'lumotni teskari qaytarish
    ensure
      client.close # Ulanishni xavfsiz yopish
    end
  end
end
```
**Tushuntirish:** `Thread` ishlatilishi bir vaqtning o'zida bir nechta mijozga xizmat ko'rsatish imkonini beradi, `ensure` esa xatolik yuz berganda ham xotira sizib chiqishining oldini oladi.

### Topshiriq #1102: UDP orqali ma'lumotlar paketi (Datagram) uzatish
**Tavsif:** UDP protokoli tezkorlik talab qilinadigan (masalan, real vaqt rejimidagi o'yinlar yoki loglar) tizimlar uchun zarur.
**Talablar:** `UDPSocket` klassidan foydalanish, ma'lumotlar yo'qolishi ehtimolini hisobga olish.
**Yechim (Ruby):**
```ruby
require 'socket'

# UDP jo'natuvchi
socket = UDPSocket.new
message = "Khorazmiy AI: Tizim holati - OK"
socket.send(message, 0, '127.0.0.1', 9000)
socket.close
```
**Tushuntirish:** UDP ulanishni talab qilmaydi (connectionless), shuning uchun `send` metodi to'g'ridan-to'g'ri manzilga paketni yuboradi. Bu tarmoq yuklamasini kamaytiradi.

### Topshiriq #1103: WebSocket orqali real vaqtda xabar almashish
**Tavsif:** HTTP protokoli doimiy so'rovlar uchun qimmatga tushadi. WebSockets doimiy ikki tomonlama aloqani ta'minlaydi.
**Talablar:** `faye-websocket` gemidan foydalanish, asinxron hodisalarni boshqarish.
**Yechim (Ruby):**
```ruby
require 'faye/websocket'

# WebSocket serveri uchun shablon
ws = Faye::WebSocket.new(env)

ws.on :message do |event|
  puts "Kelgan xabar: #{event.data}"
  ws.send("Javob: #{event.data.upcase}")
end

ws.on :close do |event|
  ws = nil
end
```
**Tushuntirish:** WebSocket ulanishni ochiq qoldiradi, bu esa serverdan mijozga ma'lumotni "push" qilish imkonini beradi.

### Topshiriq #1104: HTTP/3 (QUIC) protokoli uchun sarmoya (Wrapper)
**Tavsif:** HTTP/3 TCP o'rniga QUIC (UDP asosidagi) protokolini ishlatadi. Ruby'da buni `nghttp3` kutubxonasi orqali amalga oshirish mumkin.
**Talablar:** Protokolning past kechikish (low latency) xususiyatini ta'minlash.
**Yechim (Ruby):**
```ruby
# HTTP/3 talabi uchun pseudokod (nghttp3 gemi bilan)
require 'http3'

client = HTTP3::Client.new("https://khorazmiy.ai")
response = client.get("/")
puts response.body if response.status == 200
```
**Tushuntirish:** HTTP/3 "Head-of-line blocking" muammosini hal qiladi, bu esa tarmoq beqaror bo'lganida ham tezroq yuklanishni ta'minlaydi.

### Topshiriq #1105: Soket vaqt chegarasi (Timeout) boshqaruvi
**Tavsif:** Tarmoq muammolari tufayli soketlar "osilib" qolishi mumkin. Buni oldini olish uchun timeout o'rnatish shart.
**Talablar:** `Socket#setsockopt` yordamida vaqt chegarasini belgilash.
**Yechim (Ruby):**
```ruby
require 'socket'

socket = TCPSocket.new('127.0.0.1', 8080)
# 5 soniyalik timeout o'rnatish
timeout = [5, 0].pack("l_2")
socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_RCVTIMEO, timeout)

begin
  data = socket.read
rescue IO::WaitReadable
  puts "Vaqt tugadi!"
end
```
**Tushuntirish:** `SO_RCVTIMEO` opsiyasi tizim darajasida kutish vaqtini cheklaydi, bu esa resurslarni tejaydi.

### Topshiriq #1106: TCP oqimini (Stream) buferlash
**Tavsif:** Katta hajmdagi ma'lumotlarni uzatishda xotirani tejash uchun oqimli (stream) yondashuv zarur.
**Talablar:** `IO` klassi va bufer hajmini boshqarish.
**Yechim (Ruby):**
```ruby
# Faylni soket orqali qismlarga bo'lib yuborish
File.open("data.bin", "rb") do |file|
  while chunk = file.read(1024) # 1KB bufer
    socket.write(chunk)
  end
end
```
**Tushuntirish:** Butun faylni RAMga yuklamasdan, qismlarga bo'lib yuborish server barqarorligini oshiradi.

### Topshiriq #1107: WebSocket orqali "Heartbeat" (Ping/Pong)
**Tavsif:** Ulanish uzilib qolganini aniqlash uchun muntazam signal yuborish.
**Talablar:** `ping` mexanizmini amalga oshirish.
**Yechim (Ruby):**
```ruby
# Har 30 soniyada ping yuborish
EM.add_periodic_timer(30) do
  ws.ping("ping")
end
```
**Tushuntirish:** Heartbeat mexanizmi "ghost" ulanishlarni tozalash va tarmoq uzilishlarini tezkor aniqlash uchun muhimdir.

### Topshiriq #1108: Soket orqali JSON ma'lumotlarini serializatsiya qilish
**Tavsif:** Tarmoq orqali murakkab obyektlarni yuborish uchun JSON formatidan foydalanish.
**Talablar:** `json` kutubxonasi va xavfsiz pars qilish.
**Yechim (Ruby):**
```ruby
require 'json'

data = { status: "success", code: 200 }
socket.puts(data.to_json)

# Qabul qilish
received = JSON.parse(socket.gets)
```
**Tushuntirish:** JSON universal format bo'lib, turli dasturlash tillari o'rtasidagi o'zaro aloqani osonlashtiradi.

### Topshiriq #1109: Xavfsiz ulanish (SSL/TLS)
**Tavsif:** TCP soketlarida ma'lumotlarni shifrlash (SSL/TLS) orqali himoya qilish.
**Talablar:** `OpenSSL` kutubxonasidan foydalanish.
**Yechim (Ruby):**
```ruby
require 'socket'
require 'openssl'

tcp_sock = TCPSocket.new('khorazmiy.ai', 443)
ctx = OpenSSL::SSL::SSLContext.new
ssl_sock = OpenSSL::SSL::SSLSocket.new(tcp_sock, ctx)
ssl_sock.connect
ssl_sock.puts "GET / HTTP/1.1"
```
**Tushuntirish:** SSL/TLS ma'lumotlarning "man-in-the-middle" hujumlaridan himoyalanishini ta'minlaydi.

### Topshiriq #1110: UDP Broadcast orqali xizmatlarni topish (Service Discovery)
**Tavsif:** Lokal tarmoqda mavjud serverlarni avtomatik aniqlash.
**Talablar:** `SO_BROADCAST` opsiyasini yoqish.
**Yechim (Ruby):**
```ruby
require 'socket'

socket = UDPSocket.new
socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_BROADCAST, true)
socket.send("DISCOVER_SERVICE", 0, '<broadcast>', 9000)
```
**Tushuntirish:** Broadcast orqali tarmoqdagi barcha qurilmalarga so'rov yuboriladi, bu esa markazlashmagan tizimlarda tugunlarni topish uchun eng samarali usuldir.

---

### Topshiriq #1111: TCP Soket yordamida ma'lumotlar almashinuvi
**Tavsif:** Server va mijoz o'rtasida ishonchli ma'lumotlar oqimini ta'minlash uchun TCP soketini yaratish.
**Talablar:** `TCPServer` va `TCPSocket` kutubxonalaridan foydalanish, ulanishni yopishda xavfsizlikni ta'minlash.
**Yechim (Ruby):**
```ruby
require 'socket'

# Server tomoni
server = TCPServer.new('127.0.0.1', 8080)
puts "Server 8080-portda ishga tushdi..."

loop do
  Thread.start(server.accept) do |client|
    client.puts "Salom! Siz Khorazmiy AI serveriga ulandingiz."
    client.close # Ish tugagach ulanishni yopish
  end
end
```
**Tushuntirish:** `Thread` ishlatilishi bir vaqtning o'zida bir nechta mijozga xizmat ko'rsatish imkonini beradi (concurrency).

### Topshiriq #1112: UDP orqali tezkor xabar uzatish
**Tavsif:** TCP'ning ortiqcha tekshiruvlarisiz, tezkor ma'lumot uzatish uchun UDP protokolidan foydalanish.
**Talablar:** `UDPSocket` klassidan foydalanish, paket yo'qolishini inobatga olish.
**Yechim (Ruby):**
```ruby
require 'socket'

socket = UDPSocket.new
socket.bind('127.0.0.1', 9000)

puts "UDP server tinglamoqda..."
loop do
  text, sender = socket.recvfrom(1024) # 1024 bayt qabul qilish
  puts "Qabul qilindi: #{text} - #{sender[3]}"
end
```
**Tushuntirish:** UDP ulanishni kutmaydi, shuning uchun real vaqt rejimidagi monitoring tizimlari uchun juda samarali.

### Topshiriq #1113: WebSockets yordamida real vaqtda chat
**Tavsif:** Brauzer va server o'rtasida ikki tomonlama (full-duplex) aloqa o'rnatish.
**Talablar:** `faye-websocket` gemidan foydalanish, hodisalarga asoslangan (event-driven) arxitektura.
**Yechim (Ruby):**
```ruby
require 'faye/websocket'

# WebSocket serveri uchun asosiy mantiq
def call(env)
  if Faye::WebSocket.websocket?(env)
    ws = Faye::WebSocket.new(env)
    ws.on :message do |event|
      ws.send("Qabul qilindi: #{event.data}")
    end
    ws.rack_response
  end
end
```
**Tushuntirish:** WebSockets HTTP'ga qaraganda kamroq overhead (yuklama) talab qiladi, chunki ulanish ochiq qoladi.

### Topshiriq #1114: HTTP/3 protokoli simulyatsiyasi
**Tavsif:** QUIC protokoli ustiga qurilgan HTTP/3 ning ishlash prinsipini tushunish.
**Talablar:** `quic` gemi yoki mos keluvchi kutubxona orqali ulanishni boshlash.
**Yechim (Ruby):**
```ruby
# HTTP/3 (QUIC) ulanishini boshlash uchun abstraksiya
require 'quic' 

client = QUIC::Client.new('example.com', 443)
client.connect do |stream|
  stream.send_data("GET / HTTP/3")
  puts stream.read_data
end
```
**Tushuntirish:** HTTP/3 TCP'dagi "Head-of-line blocking" muammosini hal qiladi, bu esa tarmoq sifati past bo'lganda tezlikni oshiradi.

### Topshiriq #1115: Soketlarda xavfsizlik (SSL/TLS)
**Tavsif:** TCP soketlarida ma'lumotlarni shifrlangan holda uzatish.
**Talablar:** `OpenSSL` kutubxonasidan foydalanish, sertifikatlarni tekshirish.
**Yechim (Ruby):**
```ruby
require 'socket'
require 'openssl'

context = OpenSSL::SSL::SSLContext.new
context.cert = OpenSSL::X509::Certificate.new(File.read("server.crt"))
context.key = OpenSSL::PKey::RSA.new(File.read("server.key"))

tcp_server = TCPServer.new(4433)
ssl_server = OpenSSL::SSL::SSLServer.new(tcp_server, context)

loop do
  conn = ssl_server.accept
  conn.puts "Bu shifrlangan kanal!"
  conn.close
end
```
**Tushuntirish:** SSL/TLS ma'lumotlarni "man-in-the-middle" hujumlaridan himoya qiladi.

### Topshiriq #1116: Soket vaqt tugashi (Timeout) boshqaruvi
**Tavsif:** Soket ulanishlari osilib qolmasligi uchun vaqt limitini o'rnatish.
**Talablar:** `IO.select` yordamida kutish vaqtini cheklash.
**Yechim (Ruby):**
```ruby
require 'socket'

socket = TCPSocket.new('google.com', 80)
# 5 soniya kutish vaqti
if IO.select([socket], nil, nil, 5)
  puts "Ma'lumot keldi"
else
  puts "Vaqt tugadi!"
end
socket.close
```
**Tushuntirish:** `IO.select` bloklanmaydigan (non-blocking) I/O operatsiyalarini amalga oshirish uchun eng yaxshi usuldir.

### Topshiriq #1117: HTTP/2 Multiplexing tushunchasi
**Tavsif:** Bitta TCP ulanishida bir nechta so'rovni parallel yuborish.
**Talablar:** `http/2` gemidan foydalanish, stream'larni boshqarish.
**Yechim (Ruby):**
```ruby
require 'http/2'

conn = HTTP2::Client.new
stream = conn.new_stream
stream.on(:headers) { |h| puts "Javob keldi: #{h}" }
conn.send_data("GET / HTTP/2")
```
**Tushuntirish:** Multiplexing resurslarni yuklash vaqtini keskin kamaytiradi.

### Topshiriq #1118: Soket orqali fayl uzatish
**Tavsif:** Katta hajmdagi fayllarni soket orqali bo'laklab (chunk) uzatish.
**Talablar:** `File.read` o'rniga `read(chunk_size)` dan foydalanish.
**Yechim (Ruby):**
```ruby
# Faylni 4KB bo'laklar bilan yuborish
File.open("data.bin", "rb") do |file|
  while chunk = file.read(4096)
    socket.write(chunk)
  end
end
```
**Tushuntirish:** Xotirani tejash uchun faylni butunligicha emas, bo'laklab o'qish muhim.

### Topshiriq #1119: UDP Broadcast (Tarmoq ichida xabar tarqatish)
**Tavsif:** Bir xabar bilan tarmoqdagi barcha qurilmalarga ma'lumot yuborish.
**Talablar:** `SO_BROADCAST` opsiyasini yoqish.
**Yechim (Ruby):**
```ruby
require 'socket'

socket = UDPSocket.new
socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_BROADCAST, true)
socket.send("Khorazmiy AI: Tarmoq tekshiruvi", 0, '<broadcast>', 9000)
```
**Tushuntirish:** Broadcast tizimni avtomatik topish (service discovery) uchun ishlatiladi.

### Topshiriq #1120: Soket holatini monitoring qilish
**Tavsif:** Faol ulanishlar sonini va holatini kuzatish.
**Talablar:** `Socket` va `ObjectSpace` dan foydalanib ulanishlarni sanash.
**Yechim (Ruby):**
```ruby
def count_active_sockets
  count = 0
  ObjectSpace.each_object(TCPSocket) { |s| count += 1 unless s.closed? }
  count
end

puts "Hozirgi faol ulanishlar: #{count_active_sockets}"
```
**Tushuntirish:** `ObjectSpace` xotiradagi barcha obyektlarni kuzatish imkonini beradi, bu esa xotira sizib chiqishini (memory leak) aniqlashda yordam beradi.

---

### Topshiriq #1121: TCP Serverda "Half-Open" ulanishlarni boshqarish
**Tavsif:** Yuqori yuklamali tizimlarda mijozlar to‘satdan uzilib qolganda serverda "zombi" soketlar qolib ketadi. Buni oldini olish uchun `SO_KEEPALIVE` va timeout mexanizmini joriy etish kerak.
**Talablar:** `Socket` kutubxonasi, `setsockopt` orqali TCP keepalive sozlamalari, xatolarni qayta ishlash.
**Yechim (Ruby):**
```ruby
require 'socket'

server = TCPServer.new('0.0.0.0', 8080)
loop do
  Thread.start(server.accept) do |client|
    # TCP Keepalive sozlamalari: 60 soniya bo'sh tursa tekshir
    client.setsockopt(Socket::SOL_SOCKET, Socket::SO_KEEPALIVE, true)
    
    begin
      client.puts "Salom! Ulanish faol."
      data = client.gets
    rescue Errno::ECONNRESET, EOFError
      puts "Mijoz ulanishni uzdi."
    ensure
      client.close
    end
  end
end
```
**Tushuntirish:** `SO_KEEPALIVE` operatsion tizim darajasida ulanishni tekshiradi, bu esa resurslar isrof bo'lishining oldini oladi.

### Topshiriq #1122: UDP orqali ishonchli xabar uzatish protokoli (ACK tizimi)
**Tavsif:** UDP ulanishsiz protokol bo'lgani uchun paketlar yo'qolishi mumkin. Oddiy "Acknowledgement" (ACK) mexanizmini yaratish kerak.
**Talablar:** `UDPSocket` dan foydalanish, paket identifikatori (ID) bilan ishlash.
**Yechim (Ruby):**
```ruby
require 'socket'

socket = UDPSocket.new
socket.bind('0.0.0.0', 9000)

loop do
  message, addr = socket.recvfrom(1024)
  id, payload = message.split(':', 2)
  puts "Qabul qilindi: #{payload}"
  # ACK yuborish
  socket.send("ACK:#{id}", 0, addr[3], addr[1])
end
```
**Tushuntirish:** Har bir paketga ID berish orqali qaysi paket yetib kelganini kuzatish mumkin, bu UDP ustida ishonchli qatlam qurishning asosi.

### Topshiriq #1123: WebSocket orqali real-time xabar almashinuv
**Tavsif:** HTTP so‘rovlaridan farqli o‘laroq, WebSocket doimiy ulanishni ushlab turadi. `faye-websocket` gemi yordamida server qurish.
**Talablar:** `EventMachine` va `faye-websocket` kutubxonalari, asinxron hodisalarni boshqarish.
**Yechim (Ruby):**
```ruby
require 'faye/websocket'
require 'eventmachine'

EM.run {
  app = lambda do |env|
    if Faye::WebSocket.websocket?(env)
      ws = Faye::WebSocket.new(env)
      ws.on :message do |event|
        ws.send("Qaytarildi: #{event.data}")
      end
      ws.rack_response
    end
  end
  # Serverni ishga tushirish...
}
```
**Tushuntirish:** EventMachine asinxron I/O operatsiyalarini bloklamasdan bajarishga imkon beradi, bu minglab ulanishlarni boshqarish uchun zarur.

### Topshiriq #1124: HTTP/3 (QUIC) protokoli uchun sarlavha (Header) siqish
**Tavsif:** HTTP/3 (QUIC) da HPACK o‘rniga QPACK ishlatiladi. Kichik hajmdagi ma’lumotlarni uzatish uchun sarlavhalarni indekslash.
**Talablar:** Hash-map yordamida tezkor qidiruv, xotira samaradorligi.
**Yechim (Ruby):**
```ruby
class QPackCompressor
  def initialize
    @table = { "content-type" => 1, "user-agent" => 2 }
  end

  def compress(headers)
    headers.map { |k, v| [@table[k] || k, v] }
  end
end
```
**Tushuntirish:** Statik jadvaldan foydalanish tarmoq trafigini sezilarli darajada kamaytiradi.

### Topshiriq #1125: Soketlarda "Buffer Overflow" himoyasi
**Tavsif:** Katta hajmdagi ma’lumotlar bilan ishlashda xotira to‘lib ketmasligi uchun oqimli (stream) o‘qish.
**Talablar:** `readpartial` metodidan foydalanish, chunk hajmini cheklash.
**Yechim (Ruby):**
```ruby
def safe_read(socket, size = 1024)
  buffer = ""
  while (chunk = socket.readpartial(size))
    buffer << chunk
    break if buffer.length >= 10_000 # Maksimal limit
  end
  buffer
end
```
**Tushuntirish:** `readpartial` butun ma'lumotni kutmasdan, kelgan qismini darhol qaytaradi, bu esa xotirani tejaydi.

### Topshiriq #1126: QUIC protokoli uchun "Stream Multiplexing" simulyatsiyasi
**Tavsif:** Bitta ulanishda bir nechta mustaqil oqimlarni (streams) boshqarish.
**Talablar:** `Queue` sinfidan foydalanish, thread-safe yondashuv.
**Yechim (Ruby):**
```ruby
require 'thread'

class StreamManager
  def initialize
    @streams = Hash.new { |h, k| h[k] = Queue.new }
  end

  def push(stream_id, data)
    @streams[stream_id].push(data)
  end
end
```
**Tushuntirish:** Har bir oqim uchun alohida navbat (Queue) ajratish "Head-of-line blocking" muammosini hal qiladi.

### Topshiriq #1127: WebSocket "Ping/Pong" yurak urishi (Heartbeat)
**Tavsif:** Ulanish uzilganini aniqlash uchun muntazam signal yuborish.
**Talablar:** `Timer` mexanizmi, ulanish holatini tekshirish.
**Yechim (Ruby):**
```ruby
def setup_heartbeat(ws)
  EM.add_periodic_timer(30) do
    ws.ping("ping") { puts "Pong qabul qilindi" }
  end
end
```
**Tushuntirish:** 30 soniyalik interval server va mijoz o‘rtasidagi aloqani faol ushlab turadi.

### Topshiriq #1128: TCP soketida SSL/TLS shifrlash
**Tavsif:** Ma'lumotlarni xavfsiz uzatish uchun `OpenSSL` kutubxonasini TCP soketiga integratsiya qilish.
**Talablar:** `OpenSSL::SSL::SSLSocket` dan foydalanish.
**Yechim (Ruby):**
```ruby
require 'socket'
require 'openssl'

ctx = OpenSSL::SSL::SSLContext.new
tcp_sock = TCPSocket.new('example.com', 443)
ssl_sock = OpenSSL::SSL::SSLSocket.new(tcp_sock, ctx)
ssl_sock.connect
ssl_sock.puts "GET / HTTP/1.1"
```
**Tushuntirish:** TLS qatlami ma'lumotlarni shifrlab, "man-in-the-middle" hujumlaridan himoya qiladi.

### Topshiriq #1129: UDP Broadcast orqali xizmatni aniqlash (Service Discovery)
**Tavsif:** Mahalliy tarmoqda serverni avtomatik topish uchun UDP broadcast dan foydalanish.
**Talablar:** `SO_BROADCAST` bayrog'ini o'rnatish.
**Yechim (Ruby):**
```ruby
socket = UDPSocket.new
socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_BROADCAST, true)
socket.send("DISCOVER_SERVICE", 0, '<broadcast>', 9999)
```
**Tushuntirish:** Broadcast orqali tarmoqdagi barcha qurilmalarga so‘rov yuborish xizmatlarni avtomatik sozlash imkonini beradi.

### Topshiriq #1130: HTTP/3 uchun "0-RTT" (Zero Round Trip Time) xavfsizligi
**Tavsif:** QUIC protokoli orqali ulanish vaqtini qisqartirish uchun sessiya tiketlarini saqlash.
**Talablar:** Sessiya ma'lumotlarini keshda saqlash va tekshirish.
**Yechim (Ruby):**
```ruby
class SessionCache
  @cache = {}
  def self.save(id, data); @cache[id] = data; end
  def self.get(id); @cache[id]; end
end
# Ulanishda avvalgi sessiya ID sini tekshirish...
```
**Tushuntirish:** 0-RTT ulanish tezligini oshiradi, ammo "replay attack" xavfini kamaytirish uchun server tomonida validatsiya qat'iy bo'lishi kerak.

---

### Topshiriq #1131: TCP Socket orqali xavfsiz ma'lumot uzatish
**Tavsif:** Server va mijoz o'rtasida TCP soket orqali ma'lumot almashishda ma'lumotlar yaxlitligini ta'minlash.
**Talablar:** `Socket` kutubxonasidan foydalanish, xatolarni qayta ishlash (error handling) va ulanishni yopish.
**Yechim (Ruby):**
```ruby
require 'socket'

# TCP server yaratish
server = TCPServer.new('127.0.0.1', 8080)
puts "Server 8080-portda ishga tushdi..."

loop do
  Thread.start(server.accept) do |client|
    begin
      message = client.gets.chomp
      puts "Qabul qilindi: #{message}"
      client.puts "Xabar qabul qilindi: #{message.reverse}"
    rescue => e
      puts "Xatolik: #{e.message}"
    ensure
      client.close # Resurslarni bo'shatish
    end
  end
end
```
**Tushuntirish:** `Thread` ishlatilishi serverning bir vaqtning o'zida bir nechta mijoz bilan ishlashini ta'minlaydi. `ensure` bloki soketning har qanday holatda yopilishini kafolatlaydi.

### Topshiriq #1132: UDP orqali tezkor xabar almashish
**Tavsif:** Real vaqt rejimida monitoring tizimlari uchun UDP protokolidan foydalangan holda paketlar yuborish.
**Talablar:** `UDPSocket` klassidan foydalanish, paket yo'qolishiga bardoshli kod yozish.
**Yechim (Ruby):**
```ruby
require 'socket'

# UDP soketini ochish
socket = UDPSocket.new
host = '127.0.0.1'
port = 9000

# Xabar yuborish
socket.send("Monitoring: CPU 45%", 0, host, port)
puts "Paket yuborildi."
socket.close
```
**Tushuntirish:** UDP ulanishsiz protokol bo'lgani uchun `connect` talab qilinmaydi, bu esa tezlikni oshiradi.

### Topshiriq #1133: WebSocket serverini amalga oshirish
**Tavsif:** Brauzer va server o'rtasida ikki tomonlama (full-duplex) aloqa o'rnatish.
**Talablar:** `faye-websocket` gemidan foydalanish, event-driven arxitektura.
**Yechim (Ruby):**
```ruby
require 'faye/websocket'

# WebSocket serveri (EventMachine asosida)
App = lambda do |env|
  if Faye::WebSocket.websocket?(env)
    ws = Faye::WebSocket.new(env)

    ws.on :message do |event|
      ws.send("Echo: #{event.data}")
    end

    ws.rack_response
  end
end
```
**Tushuntirish:** WebSocket doimiy ulanishni ushlab turadi, bu esa HTTP so'rovlaridagi overhead'ni kamaytiradi.

### Topshiriq #1134: HTTP/3 (QUIC) protokoli simulyatsiyasi
**Tavsif:** HTTP/3 ning asosiy xususiyati bo'lgan multiplekslashni tushunish uchun UDP ustida qatlam yaratish.
**Talablar:** `quic-ruby` yoki shunga o'xshash kutubxona bilan ishlash mantig'i.
**Yechim (Ruby):**
```ruby
# QUIC protokoli uchun abstraksiya
class QuicConnection
  def initialize(host, port)
    @socket = UDPSocket.new
    @host = host
    @port = port
  end

  def send_stream(data)
    # QUIC paket formatida ma'lumotni kapsulalash
    packet = [0x01, data.length, data].pack("CNA*")
    @socket.send(packet, 0, @host, @port)
  end
end
```
**Tushuntirish:** QUIC TCP'dagi "Head-of-line blocking" muammosini hal qiladi, kodda paketlar stream sifatida boshqariladi.

### Topshiriq #1135: Soketlar uchun Timeout mexanizmi
**Tavsif:** Tarmoq kechikishlarida serverning osilib qolishini oldini olish.
**Talablar:** `IO.select` yordamida vaqt chegarasini belgilash.
**Yechim (Ruby):**
```ruby
require 'socket'

socket = TCPSocket.new('google.com', 80)
# 5 soniya kutish vaqti
if IO.select([socket], nil, nil, 5)
  puts "Ma'lumot keldi"
else
  puts "Vaqt tugadi!"
end
socket.close
```
**Tushuntirish:** `IO.select` bloklanmaydigan (non-blocking) I/O operatsiyalarini boshqarish uchun eng samarali usuldir.

### Topshiriq #1136: WebSocket orqali JSON ma'lumot uzatish
**Tavsif:** WebSocket orqali strukturaviy ma'lumotlarni (JSON) almashish.
**Talablar:** `json` kutubxonasi va WebSocket xabarlarini pars qilish.
**Yechim (Ruby):**
```ruby
require 'json'

def process_ws_message(data)
  payload = JSON.parse(data)
  puts "Foydalanuvchi: #{payload['user']}, Harakat: #{payload['action']}"
rescue JSON::ParserError
  puts "Noto'g'ri format"
end
```
**Tushuntirish:** Real loyihalarda ma'lumotlar JSON formatida uzatiladi, bu esa tizimlararo moslikni ta'minlaydi.

### Topshiriq #1137: TCP soketida SSL/TLS shifrlash
**Tavsif:** Ma'lumotlarni xavfsiz uzatish uchun `OpenSSL` qo'llash.
**Talablar:** `OpenSSL::SSL::SSLSocket` dan foydalanish.
**Yechim (Ruby):**
```ruby
require 'socket'
require 'openssl'

tcp_sock = TCPSocket.new('example.com', 443)
ctx = OpenSSL::SSL::SSLContext.new
ssl_sock = OpenSSL::SSL::SSLSocket.new(tcp_sock, ctx)
ssl_sock.connect

ssl_sock.puts "GET / HTTP/1.1"
puts ssl_sock.gets
ssl_sock.close
```
**Tushuntirish:** SSL/TLS transport qatlamida ma'lumotlarni shifrlab, "man-in-the-middle" hujumlaridan himoya qiladi.

### Topshiriq #1138: UDP Broadcast orqali xizmatlarni topish
**Tavsif:** Lokal tarmoqda mavjud serverlarni avtomatik aniqlash.
**Talablar:** `SO_BROADCAST` soket opsiyasini yoqish.
**Yechim (Ruby):**
```ruby
require 'socket'

socket = UDPSocket.new
socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_BROADCAST, true)
socket.send("DISCOVER_SERVICE", 0, '<broadcast>', 9000)
```
**Tushuntirish:** Broadcast orqali tarmoqdagi barcha qurilmalarga xabar yuboriladi, bu xizmatlarni avtomatik kashf qilishda (service discovery) muhim.

### Topshiriq #1139: HTTP/3 uchun 0-RTT (Zero Round Trip Time) tushunchasi
**Tavsif:** QUIC protokoli orqali ulanish vaqtini qisqartirish.
**Talablar:** Oldingi sessiya parametrlarini saqlash va qayta ishlatish.
**Yechim (Ruby):**
```ruby
# 0-RTT uchun sessiya kalitini saqlash
class SessionCache
  @cache = {}
  def self.save(host, key); @cache[host] = key; end
  def self.get(host); @cache[host]; end
end
```
**Tushuntirish:** 0-RTT foydalanuvchiga birinchi so'rovdayoq ma'lumot yuborish imkonini beradi, bu HTTP/3 ning asosiy tezlik afzalligidir.

### Topshiriq #1140: Soketlar uchun Buffer boshqaruvi
**Tavsif:** Katta hajmdagi ma'lumotlarni soket orqali bo'laklab (chunking) yuborish.
**Talablar:** `readpartial` metodidan foydalanish.
**Yechim (Ruby):**
```ruby
def stream_file(socket, file_path)
  File.open(file_path, 'rb') do |file|
    while chunk = file.read(4096) # 4KB bo'laklar
      socket.write(chunk)
    end
  end
end
```
**Tushuntirish:** Butun faylni xotiraga yuklash o'rniga, kichik bo'laklarda uzatish RAM resurslarini tejaydi va katta fayllar bilan ishlashda barqarorlikni ta'minlaydi.

---

### Topshiriq #1141: TCP Soket yordamida xavfsiz ma'lumot uzatish
**Tavsif:** TCP soketlari orqali mijoz va server o'rtasida ma'lumot almashishda "packet fragmentation" muammosini hal qilish va xabarlarni chegaralash.
**Talablar:** `TCPServer` va `TCPSocket` dan foydalanish, xabarlarni `\n` belgisi bilan ajratish, xatolarni qayta ishlash.
**Yechim (Ruby):**
```ruby
require 'socket'

# Server tomoni
server = TCPServer.new('127.0.0.1', 8080)
loop do
  Thread.start(server.accept) do |client|
    while (line = client.gets) # \n belgisigacha o'qiydi
      client.puts "Qabul qilindi: #{line.reverse}"
    end
    client.close
  end
end
```
**Tushuntirish:** TCP oqimga asoslangan protokol bo'lgani uchun `gets` metodi orqali ma'lumotlarni delimitator (chegaralovchi) yordamida ajratib olish xavfsiz va samarali yondashuvdir.

### Topshiriq #1142: UDP orqali yuqori tezlikdagi log yig'ish
**Tavsif:** UDP protokoli orqali ma'lumotlar yo'qolishiga yo'l qo'ymasdan, yuqori tezlikda log yuborish tizimini yaratish.
**Talablar:** `UDPSocket` dan foydalanish, bloklanmaydigan (non-blocking) rejimda ishlash.
**Yechim (Ruby):**
```ruby
require 'socket'

socket = UDPSocket.new
socket.send("Log: Tizim ishga tushdi", 0, '127.0.0.1', 9000)
# UDP ulanish talab qilmaydi, shuning uchun tezkor
```
**Tushuntirish:** UDP ulanishni kutmaydi (connectionless), bu esa real vaqt rejimida monitoring tizimlari uchun eng yuqori unumdorlikni ta'minlaydi.

### Topshiriq #1143: WebSockets yordamida real vaqt chat tizimi
**Tavsif:** `faye-websocket` gemi yordamida doimiy ulanishni saqlab turuvchi chat serverini qurish.
**Talablar:** EventMachine asosida asinxron ishlash, ulanishlarni boshqarish.
**Yechim (Ruby):**
```ruby
require 'faye/websocket'

# App ichida websocket ulanishini qabul qilish
ws = Faye::WebSocket.new(env)
ws.on :message do |event|
  ws.send("Siz yubordingiz: #{event.data}")
end
```
**Tushuntirish:** WebSockets HTTP so'rovlarining ortiqcha yuklamasini (overhead) olib tashlaydi va ikki tomonlama (full-duplex) aloqani ta'minlaydi.

### Topshiriq #1144: QUIC protokoli uchun sarmoya (Wrapper)
**Tavsif:** QUIC protokoli (HTTP/3 asosi) orqali ma'lumot uzatishda paket yo'qotilishini minimallashtirish.
**Talablar:** `quic-ruby` kutubxonasi bilan integratsiya, stream-based ma'lumot uzatish.
**Yechim (Ruby):**
```ruby
# QUIC stream yaratish
stream = connection.open_stream
stream.write("Ma'lumotlar paketi")
stream.close
```
**Tushuntirish:** QUIC TCP'dagi "Head-of-line blocking" muammosini hal qiladi, chunki har bir stream mustaqil ishlaydi.

### Topshiriq #1145: HTTP/3 (QUIC) orqali resurslarni yuklash
**Tavsif:** HTTP/3 protokoli orqali serverdan resurslarni parallel yuklab olish.
**Talablar:** Multiplexing imkoniyatidan foydalanish.
**Yechim (Ruby):**
```ruby
# HTTP/3 mijozini simulyatsiya qilish
client = HTTP3::Client.new("https://example.com")
response = client.get("/api/data")
puts response.body
```
**Tushuntirish:** HTTP/3 UDP ustiga qurilgani uchun tarmoq sifati past bo'lgan holatlarda ham barqaror ishlaydi.

### Topshiriq #1146: Soketlarda "Keep-Alive" mexanizmini joriy etish
**Tavsif:** Uzoq muddatli soket ulanishlarida "idle" (bo'sh) turgan ulanishlarni avtomatik uzish.
**Talablar:** `Socket::SO_KEEPALIVE` opsiyasidan foydalanish.
**Yechim (Ruby):**
```ruby
socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_KEEPALIVE, true)
```
**Tushuntirish:** Bu resurslarni tejaydi va "zombi" ulanishlarning server xotirasini band qilishiga yo'l qo'ymaydi.

### Topshiriq #1147: Soket orqali binar ma'lumotlarni serializatsiya qilish
**Tavsif:** Tarmoq orqali obyektlarni yuborishda `MessagePack` dan foydalanib trafikni kamaytirish.
**Talablar:** `msgpack` gemidan foydalanish, TCP orqali yuborish.
**Yechim (Ruby):**
```ruby
require 'msgpack'
data = { id: 1, status: 'ok' }.to_msgpack
socket.write(data)
```
**Tushuntirish:** JSON o'rniga MessagePack ishlatish tarmoq trafigini 30-40% ga qisqartiradi.

### Topshiriq #1148: Soket xavfsizligi (SSL/TLS)
**Tavsif:** TCP soketini `OpenSSL` yordamida shifrlash.
**Talablar:** Sertifikatlar bilan ishlash, `SSLSocket` klassidan foydalanish.
**Yechim (Ruby):**
```ruby
require 'openssl'
ctx = OpenSSL::SSL::SSLContext.new
ssl_socket = OpenSSL::SSL::SSLSocket.new(tcp_socket, ctx)
ssl_socket.connect
```
**Tushuntirish:** Xom TCP ma'lumotlari ochiq matn ko'rinishida bo'ladi; TLS esa ma'lumotlarni "man-in-the-middle" hujumlaridan himoya qiladi.

### Topshiriq #1149: Asinxron soket serveri (EventMachine)
**Tavsif:** Minglab bir vaqtning o'zida ulanishlarni (concurrent connections) boshqarish.
**Talablar:** `EventMachine` kutubxonasi, `Reactor` pattern.
**Yechim (Ruby):**
```ruby
require 'eventmachine'
EM.run {
  EM.start_server "0.0.0.0", 8080, Module.new {
    def receive_data(data); send_data "Qabul qilindi"; end
  }
}
```
**Tushuntirish:** EventMachine bir oqimli (single-threaded) arxitekturada juda ko'p ulanishni samarali boshqarish imkonini beradi.

### Topshiriq #1150: Soketlarda vaqt chegarasi (Timeout)
**Tavsif:** Soket ulanishlari osilib qolmasligi uchun vaqt chegarasini o'rnatish.
**Talablar:** `IO.select` yordamida kutish vaqtini nazorat qilish.
**Yechim (Ruby):**
```ruby
if IO.select([socket], nil, nil, 5) # 5 soniya kutish
  data = socket.read_nonblock(1024)
else
  raise "Vaqt tugadi!"
end
```
**Tushuntirish:** `IO.select` serverning javob bermaydigan mijozlar sababli bloklanib qolishining oldini oladi.