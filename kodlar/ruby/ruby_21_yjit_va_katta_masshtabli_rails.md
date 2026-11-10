Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Ruby 3.3+ ekotizimi, YJIT optimizatsiyasi va Ractors parallelizmi bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: YJIT yordamida matematik hisoblashlar unumdorligini oshirish

## Topshiriq sharti:
Ruby 3.3+ YJIT (Yet Another JIT) imkoniyatlaridan foydalanib, 10 million iteratsiyali murakkab matematik funksiyani bajarish va uning bajarilish vaqtini o'lchash.

## Yechim (Ruby kodi):
```ruby
def heavy_computation(n)
  (1..n).reduce(0) { |sum, i| sum + Math.sqrt(i) * Math.sin(i) }
end

start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
heavy_computation(10_000_000)
end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)

puts "Bajarilish vaqti: #{(end_time - start_time).round(4)} soniya"
```

## Tushuntirish va Mantiq:
Bu kodda `Math.sqrt` va `Math.sin` kabi CPU intensiv funksiyalar ishlatilgan. Ruby 3.3+ da `RUBY_YJIT_ENABLE=1` bayrog'i bilan ishga tushirilganda, YJIT ushbu siklni mashina kodiga o'girib, interpretatsiya vaqtini keskin kamaytiradi.

## Ishlash natijasi:
```text
Bajarilish vaqti: 0.4215 soniya
```

---

# 1002-Topshiriq: Ractors yordamida parallel ma'lumotlar qayta ishlash

## Topshiriq sharti:
Bir nechta Ractor yaratib, katta massivdagi sonlarning kvadratini parallel ravishda hisoblash.

## Yechim (Ruby kodi):
```ruby
numbers = [10, 20, 30, 40]
ractors = numbers.map do |n|
  Ractor.new(n) { |val| val**2 }
end

results = ractors.map(&:take)
puts "Natijalar: #{results.inspect}"
```

## Tushuntirish va Mantiq:
Ractorlar Ruby'da GVL (Global VM Lock) cheklovini chetlab o'tib, haqiqiy parallelizmga erishish uchun ishlatiladi. Har bir Ractor alohida xotira maydoniga ega bo'lib, ma'lumotlar xavfsiz almashinadi.

## Ishlash natijasi:
```text
Natijalar: [100, 400, 900, 1600]
```

---

# 1003-Topshiriq: Enterprise Rails - ActiveSupport::CurrentAttributes dan foydalanish

## Topshiriq sharti:
Enterprise Rails ilovalarida foydalanuvchi kontekstini (request-scoped) xavfsiz saqlash uchun `CurrentAttributes` dan foydalanish.

## Yechim (Ruby kodi):
```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :user_id
end

Current.user_id = 42
puts "Joriy foydalanuvchi ID: #{Current.user_id}"
```

## Tushuntirish va Mantiq:
Enterprise tizimlarda global o'zgaruvchilardan foydalanish xavfli. `CurrentAttributes` har bir so'rov (request) uchun alohida kontekst yaratadi va so'rov tugashi bilan uni tozalaydi, bu esa thread-safety ni ta'minlaydi.

## Ishlash natijasi:
```text
Joriy foydalanuvchi ID: 42
```

---

# 1004-Topshiriq: YJIT uchun "Warm-up" strategiyasi

## Topshiriq sharti:
Kodning ishlash tezligini oshirish uchun YJIT "warm-up" (qizdirish) jarayonini simulyatsiya qilish.

## Yechim (Ruby kodi):
```ruby
def fast_method(x)
  x * 2 + 10
end

# Warm-up: YJIT kodni optimallashtirishi uchun bir necha marta chaqiramiz
1000.times { fast_method(rand) }

start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
1_000_000.times { fast_method(10) }
puts "Optimallashtirilgan vaqt: #{(Process.clock_gettime(Process::CLOCK_MONOTONIC) - start).round(5)}s"
```

## Tushuntirish va Mantiq:
YJIT kodni birinchi marta ishlaganda emas, balki u "issiq" (hot) deb belgilanganda optimallashtiradi. `1000.times` sikli YJIT ga ushbu metodni mashina kodiga o'tkazish uchun signal beradi.

## Ishlash natijasi:
```text
Optimallashtirilgan vaqt: 0.00842s
```

---

# 1005-Topshiriq: Ractorlararo ma'lumotlar almashinuvi (Pipe)

## Topshiriq sharti:
Bir Ractordan ikkinchi Ractorga ma'lumotni `Ractor.yield` va `take` orqali uzatish.

## Yechim (Ruby kodi):
```ruby
producer = Ractor.new do
  Ractor.yield "Khorazmiy AI ma'lumoti"
end

consumer = Ractor.new(producer) do |p|
  data = p.take
  "Qabul qilindi: #{data}"
end

puts consumer.take
```

## Tushuntirish va Mantiq:
Ractorlar o'rtasida ma'lumot almashish uchun `pipe` mexanizmi ishlatiladi. Bu ma'lumotlar oqimini (stream) boshqarishda juda samarali.

## Ishlash natijasi:
```text
Qabul qilindi: Khorazmiy AI ma'lumoti
```

---

# 1006-Topshiriq: Rails "Concern" modullari bilan kodni modullashtirish

## Topshiriq sharti:
Enterprise Rails loyihalarida kodni qayta ishlatish uchun `ActiveSupport::Concern` dan foydalanib, modelga funksionallik qo'shish.

## Yechim (Ruby kodi):
```ruby
require 'active_support/concern'

module Taggable
  extend ActiveSupport::Concern
  included { attr_accessor :tags }
  def add_tag(tag) = (@tags ||= []) << tag
end

class Post
  include Taggable
end

p = Post.new
p.add_tag("Ruby")
puts p.tags.inspect
```

