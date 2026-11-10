# 201-Topshiriq: Blok tushunchasi: do ... end va { ... } sintaksislari
## Topshiriq sharti:
Bir qatorli va ko'p qatorli bloklar yordamida xabarlarni takrorlang.

## Yechim (Ruby kodi):
```ruby
# Bir qatorli blok odatda { ... } bilan yoziladi
3.times { puts "Bir qatorli blok!" }

# Ko'p qatorli blok do ... end bilan yoziladi
2.times do
  puts "Ko'p qatorli"
  puts "blok ijrosi"
end
```

## Tushuntirish va Mantiq:
Ruby-da kod bloklari mustaqil obyekt emas, ular faqat metod chaqiruviga biriktiriladigan anonim kod parchalaridir. Konvensiyaga ko'ra bir qatorli amallar `{ ... }`, ko'p qatorli amallar esa `do ... end` bilan o'raladi.

## Ishlash natijasi:
```text
Bir qatorli blok!
Bir qatorli blok!
Bir qatorli blok!
Ko'p qatorli
blok ijrosi
Ko'p qatorli
blok ijrosi
```


# 202-Topshiriq: Blok parametrlarini qabul qilish: |param|
## Topshiriq sharti:
Blok ichida kelayotgan qiymatni qabul qilib, uning kvadratini chiqaring.

## Yechim (Ruby kodi):
```ruby
[1, 2, 3].each do |son|
  puts "#{son} ning kvadrati: #{son ** 2}"
end
```

## Tushuntirish va Mantiq:
Blok parametrlari vertikal chiziqlar `|param1, param2|` orasida yoziladi. Metod qanday qiymat bersa, ular mos ravishda blok parametrlariga birikadi.

## Ishlash natijasi:
```text
1 ning kvadrati: 1
2 ning kvadrati: 4
3 ning kvadrati: 9
```


# 203-Topshiriq: Metod ichida blokni ishga tushirish: yield
## Topshiriq sharti:
O'z shaxsiy metod yarating va unga uzatilgan blokni yield yordamida chaqiring.

## Yechim (Ruby kodi):
```ruby
def takrorla_ikki_marta
  puts "Boshlanish"
  yield
  yield
  puts "Tugash"
end

takrorla_ikki_marta { puts "--> Blok bajarildi!" }
```

## Tushuntirish va Mantiq:
'yield' kalit so'zi metodga uzatilgan kod blokini chaqiradi va uning bajarilishini kutadi.

## Ishlash natijasi:
```text
Boshlanish
--> Blok bajarildi!
--> Blok bajarildi!
Tugash
```


# 204-Topshiriq: yield ga argumentlar uzatish
## Topshiriq sharti:
Metod ichidan blok parametriga ma'lumot uzating.

## Yechim (Ruby kodi):
```ruby
def foydalanuvchi_salomi
  yield("Alisher", "Navoiy")
end

foydalanuvchi_salomi do |ism, familiya|
  puts "Assalomu alaykum, #{ism} #{familiya}!"
end
```

## Tushuntirish va Mantiq:
'yield(arg1, arg2)' metod ichidagi qiymatlarni blokning `|p1, p2|` parametrlariga yetkazib beradi.

## Ishlash natijasi:
```text
Assalomu alaykum, Alisher Navoiy!
```


# 205-Topshiriq: yield dan qaytgan qiymatni qabul qilish
## Topshiriq sharti:
Blok hisoblagan natijani metod ichida qabul qilib, unga soliq qo'shing.

## Yechim (Ruby kodi):
```ruby
def soliq_qoshish
  asosiy_summa = yield
  soliq = asosiy_summa * 0.12
  asosiy_summa + soliq
end

yakuniy = soliq_qoshish { 50000 }
puts "Soliq bilan birga: #{yakuniy} so'm"
```

## Tushuntirish va Mantiq:
Blokdagi eng oxirgi ifodaning qiymati 'yield' chaqiruvining qaytaradigan natijasi bo'ladi.

## Ishlash natijasi:
```text
Soliq bilan birga: 56000.0 so'm
```


# 206-Topshiriq: Blok berilganligini tekshirish: block_given?
## Topshiriq sharti:
Metod blok bilan ham, bloksiz ham chaqirilganda xato bermasligini ta'minlang.

## Yechim (Ruby kodi):
```ruby
def hisobot_chiqar
  puts "--- HISOBOT ---"
  if block_given?
    yield
  else
    puts "Standart ma'lumot: Barcha tizimlar normal ishlamoqda."
  end
  puts "--- YAKUN ---"
end

hisobot_chiqar
hisobot_chiqar { puts "Maxsus ma'lumot: Server yuklamasi 85%" }
```

## Tushuntirish va Mantiq:
Agar metod ichida blok berilmagan bo'lsa va 'yield' chaqirilsa, Ruby 'LocalJumpError: no block given (yield)' xatosini tashlaydi. 'block_given?' orqali blok mavjudligini xavfsiz tekshirish mumkin.

## Ishlash natijasi:
```text
--- HISOBOT ---
Standart ma'lumot: Barcha tizimlar normal ishlamoqda.
--- YAKUN ---
--- HISOBOT ---
Maxsus ma'lumot: Server yuklamasi 85%
--- YAKUN ---
```


# 207-Topshiriq: Blok berilmaganda Enumerator qaytarish
## Topshiriq sharti:
Bloksiz chaqirilganda to_enum orqali zanjirli metodlarni qo'llab-quvvatlang.

## Yechim (Ruby kodi):
```ruby
def mening_raqamlarim
  return to_enum(:mening_raqamlarim) unless block_given?
  yield 10
  yield 20
  yield 30
end

# Blok bilan
mening_raqamlarim { |x| print "#{x} " }
puts ""

# Bloksiz chaqirib, Enumerator metodlaridan foydalanish
enum = mening_raqamlarim
puts "Enumerator orqali map: #{enum.map { |x| x * 2 }.inspect}"
```

## Tushuntirish va Mantiq:
Ruby standart kutubxonasidagi deyarli barcha metodlar (each, map) blok berilmaganda Enumerator qaytaradi. Bu `return to_enum(:metod)` orqali amalga oshiriladi.

