# Khorazmiy AI: Ruby - Modul 23
## Mavzu: Asinxron tarmoq: Async gem, Falcon HTTP/2 server, Socket va ActionCable WebSockets

### Topshiriq #1101: Async gem va Ruby 3.0+ Fiber scheduler asosidagi noblokirovka qiluvchi reaktor
**Tavsif:** Ruby ilovasida minglab parallel tarmoq so'rovlarini OS Threadlarining og'ir xotira sarfisiz (har bir thread 1-2 MB), yengil Fiberlar yordamida (har biri 4 KB) boshqarish talab etiladi.
**Talablar:** `require 'async'` dan foydalanish, `Async` blokida asinxron reaktorni ishga tushirish, noblokirovka qiluvchi uyqu (`sleep`) va tarmoq chaqiruvlarini o'tkazish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'

# Ruby 3+ Fiber Scheduler asosidagi asinxron reaktor
class AsyncReaktorMisoli
  def run_parallel_tasks
    Async do |task|
      puts "[#{Time.now.strftime('%H:%M:%S.%L')}] Asinxron reaktor ishga tushdi"

      # 1-vazifa
      task.async do
        puts "[#{Time.now.strftime('%H:%M:%S.%L')}] 1-vazifa boshlandi..."
        # Bu sleep OS threadini bloklamaydi, faqat joriy Fiberni to'xtatadi
        sleep 1.0
        puts "[#{Time.now.strftime('%H:%M:%S.%L')}] 1-vazifa yakunlandi"
      end

      # 2-vazifa
      task.async do
        puts "[#{Time.now.strftime('%H:%M:%S.%L')}] 2-vazifa boshlandi..."
        sleep 0.5
        puts "[#{Time.now.strftime('%H:%M:%S.%L')}] 2-vazifa yakunlandi"
      end

      puts "[#{Time.now.strftime('%H:%M:%S.%L')}] Asosiy oqim boshqa vazifalarni kutmoqda"
    end
    puts "[#{Time.now.strftime('%H:%M:%S.%L')}] Barcha asinxron vazifalar bajarildi"
  end
end

AsyncReaktorMisoli.new.run_parallel_tasks if __FILE__ == $PROGRAM_NAME
```
**Tushuntirish:** Ruby 3.0 da joriy qilingan Fiber Scheduler interfeysi operatsion tizimning `epoll`, `kqueue` yoki `io_uring` tizim chaqiruvlari bilan to'g'ridan-to'g'ri integratsiyalashgan. `Async` gemi ushbu schedulerni avtomatik o'rnatadi, natijada standart `sleep`, `Socket` va `IO` operatsiyalari avtomatik tarzda noblokirovka rejimiga o'tadi.

---

### Topshiriq #1102: Parallel asinxron vazifalar: Async do |task| task.async { ... } va natijalarni to'plash
**Tavsif:** Tizim bir nechta tashqi servisdan ma'lumotlarni parallel yig'ishi va barcha natijalar tayyor bo'lgach ularni bitta umumiy Hash strukturasida qaytarishi lozim.
**Talablar:** `task.async` yordamida bolalar vazifalarini ochish, har bir vazifa natijasini `wait` orqali xavfsiz olish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'

class ParallelDataFetcher
  def fetch_all_metrics
    results = {}

    Async do |parent_task|
      # Parallel so'rov 1
      user_task = parent_task.async do
        sleep 0.2
        { total_users: 15_420, active: 1_230 }
      end

      # Parallel so'rov 2
      sales_task = parent_task.async do
        sleep 0.3
        { daily_revenue_usd: 85_400, transactions: 412 }
      end

      # Parallel so'rov 3
      server_task = parent_task.async do
        sleep 0.1
        { cpu_load: '34%', ram_usage: '4.2GB' }
      end

      # Barcha natijalarni parallel bajarilgandan so'ng yig'ish
      results[:users] = user_task.wait
      results[:sales] = sales_task.wait
      results[:server] = server_task.wait
    end

    results
  end
end

metrics = ParallelDataFetcher.new.fetch_all_metrics
puts metrics.inspect
```
**Tushuntirish:** `task.async` yangi bolalar Fiberini (child fiber) yaratadi. `task.wait` chaqirilganda, agar natija tayyor bo'lmasa joriy Fiber kutadi, ammo boshqa parallel Fiberlar bajarilishda davom etadi. Umumiy kutish vaqti 0.2 + 0.3 + 0.1 = 0.6 soniya emas, balki eng uzoq davom etgan vazifa vaqti bo'lgan 0.3 soniyaga teng bo'ladi.

---

### Topshiriq #1103: Asinxron timeoutlar va kafolatlangan tozalash: task.with_timeout va ensure
**Tavsif:** Tashqi mikroxizmat 2 soniya ichida javob bermasa, qotib qolmasdan `Async::TimeoutError` xatosini ko'tarish va ochiq qolgan tarmoq soketlarini tozalash zarur.
**Talablar:** `task.with_timeout(duration)` dan foydalanish, timeout sodir bo'lganda `ensure` bloki orqali resurslarni yopish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'

class ResilientServiceCaller
  def call_with_deadline(url, timeout_sec = 2.0)
    Async do |task|
      socket_mock = { connected: true }

      begin
        task.with_timeout(timeout_sec) do
          puts "[#{url}] Ulanish boshlandi, timeout: #{timeout_sec}s"
          # Uzoq davom etuvchi simulyatsiya
          sleep 5.0
          puts "[#{url}] Javob muvaffaqiyatli qabul qilindi"
        end
      rescue Async::TimeoutError
        warn "[OGOHLANTIRISH] Chaqiruv belgilangan vaqtda (#{timeout_sec}s) yakunlanmadi!"
        nil
      ensure
        # Har qanday holatda soketni xavfsiz tozalash
        socket_mock[:connected] = false
        puts "[RESURS] Ulanish xavfsiz yopildi"
      end
    end
  end
end

ResilientServiceCaller.new.call_with_deadline('https://api.partner.com/data', 1.0)
```
**Tushuntirish:** `task.with_timeout` Fiber darajasida taymer o'rnatadi. Standart Ruby `Timeout.timeout` tizimidan farqli ravishda (u boshqa operatsion tizim oqimlarida `Thread#raise` chaqirib, xotira va holat buzilishlariga olib kelishi mumkin), `Async::TimeoutError` kooperativ rejimda xavfsiz uziladi.

---

### Topshiriq #1104: Cheklangan parallellik (Concurrency Limiting): Async::Semaphore yordamida resurslarni himoyalash
**Tavsif:** 1000 ta faylni tashqi serverga yuklash kerak, biroq tashqi server bir vaqtda 5 tadan ortiq parallel ulanish qabul qilmaydi (429 Too Many Requests xatosi bermasligi uchun).
**Talablar:** `Async::Semaphore.new(max)` dan foydalanish, semafor orqali vazifalarni navbatda ushlab turish va ruxsat berish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'async/semaphore'

class RateLimitedUploader
  def initialize(concurrency_limit = 5)
    @semaphore = Async::Semaphore.new(concurrency_limit)
  end

  def upload_batch(file_ids)
    Async do |task|
      file_ids.each do |fid|
        # Har bir fayl uchun asinxron ip ochiladi, lekin semafor uni nazorat qiladi
        @semaphore.async(parent: task) do
          puts "[Semafor: band=#{@semaphore.count}/#{@semaphore.limit}] Fayl ##{fid} yuklanmoqda..."
          sleep rand(0.1..0.4)
          puts "[Semafor] Fayl ##{fid} muvaffaqiyatli yuklandi"
        end
      end
    end
  end
end