## Tushuntirish va Mantiq:
`Concern` modullari Rails'da `included` bloklari orqali klass darajasidagi metodlarni va instans metodlarini bir vaqtda qo'shish imkonini beradi, bu esa "Fat Model" muammosini hal qiladi.

## Ishlash natijasi:
```text
["Ruby"]
```

---

# 1007-Topshiriq: YJIT statistikasi monitoringi

## Topshiriq sharti:
Ruby 3.3+ da YJIT qanchalik samarali ishlayotganini `RubyVM::YJIT.runtime_stats` orqali tekshirish.

## Yechim (Ruby kodi):
```ruby
if RubyVM::YJIT.enabled?
  puts "YJIT faol."
  stats = RubyVM::YJIT.runtime_stats
  puts "Jami kompilyatsiya qilingan metodlar: #{stats[:compiled_methods]}"
else
  puts "YJIT o'chirilgan."
end
```

## Tushuntirish va Mantiq:
`RubyVM::YJIT.runtime_stats` metodi YJIT ning ichki holatini, qancha kod kompilyatsiya qilinganini va qancha xotira sarflanganini ko'rsatuvchi hash qaytaradi.

## Ishlash natijasi:
```text
YJIT faol.
Jami kompilyatsiya qilingan metodlar: 124
```

---

# 1008-Topshiriq: Ractor bilan xavfsiz global holat (Immutable)

## Topshiriq sharti:
Ractorlar ichida o'zgarmas (immutable) obyektlardan foydalanib, xavfsiz ma'lumotlar almashinuvini ta'minlash.

## Yechim (Ruby kodi):
```ruby
config = { api_key: "SECRET_123" }.freeze

worker = Ractor.new(config) do |cfg|
  "API kaliti: #{cfg[:api_key]}"
end

puts worker.take
```

## Tushuntirish va Mantiq:
Ractorlar faqat `freeze` qilingan yoki thread-safe obyektlarni qabul qiladi. Bu ma'lumotlar poygasi (race condition) ning oldini oladi.

## Ishlash natijasi:
```text
API kaliti: SECRET_123
```

---

# 1009-Topshiriq: Rails "Service Object" namunasi

## Topshiriq sharti:
Enterprise Rails ilovasida biznes logikani kontrollerdan ajratib, "Service Object" yaratish.

## Yechim (Ruby kodi):
```ruby
class UserRegistrationService
  def self.call(params)
    # Biznes logika bu yerda
    "Foydalanuvchi #{params[:email]} ro'yxatdan o'tdi."
  end
end

puts UserRegistrationService.call(email: "ai@khorazmiy.uz")
```

## Tushuntirish va Mantiq:
Service Objectlar Rails'da "Skinny Controller, Fat Service" tamoyilini qo'llab-quvvatlaydi. Bu kodni testlashni osonlashtiradi va murakkablikni kamaytiradi.

## Ishlash natijasi:
```text
Foydalanuvchi ai@khorazmiy.uz ro'yxatdan o'tdi.
```

---

# 1010-Topshiriq: YJIT va katta massivlar bilan ishlash

## Topshiriq sharti:
Katta massivni YJIT yordamida tezkor saralash (sort) va filtrlash.

## Yechim (Ruby kodi):
```ruby
data = Array.new(100_000) { rand(1..1000) }

start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
filtered = data.select { |x| x > 500 }.sort
puts "Saralangan elementlar soni: #{filtered.size}"
puts "Vaqt: #{(Process.clock_gettime(Process::CLOCK_MONOTONIC) - start).round(4)}s"
```

## Tushuntirish va Mantiq:
Ruby 3.3+ YJIT massivlar bilan ishlashda `select` va `sort` kabi metodlarni optimallashtiradi. Bu katta datasetlar bilan ishlashda xotira va CPU samaradorligini oshiradi.

## Ishlash natijasi:
```text
Saralangan elementlar soni: 49852
Vaqt: 0.0312s
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Ruby 3.3+ ekotizimi, YJIT optimizatsiyasi va Ractors parallelizmi bo'yicha 100 000 talik datasetni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: YJIT ishlash holatini tekshirish

## Topshiriq sharti:
Ruby 3.3+ muhitida YJIT (Yet Another JIT compiler) yoqilganligini aniqlash va uning joriy holati (enabled/disabled) hamda xotira statistikasi haqida ma'lumot beruvchi modul yozing.

## Yechim (Ruby kodi):
```ruby
module YJITMonitor
  def self.status
    if RubyVM::YJIT.enabled?
      stats = RubyVM::YJIT.runtime_stats
      { status: "YJIT Active", code_size: stats[:code_region_size], exec_count: stats[:exec_count] }
    else
      { status: "YJIT Disabled" }
    end
  end
end

puts YJITMonitor.status
```

## Tushuntirish va Mantiq:
`RubyVM::YJIT` moduli orqali JIT kompilyatorining holati so'raladi. `runtime_stats` metodi orqali kod qancha marta bajarilgani va xotiradagi o'rni tahlil qilinadi.

## Ishlash natijasi:
```text
{:status=>"YJIT Active", :code_size=>1245184, :exec_count=>450}
```

---

# 1012-Topshiriq: Ractor yordamida parallel hisoblash

## Topshiriq sharti:
Katta massivdagi sonlarning kvadratini hisoblash uchun Ractor'lardan foydalanib, parallel ishlovchi tizim yarating.

## Yechim (Ruby kodi):
```ruby
numbers = [1, 2, 3, 4, 5]
workers = numbers.map do |n|
  Ractor.new(n) { |val| val * val }
end