## Ishlash natijasi:
```text
10 20 30 
Enumerator orqali map: [20, 40, 60]
```


# 208-Topshiriq: Blok ichidagi maxsus lokal o'zgaruvchilar: ; ajratuvchisi
## Topshiriq sharti:
Tashqi o'zgaruvchi blok ichida tasodifan o'zgarib ketmasligi uchun uni blok lokali sifatida ajrating.

## Yechim (Ruby kodi):
```ruby
x = "Tashqi qiymat"

[1, 2].each do |son; x|
  x = "Ichki qiymat #{son}"
  puts "Blok ichida: #{x}"
end

puts "Blokdan tashqarida x: #{x}"
```

## Tushuntirish va Mantiq:
Blok parametrlaridan so'ng nuqtali vergul (;) qo'yilib ro'yxat kiritilsa, bu o'zgaruvchilar blokning shaxsiy lokaliga aylanadi va tashqaridagi bir xil nomli o'zgaruvchiga ta'sir qilmaydi.

## Ishlash natijasi:
```text
Blok ichida: Ichki qiymat 1
Blok ichida: Ichki qiymat 2
Blokdan tashqarida x: Tashqi qiymat
```


# 209-Topshiriq: Closure tushunchasi: Tashqi leksik muhitni eslab qolish
## Topshiriq sharti:
Blok o'zi yaratilgan joydagi o'zgaruvchilarni qanday 'yopib' (close over) saqlab qolishini ko'rsating.

## Yechim (Ruby kodi):
```ruby
def hisoblagich_yarat
  son = 0
  Proc.new { son += 1 }
end

hisob1 = hisoblagich_yarat
puts "Birinchi chaqiruv: #{hisob1.call}"
puts "Ikkinchi chaqiruv: #{hisob1.call}"
puts "Uchinchi chaqiruv: #{hisob1.call}"
```

## Tushuntirish va Mantiq:
Blok va Proclar haqiqiy Closure (yopilish) hisoblanadi. Ular o'zgaruvchi qiymatini emas, o'zgaruvchining o'zini (reference) eslab qoladi va metod tugagandan keyin ham xotirada yashashda davom etadi.

## Ishlash natijasi:
```text
Birinchi chaqiruv: 1
Ikkinchi chaqiruv: 2
Uchinchi chaqiruv: 3
```


# 210-Topshiriq: Proc obyekti yaratish: Proc.new
## Topshiriq sharti:
Blokni qayta ishlatiladigan birinchi darajali (first-class) obyektga aylantiring.

## Yechim (Ruby kodi):
```ruby
salom_proc = Proc.new do |ism|
  puts "Salom, #{ism}!"
end

puts "Sinfi: #{salom_proc.class}"
salom_proc.call("Jasur")
salom_proc.call("Madina")
```

## Tushuntirish va Mantiq:
Ruby-da bloklar mustaqil obyekt emas, biroq `Proc.new` ularni to'laqonli `Proc` sinfi obyektiga aylantiradi va o'zgaruvchilarda saqlashga imkon beradi.

## Ishlash natijasi:
```text
Sinfi: Proc
Salom, Jasur!
Salom, Madina!
```


# 211-Topshiriq: Proc ni chaqirish usullari: call, [], === va .()
## Topshiriq sharti:
Proc obyektini ishga tushirishning barcha sintaktik shakllarini qo'llang.

## Yechim (Ruby kodi):
```ruby
kvadrat = Proc.new { |x| x * x }

puts "call orqali: #{kvadrat.call(5)}"
puts "[] orqali: #{kvadrat[5]}"
puts ".() orqali: #{kvadrat.(5)}"
puts "=== orqali: #{kvadrat === 5}"
```

## Tushuntirish va Mantiq:
Ruby-da Proc bir nechta usulda ishga tushiriladi: eng keng tarqalgoni `.call(args)`, qisqartmasi `[args]`, shuningdek `===` operatori (bu Proc-ni `case ... when` ichida ishlatishga imkon beradi).

## Ishlash natijasi:
```text
call orqali: 25
[] orqali: 25
.() orqali: 25
=== orqali: 25
```


# 212-Topshiriq: lambda yaratish: lambda va stumpy lambda ->()
## Topshiriq sharti:
Klassik va zamonaviy stumpy lambda sintaksislarini taqqoslang.

## Yechim (Ruby kodi):
```ruby
l1 = lambda { |a, b| a + b }
l2 = ->(a, b) { a * b } # Stumpy lambda

puts "l1 yig'indi: #{l1.call(3, 4)}"
puts "l2 ko'paytma: #{l2.call(3, 4)}"
puts "l2 lambda ekanligi: #{l2.lambda?}"
```

## Tushuntirish va Mantiq:
Ruby 1.9 da kiritilgan `->(param) { ... }` (stumpy lambda) sintaksisi lambdalarni qisqa va qulay yozish usulidir. Lambda ham `Proc` sinfiga tegishli, ammo maxsus bayroqqa (`lambda? == true`) ega.

## Ishlash natijasi:
```text
l1 yig'indi: 7
l2 ko'paytma: 12
l2 lambda ekanligi: true
```


# 213-Topshiriq: Proc va Lambda 1-farqi: Argumentlar qat'iyligi (Arity)
## Topshiriq sharti:
Proc va Lambda noto'g'ri sondagi argumentlar uzatilganda o'zini qanday tutishini ko'rsating.

## Yechim (Ruby kodi):
```ruby
oddiy_proc = Proc.new { |a, b| "a: #{a.inspect}, b: #{b.inspect}" }
oddiy_lambda = ->(a, b) { "a: #{a}, b: #{b}" }

# Proc ortiqcha argumentni tashlab yuboradi, yetmaganiga nil beradi
puts "Proc (1 ta arg): #{oddiy_proc.call(10)}"

# Lambda aniq argumentlar sonini talab qiladi (ArgumentError)
begin
  oddiy_lambda.call(10)
rescue ArgumentError => e
  puts "Lambda xatosi: #{e.class}"
end
```

## Tushuntirish va Mantiq:
Proc argumentlar soniga juda erkin (lenient) qaraydi: yetishmaganiga nil qo'yadi. Lambda esa oddiy metodlar kabi qat'iy (strict) tekshiradi va nomuvofiqlikda `ArgumentError` beradi.

