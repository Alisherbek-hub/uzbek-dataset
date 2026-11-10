# -*- coding: utf-8 -*-
"""
Ruby 23-modul: 1126 dan 1150 gacha bo'lgan topshiriqlar
Falcon ilg'or amaliyotlar, BSD Soketlar va ActionCable real-time arxitekturasi
"""

TASKS_1126_1150 = [
    {
        "id": 1126,
        "title": "Falcon yordamida Server-Sent Events (SSE) serveri",
        "desc": "Falcon HTTP/2 serverida brauzerlarga uzoq davom etuvchi hodisalar oqimini (SSE) har bir foydalanuvchi uchun alohida thread ochmasdan yetkazish zarur.",
        "req": "`text/event-stream` sarlavhasini qaytarish, `Async` doirasida bo'laklarni uzatuvchi cheksiz oqim (Streaming Body).",
        "code": """# frozen_string_literal: true
require 'async'

class FalconSseServerApp
  def call(env)
    return [404, {}, []] unless env['PATH_INFO'] == '/events'

    body = Async::HTTP::Body::Writable.new

    # Alohida Fiberda hodisalarni generatsiya qilish
    Async do |task|
      5.times do |i|
        task.sleep 1.0
        payload = "data: {\\\"time\\\": \\\"#{Time.now.iso8601}\\\", \\\"count\\\": #{i + 1}}\\n\\n"
        body.write(payload)
      end
      body.close
    end

    [
      200,
      {
        'content-type' => 'text/event-stream',
        'cache-control' => 'no-cache',
        'connection' => 'keep-alive'
      },
      body
    ]
  end
end""",
        "expl": "Falcon `Async::HTTP::Body::Writable` orqali Rack 3 spetsifikatsiyasining to'liq asinxron oqimini taqdim etadi. `body.write()` chaqirilganda, faqatgina ma'lumot bor paytda Fiber uyg'onadi, boshqa vaqtda esa nol xotira va CPU sarfi bilan ulanish yillab ochiq turishi mumkin."
    },
    {
        "id": 1127,
        "title": "Ko'p yadroli tizimlarda Falcon klaster konfiguratsiyasi (Container / Fork modeli)",
        "desc": "Katta yuklamali ishlab chiqarish (production) serverida serverning barcha CPU yadrolaridan (masalan 8 yadro) maksimal foydalanish uchun Falcon klasterini sozlash lozim.",
        "req": "`falcon.rb` konfiguratsiyasi, jarayonlar soni (`count = Etc.nprocessors`), `preload` va xotira boshqaruvi.",
        "code": """# frozen_string_literal: true
# falcon.rb konfiguratsiya fayli

require 'etc'

service 'app' do
  # CPU yadrolari soniga teng jarayonlar (fork) yaratish
  count Etc.nprocessors

  endpoint Async::HTTP::Endpoint.parse('http://0.0.0.0:3000')

  # Ilovani xotiraga oldindan yuklash (Copy-On-Write tejamkorligi)
  preload 'config/environment.rb'
end""",
        "expl": "Falcon ning klaster modeli 'Multi-Process + Asynchronous Fiber' gibrid arxitekturasidir. Har bir CPU yadrosida bitta Nginx uslubidagi master-worker forki ishlaydi va har bir worker ichida o'n minglab Fiberlar bir vaqtda I/O so'rovlarini qayta ishlaydi. Bu Ruby ning GIL (Global VM Lock) cheklovini to'liq chetlab o'tadi."
    },
    {
        "id": 1128,
        "title": "Falcon bilan WebSockets serveri: asinxron ulanishlarni minimal xotira bilan ushlab turish",
        "desc": "Falcon serverida bir vaqtning o'zida 50 000 ta faol WebSocket ulanishlarini server xotirasi to'lib ketmasdan qabul qilish va xabarlar almashinuvini ta'minlash kerak.",
        "req": "`async-websocket` integratsiyasi, HTTP `Upgrade: websocket` ni qabul qilish va asinxron dupleks sikl.",
        "code": """# frozen_string_literal: true
require 'async-websocket'

class FalconWebSocketApp
  def call(env)
    if Async::WebSocket::Adapters::Rack.websocket?(env)
      Async::WebSocket::Adapters::Rack.open(env) do |connection|
        while (message = connection.read)
          puts "[FALCON WS] Qabul qilindi: #{message.to_str}"
          # Orqaga echo xabar yuborish
          connection.write("Echo: #{message.to_str}")
        end
      end
    else
      [200, { 'content-type' => 'text/plain' }, ['Oddiy HTTP so\\'rov']]
    end
  end
end""",
        "expl": "Puma yoki boshqa thread-based serverlarda har bir WebSocket ulanishi 1 ta operatsion tizim oqimini (thread) bloklab turadi. Falcon da esa 50 000 ta WebSocket ulanishi atigi 50 000 ta Fiber demakdir va ular Linux epoll mexanizmida xotirada passiv turadi."
    },
    {
        "id": 1129,
        "title": "Falcon orqali Early Hints (HTTP 103) yuborish va frontend aktivlarini erta yuklash",
        "desc": "Backend ma'lumotlar bazasidan murakkab SQL so'rovini hisoblayotgan 200 ms vaqt oralig'ida, brauzer bekor o'tirmasligi uchun unga HTTP 103 Early Hints orqali CSS/JS havolalarini oldindan berish lozim.",
        "req": "`env['rack.early_hints']` dan foydalanish, 103 sarlavhalarini chiqarish va asosiy 200 javobini qaytarish.",
        "code": """# frozen_string_literal: true

class EarlyHintsApp
  def call(env)
    # Brauzerga darhol 103 Early Hints sarlavhasini yuboramiz
    if env['rack.early_hints']
      env['rack.early_hints'].call({
        'link' => '</assets/application.css>; rel=preload; as=style, </assets/main.js>; rel=preload; as=script'
      })
    end

    # Og'ir bazaviy hisob-kitob simulyatsiyasi
    sleep 0.2

    # Asosiy javob (200 OK)
    [
      200,
      { 'content-type' => 'text/html' },
      ['<html><head><title>Khorazmiy</title></head><body>Sahifa yuklandi!</body></html>']
    ]
  end
end""",
        "expl": "HTTP 103 Early Hints - web unumdorlikning eng yangi standartidir. Server yakuniy HTML ni hisoblab bo'lguniga qadar, brauzer tarmoq orqali CSS va shriftlarni yuklab olishni boshlaydi. Falcon HTTP/2 da buni tabiiy ravishda qo'llab-quvvatlaydi."
    },
    {
        "id": 1130,
        "title": "Falcon server monitoringi: Prometheus metrikalari va xotira oqishini (memory leak) aniqlash",
        "desc": "Falcon serverida ishlayotgan faol Fiberlar soni, xotira sarfi va HTTP so'rovlar statistikasini Prometheus formatida kuzatib borish kerak.",
        "req": "`/metrics` marshrutini ochish, `GC.stat` va `Async::Task.current` ko'rsatkichlarini hisoblash.",
        "code": """# frozen_string_literal: true

class FalconPrometheusMetrics
  def call(env)
    return [404, {}, []] unless env['PATH_INFO'] == '/metrics'

    gc_stats = GC.stat
    live_objects = gc_stats[:heap_live_slots]
    allocated_objects = gc_stats[:total_allocated_objects]

    metrics = <<~PROMETHEUS
      # HELP ruby_heap_live_slots Hozirda tirik obyektlar soni
      # TYPE ruby_heap_live_slots gauge
      ruby_heap_live_slots #{live_objects}

      # HELP ruby_total_allocated_objects Jami ajratilgan obyektlar
      # TYPE ruby_total_allocated_objects counter
      ruby_total_allocated_objects #{allocated_objects}
    PROMETHEUS

    [200, { 'content-type' => 'text/plain; version=0.0.4' }, [metrics]]
  end
end""",
        "expl": "Asinxron serverlarda xotira sizib chiqishi (Memory Leak) ko'pincha global kontekstlarda tozalab ketilmagan Fiber yoki callbacklar sababli yuzaga keladi. `GC.stat[:heap_live_slots]` ko'rsatkichini Prometheus orqali kuzatish anomaliyalarni erta aniqlaydi."
    },
    {
        "id": 1131,
        "title": "Past darajali Socket va TCPServer / TCPSocket ulanishlari",
        "desc": "Tashqi kutubxonalarsiz, sof Ruby standart kutubxonasidagi BSD Soketlar yordamida yuqori unumdor TCP server va mijoz aloqasini o'rnatish lozim.",
        "req": "`TCPServer.new` dan foydalanish, ulanishlarni qabul qilish (`server.accept`), ma'lumot almashish va soketni xavfsiz yopish.",
        "code": """# frozen_string_literal: true
require 'socket'

class SimpleTcpEchoServer
  def start_server(port = 9876)
    server = TCPServer.new('127.0.0.1', port)
    puts "[TCP SERVER] 127.0.0.1:#{port} da tinglamoqda..."

    # 1 ta mijoz ulanishini qabul qilish
    client = server.accept
    puts "[TCP SERVER] Mijoz ulandi: #{client.peeraddr.inspect}"

    while (line = client.gets)
      line.strip!
      break if line == 'QUIT'

      client.puts "ECHO: #{line}"
    end

    client.close
    server.close
    puts "[TCP SERVER] Server to'xtatildi"
  end
end""",
        "expl": "Ruby dagi `TCPServer` C tilidagi `socket()`, `bind()`, `listen()` va `accept()` tizim chaqiruvlarining to'g'ridan-to'g'ri o'ramidir. Bu tarmoq dasturlashning eng quyi bazaviy asosi bo'lib, har qanday protokolni noldan yaratish imkonini beradi."
    },
    {
        "id": 1132,
        "title": "IO.select orqali ko'p sonli ulanishlarni bitta oqimda multipleksirlash",
        "desc": "Har bir mijoz uchun alohida OS thread ochmasdan, klassik `IO.select` tizim chaqiruvi yordamida bitta oqimda 100 ta soketni kuzatish kerak.",
        "req": "`IO.select([sockets], nil, nil, timeout)` dan foydalanish, tayyor soketlarni aniqlash va o'qish.",
        "code": """# frozen_string_literal: true
require 'socket'

class SelectMultiplexedServer
  def run_loop(port = 8888)
    server = TCPServer.new('127.0.0.1', port)
    sockets = [server]

    puts "[SELECT SERVER] Ishga tushdi..."
    loop do
      # IO.select: o'qishga tayyor soketlarni filtrlash
      readable, = IO.select(sockets, nil, nil, 1.0)
      next unless readable

      readable.each do |sock|
        if sock == server
          # Yangi mijoz keldi
          client = server.accept
          sockets << client
          puts "[YANGI MIJOZ] Jami faol: #{sockets.size - 1}"
        else
          # Mavjud mijozdan ma'lumot keldi
          if sock.eof?
            sock.close
            sockets.delete(sock)
            puts "[MIJOZ KETDI] Qoldi: #{sockets.size - 1}"
          else
            msg = sock.gets.strip
            sock.puts "Qabul qilindi: #{msg}"
          end
        end
      end
      break if sockets.size == 1 # Faqat server qolsa to'xtash simulyatsiyasi
    end
    server.close
  end
end""",
        "expl": "`IO.select` C tilidagi `select()` tizim chaqiruvidir. U OS yadrosiga nazoratni topshirib, ro'yxatdagi istalgan bitta soketda ma'lumot paydo bo'lgandagina dasturga signal beradi. Bu xotirani 1 ta thread hajmida tejab, ko'p mijozlarga xizmat ko'rsatishning qadimiy va ishonchli usulidir."
    },
    {
        "id": 1133,
        "title": "Noblokirovka qiluvchi soketlar (read_nonblock, write_nonblock, IO::WaitReadable)",
        "desc": "Soketdan ma'lumot o'qiyotganda agar tarmoqda hali baytlar yo'q bo'lsa, jarayon kutib turmasdan darhol boshqa ishlarni bajarishi kerak.",
        "req": "`read_nonblock` chaqirish, `IO::WaitReadable` va `IO::WaitWritable` istisnolarini ushlash.",
        "code": """# frozen_string_literal: true
require 'socket'

class NonBlockingSocketReader
  def read_safely(socket)
    buffer = String.new

    loop do
      begin
        chunk = socket.read_nonblock(4096)
        buffer << chunk
      rescue IO::WaitReadable
        # Ma'lumot hali tayyor emas, boshqa ish qilish mumkin
        puts "[KUTILMOQDA] Tarmoqda hali ma'lumot yo'q, boshqa amal bajarilmoqda..."
        IO.select([socket], nil, nil, 0.5)
        retry
      rescue EOFError
        puts "[TUGADI] Oqim to'liq o'qib bo'lindi"
        break
      end
    end

    buffer
  end
end""",
        "expl": "`read_nonblock` soketni `O_NONBLOCK` bayrog'i bilan o'qiydi. Agar ma'lumot bo'lmasa, operatsion tizim `EAGAIN` yoki `EWOULDBLOCK` qaytaradi, Ruby esa uni `IO::WaitReadable` ga o'giradi. Bu xususiyat zamonaviy event-loop kutubxonalarining (Async, EventMachine) yuragidir."
    },
    {
        "id": 1134,
        "title": "UNIX Domain Sockets orqali jarayonlararo (IPC) ultra-tezkor xabar almashinuvi",
        "desc": "Bitta server ichida joylashgan Nginx va Ruby dasturi o'rtasida TCP tarmoq steki (loopback 127.0.0.1) o'rniga tezroq bo'lgan UNIX fayl soketlari (`.sock`) orqali aloqa qilish kerak.",
        "req": "`UNIXServer.new('/tmp/app.sock')` va `UNIXSocket.new`, fayl huquqlarini tozalash va uzatish.",
        "code": """# frozen_string_literal: true
require 'socket'

class UnixDomainSocketIpc
  SOCKET_PATH = '/tmp/khorazmiy_ipc.sock'

  def run_unix_ipc
    File.unlink(SOCKET_PATH) if File.exist?(SOCKET_PATH)

    server = UNIXServer.new(SOCKET_PATH)
    puts "[UNIX SOCK] Shlyuz ochildi: #{SOCKET_PATH}"

    client_thread = Thread.new do
      sleep 0.1
      sock = UNIXSocket.new(SOCKET_PATH)
      sock.puts "Salom Nginx dan Ruby ga!"
      response = sock.gets
      puts "[CLIENT QABUL QILDI]: #{response}"
      sock.close
    end

    client = server.accept
    msg = client.gets
    client.puts "IPC Javob: #{msg.strip.upcase}"
    client.close

    client_thread.join
    server.close
    File.unlink(SOCKET_PATH)
  end
end""",
        "expl": "UNIX Domain Soketlari operatsion tizimning TCP/IP tarmoq stekini (cheksunlar, marshrutlash, TCP oyna hisoblashlari) butunlay chetlab o'tadi va to'g'ridan-to'g'ri operativ xotiradagi yadro buferlari orqali ishlaydi. Natijada kechikish 50% gacha kamayadi."
    },
    {
        "id": 1135,
        "title": "UDPSocket yordamida yuqori tezlikdagi telemetriya metrikalarini yig'ish tizimi",
        "desc": "O'yin serverlaridan yoki IoT qurilmalaridan sekundiga o'n minglab koordinata va telemetriya paketlarini yo'qotishga bardoshli, lekin minimal kechikish bilan qabul qilish lozim.",
        "req": "`UDPSocket.new` dan foydalanish, `bind`, `recvfrom` orqali paket va jo'natuvchi IP/portini olish.",
        "code": """# frozen_string_literal: true
require 'socket'

class UdpTelemetryReceiver
  def start_udp_listener(port = 5005)
    socket = UDPSocket.new
    socket.bind('0.0.0.0', port)
    puts "[UDP LISTENER] #{port}-portda telemetriya kutilmoqda..."

    3.times do
      data, addr = socket.recvfrom(1024)
      sender_ip = addr[3]
      sender_port = addr[1]
      puts "[UDP KELDI] [#{sender_ip}:#{sender_port}] => #{data.strip}"
    end

    socket.close
    puts "[UDP] Tinglovchi yopildi"
  end
end""",
        "expl": "UDP handshakelarsiz va ulanish holatisiz ishlaydi. U bitta paketda to'g'ridan-to'g'ri ma'lumotni yetkazadi. Agar paket yo'lda yo'qolsa ham qolgan paketlarning navbati to'xtamaydi, bu real-time monitoring uchun ayni muddao."
    },
    {
        "id": 1136,
        "title": "Binar paketlarni bit-darajasida boshqarish (Array#pack, String#unpack1)",
        "desc": "Tarmoq uskunasi bilan o'zaro ishlashda 16-bitli port raqami, 32-bitli IPv4 manzili va 8-bitli bayroqlarni binar ko'rinishda qadoqlash (pack) va yechish (unpack) talab etiladi.",
        "req": "Ruby `pack` formatlari (`n` = 16-bit network endian, `N` = 32-bit network endian, `C` = 8-bit unsigned char) dan foydalanish.",
        "code": """# frozen_string_literal: true

class NetworkBinaryCodec
  # Sarlavha: [Type (1 bayt)] [Flags (1 bayt)] [Length (2 bayt)] [Sequence (4 bayt)]
  PACK_FORMAT = 'CCnN'

  def encode_header(type, flags, length, seq)
    [type, flags, length, seq].pack(PACK_FORMAT)
  end

  def decode_header(binary_data)
    type, flags, length, seq = binary_data.unpack(PACK_FORMAT)
    {
      type: type,
      flags: flags,
      payload_length: length,
      sequence: seq
    }
  end
end

codec = NetworkBinaryCodec.new
raw_bytes = codec.encode_header(1, 0b00000010, 256, 100_500)
puts "Binar sarlavha hajmi: #{raw_bytes.bytesize} bayt"
puts "Dekodlangan: #{codec.decode_header(raw_bytes).inspect}" """,
        "expl": "Ruby ning `Array#pack` va `String#unpack` metodlari C darajasida ishlaydi va binar tarmoq oqimlarini o'ta tez qayta ishlaydi. Tarmoq baytlar tartibi (Big-Endian) uchun `n` va `N` formatlari ishlatiladi."
    },
    {
        "id": 1137,
        "title": "OpenSSL::SSL::SSLSocket orqali xavfsiz shifrlangan TLS aloqa o'rnatish",
        "desc": "Past darajadagi `TCPSocket` ni `OpenSSL::SSL::SSLSocket` ga o'rab, xavfsiz TLS shifrlash qatlamini qo'lda o'rnatish va server sertifikatini tekshirish lozim.",
        "req": "`SSLContext` yaratish, `SSLSocket.new(tcp_socket, context)`, `connect` chaqirib TLS handshake o'tkazish.",
        "code": """# frozen_string_literal: true
require 'socket'
require 'openssl'

class LowLevelTlsClient
  def connect_secure(host, port = 443)
    tcp_socket = TCPSocket.new(host, port)

    ctx = OpenSSL::SSL::SSLContext.new
    ctx.verify_mode = OpenSSL::SSL::VERIFY_PEER
    ctx.set_params

    ssl_socket = OpenSSL::SSL::SSLSocket.new(tcp_socket, ctx)
    ssl_socket.hostname = host # SNI (Server Name Indication)
    ssl_socket.connect

    puts "[TLS O'RNATILDI] Shifr: #{ssl_socket.cipher.first}, Versiya: #{ssl_socket.ssl_version}"

    # Oddiy HTTP GET
    ssl_socket.puts "GET / HTTP/1.1\\r\\nHost: #{host}\\r\\nConnection: close\\r\\n\\r\\n"
    response_status = ssl_socket.gets
    puts "[JAVOB]: #{response_status.strip}"

    ssl_socket.close
  end
end""",
        "expl": "TLS soketlari ma'lumotlarni tarmoqqa uzatishdan oldin apparat darajasida AES/GCM algoritmlari bilan shifrlaydi. `ssl_socket.hostname = host` qatori SNI uchun o'ta muhim bo'lib, to'g'ri virtual server sertifikatini olishni ta'minlaydi."
    },
    {
        "id": 1138,
        "title": "Soket darajasidagi parametrlar (setsockopt: SO_REUSEADDR, TCP_NODELAY, SO_KEEPALIVE)",
        "desc": "Server qayta ishga tushirilganda 'Address already in use' xatosini yo'qotish va paketlarni yig'masdan (Nagle algoritmini o'chirib) darhol jo'natish uchun soket opsiyalarini sozlash kerak.",
        "req": "`setsockopt` orqali `SOL_SOCKET, SO_REUSEADDR`, `IPPROTO_TCP, TCP_NODELAY` opsiyalarini o'rnatish.",
        "code": """# frozen_string_literal: true
require 'socket'

class TunedTcpSocket
  def configure_high_perf_socket(socket)
    # 1. Server qayta yonganda kutmasdan portni darhol band qilish
    socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_REUSEADDR, true)

    # 2. Nagle algoritmini o'chirish (Kichik paketlar kechikmasdan darhol ketsin)
    socket.setsockopt(Socket::IPPROTO_TCP, Socket::TCP_NODELAY, 1)

    # 3. Ulanish tirikligini OS darajasida tekshirish
    socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_KEEPALIVE, true)

    # 4. Yuborish buferi hajmini 128 KB ga oshirish
    socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_SNDBUF, 128 * 1024)

    puts "[SOKET OPTIMIZATSIYASI] TCP_NODELAY va SO_REUSEADDR faollashtirildi"
  end
end""",
        "expl": "`TCP_NODELAY` 200 ms gacha bo'lgan Nagle kechikishini bartaraf qiladi va interaktiv ilovalarda (o'yinlar, chatlar) javob tezligini keskin oshiradi. `SO_REUSEADDR` esa tizim muhandislariga dasturni nol kechikish bilan qayta ishga tushirishga yordam beradi."
    },
    {
        "id": 1139,
        "title": "Zero-copy fayl uzatish: IO.copy_stream va tizim resurslarini tejash",
        "desc": "Faylni diskdan tarmoq soketiga uzatishda ma'lumotlarni foydalanuvchi xotirasiga (User Space) nusxalamasdan, Linux `sendfile` tizim chaqiruvi orqali to'g'ridan-to'g'ri o'tkazish kerak.",
        "req": "`IO.copy_stream(src_file, dest_socket)` dan foydalanish, minimal xotira sarfini ko'rsatish.",
        "code": """# frozen_string_literal: true
require 'socket'
require 'tempfile'

class ZeroCopyStreamer
  def stream_file_direct(file_path, destination_io)
    File.open(file_path, 'rb') do |src|
      # IO.copy_stream to'g'ridan-to'g'ri Linux sendfile(2) tizim chaqiruvidan foydalanadi
      bytes_copied = IO.copy_stream(src, destination_io)
      puts "[ZERO-COPY] Jami #{bytes_copied} bayt apparat tezligida uzatildi"
      bytes_copied
    end
  end
end""",
        "expl": "`IO.copy_stream` Ruby ning eng kuchli yashirin imkoniyatlaridan biridir. U ma'lumotni Ruby VM xotirasiga olib kirmasdan, to'g'ridan-to'g'ri yadro darajasida (Kernel Space) disk drayveridan tarmoq kartasiga uzatadi (Zero-Copy). Bu CPU va xotira yuklamasini 90% ga kamaytiradi."
    },
    {
        "id": 1140,
        "title": "Graceful restart qobiliyatiga ega TCP server (File Descriptor passing / handover)",
        "desc": "Dastur kodi yangilanganda (deploy paytida) mavjud mijozlarning ulanishlarini uzmasdan va yangi so'rovlarni yo'qotmasdan yangi jarayonga o'tish (Zero-Downtime Restart) kerak.",
        "req": "`server.fileno` orqali soket deskriptorini olish, yangi jarayonni `spawn` qilib soketni meros qilib o'tkazish.",
        "code": """# frozen_string_literal: true
require 'socket'

class GracefulRestartServer
  def start_with_inherited_fd(inherited_fd = nil)
    server = if inherited_fd
               TCPServer.for_fd(inherited_fd)
             else
               TCPServer.new('127.0.0.1', 9999)
             end

    puts "[SERVER] Ishlamoqda, FD: #{server.fileno}"

    # Restart signali (USR2) kelganda
    Signal.trap('USR2') do
      puts "[RESTART] Yangi jarayonga FD topshirilmoqda..."
      new_pid = spawn('ruby', $PROGRAM_NAME, server.fileno.to_s, close_others: false)
      Process.detach(new_pid)
      exit(0) # Eski jarayon xavfsiz chiqadi
    end

    server
  end
end""",
        "expl": "Zero-Downtime deploysiz zamonaviy klasterlarni tasavvur qilib bo'lmaydi. Soketning fayl deskriptori (FD) operatsion tizimda ochiq qoladi va `for_fd` orqali yangi ishga tushgan Ruby jarayoniga topshiriladi, natijada birorta ham kiruvchi mijoz paketi uzilmaydi."
    },
    {
        "id": 1141,
        "title": "Rails ActionCable asoslari: ApplicationCable::Channel, subscribed, unsubscribed",
        "desc": "Rails ilovasida WebSocket kanallari orqali xonalarga obuna bo'lish, ma'lumotlarni oqimlash (streaming) va mijoz chiqqanda resurslarni tozalash talab qilinadi.",
        "req": "`ApplicationCable::Channel` dan meros olish, `stream_from`, `subscribed` va `unsubscribed` metodlarini to'g'ri yozish.",
        "code": """# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  # Mijoz WebSocket orqali ulanganda chaqiriladi
  def subscribed
    room_id = params[:room_id]
    reject unless room_id.present?

    # Maxsus xonaga oqim o'rnatish
    stream_from "chat_room_#{room_id}"
    logger.info "[ACTION CABLE] Foydalanuvchi xonaga kirdi: #{room_id}"
  end

  # Mijoz xabar yuborganida
  def speak(data)
    message_text = data['message']
    # Barcha xona a'zolariga xabarni efirga uzatish
    ActionCable.server.broadcast("chat_room_#{params[:room_id]}", {
      author: current_user.name,
      body: message_text,
      sent_at: Time.now.strftime('%H:%M')
    })
  end

  # Mijoz aloqani uzganida
  def unsubscribed
    logger.info "[ACTION CABLE] Foydalanuvchi xonadan chiqdi"
    stop_all_streams
  end
end""",
        "expl": "`ActionCable` Rails ning o'rnatilgan real-time tizimidir. `stream_from` metodi orqali xona identifikatori pub/sub magistraliga ulanadi va `ActionCable.server.broadcast` orqali barcha qatnashchilarga zudlik bilan tarqatiladi."
    },
    {
        "id": 1142,
        "title": "ActionCable orqali JWT autentifikatsiyasi va ulanish xavfsizligi (Connection#connect)",
        "desc": "WebSocket ulanishi o'rnatilayotgan paytda foydalanuvchining shaxsini tekshirish, yaroqsiz yoki muddati o'tgan JWT tokenlarni rad etish lozim.",
        "req": "`ApplicationCable::Connection` ichida `connect` metodini yozish, `identified_by :current_user`, yaroqsiz bo'lsa `reject_unauthorized_connection` chaqirish.",
        "code": """# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      self.current_user = find_verified_user
      logger.add_tags 'ActionCable', "User: #{current_user.id}"
    end

    private

    def find_verified_user
      token = request.params[:token] || request.headers['Authorization']&.split(' ')&.last
      if token.present?
        decoded = JsonWebToken.decode(token)
        if (user = User.find_by(id: decoded[:user_id]))
          return user
        end
      end

      # Autentifikatsiyadan o'ta olmasa ulanishni darhol yopish
      reject_unauthorized_connection
    end
  end
end""",
        "expl": "WebSocket ochilgandan so'ng qayta autentifikatsiya qilish qiyin, shuning uchun eng xavfsiz nuqta - bu `Connection#connect` bosqichidir. `reject_unauthorized_connection` chaqirilganda Rails soketni zudlik bilan 404/401 bilan yopadi."
    },
    {
        "id": 1143,
        "title": "Redis adapteri bilan ActionCable klasterlash va gorizontal masshtablash",
        "desc": "Ilova 5 ta alohida serverda (masalan Docker/Kubernetes podlarida) ishlayotganda, bitta serverdagi xabar boshqa serverdagi foydalanuvchilarga ham yetib borishi uchun Redis Pub/Sub adapterini sozlash lozim.",
        "req": "`cable.yml` faylida Redis adapteri va kanal prefikslarini to'g'ri belgilash.",
        "code": """# config/cable.yml
development:
  adapter: async

test:
  adapter: test

production:
  adapter: redis
  url: <%= ENV.fetch("REDIS_URL") { "redis://localhost:6379/1" } %>
  channel_prefix: khorazmiy_production_cable
  # Yuqori yuklamalar uchun ulanishlar hovuzi
  pool: 50""",
        "expl": "Rivojlanishda (development) `async` adapteri bitta jarayon ichida xotirada ishlaydi. Ishlab chiqarishda (production) esa `redis` adapteri shart: ActionCable barcha xabarlarni Redis ga `PUBLISH` qiladi va boshqa serverlar `SUBSCRIBE` orqali uni o'z mijozlariga uzatadi."
    },
    {
        "id": 1144,
        "title": "AnyCable arxitekturasi: Go/Rust gRPC server bilan Ruby Rails mantiqini bog'lash",
        "desc": "ActionCable Ruby jarayonida millionlab ulanishlarni ushlaganda xotira ko'p sarflanadi. Soketlarni ushlab turishni Go/Rust tilidagi AnyCable serveriga topshirib, biznes mantiqni gRPC orqali Rails da bajarish kerak.",
        "req": "`anycable-rails` konfiguratsiyasi, RPC handler va xabarlarni uzatish sxemasi.",
        "code": """# config/initializers/anycable.rb
AnyCable.configure do |config|
  # AnyCable Go serveri bilan gRPC ulanish porti
  config.rpc_host = '0.0.0.0:50051'

  # Redis orqali efirga uzatish (Broadcasting)
  config.redis_url = ENV.fetch('REDIS_URL', 'redis://localhost:6379/1')

  # Logging darajasi
  config.log_level = :info
end

# app/channels/chat_channel.rb AnyCable ostida o'zgarishsiz ishlayveradi!
class ChatChannel < ApplicationCable::Channel
  def subscribed
    stream_from "room_\#{params[:id]}"
  end
end""",
        "expl": "AnyCable - Ruby ekotizimining eng zo'r arxitekturaviy yechimlaridan biridir. Barcha og'ir 1 000 000 ta WebSocket soketlarini Go/Rust dagi `anycable-go` ushlaydi (juda kam RAM sarflaydi), ulanish va autentifikatsiya kerak bo'lgandagina gRPC orqali Rails ga murojaat qilinadi."
    },
    {
        "id": 1145,
        "title": "Real-time birgalikda hujjat tahrirlash (Operational Transformation / CRDT xabarlari)",
        "desc": "Google Docs uslubida bir nechta foydalanuvchilar bitta matnni bir vaqtda tahrirlayotganda matn o'zgarishlarini ActionCable orqali konfliktlarsiz sinxronlash lozim.",
        "req": "O'zgarish deltalarini (Delta / Operation) qabul qilish, versiya raqamini tekshirish va boshqa qatnashchilarga uzatish.",
        "code": """# app/channels/document_channel.rb
class DocumentChannel < ApplicationCable::Channel
  def subscribed
    @doc_id = params[:document_id]
    stream_from "document_\#{@doc_id}"
  end

  # Matn o'zgarishi: { position: 12, insert: 'Salom', delete: 0, version: 5 }
  def edit(data)
    delta = data['delta']
    doc_version = data['version']

    # Xonaning boshqa barcha a'zolariga o'zgarishni yuborish
    broadcast_to_others("document_\#{@doc_id}", {
      user_id: current_user.id,
      delta: delta,
      version: doc_version + 1
    })
  end

  private

  def broadcast_to_others(stream, payload)
    ActionCable.server.broadcast(stream, payload)
  end
end""",
        "expl": "Birgalikda tahrirlashda butun matn yuborilmaydi, balki faqatgina kichik o'zgarish operatsiyalari (Deltas: insert/delete) uzatiladi. Mijoz tomonidagi CRDT (Conflict-free Replicated Data Types) algoritmlari ushbu amallarni bir-biriga moslab, to'g'ri matnni hosil qiladi."
    },
    {
        "id": 1146,
        "title": "ActionCable orqali Presence Tracking (onlayn/oflayn foydalanuvchilar ro'yxati)",
        "desc": "Ilovada qaysi foydalanuvchilar ayni paytda tizimda onlayn ekanligini real-time ko'rsatuvchi indikator kerak.",
        "req": "Redis Sets orqali foydalanuvchilarni saqlash (`SADD`, `SREM`), ulanganda va chiqqanda boshqalarga bildirishnoma yuborish.",
        "code": """# app/channels/presence_channel.rb
class PresenceChannel < ApplicationCable::Channel
  REDIS_KEY = 'online_users_set'

  def subscribed
    stream_from 'presence_channel'
    # Foydalanuvchini onlayn ro'yxatiga qo'shish
    $redis.sadd(REDIS_KEY, current_user.id)
    broadcast_presence('online')
  end

  def unsubscribed
    # Foydalanuvchini ro'yxatdan o'chirish
    $redis.srem(REDIS_KEY, current_user.id)
    broadcast_presence('offline')
  end

  private

  def broadcast_presence(status)
    ActionCable.server.broadcast('presence_channel', {
      user_id: current_user.id,
      user_name: current_user.name,
      status: status,
      total_online: $redis.scard(REDIS_KEY)
    })
  end
end""",
        "expl": "Presence tizimida Redis to'plamlari (`Sets`) dublikatlarning oldini oladi. Agar bitta foydalanuvchi bir vaqtda noutbuk va telefondan ulansa ham, `SADD` uni faqat bitta marta hisoblaydi, ulanishlar to'liq uzilgandagina oflayn deb belgilanadi."
    },
    {
        "id": 1147,
        "title": "Xabarlarni qat'iy tartibda yetkazish va yo'qotishlarning oldini olish (ACK mexanizmi)",
        "desc": "Tarmoq beqaror bo'lganida xabarlar tushib qolishi yoki kechikib yetib kelishi mumkin. Mijoz har bir xabarni olganligini tasdiqlashi (ACK) shart.",
        "req": "Xabar ID si, mijozdan ACK kelmaguncha qayta yuborish navbatida ushlab turish.",
        "code": """# app/channels/reliable_message_channel.rb
class ReliableMessageChannel < ApplicationCable::Channel
  def subscribed
    stream_from "user_reliable_\#{current_user.id}"
  end

  # Mijoz xabarni olganini tasdiqlaydi
  def acknowledge(data)
    message_id = data['message_id']
    # Tasdiqlangan xabarni navbatdan o'chirish
    $redis.hdel("pending_acks:\#{current_user.id}", message_id)
    logger.info "[ACK QABUL QILINDI] Xabar ##{message_id}"
  end

  # Xabar yuborishda pending ro'yxatiga yozish
  def self.send_reliable(user_id, message_id, payload)
    $redis.hset("pending_acks:\#{user_id}", message_id, payload.to_json)
    ActionCable.server.broadcast("user_reliable_\#{user_id}", payload.merge(message_id: message_id))
  end
end""",
        "expl": "ACK (Acknowledgment) mexanizmi moliyaviy va muhim xabarlashuv tizimlarida qat'iy talabdir. Agar mijoz 5 soniya ichida `acknowledge` yubormasa, tizim xabarni qayta uzatadi (At-least-once delivery)."
    },
    {
        "id": 1148,
        "title": "ActionCable rate limiting va spam filtrlash",
        "desc": "Foydalanuvchilar chatga sekundiga yuzlab xabarlar yuborib boshqa qatnashchilarni bezovta qilmasligi va serverni to'ldirmasligi uchun cheklov o'rnatish lozim.",
        "req": "Redis orqali 5 soniyada maksimal 5 ta xabar chegarasini o'rnatish, limitdan oshsa xabarni rad etish.",
        "code": """# app/channels/concerns/rate_limitable.rb
module RateLimitable
  extend ActiveSupport::Concern

  def check_rate_limit!(limit = 5, period = 5)
    key = "rate_limit:cable:\#{current_user.id}"
    current_count = $redis.incr(key)
    $redis.expire(key, period) if current_count == 1

    if current_count > limit
      transmit({ error: 'Xabarlar yuborish tezligi chegarasidan oshdi. Biroz kuting!' })
      return false
    end
    true
  end
end

class ChatChannel < ApplicationCable::Channel
  include RateLimitable

  def speak(data)
    return unless check_rate_limit!(5, 5)

    # Normal xabar tarqatish...
  end
end""",
        "expl": "`transmit` metodi faqatgina so'rov yuborgan joriy mijozning o'ziga xususiy xatolik xabarini qaytaradi (boshqalarga bildirmasdan). Bu spammerning xatti-harakatini zudlik bilan to'xtatadi."
    },
    {
        "id": 1149,
        "title": "Turbo Streams va ActionCable integratsiyasi: komponentlarni real-time re-render qilish",
        "desc": "Rails 7+ Hotwire ekotizimida React yoki Vue ishlatmasdan, serverda HTML bo'lagini render qilib, ActionCable orqali to'g'ridan-to'g'ri brauzer DOM ini yangilash lozim.",
        "req": "`broadcast_replace_to` yoki `broadcast_append_to` yordamida HTML Turbo Streamlarini tarqatish.",
        "code": """# app/models/comment.rb
class Comment < ApplicationRecord
  belongs_to :post
  belongs_to :user

  # Yangi sharh yaratilganda avtomatik WebSocket orqali barcha ko'ruvchilarga uzatish
  after_create_commit do
    broadcast_append_to(
      "post_\#{post_id}_comments",
      target: "comments_list",
      partial: "comments/comment",
      locals: { comment: self }
    )
  end

  # O'chirilganda DOM dan olib tashlash
  after_destroy_commit do
    broadcast_remove_to("post_\#{post_id}_comments", target: "comment_\#{id}")
  end
end""",
        "expl": "Hotwire Turbo Streams frontend arxitekturasini soddalashtiradi. JavaScript yozmasdan, serverda HTML qismi yaratiladi va ActionCable orqali yuboriladi. Brauzer o'sha HTML ni ko'rsatilgan `target` ID dagi elementga avtomatik qo'shib qo'yadi."
    },
    {
        "id": 1150,
        "title": "Real-time monitoring paneli va ActionCable metrikalari (active connections, message throughput)",
        "desc": "Tizim ma'murlari uchun jami ulangan WebSocket mijozlar soni, sekundiga o'tayotgan xabarlar soni va CPU yuklamasini ko'rsatuvchi real-time panel yaratish kerak.",
        "req": "`ActionCable.server` metrikalarini yig'ish, har 2 soniyada admin kanaliga telemetriya translyatsiya qilish.",
        "code": """# app/channels/admin_metrics_channel.rb
class AdminMetricsChannel < ApplicationCable::Channel
  def subscribed
    reject unless current_user.admin?
    stream_from 'admin_metrics'
  end

  # Fonda davriy ishlovchi metrika tarqatuvchi vazifa
  def self.broadcast_server_stats
    stats = {
      timestamp: Time.now.to_i,
      memory_rss_mb: (`ps -o rss= -p \#{Process.pid}`.to_i / 1024),
      redis_connections: $redis.info['connected_clients'],
      active_threads: Thread.list.count
    }

    ActionCable.server.broadcast('admin_metrics', stats)
  end
end""",
        "expl": "Admin panellarida polling (har 5 soniyada GET so'rov) o'rniga ActionCable orqali doimiy metrikalar oqimi berilsa, tarmoq resurslari tejaladi va ma'murlar server holatini sekundlik aniqlikda kuzatib turishadi."
    }
]