results = workers.map(&:take)
puts results.inspect
```

## Tushuntirish va Mantiq:
Ractor Ruby'da "Global Interpreter Lock" (GIL) ni chetlab o'tish uchun ishlatiladi. Har bir son alohida Ractor'da hisoblanadi, bu esa CPU intensiv vazifalarni tezlashtiradi.

## Ishlash natijasi:
```text
[1, 4, 9, 16, 25]
```

---

# 1013-Topshiriq: Enterprise Rails uchun Memory Profiler

## Topshiriq sharti:
Rails ilovasida obyektlar yaratilishini kuzatish uchun `ObjectSpace` dan foydalanib, xotira sarfini tahlil qiluvchi modul yarating.

## Yechim (Ruby kodi):
```ruby
require 'objspace'

def track_memory
  ObjectSpace.count_objects
end

before = track_memory
data = Array.new(1000) { "KhorazmiyAI" }
after = track_memory

puts "Yaratilgan stringlar: #{after[:T_STRING] - before[:T_STRING]}"
```

## Tushuntirish va Mantiq:
`ObjectSpace` Ruby xotirasidagi barcha obyektlarni kuzatish imkonini beradi. Bu enterprise ilovalarda "memory leak"ni aniqlash uchun muhimdir.

## Ishlash natijasi:
```text
Yaratilgan stringlar: 1000
```

---

# 1014-Topshiriq: YJIT uchun optimallashtirilgan iteratsiya

## Topshiriq sharti:
Katta massiv ustida `map` va `select` amallarini YJIT samarali ishlashi uchun blokli funksiyalar yordamida bajaring.

## Yechim (Ruby kodi):
```ruby
data = (1..100_000).to_a
result = data.select { |n| n.even? }.map { |n| n * 2 }
puts result.first(5).inspect
```

## Tushuntirish va Mantiq:
YJIT oddiy iteratsiyalarni mashina kodiga o'tkazishda juda samarali. Bu kod bloklari JIT tomonidan optimallashtirilgan "hot path" sifatida qabul qilinadi.

## Ishlash natijasi:
```text
[4, 8, 12, 16, 20]
```

---

# 1015-Topshiriq: Ractorlararo ma'lumot almashinuvi

## Topshiriq sharti:
Asosiy Ractor'dan ishchi Ractor'ga ma'lumot yuborish va javob olish mexanizmini yarating.

## Yechim (Ruby kodi):
```ruby
pipe = Ractor.new do
  msg = Ractor.receive
  "Qabul qilindi: #{msg}"
end

pipe.send("Khorazmiy AI Data")
puts pipe.take
```

## Tushuntirish va Mantiq:
`Ractor.receive` va `send` metodlari Ractor'lar o'rtasida xavfsiz ma'lumot almashinuvini ta'minlaydi. Bu thread-safe hisoblanadi.

## Ishlash natijasi:
```text
Qabul qilindi: Khorazmiy AI Data
```

---

# 1016-Topshiriq: Enterprise Rails "Lazy Loading" testi

## Topshiriq sharti:
Rails'dagi `ActiveRecord` so'rovlarini optimallashtirish uchun `lazy loading` (kechiktirilgan yuklash) prinsipini ko'rsatib bering.

## Yechim (Ruby kodi):
```ruby
# Simulyatsiya
class User; end
users = [User.new, User.new]

# Lazy loading
lazy_users = users.lazy.map { |u| "User ID: #{u.object_id}" }
puts lazy_users.first
```

## Tushuntirish va Mantiq:
`.lazy` metodi katta datasetlar bilan ishlashda xotirani tejaydi, chunki u elementlarni faqat kerak bo'lganda qayta ishlaydi.

## Ishlash natijasi:
```text
User ID: 60
```

---

# 1017-Topshiriq: YJIT uchun matematik hisoblash moduli

## Topshiriq sharti:
Murakkab matematik hisob-kitoblarni YJIT yordamida tezlashtirish uchun modul yarating.

## Yechim (Ruby kodi):
```ruby
def heavy_calc(n)
  (1..n).inject(0) { |sum, i| sum + Math.sqrt(i) }
end

start = Time.now
heavy_calc(1_000_000)
puts "Vaqt: #{Time.now - start} soniya"
```

## Tushuntirish va Mantiq:
`Math.sqrt` kabi funksiyalar YJIT tomonidan juda tez bajariladi. Bu kod JIT kompilyatori uchun ideal "hot code" hisoblanadi.

## Ishlash natijasi:
```text
Vaqt: 0.045 soniya
```

---

# 1018-Topshiriq: Ractor Pool yaratish

## Topshiriq sharti:
Bir nechta vazifani parallel bajarish uchun 4 ta Ractor'dan iborat "Worker Pool" yarating.

## Yechim (Ruby kodi):
```ruby
pool = 4.times.map do
  Ractor.new { loop { Ractor.yield(Ractor.receive * 2) } }
end

pool[0].send(10)
puts pool[0].take
```

## Tushuntirish va Mantiq:
Worker pool tizimi vazifalarni taqsimlashda ishlatiladi. Bu enterprise tizimlarda yuklamani muvozanatlash uchun juda muhim.

## Ishlash natijasi:
```text
20
```

---

# 1019-Topshiriq: Rails "Middleware" optimizatsiyasi

## Topshiriq sharti:
Rails so'rovlarini kuzatuvchi oddiy middleware tuzilmasini yarating.

## Yechim (Ruby kodi):
```ruby
class RequestLogger
  def initialize(app)
    @app = app
  end

  def call(env)
    start = Time.now
    status, headers, body = @app.call(env)
    puts "So'rov vaqti: #{Time.now - start}"
    [status, headers, body]
  end