## Ishlash natijasi:
```text
Proc (1 ta arg): a: 10, b: nil
Lambda xatosi: ArgumentError
```


# 214-Topshiriq: Proc va Lambda 2-farqi: return kalit so'zi
## Topshiriq sharti:
Proc va Lambda ichida 'return' ishlatilganda ko'rinish sohasidan chiqib ketish farqini ko'rsating.

## Yechim (Ruby kodi):
```ruby
def test_proc
  p = Proc.new { return "Proc-dan chiqish" }
  p.call
  "Metod oxiri" # Ushbu qatorga yetib kelmaydi!
end

def test_lambda
  l = -> { return "Lambda-dan chiqish" }
  natija = l.call
  "Metod oxiri (lambda qaytardi: #{natija})"
end

puts "test_proc natijasi: #{test_proc}"
puts "test_lambda natijasi: #{test_lambda}"
```

## Tushuntirish va Mantiq:
Proc ichidagi 'return' uni o'rab turgan tashqi butun metoddan chiqib ketadi. Lambda ichidagi 'return' esa faqat lambdaning o'zidan qiymat qaytaradi va tashqi metod o'z ishini davom ettiradi.

## Ishlash natijasi:
```text
test_proc natijasi: Proc-dan chiqish
test_lambda natijasi: Metod oxiri (lambda qaytardi: Lambda-dan chiqish)
```


# 215-Topshiriq: Metod argumentida blokni Proc ga aylantirish: &blok
## Topshiriq sharti:
Metodga kelgan blokni nomli Proc o'zgaruvchisiga oling.

## Yechim (Ruby kodi):
```ruby
def amaliyot_bajar(nom, &harakat)
  puts "Boshlanmoqda: #{nom}"
  puts "Harakat sinfi: #{harakat.class}"
  harakat.call
  puts "Tugallandi."
end

amaliyot_bajar("Fayllarni tozalash") do
  puts "--> 15 ta kesh fayl o'chirildi."
end
```

## Tushuntirish va Mantiq:
Metod parametrlarining eng oxirida `&o'zgaruvchi` yozilsa, unga uzatilgan blok avtomatik `Proc` obyektiga o'giriladi va metod ichida saqlash yoki boshqa joyga uzatish mumkin bo'ladi.

## Ishlash natijasi:
```text
Boshlanmoqda: Fayllarni tozalash
Harakat sinfi: Proc
--> 15 ta kesh fayl o'chirildi.
Tugallandi.
```


# 216-Topshiriq: Proc ni metodga blok sifatida uzatish: &proc
## Topshiriq sharti:
Mavjud Proc obyektini metodga oddiy blok sifatida yuboring.

## Yechim (Ruby kodi):
```ruby
kvadrat_proc = Proc.new { |n| n ** 2 }
natijalar = [1, 2, 3, 4].map(&kvadrat_proc)

puts "Kvadratlar: #{natijalar.inspect}"
```

## Tushuntirish va Mantiq:
Metod chaqiruvida argument oldiga `&` qo'yilsa, Ruby o'sha obyektning `to_proc` metodini chaqirib, uni oddiy blok shaklida metodga uzatadi.

## Ishlash natijasi:
```text
Kvadratlar: [1, 4, 9, 16]
```


# 217-Topshiriq: Symbol-to-Proc sehri: &:metod
## Topshiriq sharti:
Massivdagi barcha satrlarni &:upcase orqali bosh harfga aylantiring.

## Yechim (Ruby kodi):
```ruby
shaharlar = ["toshkent", "samarqand", "buxoro"]
bosh_harfli = shaharlar.map(&:upcase)

puts "Bosh harfli: #{bosh_harfli.inspect}"
```

## Tushuntirish va Mantiq:
`shaharlar.map(&:upcase)` aslida `shaharlar.map { |sh| sh.upcase }` ning qisqartmasidir. Symbol sinfida `to_proc` metodi aniqlangan bo'lib, u kelgan birinchi argument ustida ushbu nomli metodni chaqiruvchi Proc qaytaradi.

## Ishlash natijasi:
```text
Bosh harfli: ["TOSHKENT", "SAMARQAND", "BUXORO"]
```


# 218-Topshiriq: O'z sinfida to_proc metodini aniqlash
## Topshiriq sharti:
O'z maxsus sinfingizni & operatori bilan ishlashga moslashtiring.

## Yechim (Ruby kodi):
```ruby
class Kopaytiruvchi
  def initialize(koeffitsiyent)
    @k = koeffitsiyent
  end

  def to_proc
    Proc.new { |x| x * @k }
  end
end

ikki_karra = Kopaytiruvchi.new(2)
natija = [10, 20, 30].map(&ikki_karra)

puts "Ikki karra: #{natija.inspect}"
```

## Tushuntirish va Mantiq:
Har qanday sinfda `to_proc` metodini yaratib, uning obyektlarini `&` operatori orqali to'g'ridan-to'g'ri blok talab qiladigan metodlarga uzatish mumkin.

## Ishlash natijasi:
```text
Ikki karra: [20, 40, 60]
```


# 219-Topshiriq: Hash uchun to_proc (Ruby 2.3+)
## Topshiriq sharti:
Hash obyektini & orqali to'g'ridan-to'g'ri map metodiga uzating.

## Yechim (Ruby kodi):
```ruby
lugat = { uz: "O'zbekiston", en: "Angliya", ru: "Rossiya" }
kalitlar = [:uz, :en]

nomlar = kalitlar.map(&lugat)
puts "Topilgan nomlar: #{nomlar.inspect}"
```

## Tushuntirish va Mantiq:
Ruby 2.3 dan boshlab Hash sinfi ham `to_proc` ga ega. `&hash` chaqiruvi `Proc.new { |k| hash[k] }` ga teng bo'lib, kalitlar bo'yicha tezkor xaritaga aylantiradi.

## Ishlash natijasi:
```text
Topilgan nomlar: ["O'zbekiston", "Angliya"]
```


# 220-Topshiriq: Metodni Proc ga aylantirish: method(:nomi).to_proc
## Topshiriq sharti:
Mavjud oddiy metodni Proc ga o'girib, boshqa funksiyalarga uzating.