uploader = RateLimitedUploader.new(3)
uploader.upload_batch((1..10).to_a)
```
**Tushuntirish:** `Async::Semaphore` cheklangan resurslar (masalan DB ulanishlari, tashqi API rate-limitlari) bilan ishlashda eng muhim vositadir. Agar 100 ta vazifa bo'lsa va chegara 5 ta bo'lsa, qolgan 95 ta vazifa kutish navbatiga turadi va bo'shagan o'rin bo'yicha darhol bajariladi.

---

### Topshiriq #1105: Ko'p sonli asinxron vazifalarni to'plash va kutish: Async::Barrier
**Tavsif:** Katta hajmdagi ma'lumotlar partiyasini (masalan, 50 ta mijoz hisobotini) parallel generatsiya qilib, barchasi to'liq yakunlangachgina xabar berish (Barrier synchronization) kerak.
**Talablar:** `Async::Barrier.new` dan foydalanish, `barrier.async` orqali vazifalar biriktirish, `barrier.wait` orqali umumiy to'siqda kutish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'async/barrier'

class BatchReportGenerator
  def generate_all(reports)
    barrier = Async::Barrier.new

    Async do
      reports.each do |report_name|
        barrier.async do
          puts "[Boshlandi] Hisobot: #{report_name}"
          sleep rand(0.2..0.5)
          puts "[Tayyor] Hisobot: #{report_name}"
        end
      end

      puts "[To'siq] Barcha hisobotlar tugashi kutilmoqda..."
      barrier.wait
      puts "[Muvaffaqiyat] Barcha #{reports.size} ta hisobot to'liq yakunlandi!"
    end
  end
end

generator = BatchReportGenerator.new
generator.generate_all(['Moliya-2026', 'Audit-Q1', 'Soliq-Yillik', 'Kadrlar-Oylik'])
```
**Tushuntirish:** `Async::Barrier` bir guruh vazifalarni yagona to'siqqa (barrier) birlashtiradi. Har bir vazifani alohida massivda saqlab `wait` chaqirib yurish o'rniga, `barrier.wait` barcha biriktirilgan Fiberlar tugashini kutadi. Agar biron vazifada xatolik yuz bersa, to'siq xatolikni propogatsiya qiladi.

---

### Topshiriq #1106: Asinxron xabarlar almashinuvi va kanallar: Async::Queue
**Tavsif:** Ishlab chiqaruvchi (Producer) va Iste'molchi (Consumer) arxitekturasida ma'lumotlar oqimini noblokirovka qiluvchi navbat orqali xavfsiz uzatish kerak.
**Talablar:** `Async::Queue.new` dan foydalanish, `queue.enqueue` va `queue.dequeue` orqali ma'lumot almashish, oxirida `nil` bilan to'xtatish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'async/queue'

class AsyncEventPipeline
  def start_pipeline
    queue = Async::Queue.new

    Async do |task|
      # Producer (Ishlab chiqaruvchi)
      producer = task.async do
        5.times do |i|
          msg = "Hodisa ##{i + 1} [#{Time.now.to_f}]"
          queue.enqueue(msg)
          puts "[Producer ->] Yuborildi: #{msg}"
          sleep 0.1
        end
        queue.enqueue(nil) # Tugash belgisi (Poison pill)
      end

      # Consumer (Iste'molchi)
      consumer = task.async do
        while (event = queue.dequeue)
          puts "[-> Consumer] Qayta ishlandi: #{event}"
          sleep 0.15
        end
        puts "[Consumer] Barcha hodisalar tugadi"
      end

      producer.wait
      consumer.wait
    end
  end
end

AsyncEventPipeline.new.start_pipeline
```
**Tushuntirish:** `Async::Queue` Fiber-safe navbat hisoblanadi. Navbat bo'sh bo'lganida `dequeue` chaqirilsa, iste'molchi Fiberi avtomatik uyquga ketadi va yangi element tushishi bilanoq scheduler tomonidan uyg'otiladi. Bu polling (aylanib tekshirish) CPU yuklamasini nolga tushiradi.

---

### Topshiriq #1107: Asinxron noblokirovka qiluvchi DNS yechuvchi: Async::DNS::Resolver
**Tavsif:** Standart `Resolv` yoki `Socket.getaddrinfo` butun Ruby VM jarayonini to'xtatib qo'yishi mumkin. Tarmoq trafigini tahlil qilishda asinxron DNS yechuvchi talab qilinadi.
**Talablar:** `Async::DNS::Resolver` dan foydalanish, domenlar uchun A va AAAA yozuvlarini asinxron olish, xatoliklarni qayta ishlash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'async/io'

class AsyncDnsResolver
  def resolve_domains(domains)
    Async do |task|
      domains.each do |domain|
        task.async do
          # Async ichida standart Addrinfo noblokirovka ishlaydi
          address_infos = Async::IO::Address.resolve(domain, 'https')
          ips = address_infos.map(&:ip_address).uniq
          puts "[DNS] #{domain} => #{ips.join(', ')}"
        rescue => e
          warn "[DNS XATO] #{domain} yechilmadi: #{e.message}"
        end
      end
    end
  end
end

AsyncDnsResolver.new.resolve_domains(['google.com', 'ruby-lang.org', 'github.com'])
```
**Tushuntirish:** `Async::IO::Address.resolve` Ruby 3 Fiber scheduler orqali OS ning asinxron DNS mexanizmlaridan foydalanadi. Domenlar ro'yxati parallel yuboriladi va server javoblari kelishiga qarab korutinalar o'z vaqtida uyg'onadi.

---

### Topshiriq #1108: Async::IO orqali asinxron fayl va tarmoq oqimlari (Streaming)
**Tavsif:** Katta log fayllarini o'qish yoki tarmoq soketiga ma'lumotlarni oqim shaklida (streaming) uzatishda xotirani to'ldirib yubormaslik lozim.
**Talablar:** `Async::IO::Stream` dan foydalanish, bo'laklab o'qish (`read_partial`), buferlangan yozish va flush qilish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'async/io'
require 'stringio'

class AsyncStreamProcessor
  def process_stream(input_io, output_io)
    Async do
      stream_in = Async::IO::Stream.new(input_io)
      stream_out = Async::IO::Stream.new(output_io)

      total_bytes = 0
      # 16 KB qismlar bilan oqimli o'qish
      while (chunk = stream_in.read_partial(16 * 1024))
        stream_out.write(chunk)
        stream_out.flush
        total_bytes += chunk.bytesize
      end

      puts "[STREAM] Jami #{total_bytes} bayt oqim bo'yicha uzatildi"
    end
  end
end

mock_in = StringIO.new("Khorazmiy AI - Asinxron ma'lumotlar oqimi!" * 100)
mock_out = StringIO.new
AsyncStreamProcessor.new.process_stream(mock_in, mock_out)
```
**Tushuntirish:** `Async::IO::Stream` yuqori darajadagi buferlangan I/O interfeysini taqdim etadi. `read_partial` ma'lumot kelishi bilan uni darhol qaytaradi, `flush` esa tizim soketiga baytlarni noblokirovka tarzida yozib beradi.

---

### Topshiriq #1109: Asinxron vazifalarda xatoliklarni qayta ishlash va exception propagation
**Tavsif:** Parallel ishlayotgan 10 ta vazifadan bittasida istisno (exception) yuz bersa, u butun dasturni to'satdan yiqitmasdan, oqilona qayd etilishi va boshqa vazifalar nazorat qilinishi kerak.
**Talablar:** `Async::Stop` va maxsus xatoliklarni tutish, `task.wait` dagi xatoliklarni himoyalangan blokda ushlash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'

class SafeParallelExecutor
  def run_with_fault_tolerance
    Async do |parent_task|
      task1 = parent_task.async do
        sleep 0.1
        puts "[Vazifa 1] Muvaffaqiyatli bajarildi"
        :ok_1
      end

      task2 = parent_task.async do
        sleep 0.15
        raise StandardError, "Tashqi API ulanishi uzildi!"
      end

      task3 = parent_task.async do
        sleep 0.2
        puts "[Vazifa 3] Muvaffaqiyatli bajarildi"
        :ok_3
      end

      # Natijalarni xavfsiz qabul qilish
      [task1, task2, task3].each_with_index do |t, i|
        begin
          res = t.wait
          puts "[Natija #{i + 1}]: #{res}"
        rescue => e
          warn "[XATO TUTILDI] Vazifa #{i + 1} xatosi: #{e.message}"
        end
      end
    end
  end
end

SafeParallelExecutor.new.run_with_fault_tolerance
```
**Tushuntirish:** `Async` da bolalar vazifasidagi xatolik `wait` chaqirilgan vaqtda qayta ko'tariladi (re-raised). Bu strukturalangan parallellik (Structured Concurrency) tamoyiliga to'liq mos bo'lib, xatoliklarni kutilmagan joylarda emas, balki qat'iy nazorat ostida ushlash imkonini beradi.

---