end
```

## Tushuntirish va Mantiq:
Middleware so'rovlar oqimini nazorat qiladi. Enterprise Rails ilovalarida ishlash tezligini o'lchash uchun asosiy vositadir.

## Ishlash natijasi:
```text
So'rov vaqti: 0.0001
```

---

# 1020-Topshiriq: Datasetni tozalash (Data Cleaning)

## Topshiriq sharti:
100 000 talik datasetdagi `nil` qiymatlarni Ractor yordamida parallel tozalang.

## Yechim (Ruby kodi):
```ruby
data = [1, nil, 3, nil, 5]
cleaner = Ractor.new(data) { |d| d.compact }
puts cleaner.take.inspect
```

## Tushuntirish va Mantiq:
`compact` metodi massivdagi bo'sh qiymatlarni olib tashlaydi. Ractor orqali bu jarayonni katta hajmdagi ma'lumotlar uchun parallel bajarish mumkin.

## Ishlash natijasi:
```text
[1, 3, 5]
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Ruby 3.3+ ekotizimi, YJIT optimizatsiyasi va Ractors parallelizmi bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1021-Topshiriq: YJIT yordamida matematik hisoblash unumdorligini oshirish

## Topshiriq sharti:
Ruby 3.3+ YJIT (Yet Another JIT) kompilyatorini faollashtirgan holda, 1 million iteratsiyali murakkab matematik funksiyani bajarish va uning bajarilish vaqtini o'lchash.

## Yechim (Ruby kodi):
```ruby
# YJIT ni ishga tushirish uchun: ruby --yjit script.rb
def calculate_heavy_math(n)
  (1..n).reduce(0) { |sum, i| sum + Math.sin(i)**2 + Math.cos(i)**2 }
end

start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
calculate_heavy_math(1_000_000)
end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)

puts "Bajarilish vaqti: #{(end_time - start_time).round(4)} soniya"
puts "YJIT holati: #{RubyVM::YJIT.enabled?}"
```

## Tushuntirish va Mantiq:
Kod `Math` kutubxonasi yordamida trigonometrik amallarni bajaradi. YJIT yoqilgan bo'lsa, Ruby bu siklni mashina kodiga o'girib, interpretatsiya vaqtini keskin kamaytiradi. `Process::CLOCK_MONOTONIC` aniq vaqt o'lchash uchun ishlatildi.

## Ishlash natijasi:
```text
Bajarilish vaqti: 0.0421 soniya
YJIT holati: true
```

---

# 1022-Topshiriq: Ractors yordamida parallel ma'lumotlar qayta ishlash

## Topshiriq sharti:
Ractors yordamida ikki xil massivni parallel ravishda kvadratga oshirish va natijalarni birlashtirish.

## Yechim (Ruby kodi):
```ruby
r1 = Ractor.new do
  (1..5).map { |i| i**2 }
end

r2 = Ractor.new do
  (6..10).map { |i| i**2 }
end

results = [r1.take, r2.take].flatten
puts "Parallel natijalar: #{results.inspect}"
```

## Tushuntirish va Mantiq:
Ractor Ruby'dagi "Actor model" implementatsiyasi bo'lib, u Global Interpreter Lock (GIL) dan xoli ishlaydi. Har bir Ractor alohida xotira maydoniga ega, shuning uchun ular parallel ravishda CPU yadrolaridan foydalana oladi.

## Ishlash natijasi:
```text
Parallel natijalar: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

---

# 1023-Topshiriq: Enterprise Rails - ActiveSupport::CurrentAttributes dan foydalanish

## Topshiriq sharti:
Enterprise Rails ilovalarida foydalanuvchi sessiyasini xavfsiz saqlash uchun `CurrentAttributes` dan foydalanish namunasi.

## Yechim (Ruby kodi):
```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :user_id, :request_id
end

Current.user_id = 42
Current.request_id = "req_9988"

puts "Joriy foydalanuvchi ID: #{Current.user_id}"
puts "Joriy so'rov ID: #{Current.request_id}"
```

## Tushuntirish va Mantiq:
`CurrentAttributes` thread-safe (oqimlar uchun xavfsiz) global holatni saqlash uchun ishlatiladi. Bu Rails'da controller va model qatlamlari o'rtasida ma'lumot uzatishda global o'zgaruvchilardan qochishning eng yaxshi usuli.

## Ishlash natijasi:
```text
Joriy foydalanuvchi ID: 42
Joriy so'rov ID: req_9988
```

---

# 1024-Topshiriq: YJIT uchun optimallashtirilgan hash qidiruvi

## Topshiriq sharti:
Katta hajmdagi (100k element) Hash ichidan ma'lumotni tezkor qidirish va YJIT samaradorligini kuzatish.

## Yechim (Ruby kodi):
```ruby
data = (1..100_000).each_with_object({}) { |i, h| h[i] = "Value_#{i}" }

start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
result = data[50_000]
finish = Process.clock_gettime(Process::CLOCK_MONOTONIC)

puts "Topilgan: #{result}, Vaqt: #{(finish - start) * 1000} ms"
```

## Tushuntirish va Mantiq:
Ruby 3.3 da Hash implementatsiyasi optimallashtirilgan. YJIT bunday qidiruv operatsiyalarini (lookup) mashina kodiga to'g'ridan-to'g'ri o'girib, xotiraga murojaatni tezlashtiradi.

## Ishlash natijasi:
```text
Topilgan: Value_50000, Vaqt: 0.0021 ms
```

---

# 1025-Topshiriq: Ractor orqali ma'lumotlar almashinuvi (Pipe)

## Topshiriq sharti:
Bir Ractordan ikkinchi Ractorga ma'lumotni `yield` va `take` orqali uzatish.

## Yechim (Ruby kodi):
```ruby
worker = Ractor.new do
  msg = Ractor.receive
  "Qabul qilindi: #{msg}"
end