## Yechim (Ruby kodi):
```ruby
def kub(x)
  x ** 3
end

kub_proc = method(:kub).to_proc
puts "Kublar: #{[1, 2, 3].map(&kub_proc).inspect}"
```

## Tushuntirish va Mantiq:
`method(:nomi)` orqali har qanday mavjud metod 'Method' obyektiga olinadi va `to_proc` yordamida erkin uzatiladi.

## Ishlash natijasi:
```text
Kublar: [1, 8, 27]
```


# 221-Topshiriq: Proc karrilash: curry metodi
## Topshiriq sharti:
Uchta argument qabul qiluvchi funksiyani bosqichma-bosqich qisman qo'llang.

## Yechim (Ruby kodi):
```ruby
qoshuvchi = ->(a, b, c) { a + b + c }
karri = qoshuvchi.curry

qosh_10 = karri.call(10)
qosh_10_va_20 = qosh_10.call(20)
yakuniy = qosh_10_va_20.call(5)

puts "Yakuniy yig'indi: #{yakuniy}"
```

## Tushuntirish va Mantiq:
'curry' ko'p argumentli funksiyani bittalab argument oluvchi zanjirli funksiyalarga ajratadi (Currying).

## Ishlash natijasi:
```text
Yakuniy yig'indi: 35
```


# 222-Topshiriq: Lambda karrilash bilan soliq hisoblash
## Topshiriq sharti:
Turli davlatlar uchun soliq hisoblovchi ixtisoslashgan funksiyalarni curry orqali yarating.

## Yechim (Ruby kodi):
```ruby
soliq_hisoblagich = ->(stavka, summa) { summa + (summa * stavka) }.curry

uz_soliq = soliq_hisoblagich.call(0.12)
aqsh_soliq = soliq_hisoblagich.call(0.08)

puts "O'zbekistonda 100 000 so'm: #{uz_soliq.call(100_000).to_i}"
puts "AQShda $100: #{aqsh_soliq.call(100).to_i}"
```

## Tushuntirish va Mantiq:
Currying yordamida umumiy matematik modellardan aniq ixtisoslashgan hisoblagichlarni oson hosil qilish mumkin.

## Ishlash natijasi:
```text
O'zbekistonda 100 000 so'm: 112000
AQShda $100: 108
```


# 223-Topshiriq: Proc arity: argumentlar sonini aniqlash
## Topshiriq sharti:
Funksiya nechta parametr kutayotganini dasturiy ravishda aniqlang.

## Yechim (Ruby kodi):
```ruby
p1 = ->(x) { x }
p2 = ->(a, b) { a + b }
p3 = ->(a, *rest) { a }

puts "p1 arity: #{p1.arity}"
puts "p2 arity: #{p2.arity}"
puts "p3 arity: #{p3.arity}"
```

## Tushuntirish va Mantiq:
'arity' qat'iy argumentlar sonini qaytaradi. Ixtiyoriy yoki splat argumentlar bo'lsa manfiy son qaytadi.

## Ishlash natijasi:
```text
p1 arity: 1
p2 arity: 2
p3 arity: -2
```


# 224-Topshiriq: Funksiyalar kompozitsiyasi (Ruby 2.6+): >> va <<
## Topshiriq sharti:
Ikkita mustaqil funksiyani birlashtirib yangi funksiya quvuri (Pipeline) hosil qiling.

## Yechim (Ruby kodi):
```ruby
ikki_karra = ->(x) { x * 2 }
bir_qosh = ->(x) { x + 1 }

# >> chapdan o'ngga: avval ikki_karra, keyin bir_qosh
quvur1 = ikki_karra >> bir_qosh

# << o'ngdan chapga: avval bir_qosh, keyin ikki_karra
quvur2 = ikki_karra << bir_qosh

puts "(5 * 2) + 1: #{quvur1.call(5)}"
puts "(5 + 1) * 2: #{quvur2.call(5)}"
```

## Tushuntirish va Mantiq:
Ruby 2.6 da kiritilgan `>>` va `<<` operatorlari matematik funksiyalar kompozitsiyasini amalga oshiradi: `f >> g` bu `g(f(x))` demakdir.

## Ishlash natijasi:
```text
(5 * 2) + 1: 11
(5 + 1) * 2: 12
```


# 225-Topshiriq: Bloklar yordamida Benchmark (kod ishlash vaqtini o'lchash)
## Topshiriq sharti:
Har qanday kod blokining bajarilish davomiyligini o'lchovchi wrapper yozing.

## Yechim (Ruby kodi):
```ruby
def vaqtni_olcha(amal_nomi)
  boshlanish = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  yield
  tugash = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  farq = tugash - boshlanish
  puts "#{amal_nomi} bajarildi: #{farq.round(4)} soniya"
end

vaqtni_olcha("Katta massiv yig'indisi") do
  (1..100_000).sum
end
```

## Tushuntirish va Mantiq:
Around-pattern vositasida blokdan oldin va keyin zarur ko'rsatmalarni (benchmark, tranzaksiya, xavfsizlik) bajarish mumkin.

## Ishlash natijasi:
```text
Katta massiv yig'indisi bajarildi: 0.003 soniya
```


# 226-Topshiriq: Bloklar bilan resurslarni avtomatik yopish (Around pattern)
## Topshiriq sharti:
Fayl yoki ulanish ochiq qolib ketmasligini kafolatlovchi xavfsiz blok yarating.

## Yechim (Ruby kodi):
```ruby
class SoxtaBazaUlanishi
  def ochish; puts "Baza ulandi."; end
  def yopish; puts "Baza ulanishi xavfsiz yopildi."; end
  def sorov; puts "SQL so'rov bajarildi."; end

  def self.ochiq_ishlatish
    db = new
    db.ochish
    begin
      yield(db)
    ensure
      db.yopish
    end
  end
end

SoxtaBazaUlanishi.ochiq_ishlatish do |baza|
  baza.sorov
end
```

## Tushuntirish va Mantiq:
Blok va 'ensure' kombinatsiyasi dasturda xatolik yuz berganda ham resurslar (xotira, fayl deskriptorlari, soketlar) 100% yopilishini ta'minlaydi.

## Ishlash natijasi:
```text
Baza ulandi.
SQL so'rov bajarildi.
Baza ulanishi xavfsiz yopildi.
```