### Topshiriq #1110: Periodik fon vazifalari (Cron / Heartbeat ticker) Async siklida
**Tavsif:** Har 5 soniyada server salomatligini tekshiruvchi yoki keshni tozalovchi periodik vazifani `Async` reaktorida boshqa ishlarga to'sqinlik qilmasdan yurgizish kerak.
**Talablar:** Cheksiz sikl ichida `sleep(interval)`, `task.stop` signali bilan xavfsiz to'xtatish (graceful cancellation).
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'

class AsyncHeartbeatTicker
  def start_heartbeat(interval = 1.0, max_ticks = 3)
    Async do |task|
      ticker_task = task.async do
        tick_count = 0
        while tick_count < max_ticks
          sleep interval
          tick_count += 1
          puts "[TICKER ##{tick_count}] Server sog'lom: #{Time.now.strftime('%H:%M:%S')}"
        end
        puts "[TICKER] Belgilangan sikllar yakunlandi"
      end

      ticker_task.wait
    end
  end
end

AsyncHeartbeatTicker.new.start_heartbeat(0.5, 3)
```
**Tushuntirish:** Asinxron ticker fonda ishlayotganda OS ning boshqa threadlariga muhtoj emas. U bitta Ruby jarayoni ichida minglab boshqa mijoz so'rovlari bilan yonma-yon ishlayveradi. To'xtatish kerak bo'lganda `task.stop` chaqirilib, resurslar toza bo'shatiladi.

---

### Topshiriq #1111: Async::HTTP::Client yordamida asinxron HTTP/1.1 va HTTP/2 so'rovlari
**Tavsif:** Tashqi web-servislarga yuqori tezlikda ulanish va HTTP/2 protokoli orqali bitta soketda bir nechta so'rovlarni o'tkazish talab etiladi.
**Talablar:** `Async::HTTP::Client` dan foydalanish, `Async::HTTP::Endpoint` ni sozlash, GET so'rovini yuborish va status kodini tekshirish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'async/http/client'
require 'async/http/endpoint'

class AsyncHttpClientDemo
  def fetch_web_page(target_url)
    Async do
      endpoint = Async::HTTP::Endpoint.parse(target_url)
      client = Async::HTTP::Client.new(endpoint)

      begin
        response = client.get('/')
        puts "[HTTP STATUS] #{response.status}"
        body_text = response.read
        puts "[JAVOB UZUNLIGI] #{body_text.bytesize} bayt"
        body_text
      ensure
        client.close
      end
    end
  end
end

# AsyncHttpClientDemo.new.fetch_web_page('https://www.ruby-lang.org')
```
**Tushuntirish:** `Async::HTTP::Client` Ruby uchun eng zamonaviy HTTP/2 mijozidir. U ulanishlarni ochiq saqlaydi va HTTP/2 multipleksirlashidan foydalanadi, natijada har safar yangi TCP ulanish ochmasdan yuzlab so'rovlar parallel uzatiladi.

---

### Topshiriq #1112: Katta hajmdagi HTTP javob tanasini oqimli (Streaming response body) qabul qilish
**Tavsif:** Katta fayllarni (masalan, 100 MB hajmdagi zip arxiv) yuklab olishda butun faylni xotiraga yig'ib RAM ni to'ldirmasdan, diskka qismlab (chunked streaming) yozish lozim.
**Talablar:** `response.body.read` orqali bo'laklarni olish, faylga oqim shaklida yozish, xotira sarfini doimiy nazorat qilish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'async/http/client'
require 'async/http/endpoint'

class StreamingFileDownloader
  def download_stream(url, output_path)
    Async do
      endpoint = Async::HTTP::Endpoint.parse(url)
      client = Async::HTTP::Client.new(endpoint)

      begin
        response = client.get('/')
        File.open(output_path, 'wb') do |file|
          # Har bir bo'lak kelganda uni diskka yozish
          response.each do |chunk|
            file.write(chunk)
            print '.' # Progress belgisi
          end
        end
        puts "\n[YUKLANDI] Fayl saqlandi: #{output_path}"
      ensure
        client.close
      end
    end
  end
end
```
**Tushuntirish:** OpenResty dagi kabi, Ruby `Async::HTTP` ham `response.each` bloki orqali oqimli o'qishni ta'minlaydi. Fayl qanchalik ulkan bo'lmasin, dastur xotirasida faqat joriy bo'lak (masalan 16KB) ushlab turiladi, bu esa Garbage Collector yengil ishlashini ta'minlaydi.

---

### Topshiriq #1113: 1000 ta URL uchun asinxron web scraper va tezlik chegarasi (Rate limit)
**Tavsif:** Katta qidiruv tizimi yoki ma'lumotlar bazasi uchun 1000 ta saytni skanerlashda serverga ortiqcha yuklama bermasdan, maksimal 20 ta parallel ulanish bilan ishlash zarur.
**Talablar:** `Async::Semaphore` va `Async::Barrier` ni birlashtirish, URL larni o'qish, xatoliklarni qayd etish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'async/barrier'
require 'async/semaphore'

class MassWebScraper
  def initialize(concurrency = 10)
    @semaphore = Async::Semaphore.new(concurrency)
    @barrier = Async::Barrier.new
  end

  def scrape_urls(urls)
    results = {}

    Async do
      urls.each do |url|
        @semaphore.async(parent: @barrier) do
          # Simulyatsiya qilingan HTTP so'rov
          sleep rand(0.05..0.15)
          results[url] = :scraped_successfully
          puts "[SCRAPED] #{url}"
        rescue => e
          results[url] = "Xato: #{e.message}"
        end
      end

      @barrier.wait
    end

    results
  end
end

urls = (1..20).map { |n| "https://catalog.example.uz/item/#{n}" }
MassWebScraper.new(5).scrape_urls(urls)
```
**Tushuntirish:** Semafor va To'siq (Barrier) kombinatsiyasi yirik masshtabli asinxron arxitekturaning klassik namunasidir. Semafor bir vaqtda 5 tadan ortiq Fiber ishlamasligini nazorat qilsa, Barrier barcha 20 ta vazifa to'liq yakunlangachgina boshqaruvni keyingi bosqichga topshiradi.

---

### Topshiriq #1114: Asinxron Webhook yuboruvchi agent (Exponential backoff va retry bilan)
**Tavsif:** To'lov amalga oshirilganda mijozning serveriga webhook bildirishnomasini yuborish kerak. Agar mijoz serveri band bo'lsa, 3 marta kechikish bilan qayta urinish lozim.
**Talablar:** Maksimal urinishlar (3 marta), eksponentsial pauza (`sleep(delay * 2**attempt)`), muvaffaqiyatsiz bo'lsa logga yozish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'

class AsyncWebhookDispatcher
  def send_webhook(target_url, payload, max_retries = 3)
    Async do
      attempt = 0
      success = false

      while attempt < max_retries && !success
        attempt += 1
        begin
          puts "[Urinish ##{attempt}] Webhook yuborilmoqda: #{target_url}"
          # Tarmoq chaqiruvi simulyatsiyasi
          if attempt < 3
            raise StandardError, "Ulanish rad etildi (Connection Refused)"
          end
          puts "[YUBORILDI] Webhook muvaffaqiyatli yetkazildi!"
          success = true
        rescue => e
          warn "[XATO] Webhook yetkazilmadi: #{e.message}"
          if attempt < max_retries
            backoff_delay = 0.2 * (2**(attempt - 1))
            puts "[KUTISH] #{backoff_delay}s dan keyin qayta urinish..."
            sleep backoff_delay
          end
        end
      end

      success
    end
  end
end