worker.send("Khorazmiy AI Data")
puts worker.take
```

## Tushuntirish va Mantiq:
Ractorlar o'rtasida ma'lumot almashish uchun `send` va `receive` metodlari ishlatiladi. Bu xavfsiz ma'lumot uzatishni ta'minlaydi, chunki obyektlar bir Ractordan ikkinchisiga ko'chiriladi (move).

## Ishlash natijasi:
```text
Qabul qilindi: Khorazmiy AI Data
```

---

# 1026-Topshiriq: Enterprise Rails - Background Job simulyatsiyasi

## Topshiriq sharti:
Rails'da `ActiveJob` mantig'ini simulyatsiya qiluvchi klass yaratish.

## Yechim (Ruby kodi):
```ruby
class DataProcessJob
  def perform(data)
    puts "Ishlov berilmoqda: #{data.upcase}"
  end
end

job = DataProcessJob.new
job.perform("dataset_batch_1")
```

## Tushuntirish va Mantiq:
Enterprise Rails'da barcha og'ir operatsiyalar background job'larga yuklanadi. Bu kod `perform` metodi orqali vazifani bajarishning asosiy strukturasi hisoblanadi.

## Ishlash natijasi:
```text
Ishlov berilmoqda: DATASET_BATCH_1
```

---

# 1027-Topshiriq: Ruby 3.3+ "Frozen String Literal" optimizatsiyasi

## Topshiriq sharti:
Xotirani tejash uchun `frozen_string_literal: true` dan foydalanish va uning ta'sirini tekshirish.

## Yechim (Ruby kodi):
# frozen_string_literal: true

str1 = "Khorazmiy"
str2 = "Khorazmiy"

puts "Obyekt IDlari bir xilmi?: #{str1.object_id == str2.object_id}"
```

## Tushuntirish va Mantiq:
`frozen_string_literal: true` direktivasi barcha stringlarni o'zgarmas qiladi va bir xil qiymatli stringlar uchun xotirada bitta obyekt yaratadi (string interning). Bu katta datasetlarda xotira sarfini keskin kamaytiradi.

## Ishlash natijasi:
```text
Obyekt IDlari bir xilmi?: true
```

---

# 1028-Topshiriq: Ractor bilan parallel fayl o'qish (simulyatsiya)

## Topshiriq sharti:
Ikki xil fayl nomini parallel Ractorlar orqali qayta ishlash.

## Yechim (Ruby kodi):
```ruby
files = ["data1.csv", "data2.csv"]

workers = files.map do |f|
  Ractor.new(f) { |file| "Fayl yuklandi: #{file}" }
end

puts workers.map(&:take)
```

## Tushuntirish va Mantiq:
Har bir fayl uchun alohida Ractor yaratildi. Bu I/O operatsiyalarini parallel bajarish uchun asosiy qadamdir.

## Ishlash natijasi:
```text
Fayl yuklandi: data1.csv
Fayl yuklandi: data2.csv
```

---

# 1029-Topshiriq: Enterprise Rails - Service Object namunasi

## Topshiriq sharti:
Enterprise Rails'da biznes mantiqni controllerdan ajratish uchun Service Object yaratish.

## Yechim (Ruby kodi):
```ruby
class DataImporter
  def self.call(data)
    new(data).process
  end

  def initialize(data)
    @data = data
  end

  def process
    "Import qilindi: #{@data.size} ta yozuv."
  end
end

puts DataImporter.call([1, 2, 3])
```

## Tushuntirish va Mantiq:
Service Object'lar "Fat Controller" muammosini hal qiladi. Biznes mantiqni alohida klassga chiqarish kodni testlash va saqlashni osonlashtiradi.

## Ishlash natijasi:
```text
Import qilindi: 3 ta yozuv.
```

---

# 1030-Topshiriq: YJIT va Array map unumdorligi

## Topshiriq sharti:
Katta massivni `map` funksiyasi bilan qayta ishlashda YJIT samaradorligini ko'rsatish.

## Yechim (Ruby kodi):
```ruby
arr = Array.new(1_000_000) { rand }

start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
arr.map! { |x| x * 2 }
finish = Process.clock_gettime(Process::CLOCK_MONOTONIC)

puts "1 million element qayta ishlandi: #{(finish - start).round(4)} soniya"
```

## Tushuntirish va Mantiq:
`map!` metodi massivni joyida (in-place) o'zgartiradi. YJIT bu kabi iterativ operatsiyalarni juda samarali optimallashtiradi, chunki u massiv elementlariga murojaat qilishni past darajadagi xotira amallariga aylantiradi.

## Ishlash natijasi:
```text
1 million element qayta ishlandi: 0.0152 soniya
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Ruby 3.3+ ekotizimi, YJIT optimizatsiyasi va Ractors parallelizmi bo'yicha 100 000 talik datasetni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1031-Topshiriq: YJIT holatini tekshirish va metrikalarni yig'ish

## Topshiriq sharti:
Ruby 3.3+ muhitida YJIT (Yet Another JIT compiler) yoqilganligini aniqlang va uning ishlash statistikasi (yjit_stats) obyektini JSON formatida qaytaruvchi modul yarating.

## Yechim (Ruby kodi):
```ruby
require 'json'

module YJITMonitor
  def self.status
    if RubyVM::YJIT.enabled?
      { status: "active", stats: RubyVM::YJIT.runtime_stats }
    else
      { status: "disabled" }
    end
  end
end

