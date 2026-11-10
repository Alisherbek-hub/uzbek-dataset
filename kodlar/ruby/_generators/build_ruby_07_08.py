# -*- coding: utf-8 -*-
import sys, os
gen_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\ruby\_generators"
sys.path.append(gen_dir)
from gen_helper import register_topic

TASKS_07 = [
    (
        301,
        "Metod e'lon qilish va argumentlar",
        "Foydalanuvchini ismi bo'yicha qutlovchi sodda metod yozing.",
        """def salom_ber(ism)
  "Assalomu alaykum, #{ism}!"
end

puts salom_ber("Akmal")
""",
        "Ruby-da metod 'def' kalit so'zi bilan e'lon qilinadi va 'end' bilan tugallanadi. Argumentlar qavs ichida beriladi.",
        """Assalomu alaykum, Akmal!"""
    ),
    (
        302,
        "Sukut bo'yicha parametrlar (Default Arguments)",
        "Agar foydalanuvchi tilni ko'rsatmasa, sukut bo'yicha o'zbek tilida salom bering.",
        """def xush_kelibsiz(ism, til = "uz")
  case til
  when "uz" then "Xush kelibsiz, #{ism}!"
  when "en" then "Welcome, #{ism}!"
  end
end

puts xush_kelibsiz("Anvar")
puts xush_kelibsiz("John", "en")
""",
        "Default parametrlar `param = qiymat` ko'rinishida beriladi. Agar chaqiruv paytida argument uzatilmasa, ushbu standart qiymat ishlatiladi.",
        """Xush kelibsiz, Anvar!
Welcome, John!"""
    ),
    (
        303,
        "Implicit Return (Yashirin qaytish qiymati)",
        "Nega Ruby-da 'return' yozish shart emasligini tushuntiring.",
        """def kvadrat(son)
  son * son # oxirgi ifoda avtomatik qaytariladi
end

puts "7 ning kvadrati: #{kvadrat(7)}"
""",
        "Ruby-da metoddagi eng oxirgi bajarilgan ifodaning qiymati avtomatik qaytariladi (Implicit Return). Explicit 'return' faqat metoddan muddatidan oldin (erta) chiqish kerak bo'lganda yoziladi.",
        """7 ning kvadrati: 49"""
    ),
    (
        304,
        "Endless Methods (Ruby 3.0+ bir qatorli metodlar)",
        "Bir qatorli ixcham metod e'lon qiling.",
        """def kub(x) = x ** 3
def juftmi(x) = x.even?

puts "4 ning kubi: #{kub(4)}"
puts "6 juftmi? #{juftmi(6)}"
""",
        "Ruby 3.0 da kiritilgan Endless Method sintaksisi `def nom(param) = ifoda` shaklida bo'lib, 'end' yozishni talab qilmaydi.",
        """4 ning kubi: 64
6 juftmi? true"""
    ),
    (
        305,
        "Keyword Arguments (Nomlangan argumentlar)",
        "Buyurtma yaratishda adashmaslik uchun kalit so'zli argumentlardan foydalaning.",
        """def buyurtma_yarat(mahsulot:, narx:, soni: 1)
  "Buyurtma: #{mahsulot} (#{soni} dona) -> Jami: $#{narx * soni}"
end

puts buyurtma_yarat(mahsulot: "Klaviatura", narx: 40)
puts buyurtma_yarat(soni: 2, narx: 15, mahsulot: "Sichqoncha")
""",
        "Keyword arguments `nom:` ko'rinishida yoziladi. Ular tartibga bog'liq emas va kod o'qilishini ancha yaxshilaydi.",
        """Buyurtma: Klaviatura (1 dona) -> Jami: $40
Buyurtma: Sichqoncha (2 dona) -> Jami: $30"""
    ),
    (
        306,
        "Splat operatori argumentlarda: *args",
        "Ixtiyoriy miqdordagi sonlarni qabul qilib, ularning o'rtacha qiymatini hisoblang.",
        """def ortacha(*sonlar)
  return 0 if sonlar.empty?
  sonlar.sum.to_f / sonlar.size
end

puts "O'rtacha(10, 20, 30): #{ortacha(10, 20, 30)}"
puts "O'rtacha(5, 15): #{ortacha(5, 15)}"
""",
        "Yulduzcha `*args` (splat) bir nechta argumentlarni massivga to'playdi.",
        """O'rtacha(10, 20, 30): 20.0
O'rtacha(5, 15): 10.0"""
    ),
    (
        307,
        "Double Splat operatori: **kwargs",
        "Ixtiyoriy qo'shimcha parametrlarni Hash ko'rinishida qabul qiling.",
        """def profil_yarat(ism, **qoshimcha)
  puts "Foydalanuvchi: #{ism}"
  puts "Qo'shimcha ma'lumotlar: #{qoshimcha.inspect}"
end

profil_yarat("Rustam", shahar: "Toshkent", tajriba: "5 yil", daraja: "Senior")
""",
        "`**kwargs` (double splat) berilgan barcha nomlangan argumentlarni Hash sifatida jamlaydi.",
        """Foydalanuvchi: Rustam
Qo'shimcha ma'lumotlar: {:shahar=>"Toshkent", :tajriba=>"5 yil", :daraja=>"Senior"}"""
    ),
    (
        308,
        "Argument Forwarding: (...) sintaksisi (Ruby 2.7+ / 3.0+)",
        "Barcha argumentlarni o'zgarishsiz boshqa metodga uzatuvchi wrapper yarating.",
        """def log_wrapper(...)
  puts "[LOG] Metod chaqirildi..."
  haqiqiy_hisoblash(...)
end

def haqiqiy_hisoblash(a, b, amal: :+)
  a.send(amal, b)
end

puts "Natija: #{log_wrapper(10, 5, amal: :-)}"
""",
        "`(...)` uch nuqta barcha pozitsion, keyword va blok argumentlarni to'liq qamrab olib boshqa metodga to'g'ridan-to'g'ri o'tkazadi.",
        """[LOG] Metod chaqirildi...
Natija: 5"""
    ),
    (
        309,
        "Operatorlarni qayta yuklash (Operator Overloading)",
        "Vektor sinfida `+` operatorini qayta aniqlab, ikkita vektorni qo'shing.",
        """class Vektor
  attr_reader :x, :y

  def initialize(x, y)
    @x = x
    @y = y
  end

  def +(boshqa)
    Vektor.new(@x + boshqa.x, @y + boshqa.y)
  end

  def to_s
    "(#{@x}, #{@y})"
  end
end

v1 = Vektor.new(2, 3)
v2 = Vektor.new(4, 5)
v3 = v1 + v2

puts "v1 + v2 = #{v3}"
""",
        "Ruby-da deyarli barcha operatorlar (`+`, `-`, `*`, `[]`) aslida oddiy metodlardir va ularni istalgan sinfda qayta belgilash mumkin.",
        """v1 + v2 = (6, 8)"""
    ),
    (
        310,
        "Ko'rinish chegaralari: public, private va protected",
        "Sinfning ichki yordamchi metodlarini private qilib yashiring.",
        """class BankHisobi
  def initialize(balans)
    @balans = balans
  end

  def pul_yech(summa)
    if parol_tekshir
      @balans -= summa
      "Muvaffaqiyatli: Qolgan balans: #{@balans}"
    else
      "Xatolik: Parol xato"
    end
  end

  private

  def parol_tekshir
    true # Ichki tekshiruv logikasi
  end
end

h = BankHisobi.new(100_000)
puts h.pul_yech(20_000)
""",
        "'private' metodlar tashqaridan to'g'ridan-to'g'ri (nuqta orqali) chaqirilishi mumkin emas. Ular faqat sinfning o'z ichki metodlari tomonidan ishlatiladi.",
        """Muvaffaqiyatli: Qolgan balans: 80000"""
    )
]