AsyncWebhookDispatcher.new.send_webhook('https://merchant.uz/api/callback', { order_id: 9912 })
```
**Tushuntirish:** Asinxron webhook jo'natish orqali to'lov tranzaksiyasini yakunlagan asosiy mijoz veb-sahifasi tashqi mijozning sekin ishlayotgan serveri tufayli kutib qolmaydi. Barcha qayta urinishlar fondagi Fiberda mustaqil amalga oshadi.

---

### Topshiriq #1115: HTTP/2 ulanishlarida ulanishlarni multipleksirlash (Multiplexing & Connection Pooling)
**Tavsif:** Bitta mikroxizmat serveriga yuzlab API so'rovlarini jo'natishda HTTP/1.1 kabi har safar alohida TCP ochmasdan, HTTP/2 ning Streams imkoniyatidan foydalanish lozim.
**Talablar:** `Async::HTTP::Endpoint` ni HTTP/2 protokoli bilan ochish, bitta klient orqali parallel 10 ta so'rovni o'tkazish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'async/barrier'

class Http2MultiplexerDemo
  def run_multiplexed_calls(url_list)
    Async do |task|
      barrier = Async::Barrier.new
      puts "[HTTP/2] Bitta umumiy ulanish oqimi ochildi"

      url_list.each_with_index do |url, idx|
        barrier.async do
          # Bitta soket ichidagi parallel stream simulyatsiyasi
          sleep 0.1
          puts "[Stream ##{idx + 1}] Bajarildi: #{url}"
        end
      end

      barrier.wait
      puts "[HTTP/2] Barcha streamlar yagona TCP RTT doirasida yakunlandi"
    end
  end
end

Http2MultiplexerDemo.new.run_multiplexed_calls(%w[/users /orders /products /invoices])
```
**Tushuntirish:** HTTP/2 ning inqilobiy yutug'i bitta TCP ulanish ichida ikki tomonlama mustaqil oqimlarni (Streams) multipleksirlashidir. Head-of-line blocking muammosi yo'qoladi va tarmoq trafigi keskin kamayadi.

---

### Topshiriq #1116: async-websocket yordamida noblokirovka qiluvchi WebSocket mijozi
**Tavsif:** Tashqi real-time xizmatga WebSocket orqali ulanib, kiruvchi xabarlarni asinxron tinglash va kerak bo'lganda buyruqlar jo'natish zarur.
**Talablar:** `async-websocket` yoki `Async::WebSocket::Client` mantiqidan foydalanish, ulanish, xabar kutish sikli va yopish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'

class AsyncWebSocketClientSim
  def connect_and_listen(ws_url)
    Async do |task|
      puts "[WS] Ulanish o'rnatildi: #{ws_url}"

      # Xabarlarni qabul qiluvchi oqim
      listener = task.async do
        3.times do |i|
          sleep 0.2
          puts "[WS XABAR KELDI] Yangi narx: BTC = $#{65_000 + i * 150}"
        end
      end

      # Xabar jo'natuvchi oqim
      sender = task.async do
        sleep 0.1
        puts "[WS YUBORILDI] Obuna buyrug'i: {'action':'subscribe'}"
      end

      sender.wait
      listener.wait
      puts "[WS] Sessiya xavfsiz yakunlandi"
    end
  end
end

AsyncWebSocketClientSim.new.connect_and_listen('wss://stream.crypto.uz/ws')
```
**Tushuntirish:** `async-websocket` to'liq Fiber asosida qurilgan bo'lib, xabar kelishini kutayotganda hech qanday tizim ipini band qilmaydi. Bu bitta Ruby jarayonida yuzlab tashqi WebSocket kanallarini bir vaqtda kuzatib borish imkonini beradi.

---

### Topshiriq #1117: Asinxron Server-Sent Events (SSE) iste'molchisi
**Tavsif:** Tashqi yangiliklar yoki birja serveridan kelayotgan SSE (text/event-stream) oqimini to'xtatmasdan o'qib, har bir `data:` hodisasini darhol qayta ishlash kerak.
**Talablar:** `data:` qatorlarini ajratish, hodisa nomlarini tekshirish, uzilish yuz berganda qayta ulanish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'stringio'

class AsyncSseConsumer
  def consume_events(stream_io)
    Async do
      puts "[SSE] Hodisalar oqimi tinglanmoqda..."
      stream_io.each_line do |line|
        line.strip!
        next if line.empty? || line.start_with?(':') # Izohlarni o'tkazib yuborish

        if line.start_with?('data:')
          payload = line.sub(/^data:\s*/, '')
          puts "[HODISA QABUL QILINDI]: #{payload}"
        end
      end
      puts "[SSE] Oqim yakunlandi"
    end
  end
end

mock_sse = StringIO.new("data: Foydalanuvchi tizimga kirdi\n\ndata: Yangi buyurtma #402\n\n")
AsyncSseConsumer.new.consume_events(mock_sse)
```
**Tushuntirish:** SSE HTTP protokoli ustiga qurilgan bir tomonlama matnli oqimdir. Asinxron Ruby da har bir satr kelishi bilan o'qiladi va xotirani band qilmasdan real-time tizimlarga uzatiladi.

---

### Topshiriq #1118: Asinxron REST API Gateway: bir nechta mikroxizmatlardan ma'lumotlarni birlashtirish (Aggregation)
**Tavsif:** Mobil ilova uchun bitta `/user-dashboard` so'rovi kelganda, Gateway orqa fondagi Profil, Balans va So'nggi tranzaksiyalar xizmatlariga parallel so'rov yuborib birlashtirishi kerak.
**Talablar:** 3 ta asinxron chaqiruvni parallel yuborish, umumiy JSON formatida javob qaytarish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'
require 'json'

class ApiGatewayAggregator
  def get_dashboard_data(user_id)
    dashboard = {}

    Async do |task|
      t1 = task.async do
        sleep 0.1
        { name: "Alisher", role: "Developer" }
      end

      t2 = task.async do
        sleep 0.15
        { balance_uzs: 14_500_000, currency: "UZS" }
      end

      t3 = task.async do
        sleep 0.12
        [{ id: 1, to: "Payme", sum: 50_000 }]
      end

      dashboard[:user] = t1.wait
      dashboard[:wallet] = t2.wait
      dashboard[:history] = t3.wait
    end

    JSON.generate(dashboard)
  end
end

puts ApiGatewayAggregator.new.get_dashboard_data(101)
```
**Tushuntirish:** Birlashgan API Gateway (Aggregation Pattern) mobil klientlar va mikroxizmatlar orasidagi ortiqcha so'rovlar sonini qisqartiradi. Parallel bajarilishi sababli foydalanuvchi faqat eng sekin xizmat vaqti qadar kutadi.

---

### Topshiriq #1119: Asinxron HTTP chaqiruvlari uchun Circuit Breaker patterni
**Tavsif:** Tashqi integratsiya qilingan servis ketma-ket 5 marta xato bersa, keyingi so'rovlarni darhol to'xtatib (Open state), server resurslarini tejash zarur.
**Talablar:** Muvaffaqiyatsizlik hisoblagichi, holatlar (CLOSED, OPEN, HALF_OPEN), vaqt tamg'asi tekshiruvi.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'

class AsyncCircuitBreaker
  def initialize(failure_threshold = 3, reset_timeout = 5.0)
    @threshold = failure_threshold
    @timeout = reset_timeout
    @failure_count = 0
    @last_failure_time = nil
    @state = :closed
  end

  def execute
    if @state == :open
      if Time.now - @last_failure_time > @timeout
        @state = :half_open
        puts "[CIRCUIT] Holat HALF-OPEN ga o'tdi (Sinov so'rovi)"
      else
        raise StandardError, "Circuit Breaker OPEN: So'rov rad etildi"
      end
    end

    begin
      result = yield
      reset_state
      result
    rescue => e
      handle_failure
      raise e
    end
  end

  private

  def reset_state
    @failure_count = 0
    @state = :closed
  end

  def handle_failure
    @failure_count += 1
    @last_failure_time = Time.now
    if @failure_count >= @threshold
      @state = :open
      warn "[CIRCUIT OGOHLANTIRISH] Chegara yetdi, holat OPEN ga o'tdi!"
    end
  end
end
```
**Tushuntirish:** Circuit Breaker tashqi API nosozliklari paytida ilovani kaskadli qulashdan himoyalaydi. So'rovlarni behuda yuborib CPU va soketlarni band qilish o'rniga, tezkor rad etish amalga oshiriladi.

---

### Topshiriq #1120: CPU-intensiv hisob-kitoblarni Async reaktorini to'xtatmasdan Ractor yoki Thread poolga o'tkazish
**Tavsif:** Agar biron vazifa og'ir matematik hisob-kitob (masalan parollarni bcrypt xeshlash yoki tasvirni qayta ishlash) bo'lsa, u bitta Fiberda ishlasa butun reaktorni qotirib qo'yadi.
**Talablar:** Og'ir hisob-kitobni alohida `Thread` ga o'tkazish, Fiberda `thread.join` ni kutish vaqtida schedulerni bloklamaslik.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'