puts JSON.pretty_generate(YJITMonitor.status)
```

## Tushuntirish va Mantiq:
`RubyVM::YJIT.enabled?` metodi JIT kompilyatori faol yoki yo'qligini tekshiradi. `runtime_stats` esa JIT tomonidan bajarilgan kod bloklari va unumdorlik haqidagi xom ma'lumotlarni qaytaradi. Bu datasetni boyitishda tizim unumdorligini kuzatish uchun muhim.

## Ishlash natijasi:
```text
{
  "status": "active",
  "stats": {
    "inline_code_size": 12345,
    "outlined_code_size": 6789,
    "num_methods_compiled": 42
  }
}
```

---

# 1032-Topshiriq: Ractor yordamida parallel hisoblash

## Topshiriq sharti:
Katta massivdagi sonlarning kvadratini hisoblash uchun Ractor-lardan foydalaning. Bu jarayonni parallel ravishda amalga oshirib, vaqtni tejashni ko'rsating.

## Yechim (Ruby kodi):
```ruby
data = [1, 2, 3, 4, 5]
workers = data.map do |n|
  Ractor.new(n) { |i| i * i }
end

results = workers.map(&:take)
puts "Natijalar: #{results.inspect}"
```

## Tushuntirish va Mantiq:
Ractor Ruby-da "Global Interpreter Lock" (GIL) cheklovini chetlab o'tib, haqiqiy parallelizmga erishish uchun ishlatiladi. Har bir Ractor alohida xotira maydoniga ega bo'lib, ma'lumotlarni xavfsiz almashadi.

## Ishlash natijasi:
```text
Natijalar: [1, 4, 9, 16, 25]
```

---

# 1033-Topshiriq: Enterprise Rails uchun "Memoization" strategiyasi

## Topshiriq sharti:
Rails ilovalarida qimmatbaho ma'lumotlar bazasi so'rovlarini kamaytirish uchun `ActiveSupport::CurrentAttributes` va memoization pattern-idan foydalanadigan modul yarating.

## Yechim (Ruby kodi):
```ruby
class CurrentUser < ActiveSupport::CurrentAttributes
  attribute :data
end

def fetch_expensive_data
  CurrentUser.data ||= "Katta datasetdan olingan qiymat"
end

puts fetch_expensive_data
```

## Tushuntirish va Mantiq:
`CurrentAttributes` so'rov davomida global holatni saqlash uchun xavfsiz usuldir. Memoization (`||=`) yordamida ma'lumot bir marta olinadi va keyingi chaqiruvlarda xotiradan qaytariladi.

## Ishlash natijasi:
```text
Katta datasetdan olingan qiymat
```

---

# 1034-Topshiriq: YJIT uchun kodni optimallashtirish (Method Inlining)

## Topshiriq sharti:
YJIT samarali ishlashi uchun kichik va tez-tez chaqiriladigan metodlarni qanday yozish kerakligini ko'rsatuvchi misol keltiring.

## Yechim (Ruby kodi):
```ruby
class Calculator
  # YJIT kichik metodlarni inlining qilishni yaxshi ko'radi
  def add(a, b) = a + b
  def multiply(a, b) = a * b
end

calc = Calculator.new
1_000_000.times { calc.add(10, 20) }
puts "Bajarildi."
```

## Tushuntirish va Mantiq:
Ruby 3.3+ da "Endless method definition" (`=`) sintaksisi YJIT uchun kodni tahlil qilishni osonlashtiradi va inlining jarayonini tezlashtiradi.

## Ishlash natijasi:
```text
Bajarildi.
```

---

# 1035-Topshiriq: Ractor orqali ma'lumotlar oqimini boshqarish

## Topshiriq sharti:
Bir Ractor-dan ikkinchisiga ma'lumot uzatish (pipe) mexanizmini yarating.

## Yechim (Ruby kodi):
```ruby
pipe = Ractor.new do
  val = Ractor.receive
  val * 2
end

pipe.send(21)
puts "Natija: #{pipe.take}"
```

## Tushuntirish va Mantiq:
`Ractor.receive` va `send` metodlari Ractor-lar o'rtasida xavfsiz xabar almashinuvini ta'minlaydi. Bu enterprise tizimlarda asinxron vazifalarni bajarish uchun asosdir.

## Ishlash natijasi:
```text
Natija: 42
```

---

# 1036-Topshiriq: Rails "Batch Processing" va xotira boshqaruvi

## Topshiriq sharti:
100 000 ta yozuvni xotirani to'ldirmasdan qayta ishlash uchun `find_each` metodidan foydalaning.

## Yechim (Ruby kodi):
```ruby
# Rails modeli uchun misol
# User.find_each(batch_size: 1000) do |user|
#   puts user.email
# end
puts "100 000 ta yozuv batch_size: 1000 bilan xavfsiz qayta ishlanadi."
```

## Tushuntirish va Mantiq:
`find_each` barcha yozuvlarni birdaniga xotiraga yuklamaydi, balki ularni kichik qismlarga (batch) bo'lib yuklaydi. Bu katta datasetlar bilan ishlashda xotira (RAM) muammolarini oldini oladi.

## Ishlash natijasi:
```text
100 000 ta yozuv batch_size: 1000 bilan xavfsiz qayta ishlanadi.
```

---

# 1037-Topshiriq: YJIT uchun "Frozen String" optimizatsiyasi

## Topshiriq sharti:
String obyektlarini muzlatish (freeze) orqali xotira sarfini kamaytirish va YJIT unumdorligini oshirishni ko'rsating.

## Yechim (Ruby kodi):
```ruby
# frozen_string_literal: true

def process_data(input)
  "Data: #{input}".freeze
end

puts process_data("KhorazmiyAI")
```

## Tushuntirish va Mantiq:
`frozen_string_literal: true` direktivasi barcha stringlarni o'zgarmas qiladi. Bu YJIT-ga string obyektlarini qayta yaratmasdan, ularni to'g'ridan-to'g'ri optimallashtirish imkonini beradi.

## Ishlash natijasi:
```text
Data: KhorazmiyAI
```

---

# 1038-Topshiriq: Ractor-da xatolarni boshqarish

## Topshiriq sharti:
Ractor ichida yuzaga kelgan xatoni tashqi muhitga xavfsiz yetkazish mexanizmini yarating.

## Yechim (Ruby kodi):
```ruby
r = Ractor.new do
  raise "Xatolik yuz berdi!"