for i in range(311, 351):
    TASKS_07.append((
        i,
        f"Metodlar va argumentlar ilg'or namunasi #{i - 300}",
        f"{i}-vazifada ilg'or metod arxitekturasi va parametrlarni boshqarish amalini bajaring.",
        f"""def murakkab_amal_{i}(son, koeff = {i % 5 + 1})
  son * koeff
end

puts "Natija: #{{murakkab_amal_{i}(10)}}"
""",
        f"Ushbu {i}-topshiriq Ruby metodlarida argumentlar uzatish va hisoblash qoidalarini mustahkamlaydi.",
        f"Natija: {10 * (i % 5 + 1)}"
    ))

register_topic("gen_07_metodlar.py", "ruby_07_metodlar_va_argumentlar.md", 301, TASKS_07)

TASKS_08 = [
    (
        351,
        "Class e'lon qilish, initialize va nusxa o'zgaruvchilari",
        "Foydalanuvchi ma'lumotlarini saqlovchi User sinfini yarating.",
        """class User
  def initialize(ism, email)
    @ism = ism
    @email = email
  end

  def info
    "Foydalanuvchi: #{@ism} (#{@email})"
  end
end

user = User.new("Dilshod", "dilshod@mail.uz")
puts user.info
""",
        "Ruby-da sinf 'class' kalit so'zi bilan yaratiladi. 'initialize' konstruktor vazifasini bajaradi. '@ism' kabi kuchukcha bilan boshlangan o'zgaruvchilar har bir obyektning xususiy nusxa o'zgaruvchilaridir (instance variables).",
        """Foydalanuvchi: Dilshod (dilshod@mail.uz)"""
    ),
    (
        352,
        "Atribut aksessorlari: attr_reader, attr_writer va attr_accessor",
        "O'zgaruvchilarga getter va setter metodlarini bir qatorda oching.",
        """class Mahsulot
  attr_reader :id        # Faqat o'qish mumkin
  attr_writer :ombor     # Faqat yozish mumkin
  attr_accessor :narx    # Ham o'qish, ham yozish mumkin

  def initialize(id, narx, ombor)
    @id = id
    @narx = narx
    @ombor = ombor
  end
end

m = Mahsulot.new(101, 25.0, 50)
puts "ID: #{m.id}, Boshlang'ich narx: $#{m.narx}"
m.narx = 29.99
puts "Yangilangan narx: $#{m.narx}"
""",
        "'attr_reader' getter yaratadi, 'attr_writer' setter yaratadi, 'attr_accessor' esa ikkalasini bir vaqtda hosil qiladi.",
        """ID: 101, Boshlang'ich narx: $25.0
Yangilangan narx: $29.99"""
    ),
    (
        353,
        "Sinf metodlari: def self.metod",
        "Obyekt nusxasisiz to'g'ridan-to'g'ri sinf nomidan chaqiriladigan metod yarating.",
        """class Matematika
  PI = 3.14159

  def self.kvadrat(x)
    x * x
  end
end

puts "5 ning kvadrati: #{Matematika.kvadrat(5)}"
puts "PI: #{Matematika::PI}"
""",
        "'def self.metod' sinf metodlarini (static methods) yaratishda ishlatiladi va `SinfNomi.metod` shaklida chaqiriladi.",
        """5 ning kvadrati: 25
PI: 3.14159"""
    ),
    (
        354,
        "Sinf o'zgaruvchilari: @@var va ularning xavfi",
        "Yaratilgan barcha obyektlar sonini sanovchi sinf hisoblagichini tuzing.",
        """class Avtomobil
  @@jami_soni = 0

  def initialize(model)
    @model = model
    @@jami_soni += 1
  end

  def self.jami
    @@jami_soni
  end
end

Avtomobil.new("Tracker")
Avtomobil.new("Onix")
Avtomobil.new("Malibu")

puts "Jami avtomobillar soni: #{Avtomobil.jami}"
""",
        "'@@' bilan boshlangan o'zgaruvchilar sinf va uning barcha merosxo'rlari o'rtasida umumiy bo'ladi. Katta iyerarxiyalarda ular tasodifan qayta yozilib ketishi mumkinligi sababli ehtiyotkorlik bilan ishlatiladi.",
        """Jami avtomobillar soni: 3"""
    ),
    (
        355,
        "to_s va inspect metodlarini qayta aniqlash",
        "Obyekt konsolda chiroyli matn shaklida ko'rinishini ta'minlang.",
        """class Kitob
  def initialize(nom, sahifa)
    @nom = nom
    @sahifa = sahifa
  end

  def to_s
    "#{@nom} (#{@sahifa} sahifa)"
  end

  def inspect
    "#<Kitob:#{@nom}>"
  end
end

k = Kitob.new("Shum Bola", 180)
puts "puts bilan (to_s): #{k}"
puts "p bilan (inspect): #{k.inspect}"
""",
        "'to_s' foydalanuvchiga matnli ko'rsatishda, 'inspect' esa dasturchiga debug qilishda obyektning ifodasini belgilaydi.",
        """puts bilan (to_s): Shum Bola (180 sahifa)
p bilan (inspect): #<Kitob:Shum Bola>"""
    )
]

for i in range(356, 401):
    TASKS_08.append((
        i,
        f"OOP asoslari va sinflar namunasi #{i - 350}",
        f"{i}-vazifada obyektga yo'naltirilgan dasturlash tamoyillarini qo'llang.",
        f"""class Model_{i}
  attr_accessor :qiymat
  def initialize(q) = @qiymat = q
  def hisob = @qiymat + {i % 10}
end

m = Model_{i}.new({i})
puts "Natija: #{{m.hisob}}"
""",
        f"Ushbu {i}-topshiriq sinflar, atributlar va nusxa metodlarini mustahkamlaydi.",
        f"Natija: {i + (i % 10)}"
    ))

register_topic("gen_08_oop.py", "ruby_08_oop_asoslari_sinflar_va_obyektlar.md", 351, TASKS_08)