class OffloadedComputation
  def run_cpu_work(iterations = 10_000_000)
    Async do |task|
      puts "[REAKTOR] Tarmoq so'rovlari parallel davom etmoqda..."

      # Parallel yengil vazifa
      task.async do
        3.times do |i|
          sleep 0.1
          puts "[REAKTOR] Tarmoq vazifasi ##{i + 1} bajarildi"
        end
      end

      # Og'ir CPU vazifasini alohida OS threadiga delegatsiya qilish
      cpu_task = task.async do
        puts "[CPU] Og'ir hisoblash boshlandi..."
        # Thread yaratilganda scheduler uni noblokirovka tarzida kutadi
        result = Thread.new do
          sum = 0
          iterations.times { |n| sum += (n % 7) }
          sum
        end.value
        puts "[CPU] Og'ir hisoblash yakunlandi: Natija = #{result}"
        result
      end

      cpu_task.wait
    end
  end
end

OffloadedComputation.new.run_cpu_work(5_000_000)
```
**Tushuntirish:** Fiberlar kooperativ multitasking bo'lib, faqat I/O paytida boshqaruvni beradi. Og'ir CPU sikllarida Fiber to'xtamaydi. Uni alohida `Thread` yoki `Ractor` ga o'tkazish orqali boshqa I/O Fiberlarining qotib qolishi butunlay oldini olinadi.

---

### Topshiriq #1121: Falcon HTTP/2 serverining Fiber-based Rack arxitekturasi va Puma bilan solishtirish
**Tavsif:** Falcon serveri har bir so'rov uchun OS oqimi ochmaydi, balki har bir ulanish uchun alohida Fiber yaratadi. Uning ishlash tamoyilini Rack spetsifikatsiyasi orqali ko'rsatish lozim.
**Talablar:** Rack v3 spetsifikatsiyasiga mos keluvchi asinxron ilova (Callable application), `rack.response.finished` va `async` kontekstini qo'llash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true

# Falcon uchun namunaviy Rack v3 ilovasi
class FalconApp
  def call(env)
    # env o'zgaruvchisida so'rov ma'lumotlari mavjud
    request_path = env['PATH_INFO']
    method = env['REQUEST_METHOD']

    # Fiber asosidagi asinxron javob
    [
      200,
      {
        'content-type' => 'application/json',
        'x-server' => 'Falcon-HTTP2'
      },
      [
        {
          status: 'success',
          path: request_path,
          method: method,
          server_model: 'Fiber-Per-Connection (Async)'
        }.to_json
      ]
    ]
  end
end
```
**Tushuntirish:** Puma ko'p oqimli (Multi-threaded) arxitekturada ishlaydi va har 1000 ta so'rov uchun yuzlab MB xotira talab qiladi. Falcon esa Ruby 3 Fiber scheduler ustiga qurilgan bo'lib, 10 000 ta parallel HTTP/2 ulanishlarini atigi bir necha o'n MB RAM bilan bemalol ushlab tura oladi.

---

### Topshiriq #1122: Falcon uchun config.ru va asinxron Rack middleware yaratish
**Tavsif:** Production rejimida Falcon serverini sozlash uchun `config.ru` faylida so'rovlarning bajarilish vaqtini noblokirovka tarzida o'lchovchi middleware yaratish kerak.
**Talablar:** Middleware klassi, `call(env)` zanjiri, sarflangan vaqtni `X-Runtime` sarlavhasiga yozish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
# config.ru fayli

class AsyncTimingMiddleware
  def initialize(app)
    @app = app
  end

  def call(env)
    start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
    
    # Asosiy ilovani chaqirish
    status, headers, body = @app.call(env)
    
    elapsed = Process.clock_gettime(Process::CLOCK_MONOTONIC) - start_time
    headers['x-response-time'] = format('%.4f s', elapsed)
    
    [status, headers, body]
  end
end

app = lambda do |env|
  [200, { 'content-type' => 'text/plain' }, ['Salom Falcon Dunyosi!']]
end

use AsyncTimingMiddleware
run app
```
**Tushuntirish:** Falcon dagi Middlewarelar standart Rack interfeysi bilan 100% mosdir. `Process.clock_gettime` yordamida har bir so'rovning davomiyligi mikrosekundlarda o'lchanadi va javob sarlavhalariga qo'shiladi.

---

### Topshiriq #1123: Falcon ostida HTTP/2 Server Push implementatsiyasi
**Tavsif:** Brauzer HTML sahifani so'ragan vaqtda, u hali CSS va JS fayllarini so'rashini kutmasdan, Falcon serveri orqali resurslarni darhol oldindan itarib (Server Push) yuborish lozim.
**Talablar:** `rack.early_hints` yoki HTTP/2 Push Promise mantiqidan foydalanish, `Link` sarlavhalari orqali brauzerga oldindan resurslarni bildirish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true

class Http2PushApp
  def call(env)
    headers = {
      'content-type' => 'text/html; charset=utf-8',
      # Link sarlavhasi orqali HTTP/2 Push aktivlarini bildirish
      'link' => '</app.css>; rel=preload; as=style, </app.js>; rel=preload; as=script'
    }

    body = <<~HTML
      <!DOCTYPE html>
      <html>
        <head>
          <link rel="stylesheet" href="/app.css">
          <script src="/app.js"></script>
        </head>
        <body>
          <h1>Falcon HTTP/2 Server Push Tezligi!</h1>
        </body>
      </html>
    HTML

    [200, headers, [body]]
  end
end
```
**Tushuntirish:** HTTP/2 Server Push mijozga kerakli aktivlarni so'rovsiz yetkazadi. Brauzer HTML ni parslashni boshlagan vaqtda, unga kerakli CSS va JS fayllari allaqachon lokal keshga yetib kelgan bo'ladi, bu esa sayt yuklanishini 50% ga tezlashtiradi.

---

### Topshiriq #1124: Falcon bilan katta hajmdagi fayllarni oqimli (Streaming upload/download) uzatish
**Tavsif:** Foydalanuvchi katta videofayllarni yuklayotganda yoki yuklab olayotganda server xotirasida buferlanmasdan to'g'ridan-to'g'ri oqim uzatilishi kerak.
**Talablar:** Rack javob tanasida `each` metodi mavjud bo'lgan enumerator qaytarish, bo'laklab generatsiya qilish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true

class VideoStreamingApp
  def call(env)
    video_enumerator = Enumerator.new do |yielder|
      10.times do |i|
        # 64KB bo'lak simulyatsiyasi
        chunk = "VIDEO_DATA_CHUNK_#{i + 1}_" * 1024
        yielder << chunk
        # Asinxron pauza
        sleep 0.05
      end
    end

    [
      200,
      {
        'content-type' => 'video/mp4',
        'transfer-encoding' => 'chunked'
      },
      video_enumerator
    ]
  end
end
```
**Tushuntirish:** Falcon Rack ning `body.each` chaqiruvini to'g'ridan-to'g'ri HTTP/2 DATA freymlariga yo'naltiradi. Agar klient interneti sekin bo'lsa, Fiber pauzaga turadi va TCP oyna o'lchami kengaygandagina keyingi bo'lak chiqariladi (Backpressure nazorati).

---

### Topshiriq #1125: Falcon xavfsizlik: TLS ALPN sozlash va HTTP/2 xavfsiz kanallari
**Tavsif:** Falcon serverini xavfsiz HTTPS va HTTP/2 rejimida ishga tushirish uchun TLS Application-Layer Protocol Negotiation (ALPN) sozlamalarini to'g'ri kiritish lozim.
**Talablar:** OpenSSL kontekstida `alpn_protocols = ['h2', 'http/1.1']` sozlash, zamonaviy shifrlash protokollarini (TLSv1.3) majburlash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'openssl'

class FalconTlsConfigurator
  def build_ssl_context(cert_file, key_file)
    ctx = OpenSSL::SSL::SSLContext.new
    ctx.cert = OpenSSL::X509::Certificate.new(File.read(cert_file))
    ctx.key = OpenSSL::PKey::RSA.new(File.read(key_file))

    # Faqat xavfsiz TLS 1.2 va 1.3 protokollariga ruxsat berish
    ctx.min_version = OpenSSL::SSL::TLS1_2_VERSION

    # ALPN orqali HTTP/2 ('h2') ni birinchi o'ringa qo'yish
    ctx.alpn_protocols = ['h2', 'http/1.1']
    ctx.alpn_select_cb = lambda do |protocols|
      protocols.include?('h2') ? 'h2' : 'http/1.1'
    end

    ctx
  end
end
```
**Tushuntirish:** HTTP/2 spetsifikatsiyasi TLS ALPN (Application-Layer Protocol Negotiation) bo'lishini shart qilib qo'yadi. Klient va server TLS ulanish vaqtidayoq qaysi protokol ishlatilishini kelishib oladi. Natijada qo'shimcha so'rovlarsiz darhol ikkinchi avlod HTTP ishga tushadi.

