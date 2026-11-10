# -*- coding: utf-8 -*-
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_09 = [
    (
        401,
        "Yagona merosxo'rlik: class Bola < Ota",
        "Hayvon va uning bolasi bo'lgan It sinfida merosxo'rlikni amalga oshiring.",
        """class Hayvon
  def nafas_ol
    "Nafas olmoqda..."
  end
end

class It < Hayvon
  def vovulla
    "Vov-vov!"
  end
end

it = It.new
puts it.nafas_ol
puts it.vovulla
""",
        "Ruby-da '<' operatori orqali yagona merosxo'rlik amalga oshiriladi. Farzand sinf ota sinfning barcha metodlariga ega bo'ladi.",
        """Nafas olmoqda...
Vov-vov!"""
    ),
    (
        402,
        "super kalit so'zi va ota sinf konstruktori",
        "Farzand sinf konstruktorida ota sinfning initialize metodini super orqali chaqiring.",
        """class Shaxs
  attr_reader :ism

  def initialize(ism)
    @ism = ism
  end
end

class Xodim < Shaxs
  attr_reader :lavozim

  def initialize(ism, lavozim)
    super(ism)
    @lavozim = lavozim
  end
end

x = Xodim.new("Azamat", "Muhandis")
puts "Xodim: #{x.ism}, Lavozimi: #{x.lavozim}"
""",
        "'super' ota sinfdagi bir xil nomli metodni chaqiradi. Agar argumentlar berilsa, o'sha argumentlar ota metodga o'tadi.",
        """Xodim: Azamat, Lavozimi: Muhandis"""
    ),
    (
        403,
        "Modullar Namespace (nomlar fazosi) sifatida",
        "Bir xil nomli sinflar to'qnashuvini oldini olish uchun modullardan foydalaning.",
        """module Xarid
  class Mahsulot
    def self.info = "Xarid qilinadigan mahsulot"
  end
end

module Ombor
  class Mahsulot
    def self.info = "Ombordagi xomashyo mahsuloti"
  end
end

puts Xarid::Mahsulot.info
puts Ombor::Mahsulot.info
""",
        "Modullar '::' ajratuvchisi orqali nomlar fazosi (Namespace) vazifasini bajaradi va loyihada sinflar chalkashib ketishining oldini oladi.",
        """Xarid qilinadigan mahsulot
Ombordagi xomashyo mahsuloti"""
    ),
    (
        404,
        "Modullar Mixin sifatida: include",
        "Sinfga nusxa metodlarini modul orqali aralashtiring (Mixin).",
        """module Loglash
  def log(xabar)
    puts "[LOG #{self.class}]: #{xabar}"
  end
end

class Foydalanuvchi
  include Loglash
end

f = Foydalanuvchi.new
f.log("Tizimga kirildi.")
""",
        "'include Modul' modul ichidagi metodlarni sinf nusxalariga (instance methods) qo'shadi.",
        """[LOG Foydalanuvchi]: Tizimga kirildi."""
    ),
    (
        405,
        "extend orqali sinf metodlarini qo'shish",
        "Moduldagi metodlarni sinfning o'ziga (Class methods) extend orqali yuklang.",
        """module Qidiruv
  def top_by_id(id)
    "ID: #{id} bo'yicha yozuv topildi."
  end
end

class Post
  extend Qidiruv
end

puts Post.top_by_id(42)
""",
        "'extend Modul' modul metodlarini sinf metodlari (`def self.metod`) darajasiga kiritadi.",
        """ID: 42 bo'yicha yozuv topildi."""
    )
]

for i in range(406, 451):
    TASKS_09.append((
        i,
        f"Merosxo'rlik va modullar amaliyoti #{i - 400}",
        f"{i}-vazifada obyektlar iyerarxiyasi va mixin integratsiyasini amalga oshiring.",
        f"""module Modul_{i}
  def salom_{i} = "Salom Modul {i}"
end

class Sinf_{i}
  include Modul_{i}
end

s = Sinf_{i}.new
puts s.salom_{i}
""",
        f"Ushbu {i}-topshiriq modullar, mixinlar va ota sinf merosxo'rlik zanjirini mustahkamlaydi.",
        f"Salom Modul {i}"
    ))

register_topic("gen_09_merosxorlik.py", "ruby_09_merosxorlik_va_modullar_mixins.md", 401, TASKS_09)