# 227-Topshiriq: Blok orqali obyekt konfiguratsiyasi (Config Block)
## Topshiriq sharti:
Gem va kutubxonalarda qo'llaniladigan `configure do |config|` arxitekturasini yarating.

## Yechim (Ruby kodi):
```ruby
class TizimKonfiguratsiyasi
  attr_accessor :server, :port, :timeout

  def initialize
    @port = 80
    @timeout = 30
  end
end

def sozlash
  konfig = TizimKonfiguratsiyasi.new
  yield(konfig) if block_given?
  konfig
end

sozlama = sozlash do |c|
  c.server = "https://khorazmiy.uz"
  c.port = 443
  c.timeout = 60
end

puts "Server: #{sozlama.server}:#{sozlama.port}, timeout: #{sozlama.timeout}s"
```

## Tushuntirish va Mantiq:
Config Block namunasi Ruby on Rails konfiguratsiyalarida (masalan `config/environments/production.rb`) eng mashhur arxitektura hisoblanadi.

## Ishlash natijasi:
```text
Server: https://khorazmiy.uz:443, timeout: 60s
```


# 228-Topshiriq: O'z shaxsiy each metodini yaratish
## Topshiriq sharti:
Massiv nusxasini ishlatmasdan o'z maxsus konteyner sinfingizda blokli iteratsiya quring.

## Yechim (Ruby kodi):
```ruby
class JuftSonlar
  def initialize(chegara)
    @chegara = chegara
  end

  def each
    (2..@chegara).step(2) do |son|
      yield son
    end
  end
end

juftlar = JuftSonlar.new(6)
juftlar.each { |j| print "#{j} " }
puts ""
```

## Tushuntirish va Mantiq:
Har qanday sinfda `def each` yozib, ichida `yield` chaqirilsa, sinf to'liq bloklarni qabul qiladigan konteynerga aylanadi.

## Ishlash natijasi:
```text
2 4 6
```


# 229-Topshiriq: O'z shaxsiy map metodini yozish
## Topshiriq sharti:
Array#map qanday ishlashini noldan o'z funksiyangiz bilan takrorlang.

## Yechim (Ruby kodi):
```ruby
def mening_mapim(massiv)
  natija = []
  massiv.each do |element|
    natija << yield(element)
  end
  natija
end

kvadratlar = mening_mapim([1, 2, 3]) { |x| x * x }
puts "Kvadratlar: #{kvadratlar.inspect}"
```

## Tushuntirish va Mantiq:
map har bir elementni blok orqali o'tkazib, yangi massivga yig'adi.

## Ishlash natijasi:
```text
Kvadratlar: [1, 4, 9]
```


# 230-Topshiriq: O'z shaxsiy select metodini yozish
## Topshiriq sharti:
Filtrlovchi select metodini yield yordamida noldan yasang.

## Yechim (Ruby kodi):
```ruby
def mening_selectim(massiv)
  saralangan = []
  massiv.each do |item|
    saralangan << item if yield(item)
  end
  saralangan
end

juftlar = mening_selectim([1, 2, 3, 4, 5, 6]) { |x| x.even? }
puts "Juftlar: #{juftlar.inspect}"
```

## Tushuntirish va Mantiq:
select metodi blok qachon true qaytarsa o'sha elementni qoldiradi.

## Ishlash natijasi:
```text
Juftlar: [2, 4, 6]
```


# 231-Topshiriq: O'z shaxsiy reduce / inject metodini yozish
## Topshiriq sharti:
To'plamni yagona yakuniy qiymatga yig'uvchi (accumulator) mantiqni yarating.

## Yechim (Ruby kodi):
```ruby
def mening_reducem(massiv, boshlangich)
  akkumulyator = boshlangich
  massiv.each do |element|
    akkumulyator = yield(akkumulyator, element)
  end
  akkumulyator
end

yigindi = mening_reducem([1, 2, 3, 4], 0) { |sum, x| sum + x }
kopaytma = mening_reducem([1, 2, 3, 4], 1) { |prod, x| prod * x }

puts "Yig'indi: #{yigindi}"
puts "Ko'paytma: #{kopaytma}"
```

## Tushuntirish va Mantiq:
reduce har bir qadamda o'tgan qadam natijasini joriy element bilan yangilaydi.

## Ishlash natijasi:
```text
Yig'indi: 10
Ko'paytma: 24
```


# 232-Topshiriq: Blok ichida next bilan qiymat qaytarish
## Topshiriq sharti:
Iteratsiya paytida shart bajarilmasa 'next qiymat' orqali muqobil javob bering.

## Yechim (Ruby kodi):
```ruby
natijalar = [1, 2, 3, 4, 5].map do |son|
  next "Toq" if son.odd?
  son * 10
end

puts "Natijalar: #{natijalar.inspect}"
```

## Tushuntirish va Mantiq:
'map' kabi metodlarda 'next qiymat' yozilsa, ushbu iteratsiya uchun berilgan qiymat saqlanadi va keyingi elementga o'tiladi.

## Ishlash natijasi:
```text
Natijalar: ["Toq", 20, "Toq", 40, "Toq"]
```


# 233-Topshiriq: Blok ichida break ning harakati
## Topshiriq sharti:
Blok ichida chaqirilgan break butun metodni to'xtatishini ko'rsating.

## Yechim (Ruby kodi):
```ruby
def sanagich
  yield 1
  yield 2
  yield 3
  "Metod yakuniga yetdi"
end

natija = sanagich do |son|
  puts "Qabul qilindi: #{son}"
  break "Blokdan to'xtatildi!" if son == 2
end

puts "Natija: #{natija}"
```

## Tushuntirish va Mantiq:
Blok ichidagi 'break' nafaqat blokni, balki ushbu blokni chaqirgan butun tashqi metodni darhol to'xtatadi va 'break' ga berilgan qiymatni qaytaradi.

## Ishlash natijasi:
```text
Qabul qilindi: 1
Qabul qilindi: 2
Natija: Blokdan to'xtatildi!
```


# 234-Topshiriq: Hodisalarni tinglovchi (Event Listener) tizimi Procs bilan
## Topshiriq sharti:
Hodisalar yuz berganda ro'yxatdan o'tgan barcha Proc larni chaqiruvchi Event Bus tuzing.