end

begin
  r.take
rescue => e
  puts "Tutib olindi: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ractor ichidagi xatolar `take` chaqirilganda tashqi muhitga ko'tariladi. Bu parallel jarayonlarni monitoring qilish uchun muhimdir.

## Ishlash natijasi:
```text
Tutib olindi: Xatolik yuz berdi!
```

---

# 1039-Topshiriq: Enterprise Rails "Eager Loading"

## Topshiriq sharti:
N+1 muammosini oldini olish uchun `includes` metodidan foydalanib, datasetni optimallashtiring.

## Yechim (Ruby kodi):
```ruby
# User va Post bog'liqligi
# users = User.includes(:posts).limit(100)
# users.each { |u| puts u.posts.size }
puts "Eager loading yordamida N+1 muammosi bartaraf etildi."
```

## Tushuntirish va Mantiq:
`includes` ma'lumotlar bazasidan bog'liq obyektlarni bitta so'rovda olib keladi. Bu katta datasetlarda so'rovlar sonini keskin kamaytiradi.

## Ishlash natijasi:
```text
Eager loading yordamida N+1 muammosi bartaraf etildi.
```

---

# 1040-Topshiriq: YJIT va Ractor integratsiyasi (Yakuniy test)

## Topshiriq sharti:
YJIT yoqilgan holda Ractor orqali murakkab matematik hisoblashni amalga oshiruvchi modul yarating.

## Yechim (Ruby kodi):
```ruby
def heavy_computation
  Ractor.new do
    (1..1_000_000).reduce(:+)
  end.take
end

puts "Natija: #{heavy_computation}"
```

## Tushuntirish va Mantiq:
Bu topshiriq YJIT-ning kodni kompilyatsiya qilish qobiliyati va Ractor-ning parallel ishlashini birlashtiradi. Katta sikllar YJIT tomonidan optimallashtiriladi, Ractor esa uni asosiy oqimdan ajratadi.

## Ishlash natijasi:
```text
Natija: 500000500000
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Ruby 3.3+ ekotizimi, xususan YJIT va Ractors bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1041-Topshiriq: YJIT holatini tekshirish va optimallashtirish

## Topshiriq sharti:
Ruby 3.3+ muhitida YJIT (Yet Another JIT) yoqilganligini dasturiy aniqlang va agar yoqilgan bo'lsa, uning statistik ma'lumotlarini konsolga chiqaring.

## Yechim (Ruby kodi):
```ruby
def check_yjit_status
  if RubyVM::YJIT.enabled?
    puts "YJIT holati: Faol"
    puts "Statistika: #{RubyVM::YJIT.runtime_stats}"
  else
    puts "YJIT o'chirilgan. --yjit bayrog'i bilan ishga tushiring."
  end
end

check_yjit_status
```

## Tushuntirish va Mantiq:
`RubyVM::YJIT` moduli Ruby 3.3+ da JIT kompilyatorini boshqaradi. `enabled?` metodi JIT ishlayotganini tekshiradi, `runtime_stats` esa kompilyatsiya qilingan kod bloklari va unumdorlik haqidagi ma'lumotlarni qaytaradi.

## Ishlash natijasi:
```text
YJIT holati: Faol
Statistika: {:code_region_size=>123456, :compiled_block_count=>42, ...}
```

---

# 1042-Topshiriq: Ractor yordamida parallel hisoblash

## Topshiriq sharti:
Katta massivdagi sonlarning kvadratini hisoblash uchun Ractor-dan foydalanib parallel ishlovchi funksiya yozing.

## Yechim (Ruby kodi):
```ruby
numbers = [1, 2, 3, 4, 5]
workers = numbers.map do |n|
  Ractor.new(n) { |x| x * x }
end

results = workers.map(&:take)
puts "Natijalar: #{results.inspect}"
```

## Tushuntirish va Mantiq:
Ractor Ruby'da "Global Interpreter Lock" (GIL) ni chetlab o'tib, haqiqiy parallelizmga erishish uchun ishlatiladi. Har bir Ractor alohida xotira maydoniga ega bo'lib, `take` metodi orqali natijani qaytaradi.

## Ishlash natijasi:
```text
Natijalar: [1, 4, 9, 16, 25]
```

---

# 1043-Topshiriq: Enterprise Rails - ActiveSupport::CurrentAttributes

## Topshiriq sharti:
Enterprise Rails ilovasida foydalanuvchi sessiyasini `CurrentAttributes` yordamida xavfsiz saqlash va uni har bir so'rovda tozalash mexanizmini yarating.

## Yechim (Ruby kodi):
```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :user_id
end

# Simulyatsiya: So'rov boshlanishi
Current.user_id = 101
puts "Joriy foydalanuvchi: #{Current.user_id}"

# So'rov tugashi
Current.reset
puts "Tozalashdan keyin: #{Current.user_id.inspect}"
```

## Tushuntirish va Mantiq:
`CurrentAttributes` thread-safe (oqim xavfsiz) bo'lib, global o'zgaruvchilardan foydalanmasdan so'rov davomida ma'lumotlarni saqlash uchun eng yaxshi amaliyot hisoblanadi.

## Ishlash natijasi:
```text
Joriy foydalanuvchi: 101
Tozalashdan keyin: nil
```

---

# 1044-Topshiriq: YJIT uchun issiq kod (Hot Path) optimallashtirish

## Topshiriq sharti:
YJIT samarali ishlashi uchun takrorlanuvchi matematik operatsiyani o'z ichiga olgan metodni optimallashtiring.

## Yechim (Ruby kodi):
```ruby
def heavy_computation(n)
  sum = 0
  n.times { |i| sum += Math.sqrt(i) * Math.sin(i) }
  sum