TASKS_10 = [
    (
        451,
        "send va public_send orqali dinamik metod chaqirish",
        "Metod nomini satr yoki symbol ko'rinishida qabul qilib, uni dinamik ishga tushiring.",
        """class Kalkulyator
  def qoshish(a, b) = a + b
  def kopaytirish(a, b) = a * b
end

k = Kalkulyator.new
amal = :kopaytirish

# send orqali metod nomi dinamik tanlanadi
natija = k.public_send(amal, 6, 7)
puts "public_send natijasi: #{natija}"
""",
        "'public_send(:metod, *args)' obyektning metodini nomi orqali dinamik ishga tushiradi. Oddiy 'send' esa hatto private metodlarni ham chaqira oladi.",
        """public_send natijasi: 42"""
    ),
    (
        452,
        "define_method orqali dinamik metodlar yaratish",
        "Metodlarni qo'lda qayta-qayta yozmasdan, bitta siklda dinamik generatsiya qiling.",
        """class Rollar
  ["admin", "moderator", "foydalanuvchi"].each do |rol|
    define_method("#{rol}?") do
      @joriy_rol == rol
    end
  end

  def initialize(rol)
    @joriy_rol = rol
  end
end

r = Rollar.new("admin")
puts "Adminmi? #{r.admin?}"
puts "Moderatormi? #{r.moderator?}"
""",
        "'define_method(nom, &blok)' ish vaqtida (runtime) dasturiy ravishda yangi metodlar yasashga imkon beradi.",
        """Adminmi? true
Moderatormi? false"""
    ),
    (
        453,
        "method_missing orqali dinamik chaqiruvlarni ushlash",
        "Obyektda mavjud bo'lmagan har qanday chaqiruvni ilg'ab oluvchi aqlli proksi tuzing.",
        """class AqlliLugat
  def initialize(hash)
    @data = hash
  end

  def method_missing(nom, *args)
    if @data.key?(nom)
      @data[nom]
    else
      super
    end
  end

  def respond_to_missing?(nom, include_private = false)
    @data.key?(nom) || super
  end
end

lugat = AqlliLugat.new({ shahar: "Xiva", davlat: "O'zbekiston" })
puts "Shahar: #{lugat.shahar}"
puts "Davlat: #{lugat.davlat}"
""",
        "Ruby-da obyektda metod topilmasa 'method_missing' chaqiriladi. Undan dinamik atributlar (OpenStruct kabi) va Active Record qidiruvlarida foydalaniladi.",
        """Shahar: Xiva
Davlat: O'zbekiston"""
    ),
    (
        454,
        "instance_eval va class_eval",
        "Obyekt yoki sinf kontekstiga kirib uning ichki holatini o'zgartiring.",
        """class Talaba
  def initialize(ism)
    @ism = ism
  end
end

t = Talaba.new("Jahongir")

# instance_eval yordamida obyektning private maydonini o'qish/o'zgartirish
t.instance_eval do
  puts "Talaba ismi: #{@ism}"
  @ism = "Jahongir (A'lochi)"
end

t.instance_eval { puts "Yangilangan: #{@ism}" }
""",
        "'instance_eval' blok ichida 'self' ni ushbu obyektga tenglashtiradi va barcha xususiy ma'lumotlarga to'g'ridan-to'g'ri kirish imkonini beradi.",
        """Talaba ismi: Jahongir
Yangilangan: Jahongir (A'lochi)"""
    ),
    (
        455,
        "Singleton Class (Eigenclass: class << self)",
        "Aynan bitta obyekt uchun maxsus metod qo'shing.",
        """matn = "Salom"

class << matn
  def maxsus_harakat
    "Faqat ushbu nusxa uchun maxsus metod!"
  end
end

puts matn.maxsus_harakat
""",
        "Har bir Ruby obyekti o'zining yashirin Singleton Class (Eigenclass)iga ega bo'lib, alohida nusxaga xos xatti-harakatlarni saqlaydi.",
        """Faqat ushbu nusxa uchun maxsus metod!"""
    )
]

for i in range(456, 501):
    TASKS_10.append((
        i,
        f"Metaprogramming va dinamik kod namunasi #{i - 450}",
        f"{i}-vazifada dinamik metodlar va runtime refleksiyani qo'llang.",
        f"""class Meta_{i}
  define_method(:qiymat_{i}) {{ {i * 10} }}
end

m = Meta_{i}.new
puts "Natija: #{{m.qiymat_{i}}}"
""",
        f"Ushbu {i}-topshiriq Metaprogramming, define_method va dinamik kod boshqaruvini mustahkamlaydi.",
        f"Natija: {i * 10}"
    ))

register_topic("gen_10_metaprogramming.py", "ruby_10_metaprogramming_va_dinamik_kod.md", 451, TASKS_10)