## Yechim (Ruby kodi):
```ruby
class HodisalarMarkazi
  def initialize
    @tinglovchilar = Hash.new { |h, k| h[k] = [] }
  end

  def obuna(hodisa_nomi, &blok)
    @tinglovchilar[hodisa_nomi] << blok
  end

  def chaqir(hodisa_nomi, ma_lumot)
    @tinglovchilar[hodisa_nomi].each { |tinglovchi| tinglovchi.call(ma_lumot) }
  end
end

bus = HodisalarMarkazi.new
bus.obuna(:tolov) { |d| puts "SMS yuborildi: #{d[:summa]} so'm yechildi." }
bus.obuna(:tolov) { |d| puts "Telegram botga xabar ketdi: Foydalanuvchi #{d[:user]}" }

bus.chaqir(:tolov, { summa: 150_000, user: "Alisher" })
```

## Tushuntirish va Mantiq:
Observer va Event Listener patternlari Ruby-da Proclar orqali juda yengil va modulli tarzda quriladi.

## Ishlash natijasi:
```text
SMS yuborildi: 150000 so'm yechildi.
Telegram botga xabar ketdi: Foydalanuvchi Alisher
```


# 235-Topshiriq: Filtrlar zanjiri (Middleware Pipeline) bloklar yordamida
## Topshiriq sharti:
So'rovni ketma-ket bir nechta filtrlar orqali o'tkazuvchi zanjir yarating.

## Yechim (Ruby kodi):
```ruby
autentifikatsiya = ->(req) { req[:user] ? req.merge(auth: true) : req }
tozalash = ->(req) { req.merge(matn: req[:matn].strip.downcase) }

sorov = { user: "admin", matn: "   Salom Dunyo!   " }
zanjir = autentifikatsiya >> tozalash
yakuniy = zanjir.call(sorov)

puts "Qayta ishlangan so'rov: #{yakuniy.inspect}"
```

## Tushuntirish va Mantiq:
Funksional kompozitsiya yordamida HTTP middleware (masalan Rack) modullarini bir-biriga ulash juda sodda kechadi.

## Ishlash natijasi:
```text
Qayta ishlangan so'rov: {:user=>"admin", :matn=>"salom dunyo!", :auth=>true}
```


# 236-Topshiriq: Xotirani tejovchi generatorlar (Fibonacci Stream)
## Topshiriq sharti:
Cheksiz Fibonachchi ketma-ketligini faqat so'ralganda hisoblovchi blokli generator yozing.

## Yechim (Ruby kodi):
```ruby
def cheksiz_fibonachchi
  a, b = 0, 1
  loop do
    yield a
    a, b = b, a + b
  end
end

topilgan = []
cheksiz_fibonachchi do |son|
  topilgan << son
  break if topilgan.size >= 7
end

puts "Dastlabki 7 ta Fibonachchi: #{topilgan.inspect}"
```

## Tushuntirish va Mantiq:
Generatorlar xotirada millionlab sonlarni birdan saqlamasdan, har safar faqat bitta qiymatni hisoblab blok orqali uzatadi (Lazy evaluation).

## Ishlash natijasi:
```text
Dastlabki 7 ta Fibonachchi: [0, 1, 1, 2, 3, 5, 8]
```


# 237-Topshiriq: Dinamik predikatlar generatori
## Topshiriq sharti:
Berilgan songa bo'linishni tekshiruvchi maxsus lambda ishlab chiqaruvchi funksiya yozing.

## Yechim (Ruby kodi):
```ruby
def bolinish_tekshirgich(boluvchi)
  ->(son) { son % boluvchi == 0 }
end

uchga_bolinadimi = bolinish_tekshirgich(3)
beshga_bolinadimi = bolinish_tekshirgich(5)

puts "15 uchga bo'linadimi? #{uchga_bolinadimi.call(15)}"
puts "16 uchga bo'linadimi? #{uchga_bolinadimi.call(16)}"
puts "20 beshga bo'linadimi? #{beshga_bolinadimi.call(20)}"
```

## Tushuntirish va Mantiq:
Yuqori tartibli funksiyalar (Higher-order functions) yangi maxsus predikat funksiyalar ishlab chiqarish imkonini beradi.

## Ishlash natijasi:
```text
15 uchga bo'linadimi? true
16 uchga bo'linadimi? false
20 beshga bo'linadimi? true
```


# 238-Topshiriq: Blok yordamida HTML teglarini o'rab chiquvchi helper
## Topshiriq sharti:
Veb shablonlarida HTML teglarini chiroyli ichma-ich generatsiya qiling.

## Yechim (Ruby kodi):
```ruby
def teg(nom)
  "<#{nom}>" + yield + "</#{nom}>"
end

html = teg("div") do
  teg("p") do
    teg("strong") { "Muhim bildirishnoma!" }
  end
end

puts html
```

## Tushuntirish va Mantiq:
Bloklar orqali deklarativ DSL shablonlari (masalan Markaby, HTML builderlar) yaratiladi.

## Ishlash natijasi:
```text
<div><p><strong>Muhim bildirishnoma!</strong></p></div>
```


# 239-Topshiriq: Binding obyekti va kontekstni ko'chirish
## Topshiriq sharti:
Metod ichidagi o'zgaruvchilar muhitini binding orqali ushlab, tashqarida eval qiling.

## Yechim (Ruby kodi):
```ruby
def sirli_xona
  parol = "Khorazmiy_2026"
  binding
end

muhit = sirli_xona
puts "Muhit sinfi: #{muhit.class}"
puts "Tashqaridan o'qilgan parol: #{eval('parol', muhit)}"
```

## Tushuntirish va Mantiq:
'binding' obyekti joriy ko'rinish sohasidagi barcha o'zgaruvchilar, metodlar va 'self' kontekstini o'zida muhrlab oladi.

## Ishlash natijasi:
```text
Muhit sinfi: Binding
Tashqaridan o'qilgan parol: Khorazmiy_2026
```


# 240-Topshiriq: Tranzaksiya bloklari va xatoda orqaga qaytish (Rollback)
## Topshiriq sharti:
Bank hisoblaridagi o'zgarishlar xatolik yuz berganda avtomatik bekor qilinishini ta'minlang.

