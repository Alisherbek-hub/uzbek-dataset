# -*- coding: utf-8 -*-
"""
Ruby 23-modul: 1101 dan 1125 gacha bo'lgan topshiriqlar
Async gem, Fiber Scheduler, Async::HTTP va Falcon arxitekturasi
"""

TASKS_1101_1125 = [
    {
        "id": 1101,
        "title": "Async gem va Ruby 3.0+ Fiber scheduler asosidagi noblokirovka qiluvchi reaktor",
        "desc": "Ruby ilovasida minglab parallel tarmoq so'rovlarini OS Threadlarining og'ir xotira sarfisiz (har bir thread 1-2 MB), yengil Fiberlar yordamida (har biri 4 KB) boshqarish talab etiladi.",
        "req": "`require 'async'` dan foydalanish, `Async` blokida asinxron reaktorni ishga tushirish, noblokirovka qiluvchi uyqu (`sleep`) va tarmoq chaqiruvlarini o'tkazish.",
        "code": """# frozen_string_literal: true
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

AsyncReaktorMisoli.new.run_parallel_tasks if __FILE__ == $PROGRAM_NAME""",
        "expl": "Ruby 3.0 da joriy qilingan Fiber Scheduler interfeysi operatsion tizimning `epoll`, `kqueue` yoki `io_uring` tizim chaqiruvlari bilan to'g'ridan-to'g'ri integratsiyalashgan. `Async` gemi ushbu schedulerni avtomatik o'rnatadi, natijada standart `sleep`, `Socket` va `IO` operatsiyalari avtomatik tarzda noblokirovka rejimiga o'tadi."
    },
    {
        "id": 1102,
        "title": "Parallel asinxron vazifalar: Async do |task| task.async { ... } va natijalarni to'plash",
        "desc": "Tizim bir nechta tashqi servisdan ma'lumotlarni parallel yig'ishi va barcha natijalar tayyor bo'lgach ularni bitta umumiy Hash strukturasida qaytarishi lozim.",
        "req": "`task.async` yordamida bolalar vazifalarini ochish, har bir vazifa natijasini `wait` orqali xavfsiz olish.",
        "code": """# frozen_string_literal: true
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
puts metrics.inspect""",
        "expl": "`task.async` yangi bolalar Fiberini (child fiber) yaratadi. `task.wait` chaqirilganda, agar natija tayyor bo'lmasa joriy Fiber kutadi, ammo boshqa parallel Fiberlar bajarilishda davom etadi. Umumiy kutish vaqti 0.2 + 0.3 + 0.1 = 0.6 soniya emas, balki eng uzoq davom etgan vazifa vaqti bo'lgan 0.3 soniyaga teng bo'ladi."
    },
    {
        "id": 1103,
        "title": "Asinxron timeoutlar va kafolatlangan tozalash: task.with_timeout va ensure",
        "desc": "Tashqi mikroxizmat 2 soniya ichida javob bermasa, qotib qolmasdan `Async::TimeoutError` xatosini ko'tarish va ochiq qolgan tarmoq soketlarini tozalash zarur.",
        "req": "`task.with_timeout(duration)` dan foydalanish, timeout sodir bo'lganda `ensure` bloki orqali resurslarni yopish.",
        "code": """# frozen_string_literal: true
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

ResilientServiceCaller.new.call_with_deadline('https://api.partner.com/data', 1.0)""",
        "expl": "`task.with_timeout` Fiber darajasida taymer o'rnatadi. Standart Ruby `Timeout.timeout` tizimidan farqli ravishda (u boshqa operatsion tizim oqimlarida `Thread#raise` chaqirib, xotira va holat buzilishlariga olib kelishi mumkin), `Async::TimeoutError` kooperativ rejimda xavfsiz uziladi."
    },
    {
        "id": 1104,
        "title": "Cheklangan parallellik (Concurrency Limiting): Async::Semaphore yordamida resurslarni himoyalash",
        "desc": "1000 ta faylni tashqi serverga yuklash kerak, biroq tashqi server bir vaqtda 5 tadan ortiq parallel ulanish qabul qilmaydi (429 Too Many Requests xatosi bermasligi uchun).",
        "req": "`Async::Semaphore.new(max)` dan foydalanish, semafor orqali vazifalarni navbatda ushlab turish va ruxsat berish.",
        "code": """# frozen_string_literal: true
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
uploader.upload_batch((1..10).to_a)""",
        "expl": "`Async::Semaphore` cheklangan resurslar (masalan DB ulanishlari, tashqi API rate-limitlari) bilan ishlashda eng muhim vositadir. Agar 100 ta vazifa bo'lsa va chegara 5 ta bo'lsa, qolgan 95 ta vazifa kutish navbatiga turadi va bo'shagan o'rin bo'yicha darhol bajariladi."
    },
    {
        "id": 1105,
        "title": "Ko'p sonli asinxron vazifalarni to'plash va kutish: Async::Barrier",
        "desc": "Katta hajmdagi ma'lumotlar partiyasini (masalan, 50 ta mijoz hisobotini) parallel generatsiya qilib, barchasi to'liq yakunlangachgina xabar berish (Barrier synchronization) kerak.",
        "req": "`Async::Barrier.new` dan foydalanish, `barrier.async` orqali vazifalar biriktirish, `barrier.wait` orqali umumiy to'siqda kutish.",
        "code": """# frozen_string_literal: true
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
generator.generate_all(['Moliya-2026', 'Audit-Q1', 'Soliq-Yillik', 'Kadrlar-Oylik'])""",
        "expl": "`Async::Barrier` bir guruh vazifalarni yagona to'siqqa (barrier) birlashtiradi. Har bir vazifani alohida massivda saqlab `wait` chaqirib yurish o'rniga, `barrier.wait` barcha biriktirilgan Fiberlar tugashini kutadi. Agar biron vazifada xatolik yuz bersa, to'siq xatolikni propogatsiya qiladi."
    },
    {
        "id": 1106,
        "title": "Asinxron xabarlar almashinuvi va kanallar: Async::Queue",
        "desc": "Ishlab chiqaruvchi (Producer) va Iste'molchi (Consumer) arxitekturasida ma'lumotlar oqimini noblokirovka qiluvchi navbat orqali xavfsiz uzatish kerak.",
        "req": "`Async::Queue.new` dan foydalanish, `queue.enqueue` va `queue.dequeue` orqali ma'lumot almashish, oxirida `nil` bilan to'xtatish.",
        "code": """# frozen_string_literal: true
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

AsyncEventPipeline.new.start_pipeline""",
        "expl": "`Async::Queue` Fiber-safe navbat hisoblanadi. Navbat bo'sh bo'lganida `dequeue` chaqirilsa, iste'molchi Fiberi avtomatik uyquga ketadi va yangi element tushishi bilanoq scheduler tomonidan uyg'otiladi. Bu polling (aylanib tekshirish) CPU yuklamasini nolga tushiradi."
    },
    {
        "id": 1107,
        "title": "Asinxron noblokirovka qiluvchi DNS yechuvchi: Async::DNS::Resolver",
        "desc": "Standart `Resolv` yoki `Socket.getaddrinfo` butun Ruby VM jarayonini to'xtatib qo'yishi mumkin. Tarmoq trafigini tahlil qilishda asinxron DNS yechuvchi talab qilinadi.",
        "req": "`Async::DNS::Resolver` dan foydalanish, domenlar uchun A va AAAA yozuvlarini asinxron olish, xatoliklarni qayta ishlash.",
        "code": """# frozen_string_literal: true
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

AsyncDnsResolver.new.resolve_domains(['google.com', 'ruby-lang.org', 'github.com'])""",
        "expl": "`Async::IO::Address.resolve` Ruby 3 Fiber scheduler orqali OS ning asinxron DNS mexanizmlaridan foydalanadi. Domenlar ro'yxati parallel yuboriladi va server javoblari kelishiga qarab korutinalar o'z vaqtida uyg'onadi."
    },
    {
        "id": 1108,
        "title": "Async::IO orqali asinxron fayl va tarmoq oqimlari (Streaming)",
        "desc": "Katta log fayllarini o'qish yoki tarmoq soketiga ma'lumotlarni oqim shaklida (streaming) uzatishda xotirani to'ldirib yubormaslik lozim.",
        "req": "`Async::IO::Stream` dan foydalanish, bo'laklab o'qish (`read_partial`), buferlangan yozish va flush qilish.",
        "code": """# frozen_string_literal: true
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
AsyncStreamProcessor.new.process_stream(mock_in, mock_out)""",
        "expl": "`Async::IO::Stream` yuqori darajadagi buferlangan I/O interfeysini taqdim etadi. `read_partial` ma'lumot kelishi bilan uni darhol qaytaradi, `flush` esa tizim soketiga baytlarni noblokirovka tarzida yozib beradi."
    },
    {
        "id": 1109,
        "title": "Asinxron vazifalarda xatoliklarni qayta ishlash va exception propagation",
        "desc": "Parallel ishlayotgan 10 ta vazifadan bittasida istisno (exception) yuz bersa, u butun dasturni to'satdan yiqitmasdan, oqilona qayd etilishi va boshqa vazifalar nazorat qilinishi kerak.",
        "req": "`Async::Stop` va maxsus xatoliklarni tutish, `task.wait` dagi xatoliklarni himoyalangan blokda ushlash.",
        "code": """# frozen_string_literal: true
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

SafeParallelExecutor.new.run_with_fault_tolerance""",
        "expl": "`Async` da bolalar vazifasidagi xatolik `wait` chaqirilgan vaqtda qayta ko'tariladi (re-raised). Bu strukturalangan parallellik (Structured Concurrency) tamoyiliga to'liq mos bo'lib, xatoliklarni kutilmagan joylarda emas, balki qat'iy nazorat ostida ushlash imkonini beradi."
    },
    {
        "id": 1110,
        "title": "Periodik fon vazifalari (Cron / Heartbeat ticker) Async siklida",
        "desc": "Har 5 soniyada server salomatligini tekshiruvchi yoki keshni tozalovchi periodik vazifani `Async` reaktorida boshqa ishlarga to'sqinlik qilmasdan yurgizish kerak.",
        "req": "Cheksiz sikl ichida `sleep(interval)`, `task.stop` signali bilan xavfsiz to'xtatish (graceful cancellation).",
        "code": """# frozen_string_literal: true
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

AsyncHeartbeatTicker.new.start_heartbeat(0.5, 3)""",
        "expl": "Asinxron ticker fonda ishlayotganda OS ning boshqa threadlariga muhtoj emas. U bitta Ruby jarayoni ichida minglab boshqa mijoz so'rovlari bilan yonma-yon ishlayveradi. To'xtatish kerak bo'lganda `task.stop` chaqirilib, resurslar toza bo'shatiladi."
    },
    {
        "id": 1111,
        "title": "Async::HTTP::Client yordamida asinxron HTTP/1.1 va HTTP/2 so'rovlari",
        "desc": "Tashqi web-servislarga yuqori tezlikda ulanish va HTTP/2 protokoli orqali bitta soketda bir nechta so'rovlarni o'tkazish talab etiladi.",
        "req": "`Async::HTTP::Client` dan foydalanish, `Async::HTTP::Endpoint` ni sozlash, GET so'rovini yuborish va status kodini tekshirish.",
        "code": """# frozen_string_literal: true
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

# AsyncHttpClientDemo.new.fetch_web_page('https://www.ruby-lang.org')""",
        "expl": "`Async::HTTP::Client` Ruby uchun eng zamonaviy HTTP/2 mijozidir. U ulanishlarni ochiq saqlaydi va HTTP/2 multipleksirlashidan foydalanadi, natijada har safar yangi TCP ulanish ochmasdan yuzlab so'rovlar parallel uzatiladi."
    },
    {
        "id": 1112,
        "title": "Katta hajmdagi HTTP javob tanasini oqimli (Streaming response body) qabul qilish",
        "desc": "Katta fayllarni (masalan, 100 MB hajmdagi zip arxiv) yuklab olishda butun faylni xotiraga yig'ib RAM ni to'ldirmasdan, diskka qismlab (chunked streaming) yozish lozim.",
        "req": "`response.body.read` orqali bo'laklarni olish, faylga oqim shaklida yozish, xotira sarfini doimiy nazorat qilish.",
        "code": """# frozen_string_literal: true
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
        puts "\\n[YUKLANDI] Fayl saqlandi: #{output_path}"
      ensure
        client.close
      end
    end
  end
end""",
        "expl": "OpenResty dagi kabi, Ruby `Async::HTTP` ham `response.each` bloki orqali oqimli o'qishni ta'minlaydi. Fayl qanchalik ulkan bo'lmasin, dastur xotirasida faqat joriy bo'lak (masalan 16KB) ushlab turiladi, bu esa Garbage Collector yengil ishlashini ta'minlaydi."
    },
    {
        "id": 1113,
        "title": "1000 ta URL uchun asinxron web scraper va tezlik chegarasi (Rate limit)",
        "desc": "Katta qidiruv tizimi yoki ma'lumotlar bazasi uchun 1000 ta saytni skanerlashda serverga ortiqcha yuklama bermasdan, maksimal 20 ta parallel ulanish bilan ishlash zarur.",
        "req": "`Async::Semaphore` va `Async::Barrier` ni birlashtirish, URL larni o'qish, xatoliklarni qayd etish.",
        "code": """# frozen_string_literal: true
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
MassWebScraper.new(5).scrape_urls(urls)""",
        "expl": "Semafor va To'siq (Barrier) kombinatsiyasi yirik masshtabli asinxron arxitekturaning klassik namunasidir. Semafor bir vaqtda 5 tadan ortiq Fiber ishlamasligini nazorat qilsa, Barrier barcha 20 ta vazifa to'liq yakunlangachgina boshqaruvni keyingi bosqichga topshiradi."
    },
    {
        "id": 1114,
        "title": "Asinxron Webhook yuboruvchi agent (Exponential backoff va retry bilan)",
        "desc": "To'lov amalga oshirilganda mijozning serveriga webhook bildirishnomasini yuborish kerak. Agar mijoz serveri band bo'lsa, 3 marta kechikish bilan qayta urinish lozim.",
        "req": "Maksimal urinishlar (3 marta), eksponentsial pauza (`sleep(delay * 2**attempt)`), muvaffaqiyatsiz bo'lsa logga yozish.",
        "code": """# frozen_string_literal: true
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

AsyncWebhookDispatcher.new.send_webhook('https://merchant.uz/api/callback', { order_id: 9912 })""",
        "expl": "Asinxron webhook jo'natish orqali to'lov tranzaksiyasini yakunlagan asosiy mijoz veb-sahifasi tashqi mijozning sekin ishlayotgan serveri tufayli kutib qolmaydi. Barcha qayta urinishlar fondagi Fiberda mustaqil amalga oshadi."
    },
    {
        "id": 1115,
        "title": "HTTP/2 ulanishlarida ulanishlarni multipleksirlash (Multiplexing & Connection Pooling)",
        "desc": "Bitta mikroxizmat serveriga yuzlab API so'rovlarini jo'natishda HTTP/1.1 kabi har safar alohida TCP ochmasdan, HTTP/2 ning Streams imkoniyatidan foydalanish lozim.",
        "req": "`Async::HTTP::Endpoint` ni HTTP/2 protokoli bilan ochish, bitta klient orqali parallel 10 ta so'rovni o'tkazish.",
        "code": """# frozen_string_literal: true
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

Http2MultiplexerDemo.new.run_multiplexed_calls(%w[/users /orders /products /invoices])""",
        "expl": "HTTP/2 ning inqilobiy yutug'i bitta TCP ulanish ichida ikki tomonlama mustaqil oqimlarni (Streams) multipleksirlashidir. Head-of-line blocking muammosi yo'qoladi va tarmoq trafigi keskin kamayadi."
    },
    {
        "id": 1116,
        "title": "async-websocket yordamida noblokirovka qiluvchi WebSocket mijozi",
        "desc": "Tashqi real-time xizmatga WebSocket orqali ulanib, kiruvchi xabarlarni asinxron tinglash va kerak bo'lganda buyruqlar jo'natish zarur.",
        "req": "`async-websocket` yoki `Async::WebSocket::Client` mantiqidan foydalanish, ulanish, xabar kutish sikli va yopish.",
        "code": """# frozen_string_literal: true
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

AsyncWebSocketClientSim.new.connect_and_listen('wss://stream.crypto.uz/ws')""",
        "expl": "`async-websocket` to'liq Fiber asosida qurilgan bo'lib, xabar kelishini kutayotganda hech qanday tizim ipini band qilmaydi. Bu bitta Ruby jarayonida yuzlab tashqi WebSocket kanallarini bir vaqtda kuzatib borish imkonini beradi."
    },
    {
        "id": 1117,
        "title": "Asinxron Server-Sent Events (SSE) iste'molchisi",
        "desc": "Tashqi yangiliklar yoki birja serveridan kelayotgan SSE (text/event-stream) oqimini to'xtatmasdan o'qib, har bir `data:` hodisasini darhol qayta ishlash kerak.",
        "req": "`data:` qatorlarini ajratish, hodisa nomlarini tekshirish, uzilish yuz berganda qayta ulanish.",
        "code": """# frozen_string_literal: true
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
          payload = line.sub(/^data:\\s*/, '')
          puts "[HODISA QABUL QILINDI]: #{payload}"
        end
      end
      puts "[SSE] Oqim yakunlandi"
    end
  end
end

mock_sse = StringIO.new("data: Foydalanuvchi tizimga kirdi\\n\\ndata: Yangi buyurtma #402\\n\\n")
AsyncSseConsumer.new.consume_events(mock_sse)""",
        "expl": "SSE HTTP protokoli ustiga qurilgan bir tomonlama matnli oqimdir. Asinxron Ruby da har bir satr kelishi bilan o'qiladi va xotirani band qilmasdan real-time tizimlarga uzatiladi."
    },
    {
        "id": 1118,
        "title": "Asinxron REST API Gateway: bir nechta mikroxizmatlardan ma'lumotlarni birlashtirish (Aggregation)",
        "desc": "Mobil ilova uchun bitta `/user-dashboard` so'rovi kelganda, Gateway orqa fondagi Profil, Balans va So'nggi tranzaksiyalar xizmatlariga parallel so'rov yuborib birlashtirishi kerak.",
        "req": "3 ta asinxron chaqiruvni parallel yuborish, umumiy JSON formatida javob qaytarish.",
        "code": """# frozen_string_literal: true
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

puts ApiGatewayAggregator.new.get_dashboard_data(101)""",
        "expl": "Birlashgan API Gateway (Aggregation Pattern) mobil klientlar va mikroxizmatlar orasidagi ortiqcha so'rovlar sonini qisqartiradi. Parallel bajarilishi sababli foydalanuvchi faqat eng sekin xizmat vaqti qadar kutadi."
    },
    {
        "id": 1119,
        "title": "Asinxron HTTP chaqiruvlari uchun Circuit Breaker patterni",
        "desc": "Tashqi integratsiya qilingan servis ketma-ket 5 marta xato bersa, keyingi so'rovlarni darhol to'xtatib (Open state), server resurslarini tejash zarur.",
        "req": "Muvaffaqiyatsizlik hisoblagichi, holatlar (CLOSED, OPEN, HALF_OPEN), vaqt tamg'asi tekshiruvi.",
        "code": """# frozen_string_literal: true
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
end""",
        "expl": "Circuit Breaker tashqi API nosozliklari paytida ilovani kaskadli qulashdan himoyalaydi. So'rovlarni behuda yuborib CPU va soketlarni band qilish o'rniga, tezkor rad etish amalga oshiriladi."
    },
    {
        "id": 1120,
        "title": "CPU-intensiv hisob-kitoblarni Async reaktorini to'xtatmasdan Ractor yoki Thread poolga o'tkazish",
        "desc": "Agar biron vazifa og'ir matematik hisob-kitob (masalan parollarni bcrypt xeshlash yoki tasvirni qayta ishlash) bo'lsa, u bitta Fiberda ishlasa butun reaktorni qotirib qo'yadi.",
        "req": "Og'ir hisob-kitobni alohida `Thread` ga o'tkazish, Fiberda `thread.join` ni kutish vaqtida schedulerni bloklamaslik.",
        "code": """# frozen_string_literal: true
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

OffloadedComputation.new.run_cpu_work(5_000_000)""",
        "expl": "Fiberlar kooperativ multitasking bo'lib, faqat I/O paytida boshqaruvni beradi. Og'ir CPU sikllarida Fiber to'xtamaydi. Uni alohida `Thread` yoki `Ractor` ga o'tkazish orqali boshqa I/O Fiberlarining qotib qolishi butunlay oldini olinadi."
    },
    {
        "id": 1121,
        "title": "Falcon HTTP/2 serverining Fiber-based Rack arxitekturasi va Puma bilan solishtirish",
        "desc": "Falcon serveri har bir so'rov uchun OS oqimi ochmaydi, balki har bir ulanish uchun alohida Fiber yaratadi. Uning ishlash tamoyilini Rack spetsifikatsiyasi orqali ko'rsatish lozim.",
        "req": "Rack v3 spetsifikatsiyasiga mos keluvchi asinxron ilova (Callable application), `rack.response.finished` va `async` kontekstini qo'llash.",
        "code": """# frozen_string_literal: true

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
end""",
        "expl": "Puma ko'p oqimli (Multi-threaded) arxitekturada ishlaydi va har 1000 ta so'rov uchun yuzlab MB xotira talab qiladi. Falcon esa Ruby 3 Fiber scheduler ustiga qurilgan bo'lib, 10 000 ta parallel HTTP/2 ulanishlarini atigi bir necha o'n MB RAM bilan bemalol ushlab tura oladi."
    },
    {
        "id": 1122,
        "title": "Falcon uchun config.ru va asinxron Rack middleware yaratish",
        "desc": "Production rejimida Falcon serverini sozlash uchun `config.ru` faylida so'rovlarning bajarilish vaqtini noblokirovka tarzida o'lchovchi middleware yaratish kerak.",
        "req": "Middleware klassi, `call(env)` zanjiri, sarflangan vaqtni `X-Runtime` sarlavhasiga yozish.",
        "code": """# frozen_string_literal: true
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
run app""",
        "expl": "Falcon dagi Middlewarelar standart Rack interfeysi bilan 100% mosdir. `Process.clock_gettime` yordamida har bir so'rovning davomiyligi mikrosekundlarda o'lchanadi va javob sarlavhalariga qo'shiladi."
    },
    {
        "id": 1123,
        "title": "Falcon ostida HTTP/2 Server Push implementatsiyasi",
        "desc": "Brauzer HTML sahifani so'ragan vaqtda, u hali CSS va JS fayllarini so'rashini kutmasdan, Falcon serveri orqali resurslarni darhol oldindan itarib (Server Push) yuborish lozim.",
        "req": "`rack.early_hints` yoki HTTP/2 Push Promise mantiqidan foydalanish, `Link` sarlavhalari orqali brauzerga oldindan resurslarni bildirish.",
        "code": """# frozen_string_literal: true

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
end""",
        "expl": "HTTP/2 Server Push mijozga kerakli aktivlarni so'rovsiz yetkazadi. Brauzer HTML ni parslashni boshlagan vaqtda, unga kerakli CSS va JS fayllari allaqachon lokal keshga yetib kelgan bo'ladi, bu esa sayt yuklanishini 50% ga tezlashtiradi."
    },
    {
        "id": 1124,
        "title": "Falcon bilan katta hajmdagi fayllarni oqimli (Streaming upload/download) uzatish",
        "desc": "Foydalanuvchi katta videofayllarni yuklayotganda yoki yuklab olayotganda server xotirasida buferlanmasdan to'g'ridan-to'g'ri oqim uzatilishi kerak.",
        "req": "Rack javob tanasida `each` metodi mavjud bo'lgan enumerator qaytarish, bo'laklab generatsiya qilish.",
        "code": """# frozen_string_literal: true

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
end""",
        "expl": "Falcon Rack ning `body.each` chaqiruvini to'g'ridan-to'g'ri HTTP/2 DATA freymlariga yo'naltiradi. Agar klient interneti sekin bo'lsa, Fiber pauzaga turadi va TCP oyna o'lchami kengaygandagina keyingi bo'lak chiqariladi (Backpressure nazorati)."
    },
    {
        "id": 1125,
        "title": "Falcon xavfsizlik: TLS ALPN sozlash va HTTP/2 xavfsiz kanallari",
        "desc": "Falcon serverini xavfsiz HTTPS va HTTP/2 rejimida ishga tushirish uchun TLS Application-Layer Protocol Negotiation (ALPN) sozlamalarini to'g'ri kiritish lozim.",
        "req": "OpenSSL kontekstida `alpn_protocols = ['h2', 'http/1.1']` sozlash, zamonaviy shifrlash protokollarini (TLSv1.3) majburlash.",
        "code": """# frozen_string_literal: true
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
end""",
        "expl": "HTTP/2 spetsifikatsiyasi TLS ALPN (Application-Layer Protocol Negotiation) bo'lishini shart qilib qo'yadi. Klient va server TLS ulanish vaqtidayoq qaysi protokol ishlatilishini kelishib oladi. Natijada qo'shimcha so'rovlarsiz darhol ikkinchi avlod HTTP ishga tushadi."
    }
]