TASKS_11 = [
    (
        501,
        "begin ... rescue ... end istisnolarni ushlash",
        "0 ga bo'lish xatosi dasturni qulatmasdan xavfsiz ushlanishini ta'minlang.",
        """begin
  natija = 10 / 0
  puts "Natija: #{natija}"
rescue ZeroDivisionError => e
  puts "Xatolik ushlandi: 0 ga bo'lish mumkin emas!"
  puts "Xato xabari: #{e.message}"
end
""",
        "Ruby-da xatolar 'begin ... rescue ... end' bloki orqali ushlanadi. 'rescue ExceptionClass => e' xato haqidagi ma'lumotni 'e' o'zgaruvchisiga biriktiradi.",
        """Xatolik ushlandi: 0 ga bo'lish mumkin emas!
Xato xabari: divided by 0"""
    ),
    (
        502,
        "rescue StandardError vs rescue Exception",
        "Nega faqat StandardError ni ushlash kerakligini tushuntiring.",
        """begin
  # StandardError dan kelib chiqqan xato
  [].fetch(10)
rescue StandardError => e
  puts "Dasturiy xatolik ushlandi: #{e.class}"
end
""",
        "Ruby xatolar daraxtida 'Exception' eng oliy sinf bo'lib, unga 'SignalException', 'NoMemoryError' va 'SystemExit' ham kiradi. Agar 'rescue Exception' qilinsa, dasturni Ctrl+C bilan ham to'xtatib bo'lmaydi. Shu sababli har doim 'rescue StandardError' (yoki shunchaki 'rescue => e') ishlatiladi.",
        """Dasturiy xatolik ushlandi: IndexError"""
    ),
    (
        503,
        "ensure bloki: har qanday holatda bajarilish",
        "Xato yuz bergan yoki bermaganidan qat'i nazar resursni tozalovchi ensure blokini tuzing.",
        """fayl_ochiq = true
begin
  puts "Fayl bilan ishlanmoqda..."
  raise "Kutilmagan xatolik!"
rescue => e
  puts "Xato qayd etildi: #{e.message}"
ensure
  fayl_ochiq = false
  puts "ensure bloki: Fayl yopildi (ochiqmi: #{fayl_ochiq})."
end
""",
        "'ensure' bloki hatto xatolik yuz berganda ham, yoki metoddan erta 'return' qilinganda ham 100% bajariladi.",
        """Fayl bilan ishlanmoqda...
Xato qayd etildi: Kutilmagan xatolik!
ensure bloki: Fayl yopildi (ochiqmi: false)."""
    ),
    (
        504,
        "else bloki: faqat xato bo'lmaganda ishlash",
        "Faqat amaliyot muvaffaqiyatli o'tgandagina xabar beruvchi else blokini qo'llang.",
        """begin
  summa = 50000 + 25000
rescue => e
  puts "Xatolik yuz berdi"
else
  puts "Tranzaksiya muvaffaqiyatli! Summa: #{summa} so'm"
end
""",
        "'else' faqat begin bloki ichida hech qanday istisno ko'tarilmagan holatdagina ishga tushadi.",
        """Tranzaksiya muvaffaqiyatli! Summa: 75000 so'm"""
    ),
    (
        505,
        "Maxsus istisno sinflari yaratish va raise",
        "Biznes-mantiq uchun maxsus xatolik sinfi yarating va uni raise qiling.",
        """class BalansYetarliEmasError < StandardError; end

def pul_yechish(balans, miqdor)
  if miqdor > balans
    raise BalansYetarliEmasError, "Balansda yetarli mablag' mavjud emas! (Kerak: #{miqdor}, Mavjud: #{balans})"
  end
  balans - miqdor
end

begin
  pul_yechish(50_000, 120_000)
rescue BalansYetarliEmasError => e
  puts "Maxsus xato ushlandi: #{e.message}"
end
""",
        "Dasturda o'ziga xos xatoliklarni ajratish uchun `class MeningXato < StandardError` meros olinadi va `raise MeningXato, 'xabar'` orqali ko'tariladi.",
        """Maxsus xato ushlandi: Balansda yetarli mablag' mavjud emas! (Kerak: 120000, Mavjud: 50000)"""
    )
]

for i in range(506, 551):
    TASKS_11.append((
        i,
        f"Xatoliklarni boshqarish amaliyoti #{i - 500}",
        f"{i}-vazifada mustahkam xatoliklarni ushlash va jurnalga qayd etishni bajaring.",
        f"""begin
  qiymat = {i} * 2
  puts "Qiymat: #{{qiymat}}"
rescue => e
  puts "Xato: #{{e.message}}"
end
""",
        f"Ushbu {i}-topshiriq istisnolarni boshqarish, rescue va dastur barqarorligini mustahkamlaydi.",
        f"Qiymat: {i * 2}"
    ))

register_topic("gen_11_exceptions.py", "ruby_11_xatoliklarni_boshqarish_exceptions.md", 501, TASKS_11)