## Yechim (Ruby kodi):
```ruby
def tranzaksiya(hisob)
  boshlangich = hisob.dup
  puts "Tranzaksiya boshlandi: #{hisob.inspect}"
  begin
    yield
    puts "Tranzaksiya muvaffaqiyatli saqlandi!"
  rescue => e
    hisob.replace(boshlangich)
    puts "XATOLIK! O'zgarishlar bekor qilindi (Rollback): #{e.message}"
  end
end

hisoblar = { Ali: 100, Vali: 50 }

tranzaksiya(hisoblar) do
  hisoblar[:Ali] -= 80
  hisoblar[:Vali] += 80
  raise "Tarmoq uzildi!" if true
end

puts "Yakuniy hisob: #{hisoblar.inspect}"
```

## Tushuntirish va Mantiq:
Tranzaksiya bloklari ma'lumotlar yaxlitligini xavf ostiga qo'ymasdan xavfsiz boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Tranzaksiya boshlandi: {:Ali=>100, :Vali=>50}
XATOLIK! O'zgarishlar bekor qilindi (Rollback): Tarmoq uzildi!
Yakuniy hisob: {:Ali=>100, :Vali=>50}
```


# 241-Topshiriq: Lambda massivlari va ketma-ketlikda ishga tushirish
## Topshiriq sharti:
Bir nechta validatsiya qoidalarini massivga yig'ib, tartib bilan tekshiring.

## Yechim (Ruby kodi):
```ruby
qoidalar = [
  ->(matn) { matn.length >= 6 ? true : "Parol kamida 6 belgidan iborat bo'lishi kerak" },
  ->(matn) { matn =~ /\d/ ? true : "Parolda kamida bitta raqam bo'lishi kerak" }
]

parol = "sir"
xatolar = []

qoidalar.each do |qoida|
  natija = qoida.call(parol)
  xatolar << natija if natija != true
end

