# -*- coding: utf-8 -*-
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_05 = [
    (
        201,
        "Blok tushunchasi: do ... end va { ... } sintaksislari",
        "Bir qatorli va ko'p qatorli bloklar yordamida xabarlarni takrorlang.",
        """# Bir qatorli blok odatda { ... } bilan yoziladi
3.times { puts "Bir qatorli blok!" }

# Ko'p qatorli blok do ... end bilan yoziladi
2.times do
  puts "Ko'p qatorli"
  puts "blok ijrosi"
end
""",
        "Ruby-da kod bloklari mustaqil obyekt emas, ular faqat metod chaqiruviga biriktiriladigan anonim kod parchalaridir. Konvensiyaga ko'ra bir qatorli amallar `{ ... }`, ko'p qatorli amallar esa `do ... end` bilan o'raladi.",
        """Bir qatorli blok!
Bir qatorli blok!
Bir qatorli blok!
Ko'p qatorli
blok ijrosi
Ko'p qatorli
blok ijrosi"""
    ),
    (
        202,
        "Blok parametrlarini qabul qilish: |param|",
        "Blok ichida kelayotgan qiymatni qabul qilib, uning kvadratini chiqaring.",
        """[1, 2, 3].each do |son|
  puts "#{son} ning kvadrati: #{son ** 2}"
end
""",
        "Blok parametrlari vertikal chiziqlar `|param1, param2|` orasida yoziladi. Metod qanday qiymat bersa, ular mos ravishda blok parametrlariga birikadi.",
        """1 ning kvadrati: 1
2 ning kvadrati: 4
3 ning kvadrati: 9"""
    ),
    (
        203,
        "Metod ichida blokni ishga tushirish: yield",
        "O'z shaxsiy metod yarating va unga uzatilgan blokni yield yordamida chaqiring.",
        """def takrorla_ikki_marta
  puts "Boshlanish"
  yield
  yield
  puts "Tugash"
end

takrorla_ikki_marta { puts "--> Blok bajarildi!" }
""",
        "'yield' kalit so'zi metodga uzatilgan kod blokini chaqiradi va uning bajarilishini kutadi.",
        """Boshlanish
--> Blok bajarildi!
--> Blok bajarildi!
Tugash"""
    ),
    (
        204,
        "yield ga argumentlar uzatish",
        "Metod ichidan blok parametriga ma'lumot uzating.",
        """def foydalanuvchi_salomi
  yield("Alisher", "Navoiy")
end

foydalanuvchi_salomi do |ism, familiya|
  puts "Assalomu alaykum, #{ism} #{familiya}!"
end
""",
        "'yield(arg1, arg2)' metod ichidagi qiymatlarni blokning `|p1, p2|` parametrlariga yetkazib beradi.",
        """Assalomu alaykum, Alisher Navoiy!"""
    ),
    (
        205,
        "yield dan qaytgan qiymatni qabul qilish",
        "Blok hisoblagan natijani metod ichida qabul qilib, unga soliq qo'shing.",
        """def soliq_qoshish
  asosiy_summa = yield
  soliq = asosiy_summa * 0.12
  asosiy_summa + soliq
end

yakuniy = soliq_qoshish { 50000 }
puts "Soliq bilan birga: #{yakuniy} so'm"
""",
        "Blokdagi eng oxirgi ifodaning qiymati 'yield' chaqiruvining qaytaradigan natijasi bo'ladi.",
        """Soliq bilan birga: 56000.0 so'm"""
    ),
    (
        206,
        "Blok berilganligini tekshirish: block_given?",
        "Metod blok bilan ham, bloksiz ham chaqirilganda xato bermasligini ta'minlang.",
        """def hisobot_chiqar
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
""",
        "Agar metod ichida blok berilmagan bo'lsa va 'yield' chaqirilsa, Ruby 'LocalJumpError: no block given (yield)' xatosini tashlaydi. 'block_given?' orqali blok mavjudligini xavfsiz tekshirish mumkin.",
        """--- HISOBOT ---
Standart ma'lumot: Barcha tizimlar normal ishlamoqda.
--- YAKUN ---
--- HISOBOT ---
Maxsus ma'lumot: Server yuklamasi 85%
--- YAKUN ---"""
    ),
    (
        207,
        "Blok berilmaganda Enumerator qaytarish",
        "Bloksiz chaqirilganda to_enum orqali zanjirli metodlarni qo'llab-quvvatlang.",
        """def mening_raqamlarim
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
""",
        "Ruby standart kutubxonasidagi deyarli barcha metodlar (each, map) blok berilmaganda Enumerator qaytaradi. Bu `return to_enum(:metod)` orqali amalga oshiriladi.",
        """10 20 30 \nEnumerator orqali map: [20, 40, 60]"""
    ),
    (
        208,
        "Blok ichidagi maxsus lokal o'zgaruvchilar: ; ajratuvchisi",
        "Tashqi o'zgaruvchi blok ichida tasodifan o'zgarib ketmasligi uchun uni blok lokali sifatida ajrating.",
        """x = "Tashqi qiymat"

[1, 2].each do |son; x|
  x = "Ichki qiymat #{son}"
  puts "Blok ichida: #{x}"
end

puts "Blokdan tashqarida x: #{x}"
""",
        "Blok parametrlaridan so'ng nuqtali vergul (;) qo'yilib ro'yxat kiritilsa, bu o'zgaruvchilar blokning shaxsiy lokaliga aylanadi va tashqaridagi bir xil nomli o'zgaruvchiga ta'sir qilmaydi.",
        """Blok ichida: Ichki qiymat 1
Blok ichida: Ichki qiymat 2
Blokdan tashqarida x: Tashqi qiymat"""
    ),
    (
        209,
        "Closure tushunchasi: Tashqi leksik muhitni eslab qolish",
        "Blok o'zi yaratilgan joydagi o'zgaruvchilarni qanday 'yopib' (close over) saqlab qolishini ko'rsating.",
        """def hisoblagich_yarat
  son = 0
  Proc.new { son += 1 }
end

hisob1 = hisoblagich_yarat
puts "Birinchi chaqiruv: #{hisob1.call}"
puts "Ikkinchi chaqiruv: #{hisob1.call}"
puts "Uchinchi chaqiruv: #{hisob1.call}"
""",
        "Blok va Proclar haqiqiy Closure (yopilish) hisoblanadi. Ular o'zgaruvchi qiymatini emas, o'zgaruvchining o'zini (reference) eslab qoladi va metod tugagandan keyin ham xotirada yashashda davom etadi.",
        """Birinchi chaqiruv: 1
Ikkinchi chaqiruv: 2
Uchinchi chaqiruv: 3"""
    ),
    (
        210,
        "Proc obyekti yaratish: Proc.new",
        "Blokni qayta ishlatiladigan birinchi darajali (first-class) obyektga aylantiring.",
        """salom_proc = Proc.new do |ism|
  puts "Salom, #{ism}!"
end

puts "Sinfi: #{salom_proc.class}"
salom_proc.call("Jasur")
salom_proc.call("Madina")
""",
        "Ruby-da bloklar mustaqil obyekt emas, biroq `Proc.new` ularni to'laqonli `Proc` sinfi obyektiga aylantiradi va o'zgaruvchilarda saqlashga imkon beradi.",
        """Sinfi: Proc
Salom, Jasur!
Salom, Madina!"""
    ),
    (
        211,
        "Proc ni chaqirish usullari: call, [], === va .()",
        "Proc obyektini ishga tushirishning barcha sintaktik shakllarini qo'llang.",
        """kvadrat = Proc.new { |x| x * x }

puts "call orqali: #{kvadrat.call(5)}"
puts "[] orqali: #{kvadrat[5]}"
puts ".() orqali: #{kvadrat.(5)}"
puts "=== orqali: #{kvadrat === 5}"
""",
        "Ruby-da Proc bir nechta usulda ishga tushiriladi: eng keng tarqalgoni `.call(args)`, qisqartmasi `[args]`, shuningdek `===` operatori (bu Proc-ni `case ... when` ichida ishlatishga imkon beradi).",
        """call orqali: 25
[] orqali: 25
.() orqali: 25
=== orqali: 25"""
    ),
    (
        212,
        "lambda yaratish: lambda va stumpy lambda ->()",
        "Klassik va zamonaviy stumpy lambda sintaksislarini taqqoslang.",
        """l1 = lambda { |a, b| a + b }
l2 = ->(a, b) { a * b } # Stumpy lambda

puts "l1 yig'indi: #{l1.call(3, 4)}"
puts "l2 ko'paytma: #{l2.call(3, 4)}"
puts "l2 lambda ekanligi: #{l2.lambda?}"
""",
        "Ruby 1.9 da kiritilgan `->(param) { ... }` (stumpy lambda) sintaksisi lambdalarni qisqa va qulay yozish usulidir. Lambda ham `Proc` sinfiga tegishli, ammo maxsus bayroqqa (`lambda? == true`) ega.",
        """l1 yig'indi: 7
l2 ko'paytma: 12
l2 lambda ekanligi: true"""
    ),
    (
        213,
        "Proc va Lambda 1-farqi: Argumentlar qat'iyligi (Arity)",
        "Proc va Lambda noto'g'ri sondagi argumentlar uzatilganda o'zini qanday tutishini ko'rsating.",
        """oddiy_proc = Proc.new { |a, b| "a: #{a.inspect}, b: #{b.inspect}" }
oddiy_lambda = ->(a, b) { "a: #{a}, b: #{b}" }

# Proc ortiqcha argumentni tashlab yuboradi, yetmaganiga nil beradi
puts "Proc (1 ta arg): #{oddiy_proc.call(10)}"

# Lambda aniq argumentlar sonini talab qiladi (ArgumentError)
begin
  oddiy_lambda.call(10)
rescue ArgumentError => e
  puts "Lambda xatosi: #{e.class}"
end
""",
        "Proc argumentlar soniga juda erkin (lenient) qaraydi: yetishmaganiga nil qo'yadi. Lambda esa oddiy metodlar kabi qat'iy (strict) tekshiradi va nomuvofiqlikda `ArgumentError` beradi.",
        """Proc (1 ta arg): a: 10, b: nil
Lambda xatosi: ArgumentError"""
    ),
    (
        214,
        "Proc va Lambda 2-farqi: return kalit so'zi",
        "Proc va Lambda ichida 'return' ishlatilganda ko'rinish sohasidan chiqib ketish farqini ko'rsating.",
        """def test_proc
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
""",
        "Proc ichidagi 'return' uni o'rab turgan tashqi butun metoddan chiqib ketadi. Lambda ichidagi 'return' esa faqat lambdaning o'zidan qiymat qaytaradi va tashqi metod o'z ishini davom ettiradi.",
        """test_proc natijasi: Proc-dan chiqish
test_lambda natijasi: Metod oxiri (lambda qaytardi: Lambda-dan chiqish)"""
    ),
    (
        215,
        "Metod argumentida blokni Proc ga aylantirish: &blok",
        "Metodga kelgan blokni nomli Proc o'zgaruvchisiga oling.",
        """def amaliyot_bajar(nom, &harakat)
  puts "Boshlanmoqda: #{nom}"
  puts "Harakat sinfi: #{harakat.class}"
  harakat.call
  puts "Tugallandi."
end

amaliyot_bajar("Fayllarni tozalash") do
  puts "--> 15 ta kesh fayl o'chirildi."
end
""",
        "Metod parametrlarining eng oxirida `&o'zgaruvchi` yozilsa, unga uzatilgan blok avtomatik `Proc` obyektiga o'giriladi va metod ichida saqlash yoki boshqa joyga uzatish mumkin bo'ladi.",
        """Boshlanmoqda: Fayllarni tozalash
Harakat sinfi: Proc
--> 15 ta kesh fayl o'chirildi.
Tugallandi."""
    ),
    (
        216,
        "Proc ni metodga blok sifatida uzatish: &proc",
        "Mavjud Proc obyektini metodga oddiy blok sifatida yuboring.",
        """kvadrat_proc = Proc.new { |n| n ** 2 }
natijalar = [1, 2, 3, 4].map(&kvadrat_proc)

puts "Kvadratlar: #{natijalar.inspect}"
""",
        "Metod chaqiruvida argument oldiga `&` qo'yilsa, Ruby o'sha obyektning `to_proc` metodini chaqirib, uni oddiy blok shaklida metodga uzatadi.",
        """Kvadratlar: [1, 4, 9, 16]"""
    ),
    (
        217,
        "Symbol-to-Proc sehri: &:metod",
        "Massivdagi barcha satrlarni &:upcase orqali bosh harfga aylantiring.",
        """shaharlar = ["toshkent", "samarqand", "buxoro"]
bosh_harfli = shaharlar.map(&:upcase)

puts "Bosh harfli: #{bosh_harfli.inspect}"
""",
        "`shaharlar.map(&:upcase)` aslida `shaharlar.map { |sh| sh.upcase }` ning qisqartmasidir. Symbol sinfida `to_proc` metodi aniqlangan bo'lib, u kelgan birinchi argument ustida ushbu nomli metodni chaqiruvchi Proc qaytaradi.",
        """Bosh harfli: ["TOSHKENT", "SAMARQAND", "BUXORO"]"""
    ),
    (
        218,
        "O'z sinfida to_proc metodini aniqlash",
        "O'z maxsus sinfingizni & operatori bilan ishlashga moslashtiring.",
        """class Kopaytiruvchi
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
""",
        "Har qanday sinfda `to_proc` metodini yaratib, uning obyektlarini `&` operatori orqali to'g'ridan-to'g'ri blok talab qiladigan metodlarga uzatish mumkin.",
        """Ikki karra: [20, 40, 60]"""
    ),
    (
        219,
        "Hash uchun to_proc (Ruby 2.3+)",
        "Hash obyektini & orqali to'g'ridan-to'g'ri map metodiga uzating.",
        """lugat = { uz: "O'zbekiston", en: "Angliya", ru: "Rossiya" }
kalitlar = [:uz, :en]

nomlar = kalitlar.map(&lugat)
puts "Topilgan nomlar: #{nomlar.inspect}"
""",
        "Ruby 2.3 dan boshlab Hash sinfi ham `to_proc` ga ega. `&hash` chaqiruvi `Proc.new { |k| hash[k] }` ga teng bo'lib, kalitlar bo'yicha tezkor xaritaga aylantiradi.",
        """Topilgan nomlar: ["O'zbekiston", "Angliya"]"""
    ),
    (
        220,
        "Metodni Proc ga aylantirish: method(:nomi).to_proc",
        "Mavjud oddiy metodni Proc ga o'girib, boshqa funksiyalarga uzating.",
        """def kub(x)
  x ** 3
end

kub_proc = method(:kub).to_proc
puts "Kublar: #{[1, 2, 3].map(&kub_proc).inspect}"
""",
        "`method(:nomi)` orqali har qanday mavjud metod 'Method' obyektiga olinadi va `to_proc` yordamida erkin uzatiladi.",
        """Kublar: [1, 8, 27]"""
    ),
    (
        221,
        "Proc karrilash: curry metodi",
        "Uchta argument qabul qiluvchi funksiyani bosqichma-bosqich qisman qo'llang.",
        """qoshuvchi = ->(a, b, c) { a + b + c }
karri = qoshuvchi.curry

qosh_10 = karri.call(10)
qosh_10_va_20 = qosh_10.call(20)
yakuniy = qosh_10_va_20.call(5)

puts "Yakuniy yig'indi: #{yakuniy}"
""",
        "'curry' ko'p argumentli funksiyani bittalab argument oluvchi zanjirli funksiyalarga ajratadi (Currying).",
        """Yakuniy yig'indi: 35"""
    ),
    (
        222,
        "Lambda karrilash bilan soliq hisoblash",
        "Turli davlatlar uchun soliq hisoblovchi ixtisoslashgan funksiyalarni curry orqali yarating.",
        """soliq_hisoblagich = ->(stavka, summa) { summa + (summa * stavka) }.curry

uz_soliq = soliq_hisoblagich.call(0.12)
aqsh_soliq = soliq_hisoblagich.call(0.08)

puts "O'zbekistonda 100 000 so'm: #{uz_soliq.call(100_000).to_i}"
puts "AQShda $100: #{aqsh_soliq.call(100).to_i}"
""",
        "Currying yordamida umumiy matematik modellardan aniq ixtisoslashgan hisoblagichlarni oson hosil qilish mumkin.",
        """O'zbekistonda 100 000 so'm: 112000
AQShda $100: 108"""
    ),
    (
        223,
        "Proc arity: argumentlar sonini aniqlash",
        "Funksiya nechta parametr kutayotganini dasturiy ravishda aniqlang.",
        """p1 = ->(x) { x }
p2 = ->(a, b) { a + b }
p3 = ->(a, *rest) { a }

puts "p1 arity: #{p1.arity}"
puts "p2 arity: #{p2.arity}"
puts "p3 arity: #{p3.arity}"
""",
        "'arity' qat'iy argumentlar sonini qaytaradi. Ixtiyoriy yoki splat argumentlar bo'lsa manfiy son qaytadi.",
        """p1 arity: 1
p2 arity: 2
p3 arity: -2"""
    ),
    (
        224,
        "Funksiyalar kompozitsiyasi (Ruby 2.6+): >> va <<",
        "Ikkita mustaqil funksiyani birlashtirib yangi funksiya quvuri (Pipeline) hosil qiling.",
        """ikki_karra = ->(x) { x * 2 }
bir_qosh = ->(x) { x + 1 }

# >> chapdan o'ngga: avval ikki_karra, keyin bir_qosh
quvur1 = ikki_karra >> bir_qosh

# << o'ngdan chapga: avval bir_qosh, keyin ikki_karra
quvur2 = ikki_karra << bir_qosh

puts "(5 * 2) + 1: #{quvur1.call(5)}"
puts "(5 + 1) * 2: #{quvur2.call(5)}"
""",
        "Ruby 2.6 da kiritilgan `>>` va `<<` operatorlari matematik funksiyalar kompozitsiyasini amalga oshiradi: `f >> g` bu `g(f(x))` demakdir.",
        """(5 * 2) + 1: 11
(5 + 1) * 2: 12"""
    ),
    (
        225,
        "Bloklar yordamida Benchmark (kod ishlash vaqtini o'lchash)",
        "Har qanday kod blokining bajarilish davomiyligini o'lchovchi wrapper yozing.",
        """def vaqtni_olcha(amal_nomi)
  boshlanish = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  yield
  tugash = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  farq = tugash - boshlanish
  puts "#{amal_nomi} bajarildi: #{farq.round(4)} soniya"
end

vaqtni_olcha("Katta massiv yig'indisi") do
  (1..100_000).sum
end
""",
        "Around-pattern vositasida blokdan oldin va keyin zarur ko'rsatmalarni (benchmark, tranzaksiya, xavfsizlik) bajarish mumkin.",
        """Katta massiv yig'indisi bajarildi: 0.003 soniya"""
    ),
    (
        226,
        "Bloklar bilan resurslarni avtomatik yopish (Around pattern)",
        "Fayl yoki ulanish ochiq qolib ketmasligini kafolatlovchi xavfsiz blok yarating.",
        """class SoxtaBazaUlanishi
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
""",
        "Blok va 'ensure' kombinatsiyasi dasturda xatolik yuz berganda ham resurslar (xotira, fayl deskriptorlari, soketlar) 100% yopilishini ta'minlaydi.",
        """Baza ulandi.
SQL so'rov bajarildi.
Baza ulanishi xavfsiz yopildi."""
    ),
    (
        227,
        "Blok orqali obyekt konfiguratsiyasi (Config Block)",
        "Gem va kutubxonalarda qo'llaniladigan `configure do |config|` arxitekturasini yarating.",
        """class TizimKonfiguratsiyasi
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
""",
        "Config Block namunasi Ruby on Rails konfiguratsiyalarida (masalan `config/environments/production.rb`) eng mashhur arxitektura hisoblanadi.",
        """Server: https://khorazmiy.uz:443, timeout: 60s"""
    ),
    (
        228,
        "O'z shaxsiy each metodini yaratish",
        "Massiv nusxasini ishlatmasdan o'z maxsus konteyner sinfingizda blokli iteratsiya quring.",
        """class JuftSonlar
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
""",
        "Har qanday sinfda `def each` yozib, ichida `yield` chaqirilsa, sinf to'liq bloklarni qabul qiladigan konteynerga aylanadi.",
        """2 4 6"""
    ),
    (
        229,
        "O'z shaxsiy map metodini yozish",
        "Array#map qanday ishlashini noldan o'z funksiyangiz bilan takrorlang.",
        """def mening_mapim(massiv)
  natija = []
  massiv.each do |element|
    natija << yield(element)
  end
  natija
end

kvadratlar = mening_mapim([1, 2, 3]) { |x| x * x }
puts "Kvadratlar: #{kvadratlar.inspect}"
""",
        "map har bir elementni blok orqali o'tkazib, yangi massivga yig'adi.",
        """Kvadratlar: [1, 4, 9]"""
    ),
    (
        230,
        "O'z shaxsiy select metodini yozish",
        "Filtrlovchi select metodini yield yordamida noldan yasang.",
        """def mening_selectim(massiv)
  saralangan = []
  massiv.each do |item|
    saralangan << item if yield(item)
  end
  saralangan
end

juftlar = mening_selectim([1, 2, 3, 4, 5, 6]) { |x| x.even? }
puts "Juftlar: #{juftlar.inspect}"
""",
        "select metodi blok qachon true qaytarsa o'sha elementni qoldiradi.",
        """Juftlar: [2, 4, 6]"""
    ),
    (
        231,
        "O'z shaxsiy reduce / inject metodini yozish",
        "To'plamni yagona yakuniy qiymatga yig'uvchi (accumulator) mantiqni yarating.",
        """def mening_reducem(massiv, boshlangich)
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
""",
        "reduce har bir qadamda o'tgan qadam natijasini joriy element bilan yangilaydi.",
        """Yig'indi: 10
Ko'paytma: 24"""
    ),
    (
        232,
        "Blok ichida next bilan qiymat qaytarish",
        "Iteratsiya paytida shart bajarilmasa 'next qiymat' orqali muqobil javob bering.",
        """natijalar = [1, 2, 3, 4, 5].map do |son|
  next "Toq" if son.odd?
  son * 10
end

puts "Natijalar: #{natijalar.inspect}"
""",
        "'map' kabi metodlarda 'next qiymat' yozilsa, ushbu iteratsiya uchun berilgan qiymat saqlanadi va keyingi elementga o'tiladi.",
        """Natijalar: ["Toq", 20, "Toq", 40, "Toq"]"""
    ),
    (
        233,
        "Blok ichida break ning harakati",
        "Blok ichida chaqirilgan break butun metodni to'xtatishini ko'rsating.",
        """def sanagich
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
""",
        "Blok ichidagi 'break' nafaqat blokni, balki ushbu blokni chaqirgan butun tashqi metodni darhol to'xtatadi va 'break' ga berilgan qiymatni qaytaradi.",
        """Qabul qilindi: 1
Qabul qilindi: 2
Natija: Blokdan to'xtatildi!"""
    ),
    (
        234,
        "Hodisalarni tinglovchi (Event Listener) tizimi Procs bilan",
        "Hodisalar yuz berganda ro'yxatdan o'tgan barcha Proc larni chaqiruvchi Event Bus tuzing.",
        """class HodisalarMarkazi
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
""",
        "Observer va Event Listener patternlari Ruby-da Proclar orqali juda yengil va modulli tarzda quriladi.",
        """SMS yuborildi: 150000 so'm yechildi.
Telegram botga xabar ketdi: Foydalanuvchi Alisher"""
    ),
    (
        235,
        "Filtrlar zanjiri (Middleware Pipeline) bloklar yordamida",
        "So'rovni ketma-ket bir nechta filtrlar orqali o'tkazuvchi zanjir yarating.",
        """autentifikatsiya = ->(req) { req[:user] ? req.merge(auth: true) : req }
tozalash = ->(req) { req.merge(matn: req[:matn].strip.downcase) }

sorov = { user: "admin", matn: "   Salom Dunyo!   " }
zanjir = autentifikatsiya >> tozalash
yakuniy = zanjir.call(sorov)

puts "Qayta ishlangan so'rov: #{yakuniy.inspect}"
""",
        "Funksional kompozitsiya yordamida HTTP middleware (masalan Rack) modullarini bir-biriga ulash juda sodda kechadi.",
        """Qayta ishlangan so'rov: {:user=>"admin", :matn=>"salom dunyo!", :auth=>true}"""
    ),
    (
        236,
        "Xotirani tejovchi generatorlar (Fibonacci Stream)",
        "Cheksiz Fibonachchi ketma-ketligini faqat so'ralganda hisoblovchi blokli generator yozing.",
        """def cheksiz_fibonachchi
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
""",
        "Generatorlar xotirada millionlab sonlarni birdan saqlamasdan, har safar faqat bitta qiymatni hisoblab blok orqali uzatadi (Lazy evaluation).",
        """Dastlabki 7 ta Fibonachchi: [0, 1, 1, 2, 3, 5, 8]"""
    ),
    (
        237,
        "Dinamik predikatlar generatori",
        "Berilgan songa bo'linishni tekshiruvchi maxsus lambda ishlab chiqaruvchi funksiya yozing.",
        """def bolinish_tekshirgich(boluvchi)
  ->(son) { son % boluvchi == 0 }
end

uchga_bolinadimi = bolinish_tekshirgich(3)
beshga_bolinadimi = bolinish_tekshirgich(5)

puts "15 uchga bo'linadimi? #{uchga_bolinadimi.call(15)}"
puts "16 uchga bo'linadimi? #{uchga_bolinadimi.call(16)}"
puts "20 beshga bo'linadimi? #{beshga_bolinadimi.call(20)}"
""",
        "Yuqori tartibli funksiyalar (Higher-order functions) yangi maxsus predikat funksiyalar ishlab chiqarish imkonini beradi.",
        """15 uchga bo'linadimi? true
16 uchga bo'linadimi? false
20 beshga bo'linadimi? true"""
    ),
    (
        238,
        "Blok yordamida HTML teglarini o'rab chiquvchi helper",
        "Veb shablonlarida HTML teglarini chiroyli ichma-ich generatsiya qiling.",
        """def teg(nom)
  "<#{nom}>" + yield + "</#{nom}>"
end

html = teg("div") do
  teg("p") do
    teg("strong") { "Muhim bildirishnoma!" }
  end
end

puts html
""",
        "Bloklar orqali deklarativ DSL shablonlari (masalan Markaby, HTML builderlar) yaratiladi.",
        """<div><p><strong>Muhim bildirishnoma!</strong></p></div>"""
    ),
    (
        239,
        "Binding obyekti va kontekstni ko'chirish",
        "Metod ichidagi o'zgaruvchilar muhitini binding orqali ushlab, tashqarida eval qiling.",
        """def sirli_xona
  parol = "Khorazmiy_2026"
  binding
end

muhit = sirli_xona
puts "Muhit sinfi: #{muhit.class}"
puts "Tashqaridan o'qilgan parol: #{eval('parol', muhit)}"
""",
        "'binding' obyekti joriy ko'rinish sohasidagi barcha o'zgaruvchilar, metodlar va 'self' kontekstini o'zida muhrlab oladi.",
        """Muhit sinfi: Binding
Tashqaridan o'qilgan parol: Khorazmiy_2026"""
    ),
    (
        240,
        "Tranzaksiya bloklari va xatoda orqaga qaytish (Rollback)",
        "Bank hisoblaridagi o'zgarishlar xatolik yuz berganda avtomatik bekor qilinishini ta'minlang.",
        """def tranzaksiya(hisob)
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
""",
        "Tranzaksiya bloklari ma'lumotlar yaxlitligini xavf ostiga qo'ymasdan xavfsiz boshqarish imkonini beradi.",
        """Tranzaksiya boshlandi: {:Ali=>100, :Vali=>50}
XATOLIK! O'zgarishlar bekor qilindi (Rollback): Tarmoq uzildi!
Yakuniy hisob: {:Ali=>100, :Vali=>50}"""
    ),
    (
        241,
        "Lambda massivlari va ketma-ketlikda ishga tushirish",
        "Bir nechta validatsiya qoidalarini massivga yig'ib, tartib bilan tekshiring.",
        """qoidalar = [
  ->(matn) { matn.length >= 6 ? true : "Parol kamida 6 belgidan iborat bo'lishi kerak" },
  ->(matn) { matn =~ /\\d/ ? true : "Parolda kamida bitta raqam bo'lishi kerak" }
]

parol = "sir"
xatolar = []

qoidalar.each do |qoida|
  natija = qoida.call(parol)
  xatolar << natija if natija != true
end

puts "Aniqlangan xatolar: #{xatolar.inspect}"
""",
        "Lambdalardan iborat massivlar qoidalar dvigateli (Rule engine) va validatsiya tizimlarini modulli qilish imkonini beradi.",
        """Aniqlangan xatolar: ["Parol kamida 6 belgidan iborat bo'lishi kerak", "Parolda kamida bitta raqam bo'lishi kerak"]"""
    ),
    (
        242,
        "Proc#to_s va tekshiruv (Inspection)",
        "Proc qaysi faylda va nechanchi qatorda yaratilganini ko'ring.",
        """p = Proc.new { "Test" }
puts "Proc inspection: #{p.inspect.include?('Proc')}"
puts "Source location mavjudmi: #{!p.source_location.nil?}"
""",
        "'source_location' metodi `[fayl_yo'li, qator_raqami]` massivini qaytaradi. Bu yirik freymvorklarda debug qilishda nihoyatda qimmatli ma'lumotdir.",
        """Proc inspection: true
Source location mavjudmi: true"""
    ),
    (
        243,
        "Blok bilan takroriy urinish (Retry with backoff) mexanizmi",
        "Muvaffaqiyatsiz bo'lgan tarmoq so'rovini belgilangan martagacha qayta urinuvchi blokli metod yozing.",
        """def qayta_urin(maksimal = 3)
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
""",
        "Blok ichidagi xatoliklarni 'retry' orqali qayta urinish tarmoq uzilishlari va vaqtinchalik xatolarni yengishda standart usuldir.",
        """So'rov yuborilmoqda (1)...
Xatolik: Server 503 javob berdi. 1-urinish muvaffaqiyatsiz. Qayta urinilmoqda...
So'rov yuborilmoqda (2)...
Xatolik: Server 503 javob berdi. 2-urinish muvaffaqiyatsiz. Qayta urinilmoqda...
So'rov yuborilmoqda (3)...
Muvaffaqiyatli ulandi!"""
    ),
    (
        244,
        "Blok orqali obyekt nusxasini xavfsiz boshqarish (tap metodi)",
        "Obyekt ustida amallarni bajarib, zanjirli o'zgaruvchisiz obyektning o'zini qaytaruvchi tap metodidan foydalaning.",
        """foydalanuvchi = { ism: "Sardor" }.tap do |u|
  u[:rol] = "developer"
  u[:shahar] = "Toshkent"
  puts "Obyekt sozlandi: #{u.inspect}"
end

puts "Yakuniy foydalanuvchi: #{foydalanuvchi.inspect}"
""",
        "Kernel#tap metodi obyektni o'z blokiga uzatadi va blok yakunida har doim obyektning o'zini qaytaradi. Bu oraliq o'zgaruvchilarsiz zanjirli kod yozish imkonini beradi.",
        """Obyekt sozlandi: {:ism=>"Sardor", :rol=>"developer", :shahar=>"Toshkent"}
Yakuniy foydalanuvchi: {:ism=>"Sardor", :rol=>"developer", :shahar=>"Toshkent"}"""
    ),
    (
        245,
        "then / yield_self (Ruby 2.6+)",
        "Qiymatni blok orqali boshqa qiymatga aylantiruvchi zamonaviy 'then' metodini qo'llang.",
        """natija = "  khorazmiy ai  "
  .strip
  .upcase
  .then { |matn| "[RASMIY: #{matn}]" }

puts natija
""",
        "'then' (sinonimi 'yield_self') qiymatni blok parametriga beradi va blok natijasini keyingi metodga uzatadi. Bu Elixir yoki OCaml-dagi quvur (pipe) operatoriga o'xshaydi.",
        """[RASMIY: KHORAZMIY AI]"""
    ),
    (
        246,
        "Blok parametrlari destrukturizatsiyasi",
        "Juftliklar massividan kalit va qiymatni alohida parametrlar sifatida qabul qiling.",
        """juftliklar = [[:olma, 10], [:anor, 20]]

juftliklar.each do |(meva, narx)|
  puts "Meva: #{meva}, Narx: #{narx}"
end
""",
        "Blok parametrlarida `|(a, b)|` qavslar qo'yilishi ichki massiv elementlarini avtomatik alohida o'zgaruvchilarga ajratadi.",
        """Meva: olma, Narx: 10
Meva: anor, Narx: 20"""
    ),
    (
        247,
        "Proc obyektlarining tengligi",
        "Ikkita Proc obyekti teng yoki teng emasligini solishtiring.",
        """p1 = Proc.new { "salom" }
p2 = Proc.new { "salom" }
p3 = p1

puts "p1 == p2: #{p1 == p2}"
puts "p1 == p3: #{p1 == p3}"
""",
        "Proclar hatto bir xil kodga ega bo'lsa ham har safar yangi obyekt yaratiladi (`p1 != p2`). Faqat bitta manzilga ishora qilingandagina teng bo'ladi.",
        """p1 == p2: false
p1 == p3: true"""
    ),
    (
        248,
        "Bloklar bilan memoization (Keshlashtirish) dekoratori",
        "Og'ir hisob-kitoblarni faqat bir marta bajarib natijani eslab qoluvchi blokli tizim yarating.",
        """def kesh(kalit, xotira = {})
  xotira[kalit] ||= yield
end

kesh_xotirasi = {}

r1 = kesh(:faktorial_5, kesh_xotirasi) { (1..5).inject(:*) }
r2 = kesh(:faktorial_5, kesh_xotirasi) { puts "Qayta hisoblanmasligi kerak!"; 999 }

puts "Natija 1: #{r1}"
puts "Natija 2 (keshdan): #{r2}"
""",
        "Bloklar va `||=` operatori orqali natijani keshlashtirish yuqori unumdor tizimlarning asosi hisoblanadi.",
        """Natija 1: 120
Natija 2 (keshdan): 120"""
    ),
    (
        249,
        "Lambda ichida rejim tanlash: Method Dispatching",
        "Amal turiga qarab tegishli lambdani tanlab ishlatuvchi kalkulyator tuzing.",
        """amallar = {
  qoshish: ->(a, b) { a + b },
  ayirish: ->(a, b) { a - b },
  kopaytirish: ->(a, b) { a * b }
}

def hisobla(amallar, turi, a, b)
  amallar[turi].call(a, b)
end

puts "10 + 5 = #{hisobla(amallar, :qoshish, 10, 5)}"
puts "10 * 5 = #{hisobla(amallar, :kopaytirish, 10, 5)}"
""",
        "Hash ichida lambdalarni saqlash katta if-else bloklaridan xalos qiladi va dasturni kengaytirishni osonlashtiradi.",
        """10 + 5 = 15
10 * 5 = 50"""
    ),
    (
        250,
        "Amaliy loyiha: Funksional ETL (Extract, Transform, Load) ma'lumotlar quvuri",
        "Foydalanuvchilar ma'lumotlarini qabul qilib, ularni tozalovchi, formatlovchi va hisobot shakliga keltiruvchi to'liq funksional quvur yarating.",
        """xom_malumotlar = [
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
""",
        "Ushbu amaliy loyihada Ruby bloklari, lambdalar, Proc konvertatsiyalari (&operator), massivlar, satr tozalash va funksional kompozitsiya to'liq birlashtirildi.",
        """==========================================================
KOMPANIYA 25+ YOSHLI XODIMLARINING TOZALANGAN HISOBOTI
==========================================================
Xodim: Anvar Aliyev       | Yoshi: 28 | Shahar: Toshkent
Xodim: Jasur Karimov      | Yoshi: 31 | Shahar: Buxoro
=========================================================="""
    )
]

register_topic("gen_05_bloklar.py", "ruby_05_bloklar_procs_va_lambdalar.md", 201, TASKS_05)