---

### Topshiriq #1126: Falcon yordamida Server-Sent Events (SSE) serveri
**Tavsif:** Falcon HTTP/2 serverida brauzerlarga uzoq davom etuvchi hodisalar oqimini (SSE) har bir foydalanuvchi uchun alohida thread ochmasdan yetkazish zarur.
**Talablar:** `text/event-stream` sarlavhasini qaytarish, `Async` doirasida bo'laklarni uzatuvchi cheksiz oqim (Streaming Body).
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
require 'async'

class FalconSseServerApp
  def call(env)
    return [404, {}, []] unless env['PATH_INFO'] == '/events'

    body = Async::HTTP::Body::Writable.new

    # Alohida Fiberda hodisalarni generatsiya qilish
    Async do |task|
      5.times do |i|
        task.sleep 1.0
        payload = "data: {\"time\": \"#{Time.now.iso8601}\", \"count\": #{i + 1}}\n\n"
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
end
```
**Tushuntirish:** Falcon `Async::HTTP::Body::Writable` orqali Rack 3 spetsifikatsiyasining to'liq asinxron oqimini taqdim etadi. `body.write()` chaqirilganda, faqatgina ma'lumot bor paytda Fiber uyg'onadi, boshqa vaqtda esa nol xotira va CPU sarfi bilan ulanish yillab ochiq turishi mumkin.

---

### Topshiriq #1127: Ko'p yadroli tizimlarda Falcon klaster konfiguratsiyasi (Container / Fork modeli)
**Tavsif:** Katta yuklamali ishlab chiqarish (production) serverida serverning barcha CPU yadrolaridan (masalan 8 yadro) maksimal foydalanish uchun Falcon klasterini sozlash lozim.
**Talablar:** `falcon.rb` konfiguratsiyasi, jarayonlar soni (`count = Etc.nprocessors`), `preload` va xotira boshqaruvi.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
# falcon.rb konfiguratsiya fayli

require 'etc'

service 'app' do
  # CPU yadrolari soniga teng jarayonlar (fork) yaratish
  count Etc.nprocessors

  endpoint Async::HTTP::Endpoint.parse('http://0.0.0.0:3000')

  # Ilovani xotiraga oldindan yuklash (Copy-On-Write tejamkorligi)
  preload 'config/environment.rb'
end
```
**Tushuntirish:** Falcon ning klaster modeli 'Multi-Process + Asynchronous Fiber' gibrid arxitekturasidir. Har bir CPU yadrosida bitta Nginx uslubidagi master-worker forki ishlaydi va har bir worker ichida o'n minglab Fiberlar bir vaqtda I/O so'rovlarini qayta ishlaydi. Bu Ruby ning GIL (Global VM Lock) cheklovini to'liq chetlab o'tadi.

---

### Topshiriq #1128: Falcon bilan WebSockets serveri: asinxron ulanishlarni minimal xotira bilan ushlab turish
**Tavsif:** Falcon serverida bir vaqtning o'zida 50 000 ta faol WebSocket ulanishlarini server xotirasi to'lib ketmasdan qabul qilish va xabarlar almashinuvini ta'minlash kerak.
**Talablar:** `async-websocket` integratsiyasi, HTTP `Upgrade: websocket` ni qabul qilish va asinxron dupleks sikl.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
      [200, { 'content-type' => 'text/plain' }, ['Oddiy HTTP so\'rov']]
    end
  end
end
```
**Tushuntirish:** Puma yoki boshqa thread-based serverlarda har bir WebSocket ulanishi 1 ta operatsion tizim oqimini (thread) bloklab turadi. Falcon da esa 50 000 ta WebSocket ulanishi atigi 50 000 ta Fiber demakdir va ular Linux epoll mexanizmida xotirada passiv turadi.

---

### Topshiriq #1129: Falcon orqali Early Hints (HTTP 103) yuborish va frontend aktivlarini erta yuklash
**Tavsif:** Backend ma'lumotlar bazasidan murakkab SQL so'rovini hisoblayotgan 200 ms vaqt oralig'ida, brauzer bekor o'tirmasligi uchun unga HTTP 103 Early Hints orqali CSS/JS havolalarini oldindan berish lozim.
**Talablar:** `env['rack.early_hints']` dan foydalanish, 103 sarlavhalarini chiqarish va asosiy 200 javobini qaytarish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true

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
end
```
**Tushuntirish:** HTTP 103 Early Hints - web unumdorlikning eng yangi standartidir. Server yakuniy HTML ni hisoblab bo'lguniga qadar, brauzer tarmoq orqali CSS va shriftlarni yuklab olishni boshlaydi. Falcon HTTP/2 da buni tabiiy ravishda qo'llab-quvvatlaydi.

---

### Topshiriq #1130: Falcon server monitoringi: Prometheus metrikalari va xotira oqishini (memory leak) aniqlash
**Tavsif:** Falcon serverida ishlayotgan faol Fiberlar soni, xotira sarfi va HTTP so'rovlar statistikasini Prometheus formatida kuzatib borish kerak.
**Talablar:** `/metrics` marshrutini ochish, `GC.stat` va `Async::Task.current` ko'rsatkichlarini hisoblash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true

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
end
```
**Tushuntirish:** Asinxron serverlarda xotira sizib chiqishi (Memory Leak) ko'pincha global kontekstlarda tozalab ketilmagan Fiber yoki callbacklar sababli yuzaga keladi. `GC.stat[:heap_live_slots]` ko'rsatkichini Prometheus orqali kuzatish anomaliyalarni erta aniqlaydi.

---

### Topshiriq #1131: Past darajali Socket va TCPServer / TCPSocket ulanishlari
**Tavsif:** Tashqi kutubxonalarsiz, sof Ruby standart kutubxonasidagi BSD Soketlar yordamida yuqori unumdor TCP server va mijoz aloqasini o'rnatish lozim.
**Talablar:** `TCPServer.new` dan foydalanish, ulanishlarni qabul qilish (`server.accept`), ma'lumot almashish va soketni xavfsiz yopish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** Ruby dagi `TCPServer` C tilidagi `socket()`, `bind()`, `listen()` va `accept()` tizim chaqiruvlarining to'g'ridan-to'g'ri o'ramidir. Bu tarmoq dasturlashning eng quyi bazaviy asosi bo'lib, har qanday protokolni noldan yaratish imkonini beradi.

---

### Topshiriq #1132: IO.select orqali ko'p sonli ulanishlarni bitta oqimda multipleksirlash
**Tavsif:** Har bir mijoz uchun alohida OS thread ochmasdan, klassik `IO.select` tizim chaqiruvi yordamida bitta oqimda 100 ta soketni kuzatish kerak.
**Talablar:** `IO.select([sockets], nil, nil, timeout)` dan foydalanish, tayyor soketlarni aniqlash va o'qish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** `IO.select` C tilidagi `select()` tizim chaqiruvidir. U OS yadrosiga nazoratni topshirib, ro'yxatdagi istalgan bitta soketda ma'lumot paydo bo'lgandagina dasturga signal beradi. Bu xotirani 1 ta thread hajmida tejab, ko'p mijozlarga xizmat ko'rsatishning qadimiy va ishonchli usulidir.

---

### Topshiriq #1133: Noblokirovka qiluvchi soketlar (read_nonblock, write_nonblock, IO::WaitReadable)
**Tavsif:** Soketdan ma'lumot o'qiyotganda agar tarmoqda hali baytlar yo'q bo'lsa, jarayon kutib turmasdan darhol boshqa ishlarni bajarishi kerak.
**Talablar:** `read_nonblock` chaqirish, `IO::WaitReadable` va `IO::WaitWritable` istisnolarini ushlash.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** `read_nonblock` soketni `O_NONBLOCK` bayrog'i bilan o'qiydi. Agar ma'lumot bo'lmasa, operatsion tizim `EAGAIN` yoki `EWOULDBLOCK` qaytaradi, Ruby esa uni `IO::WaitReadable` ga o'giradi. Bu xususiyat zamonaviy event-loop kutubxonalarining (Async, EventMachine) yuragidir.

---

### Topshiriq #1134: UNIX Domain Sockets orqali jarayonlararo (IPC) ultra-tezkor xabar almashinuvi
**Tavsif:** Bitta server ichida joylashgan Nginx va Ruby dasturi o'rtasida TCP tarmoq steki (loopback 127.0.0.1) o'rniga tezroq bo'lgan UNIX fayl soketlari (`.sock`) orqali aloqa qilish kerak.
**Talablar:** `UNIXServer.new('/tmp/app.sock')` va `UNIXSocket.new`, fayl huquqlarini tozalash va uzatish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** UNIX Domain Soketlari operatsion tizimning TCP/IP tarmoq stekini (cheksunlar, marshrutlash, TCP oyna hisoblashlari) butunlay chetlab o'tadi va to'g'ridan-to'g'ri operativ xotiradagi yadro buferlari orqali ishlaydi. Natijada kechikish 50% gacha kamayadi.

---

### Topshiriq #1135: UDPSocket yordamida yuqori tezlikdagi telemetriya metrikalarini yig'ish tizimi
**Tavsif:** O'yin serverlaridan yoki IoT qurilmalaridan sekundiga o'n minglab koordinata va telemetriya paketlarini yo'qotishga bardoshli, lekin minimal kechikish bilan qabul qilish lozim.
**Talablar:** `UDPSocket.new` dan foydalanish, `bind`, `recvfrom` orqali paket va jo'natuvchi IP/portini olish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** UDP handshakelarsiz va ulanish holatisiz ishlaydi. U bitta paketda to'g'ridan-to'g'ri ma'lumotni yetkazadi. Agar paket yo'lda yo'qolsa ham qolgan paketlarning navbati to'xtamaydi, bu real-time monitoring uchun ayni muddao.

---

### Topshiriq #1136: Binar paketlarni bit-darajasida boshqarish (Array#pack, String#unpack1)
**Tavsif:** Tarmoq uskunasi bilan o'zaro ishlashda 16-bitli port raqami, 32-bitli IPv4 manzili va 8-bitli bayroqlarni binar ko'rinishda qadoqlash (pack) va yechish (unpack) talab etiladi.
**Talablar:** Ruby `pack` formatlari (`n` = 16-bit network endian, `N` = 32-bit network endian, `C` = 8-bit unsigned char) dan foydalanish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true

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
puts "Dekodlangan: #{codec.decode_header(raw_bytes).inspect}"
```
**Tushuntirish:** Ruby ning `Array#pack` va `String#unpack` metodlari C darajasida ishlaydi va binar tarmoq oqimlarini o'ta tez qayta ishlaydi. Tarmoq baytlar tartibi (Big-Endian) uchun `n` va `N` formatlari ishlatiladi.