puts "Aniqlangan xatolar: #{xatolar.inspect}"
```

## Tushuntirish va Mantiq:
Lambdalardan iborat massivlar qoidalar dvigateli (Rule engine) va validatsiya tizimlarini modulli qilish imkonini beradi.

## Ishlash natijasi:
```text
Aniqlangan xatolar: ["Parol kamida 6 belgidan iborat bo'lishi kerak", "Parolda kamida bitta raqam bo'lishi kerak"]
```


# 242-Topshiriq: Proc#to_s va tekshiruv (Inspection)
## Topshiriq sharti:
Proc qaysi faylda va nechanchi qatorda yaratilganini ko'ring.

## Yechim (Ruby kodi):
```ruby
p = Proc.new { "Test" }
puts "Proc inspection: #{p.inspect.include?('Proc')}"
puts "Source location mavjudmi: #{!p.source_location.nil?}"
```

## Tushuntirish va Mantiq:
'source_location' metodi `[fayl_yo'li, qator_raqami]` massivini qaytaradi. Bu yirik freymvorklarda debug qilishda nihoyatda qimmatli ma'lumotdir.

## Ishlash natijasi:
```text
Proc inspection: true
Source location mavjudmi: true
```


# 243-Topshiriq: Blok bilan takroriy urinish (Retry with backoff) mexanizmi
## Topshiriq sharti:
Muvaffaqiyatsiz bo'lgan tarmoq so'rovini belgilangan martagacha qayta urinuvchi blokli metod yozing.

## Yechim (Ruby kodi):
```ruby
def qayta_urin(maksimal = 3)
  urinishlar = 0
  begin
    urinishlar += 1
    yield(urinishlar)
  rescue => e
    if urinishlar < maksimal
      puts "Xatolik: #{e.message}. #{urinishlar}-urinish muvaffaqiyatsiz. Qayta urinilmoqda..."
      retry
    else
      puts "Barcha #{maksimal} ta urinish tugadi."
    end
  end
end

qayta_urin(3) do |urinish|
  puts "So'rov yuborilmoqda (#{urinish})..."
  raise "Server 503 javob berdi" if urinish < 3
  puts "Muvaffaqiyatli ulandi!"
end
```

## Tushuntirish va Mantiq:
Blok ichidagi xatoliklarni 'retry' orqali qayta urinish tarmoq uzilishlari va vaqtinchalik xatolarni yengishda standart usuldir.

## Ishlash natijasi:
```text
So'rov yuborilmoqda (1)...
Xatolik: Server 503 javob berdi. 1-urinish muvaffaqiyatsiz. Qayta urinilmoqda...
So'rov yuborilmoqda (2)...
Xatolik: Server 503 javob berdi. 2-urinish muvaffaqiyatsiz. Qayta urinilmoqda...
So'rov yuborilmoqda (3)...
Muvaffaqiyatli ulandi!
```


# 244-Topshiriq: Blok orqali obyekt nusxasini xavfsiz boshqarish (tap metodi)
## Topshiriq sharti:
Obyekt ustida amallarni bajarib, zanjirli o'zgaruvchisiz obyektning o'zini qaytaruvchi tap metodidan foydalaning.

## Yechim (Ruby kodi):
```ruby
foydalanuvchi = { ism: "Sardor" }.tap do |u|
  u[:rol] = "developer"
  u[:shahar] = "Toshkent"
  puts "Obyekt sozlandi: #{u.inspect}"
end

puts "Yakuniy foydalanuvchi: #{foydalanuvchi.inspect}"
```

## Tushuntirish va Mantiq:
Kernel#tap metodi obyektni o'z blokiga uzatadi va blok yakunida har doim obyektning o'zini qaytaradi. Bu oraliq o'zgaruvchilarsiz zanjirli kod yozish imkonini beradi.

## Ishlash natijasi:
```text
Obyekt sozlandi: {:ism=>"Sardor", :rol=>"developer", :shahar=>"Toshkent"}
Yakuniy foydalanuvchi: {:ism=>"Sardor", :rol=>"developer", :shahar=>"Toshkent"}
```


# 245-Topshiriq: then / yield_self (Ruby 2.6+)
## Topshiriq sharti:
Qiymatni blok orqali boshqa qiymatga aylantiruvchi zamonaviy 'then' metodini qo'llang.

## Yechim (Ruby kodi):
```ruby
natija = "  khorazmiy ai  "
  .strip
  .upcase
  .then { |matn| "[RASMIY: #{matn}]" }

puts natija
```

## Tushuntirish va Mantiq:
'then' (sinonimi 'yield_self') qiymatni blok parametriga beradi va blok natijasini keyingi metodga uzatadi. Bu Elixir yoki OCaml-dagi quvur (pipe) operatoriga o'xshaydi.

## Ishlash natijasi:
```text
[RASMIY: KHORAZMIY AI]
```


# 246-Topshiriq: Blok parametrlari destrukturizatsiyasi
## Topshiriq sharti:
Juftliklar massividan kalit va qiymatni alohida parametrlar sifatida qabul qiling.

## Yechim (Ruby kodi):
```ruby
juftliklar = [[:olma, 10], [:anor, 20]]

juftliklar.each do |(meva, narx)|
  puts "Meva: #{meva}, Narx: #{narx}"
end
```

## Tushuntirish va Mantiq:
Blok parametrlarida `|(a, b)|` qavslar qo'yilishi ichki massiv elementlarini avtomatik alohida o'zgaruvchilarga ajratadi.

## Ishlash natijasi:
```text
Meva: olma, Narx: 10
Meva: anor, Narx: 20
```


# 247-Topshiriq: Proc obyektlarining tengligi
## Topshiriq sharti:
Ikkita Proc obyekti teng yoki teng emasligini solishtiring.

## Yechim (Ruby kodi):
```ruby
p1 = Proc.new { "salom" }
p2 = Proc.new { "salom" }
p3 = p1

puts "p1 == p2: #{p1 == p2}"
puts "p1 == p3: #{p1 == p3}"
```

## Tushuntirish va Mantiq:
Proclar hatto bir xil kodga ega bo'lsa ham har safar yangi obyekt yaratiladi (`p1 != p2`). Faqat bitta manzilga ishora qilingandagina teng bo'ladi.

## Ishlash natijasi:
```text
p1 == p2: false
p1 == p3: true
```


# 248-Topshiriq: Bloklar bilan memoization (Keshlashtirish) dekoratori
## Topshiriq sharti:
Og'ir hisob-kitoblarni faqat bir marta bajarib natijani eslab qoluvchi blokli tizim yarating.

## Yechim (Ruby kodi):
```ruby
def kesh(kalit, xotira = {})
  xotira[kalit] ||= yield
end

kesh_xotirasi = {}

r1 = kesh(:faktorial_5, kesh_xotirasi) { (1..5).inject(:*) }
r2 = kesh(:faktorial_5, kesh_xotirasi) { puts "Qayta hisoblanmasligi kerak!"; 999 }

puts "Natija 1: #{r1}"
puts "Natija 2 (keshdan): #{r2}"
```

## Tushuntirish va Mantiq:
Bloklar va `||=` operatori orqali natijani keshlashtirish yuqori unumdor tizimlarning asosi hisoblanadi.

## Ishlash natijasi:
```text
Natija 1: 120
Natija 2 (keshdan): 120
```


# 249-Topshiriq: Lambda ichida rejim tanlash: Method Dispatching
## Topshiriq sharti:
Amal turiga qarab tegishli lambdani tanlab ishlatuvchi kalkulyator tuzing.

## Yechim (Ruby kodi):
```ruby
amallar = {
  qoshish: ->(a, b) { a + b },
  ayirish: ->(a, b) { a - b },
  kopaytirish: ->(a, b) { a * b }
}

def hisobla(amallar, turi, a, b)
  amallar[turi].call(a, b)
end

puts "10 + 5 = #{hisobla(amallar, :qoshish, 10, 5)}"
puts "10 * 5 = #{hisobla(amallar, :kopaytirish, 10, 5)}"
```

## Tushuntirish va Mantiq:
Hash ichida lambdalarni saqlash katta if-else bloklaridan xalos qiladi va dasturni kengaytirishni osonlashtiradi.

## Ishlash natijasi:
```text
10 + 5 = 15
10 * 5 = 50
```


# 250-Topshiriq: Amaliy loyiha: Funksional ETL (Extract, Transform, Load) ma'lumotlar quvuri
## Topshiriq sharti:
Foydalanuvchilar ma'lumotlarini qabul qilib, ularni tozalovchi, formatlovchi va hisobot shakliga keltiruvchi to'liq funksional quvur yarating.

## Yechim (Ruby kodi):
```ruby
xom_malumotlar = [
  { ism: "  anvar aliyev ", yosh: "28", shahar: "toshkent" },
  { ism: "nodira ganiyeva  ", yosh: "22", shahar: "samarqand" },
  { ism: "  jasur karimov", yosh: "31", shahar: "buxoro" }
]

tozalash = ->(user) do
  {
    ism: user[:ism].strip.split.map(&:capitalize).join(" "),
    yosh: user[:yosh].to_i,
    shahar: user[:shahar].strip.capitalize
  }
end

filtr = ->(user) { user[:yosh] >= 25 }

formatlash = ->(user) do
  "Xodim: #{user[:ism].ljust(18)} | Yoshi: #{user[:yosh]} | Shahar: #{user[:shahar]}"
end

# ETL Quvuri
yakuniy_hisobot = xom_malumotlar
  .map(&tozalash)
  .select(&filtr)
  .map(&formatlash)

puts "=========================================================="
puts "KOMPANIYA 25+ YOSHLI XODIMLARINING TOZALANGAN HISOBOTI"
puts "=========================================================="
yakuniy_hisobot.each { |qator| puts qator }
puts "=========================================================="
```

## Tushuntirish va Mantiq:
Ushbu amaliy loyihada Ruby bloklari, lambdalar, Proc konvertatsiyalari (&operator), massivlar, satr tozalash va funksional kompozitsiya to'liq birlashtirildi.

## Ishlash natijasi:
```text
==========================================================
KOMPANIYA 25+ YOSHLI XODIMLARINING TOZALANGAN HISOBOTI
==========================================================
Xodim: Anvar Aliyev       | Yoshi: 28 | Shahar: Toshkent
Xodim: Jasur Karimov      | Yoshi: 31 | Shahar: Buxoro
==========================================================
```