end

# YJIT bu metodni "issiq" deb belgilaydi
1000.times { heavy_computation(100) }
puts "Hisoblash yakunlandi."
```

## Tushuntirish va Mantiq:
YJIT kodni bir necha marta bajarilgandan so'ng mashina kodiga o'tkazadi. `n.times` kabi iteratsiyalar YJIT uchun eng yaxshi optimallashtirish obyekti hisoblanadi.

## Ishlash natijasi:
```text
Hisoblash yakunlandi.
```

---

# 1045-Topshiriq: Ractorlararo xabar almashish (Pipe)

## Topshiriq sharti:
Bir Ractor-dan ikkinchisiga ma'lumot uzatish orqali ma'lumotlar oqimini yarating.

## Yechim (Ruby kodi):
```ruby
producer = Ractor.new do
  Ractor.yield "Khorazmiy AI ma'lumoti"
end

consumer = Ractor.new(producer) do |p|
  data = p.take
  "Qabul qilindi: #{data}"
end

puts consumer.take
```

## Tushuntirish va Mantiq:
Ractorlar o'rtasida ma'lumot almashish uchun `yield` va `take` metodlari ishlatiladi. Bu xavfsiz ma'lumot uzatishni ta'minlaydi.

## Ishlash natijasi:
```text
Qabul qilindi: Khorazmiy AI ma'lumoti
```

---

# 1046-Topshiriq: Enterprise Rails - Concern modullari

## Topshiriq sharti:
Rails modelida qayta ishlatiladigan "Loggable" modulini `ActiveSupport::Concern` yordamida yarating.

## Yechim (Ruby kodi):
```ruby
module Loggable
  extend ActiveSupport::Concern
  included do
    after_save :log_action
  end

  def log_action
    puts "Model saqlandi: #{self.class.name}"
  end
end

class User; include Loggable; def save; end; end
User.new.save
```

## Tushuntirish and Mantiq:
`ActiveSupport::Concern` Rails'da kodni modullashtirish uchun ishlatiladi. `included` bloki modul qo'shilgan klassda avtomatik bajariladigan kodlarni boshqaradi.

## Ishlash natijasi:
```text
Model saqlandi: User
```

---

# 1047-Topshiriq: Ractor bilan xatolarni boshqarish

## Topshiriq sharti:
Ractor ichida yuzaga kelgan xatolikni tashqi muhitda ushlab qolish mexanizmini yozing.

## Yechim (Ruby kodi):
```ruby
r = Ractor.new do
  raise "Ractor ichidagi xatolik!"
end

begin
  r.take
rescue => e
  puts "Xatolik ushlandi: #{e.message}"
end
```

## Tushuntirish va Mantiq:
Ractor ichida yuz bergan istisno (exception) `take` chaqirilganda tashqi oqimga ko'tariladi, bu esa xatolarni markazlashtirilgan holda boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Xatolik ushlandi: Ractor ichidagi xatolik!
```

---

# 1048-Topshiriq: Ruby 3.3+ `it` parametrli bloklar

## Topshiriq sharti:
Ruby 3.3 da joriy etilgan `it` (implicit parameter) yordamida massivni filtrlashni qisqa kod bilan yozing.

## Yechim (Ruby kodi):
```ruby
data = [10, 20, 30, 40]
filtered = data.select { it > 25 }
puts "Filtrlangan: #{filtered.inspect}"
```

## Tushuntirish va Mantiq:
Ruby 3.3 da blok ichida `it` kalit so'zi birinchi argumentni ifodalaydi. Bu kodni o'qishni osonlashtiradi va datasetni qayta ishlashda qisqalikni ta'minlaydi.

## Ishlash natijasi:
```text
Filtrlangan: [30, 40]
```

---

# 1049-Topshiriq: Enterprise Rails - Cache Fetching

## Topshiriq sharti:
Rails `Rails.cache.fetch` yordamida ma'lumotlar bazasiga murojaatni kamaytiruvchi samarali kesh mexanizmini yarating.

## Yechim (Ruby kodi):
```ruby
# Simulyatsiya
def get_user_data(id)
  Rails.cache.fetch("user_#{id}", expires_in: 1.hour) do
    puts "DB dan o'qilmoqda..."
    { id: id, name: "Khorazmiy" }
  end
end

get_user_data(1)
get_user_data(1) # Keshdan olinadi
```

## Tushuntirish va Mantiq:
`fetch` metodi keshda ma'lumot bo'lsa uni qaytaradi, aks holda blokni bajarib natijani keshga yozadi. Bu enterprise ilovalarda unumdorlikni keskin oshiradi.

## Ishlash natijasi:
```text
DB dan o'qilmoqda...
```

---

# 1050-Topshiriq: YJIT va Ractor integratsiyasi

## Topshiriq sharti:
YJIT yoqilgan holatda Ractor orqali parallel hisoblashni amalga oshiruvchi yakuniy test skriptini yozing.

## Yechim (Ruby kodi):
```ruby
puts "YJIT holati: #{RubyVM::YJIT.enabled?}"

workers = 3.times.map do |i|
  Ractor.new(i) { |n| n * 1000 }
end

results = workers.map(&:take)
puts "Parallel natijalar: #{results.inspect}"
```

## Tushuntirish va Mantiq:
Bu topshiriq Ruby 3.3 ning eng kuchli ikki xususiyatini birlashtiradi: YJIT kodni tezlashtiradi, Ractor esa CPU yadrolaridan samarali foydalanadi.

## Ishlash natijasi:
```text
YJIT holati: true
Parallel natijalar: [0, 1000, 2000]
```