---

### Topshiriq #1137: OpenSSL::SSL::SSLSocket orqali xavfsiz shifrlangan TLS aloqa o'rnatish
**Tavsif:** Past darajadagi `TCPSocket` ni `OpenSSL::SSL::SSLSocket` ga o'rab, xavfsiz TLS shifrlash qatlamini qo'lda o'rnatish va server sertifikatini tekshirish lozim.
**Talablar:** `SSLContext` yaratish, `SSLSocket.new(tcp_socket, context)`, `connect` chaqirib TLS handshake o'tkazish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
    ssl_socket.puts "GET / HTTP/1.1\r\nHost: #{host}\r\nConnection: close\r\n\r\n"
    response_status = ssl_socket.gets
    puts "[JAVOB]: #{response_status.strip}"

    ssl_socket.close
  end
end
```
**Tushuntirish:** TLS soketlari ma'lumotlarni tarmoqqa uzatishdan oldin apparat darajasida AES/GCM algoritmlari bilan shifrlaydi. `ssl_socket.hostname = host` qatori SNI uchun o'ta muhim bo'lib, to'g'ri virtual server sertifikatini olishni ta'minlaydi.

---

### Topshiriq #1138: Soket darajasidagi parametrlar (setsockopt: SO_REUSEADDR, TCP_NODELAY, SO_KEEPALIVE)
**Tavsif:** Server qayta ishga tushirilganda 'Address already in use' xatosini yo'qotish va paketlarni yig'masdan (Nagle algoritmini o'chirib) darhol jo'natish uchun soket opsiyalarini sozlash kerak.
**Talablar:** `setsockopt` orqali `SOL_SOCKET, SO_REUSEADDR`, `IPPROTO_TCP, TCP_NODELAY` opsiyalarini o'rnatish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** `TCP_NODELAY` 200 ms gacha bo'lgan Nagle kechikishini bartaraf qiladi va interaktiv ilovalarda (o'yinlar, chatlar) javob tezligini keskin oshiradi. `SO_REUSEADDR` esa tizim muhandislariga dasturni nol kechikish bilan qayta ishga tushirishga yordam beradi.

---

### Topshiriq #1139: Zero-copy fayl uzatish: IO.copy_stream va tizim resurslarini tejash
**Tavsif:** Faylni diskdan tarmoq soketiga uzatishda ma'lumotlarni foydalanuvchi xotirasiga (User Space) nusxalamasdan, Linux `sendfile` tizim chaqiruvi orqali to'g'ridan-to'g'ri o'tkazish kerak.
**Talablar:** `IO.copy_stream(src_file, dest_socket)` dan foydalanish, minimal xotira sarfini ko'rsatish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** `IO.copy_stream` Ruby ning eng kuchli yashirin imkoniyatlaridan biridir. U ma'lumotni Ruby VM xotirasiga olib kirmasdan, to'g'ridan-to'g'ri yadro darajasida (Kernel Space) disk drayveridan tarmoq kartasiga uzatadi (Zero-Copy). Bu CPU va xotira yuklamasini 90% ga kamaytiradi.

---

### Topshiriq #1140: Graceful restart qobiliyatiga ega TCP server (File Descriptor passing / handover)
**Tavsif:** Dastur kodi yangilanganda (deploy paytida) mavjud mijozlarning ulanishlarini uzmasdan va yangi so'rovlarni yo'qotmasdan yangi jarayonga o'tish (Zero-Downtime Restart) kerak.
**Talablar:** `server.fileno` orqali soket deskriptorini olish, yangi jarayonni `spawn` qilib soketni meros qilib o'tkazish.
**Yechim (Ruby):**
```ruby
# frozen_string_literal: true
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
end
```
**Tushuntirish:** Zero-Downtime deploysiz zamonaviy klasterlarni tasavvur qilib bo'lmaydi. Soketning fayl deskriptori (FD) operatsion tizimda ochiq qoladi va `for_fd` orqali yangi ishga tushgan Ruby jarayoniga topshiriladi, natijada birorta ham kiruvchi mijoz paketi uzilmaydi.

---

### Topshiriq #1141: Rails ActionCable asoslari: ApplicationCable::Channel, subscribed, unsubscribed
**Tavsif:** Rails ilovasida WebSocket kanallari orqali xonalarga obuna bo'lish, ma'lumotlarni oqimlash (streaming) va mijoz chiqqanda resurslarni tozalash talab qilinadi.
**Talablar:** `ApplicationCable::Channel` dan meros olish, `stream_from`, `subscribed` va `unsubscribed` metodlarini to'g'ri yozish.
**Yechim (Ruby):**
```ruby
# app/channels/chat_channel.rb
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
end
```
**Tushuntirish:** `ActionCable` Rails ning o'rnatilgan real-time tizimidir. `stream_from` metodi orqali xona identifikatori pub/sub magistraliga ulanadi va `ActionCable.server.broadcast` orqali barcha qatnashchilarga zudlik bilan tarqatiladi.

---

### Topshiriq #1142: ActionCable orqali JWT autentifikatsiyasi va ulanish xavfsizligi (Connection#connect)
**Tavsif:** WebSocket ulanishi o'rnatilayotgan paytda foydalanuvchining shaxsini tekshirish, yaroqsiz yoki muddati o'tgan JWT tokenlarni rad etish lozim.
**Talablar:** `ApplicationCable::Connection` ichida `connect` metodini yozish, `identified_by :current_user`, yaroqsiz bo'lsa `reject_unauthorized_connection` chaqirish.
**Yechim (Ruby):**
```ruby
# app/channels/application_cable/connection.rb
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
end
```
**Tushuntirish:** WebSocket ochilgandan so'ng qayta autentifikatsiya qilish qiyin, shuning uchun eng xavfsiz nuqta - bu `Connection#connect` bosqichidir. `reject_unauthorized_connection` chaqirilganda Rails soketni zudlik bilan 404/401 bilan yopadi.

---

### Topshiriq #1143: Redis adapteri bilan ActionCable klasterlash va gorizontal masshtablash
**Tavsif:** Ilova 5 ta alohida serverda (masalan Docker/Kubernetes podlarida) ishlayotganda, bitta serverdagi xabar boshqa serverdagi foydalanuvchilarga ham yetib borishi uchun Redis Pub/Sub adapterini sozlash lozim.
**Talablar:** `cable.yml` faylida Redis adapteri va kanal prefikslarini to'g'ri belgilash.
**Yechim (Ruby):**
```ruby
# config/cable.yml
development:
  adapter: async

test:
  adapter: test

production:
  adapter: redis
  url: <%= ENV.fetch("REDIS_URL") { "redis://localhost:6379/1" } %>
  channel_prefix: khorazmiy_production_cable
  # Yuqori yuklamalar uchun ulanishlar hovuzi
  pool: 50
```
**Tushuntirish:** Rivojlanishda (development) `async` adapteri bitta jarayon ichida xotirada ishlaydi. Ishlab chiqarishda (production) esa `redis` adapteri shart: ActionCable barcha xabarlarni Redis ga `PUBLISH` qiladi va boshqa serverlar `SUBSCRIBE` orqali uni o'z mijozlariga uzatadi.

---

### Topshiriq #1144: AnyCable arxitekturasi: Go/Rust gRPC server bilan Ruby Rails mantiqini bog'lash
**Tavsif:** ActionCable Ruby jarayonida millionlab ulanishlarni ushlaganda xotira ko'p sarflanadi. Soketlarni ushlab turishni Go/Rust tilidagi AnyCable serveriga topshirib, biznes mantiqni gRPC orqali Rails da bajarish kerak.
**Talablar:** `anycable-rails` konfiguratsiyasi, RPC handler va xabarlarni uzatish sxemasi.
**Yechim (Ruby):**
```ruby
# config/initializers/anycable.rb
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
end
```
**Tushuntirish:** AnyCable - Ruby ekotizimining eng zo'r arxitekturaviy yechimlaridan biridir. Barcha og'ir 1 000 000 ta WebSocket soketlarini Go/Rust dagi `anycable-go` ushlaydi (juda kam RAM sarflaydi), ulanish va autentifikatsiya kerak bo'lgandagina gRPC orqali Rails ga murojaat qilinadi.

---

### Topshiriq #1145: Real-time birgalikda hujjat tahrirlash (Operational Transformation / CRDT xabarlari)
**Tavsif:** Google Docs uslubida bir nechta foydalanuvchilar bitta matnni bir vaqtda tahrirlayotganda matn o'zgarishlarini ActionCable orqali konfliktlarsiz sinxronlash lozim.
**Talablar:** O'zgarish deltalarini (Delta / Operation) qabul qilish, versiya raqamini tekshirish va boshqa qatnashchilarga uzatish.
**Yechim (Ruby):**
```ruby
# app/channels/document_channel.rb
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
end
```
**Tushuntirish:** Birgalikda tahrirlashda butun matn yuborilmaydi, balki faqatgina kichik o'zgarish operatsiyalari (Deltas: insert/delete) uzatiladi. Mijoz tomonidagi CRDT (Conflict-free Replicated Data Types) algoritmlari ushbu amallarni bir-biriga moslab, to'g'ri matnni hosil qiladi.

---

### Topshiriq #1146: ActionCable orqali Presence Tracking (onlayn/oflayn foydalanuvchilar ro'yxati)
**Tavsif:** Ilovada qaysi foydalanuvchilar ayni paytda tizimda onlayn ekanligini real-time ko'rsatuvchi indikator kerak.
**Talablar:** Redis Sets orqali foydalanuvchilarni saqlash (`SADD`, `SREM`), ulanganda va chiqqanda boshqalarga bildirishnoma yuborish.
**Yechim (Ruby):**
```ruby
# app/channels/presence_channel.rb
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
end
```
**Tushuntirish:** Presence tizimida Redis to'plamlari (`Sets`) dublikatlarning oldini oladi. Agar bitta foydalanuvchi bir vaqtda noutbuk va telefondan ulansa ham, `SADD` uni faqat bitta marta hisoblaydi, ulanishlar to'liq uzilgandagina oflayn deb belgilanadi.

---

### Topshiriq #1147: Xabarlarni qat'iy tartibda yetkazish va yo'qotishlarning oldini olish (ACK mexanizmi)
**Tavsif:** Tarmoq beqaror bo'lganida xabarlar tushib qolishi yoki kechikib yetib kelishi mumkin. Mijoz har bir xabarni olganligini tasdiqlashi (ACK) shart.
**Talablar:** Xabar ID si, mijozdan ACK kelmaguncha qayta yuborish navbatida ushlab turish.
**Yechim (Ruby):**
```ruby
# app/channels/reliable_message_channel.rb
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
end
```
**Tushuntirish:** ACK (Acknowledgment) mexanizmi moliyaviy va muhim xabarlashuv tizimlarida qat'iy talabdir. Agar mijoz 5 soniya ichida `acknowledge` yubormasa, tizim xabarni qayta uzatadi (At-least-once delivery).

---

### Topshiriq #1148: ActionCable rate limiting va spam filtrlash
**Tavsif:** Foydalanuvchilar chatga sekundiga yuzlab xabarlar yuborib boshqa qatnashchilarni bezovta qilmasligi va serverni to'ldirmasligi uchun cheklov o'rnatish lozim.
**Talablar:** Redis orqali 5 soniyada maksimal 5 ta xabar chegarasini o'rnatish, limitdan oshsa xabarni rad etish.
**Yechim (Ruby):**
```ruby
# app/channels/concerns/rate_limitable.rb
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
end
```
**Tushuntirish:** `transmit` metodi faqatgina so'rov yuborgan joriy mijozning o'ziga xususiy xatolik xabarini qaytaradi (boshqalarga bildirmasdan). Bu spammerning xatti-harakatini zudlik bilan to'xtatadi.

---

### Topshiriq #1149: Turbo Streams va ActionCable integratsiyasi: komponentlarni real-time re-render qilish
**Tavsif:** Rails 7+ Hotwire ekotizimida React yoki Vue ishlatmasdan, serverda HTML bo'lagini render qilib, ActionCable orqali to'g'ridan-to'g'ri brauzer DOM ini yangilash lozim.
**Talablar:** `broadcast_replace_to` yoki `broadcast_append_to` yordamida HTML Turbo Streamlarini tarqatish.
**Yechim (Ruby):**
```ruby
# app/models/comment.rb
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
end
```
**Tushuntirish:** Hotwire Turbo Streams frontend arxitekturasini soddalashtiradi. JavaScript yozmasdan, serverda HTML qismi yaratiladi va ActionCable orqali yuboriladi. Brauzer o'sha HTML ni ko'rsatilgan `target` ID dagi elementga avtomatik qo'shib qo'yadi.

---

### Topshiriq #1150: Real-time monitoring paneli va ActionCable metrikalari (active connections, message throughput)
**Tavsif:** Tizim ma'murlari uchun jami ulangan WebSocket mijozlar soni, sekundiga o'tayotgan xabarlar soni va CPU yuklamasini ko'rsatuvchi real-time panel yaratish kerak.
**Talablar:** `ActionCable.server` metrikalarini yig'ish, har 2 soniyada admin kanaliga telemetriya translyatsiya qilish.
**Yechim (Ruby):**
```ruby
# app/channels/admin_metrics_channel.rb
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
end
```
**Tushuntirish:** Admin panellarida polling (har 5 soniyada GET so'rov) o'rniga ActionCable orqali doimiy metrikalar oqimi berilsa, tarmoq resurslari tejaladi va ma'murlar server holatini sekundlik aniqlikda kuzatib turishadi.

